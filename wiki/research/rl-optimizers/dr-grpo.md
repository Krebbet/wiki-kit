---
name: dr-grpo
description: Critical study of R1-Zero training; identifies GRPO length+std biases; Dr. GRPO fix
type: research
---

# Understanding R1-Zero-Like Training: A Critical Perspective (Dr. GRPO / SAIL)

Liu, Chen, Li, Qi, Pang, Du, Lee, Lin — Sea AI Lab / NUS / SMU, arXiv:2503.20783, COLM 2025. Critically examines the two pillars of R1-Zero-like training — base models and the GRPO optimizer — rather than treating replication results as face-value evidence of RL-driven reasoning emergence. The paper finds that (1) Qwen2.5 base models already exhibit strong reasoning and self-reflection without any prompt template, suggesting pretraining on concatenated QA text, and that (2) the standard GRPO objective contains two compounding biases that artificially inflate response length on incorrect rollouts. Removing both biases gives **Dr. GRPO** (GRPO Done Right), which recovers the unbiased PPO objective, improves token efficiency, and sets a new SOTA of 43.3% on AIME 2024 at 7B scale in 27 hours on 8×A100.

## Method

### GRPO biases

The standard GRPO objective (Shao et al., 2024) is:

$$J_\text{GRPO}(\pi_\theta) = \mathbb{E}\!\left[\frac{1}{G}\sum_{i=1}^G \frac{1}{|o_i|}\sum_{t=1}^{|o_i|} \min\!\left(\frac{\pi_\theta(o_{i,t}|q,o_{i,<t})}{\pi_{\theta^\text{old}}(o_{i,t}|q,o_{i,<t})}\hat{A}_{i,t},\; \text{clip}(\cdot, 1\pm\epsilon)\hat{A}_{i,t}\right)\right]$$

where $\hat{A}_{i,t} = \dfrac{R(q,o_i) - \text{mean}(\{R_1,\ldots,R_G\})}{\text{std}(\{R_1,\ldots,R_G\})}$.

This introduces two biases relative to the PPO objective (Eq. 2 in the paper):

1. **Response-level length bias** — dividing by $|o_i|$ means positive-advantage (correct) responses receive *larger* per-token gradients for shorter outputs (pushing the policy toward brevity on correct rollouts) while negative-advantage (incorrect) responses are penalised *less* per step for being long, so the policy learns to hedge with verbose wrong answers.

2. **Question-level std bias** — normalising by $\text{std}(\{R_1,\ldots,R_G\})$ reweights questions by their within-group reward variance. Easy or uniformly-failing questions (low std) are over-weighted; medium-difficulty questions are under-weighted. This is a per-question reweighting that is absent from the original PPO formulation.

The length bias was independently present in mainstream open-source PPO implementations (OpenRLHF, trl, verl) before GRPO was published: all normalize by response length (`mask.sum(axis=dim)`) rather than by a constant global token budget, causing the same drift (Table 2 of paper; Listing 1).

### Dr. GRPO: unbiased objective

Dr. GRPO removes both normalisation terms:

$$J_\text{Dr.GRPO}(\pi_\theta) = \mathbb{E}\!\left[\frac{1}{G}\sum_{i=1}^G \sum_{t=1}^{|o_i|} \min\!\left(\frac{\pi_\theta(o_{i,t}|q,o_{i,<t})}{\pi_{\theta^\text{old}}(o_{i,t}|q,o_{i,<t})}\tilde{A}_{i,t},\; \text{clip}(\cdot, 1\pm\epsilon)\tilde{A}_{i,t}\right)\right]$$

where $\tilde{A}_{i,t} = R(q,o_i) - \text{mean}(\{R(q,o_1),\ldots,R(q,o_G)\})$.

The implementation fix is replacing `mask.sum(axis=dim)` with a constant `MAX_TOKENS` in the masked-mean function. The paper shows (Appendix A) that $\tilde{A}_{i,t}$ equals the REINFORCE Leave-One-Out (RLOO) advantage up to a $G/(G-1)$ scaling absorbed into the learning rate.

### Base model findings

