# Proposal: Role & Skill definition for a full agentic system

**Status: PROPOSAL — editorial synthesis.** Design proposal, not source-derived content. The *design* is the user's brief (2026-05-17); every recommendation is annotated with the wiki page whose evidence supports or complicates it. Part of a proposal set for a full agentic system; the memory/storage layer is [[proposals/memory-system-architecture]] — **this page owns what a role/skill *is* and how to author one well; that page owns where its artefacts are physically stored and retrieved.** Read together.

## One-line

A role/skill is defined by two separable memory classes — **role-defining** (stable identity: mandate, contracts, success criteria, improvement protocol, relationships) and **project-specific** (disposable: scope, handoff, logs, live working docs) — authored under [[agent-skills]]' progressive-disclosure + eval-first discipline, with a *uniform, Librarian-owned* improvement loop so every role learns the same way.

## Why two classes

Role-defining content is reusable across every project the role touches; project-specific content is provisioned at project start and archived at project end. Keeping them in separate stores is the operational form of [[agent-skills]]' **portability** principle (a skill works unmodified across contexts) and is what lets project state be rotated/expired without disturbing role identity. Conflating them is the most common cause of the context-bloat failure that [[conflicts/agents-md-effectiveness]] documents.

---

## ROLE-DEFINING

### 1. Role Contract — the role's `CLAUDE.md`

The only always-in-context artefact. Four required jobs:

- **(a) Mandate + clear goals** — what this role is and is for.
- **(b) Pointers to all reference material** — *not* the material itself.
- **(c) Explicit contracts** — in-bound and out-of-bound actions, stated as hard rules.
- **(d) Short.** It enters context on (almost) every call.

**Best practices (wiki-grounded):**

- **(b) is the load-bearing job, not (a).** [[agent-skills]]: the always-loaded surface must be a *table of contents that points outward* — "once loaded, every token competes with conversation history." [[conflicts/agents-md-effectiveness]] is the evidence that always-on context only helps in the *progressively-disclosed* regime; an inline knowledge dump is the failure mode, a pointer index is the fix.
- **Write the contract as boundaries, not knowledge.** [[agent-personas]]' task-type law: persona/role text *reliably helps* alignment/safety/boundary behaviour and *reliably hurts* knowledge recall. So (c) (contracts/boundaries) is exactly the content that belongs in an always-on role file; factual/domain knowledge does **not** — it goes behind a pointer (b).
- **"Short" is a discipline, not an instruction.** [[case-studies/anthropic-claude-code-postmortem]] Bug 3: a single brevity *instruction* dropped evals ~3%. Keep the *file* short by moving content out (progressive disclosure), not by adding "be brief" directives.
- **Name it for the activity.** [[agent-skills]]: gerund-form naming (`reviewing-prs`, `designing-schemas`), and the role's *description/manifest* is the single most important discovery lever — it is how the Librarian routes work to this role and how the role is found among many.
- **Match instruction specificity to task fragility.** [[agent-skills]]' freedom levels: high-freedom tasks → terse guidance; fragile/destructive tasks → exact, "do not modify" scripts. The contract states which mode each in-bound action is.

### 2. Role Reference & Best Practices

Bundled, **loaded on demand only**. [[agent-skills]] level-3 progressive disclosure: one level deep from the contract, table-of-contents header if >100 lines, split mutually-exclusive paths so irrelevant reference never loads. [[codified-context]]'s cold KB is the validated precedent (per-subsystem docs served on demand, not in the constitution).

### 3. Success Criteria

Point-form, role-specific, e.g.:
- writes code that passes PR review
- adheres to the project's overall architecture
- … (role-specific)

**Best practice:** author these **before** extensive role docs — [[agent-skills]]' eval-first loop makes evaluations the source of truth (a role's effectiveness is judged against this rubric, not asserted). This same rubric is the pass/fail signal the Improvement Loop consumes (next), and it is the kind of artefact [[sierra-monitor-eval-of-evals]] shows must itself be calibrated against labelled examples — Success Criteria are testable assertions, not aspirations.

### 4. Improvement Loop & Capabilities — *uniform across all roles*

Identify failures, correct the bad, reinforce the good — and your spec says **the same way for every role**. That single constraint has a strong consequence:

> A uniform cross-role improvement procedure is a **Librarian-owned protocol**, not per-role logic. The Worker *produces* the signal (the project Failure log); the Librarian *runs the protocol* and rewrites the role's Reference/Contract.

Wiki grounding:
- **Mechanism:** [[reflexion]] — failure → verbal reflection → episodic buffer → conditioned next trial — is the canonical reflective-memory loop.
- **Why a separate operator runs it:** [[memory-architectures]] flags self-reflection's *self-reinforcing-error* failure; [[skillos]] is the direct evidence that an executor-grounded, *separate* curator (even a small trained one) beats a model curating itself. The Worker must not grade itself.
- **The update action:** [[skillos]]' `insert_skill` / `update_skill` / `delete_skill` over a skill repo, generalised — the Librarian edits the Role Reference/Contract in response to the Failure log, evaluated against Success Criteria.
- **When to instead collapse the role:** [[skill-distillation]]'s Metric-Freedom predictor — sometimes the right "improvement" is to eliminate a role/handoff, not refine it.

