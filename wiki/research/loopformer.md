# LoopFormer: Elastic-Depth Looped Transformers for Latent Reasoning via Shortcut Modulation

LoopFormer (Jeddi, Ciccone, Taati; U Toronto / Vector Institute; Feb 2026) trains a weight-tied decoder-only transformer on variable-length loop trajectories, conditioning each pass on a normalized time $t$ and step size $\Delta t$ so that hidden-state representations evolve consistently across budgets rather than stagnating at a fixed point. The key mechanism — sinusoidal Fourier step conditioning modulated through AdaLN-style scale/gate — directly solves the hidden-state observability problem that blocks lightweight halt-head training in Huginn-based routers (Technical Challenge 2, [[experiments/exp1-router-replication]]).

## Stagnant state problem

In a standard weight-tied (looped) transformer $h^{(i)} \leftarrow \Phi_k(h^{(i-1)})$, iterative application of the same block drives hidden states toward a fixed point: $h^{(k)} \approx h^{(k+1)}$ in cosine-similarity terms. The paper calls these *stagnant states*. The paper diagnoses and quantifies stagnation via four geometric metrics:

1. **CKA similarity across loop steps** (Figure 5): depth-elastic baselines (Naive-Loop-EE, TMLT-EE, Base-Loop-EE-Cons) show high pairwise CKA across iterations, indicating the shared block transforms the hidden state by approximately zero net change.
2. **Curvature** (rate of directional change across sequence positions) — flat across iterations in stagnating models.
3. **Anisotropy** (average pairwise cosine similarity of token vectors within a layer) — fails to evolve.
4. **Prompt entropy** (matrix-based spread of token embeddings across feature dimensions) — static.

Stagnation is specifically triggered by **naive early-exit (EE)** in looped architectures: when a model is trained with a fixed $L$ loops but evaluated at $M < L$, the representations at step $M$ are not trained to be informative endpoints. Adding a consistency loss alone (Base-Loop-EE-Cons) does not solve it — without step conditioning the block has no way to know *which* iteration it is computing, so the dynamics cannot differentiate passes. The fixed-point symmetry $\Phi_k(h^*) = h^*$ is the attractor.

## Step conditioning: the fix

LoopFormer reframes iterative refinement as a trajectory in representation space: hidden states evolve from an initial $h^{(0)}$ toward a target at normalized time $t=1$ over a unit-horizon. Each loop $i$ is conditioned on the pair $(t_{i-1}, \Delta_i)$, where:

- $t_{i-1} \in [0,1]$ is the **cumulative normalized time** entering loop $i$; the sequence $0 = t_0 < t_1 < \cdots < t_M = 1$ is the trajectory schedule.
- $\Delta_i = t_i - t_{i-1}$ is the **step size** ("jump") of iteration $i$; short steps signal fine-grained refinement, large steps signal coarse traversal.

The trajectory is constrained to $\sum_{i=1}^{M} \Delta_i = 1$, so a uniform $L$-step schedule has $\Delta_i = 1/L$ for all $i$.

**Fourier feature computation.** Both scalars are separately encoded via fixed sinusoidal Fourier features of width $D_f = 256$ with frequencies:

$$\omega_k = \exp\!\left(-\frac{k-1}{D_f/2 - 1}\log 10{,}000\right), \quad k = 1,\ldots,D_f/2$$

giving per-scalar embedding:

$$\phi(\tau) = \mathrm{MLP}\!\bigl[\cos(\tau\omega_1),\, \sin(\tau\omega_1),\, \ldots,\, \cos(\tau\omega_{D_f/2}),\, \sin(\tau\omega_{D_f/2})\bigr] \in \mathbb{R}^d$$

where the MLP is 2-layer with hidden size $d$ and SiLU nonlinearity. The per-iteration conditioning vector is $\mathbf{c}_i = \phi(t_{i-1}) + \phi(\Delta_i) \in \mathbb{R}^d$.

**Injection point.** $\mathbf{c}_i$ is fed to an AdaLN-style modulator inside every LoopFormer block, producing four scalars $(\alpha_\mathrm{msa}, \alpha_\mathrm{mlp}, \gamma_\mathrm{msa}, \gamma_\mathrm{mlp})$ via a zero-initialized linear head:

$$x \leftarrow x + \alpha_\mathrm{msa} \odot \mathrm{MHSA}\!\bigl(\mathrm{RMSNorm}(x) \odot (1 + \gamma_\mathrm{msa})\bigr)$$
$$x \leftarrow x + \alpha_\mathrm{mlp} \odot \mathrm{FFN}\!\bigl(\mathrm{RMSNorm}(x) \odot (1 + \gamma_\mathrm{mlp})\bigr)$$

