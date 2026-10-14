# Snowflake

Cloud data platform (originally warehouse, now extending to AI via Cortex). Same rough ARR as Databricks but growing ~half as fast, with 10x-smaller AI revenue and declining NRR — the incumbent under structural pressure from Lakehouse, per current coverage.

**Tier:** enterprise platform. **Working verdict (2025-12):** hold for installed customers (switching cost, ecosystem); greenfield buyers should weigh the growth and AI-momentum gap vs [[databricks]] *(synthesis — single opinion source)*.

## What it does

Cloud data platform that separated compute from storage (the original innovation); now extending into AI via the **Cortex AI** family, **Snowflake Intelligence**, and "AI Data Cloud" positioning (SaaStr 2025-12-03, quoting Snowflake Q3 FY26 earnings).

## Techniques under the hood

- **Cortex AI** family (specifics not in captured source).
- **Embracing open table formats (Iceberg)** defensively against Lakehouse competition (SaaStr 2025-12-03).

## Deployment model

Not detailed beyond ecosystem partnerships with **SAP, Anthropic, and Google Cloud** (SaaStr 2025-12-03). **Re-check before quoting specifics.**

## Customization hooks

Not detailed in captured source.

## Running costs

Not specified in captured source.

## Hard limits

Not specified in captured source.

## 2026-04-21 — Intelligence + Cortex Code expansion

Snowflake's 2026-04-21 press release expands both agentic product lines and positions Snowflake as the "control plane for the agentic enterprise." Same-day competitive framing as Google Cloud Next '26 Day 2 (see [[google-cloud-next-2026-day2]]).

### Snowflake Intelligence (business-user agent)
- **MCP connectors** (GA "soon"): Gmail, Google Calendar, Google Docs, Jira, **Salesforce**, Slack. Second major platform after Salesforce to ship MCP as the primary integration layer — extends [[open-questions-2026-04]] C17.
- **Skills** — user-defined workflows described in natural language, reusable and shareable.
- **Artifacts** — save/share analyses + visualizations as reusable objects; clean abstraction layered above raw output.
- **Deep research** — multi-step agentic reports spanning structured, unstructured, and external data.
- **Personalization layer** — continuous behavioral learning (mechanism not disclosed).
- **iOS mobile app** (public preview "soon"). No self-hosted option.
- **9,100+ customers using Snowflake AI products weekly** (2026-04-21). Named production: Capita, Logitech, Telenav (20 TB/month, 200M events/day), United Rentals (1,600+ locations), Wolfspeed (dozens of agents across manufacturing/finance/supply chain).

### Cortex Code (builder agent; launched November 2025)
- **External system support**: AWS Glue, Databricks, Postgres — Cortex Code now reaches beyond Snowflake compute for data builders.
- **MCP + ACP (Agent Communication Protocol)** — external AI agents can call into Cortex Code; Cortex Code can orchestrate across external agents.
- **VS Code extension** (private preview) + **Claude Code plugin** — IDE-layer Anthropic partnership.
- **Agent SDK** (Python + TypeScript) — embed Cortex Code capabilities into external apps.
- **Cloud Agents** (private preview) — browser-based execution, no local setup.
- **Plan Mode** — preview execution plan, require approval before run. Good agentic-safety pattern.
- **Snap & Ask** — attach visual artifact (chart/table) to prompt.
- **>50% of Cortex Code customers active** (2026-04-21, vendor metric; "active" not defined).
- **Accenture** cited as leading global partner — "thousands of practitioners" and "nearly two dozen purpose-built skills." GSI adoption typically precedes enterprise volume.

### Why it matters

- Dual-persona strategy (Intelligence for business users, Cortex Code for builders) with unified governance — mirrors the broader enterprise pattern.
- **MCP-first and multi-vendor at the integration layer** (AWS Glue, Databricks, Postgres, Claude Code, Anthropic) while positioning as the *control plane*. See [[open-questions-2026-04]] C17 (pattern) and C18 (multi-vendor claim).
- Forward indicator for [[open-questions-2026-04]] C10 (NRR): 9,100+ weekly AI users + Accenture scale is usage tailwind; no NRR data itself in this release. Watch FY27 earnings.

## Market reception (2025-12-03, Q3 FY26 earnings)

- **~$5B ARR annualized; 29% YoY growth.**
- **NRR: 125%** — declining trajectory: 158% (IPO) → 171% (peak) → 135% → 127% → **125%**. Management calls it "stabilized"; source disputes — see [[open-questions-2026-04]] C10.
- **$100M AI revenue run-rate** — 10x behind Databricks' $1B+ (SaaStr 2025-12-03).
- AI "linked to roughly 50% of new bookings" — leading indicator per management.
- **688 customers paying $1M+; 766 Forbes Global 2000 customers.**
- **$4.4B cash and investments.**
- **Valuation: ~$74B public; ~15x revenue multiple** — roughly half [[databricks]]'s multiple at similar ARR.
- Q4 guidance: 27% growth.
- Author's (not company) extrapolation: $5B → $6.45B → $8.3B; path to $10B ARR by 2027 at 29%.

