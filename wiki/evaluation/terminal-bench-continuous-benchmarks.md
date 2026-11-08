# Terminal-Bench 2.1 and Continuous Benchmarks

"Benchmarks as Software" (Buchanan, Zhou, Linderman, Ré; arXiv 2611.08417, 5 Nov 2026) argues that agentic benchmarks accumulate "benchmark maintenance debt" after release: as models improve they find valid solutions the verifiers reject, and infrastructure changes invalidate assumptions baked into tasks. The authors propose a continuous-validation workflow, audit Terminal-Bench 2.0 with it, find issues in about 30% of the benchmark, and release repairs as Terminal-Bench 2.1. They also show that resource budgets, especially wall-clock limits, change harness comparisons and so belong in the measurement specification.

## Mechanisms

- **Continuous-validation workflow**: combines community reports, task artifacts, agent traces, automated oracle checks, and human-gated repairs.
- **Maintenance debt**: a growing gap between benchmark scores and the capability they are meant to measure; not only implementation bugs, but evaluation assumptions and resource settings that need revalidation as models improve.
- **Resource budgets as spec**: fixed wall-clock can materially change agent performance.

## Numbers (abstract-level)

- Terminal-Bench 2.0 had issues in roughly 30% of tasks despite extensive human and LM-assisted review and red-teaming before release.
- TB 2.1 repairs raise accuracy by over 10 percentage points and move leaderboard positions by up to three ranks; overall ranking remains highly correlated (Spearman rho = 0.958).
- Extending the time limit closes a 20pp harness gap on GPT 5.4 and shrinks a 30pp gap on GPT 5.4 mini to 5pp.

## Implications for this wiki

Terminal-Bench figures cited elsewhere (for example harness comparisons and ADK Arena medians) may predate 2.1 or depend on time limits; treat cross-harness gaps as budget-conditional.

## Authority note

Academic preprint, not peer reviewed. Only the arXiv abstract page was captured, so all figures are abstract-level and no method details or per-task tables were checked. Collect-but-confirm until the full text and TB 2.1 release are reviewed.

## Source

- raw/research/weekly-2026-11-08/01-terminal-bench-continuous.md

## Related

- [[evaluation/benchmarks]]
- [[evaluation/adk-arena]]
- [[evaluation/rigorbench]]
- [[patterns/sol-pi-harness-efficiency]]
- [[evaluation/swe-bench-pro]]
