# Code as Agent Harness (arXiv 2605.18747)

102-page, ~400-reference survey arguing that code is not the target artifact of LLM agent systems but the **runtime substrate through which agents reason, act, maintain state, and coordinate** — a unifying reframe organized as a three-layer taxonomy (Harness Interface / Harness Mechanisms / Multi-Agent Scaling), with the Plan-Execute-Verify loop as the canonical control abstraction, and a position-paper argument that the next generation of multi-agent systems requires a formal, persistent, queryable shared-harness-state substrate that the current literature almost entirely lacks. Paired anchor with [[patterns/externalization-survey]]: externalization-survey asks "what gets moved out of weights"; this survey asks "what is the medium through which all of it runs." Orthogonal lenses, same literature.

## The Central Reframe

The dominant framing treats code as what LLM systems *produce*. This survey inverts that: code is the **runtime substrate** in which agentic systems operate. Three properties make code uniquely suited as harness material:

- **Executability** — the harness can verify whether what the model intended actually ran; verification is by deterministic sensor, not model self-report.
- **Inspectability** — failures surface diagnostically; stack traces, test diffs, and static analysis reports feed back as structured evidence rather than natural-language hedging.
- **Statefulness** — interaction history persists across steps as program state, not as context-window tokens.

The practical consequence: the bottleneck of long-horizon autonomy is not model reasoning quality alone but the reliability of the system connecting model outputs to persistent states across time.

## Three-Element Decomposition

Long-running agentic systems decompose into three coupled elements:

1. **Model-internal capabilities** — reasoning, planning, in-context simulation; the domain of model training and prompting.
2. **System-provided harness infrastructure** — predefined tools, APIs, sandboxes, memory stores, validators, permission tiers, workflow scaffolding; the domain of harness engineering as a discipline.
3. **Agent-initiated code artifacts** — regression tests the agent writes, temporary tools it constructs, DSL programs, executable workflows, reusable skill modules; the **relatively underexplored** element the survey foregrounds as the frontier of the field.

The survey's diagnostic: existing work has over-invested in (1) and moderately addressed (2); (3) is where the most leverage remains.

## Three-Layer Taxonomy

### Layer 1 — Harness Interface (§2)

How code mediates the model's contact with the world, across three roles:

- **Code for Reasoning** — program-delegated reasoning (offloading computation to code execution), formal-verification-grounded reasoning, iterative code-grounded chain-of-thought.
- **Code for Acting** — grounded skill selection (choosing among coded skills rather than generating free-form actions), programmatic policy generation, lifelong code-based agents that accumulate and refine skill libraries across tasks.
- **Code for Environment Modeling** — structured world representations, execution-trace world modeling, code-grounded evaluation environments, verifiable environment construction for agentic testing.

### Layer 2 — Harness Mechanisms (§3)

The operational machinery inside a single-agent harness:

- **Planning** — linear decomposition, structure-grounded planning, search-based planning, orchestration-based planning.
- **Memory** — six-type sub-taxonomy specific to code agents: working memory (repair trajectory management), semantic memory (repository evidence retrieval), experiential memory (cross-task transfer from past debugging records), long-term memory (validated experience governance), multi-agent memory (shared blackboard / belief-state synchronization), context compaction and state offloading (the active-context ↔ durable-artifact boundary).
- **Tool Use** — function-oriented, environment-interaction, verification-driven, workflow-orchestration.
- **PEV Control** (Plan-Execute-Verify) — the canonical harness control abstraction; see below.
- **Agentic Harness Engineering (AHE)** — deep telemetry + Evolution Agent cycles; see [[patterns/agentic-harness-engineering]] for the dedicated paper.

**Permission tier model** runs through all mechanisms: read-only (browsing, retrieval, static inspection) → sandbox-edit (local patching, test execution, temp dependency install) → full-access (network, credentials, deployment, destructive FS ops, Git history mutation; mandatory HITL gates at this tier).

### Layer 3 — Scaling the Harness (§4)