## Hype-vs-reality delta

- **NRR "stabilized" disputed**: SaaStr argues the 158 → 171 → 135 → 127 → 125 trajectory indicates product-velocity and / or competitive problems, not a floor. "Stabilizing at a lower level isn't the same as re-accelerating." Flagged for reconciliation once FY27 data lands (SaaStr 2025-12-03).
- **Two-front pressure**: Snowflake is defending warehousing while attacking AI; [[databricks]] is attacking on both (SaaStr 2025-12-03). Author's framing.
- Management's "easiest and most cost-effective" positioning is not directly challenged in the captured source.

## Techniques worth stealing

- **Compute / storage separation** (historical innovation) — the architectural move that defined the first wave.
- **SQL-analyst ergonomics** — pull from the business user rather than pushing technology at them.
- **Deep ecosystem integrations** (SAP, Anthropic, Google Cloud) as a moat strategy for a platform being attacked on product velocity (SaaStr 2025-12-03).

## Build-vs-buy signals

- **Installed-base fortress**: 688 $1M+ customers and 766 Global 2000 customers suggest high switching cost — migration away is not trivial.
- For greenfield buyers, source's bear case (20% growth, NRR to 120%, multiple compression) is the risk signal.
- AI revenue must **5–10x by end of FY27** (to $500M+) for the competitive narrative to shift, per source.

## Cortex stack deep-dive (web research 2026-10-05, via /query)

Source: ad-hoc web research (Snowflake docs/release notes + practitioner blogs); not yet captured to `raw/`. Many details come from search snippets and fetch summaries — **re-verify before quoting**.

### Semantic layer
- **Semantic View** = schema-level object (logical tables, relationships, dimensions, facts, metrics); replaces the older YAML-on-stage semantic model. Feeds Cortex Analyst, CoWork, CoCo, Cortex Sense. Docs list no Analyst rate limits.
- **Cortex Analyst** = REST text-to-SQL grounded in a semantic view. Model chosen automatically by region/access (docs preference list: Claude Sonnet 4.6/4.5, GPT-4.1, Arctic Text2SQL R1.5, then Mistral Large 2 / Llama 3.1 70b). Multi-turn re-sends history but cannot see prior results; long chats degrade.
- **Semantic View Autopilot** (GA 2026-02-03): auto-generates views from table metadata, query history, SQL, Tableau/Power BI files (Power BI ingestion GA 2026-08-18); humans still review/certify. Docs advise <10 tables and ~50 columns per view → large estates need many scoped views (inference). Third-party-cited limits (unverified): 1 MB YAML, no ARRAY/VARIANT/OBJECT, no cross-account replication.
- **OSI** (Open Semantic Interchange): spec v0.1 finalized 2026-01, Apache 2.0, 50+ members incl. Salesforce, Databricks, dbt; reportedly now "Apache Ossie (incubating)".
- **Cortex Sense** (private preview, Summit 2026-06): runtime context layer learning from query history, metadata, BI dashboards. Vendor claim 47%→83% accuracy for CoCo/CoWork (secondhand, unverified).
- **Pricing:** Analyst billed per message (~67 credits/1,000 per third parties, unconfirmed) + warehouse compute.

