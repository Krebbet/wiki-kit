# Loopback Transformer

Residual aggregation for looped Transformers (UW-Madison/UCSB/Caltech/Microsoft): store each block's update, decay updates geometrically, redistribute weight with parameter-free attention while keeping the input outside the softmax. Beats matched-depth standard Transformers on ClimbMix with 40-75% of the parameters (191M-3B), and beats mHC/Hyperloop baselines by 0.005-0.011 nats. arXiv 2611.07226.

## Method
- Depth-memory view of residuals (adapting Attention Residuals / AttnRes and the linear-attention write/transport/read framing). A block output contains its input plus its update, so weighting outputs also reweights carried history. Plain addition fixes input weight and gives every update weight 1; joint softmax (AttnRes) makes input and updates compete. Loopback wants three controls: input strength, total update weight, allocation across updates.
- Layout: Huginn prefix-middle-coda [P -> K (xR) -> C], Hyperloop notation. Only residual aggregation changes.
- Store delta_s = f_k(h_s) - h_s; h_{s+1} = h0 + sum_i c_{s,i} delta_i. Input h0 on a separate path, coefficient 1. Prior c0 = lambda^(iteration boundaries crossed), bounding total update weight by K*lambda/(1-lambda). Attention redistributes within that total: c = B * softmax(z + log c0), z = q_s^T(delta_i/||delta_i||)/sqrt(d); learned zero-init query per application, no Q/K/V projections (zero queries = decay-only; lambda=1 + zero queries = plain addition).
- Cost: O(KRd) storage, O((KR)^2 d) read work per token; +0.04-0.08% forward FLOPs with a fused read kernel.
- Baselines at matched tokens and executed depth: Standard, Plain Loop, HC, mHC, Hyperloop, iHC, AttnRes, MHAR.

## Results
ClimbMix, 20 tokens/param, Table 2, Table 9, Fig 1; params exclude embeddings/head.
| Scale | Params vs Standard | Loss (Loopback vs Standard) | 13-task mean |
|---|---|---|---|
| 191M | 40.0% | 2.6187 vs 2.6234 | 38.64 vs 38.28 |
| 374M | 56.3% | 2.4008 vs 2.4395 | 40.89 vs 39.18 |
| 778M | 56.3% | 2.2404 vs 2.2644 | 43.58 vs 43.04 |
| 1.4B | 68% | 2.1073 vs 2.1283 | 46.50 vs 46.33 |
| 3B | 75% | 1.9849 vs 2.0005 | 49.45 vs 48.56 (bootstrap SE 0.40 pp) |
- mHC trails by 0.011 at 374M and 0.005-0.011 across scales. Lowest loss and best 13-task mean among 9 designs at 191M/374M/778M; per-task results mixed.
- 1.4B WikiText ppl 20.29 vs 21.09; 3B 16.74 vs 17.28; 3B word-problem accuracy 2.6% -> 6.4%. Reference-solution loss lower on GSM8K/MATH-500/HumanEval/MBPP at 1.4B and 3B (Table 3).
- Overthinking: extra inference visits raise loss less than Plain Loop (191M at 8 visits +0.060 vs +0.454; 374M at 4 visits +0.074 vs +0.270).
- Update-based readers beat state-based in all 22 family-scale comparisons; best alternative readers trail by 0.030 (191M) / 0.029 (374M) nats.
- 3B training throughput 6% below Standard on 8 H100s.

## Applicability
Pretraining-from-scratch of looped/recurrent-depth LMs (Huginn, Hyperloop style); drop-in residual aggregation for any shared-block loop. Not a retrofit. Gains are in parameters, not latency or peak memory (update history adds memory traffic/activations); fused kernel needed for speed.

## Caveats / Reproducibility
- 191M paired difference vs Standard is inconsistent across 3 seeds (-0.0047, +0.0011, -0.0064; mean -0.0033): "beats Standard" at 191M is within noise.
- Seeds: 2 at 191M/374M for most arms; 1.4B and 3B are single runs per arm. ClimbMix only, <=3B; extra visits do not improve loss.
- Code at github.com/yancyou/Loopback plus project page; fused kernel and tests stated to ship with it (release not verified here). Recipe in appendix Tables 5-7.
- Novelty is recombination; authors concede storing updates is not new. New: three-way coefficient split, bounded geometric prior plus content redistribution, input outside the softmax, update-over-state finding.

## Source
- raw/research/weekly-2026-11-21/03-loopback-transformer.md
- https://arxiv.org/abs/2611.07226

## Related
- [[hyperloop-transformers]] - direct predecessor and baseline; outperformed in the same setup.
- [[manifold-constrained-hyper-connections]] - mHC, closest looped baseline (trails by 0.005-0.011 nats).
- [[par-progress-aligned-recurrence]] - parallel looped-model work.
- [[recirculation]] - depth recurrence, training-free vs trained.
- [[gram-recursive-reasoning]] - recursive/looped reasoning cluster.
- [[hrm-text]] - recurrent-depth LM from scratch.
- [[memory-attention]] - attention-style replacement within blocks.
- [[delta-mem]] - delta-rule write/read framing parallel.
- [[gated-deltanet-2]] - linear-attention memory ideas ported to depth.
- [[mamba-3]] - recurrent memory retention/gating lineage the paper cites.
