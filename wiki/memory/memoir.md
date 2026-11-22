# MEMOIR — judge-gated consolidation + retrospective attribution

**Secondary source, unverified.** An emergent.sh news piece summarizing a reported Nov 5, 2026 arXiv paper (Anand, Raj, Jha, Saha) on MEMOIR, a training-free memory lifecycle for long-horizon agents. No arXiv ID, code or paper text was checked; every number is third-party-reported. Collect-but-confirm until the paper is captured.

## Mechanisms (as reported)

- **Judge-gated consolidation:** a judge verifies answer-relevant evidence survives before any memory merge.
- **Retrospective attribution:** after each query, retrieval priority is updated from which memories supported the answer, replacing static write-time importance. A UCB-style bonus keeps under-exposed memories in play.
- **Training-free, drop-in;** confidence-gated feedback needs no reference answers.

## Reported numbers

- Evidence recall@5 +11.92pp over bare cosine similarity on 1,905 deduplicated LoCoMo QA pairs; confidence-gated feedback +1.50pp; non-deployable oracle +1.84pp (+8.05pp multi-hop).
- Consolidation: text-evidence recall 58.82%→59.08%, store −1.42%, zero losses in 100 audited merges (95% upper bound on loss rate 2.95% — small audit).

## Caveats

Weak baseline (bare cosine); recall, not end-to-end answer accuracy; no comparison to Mem0, Zep, BM25 or raw RAG; recall-vs-use gap unaddressed.

## Source

- `raw/research/weekly-2026-11-22/03-memoir-agent-memory.md` — emergent.sh/news/memoir-lifts-llm-agent-recall-11-9pp-locomo (captured 2026-11-22).

## Related

- [[conflicts/verbatim-vs-extracted-memory]] — gated merge as a hybrid stance
- [[memory/memory-architectures]] — usage-feedback lifecycle instance
- [[memory/mem0]] — LoCoMo origin; extract+consolidate
- [[memory/agent-memory-gem]] — revision/forgetting operators parallel the merge gate
- [[memory/raw-rag-baseline]] — counterpoint evidence; MEMOIR does not compare
- [[memory/forge-decision-context]] — both revise how memory is surfaced at use time
