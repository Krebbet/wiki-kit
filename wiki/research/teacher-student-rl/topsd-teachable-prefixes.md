# TOPSD: Teachable On-Policy Self-Distillation (Cho, Yoon, Park, Seo, Chu, Oh, Kim; KAIST / Korea U.)

TOPSD patches OPSD for multilingual reasoning by restricting where and whether the privileged self-teacher is trusted. It names a failure mode, Teacher Drift: as the student's erroneous prefix grows, the reference-conditioned teacher stops correcting and starts following the student's errors, earlier in lower-resource languages. TOPSD (1) cuts each student trajectory at the first sustained rise of the cumulative teacher/student likelihood ratio, and (2) keeps the trajectory only if the teacher, greedily continuing from that prefix, reaches the correct answer. Claims best Avg@3/Pass@3 on PolyMath High (10 languages) at Qwen3-1.7B/4B/8B, +1.07 to +2.64 pp Avg@3 over the best baseline (OPSD or COPSD). arXiv:2611.08179; no code released.

## Key claims

- **Teacher Drift:** the cumulative geometric-mean ratio $C_{i,t}=\exp\big(\tfrac{1}{t-1}\sum_{s<t}\log p_T/p_S\big)$ trends toward 1 as the prefix grows, faster in low-resource languages. Teacher recoverability $\mathrm{Rec}(m)$ (fraction of student-wrong / teacher-right-from-scratch problems the teacher still solves after conditioning on the first $m-1$ student tokens, greedy) falls with $m$. Alignment up, correction ability down.
- Supervision should be restricted to a "teachable prefix", and only when the teacher can still recover. Strong-teacher engineering (COPSD: English reference as privileged context) is necessary but not sufficient.

## Method

- **Prefix selection (Eq. 7):** $d_i=\min\{j: C_{i,j+k}>\tau\ \forall k<K\}$, $\tau=0.9$, $K=4$; mask $M^{prefix}_{i,t}=\mathbb{I}[t<d_i]$. No cutoff found: whole trajectory kept. Cutoff detected in >95% of trajectories, at a relative position of 6.98-10.47% of trajectory length on average (Table 3), i.e. supervision is applied to only about the first 7-10% of tokens.
- **Recoverability verification (Eq. 8-9):** teacher (frozen base + English problem + English reference) greedily continues from $\hat y_{<d_i}$ (up to 8,192 / 12,288 tokens); $G_i=\mathcal V(\hat y_{<d_i}\oplus z_{\ge d_i},a_i)$ via rule-based `\boxed{}` check. $M^{TOPSD}=G_iM^{prefix}$. The continuation is used only as a gate, never as a target, so training stays on the original student states.
- **Objective (Eq. 10):** OPSD full-vocabulary token divergence over masked tokens, normalised per trajectory ($1/n_i$) then uniformly averaged over trajectories within a language and over languages with eligible trajectories.
- **Setup:** Qwen3-1.7B/4B/8B, LoRA r=64, $\alpha$=128, lr $10^{-6}$, batch 32, 160 steps, 1 rollout/prompt (max 2,048 tokens, T=1.1), fixed teacher. Data: 500 problems per language x 10 languages (multilingual OpenThoughts from COPSD). ~9 h per 160-step run for 1.7B on 4x A6000 (verification rollouts are costly).

## Results (PolyMath High, overall Avg@3 / Pass@3, %)

| Model | Vanilla | OPSD | COPSD | TOPSD |
|---|---|---|---|---|
| Qwen3-1.7B | 9.23 / 15.44 | 9.60 / 16.64 | 9.95 / 16.56 | 11.60 / 18.72 |
| Qwen3-4B | 15.49 / 21.92 | 16.72 / 25.12 | 16.19 / 24.88 | 17.79 / 26.00 |
| Qwen3-8B | 22.37 / 31.12 | 22.37 / 31.92 | 22.48 / 31.76 | 25.12 / 35.28 |

