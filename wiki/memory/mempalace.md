# MemPalace

Local-first AI memory library by Milla Jovovich and Ben Sigman, MIT-licensed; first release 2026-04-05. The system stores conversation transcripts as **verbatim text** in ChromaDB, retrieves via semantic search, and organises the corpus through a memory-palace metaphor: **wings** (people / projects) → **rooms** (topics) → **halls** (memory-type categories) → **drawers** (verbatim chunks), with **closets** as a separate compact-pointer index layer and **tunnels** as cross-wing connections. Backed by a Claude Code hook integration (29 MCP tools, two pre-compaction / on-stop hooks) and a temporal entity-relationship knowledge graph stored in SQLite. The design discipline is explicit in `CLAUDE.md`: *"Verbatim always — Never summarize, paraphrase, or lossy-compress user data. The system searches the index and returns the original words. 100% recall is the design requirement."*

## Architecture

The runtime, per `CLAUDE.md`, `docs/CLOSETS.md`, and the `mempalaceofficial.com/concepts/the-palace` page:

- **Storage**: ChromaDB by default for vector search, swappable via the abstract interface in `mempalace/backends/base.py`. v4-alpha adds PostgreSQL, LanceDB, and a bespoke `PalaceStore` backend. SQLite holds the temporal knowledge graph (entity → predicate → entity with valid_from / valid_to dates).
- **Embedding**: a local model (~300 MB on disk); no API key required for the core path. External LLMs (Anthropic, OpenAI, Google) are BYOK and never enabled silently — local Ollama / LM Studio / llama.cpp / vLLM are first-class.
- **Mining**: `mempalace mine <path>` ingests project files or conversation transcripts (Claude Code JSONL, ChatGPT export, Slack export). Files chunk into ~800-character verbatim **drawers**.
- **Search**: `mempalace search <query>` runs ChromaDB cosine similarity. With closets built, the searcher hits the closet index first, parses `→drawer_id` pointers, then hydrates the matching drawers; falls back to direct drawer search when closets are absent or all closet hits get filtered by `max_distance`.
- **MCP server**: 29 tools spanning palace reads/writes, KG operations, cross-wing navigation, drawer management, and agent diaries. Discoverable at runtime via `mempalace_list_agents`, `mempalace_traverse`, `mempalace_find_tunnels`.
- **Claude Code hooks**: `mempal_save_hook.sh` (Stop event) and `mempal_precompact_hook.sh` (PreCompact event). `MISSION.md` notes the v4 redesign moved diary writes off the chat window into background subagents to eliminate ~$1.13/session of re-transmitted diary tokens.

### The palace metaphor concretely

| Layer | What it holds | Implementation |
|---|---|---|
| **Wing** | A person or project (top-level) | Metadata field on every drawer |
| **Room** | A topic within a wing (e.g. `auth-migration`) | Metadata field; auto-detected from folder structure during `mempalace init`, or created manually |
| **Hall** | Memory-type category within a wing: `hall_facts`, `hall_events`, `hall_discoveries`, `hall_preferences`, `hall_advice` | Metadata field |
| **Drawer** | A verbatim ~800-character text chunk | A document in the `mempalace_drawers` ChromaDB collection |
| **Closet** | A compact pointer index — atomic topic lines like `built auth system\|Ben;Igor\|→drawer_api_auth_a1b2c3` | A document in the `mempalace_closets` ChromaDB collection (separate from drawers); cap of 1,500 chars / 12 topics / 3 quotes / 5 entities-per-pointer |
| **Tunnel** | A cross-wing connection — when the same room name appears in different wings | Discovered on traversal via `mempalace_traverse` and `mempalace_find_tunnels` |

The wing/room/hall layer is **metadata filtering** at the vector store, not a novel retrieval mechanism. Per the official concepts page: *"This is standard metadata filtering in the underlying vector store, not a novel retrieval mechanism. The useful property here is operational — clear scoping rules that a human or an agent can apply predictably — not a magic retrieval boost."*

