# mHC — Manifold-Constrained Hyper-Connections

DeepSeek-AI (arXiv:2512.24880) proposes **mHC**, a stabilized variant of Hyper-Connections that projects the residual-mixing matrix onto the Birkhoff polytope (doubly stochastic matrices) via Sinkhorn-Knopp, restoring the identity-mapping property that vanilla HC breaks at scale.

## Method

A macro-architecture refinement of Hyper-Connections (Zhu et al. 2024). HC widens the residual stream by an expansion factor `n` and introduces three learnable mappings `H^pre, H^post, H^res` that read from, write to, and mix the n-stream residual. mHC adds three constraints:

1. `H^res` is constrained to a **doubly stochastic matrix** (rows and columns sum to 1, non-negative entries) by running 20 iterations of Sinkhorn-Knopp on `exp(H^res-tilde)` — the Birkhoff polytope.
2. `H^pre` is passed through sigmoid; `H^post` through 2-sigmoid — both forced non-negative to prevent sign cancellation.
3. Dynamic mappings are computed from a flattened-and-RMSNormed `vec(x_l)` projected by per-layer matrices `φ^{pre,post,res}`, plus learnable biases `b` and a learnable gating scalar `α` (init 0.01).

The doubly-stochastic constraint guarantees:
- Spectral norm ≤ 1 (non-expansive).
- Closure under matrix multiplication (composite mappings stay doubly stochastic across depth).
- Convex-combination / "convex hull of permutations" interpretation that monotonically mixes streams.

**Infrastructure side:**
- Kernel fusion via TileLang for the Sinkhorn-Knopp iteration and the `F^{post,res} := H^res x + H^post^T F(...)` merge.
- Selective recomputation with optimal block size `L_r* ~ √(nL/(n+2))` synchronized with pipeline-stage boundaries.
- Extended DualPipe schedule (from DeepSeek-V3) overlapping the n-stream cross-stage communication with computation; FFN `F^{post,res}` on a dedicated high-priority stream.

## Results

Trained on MoE backbones inspired by DeepSeek-V3 at 3B / 9B / 27B with proportional data, plus a 3B trained on 1T tokens, all with expansion rate `n=4`.

**27B downstream (Table 4)** — Baseline → HC → mHC absolute scores:

| Benchmark | Baseline | HC | mHC |
|---|---|---|---|
| BBH | 43.8 | 48.9 | **51.0** |
| DROP | 47.0 | 51.6 | **53.9** |
| GSM8K | 46.7 | 53.2 | **53.8** |
| HellaSwag | 73.7 | 74.3 | **74.7** |
| MATH | 22.0 | **26.4** | 26.0 |
| MMLU | 59.0 | 63.0 | **63.4** |
| PIQA | 78.5 | 79.9 | **80.5** |
| TriviaQA | 54.3 | 56.3 | **57.6** |

mHC beats baseline on all 8, beats HC on 7/8 (HC wins MATH by 0.4). vs HC: +2.1 on BBH, +2.3 on DROP.

**Stability (Figs. 2-3, 7):** HC shows a loss surge around step 12k on the 27B run with composite mapping Amax-Gain-Magnitude peaking near **3000**; mHC bounds it to **~1.6** — three orders of magnitude lower. Final loss reduction of mHC vs baseline at 27B: 0.021. Scaling curves (Fig. 6) show the mHC-vs-baseline loss-improvement gap is maintained from 3B → 9B → 27B with only marginal attenuation.

**System overhead:** only **6.7%** additional wall-clock time at `n=4`.

## Applicability

Direct fit for any team training large-scale dense or MoE Transformers from scratch and willing to modify the residual-stream plumbing. Prerequisites:
1. Substantial pre-training compute budget — gains are demonstrated and matter most at multi-billion-parameter scale where vanilla HC actually destabilizes.
2. Infra that can host fused custom kernels (TileLang or equivalent) and pipeline parallelism with a DualPipe-style schedule, otherwise the n-stream memory-access overhead eats the gains.
3. Tolerance for ~6.7% step-time overhead at `n=4`.

**Less useful for fine-tuning existing models or for small (<1B) training runs where vanilla HC is already stable.**

## Novelty

A constrained refinement of HC, not a wholly new connectivity paradigm. Closest prior: Hyper-Connections (Zhu 2024) — same n-stream architecture and per-layer learnable mappings; mHC's contribution is restricting `H^res` to the Birkhoff polytope via Sinkhorn-Knopp, plus the surrounding infra optimizations.

The doubly-stochastic / Sinkhorn-Knopp tool itself dates to Sinkhorn & Knopp 1967 and is widely used in optimal transport and attention; the novelty is using it to enforce identity-mapping conservation across depth in a residual architecture.

Sits in the same "expanded residual stream" branch as DenseFormer, MUDDFormer, Residual Matrix Transformer (RMT), LAuReL, DeepCrossAttention.

## Reproducibility

No code, no released weights, no paperswithcode entry. The paper provides full architectural specs (Appendix A.1: 3B/9B/27B configs, optimizer, LR, `n=4`, `t_max=20`, α init 0.01) and the kernel-fusion design at equation-level granularity. Reproducing the algorithm on a small model is straightforward; reproducing the large-scale stability + 6.7% overhead claim requires reimplementing the TileLang kernels, the recomputation scheme, and a DualPipe pipeline.

## Adoption

Brand-new from DeepSeek-AI (late 2025). Adoption signal so far is the DeepSeek byline — the team has the infra to ship this in a future DeepSeek-V4 / -R-class model. The cluster of 2024-2025 "wider residual stream" papers (HC, MUDDFormer, RMT, LAuReL, DeepCrossAttention) suggests an active subfield mHC is positioning within.

## Source

- `raw/research/radar-2026-04/06-mhc-deepseek.md` — mHC paper PDF (arXiv:2512.24880). Captured 2026-04-22.

## Related

- [[watchlist]] — Hyper-Connections (Zhu 2024), DeepSeek-V3, MUDDFormer, DenseFormer, RMT, LAuReL, DeepCrossAttention, TileLang, DualPipe referenced but not captured.
