# Deletion Tuning

NYU + U. Calgary (Lu, Yang, Lasby, Pote, Ioannou, Ren; arXiv 2611.10866, Nov 2026). Fine-tunes by learning only a binary keep/zero mask over the MLP gate projections of a frozen model. Fewer than 0.05% of weights are deleted, yet it matches full fine-tuning (FFT) under GRPO, SFT and self-distillation at 7B-30B, with a 0.5-30 MB adapter and less forgetting than FFT, LoRA or random sparse tuning. Results are from one paper and have no independent reproduction.

## Method

- One trainable logit `G` per pretrained weight of each block's gate projection (SwiGLU `down(SiLU(gate(x)) ⊙ up(x))`). Base frozen. For MoE (Qwen3-30B-A3B), each of the 128 experts' gate is masked; router untouched.
- Forward: `W ⊙ σ(α(t)·G)`, α ramped linearly 1e3 → 1e4 (mask sharpening). Eval and on-policy rollouts use the hard mask `1[G>0]`; soft vs hard differs by ≤0.08 pt.
- Init from Wanda scores (`|W|·‖X‖₂`), η = 1/2048, ~0.18% zeroed at init. Plus the MaskLLM sparse-weight regulariser (λ = 1e-5 for SFT/GRPO, 0 for SDFT). No sparsity target; training picks it.
- Relation to MaskLLM: same init and regulariser, but one deterministic logit per weight, no N:M pattern, and the goal is capability, not compression.
- Adapter = bit-packed mask, zstd-compressed (~0.03 bits per target weight): 1.0 MB at Llama1B, 8.4 MB at Llama8B. Task switching = scatter zeros into base weights.

## Results

- GRPO (Tables 1-2, best-checkpoint val acc): Llama8B GSM8K 83.55 vs FFT 83.24 (base 60.27); Qwen7B SimpleRL-Zoo 52.32 vs 51.89 (base 40.18); Qwen14B 55.43 vs 54.87; Qwen3-30B-A3B 58.54 vs 58.43. At 0.5B-3B it recovers 90-99% of FFT, so the gap closes with scale. FFT lr/KL tuning does not change this (App. H).
- Adapter size: 0.5 MB (Qwen0.5B) to 29.6 MB (30B-A3B) against 29-116 GB FFT checkpoints, 3,600-4,700× smaller. Smaller than LoRA r=1 and MTH at 99.95% sparsity.
- Pass@k (Table 3): leads base at every k; at k=128 it is +4.3 (Llama8B) and +6.1 (Qwen7B). The authors read this as new capability, not only sharpening. Sampling is 128 per problem at T=1.0.
- Learning the mask matters (Table 4): the best Wanda-only mask over 8 sparsity levels stays within 2.4 pts of base, while the trained mask gains up to 53.2 (Llama1B 1.21 → 54.44).
- Forgetting (Sec. 5.4): six-task prior suite (HellaSwag, MMLU, TruthfulQA, WinoGrande, IFEval, HumanEval). Deletion Tuning has forward KL ≤0.05 and accuracy within 1 pt of base. FFT's KL reaches 1.0-1.5 and it loses 1.3-3.1 pts. LoRA and MTH have KL 0.4-1.3 and lose up to 5.4 pts. MTH at 99.95% edits a comparable parameter fraction, so the retention is not explained by edit count alone.
- Update geometry (Fig. 3, Llama8B step 348, Qwen7B step 100): stable rank of ΔW 66-93 (LoRA 1-2, MTH 410-650); spectrum drift within 1.4× of FFT (LoRA r=1 up to 84×); principal-weight overlap 0.43-0.46 vs FFT 0.41-0.46 (random = 0.5). Sub-random overlap and low drift are the RLVR signature the paper cites from Zhu et al. (2026).
- SFT (MMLU-Pro, BBEH, 3B) and SDFT (ToolAlpaca, Science, Qwen7B) match FFT. Adapters are 600-4,700× smaller (Tables 5-6, not extracted here).

## Caveats

- Matching FFT is shown at the largest scale per regime only. Smaller backbones trail FFT.
- Training holds one logit per masked weight: less memory than FFT, more than LoRA.
- Only the gate projection is masked in all experiments. Other targets are untested.
- The "regularizer" explanation (deletion-only edits as implicit regularisation) is the authors' hypothesis, not tested.
- Continual learning over task sequences, mask union for skill merging, and N:M or block masks are listed as future work, not shown.
- Numbers come from the paper's text and tables. I did not check them against the released code.

## Source

- `raw/research/weekly-2026-11-14/01-deletion-tuning.md` (arXiv 2611.10866; code: agentic-learning-ai-lab/deleting-weights; project page agenticlearning.ai/deleting-weights)

## Related

- [[reasonmaxxer]] — RL changes few token positions and fits in a low-rank LoRA; this paper gives a weight-space counterpart (a few deleted weights suffice)
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — debate on sparse RL updates; this adds weight-space sparsity evidence
- [[macaron-v1]] — LoRA adapter family; compare adapter size and switching cost
- [[anti-self-distillation]] — SDFT-style on-policy self-distillation is one of the three regimes tested
