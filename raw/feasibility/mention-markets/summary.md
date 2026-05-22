---
theme: "Mention markets"
slug: "mention-markets"
assessed_on: "2026-05-16"
schema_version: 1
---

# Feasibility — Mention markets

## One-line verdict

GO — academically-validated modeling technique (MixMCP, Brier 0.1402→0.1392 on Kalshi), structurally rich arb surface, and a well-enumerated cottage-industry of 9+ speaker series with tractable Poisson/NegBin count models; the 8 non-Elon speakers ($10K–$300K vol/market) are the retail-accessible entry point.

---

## 1. Market enumeration (current YES set)

Live as of 2026-05-16 Gamma API pull (tag_slug=mention-markets + tag_slug=tweets-markets); all active, not closed.

### Tweet-count bracket markets (tweets-markets tag, 20 events returned)

| Title | Slug | vol_24h | vol_alltime | Sub-markets | Structural type |
|---|---|---|---|---|---|
| Elon Musk # tweets May 12–19 | elon-musk-of-tweets-may-12-may-19 | $1,358,943 | $7,246,864 | 26 | bracket-bin (20-wide) |
| Elon Musk # tweets May 14–16 | elon-musk-of-tweets-may-14-may-16 | $1,191,701 | $1,753,604 | 10 | bracket-bin (25-wide, 2-day) |
| Elon Musk # tweets May 15–22 | elon-musk-of-tweets-may-15-may-22 | $548,967 | $2,677,556 | 26 | bracket-bin (20-wide) |
| Elon Musk # tweets May 2026 | elon-musk-of-tweets-may-2026 | $140,771 | $2,715,846 | 66 | bracket-bin (20-wide, monthly) |
| Elon Musk # tweets May 16–18 | elon-musk-of-tweets-may-16-may-18 | $97,094 | $122,596 | 10 | bracket-bin (2-day) |
| CZ # posts May 15–22 | cz-binance-of-tweets-may-15-may-22-2026 | $53,191 | $56,893 | 11 | bracket-bin (20-wide) |
| White House # posts May 12–19 | white-house-of-tweets-may-12-may-19-2026 | $16,729 | $34,048 | 11 | bracket-bin (20-wide) |
| Trump # Truth Social May 12–19 | donald-trump-of-truth-social-posts-may-12-may-19 | $15,375 | $57,607 | 11 | bracket-bin (20-wide) |
| Ted Cruz # posts May 12–19 | ted-cruz-of-tweets-may-12-may-19-2026 | $6,093 | $11,533 | 11 | bracket-bin (20-wide) |
| Zelenskyy # posts May 12–19 | zelenskyy-of-tweets-may-12-may-19-2026 | $4,949 | $16,318 | 11 | bracket-bin (20-wide) |
| Trump # Truth Social May 15–22 | donald-trump-of-truth-social-posts-may-15-may-22 | $3,935 | $12,606 | 11 | bracket-bin (20-wide) |
| CZ # posts May 12–19 | cz-binance-of-tweets-may-12-may-19-2026 | $2,380 | $8,804 | 11 | bracket-bin (20-wide) |
| NYC Mayor # posts May 12–19 | nyc-mayor-of-tweets-may-12-may-19-2026 | $2,207 | $5,520 | 11 | bracket-bin (20-wide) |
| Khamenei # posts May 12–19 | khamenei-of-tweets-may-12-may-19-2026 | $1,740 | $10,144 | 13 | bracket-bin (narrow: 0–4, 5–9) |
| Zelenskyy # posts May 15–22 | zelenskyy-of-tweets-may-15-may-22-2026 | $908 | $6,482 | 11 | bracket-bin (20-wide) |

### Keyword-binary / count-threshold markets (mention-markets tag, 13 events returned)

