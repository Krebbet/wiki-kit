# Platform Comparison — Kalshi vs Polymarket

Industry-sizing and structural-comparison page using Falcon X's Jan/Feb 2026 piece "From Opinions to Odds" (`raw/research/polymarket-market-trends-and-llm-edge/06-falconx-emerging-trends.md`). Volume and OI figures sourced from **Allium** (on-chain dashboards) and **Artemis**; the underlying data is cross-verifiable on those platforms. Falcon X is a CFTC-registered swap dealer writing for institutional readers — treat as authoritative practitioner per the wiki's source criteria.

**As of Jan 31, 2026:** Polymarket and Kalshi are **neck-and-neck on open interest (~$400M each)** but Kalshi runs **~3× the monthly volume** ($9.5B vs $3.3B in Jan 2026). The two platforms diverge sharply on category mix (Kalshi ~90% sports notional vs Polymarket politics/sports/crypto majority), tick size (Polymarket per-market 0.001–0.01 vs Kalshi $0.01 transitioning to ≥4 decimal points — see "Tick size and price granularity" section for the revision against Falcon X's earlier $0.0001 claim), and fee model. Industry totals: **$64B in 2025** (4× vs 2024); January 2026 alone hit **$27B**, annualizing to **$325B+**. The Falcon X projection extrapolates BTC+ETH perp growth (78 % CAGR 2019–2025) onto prediction markets to suggest **>$1.1T by 2030** — illustrative, not a fitted model.

## Headline figures — sizing and growth

(All Jan/Feb 2026 snapshot unless noted; sourced from `raw/research/polymarket-market-trends-and-llm-edge/06-falconx-emerging-trends.md`.)

| Metric | Polymarket | Kalshi | Total / industry |
|---|---|---|---|
| Open interest (Jan 31, 2026) | ~$400M | ~$400M | — |
| Monthly volume (Jan 2026) | $3.3B | $9.5B | $27B (whole industry) |
| Annualized volume run-rate | — | — | $325B+ |
| 2025 full-year volume | — | — | $64B (4× vs 2024) |
| Polymarket DAU peak (Jan 2026) | ~100K | — | — |
| Robinhood prediction-market ARR (4Q25) | — | — | ~$435M (4× QoQ growth — fastest-growing line) |

**Volume / OI ratio reading.** At equal OI of ~$400M each, Kalshi's $9.5B vs Polymarket's $3.3B implies Kalshi turns over **~24× per month** vs Polymarket's **~8×** — Kalshi runs higher-velocity flow at the same standing-position size. This is consistent with Kalshi's heavier sports tilt (sports markets are short-lived, fast-resolving) and Polymarket's heavier politics tilt (longer-lived event markets).

**Growth context — perpetual futures analog.** Falcon X applies the BTC+ETH perp trajectory naively to prediction markets:

```
BTC + ETH perps:   $1T (2019) → $42T (2025)   ≈ 78% CAGR
                    78%-CAGR projection → $1.1T prediction-market by 2030
```

Illustrative only — no fitted model. Treat as anchoring intuition, not a forecast.

## Category mix — where the volume lives

### Kalshi

- **Sports ~90% of notional volume.** Sports also ~80% of trade count — larger average size on sports trades.
- Crypto, entertainment, politics rounding out the remainder.
- **Top-10 OI markets concentrate ~50% of total OI** — markedly more concentrated than Polymarket.
- **NFL cadence dominates weekly seasonality:** ~80% of Kalshi sports volume on Sundays (during NFL season). Falcon X notes Sunday drives 21% of Kalshi *monthly* volume — calendar-aware models should weight weekend liquidity.

### Polymarket

- **Politics and sports majority** of top-100 by volume; crypto significant.
- **Top-10 OI markets ~25% of total OI** — half the concentration of Kalshi (more dispersed).
- Polymarket also exposes a meaningful **Mentions / culture** layer via Pop Culture (435 markets; see [[mention-markets]]) — Kalshi does not currently match this category breadth in the captured material.
- **261 active Crypto markets** at 2026-05-13 with Pre-Market (token-launch FDV / sale) the single largest sub-bucket (115/261). See [[snapshots/polymarket-crypto-category-2026-05-13]].

### Per-vertical Polymarket vs Kalshi sizing (Late 2025)

Source: Sacra (`raw/research/polymarket-market-content-and-sizing/02-sacra-polymarket.md`). Numbers are *monthly volume by vertical* in late 2025.

| Vertical | Polymarket | Kalshi |
|---|---|---|
| Sports | ~$350M/mo | ~$1.1B/mo |
| Politics | ~$350M/mo | ~$75M/mo |

**Reading:** the platforms have **complementary** category specialisations. Kalshi has scaled on US sports (Robinhood drives **>50% of Kalshi volume** — Sacra); Polymarket retains the politics lead and the only meaningful Mentions/culture breadth. See [[polymarket-bet-content-trends]] for the longer category-mix synthesis.

### Polymarket-only monthly arc

Source: Sacra + TRM Labs (`raw/research/polymarket-market-content-and-sizing/01-trmlabs-21b-volume.md`).

| Period | Polymarket volume |
|---|---|
| FY 2023 | $73M |
| FY 2024 | ~$9B |
| H1 2025 | ~$6B |
| 2025 monthly (Jan – Sep) | ~$1.2B/mo |
| Sep 2025 onward | sharp acceleration ("new regime of double-digit billions") |
| Oct 2025 monthly | $3.02B/mo (monthly record at time of writing) |
| Jan 2026 monthly | $3.3B (Falcon X) |
| **Feb 28 2026 single-day Polymarket record** | **$425M** (TRM, surpassed Election Day 2024) |

The TRM "$20B+ monthly" headline figure for January 2026 is **multi-platform**: Polymarket + LIMITLESS + Opinion Market + predict.fun, **Kalshi-excluded**. Kalshi adds another $9.5B/mo (Jan 2026, Falcon X). When citing "industry volume," carry the platform scope explicitly — see [[polymarket-bet-content-trends]] for the reconciled multi-source picture.

### Corporate / capital structure

Source: Sacra (`raw/.../02-sacra-polymarket.md`). Polymarket has raised ~$2.764B in disclosed primary capital through April 2026, with **ICE (Intercontinental Exchange) holding ~23% of outstanding (~14% fully diluted; carrying value ~$2.0B as of March 2026)**. Key inflections: $45M Series B at ~$1B (May 2024), $1.0B ICE Series D at ~$8B pre-money (October 2025), $600M ICE Series E at ~$8B pre-money (March 27, 2026), Bloomberg-reported $400M raise at $15B valuation (April 20, 2026). MLB signed as exclusive Official Prediction Market Exchange Partner (March 2026).

### Fee Structure V2 (effective March 30, 2026)

Source: Sacra. Polymarket charged **zero trading fees throughout 2025**; introduced taker fees on high-frequency crypto markets in January 2026; rolled to sports in February; full V2 schedule from March 30:

| Category | Taker fee | $-equivalent at p = 0.50 |
|---|---|---|
| Crypto | 0.072 | $1.80 / 100 shares |
| Sports | 0.030 | $0.75 / 100 shares |
| Finance / Politics / Tech / Mentions | 0.040 | $1.00 / 100 shares |
| Economics / Culture / Weather / Other | 0.050 | $1.25 / 100 shares |
| **Geopolitics / World Events** | **0%** | (fee-free) |
| Makers (all categories) | 0 + rebates funded by taker fees | — |

Under the US-specific QCX CFTC designation, Polymarket is filed at 30 bps taker / 20 bps maker rebate. The pre-V2 platform "no Polymarket protocol revenue, fees redistributed to LPs" structure (Grayscale, Sep 2024 — 2% winning-bet fee fully to LPs, $3M+ USDC LP incentives paid by Sep 2024) is now superseded; V2 captures a non-zero take rate.

Kalshi take rate is ~1% (Sacra) — Sacra-estimated **$24M revenue in 2024, +1,221% YoY**.

## Structural / microstructure differences

### Tick size and price granularity

- **Polymarket: variable per-market**, observed `0.01` and `0.001` on the live Gamma API (`orderPriceMinTickSize` field) on 2026-05-14. Sub-markets with central probabilities (e.g., 31.5%) use `0.01`; sub-markets with tail probabilities (e.g., 3.75%) use `0.001`. The `$0.0001` (4-decimal) claim from Falcon X (Jan 2026) was not reproduced — either stale, applies to specific markets we haven't sampled, or was inaccurate in the original source. The min tick narrows where the price has more room to move in absolute cent-terms.
- **Kalshi: $0.01** today, transitioning to ≥4 decimal places per Falcon X.

Implication: Polymarket's per-market tick adaptation already gives tail markets finer granularity (`0.001` = 0.1¢) than Kalshi's flat `0.01`. The "tighter spreads vs Kalshi" intuition still holds on tail markets specifically; the headline `$0.0001` claim does not hold across the captured sample. Cross-link to [[polymarket-microstructure]] for empirical spread behaviour on Polymarket (longshot half-spreads still 650–900 bps at `p < 0.10` despite the fine tick — the tick is not the binding constraint on tail spreads; inventory risk is). Also `master_notes.md` 2026-05-14 logs this revision as an open project-scope item pending broader sampling.

### Spread compression timing

Falcon X observes a **monotone decline of median spread toward the $0.01 floor as markets mature**:

- Newly-listed markets (cross-listed within 3 days of resolution — Kalshi top-100 sample): spreads materially wider.
- 7 days+ from resolution: median spread near the $0.01 minimum tick.

Operational reading: **spread elevation at listing is exploitable for patient liquidity provision**, but **the window is short** — 60% of Kalshi top-100 markets are listed within 3 days of resolution. The opportunity is narrow in calendar terms.

This is the cross-platform analog of the within-Polymarket maturation pattern documented in [[polymarket-liquidity-evolution]] (arb half-life 2 hr → 0.74 min on Trump YES Apr–Oct 2024) — both show maturation compresses microstructure friction monotonically.

### Volume concentration on final day

**60% of volume on the final day** of a Kalshi top-100 market's life. Turnover-to-OI ratio: **200–500%** on day 0 and day 1. Implication: most price discovery happens late in the lifecycle, but spread compression has already occurred by then — entry on the final day captures liquidity but not the wide-spread opportunity.

This matches the [[polymarket-microstructure]] SF8 depth-decay finding (mean depth decays as resolution approaches) and inverts the usual options-market intuition (where depth peaks at expiry). The combination — depth dropping while volume spikes — implies elevated price impact on late entries.

### Sports market 3-second delay (Polymarket)

Polymarket imposes a **3-second delay** on sports market orders to protect market-makers from holders of real-time data feeds. Signal: sports arbitrage is a *known and actively contested* category on Polymarket. Cross-link to [[single-market-arbitrage-empirics]] for the NBA empirical study (median in-game arb window 3.6 seconds — the 3-second delay puts most retail traders outside the executable window) and to [[arbitrage-taxonomy]] for Saguillo et al.'s observation that **sports is opportunity-rich but largely absent from realized extraction** — the 3-second delay is part of why.

## Resolution mechanism differences

| | Polymarket | Kalshi |
|---|---|---|
| Settlement | UMA Optimistic Oracle for ambiguous; Chainlink for deterministic / financial events | Predefined official source per market; CFTC-regulated |
| Dispute mechanism | Optimistic-oracle with bonded challenges (see [[uma-optimistic-oracle]]) | None (objective settlement) |
| Collateral | USDC, fully collateralized; `Σ(Yes + No) = $1.00` enforced | Fully collateralized; no leverage |
| Leverage | None on either platform currently | None |
| Settlement payoff | Winning share = $1.00 (in USDC) | Winning share = $1.00 |

The dual-oracle split on Polymarket (UMA + Chainlink) is a piece of platform-architecture detail not currently surfaced on [[polymarket-architecture]] or [[uma-optimistic-oracle]] — both should be updated to reflect that Chainlink handles deterministic / financial events while UMA handles ambiguous events. Logged as a maintenance task.

## Fee structures

- **Polymarket international:** zero trading fees on most markets; select markets (e.g., 15-minute crypto) carry fees.
- **Polymarket US:** 10 bp taker fee.
- **Kalshi:** dynamic fee schedule — fees higher when `p ≈ $0.50` (high uncertainty), lower when `p ≈ $0.99` (high certainty). No explicit equation in the source.

Operational implication: Kalshi's fee structure penalizes informed trading on mid-confidence markets (which is where the [[mention-markets]] MCP-edge zone sits per Kim et al.); Polymarket's flat (international) or 10 bp (US) fee is neutral on confidence regime. **For mention-market MCP-style strategies, Polymarket has a fee-structural advantage** (when the per-market resolution-criteria capture flow exists — see capture gap noted in [[mention-markets]]).

## Maturity reading

Combining the Jan 2026 snapshot with [[polymarket-liquidity-evolution]] (Trump YES Kyle's λ 0.53 → 0.01 over Apr–Oct 2024):

- **2024:** Polymarket-led volume during election cycle; classic immature-market behaviour with persistent arb deviations and high price impact.
- **2025:** Industry quadruples (Falcon X $64B); Kalshi gains share via sports.
- **Jan 2026:** Kalshi overtakes Polymarket on monthly volume despite equal OI; industry annualizes to $325B+; Robinhood emerges as third pole with $435M ARR.

For the wiki's edge-finding focus, the trajectory implies:
- **Pure-mechanical arbitrage edges are compressing** as both platforms mature and automated participation grows.
- **Category-divergent edges are widening:** Polymarket's Mentions / culture markets are a category Kalshi does not match; Kalshi's sports-day cadence is a category Polymarket trades differently. Edge lives in the platform-specific category specializations, not the platform commonalities.

## Participant profile — sparse

The captured data covers **aggregate** flow well but **participant distribution** is thin. What's currently in the wiki:

- **Polymarket DAU peak ~100K** in Jan 2026 (this page above).
- **Top arbitrageur** wallet `0xd218e4…` extracted $2.0M in 4,049 transactions; log-linear profit-vs-transactions profile of top-10 accounts consistent with automated bots, not manual operators — see [[arbitrage-taxonomy]].
- **Maker-side concentration is broadly low** (median HHI 0.031 ≈ 32 effective makers across 600 markets) but rises sharply in thin markets (max HHI 0.40 ≈ 3 effective makers) — see [[polymarket-microstructure]] SF4.

**Not currently captured** in the wiki: full wallet-size distribution (retail vs whale shares), copy-trading networks, cross-vertical participant overlap, Polymarket vs Kalshi user overlap. These are open follow-ups; the prior `/research` run flagged that `theverge.com/news/922925/polymarkets-top-0-1-percent` reports the top 0.1%-by-wallet share but the wiki has not yet ingested it.

### TRM user-cohort segmentation (Jan 1 – Mar 22 2026)

TRM Labs on-chain analysis (`raw/research/polymarket-market-content-and-sizing/01-trmlabs-21b-volume.md`) — five tiers by fill count, multi-platform (Polymarket + LIMITLESS + Opinion Market + predict.fun):

| Tier | Fills | % of trades | Volume captured | Median trade |
|---|---|---|---|---|
| First-time | 1 | <0.2% | $3.5M | $30 |
| Active | 11–1,000 | **44.7%** | $869M | — |
| Market maker | >10,000 | **35.2%** | $774M | **$12** |

Active (mid-frequency) and Market maker cohorts dominate by *trade count*; Market makers carry near-equal volume to Active despite far fewer wallets. Median MM ticket of $12 is the spread-capture signature. Top-10 wallets each generated $660K–$6.2M over the 80-day window; six of ten traded *every day*. See [[polymarket-bet-content-trends]] for the wallet case studies.

### Unique-wallet growth

TRM: ~840,000 unique wallets/month (multi-platform) by Feb 2026, **tripled in the six months prior**. Aligns with the Sep 2025 onward volume regime change. Polymarket-only DAU peak ~100K (Jan 2026, this page above).

## Source

- `raw/research/polymarket-market-trends-and-llm-edge/06-falconx-emerging-trends.md` — Falcon X (Jan/Feb 2026), "From Opinions to Odds: Emerging Trends in the Prediction Market Landscape". Allium + Artemis data; CFTC-registered swap dealer; methodology disclosed. Volume/OI figures snapshot as of Jan 31, 2026.
- `raw/research/polymarket-market-content-and-sizing/01-trmlabs-21b-volume.md` — TRM Labs (May 2026); on-chain ingestion of Polygon contract logs; user-tier segmentation, monthly volume arc, top-wallet P&L.
- `raw/research/polymarket-market-content-and-sizing/02-sacra-polymarket.md` — Sacra company profile through April 2026; volume arc, fee structure V2, per-vertical Polymarket/Kalshi splits, ICE capital structure, Robinhood-Kalshi relationship.
- `raw/research/polymarket-market-content-and-sizing/07-grayscale-polymarket.md` — Grayscale (Sep 11, 2024); pre-V2 fee model and earlier-cycle context.

## Related

- [[polymarket-architecture]]
- [[polymarket-microstructure]]
- [[polymarket-liquidity-evolution]]
- [[uma-optimistic-oracle]]
- [[single-market-arbitrage-empirics]]
- [[arbitrage-taxonomy]]
- [[mention-markets]]
- [[polymarket-bet-content-trends]]
- [[snapshots/polymarket-top-markets-2026-05-13]]
- [[snapshots/polymarket-crypto-category-2026-05-13]]
- [[conflicts/wash-trading-share]]