The **closet** layer is structurally a fact-augmented key index — short topic+entity lines acting as searchable keys that point to verbatim values. This matches the "fact-augmented key expansion" pattern the [[longmemeval]] paper recommends as a +9.4pp recall improvement over flat indexing. Closets are rebuilt on each `mempalace mine` (delete-by-source-file then re-write); only the project miner builds them today — conversation-mined wings still use direct drawer search via the searcher fallback.

### AAAK compression layer

`dialect.py` implements **AAAK** — a lossy abbreviation system using entity codes and sentence truncation, intended as an experimental compression layer for closet entries. Per the maintainers' own retraction (2026-04-07), the original "30x lossless compression" framing was overstated; AAAK is lossy by design and trades fidelity for token density. On LongMemEval, AAAK mode scores 84.2% R@5 vs raw mode's 96.6% — a 12.4pp regression that reflects the lossy compression cost rather than a bug.

### Design principles

`CLAUDE.md` lists six non-negotiables:

1. **Verbatim always** — never summarise, paraphrase, or lossy-compress user data.
2. **Incremental only** — append-only ingest; a crash mid-operation must leave the existing palace untouched.
3. **Entity-first** — keyed by real names with disambiguation by DOB / ID / context.
4. **Local-first, zero external API by default** — all extraction, chunking, embedding, and LLM-assisted refinement on the user's machine; BYOK for external providers, never a silent fallback.
5. **Performance budgets** — hooks under 500ms; startup injection under 100ms.
6. **Background everything** — filing, indexing, timestamps, pipeline work in hooks, not in the chat window.

## Where it sits in the [[memory-architectures]] taxonomy

Survey family: **retrieval-augmented memory stores** (the same family as [[mem0]]). MemPalace differs from Mem0 along one explicit design axis: Mem0 *extracts and consolidates* salient facts via per-message LLM calls (ADD/UPDATE/DELETE/NOOP), while MemPalace *stores verbatim* by design. The doctrinal disagreement is documented at [[conflicts/verbatim-vs-extracted-memory]]; the [[longmemeval]] paper recommends a hybrid (verbatim values + extracted-fact keys), which MemPalace's closets-and-drawers structure gestures at.

Cross-paradigm comparisons:

- vs [[memgpt]] / [[letta-memory-blocks]] — different family. MemPalace is metadata-scoped vector retrieval over verbatim chunks; MemGPT is OS-style virtual memory paging via agent-callable functions.
- vs [[anthropic-memory-tool]] — Anthropic's API primitive exposes six file-system commands over `/memories`; MemPalace exposes 29 MCP tools over a structured ChromaDB+SQLite store with the palace abstractions on top.
- vs [[claude-code-session-memory]] — Claude Code's product layer extracts background summaries (~10k-token cadence) and injects them into new sessions; MemPalace markets a similar "wake-up" loop via its hooks but with verbatim discipline rather than Anthropic's automated-summary discipline.
- vs [[codified-context]] — codified-context is a hand-engineered hot/cold tier system for a single 108k-line C# codebase. MemPalace's wings/rooms/halls metadata structure is a softer instance of the same scoping discipline applied to conversation history.

## Benchmark claims (collect-but-confirm)

