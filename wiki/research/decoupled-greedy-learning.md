# Decoupled Greedy Learning of CNNs

**CNN paper (ImageNet/CIFAR only).** DGL trains each module (layer or multi-layer block) of a CNN with an independent local auxiliary loss, eliminating all backward dependency on downstream blocks. Each module receives activations from its predecessor but no gradient from its successor; a lightweight auxiliary head (≤5% of primary module FLOPs, spatial-average pooling + MLP) maps the block's output to label space via cross-entropy. Two execution modes are provided: synchronous parallel updates and an asynchronous variant with a per-block LIFO replay buffer that tolerates hardware speed mismatch between modules. DGL reaches backprop parity on CIFAR-10 and near-parity on ImageNet (VGG-19, ResNet-152), while fitting 38% more samples into a 16 GB GPU and running 5–18% faster than [[ddg]] on 4 GPUs. It is the clearest published existence proof that local-loss block training converges at scale.

## Method core

Each module $j$ solves its own sub-problem independently:

$$\min_{\theta_j,\, \gamma_j}\; \hat{\mathcal{L}}(\boldsymbol{X}_j, Y;\, \theta_j, \gamma_j) \qquad (P_j)$$

where $\theta_j$ are the module's weights and $\gamma_j$ are the auxiliary head parameters. No gradient flows across module boundaries in either direction.

**Sync-DGL (Alg. 1):** all modules update in parallel each mini-batch — achieves *update unlocking*. Every module sees the same mini-batch; predecessor activations are detached before being passed forward.

**Async-DGL with replay (Alg. 2):** each module $j$ draws mini-batches from a LIFO buffer $B_{j-1}$ populated by module $j{-}1$, enabling *forward unlocking*. Robust to up to ${\sim}1.2\times$ speed mismatch between adjacent modules with negligible accuracy loss; buffer size as small as $M=1$ incurs only small degradation.

**Convergence (Corollary 3.1):** Under L-smoothness and Robbins-Monro step-size conditions, the per-module convergence rate recovers the standard non-convex SGD rate up to a multiplicative factor governed by $\sqrt{c_{j-1}^t}$, where $c_{j-1}^t$ is the TV distance between module $j{-}1$'s current output distribution and its converged distribution. The theoretical guarantee requires $\sum_t c_{j-1}^t < \infty$ — i.e., predecessors must themselves converge.

## Goal relevance

**G1 (isolated-block training) — directly relevant.** DGL is the cleanest existence proof that a block can be trained to convergence with only a local auxiliary loss. The auxiliary-head design pattern (detach activations, attach lightweight classification head, optimise independently) transfers directly to the transformer-block isolation problem.

**CNN-to-transformer gap is non-trivial.** DGL's auxiliary head exploits CNN spatial structure via spatial average pooling. Transformers have no spatial grid; the analogous operation — CLS-token projection or mean-pool over sequence positions — has not been validated in this framework. More critically, self-attention within a block computes global interactions across positions, so the information available at a block's output boundary differs structurally from a conv layer's output. Whether a local loss on that output remains a sufficient training signal for the attention weights is an open empirical question.

**G2 (dynamic per-block params) and G3 (token routing):** not addressed.

## Credibility

- **Venue / year:** ICML 2020 (PMLR 108)
- **Code:** released with submission; no public repo URL in captured PDF
- **Weights:** not released
- **Ablation rigor: strong** — auxiliary head design (CNN-aux vs MLP-aux vs MLP-SR-aux, Table 1), sequential vs parallel training curves (Fig. 3–4), async delay sweep over 10 slowdown values × all layers × 3 seeds (Fig. 5), buffer-size sweep (Fig. 6), head-to-head against [[dni]] / cDNI / [[ddg]] / backprop
- **Replication:** DDG comparison uses DDG's own parallel implementation; reported numbers match DDG's published results closely

## Empirical claims

- CIFAR-10, ResNet-110 $K{=}2$: DGL $93.5 \pm 0.1$ vs backprop $93.53$ — parity; large margin over [[dni]]/cDNI
- ImageNet, VGG-19 $K{=}4$: DGL top-1 $69.2$ vs backprop $69.7$; ResNet-152 $K{=}2$: DGL $74.5$ vs backprop $74.4$ — parity at scale
- VGG-13 layer-wise ($K{=}10$, zero backward communication): $64.4$ top-1 on ImageNet — degraded but functional, setting a lower bound on how far full isolation can be pushed in CNNs
- Memory: ResNet-152 DGL $K{=}2$ fits 38% more samples on 16 GB GPU vs standard backprop
- Wall-clock speedup vs [[ddg]]: 5% ($K{=}2$), 18% ($K{=}4$) on 4 GPUs

## Open questions / failure modes

- **No transformer experiments.** All results are CNNs (VGG, ResNet). The CNN-to-transformer gap for local-loss training is uncharted.
- **Auxiliary head design for sequence models is unsolved.** Spatial averaging exploits CNN structure. For transformers, candidate operations (CLS-token projection, sequence mean-pool) may provide weaker or noisier training signal, particularly in early layers before meaningful token structure emerges.
- **Non-stationary input distribution.** Sequential greedy (fully converge each block before the next starts) slightly outperforms Sync-DGL early in training (Fig. 3); the gap closes but hints that upstream distribution shift is a live concern in low-epoch or small-model regimes.
- **Depth scaling unknown.** No ablation beyond $K{=}10$ for CNNs. The convergence guarantee requires $\sum_t c_{j-1}^t < \infty$ — how tight this bound is for very deep decoupled stacks, or for architectures with skip connections that span block boundaries, is not characterised.
- **Representation interchangeability not studied.** No analysis of whether locally-trained blocks are composable or swappable after training — the question central to G1 in this wiki.

## Source

- `raw/research/block-training-quantization/24-dgl.md` (PDF capture)
- `raw/research/block-training-quantization/11-dgl-abs.md` (arXiv abstract)

## Related

- [[greedy-infomax]] — sibling decoupled-learning method; gradient-isolated representation learning via mutual-information local objective
- [[block-isolation-training]] — concept anchor; DGL is the clearest existence proof that local-loss training to convergence works
- [[dni]] — Decoupled Neural Interfaces; primary foil and precursor to the update/forward/backward locking taxonomy
- [[ddg]] — Decoupled Deep Greedy; backward-unlocking baseline DGL compares against directly
- [[predsim]] — Sim+Pred local loss baseline; concurrent work equivalent to a specific Sync-DGL instantiation but cannot scale to ImageNet
