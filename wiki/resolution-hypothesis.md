# The Resolution Hypothesis (Agent Evolution)

Large reproducibility study (ShanghaiTech/ByteDance; 7 evolution methods, 6 models, 1,030 evolution runs, >10M LLM calls) arguing frozen-weight agent evolution (prompts, skills, memories, harnesses) stalls because noisy evaluation cannot identify improvements, not because proposers fail to produce them. Selection is near chance (~48.6-49.7% pairwise), and reported margins of a few pp sit within single-run noise. arXiv 2611.23068.

## Method
- Variance decomposition Var(Y^) = sigma^2 (evaluation noise within an artifact) + tau^2 (run-to-run variance in true quality). "Resolution" = smallest true improvement reliably distinguishable from noise. Power: N >= 2((z_{1-a/2}+z_{1-b})/Delta)^2 (tau^2+sigma^2) runs per method.
- Methods: GEPA, SkillOpt-Lite, Trace2Skill, ReasoningBank (text artifact); HarnessLens, Meta-Harness, AHE (harness). Models: GPT-5.4 nano, GPT-5.6 Luna/Terra, DeepSeek-V4-Flash, Kimi-K3, GLM-5.2. Benchmarks: ALFWorld, SpreadsheetBench, OfficeQA, Terminal-Bench v2.1 (9 more re-examined).
- Four experiment groups: variance measurement (8 evolution runs per config, 16 evals/artifact); gain audit (single-sentence rule ablation, repaired evaluations); candidate pools (Proposal and Selection pools, n=100 skills each, Terminal-Bench/DeepSWE); trajectory re-evaluation of every intermediate artifact of 8 SkillOpt-Lite and 8 GEPA runs.
- Predictions: P1 helpful candidates exist; P2 selection is near chance; P3 selection errors compound.

## Results
- sigma 1.0-3.7 pp (SpreadsheetBench/OfficeQA/ALFWorld), 4.5 pp Terminal-Bench; tau 0-12.3 pp. Single-run score SD median 1.7-4.1 pp. >60% of config pairs differ by less than one single-run SD (Fig 2a).
- Literature: 171 benchmark-model results from 9 papers, median margin over strongest competitor 3.4 pp (IQR 1.2-6.6); none report variance, only 6 average over >1 evolution run. Runs needed for 3.4 pp at 80% power: ~5 SpreadsheetBench, 10 OfficeQA, 19 ALFWorld, 23 Terminal-Bench (181 at lower-quartile margin).
- A single-run table picks the best of 4 text-artifact methods 51-73% of the time (non-TB), 33% on Terminal-Bench (random 25%).
- Gain audit: one appended sentence recovers median 90% of gain across 27 model-benchmark pairs with reported gain >3 pp; shortcuts are grader-format or benchmark-version quirks. After evaluation repair median gain falls 17.6 -> 0.8 pp (Fig 3); re-running methods under repaired evals does not restore it.
- P1 (Fig 4a): Quality@K rises 49.2% (K=1) -> 61.8% (K=100) at 2h budget; best shared skill +8.3 pp over pool mean (57.5 vs 49.2); pool spread >15 pp.
- P2 (Table 1): pairwise accuracy execution 49.7%, SkillOpt-Lite 48.6, GEPA 48.6, LLM judges 45.4/49.0/46.9 vs random 50; false-accept 62.1% for execution vs 30.5% base rate of regressions; rank correlation 0.054. No selector benefits from more candidates (flat to K=100).
- P3 (Fig 5-6): in-loop gains 6.9-9.0 pp re-evaluate to +0.4 to -3.2 pp; run-to-run variance grows to 4.2-24.5 pp^2 by the final round (random walk).
- Sec 6 recommendations: finer-grained behavioural checks, separate proposer/selector evaluation, resolution-aware variance reporting.

## Applicability
- Any harness/skill/prompt self-evolution loop: multi-rollout validation, repeated runs, variance reporting, shortcut-rule audits, held-out re-evaluation of final artifacts, power analysis before claiming margins.
- Requires many rollouts per artifact.

## Caveats / Reproducibility
- Frozen weights only; candidate-level evidence is Terminal-Bench v2.1 only; program evolution with deterministic scoring is out of scope and noted as working.
- SkillOpt-Lite is audited, not necessarily [[skillopt]] itself; read as a probable caveat, not a refutation of its +24.8 pp claim. Likewise GEPA's gains are traced to shortcuts here, in tension with [[gepa-reflective-prompt-evolution]]'s claims.
- Project page lineshogan.github.io/resolution-hypothesis. Code and trajectory data "will be released upon acceptance" (not yet). Compute-heavy (>10M LLM calls, 400K CPU core-hours).
- Numbers above are from the ingest summary of the paper; I did not re-verify each against the raw text.

## Source
- raw/research/weekly-2026-11-21/02-resolution-hypothesis.md
- https://arxiv.org/abs/2611.23068

## Related
- [[skillopt]] - SkillOpt-Lite audited; strict-improvement acceptance near chance on Terminal-Bench.
- [[gepa-reflective-prompt-evolution]] - GEPA selection 48.6% pairwise accuracy; gains traced to single-sentence shortcuts.
- [[evolutionary-search-eval-rigor]] - sibling evaluation-rigor critique (budget-split reversal, validator exploits).
- [[memoharness]] - harness margins (0.806 vs 0.722) fall within single-run noise range.
- [[self-evolving-agent-harness]] - parallels its fresh-validation admission bounds.
- [[coevo-rsi]] - co-evolution results subject to the same noise.
- [[argus-agentic-runtime]] - evidence-gated self-evolution admission.
- [[macaron-v1]] - harness co-optimization via RSI loop.
- [[socratic-skill-learning]] - skill-authoring gains vs No Skill.
- [[disco-arex-skill]] - skill distillation gains.
- [[evidence-linked-memory]] - ReasoningBank-type memory evolution regressions.
- [[jev-as-a-judge]] - LLM judges near chance parallels judge-reliability findings.
- [[test-time-scaling-taxonomy]] - Best-of-N selection can lower accuracy when scores misalign.
- [[huxley-godel-machine]] - self-improving agent selection by benchmark score.
- [[kimi-k3]], [[deepseek-v4]] - evaluated agent models.
- [[recursive-collective-intelligence]] - gated group-level generations; several gains reported on selection sets.
