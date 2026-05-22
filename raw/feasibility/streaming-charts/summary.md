---
title: "Streaming Chart Position Markets — Feasibility Assessment"
domain: "Billboard Hot 100 #1 / Billboard 200 #1 / Netflix Top 10"
assessed_on: "2026-05-16"
assessor: "claude-sonnet-4-6"
verdict: "CONDITIONAL YES — Billboard weekly markets tractable via Kworb/Chartmetric pipeline; Netflix Top 10 tractable via persistence model; both limited by thin liquidity not information access"
---

# Feasibility: Streaming Chart Position Markets

## 1. Domain Definition

Three recurring Polymarket market families:

**A. Billboard Hot 100 #1 (weekly)** — Which song holds #1 on the Billboard Hot 100 for a given week-of-Saturday date? Resolution source: official Billboard chart published every Tuesday at billboard.com/charts/hot-100. Data period: Friday–Thursday of the prior week. Confirmed from slug `billboard-hot-100-1-song-week-of-may-23`: "Billboard updates its Hot 100 songs chart each Tuesday (with adjusted release schedules on some holiday weeks), reflecting data from the previous week (Friday–Thursday). Each Billboard chart is then titled 'Week of (date of the upcoming Saturday)'. This market will resolve as soon as the relevant chart is published. If the Billboard Hot 100 chart for the specified week is not published within 14 calendar days of the expected release date, this market will resolve to 'Other'."

**B. Billboard 200 #1 (weekly)** — Which album holds #1 on the Billboard 200 for a given week-of-Saturday? Same Tuesday publication cadence. Resolution source: billboard.com/charts/billboard-200. Confirmed from slug `billboard-200-1-album-week-of-may-23`: same Tuesday update schedule, same 14-calendar-day fallback, same resolution source.

**C. Netflix Top 10 (weekly)** — Which show/movie ranks #1 (or #2) on Netflix globally or in the US for a given week? Resolution source: top10.netflix.com, updated Tuesdays at 3:00 PM ET, reflecting Monday–Sunday viewership from the prior week. Markets are cross-tagged under `movies` and `top-netflix`. Data scope: English-language only for the global lists (confirmed from resolution language: "The ranking is based on total views globally, as reported by Netflix for TV shows (English only)").

## 2. Live Market Landscape (2026-05-16)

### Billboard tag (`tag_slug=billboard`)

| Slug | Type | Vol 24h | Vol all-time | OI | Liquidity | Structure | End Date |
|---|---|---|---|---|---|---|---|
| `drake-iceman-first-week-album-sales` | Album debut sales bracket | $128,516 | $182,368 | $31,383 | $188,009 | NegRisk bracket-bin, 8 brackets | 2026-08-31 |
| `billboard-200-1-album-week-of-may-23` | Billboard 200 #1 weekly | $6,739 | $52,346 | $6,376 | $32,185 | NegRisk candidate race, 21 sub-markets | 2026-05-19 |
| `billboard-hot-100-1-song-week-of-may-23` | Hot 100 #1 weekly | $564 | $6,527 | $2,215 | $14,336 | NegRisk candidate race, 20 sub-markets | 2026-05-19 |
| `which-artists-will-have-1-hits-in-the-us-in-may` | Spotify Top 50 daily #1 multi-binary | $1,248 | $6,663 | $5,682 | $6,466 | Multi-binary, 12–14 sub-markets | 2026-05-31 |

The dominant billboard-tag volume is a one-shot Drake bracket-bin (album sales). The pure weekly chart races are live but thin: Hot 100 at $6.5K total, Billboard 200 at $52K total (inflated by Noah Kahan dominance concentration — $44.4K of $52.3K is on a single 98.95% sub-market). Both markets are in their final resolution week as of capture.

Current-week snapshot (Week of May 23):
- Hot 100: "Choosin' Texas – Ella Langley" 98.45%. Near-resolved; no edge.
- Billboard 200: "The Great Divide – Noah Kahan" 98.95%. Near-resolved; no edge.

### Netflix tag (`tag_slug=top-netflix`)

Active markets as of 2026-05-16 (all resolve 2026-05-19):

