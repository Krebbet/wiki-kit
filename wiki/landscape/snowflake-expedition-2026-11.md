# Snowflake Expedition 2026: Business Ontology and Cortex AI Gateway (2026-11)

On 2026-11-03 at Snowflake Expedition 2026, Snowflake announced Business Ontology (governed business definitions, in Horizon Context) and an expanded Cortex AI Gateway (one policy layer for agent access to models, MCP tools and spend), both inside Horizon Catalog. Status is mixed: the gateway core, observability, inference and cost governance are GA; MCP tool governance is public preview; Business Ontology, Cortex Sense and AI Guardrails are "public preview soon"; Sandboxes, Abuse Detection, Trace Intelligence and Dynamic Model Routing are private preview. Source is a single vendor press release (2026-11-03); the only numbers are a Snowflake-sponsored survey and customer quotes. Read: Snowflake is productising agent governance as a platform layer; a credible buy for Snowflake-centric estates, but most differentiating pieces are not yet usable.

## What shipped, with status (per press-release footnotes, 2026-11-03)

| Feature | What it does (vendor description) | Status |
|---|---|---|
| Cortex AI Gateway (core) | "Single front door" for agents; one policy set across clouds, frameworks, AI providers | GA |
| Observability | Records models called, tools used, decisions made, stored in the customer's own Snowflake account | GA |
| Cortex Inference | Inference on Snowflake infrastructure across frontier and open-source models | GA |
| Cost governance | Attributes AI spend to user/team/department/agent/app; hard limits stop runaway agents | GA |
| Cortex AI Gateway Tools (MCP governance) | Authenticates and validates every tool call against fine-grained authorization policies, including on-behalf-of with identity propagation | Public preview |
| Business Ontology | Approved official definitions (e.g. net revenue) linked to tables/views, owner per definition, change log | Public preview soon |
| Cortex Sense | Infers context not already defined (usage signals); approved ontology takes precedence over inferences | Public preview soon |
| Cortex AI Guardrails | Account-wide runtime protection against prompt injection, jailbreaks; covers third-party agents routed via the gateway | Public preview soon |
| Cortex Sandboxes | Agent code execution next to data, inheriting the running user's permissions; launches in seconds | Private preview |
| Agent Abuse Detection | Analyses full agent trajectories (not single prompts); two-stage engine (screening + context-aware reasoning) | Private preview |
| Agent Trace Intelligence | Query traces against business data: loops, failing tools, cost per completed task | Private preview |
| Dynamic Model Routing | Routes each request to an org-approved model by cost, accuracy, latency | Private preview |
| Private Safety Processing (PSP) with OpenAI | Privacy-preserving safety signals from OpenAI to enrich abuse detection; Snowflake was "technical design partner" | In development |

## Techniques

- **Three-layer context model:** Business Ontology governs what a term officially means; Semantic View computes it; Cortex Sense infers undocumented operational knowledge. Human-approved ontology definitions override competing inferences (vendor design claim, 2026-11-03).
- **Metadata graph:** Horizon Context connectors ingest schemas, query logs, dashboard definitions and usage signals from Tableau, Power BI, dbt, SQL Server, PostgreSQL; enriched with lineage, auto tags, AI descriptions, popularity signals and Apache Ossie (incubating) open-standard Semantic Views. Business Ontology is the governance layer over that graph.
- **Migration path:** existing definitions in a third-party catalog or spreadsheet can be imported in one guided CoCo session; extracted domains, terms, relationships and linked assets land as drafts for owner approval. Every change is logged for audit lookups ("what did net revenue mean in Q2, who signed off").
- **Consumers:** CoCo (coding agent for data teams) and CoWork (personal work agent for knowledge workers) use approved concepts to ground answers. See [[platforms/snowflake]] for their earlier status.
- **Gateway as policy choke point:** agents act via MCP servers; the gateway applies existing access policies, authentication and permissions, so agents inherit controls set for human users. Trajectory-level (not prompt-level) abuse detection is the notable technique, and is private preview only.

## Vendor claim vs verifiable

- **Verifiable by footnote, not by use:** GA/preview labels above come from the release itself. No docs, pricing, rate limits or benchmarks are in the source.
- **Vendor claims, unverified:** "eliminates the tradeoff" between agent speed and control; "explainable findings instead of alert noise"; single policy set "regardless of which cloud, catalog, or engine". No numbers on false-positive rate, latency overhead, or routing savings.
- **Survey is sponsored:** MIT Technology Review Insights survey (400 senior data/technology executives, orgs at $500M+ revenue, fielded July-August 2026), sponsored by Snowflake: 55% cite lack of business context as primary cause of low-quality agent insights; 45% cite fragmented or inaccessible data. Sponsor framing favours the product.
- **Customer quotes are vendor-selected:** Glean and Kargo (gateway), dentsu/Merkle (ontology, "early product adopters"), Uniphore (partner). Kargo credits routing and hard limits, but Dynamic Model Routing is private preview per footnote 4; the quote does not say which features are in production use. Treat adoption as unverified.
- **Interoperability claim** (ontology applies to data "inside and outside of Snowflake") is asserted; connector list above is the only concrete evidence.
- No independent review or practitioner feedback captured as of 2026-11-11.

## Build-vs-buy readthrough

- **Buy (watch GA dates)** if data and agents already sit on Snowflake: observability in your own account, per-entity cost caps and MCP tool authorisation are cheaper than a custom gateway, and the GA subset (core gateway, observability, inference, cost governance) is usable now.
- **Wait** on anything touching ontology, guardrails, sandboxing, abuse detection, routing: none is GA. Do not architect around private-preview features.
- **Build or keep third-party** where agents span non-Snowflake estates and you need vendor-neutral policy: the press release claims cross-cloud reach, but enforcement depth outside Snowflake is undocumented here. Compare with [[platforms/databricks]] governance and [[landscape/databricks-data-ai-summit-2026-06]].
- **Lock-in note (inference):** audit trails, ontology and cost data accumulating in Snowflake raises switching cost; the Apache Ossie semantic-view standard is the only stated portability hook.
- Identity propagation and on-behalf-of tool calls map onto the issues in [[landscape/agent-identity-governance-2026-09]].

## Open questions

- Pricing for Gateway, Sandboxes, Abuse Detection and routing (not stated).
- GA timelines for the preview features.
- Which third-party agents and frameworks the gateway supports, and how guardrails reach them.
- Whether PSP ships and what OpenAI signals it carries.

## Source

- `raw/research/weekly-2026-11-11/01-snowflake-expedition-2026.md` (Snowflake press release, "Snowflake Helps Enterprises Deploy AI Agents with Trusted Business Context and Built-In Controls", dated 2026-11-03; captured 2026-11-11)

## Related

- [[platforms/snowflake]]
- [[landscape/snowflake-summit-2026-06]]
- [[platforms/databricks]]
- [[landscape/databricks-data-ai-summit-2026-06]]
- [[landscape/agent-identity-governance-2026-09]]
- [[landscape/nvidia-open-agent-safety-platform-2026-09]]
