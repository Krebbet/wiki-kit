# Feasibility Review — Cross-Theme Ranking

Meta-review of the 10 theme-level feasibility assessments. Produced 2026-05-16 after parallel agent runs against live Gamma API and the wiki backbone. Each theme was scored against 4 dimensions: data availability (5), modeling tractability (5), market depth/sizing (5), non-saturation (5). The pages live under `wiki/feasibility/*.md`; this page ranks them, surfaces what to attack first, and lists the cross-cutting open questions.

## Ranking matrix

| Rank | Theme | Verdict | Rubric | Capital tier | Time-to-edge |
|---|---|---|---|---|---|
| 1 | [[feasibility/mention-markets]] | **GO** | **16/20** | Low ($2K–$5K/bin) | Days (CZ regime-shift live) |
| 2 | [[feasibility/youtube]] | **GO** | **15/20** | Very low ($200–$500/leg) | Days (MrBeast May 31/Jun 30 milestones live) |
| 3 | [[feasibility/movies]] | Conditional YES | 15/20 | Low ($2K–$5K/film) | 1–2 weeks first build; days post-build |
| 4 | [[feasibility/geopolitical-date-ladder]] | YES with conditions | (Iran cluster strongest) | Med ($500–$5K via $500 CLOB ceiling) | Days (airspace 8pp watchlist) |
| 5 | [[feasibility/ai-tech-milestones]] | YES (two modes) | (mixed) | Med ($2K–$10K) | 4–6 weeks (Gemini ladders + Figure May 21) |
| 6 | [[feasibility/streaming-charts]] | Conditional YES | 14/20 | Low ($1K–$10K/sub-mkt) | 1 week pipeline build |
| 7 | [[feasibility/scenario-grid]] | Conditional YES (live mispricing) | — | Low-med ($15–30K binding leg) | Days (D-Senate+R-House 1.45¢ live) |
| 8 | [[feasibility/corporate-event-binaries]] | NARROW-YES | — | Low-med ($60–175K total) | 2–6 weeks (EDGAR + MSTR on-chain) |
| 9 | [[feasibility/lp-yield-farming]] | Conditional (meta-strategy) | — | **High** ($25K–$100K/market) | Phase 1 monitoring then weeks |
| 10 | [[feasibility/crypto-short-horizon]] | **AVOID** except FDV niches | — | High required, low retail edge | N/A for retail short-horizon |

Rubric column blank where theme assessment used different framework. See per-theme pages for full breakdown.

## What to attack first (next 30 days)

Five live time-sensitive opportunities surface above all others:

### 1. CZ Binance tweet-count regime shift (mention markets) — DAYS

Slug `cz-binance-of-tweets-may-19-may-26-2026` just opened ($1.2K vol). CZ cadence shifted from <20/wk to 20–39/wk; market PMF still anchored to stale prior. Fit NegBin on trailing 4 weeks of actual @cz_binance posts; compare to bracket PMF. Same-week entry. Lowest-effort highest-conviction trade across all 10 themes. See [[feasibility/mention-markets]].

### 2. D-Senate + R-House composite leg (scenario grid) — DAYS

Live mispricing at 1.45¢ vs ~3.0¢ implied by chamber-control binaries (~2× underpriced). Bind on $112K liquidity → ~$15–30K effective position → ~$200–$400 gross/round-trip. Hedge with Republican House binary short. Set up Gamma API gap_house monitor. See [[feasibility/scenario-grid]].

### 3. MicroStrategy BTC sale May 31 leg (corporate binaries) — 2 WEEKS

Live 59.5% Yes; on-chain MSTR treasury wallets are public. Set Arkham/Etherscan alert immediately. BTC outflow detected → buy YES; no outflow by May 25 → consider NO on May 31 leg. Size ≤$20K. See [[feasibility/corporate-event-binaries]].

### 4. Iran cluster monotonicity watchlist (geopolitical date-ladder) — DAILY

Airspace ladder 8pp slack (tightest); uranium 5pp. Any 4–5pp adverse move closes the gap → direct Long MRA. Daily Gamma API pull + Portwatch 7-day MA for Hormuz. Also: Portwatch 7-day MA approaching 60 in final 7–10 days converts Hormuz binary to near-certain — days-of-advance signal. See [[feasibility/geopolitical-date-ladder]].

### 5. MrBeast subscriber June 30 milestone (YouTube) — 6 WEEKS

500M sub at 26% / 497M at 62%. Linear regression on Social Blade 90-day history at ~8M/mo gain → simple model expects >85% on 497M. Build YouTube Data API + Social Blade poller; position size $200–$500/leg given thin market. See [[feasibility/youtube]].

