# Salesforce

Enterprise CRM incumbent that in 2026 pivoted from "Salesforce is where humans work" to "Salesforce is the substrate agents build on top of." The canonical **incumbent-becomes-agent-infrastructure** case study. Platform profile; expect multiple product pages to nest under `wiki/platforms/salesforce/` as volume warrants.

**Working read (2026-04-22):** for existing Salesforce customers, the "rip-and-replace with agents" angle is meaningfully reduced — **Headless 360** and **Agent Fabric** turn the existing seat-licence into the agent runtime. For greenfield, new lock-in shape: the 60+ MCP tools and AgentExchange ecosystem are a moat vs building from scratch, but every agent inherits the Salesforce dependency *(synthesis)*.

## Product portfolio (as of 2026-04)

- **Headless 360** (launched 2026-04-15 at TDX 2026) — platform exposed as APIs, MCP tools, CLI commands. See detail below.
- **Agentforce** — pre-existing Salesforce agent platform (tracked in [[ai-app-categories-2025]] horizontal-agent-platforms section).
- **Agentforce Vibes 2.0** — multi-model (Claude Sonnet, GPT-5) with org awareness.
- **Agent Fabric** — multi-vendor agent control plane with deterministic orchestration + centralized governance across non-Salesforce LLMs / agents / tools.
- **AgentExchange** — marketplace; 10,000 Salesforce apps, 2,600+ Slack apps, 1,000+ Agentforce agents / tools / MCP servers from partners (Google, Docusign, Notion, etc.). $50M Builders Fund for partner scale-up.
- **Data 360, Customer 360, Slack** — context / work surfaces that Headless 360 exposes as MCP tools.

## Headless 360 (launched 2026-04-15)

### What it does

Platform exposed as **APIs, MCP tools, and CLI commands** so agents (and humans) can build and operate on Salesforce **without ever opening a browser**. Spans the full breadth of Customer 360 (sales, service, workflows, business logic) plus Data 360 context and Agentforce agent tooling.

### Techniques under the hood (2026-04-15)

- **60+ new MCP tools** giving coding agents live access to data, workflows, and business logic.
- **30+ preconfigured coding skills**.
- **Agentforce Experience Layer** — UI service that renders rich cards / workflows natively in **Slack, Mobile, ChatGPT, Claude, Gemini, Teams, or any MCP-app client**. Build once, render everywhere.
- **DevOps Center MCP** — natural-language CI/CD.
- **Native React** for custom UIs.
- **Agentforce Vibes 2.0** — multi-model with org awareness.
- **Agent lifecycle governance** (the harness tier, in-house):
  - **Testing Center** — pre-launch.
  - **Custom Scoring Evals** — score *decision quality*, not just execution.
  - **Agent Script** — deterministic-vs-reasoning behavior control.
  - **Observability + Session Tracing** — post-launch.
  - **A/B Testing** — on real traffic.
  - **Agent Fabric** — multi-vendor control plane.

### Deployment model

Salesforce core-platform extension; customers already on Salesforce inherit it. **Agents inherit existing permissions, sharing rules, and compliance controls** rather than rebuilding the trust layer — load-bearing claim for enterprise adoption.

### Customization hooks

- Coding skills callable from **Claude Code, Cursor, Codex, Windsurf** (per source).
- Native React for custom front-ends.
- AgentExchange marketplace for third-party agent / tool / MCP-server distribution.
- **$50M Builders Fund** for partner scale-up (announced alongside launch).

### Running costs

Not specified in launch post. Re-check Salesforce pricing pages before quoting. Classic Salesforce per-seat pricing model unchanged in public material.

### Hard limits

Not specified. Agent reliability explicitly framed as "probabilistic, not deterministic … behavior to observe, evaluate, and tune" — implying **governance tooling is load-bearing** and practitioner reports will surface the real limits once they accumulate.

### Market reception (2026-04-15)

- **2.5-year rebuild** timeline disclosed.
- **>100 tools and skills** available immediately.

**Vendor-sourced customer quotes (unverified):**
- Engine (Elia Wallen, CEO): "12 days to production-ready agents, millions in savings."
- Grupo Globo (Adones Guerra, Tech Lead): Vibes for metadata / boilerplate / refactors.
- Indeed (Oliver Bodden, Senior PM): live platform access from existing coding tools with human-in-the-loop gating.

