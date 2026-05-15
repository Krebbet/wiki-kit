# Memory architectures for LLM agents

Survey synthesis of how memory is designed, implemented, and evaluated across LLM-based agents from 2022 through early 2026. The paper formalises agent memory as a **write–manage–read loop** tightly coupled with perception and action (memory plays the role of belief state in a POMDP-style cycle), and organises the design space along a three-dimensional taxonomy: **temporal scope**, **representational substrate**, and **control policy**. Five mechanism families are surveyed in depth, four recent benchmarks are flagged as exposing stubborn gaps, and the survey closes with ten open challenges. The headline takeaway: "the gap between 'has memory' and 'does not have memory' is often larger than the gap between different LLM backbones — investing in memory architecture can yield returns that rival or exceed model scaling."

## The write–manage–read loop

At each step the agent **reads** from memory to inform its action, then **writes/manages** memory as a result — with the manage step performing "summarize, deduplicate, score priority, resolve contradictions, and — when appropriate — delete." This formalism positions memory not as a passive store but as an active loop that runs alongside perception and action; the design choices live in *what* gets written, *how* it's organised, and *which* policy governs read/write/forget.

## Five mechanism families

1. **Context-resident compression** — keeps all memory inside the prompt via sliding windows, rolling summaries, hierarchical summaries, or task-conditioned compression. Paradigm example: Self-Controlled Memory (Liang et al. 2023). Core pathologies: *summarization drift* and *attentional dilution* ("lost in the middle"). [[context-folding]] (AgentFold) is a 2026 instantiation of this family with adaptive granularity. [[claude-code-session-memory]] is a product-layer instance — automated background extraction + summary injection.

2. **Retrieval-augmented memory stores** — populates a non-parametric external index with live interaction records (tool logs, observations, corrections) and queries it at inference time. Key systems: RAG (Lewis 2020), RETRO (Borgeaud 2022), RET-LLM (Sun 2024), Self-RAG (Asai 2024). Bottleneck has shifted from storage to *retrieval quality*. [[mem0]] (2025) is the production library that operationalises selective retrieval at scale (1.4K avg retrieval tokens vs 26K full-context on LOCOMO; 92% p95 latency reduction). [[mempalace]] (2026) is a doctrinal counter-position in the same family — verbatim drawers + ChromaDB cosine + metadata-scoped wings/rooms/halls/closets — applying a "never summarise" discipline where Mem0 extracts and consolidates. The verbatim-vs-extraction split is documented at [[conflicts/verbatim-vs-extracted-memory]]. **2026-05-11 addition:** [[direct-corpus-interaction]] (arXiv 2605.05242) is a *no-index extreme* in the same family — agents search the raw corpus directly via terminal tools (`grep` / `rg`) with no embedding model and no retrieval API. +11 pp accuracy and −29.4% cost on BrowseComp-Plus with matched Sonnet 4.6, with the gain coming from *within-document localisation* rather than recall. Pressures the family-defining assumption that *some form* of indexed retrieval is necessary; see [[conflicts/verbatim-vs-extracted-memory]] for the resulting three-way conflict and the new "Index existence" reconciling axis.

3. **Reflective and self-improving memory** — agent writes natural-language post-mortems or higher-order reflections after task attempts. The two foundational papers are [[reflexion]] (Shinn 2023; verbal RL with episodic buffer) and [[generative-agents]] (Park 2023; memory stream + recency × importance × relevance retrieval scoring formula — the canonical scheme adopted by most subsequent systems). Other systems: ExpeL (Zhao 2024), Think-in-Memory (Liu 2024). Core risk: *self-reinforcing error* and over-generalisation. [[agentic-context-engineering]] (ACE, 2025) extends the pattern to context engineering itself.

