# Pixel-Space vs Latent-Space (VAE) Generative Modeling

**Status:** open. Opened 2026-05-18 from the weekly-brief ingest of [[sensenova-u1]] + [[asymflow]] against the existing [[coladlm]] claim. This is an architectural design-bet conflict, not a single benchmark dispute.

## Position A — Eliminate the VAE; model directly in pixel/embedding space

**Sources:** [[sensenova-u1]] (SenseNova-U1 / NEO-unify, arXiv:2605.12500), with supporting evidence from [[asymflow]] (AsymFlow, arXiv:2605.12964).

**Claim:** A pretrained-encoder/VAE latent bottleneck imposes "scaling limitations from fixed representations" and is unnecessary. SenseNova-U1 replaces the VE with two conv layers (32× compression) and the VAE decoder with an MLP head, jointly trained pixel-space flow matching + AR cross-entropy in one MoT backbone.

**Basis / empirical:**
- SenseNova-U1 §5.2.1, Table 23: NEO-unify 2B at **32× compression matches FLUX.1-dev VAE PSNR (31.56 = 31.56) at 8× compression** on MS-COCO 512; top open-source on GenEval (0.91), DPG-Bench, OpenING, WISE, RealUnify with no VE/VAE.
- AsymFlow (head-to-head in the *image* domain): pixel-space DiT reaches **ImageNet-256 FID 1.57** (best among plain-transformer pixel diffusion); and **AsymFLUX.2 klein (pixel finetune) beats the FLUX.2 klein latent base on HPSv3 10.66 vs 9.50, DPG 86.8 vs 85.2, GenEval 0.82 vs 0.80** — direct evidence that lifting a latent model to pixel space improves it.

## Position B — Latent VAE compression is the right scaling direction

**Source:** [[coladlm]] (CoLa-DLM, ByteDance Seed, arXiv:2605.06548).

**Claim:** A causal Text VAE (d=16) feeding a block-causal DiT latent prior (Flow Matching) is the compute-optimal path; the latent bottleneck is what yields the best scaling curve at high compute (~2000 EFLOPs) vs matched AR and LLaDA, and reduces sequential decoding depth ~1.6–2×.

**Basis:** CoLa-DLM architecture (Text VAE → DiT prior → conditional decoder) and its high-compute scaling-curve argument; §5.5 multimodal extension.

## Domain-mismatch caveat (why this is "open", not "resolved")

CoLa-DLM is a **text** diffusion LM; SenseNova-U1 is a **unified multimodal** model; AsymFlow is **image** generation. There is no single shared benchmark across all three, so the conflict is currently an *opposing architectural intuition* rather than a settled head-to-head — **except** in the image domain, where AsymFlow's AsymFLUX.2 pixel-vs-latent comparison is a clean controlled result favouring Position A. Position B has no analogous controlled refutation captured yet, and CoLa-DLM's scaling-curve claim is at a compute scale (~2000 EFLOPs) none of the Position-A sources test.

## Resolution rule

Resolve per-domain on a shared benchmark at matched params/compute:
- **Image:** AsymFLUX.2 vs FLUX.2-klein (already controlled) — extend if a latent-side rebuttal at matched finetuning budget appears.
- **Text:** awaiting a pixel/embedding-space text LM evaluated against CoLa-DLM at matched compute (note [[elf-embedded-language-flows]] is embedding-space — *not* pixel, *not* a VAE — and is parallel to, not a clean test of, this axis).
- **Unified multimodal:** awaiting a VAE-based unified model matched to SenseNova-U1's training budget.
Treat CoLa-DLM's high-compute scaling claim as **unrefuted at its own scale** until a Position-A source tests there.

## Related

- [[sensenova-u1]], [[asymflow]], [[coladlm]], [[elf-embedded-language-flows]], [[tidar]], [[vision-banana]]
- [[conflicts/regression-vs-diffusion-view-synthesis]] — adjacent: regression-vs-diffusion is a different generative-modeling design-bet axis.
