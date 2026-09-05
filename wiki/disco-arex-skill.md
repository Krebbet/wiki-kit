# DisCo / AREX-Skill Library

BAAI/USTC/RUC (arXiv:2609.02749) present DisCo, a skill-powered research agent that distills GitHub repositories and papers into verified, agent-facing "AI4AI" skill graphs — the AREX-Skill Library — used as fixed operating context that lifts a frozen GPT-5.5+Codex research agent's scores substantially across four benchmarks with no change to model or harness.

## Method

Formalizes operational knowledge `K` as a third component of agentic systems (beyond backbone and harness), instantiated as Anthropic-spec Agent Skills. A fixed four-stage pipeline — scope → ground → construct → verify — distills a source (repo/paper) or a concrete task into a *skill graph* with routing/dependency/composition edges, gated by repo-native tests/CLI/smoke-script verification. DisCo runs in Creator mode (writes accepted graphs to the library) and Researcher mode (retrieves task-relevant branches at execution time), over the same fixed backbone/harness — no gradient updates, no RL. Library-scale routing uses an LLM-induced two-level taxonomy (20 areas, 178 capability families) over 5,000+ skills distilled from 1,000 repos, at ~$40/repository one-time construction cost.

## Results

Held constant across all evals (GPT-5.5 backbone, Codex harness): **MLE-bench** Any-Medal 31.11%→72.89% (+134.3% relative), beating the best public baseline by +8.45pp. **PaperBench** replication score 29.45%→39.59% (+34.4% relative, 18/20 tasks improved). **FrontierCS** 70.63→77.14 (+9.2% relative), Pareto-dominant over Claude Code+Opus 4.8 and Gemini CLI+Gemini 3.1 Pro using 3.1–3.3× fewer tokens. **PassNet** AS Score 1.343→1.5313 (+14.0% relative), beating TorchInductor.

Code released: github.com/VectorSpaceLab/AREX-Skill (library + pipeline); no open weights (proprietary GPT-5.5/GPT-5.6-sol backbone).

## Applicability

Any project running an autonomous coding/research agent with Agent Skills support that repeatedly touches known ML libraries, repos, or papers. Prerequisites: a frontier backbone/harness already consuming SKILL.md via progressive disclosure, budget for one-time distillation, and verification infra to gate skill acceptance. No RL or base-model access needed — purely an inference-time knowledge-layer addition.

## Related

- [[skillopt]] — closest sibling: skillopt iteratively *edits* existing skill documents under validation gates; DisCo *creates* skills from scratch via one-shot source distillation.
- [[skill-self-play]] — parallel skill-library-growth mechanism, via GRPO co-evolutionary self-play rather than static-source LLM distillation, at much smaller scale.
- [[memoharness]] — DisCo leaves the harness completely unmodified and only supplies skills as context, vs. memoharness's full-harness editing.
- [[macaron-v1]] — DisCo is a counterpoint to this wiki's "harness-as-training-target" cluster (harness untouched, only operational knowledge changes).
- [[argus-agentic-runtime]] — DisCo's Creator/Researcher mode split is a milder, non-self-evolving analog of Argus's evidence-gated self-evolution.
- [[ai-agents-open-ended-research]] — caveat: DisCo's gains are confined to verifiable-benchmark settings, doesn't bear on open-ended-judgment failure modes documented there.
