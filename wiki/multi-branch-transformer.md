# Multi-Branch Transformer (MBT)

UIUC/Rice/Michigan/Cornell architecture: full Transformer blocks run in parallel branches between shared prelude/coda layers. Claims 1.16-1.26x training-compute-equivalent quality, 19-34% less KV cache (via Joint-KV) and up to 51.4% higher decode throughput than a standard MoE Transformer at matched FLOPs. arXiv 2611.19800.

## Method
- Layout: shared prelude P -> K>=2 independently parameterised branch stacks G_i -> fusion F -> shared coda C. Blocks: pre-RMSNorm GQA attention + latent MoE (64 SwiGLU experts, top-8, Quantile Balancing).
- Fusion (Eq. 4): RMSNorm each branch output, concatenate, bias-free linear W_F; no branch residual.
- Allocations at matched FLOPs: Wide-Shallow (keep width, split middle blocks), Narrow-Deep (keep depth, narrower blocks), Balanced (used for K=3, 4).
- Joint-KV: one KV cache per branch depth from concatenated branch inputs via a single W_shared, scaled 1/sqrt(K); queries stay branch-local. Branch-region cache is 1/K of Independent-KV.
- Engine on nano-vLLM (paged KV, FlashAttention-3, FlashInfer): branch grouping runs same-depth blocks as one stage (serial steps L_physical -> P + max L_i + C); head folding folds the branch dimension into GQA query heads so branches read the shared KV bank in one kernel call. Tensor- and branch-parallel execution described, not benchmarked in the sections read.

## Results
- Setup: MoE ladder W1-W4, 0.80B-2.07B total, 139M-394M active-body params; FineWeb-Edu, Llama 3 tokenizer, 4K context, ~200 tokens/param. Baseline LR tuned per scale; MBT LR tuned once and reused.
- Table 1, best 2-branch Wide-Shallow vs Standard val loss: W1 2.622 vs 2.653; W2 2.525 vs 2.554; W3 2.444 vs 2.471; W4 2.367 vs 2.392 (gap 0.025-0.031). Fig 6a: ~1.23x body-compute advantage. 9-task zero-shot mean 54.23% -> 56.03% (W1-W4 average).
- Best fraction of blocks in branches ~1/3; parity with Standard at ~78-80% in branches at every scale.
- Branch count (Table 2, W3): Standard 2.471; Wide-Shallow K=2/3/4 2.445/2.457/2.451; Balanced 2.436/2.446/2.449. 2 -> 3/4 branches changes loss <0.006. Narrow-Deep with 3-4 branches loses quality, worst at 4 (App. A.4.1).
- Joint-KV, W4 (Table 3): K=2 loss 2.361, cache saved 23.74%; K=3 2.366, 28.79%; K=4 2.364, 31.82%; Standard 2.392 at 49.5 KiB/token. Across scales 19-34% saved.
- Joint-KV vs Independent-KV at matched cache (Table 5): 0.011-0.012 lower loss at all four scales, <0.6% extra body compute (GQA ratio >=8:1).
- Decode, one H200 (Fig 9, Table 16), averaged over scales: 4-branch 1.12x (one 4K request) to 1.50x (16 concurrent 128K requests), >=1.08x everywhere; 2-branch 1.01-1.32x. Intro: up to 51.4% at 64K input, 8 requests. Source: fewer serial steps plus fewer KV bytes (head folding cuts KV read per step from 1.2x to 0.675x of Standard).
- Ablations: fusion function choice robust (Table 6); branches best in middle layers.

## Applicability
MoE pretraining where decode latency / long-context serving matters. Architectural change: pretraining from scratch, not a checkpoint retrofit. Needs a custom serving engine (branch grouping, head folding are not in stock vLLM) and cross-branch KV synchronisation at each depth. Complementary to KV compression ([[triattention]], [[neural-garbage-collection]]).

## Caveats / Reproducibility
- Hyperparameters given (Tables 7, 9, 13, 14); no code or weights URL in the sections read (only a nano-vLLM link); release unconfirmed.
- Single seed per config appears reported; no variance stated. MBT LR tuned once vs baseline per scale. Scale <=2.07B total.
- Figures here come from the sections read, not the full paper. Tensor/branch-parallel results were not seen.
- Novelty is recombination (PaLM-style parallelism lifted to whole blocks; Joint-KV analogous to YOCO/CLA); MBT + YOCO + CLA flagged as future work.

## Source
- raw/research/weekly-2026-11-21/04-multi-branch-transformer.md
- https://arxiv.org/abs/2611.19800

## Related
- [[triattention]] - KV reduction by compression; MBT reduces cache architecturally (complementary).
- [[neural-garbage-collection]] - learned KV eviction, alternative route to the same goal.
- [[deepseek-v4]] - hybrid attention for ~10% KV cache; same goal, different means; also MoE.
- [[moe-architecture-survey]] - MBT backbone is a latent MoE with Quantile Balancing.
- [[kimi-k3]] - Quantile Balancing router reused.
- [[tidar]] - decode throughput via diffusion drafting.
- [[orthrus]] - shared-KV lossless decode speedup; contrast with architectural speedup.
- [[manifold-constrained-hyper-connections]] - parallel residual-stream designs; MBT fusion has no branch residual.
- [[hyperloop-transformers]] - looping, a different depth/parameter axis.
- [[memory-attention]] - another structural attention/KV change.
- [[cosmos-3]] - Mixture-of-Transformers modality branches; proposed by MBT as future work.
