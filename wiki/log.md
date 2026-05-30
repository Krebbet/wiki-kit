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

## [2026-04-21] research+ingest | consumer-data-pooling

Priority-1 run from `wiki/research-queue.md`. Topic: consumer data pooling and buyer-side tools.

**Sources captured (8):** Ada Lovelace Institute 2021 legal-mechanisms report (pymupdf fallback after marker GPU OOM); arXiv 2504.10058 data-cooperatives governance survey (Mendonça et al., pymupdf); Hardjono & Pentland 2017 OPAL paper arXiv 1705.10880 (marker); MIDATA cooperative primary page; Rockefeller Foundation grantee story on Driver's Seat; OpenTSS project methodology page (with --js to bypass Cloudflare challenge); arXiv 2506.10272 collective bargaining in information economy (Vincent, Prewitt & Li, pymupdf); Porat NYU/Harvard bargaining-with-algorithms paper (pymupdf). All under `raw/research/consumer-data-pooling/`.

**Capture notes:**
- MIT Press "wip" (work-in-progress / manifold) site bot-walled by Cloudflare even with `--js`. Substituted Pentland's MIT Press chapter with the canonical Hardjono & Pentland OPAL arXiv paper (1705.10880), which is the technical-framework source the MIT Press chapter builds on.
- Driver's Seat homepage (driversseat.co) returned a Squarespace "account expired" page — the organisation appears to have sunset. Substituted with the Rockefeller Foundation grantee-impact story as the authoritative account. Noted on the new org page as a finding about the state of the sector, not just a capture problem.
- OpenTSS required `--js` to bypass Cloudflare's standard challenge.
- GPU contention forced pymupdf fallback for 3 of the 4 papers — text intact, image extraction broken (33 broken image refs in fidelity audit; none are load-bearing for wiki claims).
- Parallel Bash batch cancels the whole batch on first error — noting as a kit-level friction for research workflows that capture multiple sources in parallel.

**Wiki pages created (5):**
- `mechanisms/data-cooperatives.md` — anchor mechanism page. Ada Lovelace 2021 + Mendonça et al. 2025 synthesis; definition/distinctions table (coop vs union vs trust vs commons); four-framework model (governance/operational/technical/social); uptake and scale challenges; live cases including MIDATA, Driver's Seat, Salus Coop, JoinData, and the dissolved Good Data (UK).
- `mechanisms/collective-bargaining-for-data.md` — bargaining-lane page. CBI proposal from Vincent, Prewitt & Li (arXiv 2506.10272, 2025) + Porat 2024 Harvard/NYU experimental findings on consumer algorithmic bargaining. Comparison table for the two framings; editorial open-questions block.
- `organizations/midata.md` — Swiss health-data coop, founded 2015. Open MIDATA Server (GPLv3); federation model; ETH Zurich + Bern University.
- `organizations/drivers-seat-cooperative.md` — US data coop for gig workers (2019–). LCA form; 13% reported income uplift; 5M trips tracked; noted sunset and migration to Princeton's Workers' Algorithm Observatory. Distinct from [[drivers-cooperative]] — cross-linked to avoid confusion.
- `tools/open-tenant-screening.md` — MIT researchers' OpenTSS project. Crowdsourced tenant-screening audit. Links directly to [[rental-housing-algorithmic-pricing]] as the tenant-side counter to RealPage.

**Pages updated (3):**
- `counter-power/regulatory-responses.md` — new section 9 "Consumer-side data pooling and collective bargaining"; previous section 9 (academic remedies) renumbered to 10. "Missing" synthesis updated: collective-bargaining-gap bullet refined to reflect partial presence via data coops. Design-input #2 (buyer-side data co-op) rewritten with references to [[data-cooperatives]], [[collective-bargaining-for-data]], [[midata]], [[drivers-seat-cooperative]], [[coopcycle]], [[open-tenant-screening]], and the Ada Lovelace challenge-framework. Source list and Related list extended.
- `industries/rental-housing-algorithmic-pricing.md` — design-input "tenant data co-op" bullet extended with [[open-tenant-screening]] as the closest existing instance and references to [[data-cooperatives]] / [[collective-bargaining-for-data]] as the structural shells. Related list extended.
- `wiki/index.md` — 5 new page entries added to the table.

