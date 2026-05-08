# AIRS-Bench (FAIR at Meta, 2026)

20-task suite for evaluating frontier AI research-science agents on the *full* scientific pipeline — hypothesis generation, implementation, experimentation, iterative analysis. Tasks are sourced from peer-reviewed SOTA ML papers (2020–2025), provide *no* baseline code to the agent, run for 24 hours each on one H-200 GPU, and span seven categories from molecules and time series to code and math. The headline result: agents exceed human SOTA on **4/20 tasks** but fail to match it on the other 16, and even when they win, they don't reach the theoretical performance ceiling. Across all 14 tested LLM × scaffold combinations, the average normalised score is **24.1%**, valid-submission rate **59.3%**, and only **1.58%** of agent-task seed combinations exceed SOTA. The benchmark is open-source at `github.com/facebookresearch/airs-bench`.

## What gap AIRS-Bench fills

Prior research-agent benchmarks fall into one or more of three traps that AIRS-Bench avoids:

- **Kaggle-sourced tasks** (MLE-Bench, DSBench): no AI-research data, no full scientific-method coverage.
- **Code-reproducibility benchmarks** (SWE-Bench, CORE-Bench, CSR-Bench): supply baseline code, so agents start from a partial solution.
- **Short/medium horizon, low GPU budget**: doesn't reflect the compute or thinking-time profile of real ML research.

Plus a contamination defence: tasks come from papers published 2020–2025 with SOTA scores and methods withheld from the agent.

## The 20 tasks

| Category | Count | Examples |
|---|---|---|
| Molecules & Proteins ML | 5 | QM9 properties (R²Abs, U0, Cv, G); GraphRegressionZinc |
| Question Answering | 4 | DuoRC, ELI5, FinQA, SQuAD |
| Text Extraction & Matching | 3 | Coreference (Winogrande, SuperGLUE WSC), TextualSimilarity SICK |
| Time Series | 3 | SolarWeekly, KaggleWebTraffic, Rideshare (MAE/MASE) |
| Text Classification | 2 | SentimentAnalysis Yelp, TextualClassification SICK |
| Code | 2 | CodeRetrievalCodeXGlue, CodeGenerationAPPS |
| Math | 1 | MathQuestionAnswering SVAMP |

Tasks were initially sourced from PapersWithCode leaderboards (~100 candidates from ~85 papers), then filtered to 20 based on tractability, dataset availability via HuggingFace, and SOTA published 2020–2025.

## Methodology

- Each task is a `{problem, dataset, metric}` triplet. Agent receives the full task spec; *no* baseline code.
- Agent must generate code that trains a model and produces a `submission.csv`. AIRS-Bench's `evaluate.py` runs the code and scores it against held-out test labels.
- 24-hour budget per task on one H-200 GPU; ≥10 seeds per task.
- HuggingFace checkpoints accessible (most recent model from 2021); internet permitted.
- **14 agents tested** (LLM × scaffold combinations):
  - LLMs: Code World Model (CWM), o3-mini, gpt-oss-20b, gpt-oss-120b, GPT-4o, Devstral-Small 24B
  - Scaffolds: One-Shot (AIRA-dojo Draft), Greedy (AIRA-dojo tree search), ReAct (MLGym sequential)
- Three metrics: mean valid-submission rate (VSR), average normalised score (0=worst observed, 1=SOTA, >1=exceeds SOTA via "march of 9s" log transform), Bradley–Terry Elo with human SOTA as an additional player.

## Headline result

> "Our results show that agents exceed human SOTA in four tasks but fail to match it in sixteen others. Even when agents surpass human benchmarks, they do not reach the theoretical performance ceiling for the underlying tasks. These findings indicate that AIRS-Bench is far from saturated and offers substantial room for improvement."

Supporting numbers: overall average normalised score **24.1%**; overall VSR **59.3%** (even *submitting* a valid solution is non-trivial); only **1.58%** of agent-task seed combinations exceed SOTA; the Elo gap between human SOTA and the top agent is described as "sizeable."

## The 4 SOTA-beating wins

