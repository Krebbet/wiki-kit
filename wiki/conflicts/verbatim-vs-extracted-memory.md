# Conflict: Verbatim storage vs extracted-fact consolidation

**Status:** OPEN — empirical evidence is mixed and depends on regime (corpus scale, query type, retrieval metric vs end-to-end QA metric).

Two production memory libraries operating in the same family of [[memory-architectures]] (*retrieval-augmented memory stores*) have made directly opposing design commitments on whether to summarise / extract or store verbatim.

## Position 1 — Verbatim, never summarise: [[mempalace]]

From `CLAUDE.md` of the project: *"Verbatim always — Never summarize, paraphrase, or lossy-compress user data. The system searches the index and returns the original words. If a user said it, we store exactly what they said. This is the foundational promise."*

Mechanism: chunk transcripts into ~800-character drawers, store as ChromaDB documents, retrieve with cosine similarity over drawer text. The wings/rooms/halls structure is metadata-scoping over the verbatim corpus, not transformation. The closet layer (compact-pointer index) optionally adds extracted topic/entity keys but the headline benchmark path bypasses it.

**Argument for the position** (paraphrased from MISSION.md and CLAUDE.md): existing memory systems felt like *"large empty warehouses where you just dump huge amounts of info"*; LLM-mediated summarisation introduces drift and forgets the user's exact words; storing verbatim is the only way to honour the promise *"the system searches the index and returns the original words."* 100% recall is the design requirement.

**Reproducible evidence:** 96.6% R@5 on [[longmemeval]] in raw mode (verbatim drawers + ChromaDB cosine, no LLM, no API key) — independently reproduced by [@gizmax (issue #39)](https://github.com/MemPalace/mempalace/issues/39).

## Position 2 — Extract and consolidate: [[mem0]]

From the Mem0 paper (arXiv 2504.19413): two-phase incremental pipeline runs an LLM extraction function `φ(P) → Ω` on each new message pair, producing candidate facts; an update phase classifies each candidate against existing memories as ADD / UPDATE / DELETE / NOOP via function calling.

Mechanism: facts (not transcripts) are the unit of storage. Mem0g extends to a labelled directed graph `(V, E, L)` with entity nodes, relationship edges, and conflict-detection on relationship invalidation.

**Argument for the position** (from the paper): full-context approaches face a *"reasoning through irrelevant material"* problem — quality degrades, latency and cost inflate. Selective retrieval of consolidated facts maintains near-full-context answer quality at *91% lower p95 latency and >90% lower token cost* on LOCOMO. The mem0 token footprint is 1,764 retrieval tokens average vs 26,031 for full context.

**Reproducible evidence:** LOCOMO J = 66.88 base / 68.44 graph; full-context J = 72.90 (Mem0 trades ~6pp accuracy for the latency/cost reduction).

## What the [[longmemeval]] paper says

The ICLR 2025 LongMemEval paper, neutral on either project, recommends a **hybrid** at the index layer (§5.3): *"While using a flat index with the memory values themselves as the keys is a strong baseline, further expanding the keys with extracted user facts improves both memory recall (9.4% higher recall@k) and downstream question answering (5.4% higher accuracy)."*

That is: keep verbatim values, but enrich the keys with extracted facts. MemPalace's intended architecture (closets-as-keys → drawers-as-values) gestures at this hybrid; MemPalace's benchmarked configuration (raw ChromaDB over drawer text) does not. Mem0 inverts the hybrid — the extracted fact is both key and value.

## Reconciling axes *(synthesis — tentative)*

The conflict may be partially resolvable along one or more of these axes; the wiki has no empirical bridge yet.

| Axis | Verbatim wins when… | Extraction wins when… |
|---|---|---|
| **Corpus scale** | Corpus fits comfortably in storage and retrieve-everything-then-rerank is feasible (≤ ~10M tokens) | Multi-year corpora where retrieve-all is infeasible; context-stuffing breaks down |
| **Query type** | "What did I say about X?" — exact-words questions, single-fact recall, citation grounding | Multi-session reasoning, knowledge updates, temporal inference across many fragments |
| **Trust budget** | User does not trust LLM to faithfully extract / summarise their words | User accepts faithful-summary tradeoff for 90% latency reduction |
| **Metric** | Retrieval recall (`recall@k`) — verbatim is hard to beat at finding the relevant text | End-to-end QA accuracy — extracted facts already pre-digest the multi-step reasoning |

These axes are speculative; the wiki does not yet have a benchmark that directly compares verbatim-MemPalace and extracted-Mem0 on the *same* metric across the *same* corpus scale.

## The scale-ceiling argument *(claim to confirm)*

Third-party reviews of [[mempalace]] argue that verbatim-everything has a scale ceiling: a year of daily agent conversations produces ~10M tokens, at which point retrieve-everything-then-let-the-LLM-sort-it-out is no longer feasible and selective retrieval becomes mandatory. The verbatim camp's response (per `MISSION.md` and the `CLAUDE.md` design principles) is that the discipline is precisely about *preserving* the original words for audit and citation grounding, with retrieval quality as a downstream optimisation problem to be solved within the discipline rather than around it. No matched-scale benchmark currently arbitrates this.

## Status — why this is OPEN

A direct empirical comparison would require:
- Running both libraries on the same corpus at multiple scales (e.g. 100k, 1M, 10M tokens).
- Reporting both retrieval recall and end-to-end QA accuracy on the same question set.
- Holding the LLM reader constant.

No such comparison exists in the captured sources. Until one does, the wiki keeps both positions documented and recommends practitioners pick by corpus-scale and metric they actually care about.

## Source

- [[mempalace]] (and `raw/research/mempalace/01-readme.md`, `06-claude-md.md`, `02-mission.md` for the verbatim-discipline argument; `09-vectorize-review.md` for the scale-ceiling argument)
- [[mem0]] (and `raw/research/memory-management/07-04-mem0.md` for the extraction-discipline argument and LOCOMO numbers)
- [[longmemeval]] (and `raw/research/mempalace/11-longmemeval-paper.md` for the hybrid recommendation)

## Related

- [[memory-architectures]] — both systems live in the *retrieval-augmented memory stores* family.
- [[mempalace]] — verbatim position.
- [[mem0]] — extraction position.
- [[longmemeval]] — academic source recommending the hybrid (verbatim values + fact-augmented keys).
- [[generative-agents]] — historical antecedent of the extraction position (memory-stream summaries via the recency × importance × relevance scoring formula).
