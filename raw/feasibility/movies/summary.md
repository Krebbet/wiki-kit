---
theme: "Movies — Opening-Weekend Box Office + Rotten Tomatoes Score Ladders"
slug: "movies"
assessed_on: "2026-05-16"
verdict: "Conditional YES — box-office brackets and RT ladders are structurally tractable with public data signals, but per-film model effort is high (~1 week/release), markets are thin ($1K–$87K per event 24h vol), and saturation from studio quant teams and professional analysts is significant; net edge is real but sizing is capped by liquidity."
---

# Feasibility Assessment: Polymarket Movies Markets

## 1. One-Line Verdict

Conditional YES — box-office brackets and RT ladders are structurally tractable with public data signals, but per-film model effort is high (~1 week/release for first build; ~2–3 days with reusable framework), markets are thin ($1K–$87K per event 24h vol), and saturation from studio quant teams and professional analysts is significant; net edge is real but sizing is capped by liquidity.

---

## 2. Market Enumeration

Live Gamma API snapshot 2026-05-16, `tag_slug=movies`, `tag_slug=box-office`, `tag_slug=rotten-tomatoes`, active + not-closed, sorted by 24h volume descending.

### Box-Office Bracket Events (Structure 4 per [[polymarket-market-structures]])

| Event | End | Vol 24h | Vol All | OI | Bins | State |
|---|---|---|---|---|---|---|
| "Obsession" Opening Weekend Box Office | 2026-05-18 | $86,916 | $127,191 | $40,202 | 5 | Near-resolution: >15m at 65%, 13–15m at 35% |
| "Michael" 4th Weekend Box Office | 2026-05-18 | $35,915 | $43,006 | $14,105 | 4 | Near-resolution: >25m at 59%, 22–25m at 41% |
| "In the Grey" Opening Weekend Box Office | 2026-05-18 | $20,909 | $24,477 | $12,105 | 5 | Near-resolution: <3.5m at 90.5% |
| "Mortal Kombat II" 2nd Weekend Box Office | 2026-05-18 | $13,265 | $26,458 | $8,650 | 4 | Near-resolution: <20m at 99.4% |
| "The Devil Wears Prada 2" 3rd Weekend Box Office | 2026-05-18 | $11,121 | $16,962 | $7,441 | 4 | Near-resolution: <23m at 95.5% |
| "Backrooms" Opening Weekend Box Office | 2026-06-01 | $779 | $2,292 | $1,744 | 5 | Future (May 29–31); spread wide; tractable |
| "Mandalorian and Grogu" 4-day Opening Weekend | 2026-05-26 | $582 | $1,165 | $1,751 | 5 | Future (May 22–25); very thin ($1–4K/sub-mkt) |

Resolution rule: The Numbers (`the-numbers.com`) "Daily Box Office Performance" tab, 3-day weekend sum (Fri–Sun; 4-day Fri–Mon for holiday weekends). Non-studio-estimate actuals required; ambiguous cases wait for both The Numbers and BoxOfficeMojo to confirm final figures.

### Rotten Tomatoes Ladder Events (Monotone threshold variant of Structure 2)

| Event | End | Vol 24h | Vol All | OI | Steps | State |
|---|---|---|---|---|---|---|
| "In the Grey" RT score | 2026-05-18 | $39,855 | $97,060 | $3,249 | 9 levels | Near-violation at 55/60 boundary; see §6 |
| "Is God Is" RT score | 2026-05-18 | $1,151 | $1,727 | $1,140 | 4 levels | Near-resolved: 93+ at 97.5%, 99+ at 0.3% |
| "Obsession" RT score | 2026-05-18 | $287 | $10,538 | $9,271 | 8 levels | Already resolved (all ≥55 rungs near 100%) |
| "Mandalorian and Grogu" RT score | 2026-05-25 | $11 | $396 | $334 | 7 levels | Future; extremely thin; spreads 0.20–0.76 |

Resolution rule: displayed Rotten Tomatoes "All Critics" Tomatometer at 10:00 AM ET on end date. Point-in-time snapshot; resolves No if no data by 4 days post-end.

NegRisk tag: RT ladder markets are `negRisk: False` — each rung is an independent binary, not a grouped exhaustive partition. No-arb constraint is monotonicity (`P(≥X) ≥ P(≥X+k)` for k > 0), not `Σ P = 1`.

### Annual Race / Long-Dated Events (PARTIAL)

