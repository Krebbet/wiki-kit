# Context Engineering

Context engineering is the systematic optimization of the information payload delivered to an LLM — reframing what used to be called "prompt engineering" as a discipline concerned with the structure, retrieval, assembly, and management of the context window, rather than the crafting of a single string. Codified as a formal field by the July 2025 arXiv survey that reviewed 1,400+ papers.

## Formalization

The survey defines context as a structured composition

> **C = {c_instr, c_know, c_tools, c_mem, c_state, c_query}**

— instruction, knowledge, tool interfaces, memory, dynamic state, user query — assembled by a higher-level function, not a monolithic prompt. *(arXiv 2507.13334, 2025-07; literature-review synthesis.)*

## Three foundational components

- **Context retrieval & generation** — prompt engineering, external knowledge acquisition via RAG, dynamic context assembly.
- **Context processing** — long-sequence handling, self-refinement, multimodal integration, structured data (knowledge graphs, tables).
- **Context management** — memory hierarchies, context compression, token-budget optimization.

## Integrated system implementations

- **RAG** — modular, agentic, and graph-enhanced variants. See [[building-effective-agents#the-augmented-llm-baseline|augmented-LLM baseline]].
- **Memory systems** — hierarchical (MemGPT-style paging), episodic, short / long-term.
- **Tool-integrated reasoning** — function calling. Three *coexisting* methodologies: prompt-based (no training), supervised fine-tuning (imitation), reinforcement learning (reward-driven).
- **Multi-agent systems** — see [[topology-taxonomy]].

## Known limitation — comprehension-generation asymmetry

The survey's most-emphasized failure mode: **models understand complex contexts well but generate equally sophisticated long-form outputs poorly.** Cited: GAIA shows 15% model accuracy vs 92% human on tool-integrated reasoning. Root cause unclear — architecture, training, or fundamental limit. *(Evidence class: survey synthesis, documented mechanism, open root cause.)*

Related: **middle-token loss** — accuracy degrades when relevant information sits mid-sequence in long contexts.

## Empirical gains cited (from surveyed primary papers)

- 18-fold enhancement in text navigation; 94% success rates.
- Few-shot: +9.90% BLEU-4 on code summarization; +175.96% exact-match on bug-fix.
- AIME2024: 26.7% → 43.3% via cognitive prompting.

*(Cited from primary sources the survey reviews; the survey does not reproduce experiments.)*

## Memory: deep-dive companion

The `c_mem` component gets a more thorough treatment in [[memory-architectures]] — write-manage-read loop, five mechanism families, four evaluation benchmarks, ten open challenges. Three concrete 2026 instances live in the wiki: [[codified-context]] (hierarchical virtual context, hand-engineered), [[context-folding]] (context-resident compression, learned), [[cognitive-fabric-nodes]] (memory lifted out of agents into the network substrate). [[agents-md-eval]] adds empirical counter-evidence on the *retrieval/generation* axis: in well-documented Python repos, naive context-file injection often *hurts* coding-agent success rate.

## Cost structure — a live constraint

Quadratic O(n²) attention complexity. Mistral-7B requires 122× more compute going from 4K → 128K tokens. *(Cited, 2025.)* Long-context is not free.

## Relation to fine-tuning

The survey explicitly frames context engineering and fine-tuning as **complementary, not substitutes**. See [[fine-tuning-vs-context-engineering]] for the decision framework synthesized across five sources.

## Source

- `raw/research/fine-tuning-vs-context-slms/03-arxiv-2507-13334-context-engineering-survey.md` — "A Survey of Context Engineering for Large Language Models" (Lingrui Mei, Jiayu Yao, Yuyao Ge, Jiafeng Guo, Shenghua Liu et al., Institute of Computing Technology / Chinese Academy of Sciences; arXiv 2507.13334, July 2025).

## Related

- [[fine-tuning-vs-context-engineering]]
- [[agentic-context-engineering]]
- [[building-effective-agents]]
- [[reasoning-frameworks]]
- [[failure-modes]]
- [[memory-architectures]] — deep-dive on the `c_mem` component.
- [[codified-context]], [[context-folding]], [[cognitive-fabric-nodes]] — three 2026 instances of context-management mechanisms.
