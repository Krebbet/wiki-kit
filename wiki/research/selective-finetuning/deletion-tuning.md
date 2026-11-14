# Deletion Tuning: Post-Training by Learning Which Weights to Zero (Lu, Yang et al.)

Deletion Tuning fine-tunes an LLM by learning only a binary mask over the gate-projection weights of each transformer block; the mask zeros fewer than 0.05% of weights and writes no new values. At the largest scale tested per regime (Qwen14B and Qwen3-30B-A3B under GRPO, Qwen7B under SDFT, Llama3B under SFT) it matches full fine-tuning (FFT), with an adapter 600-4,700x smaller than the FFT checkpoint and smaller than rank-1 LoRA. Under GRPO its forward KL stays at or below 0.05 and prior-task accuracy stays within one point of base, while FFT, LoRA and random sparse fine-tuning lose up to 5.4 points. arXiv:2611.10866; no code found (project page agenticlearning.ai/deleting-weights).

Note: main text (sections 1-6, tables 1-6) read in full; appendices A-H (per-run sparsity, per-benchmark, sweeps) were not read.

## Method

- One trainable logit $G$ per weight in the gate projection (the only trainable parameters; base frozen). Training forward pass uses the soft mask $\widetilde W(t)=W\odot\sigma(\alpha(t)G)$; deployment uses the hard mask $\widehat W=W\odot\mathbf 1[G>0]$. Sharpness $\alpha$ is ramped linearly $10^3\to10^4$ ("mask sharpening"); hard vs soft mask differs by at most 0.08 points at the end.
- Wanda prior init: logits drawn from $\mathcal N(\pm0.03,0.01^2)$ by Wanda importance quantile $\eta$ (default $\eta=1/2048$, about 0.18% of gate weights zeroed at init). Loss = regime objective plus a MaskLLM-style sparse weight regularizer ($\lambda=10^{-5}$ for SFT/GRPO, 0 for SDFT). No sparsity target is imposed.
- Regimes: GRPO (verl; rollouts use the hard mask), SFT, SDFT (self-distillation; EMA teacher gate). Adapter = bit-packed mask plus zstd (about 0.03 bits per target weight); task switching = scatter zeros into base weights.
- Models: Llama3.2-1B/3B, Llama3-8B (GSM8K), Qwen2.5 0.5B/3B/7B/14B and Qwen3-30B-A3B (SimpleRL-Zoo math, 6-benchmark mean; MoE: gate in every expert, router untouched). SFT on 14 MMLU-Pro subjects and 23 BBEH subtasks; SDFT on ToolAlpaca and Science. Baselines: FFT, LoRA r=1/4 (all 7 projections), MTH random sparse (99% / 99.95% sparsity), same data and steps.

## Results

| Finding | Number |
|---|---|
| Llama8B GSM8K (GRPO) | DT 83.55 vs FFT 83.24 (base 60.27); 8.4 MB vs 30,633 MB |
| Qwen7B SimpleRL-Zoo | DT 52.32 vs FFT 51.89 (base 40.18); 6.9 MB vs 29,051 MB |
| Qwen14B / Qwen3-30B-A3B | DT 55.43 / 58.54 vs FFT 54.87 / 58.43; 11.4 / 29.6 MB vs 56,343 / 116,471 MB |
| Small scale | 90-99% of FFT (e.g. Llama1B 54.44 vs 60.50; Qwen0.5B 17.64 vs 19.01); gap closes with scale |
| Pass@k (128 samples, T=1) | Llama8B k=1 81.75 vs base 53.20, k=128 99.62 vs 95.29; Qwen7B k=128 80.08 vs 74.01 |
| Wanda alone (best of 8 sparsities) | within 2.4 pts of base; DT gains up to 53.2 pts from same scores |
| Forgetting (Llama 1B-8B, 6-task prior suite) | DT forward KL <= 0.05, accuracy within 1 pt of base; FFT KL 1.0-1.5, 1.3-3.1 pts below base; LoRA/MTH KL 0.4-1.3, up to 5.4 pts below |
| Update geometry (Llama8B, Qwen7B) | stable rank 66-93 (LoRA 1-2, MTH 410-650); spectrum drift within 1.4x of FFT (LoRA r=1 up to 84x); principal-weight overlap 0.43-0.46 vs FFT 0.41-0.46 (LoRA ~0.48-0.50, MTH 0.50) |
| SFT, Llama3B | MMLU-Pro 22.28 vs FFT 21.19; BBEH 11.39 vs 11.39 (1B BBEH: 5.65 vs 8.35) |
| SDFT, Qwen7B | ToolAlpaca 69.07 vs 68.04; Science 70.61 vs 71.20 |
| Hyperparameter robustness | within 1.6 pts (Llama8B) / 3.2 pts (Qwen7B) across $\eta$, lr, $\lambda$; 4x change in $\eta$ moves accuracy <= 0.8 / 1.7 pts |

