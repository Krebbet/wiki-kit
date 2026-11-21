# RL Reinforces Only What It Sees Succeed: Successful-Group Count Predicts Take-Off (Sanchez-Corcuera et al.)

Synthetic-world study (nanoGPT models of 1.3M-85M parameters trained from scratch on Bayesian-player puzzle games, then GRPO) showing that outcome-reward RL converts hedging into decisions only for actions it sees succeed. Whether a rare action "takes off" is predicted before RL by $D_{rep}$, the expected number of sampled groups containing at least one winning use of that action: about 10/35/80 groups give 10%/50%/90% take-off over 400 runs. Below threshold RL sharpens the prior (and can make the rare action rarer); above it RL discovers a rule-general skill that transfers to rules never tried. Budget (repeats, continued runs) buys reach; larger groups at fixed attempts and restarts from base hurt. arXiv:2611.26084.

Note: read from the structured summary plus targeted slices of the raw source; Appendix C (OLMo-3-7B check) did not run RL.

## Method

- World: room with 1-3 obstacles; each has default tool D (works 80%) and alternative A. In the "changed world" D never works and A does; failures are uninformative. Ideal belief after $k$ failures that the world changed: $\pi(k)=\nu/(\nu+(1-\nu)\,0.2^k)$; switching is optimal once $\pi(k)>\tau=(1-\epsilon)/(2-\epsilon)\approx0.44$.
- Models: nanoGPT 6L/10.7M (also 1.3M, 85M), 1 pass on 9M scripted Bayesian-player games. Knobs: exposure (900/9k/90k games), reliability $\nu\in\{0.05,0.3\}$, rarity $\rho$ (1 in 23 down to 1 in 23,000 decisions). Switch probability $s(k)=p(A)/(p(A)+p(D))$ scored exactly by teacher forcing against $\pi(k)$.
- RL: GRPO, no KL, no std-normalisation (Dr.GRPO-style), one gradient step per batch (ratio 1, no clipping), AdamW lr 3e-5, 200 steps x 512 attempts, group size $N\in[4,256]$, step limit set so the post-failure decision is the last chance. Outcome reward = 1 on exit within the limit. Exploration is plain temperature-1 sampling.
- Take-off: more than half of 9 test rules gain >0.05 switch probability. Law (cloglog):
$$P_{\text{take-off}}=1-\exp\!\big(-\exp(b_0+b_1\log_{10}D_{rep})\big),\quad b_0=-5.75,\ b_1=3.47,$$
$$D_{rep}=\sum_i r\,\big(1-(1-q_i)^N\big),$$
with $r$ repeats of problem $i$ and $q_i$ the base-model reach (probability a sampled attempt uses the winning switch), estimated by an unbiased exact estimator. Mechanism: GRPO group-mean baseline gives zero advantage to all-fail and all-succeed groups, so learning needs a group with at least one attempt that both uses the action and wins.

## Key claims

1. Base models hedge like their corpus: within 2 pp of $\pi(k)$, tracking reliability (95% of posterior gap) and evidence count.
2. RL makes agents decisive, not stubborn: moves toward the reward-optimal choice in both directions (22% -> 10% switch after one failure on a reliable rule; 56% -> 77% after two). Closes 74-95% of held-out reward gap; calibration worsens, so not a better Bayesian.
3. Rare switch (1 in 232 or rarer): no run of 90 learns it; RL removes 25-50% of the default-tool's competitor mass, making the action rarer.
4. All-or-nothing: of 210 runs, 138 learn no rule, 53 learn all nine, 19 partial. A taken-off run applies a general "switch after default fails" skill, even to rules where the alternative was never tried (one rule +93 pp).
5. Count wins: counting attempts ($D_{att}$) or distinct problems ($D_{prob}$) fails to predict; $D_{rep}$ does, including across 12 recipe changes (910 runs; at least 12 log-lik points better).
6. Rarity is budget: at 1 in 232, 4x budget gives 15/20 take-offs vs 15.1 predicted; about 40x budget at 10x rarer.

## Results

