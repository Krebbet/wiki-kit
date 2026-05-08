# Letta memory blocks

Primary-source blog post from Letta — the company that productionised [[memgpt]] — defining **memory blocks** as the abstraction Letta uses for context-window management. The thesis: *"Memory blocks offer an elegant abstraction for context window management. By structuring the context into discrete, functional units, we can give LLM agents more consistent, usable memory."* Memory blocks are the user-visible primitive over the MemGPT runtime; this is the canonical source on the productionised form of MemGPT's tiered memory.

## The original MemGPT 2-block design

From the [[memgpt]] paper, two in-context blocks:

- **Human block** — user preferences, facts about them, relevant context.
- **Persona block** — agent self-concept, personality traits, behavioural guidelines.

Both were agent-editable and subject to a character limit to bound context-window allocation. Example given by the blog: agent writes *"prefers vanilla ice cream"* to the persona block to stay consistent across sessions.

## Memory block schema in Letta

Each block has:

- `label` — identifies purpose (e.g., `human`, `persona`, `knowledge`).
- `value` — string representation of block data.
- `limit` — character or token cap dictating context-window allocation.
- Optional `descriptions` — guide how the block should be used.
- `read-only` flag — if set, only the developer can modify; otherwise the agent edits via memory tools.

Blocks are individually persisted in the database with a unique `block_id`, accessible via the Letta API and the Agent Development Environment (ADE). At inference time the context window is **"compiled" from current DB state**. The prompt template is customisable via Jinja templating.

> Note on the broader Letta architecture: external Letta documentation describes a three-tier system (Core Memory / Recall Memory / Archival Memory) that maps onto MemGPT's main + recall + archival storage. This *blog post* focuses on the in-context blocks abstraction; the three-tier framing belongs to the larger Letta runtime, not this primary source. See [[memgpt]] for the underlying tiered architecture.

## Multi-agent shared memory

Described as *"one of Letta's most powerful features."* Multiple agents can share the same memory block. Three patterns named:

- **Shared knowledge bases** — multiple agents access the same reference information.
- **Sleep-time compute** — background agents update the memory of primary agents.
- **Collaborative memory** — teams of agents maintaining a shared understanding.

This is a meaningful departure from MemGPT, which assumed single-agent memory. The shared-block pattern addresses [[memory-architectures]]'s open challenge §9.6 *multi-agent memory governance* with concrete primitives — though the consensus / access-control problem the survey names is left to the developer to handle.

## Sleep-time compute

The blog cites Letta's own paper at arXiv 2504.13171. Agents process information during idle periods and write results as **"learned context"** to a shared memory block. **Cursor's background agents** are cited as a comparable external pattern. Learned context can be shared across multiple agents.

This is a distinct addition to the MemGPT lineage — not in the original 2023 paper. Worth flagging as where Letta extends MemGPT rather than just productionising it.

## Tool-based memory editing

Memory blocks are modified via memory tools or developer-defined custom tools. The blog shows an example **"rethink"** tool that replaces an entire block's value by specifying new value and target block label. Block values are strings, but complex structures (lists, dicts) can be stored as long as they serialise.

## Practical applications

Three named in the blog:

- **Personalised assistants** — human block stores user preferences, past interactions.
- **Sleep-time agents** — idle-period reflection on codebase or conversation history; learned context written to a shared block.
- **Long-running deep research agents** — 11x's deep research agent (Letta case study) used a memory block to track research state across many LLM invocations.

## Why it matters

- **Canonical primary source on the productionisation of MemGPT.** The MemGPT paper describes the runtime; this blog defines the developer-facing abstraction (`label`, `value`, `limit`, `read-only`, `block_id`) that engineers actually work with.
- **Shared-block multi-agent pattern is a concrete answer to a survey-flagged open problem.** [[memory-architectures]] §9.6 names multi-agent memory governance as unresolved; Letta's shared blocks operationalise it (with access control left to the application).
- **Sleep-time compute extends the MemGPT paradigm.** Memory updates need not happen during user-facing conversations — background agents can curate memory between interactions, mirroring Cursor's background-agent pattern. This is a pattern that does not exist in the foundational MemGPT or [[generative-agents]] papers.
- **The 11x case study** is one of the few public examples of memory-block usage for *long-running deep-research agents* — directly relevant to the [[topology-taxonomy#long-horizon-context-loss]] thread.

## Source

- `raw/research/memory-management/01-05-letta-memory-blocks.md` (captured 2026-04-26 from https://www.letta.com/blog/memory-blocks)

## Related

- [[memgpt]] — the foundational paper Letta productionises; the runtime under the memory-blocks abstraction.
- [[memory-architectures]] — survey's *hierarchical virtual context* family.
- [[mem0]] — alternative production memory library; different mechanism (extract + retrieve vs paged tiers).
- [[anthropic-memory-tool]] — Anthropic's API-level peer; both expose memory ops to the LLM but with different abstractions (memory blocks vs files).
- [[topology-taxonomy#long-horizon-context-loss]] — Letta's long-running deep-research case study is a concrete deployment of within-MAS context preservation.
