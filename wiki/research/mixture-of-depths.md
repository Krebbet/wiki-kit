# Mixture of Depths

Raposo et al. (Google DeepMind, 2024) show that transformers can learn to route individual tokens around full self-attention+MLP blocks using a top-k expert-choice router, achieving equal or better loss than isoFLOP-optimal vanilla baselines while cutting per-forward-pass FLOPs by up to 50% and stepping up to 66% faster. The core insight is that not all tokens require equal computation at every layer; a learned scalar router per layer dynamically assigns each token to either the full block or a residual pass-through. Results hold consistently across 60M–3B parameters and three FLOP budgets (6e18, 6e19, 1e20).

## Routing mechanism

Each token embedding is projected to a scalar router weight `r_i = W · x_i` per layer. The top-k weights within the sequence select which tokens participate in the block (expert-choice routing); the rest skip via the residual connection.

Expert-choice (EC) routing is preferred over token-choice routing for two reasons: it eliminates load-balancing auxiliary losses, and it guarantees exactly k tokens participate per block — enabling static compute graphs. Capacity is set to 12.5% of sequence length in the best-performing configuration; capacities below this threshold degrade performance.

**Autoregressive sampling caveat.** Top-k selection is non-causal and cannot be applied naively at inference. Two mitigations are proposed:
1. A binary cross-entropy auxiliary loss centering router sigmoid around 0.5 — functional but costs ~0.2–0.3% on the LM objective.
2. A small auxiliary MLP predictor (stop-gradient) that learns to predict top-k membership causally without affecting the LM objective. This achieves >97% accuracy early in training and is the preferred approach.

## Block structure and compute savings

MoD defines two computation paths per layer: (1) standard transformer block (self-attention + MLP) and (2) residual pass-through (null computation). This is a within-layer conditional skip, not a sub-architecture replacement.

Best-performing configuration interleaves routing blocks with full-capacity blocks (every other block is a routing block). Routing every block degrades performance — full-capacity interleaved blocks are required.

A 220M-parameter MoD model slightly outperforms the isoFLOP-optimal 220M vanilla baseline while stepping ~66% faster. Wall-clock training time is approximately equal. The isoFLOP optimality holds at all three tested FLOP budgets, indicating consistent scaling behavior.

## Specialization evidence

Routing analysis (Figure 5 of the paper) reveals non-trivial token-level specialization:
- Some tokens consistently engage every block; others route around blocks whenever possible.
- Tokens routed through more blocks correlate with higher-entropy predictions (harder predictions).

This is genuine conditional routing specialization, not ensemble averaging. However, stochastic (random) routing — using Gaussian-sampled weights as a control — fails badly, performing significantly worse than the vanilla baseline at equivalent FLOPs. Learned routing is necessary, not optional.

## Scale and benchmarks

| Axis | Range / Value |
|---|---|
| Model size | 60M – 3B parameters |
| Training FLOPs | 6e18, 2e19, 1e20 |
| Sequence length | 2048 |
| Batch size | 128 |
| Hardware | TPUs |
| Eval set | 256,000 sequences (500M tokens) |

Autoregressive evaluation on held-out sequences confirms training-time results generalize to inference. The isoFLOP-optimal MoD transformer uses the same FLOPs per forward pass as the isoFLOP-optimal baseline — there is no free-lunch lower-FLOP variant that is simultaneously isoFLOP-optimal.

**MoDE (MoD + MoE combined):** Integrating MoD with mixture-of-experts yields compounding gains over either alone. Integrated MoDE (no-op expert among MLP experts) outperforms staged MoDE and outperforms simply reducing MoE capacity.

## Negative results

- Stochastic routing (random router weights) fails badly vs. vanilla baseline at equivalent FLOPs — learned routing is non-negotiable.
- Routing every block degrades performance; interleaving with full-capacity blocks is required.
- Capacities below 12.5% of sequence length hurt performance.
- No free lunch: the isoFLOP-optimal MoD variant does not save FLOPs over the isoFLOP-optimal baseline; savings come from training a larger model at the same FLOP budget.
- Token-choice routing has load-balancing problems requiring auxiliary losses; avoided throughout.

## Open questions

- Whether decoupled routing for queries vs. keys vs. values within self-attention would improve performance (currently routing applies to full QKV participation).
- Whether tokens routed out of keys could be funnelled into a long-term memory buffer for future attention — proposed as a path to drastically longer effective context.
- How to extend MoD routing to heterogeneous computation types (e.g., "memory lookup", "tool use") rather than block vs. null.
- KV cache reduction during autoregressive sampling flagged as potentially significant but not studied.
- Overtraining (smaller model, more tokens) noted as still applicable on top of MoD gains — not explored.

## Source
- `raw/research/thesis-foundations/02-mixture-of-depths.md` — "Mixture-of-Depths: Dynamically allocating compute in transformer-based language models", Raposo et al., Google DeepMind, 2024.

## Related
- [[expert-choice-routing]] — MoD adopts EC routing; EC is the direct methodological parent.
- [[modular-deep-learning-survey]] — MoD is a concrete instance of the survey's hard routing / conditional-compute family.
- [[looped-transformers-and-reasoning]] — Both address adaptive depth: MoD routes tokens around blocks; Looped-Transformers repeat the same block.
- [[looped-language-models]] — Both implement conditional depth reduction with learned routers; both report naive routing fails.
- [[mamba-2-and-ssm-hybrids]] — Both show heterogeneous stacks beat homogeneous stacks, but via different mechanisms (fixed layer-type vs. per-token dynamic).
- [[routing-mechanisms-in-modular-networks]] — this page feeds the routing taxonomy aux.
- [[learned-routing-specialization]] (open conflict) — MoD's "harder predictions route through more blocks" cuts one way; other evidence cuts against learned-routing specialization.
