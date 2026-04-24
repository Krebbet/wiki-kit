# Trace

London-based YC Summer 2025 startup building a **knowledge-graph + context-engineering layer** that onboards AI agents into existing corporate tools (email, Slack, Airtable, Jira) and orchestrates mixed human/agent workflows from high-level prompts. $3M seed announced 2026-02-26.

**Tier:** startup (seed stage). **Stub — single-source page; thin evidence of working deployments.**

## What it does

Workflow-orchestration layer for enterprises. Maps a company's tools and processes into a knowledge graph, then takes a high-level prompt ("design a new microsite", "develop our 2027 sales plan") and returns a step-by-step workflow that delegates sub-tasks to AI agents or human workers, feeding each agent the specific context it needs (TechCrunch 2026-02-26).

## Techniques under the hood

- **Knowledge graph** constructed from existing enterprise systems — source names email, Slack, Airtable explicitly.
- **"Context engineering"** framed as the core thesis — feeding the right data into each agent sub-call at the right time.
- CTO Artur Romanov: *"2024 and 2025 was still about prompt engineering. Now we've moved from prompt engineering to context engineering. Whoever provides the best context at the right time is going to be the infrastructure on top of which the AI-first companies will be built."*
- No model details disclosed; Trace appears to sit **above** foundation-model providers (model-agnostic orchestration), not train its own.

## Deployment model

SaaS. Integrates into existing corporate workplace tools. London HQ. No on-prem / VPC claims in source. *Re-check before quoting.*

## Customization hooks

The knowledge graph itself is the customisation surface — shaped by the customer's own tool graph. Source does not describe explicit config / policy / persona hooks.

## Running costs

Not specified in source.

## Hard limits

Not specified in source.

## Market reception (2026-02-26)

- **$3M seed** from **Y Combinator, Zeno Ventures, Transpose Platform Management, Goodwater Capital, Formosa Capital, WeFunder**; angels Benjamin Bryant and Kevin Moore.
- **YC Summer 2025** cohort.
- **London-based.** **CEO Tim Cherkasov**, **CTO Artur Romanov**.
- No customer names, revenue, or deployment counts disclosed.

## Hype-vs-reality delta

Seed-stage; the pitch is crisp but source provides **zero independent evidence** of working deployments, integration depth, or graph quality. "Knowledge graph from email / Slack / Airtable" is a hard problem at scale (staleness, permissions, entity resolution) and the article doesn't probe it. Treat as a **thesis bet, not a proven product**.

## Techniques worth stealing

- **Persistent company-specific knowledge graph first, then agent invocation = context-retrieval problem against that graph** — inversion of the prompt-engineering frame.
- **"Manager that knows where to put the interns"** — positioning the orchestration layer between frontier-lab agents and enterprise workflows instead of competing with the labs directly. Useful pattern for any infra-tilted agent-platform play.

## Build-vs-buy signals

Trace explicitly positions itself as **infrastructure sitting between the labs' "brilliant interns"** (Cherkasov's phrase for OpenAI / Anthropic enterprise agents) **and actual enterprise workflows**. The competitive pressure is real and specifically named in the source:

- **Anthropic's enterprise-plugin push** (launched same week, 2026-02-24) — attacks from above with pre-built departmental plug-ins.
- **Atlassian Jira's native agents** (2026-02-25) — attacks from below as the workplace tools Trace wants to orchestrate grow their own agent layers.

**Buy-signal only holds if Trace's graph + orchestration is meaningfully better than what incumbents will bundle for free** — not demonstrated in this source.

## Reader notes

- Single-source TechCrunch funding announcement — vendor-PR-adjacent. All product claims are founder quotes.
- Source places Trace squarely in the [[ai-apps-layer-2026]] "narrow startups / every-team-software" thesis: it's an orchestration layer betting on the apps-vs-models divergence. Does not help resolve [[open-questions-2026-04]] C1 or C8 directly — too early-stage.
- Ingest batch context: appeared in the 2026-04-22 "emerging agentic startups" research run alongside HN practitioner threads that are much more skeptical about generic agent orchestration; [[agents-eating-saas]] notes the CAPTCHA / distribution / trust bottlenecks that any such layer inherits.

## Source

- `raw/research/emerging-agentic-startups-2026/02-techcrunch-trace-seed.md`

## Related

- [[ai-apps-layer-2026]]
- [[ai-app-categories-2025]]
- [[agents-eating-saas]]
- [[lio]]
- [[open-questions-2026-04]]
