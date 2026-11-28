# Verifiable On-Policy Distillation (VOPD)

Stanford / Google DeepMind (arXiv:2611.30325). Weights the teacher's implicit reward in OPD by the per-prompt-group correlation between teacher score and verifier reward, applied over the next-token distribution instead of only sampled tokens. Reports +1.67 (4B -> 4B) and +2.44 (4B -> 1.7B) eight-benchmark average over vanilla OPD, about +1 over fixed output-space extrapolation (ExOPD).

## Method
- Implicit reward d = log p_teacher / p_ref (p_ref = student init).
- Per group of n=4 rollouts: c = Corr(verifier reward, trajectory sum of d), in [-1, 1].
- Loss: KL(student || teacher) - lambda * c * E_student[d] (top-16 tokens in practice). Replaces the GRPO term.
- Zero-variance groups use a fixed 0.25 coefficient (ExOPD-style).
- Cost: one frozen reference model and one extra forward pass per batch. Needs teacher logits.

## Results
| 8-bench avg | Teacher | OPD | OPD+GRPO | ExOPD | VOPD |
|---|---|---|---|---|---|
| 4B -> 4B | 64.16 | 64.71 | 64.75 | 65.25 | 66.38 |
| 4B -> 1.7B | 64.16 | 50.88 | 50.97 | 52.34 | 53.32 |
- Best distillation method on 6/8 benchmarks in both settings.
- Mean c positive (0.36 over 3,266 groups, strong-to-weak).

## Caveats
- About 65% of groups at n=4 have zero variance, so most run the fixed fallback; no ablation of the fallback.
- No seeds or error bars; margins over ExOPD are ~1 point. Lambda ablation uses AIME24/25, which are also headline benchmarks (possible selection leakage).
- Printed "Student" rows in Tables 1-2 do not match their per-benchmark entries.
- Math only, two Qwen3 pairs, one teacher. Code linked (github.com/juntongshi48/VOPD), not checked.
- ExOPD beating OPD here disagrees with [[ride-opd-residual-extrapolation]]: [[conflicts/exopd-output-space-extrapolation]].

## Source
- `raw/research/weekly-2026-11-28/04-verifiable-opd.md`
- https://arxiv.org/abs/2611.30325

## Related
- [[ride-opd-residual-extrapolation]] - extrapolation in hidden-state space; reports ExOPD failing.
- [[rlsd-self-distilled-rlvr]] - verifier direction with teacher magnitude on sampled tokens.
- [[waypoint-opd]] - agreement-gated teacher shift.
- [[dopd-dual-on-policy-distillation]]
- [[p2-mopd]] - learned weighting variant of OPD.
- [[high-entropy-tokens-rlvr]] - contrasting answer to sparse verifier credit.
