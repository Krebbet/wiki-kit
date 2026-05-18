# SkillOS — Learning Skill Curation for Self-Evolving Agents (arXiv 2605.06614, May 2026)

Google Cloud AI Research paper that decouples a **frozen agent executor** from a **trainable skill curator** operating over an external Markdown SkillRepo. The curator emits `insert_skill` / `update_skill` / `delete_skill` function calls and is trained with GRPO over **grouped task streams** — earlier trajectories edit the repo, later related tasks evaluate whether those edits help. The grouped-task construction is the load-bearing training signal: removing it costs −3.9 pp on ALFWorld, the single largest ablation drop. SkillOS is the per-skill RL counterpart to [[patterns/agentic-harness-engineering]]'s whole-harness evolution; both are 2026 self-evolving systems on frozen base models. Currently #1 on alphaXiv trending.

## Source

- arXiv 2605.06614, "SkillOS: Learning Skill Curation for Self-Evolving Agents" — `raw/research/weekly-2026-05-11/04-skillos.md` (marker on CPU). May 2026.
- Authors: Siru Ouyang (UIUC, intern at Google), Jun Yan, Yanfei Chen, Rujun Han, Zifeng Wang, Bhavana Dalvi Mishra, Rui Meng, Chun-Liang Li, Yizhu Jiao (UIUC), Kaiwen Zha (MIT), Maohao Shen (MIT), Vishy Tirumalashetty, George Lee, Jiawei Han (UIUC), Tomas Pfister, Chen-Yu Lee. Primary affiliation: Google Cloud AI Research (corresponding: junyann, chenyulee @ google.com).
- Code: not linked in the captured text. Figure 1 references Anthropic's `anthropics/skills` repo as the SKILL.md format inspiration.

## The architectural split

Two distinct modular roles:

- **Executor (πL)** — frozen base model. Retrieves skills via BM25 top-K=5 and acts on the task. Held fixed across all experiments (Qwen3-8B, Qwen3-32B, Gemini-2.5-Pro, Gemini-3.1-Flash-Lite tested as executors).
- **Curator (πS)** — trainable. Observes the executor's trajectory + a self-judged correctness signal and emits one of three function calls — `insert_skill`, `update_skill`, `delete_skill` — against the external SkillRepo.

Training updates only πS. The decoupling is the load-bearing design choice and is repeatedly credited for generalisation across executor families and across task domains.

## SKILL.md format (the substrate)

Each skill is a single Markdown file with **YAML frontmatter** (`name`, `description`) plus a Markdown body of executable knowledge / workflows / constraints / heuristics. Curation is implemented as file I/O over the repo, framed as an OS-style interface — hence "SkillOS." The curator's three operations have JSON tool signatures (Figure 8 of the paper).

Explicitly cites Anthropic's Skills repo as inspiration. Deliberately *simplifies* the Anthropic format by **dropping two affordances**: (a) supporting scripts / external resource files (skills as runnable code), (b) hierarchical sub-skill composition. The paper acknowledges this simplification in its limitations — see [Caveats](#caveats).

## RL training recipe

### Grouped task streams (the key construction)

Each training instance is a *group of related tasks* solved sequentially. Earlier trajectories update the SkillRepo via the curator; later related tasks evaluate whether those updates helped. This is how the paper turns delayed, indirect downstream feedback into a usable training signal — and the explicit differentiator from prior short-horizon work (SkillRL, D2Skill, ARISE, Mem-α, UMEM).

### Composite reward

```
r = r^task + λ_f · r^fc + λ_u · r^cnt + λ_c · r^comp
```

| Term | Mechanism | Weight |
|---|---|---|
| **r^task** | Average success of executor on the *remaining tasks in the group* after the first (which sees an empty repo). The executor-grounded long-horizon signal. | 1.0 |
| **r^fc** | Function-call validity — fraction of curator-emitted calls that parse and execute. | 0.1 |
| **r^cnt** | Content quality — Qwen3-32B as external judge scoring abstraction / reusability / actionability / faithfulness (rubric in Fig. 12). | 1.0 |
| **r^comp** | Compression: 1 − \|S_t\|/\|x_t\|. Discourages verbatim trajectory copying into skills. | 0.05 |

KL term in GRPO is **discarded** to encourage exploration.

### Self-judged correctness signal

