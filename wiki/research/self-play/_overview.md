---
name: self-play overview
description: Self-play and "play-with-the-concept" landscape — four subtrees (foundation, preference-alignment, reasoning-and-concept, RLVR-bound + zero-data), nine distinct proposer-reward shapes, the two-role vs three-role decomposition axis, structural-vs-soft information-asymmetry (decision locked: structural), and the Invisible-Leash mechanistic anchor refined to Stage-1-scoped per Two-Stage Dynamic View.
type: research
---

# Self-Play and Playing-with-the-Concept — Theme Overview

Nineteen sources organised around one question: *can a model improve by "playing with" a concept the way an agent improves by playing chess against itself?* The wiki frame is single-sample, concept-based fine-tuning of small LLMs. Self-play is foundational in games (clear rules, terminal verifier); transferring it to conceptual / open-ended domains is the design question.

## Four subtrees

| Subtree | Members | Frame |
|---|---|---|
| **Foundation** | [[alphazero]], [[asymmetric-self-play]], [[debate]] | Pre-LLM templates. AlphaZero is the closed-domain prototype (MCTS as policy-improvement oracle). [[asymmetric-self-play]] is **the canonical pre-LLM proposer/solver curriculum template** — Alice/Bob with $R^A = \gamma \max(0, t_B - t_A)$. Debate is an eval-time honesty game, not a train-time skill installer. |
| **Preference alignment** | [[spin]], [[sppo]] | Imitation / Nash-equilibrium against fixed reference (real data, fixed preference model). **Not load-bearing for concept learning** — no curriculum, no concept axis. Captured for citation completeness. |
| **Reasoning and concept** | [[spag]], [[sqlm]], [[spice]], [[spiral]], [[spell]], [[understanding-self-play]], [[rstar]] | LLM self-play whose proposer/solver mechanism either *embeds* a concept (Taboo target word, topic string, document) or *transfers* skill from games to reasoning. **rStar adds the test-time per-problem multiplier template.** The subtree of direct interest. |
| **RLVR-bound + zero-data** *(added 2026-05-01)* | [[invisible-leash]], [[yue-rlvr-boundary]], [[two-stage-dynamic]], [[azr]], [[r-zero]], [[language-self-play]], [[info-gain-self-play]] | The formal/empirical bounds on what RLVR-style self-play can do, plus the zero-data instances that test the bounds. Invisible-Leash and Yue establish Position A (solver only re-weights); Two-Stage Dynamic refines to Stage-1-scoped. AZR/R-Zero/LSP are the zero-data triple that operate within the bound. Info-Gain (epiplexity) is the engineering pre-flight test. |

The wiki has adjacent coverage that should be read in conjunction: [[../self-improvement/multi-turn-policy-verifier]] (PAG — single-LLM two-role precursor to SPELL), [[../teacher-student-rl/soar-edge-of-learnability]] (bilevel teacher-student-improvement-rate, the LLM-era analogue to Sukhbaatar), [[../curriculum-and-decomposition/poet]] (co-evolving environments + agents), [[../self-improvement/rstar-math]] (MCTS-LLM cousin of AlphaZero, successor to [[rstar]]), [[../self-improvement/self-rewarding-lm]] (LLM-as-judge sibling).

## The mechanistic anchor — Invisible Leash (refined 2026-05-01)

The user has chosen Position A (quality-optimization framing) per memory `feedback_self_play_design_choices.md`. This anchor has now been formalised and refined.

**Formal foundation.** [[invisible-leash]] proves Theorem C.1: $\text{supp}(\pi_\theta^{(t)}) \subseteq \text{supp}(q)$ for on-policy gradient updates — by induction. Cor C.2: $\limsup_k \text{pass@}k_{\pi_\theta} \leq \limsup_k \text{pass@}k_q$. The critical isolating result: SFT produces *positive* NSCR (+0.042 on Olympiad) while DAPO on the *same data* produces *negative* (−0.065). This isolates the bound to the RLVR objective, not the data.

