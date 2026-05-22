# Feasibility — Movies (Box Office + Rotten Tomatoes)

Opening-weekend box-office bracket markets and Rotten Tomatoes score ladders. **Conditional YES (15/20):** structurally tractable with public data; per-film build effort high (~1 week first / 2–3 days reusable), markets are thin ($1K–$87K 24h vol), studio quant + trade-press consensus presents moderate saturation. Net edge is real but liquidity caps sizing. Live Gamma API 2026-05-16.

## Rubric (out of 20)

| Dimension | Score | Notes |
|---|---|---|
| Data availability | 4/4 | Thursday preview gross T-36h, The Numbers/BOM, RT scrape, embargo lift timing — all free |
| Model buildability | 3/4 | Comp-set regression + Beta-update RT model standard; RT API fragility, lognormal calibration ~1 week build |
| Structural arb surface | 3/4 | RT ladder monotonicity systematic; bracket Σ-check (NegRisk); In the Grey 1pp mid violation below spread |
| Liquidity | 2/4 | $1K–$87K 24h per event; 5% taker fee dominates on thin bins; Kelly capped |
| Saturation | 3/4 | Box office: trade-press consensus + informed retail; RT: low-to-moderate; no quants at this scale |
| **Total** | **15/20** | |

## Top markets

| Slug | Type | Vol_24h | Vol_all | State |
|---|---|---|---|---|
| `obsession-opening-weekend-box-office` | 5-bin bracket | $87K | $127K | Near-resolution >15m at 65% |
| `in-the-grey-rt-score` | 9-rung RT ladder | $40K | $97K | 1pp mid violation at ≥55/≥60 boundary |
| `michael-4th-weekend-box-office` | 4-bin bracket | $36K | $43K | >25m at 59%, 22–25m at 41% |
| `in-the-grey-opening-weekend-box-office` | 5-bin bracket | $21K | $24K | Near-resolved <3.5m at 90.5% |
| `highest-grossing-movie-in-2026` | 28-cand race | $140K | $7.15M | Year-long; Super Mario Galaxy 12.4% leader |
| `which-movie-has-biggest-opening-weekend-2026` | 27-cand race | $4K | $1.57M | Long-dated candidate race |

NegRisk: box-office brackets True (Σ=1 enforced); RT ladders False (monotonicity-only).

## Data sources

| Source | Access | Signal | Timing |
|---|---|---|---|
| The Numbers (`the-numbers.com`) | Free scrape | Resolution + Thursday preview gross | T+0 / T-36h |
| Box Office Mojo | Free scrape | Resolution confirmation | Same |
| Fandango / AMC / Atom advance tickets | Public scrape (no API; JS-rendered) | Pre-release demand proxy | T-7 to T-0 |
| Box Office Theory tracker threads | Public forums | Analyst consensus | Hourly opening weekend |
| Variety / Deadline weekend estimates | Public article scrape | Industry consensus (Comscore-syndicated) | Sun morning |
| Rotten Tomatoes | Free scrape (Cloudflare; unofficial API wrappers) | Resolution + live score | Continuous post-embargo |
| Metacritic | Free | Correlated signal (r≈0.85 with RT) | Same timeline |
| Review embargo lift date | Trade press | Directional prior (late = lower) | T-5 to T+0 |
| Prior-film RT (franchise/director) | Public | Bayesian prior | Pre-market-open |

**Thursday preview gross is the load-bearing signal**: posted ~11pm Thursday ET, 36h before Sunday actuals; r≈0.85–0.90 with final 3-day gross via genre-specific multiplier (horror 3–4×, superhero 4–6×, family 3–5×, drama 2–4×).

## Modeling spine

**Box-office bracket:**
```
P(gross ∈ bin_i) = F(threshold_high) − F(threshold_low)
F = empirical CDF from comp-set (5–10 films by genre × franchise × MPAA × quarter × budget)
   updated post-Thursday-preview via multiplier
```
Inputs ordered by predictive power: Thursday preview (T-36h hard signal) → advance-ticket proxy → comp-set CDF → trade-press tracking → competition adjustment.

**RT score ladder (Beta update):**
```
prior: Beta(α_0, β_0) from prior-film/franchise/genre
n reviews observed: α = α_0 + n·yes_frac, β = β_0 + n·(1−yes_frac)
P(score ≥ X) = 1 − F_Beta(X/100; α, β)
```
Monotonicity enforcement: isotonic regression / pool-adjacent-violators across rungs before comparing to market.