| Lever | Outcome |
|---|---|
| Repeat same 400 problems 8x | take-offs 1/10 -> 10/10 (a repeat is a new group) |
| 32-64 repeats of a pool | 10/10 vs about 6 predicted (count is a lower bound: success probability rises 6x on repeated, 2.5x on unseen held-out problems; 0.7x without repeats) |
| Group size at fixed attempts | N=4 or 16: 9/10; N=64: 3/10; N=256: 1/10 |
| Restart from base (1/2/4/8 restarts) | 9/7/5/3 of 10 |
| Continue a failed run | 21/30 take off |

Recipe cost in extra successful groups needed (threshold multiplier): lr 4x lower x2.6; SGD x2.2; KL $\beta=1$ x1.5; std-normalised advantage x1.4; 85M model x1.1; no clipping x1.0.

## Limitations

- Synthetic, templated world; models at most 85M; one conflict type (switch after own failures); behavioural evidence only, no mechanistic account of the all-or-nothing behaviour (induction-head/grokking analogies untested).
- 35-group threshold is specific to world and recipe; the cross-recipe fit interpolates but fails to extrapolate (lower lr, new sizes).
- GRPO-family without reference model only; law rests on zero-advantage structure, so it may not carry to critic-based or dense-reward methods. Step limit makes reward sparse and may exaggerate rarity; rarity is confounded with late-player presence in filler rules.
- OLMo-3-7B check could not run RL (60% win rate in normal world; plays whole games poorly).

## What it means for our thesis

- Single-sample RL: repeating one problem generates many groups, so $D_{rep}$ scales linearly in repeats. This supports the multi-epoch-on-one-example regime and says the pre-RL quantity to measure is the base model's reach $q$ on the target behaviour, not data diversity.
- Design guidance: repeat a small pool (new group each time, no memorisation penalty observed on held-out problems); continue a stalled run rather than restart; prefer smaller groups at a fixed attempt budget; avoid raising lr-lowering/KL/std-normalisation costs without paying budget (x1.4-2.6).
- Concept learning: take-off yields a shared, rule-general skill rather than a per-rule patch, consistent with concept-based fine-tuning aims; but evidence is cross-rule transfer in templates only.
- Practical diagnostic: estimate $q$ by sampling before RL; if expected successful groups is well under about 35, RL will sharpen the prior (possibly suppress the target) and teacher injection or reach-raising exploration is needed.

## Conflicts

- Tension/extension with [[research/self-play/invisible-leash]] and [[research/self-play/yue-rlvr-boundary]]: those say RLVR only reweights base mass; here "only sharpens" is a regime (below threshold), and RL discovers the action above it, with 4-8x budget. Gives a regime-dependent reconciliation; see [[conflicts/invisible-leash-vs-spiral-transfer]]. Caveat: tiny synthetic world, and the discovered action had non-zero base probability.
- Tension with [[conflicts/mcpo-vs-dapo-mastered-prompts]]: repeating a small pool improves take-off with no generalisation cost here, whereas mastered-prompt collapse arguments favour avoiding repeats. Not a direct contradiction; worth checking at LLM scale.

## Source

- raw/research/weekly-2026-11-20/01-rl-reinforce-what-succeeds.md (arXiv:2611.26084)

## Related

- [[research/rlvr-mechanics/_overview]]
- [[research/self-play/yue-rlvr-boundary]]
- [[research/self-play/invisible-leash]]
- [[research/single-sample-rl-finetuning/_overview]]
- [[research/single-sample-rl-finetuning/1-shot-rlvr]]
- [[research/rlvr-mechanics/deepseekmath-grpo]]
- [[research/rlvr-mechanics/curriculum-boundary-aware-rl]]
- [[research/rlvr-mechanics/rlvr-pattern-selection-theory]]
- [[research/rlvr-mechanics/what-outcome-rl-buys]]
- [[research/rlvr-mechanics/random-reward-reachability-probe]]
- [[research/rlvr-mechanics/datpo-difficulty-adaptive-tree-rlvr]]
- [[research/rlvr-mechanics/dense-rewards-grpo-matched-compute]]
- [[research/rl-optimizers/dr-grpo]]
- [[research/rl-optimizers/dapo]]
- [[research/concept-learning/_overview]]
- [[conflicts/invisible-leash-vs-spiral-transfer]]
- [[conflicts/mcpo-vs-dapo-mastered-prompts]]
- [[../weekly-briefs/2026-11-20]] — brought in by the 2026-11-20 weekly sweep