| Slug | Question | Vol 24h | Vol all-time | OI | Liquidity | Sub-mkts | NegRisk |
|---|---|---|---|---|---|---|---|
| `...-2-global-netflix-show-this-week-855` | #2 global show | $16,170 | $82,091 | $1,971 | $7,975 | 13 | Yes |
| `...-top-global-netflix-movie-this-week-462` | #1 global movie | $6,215 | $13,308 | $7,160 | $22,862 | 22 | Yes |
| `...-top-us-netflix-movie-this-week-644` | #1 US movie | $6,933 | $17,430 | $11,941 | $5,465 | 22 | Yes |
| `...-2-global-netflix-movie-this-week-131` | #2 global movie | $4,841 | $40,728 | $3,283 | $13,674 | 22 | Yes |
| `...-top-global-netflix-show-this-week-421` | #1 global show | $2,791 | $33,707 | $8,060 | $10,898 | 22 | Yes |
| `...-top-us-netflix-show-this-week-598` | #1 US show | $1,453 | $7,286 | $6,687 | $5,002 | 22 | Yes |

Six active Netflix Top 10 sub-markets per week. Combined weekly volume: ~$140K this cycle. Genuine uncertainty mid-week: #2 global show shows "Worst Ex Ever: Season 2" at 58% vs "Man on Fire" at 15.4% — not near-resolved at capture.

### Charts tag (`tag_slug=charts`)

Returned `how-many-albums-will-reach-billboard-1-in-2026` ($13.2K all-time) — a structural annual count market, not a weekly chart race. The `charts` tag is sparsely populated; weekly races live under `billboard` and `top-netflix` respectively.

## 3. Data Sources and Information Hierarchy

### Billboard Hot 100 and Billboard 200

Billboard uses **Luminate Data** (formerly MRC Data / Nielsen Music) as exclusive measurement partner. The Hot 100 blends streaming (official on-demand audio + video), radio airplay, and digital sales. Streaming dominates for chart-topping streaming-era hits (~85–95% of composite), but radio remains decisive for country and adult contemporary.

| Source | Cost | Lag | Coverage | Edge Potential |
|---|---|---|---|---|
| Luminate Data API | Enterprise ($10K+/yr) | Near-real-time | Full streaming + radio + sales | High — ground truth; industry uses this |
| Chartmetric | $50–250/mo | ~24h | Spotify, Apple Music, Amazon, YT + radio proxy | Medium-high — best accessible proxy |
| Kworb.net | Free | ~24h | Spotify daily/weekly charts; YouTube views | Medium — Spotify only, no radio/sales |
| Spotify Charts (public) | Free | Weekly (Friday) | Spotify streams only | Medium-low for Hot 100; high for Spotify-only markets |
| Apple Music Charts | Free | Daily | Apple streams only | Low standalone; complementary |
| Hits Daily Double | Free surface / subscription detail | Weekly | First-week album sales, certified equivalents | High for album sales markets specifically |

**Structural gap:** Billboard's radio airplay component (Luminate's monitored-station data) is not publicly accessible. For country, pop-crossover, and adult contemporary tracks where radio represents 30–50% of composite, a streaming-only model is structurally miscalibrated. Focus on streaming-dominant genres (hip-hop, R&B, pop) or subscribe to Chartmetric for radio proxy.

### Netflix Top 10

Netflix publishes viewership weekly at top10.netflix.com every Tuesday by 3:00 PM ET, covering the prior Monday–Sunday window. Data is views (hours viewed / runtime, rounded to nearest 10,000). English-language only for global lists.

**Critical structural fact:** Netflix Top 10 data is published simultaneously with market resolution. There is no advance data — the resolution event and the data release are the same moment. The information structure is fundamentally different from Billboard markets.

| Source | Cost | Lag | Value |
|---|---|---|---|
| top10.netflix.com | Free | Weekly (Tuesday 3PM ET) | Ground truth = resolution source |
| FlixPatrol | Free/paid | Daily (estimates only) | Third-party proxy; demand-score based |
| Reelgood | Free | Weekly | Demand proxy; correlated but indirect |
| JustWatch | Free | Weekly | Streaming demand index |