**Empirical foundation.** [[yue-rlvr-boundary]] (Yue et al., >120 cites) tests six RLVR algorithms (PPO/GRPO/Reinforce++/RLOO/ReMax/DAPO) — all cluster within ~1.3 pts; all far from base-model upper bound. AIME24: **0% problems solved by RLVR but not by base.** Mode-sharpening confirmed by perplexity analysis. Distillation uniquely escapes the bound.

**Operational confirmation.** [[understanding-self-play]] reproduces the bound in self-play settings: the proposer is the critical component; solver only re-weights existing base-model probability mass. Frozen-proposer ablation kills curriculum evolution. The $p \approx 0.5$ reward-shaping trick that works for R-Zero fails for AZR — *the trained proposer*, not a reward heuristic, drives quality.

**Stage-1-scope refinement.** [[two-stage-dynamic]] (Yao et al., Oct 2025) — bounds the bound. Stage 1 (exploitation): $\mathbb{E}[\Delta z_v^l] \propto \pi^l(v)$ — gradient updates only flow to already-sampled tokens. Optimal-but-undersampled tokens get ~0 update. Standard GRPO stays here → Invisible Leash applies. Stage 2 (exploration): once high-reward tokens saturate ($1 - \pi \to 0$), suboptimal tokens occasionally get sampled and rise. **GRPO-N variant on Qwen2.5-Math-7B reaches Pass@256 = 100% on AMC2023, with held-out entropy *exceeding* the base model.** The transition is gated by training duration + entropy preservation.

**Practical implication.** Self-play's primary lever remains proposer quality (Stage-1 bound is sharp under standard short-training RLVR). But training duration and entropy preservation are now load-bearing hyperparameters — long-enough RL with explicit entropy preservation enters Stage 2 where genuine support expansion is possible. SPIRAL's transfer result is consistent with Stage-2 dynamics (game-self-play preserves entropy by construction).

**Engineering pre-flight test.** [[info-gain-self-play]] supplies the criterion: self-play evolves only when **epiplexity** $S_{C,T}(X)$ — the learnable fraction of MDL under bounded observer parameters $C$ and inference budget $T$ — rises monotonically across iterations. Reward improvement is *not* a sufficient signal. Algorithm 1 (prequential MDL audit) is the engineering check. **Induction epiplexity is 3–4× higher than abduction/deduction**, quantifying the AZR three-mode asymmetry.

The open conflict [[../../conflicts/invisible-leash-vs-spiral-transfer]] is now refined, not closed: Position A is Stage-1-scoped; SPIRAL's gains are consistent with Stage-2; the residual gap is whether opponent-adaptation in SPIRAL adds something beyond standard Stage-2 RLVR.

## Nine proposer-reward shapes — the practical synthesis

The "what proposer prompts the right question" engineering problem has at least nine instantiations across the corpus, each with a different formal reward. They are *not* substitutable; each commits to a different hypothesis about what makes a question valuable. Full discussion in [[../synthesis/proposer-reward-shapes]].

| Method | Reward shape | What it optimises for | Where the signal comes from |
|---|---|---|---|
| [[asymmetric-self-play]] (Sukhbaatar) | $R^A = \gamma \max(0, t_B - t_A)$ | Tasks Bob takes longer to do than Alice | Time-asymmetry; no external grader |
| [[../teacher-student-rl/soar-edge-of-learnability]] (SOAR) | Improvement *rate* of student over time | Tasks where the student's success-rate is rising | Bilevel meta-RL with held-out hard set |
| [[sqlm]] | $R_P = 1 \iff 0 < \lvert\{y_i = y_\text{maj}\}\rvert < N$ | Tasks neither all-solved nor all-failed by $N$ samples | Solver's own majority-vote consensus, no labels |
| [[spice]] | $r_C = \exp(-(\text{Var}(\{l_i\}) - 0.25)^2 / 0.02)$ | Reasoner pass-rate near 50% | Variance over correctness samples |
| [[spell]] | Independent Gaussian on Responder competence | Question difficulty at responder's frontier | Verifier (third role) judgement |
| [[spag]] | ReST-style binary (train on winning episodes only) | Strategies that win the Taboo game | Game outcome via string-match; no judge |
| [[azr]] | $r^\text{propose} = 1 - \bar{r}^\text{solve}$ if $\bar{r}^\text{solve} > 0$ else $0$ | Solvable-but-not-trivial code tasks (asymmetric Goldilocks) | Code executor + solver pass-rate |
| [[r-zero]] | $1 - 2\lvert\hat{p} - 1/2\rvert$ + BLEU-cluster repetition penalty | Solver pass-rate exactly 50% + diverse questions (symmetric Goldilocks) | Solver empirical accuracy + repetition penalty |
| [[language-self-play]] | $\bar{V} - V(q_i)$ + reference-model quality (0–7) | Questions harder than batch average + meeting quality bar (general-sum) | Solver value baseline + reference-model quality score |

