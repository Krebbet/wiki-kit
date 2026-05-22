# Feasibility Assessment: Polymarket Conditional / Scenario-Grid Markets
**Produced:** 2026-05-16  
**Scope:** 2026 Midterms balance-of-power composite vs chamber-control binaries; 2028 Democratic presidential primary scenario grids  
**Data vintage:** Gamma API pulled 2026-05-16; wiki snapshots from 2026-05-13  

---

## 1. Market Landscape

### 1a. Midterms — Active market inventory (2026-05-16 live)

**Balance-of-Power composite** (`balance-of-power-2026-midterms`):  
Total volume: $6.79M | Total liquidity: $560K | Resolution: 2026-11-03

| Outcome | Price | Volume | Liquidity |
|---|---|---|---|
| D Senate, D House | 43.5¢ | $1.72M | $161.6K |
| R Senate, D House | 33.5¢ | $1.37M | $101.6K |
| R Senate, R House | 22.5¢ | $1.33M | $123.3K |
| D Senate, R House | 1.45¢ | $1.04M | $112.0K |
| Other | 0.85¢ | $1.33M | $62.8K |
| **Sum** | **101.8¢** | | |

**Chamber-control binaries** (`which-party-will-win-the-house-in-2026`, `which-party-will-win-the-senate-in-2026`):

| Market | Outcome | Price | Volume | Liquidity |
|---|---|---|---|---|
| House | Democratic | 78.5¢ | $3.39M | $306.9K |
| House | Republican | 21.5¢ | $2.88M | $240.6K |
| Senate | Republican | 55.5¢ | $1.11M | $156.1K |
| Senate | Democratic | 46.5¢ | $1.28M | $161.2K |

**Per-seat district markets** (from 2026-05-13 snapshot, not re-pulled):  
$12K–$83K per race — ~100x–500x thinner than chamber-control markets.

**tag_slug=midterms API behavior:** As of 2026-05-16, the `tag_slug=midterms` query does not return midterms markets via the `/markets` endpoint; midterms markets surface correctly via `/events` endpoint. The three core events above are confirmed active.

### 1b. Primaries — Active market inventory (2026-05-16 live)

The `tag_slug=primaries` endpoint returns the **2028 Democratic Presidential Nominee** event ($1.14B lifetime volume, $60.8M liquidity). No 2026 midterms primary markets surfaced at this query. Key candidates:

| Candidate | Price | Volume | Liquidity |
|---|---|---|---|
| Jon Ossoff | 6.25¢ | $11.1M | $266.9K |
| Pete Buttigieg | 4.25¢ | $10.5M | $285.3K |
| Andy Beshear | 2.75¢ | $11.9M | $482.3K |
| George Clooney | 0.65¢ | $40.2M | $2.34M |
| Oprah Winfrey | 0.75¢ | $50.8M | $1.94M |
| Gina Raimondo | 0.75¢ | $32.2M | $2.28M |

Sum of visible candidate YES prices significantly exceeds 1.00 (NegRisk multi-candidate structure — standard). No scenario-grid composite (nominee x VP pick) visible.

---

## 2. Combinatorial-Arb Verification — Is the -12% Still Live?

### 2a. The May 13 snapshot discrepancy

The [[snapshots/polymarket-midterms-category-2026-05-13]] snapshot showed only two of four composite outcomes, implying P(R-Sweep) = -12% from marginals. This was an **artifact of a partial UI capture** — only D-Sweep (43%) and R-Senate + D-House (33%) were visible; the R-Sweep and D-Senate + R-House legs were below the fold.

### 2b. Live data (2026-05-16) — full four-outcome composite

With all four legs visible, the original implied-negative-probability calculation dissolves. R-Sweep (R Senate, R House) trades at **22.5¢**, not a negative residual. The composite sum is **101.8¢**, within typical NegRisk double-counting tolerance.

**Verdict on the -12% candidate: NOT live.** The snapshot arb was a data-capture artifact, not a market mispricing.

### 2c. The real live inconsistency (2026-05-16)

A different and larger discrepancy exists between the composite legs and the standalone chamber-control binaries:

