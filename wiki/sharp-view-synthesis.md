# SHARP — Sub-Second Single-Image View Synthesis

Apple (arXiv:2512.10685) regresses a 1.2M-Gaussian 3D scene representation from a single RGB image in **<1s on an A100** via a single feedforward pass, beating diffusion-based view-synthesis baselines on perceptual metrics by **21–43%** while running **1000× faster**.

## Method

Single-image → 3D Gaussian Splatting (per Kerbl et al. 2023) via end-to-end feedforward regression. Pipeline (Fig. 3):

1. **Depth Pro** (Bochkovskii 2025, ICLR) ViT encoder produces 4 multi-scale feature maps from a 1536×1536 input; the low-res image encoder is unfrozen during training, the patch encoder stays frozen.
2. **DPT-based depth decoder**, with the final conv duplicated, emits a **two-layer depth map** (primary surfaces + occluded/view-dependent layer).
3. **Learned "depth adjustment" U-Net** (2M params) ingests both predicted and GT inverse depth and outputs a scale map `S` — explicitly inspired by C-VAE posteriors (Sohn 2015), with KL replaced by an MAE-to-1 plus multiscale TV regularizer acting as an information bottleneck. Replaced with identity at inference.
4. **Gaussian initializer** unprojects the adjusted depth (deliberately *without* intrinsics, working in normalized space) to seed K=14-attribute base Gaussians on a 2×768×768 grid (no spherical harmonics, to keep output size bounded).
5. **Second DPT-style Gaussian decoder** predicts deltas for position/scale/rotation/color/opacity, composed via attribute-specific activations: `G_attr = γ(γ⁻¹(G_0) + η * δG)`.
6. **In-house differentiable splat renderer**; source-view transforms folded into the target projection matrix.

**Loss recipe (Eq. 3.12):** L1 color on input+novel views, VGG-style perceptual + Gram (Johnson 2016 / Gatys 2016 / LaMa-style Suvorov 2022) on novel view, BCE alpha penalty, L1 disparity on first depth layer only, TV on second depth layer, anti-floater gradient regularizer, Gaussian-offset clamp (δ=400), screen-space variance clamp, plus depth-adjustment scale and grad-scale terms.

**Two-stage curriculum (Section 3.3):**
- **Stage 1**: 100K steps on **128 A100s** on synthetic data with perfect GT depth+novel views.
- **Stage 2** = self-supervised finetuning (SSFT): 60K steps on **32 A100s** on real images from OpenScene + online resources. The model's own pseudo-novel render becomes the input view and the real image becomes the supervision target — an **inverted variant of AdaMPI's** (Han 2022) warp-back trick that preserves geometric consistency without requiring stereo pairs.

## Results

Total **702M params (340M trainable)**. Outputs ~1.2M Gaussians per image; rendering >100 FPS on a single GPU; 3D synthesis <1s on A100.

Zero-shot evaluation on Middlebury, Booster, ScanNet++, WildRGBD, ETH3D, Tanks and Temples (Table 1) — **SHARP is best on every (DISTS, LPIPS) cell across all 6 datasets.**

Headline numbers vs. strongest prior (Gen3C, Ren et al. CVPR 2025):
- LPIPS reduced **25–34%**.
- DISTS reduced **21–43%**.
- Synthesis time reduced **~3 orders of magnitude**.

Concrete cells:
- ScanNet++ DISTS: **0.071** (SHARP) vs 0.090 (Gen3C) vs 0.128 (TMPI).
- Middlebury LPIPS: **0.358** vs 0.436 (TMPI).
- Tanks and Temples DISTS: **0.122** vs 0.177 (Gen3C).

PSNR/SSIM in supplement only — authors argue these older pointwise metrics are too sensitive to ~1% translation. Ablations: perceptual loss dominates fidelity gains; depth adjustment boosts sharpness; SSFT crispens real-image renders.

## Applicability

Direct fit for AR/VR "memory revisit" / 3D-photo browsing experiences with natural posture-shift headboxes (the explicit motivating use case). Real-time photo-to-3D for handheld and headset displays. Applicable wherever you want amortized rendering: synthesize once (<1s), render arbitrarily many nearby views at 100+ FPS — useful for interactive editing pipelines, view-consistent 2D-to-3D conversion, and as a fast prior for downstream optimization.

**Not suitable for far-away viewpoints** (explicit limitation; authors flag diffusion+distillation as future work).

Prerequisites: heavy — Depth Pro pretrained weights, 128 A100s for Stage 1 + 32 A100s for Stage 2, in-house differentiable Gaussian renderer, synthetic dataset with perfect depth+novel-view GT for Stage 1, plus access to real single-view image collections (OpenScene-style) for Stage 2. **Inference needs only a single GPU.**

## Novelty

Recombination + careful engineering rather than a wholly new primitive. The core thesis — *"regression-based feedforward beats diffusion for nearby-view single-image synthesis when scaled and tuned right"* — is a deliberate counter-positioning against the diffusion-heavy line (ViewCrafter, ZeroNVS, CAT3D, Gen3C, Wonderland, etc.).

Closest priors: Splatter Image (Szymanowicz 2024, per-pixel Gaussians via U-Net) and Flash3D (Szymanowicz 2025a, adds pretrained depth) — SHARP scales the backbone (Depth Pro ViT vs U-Net), adds the **two-layer depth output**, and introduces the **C-VAE-derived depth-adjustment trick** to handle depth ambiguity for transparent/reflective surfaces. The depth-adjustment module reframed as a learnable scale map with a **non-KL information bottleneck** is the most genuinely novel piece. The SSFT inverted-warp loop is also a small but distinctive contribution vs AdaMPI.

## Reproducibility

Repo URL printed on page 1: <https://github.com/apple/ml-sharp> (Apple ML organization — Apple has a track record of releasing code+weights for related work like Depth Pro). The paper does not state explicitly within the captured text whether weights are released, but the GitHub link strongly implies an official release. No paperswithcode entry confirmed.

Stage 1 synthetic data is "described in the supplement." Stage 2 uses public OpenScene + unspecified online resources. **Compute reproducibility is the main barrier** — 128 A100s for 100K steps is non-trivial.

## Adoption

Too new (December 2025; capture April 2026). Author list is the **Apple Zurich graphics/perception group around Vladlen Koltun and Stephan Richter**, which historically ships influential work (Free/Stable View Synthesis, Depth Pro). Builds directly on Depth Pro (ICLR 2025) and 3DGS (Kerbl, SIGGRAPH 2023, now de-facto).

## Source

- `raw/research/radar-2026-04/08-apple-sharp.md` — SHARP paper PDF (arXiv:2512.10685). Captured 2026-04-22.

## Related

- [[moonlake-world-models]] — adjacent CV cluster; Moonlake's hybrid 3D+video sidesteps the regression-vs-diffusion debate SHARP stakes out.
- [[conflicts/regression-vs-diffusion-view-synthesis]] — SHARP's central positioning claim.
- [[watchlist]] — Depth Pro, 3DGS (Kerbl 2023), Splatter Image, Flash3D, Gen3C, ViewCrafter, CAT3D referenced but not captured.