*Editorial reading:*

- **Sukhbaatar's time-asymmetry** is the most agnostic — it requires only that "doing" be an action sequence with a duration; it doesn't presume a verifier or a topic structure. It's also the hardest to translate to language.
- **SOAR's improvement-rate** requires bilevel infrastructure but produces the strongest *escape-from-plateau* signal (the user's [[../teacher-student-rl/soar-edge-of-learnability]] page documents 0/128 → non-zero on its hard set).
- **SQLM's instantaneous Goldilocks** is the cheapest-to-run LLM analogue of Sukhbaatar's frontier and the closest match to the user's "topic string = concept seed" frame.
- **SPICE's variance reward** is the only one that explicitly targets a 50% pass-rate, matching the [[../single-sample-rl-finetuning/data-efficiency-rft]] DOTS Theorem-1 prediction $\mathbb{E}[\|g\|^2] \propto p(1-p)$.
- **SPELL's responder-frontier-Gaussian** is structurally similar to SPICE but routes the difficulty signal through a *third* role (verifier) rather than two.
- **SPAG's ReST-style** is the only purely-offline option — episodes are filtered post-hoc and the model is reinforced only on winners.

This catalogue is unpacked in detail in the dedicated synthesis page [[../synthesis/proposer-reward-shapes]].

## Other structural axes

### Two-role vs three-role decompositions

| Roles | Methods |
|---|---|
| **2** (proposer + solver) | [[spag]] (attacker/defender), [[sqlm]] (proposer/solver), [[spice]] (Challenger/Reasoner), [[asymmetric-self-play]] (Alice/Bob), [[../self-improvement/multi-turn-policy-verifier]] (policy/verifier) |
| **3** (proposer + solver + verifier) | [[spell]] (Questioner/Responder/Verifier) |
| **1** (single agent + lookahead oracle) | [[alphazero]] (policy network + MCTS rollout) |

The verifier-as-third-role question — does self-play need an external grader, or can majority-vote / game-outcome / variance-correctness substitute? — is unsettled. SPELL argues yes (verifier enables an independent difficulty signal); SQLM and SPAG argue no (game outcomes / consensus suffice). Likely depends on whether the concept admits a procedural correctness check.

### Information asymmetry — structural vs soft *(decision locked 2026-05-01)*

| Mechanism | Where |
|---|---|
| **Structural** — the solver simply does not see the privileged information | [[spice]] (Reasoner does not see document $d$); [[azr]] (Solver does not see Proposer's program); [[spag]] (defender does not see target word $w$); [[asymmetric-self-play]] (Bob does not see Alice's intended target until execution) |
| **Soft (penalty)** — solver could see it, but the proposer is penalised for leakage | [[../teacher-student-rl/sakana-rlt]] $r^{KL}$ penalising answer-leakage in the teacher's think-tokens |

This is a real architectural choice, not a tuning knob. **Decision locked 2026-05-01:** user has chosen *structural* over *soft* for [[../synthesis/proposed-method]] component C (reference-in-context). Default Phase-0+ design: Reasoner does not see reference text during gradient step; teacher/Challenger does. RLT $r^{KL}$ regulariser dropped from default loss. (Memory: `feedback_self_play_design_choices.md`.)

### Stabiliser presence (new axis 2026-05-01)

