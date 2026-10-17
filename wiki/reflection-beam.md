# Reflection Beam-1.0: 501B-A23B Open MoE

Reflection's Beam-1.0 (Hugging Face launch post; Apache-2.0) is a 501B-parameter, 23B-active, text-only MoE with 1M context aimed at coding and agentic use. Architecture is mostly recombination at frontier scale (DeepSeek-V3 router, 5:1 sliding/global hybrid attention, sigmoid output gates), with two distinctive pieces: a variance-preserving 1/sqrt(k) residual accumulation and NoPE global layers with query scaling. All benchmarks are vendor-reported; the pretraining recipe and data are not disclosed. Shares the open-frontier-MoE shape (256 experts, top-8 routed, 1M context) with [[muse-spark-open]].

## Architecture

- 52 layers, hidden 5120. 43 sliding-window layers (512 tokens, RoPE) + 9 global layers (every 6th and last); global layers use no positional encoding, with query scaling (1 + (pos+1)/2048)^0.1 (scalable-softmax). GQA 48 Q / 8 KV heads, QK RMSNorm, learned sigmoid output gate per channel per head.
- MoE: first 3 layers dense SwiGLU, then 49 MoE layers x 256 experts (~39M params each, 98.4% of params), top-8 routed, no shared expert. DeepSeek-V3 group-limited sigmoid router (8 groups of 32, top-4 groups), normalized weights scaled by 2.5. See [[moe-architecture-survey]].
- Residuals: at step k add the sublayer output with weight 1/sqrt(k) and keep the stream with sqrt((k-1)/k); across 104 additions the embedding and every sublayer output end with equal weight. Pre+post norm on every sublayer; tanh logit softcap at +-30 in FP32. An alternative to learned/constrained mixing in [[manifold-constrained-hyper-connections]] (used by [[deepseek-v4]]); no ablation is given, so no evidence on relative merit.
- KV cache 36 KiB/token (1M context = 36 GiB vs 208 GiB all-global, ~1/6) via the hybrid attention, rather than compression as in [[triattention]].

## Release and serving

- BF16 (~1 TB), FP8, NVFP4 (~280 GB, Blackwell). Reasoning effort low/medium/high/xhigh/max, preserve_thinking across turns, tokenizer-embedded response template, XML-style tool-call grammar, DFlash2 speculative drafter (up to 15 tokens), Rust-based custom harness.
- Day-0 transformers (>=5.20.1), vLLM, SGLang; HF Inference Providers (Baseten, Fireworks, Together). Serving: 4x B200 / 2x B300 / 8x RTX Pro 6000 for NVFP4; 16x H200 for BF16.

## Post-training recipes

- SFT: TRL SFTTrainer + PEFT LoRA on one 8x B300 node (~19k tok/s). Demo: LoRA on Multilingual-Thinking, 1 epoch, reasoning in requested language 16/16 held-out vs 3/16 base (tiny, language adherence only).
- GRPO via Miles (Megatron train + SGLang rollout): full-param (96x H200) or LoRA rank-16 (32x H200). DAPO-Math-17K, 32 prompts x 8 responses, boxed-answer reward with soft overlong penalty, group-relative advantages with truncated importance sampling, no KL or entropy penalty (same no-KL stance as [[magistral]]), Adam constant 1e-6, one-step-off-policy async (cf. [[llamarl]]), NVMe optimizer offload.

## Benchmarks (vendor-reported, BF16 / FP8 / NVFP4)

- SWE-Bench Verified 81.6/80.2/80.7 (V4-Pro: 80.6 per [[deepseek-v4]], different harness, not matched); SWE Bench Pro v1 66.1/65.9/65.6; Terminal Bench v2.1 80.1/78.9/78.2 (cf. [[terminal-universe]]); DeepSWE v1.1 43.3/43.0/42.7.
- SWEBench Multilingual 78.3; AIME 2026 97.7; GPQA Diamond 90.6; LiveCodeBench 88.3; HLE 36.0 no tools / 51.1 with tools; MCP Atlas 80.8; BrowseComp (context mgmt) 76.8; LongBench v2 67.5; IFBench 79.6.
- Quantization loss generally <=2 points. No comparison against other models in the captured post; no independent verification. Side demos (Qwen3.5-0.8B triage model, Beam+Pi multi-agent ProgramBench) are anecdotal or numberless.

## Comparison and caveats

- Versus [[deepseek-v4]] (1.6T/49B active) and [[kimi-k3]] (2.78T): far smaller and permissively licensed; reuses V3 routing but drops the shared expert.
- Community adoption not yet measurable (~1.15k downloads, 125 likes at capture).
- Residual and NoPE ideas are transferable to from-scratch pretraining, but unablated here.

## Source

- raw/research/weekly-2026-10-17/04-reflection-beam.md
- https://huggingface.co/blog/reflection-beam

## Related

[[muse-spark-open]], [[deepseek-v4]], [[kimi-k3]], [[moe-architecture-survey]], [[manifold-constrained-hyper-connections]], [[triattention]], [[magistral]], [[llamarl]], [[polar-rl-harness]], [[terminal-universe]], [[memoharness]]
