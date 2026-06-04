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

### 2026-05-23 — lint should auto-flag elapsed time-relative claims
**Scope:** kit
**Observation:** The 2026-05-23 lint found `faa-part-108-bvlos` still describing a "~Feb 2026 deadline" as upcoming, and several pages with "as of <year>" benchmark claims now past the staleness window — while the *watchlist* had already recorded the deadline slip. The primary page lagged the watchlist; nothing mechanically caught it. Also: time-sensitive pages have no `last-verified` header, so freshness checks are all manual judgement.
**Implication:** Two generic lint upgrades worth promoting to the kit: (a) a check that parses dated/relative claims ("by <month year>", "deadline", "as of <year>") and flags any whose date is now in the past without an update note — catches deadline-drift across any wiki; (b) a `last-verified: YYYY-MM-DD` frontmatter convention for time-sensitive pages, with `lint` flagging pages past their domain staleness threshold. Both generalise beyond this wiki.
**Status:** open

### 2026-05-17 — /weekly-brief setup gate checks field presence, not value
**Scope:** kit
**Observation:** `/weekly-brief` step 0 says halt if `wiki/watchlist.md` "lacks a `setup_approved:` frontmatter field". That is a presence check — `setup_approved: false` satisfies it and the unattended run would proceed anyway. A drafted-but-unreviewed watchlist with the field present (even `false`) would not halt.
**Implication:** Harden the skill: halt unless `setup_approved` is explicitly truthy (`true`), not merely present. Until fixed, the safe convention is "only add the `setup_approved` key when you actually approve" — document this in the skill's setup section. Surfaced while drafting setup for wiki-ai-drone (kept the field `false` + warned the user explicitly).
**Status:** open

### 2026-05-15 — bundled yt-dlp too stale for fetch_transcript
**Scope:** kit
**Observation:** `tools/fetch_transcript.py` failed on a valid YouTube talk with `ERROR: [youtube] <id>: Requested format is not available`. The pinned `yt-dlp` in `poetry.lock` was stale; YouTube extractor changes break old versions silently. `poetry run pip install -U yt-dlp` fixed it immediately and the same URL captured fine.
**Implication:** yt-dlp ages out fast (YouTube changes monthly). Options for kit: (a) loosen the `yt-dlp` constraint and document a "if transcript fails, `pip install -U yt-dlp` first" troubleshooting note in `research.md`; (b) have `fetch_transcript.py` detect the format error and self-heal with an auto-update; (c) periodic lockfile refresh. Recommend (a)+(b).
**Status:** open

### 2026-05-16 — burst/parallel transcript fetches trigger YouTube HTTP 429
**Scope:** kit
**Observation:** Running two `fetch_transcript` calls in parallel (plus an earlier `yt-dlp -U` + two prior transcript pulls in the session) caused `HTTP Error 429: Too Many Requests` on subtitle download. One of the two parallel pulls succeeded, the other 429'd and kept 429ing on immediate retry — YouTube IP rate-limit, clears after a cooldown window (minutes–~1 h), not on instant retry.
**Implication:** `fetch_transcript.py` (or research-flow guidance) should serialize YouTube pulls, not parallelize them, and on 429 back off rather than retry immediately. Candidate kit fix: add a small delay/jitter + a single delayed retry in `fetch_transcript.py`, and a `research.md` note "capture YouTube sources one at a time, not in a parallel batch."
**Status:** open

### 2026-05-16 — primary-source capture is high-value when a wiki claim rests on a secondary review's number
**Scope:** kit
**Observation:** `event-cameras-for-uavs.md` cited "fully neuromorphic pipeline … ~0.94 W total" from a secondary PRISMA review. Capturing the primary (de Croon, Science Robotics 2024) showed 0.94 W is the Loihi *board idle* power; the network's marginal cost is 7–12 mW and the canonical figure is 27 µJ/inference — the secondhand framing was off by ~100× and materially understated the result.
**Implication:** Generalizable `/ingest` + `/research` heuristic worth adding to the kit: when a load-bearing quantitative claim traces only to a secondary/review source, flag it and prioritise capturing the primary before the figure propagates. Candidate: a `lint.md` check for quantitative claims whose only `## Source` is a review/survey, and an `ingest.md` takeaway prompt to tag secondhand numbers.
**Status:** open