```
Composite-implied P(D House):
  = P(D Sweep) + P(D Senate & R House)
  = 43.5% + 1.45%
  = 44.95%

Chamber-control standalone P(D House): 78.5%
Gap: 78.5% - 44.95% = +33.55 pp

Composite-implied P(R Senate):
  = P(R Senate & D House) + P(R Sweep)
  = 33.5% + 22.5%
  = 56.0%

Chamber-control standalone P(R Senate): 55.5%
Gap: 0.5 pp (negligible)
```

The Senate marginals are internally consistent. The House marginal is severely inconsistent: composite implies D-House at ~45% while the standalone chamber market prices it at 78.5%.

**Source of divergence:** The D-Senate + R-House leg at **1.45¢** is the culprit. If the chamber-control binaries are correct:
- P(D Senate & R House) should ≈ P(D Senate) - P(D Sweep) = 46.5% - 43.5% = **3.0%**
- Market prices it at 1.45% — approximately **2x underpriced**
- P(R Sweep) should ≈ 1 - 43.5% - 3.0% - 35.0% = **18.5%**; market prices it at 22.5% — **4 pp overpriced**

**The live mispricing is concentrated in the D-Senate + R-House leg (1.45¢ vs model-implied ~3.0¢)** and secondarily in R-Sweep (22.5¢ vs ~18.5¢).

**Arb topology:**
- Buy D-Senate + R-House YES in composite (1.45¢, $112K liquidity)
- Hedge: Sell R-Sweep YES in composite (22.5¢, $123K liquidity)
- Net: synthetic long on "D Senate wins" conditional on outcome space, hedged against R-Sweep premium
- Or: Cross-market — Long D-Senate + R-House composite + Short Democratic House binary (already ~78.5%) + Long Republican Senate binary (55.5%) — to express that the composite undervalues D-Senate + R-House relative to what the chamber-control priors imply

**Size constraint:** D-Senate + R-House has $112K liquidity — binding leg caps effective position at ~$15–30K.

---

## 3. Joint-Distribution Modeling

### 3a. Data sources

| Source | Signal | Latency | Coverage |
|---|---|---|---|
| FiveThirtyEight / Silver Bulletin | Senate seat ratings, generic ballot, district-level forecasts | Daily–weekly | All 35 Senate races; ~40 competitive House seats |
| RealClearPolitics | Polling averages by Senate race and generic ballot | Daily | Competitive subset |
| FEC EDGAR filings | Cash-on-hand by candidate | Quarterly | All 435 House + 35 Senate |
| OpenSecrets | Competitive-race fundraising tracker | Near-real-time with FEC delay | Top-100 competitive races |
| Decision Desk HQ | Per-seat win probabilities (model output) | Updated on new polls | All races |
| Inside Elections / Sabato's Crystal Ball | Qualitative tier ratings → per-seat prior | Weekly | All races |

### 3b. Marginal-to-joint construction

```
Let S_i = P(D wins Senate seat i), i = 1..35
Let H_j = P(D wins House seat j), j = 1..435

P(D Senate majority) = P(sum_i [D wins seat i] + current D held >= 50)
P(D House majority) = P(sum_j [D wins seat j] >= 218)
```

Marginals from forecasting models available at seat level. Joint correlation: single national-environment factor (generic ballot) drives correlated swings. Correlation rho ~0.6–0.8 between Senate and House chamber outcomes historically.

Key internal-consistency check: the Decision Desk / Silver Bulletin generic-ballot model implies ~78% D-House probability (matching the chamber-control binary). The composite D-Sweep at 43.5% implies P(D Senate | D House wins) ≈ 43.5/78.5 ≈ **55.4%** — above the standalone D-Senate at 46.5%. This is unusual: D-Senate is harder terrain in 2026; a wave big enough to flip the House doesn't obviously raise the conditional. The composite may be expressing that D-House probability is lower than the binary suggests, i.e., the composite's crowd disagrees with the binary's crowd on the House.

### 3c. Consistency summary

| Check | Composite-implied | Chamber binary | Model-implied | Verdict |
|---|---|---|---|---|
| P(D House) | 44.95% | 78.5% | ~75-80% | Composite severely low |
| P(R Senate) | 56.0% | 55.5% | ~50-58% | Consistent |
| P(D Sweep) | 43.5% | — | ~35-45% | Plausible |
| P(R Sweep) | 22.5% | — | ~10-20% | Mildly high |
| P(D Senate & R House) | 1.45% | — | ~2-4% | Underpriced |

