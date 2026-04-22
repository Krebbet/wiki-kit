# Reasoning Frameworks: Single-Agent → Tool-Based → Multi-Agent

The August 2025 arXiv reasoning-frameworks survey organizes agentic systems along a **capability tier** — how the per-agent cognitive loop scales. Complementary to the [[topology-taxonomy]] (how agents are wired) and the [[building-effective-agents|Anthropic patterns]] (what the overall system does).

## Tier 1 — single-agent

Pure prompt-engineered scaffolding on one model. Named techniques:

- **Role-playing, environment simulation, task description, in-context learning** — all prompt-side levers. *(Practitioner-consensus.)*
- **Self-improvement** loops: reflection (**Reflexion**, Shinn et al. 2023), iterative optimization (**Self-Refine**), interactive learning.

Survey caveats: role-playing biases fact-based QA; verbosity sensitivity varies by model. *(Practitioner-consensus.)*

## Tier 2 — tool-based

Three sub-stages:

1. **Integration** — API-based, plugin-based, or middleware.
2. **Selection** — autonomous zero-shot, rule-based, or learning-based. Autonomous selection is fragile when tool descriptions are ambiguous.
3. **Utilization** — sequential, parallel, or iterative invocation.

Canonical techniques:

- **ReAct** (Yao et al. 2022) — interleaved reasoning + action traces.
- **Reflexion** (Shinn et al. 2023) — verbal self-feedback loops.
- **Self-Refine** — iterate on own output.
- **CRITIC** — externally-grounded critique before revision.
- **MCP-Zero** — tool discovery via the Model Context Protocol.

## Tier 3 — multi-agent

Architectural shapes (cross-ref [[topology-taxonomy]]): **centralized** (single point of failure), **decentralized** (resource inefficient), **hierarchical** (best for high-complexity decomposition, worst for cost).

Interaction protocols: **cooperation**, **competition**, **negotiation**. Representative systems: **MetaGPT** (hierarchical), **AutoGen** (multi-agent conversations), **MAD** (multi-agent debate).

## Emerging — reasoning models internalize inference-time search

Reasoning-trained frontier models (**OpenAI o1**, **o3**, **GPT-5**, **Gemini 3 Pro**, and the 2025–2026 Claude reasoning generation) internalize chain-of-thought and inference-time search within a single model call. This collapses some multi-agent architectures: a single o1-class call can subsume what required an explicit evaluator-optimizer loop a year earlier. *(arXiv 2601.12560, 2026-01; practitioner-consensus; emerging.)*

Implication worth testing on your own workloads before committing to multi-agent scaffolds.

## Emerging — skill libraries

**Voyager** (Wang et al. 2023, Minecraft-benchmarked) demonstrated **skill libraries** — persistent, non-parametric accumulation of validated behaviors. The arXiv taxonomy highlights this as an alternative to fine-tuning that avoids catastrophic forgetting. *(Tested on Minecraft, not broader; practitioner-consensus on the pattern's value.)*

## Emerging — SLM-default heterogeneous architectures

NVIDIA's June 2025 position and the October 2025 SLM-agentic-systems survey converge on fine-tuned small models (1–12B) as the right *default* component for agent calls, with LLMs as fallback. Enabled by guided decoding and validator-first execution. See [[slm-agents]]. *(Position paper + empirical survey; emerging.)*

## Emerging — agentic context engineering

Beyond prompt-based scaffolding, structured context-evolution frameworks (notably **ACE**, Zhang et al. 2025-10) accumulate playbooks via generation / reflection / curation, with benchmark gains rivaling fine-tuning on multi-turn agent tasks. See [[agentic-context-engineering]]. *(Tested on a single paper's benchmark suite; no third-party replication yet.)*

## Fine-tuning angle

Originally documented here as an open corpus gap. The April 2026 `fine-tuning-vs-context-slms` research run substantially answered it — see [[fine-tuning-vs-context-engineering]] for the decision framework. Remaining sub-gaps in [[ft-vs-context-engineering]].

## Source

- `raw/research/effective-agentic-patterns/09-arxiv-2508-17692-agentic-reasoning-survey.md` — "LLM-based Agentic Reasoning Frameworks: A Survey from Methods to Scenarios" (Bingxi Zhao et al., Beijing Jiaotong / Lancaster / Max Planck / UESTC; arXiv 2508.17692, August 2025).
- `raw/research/effective-agentic-patterns/08-arxiv-2601-12560-agentic-ai-taxonomy.md` — for multi-agent architecture names and reasoning-model framing.
- `raw/research/effective-agentic-patterns/01-anthropic-building-effective-agents.md` — for the augmented-LLM baseline cross-reference.

## Related

- [[building-effective-agents]]
- [[topology-taxonomy]]
- [[fine-tuning-vs-context-engineering]]
- [[slm-agents]]
- [[agentic-context-engineering]]
- [[context-engineering]]
- [[failure-modes]]
