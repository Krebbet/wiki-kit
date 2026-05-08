# Microsoft Agent 365 (GA 2026-05-01)

Microsoft Agent 365 hit general availability on 2026-05-01 as an enterprise *control plane to observe, govern, and secure* agents — landing the **first vendor multicloud agent governance plane** via public-preview registry sync to AWS Bedrock and Google Cloud Gemini Enterprise Agent Platform on the same day. $15/user/month standalone or bundled into Microsoft 365 E7. Each AI agent gets its own Entra identity, Purview labels, Defender runtime governance, Intune device management. Vendor primary source.

> **Source caveat.** This page summarises a Microsoft Security Blog post (2026-05-01). Architectural and SKU claims are vendor product spec; risk-reduction and "confidence" claims are vendor marketing. Treat capability claims as vendor-stated.

## Source

- `raw/research/weekly-2026-05-04/01-microsoft-agent-365.md` — captured 2026-05-04 from `https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations/`.

## What shipped (GA today)

- **General availability** as of 2026-05-01.
- Sold *"in [Microsoft 365 E7](https://aka.ms/51ME7blog) or standalone at USD15 per user per month."*
- **Per-license framing**: "covers an individual who manages or sponsors agents, or uses agents to do work on their behalf" — i.e., *per-human, not per-agent*.
- **Entra network controls extended GA today** to Microsoft Copilot Studio agents and agents running on user endpoint devices, including local agents such as OpenClaw.

GA covers two of three agent identity classes:

| Class | Status |
|---|---|
| Agents working on behalf of users (delegated access) | GA |
| Agents operating behind the scenes (own access) | GA |
| Agents participating in team workflows (own access) | Public Preview |

In the latter two classes, each agent gets its own Entra identity.

## What's preview

- **Multicloud registry sync** (public preview) with AWS Bedrock and Google Cloud connections, *"enabling IT teams to automatically discover, inventory, and, soon, perform basic lifecycle governance — for example, start, stop, delete agents — across these platforms."*
- **Defender asset-context mapping** (June 2026 preview) — for each agent, surfaces the devices they run on, **MCP servers configured for those agents**, the identities associated with them, and the cloud resources those identities can reach. Includes runtime blocking: *"If a managed agent exhibits malicious behavior patterns, such as attempting to access or exfiltrate sensitive data, Defender will be able to block coding agents in runtime and generate alerts."*
- **Windows 365 for Agents** (US-only public preview) — *"a new class of Cloud PCs purpose-built for agentic workloads and managed in Intune."*
- **Shadow AI page** in Agent 365 in the Microsoft 365 admin center.

## The multicloud registry-sync angle (load-bearing novelty)

This is the **first vendor product to ship a cross-cloud agent registry as a primitive** — peer to Microsoft Foundry, AWS Bedrock, and Google Gemini Enterprise Agent Platform (formerly Google Vertex AI). The wiki's [[mcp-infrastructure]] page calls out cross-vendor governance as a 2026 roadmap gap; Agent 365's registry-sync preview is the first vendor *response* to that gap.

The same Defender preview adds *MCP server inventory as a first-class governance object* — the first vendor primitive of its kind.

## Identity-per-agent via Entra

Two of three agent classes get their own Entra identity. Combined with Purview labels and Defender runtime policy, this is the first widely deployed governance plane for agents that *rides on top of an existing enterprise IAM stack* rather than asking enterprises to adopt a new identity primitive.

## Local-agent discovery: Defender + Intune

Frontier-program customers can already see *"if OpenClaw agents are being used in the organization, which devices they are running on, and use Intune policies to block common ways that OpenClaw runs."* Coverage *"expanding soon to other widely used agents like GitHub Copilot CLI and Claude Code"* — i.e., the same coding agents the wiki has pages on (see [[langchain-deep-agents]], [[effective-harnesses]], [[anthropic-claude-code-postmortem]]) are now governance objects from Microsoft's POV.

## Windows 365 for Agents (runtime substrate)

Cloud PCs purpose-built for agentic workloads, managed in Intune, running with the same identity/security/management controls as employee endpoints. Microsoft's analogue to the runtime substrate other deployment-tier wiki pages document — see [[shopify-simgym]] (parallel cloud browsers via Browserbase) and [[cognition-cloud-agents]] (microVMs with hypervisor-level snapshotting).

## Pricing and packaging

- **Standalone**: $15 USD per user per month.
- **Bundled**: included in Microsoft 365 E7 ("Frontier Suite").

## Ecosystem and service partners

**SaaS agent launch partners** (agents *"fully configured to be managed by Agent 365"*): Genspark, Zensai, Egnyte, Zendesk. **Agent factories**: Kasisto, Kore, n8n. Other SDC partners visible in logo grid: Adobe, NVIDIA, Celonis. Vendor claim: *"No integration work by IT or security teams."*

**Service partners**: Accenture, Bechtle, Capgemini, Insight, KPMG, Protiviti, Slalom; also Cognizant, Avanade, Deloitte, EY, PwC, TCS. Service categories: workshops/assessments, governance/enablement, managed services, advisory/readiness, security/integration.

The partner-services framing names **five governance pillars**: Inventory and ownership; Least privilege; Compliance and data protection; Threats and multi-platform estates; Ongoing operations.

## What the post does *not* say

- No agent-discovery accuracy numbers.
- No registry-sync latency SLOs.
- No false-positive rates on shadow-AI detection.
- No blast-radius computation latency.
- No throughput / scale numbers.
- The customer testimonial (NTT DATA, Yuji Shono) is qualitative — *"scale and govern AI agents with confidence"* — no figures.

A live "Ask Microsoft Anything" session is scheduled for Tuesday May 12, 2026 — useful follow-up signal source if any quantitative claims surface there.

## How this slots into the wiki

- [[mcp-infrastructure]] — vendor data point on the *governance + audit + cross-vendor* axis the MCP 2026 roadmap explicitly defers; Defender's *"MCP servers configured for those agents"* mapping is the first vendor product to treat MCP server inventory as a first-class governance object.
- [[topology-taxonomy]] — control-plane-as-substrate framing introduces a new infrastructure tier *(governance-and-identity substrate)*, analogous to how [[cognitive-fabric-nodes]] lifts memory out of the agent. Different mitigation axis from the existing context-/state-side classes — addresses *organizational blast radius* rather than long-horizon context loss.

## Related

- [[mcp-infrastructure]] — the MCP 2026 governance roadmap that Agent 365 is the first vendor response to.
- [[topology-taxonomy]] — extended with governance-and-identity substrate as a new tier.
- [[cognition-cloud-agents]], [[shopify-simgym]], [[cognitive-fabric-nodes]], [[openai-symphony]] — peer deployment-tier pages.
- [[anthropic-claude-code-postmortem]], [[anthropic-internal-study]] — vendor-internal context for Claude Code, which Agent 365 explicitly names as a target for shadow-AI discovery and Intune blocking.
- [[langchain-deep-agents]], [[effective-harnesses]] — coding-agent harness pages whose runtime (Claude Code, GH Copilot CLI) is what Agent 365 now claims discovery and blocking authority over.
- [[externalization-survey]] — Agent 365 instantiates §6.2.5 (configuration/permissions/policy encoding) at vendor scale.
