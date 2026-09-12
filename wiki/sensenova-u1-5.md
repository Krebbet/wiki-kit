# SenseNova-U1.5: Specialize-Then-Unify Multi-Expert RL for Native Unified Visual Intelligence

SenseNova's second-generation native unified multimodal model (8.2B+8.2B-param MoT, encoder-free and VAE-free, extending [[sensenova-u1]]/NEO-unify). Fixes U1's high-resolution decode artifacts with a spatially-coupled decoder and adds a "specialize-then-unify" post-training stack — four independently RL-trained task experts consolidated via multi-teacher on-policy velocity-field distillation — pushing to leading-open-source (and on several benchmarks outright SOTA including vs. closed-source) results across generation, editing, and interleaved-generation.

## Architecture

Retains U1's near-lossless native visual interface (two conv projections, 32× downsample, no external vision encoder, no VAE). **Key change:** replaces U1's per-patch MLP decode head — prone to seams/grid artifacts at high resolution — with a spatially-coupled decoder: Pixel-Shuffle upsampling (×2, ×2, ×8) interleaved with 3×3 convolutions so neighboring tokens exchange information before pixel finalization, jointly trained under the flow-matching objective. Extends resolution-aware noise conditioning to 4096² (from U1's 2048²).

Same native Mixture-of-Transformers backbone as U1 (42 layers, hidden 4096; 8.2B understanding + 8.2B generation params sharing attention as the cross-stream interface, separate FFN/norm per stream). Adds an LPIPS perceptual loss term on the flow endpoint to the unified objective (new vs. U1).

## Post-training: specialize-then-unify

**Stage 4 — four independent RL experts**, each with its own reward/sampler rather than one joint reward (motivated by the claim that joint optimization entangles competing objectives): aesthetic (HPSv3++ preference reward interleaved with a PaddleOCR bilingual OCR reward), OCR/typography (normalized multiset-IoU reward, Precise sampling + GRPO-Guard for stability), image editing (5-dimension VLM-based reward aggregated by **min** — a bottleneck that exposes the weakest dimension — plus a coarse-to-fine sliding optimization window), infographic (3-stage: OCR-reward warmup → DPO → alternating OCR/aesthetic GRPO).

**Stage 5 — multi-expert on-policy distillation (OPD).** Each training sample hard-routes to its frozen expert; student generates its own trajectory, both student and expert are evaluated at the same student-generated state/timestep (stop-gradient), and the student matches the expert's velocity field (L_OPD = E[‖v_θ − v_m‖²]). The distillation timestep follows a Beta(2+3n/N, 5−3n/N) schedule shifting from high-noise/global-structure to low-noise/fine-detail emphasis over training. This is a diffusion/flow instantiation of the same OPD family as [[flux-opd]] and [[dopd-dual-on-policy-distillation]], but hard-routes to four frozen task experts rather than one shared distillation recipe (contrast: Flow-OPD/DiffusionOPD/DanceOPD, each single-task).

## Results

Best-open-source (some outright SOTA including closed-source) across the board: GenEval 0.92 (vs. Qwen-Image 20B 0.87), ImgEdit 4.59 (beats *all* compared models, closed-source included), CVTG-2K dense text rendering 0.948 (beats Seedream 4.5 0.899, GPT-Image-1 0.857), VBVR-Pro-Bench interleaved generation 68.2 (new SOTA, beats Nano-Banana-Pro 56.4), OpenING 9.18 (best of all compared models). RISEBench reasoning-centric editing 38.6, far ahead of next-best open-source (26.9) but still behind closed GPT-Image-1.5 (50.0). Multimodal understanding largely preserved or improved vs. U1 despite the added capability (MMLU-Pro 86.67 vs 81.44), with a few regressions (MMMU 73.86 vs 74.78).

Benchmarks against 20+ contemporaneous native-unified/pixel-space models (Emu3.5, LLaDA-Image, Z-Image, OneCAT, Mogao, HunyuanImage-3.0, etc.) plus closed frontier systems — a signal this category is now crowded and competitive, not niche.

## Novelty

Refinement + recombination, not a new paradigm. The decoder fix is a targeted repair of a known U1 artifact. The larger contribution is methodological: applying multi-teacher OPD to independently-RL-trained diffusion/flow experts with hard-routing, avoiding both single-joint-reward entanglement and single-shared-distillation-recipe collapse.

## Applicability

Lab-scale infrastructure required: a pretrained LLM understanding branch to bootstrap generation, large flow-matching pretraining compute for native 4K pixel-space generation, per-capability reward models, GRPO/flow-RL infra with SDE-style samplers. Most portable ideas for smaller projects: (1) train narrow single-capability RL experts before joint optimization to avoid reward entanglement; (2) min-aggregation ("bottleneck") reward composition for multi-dimensional quality criteria; (3) velocity-field OPD with a Beta-scheduled noise curriculum to consolidate several diffusion/flow experts into one deployable policy without full joint retraining.

## Reproducibility

Weights and demo available now (huggingface.co/collections/sensenova/sensenova-u15, unify.light-ai.top); paper states training code (SFT/RL/OPD) will be open-sourced, not yet confirmed independently. U1's repo (github.com/OpenSenseNova/SenseNova-U1) presumably extends to cover U1.5.

## Source

`raw/research/weekly-2026-09-12/02-sensenova-u1-5.md`

## Related

- [[sensenova-u1]] — direct predecessor/architecture base; this page documents the decoder fix and the full multi-expert RL + OPD stack added on top.
- [[conflicts/pixel-space-vs-latent-space-generation]] — another pixel-space (no-VAE/no-VE) data point beating latent-based open baselines; reinforces the pixel-side position U1 already established.
- [[flux-opd]] / [[dopd-dual-on-policy-distillation]] — sibling OPD refinements; this page's contribution is hard-routed multi-expert-to-single-policy distillation for diffusion/flow rather than a single shared teacher.
