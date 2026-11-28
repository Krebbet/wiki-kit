# RL Can Be Recovered From Its Own Rollouts (Sheng, Gu et al.)

Plain maximum-likelihood training on the *unfiltered* archived rollouts of an online RLVR run, from the same base model and in original order, tracks the online learning curve; a few late batches often recover final performance. Replaying the RL updates offline is unstable on the language models tested. Reading: most RL compute goes into discovering the sampling distribution, not learning it. arXiv:2611.33102.

Note: written from the structured summary; no seeds or error bars are reported in the paper text, and most figure values did not survive extraction.

## Method

- Archive batches $D_0,\dots,D_{T-1}$. Student starts at $\pi_0$, minimises token NLL on **all** responses (correct and incorrect, no rewards), one update per batch. Endpoint variant: cycle over the last $m$ batches. Population view: each step minimises $KL(\pi_t\|q)$, so the student lags $\pi_t$ by one step.
- Why offline RL replay drifts: at a fixed rollout policy the update ascends $w_t p_t[-KL(\pi_t^+\|\hat\pi_t)+KL(\pi_t\|\hat\pi_t)]$. The reward-baseline term has zero expectation on-policy; off-policy it pushes the replayed policy away from $\pi_t$ (population-level "can amplify" argument).

## Results

| Test (Qwen3-1.7B unless noted) | Result |
|---|---|
| Full replay, endpoint gap in points (base) | MATH-500 0.4 (7.9), AIME25 0.7 (4.2), GPQA 0.4 (5.9), K&K 0.3 (71.9) |
| Last batch only (4096 rollouts) | gap MATH 0.7, AIME25 0.8, K&K 0.9 |
| SmolLM2-360M / GSM8K, last 1 / 5 / 50 batches | gap 5.2 / 3.0 / 0.9 (base 22.6) |
| Maze, full / last / last 10 (online 0.252) | 0.238 / 0.157 / 0.247 |
| Order | chronological best, shuffled middle, reverse worst (can end farther from online than base) |
| Offline MaxRL replay | collapses by step 100; with clipped token IS lasts to ~600 then drops |

- GRPO and RLOO archives also recover at the final checkpoint.
- One student trained on the last batches of a math and a K&K specialist keeps most of both (70.8 / 68.3 vs 70.8 / 69.7); weight merges are worse on K&K (30.2-64.1).
- Cross-model: 0.6B trained on 1.7B rollouts roughly tracks final-checkpoint distillation (one pair, figure only).

## Scope limits

- A successful online run is still required. "Reward-free" replay data were already shaped by reward. Savings apply to reuse (retraining, merging, transfer); no compute figures.
- Collapse of offline RL replay is shown for MaxRL (and REINFORCE+IS) on LMs only; offline MaxRL works on ImageNet (within 0.006 of online).
- Last-batch sufficiency is task-dependent. Largest model 4B. "Last batch" is thousands of rollouts over many prompts, not single-sample learning.

## Bearing on the thesis

Evidence that the learnable content of an RLVR run is a data distribution that SFT can absorb *(synthesis)*: an acquired capability could be stored, ordered and composed as rollouts. Order dependence is an implicit-curriculum signal for [[../synthesis/concept-curriculum-method]]. No mechanism or compositionality test.

## Source

- raw/research/weekly-2026-11-27/01-rl-recovered-from-rollouts.md (arXiv:2611.33102)

## Related

- [[_overview]]
- [[deepseekmath-grpo]]
- [[rl-take-off-successful-groups]]
- [[../rl-optimizers/rloo]]
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]]
- [[../teacher-student-rl/mrpd-replay-consolidation]] — ordered replay of *expert* logs
- [[../teacher-student-rl/semi-opd-offline-student-rollouts]]
- [[../teacher-student-rl/opd-vs-offpolicy-kl-direction]]
- [[../self-improvement/star]] — contrast: STaR filters to correct samples
- [[../self-play/invisible-leash]]
- [[../../weekly-briefs/2026-11-27]] — brought in by the 2026-11-27 weekly sweep
