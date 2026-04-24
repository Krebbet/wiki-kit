# Google Cloud Next 2026 — Day 2 (Gemini Enterprise Agent Platform)

On **2026-04-22**, Google Cloud relaunched Vertex AI as the **Gemini Enterprise Agent Platform (GEAP)** — a unified build / scale / govern / optimize stack for enterprise agents, 200+ models via Model Garden, cryptographic agent identity, persistent Memory Bank, and "all future Vertex AI services and roadmap will be delivered exclusively through Agent Platform." The announcement lands the day after the $750M agentic partner fund (see [[google-cloud-agentic-partner-fund-2026-04]]) — channel plus product in one strategic arc.

## What GEAP is

**Vertex AI end-of-standalone.** GEAP is not additive — it's a forced migration. Enterprises mid-build on Vertex AI need to evaluate GEAP compatibility timelines; "delivered exclusively through Agent Platform" language is unusually strong for a Day-2 keynote.

Four layers:

### Build
- **Agent Studio** — low-code builder; exports to ADK when low-code ceilings out.
- **Agent Development Kit (ADK)** — code-first graph-based multi-agent framework. Google-stated: >6T tokens/month on Gemini models. MCP integration called out explicitly (L'Oréal quote: "through Model Context Protocol, they are securely connected to our single sources of truth").
- **Agent Garden** — template library (code modernization, financial analysis, invoice processing, etc.).

### Scale
- **Agent Runtime** — managed execution. Vendor claims: sub-second cold starts, provision in seconds, long-running agents "days at a time." Runtime differentiator vs session-scoped alternatives is the multi-day persistence claim (unverified).
- **Agent Memory Bank** — dynamically generates and curates long-term memories; Memory Profiles as a tunable object distinct from raw conversation logs. Gurunavi claims +30% satisfaction, Payhawk claims >50% expense-submission time reduction (both co-marketed).
- **Agent Sessions** — Custom Session IDs map agent sessions to internal CRM/DB identifiers.

### Govern
- **Agent Identity** — cryptographic ID per agent, mapped to authorization policies; auditable action trail.
- **Agent Registry** — central index of approved agents, tools, skills.
- **Agent Gateway** — unified connectivity between agents and tools across environments; enforces security + Model Armor (prompt-injection / data-leakage protection).
- **Agent Anomaly Detection + Security Command Center integration** — LLM-as-a-judge plus statistical models.

### Optimize
- **Agent Simulation** — synthetic interactions and virtualized tools; auto-scored on task success and safety.
- **Agent Evaluation** — live-traffic scoring via multi-turn autoraters.
- **Agent Observability** — visual trace of reasoning.
- **Agent Optimizer** — automatic failure clustering with refined system-instruction suggestions. The most novel claim — LLM-in-the-loop on its own failure modes; watch for independent reproduction.

### Other

- **Agent Sandbox / Workspaces** — hardened sandboxed environment for bash, file management, model-generated code, and browser-based computer use.
- **Model Garden** — 200+ models: Gemini 3.1 Pro, Gemini 3.1 Flash Image, Lyria 3, Gemma 4 (open), Anthropic Claude Opus/Sonnet/Haiku, and third-party. Gemini 3.x series is current as of 2026-04-23.
- **Agent Payment Protocol (AP2)** — named once (PayPal quote) as "foundation for trusted agent payments." Indeterminate: novel protocol or renamed API.

## Named production deployments (2026-04-22, vendor co-marketed)

| Customer | Use case |
|---|---|
| Comcast | Xfinity Assistant on Agent Runtime |
| Color Health | Cancer-screening scheduling agent |
| PayPal | Agent-based payments via AP2 |
| L'Oréal | Multi-LLM orchestration via ADK + MCP |
| Geotab | Multi-framework orchestration under governable production path |
| Burns & McDonnell | ADK deployments |
| Gurunavi ("UMAME!") | Memory Bank personalization |
| Payhawk | Memory Bank habit-based expense auto-submit |

All quotes are vendor-curated. No failure rates, pricing, or error budgets disclosed.

## Hype-vs-reality

- "Move from managing individual AI tasks to delegating business outcomes with total confidence" — marketing prose.
- "Sub-second cold starts" + "provision new agents in seconds" + "long-running days at a time" — strong performance claims, no methodology.
- "200+ models" — includes tail / experimental; the operationally important access is Gemini 3.1 Pro, Claude Opus/Sonnet/Haiku, Gemma 4.
- Customer quotes describe real production workloads but are curated — no independent practitioner validation in-source.

## Why this matters — build-vs-buy

- **Agent governance primitives** (Identity, Registry, Gateway, Anomaly Detection) are high-effort to build correctly. Buy for GCP-committed orgs; the control-plane tier is moving to hyperscaler table stakes.
- **Memory Bank lock-in risk.** Once agent memory is stored in Google's system, migration costs rise. No export/migration API indicated. Evaluate portability before committing.
- **ADK portability.** Free to use; export/hybrid path with non-Google hosting is viable. Lock-in is in Agent Runtime, not ADK itself.
- **Model Garden as procurement pattern.** L'Oréal explicitly names "multi-LLM flexibility" as a buying criterion for GCP. Multi-model access via a single CSP relationship is a live enterprise preference. Anthropic Claude available through GCP (alongside AWS Bedrock + Anthropic direct) confirms labs distributing through all channels simultaneously.

## Competitive frame — hyperscaler convergence on the control plane

Google GEAP's **Agent Identity + Registry + Gateway** is structurally identical to **Salesforce Agent Fabric** (shipped 2026-04-15; see [[../platforms/salesforce|salesforce]]). Two independent vendors converging on the same governance-layer pattern within 8 days upgrades the trend from "one vendor" to "emerging norm." See [[../conflicts/open-questions-2026-04|C17]] update.

Same week, Snowflake shipped MCP connectors + ACP support + IDE plugins (see [[../platforms/snowflake|snowflake]]) — three platform incumbents, one pattern.

## Strategic read

This is Google's full-court press to make GCP the runtime and governance layer for enterprise agents *regardless of which model you use*. Combined with the $750M partner fund ([[google-cloud-agentic-partner-fund-2026-04]]), the play is: subsidize the GSIs to get clients onto GEAP, lock them to Memory Bank and the governance primitives, monetize whichever model they pick (Gemini preferred; Claude via Model Garden; Gemma if self-hosted). A direct counter to the Salesforce Headless-360 + Agent-Fabric posture and to Microsoft Copilot Studio.

## Source

- `raw/research/weekly-2026-04-23/01-google-cloud-next-2026-day2.md` (Google Cloud Blog, 2026-04-22)

## Related

- [[google-cloud-agentic-partner-fund-2026-04]]
- [[../platforms/salesforce|salesforce]]
- [[../platforms/snowflake|snowflake]]
- [[llm-api-enterprise-share]]
- [[ai-infrastructure-frontiers-2026]]
- [[ai-app-categories-2025]]
- [[../thesis/agents-eating-saas|agents-eating-saas]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C3, C17, C18)
