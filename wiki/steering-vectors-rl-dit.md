# Steering Vectors for RL in Diffusion Transformers ("All That RL for a Constant Shift?")

Fixed per-block steering vectors added to a frozen diffusion transformer, fitted by velocity matching to an RL-tuned checkpoint (no reward model, no sampling), recover 90.0-96.3% of the RL reward gain on six image models and 89.8% / 111.9% on two video models. Training the vectors directly with Flow-GRPO reaches 103.6-104.6% of the RL-tuned gain. Implication: most diffusion-RL gain is a prompt-independent constant shift. arXiv 2611.26627; title inferred from the Fig. 1 caption (capture is untitled).

## Method
- One constant vector in R^d per block output, added to every token; indexed by block, guidance pass (cond/uncond), step bin (K=2: early t>=0.75 / late) and stream (image/text in MMDiT). alpha=1. No dependence on prompt, token, seed or resolution.
- 288,768 params on SD3.5-M: 1.5% of the rank-32 Flow-GRPO LoRA (18.8M), 65x fewer.
- Fit: velocity matching, ||v_{theta,s} - v_{theta_RL}||^2 on cached, re-noised final samples of the RL-tuned model. Both models frozen. At most 17 H100-h per image model, 70 per video model.
- Baseline s_mean: mean activation difference (RL minus base) per block, i.e. contrastive activation steering. Also s_RL: vectors trained from zero with Flow-GRPO on frozen SD3.5-M.
- Mechanism probes: restricted vector sets (cond pass, text stream, early bin); swapping in the unsteered base's text K/V that image queries read.

## Results
- Table 1, share of RL gain, fitted (mean-diff in parentheses): SD3.5-M PickScore 90.8 [89.8, 91.7] (61.0), OCR 94.4 (21.5), GenEval 95.9 (12.2); FLUX.1-dev LoRA PickScore 90.0 (64.7); DanceGRPO full fine-tune HPSv2.1 96.3 (79.0); Wan2.1-1.3B HPSv3 111.9 [106.5, 118.0] (59.3); Wan2.2-5B VBVR-Pro 89.8 [76.2, 105.6] (60.8). Fitting beats averaging everywhere.
- GenEval: on prompts the base rarely solves, vectors recover 97.7% of the +0.641 gain.
- Alternatives (fitted gate scales, conditioning offset, prompt suffix, higher CFG) gain <30% of the vectors' gain; a fitted prompt token recovers 7-32%; a global color transform 8%.
- Table 2: vectors match the RL model on out-of-objective scorers (HPSv2.1 +0.0393 vs +0.0407; ImageReward +0.400 vs +0.388) and diversity (0.847 vs 0.850).
- Table 3: s_RL 103.6% (PickScore), 104.6% (OCR). User study (50 prompts, 25 raters): 60-65% win vs base, 50-52% vs RL-tuned (indistinguishable).
- Same-size LoRA fitted with the same loss: no detectable advantage on SD3.5-M/FLUX/VBVR-Pro; on Wan2.1 69.7% vs 111.9% for vectors. For SFT (DreamBooth) vectors fall short (68-83% identity gain on fictional people, 73-95% on public LoRAs) and a same-size LoRA recovers more.
- Transfer: fitted at 512px, applies at 768/1024px; Wan2.1 fitted at 33 frames, evaluated at 81; across step counts and CFG scales (Fig. S1).
- Where the gain acts (SD3.5-M): cond-pass-only beats the full set; early bin dominates; text stream carries most gain alone. Cond+text+early (35,328 params, 0.19% of LoRA) recovers 89.5% (OCR) / 73.7% (PickScore). Reading base-model text K/V keeps 20.5% / 10.5% of vector gains; resetting what text reads from image keeps >=84.4%. Both steering and RL work via image tokens reading text through joint attention.

## Applicability
- Tiny swappable "RL adapters" for DiTs: one add per block output at inference; composable/distributable. Also a cheap RL parameterization (train only constant vectors with Flow-GRPO).
- Diagnostic: how much of an RL gain is prompt-independent.
- Needs a frozen base DiT plus either a public RL-tuned checkpoint (fit) or a reward and Flow-GRPO loop (direct). No LLM experiments; LLM relevance is by analogy only (Sinii et al., Vakada et al. RL-trained steering vectors).

## Caveats / Reproducibility
- Only 2 of 6 public RL-tuned video models showed a gain with CI above zero; video evidence rests on two models.
- Authors disclaim "RL is low-rank": full fine-tunes also recover 96.3%. Not a general claim for SFT.
- Public checkpoints evaluated (Flow-GRPO SD3.5-M, FLUX LoRA, DanceGRPO, GenRL Wan2.1, VBVR-Pro); paired bootstrap CIs; hyperparameters in appendix Tables S1-S14. No code or weights link found in the captured text.
- Partial read: main text (method, experiments, mechanism, conclusion) and Limitations; bibliography and most appendix tables skimmed or unread.
- Novelty is recombination (activation steering + velocity-matching distillation + Flow-GRPO); the new part is the empirical finding and the joint-attention analysis. Closest prior: RaTE (single prompt token), BitFit/DiffFit/Calibri, task arithmetic.

## Source
- raw/research/weekly-2026-11-21/01-activation-steering-rl-dit.md
- https://arxiv.org/abs/2611.26627

## Related
- [[reasonmaxxer]] - LLM-side parallel: RL gain captured by a tiny correction (1-4% of tokens, rank-32 LoRA); this is the diffusion-side analogue.
- [[deletion-tuning]] - tiny-parameter adaptation (mask over <0.05% of weights) matching full RL fine-tuning.
- [[poem-predicting-rl-outcomes]] - RL outcomes are low-dimensional and composable.
- [[ride-opd-residual-extrapolation]] - RL-teacher-minus-base residual treated as a transferable object.
- [[agentflow]] - source of Flow-GRPO, the RL algorithm used here.
- [[delta-mem]] - frozen backbone with small added state.
- [[sensenova-u1-5]] - RL post-training of image generators with velocity distillation.
- [[asymflow]] - flow-matching velocity-space diffusion, same model family.
- [[spurious-rewards-rlvr]] - RL amplifies latent base behaviour; consistent with a constant shift.
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] - diffusion-side data point for the "RL gain is sparse/simple" camp; LLM-side evidence favours input-dependent token selection, so this is a modality difference, not a conflict.
