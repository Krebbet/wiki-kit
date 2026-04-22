# Gap — Enterprise Data Integration

**Status: open gap.** The 2026-04-22 research run captured substantial material on *how agents consume data* (tools, retrieval, memory) but almost nothing on *how to wire LLMs to messy real-world enterprise data sources* — company data lakes, unknown or drifting schemas, privacy boundaries, governance.

## What the corpus does say

- **Hamel field guide (2026)** is the strongest voice. Grounds prescriptions in real production data:
  - Ground synthetic test data in actual database constraints (listing IDs, schedules, business rules) — not ungrounded LLM-generated examples.
  - Treat real conversation / interaction logs as the primary input for improvement.
  - Stratify evals by query category to expose schema-level failure patterns.
  - Custom annotation tools render domain data in domain-intelligent layouts.
- **arXiv 2508.17692 (2025-08)** documents heavy RAG use across scientific / healthcare / materials domains — but *assumes external retrieval is feasible*. No enterprise data governance, privacy, local-only inference, schema discovery.
- **arXiv 2601.12560 (2026-01)** surveys memory systems (**MemGPT**, **MemAgent**, **ChatDB**) — architectural retention and retrieval policies, not enterprise data-integration patterns.
- **Anthropic, Simon, cookbook:** not covered.

*(Evidence class: Hamel is practitioner-consensus grounded in real consulting; the arXiv observations are literature-review only. No source addresses the enterprise-integration problem end-to-end.)*

## What's missing

- Patterns for handing an agent a **data lake of unknown schema** and having it discover its own paths to answers.
- **Privacy and governance patterns** — scope agent access, audit logs, redact PII, stay inside regulatory perimeters.
- **Data-freshness patterns** — how agents know when cached or retrieved context is stale.
- **Enterprise retrieval tooling beyond vector DBs** — SQL, knowledge graphs, hybrid, federated-across-systems.
- **Observability for data paths** — "which data sources did this agent use to produce this answer?"
- Named-practitioner voices on enterprise data + LLMs specifically. Strong writers in the area (e.g., Jason Liu's essays on structured retrieval, Eugene Yan on evals-for-retrieval, enterprise-AI podcast guests) not yet captured.

## Targeted follow-up research

Suggested next `/research` topics:

- *enterprise LLM data integration patterns*
- *agents with unknown schema discovery*
- *LLM observability data provenance*
- *data governance for LLM applications*
- *structured retrieval / text-to-SQL patterns 2026*

## Source

- `raw/research/effective-agentic-patterns/04-hamel-field-guide.md` — Hamel Husain 2026.
- `raw/research/effective-agentic-patterns/05-hamel-llm-evals-faq.md` — Hamel / Shreya 2026-01.
- `raw/research/effective-agentic-patterns/08-arxiv-2601-12560-agentic-ai-taxonomy.md` — Arunkumar V et al., 2026-01.
- `raw/research/effective-agentic-patterns/09-arxiv-2508-17692-agentic-reasoning-survey.md` — Bingxi Zhao et al., 2025-08.

## Related

- [[error-analysis]]
- [[building-effective-agents]]
