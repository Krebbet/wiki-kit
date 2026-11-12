# Google Agentic Data Cloud — cross-cloud Lakehouse and Iceberg federation (2026-11)

Google Cloud blog post (~2026-11-04) updating its "Agentic Data Cloud": the "borderless Lakehouse" (Apache Iceberg-based) now has cross-cloud interconnect and local caching for AWS and Azure, **generally available**, with "zero variable egress fees" per Google. Iceberg catalog federation with Databricks Unity, Snowflake Horizon and AWS Glue is announced as open-catalog interop. Net read (2026-11): Google is attacking data gravity directly by letting BigQuery-side agents query AWS/Azure data in place. This is a portability win for buyers only if the federation holds up in practice; no independent validation yet.

## What shipped (2026-11-04, vendor claims)

| Feature | Status | Claim |
|---|---|---|
| Cross-cloud interconnect + caching for AWS and Azure (borderless Lakehouse) | **GA** | Private, secure connection; "zero variable egress fees"; retrieved data blocks auto-cached locally in Google Cloud |
| Iceberg catalog federation: Databricks Unity, Snowflake Horizon, AWS Glue | Announced alongside GA item; status not stated separately | Open Iceberg catalog federation |
| Zero-copy integrations: SAP, Workday, Salesforce | Not stated | Zero-copy |
| Gemini on borderless Lakehouse | Not stated | Natural-language queries across clouds |
| Lakehouse integration with Knowledge Catalog | Not stated | Auto-indexes distributed and unstructured data in cloud storage |
| AlloyDB direct Iceberg access | Not stated | Query Iceberg in cloud storage with no ETL; join live and historical data in one PostgreSQL query; "up to 7x faster" aggregations than Amazon's comparable PostgreSQL-compatible service |
| Spanner Omni | **GA** | Hybrid: on-prem, edge, multi-cloud |
| Knowledge Catalog semantic models (BigQuery, Looker/LookML, Databricks, Snowflake, dbt, SAP) | **GA** | Grounds agents in governed definitions without moving data |
| Knowledge Catalog metadata federation (Oracle AI Database@Google Cloud, Snowflake, Databricks Unity, Atlan, Collibra) | Not stated | Discovery and federation |
| Knowledge Catalog self-learning enrichment; Open Knowledge Format (OKF) context sets | Preview | Mines Workspace, GitHub, Jira, Confluence, SharePoint |
| Knowledge Catalog studio experience | Preview | Conversational UI, versioning, rollback |
| Knowledge Catalog on by default in Gemini | Preview | Resolves business terms and join paths before SQL generation, under user permissions |
| Data Agent Kit | GA (announced "recently") | MCP tooling in VS Code, Claude Code, Antigravity |
| AlloyDB Express | Preview | Sub-2-second provisioning, scale-to-zero, 1-2 vCPUs, 20GB |
| PostgreSQL for agents in AlloyDB | Preview | Workload isolation; >3M queries/sec claimed |
| BigQuery Graph | **GA** | Graph analytics on relational tables, zero ETL |
| TimesFM 3.0, TabFM in BigQuery | Preview | SQL-native forecasting / tabular prediction |

Federation GA/preview status for the catalog items is not separated out in the source; treat as unconfirmed until the docs page (cross-cloud data access) is checked.

## Build-vs-buy / lock-in readthrough

- **Portability up, gravity shifts.** Iceberg plus catalog federation with Unity, Horizon and Glue lowers the cost of leaving or straddling a platform. But the query plane, caching and agent grounding (Knowledge Catalog) are Google-hosted: you trade storage lock-in for context-layer lock-in.
- **Egress economics are the real test.** "No surprise variable egress fees" is the pitch, but the source gives no pricing for the interconnect or cache. Model the private-link and cache costs before committing; none are disclosed here.
- **Multi-cloud estates: watch.** If data sits in S3 tables or Azure and agents run on Gemini, the GA cross-cloud path avoids a copy pipeline. Customer cited: Delivery Hero talabat, ~40% lower data-movement costs and queryable within minutes (customer quote, co-marketed).
- **Semantic-model grounding** across Databricks, Snowflake, dbt and LookML is the sticky piece: definitions registered in Knowledge Catalog become the agent's source of truth. Keep canonical metric definitions in your own repo (dbt/LookML) to stay portable.
- **Counter-positions:** Databricks and Snowflake offer their own Iceberg and catalog stories; see [[databricks]] and [[snowflake]]. Federation is only as good as each side's catalog write/read support.

## Vendor-claim caveat

All numbers are Google's: "nearly 4x more accurate, up to 33% lower latency, up to 75% fewer tokens" (Knowledge Catalog, "internal benchmarks"); "up to 7x" AlloyDB vs Amazon's comparable service; Iceberg data under management "more than tripled" in a year; BigQuery queries "over 40% faster", processing cost cut ">50%"; Spark price-performance ">3x". No methodology, workloads or baselines given. Named customers (PayPal, Siemens, Telus, Vodafone, Walmart) are co-marketing, not evidence. Treat "System of Action" and "borderless" as marketing framing.

## Source

- `raw/research/weekly-2026-11-11/05-google-agentic-data-cloud-xcloud.md` (Google Cloud Blog, ~2026-11-04, captured 2026-11-11)

## Related

- [[google-cloud-next-2026-day2]]
- [[google-io-2026-enterprise]]
- [[databricks]]
- [[snowflake]]
- [[microsoft]]
