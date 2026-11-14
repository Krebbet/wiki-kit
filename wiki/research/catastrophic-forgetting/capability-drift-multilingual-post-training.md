# Capability Drift in Multilingual Post-Training (Saksena et al., Gnani.AI)

Case study of unrewarded-capability regression under GRPO in a 30B-A3B multilingual MoE. Two RL branches from one SFT checkpoint: the released branch (RL-BASE) gains +36.07 on MATH but loses 19.32 F1 on XQuAD-Indic (XQuAD-English +11.71 F1 under the same scorer). An independent sibling (RL-INDIC; Indic instruction-following environment, language and repetition shaping) recovers the Indic scores and keeps MATH but pays -10 to -14 points on HMMT, LiveCodeBench and MMLU-Pro and does not restore script compliance. A later judge-reward round collapses extraction on RL-INDIC (F1 50.44 -> 17.67); 20 steps of reward-free distillation from the earlier checkpoint restores most of it (47.13). 95% of the MATH gain is boxed-answer emission, not accuracy. arXiv:2611.15717; no code (RL-BASE released as gnani-evon-v3.3-30B-A3B, other checkpoints not).

Note: read the body, Appendix A and Tables 2-6 in full; Appendices B-H (full metric tables, estimator details, judge setup) were only skimmed via headings.

## Method

- Lineage: SFT-INIT (64% English / 36% Indic, native + romanized) -> RL-BASE (judged-answer math, JSON schema, tool-call workplace assistant, MCQ; 16 samples/prompt; no language/script/length term) and RL-INDIC (adds Indic IF env, language term on final answer, repetition penalty on whole generation, 9.9% English guardrail pool; 8 samples/prompt; advantage-divisor floor). Both leave-one-out baseline with Bessel-corrected std normalisation.
- Round 2: generative judge reward (helpfulness-style) from each branch, with and without an auxiliary reward bundle ("+"). Round 3: RL-OPD = on-policy distillation from RL-INDIC (teacher next-token distributions, no task reward), 20 steps.
- Dynamic sampling drops zero-variance groups, so realized env share $s_{eff,e}\propto s_{nom,e}\,p_{mixed,e}$ differs from the nominal mixture (not reconstructable from logs).
- Reward-differential audit: within mixed-script prompt groups, Latin-script answers earn +0.168 reward on average (driven by structured-output and workplace envs, which never require an Indic user-facing answer). Association only; sensitive to length filter and reward scale.
- MATH decomposition: $\Delta\text{acc}=\text{emission}\cdot\Delta\text{cond-acc}+\ldots$, splitting boxed-emission rate from accuracy given boxed.

## Results

| Finding | Number |
|---|---|
| RL-BASE vs SFT, MATH / XQuAD-Indic / XQuAD-En | +36.07 / -19.32 F1 / +11.71 F1 |
| Regression locus | Indic tasks that supply a passage (XQuAD-Indic, IndicQA, IndicIFEval-ground); FLORES-IN, CrossSum-IN improve; IFEval-Hindi -2 |
| RL-INDIC vs RL-BASE, 4 regressing Indic benchmarks | +11.24 to +26.95 (XQuAD EM 12.86 -> 32.00) |
| Same, costs | HMMT -10.41, AIME25 -8.96, LCB -13.06, MMLU-Pro -13.92, GPQA-D -4.99; MATH +2.00 |
| Script retention (translated IndicIFEval) | in-script 95.1% -> 84.6% under RL-INDIC despite higher task accuracy |
| MATH gain decomposition | boxed emission 55.2% -> 91.6%; acc given boxed 91.1 -> 92.6; emission = 33.13 of 34.80 pooled points (95.2%), cond. accuracy 4.0% |
| Judge round on RL-INDIC (XQuAD-Indic F1) | 50.44 -> 17.67 (EM 32.00 -> 1.91); English-language answers 8.7% -> 91.7%; median answer length up ~6-10x |
| Distillation round (no task reward) | F1 47.13 / EM 33.52; recovers most, not all; answers stay longer |
| Tool use (BFCL v4) | parallel-call categories near 0; multi-turn base 34.0 -> 58.0; TauBench telecom +26.90, SWE-bench Verified -10.60 |
| Provenance bug | comparing against the previous-epoch SFT endpoint flipped deltas (MMLU -0.78 -> +9.47; AIME25 +40.00 -> +1.46); caught only via recorded model path |

