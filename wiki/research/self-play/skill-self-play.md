---
name: skill-self-play
description: Skill Self-Play (Skill-SP) — proposer + solver + dynamic skill controller co-evolving via GRPO; a persistent, evolving skill library (induce/prune/refine) mediates task generation, gating the proposer's Goldilocks reward behind structural validity to block reward hacking and rescue backbones too weak to bootstrap unguided self-play.
type: research
---

# Skill Self-Play: Pushing the Frontier of LLM Capability with Co-Evolving Skills

Huang, Cheng, Liu, Chen, Liu, Ni, Zhou, Yang, Jiang, Zhou, Cheng, Jiang, Jiang. arXiv:2607.22529 (Jul 2026). A co-evolutionary RL framework — proposer, solver, and a **dynamic skill controller** — that routes task generation through a persistent, evolving library of modular "skill" packages (structural priors + validators, in the sense of Anthropic's 2025 Agent Skills) to reconcile open-ended task diversity with reliable verification. On tool-calling (API-Bank, BFCL) and logical reasoning (ZebraLogic), Skill-SP beats an "Unguided SP" self-play baseline on every backbone, and rescues weak backbones (Ministral-3-8B: 20.7% → 63.6% overall, +42.9 pp) where unguided self-play is essentially flat because the base model can't synthesize valid tasks unaided. On ZebraLogic, Unguided SP cannot bootstrap at all — it fails to synthesize valid puzzles and is excluded from the results table entirely.

## Method

Three components co-evolve over $T = 5$ self-play iterations, formalized as a bi-level optimization (Eq. 3): the outer objective jointly optimizes the skill library $\mathcal{S}$ and the proposer $\pi_\text{propose}$ to synthesize valid, frontier-targeted tasks; the inner objective is the solver maximizing execution success on those tasks.

**Gated proposer reward.** A verifiable task is $(\boldsymbol{x}, \boldsymbol{c})$ — visible prompt plus a hidden verification contract. Solver success rate:

$$v_\text{solve}(\boldsymbol{x},\boldsymbol{c};\pi_\text{solve}) = \mathbb{E}_{\boldsymbol{y}\sim\pi_\text{solve}}[R_\text{solve}(\boldsymbol{x},\boldsymbol{y},\boldsymbol{c})] \quad \text{(Eq. 1)}$$

$$R_\text{propose} = \mathbb{1}\{(\boldsymbol{x},\boldsymbol{c})\text{ valid}\} \cdot \bigl[1 - 2\lvert v_\text{solve} - 0.5\rvert\bigr] \quad \text{(Eq. 2)}$$

The medium-difficulty ("frontier") term is identical in shape to SQLM's and R-Zero's Goldilocks gates (see below); the novelty is the **binary structural-validity gate multiplying it**, which blocks the failure mode where an ungated proposer fabricates unsolvable or ill-posed contracts purely to farm difficulty reward. Validity (Eq. 4) requires schema compliance $\cap$ contract validity (skill validators) $\cap$ **probe consistency** — $K$ frozen-solver rollouts must converge on a unique majority answer matching the proposer's reference.

**Skill tuple.** $\boldsymbol{s} = \langle m, r, h, e, \nu, \sigma \rangle$ — routing metadata, procedural rules, generation hints, few-shot examples, executable validators, usage statistics. **Dual-stream generation**: a skill-conditioned stream $\pi_\text{propose}(\cdot\mid\boldsymbol{s})$ injects structural priors; an unconstrained exploration stream $\pi_\text{propose}(\cdot\mid\emptyset)$ prevents mode collapse and surfaces genuinely novel task patterns.

**Training.** Proposer updated via GRPO maximizing $J_\text{propose} = \mathbb{E}_{\boldsymbol{s}\sim\mathcal{S},\,(\boldsymbol{x},\boldsymbol{c})\sim\pi(\cdot|\boldsymbol{s})}[R_\text{propose}]$ (Eq. 5), reusing the $K$ verification rollouts as the empirical evaluator. Solver curriculum: rank valid candidates from both streams by $R_\text{propose}$, blend top-$\alpha M$ skill-stream / top-$(1-\alpha)M$ exploration-stream ($\alpha=0.5$, Eq. 6); solver updated via GRPO on task-verification reward (Eq. 7). The trained solver never sees skill-package context, at train or eval time — only the standard task prompt.

**Skill library evolution**, each iteration:
1. **Refine** — update usage stats $\sigma$; diagnose failure traces to rewrite skill content.
2. **Prune** — drop skills whose expected frontier reward falls below $\gamma_\text{prune}$ (Eq. 8) — saturated/trivial skills.
3. **Induce** — extract high-reward exploration-stream candidates above $\gamma_\text{induce}$ (Eq. 9); a skill controller $\pi_\text{control}$ — instantiated from the **initial base policy**, not the trained proposer/solver — abstracts them into candidate packages, filtered for structural integrity and lexical novelty against the current library (Eq. 10).

**Skill routing** (Appendix B): Beta-smoothed success rates across three outcome types (structural-verified / solver-consistent / frontier-difficulty) combine into a composite quality score $v_\text{skill}$ (Eq. 12, weights $\tfrac12,\tfrac14,\tfrac14$); sampling weight is clipped and multiplied by a decaying exploration bonus $\beta\exp(-a_j/\tau)$ (Eq. 13) — an exploitation/exploration bandit over *skills*, not just individual tasks.

## Claims

Evaluated on tool-calling (API-Bank L1–3, BFCL: JS/Py/Java/Live) and logical reasoning (ZebraLogic, 4 scale tiers) across five backbones (Qwen3-4B-Instruct, Qwen3-8B, Ministral-3-8B, Ministral-3-14B, Granite-4.1-3B), against Base and an Unguided-SP baseline (post-hoc filtering, no skill guidance):

| Backbone | Domain | Unguided SP | Skill-SP | Note |
|---|---|---|---|---|
| Qwen3-4B-Instruct / Granite | Tool-call | competent baseline | +2.8 to +6.5 pts overall | already-capable models still gain |
| Ministral-3-8B | Tool-call | +0.1 pts (flat) | +42.9 pts overall (20.7% → 63.6%) | base model can't synthesize valid tasks unaided — starves unguided loop |
| Ministral-3-14B | Logic (ZebraLogic) | excluded from table — fails to synthesize valid puzzles | +12.0 pts overall, +35.3 on Small-scale | Unguided SP cannot bootstrap in this domain at all |

**Ablations** (Tables 3–4, Qwen3-4B-Instruct): Unguided SP −2.6 overall (early plateau). Uniform skill routing −1.9; frozen skills −2.3 (dynamic orchestration, not just static structural priors, drives the gain — frozen-skills only marginally beats Unguided SP: 64.4 vs 64.1). Skill-only generation pool underperforms the mixed dual-stream pool (over-specialization). **Frozen proposer −2.1; frozen feedback solver −3.0 (largest single-component drop); frozen both −3.2** — both the proposer *and* the solver's evaluator role must co-evolve; freezing the evaluator "severs the dynamic frontier-tracking mechanism."

## Compute and sample efficiency

Not single/few-shot — this is a compute-heavy self-generated-curriculum method, orthogonal to this wiki's single-sample-training interest. Per iteration: $M=8{,}000$ tool-calling tasks ($\alpha=0.5$, $K=10$ probes) or $M=1{,}920$ reasoning tasks (deterministic checker), across $T=5$ iterations, 8×A800 GPUs, ~1 day/run. Solver-curriculum construction dominates wall-clock (57%); skill-library evolution is cheap (6.5%). Initial skill library is LLM-seeded once per domain (15 tool-call packages, 8 ZebraLogic packages) and shared across all five backbones, but the paper attributes most of the gain to online evolution, not the seed. No human labels or demonstrations required for the domains tested. This is data-*self-generation* efficiency (no external annotation), not sample-count efficiency in the wiki's single-example sense.

## Concept-learning evidence (indirect — curriculum-structure level)

§4.4 diagnostics: (1) skill-routed tasks track the solver's empirical learning frontier more tightly ($v_\text{solve}\approx0.57$) than exploration-stream (0.75) or Unguided SP (0.70) tasks; (2) Sentence-BERT + PCA shows Unguided SP tasks cluster narrowly while the Skill-SP mixed pool covers a broader semantic region — skill orchestration simultaneously sharpens difficulty *and* broadens diversity; (3) the skill library keeps inducing ~20 new packages/round while pruning stale ones; effective-skill count (exponentiated Shannon entropy) grows to 46 of 86 active skills — argued as evidence the library distills "reusable structural priors," not idling on a few templates.

No probing, no compositional-generalization test, and no pass@k support analysis of the *trained solver*. The paper's "concept" claim is about skills as reusable task-pattern interfaces (explicitly borrowed from Anthropic's Agent Skills framing), not about concept acquisition inside solver weights.

