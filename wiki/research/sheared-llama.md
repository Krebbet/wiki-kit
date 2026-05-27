# Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning

Sheared LLaMA is the **canonical LLM-scale evidence for [[block-isolation-training]]**: it demonstrates that entire transformer layers (and sub-layer components — heads, FFN rows, hidden units) can be excised from a large pretrained model and the surviving blocks retrained back to competitive quality via continued pre-training on only ~50B tokens (~3% of the scratch-training compute). Starting from LLaMA2-7B, the method produces 1.3B and 2.7B models that outperform all same-scale scratch-trained baselines (Pythia, INCITE, OpenLLaMA, TinyLlama) on 11 downstream tasks and instruction-tuning evaluations. The two technical contributions are (1) **targeted structured pruning** via jointly learned hard-concrete mask variables subject to Lagrange-enforced shape constraints, and (2) **dynamic batch loading** that re-weights per-domain data proportions in real time based on per-domain loss gaps relative to a scaling-law reference.

## Method core

### Targeted structured pruning

Source model $\mathcal{M}^S$ has $L^S$ layers, hidden dim $d^S$, $H^S$ heads/layer, intermediate dim $m^S$. Four families of binary mask variables are introduced jointly:

| Granularity | Variable | Shape |
|---|---|---|
| Layer | $z^{\text{layer}}$ | $\mathbb{R}^{L^S}$ |
| Hidden dim | $z^{\text{hidden}}$ | $\mathbb{R}^{d^S}$ |
| Attention head (per-layer) | $z^{\text{head}}$ | $\mathbb{R}^{H^S \times L^S}$ |
| FFN intermediate (per-layer) | $z^{\text{int}}$ | $\mathbb{R}^{m^S \times L^S}$ |

Masks are parametrised as **hard-concrete distributions** (Louizos et al. 2018 $\ell_0$ regularisation), concentrating mass at 0 or 1 while remaining differentiable. Shape constraints are enforced via augmented Lagrange multipliers; for a single layer's head budget $H_\mathcal{T}$:

$$
\tilde{\mathcal{L}}^{\text{head}}(\lambda, \phi, z) = \lambda^{\text{head}} \cdot \left(\sum z^{\text{head}} - H_\mathcal{T}\right) + \phi^{\text{head}} \cdot \left(\sum z^{\text{head}} - H_\mathcal{T}\right)^2
$$

Analogous terms cover $z^{\text{int}}$ (per-layer), $z^{\text{layer}}$, and $z^{\text{hidden}}$ (global). The full pruning objective is $\min_{\theta,z} \max_{\lambda,\phi}\,\mathcal{L}_{\text{prune}}$:

$$
\mathcal{L}_{\text{prune}}(\theta, z, \lambda, \phi) = \mathcal{L}(\theta, z) + \sum_{j=1}^{L^S} \tilde{\mathcal{L}}_j^{\text{head}} + \sum_{j=1}^{L^S} \tilde{\mathcal{L}}_j^{\text{int}} + \tilde{\mathcal{L}}^{\text{layer}} + \tilde{\mathcal{L}}^{\text{hidden}}
$$

where $\mathcal{L}(\theta, z)$ is the masked-model language modelling loss. Weights $\theta$ and masks $z$ are optimised jointly. Pruning uses only **0.4B tokens**; target architectures are taken from known models (Pythia-1.4B, INCITE-Base-3B) to ensure uniform, hardware-friendly layer configs — in contrast to CoFiPruning's non-uniform head-count outputs.

### Dynamic batch loading

