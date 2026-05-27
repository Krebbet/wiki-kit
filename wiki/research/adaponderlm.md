# AdaPonderLM: Gated Pondering Language Models with Token-Wise Adaptive Depth

AdaPonderLM (Song et al., LUMIA Lab / SJTU, arXiv 2603.01914, Mar 2026) extends PonderLM-style vertical recurrence with per-token early exit learned entirely self-supervised during pretraining. Iteration-specific MLP gates drive a monotonic halting mask; a KV-reuse mechanism ensures halted tokens present frozen key-value states to subsequent iterations without irregular control flow, giving train–test consistency and FlashAttention compatibility. Across Pythia 70M–2.8B, AdaPonderLM achieves ~10% inference FLOP reduction versus fixed-depth PonderLM at matched or better perplexity.

## KV-reuse mechanism

This is the concrete solution to Technical Challenge 3 (attention semantics across loop iterations) for per-token routing.

**Setup.** Let $K^{i,\ell}, V^{i,\ell} \in \mathbb{R}^{B \times H \times n \times d_h}$ be the key/value tensors at iteration $i$, layer $\ell$, computed from the current iteration's hidden states. Let $K^{i-1,\ell}, V^{i-1,\ell}$ be the corresponding tensors from the previous iteration (cached). The persistent binary mask $m^i \in \{0,1\}^n$ has $m^i_t = 1$ if token $t$ is still active (not yet halted) at iteration $i$.

**Mask definition.** The mask is initialized to all-ones and updated monotonically:

$$m^0 = \mathbf{1}, \qquad m^{i+1} = m^i \odot \mathbf{1}(s^i \geq \tau)$$

where $s^i = \text{sigmoid}(\text{MLP}_i(h^i))$ is the per-token gate probability and $\tau = 10^{-4}$ is the pruning threshold. Once $m^i_t = 0$, it stays zero — halting is irreversible.

**KV replacement.** After computing $K^{i,\ell}$ and $V^{i,\ell}$ from the backbone in iteration $i$, the caches are aligned token-wise before attention:

$$K_\text{aligned}^{i,\ell} \leftarrow \text{where}(m^i,\; K^{i,\ell},\; K^{i-1,\ell})$$
$$V_\text{aligned}^{i,\ell} \leftarrow \text{where}(m^i,\; V^{i,\ell},\; V^{i-1,\ell})$$

The mask $m^i \in \{0,1\}^n$ is broadcast to shape $B \times 1 \times n \times 1$ to match the cache tensor dimensions. Semantically: active tokens ($m^i_t = 1$) get freshly computed K/V; halted tokens ($m^i_t = 0$) silently reuse their K/V from iteration $i-1$. Attention then runs normally over the aligned caches — all $n$ token positions remain present and addressable.

**Why this avoids irregular control flow.** Alternatives (masking out halted tokens from the attention computation, running variable-length sequences per iteration) require index-gather/scatter operations or ragged batches that break optimized attention kernels. The `where` operation is a uniform elementwise select over full-sized tensors: it does not change the attention operator itself, is expressible as a single fused kernel, and is fully compatible with FlashAttention. The trade-off is that the backbone still processes all $n$ token positions in every iteration — FLOP reduction comes only from skipping the gated embedding update (Eq. 9), not from skipping backbone compute for halted tokens.

**Memory implications.** Two full sets of KV caches per layer must be resident simultaneously: $\{K^{i-1,\ell}, V^{i-1,\ell}\}$ (previous, for halted-token reuse) and $\{K^{i,\ell}, V^{i,\ell}\}$ (current, for active tokens). Peak memory per layer is $2 \times B \times H \times n \times d_h \times \text{sizeof}(\text{dtype})$. At $K$ iterations, only two consecutive iteration caches need coexist (the others can be freed after the `where` step), so the overhead is a constant 2× per-layer KV memory rather than $K$×.

## Halting mechanism

AdaPonderLM uses a custom gate-based scheme inspired by ACT/PonderNet but implemented as learned MLP gates rather than a probabilistic halting variable.

At iteration $i$, an iteration-specific two-layer MLP (not shared across iterations) produces a scalar gate logit per token:

$$g^i = \text{MLP}_i(h^i), \qquad s^i = \text{sigmoid}(g^i) \in (0,1)^n$$

Token $t$ halts at iteration $i$ if $s^i_t < \tau$ ($\tau = 10^{-4}$). The persistent mask $m^i$ (Eq. above) enforces monotonicity. Once halted, the token's embedding is frozen (the gated update in Eq. 9 contributes zero because $m^{i+1}_t = 0$), and its KV states are reused via the `where` operation.