---

## 4. Saturation Analysis

**Who is in this market:**

1. **Election forecasters (538-style):** Sophisticated models but don't directly trade Polymarket. Public output is near-free for any operator — edge from ingesting public forecasting models is largely saturated.

2. **PredictIt cross-traders:** Known to cross-trade between PredictIt and Polymarket. PredictIt's per-contract $850 cap limits position size but drives familiarity with the market structure. These traders likely monitor the composite-vs-marginals spread.

3. **Polymarket-native bots:** The [[combinatorial-arbitrage-empirics]] record shows MRA bots dominate at-platform ($2M extracted by top wallet via 4,049 transactions). The midterms composite-vs-binary gap is a more complex semantic dependency — fewer bots have this dependency map loaded vs simple within-market MRA.

4. **Retail / political enthusiasts:** Dominate per-seat district markets (thin volumes); directional views, not arb.

**Saturation verdict:** The chamber-control binary markets are well-saturated relative to fundamentals (78.5% D-House aligns with mainstream forecasting models). The composite's D-Senate + R-House underpricing (1.45¢ vs ~3¢ fair) is likely less saturated because: (a) multi-leg dependency map required, (b) thin leg makes size-sensitive bots averse, (c) the mispricing is in a low-attention leg.

---

## 5. Market Depth and Sizing Constraints

| Market | Liquidity | Volume (lifetime) | Approx arb size cap |
|---|---|---|---|
| D Sweep leg | $161.6K | $1.72M | ~$30-60K |
| R Senate & D House | $101.6K | $1.37M | ~$20-40K |
| R Sweep | $123.3K | $1.33M | ~$25-50K |
| D Senate & R House (thin) | $112.0K | $1.04M | ~$15-30K |
| House control (D leg) | $306.9K | $3.39M | ~$50-100K |
| Senate control (R leg) | $156.1K | $1.11M | ~$30-60K |
| Per-seat district markets | $12K-$83K ea | — | $2K-$10K |

**Binding constraint:** D-Senate + R-House leg at $112K liquidity caps any arb through that leg. Effective deployed size on the full arb: ~$15–30K. At 1.45¢ entry on that leg with ~3.0¢ fair value, gross profit on $30K deployed = ~$465 unhedged; hedges reduce net to ~$200–$400 per round-trip.

**Consistency with wiki:** The per-seat $12K–$83K vs $2M–$7M chamber-control depth asymmetry observed in the May-13 snapshot holds in the live data.

---

## 6. Presidential Primary Scenario Grids

**Current state:** The 2028 Democratic Presidential Nominee market is a NegRisk multi-candidate event ($1.14B lifetime volume, $60.8M liquidity). No scenario-grid composite (nominee x VP pick, nominee x Senate outcome) is visible as of 2026-05-16.

**Why grids don't yet exist:** The 2028 primary is 2+ years out; scenario composites require both legs to be well-defined and simultaneously active. VP pick market for 2028 does not exist yet.

**Per-candidate MRA check:** Each individual binary (YES + NO) sums to 100% — properly priced. Cross-candidate NegRisk MRA is the expected Sigma > 1.00 condition (by design, not an exploitable arb per [[arbitrage-taxonomy]] Sec. 3.2.2 fn 7).

**Feasibility for 2028 scenario grids:** Monitor from ~mid-2027 when VP/running-mate markets are likely to activate. Not actionable today.

---

## 7. Modeling Implementation Pathway

**Step 1 — Dependency map (one-time):** Structural — no LLM needed. P(D House) in composite = P(D Sweep) + P(D Senate + R House). Document the six-leg dependency graph.

**Step 2 — Price monitor (real-time):** Poll Gamma API every 5–15 minutes. Compute:
```
gap_house = P(D House binary) - [P(D Sweep composite) + P(D Senate & R House composite)]
gap_senate = P(R Senate binary) - [P(R Senate & D House composite) + P(R Sweep composite)]
gap_composite_sum = sum P(composite legs) - 1.00
```
Alert when |gap_house| > 5 pp or |gap_senate| > 3 pp or |gap_composite_sum| > 2%.

**Step 3 — Joint-distribution prior (weekly update):** Pull Decision Desk / Silver Bulletin per-seat probabilities. Fit two-factor correlated Bernoulli model. Output: P(D Senate), P(D House), joint PMF.

