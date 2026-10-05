---
title: "Databricks Data+AI Summit 2026 — Agentic Data Platform"
date: 2026-06-16
tags: [databricks, genie, lakebase, lakeflow, opensharing, agentic-ai, data-platform]
---

# Databricks Data+AI Summit 2026 — Agentic Data Platform

At Data+AI Summit on June 16, 2026, Databricks repositioned itself from a lakehouse vendor to a full "agentic data platform," shipping Genie One (GA), Genie Code (GA), the Genie Ontology context layer, Lakebase GA on Azure across 14 regions, and the OpenSharing open protocol under the Linux Foundation — all unified under Unity Catalog governance. The net effect: Databricks is now directly contesting Snowflake's AI-on-data play, Salesforce's CRM-data boundary, and AWS Glue/SageMaker's end-to-end pipeline story simultaneously.

## What shipped (June 16, 2026)

### Genie One (GA)

Business-facing agentic coworker available on web, iOS, and Android. Extends first-gen Genie (Databricks-only SQL analytics) to structured and unstructured data inside and outside Databricks, connecting to 50+ apps: Google Drive, Jira, Slack, Confluence, SharePoint, and more. Capabilities beyond Q&A: generates documents and reports, schedules tasks, sets monitoring alerts, creates repeatable "skills," and invokes external tools via MCP. No seat-based pricing; organizations get $10/user/month free, pay for AI consumed beyond that.

### Genie Ontology

Live, self-improving context layer shared across all Genie products. Continuously extracts and updates business metadata — metrics, dataset definitions, tags, tickets, chats, meetings — from Databricks and connected apps. Grounds all Genie reasoning in SQL-retrieved authoritative data rather than embedding retrieval. Databricks claims higher answer accuracy, lower latency, and lower token costs vs. RAG-over-documents approach. No separate SKU; bundled into Genie.

### Genie Agents and Genie App Builder (private preview, imminent)

- **Genie Agents**: any Genie conversation can be saved as a named, reusable agent that inherits the session's memory, sources, instructions. Shareable across teams.
- **Genie App Builder**: "vibe coding" environment for non-engineers. Upload business context → Genie generates live build plan and working app preview against governed data. All apps run under Unity Catalog permissions from birth. Entering private preview shortly after summit.

### Genie ZeroOps (private preview, imminent)

Background autonomous agent for DataOps. Monitors live pipelines, jobs, tables, ML models; investigates anomalies using Unity Catalog lineage to trace failures (bad data, upstream schema change, code bug); proposes fixes. Verification runs in a sandboxed zero-copy clone of production data with scoped permissions — nothing applied until operator approves. Targets the monitoring/diagnosis→repair loop that currently requires on-call data engineers. Entering private preview shortly after summit.

### Genie Code (GA)

Autonomous coding agent for data teams; originally launched March 11, 2026, confirmed GA at summit. Covers full-stack data work: builds DLT pipelines from natural language, handles end-to-end ML workflows with MLflow logging, generates AI/BI dashboards. Runs natively in notebooks, SQL editor, Lakeflow Pipelines Editor, and MLflow. Summit addition: dedicated workspace for progress tracking, step review, and multi-thread project management. Databricks reports Genie Code "more than doubled the success rate of leading coding agents" on real-world data science tasks.

### Lakebase (Azure GA, 14 regions)

PostgreSQL-compatible operational database running on the Databricks lakehouse. Reached GA on Azure at summit covering 14 regions: eastus, eastus2, centralus, southcentralus, westus, westus2, canadacentral, brazilsouth, northeurope, uksouth, westeurope, australiaeast, centralindia, southeastasia. Positions Databricks as an OLTP+OLAP platform, eliminating the sync step between operational and analytical stores.

### OpenSharing (Linux Foundation, GA)

Announced June 10, 2026 (pre-summit); formally highlighted at summit. Next evolution of Delta Sharing, now donated to the Linux Foundation as a vendor-neutral open standard. Extends Delta Sharing to cover AI-era assets: agent skills, AI models, and unstructured data. Adds Apache Iceberg IRC client support. Enables on-premises and private-cloud sources to connect to cloud platforms without data movement (zero-copy). Founding backers: OpenAI, SAP, Stripe, Atlassian, LSEG, Amadeus.

### Salesforce partnership expansion

Announced at summit on June 16, 2026. Key deliverables:

- **Slack Genie App**: public preview now, GA targeted H2 2026. Brings Databricks-powered insights and security workflows into Slack.
- **Federated Search**: Agentforce agents can search Databricks; Databricks users can search Salesforce. GA timeline not stated.
- **Data 360 Zero Copy**: MuleSoft Agent Scanner for Databricks and foundational zero-copy capabilities between Salesforce Data Cloud and Unity Catalog are GA now; governance feature enhancements slated H2 2026+.
- Salesforce named Databricks ISV Business App Partner of the Year at the summit.

