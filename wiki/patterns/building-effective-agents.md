# Building Effective Agents

Anthropic's December 2024 engineering piece codified what has become the default vocabulary for LLM-application design. It distinguishes **workflows** (LLMs and tools orchestrated through predefined code paths) from **agents** (systems where the LLM dynamically directs its own process and tool usage), and recommends starting from the simplest viable solution — introducing agentic complexity only when it measurably pays off.

## The augmented-LLM baseline

The foundational building block is the **augmented LLM** — a model with tool use, retrieval, and memory, actively generating its own search queries, selecting tools, and deciding what to retain. Everything above this is a composition of augmented LLMs. *(Anthropic 2025, practitioner-consensus.)*

## The five patterns

Five composable patterns make up the workflow vocabulary:

- **Prompt chaining** — sequential decomposition; each step consumes the prior step's output. Optional programmatic gates between steps. Fits when the decomposition is known and stable.
- **Routing** — classify input and dispatch to the appropriate downstream pipeline. Fits when different query classes warrant different handling.
- **Parallelization** — run multiple LLM calls concurrently and aggregate. Either *sectioning* (independent subtasks) or *voting* (multiple passes for reliability).
- **Orchestrator-workers** — a coordinator LLM dynamically decomposes a task and delegates to worker LLMs. Fits open-ended problems where subtask count cannot be hardcoded.
- **Evaluator-optimizer** — an evaluator LLM critiques an optimizer LLM's output; iterate. Fits quality-bound tasks with clear evaluation criteria.

**Agents** (as distinguished from workflows) are LLMs using tools in a loop with environmental feedback, steering themselves. Fit open-ended, high-variance tasks where human oversight still applies. *(Practitioner-consensus.)*

## Design emphasis: the agent-computer interface (ACI)

Anthropic treats tool definitions and documentation as first-class design work, on par with the human-computer interface. Concrete tested prescriptions:

- Absolute filepaths over relative.
- Diffs over full rewrites.
- Formats chosen to minimize the LLM's effort, not the programmer's.

*(Evidence class: tested — cited as SWE-Bench-level improvements from ACI work on Anthropic's customer deployments.)*

## Scope limits

Does not address fine-tuning, domain-specific evaluation design, or enterprise-data integration. Treats the framework-vs-direct-API choice as decided (direct API preferred — see [[framework-skepticism]]).

## Source

- `raw/research/effective-agentic-patterns/01-anthropic-building-effective-agents.md` — Anthropic engineering blog, authors Erik Schluntz and Barry Zhang. Lab blog: flagged as primary but marketing-tainted.
- `raw/research/effective-agentic-patterns/02-anthropic-cookbook-agents.md` — reference implementations (Jupyter notebooks) for the five patterns.

## Related

- [[topology-taxonomy]] — orthogonal axis: how agents are wired together
- [[reasoning-frameworks]] — orthogonal axis: per-agent cognitive scaffolding
- [[framework-skepticism]] — why Anthropic prefers direct API over frameworks
- [[measurement-vs-architecture]] — the counter-thesis: evaluation outweighs pattern choice
