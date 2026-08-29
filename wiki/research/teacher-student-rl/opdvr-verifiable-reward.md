---
name: opdvr-verifiable-reward
description: OPDVR reinterprets sampled-token on-policy distillation's implicit token reward as a mis-signed RLVR signal and fixes it with a hyperparameter-free ReLU gate, producing a valid RLVR method that composes with GRPO (GRPD) and beats OPD on six math benchmarks, exceeding the teacher on AIME24
type: research
---

# On-policy Distillation with Verifiable Reward (OPDVR)

Lin, Zhao, Jiang et al. (LeapLab Tsinghua), arXiv:2608.24696. The paper shows sampled-token OPD's implicit per-token reward has the wrong sign convention for RLVR — it can penalize tokens on correct trajectories and reward tokens on incorrect ones — and repairs it with a single ReLU gate, no new hyperparameters. The corrected reward, OPDVR, is a genuine RLVR method: it composes with GRPO to give Group Relative Policy Distillation (GRPD), and is formally proven never anti-aligned with the underlying RLVR gradient.

## Method

Standard sampled-token OPD reward, per generated token $o_t \sim \pi_\theta$, on a trajectory judged correct/incorrect by the verifier:

$$
R_\text{OPD}(o_t) = \begin{cases} \log \dfrac{\pi_T(o_t)}{\pi_\theta(o_t)} & \text{correct trajectory } (+1) \\[4pt] \log \dfrac{\pi_\theta(o_t)}{\pi_T(o_t)} & \text{incorrect trajectory } (-1) \end{cases}
$$

The sign of this reward is set by whichever of teacher/student is more confident at that token — not by trajectory correctness. It can be negative on a correct trajectory (penalizing a token the verifier says is fine, whenever the student already outperforms the teacher there) or positive on an incorrect trajectory (rewarding a token that led to a wrong answer, whenever the teacher happens to be more confident than the student there). This violates the standard RLVR sign contract (correct trajectory ⇒ non-negative advantage).

**Fix.** Wrap each branch in $\max(0, \cdot)$:

$$
R_\text{OPDVR}(o_t) = \begin{cases} \max\!\left(0, \log \dfrac{\pi_T}{\pi_\theta}\right) & \text{correct } (+1) \\[4pt] \max\!\left(0, \log \dfrac{\pi_\theta}{\pi_T}\right) & \text{incorrect } (-1) \end{cases}
$$

This is a conditional token mask, not a reweighting: it zeroes gradient on exactly two "conflicting" token types — Type I (correct trajectory, student already more confident than teacher, $\pi_\theta > \pi_T$) and Type II (incorrect trajectory, teacher more confident than student, $\pi_T > \pi_\theta$) — and leaves the teacher log-ratio magnitude untouched elsewhere. No extra hyperparameters. Because the reformulated reward now obeys the RLVR sign contract, it composes with any policy-gradient algorithm; substituting GRPO's group-relative advantage $\hat A_{i,t}$ for the binary $\pm 1$ label gives **Group Relative Policy Distillation (GRPD)**:

$$
R_\text{GRPD} = \operatorname{sign}(\hat A_{i,t}) \cdot \operatorname{ReLU}\!\left(\operatorname{sign}(\hat A_{i,t}) \cdot \log\frac{\pi_T}{\pi_\theta}\right)
$$

GRPD reuses GRPO's group mean/std advantage normalization unmodified — see [[../rl-optimizers/grpo-std-identity]] for the caveats that carry over.

## Results

Six math benchmarks (AIME24, AIME25, AMC, MATH500, Minerva, OlympiadBench), two settings:

**Table 1 — same-architecture** (Qwen3-4B student ← Qwen3-4B-RL teacher). OPDVR beats sampled-token OPD and top-64 OPD on all six benchmarks: +2.7 pp AIME24 (34.2 → 36.9, exceeding the 36.0 teacher), +2.1 pp AIME25 over sampled-token OPD. Average: 49.1 (OPDVR) vs 47.8 (OPD) vs 50.4 (teacher).

**Table 2 — cross-architecture** (Qwen3-1.7B-Base student ← Qwen3-4B-Base-RL teacher). +5.5 pp AMC, +1.7 pp MATH500 over sampled-token OPD. Average: 22.8 vs 20.9.

