# LoopTitan: what parameter revisit buys an MoE

Controlled decomposition (arXiv:2611.34821, Phase 1 technical report; Shanghai AI Lab / SMU) of looped-MoE gains in from-scratch pretraining. At matched stored params, FLOPs and KV cache, parameter revisit itself adds nothing resolvable (+0.7 AdamW / +0.6 Muon mBPB, within noise; lower is better). The recipe's gain comes from network shape and residual scaling, and switching optimizer to Muon is worth far more.

## Method
- Looped MoE follows SMELT: middle layers computed twice with all core parameters shared, residual scale 1/2 on revisited layers, fixed visit count.
- Key control: same computed layers, width, top-8, residual scaling and training, but unshared middle layers with half the experts each (1.1% more params).
- DCLM, 1.3B stored / 0.2B active at 5B tokens (to 20B), plus 3.0B stored. Noise = 2 SE from per-optimizer seed SD. Only the main setting has multiple seeds.
- Proposition 1: a constant residual scale *a* is equivalent to rescaling output-projection init, LR (by *a*) and weight decay (by 1/*a*) under AdamW and Muon, up to clipping and epsilon.

## Results
- Cumulative decomposition, AdamW / Muon (Tab. 1): shape -4.5 / -3.0; layout + residual scaling -2.6 / -0.8; revisit +0.7 / +0.6; total -6.3 / -3.2.
- Optimizer: standard MoE AdamW -> Muon = -23.6 mBPB, 3.7x the recipe's AdamW gain (worth ~1.53x tokens at 5B).
- Added compute (Muon): one extra visit -11.5; deeper unshared MoE -10.4 (90.2% of it); 2x experts -9.3. The visit's remaining 1.1 edge is beyond noise; interpolation says spending the compute on 1.31x tokens would give -13.4.
- Revisit hurts at 0.625B tokens (+7.5 AdamW / +2.0 Muon).
- 3-4 visits do not beat 2 at matched budgets.

## Caveats
- MoE only. Dense looped models ([[loopback-transformer]], [[hyperloop-transformers]], [[mixture-of-loops-transformer]]) are not tested; the paper's remarks on dense looping summarise other work. See [[conflicts/looped-parameter-sharing-benefit]].
- Small scale (<=3.0B stored, 24B tokens, one dataset, test loss only). Under Muon the revisit point estimate favors looping in every longer or larger single-seed setting (-0.4 to -1.3), all within noise.
- The authors replaced the pre-registered pooled seed SD with per-optimizer SDs; two verdicts flip under the registered one.
- Appendices were only partly read at ingest.
- Release stated (github.com/datamllab/LoopTitan, 17 checkpoints), contents not verified.

## Source
- `raw/research/weekly-2026-11-28/01-looptitan.md`
- https://arxiv.org/abs/2611.34821

## Related
- [[loopback-transformer]] - dense looped design whose gains this does not test; check optimizer sensitivity.
- [[hyperloop-transformers]] - same.
- [[mixture-of-loops-transformer]] - concurrent looped design without a compute-matched control.
- [[recirculation]] - inference-time looping, outside this scope.
- [[moe-architecture-survey]] - depth-vs-experts trade.
- [[conflicts/looped-parameter-sharing-benefit]]
