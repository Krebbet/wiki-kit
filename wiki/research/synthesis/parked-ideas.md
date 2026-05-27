---
name: parked-ideas
description: Low-ceremony parking lot for tangential research ideas raised in conversation that don't yet warrant a full synthesis page or a /research run. Each entry: the idea verbatim-ish, why it's here, and where it connects to existing wiki machinery. Promote to a full page / research run when an entry accrues enough weight.
type: research
---

# Parked ideas

Editorial scratch space. Ideas raised in conversation that are adjacent-but-not-core, captured so they aren't lost. Not synthesised from sources — each entry is the researcher's (David's) idea, tagged *(parked)*. Promote an entry to its own synthesis page or a `/research` run when it accrues weight or a second converging signal.

---

## P1 — Longitudinal agentic-failure telemetry → deficit list → targeted base-model fine-tuning

*Parked 2026-05-16.*

**The idea.** Instrument a deployed agentic system to collect feedback over time — where it fails, what it does wrong — and accumulate that telemetry. Later, mine the accumulated record into a structured list of *deficits*, and use that deficit list as the training-target curriculum for fine-tuning the agent's base model. I.e. the production system generates, longitudinally, its own fine-tuning curriculum from observed real-world failures rather than from a synthetic eval battery.

**Why it's parked here and not elsewhere.** It is *not* about single-sample concept fine-tuning per se (the wiki's core), so it doesn't belong in [[proposed-method]]/[[recursive-concept-learning]] as a component. But it is the **deployed-agent, longitudinal-telemetry data source** for machinery the wiki has already built, so it should not be orphaned:

