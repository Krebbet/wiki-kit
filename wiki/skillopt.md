# SkillOpt: Executive Strategy for Self-Evolving Agent Skills

Microsoft Research introduces SkillOpt, a text-space optimizer that treats an agent's skill document as an external parameter and trains it via scored-rollout feedback, achieving best-or-tied results across all 52 (model × benchmark × harness) evaluation cells with zero inference-time overhead.

## Source

- `raw/research/weekly-2026-06-03/01-skillopt.md` (arXiv:2605.23904, May 2026)

## Method

SkillOpt frames agent skill optimization as the text-space analogue of weight-space gradient descent: a frozen target agent is the "model", and its skill document is the "external state" (parameter) being optimized. A separate optimizer model consumes scored rollouts and proposes bounded add/delete/replace edits to a single skill document.

Three training-hygiene mechanisms stabilize optimization:
1. **Textual learning-rate budget** — caps edit magnitude per step, preventing catastrophic single-step changes.
2. **Rejected-edit buffer** — retains failed edits to inform future proposals (analogue of momentum with negative examples).
3. **Epoch-wise slow/meta updates** — separates frequent incremental refinements from larger structural revisions.

An edit is accepted only when it strictly improves a held-out validation score. At deployment, no additional inference-time model calls are required — the optimized skill artifact is consumed directly by the frozen target agent.

## Results

Evaluated across six benchmarks, seven target models (including GPT-5.5, GPT-4.1-Mini, Claude Code), and three execution harnesses (direct chat, Codex, Claude Code):
- **52/52** (model, benchmark, harness) cells: SkillOpt is best or tied, beating human-authored, one-shot LLM, Trace2Skill, TextGrad, GEPA, and EvoSkill baselines.
- **GPT-5.5 direct chat**: +23.5 pp average over no-skill baseline.
- **GPT-5.5 Codex**: +24.8 pp.
- **GPT-5.5 Claude Code**: +19.1 pp.
- **Transfer**: optimized skill artifacts retain value when moved across model scales, between Codex and Claude Code environments, and to a nearby out-of-distribution math benchmark without re-optimization.

## Novelty

Prior skill approaches are hand-crafted, generated one-shot, or loosely self-revised without controlled optimization dynamics. SkillOpt is the first systematic, controllable text-space optimizer for agent skills:
- Strict monotone acceptance (unlike EvoSkill, TextGrad) prevents regression.
- Zero deployment overhead (unlike TextGrad/GEPA which require inference-time optimizer calls).
- Rejected-edit buffer + textual learning rate = first application of deep-learning training hygiene to text-space optimization.

Directly compares against [[gepa-reflective-prompt-evolution]] (genetic-Pareto prompt optimizer) and outperforms it — the skill-document framing is a different unit of optimization than a prompt template.

## Related

- [[gepa-reflective-prompt-evolution]] — explicitly beaten baseline; shares the "text artifacts as optimization targets" framing but operates on prompts, not skill documents
- [[huxley-godel-machine]] — tree-search self-improving agent that modifies code/logic; SkillOpt modifies skill documents; complementary axes of self-modification
- [[agentflow]] — multi-role agentic pipeline trained on-policy; SkillOpt's optimizer-model/target-model split is a related decomposition
- [[eggroll]] — applies ES training discipline to LLM weights; SkillOpt applies analogous discipline to text space
- [[seal-self-adapting]] — RL-trained self-edit generation for weight updates; SkillOpt is the prompt/skill-document counterpart
