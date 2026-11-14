# Evidence-Linked Memory (WikiTrace)

KAIST/DeepAuto.ai (arXiv 2611.14320; Lee, Choi, Baek, Hwang). Agent memory can cause "memory-induced degradation": failures on tasks the agent solves without memory. WikiTrace stores each lesson as an insight linked to a compilation and the raw trajectory, and lets the agent descend through those links with terminal tools before acting. Avg 90.2 vs 79.5 No Memory across 8 suites; Regression 4.5% vs 9.7% rerun baseline. Code released.

## Problem
- Lessons are distilled from trajectories labelled only success/failure, so credit assignment is a guess; wrong lessons mislead on new tasks.
- Aggregate accuracy hides this. The paper separates Gain = P(success | No-Memory majority fail) from Regression = P(fail | No-Memory majority success).
- Diagnosis (LLM-judged, tasks solved 3/3 without memory but failed with it): 52% of failures trace to a followed memory item, 20% to a plainly wrong item; the rest are out-of-scope use, misuse, or a better item ignored. Existing methods (ExpeL, AWM, ReasoningBank) show Regression comparable to or above the no-memory rerun baseline (9.7%).

## Method
- Per past run: a compiler emits a compilation (key decisions, failure causes; separate success/failure templates) and at most 3 insights (what to do, applicability, source ids). Raw trajectory kept unchanged. Layers are indexed and mounted read-only.
- Insights are never updated or deleted; redundant or conflicting ones are left for the agent to adjudicate.
- Test time: agent gets all insights plus the 3 most similar past runs. It descends when an insight lacks detail, conflicts with another, comes from a failed run, or an action fails.
- Memory is built once offline from No-Memory runs, with no validation runs.

## Results
Eight suites: ALFWorld seen/unseen, PlanCraft, tau3-bench Retail, AppWorld normal/challenge, ScienceWorld. deepseek-v4-flash backbone, Pi terminal agent, 3 trials.
- Avg: WikiTrace 90.2, Insights Only 87.0, ReasoningBank 81.7, AWM 81.6, ExpeL 80.3, No Memory 79.5. Best on all 8 suites; only method matching or beating No Memory on all.
- Insights Only (same insights, no source access) isolates the effect: +3.2 avg, Regression 6.5% -> 4.5%, lower on 7 of 8 suites. Gain over rerun +35 pp vs +27 (Insights Only), +7 to +14 (existing methods).
- Descent rate 22% (Easy) to 44% (Hard); descent advantage over staying grows with difficulty (1.8 -> 4.1 pts).

## Caveats
- Single backbone in the main table; the other-backbone result was not checked.
- Descent vs stay is agent-chosen, so confounded.
- Large variance on some suites (e.g. AppWorld Normal 81.3 +/- 8.5).
- Costs of compilation and extra tool calls at inference are not quantified here. The judge model name ("gpt-5.6-sol") and benchmark names such as tau3-bench are unverified.
- Preprint, no independent reproduction.

## Source
- raw/research/weekly-2026-11-14/03-evidence-linked-memory.md (arXiv 2611.14320; github.com/yukyeongleee/wikitrace)

## Related
- [[memharness]] — alternative fix: RL-trained reconstruction of retrieved memory into state-specific guidance
- [[memoharness]] — experience-bank harness optimization
- [[skillopt]] — admission-time validation of skill updates; WikiTrace is complementary use-time checking
- [[self-evolving-agent-harness]] — experience reuse in agents
- [[openclaw]] — file-based agent memory the agent browses with tools
