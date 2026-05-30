# Looped Language Models (Ouro)

Ouro (arXiv 2510.25741) introduces Looped Language Models (LoopLM), a weight-shared recurrent transformer architecture where a single N-layer decoder stack is applied t times with fully shared weights. Pre-trained at 1.4B and 2.6B parameters on 7.7T tokens with up to 4 recurrent steps, Ouro achieves 2–3× parameter efficiency over dense baselines on reasoning tasks. The central empirical finding is that recurrence enhances knowledge *manipulation* (multi-hop reasoning, compositional tasks) but does not increase knowledge *storage* capacity — bits-per-parameter remains ~2 regardless of loop depth.

## Architecture (weight-shared recurrence)

The base model is a standard decoder-only transformer: MHA + SwiGLU FFN, RoPE positional encoding, sandwich RMSNorm. The entire N-layer stack is applied recurrently t ∈ {1, …, T_max} times with fully shared weights — no per-step adapters, no LoRA injection in the Ouro design (LoRA-per-step cited only as prior work: "Relaxed Recursive Transformers"). Effective depths at 1.4B and 2.6B with T_max=4 are 96 and 192 layers respectively.

## Adaptive exit / entropy-regularized gate

A learned per-token, per-step scalar exit gate projects the final-layer hidden state through a linear layer and sigmoid to produce an instantaneous exit probability λ_t. A survival-function formulation yields a discrete distribution over exit step p_ϕ(t|x).

Training is two-stage:
- **Stage I:** Gate trained jointly with LM under KL-ELBO entropy regularization against a uniform prior (β=0.1→0.05). Without this regularization, raw gradient descent collapses to always using T_max (self-reinforcing depth bias).
- **Stage II:** LM weights frozen; gate fine-tuned with an explicit adaptive exit loss (binary cross-entropy against a marginal-improvement label).

At inference, **Q-exit** applies: exit at the first step where the gate CDF ≥ q. The two-stage trained gate outperforms static baselines and hidden-state-difference heuristics by ~2–3 pp on MMLU at identical compute budgets.

## Knowledge manipulation vs. storage

The most thesis-load-bearing result in this batch: on synthetic bioS and multi-hop QA tasks (Mano/bioS, 1M–40M parameter GPT-2 style models), looped and non-looped models of equal parameter count both settle at ~2 bits/parameter for raw factual memorization. Looping confers no advantage in knowledge storage capacity. Gains are narrowly confined to *manipulation* tasks requiring composition or chaining of stored facts across hops. This directly supports the thesis that architectural structure affects transformation capability, not knowledge storage.

## Training pipeline / scale

- Parameters: 1.4B and 2.6B
- Training tokens: 7.7T (vs. Qwen3-4B at 36T)
- Recurrent steps: T_max=4 (reduced from 8 after Stage 1a gradient instability)
- Benchmark suite: MMLU, MMLU-Pro, BBH, ARC-C, HellaSwag, Winogrande (5-shot), GSM8K, MATH500, HumanEval(+), MBPP(+), AIME 2024/2025, OlympiadBench, GPQA, SuperGPQA, BeyondAIME, HLE, HEx-PHI
- Dense comparisons: Qwen2.5, Qwen3, Gemma3, Llama3.1/3.2 series up to 12B

## Scale / benchmarks

Ouro 1.4B (4 recurrent steps) vs. Qwen3-4B (36T tokens):

| Benchmark | Ouro 1.4B | Qwen3-4B |
|-----------|-----------|----------|
| BBH       | 71.02     | 70.95    |
| GSM8K     | 78.92     | 72.86    |
| MATH500   | 82.40     | 59.60    |

Ouro 2.6B exceeds all tested ≤8B dense baselines on MATH500: 90.85 vs. best 83.20. The 2.6B model peaks at T=3–4 steps for reasoning tasks; performance is non-monotone beyond training depth.

## Failure modes

Six concrete failure modes, all practical deployment barriers:

1. **RL alignment broken** — RLVR with DAPO/GRPO failed: variable-depth early exit is incompatible with vLLM/SGLang fixed-path rollouts. Both off-policy simulation and fixed-4-step RL produced no gains over the SFT checkpoint.
2. **Gradient oscillation >4 recurrent steps** — Stage 1a at 8 steps caused loss spikes and gradient oscillations; T_max was reduced to 4. Extrapolating beyond T=4 at inference degrades reasoning benchmarks (though monotonically improves safety scores on HEx-PHI).
3. **KV cache reuse catastrophic** — Reusing first-step KV cache across recurrent steps causes collapse: GSM8K drops from 78.92 to 18.73. Prefill-phase KV sharing across steps causes >10 point degradation; no cross-step cache reuse is feasible without architectural changes.
4. **Naive gate training collapses** — Without entropy regularization, the gate converges to always selecting T_max (depth bias is self-reinforcing under vanilla gradient descent).
5. **Depth extrapolation degrades** — Performance degrades when T > T_max at inference for standard benchmarks; Ouro-Thinking 1.4B peaks at T=4–5, 2.6B at T=3–4.
6. **Zero storage gain** — Looping does not expand factual memorization capacity; bits/parameter ≈ 2 identical between looped and non-looped iso-parameter models.

## Open questions

From the authors:

1. Extrapolation beyond T_max — models degrade past training depth on reasoning tasks; improving this would allow test-time scaling without retraining.
2. More complex recurrent mechanisms — current design is maximally simple (full weight sharing, no per-step specialization); per-step adapters or state passing may unlock further gains.
3. RL infrastructure for variable-depth computation — RLVR is currently blocked by early-exit incompatibility with standard inference engines.
4. Mechanism of fixed-step RL → adaptive-depth inference — fixed-step RL training still produces adaptive-depth behavior at inference; the mechanism is unexplained.
5. LoopLM scaling laws — loop depth as a third scaling axis (alongside parameters and tokens); saturation behavior only partially characterized.

## Source
- `raw/research/thesis-foundations/06-ouro-looped-lm.md` — *Scaling Latent Reasoning via Looped Language Models* — arXiv 2510.25741

## Related
- [[universal-transformer]] — foundational precursor; Ouro extends with entropy-regularized adaptive exit replacing ACT, scales to 7.7T tokens.
- [[looped-transformers-and-reasoning]] — Latent-Thoughts makes the theoretical reasoning case at 1B; Ouro validates and extends at 1.4B with full pretraining pipeline.
- [[mixture-of-depths]] — both use learned routers for conditional depth reduction; both report naive routing fails.
- [[looped-vs-depth-scaling]] (open conflict) — Ouro claims matches/beats dense models generally, which tensions Latent-Thoughts' perplexity-tradeoff finding; comparison bases differ (iso-param vs iso-FLOP vs iso-token).
- [[knowledge-manipulation-vs-capacity]] — dedicated treatment of the ~2 bits/param storage invariance and contrasting manipulation gains; cross-references Mano/bioS synthetic experiments.
- [[adaptive-computation-exit-mechanisms]] — collects exit/halting strategies across sources (PonderNet, MoD, Ouro Q-exit); Ouro provides multi-strategy empirical comparison on MMLU.
