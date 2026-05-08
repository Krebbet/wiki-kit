# Architectural Design Decisions in AI Agent Harnesses (arXiv 2604.18071)

Hu Wei's protocol-guided empirical study of 70 publicly available agent harness projects (corpus frozen 2026-03-23) identifies five recurring design-decision dimensions — subagent architecture, context management, tool systems, safety mechanisms, and orchestration — and synthesizes five canonical architectural patterns spanning lightweight tools through enterprise platforms. Cross-project co-occurrence analysis reveals three structured decision bundles (coordination depth + context sophistication; execution isolation + governance formality; tool-registration formality + ecosystem ambition) and three analytically important non-co-occurrences, including the finding that capability growth does not automatically produce safety maturity. Registry-oriented tool systems remain dominant (34.3%) while MCP-first adoption is a clear minority (14.3%) as of Q1 2026; 40% of projects have no audit capability at all.

## Source

- arXiv 2604.18071, Hu Wei (`1990huwei@sina.com`) — `raw/research/weekly-2026-05-08/05-architectural-design-decisions-agent-harnesses.md`. Empirical design-space study. Single author; affiliation not stated in abstract or header. PDF captured 2026-05-08 via marker engine.

## Methodology

**Corpus:** 70 agent-system projects. Project list frozen 2026-03-23. 67 open-source repositories + 3 public-evidence comparison cases (including a source-visible leaked snapshot of claude-code-src and a paper/architecture-inferred case for codex). Inclusion required >~500 lines of implementation code or equivalent architectural footprint and at least one inspectable infrastructure capability beyond a single prompt-to-API call path.

**Discovery:** systematic search (keyword families: "AI agent," "harness," "agent framework," "vibe coding," etc.) + reference tracing + snowball expansion. Not a PRISMA-style exhaustive pipeline; goal is analytic coverage rather than census reconstruction.

**Investigation protocol:** 14-module per-project SOP — overview, architecture, runtime loop, orchestration, tool system, sandbox execution, workspace filesystem, memory system, subagent relations, model abstraction, observability/debug, safety governance, technical environment. LLM agents assisted navigation and preliminary evidence surfacing; final coding judgments required human verification of cited artifacts.

**Coding:** presence/absence observations and categorical labels. Borderline cases retained with confidence notes rather than forced into high-certainty labels. Sampled human re-review of 15 projects (21% of corpus); 94% initial field-level agreement before final consensus coding.

**Analysis methods:** descriptive statistics (RQ1), descriptive co-occurrence analysis using support / confidence / lift (RQ2 — not inferential significance tests), interpretive pattern synthesis (RQ3 — not unsupervised clustering).

## The Five Design Dimensions

### 1. Subagent Architecture

Whether and how a framework supports task decomposition through additional agent instances. Four underlying decisions: whether subagents exist, how they are created, how deeply they can be nested, and how they communicate.

| Pattern | Count | % |
|---|---|---|
| None (Single-agent only) | 21 | 30.0% |
| Basic Spawn | 5 | 7.1% |
| Tool-based Delegation | 12 | 17.1% |
| Pipeline/Stage | 1 | 1.4% |
| Orchestrator-Worker | 13 | 18.6% |
| Multi-level Recursive | 9 | 12.9% |
| Swarm/Collective | 4 | 5.7% |
| Event-driven | 5 | 7.1% |

Notable: several projects that appeared to support deep recursion were found upon source inspection to enforce explicit depth limits — documented capability may exceed implemented reality.

### 2. Context Management

How frameworks retain, compress, and reintroduce information across turns. Spans four decision axes: storage backend, compression strategy, persistence scope, and token awareness. Token budgeting (active control mechanism) differentiates architecturally mature context management from passive storage.