### 2026-05-16 — shell cwd drift sends captures to wrong dir / triggers false-alarms
**Scope:** kit
**Observation:** The Bash tool persists cwd between calls. A `cd .../wiki && <check>` used for link-integrity left cwd in `wiki/`; subsequent `capture_*` calls with relative `--out raw/research/<topic>` then wrote to `wiki/raw/research/<topic>` instead of the repo-root `raw/`. Earlier in the same session the same drift caused a false "file deleted" scare. Both cost recovery time.
**Implication:** `capture_url/capture_pdf/fetch_transcript` `--out` is interpreted relative to cwd, which is fragile in a long agent session. Kit fixes to consider: (a) capture tools resolve `--out` against the git repo root (e.g. `git rev-parse --show-toplevel`) rather than cwd; (b) `research.md` guidance: always pass an absolute `--out`, or prefix capture commands with `cd "$(git rev-parse --show-toplevel)" &&`; (c) never leave cwd changed — run checks in a subshell `( cd wiki && … )`.
**Status:** open

### 2026-05-16 — PMC can serve a reCAPTCHA wall that passes the fidelity audit
**Scope:** kit
**Observation:** `capture_url` on a PMC article (pmc.ncbi.nlm.nih.gov/articles/PMC11751315) returned a 20 KB Google reCAPTCHA challenge page, not the paper. It passed `audit_captures` (>2 KB, line count not << page count, has a paired… nothing) and the >2 KB heuristic — only the per-source ingest subagent caught it by reading content. Other PMC captures the same day worked, so it's intermittent bot-detection, not a blanket block.
**Implication:** (1) PMC is not a reliably safe mirror — add to the cautious list and prefer the Europe PMC `?pdf=render` endpoint or `capture_pdf` on the DOI when PMC HTML is used. (2) `audit_captures` should add a bot-wall/captcha signature check (look for `recaptcha`, `g-recaptcha`, `challenge-form`, `Just a moment`) independent of size — a captcha page is small-ish but not <2 KB and has many lines, so current heuristics miss it.
**Status:** open

### 2026-05-15 — capture_pdf --engine pymupdf emits image refs it never writes
**Scope:** kit
**Observation:** `capture_pdf --engine pymupdf` on three arXiv survey PDFs produced clean text but 50 dangling `![](assets/<slug>/source.pdf-N-M.png)` refs — the image files are referenced in the markdown but never extracted to disk. `audit_captures` correctly flagged all 50. Text fidelity is fine (no thin-capture flags); only images are missing. Default `marker` engine presumably extracts images, but was avoided here due to GPU contention/degradation.
**Implication:** `pymupdf` path should either extract page images (pixmap per referenced xref) or suppress the image refs entirely so captures pass the fidelity audit. Current behavior guarantees a dirty audit for every figure-bearing PDF captured without marker. Candidate fix in `tools/capture_pdf.py`. Also worth a `research.md` note: pymupdf engine = text-only, expect image-ref audit noise.
**Status:** open

### 2026-05-15 — cdnsciencepub.com is bot/JS-walled like MDPI/ScienceDirect
**Scope:** kit
**Observation:** `capture_url` on a Canadian Science Publishing article (cdnsciencepub.com/doi/10.1139/dsa-2024-0005) hung at Playwright `networkidle` and produced no file, both with and without `--js`; `capture_pdf` on its open-access PDF endpoint returned 403. `preprints.org/manuscript/.../download` also returned 403. Both are open-access hosts that nonetheless bot-block our scripts — same failure class as MDPI/ScienceDirect already named in `research.md`.
**Implication:** Add `cdnsciencepub.com` and `preprints.org` to the "Known bot-walled hosts" paragraph in `research.md` so future runs skip straight to the manual-download fallback instead of burning timeouts. Note these are *open-access* yet still walled — the heuristic "open access = capturable" is false; the wall is bot-detection, not paywall.
**Status:** open

