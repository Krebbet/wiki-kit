# OpenAI Model + Platform Family

Running page for OpenAI's model and product portfolio — frontier models (GPT-5.x), enterprise platform (ChatGPT Enterprise + Workspace Agents), developer surface (Codex CLI + Codex Cloud), agent-builder stack (AgentKit → Frontier → Workspace Agents), and adjacent products (Sora, Operator). Updated as ingestion surfaces concrete material. For the Microsoft partnership context see [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]]; for enterprise share + spend see [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]].

## Distribution surfaces (2026-05-10 snapshot)

- **Direct API** — primary developer surface; ChatGPT Enterprise platform.
- **Azure** — primary cloud, first-launch venue (preserved through 2030 per the 2026-04-27 amended Microsoft partnership).
- **AWS Bedrock** — limited preview from 2026-04-28; GA "within weeks." First time OpenAI flagship reasoning models available outside Azure / OpenAI direct API.
- **Strategic non-exclusivity (post 2026-04-27):** OpenAI can serve products to customers across any cloud provider; IP license to Microsoft remains through 2032 but is non-exclusive.

## Workspace Agents (ChatGPT Enterprise, launched 2026-04-22)

**One-line:** Codex-powered cloud agents that plug into Slack, Google Drive, Microsoft apps, Salesforce, Notion, Atlassian Rovo, and 90+ other connectors. Successor to Custom GPTs for organisations (individual GPTs continue indefinitely). Free trial through **2026-05-06**, then credit-based pricing.

### Capabilities

