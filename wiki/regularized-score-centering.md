# Regularized Score Centering (RSC)

Off-policy/async RL stabilizer (Bai, Ye, Zhang, Kumar, Zhang; UIUC/CMU) that adds a per-token reverse-KL penalty to score centering (SC), with or without truncated IS. Claims convergence guarantees; best or tied-best on six agentic benchmarks, and survives higher learning rates in fully async SWE training. arXiv 2611.21791.

## Method
- Problem: async RL and training/inference numerical mismatch (TIM) make data off-policy. Full IS gives extreme gradients; token-level TIS caps weights at a clipping-bias cost. SC (Marek and Ryabinin, 2026) subtracts the behavior-policy mean of the (TIS-weighted) score per history.
- Diagnosis: SC leaves the behavior-policy advantage A^mu rather than learner advantage A^pi, so it can fail when the learner drifts from mu; worst in agentic tasks (actions change later states) and with long sampler-refresh intervals.
- RSC = SC + beta*KL(pi_theta || mu) (+TIS). Per-history KL over next-token distributions, estimated from behavior samples (E_mu[rho log rho]); mu fixed, so refreshing the sampler refreshes the KL reference. No extra environment interaction. Variants: RSC (w/o IS), RSC (TIS, cap 2).
- Replaces SC's top-128 + modeled-tail center with unbiased Monte Carlo draws from mu (128 samples controlled, 32 SWE).
- Theory: regularized surrogate converges; final policy approaches best-of-N from the initial policy; token log-ratio radius does not shrink with horizon (App. C).
- Settings: beta=0.01 (controlled), 0.001 (SWE uncapped); 8 responses/prompt; no entropy bonus; no KL to a fixed reference; hyperparameters not tuned for benchmark scores.

## Results
- Table 1 (3 seeds, mean+-std): RSC(TIS) best or tied-best on all six. WebShop 74.80 (IS-PPOClip 74.81, SC+TIS 52.21); TextWorld Cooking 99.95; AppWorld 14.04 (SC 12.28); BabyAI 18.06 vs IS-PPOClip 1.83 (~9.9x); Crafter 14.21 vs 9.34 (+52%); Craftax 4.71 vs 4.04 (+16%). Plain TIS scores 0 on WebShop and AppWorld. Several baselines have very high variance (WebShop IS +-36).
- Fig 7: higher training reward at equal sampled responses on Crafter and Craftax.
- Fig 6 (staleness): at the longest Countdown refresh interval RSC(TIS) beats SC by ~65% absolute heldout reward, even with Monte Carlo centering. MoE math: SC falls behind SC+TIS and RSC at the longest interval. Dense math: KL changes accuracy <1%.
- Fig 4: Monte Carlo centering beats Top-128 on every tested variant (math is one seed per method).
- Table 2, fully async SWE (Qwen3.5-35B-A3B-Base, SWE-Gym, SWE-bench Verified Avg@8, one seed):
| LR | RSC(w/o IS) | RSC(TIS) | SC+TIS | SC | IS | TIS |
|---|---|---|---|---|---|---|
| 1e-6 | 61.14 | 54.77 | 59.06 | 58.48 | - | - |
| 2e-6 | 47.89 | 54.47 | 36.04 | 21.13 | 0.40 | 51.51 |
  RSC gains are mostly about surviving the higher LR; the paper calls this observational. RSC(TIS) trails SC+TIS at LR 1e-6.

## Applicability
Async/off-policy LLM RL: agentic RL, long-horizon tool use, SWE agents, MoE RL (worse TIM), long sampler-refresh intervals, high learning rates. Needs behavior-policy token logprobs and a few auxiliary samples per history; no extra rollouts. Drop-in loss change for GRPO-style trainers already using TIS.

## Caveats / Reproducibility
- SWE results are single-seed and expensive; RSC(TIS) underperforms at low LR there. No benefit on dense-model math.
- Project page biechi.github.io/blog/rsc/. No code or weights link in the extracted text. Hyperparameters, datasets, configs in App. A; benchmarks public.
- Novelty is refinement: builds on SC and TIS (Ionides 2008; MiniMax 2025); relates to IMPALA, GSPO, Sequence MIS, PPO clipping. New: reverse-KL to behavior policy as SC stabilizer, unbiased MC center, A^mu vs A^pi diagnosis, convergence theory.
- Numbers are from the ingest summary of the paper; not re-verified against the raw text.

## Source
- raw/research/weekly-2026-11-21/05-regularized-score-centering.md
- https://arxiv.org/abs/2611.21791

## Related
- [[token-gradient-cancellation]] - per-token gradient-cancellation view; SC is the same family of argument.
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] - SC as another gradient-cancellation argument.
- [[delta-token-credit]] - token-level gradient analysis in GRPO/DAPO.
- [[llamarl]] - async off-policy RL framework; RSC addresses the instability it tolerates.
- [[polar-rl-harness]] - async agentic rollout, same staleness setting.
- [[magistral]] - async GRPO with no-KL and Clip-Higher; contrasts with adding KL to the behavior policy.
- [[kimi-k3]] - agentic MoE RL at scale; TIM/staleness relevant.
- [[memagent]] - DAPO-based agentic RL that could benefit.
- [[scalelogic]] - RL algorithm comparison benchmark (DAPO/GRPO/GSPO); GSPO is a baseline family here.
