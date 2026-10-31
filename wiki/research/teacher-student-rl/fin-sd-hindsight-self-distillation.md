# Fin-SD: Hint Scope Conditions for Hindsight Self-Distillation (Yu & Gorlla, CTGT/Berkeley)

Fin-SD adapts HINT-SD to single-CoT reasoning: the student localizes its own first faulty step, the trajectory is truncated there, and a frozen self-copy conditioned on a short hint supervises 100 on-policy tokens under reverse KL. The headline finding is an ablation result: most of the gain comes from where supervision is applied, not hint content or hint-writer strength. A generic placebo hint ("Your mistake is conceptual") matches the informative one. GPT-OSS-20B on FinanceReasoning Hard: +3.03 pp over base. arXiv:2610.36082 (ICAIF'26); code: github.com/johnnyhyu/fin-sd.

Note: read from an ingest summary; appendices were not read directly.

## Method

- Per epoch: re-freeze teacher $\phi\leftarrow\theta$; sample the student and judge vs ground truth to mine failures; hint model $\pi_H$ (frozen self, or GPT-OSS-120B) sees $(x,\tau,y^*)$ and returns $(k,h,\text{type})$: quote of the first faulty clause, a short critique, and type in {reasoning, arith_slip}. Arithmetic slips get no gradient.
- Student sees $[x;\tau_{<k}]$, teacher sees $[x;\tau_{<k};h]$. Loss: reverse KL over full vocab on $L=100$ rollout positions, teacher constant.
- LoRA r=64, lr 2e-5, 10 epochs. 220 synthetic problems; ~25 trained problems/epoch after failure mining.

## Results (FinanceReasoning Hard, 238 problems)

| Variant | Acc. | vs base 69.16 |
|---|---|---|
| Fin-SD | 72.19 (CI [0.31, 5.75] on delta) | +3.03 |
| Placebo hint | 72.52 | +3.36 |
| 120B writer, RKL / FKL | 72.19 / 71.26 (self FKL 70.93) | +3.03 / +2.10 |
| OPSD (full reference) | 70.42 (CI includes 0) | +1.26 |
| SFT | 62.46 | -6.70 |
| $L=8192$ rollout | -- | +1.93 (L=100 better by 1.09 in 4/5 seeds) |

Tokens: 508.5k vs OPSD 562.1k (-9.5%). MMLU-Pro 68.91 -> 68.34 (chemistry -5.47); FinTrust no large regression (single runs). Self-written hint equals 120B-written; reverse KL beats forward KL by ~1 pp.

## Limitations

- Most CIs wide and overlapping; Fin-SD vs OPSD vs ablations are not significantly separated.
- Placebo = full hint conflates "hint content irrelevant" with "any extra-context nudge suffices"; there is no truncation-only/no-hint control for the prefix itself.
- Writer-invariance likely holds only where the student can still diagnose its own errors; HINT-SD (4B student) reports the opposite. One 20B model, one domain, synthetic corpus built by frontier models; localization needs ground-truth answers.

## Thesis relevance

- Errors are dominated by "convention selection" (latent knowledge held but not selected), consistent with the reuse-not-installation framing; placebo equivalence implies no new concept content is transmitted.
- Third position in the hint-design debate ([[conflicts/knowrl-vs-rlt-hint-design]]): content barely matters once the site is localized. Another data point for [[conflicts/opsa-vs-opd-pattern-transfer]] (information content of teacher signal looks dispensable).
- Few-dozen-problem scale (~25/epoch) shows localized self-distillation can move a 20B model ~3 pp, though it is not a single-sample study.

## Source

- `raw/research/weekly-2026-10-30/02-fin-sd-hint-scope-conditions.md` (arXiv:2610.36082, https://arxiv.org/abs/2610.36082)

## Related

- [[research/teacher-student-rl/tapo-error-trajectory-distillation]] — also builds on own erroneous prefixes; claims diagnosis is the bottleneck
- [[research/process-reward-models/cliff-first-mistake-credit]] — first-mistake localization as GRPO advantage site
- [[research/teacher-student-rl/esr-early-stopping-opd]] — short rollouts suffice
- [[research/teacher-student-rl/opsd-compresses-rlvr]] — compaction-style token reduction
- [[research/teacher-student-rl/privileged-info-opsd]] — small, model-dependent value of privileged reference
- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]] — placebo-matches-hint resembles teacher-free matching OPD
- [[research/teacher-student-rl/rlcsd]] — hint self-distillation; wrong-hint control
- [[research/teacher-student-rl/knowrl]] — minimal-sufficient hint design presumes content matters
- [[research/teacher-student-rl/sgsd-skill-gated-distillation]]
- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]]
- [[research/teacher-student-rl/reverse-kl-distillation-guarantees]]
- [[research/teacher-student-rl/opd-skill-vs-knowledge-transfer]] — selection of latent knowledge vs new facts
- [[research/teacher-student-rl/bsd-bridged-self-distillation]] — frozen student copy with privileged context
- [[research/rlvr-mechanics/curriculum-boundary-aware-rl]] — failure-mined training sets with guided traces
- [[research/rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[research/rlvr-mechanics/rlvr-pattern-selection-theory]]
- [[research/catastrophic-forgetting/_overview]]
- [[research/teacher-student-rl/_overview]]
- [[conflicts/knowrl-vs-rlt-hint-design]]
- [[conflicts/opsa-vs-opd-pattern-transfer]]
- [[../weekly-briefs/2026-10-30]] — brought in by the 2026-10-30 weekly sweep