## Recurring model archetypes (cross-theme synthesis)

Five model classes repeat across the 10 themes. Ranked by `breadth × evidence × build_cost⁻¹ × non-saturation`. Use this lens to prioritize *infrastructure* builds rather than per-theme builds.

### A1 — Count-distribution bracket PMF (Poisson / NegBin / lognormal)

**Applies to:** tweet-count brackets (8 non-Elon speakers per [[feasibility/mention-markets]]), MrBeast Day-1/Week-1 view brackets per [[feasibility/youtube]], Figure F.03 package count per [[feasibility/ai-tech-milestones]], MrBeast subscriber milestones, Hormuz traffic 7-day MA threshold.

**Model:** `N ~ Poisson(λ)` or `NegBin(r,p)` fit on trailing 8–12 wks; `P(bracket) = F(b_high) − F(b_low−1)`; mid-period Bayesian posterior `P(bracket|k obs in t/7) ∝ Poisson(k; λ·t/7)·prior`. View counts: `log(views) ~ N(μ,σ²)`. Closed-form, sub-second per event.

**Edge:** Non-Elon tweet markets carry stale priors not updating intra-period; CZ Q3 2025 regime shift uncontested; MrBeast 497M sub at 62% vs linear model >85% (~23pp). Mid-period posterior collapses sharply at day 4-of-7 → pre-vs-post-update repricing lag.

**Conditions:** Stable cadence; X API free-tier sufficient for 8 non-Elon speakers; sample-size adequate but flag regime-break overfit risk.

### A2 — Hazard / survival models for date-ladder markets

**Applies to:** SpaceX IPO + MSTR sale ladders per [[feasibility/corporate-event-binaries]], Iran cluster per [[feasibility/geopolitical-date-ladder]], Gemini 3.x release-date ladders per [[feasibility/ai-tech-milestones]].

**Model:** `S_mkt(t) = 1 − P_market(release_by_t)`; `S_prior(t) = Weibull(α, β; t − last_event)`; `S_posterior = (1−w)·S_mkt + w·S_prior`. Saguillo conditional: `P(event ∈ (T1,T2] | not by T1) = (P2 − P1)/(1 − P1)`. Catalyst updates from USPTO/EDGAR/IAEA/Portwatch sharply shift S(t).

**Edge:** Gemini 3.2 hazard ~83% mass at Google I/O May 20-21; Iran term-structure monotonicity 8pp/5pp slack on airspace/uranium; US-Iran Dec 31 peace 66.5% vs calibrated LLM 30-45% (~25pp, with UMA dispute risk caveat).

**Conditions:** Single discrete triggering event; public + machine-readable catalyst feeds. UMA dispute risk HIGH on consensus-based; LOW on Portwatch-keyed.

### A3 — LLM keyword-binary prediction (MixMCP + threshold-count regression)

**Applies to:** keyword-binary mention markets (Trump, Starmer, ICEMAN, MrBeast, JRE) per [[feasibility/mention-markets]]; geopolitical news-catalyst per [[feasibility/geopolitical-date-ladder]].

**Model:** Kim et al. `p_mcp = LLM_θ(T, N | p_mkt)`; `p_mix = 0.7·p_mkt + 0.3·p_mcp` (α=0.7 plateau in [0.6, 0.8]). Threshold-count variant: predict continuous latent count via regression, threshold to binary — empirically untested gap per [[mention-markets]] Open Research Q4.

**Edge:** Kim et al. Brier **0.1402 → 0.1392** on Kalshi (N=856 OOS, earnings-call only). Edge concentrates in `p_mkt ∈ [0.5, 0.7]` (MCP wins 56.7%/62.5% at 50-60%/60-70%; loses at tails). Geopolitics: GPT-5 Brier 0.14 + ECE 0.09 per [[llm-forecasting-by-domain]]; PolyBench `news_catalyst` CWR 50.0%.

**Conditions:** **Platform-transfer caveat — Kim validated on Kalshi fixed-format only.** Per-corpus retrieval pipelines (Truth Social, podcast video, live speeches) are non-trivial. ICEMAN is cleanest non-political test bed. $500/lot CLOB alpha ceiling.

### A4 — Bayesian intra-period update on real-time observable

**Applies to:** RT ladders (Beta-update per review) per [[feasibility/movies]]; box-office brackets (Thursday preview T-36h) per [[feasibility/movies]]; MrBeast Day-1 view brackets (NoxInfluencer hourly) per [[feasibility/youtube]]; mid-week tweet-count posterior per [[feasibility/mention-markets]].