Multi-agent orchestration viewed as an extension of the single-agent harness substrate:

- **Role taxonomy** — Manager, Planner, Coder, Reviewer, Tester, Executor as typed harness participants.
- **Interaction modes** — collaborative synthesis, critique-and-repair, adversarial validation, reasoning debate.
- **Workflow topologies** — chain/waterfall, cyclic-agile, hierarchical, star, objective-driven adaptive.
- **Shared harness synchronization** and convergence criteria — correctness, security, performance, score-based, consensus, implicit.

## The PEV Loop as Canonical Control Abstraction

Plan-Execute-Verify is the survey's load-bearing control structure:

- **Plan** forms a contract (structured decomposition, invariant specification, or test-first skeleton) that makes intent inspectable before execution.
- **Execute** is sandboxed and permissioned; the harness governs what the model is allowed to do, not the model itself.
- **Verify** uses deterministic sensors — tests, linters, static analysis, fuzzers — not model self-report. Termination is governed by verification outcome, not model confidence.

This makes failure modes legible: a failed test is evidence, not an opinion. The PEV loop is the mechanism by which executability and inspectability translate into closed-loop reliability.

## Shared-Harness-State Formality Spectrum

The survey identifies four levels of shared harness representation across multi-agent systems, and finds that the vast majority of existing literature operates at level 1:

1. **Implicit / file-only** — agents exchange through files and loosely-structured outputs; no formal shared state. Most common. The survey argues this is the root cause of multi-agent brittleness, not a scalability trade-off.
2. **Repository-based** — Git repository as the shared artifact; structured but not queryable at runtime.
3. **Execution-based** — shared oracle signals (objective functions, test suites) as the coordination medium; structurally stronger.
4. **Blackboard / shared-state** — formal, persistent, queryable program state accessible to all agents; closest to a principled substrate. Rare in practice.

**Key finding:** topology complexity inversely correlates with substrate formality. Elaborate adaptive topologies — EvoMAC's dynamic DAGs, SEW's workflow mutation, objective-driven reconfiguration — are **symptoms of a missing formal substrate**, not advances in coordination. Systems that invest in a formal shared substrate can use simpler, more stable topologies. This is the survey's sharpest diagnostic claim about the current literature.

## AHE: Harness Engineering as a Discipline

The survey treats [[patterns/agentic-harness-engineering]] (AHE) as one of three strands of Layer 2 harness mechanisms and as the paper that names the discipline. The core loop: observe trajectories → diagnose failure modes → propose candidate revisions → evaluate on held-out tasks → promote only regression-safe improvements. The harness itself is the object of measurement and improvement, not only the model or the prompt.

Directly cites [[patterns/effective-harnesses]] (Anthropic blog) as evidence that planning, generation, and evaluation must be distinct roles, with structured artifacts and independent evaluation — an instance of PEV at the implementation level. The `feature_list.json` / `claude-progress.txt` pattern named there is a direct instance of what the survey calls a "filesystem-backed control object."

## Harness as Distillation Surface

A 2026 trend the survey names explicitly: production harnesses — Cursor Composer (continuous online RL on real usage traces), Codex harness, Claude Code dogfooding — are becoming the **primary training data source** for the next model generation. The boundary between "the agent" and "the harness around the agent" is eroding. The harness is no longer just the runtime; it is the training-data generator that shapes the next model's internal capabilities. This closes a feedback loop that the three-element decomposition (model-internal / system-provided / agent-initiated) treats as separate: the harness writes the model.

This connects directly to the externalization arc in [[patterns/externalization-survey]] — if the harness becomes the distillation surface, "externalization" and "internalization" are no longer stable opposites.

## Execution Feedback: A Collect-But-Confirm Finding

