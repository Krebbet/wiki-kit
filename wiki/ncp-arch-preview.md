# NCP-ArchPreview: Latent-Space Language Modeling via Next Concept Prediction

Shanghai AI Lab / SJTU (arXiv:2609.10715) scales discrete-concept latent-space language modeling — joint Next-Token-Prediction (NTP) + Next-Concept-Prediction (NCP) over a product-quantized concept vocabulary — to 8.9B params / 5.73T tokens, the largest latent-space LM demonstration to date. Converges 1.95× faster than a token-matched OLMo-3-7B baseline and beats it on a 30-benchmark downstream macro-average (+2.45 pts, +5.99 GSM8K). Direct architectural descendant of ConceptLM (Liu et al. 2026), scaled from ≤1.5B to full frontier-scale pretraining plus a new hierarchical residual-connection mechanism.

## Architecture

Forks an OLMo-3-7B-style 32-layer Transformer into three pieces: a 16-layer Token Encoder, an 8-layer Concept Module, and a 16-layer Token Decoder. Token Encoder hidden states are mean-pooled into concept vectors (chunk size k=4), then mapped to a discrete codebook via **product quantization** (32 codebooks × 128 entries × dim 128, giving N^S combinations from small per-segment codebooks). The Concept Module autoregressively predicts a distribution per PQ segment and forms a differentiable predicted concept as the expectation over codeword embeddings — soft/weighted, not argmax/sample, keeping NCP loss end-to-end differentiable. Predicted concepts are causally shifted back to token resolution and added residually into the Token Decoder.

**Hierarchical residual connections (new).** IRC (IntraModule) generalizes MUDDFormer's per-layer dynamic dense connections to a single hidden stream; CRC (CrossModule) is a softmax-gated cross-module state transfer (Encoder→ConceptModule, Encoder→Decoder, ConceptModule→Decoder) with learned diagonal scaling, initialized near-zero.

Joint loss: L = L_NTP + α·L_NCP + β·L_VQ, where L_VQ is a stop-gradient codebook-fitting loss and L_NCP is MSE between predicted and stop-gradient true concept. Optimized with Moonlight Muon (built on Jordan et al.'s Muon) for matrix params, AdamW elsewhere. Base backbone/data recipe (Dolma 3 Mix → Dolmino) and eval protocol borrowed directly from OLMo-3, keeping baselines directly comparable — a methodologically stronger head-to-head than most latent-LM comparisons in this wiki, since [[coladlm]]'s own PPL is explicitly not AR-comparable while NCP-ArchPreview reports directly comparable token-level loss and downstream deltas.

## Results

- **Convergence:** Stage-1 (Dolma 3 Mix, full 5.73T tokens) — 1.95× faster than token-matched OLMo-3-7B, 0.091 lower final loss. Stage-2 (Dolmino) — 1.51× faster, 0.027 lower loss.
- **Downstream (30-benchmark macro-average):** Stage-1 +2.45 pts (46.59→49.04), GSM8K +5.99, MATH avg +3.75, Code avg +2.64. Stage-2 +0.59, gains concentrated outside code (Stage-2 data is ~10% code, so code regresses).
- **Compute-matched ablations:** NCP-ArchPreview (40 P_blk params / 34 F_blk compute) beats both a compute-matched and a plain-32-layer OLMo-3-7B baseline, approaching a size-matched 40-layer baseline at 85% of its compute.
- **Hierarchical residual ablation:** full IRC+CRC gives 0.0323 loss reduction for +0.051% FLOPs; a competing "Block AttnRes" design gets only 0.0180 at comparable FLOPs.
- **Scaling law:** 1.74× compute efficiency vs. OLMo-3 compute-optimal training.
- **Downstream reuse findings:** (1) updating only the 17M-param VQ module (frozen backbone) beats parameter-matched LoRA on code/math with the smallest general-capability forgetting, at 1.5–2× higher training throughput; (2) injecting Concept Module states into a DFlash2/DFlare-style speculative drafter raises mean accepted length +4.17% (+7.59% on HumanEval) at no extra target-model compute.

## Novelty

A refinement/scaling of ConceptLM rather than a new mechanism — the paper's own related-work section says so directly. What's new: scaling NCP to 8.9B/5.73T with NCP active from step 0 (vs. ConceptLM's ≤1.5B or continual-pretraining addition); the IRC/CRC hierarchical residual design, validated against a competing scheme and the second-largest contributor to loss reduction after the Concept Module itself; and two novel downstream applications (VQ-only lightweight domain adaptation, concept-injection into speculative drafters).

## Applicability

Frontier-lab-scale pretraining change (5.73T tokens, from-scratch), not cheaply retrofittable. But released Stage-1 checkpoints (every 100K steps) plus the 17M-parameter VQ-only adaptation path make downstream reuse accessible: teams with a checkpoint and modest compute can do domain adaptation via the VQ module alone, or splice concept representations into an existing speculative decoder for a near-free accepted-length gain.

## Reproducibility

High. HF collection with Stage-1 checkpoints every 100K steps, drafter models, and final checkpoints (huggingface.co/collections/ArchSpace-Collection/ncp-archpreview); inference via InternLM/lmdeploy; eval harness at github.com/LUMIA-Group/ncp_olmo_eval; full architecture/forward-pass pseudocode in Appendix B. Built on fully open OLMo-3 backbone/data.

## Source

`raw/research/weekly-2026-09-12/01-ncp-arch-preview.md` (arXiv:2609.10715)

## Related

- [[coladlm]] — parallel large-scale latent-space-LM bet (continuous latent diffusion vs. this page's discrete concept-prediction-as-auxiliary-objective); both argue latent/concept structure scales, via structurally different mechanisms.
- [[elf-embedded-language-flows]] — another continuous-embedding-space LM (Flow Matching) discarding token-level generation until t=1; contrasts with this page's choice to keep full token-level NTP as primary and add concept prediction as a parallel objective.
- [[manifold-constrained-hyper-connections]] / [[hyperloop-transformers]] — prior dynamic/hyper residual-connection mechanisms (Sinkhorn-constrained HC; loop-level mHC); IRC/CRC is a third variant in this space, built on MUDDFormer.
- [[deepseek-v4]] — shares the Muon optimizer family (Moonlight Muon here vs. plain Muon there, both from Jordan et al. 2024).
- [[conflicts/pixel-space-vs-latent-space-generation]] — this page extends the "is compressed/latent representation the right scaling axis" question from vision generation into language-model pretraining, via a still-different mechanism than either side of that conflict.
