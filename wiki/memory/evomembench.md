# EvoMemBench: Benchmarking Agent Memory from a Self-Evolving Perspective

EvoMemBench (arXiv 2605.18421, DSAIL-Memory) evaluates 15 agent memory methods across a 2×2 axis — scope (in-episode vs. cross-episode) × content (knowledge-oriented vs. execution-oriented) — yielding four settings: INEP-KNOW, INEP-EXEC, CROSSEP-KNOW, CROSSEP-EXEC. Across six datasets and 800–2800 samples each, the central finding is that no single memory family generalises across all four quadrants: strong long-context LLMs (Gemini-3-Flash) and sparse retrieval (BM25) match or beat extraction-based systems on knowledge tasks, while procedural memory (ReasoningBank, AWM) leads on execution tasks, and memory methods as a whole provide the largest gains at tight context budgets with diminishing returns above 64K. All memory-augmented experiments use **DeepSeek-V3.2 as backbone**; absolute numbers are not directly comparable to [[memory/groupmembench]] (GPT-4o backbone) or [[memory/longmemeval]] (commercial assistant baselines).

## The 2×2 Axis

| | Knowledge-oriented | Execution-oriented |
|---|---|---|
| **In-episode** | INEP-KNOW | INEP-EXEC |
| **Cross-episode** | CROSSEP-KNOW | CROSSEP-EXEC (TOOL / WEB / EMB) |

This scope axis — _when_ memory is used (within vs. across episodes) — is **orthogonal** to [[memory/memory-evolution-survey]]'s Storage→Reflection→Experience axis, which describes _cognitive abstraction depth_. Both papers use "self-evolving" or "evolution" in their titles; they are not the same taxonomy. EvoMemBench's cross-episode accumulation is closest to the survey's Experience tier, but the survey's axis is about representation depth, not session boundary.

## Benchmark Setup

**Six datasets:**

- INEP-KNOW: MemoryAgentBench (2800 samples — Accurate Retrieval 2000 + Selective Forgetting/FactConsolidation 800); includes LME-S* sub-tasks from [[memory/longmemeval]].
- INEP-EXEC: BFCL-MultiTurn-LongContext (800 samples, 4 categories); evaluated at 4 context budgets (16K / 32K / 64K / 128K).
- CROSSEP-KNOW: CL-Bench (884 samples, 120 contexts, difficulty split by DeepSeek-V3.2 baseline tertiles).
- CROSSEP-TOOL: BFCL-MultiTurn-Base (800 samples).
- CROSSEP-WEB: xbench-DeepSearch (100) + WebWalkerQA (170).
- CROSSEP-EMB: ALFWorld (200 samples, 6 task categories).

**15 memory methods** (all on DeepSeek-V3.2):

- Retrieval-augmented: BM25, Qwen3-Emb-4B, GraphRAG
- Short-term compression: MemAgent, MemoBrain
- General long-term: [[memory/mem0|Mem0]], A-MEM, MemOS, MemoryOS
- Procedural long-term: AWM, SkillWeaver (see [[patterns/skillos]]), AgentKB, ACE, ReasoningBank
- Meta-evolution: MemEvolve

Long-context LLM baselines: Gemini-3-Flash, GPT-5-mini, DeepSeek-V3.2 (no-memory).

Protocols: in-episode memory initialised and cleared per episode; cross-episode memory persists within an environment/context group and resets at group boundaries. Retrieval top-k=10 (knowledge), top-k=3 (execution).

## Central Findings

### (a) Long-context baselines and BM25 beat extraction on INEP-KNOW

Gemini-3-Flash ranks #1 overall (rank 1.0) on INEP-KNOW; BM25 ranks #2 (rank 4.17), ahead of Mem0 (4.50) and A-MEM (4.83). GPT-5-mini ranks #3 (3.0) as a baseline. On the hardest sub-task — FactConsolidation multi-hop (FC-MH) — Gemini-3-Flash scores 58%, GPT-5-mini 24%, while BM25 = 7%, Mem0 = 5%, A-MEM = 4%, MemOS = 1%. The LME-S* sub-task from [[memory/longmemeval]] shows the same pattern: Gemini-3-Flash 83% vs. DeepSeek-V3.2 32%, reinforcing that sufficient context window supplants extraction-based memory on knowledge retrieval.

Section 5.2.5 states explicitly: "strong memory-free long-context baselines remain highly competitive, and explicit memory provides the clearest gains only in some settings."

This is a **second independent empirical data point** for the verbatim/no-extraction pole of [[conflicts/verbatim-vs-extracted-memory]], after [[memory/groupmembench]]'s multi-party finding. Both papers find BM25 ≥ or ≈ extraction-based systems on knowledge tasks; EvoMemBench extends coverage to single-session and cross-episode settings. See the knowledge-vs-execution asymmetry below for the important caveat: extraction-based methods recover competitive standing on execution tasks.

### (b) Memory helps most at constrained context budgets (INEP-EXEC)

| Context budget | DeepSeek-V3.2 no-memory | Best memory method | Delta |
|---|---|---|---|
| 16K | 28.5% | 43.0% (ReasoningBank) | +14.5 pp |
| 32K | 35.5% | 49.5% (ReasoningBank) | +14.0 pp |
| 64K | 45.3% | 53.1% (AWM) | +7.8 pp |
| 128K | 39.5% | 48.0% (ReasoningBank) | +8.5 pp |

Above 64K, gains shrink substantially. Some methods fall _below_ the no-memory baseline at 128K (MemAgent: 37.0% vs. 39.5%).

### (c) Procedural memory leads execution

