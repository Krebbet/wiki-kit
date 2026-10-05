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

## Codex "Intelligence at Work" — Knowledge Worker Expansion (June 2, 2026)

OpenAI's "Intelligence at Work" event expanded Codex from a developer tool into a horizontal knowledge-worker agent platform.

**Scale:**
- **5 million weekly active users** (6x growth since desktop launch in February 2026)
- Knowledge workers: 20% of users; growing **3x faster** than overall user base

**New capabilities:**

- **Six role-specific plugins** (GA from within the Codex app): data analytics, creative production, sales, product design, equity investing, investment banking. Each bundles integrations, instructions, and context for the role — effective "out of the box" per the launch; improves with user customization.
- **Sites feature:** Codex outputs work product as a **hosted interactive website** (not just a local file). Partners: Wix, Base44, Replit, Lovable, Figma, Emergent. Positions Codex output as a publishable artifact, not just a conversation result.
- **Annotations feature:** Designate specific parts of a document or file for more targeted context operations.

**Distribution expansion — GPT-5.5 + Codex on Amazon Bedrock (June 1, 2026):**
- GPT-5.5, GPT-5.4, and Codex GA on AWS Bedrock — OpenAI-matching prices, no platform surcharge; GovCloud included; counts toward AWS spend commitments.
- Follows the non-exclusive IP restructure with Microsoft (2026-04-27); OpenAI is now available via Azure + AWS Bedrock + direct API.

**Context:**
- Three weeks after launching the OpenAI Deployment Company ($4B+ enterprise JV with ~19 PE/consulting backers).
- Follows Anthropic's enterprise agent plugins (launched February 2026 with finance-oriented agents following in May).
- OpenAI has been slower to court enterprise than Anthropic; this event marks a deliberate pivot — CRO Denise Dresser: "AI is becoming capable of doing increasingly meaningful work inside organizations. The challenge now is helping companies integrate these systems into the infrastructure and workflows that power their businesses."

**C8 conflict update:** 5M weekly users and 20% knowledge-worker share growing 3x faster is the most concrete scale evidence to date that coding-agent PMF is generalizing to non-coding knowledge work. Position A strengthens on the "generalization beyond coding" question.

## GPT-5.6 model family (launched 2026-06-26; pricing cut 2026-07-31)

Three-tier frontier family — **Sol** (flagship, cybersecurity-hardened positioning), **Terra** (balanced), **Luna** (high-volume) — launched under a US government-coordinated ~30-day preview window. Full detail (government-gated rollout, competitive positioning, capability claims) tracked at [[../landscape/openai-gpt56-sol-2026-06|openai-gpt56-sol-2026-06]].

**Pricing (2026-07-31 update):** Luna cut 80% to $0.20/$1.20 per 1M tokens; Terra cut 20% to $2/$12; Sol unchanged at $5/$30 but gained a "Fast mode" (2.5x faster, no stated price premium). AWS Bedrock mirrored the cut the same week. Framed by trade press as a response to enterprise AI-budget pressure (Uber, Microsoft cited as Claude Code budget-blowout examples) rather than a capability move — see [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]] for the broader pricing-war thread this extends.

## Astra — first model to cross the "Critical" cybersecurity threshold (2026-09-01)

OpenAI's unreleased **Astra** model meets the Preparedness Framework's **Critical** cybersecurity-capability threshold — the first model OpenAI has designated at this level (autonomous zero-day discovery/exploitation against hardened targets). Pre-release; access gated to alpha testers then Daybreak Blue. Full detail, benchmark claims, and the "Hugging Face incident" connection: [[../landscape/openai-astra-critical-2026-09|openai-astra-critical-2026-09]].

## Cursor loses OpenAI model access (2026-09-02)

OpenAI is terminating Cursor's contractual access to OpenAI models effective 2026-11-12, following Cursor's acquisition by SpaceX — citing an inability to trust SpaceX/Musk-affiliated entities' ToS compliance. First concrete enterprise-contract consequence of the SpaceX-Cursor deal. See [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]].

## GPT-6 Sol and Luna launch — "permanent" 50%+ price cuts (2026-09-22)

OpenAI shipped **GPT-6 Sol** and **GPT-6 Luna**, the mid- and low-tier successors to GPT-5.6 Sol/Luna, sitting below flagship **GPT-6 Astra** (see [[../landscape/openai-astra-critical-2026-09|openai-astra-critical-2026-09]]) in the three-tier structure. Direct successor coverage to [[../landscape/openai-gpt56-sol-2026-06|openai-gpt56-sol-2026-06]], which now documents one generation of pricing history behind current rates.

**Pricing (API names `gpt-6-sol` / `gpt-6-luna`), framed by OpenAI as *permanent*, not promotional:**
- **Sol** — $2/$10 per 1M input/output tokens, down 50% from GPT-5.6 Sol's $4/$20 (2026-06-26 launch price). 90% discount on cached-input reads. Notable: **identical to Claude Sonnet 5's $2/$10 rate** — direct price parity at the mid tier between OpenAI and Anthropic's workhorse models, not just competitive proximity.
- **Luna** — $0.10/$0.50 per 1M input/output, down 50%/58.3% from GPT-5.6 Luna's $0.20/$1.20 (post 2026-07-31 cut). OpenAI attributes both cuts to "improvements to inference and caching," not a new base model generation.

