# Mem0: Production-ready scalable long-term memory

Mem0 paper (Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav; arXiv 2504.19413, 2025) backing the popular `mem0` open-source library (47k+ GitHub stars per third-party trackers as of early 2026). The gap targeted: fixed context windows force LLMs to "reset" between sessions, and even very large contexts (200K–10M tokens) merely *delay* the problem. Two sub-problems are called out: (a) conversations eventually exceed any context limit over weeks/months of use; (b) full-context processing forces the model to reason through irrelevant material, degrading retrieval quality and inflating latency/cost. [[memgpt]] addresses this via OS-style tiered paging but does not compress memories into efficient representations; raw RAG retrieves text chunks and preserves noise. Mem0's claim: dynamically extract and consolidate only salient facts, enabling selective retrieval that maintains near-full-context answer quality at **91% lower p95 latency and >90% lower token cost** on the LOCOMO benchmark.

## Architecture — base Mem0

Two-phase incremental pipeline triggered on each new message pair `(m_{t-1}, m_t)`:

**Extraction phase**: Builds prompt `P = (S, {m_{t-m},...,m_{t-2}}, m_{t-1}, m_t)` where `S` is an asynchronously refreshed conversation summary (global context) and the recent `m=10` messages provide granular temporal context. An LLM (GPT-4o-mini in experiments) runs an extraction function `φ(P) → Ω`, a set of candidate salient facts.

**Update phase**: For each candidate fact `ω_i`, retrieve the top `s=10` semantically similar existing memories via vector embeddings. Pass candidate + retrieved memories to the LLM via a function-calling interface. The LLM selects one of four operations:
- **ADD** — no semantically equivalent memory exists.
- **UPDATE** — augment existing memory with complementary info.
- **DELETE** — new info contradicts existing.
- **NOOP** — no change needed.

Vector database stores dense embeddings for similarity search.

## The graph variant — Mem0g

Mem0g represents memories as a directed labelled graph `G = (V, E, L)`: nodes are entities (e.g., Alice, San_Francisco), edges are relationships (e.g., `lives_in`), labels assign semantic types (Person, City).

**Two-stage extraction**: (1) entity extractor identifies key entities with types; (2) relationship generator derives `(source, relation, destination)` triplets via LLM with function calling. Both use GPT-4o-mini.

**Storage / update**: new triplets are embedded; source and destination entities matched against existing nodes by semantic similarity threshold. A conflict-detection mechanism identifies potentially obsolete relationships; an LLM-based update resolver marks them invalid (rather than deleting) to preserve temporal reasoning.

**Retrieval (dual-mode)**:
1. **Entity-centric** — identify key entities in query, locate matching nodes, traverse incoming/outgoing relationships to build a subgraph.
2. **Semantic triplet** — encode full query as a dense vector, score against all triplet text encodings, return those above a relevance threshold.

Backend: Neo4j.

## Empirical results — LOCOMO benchmark

LOCOMO: 10 extended conversations, ~600 dialogues each, ~26K tokens average, ~200 questions each across single-hop, multi-hop, temporal, and open-domain categories.

Metrics: F1, BLEU-1 (B1), LLM-as-Judge (J, 10-run mean ± 1 SD). Deployment: token consumption + search/total latency at p50/p95.

**Overall J scores (Table 2)**:

| Method | J | p95 total latency | Avg tokens |
|---|---|---|---|
| Full-context (26,031 tokens) | **72.90** | 17.117s | 26,031 |
| Mem0g | 68.44 | 2.590s | 3,616 |
| **Mem0** | **66.88** | **1.440s** | **1,764** |
| Zep | 65.99 | 2.930s | 3,911 |
| OpenAI memory | 52.90 | 0.890s | 4,437 |
| Best RAG (k=2, 256-chunk) | 60.97 | — | — |
| LangMem | 58.10 | 59.82s search | — |
| A-Mem | 48.38 | — | — |

**Per-category highlights** (Table 1):
- *Single-hop*: Mem0 best (J=67.13); Mem0g slightly behind (65.71).
- *Multi-hop*: Mem0 best (J=51.15).
- *Temporal*: Mem0g best (J=58.13) — graph structure helps for event sequencing.
- *Open-domain*: Zep marginally leads (76.60 vs Mem0g 75.71); Mem0 at 72.93.

The headline claim from the abstract: **26% relative improvement over OpenAI memory on the LLM-as-Judge metric**. Mem0g scores ~2pp higher than base Mem0 overall.

**Token footprint**: Mem0 averages 7K tokens per conversation; Mem0g 14K; Zep >600K; raw full-context 26K.

## Latency claim

- **Mem0 search latency**: p50 = 0.148s, **p95 = 0.200s** (lowest of all methods).
- **Mem0 total latency**: p50 = 0.708s, **p95 = 1.440s**.
- Full-context total latency: p50 = 9.870s, p95 = 17.117s.
- **Mem0 p95 reduction vs full-context: 92%** (paper rounds to 91%).
- Mem0g p95 total = 2.590s — 85% reduction vs full-context.
- LangMem p95 search = 59.82s — authors call it *"impractical for interactive applications."*

Mechanism: selective retrieval of only the most salient memories rather than fixed-size chunks or full context. Mem0's 1,764 average retrieval tokens vs 26,031 for full-context explains the latency gap.

## Self-documented limitations

The paper does not have a dedicated limitations section but flags:
- Mem0g does not outperform base Mem0 on multi-hop queries; graph overhead introduces *"potential inefficiencies or redundancies"* for complex integrative tasks.
- Full-context still achieves the highest J score (72.90 vs Mem0g 68.44); memory systems trade some accuracy for latency/cost.
- Future work: optimise Mem0g graph operations to reduce latency overhead; explore hierarchical memory architectures blending efficiency with relational representation; develop more sophisticated memory consolidation; extend to procedural reasoning and multimodal interactions.

