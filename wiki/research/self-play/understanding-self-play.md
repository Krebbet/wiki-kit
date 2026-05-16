---
name: understanding-self-play
description: Chae, Alam, Rastogi 2025 — mechanistic analysis of LLM self-play (AZR) showing the proposer is the critical component; the solver only re-weights base-model probability mass (Invisible Leash), and reward shaping for difficulty calibration adds nothing beyond what proposer training already achieves.
type: research
---

# Towards Understanding Self-Play for LLM Reasoning

Justin Yang Chae (University of Washington), Md Tanvirul Alam, Nidhi Rastogi (Rochester Institute of Technology). NeurIPS 2025 Workshop: Math-AI. arXiv:2510.27072. An ablation and dynamics analysis of the Absolute Zero Reasoner (AZR) framework, asking which component of LLM self-play actually drives improvement. Central finding: the proposer generates a diverse, progressively difficult curriculum that activates existing base-model capacity; the solver merely re-weights probability mass already present at initialisation. The paper formalises this via the "Invisible Leash" support-preservation theorem, measures entropy collapse, parameter-update sparsity, and curriculum difficulty evolution, and tests a $p \approx 0.5$ proposer reward variant that succeeds in R-Zero but fails in AZR.

## Method

**Framework.** Absolute Zero Reasoner (AZR): a single LLM acts simultaneously as proposer (generates coding tasks) and solver (solves them) over three task families — deductive, abductive, and inductive reasoning on coding triplets $(p, i, o)$. Training uses Task-Relative REINFORCE++ (TRR++) with separate baselines per task–role combination.

**Proposer reward (default AZR):**

$$r_{\text{propose}} = \begin{cases} 0 & \text{if } \bar{r}_{\text{solve}} \in \{0, 1\} \\ 1 - \bar{r}_{\text{solve}} & \text{otherwise} \end{cases}$$

Reward decreases linearly with solve rate, excluding trivial (always-solved) and impossible (never-solved) tasks.

**Proposer reward (RQ5 ablation — $p \approx 0.5$ peak):**

$$r_{\text{propose}} = \begin{cases} 0 & \text{if } \bar{r}_{\text{solve}} \in \{0, 1\} \\ 1 - 2\left|\bar{r}_{\text{solve}} - 0.5\right| & \text{otherwise} \end{cases}$$

**Invisible Leash bound (Theorem 1, Appendix C).** For any on-policy PPO-style update with $\gamma_t = 0$ and no off-policy mixing, support is preserved: $\text{supp}(\pi_t^S(\cdot \mid x)) \subseteq \text{supp}(q_0(\cdot \mid x))$ for all $t$. AZR sets $\gamma_t = 0$, so the solver cannot assign positive probability to solutions the base model assigned zero probability.

**Policy entropy definition:**

$$H(\pi_\theta, D) = -\mathbb{E}_{x \sim D,\, y \sim \pi_\theta}\left[\log \pi_\theta(y_t \mid y_{<t}, x)\right]$$

tracked for full model, proposer role, and solver role separately.

**Parameter update sparsity:**

$$S(\theta_0, \theta_1) := 1 - \frac{\|\theta_1 - \theta_0\|_0}{n}$$

compared across SFT, AZR (self-play), and RLVR checkpoints on identical base models (QWEN2.5-CODER-3B and 7B).

**Frozen-proposer ablation.** Proposer receives no PPO gradient updates; solver trains normally. Tests whether curriculum evolution requires trained proposer weights.

## Claims

| Finding | Evidence |
|---|---|
| Proposer is the critical component | Frozen-proposer variant retains higher entropy but loses curriculum progression; performance degrades |
| Solver is bounded by base model (Invisible Leash) | Pass@k: AZR improves small $k$ but base model matches or exceeds at large $k$; Theorem 1 formal proof |
| Proposer generates progressive difficulty | 800 deductive questions sampled across training: $\bar{r}_{\text{solve}}$ decreases and response length grows over iterations |
| Self-play has intermediate sparsity | AZR-CODER-7B ~45.7% sparse; SFT ~94–98%; RLVR ~3–7% |
| $p \approx 0.5$ proposer reward does not help in AZR | Reduced final validation accuracy by 2%; entropy dynamics unchanged vs. default reward |
| Proposer entropy stays higher than solver entropy | Role-decomposed entropy curves (Fig. 4): proposer consistently above solver throughout training |
| Both roles undergo entropy collapse | Decay rates vary by model size and proposer setup; frozen proposer slows collapse by reducing optimization pressure |

The $p \approx 0.5$ null result (RQ5) is particularly informative: Huang et al. used this reward successfully in R-Zero, but the mechanism there appears to be other system components rather than the difficulty-targeting reward per se. Difficulty calibration emerges organically from proposer training, not from reward shaping.