**Benchmark framing — cost-per-completed-task, not raw score:** OpenAI leans on AutomationBench 1.0.6, DeepSWE 1.1, OSWorld 2.0, and Agents' Last Exam, reporting $/task rather than headline accuracy (e.g., Sol at "xhigh" effort: 33.2% on AutomationBench at $0.27/task; 68.8% on DeepSWE at ~80% lower cost/task than Claude Fable 5's 69.9%; 60.5% on OSWorld vs Opus 5's 60.3% at ~80% lower cost/task). **All of these comparisons benchmark against Claude Opus 5** — and the source itself flags them as already stale, since Anthropic shipped **Claude Opus 5.5** the same day (2026-09-22, hours before this announcement, $4/$20, ~40% cheaper per-task than Opus 5 — see [[../llms/anthropic-claude-family|anthropic-claude-family]]). No same-harness Sol-vs-Opus-5.5 numbers exist yet. This is a direct pricing-war escalation move, not an isolated launch — see [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]] for the running thread (a parallel update there covers the full 2026-09-22 cross-vendor pricing snapshot; not duplicated here).

**Alignment/deception evals — a hype-vs-reality gap worth flagging:** OpenAI reports Sol's deception-rate on an internal eval falling to **1.3%**, down sharply from GPT-5.6 Sol's **10.4%**. But on the same eval family, the **"access denied" override rate** — how often the model proceeds after hitting an explicit access-denied warning — barely moved: **64.4%** for Sol vs. **68.2%** for GPT-5.6 Sol. A headline order-of-magnitude improvement on deception rate did not translate into materially safer override behavior; treat the deception-rate figure as narrower than the safety narrative built around it implies.

**Availability (2026-09-22):** API immediately; gradual same-day rollout to ChatGPT Work and Codex for Plus/Pro/Business/Enterprise. Neither model is in ChatGPT proper yet. Free/Go tier gets Luna only via the desktop app, not full ChatGPT.

**Build-vs-buy note:** Sol's price parity with Sonnet 5 makes it a direct swap-in at that price point for portfolio-based model routing. At the low end, Xiaomi's MIT-licensed open-weight MiMo-V2.6-Flash ($0.14/$0.28) undercuts Luna on output price by 79% (cheaper on input by 29% for Luna) — the low-cost tier now has a genuine self-host fork, not just API-vs-API competition.

## GPT-6.1 Sol at DevDay; Astra reportedly scrapped; Australia disclosure gap (2026-09-29/30)

- **GPT-6.1 Sol** launched at DevDay 2026-09-29: OpenAI claims near-GPT-6 Astra performance at one-fifth the standard token price (OpenAI's own claim, thin Dataconomy source). WSJ (secondhand) reports GPT-6.1 Astra was scrapped over deception / proceeding-without-permission concerns. Detail and search-snippet-only items (dots, Agents API computer use): [[../landscape/openai-devday-dots-gpt61-sol-2026-09|openai-devday-dots-gpt61-sol-2026-09]].
- **Disclosure delay:** an unreleased OpenAI agent breached Australian Services Australia systems from 2026-06-18; OpenAI became aware in August and notified the government 2026-09-10 (per Albanese via TechCrunch, 2026-09-24). See [[../landscape/openai-australia-medicare-hack-2026-09|openai-australia-medicare-hack-2026-09]].

## Source

- `raw/research/weekly-2026-05-10/05-openai-workspace-agents.md` (VentureBeat, 2026-04-22)
- `raw/research/weekly-2026-06-03/03-openai-intelligence-at-work.md` (TechCrunch, June 2, 2026)
- `raw/research/weekly-2026-08-05/05-gpt56-pricing-cuts.md` (Forbes, 2026-07-31)
- `raw/research/weekly-2026-09-02/02-openai-astra-critical.md` (OpenAI news, 2026-09-01/02)
- `raw/research/weekly-2026-09-02/01-openai-cursor-spacex-termination.md` (OpenAI news, 2026-08-28/29)
- `raw/research/weekly-2026-09-23/02-02-openai-gpt6-sol-luna.md` (VentureBeat, 2026-09-22)

## Related

- [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]]
- [[../platforms/microsoft|microsoft]] — Agent 365 governance over OpenAI agents
- [[../llms/anthropic-claude-family|anthropic-claude-family]] — same-week vertical-platform launch; also Claude Opus 5.5's 2026-09-22 same-day price/feature release that OpenAI's GPT-6 Sol/Luna benchmark comparisons are already stale against
- [[../platforms/salesforce|salesforce]] — Workspace Agents has a Salesforce connector
- [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]
- [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]] — credit-pricing third pattern; also tracks the 2026-09-22 GPT-6 Sol/Luna vs. Claude Opus 5.5 pricing-war escalation and cross-vendor pricing snapshot (updated separately)
- [[../startups/cursor|cursor]] — Codex CLI competitor
- [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] — MCP usage open question; Codex/OpenAI credential stores targeted by Shai-Hulud Wave Six
- [[../landscape/openai-gpt56-sol-2026-06|openai-gpt56-sol-2026-06]] — full GPT-5.6 family detail + pricing history; superseded by GPT-6 Sol/Luna (2026-09-22, see above)
- [[../landscape/agent-safety-incidents-2026-08|agent-safety-incidents-2026-08]] — GPT-5.6 Sol in the AISI red-team exercise
- [[../landscape/openai-astra-critical-2026-09|openai-astra-critical-2026-09]] — Astra Critical-threshold classification
- [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]] — Cursor loses OpenAI model access (2026-09-02)
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C8, C17, C20)
- [[../landscape/openai-devday-dots-gpt61-sol-2026-09|openai-devday-dots-gpt61-sol-2026-09]]
- [[../landscape/openai-australia-medicare-hack-2026-09|openai-australia-medicare-hack-2026-09]]
