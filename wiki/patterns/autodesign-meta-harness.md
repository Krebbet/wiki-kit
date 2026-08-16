# AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design

arXiv:2608.13560 (Luo et al., submitted 2026-08-13) introduces AutoDesign, a framework in which a "meta-harness optimizer" observes rollout feedback and directs a separate code agent to recursively rewrite its own task harness — pursuing what the abstract calls "recursive self-improvement," applied here to academic paper-to-poster generation. AutoDesign beats the closed-source commercial system "Claude Design" on a new benchmark (PosterBench) and wins a system-blind human preference study. This is the second strong positive data point (alongside [[patterns/agentic-harness-engineering]]) that automatic harness evolution measurably lifts performance — and it sits in tension with [[evaluation/continualskillbench]]'s finding that explicit in-context skill maintenance barely beats plain in-context learning.

**Capture caveat**: the raw source is the arXiv abstract/landing page only (no full-text PDF body was captured) — treat Method and Results detail below as abstract-level, not full-paper-verified, until a full-text ingest happens.

## Method

A meta-harness optimizer module observes rollout feedback (success/failure and quality signals from generation attempts) and directs a code agent to recursively edit and improve the task harness, producing a learned artifact called "DesignHarness." The abstract frames this as pursuing recursive self-improvement aligned with "human design priors," contrasted against "existing paradigms [that] remain static." A reported example run executes 253 tool calls across 11 editing turns within 40 minutes for under $3. The two-role separation (optimizer proposes, code agent implements) is inferred from the abstract's phrasing and should be confirmed against the full paper/repo before being treated as established.

## Results

- Introduces **PosterBench**: a 100-paper Main Track spanning five disciplines, plus **PosterBench-mini**, a shared 10-paper subset for controlled evaluation.
- On the PosterBench Main Track, AutoDesign scores **78.32**, beating the closed-source commercial system Claude Design by **7.45 points**.
- Across seven controlled code-agent-model configurations, adding the learned DesignHarness lifts the average PosterBench Score from **54.99 to 67.39 (+12.4%)** — the benefit generalizes across different underlying agent/model pairings, not just one configuration.
- A system-blind human study reports AutoDesign achieves the highest human preference among evaluated systems, reaching "average conference-poster quality."
- Cost/efficiency: 253 tool calls, 11 editing turns, ~40 minutes, under $3 per full autonomous run.

## Applicability

Domain-specific: paper-to-poster generation (multimodal source → structured design output), not general coding. Requires a code agent to execute harness edits plus an LLM backbone; evaluated across seven different code-agent-model configurations, suggesting the mechanism is agent/model-agnostic to some degree. Requires PosterBench (or an equivalent rollout-feedback source) to drive the recursive improvement loop.

## Novelty

Distinguishes itself from prior harness-evolution work by: applying automatic/recursive harness evolution to a creative multimodal design-generation task rather than coding or terminal-agent benchmarks; explicitly targeting alignment with human design priors as an objective, not just task success rate; introducing a new benchmark with human-eval and system-blind preference studies rather than relying solely on an automated scorer; and reporting a head-to-head win against a named closed-source commercial system rather than only open baselines. It sits in the same "meta-harness optimizer recursively improves harness from rollout feedback" lineage as [[patterns/agentic-harness-engineering]] (AHE) and [[patterns/moss-production-self-evolution]] (MOSS), but is the first of that group evaluated on a design/creative-output task with a commercial-system comparison point.

## Reproducibility

Code released: https://github.com/Yaxin9Luo/AutoDesign. No mention in the abstract of released model weights (the framework orchestrates existing LLM backbones/code agents rather than training new weights). Benchmark availability is not explicitly confirmed in this abstract-only capture — collect-but-confirm pending full-paper/repo review.

## Tension with ContinualSkillBench

[[evaluation/continualskillbench]] found explicit agent-driven skill maintenance statistically indistinguishable from plain in-context learning (0.602 vs. 0.605 normalized reward) and used this to challenge self-improving-agent narratives broadly. AutoDesign reports a much larger, generalizing lift from an explicit self-rewriting harness, on a different task domain.

This is a scope-limited tension, not a strict contradiction: the two papers evaluate different mechanisms (harness-level rewriting of tools/workflow vs. ContinualSkillBench's in-context skill-library maintenance) on different task domains and metrics. AutoDesign is also a single-paper, abstract-only-verified claim with no third-party replication, while ContinualSkillBench is a purpose-built adversarial-style benchmark designed to stress-test self-improvement claims. Worth distinguishing as possibly two different mechanisms with different empirical track records — "harness/tool-level self-rewriting" (AHE, AutoDesign — now 2-for-2 positive) versus "in-context skill-library maintenance" (ContinualSkillBench — negative) — rather than lumping both under one "self-improvement" bucket.

## Source

- arXiv:2608.13560 — Luo et al., "AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design" (2026-08-13, Tech Report)

## Related

- [[patterns/agentic-harness-engineering]] — structurally the same "meta-optimizer recursively evolves the harness from rollout feedback" idea; a second corroborating data point for automatic harness evolution, this time in a non-coding domain against a closed commercial baseline
- [[patterns/moss-production-self-evolution]] — same self-evolving-harness mitigation class; MOSS is production/real-user-failure-driven, AutoDesign is benchmark/rollout-driven
- [[patterns/skillos]] — parallel line of policy/curator-trained self-improvement via RL over a frozen executor, vs. AutoDesign's code-agent-executed harness rewriting
- [[evaluation/continualskillbench]] — direct thematic tension; see above
- [[patterns/harness-design-space]] and [[patterns/externalization-survey]] — AutoDesign is a concrete instance of the "self-evolving harness" direction both already name as an emerging pattern
- [[patterns/topology-taxonomy]] — belongs in the self-evolving-harness mitigation class alongside AHE, MOSS, and SkillOS
