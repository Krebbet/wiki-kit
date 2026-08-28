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
**Implication:** Add a step to `bootstrap.md` that writes `wiki/reference-sources.md` (newer format, with the domain's watched sources surveyed or seeded) and `wiki/watchlist.md` (with `setup_approved: <date>`, `seeded: false`, and empty body), plus `wiki/weekly-briefs/` and `wiki/lint-reports/`. The bootstrap interview should gain the questions those files need — scope in/out, selection priority, delivery/branch/frequency conventions. Also worth extending the template's `wiki/CLAUDE.md` structure tree to list these files.
**Status:** applied — fixed directly on `main` and pushed as `290a770` (2026-08-19), not via `/harvest` (this wiki's `bootstrap.md` had already self-deleted, so there was nothing on the topic branch to promote). Interview grew 7 → 10 questions; new step 5 seeds the radar files; template structure tree and README updated. Other topic wikis need nothing — they are already past bootstrap.

### 2026-08-19 — wiki-agentic-trends was never slot-filled
**Scope:** project
**Observation:** While surveying sibling wikis for conventions, found that `/home/david/code/wiki-agentic-trends` still has all five `{{...}}` placeholders in `wiki/CLAUDE.md` and all five DOMAIN-SLOT regions at raw template text, and still has `.claude/commands/bootstrap.md` present (it self-deletes on success). It has real content regardless — domain guidance was evidently applied in-session rather than through the slot mechanism.
**Implication:** Not this wiki's problem, but that wiki is running without its tailored ingest/lint/query guidance and would benefit from a `/bootstrap` run. Flagging here so it isn't lost. Not actioned.
**Status:** open

### 2026-08-19 — capture_url does not detect the Cloudflare "Just a moment..." interstitial
**Scope:** kit
**Observation:** During `/research neuromorphic commercial viability`, `capture_url` returned **exit 0** on a Wiley article (`advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202500806`) while actually capturing Cloudflare's bot-check interstitial — title `"Just a moment..."`, body `"Performing security verification"`, 755 bytes. Identical result with `--js`. `research.md` documents MDPI (Akamai `Access Denied`) and ScienceDirect (Cloudflare IP-block) signatures, but this newer Cloudflare *challenge* page is not in the detector's signature set. It is only caught by the "under ~2KB is almost certainly a failure" heuristic in step 5 — i.e. by a human reading the file, not by the tool.
**Implication:** Add the Cloudflare challenge signature to `capture_url`'s block-page detection — `Just a moment...` in `<title>`, plus body markers `Performing security verification` / `This website uses a security service to protect against malicious bots` / `Ray ID:`. Wiley (`onlinelibrary.wiley.com`) also belongs on the known-bot-walled-hosts list in `research.md`. Promote via `/harvest`.
**Status:** open

### 2026-08-19 — capture_url succeeds on Nature paywalls, capturing abstract-only
**Scope:** kit
**Observation:** `capture_url` on a paywalled Nature Materials article (`doi:10.1038/s41563-026-02600-y`) exited 0 and produced an **86 KB** file — comfortably over the "under ~2KB is a failure" threshold — but the content is title, authors, abstract, an `## Access options` section, and the full reference list. **No article body.** Size-based heuristics cannot catch this: a Nature reference list alone clears any reasonable byte floor. The wiki nearly ingested an abstract as if it were a paper.
**Implication:** Add a *structural* paywall check to `capture_url` (or to `audit_captures`): flag any capture containing an `## Access options` / `Access through your institution` / `Buy this article` section, or whose non-reference body is a small fraction of total length. Byte-count thresholds are necessary but not sufficient for paywall detection — worth stating explicitly in `research.md` step 5 alongside the existing 2KB rule. Promote via `/harvest`.
**Status:** open

### 2026-08-20 — /ingest page-shape parser leaks markdown emphasis and parentheticals into page titles
**Scope:** kit
**Observation:** `tools.ingest_plan.aggregate` produced `page_plan` titles like `Innatera** (company/vendor page)` and `SNN energy efficiency vs. quantized ANNs" (or similar, under a \`research/\` or \`snn/\` topical subdir)`. The parser tolerates markdown emphasis (per the `d3d9407` fix on main) but does not strip trailing `**`, quotes, or the parenthetical hedges subagents naturally write in a `- New page: **X** — justification` line. Titles are unusable as filenames without hand-cleaning.
**Implication:** Strip paired emphasis markers, surrounding quotes, and any trailing parenthetical from the extracted title in the page-shape parser; or tighten the `ingest.md` template to demand a bare slug (`- New page: \`some-slug\` — justification`). The orchestrator has to rewrite every title by hand today, which quietly defeats the point of the structured aggregation. Promote via `/harvest`.
**Status:** open

### 2026-08-20 — mechanical conflict detection cannot see cross-source conflicts
**Scope:** kit
**Observation:** In a fresh wiki with no pages, every subagent correctly reported `## Conflict flags: (none)` — the template asks each to compare its source against *existing wiki pages*, and there were none. `aggregate` therefore returned `conflicts: []`. But the batch contained a genuine order-of-magnitude conflict **between sources in the same run** (vendor efficiency claims vs two independent hardware-realistic analyses). It was found only because the orchestrator read the summaries and noticed. A first ingest into an empty wiki is exactly when cross-source conflicts are most likely and least detectable.
**Implication:** Add an orchestrator step between aggregation and the human gate: scan the summaries' `## Conflicts` (not `## Conflict flags`) sections for claims about the same quantity that disagree, and propose cross-source conflict files. Alternatively have `aggregate` cluster summaries by shared claim-topic and surface disagreeing pairs. Worth noting in `ingest.md` that `conflicts: []` from a fresh wiki means "no *existing-page* conflicts", never "no conflicts". Promote via `/harvest`.
**Status:** open

### 2026-08-20 — capture_url has no internal timeout; hostile hosts hang instead of failing
**Scope:** kit
**Observation:** `capture_url` against `science.org` and `eetimes.com` does not return. Measured this run: `science.org/doi/10.1126/science.adh1174` and `.../sciadv.adl3350` both hit exit 124 at a caller-imposed 90 s timeout with zero bytes written; `eetimes.com` likewise. An earlier un-timed batch burned its entire 2-minute budget on a single science.org URL and captured nothing at all. This is a **third, distinct** failure mode alongside the two already logged: the Cloudflare challenge fails fast with a small file, the Nature paywall succeeds with a large body-less file, and this one simply never returns. It is the worst of the three for `/weekly-brief`, which runs unattended on a cron — a single hostile URL in the candidate list can consume the whole run and produce no brief, with nothing in the log to explain why.
**Implication:** Give `tools/capture_url.py` (and `capture_pdf.py`) a default wall-clock timeout — 60–90 s seems right based on the successful captures this run, all of which returned in well under 30 s — with a `--timeout` override, exiting non-zero and naming the URL on expiry. Add `science.org` and `eetimes.com` to the known-bot-walled-hosts list in `research.md`, noting they hang rather than block. Promote via `/harvest`.
**Status:** open

### 2026-08-20 — verify watched sources with the capture tool, not WebFetch
**Scope:** both
**Observation:** A subagent verifying the radar used `WebFetch` to check each source's liveness and capturability, and marked three sources down on that basis: Intel's own neuromorphic-lab page (`blocked`, "WAF 403"), Semiconductor Engineering (`probation`, "Cloudflare challenge blocks WebFetch and curl"), and EE Times (`blocked`). Re-testing with `capture_url` — the tool the wiki actually captures with — showed **two of the three were wrong**: Intel's page retrieved cleanly at 5.7 KB, and SemiEngineering retrieved cleanly at both homepage and article level. Only EE Times was genuinely unusable, and for a different reason than reported (it hangs, it does not 403). `WebFetch` and `capture_url` use different clients and headers, so they have materially different blocking profiles. Verifying with one and capturing with the other produces false negatives — and marking a vendor's own site `blocked` would have silently removed a primary source from every future sweep.
**Implication:** State in `lint.md` step 12 and in `weekly-brief.md`'s radar-survey step that source capturability must be verified with `tools/capture_url.py` (or the relevant capture tool), never with `WebFetch` alone. `WebFetch` is fine for judging *relevance and liveness*; it is not evidence about *capturability*. Worth a line in the kit's `reference-sources` template too. Promote via `/harvest`.
**Status:** open

### 2026-08-20 — marker on CPU is not robust under machine contention; /weekly-brief has no fallback
**Scope:** kit
**Observation:** A 7-paper arXiv batch with `capture_pdf --engine marker` on CPU lost **6 of 7** while two other wikis' marker jobs ran concurrently on the same box (16 cores, load average 22–25, ~9 GB and ~8 GB RSS for the competing jobs). Five hit a 300 s caller timeout; one died with exit 134 (SIGABRT). The same tool on the same machine had completed 4 papers in ~6 minutes earlier the same day when the box was idle. Resources were otherwise fine — 102 GB RAM available, swap untouched, 159 GB disk free — so this is pure CPU oversubscription, not memory or disk. Re-running with `--engine pymupdf` succeeded, per `research.md`'s own rule that pymupdf is sanctioned once marker has failed on CPU.
**Implication:** This is an operational hazard for the fleet, not just a one-off. Seven wikis on this machine each run `/weekly-brief` unattended, and step 4 of that skill calls `capture_pdf --engine marker` with no timeout and no documented fallback — so a run that happens to overlap any other heavy job will silently capture nothing and email a brief with `skipped: <slug> (capture failed)` for every paper, or hang indefinitely (see the no-timeout note above). Suggested fix: give `capture_pdf` a timeout with automatic `pymupdf` fallback on expiry, log the downgrade loudly so the resulting wiki page can be flagged as figure-less, and have `/weekly-brief` report engine downgrades in its Run notes. A cheap machine-load pre-check before a marker batch would also help.
**Status:** open

### 2026-08-20 — capture_url --js does not force-expand Nature Communications full text
**Scope:** kit
**Observation:** `capture_url` against a Nature Communications article (`nature.com/articles/s41467-026-76067-5`, DOI 10.1038/s41467-026-76067-5) — a fully open-access journal, no paywall — returned only title, abstract, "Similar content" recommendations, Acknowledgements, Funding, Author info, Ethics, and Supplementary-file links. Introduction, Results, Methods, Discussion and all figures were absent, identically on two attempts: once with default settings and once with `--js` (Playwright fallback) explicitly forced. This is a **distinct failure mode** from the already-documented Nature paywall signature (no `## Access options` / `Buy this article` text present) — the article is OA, so nothing should be gating the body. Likely cause: Nature Comms renders full-text sections behind a tab/lazy-load boundary that neither the default fetch nor Playwright's default wait condition satisfies (probably needs an explicit click/scroll trigger or a longer settle time, not just `--js`).
**Implication:** The existing structural-paywall check (`grep` for "Access options"/"Buy this article") is not sufficient to catch this — a capture can be abstract-only with zero paywall markers. Add a broader "thin Nature capture" heuristic: any nature.com capture missing an `## Introduction`/`## Results`/`## Methods` heading should be flagged regardless of paywall-text presence, and downgraded to a watchlist entry rather than ingested as a full source. Worth investigating whether Nature's full text needs a specific Playwright interaction (e.g., click "Full text" tab) to render. Promote via `/harvest`.
**Status:** open

### 2026-08-27 — marker crashed on CUDA, not CPU contention; a fourth capture failure mode
**Scope:** kit
**Observation:** `capture_pdf --engine marker` on the TaS2 arXiv PDF (2608.24693) died mid-run with `CUDA error: unspecified launch failure` during the table-recognition stage — distinct from the already-logged 2026-08-20 finding (CPU oversubscription, 300s timeouts / SIGABRT, no GPU involved). This machine's GPU has a documented progressive VRAM signal-integrity degradation (see the user's global CLAUDE.md); `unspecified launch failure` is listed there as a expected crash signature, not a code bug. Fallback to `--engine pymupdf` succeeded immediately, per the existing sanctioned-fallback rule.
**Implication:** `capture_pdf`'s marker path can fail for at least two unrelated reasons — CPU oversubscription and GPU hardware instability — and both currently surface as opaque stack traces with no structured signal for the caller to distinguish "retry later" from "fall back now" from "this box's GPU is degrading, stop using marker here." Worth having `capture_pdf` catch CUDA-specific exceptions and auto-fall-back to pymupdf without caller intervention, logging which engine actually produced the output. Not urgent to promote alone, but should be folded into whatever `/harvest` does with the existing marker-robustness finding rather than filed as a wholly separate fix.
**Status:** open

### 2026-08-27 — a scan agent's reported figures didn't exist in the actual captured source
**Scope:** kit
**Observation:** A survey subagent (scanning trade press for weekly-brief candidates) reported a KAIST memristor item with specific accuracy figures (~94.8%/95.0% on human-activity/speech classification). After capturing the actual source page and dispatching an ingest subagent that reads *only* the captured file (never the survey summary or the briefing prompt), the ingest agent found the real source was a two-sentence blurb with **zero quantitative claims** — the figures did not exist anywhere in the captured text. The ingest agent correctly refused to use the briefed numbers and flagged the discrepancy explicitly rather than propagating it.
**Implication:** This is exactly the failure mode the subagent-per-source, read-only-source architecture in `/ingest` and `/weekly-brief` is designed to catch, and it worked as designed — but it's worth noting the failure originates one layer earlier than previously documented (in a *survey/scan* agent's WebSearch-snippet synthesis, not in an ingest agent's source reading, and not in the orchestrator's own recollection as the 2026-08-21 EnCharge incident was). Any pipeline step that free-text-summarizes search results before a source is captured is a plausible injection point for unsourced numbers; the fix already in place (ingest agents read only the raw capture, never the brief) fully contained it this time, but a `/weekly-brief` survey step could add a one-line reminder that its own figures are unverified hints for source discovery, not citable content. Low priority — the existing architecture already handled it correctly.
**Status:** open

### 2026-08-21 — weekly-brief validated the unattended path on its first cron firing
**Scope:** project
**Observation:** The Thursday 23:13 cron fired on schedule (2026-08-20) and completed the full unattended loop: 4 captures, 10 watchlist additions, one new wiki page, commit `6be4a1b`, push to origin, SMTP email, Telegram ping. This contradicts the caveat recorded at install time that the unattended path was unproven. Two design details held up under a genuinely adversarial condition — the run happened while this session had uncommitted work in `master_notes.md` and `wiki/reference-sources.md`. Path-scoped staging kept that backlog out of the commit **even within a shared file**: the run committed its own `master_notes.md` entry while leaving three uncommitted entries from this session untouched.
**Implication:** No action needed; recording the validation so the "unproven" caveat in `wiki/reference-sources.md` § Scheduling can be retired. One small defect to note: the run introduced a broken wiki-link in `wiki/watchlist.md` (`[[../chips/...]]` from a page at the wiki root, which resolves outside `wiki/`), fixed 2026-08-21. Relative-link discipline for pages at the wiki root versus in subdirectories is a plausible `/lint` check.
**Status:** applied
