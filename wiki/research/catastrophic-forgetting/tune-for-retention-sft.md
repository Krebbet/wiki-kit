# Tune for Retention, Not Just Gain: SFT Forgets Far Less than You Think (Joshi, Srebro, Malach)

SFT configurations with near-equal new-task gain differ widely in forgetting. Selecting learning rate and batch size jointly on gain and retention makes off-policy SFT competitive with on-policy self-distillation fine-tuning (SDFT), challenging "on-policy is what enables retention". SDFT stays more lr-robust and clearly wins on one of three tasks. arXiv:2611.34579.

## Method

- Selection rule only. $\Delta L$ = new-task accuracy minus base; $\Delta R$ = mean prior-suite accuracy minus base. Pick $\arg\max\,\Delta L+\Delta R$ on validation, or max $\Delta L$ s.t. $-\Delta R\le\epsilon$.
- Qwen2.5-7B-Instruct; lr 5e-6 to 1e-4; bs 16/32/64; 2 epochs; 3 seeds. Tasks: SciKnowEval chemistry, ToolUse, MBE. SDFT gets 2× the candidate configs.

## Results

Similar gain, different forgetting (SFT, ToolUse): lr 1e-5/bs16 scores 66.32 with suite average 63.54; lr 5e-5/bs64 scores 67.35 with average 54.26.

Chen et al. settings, gain / prior-task change (pp):

| Setting | aggressive SFT | retuned SFT | GRPO (single config) |
|---|---|---|---|
| 8B MMLU | +9.34 / −33.00 | +12.13 / +0.55 | +11.95 / −1.22 |
| 8B IFEval | +22.56 / −25.92 | +18.16 / −1.60 | +21.39 / −1.97 |
| 1B MMLU | +4.32 / −24.00 | +6.23 / −2.72 | +8.65 / −0.09 |
| 1B IFEval | +26.25 / −20.77 | +24.61 / −3.88 | +21.60 / −0.26 |

Best gain under a ≤3 pp forgetting budget, SFT vs SDFT: Science 35.6 / 36.0; ToolUse 28.5 / 28.5; MBE **7.3 / 18.5**.

- Practical recipe: bs 16, binary-search lr downward if the drop exceeds 2 pp. A 3-benchmark retention triplet recovered full-suite selection on two held-out tasks (retrospective).
- Parameter drift ($\ell_1,\ell_2,\ell_\infty$) and new-task CE loss did not separate catastrophic from benign configs. KL to base not reported.

## Scope limits

- GRPO is not lr-swept and gain is not matched by design; no outcome-reward method is swept.
- lr and bs move together. $\Delta L+\Delta R$ weights one new task against a 9-task mean.
- MBE: SFT loses ~19 pp MATH vs ~2 pp for SDFT.
- ToolUse (97 items) selected and reported on the same set; its Table 7 SFT and SDFT scores are identical (69.76 ± 2.59), unverified.
- Selection needs access to prior-task evals. No few-shot setting.

## Bearing on the thesis

Any $R_w$ or selective-fine-tuning primitive in [[../synthesis/proposed-method]] should be compared against a retention-tuned plain SFT baseline *(synthesis)*. Evidence added to [[../../conflicts/on-policy-forgetting-vs-lr-confound]].

## Source

- raw/research/weekly-2026-11-27/03-tune-for-retention-sft.md (arXiv:2611.34579)

## Related

- [[_overview]]
- [[rls-razor]]
- [[rft-mitigates-forgetting]]
- [[rft-data-perspective]]
- [[empirical-forgetting]]
- [[../teacher-student-rl/opd-vs-offpolicy-kl-direction]]
- [[../selective-finetuning/deletion-tuning]]
- [[../rlvr-mechanics/dense-rewards-grpo-matched-compute]]
- [[../../conflicts/on-policy-forgetting-vs-lr-confound]]
- [[../../weekly-briefs/2026-11-27]] — brought in by the 2026-11-27 weekly sweep
