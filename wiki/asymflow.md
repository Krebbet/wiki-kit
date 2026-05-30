# Asymmetric Flow Models (AsymFlow)

Stanford preprint (arXiv:2605.12964). AsymFlow introduces a rank-asymmetric velocity parameterization for flow/diffusion models: the data prediction term x₀ remains full-dimensional while the noise term ε is projected onto a low-rank PCA subspace (r=8 optimal, D=768), letting a vanilla DiT handle pixel-space ImageNet 256² generation unmodified. Achieves FID 1.57 (+REPA) — best among plain-transformer pixel diffusion methods — and enables principled latent→pixel finetuning of pretrained latent diffusion models (e.g. FLUX.2 klein) via Procrustes alignment without architectural changes.

## Method

Redefines the flow-matching velocity target asymmetrically: asymmetric target u_A := Pε − x₀ where P = AA^T, A ∈ ℝ^(D×r) orthonormal, learned from patch-wise PCA. Full-rank velocity recovered analytically from the network's asymmetric prediction via x₀-to-u conversion in the orthogonal complement. Standard flow-matching loss and sampling schedule unchanged. Generalizes x₀-prediction (r=0) and full u-prediction (r=D) as endpoints. Closest prior k-Diff (Jin & Wang 2026) interpolates isotropically; AsymFlow's restriction is PCA-aligned and directional, not isotropic.

Latent→pixel lift: pretrained latent model (patch dim d) adapted to rank-d pixel flow via Procrustes alignment (A aligns latent↔pixel patches), A^T/A fused into input/output linear layers as init. Finetuning corrects only the low-level projection gap x₀ − x₀^L. Variance-reduced finetuning loss (control-variate vs frozen init copy) + LPIPS perceptual correction improve convergence and texture. Derives from flow matching (Albergo & Vanden-Eijnden 2023; Lipman 2022; Liu 2022), JiT (Li & He, CVPR 2026), DiT (Peebles & Xie 2023).

## Results

**ImageNet 256² pixel diffusion** (Table 2): AsymFlow-H/16 (953M, 363 GFLOPs) + REPA = FID 1.57. Best among plain-transformer (DiT-like) pixel diffusion — beats JiT-H/16 (1.86*), PixelREPA-H/16 (1.81*), PixelGen-XL/16 (1.83). Only SiD2-UViT/1 (1306 GFLOPs, hierarchical) reaches lower at 1.38. Without REPA: AsymFlow-H/16 FID 1.76 vs JiT-H/16 1.90 (Table 1); less sensitive to σ_min clamping (degradation 0.52 vs 1.37 FID for JiT). Convergence 40% faster than JiT (Fig 6).

**Text-to-image 1024²** (Table 4): AsymFLUX.2 klein (finetuned from FLUX.2 klein 9B, rank-256 LoRA, LAION-Aesthetics 3M) — HPSv3 10.66, DPG-Bench 86.8, GenEval 0.82. Beats FLUX.2 klein latent base (9.50 / 85.2 / 0.80) on all three metrics and substantially beats prior pixel T2I PixelDiT-T2I (8.95 / 83.5 / 0.74).

## Novelty

Prior pixel diffusion addressed the high-dim noise bottleneck via hierarchical skip-connection architectures (U-ViT, hourglass), decoder heads (DDT, PixelDiT, DeCo), or x₀-prediction (JiT) at the cost of low-noise numerical instability. AsymFlow is the first method to treat the two velocity components asymmetrically — full-rank data, low-rank noise — enabling a vanilla DiT to operate in pixel space unmodified. Also the first principled latent→pixel initialization path (Procrustes lift + trajectory-coupling theorem).

## Reproducibility

Preprint only; no code or weights released as of 2026-05-18. Project page: https://hanshengchen.com/asymflow. Finetuning details in appendices. No paperswithcode entry, no citations/reproductions yet. Stanford (Wetzstein + Guibas groups).

## Source

`raw/research/weekly-2026-05-18/04-asymflow.md` (arXiv:2605.12964)

## Related

- [[coladlm]] — parallel latent→pixel lift idea; VAE→DiT pipeline structurally analogous to AsymFlow's Procrustes-based latent→pixel init; no contradiction in-domain
- [[sharp-view-synthesis]] — CV/generative area; pixel-space generation quality relevant
- [[moonlake-world-models]] — CV/generative area; pixel-space modeling context
- [[conflicts/pixel-space-vs-latent-space-generation]] — AsymFlow FID 1.57 is direct supporting evidence for the pixel-space side
- [[conflicts/regression-vs-diffusion-view-synthesis]] — tangential; pixel-space diffusion competitiveness relevant to the broader regression-vs-diffusion debate
