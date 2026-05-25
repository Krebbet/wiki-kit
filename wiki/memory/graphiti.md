# Graphiti (Zep)

Graphiti (`getzep/graphiti`) is the **open-source temporal knowledge-graph engine** at the core of Zep's managed agent-memory product (Zep = the hosted product; Graphiti = the self-hostable OSS core). Its defining property is **bi-temporal** modelling: every fact/edge carries a validity window, and a contradicting fact triggers **automatic invalidation** (the old edge's `valid_to` is set) rather than deletion — preserving a queryable history of what was true when. It ingests *episodes* (the raw data, retained as provenance), LLM-extracts entities and relationships into a graph at ingest time, and answers queries via **hybrid semantic + BM25 + graph-traversal** retrieval with graph-distance reranking. It ships an official MCP server (Claude/Cursor/etc.) and is backed by an arXiv paper, *"Zep: A Temporal Knowledge Graph Architecture for Agent Memory"* (arXiv 2501.13956). Doctrinally it is on the **extract pole**, but its temporal model makes it a distinct sub-family from flat extract stores.

> **Authority:** the README (`03-zep-graphiti.md`) is a vendor doc — authoritative for Graphiti's own mechanics (episode/edge structure, bi-temporal model, backends, MCP server). The backing paper has now been ingested (see *Benchmark results* below): the accuracy/latency-reduction claims are paper-substantiated against a full-context baseline (vendor-run), but the README's **"sub-second / sub-200 ms" latency claim is *not* in the paper** (paper latencies are 2.58–3.2 s end-to-end) and the "state-of-the-art" claim is only *partially* substantiated. License not stated in the captured README.

## Architecture — the temporal knowledge graph

Graphiti calls its structure a **context graph**:

| Component | What it holds |
|---|---|
| **Entities (nodes)** | People, products, policies, concepts — summaries evolve over time |
| **Facts (edges)** | `(source) → relation → (destination)` triplets, each with a temporal **validity window** |
| **Episodes** | The raw data as ingested — the ground-truth stream; every derived fact traces back to one |
| **Custom types** | Developer-defined entity/edge types via Pydantic models (prescribed *or* learned ontology) |

- **Incremental, not batch:** new episodes integrate immediately "without batch recomputation" — an explicit contrast with batch-oriented RAG/GraphRAG.
- **LLM on the write path:** ingestion calls an LLM to extract entities/relationships; defaults to OpenAI, supports Anthropic/Gemini/Groq/Azure/Ollama. Requires structured-output support (the README warns smaller models can produce schema failures). Concurrency gated by `SEMAPHORE_LIMIT` (default 10).
- **Pluggable backends:** Neo4j 5.26 (default), FalkorDB, Kuzu (embedded), and Amazon Neptune + OpenSearch Serverless.

### How it differs from GraphRAG (per the README)

| Aspect | GraphRAG | Graphiti |
|---|---|---|
| Data handling | Batch-oriented | Continuous, incremental |
| Temporal handling | Basic timestamps | **Explicit bi-temporal** with automatic fact invalidation |
| Contradictions | LLM-driven summarisation | Automatic invalidation, history preserved |
| Query latency | Seconds–tens of seconds | "Sub-second" is a README claim; the *paper* measures **2.58–3.2 s end-to-end** (still ~90% faster than full-context) — see *Benchmark results* |
| Custom entity types | No | Yes (Pydantic) |

## Retrieval

