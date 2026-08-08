# Argus: A General-Purpose Agentic Runtime for Long-Horizon Reasoning

Microsoft/SJTU-led 20+-author consortium technical report (arXiv:2608.05144, Aug 2026). Argus is a runtime layer, not a training method — model weights stay fixed; what evolves is persistent runtime state (Memory, Skills, Tools, Verifiers, Routing, Tasks) across four role-separated agents: Manager (owns objective and stage transitions), Planner (decomposes work into bounded tasks), Engineer (executes, may self-review low-risk work), and Reviewer (independently inspects, issues completion verdicts). A formal `ManagerAdmit` operator gates material revisions to the working contract (standing intent, operational objective, constraints, verification criteria) against recorded evidence, making a legitimate pivot distinguishable from silent objective drift. All runtime self-evolution — candidate memories, skills, procedures, verifiers, routing decisions — becomes reusable only after role-owned review and, where available, task-native verifier evidence.

## Method

Derives directly from ReAct/SWE-agent/OpenHands (execution-loop substrate), MemGPT/Agent Workflow Memory/A-MEM (persistent memory tiers, extended with explicit ownership/commit gating per state surface), and full-lifecycle autonomous-research systems (AI Scientist, CycleResearcher, AutoSci, FARS, Arbor) whose "objective is given" assumption Argus explicitly rejects in favor of gated objective revision. Cross-session continuity runs through a shared `CHECKPOINT.md` rather than a long model context — Engineer/Reviewer calls use fresh provider sessions each round.

## Results

SWE-Bench Pro (731 tasks, GPT-5.5/xhigh via Copilot): ~78% accuracy vs ~59% for Direct Copilot (+19pp) at 1.41× aggregate tokens. Longitudinal self-evolution: mature runs use 21% fewer solve-input tokens and 15% less active time per task than startup runs. Seven-arena capability floor spans GPU kernel optimization (global #6 of 101), nanochat/nanoGPT speedrun records near human-best, and MLE-Bench Lite Kaggle medals (3 gold, 3 silver, 3 bronze). Vertical case studies: six autonomous paper-production campaigns all reach submission (640 campaign-hours, 254 missions); an Argus-designed W4A8 inference accelerator closes functionally (13,914/13,914 commands, 0 first failures) and physically via SKY130 synthesis; a materials/MOF campaign replaces a published sampling method with a simpler one after isolating a statistically-confirmed confound; an Argus-optimized TileLang RWKV6 kernel merged upstream into `fla-org/flash-linear-attention` (PR #1045) — the one independently verifiable external-adoption data point.

## Applicability

Not a training recipe — for teams building agent orchestration/harness layers on top of an existing strong backbone. Requires a capable instruction-following backbone behind an execution surface, task-native verifiers per domain (unit tests, static-timing tools, external graders), and substantial autonomous wall-clock budget (multi-day campaigns) with persistent storage for checkpoints/skills/memory/routing state. Not useful for tasks without an executable/external evaluator.

## Novelty

Recombination and formalization rather than a new core algorithm — the tool-use loop, persistent memory tiers, and role-separated research agents all pre-exist. The contribution is (1) the formal contract/`ManagerAdmit` apparatus making objective-pivoting evidence-backed and audited rather than an implicit consequence of replanning, (2) an explicit ownership table assigning commit authority per persistent-state surface, and (3) an adaptive Engineer-self-review-vs-independent-Reviewer routing policy with measured recovery funnels.

## Conflicts

Argus's framing — a "general, self-evolving harness" that closed 6/6 autonomous paper campaigns to submission and retained proof-backed math frontier updates — sits in soft tension with [[ai-agents-open-ended-research]], which found frontier agents' open-ended research judgment rejected by the source papers' own authors (2/6, 1/6) despite flawless engineering execution. Argus's own paper concedes the same limitation almost verbatim (§8: "does not establish paper acceptance, scientific novelty, or superiority to human research teams"). Treated as an open tension, not a resolved contradiction — no dedicated conflict file opened this week since neither source claims a hard, checkable disagreement; watch for a future source that forces a ruling.

## Related

- [[ai-agents-open-ended-research]] — see Conflicts above.
- [[memoharness]] — closest architectural parallel: bounded structured-edit + correctness-validation gate for harness components with no gradients/RL. Argus generalizes the same propose→validate→commit pattern to the full runtime state.
- [[skillopt]] — Argus's skill-update mechanism (propose → Reviewer commits) mirrors SkillOpt's propose-edit-validate loop, extended beyond skill documents.
- [[agentflow]] — parallel four-module role decomposition (Planner/Executor/Verifier/Generator vs Manager/Planner/Engineer/Reviewer) but the opposite design bet: AgentFlow trains its roles on-policy via Flow-GRPO (weights change); Argus freezes weights and evolves only external runtime state.
- [[huxley-godel-machine]] — shares the "self-improvement without gradient updates to the base policy" theme via a different mechanism (clade-based tree search vs verification-gated runtime-state admission).
- [[seal-self-adapting]] — direct contrast: SEAL trains the adaptation strategy itself via an outer RL loop; Argus keeps self-evolution fixed-model, with SFT/RL on retained trajectories named only as future work.

## Source

- `raw/research/weekly-2026-08-08/02-argus-agentic-runtime.md` (arXiv:2608.05144)
