# ColaDLM: Continuous-Latent Diffusion Language Model

ByteDance Seed (arXiv:2605.06548). Three-stage hierarchy: (1) a strictly causal Text VAE maps tokens to continuous latent vectors (d=16); (2) a ~1.8B-parameter block-causal Diffusion Transformer (DiT) learns a continuous-latent prior via Flow Matching, with bidirectional attention within blocks and causal cross-block dependence; (3) a conditional decoder reconstructs text tokens from diffused latents. Total ~2B parameters (VAE ~500M + DiT ~1.8B). Matched against same-scale AR and LLaDA baselines across 8 benchmarks under few-shot generative evaluation — ColaDLM's scaling curve is most persistent at high compute (~2000 EFLOPs), with clearest gains on global-semantic tasks (MMLU, RACE, Story Cloze, OBQA). Block-parallel inference yields ~1.6–2× reduction in sequential decoding depth vs token-by-token AR; not a full 16× because denoising steps remain sequential.

## Method

- **Text VAE (Stage 1):** Strictly causal encoder maps text to continuous latent z₀ ∈ ℝ¹⁶ (patch size 1 → 1 token per latent, no compression). Causal decoder reconstructs text conditioned on z₀. Training objective: reconstruction NLL + KL regularization + BERT-style masking loss (masking loss prevents encoder semantic collapse, critical during active VAE update).
- **Block-causal DiT (Stage 2 — prior learning):** Flow Matching over latent sequences divided into blocks of 16. Within each block: bidirectional attention. Across blocks: strictly causal (each block conditioned on stop-gradient clean latents of all prior blocks + noisy current block). This is latent prior transport, not observation recovery — distinct from discrete-diffusion (LLaDA, MDLM) and continuous-observation methods (Plaid).
- **Joint training:** VAE and DiT are co-trained in Stage 2 with a shared learning rate and a reference-encoder KL regularizer to prevent latent drift. Fixed-VAE variants saturate earlier; all-scratch underperforms stable-init joint. BERT loss is critical throughout.
- **Conditional decoder:** Auto-regressively decodes each latent block back to text tokens with KV cache after block-level denoising. Prefix tokens are encoded to clean latent conditions; response latents are generated block-by-block via ODE flow from noise. Optimal: 16 denoising steps + CFG=7; quality saturates at ~16–32 steps.
- **Scale and data:** VAE ~500M params, DiT ~1.8B; total ~2B. Trained and evaluated up to ~2000 EFLOPs. Baselines: matched-scale LLaMA-style AR and LLaDA at same 2B scale.

## Results

All evaluations use **few-shot generative evaluation, not likelihood** — a deliberate choice the authors flag explicitly because PPL is structurally misleading for this class: generation requires prior mass to reach semantically valid latent regions, but likelihood also requires local probability calibration around the gold posterior. ColaDLM's PPL is substantially worse than its generation quality implies; direct PPL comparison to AR or TiDAR is not valid.

- **Scaling (Figure 10):** Best Task Average across 8 benchmarks at large compute budgets (~2000 EFLOPs); AR is stronger at small budgets, ColaDLM's curve rises most persistently.
- **Global-semantic tasks:** Clearest wins on MMLU, RACE, Story Cloze, OBQA — consistent with continuous latent prior modeling benefiting tasks that require global semantic planning.
- **Generative tasks:** LAMBADA and SQuAD match or approach AR at larger compute; SQuAD shows particularly clear late-stage gains.
- **Block-parallel efficiency:** 16 tokens generated per DiT block with 8–10 denoising steps → ~1.6–2× reduction in sequential generation depth vs AR. Not a full 16× (denoising steps are still sequential).
- **No specific LAMBADA/MMLU/SIQA numeric accuracy figures** are reported in the summary; results are presented as scaling curves and task-level breakdowns rather than single headline accuracy numbers.
- **Multimodal extension (Section 5.5, qualitative only):** Preliminary text-to-image and image-conditioned text generation via shared block-causal MMDiT prior over modality-specific VAE latents. No benchmark numbers — feasibility proof only.

## Why this matters

ColaDLM is one of three concurrent diffusion-LM papers this week moving beyond naive masked-token generation. The shared structural move across all three (ColaDLM arXiv:2605.06548; Joint Latent DLM arXiv:2605.07933; Break the Block arXiv:2605.02263 — both on watchlist) is decoupling semantic planning in a continuous or latent space from token realization. This is a cluster worth watching: whether continuous-latent or discrete-token diffusion wins the "successor to AR" argument is still open.

The most direct architectural contrast is with [[tidar]]. TiDAR is a hybrid AR + discrete-masked-diffusion model in token space (ByteDance vs NVIDIA; discrete-token counterpart vs ColaDLM's continuous-latent alternative). Both pursue block-parallel generation but from opposite ends of the discrete/continuous spectrum. However, **direct comparison is premature**: TiDAR reports coding + math benchmarks + likelihood at 1.5B/8B scale; ColaDLM reports few-shot generative evaluation across 8 language benchmarks at ~2B scale. The implicit claim from each paper — that its paradigm is the right next step beyond pure AR — is live but not yet adjudicated by a shared eval protocol.

[[latent-grpo]] is a close peer on "continuous latent" LM territory via a completely different mechanism: RL post-training that stabilizes GRPO on vocabulary-superposition latent tokens (Coconut/CoLaR lineage), where ColaDLM does continuous-latent diffusion pretraining. Orthogonal mechanisms, shared concern about continuous latent stability and training dynamics. ColaDLM's joint VAE + DiT training and Latent-GRPO's Latent-SFT → RL pipeline are complementary: one builds the latent prior, the other fine-tunes reasoning within it.

The multimodal angle in Section 5.5 connects to [[vision-banana]]: Vision Banana recasts perception as image generation (generation pretraining as universal substrate); ColaDLM recasts multimodal generation as shared continuous-latent diffusion over modality-specific VAE latents. Both frame generation pretraining as the right unifying primitive, from opposite directions (perception → generation vs language → multimodal). The ColaDLM multimodal result is qualitative-only at this point.

## Reproducibility

No GitHub URL, no Hugging Face weights, no paperswithcode entry referenced in the source. Training framework: standard DiT + Flow Matching on top of causal VAE; no exotic infrastructure described. Evaluation protocol (few-shot generative, 8 benchmarks) differs from TiDAR (coding/math + likelihood, 1.5B/8B) — cross-paper comparison requires a shared eval harness neither paper provides.

## Source

- `raw/research/weekly-2026-05-11/05-coladlm.md` — arXiv:2605.06548.

## Related

- [[tidar]] — discrete-token counterpart: AR+masked-diffusion hybrid in token space; ColaDLM is the continuous-latent alternative. Eval protocols differ; direct contradiction premature.
- [[latent-grpo]] — continuous-latent RL post-training (Coconut/CoLaR lineage); orthogonal mechanism (RL vs diffusion pretraining), shared continuous-latent substrate.
- [[vision-banana]] — shared "generation pretraining as universal substrate" framing; ColaDLM Section 5.5 extends this to multimodal via MMDiT over modality-specific VAEs.
- [[watchlist]] — Joint Latent DLM (arXiv:2605.07933) and Break the Block (arXiv:2605.02263) are concurrent diffusion-LM papers in the same cluster, not yet captured.
