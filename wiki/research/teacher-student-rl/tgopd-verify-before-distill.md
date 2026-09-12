# Teacher-Gated On-Policy Distillation (TGOPD)

"Verify Before You Distill: Prompt-Level Teacher Gating for On-Policy Distillation" (arXiv:2609.02998) introduces TGOPD, which probes the frozen teacher with a few extra rollouts per prompt during its otherwise-idle GPU time, verifier-scores them to estimate **prompt-level teacher reliability**, and hard-routes each prompt to either dense reverse-KL OPD (if the teacher is reliable) or verifier-grounded GRPO (if not) — at near-zero wall-clock cost.

## Method

Standard async OPD setup: student policy $\pi_\theta$, frozen teacher $\pi_T$, binary verifier $r$. Teacher reliability on prompt $x$ is defined as $R_T(x) = \mathbb{E}_{y \sim \pi_T}[r(x,y)]$, estimated online from $K_T=3$ teacher probe rollouts drawn during the idle window while the student is still decoding: $q_T(x)$ = mean pass rate.

A hard gate $g(x) = \mathbb{1}[q_T(x) \geq \tau]$ ($\tau = 2/3$, i.e. 2-of-3 majority) selects the per-token advantage: if open, use the sampled-token reverse-KL OPD advantage (teacher–student log-prob gap); if closed, use the (un-normalized) GRPO group-centered advantage as fallback — **never blended**, a selector not an interpolation. Both candidate advantages are always computed so the pipeline shape doesn't change. Extends unmodified to multi-domain OPD (MOPD) by gating per-prompt against the routed domain-specialist teacher.

## Results

Tested at 4B (Qwen3.5) and 35B (Qwen3.6-A3B MoE) across math/code/instruction-following:

- Beats vanilla OPD in **all 6 domain×scale settings**. Largest gains on code (+3.0 avg at 4B, +2.9 at 35B) — exactly where teacher confidence is least diagnostic of reliability (AUROC 0.51).
- At 35B, **every other baseline** (vanilla OPD, TrOPD, RG-OPD, RLSD-style) causes *negative* transfer on LiveCodeBench vs. the untrained base model (−0.8 to −4.1), while TGOPD achieves +3.0 over base and **surpasses its own teacher** (+1.3 LCB, +1.1 OJBench).
- Ranks first among distillation methods on 7/14 in-domain benchmark columns; surpasses the domain teacher on 6.
- Motivating diagnostic (Fig. 2): in the low-reliability regime, the teacher's own highest-confidence response is still wrong 84% of the time (code) / 61% (math) — reverse-KL OPD otherwise propagates that specific error.
- Compute cost: 3 extra teacher rollouts per prompt, mostly absorbed into previously-idle teacher-node GPU time (utilization 9.8%→78.9% at 4B single-domain); modest measured overhead (5.9% mean step-time increase in one matched 35B code run).
- Gate-threshold ablation shows an inverted-U with peak near $\tau \approx 3/5$–$2/3$ (majority vote); very strict gates ($\tau=5/5$) start discarding useful signal.

## Limitations (acknowledged)

- Requires an automatic/binary verifier — doesn't extend to open-ended tasks without one.
- Binary gate is coarse: doesn't rank prompts, doesn't blend signals.
- GRPO fallback is exactly inert (zero advantage) when a rollout group has uniform outcome; the paper doesn't report how often this occurs.
- The $K_T=3$ probe estimator has variance $R_T(1-R_T)/K_T$ — borderline-reliability prompts get noisy gate decisions.
- The closed-gate-policy ablation (GRPO fallback vs. simple masking) shows the two policies swap which is better depending on scale/domain, with small margins (0.15–0.6 pts) — "fallback is the stronger default" is fairly weakly supported by the reported numbers.

## Relation to the OPD-gating cluster

TGOPD's mechanism (idle-teacher-compute reliability probing + hard binary route) is mechanistically distinct from the wiki's existing OPD-gating cluster: [[gc-opd-group-calibrated]] calibrates continuous per-token advantages against a verifier (not a binary prompt-level gate); [[ida-opd-entropy-influence]] gates on diversity collapse via entropy-influence shrinkage, not reliability; [[sg-opd]]'s sign-consistency gate operates at token granularity; [[rstg-selective-negative-group-distillation]] gates on student-outcome variance, not teacher correctness. All converge on "don't trust the teacher signal unconditionally," at different granularities and for different failure modes.

## Conflict flags

TGOPD's premise and central result — large, reliability-tied gains specifically from *withholding* OPD supervision when the teacher is verifiably wrong — cuts against a purely teacher-content-independent account of OPD's mechanism. See [[opsa-teacher-free-self-adaptation]] and [[../../conflicts/opsa-vs-opd-pattern-transfer]], extended 2026-09-11 with this paper as one of three pieces of new evidence.

## Source

- arXiv: [2609.02998](https://arxiv.org/abs/2609.02998) — "Verify Before You Distill: Prompt-Level Teacher Gating for On-Policy Distillation"
- Captured via 2026-09-11 weekly sweep: `raw/research/weekly-2026-09-11/04-verify-before-distill-teacher-gating.md`

## Related

- [[_overview]] — teacher-student-rl theme overview, OPD saga
- [[gc-opd-group-calibrated]] — closest mechanism-level neighbor: continuous per-token calibration vs. TGOPD's binary per-prompt gate
- [[ida-opd-entropy-influence]] — parallel gating design family, different failure mode (diversity collapse vs. reliability)
- [[sg-opd]] — token-level sign-consistency gate, same "don't trust unconditionally" design family
- [[rstg-selective-negative-group-distillation]] — selective activation of distillation, gates on outcome-variance rather than reliability
- [[esr-early-stopping-opd]] — complementary diagnosis: off-policy teacher decay at late positions vs. TGOPD's per-prompt correctness gate
- [[opd-dual-nature-generalization]] — TGOPD's MOPD extension touches the mixture-dependent capability seesaw by gating each prompt independently per domain teacher
- [[opsa-teacher-free-self-adaptation]] — conflicting mechanism account, see conflict below
- [[one-shot-opd]] — 2026-09-11 sibling capture, same conflict extension
- [[sequential-opd-then-rl]] — 2026-09-11 sibling capture, same conflict extension
- [[../../conflicts/opsa-vs-opd-pattern-transfer]] — extended with this paper's evidence
- [[../../weekly-briefs/2026-09-11]] — brought in by the 2026-09-11 weekly sweep
