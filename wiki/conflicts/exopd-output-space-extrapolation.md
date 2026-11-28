# Does output-space extrapolation (ExOPD) help or hurt OPD?

**Status:** open (opened by weekly-brief 2026-11-28).

## Position A (new) - fixed ExOPD improves on OPD

**Source:** [[verifiable-opd]] (arXiv:2611.30325). ExOPD at coefficient 0.25: 65.25 vs OPD 64.71 (RL Qwen3-4B -> Qwen3-4B) and 52.34 vs 50.88 (4B -> 1.7B), eight-benchmark average. No seeds.

## Position B (existing wiki) - ExOPD degrades

**Source:** [[ride-opd-residual-extrapolation]] (arXiv:2609.36484). ExOPD at lambda=1.25 falls below teacher on four same-init pairs (3 seeds, math); on Qwen3-4B -> Just-Qwen3-4B it scores 48.75 vs untouched student 62.82.

## Comparability
- Synthesis: VOPD's 0.25 on the implicit reward appears to equal an extrapolation strength of 1.25 in the teacher/reference-exponent form RIDE uses; not confirmed against either implementation.
- Different RL teachers, benchmark sets, base distillation loss (RIDE also reports OPD top-1), training length (500 vs 140-160 steps).

## Resolution rule
Run both ExOPD implementations on one teacher/student pair with the same KL form, step count and seeds. Until then treat ExOPD's sign as setup-dependent.

## Related
- [[verifiable-opd]]
- [[ride-opd-residual-extrapolation]]