| Pattern | Count | % |
|---|---|---|
| Context Window only | 3 | 4.3% |
| LLM Summarization | 4 | 5.7% |
| File Persistence | 16 | 22.9% |
| Vector Database/RAG | 7 | 10.0% |
| Hierarchical | 12 | 17.1% |
| Hybrid | 19 | 27.1% |
| Enterprise | 9 | 12.9% |

The corpus center of gravity is file-persistent, hybrid, and hierarchical designs — not at either extreme. Pure context-window-only systems are rare (4.3%), consistent with context handling becoming an infrastructural concern once sessions extend beyond narrow boundaries.

### 3. Tool System

How frameworks define, register, discover, and execute tools. Three core questions: registration style, discovery/discoverability, and execution bounding.

| Pattern | Count | % |
|---|---|---|
| Minimalist (hard-coded) | 8 | 11.4% |
| Decorator-driven | 7 | 10.0% |
| Explicit Registry | 24 | 34.3% |
| Declarative/DSL | 6 | 8.6% |
| MCP-first | 10 | 14.3% |
| Plugin Ecosystem | 7 | 10.0% |
| Enterprise | 6 | 8.6% |
| Delegation/Proxy | 2 | 2.9% |

Registry-oriented systems are the modal pattern. MCP-first (14.3%) + Plugin (10%) + Enterprise (8.6%) together constitute about a third of the corpus but are not yet the majority. The paper reads this as: most frameworks formalize tools internally before committing to broader protocol-based interoperability.

### 4. Safety Mechanisms

Three recurring axes: approval workflows (none → one-off confirmation → policy-based), isolation level, and audit capability.

**Isolation level (Table 7):**

| Level | Share |
|---|---|
| No isolation | 17% |
| Process separation | 45% |
| Container isolation | 31% |
| WASM sandboxing | 7% |

**Audit capability (Table 8):**

| Capability | Share |
|---|---|
| No audit | 40% |
| Basic logging | 35% |
| Structured audit | 20% |
| Tamper-evident | 5% |

Key asymmetry: intermediate isolation is common (process + container = 76%), but high-assurance audit is rare (structured + tamper-evident = 25%). A substantial minority of projects expose broad execution power without a correspondingly strong accountability layer.

### 5. Orchestration

Two primary axes:

**Workflow definition:**
- Imperative (45%) — explicit sequential control flow
- Declarative/YAML/DSL (25%) — configuration-driven
- Event-driven (30%) — triggered by state changes or asynchronous signals

**Planning approach:**
- ReAct-style (50%) — interleaved reasoning and action
- Plan-and-Execute (35%) — planning phase separated from execution
- Hierarchical (15%) — recursive goal decomposition

Imperative + ReAct remains the default center of gravity, but declarative and event-driven options appear in a substantial minority, suggesting these choices differentiate frameworks targeting repeatable pipelines or persistent operating contexts.

## The Five Canonical Patterns

Patterns were identified by comparing recurring cross-dimensional bundles; not produced by unsupervised clustering. Each project assigned to the dominant pattern; borderline/hybrid cases recorded separately.

### Pattern 1: Lightweight Tool (21.4%, n=15)

Single-agent; in-memory or simple file state; hard-coded or decorator tools; no sandbox or basic command filtering; imperative control flow. Target: personal tools, prototypes, single-purpose assistants.

Tradeoff: minimal overhead at the cost of no support for long-running coordination, durable state, or operational control. Becomes strained when workflow scope grows.

Representative projects: subzeroclaw, shrew, babyclaw.

### Pattern 2: Balanced CLI Framework (25.7%, n=18)

Basic or tool-based delegation; file-based persistence (JSONL, Markdown); MCP-first or decorator-based registration; process-level sandboxing; declarative config; category/semantic tool routing. Target: developer-facing CLIs, coding tools, extensible productivity frameworks.

Tradeoff: practical extensibility and repeatability, short of the deeper coordination and governance of larger platforms. May become insufficient when deep subagent hierarchies or organization-wide governance are required.

