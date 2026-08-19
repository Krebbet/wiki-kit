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

### 2026-08-19 — yt-dlp pinned version is stale; transcript capture broken
**Scope:** kit
**Observation:** Fresh clone of `main` at `dd10a69` installs `yt-dlp 2024.12.23` (per `poetry.lock`). `tests/test_fetch_transcript.py::test_fetch_transcript_smoke` fails against live YouTube with yt-dlp's "Please report this issue... Confirm you are on the latest version using yt-dlp -U" error. YouTube rejects extractors this old, so `/research` and `/weekly-brief` cannot ingest YouTube talks on a new clone.
**Implication:** `yt-dlp` should be unpinned or floated to a recent release in `pyproject.toml`/`poetry.lock` on `main`, or `tools/fetch_transcript.py` should detect the stale-extractor failure and emit an actionable "run `poetry update yt-dlp`" message instead of the raw traceback. Promote via `/harvest`.
**Status:** open

### 2026-08-19 — capture_pdf pymupdf engine pollutes stdout with a progress bar
**Scope:** kit
**Observation:** `python -m tools.capture_pdf --engine pymupdf` writes PyMuPDF's page-progress bar and a "Consider using the pymupdf_layout package" notice to **stdout**, so the documented contract "stdout is the written path" only holds for the *last* line. `tests/test_capture_pdf.py::test_capture_pdf_pymupdf` does `Path(result.stdout.strip())` and fails on a fresh clone even though the capture itself succeeds (verified: `01-attention.md` + `assets/` written correctly).
**Implication:** Either route PyMuPDF's chatter to stderr in `tools/capture_pdf.py`, or fix the test and any caller to take the last non-empty stdout line. The `marker` engine path should be checked for the same issue. Promote via `/harvest`.
**Status:** open

### 2026-08-19 — /bootstrap no longer creates the files /weekly-brief requires
**Scope:** kit
**Observation:** `.claude/commands/bootstrap.md` on `main` @ `dd10a69` fills the five `wiki/CLAUDE.md` placeholders and the four/five DOMAIN-SLOT regions, then self-deletes. It never creates `wiki/reference-sources.md` or `wiki/watchlist.md`. But `/weekly-brief` step 0 **halts** if `reference-sources.md` is missing or `watchlist.md` lacks `setup_approved:` frontmatter, and `/lint` steps 10 and 12 both read `reference-sources.md`. `/lint` and `/weekly-brief` do not create them either. So a wiki bootstrapped strictly by the book is dead on arrival for its two automated operations. All five surveyed bootstrapped wikis have both files, meaning every one of them was hand-seeded outside the documented flow. Two format generations exist in the wild; only the newer one (`## Scope` / `## Selection priority` / `## Local conventions`) matches what the current `weekly-brief.md` reads.
**Implication:** Add a step to `bootstrap.md` that writes `wiki/reference-sources.md` (newer format, with the domain's watched sources surveyed or seeded) and `wiki/watchlist.md` (with `setup_approved: <date>`, `seeded: false`, and empty body), plus `wiki/weekly-briefs/` and `wiki/lint-reports/`. The bootstrap interview should gain the questions those files need — scope in/out, selection priority, delivery/branch/frequency conventions. Also worth extending the template's `wiki/CLAUDE.md` structure tree to list these files. Promote via `/harvest`.
**Status:** open

### 2026-08-19 — wiki-agentic-trends was never slot-filled
**Scope:** project
**Observation:** While surveying sibling wikis for conventions, found that `/home/david/code/wiki-agentic-trends` still has all five `{{...}}` placeholders in `wiki/CLAUDE.md` and all five DOMAIN-SLOT regions at raw template text, and still has `.claude/commands/bootstrap.md` present (it self-deletes on success). It has real content regardless — domain guidance was evidently applied in-session rather than through the slot mechanism.
**Implication:** Not this wiki's problem, but that wiki is running without its tailored ingest/lint/query guidance and would benefit from a `/bootstrap` run. Flagging here so it isn't lost. Not actioned.
**Status:** open