ReasoningBank and AWM consistently top INEP-EXEC rankings (ReasoningBank: 43.0 / 49.5 / 48.0 at 16K / 32K / 128K; AWM best at 64K: 53.1). On CROSSEP-EXEC, A-MEM ranks #1 overall (rank 5.2), ReasoningBank #2 (5.4). Domain matters: retrieval-augmented memory leads tool use (avg rank 5.43), general long-term memory leads web search (avg rank 5.38), procedural long-term memory leads embodied AI (avg rank 5.60 — ALFWorld).

### (d) Knowledge-vs-execution asymmetry

Extraction-based general long-term methods (Mem0, A-MEM, MemOS) underperform BM25 and no-memory baselines on knowledge tasks but are meaningfully more competitive on CROSSEP-EXEC tasks. On CROSSEP-KNOW easy, DeepSeek-V3.2 no-memory = 52.1%; Qwen3-Emb-4B best memory method at 50.0%; Mem0 = 44.6%, A-MEM = 43.8%. On CROSSEP-KNOW hard, no-memory = 0.0%; ACE = 13.0%, BM25 = 10.1% lead; general long-term methods (Mem0 etc.) trail. This asymmetry is load-bearing for [[conflicts/verbatim-vs-extracted-memory]]: the no-extraction pole is strongest on knowledge tasks; extraction-based methods regain ground on execution tasks.

### (e) Short-term compression hurts execution-state tracking

MemAgent (26.0) and MemoBrain (25.0) fall _below_ the DeepSeek-V3.2 no-memory baseline (28.5) on INEP-EXEC at 16K. MemoBrain also below baseline at 32K (30.5 vs. 35.5). Root cause: execution-state tracking requires fine-grained details — exact tool-call arguments, entity references, intermediate results — that summary compression discards. [[memory/memgpt]]'s tiered-context framing is the antecedent for these short-term families; EvoMemBench shows that, on execution tasks, compression is counterproductive at constrained budgets.

### (f) Token cost: memory methods 2–5× the no-memory baseline

On CROSSEP-KNOW, Mem0 uses ~21K–26K tokens per domain vs. DeepSeek-V3.2 ~5.6K–8.1K; A-MEM ~31K–35K. Memory-augmented methods impose a 2–5× token overhead before yield is considered. At easy difficulty, most methods underperform the no-memory baseline — the efficiency trade-off is unfavourable except at hard difficulty or tight context.

## Interpretation Notes

- **Backbone constraint:** All 15 methods run on DeepSeek-V3.2. The long-context baselines (Gemini-3-Flash, GPT-5-mini) use their native context window without a memory wrapper. Cross-backbone comparison with GroupMemBench (GPT-4o) or LongMemEval (commercial assistants) is unreliable.
- **Cross-environment transfer:** Tool-use memory transfer is stable across BFCL sub-environments (similar decision structure). ALFWorld transfer is neutral-to-negative — sub-environments differ substantially in task requirements, undermining procedural generalisation.
- **[[memory/reflexion]]** is the canonical antecedent for procedural/meta-evolution families (AWM, ReasoningBank, MemEvolve) — verbal RL / episodic feedback as a skill-building mechanism.
- **[[patterns/skillos|SkillWeaver]]** is one of the five procedural methods evaluated; it performs well on embodied AI but ranks mid-table on tool use (avg rank 12.3). SkillOS (parallel RL-trained skill curator) is not evaluated here.
- **[[memory/mem0|Mem0]]** is moderately competitive on knowledge retention but weak on revision (FC-MH: 5%) and cross-episode easy tasks (43.8% vs. 52.1% no-memory) — consistent with GroupMemBench's Knowledge-Update collapse finding.

## Source

`raw/research/weekly-2026-05-25/02-evomembench.md` · arXiv 2605.18421 · [github.com/DSAIL-Memory/EvoMemBench](https://github.com/DSAIL-Memory/EvoMemBench)

## Related

- [[conflicts/verbatim-vs-extracted-memory]] — EvoMemBench is a second independent empirical data point for the no-extraction pole on knowledge tasks, and establishes the knowledge-vs-execution asymmetry that nuances the conflict.
- [[memory/groupmembench]] — parallel finding: BM25 Pareto-dominates extraction-based systems on knowledge tasks; different backbone, different corpus (multi-party), same pole.
- [[memory/longmemeval]] — LME-S* sub-tasks directly included in INEP-KNOW; Gemini-3-Flash 83% vs. DeepSeek-V3.2 32% on LME-S* corroborates the long-context-beats-memory finding.
- [[memory/memory-architectures]] — EvoMemBench's five method families map directly onto the five mechanism families; the 2×2 axis adds knowledge/execution × in/cross-episode dimensions for evaluating family fitness.
- [[memory/memory-evolution-survey]] — both use "self-evolving" / "evolution" framing; the axes are orthogonal: EvoMemBench separates by _when_ memory is used (scope), the survey separates by cognitive abstraction depth. Not the same taxonomy.
- [[memory/mem0]] — evaluated; weak on knowledge revision (FC-MH: 5%) and cross-episode easy tasks; consistent with GroupMemBench Knowledge-Update finding.
- [[memory/memgpt]] — tiered-context framing is antecedent for short-term families; EvoMemBench shows compression backfires on execution tasks.
- [[memory/reflexion]] — episodic verbal RL is antecedent for procedural (AWM, ReasoningBank) and meta-evolution (MemEvolve) families.
- [[patterns/skillos]] — SkillWeaver is one of the five evaluated procedural methods; top embodied AI, mid-table tool use.
