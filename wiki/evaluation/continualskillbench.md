# ContinualSkillBench

ContinualSkillBench (arXiv 2608.03874, Peking University / Beijing Institute for General Artificial Intelligence) is a dynamic five-domain, 100-subtask-per-domain benchmark testing whether LLM agents truly evolve reusable skills over a task sequence, or merely adapt to accumulated in-context feedback. Its headline finding directly challenges self-improving-agent and continual-learning-agent narratives: explicit, agent-driven skill maintenance provides **no consistent aggregate advantage over pure in-context learning**, and weaker models accumulate larger, more fragmented, less-reused skill collections than stronger ones. As an author-run benchmark not yet independently replicated, all quantitative claims here are collect-but-confirm.

## Methodology

Five domains — Law, Healthcare, Finance, Mathematics, Office — each contribute 100 interconnected subtasks drawn from a three-tier task pool (foundational knowledge benchmarks, open-ended agent benchmarks like GAIA/ClawBench, and complex human-evaluated benchmarks like OneMillionBench). Tasks are ordered via an LLM-built pairwise skill-dependency graph: GPT-5.4 judges YES/PARTIAL/NO transfer between 200 sampled task pairs per domain (400 directional judgments), followed by difficulty-constrained topological ordering and human review. Structural validation shows 69.5% of eligible tasks (macro-average across domains) reuse at least one core skill from earlier in the sequence, and the curated ordering beats random permutations on skill-coverage at 1/5/10-task history windows.

The benchmark runs on the Harbor framework with two sequential-agent harnesses (Codex CLI, Claude Code). Each subtask follows a 3-turn protocol — task + skill repository → execute → reflect — with Create Skill and Modify Skill meta-skills available during the reflection turn. Four evaluator types are used: Exact Match/F1, Numeric (tolerance ε ≤ 10⁻⁴), an LLM Rubric Judge, and Programmatic checks (executable tests, including official GAIA/ClawBench evaluators).

**The key design move** for isolating true skill abstraction from in-context adaptation is a three-condition comparison: **Independent** (fresh context and an empty skill repo per task — the baseline), **Sequential** (full skill-repo retention plus context/feedback retention), and a pure **In-Context Learning (ICL)** condition that retains context and feedback across the sequence but is *not allowed* to create or modify skills. The Sequential-vs-Independent gap alone conflates skill maintenance with general context retention; the ICL condition isolates the marginal value that explicit skills add on top of context retention.

Only three models/harnesses were evaluated — GPT-4o, GPT-5.3-Codex, and Claude 4.7 Opus — an explicit cost limitation of running sequential agent evaluation; no Gemini or other Claude/GPT variants are included.

## Headline results

- Sequential execution improves normalized reward in 14 of 15 model–domain combinations and raw reward in 13 of 15; macro-average absolute gains are +0.071 raw / +0.078 normalized (roughly 16–17% relative improvement over the Independent baseline).
- Gains are model-dependent and not tied to baseline strength: GPT-5.3-Codex shows the largest average normalized gain (+0.098), then GPT-4o (+0.077), then Opus 4.7 (+0.058) — despite Opus 4.7 having the strongest Independent baseline.
- Gains are domain-dependent: Healthcare shows the largest improvement (+0.149); Finance +0.076, Law +0.058, Office +0.054, Math +0.052. The only regression is Opus 4.7 on Math (−0.008).
- **Core finding** (ICL vs. explicit skills, GPT-5.3-Codex, three domains): average normalized reward is 0.466 for Independent, 0.605 for pure ICL, and 0.602 for skill-maintaining Sequential. Explicit skill maintenance provides no consistent aggregate advantage over pure in-context learning — Sequential slightly beats ICL in Law and Finance but trails it in Healthcare. Explicit skills do help selectively: Exact Match scores in Law/Finance, and Programmatic scores in Healthcare (0.250 → 0.500), while ICL scores higher on the open-ended Rubric judge across all three domains.
- **Skill fragmentation:** GPT-4o accumulates 384 skills across the five domains versus 205 for GPT-5.3-Codex, but GPT-4o's skills are invoked less frequently and score lower on quality — the weaker/older model builds a larger, more fragmented, less-reused skill collection, while the stronger model consolidates a more compact, higher-utility library.

