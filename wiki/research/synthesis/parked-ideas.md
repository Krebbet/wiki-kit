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

## Source

Editorial. Idea raised by David in conversation 2026-05-16; connections to existing pages are this page's framing, not source claims.

## Related

- [[recursive-concept-learning]] — D1 / Tier-5 item 32 is the gap this idea feeds (failure-trace-conditioned decomposition)
- [[proposed-method]] — components **P1** (failure trigger) and **S** (deficit map); this is their longitudinal form
- [[../concept-evaluation/_overview]] — the battery that turns logged failures into a structured deficit list
- [[../catastrophic-forgetting/_overview]] / [[../selective-finetuning/_overview]] / [[../moe-adapters/_overview]] — sequential deficit-targeting is skill-stacking; the three interference answers apply
- [[../self-play/info-gain-self-play]] — epiplexity as the learnability filter before a deficit becomes a target