**Partner listing outcomes cited:**
- Notion sales cycle: 4 months → 3 weeks post-listing.
- Docusign: 200+ private offers Q4 2025, 60% faster time-to-signature.
- MeshMesh: first F500 customer six weeks post-listing.

**Slack metric:** custom AI agents on Slack +300% since January 2026.

All outcome numbers are Salesforce-curated launch quotes — **no independent validation yet**. Practitioner reviews will emerge on G2, HN, Reddit over the coming weeks.

### Hype-vs-reality delta

- Vendor launch post; no pricing, no independent customer adoption metrics, no practitioner reviews.
- Four-layer "only Salesforce has all of this" framing (**System of Context / Work / Agency / Engagement**) is classic incumbent-moat marketing — flag for practitioner validation.
- **Agent Fabric multi-vendor governance claim** needs scrutiny: if real, Agent Fabric is a big land-grab for the control-plane tier. If it's Salesforce-agents-only with superficial multi-vendor branding, it's marketing. See [[open-questions-2026-04]] C18.

### Techniques worth stealing

- **The "become-the-infrastructure" pivot** — incumbent SaaS exposing every capability as API / MCP / CLI rather than fighting agents for the UI. Template move for SAP, Oracle, Workday, ServiceNow, HubSpot.
- **Logic / rendering separation** — "what an agent does" (business logic) vs "how it appears" (Experience Layer renders natively per surface). Build once, render everywhere MCP-capable.
- **Lifecycle-governance split**: pre-launch (testing, eval, script) vs post-launch (observability, tracing, A/B). This is a harness-tier pattern and competes directly with the startups in [[ai-infrastructure-frontiers-2026]] §1.
- **Agent Fabric as multi-vendor control plane** — acknowledging enterprises run agents from many vendors and positioning Salesforce as the governance layer over all of them.

### Build-vs-buy signals

- **Existing Salesforce customers**: the buy keeps being valuable — context, workflows, trust layer already in place. The rip-and-replace story weakens.
- **Greenfield buyers**: the 60+ MCP-tool surface + AgentExchange ecosystem is a real moat vs building from scratch; trade-off is Salesforce lock-in inherited by every agent that uses it.
- **Multi-vendor shops**: Agent Fabric's cross-vendor claim is the most interesting piece to verify — if real, Salesforce is trying to be the **control plane over all your agents**, not just the Salesforce ones.

## Summer '26 Release (GA 2026-06-15)

Platform release announced 2026-06-10; available June 15. Extends the Headless 360 / Agentforce substrate with multi-agent orchestration as a GA capability, MCP-backed analytics integration, and 10+ domain-specific agent packs.

### Multi-Agent Orchestration

Agents divide end-to-end workflows among themselves with shared context across channels. Customer sees a single point of contact; agents hand off state internally without requiring the customer to re-state the problem. Framing matches Microsoft Agent 365 (June 2026) and Google Agent Factory — GA from Salesforce signals multi-agent orchestration is now table stakes for enterprise CRM platforms, not a roadmap item.

**Unverified claim:** seamless inter-agent context sharing. The architectural mechanism (true context threading vs state serialization at handoff) is not specified. Practitioner reports will surface the real behaviour.

### Tableau MCP

AI agents query Tableau's analytics engine directly via MCP, scoped by the **Agentforce Trust Layer**. Framed as a secure MCP integration — directly relevant to the MCP RCE disclosure (2026-05-08, see [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]]). Salesforce does not specify which attack classes the Trust Layer mitigates against the STDIO RCE class; treat the "secure" framing as a claim requiring scrutiny, not a resolved posture.

Competing direction: Snowflake CoWork / MCP governance layer (Snowflake Summit, 2026-06) pursues the same "AI agents with governed analytics access" pattern via Snowflake Cortex. For shops using both, this is now a platform selection dimension.

### Domain Packs and Agent Features (2026-06-15)

