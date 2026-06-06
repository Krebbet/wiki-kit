# Cosmos 3: Omnimodal World Foundation Model (NVIDIA)

NVIDIA Cosmos 3 is a family of open-weight omnimodal world models (4B/16B/64B) that jointly generate language, image, video, audio, and action within a single model, achieving #1 open-weight across T2I, I2V, T2V, and robot-policy benchmarks as of June 2026. It is the strongest empirical evidence to date for [[conflicts/pure-video-vs-3d-world-models]] Position B: action-conditioned interactive world simulation is achievable without explicit 3D scaffolds.

## Architecture — Mixture-of-Transformers (MoT)

Each transformer layer carries two independent parameter sets: a **Reasoner tower** (causal self-attention over AR tokens) and a **Generator tower** (bidirectional attention over the union of AR+DM keys/values). Both towers co-initialize from a pretrained VLM (Qwen3-VL-8B for Nano, Qwen3-VL-32B for Super). AR tokens never attend to DM tokens, preserving autoregressive integrity; DM tokens attend to all context:

- AR: `O_AR = Attn_causal(Q_AR, K_AR, V_AR)`
- DM: `O_DM = Attn_full(Q_DM, [K_AR; K_DM], [V_AR; V_DM])`

Three scales — Edge (4B), Nano (16B), Super (64B) — with total parameters counting both Reasoner+Generator tower sets per layer.

**Token layout.** All tasks share one sequence format: AR subsequence (ViT-encoded visual + language tokens) followed by DM subsequence (VAE-encoded video/image + audio + action tokens). Generation modes (T2I, T2V, I2V, FD, ID, policy) differ only in which DM tokens are noisy vs clean — no architectural switching.

**Action as a first-class modality.** Domain-aware linear projectors (`W_in^(k)`, `W_out^(k)`) per embodiment domain map ego poses (9D SE(3)), effector poses (9D), and grasp states into a shared pseudo-action space (9–57D), sharing the MoT backbone across autonomous vehicles, cameras, and robots.

**Position embedding.** Extended 3D MRoPE with absolute temporal modulation. A 15000-position temporal gap separates AR and DM subsequences to prevent over-saturation from adjacent text/vision embeddings.

## Training

Rectified flow matching (`v* = ε - x0`) for generation; logit-normal noise sampling for images/audio/action, mode sampling for video. Multi-resolution (256p/480p/720p), 5 aspect ratios, up to 400 frames, 74k-token packed context.

Four stages: (1) image/video/audio pre-training (Nano: 31T tokens / 1024 GB200s; Super: 18T tokens / 2048 GB200s); (2) mid-training adds action (25%), transfer (25%), audio (8%); (3) T2I post-training; (4) I2V/policy post-training. Reasoner training: 22M-sample pre-training + 2.2M-sample SFT with AI-judge quality filtering.

## Results

**Image generation (T2I):** UniGenBench 91.36 (#1 open, beats FLUX.2-dev 87.60); #1 open-weight on Artificial Analysis T2I (2026-05-28).

**Video generation (T2V/I2V):** PAIBench-G T2V 80.0 (beats Veo-3.1 79.1 closed); PAIBench-G I2V 82.8 (#1 open, matches Veo-3.1 82.6 closed); HWB human-preference 71.9 (best overall including closed, vs Veo-3.1 67.8); Physics-IQ V2V 63.4 with BoN.

**Reasoning (Cosmos3-Super vs domain-tuned baselines):**
- Driving: 79.3 (best overall)
- Smart Infra: 62.6 (best overall, above Gemini 3.1 Pro 58.6)
- General: 73.7 (vs Qwen3-VL-32B 72.8, below Gemini 3.1 Pro 77.5 closed)

**Robot policy (RoboLab-120):** 39.7% task success vs π0.5 28.1%, GR00T N1.6 5.3%; #1 on RoboArena (2026-05-30).

**Forward dynamics (DROID):** PSNR 26.04 dB vs Ctrl-World 22.99 dB.

## Applicability

Nano (16B) fits on a single H100 80GB. Super (64B) requires multi-GPU. Action generation requires domain-specific projection heads; not zero-shot to new embodiments without post-training (MT-init needs ~500 steps to 24.6% on LIBERO-10). Context capped at 74k tokens (limits 720p video to ~300 frames). Inference via vLLM, TensorRT-LLM (Reasoner), vLLM-Omni (Generator).

## Source

- arXiv: https://arxiv.org/abs/2606.02800 (2026-06-03)
- Weights: huggingface.co/collections/nvidia/cosmos3 (OpenMDW-1.1)
- Code: github.com/nvidia/cosmos

## Related

- [[moonlake-world-models]] — Cosmos 3 is the primary empirical counter to Moonlake's "pure video cannot yield interactive simulation" thesis
- [[conflicts/pure-video-vs-3d-world-models]] — Position B evidence; updates the conflict with the first interactive-simulation counter
- [[vision-banana]] — static-3D-prior side of the same debate
- [[sharp-view-synthesis]] — adjacent view-synthesis cluster; complementary problem domain
- [[tidar]] — NVIDIA AR+diffusion inference; action-conditioned generation shares motivation
