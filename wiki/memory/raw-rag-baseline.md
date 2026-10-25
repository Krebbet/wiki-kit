# RAW-RAG: Naive Dense Retrieval Over Raw Chat History as a Memory Baseline

"Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought" (arXiv 2610.30755, Bao et al., Xi'an Jiaotong / SJTU) proposes RAW-RAG, a no-LLM-at-write-time baseline (windowed raw history, dense retrieval, cross-encoder rerank), and reports it ranks first among 12 recent agentic memory systems in 6 of 7 benchmark-model settings. It is an author-run academic preprint with no independent replication, so treat the headline margins as collect-but-confirm. It is the third benchmark-style result in this wiki, after [[memory/groupmembench]] and [[memory/evomembench]], in which a simple retriever over raw text matches or beats extraction systems.

## Mechanism

No LLM extraction, summarization, graph, or mutation. Conversations are serialized with timestamps and image captions, split into 256-token windows with 32-token overlap, and stored in a flat embedding index (text-embedding-3-small; Qwen3 as an alternate). At query time: top 128 windows by cosine similarity, a cross-encoder reranks, the top 15 go to the reader, which handles temporal order and state changes itself. Readers: GPT-4o-mini, GPT-4.1-mini, DeepSeek-V4-Flash. Code: github.com/Litmeb/RAW-RAG.

## Headline results (reported; collect-but-confirm)

- Beats the strongest compared memory system by 0.13 to 5.53 points.
- [[memory/longmemeval]]-S: 87.53 vs Memora 87.40 (0.13 lead, essentially a tie).
- LoCoMo overall: 89.07 (GPT-4o-mini) and 93.70 (GPT-4.1-mini), leading by 0.65-0.95. [[memory/mem0]] scores 66.88 on LoCoMo (GPT-4o-mini) in the same table.
- MEME (GPT-4o-mini): 39.30 vs MemMachine 37.06.
- MemoryAgentBench: 48.32 vs Memora 43.84 (GPT-4o-mini); 53.41 vs Memora 47.88 (DeepSeek-V4-Flash).
- Exceptions: on DeepSeek-V4-Flash MEME, MemMachine (44.71) beats RAW-RAG (43.19), and Full-context (63.17) beats it by about 20 points. Full-context is excluded from "ranks first" and cannot run on MemoryAgentBench.
- LoCoMo and LongMemEval "aligned" settings come from prior comparisons (Appendix A); the authors also note that 14 prior RAG evaluations used weak baselines (coarse chunks, low top-k, no reranking).

## Ablations (MemoryAgentBench)

| Change to RAW-RAG | Total change |
|---|---|
| Add atomic-fact extraction | -19.62 (test-time learning 47.68 -> 15.37) |
| Add raw-summary augmentation | -5.81 (mostly conflict resolution) |
| Add graph expansion | -5.78 (mostly conflict resolution) |
| Remove reranker | -3.92 (Holm p=0.0012) |
| Top-1 retrieval / top-120 | -11.73 / -14.57 |
| Final-k 5-60; chunk size 128-1024 | within ~1.3 / ~0.3 points |

Bootstrap CIs use 20k paired resamples. The reranker and a moderate final-k matter; chunk size does not.

## Why it works: coverage vs utilization

- Coverage (fraction of questions with sufficient retrieved evidence) varies far more across systems than utilization (accuracy given sufficient evidence). On MemoryAgentBench coverage spans 19.07-45.29% vs utilization 80.00-89.71%.
- RAW-RAG has the top coverage (45.29%; 76.35% on MEME) but not the top utilization.
- On MEME tracking/cascade, P(path | result) is 62.34% for RAW-RAG vs MemMachine 56.70, Mem0 47.66, MemU 9.62: retrieved memory needs the relations and dependency order, not just answer values.
- Information loss: a gold-informed "complete-store oracle" improves all 7 systems on MEME, yet the transformed stores stay 7.58-29.38 points below the raw-evidence control. Source-preserving systems (RAW-RAG 57.54%, MemMachine 57.46%) come closest to raw evidence (61.60%). The authors caution the residual gap is not a pure ingestion-loss measure; evidence assembly and lost-in-the-middle effects contribute.

This extends the recall-vs-use framing in [[memory/memory-architectures]]: the bottleneck on these benchmarks is getting the evidence into the retrieved set, which lossy writes undermine.

## Efficiency

On 10 MEME episodes, add-to-ready plus search takes 305.91 s for RAW-RAG vs EverMemOS 9301 s, Mem0 4143 s, MemMachine 3516 s, MemOS 2770 s, EMem 1562 s. The three memory-management additions need 21.6-109.3M LLM tokens and 2.9-8.8 h for Add+Search vs about 12 min for RAW-RAG.

## Caveats

- Author-run baselines; no independent replication.
- Offline conversation benchmarks only: no interactive, multimodal, or deletion/privacy settings. The authors flag storage and privacy concerns for keeping raw history.
- Reader capability matters; weaker readers may benefit from explicit state maintenance.
- LongMemEval and some MEME margins are within noise; Full-context still wins on DeepSeek MEME.
- Not like-for-like with Mem0's own claims (26% J gain over OpenAI memory on LOCOMO): different baseline, different harness. See [[conflicts/verbatim-vs-extracted-memory]].

## Implication for this wiki

Supports the verbatim-first store and text-search-first retrieval ladder in [[proposals/memory-system-architecture]]; a dense+rerank rung over raw windows is a cheap baseline to add before any extraction layer.

## Source

- `raw/research/weekly-2026-10-25/05-naive-rag-vs-agentic-memory.md` (arXiv 2610.30755)

## Related

- [[conflicts/verbatim-vs-extracted-memory]] - matched-benchmark evidence for the verbatim pole (status stays OPEN).
- [[memory/groupmembench]] - parallel: BM25 beats extraction systems on multi-party corpora.
- [[memory/evomembench]] - parallel: BM25/long-context beat extraction on knowledge tasks.
- [[memory/mem0]] - compared baseline.
- [[memory/longmemeval]] - benchmark used.
- [[memory/agent-native-memory-system]] - parallel finding that verbatim storage beats extraction.
- [[memory/memory-architectures]] - coverage vs utilization framing.
- [[memory/memory-evolution-survey]] - Reflection/Experience-style transformation lowers accuracy here.
- [[memory/mempalace]] - verbatim-first discipline corroborated.
- [[evaluation/learn2play-bench]] - parallel: raw histories beat summarized memory.
- [[proposals/memory-system-architecture]] - verbatim-first design.