| Feature | What it does |
|---|---|
| **IT Service Domain Pack** | 50+ OOB agents in Slack, Teams, IT Service Desk; intent detection routes and resolves employee needs proactively |
| **Agentforce Self-Service** | Help Agent setup in 6 clicks; new Portal experience; simplified pricing (actual pricing not disclosed) |
| **Customer Engagement Agent** | Qualifies leads 24/7 via two-way conversation on website/email; warm handoff to sales |
| **Momentum** | Passive capture of calls, emails, meetings; writes structured data back to Salesforce CRM in real time; no rep workflow change |
| **Collections with Agentforce** | Predictive AI scores invoices by payment history; Agentforce recommends dunning plans with dynamic rules per customer tier |
| **Slack First Sales** | Agentforce Sales agents inside Slack; proactive prospect/engage/pipeline agents; single seller operates with full revenue team context |
| **Process Compliance Navigator** | Monitors live workflows; intercepts non-compliant actions in real time; single platform for regulation/policy/risk/control |
| **Scheduling Console** | Live appointment updates, map-route visualisation, Agentforce surfaces closest qualified technicians for emergency dispatch |
| **Real-Time Offer Management** | Personalised channel-optimised offers based on dynamic customer behaviour; agent-first orchestration at scale |
| **Security Mesh** | Unifies disparate data sources into a cohesive data fabric; transforms disconnected alerts into risk scores |

Secondary: Storefront Next (AI-first commerce storefront), Briefings (audio account summaries for field sales), Warranty Claims Assistance, Retail Execution Dashboards for Tableau Next, Slack for Education.

### Techniques under the hood (2026-06-15)

- **MCP as analytics bridge** — Tableau MCP uses MCP protocol for agent→analytics queries, Trust Layer as access/isolation scope.
- **Predictive AI for invoice risk scoring** — technique not specified beyond "payment history and account data"; likely standard gradient-boosted model on CRM payment history.
- **Intent detection for IT routing** — unspecified; inferred from "auto-detects intent" claim.
- **Momentum passive capture** — conversation/email/meeting ingestion pipeline writing structured records to CRM; no agent workflow changes required on the rep side.

### Hard limits (2026-06-15)

Not disclosed. No concurrency caps, inter-agent latency specs, MCP query rate limits, or cost-per-orchestration-step published. Re-check before advising.

### Hype-vs-reality delta (2026-06-15)

- All reception is vendor-sourced; no independent reviews as of 2026-06-10.
- Multi-agent orchestration "single point of contact, shared context" is the headline claim — needs practitioner validation on whether context is truly threaded or serialised at handoff.
- Tableau MCP "secure" framing is asserted, not demonstrated — no CVE scope, no isolation architecture disclosed.
- IT Service Domain Pack "50+ OOB agents" is a quantity claim, not a quality claim; coverage depth unknown until practitioners map it against real IT workflows.

### Build-vs-buy signals (2026-06-15)

- **Existing Salesforce + Tableau customers:** clear buy — Momentum passive capture, Collections automation, IT Domain Pack, and Tableau MCP all land on existing data/permissions with no rebuild.
- **Greenfield:** multi-agent orchestration and Tableau MCP are compelling but compound Salesforce dependency. Evaluate against Snowflake Cortex / MCP governance if Snowflake is already in the stack.
- **Multi-vendor shops:** Slack First Sales and Process Compliance Navigator extend the Agent Fabric control-plane pattern. The "single seller with full revenue team context" claim is where Salesforce lock-in is stickiest.

## Claudeforce (2026-08-26)

Salesforce and Anthropic announced an expanded partnership branded **Claudeforce** — first use of the "force" suffix for a partner product. Flagship deliverable **Salesforce in Claude**: 37 prebuilt sales skills usable directly from Claude's interface (query/update/act on live CRM data), explicitly pitched so customers "will never need [the Salesforce] app again" (Salesforce's own framing, per VentureBeat). Pilot customers live now; open beta targeted September 2026.

This is a step beyond Headless 360's "expose everything as API/MCP/CLI" pattern: Headless 360 kept Salesforce as the substrate agents build on top of; Claudeforce makes Salesforce's *own* first-party interface optional in favor of a competitor's chat surface. Announced same-day as Salesforce's Q2 FY27 earnings (raised forecasts; Agentforce ARR reported $1.5B+); framed by Reuters/CNBC as Benioff directly answering "SaaSpocalypse" investor concerns by embracing rather than resisting the agent-as-interface trend. Full detail, conflict-flag analysis (see [[../conflicts/open-questions-2026-04|C1]]), and sourcing: [[../landscape/salesforce-anthropic-claudeforce-2026-08|salesforce-anthropic-claudeforce-2026-08]].

