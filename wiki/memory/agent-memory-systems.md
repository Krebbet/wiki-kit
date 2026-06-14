# Agent Memory: Systems Characterization

Stanford/KU Leuven systems paper (arXiv 2606.06448) presenting the first comprehensive characterization of agent memory as a **computational workload** — benchmarking ten systems across four paradigms on accuracy, latency, energy, storage, and construction cost. Derives ten deployment recommendations for production practitioners.

## Source

- arXiv 2606.06448 — "Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads" (Stanford, KU Leuven, June 2026)
- Raw: `raw/research/weekly-2026-06-14/03-03-agent-memory-systems.md`
- Hardware: single NVIDIA H100 80 GB (vLLM); LLM ladder Qwen3-32B/14B/8B/1.7B; Qwen3-Embedding-0.6B

## Core framing

Agent memory **generalizes RAG from static retrieval to mutable state management**. The memory corpus is produced by the agent's own interaction stream and may be rewritten across sessions. This creates workload properties absent from document-retrieval benchmarks: construction (write) costs dominate serving (read) costs, and store growth compounds across sessions.

## Four-paradigm taxonomy

| Paradigm | Representatives | Characteristic |
|---|---|---|
| I — Long-context passthrough | Raw conversation history | Quadratic prefill cost; U-shaped recall at long lengths |
| II — Flat RAG | BM25, embedRAG | No construction LLM calls; fast, cheap, strong on exact recall |
| III.a — Append-only structured | GraphRAG, HippoRAG v2 | Knowledge-graph construction; high construction cost, strong multi-hop |
| III.b — Consolidating structured | Mem0, SimpleMem | Extract + deduplicate facts; LLM mediates every write; 1:1 embedding calls |
| IV — Agentic control flow | A-Mem, Letta, MIRIX | LLM decides when/what to remember; super-linear cost growth with store size |

## Key findings

### Accuracy vs energy trade-off

- **BM25 achieves highest macro-averaged accuracy (55.8%)** at lowest energy (582 kJ total, 4,128 J/correct-answer)
- Full LLM-mediated systems (Paradigm IV) cost 47× more per correct answer: A-Mem 116,116 J/correct, Letta 185,873 J/correct
- **No single system is Pareto-optimal** across construction cost, per-query latency, and accuracy
- GraphRAG is unusually robust to LLM downscaling: ~47–48% accuracy from Qwen3-1.7B to GPT-4o-mini, because entity-relation extraction degrades gracefully

### Construction cost dominates

- For LLM-mediated systems, **construction energy exceeds total query-phase energy** across 300 queries
- Construction time spans five orders of magnitude: BM25 ~1 ms, Letta ~14h
- Embed traffic is bimodal: GraphRAG batches ~2,300 sequences/call; Mem0 submits 1:1 call-to-sequence per fact before ADD/UPDATE/DELETE

### Per-query serving latency

- Range across systems: Mem0 <0.1 s to long-context ~38 s (OpenAI API, GPT-4.1-mini)
- Retrieval latency stays nearly flat as store grows (sub-linear index lookup) — read cost decoupled from history length
- Tail latency spread: deterministic systems p95/p50 ~1.3–1.6×; LLM-bounded systems up to 5.9× (GraphRAG)

### Storage footprint

- Range ~9× at 1 M tokens: HippoRAG v2 ~62 MB to embedRAG ~7 GB per user
- At 100K users: 0.7 TB (HippoRAG v2) to 6.2 TB (embedRAG)

### Agentic systems super-linear cost growth

Paradigm IV systems scale **super-linearly** in LLM token cost as memory grows — per-ingestion cost rises with store size. Letta diverges steeply beyond 256K tokens.

### MIRIX capability floor

Systems with strict output contracts have hard capability floors: MIRIX fails entirely at Qwen3-1.7B (malformed JSON tool calls) — the store becomes unusable below the model threshold.

### No pruning/forgetting by default

All evaluated systems accumulate memory monotonically. No built-in pruning or forgetting policy. This is an open deployment concern for long-running agents.

## Deployment implications

1. BM25 is the default if latency and cost are constrained — it outperforms LLM-mediated systems on aggregate accuracy at a fraction of the energy
2. Separate construction (write-heavy prefill) from serving (read) workloads — co-location creates interference
3. Async construction is forced for inter-session use with slow-construction systems (Letta, MIRIX) — staleness trade-off is explicit
4. Monitor J/correct-answer, not just accuracy — energy per correct answer varies 47×
5. Model capability sets a hard floor for Paradigm IV systems; don't deploy MIRIX/A-Mem class systems below the validated LLM size
6. Per-user storage estimates at 1 M tokens vary 9× — plan accordingly at scale

## Relation to existing memory benchmarks

- Benchmark: **MemoryAgentBench** (primary workload in this paper)
- BM25 #1 result corroborates [[memory/groupmembench]] (BM25 ~43.2% Pareto-dominates extraction-based systems on GroupMemBench) and [[memory/evomembench]] (BM25 competitive on knowledge tasks) — cumulative evidence for the no-extraction pole across three independent benchmarks

## Related

- [[memory/memory-architectures]] — five-family taxonomy gets empirical cost data per paradigm; this paper's four-paradigm taxonomy is a system-oriented complement
- [[memory/mem0]] — Mem0 characterized: <0.1 s per-query latency (confirmed), 32% accuracy on LongMemEval_S_*, ~4h construction, ~4,878 kJ
- [[memory/memgpt]] — Letta (MemGPT lineage): worst energy efficiency (185,873 J/correct), super-linear token cost growth
- [[memory/longmemeval]] — LongMemEval_S_* is the primary workload; extends with cross-system cost profiling
- [[memory/groupmembench]] — BM25 dominance finding corroborated here on a different benchmark
- [[memory/evomembench]] — parallel BM25 competitive finding; energy data added here
- [[memory/agent-memory-gem]] — GEM (arXiv 2605.26252) provides theoretical correctness conditions; this paper provides empirical cost characterization — complementary
- [[conflicts/verbatim-vs-extracted-memory]] — this paper extends the BM25/verbatim pole case; but shows structure-augmented systems win on harder sub-tasks (temporal, multi-hop)