4. **Hierarchical virtual context management** — borrows OS virtual-memory paging: a main context (RAM), a searchable recall database (disk), and a cold vector archive, managed via explicit memory-operation function calls. The foundational paper is [[memgpt]] (Packer et al. 2023; the LLM-as-OS framing); [[letta-memory-blocks]] is the production runtime built on it. Anthropic ships the same paradigm as a vendor primitive: [[anthropic-memory-tool]] exposes six file-system commands (view/create/str_replace/insert/delete/rename) over a `/memories` directory with an auto-injected MEMORY PROTOCOL ("ASSUME INTERRUPTION") system prompt. [[codified-context]]'s hot/cold tiering is a hand-engineered application-layer instance. Extended by JARVIS-1 (Wang 2024) for multimodal settings. Core risk: *silent orchestration failure* ("memory blindness").

5. **Policy-learned memory management** — treats store/retrieve/update/summarize/discard as callable tools within the agent policy and optimises end-to-end via RL. Paradigm system: Agentic Memory / AgeMem (Yu 2026) using three-stage RL with step-level GRPO. Discovers non-obvious tactics like preemptive summarization; concerns include training cost, learned forgetting of safety-critical records, and poor transfer across task distributions. **2026-05-11 addition:** [[skillos]] (arXiv 2605.06614, May 2026) is the new substantial public-benchmark instance in this family — frozen executor + RL-trained curator emitting `insert_skill` / `update_skill` / `delete_skill` calls over an external Markdown SkillRepo, trained with GRPO over **grouped task streams** so that early skill edits are evaluated by their effect on later related tasks. +5.5 to +13.8 pp absolute SR on ALFWorld across executor scales; +7.1 pp cross-family transfer; the **8B-RL-trained curator beats Gemini-2.5-Pro-as-curator-without-RL** — executor-grounded training matters more than curator scale.

(The survey also covers a sixth family — *parametric/weight-based memory* via fine-tuning and adapters — but treats it as secondary.)

## Evaluation: four benchmarks exposing stubborn gaps

- **LoCoMo** (Maharana et al. 2024) — up to 35 sessions, 300+ turns; tests factual QA, event summarisation, dialogue generation; exposes failure on temporal and causal dynamics.
- **[[longmemeval]]** (Wu et al. 2025, ICLR) — 500 questions covering five abilities (information extraction, multi-session reasoning, knowledge updates, temporal reasoning, abstention); standard sizes ~115k and ~1.5M tokens; commercial assistants drop 30–60% relative to offline reading of the same content. The only peer benchmark covering knowledge updates.
- **MemBench** (Tan et al. 2025) — distinguishes factual vs. reflective memory in participation vs. observation modes; metrics across effectiveness, efficiency, and capacity.
- **MemoryAgentBench** (Hu et al. 2025) — four cognitive competencies: accurate retrieval, test-time learning, long-range understanding, selective forgetting. Survey's note: "no current system masters all four."
- **MemoryArena** (He et al. 2026) — embeds memory inside complete agentic tasks (web nav, preference-constrained planning, sequential formal reasoning). Most striking finding: models scoring near-perfectly on LoCoMo plummet to 40–60% on MemoryArena, exposing "a deep gap between passive recall and active, decision-relevant memory use."

The MemoryArena delta is the cleanest empirical signal in the survey that *static recall benchmarks substantially overstate* an agent's ability to use memory in live task settings — the same general pattern [[swe-bench-pro]] documents for code benchmarks vs. real production conditions.

## Open challenges (Section 9)

- **Principled consolidation** — balance hoarding vs. amnesia; analogous to hippocampal sleep-replay; estimating importance without future-sight; guaranteeing safety-critical records survive.
- **Causally grounded retrieval** — semantic similarity answers "what looks like this?" not "what caused this?"; hybrid retrievers blending similarity, temporal ordering, causal graph traversal, and counterfactual relevance "remain largely unexplored."
- **Trustworthy reflection** — self-reflection can entrench mistakes; needs external validation, uncertainty quantification, adversarial probing, expiration policies.
- **Learning to forget** — selective forgetting under safety and compliance constraints; connections to machine unlearning when memories have influenced model weights.
- **Multimodal and embodied memory** — fusing text, vision, audio, proprioception, tool state.
- **Multi-agent memory governance** — access control over shared stores, consensus for concurrent writes, knowledge transfer between specialisations. *(See [[cognitive-fabric-nodes]] for one architectural answer that lifts memory out of individual agents and into the network layer.)*
- **Memory-efficient architectures** — sparse retrieval, compressed session vectors, memory-native architectures (Recurrent Memory Transformers).
- **Foundation models for memory management** — a task-agnostic memory controller trained across diverse agent tasks; AgeMem is a first step.
- **Standardised evaluation** — "The field still lacks a community-standard evaluation harness... A GLUE-style shared leaderboard for agent memory would substantially accelerate progress."

