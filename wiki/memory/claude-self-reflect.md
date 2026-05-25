# claude-self-reflect

An MIT-licensed community tool (by `ramakay`) that gives Claude Code persistent cross-session memory by **indexing the user's entire Claude Code conversation history** (`~/.claude/projects/` JSONL logs) into a local vector index and surfacing relevant past context automatically. Tagline: *"Claude forgets everything. This fixes that."* As of **v8 it is a single 44 MB Rust binary** — SQLite for storage, an in-process HNSW vector index, and local FastEmbed (384-dim) embeddings — having replaced the earlier Python/Docker/Qdrant stack. It wires into Claude Code via 6 lifecycle hooks and 12 MCP tools. Doctrinally it is **verbatim-leaning by default** (it indexes raw conversation chunks, not LLM-extracted facts) with an *optional* "AI Narratives" enrichment layer that adds an extract/compress step. Of everything in this wiki, it is the closest match to "a RAG that records everything in your conversation history."

> **Authority:** the README (`01-claude-self-reflect.md`) is a vendor doc — trustworthy for *what the tool does and how to install it*. Performance/quality numbers (the "9.3× search quality" and "<20% retention after 10 sessions" figures) cite no named benchmark or methodology and are **collect-but-confirm**. Marketing framing ("perfect memory") is excluded.

## How it works

Per the README:

- **Single binary (v8 Rust rewrite):** 44 MB, no Docker, no external database, no API key required for the base path. Replaces the prior Python/Docker/Qdrant architecture. 93 ms cached startup; ~14 s on the first run while the index builds.
- **Storage:** SQLite holds chunks, embeddings, and enrichment state.
- **Vector search:** in-process **HNSW** (claimed sub-millisecond p95).
- **Embeddings:** **FastEmbed**, 384-dimensional, local. Optional Voyage AI cloud embeddings (1024-dim).
- **What it indexes:** the `~/.claude/projects/` conversation JSONL files Claude Code writes; import ~20 conversations/sec. **AST code-aware search** across 6 languages.
- **Memory decay:** biomimetic time-based relevance weighting with a ~90-day half-life — recent solutions are prioritised while history is retained.

## Doctrine placement

claude-self-reflect straddles the [[conflicts/verbatim-vs-extracted-memory]] axis:

- **Base mode — verbatim, with a vector index.** It chunks and embeds the raw conversation JSONL; the `get_full_conversation` tool returns the *complete* JSONL. No LLM decides what to keep — the raw trace is the substrate. This is the same posture as [[mempalace]]'s raw mode (verbatim values + vector index), and it is the verbatim/no-extraction pole.
- **AI Narratives mode — optional extract/compress.** A daemon (requires an Anthropic API key, uses Claude via the Batch API at ~$0.012/conversation) "transforms raw conversations into rich, searchable narratives," claiming an 82% token reduction. The `store_reflection` tool likewise stores explicit extracted insights. This opt-in layer is the extract pole.

The dual-mode design makes it a clean illustration that verbatim and extract are *layers*, not mutually exclusive choices — captured at [[conflicts/verbatim-vs-extracted-memory]].

## Claude Code integration

**6 lifecycle hooks** (all use catch-all error handling — stated to "never block Claude Code"):

| Hook | Behaviour |
|---|---|
| `SessionStart` | Surfaces relevant past context at conversation start |
| `UserPromptSubmit` | Predicts and injects context before Claude responds |
| `PostToolUse` | Tracks file edits with session-scoped dedup |
| `Stop` | Stores iteration learnings; detects stuck patterns (e.g. "Ralph loops") |
| `PreCompact` | Backs up state before context compaction |
| `SessionEnd` | Stores the session narrative for future retrieval |

**12 MCP tools:** `csr_reflect_on_past`, `store_reflection`, `csr_quick_check`, `search_by_recency`, `get_recent_work`, `get_timeline`, `csr_search_by_file`, `csr_search_by_concept`, `csr_search_insights`, `csr_get_more`, `get_full_conversation`, `get_session_learnings`. Tools carry MCP read-only/write annotations per the 2025-11-05 spec.

**Install:** a single `install.sh` (downloads the binary, registers the MCP server, installs the 6 hooks), or `npm install -g claude-self-reflect`, or build from source via Cargo. macOS Intel requires building from source (no prebuilt binary).

Its `SessionStart` + `UserPromptSubmit` injection is a *push* wake-up model, like [[claude-mem]]'s and unlike [[mempalace]]'s pull-based protocol.

## Where it sits

- **Family:** *retrieval-augmented memory stores* in [[memory-architectures]] — specifically the **conversation-history indexer** sub-pattern (index the agent's own raw transcripts, retrieve later). The `get_full_conversation` verbatim return is a form of [[direct-corpus-interaction]] over the conversation log.
- **Ecosystem role:** a Level-5/6 entry in the [[claude-code-memory-ecosystem]] ladder. Its closest CC peer is [[claude-mem]] (same target — `~/.claude` memory via hooks + injection — but extract/compress doctrine rather than verbatim-first). Contrast with [[mem0]] (extract) and the verbatim peer [[mempalace]].
- **Benchmark caveat:** the "9.3× search quality" claim names no benchmark, dataset, or methodology — it cannot be placed against [[longmemeval]] or [[groupmembench]]. Treat as vendor self-report.

## Source

- `raw/research/oss-agent-memory/01-claude-self-reflect.md` (https://github.com/ramakay/claude-self-reflect) — project README; vendor/tool documentation. Captured 2026-05-24.

## Related

- [[claude-code-memory-ecosystem]] — the practitioner-landscape hub; claude-self-reflect is a conversation-history-indexer entry.
- [[claude-mem]] — closest Claude Code peer (same `~/.claude` target, hooks + injection) but extract/compress doctrine.
- [[mempalace]] — verbatim peer; both index raw conversation with a vector store, verbatim discipline.
- [[mem0]] — extract-pole contrast.
- [[conflicts/verbatim-vs-extracted-memory]] — claude-self-reflect's verbatim-base + optional-extract straddle illustrates the axis.
- [[direct-corpus-interaction]] — `get_full_conversation` returns the raw JSONL; verbatim retrieval over the conversation log.
- [[memory-architectures]] — *retrieval-augmented memory stores* family.
- [[anthropic-memory-tool]] — the AI Narratives daemon calls the Anthropic Batch API for enrichment.
