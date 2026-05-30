# Microsoft

Microsoft platform profile — covering the agent-control-plane (Microsoft Agent 365), productivity-AI surface (Microsoft 365 Copilot), agent-builder (Copilot Studio + Azure AI Foundry), and agentic-compute substrate (Windows 365 for Agents). Microsoft's enterprise AI play is now bundled around **seat-based monetisation**: governance ships in M365 E7 or as a $15/user/month standalone, not per-agent. As of the **2026-04-27 Microsoft–OpenAI restructure** (see [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]]), Microsoft has positioned itself to govern multi-vendor agent estates including non-exclusive OpenAI agents, Anthropic finance agents distributing inside M365, local agents (OpenClaw, Claude Code), and partner-built agents from the SDC ecosystem.

## Microsoft Agent 365 — agent control plane (GA 2026-05-01)

**One-line:** Enterprise agent governance platform that discovers, observes, governs, and secures AI agents — both delegated-access (on behalf of users) and own-access (autonomous) — across Microsoft and non-Microsoft cloud estates. Bundled in M365 E7 SKU; standalone at **USD 15/user/month**. Per-user license, not per-agent.

### Named GA capabilities (2026-05-01)

| Capability | Status at GA |
|---|---|
| Agents working on behalf of users (delegated access) | GA |
| Agents operating behind the scenes (own access) | GA |
| Microsoft Entra network controls extended to Copilot Studio + local agents (e.g., OpenClaw) | GA |
| Agents participating in team workflows (own access) | Public Preview |
| Shadow-AI discovery via Microsoft Defender + Intune (local + cloud agents) | Frontier preview at GA; broader public preview June 2026 |
| Agent 365 registry sync with **AWS Bedrock** and **Google Cloud** | Public Preview (2026-05-01) |
| Windows 365 for Agents (secured managed Cloud PC for agentic workloads) | Public Preview, US only |
| Context mapping (devices, MCP servers, identities, cloud resources per agent) | Public Preview June 2026 |
| Policy-based controls + runtime blocking via Intune/Defender | Public Preview June 2026 |

### Techniques under the hood

- **Microsoft Defender** for shadow-AI discovery + runtime behavioural blocking
- **Microsoft Intune** for endpoint policy enforcement (e.g., block OpenClaw on managed devices)
- **Microsoft Entra** for identity / credentials governance + network controls (agent traffic inspection at the network layer)
- **Microsoft Purview** implied (compliance / audit-ready evidence via partner services language)
- **MCP integration:** Defender context mapping explicitly surfaces "MCP servers configured for those agents" (June 2026 preview) — see also [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] for why this matters as a governance surface
- **Agent 365 registry** as a unified inventory layer, syncing across AWS Bedrock and Google Cloud

### Pricing model (the load-bearing fact)

- **USD 15/user/month** standalone, OR bundled in **M365 E7** (E7 list price not given in source).
- License is per "individual who manages or sponsors agents, or uses agents to do work on their behalf" — **not per agent**.
- Governance monetised via seat-based E7 upgrade. For Microsoft-shop enterprises, this is effectively cost-neutral relative to building governance infrastructure.

### Hard limits at GA

- Shadow-AI discovery for local agents currently limited to OpenClaw (GitHub Copilot CLI and Claude Code "expanding soon").
- Windows 365 for Agents public preview is US only.
- AWS Bedrock + Google Cloud registry sync is preview, not GA.
- Context mapping, policy-based controls, runtime blocking are June 2026 public preview.
- Frontier program (early access) required for some shadow-AI discovery at GA.

### Named customers / partners (2026-05-01)

- **NTT DATA Group Corporation** (Yuji Shono, Head of Global AI Office) — sole quoted customer endorsing scale/governance.
- **SDC launch partners:** Adobe, NVIDIA, Zendesk, n8n, Kore.ai, Celonis, Genspark, Zensai, Egnyte, Kasisto.
- **SI/services partners:** Accenture, KPMG, Cognizant, Capgemini, Avanade, Deloitte, EY, PwC, TCS, Bechtle, Insight, Protiviti, Slalom.

### Hype-vs-reality (2026-05-01)

Microsoft frames Agent 365 as "control plane for all enterprise AI" including non-Microsoft agents. **Reality at GA:** AWS/Google cloud registry sync is preview; local agent discovery limited to OpenClaw; runtime blocking is June 2026 preview. Cross-platform governance is partially real today (Entra network controls, registry for Microsoft-native estate) and partially roadmap.

### Strategic timing

