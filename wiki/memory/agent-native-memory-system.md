# Agent-Native Memory System (arXiv 2606.24775)

*"Are We Ready For An Agent-Native Memory System?"* — SJTU/Tsinghua/MemTensor, June 23, 2026. Systematic evaluation of 12 agent memory systems across 5 benchmarks and 11 datasets, reframing memory as a data-management lifecycle problem and identifying a no-universal-winner result.

## Framework: Four-Module Decomposition

The paper introduces a formal four-module framework for agent memory:
- **R (Representation + Storage)**: how memories are structured and persisted
- **S (Extraction)**: how raw agent experience becomes stored memories
- **Q (Retrieval + Routing)**: how memories are located and returned at query time
- **U (Maintenance)**: how memory is updated, consolidated, and invalidated over time

This is a more formal decomposition of the write-manage-read loop from [[memory/memory-architectures]].

## Key Empirical Findings (9 findings)

1. **No universal winner**: composite hybrid systems (MemoryOS, MemOS) come closest to cross-workload robustness, but each task type has a different winner.
   - Knowledge update: Zep leads (44.4 Substring EM / 36.8 ROUGE-L F1 on LongMemEval)
   - Multi-party chat: MemoryOS leads
   - Task execution: MemoChat leads
   - Raw EM: Long Context model leads on DB-Bench (48.20 EM — above all memory systems)

2. **Raw long-context retrieval is still competitive** on temporally-ordered factual queries: Long Context achieves 48.20 EM on DB-Bench vs. best memory system MemOS at 46.32. This challenges the assumption that external memory always wins at context-window limits.

3. **Verbatim raw storage beats abstraction for factual recall** on LoCoMo: LightMem User-Only Raw (24.2 EM / 38.9 Ans. F1) outperforms User-Only Summary (8.5 / 15.6) and User-Only Compressed (23.6 / 38.6) — a strong empirical signal for Position 1 in [[conflicts/verbatim-vs-extracted-memory]].

4. **Fact-extraction approaches struggle with dynamic updates**: Mem0 achieves only 15.6 Substring EM / 17.1 ROUGE-L F1 on LongMemEval Knowledge Update vs. Zep at 44.4 / 36.8. Root cause: fact-extraction lacks timestamp-based invalidation in its vector-only variant.

5. **Fine-grained extraction degrades multi-hop reasoning**: MemOS Fine Memorize drops to 2.5 EM / 5.0 Ans. F1 on LoCoMo vs. Fast Memorize at 25.5 / 40.8 — each compression layer discards context needed for downstream reasoning chains.

6. **Retrieval is an evidence-completion problem, not top-1 ranking**: A-MEM and MemTree reach Recall@10 of 69.5 and 80.5 on LoCoMo; SimpleMem's high Recall@1 (39.0) degrades sharply at longer evidence distances.

7. **Localized maintenance is dramatically cheaper**: LightMem at 3.67 s/query vs. Cognee at 116.5 s and Zep at 155.1 s; on LongBench, Mem0 and A-MEM balloon to 374 s and 552 s vs. LightMem at 17.3 s. Comparable or higher normalized utility at ~20× lower latency.

8. **Adding retrieval reflection yields no gain**: SimpleMem Planning Only (90.6 Strict Recall) beats Planning + Reflect (88.6) — extra deliberation adds overhead without improving routing.

9. **Conservative memory consolidation is the safest maintenance default**: MemoryOS Conservative-Merge (23.5 Ans. F1) outperforms both default (23.2) and Delayed-Flush (20.6).

## Systems Evaluated (12)

SimpleMem, MemTree, A-MEM, MemoChat, MemOS (several variants), MemoryOS, Mem0, Letta (MemGPT), Zep, Cognee, LightMem, Long Context (baseline).

## Conflict Flags

- **Mem0 knowledge-update**: source reports Mem0 at 15.6 / 17.1 on LongMemEval Knowledge Update. [[memory/mem0]] presents fact-extraction as the production-ready long-term memory approach — this data challenges that claim specifically for dynamic-update workloads.
- **Long-context competitiveness**: on DB-Bench, Long Context (48.20 EM) beats all 12 memory systems. [[memory/memory-architectures]] and [[memory/memgpt]] position external memory as the solution to context limits — the result suggests the boundary condition is workload-dependent.

Both conflicts are additive to the open [[conflicts/verbatim-vs-extracted-memory]] — no resolution required this run.

## Source

- Raw: `raw/research/weekly-2026-06-28/02-agent-native-memory-system.md`
- arXiv: https://arxiv.org/abs/2606.24775
- Captured: 2026-06-28

## Related

- [[memory/memory-architectures]] — five-family taxonomy; this paper's R/S/Q/U framework is a more formal decomposition of the same space
- [[memory/mem0]] — benchmarked directly; fact-extraction struggles on knowledge-update tasks
- [[memory/memgpt]] — Letta benchmarked (17.8 / 5.7 on Knowledge Update, near bottom)
- [[memory/longmemeval]] — one of the five benchmark workloads used
- [[memory/groupmembench]] — independent corroboration: BM25 beats extraction systems on multi-party
- [[conflicts/verbatim-vs-extracted-memory]] — OPEN conflict; this paper adds strong empirical support for the verbatim side
- [[proposals/memory-system-architecture]] — localized-maintenance and late-filtering findings directly inform the Librarian/Worker proposal
