# IBM + Microsoft "Imagine Enterprise" Agent Platform (November 2026)

On Tuesday 2026-11-10, Microsoft and IBM announced Imagine Enterprise, an agentic platform for building and governing agents "across data and daily processes." IBM Consulting supplies 6,000+ pre-built agents and transformation expertise; Microsoft supplies the AI and cloud foundation. Forward deployed engineers (FDEs) from both companies support adopters. Verdict: watch, not buy-on-announcement. This is a services-led bundle; the only evidence is one trade-press article relaying the announcement. Technical architecture, pricing and availability are not disclosed.

## What it is (as of 2026-11-18)

- **Platform:** an "agentic platform letting companies build and govern agents across data and daily processes" (CIO Dive's paraphrase of the announcement).
- **IBM's part:** IBM Consulting brings "more than 6,000" pre-built AI agents plus transformation expertise. Mohamad Ali (SVP, head of IBM Consulting): "Clients are no longer looking for AI that simply helps people do the same work a little faster... They want to build an agentic business."
- **Microsoft's part:** the "AI and cloud foundation supporting agents' secure operation." Rodrigo Kede Lima (president, Microsoft Frontier Company): "Enterprise AI will be won by organizations that can turn their data, industry expertise, and AI into action."
- **Delivery:** FDEs from both companies support enterprise adoption.
- **Verticals:** industry-specific frameworks "initially targeting financial services, insurance and retail."
- **Not disclosed in the source:** pricing, general availability or preview status, which Microsoft products form the "foundation" (Foundry, Copilot Studio, Agent 365 are not named), whether IBM watsonx is involved, customer names, and how the 6,000 agents are licensed or deployed.

## Reading the claims

- **"6,000+ pre-built agents" is inventory, not deployments.** The source gives no count of live customer deployments, no definition of "agent," and no quality or usage data. Treat the number as a catalogue size from the consulting arm.
- **Vendor adjectives:** "agentic business" and "secure operation" are announcement language. Nothing in the source evidences either.
- **Governance is asserted, not described.** "Build and govern" is in the brief, but no controls, identity model or audit mechanism is named. Compare Microsoft's actual governance surface in [[platforms/microsoft]] and [[landscape/microsoft-foundry-agent-harness-2026-09]].
- **Single secondary source.** The only source is CIO Dive trade press summarising the joint announcement. There was no primary press release, technical documentation or independent customer evidence in the capture.

## Market framing (CIO Dive, citing Gartner and IBM)

- Gartner (via CIO Dive): only **4%** of CIOs have implemented plans to adjust roles for a human-agent workforce, and most are not doing the deep redesign an agentic-era workforce needs. The article uses this to set up why vendors are packaging help. The Gartner survey itself was not read; the figure is second-hand and undated in the capture.
- Vendors are "jockeying": Microsoft, IBM, Google and AWS have all launched FDE programs, and many offer pre-built industry agents. Imagine Enterprise combines both.
- IBM CEO Arvind Krishna on the Q3 2026 earnings call (October 2026): "AI is only as effective as the system around it": data context, workflows, infrastructure, and a hybrid cloud foundation "without lock-in." The article places Imagine Enterprise less than a month later.

## Build-vs-buy readthrough

- **Buy-side signal:** the packaging says integration and organizational readiness, not model access, is the bottleneck vendors expect to bill for. The same FDE-led pattern appears in [[landscape/openai-deployment-company-2026-05]] (OpenAI DeployCo, Tomoro's ~150 FDEs) and [[landscape/anthropic-enterprise-distribution-2026-05]].
- **When it fits:** a regulated financial-services, insurance or retail shop that wants a consultancy to own agent delivery and already runs on Microsoft cloud. The stated vertical frameworks match that case.
- **When to build:** if you already run agents on Foundry or Copilot Studio with an internal team, a catalogue of generic pre-built agents adds little until IBM shows per-agent quality, licensing and portability terms.
- **Lock-in:** Krishna's "without lock-in" line is unverified for this bundle. Ask how agents are exported, and who owns them after the FDEs leave.
- **Watch for:** a primary announcement with pricing, named Microsoft components, first customers, and any definition of what counts as an "agent" in the 6,000.

## Source

- CIO Dive, "Microsoft, IBM team up on AI agent platform" (captured 2026-11-18): https://www.ciodive.com/news/microsoft-ibm-team-up-ai-agent-platform/874152/ (raw/research/weekly-2026-11-18/06-ciodive-imagine-enterprise.md). Single trade-press secondary source.

## Related

[[platforms/microsoft]] [[landscape/microsoft-foundry-agent-harness-2026-09]] [[landscape/microsoft-build-2026-06]] [[landscape/openai-deployment-company-2026-05]] [[landscape/anthropic-enterprise-distribution-2026-05]] [[landscape/google-cloud-agentic-partner-fund-2026-04]] [[conflicts/open-questions-2026-04]]
