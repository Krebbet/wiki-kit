# Let's Verify Step by Step

OpenAI's large-scale comparison of outcome- vs. process-supervised reward models on the MATH dataset, training a PRM from 800K human step-level labels (PRM800K). The process-supervised PRM (GPT-4 finetune) reaches 78.2% best-of-1860 on a 500-problem MATH subset, decisively beating ORM and majority voting at every N. Active learning over "convincing wrong-answer" solutions yields ~2.6x data efficiency. Notably reverses the [[process-outcome-feedback]] (Uesato et al.) finding that process and outcome supervision tie — attributed to (i) harder dataset, (ii) more human labels, (iii) more capable base.

## Method
- Generator: GPT-4 finetuned on filtered correct solutions to produce newline-delimited steps. Generator never RL'd; reward model is the sole object of study.
- Step-level labels: positive / negative / neutral (subtly misleading or harmless-but-useless). Labelers stop at first negative. Label budget: 800K steps, 75K solutions, 12K problems.
- PRM training: standard LM pipeline; predict label token after each step. Solution score = product of per-step P(positive). Neutrals treated as positive.
- ORM: trained on 100 uniform samples/problem with final-answer-checking labels. Single scalar at final token.
- Active learning: surface top-K "convincing wrong-answer" solutions per problem (rated highly by current PRM, but final answer wrong). Iteratively re-train.
- Small-scale ablation: large PRM acts as oracle to label data for small-scale PRMs/ORMs, removing confounds (label distribution, false positives from final-answer grading).

## Claims
- Best-of-1860 PRM = 78.2% on MATH-500 subset; gap over ORM and majority voting widens with N (Fig. 3).
- At small scale with PRM-large supervision, process supervision dominates both outcome variants across all data scales N=1..200 samples/problem (Fig. 4a).
- ORM supervised by PRM-large outperforms ORM supervised by final-answer-checking — false positives from final-answer grading hurt ORM (Fig. 4b).
- Active learning ≈ 2.6x more data efficient than uniform labelling (slope comparison, Fig. 4a).
- OOD: on 224 fresh AP/AMC problems, PRM 72.9% vs ORM 63.8% vs majority 61.3% (Table 1). Holds across difficulty quintiles (Appendix G).
- PRM advantage is largest on the hardest problems and remains positive even on the easiest (where ORM degrades with N due to adversarial best-of-N).

## Sample efficiency
- 800K step labels across 75K solutions / 12K problems is the headline budget — large by any standard.
- Active-learning multiplier ≈ 2.6x; ORM trained on 100 samples/problem (≈10x more solutions than PRM training set) still loses.
- Small-scale ablations show process supervision wins at every dataset scale tested (1–200 samples/problem), so the advantage is not contingent on the 800K scale.
- Compute: GPT-4 finetuning for both generator and PRM; specific FLOPs not reported. Inference cost dominated by best-of-N (1860 generations per test problem in headline number).

## Relevance to the project
Strongest empirical support to date for step-level credit assignment outperforming sparse outcome rewards on multi-step reasoning. Directly relevant to the "components of the concept" reward design: PRM800K demonstrates that humans labelling per-step correctness yields a strictly better gradient signal than terminal correctness, even when the latter is automatically verifiable. Two design hooks for the new method: (1) decompose a concept into orderable sub-claims so a reward model can credit partial progress; (2) actively surface "convincing wrong" rollouts for labelling rather than uniform sampling — the 2.6x efficiency gain matters at single-sample/few-sample budgets. Caveat: PRM800K-scale annotation is incompatible with the project's data-efficiency thesis, so [[math-shepherd]]-style automated step labels are likely the relevant operationalisation.

## Source
- arXiv: 2305.20050
- Raw markdown: `../../../raw/research/single-sample-llm-learning/16-C-1-lets-verify-step-by-step.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/C-1-lets-verify-step-by-step.pdf`

## Related
- [[math-shepherd]]
- [[process-outcome-feedback]]
- [[training-verifiers-gsm8k]]
- [[_overview]]