The task-outcome supervision channel `1_t` is obtained via **LLM-as-a-judge with the frozen executor itself** (prompts in Figs. 13/14/15). Not a ground-truth verifier, not a learned reward model — the same model self-judging. ALFWorld and WebShop have programmatic rewards available, but the paper uses LLM-judge anyway, presumably for unification with reasoning settings. See [Caveats](#caveats).

## Headline numbers

All numbers reported as mean over 3 seeds.

| Setting | Executor | Curator | SkillOS | Strongest prior baseline | Δ (abs) |
|---|---|---|---|---|---|
| **ALFWorld** | Qwen3-8B | Qwen3-8B (RL) | 61.2% SR | ReasoningBank 55.7% | **+5.5** |
| **ALFWorld** | Gemini-2.5-Pro | Qwen3-8B (RL) | 80.2% SR | no-memory 66.4% | **+13.8** |
| **WebShop** | Qwen3-8B | Qwen3-8B (RL) | Score 40.6 / SR 16.5% | strongest baseline 35.7 / 12.0% | +4.9 / +4.5 |
| **Reasoning (AIME24+25, GPQA-D)** | Qwen3-8B | Qwen3-8B (RL) | 73.8% avg | no-memory 69.6% | +4.2 |
| **Cross-executor transfer (App. C.1)** | Gemini-3.1-Flash-Lite | Qwen3-8B (RL) | 73.1% SR | ReasoningBank 66.0% / no-memory 61.2% | +7.1 / +11.9 |

Step counts also drop (e.g. ALFWorld 21.1 → 18.9 with Qwen3-8B executor).

**The 8B-curator-beats-Gemini-2.5-Pro-curator finding.** SkillOS-gemini (Gemini-2.5-Pro as curator, no RL) underperforms RL-trained Qwen3-8B curator on most settings. Stronger raw curator does not guarantee better skill curation; *executor-grounded RL training* matters more than curator scale. Quoted: *"Our 8B curator also outperforms Gemini-2.5-Pro when used directly as the curator."*

This is the cleanest architectural signal the paper offers and structurally mirrors AHE's "structural components carry the lift, model scale does not" finding ([[patterns/agentic-harness-engineering]]).

## Operation-mix dynamics (Figure 4)

- **Early training** — `insert_skill` overwhelmingly dominates (the curator blindly populates the repo).
- **Mid-to-late training** — `update_skill` increases, `insert_skill` declines, `delete_skill` grows slowly.

The curator learns to *refine* rather than just expand. The compression reward is what holds the repo size in check.

## Skill evolution becomes "richer Markdown encoding meta-skills"

**Within-skill.** Early skills add generic "tips/recommendations" sections; later skills add *failure-handling logic and conditional branches* (when to deviate from the default workflow). RL steers the curator from superficial enrichment toward execution-oriented refinement.

**Across-skills.** Early repos are dominated by narrow, task-specific skills. Late repos contain *meta-strategy* skills covering verification, fallback planning, system search, and strategy adjustment. The curator does not just accumulate — it expands the *strategic space*.

Case study (Fig. 17a): an ALFWorld failure-recovery meta-skill that *references other skills* (compositional curation) — exhaustive search → confirm unavailability → identify substitute → proceed.

## Skill-utilisation attribution (Figure 6, ALFWorld)

Four metrics:

- **Usage rate** — SkillOS invokes a skill on 100% of evaluation examples (vs lower for baselines).
- **Successful skill-usage rate** — higher.
- **Coverage** — fraction of repo actually used; higher (curated skills aren't dead weight).
- **Skills per example** — *lower*. Gains come from precise selection, not larger context.

## Cross-task transfer (Figure 3)

Trained curator transfers across task domains. Reasoning-trained curator transfers especially well to agentic tasks (because reasoning skills encode abstract decomposition / verification / adaptive planning). Agentic-trained curators transfer less well in the other direction (more environment-specific knowledge).

## Ablations (Table 3, ALFWorld)

| Variant | SR | Steps |
|---|---|---|
| Full SkillOS-GRPO | 61.2% | 18.9 |
| w/o content-quality reward | 58.6% (−2.6) | 20.1 |
| w/o compression reward | 60.0% (−1.2) | 19.3 |
| **w/o grouping (random task sequences)** | **57.3% (−3.9)** | **20.6** |

Removing grouping is the largest single-component loss. The grouped-task-stream construction is the critical training-signal mechanism.

## Data construction pipeline (Appendix B.2)

For reasoning, each task is annotated by Gemini-2.5-Pro with a tuple of five phrase-lists: **Topic / Skills / Concepts / Heuristic Strategy / Common Pitfalls** (each phrase ≤5 words; standardised terminology only). Task pairing uses an inverted index over {Concepts, Skills, Heuristic Strategy} + a **soft-Jaccard** with sentence embeddings (all-MiniLM-L6-v2, cosine threshold 0.60). Six explicit gate conditions per pair (shared foundation, shared reasoning, not-near-duplicate, not-too-unrelated, progression, curriculum direction). Forward-curriculum mode (p↑ = 0.80) was found notably more stable than mixed.

For ALFWorld and WebShop, the existing default task-type annotations (e.g. ALFWorld's 6 task types) substitute for the annotated attribute set. Group sizes: ALFWorld 10, WebShop 10, Reasoning Random(5,12).

## Compute

- 16× H100 GPUs, verl framework.
- ALFWorld ~3 days. Reasoning ~2.5 days. WebShop ~5 days.
- GRPO: lr 1e-6, batch 32, group size 8, 50–100 steps depending on benchmark.
- Max prompt length 16,384, max response 4,096.

## Where this fits the wiki

- [[patterns/externalization-survey]] §4 (Skills externalisation as procedural-expertise) and §8.3 (self-evolving harnesses as emerging direction) — SkillOS is the canonical RL operationalisation of both, on the *skills externalization axis specifically*.
- [[patterns/agentic-harness-engineering]] — closest peer paper. Both 2026; both freeze the LLM and evolve external structure; both observe structural components carry the lift over prose-level edits. **Different scope** (whole harness vs skills only) and **different attribution mechanism** (change-manifest verification vs grouped-task downstream rewards). They do not cite each other (publication-lag); worth checking whether final SkillOS bibliography catches AHE.
- [[patterns/skill-distillation]] — apparent-not-real conflict. F-predictor argues high-F regimes favour collapsing structure entirely (single-agent + tools); SkillOS argues for evolving structured skill libraries. Different abstraction levels: F-distillation chooses between *one big agent vs MAS at the task level*; SkillOS curates *thousands of micro-skills* within a single executor. Compatible.
- [[memory/memory-architectures]] — SkillOS is the new 2026 paradigm instance of the **Policy-learned memory management** family (mechanism #5): store/retrieve/update/discard treated as callable operations within a learned policy, end-to-end RL'd against downstream task outcomes. Joins AgeMem (Yu 2026) on that family line.
- [[patterns/effective-harnesses]] — Anthropic writes `feature_list.json` + `claude-progress.txt` via prompt; SkillOS makes the artefact-curation *learned*. Same architectural class — externalised structured artefacts that bridge sessions — but different curation mechanism.
- [[case-studies/notion-token-town]] — Notion runs 100+ custom tools + progressive disclosure at scale via 4–5 hand-rebuilds; SkillOS is the academic RL answer to the same problem Notion solves by hand. Notion's "build for what the model understands" doctrine maps onto SkillOS's content-quality reward (abstraction / reusability / actionability).
- [[patterns/topology-taxonomy]] — slots in as a *policy-learned variant* of the externalised-handoff-artefacts mitigation class, alongside [[patterns/effective-harnesses]] and [[coding-agents/langchain-deep-agents]]. The artefacts here are SkillRepo entries; the curation policy is RL-trained rather than prompt-driven.
- [[patterns/harness-design-space]] — codes as: subagent architecture = pipeline (executor+curator), context management = file persistence (Markdown skills), tool system = minimalist (BM25 retrieval), safety = none discussed, orchestration = imperative ReAct/CoT.

## Tensions

- **vs [[evaluation/agents-md-eval]] / [[conflicts/agents-md-effectiveness]] (potentially real, untested).** AGENTbench finds LLM-generated context files reduce coding-agent success ~3% in well-documented Python repos. SkillOS demonstrates RL-trained Markdown-skill curation lifts agentic-task SR by 5–14 pp. Reconciling axes per the open conflict: domain (web-shopping/embodied vs Python repos), authorship (RL-trained curator vs hand-prompted `/init`), evaluation methodology (controlled benchmark with executor frozen vs natural deployment). SkillOS adds a fifth distinct authorship position to that conflict: **RL-trained curator with composite rewards**.
- **vs [[patterns/agentic-harness-engineering]] component-ablation finding (subtle).** AHE's headline ablation: prose-level edits (+system_prompt only) regress; structural edits (memory/tools/middleware) carry the lift. SkillOS evolves *prose-Markdown skills* and gets monotonic lifts. Possible reconciling axis: AHE's "system_prompt" is the *seed instruction layer* (universal discipline), whereas SkillOS skills are *retrieved per-task contextual instructions* — closer to AHE's `LongTermMEMORY.md` than its system_prompt. Worth investigating whether SkillOS skills behave more like "memory" (which AHE found load-bearing) or "system_prompt" (which AHE found regressive) in AHE's taxonomy.

## Caveats

The authors call out three limitations explicitly (Appendix D):

1. **Retrieval is BM25 only.** Joint optimisation of curation + retrieval is left to future work. As repos grow this is a foreseeable bottleneck; the paper proposes "agentic search over experiential memory" (Appendix E) but does not measure where BM25 breaks down.
2. **Simplified skill representation.** Single Markdown file only; drops Anthropic's two killer affordances (scripts as runnable code; hierarchical sub-skill composition). Behaviors most naturally expressed as code or as compositions must be flattened to prose. Re-introducing these affordances may either compound SkillOS's gains or destabilise the curator's RL signal.
3. **Frozen executor** is a methodological choice for clean attribution. Joint πS + πL training would likely yield a better-aligned pair at higher cost. Skill–executor miscalibration must be absorbed by the curator alone.

Additional open questions:

- **Curator–executor mismatch.** SkillOS-gemini (Gemini-2.5-Pro curator + Qwen3-8B executor) underperforms SkillOS (Qwen3-8B curator + Qwen3-8B executor) — paper attributes this to "frontier-generated skills may be misaligned with the executor's capacity or usage patterns." Raises whether SkillOS skills are *executor-coupled* in a way that limits portability.
- **Self-judged correctness bias.** The curator may learn to satisfy the executor's idiosyncratic notion of correctness rather than ground-truth task success. Programmatic rewards available on ALFWorld/WebShop could test this.
- **Lift gradient: agentic > reasoning.** Hypothesised cause is procedural regularity in agentic tasks vs abstract decomposition heuristics in reasoning. Could also be measurement: AIME/GPQA accuracy is more variance-bound at the per-question level than ALFWorld success rates.

## Future directions named (Appendix E)

- **Agentic search over experiential memory** — replace static top-K BM25 with iterative query reformulation by the curator or a dedicated retrieval agent. Treats memory access as a first-class policy decision. (Note: this echoes [[patterns/direct-corpus-interaction]]'s 2026 argument from a different angle.)
- **Hierarchical and compositional skills** — unlock the affordances dropped in the simplification; connects to program synthesis / library learning.
- **Multi-agent shared memory** — credit assignment when a shared skill helps one agent and hurts another. Currently an unsolved direction.

## SDAR contrast: two approaches to skill-conditioned RL on the same benchmarks

[[patterns/sdar]] (arXiv 2605.15155) addresses the same problem space on the same benchmarks (ALFWorld, WebShop) but via the opposite design choice: **SkillOS = trained curator over a frozen executor** — skill management happens at inference via an external live SkillRepo (insert/update/delete); **SDAR = gated distillation during training** — skills are injected as privileged context for a teacher branch at training only, then internalized into policy weights, leaving no runtime skill dependency. SkillOS externalizes skills permanently; SDAR internalizes them permanently. Different runtime footprint: SkillOS requires the curator + SkillRepo at inference; SDAR requires only the trained policy. Both are viable; the choice depends on whether online skill editing (SkillOS) or zero-overhead deployment (SDAR) matters more.

## Related

- [[patterns/agentic-harness-engineering]] — closest peer self-evolving system; whole-harness vs skills-only.
- [[patterns/externalization-survey]] — canonical operationalisation of the survey's skills chapter and self-evolving-harness emerging direction.
- [[patterns/skill-distillation]] — different abstraction level; compatible.
- [[patterns/agent-skills]] — the human/Claude-A *authoring* counterpart to SkillOS's *policy-learned* curation of the same skill-as-Markdown abstraction.
- [[memory/memory-architectures]] — Policy-learned memory-management family instance.
- [[patterns/effective-harnesses]] — learned-curation counterpart to Anthropic's hand-prompted artefacts.
- [[patterns/topology-taxonomy]] — policy-learned variant of the externalised-handoff-artefacts mitigation class.
- [[patterns/harness-design-space]] — five-dimension empirical comparator.
- [[case-studies/notion-token-town]] — practitioner counterpart (hand-rebuilds vs RL curation).
- [[memory/longmemeval]] — peer 2026 memory work; SkillOS's content-quality rubric is a useful complement to LongMemEval's recommended index designs.
- [[memory/mempalace]] — peer 2026 memory work.
- [[conflicts/agents-md-effectiveness]] — adds RL-trained-curator as a fifth authorship position.
- [[patterns/direct-corpus-interaction]] — same week; SkillOS's "agentic search over experiential memory" future direction echoes DCI's no-index argument from a different angle.
- [[patterns/sdar]] — parallel skill-conditioned RL on ALFWorld/WebShop; SkillOS externalizes skills at inference, SDAR internalizes them during training.
