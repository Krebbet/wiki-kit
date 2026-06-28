# RigorBench (arXiv 2606.22678)

First benchmark evaluating AI coding agents on engineering *process discipline* — how they plan, verify, recover, abstain, and maintain codebase integrity — rather than outcome correctness alone. Published June 21, 2026. Finds a 0.87 correlation between process score and outcome quality, and shows disciplined agents use 12% fewer tokens despite producing more artifacts.

## Motivation: The Process Discipline Gap

A survey of 9 existing benchmarks (HumanEval, MBPP, SWE-bench, BigCodeBench, DevBench, Terminal-Bench, ProjDevBench, AgentBench, LiveCodeBench) found that none measure planning behavior, testing coverage, or recovery strategy — only whether the final output is correct. RigorBench fills this gap by logging the full execution trajectory.

## Five Scoring Pillars

| Pillar | Weight | What It Measures |
|--------|--------|-----------------|
| Planning Fidelity | 0.20 | Does the agent produce and follow a decomposed plan? |
| Verification Coverage | 0.25 | Does the agent write tests proportional to its changes? |
| Recovery Efficiency | 0.25 | Does the agent recover from failures without wasteful loops? |
| Abstention Quality | 0.15 | Does the agent decline impossible tasks instead of hallucinating? |
| Atomic Transition Integrity | 0.15 | Does the agent make atomic, non-breaking commits/edits? |

RIGORSCORE = weighted sum, normalized to [0, 1].

## Key Results (120 runs: 4 harnesses × 30 tasks)

- **Process–outcome correlation**: r = 0.87, p < 0.001. Linear fit: Outcome = 0.41 + 0.54 × RIGORSCORE.
- **Agent-Rigor (6-phase lifecycle harness)**: RIGORSCORE 0.61 / Outcome 0.83 vs. Baseline ReAct RIGORSCORE 0.48 / Outcome 0.64.
- **Structured discipline saves tokens**: disciplined agents use 12% fewer tokens on average despite producing more artifacts — the harness suppresses failed-recovery waste more than planning adds overhead.
- **Planning fidelity gap is largest**: baseline agents score ~0.25 on Planning Fidelity; disciplined agents reach ~0.72–0.89. Agents can plan when scaffolded but don't by default.
- **Abstention baseline is zero**: no baseline agent abstained from any impossible task; all produced plausible-looking wrong answers. Disciplined agents correctly abstained on ~62% of impossible tasks.

## Task Suite Structure

30 tasks across 5 categories:
- **Plan-Then-Build**: multi-step feature implementation requiring decomposition
- **Verify-Or-Die**: must write and pass tests to succeed
- **Doom Loop Gauntlet**: tasks designed to expose try-too-much failure modes
- **Know When to Fold**: 6 impossible tasks testing abstention quality
- **Don't Break the Build**: incremental edits that must preserve test suite

Trajectory-based scoring logs every plan artifact, file diff, command execution, and token count.

## Relation to Existing Evaluation Cluster

RigorBench's five pillars operationalize the failure modes named in [[patterns/effective-harnesses]] (try-too-much, doom loops, declare-done-prematurely) with quantified scores. The TestGen-hacking anti-pattern in [[evaluation/swe-cycle]] maps directly to the False Confidence failure that Abstention Quality is designed to catch. The 12% token reduction finding is consistent with AHE's finding ([[patterns/agentic-harness-engineering]]) that well-engineered harnesses are not net-wasteful.

## Conflict Flag

The +17% outcome improvement from structured harnesses (Agent-Rigor vs. Baseline ReAct) is in mild tension with [[patterns/effective-harnesses]]'s documentation of the try-too-much failure mode — the concern that heavy structure adds overhead. RigorBench's token data (12% *reduction*) suggests the concern is mitigated when the harness is calibrated; the conflict is context-dependent rather than categorical.

## Source

- Raw: `raw/research/weekly-2026-06-28/03-rigorbench.md`
- arXiv: https://arxiv.org/abs/2606.22678
- Captured: 2026-06-28

## Related

- [[patterns/effective-harnesses]] — try-too-much and declare-done-prematurely failure modes operationalized here
- [[patterns/agentic-harness-engineering]] — AHE; Terminal-Bench 2 cited in RigorBench's related-work
- [[evaluation/swe-cycle]] — SWE-Cycle's TestGen-hacking = Abstention Quality failure mode
- [[patterns/harness-design-space]] — both do empirical cross-harness comparisons
- [[case-studies/cursor-agent-harness]] — Cursor Rules as a configuration-level discipline mechanism
- [[patterns/sierra-monitor-eval-of-evals]] — both argue outcome metrics miss process quality
