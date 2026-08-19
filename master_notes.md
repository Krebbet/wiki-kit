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

### 2026-08-19 — `capture_pdf` stdout contract broken by pymupdf4llm progress output
**Scope:** kit
**Observation:** `tests/test_capture_pdf.py::test_capture_pdf_pymupdf` fails on a fresh clone. The tool itself
works — the markdown file is written correctly — but `pymupdf4llm` writes its own progress bar
(`Processing /tmp/...pdf... [====] (15/15)`) to **stdout**, so `result.stdout.strip()` yields the progress
text concatenated with the path instead of the path alone. Any caller that parses stdout to locate the
capture (which is the documented contract — `tools/capture_pdf.py` ends with `print(written)`) gets garbage.
Not observed with the default `marker` engine in this run.
**Implication:** either redirect the third-party library's stdout to stderr around the pymupdf call in
`tools/capture_pdf.py`, or have the tool emit the path on a sentinel-prefixed final line and update callers.
The former is cleaner and keeps the contract. Affects every wiki, not just this one.
**Resolution (2026-08-19):** wrapped the `capture(...)` call in `main()` with
`contextlib.redirect_stdout(sys.stderr)`. Chose the blanket guard over silencing each library's progress flag
because it is engine-agnostic — it covers `marker` and `pymupdf4llm` today and any future converter's chatter
without a per-library fix. Errors and warnings still reach stderr; stdout is now the path and nothing else.
**Status:** applied 2026-08-19 — harvested to main as e3bcf3a

### 2026-08-19 — `fetch_transcript` blocked by YouTube ("No video formats found")
**Scope:** kit
**Observation:** `tests/test_fetch_transcript.py::test_fetch_transcript_smoke` fails with
`ERROR: [youtube] jNQXAC9IVRw: No video formats found!`. Updating yt-dlp in the venv (to 2026.07.04) did not
fix it, so this is YouTube-side blocking of unauthenticated extraction from this host rather than a stale
dependency.
**Implication:** YouTube transcripts are a declared source type for this wiki (author lectures, book talks,
Ostrom Workshop seminars), so this is a live gap, not a cosmetic test failure. Likely fix is cookie-based auth
(`--cookies-from-browser`) or a subtitle-only extraction path that avoids format resolution. Until then,
`/research` and `/weekly-brief` should treat YouTube captures as expected-to-fail and fall back to a written
source. Worth confirming whether the other wikis hit this too before investing in a fix.
**Correction (2026-08-19):** the "No video formats found" diagnosis was wrong — or rather, transient. It
stopped reproducing within the hour and unauthenticated extraction now works from this host, so it was
YouTube-side throttling rather than a persistent block. **Do not build a cookie-auth path on the strength of
one bad hour.** If it recurs under load, the right first move is `ignore_no_formats_error: True` (verified to
work, and correct in principle — this tool is subtitle-only and never needs a video format), before reaching
for `--cookies-from-browser`.
The *residual*, reproducible failure was the same defect as the `capture_pdf` entry above: yt-dlp writes
download progress to stdout, corrupting the path-only stdout contract. `quiet: True` does not suppress
progress — `noprogress: True` is the separate switch.
**Resolution (2026-08-19):** added `noprogress: True` to the yt-dlp opts and wrapped `capture(...)` in
`contextlib.redirect_stdout(sys.stderr)`, matching the `capture_pdf` fix. Full suite now 95/95 on a fresh
clone (was 93/95). YouTube transcripts are usable; the declared source type stands.
**Lesson worth keeping:** two red tests were reported as two unrelated problems when they shared one root
cause. The first error message on a network-dependent test is a hypothesis, not a diagnosis — re-run before
writing it down as a finding.
**Status:** applied 2026-08-19 — harvested to main as e3bcf3a

### 2026-08-19 — concurrent ingest jobs race on the shared tracking files
**Scope:** kit
**Observation:** Running two `/ingest` page-writing passes concurrently (different research jobs, disjoint
`raw/` topic dirs, disjoint new pages) still puts them in a lost-update race on the **shared** tracking files —
`wiki/index.md` above all, since it is rewritten as a whole table rather than appended to. Job 5's writer
noticed this itself and flagged it: it had written its 8 index rows, and job 4's writer had created its pages
but not yet done its bookkeeping, so if job 4's writer had read `index.md` before job 5's write it would
silently drop those 8 rows on save. `revisions.md` and `log.md` are append-only in practice and are much
lower risk; `index.md` is the exposed one. `dimensions-of-institutional-variation.md` has the same shape when
two jobs both add rows, and is arguably worse because a dropped dimension row is harder to notice than a
missing index entry.
**Implication:** the kit's `/ingest` assumes one job at a time and says so ("one job at a time, ingested to
completion"), but nothing enforces it and nothing detects a violation after the fact. Cheapest fix is a note
in `ingest.md` telling the orchestrator to re-read `index.md` immediately before writing it and to merge
rather than replace. A stronger fix is to make `index.md` generated rather than hand-maintained — derive the
table from the pages on disk plus their first-paragraph summary, so the whole class of races disappears. A
`/lint` check comparing `ls wiki/*.md` against the index rows would at least catch a drop after the fact.
**Status:** open
