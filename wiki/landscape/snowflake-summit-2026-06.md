# Snowflake Summit 2026 — CoWork, Natoma MCP Acquisition, Cortex Training

At Snowflake Summit 26 (San Francisco, June 2–5, 2026), Snowflake announced a cluster of AI-agent platform moves: CoWork (rebranded from Snowflake Intelligence) expanded into a knowledge-worker personal agent with MCP connectors and multi-agent orchestration; the company announced intent to acquire Natoma (enterprise MCP gateway); and Cortex Training was introduced to enable customers to fine-tune open-weight models inside Snowflake's governed environment. Taken together, these position Snowflake as an "agent control plane" atop the AI Data Cloud, competing with Salesforce Agentforce, Microsoft Copilot Studio, and Google Agentspace for the enterprise knowledge-worker agent surface.

## CoWork (formerly Snowflake Intelligence)

**Renamed** from Snowflake Intelligence to CoWork at Summit 26. Positioned as "the personal agent for knowledge workers."

**Key features announced (GA/preview status marked):**

- **MCP connectors (GA):** Google Drive, Salesforce, Slack — CoWork can read/write across these systems. Built on Natoma acquisition intent (see below).
- **Artifacts with publishable dashboards (GA soon):** analysts create interactive, governed dashboards that knowledge workers query in natural language — "from dashboards to decisions."
- **Deep Research:** multi-step reasoning across all structured + unstructured enterprise data; agent-swarm orchestration (Snowflake AI Research). Benchmarked against Snowflake's own Hybrid Deep Research Benchmark — "outperforming single-agent systems by over a third."
- **Cortex Sense:** automatically aggregates enterprise data, business definitions, and operational knowledge into a shared context layer used by both CoWork and CoCo (coding agent). Prebuilt role-specific plugins (finance, sales) for day-one deployment.
- **User Skills + Skill Catalog:** automate personal workflows; share/reuse across org.
- **User Memory (preview soon):** learns from individual behavior; scheduled task delivery via Gmail/Slack.
- **CoWork iOS mobile app (GA soon):** take action on data from mobile; CoWork Slackbot and Microsoft Excel Extension in private preview.

**Named customers:** Synopsys (20+ purpose-built agents across RevOps/legal/finance/PM/IT); WHOOP; Under Armour.

**Model choice:** Anthropic, OpenAI, Google, Meta, Mistral, DeepSeek, SpaceXAI — all available via Cortex AI. Snowflake does not lock customers to a single provider.

## Natoma Acquisition (Intent Announced)

Snowflake announced intent to acquire **Natoma** — an enterprise MCP (Model Context Protocol) gateway that manages AI agent permissions across enterprise apps at the tool-call level.

- **What Natoma provides:** secure connectivity, governance, identity-aware authorization, and auditability for AI agents operating across enterprise systems.
- **Why it matters:** Rather than building bespoke connectors per tool, Natoma intercepts MCP tool calls and enforces enterprise-wide permissions — a control-plane primitive that sits above individual MCP server implementations.
- **Conflict read-through:** This is a **Position A follow-through for C17** (MCP-fluency-with-isolation). Natoma's model is exactly the architecture Position A predicted: MCP adoption combined with a governance/isolation layer. Adds a fifth named enterprise incumbent choosing MCP-first (alongside SAP+Anthropic, ServiceNow AI Control Tower, Lyrie ATP, Microsoft Copilot Studio MCP connectors). See [[mcp-rce-supply-chain-2026-05]].
- **Competitor framing:** The governance layer competes with ServiceNow Traceloop-integrated AI Control Tower and Lyrie's Agent Trust Protocol (ATP). All three emerging simultaneously in Q2 2026.

## Cortex Training

Fine-tuning of open-weight models (Qwen, Mistral families) **inside Snowflake's governed environment**, using managed GPUs — no external data movement.

- **Customer example:** Resolve AI committed multi-million-dollar 2-year deal to train production-operations-specific RL models on Cortex Training. Uses simulated environments + evaluation workflows to build domain-specific models that outperform general-purpose APIs on production-ops reasoning tasks.
- **Economics claim:** "Up to 2x more training runs for the same GPU budget" vs external fine-tuning platforms.
- **Fit:** Directly targets the C2 conflict (enterprise fine-tuning in decline) — Cortex Training lowers the barrier to domain-specific model specialization within an existing governed data stack. Watch whether this reverses the a16z "fading fine-tuning" observation.

## Competitive Positioning

| Dimension | Snowflake CoWork | Microsoft Copilot Studio | Salesforce Agentforce | Google Gemini Spark |
|---|---|---|---|---|
| Knowledge-worker agent | Yes (CoWork) | Yes (Copilot Chat) | Agentforce for Slack | Yes (Gemini Spark) |
| Data substrate lock-in | Snowflake data cloud | Microsoft Graph | Salesforce CRM | Google Workspace |
| MCP-first | Yes (Natoma acquisition) | Yes (connectors) | Agent Fabric | Partial |
| Model choice | Multi-vendor | Multi-vendor (Claude/OpenAI CUA) | Single (Salesforce-controlled) | Gemini-first, extensible |
| Fine-tuning on-premises | Cortex Training | None | None | None |
| Agent governance | Natoma (acquiring) | Purview + AI Control Tower overlay | Agent Fabric | Managed Agents API |

## Source

- Snowflake press release (Snowflake Summit 26, June 2, 2026): `raw/research/weekly-2026-06-03/02-snowflake-summit-2026.md`
- Captured: 2026-06-03

## Related

- [[mcp-rce-supply-chain-2026-05]] — C17; Natoma is Position A follow-through (MCP+governance-layer)
- [[platforms/snowflake]] — Snowflake platform profile; CoWork extends prior Intelligence section
- [[platforms/salesforce]] — Agentforce; direct CoWork competitor
- [[platforms/microsoft]] — Copilot Studio; direct competitor
- [[landscape/google-io-2026-enterprise]] — Gemini Spark; direct competitor
- [[landscape/agentcore-payments-x402-2026-05]] — AWS agent control-plane; parallel stack
- [[conflicts/open-questions-2026-04]] — C17 (MCP-fluency-with-isolation), C2 (enterprise fine-tuning)
