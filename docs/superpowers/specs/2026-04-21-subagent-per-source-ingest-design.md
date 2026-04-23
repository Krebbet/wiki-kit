# Subagent-per-Source `/ingest` with Coherence Orchestration

**Date:** 2026-04-21
**Status:** Design approved; awaiting implementation plan
**Scope:** `wiki-kit` (generic — harvestable to `main`)

## Problem

Today's `/ingest <path>` reads every raw source into the main agent's context, discusses takeaways, then writes wiki pages. Two concrete failures with this approach:

1. **Token waste.** An N-source ingest loads all N raw bodies into the main session, even though only distilled takeaways are needed for the write decisions.
2. **Usage-policy false positives.** On 2026-04-21 a `/ingest` over 11 alignment/post-training papers (`raw/research/post-training-alignment-2026/`) tripped the Claude Code usage-policy classifier. Cause: cumulative context packed with safety-spec excerpts, jailbreak taxonomies, disallowed-content categories, and CoT traces reasoning about harmful requests — precisely the content a classifier is tuned for, even though each source individually is a legitimate research paper. Subsequent turns and `/compact` re-sent the flagged context and also 403'd. Only a new session recovered.

Both point to the same fix: **keep raw source bodies out of the main session.** Process each source in its own subagent with fresh context; have the main agent orchestrate.

## Goals

- Main context never sees raw source bodies.
- Each subagent sees only one source + `wiki/index.md`.
- Wiki coherence (page boundaries, cross-refs, conflicts) is decided centrally, by the orchestrator, after all summaries are in.
- One human gate per ingest, not N.
- Resumable across session crashes.
- Generic enough to harvest to `main`.

## Non-goals

- Adaptive concurrency limits. Dispatch all subagents in one batch.
- Cross-topic summary dedup.
- Post-write verification that wiki pages match summary intent (belongs in `/lint`).
- Tree-based aggregation for ingests >20 sources (revisit if that load shape becomes common).

## Architecture

`/ingest <path>` becomes an orchestrator + fan-out + aggregate + write pipeline.

```
/ingest <path>
  │
  ├─ 1. Resolve inputs ─ file → [file]; dir → [*.md]; read wiki/index.md once
  │
  ├─ 2. Dispatch fan-out ─ one subagent per source, in parallel
  │     input:  source path + contents + wiki/index.md
  │     output: .ingest/<slug>.summary.md
  │
  ├─ 3. Wait for all ─ orchestrator blocks until every subagent returns or errors
  │
  ├─ 4. Aggregate ─ read all .ingest/*.summary.md, build unified picture
  │
  ├─ 5. Human gate ─ present review packet; wait for direction + rulings
  │
  ├─ 6. Write ─ create/update wiki pages per approved plan
  │
  └─ 7. Track ─ update index.md / revisions.md / log.md; report pages touched
```

**Invariants:**
- Main context never sees raw source bodies — only summaries (short, structured) and existing wiki pages the plan touches.
- Subagent context sees only its source + `index.md`.
- All writes to `wiki/` happen in step 6, by the orchestrator, after human approval.
- Subagents are read-only over `wiki/` and write-only into `.ingest/`.
- Re-running `/ingest` on the same dir reuses existing summaries; only missing or failed slugs re-dispatch.

## Subagent contract

**Agent type:** `general-purpose` (needs Read/Write/Bash to read source and write one summary file).

**Inputs (passed in the dispatching prompt):**
- Absolute path of the one source file it owns
- Absolute path of `wiki/index.md` (for cross-ref candidate naming)
- Absolute path of the `.ingest/` dir where it writes its output
- The DOMAIN-SLOT schema the orchestrator pulled from `.claude/commands/ingest.md`

**Hard rules in the prompt:**
- Read only those two paths (source + index). Do not glob the wiki, do not read other raw sources, do not read sibling summaries.
- Write exactly one file: `.ingest/<slug>.summary.md`. Do not write anywhere else.

**Output file format** — `.ingest/<slug>.summary.md`:

```markdown
---
source: raw/<topic>/<slug>.md
slug: <slug>
summarized_on: YYYY-MM-DD
schema_version: 1
---

# <source title>

## One-line
<single sentence: what is this source, what does it claim>

<!-- DOMAIN-SLOT schema sections, rendered from ingest.md's takeaway-prompts slot -->
## Method
...
## Results
...
(etc. — exact sections determined by the domain slot)

## Cross-ref candidates
- [[existing-page-name]] — <why this source touches it: extends / contradicts / parallels>
- ...

## Conflict flags
- Claim: <precise statement from this source>
  Contradicts: [[existing-page]] which says <precise existing statement>
  Basis: <quote or tight paraphrase, with which section of the source>

## Proposed page shape
- New page: <title> — <one-line justification>
- OR: extend [[existing-page]] with section "<section name>"
- OR: split into N pages: ...
```

