# Sequential Beats Joint: OPD-then-RL

"Sequential Beats Joint: On the Interplay between On-Policy Distillation and RLVR" (arXiv:2609.04108) shows that a simple two-stage recipe — reverse-KL on-policy distillation (OPD) against a frozen external teacher, then a hard switch to pure GRPO — consistently beats pure OPD, pure RLVR, and **nine** joint OPD+RLVR combination methods on logic and math reasoning. The mechanism: decoupling lets OPD expand the student's teacher-bounded solution *coverage*, while RL *sharpens* within it; fusing the two signals in one training step causes gradient interference.

## Method

Unifies existing OPD–RLVR hybrids under one token-level policy-gradient view: $\nabla_\theta J = \mathbb{E}[\sum_t A_t^{(i)} \nabla_\theta \log \pi_\theta(y_t|h_t)]$, differing only in the per-token advantage. GRPO uses group-normalized outcome advantage $\hat{A}^{(i)}$; OPD uses $d_t^{(i)} = \log\pi_T(y_t|h_t) - \log\pi_\theta(y_t|h_t)$ (reverse-KL against a frozen teacher).

Existing joint methods split into:
- **Weighted-additive** ($A = w_R \hat{A} + w_T d$; KDRL, KDRL-mask, SRPO, HDPO) — teacher term can flip the RL advantage's sign.
- **Teacher-modulated** ($A = m(d) \cdot \hat{A}$; TRRD, RLSD) — teacher rescales magnitude only, sign fixed to $\hat{A}$.

The proposed **OPD-then-RL** is a hard switch: $A_t^{(i)} = d_t^{(i)}$ for training step $\leq S$, then $\hat{A}^{(i)}$ afterward ($S=60$, chosen from validation-curve saturation). A "soft switch" analogue (KDRL-Annealing, linear $\beta$ decay) underperforms the hard switch.

## Results

Teacher = Qwen3-8B (non-thinking); student = Qwen3-1.7B-Base (0.6B ablation shows the same trend).

- **Logic reasoning** (K&K, Zebra, Countdown from ReasoningGym): OPD-then-RL avg pass@1 = 80.6, beating the next-best joint method (KDRL-Annealing, 68.9) by 11.7, and pure OPD (53.9) by **26.7 points**.
- **Math** (DeepMath-103K → MATH500/AMC23/AIME24/AIME25): 31.8, a statistically significant lead over 6/9 competitors, tied with the 3 strongest.
- No competing method beats OPD-then-RL on pass@32 on either family.

## Mechanism: coverage expansion vs. sharpening

The central claim, via pass@k analysis: **OPD expands** the student's pass@k curve (especially at large $k$) above the base model — treated as capability expansion / coverage of teacher-supported solutions — while **RL sharpens**, redistributing probability mass toward pass@1 without much further boundary expansion on its own.

Critically: **OPD and every tested joint method plateau at or near the teacher's own pass@1** (56.6% on K&K) — genuine capability expansion beyond the teacher only appears once continual RL is layered on top after the OPD stage. A KL$(p_S \| p_T)$ decomposition during the RL stage shows cross-entropy $H(p_S, p_T)$ keeps falling (teacher still assigns high likelihood to student outputs) while entropy $H(p_S)$ falls faster — divergence rises not because the student leaves the teacher's support, but because it concentrates onto a smaller nucleus within it.

A sign-conflict-rate (SCR) analysis of parameter updates explains *why* joint mixing underperforms: OPD-then-RL's updates are near-zero-conflict (3.38–3.89% even at the top-100% of parameters), far below pure RL (20.36%/17.00%) and joint methods — joint mixing forces sign-conflicting gradients on the same parameters every step.

## Limitations (authors' own)

- Scope restricted to a frozen, generally-stronger external teacher; untested for comparable-capability teachers, multi-teacher setups, or on-policy self-distillation.
- Frozen-teacher only — doesn't test the "teacher-first" allocation (RL-improve the teacher, then distill) used by GLM-5/DeepSeek-V4 pipelines; authors note OPD-then-RL is a low-cost partial proxy for that variant.
- Only the standard on-policy reverse-KL OPD objective is tested; forward-KL/JSD variants left open.
- Only one teacher/student scale pair thoroughly explored (8B→1.7B). The switch point $S$ is chosen per-task from a validation curve, not a closed-form stopping rule — closer to an empirical heuristic than an algorithm.

## Conflict flags

The teacher-pass@1-bounded ceiling found here — OPD and joint methods plateau at the *specific* teacher's actual measured performance — is difficult to square with a teacher-optional, token-suppression-only account of OPD's mechanism. See [[opsa-teacher-free-self-adaptation]] and [[../../conflicts/opsa-vs-opd-pattern-transfer]], extended 2026-09-11 with this paper as one of three pieces of new evidence.

## Source

- arXiv: [2609.04108](https://arxiv.org/abs/2609.04108) — "Sequential Beats Joint: On the Interplay between On-Policy Distillation and RLVR"
- Captured via 2026-09-11 weekly sweep: `raw/research/weekly-2026-09-11/03-sequential-beats-joint-opd-rlvr.md`

## Related

- [[_overview]] — teacher-student-rl theme overview, OPD saga
- [[opsd-compresses-rlvr]] — reinforces "compaction not correction": OPD alone can't create new reasoning states, only subsequent RL breaks the teacher ceiling
- [[opd-dual-nature-generalization]] — parallel "teacher-bounded" framing (same-origin/cross-origin generalization there, teacher-pass@1 ceiling here)
- [[opsa-teacher-free-self-adaptation]] — conflicting mechanism account, see conflict below
- [[one-shot-opd]] — 2026-09-11 sibling capture, same conflict extension
- [[tgopd-verify-before-distill]] — 2026-09-11 sibling capture, same conflict extension
- [[../single-sample-rl-finetuning/reft]] — ReFT's SFT-then-PPO is the sequential baseline this paper benchmarks against; OPD is a strictly better cold start than SFT for subsequent RL
- [[../rlvr-mechanics/_overview]] — nuances the "does RLVR expand capability beyond the base distribution" debate (Invisible Leash / RL-as-selection thread): pure RL sharpens within existing support, but RL after OPD (which already expanded support) can exceed both base and teacher
- [[../../conflicts/adrs-vs-opsd-compaction]] — orthogonal axis (does self-distillation add capability at all); this paper reframes the question as training-order/schedule
- [[../../conflicts/opsa-vs-opd-pattern-transfer]] — extended with this paper's evidence
- [[../../weekly-briefs/2026-09-11]] — brought in by the 2026-09-11 weekly sweep
