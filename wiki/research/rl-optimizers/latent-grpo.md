# Latent-GRPO — GRPO for Latent Reasoning

(arXiv:2604.27998). First **stable** GRPO extension to **continuous (vocabulary-superposition) latent reasoning chains**. Identifies and fixes three coupled bottlenecks of prior Soft-GRPO: (1) **Invalid-Sample Advantage Masking** (excludes off-manifold trajectories from group statistics), (2) **One-sided Gumbel noise sampling** with conditional Straight-Through estimator (eliminates positive-advantage / downward-update gradient mismatch), (3) **Optimal Correct-Path First-Token Selection** (resolves harmful gradient averaging across multiple correct latent paths at $t=1$). On hard math benchmarks it surpasses explicit GRPO by **+4.27 Pass@1** on AIME / Math500 with **3.31×** shorter chains; pass@64 on AIME24 reaches 50.0 vs. GRPO's 23.3 under Gumbel sampling.

## Source
- [`raw/research/weekly-2026-05-03/05-latent-grpo.md`](../../../raw/research/weekly-2026-05-03/05-latent-grpo.md) — captured 2026-05-03 (arXiv:2604.27998)

## Latent token

A latent token is a top-$K$ vocabulary-superposition embedding (Eq. 1):
$$s_t = \sum_{i=1}^{K} p_{t,i}\, e_{t,i}.$$
Cf. Coconut (hidden-state latent) and Soft Thinking (vocabulary-superposition); Latent-GRPO inherits the latter.

## Three fixes over Soft-GRPO

### 1. Invalid-Sample Advantage Masking (Eq. 9–11)

Overlength / off-manifold trajectories are excluded from the group statistic when computing $\hat{A}_j = (R_j - \mu_R)/\sigma_R$. Soft-GRPO's failure is rooted in contaminated baselines from invalid samples; masking restores group-relative honesty.

### 2. One-sided Noise Sampling + STE (Eq. 12–17)

Standard two-sided Gumbel density causes gradient-direction mismatch — positive-advantage latent components can receive *downward* updates (Section 2 / Appendix A). The fix: clip+shift Gumbel noise to be strictly positive, with a conditional Straight-Through Estimator to maintain alignment through repeated PPO epochs.

### 3. Optimal Correct-Path First-Token Selection (Eq. 18–21)

**Latent Mixture Non-Closure** — a new failure mode this paper documents. Multiple correct latent trajectories diverge at $t=1$; naive group-relative averaging blends them, producing a destructive gradient. Fix: among multiple correct trajectories, choose the one with highest average surrogate log-prob (Eq. 18–19) and mask competing correct paths *only at $t=1$* (Eq. 20–21). Final objective (Eq. 22–23) is PPO-clipped + KL on a mixed latent / discrete trajectory.

## Empirical headline

| Suite | Backbone | Δ Pass@1 | Chain ratio |
|---|---|---|---|
| Low-difficulty (GSM8K-Aug, GSM-Hard, SVAMP, MultiArith) | LLaMA-3.2-1B-Instruct | **+7.86** vs. Latent-SFT | **4.44×** shorter than explicit GRPO |
| High-difficulty (Math500, AIME24/25, GPQA) | Qwen2.5-Math-7B | **+14.77** vs. Latent-SFT, **+4.27** vs. explicit GRPO | **3.31×** shorter than explicit GRPO |

Best Pass@1: Math500 80.40, AIME24 26.56, AIME25 23.23. Under Gumbel sampling, AIME24 pass@64 reaches **50.0** vs. GRPO's **23.3**.

## Where it sits in the wiki

- Cleanly extends the [[_overview]] family as **the first latent-space variant** of GRPO. Compare:
  - [[dr-grpo]] — removes length / std bias (discrete-token).
  - [[dapo]] — Clip-Higher / Dynamic Sampling (discrete-token).
  - [[gspo]] — sequence-level clip (MoE stability, discrete-token).
  - **Latent-GRPO** — invalid-sample masking + one-sided noise + first-token selection (continuous latent).
- The **Latent Mixture Non-Closure** failure mode is genuinely new for the wiki — current [[../rlvr-mechanics/_overview]] pages assume discrete tokens.
- Chain compression (3.31×) reduces cost-per-RL-step — directly relevant to single-sample / few-shot RL training budget; cross-link [[../single-sample-rl-finetuning/_overview]].
- Latent-token reasoning as continuous concept representation may bear on [[../in-context-learning-theory/icl-as-gradient-descent]] (linear-attention ↔ implicit GD parallel).

## Tension flagged

Wiki position via [[../self-play/invisible-leash]] / [[../self-play/yue-rlvr-boundary]] is that RLVR selects for latent reasoning already present in the base model. Latent-GRPO's +4.27 over explicit GRPO on AIME could suggest latent training unlocks capacity beyond base-model pass@k — but the paper does not test against base-model pass@k directly. **Open empirical question.** Would resolve cleanly if a base-model upper bound were reported.

## Limitations

1. Requires **Latent-SFT warm-start** — cold RL on an explicit model collapses.
2. No deterministic sampling mode (same prompt → different output) — pass@k only measurable via injected inference-time Gumbel noise.
3. Slight pass@1 drop under Gumbel sampling on hardest AIME problems (deterministic mode > noisy pass@1, but noisy mode wins pass@64).
4. Slightly below GRPO on SVAMP — attributed to mismatched SFT vs. Latent-SFT starting points.

## Related

- [[_overview]] — RL optimiser theme
- [[deepseekmath-grpo]] — GRPO baseline this extends
- [[dr-grpo]] / [[dapo]] / [[gspo]] — sibling fixes on discrete-token GRPO
- [[../rlvr-mechanics/_overview]] — discrete-token assumption now incomplete
- [[../single-sample-rl-finetuning/_overview]] — chain compression as single-sample budget multiplier
- [[../in-context-learning-theory/icl-as-gradient-descent]] — latent reasoning as continuous concept representation
- [[../self-play/invisible-leash]] / [[../self-play/yue-rlvr-boundary]] — open base-bound question
- [[../../weekly-briefs/2026-05-03]] — brought in by the 2026-05-03 weekly sweep
