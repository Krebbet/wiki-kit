# Proposal: A two-operator, text-search-first agent memory system

**Status: PROPOSAL — editorial synthesis.** This page is a design proposal, not source-derived content. The *design* is the user's brief; every architectural choice below is annotated with the wiki page whose evidence supports (or complicates) it via `[[wiki-link]]`. Where the wiki's evidence is contested, that is called out rather than smoothed over. Stated assumptions are listed under [Assumptions](#assumptions-state-before-building); revisit them before implementation.

## One-line

A memory architecture with two distinct operators — a **Librarian** that owns where information lives and a **Worker/Extractor** that produces and consumes it — built on a *verbatim-first store* with a *traditional-text-search-first retrieval ladder* (grep/regex → structured index → vector/graph → LLM), so that most reads cost no LLM calls and role-specific knowledge is discoverable by the role that needs it.

## The two operators

This separation is the proposal's spine and it has direct wiki grounding — the split already exists in the literature under different names:

| Operator | Role in this proposal | Wiki precedent |
|---|---|---|
| **Librarian** | Owns the *architecture of the information system*: what tier a fact belongs in, when to consolidate/deduplicate/expire, how the index is shaped, which role-scoped store a record routes to. Does not do task work. | [[memgpt]]'s queue-manager + memory-operation function interface (the component that decides what pages in/out); [[letta-memory-blocks]]'s **sleep-time compute** (a background agent that curates the memory of primary agents — this *is* the Librarian); [[skillos]]'s **frozen executor + RL-trained curator** split (the cleanest evidence that a dedicated curator, even a small one, beats a frontier model doing its own curation); [[memory-architectures]]'s "manage" step (summarize, deduplicate, score priority, resolve contradictions, delete). |
| **Worker / Extractor** | Does the task and records what it learned, verbatim, into the place the Librarian designated. Reads via the retrieval ladder. One per skill/personality. | [[reflexion]] (worker writes verbal post-mortems to an episodic buffer); [[anthropic-memory-tool]]'s "record status/progress/thoughts as you go" discipline; [[mem0]]'s extraction phase (the per-interaction fact producer). |

**Why two operators and not one.** [[skillos]] is the load-bearing evidence: an 8B RL-trained curator beat Gemini-2.5-Pro-as-its-own-curator — *executor-grounded curation outperforms self-curation*. [[memory-architectures]] names the failure mode of a single conflated operator as **silent orchestration failure / "memory blindness"**. The separation also matches [[letta-memory-blocks]]'s sleep-time pattern, where curation happens *off the task's critical path* (no user-facing latency, no token cost charged to the Worker's context).

## The architecture the Librarian governs

A tiered store, Librarian-owned, following the hierarchical-virtual-context family ([[memory-architectures]] family 4; foundational [[memgpt]]; hand-engineered instance [[codified-context]]):

- **Hot tier** — small, always-in-context working set (the Librarian's current "shelf"). Bounded like [[letta-memory-blocks]]' `limit` field; analogous to MemGPT main context.
- **Warm tier** — on-disk verbatim records, reachable by *algorithmic* retrieval with zero LLM calls (the bulk of the system; see retrieval ladder).
- **Cold tier** — archival verbatim, rarely touched, partitioned so it never enters context unless explicitly paged ([[codified-context]]'s 34-doc cold KB served on demand).
- **Role-scoped stores** — per skill/personality (next section).

The Librarian decides tier placement and migration. This is exactly [[memgpt]]'s paging logic and [[codified-context]]'s drift-detector + trigger-table, generalised: a record's tier is a Librarian decision, not a Worker decision.

## The five tenets — grounding and caveats

### 1. Store verbatim as much as possible

**Wiki support:** [[mempalace]] is the doctrinal verbatim camp ("never summarize, paraphrase, or lossy-compress user data — 100% recall is the design requirement"); it reaches 96.6% R@5 on [[longmemeval]] in raw mode with *no LLM and no API key*, which is precisely the "save LLM calls" goal.

**Caveat you must design around — this is an OPEN conflict.** [[conflicts/verbatim-vs-extracted-memory]] is unresolved. The scale-ceiling argument: ~a year of daily agent conversation ≈ 10M tokens, beyond which retrieve-everything-then-sort is infeasible and selective extraction ([[mem0]]) becomes mandatory. The wiki's recommended reconciliation is **not** pure verbatim — it is [[longmemeval]]'s hybrid (§5.3): keep **verbatim values** but **expand the keys with extracted facts** (+9.4pp recall@k, +5.4pp downstream QA). [[mempalace]]'s own closets-as-keys → drawers-as-values structure is a gesture at exactly this. **Recommendation:** verbatim *values*, Librarian-maintained *extracted-fact keys* — this satisfies your "verbatim as much as possible" tenet without inheriting the scale ceiling.

### 2. Algorithmic retrieval to save context, LLM calls, token cost

**Wiki support — strong and recent.** [[direct-corpus-interaction]] (arXiv 2605.05242) is the headline evidence: replacing a vector retriever with **direct `grep`/`rg` over the raw corpus** lifted BrowseComp-Plus 69.0→80.0 (+11pp) **while cutting cost 29.4%** at matched model. The mechanism is *interface resolution*, not recall — terminal search localises within documents better than top-k vector retrieval. This is the single strongest wiki data point for "lean on traditional text search first to save cost." [[mem0]] is the complementary evidence on the extraction side: selective retrieval gave 92% p95 latency reduction vs full-context.

### 3. Traditional text search first, then vector/graph, then LLM

**This becomes the retrieval ladder (editorial — the synthesis of tenets 2+3):**

1. **Exact/structured text search first** — `grep`/`rg`/`find`/regex over verbatim records and over the Librarian's extracted-fact key index. Zero LLM calls. Grounded in [[direct-corpus-interaction]]; the within-document localisation advantage (48.4 vs 21.7) is why this tier is first, not just cheapest.
2. **Structured index lookup** — the fact-augmented key layer ([[longmemeval]] §5.3; [[mempalace]] closets). Still algorithmic, still zero-LLM.
3. **Vector / graph** — semantic similarity ([[mempalace]] ChromaDB cosine) or entity-graph traversal ([[mem0]]'s Mem0g, best on temporal/relational queries) **only when 1–2 miss**. The survey notes the bottleneck here has shifted from storage to *retrieval quality* ([[memory-architectures]] family 2) — so this tier is a fallback, not the default.
4. **LLM-mediated** — query expansion, re-ranking, or reflective synthesis ([[longmemeval]] time-aware query expansion; [[reflexion]]) only as the last resort, because it is the only tier that spends tokens.

**Hard boundary (design constraint, from the wiki):** [[direct-corpus-interaction]] degrades sharply above ~200K docs and collapses at ~400K. The text-search-first ladder is **workspace/project scale**. Beyond that the Librarian must partition the corpus into workspace-sized shards (per role, per project, per time-window) before tier 1 applies — partitioning is a core Librarian responsibility, not an afterthought.

### 4. Information recorded where it is needed

The Librarian routes each record to the tier *and* the role-scoped store where it will be read. Precedent: [[codified-context]]'s trigger table routes tasks to specialist agents by which files change; [[memgpt]] writes evicted content to the store it will be searched from.

### 5. Role-specific information stored, easily found, and discovered by that role

**Wiki support:** this is exactly [[agent-skills]]' **progressive disclosure** + **description-as-discovery**: a skill bundles its own reference files, and the *description* is the load-bearing index that lets the right role find the right material among 100+ without loading everything. [[letta-memory-blocks]] gives the multi-agent primitive: labelled memory blocks, optionally shared, each role editing its own. [[agent-personas]] supplies the caveat: persona/role text in the system prompt is *task-type dependent* (helps alignment/style, hurts knowledge recall, ≈0 naive net) — so a role's *identity* belongs in its scoped store and its routing key, **not** bloated into a always-on system-prompt persona.

**Mechanism (editorial):** each role/skill/personality gets (a) a verbatim store, (b) a Librarian-maintained extracted-fact key index scoped to that role, (c) a description/manifest the Librarian uses to route writes in and the role uses to discover reads — the [[agent-skills]] pattern applied to memory, not just to procedures.

## Skill / Role definition — the two memory classes

A role's memory splits into **role-defining** (stable identity: who am I, how do I act, what are my contracts) and **project-specific** (volatile: this project's tasks, progress, feedback). The first is the Worker's reusable identity; the second is disposable per project. Keeping them in *separate stores* is the operational expression of [[agent-skills]]' portability principle (a skill works unmodified across contexts) and is what lets the Librarian rotate/expire project state without touching role identity.

### Role-defining store

| Element | What it is | Wiki grounding & discipline |
|---|---|---|
| **Role Contract** (the role's `CLAUDE.md`): mandate + goals, pointer to all reference material, explicit in/out-of-bound actions, **short, in context every call** | The only always-on part | This is [[agent-skills]]' `SKILL.md` body under its strictest reading: the always-loaded surface must be minimal because *"once loaded every token competes with conversation history"*. Point (b) — *tell the role where to find materials* — is **load-bearing, not optional**: it is exactly the [[agent-skills]] progressive-disclosure contract, and the [[conflicts/agents-md-effectiveness]] evidence is that always-on context only helps in the *progressively-disclosed* regime. The contract should be a table-of-contents that points outward, not a knowledge dump. In/out-of-bound contracts are the one place [[agent-personas]] says role text *reliably* helps (alignment/safety/boundary behaviour is the persona-positive task type) — so encode boundaries here, not knowledge. |
| **Role Reference & Best Practices** | Bundled, loaded on demand | [[agent-skills]] level-3 references (one level deep from the contract, ToC header if >100 lines); [[codified-context]]'s cold KB served on demand. Never always-on. |
| **Success Criteria** (point-form, role-specific) | The local rubric | [[agent-skills]]' eval-first loop: evaluations are the source of truth, authored *before* extensive docs (JSON-style rubric: query / expected_behavior). This rubric is also the Improvement Loop's pass/fail signal (next row) and a calibration target like [[sierra-monitor-eval-of-evals]]. |
| **Improvement Loop & Capabilities** (identify failures, reinforce good, correct bad — *uniform across all roles*) | The reflective-memory engine | **This is where your spec tightens the two-operator spine.** "Same for all roles" ⇒ it is a *Librarian-owned, uniform protocol*, not per-role code. Mechanism = [[reflexion]] (failure → verbal reflection → buffer → next trial) but **validated by a separate operator**: [[memory-architectures]] flags self-reflection's *self-reinforcing-error* failure mode, and [[skillos]] is the direct evidence that an executor-grounded *separate* curator beats self-curation. So: Worker writes the failure log; the Librarian runs the (uniform) improvement protocol against Success Criteria and rewrites the Role Reference/Contract — [[skillos]]' `insert/update/delete` over a skill repo, generalised. The Worker never grades itself. |
| **Role Context Management** (how this role retrieves/stores/folds its own memory) | The retrieval ladder, scoped to this role | The [§ retrieval ladder](#3-traditional-text-search-first-then-vectorgraph-then-llm) instantiated per role. Inline in the Contract only if tiny; otherwise a referenced file ([[agent-skills]]: split when unwieldy). |
| **Role Relationships** (explicit hierarchy: prototyper→owner sign-off, dev→reviewer PR approval, dev→architect schema check) | The handoff graph | [[patterns/topology-taxonomy]] manager-agent / handoff topology; the handoff *artefacts* are [[effective-harnesses]]-style (`feature_list.json`, progress file) and the cross-role shared state is [[letta-memory-blocks]] **shared memory blocks**. **Caveat (must rule on):** [[skill-distillation]]'s Metric-Freedom predictor says explicit handoffs are a *cost* worth eliminating when task Freedom is high — so the relationship graph should be Librarian-owned *configuration*, with collapse-the-handoff as the default when a relationship isn't earning its keep. |

### Project-specific store

All of this is disposable per project; the Librarian provisions it at project start and archives it at project end.

| Element | Wiki grounding |
|---|---|
| **Scope** (tasks & goals) | [[anthropic-memory-tool]]'s initializer-session pattern (feature checklist + goals authored before work); [[effective-harnesses]] `feature_list.json`. |
| **Handoff.md** | [[effective-harnesses]] `claude-progress.txt`; [[anthropic-memory-tool]] end-of-session update; the explicit-handoff-artefact class in [[topology-taxonomy]]. |
| **Actions log** (running actions + results) | [[effective-harnesses]] progress file; [[reflexion]]'s short-term trajectory buffer; [[claude-code-session-memory]] work-log. Verbatim, append-only. |
| **Project reference materials** ("what good looks like") | [[codified-context]] cold KB; the *"memory is just pages and databases"* pattern from [[case-studies/notion-token-town]] — this is the wiki-as-memory move, applied per project. |
| **Project plan materials** (technical plan docs) | [[effective-harnesses]] `init.sh` + plan; cold-tier, paged on demand. |
| **Failure log** (every bad action + why; feeds skill improvement later) | [[reflexion]]'s long-term reflection buffer *exactly*; it is the **training signal** for the Improvement Loop above and the input [[skillos]]' curator consumes. Caveat: subject to [[memory-architectures]]' *trustworthy-reflection* open challenge — hence Librarian-validated, not Worker-trusted. |
| **Current task working docs** (live md notebook: don't lose info + shrink per-call context, role-managed) | The clearest grounding in the cluster: [[anthropic-memory-tool]]'s *"ASSUME INTERRUPTION — record progress as you go"* + [[context-folding]] (AgentFold: proactive variable-granularity folding, ~7k tokens after 100 turns) + [[claude-code-session-memory]] background extraction. Goal (2) "reduce what's required in context per call" *is* the compaction/folding objective. Role-managed = your call; the wiki supports leaving granularity to the agent ([[context-folding]] is adaptive). |
| **Historical working docs** (archived, untouched unless needed) | Cold tier; [[memgpt]] archival storage; verbatim discipline from [[mempalace]]. |

### Concrete on-disk layout *(editorial — one viable instantiation)*

```
memory/
  roles/<role>/                 # role-defining (stable, reusable across projects)
    CONTRACT.md                 # [HOT] always-in-context: mandate, goals, pointers, in/out contracts — short
    reference/                  # [COLD] best-practices, loaded on demand (one level deep, ToC headers)
    success-criteria.md         # [WARM] rubric: also the Improvement Loop pass/fail signal
    context-policy.md           # [WARM] this role's retrieval-ladder rules (or inlined in CONTRACT if tiny)
    relationships.md            # [WARM] Librarian-owned: handoff graph + which shared blocks it joins
  shared-blocks/<block>/        # [WARM] Letta-style cross-role shared memory (Librarian-provisioned)
  improvement/                  # [WARM] Librarian-owned, UNIFORM across roles
    protocol.md                 #   the one improvement procedure all roles run through
  projects/<project>/<role>/    # project-specific (disposable; provisioned + archived by Librarian)
    SCOPE.md  HANDOFF.md  actions.log  failures.log     # [WARM] append-only, verbatim
    plan/  reference/                                   # [COLD] paged on demand
    work/                       # [HOT→WARM] live task notebook, role-managed, folded per context-folding
  archive/projects/<project>/   # [COLD] historical working docs — never touched unless asked
```

`[HOT]` = enters context every/most calls (keep minimal — the [[conflicts/agents-md-effectiveness]] fragile surface). `[WARM]` = algorithmic retrieval, zero LLM (the retrieval ladder's tiers 1–2). `[COLD]` = archival, paged only on explicit Librarian/role request.

## Risks & open decisions *(editorial — surfaced honestly from the wiki)*

- **The verbatim-vs-extracted conflict is OPEN.** [[conflicts/verbatim-vs-extracted-memory]] has no empirical bridge at matched scale/metric. The proposal takes the [[longmemeval]] hybrid as its working position; if you want pure verbatim, accept the documented scale ceiling and design shard-rotation early.
- **The Librarian is an LLM-mediated component and can fail silently.** [[memory-architectures]] open challenges: principled consolidation (hoard-vs-amnesia), *learning to forget under safety constraints* (a curator can learn to drop safety-critical records), trustworthy reflection (self-reinforcing error). Mitigation evidence: [[skillos]] shows a *trained, executor-grounded* curator beats an ad-hoc one — budget for evaluating the Librarian, not just the Workers.
- **Text-search-first is scale-bounded** (tenet 3 boundary above). Decide the sharding axis (role / project / time) up front.
- **Role memory can become context bloat.** [[conflicts/agents-md-effectiveness]] (OPEN) — context files help only in the favorable regime (agent-authored, progressively disclosed, eval-tested). Role stores must be lazily loaded, never always-on.
- **The improvement loop can entrench errors.** [[memory-architectures]]' *trustworthy-reflection* open challenge: a self-graded failure log amplifies mistakes. The proposal mitigates by making the loop Librarian-owned and validated against Success Criteria ([[skillos]] evidence: separate executor-grounded curation > self-curation) — but *who/what validates the Librarian itself* is an open decision.
- **The role-relationship graph is a cost, not free structure.** [[skill-distillation]]'s Metric-Freedom predictor: explicit handoffs should be collapsed when task Freedom is high. Decide per-relationship whether the handoff earns its keep; default to collapse.
- The full role/skill *definition* spec (contracts, success criteria, improvement protocol, relationships) lives in [[proposals/agentic-system-roles-skills]]; this page owns only where those artefacts are *stored and retrieved*.

## Assumptions (state before building)

1. **Scale:** workspace/project-scale corpora per shard (≤~100–200K docs) — sets the text-search-first ladder as viable. If multi-year/enterprise, the extraction tier ([[mem0]]) moves earlier.
2. **Topology:** multi-worker (one Worker per skill/personality) + one Librarian, matching [[letta-memory-blocks]] shared-block multi-agent. Single-agent collapses the two operators back into one (see [[skill-distillation]] — sometimes the right call when task Freedom is high).
3. **Substrate:** filesystem + terminal tools available to the Librarian and Workers (required for tier-1 `grep`/`rg`; [[direct-corpus-interaction]] assumes this).

## Source

- Editorial synthesis of the user's design brief (2026-05-17 conversation). No new external sources captured; this is a `/query`-class synthesis over the existing memory cluster, not a `/research` ingest.
- Grounding pages (all claims traceable to these): [[memory-architectures]], [[memgpt]], [[letta-memory-blocks]], [[mem0]], [[mempalace]], [[longmemeval]], [[direct-corpus-interaction]], [[reflexion]], [[anthropic-memory-tool]], [[codified-context]], [[skillos]], [[agent-skills]], [[agent-personas]], [[conflicts/verbatim-vs-extracted-memory]], [[conflicts/agents-md-effectiveness]].

## Related

- [[memory/memory-architectures]] — the five-family taxonomy this proposal composes (hierarchical-virtual-context for tiering + retrieval-augmented for the store + policy-learned for the Librarian).
- [[conflicts/verbatim-vs-extracted-memory]] — the OPEN conflict the verbatim tenet sits inside; the hybrid working position is taken from here.
- [[memory/direct-corpus-interaction]] — empirical backbone for text-search-first (+11pp, −29% cost) and its scale ceiling.
- [[memory/longmemeval]] — the verbatim-values + extracted-fact-keys hybrid; indexing/retrieval/reading control points.
- [[patterns/skillos]] — the frozen-executor + trained-curator split that justifies two operators.
- [[memory/letta-memory-blocks]] — sleep-time compute = the off-critical-path Librarian; shared blocks = role-scoped stores.
- [[patterns/agent-skills]] / [[patterns/agent-personas]] — role/personality-scoped discovery mechanism and the persona caveat.
- [[patterns/codified-context]] — hand-engineered tiered + role-routing precedent.
