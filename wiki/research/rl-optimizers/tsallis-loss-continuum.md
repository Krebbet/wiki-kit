# Tsallis Loss Continuum ($\mathcal{J}_Q$) — Cold-Start RLVR via Gradient Amplification

Lin & Ie (Google, arXiv:2604.25907). Introduces $\mathcal{J}_Q$, a single-parameter loss family via the Tsallis $q$-logarithm that **interpolates between RLVR ($q=0$, exploitation pole) and log-marginal-likelihood ($q=1$, density-estimation pole)** through per-instance gradient amplification $P_\theta^{-q}$. Two drop-in Monte Carlo estimators — **GARL** (prior-sampling) and **PAFT** (posterior-resampling) — fix cold-start stalling where GRPO yields zero gradient. **GARL at $q=0.75$** escapes cold-start on FinQA/HotPotQA/MuSiQue where GRPO and all $q \leq 0.5$ remain at 0% across all metrics; warm-start best deltas of +6.6 to +14.4 maj@16 over GRPO. Most direct fix in the wiki to date for the sparse-success regime that single-sample / few-shot RLVR lives in.

## Source
- [`raw/research/weekly-2026-05-03/04-tsallis-loss-continuum.md`](../../../raw/research/weekly-2026-05-03/04-tsallis-loss-continuum.md) — captured 2026-05-03 (arXiv:2604.25907)

## The continuum

Tsallis $q$-log loss:
$$\ell_q = -\log_q P_\theta = \frac{1 - P_\theta^{1-q}}{1-q}.$$
Gradient identity (Proposition 4.1) — the load-bearing equation:
$$\nabla_\theta \ell_q = P_\theta^{-q} \nabla_\theta \ell_0 = P_\theta^{1-q} \nabla_\theta \ell_1.$$

Endpoints:

| $q$ | Loss | Behaviour | Existing wiki anchor |
|---|---|---|---|
| 0 | RLVR / cross-entropy on correct samples | mode-seeking, escort minimiser concentrates on majority output | [[deepseekmath-grpo]] |
| 1 | log-marginal-likelihood | mode-covering, proper scoring rule | SFT |
| $0 < q < 1$ | smooth interpolation | per-instance amplification $P_\theta^{-q}$ | new |

The escort minimiser $\theta_j^* \propto \alpha_j^{1/q}$ acts as a training-time temperature analogue. **RLVR capability narrowing** (Yue 2025 / [[../self-play/yue-rlvr-boundary]]) is mechanistically explained as the $q=0$ mode-seeking escort distribution.

## Two estimators

| Estimator | Sampling | Recovers at $q=0$ | Recovers at $q=1$ | Cold-start | Warm-start |
|---|---|---|---|---|---|
| **GARL** (Algorithm 1) | prior-sample, amplify by $(\bar{w}_M)^{-q}$ | RB-REINFORCE / VeriFree | IWAE | escapes at $q=0.75$ | best on FinQA $q=0.25$ (+11.8) |
| **PAFT** (Algorithm 2) | posterior-resample, attenuate by $(\bar{w}_M)^{1-q}$ | mode-seeking RL | TRICE EM E-step | escapes at $q=0.75$ | best on HotPotQA / MuSiQue $q=0.75$ (+14.4 / +6.6) |

Both use $M=32$ rollouts (same compute as GRPO) and are verifier-free.

## Cold-start headline (FinQA, no warm-start, no task prompts)

| Method | $q$ | maj@16 |
|---|---|---|
| GRPO / RB-RLOO / all $q \leq 0.5$ | — | **0.0** (no escape) |
| GARL | 0.75 | **38.3** |
| GARL | 1.0 | 33.5 |

Theorems 5.1/5.2 explain the gap: exploitation pole ($q=0$) escape time $\Omega(1/p_0)$; density-estimation pole ($q=1$) $\Theta(\log(1/p_0))$ — exponential separation at low initial success $p_0$.

