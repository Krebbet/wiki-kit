# Rethinking Critic Learning in PPO: Value Flattening & SP³O

Diagnoses **Value Flattening** — PPO critics in LLM RLVR fail to track sharp within-response Monte Carlo state-value changes, staying comparatively flat — and traces it to an implicit variance penalty plus redundant gradient updates from temporally correlated states. Fixes it with **SP³O** (Sparse PPO), which applies the critic loss to only ~3 well-separated states per response instead of every token, and beats both PPO and GRPO in controlled comparisons. This is the theme's **first critic/value-function-side entry** — every existing rlvr-mechanics page targets the policy-side objective or token distribution.

## Diagnosis

Standard PPO/GAE setup, terminal-only binary reward, $\gamma=\lambda=1$ — so the critic regression target $\tilde G_t = R(\tau)$ is *identical at every token position* in a response. To measure critic fidelity, the paper independently samples K∈{128,192,256} continuations per intermediate state (Wilson-CI-gated) to get a low-variance policy-conditioned MC value estimate $\hat V^\pi_\text{MC}(s_t)$, compared against the critic's own prediction: MC values swing sharply within a response; the critic stays flat, sometimes moving in the *opposite* direction.

**Mechanistic account** (Eq. 5): $\frac{1}{T}\sum(v_t-R)^2 = (\bar v - R)^2 + \frac{1}{T}\sum(v_t-\bar v)^2$ — the critic's loss decomposes into a mean-fit term plus a term that is *minimized by flat predictions* regardless of the true within-response value trajectory (an implicit variance penalty). Compounded by redundant gradient updates from temporally correlated adjacent states — gradient cosine similarity decays with token-position distance, evidence the critic is effectively re-fit to near-duplicate targets at every step.

## Method — SP³O

Keep the actor objective, rollout procedure, and return targets unchanged. Apply the value-loss MSE only at a **sparse anchor set** $I(\tau)$ per response (Eq. 6), instead of every token. Default anchors: response-relative positions 0.3 / 0.6 / 0.9, plus a 0.95 "tail" anchor for responses ≥6144 tokens.

- **Anchor count**: K=3 is optimal; K=16/64 degrades back toward the dense-PPO baseline.
- **Anchor placement** matters more than count — spaced, late-tail-inclusive placement beats a naive count-matched random placement, which is worst.
- Tail anchor specifically: +1.47pp accuracy, cuts repetition from 18.33% → 1.12%.

## Claims

| Model | Metric | PPO | GRPO | **SP³O** |
|---|---|---|---|---|
| Qwen3-4B-Base | Math avg@32 | 37.60 | 39.26 | **45.57** |
| Qwen3-4B-Base | OOD avg@4 | 51.95 | 56.44 | **59.28** |
| Qwen3-8B-Base | Math avg@32 | 48.50 | 47.91 | **50.51** |
| Qwen3-8B-Base | OOD avg@4 | 64.38 | 64.91 | **66.37** |

- Math benchmarks: AIME24/25/26, AMC23, MATH500, Minerva, OlympiadBench. OOD: ARC-C, MMLU-Pro, GPQA, AGIEval, BBH, ZebraLogic.
- Profile MSE vs. MC values reduced 36% / 11% / 21% at 30% / 60% / 90% response progress. Critic representation effective rank rises (median 4.33 → 5.63).
- SP³O produces smaller, more stable within-iteration actor updates, higher validation accuracy/reward, and longer responses (online-dynamics analysis).

## A repaired critic beating GRPO — a tension worth flagging

**SP³O (a critic-*based* PPO variant) beats GRPO by +6.31pp (4B math avg) and +2.84pp (4B OOD avg), with the gap holding at 8B.** This sits in direct tension with [[../rl-optimizers/_overview]]'s framing of the RL-for-LLM optimiser lineage as a "critic-free trend" (PPO → InstructGPT → DPO → GRPO → post-GRPO — see that page's "The critic is optional" section) and with [[deepseekmath-grpo]]'s framing of GRPO's critic removal as motivated by cost/instability, which implicitly treats critic-free GRPO-family methods as the superior successor line to PPO. This paper doesn't claim to refute critic-free RL in general — its argument is narrower ("PPO's critic was badly *trained*, not badly *motivated*") — but its own controlled numbers show a repaired critic-based method beating GRPO. Genuine open tension, not yet ruled on.

## Limitations (authors' own)

- Findings specific to the terminal-only-reward setting with $\gamma=\lambda=1$, where all within-response MC targets are literally identical — unclear how the implicit-variance-penalty argument transfers to dense/shaped rewards.
- Sparse supervision requires manual anchor-position tuning; the K=3, 0.3/0.6/0.9+tail "sweet spot" is empirically found, not derived.
- FrozenLake (toy diagnostic) and Qwen3-Base only — no larger-model or non-math validation.
- Theoretical analysis (Appendix A.2) shows expected-policy-gradient invariance to baseline choice does **not** imply identical practical finite-batch/clipped-PPO updates — the theory only partially explains the empirical gains.
- No comparison to VinePPO (auxiliary-rollout critic fix) or other PPO-critic-repair baselines despite citing them as directly relevant prior work.

## Source

- `raw/research/weekly-2026-09-18/05-ppo-critic-value-flattening.md`
- arXiv:2609.18708

## Related

- [[../rl-optimizers/ppo]] — deep mechanistic dissection + repair of exactly the critic/GAE machinery that page documents as canonical
- [[_overview]] — first critic-side entry in the theme; every existing entry ([[rethinking-rl-sparse-selection]], [[binary-rewards-rl-challenges]], [[spurious-rewards-rlvr]], [[rlvr-pattern-selection-theory]], [[high-entropy-minority-tokens]], [[datpo-difficulty-adaptive-tree-rlvr]]) targets the policy-side objective or token distribution
- [[deepseekmath-grpo]] — GRPO's critic-free design was explicitly motivated by PPO critic cost/instability; this paper's result is a direct empirical counterpoint
- [[../rl-optimizers/_overview]] — flagged tension with the "critic-free trend" framing (see above)
- [[../../weekly-briefs/2026-09-18]] — brought in by the 2026-09-18 weekly sweep
