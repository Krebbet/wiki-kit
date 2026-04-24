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
