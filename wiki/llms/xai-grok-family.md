# xAI / SpaceXAI (Grok)

Running page for xAI's Grok model family and agent products. First wiki coverage: **Grok Bot** (beta, 2026-08-11), persistent always-on AI agent "teammates" with dedicated cloud compute, delivered through SpaceX-owned Cursor and SuperGrok subscription tiers. Note the vendor now self-describes as **SpaceXAI** (xAI as a SpaceX division) in this source's framing — a naming/identity shift not previously tracked in this wiki, following SpaceX's $60B Cursor acquisition option (see [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]]).

## Grok Bot (beta, 2026-08-11)

**One-line:** persistent, role-assigned AI agents ("Bots") that operate a user's actual software — logging into apps and sites like a human, including ones with no API or MCP — continuously, even while the user's device is offline, and hand off work between each other.

### What it does

- **Computer-use automation, not API integration.** Each Bot runs in its own dedicated cloud compute environment rather than calling app-specific APIs — explicitly targets apps/sites with "no clean API or MCP."
- **Multi-agent orchestration.** Bots coordinate via shared threads; a documented pattern uses a "Chief of Staff" Bot supervising specialist Bots (inbox, recruiting, expenses, ops, bug fixes) — removes the user as routing layer.
- **Workflow learning.** Users demonstrate a task once; the Bot saves it as a reusable "routine," refined by later corrections. Persistent memory beyond chat transcript — retained preferences, learned escalation thresholds (when to ask for approval vs. act independently).
- **Model layer fully abstracted.** SpaceXAI does not disclose which underlying models the router selects; no user-facing model pick/pin mechanism. A beta tester (Matt Shumer) called the router "wasn't great" during testing, later told it improved — unverified.

### Deployment and pricing

SaaS only, bundled into subscription tiers — not enterprise VPC/on-prem. Available macOS, Windows, Linux, iOS at launch; Android "coming soon."

| Tier | Price | Notes |
|---|---|---|
| Cursor Premium Teams | $120/seat/month | Centralized billing/settings, team skill/plugin marketplace, shared usage analytics, SAML/OIDC SSO |
| Cursor Ultra (individual) | $200/month | Includes "a computer for Grok Bot," tool access, scheduled routines, desktop/mobile operation |
| SuperGrok Heavy ($300/month) subscribers | Included | No extra charge |

Org signups are waitlist-only as of 2026-08-11, not self-serve. Open cost question flagged in coverage: "how usage limits affect total cost once agents begin running continuously" — 24/7 operation is a not-yet-quantified cost driver, directly relevant to the flat-subscription-vs-agent-economics thread at [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]].

### Market reception

Two named early-access reactions, both positive on capability, mixed on the model router: Lenny Rachitsky (Lenny's Podcast) called it more reliable than "OpenClaw" and predicted it becomes "a huge new product line for Cursor/Grok/SpaceX." Matt Shumer praised the multi-agent orchestration ("worked out of the box") but flagged the opaque model router. No customer names, revenue/ARR, or G2/HN/Reddit commentary in coverage yet — beta-stage reception only.

### Hype-vs-reality

No published benchmarks for agentic task performance at launch. The vendor's own reliability framing ("the work lands where a human would put it") is undercut by the source's own caveat: proactive, memory-driven, permission-light autonomous agents "expand the consequences of an incorrect assumption, stale context, or improperly scoped permission" — reliability and safety claims are unproven at launch scale, not reality-tested.

### Build-vs-buy signals

An in-house equivalent requires: persistent per-agent compute/session infrastructure (not just API calls), a UI-automation/computer-use engine robust against arbitrary third-party sites, a memory/preference-learning layer distinct from chat history, a model-routing layer, and permission/escalation tooling for production-system access. **Lock-in risk:** the model layer is fully opaque — customers cannot control or audit which model handles a given task, a meaningful governance risk for enterprises with model-specific compliance requirements. Bundling into Cursor subscriptions (post SpaceX-Cursor acquisition) also ties adoption to the Cursor/xAI ecosystem rather than an open standard.

### Competitive context

Positioned directly against Anthropic's computer-use capability and Claude Cowork, OpenAI's Codex computer-use expansion / Workspace Agents / ChatGPT Work, and Microsoft's Scout (always-on personal agent, [[../landscape/microsoft-build-2026-06|microsoft-build-2026-06]]) — all now converging on the same "persistent agent teammate" category from different platform bases.

### Source

VentureBeat, 2026-08-11 ("SpaceXAI's Grok Bot turns agents into persistent digital coworkers"). Captured `raw/research/weekly-2026-08-12/05-xai-grok-bot-agent-teammates.md`.

## Related

- [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]]
- [[anthropic-claude-family]]
- [[openai]]
- [[../platforms/microsoft|microsoft]]
- [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]
- [[../startups/cursor|cursor]]