- **Qwen2.5-Math models are SFT-like at base**: 100% answering rate without any prompt template; best benchmark accuracy with no template (Table 1 — Qwen2.5-Math-7B: 38.2% avg with no template vs. 26.5% with Qwen-Math template, vs. 0.0% with R1 template). The paper hypothesises the models were pretrained on concatenated `q;o` text, making the base model already near-SFT for QA.
- **DeepSeek-V3-Base already exhibits Aha-moment keywords** (self-reflection tokens, "Aha", "wait") before any RL, consistent with prior blog-post claims (Liu et al., 2025b). Self-reflection frequency after R1-Zero RL does *not* positively correlate with higher accuracy (Sec. F).
- **Template–question-set interaction**: when base model capability already covers the template format (e.g., Qwen2.5-Math + Qwen-Math template), even a small OOD question set (GSM-8K) can nearly double downstream hard-benchmark accuracy — RL reinforces existing reasoning behaviours rather than infusing new knowledge.
- **Domain pretraining sets the RL ceiling**: continual pretraining Llama-3.2-3B on FineMath then NuminaQA before Dr. GRPO raises AIME 2024 from 0.0% to 6.7% and avg from 3.3% to 20.7% (Table 4). GRPO's "double-increase" length artefact on Llama models disappears with Dr. GRPO.

## Claims

- **SOTA at 7B / 27 h / 8×A100**: Oat-Zero-7B (Qwen2.5-Math-7B + Dr. GRPO, MATH level 3–5, Qwen-Math template) achieves 43.3% AIME 2024 / 62.7% AMC / 80.0% MATH500 / 30.1% Minerva / 41.0% OlympiadBench = **51.4% avg** — highest average among 7B models compared (Table 4 at 3k budget), beating SimpleRL-Zero-7B (46.6%), PRIME-Zero-7B (48.0%), and OpenReasoner-Zero-7B (43.0%).

| Model | AIME24 | MATH500 | Avg |
|---|---|---|---|
| Qwen2.5-Math-7B (no template) | 0.2 | 69.0 | 38.2 |
| SimpleRL-Zero-7B | 26.7 | 78.2 | 46.6 |
| PRIME-Zero-7B | 16.7 | 83.8 | 48.0 |
| OpenReasoner-Zero-7B @3k | 13.3 | 79.2 | 43.0 |
| **Oat-Zero-7B** | **43.3** | **80.0** | **51.4** |

- **Token efficiency**: Dr. GRPO cuts incorrect-response length substantially vs. GRPO across training (Figure 5, plot 4 — incorrect responses diverge to ~1800 tokens with GRPO vs. ~1000 with Dr. GRPO on Qwen2.5-1.5B). Correct-response length stabilises earlier under Dr. GRPO.
- **No performance regression**: at matched training steps, Dr. GRPO benchmark accuracy tracks GRPO or improves slightly (Figure 5, plot 5).
- **Oat-Zero-1.5B**: 20.0% AIME 2024 / 74.2% MATH500 / 42.1% avg — outperforms R1-Distill-Qwen-1.5B at 3k budget (22.0%) and nearly matches its 8k budget result (41.5%).

## Relevance to the project

Dr. GRPO's unbiased objective is the correct base for single-sample concept-learning experiments. The length bias becomes catastrophic when group size $G$ is small and most rollouts fail (all-zero reward group): std normalisation explodes near zero, and per-response length normalisation creates extreme gradient variance between the rare correct (short by bias) and the frequent incorrect (long by bias) rollouts — exactly the regime of low-$G$, curriculum-early training. Using Dr. GRPO (constant-budget masked mean, no std normalisation) is a prerequisite before interpreting length or self-reflection changes as genuine capability signals. Compare to [[dapo]]'s Token-Level Policy Gradient Loss, which arrives at the same correction (remove per-response length normalisation, clip by constant budget) from a different framing — DAPO focuses on the token-level gradient magnitude, Dr. GRPO motivates the fix via the biased-advantage derivation. Both converge on the same implementation fix.

## Source

- arXiv: https://arxiv.org/abs/2503.20783
- COLM 2025
- Code: https://github.com/sail-sg/understand-r1-zero
- Raw: `../../../raw/research/rl-optimizers/08-07-dr-grpo-liu.md`

## Related

- [[_overview]]
- [[../rlvr-mechanics/deepseekmath-grpo]] — original biased GRPO this paper corrects
- [[dapo]] — independent convergent fix: Token-Level Policy Gradient Loss
- [[../single-sample-rl-finetuning/deepseek-r1]] — R1-Zero setting this paper critically examines
- [[gspo]]
