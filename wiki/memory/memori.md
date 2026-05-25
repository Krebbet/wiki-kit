# Memori

Memori (**MemoriLabs/Memori**, Apache 2.0; the repo was transferred from `GibsonAI/memori` and repositioned — older write-ups describe a "SQL-native" memory store, but the current product pitches itself as **"agent-native memory infrastructure"**) is an LLM-agnostic, datastore-agnostic memory layer for production agents. Its distinctive framing is **"memory from what agents *do*, not just what they say"** — it captures agent *execution* (tool calls, decisions, outcomes) alongside conversation, extracting into typed memory categories. It wraps existing LLM client calls and runs background "Advanced Augmentation," with memory scoped along an entity → process → session hierarchy. Doctrinally it sits on the **extract pole**, and offers a BYODB / hosted-cloud split rather than being purely local.

> **Authority:** the README (`07-memori.md`) is a vendor doc — trustworthy for the integration surface and capture model. The backing paper is now ingested (see *Benchmark results*): Memori's own LoCoMo row is self-run, but its competitor baselines are **borrowed from a third-party paper, not re-run** — so head-to-head claims are weakly grounded. The "SQL-native" descriptor from third-party comparison blogs is not in the current README; the storage substrate is not disclosed there (BYODB is offered, internals unspecified).

## Architecture & capture model

- **Capture from execution, not just chat:** the SDK intercepts LLM API calls (OpenAI/Anthropic/Bedrock/DeepSeek/Gemini/Grok) and runs background "Advanced Augmentation" after each turn — extracting and enriching across **eight typed categories**: attributes, events, facts, people, preferences, relationships, rules, skills. It captures tool calls, decisions, and outcomes, not only utterances. Claimed to add no latency (background; collect-but-confirm).
- **Scoping hierarchy:** entity → process → session (person/place/thing → agent/program → current interaction window). Memories are keyed to an `entity_id` + `process_id` pair; no attribution = nothing stored.
- **Storage:** datastore-agnostic with a **BYODB** ("bring your own database") mode plus a hosted Memori Cloud tier. The README does not disclose the internal storage model (vector/graph/relational) or the retrieval mechanism.

## Doctrine placement

**Extract pole.** Augmentation distils conversation *and* execution traces into eight typed memory categories rather than storing raw transcripts — the same family as [[mem0]] and [[supermemory]] in [[memory-architectures]]' retrieval-augmented stores. Its distinctive contribution within that pole is the **execution-capture** emphasis (what the agent did), which echoes [[claude-mem]]'s tool-usage-observation capture but generalised across providers and frameworks. See [[conflicts/verbatim-vs-extracted-memory]].

## Integration surface (incl. Claude Code)

- **LLM SDK wrapping:** Anthropic, OpenAI (Chat Completions + Responses), Bedrock, DeepSeek, Gemini, Grok — sync/async, streamed/unstreamed.
- **Agent frameworks:** Agno, LangChain, Pydantic AI; plugins for OpenClaw (`@memorilabs/openclaw-memori`) and Hermes (`hermes-memori`, exposing `memori_recall` tools).
- **Claude Code:** explicit HTTP MCP integration —
  ```
  claude mcp add --transport http memori https://api.memorilabs.ai/mcp/ \
    --header "X-Memori-API-Key: ${MEMORI_API_KEY}" \
    --header "X-Memori-Entity-Id: your_username" \
    --header "X-Memori-Process-Id: claude-code"
  ```
  Same HTTP MCP endpoint also documented for Cursor, Codex, Warp, Antigravity. This makes it a cross-tool Level-6 entry in the [[claude-code-memory-ecosystem]] ladder (note: the MCP endpoint is the *hosted* API; OSS scope of the backend is unclear from the README).

## Benchmark results (from the paper, arXiv 2603.19935)

The Memori paper (Borro et al., **Memori Labs** — vendor-authored, March 2026) evaluates on **LoCoMo** with an LLM-as-Judge across four reasoning categories. Memori's own row is averaged over 3 runs; its benchmark pipeline is semantic triples + summaries, Gemma-300 embeddings, FAISS index, hybrid cosine+BM25 retrieval, GPT-4.1-mini reader.