**Deferred from queue's anticipated output:**
- `tools/consumer-data-pooling.md` — replaced by the more substantive `mechanisms/data-cooperatives.md` anchor + `tools/open-tenant-screening.md` (a concrete proto-instance) combination, which better fits captured sources.
- `mechanisms/tech-workaround.md` — split between coverage on [[data-cooperatives]] (infrastructural) and [[collective-bargaining-for-data]] (Porat's individual-level tactic). A standalone tech-workaround mechanism page would be redundant with these; defer unless future research runs surface distinct tech-workaround patterns (e.g., ad-blockers, privacy browsers, burner cards).
- Salus Coop standalone org page — referenced in [[data-cooperatives]] but no dedicated capture; defer.
- JoinData standalone page — same reason; defer.
- Pentland MIT Press chapter — MIT Press wip site bot-walled; substituted with Hardjono & Pentland arXiv as the primary source.

**Substantive tensions documented (not resolved):**
- **Data-coop sustainability** — Ada Lovelace 2021 flags financial sustainability as a structural challenge; Mendonça et al. 2025 position data coops optimistically. The Good Data (UK) and Driver's Seat (US) both illustrate the sustainability risk in live cases. Both framings preserved on [[data-cooperatives]].
- **Antitrust asymmetry** — Vincent et al. (arXiv 2506.10272) propose safe-harbour / Parker Immunity tooling for CBI-style intermediaries, while the DOJ's [[rental-housing-algorithmic-pricing|RealPage action]] treats seller-side data pooling as a per-se Sherman Act violation. Whether buyer-side data pooling would receive symmetric treatment is an open legal question flagged on [[collective-bargaining-for-data]].

**Open design-input candidates surfaced:**
- Tenant pricing data coop combining OpenTSS-style crowdsourced collection, MIDATA-style open-source platform, Colorado LCA legal form, and CBI-style bargaining mandate.
- Consumer algorithmic-price-bargaining tool — automates the Porat 2024 strategic-abstention + cookie/erasure-exercise pattern at per-session granularity.

**Kit-level findings logged to `master_notes.md`:**
- **Parallel-Bash batch cancellation.** When one of N parallel Bash captures errors out, the whole batch is cancelled — uncompleted captures must be re-run individually. Friction for `/research` workflows that capture 5–8 sources at once. Research.md could note this or the harness could offer a "best-effort parallel" mode.
- **driversseat.co is dead** — the canonical Driver's Seat homepage is now a Squarespace "account expired" page. Any wiki kit-template research queue referencing driver-owned data coops should triangulate from the Rockefeller grantee story or Ada Lovelace 2021 report rather than the primary org URL. Logging as a domain-specific note, not a kit fix.

## [2026-04-22] research+ingest | price-transparency-tools

Priority-2 run from `wiki/research-queue.md`. Topic: price transparency tools and personalised-pricing detectors.

**Sources captured (7):** Hannak et al. 2014 Northeastern IMC paper on measuring price discrimination and steering (captured via mislove.org mirror after the personalization.ccs.neu.edu primary timed out; pymupdf engine); Keepa Chrome Web Store listing; Keepa Firefox add-on listing; Wikipedia PayPal Honey article; Mozilla shutdown announcement (captured as redirect target of fakespot.com/faq); The Markup Citizen Browser project page; The Markup *How We Built a Facebook Inspector* methodology piece. All under `raw/research/price-transparency-tools/`.

**Capture notes:**
- **OECD 2018 *Personalised Pricing in the Digital Era*** (both one.oecd.org and www.oecd.org URLs) returned 403 even with the browser UA. Dropped from the shortlist — Hannak et al. 2014 carries the academic anchor load. Logged as a new kit-level note (OECD added to known-bot-walled-hosts).
- **keepa.com and camelcamelcamel.com** both timed out on Playwright's `networkidle` wait (30s). Substituted with Chrome Web Store and Firefox add-on listings for Keepa; dropped CamelCamelCamel entirely. Logged as a kit-level note — networkidle is unreachable on many ad-heavy consumer sites.
- **fakespot.com/faq** redirected to Mozilla's shutdown blog post — unexpectedly *more* useful than the original FAQ would have been, since it confirms the July 2025 Fakespot shutdown with Mozilla's own framing. Kept the capture as the primary source for the sunset claim.
- **Hannak IMC PDF** timed out on the canonical `personalization.ccs.neu.edu` URL; captured via the `mislove.org` mirror. Text-complete; only 2 broken image refs (not load-bearing).
- No GPU OOM this run (only one marker PDF attempted; rest pymupdf).

**Wiki pages created (5):**
- `mechanisms/transparency-tools.md` — anchor mechanism page. Taxonomy (price-history trackers / review-authenticity / crowdsourced observatory). Hannak et al. 2014 methodology in depth. Commercial and failure-mode patterns. Comparison table vs other mechanisms (data coops, platform coops, CBI, regulatory).
- `tools/keepa.md` — Keepa primary-source page. 4M Chrome users, 6B+ products, 11 Amazon locales, Keepa GmbH Germany. Permissions, privacy disclosures, structural limits (Amazon-only, no personalisation detection).
- `tools/paypal-honey.md` — full chronology of the Honey controversy 2012–2026 (founding → $4B PayPal acquisition → MegaLag exposé Dec 2024 → class actions → Chrome Web Store policy change March 2025 → 8M user loss → Rakuten removal + PayPal evasion-code admission Jan 2026). Three alleged mechanisms: cookie stuffing, merchant-controlled coupon visibility, affiliate-network evasion code. Framed as the extractive-drift failure mode for transparency tools.
- `tools/fakespot.md` — review-authenticity tool, Mozilla-acquired 2023, shut down July 2025. Framed as the acquisition-and-sunset failure mode. Capture thin (FAQ redirect); page acknowledges the trust limit.
- `tools/markup-citizen-browser.md` — The Markup's crowdsourced algorithmic audit. Standalone desktop app, 1,000+ paid panelists, Trail of Bits-audited redaction pipeline, NYT/SZ co-reporting. Positioned as the closest live template for a pricing observatory (design-input #1).

**Pages updated (2):**
- `counter-power/regulatory-responses.md` — section 9 transparency-tools sub-section rewritten with the three sub-categories (single-seller price trackers, crowdsourced audit, academic methodology) and the two failure modes (extractive drift, acquisition-and-sunset). Design-input #1 (consumer-side pricing observatory) extended with Hannak (methodology template), Markup Citizen Browser (operational template), OpenTSS (adjacent-domain precedent), and the two failure modes to budget for. Source list extended; Related list extended.
- `wiki/index.md` — 5 new entries added.

**Deferred from queue's anticipated output:**
- `mechanisms/transparency-tool.md` — renamed to `mechanisms/transparency-tools.md` (plural); serves the same anchor role.
- OECD 2018 standalone treatment — dropped because of 403 bot-wall; academic anchor carried by Hannak.
- CamelCamelCamel standalone page — dropped because of networkidle timeout; referenced on [[keepa]] page as context only.
- Detailed Hannak standalone page under `wiki/research/` — folded into `transparency-tools.md` instead; wiki/research/ directory remains empty (no new convention introduced).

**Substantive tensions documented (not resolved):**
- **"Transparency tool" as regulatory panacea vs as extractive vehicle.** The FTC's 6(b) framing (see [[surveillance-pricing-retail]]) treats transparency as the main regulatory lever; the Honey case shows transparency-tool deployment without governance safeguards doesn't automatically produce consumer benefit. Both framings preserved; tension flagged on [[paypal-honey]] and [[transparency-tools]].
- **Methodology opacity in transparency tools.** Fakespot did not disclose its detection algorithm (per WebSearch preamble); OpenTSS flags tenant-screening "tenant score" opacity as anti-pattern. An opaque-methodology transparency tool reproduces the asymmetry it claims to correct, for a different audience. Flagged on [[fakespot]] as editorial observation.

**Open design-input candidates surfaced:**
- "Hannak at scale, continuously" — the direct architectural target for design-input #1; Hannak's 2014 methodology plus The Markup's 2020+ panel/redactor architecture plus OpenTSS's crowdsourced pipeline would constitute the stack.
- Chrome-Web-Store-policy-tracking tool — the March 2025 affiliate-commission policy change in response to Honey is one data point; tracking platform-policy changes that affect consumer counter-power tooling would be a lightweight design.

**Kit-level findings logged to `master_notes.md`:**
- **OECD document server bot-walls capture.** `one.oecd.org` and `www.oecd.org/officialdocuments` both return 403 to the browser UA. Add to known bot-walled-hosts list in `research.md`.
- **Playwright `networkidle` unreachable on ad-heavy sites.** Keepa.com and camelcamelcamel.com both failed the default `networkidle` wait in `capture_url.py --js` within 30s. These are real target sites for this wiki's domain (commercial consumer tools). Consider: (a) add a `--wait-until` / `--wait-timeout` CLI flag to `capture_url.py` so the caller can downgrade to `domcontentloaded` or `load`; (b) default to `domcontentloaded` with a longer total timeout for consumer commercial sites; (c) document the issue in `research.md` with a workaround list.
- **Defunct/redirected primary sources can be load-bearing.** The `fakespot.com/faq` → Mozilla-shutdown-announcement redirect produced *better* source material than the original FAQ would have. Keeping a redirect is correct behaviour; flagging here as a reminder that size-check and bot-wall-check alone can miss "fortuitous redirects" that are actually valuable. No kit change needed — working as intended.

## [2026-04-22] research+ingest | collective-bargaining-group-purchasing

Priority-3 run from `wiki/research-queue.md`. Topic: consumer collective bargaining and group purchasing.

**Sources captured (7):** Wikipedia Consumers' co-operative (Rochdale history); Wikipedia Group purchasing organization (GPO primer, healthcare Safe Harbor history); Wikipedia Group buying (Tuángòu / Pinduoduo / Groupon / Mercata); Wikipedia Park Slope Food Coop; Wikipedia REI; Wikipedia Community Choice Aggregation; Blair & Durrance 2013 *Group Purchasing Organizations, Monopsony, and Antitrust Policy* (Managerial and Decision Economics) hosted on HSCA, pymupdf engine. All under `raw/research/collective-bargaining-group-purchasing/`.

**Capture notes:**
- **GAO-12-399R PDF** (www.gao.gov/assets/gao-12-399r.pdf) returned 403; the GAO landing page (/products/gao-12-399r) returned "Access Denied" (247 chars). `www.gao.gov` is fully bot-walled for capture scripts. Logged as a new kit-level note.
- **Two Wikipedia captures** (Consumers' co-operative, Community Choice Aggregation) hit 429 "Too Many Requests" from upload.wikimedia.org for image thumbnails. Markdown text captured cleanly in both cases; images were not load-bearing for the wiki pages.
- Fidelity audit returned 0 issues — cleanest capture batch so far.

**Wiki pages created (4):**
- `mechanisms/consumer-collective-bargaining.md` — anchor mechanism page. Four-mechanism taxonomy: GPOs, consumer coops, transactional group-buying, public-agency aggregation. Full healthcare-GPO scale data (90% of hospital purchases, 1986 Safe Harbor, 2002 GAO finding, admin-fee cap, Vizient/Premier/HealthTrust concentration). Blair & Durrance procompetitive vs Elhauge exclusionary debate. Rochdale 1844 lineage. Comparison table vs other wiki mechanisms.
- `mechanisms/community-choice-aggregation.md` — dedicated page for the US electricity-sector public-agency aggregation construct. 9 states, 1,850+ municipalities, 15% of Americans. Massachusetts (Cape Light Compact 1997), Ohio (NOPEC 2000), California (2002+). UCLA Luskin Center 11 TWh voluntary renewable procurement figure. Under-replicated outside electricity.
- `organizations/park-slope-food-coop.md` — Brooklyn consumer coop, 1973–, 17K members (July 2025). Member-labour model (2h45m/6wks), 25% markup, long boycott history from anti-apartheid to 2024+ BDS debate.
- `organizations/rei.md` — 181-store US outdoor-recreation coop, 1938–. Jim Whittaker, Sally Jewell, #OptOutside Black Friday closure (2015–2022), 2022 dividend-to-store-credit rebranding as an instance of cooperative-drift at scale. Comparison table vs Park Slope.

**Pages updated (2):**
- `counter-power/regulatory-responses.md` — new section-9 sub-section on consumer collective bargaining and group purchasing (before the transparency-tools sub-section). Two new bullets added to "Missing" synthesis: GPO analogue for consumers against personalised pricing; public-agency aggregation under-exploited outside electricity. Source list extended; Related list extended.
- `wiki/index.md` — 4 new entries.

**Deferred from queue's anticipated output:**
- `mechanisms/collective-bargaining.md` — renamed to `consumer-collective-bargaining.md` to avoid collision with existing [[collective-bargaining-for-data]] and to clarify scope.
- GAO report standalone treatment — dropped because of bot-wall; Blair & Durrance (peer-reviewed academic economics, not industry advocacy) carries the analytic load plus Wikipedia GPO page carries the GAO findings via its footnote trail.
- Standalone page for Rochdale Society, specific CCAs (Cape Light Compact, NOPEC, Sonoma Clean Power), or Groupon — all folded into the anchor mechanism pages due to thin or secondary sourcing.

**Substantive tensions documented (not resolved):**
- **GPO procompetitive vs exclusionary.** Blair & Durrance (2013) vs Elhauge (2002, 2003). Both framings preserved on [[consumer-collective-bargaining]]. Wikipedia's GPO page also surfaces the consumer-advocacy critique (three GPOs manage procurement for 90% of medical equipment) — the concentration-within-the-intermediary-layer concern.
- **Cooperative drift at scale.** REI's 2022 dividend-to-store-credit rebranding vs Park Slope's 5-decade stability of the member-labour model. Both framings preserved; flagged editorially on [[rei]] as an instance of the generic pattern Ada Lovelace 2021 warned about on [[data-cooperatives]].
- **Tuángòu-WeChat vs Groupon-US model viability.** Pinduoduo succeeded in China; Groupon collapsed in the US. Framing is that transactional group-buying works better when embedded in a standing social network than when sold standalone; the sourcing is WebSearch-preamble-only, treated as lower-trust editorial synthesis.

**Open design-input candidates surfaced:**
- **CCA-for-other-sectors policy gap.** Opt-out default aggregation under public-agency governance is authorised only for electricity, in 9 US states. No comparable rule for broadband, insurance, pharmaceuticals, or data-privacy. Highest-leverage policy gap surfaced in this run.
- **Cooperative-intermediary alternative to GPO admin-fee model.** A GPO owned by its member hospitals (rather than funded via supplier admin fees) would close the incentive-incompatibility critique. Captured sources do not document live examples; noted as an open design-input area.

**Kit-level findings logged to `master_notes.md`:**
- **GAO.gov bot-walls captures.** Both `/assets/*.pdf` and `/products/*` URLs return 403 / "Access Denied" to browser UA. Add to known-bot-walled-hosts list.
- **Wikipedia Commons image 429 rate-limiting.** `upload.wikimedia.org` regularly returns 429 Too Many Requests on thumbnail fetches. Markdown text captures succeed; image extraction partially fails. Cross-run pattern — consider polite-retry-with-backoff or image-skip flag in `capture_url.py`.

## [2026-04-22] mandate-update + new-section | strategies/

User-initiated scope expansion. Wiki now operates in two layers — a **reference layer** (neutral, source-traceable; existing pages unchanged) and a new **strategy layer** (editorial / design-oriented). Mandate in `wiki/CLAUDE.md` updated from "answer queries against a neutral reference with secondary design-input" to "uncover strategies and determine technical solutions to implement."

**Pages created (2):**
- `wiki/strategies/index.md` — section landing page. Working conventions for the strategy layer (claims cite reference layer or are marked *(editorial)*; one concept per page; research-needed flags are first-class; revisit cadence).
- `wiki/strategies/possible-strategic-levers.md` — first page of the strategy section. Inventory of **29 strategic levers across 8 categories** (aggregation, collective redirection, profile/algorithm manipulation, account arbitrage, disintermediation, information layer, economic-structural, regulatory-proxy). Each lever has a summary-table row with (a) category, (b) reference-layer wiki anchor (or *(editorial)* if none), (c) possible tech solutions, (d) research-needed flag. Full descriptions below the table. 24 of 29 levers need further research before a development plan; 5 have sufficient reference-layer support to proceed. Triggered by prior user dialogue: earlier `/query` response surfaced only the wiki's neutral-observer counter-power catalogue; user pushed back with a sharper list of 5 offensive levers and asked for an assessment + generation. This page is the persisted result.

**Pages updated (3):**
- `wiki/CLAUDE.md` — goal paragraph and wiki-structure section rewritten to codify the two-layer (reference / strategy) split. Role definition changed: "uncover strategies and surface technical solutions" is now the primary job; "maintain the wiki" is the maintenance job underneath.
- `wiki/index.md` — restructured: strategy layer surfaced first (new "## Strategy layer" table with the 2 strategy pages), reference layer heading renamed to "## Reference layer — Overview" to clarify the split. Top-of-page summary rewritten to state the new mandate explicitly.
- `wiki/revisions.md` — three new rows (one for the query-time counter-weight-table addition, one for the mandate update, one for the strategies-section creation).

**Directory scaffolding added:**
- `wiki/strategies/` (new top-level section for editorial content)
- `wiki/strategies/development-plans/` (created but empty — landing for per-plan docs as they are developed)

**Structural-convention decisions codified:**
- Reference-layer content still requires captured-source traceability and *(editorial)* tags on any synthesis.
- Strategy-layer content cites reference-layer pages where possible; novel proposals must be explicitly tagged *(editorial)* / *(synthesis)* / *(design proposal)*.
- Strategy-layer content has lower source-bar than reference-layer but same wiki-link discipline.
- Revisit cadence for strategy pages: on major reference-layer updates (new research runs, material lint fixes), re-read and update or deprecate.

**Next steps queued (from the levers page's "Next-step development plan" section):**
- Plan A: flash-redirection observatory for rental housing (combines lever #12 + #15; targets RealPage-class coordination).
- Plan B: buyer-side data cooperative for personalised e-commerce (lever #1 implemented as a [[data-cooperatives|data coop]] with a [[collective-bargaining-for-data|CBI]] bargaining mandate).
- Plan C: pricing-transparency-overlay extension (lever #22; lowest-dependency build).
- Plan D: consumer-side CCA-port research (lever #29; research-first effort).

Each expanded plan will go in `wiki/strategies/development-plans/<plan-name>.md` with: target extraction pattern, reference-layer mechanism anchor, milestone structure, known unknowns, open dependencies. No plan is committed until the user selects one for expansion.

**No kit-level findings this entry** — pure content/convention change.

## [2026-04-22] research+ingest | lever-implementations

Cross-domain run on live / real-world implementations of the [[possible-strategic-levers|29 strategic levers]]. User explicitly permitted out-of-domain sources ("they don't necessarily need to be in the identified domains"). Topic slug: `lever-implementations`.

**Sources captured (11):** Wikipedia AdNauseam; Nightshade primary (UChicago SAND Lab); Glaze primary (same); Privacy Badger Wikipedia; Buycott Wikipedia; Goods Unite Us primary homepage; Open Food Network /software-platform/; TimeBanks.org /how-it-works; NOYB Wikipedia; AlgorithmWatch /en/what-we-do/; CalSavers employer help-center /enrollment.html. All under `raw/research/lever-implementations/`.

**Capture notes:**
- **Privacy Badger EFF page** (/pages/privacy-badger) was a 712-byte redirect stub pointing to privacybadger.org — re-captured via Wikipedia article instead (12KB, substantive).
- **AlgorithmWatch /en/ homepage** captured only a heading fragment (349 bytes) — re-captured via /en/what-we-do/ (7.7KB, substantive).
- **Nightshade** had 2 non-load-bearing broken image refs (team headshots on non-SAND-Lab domains) — text content intact.
- **Image-path collision** on one Wikipedia "Edit this at Wikidata" SVG between NOYB and Privacy Badger captures — Wikipedia artefact, not a content concern.
- All other captures clean per `audit_captures`.

**Wiki pages created (10):**
- `mechanisms/obfuscation.md` — anchor mechanism page. Helen Nissenbaum's 2015 *Obfuscation* as theoretical anchor. Two live variants: ad/tracking (AdNauseam, TrackMeNot) and AI-training (Nightshade, Glaze). Structural properties: asymmetric costs, no network dependency, robust to countermeasures, platform-enforcement friction. Cross-mechanism design lessons for pricing-obfuscation tools.
- `tools/adnauseam.md` — full case study including the Chrome Web Store Jan 2017 ban, the Google-marked-as-malware escalation, the MIT Tech Review 2021 efficacy test ($100 earned on test AdSense account), and ad-industry-executive reception.
- `tools/nightshade-glaze.md` — UChicago SAND Lab paired tools. Ben Zhao + Heather Zheng; IEEE S&P 2024 paper. Stated cost-asymmetry goal ("increase the cost of training on unlicensed data, such that licensing images from their creators becomes a viable alternative"). Explicit Glaze-vs-Nightshade individual-vs-collective distinction.
- `tools/privacy-badger.md` — EFF algorithmic tracker-learning browser extension. Distinction from ad-blockers (enforces on surveillance, not advertising). Template for a "learn-the-pattern-then-block" pricing-detection tool.
- `tools/boycott-apps.md` — Buycott + Goods Unite Us combined. UPC-barcode + parent-company lookup + campaign match; FEC-data political-alignment scoring; 7K companies and 2M users (Goods Unite Us); 600M+ barcode database (Buycott).
- `organizations/open-food-network.md` — open-source farmer marketplace, 1% of sales fee, multi-country federation, direct-payment flow. CoopCycle pattern applied to food supply. Transferable lesson: cooperative-technology can be multi-tenant and multi-topology without extracting.
- `mechanisms/time-banks-lets.md` — TimeBanks.org + hOurworld. 1 hour = 1 Time Dollar, $300–1,200/yr member savings. True disintermediation: transactions never priced in currency. Category-bound and community-scale-friction-bound.
- `organizations/noyb.md` — Vienna non-profit, 4,400+ members, Max Schrems. Schrems I + Schrems II (invalidated Privacy Shield 2020), €50M Google CNIL fine, €5M Spotify IMY fine, Austrian DSB 2022 Google Analytics decision. Live template for strategic-litigation consumer-union-with-war-chest model.
- `organizations/algorithmwatch.md` — Berlin/Zurich ADM-accountability nonprofit. 2016 Automated Decision-Making Manifesto. Research + fellowships + policy advocacy hybrid. No standing Citizen-Browser-style observatory (captured source gap — open opportunity).
- `mechanisms/auto-enrollment-opt-out.md` — OregonSaves (2017–) + CalSavers state auto-IRA mandate. 30-day opt-out, 5% default contribution, Roth IRA. Second working US precedent (alongside CCA) for opt-out default aggregation outside electricity — **corrects the earlier gap-analysis claim on [[community-choice-aggregation]] that "no comparable opt-out default exists outside electricity."**

**Pages updated (2):**
- `wiki/strategies/possible-strategic-levers.md` — new sub-section "Working real-world implementations (added 2026-04-22)" added after the count summary. Pointer table mapping 7 of the 29 levers to the newly-captured working-implementation pages.
- `wiki/index.md` — 10 new entries in the reference-layer catalogue.

**Capture substitutions / drops:**
- DoneGood (mentioned in search results) — dropped; WebSearch did not surface a current primary site.
- Consumer Reports standalone — dropped in favour of NOYB for the "strategic advocacy" template (NOYB is closer structurally to what lever #26 describes).
- TrackMeNot standalone — folded into AdNauseam treatment (same author team; same lineage).
- OregonSaves standalone — folded into the auto-enrollment-opt-out page; primary capture was CalSavers.

**Substantive reference-layer correction surfaced by this run:**
- [[community-choice-aggregation]] previously stated "No comparable opt-out default exists for broadband, insurance, pharmaceuticals, or data-privacy" — this is imprecise. Auto-IRAs (state programmes) are a live second US precedent for opt-out default aggregation outside electricity. The correct scope of the gap is narrower: no comparable default in those four named sectors specifically. The [[auto-enrollment-opt-out]] page documents the correction explicitly; flagging for a future `/lint` pass to update [[community-choice-aggregation]] itself.

**Open-question gap surfaced:**
- Complaint-for-inaction against regulators (NOYB's distinctive tactic against the Swedish IMY and Irish DPC) has no captured US equivalent pressure point. A pricing-side consumer-union analogue would need to identify the US-analogous procedural lever (FTC ombudsman? state-AG failure-to-enforce statute?) before replicating NOYB's playbook. Logged on [[noyb]] as an open research question.

**Kit-level findings logged to `master_notes.md`:** none this run. Wikipedia 429-rate-limiting pattern recurred but was already logged from a prior run.

## [2026-04-23] research+ingest | obfuscation-deep-dive

User-requested deep dive: "obfuscation is emerging as a legitimate lever… strengths and weaknesses, technical approaches, counter-measures that will likely be attempted."

**Sources shortlisted (11):** Brunton & Nissenbaum *Obfuscation* book PDF (riseup mirror); Yale LJ *Privacy's Trust Gap* (Richards & Hartzog); Peddinti & Saxena JCS 2014 TMN attack; Howe & Nissenbaum IWPE 2017 AdNauseam case study; Bó Chen Hakimov arXiv 2304.11415 strategic-response to personalized pricing; Bergemann "Surfing incognito" ScienceDirect; Solanki et al. arXiv 2505.05707 "Crowding Out The Noise" ACA-vs-DP; Wang et al. arXiv 2401.01527 poisoning-RS survey; Lawall arXiv 2411.12045 fingerprinting survey; Venugopalan et al. arXiv 2406.07647 FP-Inconsistent; White & Case 2022 hiQ/Van Buren CFAA memo.

**Sources captured (9):** all of the above except the *Obfuscation* book PDF (sandbox-denied — copyright concerns on third-party mirror) and Bergemann (ScienceDirect bot-walled — known from prior master-notes entry). 9 captures under `raw/research/obfuscation-deep-dive/`.

**Capture audit:** clean on paired-PDFs, thin-captures, and collisions. 45 broken image refs across the 8 arXiv PDFs — all pymupdf engine limitation (figures not extracted, text intact). Not load-bearing for any claim cited. Consistent with prior arxiv-capture runs on this wiki.

**Wiki pages created (3):**
- `mechanisms/adversarial-data-poisoning.md` — Wang et al. 2024 poisoning-attacks-on-RS taxonomy (three dimensions: Component-Specific, Goal-Driven, Capability-Probing) + Solanki et al. 2025 Algorithmic Collective Action formalism (feature-label strategy h(x,y) = (g(x), y*); Theorem 1 size-proportional success; Theorem 2 DP-noise degradation; empirical validation MNIST / CIFAR-10 / Bank Marketing; ACA-improves-MIA-empirical-privacy side finding).
- `mechanisms/browser-fingerprinting.md` — Lawall 2024 technique catalogue (Canvas / WebGL / Audio / Font / Screen / WebRTC / CSS / plugin enumeration / navigator) + entropy figures + countermeasures (Tor uniformity, Firefox / Brave / WebKit, CanvasBlocker, NoScript) + the "blending in" paradox. Venugopalan et al. 2024 FP-Inconsistent method (spatial + temporal cross-attribute inconsistency detection; 44.95–48.11% evasion-rate reduction at 96.84% TNR; iPhone-resolution example; Brave partial counterexample).
- `strategies/obfuscation-strategic-readout.md` — editorial strategy-layer synthesis directly answering the user's question. Structure: TL;DR (6 points) → Strengths (6 source-traceable) → Weaknesses (6 source-traceable) → Technical approaches (Tier 1 mature / Tier 2 formalised / Tier 3 speculative) → Countermeasures to expect (Tier 1 off-the-shelf / Tier 2 deliberate / Tier 3 structural including DP-as-firm-counter) → Readout recalibrations to lever-implementation-readout + possible-strategic-levers → Open strategic questions.

**Wiki pages updated (3):**
- `mechanisms/obfuscation.md` — major expansion. Added Strengths / Weaknesses / Technical Approaches / Countermeasures / Legal-risk-layer sections, each source-traceable. Cross-references to the two new mechanism pages and the strategy-layer readout. Source list expanded from 3 to 12 entries with origin / audience / purpose / trust metadata per line.
- `counter-power/regulatory-responses.md` — added §5a on CFAA post–Van Buren / hiQ doctrine. Cross-linked to `obfuscation.md` legal-risk layer for the strategic read.
- `strategies/possible-strategic-levers.md` — recalibrated research-needed flags on levers #3, #6, #7, #10, #11 with new reference-layer anchors. Lever #6 upgraded from "research needed" to "research-backed design constraint: joint-distribution-preserving rotation required." Lever #10 upgraded from "no wiki precedent" to "formalism exists; engineering gap + DP-counter risk." Working-implementations table extended with pointers to new pages. Count footer updated.

**Key user-answering findings:**
- **Obfuscation's live domain evidence is stronger than documented in April 22 readout, AND the weakness evidence is sharper.** The paradoxical combination: cost-asymmetry framing (Nightshade) works; naive rotation (TMN) is already defeated; the sophisticated approach (joint-distribution fingerprint spoofing, per-user decoy-seed diversification, feature-label ACA) is live research not deployed tools.
- **The single most important countermeasure for builders to internalise: Solanki et al. 2025's DP-as-firm-counter result.** A pricing operator training with DP protects individual privacy *and* blunts collective action. Expected to be adopted under regulatory pressure; no tool-level mitigation.
- **Richards & Hartzog's structural critique is the largest strategic risk.** Obfuscation deployed as primary frame reinforces individualistic-privacy trap; use as tactical auxiliary to collective-bargaining / data-coop / regulatory levers, not as main game.
- **Post-Van Buren / hiQ: public-endpoint automation is federally defensible; authenticated-endpoint automation remains materially risky.** Retailers may respond by moving personalisation behind login walls.
- **Bó et al. 2024's pricing-specific finding: users demand privacy LESS in opaque-context settings (24% optimal Movies vs 67% Risk).** Direct implication: obfuscation tools must default-on, not opt-in — Notice-and-consent is broken from the consumer side, not just the regulatory side.

**Open questions surfaced (none requiring user ruling at ingest; all logged on strategic-readout page):**
1. Build vs advocate — does the Richards/Hartzog critique argue the wiki's bandwidth is better spent on structural levers than tool-build?
2. How to handle DP-as-firm-counter politically? No tool-level mitigation; pre-emptive naming of "DP-trained pricing as ACA suppression" is the analogous move to RealPage's "revenue management software" framing pre-emption.
3. Is default-on realistic? Requires a distribution channel (Brave? Firefox?) that will carry it.
4. What is the negotiation endpoint? The wiki has not written down an answer.

**Kit-level findings logged to `master_notes.md`:** none new. Sandbox denial on third-party copyrighted book mirrors is expected behaviour (not a bug); ScienceDirect bot-wall was already known.

## [2026-04-23] research+ingest | seller-algorithm-taxonomy

User-requested second run of the day: "look at the different seller side algorithms for dynamic pricing and categorize the types of data they need to succeed. This will be used to determine if there are effective strategies to disrupt or manipulate that datastream while mitigating the risk of platform enforcement."

**Sources shortlisted (10):** MAB survey (ace.ewapub.com); Ban & Keskin 2020 canonical personalized-ML pricing (SSRN); Zhao Jiang Yu 2024 contextual bandit + LDP (arXiv 2406.02424); Safonov 2024 neural demand estimation (arXiv 2412.00920); Tanković & Šajina 2025 contextual bandits review + retail prototype (arXiv 2505.16918); GMU Revenue Management chapter; Williams 2018 airline pricing (Wharton marketing pdf mirror); Yale Thurman Arnold Project 2025 RealPage paper; PMC Uber surge Austin study; FTC Press Jan 2025 on 6(b) findings.

**Sources captured (6):** Zhao et al. 2024, Safonov 2024, Tanković & Šajina 2025, Yale TAP 2025, Williams 2018, *Not Even Nice Work If You Can Get It* (arXiv 2506.15278 — substitute for PMC Uber Austin after PMC reCAPTCHA bot-wall).

**Sources dropped (4):**
- Ban & Keskin 2020 (SSRN 403 bot-wall; INFORMS pdf also 403 bot-wall). Content overlapping with Zhao et al. Family 1 is comprehensive enough without it.
- GMU Revenue Management textbook chapter (SSL cert verify failure — kit finding already exists for SSL issues; not worth a new entry). Williams airline-pricing paper is a better empirical deployed-RM source anyway.
- FTC Jan 2025 press release. `ftc.gov/news-events/*` is bot-walled with FTC's own PWH-Alert@ftc.gov anti-scraping WAF (new variant; existing UA fix does not satisfy it). Tried `--js`; same 693-byte stub. **Kit finding logged to master_notes.** Primary FTC sources (Issue Spotlight PDF, Research Summaries PDF) from prior dynamic-pricing-landscape run are already captured and cover the same findings.
- PMC Uber surge Austin study. `pmc.ncbi.nlm.nih.gov` returns a Google reCAPTCHA challenge page. **Kit finding logged to master_notes** — NCBI/PMC is a high-value biomedical source lane. Substituted with arXiv 2506.15278 participatory Uber audit.

**Capture audit:** clean on paired-PDFs, thin-captures, and collisions. 34 broken image refs — same pymupdf engine limitation as prior runs; text intact.

**Session-specific cwd drift issue encountered.** My shell working directory had drifted to `wiki/` during the ingest, causing `poetry run python -m tools.capture_url --out raw/research/...` to write to `wiki/raw/research/...` on first attempt. Moved captures to correct location manually; no content loss. Flag for future attention: use absolute paths for `--out` when cwd may have drifted in a long session. (Not severe enough to be a kit finding — it's an operator-discipline issue, not a tool bug.)

**Stray empty files at wiki/ root surfaced** — `wiki/adnauseam.md` (0 bytes) and `wiki/lever-implementation-readout.md` (0 bytes). Likely Obsidian auto-creation on unresolved wiki-links (Obsidian is enabled in this vault — see `.obsidian/` in git status at session start). NOT created by me this session; I wrote to `tools/adnauseam.md` and `strategies/lever-implementation-readout.md` correctly. Flagging for user cleanup; risk is low since 0-byte.

**Wiki pages created (2):**
- `mechanisms/pricing-algorithm-taxonomy.md` — reference-layer anchor. Six algorithm families (GLM / contextual bandit, neural demand estimation, retail-offer bandit, airline stochastic DP, RealPage hub-and-spoke, Uber per-trip opaque) each with source-traceable data-input catalogue and structural-vulnerability notes. Plus six-category cross-family data-input catalogue (first-party operational, first-party consumer signals, pooled nonpublic peer data, third-party broker data, aggregate market signals, consumer response labels). Four cross-family themes.
- `strategies/data-disruption-strategy-map.md` — strategy-layer matrix directly answering the user's brief. Six-family × six-lever-class effectiveness grid. Six platform-enforcement risk tiers catalogue. Recommended strategy portfolio split Tier-1 build-now / Tier-2 build-with-care / Tier-3 long-game / Not-recommended. Five open strategic questions.

**Wiki pages updated (4):**
- `industries/rental-housing-algorithmic-pricing.md` — new "Algorithm and data-input detail (Yale TAP 2025)" subsection with joint-owner profit maximization quote, 11-million-property / 50K-monthly-calls surveillance-mechanism figures, market seasonality feature name, 90% auto-accept rate, and the TAP authors' explicit rejection of the data-moat framing in favour of the structural remedy.
- `industries/consumer-facing-dynamic-pricing.md` — new "Uber's Q1 2023 transition to per-trip dynamic pricing (UK)" subsection. Covers the pre/post-dynamic fare formula shift, pay table (£22.20→£19.06/hr, take-rate 25%→29%, surplus +38%, R² 0.85→−54, standby-time +1hr/week), CEO quote on per-driver point estimates, and methodology (258 drivers / 1.5M trips / DSAR).
- `dynamic-pricing-overview.md` — added pointers to the new taxonomy page and the strategy map under Coverage.
- `strategies/possible-strategic-levers.md` — added reference anchors for Category C (Profile / algorithm manipulation) pointing to pricing-algorithm-taxonomy and data-disruption-strategy-map. Added a critical structural correction: identity-based levers are ineffective against airline-RM and neural-retail families.

**Key user-answering findings:**
- **Not all dynamic pricing is surveillance pricing.** Williams's airline-RM model and Safonov's neural retail demand model both operate on *aggregate* signals with no per-user features. Identity-based obfuscation levers are structurally ineffective against them.
- **The critical data type varies per family** — GLM/bandit needs context vectors; neural-retail needs sales-history aggregates + on-shelf availability; airline-RM needs capacity + booking curve; RealPage needs pooled competitor data; Uber needs per-driver acceptance history. Disruption strategy must match.
- **The lowest-platform-enforcement-risk levers are already lawful:** coordinated consumer behaviour (L2) and DSAR/GDPR exercise (L3). The Uber audit is the existence-proof that 258 DSAR-contributing users can expose an algorithm's predictability collapse — higher information yield per user than obfuscation has ever delivered at comparable scale.
- **Post-Van Buren CFAA gives cover to public-endpoint automation but not authenticated-endpoint automation.** Airline pricing is authenticated; retail browsing is mostly public. This maps which sectors have lower legal risk for automation-based levers.
- **DP-as-firm-counter appears a second time from Zhao et al.'s pricing-specific derivation** — confirms the Solanki et al. finding. A pricing operator training under LDP protects individual privacy *and* suppresses consumer collective action by shrinking effective sample size by d/ε². Pre-emption this move politically before it's adopted.

**Open questions surfaced (carried into the strategy map):**
1. Minimum DSAR-submitter count for pricing-operator audits at comparable leverage to the Uber WIE audit.
2. Concrete Family-2 target selection — which specific retailer for a first Tier-1 build project. FTC 6(b) 8-vendor list is the starting point.
3. Timing-coordination commitment-device design (Kickstarter-style vs enforceable contract).
4. Whether a single tool can deliver both obfuscation and probe-and-publish given the conflict (obfuscate = confuse algorithm; probe = reveal algorithm).
5. The Family-5 (RealPage-class) problem: consumer-side disruption has nothing to offer; is there a wiki-sanctioned early-warning role for new RealPage-analogues across sectors?

**Kit-level findings logged to `master_notes.md`:** two new entries, both bot-wall additions.
1. `ftc.gov/news-events/*` bot-walls capture_url even with --js (FTC's own PWH-Alert@ftc.gov anti-scraping WAF; 693-byte stub; slips the existing bot-wall detector because format is non-Akamai/non-Cloudflare).
2. `pmc.ncbi.nlm.nih.gov` bot-walls capture_url with Google reCAPTCHA (~20KB of reCAPTCHA boilerplate JS, above 2KB threshold but content is worthless).

Both will be picked up by `/harvest`.

## [2026-04-23] lint | full pass

Persisted report: `wiki/lint-reports/2026-04-23.md`.

**Scope:** 46 non-empty wiki pages + 64 raw source captures across 8 topic directories. Full pass of the 10-check lint protocol including all domain-specific checks (10a–10e).

**Clean:** orphans, broken links, format compliance, un-ingested sources, thin captures, source metadata (10a), conceptual cross-links (10b).

**Flagged (all minor, none blocks normal operation):**
- **Coverage:** `surveillance-pricing-retail` counter-power thin (only `markup-citizen-browser` addresses it directly). Data-broker page absent.
- **Stale-tech (10e):** 4 pages — `markup-citizen-browser` (Jan 2021 sources), `algorithmwatch` (undated), `drivers-seat-cooperative` (2021/22), `open-food-network` (undated).
- **Claim attribution (10d):** 2 flags — `algorithmic-collusion` 28% margin cited via arXiv survey not primary JPE paper; `park-slope-food-coop` June 2025 vote percentages Wikipedia-only without footnote-trail annotation.
- **Industry ↔ counter-power (10c):** same as coverage — `surveillance-pricing-retail` thin.

**Capture fidelity:** 128 total issues = 127 pymupdf broken-image-refs (known engine limitation, text intact across captures) + 1 image-path collision (benign shared Wikimedia UI icon `assets/ac44065f938ab450.png` referenced by both `09-09-wikipedia-noyb.md` and `12-04-wikipedia-privacy-badger.md`).

**New noise category surfaced:** 6 stray 0-byte `.md` files at `wiki/` root — `2026-04-23.md`, `adnauseam.md`, `algorithmic-collusion.md`, `lever-implementation-readout.md`, `obfuscation-strategic-readout.md`, `possible-strategic-levers.md`. Canonical pages for each exist in correct subdirectories. Cause: Obsidian auto-creation on unresolved wiki-link clicks (vault has `.obsidian/` enabled). Safe to delete. Not detected by any existing lint check because the check's `find` filter used `! -empty`.

**Un-ingested raw sources:** none. All 64 captures cited on the wiki.

**Auto-ingest step skipped:** nothing to ingest.

**Kit-level finding logged to `master_notes.md`:** add a lint check for 0-byte wiki/*.md files as a distinct "stray / noise" category — generic to any Obsidian-enabled wiki-kit deployment.

**Fixes requested from user:** pending — presented the report and offered to fix claim-attribution flags, stale-tech refreshes, coverage-gap fills, and stray-stub deletion.

## [2026-04-23] weekly-brief | first run

First /weekly-brief run on this wiki, immediately after the setup interview that produced wiki/reference-sources.md and wiki/watchlist.md.

**Trend scan.** Dispatched 4 parallel subagents across the source-stream taxonomy: editorial primary (BIG/Pluralistic/The Markup/ProPublica/404 Media/Rest of World/Wired/Hell Gate/Platformer), enforcement (FTC/DOJ/state AGs/EU/CMA/CourtListener), research-think-tank (Ada Lovelace/Berkman/AlgorithmWatch/NoyB/FAccT), and movement (platform.coop/ICA/CoopCycle/Drivers Coop/Open Markets/Mozilla Foundation). Window: 2026-04-16 to 2026-04-23 (editorial / enforcement / movement) and ~3 weeks for research.

**Selection (5 captures).** Strongest cluster was state-AG-led enforcement against Live Nation/Ticketmaster + state-level legislation on personalised pricing. Selected:
1. NPR — Live Nation/Ticketmaster jury verdict (33 states + DC, Apr 15 2026)
2. Maryland HB0895 status page — Protection From Predatory Pricing Act (Apr 11 2026, effective Oct 1 2026)
3. Washington Times — DC AG $9.9M Live Nation settlement (Apr 21 2026, separate consumer-protection track)
4. OMI press release — Sen. Murphy's Fair Prices for Local Businesses Act (Robinson-Patman revival)
5. UK CMA blog — Direct Consumer Enforcement: One Year On (year-1 readout + AA Driving School £4.2M drip-pricing fine)

**Captures.** All 5 via tools.capture_url. Audit clean (0 issues). Maryland legislative page is structurally listy (legislative metadata) but text content extracted cleanly.

**Wiki updates.** No new pages — all 5 captures slotted into existing reference-layer pages:
- counter-power/regulatory-responses.md: 6 edits — new § 1 DOJ-Live-Nation subsection (March 2026 $280M settlement); new § 2 Fair Prices Act subsection; § 3 State AGs extension (Live Nation jury verdict + DC AG separate track); new § 3 Maryland HB0895 subsection; § 4 UK CMA Year-1 readout subsection; "What exists vs what is missing" line on state regimes refined to distinguish disclosure (NY) from prohibition (Maryland) regimes; Source list extended.
- industries/consumer-facing-dynamic-pricing.md: new "2026 Live Nation / Ticketmaster outcomes" subsection in Live events section (3 events, doctrinal-pattern callout).

**Watchlist overflow.** Appended 10 items: noyb 83.5% access-request failure rate; AlgorithmWatch Microsoft EU policy ghostwriting expose; Pluralistic surveillance-wage-discrimination piece; OMI "Fighting for Democracy Amid the AI Race"; OMI Brussels EC monopoly-agenda push; Drivers Cooperative Colorado scaling profile; Camden Property Trust $53M RealPage class settlement; EU TTBER revision (data-licensing framework); PCC 2026 "Solidarity AI" conference Bangkok Nov 12-15; Pluralistic Switzerland fiber structural-separation piece.

**Brief.** Watchlist-centric shape per skill template. 6 trend-bullets at top; 3 top-of-watchlist (Live Nation verdict + Maryland HB0895 + Murphy Fair Prices Act); other-watchlist-references organised by section header; conflicts opened: none this run; run notes with capture/wiki-page/watchlist counts and the uncommitted-changes summary.

**Delivery.** [pending — see brief send step.]

**Brief output paths.** /tmp/weekly-brief-2026-04-23.md and wiki/weekly-briefs/2026-04-23.md (both written before email send).

**Pre-existing uncommitted state at run start.** This wiki had substantial uncommitted work from earlier sessions (master_notes.md, several reference-layer pages, all the new mechanisms/organizations pages from the 2026-04-22 and 2026-04-23 research+ingest runs, lint-reports/, the merge-commit pull from main, and the just-written setup files). The weekly-brief diff is therefore mixed in with that backlog — flagged in the brief's run-notes section so the user can separate the two when committing.

## [2026-04-25] query | ClawNet paper applied to wiki

User `/query`: "take a look at the paper for an agentic method called clawnet. See how it could be applied in the context of this wiki."

**External source.** Yang, Zhang, Jia, Song, Xue, Zhang & Guo. 2026. *ClawNet: Human-Symbiotic Agent Network for Cross-User Autonomous Cooperation*. arXiv 2604.19211. HKUST / HKGAI / HKBU. Not captured as a raw source; arXiv URL is the primary external reference.

**Synthesis.** ClawNet is infrastructure (three governance primitives — identity binding, scoped authorization, action-level accountability), not a lever. It maps onto the multi-party-with-divergent-interests subset of the wiki's 29-lever inventory: Tier-1 #1 (DSAR coordination), levers #14 / #16 (commitment device — resolves [[data-disruption-strategy-map]] open Q#3), #1 (CBI agent representation), #4 (group-buy), #8 (probe-and-publish), #26 (consumer union). Architecturally incompatible with obfuscation / ACA cluster (#6 / #7 / #10 / #11) and adds nothing for Family 4 (airline RM) / Family 5 (RealPage) per [[pricing-algorithm-taxonomy]].

**Five deployment risks** catalogued: (1) centralised operator trust = Honey extractive-drift pattern, (2) CFAA risk class 3 (authenticated-endpoint automation), (3) adversarial-training inoculation against the substrate signature, (4) DP-as-firm-counter from Solanki et al. 2025 unchanged, (5) cross-user contact graph privacy not addressed by the paper.

**Net read.** A cooperatively-owned ClawNet-style substrate (orchestration governed under a [[platform-cooperatives|platform coop]] shell, not the original cloud-vendor configuration) could be the missing technical layer for the [[data-cooperatives]] / [[collective-bargaining-for-data]] / [[platform-cooperatives]] convergence — agent-mediated cross-consumer coordination as the substrate all three wiki-anchor mechanisms have separately needed but none has built.

**Wiki updates.**
- New strategy-layer page: `wiki/strategies/clawnet-readout.md`.
- Cross-references added: `possible-strategic-levers.md` (new "Cross-cutting infrastructure (added 2026-04-25)" subsection); `data-disruption-strategy-map.md` (§L3 substrate note + open question #3 partial-answer annotation).
- Index updates: `wiki/index.md`, `strategies/index.md`.
- Revision row appended.

**Surfacing for future work.** "Agent-mediated coordination" flagged as a candidate cross-cutting infrastructure pattern for the future strategy-layer pattern library subsection. If the synthesis grows into a development plan, the ClawNet paper itself warrants a formal `/ingest` capture into `raw/`.

## [2026-04-26] research+ingest | clawnet-adjacent-methods

User `/research`: scan for methods like ClawNet — agentic / algorithmic / DL / optimisation / network-graph approaches that relate to the wiki's core problems.

**Sources captured (14 PDFs + 12 abs):** in `raw/research/clawnet-adjacent-methods/`. Originally attempted with marker engine; GPU OOM on parallel runs; switched to pymupdf — clean text extraction (text intact, broken-image-refs in known-issue category per past lint runs). 12 arXiv abs pages via `capture_url`.

**Sources dropped (1):**
- E2 *Social Learning with Complex Contagion* (PNAS 2024, doi 10.1073/pnas.2414291121): 403 bot-walled on both PDF and HTML routes. Per user ruling, skipped — Centola E1 chapter covers the foundational network-science layer adequately.

**Sources captured by category:**
- **Algorithmic Collective Action lineage:** Hardt, Mazumdar, Mendler-Dünner & Zrnic 2023 (foundational, ICML, arXiv 2302.04262); Baumann & Mendler-Dünner 2024 (ACA in recsys, arXiv 2404.04269); Karan, Karahalios, Vincent & Sundaram 2025 (multi-collective dynamics, arXiv 2505.00195).
- **Strategic classification:** Hardt, Megiddo, Papadimitriou & Wootters 2016 (foundational, ITCS, arXiv 1506.06980); *Contextual Dynamic Pricing with Strategic Buyers* (arXiv 2307.04055); Milli, Miller, Dragan & Hardt 2019 (FAccT, arXiv 1808.08460).
- **Federated learning:** Rahman 2025 survey (arXiv 2504.17703).
- **Multi-agent LLM negotiation:** Liu, Gu & Song 2026 *AgenticPay* (arXiv 2602.06008); Abdelnabi et al. 2024 *LLM-Stakeholders Interactive Negotiation* (NeurIPS, arXiv 2309.17234); Louck, Stulman & Dvir 2025 *Improving A2A* (arXiv 2505.12490).
- **Network science:** Centola *Complex Contagions* book chapter.
- **Mechanism design:** OECD 2022 *Purchasing Power and Buyers' Cartels*; Agarwal, Dahleh & Sarkar 2019 *A Marketplace for Data* (EC, arXiv 1805.08125).
- **Decentralised identity:** Garzon et al. 2025 *AI Agents with Decentralized Identifiers and Verifiable Credentials* (arXiv 2511.02841).

**User rulings (2026-04-26):**
1. Keep [[adversarial-data-poisoning]] as legitimate-weapon framing; create new [[the-firms-view]] page collecting firm-side counter-perspectives; both link bidirectionally.
2. Reflect B2 (adaptive-pricing recovery) caveat in [[obfuscation-strategic-readout]] and [[the-firms-view]].
3. (My choice) B3 disparate-impact externality — add as new section in [[obfuscation-strategic-readout]] §7, full treatment in [[strategic-classification]] + [[the-firms-view]] §4, new risk class 8 in [[data-disruption-strategy-map]].
4. C1 (FL survey) — standalone [[federated-learning]] page with primary-citation pattern.
5. E2 PNAS — skipped (bot-walled).
6. (My choice) Antitrust treatment — handled as new "Antitrust treatment by lever" section on [[possible-strategic-levers]] + new [[buyer-cartels-antitrust]] mechanism page; not as new column on the summary table (cleaner separation).
7. (My choice) ClawNet readout expansion — three new sections (empirical capability evidence, substrate dependencies, centralised vs decentralised comparison) added in-place; no separate comparison page.

**Wiki pages created (10 mechanism-layer):** [[algorithmic-collective-action]], [[strategic-classification]], [[the-firms-view]], [[federated-learning]], [[complex-contagion]], [[buyer-cartels-antitrust]], [[data-market-mechanism-design]], [[decentralized-agent-identity]], [[agent-mediated-negotiation-empirics]], [[agent-interop-protocols]]. All under `wiki/mechanisms/`.

**Wiki pages updated:** [[adversarial-data-poisoning]] (intro + Related — keep legitimate-weapon framing per user ruling, add cross-links); [[obfuscation-strategic-readout]] (renumbered weaknesses §6 → §8; added §6 adaptive-seller caveat + §7 disparate-impact externality; Related additions); [[clawnet-readout]] (added "Empirical capability evidence" + "Substrate dependencies" + "Centralised vs decentralised — ClawNet vs DID/VC" sections; Related additions); [[possible-strategic-levers]] (expanded Cross-cutting infrastructure from 1-entry to 12-entry table; added Antitrust-treatment-by-lever section; per-lever upgrade notes); [[data-disruption-strategy-map]] (risk class 7 + 8 added; Related additions); [[pricing-algorithm-taxonomy]] / [[data-cooperatives]] / [[collective-bargaining-for-data]] / [[consumer-collective-bargaining]] (Related cross-links + antitrust section in consumer-collective-bargaining); [[index]] / [[strategies/index]] (catalog updates); revisions.md row appended.

**Open carry-overs:**
- DID/VC × ClawNet hybrid architecture — flagged on [[clawnet-readout]] + [[decentralized-agent-identity]] as future research-queue topic.
- Issuer-trust governance for DID/VC — unsolved problem flagged on [[decentralized-agent-identity]].
- FL primary-citation capture — McMahan 2017, Bonawitz 2017, Abadi 2016, Zhu 2019, Blanchard 2017 referenced via the Rahman 2025 survey but not yet in `raw/`. Future research-queue topic.
- Centola chapter bibliographic uncertainty (book of origin not definitively confirmed).
- E2 PNAS *Social Learning with Complex Contagion* skipped — recapture if user wants the recent extension.

**Kit-level findings logged to master_notes:**
- Subagent prompts must explicitly forbid writing to disk. Two subagents in this run wrote scratch summaries to `wiki/sources/`, `structured-ingests/`, and `/tmp/` despite prompts asking for in-message returns. Cleaned up. Recommend updating standard subagent prompt template.
- Marker engine OOMs under parallel invocation on shared GPU. `capture_pdf.py` could detect GPU pressure and auto-fall-back to pymupdf (or document the parallel-safety constraint clearly in the tool docstring). Currently the GPU OOM error path exits 0 (succeeds the script) but leaves no output file.

## [2026-04-26] query | mechanism synthesis — novel applications across new mechanism set

User `/query`: "with all the new methods now in the wiki being considered. How would you novelly apply technology/algorithms to enable some of our identified levers are there new avenues to consider?"

**Synthesis output.** Cross-product of the 10 new mechanism pages (added earlier 2026-04-26) × the existing 29-lever inventory on [[possible-strategic-levers]]. Eight novel builds and five candidate new lever avenues identified.

**Eight builds:**
1. Federated Pricing Observatory — FL substrate + Markup probe-and-publish pattern → eliminates Citizen Browser's Trail-of-Bits redaction engineering as substrate-level property. Enables [[possible-strategic-levers|lever #8]] / [[data-disruption-strategy-map|Tier 1 #3]].
2. Verifiable Mandate-Bound DSAR Pipeline — DID/VC + ClawNet + DSAR coordination → cryptographically-verifiable mandate at request time, anonymous aggregation at response time. Direct upgrade for [[possible-strategic-levers|lever #9]].
3. Multi-Collective Adaptive-Pricing Disruption — Karan two-collectives + Contextual Pricing Strategic Buyers → aligned collectives with different manipulation rules defeat the seller's two-phase identification. Enables [[possible-strategic-levers|lever #10]]; partial mitigation of [[the-firms-view|§3]].
4. Periphery-First Threshold Coordinator — Centola + Kickstarter + ClawNet → contact-graph-aware seeding with influencer down-weighting. Reformulates [[possible-strategic-levers|levers #14, #16, #28]].
5. Lever-Selection Decision Tool — strategic-classification separability dichotomy + pricing-algorithm-taxonomy → ranks manipulation dimensions by durability per pricing algorithm family. Refines [[possible-strategic-levers|cluster #3, #6, #7, #10, #11]].
6. Layered Cooperative Governance — Shapley external-sales + democratic strategic-decisions → resolves the documented governance tension on [[data-market-mechanism-design]].
7. Dual-Use Byzantine-Robust Observatory — mirror firm-side defence to consumer-side observatory → defends Build #1 against firm-side counter-poisoning.
8. Privacy Budget Marketplace — FL DP + data-market Shapley → ε-as-currency for queries + Shapley-as-currency for contribution attribution. New parallel institution.

**Five candidate new lever avenues** (not yet on [[possible-strategic-levers]]): DSAR-as-a-Service for member-bound litigation orgs; Federated price-discrimination detector as public service; Multi-cooperative agent federation; Lever-tactics simulator; Privacy-budget marketplace as parallel institution.

**Hard limits catalogued** (from new mechanism pages, not invalidating but bounding the builds): adaptive-seller recovery, disparate-impact externality, DP-as-firm-counter, LLM-negotiation buyer-disadvantage, antitrust risk concentration on lever #26, DID/VC issuer-trust governance unsolved.

**Tier-1 build recommendation:** Build #2 (Verifiable Mandate-Bound DSAR Pipeline) sits highest — sidesteps LLM-negotiation buyer-disadvantage, aligned with [[data-disruption-strategy-map|Tier 1 #1]], risk class 1, existence-proof exists (Uber audit). Build #1 (Federated Pricing Observatory) and Build #4 (Periphery-First Threshold Coordinator) follow.

**Wiki updates:**
- New strategy-layer page: `wiki/strategies/mechanism-synthesis-readout.md`.
- Index updates: `wiki/index.md` + `wiki/strategies/index.md`.
- Revision row appended.

**Open strategic questions surfaced** (preserved on the readout page): aggregator-governance for Builds #1/#7/#8; cross-collective coordination antitrust treatment; bootstrap path for Build #5 (catch-22 with Build #1); multi-cooperative federation governance; privacy-budget composition under repeated queries.

**Carry-over for future inventory revision:** the five candidate new lever avenues should be considered for addition to [[possible-strategic-levers]] when the inventory next gets refreshed.

## [2026-04-27] weekly-brief | second autonomous run

Second `/weekly-brief` run. Window: past 7 days (since 2026-04-20). 4 trend-scan subagents dispatched in parallel across the 4 streams (counter-algorithmic tooling; platform/federation/coop builds; counter-power research/think-tank; extraction news + enforcement). Trend-scan output ranked into 5 captures and 10 watchlist overflow items per the local Selection priority on `wiki/reference-sources.md`.

**5 captures:**
1. **webXray California GPC compliance audit** via The Markup (Apr 21 2026) — 7,634 sites, Google 86% / Meta 69% / Microsoft 50% non-compliance with the Global Privacy Control opt-out signal. Replicates the noyb 83.5% GDPR Art.15 pattern cross-jurisdictionally. Slotted into [[counter-power/regulatory-responses]] as new "GPC compliance audit" subsection under §9; cross-jurisdictional empirical-pattern note added on [[organizations/noyb]].
2. **Bharat Taxi Mumbai launch** (Apr 23 2026) — Indian state-sponsored driver cooperative under the Multi-State Co-op Societies Act, ~5.17 lakh drivers nationally, ~25K rides/day, EV-procurement and ₹5 lakh insurance bundling, zero-commission claim, passenger services slated for May. **Created new page** [[organizations/bharat-taxi]]; introduced **government-cooperative hybrid** as 5th typological category beyond the OECD four-type taxonomy on [[mechanisms/platform-cooperatives]].
3. **EU DMA Google search-data FRAND sharing preliminary findings** (Apr 16 2026) — first regulated, priced commercial-search-intent-data access surface (ranking, query, click, view; AI chatbots explicitly named as eligible beneficiaries). Public consultation closes May 1; final decision expected July 27. New subsection under [[counter-power/regulatory-responses|§4 EU]]; flagged on [[strategies/mechanism-synthesis-readout|Build #1 substrate update]] as candidate substrate for the Federated Pricing Observatory.
4. **JetBlue surveillance-pricing inflection event** (Apr 21–22 2026) — deleted-tweet incident → federal class action filed within 24h → FTC Chair Andrew Ferguson directed staff to examine new disclosure rules at Senate Commerce → multi-state legislative stack (NY/NJ/AZ/PA bills introduced). Activation curve compressed from years (RealPage / Live Nation arc 2022–2026) to one week. New "JetBlue Apr 2026 inflection event" subsection in [[industries/consumer-facing-dynamic-pricing|Airlines]]; FTC subsection in [[counter-power/regulatory-responses|§1]]; **Family 4 (airline RM) no-individual-features claim flagged contested** on [[mechanisms/pricing-algorithm-taxonomy]].
5. **PETS 2026 fingerprint-defence cluster** (Calgary, Apr 21 2026) — Ephemeral Network-Layer Fingerprinting Defenses (Pulls et al., maybenot framework, Reproduced artifact) + Dodge Application-Layer Video Fingerprinting Defenses (Witwer et al., Reproduced) + PriVA-C voice-assistant defence + Schramm et al. societal-awareness baseline + Berke et al. Google-authored entropy measure + EXADPrinter Android + Song et al. multi-agent LLM attack + MV3 ad-blocker effectiveness. New "PETS 2026 defence cluster" section on [[mechanisms/browser-fingerprinting]] with layer-scoping note clarifying that the Reproduced defences operate at network/application-stream layers (not in conflict with Venugopalan 2024 browser-attribute layer).

**Page-plan decisions made autonomously per the skill's policy:**
- 1 new page (bharat-taxi) — distinct enough scale + hybrid typology to warrant its own org page; not absorbed into drivers-cooperative.
- 7 existing-page updates — consolidating regulatory captures into [[regulatory-responses]] (already the landing page for this cluster), distributing JetBlue across consumer-facing-dynamic-pricing + pricing-algorithm-taxonomy + regulatory-responses, and the PETS 2026 cluster into browser-fingerprinting.
- **No conflict files opened.** The 86% Google GPC tracking vs Google's compliance claim is a *factual dispute between audit and corporate position* (both documented in the source itself), not a wiki-internal conflict. The JetBlue contested-claim on airline-RM is handled via in-page contested-claim flag (per the watchlist's existing "reference-layer claims to monitor for counter-evidence" entry) rather than a separate conflict file.

**Watchlist additions (10 overflow items):**
1. OpenAI Privacy Filter — open-weight on-device PII redaction (frontier-lab trust-asymmetry)
2. Drivers Cooperative Colorado RTD public-transit contract bid — decision imminent
3. Radish Cooperative NYC expansion — federated multistakeholder governance template
4. PETS 2026 CCPA-Android opt-out audit (Zimmeck et al.) — practical exercisability gap
5. PETS 2026 DSA ad-transparency audit (Benzaamia et al.) — uneven year-1 compliance
6. PETS 2026 Apple-vs-Google EU app-store ad-personalization comparison (Breuer et al.)
7. PCC Solidarity Stack pre-conference — Bangkok submission deadline Apr 30
8. FTC ANPRM grocery delivery fees — comments due May 18 2026
9. WPP/Publicis/Dentsu brand-safety collusion settlement — algorithmic coordination via trade-association theory
10. Berkman Klein Transparency Hub — terms-of-service surveillance database

**Trend-scan signal observations** (preserved on the brief):
- PETS 2026 dominates the counter-algorithmic-tooling stream this week (venue-event week, not organic dispersed trend).
- Empirical compliance-failure data is becoming the cross-jurisdictional baseline (webXray + noyb pattern).
- Driver-cooperative model going national-and-state-simultaneously, with an emergent gov-coop hybrid lens (Bharat Taxi vs Drivers Cooperative Colorado).
- EU DMA produces the week's clearest new data-access surface; signals possible substrate for the wiki's Build #1.
- The week's main signal is regulatory and litigation-side counter-power; consumer-side tool-release cadence from EFF / noyb / Mozilla / DAIR was zero this window.

**Outputs:** brief written to `wiki/weekly-briefs/2026-04-27.md` + `/tmp/weekly-brief-2026-04-27.md`. Email rendered to HTML and dispatched via SMTP. All wiki/raw changes left uncommitted on `collective-consumer-action-wiki` per skill policy; user commits on next login.

**Pre-existing uncommitted changes flagged at run start:** the working tree had substantial uncommitted work-in-progress carried from prior sessions (master_notes.md; wiki/index.md; wiki/log.md; wiki/mechanisms/* — 10 files modified or untracked; wiki/strategies/* — 4 files modified or untracked; wiki/reference-sources.md; wiki/revisions.md). Weekly-brief diff is layered on top — see brief's "Run notes" section for the separation.

## [2026-05-04] weekly-brief | third autonomous run

Third `/weekly-brief` run. Window: past 7 days (since 2026-04-27). 4 trend-scan subagents dispatched in parallel across the 4 streams (counter-algorithmic tooling; platform/coop/federation builds; counter-power research/think-tank; extraction news + enforcement). Slow week for tier-1 arXiv signal; solid platform-coop and enforcement material.

**5 captures:**
1. **Berkman Klein Center / ASML — Keyring open-source DID/VC mobile wallet** (launched April 16 2026; Harvard Gazette feature in window). On-device biometric auth + selective-disclosure proofs (age-band not birthdate; account-ownership not username); peer-to-peer trust graph; co-built with Linux Foundation Decentralized Trust Graph WG; GitHub `berkmancenter/keyring-wallet`. The first production-grade consumer reference implementation of the W3C DID/VC pattern documented at [[mechanisms/decentralized-agent-identity]]. ASML PI James Mickens + product team's incentive-misalignment admission ("incumbents benefit from owning your data") is the best-sourced public confirmation of the issuer-governance bottleneck the page already flags.
2. **Bharat Taxi — passenger-side go-live (May 2026).** State change on the existing wiki page captured 2026-04-27. ZeeBiz second-source corroboration; introduces the **Sahakar Taxi Cooperative Limited** operating-entity name + MSCS Act registration date (June 6 2025) + the eight sponsoring cooperative-federation list (AMUL, IFFCO, KRIBHCO, NAFED, NDDB, NCEL, NCDC, NABARD); confirms initial six-city scope (Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata) + accessibility flag at booking + intercity / metro-linked modes.
3. **PCC — Solidarity Stack framework (Trebor Scholz keynote, Cooperative AI Conference Istanbul, Nov 11 2025; PCC blog Apr–May 2026).** Seven-layer cooperatively-owned AI counter-architecture (Earth → Compute → Data → Algorithms → Labour → Application → Governance) plus a federation primitive (Solidarity Stack Circles → 2026 global online course → democratic planetary org), modelled on SWIFT as the working precedent for planetary-scale cooperative-protocol governance. Created **new strategy-layer page** [[strategies/solidarity-stack-readout]]. Three new research candidates flagged: African Tech Worker Cooperative, Sicredi Ouro Verde / Arla Foods, Hostsharing eG / Ashton Data Center Cooperative.
4. **NY AG → Instacart algorithmic pricing demand letter (Jan 2026) under NY Algorithmic Pricing Disclosure Act (effective Nov 10 2025).** Mandated disclosure phrase verbatim ("THIS PRICE WAS SET BY AN ALGORITHM USING YOUR PERSONAL DATA"); placement standard "clearly and conspicuously near prices" operationalised as a DOM-testable benchmark. Behavioral state change: Instacart ended all "item price tests" (partner-level promotion testing continues). Quantitative anchors from December 2025 Groundwork Collaborative + Consumer Reports field study: 437 shoppers / 4 cities / 73% of items at multiple prices / 13% avg differential / 23% max / ~$1,200/yr per family of four.
5. **Pluralistic — HB0895 loophole assessment (Doctorow / Garofalo, Apr 30 2026).** Six-loophole carve-out taxonomy on Maryland HB0895 (the "load-bearing first-in-nation prohibition" already documented on the wiki): grocery-only scope; consent-via-clickwrap exemption; promotional/temporary-discount exemptions (undefined); loyalty-card exemption; subscription exemption; no private right of action + pre-emption of Maryland Consumer Protection Act. Functions as a six-point evaluation checklist for assessing future state surveillance-pricing bills (NY/NJ/AZ/PA, CA AB 2564, Colorado HB26-1210). The "first-in-nation prohibition" framing is qualified, not overturned.

**Page-plan decisions made autonomously per the skill's policy:**
- 1 new page (`strategies/solidarity-stack-readout`) — cross-layer narrative architecture justified by 6+ concrete cross-links into existing mechanism pages.
- 4 existing-page extensions: `mechanisms/decentralized-agent-identity` (Keyring section), `organizations/bharat-taxi` (Passenger-side launch May 2026 section), `counter-power/regulatory-responses` (replace NY A3008 stub with substantive section + AG enforcement subsection; add HB0895 loophole assessment subsection), `industries/consumer-facing-dynamic-pricing` (Grocery delivery — Instacart subsection).
- **No conflict files opened.** The HB0895 loophole assessment is a refinement not a contradiction; the Solidarity Stack regulatory-skepticism is editorial disagreement not falsifiable; no other wiki-internal contradictions surfaced.

**Watchlist additions (10 overflow items):**
1. Global Web, Local Privacy? (arXiv 2604.18633, Apr 18 2026) — cross-jurisdictional tracking audit replicating webXray/GPC pattern (50.5% fewer trackers in EU opt-in vs CA opt-out)
2. APPSI-139 (arXiv 2604.27550) — privacy-policy summarization corpus; substrate for automated DSAR / disclosure-compliance audit pipelines
3. Nightshade 1.1 release (Apr 20 2026) — bug-fix maintenance signal; SAND Lab cadence confirmed
4. Boycat 3.1 Digital Risk Index — first consumer-facing tool combining boycott coordination + structured privacy-risk scoring
5. May Day 2026 spending boycott (May 1 2026) — ~750 events / 500+ orgs targeting Amazon and Target; mobilisation-scale-vs-tool-sophistication gap
6. WAO FareShare tool (Princeton; CSCW 2026 acceptance) — wage-audit tool for algorithmic deactivation; updates stale "drivers-seat-cooperative → watch WAO" entry
7. FPF "The Price is Right" report (Apr 9 2026) — taxonomy of US data-driven-pricing legislation (70+ active bills) + vendor-due-diligence audit template
8. EU DMA Google FRAND consultation closed May 1; final decision expected July 27 — ITIF filed comments opposing free-riding; Google demanded "reset"
9. House Oversight Committee surveillance-pricing investigation (March 5 2026; document responses arriving in window)
10. CA AB 2564 — full surveillance-pricing ban (broader than HB0895); CA AG CCPA-purpose-limitation CID sweep ongoing
11. CMA AA Driving School DMCC Act first decision — already documented on regulatory-responses but worth tracking as compliance-floor benchmark for drip pricing

**Trend-scan signal observations** (preserved on the brief):
- Counter-algorithmic tooling pipeline went **quiet** this week — no in-window tier-1 arXiv hits or major tracked-tool releases.
- Strongest material this week is on the **enforcement-applied-to-disclosure-laws** axis (NY APDA → Instacart halt) and the **prohibition-laws-have-loopholes** counter (HB0895 carve-out taxonomy).
- The **Solidarity Stack** is the week's most consequential strategy-layer addition — gives the wiki its first cross-layer narrative architecture for cooperative AI infrastructure.
- **Keyring** is the cleanest tooling-side capture: production-grade consumer DID/VC reference implementation answering the "is this user-deployable?" question Garzon et al. left open.
- **May Day 2026 spending boycott** is the most-coordinated consumer collective action in current cycle but ran on Action Network + social-media coordination — the gap between mobilisation scale and tool sophistication is itself wiki-relevant evidence for the Tier-1 collective-timing coordinator build candidate.

**Outputs:** brief written to `wiki/weekly-briefs/2026-05-04.md` + `/tmp/weekly-brief-2026-05-04.md`. Email rendered to HTML and dispatched via SMTP. All wiki/raw changes left uncommitted on `collective-consumer-action-wiki` per skill policy; user commits on next login.

**Pre-existing uncommitted changes flagged at run start:** working tree carried substantial uncommitted work from prior sessions (master_notes.md; wiki/index.md; wiki/log.md; wiki/revisions.md; wiki/reference-sources.md; multiple wiki/mechanisms/* and wiki/strategies/* files modified or untracked from clawnet-adjacent-methods and 2026-04-27 weekly-brief runs; the 2026-04-27 weekly brief itself untracked). The 2026-05-04 weekly-brief diff is layered on top — see brief's "Run notes" section for the separation. **Recommend a single `git add wiki/ master_notes.md` + `git commit` to absorb the whole backlog** rather than separating weekly-brief's contribution.

**Kit-level finding to log on `master_notes.md`:** the `/weekly-brief` template's poetry invocations (`poetry run python -m tools.capture_url ...`) assume `poetry` is on PATH for the harness's non-login shell. Under this Claude Code session the `~/.local/bin/poetry` binary was *not* on PATH; the first capture batch silently no-opped (`/bin/bash: line 1: poetry: command not found`). Workaround applied inline: `export PATH="/home/david/.local/bin:$PATH" && poetry run …`. Recommend the skill template either prepend `~/.local/bin` to PATH explicitly or invoke poetry via its full path. Generalises to any wiki-kit deployment using `pipx`-installed or user-local poetry.

## [2026-05-11] weekly-brief-ingest | OpenCourier protocol

Ingest of the **OpenCourier protocol** — the strongest find from the 2026-05-11 `/weekly-brief` trend scan. Platform Cooperativism Consortium blog post (`raw/research/weekly-2026-05-11/01-opencourier-protocol.md`) + corroborating arXiv 2511.02455 v2 vision paper (`raw/research/weekly-2026-05-11/07-opencourier-paper.md`) — Liu, Rao, Hwang, Vertesi & Monroy-Hernández, Princeton WAO, CHI '26 Extended Abstracts Barcelona.

**Page-plan decision:** new dedicated page `wiki/mechanisms/opencourier-protocol.md` (not an extension of [[agent-interop-protocols]]). Justified by: distinct counter-party pair (courier ↔ instance ↔ requester vs A2A's agent ↔ agent); separate institutional anchor (PCC/Princeton WAO vs Google/Linux Foundation A2A); substantive ≥1.5KB content depth (3-layer architecture, federation primitive contrast with FairFare, distinction from Beckn, reference-implementation details, 11 wiki-anchor cross-links).

**Substance captured:**
- Three-layer architecture: **Registry** (instance discovery, multiple registries can exist), **App-Instance** (courier-side job management; reference Courier Client surfaces worker-preference collection), **Instance-Requester** (instance ↔ restaurant/retailer via quotes + data-disclosure to auditors).
- Three goals (courier-facing translation of the wiki's info-asymmetry / power-imbalance / values-alignment framing): value alignment / correcting information asymmetries / reducing power imbalances.
- **Federation primitive** (cross-instance courier mobility) — explicit architectural contrast with same team's prior centralised FairFare crowdsource; protocol-layer abstraction above [[coopcycle]]'s single-implementation federation; CoopCycle becomes one possible OpenCourier-compliant implementation.
- **Distinction from Beckn**: complementary, not competing — Beckn = customer-vendor, OpenCourier = courier-facing. A composed Beckn+OpenCourier stack would form a complete decentralised gig-economy substrate.
- Reference implementation: `opencourier.cs.princeton.edu` (dummy Courier Instance) + multiplatform mobile Courier Client + admin dashboard; open-source with explicit contributor call.
- WAO connection: same Princeton team as [[drivers-seat-cooperative|FairFare]] (~1M rideshare trips crowdsourced) — OpenCourier is the substrate-layer evolution.

**Cross-references added (11):** [[platform-cooperatives]], [[coopcycle]], [[drivers-cooperative]], [[drivers-seat-cooperative]], [[agent-interop-protocols]], [[decentralized-agent-identity]] (Registry-issuer trust gap mirrors DID/VC issuer-governance gap), [[solidarity-stack-readout]] (sits in Scholz's "Application" layer; first Application-layer cooperative protocol with reference implementation), [[mechanism-synthesis-readout]] (direct architectural input to Build #6 Layered Cooperative Governance), [[possible-strategic-levers]], [[bharat-taxi]] (grassroots-protocol path vs state-capitalised path — opposite institutional logics, same capital-conundrum answer), [[buyer-cartels-antitrust]] (open question: cross-instance pricing coordination antitrust posture).

**Open questions flagged on the page:** (1) Registry governance unsolved; (2) courier identity/reputation portability across instances unspecified; (3) Beckn+OpenCourier composition undemonstrated; (4) antitrust posture for federated courier coops vs OECD safe-harbour thresholds open; (5) production-deployment numbers (courier earnings, fee structure, instance-switching) not yet measurable.

**No conflicts noticed.** OpenCourier is a refinement/extension of the existing platform-cooperative + federation framing on the wiki, not a contradiction. Per skill policy, watchlist update deferred to orchestrator.

**Outputs:** `wiki/mechanisms/opencourier-protocol.md` (new); `wiki/index.md` (catalog row); `wiki/revisions.md` (row appended).

## [2026-05-11] weekly-brief-ingest | Connecticut SB4

Autonomous subagent ingest from the 2026-05-11 weekly-brief trend-scan. Source: `raw/research/weekly-2026-05-11/02-ct-sb4-passage.md` (CT Mirror, May 4 2026 — "Consumer data privacy bill gets final passage in CT House"). Supplementary: `raw/research/weekly-2026-05-11/06-md-hb0895-cfm-context.md` (Consumer Finance Monitor cross-state framing).

**What CT SB4 does (three load-bearing mechanisms):**
1. State-run **data-broker registry** at the CT Department of Consumer Protection; mandatory enrollment + mandatory fees; effective **Jan 1 2027**.
2. **Centralized one-click deletion mechanism** at DCP spanning *all* registered brokers — **first cross-broker API-equivalent surface in US law**. Strongest tooling-hook of the week as a regulated single-endpoint substrate for the DSAR-coordination lever and [[strategies/mechanism-synthesis-readout|Build #2 Verifiable Mandate-Bound DSAR Pipeline]].
3. Surveillance-pricing disclosure mandate for *retail sellers and third-party delivery services* (Instacart-class vertical).

**Status:** House 141-6 May 4 2026 (Senate 31-4 April 23 2026); awaiting Gov Lamont (expected to sign). Builds on the Connecticut Data Privacy Act (2022).

**Wiki pages updated (2):**
- `wiki/counter-power/regulatory-responses.md` — new "Connecticut SB4" subsection added to §3 immediately before the MD HB0895 subsection. Contents: three-mechanism breakdown, tooling-hook framing, cross-state comparison table (NY APDA disclosure vs MD HB0895 prohibition vs CT SB4 disclosure+infrastructure), six-point Doctorow/Garofalo loophole checklist applied to CT (4 of 6 dimensions "not specified in capture" — flagged for follow-up via bill text), open enforcement-architecture question, MD-framing effect note. "Exists but weak" line on state regimes refined to characterise three distinct theories of the case (disclose / ban / build-infrastructure). Sources block extended with both 2026-05-11 captures.
- `wiki/industries/consumer-facing-dynamic-pricing.md` — brief "State-legislative cluster update (May 2026)" note added to the Grocery delivery — Instacart subsection, pointing at the new regulatory-responses subsection.

**No new pages.** Per the page-plan brief, CT SB4 is a regulatory artefact and fits within the existing regulatory-responses cluster.

**Conflict-flag check.** CT's centralized-deletion API does **not** overturn the wiki's load-bearing MD HB0895 framing — that framing was already qualified by the Doctorow / Garofalo carve-out taxonomy, and CT/MD are doctrinally distinct (categorical-ban vs centralized-deletion-API). MD remains the first-in-nation categorical prohibition; CT becomes the first-in-nation centralized cross-broker deletion API. **No `wiki/conflicts/` file warranted** — refinement, not contradiction.

**Open question for follow-up.** The CT Mirror capture does not specify SB4's enforcement architecture — AG-only (MD pattern), private-right-of-action (strongest), or DCP-led / shared. Binding question for whether the deletion API is operative at scale. Future capture from bill text or AG / DCP follow-up sources recommended.

**Revisions row appended.** `wiki/revisions.md` updated with summary row + source pointers. Watchlist update deferred to the orchestrator per the ingest-brief directive.

## [2026-05-11] weekly-brief-ingest | PIIGuard — publisher-side adversarial prompt-injection defense

Ingest of capture 4 from the 2026-05-11 weekly-brief: Liu, Zha & Chen 2026, *PIIGuard: Mitigating PII Harvesting under Adversarial Sanitization*, arXiv 2605.03129 (cs.CR), submitted 4 May 2026.

**Page-plan decision: new mechanism page.** PIIGuard introduces a distinct enough mechanism category — **publisher-side adversarial defense via repurposed indirect prompt injection** — that it anchors its own node rather than extending [[adversarial-data-poisoning]] (Glaze/Nightshade). Both are "adversarial publisher counter-tooling against scrapers" but operate on different objects (training-time image-pixel poisoning vs. inference-time scraper-LLM prompt steering) at different layers. Created `wiki/mechanisms/adversarial-prompt-injection-defense.md`.

**Key claims captured.**
- **Novelty framing.** The mechanism inverts indirect prompt injection from offensive primitive (the canonical attack on agentic systems, documented on [[agent-interop-protocols]] as a 60–100% leakage vector against A2A baseline) into a publisher-side **defensive** primitive. Same dual-use pattern as [[adversarial-data-poisoning]]'s offense/defense reframing — but at a different layer and with a different defender (webpage owner, not artist or recsys user).
- **Threat model.** Defender = ordinary public-webpage owner. Attacker = browsing-enabled LLM assistant (GPT-5.4-nano, Claude-haiku-4.5, DeepSeek-chat v3.2) fetching pages on behalf of a user issuing contact-seeking queries at scale. Prior defenses sit at the model/service/agent layer (requires LLM-vendor cooperation); PIIGuard is the first **webpage-level** defense ordinary owners can deploy.
- **Mechanism.** Optimised hidden HTML fragments. Three-component search loop: (1) rule-based leakage scoring, (2) evolutionary mutation over fragment text + insertion position, (3) judge-based recoverability assessment via a separate LLM judge. Fragment is hidden in the rendered page (specific hiding mechanism — CSS / ARIA / off-screen — deferred to PDF read; abstract does not specify).
- **Evaluation.** Direct-HTML mode, three target models: defense success rate **≥97% (often 100%)** under both rule-based and judge-based leakage evaluation, while preserving benign same-page QA utility. Two harder settings: public-URL browsing and attacker-side LLM sanitization — paper's stated finding is that "page-side defensive fragments can remain effective in deployment for some model-position pairs, but robustness varies substantially across browsing interfaces and sanitizer prompts." Honest reading: not a closed defense against scraping pipelines that include an LLM-based sanitizer.
- **Code-release status: NOT YET LINKED.** The arXiv abstract page (captured 2026-05-11) does not link to a code repository. The "Code, Data and Media Associated with this Article" panel lists only generic third-party services (alphaXiv, CatalyzeX, DagsHub, Hugging Face) with no paper-specific entries populated. Watch the arXiv listing for v2 with a `github.com/...` link, or a Hugging Face Space release. Until then, mechanism documented but not directly forkable.

**Wiki-fit framing.** Per the wiki's two-layer mandate, this is reference-layer documentation of a new mechanism class. Strategy-layer implications (editorial bullets) flagged in the page's "Relevance for consumer counter-power" section: deployable today by [[noyb]]-class data-subject-rights organisations publishing contact pages; substrate for the publisher-side equivalent of consumer-side [[obfuscation]] tooling; Tier-3 build candidate (cooperative-platform-level deployment) pending code release; watch for the sanitizer-vs-injector arms-race follow-on literature.

**Cross-refs added.** Page links into [[adversarial-data-poisoning]] (sibling on publisher-side counter-tooling axis), [[obfuscation]] (consumer-side equivalent), [[browser-fingerprinting]] (adjacent inference-time arms race from the consumer side), [[agent-interop-protocols]] (the offensive-use parallel — same primitive, opposite framing), [[agent-mediated-negotiation-empirics]] (Abdelnabi cooperative-collapse-under-adversary as the negotiation-domain analogue), [[noyb]] (deployment candidate), [[the-firms-view]] (publisher/firm-side adversarial-tooling frame). Three-row taxonomy table added clarifying defender / layer / attack-surface differences across the three publisher-side mechanisms now on the wiki.

**No conflict file warranted.** PIIGuard does not contradict any wiki-internal load-bearing claim. The dual-use framing (offense ↔ defense of the same primitive) is harmonised with the existing dual-use framing on [[adversarial-data-poisoning]] (poisoning attacks as both threat and "response from below").

**No watchlist update.** Per ingest-brief directive — orchestrator handles watchlist additions.

**Outputs.** `wiki/mechanisms/adversarial-prompt-injection-defense.md` (new); `wiki/index.md` row added in mechanism cluster after `adversarial-data-poisoning`; `wiki/revisions.md` row appended; this log entry.

## [2026-05-11] weekly-brief-ingest | Phillips v. JetBlue (ClassAction.org)

Autonomous ingest subagent for /weekly-brief 2026-05-11. Source: `raw/research/weekly-2026-05-11/03-jetblue-class-action.md` — ClassAction.org coverage (published April 29 2026) of *Phillips v. JetBlue Airways Corporation*, case 1:26-cv-02405, US District Court, filed April 22 2026. Extends the existing JetBlue inflection-event capture from 2026-04-27 (Fortune-based).

**New facts surfaced (vs. 2026-04-27 capture):**
- Case caption and docket number (*Phillips v. JetBlue Airways Corporation*, 1:26-cv-02405). 45-page complaint.
- National class scope: *"all natural individuals in the United States who used JetBlue's website and/or mobile application and whose communications and/or data were shared with third parties during the applicable statutory period."*
- Third-party vendor identities: **PROS Holdings, Inc.** (pricing algorithm vendor — alleged to be *"using an algorithm to set prices based on consumer behavior"*; **also one of the eight FTC 6(b) order recipients from July 2024** — same vendor surfacing on both regulatory inquiry and civil complaint) and **FullStory, Inc.** (session-replay / behavioural analytics).
- Privacy-tort framing rather than antitrust or price-discrimination: *"surveillance pricing is not illegal, [but] 'secretly' collecting consumer data without consent is."*
- Coerced cookie-consent contradiction: JetBlue's privacy policy notes site features will not function unless all cookies accepted.

**Page-plan decision (autonomous):** extend existing pages, no new dedicated page. Specifically:
1. `wiki/industries/consumer-facing-dynamic-pricing.md` — added "May 2026 build — *Phillips v. JetBlue Airways Corporation* (ClassAction.org coverage)" subsection under existing Airlines § April 2026 inflection event. Captures case details + doctrinal-significance editorial (standing template for cookie/fingerprint-based price-discrimination as privacy harm — lowers standing threshold below quantified-overcharge bar) + tooling-hook editorial (direct demand for paired-session *"did this site price-discriminate against me?"* audit tool, Tier-1 build candidate adjacent to DSAR-coordination cluster on [[strategies/data-disruption-strategy-map]]). Source block extended with ClassAction.org capture.
2. `wiki/mechanisms/browser-fingerprinting.md` — added "Case: *Phillips v. JetBlue Airways Corporation* — cookie / cache-based price personalisation alleged on commercial aviation" section before Regulatory context. Connects alleged mechanism (cookie / cache tracking + PROS + FullStory) to the fingerprint-defence literature: notes that incognito mode + cache-clearing only defeats cookies, not the active fingerprint stack; discovery in the case may produce the first US judicial finding on browser-fingerprinting-as-pricing-input if vendor stack includes any of the catalogued fingerprinting techniques. Tooling-implications subsection editorial: paired-session detector design is exactly the inverse of FP-Inconsistent (deliberately construct consistent-but-different fingerprints rather than identify inconsistent ones); the "blending in" paradox cuts both ways. Source block extended.
3. `wiki/mechanisms/pricing-algorithm-taxonomy.md` — extended the existing Family 4 contested-claim flag with a "May 2026 strengthening" sub-block. PROS cross-appearance on FTC 6(b) order list + vendor self-description as consumer-behavioural-input pricing engine is non-trivial *circumstantial* evidence against the "no individual identity features" reading; FullStory session-replay data, if used as pricing input, would directly contradict the aggregate-population-mix-inference framing. **Wiki position update: contested marker remains *contested, not resolved-against-Williams*.** Evidence is (a) circumstantial (vendor identity + vendor self-description), (b) untested in discovery. No algorithm-level disclosure has happened. Continue to treat known-architecture Williams-style RM as identity-feature-free; treat post-2020 industry trend (Delta 3% → 20%, JetBlue's PROS deployment) as a separate sub-family whose identity-feature use is *open*.
4. `wiki/index.md` — extended consumer-facing-dynamic-pricing summary entry with *Phillips v. JetBlue* mention.

**Conflict-file decision (autonomous, per skill):** **no new conflict file opened.** Reasoning: per skill, conflict file requires ≥2 sources from the run touching the same theme; this is one source. Per orchestrator instruction, the existing contested-claim watchlist marker is strengthened in place via the pricing-algorithm-taxonomy.md edits above rather than escalated to a new `wiki/conflicts/airline-rm-individual-identity-features.md` file. **Recommend the orchestrator's brief flag the contested marker as strengthened but unresolved.** The case is still circumstantial (PROS vendor-identity overlap + FullStory naming) — algorithm-level disclosure has not happened. A conflict file (or a strengthened watchlist entry) would become warranted if (a) a second source in a future run produces algorithm-level disclosure, (b) class certification is granted (which materially shifts the doctrinal status), or (c) the case is dismissed (which materially shifts the contested marker back toward settled).

**Watchlist update:** not done — orchestrator handles per skill.

**Cross-refs added:** four-way internal cross-link cluster: consumer-facing-dynamic-pricing § May 2026 build ↔ browser-fingerprinting § Case ↔ pricing-algorithm-taxonomy § Family 4 contested ↔ surveillance-pricing-retail (FTC 6(b) PROS recipient list cross-ref). Tier-1 build candidate explicitly cross-linked to strategies/data-disruption-strategy-map.

## [2026-05-11] weekly-brief-ingest | bharat-taxi multi-city expansion

ThePrint May 2026 coverage on Bharat Taxi's multi-city expansion push. Source: `raw/research/weekly-2026-05-11/05-bharat-taxi-multicity.md`. Pure extension of existing `wiki/organizations/bharat-taxi.md` with new "Multi-city expansion (May 2026)" section + surgical update to `wiki/mechanisms/platform-cooperatives.md` government-cooperative-hybrid paragraph.

**State-change captured.** First scale-out evidence for the wiki's emergent 5th-type government-cooperative-hybrid framing (flagged 2026-04-27 at founding; passenger-side go-live captured 2026-05-04; now first multi-city expansion). The question "will Bharat Taxi scale or stall at the Delhi pilot stage?" is being answered, but with substantial revisions to the launch-era scale claims.

**Cities reconfirmed.**
- *Operating*: Delhi NCR (Delhi / Gurugram / Noida); Gujarat (Ahmedabad / Rajkot / Somnath / Dwarka); Delhi airport pre-paid + app-based booking.
- *Pilot (April 2026, full-scale by month-end)*: Lucknow, Chandigarh.
- *Near-term (May 2026 → next 2–3 months)*: Jaipur (May), Mumbai + Pune (2–3 months).
- *Long-term*: nationwide by 2029, positioned explicitly as Uber / Ola challenger.

**Mumbai correction.** Apr 23 2026 onboarding event (captured 2026-04-27) was driver-side preparation; passenger-side operations in Mumbai still 2–3 months out per Gupta's May 2026 interview. This contradicts the ZeeBiz May 2026 "six initial cities at passenger go-live" framing — documented as scale drift on the page rather than escalated to a separate conflict file (single-discrepancy, already-stated low-moderate trust frame absorbs it).

**Scale drift documented (table on the page).** Three sources, three different figures:
- April 2026 Free Press Journal: ~5.17 lakh drivers / ~25K rides per day / Mumbai onboarding event.
- May 2026 ZeeBiz: 51K+ in Delhi at passenger-side launch; six-city initial scope (Delhi / Mumbai / Bengaluru / Chennai / Hyderabad / Kolkata).
- May 2026 ThePrint: ~3 lakh registered drivers nationwide / ~20K rides per day / ~29 lakh customers / Delhi NCR + Gujarat + pilots in Lucknow + Chandigarh only.

Resolution rule applied: ThePrint May 2026 is the working baseline because (a) most recent, (b) non-launch-event interview context (Gupta speaking to ThePrint reporter, not a press release). April launch-event figures retained as historical record but flagged not-corroborated.

**Pricing-model partial relaxation.** ThePrint reports a "nominal subscription fee per ride to cover operational costs" — the platform initially levied no fee, but operating costs are now partly covered through a per-ride charge. Fee amount and structure not disclosed. Page reframed: "partial-zero-commission with undisclosed fee structure" rather than pure zero-commission. The wiki's previous "zero-commission viability is not proven" caveat is now factually superseded — the platform itself has conceded the viability problem.

**Governance scale-out structurally distinct.** Single multi-state cooperative entity (Sahakar Taxi Cooperative Limited, registered June 6 2025 under MSCS Act 2002) is the operating vehicle across all cities; not a federation of per-city or per-state cooperative entities. Replication across cities happens via institutional tie-ups (UP Metro Rail Corporation; traffic police; Delhi airport authority for Terminal 1 expansion) rather than new cooperative incorporations. This is structurally different from the [[coopcycle]] federation-of-local-coops pattern documented on [[platform-cooperatives]] — flagged for tracking as membership grows from one region to dozens (driver representation at the board level, currently two driver reps per ZeeBiz source, becomes more dilute structurally).

**Sarathi-owner / Sarathi Didi framings captured.** Minister of Cooperation Amit Shah's March 2026 written reply in Parliament described the model as "a transition from the conventional 'driver-partner' model to a 'Sarathi-owner' model wherein drivers can become owner of the cooperative society, have representation in Board of Management and participate in profit sharing while having professional management to oversee operations." Sarathi Didi sub-programme: ~5,200 women drivers onboarded as of May 2026.

**Open questions logged in-page** (not surfaced as new wiki-wide research candidates):
1. Drivers-figure reconciliation (5.17 lakh April vs 3 lakh May 2026) — churn between announced-onboarding and actively-driving status? Different counting bases? Launch over-claiming? Or reporting inconsistency?
2. Pricing-algorithm architecture — flat / fixed-rate-card vs surge / dynamic? Source describes "transparency through periodic reviews" which suggests fixed-rate, but no algorithm-level disclosure.
3. Cost structure / take-rate transparency — what does "nominal subscription fee" mean numerically? How does it compare to incumbents' 25–40% commissions?

**No new mechanism page; no conflict file.** Pure extension of existing reference-layer page (`organizations/bharat-taxi.md`) plus surgical update to `mechanisms/platform-cooperatives.md` government-cooperative-hybrid paragraph. Scale drift documented in-place rather than escalated, per CLAUDE.md's "in-page documentation is sufficient when the wiki's framing already anticipates the discrepancy" pattern.

**Outputs.** `wiki/organizations/bharat-taxi.md` (Multi-city expansion section + Scale section restructure + Trust caveats rewrite + comparison-table row update + Source block extension); `wiki/mechanisms/platform-cooperatives.md` (government-cooperative-hybrid paragraph extended); `wiki/index.md` (bharat-taxi summary updated); `wiki/revisions.md` row; this log entry.

## [2026-05-18] weekly-brief | ingest run

**Sources ingested (7):** CO HB26-1210 (Colorado General Assembly bill page); DOJ Agri Stats press release; American Prospect Agri Stats critique (Dayen); noyb LinkedIn Art. 15 paywall complaint; Drivers Cooperative–Colorado Denverite feature; Battiloro et al. 2026 arXiv 2605.06749 ACA multiple-collectives preprint; Agri Stats proposed final judgment (D. Minn. 0:23-CV-03009).

**Pages created (2):**
- `counter-power/agristats-consent-decree.md` — reference-layer page for the DOJ + 6-state Agri Stats consent decree. Five-component remedy architecture (§IV/§VI/§VII/§VIII cites), comparison to RealPage remedy, criticism/remedy-efficacy subsection (Dayen/Hepner "laundering the cartel," ATPCO 1992 parallel, Tunney Act avenue).
- `conflicts/information-sharing-remedy-efficacy.md` — first conflict file; open. Position A: DOJ open-access + anonymisation floor structurally disrupts coordination. Position B: Dayen/Hepner open-access expands revenue without blocking ranking reports or consulting relationships. Pending user ruling.

**Pages extended (4):**
- `counter-power/regulatory-responses.md` — (1) Colorado HB26-1210 subsection (dual pricing+wage scope; PWSA definition; AG-only enforcement; private right of action struck by Senate amendment — stated explicitly; worker data-access entitlements; four-state comparative table updated); (2) Agri Stats DOJ pointer paragraph with five-component summary and conflict-file cross-link.
- `mechanisms/platform-cooperatives.md` — "Federation pattern — in-progress cases" section; Drivers Cooperative–Colorado (DCC) as second case alongside CoopCycle; Minsun Ji federation roadmap as load-bearing signal; RTD public-agency contract pending; fee-structure note (DCC 80% ≠ NYC DC 85%, neither canonical).
- `mechanisms/algorithmic-collective-action.md` — "Multi-collective dynamics: statistical bounds (Battiloro et al. 2026)" subsection; Theorems 3.1/4.1; label alignment as dominant driver; computability hierarchy; regime-dependence annotation on Karan ≤75% figure.
- `organizations/noyb.md` — "LinkedIn Art. 15 paywall complaint (May 2026)" section; legal theory (monetisation acknowledgement defeats data-protection-grounds refusal); model-complaint template value; DSAR-coordination Tier-1 build signal.

**Bookkeeping:** `wiki/index.md` (regulatory-responses, platform-cooperatives, algorithmic-collective-action, noyb summaries updated; agristats-consent-decree entry added; Open conflicts section created); `wiki/revisions.md` (8 rows appended); `wiki/watchlist.md` (ACA multiple-collectives entry struck; 10 new overflow entries added).

**Conflict opened:** `information-sharing-remedy-efficacy` — forward-looking remedy-efficacy dispute on the Agri Stats decree; pending user ruling.

---

## 2026-05-25 — /weekly-brief autonomous run

**Trigger:** Weekly cron (local), branch `collective-consumer-action-wiki`.

**Trend scan:** 4 parallel subagents covering arXiv cs.CY/cs.CR, GitHub trending + tracked tool repos, platform.coop + cooperative infrastructure, EFF + AlgorithmWatch + enforcement news. Window: 2026-05-18 to 2026-05-25.

**Captures attempted / succeeded:** 5 / 4
- `01-data-broker-compliance-california-2026` — succeeded (pymupdf; broken image refs, text complete)
- `02-apple-dp-audit-sp2026` — succeeded (pymupdf; broken image refs, text complete)
- `03-barriers-to-evidence-faccT2026` — succeeded (pymupdf)
- `04-doj-realpage-tunney-final-2026` — **FAILED** (DOJ 404 — Biden-era press release removed by Trump administration)
- `05-connecticut-sb4-pa26-64` — succeeded (capture_url)

**Pages written:** 3 new, 1 extended
- `wiki/mechanisms/dsar-and-data-deletion.md` — new (fills lint gap "data-broker page absent")
- `wiki/counter-power/dp-audit-methodology.md` — new (Apple DP audit)
- `wiki/mechanisms/barriers-to-evidence.md` — new (FAccT 2026 algorithmic evidence barriers)
- `wiki/counter-power/regulatory-responses.md` — extended (Connecticut PA 26-64 section)

**Watchlist updates:** Connecticut SB4 item updated (signed; phased rollout corrected). 10 overflow entries added.

**Conflict opened:** `dp-deployment-trustworthiness` — Apple DP audit vs watchlist "DP-as-firm-counter" framing. Pending user ruling.

**Bookkeeping:** `wiki/index.md` (3 new page entries added; 2nd open conflict added); `wiki/revisions.md` (entries appended); `wiki/watchlist.md` (SB4 item updated; 10 overflow entries added).
