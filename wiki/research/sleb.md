# SLEB: Streamlining LLMs through Redundancy Verification and Elimination of Transformer Blocks

Training-free post-hoc block pruning that iteratively identifies and permanently removes the most redundant transformer blocks using a calibration-set perplexity metric, achieving wall-clock speedup proportional to sparsity ratio. Calibration requires 128 WikiText-2 samples; no fine-tuning or recovery training is performed. The resulting model is permanently shrunken with a contiguous parameter footprint.

## Method core

SLEB evaluates three redundancy metrics in ablation before selecting **Metric³** as the operative criterion. Metric¹ is input–output cosine similarity per block (SLEB shows this is insufficient for selection; this directly conflicts with [[shortgpt]]'s primary angular-distance criterion — see Open questions). Metric² extends Metric¹ with a global normalization. **Metric³** (Eq. 5): for candidate block $j$, compute per-token log-likelihood of the already-pruned model with block $j$ additionally bypassed; the block whose removal yields the *smallest* perplexity increase is dropped first.

Algorithm: greedy iterative loop over remaining blocks, each round running $N_{\text{remaining}}$ forward passes on the calibration set. Complexity is $O(N^2)$ forward passes; empirically ~5400 s for LLaMA-2-70B at 20% sparsity on 2× A100. Removed blocks are non-contiguous and model-dependent (LLaMA-2-7B at 20%: indices 14, 23, 11, 24, 10, 27, 15). Key motivation: residual-path increments create high cosine similarity between adjacent block outputs, so block-level granularity captures redundancy that weight-level sparsity misses.

## Goal relevance

Background relevance to **G1** (swappable isolated [[block-isolation-training]] blocks): SLEB's Metric³ quantifies each block's marginal contribution to the residual stream — precisely the isolation assumption G1 depends on. The empirical redundancy pattern (scattered non-adjacent blocks absorb the removal budget) is evidence that blocks are *not* fully interchangeable, which constrains swap-experiment design. No relevance to G2 or G3.

## Credibility

- **Venue:** ICML 2024 (Proceedings of the 41st ICML, PMLR 235)
- **Code:** public — https://github.com/jiwonsong-dev/SLEB
- **Ablations:** Metric¹ vs Metric² vs Metric³ compared; calibration-dataset sensitivity ablated; [[gptq]]-family PTQ compatibility confirmed. No ablation of calibration set size or iterative-vs-one-shot removal order beyond the metric comparison.
- **Replication:** Standard HuggingFace OPT/LLaMA-2 checkpoints; straightforward to replicate.

## Empirical claims

| Setting | Metric | SLEB | Baseline |
|---|---|---|---|
| LLaMA-2-70B, 20% sparsity, 2× A100 | Throughput | **1.27×** | 0.98× (2:4 pruning at 50%) |
| LLaMA-2-70B, 20% sparsity | Prompt latency | **1.26×** | ≈SliceGPT at 30% channel sparsity |
| LLaMA-2-7B, 20% sparsity | C4 perplexity | 12.32 | 7.26 dense |
| OPT-6.7B, 20% sparsity | C4 perplexity | 15.99 | 12.71 dense |
| SLEB-20% + AWQ 4-bit | C4 perplexity | no additional degradation vs SLEB alone | — |

2:4 structured pruning (SparseGPT, Wanda, DSnoT) yields **zero** end-to-end throughput gain at batch sizes 1–128 on A6000; SLEB's block drop delivers consistent speedup independent of batch size.

## Open questions / failure modes

- **Metric conflict with [[shortgpt]]:** SLEB claims Metric¹ (input–output angular similarity) is insufficient for block selection. ShortGPT uses an analogous angular-distance metric as its primary criterion. This is an open conflict — ruling pending ingestion of ShortGPT. Flagged for a `conflicts/` page once both are ingested.
- Perplexity cost at 20% is substantial for smaller models (LLaMA-2-7B: 7.26 → 12.32); no recovery mechanism explored. Unclear how much LoRA/PEFT fine-tuning could reclaim (cf. [[iterative-layer-distill]], which builds recovery in).
- $O(N^2)$ forward passes; ~5400 s for 70B at 20% — "training-free" does not mean cheap.
- Evaluated only on OPT and LLaMA-2; generalization to non-uniform block structures (MoE layers, cross-attention) unknown.
- Static removal only; per-input dynamic skipping explicitly rejected. Hybrid (SLEB as warm start for a sparse routing pool) is unexplored.

## Source

- `raw/research/block-training-quantization/17-sleb.md` (PDF capture)
- `raw/research/block-training-quantization/08-sleb-abs.md` (arXiv abstract)

## Related

- [[layerskip]] — block-elimination cousin; LayerSkip trains blocks to be skippable, SLEB is entirely training-free
- [[block-isolation-training]] — concept anchor; SLEB's Metric³ operationalizes each block's marginal contribution to the residual stream
- [[shortgpt]] — predecessor / sibling block-pruning method; **potential conflict** on redundancy metric (SLEB demotes angular-distance metric that ShortGPT treats as primary — flag for `conflicts/` page)
- [[laco]] — sibling block-pruning baseline; contemporaneous with SLEB
- [[iterative-layer-distill]] — combines block removal with recovery training (SLEB omits recovery entirely)
- [[gptq]] — confirmed compatible; SLEB + AWQ 4-bit stack produces no additional perplexity hit beyond SLEB alone
