# Bridged Self-Distillation (BSD) (Chen, Liu et al., TUM/LMU)

BSD distills any teacher that emits reasoning text (shared-tokenizer, cross-tokenizer, closed API) by feeding one teacher trace as privileged context to a frozen copy of the student. The copy's per-token log-prob gap on the student's own rollouts reweights the penalty on failed GRPO rollouts only. The verifier fixes the sign; guidance changes only magnitude. Beats base in 12/12 student-teacher pairs (+1.2 to +4.7 Avg@4 on AIME24/25, HMMT25) and SFT by 3.1-9.7 pts, but margins are small, with no seeds or CIs. Not a single-sample study (2,400 problems). arXiv:2610.26397; code: github.com/TUMLegalTech/Bridged-Self-Distillation.

Note: read from an ingest summary of the paper; appendices (Prop. 1 proof in App. C, OOD forgetting in App. I) were not read directly.

## Method

- **Teacher access:** one reasoning trace $z$ per question, offline, text only. No logits, so tokenizer-agnostic and API-compatible.
- **Rollouts:** student samples without $z$ (standard GRPO, binary verifier reward).
- **Self-teacher:** frozen copy of the student conditioned on $(x, z)$ scores the same tokens: $\delta_t = \mathrm{sg}[\log q_t - \log p_t]$ (Eq. 3), with $q$ the student policy and $p$ the privileged-context self-teacher.
- **Weighting (Eq. 4-5):** for rollouts with $A<0$ only, $A \to w_t A$ with $w_t = (1-\lambda) + \lambda\,\mathrm{clip}_{1\pm\epsilon}(e^{-\delta_t})$. Successes keep plain GRPO advantage. $\lambda$ decays over training.
- **Prop. 1 (App. C):** to first order, equals GRPO on successes plus an OPD-style correction on failures. It is RLSD (Yang 2026a) with the ground-truth answer replaced by an external trace, restricted to negatives.

## Results / Claims

| Result | Number |
|---|---|
| Pairs (Qwen3-0.6B/1.7B/4B, 4B-Instruct x Qwen3-32B, Nemotron-3-30B-A3B, GPT-5.6 Luna) | beats base 12/12 (+1.2 to +4.7); best avg in 11/12 |
| Qwen3-4B, base -> BSD | 59.2 -> 63.9 (shared), 63.6 (cross), 61.9 (API) |
| vs SFT | +3.1 to +9.7; SFT below base in 3 of 4 students (shared, API); Qwen3-0.6B API SFT 10.8 -> 2.8 |
| vs per-setting OPD (OPD / xOPD / ROPD) | up to ~3.6 |
| Ablation (4B, 32B teacher): GRPO | 60.6 |
| answer-only RLSD / BSD-hint | 61.7 / 61.7 |
| BSD-guide / BSD-trace | 62.5 / 63.9 |
| BSD weighting successes too | 61.4 |
| OPSD (no verifier) | 59.7, declining 63.3 (step 25) -> 55.8 (step 150); responses 16.8k -> 12.5k tokens |

- Hint < guide < trace ordering: richer privileged context yields more gain.
- Training-accuracy curves for GRPO/RLSD/BSD differ by <0.2, yet downstream differs: privileged context changes how verifier feedback transfers, not how much is fit.
- Table 2: $|\delta_t|$ correlates with token entropy ($\rho_H$ = 0.83-0.90); gain tracks mean $|\bar\delta|$ (0.037 -> +1.5; 0.114 -> +3.9). Correlational, four students.
- Fig. 3: SFT on short API traces (avg 247 tokens) shortens responses and collapses to ~0 accuracy; BSD and OPD stay stable. App. I: SFT forgets on two OOD benchmarks, BSD does not.
- Case study (AIME24, erroneous prefix): base 4/8 vs BSD 6/8 continuations; student re-checks a quotient/remainder step. Anecdotal, n=1.

## Relation to thesis