## Warm-start headline (Qwen 3 0.6B, +Δ over GRPO maj@16)

| Benchmark | Best estimator | $q$ | Δ |
|---|---|---|---|
| FinQA | GARL | 0.25 | +11.8 |
| HotPotQA | PAFT | 0.75 | +14.4 |
| MuSiQue | PAFT | 0.75 | +6.6 |

## Where it sits in the wiki

- Lands cleanly in [[_overview]] as the **fifth post-GRPO axis** of fix:
  - [[dr-grpo]] — length / std bias (warm-start).
  - [[dapo]] — Clip-Higher (cold-start, but variance-style).
  - [[gspo]] — sequence-level clip (MoE stability).
  - [[mcpo]] — mastered-prompt KL hinge (overfitting).
  - [[maspo]] — unifying objective across DAPO / BAPO axes.
  - **$\mathcal{J}_Q$** — RL ↔ SFT interpolation via gradient amplification (cold-start escape rate).
- **Most directly load-bearing for single-sample RLVR** — cold-start $p_0 \ll 1$ is exactly the sparse-success regime [[../single-sample-rl-finetuning/_overview]] inhabits. PAFT's implicit curriculum (early training only easiest rationales pass importance resampling; effective distribution broadens as $P_\theta$ grows) is a no-explicit-schedule curriculum analog.
- **Cleanly subsumes**: $q=1$ PAFT recovers [[../teacher-student-rl/trice-cot-latent-variable]] EM E-step; STaR ([[../self-improvement/star]]) is the hard-acceptance limit of PAFT; $q=0$ GARL recovers VeriFree / RB-REINFORCE.
- SFT-then-RL pipelines ($q=1 \to q=0$ hard switch) are recovered as the degenerate special case; $\mathcal{J}_Q$ replaces the switch with smooth interpolation.

## Conflict touchpoints

- **vs. [[dr-grpo]]:** non-overlapping (warm-start std bias vs. cold-start stalling) — document both axes as orthogonal fixes.
- **vs. [[maspo]]:** MASPO subsumes DAPO/BAPO along Gradient-Utilization, Probability-Mass, Signal-Reliability axes; $\mathcal{J}_Q$ adds an RL↔SFT interpolation axis. Check whether MASPO's Signal-Reliability axis overlaps $P_\theta^{-q}$ — if so, partial subsumption tension.
- **vs. [[mcpo]]:** convergent finding (over-commitment to familiar examples is dangerous), not a conflict.

## Limitations

1. **GARL warm-start collapse** on HotPotQA / MuSiQue: validation drops sharply mid-training at all tested $q$; PAFT does not collapse. Mechanism unverified (pathwise-term corruption from incoherent rationales is the leading candidate).
2. Estimator bias $O(q / M P_\theta^{q+1})$ explodes as $P_\theta \to 0$ — $q=1$ is noisier despite faster escape.
3. Exact-match supervision only; extension to general reward functions open.
4. Single model scale (Qwen 3 0.6B), single seed, no bootstrap CIs.

## Related

- [[_overview]] — RL optimiser theme
- [[dr-grpo]] / [[dapo]] / [[gspo]] / [[mcpo]] / [[maspo]] — sibling post-GRPO fixes (orthogonal axes)
- [[deepseekmath-grpo]] — GRPO baseline ($q=0$ pole)
- [[../single-sample-rl-finetuning/_overview]] — sparse-success regime $\mathcal{J}_Q$ targets
- [[../rlvr-mechanics/_overview]] — mechanism: $P_\theta^{-q}$ amplification explains cold-start
- [[../self-play/yue-rlvr-boundary]] — RLVR capability narrowing now has a mechanistic account
- [[../self-improvement/star]] — hard-acceptance limit of PAFT
- [[../teacher-student-rl/trice-cot-latent-variable]] — PAFT at $q=1$ = TRICE EM E-step
- [[../../weekly-briefs/2026-05-03]] — brought in by the 2026-05-03 weekly sweep