**Return value** to the orchestrator (what Agent tool reports back): a short confirmation line plus any warnings (e.g., "source appears truncated at line X; flagging"). Orchestrator reads summaries from disk, not from return values.

**Schema ownership:**
- Fixed sections (frontmatter, One-line, Cross-ref candidates, Conflict flags, Proposed page shape) are generic kit.
- DOMAIN-SLOT governs only the takeaway-prompts list (Method / Results / Applicability / Novelty / Repro / Adoption / Conflicts for this wiki).

## Orchestrator aggregation + human gate

After all subagents return, the orchestrator reads every `.ingest/*.summary.md` and builds a unified review packet. One pause, user responds once.

**Review packet format:**

```markdown
# Ingest Review — <topic>

## Sources processed
| Slug | Title | Status | Summary path |
|---|---|---|---|
| 01-foo | ... | ok | .ingest/01-foo.summary.md |
| 02-bar | ... | FAILED (retry?) | — |

## Page plan (proposed)
- NEW: wiki/<topic>/<page-title>.md — sources: [01-foo, 03-baz]
- EXTEND: wiki/existing-page.md with new section "<name>" — sources: [02-bar]
- MERGE CANDIDATE: [04-x, 05-y] both propose new pages but overlap ≥70% on method — suggest single page, user confirms

## Cross-references to add
- [[new-page-a]] ↔ [[existing-page-b]] — justification
- ...

## Conflict flags (require ruling)
- <source> claims X; [[existing-page]] says Y. Evidence: ...
  → options: (a) resolve in favour of new source, (b) keep existing, (c) open wiki/conflicts/<slug>.md

## Novelty / adoption highlights
- <slug>: high-novelty — <one line why>
- <slug>: widely-cited per source — <one line>

## Low-value candidates (suggest skip)
- <slug>: redundant with [[existing-page]]; no new method/result. Suggest skip write.

## Awaiting your direction
- Accept page plan as-is?
- Any emphasis / de-emphasis per source?
- Conflict rulings?
- Retry failed summaries?
```

**Aggregation rules:**
- **Page plan** — greedy grouping from each summary's "proposed page shape"; when ≥2 NEW proposals share ≥2 named concepts, flag as merge candidate (don't merge unilaterally).
- **Cross-references** — union of all "cross-ref candidates", deduplicated; duplicates named by ≥2 summaries promoted to "strong".
- **Conflicts** — surfaced verbatim; user rules.
- **Novelty highlights** — pulled from per-summary novelty sections where the subagent marked something explicitly new or widely-adopted.
- **Low-value candidates** — flagged when cross-ref candidates are fully "extends [[X]]" with no new method/results.

**Context budget during aggregation:** orchestrator reads summaries (small, structured) plus the specific existing pages their cross-ref candidates name. Never the whole wiki.

## Persistence + resume

**Directory layout:**

```
raw/<topic>/
  01-foo.md                     ← source (immutable)
  02-bar.md
  assets/
  .ingest/                      ← the one exception to raw/ immutability
    01-foo.summary.md
    02-bar.summary.md
    run.json
```

`.ingest/` is committed to git. Summaries are small, structured, reviewable. No `.gitignore` changes.

**`run.json`:**

```json
{
  "schema_version": 1,
  "started_at": "2026-04-21T14:30:00Z",
  "last_updated": "2026-04-21T14:52:00Z",
  "sources": {
    "01-foo": {"status": "ok",      "summary": "01-foo.summary.md"},
    "02-bar": {"status": "failed",  "error": "subagent timeout"},
    "03-baz": {"status": "ok",      "summary": "03-baz.summary.md"}
  },
  "review_completed_at": null,
  "pages_written": []
}
```

**Resume semantics:**
- On re-invocation, orchestrator reads `run.json` and skips slugs with `status: ok` and an on-disk summary file. Re-dispatches `failed` and any source missing an entry.
- Crash between dispatch and review → re-read summaries, go straight to review.
- Crash between review and writes → page plan is NOT persisted; re-run aggregation, re-present to user. Deliberate: plan decisions are user-owned, not re-used silently.
- Crash during writes → `pages_written` appended as-we-go. Resume skips already-written pages.

