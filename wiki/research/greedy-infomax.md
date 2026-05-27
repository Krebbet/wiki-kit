# Putting An End to End-to-End: Gradient-Isolated Learning of Representations (Greedy InfoMax)

Greedy InfoMax (GIM; Löwe et al., NeurIPS 2019) trains a stack of gradient-isolated CNN modules — each optimised with a local InfoNCE contrastive objective — achieving competitive self-supervised representations on STL-10 (vision) and LibriSpeech (audio) **without any cross-module backpropagation**. This is **representation learning**, not autoregressive generation: the trained encoders are evaluated via linear probe, not next-token prediction. The gradient-blocking + local-loss pattern is the direct architectural ancestor of isolated-module training, but the applicability gap to transformer-based autoregressive generation is real and non-trivial (see Goal relevance below).

## Method core

A deep network is partitioned by depth into $M$ gradient-isolated modules. Forward activations pass freely; backward gradients do not — enforced via a `GradientBlock` operator:

$$\nabla\,\text{GradientBlock}(x) \triangleq 0$$

Each encoding module $g^m_\text{enc}$ is optimised with a module-local InfoNCE loss contrasting future patch representations against in-batch negatives:

$$\mathcal{L}_N^m = -\sum_k \mathbb{E}\!\left[\log \frac{f_k^m(z^m_{t+k},\, z^m_t)}{\sum_{z^m_j \in X} f_k^m(z^m_j,\, z^m_t)}\right], \quad f_k^m(z^m_{t+k}, z^m_t) = \exp\!\left(z^{m\top}_{t+k}\, W^m_k\, z^m_t\right)$$

The scoring matrices $W^m_k$ and the encoder $g^m_\text{enc}$ are trained jointly per module; $W^m_k$ is discarded after training. Modules may be trained **simultaneously** (all in memory, all updated each step) or **iteratively** (freeze-and-cache lower modules before training higher ones). An optional autoregressive module $g^M_\text{ar}$ (GRU or PixelCNN) can be appended with its own isolated loss for tasks requiring broad temporal context — though this reintroduces sequential BPTT within that module.

## Goal relevance

**G1 — direct ancestor.** GIM is the clearest prior art for "train an isolated transformer block." It establishes: (a) gradient-stopping as the isolation primitive, (b) a local contrastive loss as a substitute for end-to-end gradient signal, and (c) simultaneous vs. iterative training as a design axis with measurable quality tradeoffs.

**Applicability gap.** The experimental setting differs from isolated transformer block training along two critical axes:

1. *Architecture*: all GIM experiments use ResNet-50 (vision) or 1-D convolutional stacks (audio). CNNs have local receptive fields; transformer attention layers aggregate global context within each block. The gradient-stopping primitive transfers, but whether local InfoNCE provides sufficient credit signal to a self-attention block — which must learn both QKV projections and multi-head routing — is untested.
2. *Task*: GIM trains for representation quality measured by linear probe. Autoregressive generation requires the stack to preserve and propagate precise token-level state across modules; a contrastive local objective that discards $W^m_k$ post-training provides no mechanism for this. A generation-compatible local loss (e.g., distillation from a teacher, causal LM loss on local outputs) would be needed, and its interaction with gradient isolation is an open question.

**G2 — background.** No dynamic parameter allocation; module capacity is fixed at partition time.

**G3 — background.** No token-conditional routing; all tokens traverse the same module stack.

## Credibility

- **Venue / year:** NeurIPS 2019
- **Code:** released — https://github.com/loeweX/Greedy_InfoMax
- **Weights:** not released
- **Ablation rigor:** partial — ablates simultaneous vs. iterative training and BPTT removal; no ablation on number of modules or partition granularity
- **Replication:** [[cpc]] baseline reproduced from Oord et al. 2018 within the paper

## Empirical claims

- **STL-10 linear probe:** GIM 81.9 ± 0.3% vs. CPC (end-to-end) 80.5 ± 3.1% — greedy training outperforms end-to-end despite no cross-module gradients.
- **Iterative variant:** drops to 79.8%; attributed to overfitting when lower modules no longer supply noisy upstream signal during upper-module training.
- **GPU memory:** simultaneous training peaks at 7.0 GB (ResNet-50); iterative (one module at a time) peaks at 2.5 GB — a 2.8× reduction.
- **LibriSpeech speaker classification:** GIM 99.4% ≈ CPC 99.6% (both exceed supervised 98.9%).
- **LibriSpeech phone classification:** GIM 62.5% < CPC 64.9% < supervised 77.7% — gap persists without autoregressive context; long-range phonetic dependencies are not captured by local InfoNCE alone.
- **Intermediate-layer probing:** each GIM module monotonically improves on its predecessor; InfoNCE "stacks well" greedily.

## Open questions / failure modes

- Local objective shown only for contrastive (InfoNCE) losses; whether reconstruction or distillation losses are competitive without end-to-end gradients is untested.
- Iterative training induces overfitting in higher modules; simultaneous training is preferred but requires all modules resident in memory simultaneously.
- Tasks requiring long-range context (phone classification) show a meaningful gap vs. end-to-end CPC; the autoregressive $g^M_\text{ar}$ module restores some performance but reintroduces BPTT, undermining isolation.
- Partition granularity (number of modules, depth of each cut) is not ablated — no guidance on optimal split for deep networks, let alone transformer stacks.
- All experiments on CNNs; direct evidence on transformer blocks is absent. The attention mechanism's global mixing may be incompatible with purely local credit signals.
- Scoring functions $W^m_k$ are discarded post-training — no reuse, transfer, or composition of module-level knowledge.

## Source

- `raw/research/block-training-quantization/13-gim.md` (PDF capture)
- `raw/research/block-training-quantization/12-gim-abs.md` (arXiv abstract)

## Related

- [[decoupled-greedy-learning]] — sibling decoupled-learning method
- [[block-isolation-training]] — concept anchor; GIM is a foundational ancestor of "isolated module training"
- [[cpc]] — CPC baseline reproduced from Oord et al. 2018; GIM is a gradient-isolated variant of CPC with identical local loss form
- [[predsim]] — concurrent Sim+Pred local loss alternative; outperformed by GIM on STL-10
- [[dni]] — Decoupled Neural Interfaces context; same asynchronous-training motivation but predicts gradients rather than blocking them
