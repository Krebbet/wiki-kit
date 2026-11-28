# VOPD: Verifiable On-Policy Distillation (Shi, Ermon, Leskovec, Xu)

Scales on-policy distillation's dense teacher implicit reward per prompt group by the correlation between verifier reward and teacher preference, giving small average gains over OPD, OPD+GRPO and fixed-strength extrapolation (ExOPD) in two Qwen3 teacher-student settings. arXiv:2611.30325.

## Method

- Implicit reward $d(s,a)=\log\frac{p_T(a|s)}{p_{ref}(a|s)}$, with $p_{ref}$ the frozen student init.
- Per group of $n$ rollouts, z-score verifier reward ($A^V$) and trajectory sum of $d$ ($A^D$). Projection gives $c_x=\frac1n\sum_i A^V_iA^D_i=\mathrm{Corr}(V,D)$.
- Loss: $\ell=D_{KL}(p_\theta\|p_T)-\lambda c_x\sum_a p_\theta(a|s)\,d(s,a)$, replacing the GRPO term. Equivalent reverse-KL target $q_x\propto p_T^{1+\lambda c_x}p_{ref}^{-\lambda c_x}$; ExOPD is $c_x=1$.
- $c_x$ undefined (zero verifier variance): fall back to fixed 0.25. Top-16 vocabulary, $n=4$, $\lambda=0.25$.

## Results (mean over eight math benchmarks; teacher Qwen3-4B-RL-Math, 64.16)

| Method | 4B → 4B | 4B → 1.7B |
|---|---|---|
| Student init | 35.97 | 31.01 |
| OPD | 64.71 | 50.88 |
| OPD+GRPO | 64.75 | 50.97 |
| ExOPD | 65.25 | 52.34 |
| **VOPD** | **66.38** | **53.32** |

Mean $c_x$ stays positive (~0.36, strong-to-weak) with a nontrivial neutral/negative fraction.

## Scope limits

- ~65% of groups at $n=4$ have zero verifier variance, so most updates are the ExOPD fallback; all-wrong groups carry no outcome signal.
- Gains ~1 pt over ExOPD, no seeds; $\lambda$ swept on AIME24/25, which are also headline columns.
- $D_i$ is an unnormalised length sum, so length/truncation may confound $c_x$. Unbiasedness holds only for the immediate-token-reward estimator.
- Not compared with other outcome-aware methods (e.g. [[opdvr-verifiable-reward]], [[rlcsd]]). Needs teacher logits and an extra frozen reference model.

## Bearing on the thesis

Another way to turn one sparse verifier bit into dense per-token supervision, but the signal vanishes exactly where outcomes are uniform, which is the single-sample regime's typical state *(synthesis)*.

## Source

- raw/research/weekly-2026-11-27/04-vopd-verifiable-opd.md (arXiv:2611.30325)

## Related

- [[_overview]]
- [[opdvr-verifiable-reward]]
- [[gc-opd-group-calibrated]]
- [[uecr-grpo-entropy-calibrated-credit]]
- [[sg-opd]]
- [[tgopd-verify-before-distill]]
- [[rlcsd]]
- [[sequential-opd-then-rl]] — scope tension: staged vs joint
- [[rlt-followups-2026]]
- [[../rl-optimizers/grpo-std-identity]]
- [[../../weekly-briefs/2026-11-27]] — brought in by the 2026-11-27 weekly sweep