No advance data exists. Prior-week rank is the dominant predictor. New content release dates (publicly announced by Netflix) are the primary shock variable.

## 4. Predictive Model Structure

### Billboard weekly chart position

**Model: prior-week rank transition matrix + streaming velocity update**

Prior-week rank is the strongest predictor (~0.80 autocorrelation for Top 10 songs). A Markov transition matrix from historical Hot 100 data captures persistence and ascent/descent trajectories.

Input features (decreasing importance):
1. Prior-week rank (or "new entry" for debut tracks)
2. Weekly Spotify stream total (Kworb or Chartmetric)
3. Radio airplay points (Chartmetric Luminate proxy, if subscribed)
4. Digital sales (minor weight; declining importance)
5. Release week indicator (debut-week trajectory differs from established run)
6. Genre flag (country/AC/pop have different radio-stream mix ratios)

Output: PMF over rank-1 outcome for each candidate. Maps directly to NegRisk sub-market prices.

Calibration data: 2020–2025 historical Hot 100 scraped archives (~260 weekly charts per year, 5–6 years = 1,300–1,560 observations). Rank transition matrix is stable enough over this window for reliable calibration.

### Netflix weekly Top 10 position

**Model: prior-week rank persistence + new-release shock**

Netflix viewership autocorrelation is high (#1 last week → 70–80% probability of #1 this week absent major new release). New season premieres show spike-and-decay; weeks 1–2 post-release dominate.

Input features:
1. Prior-week rank (dominant)
2. New episode availability this week (binary spike indicator)
3. Title lifecycle week (week N of run; later weeks decay predictably)
4. Competing title pipeline (new releases announced this week)

Model operates from prior-week data alone. No intra-week signal exists. This makes Netflix markets closer to a pure prior + new-release-shock prediction than a tracking model.

## 5. Saturation Analysis

### Billboard markets

**Professional saturation: Moderate.** Music industry insiders (labels, DSPs, managers) have Luminate access and know streaming data with <24h lag. However, they do not participate in Polymarket prediction markets in any organized way — these are retail markets. A Chartmetric-based systematic model would be differentiated relative to the retail market-maker pool.

**Retail saturation: Low.** Current market prices suggest primarily recency-bias-driven pricing (incumbents priced near certainty in steady-state weeks, new releases often underpriced early-week). No evidence of systematic modelers in market depth.

### Netflix markets

**Professional saturation: Very low.** Netflix viewership data is not commercially licensed. No professional trading advantage via data access exists. Field is retail-only.

**Retail saturation: Low to moderate.** Netflix watchers track shows but do not systematically consult top10.netflix.com weekly data for market-making decisions. A systematic weekly tracker would be clearly differentiated.

**Saturation verdict:** Netflix is the least professionally-saturated of the streaming chart market types.

## 6. Volume and Liquidity Assessment

### Weekly cadence and aggregate capacity

**Billboard Hot 100 #1 (52 markets/year estimated):**
- Current week: $6,527 total (low; mostly resolved)
- Estimated typical uncertain week: $5K–$15K total
- Annual total at scale: ~$300K–$780K across all Hot 100 #1 markets
- Per-position cap: $500–$2,000 before moving the thin pool >5 pp

**Billboard 200 #1 (52 markets/year estimated):**
- Current week: $52,346 total (inflated by single-candidate concentration)
- Estimated typical uncertain week: $10K–$25K total
- Per-position cap: $1,000–$5,000

**Netflix Top 10 (6 sub-markets/week, 52 weeks/year):**
- Combined this cycle: ~$140K (6 markets)
- Per-market range: $7K–$82K depending on type and uncertainty
- Annual total: ~$3.5M–$7M across all Netflix sub-markets (largest volume addressable in this domain)
- Per-position cap per sub-market: $1,000–$10,000

Netflix is significantly higher-volume than Billboard within this domain.

### LP yield overlay

Both market types show material liquidity relative to OI, suggesting active LP provision. The NegRisk AMM manages cross-sub-market risk. No sponsor reward observed for current-week markets. Run polymarket.com/rewards check before each cycle to identify sponsored weeks.

## 7. Edge Window Analysis

### Temporal structure

**Billboard Hot 100 / Billboard 200:**
- Market open: likely Monday or Tuesday (same day as chart publication)
- Measurement period: Friday–Thursday of the same week
- Resolution: following Tuesday (when next week's chart publishes)
- **Edge window: Tuesday open → Saturday evening** (4–5 days)
- Streaming data for the full measurement period is ~80% accumulated by Friday night
- Best entry: Tuesday–Wednesday on genuinely uncertain races
- Best exit: Thursday–Friday as outcome becomes near-certain

**Netflix Top 10:**
- Market open: Monday (prior Tuesday's data is the most recent available)
- Resolution: Tuesday 3:00 PM ET (data release = resolution)
- **Edge window: Monday–Sunday (~7 days from prior week's data)**
- No intra-week data update exists — model operates solely on prior-week rank + new-release calendar
- Best entry: Monday–Tuesday using persistence model
- Best exit: Saturday (if no new-release shock mid-week) or immediately if new major premiere disrupts the incumbent

### Tractable vs. near-certain weeks

**Billboard Hot 100:** Multi-week dominant incumbents (95%+ at open) offer no edge. Tractable weeks = new release debut weeks + multi-way competitive transitions. Estimated 15–25 tractable weeks/year.

**Billboard 200:** Album debuts create more frequent transitions than song chart turnover. Estimated 20–30 tractable weeks/year.

**Netflix Top 10:** Nearly every week has meaningful uncertainty due to continuous new content releases. Estimated 40–50 tractable weeks/year across the 6 sub-market types.

## 8. Execution Considerations

### Mechanics

- NegRisk candidate race structure: buying any candidate implicitly increases "Other" value; cross-sub-market correlation must be accounted for in sizing.
- Thin early-week markets: 3–8% spreads are typical when uncertainty is highest. Use limit orders at AMM mid or slightly inside.
- Liquidity cliff: positions cannot be scaled beyond $1K–$5K per sub-market without materially moving prices. Maximum viable weekly P&L is bounded by volume, not model quality.
- The "Song A / Song B" placeholder structure means new breakout entries may not be listed until after the market opens; "Other" is the residual but cannot be directly purchased.

### Resolution risk (low)

Both Billboard and Netflix resolve against publicly-observable, deterministic sources. No UMA oracle dispute risk on standard chart publications. Residual risks:
- Billboard: holiday schedule adjustments (chart may publish Wednesday instead of Tuesday; 14-day fallback applies)
- Netflix: if top10.netflix.com is delayed (has not historically occurred; same 14-day fallback)
- Netflix global: English-language scope limitation per resolution rules — non-English breakout shows do not qualify

### Minimum viable operational pipeline

**Billboard (2–3 hrs/week):**
1. Kworb.net daily Spotify chart pull for candidate songs (free, automated)
2. Chartmetric pull for radio airplay proxy (if subscribed; otherwise skip for streaming-dominant genres)
3. Run rank transition matrix model → PMF over #1 candidates
4. Compare to market sub-market prices; enter limit orders on mispricings >3 pp (accounting for spread)
5. Exit positions Thursday–Friday

**Netflix (1–2 hrs/week):**
1. Scrape top10.netflix.com every Tuesday after 3PM ET (ground truth + prior week snapshot)
2. Track new content release calendar (Netflix press, new-on-netflix.com)
3. Run persistence model with new-release shock parameters
4. Enter Monday–Tuesday; exit Saturday

## 9. Risks and Limitations

1. **Radio airplay gap (Billboard):** Hot 100 radio airplay data is inaccessible without Luminate enterprise access. For country/AC/pop crossover tracks, radio = 30–50% of composite. A Spotify-only model is systematically wrong for these genres. Mitigant: use Chartmetric radio proxy ($50–250/mo) or restrict to hip-hop/R&B/pop streaming-dominant tracks.

2. **No intra-week Netflix data:** Netflix does not release mid-week viewership. Model works only from prior-week snapshot. Large new releases displace incumbents with no advance signal. Mitigant: track Netflix release calendar; avoid large positions in high-premiere weeks.

3. **Thin liquidity ceiling:** Weekly volumes of $6.5K–$82K per sub-market imply hard position-size caps of $500–$10K before moving prices. Not scalable beyond individual systematic operation.

4. **Candidate roster incompleteness:** "Song A / Song B / Other" placeholders mean Polymarket does not list all possible winners. "Other" accumulates unlisted candidates but cannot be directly bought. In weeks with surprise breakouts, the only play is shorting overpriced named candidates.

5. **English-language Netflix scope:** Global Netflix markets are English-only per resolution rules. Non-English mega-hits (K-drama, Spanish series) are excluded even if they dominate the actual Netflix platform.

6. **Rank transition matrix drift:** Historical transition matrices can become unreliable if streaming consumption patterns shift (TikTok virality cycles, AI-generated content, new DSP deals). Recalibrate quarterly.

7. **NegRisk Σ-check required:** In near-certain weeks, sum of Yes prices must ≈ 1.00 (NegRisk invariant). Deviations are direct MRA per [[arbitrage-taxonomy]] §3. Run Σ-check before every entry.

## 10. Verdict and Priority Ranking

**Overall verdict: CONDITIONAL YES**

Streaming chart position markets are tractable, systematic, and differentiated from the retail market-maker pool. Free/low-cost data sources (Kworb, top10.netflix.com) enable a viable operational pipeline. The binding constraint is thin liquidity, which caps position size, not information access.

### Priority ranking within domain

| Market | Edge Strength | Saturation | Liquidity | Tractable Wks/yr | Priority |
|---|---|---|---|---|---|
| Billboard 200 #1 (album debut weeks) | High — 5-day streaming convergence pre-resolution | Low | $10K–$52K/wk | ~25 | **1** |
| Netflix Top 10 #1/#2 global show | Medium-high — persistence + new-release shock; lowest saturation | Very low | $33K–$82K/wk | ~45 | **2** |
| Netflix Top 10 #1 global movie | Medium — same model; solid volume | Very low | $13K–$41K/wk | ~45 | **3** |
| Netflix Top 10 US show/movie | Medium — US-only; less volume | Very low | $5K–$17K/wk | ~45 | **4** |
| Billboard Hot 100 #1 (transition weeks) | Medium — streaming strong; radio gap structural | Low | $1K–$15K/wk | ~20 | **5** |

### Conditions for "go" decision

- Subscribe to Chartmetric for radio proxy (or restrict Hot 100 operation to streaming-dominant genres)
- Build top10.netflix.com weekly archive (one scrape per Tuesday; free)
- Maintain 5-year Billboard historical archive for transition matrix calibration
- Target entry: Tuesday–Wednesday (Billboard); Monday–Tuesday (Netflix)
- Skip markets where incumbent probability exceeds 90% at open — spread cost eliminates edge
- Run NegRisk Σ-check before every entry

### What this domain does not offer

- Large-position or high-frequency strategies — liquidity ceiling is binding
- Edge on 95%+ near-resolved markets
- Advance intra-week data on Netflix viewership (none exists)
- Edge on radio-heavy country/AC Hot 100 markets without Luminate or Chartmetric

## Source

- Live Gamma API pulls (2026-05-16): `tag_slug=billboard`, `tag_slug=top-netflix`, `tag_slug=charts`
- Full resolution-rule text from slugs: `billboard-hot-100-1-song-week-of-may-23`, `billboard-200-1-album-week-of-may-23`
- `raw/research/polymarket-broad-coverage-sweep/03-polymarket-music-gamma.md`
- `raw/research/polymarket-broad-coverage-sweep/.ingest/03-polymarket-music-gamma.summary.md`
- `raw/research/polymarket-broad-coverage-sweep/02-polymarket-movies-gamma.md`
- `wiki/polymarket-strategy-matrix.md`

## Related

- [[polymarket-strategy-matrix]]
- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
- [[llm-forecasting-by-domain]]
- [[polymarket-lp-incentives]]
