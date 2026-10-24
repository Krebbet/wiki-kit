# Predicting Privileged Information Effectiveness for On-Policy Self-Distillation (Scale AI / U. Michigan / Mila)

Controlled study of 16 privileged-information (PI) configurations for on-policy self-distillation (OPSD) on three multi-turn agentic benchmarks (ALFWorld, AppWorld, tau2). Two cheap KL-based offline metrics, sampled-token reverse KL $D$ and the error-step KL contrast $\Delta d_{err}^-$, predict post-training gains better than PI utility (teacher reward with PI minus student reward), which is inflated by answer leakage. A Passcode control shows utility tracks what a student can copy while KL tracks what it can learn. Mixing OPSD with GRPO at the advantage level ($\lambda=0.99$) beats matched GRPO on all three benchmarks.

Note: derived from an ingest summary of the paper; appendices were not read. Authors not recorded in the summary.

## Method

- **OPSD loss (Eq. 1):** reverse KL from student to the same model conditioned on PI, stop-grad teacher. No reward in pure OPSD.
- **PI formats:** 4 trajectory variants (Action, +Obs, +Thought, +Obs+Thought); 3 hints (Summary, Skill = strategy + mistake analysis, Checklist from expert-vs-failed-student pair). Generators: GLM-5.2, Qwen3.7-Plus, or the student itself.
- **Offline metrics:**
  - Utility $U$ = teacher reward with PI minus student reward (Eq. 2).
  - $D$ = mean $|\log p_S/p_T|$ on student-sampled tokens (Eq. 3).
  - $\Delta d_{err}^-$ = positive-part sampled-token KL at judge-labelled error steps of failed rollouts minus a task- and step-index-matched baseline (Eqs. 4-6). Needs an LLM judge.
- **Combined objective (Eq. 7):** $A = \lambda A_{GRPO} + (1-\lambda) A_{OPSD}$.
- **Students:** Qwen3 family up to 30B-A3B; GRPO combination tested on 4B-Instruct. Train sets: ALFWorld 1,600 tasks, AppWorld 90, tau2 352; one static PI reference per task.

## Results / claims

| Result | Number |
|---|---|
| PI ordering | Info-dense trajectory (esp. with obs) > hints; Skill best hint |
| Generator effect | GLM-5.2 lead up to 36.0 pts on ALFWorld hints; within 3.2 for trajectories |
| Thinking model (Qwen3-4B-Thinking) | Inconsistent benefit; extra obs/thought can hurt |
| Spearman $\rho$, $\Delta d_{err}^-$ vs post-training perf | Positive in 9/9 student-benchmark cells (0.10-0.94) |
| Spearman $\rho$, $D$ | Positive in 8/9 (0.65-0.95); $-0.84$ for Thinking on tau2 |
| Spearman $\rho$, utility | Erratic: 0.81-0.96 AppWorld; $-0.56$ / $-0.10$ ALFWorld; $-0.06$ to 0.71 tau2 |
| Per-task PI selection | $\Delta d_{err}^-$ beats random (most on mixed win/loss pools; +5.1 pts at step 40 among self wins, gap closes by epoch 3); $D$-selection at or below random except for the single strong-generator pool |
| OPSD+GRPO ($\lambda=0.99$, trajectory PI) vs GRPO | ALFWorld 95.13 vs 84.96; AppWorld 43.90 vs 42.91; tau2 55.04 vs 48.27 |
| $\lambda$ sweep | More GRPO helps all PI types, weak PI (Checklist, Skill) most; PI quality ordering persists through 0.99 |
| Early-learning dynamics | PI plateaus/declines after ~step 100 (1 epoch, ALFWorld) while GRPO keeps improving |
| AppWorld overfit | Trajectory PI reaches ~100% train success but 39.14 test pass@1 |

**Passcode leakage control (ALFWorld, Fig. 5):**
- PI holding only the correct key: 98.1 pass@1 utility, student unchanged by training.
- Swapping the key moves utility 25 pts but not training.
- Swapping the trajectory (mismatched task) halves training perf to 45.0 and lowers both KL metrics.
- Paper's conclusion: effective PI is mistake-aware context beyond the correct answer.

## Relation to thesis