## Application domains the survey calls out

- **Coding agents** (§6.2) — distinguishing challenge is *structural scale*: indexing and retrieving relevant portions of a codebase spanning thousands of files. ChatDev, MetaGPT cited as instances using shared standardised documents as persistent memory. Maps onto [[codified-context]].
- **Multi-agent teamwork** (§6.5) — AutoGen, CAMEL, ProAgent; role-based access control to shared stores flagged as an unsolved design gap. See [[topology-taxonomy]].
- **Tool-use and API orchestration** (§6.6) — schema drift, version tracking, "living versioned catalog of tool capabilities." Connects directly to [[mcp-infrastructure]]'s async-task-lifecycle gap.
- **Scientific reasoning** (§6.4) — hypothesis ledgers and uncertainty-aware memory; resonates with [[ai-scientist-v2]]'s node-tuple state representation.

## Why it matters

- **Vocabulary backbone for the wiki.** The three-axis taxonomy and five-family decomposition give every other page a stable referent — *which mechanism family*, *which axis* — rather than each design being described in its own ad-hoc terms.
- **Calibrates the model-vs-architecture debate.** The headline pull-quote ("memory architecture can yield returns that rival or exceed model scaling") is a concrete contribution to the [[measurement-vs-architecture]] argument.
- **Names the recall-vs-use gap.** MemoryArena's 40–60% drop on agentic tasks (vs near-perfect on LoCoMo) is the cleanest current empirical evidence that benchmark scores on passive recall are not predictive of decision-relevant memory use.

## Source

