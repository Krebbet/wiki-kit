# AdaBack: Adaptive Backtracking via Rationale Prefix Curriculum

AdaBack (Amani, Lotfi, Baldwin, Bengio, Farajtabar, Abbe, West; 2025/2026, arXiv:2506.18110) introduces a per-sample curriculum RL algorithm that reveals a prefix of the correct output (rationale prefix) as a training hint, adaptively scaling the hint length up or down per sample based on its rolling reward history. The core claim is that this intermediate regime — between full supervised training (full solution shown) and pure RL (no hints) — unlocks a class of hard-exploration problems with long sequences of latent dependencies where both SFT and vanilla RL fail to generalise. On a synthetic parity task designed to stress-test sparse-reward RL, AdaBack is the only method that reliably succeeds; on mathematical reasoning benchmarks (DeepScaleR, MATH, GSM8K) it enables models to solve problems that RL alone cannot.

## Key claims

- **SFT and RL both fail on latent-dependency tasks.** For sequence generation problems with combinatorially large output spaces and long chains of latent constraints (e.g., parity), SFT scales poorly with sequence length and RL finds no reward signal to bootstrap from.
- **Partial supervision fills the gap.** Revealing a correct prefix of the solution conditions the model on a valid partial state, dramatically reducing the effective search space for the remaining sequence.
- **Per-sample adaptation is load-bearing.** The hint length is not a global schedule — it is adjusted independently per sample based on that sample's past reward. Samples the model already handles receive shorter hints (or none); samples where the model consistently fails receive longer hints.
- **Incremental chain completion.** By conditioning on progressively shorter prefixes as competence grows, the model learns to complete increasingly long reasoning chains, building up to full autonomous generation.
- **Gains on standard math benchmarks.** AdaBack solves problems on DeepScaleR, MATH, and GSM8K that GRPO-style RL alone cannot, demonstrating the mechanism transfers beyond the synthetic setting.

## Mechanism

**Setup.** For each training sample $x$, the ground-truth solution $y^* = (y^*_1, \ldots, y^*_L)$ exists (from a teacher/reference corpus). AdaBack maintains a per-sample hint length $h_i \in \{0, 1, \ldots, L_i\}$.

**Rollout with hint.** At training step $t$, sample $i$ is presented to the model as $(x_i, \text{prefix}(y^*_i, h_i))$, i.e., the question concatenated with the first $h_i$ tokens of the correct solution. The model must generate the remaining tokens. Reward $r_i^t$ is computed on the full output.

**Adaptive hint update.** After each rollout, $h_i$ is updated based on the reward signal:
- If $r_i^t$ is low (model still failing despite current hint), increase $h_i$ — reveal more of the solution.
- If $r_i^t$ is high (model succeeds), decrease $h_i$ — withdraw the hint, pushing the model toward autonomous generation.

This is the "backtracking" in AdaBack: when the model fails, it backtracks to a longer hint (more supervision), then advances again as it masters the partial problem. The per-sample independence means each sample rides its own curriculum trajectory rather than a global difficulty schedule.

**RL objective.** The RL loss is applied only over the generated (non-hinted) portion of the sequence. The prefix is treated as context, not as tokens to be predicted. The method is agnostic to the specific RL algorithm (GRPO or similar).

**Hard-explore regime.** On the synthetic parity task, the output sequence has cascading bit-level dependencies: getting any one bit wrong makes all subsequent reward zero. Pure RL never finds a positive reward signal; SFT memorises without generalising. AdaBack's partial prefix breaks the dependency chain at a controlled depth, giving RL a manageable sub-problem with nonzero reward.

## Comparison to related methods

| Method | Hint mechanism | Per-sample adaptive | Hard-explore coverage |
|---|---|---|---|
| AdaBack (this work) | Correct solution prefix (rationale) | Yes — per-sample based on reward history | Yes — designed for zero-reward failure mode |
| E2H Reasoner ([[e2h-curriculum-rl]]) | Dataset difficulty scheduling (task-level) | No — global schedule across difficulty buckets | Partial — helps sparse reward but not zero-reward |
| Vanilla RL (GRPO/PPO) | None | N/A | No — collapses on zero-reward tasks |
| SFT | Full solution (dense supervision) | No | Fails to generalise on latent-dependency tasks |
| Teacher-student distillation | Policy output as soft label / KL target | No (global) | Depends on teacher coverage |
| TTC-RL / VCRL (curriculum RL variants) | Task selection / value-guided curriculum | Task-level, not hint-level | Partial |

## Source

- `raw/research/weekly-2026-06-19/02-adaback-adaptive-rationale.md`
- arXiv:2506.18110v2 (last revised 2 Mar 2026)
- Amani, Lotfi, Baldwin, Bengio, Farajtabar, Abbe, West. 22 pages, 11 figures.

## Related

- [[_overview]] — curriculum and decomposition theme overview; AdaBack introduces a novel hint-level curriculum axis
- [[e2h-curriculum-rl]] — E2H: dataset-difficulty scheduling; orthogonal mechanism (task ordering vs. hint revealing); both address hard-explore failure but at different granularities
- [[../teacher-student-rl/_overview]] — AdaBack is a form of on-policy distillation where the teacher's solution is revealed as a prefix hint; differs from standard KL distillation by using prefix conditioning rather than output matching
- [[../weekly-briefs/2026-06-19]] — brought in by the 2026-06-19 weekly sweep
