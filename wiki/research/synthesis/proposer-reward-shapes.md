---
name: proposer-reward-shapes
description: Cross-method synthesis of six distinct proposer-reward shapes (Sukhbaatar / SOAR / SQLM / SPICE / SPELL / SPAG) — formal expressions, what each optimises for, source of signal, hypothesis, and how each could plug into the proposed-method's component C / D.
type: research
---

# Proposer Reward Shapes — Cross-Method Synthesis

*Editorial synthesis. Composes one finding from each of six papers in the corpus into a single comparison table. The composition is the project frame; each row traces to a specific source page.*

## Why this synthesis exists

[[../self-play/understanding-self-play]] (Chae, Alam, Rastogi 2025) finds that **the proposer is the critical component** in LLM self-play; the solver only re-weights base-model probability mass. If that finding holds, the central engineering decision in any self-play / asymmetric-curriculum method is *what reward shapes the proposer*. The corpus contains six distinct, non-substitutable answers. They commit to different hypotheses about what makes a question valuable.

This page is the dedicated comparison; the [[../self-play/_overview]] is the broader theme synthesis.

## The nine reward shapes

| # | Method | Reward formula | Optimised target | Signal source | Underlying hypothesis |
|---|---|---|---|---|---|
| 1 | [[../self-play/asymmetric-self-play]] (Sukhbaatar et al. ICLR 2018) | $R^A = \gamma \max(0, t_B - t_A)$ | Tasks Bob takes longer than Alice | Time asymmetry; environment dynamics | Tasks worth proposing are ones the solver finds *harder* than the proposer can demonstrate |
| 2 | [[../teacher-student-rl/soar-edge-of-learnability]] (Sundaram et al. 2026) | $R^T \propto \frac{d}{dt}[\text{success-rate}_\text{hard set}(\pi_S)]$ | Tasks where student is currently improving | Bilevel meta-RL; held-out hard set | Valuable questions accelerate learning, not just measure it |
| 3 | [[../self-play/sqlm]] (Chen et al. 2025) | $R_P = \mathbb{1}[0 < \lvert\{y_i : y_i = y_\text{maj}\}\rvert < N]$, $N=4$ | Questions neither all-solved nor all-failed | Solver's own majority vote; no labels | The frontier of competence is detectable from solver disagreement alone |
| 4 | [[../self-play/spice]] (Liu, Jin et al. 2025) | $r_C = \exp\!\left(-\frac{(\text{Var}(\{l_i\}) - 0.25)^2}{0.02}\right)$ | Reasoner pass-rate $\approx 50\%$ | Variance over correctness samples | The optimal training point is exactly $p \approx 0.5$ ([[../single-sample-rl-finetuning/data-efficiency-rft|DOTS Theorem 1]]) |
| 5 | [[../self-play/spell]] (Yang et al. 2025) | Independent Gaussian on Responder pass-rate, peak at $\bar{r}^{\text{res}} = 0.5$ | Question difficulty at responder's frontier | Verifier (third role) judgement | Difficulty is a separate signal from correctness; needs an independent verifier |
| 6 | [[../self-play/spag]] (Cheng et al. NeurIPS 2024) | ReST-style: train on episodes where attacker won (binary $r > \xi = 0$ filter) | Strategies that win the game | Game outcome via string-match | Winning trajectories already select for proposer quality; reward shaping is unnecessary |
| 7 | [[../self-play/azr]] (Zhao et al. NeurIPS 2025) | $r^\text{propose} = \begin{cases} 1 - \bar{r}^\text{solve} & \bar{r}^\text{solve} > 0 \\ 0 & \text{else} \end{cases}$ | Solvable-but-not-trivial code tasks | Code executor; solver's empirical pass-rate | Asymmetric Goldilocks: hard zero on impossible kills wasted compute; linear decay rewards calibrated difficulty. **No KL needed** under task-mode diversity (3 modes). |
| 8 | [[../self-play/r-zero]] (Huang et al. 2025) | $r = 1 - 2\lvert\hat{p} - \tfrac{1}{2}\rvert - \lambda \cdot \text{BLEU-cluster}$ | Solver pass-rate exactly 50% + diverse questions | Solver empirical accuracy (majority vote) + repetition penalty | Symmetric Goldilocks at $p=0.5$ with explicit diversity penalty. Authors claim **two-model split** is required (unified collapses) — see [[../../conflicts/unified-vs-two-model-self-play]]. |
| 9 | [[../self-play/language-self-play]] (2025) | $r^\text{Challenger} = \bar{V} - V(q_i) + \beta \cdot \text{quality}(q_i)$ | Questions harder than batch average + meeting quality bar | Solver's value baseline + reference-model quality score (0–7) | **General-sum** game (both players incentivised by joint quality) prevents adversarial collapse. Without quality term, Solver hacks by answering everything in Python. |

