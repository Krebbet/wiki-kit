# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-05-08] bootstrap | edge-finding in immature prediction markets

Initial bootstrap. Domain: Polymarket as primary platform (subject + data source for market definitions and historical prices), Kalshi as comparison point; applied focus on betting strategies, modeling techniques (Bayesian, ML calibration, game theory), and market microstructure for identifying and back-testing exploitation of mispriced markets.

Schema and commands tailored:
- `wiki/CLAUDE.md` — domain, goal, audience (single-operator quant), tone (quant/analytical, math-heavy, citation-dense), source-type list filled.
- `/research` authoritative-sources slot — peer-reviewed prediction-market lit, platform primary docs, arXiv preprints, named practitioner blogs, standard ML/game-theory texts. Excludes crypto-Twitter, market-recap content, content mills.
- `/research` source-type-notes slot — Polymarket capture requires `--js`; price snapshots dated under `raw/markets/<slug>/`; arXiv preferred over paywalled journals; chapter-by-chapter for books; lecture notes acceptable for math/ML.
- `/ingest` takeaway-prompts slot — flag strategies (with conditions), modeling techniques (with inputs), inefficiencies (with sample size + scope), calibration data (with metric), resolution-mechanism details, math/formulas (with derivation), conflicts.
- `/lint` domain-checks slot — stale/undated market data, math without provenance, strategy pages missing scope, calibration claims without scope, market pages missing resolution criteria.
- `/query` answer-tone slot — quant/analytical, terse, math inline, never define basic terms, lead strategy claims with their applicability conditions.

Ready to receive first source.

## [2026-05-12] research+ingest | market opportunities and types on Polymarket

First research run. Topic: "market opportunities and types on poly market". Captured 8 sources into `raw/research/polymarket-types-and-opportunities/`:

- 3 Polymarket docs (markets-events, top-level overview, UMA resolution)
- 5 arXiv papers: 2604.24366 (microstructure / Dubach), 2603.03136 (2024 election / Tsang & Yang), 2605.00864 (NBA arb / Cheng-Yang-Zou), 2510.15205 (Black–Scholes kernel / Dalen-Daedalus), 2508.03474 (arbitrage taxonomy / Saguillo et al.)

Dispatched 8 ingest subagents in parallel; all 8 returned ok with schema-valid `.ingest/<slug>.summary.md` files. Aggregator proposed 7 explicit new pages + 1 unknown + 46 cross-ref entries; consolidated to 10 pages (sub-source mini-pages folded as sections where appropriate; 09-polymarket-docs-overview folded into polymarket-architecture rather than standing alone — confirmed low-value as standalone).

Pages created (10):
1. `wiki/polymarket-market-taxonomy.md` — taxonomy of markets/events
2. `wiki/polymarket-architecture.md` — CLOB+chain settlement, CTF primitives
3. `wiki/uma-optimistic-oracle.md` — resolution flow with bond economics
4. `wiki/polymarket-microstructure.md` — eight stylized facts + sign-inference failure
5. `wiki/polymarket-liquidity-evolution.md` — Kyle's λ and half-life trajectories
6. `wiki/arbitrage-taxonomy.md` — MRA vs Combinatorial; $40M empirical anchor
7. `wiki/single-market-arbitrage-empirics.md` — platform vs NBA reconciliation
8. `wiki/combinatorial-arbitrage-empirics.md` — semantic vs structural dependence
9. `wiki/logit-jump-diffusion-kernel.md` — RN-JD framework (synthetic-only caveat)
10. `wiki/market-maker-handbook-prediction-markets.md` — A–S quoting in logit units

Soft tensions flagged on pages (no conflicts/ ruled): Kyle's λ stability (Dubach cross-section vs Tsang & Yang single-market trajectory); single-market arb scope (Saguillo full-lifecycle vs Cheng NBA in-game).

Kit-level fixes harvested during the run, logged to `master_notes.md`:
- `capture_url` networkidle timeout on Mintlify-style docs hosts → patched to domcontentloaded + opportunistic networkidle settle
- `capture_url` script-content leak via markdownify strip → patched to BS4 `tag.decompose()` for script/style/noscript
- Project-scope note: marker engine risky when host GPU is busy → defaulted to pymupdf this run

