# Polymarket Broad-Coverage Sweep — Snapshot 2026-05-16

First broad enumeration filtered by the **retail-tractable predictive-edge criterion** (saved as `feedback_market_research_focus.md`): probabilistic event + historical data + structured-model attack surface + non-saturated by professional quant/analyst coverage.

**Sweep:** top-30 events by 24h volume in each of 6 categories (Polymarket only had 12 active YouTube events). Captured via the **Gamma API `tag_slug` filter** after Polymarket's SPA category-landing routes began returning Vercel security-checkpoint pages on 2026-05-16 (kit gap logged in `master_notes.md`). 162 events surveyed total.

**Aggregate verdict:**

| Category | YES | PARTIAL | NO | n | YES rate |
|---|---|---|---|---|---|
| YouTube | **7** | 2 | 3 | 12 | **58%** |
| Movies | 9 | 10 | 11 | 30 | 30% |
| Music | 9 | 7 | 14 | 30 | 30% |
| Celebrities | 9 | 9 | 12 | 30 | 30% |
| Tech | 8 | 10 | 12 | 30 | 27% |
| Finance | 3 | 2 | 25 | 30 | 10% |
| **Total** | **45** | **40** | **77** | **162** | **28%** |

**Headline reading.** **YouTube view-count/milestone markets are the densest single retail-tractable cluster on Polymarket today** (58% YES rate from a small base). Movies / Music / Celebrities / Tech all run ~30% YES — close to a third of each category's flow fits the criterion. Finance is heavily quant-saturated (~10% YES rate, mostly commodity hit-price ladders that compete against CME quant shops).

