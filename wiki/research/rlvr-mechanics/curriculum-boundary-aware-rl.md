# Curriculum Boundary-Aware RL: Expanding Reasoning Beyond the Base Model

Boundary-aware Curriculum RL diagnoses why vanilla RLVR stalls at the base-model's reasoning ceiling and escapes it via three stages: pass@256 boundary mapping to classify problem difficulty, teacher-guided trace injection for frontier and unsolvable examples, and GRPO consolidation over a curriculum-selected training pool. Across five 7–8B models on AIME 2024/2025 and MATH500, the method improves pass@256 by +9.8 pp over base models and +10.3 pp over vanilla RLVR; 42% of base-model-unsolvable problems (226 of 538) become solvable after training. The paper accepts the zero-advantage collapse diagnosis that motivates the Invisible Leash critique, but argues the leash is a training-set composition artifact rather than an intrinsic ceiling on RL fine-tuning.

**Paper:** arXiv:2606.22317 — "Curriculum Reinforcement Learning Can Incentivize Reasoning Capacity in LLMs Beyond the Base Model"

## Core Mechanism: Zero-Advantage Collapse

Standard GRPO computes group-normalized advantages over $G$ rollouts per prompt. For binary rewards $r_i \in \{0,1\}$:

$$\hat{A}_i = \frac{r_i - \bar{r}}{\sigma_r + \varepsilon}$$

**Proposition 1 (Zero-advantage collapse):** If all rollouts in a group receive the same reward, $\hat{A}_i = 0$ for every rollout and the policy gradient $g_x(\theta) = 0$. Problems the base model never solves (all-fail groups) produce zero learning signal — they are invisible to vanilla RLVR.

**Proposition 2 (Mixed-reward contrast):** If $0 < m < G$ rollouts succeed, successful and failed rollouts receive advantage weights with opposite signs:
- Successful: $\hat{A}^+ = \frac{1 - m/G}{\sqrt{m(G-m)/G + \varepsilon}} > 0$
- Failed: $\hat{A}^- = \frac{-m/G}{\sqrt{m(G-m)/G + \varepsilon}} < 0$

**Proposition 3 (Reachability probability):** Under i.i.d. rollouts with per-rollout success probability $p_\theta$, the probability of a mixed-reward (reward-reachable) group is:

$$q_G(p_\theta) = 1 - (1-p_\theta)^G - p_\theta^G$$

This is zero only at $p_\theta = 0$ or $p_\theta = 1$, and is maximized at $p_\theta = 0.5$. Problems near the base model's boundary (rare successes) sit where reward contrast is highest; problems where the base model always fails sit in the zero-signal regime.

## Three-Stage Method

### Stage I — Reasoning Capacity Boundary Exploration

Run pass@256 sampling (256 decoding attempts, 3 seeds: {2027, 2028, 2029}) and classify each problem by first-success index $k^*$ (smallest $k$ for which pass@k = 1):

| Difficulty Tier | Criterion |
|-----------------|-----------|
| Easy | $k^* = 1$ |
| Medium | $2 \leq k^* \leq 8$ |
| Hard | $8 < k^* \leq 32$ |
| Frontier | $32 < k^* \leq 256$ |
| Beyond | $k^* > 256$ (never solved in budget) |

### Stage II — Targeted Teacher Guidance

Select 10 Frontier and 10 Beyond examples nearest to their respective boundary cutoffs. A teacher model (stronger LLM) generates solution traces with logical backbones, explicit self-reflection, multi-path exploration, and coherence checks. This small guided corpus (~20–40 traces per round) injects structural reasoning patterns for beyond-boundary examples, raising their effective $p_\theta$ above zero and making them reward-reachable for Stage III.

### Stage III — Curriculum Selection and GRPO Consolidation

Five curriculum ranges tested (e.g., Easy-to-Beyond, Medium-to-Beyond, Hard-to-Beyond, Frontier-to-Beyond, Beyond-only). Standard GRPO consolidates newly introduced patterns; teacher-guided traces replace vanilla rollouts for the Beyond tier. The method iterates: after one round, a new pass@256 sweep re-classifies problems for the next round (3 curriculum rounds per model in experiments).

## Experimental Results

Evaluated on Qwen2.5-7B, Qwen2.5-7B-Instruct, Qwen3-8B, DeepSeek-R1-0528-Qwen3-8B, Llama-3.1-8B-Instruct:

| Method | Average pass@256 vs. base model |
|--------|----------------------------------|
| Base Model | 0 pp (reference) |
| Vanilla RLVR | −0.5 pp |
| Boundary-aware Curriculum RL | +9.8 pp |

Curriculum RL beats vanilla RLVR by **+10.3 pp** on pass@256 on average.

**Problem-level boundary migration (538 base-model-unsolvable problems):**
- 226 problems (42%) became solvable after Curriculum RL
- Qwen2.5-7B-Instruct: 53 of 86 base-unsolved problems solved
- Llama-3.1-8B-Instruct: 90 of 170 base-unsolved problems solved

**Notable per-benchmark gains (Curriculum RL vs. vanilla RLVR):**

| Model | Benchmark | Gain |
|-------|-----------|------|
| Qwen2.5-7B | AIME 2024 | +25.6 pp |
| Qwen2.5-7B | AIME 2025 | +18.9 pp |
| Llama-3.1-8B-Instruct | MATH500 | +32.6 pp |

**Curriculum dynamics (Qwen2.5-7B-Instruct, 3 rounds):** Beyond examples migrate 113 → 45 (−68); reward-reachable examples 1835 → 1903 (+68). Direct one-for-one migration confirms the boundary is being pushed, not reshuffled.

## Relation to the Invisible Leash / Vanilla RLVR Limits

The paper explicitly engages with Yue et al. (2025) — the empirical foundation of the [[../../../conflicts/invisible-leash-vs-spiral-transfer|Invisible Leash vs. SPIRAL conflict]]. It **accepts** the diagnostic: vanilla RLVR sharpens the distribution over existing capabilities, reflected in degraded or flat pass@k for large $k$. The argument is that this sharpening is a **structural property of training set composition** (zero-advantage collapse excludes hard problems from receiving any gradient signal), not an intrinsic ceiling on RL fine-tuning.

The intervention — boundary estimation + teacher seeding of beyond-boundary examples — bypasses zero-advantage collapse without full-scale distillation. This is best read as evidence that the leash can be loosened by hybrid curriculum + teacher-seeding, not that the leash is wrong in its original vanilla-RLVR context.

Concurrent approaches to the same problem: He et al. (2025) "Rewarding the unlikely: lifting GRPO beyond distribution sharpening" and Liu et al. (2025) "ProRL: prolonged reinforcement learning expands reasoning boundaries in large language models."

## Limitations

- pass@256 is an empirical proxy for the capacity boundary; the true boundary is computationally inaccessible.
- Optimal curriculum selection strategy is unexplored — five fixed ranges tested, no systematic search.
- Teacher guidance requires a stronger model with automatic correctness verification; non-verifiable reward domains require adaptation.
- Evaluated on math reasoning only (AIME 2024/2025, MATH500); generalization unverified.
- The 256-rollout boundary-estimation sweep is computationally expensive for large training sets.
- If the teacher also fails at beyond-boundary problems, Stage II produces no useful signal.
- Catastrophic forgetting on easy/medium problems is a risk when curriculum shifts toward harder tiers.
- Iterative multi-round design compounds boundary miscalibration errors across rounds.

## Source

- arXiv:2606.22317 — "Curriculum Reinforcement Learning Can Incentivize Reasoning Capacity in LLMs Beyond the Base Model"
- Summary: `raw/research/weekly-2026-07-03/.ingest/02-curriculum-beyond-base-model.summary.md`

## Related

- [[_overview]] — rlvr-mechanics theme synthesis
- [[../../../conflicts/invisible-leash-vs-spiral-transfer]] — core conflict this paper bears on (counter-evidence to Position A's scope)
- [[rethinking-rl-sparse-selection]] — token-level evidence for vanilla RLVR's distribution-sharpening behavior
- [[binary-rewards-rl-challenges]] — formal account of why vanilla RLVR collapses toward near-Dirac policies
- [[rlvr-pattern-selection-theory]] — pattern-level theoretical account of Position A; base model quality gates RLVR convergence
- [[../../self-play/two-stage-dynamic]] — Stage-2 dynamics framing; boundary-aware curriculum is a mechanism for reaching Stage 2
- [[../../self-play/yue-rlvr-boundary]] — Yue et al. (2025), the primary paper this work responds to
- [[../../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — concurrent counter-evidence to the pure-reweighting reading
- [[../../teacher-student-rl/_overview]] — Stage II teacher trace injection is a teacher-student hybrid
- [[../../weekly-briefs/2026-07-03]] — brought in by the 2026-07-03 weekly sweep