Representative projects: openclaw, fast-agent, kimi-cli.

### Pattern 3: Multi-Agent Orchestrator (31.4%, n=22)

Orchestrator-worker or recursive subagent architecture; hierarchical or hybrid memory; structured tool delegation with routing; policy-based approval; container/WASM sandboxing; event-driven or structured workflow orchestration. Target: complex automation, collaborative coding, research workflow engines, multi-step execution platforms.

This is the modal pattern in the corpus. claude-code-src maps here (see [[patterns/effective-harnesses]]). Tradeoff: coordination raises cost of context management, safety design, and system comprehensibility.

Representative projects: claude-code-src, docker-agent, agentpool.

### Pattern 4: Enterprise Full-Featured (11.4%, n=8)

Multi-level recursive or event-driven subagents; enterprise memory with vector DB; full MCP ecosystem; multi-layer defense (container + policy + audit); hierarchical memory tiers; plugin architecture with versioning. Target: production deployments, security-sensitive systems, compliance-oriented platforms.

Tradeoff: high assurance and extensibility at substantially greater infrastructure, governance, and organizational cost.

Representative projects: openhands, openfang, nullclaw.

### Pattern 5: Scenario-Verticalized / Research-Oriented (10.0%, n=7)

Highly variable across all axes; one dimension sophisticated (matching research focus), others minimal or absent; security often minimal or absent; simplified infrastructure. Target: academic research, algorithm prototyping, narrow domain specialization.

Tradeoff: rapid experimentation or narrow optimization at the cost of generality, operational robustness, or governance completeness.

Representative projects: autoresearchclaw, deer-flow, deepagents (LangChain — see [[coding-agents/langchain-deep-agents]]).

## Empirical Findings Worth Quoting

**Tool system base rates:** Registry-oriented (34.3%) is the dominant tool-system pattern. MCP-first (14.3%) and Plugin Ecosystem (10%) are growing minorities. The paper states: "most projects formalize tools internally before adopting protocol-based interoperability."

**Audit gap:** 40% of the corpus has no audit capability at all. Only 5% reach tamper-evident audit trails. This is independent of isolation level: the two dimensions do not automatically co-evolve.

**Safety maturity does not follow capability:** Non-co-occurrence 3 directly states this. Some frameworks expose substantial execution power while retaining only modest oversight. The safety landscape across the corpus is uneven rather than a single maturity trajectory.

**File persistence and coordination depth:** File persistence is present in 85% of Orchestrator-Worker pattern cases vs 20% of single-agent cases (Pattern 1), consistent with coordination complexity raising state-sharing pressure.

**Co-occurrence metric for execution isolation + governance:** Support 0.89, lift 3.4. 100% of container-isolated projects implement policy engines, vs 23% of projects without container isolation. Security-score gradient: container 4.5 → process 3.2 → none 2.1.

**MCP and discovery:** MCP-first projects average 4.62 on tool discovery vs 3.86 for registry-centered vs 2.81 for minimalist systems (support 0.62, lift 2.8).

**Language does not determine architecture:** Python/TypeScript/Rust/Go all span lightweight through enterprise patterns. Advanced subagent patterns (Orchestrator-Worker through Event-driven) range 40–57% across language families.

**Use case does not determine complexity:** "General purpose" and "coding assistant" labels span the full pattern range from Lightweight Tool to Enterprise Full-Featured.

## Tensions with Existing Wiki Positions

**MCP-as-deployed-minority vs MCP-as-infrastructure:** [[deployments/mcp-infrastructure]] characterizes MCP as already transitioning to enterprise infrastructure (vendor roadmap framing). This paper's corpus (frozen 2026-03-23) puts MCP-first at 14.3% of 70 harnesses — a clear minority among deployed OSS projects. Reconciling axis: mcp-infrastructure reports vendor intent and roadmap trajectory; this paper reports deployed harness reality across open-source projects in early 2026. The two framings are compatible if MCP adoption is concentrated in vendor-tier and enterprise-tier projects rather than distributed across the OSS ecosystem.