## Why it matters

- **Production-ready alternative to MemGPT/Letta lineage.** [[memgpt]] / [[letta-memory-blocks]] expose memory paging as agent-callable functions; Mem0 extracts and consolidates facts with conflict-resolution semantics, without requiring the agent to manage paging itself. Different mechanism families in [[memory-architectures]] — Mem0 is *retrieval-augmented memory stores*, MemGPT is *hierarchical virtual context*.
- **Operationalises [[generative-agents]]'s retrieval discipline at production scale.** Mem0 implements relevance-based retrieval with semantic similarity and adds the operations primitive (ADD/UPDATE/DELETE/NOOP) that the original Generative Agents paper handled informally.
- **The LOCOMO numbers are the cleanest available benchmark for the latency-vs-accuracy trade-off** in production memory systems. The 92% latency reduction at modest accuracy cost (66.88 vs 72.90 J, ~6pp) is a concrete engineering data point.
- **Direct comparison data vs Zep, LangMem, A-Mem, OpenAI memory** in a single benchmark — useful for selection decisions in production.

## Multi-party performance (GroupMemBench, collect-but-confirm)

[[memory/groupmembench]] (arXiv 2605.14498, 2026-05-18) reports Mem0 underperforms BM25 on multi-party conversational corpora: ~25.7% average accuracy vs BM25 ~43.2%, and a collapse on Knowledge Update (~4.67% vs BM25 ~25.23%). The Knowledge-Update failure is attributed to Mem0's extractor appending new statements alongside obsolete ones without speaker-conditioned consolidation — a regime its ADD/UPDATE/DELETE/NOOP pipeline was not designed for. These numbers contrast with Mem0's favorable LOCOMO results (J=66.88, 26% improvement over OpenAI memory), which are dyadic. The two regimes are different enough that neither result invalidates the other; practitioners should note the multi-party degradation for any deployment spanning group conversations.

## Claude Code integration

The preceding sections document the Mem0 *paper* and open-source library. This section covers the *productised Claude Code integration* described at docs.mem0.ai/integrations/claude-code — a separate layer built on top of the same extraction-and-consolidation doctrine.

**Three install paths:**
- **Plugin marketplace** (recommended) — installs the MCP server, lifecycle hooks, and an SDK skill in a single step.
- **MCP-only** (`claude mcp add` one-liner) — wires the MCP server without lifecycle hooks.
- **Manual `.mcp.json` config** — for teams that manage MCP configuration declaratively.

**Nine MCP tools exposed:** `add_memory`, `search_memories`, `get_memories`, `get_memory`, `update_memory`, `delete_memory`, `delete_all_memories`, `delete_entities`, `list_entities`.

**Five lifecycle hooks** (plugin install only):
1. **Session-Start** — loads relevant prior-session context before the agent begins.
2. **per-User-Prompt** — injects relevant memories on each prompt; prompts shorter than 20 characters are skipped for latency.
3. **Pre-Compaction** — stores a session summary immediately before Claude Code's context compaction event; this hook targets the same event discussed at [[claude-code-session-memory]].
4. **Task-Completed** — extracts learnings: successful strategies, failed approaches, decisions taken, conventions adopted.
5. **Session-End** — safety-net capture via REST API in case Task-Completed was skipped.

**Platform vs OSS:** The cloud platform (`m0-` API key) is the default path. The docs tag the Claude Code integration `[Both]`, so the self-hosted OSS MCP server (`openmemory/api/`, FastAPI over Qdrant) also works as a drop-in backend.

The Pre-Compaction and Task-Completed hooks are the concrete "extraction at named lifecycle events" form of Mem0's extract-and-consolidate doctrine — the same doctrinal axis examined at [[conflicts/verbatim-vs-extracted-memory]]. For the broader practitioner landscape of Claude Code memory options (including community plugins that operate on the same hooks), see [[claude-code-memory-ecosystem]]. The closest community-plugin peer on the extract-and-inject axis is [[claude-mem]].

## Source

- `raw/research/memory-management/07-04-mem0.md` (captured 2026-04-26 from https://arxiv.org/pdf/2504.19413 via marker on CPU; figures preserved in `assets/04-mem0/`)
- `raw/research/cc-memory-ecosystem/02-mem0-cc-integration.md` (https://docs.mem0.ai/integrations/claude-code)
- `raw/research/cc-memory-ecosystem/03-mem0-cc-integration.md` (https://docs.mem0.ai/llms.txt — Platform-vs-OSS framing)

## Related

- [[memory-architectures]] — survey's *retrieval-augmented memory stores* family; Mem0 is a 2025 production instance.
- [[memgpt]] — alternative paradigm (tiered paging vs extracted-facts retrieval).
- [[letta-memory-blocks]] — productionised MemGPT; the closest peer in the production-library landscape.
- [[generative-agents]] — Mem0 is a production realisation of the retrieval-scored memory stream concept.
- [[anthropic-memory-tool]] — Anthropic's API-level memory primitive; complementary rather than competing.
- [[memory/groupmembench]] — reports Mem0 ~25.7% avg / ~4.67% Knowledge Update vs BM25 ~43.2% on multi-party corpora; different regime from LOCOMO.
- [[claude-code-memory-ecosystem]] — practitioner landscape of Claude Code memory options; Mem0's CC integration is the commercial anchor.
- [[claude-mem]] — closest community-plugin peer; same extract-and-inject doctrine, different implementation (AI-compress, ChromaDB+SQLite, open-source).
