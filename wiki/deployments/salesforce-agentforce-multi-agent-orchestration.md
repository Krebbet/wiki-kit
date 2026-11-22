# Salesforce Agentforce Multi-Agent Orchestration

Salesforce vendor blog (GA announcement, collected 2026-11-22) arguing enterprises progress from a monolithic agent to domain specialists to a **front-door orchestrator** that decomposes requests, routes each part to a subagent by description, and consolidates the answers. Adds **Agent Script** (declared deterministic routing for mission-critical flows) and turn-level **session tracing**. Pure vendor marketing: no benchmarks, architecture detail or code — collect-but-confirm.

## Key points

- **Three-stage narrative:** monolith (instruction bloat, misrouting) → specialists (users must pick agents, repeat themselves at handoffs) → orchestrator.
- **Routing:** description-driven LLM inference by default; Agent Script lets builders pin the path where "95% reliability isn't good enough" (returns, compliance). A hybrid deterministic/probabilistic split.
- **Observability:** Agentforce Observability traces every multi-agent turn (which agent, where routed, why) to debug handoff failures.
- **Roadmap (pilot):** orchestration over A2A-compliant third-party agents (Google, AWS).
- **Unmeasured:** monolith degradation and routing-accuracy claims are asserted only.

## Source

- `raw/research/weekly-2026-11-22/02-salesforce-multi-agent-orchestration.md` — salesforce.com/blog/multi-agent-orchestration (captured 2026-11-22).

## Related

- [[patterns/topology-taxonomy]] — orchestrator topology and handoff failure modes
- [[patterns/agent-communication-protocols]] — A2A interoperability item
- [[deployments/anthropic-dynamic-workflows]] — lead agent designs its own topology (dynamic) vs declared routing (static)
- [[deployments/anthropic-commerce-agents]] — single loop + skills contrast
- [[patterns/sierra-context-engineering]] — deterministic/probabilistic hybrid parallel
- [[deployments/microsoft-agent-365]] — another cross-vendor governance plane
- [[deployments/langsmith-agent-platform]] — same-week agent-registry/governance launch