## Editorial commentary — what each commits to

**Shape 1 (Sukhbaatar) — Time asymmetry.** The most agnostic. It requires only that "doing" be an action sequence with a duration. No verifier, no topic structure, no presumed concept axis. **The hardest to translate to language** — there is no obvious linguistic analogue of $t_B - t_A$. Token count fails because length doesn't track difficulty in language; turn count is closer but still loose.

**Shape 2 (SOAR) — Improvement-rate.** The strongest signal for *escaping plateaus*. SOAR documents 0/128 → non-zero on a hard held-out set — the bilevel reward is what tells the teacher to keep generating questions on the part of the distribution where the student isn't yet learning. **Cost: requires bilevel infrastructure** (track student-checkpoint deltas) and a held-out hard set. The richest signal but the most expensive to instantiate.

**Shape 3 (SQLM) — Goldilocks.** The cheapest LLM-self-play signal in the corpus. Single-model, no labels, no held-out set, no verifier. Turns "is this question valuable" into "did the solver disagree with itself across $N$ samples". **Closest match to the wiki's "topic string = concept seed" frame.** Subtle failure mode: when $N$ is small ($N=4$), the gate fires for any question with intermediate $p \in (0, 1)$, but the gradient signal density is low (binary).

**Shape 4 (SPICE) — Variance-at-50%.** The most theoretically grounded. Matches DOTS Theorem 1 — the gradient variance peaks at $p = 0.5$ — directly. **Requires multiple correctness samples** (compute cost) but produces a continuous-valued reward that's strongest at the sweet spot. Crucially paired with structural information asymmetry (Reasoner doesn't see the source document).

**Shape 5 (SPELL) — Responder-frontier-Gaussian via third role.** Structurally similar to SPICE's variance reward but routes the difficulty signal through an explicit verifier (the third role) rather than direct correctness sampling. **The verifier is a learned head of the same model**; the question is whether the verifier-honesty problem makes this a better or worse choice than SPICE's direct sampling.

**Shape 6 (SPAG) — ReST winners-only.** The only purely-offline option. Episodes are filtered post-hoc; the model is reinforced only on traces where the attacker won. **Selection-pressure-as-reward.** Works because the game is competitive: a good attacker question implicitly survives only against a good defender, so winning attacker traces co-evolve with the model. **Limit:** the game must be genuinely zero-sum; there's no clear analogue for one-sided concept exercises.

**Shape 7 (AZR) — Asymmetric Goldilocks (cleanest single-formula).** $r^\text{propose} = 1 - \bar{r}^\text{solve}$ with hard zero at $\bar{r}^\text{solve} = 0$. Crucially **runs without KL leash** — the three task modes (deduction, abduction, induction) provide enough partition diversity that the proposer can't collapse to a trivial pattern. Code executor as ground-truth verifier makes $\bar{r}^\text{solve}$ cheap to compute. **Strongest empirical anchor in the family**: AZR-Coder-7B reaches +15pp OOD math from code-only training (zero curated math data).

**Shape 8 (R-Zero) — Symmetric Goldilocks with diversity penalty.** $1 - 2\lvert\hat{p} - 1/2\rvert$ peaks symmetrically at 50% solver accuracy; the BLEU-cluster repetition penalty is the explicit diversity term that no other shape carries. Authors claim **two independent base-LLM copies** are required — Appendix D ablation reports unified-model collapse after one iteration. **This claim is in conflict** with shapes 3, 4, 7, and 9 which all use unified models successfully — see [[../../conflicts/unified-vs-two-model-self-play]] for the resolution-via-stabiliser-presence reading.