- Gains concentrate in low/medium-resource groups (+0.89 to +3.47 pp Avg@3 over best baseline); Qwen3-8B medium group 24.09 -> 27.56 Avg@3, 35.73 -> 39.73 Pass@3. High-resource is "competitive", not better: 4B high-resource Avg@3 26.20 vs OPSD 26.93; Pass@3 36.80 vs 38.40.
- Ablation (1.7B, Avg@3): COPSD 9.95 -> teachable prefix, no filter 10.76 -> failed-recovery only 10.21 -> successful-recovery only 11.60. Training on failed-recovery prefixes is worse than no filter: the verifier carries real signal (+0.84 on top of selection).
- English AIME (Qwen3-4B, 500 OpenThoughts problems, 160 steps), Avg@3 / Pass@3: AIME24 76.67/90.00 (base 76.67/80.00, OPSD 76.67/86.67); AIME25 71.11/86.67 (base 64.44/76.67, OPSD 67.78/83.33). Only 30 problems per benchmark, so differences are a few problems.

## Caveats

- Absolute numbers are low (1.7B Overall Avg@3 11.6%; Swahili/Telugu 1-8%), and gains are 1-3 pp from a small PolyMath High split (several languages with 0.27-pp granularity, 3 samples). No seeds or variance; one run per cell.
- Math only, Qwen3 only, English reference solutions required as privileged info. Gains for 4B are small (+1.07) and the ordering OPSD vs COPSD flips across scales, so differences between baselines are within noise.
- Selection uses a hard threshold ($\tau$, $K$) with no sensitivity study in the main text; verification needs ground-truth answers (outcome verifier), so this is not label-free, and it adds long greedy teacher rollouts per trajectory.
- Never says whether the "supervise only 7-10% of tokens" result is a sparse-selection effect (cf. fork-token work) or specifically a teacher-reliability effect; no control with a random/early fixed-length cutoff is reported.

## Thesis relevance

- Direct evidence that a privileged self-teacher is position-dependent: its value decays as the student prefix accumulates errors. For the single-sample setting this argues for gating or truncating dense teacher supervision on the early, still-recoverable part of a rollout, and for a recoverability check (cheap with one sample, expensive at scale).
- Sits with the verify-before-distill thread: [[research/teacher-student-rl/tgopd-verify-before-distill]] gates on a verified teacher; TOPSD gates per trajectory on teacher recoverability from the student's own prefix, using a ground-truth verifier.
- Bears on [[conflicts/adrs-vs-opsd-compaction]]: the teacher can only add information while it stays outside the student's error basin; once it follows the student it merely reinforces existing (wrong) behaviour, consistent with OPSD being limited to what the student can already reach. Weakly supports the "compaction" side; the observed gains still come from teacher guidance on early prefixes, not new capability.
- Mild relevance to [[conflicts/opsa-vs-opd-pattern-transfer]]: teacher drift (teacher mimics student) is the extreme case of the teacher signal collapsing into the student's own distribution.

## Source

- `raw/research/weekly-2026-11-13/03-topsd-teachable-prefixes.md` (arXiv:2611.08179, https://arxiv.org/abs/2611.08179); main text and Appendix A read; appendices B-D (extra method detail, per-language results, qualitative examples) only skimmed.

## Related

- [[../weekly-briefs/2026-11-13]] — brought in by the 2026-11-13 weekly sweep
- [[research/teacher-student-rl/privileged-info-opsd]] — OPSD with reference-conditioned teacher (the base method)
- [[research/teacher-student-rl/tgopd-verify-before-distill]] — verified-teacher gating
- [[research/teacher-student-rl/gift-gradient-informed-filtering]] — OPSD token filtering
- [[research/teacher-student-rl/esr-early-stopping-opd]] — truncating OPD rollouts early
- [[research/teacher-student-rl/ier-gradient-reliability-opd]] — gradient reliability in OPD
- [[research/teacher-student-rl/ida-opd-entropy-influence]]
- [[research/teacher-student-rl/opsd-compresses-rlvr]] — compaction vs capability
- [[research/teacher-student-rl/wisd-weakening-induced-opsd]] — alternative OPSD variant without privileged context
- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]]
- [[research/teacher-student-rl/bsd-bridged-self-distillation]]
- [[research/teacher-student-rl/one-shot-opd]]
- [[research/rlvr-mechanics/high-entropy-minority-tokens]] — sparse token selection
- [[research/teacher-student-rl/_overview]]
- [[conflicts/adrs-vs-opsd-compaction]]
- [[conflicts/opsa-vs-opd-pattern-transfer]]