| Title | Slug | vol_24h | vol_alltime | Sub-markets | Structural type |
|---|---|---|---|---|---|
| Trump bilateral events with Xi | what-will-trump-say-during-bilateral-events-with-xi-jinping | $6,469,462 | $10,775,119 | 33 | binary per keyword |
| Trump Bret Baier interview | what-will-trump-say-during-bret-baier-interview | $37,605 | $40,365 | 23 | binary per keyword |
| ICEMAN episode | what-will-be-said-on-iceman | $22,651 | $104,124 | 32 | binary per keyword |
| Trump weekly speech (May 17) | what-will-trump-say-this-week-may-17 | $4,112 | $84,179 | 23 | binary per keyword |
| MrBeast next YouTube video | what-will-mrbeast-say-during-his-next-youtube-video-268 | $3,739 | $8,530 | 28 | binary + count-threshold |
| Eurovision finals | what-will-be-said-during-the-eurovision-finals | $3,706 | $3,706 | 19 | binary per keyword |
| Trump Truth Social May 11–17 | what-will-trump-post-this-week-may-11-may-17 | $879 | $8,292 | 21 | binary per keyword |
| IEM Atlanta 2026 Grand Finals | what-will-be-said-during-the-iem-atlanta-2026-grand-finals | $506 | $1,214 | 29 | count-threshold (10+) |
| Starmer next PMQs | what-will-keir-starmer-say-at-the-next-prime-ministers-questions-event-154 | $393 | $33,739 | 30 | binary + count-threshold |
| Trump says in May | what-will-trump-say-in-may | $158 | $38,247 | 30 | binary per keyword |
| Animals Trump says in May | what-animals-will-trump-say-in-may | $136 | $14,808 | 29 | binary per keyword |
| Press Secretary next briefing | what-will-the-press-secretary-say-during-the-next-white-house-press-briefing | $136 | $5,655 | 25 | binary per keyword |
| Trump-named things in May | what-trump-named-things-will-trump-mention-in-may | $0 | $3,574 | 25 | binary per keyword |

**Volume tiering summary (tweet-count bracket series only):**
- Elon Musk aggregate (4+ active windows): ~$14.3M vol_alltime, ~$2.2M vol_24h — saturated tier
- Trump Truth Social aggregate (2 active windows): ~$70K vol_alltime
- White House aggregate (2 active windows): ~$42K vol_alltime
- CZ aggregate (2 active windows): ~$66K vol_alltime
- Ted Cruz: ~$12K, Zelenskyy: ~$23K, NYC Mayor: ~$6K, Khamenei: ~$10K

---

## 2. Predictive-edge data sources

### Source 1: X (Twitter) public timeline API
- **Access:** Basic-tier X API v2 (`GET /2/users/:id/tweets`) returns recent tweets; free tier is rate-limited to 500K monthly read requests. Full historical archives require X API Pro (~$5K/mo) or third-party scrapers (Apify, Nitter mirrors).
- **Freshness:** Near-real-time (minutes lag). Critical for mid-week Bayesian bracket narrowing.
- **Cost:** Free tier sufficient for the 8 low-volume non-Elon speakers (<=200 posts/week each). Elon Musk may hit rate limits at free tier.
- **Difficulty:** Low for current data; moderate for long historical backfill.

### Source 2: Truth Social public posts (Trump)
- **Access:** No official API. Public posts scrapable via `truthsocial.com/@realDonaldTrump.rss` (RSS feed, free) or Apify scraper (~$10/1K posts). Full archive publicly browsable back to 2022.
- **Freshness:** RSS updates within minutes of posting.
- **Cost:** Free (RSS) to ~$10/week (Apify).
- **Difficulty:** Low — RSS ingestion is straightforward.

### Source 3: YouTube auto-captions (podcast/show keyword markets)
- **Access:** YouTube Data API v3 (free, 10K units/day quota); auto-captions via `youtube-transcript-api` Python library (unofficial, no auth required). Covers MrBeast, ICEMAN, JRE, All-In, Lemonade Stand.
- **Freshness:** Auto-captions lag live video by minutes; historical episode corpus is the key modeling input (Kim et al. ablation: T dominates N).
- **Cost:** Free within API quota.
- **Difficulty:** Low-moderate. Per-speaker corpus assembly (prior episodes -> keyword frequency base-rates) is the engineering bottleneck.

### Source 4: UK Parliament Hansard API (Starmer PMQs)
- **Access:** `api.parliament.uk` (free REST API), transcripts published within 2-4 hours of PMQs. Live stream via Parliament TV. Historical transcripts back decades.
- **Freshness:** T+2-4 hours post-session. The resolution corpus is exactly the Hansard text, eliminating corpus-mismatch risk.
- **Cost:** Free.
- **Difficulty:** Very low. Direct API, verbatim resolution match, well-documented.