- **Copy vs learn.** The Passcode control is the cleanest indirect evidence in the wiki that a privileged teacher signal can be high-utility yet non-instructive. For a single-sample method, "the example makes the teacher succeed" is not a sufficient selection criterion; the signal must induce student-relevant divergence at error steps.
- **Pre-training screening.** $D$ and $\Delta d_{err}^-$ are computed offline from student rollouts and a PI-conditioned forward pass, so they can rank candidate examples or PI formats per task without a training run. Directly reusable for choosing which single example to train on. The per-task selection result (gain concentrated in mixed win/loss pools) is the relevant datum.
- **Error-step targeting as credit assignment proxy.** Judge-labelled error steps localise where the PI-conditioned teacher disagrees most; parallels first-mistake credit work.
- **Sample efficiency.** Not a single-sample study; PI speeds early learning but saturates after ~1 epoch and can interfere with outcome learning, and small-set overfit is visible (AppWorld). Static PI is a one-epoch tool; pair with outcome RL.
- **Mixing.** Near-pure GRPO weighting ($\lambda=0.99$) with a small OPSD term is the winning regime, consistent with OPSD as a light shaping signal rather than a standalone learner.

## Limitations

- **Stated:** static PI becomes redundant after ~1 epoch and can interfere; overfitting on small sets; large distribution shifts can overwrite a strong thinking model ($D$ negative for Thinking on tau2); $\Delta d_{err}^-$ needs an LLM judge; correlation floor $\rho=0.10$.
- **Unstated:**
  - Only Qwen3 students and three agentic benchmarks; no math/reasoning RLVR.
  - Each correlation is over ~7-16 points per cell, so $\rho$ is noisy.
  - GRPO combination tested on 4B-Instruct only with one simple mixing rule.
  - Best-of-3-checkpoint-window pass@1 reporting is optimistic.
  - Per-task selection tested only on ALFWorld.
  - Reference trajectories come from much stronger models, a different regime than self-only PI.
  - Appendices unread here.

## Conflict notes

- **Soft:** the OPSD+GRPO mix beating GRPO conflicts with the claim in [[research/teacher-student-rl/sequential-opd-then-rl]] that joint OPD+RLVR mixing causes sign-conflicting gradients and loses to a hard sequential switch. Settings differ (agentic, privileged self-teacher, 4B-Instruct vs math/logic with external teacher), the paper does not compare against sequential, and its own observation that OPSD interferes after 1 epoch is consistent with the sequential view.
- **Moderate:** mismatched-trajectory PI halving training perf (45.0) counts against the "teacher is unnecessary" claim of [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]]; the signal is not purely teacher-free low-logp suppression. Extra data point for [[conflicts/opsa-vs-opd-pattern-transfer]]. Setting differs (agentic, PI-conditioned self-teacher), so not a direct contradiction.
- **Tension:** [[research/teacher-student-rl/opsd-compresses-rlvr]] (compaction, not correction) vs mistake-aware PI and error-step targeting adding value beyond GRPO here.

## Source

- `raw/research/weekly-2026-10-23/04-privileged-info-effectiveness-prediction.md` (arXiv:2610.22512)

## Related

- [[research/teacher-student-rl/privileged-info-opsd]] — AMPLE-MATH (arXiv:2609.20612) on what PI adds; this paper extends with format/source/metric screening on agentic tasks
- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]] — teacher-free claim; PI content matters here
- [[research/teacher-student-rl/opsd-compresses-rlvr]] — compaction not correction
- [[research/teacher-student-rl/rlcsd]] — contrastive correct-vs-wrong-hint KL; parallels error-step KL contrast
- [[research/teacher-student-rl/sgsd-skill-gated-distillation]] — Skill-style PI strongest hint format (corroborates)
- [[research/teacher-student-rl/tapo-error-trajectory-distillation]] — explicit error diagnosis; $\Delta d_{err}^-$ operationalises error-targeted supervision
- [[research/teacher-student-rl/sequential-opd-then-rl]] — joint-mixing conflict (soft)
- [[research/process-reward-models/cliff-first-mistake-credit]] — judge-located error steps for credit vs diagnostics
- [[conflicts/opsa-vs-opd-pattern-transfer]]
- [[../weekly-briefs/2026-10-23]] — brought in by the 2026-10-23 weekly sweep
