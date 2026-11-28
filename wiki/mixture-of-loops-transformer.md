# Mixture-of-Loops Transformer (MoLT)

HUST / ByteDance Seed / Toronto (arXiv:2611.34923). Looped Transformer that reuses keys/values across loop iterations through joint sequence+depth attention (MoLA). The U-shaped variant (looped encoder + non-looped cross-only decoder) beats a non-looped OLMo3 at equal training tokens, **not equal compute**; its 700M run costs 2.01x training FLOPs for a 1.7x token speedup.

## Method
- MoLA: one softmax over sequence KV plus same-position KV from other layers/loops (extends MoDA).
- MoLT-R carries the residual across loops. MoLT-KV restarts each loop from embeddings and reads the previous loop's output as prefix memory KV.
- U-MoLT: loop-KV encoder + causal cross-only decoder with per-layer KV re-projections; decoder skipped at intermediate loops.
- Loop forcing: next-token loss at every loop, trained in parallel over positions.
- Mixture-of-Loops decoding: one traversal per new token from cached prefix memory, with 1-2 loop parallel prefill (Hybrid).

## Results
| 400B tokens | OLMo3 acc / PPL | Looped acc / PPL |
|---|---|---|
| 700M (U-MoLT) | 56.6 / 15.64 | 59.1 / 14.86 |
| 1.5B (U-MoLT) | 61.2 / 13.86 | 62.6 / 13.15 |
| 3B MoE, 660M active (U-MoLT) | 60.1 / 13.99 | 62.2 / 13.24 |
- 700M MoLT-R: 59.2 / 14.84. COPA alone is about 1.2 of the 2.5-point U-MoLT gain at 700M (ingest arithmetic).
- Cost at 700M: +1.5% params, 1.99x wall clock, 1.34x peak memory.
- Qwen3.5-0.8B continued pretraining, 100B tokens: mean CE 2.496 -> 2.480.
- Hybrid decoding at 4,096-token prompts cuts latency 32-50% vs fixed 2-loop, about matching non-looped OLMo3 (~113M models). Pure single-traversal prefill is far slower (47-74 s vs ~1 s).

## Caveats
- No non-looped model gets matched added compute. The authors defer that test; ingest arithmetic on their numbers suggests ~1.17x baseline FLOPs to reach baseline loss (mid-schedule, so not a fair test either way). Compare [[looptitan]].
- No looped-residual baseline at scale; ablations are single-seed; the 700M run uses AdamW, small ablations Muon.
- Code URL given (github.com/hustvl/MoLT) but the paper says release is forthcoming.

## Source
- `raw/research/weekly-2026-11-28/02-mixture-of-loops.md`
- https://arxiv.org/abs/2611.34923

## Related
- [[loopback-transformer]] - parameter-free cross-iteration aggregation.
- [[hyperloop-transformers]] - cross-loop residual mixing.
- [[looptitan]] - matched-budget controls for looped MoEs.
- [[multi-branch-transformer]] - parallel Joint-KV / KV-efficiency design.
- [[par-progress-aligned-recurrence]] - alternative looped training objective.
- [[conflicts/looped-parameter-sharing-benefit]]
