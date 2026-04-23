---
name: cbrl
description: CBRL stochastically prepends few-shot demonstrations during RLVR training with a linearly annealed injection probability, bootstrapping early reward signal without inducing inference-time dependence on examples.
type: research
---

# Context Bootstrapped Reinforcement Learning

CBRL addresses the zero-gradient failure mode in GRPO/RLOO — when all rollouts in a group fail, advantage collapses and no policy update occurs. The fix is algorithm-agnostic: at each training step, $k=2$ solved examples are prepended to the prompt with probability $p_i$ drawn from a linearly decaying schedule, then annealed to zero by the end of training. Rewards are computed solely on the model's generated response, leaving the RL objective untouched. The net effect is a curriculum over scaffold reliance — early training runs guided, late training runs autonomous — and the resulting reasoning patterns persist parametrically after demonstrations are fully withdrawn.

## Method

**Injection schedule (Eq. 1):**

$$p_i = p_\text{start} + \frac{t-1}{T-1}(p_\text{end} - p_\text{start})$$

where $t$ is the current step, $T$ is total steps, $p_\text{start} = 0.5$ (default), $p_\text{end} = 0.0$. Ablations show $p_\text{start} = 0.5$ optimal; $p_\text{start} = 1.0$ over-scaffolds and suppresses independent exploration; $p_\text{start} = 0.0$ recovers standard GRPO.

**Demonstration bank:** A fixed bank of ~20–50 solved examples per task is constructed once from expert traces or stronger-model solutions (GPT-5.2 for Reasoning Gym; tag-filtered retrieval for the Q programming domain). No learned retrieval. At peak injection rate, only ~50% of prompts carry examples; no additional inference cost at test time.

**Curriculum shape:** Early training receives scaffolded prompts that generate enough successful rollouts for non-zero reward signal; injection probability decays linearly until the model operates fully unassisted. The input distribution is non-stationary and demonstration-conditioned during training — the paper frames this as "fully on-policy" because rewards are computed on the model's own output, though input-distribution shift means subtle off-policy nuances apply when comparing to methods like LUFFY.

## Claims

Evaluated on Reasoning Gym (Qwen2.5-3B, Llama-3.2-3B; 500 steps, batch 32) and Q programming (Qwen2.5-7B):

- **All 10 model–environment pairs** improve over GRPO-only baseline: +1.3% to +22.3%.
- Q programming (domain-specific language with minimal pretraining coverage): Pass@1 5.0% → 26.3%.
- Gains persist after $p_i \to 0$, confirming durable internalization rather than in-context dependence.
- Also works with RLOO; largest RLOO gains: Word Sorting 20% → 67%, Puzzle-24 23% → 66%.
- RLOO regressions: ARC-1D (−2.3 pts), Manipulate Matrix (−7.0 pts) — attributed to context–task mismatch; the "algorithm-agnostic" claim is partially qualified by these.
- Qualitative Figure 5 (Word Sorting): CBRL-trained model explicitly retrieves ASCII code points and applies step-by-step comparison, mirroring the injected exemplar structure. Baseline produces superficial output and incorrect ordering — direct evidence of reasoning-pattern internalization.

Tasks covered: ARC-1D, Word Sorting, Spell Backward, Matrix Manipulation, Puzzle-24, Q programming.

## Relevance to the project

**Critical.** CBRL's annealed-demonstration curriculum maps directly onto [[../synthesis/concept-curriculum-method]]'s per-concept packet construction: construct a bank of solved examples for each concept, inject with decaying probability during RL training, withdraw scaffold as the policy internalises the reasoning pattern. CBRL provides a concrete, empirically validated instantiation of this structure at small model scale (3B–7B), with a working annealing formula and bank-size guidance (20 examples suffices).

CBRL and DAPO's Dynamic Sampling both target the zero-variance exploration problem from different angles: CBRL rescues failing rollouts via demonstration prepending (input-augmentation); DAPO filters out prompts where all rollouts succeed or all fail (prompt-level filtering). These are complementary mechanisms and could be composed.

Open questions for adaptation: adaptive scheduling (fixed linear decay ignores reward trend), learned retrieval (current bank construction is hand-crafted or requires a stronger model), behavior at >7B scale, and multi-step agentic rollouts.

## Source

- arXiv: 2603.18953
- Raw markdown: `../../../raw/research/weekly-2026-04-23/02-cbrl-context-bootstrapped.md`

## Related

- [[_overview]]
- [[1-shot-rlvr]]
- [[data-efficiency-rft]]
- [[../teacher-student-rl/ho-reasoning-teachers]]
- [[../teacher-student-rl/sakana-rlt]]
- [[../teacher-student-rl/_overview]]
- [[../rl-optimizers/dapo]]
- [[../rl-optimizers/dr-grpo]]
- [[../rl-optimizers/_overview]]
- [[../in-context-learning-theory/_overview]]
- [[../synthesis/concept-curriculum-method]]
- [[../synthesis/single-sample-concept-skeleton]]
- [[../synthesis/proposed-method]]
- [[../../weekly-briefs/2026-04-23]] — brought in by the 2026-04-23 weekly sweep
