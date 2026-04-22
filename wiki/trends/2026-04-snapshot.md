# Trend Snapshot — 2026-04

Pointer page aggregating the live themes across the wiki as of 2026-04-22. Intended to be the recurring artifact that the weekly-digest pipeline populates. Each bullet links to the page where the theme is documented with evidence class and source traceability.

## Frontier capability

- **Reasoning models internalize inference-time search.** Single-call o1 / o3 / GPT-5 / Gemini 3 / Claude reasoning-generation collapses scaffolding that was load-bearing a year earlier. → [[reasoning-frameworks]], [[benchmarks]].

## Standardization

- **MCP is the sticky convention** for cross-framework tool discovery and governance. Protocol layer *below* frameworks, different category from LangGraph-style orchestration. → [[framework-skepticism]], [[topology-taxonomy]].

## Evaluation discipline

- **Measurement-first thesis consolidating** (Hamel / Shreya). → [[measurement-vs-architecture]], [[error-analysis]].
- **Binary pass/fail displacing Likert scales.** → [[llm-as-judge]].
- **LLM-as-judge hardening into a protocol** (100+ labels prerequisite, >90% alignment, weekly recalibration). → [[llm-as-judge]].
- **Custom annotation UIs as table-stakes infra** (~10x iteration speedup cited). → [[error-analysis]].

## Architecture discourse

- **Convergent framework skepticism** across lab + practitioner + academic voices. → [[framework-skepticism]].
- **Agentic engineering** being named as a professional discipline (distinct from vibe coding). → [[agentic-engineering]].

## Emerging alternatives to fine-tuning

- **Skill libraries** (Voyager-style) as non-parametric learning. → [[reasoning-frameworks]].
- **GUI agents shifting toward SFT/RL** as complexity rises. → [[fine-tuning-vs-context-engineering]].
- **Agentic Context Engineering (ACE)** — structured playbook evolution rivals fine-tuning without weight updates on multi-turn agent benchmarks. → [[agentic-context-engineering]].

## SLM agents — the new default

- **SLM-default, LLM-fallback** is the architectural thesis converging across NVIDIA Research (2025-06) and the October 2025 agent-systems survey. Fine-tuned 1–12B models serve the bulk of agent calls; frontier LLMs reserved for residual complexity. 10–30× cheaper at inference. Guided decoding (Outlines / XGrammar / SGLang) and validator-first tool execution are the enabling techniques. → [[slm-agents]].

## Context engineering as a formal discipline

- **Context engineering** is now a named, taxonomised field — not just "prompt engineering with extra steps." The July 2025 survey reviews 1,400+ papers, formalises the context composition, and flags the **comprehension-generation asymmetry** as the field's central limitation. → [[context-engineering]], [[failure-modes#model-capability-limits]].

## The FT-vs-context question, answered

- The decision framework synthesised across five sources has moved from "open gap" to load-bearing guidance. → [[fine-tuning-vs-context-engineering]]. Remaining sub-gaps tracked at [[ft-vs-context-engineering]].

## Production deployments, now cataloged

- Per-company case pages under `case-studies/`: [[klarna|Klarna]] (hybrid-correction lesson), [[cursor-fast-apply|Cursor Fast Apply]] (FT-SLM exemplar), [[perplexity|Perplexity]] (SLM-default routing), [[stanford-51-enterprise-playbook|Stanford 51-deployment playbook]] (academic synthesis). Cross-lever catalog at [[production-deployments]].
- **Escalation-vs-approval** is a new named design lever. Stanford's quantification: **71% vs 30% median productivity gains** across 51 mature deployments. → [[escalation-vs-approval]].
- **Metric-masked quality degradation** is the dominant practical-risk theme emerging from Klarna. Named failure mode → [[failure-modes#metric-masked-quality-degradation]].
- **Academic-synthesis validation** of measurement-first and framework-skepticism theses. Upgraded from practitioner-consensus to practitioner-consensus + academic synthesis. → [[stanford-51-enterprise-playbook]].

## Live design constraints

- **Cost-depth tradeoff** in hierarchical reasoning — exponential token overhead. → [[topology-taxonomy]], [[failure-modes]].

## What's not covered yet

- Absolute dollar / millisecond economics at production volumes. Sources give ratios, not bills; Klarna's $40M is projected not audited.
- Practitioner takes (Eugene Yan, Hamel, Chip Huyen, Shreya) directly on FT-vs-RAG — not yet surfaced by any research run.
- Independent third-party replication of ACE headline claims, SLM survey Table II, and Stanford's 71% / 30% escalation-vs-approval gap.
- Failed-deployment post-mortems — Stanford's 61% prior-failure stat names categories, not specific post-mortems.
- Enterprise data integration, schema discovery, governance, provenance. → [[enterprise-data-integration]] (gap page, targeted follow-up research queued).
- Twitter / Discord / podcast watchlist signals and named-individual tracking — bootstrap listed these as desired sources; no feeds ingested yet.
- Enterprise self-published engineering blogs — wiki is skewed to vendor and academic sources.

## Source

This snapshot is a synthesis over the wiki pages linked above; no new raw sources. Generated during a `/query` session on 2026-04-22. The first source corpus was ingested 2026-04-22 (see [[log]]).

## Related

- [[building-effective-agents]]
- [[measurement-vs-architecture]]
- [[framework-skepticism]]
- [[reasoning-frameworks]]
- [[fine-tuning-vs-context-engineering]]
- [[slm-agents]]
- [[agentic-context-engineering]]
- [[context-engineering]]
- [[escalation-vs-approval]]
- [[klarna]]
- [[cursor-fast-apply]]
- [[perplexity]]
- [[stanford-51-enterprise-playbook]]
- [[production-deployments]]
- [[ft-vs-context-engineering]]
- [[enterprise-data-integration]]
