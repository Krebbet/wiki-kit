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
**Status:** open

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
**Status:** open
