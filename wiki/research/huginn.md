# Huginn-0125: Scaling Test-Time Compute with Recurrent Depth

Huginn-0125 (Geiping et al., 2025; arXiv 2502.05171) is a 3.5B-parameter decoder-only language model that replaces fixed-depth stacking with a **depth-recurrent** architecture: a single shared transformer block is iterated $r$ times per token before logit projection, where $r$ is variable at both train and test time. Trained on 800B tokens on Frontier (4096 AMD MI250X GPUs), the model improves on reasoning benchmarks with increasing $r$, reaching compute-equivalent performance of a ~50B-parameter fixed-depth model at $r = 48$–$64$. The central claim is that latent recurrence is a third axis of LLM scaling, complementary to parameter count and chain-of-thought token scaling.

## Architecture

The architecture is structured as three functional groups: **prelude** $P$, **core** $R$ (recurrent), and **coda** $C$.

**Forward pass** for input tokens $x \in V^n$ and recurrence count $r$:

$$e = P(x)$$
$$s_0 \sim \mathcal{N}(0,\, \sigma^2 I_{n \cdot h})$$
$$s_i = R(e,\, s_{i-1}), \quad i \in \{1, \ldots, r\}$$
$$p = C(s_r)$$

The hidden state $s_i \in \mathbb{R}^{n \times h}$ is the full sequence residual stream. $e \in \mathbb{R}^{n \times h}$ is injected at every iteration of $R$; it is never updated.

**Layer shape** — the model is parameterised by the triplet $(l_P, l_R, l_C)$:

| Group | Layers | Function |
|-------|--------|----------|
| Prelude $P$ | $l_P = 2$ | Embeds tokens via $\gamma E(x)$ then 2 transformer layers; produces $e$ |
| Core $R$ | $l_R = 4$ | Shared recurrent block, iterated $r$ times; produces $s_r$ |
| Coda $C$ | $l_C = 2$ | 2 transformer layers + RMSNorm $n_c$ + tied-embedding projection $E^T$ |

At training, $\bar{r} = 32$, giving effective depth $2 + 4r + 2 = 132$ at $r = 32$. Parameter budget: ~1.5B in prelude + head, ~1.5B in core, ~0.5B in tied embeddings; total 3.5B.

**Hidden dimension:** $h = 5280$; 55 attention heads of size 96; MLP inner dim 17920; vocabulary $|V| = 65536$ (BPE).

**Input injection** — $R$ begins with a learned adapter matrix $A_{\text{inj}} : \mathbb{R}^{2h} \to \mathbb{R}^h$ applied to $[s_{i-1} \| e]$ (concatenation along the feature dimension). The result feeds into $l_R = 4$ transformer layers.

**Normalization ("sandwich" format)** — every layer inside all three groups uses the pattern:

$$\hat{x}_l = n_2(x_{l-1} + \text{Attn}(n_1(x_{l-1})))$$
$$x_l = n_4(\hat{x}_l + \text{MLP}(n_3(\hat{x}_l)))$$

Four RMSNorm instances per layer ($n_1$–$n_4$, all learned). The coda adds a fifth RMSNorm $n_c$ after the final core output $s_r$, before the tied-embedding projection. This sandwich scheme was found empirically necessary to prevent hidden-state collapse at scale.

**Positional encoding:** RoPE with base 50000. Learnable biases on $Q$ and $K$ only.

**State initialization:** $s_0 \sim \mathcal{N}(0, \sigma_s^2 I)$ with $\sigma_s^2 = \frac{2}{5}$ (truncated at $3\sigma$). Path independence — convergence of $s_r$ to the same attractor regardless of $s_0$ — is verified empirically.

**Training recurrence distribution** $\Lambda$: log-normal Poisson with $\bar{r} = 32$:

$$\tau \sim \mathcal{N}(\log \bar{r} - \tfrac{1}{2}\sigma^2,\, \sigma), \quad r \sim \text{Poisson}(e^\tau) + 1$$

Backpropagation is truncated to the last $k = 8$ iterations; prelude $P$ still receives gradients because $e$ is injected at every step.

## EXP1_INSERTION_POINT

**Where to insert the router.** The recurrent loop is the only place where per-token compute can be intercepted. The natural hook is **after each core-block output, before the next iteration begins** — i.e., between $s_i = R(e, s_{i-1})$ and the start of $R(e, s_i)$.