#### The protocol — concrete step sequence *(editorial; this is the content of `memory/improvement/protocol.md` in the [[proposals/memory-system-architecture]] layout)*

Runs **off the task's critical path** (sleep-time-compute style, [[letta-memory-blocks]]), per role, Librarian-executed. One procedure, identical for every role.

- **Step 0 — Trigger.** Run when: (a) a Worker task fails its Success Criteria (binary/scalar signal), or (b) a heuristic fires — same action repeated > N cycles, or step/cost budget exceeded ([[reflexion]]'s concrete triggers: >3 repeats / >30 actions), or (c) a scheduled batch sweep of Failure-log entries accumulated since the last run. Fires on failures *and* on validated wins (the "reinforce the good" half) — never on raw success without a score.
- **Step 1 — Collect signal (verbatim, read-only).** Librarian reads, for this role: the project **Failure log** + **Actions log** (Worker-written during execution, [[anthropic-memory-tool]] "record as you go") and the relevant **Success Criteria**. No Worker self-summary enters the loop — verbatim in ([[mempalace]] discipline; the [[memory-architectures]] *trustworthy-reflection* caveat is that self-summarised reflection entrenches error).
- **Step 2 — Diagnose (separate operator).** The Librarian — not the Worker — produces the verbal reflection: failure description, minimal causal hypothesis, and which artefact is implicated (Contract / Reference / a specific procedure). This is [[reflexion]]'s self-reflection step executed by the curator, per the [[skillos]] separation result.
- **Step 3 — Propose one edit.** Emit a single [[skillos]]-style op against the role-defining store: `update` (refine an instruction — e.g. `"always filter"` → `"MUST filter"`, the concrete [[agent-skills]] example), `insert` (add a missing best-practice/reference), or `delete` (remove a stale/harmful instruction). Target **Reference first**; touch the **Contract only** for a contract/boundary failure (keeps the always-on surface stable — [[conflicts/agents-md-effectiveness]] fragility).
- **Step 4 — Validate before commit (the gate).** (i) *Regression:* re-run the failing case **plus a sample of previously-passing cases** against the edited role, scored by Success Criteria — [[agent-skills]]' fresh-instance ("Claude-B") test on real workflows, not the triggering scenario. (ii) *Grouped evaluation:* score the edit by its effect on **later related tasks**, not just the trigger — [[skillos]]' grouped-task-stream signal (its single largest ablation; blocks locally-good / globally-bad edits). (iii) *Content-quality:* abstraction / reusability / actionability ([[skillos]] content reward) — reject edits that merely memorise the one failure.
- **Step 5 — Commit or roll back.** Commit only if the grouped Success-Criteria score improves without regressing the passing sample. The role-defining store is versioned/verbatim ([[memgpt]] archival + [[mempalace]]), so a commit is revertible. Otherwise discard and leave the Failure-log entry **open for more signal** — no forced edit on weak signal ([[memory-architectures]] uncertainty).
- **Step 6 — Expire / forget (bounded growth + safety floor).** Demote Reference entries unused for K cycles to cold ([[memory-architectures]] principled consolidation; [[reflexion]]'s bounded Ω buffer is the precedent). **Hard invariant:** a protected safety/compliance contract set is *never* auto-`delete`d by Steps 3/6 — [[memory-architectures]]' "guarantee safety-critical records survive / learning-to-forget-under-constraints" challenge. Removing a protected rule escalates **out of the loop** (open decision #1 below).
- **Step 7 — Reinforce (positive half).** A validated Worker win (passed + improved the grouped score) is promoted by the same `insert`/`update` into Reference as a named best-practice. Expected maturation curve, per [[skillos]]' observed progression: early iterations add *facts*; later iterations add *decision logic* (conditional branches, failure-handling).

**Invariants (every role, every iteration):** Worker never grades or edits itself · verbatim in, validated out · grouped evaluation not single-case · protected safety set is escalation-only · growth is bounded by expiration. Step 4(ii) is the *mechanical* validator that answers open decision #1 partially; the human / separate-harness gate is reserved for Step 6 protected-set changes.

### 5. Role Context Management

How this role retrieves/stores/folds its own memory. **Defined in [[proposals/memory-system-architecture]]** (the retrieval ladder + tiering), instantiated per role; referenced from the Contract, or inlined only if tiny ([[agent-skills]]: split when unwieldy).

### 6. Role Relationships

Explicit hierarchy and handoffs, e.g. *prototyper needs project-owner sign-off; dev needs reviewer PR approval; dev verifies schema compliance with architect.*

- **Structure:** [[patterns/topology-taxonomy]] manager-agent / handoff topology; cross-role shared state is [[letta-memory-blocks]] **shared memory blocks** (Librarian-provisioned); the handoff *artefacts* are [[effective-harnesses]]-style (`feature_list.json`, progress file).
- **Caveat — must rule on:** [[skill-distillation]] — an explicit handoff is a *cost*; collapse it when task Freedom is high. Treat the relationship graph as Librarian-owned **configuration** with "collapse the handoff" as the default whenever a relationship isn't demonstrably earning its keep.

---

## PROJECT-SPECIFIC

Disposable per project; Librarian provisions at start, archives at end.

| Element | Purpose | Wiki grounding |
|---|---|---|
| **Scope** | tasks & goals for the project | [[anthropic-memory-tool]] initializer-session pattern (checklist + goals authored before work); [[effective-harnesses]] `feature_list.json` |
| **Handoff.md** | what the next session/role needs | [[effective-harnesses]] `claude-progress.txt`; [[anthropic-memory-tool]] end-of-session update |
| **Actions log** | running actions + results, append-only verbatim | [[effective-harnesses]] progress file; [[reflexion]] short-term trajectory buffer |
| **Project reference** | "what good looks like" here | [[codified-context]] cold KB; *"memory is just pages and databases"* ([[case-studies/notion-token-town]]) — wiki-as-memory per project |
| **Project plan** | technical plan docs | [[effective-harnesses]] `init.sh` + plan; cold-tier, paged on demand |
| **Failure log** | every bad action + why; the improvement signal | [[reflexion]] long-term reflection buffer *exactly*; the input [[skillos]]' curator consumes; Librarian-validated per [[memory-architectures]] trustworthy-reflection |
| **Current task working docs** | live md notebook — don't lose info + shrink per-call context; role-managed | [[anthropic-memory-tool]] "ASSUME INTERRUPTION, record as you go" + [[context-folding]] (adaptive folding, ~7k tokens after 100 turns) + [[claude-code-session-memory]] background extraction; goal "reduce per-call context" *is* the folding objective |
| **Historical working docs** | archived, untouched unless asked | cold tier; [[memgpt]] archival storage; [[mempalace]] verbatim discipline |

---

## Cross-cutting best practices *(editorial — the do/don't distilled from the cluster)*

- **Always-on surface = boundaries + pointers only.** Knowledge goes behind progressive disclosure. (sources: [[agent-skills]], [[agent-personas]], [[conflicts/agents-md-effectiveness]])
- **Eval-first.** Success Criteria before docs; the rubric is the source of truth and is itself calibrated. ([[agent-skills]], [[sierra-monitor-eval-of-evals]])
- **The role never grades itself.** Improvement is a separate-operator, uniform, Librarian-owned protocol. ([[skillos]], [[memory-architectures]], [[reflexion]])
- **Handoffs are a cost.** Default to collapsing role relationships unless they demonstrably earn their keep. ([[skill-distillation]], [[patterns/topology-taxonomy]])
- **Project state is disposable; role identity is not.** Separate stores; archive projects verbatim. ([[agent-skills]] portability, [[mempalace]], [[memgpt]])
- **Working docs are a notebook, folded continuously.** Not a transcript. ([[context-folding]], [[anthropic-memory-tool]])

## Open decisions (for you)

1. **Improvement-loop validator:** Librarian-validates-against-Success-Criteria is the working position — but what validates the Librarian? (separate eval harness à la [[sierra-monitor-eval-of-evals]], or a human gate?)
2. **Relationship graph default:** confirm "collapse handoff unless it earns its keep" as the default, or specify a fixed hierarchy.
3. **Contract size threshold:** at what size does Role Context Management move from inline-in-Contract to a referenced file? ([[agent-skills]] says "when unwieldy" — pick a concrete budget.)
4. **Role vs personality:** are "skill" and "personality" the same unit here, or does personality (identity/tone) get its own sub-store given [[agent-personas]]' task-type caveat?

## Source

- Editorial synthesis of the user's role/skill design brief (2026-05-17 conversation). No external sources captured — a `/query`-class synthesis over the existing skills + harness + memory clusters.
- Grounding pages: [[agent-skills]], [[agent-personas]], [[skillos]], [[skill-distillation]], [[reflexion]], [[memory-architectures]], [[effective-harnesses]], [[anthropic-memory-tool]], [[context-folding]], [[claude-code-session-memory]], [[codified-context]], [[letta-memory-blocks]], [[memgpt]], [[mempalace]], [[patterns/topology-taxonomy]], [[sierra-monitor-eval-of-evals]], [[conflicts/agents-md-effectiveness]], [[case-studies/notion-token-town]].

## Related

- [[proposals/memory-system-architecture]] — companion proposal; owns the two-operator model, tiering, retrieval ladder, and on-disk layout these roles plug into.
- [[patterns/agent-skills]] — the authoring discipline (progressive disclosure, description-as-discovery, eval-first) this proposal applies to roles.
- [[patterns/agent-personas]] — the task-type law that says contracts/boundaries belong always-on but knowledge does not.
- [[patterns/skillos]] — separate trained curator > self-curation; the evidence behind the Librarian-owned improvement loop.
- [[patterns/skill-distillation]] — when to collapse a role/handoff rather than improve it.
- [[patterns/effective-harnesses]] — the project-specific artefact set (scope/handoff/progress) precedent.
- [[patterns/topology-taxonomy]] — role-relationship / handoff topology.
