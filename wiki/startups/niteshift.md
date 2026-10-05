# Niteshift

Cloud infrastructure platform for AI coding agents, founded by Sajid Mehmood (CEO) and Conor Branagan — both early Datadog engineers. Raised $7M seed led by Greylock's Jerry Chen; GA launched June 10, 2026. Sells per-minute compute and dev-environment provisioning, not tokens or model access.

## Source
TechCrunch, 2026-06-10. Captured 2026-06-10.

## What it is

Niteshift routes coding agents (Claude Code, OpenAI Codex, open-source alternatives) through fully configured development environments hosted on Niteshift's cloud. The platform handles environment provisioning, model routing, and switching between GPT/Claude/OSS backends based on project requirements. Enterprises pay per-minute usage rates — an infrastructure pricing model rather than per-token — similar to how cloud VMs are billed.

The founders' stated thesis is that frontier labs are moving "up the stack" into vertical markets (legal, healthcare, finance), making them direct competitors to enterprise software buyers. Niteshift positions as a vendor-neutral middle layer: code never goes directly to a single frontier lab, and the enterprise retains choice over which model runs against sensitive codebases. The founding team draws an explicit parallel to Datadog's early growth among e-commerce companies who refused to build core infrastructure on AWS (framed as the "retail apocalypse" analogy) — enterprises choosing neutrality over convenience.

No details on orchestration stack, container isolation technology, or compliance certifications were published at GA. All product claims as of launch are founder-quoted; no customer case studies or enterprise adopters have been disclosed.

## Why it matters

Niteshift is an early articulation of a distinct infrastructure category: "selling software to agents, not humans." As coding agents displace individual developer tooling, the billing and trust surface shifts from per-seat SaaS to per-minute compute — a structural change the [[landscape/agentic-compute-pricing-2026-04]] entry traces. Niteshift's model-agnostic routing also directly counters the bundling strategies of OpenAI ([[landscape/openai-deployment-company-2026-05]]) and Microsoft ([[landscape/microsoft-build-2026-06]]), which are pushing enterprises toward captive model stacks.

The security/compliance angle — keeping sensitive code off frontier lab APIs — is plausible as enterprise anxiety grows, though it overlaps with concerns documented in [[landscape/mcp-rce-supply-chain-2026-05]]. Whether "model independence" (vendor framing, scare-quotes warranted) is a durable moat or a wedge that hyperscalers close quickly via Bedrock/Azure AI Foundry is the central open question.

## Competitive context

- **Cursor** — named direct competitor; IDE-layer product rather than infra; reportedly in acquisition talks with SpaceX at $60B valuation (June 2026). See [[startups/cursor]].
- **Cognition** — $1B raised, $26B valuation; agent-layer competitor but focused on autonomous coding (Devin) rather than infra routing.
- **OpenRouter** — $113M raised, $1.3B valuation; model-routing overlap is significant. Niteshift differentiates on bundled dev environments and enterprise security posture, not routing alone.
- **Amazon Bedrock / Azure AI Foundry** — hyperscaler alternatives. Enterprises already on these platforms have partial model-routing coverage; Niteshift's bet is that code-specific compliance friction justifies a dedicated neutral layer.
- **Microsoft Copilot + Agent 365 bundle** — Microsoft's enterprise bundling ([[landscape/microsoft-build-2026-06]]) is a direct counter-positioning threat: if coding agents ship pre-bundled with enterprise agreements, the "neutral infra" argument weakens.

## Status

Seed stage. $7M raised, June 2026. GA launched June 10, 2026. No disclosed enterprise customers. Angels include Reid Hoffman, Datadog's Olivier Pomel and Alexis Lê-Quôc, Ankur Goyal (Braintrust), Misha Laskin (Reflection AI). Evidence base is thin: all product and thesis claims are founder-sourced from TechCrunch launch coverage.

## Related
[[landscape/agentic-compute-pricing-2026-04]]
[[startups/cursor]]
[[thesis/agents-eating-saas]]
[[landscape/ai-infrastructure-frontiers-2026]]
[[landscape/openai-deployment-company-2026-05]]
[[landscape/microsoft-build-2026-06]]
[[landscape/mcp-rce-supply-chain-2026-05]]
