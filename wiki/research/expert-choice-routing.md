# Expert Choice Routing

Expert Choice (EC) routing inverts the standard MoE token-to-expert assignment: each expert independently selects its top-k tokens from the batch rather than each token selecting its experts. This structural inversion guarantees perfect load balance without any auxiliary loss, enables heterogeneous (variable) compute allocation per token, and achieves >2× training convergence wall-clock speedup over Switch Transformer and GShard top-2 at comparable scale (NeurIPS 2022, Google).

## Routing mechanism

The routing signal is a learned linear projection W_g mapping each token hidden state to a score over all experts via softmax, producing an n×e score matrix S. Each expert independently takes its top-k tokens from S^T; the result is a soft gating matrix G of continuous weights. Expert outputs are weighted-summed back into the residual stream. W_g is trained end-to-end — load balance falls out of the structural top-k constraint, not from an auxiliary loss term.

A constrained variant, EC-CAP, caps the maximum number of experts any single token can attend via entropy-regularized LP (Dykstra's algorithm). EC-CAP2 (cap of 2) drops avg accuracy by ~0.8 points versus uncapped EC-CF2 at 100M/64E, confirming that variable per-token compute allocation is load-bearing, not cosmetic.

## Architecture context

EC replaces the dense FFN sub-layer in every other transformer layer (interleaved MoE/dense pattern, T5/GLaM lineage). Attention blocks are untouched. Non-MoE FFN layers use Gated Linear Units (GLU) in place of the standard linear+activation. Specialization operates at the FFN-block level, not attention.

## Specialization evidence

The paper argues learned affinity drives genuine expert specialization by contrasting against hash-layer routing: hash routing guarantees load balance by construction but scores 81.3 avg on GLUE/SuperGLUE (100M/64E) versus 84.0 for EC-CF2 — a 2.7-point gap attributable to learned vs. random assignment. The specialization claim is inferred from downstream performance gaps; the paper does not provide mechanistic inspection of what semantic content routes to which expert.

## Scale and benchmarks

- 100M expert-size family: 0.1B dense (130M params) up to 0.1B/128E (3.7B total, 145M activated). Pre-trained on GLaM 1.6T tokens, max seq 1024, Adafactor, 512 TPU V4 chips at 8B scale.
- 8B scale: dense 8B (8.7B params) vs. EC-CF2 8B/64E (143B total, 9.8B activated). EC-CF2 scores 92.6 avg on 11 GLUE/SuperGLUE tasks vs. 89.2 for dense 8B (+3.4 pts) and 90.3 for GShard top-2.
- Training convergence: EC-CF2 reaches GShard top-2 perplexity in <50% of steps; each EC step is ~20% faster than GShard top-2 (latter bottlenecked by load-imbalance step latency).
- Expert scaling: perplexity improves monotonically from 16 to 128 experts at fixed 100M expert size.

## Negative results / failure modes

1. **Hash routing gap** — load balance alone does not confer EC's gains; learned affinity is required (81.3 vs. 84.0 at 100M/64E).
2. **Capped variable routing** — EC-CAP2 underperforms uncapped EC-CF2 by ~0.8 points; heterogeneous per-token compute is load-bearing.
3. **Autoregressive incompatibility** — top-k selection over the full batch requires seeing all tokens simultaneously, including future tokens; EC does not straightforwardly apply to decoder-only generation.
4. **Inference batch degeneracy** — very small batch sizes destabilize expert selection; the paper proposes global top-k with per-expert/per-token caps as a partial mitigation.
5. **Perplexity/task misalignment** — the 100M/32E model outperforms 100M/64E and 100M/128E on fine-tuning tasks despite lower pre-training perplexity at higher expert counts; pre-training perplexity does not monotonically predict downstream performance.

## Open questions

1. How to adapt expert choice to autoregressive (decoder-only) generation without access to future tokens at dispatch time; batch-level grouping is proposed but not validated.
2. Handling very small inference batch sizes (proposed: global top-k with per-expert/per-token caps).
3. Memory footprint: total parameter count scales linearly with expert count, and hardware sparsity does not reduce static reservation — power-gating techniques flagged as future work.

## Source
- `raw/research/thesis-foundations/01-expert-choice-routing.md` — "Mixture-of-Experts with Expert Choice Routing", Zhou et al., NeurIPS 2022 (Google)

## Related
- [[mixture-of-depths]] — MoD adopts expert-choice routing to avoid load-balance aux losses; EC is the direct methodological parent.
- [[modular-deep-learning-survey]] — EC is a primary instantiation of the survey's "load balance structural, not incentivized" design point.
- [[mixture-of-cognitive-reasoners-micro]] — Both claim learned routing produces genuine specialization; MICRO extends scope from FFN-only to full blocks.
- [[mamba-2-and-ssm-hybrids]] — Both study block specialization via non-uniform compute — within-layer (EC) vs. cross-layer (SSM hybrid).
- [[routing-mechanisms-in-modular-networks]] — this page is a source for the routing taxonomy aux page.
- [[learned-routing-specialization]] (open conflict) — EC's specialization claim is inferred from performance gap; other sources contest whether learned routing reliably specializes.
