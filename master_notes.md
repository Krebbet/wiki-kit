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

### 2026-08-19 — `audit_captures` reports "0 issues" while its two most valuable checks never run
**Scope:** kit
**Observation:** `tools/audit_captures.py:71` gates both the missing-source-PDF check and the thin-capture
check behind `if pdfs_dir.exists():`. `tools/capture_pdf.py:102` downloads the source to a **temp** directory
as `source.pdf` and never copies it into `<topic>/pdfs/`, so for any URL-sourced PDF that directory is never
created. Verified: `find raw -type d -name pdfs` returns nothing across all seven topic dirs captured today.
Every one of those topics reported `Total issues: 0`, and in every case only the image-reference checks
actually executed. The one thin capture we did have (Parkinson, 561 words against a full essay) was caught by
an agent reading the file, not by the audit.
**Why it matters more than a normal bug:** the failure is silent and reports *success*. `/research` step 5
tells the operator to run this audit as the fidelity gate before `/ingest`, so a clean audit is exactly the
signal that licenses proceeding. It licensed proceeding seven times today on a check that never ran. A tool
that cannot perform its check must not return the same output as a tool that performed it and passed.
**Implication:** two defensible fixes, and they are not exclusive.
(a) Make `capture_pdf` honour the contract the audit and the `/research` domain notes both assume — persist
the fetched PDF to `<out>/pdfs/<slug>.pdf` instead of discarding it with the temp dir. This also makes
captures re-derivable without re-fetching, which matters because `raw/research/` is gitignored.
(b) Make `audit_captures` report `SKIPPED (no pdfs/ directory — source PDFs not retained)` for the checks it
cannot run, and exit non-zero or print a prominent warning rather than folding them into a clean bill of
health. Silence and success must not be the same output.
Note (a) alone would change disk behaviour for every wiki; worth checking with the user before harvesting,
since some may have chosen not to retain PDFs. (b) is safe unconditionally and should go first.
**Status:** open

### 2026-08-20 — `capture_pdf` has no timeout; marker hung 2h+ on a 25-page scan
**Scope:** kit
**Observation:** A marker run on a 25-page scanned PDF (`burawoy.berkeley.edu/.../Weber.Bureaucracy.pdf`) ran
for **2 hours 8 minutes** without completing or failing, and because `capture.sh` processes a spec file
sequentially, it blocked the other seven sources in that job for the whole period. Nothing in `capture_pdf`
bounds the conversion, so a pathological input stalls indefinitely and silently — there is no progress output,
no timeout, and no way to distinguish "slow" from "hung" without inspecting process elapsed time by hand.
Scanned documents appear to be the trigger: marker's OCR path on a scan is far more expensive than on a
digital-native PDF of the same page count, and page count alone does not predict it.
**Implication:** `capture_pdf` should take a `--timeout` (defaulting to something like 15 minutes) and, on
expiry, either fail cleanly with a message naming the engine or automatically retry once with
`--engine pymupdf`, which handles scans far faster at some fidelity cost. Either behaviour is better than an
unbounded stall. A cheaper interim mitigation is a note in `/research` telling the operator that a scanned PDF
may need `--engine pymupdf` from the start, and that a capture exceeding ~15 minutes should be treated as hung
rather than slow.
**Status:** open

### 2026-08-21 — `capture_pdf` does not verify the download is a PDF, producing misleading errors
**Scope:** kit
**Observation:** When a URL returns an HTML error page or a JSON redirect pointer instead of a PDF,
`capture_pdf` saves the bytes as `source.pdf` and hands them to marker anyway. marker then detects the file is
not a PDF and tries to convert it, emitting `Failed to convert /tmp/wk-pdf-*/source.pdf to PDF: No module
named 'weasyprint'`. The operator sees a **missing-dependency error** for a package that is not in
`pyproject.toml` and never was, when the actual problem is that the server returned a 500 page. Two separate
sources this session failed this way, and diagnosing either took a manual `curl -sI` to discover the real
cause.
**Implication:** check the magic bytes (`%PDF-`) or the response `content-type` immediately after download and
fail with the real reason — "server returned text/html, not a PDF (HTTP 500)" — before marker is invoked. This
is a three-line fix that converts a misleading error into an actionable one. Note also that the weasyprint
code path lives inside `marker-pdf`, not in this repo, so the dependency is undeclared here by construction;
that is a second reason not to let a non-PDF reach marker at all.
Related to the earlier entry on `audit_captures` reporting success for checks it never ran: both are cases of
the tooling giving a confident answer that describes something other than what happened.
**Status:** open

