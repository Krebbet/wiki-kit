# Harness Scaling: From Model Scaling to System Scaling

A 2026 position paper by Shangding Gu (arXiv:2605.26112) argues that the next major bottleneck in agentic AI is not model capability but system-layer design — what the paper calls "harness scaling." The thesis holds that agent performance emerges from the structured execution layer wrapped around a foundation model, and that current evaluation frameworks, which reduce agents to final-task success while treating memory, retrieval, tool use, orchestration, and governance as implementation details, are increasingly inadequate. The paper proposes a six-component decomposition of the agent harness, names three core bottlenecks (context governance, trustworthy memory, dynamic skill routing), and outlines a seven-dimension benchmark agenda to move evaluation beyond one-shot task success.

## Source

Shangding Gu. "From Model Scaling to System Scaling: Scaling the Harness in Agentic AI." arXiv:2605.26112 [cs.AI], submitted 25 May 2026.
- Abstract: https://arxiv.org/abs/2605.26112
- DOI: https://doi.org/10.48550/arXiv.2605.26112

**Coverage note:** Only the abstract page was captured (pymupdf rendered the HTML abstract, not the full PDF body). All claims on this page derive from the abstract. The six-component decomposition, three bottlenecks, seven benchmark dimensions, and CheetahClaws comparison are named in the abstract but their full treatment awaits a deeper capture of the paper body.

## The Harness Scaling Thesis

The paper's central claim is that scaling the harness — treating the structured execution layer around a foundation model as a first-class object of design, evaluation, and optimization — is what future progress in agentic AI depends on, as much as stronger foundation models.

The argument is that LLMs now enable tool use, retrieval, memory, and long-horizon workflows, but evaluations still credit or blame the model alone. The harness (everything except the weights) shapes whether that capability translates into reliable long-horizon behavior. Treating harness components as secondary details leaves the actual bottlenecks unaddressed and unmeasured.

## Six-Component Harness Decomposition

The paper proposes that agent performance emerges from the interaction of six named components:

1. **Foundation model** — the base LLM
2. **Memory substrate** — persistent and working memory
3. **Context constructor** — assembles what goes into the context window at each step
4. **Skill-routing layer** — selects and dispatches tools, sub-agents, or specialized modules
5. **Orchestration loop** — coordinates execution across steps and components
6. **Verification-and-governance layer** — validates outputs and enforces constraints

Together these constitute "the agent harness," which the paper frames as the translation layer between model capability and long-horizon agent behavior.

## Three Core Bottlenecks

The paper identifies three bottlenecks as the crux of harness scaling:

- **Context governance** — managing what enters and persists in the context window across long-horizon runs; overflow, staleness, and signal dilution degrade performance independently of model quality.
- **Trustworthy memory** — persistent memory that remains accurate, attributable, and hygienically maintained across sessions and updates.
- **Dynamic skill routing** — real-time selection of the right tool, API, or sub-agent for each step; static routing schemes break down as task complexity and tool inventories grow.

These three are described as coordinated and constrained by orchestration and governance mechanisms, the other two components in the decomposition.

## Harness-Level Benchmark Agenda

The paper proposes moving evaluation beyond one-shot task success to a seven-dimension harness-level benchmark agenda:

1. Trajectory quality
2. Memory hygiene
3. Context efficiency
4. Communication fidelity
5. Verification cost
6. Safe evolution over time
7. (One-shot task success as the baseline to be surpassed, not the ceiling)

The motivation is that each dimension captures a failure mode that task-success metrics can miss entirely — an agent can solve a benchmark task while accumulating corrupted memory, burning context budget unsustainably, or producing unverifiable intermediate steps.

## Reference Implementation: CheetahClaws

The paper introduces CheetahClaws (https://github.com/SafeRL-Lab/cheetahclaws), a Python-native open-source reference harness that instantiates the six-component architecture. The abstract states it is compared against Claude Code and OpenClaw. Quantitative results are not visible from the abstract alone; collect-but-confirm pending full paper capture.

## Related

[[patterns/agentic-harness-engineering]] — AHE is the empirical instantiation of harness evolution: benchmark-driven real-world harness development; this paper provides the naming thesis and taxonomy that AHE's observations fit into.

[[patterns/moss-production-self-evolution]] — MOSS is a concrete production instance of "safe evolution over time," one of the seven proposed benchmark dimensions; it operationalizes harness self-rewriting under live constraints.

[[patterns/code-as-agent-harness]] — the three-layer taxonomy (Harness Interface / Mechanisms / Multi-Agent Scaling) overlaps substantially with the six-component decomposition; code-as-substrate framing is adjacent to the harness-as-first-class-object thesis.

[[patterns/harness-design-space]] — empirical 70-project survey of harness design dimensions; directly complements the six-component decomposition and three-bottleneck framing with observed patterns from production systems.

[[patterns/externalization-survey]] — Zhou et al.'s weights→context→harness arc is the closest prior vocabulary for the harness-scaling thesis; both frame the harness as the emerging locus of agent capability.

[[patterns/topology-taxonomy]] — both address long-horizon context loss and multi-component coordination as structural problems; topology taxonomy provides a coordination-substrate lens on the same decomposition.