**Invalidation:**
- Source `mtime` newer than its summary → re-dispatch (source was re-captured).
- `--force` ignores cache entirely.
- Schema bump (`schema_version` in `ingest.md` incremented) → older summaries stale; orchestrator reports count and re-dispatches.

**Cleanup.** `.ingest/` is kept after successful writes. It's the audit record. Only `/harvest` or `tools/clear_ingest_cache.py <topic>` removes it.

## `/research` coordination

`/research`'s tail already invokes `/ingest raw/research/<topic-slug>`. The new `/ingest` handles fan-out transparently. Two small edits:

1. Step 6 wording — note that `/ingest` dispatches one subagent per captured source and produces one consolidated review (not per-source back-and-forth).
2. `tools/audit_captures` remains pre-`/ingest`; broken captures are a pre-dispatch concern since subagents will choke on them.

Everything else in `/research` stays untouched (capture rules, source attribution, editorial framing, DOMAIN-SLOTs for authoritative-sources and source-type-notes).

## DOMAIN-SLOT boundaries

**Generic kit (harvestable to `main`):**
- Orchestrator/subagent topology
- Subagent contract: inputs, read-two/write-one rules, output frontmatter + fixed sections (One-line, Cross-ref candidates, Conflict flags, Proposed page shape)
- `.ingest/` layout, `run.json` schema, resume semantics, `schema_version` handling
- Aggregation logic (page plan, cross-ref union, conflict surfacing, low-value flagging)
- Review packet structure
- Write sequence (index / revisions / log tracking)

**Remaining in `<!-- DOMAIN-SLOT: takeaway-prompts -->`:**
- The domain-specific schema sections the subagent fills in (Method / Results / Applicability / Novelty / Repro / Adoption / Conflicts for this wiki). Other wikis replace these with their own schema.

**No new DOMAIN-SLOTs.**

## CLAUDE.md edit

One new line under "Raw Sources":

> `raw/<topic>/.ingest/` is the **one exception** to the immutability rule — it holds derived summaries written by `/ingest`'s subagents. Raw source files themselves are still never modified.

## Error handling

**Subagent-level failures:**

| Failure | Detection | Response |
|---|---|---|
| Subagent errors out (API, timeout, crash) | Agent tool returns error | `run.json` entry → `failed` with error. Continue waiting for siblings. Report in review packet. User decides retry or skip. |
| Schema-invalid summary | Orchestrator validates each summary on read | Mark `invalid`. File kept for inspection. Retry or skip. |
| Subagent writes outside `.ingest/` | Post-run check | Mark `invalid`. Flag loudly — contract breach. |
| Empty / near-empty summary | Size heuristic | Warn, don't block. User may skip. |

**User-disputed aggregation.** User can reject the page plan at the review gate (edit boundaries, split/merge pages, mark sources to skip). Orchestrator accepts the edited plan verbatim and proceeds. No "convince the user" loop — rulings are final.

## Testing

Two unit-testable pieces:

1. **`tools/ingest_plan.py` (new)** — pure function: takes a list of summary files, returns page plan + cross-ref graph + conflict list. Tested on golden-input fixtures under `tests/fixtures/ingest/`.
2. **`tools/audit_captures.py` (existing)** — unchanged.

The orchestrator and subagent prompts live inside `ingest.md` as prose — not unit-testable code. Integration smoke-test: run `/ingest tests/fixtures/ingest-smoke/` (a minimal 2-source fixture with a pre-known conflict) and eyeball the review packet + resulting pages. Documented as a manual QA step in CLAUDE.md, not automated.

## Process learning

Log in `master_notes.md` with `Scope: kit`:

> Reading a safety/alignment paper dense with content-policy vocabulary into the main Claude Code context can trigger the usage-policy classifier, even though each source is individually legitimate. Fix: subagent-per-source isolation so raw bodies never accumulate in one session. This redesign is the concrete response.

## Open questions

None. All consequential decisions settled during brainstorming:
- Subagent output boundary: structured takeaways only, no wiki writes (chosen from A/B/C)
- Human-gate cadence: single batch review after all summaries (chosen from A/B/C/D)
- Subagent wiki context: index + source, not whole wiki (chosen from A/B/C)
- Single-file behavior: always spawn a subagent (chosen from A/B/C)
- Persistence: summaries to disk, committed (chosen from A/B/C)
- Orchestrator waits for all subagents before remediation (explicit user requirement)
