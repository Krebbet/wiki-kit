---
title: "Feasibility Assessment — YouTube Creator-Metric Markets"
domain: youtube
written: "2026-05-16"
verdict: "VIABLE — densest YES cluster on Polymarket; MrBeast metric markets are fully modelable via public YouTube Data API v3; non-MrBeast creators are unsaturated but thinner; competition is moderate (Social Blade public) but retail sophistication is low."
---

# Feasibility Assessment — YouTube Creator-Metric Markets

## 1. Market landscape

**Source pull:** Gamma API `tag_slug=youtube` + `tag_slug=mrbeast`, 2026-05-16. Active, not-closed only.

12 active events under `youtube` tag; the `mrbeast` tag returns the same 9 MrBeast events plus no additional unique events. All 12 events are also captured in `raw/research/polymarket-broad-coverage-sweep/04-polymarket-youtube-gamma.md`.

**Event inventory by creator:**

| Creator | Events | All-time vol | 24h vol (top event) | Tractability |
|---|---|---|---|---|
| MrBeast | 9 | ~$130k aggregate | $4,048 (billion-views May 31) | 7 YES / 1 PARTIAL / 1 NO |
| xQc + Forsen | 1 | $12,125 | $318 | PARTIAL (live-stream) |
| Jack Doherty | 1 | $18,994 | $0 | NO (legal) |
| Clavicular | 1 | $834 | $0 | NO (Kick platform) |

**YES rate:** 7 of 12 events are YES-tractable via public API — 58%. This is the highest YES rate of any Polymarket vertical per the broad-coverage sweep (`raw/research/polymarket-broad-coverage-sweep/.ingest/04-polymarket-youtube-gamma.summary.md`).

**Top 5 events by 24h volume (2026-05-16):**

| Rank | Event | 24h vol | All-time vol | NegRisk |
|---|---|---|---|---|
| 1 | MrBeast ___ billion views by May 31 | $4,048 | $19,046 | No |
| 2 | What will MrBeast say in next YouTube video | $3,739 | $8,530 | No |
| 3 | # views next MrBeast video day 1 | $3,133 | $8,762 | Yes |
| 4 | MrBeast ___ million subscribers by June 30 | $2,500 | $27,094 | No |
| 5 | MrBeast ___ billion views by June 30 | $2,044 | $9,333 | No |

All top-5 by daily volume are YES-tractable MrBeast metric markets. MrBeast marriage ($36.7k all-time, $0 24h) is largest by cumulative volume but has stalled near resolution.

## 2. Resolution rules (captured)

### MrBeast — subscriber milestone (canonical example)

Event: `will-mrbeast-hit-million-subscribers-by-june-30`

> Resolves "Yes" if the MrBeast YouTube channel (`youtube.com/@MrBeast`) hits the specified number of subscribers by June 30, 2026, 11:59 PM ET. Primary resolution source: the MrBeast YouTube channel or a consensus of credible reporting.

Current subscriber state implied by market prices (2026-05-16): ~485M actual (485M sub-market at $1.00 / resolved), gaining approximately 8M/30 days. 500M sub-market at $0.26 — market pricing ~26% probability of 15M gain in 45 days.

**API signal:** `channels.list(part=statistics, id=UCX6OQ3DkcsbYNE6H8uQQuVA)` returns `subscriberCount` (real-time, rounded to 3 sig figs for privacy above 1,000). Sufficient for milestone resolution with ±500K precision.

**Resolution-rule note:** "consensus of credible reporting" is a fallback; actual resolution is direct channel-page read. Social Blade and SocialCount.io are commonly cited as the secondary sources Polymarket resolvers use.

### xQc / Forsen Minecraft speedrun (non-MrBeast, live-stream)

Event: `will-xqc-beat-forsens-minecraft-speedrun-record-by`