- **Sample efficiency:** none shown. 2,400 problems per pair, one trace each, 150 steps; 128-problem dev set for checkpoint selection only. No N=1 or few-problem curve. [[research/teacher-student-rl/one-shot-opd]] is the only N=1 OPD evidence in the wiki; BSD is plausibly testable at N=1 since it needs only one text trace per problem.
- **Concept learning:** no direct evidence. Indirect: privileged-context route preserves the student's distribution (no OOD forgetting) rather than installing teacher surface form, which is the desirable property for a concept-from-example method.
- **RL connection:** credit-assignment reweighting on top of GRPO, not exploration; does not expand the reachable set. Consistent with the reuse/selection view: negatives get dense, token-level shaping from the student's own conditional.
- **Design lesson:** verifier-gated, negatives-only application avoids the OPSD compaction/length-collapse seen in the no-verifier ablation ([[research/teacher-student-rl/opsd-compresses-rlvr]]).
- **Fork tokens:** guidance concentrates on high-entropy tokens ($\rho_H$ 0.83-0.90), independent corroboration of [[research/rlvr-mechanics/high-entropy-minority-tokens]].

## Limitations

- **Stated:** students $\le$4B, one family (Qwen3), English competition math only; needs an automatic verifier; guidance-vs-gain link is correlational.
- **Unstated:**
  - Best-checkpoint selection on a 128-problem dev set; AIME-scale eval (30 problems x 4 samples) gives substantial noise, with no seeds or CIs.
  - Table 2 correlation rests on four students.
  - API trace averages 247 tokens, so the gain is plausibly mostly a final-answer hint (consistent with the hint < guide < trace ordering).
  - Teacher-trace correctness is never verified (no TGOPD-style gating, [[research/teacher-student-rl/tgopd-verify-before-distill]]); only student outcome is checked.
  - No comparison to a strong GRPO + SFT-warmup recipe.
  - OPD baselines are weak on cross-tokenizer pairs (xOPD barely helps), which flatters the "unified" claim.
  - No matched trace-less self-teacher control, so teacher content vs self-teacher contribution is confounded.

## Conflict notes

- **Soft tension with [[research/teacher-student-rl/privileged-info-opsd]]:** AMPLE-MATH finds a genuine teacher reference adds little and is model-dependent; BSD reports +2-4 pts from trace over answer-only/GRPO. Different setups (4B, 150 steps, small eval, no reference-free control); not a clean contradiction.
- **Soft evidence for [[conflicts/opsa-vs-opd-pattern-transfer]]:** trace content matters (hint < guide < trace), mildly against a purely teacher-free story ([[research/teacher-student-rl/opsa-teacher-free-self-adaptation]]); confounded by the self-teacher. Candidate seventh data point; no ruling implied.

## Source

- `raw/research/weekly-2026-10-23/03-bridged-self-distillation.md` (arXiv:2610.26397)

## Related

- [[research/teacher-student-rl/privileged-info-opsd]] — parallel privileged-context self-distillation; trace-richness is a new axis
- [[research/teacher-student-rl/opsd-compresses-rlvr]] — BSD's no-verifier OPSD ablation shows the same compaction
- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]] — teacher-content evidence vs teacher-free claim
- [[research/teacher-student-rl/rlcsd]] — another fix for privileged-context drift (contrastive subtraction)
- [[research/teacher-student-rl/tgopd-verify-before-distill]] — teacher-correctness gating that BSD lacks
- [[research/teacher-student-rl/sgsd-skill-gated-distillation]] — gated self-distillation on negative rollouts
- [[research/teacher-student-rl/one-shot-opd]] — N=1 scale contrast
- [[research/rlvr-mechanics/high-entropy-minority-tokens]] — guidance concentrates on fork tokens
- [[research/teacher-student-rl/_overview]]
- [[conflicts/opsa-vs-opd-pattern-transfer]]
- [[../weekly-briefs/2026-10-23]] — brought in by the 2026-10-23 weekly sweep