Concretely, in `recpre/raven_modeling_minimal.py` (or equivalently `recpre/model_dynamic.py`), the loop has the structure:

```python
for i in range(r):
    s = core_block(s, e)          # ← router observes s here, after core block
    # [INSERT ROUTER HERE]
```

**Tensor the router observes:** $s_i \in \mathbb{R}^{n \times h}$, where $n$ is sequence length and $h = 5280$. This tensor has **not** yet been normalized by $n_c$ (the final RMSNorm applied by the coda); it is the raw residual-stream output of the last layer of the core block ($l_R = 4$). If the router needs to produce a normalized signal, it must apply its own norm.

**What the router controls:** The decision of whether to continue iterating (standard loop), exit early (break and route $s_i$ directly to coda), or route to an alternative branch. The router must not touch $e$ — the prelude embedding is frozen and injected read-only each iteration.

**Internal gating Huginn does not use:** Huginn has no internal per-iteration gating or halting mechanism — it is a "dumb" fixed-$r$ loop with no learned stopping signal. The KL-divergence adaptive exit described in §6.1 of the paper is a post-hoc inference heuristic, not a trained gate. This means the router has a clean insertion surface: there is no existing conditional pathway to respect or conflict with. The router's output must remain in $\mathbb{R}^{n \times h}$ (or be a routing decision that selects which block to run next), and must pass a valid $s$ into either the next iteration of $R$ or directly to $C$.

**Frozen-weight constraint:** Exp 1 freezes all Huginn weights. The adapter $A_{\text{inj}}$, all transformer layers in $P$, $R$, $C$, and the tied embedding $E$ are fixed. The router is a new module trained on top, receiving $s_i$ as input and outputting either a routing decision or a modified hidden state. Gradients do not flow into Huginn weights.

**Code repo:** `seal-rg/recurrent-pretraining`. The HF-compatible inference file `recpre/raven_modeling_minimal.py` is the cleanest entry point; `recpre/model_dynamic.py` is the training version. Both expose the recurrence loop explicitly.

**R4 anomaly warning — final step only.** The "observes $s_i$ unnormalized" spec above is correct for steps $i \in \{1, \ldots, r-1\}$. The final step ($i = r$, i.e., immediately after R4 on the last recurrence) is a special case. Because R4's hidden state serves a dual role — feeding both the next R1 input and the Coda C1 — its representational structure is incoherent under the standard logit lens at the router's insertion point. A simple MLP router reading raw $s_r$ may pick up this incoherent structure and make poorly grounded routing decisions specifically at the last step.

*Recommended mitigations (either):*
1. **Coda lens pass-through:** Before feeding $s_r$ to the router head, pipe it through Huginn's own Coda module (C1, C2). This is the representational basis R4 was trained to produce; it yields numerically interpretable tokens. This adds a forward pass through $l_C = 2$ frozen transformer layers.
2. **Step-index conditioning:** Augment the router's input with a learned or one-hot step-index embedding so the router can learn step-specific projections, handling R4's dual-role output differently from R1–R3.

The R4 anomaly is reported in [[latent-cot-huginn]] (arXiv:2507.02199); see that page once created. The anomaly does not affect the logical correctness of the insertion point for early-exit decisions at steps $i < r$; it is specifically the full-depth final step where the representational mismatch applies.

## Training details

