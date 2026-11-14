# Dense Rewards in GRPO at Matched Compute (Singh et al.)

Matched-compute protocol (equal generated tokens and equal training GPU-hours, preregistered, 1,668 runs on six small models) applied to two GRPO interventions. Dense Monte-Carlo process rewards lead outcome-only GRPO per update but lose 14.3 points at equal tokens (continuations are 91% of generated tokens) and 7.8 points at equal training time; no dense variant beats GRPO even given equal time. Prompt selection (train on prompts with predicted success nearest 1/2) gains 1.7 / 0.8 points on Qwen3-0.6B / Qwen2.5-1.5B, helps only where candidates are predicted to fail more often than not, and a retuned baseline (2x learning rate) comes within half a point. Strong evidence that dense credit is not worth its tokens at this scale, plus an evaluation protocol. arXiv:2611.13560; code: github.com/vicky157/grpo-validation.

Note: main text and appendix summaries (C.8, tables 3/4/10/12) were read; per-study appendix tables (S1-S35) and sections E-I were skimmed, not read line by line.

## Method

- GRPO advantage $A_g=(R_g-\bar R)/(\text{std}(R)+\epsilon)$; update $u=\sum_{g,h}c_{g,h}s_{g,h}$ with token credit $c_{g,h}$ and score $s_{g,h}=\nabla\log\pi$. Outcome-only: $c_{g,h}=A_g$, so the update lies in $V=\text{span}\{q_g\}$ (weighted sums of whole-completion scores). Dense reward: $c_{g,h}=A_g+w_{g,h}$, can leave $V$; only the out-of-$V$ part can beat completion reweighting to first order.
- Monte-Carlo reward: 5 cuts per completion (6 segments), $k$ continuations per cut estimate prefix value; segment credit = value change. At $k=4$: 91% of generated tokens, 50 updates vs 584 for GRPO at the same token budget $B$ (12.25M for Qwen2.5-1.5B; $B$ preregistered = tokens the $k=4$ reward uses in 48 iterations).
- Variants: $k=1,2,4$; VinePPO-style (value-difference advantage, 4 clipped steps/batch); continuation reuse (SPO-tree/TreeRL-style, trains on continuations); two learned critics (no continuations).
- Prompt selection: draw 24 candidates, ridge critic on end-of-prompt hidden state predicts success (one prefill, no generation), train on 6 nearest 1/2 plus 2 random. Controls: random choice of 8 of the 24; history filter (GRESO-like); level filter; DAPO dynamic sampling.
- Models: Qwen2.5-1.5B-Instruct (380 tok), Qwen3 0.6B/1.7B/4B non-thinking and Llama-3.2-1B/3B (768 tok). MATH numeric-answer problems, 200 held-out test problems, pass@1 over 8 samples at T=1, first eval at or after $B$, no checkpoint selection. Primary/secondary/exploratory labels, Holm correction, TOST equivalence (+-2 pts, +-1 in four studies), crossed bootstrap. Default vs strict (boxed-only) verifier to rule out format drift.
- Gradient tests: alignment (cosine of out-of-$V$ components with a reference gradient from separately sampled continuations) and efficiency $(\mathbb E\langle u,\hat h\rangle)^2/\mathbb E\|u\|^2$, relative to GRPO, per update and per generated token.

## Results

| Finding | Number |
|---|---|
| Equal-iteration study (greedy val, 14 seeds) | GRPO +5.6 [4.1,7.1]; MC reward with $\alpha\le1$ equivalent within 3 pts; $\alpha=5$ loses 12.4 [8.7,16.1] |
| $\alpha=5$ failure mode | alignment stays 0.969-1.000 while greedy acc 25% to 12%; entropy 0.21 to 0.58; KL ~30x low-weight runs |
| Gradient efficiency, $k=4$ | 1.56x GRPO per update, 0.145x [0.120,0.190] per generated token |
| MC reward vs GRPO at equal tokens (Qwen2.5-1.5B) | -14.3 [12.7,16.0] (n=5); -14.9 on 12 fresh seeds; Qwen3 0.6B/1.7B/4B -8.0/-9.1/-10.0; GSM8K -9.8; 768-tok -6.6 |
| At equal training time | -7.8 [6.8,8.8] (0.14 h vs 0.43 h to $B$ on H200) |
| Fewer continuations | $k=1$ -6.8, $k=2$ -11.2, $k=4$ -14.3 at equal tokens; at own training time $k=2$/$k=1$ trail 5.1/2.2 |
| Sample reuse (3-seed pilot) | +7.7 for MC reward, -5.9 for GRPO at matched tokens |
| Beyond $T_c$ (1.29 A100-h, 8 seeds, strict) | MC $k=4$ -3.3, continuation reuse -5.2; none of 4 variants better; closest two trail by 1.1 |
| Learned critics | trail GRPO by 1.2 and 0.7 at equal time; at most +0.7 per-token gain |
| Efficiency-to-accuracy extrapolation | predicts 35.9/31.9/27.5% for $k=1,2,4$; actual 34.3/29.9/26.3; overestimates all five rewards by 0.8-1.8 pts |
| Critic filter, Qwen3-0.6B | +1.7 [1.2,2.1] (54 seeds, 4 studies); replication +1.2 [0.5,1.9] on 24 fresh seeds |
| Critic filter, Qwen2.5-1.5B | +0.8 [0.4,1.1] (60 seeds); unseen MATH L3-5 +0.8 / +1.1; GSM8K +1.1 / +1.3 |
| Other four models | no significant gain |
| Random choice among same 24 | trails filter by 1.7 / 1.0 / 0.9; equivalent to GRPO within 2 pts |
| Filter at equal training time | +1.0 (0.6B), +0.5 (1.5B); scoring adds 9-14% time |
| Cheaper selectors | history filter +0.6 (36 seeds); critic adds early +1.9; level filter 0; DAPO dynamic sampling -1.8 [0.8,2.7] |
| When it helps | mean predicted candidate success 0.42/0.40 (helped) vs 0.54-0.70 (not); 5 of 6 preregistered tests held; aiming at $p^\star=0.25$ removes gain (-2.8, -1.0); L1-2 pool (0.79) no gain |
| Mixed-group share | filter raises it by 8-19 pts everywhere, but does not predict accuracy gain |
| Gain worth | peak +2.6 at 3B/16 tokens, 0.8 at $B$; reaches GRPO's final accuracy with 0.78 of tokens (0.85-0.87 of time); at 2B on Qwen3-0.6B +0.5 [-0.5,1.6], equivalent to 0 |
| Retuned baseline | 2x LR on Qwen3-0.6B: GRPO +1.9, equals filter within 2 pts; linear-decay LR from $2\times10^{-6}$: GRPO within 0.5 of filter |