**Model:** RT — Beta(α + n·yes_frac, β + n·(1−yes_frac)) with isotonic-regression monotonicity enforcement. Box-office — `E[opening | preview] = preview × genre_multiplier` (horror 3-4×, superhero 4-6×, family 3-5×, drama 2-4×). Views — `log(views(24h)) ≈ log(views(t)) + (24−t)·slope` with slope refit hourly hour-6 to hour-12.

**Edge:** Pre-vs-post-observable repricing lag is the exploitation window. NoxInfluencer hour-6 to hour-12 log-linear extrapolation within ±15% of hour-24 actual. RT monotonicity arb on `in-the-grey-rt-score` 1pp mid violation persists (below spread for riskless, but rule `mid(≥X) < mid(≥X+5) − spread/2` is exploitable when slack expands).

**Conditions:** Pre-vs-post repricing lag must exceed execution latency. Per-film build cost 5–7d first / 2–3d reusable. Adverse selection risk when observable is highly public.

### A5 — Structural-feed binary prediction + zero-modeling Σ-check overlay

**Applies to (a) detection-speed:** Chatbot Arena leaderboard race + Figure F.03 livestream per [[feasibility/ai-tech-milestones]]; SpaceX EDGAR + MSTR Arkham + Anthropic Crunchbase per [[feasibility/corporate-event-binaries]]; IMF Portwatch oracle per [[feasibility/geopolitical-date-ladder]].

**Applies to (b) zero-modeling Σ-check:** all NegRisk bracket events + all date-ladder events + all count-threshold N+/M+ + RT ladders + scenario-grid composite-vs-binary per [[feasibility-review]] §"Cross-cutting structural arb watchlist".

**Model:** (a) `P(rank_1 unchanged by T) = (1 − λ_displacement)^days_to_T`; HuggingFace/GitHub model-card detection; USPTO/EDGAR/on-chain monitoring with hours-to-days lead-time. (b) Pure constraint check; Σ = 1 (NegRisk), `P(by T1) ≤ P(by T2)` (ladder), `P(20+) ≤ P(10+)` (threshold), `mid(≥X) ≥ mid(≥X+5)` (RT), `P(D House)_composite ≈ P(D House)_binary` (scenario).

**Edge:** Chatbot Arena niche-tracking lag = hours-to-days before retail repricing. D-Senate+R-House live ~2× underpriced (1.45¢ vs ~3.0¢ implied). Saguillo: ~$39.6M extracted Apr 2024–Apr 2025; 41% of conditions had ≥1 MRA opportunity per [[arbitrage-taxonomy]]. Iran airspace 8pp / uranium 5pp slack live.

**Conditions:** (a) sub-hour automation latency for detection edge. (b) zero modeling; multi-leg partial-fill is primary execution risk — limit-order both legs simultaneously. Polymarket-native bots dominate within-market MRA (top wallet $2M / 4,049 tx per [[combinatorial-arbitrage-empirics]]); semantic-dependency MRAs less saturated.

### Cross-archetype patterns

1. **Mid-confidence band (p ∈ [0.5, 0.7]) is where predictive-edge concentrates** — verified across A2/A3/A4. Tail markets dominated by 650–900 bps half-spread per [[polymarket-microstructure]] SF1.
2. **Liquidity ceiling ~$500/trade** for predictive-edge per [[llm-forecasting-by-domain]] PolyBench across A1/A2/A3/A4; ~$15–30K for A5 with hedges.
3. **Free public data is sufficient for all 5 archetypes.** Only paid-tier flagged: Chartmetric ($50–250/mo) for Billboard radio proxy per [[feasibility/streaming-charts]]; Crunchbase Pro ($49/mo) optional for VC alerts per [[feasibility/corporate-event-binaries]].
4. **Polymarket-specific OOS validation is the cross-cutting gap.** Kim et al. is Kalshi earnings-call only. PolyBench provides Brier benchmarks but per-archetype Polymarket backtests are gaps flagged across [[feasibility/movies]], [[feasibility/mention-markets]], [[feasibility/youtube]].

### Implication for infrastructure sequencing

Build *one* archetype-A5 daily Σ-check automation first (covers entire surface, zero modeling, zero capital). Then build *one* corpus + model class per remaining archetype in priority order, applied to multiple themes simultaneously rather than per-theme silos:
1. A1 count-distribution: X API + Social Blade ingestion pipeline → attacks 4 themes simultaneously (mention markets, YouTube, Figure F.03, MrBeast subscribers).
2. A4 Bayesian update: comp-set DB + Beta-Binomial + NoxInfluencer integration → attacks movies + YouTube + mid-week tweet count.
3. A2 hazard model: catalyst-feed monitors (USPTO, EDGAR, IAEA, Portwatch) + Weibull fit → attacks geopolitics + AI/tech + corporate-event simultaneously.
4. A3 LLM keyword: ICEMAN MixMCP prototype first (cleanest non-political test bed); validate transfer before extending to political mention markets.