**Governance as natural complement to coordination depth:** [[patterns/topology-taxonomy]] and [[deployments/cognition-cloud-agents]] implicitly treat governance as a natural complement to coordination sophistication. This paper's Non-co-occurrence 3 bounds that assumption: some frameworks expose broad execution power with minimal oversight. The positive co-occurrence (isolation + governance, lift 3.4) is real, but not universal — the tail of high-capability / low-governance systems is non-negligible.

**Context files and architectural maturity:** [[evaluation/agents-md-eval]] found LLM-generated context files reduce success ~3% and inflate cost >20% in well-documented Python repos. This paper treats file-persistent and hybrid context management as the corpus majority (22.9% + 27.1% = 50% of harnesses), suggesting the agents-md-eval finding may be scope-limited to a specific setting (well-documented repos, LLM-generated files) rather than indicative of file-persistent context management broadly.

## Design Guidance Extracted

The paper synthesizes four practitioner-facing implications from the empirical structure:

1. Define the intended complexity envelope before making architectural decisions; commitments accumulate as bundles, not isolated knobs.
2. Choose coherent bundles rather than maximizing feature count; many "local" enhancements are empirically associated with broader coordination and governance burdens.
3. Evaluate fit to operational demand rather than abstract sophistication; no single dominant architecture exists in the corpus.
4. Treat safety and operability as first-order design concerns alongside tool execution and workspace access; capability growth does not imply governance maturity.

The paper also notes that architectural pluralism in Agent harnesses is partly a consequence of "genuinely competing infrastructural commitments, not transient immaturity."

## Related

- [[patterns/topology-taxonomy]] — the five canonical patterns provide an empirically grounded five-class harness taxonomy that complements topology-taxonomy's multi-agent topologies; the Orchestrator-Worker subagent class maps directly onto the orchestrator-worker topology
- [[patterns/agentic-harness-engineering]] — AHE uses observability-driven evolution on a single harness; this paper is the cross-sectional view across 70; the five dimensions here provide vocabulary for what AHE evolves (memory/tools/middleware)
- [[patterns/externalization-survey]] — externalization-survey's memory + skills + protocols + harness arc maps onto this paper's five dimensions; "self-evolving harnesses" and "shared infrastructure" map to Pattern 3 and Pattern 4 respectively
- [[deployments/mcp-infrastructure]] — deployed-reality counterpoint to vendor-intent framing; MCP-first at 14.3% of corpus vs mcp-infrastructure's transition-to-infrastructure narrative
- [[patterns/effective-harnesses]] — Anthropic's initializer + coding-agent harness maps to Pattern 3 (Multi-Agent Orchestrator) with file-persistence context management; compaction-insufficiency observation aligns with this paper's finding that file persistence is more common in orchestrator-worker cases
- [[deployments/cognition-cloud-agents]] — Cognition's hypervisor-level snapshotting as context management maps to the Enterprise Full-Featured pattern bundle; governance-and-coordination assumption bounded by Non-co-occurrence 3
- [[coding-agents/langchain-deep-agents]] — deepagents appears in this corpus as Scenario-Verticalized / Research-Oriented; "shallow vs deep" axis maps roughly to Lightweight vs Multi-Agent Orchestrator pattern split
- [[deployments/openai-symphony]] — Symphony's session-log distillation + agents.md context strategy sits at the Balanced CLI / Multi-Agent Orchestrator boundary (Pattern 2/3)
- [[conflicts/agents-md-effectiveness]] — this paper's 40%-no-audit finding and Non-co-occurrence 3 add a further data point showing governance does not follow capability automatically
- [[evaluation/agents-md-eval]] — scope-of-finding tension documented above; file-persistent context management is the corpus majority here while agents-md-eval found LLM-generated context files hurt performance