Key design choices, each ablated:

- **Per-iteration independent MLPs.** A single shared MLP collapses to degenerate solutions (all-halt or all-active). Independent $\text{MLP}_i$ per iteration provides sufficient inductive bias for a calibrated policy.
- **bottomK selection.** Removing the bottomK mechanism (see Training objective) causes further collapse. The loss must explicitly penalize the smallest gate values to push the model away from full-depth recurrence.
- **Threshold vs. learned $p_h$.** Unlike PonderNet's probabilistic $\lambda_n$ (cumulative halting probability with KL regularization), AdaPonderLM uses a hard threshold with a penalty on the bottom-$k$ gate values. This avoids the need for a per-step geometric prior and is simpler to pretrain from scratch.

## Training objective

Two-stage training:

**Stage 1 (warm-up):** Train with cross-entropy only, no halting pressure:

$$\mathcal{L} = \mathcal{L}_\text{CE}$$

**Stage 2 (pondering regularization):** Add a ponder loss:

$$\mathcal{L} = \mathcal{L}_\text{CE} + \lambda \mathcal{L}_\text{ponder}$$

The ponder loss penalizes the bottom-$k_s$ fraction of gate values across all tokens and all iterations in the batch:

$$\mathcal{L}_\text{ponder} = \text{bottomK}_{k_s}(g)$$

where $g$ collects all gate values $\{g^i_t\}$ and $\text{bottomK}_{k_s}(\cdot)$ returns the mean of the smallest $k_s$ fraction. This directly incentivizes low gate scores (i.e., early halting) without specifying which tokens or which iterations. The fraction $k_s$ is warmed up linearly from $0$ to $k_\text{max}$ between steps $S_0$ (Stage 2 start) and $S_1$:

$$k_s = \frac{s - S_0}{S_1 - S_0} \cdot k_\text{max}$$

Default: $k_\text{max} = 0.1$, $\lambda = 0.1$. Both hyperparameters show monotonic loss degradation as they increase — smaller values are preferred for quality, but larger values are required to achieve non-trivial pruning rates.

For continued pretraining from a PonderLM checkpoint: gate MLPs are first trained alone for 1B tokens (backbone frozen), then all parameters are jointly fine-tuned.

## Architecture integration

AdaPonderLM is built on **PonderLM** (Zeng et al., 2025b), itself a vertical recurrent LM that refines token embeddings across $K$ iterations through a shared Transformer backbone. The PonderLM-style update uses a probability-weighted expectation over vocabulary embeddings as the candidate residual:

$$E^i_\text{upd} = P^i V \in \mathbb{R}^{n \times d}, \qquad P^i = \text{softmax}(z^i)$$

$$E^{i+1}_t = E^i_t + m^{i+1}_t \cdot s^i_t \cdot e^i_t$$

AdaPonderLM adds:
1. Per-iteration MLPs $\{\text{MLP}_i\}_{i=0}^{K-1}$ — small two-layer networks ($4h$ hidden states), one per recurrent step. Total parameter overhead is $K \times O(d^2)$, modest relative to the backbone.
2. The KV-reuse alignment step (Algorithm 2) inserted after each backbone forward pass, before attention (or equivalently, replacing the raw KV in the cache before the attention kernel runs).
3. Stage-2 training with bottomK ponder loss.

