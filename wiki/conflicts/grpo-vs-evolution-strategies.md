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

## Position B — GRPO/RLHF is the right primitive for LLM post-training

**No source captured.** Awaiting an ingest of a primary GRPO/RLHF paper (DeepSeek-R1, GRPO original, broader RLHF-as-default-stance work) that argues for the orthodoxy.

## Resolution rule when Position B arrives

Compare on matched substrate (RWKV-7 vs. transformer; same base scale; same task family). Note that EGGROLL's compute argument is substrate-dependent — the win narrows or reverses on transformers because constant-state batching disappears. Resolution may be "ES wins on RWKV/SSM-class substrates; GRPO wins on transformers" rather than a universal answer.

## Related

- [[eggroll]], [[watchlist]] (Salimans 2017 OpenES, MeZO, Qiu 2025, Korotyshova 2025, RWKV-7).