Single-model self-play is collapse-prone unless a stabiliser is in place. Four working stabiliser patterns:

| Stabiliser | Method | Mechanism |
|---|---|---|
| **Task-mode diversity** | [[azr]] | Three reasoning modes (deduction/abduction/induction) prevent collapse to a single trivial pattern. No KL needed. |
| **General-sum quality reward** | [[language-self-play]] | Reference-model quality score (0–7) added to both players. Game becomes general-sum; trivial-collapse equilibrium no longer Nash-stable. **Without it, Solver hacks by answering everything in Python.** |
| **Hard Goldilocks floor** | [[sqlm]] | Proposer reward $= 0$ for both trivially-easy and impossible questions; topic conditioning prevents drift. |
| **Structural information asymmetry** | [[spice]] | Reasoner doesn't see document; questions must be answerable from grounded source; no hallucination shortcut. |
| **Architectural separation (two models)** | [[r-zero]] | Two independent base-LLM copies. Authors claim unified collapses (Appendix D); see [[../../conflicts/unified-vs-two-model-self-play]] for the contradiction with the four working unified-model methods. |

**Practical reading:** any inner-loop self-play implementation must commit to at least one stabiliser. Stabiliser presence — not single-vs-two-model architecture — is the load-bearing axis.

### Online vs offline signal

| Mechanism | Where |
|---|---|
| **Online** | [[sqlm]], [[spice]], [[spell]], [[spiral]] — proposer reward computed against the current solver |
| **Offline (filter then train)** | [[spag]] ReST-style; [[../single-sample-rl-finetuning/critique-ft-one-problem]] critique-FT (analogous SFT version) |
| **Iterated-offline** | [[spin]] previous-iterate as reference; [[sppo]] previous-policy in the constant-sum game |

## What this corpus does *not* answer

- **Single-sample regime — partial answer found 2026-05-01.** [[rstar]] supplies the *test-time per-problem multiplier*: 32 MCTS rollouts × 5 actions over a single $(Q, A)$ seed, frozen weights. **LLaMA2-7B GSM8K 12.51% → 63.91% without fine-tuning.** This is the cleanest match for the user's "self-play as multiplier on single-sample optimization" frame (memory: `feedback_self_play_design_choices.md` Ruling 3). For the *training-time* analogue (gradient updates from single-sample self-play episodes), the corpus still has no direct instance.
- **Reference-grounded RL with weight updates.** [[spice]] grounds in a corpus but the document set is large (20K). The intermediate band ($N \approx 10\text{–}100$ exercises sharing a reference) is unmeasured.
- **Concept identity.** None of these methods need a concept-identity hash; the concept is implicit in the topic / target-word / document. The wiki's [[../synthesis/recursive-concept-learning|RCL]] requires explicit identity ($E3$); self-play does not address it. *Note 2026-05-01:* [[azr]]'s three reasoning modes is a concept-mode-decomposition (different from concept-prereq decomposition); flagged in [[../synthesis/recursive-concept-learning]] D1 as a candidate.
- **Forgetting protection across concept episodes.** Self-play assumes a single fixed concept domain (or a uniform mix). Sequential per-concept self-play with mask-composition or EWC anchors is unmeasured here — the wiki's [[../rlvr-mechanics/rl-sparse-subnetwork]] capacity-bound section flags this generally.

## Cross-references back into the wiki

- [[../synthesis/proposed-method]] component **C** (reference-in-context) — gap §4 closed 2026-05-01: structural asymmetry chosen, [[spice]] template adopted; RLT $r^{KL}$ dropped from default loss. Component **G** (diversity) updated with [[info-gain-self-play]]'s epiplexity pre-flight test.
- [[../synthesis/recursive-concept-learning]] gap #1 (curriculum-level credit assignment) — [[spiral]]'s RAE and [[sqlm]]'s Goldilocks gate as flat-curriculum anchors. Still open at the curriculum-DAG level. Component **D1** updated with [[azr]]'s three-mode decomposition as candidate concept-mode partition.
- [[../self-improvement/multi-turn-policy-verifier]] (PAG) — generalised by [[spell]] from two to three roles.
- [[../teacher-student-rl/soar-edge-of-learnability]] (SOAR) — [[sqlm]] is the cheapest LLM analogue; [[asymmetric-self-play]] is the pre-LLM precursor.
- [[../curriculum-and-decomposition/auto-kc-generation]] — strongly justified as the load-bearing concept-decomposition component if Invisible Leash holds (proposer-quality is the bottleneck).
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] (Wen et al., 2506.14245) — **counter-evidence**, not support: via CoT-Pass@K argues RLVR genuinely extends the reasoning boundary, pushing back on the Invisible-Leash / Position-A reading.

