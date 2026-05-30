# SenseNova-U1: Unifying Multimodal Understanding and Generation with NEO-unify

SenseNova-U1 (arXiv:2605.12500) is a fully end-to-end unified multimodal model — 8B dense and 30B-A3B MoE — instantiating the NEO-unify architecture: no pretrained vision encoder, no VAE, single Mixture-of-Transformers backbone jointly trained with AR cross-entropy (language) + pixel-space flow matching (vision). On image understanding, 8B beats Qwen3VL-8B-Think on MathVision (75.82 vs 62.70) and VSI-Bench (62.66 vs 56.61); on generation, GenEval 0.91 overall bests all open-source and matches closed GPT-Image-1/Seedream 3-4 (0.84); image reconstruction at 32× compression matches FLUX.1-dev VAE PSNR 31.56 at 8×. Weights and code are public.

## Architecture

NEO-unify backbone: understanding and generation share one MoT (Mixture-of-Transformers), with fully decoupled stream parameters — separate projection, norm, and FFN per stream, dynamically routed by token type. No pretrained VE or VAE.

Visual interface: two conv layers (stride 16×2 = 32× total compression) replace VE for encoding; MLP head replaces VAE decoder for generation. Native 3-axis RoPE (T/H/W).

Attention mask structure: text tokens causal; image tokens bidirectional within block, causal to preceding context; noise tokens have full access to clean tokens, clean tokens blocked from noise. MHSA shared across understanding (clean) and generation (noise) streams.

Joint objective: AR CE with λ₁=0.1 + pixel-space flow matching MSE with λ₂=1.0. Rectified-flow x-predict / v-loss from JiT. Resolution-adaptive noise scale σ_R = σ₀√(N/N₀). CFG: text guidance γ=4, image-context γ_img=1; text cond dropped p=10%, both dropped p=10%.

Scale: 8B dense (42 layers, 4096 hidden); 30B-A3B MoE (48 layers, 128 understanding experts + 32 generation experts, top-k=8, ~3B active).

## Training

6-stage recipe, ~3.45T tokens total:

1. Understanding warmup from NEO checkpoint.
2. Generation pretraining — 3 phases, 256²→2048² resolution.
3. Unified mid-training — 84K steps, 1.19T tokens.
4. Unified SFT — 9K steps.
5. Post-training via Flow-GRPO — OCR-IoU text-rendering reward, VLM style reward, HPSv3 aesthetic reward.
6. Step distillation via DMD2 — 100 NFE → 8 NFE.

Disaggregated inference: LightLLM (AR) + LightX2V (diffusion) with pinned shared memory; hybrid FlashAttention3 kernel for mixed causal/bidirectional prefill.

## Results

**Image understanding (8B vs Qwen3VL-8B-Think):** MMMU 74.78 vs 74.10; MathVision 75.82 vs 62.70; VSI-Bench 62.66 vs 56.61 (32-frame EASI). A3B: MMMU 80.55, MathVision 79.63.

**Text understanding:** IFBench 67.01 (8B) vs 29.93 (Qwen3VL-8B); τ²-Bench 71.70 vs 31.65.

**Image generation — GenEval:** 0.91 overall (both 8B and A3B); beats Qwen-Image 20B (0.87), BAGEL 7B (0.82), FLUX.1-dev (0.66); matches closed GPT-Image-1/Seedream 3-4 (0.84).

**DPG-Bench:** A3B 88.14, 8B 87.78 (vs Qwen-Image 20B 88.32, Seedream 4.5 closed 88.63).

**Text rendering CVTG-2K:** 8B best open-source avg word accuracy 0.940 (vs Emu3.5 32B 0.912, Qwen-Image 20B 0.829). LongText-Bench: 8B EN 0.979 / ZH 0.962.

**WISE:** A3B-SFT w/CoT 0.81 — large gap over open-source.

**OpenING:** A3B-SFT w/CoT 9.16 best open-source (Nano-Banana closed 8.85; GPT-4o+DALL-E3 8.20).

**RealUnify:** 8B 52.4 overall (BAGEL 42.9).

**Image reconstruction (MS-COCO 512, Table 23):** NEO-unify 2B 31.56 PSNR / 0.85 SSIM at 32× compression, matching FLUX.1-dev VAE 31.56 PSNR / 0.93 SSIM at 8×.

Ablation: understanding–generation co-training converges with minimal conflict; consistent data-scaling on DPG-Bench/WISE/GEdit-Bench/RISEBench.

## Novelty

NEO-unify (March 2026 blog) established the architecture; SenseNova-U1 is a scaled, refined instantiation. New contributions beyond NEO-unify: (1) full parameter decoupling between streams in MoT; (2) resolution-adaptive noise scale σ_R; (3) 6-stage recipe integrating Flow-GRPO + DMD2; (4) disaggregated LightLLM+LightX2V shared-memory inference system; (5) comprehensive SOTA eval across unified multimodal leaderboards. Closest prior: NEO-unify (same arch, smaller), BAGEL (shared backbone + VAE), Show-o/Janus-Pro (shared backbone + VE/VAE), Tuna-2 (pixel-space generation but not fully encoder-free for understanding).

## Reproducibility

Code: github.com/OpenSenseNova/SenseNova-U1 (open). Weights: huggingface.co/collections/sensenova/sensenova-u1 (released). NEO-unify blog: huggingface.co/blog/sensenova/neo-unify. Demo: unify.light-ai.top. No independent reproduction yet as of capture date 2026-05-18.

## Positioning

**vs [[vision-banana]]:** Both argue generation–perception unification, but different routes. [[vision-banana]] instruction-tunes a generative model for perception (generation-first, perception added). SenseNova-U1 jointly trains one backbone both directions from the start. Complementary design philosophies, not contradictory.

**vs [[coladlm]]:** Opposing latent-space bet. [[coladlm]] advocates Text VAE + latent diffusion scaling. SenseNova-U1 eliminates the VAE entirely and operates in pixel space — 32× compression conv layers match FLUX.1-dev VAE PSNR at 8×, challenging the assumption that latent compression is necessary. Tension documented in [[conflicts/pixel-space-vs-latent-space-generation]] (SenseNova-U1 = pixel side).

**Flow-GRPO post-training** is the same RL-over-flow paradigm as [[agentflow]] applies to agentic trajectories — here applied to image generation quality rewards.

## Source

`raw/research/weekly-2026-05-18/05-sensenova-u1.md` (arXiv:2605.12500)

## Related

- [[vision-banana]] — generation-first unification; complementary approach
- [[coladlm]] — latent diffusion + Text VAE; opposing pixel-vs-latent bet
- [[conflicts/pixel-space-vs-latent-space-generation]] — tension SenseNova-U1 (pixel) vs CoLaDLM (latent)
- [[agentflow]] — Flow-GRPO applied in agentic context; same post-training paradigm
- [[tidar]] — multimodal understanding scaling; adjacent leaderboard territory