Lint check follow-ups outstanding: per-market pages and dated price snapshots not yet present (the lint rules for stale market data + resolution-criteria-link will start mattering once specific-market pages are added).

## [2026-05-12] research+ingest | trends in bet types + LLM edge opportunities

Second research run. Topic: "trends in the types of bets being made on polymarket... identify where these emerging betting markets have opportunities to use predictive models to get an edge". User cited word-prediction markets (Trump speech words, etc.) as the example exploitable category.

Captured 7 sources into `raw/research/polymarket-market-trends-and-llm-edge/`:
- 5 arXiv LLM-forecasting papers: PolyBench (2604.14199), Forecasting Future Language / Mention Markets (2602.21229), PolySwarm (2604.03888), Future Is Unevenly Distributed (2511.18394), KalshiBench (2512.16030)
- 1 Polymarket primary: Mentions category landing page (`polymarket.com/culture/mention-markets`)
- 1 practitioner: Falcon X "From Opinions to Odds" (CFTC swap dealer; Allium/Artemis data)

**2 captures failed** — Polymarket SPA event pages (`/event/what-will-powell-say-during-may-press-conference` and `/event/what-will-trump-say-in-next-speech`) timed out at 60s `domcontentloaded`. Logged in `master_notes.md`; proposed fix is a Gamma-API capture tool (`tools/capture_polymarket_market.py`) to bypass SPA hydration entirely. This is the highest-priority kit follow-up because the per-market resolution-criteria text is what the wiki's lint rules expect.

7 ingest subagents dispatched in parallel; all 7 returned ok with schema-valid summaries. Aggregator's heuristic title-extraction was weaker this run (only 1 of 7 explicit `new` titles parsed; rest came back `unknown`) — synthesized the page plan manually from subagent return reports.

Pages created (5):
1. `wiki/llm-forecasting-by-domain.md` — sources [01, 04]; domain tiers, news-augmentation recipe, lot-size alpha ceiling
2. `wiki/mention-markets.md` — sources [02, 06-mentions]; the user's edge thesis page; Polymarket category snapshot + Kalshi-validated MCP technique; flags per-market resolution-criteria gap
3. `wiki/polyswarm-llm-trading-framework.md` — source [03]; system-design only; latency-thesis conflict with [[polymarket-liquidity-evolution]] spelled out
4. `wiki/llm-epistemic-calibration.md` — source [05]; KalshiBench; temporal-filter methodology + per-model calibration table + model-naming anachronism caveat
5. `wiki/platform-comparison-kalshi-polymarket.md` — source [06-falconx]; industry sizing, OI/volume comparison, category mix, tick/fee differences

