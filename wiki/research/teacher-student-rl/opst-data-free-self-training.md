# OPST: On-Policy Self-Training, Data-Free Self-Improvement (Sick et al., Google / Ulm)

OPST seeds a model with only coarse topic strings, has it synthesize questions plus privileged information (rationale + candidate answer), filters them (pseudo-verification, then a consensus gate), and trains by on-policy self-distillation from an EMA teacher conditioned on that synthetic privileged info. No human questions or answers. On Gemma 4 E2B (no-think) MMLU 37.5 -> 47.7 (+10.2), avg +7.3; beats SFT and GRPO on the same synthetic data. arXiv:2610.32770; no code.

Note: read from an ingest summary; appendices were not read directly.

## Method

- Per round: generator (EMA teacher or frozen init) writes $(x,z=(r,a))$ per topic; filter: generator must re-solve $x$ and a paraphrase without $z$ and recover $a$, then the student samples $G$ rollouts and the problem is discarded if 100% agree with $a$ (student already solves it) or it duplicates earlier rounds.
- Student rolls out $y\sim\pi_\theta(\cdot|x)$; teacher $\pi_\phi(\cdot|x,z,y_{<t})$ gives dense token targets; loss is skewed JSD ($\alpha=0.8$, mode-seeking, bounded). EMA $\beta=0.05$; returned model is the EMA teacher. Student never sees $z$. A visual variant uses unlabeled images with view-agreement verification.

## Results

| Result | Number |
|---|---|
| Gemma 4 E2B no-think | avg +7.3 (MMLU +10.2, GPQA +4.0, HellaSwag +7.5); with thinking 58.4 -> 63.0 |
| Vs same synthetic data (2B) | SFT +1.7, GRPO +1.0, OPST +7.3 avg |
| Vs no-reference methods | +1.0 to 2.8 over u-OPSD, +1.4 to 5.2 over R-Zero |
| Vs supervised OPSD | recovers 88% at 2B no-think (+7.3 of +8.3) |
| Qwen3-4B-Base | avg 66.7 -> 72.7 (GSM8K +13.3) |
| Scale | ~285 samples x 7 rounds (~2k problems) optimal; 57/round already 43.8; 570 saturates |

## Ablations

| Ablation (E2B MMLU) | Result |
|---|---|
| Privileged info: none / placebo (other problem, same topic) | 40.6 / 40.2 |
| answer-only / rationale-only / full | 44.6 / 45.8 / 47.7 |
| Filters: none / +verification / +gate | 42.7 -> 45.4 -> 47.7 (Table 5a, from 37.5 base) |
| 75% wrong candidate answers, no filters | -1.9 vs clean (still +3.3 over base); SFT -5.7 |
| EMA $\beta=1$ | no gain (38.1) |

Placebo ~ none means the gain stems from sample-specific privileged info; only ~3 of the 10.2 points are residual self-distillation toward the EMA teacher. Rationale carries more than answer.

## Limitations

- Authors: only amplifies existing knowledge; pseudo-verification measures self-consistency, not correctness; hand-chosen topics; small models.
- Topic seeds derived from eval-benchmark domains (distribution leakage); gains shrink under thinking on strong bases (MMLU +1.2); plateau after 7 rounds; MATH-500 regresses (-8.5 / -4.9 in mixtures); EMA teacher is evaluated (+1.8 over student); GRPO baseline may be weak (agreement-with-generated-answer reward); no N=1 or few-shot training.

## Thesis relevance

- Supports Position B of [[conflicts/opsa-vs-opd-pattern-transfer]]: real, sample-specific privileged content matters; teacher-free residual is small. Evidence for capability gain from OPSD (vs compaction) for [[conflicts/adrs-vs-opsd-compaction]], though the base lacks an RLVR stage, so contexts differ.
- Data-free alternative to proposer-reward self-play: dense self-distillation replaces scalar reward; the gate is a one-sided Goldilocks filter. "Amplifies existing knowledge" aligns with the support-bound claim in [[research/self-play/invisible-leash]].
- Noise robustness to wrong answers (dense context vs SFT) is a related result to [[research/rlvr-mechanics/wrong-votes-right-gradients]].

## Source

- `raw/research/weekly-2026-10-30/04-on-policy-self-training-data-free.md` (arXiv:2610.32770, https://arxiv.org/abs/2610.32770)

## Related

- [[research/teacher-student-rl/opsd-compresses-rlvr]]
- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]]
- [[research/teacher-student-rl/privileged-info-opsd]]
- [[research/teacher-student-rl/rlcsd]] — privilege-induced drift; OPST uses bounded JSD + EMA
- [[research/teacher-student-rl/sgsd-skill-gated-distillation]]
- [[research/teacher-student-rl/one-shot-opd]]
- [[research/teacher-student-rl/soar-edge-of-learnability]]
- [[research/teacher-student-rl/gift-gradient-informed-filtering]]
- [[research/teacher-student-rl/bsd-bridged-self-distillation]]
- [[research/self-play/sqlm]]
- [[research/self-play/r-zero]]
- [[research/self-play/azr]]
- [[research/self-play/understanding-self-play]]
- [[research/self-play/invisible-leash]]
- [[research/self-play/lure-pursuit-evasion]]
- [[research/single-sample-rl-finetuning/rlsc-self-confidence]]
- [[research/rlvr-mechanics/wrong-votes-right-gradients]]
- [[research/rlvr-mechanics/revisql-verified-data-reward-shaping]]
- [[research/rlvr-mechanics/spurious-rewards-rlvr]]
- [[research/catastrophic-forgetting/_overview]]
- [[research/self-improvement/_overview]]
- [[research/self-improvement/star]]
- [[research/test-time-training/tempo]]
- [[research/teacher-student-rl/_overview]]
- [[conflicts/opsa-vs-opd-pattern-transfer]]
- [[conflicts/adrs-vs-opsd-compaction]]
- [[../weekly-briefs/2026-10-30]] — brought in by the 2026-10-30 weekly sweep