GA 2026-05-01 — **two days before Anthropic launched Claude Finance Agents inside M365** (2026-05-03 add-ins for Excel/PowerPoint/Word per Anthropic news; see [[../llms/anthropic-claude-family|anthropic-claude-family]]). The same Microsoft-owned governance layer is positioned to govern competing-vendor agents running on Microsoft infrastructure. Combined with:

- **Microsoft–OpenAI restructure (2026-04-27)** — OpenAI now non-exclusive; OpenAI Workspace Agents (2026-04-22 launch in ChatGPT Enterprise; see [[../llms/openai|openai]]) is one of the agent classes Agent 365 is designed to govern when those agents touch the Microsoft estate.
- **Anthropic finance agents inside M365** — Anthropic distributing Excel/PowerPoint/Word add-ins under Microsoft governance substrate.

…Microsoft has consolidated a position as the **multi-vendor agent governance default for the M365 estate** within an 11-day window (2026-04-27 → 2026-05-08).

## Microsoft 365 Copilot — productivity AI

Not the focus of this run. Tracked secondarily; under pricing pressure from Anthropic's M365 add-ins. Watch whether Microsoft 365 Copilot ships meaningful non-OpenAI model integration in 2026-Q3 — that's the resolution path for [[../conflicts/open-questions-2026-04|C20]] (Microsoft IP-exclusivity end: long-tail monetisation or accelerating substitution).

## Copilot Studio + Azure AI Foundry — agent builder

Not deeply ingested in this run. Copilot Studio is the no-code agent builder; Azure AI Foundry is the developer surface (model catalogue, agent runtime, evaluation). Both sit under Agent 365 governance per the GA announcement.

## Windows 365 for Agents — agentic compute substrate

Public preview at GA, US only. Secured managed Cloud PC environment for agentic workloads — Microsoft's answer to "where do you run a long-lived agent that needs OS / browser / file-system access." Track for cross-region availability + GA timing.

## Build-vs-buy signals

- **Microsoft-shop enterprises:** effectively buy. E7 upgrade (or USD 15/seat for governance alone) is cheap relative to building governance infrastructure; existing Intune/Defender/Entra investment is the moat.
- **Non-Microsoft shops:** governance must come from elsewhere — [[salesforce|Salesforce Agent Fabric]], ServiceNow AI Control Tower, or [[../landscape/google-cloud-next-2026-day2|GEAP Agent Gateway]]. Agent 365 is architecturally Microsoft-tilted; cross-platform registry sync is preview and may remain shallow.
- **Three-way enterprise-agent-platform race:** Microsoft owns governance (Agent 365), Anthropic owns vertical platforms ([[../llms/anthropic-claude-family|Claude Finance Agents]]), OpenAI owns admin-builder ([[../llms/openai|OpenAI Workspace Agents]]). All three GA / launched within the same 11-day window (2026-04-22 → 2026-05-03).

## Techniques worth stealing

- Bundling agent governance into existing seat-based SKU (E7) rather than per-agent pricing — adoption cost is near-zero for existing E7 customers.
- Using existing IDP (Entra) and endpoint management (Intune/Defender) as governance substrate rather than introducing net-new tooling.
- **Registry-as-inventory** pattern: unified agent registry syncing across clouds as the foundation for governance.
- **MCP server asset mapping** as a discovery vector for agent exposure analysis (load-bearing in light of [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]]).

## Conflict-flag cross-refs

- **C17** — MCP-as-platform-fluency: Agent 365's MCP-server context mapping (June 2026 preview) is the cleanest example of MCP-isolation-via-vendor-governance, the new Position B from [[../landscape/mcp-rce-supply-chain-2026-05|the MCP RCE incident]]. Agent 365 buyers inherit MCP-isolation-as-feature.
- **C20** — Microsoft IP-exclusivity end (long-tail vs substitution): Agent 365 GA confirms the **multi-vendor governance** read — Microsoft monetises governance over the multi-vendor estate it has just unlocked, regardless of which model vendor wins long-term.

## Source

- `raw/research/weekly-2026-05-10/03-microsoft-agent-365-ga.md` (Microsoft Security Blog, 2026-05-01)

## Related

- [[salesforce]] — Agentforce + Agent Fabric (direct competitor, seat-based governance + own IDP substrate)
- [[../landscape/google-cloud-next-2026-day2|google-cloud-next-2026-day2]] — GEAP Agent Gateway (parallel governance, cross-cloud)
- [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]] — Agent 365 governs OpenAI agents post non-exclusivity
- [[../llms/anthropic-claude-family|anthropic-claude-family]] — Claude Finance Agents distribute inside M365 under Agent 365 governance
- [[../llms/openai|openai]] — Workspace Agents launch in same 11-day window
- [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] — Agent 365 MCP isolation context
- [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]] — agent control-plane consolidation
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C17, C20)
