# Ingest a New Source

Process raw source documents into the wiki by dispatching one subagent per source, aggregating structured summaries, and writing wiki pages from a single human review gate. Main context never reads raw source bodies.

## Arguments

$ARGUMENTS — a file path or a directory path. If a directory, every `*.md` file in it (non-recursive) is treated as a source.

## Critical rules

- **Main agent MUST NOT read raw source bodies.** Only subagents read `raw/**/*.md` source content. Main agent reads only `.ingest/*.summary.md` (small, structured) and the specific existing wiki pages that the review plan touches.
- **Subagents write only `.ingest/<slug>.summary.md`.** No other files. No wiki writes.
- **All wiki writes happen in the orchestrator, after the human gate.**

## Placeholder convention

Bash snippets in the pipeline refer to a few variables the orchestrator must bind before executing:

- `TOPIC_DIR` — absolute path of the topic directory (file's parent if `$ARGUMENTS` is a file).
- `WIKI_INDEX` — absolute path of `wiki/index.md` in this repo.
- `RUN_UPDATE_JSON` — when recording a subagent's completion, a single-line JSON blob like `{"01-foo": {"status": "ok", "summary": "01-foo.summary.md"}}`.

Bind these before running any snippet. Example:

`TOPIC_DIR=/abs/path/to/raw/research/post-training-alignment-2026`
`WIKI_INDEX=/abs/path/to/wiki/index.md`

## Pipeline

### 1. Resolve inputs

Normalise `$ARGUMENTS` to a topic directory and a list of source files:
- If `$ARGUMENTS` is a directory: enumerate `*.md` at the top level.
- If `$ARGUMENTS` is a file: topic_dir = parent dir; sources = [that file].

Read `wiki/index.md` once. Keep its contents in your working memory — subagents will each need the path to it.

### 2. Compute dispatch list

Run:

```bash
poetry run python -c "
from pathlib import Path
from tools.ingest_plan import compute_dispatch_list
import json, sys

topic = Path(sys.argv[1])
sources = sorted(topic.glob('*.md'))
to_dispatch, cached = compute_dispatch_list(topic, sources)
print(json.dumps({
    'to_dispatch': [str(p) for p in to_dispatch],
    'cached': [str(p) for p in cached],
}))
" "$TOPIC_DIR"
```

Report to the user: `N sources total, K cached, (N-K) to dispatch`.

### 3. Dispatch subagents in parallel

For every source in `to_dispatch`, spawn a `general-purpose` Agent with the prompt template below. **Send all Agent tool calls in a single message** so they execute in parallel.

Subagent prompt template (substitute `<SOURCE_PATH>`, `<TOPIC_DIR>`, `<SLUG>`, `<WIKI_INDEX>`). The orchestrator already has `$WIKI_INDEX` bound per the Placeholder-convention block above; substitute its value when dispatching.

```
You are ingesting ONE raw source into a structured summary file. Your output is consumed by an orchestrator that aggregates many such summaries into a wiki update plan.

Read only these two paths:
- <SOURCE_PATH>   (the one raw source you own)
- <WIKI_INDEX>    (absolute path to wiki/index.md — for cross-ref candidate naming)

Do NOT read:
- Other raw sources
- Sibling summaries in .ingest/
- Any other wiki pages

Write exactly ONE file:
- <TOPIC_DIR>/.ingest/<SLUG>.summary.md

Use this schema EXACTLY:

---
source: "<fill in with the relative path from repo root, e.g., raw/research/foo/01-bar.md>"
slug: "<SLUG>"
summarized_on: "<fill in with today's ISO date, e.g., 2026-04-21>"
schema_version: 1
---

# <source title>

## One-line
<single sentence: what is this source, what does it claim>

<!-- DOMAIN-SLOT: takeaway-prompts -->
   - (Domain-specific takeaway prompts go here — bootstrap fills this in. Examples: for history, flag dates and key actors; for science, flag methodology and data; for cooking, flag ingredients and technique names.)
   <!-- /DOMAIN-SLOT -->

## Cross-ref candidates
- [[existing-page-name]] — <why this source touches it: extends / contradicts / parallels>
- ...

## Conflict flags
- Claim: <precise statement from this source>
  Contradicts: [[existing-page]] which says <precise existing statement>
  Basis: <quote or tight paraphrase, with which section of the source>
(or `(none)` if no conflicts)

## Proposed page shape
- New page: <title> — <one-line justification>
- OR: extend [[existing-page]] with section "<section name>"
- OR: split into N pages: ...

Return value: a single line confirming the file was written, plus any warnings (e.g., "source appears truncated at line X").
```

### 4. Wait for all subagents; update run.json

**When**: after each subagent returns (success or failure). Invoke the snippet below once per subagent completion with a single-entry blob.

**What**: construct `RUN_UPDATE_JSON` as a single-entry object keyed by slug, e.g. `{"01-foo": {"status": "ok", "summary": "01-foo.summary.md"}}` on success or `{"01-foo": {"status": "failed", "error": "timeout"}}` on error.

**How success is determined**: check that `$TOPIC_DIR/.ingest/<slug>.summary.md` exists AND `tools.ingest_plan.parse_summary()` on it does not raise `SummarySchemaError` (imported from `tools/ingest_plan.py`). The Agent tool's return line is not authoritative.

> **Orchestrator does not trust the Agent return value for success.** After each return, check both:
> 1. `$TOPIC_DIR/.ingest/<slug>.summary.md` exists.
> 2. `poetry run python -c "from tools.ingest_plan import parse_summary; parse_summary('$TOPIC_DIR/.ingest/<slug>.summary.md')"` exits 0 (it raises `SummarySchemaError` on schema failure).
> Only if both pass: record `status: "ok"`. Otherwise `status: "failed"` with the error reason.

Persist via (reads JSON from stdin to avoid shell quoting land-mines):

```bash
echo "$RUN_UPDATE_JSON" | poetry run python -c "
import json, sys
from pathlib import Path
from tools.ingest_plan import load_run_state, save_run_state

topic = Path(sys.argv[1])
state = load_run_state(topic)
state['sources'].update(json.loads(sys.stdin.read()))
save_run_state(topic, state)
" "$TOPIC_DIR"
```

Block on all siblings before moving to aggregation.

### 5. Aggregate

Run:

```bash
poetry run python -c "
from pathlib import Path
from tools.ingest_plan import aggregate
from dataclasses import asdict
import json, sys
topic = Path(sys.argv[1])
summaries = sorted((topic / '.ingest').glob('*.summary.md'))
plan = aggregate(summaries)
print(json.dumps({
    'page_plan': [asdict(x) for x in plan.page_plan],
    'cross_refs': [asdict(x) for x in plan.cross_refs],
    'conflicts': plan.conflicts,
    'merge_candidates': [asdict(x) for x in plan.merge_candidates],
    'low_value': plan.low_value,
}, indent=2))
" "$TOPIC_DIR"
```

### 6. Human gate — render the review packet

Present this block to the user, filled in from the aggregation output:

```markdown
# Ingest Review — <topic>

## Sources processed
| Slug | Title | Status | Summary path |
|---|---|---|---|
| <slug> | <title> | ok | .ingest/<slug>.summary.md |
| <slug> | — | FAILED (retry?) | — |

## Page plan (proposed)
- NEW: wiki/<topic>/<page-title>.md — sources: [<slugs>]
- EXTEND: wiki/<existing>.md with new section "<name>" — sources: [<slugs>]
- MERGE CANDIDATE: [<slugs>] both propose NEW pages but share N cross-ref pages — suggest single page, confirm?

## Cross-references to add
- [[new-page]] ↔ [[existing-page]] — strong/weak, justification
- ...

## Conflict flags (require ruling)
- <source-slug>: claim X; [[existing-page]] says Y. Basis: ...
  → options: (a) resolve in favour of new source, (b) keep existing, (c) open wiki/conflicts/<slug>.md

## Novelty / adoption highlights
- ...

## Low-value candidates (suggest skip)
- ...

## Awaiting your direction
- Accept page plan as-is?
- Any emphasis / de-emphasis per source?
- Conflict rulings?
- Retry failed summaries?
```

Wait for user input. Accept their page plan edits, skip lists, conflict rulings, and retry list verbatim. No "convince the user" loop.

### 7. Write + track

For each approved page-plan entry:
- **NEW**: create `wiki/<topic>/<title>.md` with frontmatter-free page format: `# Title`, one-paragraph summary, takeaway content drawn from the relevant summaries, `## Source` (listing raw files), `## Related` (cross-refs from the plan).
- **EXTEND**: read the existing page, add the new section, update `## Related` if new cross-refs apply.

Append each written page to `state['pages_written']` and `save_run_state` after each write, so a crash mid-write is resumable:

```bash
PAGE_WRITTEN="wiki/<topic>/<page-title>.md"
poetry run python -c "
import sys
from pathlib import Path
from tools.ingest_plan import load_run_state, save_run_state
topic = Path(sys.argv[1])
page = sys.argv[2]
state = load_run_state(topic)
state.setdefault('pages_written', []).append(page)
save_run_state(topic, state)
" "$TOPIC_DIR" "$PAGE_WRITTEN"
```

After all writes:
- `wiki/index.md` — add/update entries for created or modified pages.
- `wiki/revisions.md` — add a row per logical change.
- `wiki/log.md` — append a dated ingest entry: `## [YYYY-MM-DD] ingest | Source Title or Topic`.
- `run.json` — set `review_completed_at` to now.

## Error handling

| Failure | Detection | Response |
|---|---|---|
| Subagent errors out (API, timeout) | Agent tool returns non-zero | `run.json` → `failed` with error. Continue waiting for siblings. Report in review packet. User decides retry or skip. |
| Schema-invalid summary | `parse_summary()` raises `SummarySchemaError` (from `tools/ingest_plan.py`) when orchestrator tries to aggregate | Treat as `failed`; offer retry with an extra-strict prompt. |
| Subagent wrote outside `.ingest/` | Orchestrator post-check lists files under the topic dir written in the run window | Treat as `failed`; flag loudly — contract breach. |
| Empty / near-empty summary | Size < 500 bytes heuristic | Warn in review packet, don't block. |

## Resume

Re-running `/ingest <same-path>` reads existing `run.json` and skips sources already marked `ok` with a valid summary on disk. Use `poetry run python -m tools.clear_ingest_cache "$TOPIC_DIR"` to force full re-dispatch.

## Report

At the end, print:
- Pages created/modified.
- Conflicts opened under `wiki/conflicts/`.
- Failed/skipped sources, if any.
- Tracking files touched.

## Harvest checkpoint

Did anything surface during this ingest that would help *any* wiki, not just this one? Examples: a source-format gotcha worth warning about in this file, a synthesis pattern worth codifying, a capture bug you worked around. If yes, append a brief entry to `master_notes.md` with `Scope: kit` and `Status: open`, and mention it inline. `/harvest` will pick it up.
