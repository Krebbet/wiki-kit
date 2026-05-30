# Orthrus: Memory-Efficient Parallel Token Generation via Dual-View Diffusion

Orthrus injects a lightweight trainable masked-diffusion attention head into a frozen AR transformer so both views share one KV cache, achieving up to 7.83× inference speedup (Pseudo2code, Qwen3-8B, T=0) with mathematically guaranteed lossless output distribution — exact parity with the frozen AR base by construction, not approximation.

## Method

Each transformer layer gains a second Q/K/V projection set ("diffusion head"), initialized from frozen AR counterparts. Prefill: frozen AR backbone builds standard causal KV cache. Generation: diffusion head appends K−1 `<mask>` tokens to the current anchor, processes all K positions in one forward pass attending jointly over (i) shared AR KV cache (causal, history) and (ii) bidirectional intra-block self-attention (future block). Custom attention mask via FlexAttention/FlashAttention-4 enforces both constraints simultaneously.

Training objective: KL divergence of diffusion head's per-position predicted distribution vs frozen AR head's exact softmax (soft distillation, eq. 7) — not CE vs ground-truth. AR backbone strictly frozen throughout; only diffusion Q/K/V updated (~16% of total params). Data: 600K examples (~0.96B tokens) from Nemotron-Post-Training-Dataset-v2, 1:1:1 math:code:chat mix, 2 epochs, 8×H200, <24h.

Inference/consensus (two-step): diffusion head projects K candidates in one forward pass (Step 1); frozen AR head evaluates the filled block in one forward pass for exact causal probs (Step 2); tokens accepted left-to-right via greedy match (T=0) or rejection sampling (T>0). Output distribution is provably identical to base AR. KV cache overhead is O(1) — fixed ~4.5 MiB, sequence-length independent.

## Results

**Efficiency (Table 1, Qwen3-8B, greedy T=0 unless noted):**
- Avg Tokens-Per-Forward-pass (TPF): 5.39 → 5.36× speedup (T=0); 4.43 TPF / 5.02× (T=1)
- Peak: 7.51 TPF / **7.83×** on Pseudo2code (8B, T=0)
- MATH-500: 6.35 TPF (5.95×); AIME24: 5.63 TPF (6.81×); LiveCodeBench-v5: 5.17 TPF (6.68×)

**Acceptance length (Fig 4), MATH-500:** Orthrus 11.7 vs DFlash 7.9 vs EAGLE-3 3.5.

**Accuracy vs DLM baselines (Table 2, Qwen3-8B):**

| Task | Orthrus | SDAR-Qwen3-8B | Fast-dLLM-v2 | Dream-7B |
|---|---|---|---|---|
| GSM8K | **96.0** | 91.7 | — | 79.3 |
| MATH-500 | **86.2** | 78.6 | 61.5 | — |
| AIME-24 | **28.3** | 10.0 | — | — |
| AIME-25 | **23.3** | 10.0 | — | — |
| HumanEval | **95.1** | 78.7 | 43.3 | — |
| MBPP | **93.4** | 72.0 | — | — |

Exact parity with frozen Qwen3-8B AR on all tasks by design.

**Memory (Fig 6):** peak GPU overhead ~100 MiB (<1%); KV cache overhead fixed ~4.5 MiB at all sequence lengths.

**Ablations:** block K=32 → TPF 6.35 vs K=4 → 1.85 (3.6× gain, zero latency penalty); single-step projection TPF 6.35 vs two-step 3.53; KL(soft) vs CE(hard) identical accuracy 86.2% but CE cuts TPF 6.35→5.86 (more rejections).

## Novelty

Prior AR→diffusion adaptations (Fast-dLLM-v2, SDAR, LLaDA, Dream) fine-tune or retrain the base model → distributional drift. Speculative decoding (EAGLE-3, DFlash) keeps base intact but requires an external drafter and a separate KV cache. Orthrus eliminates both: intra-model consensus via injected diffusion Q/K/V projections against the live frozen AR teacher guarantees exact distributional parity — not an approximation. Intra-block bidirectional attention + causal AR-context attendance in a single shared KV cache is the core architectural contribution.

## Comparison: [[tidar]]

Orthrus is the closest architectural parallel to [[tidar]]: both are single-model AR+masked-diffusion hybrids where the diffusion head attends over a shared KV cache with an AR verification step. Key distinction: Orthrus keeps the AR backbone **strictly frozen** and trains only the injected diffusion Q/K/V projections via KL distillation against the live AR teacher, giving mathematically guaranteed lossless output distribution. [[tidar]] adapts/repurposes base weights, which allows capability improvement but introduces distributional drift by construction.

Speedup figures (Orthrus peaks 7.83× on Pseudo2code @8B vs [[tidar]]'s reported 4.71×–5.91× vs Qwen base AR) are not a genuine contradiction: different setups, metrics (TPF vs measured T/s), and the frozen-vs-adapted-backbone distinction make them incommensurable. Treat as parallel methods on the same design axis, not a conflict ruling.

## Applicability

Plug-in inference accelerator for any pretrained AR transformer; no base retraining. Requirements: frozen open-weights AR base, FlexAttention/FlashAttention-4, ~1B token fine-tune, <24h on 8×H200. No RL infra. Production-ready O(1) memory profile, no external drafter. Does **not** improve base capabilities — output distribution is upper-bounded by the frozen AR backbone; purely inference-side acceleration.

## Reproducibility

Code: https://github.com/chiennv2000/orthrus. Training data open (Nemotron-Post-Training-Dataset-v2). No released weights, no paperswithcode entry as of capture date. Preprint only; no citations or reproductions yet. Authors: University of Oregon + Adobe Research + Google DeepMind.

## Source

`raw/research/weekly-2026-05-18/03-orthrus.md` (arXiv:2605.12825)

## Related

[[tidar]], [[coladlm]]
