# Feasibility — Streaming Chart Positions

Billboard Hot 100 / Billboard 200 weekly #1 + Netflix Top 10 weekly position. **Conditional YES:** Billboard tractable via Kworb/Chartmetric pipeline; Netflix tractable via persistence-plus-shock model. Binding constraint is thin liquidity (not information access). Saturation is professional-low / retail-low to moderate. Live Gamma API 2026-05-16.

## Rubric (out of 20)

| Dimension | Score | Notes |
|---|---|---|
| Data availability | 3/4 | Kworb (free Spotify), top10.netflix.com (free; = resolution), Chartmetric paid for radio proxy |
| Modeling tractability | 3/4 | Markov rank-transition + persistence model + new-release shock; radio gap for country/AC |
| Structural arb | 2/4 | NegRisk Σ-check only; near-certain weeks dominate; thin transition weeks |
| Liquidity | 2/4 | Hot 100 $5–15K/wk uncertain; Billboard 200 $10–25K; Netflix $5–82K per sub-market |
| Non-saturation | 4/4 | Netflix lowest professional saturation of any chart type (no commercial license exists) |
| **Total** | **14/20** | Conditional YES |

## Top markets (priority order)

| Rank | Slug | Type | Vol_24h | Vol_all | Notes |
|---|---|---|---|---|---|
| 1 | `drake-iceman-first-week-album-sales` | NegRisk 8-bracket | $129K | $182K | One-shot bracket-bin; album-debut sales |
| 2 | `billboard-200-1-album-week-of-may-23` | NegRisk 21-cand race | $7K | $52K | Mostly Noah Kahan concentration |
| 3 | `top-global-netflix-show-this-week-855` (#2) | NegRisk 13-cand | $16K | $82K | Mid-week uncertainty: WEE2 58%, MoF 15% |
| 4 | `top-global-netflix-movie-this-week-462` (#1) | NegRisk 22-cand | $6K | $13K | $7K OI |
| 5 | `billboard-hot-100-1-song-week-of-may-23` | NegRisk 20-cand | $0.6K | $7K | Ella Langley 98.45% — near-resolved |
| 6 | `top-us-netflix-movie-this-week-644` (#1) | NegRisk 22-cand | $7K | $17K | US-only scope |

Six active Netflix sub-markets/week, combined ~$140K weekly. Annual: Netflix ~$3.5M–$7M total; Billboard 200 ~$300K–$780K; Hot 100 ~$300K–$780K.

## Data sources

### Billboard (Hot 100 + Billboard 200)

| Source | Cost | Lag | Edge |
|---|---|---|---|
| Luminate Data API | Enterprise ($10K+/yr) | Near-real-time | Ground truth (industry uses this) |
| Chartmetric | $50–250/mo | ~24h | Spotify+Apple+Amazon+YT + radio proxy |
| Kworb.net | Free | ~24h | Spotify daily/weekly + YouTube views |
| Spotify Charts (public) | Free | Weekly Fri | Spotify-only — strong for streaming-dominant genres |
| Apple Music Charts | Free | Daily | Complementary |
| Hits Daily Double | Free surface / paid detail | Weekly | First-week album sales |

**Structural gap:** Billboard radio airplay (Luminate monitored stations) is non-public. Radio = 30–50% of Hot 100 composite for country/AC/pop-crossover. Streaming-only model is structurally miscalibrated for those tracks — restrict to hip-hop/R&B/pop streaming-dominant OR subscribe to Chartmetric.

### Netflix Top 10

- `top10.netflix.com` — free, weekly Tuesday 3PM ET, Mon–Sun viewership window. **Data release = market resolution.** No advance intra-week signal exists.
- FlixPatrol/Reelgood/JustWatch — demand-proxy, correlated but indirect.
- Netflix release calendar — primary shock variable (new-season premieres).
- Scope: English-language only for global lists per resolution rules.

## Modeling spine

**Billboard weekly rank:**
```
P(rank_1 = candidate_i) from rank-transition matrix M (estimated on 2020–2025 Hot 100; 1,300+ obs)
features: prior-week rank, weekly Spotify streams, radio points (if subscribed), digital sales (minor),
          release-week indicator, genre flag (radio-mix ratio)
```
Prior-week rank ~0.80 autocorrelation for Top 10. Output PMF maps to NegRisk sub-markets directly.

**Netflix Top 10:**
```
P(rank_1 this week | prior week, new releases) = persistence(0.70–0.80) × (1 − shock_indicator) + shock_p
shock_indicator = 1 if major new premiere this week
title lifecycle: week N decay (spike-and-decay, weeks 1–2 dominate)
```
Operates from prior-week data alone. No intra-week update. Closer to pure prior + shock prediction than tracking model.

## Structural-arb shape

**NegRisk Σ-check:** Σ Yes ≈ 1.00 across sub-markets enforced. Run before every entry per [[arbitrage-taxonomy]] §3.

**No date-ladder structure here.** Cross-week candidate-race events don't form a monotone ladder; no structural arb beyond Σ-check.

## Microstructure regime

- **Newly-opened week:** Open Monday–Tuesday; 3–8% spreads typical when uncertainty highest.
- **Edge window:** Billboard Tue open → Sat (~5 days; data ~80% by Fri night). Netflix Mon–Sun (~7 days; no intra-week).
- **Tractable weeks:** Hot 100 ~15–25/yr (debut + transition); Billboard 200 ~20–30/yr (album debuts); Netflix ~40–50/yr (continuous new content drives weekly uncertainty).
- **Skip rule:** Markets where incumbent P>0.90 at open — spread cost eliminates edge.

## Saturation

- **Billboard professional:** Moderate. Labels, DSPs, managers have Luminate access but do not organize Polymarket trading. Chartmetric-based model differentiates relative to retail market-maker pool.
- **Billboard retail:** Low. Pricing primarily recency-bias-driven (incumbents near certainty, debuts often underpriced).
- **Netflix professional:** Very low. Viewership data not commercially licensed; no professional trading advantage exists. Field is retail-only.
- **Netflix retail:** Low-moderate. Watchers track shows but don't systematically consult Tuesday data for market-making.
- **Verdict:** Netflix is the least professionally-saturated of the streaming chart types.

## Decision-tree mapping

1. **Q1 YES-theme?** Both Billboard and Netflix: YES.
2. **Q2 Data source?** YES — Kworb (free), top10.netflix.com (free + = resolution), Chartmetric for radio proxy if needed.
3. **Q3 Structural-arb?** NegRisk Σ-check only; no ladder monotonicity.
4. **Q4 Microstructure?** Thin candidate-race spreads early-week; "Other" residual cannot be directly bought.

## Risks / limitations

1. **Radio airplay gap (Billboard):** Hot 100 radio non-accessible without Luminate. 30–50% composite for country/AC/pop crossover. Restrict to streaming-dominant genres or pay Chartmetric.
2. **No intra-week Netflix data:** Model operates from prior-week snapshot only. New releases displace incumbents with no advance signal.
3. **Liquidity ceiling:** $500–$10K per sub-market caps deployable size. Not scalable beyond systematic individual operation.
4. **Candidate roster incompleteness:** "Song A / Song B / Other" — surprise breakouts not listable; "Other" residual cannot be directly bought.
5. **English-language Netflix scope:** Global Netflix markets English-only per resolution. K-drama / Spanish mega-hits excluded.
6. **Rank transition matrix drift:** Recalibrate quarterly (TikTok cycles, new DSP deals).
7. **Resolution risk:** Holiday schedule shifts (Billboard 14-day fallback); low historically.

## Priority within domain

| Market | Edge | Saturation | Liquidity | Tractable wks/yr | Priority |
|---|---|---|---|---|---|
| Billboard 200 #1 (album debut weeks) | High | Low | $10–52K | ~25 | **1** |
| Netflix Top 10 #1/#2 global show | Med-high | Very low | $33–82K | ~45 | **2** |
| Netflix Top 10 #1 global movie | Med | Very low | $13–41K | ~45 | **3** |
| Netflix Top 10 US show/movie | Med | Very low | $5–17K | ~45 | **4** |
| Billboard Hot 100 #1 (transition weeks) | Med | Low | $1–15K | ~20 | **5** |

## Conditions for "go"

- Subscribe to Chartmetric for radio proxy OR restrict Hot 100 to streaming-dominant genres.
- Build top10.netflix.com weekly archive (one Tuesday scrape).
- Maintain 5-year Billboard historical archive for transition matrix calibration.
- Entry: Tue–Wed (Billboard); Mon–Tue (Netflix). Skip markets where incumbent P > 0.90 at open.
- Run NegRisk Σ-check before every entry.

## Open follow-ups

1. Operational pipeline build: Kworb daily pull + top10.netflix.com Tuesday scrape + rank-transition matrix calibration on 5-year Hot 100 archive.
2. Brier-score backtest of Markov model vs market mid on closed weekly events.
3. Chartmetric eval: cost-benefit of $50–250/mo subscription for radio proxy.
4. Sponsor-reward sweep before each weekly cycle — `polymarket.com/rewards` check.

## Source

- `raw/feasibility/streaming-charts/summary.md` (2026-05-16)
- Gamma API live pulls: `tag_slug=billboard`, `tag_slug=top-netflix`, `tag_slug=charts`
- Slugs `billboard-hot-100-1-song-week-of-may-23`, `billboard-200-1-album-week-of-may-23`

## Related

- [[polymarket-strategy-matrix]]
- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
- [[llm-forecasting-by-domain]]
- [[polymarket-lp-incentives]]
- [[feasibility-review]]
