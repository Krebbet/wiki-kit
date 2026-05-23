# Conflict: Verbatim storage vs extracted-fact consolidation

**Status:** OPEN — empirical evidence is mixed and depends on regime (corpus scale, query type, retrieval metric vs end-to-end QA metric). *(2026-05-11: a third position — direct corpus interaction with **no separate index at all** — entered the conflict; see [Position 3](#position-3--no-index-direct-substrate-search-direct-corpus-interaction).)*

Two production memory libraries operating in the same family of [[memory-architectures]] (*retrieval-augmented memory stores*) have made directly opposing design commitments on whether to summarise / extract or store verbatim. A May 2026 academic paper has now added a third pole that questions whether a separate index is needed at all.

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

## Position 3 — No index, direct substrate search: [[direct-corpus-interaction]]

From "Beyond Semantic Similarity" (arXiv 2605.05242, May 2026): *no offline index at all.* The agent searches the raw corpus using terminal tools (`grep` / `rg` / `head` / `cat`), moving semantic interpretation downward into the LLM at query time.

Mechanism: bash-mediated traversal of raw files. No embedding model, no top-k API, no extracted facts. Both Position 1's "preserve original" commitment and Position 2's "extract for selection" mechanism are bypassed — there is nothing between the agent and the substrate.

**Argument for the position:** the bottleneck isn't the retriever, it's the *retrieval interface resolution*. Top-k similarity collapses the corpus into a fixed-format ranked list and silently filters out evidence that downstream reasoning cannot recover. Stronger models can extract better evidence from raw text than any retriever can pre-package.

**Reproducible evidence:** on BrowseComp-Plus with matched Sonnet 4.6 backbone, replacing Qwen3-Embedding-8B retrieval with DCI lifts accuracy 69.0 → 80.0 (+11 pp) **while reducing cost 29.4%**. +30.7 pp average over best retrieval-agent baseline on six knowledge-intensive QA benchmarks. Operates well in depth (within-document evidence isolation 48.4 vs 21.7) but poorly in breadth — at 200K docs cost more than doubles for −13.6 pp accuracy; at 400K docs accuracy falls to 37.5%.

**Limitation that bears on this conflict:** DCI is workspace-scale, not 10M-doc enterprise-scale, in its current form. Hybrid (cheap retriever to narrow then DCI within subset) is unexplored.

## What the [[longmemeval]] paper says

The ICLR 2025 LongMemEval paper, neutral on either project, recommends a **hybrid** at the index layer (§5.3): *"While using a flat index with the memory values themselves as the keys is a strong baseline, further expanding the keys with extracted user facts improves both memory recall (9.4% higher recall@k) and downstream question answering (5.4% higher accuracy)."*

That is: keep verbatim values, but enrich the keys with extracted facts. MemPalace's intended architecture (closets-as-keys → drawers-as-values) gestures at this hybrid; MemPalace's benchmarked configuration (raw ChromaDB over drawer text) does not. Mem0 inverts the hybrid — the extracted fact is both key and value.

## Reconciling axes *(synthesis — tentative)*

The conflict may be partially resolvable along one or more of these axes; the wiki has no empirical bridge yet.

| Axis | Verbatim wins when… | Extraction wins when… | No-index DCI wins when… |
|---|---|---|---|
| **Corpus scale** | Corpus fits comfortably in storage and retrieve-everything-then-rerank is feasible (≤ ~10M tokens) | Multi-year corpora where retrieve-all is infeasible; context-stuffing breaks down | Workspace / project-scale corpora (≤ ~100K docs) where the agent can traverse via tools without an index |
| **Query type** | "What did I say about X?" — exact-words questions, single-fact recall, citation grounding | Multi-session reasoning, knowledge updates, temporal inference across many fragments | Multi-hop QA where evidence must be located *within* a document, not just that the document was retrieved |
| **Trust budget** | User does not trust LLM to faithfully extract / summarise their words | User accepts faithful-summary tradeoff for 90% latency reduction | User accepts higher reasoning-tier model dependency for 11+ pp accuracy lift at 29% lower cost |
| **Metric** | Retrieval recall (`recall@k`) — verbatim is hard to beat at finding the relevant text | End-to-end QA accuracy — extracted facts already pre-digest the multi-step reasoning | Within-document **localisation** (DCI 48.4 vs retrieval 21.7) over coverage (DCI 28.0 vs 56.7) |
| **Index existence** | Index exists; values are verbatim text | Index exists; values *are* the extracted facts | **No index**; raw corpus is itself the queryable substrate |

These axes are speculative; the wiki does not yet have a benchmark that directly compares verbatim-MemPalace, extracted-Mem0, and no-index-DCI on the *same* metric across the *same* corpus scale.

**The "Index existence" axis** (added 2026-05-11) is the new structural axis introduced by Position 3. The earlier two positions both assume an index — they disagree on what to put *in* it. DCI questions whether the index needs to exist at all for capable agents on appropriately-sized corpora.

## The scale-ceiling argument *(claim to confirm)*

Third-party reviews of [[mempalace]] argue that verbatim-everything has a scale ceiling: a year of daily agent conversations produces ~10M tokens, at which point retrieve-everything-then-let-the-LLM-sort-it-out is no longer feasible and selective retrieval becomes mandatory. The verbatim camp's response (per `MISSION.md` and the `CLAUDE.md` design principles) is that the discipline is precisely about *preserving* the original words for audit and citation grounding, with retrieval quality as a downstream optimisation problem to be solved within the discipline rather than around it. No matched-scale benchmark currently arbitrates this.

## New data points — 2026-05-18

### (a) GroupMemBench: first matched-corpus empirical evidence for the verbatim/no-extraction side

[[memory/groupmembench]] (arXiv 2605.14498) is the first benchmark to compare extraction-based agent memory systems against a BM25 verbatim baseline on a matched corpus with controlled ingestion. Results (reported; collect-but-confirm): BM25 (~43.2% cross-domain accuracy, ~\$0 ingestion) strictly Pareto-dominates four of five extraction-based systems — Mem0 (~25.7%), MemGPT (~28.2%), A-Mem (~35.1%), GraphRAG (~20.6%). Extraction pipelines lose ~10–20pp absolute to BM25 on average. Only Hindsight (~46.0%) beats BM25.

This is load-bearing for Position 1 (verbatim) and Position 3 (no-index): both positions predict that extraction discards structural and lexical features that matter for retrieval; GroupMemBench's multi-party corpus (speaker identity, thread structure, coexisting beliefs) amplifies exactly those discarded features. The result fills the "no matched-scale benchmark" gap explicitly noted in the reconciling-axes table above.

Knowledge-Update sub-result: Mem0 collapses to ~4.67% vs BM25 ~25.23% — Mem0's extractor appends new statements alongside obsolete ones without speaker-conditioned consolidation, a regime it was not designed for. Caveat: GroupMemBench is multi-party; favorable Mem0 LOCOMO numbers come from a dyadic regime. The conflict is real but involves a regime shift, not a direct contradiction on the same corpus.

### (b) Memory-evolution survey: abstraction-depth framing axis

[[memory/memory-evolution-survey]] (arXiv 2605.06716) adds a third framing axis to this conflict. Its Storage → Reflection → Experience evolutionary taxonomy maps the conflict positions onto a cognitive-depth axis: **Storage = verbatim-fidelity pole** (Position 1), **Reflection = middle ground** (extraction + consolidation, Position 2), **Experience = full-abstraction pole** (cross-trajectory policy priors, not yet a named position in this conflict). [[memory/longmemeval]]'s hybrid recommendation (verbatim values + extracted-fact keys) sits at the Storage/Reflection boundary on this axis. The survey does not resolve the conflict but provides vocabulary for locating each position. The survey also cites evidence (Xiong et al. 2025, Srivastava and He 2025 — collect-but-confirm) that unrestricted memory expansion is detrimental, which is mild pressure against the pure Storage/verbatim pole.

**Status remains OPEN** — GroupMemBench strengthens Position 1/3 empirically on multi-party corpora; the regime dependency (dyadic vs multi-party) means the conflict is not closed, only better bounded.

### 2026-05-23: the doctrinal split as a Claude Code product choice

*Note: the following is illustrative — these instances confirm the axis exists as a product-level choice, not new empirical evidence. They do not change the conflict's status.*

The verbatim-vs-extract axis is now directly visible to practitioners as a choice between Claude Code memory plugins and tools. The positions map cleanly:

- **Extract pole:** [[mem0]] (concrete CC lifecycle hooks — Pre-Compaction, Task-Completed — are the "extraction at named events" doctrine in product form) and [[claude-mem]] (AI compress-and-inject: tool-usage observations are AI-compressed and injected at SessionStart and PreToolUse:Read).
- **Verbatim pole:** [[mempalace]] and mcp-knowledge-graph (verbatim entity/relation/observation triples stored and retrieved via keyword search, no extraction step).
- **A distinct third stance — user-authored structured notes:** Basic Memory stores human-written markdown notes in a structured schema, neither machine-extracted nor raw-trace capture. This sits orthogonally to the verbatim/extract axis: the *content* is authoritative (user-authored), but the representation is structured, and retrieval is index-mediated.

For the full practitioner landscape across these options, see [[claude-code-memory-ecosystem]]. Status remains OPEN; these product instances confirm the doctrinal axis has real-world traction but do not constitute a benchmark comparison.

## Status — why this is OPEN

A direct empirical comparison would require:
- Running all three approaches on the same corpus at multiple scales (e.g. 100k, 1M, 10M tokens).
- Reporting both retrieval recall and end-to-end QA accuracy on the same question set.
- Holding the LLM reader constant.

No such comparison exists in the captured sources. Until one does, the wiki keeps the three positions documented and recommends practitioners pick by corpus-scale and metric they actually care about. DCI's scale ceiling (degrades sharply above 200K docs) and Mem0's claimed scale advantage (multi-year corpora) suggest the three positions may end up partitioning the regime space rather than competing head-on.

## Source

- [[mempalace]] (and `raw/research/mempalace/01-readme.md`, `06-claude-md.md`, `02-mission.md` for the verbatim-discipline argument; `09-vectorize-review.md` for the scale-ceiling argument)
- [[mem0]] (and `raw/research/memory-management/07-04-mem0.md` for the extraction-discipline argument and LOCOMO numbers)
- [[longmemeval]] (and `raw/research/mempalace/11-longmemeval-paper.md` for the hybrid recommendation)
- [[direct-corpus-interaction]] (and `raw/research/weekly-2026-05-11/05-beyond-semantic-similarity.md` for the no-index argument and BrowseComp-Plus / multi-hop QA numbers)
- `raw/research/cc-memory-ecosystem/01-claude-mem-repo.md` — [[claude-mem]] as extract-pole CC plugin instance
- `raw/research/cc-memory-ecosystem/04-basic-memory-cc.md` — Basic Memory as the user-authored third stance
- `raw/research/cc-memory-ecosystem/05-mcp-knowledge-graph.md` — mcp-knowledge-graph as verbatim-pole CC plugin instance

## Related

- [[memory-architectures]] — Positions 1 and 2 live in the *retrieval-augmented memory stores* family; Position 3 challenges the family-defining assumption that an index exists.
- [[mempalace]] — Position 1 (verbatim, with index).
- [[mem0]] — Position 2 (extracted, with index).
- [[direct-corpus-interaction]] — Position 3 (no index, direct substrate search).
- [[longmemeval]] — academic source recommending a *with-index* hybrid (verbatim values + fact-augmented keys); DCI sits at a different point on the new "Index existence" axis.
- [[generative-agents]] — historical antecedent of the extraction position (memory-stream summaries via the recency × importance × relevance scoring formula).
- [[memory/groupmembench]] — 2026-05-18 addition; first matched-corpus benchmark evidence for Position 1/3 (BM25 Pareto-dominates four of five extraction systems on multi-party corpora).
- [[memory/memory-evolution-survey]] — 2026-05-18 addition; Storage→Reflection→Experience axis locates each position on an abstraction-depth continuum.
- [[claude-code-memory-ecosystem]] — 2026-05-23 addition; practitioner landscape where the doctrinal split is visible as a product choice.
- [[claude-mem]] — 2026-05-23 addition; extract-pole CC community plugin (AI-compress, ChromaDB+SQLite).
