# VIMPO: Value-Implicit Policy Optimization

VIMPO (Kang, Feng, Levine, Song, Zhao; arXiv:2606.20008) is a critic-free RL post-training method for LLMs that derives a token-level value function analytically from the KL-regularized RL optimality conditions, without training a separate critic network. The value is *implicit in the policy itself*: the value recurrence is expressed entirely in policy-reference log-ratios (log π/π_ref per token), anchored at end-of-sequence by the terminal condition that no future reward remains. This yields a value loss that incorporates outcome-level verifiable rewards and a decoupled actor advantage for a PPO-style update — all without any additional learned parameters. It occupies a third position between GRPO (trajectory-level advantage, no critic) and actor-critic methods (dense signal, learned value network), and outperforms GRPO on competition math benchmarks.

## Method

Starting from the optimality conditions of KL-regularized RL, VIMPO constructs a value recurrence for autoregressive generation. At each token position, the value can be written as a function of the cumulative log π/π_ref ratio over the suffix of the sequence. The terminal condition anchors this recurrence: at the final token, no future reward exists, so the value equals the outcome reward directly. Rolling backwards gives per-token value estimates expressed purely in terms of quantities already computed in a standard PPO-style update loop.

From this recurrence, VIMPO derives two training signals:

1. **Value loss** — incorporates the verifiable outcome reward into per-token value targets without a critic network.
2. **Critic-free actor advantage** — separates reward incorporation (via the value loss) from policy improvement (via the PPO-style surrogate). This decoupling is what GRPO cannot do at trajectory level.

No architecture changes are required. The only overhead beyond GRPO is computing the value recurrence from per-token log-ratios already present in the PPO setup — a drop-in substitution.

## Results

Evaluated on mathematical RLVR benchmarks, VIMPO improves over GRPO on all four:

- MATH-500
- AIME 2024
- AIME 2025
- OlympiadBench

Gains are described as "especially larger" on competition-style evaluations (AIME, OlympiadBench). Under noisy reward conditions, VIMPO retains a consistent advantage over GRPO — the per-token signal is more robust to reward noise than trajectory-level advantage, which degrades faster as reward signal is corrupted. Specific numeric deltas are not available from the abstract-only capture; full tables require the paper PDF.

## Novelty

The core contribution is the analytical derivation of a policy-implied value function from KL-regularized RL optimality conditions. This is not an approximation or heuristic — it follows directly from the theoretical framework. Prior work bifurcated into two positions:

- **GRPO/DAPO lineage**: trajectory-level group advantage, no critic. Simple, stable, but coarse: every token in a trajectory receives the same credit signal regardless of its contribution.
- **Actor-critic**: dense per-token signal from a learned value network. Finer credit assignment, but introduces a second optimization target and its associated instability.

VIMPO is a third position: **token-level credit without a learned critic**. The value is computable from quantities already present in the training loop. The key insight is that the KL-regularized optimality condition pins down what the value *must* be under the current policy — making a separate value network redundant in this setting.

## Comparison to Related Methods

| Method | Credit Granularity | Value Function | Stability |
|---|---|---|---|
| GRPO | Trajectory-level | None | High (no critic) |
| Actor-critic | Token-level | Learned (separate network) | Lower (critic training) |
| DFPO ([[token-gradient-cancellation]]) | Token-level (structural fix) | None | High; fixes gradient exchangeability pathology |
| DelTA ([[delta-token-credit]]) | Token-level | None (discriminator reweighting) | High; empirical, not theory-derived |
| VIMPO | Token-level | Analytically derived from policy | High; no critic training |

DFPO (Drift Fixing Policy Optimization) addresses the same trajectory-level-credit problem by ensuring gradient exchangeability — reward-irrelevant tokens cancel across trajectories. It is a structural fix to the gradient computation, not a value-function derivation. VIMPO's value recurrence and DFPO's stop-gradient transforms target the same failure mode via different mechanisms and are potentially composable.

DelTA provides per-token credit via discriminator-contrast over token-gradient centroids — an empirical/geometric approach derived from viewing the RLVR objective as a linear classifier. VIMPO's token-level weights emerge instead from the KL-regularized theory directly.

## Applicability

Drop-in replacement for GRPO in any RLVR training loop using PPO-style infrastructure (policy-reference log-ratios per token are already computed). No new architecture, no value head, no additional rollouts. Particularly effective on hard competition-style math tasks where trajectory-level advantage is a coarse signal. Robustness to reward noise suggests applicability in settings where verifiers are imperfect or reward hacking is a concern.

**Constraint:** the value recurrence is specific to KL-regularized RL objectives. May not transfer directly to reward-only (no KL) training setups.

## Reproducibility

- **arXiv:** 2606.20008
- **Code:** https://github.com/backprop07/VIMPO
- **Authors:** Zhewei Kang, Aosong Feng, Sergey Levine, Dawn Song, Xuandong Zhao
- **Venue:** preprint, June 2026

## Source

`raw/research/weekly-2026-06-27/04-vimpo.md` (arXiv:2606.20008)

## Related

- [[token-gradient-cancellation]] — DFPO fixes gradient non-cancellation in trajectory-level GRPO via stop-gradient transforms; VIMPO derives per-token value analytically from the same KL-regularized RL framework — different mechanisms for the same coarse-credit pathology, potentially composable.
- [[delta-token-credit]] — DelTA assigns per-token credit via discriminator-contrast over gradient centroids (empirical/geometric); VIMPO derives token-level value from KL-regularized RL theory; parallel critic-free solutions to the same credit-assignment bottleneck.
- [[latent-grpo]] — both extend KL-regularized RL theory to fix GRPO failure modes; Latent-GRPO targets manifold geometry of continuous latent tokens, VIMPO targets discrete-token credit assignment precision; shared theoretical lineage.
