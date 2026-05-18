# GroupMemBench: Benchmarking LLM Agent Memory in Multi-Party Conversations

GroupMemBench (arXiv 2605.14498, Yang et al., UCSB + Microsoft) introduces the first multi-party memory benchmark with speaker-grounded, Theory-of-Mind-aware adversarial queries, finding that the best memory system reaches only ~46% accuracy and a bare BM25 baseline matches or strictly Pareto-dominates four of the five evaluated agent memory systems. It is the multi-party successor to [[memory/longmemeval]] and, as of May 2026, the strongest matched-corpus empirical evidence for the verbatim/no-extraction pole of [[conflicts/verbatim-vs-extracted-memory]].

## The multi-party gap

All prior memory benchmarks — LoCoMo, LongMemEval, MemoryAgentBench, MemoryBench, EverMemBench — are strictly dyadic (one user, one assistant). GroupMemBench adds:
- Multi-user speakers with distinct participant identities
- Theory-of-Mind vocabulary: speakers hold coexisting, sometimes contradictory beliefs
- Threaded reply structure (multi-level quoting and back-references)
- User-conditioned queries ("what does Alice believe about X?")

No existing memory system was designed or evaluated for these properties.

## Headline results (reported; collect-but-confirm)

All numbers from Table 2 / Section 4, arXiv 2605.14498:

| System | Avg accuracy | Knowledge Update |
|---|---|---|
| **Hindsight** (best) | ~46.0% | 27.1% |
| **BM25** (no LLM ingestion) | ~43.2% | 25.23% |
| A-Mem | ~35.1% | — |
| MemGPT | ~28.2% | — |
| Mem0 | ~25.7% | 4.67% |
| GraphRAG | ~20.6% | — |
| HippoRAG | — | 27.10% |

BM25 achieves ~43.2% cross-domain accuracy at effectively \$0 ingestion cost (one-time inverted-index build, no LLM or embedding calls), strictly Pareto-dominating four of the five agent memory systems. Only Hindsight (~46.0%) beats BM25.

## The load-bearing BM25 result

The paper's central finding: ingestion transformations — fact extraction (Mem0), graph construction (GraphRAG), note rewriting (A-Mem) — "do not, on average, repay their cost in retrievability beyond what raw text already provides" (Section 4.3). On multi-party corpora, these pipelines discard the structural and lexical features (speaker identity, thread structure, exact phrasing) that raw text preserves, costing more while performing worse.

This is the first matched-corpus, controlled benchmark evidence for the verbatim/no-extraction position. Earlier evidence came from [[patterns/direct-corpus-interaction]] (DCI) on workspace-scale corpora; GroupMemBench extends the finding to memory-system ingestion pipelines on conversational corpora.

## Knowledge-Update collapse

Mem0 collapses to ~4.67% on Knowledge Update (vs BM25 ~25.23%) because its extractor appends new statements alongside obsolete ones without speaker-conditioned consolidation. In a multi-party setting, different speakers may hold contradictory beliefs simultaneously — Mem0's ADD/UPDATE/DELETE/NOOP pipeline was designed for a single user's beliefs and does not handle this regime. The contrast with Mem0's favorable LOCOMO/dyadic numbers is stark: different regime, different failure mode.

## Retrieval-vs-reasoning decomposition

Section 4.4 decomposes errors into retrieval failure and reasoning failure. Key findings:
- 41–79% of errors are retrieval failures; given the gold message, GPT-5 reliably synthesises a correct answer.
- **MemGPT is below the diagonal** (Figure 5): it retrieves adequately but answers far worse than retrieval recall predicts — its tiered representation degrades downstream reasoning on multi-party corpora.
- **Term Ambiguity** is the only failure category that survives retrieval: P(correct \| gold retrieved) stays below 40% across all systems; representation (not retrieval) is the wall here.

## Eval methodology

Difficulty is enforced via a Solve-Judge-Refine loop: queries enter the benchmark only after a competent retrieval baseline fails them. This adversarial difficulty enforcement is a methodological refinement over prior benchmarks that use static query generation — it prevents easy questions from diluting the signal.

Six query categories: Information Extraction, Multi-hop Reasoning, Knowledge Update, Temporal Reasoning, Term Ambiguity, Abstention. Abstention is the only category above 77% across systems.

## Enterprise / production implication

Real deployments routinely span group channels and threads (Slack, shared assistants, project threads). The ~46% ceiling and BM25 dominance mean production deployments using dyadic-designed memory systems are silently degraded in any multi-user context. No current system handles user-conditioned retrieval or coexisting beliefs.

## Source

`raw/research/weekly-2026-05-18/04-groupmembench.md`

## Related

- [[conflicts/verbatim-vs-extracted-memory]] — this benchmark is the load-bearing empirical data point for Position 1 / Position 3 (verbatim and no-index poles).
- [[memory/longmemeval]] — dyadic predecessor; GroupMemBench frames itself as the multi-party successor.
- [[memory/memory-architectures]] — adds multi-party benchmark data point; BM25 ≥ neural on this regime.
- [[memory/memory-evolution-survey]] — Storage/verbatim pole empirically corroborated by BM25 result.
- [[memory/mem0]] — collapses on Knowledge Update (~4.67%) vs BM25 (~25.23%) in multi-party regime.
- [[memory/memgpt]] — retrieves adequately but answers below recall (below-diagonal in Figure 5).
- [[patterns/direct-corpus-interaction]] — DCI's no-index thesis independently corroborated by BM25 dominance here.
