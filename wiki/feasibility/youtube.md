# Feasibility — YouTube Creator Metrics

MrBeast metric markets (subscriber + total-view milestones, Day-1/Week-1 view brackets, mention markets) are fully modelable via free public YouTube Data API v3. **VIABLE — HIGH priority.** Densest YES cluster on Polymarket (58% tractability — highest of any vertical per [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]). Non-MrBeast creators either Twitch-primary (xQc, Forsen, Clavicular) or legal-outcome (Doherty). Live Gamma API 2026-05-16.

## Rubric (out of 20)

| Dimension | Score | Notes |
|---|---|---|
| Data availability | 5 | YouTube Data API v3 free, 10K units/day quota; Social Blade 90-day history; NoxInfluencer hourly tracker |
| Modeling tractability | 4 | Poisson/linear trajectory + lognormal Day-1 distribution + Beta-Binomial bracket; no LLM needed for milestones |
| Market depth/sizing | 2 | $2K–$28K all-time per MrBeast sub-market; $200–$500 per leg before moving market |
| Non-saturation | 4 | Social Blade public (theoretical moderate) but retail sophistication empirically low — 122.5B already exceeded but trades 99.6% not 100% |
| **Total** | **15/20** | YES |

## Top markets

| Rank | Event | Vol_24h | Vol_all | NegRisk | Tractability |
|---|---|---|---|---|---|
| 1 | MrBeast ___ billion views by May 31 | $4.0K | $19.0K | No | YES — channel API + Social Blade trajectory |
| 2 | What will MrBeast say in next video | $3.7K | $8.5K | No | PARTIAL — auto-caption pull post-upload |
| 3 | # views next MrBeast video day 1 | $3.1K | $8.8K | Yes | YES — lognormal + NoxInfluencer hourly |
| 4 | MrBeast ___ million subs by June 30 | $2.5K | $27.1K | No | YES — linear regression on Social Blade |
| 5 | MrBeast ___ billion views by June 30 | $2.0K | $9.3K | No | YES — same trajectory model |

12 active events under `tag_slug=youtube`; 9 MrBeast, 1 xQc/Forsen, 1 Doherty (legal), 1 Clavicular (Kick). 7 of 12 YES-tractable (58%).

## Data sources

| Source | Access | Endpoint / Notes |
|---|---|---|
| YouTube Data API v3 | Free, Google API key (no OAuth for public) | `channels.list(part=statistics,id=UCX6OQ3DkcsbYNE6H8uQQuVA)` = 1 unit; 10K/day quota |
| Social Blade | Free tier | Daily subscriber + view-count history; 90-day series builds growth-rate priors |
| NoxInfluencer | Free basic / paid | Hourly Day-1 view tracker for major channels; live MrBeast video tracker |
| youtube-transcript-api | Free (unofficial) | Auto-captions for mention markets; available 15–60min post-upload |

**Subscriber count caveat:** YouTube rounds public `subscriberCount` to 3 sig figs above 1,000. At MrBeast scale (~485M), ±500K ambiguity. Matters within last 1M of a milestone threshold. Resolution = channel page (rounded display), same as API. Apply conservative rounding buffer; prefer round-100M thresholds.

**Historical view-count:** API gives current only — no per-video historical series. Must poll + store locally. Social Blade fills channel-level historical.

**Excluded — YouTube Analytics API:** Channel-owner-only OAuth; cannot be used for third-party channels.

## Modeling spine

**Milestone / date-ladder (subscriber count by date):**
```
λ_daily = OLS on Social Blade 90-day daily subscriber gain
E[count(T)] = count(today) + λ · (T − today)
σ_trajectory = √(σ_regression² + σ_video_timing²)
P(hits M by T) = Φ((E[count(T)] − M) / σ_trajectory)
```
Intra-period update: daily API poll → Bayesian posterior on λ tightens. Milestones within 2σ of trajectory converge to near-certainty quickly.

**Bracket-bin Day-1 views (NegRisk):**
```
log(views_day1) ~ Normal(μ_genre, σ_genre)  # fit on last 15–20 MrBeast videos
P(bracket_i) = Φ(log(b_high); μ,σ) − Φ(log(b_low); μ,σ)
ΣP(bracket_i) = 1.00 enforced (NegRisk)
```
Real-time post-upload: NoxInfluencer hour-6 to hour-12 gives log-linear extrapolation to hour-24 within ±15%. Update bracket PMF accordingly — sharp convergence if NoxInfluencer pulled before market repricing.

**Mention market (say-Y-in-next-video):** Binary per phrase; base rate from historical videos. 28 sub-markets span high-base ("Prize" 76.5%) to niche ("Jet" 14.5%). Pre-video: base-rate modeling moderately predictive but content-type-dependent. Post-video: auto-caption pull = near-certain resolution within 60min of market maturity — execution-speed arb, not predictive edge.

