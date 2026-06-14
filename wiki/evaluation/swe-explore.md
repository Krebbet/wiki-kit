# SWE-Explore

SWE-Explore is a benchmark that isolates **repository exploration** as a distinct coding-agent sub-capability, scoring agents on line-level context selection against trajectory-derived ground truth across 848 multilingual issues. It reveals that current agents locate the right files but fail to cover the specific line spans that successful trajectories relied on — and that this line-level gap is the binding constraint on downstream repair success.

## Source

- arXiv 2606.07297 — "SWE-Explore: Benchmarking How Coding Agents Explore Repositories" (June 2026)
- Raw: `raw/research/weekly-2026-06-14/02-02-swe-explore.md`

## Motivation

SWE-bench and its descendants reduce coding to a binary pass/fail metric that conflates exploration, localization, and patch synthesis. SWE-Explore isolates the **exploration subproblem**: given a bug report, which lines of the repository does the agent need to read before it can write a correct patch?

Ground truth is derived from successful agent trajectories — the intersection of regions read by ≥2 independent agents that resolved the same issue — with LLM-assisted refinement and manual audit. No hand-labeling required at scale.

## Benchmark specification

- **848 instances** across Python (64.5%), Go (9.9%), JavaScript (6.0%) and 7 other languages
- **203 repositories**, sourced from SWE-bench Verified + SWE-bench-Pro + SWE-bench Multilingual
- **Average ground-truth core**: 4.3 files / 4.7 regions / 1,578 lines, embedded in repos averaging 759 files / 180K non-test lines

## Key metrics

| Metric | What it measures |
|---|---|
| HitFile | File-level hit rate: did the agent open the right file? |
| HitReg | Region-level hit rate: did the agent open a region containing core lines? |
| Rec_ℓ | Line-level recall: fraction of core lines actually read |
| nDCG@500 | Ranking quality of explored regions |
| CtxEff | Context Efficiency: useful/total context ratio |

**Context Efficiency (r=0.950)** and **Rec@100 (ρ=0.845)** are the strongest single predictors of downstream repair success.

## Results

### Downstream resolve rates (K=5 explorer output, n=150 validation set)

| Explorer | Resolve rate |
|---|---|
| Oracle (ground truth) | 59.7% |
| CoSIL (iterative code-graph) | 59.3% |
| Codex | 50.3% |
| Mini-SWE-Agent | 50.0% |
| Claude Code | 48.0% |
| OpenHands | 47.7% |
| TF-IDF | 26.0% |
| BM25 | 12.7% |
| Random | 4.7% |

### Agent exploration profiles

All general-purpose coding agents (Claude Code, Codex, OpenHands, Mini-SWE-Agent, AweAgent) converge on nearly **identical exploration profiles**:
- High file-level hit rate (~0.65 HitFile)
- High early ranking (nDCG@500 ~0.90–0.95)
- Low line-level recall (Rec_ℓ ~0.14–0.19)

Swapping the underlying LLM shifts the operating point but does not change the profile shape. Line-level recall is the binding bottleneck.

### Specialized localizers vs general agents

Specialized academic localizers (LocAgent, OrcaLoca, AutoCodeRover) **do not uniformly outperform** general coding agents on exploration:
- LocAgent HitReg 0.472 vs Claude Code 0.531
- AutoCodeRover: Prec=0.680 but Rec_ℓ=0.233 (extremely precise but recall-limited; emits ~1 region)
- **CoSIL is the exception**: Rec_ℓ=0.788, F1=0.602 via iterative code-graph search

### Model comparison on same scaffold

GPT-5.4-mini surfaces more core regions earlier (FUH 0.956 vs 0.927) than GPT-5.4, despite being smaller — the smaller model is more exploration-aggressive.

## Recall threshold effect

Missing core evidence is the dominant failure mode. There is a threshold between α=50–75% of core regions covered: below it, downstream repair fails; above it, moderate redundant context is tolerated by strong patchers. This suggests exploration should aim for high recall rather than precision.

## Contamination caveat

Empty-context baselines on canonical (popular) repositories may be inflated by memorization — they show a dip at α=0→25 under strong patchers. Interpret benchmark numbers on canonical repos cautiously.

## Related

- [[evaluation/swe-bench-pro]] — SWE-Explore builds on SWE-bench-Pro instances; adds line-level ground truth and trajectory-grounded annotation that SWE-bench-Pro lacks
- [[evaluation/swe-cycle]] — complementary: SWE-Cycle adds Env/TestGen phases; both argue binary resolve rate is insufficient; non-overlapping scope
- [[evaluation/agents-last-exam]] — both disaggregate "coding agent" into measurable sub-capabilities
- [[patterns/direct-corpus-interaction]] — DCI agents use grep/rg/head/cat; SWE-Explore's ground-truth extraction counts exactly these read actions; CoSIL's iterative code-graph search is related
- [[patterns/agentic-harness-engineering]] — AHE evolves harnesses to improve agent performance; SWE-Explore isolates exploration as the empirically binding bottleneck, narrowing the improvement target
- [[patterns/harness-design-space]] — SWE-Explore data shows complex harnesses don't outperform simpler ones on the exploration subproblem
- [[memory/longmemeval]] — parallel recall-vs-use gap: LongMemEval shows 40-60% drop from retrieval to answer use; SWE-Explore shows high file-level hit rate but low line-level recall — same structural gap in different domains
