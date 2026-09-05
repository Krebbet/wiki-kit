# PAC: Progress-Augmented Advantage Curriculum for Multi-Task Reinforcement Learning of LLMs

Yu, Zheng, Zhang, Xu, Ma, Zhu, Liu, Deng, Dong, Zhu, and Huang (Alibaba Group, Hangzhou, China), arXiv:2608.30528. The paper proposes PAC, an online Bayesian curriculum controller for multi-task GRPO post-training: instead of sampling training tasks uniformly at random or from a fixed hand-designed schedule, PAC uses Thompson Sampling over a per-task posterior that fuses two signals — how much a task's gradient is still moving the policy (advantage magnitude) and whether that movement is actually converting into reward gains (reward trend) — to keep allocating rollout budget toward the tasks currently worth training on.

## Method

PAC casts task selection in multi-task GRPO as a non-stationary multi-armed bandit, with arms = task datasets $D_1,\dots,D_N$ (e.g., different difficulty levels or different domains such as math/code/logic). Two online per-task signals are computed from training telemetry:

- **Advantage-derived learnability** $s_i^{(adv)}$: a windowed mean of the absolute group-normalized GRPO advantage for task $i$ (Eq. 5) — a proxy for the magnitude of policy update the task can still induce.
- **Reward-derived progress** $s_i^{(prog)}$: the normalized slope of a least-squares linear fit of windowed mean task reward vs. training step (Eq. 6–7) — whether performance on the task is actually trending upward, as opposed to just producing large but unproductive advantage.

These are motivated by a first-order Taylor decomposition of expected task-value gain into a magnitude factor times a conversion-rate factor (Eq. 3–4), and fused multiplicatively into a single utility:

$$u_i^{(t)} = (1+s_i^{(prog)})\cdot s_i^{(adv)} \quad \text{(Eq. 8)}$$

A **Bayesian Gaussian–Gaussian controller** maintains a posterior $v_i\sim\mathcal N(\mu_i,\sigma_i^2)$ per task, updated by a precision-weighted average keyed on relative recent sample count $\rho_i^{(t)}$ (Eq. 10). After every update, a **non-stationary variance-inflation** step $\sigma_i^2\leftarrow(\sigma_i^2)^++\delta^2$ (Eq. 11) prevents the posterior from collapsing, keeping the controller responsive as task utility drifts over training. Rollout batches are built by **sequential Thompson Sampling**: for each of $B$ slots, draw a sample $\tilde v_j\sim\mathcal N(\mu_j,\sigma_j^2)$ for every arm, pick $\arg\max_j\tilde v_j$, and sample a prompt from that task's dataset. Training begins with a $T_{cold}$-step uniform-sampling warm-up (posteriors are still updated but not yet used for selection) before Thompson Sampling takes over allocation (Algorithm 1). GRPO's own loss and group-normalized advantage computation are untouched — PAC only changes which task a rollout batch is drawn from.

## Claims

PAC reaches the final validation score of the strongest prior curriculum baseline using fewer rollout steps: roughly 1.3x/1.6x fewer steps for Qwen2.5-3B/7B vs. SEC in a multi-level (difficulty-split) setting, and roughly 1.2x/1.3x fewer steps for Qwen2.5-7B/32B vs. DUMP in a multi-domain setting. It also reaches a higher final average: +13.1%/+8.5% over SEC (multi-level, 3B/7B) and +6.2%/+1.9% over DUMP (multi-domain, 7B/32B). Baselines: ST (single-task reference), Random, SEC (Chen et al. 2025 — advantage-only Boltzmann bandit over task categories), DUMP (Wang et al. 2025 — advantage-only UCB distribution-level bandit). Benchmarks: multi-level uses Countdown/Zebra/ARC difficulty splits (Table 1, 500 steps); multi-domain uses MATH500/AMC/AIME24/BigCodeBench/K&K (Table 2, 400 steps). An ablation (Section 4.3) shows dropping the reward-derived progress term costs 9.5% (the dominant factor — without it, allocation over-invests in already-saturated arms like K&K logic), dropping advantage-derived learnability costs 3.0%, and replacing Thompson Sampling with a Boltzmann/softmax selector costs 4.2% (allocation over-concentrates without posterior-uncertainty-driven exploration). The paper also reports gains on held-out "extremely hard" splits disjoint from training splits, arguing this reflects more balanced transfer to harder problems rather than overfitting to one validation distribution.