Three-way hybrid — semantic embeddings + keyword/BM25 + graph traversal — explicitly **without LLM summarisation at query time** (contrast with GraphRAG's sequential-LLM approach). Reranking by graph distance; OpenAI and Gemini rerankers available; "predefined search recipes" for node search.

## Doctrine placement

**Extract pole, with a temporal twist.** Raw episodes go in; an LLM extracts triplets that are stored with time-bounded validity; the original episode is retained as provenance. This is the same extract doctrine as [[mem0]] (and [[mem0]]'s graph variant Mem0g, which also uses Neo4j for extracted relationships) — but Graphiti adds **bi-temporal validity + automatic invalidation**, which Mem0g does not implement. It is therefore a worked example of *automated conflict handling* on the extract pole, distinct from flat-vector extract stores. See [[conflicts/verbatim-vs-extracted-memory]].

Its nearest OSS peer in this research batch is [[cognee]] (also graph + extract); the lightest-weight relative is [[mempalace]], which keeps a temporal entity-relationship KG in SQLite alongside verbatim drawers — an embedded, verbatim-first counterpoint to Graphiti's Neo4j-backed extract-first design.

## Agent / Claude integration

An **official MCP server** ships in the repo (`mcp_server/`, deployed via Docker + Neo4j): episode management, entity/relationship handling, semantic + hybrid search, group management, graph maintenance. The README highlights it for "Claude, Cursor, and other MCP clients." A FastAPI REST server is also included. For Claude users, `graphiti-core[anthropic]` makes Anthropic the extraction LLM (though OpenAI gets the best structured-output support per the README). This makes Graphiti a graph-based memory backend usable from [[claude-code-memory-ecosystem]] alongside the file/SQLite stores catalogued there.

## Benchmark results (from the paper, arXiv 2501.13956)

The paper is authored by Zep AI staff (Rasmussen et al.) — **vendor-run, not independently replicated**. It reports two benchmarks. *Bottom line:* the accuracy and latency-reduction claims hold against a *full-context baseline*; the README's "sub-second / sub-200 ms" latency claim is **not** in the paper.

**Deep Memory Retrieval (DMR)** — 500 conversations, ~60 messages each:
- Zep **94.8%** vs MemGPT 93.4% (gpt-4-turbo); Zep **98.2%** vs full-context 98.0% (gpt-4o-mini).
- Margins are tiny (1.4 pp over MemGPT; 0.2 pp over full-context). The authors themselves call DMR inadequate — *"each conversation contains only 60 messages, easily fitting within current LLM context windows"* — i.e. a memory system barely beats stuffing the whole conversation in.

**LongMemEval (LME)** — ~115k tokens/conversation, six question types:

| Model | Full-context | Zep | Latency (Zep vs full) | Zep context |
|---|---|---|---|---|
| gpt-4o-mini | 55.4% | **63.8%** | 3.20 s vs 31.3 s | ~1.6k tokens |
| gpt-4o | 60.2% | **71.2%** | 2.58 s vs 28.9 s | ~1.6k tokens |

- +15.2 / +18.5 pp over full-context; ~90% end-to-end latency reduction (Zep's latency *includes* a cross-region network round-trip, so the comparison disfavours Zep on latency rather than flattering it).
- **MemGPT could not be run on LME** (it can't ingest pre-existing histories), so there is **no peer-memory-system comparison on LME** — only Zep vs full-context.
- Zep *underperforms* full-context on single-session-assistant questions (−17.7 pp with gpt-4o); the authors flag this as needing work.

**Claim adjudication:**
- *"Sub-second / sub-200 ms"* → **README only, not in the paper.** Paper latencies are 2.58–3.2 s end-to-end. Downgraded from collect-but-confirm to *unsubstantiated by the paper*.
- *"State of the art"* → **partially substantiated**: beats MemGPT on DMR (narrow margin, on a benchmark the authors call weak) and full-context on LME; no other memory system compared on LME; vendor-run, unreplicated.

Useful cross-data: Zep's LME scores (63.8 / 71.2) and its LOCOMO appearance in [[mem0]]'s comparison table (J=65.99) now have a primary-source anchor; [[memori]] claims to *beat* Zep on LoCoMo, a head-to-head the wiki has not independently checked.

## Source

- `raw/research/oss-agent-memory/03-zep-graphiti.md` (https://github.com/getzep/graphiti) — project README; vendor/tool documentation. Captured 2026-05-24.
- `raw/research/oss-agent-memory/11-graphiti-paper.md` (https://arxiv.org/abs/2501.13956 — *"Zep: A Temporal Knowledge Graph Architecture for Agent Memory"*, Rasmussen et al., Zep AI) — captured 2026-05-24 via marker (CPU). Vendor-authored; numbers author-run, unreplicated.

## Related

- [[memory-architectures]] — *retrieval-augmented memory stores* family; Graphiti is the canonical **temporal knowledge-graph** instance.
- [[mem0]] — closest extract-pole peer; Mem0g is its graph variant, but without bi-temporal validity windows.
- [[cognee]] — the other OSS graph-memory system in this batch; both extract into a graph, both ship Claude integrations.
- [[mempalace]] — embedded, verbatim-first counterpoint that also keeps a temporal KG (in SQLite).
- [[mcp-memory-server]] — the simpler official MCP knowledge-graph server (keyword search, no temporality).
- [[conflicts/verbatim-vs-extracted-memory]] — Graphiti is an extract-pole example with explicit automated conflict resolution.
- [[claude-code-memory-ecosystem]] — Graphiti's MCP server is a graph-based backend option for Claude Code.
- [[longmemeval]] / [[groupmembench]] — benchmarks to cross-check Graphiti/Zep's "state-of-the-art" claims against.
