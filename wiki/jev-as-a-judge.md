# JEV-as-a-Judge: Confidence-Gated LLM-Judge Cascades

CMU (arXiv:2609.26550, Sept 2026). Benchmarks TypeSafe JEV — a hosted, decision-only (no chain-of-thought) LLM-judge interface returning a verdict plus label probabilities — against 16 generative/reward-model judges. JEV alone lands within 3pp of a SOTA generative judge (GPT-6 Astra) on ordinary preference/factuality tasks at 0.36% of its fee, but degrades sharply on derivation-checking and style-adversarial tasks. A frozen confidence-threshold cascade (accept JEV when confident, escalate to GPT-6 when unsure) retains ~99% of GPT-6's accuracy at under half its fee.

## Method

JEV exposes a typed decision-only contract: given instructions + structured state, it returns a verdict and probabilities over an allowed output type (no rationale generated). Confidence is `q = max_k p_k` over label probabilities. Compared against 13 hosted generative judges (GPT-4.1 through GPT-6 Astra, GPT-OSS-120B, Qwen3.6/3.8, Claude Sonnet 5, Gemini 3) forced into the same decision-only contract, plus local Qwen3-32B/3.5-27B, PairRM, and Skywork-Reward-V2-Qwen3-8B.

The contribution is a **frozen, pre-specified** two-stage cascade: a threshold `τ` chosen on a held-out pilot set to maximize coverage while keeping selection-set accuracy within 2 points of the fallback judge. For pairwise items, JEV is queried in both candidate orders and probabilities averaged before gating (mitigates order bias). Builds on selective classification (Geifman & El-Yaniv 2017), temperature scaling (Guo et al. 2017), and model-cascade literature (FrugalGPT, RouteLLM); closest priors are Jung et al. 2025 (cascading judges with agreement guarantees) and Xu et al. 2025 (routing uncertain reward-model comparisons). The paper frames itself as an empirical operating profile, not a new routing algorithm.

## Results

- Base accuracy (1312 items): JEV 92.2% RewardBench (GPT-6: 93.5%), 87.5% HaluEval (86.7%), 94.0% label adjudication (96.7%) — "use JEV" territory.
- JudgeBench (hard correctness): JEV 78.6% vs. GPT-6 93.1% (−14.6pp, worst in reasoning/coding); RM-Bench style-adversarial: 74.8% vs. 94.6% (−19.8pp) — "escalate" territory. Blinded human adjudication of 183 disagreements confirms these aren't label noise.
- Cost/latency: JEV median 0.152s / $0.044 per 1000 judgments vs. GPT-6's 1.885s / $12.182 (~277× cheaper).
- Cascade at τ=0.9 (510 extension pairs): accepts 53.7% of items, scores 92.5% vs. fallback's 93.1% (−0.6pp) at 56.8% of GPT-6's fee. Single-order pooled cascade: 91.3% vs. 91.7% (99.6% retained) at 47% of fee.
- Confidence signal quality is task-dependent: near-interchangeable with GPT-6 at q≥0.9 on calibrated tasks, but AUROC of confidence vs. correctness drops to 0.770 on style-adversarial pairs and collapses to 0.518 (chance) on reference-free prose grading — no threshold helps there.

## Applicability

Any team running high-volume LLM-judge workloads (RLHF/RLAIF reward pipelines, eval harnesses, best-of-N filtering, data quality gating) dominated by preference judgment or evidence-grounded factuality. Requires the proprietary JEV API (not self-hostable) plus a fallback judge, and a local calibration set per workload — thresholds do **not** transfer across fallback models or task difficulty (one naive transfer lost 2.35pp beyond tolerance). Not usable as-is for derivation-checking (math/code correctness), style-adversarial resistance, or reference-free prose grading — must escalate 100% or use a different judge there.

## Reproducibility

JEV itself is closed/proprietary. An anonymous supplementary artifact (Appendix L) reportedly contains public-task inputs/rubrics, decision-level outcomes, executable reproduction code for public results, and the human-adjudication materials — reproducible without API calls or a GPU, but this reads as a submission artifact, not a maintained public repo.

## Source

- raw/research/weekly-2026-09-26/02-jev-as-a-judge.md
- arXiv: https://arxiv.org/abs/2609.26550

## Related

- [[rrc-reward-ranking]] — parallel comparison of generative vs. discriminative reward models as judges/scorers, from the RL-training-signal-construction angle rather than post-hoc evaluation economics.
- [[debate-training-reward-hacking]] — both concern LLM-judge reliability, but different failure modes: adversarial reward-hacking of judges as an RL signal there, vs. confidence miscalibration on style-adversarial/derivation tasks here.

This is the wiki's first source on evaluation-time LLM-judging economics and confidence-cascading — a distinct subtopic from the existing RL reward-design cluster, which concerns reward signals *during* training rather than post-hoc judge cost/confidence.
