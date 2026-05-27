# TIDE: Token-Informed Depth Execution for Per-Token Early Exit in LLM Inference

Post-training system that attaches lightweight learned routers at checkpoint layers and, at inference time, selects the earliest layer whose hidden state has converged for each token — no model retraining required.

## Method core

**Problem.** Standard transformers allocate identical depth to every token regardless of difficulty. A function word like "the" gets the same 32-layer treatment as a reasoning step. Prior work shows intermediate hidden states often converge to the final-layer representation well before the last layer, making the remaining compute wasteful.

**Convergence signal.** TIDE defines convergence via cosine similarity between a checkpoint layer's hidden state and the final layer's hidden state: label token *i* as converged at checkpoint *k* if cos(**h**_k^i, **h**_L^i) > τ (default τ=0.98). This replaces softmax-entropy heuristics (unreliable for generation, where entropy is naturally high) with a direct representational-similarity criterion.

**Routers.** At each checkpoint layer (interval *c*=4 by default), TIDE trains a tiny two-layer MLP router — RMSNorm → down-projection (d×128) → SiLU → up-projection (128×1) → sigmoid — on binary convergence labels from 2,000 WikiText-103 samples, using BCE + Adam for 100 epochs. Calibration takes under 3 minutes; the resulting checkpoint is ~4 MB.

**Attention / KV cache consistency.** TIDE uses a *post-hoc* exit strategy: the full forward pass always runs all *L* layers (so the KV cache is always fully populated), and then routers evaluate each checkpoint's hidden state after the fact, selecting the earliest converged layer's representation for logit computation (LMHead(RMSNorm(**h**_k))). This sidesteps the cache-corruption issue common to exception-based or hook-based early-exit approaches and remains compatible with `transformers` v5.3+ wrappers.

**CUDA implementation.** Four fused kernels: (1) fused RMSNorm + router evaluation in a single launch using warp-level reductions, (2) batch-compact for separating exiting/continuing tokens, (3) exit-scatter for copying exited hidden states, (4) exit-projection for fused RMSNorm + scatter. Template-specialized for fp32/fp16/bf16 and common hidden dimensions (2048–8192). Falls back to pure Python if CUDA compilation fails.

**Universality.** A `UniversalAdapter` probes 17 known attribute paths across 5 component types to support LLaMA, Mistral, Qwen, GPT-2, GPT-NeoX, Phi, Falcon, OPT, and Gemma without per-model adapter code.

## Comparison to related approaches

**vs. CALM (Schuster et al., NeurIPS 2022).** CALM uses softmax confidence as the exit signal on encoder-decoder (T5) models. TIDE targets decoder-only autoregressive LLMs, replaces entropy heuristics with learned cosine-convergence routers, and is fully post-training (CALM requires fine-tuning with early-exit objectives). CALM does not preserve KV cache integrity for arbitrary generation; TIDE's post-hoc mode does.

**vs. AdaPonderLM / adaptive-ponder approaches.** Approaches in this family typically modify training (additional halting-probability loss, shared-weight universal transformers) or require architecture changes. TIDE is strictly post-training: frozen model weights, router calibration only. The exit decision is binary per checkpoint rather than a soft halting probability.

**vs. LayerSkip (Elhoushi et al., ACL 2024).** LayerSkip trains from scratch with layer-dropout early-exit loss — hundreds of GPU-hours and access to the training pipeline. TIDE requires none of that; it wraps any pretrained HuggingFace checkpoint.

**vs. SkipDecode (Del Corro et al., 2023).** SkipDecode physically skips lower layers during decode, accepting KV cache discontinuity and not supporting per-token granularity. TIDE is per-token and cache-safe (post-hoc mode), though it does not yet achieve wall-clock layer skipping for the compute it nominally skips.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** Modular composition | Low | TIDE does not compose separately trained modules; it routes within a single fixed model. |
| **G2** Continual / efficient adaptation | Low-Medium | Post-training calibration is cheap (~3 min, ~4 MB checkpoint) and model-agnostic, which is relevant to rapid adapter deployment, but TIDE itself does not address continual learning. |
| **G3** Token-conditional routing | High | Direct instantiation: per-token variable-depth inference based on learned hidden-state convergence. Addresses TC2 (attention consistency across depths) via post-hoc KV-cache-preserving design, and TC3 (routing granularity) via per-token exit decisions. |

## Credibility

- **Venue:** NeurIPS 2023 (stated in the PDF footer). Submitted to arXiv March 2026.
- **Code:** Open-source, Apache 2.0 — `https://github.com/RightNow-AI/TIDE`; PyPI package `tide-inference`. 74 passing tests covering adapters, calibration, CUDA numerical equivalence, and end-to-end runtime.
- **Ablation rigor:** Limited. Evaluation covers two 8B models (DeepSeek R1 Distill 8B, Qwen3 8B) on 16 prompts (8 reasoning, 8 general) and one math problem for quality. No perplexity benchmarks, no comparison to CALM or LayerSkip on the same tasks. Threshold sensitivity (τ, θ) is partially explored but not systematically ablated. Authors acknowledge the τ=0.98 default is conservative and concentrates exits at the penultimate checkpoint.

## Empirical claims

- DeepSeek R1 Distill 8B (32 layers, A100, bf16): 100% prefill exit rate; 5% of tokens exit at L11, remainder at L31. Prefill latency −7.2%, single-batch throughput +6.6%. At batch size 8: throughput −16.3% (output_hidden_states overhead dominates).
- Qwen3 8B (36 layers): throughput +8.1% at batch size 8.
- Decode quality: 98.4–99.6% of tokens exit early on a math word problem while correctly preserving mathematical reasoning (95 unique tokens vs. 99 baseline).
- Calibration: 2,000 WikiText samples, ~170 s on A100, ~4 MB router checkpoint.

**Negative result.** At BS=8 for DeepSeek R1, throughput degrades 16.3%. The `output_hidden_states=True` overhead scales super-linearly with batch size for this model. Post-hoc mode's correctness guarantee comes at this cost; a hybrid that collects hidden states only at checkpoint layers is listed as future work.

## Open questions / failure modes

- **No wall-clock layer skipping.** Post-hoc mode runs all layers every step; speedup comes from cheaper logit computation and fused kernels, not from physically skipping transformer blocks. True layer skipping (with cache-discontinuity management) is deferred.
- **Conservative threshold clusters exits at penultimate checkpoint.** With τ=0.98, nearly all tokens exit at L31/L35 rather than earlier layers. Per-layer threshold tuning or an annealed schedule is needed to unlock earlier exits in practice.
- **Batch-size scaling.** `output_hidden_states` overhead makes TIDE net-negative at large batch sizes for some architectures. Limits applicability in high-throughput serving scenarios.
- **Evaluation scope.** Only 8B-class models; no multi-GPU validation; no perplexity/task-accuracy benchmarks (MMLU, HellaSwag, etc.) demonstrating quality preservation at scale.
- **Single domain calibration.** Routers trained on WikiText-103 may mis-generalize for highly out-of-distribution domains (code, structured data, non-English).

## Source

- `raw/research/loop-challenges/05-tide-abs.md`
- `raw/research/loop-challenges/08-tide-pdf.md`

## Related

[[calm]], [[adaponderlm]], [[depth-adaptive-transformer]], [[token-conditional-routing]], [[layerskip]], [[mixture-of-depths]]
