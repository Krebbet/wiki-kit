---
title: "Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints"
aliases: ["sparse-upcycling", "Sparse Upcycling"]
tags: [moe, upcycling, mixture-of-experts, initialization, dense-to-sparse, foundational]
arXiv: "2212.05055"
venue: "ICLR 2023"
authors: "Komatsuzaki et al."
year: 2023
depth: background-to-primary
theme: moe-adapters
---

# Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints

Komatsuzaki et al. (ICLR 2023) introduce **sparse upcycling**: a recipe for converting a pretrained dense Transformer checkpoint into a sparsely activated Mixture-of-Experts (MoE) model, recovering the dense model's quality and then exceeding it at a fraction of the original pretraining cost. This is the foundational "dense → MoE" initialization paper that BTX, Self-MoE, LoRAMoE, and their successors all descend from.

## Source

- arXiv: [2212.05055](https://arxiv.org/abs/2212.05055) — ICLR 2023
- Raw capture: `raw/research/moe-adapters/06-05-sparse-upcycling.md`

## Method

### Architecture surgery

Given a pretrained dense Transformer with $L$ layers, a subset of the MLP sublayers (default: $L/2$) are promoted to MoE layers. The remaining MLP, attention, layer-norm, and embedding layers are copied verbatim from the dense checkpoint.

**Expert initialization.** Each MoE layer contains $E$ experts (default $E=32$). Every expert is initialised as an **exact copy** of the dense MLP it replaces:

$$\theta_{e}^{(0)} = \theta_{\mathrm{MLP}}^{\mathrm{dense}}, \quad e = 1, \ldots, E$$

The router alone is randomly initialised; it has no dense counterpart. Formally, let $\mathbf{R} \in \mathbb{R}^{n \times E}$ be the routing matrix over $n$ tokens. Under Expert Choice routing, expert $e$ selects the top-$T$ tokens by column, where $T = C \cdot (n/E)$ and $C$ is a capacity factor (default $C=2$).

### Training continuation

After surgery, training resumes from the upcycled checkpoint using the **original hyperparameters**: same batch size, learning rate schedule (inverse-square-root), and weight decay. No new data is required. The additional compute budget is expressed as a fraction of the original dense pretraining cost.

### Design knobs

| Knob | Default | Effect |
|---|---|---|
| Fraction of MLP layers upcycled | $1/2$ | More → larger capacity drop initially |
| Number of experts $E$ | 32 | More → more params, larger initial drop |
| Capacity factor $C$ | 2 | Higher → more FLOPs, better quality per step |
| Router type | Expert Choice (encoder), Top-K $K=2$ (decoder) | Expert Choice outperforms Top-K on train-time basis |
| Optimizer state reuse | Vision only | Boosts vision; no benefit in language |

Optimizer state reuse for the dense model parameters (Adam moments) helps vision models recover faster; language experiments show no benefit and it is omitted.

## Claims

- **T5 Base, Large, XL upcycled models outperform their dense baselines on SuperGLUE** using only ~46–55% additional compute beyond the original dense pretraining cost.
- **ViT-B/16, B/32, L/16, L/32 upcycled models outperform their dense baselines on ImageNet (10-shot)** using as little as +13% additional compute relative to the dense checkpoint (vs. +58% required for dense continuation to match the same gain).
- **Upcycled models outperform MoE-from-scratch models** trained on 100% of the original dense computation budget. The MoE-from-scratch baseline requires ~120% of the original budget to catch up to the upcycled model on language tasks.
- **Expert initialization from the dense MLP is critical at low budgets.** Random expert initialization eventually matches standard upcycling given sufficient compute, but is strictly worse in the constrained-budget regime.
- **Sparse upcycling strictly dominates dense warm-starting** ("depth tiling" / dense upcycling) at every compute level tested.
- Gains are robust to the degree of convergence of the starting dense checkpoint: upcycling from partially trained checkpoints yields similar relative improvements.

## Strengths / Novelty

- **Zero wasted compute:** sunk pretraining cost is repurposed rather than discarded; the dense model acts as an MoE initialiser that already encodes rich representations.
- **Simple surgery:** the recipe requires no architectural changes beyond cloning MLP weights; no distillation, no curriculum, no new data.
- **Efficient capacity expansion:** adding $E$ experts multiplies parameter count by $\sim E/2$ (for half the layers upcycled) with minimal FLOPs increase — router computation is cheap, and Expert Choice routing keeps per-token compute nearly constant.
- **Demonstrated across modalities:** both T5 (encoder-decoder language) and ViT (encoder-only vision) benefit, suggesting the recipe is architecture-agnostic.
- **Practical entry point:** practitioners can train a dense model to saturation, then upcycle if they have residual compute budget — the method slots into existing training pipelines without redesign.

## Weaknesses / Limits

- **Data hunger persists:** sparse upcycling still requires continued pretraining on the full (masked-LM / span-corruption / contrastive) corpus; it does not eliminate the need for large-scale data.
- **Pre-LLM-scale experiments:** all benchmarks use T5 (up to XL, ~3B parameters) and ViT (up to L). Behaviour at GPT-3 / PaLM scale is not established in this paper.
- **Expert collapse risk:** all experts start identical; divergence depends entirely on the random router. The paper notes that adding Gaussian noise to expert copies has negligible benefit (and hurts if too large), but expert specialisation is not guaranteed at short continued-training budgets.
- **Routing discrepancy (language decoder):** Expert Choice routing cannot be used autoregressively; the decoder reverts to Top-K ($K=2$), creating an asymmetry not present in the encoder.
- **Compute regime dependency:** for budgets $> 100\%$ of the original dense cost, MoE-from-scratch eventually matches or exceeds upcycling. The method's advantage is specifically in the constrained-budget regime.
- **Not parameter-efficient:** the upcycled model stores $E$ full copies of each upcycled MLP, inflating total parameter count substantially. No adapter factorisation is applied.

## Relevance to this wiki's project

Sparse Upcycling is **the ancestor primitive of the MoERA family**. MoERA's core insight — reuse a trained dense checkpoint as the MoE initializer rather than training an MoE from scratch — is exactly what this paper establishes and validates empirically.

Where Sparse Upcycling copies the entire dense FFN into each expert ($\theta_e = \theta_{\mathrm{MLP}}$), MoERA replaces the full copy with a **shared frozen dense base plus a small expert-specific delta adapter** $\Delta_e$:

$$\theta_e = \theta_{\mathrm{MLP}} + \Delta_e, \quad \Delta_e \ll \theta_{\mathrm{MLP}}$$

This makes the parameter cost sublinear in $E$ and keeps the total added weight proportional to the adapter rank, which matters critically in the single-sample / low-resource regime targeted by this project. The $R_w$ regularisation term in the proposed method (see [[../synthesis/proposed-method]]) similarly reuses the dense FFN as a reference point — penalising expert weights from drifting far from the pretrained initialisation, exactly the intuition Sparse Upcycling validates empirically.

In short: Sparse Upcycling proves that dense-checkpoint initialisation is strictly superior to random MoE initialisation; the downstream MoERA literature then asks how to make that initialisation parameter-efficient.

## Connections to the wiki

- [[_overview]] — situates upcycling within the MoE-adapter theme
- [[../synthesis/proposed-method]] — $R_w$ regulariser is a delta-adapter generalisation of the upcycling init
- [[../selective-finetuning/_overview]] — sparse upcycling selectively replaces only MLP sublayers; connects to selective-layer finetuning intuitions
- [[../catastrophic-forgetting/_overview]] — identical expert initialisation is a form of anchor regularisation against forgetting the dense model's representations

## Related

Within this theme (direct descendants):

- [[btx]] — BTX ("Branch-Train-MiX") upcycles via parallel expert branches, a direct architectural successor
- [[self-moe]] — Self-MoE assembles LoRA-expert MoEs from a dense base, the parameter-efficient fork of upcycling
- [[loramoe]] — LoRAMoE inserts LoRA experts alongside frozen dense FFNs, combining upcycling with PEFT
- [[mov-molora]] — MoV / MoLoRA explore vector/LoRA gating from the same initialisation philosophy
- [[mole]] — MoLE applies upcycling-style init to LoRA ensembles
- [[moram]] — MoRAM adds rank-adaptive experts to the upcycled MoE framework