The zero-init ensures that at training onset the modulator is a no-op (identity), matching the unmodulated backbone; conditioning is learned incrementally.

**Why this breaks fixed-point symmetry.** The fixed-point equation $\Phi_k(h) = h$ is for an *unmodulated* block. With conditioning, the effective operator at iteration $i$ is $\Phi_k(\cdot;\, \mathbf{c}_i)$, and distinct $(t_{i-1}, \Delta_i)$ produce distinct operators. There is no static $h^*$ satisfying $\Phi_k(h^*;\, \mathbf{c}_i) = h^*$ for all $i$ simultaneously; the system is forced to produce a non-degenerate trajectory. In the Exp 1 halting context: a halt head reading $h^{(k)}$ can now disambiguate "step 3 of 8" from "step 7 of 8" because the hidden states are structurally different — the fixed-point symmetry that collapsed them has been lifted.

## Architecture and training

**Architecture.** LoopFormer is a $(k \otimes L)$ GPT-style decoder-only transformer: $k$ transformer blocks (denoted $\Phi_k$) are applied for up to $L$ iterations. All $k$ blocks share weights across all $L$ iterations; the key novelty is the per-iteration $(t, \Delta t)$ conditioning. Hyperparameters: $d = 2048$, 32 heads, $d_\mathrm{ff} = 5120$, RMSNorm throughout, learned positional embeddings, weight-tied input/output embeddings.

**Training objective.**
$$\mathcal{L} = \mathcal{L}_L + \lambda_1 \mathcal{L}_S + \lambda_2 \mathcal{L}_\mathrm{cons}$$

- $\mathcal{L}_L$: next-token CE on the full $L$-loop trajectory.
- $\mathcal{L}_S$: next-token CE on a sampled shortcut trajectory of length $S \sim \mathcal{U}\{1,\ldots,L-1\}$ with a uniformly drawn step schedule $\boldsymbol{\Delta}_S$.
- $\mathcal{L}_\mathrm{cons} = \|\mathrm{stopgrad}(h^{(L)}) - h^{(S)}\|^2$: stop-gradient L2 alignment of shorter trajectory endpoint to full trajectory (self-distillation).
- $\lambda_1 = \lambda_2 = 0.1$ throughout.

Training overhead: dual-trajectory forward pass costs $\sim 1.5\times$ the FLOPs of fixed-loop training ($\sim 1.3\times$ wall-clock on 4×H100).

**Tasks and scale.** Trained on a 25B-token deduplicated subset of The Pile (Chinchilla-optimal regime). Evaluated on perplexity (Pile, FineWeb-Edu, OpenWebText) and zero-shot reasoning on 10 benchmarks (COPA, HellaSwag, LAMBADA, OpenBookQA, PIQA, RACE, SciQ, ARC, SocialIQA, WinoGrande). Primary configuration: $(3 \otimes 8)$, $\sim 1$B parameters, compared against iso-FLOP non-looped $(24 \otimes 1)$ base.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (block isolation / swappability) | Low-moderate | Step conditioning is a training mechanism on a single shared block, not a technique for isolating or swapping heterogeneous blocks. Indirectly relevant: it demonstrates that a shared block can be made to produce varied, non-degenerate representations across iterations — a prerequisite for any block-pool design where the same block would be reused. The zero-init AdaLN modulator is a transferable pattern for injecting loop-step identity into a frozen block. |
| **G2** (dynamic per-block parameter budget) | Low | Budget is global (sequence-level $M \leq L$) not per-token or per-block. The elastic-depth framing is architecturally related but does not allocate parameters or FLOPs at block granularity. |
| **G3** (token-conditional routing) | Moderate | LoopFormer does not route per-token; all tokens run the same $M$ steps. However, the step-conditioning mechanism is directly applicable to a Huginn-based router: inject $(t, \Delta t)$ into Huginn's existing loop to make $h^{(k)}$ step-discriminative, enabling a halt head to read off loop progress. This is the mechanism that resolves Technical Challenge 2 in [[experiments/exp1-router-replication]]. |

## Credibility

