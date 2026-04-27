# GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

UC Berkeley / Stanford / Databricks / MIT (arXiv:2507.19457; ICLR 2026 oral). **Genetic-Pareto** prompt optimizer for compound AI systems: evolves prompts via natural-language reflection + Pareto-based candidate selection, no weight updates. Beats GRPO by up to 20% with up to 35× fewer rollouts on Qwen3-8B across 6 tasks. Optimized prompts transfer cross-model: Qwen3→GPT-4.1-Mini gains +9% over baselines optimized natively on the target. Open code, ICLR oral acceptance.

## Method

Prompt optimization for compound AI systems (multi-module LLM pipelines). Fixes only Π_Φ (prompts); weights Θ_Φ remain frozen — no weight-space RL.

Core loop:

1. Sample rollouts from existing candidate prompts.
2. Extract natural-language **execution + evaluation traces**.
3. **Reflection LM** diagnoses errors and proposes updated module prompts.
4. Evaluate on a minibatch; accept if improved.

**Candidate selection — Pareto illumination**: retain candidates that achieve best-per-task scores on the validation set, prune dominated ones, sample stochastically weighted by task-win count. Adapts MAP-Elites / QD search (Mouret & Clune 2015) to prompt space.

**Optional System-Aware Merge crossover**: identify two candidate lineages that evolved distinct modules and splice the best module-level prompts from each.

Derives from: MIPROv2 (Opsahl-Ong et al. 2024) for the compound-AI-system framing.

## Results

Qwen3-8B aggregate, 6 tasks (HotpotQA, IFBench, HoVer, PUPA, AIME-2025, LiveBench-Math). Table 1:

| Method | Aggregate Δ | Rollouts |
|---|---|---|
| Baseline | 0 | — |
| MIPROv2 | +2.61 | — |
| GRPO | +3.68 | 24,000 |
| **GEPA** | **+9.62** | **678–7,051** |

- GEPA beats GRPO on 5/6 tasks: +19.0, +2.73, +13.66, +5.19, +0.7. GRPO wins only AIME-2025 (38.00 vs 32.00).
- **35× fewer rollouts** in the best case; ≥3× across the board.

GPT-4.1 Mini (Table 2): GEPA+Merge aggregate **+13.33** vs MIPROv2 +5.64, TextGrad +6.11.

**Cross-model transfer**: prompts optimized on Qwen3-8B achieve **+9.00% on GPT-4.1-Mini**, *beating* baselines optimized natively on the target.

**Pareto vs ablations** (Table 3): GEPA +12.44 vs SelectBestCandidate +6.05 vs BeamSearch +5.11.

**Code generation** — NPUEval mean vector utilization 4.25% (GPT-4o baseline) → **30.52%** (GEPA); KernelBench fast1 score 0% → **>20%**.

## Novelty

Genuine new combination within the prompt-optimization family. Prior art: MIPROv2 (instruction + few-shot joint, no evolutionary search), TextGrad (text-based gradient descent, greedy), APO (beam search), Trace / OptoPrime. GEPA's combination of (a) **multi-module reflective mutation** with evaluation-trace feedback, (b) **Pareto-illumination** candidate selection (vs greedy/beam), and (c) **system-aware lineage crossover** is novel.

Headline claim beyond prior work: *instruction-only* optimization with Pareto search now matches or beats joint instruction+few-shot optimization, **reversing Wan et al. 2024's finding** — attributed to improved LLM instruction-following at frontier scale.

## Conflict positions

GEPA's main result extends [[conflicts/grpo-vs-evolution-strategies]] (where [[eggroll]] holds Position A) from **weight-space ES** to **prompt-space evolution**. Different mechanism, same competitive claim against GRPO. Strengthens the Position-A coalition; doesn't resolve the conflict.

## Reproducibility

Code at https://github.com/gepa-ai/gepa. Appendices include full optimized prompts (Appendix L), optimizer configs (E.4), cost breakdowns (E.3). Tied to the DSPy / MIPROv2 ecosystem (overlapping co-authors). No released weights — prompt optimizer only.

## Source

- `raw/research/weekly-2026-04-27/05-gepa-reflective-prompt-evolution.md` — arXiv:2507.19457.

## Related

- [[eggroll]] — parallels: both challenge GRPO dominance with non-weight-update methods. EGGROLL evolves weights, GEPA evolves prompts. Same competitive claim, different mechanism axis.
- [[rlsd-self-distilled-rlvr]] — GEPA bypasses weight updates entirely; RLSD improves GRPO sample efficiency via self-distillation.
- [[huxley-godel-machine]] — both are self-improving systems using evolutionary / tree-search over candidate programs (HGM: clade scoring; GEPA: Pareto illumination).
- [[conflicts/grpo-vs-evolution-strategies]].
- [[watchlist]] — MIPROv2, TextGrad, APO, Trace/OptoPrime, MAP-Elites.
