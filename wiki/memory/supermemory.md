# Supermemory

Supermemory (`supermemoryai`) is a memory engine / context layer for AI systems that **extracts facts from conversations, builds static + dynamic user profiles, resolves contradictions, and forgets expired information**, plus hybrid RAG-over-documents + memory search and external connectors. It exposes one unified API and ships cross-tool plugins — Claude Code, OpenCode, OpenClaw, Hermes — that share a single account-level memory. Doctrinally it is firmly on the **extract pole**.

> **Open-source boundary (read first).** Supermemory is **not** a fully open-source system. Per its own README, the **MCP server and the plugins are open source**, but the **core extraction engine is a hosted commercial API** (dashboard at console.supermemory.ai, consumer app, paid tiers). Self-hosting the extraction engine is not offered. This matters for an open-source memory survey: you can self-host the *client* glue but depend on a proprietary *service* for the actual memory. License is not stated in the captured README.

> **Authority:** the README (`05-supermemory.md`) is a vendor marketing doc — moderate authority for feature description, low for benchmark claims. The "#1 on LongMemEval / LoCoMo / ConvoMem" claim is **self-graded via Supermemory's own MemoryBench framework** and is **collect-but-confirm** (self-certification). Vendor superlatives are excluded.

## Architecture & memory model

- **Memory engine:** extracts facts from conversations, tracks updates over time, resolves contradictions, automatically forgets expired information (temporal expiry — *"I have an exam tomorrow"* expires after the date; contradiction supersession — *"I just moved to SF"* overwrites *"I live in NYC"*).
- **User profiles (two-tier):** `profile.static` (stable long-term facts — role, preferences) and `profile.dynamic` (recent/current context — what you're working on now). Auto-maintained; retrievable in one call (claimed ~50 ms, *collect-but-confirm*).
- **Hybrid search:** RAG over documents **and** personalised memory retrieval in one query (`searchMode: hybrid | memories | documents`). The README explicitly distinguishes itself from plain RAG: *"RAG retrieves document chunks — stateless... Memory extracts and tracks facts about users over time."*
- **Connectors:** Google Drive, Gmail, Notion, OneDrive, GitHub, Web Crawler (webhook sync, auto-chunked). Multimodal file processing (PDF/image OCR, video transcription, AST-aware code chunking).
- **Scoping:** memory organised by `containerTag` ("projects") — separate work/personal or per-repo/client.
- **Framework integrations:** Vercel AI SDK, LangChain, LangGraph, OpenAI Agents SDK, Mastra, Agno, n8n.

## Doctrine placement

**Extract pole, with the most explicit contradiction-resolution and temporal-forgetting description of any tool in this batch.** The `memory` MCP tool fires automatically when something is "worth remembering"; profiles are distilled structured facts, not raw transcript chunks. The `profile.static` / `profile.dynamic` split is a noteworthy two-tier *within* the extract pole (stable facts vs recency-weighted context). It is the closest peer to [[mem0]] in the API-as-memory-service model, and to [[claude-mem]] as a Claude Code extract/inject plugin — but unlike claude-mem (fully local/OSS) it depends on a hosted engine. See [[conflicts/verbatim-vs-extracted-memory]].

## Claude Code integration

The `claude-supermemory` plugin (open source) provides a **three-layer** memory for coding: user profile (cross-project developer facts) + project memory (per-repo, via `containerTag`) + semantic search. Three MCP tools: `memory` (save/forget, called automatically), `recall` (search; returns memories + profile summary), `context` (injects the full profile at session start — in Claude Code triggered by typing `/context`). Install via an `install-mcp` npx one-liner with OAuth. Because all plugins share the Supermemory API, a profile built in Claude Code sessions is accessible from OpenCode/OpenClaw/Hermes under the same account — the distinctive **cross-tool memory portability** angle. It is a Level-6 cross-tool entry in the [[claude-code-memory-ecosystem]] ladder.

## Benchmark claims (self-certification caveat)

| Benchmark | Claimed | Note |
|---|---|---|
| [[longmemeval]] | 81.6%, "#1" | self-graded |
| LoCoMo | "#1" | self-graded |
| ConvoMem | "#1" | self-graded |

Supermemory also built and released **MemoryBench**, an open-source framework for comparing memory providers (Supermemory vs Mem0, Zep, …). The framework's existence is verifiable; Supermemory's *own results within a framework it authored* are a self-certification concern — **collect-but-confirm**. Note the cross-system non-comparability: this 81.6% LongMemEval figure (end-to-end QA) is not the same metric as [[mempalace]]'s 96.6% LongMemEval (recall@5), so the two cannot be ranked against each other.

## Source

- `raw/research/oss-agent-memory/05-supermemory.md` (https://github.com/supermemoryai/supermemory) — project README; vendor marketing/tool documentation. Captured 2026-05-24.

## Related

- [[claude-code-memory-ecosystem]] — Supermemory is a cross-tool Level-6 entry; note the hosted-engine caveat.
- [[claude-mem]] — closest Claude Code peer (extract/inject plugin); claude-mem is fully local/OSS, Supermemory depends on a hosted engine.
- [[mem0]] — closest API-as-memory-service peer; MemoryBench explicitly benchmarks against it.
- [[conflicts/verbatim-vs-extracted-memory]] — extract-pole reference implementation; static/dynamic profile split is a two-tier within the pole.
- [[memory-architectures]] — *retrieval-augmented memory stores* family.
- [[longmemeval]] / [[groupmembench]] — the benchmarks behind the "#1" claims; cross-check before trusting.
