# Agent Benchmarks

Public benchmarks that recur across the 2025–2026 agent literature. Useful for tracking capability frontier and comparing framework claims — *not* a substitute for domain-specific evaluation on your own traces.

## What each measures

### General-purpose agent benchmarks

- **SWE-Bench / SWE-Bench Verified / SWE-Bench Pro** — real GitHub issues; code-editing and patch-generation agents. *(2025 versions current.)*
- **OSWorld / OSWorld Verified** — desktop-environment agents; computer-use tasks across applications. *(2025.)*
- **GAIA** — general-AI-assistant benchmark; tool use plus reasoning. Cited: 15% model accuracy vs 92% human (comprehension-generation gap — see [[failure-modes#model-capability-limits]]).
- **WebArena** — web navigation and task completion.
- **AgentBench** — heterogeneous environments; broader agent-capability probe.
- **AppWorld** — multi-turn agent benchmark with normal / challenge splits; leaderboard snapshot September 2025. Used in the ACE paper (see [[agentic-context-engineering]]).

### Tool-use / schema-constrained

- **BFCL v4 (Berkeley Function Calling Leaderboard, 2025)** — multi-turn enterprise tool use. Primary benchmark for SLM tool-calling claims (see [[slm-agents]]).
- **StableToolBench** — virtual API server, reduced API drift. Companion to BFCL for reproducible tool-use evaluation. *(2024–2025.)*
- **JSONSchemaBench / JSON Schema Test Suite** — schema-compliance evaluation for guided-decoding stacks (Outlines, XGrammar, SGLang).

### Domain-specific

- **DDXPlus** — medical differential diagnosis. ACE cited +15.0% (75.2% → 90.2%).
- **FiNER** — financial named-entity recognition.
- **Formula** — financial formula extraction.
- **BIRD-SQL** — text-to-SQL.

### Code / QA (legacy in this context)

- **HumanEval / MBPP** — code generation (older; still used in reasoning-framework ablations).
- **SQuAD** — reading comprehension (legacy; appears in software-repair pipelines).

*(Primary sources: arXiv 2601.12560 2026-01, arXiv 2508.17692 2025-08, arXiv 2510.03847 2025-10, arXiv 2510.04618 2025-10, arXiv 2507.13334 2025-07.)*

## When benchmarks mislead

- **Benchmark contamination.** Frontier models are likely trained on the tasks. Treat absolute numbers cautiously; relative gains under controlled ablations are more informative.
- **Public ≠ your workload.** Benchmark traces do not resemble your production traffic. Hamel's position (see [[error-analysis]]): build your own eval set from real traces *before* reading benchmark leaderboards.
- **Framework-claim inflation.** Framework authors report their best configuration; your setup may regress. Reproduce claims before committing.
- **Version drift.** SWE-Bench / OSWorld both shipped "Verified" / "Pro" revisions within 12 months; older results may not compare cleanly. Always cite the specific benchmark revision and the model version.

## The reasoning-model-era shift

**OpenAI o1 / o3 / GPT-5**, **Gemini 3 Pro**, and the 2025–2026 Claude reasoning models internalize inference-time search. Benchmark gains from elaborate agent scaffolding are shrinking: a single reasoning-model call now subsumes what multi-agent scaffolding accomplished a year earlier. *(arXiv 2601.12560, 2026-01; practitioner-consensus; emerging.)*

Re-benchmark your own stack against a naked reasoning-model baseline periodically — scaffolding that was load-bearing on non-reasoning models may now be dead weight.

## Source

- `raw/research/effective-agentic-patterns/08-arxiv-2601-12560-agentic-ai-taxonomy.md` — Arunkumar V et al., 2026-01.
- `raw/research/effective-agentic-patterns/09-arxiv-2508-17692-agentic-reasoning-survey.md` — Bingxi Zhao et al., 2025-08.
- `raw/research/effective-agentic-patterns/05-hamel-llm-evals-faq.md` — Hamel / Shreya 2026-01.
- `raw/research/fine-tuning-vs-context-slms/03-arxiv-2507-13334-context-engineering-survey.md` — Lingrui Mei et al., 2025-07 (GAIA framing, long-context costs).
- `raw/research/fine-tuning-vs-context-slms/04-arxiv-2510-03847-slm-agentic-systems-survey.md` — Raghav Sharma, Manan Mehta, 2025-10 (BFCL v4, StableToolBench, JSONSchemaBench).
- `raw/research/fine-tuning-vs-context-slms/05-arxiv-2510-04618-agentic-context-engineering.md` — Qizheng Zhang et al., 2025-10 (AppWorld, DDXPlus, FiNER, Formula, BIRD-SQL).

## Related

- [[error-analysis]]
- [[llm-as-judge]]
- [[failure-modes]]
- [[reasoning-frameworks]]
- [[slm-agents]]
- [[agentic-context-engineering]]
