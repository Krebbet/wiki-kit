# Gemini at Work 2026: the Gemini agent (Google Cloud, 2026-10)

Google Cloud announced a cloud-persistent "universal agent for work" (called "Gemini") at its Gemini at Work 2026 event, announced 2026-10-08 and captured 2026-10-28. The vendor-stated differentiators are four memory types, a per-agent cryptographically attested identity, an Agent Sandbox plus Agent Gateway governance layer, and routing across Gemini and Claude models. Watch, do not buy on this evidence. The only source is Google's own keynote-adaptation post. It gives no GA date and no pricing for the agent. Only the Financial Services and Legal verticals carry a status ("in preview"), and the "real-time spend caps" claim is cut off mid-sentence in the capture.

## What it is (vendor-stated, 2026-10-28 capture)

- A "single, universal agent" for Q&A, knowledge work, media creation and code, "in a single agent and a single API". It takes objectives rather than instructions, plans, uses skills and tools, and returns finished work. It can be a personal assistant, a team member or a role-based agent such as a finance analyst, and can be assigned work, scheduled or event-triggered.
- Runs in Google's cloud with "persistent execution": work continues after the laptop closes. Surfaces named: web, mobile, desktop, CLI, Workspace, Microsoft 365, Slack. It can also run "headless" inside third-party apps.
- Multi-agent by design: temporary sub-agents are created dynamically, each with its own identity, running parallel and sequential steps for hours or days. Persistent "coworker agents" have defined roles and their own Workspace account (an @agents.company.com address, calendar, Drive), and appear under their own name in version history.
- Overlaps with earlier Google agent announcements: [[landscape/google-cloud-next-2026-day2]] (agent platform, runtime, memory) and [[landscape/google-io-2026-enterprise]] (background agent). The relationship to those stacks is not spelled out in this source.

## Four memory types

Vendor-stated taxonomy (2026-10-28):

| Type | Vendor description |
|---|---|
| Session | Task-level memory, can span days |
| Semantic | Structured knowledge base built from documents, people and agents |
| Procedural | How jobs get done, including skills the agent writes for itself |
| Episodic | Record of prior actions |

A single "personalization graph" is said to be shared across devices and channels, and the agent "continuously learns from each execution". "Learns from every interaction" and self-authored skills are unverified: no evidence of retention quality, eviction or inspection controls in the source. The taxonomy is the useful part to borrow, since it maps cleanly onto how agent memory gets designed elsewhere.

## Identity, audit and governance

Framed around four questions: who is the agent, what may it do, what did it do, what must it never touch.

- **Per-agent identity (2026-10-28):** every agent gets its own cryptographically attested identity, "governed like an employee" and least-privilege. The identity is stamped into logs and into any VM spun up for code execution. It is mapped to external systems via OAuth and "industry standards" (unnamed).
- **Authorization:** fine-grained role-based permissions approved by security admins. Coworker agents see only what is shared with them.
- **Audit attribution:** every action goes to an audit trail attributed to the agent, not to a person, with real-time monitoring for anomalous behaviour. The source gives no log schema, retention or export details.
- **Policy:** write once, applies to all agents (vendor example: agents may not open documents classified "Need to Know"). The Legal vertical is said to inherit matter-level permissions and ethical walls from NetDocuments and iManage.
- **Agent Sandbox:** agents execute inside a sandbox with its own network boundary.
- **Agent Gateway:** all traffic in, out and between agents passes through it. Google describes it as an AI network firewall enforcing organisational policy in real time.
- These are vendor assertions that the controls are secure "by default". Nothing independent is cited. Compare Google's own disclosed incidents in [[landscape/agent-safety-incidents-2026-08]].

## Claude routing inside Gemini

The agent orchestrates across the Gemini family and Anthropic Claude models "today", with other private and open models promised "in the future" (2026-10-28). "Smart Routing" is claimed to triage each workload to the cheapest adequate model. The pitch is "choice at every layer", but memory, skills, registries and identity stay in Google's control plane. Model lineup named in the post: Argon (frontier reasoning), Flash, Omni (media), Gemma (open weights). See [[llms/anthropic-claude-family]].

## Verticals

- **Financial Services:** "in preview" (2026-10-28). Vendor claims 50+ foundational skills, FactSet, LSEG and S&P data, confidence scores and lineage.
- **Legal:** "in preview" (2026-10-28), with partners Harvey and Onit named.
- Government, Healthcare and Retail are "coming soon", with no dates.

## Cost, limits and what is missing

- No price list, no GA date and no stated hard limits for the agent itself (checked against the 2026-10-28 capture).
- The **"real-time spend caps" bullet is truncated in the capture** (it ends "You can"), so the headline cost-control claim has no mechanics here. The adjacent claims, multi-model orchestration and Smart Routing, are described only in a sentence each.
- Infra claim: TPU 8i "80% better price-performance" than the prior generation (vendor-stated, 2026-10-28).
- Customer bullets in the capture are garbled, so named customer outcomes are omitted from this page. Most would concern the existing Gemini Enterprise product rather than this agent anyway.
- Source type: vendor first-party only. No practitioner, reviewer or issue-tracker evidence.

## Build-vs-buy read

Identity, gateway, audit and sandbox are the primitives most teams will not build themselves, and Google is selling them as a bundle. The cost is concentration: the control plane that holds identity, memory and skills is Google's. Comparable sets: [[landscape/aws-bedrock-agentcore-june-2026]], Microsoft's offerings in [[landscape/microsoft-build-2026-06]], and ServiceNow's credential approach in [[platforms/servicenow]]. Re-evaluate once GA, pricing and the spend-cap mechanics are published.

## Source

- `raw/research/weekly-2026-10-28/06-google-gemini-at-work-agent.md`: Google Cloud Blog, "Welcome to Gemini at Work 2026" (keynote adaptation), event announced 2026-10-08, captured 2026-10-28. Section on spend caps truncated; customer bullets garbled.

## Related

[[landscape/agent-identity-governance-2026-09]] [[landscape/google-cloud-next-2026-day2]] [[landscape/google-io-2026-enterprise]] [[landscape/google-a2a-agentic-foundation-2026-08]] [[landscape/aws-bedrock-agentcore-june-2026]] [[landscape/microsoft-build-2026-06]] [[platforms/microsoft]] [[platforms/servicenow]] [[llms/anthropic-claude-family]] [[landscape/agent-safety-incidents-2026-08]]
