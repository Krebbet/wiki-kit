# claude-mem

A community Claude Code plugin (Apache 2.0, by `thedotmack`) that gives the agent persistent cross-session memory by **capturing tool-usage observations during a session, AI-compressing them, and proactively injecting relevant context into future sessions**. It installs as a Claude Code plugin (hooks + a background worker), stores data locally in SQLite plus a ChromaDB vector index, and works across several agents (Claude Code, Codex, Gemini CLI, OpenCode, and others). Architecturally it sits on the **extract/compress** pole of the [[conflicts/verbatim-vs-extracted-memory]] axis — the opposite discipline from [[mempalace]]'s verbatim store — and is the closest community-plugin peer to the productised [[mem0]] integration.

> **Authority:** the README (`01-claude-mem-repo.md`) is trustworthy for *what the tool does*. The MagnaCapax gist (`09-magnacapax-comparison.md`) supplies code-level architectural detail but is written by a competitor — its claude-mem descriptions are specific and checkable, but treat them as **collect-but-confirm**. The `$CMEM` Solana token mentioned in the README is a third-party creation unrelated to the tool's function and is deliberately excluded.

## How it works

Per the README (`01-claude-mem-repo.md`):

- **Install:** `npx claude-mem install` (registers hooks + the worker). The README explicitly warns that `npm install -g` installs the SDK only and does **not** wire up the hooks — `npx claude-mem install` is required.
- **Core loop:** capture tool-usage observations during a session → AI-compress them → inject relevant context at the start of the next session.
- **Stack:** Bun (JS runtime + process manager), `uv` (Python, for vector search), SQLite 3 (persistent storage). Built with the Claude Agent SDK; TypeScript.
- **Config:** `~/.claude-mem/settings.json`; supports multiple workflow modes (`code`, `chill`, `investigation`) and multi-language output variants, defined under `plugin/modes/`.
- **Local web viewer** at `http://localhost:37777`.
- **Cross-agent:** works with Claude Code, OpenClaw, Codex, Gemini CLI, Hermes, Copilot, OpenCode.
- A beta **"Endless Mode"** is described as a "biomimetic memory architecture for extended sessions" — no technical detail given (CLAIM, collect-but-confirm).

## Architecture detail (from the MagnaCapax comparison — collect-but-confirm)

The MagnaCapax gist (`09-magnacapax-comparison.md`, reviewing claude-mem v12.1.0) describes claude-mem's distinguishing feature as **proactive injection**, which it calls "genuinely novel":

- **Dual store:** SQLite for structured observation data + metadata filtering; ChromaDB for vector embeddings. (Contrast with MemPalace's single ChromaDB collection.)
- **SessionStart hook:** injects the last ~50 observations + ~10 session summaries at the start of a session.
- **PreToolUse:Read hook:** when the agent reads any file, past observations *about that file* are auto-injected, with specificity scoring. This file-context injection is the feature the gist singles out as novel.
- **Per-prompt semantic injection:** experimental, off by default.

*(Editorial: the SessionStart + PreToolUse injection model is a stronger "wake-up" mechanism than MemPalace's, which is pull-based and relies on the agent voluntarily calling `mempalace_status` per `CLAUDE.md` instruction — see [[mempalace]]. Whether compress-and-inject's lossy capture costs accuracy vs verbatim storage is the open [[conflicts/verbatim-vs-extracted-memory]] question.)*

## Where it sits

- **Doctrine:** extract/compress — an LLM decides what to keep, like [[mem0]] and unlike [[mempalace]]/mcp-knowledge-graph. Belongs to the *retrieval-augmented memory stores* family in [[memory-architectures]].
- **Ecosystem role:** one of the Level-6 cross-tool options in the [[claude-code-memory-ecosystem]] ladder; the leading community-plugin (vs vendor-service) instance of automatic CC memory.

## Source

- `raw/research/cc-memory-ecosystem/01-claude-mem-repo.md` (https://github.com/thedotmack/claude-mem) — project README; vendor/tool documentation.
- `raw/research/cc-memory-ecosystem/09-magnacapax-comparison.md` (https://gist.github.com/MagnaCapax/748b0be92dc31d4f5b6ba13286203766) — competitor code-level comparison; collect-but-confirm.

## Related

- [[claude-code-memory-ecosystem]] — the practitioner-landscape hub this is one entry in.
- [[mem0]] — closest peer; same extract/compress doctrine, but a vendor service rather than a community plugin.
- [[mempalace]] — doctrinal opposite (verbatim store, pull-based retrieval); the MagnaCapax gist compares the two directly.
- [[conflicts/verbatim-vs-extracted-memory]] — the extract-vs-verbatim axis this sits on (extract pole).
- [[memory-architectures]] — *retrieval-augmented memory stores* family.
- [[claude-code-session-memory]] — claude-mem is the community-built answer to the absence of native CC cross-session memory.
