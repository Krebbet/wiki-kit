# Skill Self-Play (Skill-SP)

Alibaba/Qwen Applications Team paper (arXiv:2607.22529) introducing Skill-SP, a co-evolutionary self-play RL framework that resolves the tension between environment-bound verification (reliable but narrow) and unguided open-ended generation (broad but noisy) by routing task generation through an evolving library of Anthropic-style "skills." A Proposer, Solver, and skill Controller co-train via GRPO in a closed loop, giving gains from +2.8 to +42.9 avg points across tool-calling and logical-reasoning benchmarks on 3B–14B backbones.

## Method

Three components, all initialized from the same backbone (no external stronger teacher), trained jointly over 5 self-play iterations:

- **Proposer** — generates tasks conditioned on a sampled skill `s ~ S`, plus a parallel skill-free "exploration stream" for breadth.
- **Solver** — attempts generated tasks; reward is exact-match/format correctness.
- **Skill Controller** — maintains skill library `S`, where each skill is `⟨routing metadata, procedural rules, generation hints, few-shot examples, executable validators, usage statistics⟩`. This tuple is lifted directly from Anthropic's (2025) Agent Skills format but repurposed as a *training-time* task-generation interface rather than an inference-time tool.

Formalized as bi-level optimization: outer objective maximizes proposer+library reward under a **gated curriculum reward** `R_propose = 1{valid} · (1 − 2|v_solve − 0.5|)` — targets medium difficulty (solve-rate near 0.5) while a binary validity gate blocks reward hacking via unsolvable/ill-posed tasks. Validity = schema compliance ∩ contract validity (skill-defined validators) ∩ "probe consistency" (majority-vote rollouts from the current solver agree with the proposer's reference answer). Inner objective is standard solver policy-gradient maximization on `R_solve`. Both proposer and solver use GRPO (Shao et al. 2024); proposer gets a −1 penalty for parse failures.

Curriculum per iteration mixes top-`αM` skill-stream and top-`(1−α)M` exploration-stream candidates ranked by proposer reward (α=0.5). The skill library evolves every iteration via three controller-driven ops:
- **Refinement** — diagnose failure traces, update skill content.
- **Pruning** — drop skills whose expected frontier reward falls below `γ_prune` (saturated/trivial skills).
- **Induction** — abstract new skill packages from high-reward exploration-stream candidates, filtered for integrity + novelty vs. existing library.

Scale: 8,000 tasks/iteration for tool-use, 1,920 for reasoning; 4 proposer + 5 solver rollouts/iteration.

## Results

Evaluated avg@8 on 5 backbones (3B–14B): Qwen3-4B-Instruct, Qwen3-8B, Ministral-3-8B/14B-Instruct, Granite-4.1-3B.

- **Tool calling** (API-Bank L1–L3, BFCL JS/Py/Java/Live): Skill-SP beats base and Unguided-SP baselines on every backbone/subtask. Competent backbones (Qwen3, Granite) gain +2.8 to +6.5 avg pts. Misaligned backbones show dramatic turnarounds: Ministral-3-8B +42.9 avg pts (63.6 vs. base 20.7) — Unguided-SP is essentially flat (+0.1) here because the base model can't synthesize valid tasks unaided, starving the loop entirely.
- **Logical reasoning** (ZebraLogic, grid-level/cell-level accuracy across Small/Medium/Large/X-Large scales): Unguided-SP fails to bootstrap at all and is excluded from the results table (cannot synthesize valid puzzles without skill guidance). Skill-SP shows universal improvement: Qwen3-4B-Instruct +1.4 grid-level; Ministral-3-14B +12.0 grid-level overall, +35.3 on Small-scale puzzles.
- **Ablations** (Qwen3-4B-Instruct): Unguided-SP −2.6 overall; skill-only pool (no exploration stream) degrades generalization; uniform routing −1.9; frozen skills −2.3; frozen proposer −2.1; frozen solver −3.0; frozen both −3.2. Confirms gains come from dynamic curriculum + continuous co-evolution, not static structural priors alone.
- Diagnostics: skill-routed stream holds mean solve-rate ≈0.57 (near the targeted frontier) vs. 0.70–0.75 drift for the unguided/exploration streams; the skill library inducts ~20 new packages/iteration while pruning obsolete ones.

## Novelty vs. prior work

Recombination more than a wholly new mechanism — self-play, GRPO, skill libraries, and gated/frontier-targeted curricula each exist independently in prior work (Absolute Zero, SPIRAL/MARSHAL, Search Self-play for environment-bound self-play; unguided synthetic generation + post-hoc filtering via unit tests/majority voting for breadth; skill-interface literature on retrieval/compression/progressive disclosure, mostly at inference time). The genuinely new contribution is moving the skill library to **training-time curriculum control**: a Controller with its own RL-driven lifecycle (refine/prune/induce) that closes the loop between structural priors (normally static, as in [[skillopt]]'s inference-time optimization) and continuous curriculum evolution (normally purely reward-based, as in unguided self-play). The ablation suite (uniform routing, frozen skills, frozen proposer/solver) is explicitly constructed to isolate this contribution from those baselines.

## Reproducibility

Code released: https://github.com/Qwen-Applications/skill-self-play. No released model weights/checkpoints — backbones are pre-existing open models (Qwen3, Ministral-3, Granite-4.1); Skill-SP is a training recipe applied on top, not a new base model. No PapersWithCode entry found.

## Applicability

Requires an RL/GRPO training stack (proposer + solver + controller, single backbone, no external teacher), a domain with at least partial verifiable-task structure (schema checkers, unit tests, deterministic constraint checkers — needed for the skill's contract validator), and compute for iterative rollout-heavy self-play. Best fit: agentic tool-use / structured-reasoning fine-tuning where labeled data is scarce but partial verifiers exist — particularly strong as a recovery tool for a competent-in-principle but currently-misaligned base model (per the Ministral results), where unguided self-play can't get off the ground at all.

## Source

- `raw/research/weekly-2026-08-01/02-skill-self-play.md`

## Related

- [[skillopt]] — also treats agent skills as an optimizable artifact, but via a text-space edit optimizer at inference/deployment time rather than training-time RL curriculum generation; both treat "skill" as a first-class evolvable unit instead of a fixed prompt.
- [[seal-self-adapting]] — parallel RL-outer-loop structure: a model (or adjunct controller) learns to produce its own training artifacts (self-edits vs. skill packages) that drive downstream adaptation.
- [[qwen-agentworld]] — same lab (Qwen/Alibaba), same general theme of synthetic self-play environments for agentic training.
- [[huxley-godel-machine]] — parallel self-improving-agent structure: a controller manages a growing artifact library (skills vs. clade tree) to drive continued capability gain.
- [[gepa-reflective-prompt-evolution]] — parallel evolution of a structured artifact (skills vs. prompts) via feedback-driven refinement, though Skill-SP's proposer/solver additionally get GRPO weight updates while GEPA does not touch weights at all.