| Event | Vol 24h | Vol All | Structure |
|---|---|---|---|
| Highest grossing movie in 2026? | $139,541 | $7,153,400 | Candidate race, 28 sub-markets, BoxOfficeMojo |
| Which movie has biggest opening weekend in 2026? | $3,736 | $1,570,601 | Candidate race, 27 sub-markets, The Numbers |

Long-dated candidate-race structures (NegRisk: True) with year-long resolution. High total volume because they run all year. Per-film edge requires advance box-office calendar modeling; slow-money positioning only.

---

## 3. Data Sources

### Box-Office

| Source | Access | Signal Type | Timing |
|---|---|---|---|
| The Numbers (`the-numbers.com`) | Public, free | Resolution source | Fri–Sun daily figures: estimates Saturday night, revised estimates Sunday evening, finals Monday–Tuesday |
| Box Office Mojo | Public, free | Secondary resolution confirmation | Same cadence |
| Fandango presale index | Public page scrape, no official API | Advance ticket proxy | T-7 to T-0 |
| AMC Theatres showtimes / seats | Public page scrape, no official API | Advance ticket proxy | T-7 to T-0 |
| Atom Tickets "Top Sellers" | Public page | Advance ticket proxy (ordinal) | T-7 to T-0 |
| Box Office Theory tracker threads | Public forums | Analyst community consensus | T-3 to opening; updated hourly on opening weekend |
| Thursday preview gross | The Numbers / BOM, ~11pm Thursday ET | Hard pre-resolution signal | ~36 hours before Sunday afternoon post-actuals |
| Variety / Deadline weekend estimates | Public article scrape | Industry consensus | Sunday morning before actuals; accurate for wide releases |
| Comscore proprietary | Paid subscription (trade press syndication) | Industry insider | Sunday morning; syndicated via Deadline/Variety |

**Thursday preview gross as 36h hard signal:** Preview gross is posted ~11pm Thursday ET, 36 hours before the Sunday-evening posting of weekend actuals (which is when resolution conditions are typically met). For wide releases, Thursday preview gross correlates strongly (empirically r ≈ 0.85–0.90) with final 3-day gross via a genre-dependent multiplier (typically 3x–6x). A film with $3M Thursday previews will almost certainly open >$20M; one with $300K will almost certainly open <$5M. This is the single highest-value pre-resolution signal and is freely accessible.

**API/scraping access assessment:** Fandango/AMC/Atom have no public API. Scraping is viable but fragile (JS-rendered SPAs; Cloudflare on some). Practical stack: (a) monitor Fandango showtimes-sold-out density via headless browser scrape; (b) subscribe to Box Office Theory tracker threads; (c) watch Deadline/Variety for Sunday morning consensus. The Numbers and BoxOfficeMojo are freely scrapeable for daily figures.

### Rotten Tomatoes

| Source | Access | Signal Type | Timing |
|---|---|---|---|
| Rotten Tomatoes website | Public, no official API (API deprecated ~2019) | Resolution source | Score displayed at resolution snapshot time |
| Unofficial RT API wrappers | Fragile / reverse-engineered | Live score scrape | Continuously once embargo lifts |
| Metacritic | Public, stable | Correlated signal (r ≈ 0.85 with RT score) | Same timeline as RT |
| Review embargo lift date | Trade press (Deadline, Variety, THR) | Event signal — score will be observable | Typically 1–5 days pre-release; later lift = lower expected score (directional prior) |
| Prior-film RT score (franchise/director) | Historical, public | Bayesian prior | Available before market opens |

**RT API status:** Official Rotten Tomatoes API closed to new developers circa 2019. Unofficial/reverse-engineered wrappers exist (`rotten-tomatoes-client` npm, Python scrapers). The official site is scrapeable but employs bot-detection (Cloudflare). A reliable scraper or unofficial wrapper is required for automated score monitoring.

**Embargo lift timing as signal:** Studios embargo reviews for wide releases, typically lifting 1–5 days before release (sometimes same day for low-confidence releases). Late embargo lifts are associated with lower scores — directionally reliable, not precise. This creates a two-stage model: (1) predict score range from embargo timing and prior-film priors, (2) update rapidly as individual reviews aggregate post-lift.

---

## 4. Modeling Spine

### Box-Office Bracket Model

Goal: produce `P(gross in bin_i)` for each bracket bin from pre-release public data.