## Limitations

- Small models (0.6B-4B), non-thinking, short completions (380/768 tokens), MATH-style numeric answers, about 50 updates at the matched budget; per-update dense-reward gains at long horizons, large models, or thinking regimes are not ruled out. A 43-run Qwen2.5-7B sweep and SmolLM3-3B/NuminaMath studies agree, but only single-seed Phi-4 pilots are positive.
- Monte-Carlo rewards are tested with fixed 5 cuts and small $k$; VinePPO's own recipe (9 rollouts/step, task-tuned models, KL-PPO) is not reproduced.
- Prompt-selection account was formed post hoc from five settings; one of six preregistered predictions failed (Llama-3.2-1B), and four of the five confirmations are predictions of no gain. Gains are small (1-2 points), the filter's equal-time lead is exploratory, and the efficiency extrapolation is a heuristic.
- Default-verifier runs drift away from boxing; strict-verifier studies control this but not all studies use it.

## Thesis relevance

- Cost-accounting lens for any single-sample method: a per-update or per-batch gain that spends tokens on extra rollouts (credit estimation, tree continuations) must be compared at equal generated tokens and GPU-hours. Directly relevant to token-heavy concept-learning loops (teacher continuations, verification rollouts).
- Supports the critic-free side of [[conflicts/sp3o-critic-repair-vs-critic-free-trend]] at small scale: learned critics ended at or below GRPO at equal time, dense Monte-Carlo credit lost badly. Does not test SP3O's critic-repair mechanism, so it is indirect.
- Bears on [[conflicts/mcpo-vs-dapo-mastered-prompts]]: DAPO-style dynamic sampling lost 1.8 points here and the share of informative (mixed) groups did not predict gains, undercutting the zero-advantage-groups-are-waste rationale (Position A). Different setting from MCPO's drift argument, which it neither confirms nor tests.
- Baseline-retuning result (2x LR nearly matches the selection gain) parallels [[conflicts/on-policy-forgetting-vs-lr-confound]]: apparent method gains can be learning-rate artefacts. Candidate checklist item for [[research/synthesis/fine-tuning-best-practices]] (state token/GPU-hour budgets, verifier, retuned baseline), proposal only.
- Selecting prompts the model fails more often than not echoes boundary-aware curricula ([[research/rlvr-mechanics/curriculum-boundary-aware-rl]]) but at a very small effect size.

## Source

- `raw/research/weekly-2026-11-13/02-dense-rewards-grpo-tokens.md` (arXiv:2611.13560, https://arxiv.org/abs/2611.13560; code github.com/vicky157/grpo-validation)

## Related

- [[research/rlvr-mechanics/_overview]]
- [[research/rlvr-mechanics/deepseekmath-grpo]]
- [[research/rlvr-mechanics/grpo-secretly-prm]] — GRPO already induces process-like credit; consistent with dense add-ons not paying
- [[research/rlvr-mechanics/ppo-critic-value-flattening]]
- [[research/rlvr-mechanics/what-outcome-rl-buys]] — another measurement-discipline paper on RL gain attribution
- [[research/rlvr-mechanics/curriculum-boundary-aware-rl]]
- [[research/rlvr-mechanics/datpo-difficulty-adaptive-tree-rlvr]] — tree rollouts; continuation cost
- [[research/rlvr-mechanics/flowtracer-attention-credit]]
- [[research/rlvr-mechanics/binary-rewards-rl-challenges]]
- [[research/rl-optimizers/dapo]]
- [[research/rl-optimizers/cue-grpo-rarity-credit]]
- [[research/teacher-student-rl/uecr-grpo-entropy-calibrated-credit]]
- [[research/process-reward-models/_overview]]
- [[research/process-reward-models/pav-rewarding-progress]]
- [[research/synthesis/fine-tuning-best-practices]]
- [[conflicts/sp3o-critic-repair-vs-critic-free-trend]]
- [[conflicts/mcpo-vs-dapo-mastered-prompts]]
- [[conflicts/on-policy-forgetting-vs-lr-confound]]
- [[../weekly-briefs/2026-11-13]] — brought in by the 2026-11-13 weekly sweep