- **It is a real-failure data source for [[recursive-concept-learning]]'s D1 gap** — the wiki's single *deepest* open gap (RCL §Known-gaps #5, Tier-5 item 32): *failure-trace-conditioned concept decomposition*. RCL assumes failure traces come from a test harness; this idea supplies them from production telemetry instead. The decomposition step (`Decompose(c, trace)`) is unchanged; the **trace source** is the contribution.
- **It is the longitudinal form of [[proposed-method]]'s P1 + S** — the failure trigger $F(x) = H(\pi_\theta(y\|x))/(M(\pi_\theta(y\|x))+\varepsilon)$ (component **P1**) and the deficit map / stopping signal (component **S**) are *per-exercise, in-loop*. This idea accumulates the same kind of signal *across deployments and time*, then batches it into a curriculum — P1/S run as a background telemetry process rather than a training-loop gate.
- **The deficit-extraction step is the [[../concept-evaluation/_overview]] battery applied to logged failures** — contrast-set / counterfactual / MDL-sibling probes turn a pile of failure traces into a *structured* deficit list (which concepts, not just which prompts). The "Test-dataset references" subsection there (Learning-from-Less procedural datasets) is a candidate synthetic backstop when telemetry is sparse.
- **Agentic failure-attribution is the unfilled prerequisite.** The 2026-05-13 decoding-time `/research` run noted that *agent* failure-attribution (MAST / Who&When / AgenTracer 2025) is a *different problem class* than concept-decomposition and was deliberately not captured. This idea is exactly where those two problem classes meet: agent-failure-attribution produces the trace; concept-decomposition (D1) turns it into a deficit. A future `/research` run on agentic failure-attribution would be the natural feeder.

**What's genuinely new vs. existing wiki machinery.** The novel element is *temporal accumulation from a live system* as the deficit source — every captured method (RCL, proposed-method, the concept-evaluation battery) assumes an offline harness or synthetic generator. Open sub-questions if promoted:
1. **Attribution.** Mapping a multi-step agentic failure to a *concept* deficit (vs. a tool error, a planning error, a context-window artefact) — this is the agent-failure-attribution × D1 intersection, currently unowned in the corpus.
2. **Curriculum debounce.** Telemetry is noisy and non-stationary; the deficit list needs the same kind of learnability filter the wiki already uses ([[../self-play/info-gain-self-play]] epiplexity, [[../single-sample-rl-finetuning/data-efficiency-rft]] $p\approx0.5$) before a deficit becomes a fine-tuning target — otherwise you fine-tune on noise.
3. **Forgetting under repeated deficit-targeting.** Sequentially fine-tuning on an evolving deficit list is exactly the skill-stacking regime — [[../catastrophic-forgetting/_overview]] (RL's-Razor implicit / [[../selective-finetuning/_overview]] explicit / [[../moe-adapters/_overview]] architectural) applies directly; the architectural answer (a per-deficit MoERA expert, [[../moe-adapters/loramoe]]) is an especially natural fit since deficits arrive incrementally.

**Promotion trigger.** Promote to a full synthesis page (or a `/research` run on agentic failure-attribution → concept decomposition) if (a) a second converging signal appears, or (b) the project moves toward a deployed-agent setting where the telemetry source becomes concrete.

---

## P2 — "Backtrack": interventional, prompt-level concept credit assignment

*Parked 2026-05-18. Triggered by [[../process-reward-models/uprm]].*

**The idea.** The shared bottleneck under uPRM, [[../rl-optimizers/ep-grpo]], [[../rlvr-mechanics/rethinking-rl-sparse-selection]], and the entire [[../process-reward-models/_overview]] theme is **identifying which parts of a token trace are responsible for a good rollout**. Two routes:

1. **Concept-targeted do-over (re-elicitation).** After a correct rollout, re-prompt: *"you got this right before; we want to check you understood X — answer again and justify X."* If the model stays correct only when forced through concept X, X was load-bearing; if it stays correct without needing X, X was not. Credit assignment by *intervention on the re-prompt*, not by scoring the original steps.
2. **Question-side self-play / rollout distillation.** (2a) Use perturbations of the *question itself* as a probe for which model regions / positions are responsible for the correct answer, then focus the gradient there. (2b) Distil the N rollouts of one question into a single *concentrated* question+trace that isolates the causal concept — a maximally-informative single training sample.

**Why it's parked here.** It's *more core* than P1 (credit assignment is central to the wiki's RL themes), but it's a forming idea, not a worked proposal. Where it sits against existing machinery:

- **Observational vs interventional is the axis.** Every captured credit-assignment method is *observational* — score the steps that happened: PAV ([[../process-reward-models/pav-rewarding-progress]], step-advantage under a complementary prover), Math-Shepherd (MCTS-rollout potential), uPRM (frozen-LLM marker probs), REASONMAXXER/EP-GRPO (entropy gating). "Backtrack" is *interventional* — re-elicit/re-question to test a causal hypothesis. The corpus has interventional credit assignment only at the **activation** level ([[../decoding-time-steering/iti]], [[../concept-evaluation/causal-abstraction]] IIA). **Interventional, prompt-level concept credit assignment is unowned in the corpus — this is the contribution.**
- Route 1 is the *interventional* upgrade of [[../self-improvement/star]] rationalization (answer-as-hint re-derivation) and ExGRPO explanatory probes ([[../teacher-student-rl/rlt-followups-2026]]); the concept-conditioning is the [[../concept-evaluation/counterfactual-tasks]] / IIA idea applied to a re-prompt rather than an activation patch.
- Route 2a is REASONMAXXER's entropy-gated contrastive + [[../catastrophic-forgetting/path-not-taken]] off-principal sparsity + [[../rlvr-mechanics/rl-sparse-subnetwork]], but with **question-perturbation as the attribution probe** (orthogonal to trace-side entropy — no captured paper uses it for attribution).
- Route 2b is the *inverse* of [[../single-sample-rl-finetuning/critique-ft-one-problem]] (1 problem → 600 rows): compress many rollouts of one problem into one concentrated sample. Directly the single-sample core thesis; the concentrated question is also a precise deficit-targeting datum for P1.
- Maps onto [[proposed-method]]: a sharper realisation of components **P1** (failure/uncertainty trigger), **V** (MDL-sibling concept test), and **S** (deficit map) — and a candidate dense inner-loop reward (see the uPRM flag in [[proposed-method]]).

**Open sub-questions.** (a) Does the do-over's "still correct when forced through X" actually discriminate causal-X from spurious-X, or does the model confabulate a post-hoc X-justification regardless? (the [[../concept-evaluation/causal-abstraction]] confound). (b) Question-perturbation attribution needs a learnability/validity filter ([[../self-play/info-gain-self-play]] epiplexity) so you don't attribute to noise. (c) Distillation objective for 2b: what makes a rollout "concentrated" — minimal-description-length over the concept ([[../concept-learning/recursive-concept-evolution]] MDL) is the natural candidate.

**Promotion trigger.** Promote to a full synthesis page if a second converging signal appears, or when the experiment proposal reaches the inner-loop-reward design decision (uPRM / interventional credit is flagged there — see [[proposed-method]]).

---

## P3 — VPO stochastic scalarization for component P4

*Parked 2026-05-27. Triggered by [[../rl-optimizers/vpo]] (arXiv:2605.22817).*

**The idea.** Replace P4's fixed-weight principle scalarization with the VPO set-level objective: Dirichlet-sampled per-rollout weight vectors + best-of-$m$ selection + GRPO advantage over rollout-sets. VPO demonstrates this produces reward-diverse candidate sets that support test-time search far better than scalar baselines (best@k gap widens with k; OpenEvolve unlocks problems GRPO cannot solve at any budget), with the gain predictable from the on-policy reward-component collinearity $\bar\rho$.

**Why it's here and not directly in proposed-method.** VPO is validated on large training corpora (thousands of prompts, $n=8$ rollout-sets, $m=3$ answers per rollout). Proposed-method runs 1–100 exercises with a small group budget. Two pre-conditions must be checked before promoting this to a P4 design decision:

1. **Non-collinearity.** VPO's advantage collapses when on-policy $\bar\rho \approx 1$ (UltraFeedback: $\bar\rho = 0.95$ → VPO hurts). For a textbook concept domain, whether the 5–10 sub-principles (e.g., "applies chain rule correctly," "identifies boundary condition," "writes clean notation") are non-collinear under the base model is unknown. Run the $\bar\rho$ diagnostic first.
2. **Pass@1 vs best@k.** VPO explicitly degrades pass@1 (LCB: VPO < GRPO at pass@1, better at every best@k). If the concept-installation eval is single-shot correctness rather than search-augmented, VPO's stochastic scalarization is the wrong objective. Confirm the eval regime first.
3. **Group size.** VPO requires $G > 1$ rollout-sets to compute a non-degenerate group advantage. Confirmed consistent with proposed-method component **G** (diversity injection, group size > 1), but rules out $G=1$ settings.

**Additional caution — goal-conditioning failure.** VPO shows that conditioning the model on a text-encoded weight vector (goal-conditioned GRPO) mode-collapses — the model ignores the conditioning and best@k stalls. Any P4 design that relies on *explicit* principle-axis conditioning in the prompt (rather than in-context multi-answer exploration) is fragile.

**Connection to existing machinery.**
- Component **G** (diversity injection): VPO's multi-answer chain is the structural homologue of diversity injection at the in-context level rather than the group-rollout level. They are complementary, not substitutes.
- Concept-evaluation battery ([[../concept-evaluation/_overview]]): the $\bar\rho$ check maps onto the question of whether the concept's sub-criteria are genuinely distinct axes, which the battery is designed to probe.
- [[../rlvr-mechanics/binary-rewards-rl-challenges]]: formal substrate for the diversity collapse VPO addresses (I-projection mode collapse under scalar RL).

**Promotion trigger.** Promote to a P4 design ruling when: (a) on-policy $\bar\rho$ diagnostic confirms sub-principles are non-collinear on target-domain exercises, and (b) the experiment frame confirms the eval regime is best@k or search-augmented rather than pass@1.

---

## Source

Editorial. Ideas raised by David in conversation (P1: 2026-05-16; P2: 2026-05-18). P3 triggered by [[../rl-optimizers/vpo]] (2026-05-27). Connections to existing pages are this page's framing, not source claims.

## Related

- [[recursive-concept-learning]] — D1 / Tier-5 item 32 is the gap this idea feeds (failure-trace-conditioned decomposition)
- [[proposed-method]] — components **P1** (failure trigger) and **S** (deficit map); this is their longitudinal form
- [[../concept-evaluation/_overview]] — the battery that turns logged failures into a structured deficit list
- [[../catastrophic-forgetting/_overview]] / [[../selective-finetuning/_overview]] / [[../moe-adapters/_overview]] — sequential deficit-targeting is skill-stacking; the three interference answers apply
- [[../self-play/info-gain-self-play]] — epiplexity as the learnability filter before a deficit becomes a target (P1 and P2)
- [[../process-reward-models/uprm]] — P2 trigger; observational-credit foil to P2's interventional approach
- [[../process-reward-models/pav-rewarding-progress]] — closest observational step-credit method P2 contrasts with
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] / [[../rl-optimizers/ep-grpo]] — entropy-gated credit assignment; P2 route 2a builds on these
- [[../single-sample-rl-finetuning/critique-ft-one-problem]] — P2 route 2b is its inverse (compress, not amplify)
- [[../concept-evaluation/causal-abstraction]] — interventional (IIA) credit at activation level; P2 lifts it to the re-prompt level