- Code execution + tool use + connected-app actions in a single agent loop.
- Persistent memory across runs.
- Scheduling / wake-up for long-running multi-step workflows.
- Background computer use.
- **Two auth modes:**
  - End-user account (agent uses caller's credentials).
  - Agent-owned account (shared service account).
- **Write actions default to "Always ask"** (human-in-the-loop); builders can relax to "Never ask" or define a custom approval policy.
- **Team-level "Agents tab"** in ChatGPT sidebar — shared workspace directory of reusable agents.

### Named first-party templates

- **Spark** — lead qualification.
- **Slate** — software-request review.
- **Tally** — metrics reporting.
- **Scout** — product feedback routing.
- **Trove** — vendor risk.
- **Angle** — marketing / web content.

### Connectors

90+ at launch including Atlassian Rovo, CircleCI, GitLab, Microsoft Suite, Neon by Databricks, Render, Slack, Salesforce, Notion, Google Drive.

**MCP status:** not confirmed in launch materials. Whether Workspace Agents use MCP or a proprietary connector protocol is an open question — relevant in light of [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] (Anthropic declined to fix the MCP STDIO RCE; alternative protocols become competitively positioned).

### Pricing

- Free trial through **2026-05-06**.
- **Credit-based pricing** from 2026-05-06 onward; specific rates not disclosed in launch coverage.
- Sits on top of existing ChatGPT Business ($20/user/month) / Enterprise / Edu / Teachers seat costs.
- **Third pricing pattern** in the agentic-compute landscape (alongside flat-Pro+ subscriptions and burst-API metering — see [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]).

### Hard limits

- **Off by default at launch** for ChatGPT Enterprise pending admin enablement.
- **Not available** to Enterprise customers using Enterprise Key Management (EKM) — material blocker for security-sensitive enterprises.
- Admin console for fleet view of all agents with usage patterns is "coming soon" — not live at launch (mockup-only in launch materials).
- Per-agent throttles, fleet caps, tool budgets not disclosed.

### Named early testers (launch coverage 2026-04-22)

- **Rippling** — AI Engineering lead Ankur Bhatt cited; sales consultant built a sales agent without engineering ("5–6 hours/week now runs automatically").
- **SoftBank Corp.**
- **Better Mortgage**
- **BBVA**
- **Hibob**

### Hype-vs-reality

- Custom GPTs (introduced late 2023) were widely considered weak; Workspace Agents is OpenAI's **second swing** at admin-built agent surface.
- Custom GPT deprecation for organisations is announced — date TBD; individual Custom GPTs continue.
- Prompt-injection safeguards claimed but "not yet proven in the wild" (VentureBeat caveat in launch coverage).
- Direct competitive framing in launch materials: against [[../platforms/microsoft|Microsoft Copilot Studio]], Google Agentspace, [[../platforms/salesforce|Salesforce Agentforce]], and Anthropic Claude Managed Agents (see [[../llms/anthropic-claude-family|anthropic-claude-family]]).

## Codex Cloud + Codex CLI (the harness substrate)

Workspace Agents' runtime is Codex cloud-hosted. The OpenAI coding-agent stack now has two surfaces:

- **Codex Cloud** — the cloud-hosted harness underlying Workspace Agents and other ChatGPT Enterprise agents. Code execution substrate (vs pure LLM call-and-response) — enables real CSV transforms, chart generation, system reconciliation.
- **Codex CLI** — local developer surface. Comparable category to [[../startups/cursor|Cursor]] and Anthropic Claude Code. May 2026 release notes: persisted `/goal` workflows, MultiAgentV2 (per scout report).

The cloud-vs-local split parallels the Cursor 3.2 + Claude Code architecture (see [[../startups/cursor|cursor]]).

## OpenAI's enterprise agent stack — 12-month build-out

Workspace Agents sits atop a layered platform OpenAI has been assembling for 12 months. OpenAI does not explicitly describe this architectural relationship in launch materials, but the layering is visible:

| Layer | When | What |
|---|---|---|
| Foundation | (existing) | GPT-5.x family, ChatGPT Enterprise, direct API |
| AgentKit | Oct 2025 | Developer-facing drag-and-drop agent builder + Connector Registry + ChatKit |
| **Frontier** | Feb 2026 | Enterprise agent management platform — shared business context, execution environments, evaluation, permissions |
| **Workspace Agents** | Apr 2026 | No-code, in-product entry point for admins on top of Frontier; ships in ChatGPT Enterprise |

Each layer is a **higher-margin, stickier surface** moving enterprise spend up the value chain from foundation-model API → agent platform.

## Strategic timing — three-way enterprise-agent-platform launch (2026-04-22 → 2026-05-03)

OpenAI Workspace Agents launches in the same 11-day window as **two competing enterprise-agent platform plays**:

| Date | Vendor | Launch | Positioning |
|---|---|---|---|
| 2026-04-22 | OpenAI | Workspace Agents | Horizontal admin-builder; Codex cloud runtime |
| 2026-05-01 | Microsoft | Agent 365 GA | Multi-vendor governance / control plane (incl. OpenAI agents) |
| 2026-05-03 | Anthropic | Claude Finance Agents | Vertical platform (financial services); Excel/PowerPoint/Word add-ins |

This same-week parallelism is **trend-defining** — see this week's brief for the synthesis. All three vendors moving up the stack from foundation-model API to enterprise platform within the same 11 days.

## Build-vs-buy signals

- **ChatGPT-Enterprise-anchored shops:** buy is the natural path given Workspace Agents' no-code entry point.
- **Multi-vendor shops:** Workspace Agents is the OpenAI play in the 3-way race against Anthropic vertical platforms (Finance Agents) and Microsoft governance (Agent 365).
- **Lock-in surface:** OpenAI-account-bound agent state + connector entitlements + Codex cloud runtime.
- **EKM blocker:** EKM Enterprise customers excluded at launch — material blocker for security-sensitive enterprises (financial services, regulated healthcare). Track for resolution.
- **Pricing risk:** credit-based pricing model (post 2026-05-06) creates a separate cost-centre line above seat cost; finance teams need to model agent-credit consumption distinctly.

## Techniques worth stealing

- **Cloud-Codex-as-runtime** pattern — code execution substrate vs pure LLM loop.
- **Admin-policy-gated connector model** with role-level publish controls.
- **Credit pricing for agent-as-cost-centre** accounting separate from seat cost.
- **Shared workspace agent directory** (team-reuse pattern vs individual Custom GPTs).
- **Two-mode auth** (end-user creds vs agent-owned service account) — clean primitive for governing what an agent can do under whose authority.

## Conflict-flag cross-refs

- **C8** (autonomous-agent generalisation beyond coding) — Workspace Agents claim is admin-builder for non-coding work (lead qualification, vendor risk, marketing); evidence value depends on actual production usage data, which is not yet available outside named early testers.
- **C17** (MCP-fluency-with-isolation) — OpenAI's connector framework is an open question for MCP usage; if Workspace Agents uses a proprietary connector protocol, OpenAI is competitively differentiated against the MCP RCE surface (see [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]]).
- **C20** (Microsoft IP-exclusivity end) — Workspace Agents launches in the same window OpenAI gets multi-CSP distribution; the diversification the [[../landscape/openai-microsoft-restructure-2026-04|2026-04-27 restructure]] was strategic-prep for is now operational.

## Source

- `raw/research/weekly-2026-05-10/05-openai-workspace-agents.md` (VentureBeat, 2026-04-22)

## Related

- [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]]
- [[../platforms/microsoft|microsoft]] — Agent 365 governance over OpenAI agents
- [[../llms/anthropic-claude-family|anthropic-claude-family]] — same-week vertical-platform launch
- [[../platforms/salesforce|salesforce]] — Workspace Agents has a Salesforce connector
- [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]
- [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]] — credit-pricing third pattern
- [[../startups/cursor|cursor]] — Codex CLI competitor
- [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] — MCP usage open question
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C8, C17, C20)