### 2026-08-21 — `capture_url`'s bot-wall detection misses SEC EDGAR's "undeclared automated tool" page, and its browser-spoofing User-Agent is the actual cause
**Scope:** kit
**Observation:** Two SEC EDGAR filings (Meta's 10-K and DEF14A proxy, job `institution-case-profiles`) were
captured with `capture_method: url`, exited zero, and wrote plausible-looking 63-line markdown files — but the
content was SEC's block page, "Your Request Originates from an Undeclared Automated Tool." `audit_captures`
reported 0 issues, because its checks (image refs, PDF pairing, thin-capture-by-line-count) don't apply to a
short-but-well-formed HTML capture. Only reading the files by hand caught it — exactly the failure mode the
2026-08-21 `capture_pdf` entry above describes for a different tool. Root cause is double: (1) `capture_url`'s
`_BOT_WALL_SIGNATURES` list (in `tools/capture_url.py`) does not include SEC's phrasing, so the built-in
bot-wall guard didn't fire; (2) `USER_AGENT` in `tools/_common.py` deliberately spoofs a real browser to get
past sites like ftc.gov — but SEC EDGAR's policy is the mirror image: it wants a **declared, non-browser**
User-Agent identifying the actual tool and a contact ("Please declare your traffic by updating your user agent
to include company specific information"), and rejects generic browser UAs as undeclared bot traffic. The two
sites need opposite UA strategies, and the tool only has one. Confirmed the fix works: `curl` with
`User-Agent: <tool-name> <contact-email>` against the same URL returns the real filing (2.3MB real XBRL/HTML,
vs. the 63-line block page). Worked around manually this session by fetching with a compliant UA and running
the result through `trafilatura.extract` directly, matching the tool's own extraction pipeline.
**Implication:** add SEC's block-page phrase ("undeclared automated tool") to `_BOT_WALL_SIGNATURES` so this at
least surfaces as a loud failure instead of a silent success. The deeper fix is a `--declared-ua "<contact>"`
flag (or an EDGAR-specific host rule) that swaps in a compliant, non-spoofed User-Agent for hosts that require
one — SEC EDGAR is a first-class, frequently-needed source for this wiki's institution-case-profile work
(10-Ks, proxies, filings) and will recur every time a public-company case is captured.
**Status:** open

### 2026-08-21 — Evidence-tier token retirement needs a wiki-wide grep, not a spot pass
**Scope:** kit
**Observation:** `[framework]` was retired and normalised to `[model]` on 2026-08-20, per `CLAUDE.md`. The
2026-08-21 lint run found it still present, unnormalised, in 10 of the wiki's ~126 pages — including
`transaction-costs.md`, one of the wiki's oldest and most heavily cross-referenced pages. Whatever swept the
token the first time evidently touched only recently-edited pages, not the whole corpus.
**Implication:** any future evidence-tier vocabulary change (retiring a token, adding one, renaming one)
should be applied via `grep -rl '\[oldtoken' wiki/` across the entire wiki, not a pass over pages edited in
the same session as the change. Worth adding as a standing step in the `/lint` skill's domain-specific checks
rather than relying on the normalisation event itself to be exhaustive.
**Status:** open

### 2026-08-21 — Case/theory linkage check needs an explicit backward pass
**Scope:** kit
**Observation:** `/lint` check 13 asks whether framework/mechanism pages link to case-study pages and vice
versa. When a case-study job (job 15, `institution-case-profiles`) lands after the framework pages it draws
on already exist, the case pages correctly link forward to the frameworks they apply, but the frameworks —
written with no way to know a case would later cite them — have no forward link back. Confirmed on this wiki:
three case pages linked out to six framework pages; none of the six linked back until this lint run added
them manually.
**Implication:** any wiki whose case-study job runs after its framework pages exist will hit this same
one-directional gap by construction. The `/lint` skill's check 13 should explicitly instruct a "grep each
named framework page's own Related section for the case page, don't just read the case page's outbound
links" step, since reading only the case page will make the check look compliant when it isn't.
**Status:** open

### 2026-08-25 — `capture_url`/`capture_pdf` fail against Cloudflare-gated academic publishers and gov domains
**Scope:** kit
**Observation:** This wiki's first `/weekly-brief` sweep selected 5 sources for capture. 3 of the original 5
picks (two AJPS articles, one Governance article — all onlinelibrary.wiley.com) came back as Cloudflare
"Just a moment... Performing security verification" bot-check pages, not the article text; `tools.capture_url`
has no bot-wall detection for this signature (unlike the SEC EDGAR case logged 2026-08-21, this one didn't
even fail loudly — the audit tool's "suspiciously thin" heuristic missed it too, since the challenge page's
line count wasn't thin enough to trip the threshold; it was only caught by an image-path-collision flag,
which is an accident, not a designed check). Separately, mercatus.org also served the same Cloudflare
challenge page (worked around by finding the piece's Substack syndication mirror), and both gao.gov and
oecd.org returned flat 403s to every URL pattern tried, including with a browser User-Agent — no HTML
challenge page at all, just a hard block.
**Implication:** two distinct gaps. (1) `tools.audit_captures` should add a dedicated Cloudflare/bot-check
signature check (grep captured markdown for "Performing security verification" / "Just a moment" / similar
challenge-page strings) rather than relying on the thin-capture and image-collision heuristics to catch it by
accident — a systematic false-negative right now. (2) Wiley (onlinelibrary.wiley.com), Mercatus (mercatus.org),
GAO (gao.gov) and OECD (oecd.org, oecd-ilibrary.org) are all effectively uncapturable by the current tooling
and should probably be marked as "landing-page-only, expect to substitute a preprint/syndicated mirror" in
this wiki's `reference-sources.md` rather than treated as directly capturable — this will recur every week
these sources are in the candidate pool, since GAO and OECD are both explicitly-watched source categories for
this wiki (primary institutional documents; multilateral comparative-governance reports).
**Status:** open