**Per-film effort:** First film 5–7 days (comp-set build + lognormal calibration + scraper deploy). Subsequent 2–3 days with reusable framework. Marginal cost drops sharply after films 3–4.

## Structural-arb shape

**RT monotonicity (live "In the Grey" 2026-05-16):**

| Rung | Mid | Bid | Ask | Spread |
|---|---|---|---|---|
| ≥55 | 0.100 | 0.040 | 0.160 | 0.120 |
| ≥60 | 0.090 | 0.040 | 0.140 | 0.100 |

Mid violation 1pp (P(≥55)=0.10 > P(≥60)=0.09 — monotonic; earlier capture morning of 2026-05-16 showed harder reversal P(≥55)=7% < P(≥60)=9.5%). Spread-adjusted: pure two-leg riskless arb at prevailing prices is loss-making (buy ≥55 at 0.16, sell ≥60 at 0.04 → net −0.12 on Yes-resolution). Becomes exploitable when `mid(≥X) < mid(≥X+5)` by more than `max(spread_X, spread_X+5)/2`. Automate daily Γ-check.

**Bracket Σ-check (NegRisk box-office):** ΣP(bin) ≈ 1.00 enforced. Obsession live: 0.65 + 0.345 + 0.0035 + 0.001 + 0.0005 = 1.000 (clean). Wider residuals on future/early-lifecycle events ("Backrooms", "Mandalorian"); run Σ-check at market open.

## Microstructure regime

- **Liquidity:** Top box-office event $87K 24h; sub-market depth $8K–$55K all-time; RT ladder $40K with $1K–$6K per rung. Thin.
- **Fees:** 5% taker / 25%-of-fee maker rebate (culture_fees). Thin tail bins → fee eats edge; favors limit-order entries.
- **Fee impact:** Buy ≥55 at ask 0.16 on $500 notional → fee $4; 1pp edge over mid → EV $5. Supports fractional Kelly f<0.20.
- **Event lifecycle:** Bracket markets launch T-5 to T-7; volume concentrates T-3 to Thursday night. After Thursday preview, market has partially resolved in price. Edge window T-7 to T-1.

## Saturation

- **Box-office:** Moderate. Studio internal models (Comscore, PostTrak, tracking data) accurate within 10–15% on wide-release openings; Deadline/Variety consensus published before every release. No institutional quants at $1K–$87K event scale (operational overhead prohibitive). Edge requires beating trade-press consensus by >1–2% on bracket CDF net of 5% fee.
- **Rotten Tomatoes:** Low-to-moderate. No known quant shop systematically trades RT ladders. Film critics with screening access cannot legally trade in US; offshore Polymarket creates ambiguity but score typically public pre-resolution.

## Decision-tree mapping

1. **Q1 YES-theme?** Box-office bracket: YES. RT ladder: YES. Annual race: PARTIAL.
2. **Q2 Data source?** YES — Thursday preview (T-36h hard), advance tickets, BOM/The Numbers, RT scrape, prior-film priors.
3. **Q3 Structural-arb?** YES — RT monotonicity + box-office Σ=1 NegRisk; automate daily.
4. **Q4 Microstructure?** Newly-listed brackets wider-spread; tail bins 650–900 bps per [[polymarket-microstructure]] SF1.

## Open follow-ups

1. Build 2024–2026 comp-set database from The Numbers historical tables (genre × franchise × MPAA × quarter). Reusable backbone.
2. RT scraper + monotonicity alert against live Gamma API; trigger `mid(≥X) < mid(≥X+5) − spread/2`.
3. Thursday preview gross automation (nightly pull on release dates).
4. Fandango advance-ticket scraper (headless browser); back-test correlation against Thursday preview gross.
5. RT Beta-model backtest on closed RT ladder markets (`closed=true` Gamma API); compute Brier vs market mid.
6. Annual race position: build year-end box-office calendar model for `highest-grossing-movie-in-2026`; Super Mario Galaxy Movie at 12.4% with 7-month horizon.
7. Pipeline guard: `end_date < today` check — "How to Make a Killing" RT (end 2026-02-23, still `active: True`) is documented false-open case.

## Source

- `raw/feasibility/movies/summary.md` (2026-05-16)
- Gamma API live pulls: `tag_slug=movies`, `tag_slug=box-office`, `tag_slug=rotten-tomatoes`
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]

## Related

- [[polymarket-strategy-matrix]]
- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
- [[polymarket-lp-incentives]]
- [[feasibility-review]]
