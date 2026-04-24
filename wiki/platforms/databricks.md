# Databricks

Unified data + AI platform ("Lakehouse") competing with hyperscalers on data workloads and with Snowflake on warehousing. Currently the clearest enterprise-platform winner on AI revenue — **$1B+ AI revenue run-rate at ~$5B total ARR, growing >55% YoY** (as of 2025-12-16).

**Tier:** enterprise platform. **Working verdict (2025-12):** buy-signal for AI-native data / ML workloads; initial-deployment winners tend to win expansion *(synthesis — single source)*.

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

## Related

- [[snowflake]]
- [[ai-app-categories-2025]]
- [[llm-api-enterprise-share]]
- [[enterprise-ai-market-2025-2026]]
