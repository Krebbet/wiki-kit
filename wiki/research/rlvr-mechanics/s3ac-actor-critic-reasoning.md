# S3AC: Stabilized, Selective, Scalable Actor-Critic for LLM Reasoning (Shanghai AI Lab)

A practical critic-training recipe (coverage pretraining of the value model, small value-head init, relaxed critic grad clip) makes PPO-style actor-critic beat a modern GRPO variant (GRPO-X) from 1.5B to 397B, sustains single-rollout ($K=1$) RLVR at 35B where critic-free baselines decay, and adds critic-reusing Difficulty-Aware Prompt Sampling (DAPS). Second critic-side data point beside [[research/rlvr-mechanics/ppo-critic-value-flattening]]. arXiv:2610.35518; no code.

Note: read from an ingest summary; appendices were not read directly.

## Method

- Token-level MDP, $R\in\{-1,+1\}$ on the last token; CISPO actor with GAE advantages, IcePoP token masks and MIS-style sequence masks. Clipped squared-error critic loss.
- **Coverage-oriented value pretraining** on trajectories pooled from policies of different strengths (35B: 327,680 trajectories / 7.08B tokens vs 65,536 / 0.74B for the on-policy critic); attention and router frozen.
- **Value-head init** std $1/(H+1)$ and critic grad-clip 1 -> 10: the head is under 0.01% of parameters but over 99% of squared gradient norm early, so global clipping starves the backbone (clipped steps 99.7% -> 12.5%).
- **Two-timescale online updates:** critic LR 5x actor, 2 critic epochs vs 1 actor, decoupled GAE ($\lambda_{critic}=1$, $\lambda_{actor}=1-1/(1.5T)$).
- **DAPS:** critic prior $p_c=\mathrm{clip}((V(s_0)+1)/2)$ blended with observed counts; accept prompt with prob. $a_{min}+(1-a_{min})\,4\hat p(1-\hat p)$. A Goldilocks acceptance, selects prompts before generation, no offline difficulty rollouts.

## Results

| Setting | GRPO-X / baseline -> S3AC |
|---|---|
| 35B group rollout | 76.4 -> 80.5 (all 7 benchmarks) |
| 397B group rollout | 85.1 -> 87.3 (all 5) |
| Qwen2.5-Math-1.5B | 42.7 -> 43.3 |
| R1-Distill-1.5B | 29.5 -> 31.4 |
| 35B single rollout | S3AC 80.9 vs REINFORCE++ 70.4, FlashREINFORCE 67.4 (baselines peak early then decline; S3AC holds through 1,600 steps) |
| DAPS vs uniform (35B group / single) | 79.04 -> 80.49 / 74.40 -> 76.94 |
| Coverage critic ablation (35B) | 80.78 vs 79.86 (confounded with data amount) |

Costs 27-40% more wall time per step; critic pretraining needs 0.3-1.9M trajectories. REINFORCE++ entropy collapses/blows up in single-rollout; S3AC stays stable. Prompt-level $V(s_0)$ tracks held-out MC return, acting as a learned difficulty predictor.

## Limitations

- Math/science/multimodal verifiable reasoning only; no multi-seed variance; R1D differences within eval noise; R1D S3AC truncates far more (26-29% vs 7%), which may inflate scores.
- Coverage pretraining needs trajectories from earlier-stage policies; DAPS off at 397B; in-house data at 35B/397B; single-rollout comparators are weak or published-config baselines; GRPO-X recipe partly mismatched.

## Thesis relevance

- "Single rollout" here means $K=1$ response per prompt with thousands of prompts per batch, not $N=1$ training example; do not conflate with [[research/single-sample-rl-finetuning/1-shot-rlvr]].
- Second independent critic-beats-critic-free data point for [[conflicts/sp3o-critic-repair-vs-critic-free-trend]], at far larger scale than SP3O. Soft tension (not contradiction) with [[research/rlvr-mechanics/grpo-secretly-prm]], which argues GRPO already does implicit MC-PRM credit assignment.
- DAPS is a critic-reuse Goldilocks curriculum, the same $p\approx0.5$ shape as self-play proposer rewards ([[research/self-play/sqlm]]).

## Source

- `raw/research/weekly-2026-10-30/05-s3ac-actor-critic-reasoning.md` (arXiv:2610.35518, https://arxiv.org/abs/2610.35518)

## Related

- [[research/rlvr-mechanics/ppo-critic-value-flattening]] — the other critic-side repair
- [[research/rlvr-mechanics/deepseekmath-grpo]] — GRPO baseline and original critic-removal motivation
- [[research/rlvr-mechanics/grpo-secretly-prm]]
- [[research/rlvr-mechanics/datpo-difficulty-adaptive-tree-rlvr]] — rollout-allocation analogue of DAPS
- [[research/rlvr-mechanics/high-entropy-minority-tokens]]
- [[research/rlvr-mechanics/rlvr-ood-gain-answer-format]] — truncation/length caution for benchmark gains
- [[research/rl-optimizers/_overview]]
- [[research/rl-optimizers/ppo]]
- [[research/rl-optimizers/dapo]]
- [[research/rl-optimizers/gspo]]
- [[research/process-reward-models/_overview]]
- [[research/curriculum-and-decomposition/_overview]]
- [[research/curriculum-and-decomposition/metis-curriculum-judgment]]
- [[research/curriculum-and-decomposition/pac-progress-augmented-curriculum]]
- [[research/single-sample-rl-finetuning/data-efficiency-rft]]
- [[research/single-sample-rl-finetuning/1-shot-rlvr]]
- [[research/self-play/sqlm]]
- [[research/rlvr-mechanics/_overview]]
- [[conflicts/sp3o-critic-repair-vs-critic-free-trend]]
- [[../weekly-briefs/2026-10-30]] — brought in by the 2026-10-30 weekly sweep
