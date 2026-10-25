# Harness Adaptation Gap on ARC-AGI-3 (arXiv 2610.30499)

A controlled study (Lehmann and Vahdati, arXiv preprint) of whether frontier models can improve their own task harness without human edits. Each model builds an ARC-AGI-3 harness, then revises the whole codebase twice using only development-game evidence. Result: two self-revisions raise mean held-out score by +2.80 RHAE with a 95% bootstrap CI of [-1.44, 7.35], while development score rises +8.42. The difference, the "harness adaptation gap", is the paper's reusable measure. All figures are single-paper, preprint-level, one benchmark; treat as collect-but-confirm.

## Protocol

- A fixed coding bootstrap (OpenCode) has the same model build a full harness (must produce `run.sh`), run it on 5 development games, then revise the whole codebase twice with no human edits. Snapshots H0, H1, H2 are frozen and scored on 20 held-out public games.
- Smoke qualification on 2 dev games allows up to 10 repair cycles.
- Scale: 3 lineages x 9 model-effort conditions (7 model families) = 27 lineages, 81 snapshots, 2,025 game evaluations. Total program cost at least $18,129.27.
- Evaluation noise: 10 re-runs of one frozen harness had SD 3.99 RHAE, comparable to the headline gain.

## The adaptation gap

Gap (G2) = dev improvement minus held-out improvement = 5.62 (CI [1.78, 9.77]). Development gains overstate transfer.

- Per lineage: 15 gains, 12 losses (sign test p=.70). At a 5-point threshold: 9 gains, 3 losses, 15 within threshold.
- Per game: 13 improve, 7 decline (largest +20.44 and -15.03).
- Abstention and rollback: choosing the snapshot with the best dev RHAE post hoc gives +4.53 held-out (CI [0.81, 8.68]) versus +2.80 for always deploying H2, at $9.15 versus $7.57 per game. Keeping the parent when evidence is weak is part of adaptation. The paper cites RRSI-style edit budgets and noise- and cost-aware acceptance as one fix.

## Cost and quality move separately

Of 27 H2 descendants: 9 improve both RHAE and cost, 6 gain RHAE at higher cost, 9 get cheaper but lose RHAE, 3 get worse on both. Mean cost falls $2.72 per game; the median only -$0.54. A Sol-xhigh lineage fell from 43.95 to 21.99 RHAE as cost fell from $31.39 to $7.18 per game; a Sol-high lineage rose from 29.24 to 53.56 at about equal cost by changing action budgeting, memory management and observations.

## What models build and how they revise

- Designs spanned direct model controllers, heuristic-first systems, strategist-executor hybrids, persistent manuals, explicit world models, replay systems, deterministic planners and inference-budget managers.
- Of 54 transitions, 22 of 27 first revisions "Reorient" and none "Replace" the harness family; edits mostly reorganize memory, perception, batching, replay and resource allocation.
- Exploratory revision-behavior coding: all 54 episodes inspected dev evidence and passed proximal checks, yet held-out outcomes varied, so process compliance does not imply improvement. Broad rewrites averaged +3.75 held-out versus -0.20 for contained edits; reactive episodes -0.76 versus +2.48 for hand-off episodes. Both CIs include zero.

## Gap to human steering

At Opus 5 xhigh, revision-2 harnesses average 39.95 RHAE on 20 games versus 100 for the human-steered Tycho (same first author) and 99.86 for Retrodict with Sol. Other baselines: Sol 38.3 in a simple harness (OpenAI report), Claude Code 42.83 (Zeng et al.). The paper notes selection procedures differ, so this does not isolate human steering.

## Caveats

- One benchmark, two revisions, 3 runs per condition; model comparisons are descriptive only. Public games may be in training data.
- Revision-behavior coding was done by an LLM (GPT-5.6 Sol xhigh) with no human agreement check; weak-reliability codes (diagnosis kappa 0.35, incumbent protection 0.47, resource metareasoning 0.29) were excluded.
- Authors report Amazon affiliation but say the work was done outside Amazon. Peer-review status unknown. The supplementary artifact (framework, frozen prompts and splits, snapshots, scripts) is described but no public URL is given.

## Takeaways for this wiki

- Any self-evolving harness result reported on its own development set should be read as an upper bound; report the dev-minus-held-out gap alongside gains.
- Admission gating (keep the parent unless evidence clears noise) is empirically motivated here, supporting designs like [[patterns/moss-production-self-evolution]].

## Source

- raw/research/weekly-2026-10-25/04-llm-improve-own-harness-arc-agi-3.md (arXiv 2610.30499, Lehmann and Vahdati)

## Related

- [[patterns/harness-self-evolution-survey]] - this study is a controlled held-out test of the weight-fixed self-evolution that survey formalizes
- [[patterns/agentic-harness-engineering]] - AHE cited as prior art; this adds generalization caveats
- [[patterns/autodesign-meta-harness]] - same dev-versus-test overfitting question
- [[patterns/sol-pi-harness-efficiency]] - cost/performance tradeoff at a fixed model
- [[patterns/moss-production-self-evolution]] - production admission gating and rollback
- [[patterns/skillos]] - constrained curator over a frozen executor, contrast with unconstrained self-revision
- [[patterns/harness-design-space]] - emergent families (memory, perception, replay) map onto design axes
- [[patterns/harness-scaling-position]] - empirical limits on harness-scaling claims
- [[patterns/code-as-agent-harness]] - harness as code that models write and rewrite
- [[patterns/sdar]] - weight-updating contrast to weight-fixed harness revision
- [[patterns/eureka-agent-environment-engineering]] - agent-driven environment engineering parallel
- [[evaluation/agents-last-exam]] - shared theme of evaluation validity
- [[evaluation/learn2play-bench]] - harness choice at fixed backbone; cross-episode learning