## Authors' conclusion

Current in-context skill-evolution mechanisms support continual adaptation but "still struggle to consistently consolidate experience into robust and transferable skills." The paper's framing explicitly targets platforms like Claude Code and Codex, which ship exactly this kind of autonomous skill-authoring mechanism.

## Caveats

Author-run benchmark (single Peking University / BIGAI team), not yet independently replicated. The task-dependency graph and rubric judges are self-graded (LLM-as-judge), the same general caveat class as other LLM-judged benchmarks already in this wiki. Only three models/harnesses were evaluated. Treat the 16–17% relative-gain figure, the 384-vs-205 skill counts, and the 0.605-vs-0.602 ICL-parity result as collect-but-confirm.

## Tension with the skill-library value hierarchy

[[memory/memory-evolution-survey]]'s Storage → Reflection → Experience axis places skill libraries (the "Experience" tier) above Reflection and Storage as the more advanced, more valuable mechanism. ContinualSkillBench's finding that skill-maintaining Sequential execution ties pure ICL on average directly pressures that implicit ordering — it's a challenge to the *value assumption* embedded in the taxonomy, not a claim the survey makes explicitly about benchmarked performance, so it reads as an open tension for a future curator ruling rather than a hard factual contradiction.

## Source
- arXiv 2608.03874, "ContinualSkillBench: Can LLM Agents Truly Evolve Their Capabilities?" (Peking University / Beijing Institute for General Artificial Intelligence), submitted 2026-08-04 — `raw/research/weekly-2026-08-09/05-continualskillbench.md`.

## Related
- [[evaluation/agents-last-exam]] — sibling 2026 evaluation-cluster benchmark with a parallel "headroom" finding (domain knowledge, not execution, is the dominant failure mode there) versus this paper's "consolidation, not adaptation, is the failure mode" — both push back on over-optimistic agent-capability narratives.
- [[evaluation/open-world-agents]] — parallel distributional-shift/failure-mode taxonomy; both are diagnostic-tier benchmark designs meant to unmask capability illusions rather than just rank leaderboard position.
- [[evaluation/rigorbench]] — parallel argument that outcome-only reward metrics hide important behavioral distinctions: RigorBench targets process discipline, this benchmark targets skill-abstraction quality versus raw reward.
- [[patterns/skillos]] — the most direct architectural contrast. SkillOS trains an RL-tuned curator over a frozen executor and reports real ALFWorld gains from explicit skill curation; ContinualSkillBench evaluates *naive*, ungated agent-driven skill creation and finds it ties pure ICL — suggesting SkillOS's gains come specifically from the trained-curator mechanism, not from explicit skill maintenance per se. This is a boundary condition on when explicit skill libraries pay off, not a contradiction between the two papers.
- [[patterns/agent-skills]] — that page's skill-authoring guidance is oriented to human-authored, well-designed skills; ContinualSkillBench tests the harder case of autonomous skill authoring from task feedback alone and finds it underdelivers relative to the human-authored ideal.
- [[memory/memory-evolution-survey]] — see the tension noted above.
- [[patterns/sdar]] — a complementary data point: SDAR distills privileged in-context signal into model weights at training time rather than maintaining skills at inference, and also reports gains over skill-based baselines — another indication that naive test-time explicit-skill mechanisms may be a weaker lever than either trained curation or weight-level distillation.
- [[patterns/moss-production-self-evolution]] and [[patterns/agentic-harness-engineering]] — both describe self-evolving *harness* mechanisms with strong external eval-gating driving the evolution loop, unlike this benchmark's unguided agent-driven skill creation. Useful boundary case for [[patterns/topology-taxonomy]]'s self-evolving-harness section: guided/gated self-evolution (MOSS, AHE) versus ungated in-context self-evolution (this paper), where only the latter is shown not to consolidate reliably.
- [[patterns/agent-plugins-spec]] — Agent Plugins' skills-distribution format assumes human-authored skills as the unit of value being packaged; this benchmark's finding is a relevant caution for any ecosystem that instead expects agents to author their own skills autonomously.