## AIforce / Dreamforce 2026 (2026-09-15/16)

At Dreamforce 2026, Salesforce rolled Claudeforce into a broader umbrella brand, **AIforce**, described by President of Applications and Marketing Solutions Patrick Stokes as sitting one layer above Headless 360: "Headless 360 is really the raw MCP servers, the raw APIs... AIforce is a step above it... March was like the raw materials, or the raw ingredients, and AIforce is like the chocolate chip cookie that comes out of the oven" (SiliconANGLE, 2026-09-15). AIforce is not a standalone SKU — it groups three concrete products under one interface-layer story: **Claudeforce** (expanded, see below), **Slackforce** (new), and **Agentforce Coworker** (100,000 users activated in its first 35 days, per TechNode). Benioff's framing: "an intelligent, dynamic, composable system that is securely governed, built with Zero Data Retention."

### Interface-decoupling architecture claim (2026-09-15)

The load-bearing claim: Salesforce data, workflows, permissions, and business logic become reachable from third-party AI surfaces (Claude, Slack, Agentforce, other MCP clients) **without the native Salesforce UI**, while requests still route through Salesforce's existing permissions and business rules (TechNode, SiliconANGLE, both 2026-09-15/16). SiliconANGLE distinguishes this from a generic MCP wrapper — Salesforce's pitch is that AIforce carries "business logic, semantics, security and governance" with each exposed action, not just data access. Neither source independently verifies this is new infrastructure versus a repackaging of Headless 360/MCP; TechNode is the more skeptical of the two, flagging the real open question explicitly: "the practical issue for enterprises will be how permissions, auditability and approval controls behave as interfaces become more flexible and agents can initiate actions across multiple systems" (TechNode, 2026-09-16). Treat "live interface layer" as a Salesforce-coined term pending practitioner verification, same caveat status as Agent Fabric's multi-vendor governance claim above.

Separate context on the messaging pattern: Salesforce Ben's pre-Dreamforce piece (published before the Sept 15-16 announcements; not a report on AIforce/Slackforce/Koa themselves) argues Salesforce has shipped one major architectural rebrand per Dreamforce for several years running (Agentforce → 2.0 → 2dx → 3 → 360 → Claudeforce) and predicted "something bigger" than Claudeforce alone would headline 2026 — a prediction AIforce's umbrella framing arguably fulfills. It also notes Benioff polled X on renaming Salesforce "SalesforceSlack" (68.3% no, Aug 13 2026) and flags the unresolved Agentforce pricing saga ($2/conversation → Flex Credits → pay-as-you-go → pay-per-resolution) as still-open. Read this source as messaging-pattern context, not as independent verification of the technical claims below.

### Slackforce (announced 2026-09-15)

Pulls "relevant context and data from Salesforce, chat and other tools to create live, interactive interfaces for the whole team to explore, comment on and work within" (SiliconANGLE) — branded **Slackforce Surfaces**, and powers Salesforce's out-of-the-box Slackbot assistant. A companion feature, **Slack CRM with Slackforce**, connects "every Slack conversation, user and update back to Salesforce," letting users open accounts, log call notes, and update records without leaving Slack (TechNode: "create or update CRM records and trigger workflows from Slack rather than opening a separate CRM view"). No GA date disclosed in either source (contrast Claudeforce, explicitly beta — below). One named customer: Hotel Engine ("We handle over 800,000 customer inquiries a year, so getting our people the right context fast is everything. Slackforce makes that possible" — SiliconANGLE).

### Koa — CRM reasoning model on Nvidia Nemotron (announced 2026-09-15)

