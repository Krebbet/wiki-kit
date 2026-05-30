# ScaleLogic: RL Scaling Laws for Reasoning Depth and Expressiveness

ScaleLogic (arXiv:2605.06638) introduces a controlled synthetic benchmark for measuring how RL training compute scales with proof-tree depth and logical expressiveness, establishing a power-law T ∝ D^γ with R² > 0.99 fits across five logical complexity levels and three RL algorithms. The exponent γ rises monotonically from 1.04 (implication-only) to 2.60 (+quantification), meaning doubling reasoning depth multiplies training cost by ~2× to ~6× depending on expressiveness class. The headline downstream result: training on the most-expressive (+Quantification) curriculum transfers to +10.66 pp gain across 8 math/reasoning benchmarks vs base model (49.39% → 60.05%), while simpler curricula plateau around +2–3 pp regardless of compute. The central claim is "what you train on dominates how much" — task expressiveness governs downstream transfer more than raw training-compute volume.

## Method

- **ScaleLogic synthetic benchmark:** generates logical-reasoning multiple-choice problems with exact verifiability and unlimited data. Two independently controlled axes: proof-tree depth D (long-horizon reasoning) and logical expressiveness (5 levels: implication-only → +conjunction → +negation → +disjunction → +quantification).
- **Problem structure:** B candidate proof trees per instance (default B=4); exactly one has a provable conclusion; remaining B−1 are corrupted by removing or polarity-flipping one axiom. Distractors added to limit shortcut exploitation.
- **Compute metric:** T = RL training steps to reach 90% validation accuracy (Pass@1); power-law fit via OLS in log-log space; ΔAIC ≥ +7.1 vs exponential fit confirms polynomial (not exponential) growth.
- **Algorithms tested:** primary DAPO (GRPO extension with dynamic sampling + clip-higher); robustness checks with standard GRPO and GSPO. Training distribution variants: uniform depth sampling, curriculum (depth gradually increases), difficult-only (depth-D instances only).
- **Model scale:** Qwen3-34B (non-thinking) as primary; Qwen3-8B replication in appendix. Downstream evaluation: 8 benchmarks including AIME 2024/25, AMC 2023, MATH-500, Minerva, OlympiadBench, GPQA-Diamond, MMLU-Pro STEM.

## Results

- Power-law T ∝ D^γ holds with R² > 0.99 across all five expressiveness levels and all three RL algorithms.
- Scaling exponent γ by logical class (DAPO): implication-only 1.04 ± 0.03 → +conjunction 1.72 ± 0.08 → +negation 1.81 ± 0.05 → +disjunction 2.11 → +quantification 2.60 ± 0.06.
- Cross-algorithm γ in +Conjunction: DAPO 1.70, GRPO 2.05, GSPO 1.65 — all follow the same power-law shape, confirming algorithm-agnostic regularity.
- Downstream transfer: base model 49.39%; +Quantification 60.05% (+10.66 pp); simpler settings plateau ~52%; at fixed depth D=12 and fixed compute (~100 steps), expressiveness remains strictly monotone (+0.49 pp implication-only → +8.10/+6.33 pp quantification).
- Curriculum training reduces γ substantially: 1.33 (curriculum) vs 1.70 (uniform) vs 2.36 (difficult-only) in +Conjunction — same power-law shape, lower slope.
- OOD generalization: models trained on depth D_train extrapolate gracefully to unseen depths beyond the training boundary rather than collapsing.

## Why this matters

ScaleLogic provides the first calibrated empirical scaling law for RL reasoning compute as a function of *task structure*, not just model scale or data volume. Prior RL scaling law work (Khatri et al. 2025, Tan et al. 2025, cited in the paper) primarily varied data volume and model scale while holding task difficulty fixed. ScaleLogic's controlled experiments show that task expressiveness is a previously unmeasured axis that can swamp volume effects: implication-only saturates at ~+2.6 pp downstream regardless of training steps, while +quantification reaches +10.66 pp. The implication for practitioners: curriculum and dataset design decisions dominate marginal compute spend, especially at depth D > ~8 where γ differences compound.

The "expressiveness > compute" finding is structurally parallel to [[gepa-reflective-prompt-evolution]]'s core claim — that the *shape* of the search space (Pareto-illuminated prompt curriculum vs flat beam search) determines outcome quality more than rollout volume — but operates on the weight-update axis instead of the prompt-space axis. Both papers land on the same meta-principle from different mechanisms. [[agentflow]]'s Flow-GRPO multi-turn depth axis maps directly onto ScaleLogic's reasoning-depth D: as task horizon grows, RL training cost escalates super-linearly, which is exactly the instability AgentFlow's reward broadcast addresses at the multi-module level.

ScaleLogic's cross-algorithm validation (GRPO, DAPO, and GSPO all follow the same power-law with R² > 0.99) is relevant context for [[conflicts/grpo-vs-evolution-strategies]]: the scaling regularity holds across the RL algorithms tested, but ScaleLogic does not test evolution strategies (ES). The EGGROLL competitive claim — that ES outperforms GRPO — is therefore untouched by these findings, and the conflict remains open. What ScaleLogic does establish is that within the GRPO/DAPO/GSPO family, algorithm choice shifts the γ magnitude (GRPO γ=2.05 vs GSPO γ=1.65 in +Conjunction) but doesn't break the power-law structure.

## Reproducibility

The ScaleLogic benchmark generator is described in sufficient detail to reconstruct (proof-tree generation, corruption strategy, distractor construction). No explicit code release mentioned in the source. Empirical fits use Qwen3-34B as primary model; Qwen3-8B appendix replication is included. Downstream evaluation covers 8 standard math/reasoning benchmarks for broad transfer measurement.

## Source

- `raw/research/weekly-2026-05-11/03-scalelogic.md` — arXiv:2605.06638.

## Related

- [[gepa-reflective-prompt-evolution]] — parallel "expressiveness > volume" framing in prompt-space; both papers converge on curriculum/data design dominating raw compute.
- [[agentflow]] — Flow-GRPO multi-turn depth axis maps onto ScaleLogic's proof-tree depth D; AgentFlow's reward-broadcast fix addresses the super-linear cost ScaleLogic measures.
- [[latent-grpo]] — both study RL training efficiency on reasoning; "expressiveness > quantity" complements Latent-GRPO's token-compression angle on RL compute efficiency.
- [[token-gradient-cancellation]] — GRPO stability and scaling; ScaleLogic's cross-algorithm validation (GRPO/DAPO/GSPO all follow same power-law) provides context for why gradient pathologies don't invalidate the scaling regularity.
- [[tempo-test-time-rl]] — adjacent RL framing; TEMPO targets EM-step drift at inference, ScaleLogic targets training-time scaling structure.
- [[eggroll]] — ScaleLogic's power-law holds across GRPO/DAPO/GSPO but doesn't test ES; the EGGROLL competitive claim remains untouched.
- [[conflicts/grpo-vs-evolution-strategies]] — ScaleLogic measures γ differences across RL algorithms but leaves ES vs GRPO unresolved.
