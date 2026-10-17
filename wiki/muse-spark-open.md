# Muse Spark Open: Meta's 816B-A42B Open Multimodal MoE

Meta's Muse Spark Open (Hugging Face launch/integration blog) is an open-weight ~816B-total / ~42B-active MoE with 1M context and text+image+audio+video input, text output, positioned as the most capable US open-weights model. The source gives no capability benchmarks, so that claim is unsubstantiated here; the post documents architecture, deployment footprint and a MoE-LoRA fine-tune recipe. Shares the 256-expert, top-8, 1M-context shape with [[reflection-beam]]. Training recipe and data are not described.

## Architecture

- 62 layers, hidden 8192, GQA (128 Q / 16 KV heads, head dim 64), attention output gate + output norm, QK-norm, learned residual gate instead of a plain sum (contrast with mixing in [[manifold-constrained-hyper-connections]]).
- MoE: the dense FFN of the smaller sibling Muse Glimmer is replaced by 256 experts/layer, top-8 routing; each expert 8192->4096->8192 with its own output norm; experts hold ~97% of params. Untied embeddings (~1.66B each). See [[moe-architecture-survey]].
- Unlike [[reflection-beam]], the captured post describes no sliding-window/global split for the language tower; KV cache is ~250 KB/token (~266 GB at 1M tokens), roughly 7x Beam's 36 KiB/token.
- Multimodal: 1.8B perception encoder (50 layers, 14x14 patches, 2D RoPE + learned absolute pos, full attention every 4th and last layer, rest sparse; derived from Meta's Perception Encoder, arXiv:2504.13181; shared with Muse Glimmer 30B). Audio: convolutional-pyramid tower on raw 24 kHz waveform, 12.5 tokens/s. Video 2 FPS (cap 96 frames) with timestamp text and optional audio.
- Harmony-style channel chat template (from gpt-oss). Reasoning cannot be disabled; effort low/medium/high/xhigh maps to 16/64/256/512 (default xhigh).

## Deployment

- BF16 (~1.5 TB) and NVFP4 (Blackwell; "negligible loss" claimed, unquantified). BF16 needs 4x8 H200 (TP=32); NVFP4 fits one B200 node or 4 GB300 (SGLang); HF Inference Endpoints NVFP4 on 8x RTX Pro 6000 (128K) or 8x H200 (1M).
- Local: 2-bit imatrix quant on M3 Ultra 512GB, 304 GB, 18 tok/s; MLX oQ3e 344 GB, ~21 tok/s gen. Day-0 transformers, llama.cpp, vLLM (plugin), SGLang, mlx-lm.

## Fine-tune recipe

TRL SFTTrainer, LoRA r=16/alpha=32 on q/k/v/o only with experts frozen, FSDP2 (fsdp_size=64) + expert parallel (ep_size=8) on 64 H100s, tulu-3-sft-mixture subset, packing, 500 steps (~2 h, ~8k tok/s). Mean token accuracy 72% to 84%, loss 1.26 to 0.57: chat-template adaptation, not a capability eval.

## Caveats

- No benchmarks, ablations or training details; novelty is architectural description only.
- Qualitative demos only (Pi coding agent with a 2-bit model on Three.js, screenshot-only computer-use agent via OpenEnv, voice-driven shopping agent).
- HF is integrator, not independent evaluator. About 1.6k downloads / 470 likes at capture.
- "Most capable US open-weights" is a different axis from [[kimi-k3]]'s "largest open-weight release" (2.78T, 896 experts); no contradiction. Compare [[deepseek-v4]] (1.6T/49B active, CSA/HCA attention).

## Source

- raw/research/weekly-2026-10-17/05-muse-spark-open.md
- https://huggingface.co/blog/meta-muse-spark-open

## Related

[[reflection-beam]], [[deepseek-v4]], [[kimi-k3]], [[moe-architecture-survey]], [[manifold-constrained-hyper-connections]], [[agents-a1-horizon-scaling]], [[polar-rl-harness]], [[sensenova-u1]], [[openclaw]]
