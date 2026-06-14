# Agents' Last Exam (ALE)

ALE (Agents' Last Exam) is a 1,490-task benchmark from UC Berkeley's Dawn Song lab that evaluates AI agents on verifiable, long-horizon professional workflows grounded in the SOC 2018 / O*NET occupational taxonomy — the first benchmark with complete coverage across all 55 industry subdomains. Frontier agents achieve below 1% full pass rate on the hardest tier.

## Source

- arXiv 2606.05405 — "Agents' Last Exam: A Benchmark for Long-Horizon, Economically Valuable Agent Tasks" (UC Berkeley, June 2026)
- Raw: `raw/research/weekly-2026-06-14/01-01-agents-last-exam.md`

## Key claims

- **Evaluation gap is the problem**: current benchmark success has not translated into measurable economic output; ALE argues this reflects an evaluation problem (benchmarks are too narrow / contaminated / low-horizon), not solely a capability gap.
- **Complete occupational coverage**: 55 SOC 2018 subdomains across 13 industry clusters; the union of 16 prior benchmarks leaves 13 subdomains entirely uncovered. Prior benchmarks cluster in computing/engineering.
- **Expert-sourced tasks**: 250+ domain experts contributed tasks from projects they actually completed (taking days–weeks of professional work). Not curator-invented scenarios.
- **Full CUA-agent target**: tasks run on Linux/Windows VMs requiring interleaved GUI and CLI use. The benchmark defines the "Generalist CUA-agent" (GCUA) architecture: Brain (LLM), Eyes (screen/screenshot), Body (memory), Hands (input control), Feet (OS). 
- **Automated evaluation**: deterministic artifact checks or structured rubrics wherever possible; LLM-as-judge used only where no checkable artifact exists.
- **Hardest tier (Last-Exam, 38 tasks): 0% full pass rate** for every mainstream agent tested. Best overall result: Codex + GPT-5.5 at 24.0% on the full public set.
- **Model > harness (~3× spread)**: foundation model choice accounts for roughly 3× the performance spread that harness choice does among well-engineered systems. The model is the binding constraint.
- **Dominant failure mode is domain knowledge**: Understanding + Approach failures account for ~75% of cases, not execution capability failures.

## Three difficulty tiers

| Tier | Tasks | Top pass rate | Notes |
|---|---|---|---|
| Near-Term | 67 | ~38% (Codex + GPT-5.5) | Multi-step but within current model capability |
| Full-Spectrum | 55 | ~20% | ≥1 task per all 55 subdomains |
| Last-Exam | 38 | 0% (nearly all agents) | Saturation-resistant ceiling; professional week-scale tasks |

## Representative results (public set, OpenClaw-fixed harness)

| Agent | Overall pass | Near-Term | Notes |
|---|---|---|---|
| Codex + GPT-5.5 | 24.0% | 38.1% | Best overall; $243 API cost for Near-Term tier, 154h wall-clock |
| OpenClaw + GPT-5.5 | 21.1% | — | Fixed harness comparison |
| OpenClaw + Claude Opus 4.7 | 15.1% | — | — |
| OpenClaw + Claude Sonnet 4.6 | 9.9% | — | — |
| Cursor + Claude Sonnet 4.6 | ~32–34% (Near-Term est.) | — | — |

**ALE-Claw**: simplified OpenClaw-derived GCUA achieves comparable performance to full OpenClaw, confirming that the core GCUA loop (single LLM call, GUI-as-Tool, context compaction) is sufficient — complexity does not help.

## Terminal-Bench vs ALE-CLI gap

A key calibration finding: Codex + GPT-5.5 achieves 82% on Terminal-Bench 2 but only 23.3% overall on the ALE-CLI subset (and 0% on Last-Exam tasks). ALE-CLI tasks require longer, harder multi-step sessions; Terminal-Bench is not predictive of ALE-level difficulty.

## Domain performance variation

- **Highest performing**: computational math, agriculture/environment (~55–85% for frontier models)
- **Lowest performing**: education (<25%)
- **GUI underutilization**: 34% of public tasks designate GUI software as primary tool; agents mostly substitute CLI/Bash workarounds, correlating with the domain-knowledge failure mode

## Benchmark anti-contamination design

- 10% of tasks (150 of 1,490) are public; remainder are private and rotate
- Five-gate construction: expert sourcing → submission → first-pass review → engineering implementation → final QC peer review
- Average task cost per run: $3–10, tens of minutes to hours

## Related

- [[evaluation/swe-bench-pro]] — SWE-bench positions on 5/55 SOC subdomains; ALE extends to full professional multi-domain workflows; ALE is substantially harder than SWE-bench
- [[evaluation/swe-cycle]] — parallel critique: both argue binary resolve rate misses the real-world gap; SWE-Cycle targets the full issue-resolution cycle, ALE targets full professional workflows
- [[evaluation/adk-arena]] — meta-benchmark comparison: both evaluate agentic systems; ALE targets professional task completion, ADK Arena targets framework comparison
- [[patterns/agentic-harness-engineering]] — AHE targets Terminal-Bench 2 (82%); ALE-CLI at 23.3% for the same agent sets a harder ceiling for harness improvement
- [[patterns/harness-design-space]] — ALE's 3× model-vs-harness spread quantifies the relative impact of harness design
- [[patterns/effective-harnesses]] — ALE's model-dominance finding supports effective-harnesses' framing that model capability is the primary lever
- [[deployments/cognition-cloud-agents]] — long-horizon professional tasks are the target regime for cloud agent deployments; ALE is the first evaluation instrument calibrated to that regime
- [[coding-agents/coding-agent-adoption]] — adoption data shows coding agents pervasive in new projects; ALE provides the performance ceiling for what those agents actually achieve on professional tasks