## Open questions

1. **Does the Invisible Leash bound hold for textbook-sized curricula?** The bound is shown for tasks where the base model has the latent capacity. For deliberately-novel concepts (a new theorem, a new procedure), is the bound informative? Refined: under standard short-training RLVR (Stage 1) almost certainly yes; Stage-2 escape requires entropy preservation that hand-curated curricula may or may not provide.
2. **Can SPAG-style "play with a concept" be lifted from single-word to procedural concepts?** All experiments use lexical targets; modular multiplication / chain rule / supply-and-demand is not in the empirical record. [[azr]]'s code-domain three-mode result is suggestive (concept-mode generalises across code), but not directly procedural-concept evidence.
3. **Three-role generalisation of SQLM.** SQLM uses majority-vote as implicit verifier; would [[spell]]-style explicit-verifier-role improve calibration on the Goldilocks gate?
4. **Self-play + sparse-mask + EWC.** None of these methods use [[../rlvr-mechanics/rl-sparse-subnetwork]] mask-bounded gradients or [[../catastrophic-forgetting/ewc-gemma2-cpt]] anchors. The compositional question (sequential per-concept self-play with forgetting protection) is open.
5. **Stabiliser comparison head-to-head.** Stabiliser-vs-architecture is the load-bearing axis; no paper directly compares (mode-diversity vs quality-reward vs hard-Goldilocks vs structural-asymmetry). See [[../../conflicts/unified-vs-two-model-self-play]].
6. **Stage-2 entry conditions.** [[two-stage-dynamic]] identifies the transition; engineering knobs that reliably *induce* Stage 2 (entropy preservation, training duration thresholds, learning-rate schedules) are not catalogued.
7. **Epiplexity in practice.** [[info-gain-self-play]]'s prequential MDL audit is conceptually crisp; computing $S_{C,T}$ before training in a standard pipeline is not yet a routine operation.

## Source

Editorial synthesis. All claims trace to [[spag]], [[sqlm]], [[spice]], [[understanding-self-play]], [[asymmetric-self-play]], [[spiral]], [[spell]], [[alphazero]], [[debate]], [[spin]], [[sppo]], [[invisible-leash]], [[yue-rlvr-boundary]], [[two-stage-dynamic]], [[azr]], [[r-zero]], [[language-self-play]], [[rstar]], [[info-gain-self-play]] in this theme, plus the cross-referenced existing wiki pages.

## Related

- [[../synthesis/proposed-method]] — component C (structural asymmetry locked) and component G (epiplexity pre-flight)
- [[../synthesis/recursive-concept-learning]] — credit-assignment gap (RAE / Goldilocks anchors); D1 (three-mode decomposition candidate)
- [[../synthesis/proposer-reward-shapes]] — dedicated synthesis of the nine reward shapes
- [[../self-improvement/multi-turn-policy-verifier]] — PAG; SPELL's predecessor
- [[../teacher-student-rl/soar-edge-of-learnability]] — bilevel student-improvement reward
- [[../curriculum-and-decomposition/auto-kc-generation]] — concept-decomposition by LLM
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — open conflict, refined 2026-05-01 to Stage-1-scoped
- [[../../conflicts/unified-vs-two-model-self-play]] — open conflict, stabiliser-vs-architecture resolution candidate
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — Wen et al.: counter-evidence to the Invisible-Leash family (CoT-Pass@K shows boundary extension)