- **Data:** 800B tokens. Mixture skewed toward code and math with general webtext. All sources public; uploaded to `tomg-group-umd/huginn-dataset` (4096 parquet shards, one per GPU). BPE tokenizer (65536 vocab) trained on the instruction split of the pretraining corpus for domain efficiency.
- **Context length:** 4096 tokens; sequences packed with document-end truncation to avoid the grounding problem.
- **Optimizer:** AdamW ($\beta_1 = 0.9$, $\beta_2 = 0.95$, $\eta = 5 \times 10^{-4}$) with update clipping and no $\varepsilon$ (Everett et al., 2024). Gradient clip at 1. Constant LR schedule with 4096-step warmup; no cooldown.
- **Hardware:** 4096 AMD MI250X GPUs on Oak Ridge Frontier; bfloat16 mixed precision; data parallelism + ZeRO optimizer sharding; gradient checkpointing per iteration. Global batch size 16M tokens/step ($1 \times 4096$ per GPU × 4096 GPUs). 21 training segments of ≤12 hours scheduled Dec 2024.
- **Throughput:** 52–64 TFLOP/s per GPU (41–51% AFU) at 4096 nodes; 1–1.2M tokens/second. Single-node speed 108.75 TFLOP/s (87% AFU).
- **Initialization:** Takase et al. (2024) scheme: $\sigma_h^2 = \frac{2}{5h}$ for standard layers, $\sigma_{\text{out}}^2 = \frac{1}{5hl}$ for output-projections ($l = 132$ effective layers). Truncated normal at $3\sigma$.
- **Weight averaging:** Post-training EMA over last 75 checkpoints (dilation 7, $\beta = 0.9$); improves GSM8k to 47.23% flex / 38.59% strict at $r = 64$.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (block isolation / swappability) | Medium | Core block is maximally isolated: single shared module with clean input/output contract $(e, s_{i-1}) \to s_i$. Not designed for block swapping, but the structure naturally supports it. |
| **G2** (dynamic per-block parameter budget) | Low-Medium | $r$ is a compute-budget knob, not a parameter-budget knob. Variable-$r$ training demonstrates that compute per token is learnable; no per-block parameter scaling. |
| **G3** (token-conditional routing) | **High — primary testbed** | Each token position has an independent hidden-state trajectory $\{s_i^{(t)}\}_{i=1}^r$. A router inserted after each core iteration can condition on $s_i^{(t)}$ to make per-token, per-iteration decisions. This is the base model for Exp 1. |

## Credibility

- arXiv 2502.05171; submitted Feb 2025, revised Feb 17 2025. Not yet peer-reviewed at a venue; tech-report status.
- Weights: `tomg-group-umd/huginn-0125` (HuggingFace). vLLM v1 plugin available in the repo's `vllm/` folder.
- Code: `seal-rg/recurrent-pretraining` (Apache-2.0). Training data: `tomg-group-umd/huginn-dataset`.
- Replication: full training replicated at scale on Frontier only. Two earlier training runs failed (hidden-state collapse and recurrence collapse), documented in §4.3 and Figure 5. The final run required specific sandwich norm + reduced LR ($4 \times 10^{-5}$) at scale. Small-scale replications are feasible; large-scale requires AMD cluster access and custom distributed implementation.
- No known follow-up papers as of capture date (2026-05-26); the approach is novel at scale.

## Empirical claims

**Standard benchmarks (zero-shot, Table 1, $r = 32$):**

| Task | Huginn ($r = 32$) | OLMo-7B | OLMo-7B-0724 |
|------|-------------------|---------|--------------|
| ARC-E | 69.91 | 68.81 | 74.28 |
| ARC-C | 38.23 | 40.27 | 43.43 |
| HellaSwag | 65.21 | 75.52 | 77.76 |
| MMLU | 31.38 | 28.39 | 50.18 |
| WinoGrande | 59.43 | 67.09 | 67.17 |

Huginn is roughly competitive with first-generation OLMo-7B (2.5T tokens) at 3.5B parameters and 0.8T tokens; it lags behind later OLMo generations with larger, curated datasets.

**Math and code ($r = 32$, Table 2–3):**

| Task | Huginn | OLMo-7B-0724 | OLMo-2-1124-7B |
|------|--------|--------------|----------------|
| GSM8k (flex/strict, w/ sys prompt) | 38.13 / 24.87 | 28.73 / 28.89 | 66.79 / 66.72 |
| GSM8k CoT (flex/strict, w/ sys prompt) | 42.08 / 34.80 | 28.89 / 28.89 | 66.19 / 61.94 |
| MBPP (pass@1) | 24.80 | 25.60 | — |
| HumanEval (pass@1) | 23.17 | 20.12 | — |

Significantly surpasses early OLMo variants on math; code beats general-purpose open models but not code-specialist models (StarCoder2-3B: 43.00 MBPP).

**Recurrence scaling:** At $r = 1$, Huginn scores near or below a fixed-depth baseline; at $r = 32$, it substantially outperforms (ARC-C: 38.23 vs. 26.96 fixed-depth baseline at same 180B-token snapshot). GSM8k CoT at $r = 1$: 0.00/0.00; at $r = 32$: 34.80/42.08. HellaSwag saturates at $r \approx 8$; GSM8k continues to improve to $r = 64$.

