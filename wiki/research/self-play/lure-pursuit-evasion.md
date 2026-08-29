---
name: lure-pursuit-evasion
description: LURE recasts zero-data LLM self-play as a pursuit-evasion game. An RL-trained evader/challenger positions tasks at the solver's capture frontier (p≈1/2) via a learned frontier-distance reward, rather than the post-hoc rejection filtering LURE attributes to R-Zero. A planner-executor pursuer/solver gets dense, verifier-derived process credit (terminal capture + monotone progress) instead of sparse terminal reward, and both sides are stabilized by round-anchored KL to per-round snapshots. Across three verifiable environments and three backbones it beats R-Zero and GRPO baselines while training on 4x more tasks at 80% of R-Zero's rollout cost; ablation shows removing the learned challenger costs more than any credit-shaping change. Self-reported audit finds R-Zero's ZebraLogic accuracy drops 68.0%→6.0% when a leaked gold answer is removed from a role-specific prompt.
type: research
---

# LURE: Pursuit-Evasion Self-Play for Zero-Data LLM Reasoning

Yu, Chen, Tan. *The Chase Is the Curriculum, the Capture Anchors the Credit: Pursuit-Evasion Self-Play for Zero-Data LLM Reasoning*. arXiv:2608.21871, August 2026. Reframes zero-data self-play as a cops-and-robbers pursuit-evasion game (Bonato 2011 lineage): an evader learns, via RL, to place tasks exactly at the solver's capture frontier, while a two-role pursuer (planner + executor) receives dense verifier-derived credit rather than a single sparse terminal signal. Both sides train with the same clipped-GRPO objective under a round-anchored KL trust region. Direct empirical and evaluation-integrity challenge to [[r-zero]].

## Method

**Three co-evolving policies**, all separate models trained with the identical clipped-GRPO + round-anchored-KL objective (Eq. 7), differing only in reward/advantage construction:

- **Evader $\pi_C$ (challenger).** Picks a difficulty $d \in [0,1]$ per environment. Reward is the *capture-frontier* reward:

$$\max_{\pi_C} \mathbb{E}_x\left[\min(p(x), 1-p(x)) - \rho(x)\right]$$

