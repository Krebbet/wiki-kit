# Databricks

Unified data + AI platform ("Lakehouse") competing with hyperscalers on data workloads and with Snowflake on warehousing. Currently the clearest enterprise-platform winner on AI revenue — **>$7B revenue run-rate, growing >80% YoY** (Q2 2026, closed 2026-08-13); closed a **$5B round at $190B valuation**, up from $165B–$175B talk-stage estimates in June 2026.

**Tier:** enterprise platform. **Working verdict (2026-06):** buy-signal for AI-native data / ML workloads; initial-deployment winners tend to win expansion *(synthesis — single source)*.

## What it does

Unified Lakehouse combining data-lake flexibility with data-warehouse performance, plus AI tooling for model serving, vector search, and agent building on enterprise data (SaaStr 2025-12-16).

## Techniques under the hood

- **MLflow** (experiment tracking), **Delta Lake** (storage), **Feature Store**, **model serving**, **vector search**, **Agent Bricks** — platform for building AI agents over enterprise data (SaaStr 2025-12-16).
- Framed as long-running investments since the company's inception — the AI stack built as a coherent layer rather than bolted onto a warehouse.

## Deployment model

Not detailed in captured source beyond competing directly with hyperscalers (AWS / Azure / GCP). **Re-check before quoting specifics.**

## Customization hooks

**Agent Bricks** is the customer-facing mechanism for building AI agents over enterprise data (SaaStr 2025-12-16). Further detail not in captured source.

## Running costs

Not specified in captured source.

## Hard limits

Not specified in captured source.

## Series L+ Funding Close (2026-08-13)

Databricks' own press release confirms the round talked-about in June closed higher than estimated, alongside a fresh revenue disclosure:

