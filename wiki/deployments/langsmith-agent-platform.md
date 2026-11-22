# LangSmith Agent Platform (agent-as-core-object)

LangChain's November 2026 rebuild of LangSmith (announced alongside its Series C) makes a registered **agent record** — named owner, globally unique immutable ID, type — the core object that ties together environments, traces, evals, deployments and failure analysis ("Engine"). Any agent emitting OTLP can be registered, including third-party vendor agents, to address "agent sprawl". Vendor-primary architecture claims; no measured results.

## Key points

- **Data-model shift:** traces formerly sat in a flat project hierarchy with no agent link; now one record groups local/dev/staging/prod, traces, evals, Agent Server deployments and Engine issues.
- **Typed agents:** type selects dashboards, data connections and eval criteria. Shipped: *general purpose* and *coding* (merged PRs, token cost, GitHub connection); *voice* on roadmap.
- **Governance of third-party agents:** OTLP ingestion (e.g. ServiceNow, Glean, hyperscaler-hosted agents); cost/quality roll up per agent; a named owner answers cost spikes.
- **Composable:** observability/governance only, or end to end (Studio builder, Agent Server, LLM Gateway, registry). Engine can validate a fix against an Agent Server preview before merge. Cloud, BYOC, self-hosted.
- **Roadmap (unshipped):** more types, org-level dashboards, registering agents in a customer identity provider so security can audit them like other identities.
- **Caveat:** vendor positioning tied to a funding announcement; collect-but-confirm.

## Source

- `raw/research/weekly-2026-11-22/01-langsmith-rebuilt-around-agent.md` — langchain.com/blog/we-rebuilt-langsmith-around-the-agent (captured 2026-11-22).

## Related

- [[patterns/agent-development-lifecycle]] — lifecycle now keyed on an agent record
- [[patterns/langsmith-tuned-evaluators]] — same vendor's eval philosophy
- [[deployments/microsoft-agent-365]] — parallel registry/governance plane (Entra identity vs immutable ID + OTLP)
- [[coding-agents/langchain-deep-agents]] — open-source harness underneath
- [[patterns/sierra-monitor-eval-of-evals]] — monitor/improve-phase counterpart (build vs buy)
- [[deployments/mcp-infrastructure]] — agent identity as a named priority; parallels the identity-provider roadmap item
