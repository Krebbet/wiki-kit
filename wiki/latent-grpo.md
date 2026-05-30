# Latent-GRPO: Group Relative Policy Optimization for Latent Reasoning

Tsinghua + Alibaba (arXiv:2604.27998, 2026-04-30). RL post-training framework that stabilizes GRPO on latent-reasoning models — where intermediate steps are vocabulary-superposition latent tokens rather than discrete words. Standard GRPO collapses on Latent-SFT initializations; Soft-GRPO (Zheng & Lee 2025) provided a Gumbel-density bridge but failed to outperform discrete RL. Latent-GRPO diagnoses three coupled failure modes (off-manifold exploration, optimization-direction mismatch under multi-epoch PPO, mode averaging across correct paths) and adds three targeted fixes. +14.77 pp Pass@1 over Latent-SFT on Qwen2.5-Math-7B with **3.31× fewer reasoning tokens** than explicit GRPO; +4.27 pp over explicit GRPO on the same hard-difficulty mix.

## Method

Builds on Soft-GRPO's Gumbel-reparameterized density estimation for mixed latent/discrete trajectories. The three additions:

1. **Invalid Sample Advantage Masking.** Non-terminating (over-length) trajectories are excluded from group normalization and assigned zero advantage, so off-manifold rollouts can't corrupt the per-group statistics that GRPO depends on.
2. **One-sided Noise Sampling.** Gumbel perturbations are clipped and shifted to be strictly positive; a conditional Straight-Through Estimator flips gradients when the rollout target is exceeded during multi-epoch PPO updates. This aligns the per-component update direction with the trajectory-level advantage sign — the "Latent Mixture Non-Closure" fix.
3. **Optimal Correct Path First Token Selection.** When multiple correct trajectories share a prefix, only the single highest-average-surrogate-log-prob correct path contributes to the **first** latent-token update (later-token updates from all correct paths remain active). Prevents barycentric averaging at the shared initial step.

Initialization requires a Latent-SFT warm-start — RL alone cannot induce the latent manifold from scratch.

## Results

**Low-difficulty (LLaMA-3.2-1B-Instruct, Table 1):**
- Latent-GRPO avg Pass@1: **58.32** vs Latent-SFT 50.46 (+7.86 pp), vs explicit GRPO 57.98 (+0.34 pp).
- Reasoning length: **21.20 tokens** vs explicit GRPO 94.20 — 4.44× compression.
- Soft-GRPO: 50.73 (+0.27 over SFT — essentially flat).

**High-difficulty (Qwen2.5-Math-7B, Table 2):**
- Latent-GRPO avg Pass@1: **41.72** vs Latent-SFT 26.95 (+14.77 pp), vs explicit GRPO 37.45 (+4.27 pp).
- Reasoning length: 1649 vs explicit GRPO 5466 — 3.31× compression.
- Math500 80.40 / AIME24 26.56 / AIME25 23.23.
- Soft-GRPO: 24.38 avg (−2.57 vs SFT — confirms the baseline instability the paper diagnoses).

**Pass@k under Gumbel sampling (Figure 4):**
- AIME24 pass@64: Latent-GRPO 50.0 vs explicit GRPO 23.3.
- AIME25 pass@64: 53.3 vs 30.0.
- Math500 pass@64: 87.8 vs 84.2.
- Trade-off: pass@1 drops under sampling vs deterministic mode (AIME24 26.7 → 20.0 at noise=0.5).

**Ablation (Figures 2-3):** One-sided Noise Sampling is the dominant factor — removing it causes collapse. First-Token Selection adds incremental gains, especially on hard tasks.

## Why this matters

Latent reasoning (Coconut, CODI, CoLaR, Latent-SFT) is an active subfield betting that continuous-token chains can compress reasoning. The bottleneck has been that standard discrete-token RL (GRPO) doesn't transfer cleanly: Soft-GRPO showed the Gumbel bridge worked but didn't move the empirical needle. Latent-GRPO is the first method to make GRPO-on-latent strictly dominate explicit GRPO at matched compute, and the gain compounds with the **3.3-4.4× token compression** the latent representation already provides. Pass@k under Gumbel sampling (50.0 vs 23.3 on AIME24) is the more striking result — the noise injection turns out to be a diversity engine, not just a stabilizer.

The diagnosis bridges to [[token-gradient-cancellation]]: both papers identify GRPO update-direction pathologies but in different geometries (gradient exchangeability for discrete tokens; manifold geometry for latent components). The fixes are different but the failure-mode framing is shared.

## Reproducibility

- Code, models, data: https://github.com/DJC-GO-SOLO/Latent-GRPO.
- Preprint only at capture date; no paperswithcode entry; no independent reproduction yet.

## Source

- `raw/research/weekly-2026-05-04/02-latent-grpo.md` — arXiv:2604.27998.

## Related

- [[token-gradient-cancellation]] — parallel diagnosis of GRPO update-direction pathologies; DFPO fixes gradient exchangeability for discrete tokens, Latent-GRPO fixes one-sided alignment for latent components.
- [[rlsd-self-distilled-rlvr]] — adjacent training-stabilization theme; RLSD via teacher/student weighting, Latent-GRPO via manifold-aware masking.
- [[gepa-reflective-prompt-evolution]] — opposite end of the "trainable vs training-free" axis on reasoning efficiency: GEPA evolves prompts, Latent-GRPO compresses traces.
- [[eggroll]] — touches the [[conflicts/grpo-vs-evolution-strategies]] thread (GRPO viable at 7B latent ≠ resolves EGGROLL's 14B+ Adam-state claim).
- [[watchlist]] — Latent-SFT, Soft-GRPO, Coconut, CODI, CoLaR are the latent-reasoning lineage referenced but not captured.