Self-Collaboration and QualityFlow results (cited in §4.4) show LLM-simulated execution achieving 98%+ precision/recall predicting actual test outcomes, suggesting execution grounding's value is not uniform: linguistic simulation may suffice for many failure modes, while real execution remains essential for runtime crashes, resource exhaustion, and boundary conditions. **Collect-but-confirm**: this 98%+ figure is second-hand synthesis from two systems in a survey; it adds nuance to the assumption that real execution is always necessary, but should not be treated as a settled result without consulting the primary papers.

## Seven Open Problems

1. **Harness-level evaluation** beyond final task accuracy — trajectory efficiency, verification strength, recovery ability, state consistency, safety compliance, replayability.
2. **Semantic verification beyond executable feedback** — oracle adequacy, evidence bundles, verification scope declaration; many real-world states are not fully testable.
3. **Self-evolving harnesses without regression** — change contracts, canary deployment, rollback semantics for harness mutations.
4. **Transactional shared program state** and semantic conflict resolution across concurrent agent writes.
5. **HITL safety and accountability as durable harness state** — human oversight must be recorded and replayable, not just injected ad hoc.
6. **Multimodal code-harness systems** — bridging code-based harness reasoning with visual and embodied domains.
7. **A science of harness engineering** — principled methods for designing, measuring, and evolving harnesses; currently practitioner art.

## Relationship to the Externalization-Survey Anchor

[[patterns/externalization-survey]] (Zhou et al., arXiv 2604.08224) and this survey are the wiki's two cross-cutting vocabulary anchors for the 2024–2026 agentic stack. They are complementary and orthogonal:

- Externalization-survey organizes by **what is moved** — memory, skills, protocols, harness as four coupled externalizations from weights → context → harness.
- This survey organizes by **the medium through which all of it runs** — code as the substrate with executability, inspectability, and statefulness as its harness-relevant properties.

Both surveys draw on the same literature. Neither contradicts the other. The reason this is a separate anchor page rather than an extension of externalization-survey is that the organizing thesis is different: externalization-survey's question is ontological ("what is being externalized?"); this survey's question is substrative ("what is the runtime medium?"). The answer to the second question — code — applies equally to all four of the first survey's externalization dimensions.

## Source

- `raw/research/weekly-2026-05-25/05-code-as-agent-harness.md` — captured 2026-05-25 via pymupdf fallback (marker crashed on 102-page file); ~22 figure image-binaries absent, all text intact.
- arXiv 2605.18747 — survey, ~400 refs, 102 pages.

## Related

- [[patterns/externalization-survey]] — complementary vocabulary anchor; "what gets externalized from weights" vs. "the medium through which it runs." Most important cross-link.
- [[patterns/agentic-harness-engineering]] — AHE paper (arXiv 2604.25850) cited directly as a Layer 2 strand; this survey provides its broader taxonomic context.
- [[patterns/effective-harnesses]] — Anthropic blog cited in §3.1.4; `feature_list.json`/`claude-progress.txt` as filesystem-backed control objects, PEV in practice.
- [[patterns/harness-design-space]] — 70-project empirical harness survey; direct empirical counterpart to this survey's taxonomic framing.
- [[patterns/topology-taxonomy]] — Layer 3 multi-agent orchestration here is the most systematic topology treatment in any source the wiki has ingested; the inverse-correlation finding (topology complexity ↔ substrate informality) belongs there.
- [[deployments/openai-symphony]] — cited directly; "code for agent legibility," skill + session-log distillation as harness-interface and harness-as-distillation-surface instances.
- [[case-studies/notion-token-town]] — "build for what the model understands" maps to code-for-environment-modeling; 100+ tools with progressive disclosure as tool-lifecycle control.
- [[patterns/skillos]] — frozen executor + RL-trained skill curator as lifelong code-based agents (§2.2.3) and experiential memory (§3.2.3).
- [[coding-agents/langchain-deep-agents]] — LangChain harness anatomy and "improving deep agents" guides cited directly; convergent engineering lessons.
- [[patterns/agent-development-lifecycle]] — Build→Test→Deploy→Monitor framing cited; this survey provides the academic taxonomy beneath "Build" and "Monitor→Iterate."
