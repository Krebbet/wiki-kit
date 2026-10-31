# What Outcome RL Buys: Finishing, Reliability, Rarely Reach (Yang)

Budget-aware decomposition of pass@1 gains for 20 released outcome-RL thinking models (1.5B-32B) against their bases: $\Delta\text{pass@1}(B)=F+P+\text{reach}@k(B)$ (finishing, reliability, reach). At tight budgets (4k/8k) finishing is 82% of the change; where the base finishes, reliability rises in 16/16 recipes; net reach is at most 2.1 pp on every set. A small 8B probe finds supplying setup knowledge during RL does not beat plain RL. Strong evidence for the "RL = changed behaviour, not new knowledge" thesis plus an evaluation protocol. arXiv:2610.34894; code: github.com/shanyang-me/outcome-rl-buys.

Note: read from an ingest summary; appendices and tables 6-13 were not read.

## Method

- $F=\Delta\text{fin}\cdot\text{pass}_{RL}(B|\text{fin})$ (takes the cross term); $P=\text{fin}_{base}\cdot\Delta\text{pass}(B|\text{fin})$; reach = (base-unsolved problems RL solves) minus (RL-unsolved problems base solves), with "unsolved" = finishes all $k=8$ samples, all wrong (mirror term controls sampling noise). Robust reach requires the other model to solve in $\ge k/2$ samples.
- $k=8$, $T=0.6$, budgets 4k/8k/16k, training cap, and next budget above (up to 64k). Sets: physics (300 text problems), MATH-500, 276 recent contest problems. Predictions for 10 pairs pre-registered.
- Probe: Qwen3-VL-8B-Thinking, GSPO outcome RL on physics, 60 updates, five channels for supplying setup knowledge (prompt hint, teacher derivation, written sections, fine-tune question, setup reward).

## Results

| Finding | Number |
|---|---|
| Finishing share at 4k/8k | 82% [77,86] of change; $\rho=-0.93$ (length change vs finishing change); $\rho=0.97$ score change vs $F$ |
| Reliability (base finishes >= 93%) | rises 16/16; larger than $F$ in 14/16; matched reliability rises 16/16 (12 clear of 0) |
| Reach | <= 0.021 on every set; mean +0.003 |
| RL-only physics wins (144 checked) | 5 (3.5%) real; base already solves 85% of RL's solves |
| Blind step audit | 0/26 decisive RL steps absent from base samples (17/26 base states but does not carry through) |
| Base at 64k vs RL (4k-picked problems) | base 0.44 -> 0.80, RL 0.68 |
| 8B probe, plain RL held-out | 0.16 -> 0.26, gain is finishing; hint +0.01 [-0.01,0.03]; teacher derivation -0.05 [-0.08,-0.03] |
| Backtracking words ("wait") | halved by RL with matched reliability unchanged |

Reward works where it lands: revisiting 60 problems lifts their solve rate 0.10 -> 0.28 but moves neither the other 293 hard problems nor held-out.

## Limitations

- Thinking (distillation-widened) bases only; physics and math only; 8 samples/problem; strict answer matcher (12/40 reliability wins are answer-form only).
- One LM reads traces; 10-34% of gain on "base never right but some samples unfinished" problems counted as behaviour (conservative against reach; would lift ProRL v2 net reach to 0.067). ProRL v2 holds 2 of 5 real wins: a large-scale effect is not ruled out.
- Probe: 1 seed, 1 family, 1 domain, short training; cannot tell whether channels failed or supplied knowledge does not transfer this way. No decontamination check; some post-hoc adjustments.

## Thesis relevance

- Supports the Invisible Leash side of [[conflicts/invisible-leash-vs-spiral-transfer]] with a noise-controlled reach measure; pushes back on the boundary-extension reading of [[research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] (different metric and domain; partially reconcilable).
- Hint-channel null (+0.01 held-out) is a small-scale data point against hint-based knowledge installation in [[conflicts/knowrl-vs-rlt-hint-design]]; tension with [[research/rlvr-mechanics/curriculum-boundary-aware-rl]] (42% of base-unsolvable solved via teacher traces; different scale/domain).
- Measurement-validity lens for concept evaluation: control for finishing, answer form, and sampling noise. Evaluation-protocol suggestion (report fin@1(B); compare a recipe to its base at or above the training cap) is a candidate for the best-practices page, proposal only.

## Source

- `raw/research/weekly-2026-10-30/03-what-outcome-rl-buys.md` (arXiv:2610.34894, https://arxiv.org/abs/2610.34894)

## Related

- [[research/single-sample-rl-finetuning/_overview]]
- [[research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]]
- [[research/single-sample-rl-finetuning/1-shot-rlvr]] — finishing/length confound may explain part of tight-budget gains
- [[research/single-sample-rl-finetuning/deepseek-r1]]
- [[research/rlvr-mechanics/rlvr-ood-gain-answer-format]] — measurement artefacts inflate reported RL gain
- [[research/rlvr-mechanics/wait-marker-provenance]] — markers are not evidence of acquired reasoning
- [[research/rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[research/rlvr-mechanics/rlvr-pattern-selection-theory]]
- [[research/rlvr-mechanics/spurious-rewards-rlvr]]
- [[research/rlvr-mechanics/high-entropy-minority-tokens]]
- [[research/rlvr-mechanics/curriculum-boundary-aware-rl]]
- [[research/rlvr-mechanics/datpo-difficulty-adaptive-tree-rlvr]]
- [[research/rlvr-mechanics/es-broader-reasoning-coverage-grpo]] — method class where reach might be nonzero
- [[research/rlvr-mechanics/random-reward-reachability-probe]]
- [[research/rlvr-mechanics/thinking-leakage-no-think-rl]]
- [[research/rlvr-mechanics/context-grounding-mechanism-reuse]]
- [[research/teacher-student-rl/knowrl]]
- [[research/teacher-student-rl/opsd-compresses-rlvr]]
- [[research/synthesis/test-time-scaling]]
- [[research/synthesis/fine-tuning-best-practices]]
- [[research/concept-evaluation/_overview]]
- [[research/rlvr-mechanics/_overview]]
- [[conflicts/invisible-leash-vs-spiral-transfer]]
- [[conflicts/knowrl-vs-rlt-hint-design]]
- [[../weekly-briefs/2026-10-30]] — brought in by the 2026-10-30 weekly sweep
