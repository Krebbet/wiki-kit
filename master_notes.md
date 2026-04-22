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

### 2026-04-21 — capture_pdf missing User-Agent header; 403 on ftc.gov
**Scope:** kit
**Observation:** Direct fetch of FTC PDFs (`sp6b-issue-spotlight.pdf`, `p246202_surveillancepricing6bstudy_researchsummaries_redacted.pdf`) via `capture_pdf.py --src <URL>` returned 403 Forbidden. Reproduced with `curl -sI <URL>` — default UA yields 403 via Akamai; `curl -H "User-Agent: Mozilla/5.0..."` yields 200. `capture_pdf.py` does not set a User-Agent. Workaround: curl the PDFs locally with a browser UA, then pass local paths to `capture_pdf --src`.
**Implication:** Add a sane browser User-Agent to the httpx client in `capture_pdf.py`'s download path (same convention `capture_url.py` presumably already uses). Government and enterprise sources behind Akamai / Cloudflare are a load-bearing category for many wikis; this will bite repeatedly otherwise.
**Status:** applied (2026-04-21 kit harvest → main @ 678dc4c)

### 2026-04-21 — capture_url mishandles protocol-relative URLs on Wikipedia
**Scope:** kit
**Observation:** Capturing `en.wikipedia.org/wiki/Dynamic_pricing` produced repeated `download_asset failed` warnings: first for `//upload.wikimedia.org/...` ("Request URL is missing an 'http://' or 'https://' protocol"), then for the fallback `http://upload.wikimedia.org/...` (403 Forbidden — Wikimedia requires https on some upload endpoints). Main article markdown captured fine; only thumbnail images are missing. Two compounding bugs: (1) protocol-relative URLs not resolved via `urljoin` against page URL; (2) fallback retry appears to prepend `http://` rather than matching the source page's scheme.
**Implication:** In `capture_url.py` asset resolver, use `urllib.parse.urljoin(page_url, asset_href)` so protocol-relative and root-relative URLs both resolve correctly. Default scheme should be the source page's scheme (`https://`), not `http://`.
**Status:** applied (2026-04-21 kit harvest → main @ 678dc4c)

### 2026-04-21 — /research should signpost the phase transition into ingest
**Scope:** kit
**Observation:** `/research` step 6 says to "Integrate via `/ingest`" but slash commands do not nest — the model follows `/ingest`'s process inline without announcing it. From the user's perspective the boundary is invisible; it can read as "research paused for no clear reason" when `/ingest` reaches its "wait for user input" checkpoint. In this session the user asked explicitly whether ingest runs automatically after research — legibility issue, not a behaviour issue.
**Implication:** Add a one-line announcement requirement to `/research` step 6 — literally "— transitioning to ingest —" or similar, so the user sees the phase boundary. Optionally mirror on step 5→6 and 6→7 for consistent signposting. Pure prose change to `.claude/commands/research.md`; no tooling change.
**Status:** applied (2026-04-21 kit harvest → main @ 678dc4c)

### 2026-04-21 — /lint should emit a summary document and then auto-ingest surfaced raw sources
**Scope:** kit
**Observation:** Current `/lint` flow ends with an interactive "would you like me to fix any of these issues?" prompt. User wants a different flow for lint: (1) produce a summary document as a persisted artifact (not just inline chat output), presented to the user first. (2) Lint step 6 ("coverage gaps — important concepts discussed in `raw/` source documents that have no wiki page or are only mentioned in passing") currently only reports gaps; user wants it to *then* run `/ingest` on any un-ingested raw sources it surfaces, so lint closes the coverage gap rather than merely naming it.
**Implication:** Two changes to `.claude/commands/lint.md`:
1. Persist the lint report to a file (e.g., `wiki/lint-reports/YYYY-MM-DD.md` or similar) before any remediation, so the user has a durable artefact to review. Present a pointer to the file, not only inline output.
2. After presenting the report, for coverage-gap items that are *un-ingested raw source files* (distinct from conceptual gaps in existing pages), invoke the `/ingest` process on each. Apply the same phase-transition signposting as /research (previous note). Respect `/ingest`'s user-input checkpoint — the user still approves page structure per source.
**Status:** applied (2026-04-21 kit harvest → main @ 678dc4c)