| Task | SOTA | Agent | Winner |
|---|---|---|---|
| TextualClassification SICK Accuracy | 0.90 | 0.93 | Greedy gpt-oss-120b (stacked RoBERTa-large + DeBERTa-v3-large) |
| TextualSimilarity SICK Spearman | 0.85 | 0.89 | Greedy gpt-oss-120b |
| Coreference Winogrande Accuracy | 0.85 | 0.88 | Greedy gpt-oss-20b |
| TimeSeries Rideshare MAE | 1.185 | 1.153 | Greedy CWM (Bi-directional GRU vs SOTA's general transformer) |

## Difficulty pattern by category

- **Easiest (agents win or come close)**: Text Classification/Similarity (SICK), Molecular Property Prediction (QM9). Pretrained chemistry models give agents a leg up in the molecules tasks.
- **Medium**: NLP question answering — reading comprehension (SQuAD).
- **Hard / expert (effectively unsolved)**: long-form QA (ELI5), numerical QA (FinQA), time series (KaggleWebTraffic), and the entire Code (APPS, CodeXGlue) and Math (SVAMP) categories — near-zero normalised scores.

The clean signal: agents are competitive on *pattern-recognition-with-strong-priors* tasks and absent on tasks requiring *novel symbolic synthesis*.

## Comparison to peer evals

| Benchmark | AI Research Data | Long Horizon | No Baseline | High GPU | Full Scientific Method |
|---|---|---|---|---|---|
| AIRS-Bench (this) | ✓ | ✓ (>12h) | ✓ | ✓ (H-200) | ✓ (H+I+E+A) |
| MLE-Bench (75 Kaggle tasks) | ✗ | ✓ | ✓ | ✗ | partial |
| RE-Bench (METR, 7 tasks) | ✗ | medium | ✓ | medium | partial |
| SWE-Bench | ✗ | short | ✗ | CPU | ✗ |
| PaperBench (20 ICML papers) | ✓ | short | ✓ | low | replication only |

AIRS-Bench's distinctive combination — AI-research data + long horizon + no baseline + high GPU + full scientific method (hypothesis + implementation + experimentation + analysis) — is what makes it a peer to [[swe-bench-pro]] for autonomous research agents specifically.

## Self-documented limitations

- **Community SOTA infrastructure is patchy** — no unified machine-readable platform; tracking up-to-date SOTA gets harder as the submission tsunami grows.
- **Agent failure modes** — formatting errors, failure to save intermediate results, context overflow causing performance deterioration, misaligned behaviour from long agentic traces.
- **Human bottlenecks on task onboarding** — current semi-manual creation/review process limits scaling to more tasks or new domains.
- **Uniform restrictions** — same compute/time per task may penalise some categories more; lifting them would improve performance but reduce comparability.

## Why it matters

- **First eval purpose-built for autonomous research agents.** [[ai-scientist-v2]] is the system; [[paperorchestra]] is the writing pipeline; AIRS-Bench is the evaluation infrastructure that quantifies what such systems can actually accomplish against known SOTA.
- **Concrete ceiling on agent capability.** 24.1% average score and 1.58% SOTA-beating rate is the cleanest measurement in the wiki of how far autonomous research agents are from human ML researchers — and where the gap is largest (code, math, long-form reasoning).
- **Documents the "context overflow" failure mode in research-agent settings.** Section 7 of the paper names context overflow as a primary cause of agent performance deterioration on long-horizon tasks — direct empirical support for the [[topology-taxonomy#long-horizon-context-loss]] thesis.
- **Open-source.** Tasks and harness available at `github.com/facebookresearch/airs-bench`, enabling third-party evaluation.

## Source

- `raw/research/long-horizon-context/12-13-airs-bench-pdf.md` (captured 2026-04-25 from https://arxiv.org/pdf/2602.06855 via marker on CPU; figures preserved in `assets/13-airs-bench-pdf/`)

## Related

- [[swe-bench-pro]] — peer benchmark for coding agents; AIRS-Bench is the research-agent counterpart.
- [[agents-md-eval]] — peer eval; AGENTbench tests interventions, AIRS-Bench tests capability ceilings.
- [[ai-scientist-v2]] — the autonomous research agent that AIRS-Bench is purpose-built to measure.
- [[paperorchestra]] — the standalone-writer pipeline; complementary to AIRS-Bench's full-pipeline eval.
- [[topology-taxonomy#long-horizon-context-loss]] — context overflow named as a primary failure mode in Section 7.
- [[memory-architectures]] — agent failure modes (context overflow, intermediate-result loss) map directly to memory-architecture deficits.
