---
title: "MoV / MoLORA: Extremely Parameter-Efficient MoE for Instruction Tuning"
authors: "Zadouri, Ahmadian, Üstün, Ermiş, Locatelli, Hooker"
year: 2023
institution: "Cohere for AI"
arXiv: "2309.05444"
tags: [moe, peft, lora, ia3, instruction-tuning, mixture-of-experts, parameter-efficiency]
theme: moe-adapters
---

# MoV / MoLORA: Extremely Parameter-Efficient MoE for Instruction Tuning

Zadouri et al. (Cohere for AI, 2023) show that plugging lightweight PEFT adapters as MoE experts into a frozen pretrained model yields a parameter-efficiency floor that was previously thought unattainable: <1% of an 11B model's parameters, yet on par with full fine-tuning on unseen tasks. The two instantiations — **Mixture of Vectors (MoV)** using (IA)$^3$ scaling vectors as experts, and **Mixture of LoRA (MoLORA)** using LoRA adapters as experts — become the canonical reference for "how cheap can MoE-adapter tuning get?"

## Source

- arXiv: [2309.05444](https://arxiv.org/abs/2309.05444)
- Raw capture: `raw/research/moe-adapters/04-02-mov-molora.md`

## Method

### PEFT primitives as experts

**(IA)$^3$** injects three learned rescaling vectors $l_k \in \mathbb{R}^{d_k}$, $l_v \in \mathbb{R}^{d_v}$, $l_{ff} \in \mathbb{R}^{d_{ff}}$ that element-wise rescale key/value activations in self-attention and intermediate activations in the FFN:

$$\text{softmax}\!\left(\frac{Q\,(l_k \odot K^\top)}{\sqrt{d_k}}\right)(l_v \odot V); \quad l_{ff} \odot \gamma(W_1 x)\,W_2$$

For a T5-3B, (IA)$^3$ updates only **0.018%** of total parameters — the smallest PEFT footprint in common use.

**LoRA** decomposes weight updates into low-rank matrices $B \in \mathbb{R}^{d_p \times r}$, $A \in \mathbb{R}^{r \times d_m}$:

$$h = W_0 x + \Delta W x = W_0 x + B A x$$

with rank $r \ll \min(d_m, d_p)$. At rank 4, T5-3B updates 0.3% of parameters — more flexible but costlier than (IA)$^3$.

### MoE routing over PEFT experts

A router $R$ with trainable weights $W_g \in \mathbb{R}^{d_m \times n}$ assigns soft scores over $n$ experts from a token representation $x$:

$$s_i = R(x)_i = \text{softmax}(W_g^\top x)_i$$

The **soft merging** output (key design choice — see Ablations):

$$E_{\text{mix}} = \sum_{i=1}^{n} s_i \cdot E_i, \qquad y = E_{\text{mix}}(x)$$

Because each expert $E_i$ is linear ((IA)$^3$ vectors or LoRA matrices), the weighted sum can be precomputed as a single merged adapter before applying it — no per-expert forward pass, no MoE memory overhead beyond one model copy plus $n$ tiny expert tensors.

**MoV** sets each $E_i$ to an (IA)$^3$ vector triple. **MoLORA** sets each $E_i$ to a LoRA $(A_i, B_i)$ pair. Pretrained weights stay frozen; only experts and router are trained from scratch.

## Claims

- **<1% parameters, full-FT parity.** MoV-10 updates **0.32%** of T5-3B (30 experts: 0.68%) and matches the fully fine-tuned T0-3B baseline (60.06 avg median) at 59.93 / 60.61.
- **Consistent outperformance over single-expert PEFT.** MoV-30 improves over (IA)$^3$ by **+14.57%** at 3B and **+8.39%** at 11B on 8 held-out tasks (zero-shot). MoLORA-15 improves over LoRA by **+5.70%** at 3B.
- **MoV > MoLORA at fixed parameter budget.** MoV-30 (0.68%) matches MoLORA-15 (4.69%) at 3B. The gap narrows at 770M where MoLORA-10 is preferred.
- **Soft merging > sparse routing.** Soft MoV-10: 59.93 avg; top-2 discrete: 57.45; top-1: 54.92. Adding load-balancing loss to top-2 further hurts (−1.5).
- **Token routing > sentence embedding routing.** Using frozen sentence-T5 embeddings as router input degrades performance by 0.94–8.86% vs token-level routing — task-level inductive bias is counterproductive; the router learns from hidden states directly.
- **Scales to 11B.** MoV-60 at 11B (0.86%) achieves performance competitive with full fine-tuning (<1.3% parameter updates). Expert specialization (distinct routing probabilities per task) generalises from seen to unseen tasks.
- **Training stability requires small batch.** Batch size ≥ 2048 causes expert collapse (convergence back to dense-PEFT level by 5k steps). Batch 32 + lr $3\times10^{-4}$ is the stable recipe.

## Strengths / Novelty

- First systematic study of MoE in an *extremely* parameter-efficient regime — prior MoE work assumed full FFN experts multiplying total parameter count.
- Soft merging of linear experts is a clean, zero-overhead inference trick: merge once, apply once.
- No prior task knowledge required for routing; generalises to zero-shot unseen tasks.
- Comprehensive ablation across model sizes (770M–11B), expert counts (1–60), routing strategies, and routing input types across 12 tasks / 55 datasets (P3).

## Weaknesses / Limits

- All experiments on T5 encoder-decoder (instruction tuning formulation); decoder-only LLM behaviour is unverified.
- Expert collapse under large batches and higher learning rates; recipe is sensitive to hyperparameters in ways that require careful tuning for new settings.
- Soft merging removes sparsity — inference cost equals a single dense expert, not a fraction of it. Conditional compute gains are traded away for stability.
- MoLORA's relative improvement over LoRA is smaller than MoV's over (IA)$^3$, presumably because the base LoRA already has higher expressive capacity; diminishing returns from mixture at higher per-expert cost.
- Expert interpretability is limited: routing probabilities are task-correlated but do not map to human-readable skills.

## Relevance to this wiki's project

MoV / MoLORA establish the **parameter-efficiency floor** for MoE-adapter methods. The directly relevant design parallels for MoERA:

1. **Delta-LoRA-as-expert.** MoERA's core primitive — replacing full FFN experts with $\Delta W = BA$ LoRA deltas — is structurally identical to MoLORA. MoV / MoLORA validate that this is sufficient for competitive performance at <1% cost, and that the mixture multiplies quality over a single adapter.
2. **Soft merging as default.** The ablation result that soft merging beats top-k routing in this regime is a strong prior for MoERA's routing design; sparse routing should be justified, not assumed.
3. **Scale of regime.** MoERA operates in a similar regime (dense → MoE via PEFT adapters, frozen backbone). MoV / MoLORA set the reference baseline that MoERA must beat or match to justify its added complexity.
4. **Weight $R_w$ in the synthesis.** The proposed-method's parameter-efficiency weighting term $R_w$ can be grounded against MoV / MoLORA's <1% figure as the lower anchor; anything above that should carry extra justification.

## Connections to the wiki

- [[_overview]] — theme entry point; MoV / MoLORA is the canonical lightweight-expert primitive
- [[loramoe]] — forgetting-focused sibling; same LoRA-expert idea but optimised for continual learning over task arithmetic
- [[self-moe]] — self-specialisation variant without external routing supervision
- [[btx]] — Branch-Train-MiX: upcycles task-specific FFN checkpoints vs MoV's from-scratch tiny experts
- [[sparse-upcycling]] — upcycles dense pretrained FFN into full MoE experts (opposite efficiency direction)
- [[mole]] — Mixture of LoRA Experts: another LoRA-as-expert instantiation, different routing
- [[moram]] — MoRA: rank-aware MoE adapter variant
- [[../selective-finetuning/dora]] — weight decomposition PEFT; MoV / MoLORA can be read as the mixture-of-PEFT cousin of DoRA's decomposed update
- [[../selective-finetuning/o-lora]] — orthogonal LoRA for sequential tasks; complementary to the MoV forgetting perspective
- [[../selective-finetuning/_overview]] — PEFT landscape context
- [[../synthesis/proposed-method]] — MoERA; $R_w$ parameter-efficiency anchor
- [[../catastrophic-forgetting/_overview]] — MoV / MoLORA's frozen backbone sidesteps forgetting; contrast with EWC-style approaches

## Related

- Fedus et al. 2022 — Switch Transformer (standard MoE baseline)
- Liu et al. 2022 — (IA)$^3$ (MoV's expert primitive)
- Hu et al. 2021 — LoRA (MoLORA's expert primitive)
- Muqeeth et al. 2023 — soft merging of fine-tuned models (precursor to soft-merge routing)
- Shen et al. 2023 — instruction tuning at scale stabilises MoE training
