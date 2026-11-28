# Does looping beat unshared depth at equal compute?

**Status:** open (opened by weekly-brief 2026-11-28).

## Position A (new) - gains come from compute, shape and training setup, not sharing

**Source:** [[looptitan]] (arXiv:2611.34821).

- First-party, MoE only: at matched stored params, FLOPs and KV cache, revisit adds +0.7 AdamW / +0.6 Muon mBPB (within noise) over an unshared control.
- Second-hand, dense: its related-work section states that in dense models looping gains come from extra compute and that, at equal compute, unshared models with more parameters reach lower loss (citing other papers; not tested there).

## Position B (existing wiki) - dense looped models beat matched-depth Transformers with fewer parameters

- [[loopback-transformer]]: lower loss than matched-depth Standard on ClimbMix with 40-75% of the params (191M-3B). The 191M margin is within seed noise; 1.4B and 3B are single runs.
- [[hyperloop-transformers]]: beats depth-matched Transformer on FineWeb-Edu at three scales with ~50% fewer params.

## Related evidence
- [[mixture-of-loops-transformer]] beats non-looped OLMo3 at equal tokens with 2x training compute, so it does not discriminate.

## Not yet comparable
LoopTitan's matched-budget control relies on MoE sparsity and has no dense analogue. The Position B baselines match executed depth and tokens but optimizer sensitivity was not isolated in the wiki pages (not checked against raw sources).

## Resolution rule
A dense looped design must beat an unshared model at matched training FLOPs, with a tuned baseline under at least two optimizers (including Muon) and multiple seeds. Until then, scope Position B claims to "per stored parameter at equal executed depth" and do not generalise Position A beyond MoE.

## Related
- [[looptitan]]
- [[loopback-transformer]]
- [[hyperloop-transformers]]
