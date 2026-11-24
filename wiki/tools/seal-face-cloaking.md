# SEAL (sparse face cloaking against diffusion personalization)

SEAL ("Location Matters: Sparse Latent-Variance Attacks for Face Privacy against Diffusion Personalization", arXiv 2611.14254, code at github.com/Lvxan/SEAL) is an academic proposal for a sparse adversarial perturbation, touching about 5% of pixels, that protects face photos from DreamBooth-style fine-tuning while preserving image quality. It is a per-image, individual, proactive cloaking technique in the same family as [[nightshade-glaze]]. It is peripheral to the wiki's pricing focus; it matters mainly as a worked example of the robustness-versus-quality arms race in [[adversarial-data-poisoning]].

## Mechanism

- Targets the variance of the frozen VAE encoder's latent distribution, using differentiable top-k masking (from SparsePGD) plus a saliency-guided dispersion penalty.
- Sparse (L0-style) rather than dense L-infinity perturbation; choice of pixel *location* is the key factor.

## Reported results (self-reported, preprint)

- PSNR above 41 dB, SSIM 0.97, LPIPS at most 0.07.
- Identity similarity (ISM) at most 0.15 after personalization; random 5% locations give ISM 0.68.
- Benchmarks: CelebA-HQ and VGGFace2; evaluated on Stable Diffusion v2.1 with DreamBooth only.

## Limits

- Does not stop encoder-based methods such as IP-Adapter FaceID.
- JPEG compression, blur and resizing largely remove the perturbation, so platform recompression defeats it unless the release pipeline avoids smoothing. Contrast Nightshade's claimed robustness to such transforms.
- Only fine-tuning attacks tested; no independent replication captured.
- Individual, not collective; could be offered as a shared service *(editorial)*.

## Evaluation-realism caveat

See [[mechanisms/face-cloak-evaluation-protocol]]: reported cloak efficacy drops sharply under detect-align-crop pipelines (arXiv 2611.21923); the resampling mismatch it identifies plausibly explains the resize fragility above.

## Source

- `raw/research/weekly-2026-11-16/02-seal-sparse-latent-variance-face-privacy.md`
  - **Origin:** NUS, NTU, PolyU academic preprint, arXiv 2611.14254 (https://arxiv.org/pdf/2611.14254).
  - **Audience:** ML security and privacy research community.
  - **Purpose:** improve the quality/protection trade-off of dense anti-personalization perturbations.
  - **Trust:** medium; preprint, self-reported benchmarks.

## Related

- [[adversarial-data-poisoning]]
- [[nightshade-glaze]]
- [[obfuscation]]
- [[obfuscation-strategic-readout]]
- [[data-cooperatives]]