Per-domain **reference losses** $\ell^{\text{ref}}(D_i)$ are fit via Chinchilla-style scaling on the LLaMA2 model family (or the source model's own per-domain validation loss as a proxy). At each update step $t$, proportions update by exponential ascent on the per-domain loss gap $\Delta_t[i] = \max\{\ell_t[i] - \ell^{\text{ref}}[i],\, 0\}$:

$$
\alpha_t = w_{t-m} \cdot \exp(\Delta_t); \quad w_t = \frac{\alpha_t}{\sum_i \alpha_t[i]}
$$

Proportions are recomputed every $m$ steps with negligible overhead (no auxiliary proxy model). In practice C4 dominates the dynamic mixture (49.2% vs. 15.0% original); GitHub drops to 0.8%.

## Goal relevance

**G1 — STRONG. This is the canonical LLM-scale citation for [[block-isolation-training]].** The continued pre-training stage instantiates exactly the "heal after removal" dynamic G1 needs: entire layers are excised via mask collapse and the surviving blocks are retrained under standard LM loss. When a layer mask collapses to 0, every remaining layer must adapt to shifted neighbour activations — precisely the neighbour-distribution shift that block-isolation experiments will induce. The per-domain loss imbalance (GitHub overcorrects, C4 lags) is also a direct data-curriculum signal transferable to any selective-removal + recovery setup.

**G2 — WEAK/INDIRECT.** Per-component budgets (heads, FFN width, layer count) are solved once by the Lagrange-constrained mask search — a one-shot allocation, not dynamic per-token or per-step. Relevant as structured-allocation prior art but not dynamic in the G2 sense.

**G3 — NOT RELEVANT.**

## Credibility

Published at ICLR 2024. Rigorous ablations: budget sensitivity (Table 5), static vs. dynamic batch loading (Figure 5), target architecture choice. Open-source weights and code released. Main limitation: source model restricted to LLaMA2-7B; scalability to larger sources is asserted but not demonstrated.

## Empirical claims

- Sheared-LLaMA-1.3B (50B tokens) outperforms OPT-1.3B, Pythia-1.4B (300B tokens), and TinyLlama-1.1B (3T tokens) averaged over 11 tasks.
- Sheared-LLaMA-2.7B (50B tokens) outperforms INCITE-Base-3B (800B), OpenLLaMA-3B-v1 (1T), OpenLLaMA-3B-v2 (1T).
- Instruction-tuned variants achieve higher ShareGPT win-rates than all same-scale baselines.
- Budget ablation with 5B total tokens: doubling pruning budget 0.4B → 0.8B → 1.6B improves post-recovery PPL 7.32 → 7.23 → 7.08, but pruning's 5× per-step cost makes 0.4B the practical sweet spot.
- Dynamic batch loading provides consistent downstream gains over static RedPajama proportions.

## Open questions / failure modes

- Scalability beyond LLaMA2-7B source not demonstrated; mask search cost scales with source model size.
- Recovery training at 50B tokens appears not saturated (Figure 1 trajectories still declining); full gap vs. scratch-trained models at equal token count is uncharacterised.
- Dynamic batch loading reference losses require either a family of source models (scaling-curve fit) or the source model itself as domain-loss proxy — neither is available in a true from-scratch setting, limiting applicability to the pruning-from-pretrained regime.
- No experiments on heterogeneous source/target operator types; mask search assumes the source architecture is a strict superset of the target.

## Source

- `raw/research/selective-replacement-and-training/23-sheared-llama.md` (PDF capture)
- `raw/research/selective-replacement-and-training/05-sheared-llama-abs.md` (arXiv abstract)

## Related

- [[shortgpt]] — predecessor in spirit (block-importance metric)
- [[sleb]] — training-free pruning sibling
- [[iterative-layer-distill]] — successor (iterative + distillation recovery)
- [[lottery-ticket-bert]] — sparse-subnet predecessor at BERT scale; Sheared LLaMA is the structured-LLM successor
- [[layerskip]] — alternative isolation pressure (skippable rather than prunable)
- [[block-isolation-training]] — concept anchor; this is the canonical LLM-scale evidence
- [[bert2bert]] — opposite direction (growth vs prune)
- [[modular-deep-learning]] — survey context