### 2026-05-24 — capture_url can return wrong-but-right-sized content (silent topic swap)
**Scope:** kit
**Observation:** `capture_url` on an amazon.science publications URL returned an **Amazon Ads job posting**, not the MAPF-execution paper — full-sized (passed the >2 KB / not-thin heuristic and `audit_captures`), but the wrong document entirely. Only the ingest subagent reading the body caught it (it sourced the MAPF substance from the arXiv mirror instead and flagged the bad capture in-page). Distinct from bot-walls/captchas: the page is "real" content, just not the requested content (server-side redirect to a generic/marketing/listing page when the canonical URL isn't directly fetchable).
**Implication:** Size/audit heuristics can't catch topic-swap. Cheap defenses worth adding: (a) `audit_captures` or a new check could compare the capture's title/`<h1>` against the requested slug/expected keywords and warn on low overlap; (b) `research.md` guidance — for publisher landing pages, prefer the arXiv/DOI-PDF mirror over the publisher HTML, which is both more capturable and less prone to redirect-to-listing. Recurring lesson: always have a second mirror for any single load-bearing source.
**Status:** open

### 2026-05-24 — page-writer subagents default to the folder-prefixed [[conflicts/x]] link form
**Scope:** kit
**Observation:** When briefed that a conflict page's slug is `conflicts/lidar-vs-vision-autonomy`, fresh page-writer subagents wrote `[[conflicts/lidar-vs-vision-autonomy]]`, but the established wiki convention (every existing content page) is the bare basename `[[lidar-vs-vision-autonomy]]` (Obsidian resolves both, but mixing is untidy and trips strict full-path link checkers). Had to normalize 5 pages post-hoc.
**Implication:** (1) A strict link-integrity check should resolve `[[...]]` by **basename** (Obsidian semantics), not full relpath, or it floods with false positives for any page in a subdir like `conflicts/`. (2) `/ingest` + `/research` page-writer briefs should state the link convention explicitly: "link conflict pages by bare basename `[[slug]]`, not `[[conflicts/slug]]`." Worth baking into the shared subagent prompt template so it doesn't recur each batch.
**Status:** open

### 2026-06-04 — capture_pdf --engine marker fails on NumPy ≥ 2.0 environments
**Scope:** kit
**Observation:** `python3 -m tools.capture_pdf --src <arxiv_pdf_url> --engine marker` exits 137 (OOM/killed) after a NumPy 2.x / PyArrow / sklearn ABI incompatibility cascade (pyarrow `_ARRAY_API not found`). The marker engine imports sklearn → pandas → pyarrow, all of which were compiled against NumPy 1.x. The OOM kill occurs because the process loads conflicting .so files, corrupts memory, and is then killed by the OOM killer. **Update (2026-06-04, stereo-dense-reconstruction session):** The OOM kill with marker actually occurred when CUDA was available (CUDA_VISIBLE_DEVICES not set). Running the SAME marker engine with `CUDA_VISIBLE_DEVICES=""` (forcing CPU) succeeded and produced full captures with extracted images — marker on CPU works fine; the GPU path + NumPy ABI mismatch is the failure point.
**Implication:** On systems with NumPy ≥ 2.0 / old CUDA driver (seen: NVIDIA driver version 12020): first retry is `CUDA_VISIBLE_DEVICES="" python3 -m tools.capture_pdf --engine marker`, NOT `--engine pymupdf`. CPU marker produces images; pymupdf does not. Only fall back to pymupdf if CPU marker also fails. Update the `/research` skill guidance to try `CUDA_VISIBLE_DEVICES="" marker` before the pymupdf fallback.
**Status:** open

### 2026-06-04 — bostondynamics.com and 1x.tech are reliably bot-walled (both trafilatura and Playwright)
**Scope:** kit
**Observation:** Six separate `capture_url` attempts on bostondynamics.com blog/product pages (with and without `--js`) returned 23-line navigation fragments — not real article content. 1x.tech similarly returned 12-line near-empty extractions. Both domains defeat both the trafilatura extraction path and the Playwright JS path. Content appears to be gated behind React/Next.js hydration that doesn't execute in the headless browser, or the servers detect the Playwright UA and serve a stripped template.
**Implication:** Add `bostondynamics.com` and `1x.tech` to the "Known bot-walled hosts" section in `research.md`. Manual-download fallback is needed: open the page in a real browser, use "Save as" or "Copy text", and drop into `raw/research/<topic>/` as a `.txt` or `.md` file. The Robot Report and Robotics 24/7 articles *about* these companies capture cleanly — they are a viable secondary-primary fallback when vendor pages are walled.
**Status:** open

### 2026-05-28 — capture/ingest work should be dispatched to subagents, not run in the main context
**Scope:** kit
**Observation:** During a `/research` run, four `poetry run python -m tools.capture_pdf` commands were run directly in the main conversation context instead of being delegated to a subagent. This bloats the main context window with capture progress output, ties up the main thread, and wastes a larger model on mechanical execution work. The user flagged this explicitly.
**Implication:** Any batch of capture commands (≥2 URLs, or any single long-running capture) should be dispatched to a `haiku`-class subagent via the Agent tool. The subagent handles capture, fidelity audit, and returns a summary (file paths + sizes). Only the summary lands in the main context. Similarly, ingest (reading raw files, writing wiki pages, updating tracking files) is a bounded execution task that belongs in a dedicated `sonnet`-class subagent. The main thread should dispatch both phases and wait for results — it should not run capture scripts or read raw source bodies directly.
**Status:** open
