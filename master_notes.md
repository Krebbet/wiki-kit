# Master Notes

Running log of what works and what doesn't — both for this specific wiki's operation and for the collaboration generally. Append-only scratchpad for observations that might deserve to become CLAUDE.md guidance, command updates, or kit-level improvements.

During normal operation, Claude appends observations here with `Status: open`. At `/harvest` time (or whenever you review), entries are triaged: some become kit-level code or doc changes promoted to main via `/harvest`; some become this wiki's project CLAUDE.md updates; some are rejected; some stay open for more signal.

## Format

Append entries using this structure:

```
### YYYY-MM-DD — short title
**Scope:** project | interaction | kit | both
**Observation:** what was noticed
**Implication:** what this suggests for CLAUDE.md, a command, a tool, or process
**Status:** open | proposed | applied | rejected
```

**Scope guide:**
- `project` — specific to this wiki (lands in this wiki's `wiki/CLAUDE.md` or DOMAIN-SLOT content).
- `kit` — generic to wiki-kit itself (gets promoted to main via `/harvest`; every other wiki benefits).
- `interaction` — about how the user and assistant work together (may become memory or user-level CLAUDE.md).
- `both` — overlaps more than one scope.

## Notes

<!-- Entries appended during operation go below. -->

### 2026-04-21 — Raw source bodies in main context can trip the usage-policy classifier
**Scope:** kit
**Observation:** `/ingest` on `raw/research/post-training-alignment-2026/` (11 alignment/post-training papers) crashed mid-run with a Claude Code usage-policy 403. Cause: cumulative main-session context packed with safety-spec excerpts, jailbreak taxonomies, disallowed-content categories, and CoT traces reasoning about harmful requests — the concrete vocabulary a content classifier is tuned for, even though each source individually is a legitimate research paper. The next turn and `/compact` also 403'd because the flagged context was re-sent each call. Only a fresh session recovered.
**Implication:** `/ingest` must keep raw source bodies out of the main session. Design approved in `docs/superpowers/specs/2026-04-21-subagent-per-source-ingest-design.md`: subagent-per-source with coherence orchestration. Main context only ever sees distilled summaries plus the specific existing wiki pages touched by a plan. Also an input signal for `/research` tooling: the capture pipeline shouldn't feed straight into a main-session summarisation loop for topics rich in safety/alignment vocabulary.
**Status:** proposed

### 2026-04-22 — `capture_pdf` --out path resolves relative to CWD; nests when CWD is the target dir
**Scope:** kit
**Observation:** `/tmp/radar_captures.sh` was launched with `OUT=raw/research/radar-2026-04` from CWD `/home/david/code/wiki-ai-trends/raw/research/radar-2026-04`, so marker wrote all 8 PDFs to a doubly-nested `raw/research/radar-2026-04/raw/research/radar-2026-04/` path. The capture itself succeeded (real content, audit-clean once moved), but every output had to be `mv`'d into place after the batch. Asset images were split between the outer (created by my manual eggroll move) and the nested locations and had to be merged with `cp -rn`. The `audit_captures.py` tool didn't catch the misplaced output because it was given the outer dir and only saw the empty layout.
**Implication:** Either (a) `tools/capture_pdf.py` should resolve `--out` to an absolute path early and warn if it nests beyond what looks reasonable, or (b) the `/research` command should explicitly tell the user to run capture commands from the repo root, not from inside the topic dir. Probably (a) — too easy to forget on a long batch script. Could also be a single-line check in `audit_captures` for a `raw/research/<slug>/raw/research/<slug>/` doubly-nested layout.
**Status:** open

### 2026-04-22 — `tools.ingest_plan.parse_summary` quietly fails when given a string instead of a Path
**Scope:** kit
**Observation:** First validation pass in `/ingest` step 4 marked all 10 summaries `failed` with `AttributeError: 'str' object has no attribute 'read_text'`. Cause: passed `str(p)` instead of `Path(p)` to `parse_summary`. The function uses duck-typed `Path.read_text()` and explodes on str. The orchestrator block in `ingest.md` is ambiguous about types — uses `parse_summary('$TOPIC_DIR/.ingest/<slug>.summary.md')` in shell substitution, which evaluates to a str when interpolated.
**Implication:** Either (a) `parse_summary` should accept `str | Path` and convert internally, or (b) the snippet in `ingest.md` should make the `Path(...)` wrap explicit. (a) is friendlier to all future callers. Single-line fix.
**Status:** open

### 2026-04-22 — Aggregator's `merge_candidates` matches on DOMAIN-SLOT marker tokens
**Scope:** kit
**Observation:** `tools.ingest_plan.aggregate()` produced 14 spurious merge_candidates whose `shared_concepts` were words like "domain", "prompts", "slot", "takeaway" — i.e., the literal text of the `<!-- DOMAIN-SLOT: takeaway-prompts -->` markers that appear in every summary. The aggregator extracts named-concept tokens from the full body text without stripping HTML comment markers first.
**Implication:** Strip HTML comments (and ideally a small stoplist of structural words) before extracting shared-concept tokens. Otherwise every multi-source ingest produces O(N²) noise pairs that the orchestrator has to filter by hand. Single-function fix in `tools/ingest_plan.py`.
**Status:** open

### 2026-04-22 — Aggregator's `page_plan` parser misses Proposed-page-shape entries with bold-or-emphasized headers
**Scope:** kit
**Observation:** Out of 10 summaries, 9 produced `kind: "new"` correctly but 01-05-titans-miras produced `kind: "unknown"` with empty title. Cause: that summary used a `**New page**:` markdown bold prefix on its proposed-page bullets where the others used plain `New page:`. The parser regex apparently doesn't tolerate `**`/asterisk wrapping or other emphasis variants.
**Implication:** Loosen the parser to strip leading/trailing markdown emphasis (`**`, `*`, `` ` ``, etc.) before matching the `New page` / `Extend` / `MERGE` keywords. Or have the subagent prompt template show the bullets unambiguously and instruct subagents to keep that exact form.
**Status:** open