**Inputs, ordered by predictive power:**
1. Thursday preview gross (T-36h, hard): anchor the distribution via empirical preview-to-weekend multiplier. Genre-specific multiplier distributions (horror: 3–4x; superhero: 4–6x; family: 3–5x; prestige drama: 2–4x).
2. Advance ticket proxy (T-7 to T-0): Fandango showtimes-sold-out density or Atom Top Sellers ranking; regress against historical openings for comp films.
3. Comp-set analysis: 5–10 comparable releases by genre, franchise status, MPAA rating, release-date quarter, marketing spend tier. Fit lognormal or empirical CDF over opening weekends; Bayesian shrinkage toward comp mean.
4. Trade-press tracking data: "awareness" and "definite interest" figures syndicated via Variety/Deadline. Rough positive predictor.
5. Weekend competition: opening gross negatively impacted by competition in same audience demographic; model using overlap-adjusted market share.

**Output:** `P(gross > X)` as CDF over bracket thresholds → `P(bin_i)` by differencing. Compare to Polymarket implied PMF; bet mispriced bins.

**Calibration note:** No Polymarket-specific backtest in the wiki (flagged in [[polymarket-strategy-matrix]]). Box Office Theory / Box Office Pro / Variety consensus is the natural benchmark — beating their track record by >1–2% on the CDF (net of 5% taker fee) is the required hurdle.

### RT Score Ladder Model

Goal: produce `P(score ≥ X)` for each rung.

**Inputs:**
1. Prior-film RT score (franchise/director/studio): strong prior for sequels and director-consistent releases.
2. Metacritic score (if earlier than RT lift): high correlation; infer approximate RT score range.
3. Embargo lift timing: late lift → lower expected score (directional prior).
4. Individual reviews as they post: Beta-distribution Bayesian update — with n reviews in, posterior Beta(α, β) where α = running_yes_fraction × n + prior_α, β = (1 - running_fraction) × n + prior_β. Each review shifts the posterior; `P(≥X) = 1 - F_Beta(X/100; α, β)`.
5. Genre base rate: maintain per-genre Beta prior (horror films, prestige drama, animation, etc. have distinct RT score distributions).

**Monotonicity enforcement:** `P(≥X) ≥ P(≥X+k)` for all k > 0. After any model update, isotonic regression or pool-adjacent violators (PAV) can enforce monotonicity across rungs before comparing to market prices.

---

## 5. Structural Arb — RT Monotonicity

### "In the Grey" RT Ladder — Live Analysis (2026-05-16)

Live prices from Gamma API:

| Rung | Mid | Bid | Ask | Spread |
|---|---|---|---|---|
| ≥40 | 0.955 | 0.950 | 0.960 | 0.010 |
| ≥45 | 0.600 | 0.500 | 0.700 | 0.200 |
| ≥50 | 0.240 | 0.060 | 0.420 | 0.360 |
| ≥55 | 0.100 | 0.040 | 0.160 | 0.120 |
| ≥60 | 0.090 | 0.040 | 0.140 | 0.100 |
| ≥65 | 0.018 | 0.006 | 0.029 | 0.023 |
| ≥70 | 0.013 | 0.005 | 0.022 | 0.017 |
| ≥75 | 0.006 | 0.003 | 0.009 | 0.006 |
| ≥80 | 0.004 | 0.002 | 0.005 | 0.003 |

**Update vs prior capture:** Earlier research (2026-05-16 morning) documented a harder violation of `P(≥55) = 7% < P(≥60) = 9.5%`. Live Gamma API now shows mid-price violation partially closed: `P(≥55 mid) = 10% > P(≥60 mid) = 9%`. The 1 pp gap at mid persists.

**Spread-adjusted arb:** The 1 pp mid violation is below both spreads (12% on 55+, 10% on 60+). A pure two-leg riskless arb (buy 55+ Yes at ask 0.16, sell 60+ Yes at bid 0.04) is loss-making:
- If score ≥ 60: +0.84 on leg1, -0.96 on leg2 = net -0.12.
This is **not a riskless arb** at prevailing prices. The opportunity is a limit-order bet: buy 55+ Yes at ~0.07–0.09 (below the 60+ mid), profiting if score lands in [55, 60). This requires a genuine view on the score range.

**When the arb IS exploitable:** If a future RT ladder event shows `mid(≥X) < mid(≥X+5)` by more than `max(spread_X, spread_{X+5}) / 2`, then buying the lower-threshold Yes and holding to resolution is profitable regardless of outcome where score ≥ X. Monitor daily with automated Γ-check.

### Box-Office Bracket Σ-Check

For NegRisk: True bracket events, `Σ P(bin_i) = 1` must hold. Live check for "Obsession":
- Bins: >15m (0.65) + 13–15m (0.345) + 11–13m (0.0035) + 9–11m (0.001) + <9m (0.0005) = **1.000**. No violation; market is near-resolved.

