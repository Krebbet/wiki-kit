# GRPO/RLHF vs Evolution Strategies for LLM Post-Training

**Status:** open. Pre-flagged from radar-2026-04 ingest. No GRPO-side source captured yet.

## Position A — Evolution Strategies match or beat GRPO at scale

**Source:** [[eggroll]] (EGGROLL paper, arXiv:2511.16652).

**Claim:** EGGROLL matches or beats GRPO on LLM reasoning fine-tuning across multiple benchmarks, and is *the only feasible method* at scales where Adam optimizer state breaks GRPO.

**Basis (concrete numbers):**
- Countdown on RWKV-7 1.5B: **EGGROLL 35% vs GRPO 23%** validation accuracy at equal wall-clock.
- GSM8K on RWKV-7 7B (8 GPUs): EGGROLL beats GRPO.
- 14B RWKV-7 on DeepScaleR (32 GPUs × 12h): AIME24 13% → 30%, AIME25 7% → 33%. **GRPO infeasible at this scale due to Adam optimiser memory.**
- Can directly optimise pass@k (a documented GRPO limitation per Yue et al. 2025).

**Why it works:** Constant-state recurrent models (RWKV, SSM, RNN) make population sizes ~1k–~1M cheap because the inference batch shares the base matmul. Transformers benefit less; KV cache eats the population budget.

Concurrent ES-for-LLMs work: Qiu et al. 2025, Korotyshova et al. 2025 (ESSA / CMA-ES on LoRA SVD bases) — an active subfield is forming.

### Position A extension — Prompt-space evolution beats GRPO too (2026-04-27)

**Source:** [[gepa-reflective-prompt-evolution]] (GEPA, arXiv:2507.19457, ICLR 2026 oral).

**Claim:** Reflective prompt evolution + Pareto-illumination candidate selection beats GRPO with **35× fewer rollouts**, no weight updates.

**Basis:**
- Qwen3-8B, 6 tasks: GEPA aggregate +9.62 vs GRPO +3.68 (24,000 rollouts) vs MIPROv2 +2.61. GEPA wins 5/6 (Table 1).
- GEPA rollouts: 678–7,051 (vs GRPO's 24,000).
- Cross-model transfer: prompts optimized on Qwen3-8B beat baselines optimized natively on GPT-4.1-Mini (+9.00%).

**Why it matters here:** Position A now spans **two mechanism axes** — weight-space ES (EGGROLL) and prompt-space evolutionary search (GEPA). Different substrates, same competitive claim against GRPO. Tightens the burden on Position B.

### Position A extension — Weight-space ES beats GRPO on ordinary transformers too, at every scale 1.5B–32B (2026-08-29)

**Source:** [[es-solution-coverage]] ("Beyond the Best Guess," Cognizant AI Lab, arXiv:2608.12679).

**Claim:** ES beats RL/GRPO on pass@k solution coverage across Qwen2.5-Instruct and Qwen3 models from 1.5B to 32B, while matching or exceeding RL on pass@1. Total regressions vs. base model: ES 24 vs. RL 106 (across MATH500/Olympiad Bench/Minerva, Qwen2.5-Math-7B).

**Basis:** GSM8K pass@k crossover ~k=2 favoring ES, gap growing with k, at every scale from Qwen2.5-1.5B-Instruct up through 32B; RL/GRPO-tuned models are eventually overtaken by the *base* (pre-RL) model at large k, replicating Yue et al. 2025 — ES is never overtaken by base at any tested scale.

**Why it matters here:** EGGROLL's compute argument was explicitly substrate-dependent — constant-state recurrent models (RWKV) make large ES populations cheap; the framing in this file's Resolution rule ("ES wins on RWKV/SSM-class substrates; GRPO wins on transformers") assumed the win narrows or reverses on transformers. This source directly weakens that assumption: it runs ES on ordinary Qwen transformers (not RWKV/SSM) and finds ES beats GRPO on solution coverage at every scale tested, with population size only 30 — cheap even without constant-state batching. The axis is different from EGGROLL's (solution coverage/pass@k, not wall-clock training efficiency), so this doesn't fully overturn the substrate-dependent resolution, but it removes the "ES only wins on RWKV" fallback for at least the coverage/diversity claim. Position B (a GRPO-orthodoxy defense) is still uncaptured.

## Position B — GRPO/RLHF is the right primitive for LLM post-training

**No source captured.** Awaiting an ingest of a primary GRPO/RLHF paper (DeepSeek-R1, GRPO original, broader RLHF-as-default-stance work) that argues for the orthodoxy.

## Resolution rule when Position B arrives

Compare on matched substrate (RWKV-7 vs. transformer; same base scale; same task family) *and* matched axis (wall-clock training efficiency vs. solution coverage/pass@k vs. pass@1). EGGROLL's compute-efficiency argument is substrate-dependent (constant-state RWKV batching); [[es-solution-coverage]]'s coverage argument holds on ordinary Qwen transformers at every scale 1.5B–32B, so the "ES only wins on RWKV" fallback no longer applies to the coverage axis specifically — resolution will likely need to be per-axis (e.g. "GRPO may still win on transformer wall-clock efficiency; ES wins on solution coverage/pass@k regardless of substrate") rather than a single universal answer.

## Related

- [[eggroll]], [[gepa-reflective-prompt-evolution]], [[es-solution-coverage]], [[watchlist]] (Salimans 2017 OpenES, MeZO, Qiu 2025, Korotyshova 2025, RWKV-7, MIPROv2, TextGrad).
