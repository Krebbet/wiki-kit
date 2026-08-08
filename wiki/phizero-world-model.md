# PHIZERO: A World Model Built Around Physical Language

CASIA/NLPR (arXiv:2607.28624, Jul 2026). Introduces a video world model that learns a compact discrete "physical language" from unlabeled in-the-wild video via self-supervision, then reasons about future world evolution in that discrete space before rendering it into video — replacing direct pixel-space prediction with a reason-then-render paradigm.

## Method

Two components. **Physical Language Tokenizer**: a spatiotemporal encoder feeds pairs of adjacent latent frames into a shared transition-level Q-Former (32 learnable queries) that extracts per-interval transition features, discretized via Finite Scalar Quantization (25K-symbol vocabulary, no learned codebook). A pretrained video diffusion model (Wan2.2-5B, LoRA rank 32) is repurposed as decoder, with its text-conditioning slot replaced by the physical-language context and the first frame supplied as a separate clean condition, so the discrete bottleneck carries only state-*change* information. **Physical Language Reasoner**: a pretrained VLM (Qwen3-VL-4B), vocabulary-extended with one atomic symbol per FSQ index, autoregressively predicts the physical-language sequence from a first frame + textual action intent — decoupling "what happens" (symbolic reasoning) from "what it looks like" (diffusion rendering). Generalizes latent-action learning (Genie-style) from embodiment/task-specific control tokens to an open-domain reasoning target.

## Results

Video generation: Physics-IQ Verified IQ-Score 41.2 (best; vs Wan2.2-14B 32.2, Cosmos3-Super 39.5); best-in-class on PhyGround and WorldModelBench. Tokenizer compression: 256 discrete symbols vs Wan2.2 VAE's 44,800 continuous tokens, at PSNR/SSIM/LPIPS beating other compressed tokenizers. Reasoner ablation (Physics-IQ IQ-Score): Wan2.2-5B pixel-space baseline 21.2 → +natural-language prompt enhancement 26.6 → full PHIZERO 41.2 — the physical-language reasoning layer, not prompt conditioning, is what drives the gain. Trained on 128 A100 GPUs; demonstrates cheap domain adaptation (brief tokenizer fine-tuning transfers to driving, robot manipulation, and human-motion domains without paired data).

## Applicability

Requires a pretrained video diffusion backbone and pretrained VLM as initialization, 128-A100-class training infrastructure, and a large curated video corpus. Not a lightweight from-scratch recipe, but the demonstrated cheap domain-adaptation step (brief tokenizer fine-tuning for a new embodiment) looks far cheaper than full pretraining — relevant to labs already running large-scale video-diffusion or VLM training wanting an explicit intermediate reasoning layer for action-conditioned or interactive world models.

## Reproducibility

Project page given; no explicit code or weight release language found in the source. Unusually thorough hyperparameter/dataset documentation aids independent reproduction, but the largest data component (a 50K-hour in-house video pool) is not public.

## Conflicts

Bears directly on [[conflicts/pure-video-vs-3d-world-models]]. PHIZERO's own ablation (pure pixel-space Wan2.2-5B baseline scores far worse; natural-language prompt enhancement barely helps) is evidence *against* the pure-scaling position [[cosmos-3]] is credited with supporting. Simultaneously, PHIZERO achieves interactive, physically-coherent world modeling with **no 3D geometry at all**, which is a different fix than [[moonlake-world-models]]'s 3D-mesh-scaffold remedy for the same diagnosed problem (pixel-only prediction → physically inconsistent outcomes). This is a genuine third position — added to the conflict file as Position C.

## Related

- [[moonlake-world-models]] — both diagnose pure pixel-space prediction as insufficient, but propose incompatible fixes (3D mesh scaffold vs discrete physical-language reasoning).
- [[cosmos-3]] — PHIZERO's ablation is direct counter-evidence using a similar pixel-space baseline family (Wan2.2).
- [[orca-world-foundation]] — parallels PHIZERO's own language-space (not 3D) alternative within the same conflict.
- [[conflicts/pure-video-vs-3d-world-models]] — this source is central evidence for a third position.

## Source

- `raw/research/weekly-2026-08-08/04-phizero-world-model.md` (arXiv:2607.28624)