For future/early-lifecycle bracket events ("Backrooms", "Mandalorian"), wider spreads create larger residuals. Run Σ-check at market open to detect violations worth trading.

---

## 6. Microstructure

**Liquidity levels:**
- Top box-office event (Obsession): $86,916 24h vol; sub-market depths: $8K–$55K all-time. Tight leading bin (2% spread); wide tail bins (0.1–0.3% mid, but very wide absolute spreads).
- RT ladder (In the Grey): $39,855 24h vol; sub-market liquidity: $987–$6,287 per rung. Thin.
- Taker fee: 5% (culture_fees). Maker rebate: 25% of fee paid by taker. On thin markets, taker fee dominates; limit-order (maker) strategy preferred.

**Fee impact at typical RT sizes:**
- Buy 55+ at ask=0.16 on $500 notional: fee = 0.16 × 0.05 × 500 = $4. For a 1 pp edge over market mid, EV ≈ 0.01 × 500 = $5. Fee nearly eats the edge. Supports small fractional-Kelly sizing (f < 0.20).

**Event lifecycle timing:**
- Box-office brackets launch ~5–7 days pre-weekend. Volume concentrates T-3 to T-1 Thursday night. After Thursday preview gross posts, the market has often partially resolved in price.
- Edge window: T-7 to T-1 Thursday night. Ideal entry: T-3 to T-2 for comp-set model; update to strong view after preview gross.

---

## 7. Saturation Assessment

**Box-office:**
- Hollywood studios run proprietary internal box-office models (Comscore, PostTrak, tracking data). Studio projection teams have decades of comp databases. Studio forecast accuracy on wide releases is within 10–15% of actuals on opening-weekend gross.
- Dedicated analyst firms: EntTelligence, Quorum, Comscore, Box Office Pro. Trade press (Deadline, Variety) publish consensus forecasts before every wide release. This consensus is the primary competitor: Polymarket prices quickly converge toward the Deadline/Variety consensus.
- Retail box-office traders on Polymarket are often genuinely knowledgeable (Box Office Theory community).
- Professional quant shops are not present at this liquidity scale ($1K–$87K per event); operational overhead is prohibitive.
- **Saturation verdict:** Moderate. Competition is informed retail + trade-press consensus, not institutional quants. Edge requires consistently beating the Variety/Deadline consensus by >1–2% on the bracket CDF, net of 5% taker fee.

**Rotten Tomatoes:**
- RT score prediction is a niche within entertainment analytics. No known quant shop systematically trades RT ladders at this liquidity.
- Film critics with early screening access cannot legally trade on that information in US markets; offshore platform (Polymarket) creates ambiguity, but the RT score is typically public before market resolution.
- Primary competitor: retail traders who monitor RT score forecasting communities and scrape RT in real time.
- **Saturation verdict:** Low-to-moderate. Thinner competition than box-office; also thinner liquidity.

---

## 8. Top Markets by Attractiveness

Ranked by: liquidity × edge-availability × data-access / effort.

1. **Opening-weekend box-office brackets for wide releases** — highest liquidity; Thursday preview is near-infallible signal; edge window T-7 to T-1. Obsession ($87K/day) is the current canonical instance. Effort: 2–4 days/film with reusable comp-set framework.

2. **RT score ladders for prestige releases near embargo lift** — edge window is 1–3 days post-embargo-lift while score is updating and market hasn't fully incorporated individual reviews. In the Grey ($40K/day) is the current live example; Mandalorian/Grogu ($11/day) is too thin for now but will grow on release. Effort: ~1 week for first Beta-update model build; reusable thereafter.

3. **Annual highest-grosser race** — $7.1M all-time, $140K/day. NegRisk candidate race; liquid enough for meaningful sizing. Super Mario Galaxy Movie at 12.4% is the current leader. Long-dated (year-end); slow-money position building only.

4. **Near-resolved bracket events as LP targets** — provide liquidity on the near-certain leading bin to harvest maker rebate and liquidity rewards. Mortal Kombat II <20m at 99.4%, Devil Wears Prada 2 <23m at 95.5%. Minimal edge; pure LP yield play.

---

## 9. Rubric Score (out of 20)