## Cross-cutting structural arb watchlist (zero-modeling, daily Σ-check)

These run as daily Gamma API automation regardless of which themes get capital:

1. **Bracket Σ-check** across all NegRisk bracket-bin events (`tag_slug=tweets-markets&active=true` + box-office brackets + Day-1 view brackets + Hit Price brackets). Σ P(bracket_i) should ≈ 1.00; deviations >2–3pp = MRA per [[arbitrage-taxonomy]] §3.
2. **Date-ladder monotonicity Σ-check** across all date-ladder events (SpaceX IPO ladder, MSTR sale ladder, Iran cluster, Gemini released-on 27-bucket). P(by T1) ≤ P(by T2) must hold; inversions are direct MRA.
3. **Count-threshold monotonicity** for keyword-binary markets with N+/M+ ladders (Starmer Mr-Speaker, MrBeast Hundred/Thousand/Million). P(20+) ≤ P(10+) must hold.
4. **RT score ladder monotonicity** for active RT events. `mid(≥X) < mid(≥X+5)` by more than `max(spread_X, spread_X+5)/2` is exploitable. In the Grey case still has 1pp mid violation as of capture.
5. **Composite-vs-binary gap monitor (midterms):** `gap_house = P(D House binary) − [P(D Sweep) + P(D Senate & R House)]` — alert when |gap| > 5pp.

## Saturation tier summary (informs sizing)

| Tier | Themes | Implication |
|---|---|---|
| **Very low** | Netflix Top 10; non-MrBeast Twitter (CZ regime, Zelenskyy, NYC Mayor, Khamenei); MrBeast metric markets (theoretical-mod / empirical-low); ICEMAN mention market; Esports LP sponsor pools | Retail edge real; sized to thin liq |
| **Low-moderate** | Movies (trade-press consensus + informed retail; no institutional quants at scale); Rotten Tomatoes (no quants); Starmer PMQs; corporate-event binaries (domain-knowledge gap unexploited by quants) | Build pipeline before capital |
| **Moderate** | AI/tech (trademark tracking is known practitioner edge; compressed on near-term Gemini); Geopolitics Iran (consensus, but news-catalyst CWR 50.0% remains); Trump Truth Social mention | Edge requires specific differentiation |
| **High** | Top-100 LP markets (HHI 0.031); MicroStrategy on-chain ($27M total vol); Chatbot Arena May leaderboard (Anthropic 81.5%) | Skip or sub-niche only |
| **Maximum** | Crypto 5m/15m/1h/4h Up-Down; ATM monthly Hit Price; FIFA sub-markets | Avoid for retail |

## Key infrastructure builds (reusable across themes)

These pipelines pay back across multiple themes — sequence first:

1. **Gamma API automation framework** — single poller with `rewardsDailyRate / rewardsMaxSpread / clobRewards[].endDate / liquidityNum / volume24hr` extraction; powers LP yield farming, Σ-check automation, date-ladder monotonicity, sponsor-end depth pull. Used by themes 1–10.
2. **X API v2 + Truth Social RSS + Hansard API ingestion** — covers 8 non-Elon tweet-count speakers + Starmer keyword-binary. Powers mention-markets entire surface.
3. **YouTube Data API v3 + Social Blade scraper + NoxInfluencer hourly** — covers MrBeast milestone + Day-1 view + mention markets.
4. **SEC EDGAR EFTS + Etherscan + Arkham wallet watcher** — covers SpaceX IPO + MSTR BTC sale; minimal incremental cost after first build.
5. **The Numbers / BOM scraper + Thursday-preview tracker + RT scraper with Beta-update + monotonicity alert** — covers all movies markets.
6. **lmarena.ai leaderboard scrape + HuggingFace + GitHub release feed + USPTO trademark crawler** — covers AI/tech milestones full surface.
7. **GDELT CAMEO Iran filter + IMF Portwatch daily pull** — covers Iran cluster.
8. **Decision Desk + Silver Bulletin per-seat pull + joint-distribution model** — covers scenario grid + per-seat district markets.

## What was confirmed live