where $p(x) = \frac{1}{G}\sum_g \mathbb{1}[R(\tau_g) = 1]$ is the empirical pursuer capture rate over $G$ rollouts, and $\rho(x) = (n_{sig}(x)-1)/N$ is a difficulty-signature repetition penalty (coarse per-environment signature: hop count/population for QA, constraint count for IF, grid dimensions for logic). The reward peaks uniquely at $p=1/2$. **Theorem 1** proves $p=1/2$ is also the point of maximal group-normalized-advantage variance ($\sum_g A_g^2 = (G-1)\mathbb{1}[s(R)>0]$, expectation maximized at $p=1/2$) — the frontier reward and the point of maximal learning signal coincide by construction, not by tuning. **Proposition 2** rules out signature collapse (support size $k \geq 2$, $|m_s^\star - m_{s'}^\star| \leq 1/4$).

- **Pursuer (planner $\pi_{plan}$ + executor $\pi_{exec}$).** Per executor turn $t$, raw scalar reward:

$$r_t = R(\tau)\mathbb{1}[t=T_\tau] + \lambda(\Delta\phi_t - c_{red}\mathbb{1}[\Delta\phi_t=0])$$

— terminal capture $R \in \{0,1\}$ credited once on the last turn, plus a $\lambda$-weighted monotone verifier-progress increment $\Delta\phi_t \geq 0$ (best-so-far progress $\phi_t \in [0,1]$), minus a small redundancy cost $c_{red}$ charged only on zero-progress steps (kept off the progress term so shift-invariance of group-normalization can't cancel it). Standardized jointly over all executor turns across the $G$ rollouts of $x$: $A_t = z_{G(x)}(r_t)$. The planner gets separate credit, $r^{plan}(\tau) = \sum_i \Phi_i$ — the sum of stage potentials of the executor segments it governed, group-normalized with no terminal term — so the planner is judged on how far execution advanced, not on whether capture occurred.

- **Round-anchored KL stabilization.** Each round freezes snapshots $\bar\pi_C, \bar\pi_{plan}, \bar\pi_{exec}$; all sampling, the KL reference, and the proximal center use that frozen snapshot; one GRPO update per role per round ($\beta = 0.1$). Framed as "proximal co-evolution" — structurally a multi-agent PPO trust region re-anchored every round rather than fixed. Authors report format/mode collapse without this.

**Round loop (Algorithm 1).** Evader emits $K=48$ candidates/environment (8 slots × 6 samples) → generator instantiates tasks → pursuer attacks each surviving task with $G=8$ rollouts → verifier returns $R, \{\phi_t\}$ → evader/planner/executor buffers built → three simultaneous GRPO updates. 8 rounds total; verl-GRPO/FSDP-2; 16× RTX 6000 Pro 96GB; lr $5\times10^{-6}$; 1 PPO epoch/round.

**Zero-reward-barrier fix.** Under standard GRPO the group-normalized gradient vanishes whenever every rollout of a task fails — exactly the case for hard, self-generated tasks (Prakash and Buvanesh 2025, arXiv:2510.03971, "zero-reward barrier," not yet in wiki). LURE's dense process credit still varies within an all-fail group even when the terminal term is identically zero. **Proposition 3** formalizes that regression is never penalized (only zero credit), and capture always outranks non-capture, given $\lambda c_{red}(T_{max}-1) < 1$.

## Claims

- **Main results (Qwen2.5-7B-Instruct, unified model):** PhantomWiki SUCCESS 65.8% vs. R-Zero 50.8% (+15.0 pts) vs. GRPO 43.3% vs. Base 25.0%. ZebraLogic puzzle-acc 16.9% vs. R-Zero 14.2%. IFEval prompt-acc 61.2% vs. R-Zero 57.9% — though **Base** (63.0%) beats every trained method on IFEval, flagged explicitly by the authors as a failure case for self-play on this environment/backbone. Same ranking holds on Llama-3.1-8B-Instruct and Gemma-2-9B-it; a "specialist" (per-environment-trained) setting pushes LURE's PhantomWiki SUCCESS to 80.0%.
- **Ablation (Table 2):** removing the learned challenger costs the most of any single ablation (−10.6 mean pts) — more than any dense-credit term (−2.2 to −4.5) or stabilization term (−6.3 to −7.7). Curriculum placement dominates credit shaping in effect size.
- **Rollout budget (Table 4):** LURE trains on all 144/144 emitted tasks at 8 rollouts/task = 1152 rollouts/round. R-Zero spends 1152 probe rollouts filtering down to 36/144 tasks, then trains on those at 8 rollouts/task (288 rollouts) = 1440 rollouts total. LURE trains on 4x more tasks at 80% of R-Zero's total rollout budget.
- **Scaling (Fig. 5, 7B→72B, power-law fits):** IFEval gains only appear from 14B onward — Base wins at 7B. LURE's PhantomWiki margin over R-Zero diminishes at 72B. Most hyperparameter-sensitive to the KL coefficient $\beta$ and rollout group size $G$ (Fig. 3).
- **Curriculum dynamics (Fig. 4):** LURE actively lowers mean task difficulty toward the frontier over rounds while held-out success rises 27%→65.8%; R-Zero's difficulty distribution stays roughly fixed across rounds.
- **Evaluation-integrity audit (Table 3, self-reported):** R-Zero's previously reported ZebraLogic advantage was largely gold-answer leakage in a role-specific prompt, not genuine reasoning gain. Removing the leaked gold grid drops R-Zero's round-5 checkpoint accuracy from 68.0% to 6.0% (a 62-point drop). The authors note "leakage originates from a role-specific prompt rather than the benchmark answer key" — implying multi-role self-play evals need auditing of *all* role-conditioned prompts, not just the final-answer key. This directly undercuts R-Zero's headline ZebraLogic numbers as reported in that paper and as currently summarized on [[r-zero]] (which does not carry this caveat).
- **OOD transfer (Table 5, 9 held-out benchmarks across math/rule-based/relational families, raw single-shot prompt, no planner/executor scaffolding):** "No method shows consistent gains over Base across individual benchmarks" — in-domain improvements do not transfer uniformly. At the aggregate level LURE is the only trained method that improves over Base at all (+0.6 mean pts; GRPO −0.1, GRPO-Zero −1.0, R-Zero 0.0), and wins all three benchmark-family aggregates, but the authors themselves call this "modest and benchmark-dependent," not clean concept transfer.

## Why this is load-bearing

**Proposer-reward taxonomy.** A distinct (candidate twelfth) entry in the frontier-reward family cataloged in [[../synthesis/proposer-reward-shapes]] (R-Zero, SPICE, SQLM, Skill-Self-Play all peak near 50% solve rate) — LURE's distinguishing move is an RL-trained evader whose reward *is* the frontier distance $\min(p, 1-p)$, decoupling curriculum placement from any post-hoc filtering step, combined with a separately-innovated dense process-credit scheme on the solver side.

**Proposer-primacy corroboration.** The ablation result (removing the learned challenger costs −10.6 mean pts, the largest single effect, larger than any pursuer-side credit change) is independent evidence for the mechanistic claim on [[understanding-self-play]] that the proposer is the critical component and the solver mostly re-weights existing capability.

**Zero-reward-barrier connection.** Directly instantiates and formally addresses (Proposition 3) the all-rollouts-fail GRPO zero-gradient case (Prakash and Buvanesh 2025), the mirror image of the all-rollouts-succeed "mastered prompts" case in [[../../conflicts/mcpo-vs-dapo-mastered-prompts]] — both are faces of the same group-variance-collapse failure mode in GRPO-family methods.

**Eval-integrity precedent.** The self-reported ZebraLogic leakage audit (68.0%→6.0%) is a methodological warning that applies beyond this paper: role-specific prompts in multi-role self-play setups are an under-audited leakage surface, distinct from and easier to miss than answer-key leakage.

## Limitations

- No formal game-theoretic guarantee: the evader/pursuer objectives are "stated as a pair rather than a minimax and carrying no equilibrium or convergence claim" (authors' own framing).
- IFEval regression: uncorrected zero-shot Base beats every trained method on this environment/backbone — self-play doesn't help and may hurt here.
- OOD transfer is modest (+0.6 mean pts) and explicitly benchmark-dependent, not uniform generalization — closer to weak/no-transfer than to a strong concept-learning claim.
- Diminishing returns at scale: IFEval gains only emerge from 14B onward; LURE's margin over R-Zero shrinks at 72B on PhantomWiki.
- Heavier footprint: needs three separately-trained models (evader, planner, executor) versus single- or two-model self-play baselines (R-Zero, AZR); the paper does not report total compute versus R-Zero beyond the rollout-count table, so the rollout-budget win (80% of R-Zero's rollouts) may not translate into a compute or wall-clock win once three-model training/serving overhead is counted.
- Verifiability constraint inherited from the self-play family generally: depends on programmatic verifiers (PhantomWiki, IFEval, ZebraLogic); open-ended/subjective tasks are out of scope.

## Source

- `raw/research/weekly-2026-08-28/04-lure-pursuit-evasion-self-play.md`
- arXiv: https://arxiv.org/abs/2608.21871

## Related

- [[r-zero]] — LURE's direct baseline; capture-frontier reward $\min(p,1-p)$ is mathematically equivalent (up to scale) to R-Zero's own challenger reward $r=1-2|\hat p-1/2|$. LURE's related-work section characterizes R-Zero's challenger as pure post-hoc rejection filtering against a fixed hand-set band rather than as RL-trained frontier-seeking — **this characterization is disputed**; see [[../../conflicts/lure-vs-r-zero-challenger-mechanism]].
- [[_overview]] — self-play theme overview; candidate twelfth proposer-reward-shape entry, distinguished from the existing eleven by an adversarial pursuit-evasion framing rather than a cooperative co-evolution framing.
- [[../process-reward-models/_overview]] — capture-anchored dense process credit parallels PAV/CEDAR-GRPO group-normalized process rewards, though LURE derives its signal entirely from a programmatic verifier rather than a trained PRM.
- [[../teacher-student-rl/_overview]] — the planner-executor pursuer loosely maps onto the teacher-student axis map, though here both roles are co-trained rather than one being fixed/pretrained.
- [[../../conflicts/mcpo-vs-dapo-mastered-prompts]] — LURE's dense-credit fix for the all-rollouts-fail zero-reward barrier is the mirror image of this cluster's all-rollouts-succeed mastered-prompts case; both are GRPO group-variance-collapse failure modes.
- [[../synthesis/proposer-reward-shapes]] — LURE's capture-frontier reward as a candidate new row in the Goldilocks/frontier-reward comparison table.
- [[../../weekly-briefs/2026-08-28]] — brought in by the 2026-08-28 weekly sweep.