- `raw/research/long-horizon-context/02-02-memory-survey.md` (captured 2026-04-25 from https://arxiv.org/abs/2603.07670)

## Related

- [[topology-taxonomy#long-horizon-context-loss]] — memory architecture is the orthogonal axis to topology that determines whether long-horizon context survives.
- [[context-engineering]] — broader six-component context formalism (`C = {c_instr, c_know, c_tools, c_mem, c_state, c_query}`); this page deep-dives the `c_mem` component the survey treats more briefly.
- [[agentic-context-engineering]] — ACE's generate-reflect-curate playbook is a 2025 instance of *reflective and self-improving memory*.

**Foundational papers (added 2026-04-26):**
- [[memgpt]] — *hierarchical virtual context* foundation paper (Packer et al. 2023).
- [[reflexion]] — *reflective and self-improving memory* foundation paper (Shinn et al. 2023).
- [[generative-agents]] — companion foundation paper for reflective memory; the canonical recency × importance × relevance retrieval scoring formula (Park et al. 2023).

**Production / vendor instances:**
- [[mem0]] — production library for *retrieval-augmented memory stores*; LOCOMO benchmarks vs MemGPT/Zep/LangMem/OpenAI memory.
- [[mempalace]] — 2026 local-first library; verbatim-storage discipline (the doctrinal counter to Mem0's extract-and-consolidate). Wings/rooms/halls/closets/drawers metaphor over ChromaDB + SQLite KG. See [[conflicts/verbatim-vs-extracted-memory]].
- [[letta-memory-blocks]] — production runtime built on MemGPT; memory-blocks abstraction + sleep-time compute extension.
- [[anthropic-memory-tool]] — Claude API vendor primitive; six file-system commands over `/memories` + auto-injected MEMORY PROTOCOL ("ASSUME INTERRUPTION").
- [[claude-code-session-memory]] — Claude Code product-layer; automated background extraction + cross-session summary injection.

**Benchmarks with their own pages:**
- [[longmemeval]] — ICLR 2025; the benchmark MemPalace's headline number is graded against, with recommended index designs (round-granularity values, fact-augmented key expansion, time-aware query expansion).

**Related applications:**
- [[codified-context]] — hand-engineered application-layer instance of *hierarchical virtual context*.
- [[context-folding]] — AgentFold is a 2026 instance of *context-resident compression* with adaptive granularity.
- [[cognitive-fabric-nodes]] — proposes lifting memory out of individual agents into the network layer; addresses the *multi-agent memory governance* open challenge.
- [[ai-scientist-v2]] — node-tuple state pattern is a manual instantiation of memory in a research-agent setting.
- [[mcp-infrastructure]] — async-lifecycle gap is the protocol-level expression of the survey's tool-orchestration memory problem.

## Reading path for newcomers

A four-paper minimum to navigate the cluster: this survey → [[memgpt]] (hierarchical virtual context, the dominant production paradigm) → [[mem0]] (retrieval-augmented stores, the latency/cost-optimised peer) → [[anthropic-memory-tool]] (the API-level vendor primitive) → [[conflicts/verbatim-vs-extracted-memory]] (the live three-way disagreement). Add [[reflexion]] + [[generative-agents]] for the 2023 foundational layer; add [[longmemeval]] for the indexing/retrieval/reading vocabulary used to compare systems on the same axis.

**Picking by use-case** (synthesised across the family pages):

| If you need… | Read |
|---|---|
| Exact-words recall, citation grounding, audit trails | [[mempalace]] (verbatim discipline) |
| Multi-session reasoning at scale, 90% latency reduction | [[mem0]] (extract + consolidate) |
| Multi-agent shared memory + sleep-time compute | [[letta-memory-blocks]] |
| Vendor-supported primitive on the Claude API (ZDR-eligible) | [[anthropic-memory-tool]] |
| Cross-session continuity inside Claude Code | [[claude-code-session-memory]] |
| Application-layer hot/cold tiering for a large codebase | [[codified-context]] |
| RL-trained skill curation (frozen executor) | [[skillos]] |
| No-index, terminal-tool corpus search | [[direct-corpus-interaction]] |

The three retrieval-augmented systems ([[mem0]], [[mempalace]], [[direct-corpus-interaction]]) sit in direct doctrinal tension; [[conflicts/verbatim-vs-extracted-memory]] is the page that catalogues the disagreement and the (currently speculative) reconciling axes.

## Externalization framing (Zhou et al. 2026)

The [[externalization-survey]] (arXiv 2604.08224) reframes memory as one of four coupled externalizations (memory + skills + protocols + harness) with a four-content-type decomposition — *working context*, *episodic experience*, *semantic knowledge*, *personalised memory* — more granular than this page's three-axis taxonomy but mapping cleanly onto it. The survey's memory chapter (§3) uses Du 2026's four-paradigm taxonomy (monolithic context → context+retrieval → hierarchical memory & orchestration → adaptive memory systems), which aligns one-to-one with this page's five mechanism families. See [[externalization-survey]] for the cross-cutting framing across memory + skills + protocols + harness; this page remains the focused memory survey.

Two new memory-adjacent instances surfaced the week of 2026-05-04:

- **[[agentic-harness-engineering]]'s `LongTermMEMORY.md`** — machine-evolved persistent cross-session knowledge; instance of the *episodic + structured working memory* family, with the twist that the contents are now machine-evolved rather than human- or runtime-agent-authored. AHE's component-ablation finding (+memory only +5.6 pp; +system_prompt only −2.3 pp) is the cleanest empirical isolation to date of *which* externalization carries the lift in coding-agent harnesses.
- **[[notion-token-town]]'s "memory is just pages and databases"** — primitive-composition data point: Notion deliberately *does not* invent a memory primitive for its Custom Agents. *"If you wanna give a memory, just give it a page and give it edit access to that page."* Same for inter-agent communication: agents file issues into a shared "issues" database that a manager agent reads. Sits adjacent to the dedicated-memory-primitive lineage (MemGPT, Letta, Mem0, MemPalace) as a counter-design that says: the dedicated primitive may not be necessary if the existing data primitives can carry the semantics.