Soft conflicts flagged on pages (no rulings required):
- PolySwarm "several minutes" latency vs [[polymarket-liquidity-evolution]] 0.74-min half-life → scoped to immature markets only (recommendation accepted).
- PolyBench Brier-not-appropriate-for-Polymarket claim is methodological choice, noted on the page rather than the wiki tone slot.
- KalshiBench model-naming anachronism (Claude Opus 4.5, GPT-5.2-XHigh don't correspond to real releases) — methodology trusted, per-model rankings caveated at top of page.
- Mention Markets internal Brier inconsistency 0.1402 vs 0.1441 — noted; canonical 0.1402.
- LLM-by-domain Rumour Overweighting trace mismatch — flagged on page; taxonomy trusted at tier level, specific trace not cited.

Kit-level items harvested this run, logged to `master_notes.md`:
- `capture_url` fails on Polymarket SPA event pages even with prior patches → propose `tools/capture_polymarket_market.py` using Gamma API.
- Parallel-capture race in `next_numbered_filename` produces duplicate index prefixes (observed twice now; cosmetic only since slugs disambiguate) → propose per-output-dir file lock or uuid/timestamp suffix.

Open research directions surfaced:
- Build per-market Polymarket capture flow via Gamma API → enables per-market wiki pages and the lint check.
- Backtest MCP on Polymarket mention markets (Kim et al. validated on Kalshi only).
- Polymarket calibration baseline (Brier of *the market itself* on temporally-filtered post-cutoff outcomes) — the bar any LLM signal must clear.
- Recurring-cadence base-rate edge on weekly speaker markets (no LLM required).

## [2026-05-13] research+ingest | bet content and sizing

Third research run. Topic: "what is actually being bet on, breakdown of bet types, market sizes". User wanted granular data — top markets by volume, per-vertical sizing, who's in them.

Captured 7 sources, 5 succeeded; 2 Dune dashboards failed at Cloudflare interstitial (kit gap logged in `master_notes.md`). Successful captures into `raw/research/polymarket-market-content-and-sizing/`:
- 01-trmlabs-21b-volume — TRM Labs May 2026 on-chain analysis
- 02-sacra-polymarket — Sacra company profile through April 2026
- 03-polymarket-predictions — Polymarket Popular Predictions page (primary, 2026-05-13)
- 04-polymarket-crypto-category — Polymarket Crypto category (primary, 2026-05-13)
- 07-grayscale-polymarket — Grayscale Sep 2024 institutional research

5 ingest subagents dispatched in parallel; all returned ok with schema-valid summaries. The Polymarket Predictions and Crypto category captures yielded the first dated cross-market snapshots in the wiki (20 + 21 markets respectively with $-volume/odds/liquidity).

User accepted the review packet's 3-NEW + 2-UPDATES + 1-CONFLICT plan after a /query interruption.

Pages created (3 NEW):
1. `wiki/polymarket-bet-content-trends.md` — synthesis page; multi-source volume trajectory, per-vertical sizing, user-tier P&L case studies, manipulation patterns.
2. `wiki/snapshots/polymarket-top-markets-2026-05-13.md` — dated primary-source snapshot; 20 markets with full data table.
3. `wiki/snapshots/polymarket-crypto-category-2026-05-13.md` — dated vertical snapshot; 261 crypto markets, full subcategory taxonomy, 21 markets enumerated.

Conflict file (1):
4. `wiki/conflicts/wash-trading-share.md` — Dubach 2026 (1% median / 22.2% max) vs Columbia Nov 2025 (25% avg / 60% Dec 2024 peak); both findings stand; operational guidance + open follow-ups.

Updates (2):
5. `wiki/platform-comparison-kalshi-polymarket.md` — added per-vertical Polymarket/Kalshi sizing (sports / politics monthly breakdown), Polymarket-only monthly volume arc through 2025, Feb 28 2026 single-day record $425M, ICE capital structure (~$2.0B / ~23% / $8B pre-money Series E), Fee Structure V2 (March 30 2026), TRM 5-tier user cohort table, Robinhood drives >50% Kalshi volume.
6. `wiki/uma-optimistic-oracle.md` — added Pyth + Chainlink as additional oracles (Pyth for some markets per Grayscale; Chainlink for deterministic events per Falcon X). Resolution layer is multi-oracle, not UMA-only.

New subdirectories created: `wiki/snapshots/` and `wiki/conflicts/`. These establish the dated-snapshot pattern (one file per capture date) and explicit-conflict pattern (one file per unresolved tension) the wiki has needed.

Kit-level items logged to `master_notes.md` from this run:
- `capture_url` returns Cloudflare interstitial when target host runs a JS bot challenge (Dune Analytics dashboards). Proposed fix: extend bot-wall heuristic + add post-DOM Cloudflare-challenge wait.

Open follow-ups surfaced:
- Ingest `theverge.com/news/922925/polymarkets-top-0-1-percent` for explicit wallet-distribution numbers (referenced by Sacra but not in the Sacra body).
- Ingest the Columbia University wash-trading study directly to resolve the conflict.
- Build `tools/capture_polymarket_market.py` (Gamma API) — would also reveal crypto price-feed oracle identity, currently a snapshot-page open question.
- Re-attempt Dune dashboard captures after the kit's Cloudflare-handling fix.

## [2026-05-14] research+ingest | shape of mention markets + other niche Yes/No bets

Fourth research run. Topic: politics + niche-market shape (user explicitly excluded sports). Asked: "What is the shape of mentions markets and what other yes/no type bets are being published?"

Captured 8 sources, all successful (Polymarket category landing pages have proven reliably capturable; Help Center pages are short but contentful). Captures into `raw/research/polymarket-politics-and-niche-markets/`:
- 01-polymarket-politics-master — `polymarket.com/politics` (1,600 markets, 22 subcategories)
- 02-polymarket-geopolitics-master — `polymarket.com/geopolitics` (567 markets, 16 subcategories)
- 03-polymarket-iran-category — `polymarket.com/iran` (184 markets, 12 subcategories)
- 04-polymarket-midterms-category — `polymarket.com/politics/midterms` (544 markets, 6 structural types)
- 04-polymarket-help-resolution — Polymarket Help Center "How Are Prediction Markets Resolved?" (short, dense)
- 05-polymarket-aliens-category — `polymarket.com/pop-culture/aliens` (4 active markets; Kevin Warsh conditional bundle)
- 06-polymarket-science-predictions — `polymarket.com/predictions/science` (20 markets, $58.7M aggregate)
- 07-polymarket-help-clarifications — Polymarket Help Center "How Are Markets Clarified?" (canonical 3-component rule grammar)

Parallel-capture race produced two files at `04-` prefix (Midterms + Help Resolution); cosmetic only, slugs disambiguate. Same kit issue logged previously.

8 ingest subagents dispatched in parallel; all returned ok with schema-valid summaries. Notable structural findings emerged:

- **Conditional cross-market bundle** ("What will happen before Kevin Warsh is confirmed?" bundling Fed-rate-cut + alien-disclosure legs in one event) — Structure 6 in the new market-structures spine page. Previously undocumented in the wiki.
- **Date-ladder term-structure dominates Iran vertical**: every high-volume Iran market has 2–3 dated legs (May 31 / Jun 30 / Dec 31); all currently no-arb-compliant; Iran airspace 39%/47% is the tightest live spread.
- **Combinatorial-arb candidate on Midterms**: balance-of-power composite (D-Sweep 43%, R-Sen ∧ D-House 33%) vs chamber-control marginals (P(D-House) 79%, P(R-Senate) 53%) implies P(R-Sweep) ≈ −12% — visible inconsistency.
- **Earthquake magnitude ladder** in Science shows potential monotonicity violation (10.0+ at 6% > 9.0+ at 3%); flagged for investigation in a follow-up run.

User accepted the review packet's 5-NEW + 2-UPDATES plan (no conflict-doc this run; the structural-shape question was the spine).

Pages created (5):
1. `wiki/polymarket-market-structures.md` — the spine; 7 structural types catalogued with examples + arb topology + 3-component resolution-rule grammar.
2. `wiki/snapshots/polymarket-politics-category-2026-05-13.md` — 22 subcategories, 21 markets, 5 structures present.
3. `wiki/snapshots/polymarket-geopolitics-category-2026-05-13.md` — combined Geopolitics + Iran; date-ladder term-structure tables; 6 conditional-probability calculations.
4. `wiki/snapshots/polymarket-midterms-category-2026-05-13.md` — 6 structural types; combinatorial-arb derivation; per-seat liquidity asymmetry (~100×–500× vs chamber-control).
5. `wiki/snapshots/polymarket-niche-categories-2026-05-13.md` — Aliens + Science combined; Kevin Warsh bundle documented; Science Poisson territory identified.

Updates (2):
6. `wiki/mention-markets.md` — added canonical 3-component rule grammar section (resolution source / end date / edge cases) and title-vs-rules distinction; explains why per-market resolution-criteria gap matters (count thresholds + observation windows + exact-string semantics all live in component 3).
7. `wiki/uma-optimistic-oracle.md` — added 4 details from Help Center: proposer reward separate from bond return; propose-too-early = full $750 bond loss explicit; USDC.e/pUSD alias note; settlement-mechanics primary statement ($1/share win, $0 loss, trading halts).

No new kit-level items this run; all captures succeeded. Cumulative kit gap on per-market resolution-rule extraction (Gamma API tool) remains the highest-priority follow-up.

Open follow-ups surfaced:
- Investigate the earthquake-ladder monotonicity violation (`9.0+` at 3% vs `10.0+` at 6%) — either captured-data label flip or a genuine MRA candidate.
- Verify "Aliens.gov confirmed immigration website?" resolution criteria (49% near-coinflip needs definition of "confirmed").
- Locate the Hantavirus / Jesus-Christ markets cited in prior search snippets but absent from the Science capture (likely sibling categories or resolved).
- Deeper Midterms capture: 522 of 544 markets are below the fold; Senate per-seat (35) and Governor (36) markets not in current snapshot.

## [2026-05-15] research+ingest + kit | cottage-industry mention markets + Gamma API tool

Fifth research run, scoped per user's saved feedback (`feedback_market_research_focus.md`): focus on retail-tractable mention markets, exclude Senate-style high-information races and tail-event pandemic-style markets. Captured 6 Pop Culture subcategories to enumerate the cottage industry: Tweet Markets, MrBeast, Taylor Swift, Iceman, Reality TV, GTA VI.

6 ingest subagents dispatched in parallel; all returned ok with schema-valid summaries. Critical finding from this run: **only 3 of 6 named "mention-adjacent" subcategories actually host mention markets**. Tweet Markets (28 markets, 9 distinct speakers) is the headline cottage industry — Elon Musk dominates at ~$19M aggregate; the 8 smaller-volume speakers (Trump-Truth-Social, White House, Ted Cruz, CZ, Zelenskyy, Khamenei, NYC Mayor) are the retail-tractable target. MrBeast contains 1 mention market + 8 brackets/milestones. Iceman is partial (keyword markets alongside chart/sales). **Taylor Swift, Reality TV, GTA VI are all outcome bets** (pregnancy binaries, season winners, launch-date races) — not mention markets despite living under Pop Culture.

KIT-level deliverable this run: **`tools/capture_polymarket_market.py`** implemented and smoke-tested. Resolves the per-market resolution-rule kit gap that was logged at `master_notes.md` 2026-05-12 and surfaced as a blocker across [[mention-markets]], [[snapshots/polymarket-crypto-category-2026-05-13]], and [[snapshots/polymarket-niche-categories-2026-05-13]]. The tool hits `gamma-api.polymarket.com/events?slug=<slug>` and returns the full event tree (event + all sub-markets) with binding resolution rules in the `description` field. Smoke test on `what-will-trump-say-during-bilateral-events-with-xi-jinping` captured 33 sub-markets with the canonical mention-market criteria (plural/possessive counts; compound-word rule with explicit `joyful`/`killjoy` example; full-name accounting; **AI-generated audio/video does NOT count**; only live-broadcast remarks; cancellation clause). Output at `raw/markets/what-will-trump-say-during-bilateral-events-with-xi-jinping/2026-05-14.md` (979 lines).

Two new project-scope conflicts surfaced by live Gamma API responses:
- **`umaBond` = $500 USDC.e** (live, on both Trump-Xi mention market and FIFA World Cup market at $976M cumulative volume). Wiki [[uma-optimistic-oracle]] documents $750 from the Polymarket Help Center. Either help docs stale, or $750 is disputer-side vs $500 proposer-side, or higher-stakes bonds exist (FIFA capture argues against). Logged.
- **`orderPriceMinTickSize` per-market** at `0.01` (central probabilities) or `0.001` (tail probabilities). Wiki [[platform-comparison-kalshi-polymarket]] cited Falcon X's `$0.0001` figure — not reproduced on the captured sample. Logged.

Pages created (1):
1. `wiki/snapshots/polymarket-mention-cottage-industry-2026-05-14.md` — combined 6-subcategory snapshot with explicit mention-vs-outcome classification; full Tweet Markets 9-speaker enumeration with implied base rates per speaker; modeling spine (Poisson / NegBin + mid-week Bayesian update); cross-references to the Gamma API tool.

Updates (3):
2. `wiki/mention-markets.md` — Added Gamma API workflow section documenting `tools/capture_polymarket_market.py` with usage examples + the 6 canonical mention-market criteria (plural/possessive/compound/full-name/AI-exclusion/live-only/cancellation) extracted from the Trump-Xi capture; added 8-speaker tweet-market enumeration to the Active Series Matrix; added subcategory-name vs actual-content reality check.
3. `wiki/uma-optimistic-oracle.md` — Added "Live Gamma API observation" section documenting the $500 bond / $5 reward live values with the conflict caveat against the $750 help-center number; updated bond-economics math (~$250 net gain at $500 bonds vs ~$375 at $750).
4. `wiki/platform-comparison-kalshi-polymarket.md` — Revised tick-size claim to per-market variable (0.001 tail, 0.01 central); flagged Falcon X's $0.0001 figure as not reproduced; updated lead paragraph to match.

Master_notes additions:
- `2026-05-14 — Gamma-API capture tool implemented` (Status: applied; resolves the 2026-05-12 SPA gap)
- `2026-05-14 — umaBond = $500 (not $750)` (Status: open; project scope)
- `2026-05-14 — Polymarket tick size varies 0.001-0.01 per-market` (Status: open; project scope)

Open follow-ups:
- Verify the $500/$750 bond discrepancy by capturing a *disputed and resolved* event via Gamma API (should reveal whether disputer bond is the $750 figure).
- Run `capture_polymarket_market` against each of the 8 smaller-volume tweet speakers to grab their per-market resolution rules — needed for systematic per-speaker base-rate modeling.
- Apply the captured rule criteria (no AI audio/video, live-only, compound-word semantics) to any text-corpus modeling pipeline downstream.

## [2026-05-16] research+ingest (two runs) | mechanics + broad-coverage sweep

Two research runs in one session.

**Run A — mechanics (8 sources, all Polymarket Help Center / Docs):**

How-are-markets-created (×2 — help + docs URLs serve identical content), Can-I-sell-early, Limit Orders, Sponsor Market Rewards, Maker Rebates Program, Liquidity Rewards Program, Rewards landing page.

Closed the creation-pipeline gap in [[polymarket-market-taxonomy]]: users cannot self-create; proposals via Twitter @polymarket; required fields are title + resolution source + evidence of demand; no community vote / on-chain governance. The closest retail-accessible analog to "create a market" is **sponsoring** an existing one (deposit USDC into a smart contract that pays daily rewards to LPs; sponsor return = zero; purpose is liquidity acquisition for your own trading).

Closed the secondary-market question: positions are freely tradable pre-resolution via market orders (min $1, prevailing bid) or limit orders (min 5 shares, partial fills supported). Sports markets have a 3-second taker delay and whole-book wipe at scheduled game start.

Surfaced three LP-reward programs as **distinct, stackable mechanisms**: Liquidity Rewards (platform-funded, proximity-weighted, max-spread gate, both-sides-rule-below-$0.10), Maker Rebates (taker-fee-funded, formula `fee_eq = C·feeRate·p·(1−p)`, Crypto 20% / others 25% rebate), Sponsor Market Rewards (third-party-funded, daily distribution). Live Rewards landing data 2026-05-16: Esports dominates current sponsor queue (~$3,412/Valorant series). The combined LP-yield calculation is per-market `liquidity_rewards_share + maker_rebate_share + Σ active_sponsor_rewards_share`.

Pages: 1 NEW (`polymarket-lp-incentives`) + 2 UPDATES (`polymarket-market-taxonomy` creation pipeline; `polymarket-architecture` Trading & Order Lifecycle).

**Run B — broad-coverage sweep (6 categories × top-30 events via Gamma API tag_slug):**

162 events surveyed across Tech, Movies, Music, YouTube, Celebrities, Finance — filtered by saved `feedback_market_research_focus.md` criterion. **Aggregate: 45 YES / 40 PARTIAL / 77 NO.**

KIT REGRESSION: Polymarket SPA category landings (`polymarket.com/tech`, `/pop-culture/movies`, etc.) began returning **Vercel security-checkpoint** pages on 2026-05-16. Identical URLs captured cleanly 2 days prior. The Gamma API `tag_slug=<slug>` filter is the discovered bypass — returns the same event data server-side. Logged at `master_notes.md` 2026-05-16 with proposed kit fixes (bot-wall heuristic + category-level Gamma capture tool).

YouTube emerged as the densest YES cluster (7/12 = 58% YES rate). Non-MrBeast creators discovered: xQc, Forsen, Jack Doherty, Clavicular — previously absent from the wiki. Movies / Music / Celebrities / Tech all ~30% YES rate. Finance is the worst (10% YES rate; commodity hit-price ladders dominate and are heavily quant-saturated). Confirmed prior [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] claim that Celebrities is outcome-driven — the 9 visible YES events in Celebrities are mostly Music cross-listings (Drake, ICEMAN, Eurovision).

Live MRA candidate flagged: "In the Grey" Rotten Tomatoes ladder `P(≥55) = 7% < P(≥60) = 9.5%` — direct monotonicity violation per [[arbitrage-taxonomy]] §3. Depth-bound ($18K vol on the underpriced leg); standard limits-to-arb signature.

Page: 1 NEW (`snapshots/polymarket-broad-coverage-sweep-2026-05-16`) + index Coverage Status update (7 of 10 in-scope categories now covered; gap ranking re-prioritized to Politics non-Midterms, Geopolitics non-Iran, per-event resolution rules for the 45 YES markets, smaller-volume tweet speakers, Weather/Economics/Other categories).

Master_notes additions:
- 2026-05-16: Vercel security checkpoint on Polymarket SPA + Gamma `tag_slug` bypass (Scope: kit; status: open — pending bot-wall heuristic + category Gamma tool)
- 2026-05-16: Ingest schema validator brittleness on section-name variants (Scope: kit; observed 3-of-8 failure rate on parallel subagent dispatch)

Open follow-ups beyond the page writes:
- Productize the Gamma category-enumeration as `tools/capture_polymarket_category.py` (or extend `capture_polymarket_market.py` with `--tag-slug`).
- Per-event Gamma captures for the 45 YES-classified markets from the broad sweep → starts the per-market resolution-rule corpus.
- Sweep remaining Politics / Geopolitics / Weather / Economics subcategories via the same tag_slug bypass.
- Verify the RT monotonicity arb on "In the Grey" against the live order book before sizing.

---

## [2026-05-16] feasibility-deep-dive | per-theme assessment of the 10 strategy-matrix themes

User asked for a feasibility page per theme from [[polymarket-strategy-matrix]] and a meta-review to make first-attack decisions. Process:

1. Dispatched 10 parallel research agents (one per theme) against live Gamma API + the existing wiki backbone. Each returned a structured summary at `raw/feasibility/<theme>/summary.md` answering the 4 strategy-matrix decision-tree questions (YES-theme? data source? structural-arb shape? microstructure regime?) with rubric scores 1-5 on data / modeling / depth / non-saturation.
2. Wrote 10 wiki feasibility pages at `wiki/feasibility/<theme>.md` consolidating each summary into tight quant-tone reference (~150-200 lines each).
3. Wrote `wiki/feasibility-review.md` cross-theme meta-review ranking 1-10 with top-5 live time-sensitive trades + cross-cutting daily Σ-check watchlist + reusable infrastructure build sequence.
4. Updated `wiki/index.md` (added 11 page entries) and `wiki/revisions.md`.

Outcome ranking (rubric / capital tier / time-to-edge):
1. **Mention markets** — GO 16/20. Top trade: CZ Binance regime-shift (`cz-binance-of-tweets-may-19-may-26-2026`, just opened).
2. **YouTube** — GO 15/20. Top trade: MrBeast 497M-subscriber June 30 milestone (market at 62%; linear model implies >85%).
3. **Movies** — Conditional YES 15/20. Top trade: RT monotonicity arb on In the Grey persists 1pp at mid; Thursday-preview gross is T-36h hard signal.
4. **Geopolitical date-ladder (Iran)** — YES. Top trade: airspace 8pp slack monotonicity watchlist; Portwatch 7-day MA as Hormuz near-resolution oracle.
5. **AI/tech milestones** — YES. Top trade: Gemini 3.5 by May 31/Jun 30 hazard model with USPTO trademark monitor.
6. **Streaming charts** — Conditional YES 14/20. Netflix Top 10 lowest pro-saturation of any chart type.
7. **Scenario grid (Midterms)** — Conditional YES. LIVE MISPRICING: D-Senate+R-House composite 1.45¢ vs ~3.0¢ implied (~2× underpriced); $200-400 gross per round-trip on $15-30K position.
8. **Corporate-event binaries** — NARROW-YES. SpaceX EDGAR S-1 + MSTR Arkham/Etherscan + Anthropic Crunchbase; total $60K-$175K deployable.
9. **LP yield farming** — Meta-strategy. Starmer cluster $300-400/day with $98-129K deployed; A-S quoting with inventory skew required.
10. **Crypto short-horizon** — AVOID for 5m/15m/1h/4h Up-Down (max saturation). Pre-Market FDV is the retail niche.

Live findings updating wiki gaps:
- **BTC price markets resolve via Binance BTC/USDT 1m candles, NOT Chainlink/Pyth.** Partially closes [[uma-optimistic-oracle]] open follow-up. OpenSea Pre-Market FDV uses vague "most liquid price source" — elevated UMA dispute risk.
- **May-13 P(R-Sweep)=−12% candidate is NOT live** — was a partial-capture artifact of UI snapshot showing only 2 of 4 composite outcomes. Replaced with a different and larger live discrepancy: composite-implied P(D House) 44.95% vs binary standalone 78.5% (33.5pp gap) concentrated in the D-Senate+R-House leg.
- **RT monotonicity arb on In the Grey** persists at 1pp mid violation (below spread for riskless arb but indicates the mechanism). Generalizable rule: `mid(≥X) < mid(≥X+5)` by more than `max(spread_X, spread_X+5)/2` is exploitable.
- **NegRisk anonymization in Gamma API** — only companies with nonzero liquidity history appear with real names; Best Chinese AI Company May fully blocked (all 25 "Company A"-"Company Y" at $0). Main AI leaderboard race not blocked.
- **Fourth yield layer discovered**: `holdingRewardsEnabled: True` on select FIFA sub-markets (not NBA/NHL/Starmer). Mechanics unknown — flagged as open question in [[feasibility/lp-yield-farming]].

Open follow-ups to address before capital deployment:
- On-chain `OrderFilled` maker-HHI analysis for Starmer + MrBeast sub-markets (saturation empirics; the wiki currently relies on heuristics).
- Fill-rate empirics for LP yield farming on mid-cap political (load-bearing unknown for MR income).
- MixMCP transfer validation on Polymarket (Kim et al. validated only on Kalshi earnings calls); ICEMAN prior-episode corpus is cleanest test bed.
- `holdingRewardsEnabled` mechanics resolution.
- 2028 primary scenario grids — defer to mid-2027 when VP-pick markets emerge.

Tier-1 immediate actions per the meta-review (no further user input needed per "do not wait" directive):
- CZ tweet-count regime-shift trade (same-week entry).
- D-Senate+R-House composite long with Republican House binary short hedge.
- MSTR Arkham/Etherscan alert configured.
- Iran airspace + uranium daily monotonicity Σ-check.

Pages written (11):
- wiki/feasibility/mention-markets.md
- wiki/feasibility/movies.md
- wiki/feasibility/streaming-charts.md
- wiki/feasibility/youtube.md
- wiki/feasibility/ai-tech-milestones.md
- wiki/feasibility/crypto-short-horizon.md
- wiki/feasibility/corporate-event-binaries.md
- wiki/feasibility/geopolitical-date-ladder.md
- wiki/feasibility/scenario-grid.md
- wiki/feasibility/lp-yield-farming.md
- wiki/feasibility-review.md