## Structural-arb shape

- **NegRisk bracket Σ-check (Day-1 views):** ΣP(bracket_i) ≈ 1.00 mechanically enforced by NegRisk AMM. Σ deviations are mechanical MRA per [[arbitrage-taxonomy]].
- **Date-ladder monotonicity:** Across same-event multi-expiry legs (e.g., milestone by T1 vs T2), P(by T1) ≤ P(by T2). Inversions = direct Long MRA.
- **Subscriber-milestone monotonicity within event:** Ladder legs weakly decreasing as thresholds increase. Inversion = no-modeling arb.

## Microstructure regime

- **Spreads:** Sub-$10K all-time per sub-market = wide spreads on near-50% bins; tight (0.5–2%) on near-certain legs.
- **LP yield:** Near-certainty legs (>95%) have very narrow spreads — poor LP. Mid-range thresholds (e.g., 500M at 26%, 497M at 62%) have wider spreads — viable LP but maker rebates modest ($5–$50/wk at current volume).
- **Position cap:** $200–$500/leg before moving thin markets. Kelly f* ≈ 10% on 5–10% edge at p=0.70.

## Saturation

- **Theoretical:** Moderate. Social Blade public; any competitor can run same regression.
- **Empirical:** Low. Mispricing evidence (2026-05-16):
  - 122.5B views by May 31 trades $0.996 despite 122.5B already exceeded — participants not running live API polls.
  - 497M subscriber milestone at 62% — implies uncertainty inconsistent with 8M/mo gain from 485M with 45 days remaining; simple linear model gives >85%.
- **Sweet spot:** Individual operator with API + simple pipeline. Sub-markets average $2K–$8K all-time = too small for institutional quant desks.
- **Non-MrBeast (xQc speedrun):** Different model class (hazard/event-study); no YouTube API signal; esports community insiders more informed than retail.

## Risks

1. **Subscriber count rounding (±500K):** Model says 488M reached, channel page displays 487M → market resolves NO. Mitigate with rounding buffer; prefer round-100M thresholds.
2. **Video posting timing:** Day-1/Week-1 markets expire May 31 / June 30. MrBeast posts ~monthly → 5–15% probability of no video before expiry; resolves to lowest bracket. Priced in via lowest-bracket sub-market.
3. **Mention transcript accuracy:** Auto-captions 5–10% WER; higher for brand names ("Feastables"). Manual verification for high-stakes sub-markets.
4. **Creator lifecycle:** Platform ban / controversy-driven demonetization could interrupt trajectory. Low probability; non-zero tail.
5. **Gamma API only — Vercel checkpoint blocks SPA scraping.** Use Gamma API throughout pipeline.

## Decision-tree mapping

1. **Q1 YES-theme?** YES — densest YES cluster on Polymarket.
2. **Q2 Data source?** YES — YouTube Data API v3 (free, 10K/day) + Social Blade (free) + NoxInfluencer (free basic).
3. **Q3 Structural-arb?** YES — NegRisk Σ-check (Day-1 brackets) + monotonicity (ladder legs).
4. **Q4 Microstructure?** Thin spreads + LP available on mid-range threshold legs.

## Strategic priority

| Tier | Markets | Edge |
|---|---|---|
| HIGH | MrBeast subscriber + total-view milestones | Trajectory model; 8M/mo prior |
| MEDIUM | MrBeast Day-1/Week-1 view bracket | Lognormal + NoxInfluencer hourly post-upload |
| LOW-MED | MrBeast mention market | Pre-video weak; post-video = execution-speed arb |
| LOW | xQc speedrun, Doherty legal, Clavicular Kick | Off-YouTube or legal-outcome |

## Open follow-ups

1. Instrument YouTube Data API v3 subscriber/view polling loop.
2. Pull Social Blade 90-day history for MrBeast channel.
3. Build Poisson/linear trajectory for June 30 subscriber + view milestones.
4. Validate vs market: 500M sub at 26%, 497M at 62% — model expects >85% — flag if model deviates >10pp.
5. NoxInfluencer integration for Day-1 bracket update post-upload.
6. Monitor non-MrBeast for YouTube-metric variant listings (currently absent).

## Source

- `raw/feasibility/youtube/summary.md` (2026-05-16)
- `raw/research/polymarket-broad-coverage-sweep/04-polymarket-youtube-gamma.md`
- Gamma API live pulls: `tag_slug=youtube`, `tag_slug=mrbeast`
- Slugs `will-mrbeast-hit-million-subscribers-by-june-30`, `will-xqc-beat-forsens-minecraft-speedrun-record-by`

## Related

- [[polymarket-strategy-matrix]]
- [[mention-markets]]
- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
- [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]
- [[polymarket-microstructure]]
- [[llm-forecasting-by-domain]]
- [[feasibility-review]]
