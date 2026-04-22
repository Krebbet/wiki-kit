# Agent Topology Taxonomy

Multi-agent systems vary along an orthogonal axis to the per-agent reasoning loop: **how agents connect**. The January 2026 arXiv taxonomy survey names four topologies, each with a different sweet spot and failure mode.

## The four topologies

- **Chain / waterfall** — agents pass work sequentially with fixed handoffs. Example frameworks: **MetaGPT**, **ChatDev**. Fits rigid multi-stage workflows with clear handoffs (software-engineering pipelines).
- **Star / hub-and-spoke** — a central controller dispatches to specialist workers. Example: **AutoGen**. Fits heterogeneous tool integration and human-in-the-loop oversight.
- **Mesh / swarm** — decentralized, dynamic collaboration. Fits ideation and debate — used in **MAD** (multi-agent debate) and similar.
- **Explicit workflow graphs** — typed state machines with declared transitions. Examples: **LangGraph**, **Swarm**. Fits production systems needing debuggability, checkpointing, and safety guardrails.

*(arXiv 2601.12560, 2026-01, literature-review synthesis; practitioner-consensus in current industry adoption.)*

## When each breaks

- **Chain** — a single early failure cascades downstream; no recovery path.
- **Star** — central controller is a single point of failure and a bottleneck.
- **Mesh** — task-decomposition quality degrades sharply at scale; coordination overhead swamps gains.
- **Graph** — most complex to design; still breaks on unmodeled states.

See [[failure-modes]] for more.

## The cost-depth tradeoff

Hierarchical architectures (e.g., **ReAcTree**) maximize reasoning depth but incur *exponential* token overhead relative to linear chains. This is a live constraint for any deep-tree decomposition — budget accordingly. *(arXiv 2601.12560, cited experiments.)*

## Standardization signal

**Model Context Protocol (MCP)** is named in both Anthropic's 2024–2025 writing and the 2026 arXiv taxonomy as the emerging cross-framework standard for tool discovery and governance. A rare sticky convention in a field that churns — see [[framework-skepticism#mcp-exception]]. *(Emerging, 2024–2026.)*

## Relation to Anthropic's five patterns

The Anthropic pattern vocabulary (see [[building-effective-agents]]) maps onto these topologies without conflict:

- **Orchestrator-workers** → typically **star**.
- **Prompt chaining** → **chain**.
- **Evaluator-optimizer** → either **chain** (single critic pass) or a small **mesh** (debate).
- **Routing** → a shallow **star**.
- **Parallelization** → trivial **star** with identical workers.

The taxonomy paper does not explicitly engage Anthropic's framework; this mapping is *synthesis* across sources — Claude's reading of the corpus, not a source claim.

## Source

- `raw/research/effective-agentic-patterns/08-arxiv-2601-12560-agentic-ai-taxonomy.md` — "Agentic Artificial Intelligence: Architectures, Taxonomies, and Evaluation of LLM Agents" (Arunkumar V, Anna University; Gangadharan G.R., NIT Tiruchirappalli; Rajkumar Buyya, University of Melbourne; arXiv 2601.12560, January 2026).
- `raw/research/effective-agentic-patterns/01-anthropic-building-effective-agents.md` — Anthropic engineering blog.

## Related

- [[building-effective-agents]]
- [[reasoning-frameworks]]
- [[failure-modes]]
- [[framework-skepticism]]