Salesforce's first purpose-built **CRM reasoning model**, co-announced with Nvidia. Built by post-training **Nvidia Nemotron 3 Super** on a proprietary synthetic dataset modeled on "nearly three decades of CRM deployments" (Salesforce newsroom, 2026-09-15). Vendor benchmark claim: Koa "matches or exceeds leading model performance on CRM actions with three times fewer errors" on tasks like updating opportunities, routing cases, and scheduling follow-ups — unverified by independent benchmark as of this writing. Deployment/privacy angle: because Nemotron is open-weight, Salesforce fine-tunes and runs Koa entirely within its own infrastructure — "no customer data is used during training or inference" (vendor claim). Timeline: customer pilots start October 2026 inside Agentforce; US general availability targeted **winter 2026**. TechCrunch's framing ("everything the AI labs should fear," 2026-09-15) is the narrative to watch: a vertical incumbent shipping its own domain-tuned reasoning model on open-weight infra is a direct build-vs-buy signal against paying frontier-lab API rates for CRM-shaped agent work — flag for the [[../conflicts/open-questions-2026-04|open-questions]] build-vs-buy thread once pilot data lands.

### Claudeforce expansion (2026-09-15)

The **37 prebuilt sales skills** figure from the 2026-08-26 launch is unchanged at Dreamforce — not expanded in count — but scope and status moved: **Salesforce in Claude now moves into beta** (TechNode, 2026-09-16), delivered via "a prebuilt Model Context Protocol server" covering prospecting, meeting preparation, and pipeline management. Piloted by **Deloitte, GitLab, and Legora** (TechNode names all three as pilots; no per-customer use-case detail given in the source). Roadmap disclosed by SiliconANGLE: skills will "soon include analytics in Tableau as well as skills for service, marketing, commerce and industries" — not yet shipped. Separately for builders: a **Claude Code plug-in** ships with 40 skills and access to Salesforce's skills library on GitHub, with specialized sub-plug-ins loading dynamically for dev tasks. TechNode is the only source to flag pricing/availability uncertainty explicitly: "pricing and packaging may change and... availability can vary by region and customer agreement."

### Adjacent: seven named Agentforce agents (2026-09-11)