Backbone: Pythia suite (GPT-NeoX architecture, decoder-only). Pretrained from scratch at 70M and 410M; continued from PonderLM at 1.4B and 2.8B. All experiments use 4 recurrent iterations as the nominal budget, with AdaPonderLM achieving effective 3.7–3.8× inference FLOPs vs. vanilla Pythia (vs. PonderLM's full 4×). Training data: 26B tokens from the Pile (pretraining), 300–312B tokens (continued pretraining).

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (swappable isolated blocks) | Low | AdaPonderLM shares weights across all recurrent iterations — there is one backbone, not a pool of swappable blocks. The block-isolation problem is orthogonal to per-token halting. |
| **G2** (per-block dynamic parameter allocation) | Indirect | The gate MLPs allocate recurrent depth per token, which is a form of dynamic compute allocation, but it operates over iterations of a single shared block rather than over a pool of distinct parameterized blocks. |
| **G3** (token-conditional routing) | **Direct — solves Exp 1 Option B** | The KV-reuse `where(mask, K_new, K_prev)` mechanism is the concrete, tested solution for per-token routing with attention consistency. Halted tokens freeze their KV states; active tokens get fresh KV; all tokens remain addressable. Directly addresses Technical Challenge 3 for per-token depth routing. |

## Credibility

arXiv 2603.01914 (submitted 2 Mar 2026, revised 11 Mar 2026). LUMIA Lab, Shanghai Jiao Tong University / Shanghai AI Laboratory. No published venue at time of capture — preprint only. No code repository linked from the paper. Ablations on KV-reuse are implicit (the mechanism is central; the paper ablates the MLP sharing and bottomK selection but not a direct comparison of KV-reuse vs. alternative attention consistency strategies). Results span four backbone sizes (70M–2.8B) and multiple benchmarks, lending reasonable empirical coverage for a preprint.

## Empirical claims

- **70M from scratch:** AdaPonderLM (3.8× FLOPs) achieves PPL 14.32 vs. PonderLM (4× FLOPs) PPL 14.40 — best among recurrent baselines at lower compute.
- **410M from scratch:** AdaPonderLM (3.8× FLOPs) PPL 9.87; PonderLM and Loop Transformer at 4× FLOPs achieve PPL 9.72 — comparable, slight deficit for AdaPonderLM.
- **1.4B CPT:** Matches PonderLM val loss 1.92 at 3.7× vs. 4× FLOPs.
- **2.8B CPT:** Matches PonderLM val loss 1.83 at 3.8× vs. 4× FLOPs.
- **Downstream (2.8B, 0-shot):** Average accuracy 59.6% vs. PonderLM 60.4% (+2.2% over Pythia-2.8B baseline) — marginal gap vs. PonderLM.
- **Downstream (2.8B, 5-shot):** Average accuracy 61.1% vs. PonderLM 61.5% (+3.5% over Pythia-2.8B) — within noise.
- **Adaptive vs. fixed policy (iso-FLOPs):** Learned gate consistently beats uniform and geometric fixed-pruning distributions, confirming the gate allocates compute to the right tokens rather than just reducing average depth.
- **NLL–depth correlation:** Tokens halted at Step 2 have the lowest mean NLL (~1.0); Steps 3–4 increasingly retain high-NLL, semantically ambiguous tokens. Staged filter, not a simple difficulty threshold.

## Open questions / failure modes

- **Memory cost of dual KV caches.** Storing $K^{i-1,\ell}$ and $K^{i,\ell}$ simultaneously doubles the per-layer KV footprint during the `where` alignment step. At large $n$ and $L$, this is non-trivial. No memory profiling is reported.
- **Frozen-KV distribution drift.** Halted tokens contribute K/V computed at iteration $i_\text{halt}$ to attention in all later iterations. As active tokens' representations evolve across iterations, the frozen K/V vectors become increasingly stale relative to the current query distribution. The paper assumes this is acceptable (empirically it appears to be), but the magnitude of the resulting cross-iteration distribution mismatch is uncharacterized.
- **Backbone still processes all tokens.** The `where` mechanism preserves regular compute graphs, but the backbone computes full forward passes over all $n$ positions in every iteration. The ~10% FLOP saving comes only from the skipped gated embedding update, not from reduced attention computation. True per-token backbone skipping (as in MoR-style routed computation) would yield larger savings but requires the irregular control flow that `where` was designed to avoid.
- **Sensitivity to $\lambda$ and $k$.** Loss degrades monotonically with both hyperparameters and the pruning rate collapses to near-zero without sufficient regularization. The efficiency–quality frontier is narrow and may require retuning across backbone sizes.
- **Scaling unvalidated.** All experiments use Pythia suite up to 2.8B. Behavior of the gate MLPs and KV-reuse mechanism at 7B+ is unknown.
- **No code release.** Reproducibility relies solely on the paper's algorithm boxes.

## Source

- `raw/research/loop-challenges/04-adaponderlm-abs.md`
- `raw/research/loop-challenges/09-adaponderlm-pdf.md`

## Related

- [[pondernet]] — probabilistic halting inspiration; AdaPonderLM replaces the geometric KL prior with a direct bottomK gate penalty.
- [[calm]] — per-token early exit in the layer dimension (depth routing); uses state-copying rather than KV-reuse for consistency. Complementary approach to the same problem class.
- [[layerskip]] — training-time preparation for early exit via layer dropout; AdaPonderLM achieves similar goals self-supervisedly in a recurrent setting.
- [[mod]] — per-token routing in the iteration/block dimension via top-$k$ selection; no explicit KV-consistency mechanism described.
- [[experiments/exp1-router-replication]] — Exp 1 Option B (per-token routing) directly benefits from the `where(mask, K_new, K_prev)` KV-reuse primitive characterized here.