**Shape 9 (LSP) — Frontier-relative + general-sum quality stabiliser.** $\bar{V} - V(q_i)$ tracks "harder than the batch average" without committing to a fixed difficulty target — the frontier auto-translates as the solver improves. The added reference-model quality score (0–7) is the **explicit collapse-prevention mechanism**: by giving both players a stake in joint quality, the game becomes general-sum and the trivial-collapse equilibrium is no longer Nash-stable. **Without this stabiliser, the Solver hacks by answering everything in Python** (paper's own ablation). LSP is the cleanest demonstration that *stabiliser presence*, not architectural separation, is the load-bearing axis for unified-model self-play.

## How they could plug into [[proposed-method]]

Three places in the wiki's proposed reference-grounded single-sample concept fine-tuning method need a proposer-style signal:

1. **Component C (reference-in-context during gradient steps)** — should the reference text be *removed* during the gradient step (structural asymmetry, [[../self-play/spice]] template) or kept with $r^{KL}$ leakage penalty ([[../teacher-student-rl/sakana-rlt]] template)? **Locked 2026-05-01: structural asymmetry** — Reasoner does not see the reference during the gradient step (Challenger/teacher does); RLT $r^{KL}$ regulariser dropped from the default loss. See [[proposed-method]] gap §4 and memory `feedback_self_play_design_choices`. (Corrected 2026-05-16; previously mislabelled "Open. Decision pending".)
2. **Component G (diversity injection)** — the existing component just sets group size $G > 1$ and an entropy bonus. None of the six reward shapes here address diversity directly, but [[../self-play/sqlm]]'s Goldilocks gate *implies* a diversity floor ($N=4$ samples must disagree to pass). Could be incorporated.
3. **Sibling-set construction (component V)** — siblings are currently LLM-generated, audited (Phase-0 lock per [[recursive-concept-learning]]). A SPAG-style winners-only filter on the sibling-generation rollouts is a candidate refinement: keep only siblings where the teacher-as-attacker successfully induces the student-as-defender to fail.

For the *outer-loop* curriculum decision in [[recursive-concept-learning]] — "which concept to train next" — the SOAR improvement-rate reward (#2) is the natural fit. SQLM's Goldilocks (#3) is a cheaper substitute when bilevel infrastructure is unavailable.

## Recommendation for Phase-0

Phase-0 of [[recursive-concept-learning]] (modular multiplication, single concept, no recursion) does not need any of these — the inner loop uses RLT-style $r^{SS} - \lambda r^{KL}$. But Phase 1 (3-node DAG) and Phase 2 (verifier-independence) introduce decisions where these reward shapes become live:

- **Phase 1, child-select within the recursion:** SOAR-style improvement-rate is well-motivated.
- **Phase 1, sibling generation:** SQLM-style Goldilocks gate as a cheap quality filter.
- **Phase 2, verifier independence:** SPELL-style three-role decomposition (separating the verifier-A1 deliverable from the existing $V$).

## Source

Editorial composition. All formulas, claims, and findings trace to:
- [[../self-play/asymmetric-self-play]]
- [[../teacher-student-rl/soar-edge-of-learnability]]
- [[../self-play/sqlm]]
- [[../self-play/spice]]
- [[../self-play/spell]]
- [[../self-play/spag]]
- [[../self-play/azr]] — shape 7 (asymmetric Goldilocks)
- [[../self-play/r-zero]] — shape 8 (symmetric Goldilocks + diversity)
- [[../self-play/language-self-play]] — shape 9 (general-sum quality stabiliser)
- [[../self-play/understanding-self-play]] (mechanistic motivation)
- [[../self-play/info-gain-self-play]] (epiplexity criterion — what unifies these shapes)
- [[../single-sample-rl-finetuning/data-efficiency-rft]] (DOTS Theorem 1 grounding for shape #4)

## Related

- [[../self-play/_overview]] — broader theme synthesis
- [[proposed-method]] — where these reward shapes plug in (components C, G, V)
- [[recursive-concept-learning]] — outer-loop curriculum reward question
- [[single-sample-concept-skeleton]] — earliest synthesis; predates this comparison
- [[../../conflicts/unified-vs-two-model-self-play]] — stabiliser-vs-architecture resolution candidate
