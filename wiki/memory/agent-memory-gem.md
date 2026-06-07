# Is Agent Memory a Database? — GEM Framework

A 2026 vision paper from Concordia University (Orogat & Mansour, arXiv 2605.26252) argues that long-term agent memory is a fundamentally new data-management workload — not a database problem. The paper's central claim: correctness in agent memory is a property of the *state trajectory*, not of individual records. This abstraction gap cannot be closed by bigger context windows or better retrieval; it requires four state-level operators and six trajectory-level correctness conditions that no existing database paradigm or agent memory system satisfies simultaneously. The authors formalize this as **Governed Evolving Memory (GEM)** and demonstrate feasibility in **MemState**, a prototype built on the Kuzu embedded property graph engine.

## Core contribution

GEM replaces record-level CRUD operations with four **state-level operators** and enforces their correctness through six **trajectory-level conditions**. The key reframing: CRUD localizes correctness at individual records; GEM localizes correctness at the memory state trajectory `{S_t}_{t≥0}`. Every failure mode in current systems traces to a CRUD operation that cannot express the required semantics:

- `create` cannot integrate (appends duplicates)
- `update` cannot propagate (leaves dependents inconsistent)
- `delete` cannot regulate relevance (evicts by age or capacity, not importance)
- `read` cannot adapt (access patterns cannot reinforce important content)

Three structural observations prove these are not implementation gaps — they are impossibility results for any CRUD-based system regardless of storage model.

## Why standard databases fall short

The paper surveys five database paradigms and six families of agent memory systems against four required capabilities:

| Capability | What it provides | Who comes closest |
|---|---|---|
| **Relevance-driven retention** | Bounds active memory by utility, not capacity/age | Generative Agents (importance score at retrieval — classified as local heuristic, not a policy bounding the footprint) |
| **Dependency-aware propagation** | Keeps related facts consistent when one changes | Zep/Graphiti (bi-temporal edge invalidation — but only one edge at a time, not multi-hop) |
| **Graded attenuation** | Deprioritizes obsolete content while preserving history for audit | EverMemOS (partial: expires time-bounded foresight only) |
| **State-modifying retrieval** | Updates salience on read so accessed content stays prominent | None |

No system supports all four. Each paradigm or family contributes exactly one substrate strength. The result is four **recurring failure modes** visible in any accumulation-strategy memory:

1. **Unregulated growth** — append-only ingestion accumulates redundant entries that crowd out useful content
2. **Missing semantic revision** — updates are appended as new records, leaving outdated and current values coexisting (e.g., two conflicting deadlines returning semantically similar results)
3. **Absence of selective forgetting** — eviction is capacity- or age-driven, so low-relevance entries ("discussed lunch preferences") outlast high-utility ones ("project deadline")
4. **Read-only retrieval** — frequently accessed facts gain no importance, competing with stale content on equal terms

The paper explicitly names Claude, Claude Code, ChatGPT, and Cursor as real-world systems exhibiting these failures.

## GEM: Governed Evolving Memory

GEM defines memory as a global state tuple **S = (C, G, P)**:

- **C** — stored content organized as *semantic units*, each carrying a value history and a salience signal
- **G** — structural organization over content (a typed graph of semantic units)
- **P** — declarative policies governing access, ingestion, revision, and forgetting

Memory evolves via a state transition function: `S_{t+1} = U(S_t, I_t, Op_t)`, where `I_t` is new external input and `Op_t` is an internal operation. The sequence `{S_t}_{t≥0}` is the **memory trajectory** — the unit of correctness.

**Evolution policies** in P are typed `⟨event, condition, action⟩` rules whose conditions reference S directly. Policy postconditions are evaluated against proposed `S_{t+1}` before commit; violating transitions are rejected atomically. Policies are declarative: they specify what transitions occur and when, independent of how operators execute them, and can be modified without changing operator code.

## State operators

Four operators act over global memory under policy constraints, each supplying one of the four required capabilities:

**Ingestion** integrates input into existing state. An updated value is appended to the existing semantic unit's value history; the prior value is retained as historical evidence. C1, C2, and C4 hold by construction (no two values for the same fact have equal status; the prior is marked superseded with provenance).

**Revision** reconciles internal evidence — conflicting field values, duplicate topics, schema drift, dependency inconsistencies. It propagates updates along the structural graph G and preserves superseded values with provenance. Critically, revision traverses only *extension edges* (those with entailment semantics), not association edges (relatedness without entailment), keeping the propagation frontier small.

**Forgetting** is a policy-governed, graded process operating on salience signals rather than age or capacity. Each field maintains a salience score that rises on access and decays on disuse. Three thresholds define a ladder: below `summary` → history compressed; below `remove` → field hidden from active retrieval; below `archive` → topic archived but recoverable via explicit lookup. Forgetting is sub-unit granular — part of a semantic unit may be attenuated while the rest stays current.

**Retrieval** maps a query to output *and* induces a state transition — every read updates the salience of accessed units. This makes retrieval a first-class write operation, not a pure function. The salience increment on access closes the loop with forgetting: frequently accessed facts strictly reduce their eligibility for attenuation.