### SQL agent accuracy — vendor claims only
- "90%+" Cortex Analyst claim = internal 150-question BI set, blog 2024-08-29; no updated 2026 methodology, no independent replication found. Practitioners say it holds "when the semantic model is mature"; est. 60–70% without one (consultancy, unsourced).
- Databricks claims "32%→90%+" on its own unreleased benchmark (2026-05-08) — the two 90% figures are **not comparable**.
- Arctic-Text2SQL-R1 (2025-05): 71.83% BIRD-test (32B), open weights; no evidence it powers Analyst. Snowflake CoCo 72.1% vs 65.1% Claude Code/Codex on dbt Labs' ADE-bench (2026-01, vendor-run). Measures data-engineering, not BI Q&A.
- Known failure modes (Snowflake's own docs + AtScale, biased): join hallucination, fan/chasm traps, valid-SQL-wrong-business-definition, conflicting metric definitions, low-cardinality categoricals.
- **Gap:** no independent Cortex vs Genie vs Google head-to-head; no CoWork reliability reports. Build your own eval on your schema (verified queries + built-in Evaluations).

### Agentic loop / harness
- **Cortex Agents:** Plan → tool-use → reflect/respond loop within one request. Agent object = model + tools (Analyst, Search, code exec, UDF/proc custom tools, MCP, web search, skills) + `instructions.orchestration`/`response` + `tool_resources`. Server-side **threads** hold state. Configurable: orchestration token budget, `tool_choice` pinning, `background: true`; 15-min default stream timeout.
- **2026-04-13:** agents on semantic views generate SQL directly (no separate Analyst call). **2026-08-28:** Snowflake "recommends transitioning" Analyst → Agents; semantic views carry over; no EOL date seen.
- Models in agent docs: Claude Opus 5 / Sonnet 5 / Haiku 4.5, GPT-5.x, Gemini 3.1 Pro / 3.5 Flash.
- **CoCo:** CLI/Desktop/Snowsight; Plan Mode (read-only, approve before run), Cloud Agents (managed runtime, browsing + FS + code exec), ACP, Agent SDK ("same loop as CLI"), OS sandboxing + tiered approvals. Underlying models not named in docs.
- **Observability:** AI Observability on TruLens (LLM-as-judge relevance/groundedness/correctness + tracing).
- **Governance:** `CORTEX_USER`/`CORTEX_AGENT_USER` roles + privileges on every tool's objects; per-user quotas GA (AI Functions, Agents, CoWork). Natoma intent announced 2026-05-27; closing status unchecked.
- **Cost:** AI Credits $2.00 global / $2.20 home-region (since 2026-04-01). Agent cost = orchestration tokens + Analyst tokens + Search + warehouse compute for tools, spread over four Account Usage views. Anecdotes (cost-tool vendor, biased): 5–15 LLM calls per question; one team $200/wk test → $4,000/wk prod at 80 daily users; iteration caps of 5–10 cut cost 20–30%.
- **Gotchas:** tool-name typos fail silently at `CREATE AGENT`; broken semantic-view refs surface only at runtime; Agents API unsupported from Streamlit-in-Snowflake warehouse runtime. Practitioner (QueryPlane): tool-description quality dominates tool selection; use 24–32k orchestration tokens.
- **Gap:** rate limits, context size, model-routing internals, Horizon, Agent SDK internals not found.

### Front-ends and custom deployment (web research 2026-10-05, via /query)
Verdict: Cortex is **not** tied to Streamlit. Streamlit-in-Snowflake (SiS) is the easiest path; custom apps cost you the hosting/auth plumbing. Re-verify details — much from snippets/practitioner posts.
- **Agents REST API** (`POST /api/v2/databases/{db}/schemas/{schema}/agents/{agent}:run`, SSE streaming; agent object ref or inline config) — callable from any language/backend. Auth: PAT (fastest start), key-pair JWT (headless backends), OAuth (end-user identity). Caller needs `CORTEX_USER`/`CORTEX_AGENT_USER` + USAGE on agent + warehouse + tool privileges. Unverified: PAT network-policy specifics, SSE buffering behind Next.js/API gateways.
- **SiS warehouse runtime:** Conda-channel packages, slower start, per-viewer runtime; **Cortex Agents API unsupported** (per Snowflake quickstart + practitioner post).
- **SiS container runtime:** Streamlit 1.50+, PyPI packages (needs external access integration, EAI), compute-pool billing (docs: "significantly less" than warehouse), no `_snowflake` module (read OAuth token from `/snowflake/session/token`, call REST via `requests`), not in gov regions. Practitioner: two EAIs needed (package index + Agents REST). Warehouse-runtime deprecation not confirmed (container-first is inference).
- **SPCS** hosts any container (React/Next.js etc.) with a stable ingress URL, but ingress auth = Snowflake sign-in → **end users must be Snowflake users** (blocks customer-facing apps). Single-source cost gotcha (select.dev/Flexera): public-endpoint services auto-resume but don't auto-suspend on HTTP traffic; XS pool ≈ $4.32/day vs <$3/day Cloud Run.
- **CoWork UI** customization limited to chart settings, agent colors/themes/fonts; no documented embed/white-label. Branded UI = REST + own front end.
- **Native Apps:** Agents + MCP servers GA 2026-08-07; SPCS-hosted custom MCP servers usable by agents/CoWork (ISV distribution route; details unverified). Managed MCP server (`CREATE MCP SERVER`) wraps Search/Analyst/Agents/UDFs/procs, OAuth for external clients.
- **Evidence quality:** mostly tutorials by Snowflake-affiliated authors; no neutral friction reports found (no Reddit/HN sweep).

## Source

- `raw/research/enterprise-ai-landscape-2026/06-saastr-databricks-snowflake.md`
- `raw/research/enterprise-ai-landscape-2026/02-menlo-state-2025.md` (infra-layer context)
- `raw/research/weekly-2026-04-23/02-snowflake-intelligence-cortex-code-2026-04.md` (Snowflake press release, 2026-04-21)

## Related

- [[databricks]]
- [[salesforce]]
- [[ai-app-categories-2025]]
- [[enterprise-ai-market-2025-2026]]
- [[google-cloud-next-2026-day2]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]]
- [[open-questions-2026-04]]