- **Closed $5B strategic round at $190B valuation** (vs. $165B–$175B talk-stage range in June) — led by **Coatue**; new investors Blackstone, MGX, T. Rowe Price (Associates + Investment Management), Sixth Street Growth, BOND, Clearlake Capital, Point72, Premji Invest, TPG; existing investors reupped (a16z, Dragoneer, Fidelity, Franklin Templeton, GIC, Goldman Sachs Alternatives, Insight Partners, J.P. Morgan Private Capital, Kinetic, Morgan Stanley Investment Management, NEA, Ontario Teachers' Pension Plan, Temasek, Thrive Capital, WCM).
- **>$7B revenue run-rate, >80% YoY growth** (Q2 2026) — up from $5.4B ARR / 65% YoY in January 2026.
- **Lakehouse (data warehousing):** >$1.5B run-rate, >100% YoY.
- **Lakebase (serverless Postgres for AI agents):** >$100M run-rate — first funding-tied revenue figure disclosed for this product line.
- **Customer concentration:** >1,000 customers at >$1M revenue run-rate; >100 customers at >$10M revenue run-rate. >20,000 organizations total, including adidas, AT&T, Bayer, Block, Mastercard, Rivian, Unilever; "70% of the Fortune 500."
- Positive adjusted free cash flow over the trailing 12 months.
- CEO Ali Ghodsi frames strategy as real-time operational data (Lakebase) + business context (Genie) + multi-AI cost controls (Unity AI Gateway) for enterprise agents. Investor Thomas Laffont (Coatue): Databricks "compressed R&D timelines that used to take years into months, more like a research lab than a typical software company."

Funds earmarked for scaling Lakebase, Genie, and Unity AI Gateway specifically — see [[../landscape/databricks-data-ai-summit-2026-06|databricks-data-ai-summit-2026-06]] for the product-feature detail (Lakebase GA on Azure, Genie One GA, Genie Ontology/ZeroOps) this funding backs.

## Market reception (2026-06, Series L+ valuation talks — superseded above)

- **Valuation: $165B–$175B** (in discussions as of 2026-06-09; round could open as early as July 2026).
- Step-up from $134B in February 2026 — a **23–31% jump in ~4 months**.
- **Revenue run rate: $5.4B annualized** (January 2026 quarter), **65% YoY growth** (up from >55% at the Dec 2025 Series L). Multiple expanding: ~32x vs. ~28x in February — market pricing in continued acceleration, not deceleration.
- **Free cash flow positive** over the prior 12 months.
- **~8,000 employees** as of mid-2026.
- CEO Ali Ghodsi reiterated IPO on track, possibly **2027**.
- February 2026 round mechanics: $5B equity + $2B debt at $134B.
- Source: TechStarts 2026-06-09 (`raw/research/weekly-2026-06-10/01-databricks-175b-valuation-2026-06.md`)

## Market reception (2025-12-16, Series L announcement)

- **$4.8B run-rate ARR**, growing **>55% YoY**.
- **>140% net revenue retention** at ~$5B scale.
- **>$1B AI revenue run-rate.**
- **Data warehousing business crossed $1B ARR** — framed as taking share on Snowflake's home turf.
- **Valuation: $134B private; ~28x revenue multiple.**
- Series L raised; includes employee liquidity provision. IPO pressure noted.
- FCF positive; GAAP profitability not yet at scale.
- Author's (not company) extrapolation: $5B → $7.75B → $12B; path to $15B+ ARR by 2027 if 55% holds.

### Market-reception context

- Menlo names Databricks among infrastructure-layer incumbents "re-accelerating" as even AI-native app builders default to existing platforms (Menlo 2025-12-09). See [[ai-app-categories-2025]].
- a16z 2025 observed enterprises increasingly using Databricks as a third-party host for models where their primary cloud didn't host the target (e.g., OpenAI on AWS-heavy accounts) (a16z 2025-05). See [[llm-api-enterprise-share]].

## Hype-vs-reality delta

- SaaStr argues Databricks' AI advantage is **structural, not cyclical** — attributed to early AI-convergence bets (pre-2022 investments in MLflow / Delta / Feature Store paying off now) (SaaStr 2025-12-16).
- **Law-of-large-numbers risk** flagged in same source: sustaining 55% at $10B ARR would be "historic" — a meaningful caveat to the linear extrapolation *(author's own warning)*.

## Techniques worth stealing

- Early bet on data + AI convergence.
- Build the AI infrastructure stack (experiment tracking, feature store, model serving, vector search, agent platform) as **a coherent layer** rather than bolting AI onto an existing product.

## Build-vs-buy signals

- Source implies enterprises making AI platform bets *now* — initial-deployment winners tend to win expansion (SaaStr 2025-12-16).
- Lakehouse pitch explicitly targets customers who don't want to run warehouse + lake separately. Compelling when that is the pattern; less so for teams with a mature Snowflake + separate ML stack.
- **Lock-in risk:** IPO pending (as of 2025-12-16) could change pricing / terms. Worth a clause in any new contract *(synthesis)*.

## Source

- `raw/research/enterprise-ai-landscape-2026/06-saastr-databricks-snowflake.md`
- `raw/research/enterprise-ai-landscape-2026/02-menlo-state-2025.md` (infra-layer context)
- `raw/research/enterprise-ai-landscape-2026/05-a16z-cio-2025.md` (third-party hosting role)
- `raw/research/weekly-2026-06-10/01-databricks-175b-valuation-2026-06.md` (TechStarts 2026-06-09 — Series L+ valuation talks)
- Databricks press release, 2026-08-13: `raw/research/weekly-2026-08-19/04-databricks-5b-round-190b-2026-08.md`

## Related

- [[snowflake]]
- [[ai-app-categories-2025]]
- [[llm-api-enterprise-share]]
- [[enterprise-ai-market-2025-2026]]
- [[../landscape/databricks-data-ai-summit-2026-06|databricks-data-ai-summit-2026-06]]
- [[../landscape/anthropic-series-h-2026-05|anthropic-series-h-2026-05]] — comparable-scale 2026 mega-raise for cross-vendor comparison