## Correctness conditions

Six conditions govern the state trajectory across three axes:

| # | Condition | Axis |
|---|---|---|
| C1 | Query soundness — returns most recent non-archived value; prior values only on explicit temporal request | What queries return |
| C2 | Transition soundness — every transition respects P; no revision makes a superseded value current | What queries return |
| C3 | Dependency consistency — update to unit u triggers evaluation of all extension-edge-connected units | What state preserves |
| C4 | Provenance preservation — forgetting and revision preserve the provenance chain of any reachable unit | What state preserves |
| C5 | Bounded active state — active memory satisfies `|C_active| ≤ B(t)` for policy-defined bound B; archived content recoverable | How state adapts |
| C6 | Retrieval-induced adaptation — every retrieval accessing u induces a salience update; repeated retrieval strictly reduces u's attenuation eligibility | How state adapts |

Every failure mode in Figure 1 of the paper maps to violation of at least one of C1–C6.

## MemState prototype

MemState realizes GEM on **Kuzu** (embedded property graph). Topics are self-contained semantic units: each has a title, summary, dense embedding, and fields with value histories. Two edge types distinguish propagation semantics from mere relatedness:

- **Extension edges** — entailment relationship; revision traverses these to propagate updates (e.g., deadline change on a project triggers milestone re-evaluation)
- **Association edges** — relatedness without entailment; used for retrieval context expansion only

The atomic commit mechanism lifts C2 to a data-model-level guarantee. The salience increment inside the retrieval branch closes Observation 1 (the impossibility of satisfying C6 with a pure-function retrieval operator).

What MemState exposes as gaps for a **native GEM engine**: field histories are currently reconstructed from generic graph primitives rather than stored as first-class bitemporal attributes; propagation-bearing edges require schema-level semantics; retrieval-induced salience updates need a single read-modify-write primitive; relevance-driven forgetting should be scheduled like index maintenance.

## Research agenda

Three directions define memory-centric data management as a workload:

1. **Native engine** — storage layout co-locating topics/histories/embeddings; joint index over semantic similarity and history predicates; retrieval-as-write with consistent salience updates under concurrency. First target: I/O-aware page layout + joint index prototype.

2. **Trajectory-level correctness and evaluation** — current benchmarks (LongMemEval, LoCoMo, MemBench) measure answer-level recall and partially exercise C1 only; a trajectory benchmark needs ground truth for C2 (current values over time), C3 (dependent units per update), and C5 (active footprint per interaction count). First target: 500-turn adversarial workload scoring Mem0, Zep, and MemState.

3. **Privacy under multi-tenancy** — C6 makes retrieval a write; in shared-memory deployments, tenant A's query reinforces salience that tenant B later surfaces — a cross-tenant information leakage path. Verifiable erasure is also strictly harder than relational delete because a tenant's data shapes provenance chains and salience aggregates affecting other tenants.

**Success criteria**: at least one DBMS exposes governed-evolution operators as first-class primitives; standardized trajectory benchmarks measure C2–C6 violations; long-horizon deployments show measurable reductions in temporal-reasoning errors; privacy/forgetting guarantees become as well-understood as ACID.

## Implications

- The paper's impossibility results are structural claims (not formal theorems), but their consequence is clear: no amount of engineering on top of CRUD-based storage can satisfy all six correctness conditions. Systems that currently use vector databases, property graphs, or tiered memory as their substrate are all subject to at least one failure mode by construction.
- The GEM operator model maps naturally onto what practitioners already want: memory that learns what matters, forgets what doesn't, stays consistent when facts change, and tells you how it arrived at an answer.
- The privacy finding is novel: state-modifying retrieval (C6) is not just a correctness requirement but a security surface — salience scores become an inadvertent side channel across tenant boundaries in multi-tenant deployments.
- The analogy to stream processing is instructive: streams became a recognized workload when continuous state and event-time semantics moved from application code into the data model. GEM argues memory is at the same inflection point.

## Source
- arXiv 2605.26252 — "Is Agent Memory a Database? Rethinking Data Foundations for Long-Term AI Agent Memory" (Orogat & Mansour, Concordia University)
- Code: https://github.com/CoDS-GCS/MemState

## Related
- [[memory-architectures]] — GEM critiques all memory architecture families and provides a unifying four-capability lens
- [[memory-evolution-survey]] — covers the same agent memory system families (tiered, fact-extraction, graph-structured, consolidation, RL-driven)
- [[memgpt]] — cited as tiered/paging approach; GEM shows two-level eviction by age violates C5
- [[letta-memory-blocks]] — MemGPT lineage; same structural gaps apply
- [[graphiti]] — cited as the strongest existing dependency mechanism; GEM shows single-edge-at-a-time invalidation still fails multi-hop C3
- [[generative-agents]] — closest existing system to relevance-driven retention; GEM classifies its importance scoring as a retrieval-time heuristic, not a policy bounding active footprint
- [[proposals/memory-system-architecture]] — GEM's correctness conditions and operator model are directly applicable to system design proposals