### Lakeflow Connect Free Tier + agentic data engineering

Free tier: every workspace gets 100 DBUs/day dedicated to managed SaaS and database connectors — enough to ingest ~100M records/day/workspace across eligible sources (Salesforce, Workday, ServiceNow, Dynamics 365, Snowflake, BigQuery, PostgreSQL, MySQL, Oracle, and more). Previously announced at FabCon 2026; highlighted at summit alongside Genie Code's deep integration into Lakeflow UI for creating connectors, building pipelines, and authoring jobs via natural language.

## Novel mechanisms

- **Genie Ontology as persistent context**: departing from session-scoped RAG. A continuously updated, durable enterprise knowledge graph that all Genie products share. Grounding in SQL-queried structured data (not vector similarity) is the stated differentiator — accuracy claim is meaningful if it holds under enterprise messy-data conditions.
- **ZeroOps sandbox verification loop**: zero-copy clone + scoped permissions for agent-proposed fixes before production apply. Closes the "autonomous agent makes unreviewable changes" trust gap.
- **OpenSharing asset-type expansion**: Delta Sharing was tables-only. OpenSharing covers agent skills and model weights — a protocol-level answer to AI asset portability across vendors.
- **Lakebase OLTP convergence**: eliminating the lakehouse's traditional read-only / batch-only limitation by embedding a transactional engine natively, rather than bolting on a Postgres sidecar.

## Competitive implications

- **Snowflake**: Direct assault. Genie One vs. Cortex Analyst; Genie ZeroOps vs. Snowflake's Horizon observability; Lakebase vs. Snowflake's OLTP ambitions (Unistore). OpenSharing explicitly supports Iceberg — vendor-neutral data sharing is a shot across Snowflake's proprietary-format bow.
- **Salesforce**: Partnership softens competitive tension at the data layer, but Genie One's 50+ app connectors (including Slack) mean Databricks is now a workflow surface, not just a data store. The Slack Genie App competes structurally with Salesforce's own Agentforce-in-Slack strategy.
- **AWS**: Genie Code + Lakeflow directly challenges Glue + SageMaker as the integrated data+ML pipeline. Lakebase challenges RDS-to-Redshift architectures. Databricks' multi-cloud GA pace (Azure 14 regions, AWS existing) forces AWS to accelerate native Spark/Iceberg feature parity.
- **Palantir / enterprise AI platforms**: Genie Ontology's continuously-learning enterprise knowledge graph is a direct alternative to Palantir's AIP ontology model.

## Build-vs-buy signal

- **Genie (all tiers)**: No seat license. $10/user/month free; consumption billing beyond that. Lowers barrier for wide org rollout — cost risk moves to heavy usage, not head count.
- **Lakeflow Connect Free Tier**: 100 DBUs/day/workspace free for ingestion. Meaningful for mid-market; not a cost driver for enterprise-scale pipelines.
- **Genie ZeroOps / Genie App Builder**: Private preview only — no public pricing. Expect premium SKU or DBU-consumption model consistent with Genie.
- **OpenSharing**: Open source under Linux Foundation — no Databricks licensing cost; operational costs remain.
- **Lakebase**: GA on Azure, 14 regions. Pricing not broken out in summit materials; billed as part of Databricks platform (DBU-based). High-availability multi-node and autoscaling are separate availability tiers within the product.
- **Deployment**: All products are cloud-hosted SaaS (AWS/Azure/GCP). No on-premises Genie offering mentioned. OpenSharing protocol enables on-prem data *sources* to connect without moving data, but Genie itself requires cloud.

## Source

- `raw/research/weekly-2026-06-17/01-databricks-genie-one-summit-2026.md`
- https://www.databricks.com/blog/introducing-genie-zeroops
- https://www.databricks.com/blog/azure-databricks-lakebase-generally-available
- https://www.databricks.com/company/newsroom/press-releases/databricks-announces-opensharing
- https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange
- https://www.databricks.com/blog/introducing-opensharing-next-evolution-delta-sharing-agentic-era
- https://www.salesforce.com/news/stories/salesforce-databricks-shared-foundation-of-human-agent-work-announcement/
- https://www.databricks.com/blog/lakeflow-new-era-agentic-data-engineering
- https://www.databricks.com/blog/accelerate-business-insights-lakeflow-connect-now-free-tier
- https://www.databricks.com/blog/whats-new-genie-code-data-ai-summit-2026
- https://www.techtimes.com/articles/318450/20260616/databricks-summit-2026-day-2-agentic-ai-catalog-federation-move-lab-enterprise.htm

## Related

[[platforms/databricks]] [[platforms/snowflake]] [[landscape/snowflake-summit-2026-06]] [[landscape/google-cloud-next-2026-day2]]