## Sample efficiency

This is not a single-sample or few-shot method in the wiki's usual sense. PAC operates on large multi-task RL corpora (DAPO-Math-17k, Code-R1-12k, K&K puzzle splits, Countdown/Zebra/ARC splits) over 400–500 GRPO training steps with 3–9 task arms, and "sample efficiency" here refers strictly to fewer training steps/rollouts needed to reach a fixed validation score — not fewer labeled examples or fewer distinct concepts learned per example. It is a rollout-budget allocation layer sitting on top of standard on-policy GRPO training, orthogonal to the wiki's core single-sample/concept-acquisition question. No mechanistic or representational evidence of concept formation is offered; the closest analog is the cross-difficulty transfer result, which speaks to generalization breadth of the curriculum choice rather than depth of any single skill.

## Relevance to the project

PAC belongs to the wiki's curriculum-and-decomposition theme as a fifth entry in the multi-task/GRPO curriculum sub-cluster, alongside SCRL, METIS, E2H, and AdaBack. Its most direct connection is to [[e2h-curriculum-rl]]: PAC's own related-work section cites Parashar et al. 2026 (E2H) as an example of the fixed/hand-designed difficulty-schedule curricula it improves on, and frames such schedules as often transferring poorly across settings. PAC can be read as the online-adaptive, Thompson-Sampling counterpart to E2H's fixed Gaussian/cosine difficulty-fading schedule — same GRPO multi-task setting, but the task-mixing weights are learned online from advantage/reward telemetry rather than fixed in advance. More broadly, PAC is one instance of a recurring theme in this cluster: reallocating a fixed training-signal budget toward where it currently does the most good, whether at the level of whole task arms (PAC), subproblems within one hard problem (SCRL), or in-context task selection (METIS).

## Limitations

Authors' own: (1) validated only with dense, verifiable outcome rewards (math answer-checkers, symbolic K&K verifiers, unit-test execution); the linear-trend progress estimator (Eq. 6) is flagged as likely to break under sparser, noisier, process-level, or learned-reward-model signals, requiring a more robust estimator. (2) Posterior granularity is per-arm, tied to the task/domain split, so it cannot exploit within-arm diversity (e.g., a broad "math" arm spanning many difficulties); the largest arm count tested is nine, and prompt/instance-level extension is explicitly left open. (3) Empirical scope stops at Qwen2.5-32B and math/code/logic domains only — no instruction-following, dialogue, multilingual, or safety tasks, and no test against alternative GRPO advantage-normalization variants (DAPO, Dr. GRPO, GSPO).

Unstated: no wall-clock or compute overhead is reported for maintaining per-task Bayesian posteriors versus plain random or UCB sampling. Both the main results and the ablation average only 3 seeds. Sensitivity of the cold-start length $T_{cold}$ and the history window $W$ is deferred to an appendix not fully captured in the available source.

## Source

- `raw/research/weekly-2026-09-04/04-pac-progress-augmented-curriculum.md`
- arXiv: https://arxiv.org/abs/2608.30528

## Related

- [[e2h-curriculum-rl]] — PAC is the online-adaptive counterpart to E2H's fixed Gaussian/cosine fading schedule, same GRPO multi-task setting
- [[scrl-curriculum-credit-assignment]] — orthogonal granularity: SCRL decomposes a hard problem into verifiable subproblems, PAC reallocates rollout budget across whole task arms
- [[metis-curriculum-judgment]] — parallel solution to online task-utility estimation, different mechanism (explicit Bayesian controller vs. in-context calibration memory)
- [[_overview]] — candidate addition to the multi-task/GRPO curriculum sub-cluster alongside SCRL, METIS, E2H, AdaBack
- [[../rlvr-mechanics/deepseekmath-grpo]] — PAC is built directly on GRPO's group-normalized advantage and is explicitly complementary to GRPO-optimizer-level advances (DAPO, Dr. GRPO, GSPO) — it only changes the task-sampling distribution
- [[../../weekly-briefs/2026-09-04]] — brought in by the 2026-09-04 weekly sweep