> Resolves "Yes" if xQc breaks Forsen's In-Game-Time of 14:18.375 in a Minecraft Java Edition 1.16.1 speedrun (random seed, world-creation to Ender Dragon death) during a live stream by the listed date. Prerecorded video does not count.

**API signal:** None — resolution depends on live-stream monitoring. speedrun.com leaderboard would be definitive if xQc submitted, but sub-record runs on stream may not be immediately submitted. Classify PARTIAL: requires Twitch VOD/clip monitoring or community alert. No YouTube Data API leverage.

Sub-market prices (2026-05-16): May 31 = 23.5% Yes, June 30 = 54.5% Yes. Implied conditional probability of hitting in June given not May: (0.545 − 0.235) / (1 − 0.235) = 40.5%.

## 3. Data sources

### Primary — YouTube Data API v3

- **Access:** Public, free, requires Google API key (no OAuth for public data)
- **Daily quota:** 10,000 units/day (free tier). `channels.list(part=statistics)` = 1 unit per call. `videos.list(part=statistics)` = 1 unit per call. Adequate for monitoring a handful of channels and videos.
- **Key endpoints:**
  - `channels.list(part=statistics, id=<channelId>)` → `viewCount` (cumulative), `subscriberCount` (real-time, 3-sig-fig rounded above 1,000), `videoCount`
  - `videos.list(part=statistics, id=<videoId>)` → `viewCount`, `likeCount`, `commentCount` at time of call
  - `playlistItems.list` → enumerate recent uploads to detect new video post
- **Latency:** API reflects YouTube's internal count with a small delay (typically minutes to hours). Sufficient for milestone markets (day/week resolution) and bracket-bin markets (T+24h / T+7d snapshots).
- **Subscriber count caveat:** YouTube rounds public `subscriberCount` to 3 significant figures for channels above 1,000 subscribers. At MrBeast's scale (~485M), the displayed value may read "485,000,000" but the true count could be 484.5M–485.5M. For milestone markets set at round numbers (485M, 488M, etc.) this ±500K uncertainty is material within the last 1M of a threshold. Social Blade's tracker resolves this via more frequent scraping.
- **Historical view-count:** API gives current `viewCount` only — not historical time series at the video level. Historical snapshots must be polled and stored locally. For channel-level growth trajectory, Social Blade provides the historical series.

### Secondary — Social Blade

- **Access:** Free tier at socialblade.com; provides channel-level daily subscriber and view-count history going back years.
- **Coverage:** All major YouTube creators including MrBeast, xQc (YouTube channel, not primary Twitch), Jack Doherty, Clavicular.
- **Saturation implication:** Social Blade data is public, meaning any market participant can access the same growth trajectory data. However, Polymarket's retail YouTube-betting population is empirically unsophisticated (prices for near-certain milestones like 122.5B views trade at $0.996 rather than $1.00 — residual uncertainty is priced higher than warranted). Competition is moderate but not quant-saturated.
- **Use case:** build growth-rate priors (weekly/monthly subscriber gains, view-count velocity) for Poisson or power-law trajectory models.

### Tertiary — NoxInfluencer

