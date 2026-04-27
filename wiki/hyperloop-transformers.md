# Hyperloop Transformers

MIT (arXiv:2604.21254). Hyper-Connected Looped Transformers combine middle-cycle looped Transformers with **loop-level** hyper-connections. Beats depth-matched standard Transformers on FineWeb-Edu perplexity and downstream task accuracy at three scales while using ~50% fewer parameters. Direct, simplified extension of [[manifold-constrained-hyper-connections]].

## Method

Partitions a Transformer into begin / middle / end blocks (middle-cycle strategy from Bae et al. 2025); only the middle block is looped (×3 default). After each loop, manifold-constrained hyper-connections (mHC; Xie et al. 2026) are applied to the outer parallel residual stream — but at **inter-loop granularity**, not per-layer.

Key simplification over mHC: replaces the Sinkhorn doubly-stochastic transition matrix `H_res` with a **data-dependent diagonal** (sigmoid over a diagonal matrix). Cheaper than Sinkhorn-Knopp; matches or exceeds mHC perplexity at this granularity. Adds a per-loop position embedding `e_l` as the recurrent input signal. The design reads as a depth-wise RNN with matrix-valued hidden states.

Derives from: Universal Transformers (Dehghani 2018), ALBERT (Lan 2019), middle-cycle looping (Bae 2025, Saunshi 2025), and mHC (Zhu 2025a / Xie 2026).

## Results

FineWeb-Edu pretraining, three scales (Table 1). Looped model is ~50% the non-looped parameter count.

| Non-loop / Loop params | Tokens | PPL Transformer | PPL Hyperloop | Task Acc Transformer | Task Acc Hyperloop |
|---|---|---|---|---|---|
| 238M / 135.7M | 12.5B | 14.65 | **14.40** | 41.1% | **41.6%** |
| 990M / 580M | 50B | 10.19 | **9.65** | 48.0% | **49.8%** |
| 2018M / 991M | 100B | 8.60 | **8.49** | 52.8% | **54.6%** |

- Beats full-size Transformer in BF16 perplexity, INT4 GPTQ perplexity, and downstream task accuracy at all three scales.
- Overtrained 100B-token setting: Hyperloop 135.7M matches Transformer 238M (PPL 12.19 vs 12.15, Table 2).
- Throughput: 750K vs 786K tok/s at 136M scale (8×H100) — minimal slowdown vs vanilla looped Transformer.
- Requires GPTQ modification to estimate Hessian aggregated across loop iterations for INT4 quantization.

## Novelty

Refinement / recombination, not a new paradigm. The novel contribution is the **granularity** of hyper-connection application (loop boundaries, not per-layer) plus the **diagonal-sigmoid** parameterization for `H_res`. Together this closes the perplexity gap that vanilla looped Transformers had vs unlooped baselines (which hyper-connections alone did not close, per mHC results). Positions as a memory-constrained-deployment win: cloud, edge, on-device.

## Reproducibility

No code released as of capture. PyTorch + torch.compile, no custom kernels. No paperswithcode entry. Off-the-shelf hyperparameters work — no special tuning.

## Source

- `raw/research/weekly-2026-04-27/02-hyperloop-transformers.md` — arXiv:2604.21254.

## Related

- [[manifold-constrained-hyper-connections]] — direct predecessor; Hyperloop simplifies and re-applies mHC at loop granularity.
- [[test-time-training]] — looped Transformers as depth-wise RNNs share the "compute as variable depth" framing; logit-lens analysis suggests early-exit potential.
- [[watchlist]] — Universal Transformers (Dehghani 2018), ALBERT, middle-cycle looping (Bae 2025, Saunshi 2025), Geiping 2025, Prairie 2026.