| Dimension | Assessment |
|-----------|------------|
| Venue / year | arXiv preprint, Feb 2026 (submitted 11 Feb 2026); not yet peer-reviewed at time of capture |
| Authors / affiliation | U Toronto, Vector Institute, University Health Network; acknowledged by Prof. Colin Raffel |
| Code | Project page: `loopformer.github.io` — code availability not confirmed from captured sources |
| Ablation of step conditioning | Present. Table 1 compares LoopFormer vs. TMLT-EE (loop-index conditioning only, no $\Delta t$) vs. Base-Loop-EE-Cons (consistency loss only, no conditioning) at matched FLOPs. TMLT-EE uses $t$ alone; LoopFormer adds $\Delta t$ and multi-trajectory training. Figures 4 and 5 directly measure stagnation metrics; LoopFormer is the only model with non-flat trajectories. No standalone ablation of $\Delta t$ vs. $t$-only on the full model is reported in the main paper — this is a gap. |

## Empirical claims

**Perplexity (Pile, full $24\times$ budget, $3 \otimes 8$):**
- LoopFormer: 10.28 vs. TMLT: 10.38 vs. Base-Loop: 10.91 vs. Naive-EE: 11.6.
- Non-looped $(24 \otimes 1)$ base: 9.49 — gap persists but narrows to ~0.8 PPL.

**Zero-shot reasoning (avg over 10 tasks, $24\times$ budget):**
- LoopFormer: 44.81 vs. TMLT: 44.69 vs. Base-Loop: 42.88 vs. non-looped base: 45.27.
- LoopFormer is the best looped model at full budget, within 0.5 points of the non-looped base.

**Budget degradation (elastic depth, $3 \otimes 8$):**
- At $12\times$ budget: LoopFormer 11.12 PPL (Pile) vs. non-looped $(12 \otimes 1)$ base 9.98 — gap widens but reasoning accuracy 43.73 vs. base 44.93.
- TMLT-EE at $12\times$: 12.18 PPL (vs. LoopFormer 11.12 — 1.06 PPL improvement); Naive-EE collapses (11.66 PPL but reasoning drops).
- At $6\times$ budget: LoopFormer 14.3 vs. TMLT-EE 15.79 — LoopFormer degrades more gracefully.

**Representation metrics (Figure 4/5):** LoopFormer is the only depth-elastic model with non-flat curvature, anisotropy, entropy, and CKA trajectories across loop steps. All EE baselines show flat/high-CKA patterns consistent with stagnation.

**Trajectory schedule (Figure 6):** At fixed budget $M=4$ with $(3 \otimes 8)$, enumeration of all valid step schedules shows $\sim 1.4$ PPL spread and $\sim 1.3$ accuracy-point spread — trajectory choice is not a minor hyperparameter. Best schedules allocate coarser steps early, finer steps late.

## Open questions / failure modes

- **No per-token budget.** Budgeting is sequence-global; easy tokens run the same $M$ steps as hard tokens. Token-level halting (e.g., [[pondernet]]) would require composing step conditioning with a per-token halt decision — the interaction is unstudied.
- **Missing $\Delta t$-only ablation.** The paper does not ablate $\Delta t$ in isolation from multi-trajectory training; it is unclear how much gain comes from the $\Delta t$ signal vs. the shortcut consistency training regime.
- **Off-distribution schedules at inference.** Training uses uniform step draws over $[0,1]$; the best inference schedules (coarser-early/finer-late) are not seen during training at that exact form, which raises a distribution shift question. The paper does not address this explicitly.
- **Pretraining only.** All experiments train from scratch on The Pile. Applicability to a pretrained model like Huginn (where step conditioning would need to be retrofitted, not jointly trained) is an open question — AdaLN zero-init may ease fine-tuning, but residual stream norm dynamics at 3.5B scale are untested.
- **Causal vs. causal + stagnation interaction.** In a causal decoder, KV caches across loop iterations can be synchronized (Option A in Exp 1) or step-indexed (Option B). LoopFormer uses standard GPT-style causal attention; it does not address multi-step KV cache semantics (Technical Challenge 6 in [[experiments/exp1-router-replication]]).
- **Representation analysis is correlational.** The paper acknowledges CKA/curvature/entropy diagnostics are not causal — they show LoopFormer avoids stagnation, not that stagnation was the performance bottleneck.

## Source

- `raw/research/loop-challenges/03-loopformer-abs.md`
- `raw/research/loop-challenges/11-loopformer-pdf.md`

## Related

- [[mechanistic-looped-lms]]
- [[huginn]]
- [[universal-transformers]]
- [[experiments/exp1-router-replication]]
- [[pondernet]] — alternative halting mechanism; no step-conditioning; stagnation problem applies
- [[research/shortgpt]] — uses input/output cosine similarity as a block-importance proxy; LoopFormer's stagnation is the same phenomenon in a looped setting
- [[concepts/token-conditional-routing]]