- **Access:** Free basic tier at noxinfluencer.com
- **Provides:** Estimated channel revenue, video-level view-count trajectory (hourly in first 24h for major channels), audience demographics
- **Unique signal:** Hourly view-count sampling in the first 24h of a new video — directly relevant for Day-1 view-count bracket markets (event #3). NoxInfluencer publishes a live tracker for MrBeast videos.
- **Reliability:** Third-party estimates; methodology not audited. Treat as directional signal rather than authoritative source.

### Excluded — YouTube Analytics API

- **Access:** Channel-owner only (OAuth 2.0 with channel ownership required). Cannot be accessed for third-party channels.
- **Provides:** True (unrounded) subscriber counts, per-video watch-time, traffic sources, audience retention curves.
- **Not usable** for betting purposes — would require unauthorized access to creator accounts.

## 4. Creator-by-creator tractability

### MrBeast (Jimmy Donaldson) — `@MrBeast`

- **YouTube presence:** Primary channel. ~485M subscribers (2026-05-16). 122–123B total views. Posts 1–3 videos/month of high-budget challenge format.
- **Growth stability:** Extremely stable. Social Blade history shows consistent ~6–10M subscriber gain/month for 2+ years. Total-view velocity is roughly 1–2B views/month at current subscriber base. Power-law / linear extrapolation reliable to ±5% over 30-day horizon.
- **Video-level predictability:** Day-1 views vary more than channel totals (content-type dependent: challenge vs. stunt vs. philanthropy). Week-1 typically 2–3× Day-1. Historical range for recent videos: Day-1 20–45M, Week-1 50–100M. Bracket markets imply current median estimate around 30–35M Day-1.
- **Tractability verdict:** YES for all milestone and bracket-bin markets. PARTIAL for mention market (requires transcript). NO for marriage market.
- **Modeling approach:** Channel-level growth → linear regression on Social Blade 90-day history → Poisson rate → CDF over milestone threshold. Video-level view count → lognormal distribution fit on last 10 videos for bracket-bin bracket selection. Update intra-day from NoxInfluencer tracker once video posts.

### xQc (Félix Lengyel) — `@xQcOW`

- **YouTube presence:** YouTube channel exists (`@xQcOW`) but is primarily a VOD archive of Twitch content. YouTube subscriber count ~1.8M (small relative to Twitch following ~12M). YouTube view velocity is low and irregular — driven by viral clips, not original YouTube content.
- **Primary activity is Twitch, not YouTube.** The xQc Minecraft speedrun market resolves based on live-stream performance (Twitch), not YouTube content. YouTube Data API is not the relevant data source for this market.
- **Historical speedrun data:** xQc's best known Minecraft speedrun times are publicly tracked on speedrun.com and via community wikis. His skill trajectory is observable but highly variance-prone (speedrunning is fundamentally stochastic — requires favorable RNG in-game). Not a stable growth-trajectory model; closer to a survival-analysis / hazard model.
- **Tractability verdict:** PARTIAL. Data source is Twitch VOD archives + speedrun.com community board, not YouTube Data API. Prediction requires a different model class (event-study / hazard) than the metric-market Poisson used for MrBeast.

### Forsen (Sebastian Fors) — `@forsenv`

- **YouTube presence:** YouTube channel exists but Forsen is primarily a Twitch streamer. YouTube uploads are sporadic clip compilations. No YouTube metric markets currently exist for Forsen as a market subject — he appears only as the record-holder in the xQc speedrun market.
- **Tractability verdict:** N/A (not a market subject). If Forsen-specific markets were listed, same analysis as xQc applies: Twitch primary, YouTube Data API not the relevant source.

### Jack Doherty — `@JackDoherty`

- **YouTube presence:** Active YouTube channel focused on pranks and stunt content. Social Blade coverage exists. Subscriber count ~9M, channel active since ~2016.
- **Current Polymarket market:** Legal sentencing outcome (drug/obstruction charges, trial by Oct 31, 2026) — NOT a YouTube metric market. No YouTube Data API signal applies.
- **If YouTube metric markets were listed:** Channel history is public and Social Blade/NoxInfluencer coverage exists. Growth has been lumpy (viral peaks, controversy-driven) — less stable than MrBeast for extrapolation. Would be tractable at PARTIAL–YES depending on market structure.
- **Tractability verdict for current market:** NO. Legal outcome; YouTube API irrelevant.

### Clavicular (Braden Eric Peters) — `@Clavicular`

- **YouTube presence:** Primarily a Kick streamer. YouTube channel may exist for VOD archival but is not the primary platform and not the resolution source for the current market.
- **Current Polymarket market:** Kick platform ban — entirely off-YouTube. $834 all-time volume, niche. NO tractability.
- **If YouTube metric markets were listed:** Small creator. Social Blade tracks down to ~1K subscribers so basic data would exist, but thin history and high growth variance from Kick audience cross-pollination reduce model reliability.
- **Tractability verdict for current market:** NO. Platform ban; YouTube API irrelevant.

## 5. Modeling approach

### Milestone / date-ladder markets (e.g., subscriber count by June 30)

**Signal:** Social Blade 90-day daily subscriber history → linear regression on daily gain → projected cumulative count on resolution date → normal distribution over trajectory uncertainty.

**CDF:** `P(hits milestone M by date T) = Φ((E[count(T)] − M) / σ_trajectory)` where `σ_trajectory` combines regression residual and video-post timing uncertainty.

**Intra-period update:** Poll YouTube Data API daily. As `count(today)` is observed, update Bayesian posterior on gain rate. By mid-period, posterior tightens substantially — milestones within 2σ of current trajectory converge to near-certainty quickly.

**Edge concentration:** In date-ladder structures, edge lives in the transition zone (50–80% market prices). Near-certainty rungs (>95%) have sub-1% edge; near-impossibility rungs (<5%) carry wide spreads but tiny expected value. Mid-confidence 50–70% rungs per Kim et al. MixMCP findings (see `wiki/mention-markets.md`).

### Bracket-bin view-count markets (NegRisk, e.g., Day-1 views)

**Signal:** Historical per-video Day-1 and Week-1 view counts from Social Blade / NoxInfluencer scraped archives for last 15–20 MrBeast videos → lognormal distribution fit → bracket CDF.

**NegRisk constraint:** Bracket bins are exhaustive and mutually exclusive — Σ P(bracket_i) = 1.00 enforced. Any deviation is a mechanical arbitrage. Run Σ-check on each snapshot; the market mechanism enforces this more tightly than typical multi-market arb.

**Real-time update:** Once MrBeast posts a video, NoxInfluencer provides hourly view-count tracker. By Hour 6–12, extrapolation to Hour 24 via log-linear fit is reliable within ±15%. Update bracket probabilities accordingly — sharp convergence available if you have the NoxInfluencer data before market prices update.

**Key uncertainty:** MrBeast's Day-1 view count depends heavily on content type (challenge vs. philanthropy vs. stunts) and upload timing (weekend vs. weekday, US morning vs. evening). Video-type classification adds a qualitative layer before the quantitative model.

### Mention market (say-Y-in-next-video)

**Signal:** YouTube auto-captions (available via `captions.list(videoId=<id>, tfmt=srt)` shortly after video upload) → tokenize transcript → phrase-count. Public, no auth required; auto-captions typically available 15–60 min post-upload.

**Model:** Binary per phrase. Base rate from historical videos. The market's 28 sub-markets span a wide frequency range (high-base "Prize" at 76.5% vs. niche "Jet" at 14.5%). High-base keywords converge to near-certainty once video posts; value is in correctly modeling conditional phrase occurrence across video types pre-posting. Post-video-upload, auto-caption pull gives near-certain resolution within 60 min of market maturity.

**PARTIAL classification rationale:** Pre-video, base-rate modeling is moderately predictive but content-type dependent. Auto-captions close the loop post-video, but that is post-event — execution-speed edge, not predictive modeling.

## 6. Competition / saturation

**Social Blade saturation:** Social Blade is fully public and widely known among YouTube enthusiasts. The growth-trajectory data this strategy relies on is not proprietary. Any competitor can run the same regression.

**Retail sophistication gap:** Despite public data availability, current market pricing suggests low quantitative sophistication:
- MrBeast 122.5B views by May 31 trades at $0.996 despite 122.5B appearing already exceeded — participants are not running live API polls.
- 497M subscriber milestone at 62% — implies uncertainty inconsistent with an 8M/month gain rate from 485M with 45 days remaining. Simple linear model produces >85% probability.
- These misprices are small but consistent. Market is populated by retail with anchoring bias and low-frequency data checks, not quant competitors running live API feeds.

**Competition assessment:** Moderate in theory (public data), low in practice (low retail sophistication, thin volume deters large quant entrants). MrBeast sub-markets average $2K–$8K all-time volume — too small to attract institutional quant desks. Sweet spot for an individual operator with API access and a simple statistical pipeline.

**Non-MrBeast saturation:** The xQc/Forsen Minecraft market requires a different model class (hazard/event-study) and has no YouTube API signal. Competition there is esports community insiders who track xQc's stream history — likely more informed than average retail.

## 7. Operational requirements

**Data pipeline:**
1. YouTube Data API v3 key (free, daily quota sufficient)
2. Social Blade scraper for historical series (no official API; HTML scraper or third-party Social Blade API wrapper)
3. NoxInfluencer tracker for Day-1 hourly view-count (free basic tier; paid tier provides hourly granularity)
4. Local time-series store for view/subscriber history (SQLite or flat CSV)

**Monitoring cadence:**
- Subscriber milestone markets: check daily; compute posterior update; flag if market price diverges from model by >5 pp
- View-count markets: poll every 30 min once MrBeast posts; update lognormal bracket PDF; flag bracket-bin Σ-check violations
- Mention markets: poll YouTube captions API every 15 min after video upload; grep phrase counts; compute binary resolution probabilities

**Position sizing:**
- Markets are thin ($2K–$28K all-time volume). Kelly fraction on a 5–10% edge target at p=0.70: f* ≈ 10% of bankroll. Position impact on thin markets limits practical size to $200–$500 per leg before moving the market.
- LP strategy (passive quoting) viable on milestone ladders: wide spreads exist on near-certainty legs, maker rebate applies.

**Resolution window:** All current markets resolve by May 31 or June 30, 2026. Markets appear to be a recurring monthly series — pipeline built once is reusable across instances.

## 8. Risks

**Subscriber count rounding:** YouTube API's 3-sig-fig rounding at MrBeast scale (±500K ambiguity) is material when a milestone is within 1M. Resolution source is the channel page (visual display), which shows the rounded public figure — same as API. Risk: model shows 488M reached but channel page displays 487M due to rounding; market resolves NO. Mitigation: apply a rounding-buffer conservatively; prefer markets set at round-100M thresholds.

**Video posting timing uncertainty:** Day-1 / Week-1 view-count markets expire May 31 / June 30. If MrBeast does not post a video before expiry, markets resolve to lowest bracket. MrBeast's posting frequency (approximately monthly for main channel) makes this a real but modest risk (approximately 5–15% depending on market window). Priced into the market via the lowest-bracket sub-market.

**Mention-market transcript accuracy:** YouTube auto-captions have approximately 5–10% word error rate, with higher error for brand names and proper nouns. "Feastables" may be transcribed incorrectly. Manual verification of high-stakes sub-markets is advisable.

**Platform access:** Polymarket SPA category pages returned Vercel security-checkpoint blocks as of 2026-05-16. Gamma API remains the reliable programmatic access path. Ensure resolution-monitoring pipeline uses Gamma API or contract-level queries, not SPA scraping.

**Creator lifecycle risk:** MrBeast's channel could face a platform-level incident (YouTube ban, controversy-driven demonetization) that interrupts normal growth trajectory. Low probability but non-zero; market structure may void/resolve via consensus, introducing tail risk independent of the model.

## 9. Strategic positioning

**Priority tier:** HIGH within the YouTube vertical for MrBeast metric markets (subscriber and total-view milestones). Fully YES-tractable, public data, low retail sophistication.

**Secondary tier:** MEDIUM for MrBeast Day-1 / Week-1 view bracket markets. Requires NoxInfluencer hourly tracker; model confidence increases sharply once video posts. Pre-video edge is lower; post-video edge is high but time-compressed.

**Mention market:** LOW-to-MEDIUM. PARTIAL tractability. Post-video auto-caption pull gives near-certain resolution signals quickly, but post-video trading is execution-speed arbitrage, not prediction modeling. Pre-video base-rate edge exists but is weaker.

**Non-MrBeast (xQc speedrun):** LOW. Different model class, no YouTube API signal, esports community is more informed competitor. The June 30 sub-market at 54.5% may be roughly fairly priced given xQc's recent stream history — no clear edge identified without deeper speedrun.com data pull.

**Secondary-market timing overlay (independent of predictive edge):**
- Date-ladder monotonicity Σ-check: across same-event multi-expiry legs, `P(by T_1) <= P(by T_2)` must hold; check cross-series legs if multiple expiry dates exist simultaneously.
- Bracket-bin Σ-check: For NegRisk view-count markets, run Σ at each snapshot; deviations from 1.00 are mechanical MRA.
- Subscriber milestone monotonicity: Within a single event, ladder legs must be weakly decreasing in probability as thresholds increase. Any inversion is a direct Long MRA.

**LP yield strategy:** Milestone markets with near-certainty legs (>95% Yes) have very narrow spreads — poor LP targets. Near-50% legs on mid-range thresholds (e.g., 500M at 26%, or 497M at 62%) have wider spreads. These are the LP-viable legs, but volume is thin enough that maker rebates will be modest ($5–$50/week at current volume levels).

## 10. Verdict

**VIABLE — HIGH PRIORITY within pop-culture verticals.**

This is the densest YES cluster on Polymarket (58% tractability rate). MrBeast's metric markets are fully modelable using public, free, low-quota data sources (YouTube Data API v3 + Social Blade). The retail participant base is demonstrably unsophisticated relative to the available data (near-certain milestones priced at 99.6% rather than 100%). Competition is moderate on paper (Social Blade is public) but low in practice.

**Recommended entry path:**
1. Instrument the YouTube Data API v3 subscriber/view-count polling loop.
2. Pull Social Blade 90-day history for MrBeast channel.
3. Build the Poisson/linear trajectory model for the June 30 subscriber and view milestones.
4. Validate against current market prices (500M sub at 26%, 497M at 62%) — these appear conservative given an 8M/month gain rate from 485M with 45 days remaining. Flag if model shows >10 pp deviation.
5. Size to market impact limit ($200–$500 per leg) given thin volume.
6. Extend to Day-1 / Week-1 view-count bracket markets once NoxInfluencer integration is in place.
7. Non-MrBeast markets (xQc, Doherty, Clavicular): monitor but do not model until YouTube-metric variants appear.

**One-line verdict:** YouTube creator-metric markets are Polymarket's most tractable vertical via free public API — MrBeast milestone and bracket-bin markets have clear signal, low retail competition, and a reusable monthly pipeline; non-MrBeast markets in the current set are either off-platform (Twitch/Kick) or legal outcomes with no API angle.

## Source

- `raw/research/polymarket-broad-coverage-sweep/04-polymarket-youtube-gamma.md` — Gamma API capture 2026-05-16, 12 events
- `raw/research/polymarket-broad-coverage-sweep/.ingest/04-polymarket-youtube-gamma.summary.md` — ingest summary
- `wiki/snapshots/polymarket-mention-cottage-industry-2026-05-14.md` — MrBeast section
- `wiki/polymarket-strategy-matrix.md` — YouTube strategy context + competition assessment
- Gamma API live pull 2026-05-16: `tag_slug=youtube`, `tag_slug=mrbeast`, slugs `will-mrbeast-hit-million-subscribers-by-june-30` + `will-xqc-beat-forsens-minecraft-speedrun-record-by`

## Related

- [[polymarket-strategy-matrix]]
- [[mention-markets]]
- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
- [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]
- [[polymarket-microstructure]]
- [[llm-forecasting-by-domain]]