### 2026-04-21 — Fast Company and Wiley online library bot-wall captures (add to known-hosts list)
**Scope:** kit
**Observation:** During `/research platform cooperatives`, capturing `fastcompany.com/90651242/...` via `capture_url.py` returned only a captcha-delivery script (geo.captcha-delivery.com — Datadome-style). Capturing a Wiley open-access PDF via `capture_pdf.py --src https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/apce.12478` returned 403 even with the browser User-Agent now in place. Neither site is currently listed in `research.md`'s "Known bot-walled hosts" paragraph.
**Implication:** Extend the bot-walled-hosts list in `research.md` step 4 to include Fast Company (Datadome captcha) and Wiley Online Library (403 on pdfdirect). Consider: (a) improve `capture_url.py` to detect common captcha/bot-wall signatures (Datadome cookies, Cloudflare challenge pages) and exit non-zero with a clear message rather than writing a thin capture; (b) document the workaround pattern (substitute with a republished or mirror source, or ask the user to download manually) per the existing "ask the user" convention for MDPI/ScienceDirect. The capture-side detection would also catch the PCC-about case where trafilatura captured headings only, not the JS-rendered body — those returned 718 bytes initially, below the ~2KB threshold the merged research.md already flags.
**Status:** open

### 2026-04-21 — /harvest should fast-forward local main to origin/main before branching
**Scope:** kit
**Observation:** During the 2026-04-21 harvest, `git switch -c kit-harvest-2026-04-21 origin/main` correctly branched from the live `origin/main` ref, but local `main` was 2 commits behind (someone had merged PR #1 "kit-learning-capture" since the local tree was last touched). This was not detected before the final merge. When I eventually ran `git merge --ff-only kit-harvest-...` into local main, the output showed *all* commits between the stale local HEAD and the harvest HEAD — including the 2 that were already on origin/main — making it look as though the harvest had promoted a large amount of additional content (including DOMAIN-SLOT bodies and `master_notes.md`, which are meant to be skipped). The push was correct — `a94db53..678dc4c` shipped only the 5 harvest commits I added — but the merge output was genuinely alarming until I traced it.
**Implication:** Add a pre-check in `/harvest` step 1 (or step 2 right after `git fetch origin main`): compare `git rev-parse main` to `git rev-parse origin/main`. If they differ, first fast-forward local main to origin/main (safe as long as it is a pure ancestor — verify with `git merge-base --is-ancestor main origin/main`). This ensures the eventual ff-merge output reflects *only* the harvest diff. If local main has diverged rather than merely lagged, stop and surface it. Pure prose change to `.claude/commands/harvest.md`.
**Status:** open

### 2026-04-21 — capture_pdf marker engine has no graceful fallback on CUDA OOM
**Scope:** kit
**Observation:** On a host where another process held ~21 GB of the 23.5 GB GPU, `capture_pdf --engine marker` for the HBS working paper failed with `CUDA out of memory. Tried to allocate 20.00 MiB...` and exited with a stacktrace. No automatic fallback. Workaround: re-ran with `--engine pymupdf` — cost was 2 broken image refs in the arXiv capture (figures that marker would have extracted, pymupdf did not).
**Implication:** Either (a) catch `torch.cuda.OutOfMemoryError` and retry on CPU with a clear single-line warning, (b) catch and emit a one-line error pointing to `--engine pymupdf` instead of a stacktrace, or (c) add an explicit `--device cpu` flag for users on contended GPU hosts. Option (b) is the cheapest useful fix.
**Status:** applied (2026-04-21 kit harvest → main @ 678dc4c)