| Dimension | Score | Notes |
|---|---|---|
| Data availability | 4/4 | Thursday preview gross (free, T-36h), advance ticket proxies (scrapeable), The Numbers/BOM (free, resolution source), RT page (scrapeable with unofficial API). Full stack publicly accessible. |
| Model buildability | 3/4 | Comp-set regression (standard) and Beta RT model (standard). Challenge: RT API fragility; lognormal comp-set calibration requires historical data work. Builds in ~1 week for first film; reusable. |
| Structural arb surface | 3/4 | RT ladder monotonicity arb is systematic and real. Box-office Σ-check (NegRisk enforced) adds secondary layer. Current In the Grey violation is 1 pp at mid — below spread for riskless arb but signals the mechanism. |
| Liquidity | 2/4 | Box-office: $1K–$87K 24h per event; RT: $1K–$40K. 5% taker fee. Thin books cap Kelly sizing. Annual races have more depth but slow movement. |
| Saturation | 3/4 | Box-office: moderate (trade-press consensus + informed retail). RT: low-to-moderate. No institutional quants at this liquidity scale. |

**Total: 15/20** — Viable niche with real structural edge; liquidity and per-film effort are the binding constraints.

---

## 10. Decision-Tree Mapping

Per [[polymarket-strategy-matrix]] signal-availability decision tree:

1. **YES-classified theme?** Box-office brackets: YES. RT ladders: YES. Annual races: PARTIAL.
2. **Predictive-edge data source available?** YES — advance ticket proxy (Fandango scrape), Thursday preview gross (public, T-36h hard signal), The Numbers/BOM actuals (resolution source), RT scrape, prior-film priors.
3. **Structural-arb shape?** YES — RT ladder monotonicity constraint; box-office bracket Σ = 1 (NegRisk). Run daily automated Σ/monotonicity checks for live violations.
4. **Microstructure regime?** Newly-listed box-office markets carry wider spreads (tighten mid-maturity); tail bins carry 650–900 bps half-spread per [[polymarket-microstructure]] SF1.

**Recommended entry strategy:**
- Box-office: comp-set regression at T-7; limit-order bets at T-3 to T-2; hard model update on Thursday preview gross (~11pm ET Thursday). Avoid taker fills on thin tail bins.
- RT ladders: open Beta model once first 10–20 reviews post-embargo-lift. Run monotonicity checks daily. Use limit orders; avoid 5% taker fee except for high-conviction entries.

**Per-film effort estimate:**
- First film: 5–7 days to build comp-set database, calibrate lognormal/empirical CDF, set up The Numbers scraper, deploy RT Beta model.
- Subsequent films: 2–3 days/film with reusable framework. Marginal cost drops sharply after films 3–4.
- Genre-specific models (horror, superhero, family animation) reduce comp-set search space; build these once each.

---

## 11. Next Steps

1. **Comp-set database:** Pull all 2024–2026 wide-release opening weekends from The Numbers historical tables. Categorize by genre, franchise status, MPAA rating, release quarter. This is the reusable backbone for all future box-office bracket bets.

2. **RT scraper:** Build lightweight scraper (or unofficial API wrapper) to monitor live Tomatometer scores as reviews aggregate. Add automated monotonicity violation alerts against live Gamma API prices — trigger: `mid(≥X) < mid(≥X+5)` by >half the spread.

3. **Thursday preview tracker:** Automate nightly pull of The Numbers "Daily Box Office Performance" for release days. Highest-value signal; free to access.

4. **Advance ticket proxy:** Evaluate headless-browser Fandango showtimes-sold-out scraper. Alternatively use Atom "Top Sellers" ordinal ranking. Back-test proxy correlation against historical Thursday preview gross.

5. **RT Beta model backtest:** Pull all resolved RT ladder markets from Gamma API (`closed=true`), compare Beta model predictions vs market mid-prices; compute Brier score and assess calibration.

6. **Annual race position:** For "Highest grossing movie in 2026?", build year-end box-office calendar model. Super Mario Galaxy Movie at 12.4% is the current leading candidate; position with fractional Kelly given 7-month horizon and high uncertainty.

7. **Data quality guard:** Add `end_date < today` check to any Gamma API pipeline. "How to Make a Killing" (RT, end 2026-02-23, still returning `active: True`) is the documented false-open case; this guard prevents false positives in the monitoring pipeline.

---

## Source

- Live Gamma API queries: `tag_slug=movies`, `tag_slug=box-office`, `tag_slug=rotten-tomatoes` — 2026-05-16
- `raw/research/polymarket-broad-coverage-sweep/02-polymarket-movies-gamma.md` — captured 2026-05-16
- `raw/research/polymarket-broad-coverage-sweep/.ingest/02-polymarket-movies-gamma.summary.md`
- `wiki/polymarket-strategy-matrix.md`
- `wiki/polymarket-market-structures.md`

## Related

- [[polymarket-market-structures]]
- [[polymarket-strategy-matrix]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
- [[polymarket-lp-incentives]]
- [[mention-markets]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
