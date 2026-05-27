# GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers

GPTQ quantizes GPT-scale weight matrices to 3–4 bits in a single pass using approximate second-order (Hessian) information derived per transformer block, achieving near-lossless compression with negligible perplexity degradation. The method is a heavily optimized variant of Optimal Brain Surgeon (OBS) that scales to 175B-parameter models in under five hours on a single A100. It requires no architectural change, no training-time modification, and applies purely post-hoc to frozen weights.

## Method core

Layer-wise reconstruction objective: $\operatorname{argmin}_{\widehat{W}} \|WX - \widehat{W}X\|_2^2$ solved via an OBS-derived closed form. Three key modifications over the original OBQ algorithm:

1. **Arbitrary-order insight** — quantize all rows of $W$ in the same column order, reducing runtime from $O(d_\text{row} \cdot d_\text{col}^3)$ to $O(\max\{d_\text{row} \cdot d_\text{col}^2,\, d_\text{col}^3\})$.
2. **Lazy batch-updates** — accumulate column updates in blocks of $B=128$, then flush globally; turns a memory-bound loop into a compute-bound one.
3. **Cholesky reformulation** — precompute all needed rows of $H^{-1}$ via Cholesky instead of iterated Gaussian elimination, eliminating numerical blow-up at large scale.

Calibration uses 128 random 2048-token C4 segments; quantization grid is per-row asymmetric min-max. Blocks are processed sequentially; each block's inputs are re-derived from the already-quantized prefix so later blocks see realistic activations.

No weight-sharing, routing, or modularity mechanism. This is a post-hoc compression technique, not a training-time method.

## Goal relevance

- `background` — GPTQ operates on frozen weights after training; it does not bear on G1 (swappable blocks), G2 (dynamic per-block parameter allocation during training), or G3 (token-conditional routing). Relevant only as a compression step applicable *after* a modular model is trained, or as an example of block-granular processing of transformer weights.

## Credibility

- Venue / year: ICLR 2023
- Code released: Yes — https://github.com/IST-DASLab/gptq (PyTorch, CUDA kernel included)
- Weights released: No (quantized weights not distributed; reproducible from OPT/BLOOM checkpoints)
- Ablation rigor: **strong** — ablates arbitrary-order vs. greedy OBQ, small- vs. large-model regimes, grouping granularities (g1024, g128, g32, g8), 2/3/4-bit, ternary; runtime scaling measured empirically
- Replication status: Widely replicated; integrated into AutoGPTQ, llama.cpp, HuggingFace `transformers` quantization; considered a standard PTQ baseline as of 2024

## Empirical claims

- OPT-175B 4-bit: PPL 8.37 vs. FP16 8.34 (WikiText2); RTN at 4-bit gives 10.54
- OPT-175B 3-bit: PPL 8.68; RTN collapses to ~7300
- BLOOM-176B 4-bit: 8.21 vs. FP16 8.11; 3-bit: 8.64
- 3-bit OPT-175B fits on a single A100-80GB (vs. 5× A100 for FP16)
- Generation latency: 71 ms/token vs. 230 ms FP16 on A100 (3.24×); 130 ms vs. 589 ms on A6000 (4.53×, 8→2 GPUs)
- Quantization runtime: OPT-175B in 4.2 h, BLOOM-176B in 3.8 h on one A100; OPT-13B in 20.9 min
- 2-bit with g128 (≈2.2 bit effective): OPT-175B 9.58 PPL; ternary with g8: 9.20 PPL
- Load-bearing condition: speedup is memory-bandwidth-limited (matrix-vector regime, batch size 1); hardware lacks native FP16×INT4 multiply so no compute speedup for matrix-matrix products

## Open questions / failure modes

- Speedup is bandwidth-bound; batch size >1 erodes advantage as compute starts dominating
- Weights-only quantization — activations remain FP16; no activation quantization
- OPT-66B anomaly: harder to quantize, correlated with many dead units in early layers
- Numerical stability required Cholesky + dampening; may still fail on pathological weight distributions
- Grouping adds storage overhead (scale/zero-point per group); memory vs. accuracy tradeoff not fully characterized across model families
- No analysis of quantization bias effects (acknowledged in ethics statement)
- Does not address KV-cache quantization

## Source

- raw/research/block-training-quantization/19-gptq.md (PDF capture)
- raw/research/block-training-quantization/02-gptq-abs.md (arXiv abstract)

## Related

- [[brecq]] — block-reconstruction PTQ predecessor; GPTQ uses per-layer Hessian rounding, BRECQ uses Fisher-weighted output reconstruction at block granularity
- [[awq]] — activation-aware scaling alternative; complementary (AWQ scaling can precede GPTQ rounding)
- [[omniquant]] — extends GPTQ baseline with block-wise learnable clipping
- [[spinquant]] — applies learned rotations on top of GPTQ-style weight quant
- [[block-isolation-training]] — concept anchor; GPTQ's per-block sequential processing is structurally related but is post-training-only (no training-time isolation)
- [[llm-int8]] — predecessor W8A8 approach (Dettmers et al.)
- [[smoothquant]] — alternative PTQ via outlier migration
