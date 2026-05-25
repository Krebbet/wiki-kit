# Claude Code Memory Ecosystem

Practitioner-landscape survey of the auxiliary memory systems people pair with Claude Code for long-term projects. Claude Code has **no native session-to-session memory** (curator ruling 2026-05-23; corroborated by the MindStudio survey's FAQ — see [[claude-code-session-memory]] for the disputed contrary claim): each session is a fresh API conversation, so anything that must survive a session reset has to be written to an external store and re-loaded deliberately. The community has converged on a ladder of approaches — from a single `CLAUDE.md` file, through a markdown "memory bank", to MCP-server-backed stores (Mem0, Basic Memory, mcp-knowledge-graph, MemPalace) and full cross-tool databases. This page maps that ladder, the tools at each rung, and the doctrinal split running through it. It is a hub; individual systems have their own pages.

> **Framing note (editorial):** the page leads with the no-native-memory premise per the curator's ruling. The six-level taxonomy below is the MindStudio survey's framing; tool-specific mechanics are attributed to each tool's own docs. Comparative/benchmark assertions from blog sources are **collect-but-confirm**.

## The three problems memory has to solve

The MindStudio survey frames Claude Code memory as three distinct sub-problems (`06-mindstudio-comparison.md`); most teams need two or three of them solved at once:

- **Instruction memory** — rules, preferences, constraints that always apply.
- **Knowledge memory** — facts, decisions, project/architecture context.
- **Episodic memory** — what happened in past sessions that's relevant now.

*(Editorial: this maps onto the academic five-family taxonomy in [[memory-architectures]] — instruction ≈ static parametric/context, knowledge ≈ retrieval-augmented stores, episodic ≈ the write-manage-read loop. The practitioner framing is a restatement, not a competing taxonomy.)*

## The six-level ladder

Per the MindStudio survey (`06-mindstudio-comparison.md`), with setup-effort and best-fit as that source states them:

| Level | What it is | Persistence | Setup | Best for (per source) |
|---|---|---|---|---|
| 1. In-context | The active context window; nothing survives session end | Session only | None | Quick, contained tasks |
| 2. `CLAUDE.md` | Plain markdown auto-loaded at session start (global / project / subdir scopes) | Permanent | Minutes | "~80% of needs"; most solo devs & small teams |
| 3. Markdown KB | Structured folder of markdown with an `INDEX.md`; agent selectively reads files | Permanent | Hours | Established projects, multi-contributor |
| 4. Auto-updating hooks | Claude Code hooks instruct the agent to update its own memory files | Permanent | Hours | Long-running solo, power users |
| 5. Vector/RAG | Chunk → embed → vector DB; semantic retrieval into context | Permanent | Days | Large codebases, 50+ docs |
| 6. Cross-tool DB | Memory in SQLite/Postgres or a service (e.g. Mem0); tool-call access, shareable | Permanent | Days–weeks | Multi-agent teams, production |

The survey's own recommendation is to **combine layers** — `CLAUDE.md` for always-loaded instructions + a markdown KB for selectively-loaded knowledge + a database/service for episodic queries — and gives upgrade triggers (e.g. promote from `CLAUDE.md` to a markdown KB once the file passes ~500 lines or spans multiple knowledge domains).

Two CLAIM-tagged assertions from this source are recorded as **attributed practitioner opinion, not fact**: that "well-organized markdown is often more reliably retrieved than vector embeddings" (attributed to Karpathy) and that "Mem0 has shown measurably better retrieval accuracy than built-in model memory" (sourced to another MindStudio post, no primary benchmark). The first is a practitioner statement of the same thesis the wiki documents empirically at [[direct-corpus-interaction]].

## The markdown "memory bank" pattern (Levels 2–4)

The vexp blog (`07-memory-bank-pattern.md`) documents a concrete, widely-repeatable convention for the file-based rungs:

- **Layer 1 — `CLAUDE.md`** (static, 300–600 words): project overview, architecture decisions (*why*, not *what*), code conventions, "things not to re-derive". Avoid file contents, full API docs, frequently-changing info.
- **Layer 2 — `.claude/memory/` directory** (dynamic): `MEMORY.md` (index, kept ≤200 lines), `decisions.md` (dated architecture-decision log — the author calls it the most valuable file), `patterns.md`, `debugging.md`, `sprint.md`. Loaded by an explicit instruction in `CLAUDE.md` ("read `.claude/memory/MEMORY.md` at session start"); refreshed by a manual end-of-session write-back ("write today's decisions to `decisions.md`"). Committed to the repo so the whole team benefits.

The mechanism is pure filesystem persistence + deliberate instruction — nothing is automatic. *(Editorial: this is the practitioner-discipline cousin of [[effective-harnesses]]' `feature_list.json` + `claude-progress.txt` + git-as-recovery, and an instance of [[direct-corpus-interaction]] — the agent reads/greps its own notes rather than querying an index.)* The author's token-saving arithmetic (a ~200-line `MEMORY.md` costs ~1.5–2k tokens but saves re-explaining 3–5k) and the "200-line truncation" claim are author estimates, **collect-but-confirm**.

## The MCP-server tools (Levels 5–6)

When file-based memory stops scaling, practitioners reach for an MCP server backing a real store. The captured tools, with their doctrinal placement on the [[conflicts/verbatim-vs-extracted-memory]] axis:

| Tool | Store | Retrieval | Capture model | Doctrine | CC integration |
|---|---|---|---|---|---|
| [[mem0]] | Cloud (Platform) or self-host (OSS, Qdrant) | Semantic | LLM extract-and-consolidate | **Extract** | 9 MCP tools + 5 lifecycle hooks (`02/03-mem0-cc-integration.md`) |
| [[claude-mem]] | SQLite + ChromaDB (local) | Vector | AI compress-and-inject | **Extract** | Plugin install; SessionStart + PreToolUse:Read injection (`01`, `09`) |
| Basic Memory | Local markdown note-graph | Semantic | **User-authored** structured notes | *Third position* | MCP server, cloud or local (`04-basic-memory-cc.md`) |
| mcp-knowledge-graph | Local JSONL entity/relation/observation KG | **Keyword** | Verbatim observations | Verbatim-ish | 10 `aim_*` MCP tools, project-local or global (`05-mcp-knowledge-graph.md`) |
| [[mempalace]] | ChromaDB + SQLite KG (local) | Vector + closet/BM25 hybrid | **Verbatim** ("never summarize") | **Verbatim** | 19–29 MCP tools (version-sensitive) + Stop/PreCompact hooks |
| [[claude-self-reflect]] | SQLite + in-process HNSW (v8 Rust binary, local) | Vector (+ optional AI-narrative) | Indexes raw `~/.claude` JSONL transcripts | **Verbatim** (+ optional extract) | 6 hooks + 12 MCP tools (`01-claude-self-reflect.md`) |
| [[graphiti]] | Neo4j / FalkorDB / Kuzu / Neptune | Semantic + BM25 + graph traversal | LLM extract → **bi-temporal** KG | **Extract** (temporal) | Official MCP server (`03-zep-graphiti.md`) |
| [[cognee]] | Graph (Neo4j/Falkor/Kuzu) + vector | Auto-routed semantic/graph | `cognify` extract → graph | **Extract/transform** | Plugin; 5 hooks incl. PreCompact (`04-cognee.md`) |
| [[supermemory]] | Hosted commercial engine | Hybrid RAG + memory | LLM fact-extract + static/dynamic profiles | **Extract** | Plugin + MCP; cross-tool (`05-supermemory.md`) |
| [[memori]] | BYODB or hosted cloud | (undisclosed) | LLM extract from agent **execution** + chat (8 typed categories) | **Extract** | HTTP MCP server; cross-tool (`07-memori.md`) |

Notes per source:

- **[[mem0]]** (`02-mem0-cc-integration.md`): three install paths (plugin marketplace / MCP-only / manual `.mcp.json`); 9 MCP tools (`add_memory`, `search_memories`, …); **five lifecycle hooks** — SessionStart (load prior context), per-prompt (inject relevant memories; <20-char prompts skipped), Pre-Compaction (store session summary before compaction), Task-Completed (extract learnings), Session-End (safety-net capture). Platform (cloud, `m0-` API key) is the default but the docs tag CC integration `[Both]`, so an OSS self-hosted MCP server (`openmemory/api/`) also works. See [[mem0]] for the underlying paper.
- **Basic Memory** (`04-basic-memory-cc.md`): articulates a clean three-layer model — `CLAUDE.md` = "how to work here", CC's built-in handling = short preferences, Basic Memory = "everything we know" (decisions/architecture/research that grows over time, searchable across any AI tool, not CC-exclusive). Distinct from both extract and verbatim: memory is *user-authored structured notes*.
- **mcp-knowledge-graph** (`05-mcp-knowledge-graph.md`): the closest community analog to MemPalace's KG framing, but far simpler — flat JSONL triples, **keyword** search (no vector), project-local `.aim/memory.jsonl` or a global path. A known limitation: agents invent inconsistent database names. The maintainer syncs a global memory path via Dropbox for cross-machine portability (maintainer EXPERIENCE).
- **[[mempalace]]** is the verbatim-discipline maximalist of this set; its in-practice behaviour and effectiveness questions are covered on its own page.

Mem0 and Zep pricing context, from the danilchenko review (`10-danilchenko-review.md`, collect-but-confirm): Mem0 ~$19–249/mo, Zep ~$25+/mo; MemPalace/Basic-Memory/mcp-knowledge-graph are free/local.

**2026-05-24 — the wider open-source landscape (`raw/research/oss-agent-memory/`).** Beyond the Claude-Code-specific tools, the broader OSS agent-memory field includes graph-based engines — [[graphiti]] (Zep's bi-temporal temporal-KG core) and [[cognee]] (graph+vector "memory control plane" with a 5-hook CC plugin) — and the hosted-engine [[supermemory]] (OSS plugins, but a *commercial* extraction API; the open-source boundary matters). A distinct **conversation-history-indexer** pattern indexes the agent's *own* raw `~/.claude` transcripts and retrieves them later: [[claude-self-reflect]] (local SQLite + HNSW, verbatim-first, v8 single Rust binary) is the leading instance — the closest tool to "a RAG that records everything you've said to Claude." Finally, the `mcp-knowledge-graph` row above is a community fork of the canonical [[mcp-memory-server]] (the official MCP knowledge-graph reference). Graphiti and Cognee are documented as standalone systems because they are used well beyond Claude Code.

### Conversation-history indexers (2026-05-24 follow-up)

A distinct family indexes the agent's *own* raw `~/.claude` transcript JSONL and exposes search — "find what we figured out before" rather than maintaining a curated memory store. All three are local, **verbatim pole** (no LLM extraction in the retrieval path), and give *both* the user and the agent (via MCP) search access:

| Tool | Engine | Doctrine | Notable |
|---|---|---|---|
| [[claude-self-reflect]] | SQLite + HNSW **vector** (v8 Rust) | Verbatim + optional AI-narrative extract | Richest: 6 hooks, 12 tools, 90-day time-decay; the only one with a vector path |
| claude-conversation-search-mcp (`ticpu`, MIT, Rust) | **Tantivy / BM25** keyword | Verbatim | "Smart filtering" skips `tool_result` file dumps, keeps text+thinking; 6 MCP tools; offloads summarisation to haiku |
| cowork-history (`egoughnour`, MIT, Python) | SQLite **FTS5** + macOS **Spotlight** + optional Ollama vector | Verbatim (+ optional vector) | Triple-backend hybrid; covers Claude Code *and* "Cowork" stores; beta, minimal adoption |

These are [[direct-corpus-interaction]]-adjacent on the verbatim pole: keyword/FTS over raw transcripts with no extraction step. Only [[claude-self-reflect]] is promoted to a standalone page (richest feature set + a vector path + the optional extract layer); the two BM25/FTS tools are catalogued here. The user-facing value is identical across all three: stop re-deriving what a past session already solved.

## Cross-source themes (editorial)

- **The doctrinal split is the organising axis.** The extract pole (Mem0, claude-mem — LLM decides what to keep) vs the verbatim pole (MemPalace, mcp-knowledge-graph — store the words, search later) is exactly the open [[conflicts/verbatim-vs-extracted-memory]] tension, now visible as a *product* choice CC users make. Basic Memory adds a genuinely distinct third stance: neither machine-extracted nor raw-trace, but **human-curated structured notes**.
- **"CLAUDE.md is the product."** The single most repeated practitioner lesson (ivanmorgillo `08`, the memory-bank blog `07`, the MindStudio Level-4 caveat): an external memory store does nothing unless `CLAUDE.md` explicitly instructs the agent *when* to read and write it. Without that, the agent acknowledges information verbally and stores nothing. This is the operational counterpart to the "no native memory" premise.
- **Retrieval ≠ use.** The strongest effectiveness caveat (detailed on [[mempalace]]): high retrieval-recall benchmark scores do not imply the agent answers correctly from what it retrieves — the same recall-vs-use gap the [[memory-architectures]] survey names.

## Source

- `raw/research/cc-memory-ecosystem/06-mindstudio-comparison.md` (https://www.mindstudio.ai/blog/claude-code-memory-systems-compared) — six-level taxonomy; vendor/practitioner blog (Remy product pitch excluded).
- `raw/research/cc-memory-ecosystem/07-memory-bank-pattern.md` (https://vexp.dev/blog/building-memory-bank-claude-code-session-resets) — markdown memory-bank convention (vexp product pitch excluded).
- `raw/research/cc-memory-ecosystem/02-mem0-cc-integration.md`, `03-mem0-cc-integration.md` (https://docs.mem0.ai/integrations/claude-code, /llms.txt) — Mem0 CC integration.
- `raw/research/cc-memory-ecosystem/04-basic-memory-cc.md` (https://docs.basicmemory.com/integrations/claude-code) — Basic Memory CC integration.
- `raw/research/cc-memory-ecosystem/05-mcp-knowledge-graph.md` (https://github.com/shaneholloman/mcp-knowledge-graph) — local KG MCP server.
- `raw/research/cc-memory-ecosystem/01-claude-mem-repo.md`, `09-magnacapax-comparison.md`, `10-danilchenko-review.md` — referenced for claude-mem architecture and Mem0/Zep pricing (see [[claude-mem]], [[mempalace]] for full treatment).

## Related

- [[claude-code-session-memory]] — the disputed "native automatic memory" page; the no-native-memory premise here contradicts it (curator ruling).
- [[mempalace]] — the verbatim maximalist; in-practice usage & effectiveness.
- [[claude-mem]] — highest-profile community plugin; extract/compress doctrine.
- [[mem0]] — extract-and-consolidate; the CC integration is the productised form.
- [[anthropic-memory-tool]] — Anthropic's API-level memory primitive (FS commands over `/memories`), an alternative substrate for Level 6.
- [[memory-architectures]] — the academic five-family taxonomy the three-problem framing restates.
- [[conflicts/verbatim-vs-extracted-memory]] — the doctrinal axis these tools sit on.
- [[direct-corpus-interaction]] — grep-over-files retrieval; the mechanism behind Levels 2–3 and the "markdown beats embeddings" practitioner claim.
- [[effective-harnesses]] — progress-file/git-recovery discipline; the memory-bank pattern's engineered cousin.
- [[claude-self-reflect]] — conversation-history indexer (verbatim-first, local SQLite+HNSW over `~/.claude`); the literal "records everything" tool.
- [[graphiti]] — Zep's OSS temporal knowledge-graph core; bi-temporal extract pole.
- [[cognee]] — graph+vector "memory control plane"; deepest CC-hook integration in the OSS batch.
- [[supermemory]] — extract-pole engine with cross-tool plugins; OSS plugins but a hosted commercial core.
- [[mcp-memory-server]] — the official MCP knowledge-graph reference; upstream of the `mcp-knowledge-graph` fork above.
- [[memori]] — extract-pole memory layer (MemoriLabs); captures agent *execution* + chat into 8 typed categories; HTTP MCP server.