## Why this is load-bearing for single-sample concept learning

This is the **mechanistic-claim paper for the entire self-play family**. If the proposer-is-critical finding holds, it reshapes the design question from "how do we train a self-play system?" to "what prompts the proposer to generate questions that activate the concept in the solver's existing capacity?" The Invisible Leash bound formalises why you cannot expect self-play to teach a model something genuinely new; you can only extract latent capacity more efficiently. For a single-sample concept fine-tuning system, this is both a constraint and a design guide.

The direct implication: the primary engineering variable is proposer quality, not solver architecture or reward shaping. This provides mechanistic justification for the [[../curriculum-and-decomposition/auto-kc-generation]] direction — LLM-generated knowledge components are a proposer-side intervention, and this paper supplies the empirical and theoretical rationale for why that intervention is where leverage lives.

The frozen-proposer ablation also implies that static curricula (fixed decomposition trees, no gradient feedback to the proposer) leave performance on the table relative to curricula that evolve. A system that decomposes a concept into fixed sub-tasks and trains the solver on them is analogous to frozen-proposer AZR: it preserves entropy but cannot track the solver's improving frontier. Adaptive KC generation is the linguistic analogue of training the proposer.

The intermediate sparsity finding (~45.7% for 7B) raises an open question for single-sample regimes: self-play sits between dense SFT and very sparse RLVR, so it may have distinctive catastrophic-forgetting behaviour worth studying before deploying in low-data settings where preservation of prior knowledge matters.

The tension with [[spiral]] is worth flagging: SPIRAL reports non-trivial reasoning gains from game-trained self-play, which the Invisible Leash interpretation might seem to preclude. The reconciliation is that the Leash bounds *support*, not *probability mass redistribution within support* — there is headroom for substantial capability improvement even within the base model's support, and SPIRAL's transfer gains are consistent with activating latent capacity rather than generating genuinely novel reasoning. This tension is a candidate for `wiki/conflicts/`.

## Limitations

- Single framework (AZR) and two model sizes (3B and 7B); patterns may not hold in other self-play systems or at larger scales.
- All experiments on coding tasks (deduction, abduction, induction over Python triplets); generalization to math in natural language or science QA not tested.
- Frozen-proposer experiment only run at 3B; cross-scale conclusions about entropy comparison are limited.
- The $p \approx 0.5$ result is one data point; other proposer reward designs unexplored.
- Catastrophic forgetting with intermediate sparsity flagged as future work, not studied here.
- No entropy-collapse mitigation proposed; paper identifies the failure mode but does not solve it.

## Source

- `../../../raw/research/self-play-concept-learning/.ingest/10-understanding-self-play.md`
- `../../../raw/research/self-play-concept-learning/08-10-understanding-self-play.md`
- arXiv: https://arxiv.org/abs/2510.27072

## Related

- [[../curriculum-and-decomposition/auto-kc-generation]] — LLM-generated knowledge components are a proposer-side intervention; this paper is the mechanistic justification for why proposer quality determines outcomes
- [[../curriculum-and-decomposition/_overview]] — proposer = curriculum-generator; this paper is the empirical anchor for that identification
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — DOTS difficulty targeting at $p \approx 0.5$; RQ5 here provides a counterpoint (mechanism matters, not reward shape alone)
- [[../teacher-student-rl/soar-edge-of-learnability]] — learnability-edge / $p \approx 0.5$ connection; SOAR's student-improvement signal is a bilevel variant of the proposer curriculum
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — intermediate sparsity raises forgetting questions studied in this domain
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — RQ4 sparsity finding complements the sparse-subnetwork RL literature
- [[asymmetric-self-play]] — pre-LLM canonical proposer/solver template
- [[sqlm]] — LLM self-play analogue; proposer quality is the central design variable here too
- [[spice]] — self-play in concept space
- [[spag]] — game-as-reasoning-training
- [[spiral]] — transfer claim from game self-play; tension with Invisible Leash refined by [[two-stage-dynamic]]
- [[invisible-leash]] — the formal bound this paper operationalises (Theorem C.1: $\text{supp}(\pi_\theta) \subseteq \text{supp}(q)$)
- [[yue-rlvr-boundary]] — independent empirical foundation: pass@k inversion across 6 RLVR algorithms
- [[two-stage-dynamic]] — refines the proposer-is-everything frame: Stage-1 exploitation traps GRPO; Stage-2 exploration possible under entropy preservation
- [[azr]] — the self-play system this paper *studies*; three-mode reasoning + asymmetric Goldilocks
- [[info-gain-self-play]] — refines proposer-is-everything: proposer is necessary but not sufficient; must satisfy epiplexity criterion
- [[_overview]] — theme synthesis
