# Sierra

Enterprise AI agent platform co-founded by **Bret Taylor** (also OpenAI chairman; former co-CEO of Salesforce) and **Clay Bavor**. Specialises in customer-experience agents (mortgage refinancing, insurance claims processing, product returns, nonprofit fundraising). Raised **$950M Series D** led by Tiger Global and GV at a **>$15B post-money** valuation on **2026-05-04** — the largest pure-play vertical-agent raise to date.

## Key facts (2026-05-04)

| Element | Detail |
|---|---|
| Round | $950M Series D |
| Lead | Tiger Global + GV |
| Post-money | $15B+ |
| Total capital raised | >$1B |
| ARR trajectory | $100M (Nov 2025) → $150M (Feb 2026); ~50% growth in ~3 months |
| Customer base claim | 40%+ of Fortune 50 (vendor self-reported) |
| Interaction scale | "billions of interactions" handled (vendor self-reported) |
| Notable governance | Bret Taylor: also chairman of OpenAI |

## What the platform does

Customer-experience agents that handle:
- Mortgage refinancing
- Insurance claims processing
- Product returns
- Nonprofit fundraising

Across regulated, multi-step customer-facing workflows. Sierra positions itself toward the "global standard for AI customer experiences" — vendor framing, not independently validated.

## Ghostwriter (April 2026)

"Agent as a service" meta-layer. Users describe the agent they need in natural language; Ghostwriter autonomously builds and deploys a specialised sub-agent. Implies Sierra has a productised vertical-template library that encodes domain-specific orchestration logic across the named workflow categories.

## Deployment / customisation

- **Deployment model:** Sierra-hosted SaaS (implied — not addressed explicitly in the launch coverage).
- **Customisation hooks:** Ghostwriter (NL spec → spawned sub-agent); customer-defined agent personalities; vertical-template library across regulated workflows.
- **Pricing / running costs:** Not disclosed. The Uber CTO datapoint (Praveen Neppalli Naga, StrictlyVC late April 2026: "blew through our [AI] budget" after enabling agentic AI tools late 2025) is attributed to the agentic-AI category broadly, not Sierra specifically.

## Hype-vs-reality

- ARR figures and Fortune 50 penetration are **vendor self-reported**; TechCrunch does not independently corroborate.
- Bret Taylor's dual role as Sierra CEO and OpenAI chairman is a **conflict-of-interest surface**: Sierra is a large downstream consumer of OpenAI infrastructure, and Taylor's OpenAI governance role is not at arm's length from Sierra's vendor relationships.
- The Uber 10%-autonomous-code stat quoted in the coverage relates to **coding agents** (Cursor / Copilot category), not Sierra's customer-experience platform — the article conflates two distinct agent verticals.
- "Global standard" framing is marketing prose with no benchmark or share data attached.

## Build-vs-buy signals

- **Buy signal** for cross-domain, regulated customer-experience agents — Sierra's compliance scaffolding across refinancing / claims is a strong moat. In-house ChatGPT-on-your-data would require agent orchestration, regulatory guardrails, and vertical workflow templates Sierra has already built.
- **Lock-in risk:** deep vertical-template library and Ghostwriter-built agents likely embed Sierra-proprietary abstractions; switching cost rises with agent count.

## Why this matters for the wiki

- **Largest pure-play vertical-agent raise to date** ($950M @ $15B post-money) establishes a category-leader benchmark for the customer-experience subcategory under [[../landscape/ai-app-categories-2025|ai-app-categories-2025]].
- **Validates Sequoia "services are the new software" thesis** — Bret Taylor's "people never need to navigate complex systems" framing is the cleanest public articulation of the narrow-deep vertical wedge from [[../thesis/agents-eating-saas|agents-eating-saas]].
- **Strongest non-coding agent-vertical evidence at scale** — extends [[../conflicts/open-questions-2026-04|C8]]'s generalization-side argument with $150M ARR across multiple regulated verticals (vendor self-reported, weight at 0.7).

## Source

- `raw/research/weekly-2026-05-10/01-sierra-950m-series-d.md` (TechCrunch, 2026-05-04)

## Related

- [[../thesis/agents-eating-saas|agents-eating-saas]]
- [[../landscape/ai-app-categories-2025|ai-app-categories-2025]]
- [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]
- [[cursor]]
- [[parallel-web-systems]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C8)