Days before Dreamforce, Salesforce gave Agentforce a named-agent lineup ("job-ready agents"): **Casey** (customer service — voice/SMS/WhatsApp/web chat), **Paige** (IT & HR service), **Carter** (shopper/commerce), **Hunter** (outbound sales — pilot now, GA targeted November 2026, first agent on a new "long-horizon runtime" designed to work a pipeline over weeks rather than single sessions), **Marshall** (supply-chain/back-office orchestration with a deterministic-execution audit trail), and **Piper** (inbound pipeline generation). A seventh, **Fin** (customer experience), is not built in-house — Salesforce completed its acquisition of Fin AI on 2026-09-10 and folded it into the lineup, one day before the named-agent announcement (Salesforce newsroom: [agentforce-job-ready-ai-agents](https://www.salesforce.com/news/stories/agentforce-job-ready-ai-agents/), [salesforce-completes-acquisition-of-fin](https://www.salesforce.com/news/press-releases/2026/09/10/salesforce-completes-acquisition-of-fin/)). Note for the build-vs-buy read: a "portfolio of named agents" narrative includes at least one acquired product, not seven from-scratch builds.

### Hype-vs-reality delta (2026-09-15/16)

- SiliconANGLE reads close to a press-release rewrite: heavy direct-quote reliance (Benioff, Stokes), no independent verification of the governance or interface-decoupling claims.
- TechNode is the more useful source for scrutiny: explicitly beta-flags Claudeforce, states the Coworker adoption number, and is the only one of the three to name governance/auditability as an open enterprise risk rather than a solved problem.
- Salesforce Ben's piece is *not* coverage of the Sept 15-16 announcements — it's pre-event speculation about Salesforce's rebrand cadence and pricing history; useful as messaging-pattern context, not as a fact source on AIforce/Slackforce/Koa.
- Koa's benchmark claim ("3x fewer errors") and all Zero-Data-Retention / permissions-inheritance claims are vendor-sourced with no independent practitioner validation yet — same caveat pattern as Headless 360's 2026-04-15 launch numbers above.

## Cross-vendor context (2026-04 / 2026-06)

- **Gemini Enterprise agent catalog** (see [[google-cloud-agentic-partner-fund-2026-04]]) surfaces Salesforce as one of the named ISV agents — i.e., Salesforce is *both* building the headless-substrate motion (this page) *and* shipping into a hyperscaler runtime. Two distribution arcs.
- **Microsoft Agent 365 / Copilot Studio** (June 2026, see [[microsoft]]) — parallel move on multi-agent orchestration and MCP integration. Both Salesforce and Microsoft GA'd multi-agent orchestration in the same release window; this is now a table-stakes enterprise feature, not a differentiator.
- **Snowflake CoWork / MCP governance** (Snowflake Summit 2026-06, see [[../landscape/snowflake-summit-2026-06|snowflake-summit-2026-06]]) — competing "governed AI analytics access" direction to Tableau MCP. Shops using both Salesforce and Snowflake face a platform selection dimension on which MCP governance layer they anchor to.
- **MCP RCE supply-chain disclosure** (2026-05-08, see [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]]) — Tableau MCP Trust Layer is Salesforce's answer to the enterprise MCP security question. Mechanism not specified; treat as a claim requiring scrutiny.
- **Open question**: does the "everything as MCP / API / CLI" pattern spread to Microsoft Dynamics, SAP, Oracle, Workday, ServiceNow, HubSpot within 12 months? See [[open-questions-2026-04]] C17. If yes, structural pivot. If no, Salesforce-specific defensive play. Multi-agent GA from Salesforce and Microsoft in the same window strengthens the "structural pivot" read.

## Reader notes

- This page covers Salesforce as a platform — not just Headless 360 as a product.
- Pricing and hard limits deliberately omitted where source is silent — re-check before client advisory.
- Agent Fabric's multi-vendor governance is the single most important claim to verify in next-few-months practitioner ingests.

## Security: SalesBleed (2026-09-24)

Zenity Labs disclosed three now-fixed Agentforce vulnerabilities (two 0-click CRM exfiltration chains via Web-to-Lead prompt injection, one anonymous Slack phishing flaw); Trusted URLs redaction was bypassed with trivial parsing edge cases. Fixes verified 2026-09-21. Security-vendor research via The Register. See [[../landscape/salesforce-agentforce-salesbleed-2026-09|salesforce-agentforce-salesbleed-2026-09]]; bears on C18 governance claims.

## Source

- `raw/research/weekly-2026-04-22/03-salesforce-headless-360.md`
- `raw/research/weekly-2026-06-10/01-salesforce-summer26-multiagent-2026-06.md`
- `raw/research/weekly-2026-08-26/02-01-salesforce-anthropic-claudeforce-2026-08.md` (VentureBeat, 2026-08-26 — Claudeforce)
- `raw/research/weekly-2026-09-16/04-siliconangle-aiforce.md` (SiliconANGLE, 2026-09-15 — AIforce)
- `raw/research/weekly-2026-09-16/05-salesforceben-claudeforce-df26.md` (Salesforce Ben, pre-Dreamforce speculation piece — messaging-pattern context only)
- `raw/research/weekly-2026-09-16/07-technode-aiforce.md` (TechNode Global, 2026-09-16 — AIforce/Claudeforce/Slackforce)
- Koa: Salesforce newsroom press release (2026-09-15, `salesforce.com/news/press-releases/2026/09/15/koa-reasoning-model`) and TechCrunch (2026-09-15) — found via WebSearch, not captured to `raw/`; re-capture if a durable citation is needed.
- Seven named agents: Salesforce newsroom (2026-09-11, `salesforce.com/news/stories/agentforce-job-ready-ai-agents`) and acquisition press release (2026-09-10) — found via WebSearch, not captured to `raw/`.

## Related

- [[agents-eating-saas]]
- [[ai-app-categories-2025]]
- [[ai-apps-layer-2026]]
- [[ai-infrastructure-frontiers-2026]]
- [[google-cloud-agentic-partner-fund-2026-04]]
- [[trace]]
- [[open-questions-2026-04]]
- [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]]
- [[../landscape/snowflake-summit-2026-06|snowflake-summit-2026-06]]
- [[microsoft]]
- [[../landscape/salesforce-anthropic-claudeforce-2026-08|salesforce-anthropic-claudeforce-2026-08]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]] — Claudeforce/Salesforce-in-Claude tracked there too (now beta as of 2026-09-15); links back to this page
- [[../landscape/salesforce-agentforce-salesbleed-2026-09|salesforce-agentforce-salesbleed-2026-09]]