### Source 5: FOMC transcripts / press conference video (Powell, if FOMC markets recur)
- **Access:** Fed publishes verbatim press conference transcripts at `federalreserve.gov` within 3 weeks; live stream real-time. Historical transcripts back to 1994.
- **Freshness:** For pre-resolution modeling, prior-FOMC transcript is the load-bearing input (Kim et al. ablation: T > N). Live stream access adds real-time option.
- **Cost:** Free.
- **Difficulty:** Low. Challenge is that Polymarket FOMC markets resolve on the live press conference, so real-time monitoring is needed for intra-event updating.

---

## 3. Modeling spine

### Count-bracket markets (Elon Musk, Trump Truth Social, White House, Ted Cruz, CZ, Zelenskyy, NYC Mayor, Khamenei)

**Step 1 — Fit speaker-level count distribution on historical weekly totals:**

```
N_week ~ Poisson(lambda)       if Var(N) ~= E[N]
N_week ~ NegBin(r, p)         if Var(N) >> E[N]   (overdispersed; likely for Musk)

lambda = sample mean of weekly post counts over trailing 8-12 weeks
r, p = MLE on trailing window for NegBin
```

**Step 2 — Convert to bracket PMF:**

```
P(N in [a, b]) = CDF(b; lambda) - CDF(a-1; lambda)         Poisson
               = NegBinCDF(b; r,p) - NegBinCDF(a-1; r,p)   NegBin
```

Compare model PMF to market-implied PMF (sub-market last trade prices). Mispriced bins are the trades.

**Step 3 — Mid-week Bayesian update (intra-market signal):**

```
P(bracket | k posts observed in t/7 of window elapsed) proportional to
   P(bracket) * P(k | bracket, t/7 elapsed)

Likelihood: Poisson(k; lambda * t/7) truncated to brackets consistent with k
```

With 4 days elapsed and 60 posts observed, the bracket posterior collapses dramatically — this is where the intra-week edge is extracted.

**Computational cost:** Trivial — closed-form CDF evaluations. No GPU, sub-second per event.

**Step 4 — Keyword-binary markets (Trump speeches, Starmer PMQs, MrBeast, ICEMAN, JRE):**

Kim et al. MixMCP:

```
p_mcp = LLM_theta(T, N | p_mkt)    # T = prior episode/speech transcripts, N = recent news
p_mix = 0.7 * p_mkt + 0.3 * p_mcp
```

Edge concentrates in mid-confidence regime `p_mkt in [0.5, 0.7]` per Kim et al. disagreement-subset analysis (MCP wins 56.7% at 50-60%, 62.5% at 60-70%; loses at tails). Alpha=0.7 plateau confirmed at [0.6, 0.8] in-sample.

**Expected accuracy delta:** Brier 0.1402->0.1392 (absolute gain 0.0010 on N=856 Kalshi contracts). Operationally meaningful only across a portfolio of mid-confidence bins, not one-at-a-time.

**Platform transfer caveat:** Kim et al. validated on Kalshi earnings-call only (fixed-format transcripts, automated exact-string resolution). Polymarket corpora vary (Truth Social posts, podcast video, live speeches, esports broadcasts). Per-corpus retrieval pipelines are non-trivial before MixMCP is deployable here.