The README headline is **96.6% R@5 on [[longmemeval]] in raw mode** (no LLM, no API key) on the 500-question set, reproduced from the repository via `python benchmarks/longmemeval_bench.py /path/to/longmemeval_s_cleaned.json`. Independently reproduced on M2 Ultra in under 5 minutes by community member [@gizmax (issue #39)](https://github.com/MemPalace/mempalace/issues/39).

Other published numbers (per `benchmarks/BENCHMARKS.md` and the corrected README):

| Benchmark | Mode | Score | Notes |
|---|---|---|---|
| LongMemEval | Raw, semantic search only | 96.6% R@5 | No LLM, no API key |
| LongMemEval | Hybrid v4, held-out 450q (tuned on 50 dev) | 98.4% R@5 | Honest generalisable hybrid figure |
| LongMemEval | Hybrid v4 + LLM rerank, full 500 | ≥99% R@5 | Any capable model |
| LoCoMo | Top-10, no rerank | 60.3% R@10 | 1,986 questions |
| LoCoMo | Hybrid v5, top-10, no rerank | 88.9% R@10 | Same set |
| ConvoMem | All categories | 92.9% avg recall | 50 per category × 6 = 300 sampled from 75,000+ |
| MemBench (ACL 2025) | All categories | 80.3% R@5 | 8,500 items |

These numbers are **claims to confirm** rather than established facts: independent reproductions exist for the 96.6% raw figure but not for the others, and the ConvoMem 50-per-category sample is statistically underpowered against the 75k-item parent set. The reported metric for LongMemEval is `recall_any@5` — whether the correct memory is retrieved into the top-5 — not end-to-end QA accuracy. Cross-system comparisons that mix retrieval-recall and QA-accuracy metrics are not apples-to-apples; the README explicitly declines to publish such tables.

### Maintainer-corrected claims

`docs/HISTORY.md` is the canonical record of post-launch corrections — itself a useful primary source on what the system *doesn't* do:

- **"100% LongMemEval"** — removed from headlines (2026-04-14). The 99.4→100% step was achieved by inspecting the three remaining wrong answers and engineering targeted fixes — explicitly flagged as "teaching to the test."
- **"100% LoCoMo with top-50 rerank"** — removed (2026-04-14). At top_k=50 against per-conversation session counts of 19–32, retrieval returns every session by construction; the metric reduces to LLM reading comprehension over the whole conversation.
- **"30x lossless compression"** (AAAK) — retracted as overstated (2026-04-07). AAAK is lossy by design.
- **"+34% palace boost"** — retracted (2026-04-07). The compared configurations were unfiltered search vs wing+room metadata filtering; metadata filtering is a standard vector-store feature, not a MemPalace-specific mechanism.
- **Cross-system comparison tables mixing retrieval recall with QA accuracy** — removed (2026-04-14).

The candor of the corrections process is itself a usable signal: the project ships a public retraction log naming community auditors and explicitly preferring "right over impressive."

### Independent technical analyses

Captured for the wiki: an [`lhl/agentic-memory` code review](https://github.com/lhl/agentic-memory/blob/main/ANALYSIS-mempalace.md) and a Vectorize teardown report that several README-described features were not wired into the codebase at launch — `fact_checker.py` exists but isn't called from KG operations; `knowledge_graph.py` has no `contradict` operations (only identical-triple deduplication); halls are stored as metadata strings but not used in retrieval ranking; entity resolution is naive slug conversion. The maintainers' April 7 note acknowledges the contradiction-detection gap and lists wiring `fact_checker.py` into KG ops as future work. These are claims-to-confirm against current code rather than established facts; worth re-checking after the v4-alpha ships.

The same independent reproduction (issue #39) reports that on the M2 Ultra setup, room-mode retrieval scored 89.4% (–7.2pp vs raw) and AAAK mode 84.2% (–12.4pp) — i.e., the novel architectural features did not improve retrieval over raw ChromaDB defaults on that benchmark. The official concepts page now reflects this candidly.

## Roadmap (v4.0.0-alpha)

`ROADMAP.md` lists three v4 themes:
- **Swappable storage** — PostgreSQL (with `pg_sorted_heap`), LanceDB (multi-device sync without a server), `PalaceStore` (bespoke). Backend abstraction shipped in #413.
- **Local NLP** — on-device entity / relationship / topic extraction without external API calls; feature-flagged, falls back to existing heuristics.
- **Improved retrieval** — hybrid keyword + vector fallback (#662), stale-index detection (#663), time-decay scoring (#337), query sanitization for system-prompt contamination (#385, shipped in v3.1).

Deferred: Synapse advanced retrieval (MMR, pinned memory, query expansion — #596), multi-device sync (#575, blocked on LanceDB), multilingual embedding (#488, #442), Qdrant backend (#381).

## Tensions and corroboration from 2026 surveys (collect-but-confirm)

[[memory/memory-evolution-survey]] (arXiv 2605.06716, 2026-05-18) argues that unrestricted memory expansion is detrimental to agent performance, citing Xiong et al. 2025 and Srivastava and He 2025 (neither independently verified in this wiki). This is mild tension with MemPalace's never-summarize tenet, which holds that expansion is preferable to lossy compression. The conflict is not direct — the survey is arguing against *unbounded growth without management policy*, not against verbatim storage per se — but the framing is worth noting. The cited papers should be checked before treating this as a strong counter-claim.

Conversely, [[memory/groupmembench]] (arXiv 2605.14498) provides the strongest current empirical support for MemPalace's verbatim/raw-text-first discipline: a BM25 baseline over raw text (~43.2%) Pareto-dominates four of five extraction-based memory systems on multi-party conversational corpora, with extraction pipelines costing more while performing worse. This is independent corroboration from a different team and corpus type that the verbatim-first approach is competitive.

## Source

- `raw/research/mempalace/01-readme.md` (https://github.com/MemPalace/mempalace/blob/develop/README.md)
- `raw/research/mempalace/02-mission.md` (https://github.com/MemPalace/mempalace/blob/develop/MISSION.md)
- `raw/research/mempalace/03-roadmap.md` (https://github.com/MemPalace/mempalace/blob/develop/ROADMAP.md)
- `raw/research/mempalace/04-closets.md` (https://github.com/MemPalace/mempalace/blob/develop/docs/CLOSETS.md)
- `raw/research/mempalace/05-history.md` (https://github.com/MemPalace/mempalace/blob/develop/docs/HISTORY.md)
- `raw/research/mempalace/06-claude-md.md` (https://github.com/MemPalace/mempalace/blob/develop/CLAUDE.md)
- `raw/research/mempalace/07-concepts-the-palace.md` (https://mempalaceofficial.com/concepts/the-palace.html)
- `raw/research/mempalace/08-rhodes-review.md` (third-party review — collect-but-confirm)
- `raw/research/mempalace/09-vectorize-review.md` (third-party review citing independent code analysis — collect-but-confirm)
- `raw/research/mempalace/10-hn-thread.md` (community discussion — collect-but-confirm)

## Related

- [[memory-architectures]] — survey's *retrieval-augmented memory stores* family.
- [[mem0]] — closest peer in the production-library landscape; direct doctrinal counter on extract-vs-verbatim. See [[conflicts/verbatim-vs-extracted-memory]].
- [[longmemeval]] — the academic benchmark MemPalace's headline is graded against; the paper's recommended index designs (round-granularity values, fact-augmented key expansion, time-aware query expansion) frame MemPalace's closets-as-keys / drawers-as-values structure.
- [[memgpt]] / [[letta-memory-blocks]] — alternative paradigm (tiered virtual memory paging vs metadata-scoped vector index over verbatim chunks).
- [[anthropic-memory-tool]] — Anthropic's API-level memory primitive; vendor counterpart with file-system commands.
- [[claude-code-session-memory]] — Claude Code product-layer; MemPalace's hooks target the same loop with verbatim discipline rather than automated summary.
- [[codified-context]] — hand-engineered hot/cold tier system; MemPalace's wings/rooms/halls is a softer instance of the same scoping discipline.
- [[conflicts/verbatim-vs-extracted-memory]] — open conflict pairing this page against [[mem0]].
- [[memory/memory-evolution-survey]] — places MemPalace's verbatim discipline at the Storage pole of the Storage→Reflection→Experience axis; notes mild tension with expansion-is-detrimental claim (collect-but-confirm).
- [[memory/groupmembench]] — BM25 over raw text Pareto-dominates four of five extraction systems on multi-party corpora; independent empirical corroboration of verbatim-first discipline.
