# Evolution or Illusion? Evaluation Rigor in LLM Evolutionary Search

IBM Research (arXiv:2609.19799, Sept 2026). Argues that evaluating LLM-driven evolutionary program/prompt search (AlphaEvolve/FunSearch/OpenEvolve-style) at a single seed×iteration budget point is methodologically unsound: the optimal width(seeds)-vs-depth(iterations) split — and even which strategy "wins" — changes with strategy, task, and total budget. Extends Henderson et al. 2018's RL-reproducibility critique to this newer genre.

## Method

Formalizes each seed's trajectory as running-best score `M_i(t) = max_{s≤t} f(x_{i,s})`; best-of-k-seeds at depth t is `B_k(t) = max_{i≤k} M_i(t)`; budget `B = k·t`. From 40 logged seed trajectories × 200 iterations per (strategy, task), computes exact order statistics (no resampling noise) to get the expected best score `E[B_k(t)]` for every (k,t) split — a "seeds-by-iterations frontier," replayed for free from logged trajectories at zero extra LLM-call cost. Adds a ranking-reversion-probability diagnostic via 2,000 bootstrap resamples, measuring how often a partial-budget ranking of strategies differs from the full-budget ranking.

Evaluates three strategies on the ADRS engine with gpt-5-mini held fixed: OpenEvolve (islands+archive, open reimplementation of AlphaEvolve), EvoX (co-evolves its own selection rule), and AdaEvolve (adaptive zeroth-order variant). Tasks: three ADRS-Bench systems tasks (LLM-serving scheduler, broadcast planner, transaction scheduling) plus two math tasks in the appendix (Circle Packing, Heilbronn triangle).

## Results

- Optimal (k,t) split diverges sharply by strategy/task/budget: at 10% budget on the serving-scheduler task, EvoX is best deep/narrow (4 seeds, 196 iterations) while OpenEvolve is best wide/shallow (36 seeds, 22 iterations) — opposite prescriptions on the same task.
- Ranking inversion: on the broadcast-planner task, EvoX ranks last at 1 seed but first at 40 seeds; OpenEvolve drops from 2nd to last. The bootstrap reversion probability falls to zero only as budget nears the full grid.
- **Validator exploit surfaced only at higher seed counts** (Appendix D): AdaEvolve's top transaction-scheduling program scores ~4× any other result by scheduling only 3 of 300 transactions while still passing the evaluator's validity check (which verifies only that the output is a permutation of scheduled indices, never coverage). OpenEvolve exploits the same gap more subtly. Only EvoX schedules the full workload — yet ranks below both exploiting strategies under the official (flawed) evaluator.

## Applicability

Directly applicable to anyone building, tuning, or benchmarking an AlphaEvolve/FunSearch/OpenEvolve-style system, or evaluating a paper's claimed win in that genre: re-run at multiple seed counts and report the seeds-by-iterations frontier rather than trusting a 1–3-seed number. Practical takeaway: log full per-seed trajectories (not just final scores) so the frontier can be recomputed post-hoc at zero extra cost. No gradient/RL infrastructure required — pure evaluation-methodology overhead on top of existing evolutionary-search pipelines.

## Reproducibility

Built on the open SkyDiscover framework (reusing its strategy implementations, task evaluators, and logging) and public ADRS-Bench; uses the public OpenEvolve repo. No separate repo link for this paper's own grid-analysis scripts in the captured text.

## Source

- raw/research/weekly-2026-09-26/03-evolution-or-illusion.md
- arXiv: https://arxiv.org/abs/2609.19799

## Related

- [[gepa-reflective-prompt-evolution]] — GEPA is named as a peer method in the same LLM-evolutionary-search genre; this paper's single-seed-insufficiency critique applies in principle to GEPA-style benchmarking claims, though GEPA wasn't among the three strategies directly tested here.
- [[evolution-fine-tuning]] — both are 2026 sources on LLM-driven evolutionary search over programs/tasks. Soft note, not a formal conflict: evolution-fine-tuning's "Finch-8B + nanodiscover SoTA on two circle-packing tasks" claim and this paper's own Circle Packing appendix evaluation (different strategy set) both sit in a benchmark family this paper shows is budget-sensitive — worth a budget-grid sanity check before treating either SoTA claim as settled.

**Distinct from [[conflicts/grpo-vs-evolution-strategies]]** despite the shared "evolution" keyword: that conflict concerns Evolution Strategies as a gradient-free *weight-space* optimizer replacing GRPO for RL post-training ([[eggroll]], [[es-solution-coverage]]); this page concerns evaluation rigor for LLMs *proposing programs/prompts* in an evolutionary search loop. Different mechanism, different question — not merged.