**Threshold count alternative:** For Starmer "Mr. Speaker 10+/20+" or MrBeast "Hundred/Thousand/Million 10+ times," fit a count regression then threshold. Predict continuous latent count, map to binary indicator. Likely outperforms direct binary prompting on threshold markets (Kim et al. do not test; documented gap in [[mention-markets]] Open Research Questions #4).

---

## 4. Structural-arb shape opportunities

### 4a. Rolling-window overlap arb (Elon Musk multi-window)

Three simultaneous Elon Musk weekly windows (May 12-19, May 14-16, May 15-22) share interior days. If May 14-16 resolves at 65-89 posts (currently 98% probability), this constrains May 12-19's plausible final count: with >=65 posts in May 14-16 alone, May 12-19 can only resolve in bins above some lower bound. This allows a no-model-needed bracket-elimination trade immediately post-earlier-window resolution.

Pre-condition: real-time tweet-count tracking (X API intraday pull).

### 4b. Bracket Sigma-check (cross-bracket no-arb constraint)

Within any bracket-bin event, `Sigma P(bracket_i) ~= 1.00`. Deviations >2-3 pp are Market Rebalancing Arbitrage per [[arbitrage-taxonomy]] S3. Khamenei brackets sum to ~102% (`<5` at 91% + `5-9` at 9%) — boundary case worth monitoring. Automated daily Sigma-check across all 20 tweet-market events costs one API call.

### 4c. Count-threshold monotonicity (Starmer 10+/20+)

Where both "10+ times" and "20+ times" sub-markets exist for the same keyword, P(20+) <= P(10+) must hold. Currently P(20+)=0.66, P(10+) inferred as >=0.89 (consistent). Track for inversions — any P(20+) > P(10+) is a direct MRA with no modeling required.

---

## 5. Microstructure regime

### Volume tiers per speaker (tweet-count markets)

| Speaker | Weekly vol tier | Regime classification |
|---|---|---|
| Elon Musk | ~$2-7M/window | High-volume, tight-spread, likely well-modeled — assume saturated |
| Trump Truth Social | ~$58K/window | Mid-volume, moderate spread, limited sophistication |
| White House | ~$34K/window | Mid-volume |
| CZ | ~$9-57K/window (regime-shifting) | Thin-to-mid, regime-shift mispricing window |
| Ted Cruz | ~$12K/window | Thin, low saturation |
| Zelenskyy | ~$6-16K/window | Thin, low saturation |
| NYC Mayor | ~$6K/window | Thin, very low saturation |
| Khamenei | ~$10K/window | Thin, stable cadence (<5/week) — base-rate certainty |

**Longshot bias on tail keyword bins:** Binary keyword markets typically price rare words at 5-15% Yes. Per [[polymarket-microstructure]] SF1, tail markets carry 650-900 bps half-spread. Patient limit-order liquidity provision on clearly-Yes bins is a yield strategy orthogonal to directional modeling.

**Depth profile:** Non-Elon markets are thin — $500-$2,000 positions move prices meaningfully. Favorable for retail (no fill slippage) but limits absolute sizing. Elon markets are the only ones with depth for institutional-scale sizing.

**Newly-opened window spread:** Freshly-listed windows (NEW tag) carry wider spreads before mid-week observations narrow the bracket. First-mover advantage is highest in first 12-24 hours of a window's life.

---

## 6. Saturation risk

**Elon Musk tweet-count (~$14M+ aggregate):** Almost certainly modeled by 2-3+ sophisticated retail operators with X API access. Market consolidates quickly around observed mid-week count. Assume near-zero edge without a real-time tracking pipeline that meaningfully outperforms the crowd.

**Trump Truth Social / White House / Ted Cruz:** Moderate saturation. Public RSS/API access means any retail operator can check the count. However, proper NegBin fitting with regime detection is non-trivial — likely not done by average participants. Estimated 1-3 sophisticated models in play.

**CZ (active regime shift):** Highest-probability mispricing candidate right now. Models trained on historical <20/week cadence are stale; the regime shift to 20-39/week is not yet fully priced into newly-opened windows. Low saturation given thin volume.

**Zelenskyy / NYC Mayor / Khamenei:** Very low saturation. Thin volume indicates few or no sophisticated participants. Straightforward base-rate modeling is likely uncontested.

**Keyword-binary markets (Trump speech, Starmer PMQs, MrBeast, ICEMAN, JRE):** MixMCP is an academic methodology not yet widely deployed at retail. Mid-confidence band (50-70%) is exactly where MixMCP edge concentrates and is least likely to be modeled. Saturation risk is low.

**Quant shops / Polymarket internals:** No direct evidence of quant-shop activity in these niche series. Sub-$300K weekly volumes are below minimum-viable-sizing threshold for most institutional desks. Polymarket market-making activity concentrates in high-volume Politics/Crypto, not Pop Culture cottage industry.

---

## 7. Top 3-5 specific markets to attack first

### 1. CZ (Changpeng Zhao) weekly post-count — HIGHEST PRIORITY
- **Slugs:** `cz-binance-of-tweets-may-15-may-22-2026`, `cz-binance-of-tweets-may-19-may-26-2026` (just opened, $1.2K vol)
- **Vol:** $53K (May 15-22), $1.2K (May 19-26)
- **Why:** Active regime shift from <20/week to 20-39/week. Models calibrated on stale historical cadence are mispriced. Newly-opened May 19-26 window will inherit the old prior before mid-week count observations update it. Non-Elon, not saturated. Bracket PMF fit trivial.
- **Entry signal:** Fit NegBin to CZ's actual post counts over the last 4 weeks (incorporating the regime shift); compare to May 19-26 opening PMF.

### 2. Keir Starmer PMQs keyword-binary markets
- **Slug:** `what-will-keir-starmer-say-at-the-next-prime-ministers-questions-event-154`
- **Vol:** $393 vol_24h, $33,739 vol_alltime
- **Why:** Stable recurring corpus (weekly PMQs, fixed format), authoritative resolution source (Hansard API, free, exactly the resolution corpus). 30 sub-markets per episode = large simultaneous position surface. Non-Elon, non-Trump, very low saturation. The "Mr. Speaker 10+/20+" structure is the regression-then-threshold target.
- **Entry signal:** Pull last 10 Hansard PMQs transcripts; compute per-keyword frequency base-rates; compare to market odds in the 50-70% band.

### 3. NYC Mayor weekly post-count
- **Slugs:** `nyc-mayor-of-tweets-may-12-may-19-2026`, `nyc-mayor-of-tweets-may-19-may-26-2026`
- **Vol:** $2.2K (May 12-19), $903 (May 19-26, freshly opened)
- **Why:** Very thin volume = very low saturation. Stable, low-volume X account with easily-trackable history. Simple Poisson model. Newly-opened May 19-26 window (P(20-39)=51%) is a clean entry before mid-week observations narrow the bracket. Smallest position sizing of any listed market; appropriate for initial model validation at low risk.
- **Entry signal:** Fetch last 12 weeks of @NYCMayor weekly post counts; fit Poisson; compare to May 19-26 bracket PMF.

### 4. ICEMAN keyword-binary markets (per-episode)
- **Slug:** `what-will-be-said-on-iceman`
- **Vol:** $22,651 vol_24h, $104,124 vol_alltime
- **Why (non-Elon-Musk speaker):** Podcast/show with stable speaker and episode format; MixMCP applicable with prior-episode transcripts as T. 32 sub-markets per episode = large simultaneous surface. Non-political, likely very low saturation. Mid-range vol ($22K daily) means meaningful sizing is possible without moving market.
- **Entry signal:** Scrape prior ICEMAN episode captions via YouTube API; compute keyword frequency; identify mid-confidence (50-70%) bins and apply MixMCP.

### 5. Zelenskyy weekly post-count
- **Slugs:** `zelenskyy-of-tweets-may-15-may-22-2026`, `zelenskyy-of-tweets-may-19-may-26-2026`
- **Vol:** $908 (May 15-22), $563 (May 19-26)
- **Why:** Zelenskyy maintains a disciplined posting cadence (~80-140/week) driven by the war's communication requirements, making it stable and predictable. Low saturation. Geopolitical events (ceasefire, escalations) are regime-change triggers worth monitoring — base-rate Poisson edge is cleanest on weeks without major events.
- **Entry signal:** Fit trailing 8-week Zelenskyy X post counts; apply regime filter (exclude weeks with declared major escalations); compare to market bracket PMF.

---

## 8. Feasibility rubric (1-5 each, higher = better; total /20)

- **Data availability: 5** — X API (public, free tier sufficient for 8 speakers), Truth Social RSS (free), Hansard API (free), YouTube auto-captions (free unofficial library), FOMC transcripts (free). Near-complete coverage of all resolution corpora at minimal cost (<$50/month operational estimate for the non-Elon tier).
- **Modeling tractability: 4** — Count markets: Poisson/NegBin bracket CDF is trivially implemented. Keyword-binary markets: MixMCP requires LLM inference (GPT-4-class, adds API cost and latency) plus corpus retrieval pipeline (non-trivial engineering). Threshold markets: regression-then-threshold not yet empirically validated on Polymarket. -1 for engineering overhead vs a pure-quant setup.
- **Market depth/sizing: 3** — Elon Musk tier is deep but saturated. Non-Elon speakers are $5K-$300K weekly — meaningful for retail but position sizing is constrained. Maximum realistic deployment: $2K-$5K per bracket bin per week in the non-Elon tier. Monthly Elon market ($2.7M) is large enough for moderate sizing if edge can be established.
- **Non-saturation: 4** — Elon Musk markets: assume saturated. Non-Elon tweet-count markets: thin volume, low sophistication. Keyword-binary markets: MixMCP not widely deployed, mid-confidence band uncontested. Regime-shift windows (CZ, newly-opened markets): possibly 0-to-1 sophisticated operators. Blended score across the retail-accessible subset: 4.
- **Total: 16/20**

---

## 9. Decision-tree mapping

- **Q1 YES-theme?** Yes — mention markets are the canonical YES theme from [[polymarket-strategy-matrix]]. Count-bracket and keyword-binary structures both have documented modeling approaches (Poisson/NegBin for count, MixMCP for keyword-binary). Resolution observable is text — directly aligned with LLM and corpus-based modeling.

- **Q2 Data source available?** Yes — specifically:
  - X public timeline API (tweet-count markets for all 8 non-Elon speakers)
  - Truth Social RSS (Trump Truth Social series)
  - YouTube auto-captions API (MrBeast, ICEMAN, JRE, All-In, Lemonade Stand)
  - Hansard API (Starmer PMQs)
  - All free or very low cost (<$50/month operational estimate for the non-Elon tier)

- **Q3 Structural-arb shape?** Yes — three shapes available:
  - Rolling-window overlap arb (Elon Musk simultaneous weekly windows sharing interior days)
  - Bracket Sigma-check (cross-bracket sum ~= 1.00 monitoring via daily API call)
  - Count-threshold monotonicity (Starmer 10+/20+ ladder; P(20+) > P(10+) is a direct MRA with no modeling)

- **Q4 Microstructure regime exploitable?** Yes — two regimes:
  - Thin-market regime (non-Elon speakers, $5K-$50K weekly): wide spreads, patient limit-order LP viable, first-mover advantage on newly-opened windows
  - Regime-shift moments (CZ, newly-opened markets): stale priors in market PMF before mid-week observations update — directional edge without requiring LLM infrastructure

---

## 10. Open questions / first concrete next steps

1. **Build the X API tweet-count backfill pipeline.** Fetch trailing 12 weeks of weekly post counts for all 8 non-Elon speakers (Trump-TS via RSS, others via X API v2). Fit Poisson/NegBin per speaker. Compute model bracket PMF for the current open window vs market odds. No LLM required — pure statistics. Expected time: ~1 day of engineering.

2. **Validate the CZ regime-shift trade immediately.** CZ May 19-26 window just opened ($1.2K vol). Determine CZ's actual posting rate for the past 4 weeks; if the 20-39 bracket is underpriced relative to the new regime, this is a same-week entry opportunity. Time-sensitive.

3. **Assemble the Starmer PMQs historical corpus and compute keyword base-rates.** Pull last 10 Hansard PMQs transcripts via `api.parliament.uk`; compute per-keyword occurrence rates across 30 sub-market keywords; compare to current market implied probs. Identify mid-confidence (50-70%) discrepancies as MixMCP entry triggers. Resolution corpus is exactly the data source, eliminating the corpus-mismatch caveat that applies to Trump speech or podcast markets.

4. **Implement the bracket Sigma-check monitoring tool.** Wire up a daily call to `gamma-api.polymarket.com/events?tag_slug=tweets-markets&active=true` and compute Sigma P(bracket_i) per event. Log violations >3 pp for manual review. Catches mechanical MRA opportunities across the entire tweet-market suite with no per-market modeling. Low-effort, run indefinitely.

5. **Prototype MixMCP on ICEMAN prior-episode corpus.** Cleanest non-political keyword-binary test bed — stable speaker, available YouTube transcripts, 32 sub-markets per episode. Implement the T = prior episode transcripts retrieval pipeline; apply `p_mix = 0.7*p_mkt + 0.3*p_mcp` across all 32 bins for the next episode. Log predictions vs resolutions for 3-5 episodes before committing capital. This validates MixMCP transfer from Kalshi earnings-call corpus to Polymarket podcast corpus before attacking higher-saturation Trump speech markets.