Judge reward sees the behaviour (reads whole answer) yet still erodes it: visibility is not protection. The judge round separates language from task shape: grounded Indic IF gains ~5 points while grounded Indic extraction loses two thirds of F1, so the effect tracks "prose a helpfulness judge likes", not language.

## Limitations

- Single seed, no per-item CIs (only the reward differential has a bootstrap interval); bundled recipe change (envs, rewards, group size, floor) so no reward term is isolated; reward-coverage account is a hypothesis, not established.
- Some comparisons pair evaluation campaigns run weeks apart with unrecovered harness versions; exact match changed to a more permissive grader after Aug 2026 (read on F1). BBQ is a bias diagnostic, not capability.
- MATH boxing decomposition is not semantic regrading; unboxed-correct answers untested. IndicIFEval-ground construction and XorQA passage presence unverified.
- Three-round trace is one branch, one benchmark, one language for the judge result; recovered student inherits teacher limits by construction and was scored on XQuAD-Indic only.

## Thesis relevance

- Forgetting here is not parameter-level interference from a new task but drift in behaviours the reward is silent on (language, script, extraction, answer form, tool-call batching). Rewards can be satisfied in the dominant-language slice and transfer asymmetrically; this is an evaluation-coverage warning for any single-example method: measure held-out capability classes, not only the rewarded one.
- Bears on [[conflicts/on-policy-forgetting-vs-lr-confound]]: both RL rounds are on-policy and still forget heavily, and a gap of this size (19 F1) with no matched SFT or LR control gives no clean evidence for either side; it shows on-policy data is not sufficient protection when the reward is blind to the capability. Reward-free on-policy distillation from an earlier checkpoint as the repair operation fits the anchoring/self-distillation line in [[research/catastrophic-forgetting/composing-cl-anchors-long-horizon]] and [[research/teacher-student-rl/sequential-opd-then-rl]].
- Reinforces the answer-format confound in [[research/rlvr-mechanics/rlvr-ood-gain-answer-format]] and the finishing/format share of RL gains in [[research/rlvr-mechanics/what-outcome-rl-buys]]: 95% of a +36 MATH gain is emission rate.
- Judge-reward collapse and checkpoint-provenance error are practical hazards for sequential adaptation; candidates for the best-practices page (track extraction/held-out classes across rounds; verify init checkpoint by recorded path), proposal only.

## Source

- `raw/research/weekly-2026-11-13/05-capability-drift-multilingual.md` (arXiv:2611.15717, https://arxiv.org/abs/2611.15717)

## Related

- [[research/catastrophic-forgetting/_overview]]
- [[research/catastrophic-forgetting/rls-razor]] — on-policy KL-minimal account; this paper is a counter-instance when reward is blind
- [[research/catastrophic-forgetting/rft-mitigates-forgetting]]
- [[research/catastrophic-forgetting/rft-data-perspective]]
- [[research/catastrophic-forgetting/empirical-forgetting]]
- [[research/catastrophic-forgetting/composing-cl-anchors-long-horizon]]
- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]]
- [[research/teacher-student-rl/sequential-opd-then-rl]]
- [[research/rlvr-mechanics/rlvr-ood-gain-answer-format]]
- [[research/rlvr-mechanics/what-outcome-rl-buys]]
- [[research/rlvr-mechanics/spurious-rewards-rlvr]]
- [[research/synthesis/fine-tuning-best-practices]]
- [[conflicts/on-policy-forgetting-vs-lr-confound]]
- [[../weekly-briefs/2026-11-13]] — brought in by the 2026-11-13 weekly sweep