Cross-cutting facts confirmed across the 10 runs:
- Crypto BTC price markets resolve via Binance BTC/USDT 1m candles (NOT Chainlink/Pyth) — partially closes [[uma-optimistic-oracle]] open follow-up.
- UMA bond $500 USDC.e (not $750), $5 reward — confirmed by capture tool.
- NegRisk anonymization in Gamma API: blocks Chinese AI Company market entirely; partial on Style Control variant; does NOT block primary Chatbot Arena races.
- Gamma API exposes all 3 LP reward program parameters in `clobRewards[]` — Sponsor Rewards roll into `rewardsDailyRate` with platform LR.
- Fourth yield layer `holdingRewardsEnabled` discovered on select FIFA sub-markets — mechanics unknown.
- RT monotonicity arb on In the Grey 1pp mid violation persists at capture.
- D-Senate + R-House composite leg at 1.45¢ vs ~3.0¢ implied — live ~2× underpricing.
- The May-13 "P(R-Sweep)=−12%" candidate is NOT live; was a partial-capture artifact.

## Open follow-ups across themes

1. **Saturation empirics** — for every theme, the wiki currently estimates saturation from heuristics (volume tier + market depth + retail-vs-institutional proxies). On-chain `OrderFilled` maker-HHI per market would convert these estimates to measurements. Highest priority: Starmer date-ladder cluster (LP target), MrBeast sub-markets (predictive-edge target).
2. **Fill-rate backtest** — for LP yield farming, the load-bearing unknown is what fraction of quotes inside `rewardsMaxSpread` actually fill on mid-cap political. Needs on-chain `OrderFilled` analysis.
3. **MixMCP transfer validation** — Kim et al. results are Kalshi-only (fixed-format earnings calls + automated string-match resolution). Polymarket transfer must be validated on at least one non-political stable corpus before capital. ICEMAN is the cleanest test bed (32 sub-markets/episode, stable speaker, YouTube transcripts).
4. **`holdingRewardsEnabled` mechanics** — fourth yield layer with unknown payout mechanics. Resolve before treating it as part of the stack.
5. **GPT-6 release ladder market emergence** — currently absent; trademark-monitoring should detect first appearance.
6. **2028 primary scenario grids** — VP-pick markets do not exist yet; expected mid-2027 emergence.
7. **PolyBench backtest of Chatbot Arena binary stability** — Tech is "mixed-tier" per [[llm-forecasting-by-domain]] but Chatbot Arena (single observable feed) is structurally closer to Sports tier. Empirical Brier check warranted.
8. **Portwatch 7-day MA backtest** — confirm threshold-crossing detection precedes Polymarket repricing by enough margin to enter.

## Recommendations (no user decision required per "do not wait" instruction)

**Tier 1 — start immediately:**
- CZ tweet-count regime-shift trade (same-week entry window).
- D-Senate + R-House composite leg position with hedge (live mispricing).
- MSTR Arkham/Etherscan alert (zero cost; 2-week resolution).
- Iran airspace + uranium daily monotonicity Σ-check (zero modeling).

**Tier 2 — build pipeline this week:**
- YouTube Data API v3 + Social Blade for MrBeast June 30 milestones.
- X API v2 backfill for 8 non-Elon tweet speakers; Poisson/NegBin fit.
- Hansard last-10-PMQs scrape; per-keyword base-rates for Starmer 30 sub-markets.
- Bracket Σ-check automation across all `tag_slug=tweets-markets`.

**Tier 3 — month-horizon builds:**
- Movies comp-set + Thursday preview tracker + RT Beta model.
- EDGAR EFTS S-1 alert for SpaceX.
- ICEMAN MixMCP prototype on prior-episode YouTube transcripts.

**Skip / deprioritize:**
- All 5m/15m/1h/4h crypto Up-Down markets (saturated).
- Top-100 FIFA / NBA LP yield farming (institutional saturation).
- Anthropic vs OpenAI 89c position (thinnest of all corporate binaries; high possible-insider risk).

## Source

- `raw/feasibility/<theme>/summary.md` × 10 (all 2026-05-16)
- All 10 theme pages under `wiki/feasibility/`
- [[polymarket-strategy-matrix]] — spine for 10-theme enumeration
- Gamma API live pulls across all themes (2026-05-16)

## Related

- [[polymarket-strategy-matrix]]
- [[feasibility/mention-markets]]
- [[feasibility/movies]]
- [[feasibility/streaming-charts]]
- [[feasibility/youtube]]
- [[feasibility/ai-tech-milestones]]
- [[feasibility/crypto-short-horizon]]
- [[feasibility/corporate-event-binaries]]
- [[feasibility/geopolitical-date-ladder]]
- [[feasibility/scenario-grid]]
- [[feasibility/lp-yield-farming]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
- [[polymarket-lp-incentives]]
- [[llm-forecasting-by-domain]]
- [[uma-optimistic-oracle]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
