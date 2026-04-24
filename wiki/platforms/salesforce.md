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

## Cross-vendor context (2026-04)

- **Gemini Enterprise agent catalog** (see [[google-cloud-agentic-partner-fund-2026-04]]) surfaces Salesforce as one of the named ISV agents — i.e., Salesforce is *both* building the headless-substrate motion (this page) *and* shipping into a hyperscaler runtime. Two distribution arcs.
- **Open question**: does the "everything as MCP / API / CLI" pattern spread to Microsoft Dynamics, SAP, Oracle, Workday, ServiceNow, HubSpot within 12 months? See [[open-questions-2026-04]] C17. If yes, structural pivot. If no, Salesforce-specific defensive play.

## Reader notes

- This page covers Salesforce as a platform — not just Headless 360 as a product.
- Pricing and hard limits deliberately omitted where source is silent — re-check before client advisory.
- Agent Fabric's multi-vendor governance is the single most important claim to verify in next-few-months practitioner ingests.

## Source

- `raw/research/weekly-2026-04-22/03-salesforce-headless-360.md`

## Related

- [[agents-eating-saas]]
- [[ai-app-categories-2025]]
- [[ai-apps-layer-2026]]
- [[ai-infrastructure-frontiers-2026]]
- [[google-cloud-agentic-partner-fund-2026-04]]
- [[trace]]
- [[open-questions-2026-04]]