**Table 3 — GRPD on held-out DAPO-Math-17K** (disjoint from the teacher's DeepMath training data). GRPD beats both GRPO (+6.5 pp AIME24, +10.9 pp AIME25) and plain OPD (+2.8 pp AIME24). Average: 49.4 (GRPD) vs 48.4 (OPD) vs 44.8 (GRPO).

**Ablation (Table 4 / Fig. 3).** An inverse-gated variant (flipping which tokens get masked) drops below vanilla OPD on all six benchmarks — monotone separation OPDVR > OPD > Inverse-Gated throughout training. The gate direction, not just the existence of a gate, is load-bearing.

**Formal results (Appendix).** Prop. A.1: $\langle \Delta_\text{OPDVR}, \Delta_\text{RLVR} \rangle \geq 0$ always — OPDVR's gradient is never anti-aligned with the verifier gradient. Plain OPD's inner product $= r_t \cdot R \cdot \|u_t\|^2$ can be negative whenever the log-ratio sign disagrees with correctness. Prop. A.2 decomposes standard OPD's gradient as $\Delta_\text{OPD} = \Delta_\text{OPDVR} + \Delta_\text{conflict}$, with the conflict term always having non-positive projection onto the verifier gradient — OPDVR is exactly OPD minus its verifier-opposing component, not an ad hoc modification. Appendix A.3 gives a simplified single-token toy model (fixed prefix, binary choice, teacher-suboptimal initial condition $q_0 > p$) proving $J_\text{OPDVR} = 2q_0 - 1 > 2p - 1 = J_\text{OPD} = J_\text{teacher}$ — the formal backing for the AIME24 teacher-exceeding result, though illustrative rather than a guarantee for full multi-token generation.

**Training dynamics (Fig. 4).** The zero-gated token ratio — the fraction of tokens masked out by the ReLU — stabilizes near 40–50% throughout training in both settings. Response length is erratic and setting-dependent: same-architecture length inflates 1.6k → 6.7k tokens over training for both OPD and OPDVR; cross-architecture instead shows student entropy collapsing from ~2.0. The paper notes this is not controlled by the gating mechanism itself.

## Limitations

- All evaluation is math reasoning (AIME/AMC/MATH500/Minerva/OlympiadBench); no code, agentic, or non-verifiable-domain tests.
- Response-length/entropy dynamics are erratic and setting-dependent, and the paper leaves this as an unaddressed side effect rather than something the gate controls.
- The ~40–50% zero-gated token ratio is reported but not further analyzed — no ablation on whether soft weighting (vs. the hard ReLU mask) does better.
- The teacher-exceeding proof (Appendix A.3) is a single-token toy model with a fixed prefix and binary choice; illustrative, not a guarantee for full multi-token generation.
- GRPD inherits GRPO's own known biases (advantage normalization, group-size effects) unmodified, since it reuses $\hat A_{i,t}$ verbatim — see [[../rl-optimizers/grpo-std-identity]].
- The inverse-gated ablation confirms gate direction matters, but no intermediate/soft-gating variant is tested.

## Relation to the wiki

OPDVR's Appendix A.3 formally proves the student can strictly exceed the teacher, and Table 1 shows this empirically (36.9 vs 36.0 teacher on AIME24) — a soft tension with [[opsd-compresses-rlvr]]'s "compaction not correction" claim that OPD-family distillation cannot push the student past what it already supports. The mechanism reconciles the two readings only partially: OPDVR beats the teacher by *preserving* the student's own already-correct high-confidence predictions (gating out the pull-down-to-teacher gradient), not by the teacher injecting new capability — arguably compatible with a compaction-only reading if the student's own latent correct predictions don't count as "new reasoning states." Recorded as an unresolved conflict in [[../../conflicts/adrs-vs-opsd-compaction]].

The ReLU sign-gate is mechanistically close to [[sg-opd]]'s sign-consistency gate (extrapolate agreement, dampen disagreement per token); worth a direct side-by-side to determine whether these are independently-discovered variants of the same idea. It's also a simpler, hyperparameter-free alternative to [[gc-opd-group-calibrated]]'s group-normalized signed residual for the same underlying problem — aligning a dense teacher-likelihood signal with verifier correctness. Positioned in [[rlt-followups-2026]]'s OPD-siblings catalogue as the entrant that removes hyperparameters/heuristic switching from prior OPD+RLVR combination attempts (Hübotter et al.'s direct weighted combination, hybrid hindsight self-distillation's sign-of-advantage switching, Uni-OPD, self-distilled RLVR).

GRPD is a concrete, formally-analyzed instance of the "GRPO-OPD hybrid" structural extension category named in [[../rl-optimizers/first-principles-two-axis-framework]].

## Source

- `raw/research/weekly-2026-08-28/01-opdvr-verifiable-reward.md`
- https://arxiv.org/abs/2608.24696

## Related

- [[../../conflicts/adrs-vs-opsd-compaction]] — this paper is a third data point on the "does OPD/self-distillation add genuine capability" debate
- [[opsd-compresses-rlvr]] — soft tension: OPSD's compaction-not-correction claim vs. OPDVR's teacher-exceeding result
- [[gc-opd-group-calibrated]] — parallel fix for the same teacher-likelihood/verifier misalignment problem, via continuous group-normalized calibration instead of a hard ReLU gate
- [[sg-opd]] — closest mechanistic overlap: sign-consistency gating vs. OPDVR's ReLU sign-gate, worth a side-by-side comparison
- [[rlt-followups-2026]] — OPD-siblings landscape page; OPDVR is the entrant that removes hyperparameters/heuristic switching from prior OPD+RLVR combination attempts
- [[../rlvr-mechanics/deepseekmath-grpo]] — base GRPO algorithm GRPD extends
- [[../rl-optimizers/first-principles-two-axis-framework]] — names "GRPO-OPD hybrid" as a structural extension category; GRPD is a concrete instance
- [[../rl-optimizers/grpo-std-identity]] — GRPD inherits GRPO's group mean/std normalization unmodified
- [[../../weekly-briefs/2026-08-28]] — brought in by the 2026-08-28 weekly sweep
