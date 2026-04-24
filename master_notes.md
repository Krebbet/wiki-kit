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

### 2026-04-21 — parallel Bash batch cancels on first error; fragile for multi-source research captures
**Scope:** kit
**Observation:** During `/research consumer-data-pooling`, running 8 capture commands in parallel via a single Bash batch produced a cascading cancellation when the first command errored (GPU OOM on a marker PDF). The other 7 commands were not executed at all. Repeat attempts with the remaining 7 in a new parallel batch then hit a different first-error (OpenTSS Cloudflare block), cancelling again. Net result: I ended up running each capture one-by-one to avoid the cancellation cascade, which slowed the research phase meaningfully.
**Implication:** Either (a) document the cancellation behaviour in `.claude/commands/research.md` step 4 so the model knows not to batch captures; or (b) prefer sequential captures in research.md's example invocations; or (c) if the harness supports a "best-effort parallel" mode that collects errors without cancelling the batch, document that. Lightweight prose fix in `research.md` is cheapest.
**Status:** open

### 2026-04-21 — MIT Press "wip" subdomain bot-walled by Cloudflare challenge
**Scope:** kit
**Observation:** Capturing `wip.mitpress.mit.edu/pub/...` (the MIT Press work-in-progress / manifold site for open-access book chapters like *Building the New Economy*) returns "Attention Required! | Cloudflare" (2470 chars) both with and without `--js`. The bot-wall detection in `capture_url.py` (from previous kit harvest) correctly caught this and exited non-zero — working as intended.
**Implication:** Add `wip.mitpress.mit.edu` to the "Known bot-walled hosts" list in `research.md` step 4 alongside Fast Company and Wiley. Also consider noting a general heuristic: for book-chapter sources on publisher platforms, prefer an arXiv / SSRN / author-homepage preprint over the publisher URL, since open-access publisher sites increasingly bot-detect capture tools.
**Status:** open