| Method | Single-hop | Multi-hop | Open-domain | Temporal | **Overall** |
|---|---|---|---|---|---|
| **Memori** | 87.87 | 72.70 | 63.54 | 80.37 | **81.95** |
| Zep | 79.43 | 69.16 | **73.96** | 83.33 | 79.09 |
| LangMem | 74.47 | 61.06 | 67.71 | **86.92** | 78.05 |
| Mem0 | 62.41 | 57.32 | 44.79 | 66.47 | 62.47 |
| Full-Context (ceiling) | 88.53 | 77.70 | 71.88 | 92.70 | 87.52 |

**Does Memori beat Zep on LoCoMo? Qualified yes — with a load-bearing caveat:**

1. **Not a controlled head-to-head.** The paper states the Zep / LangMem / Mem0 / Full-Context rows were **"retrieved from Du et al. [2025]"** — lifted from a third-party paper's harness, *not* re-run alongside Memori. Only Memori's row is the authors' own measurement. So the 81.95 vs 79.09 overall lead pits a self-run number against borrowed baselines from a different setup.
2. **Mixed by category.** Memori wins overall, single-hop, and multi-hop, but **Zep beats Memori on open-domain (73.96 vs 63.54) and temporal (83.33 vs 80.37)**, and LangMem also beats Memori on temporal. The overall lead rests on single-/multi-hop strength.
3. **Token efficiency** (Table 2, baselines also borrowed — from the Mem0 paper, Chhikara et al. 2025): Memori 1,294 tokens (4.97% of full context) vs Mem0 1,764 vs Zep 3,911 — ~67% fewer than Zep, the one claim that is robust regardless of accuracy harness.

**Harness-dependence red flag (synthesis):** this paper's borrowed Zep score (79.09% overall on LoCoMo) is not reconcilable with the Zep figure in [[mem0]]'s own LoCoMo table (J = 65.99). Worse, the two papers **disagree on the ordering** — the Mem0 paper has Mem0 ≈ Zep (Mem0 marginally ahead), while this paper (via Du et al.) has Zep ≫ Mem0 by ~17 pp. Same benchmark name, different harness → different absolute scores *and* a reversed winner. Treat cross-paper LoCoMo rankings as unreliable; see [[conflicts/verbatim-vs-extracted-memory]].

## Caveats & authority

- README/vendor doc; all benchmark and comparison claims are first-party and unreplicated.
- OSS boundary: the SDK is Apache 2.0; Memori Cloud is SaaS; BYODB exists but how much of the pipeline runs without the hosted service is not spelled out.
- OpenClaw/Hermes are listed as first-class integrations but are MemoriLabs-adjacent rather than mainstream frameworks.

## Source

- `raw/research/oss-agent-memory/07-memori.md` (https://github.com/GibsonAI/memori → MemoriLabs/Memori) — project README; vendor/tool documentation. Captured 2026-05-24.
- `raw/research/oss-agent-memory/13-memori-paper.md` (https://arxiv.org/abs/2603.19935 — *"Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents"*, Borro et al., Memori Labs, March 2026) — captured 2026-05-25 via marker (CPU). Vendor-authored; only Memori's own LoCoMo row is self-run, baselines borrowed from Du et al. 2025.

## Related

- [[mem0]] — closest peer (extract-and-consolidate, OSS + hosted tier); a named benchmark competitor.
- [[supermemory]] — peer extract-pole engine with OSS-client / hosted-core split.
- [[claude-mem]] — shares the capture-from-tool-usage angle, but as a local Claude Code plugin.
- [[conflicts/verbatim-vs-extracted-memory]] — extract pole.
- [[memory-architectures]] — *retrieval-augmented memory stores* family.
- [[claude-code-memory-ecosystem]] — Memori's HTTP MCP server is a cross-tool Level-6 entry.
- [[graphiti]] — Memori reports beating Zep on LoCoMo *overall* (but loses on temporal + open-domain, and the baselines are borrowed not re-run); Zep's own paper-verified numbers live here.