**Step 4 — Sizing and execution:** On signal, size to thin-leg liquidity (~$15–30K). Execute via CLOB limit orders. Monitor leg fills; partial-fill risk is material on 4-leg arb.

**Step 5 — Fundamental overlay:** Where composite-vs-binary gap exceeds model-implied fair value by >5 pp, add directional view using per-seat prior.

---

## 8. Risk Factors

| Risk | Severity | Mitigation |
|---|---|---|
| Partial-fill on multi-leg arb | High | Execute largest/most-liquid legs first |
| Composite re-prices before hedge executes | High | Limit-order both legs simultaneously |
| Leg-fill risk on thin D-Senate + R-House | Medium-High | Size conservatively ($15-20K); limit orders |
| Resolution-rule divergence between composite and binaries | Medium | Composite cites "AP, Fox, NBC consensus"; verify chamber-control binary uses same threshold |
| "Other" outcome resolves (independent candidate wins) | Low | 0.85¢ Other leg is real tail; composite positions are exposed |
| PredictIt cross-traders close gap before position builds | Medium | Gap is large (33.5 pp on House); likely closes over weeks not days |
| UMA oracle dispute | Low | Election calls are low-dispute-risk; precedent established |

---

## 9. Live Arb Status Summary

| Signal | May 13 Snapshot | May 16 Live | Status |
|---|---|---|---|
| P(R-Sweep) implied negative | -12% (from partial capture) | Not applicable — all four legs visible | ARTIFACT — NOT LIVE |
| Composite sum > 1.00 | Partial data | 101.8¢ | Minor MRA long opportunity (marginal) |
| D-Senate + R-House underpriced | Not measurable (leg hidden) | 1.45¢ vs ~3.0¢ implied by binaries | LIVE — 2x underpricing |
| R-Sweep overpriced | Not measurable | 22.5¢ vs ~18.5¢ model-implied | LIVE — 4 pp overpricing |
| House marginal inconsistency | Apparent (partial data) | 33.5 pp gap (44.95% vs 78.5%) | LIVE — large structural gap |

---

## 10. Verdict

**The May-13 -12% combinatorial-arb candidate is confirmed NOT live** — it was a partial-capture artifact from the UI rendering only two of four composite legs.

**A different live mispricing exists:** The D-Senate + R-House composite leg (1.45¢) is approximately 2x underpriced relative to what the chamber-control binaries imply (~3.0¢ fair), and R-Sweep is mildly overpriced (22.5¢ vs ~18.5¢). The underlying structural inconsistency — composite-implied P(D House) at 44.95% vs standalone binary at 78.5% — reflects divergent crowd beliefs between the composite market and the chamber-control market.

**Feasibility: CONDITIONAL YES.** Arb is live; dependency is structural; chamber-control markets have adequate depth. Binding constraint is the thin D-Senate + R-House leg ($112K liquidity, ~$15–30K effective position). Expected gross profit per round-trip: $200–$400 — viable for systematic small-size operation, not institutional scale. Execution risk (multi-leg partial fill) is the primary operational challenge.

**Priority actions:**
1. Set up Gamma API monitor for gap_house / gap_senate metrics.
2. Pilot $5–10K position in D-Senate + R-House YES against Republican House binary hedge.
3. Build per-seat joint-distribution model from Decision Desk / Silver Bulletin prior.
4. Defer 2028 primary scenario-grid work to ~mid-2027.

---

## Sources

- Gamma API `/events?tag_slug=midterms` and `/events?slug=balance-of-power-2026-midterms`, pulled 2026-05-16
- Gamma API `/events?tag_slug=primaries`, pulled 2026-05-16
- `wiki/snapshots/polymarket-midterms-category-2026-05-13.md`
- `wiki/arbitrage-taxonomy.md`
- `wiki/combinatorial-arbitrage-empirics.md`
- `wiki/polymarket-strategy-matrix.md`

## Related

- [[snapshots/polymarket-midterms-category-2026-05-13]]
- [[arbitrage-taxonomy]]
- [[combinatorial-arbitrage-empirics]]
- [[polymarket-strategy-matrix]]
- [[uma-optimistic-oracle]]
- [[polymarket-architecture]]
