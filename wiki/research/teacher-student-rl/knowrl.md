---
name: knowrl
description: KnowRL decomposes per-problem hints into atomic knowledge points (KPs) and uses Constrained Subset Search (CSS) to find the minimal-sufficient KP subset, improving GRPO-based RLVR on hard math benchmarks without a KL loss or live teacher.
type: research
---

# KnowRL: Boosting LLM Reasoning via Reinforcement Learning with Minimal-Sufficient Knowledge Guidance

Guo et al., arXiv:2604.12627 (2026). KnowRL introduces an offline KP curation pipeline on top of GRPO-based RLVR: correct solutions are sampled from DeepSeek-R1, decomposed into atomic "indispensable mathematical principles" (KPs), leakage-verified, and then filtered by CSS to the minimal subset that preserves full task coverage. Only hard samples receive hint injection at training time (under a `## Hint` header); no KL regulariser is used; inference runs without KPs, confirming policy internalization rather than hint dependency. The central empirical finding is a "critical-segment effect": accuracy jumps non-linearly once a key KP is included, with flat/diminishing returns from additional hints — demonstrating that reasoning improvement keys on specific concept unlocks, not cumulative token exposure.

## Method

**KP extraction.** For each training problem, sample correct solutions from DeepSeek-R1, then prompt for "indispensable mathematical principles" — the atomic steps whose absence would make the solution unrecoverable. Each KP is leakage-verified (KP alone should not give away the answer) before entering the candidate set $H$.

**Constrained Subset Search (CSS).** Two-phase selection over $H$:
1. *Near-optimal single removal:* For each $k \in H$, remove it and measure accuracy. KPs where removal causes negligible drop are placed in the "near-optimal removable" set $N$ and pruned first.
2. *Enumeration over candidates:* Let $C = H \setminus N$. Enumerate all $2^{|C|}$ subsets of $C$ and select $S^* = \arg\max_{S \subseteq (N \cup \tilde{C})} A(S)$.

Average KP count after CSS: 2.57 (down from 5.86 for full $H$; 1.21 for $N$ pruning alone). Simple problems receive no hints.

**Pruning interaction paradox.** LOO-identified "removable" KPs conflict when removed jointly: $p_m \in [40\%, 60\%]$ of joint removals degrade more than expected from individual ablations. CSS handles this via constrained enumeration rather than greedy LOO, but the offline approximation is imperfect.

**RLVR training.** GRPO-style training with rule-based verifier reward. No KL loss; token-mean loss; entropy annealing (clip_high reduced after step 2,590 to encourage convergence). Hard samples identified by zero-correct rollout fraction inject their CSS-selected KP subset under a `## Hint` header. Backbone: OpenMath-Nemotron-1.5B → KnowRL-Nemotron-1.5B; 8.8k training instances (QuestA dataset); 2,960 steps; 64×H100 GPUs over 13 days.

## Claims

| Model | KPs at inference | Avg (8 benchmarks) | vs. Nemotron-1.5B base | vs. JustRL |
|---|---|---|---|---|
| KnowRL-Nemotron-1.5B | None | **70.08** | +9.63 | +1.50 |
| KnowRL-Nemotron-1.5B | CSS-selected | **74.16** | — | — |

Benchmarks: AIME 2025, HMMT 2025, CMIMC 2025, and five additional math competition/evaluation sets. Gains are largest on hardest tasks: AIME25 +15.11, HMMT25 +12.98, CMIMC25 +15.49 vs. base. Zero-correct fraction drops from 41.21% to 13.00% after training (no KPs at inference), confirming internalization.

Per-problem CSS selection outperforms random KP selection at matched cardinality — structure, not volume, is the signal.

## Relevance to the project

CSS is a concrete, empirically validated mechanism for packet-construction in [[../synthesis/concept-curriculum-method]]: it answers "which prerequisite knowledge atoms should be surfaced for a given problem?" in a principled way. The pruning interaction paradox is precisely the concept-interference problem the curriculum method must handle — naive greedy KP selection degrades, and CSS-style enumeration over a constrained candidate set is the current best answer.

KnowRL also provides direct evidence for the hint-density vs. concept-mastery tradeoff: injecting all KPs can induce regression (Figures 1b and 3), while the minimal-sufficient subset reliably improves training. For the proposed method, this means packet density is a design parameter, not a free variable — more scaffolding is not monotonically better.

## Source

- arXiv: https://arxiv.org/abs/2604.12627
- `../../../raw/research/weekly-2026-04-23/01-knowrl-knowledge-guided.md`

## Related

- [[_overview]]
- [[sakana-rlt]]
- [[saha-teacher-explanations]]
- [[rlt-followups-2026]]
- [[../rl-optimizers/dapo]]
- [[../rl-optimizers/dr-grpo]]
- [[../rlvr-mechanics/deepseekmath-grpo]]
- [[../process-reward-models/_overview]]
- [[../single-sample-rl-finetuning/1-shot-rlvr]]
- [[../synthesis/concept-curriculum-method]] — CSS directly applies to concept-packet-building: it picks which prerequisite KPs to surface per problem
- [[../synthesis/proposed-method]]
- [[../../weekly-briefs/2026-04-23]] — brought in by the 2026-04-23 weekly sweep

## Conflicts raised

**vs. Sakana RLT (hint-design principle).** KnowRL Sec 4.2 uses no KL loss; Figures 1b and 3 show full-KP injection can induce regression on subsets of problems. RLT's design includes both teacher-solution-in-prompt AND $r^{KL}$ plausibility regularisation — regularisation that KnowRL argues is unnecessary and that full context injection is actively harmful when hints are redundant or inconsistent. KnowRL's minimal-sufficient principle (prune until performance drops) is in tension with RLT's maximal-context + plausibility-regularisation principle. The conflict may partially dissolve given different student-capability regimes (RLT targets larger students who benefit from full solution context; KnowRL targets 1.5B students who are confused by it), but as a general hint-design principle they disagree: more teacher context is not universally better.
