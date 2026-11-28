# RL Unlearns Corrupted SFT Reasoning (Misra, Vinod, Dai)

On OLMo-2-1B / GSM8K, GRPO run to saturation after SFT largely erases the damage from corrupted SFT traces across 361 corruption configurations. The headline that 8 synthetic "form-only" traces beat gold-trace SFT is reported but weakly supported. arXiv:2611.26756.

Note: written from the structured summary; no seeds or error bars anywhere in the paper.

## Setup

- SFT then GRPO on the full uncorrupted GSM8K train set (7473). 361 SFT configs: 6 error types × first/last equation × 3 trace/answer correctness combinations × 10 corruption ratios, plus gold. Errors propagate downstream.
- Form-only SFT: three-line addition-like traces, correct or corrupted, $N\in\{8,\dots,256\}$.
- Headline metric is pass@2.

## Results (pass@2)

| Init | SFT only | SFT + GRPO |
|---|---|---|
| Gold traces | 43.61 | 60.71 |
| 100% corrupted (aggregate) | 13.80 | near gold (aggregate deviation ≤0.5 pp; worst config −1.83 pp) |
| GRPO only | — | 35.00 |
| Form-only, best correct / corrupted | — | 69.82 / 69.30 |

SFT-only vs post-GRPO accuracy is uncorrelated across configs ($r\approx-0.06$ to $0.00$, all $p>0.05$).

## Reliability of the form-only claim (wiki assessment)

- At identical $N=8$, correct traces give 60.93 and corrupted 69.30; unexplained, suggests high variance.
- Best of six sizes per family, picked on the test set.
- No small-gold control ($N{=}8$–256 real traces, or early-stopped gold SFT), so "form beats reasoning" is not separated from "less SFT is better".
- GRPO-only pass@1 (22.0) equals the base model's (21.99) and its traces are poorly formatted under a strict `####` evaluator; that baseline likely measures missing output format.

Treat corruption recovery as the finding; treat form-only-beats-gold as unreplicated.

## Bearing on the thesis

Initialisation content matters little once outcome RL saturates on in-distribution data *(synthesis)*; consistent with SFT mainly supplying format. Not few-shot learning: RL still consumes 7473 labelled problems. No transfer or trace audit. A low correlation could also reflect range restriction after saturation.

## Source

- raw/research/weekly-2026-11-27/02-rl-unlearns-corrupted-sft.md (arXiv:2611.26756)

## Related

- [[_overview]]
- [[../single-sample-rl-finetuning/fest]]
- [[../selective-finetuning/lima]]
- [[rlvr-ood-gain-answer-format]]
- [[rethinking-rl-sparse-selection]]
- [[random-reward-reachability-probe]]
- [[revisql-verified-data-reward-shaping]] — contrast: reward-label noise is harmful there
- [[../data-efficient-survey/sft-rl-budget-allocation]]
- [[../../conflicts/fest-tuned-rl-vs-demonstration-necessity]]
- [[../../weekly-briefs/2026-11-27]] — brought in by the 2026-11-27 weekly sweep
