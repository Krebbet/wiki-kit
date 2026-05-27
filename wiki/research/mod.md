# Mixture-of-Depths: Dynamically allocating compute in transformer-based language models

**Authors:** David Raposo, Sam Ritter, Blake Richards, Timothy Lillicrap, Peter Conway Humphreys, Adam Santoro (Google DeepMind / McGill & Mila). *Equal contribution: Raposo & Santoro.*

**Venue:** arXiv 2404.02258, 2024.

MoD replaces uniform per-token compute in a vanilla transformer with a learned, per-layer routing decision: at each designated routing layer a lightweight scalar router selects the top-$k$ tokens to pass through the full self-attention + MLP block; all other tokens bypass via the residual path at zero additional cost. This is the **primary citation** for the [[token-conditional-routing]] concept page — MoD's expert-choice top-$k$ depth routing is the concrete mechanism that concept page foregrounds.

## Method core

Given token embeddings $\{x_i^l\}_{i=1}^{T}$ at layer $l$, each token receives a scalar router weight:

$$r_i^l = x_i^l \cdot \mathbf{w}^l$$

where $\mathbf{w}^l \in \mathbb{R}^d$ is a learned linear projection. Let $\beta = 1 - k/T$ and $P_\beta(R^l)$ be the $\beta$-th percentile of all router weights $R^l = \{r_i^l\}$. The block output is:

$$x_i^{l+1} = \begin{cases} r_i^l \cdot f_i(\tilde{X}^l) + x_i^l, & \text{if } r_i^l > P_\beta(R^l) \\ x_i^l, & \text{if } r_i^l \leq P_\beta(R^l) \end{cases}$$

where $\tilde{X}^l = \{x_j^l : r_j^l > P_\beta(R^l)\}$ is the set of top-$k$ tokens and $f_i(\tilde{X}^l)$ is the standard transformer block (multi-head self-attention over $\tilde{X}^l$, then MLP). The router weight $r_i^l$ sits on the gradient path for routed tokens, making the scheme end-to-end differentiable.

Key design properties:

- **Expert-choice routing.** Each block selects the top-$k$ tokens (rather than tokens choosing paths), guaranteeing exactly $k$ tokens processed per block and trivially enforcing load balance with no auxiliary load-balancing loss.
- **Static computation graph.** $k$ is fixed a priori — known tensor sizes, no dynamic shapes.
- **Two-path routing.** One path is the full block; the other is the residual (zero additional FLOPs). No auxiliary expert capacity beyond the residual.
- **Routing scope.** Top-$k$ tokens form both queries and the available keys/values. Tokens not selected at layer $l$ are invisible as keys to other tokens at that layer.
- **Joint end-to-end training.** Router and model weights trained jointly from scratch on the language modeling objective.

**Inference challenge.** The top-$k$ operation is non-causal: selection at token $i$ depends on router weights from future tokens unavailable during autoregressive decoding. Two tested solutions:

1. **Auxiliary router loss** — binary cross-entropy on router logits with top-$k$ selections as targets; centers sigmoid outputs around 0.5; costs ~0.2–0.3% in LM loss; enables direct threshold inference ($r_i^l > 0.5$ → route to block).
2. **Auxiliary predictor MLP** — a second small router (stop-gradient inputs) predicts top-$k$ membership; no impact on LM loss; minimal step-speed overhead; ~99% accuracy early in training.

Preferred solution: auxiliary predictor MLP when LM loss purity matters.

## Goal relevance

**G3 — PRIMARY.** MoD is the closest published instantiation of the G3 experiment. Tokens are dynamically routed per-layer to either receive the full block transformation or pass through unchanged, varying effective depth per token. Key G3 parallels: per-token routing, skip-or-process binary choice, block-level granularity, joint training. The G3 page should anchor on MoD as the reference implementation.

**G1 — NOT applicable.** Routing and block weights train jointly; no isolated block training or post-hoc block replacement.

**G2 — PARTIAL.** Capacity $k$ is a fixed design hyperparameter, not a learned variable. The *pattern* of which tokens fill the $k$ slots is learned dynamically; $k$ itself is not.

## Credibility

Primary literature (arXiv preprint, Google DeepMind). Systematic isoFLOP analysis across three compute budgets (6e18, 2e19, 1e20 FLOPs) and model scales 60M–3B parameters. No peer-review record at time of ingest but consistent with DeepMind experimental standards. MoDE composability results are preliminary (limited sweep).

## Empirical claims

- Best configuration: interleaved routing (every other block is a routing block), capacity $k/T = 12.5\%$ (87.5% bypass per routing block).
- Stochastic routing (Gaussian-sampled weights) fails badly — learned routing is load-bearing.
- Optimal MoD models are *larger* than isoFLOP-optimal baselines (more parameters, fewer FLOPs per forward pass per parameter).
- MoD variants exist that match or beat the isoFLOP-optimal baseline in loss while being up to ~50% faster per step and equivalent in wall-clock training time.
- Routing behavior: tokens with higher-entropy (harder) predictions tend to route through more blocks; some tokens engage nearly every block, others bypass aggressively.
- **MoDE (Mixture-of-Depths-and-Experts):** MoD + MoE compose cleanly. Staged MoDE (MoD routing precedes MoE per block) and integrated MoDE (no-op expert among MoE experts; single routing op) both outperform naive capacity reduction on MoE.

## Open questions / failure modes

1. **Train/inference distribution gap.** Top-$k$ is non-causal at training time; the inference fix (predictor or auxiliary loss) works empirically but gap may widen with longer contexts or unusual routing patterns. Downstream MoD adaptations should validate.
2. **$k$ transferability.** $k/T = 12.5\%$ is empirically optimal for 2048-token sequences at up to 1e20 FLOPs. Generalization to other sequence lengths, domains, or scales is not established.
3. **Interleaving requirement.** Pure routing (every block gated) degrades significantly. Any G3 adaptation must plan for interleaved routing blocks.
4. **Memory savings uncharacterized.** Smaller KV-cache footprint and reduced device topology are flagged as promising at larger scale but left to future work.
5. **MoDE results preliminary.** Integrated vs. staged tradeoffs not fully resolved.

## Source

- `raw/research/selective-replacement-and-training/18-mod.md` — PDF capture
- `raw/research/selective-replacement-and-training/13-mod-abs.md` — arXiv abstract

## Related

- [[token-conditional-routing]] — concept anchor; MoD is the primary citation
- [[layerskip]] — related but different routing primitive: layer dropout + shared early-exit head vs. per-layer per-token top-$k$; MoD allows non-monotonic depth paths whereas LayerSkip exits monotonically
- [[calm]] — concurrent / complementary: per-token confidence-based early exit (monotonic) vs. MoD's arbitrary per-layer skip pattern
- [[sparse-upcycling]] — alternative routing primitive: FFN-experts instead of depth
- [[btx]] — alternative routing primitive: FFN-experts post-hoc
- [[demix]] — alternative routing primitive: domain-conditional
- [[modular-deep-learning]] — survey context; MoD is conditional computation applied to depth allocation
- [[hash-routing]] — queued; alternative routing primitive
