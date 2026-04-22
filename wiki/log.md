# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-04-21] bootstrap | collective consumer counter-power

Initial bootstrap. Schema and commands tailored for collective consumer counter-power. Ready to receive first source.

## [2026-04-21] research+ingest | dynamic-pricing-landscape

First content run. Topic: industries using dynamic / algorithmic / surveillance pricing and how they deploy it.

**Sources captured (8):** FTC Issue Spotlight (surveillance pricing 6(b) study); FTC Research Summaries (6(b) redacted); DOJ RealPage press release; ProPublica on DOJ/RealPage settlement; NBER working paper on algorithmic pricing; HBS working paper 22-050 on algorithmic pricing consumer harm; arXiv 2504.16592 on algorithmic collusion; Wikipedia dynamic-pricing article. All under `raw/research/dynamic-pricing-landscape/`.

**Capture audit:** clean except 2 broken image refs in `08-arxiv-algorithmic-collusion.md` (pymupdf fallback — no figure extraction; text intact). No mitigation needed; figures are not load-bearing for the claims cited.

**Wiki pages created (6):**
- `dynamic-pricing-overview.md` — hub / term disambiguation.
- `industries/rental-housing-algorithmic-pricing.md` — RealPage case study.
- `industries/surveillance-pricing-retail.md` — FTC 6(b) findings.
- `industries/consumer-facing-dynamic-pricing.md` — classic consumer industries.
- `mechanisms/algorithmic-collusion.md` — theory and evidence.
- `counter-power/regulatory-responses.md` — consolidated counter-power landscape with emphasised design-input candidates.

**Design-input section** added to each page (editorial, clearly labelled) per user request — emphasised on `regulatory-responses.md` given the user's focus on tools to build.

**Open questions surfaced during research** (none required user ruling at ingest time — all sources complementary rather than contradictory):
- HBS "non-collusive asymmetric-frequency harm" is a *stronger* theoretical claim than the DOJ's explicit-coordination framing. Both are documented on the relevant pages without implying one supersedes the other.

**Kit-level findings logged to `master_notes.md`:**
1. `capture_pdf.py` missing User-Agent header (403 on ftc.gov via Akamai).
2. `capture_url.py` mishandles protocol-relative URLs (Wikipedia thumbnails fail).
3. `capture_pdf.py --engine marker` has no graceful fallback on CUDA OOM.

All three tagged `Scope: kit`, `Status: open` — available to `/harvest`.

## [2026-04-21] lint | first lint run

Pre-harvest lint flow (report inline in chat; persisted-report behaviour and auto-ingest landed on `main` after this branch was created, arrives here on next `git merge origin/main`).

**Findings:** no orphans, no broken links, no conflicts, no format issues. 4 missing first-mention cross-references. 1 domain-specific convention question on source-metadata pointer pattern.

**Fixes applied:**
- Added first-mention `[[dynamic-pricing-overview|...]]` links on `surveillance-pricing-retail.md`, `consumer-facing-dynamic-pricing.md`, `rental-housing-algorithmic-pricing.md`, `algorithmic-collusion.md`.
- Amended domain lint check 10a in `.claude/commands/lint.md` DOMAIN-SLOT to explicitly allow the metadata-by-pointer pattern (full metadata on canonical page; other pages cite with a short pointer and explicit disclaimer).

**Deferred:**
- Creating mechanism pages (collective-bargaining, co-op, class-action, regulation, exit-alternative, transparency-tool, boycott, tech-workaround) — appropriate as a targeted research job, not a lint-fix stub. The wiki's "no synthesised knowledge" rule precludes empty definitional stubs.
- Re-capturing primary sources for 2 Wikipedia-chained claims (Delta 3%→20% expansion; 74% cost-plus figure) — low priority.

**Known issues left open:**
- 2 broken image refs in `08-arxiv-algorithmic-collusion.md` (pymupdf fallback after marker CUDA OOM). Figures not cited on any wiki page.

## [2026-04-21] research+ingest | platform-cooperatives

Priority-1 run from `wiki/research-queue.md`. Topic: platform cooperatives as an exit-pathway counter-power mechanism.

**Sources captured (8):** Trebor Scholz 2016 Rosa Luxemburg Stiftung NYC pamphlet (foundational text); OECD 2023 "Empowering Communities with Platform Cooperatives" policy report; Wikipedia platform-cooperative article; Wikipedia Mondragon Corporation article; Platform Cooperativism Consortium About page (thin, JS-rendered); Grassroots Economic Organizing excerpt on Drivers Cooperative; The Drivers Cooperative homepage; Shareable "11 Platform Cooperatives" list. All under `raw/research/platform-cooperatives/`.

**Capture notes:**
- Fast Company article bot-walled by Datadome captcha — substituted GEO repost (partial quote).
- Wiley pdfdirect URL 403'd even with browser UA — substituted Shareable list for case-study breadth.
- Both substitutions logged to `master_notes.md` as kit-level note on bot-walled-host detection.
- 4 broken image refs in OECD PDF (pymupdf fallback). Figures not cited on any wiki page; acceptable.

**Wiki pages created (4):**
- `mechanisms/platform-cooperatives.md` — anchor page; definition, Scholz origin, OECD typology, capital-conundrum debate (Srnicek/Morozov vs Sundararajan), federation pattern, legal vehicles.
- `organizations/drivers-cooperative.md` — NYC driver-owned rideshare; 15% commission vs Uber/Lyft 25–40%; Forman/Lewis/Orlando founding team.
- `organizations/mondragon.md` — the pre-digital foundational federation; 70K workers, 10 principles, 3:1–9:1 wage-ratio cap, 10% solidarity fund, Fagor 2013 bankruptcy and 2022 ULMA/Orona exits as stress-test evidence.
- `organizations/coopcycle.md` — OECD's featured federation case; 72 coops in 12 countries; second-level cooperative pattern as the transferable scaling blueprint.

**Pages updated (2):**
- `counter-power/regulatory-responses.md` — new section 8 "Exit-alternative — platform cooperatives"; previous section 8 renumbered to 9; gap analysis updated with platform-coops as "exists but weak"; design-input #2 (buyer-side data co-op) extended with MIDATA.coop and CoopCycle precedents.
- `dynamic-pricing-overview.md` — added orthogonal-framing note that platform-coops sit outside the dynamic-pricing debate as an ownership alternative.

**Deferred from the queue's anticipated output:**
- `mechanisms/exit-alternative.md` — captured sources frame "exit" through platform-cooperatives specifically rather than as a distinct standalone concept. Better deferred to a future research run.
- Stocksy and other Shareable-list co-ops — thin sourcing (only Wikipedia + Shareable). Deferred to avoid empty stubs.

**Open design-input candidates surfaced:**
- Consumer data cooperative for pricing-surveillance data (MIDATA.coop model applied to the personalised-pricing problem).
- Federation-first architecture for any new consumer-side counter-power tool (CoopCycle pattern).
- Colorado LCA as the practical US legal vehicle for investor-member cooperatives.

**Substantive tension documented (not resolved):**
- Scholz vs Morozov/Srnicek on platform-coop viability. OECD 2023 takes a middle position. Both framings preserved on `mechanisms/platform-cooperatives.md`.

**Kit-level findings logged to `master_notes.md`:**
- Fast Company (Datadome captcha) and Wiley Online Library (pdfdirect 403 even with UA) are now listed as bot-walled hosts; research.md could gain a detection hint for common captcha-wall signatures.