**One live arbitrage flag** surfaced during the sweep: see [`Movies — live RT monotonicity arb`](#movies--live-rt-monotonicity-arb) below.

Sources: `raw/research/polymarket-broad-coverage-sweep/01-polymarket-tech-gamma.md` through `06-polymarket-finance-gamma.md`, all captured 2026-05-16 via Gamma API.

## YouTube — 58% YES rate, the densest cluster

(Source: `raw/research/polymarket-broad-coverage-sweep/04-polymarket-youtube-gamma.md`. 12 events.)

Polymarket has only 12 active YouTube events at 2026-05-16. 7 satisfy the user criterion outright. **MrBeast accounts for 9 of 12**; the remaining 3 cover four non-MrBeast creators — **xQc (Felix Lengyel), Forsen (Sebastian Fors), Jack Doherty, Clavicular (Braden Eric Peters)**. Cottage-industry expansion beyond MrBeast was previously absent from the wiki ([[snapshots/polymarket-mention-cottage-industry-2026-05-14]] documented MrBeast only).

**Retail-tractable shape:** YouTube view-counts, subscriber-milestone date-ladders, per-video count-bracket markets. All resolution observables are accessible via the **public YouTube API** (view counts, subscriber counts, video metadata). Structured-model attack: Poisson / power-law fit to historical channel-level growth, updated with intra-period view trajectory.

## Movies — Box-office brackets + RT ladders are the wins

(Source: `raw/research/polymarket-broad-coverage-sweep/02-polymarket-movies-gamma.md`. 30 events; **9 YES / 10 PARTIAL / 11 NO**.)

**Three YES sub-types** confirmed:

1. **Opening-weekend box-office bracket bins (7 YES events).** Structure 4 bracket-bins over a measurable quantity. Advance ticket sales (Fandango / AMC) anchor the prior; Thursday-preview gross is a hard 36-hour-before-resolution update signal. Per-event vol $1K–$84K; thin but recurring (new releases every weekend). Captured examples include *Obsession*, *Mortal Kombat II* 2nd weekend, *Devil Wears Prada 2* 3rd weekend, *In the Grey* opening.
2. **Rotten Tomatoes score ladders (3 YES events).** Cumulative-threshold sub-markets — `P(≥X)` for ladders of X. **Monotone constraint** `P(≥X) ≥ P(≥X+5)` is a free consistency check; violations are direct MRA opportunities per [[arbitrage-taxonomy]]. Edge window: critic-screening wave timing (1–3 days pre-release).
3. **Netflix top-show weekly rankings (6 PARTIAL events).** Weekly candidate-race over a public observable (Netflix Top 10 viewership feed). Thin per-event ($7K–$82K) but repeating cadence creates compound edge.

**Drop:**
- *Character-death bundles* (The Boys S5, Witcher S5, Euphoria S3) — PARTIAL; require leak monitoring / inside script knowledge, not corpus modeling. Lower repeatability than the cottage-industry mention markets in [[mention-markets]].
- *Award-winner picks* (Anime Awards, Oscars-style) — NO; saturated by entertainment-industry analyst shops.
- *Annual highest-grosser races* — NO; long-horizon slow-moving, edge requires advance box-office calendar analysis.

### Movies — live RT monotonicity arb

(Per `raw/research/polymarket-broad-coverage-sweep/.ingest/02-polymarket-movies-gamma.summary.md`, captured 2026-05-16.)

**"In the Grey" Rotten Tomatoes score** sub-markets at capture:

```
P(≥55) = 7%
P(≥60) = 9.5%
```

Required monotonicity: `P(≥55) ≥ P(≥60)`. Actual: **`P(≥55) − P(≥60) = −2.5 pp`** — a direct violation. The 60-threshold sub-market carries more volume ($77K) than the 55-threshold ($18K); the 55-threshold is likely stale/thin.

**Arb construction:** if `P(≥60) = 9.5%` is the correct value, then `P(≥55) ≥ 9.5%` — the current 7% offer underprices the 55+ Yes. Buy 55+ Yes at the offered price; the position is dominated by holding 60+ Yes at any price ≥ 9.5% — i.e., a winning 60+ outcome is necessarily also a winning 55+ outcome, so the 55+ Yes is structurally more likely. This is a textbook [[arbitrage-taxonomy]] §3 Long MRA on a within-ladder monotonicity constraint.

Liquidity caveat: sub-market is thin ($18K vol). Sizing is depth-bound, not capital-bound (the standard Shleifer-Vishny limits-to-arb signature documented in [[single-market-arbitrage-empirics]]).

### Movies — Gamma API data-quality gap noted

The ingest subagent flagged "How to Make a Killing" RT (`active=true&closed=false` per API) had end_date 2026-02-23 (already resolved) but Gamma returned it as live. **Operational rule for any downstream pipeline:** add an `end_date < today` guard before treating any Gamma API market as pre-resolution. Logged.

## Music — Billboard tractable; Eurovision near-resolution

(Source: `raw/research/polymarket-broad-coverage-sweep/03-polymarket-music-gamma.md`. 30 events; **9 YES / 7 PARTIAL / 14 NO**.)

Live snapshot is **Eurovision-dominated by 24h volume** — Winner ($6.7M/day), Top 10, Televote, Jury Winner, Top 5, Semi-Finals. **All 13 Eurovision-tagged events are NO** for the user criterion (one-shot near-resolution; no recurring structure; no model edge — pure crowd judgment).

**Real YES cluster: Billboard + Spotify weekly markets.** 13 events split 9 YES + 4 PARTIAL. Sub-types:

- **Billboard Hot 100 #1 song weekly** — recurring weekly cadence, public Spotify / Apple Music streaming data anchors the prior.
- **Billboard 200 #1 album weekly** — same recurring weekly cadence.
- **Album first-week sales bracket markets** — Structure 4 bracket-bins. Drake "Iceman" first-week sales is the headline example ($120K/day during release week).
- **Drake top-10 count markets** — count brackets on chart-position aggregates.

**Operational reading.** Music splits cleanly: ~half the queue is event-driven one-shots (Eurovision, specific awards) which fail the criterion, and ~half is recurring chart-based structure which is the canonical cottage-industry fit. The Music cottage industry is **wider than the wiki previously documented** — [[mention-markets#active-series-matrix-the-cottage-industry]] catalogued recurring tweet-count series; the analog for Music is recurring Billboard-position series.

## Tech — AI leaderboard + release-date ladders

(Source: `raw/research/polymarket-broad-coverage-sweep/01-polymarket-tech-gamma.md`. 30 events; **8 YES / 10 PARTIAL / 12 NO**.)

**YES cluster (8 events):**

- **AI leaderboard races** — "Which company has best AI model end of May" / "with Style Control On". Chatbot Arena is a single authoritative observable feed. Thin liquidity, structured observable, real probability mass in non-dominant outcomes.
- **Gemini release date-ladders** — per-date Yes/No sub-markets on Google Gemini version releases. Date-ladder Structure 2 ([[polymarket-market-structures]]) with monotonicity consistency checks.
- **Figure robotics livestream counting markets** — count brackets on robot-action observations during scheduled livestreams.

**PARTIAL (10 events):** deeper liquidity / NegRisk anonymization issues / conditional structure (e.g., SpaceX IPO brackets require IPO to happen first).

**NO (12 events):** saturated consensus (NVIDIA #1 cap at 97%), pure speculation without model (Ryanair, Tesla-SpaceX merger), Anthropic IPO dominated by 98.7% No-IPO outcome.

**NegRisk data-quality gap.** 16/30 Tech events use NegRisk grouped-event structure, and the Gamma API **anonymizes non-visible sub-market competitors as "Company A/B/C"** — a systematic data-quality gap for reconstructing full odds distributions on AI-leaderboard races. Flag for downstream model-building: the visible-named outcomes may not exhaust the candidate set.

## Celebrities — confirmed NOT a real cottage industry

(Source: `raw/research/polymarket-broad-coverage-sweep/05-polymarket-celebrities-gamma.md`. 30 events; **9 YES / 9 PARTIAL / 12 NO**.)

**Verifies the prior wiki claim** from [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] that Celebrities is mostly outcome-driven. Of the 9 YES events:

- 5 are chart-cross-listings (Billboard Hot 100, Spotify, ICEMAN) that **belong to Music**, not Celebrities — the "Celebrities" tag is contaminated by Music cross-listings.
- 2 are Eurovision semi-final markets.
- 1 is a global Spotify ranking market.
- 1 is the ICEMAN lyrics mention-market (already documented in [[mention-markets]]).

True "Celebrities" markets (gossip / lifestyle / announcement) are 57% NO — divorce/pregnancy/marriage/engagement/firing binaries with no structured-model signal. The largest Celebrities-native event is **Bachelorette Season 22** ($2.4M all-time) — a spoiler-arb pattern, not a base-rate-model target.

Operational reading: **the Celebrities tag is not a worth-mining surface independent of Music**. Treat any Celebrities cottage-industry target as a Music or Mentions cross-listing rather than a native Celebrities series.

## Finance — quant-saturated, narrow YES window

(Source: `raw/research/polymarket-broad-coverage-sweep/06-polymarket-finance-gamma.md`. 30 events; **3 YES / 2 PARTIAL / 25 NO**.)

**The 5th of 10 in-scope categories now covered.** Lowest YES rate in the sweep (10%). The top-30 by 24h volume is dominated by:

- **Commodity hit-price ladders** (11/30 events: WTI Crude, Gold, Silver, SPY, NVDA, TSLA, PLTR, AAPL, ABNB, HOOD, NG) — all tagged `pyth-finance` + `hide-from-new`. **All NO**: heavily quant-saturated by CME quant shops. Confirms [[llm-forecasting-by-domain]] Finance-weak claim with direct enumeration.
- **"Largest Company" NegRisk monthly races** — 4 events; all NO. Compete with equity quant.
- **Fed rate-cut / FOMC markets** — NO. Saturated.
- **Treasury yield bracket markets** — NO. Saturated.

**The 3 YES + 1 PARTIAL niche-tractable markets:**

| # | Market | Vol 24h | Why YES |
|---|---|---|---|
| 6 | **SpaceX IPO by ___** (date-ladder) | **$210K** | Specific corporate-event binary. June 30 leg at 91¢ (~$291K vol) near-resolved; July–Dec legs tractable for anyone monitoring SEC S-1 filings. Cross-listed under Tech (event 4 in Tech capture). |
| 13 | **In which month will SpaceX IPO** (NegRisk month picker) | $21K | 12-option NegRisk on same underlying. June at 93¢ consensus. Complementary granularity to event 6. |
| 15 | **Anthropic valued higher than OpenAI in 2026** (binary) | $17K | $78K all-time, OI $44K, 89¢ Yes. Small-information-set: resolution depends on private fundraising rounds. Edge from tracking VC announcements, S-1 / 10-K filings — not quant. |
| 3 | MicroStrategy sells any Bitcoin (PARTIAL) | $562K | Corporate-action binary. June 30 sub-market at 76¢ Yes ($2.7M vol). On-chain monitoring of MSTR treasury operations gives edge — but crypto-native sophisticated traders are present. |

**Reading.** Finance is the *narrowest* YES window of the sweep, but the 3 YES events all happen to involve **SpaceX / Anthropic / OpenAI** — exactly the AI-frontier funding round territory you (per saved user-profile context) track domain-specifically. The combined ~$248K/day vol across the 3 markets is small in absolute terms but large per-bet given the thin information set.

## Cross-cutting findings

(Synthesis — these observations span multiple categories of the sweep.)

1. **Monotonicity violations are present in Polymarket bracket markets.** The RT ladder on "In the Grey" is one captured example; the underlying mechanism (independent sub-market order books per bracket, no atomic constraint) means **any cumulative-threshold ladder is a candidate for MRA monitoring**. Cross-link to [[arbitrage-taxonomy]] §3 (Long MRA) and [[polymarket-market-structures]] Structure 4 (bracket bins).
2. **NegRisk sub-market anonymization is a Gamma API data-quality gap.** Tech AI-leaderboard races and "Largest Company" Finance races both anonymize non-leading candidates as "Company A/B/C". Any downstream model that reconstructs the full PMF needs a fall-back source (e.g., scraping the live category landing — currently Vercel-blocked).
3. **Recurring-cadence structure is the unifying signature of YES markets.** Tweet count weekly (cottage industry per [[mention-markets]]), Billboard Hot 100 weekly, Netflix top-show weekly, MrBeast per-video, YouTube subscriber milestone date-ladders — all share a fixed observation cadence + stable speaker/source corpus + measurable quantity. This is the operational template for the retail-tractable Polymarket pattern.
4. **The Vercel-checkpoint regression on category landings is current.** SPA captures via `tools/capture_url` no longer work for `polymarket.com/<category>` and `polymarket.com/pop-culture/<sub>`. The Gamma API `tag_slug` filter is the bypass. A kit-level companion to `tools/capture_polymarket_market.py` for category-level enumeration is the natural next tool (logged in `master_notes.md` 2026-05-16).

## What this sweep does NOT cover

- **Politics subcategories beyond Midterms** (Trump 305, Primaries 189, Global Elections 147, US Election 146 — 787 markets). Many of these are mention-style Trump-speech markets that fit the user criterion; the Gamma API tag-slug bypass works equally well for them.
- **Geopolitics subcategories beyond Iran** (Ukraine, Israel, Middle East, China — 302 markets).
- **Awards subcategory** — explicitly skipped per saved feedback (Oscars/Emmys/Grammys saturated by Hollywood analytics).
- **Most Crypto subcategories beyond top 21** (~240 markets).
- **Per-event resolution-rule text** for any of the 162 events here. The Gamma API event-detail captures (via `tools/capture_polymarket_market.py --slug <slug>`) would provide the binding spec for each.

## Operator next-step recommendations

(Editorial — your call.)

1. **Pick 2–3 YouTube YES events** (one MrBeast + one xQc/Forsen non-MrBeast) and run `capture_polymarket_market --slug <slug>` to grab binding resolution rules; then start the per-channel base-rate fit. YouTube has the highest YES density of the sweep.
2. **Monitor the "In the Grey" RT monotonicity arb.** Direct MRA candidate, depth-bound but live. Cross-check the order books before sizing.
3. **Capture SpaceX-IPO and Anthropic-vs-OpenAI per-event detail** via Gamma. These three Finance YES events fit your AI-frontier domain.
4. **Build the Gamma-API category-enumeration tool** to unblock the remaining 5 in-scope-category gaps (Politics-non-Midterms, Geopolitics-non-Iran, Weather, Economics, Other). The ad-hoc script that produced this snapshot is a starting point.

## Source

- `raw/research/polymarket-broad-coverage-sweep/01-polymarket-tech-gamma.md` — Tech category top-30 by 24h vol (Gamma API)
- `raw/research/polymarket-broad-coverage-sweep/02-polymarket-movies-gamma.md` — Movies category top-30 (includes live RT monotonicity arb on "In the Grey")
- `raw/research/polymarket-broad-coverage-sweep/03-polymarket-music-gamma.md` — Music category top-30 (Eurovision-dominated 24h vol)
- `raw/research/polymarket-broad-coverage-sweep/04-polymarket-youtube-gamma.md` — YouTube category, 12 events total
- `raw/research/polymarket-broad-coverage-sweep/05-polymarket-celebrities-gamma.md` — Celebrities top-30 (verifies prior outcome-dominant claim)
- `raw/research/polymarket-broad-coverage-sweep/06-polymarket-finance-gamma.md` — Finance top-30 (3 YES + 1 PARTIAL, otherwise quant-saturated)

## Related

- [[mention-markets]]
- [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]
- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[llm-forecasting-by-domain]]
- [[platform-comparison-kalshi-polymarket]]
- [[polymarket-bet-content-trends]]
- [[polymarket-lp-incentives]]
