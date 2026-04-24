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