MTH at 99.95% sparsity trains about as many parameters (0.05%) as DT deletes (0.035-0.046%) yet forgets far more, so edit count does not explain retention; the authors attribute it to deletion itself. The RLVR signature of Zhu et al. (low spectrum drift, sub-random principal-weight overlap) is reproduced by DT but not by LoRA or random sparse updates.

## Limitations

- Mostly <=8B dense models plus two 14B/30B runs; the "gap closes with scale" claim rests on a few backbones, and DT trails FFT by 6 points at Llama1B and 2.7 points at BBEH 1B.
- Retention measured only under GRPO on Llama (three scales, one prior-task suite, forward-KL as predictor); no sequential multi-task continual-learning run is reported, despite the continual-learning framing.
- Only the gate projection is masked; no ablation of other targets in the capture's main text. Validation accuracy is the best checkpoint (selection on the validation set), single reported runs, no seed variance.
- Pass@k gain at k=128 is 4-6 points: real but modest; no analysis of which problems become solvable. Training cost (one logit per gate weight plus soft-mask forward) is not compared with LoRA. No released code.
- The "deletion as regularizer" explanation for matching FFT is the authors' hypothesis, not tested.

## Thesis relevance

- Strong data point for the R_w-primitive view in [[research/selective-finetuning/_overview]]: localized, extremely sparse edits suffice for RLVR gains, consistent with [[research/rlvr-mechanics/rl-sparse-subnetwork]] and [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] (RL updates sparse and selection-like). DT turns that observation into a trainable, tiny, swappable adapter.
- Forgetting: supports the on-policy / low-forward-KL side of [[conflicts/on-policy-forgetting-vs-lr-confound]] in the sense that forward KL predicts forgetting, and shows a parametrization (deletion) that lowers it further under the same on-policy GRPO rollouts. It does not vary rollout policy or learning rate, so it does not settle the confound; the DT learning rates ($3\times10^{-4}$ for the logits) are not comparable to FFT's $10^{-6}$.
- Candidate for single-sample / concept settings: a 1-8 MB mask per concept is a cheap per-concept adapter and composes by mask union or intersection (untested); pairs with [[research/selective-finetuning/skill-localization]] and [[research/selective-finetuning/pit]]. Unclear whether a mask learned from one sample overfits; no low-data experiment.
- Mild support for "RL = selecting existing behaviour": the update only removes pretrained weights, yet pass@128 still rises, a modest reach-extension signal next to [[research/rlvr-mechanics/what-outcome-rl-buys]].

## Source

- `raw/research/weekly-2026-11-13/04-deletion-tuning.md` (arXiv:2611.10866)

## Related

- [[research/selective-finetuning/_overview]]
- [[research/selective-finetuning/surgical-finetuning]]
- [[research/selective-finetuning/skill-localization]]
- [[research/selective-finetuning/pit]]
- [[research/selective-finetuning/o-lora]]
- [[research/selective-finetuning/dora]]
- [[research/selective-finetuning/packnet]]
- [[research/rlvr-mechanics/rl-sparse-subnetwork]]
- [[research/rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[research/rlvr-mechanics/what-outcome-rl-buys]]
- [[research/rlvr-mechanics/deepseekmath-grpo]]
- [[research/catastrophic-forgetting/_overview]]
- [[research/catastrophic-forgetting/rls-razor]]
- [[research/catastrophic-forgetting/rft-mitigates-forgetting]]
- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]]
- [[research/teacher-student-rl/opsd-compresses-rlvr]]
- [[research/synthesis/fine-tuning-best-practices]]
- [[conflicts/on-policy-forgetting-vs-lr-confound]]
- [[../weekly-briefs/2026-11-13]] — brought in by the 2026-11-13 weekly sweep