**Non-recurrent comparison (Table 4):** At 180B tokens, the recurrent model at $r = 32$ scores 9.02/10.24 on GSM8k CoT vs. 1.82/2.20 for the fixed-depth baseline — a 5× advantage early in training.

## Open questions / failure modes

- **Training instability at scale:** Two failed runs before a stable configuration was found. The specific combination of sandwich norm + low LR + learned adapter appears necessary; generalization to other scales or architectures is unclear.
- **LR never cooled down:** The constant-LR schedule means the checkpoint is not fully converged; weight averaging provides a partial substitute.
- **Data mixture untested:** The math/code-heavy mixture was not ablated; standard NLP benchmarks (HellaSwag, WinoGrande) are mediocre relative to model size, likely due to data skew.
- **Router interaction with path independence:** Huginn is designed for path-independent convergence (the attractor $s^*$ is independent of $s_0$). A trainable router that modifies $s_i$ mid-loop may disrupt this property, leading to convergence failure or instability in the remaining iterations.
- **KV-cache structure under variable $r$:** Per-token adaptive exits (§6.1) attend to the deepest available KV cache from previous tokens; a router that exits different tokens at different iterations must handle this same mismatch, potentially with different caching strategy.
- **No per-token routing at train time:** Huginn trains with a single $r$ per micro-batch (locked-step sampling). A router that produces per-token exit decisions introduces gradient flow that was never seen in pretraining; the core block has no incentive to produce easily-routed signals.
- **No official instruct/RLHF checkpoint:** The released weights are base pretraining only; downstream fine-tuning on Huginn has not been publicly documented.

## Latent CoT probing — Lu et al. 2025

Lu et al. (arXiv:2507.02199, Brown / Harvard, Jul 2025) probe whether Huginn's recurrent hidden states implement an interpretable latent chain-of-thought on arithmetic tasks. Code: `https://github.com/wenquanlu/huginn-latent-cot`.

**No interpretable latent CoT.** Rank-trajectory analysis on arithmetic tasks shows no temporal separation between intermediate-result tokens and final-result tokens. Both token types descend together in early recurrent steps. The expected signature — intermediate token rises first, then falls as the final token rises — is absent. Latent recurrence computes differently from explicit CoT, not as a compressed version of it.

**R4 dual-role anomaly.** Huginn's R4 block (the final of the four core layers, executed on the last recurrence step) feeds both the next recurrence cycle (back to R1) and the Coda (C1). This forces R4's hidden state to serve two representational masters simultaneously, producing a sharp interpretability inconsistency:

- *Logit lens* applied to the raw R4 hidden state → incoherent tokens.
- *Coda lens* (piping the identical R4 hidden state through C1–C2) → numerically interpretable tokens.
- R1–R3 behave the *opposite*: logit lens is interpretable there; coda lens is not.

No single lens is universally applicable. Interpretability is per-block and per-method. The paper terms this the "dual-role" anomaly of the final recurrent step.

**Depth-scaling ceiling.** GSM8K accuracy without explicit CoT as a function of recurrence steps $T$:

| $T$ | GSM8K (no CoT) |
|-----|----------------|
| 4 | 3.11% |
| 8 | 4.47% |
| 16 | 4.78% |
| 32 | 4.93% |
| 64 | 4.70% |
| 128 | 4.93% |
| 256 | 4.62% |

Performance plateaus near 5% and degrades slightly at very high step counts. With explicit CoT, Huginn achieves 24.87% / 38.13% (strict/flexible) — roughly 5–8× higher than latent compute alone. This is consistent with the rapid fixed-point convergence finding in [[mechanistic-looped-lms]]: once $s_i$ converges to its attractor, additional steps cannot inject new information.

## Source

- `raw/research/loop-computation/05-huginn-abs.md`
- `raw/research/loop-computation/07-huginn-github.md`
- `raw/research/loop-computation/13-huginn-pdf.md`
- `raw/research/recurrent-reasoning/04-latent-cot-huginn-abs.md`
- `raw/research/recurrent-reasoning/06-latent-cot-huginn-pdf.md`

## Related

[[universal-transformers]], [[parcae]], [[mechanistic-looped-lms]], [[adaponderlm]], [[loopformer]], [[experiments/exp1-router-replication]]