## Failure modes and limitations

Authors (Appendix H): discovering genuinely novel task patterns requires the base model to already have a minimum foundational capability to bootstrap valid signals; for extremely complex domains the framework "might initially benefit from a small set of human demonstrations." Confirmed empirically — weak backbones still show near-zero accuracy on ZebraLogic Large/X-Large tiers even with Skill-SP; self-play alone cannot cross a capability floor. Fixed per-domain hyperparameters: mixing ratio $\alpha$, pruning/induction thresholds $\gamma_\text{prune}/\gamma_\text{induce}$.

Unstated in the paper: (a) the skill controller $\pi_\text{control}$ is instantiated from the *initial* base policy for every iteration — self-referential drift risk is not analyzed beyond lexical-novelty dedup; (b) the "probe consistency" validity leg relies on $K=10$ frozen-solver majority-vote — structurally the same mechanism as the majority-voting post-hoc filters the paper explicitly critiques Unguided SP for using, just gated behind additional skill-validator and schema checks; (c) substantial compute footprint (8×A800, ~1 day/run) sits at the opposite end of the cost spectrum from this wiki's single-sample-training interest.

## Why this matters for the self-play family

Skill-SP is the wiki's first proposer/solver self-play instance to formalize a **persistent, evolving skill library** — not just a policy role — as a third co-evolving component, and the first to gate a Goldilocks-style medium-difficulty reward behind a binary structural-validity check rather than relying on the difficulty signal alone. Two direct parallels already in the corpus:

- **[[sqlm]]** — the same medium-difficulty principle ($0 < |\{y_i=y_\text{maj}\}| < N$) reward-shape, independently instantiated via skill-conditioning rather than shared-weights topic-seeding. Skill-SP's Eq. 2 ($1-2|v_\text{solve}-0.5|$) is continuous where SQLM's gate is binary, but both target $v_\text{solve}\approx 0.5$.
- **[[spice]]** — a parallel anti-reward-hacking mechanism. SPICE uses **structural information asymmetry** (Challenger sees a document, Reasoner doesn't) to prevent the proposer from farming unanswerable questions. Skill-SP uses a **binary skill-validator gate** multiplying the difficulty reward instead. Both solve the same "proposer fabricates unsolvable tasks to farm difficulty reward" failure mode via different structural mechanisms — worth tracking as two candidate anti-reward-hacking primitives for [[../synthesis/proposed-method]] component C.

**A partial complication to the Invisible-Leash mechanistic anchor.** [[understanding-self-play]] claims the proposer is the critical component and the solver only re-weights base-model probability mass. Skill-SP's ablations complicate this only partially: frozen *feedback* solver (the evaluator role used to compute proposer reward and probe validity) costs −3.0 pts — more than frozen proposer at −2.1 pts. But "feedback solver" here is the reward-computation/evaluator role, not a test of whether the *trained* solver's pass@k support ever exceeds the base model — so this is not counter-evidence to the Invisible-Leash bound itself, just a reminder that "solver" conflates two distinct roles (evaluator vs. learner) whose ablation costs differ.

The evolving skill library — induce/prune/refine each iteration — is also a self-generated, bottom-up curriculum-selection mechanism, parallel to [[../curriculum-and-decomposition/metis-curriculum-judgment|METIS's]] internalized curriculum-selection-via-ICL and [[../curriculum-and-decomposition/scrl-curriculum-credit-assignment|SCRL's]] subproblem decomposition — except the curriculum unit here is a reusable *skill*, not a subproblem or a memory of reward-variance.

## Source

- `raw/research/weekly-2026-07-31/03-skill-self-play.md`
- arXiv: https://arxiv.org/abs/2607.22529

## Related

- [[_overview]] — self-play theme overview; eleventh proposer-reward shape
- [[../synthesis/proposer-reward-shapes]] — cross-method reward-shape comparison table
- [[sqlm]] — closest reward-shape parallel: Goldilocks/medium-difficulty gate
- [[spice]] — parallel anti-reward-hacking mechanism (structural asymmetry vs. validator gate)
- [[understanding-self-play]] — mechanistic anchor this page's ablations partially complicate (evaluator-role vs. trained-solver distinction)
- [[azr]] — cited by Skill-SP as the "environment-bound" self-play family it contrasts against
- [[spiral]] — cited alongside AZR as environment-bound/game-simulator self-play
- [[../curriculum-and-decomposition/_overview]] — skill induce/prune/refine as a self-generated curriculum mechanism
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO is the optimizer for both proposer and solver updates
- [[../../weekly-briefs/2026-07-31]] — brought in by the 2026-07-31 weekly sweep