### 2026-04-21 — defunct org websites worth detecting (Squarespace "account expired" pages)
**Scope:** kit
**Observation:** `driversseat.co` (canonical homepage of Driver's Seat Cooperative) returned a Squarespace "Website Expired" page as the full HTML response, which `capture_url.py` captured as a 2.7 KB markdown containing only Squarespace error-page JavaScript. The bot-wall check did not catch it (title "Squarespace - Website Expired" is not Cloudflare-branded). A human reading the file can immediately tell it is a defunct-site wrapper, but automated size-check alone did not flag it (file was above 2 KB).
**Implication:** Extend the bot-wall detector in `capture_url.py` to also flag a small set of defunct-site signatures: (a) Squarespace `SQUARESPACE_CONTEXT.title === "Website Expired"`; (b) GoDaddy "domain parked" pages; (c) 404-redirect-with-200 patterns. These are analogous to bot-walls in that the capture succeeds but the content is worthless. Alternatively, just raise the thin-capture threshold for JS-rendered captures, since defunct-site wrappers tend to be well under 5 KB. The finding that driversseat.co is dead is itself interesting domain content — the tool doesn't need to save the user from it, but it should emit a warning so the user notices rather than letting thin content flow downstream to `/ingest`.
**Status:** open

### 2026-04-22 — OECD document server bot-walls captures (add to known-hosts)
**Scope:** kit
**Observation:** During `/research price-transparency-tools`, capturing the canonical OECD 2018 *Personalised Pricing in the Digital Era* paper via either `one.oecd.org/document/DAF/COMP(2018)13/en/pdf` or `www.oecd.org/officialdocuments/publicdisplaydocumentpdf/?cote=DAF%2FCOMP%282018%2913&docLanguage=En` returned HTTP 403 with the browser User-Agent now in place. Both URLs are the standard OECD document-server patterns, so this is likely to recur for any OECD policy paper in a future research run.
**Implication:** Extend the "Known bot-walled hosts" list in `.claude/commands/research.md` step 4 to include `one.oecd.org` and `www.oecd.org/officialdocuments/*`. Workaround: ask the user to download the PDF manually via a browser and drop it into the raw/ directory for local-path ingest (the convention already in place for MDPI/ScienceDirect).
**Status:** open

### 2026-04-22 — Playwright networkidle unreachable on ad-heavy consumer sites
**Scope:** kit
**Observation:** `capture_url.py --js` uses Playwright with `wait_until="networkidle"` (default 30s timeout). On ad/tracker-heavy consumer sites — specifically `keepa.com` and `camelcamelcamel.com` in this research run — networkidle is never reached because third-party analytics/ads scripts continuously poll. Both captures failed with `Page.goto: Timeout 30000ms exceeded`. These are not bot-walls — the sites serve content; they just never reach a quiet state. `capture_url.py` without `--js` also appears to use Playwright based on the error message, so the fallback path has the same issue.
**Implication:** Three options for `tools/capture_url.py`:
1. Add a `--wait-until` CLI flag accepting Playwright's `load|domcontentloaded|networkidle|commit` values, defaulting to `networkidle` (current) but callable with `domcontentloaded` for ad-heavy consumer sites.
2. Change the default to `domcontentloaded` with a longer total timeout. Safer default for consumer sites; slightly less reliable for SPAs that fetch content after DOMContentLoaded.
3. Fall back to `domcontentloaded` automatically on `networkidle` timeout, with a warning.
Option 1 is most explicit and least behaviour-changing. Option 3 is most invisible-fix but slightly magical. Also document the workaround in `research.md` step 4.
**Status:** open

### 2026-04-22 — Fortuitous redirects to substantively-better content
**Scope:** kit
**Observation:** During `/research price-transparency-tools`, `capture_url.py` on `fakespot.com/faq` returned a Mozilla blog post (`Investing in what moves the internet forward`) because the FAQ URL 301s to the Mozilla shutdown announcement now that Fakespot has been wound down. The new content is *more* useful for the wiki than the original FAQ would have been (confirms the July 2025 sunset with Mozilla's own framing). The capture succeeded, the content passed all quality checks (3.4 KB markdown of real prose), and the ingest used it as the primary shutdown-announcement source.
**Implication:** No kit change needed — this is `capture_url.py` working as designed. Logging as a positive signal that "follow redirects" is doing useful work in the live research stream, and as a reminder for future capture-tool changes: don't over-correct toward "reject any redirect" or "warn on redirect" — the content-quality checks (title, body size, bot-wall detection) are the right locus of scrutiny, not the URL.
**Status:** applied (confirming current behaviour is correct)

### 2026-04-22 — GAO.gov bot-walls captures (add to known-hosts)
**Scope:** kit
**Observation:** During `/research collective-bargaining-group-purchasing`, capturing the GAO-12-399R report on GPO oversight via `www.gao.gov/assets/gao-12-399r.pdf` returned HTTP 403 with the browser User-Agent in place. Falling back to the HTML landing page `www.gao.gov/products/gao-12-399r` returned a 247-byte "Access Denied" page (caught by the existing bot-wall detector). Both URLs are the canonical GAO document-serving patterns — any future GAO report capture will hit the same wall.
**Implication:** Extend the "Known bot-walled hosts" list in `.claude/commands/research.md` step 4 to include `www.gao.gov` (both `/assets/*.pdf` and `/products/*`). Workaround: ask the user to download the PDF manually via a browser and drop it into the raw/ directory for local-path ingest — the convention already in place for MDPI/ScienceDirect/OECD. GAO reports are a high-value source category (US government primary documents on regulatory oversight) so this bot-wall is worth surfacing explicitly rather than leaving it to be re-discovered.
**Status:** open

### 2026-04-22 — Wikipedia Commons image 429 rate-limiting is a recurring pattern
**Scope:** kit
**Observation:** Two separate `capture_url.py` runs against Wikipedia pages in this research run (`Consumers'_co-operative` and `Community_Choice_Aggregation`) hit `429 Too Many Requests (f061ab2)` from `upload.wikimedia.org` when downloading thumbnail images. The markdown-body capture succeeded in both cases, but `download_asset` printed the 429 error for each affected image and the images are absent from the assets directory. This has been observed across multiple research runs now — not a one-off. The 429 response includes a specific tracking code (`f061ab2`) that suggests Wikimedia has per-IP or per-useragent rate limits that `capture_url.py` is hitting when it downloads multiple thumbnails in a short window.
**Implication:** Two options for `tools/capture_url.py`:
1. Add polite-retry-with-backoff on 429 for `download_asset` (e.g., 3 retries with exponential backoff 2s/4s/8s). Low-risk change since we're not hammering — we're just re-trying a small number of thumbnails.
2. Add a `--skip-images` CLI flag that skips asset download entirely and rewrites image refs to the external URL. Useful when the user knows images aren't load-bearing (most Wikipedia captures on this wiki).
Option 1 addresses the symptom; option 2 sidesteps it when the user knows images aren't needed. Both are independent of each other. Also: the 429 message mentions the tracking code — consider including that in the `download_asset failed` stderr message so the user can search Wikimedia's published rate-limit policy if needed.
**Status:** open

### 2026-04-23 — ftc.gov news/press-releases/ bot-walls capture_url even with --js
**Scope:** kit
**Observation:** During `/research seller-algorithm-taxonomy`, capturing `www.ftc.gov/news-events/news/press-releases/2025/01/ftc-surveillance-pricing-study-indicates-...` returned a bot-wall page of 693 bytes with the FTC's "PWH-Alert@ftc.gov" incident-reporting stub (non-Akamai/non-Cloudflare pattern, so existing bot-wall detector did not trip). Retry with `--js` returned the same 693-byte stub. This is the FTC's own anti-scraping WAF for news/press-releases. Note: the earlier kit harvest (2026-04-21) fixed the FTC Akamai 403 on /system/files/ PDFs by adding a browser User-Agent; the /news-events/ path has a different WAF layer that the UA header does not satisfy. PDF captures of FTC documents via /system/files/ still work (confirmed by prior-run `p246202_surveillancepricing6bstudy_researchsummaries_redacted.pdf`).
**Implication:** Add `ftc.gov/news-events/*` to the "Known bot-walled hosts" list in `.claude/commands/research.md` step 4. Also consider extending `capture_url.py`'s bot-wall detector to catch the FTC-specific signature (text includes "The request resembles an abusive automated request" + "PWH-Alert@ftc.gov") so the check-tool fails fast rather than returning a thin capture that slips past the 2KB heuristic. Workaround: when a press release is needed, capture the linked primary PDF (usually at `/system/files/ftc_gov/pdf/*`) or ask the user to download the page manually and drop HTML into `raw/`.
**Status:** open

### 2026-04-23 — PMC (pmc.ncbi.nlm.nih.gov) bot-walls capture_url with reCAPTCHA
**Scope:** kit
**Observation:** During `/research seller-algorithm-taxonomy`, capturing `pmc.ncbi.nlm.nih.gov/articles/PMC10676015/` returned a Google reCAPTCHA challenge page (`title: "Checking your browser - reCAPTCHA"`, 20KB of reCAPTCHA boilerplate JS). Existing bot-wall detector did not catch it — the size was above the 2KB threshold because the reCAPTCHA bundle is verbose. PMC is a high-value source lane (peer-reviewed open-access primary research hosted by NCBI / NLM), so this will bite repeatedly across medicine-adjacent wikis.
**Implication:** Add `pmc.ncbi.nlm.nih.gov` to the "Known bot-walled hosts" list in `.claude/commands/research.md` step 4. Also extend `capture_url.py` bot-wall detector: check for `title == "Checking your browser - reCAPTCHA"` or document body containing `RecaptchaChallengePageUi` — these are unambiguous captcha-page markers. Captures with a reCAPTCHA title should always be treated as failed regardless of byte-count, since the captured content is worthless even when it's 20KB of JS. Workaround: ask the user to download the PDF via a browser and drop the local path, OR search for an arXiv / author-homepage / PubMed-indexed preprint mirror (most biomedical papers on PMC have one).
**Status:** open

### 2026-04-23 — lint should detect 0-byte stub files at wiki/ root (Obsidian auto-creation artifacts)
**Scope:** kit
**Observation:** During 2026-04-23 lint, found 6 stray 0-byte `.md` files at `wiki/` root whose canonical pages exist in the correct subdirectories (`wiki/adnauseam.md` vs canonical `wiki/tools/adnauseam.md`; similar for `wiki/algorithmic-collusion.md`, `wiki/lever-implementation-readout.md`, `wiki/obfuscation-strategic-readout.md`, `wiki/possible-strategic-levers.md`, `wiki/2026-04-23.md`). Most likely cause: Obsidian auto-creates an empty `.md` at the vault root when a user clicks an unresolved `[[wiki-link]]` that the resolver can't place. The vault has `.obsidian/` enabled (visible in git status at session start of the first-user-session of this wiki branch). These stubs:
- Don't appear in the link graph (my own lint extractor filtered on `! -empty`).
- Don't trigger orphan detection (they're not in the pages inventory either).
- Are not detected by any existing lint check.
- Create confusing duplicate-name pairs in file listings.

The lint check I hand-wrote for this session caught them only because I happened to run `find wiki -name "*.md" -type f` (including empty) as initial inventory, then noticed the duplicate basenames.
**Implication:** Add a lint check: `find wiki -name "*.md" -type f -empty` as an early gate; report any 0-byte files as a distinct "stray / noise" category, independent of orphans and broken links. The check should probably exempt files under known Obsidian-special paths (none in this wiki's setup) and recommend deletion. Could live in `.claude/commands/lint.md` as a generic check; would help any Obsidian-enabled wiki-kit deployment.
**Status:** open
