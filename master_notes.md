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

### 2026-05-11 — capture_url `networkidle` hangs on modern docs sites
**Scope:** kit
**Observation:** `tools/capture_url.py` hardcoded `page.goto(url, wait_until="networkidle", timeout=30_000)`. Modern documentation hosts (Mintlify, etc., and including Polymarket's `docs.polymarket.com`) ship continuous telemetry/heartbeat scripts, so `networkidle` never fires within 30s and every capture fails with `Page.goto: Timeout 30000ms exceeded`. The script's bot-wall heuristic doesn't catch this — it surfaces only as a generic capture failure, but the root cause is a Playwright wait strategy that is wrong for the modern web.
**Implication:** Patched in-situ on this branch: use `wait_until="domcontentloaded"` with a 60s timeout, then opportunistically wait up to 5s for `networkidle` (swallowing its timeout), then a 1s settle. This is a strict improvement — quiet sites still get the same effective gating; noisy ones now succeed. Promote via `/harvest`. Consider whether to additionally expose `--wait-until` / `--wait-timeout` CLI flags, or leave the heuristic implicit. Leaning implicit since the new defaults work for both regimes.
**Status:** applied (kit patch on `polymarket-wiki` branch, awaiting `/harvest` to promote)

### 2026-05-11 — capture_url leaks inline-script bodies on Mintlify-style hosts
**Scope:** kit
**Observation:** Even with `markdownify(..., strip=["script", "style"])`, captures of `docs.polymarket.com` (Mintlify SPA) emitted ~150 lines of escaped JavaScript source as visible text at the top of the markdown body before the real docs content began. The pages parse cleanly with BeautifulSoup, but markdownify's `strip=` parameter does not reliably suppress text nodes inside `<script>` elements that have been promoted into `<main>` for hydration. Captures still contained usable content below the gunk, but the prefix is enormous and would burn ingest-subagent context.
**Implication:** Patched `_main_content_html` to `tag.decompose()` all `<script>/<style>/<noscript>` at the BS4 layer before extracting `<article>`/`<main>`. This is a strict improvement — pages without inline scripts are unaffected; pages with them are now clean. Promote via `/harvest`. Together with the `networkidle`-timeout fix above, this brings capture_url into shape for the modern SPA-docs world that wikis built on this kit will routinely encounter.
**Status:** applied (kit patch on `polymarket-wiki` branch, awaiting `/harvest` to promote)

### 2026-05-13 — capture_url returns Cloudflare interstitial when target host runs a JS bot challenge
**Scope:** kit
**Observation:** Two Dune Analytics dashboard captures (`dune.com/filarm/polymarket-activity`, `dune.com/thxshogun/polymarket-2025-capital-and-whales`) returned ~650-byte files containing only the Cloudflare "Just a moment..." / "Performing security verification" interstitial. The capture script's `domcontentloaded` wait fires on the interstitial DOM; the opportunistic 5s `networkidle` wait expires before Cloudflare's JS challenge completes its handshake and navigates to the real page. `capture_url`'s existing bot-wall heuristic does not catch this signature ("Just a moment...", "Performing security verification", Cloudflare "Ray ID:" footer); the result is a non-zero-exit-non-empty-file that looks superficially OK to downstream tooling.
**Implication:** Two complementary fixes worth doing:
  1. **Extend bot-wall heuristic** in `_looks_like_bot_wall()` to include "performing security verification", "just a moment", "ray id" — so the script exits non-zero on Cloudflare interstitials instead of writing a junk file.
  2. **Add post-DOM Cloudflare-challenge wait** — detect the interstitial after `domcontentloaded`, wait up to 15s for navigation away (using `page.wait_for_url(lambda url: ...)` or `page.wait_for_function`), then capture. This would let benign Cloudflare-protected sites through.
Doing both gives clean fail-fast behaviour on truly blocked hosts plus successful capture on hosts that just have a slow JS challenge. Promote via `/harvest`.
**Status:** open

### 2026-05-12 — parallel-capture race in `next_numbered_filename` produces duplicate index prefixes
**Scope:** kit
**Observation:** When multiple capture commands run in parallel into the same output directory, each invocation independently computes the next index by listing existing files. If two captures race past the listing step before either has written, both stamp the same prefix. Observed twice now — last research run got `02-polymarket-microstructure.md` and `02-polymarket-docs-overview.md`; this run got `06-polymarket-mentions-category.md` and `06-falconx-emerging-trends.md`. Distinct slugs so file paths are unique, but the duplicate prefix is cosmetic noise and would break any tooling that assumes per-prefix uniqueness.
**Implication:** Two cheap fixes: (a) use a per-output-dir file lock around the (list → next_index → write_path) sequence; (b) use a uuid/timestamp suffix instead of a sequential index. (a) preserves the readable ordering, (b) is simpler and removes the race entirely. Either is a small change in `tools/_common.py`. Not blocking — slugs already disambiguate — but cleaner.
**Status:** open

### 2026-05-16 — Polymarket SPA pages now behind Vercel security checkpoint; Gamma API `tag_slug` filter is the bypass
**Scope:** kit
**Observation:** Polymarket rolled out Vercel anti-bot protection on category-landing routes between 2026-05-14 and 2026-05-16. Pages that captured cleanly two days prior (`polymarket.com/tech`, `polymarket.com/pop-culture/movies`, `polymarket.com/pop-culture/music`, `polymarket.com/pop-culture/youtube`, `polymarket.com/pop-culture/celebrities`, `polymarket.com/finance` — captured for the broader-sweep run) now return ~250-byte HTML containing only `"Vercel Security Checkpoint" — "We're verifying your browser"` and a Vercel error link. `capture_url`'s networkidle/script-strip patches do not help; the JS challenge requires a real browser fingerprint Vercel accepts. The bot-wall heuristic in `_looks_like_bot_wall` does not catch the Vercel signature ("Vercel Security Checkpoint", "verifying your browser", "vercel.link/security-checkpoint" link).
**Bypass discovered:** `https://gamma-api.polymarket.com/events?tag_slug=<slug>&active=true&closed=false&limit=30&order=volume24hr&ascending=false` returns the full event list per category — same data the SPA renders, but server-side via the Gamma API. `tag_slug` accepts category names matching the URL slugs (`tech`, `movies`, `music`, `youtube`, `celebrities`, `finance`, etc.). Sort parameters work (`order=volume24hr` / `volume1wk` / `volume1mo`; `ascending=true/false`). Returns the same field set as the existing `tools/capture_polymarket_market.py` per-event endpoint, plus an event-level `tags[]` array and `category` metadata.
**Implication (kit fix):**
  1. **Extend bot-wall heuristic** in `_looks_like_bot_wall` to add `"vercel security checkpoint"`, `"verifying your browser"`, `"vercel.link/security-checkpoint"` so captures exit non-zero on Vercel walls rather than writing 250-byte junk.
  2. **Add a category-level Gamma capture tool** — either extend `tools/capture_polymarket_market.py` with a `--tag-slug` mode or add `tools/capture_polymarket_category.py`. For this run an ad-hoc inline Python script produced the 6 category captures into `raw/research/polymarket-broad-coverage-sweep/`; the tool should be productized.
Both should ship via `/harvest`. Status of the actual broader-sweep run was NOT blocked — captured all 6 categories via the API bypass.
**Status:** open (kit improvements pending)

### 2026-05-16 — Ingest schema validator is brittle on section-name variants
**Scope:** kit
**Observation:** `tools/ingest_plan.parse_summary` requires exact section headers `## One-line`, `## Cross-ref candidates`, `## Conflict flags`, `## Proposed page shape`. When dispatched in parallel, 3 of 8 subagents this run produced variant headers (`## Cross-references` vs `## Cross-ref candidates`, `## Conflicts` vs `## Conflict flags`, `## Proposed disposition` vs `## Proposed page shape`, or omitted `## One-line` entirely when adding a "Duplicate verdict" section first). Each failure required orchestrator-side patching before aggregation could proceed.
**Implication:** Two options: (a) loosen the validator to accept canonical aliases — `Cross-references|Cross-ref candidates`, `Conflicts|Conflict flags`, `Proposed disposition|Proposed page shape`; or (b) tighten the subagent prompt template to explicitly emphasise the four required header names and refuse to add any pre-summary sections. (a) is the more forgiving / robust choice given subagent variability under parallel dispatch; (b) preserves the strictness signal. Either is a small change.
**Status:** open

### 2026-05-14 — Gamma-API capture tool implemented (resolves 2026-05-12 SPA-event gap)
**Scope:** kit
**Observation:** Implemented `tools/capture_polymarket_market.py` against the Gamma API (`gamma-api.polymarket.com/events?slug=<slug>`). Single HTTP call returns the full event tree including all sub-markets, with per-market resolution-rule text (the binding spec hidden in component 3 of Polymarket's rule grammar) directly accessible in the `description` field. Smoke-tested on `what-will-trump-say-during-bilateral-events-with-xi-jinping` — captured 33 sub-markets with full plural/possessive/compound/AI-exclusion rules, umaBond/umaReward, tick size, and current prices in one ~1KB JSON request.
**Implication:** Unblocks the per-market resolution-criteria gap that was blocking the wiki's lint rule and the mention-market modeling pipeline. Output goes to `raw/markets/<slug>/<YYYY-MM-DD>.md` per the source-type-notes convention. Promote via `/harvest` — this is a strict kit improvement (capture_url remains the right tool for category-landing pages; this is for per-event detail). Companion: the prior `capture_url` patches (networkidle / script-strip) and the Cloudflare-interstitial bot-wall heuristic gap still apply to other contexts and remain open.
**Status:** applied (kit addition; awaiting `/harvest`)

### 2026-05-14 — umaBond = $500 (not $750) on live mention markets — wiki conflict
**Scope:** project
**Observation:** Live Gamma API on `what-will-trump-say-during-bilateral-events-with-xi-jinping` shows every sub-market's `umaBond = "500"` and `umaReward = "5"`. The wiki's [[uma-optimistic-oracle]] documents "$750 pUSD" bond (from the Polymarket Help Center capture 2026-05-13). The FIFA World Cup market (a high-volume non-mention market) also shows $500 — so the discrepancy isn't mention-market specific. Either (a) the help docs are stale; (b) $750 is for *disputer* bonds while $500 is the proposer bond; (c) different bond tiers exist that the help docs simplify. Currently unresolved.
**Implication:** [[uma-optimistic-oracle]] should be updated to reflect the live API data ($500 proposer bond, $5 reward), with a note that the help-doc $750 figure may apply to disputes or be stale. The bond-economics "net gain ~$375" math in that page (½ of opponent's bond) becomes ~$250 at $500 bonds — also need updating. Worth a follow-up capture of a *resolved* disputed market to see what the dispute-side bond actually was.
**Status:** open

### 2026-05-14 — Polymarket tick size varies per market (0.001 vs 0.01), not the documented $0.0001
**Scope:** project
**Observation:** Live Gamma API shows `orderPriceMinTickSize` as 0.01 on central-probability sub-markets (e.g., Taiwan/Tibet at 31.5%) and 0.001 on tail-probability sub-markets (e.g., Autopen at 3.75%). The wiki [[platform-comparison-kalshi-polymarket]] cites Falcon X claiming Polymarket tick = $0.0001 (4-decimal). The actual API ranges 0.01 to 0.001 (2- to 3-decimal). Either Falcon X was wrong, or $0.0001 is only available on specific markets (a per-market field after all), or the field changed since Jan 2026.
**Implication:** [[platform-comparison-kalshi-polymarket]] tick-size claim needs revision to "0.001–0.01 typical, with finer ticks (0.001) on low-probability markets where price has more room to move in absolute terms". The "tighter spread vs Kalshi $0.01" claim partially holds — Polymarket's tail markets use 0.001 vs Kalshi's flat 0.01.
**Status:** open

### 2026-05-12 — capture_url fails on Polymarket SPA event pages even after networkidle/script-strip patches
**Scope:** kit
**Observation:** With the prior two `capture_url` patches applied (`domcontentloaded` 60s + opportunistic `networkidle` settle + BS4 script-strip), captures of Polymarket *docs* pages (`docs.polymarket.com/...`) and a Polymarket *category landing* page (`polymarket.com/culture/mention-markets`) work cleanly. But captures of two specific *event* pages — `polymarket.com/event/what-will-powell-say-during-may-press-conference` and `polymarket.com/event/what-will-trump-say-in-next-speech` — fail with `Page.goto: Timeout 60000ms exceeded` waiting on `domcontentloaded`. The shallower URLs in the same domain succeed; deeper event URLs do not. Likely cause: event pages embed live order-book streams / WebSocket subscriptions / heavy SPA hydration that prevents the initial DOM parse from completing within 60 s. May also be region/geo-block specific; not yet diagnosed.
**Implication:** For per-market data (resolution-criteria text, current odds, dispute history), `capture_url` is not currently a reliable path on Polymarket event URLs. Two cleaner options worth exploring:
  1. **Gamma API JSON fallback.** Polymarket's documented Gamma API (`https://gamma-api.polymarket.com/events?slug=<slug>`) returns structured JSON including the resolution criteria text directly. A small `tools/capture_polymarket_market.py` that hits Gamma, formats the JSON into the kit's markdown+frontmatter convention, and writes to `raw/markets/<slug>/<date>.md` would be the right primitive. This also matches the wiki's stated dated-snapshot convention from the source-type-notes slot.
  2. **Increase `capture_url` timeout + use `wait_until="commit"`** to fire on first byte and accept partial rendering. Less robust than the API path but generic.
Both worth doing eventually. (1) is the right answer for this wiki since it directly serves the lint check that every market page must link its resolution criteria. Promote via `/harvest` once written.
**Status:** open

### 2026-05-11 — marker engine risky when host GPU is busy
**Scope:** project
**Observation:** Default `capture_pdf` engine is `marker` (which uses CUDA/torch). On this workstation, a long-running training job (`train_experiment_a.py`) holds the GPU during normal working sessions, and the host has documented progressive VRAM degradation (`~/.claude/CLAUDE.md`). Running marker concurrently risks CUDA OOM and the documented degradation crash signatures, which would then need GPU recovery (`nvidia-smi -r`) and re-apply of safe-mode caps.
**Implication:** For this wiki's `/research` runs while training is active, default to `--engine pymupdf` and accept lower figure fidelity. Re-capture critical papers with marker only when the GPU is free (e.g., between training rounds). Worth noting in this wiki's CLAUDE.md if it becomes a recurring pattern, but for now leaving as an interaction-time judgement call.
**Status:** open
