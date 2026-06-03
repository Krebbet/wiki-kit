# Prediction Market House Edge and Take Rates

On prediction markets, the "house" in the traditional sense does not exist: the platform is a peer-to-peer exchange that earns an explicit transaction fee and takes no position on outcomes. The actual cost of trading has two distinct components: (1) the explicit fee charged per contract, which varies widely across platforms and is well-documented, and (2) a structural behavioral disadvantage that causes takers—and to a lesser extent makers—to earn negative expected returns well beyond what fees alone would explain. The second component is a consequence of the favorite-longshot bias (FLB), a documented pattern in which low-probability contracts are systematically overpriced relative to their actual win rates. Conflating these two costs produces a distorted picture of venue economics. Understanding them separately is prerequisite to any sensible venue selection or market-making strategy.

---

## The Two Components of Cost

### 1. Platform Fees (Explicit)

Every platform charges a transaction fee, but the structure, magnitude, and which side pays it vary substantially.

**Kalshi (pre-April 2025 taker-only regime):** fee per contract = `γ × P × (1 − P)`, where γ = 0.07 and P is the price in dollars. This is zero-sum symmetric around 0.50: fee peaks at $0.0175 per contract (1.75% of a $1 contract) at P = 0.50 and shrinks toward zero at the extremes. The formula means cheap longshots cost almost nothing in absolute fees but very large amounts relative to the contract price. After April 2025, Kalshi introduced maker fees as well; the Whelan et al. dataset ends at this cutoff and does not capture the revised regime (`raw/research/house-edge-and-market-making/10-kalshi-economics-whelan-2026.md`).

**Polymarket V2 (Sports, effective March 30, 2026):** taker fee formula is `fee = C × p × 0.03 × (p × (1−p))^1`, where C is contracts and p is price. Peak effective fee is 0.75% at p = 0.50. Geopolitics & World Events markets are completely fee-free. Sell orders are not subject to taker fees. Makers pay zero and receive rebates funded by taker fees (`raw/research/house-edge-and-market-making/06-polymarket-trading-fees-v2.md`).

**Sportsbooks:** charge no explicit fee; instead, 4.5–5% is baked into the odds as an implicit hold (vig). On a two-way market the sum of implied probabilities exceeds 1 by 4–5 percentage points. This hold is invisible until you calculate it (`raw/research/house-edge-and-market-making/05-pm-vs-sportsbooks-vig.md`).

### 2. Structural Behavioral Disadvantage (Implicit, Distinct from Fees)

The Whelan, Bürgi & Deng (2026) study examined 46,282 distinct Yes contracts on Kalshi from 2021 through April 2025. Key finding: the average post-fee return for takers was **−31.46%** and for makers was **−9.64%**. Because the market is zero-sum in dollar terms before fees, the average pre-fee return across all contracts should be zero. Instead, the dataset shows an average pre-fee return on any given Kalshi contract of **−20%** (`raw/research/house-edge-and-market-making/10-kalshi-economics-whelan-2026.md`).

This -20% pre-fee average is not a fee artifact—it is a consequence of the asymmetric distribution of contracts. Two-thirds of all observed contracts are priced below 10¢ or above 90¢. The FLB penalizes the cheap end severely: contracts at 1–10¢ win far less often than their price implies, producing large negative returns. High-price contracts earn small positive returns. Because cheap contracts are so numerous, the per-contract average return is pulled deeply negative even before fees are applied.

**Why FLB exists in this market:** Whelan et al. model two mechanisms. First, agents self-select into making versus taking based on belief extremity: takers have more extreme views than makers and accept worse prices in exchange for immediate execution certainty. Second, there is a modest but statistically necessary overestimation of small probabilities (analogous to Kahneman-Tversky probability weighting). The model calibration finds a bias parameter β ≈ 0.09 (9% shrinkage of beliefs toward 0.50) is sufficient to reproduce the observed FLB pattern for both sides. This is not large irrational bias—it is a small tilt that compresses catastrophically at the cheap end of the price range.

The FLB is a peer-to-peer transfer, not a platform extraction: money flows from poorly-calibrated takers of cheap contracts to the makers who hold the other side. The platform collects fees on top, but the behavioral component is independent and larger for takers.

**FLB by category (Mincer-Zarnowitz ψ coefficient, full sample ψ = 0.034***):**

| Category | ψ | Significance |
|---|---|---|
| Crypto | 0.058 | *** |
| Other | 0.053 | *** |
| Financials | 0.032 | *** |
| Climate & Weather | 0.031 | *** |
| Economics | 0.034 | *** |
| Politics | 0.022 | not individually significant |
| Entertainment | 0.020 | not individually significant |

Crypto has the strongest FLB; Politics and Entertainment are weakest (though the null of unbiased pricing is still rejected at the event level for both).

**FLB over time:** ψ = 0.048*** in 2024, declining to ψ = 0.021* in 2025, suggesting the bias is weakening—potentially as the market matures and more sophisticated participants enter. The directional trend matters for anyone building a maker strategy around FLB capture.

---

## Per-Platform Fee Breakdown

### Full Platform Comparison

Source: DeFiRate, "Prediction Market Fees: Kalshi, Polymarket, Robinhood & Coinbase," February 2026 (`raw/research/house-edge-and-market-making/07-defirate-pm-fees-comparison.md`):

| Exchange | Fee model | Trading fee | Maker fee |
|---|---|---|---|
| Kalshi | Formula-based | 0.07–1.75% (50/50 at 1.75%) | up to 0.44% |
| Polymarket Global | Profit-based | 0% most markets | 0% |
| Polymarket US | Taker fee | 0.10% (10 bps) | 0% |
| Robinhood | Flat per-contract | $0.02 total | 0% |
| FanDuel Predicts | Payout-based | 2% of potential payout | 0% |
| DraftKings Predictions | Flat per-contract | $0.01 + exchange fee | 0% |
| ForecastEx | Built into spread | $0.01/contract | 0% |
| PredictIt | Profit + withdrawal | 10% of gross profits | 0% |

**Note on maker fees post-April 2025:** Kalshi began charging maker fees after April 2025, which is why Whelan et al. end their dataset there. The DeFiRate table reflects the post-April 2025 regime, showing makers paying up to 0.44%. The Whelan dataset reflects the taker-only period and cannot be used to draw conclusions about maker economics under the current fee regime.

### Worked Cost Examples

**$100 position at coin-flip odds (p ≈ 0.48):**

| Platform | Total Fees |
|---|---|
| Polymarket US | $0.10 |
| Kalshi | $3.51 |
| Robinhood / FanDuel / DraftKings / Crypto.com | $4.00 |
| PredictIt | $20.68 |

**$10,000 position at 0.76 favorite:**

| Platform | Total Fees |
|---|---|
| Polymarket US | $10 |
| Kalshi | $165 |
| Robinhood / FanDuel / DraftKings | $256 |
| PredictIt | $958 |

### Polymarket

Geopolitics & World Events: fee-free. Sports markets (V2, effective March 30, 2026): peak 0.75% at p = 0.50 using the formula above. Sell orders are not subject to taker fees. Makers pay zero and receive rebates funded by taker fees—the rebate structure creates a structural maker incentive even on categories with non-zero taker fees. See [[polymarket-lp-incentives]] for detail on the rebate program.

The Polymarket fee schedule anticipates future expansion of the V2 structure to Finance, Politics, Economics, Culture, Weather, and Tech categories (`raw/research/house-edge-and-market-making/06-polymarket-trading-fees-v2.md`).

### Kalshi

Standard markets: fee = 0.07 × P × (1 − P) per contract. Maximum 1.75% at P = 0.50. At P = 0.10, fee ≈ 0.63%; at P = 0.90, fee ≈ 0.63%; at P = 0.50, fee = 1.75%.

**S&P 500 and Nasdaq-100 markets use a halved multiplier** (0.035 instead of 0.07), making them 50% cheaper than standard Kalshi contracts. At P = 0.50 this implies a 0.875% taker fee (`raw/research/house-edge-and-market-making/07-defirate-pm-fees-comparison.md`).

Maker fees (post-April 2025): up to 0.44%. The DeFiRate case study (June 2025, Rufus Peabody) documented extreme maker fee outcomes at very low prices: a single $0.02 contract fill rounded up to $0.01 in fees, a 50% effective rate. Kalshi revised its maker fee formula in July 2025 to scale with probability rather than use a flat per-contract charge.

See [[kalshi-market-maker-program]] and [[platform-comparison-kalshi-polymarket]] for depth on the Kalshi maker fee structure.

### Other Platforms

- **Robinhood:** $0.02 flat per contract ($0.01 commission + $0.01 exchange fee). Predictable but scales poorly at size—a $10,000 trade at 0.76 costs $256, versus $10 on Polymarket US.
- **FanDuel Predicts:** 2% of potential payout at checkout, applied regardless of outcome. Economically identical to a 2% taker fee but structured differently.
- **DraftKings Predictions:** $0.01 per contract plus exchange fee. Same dollar outcome as Robinhood at most price levels.
- **ForecastEx:** $0.01/contract built into the spread; Yes + No always sum to $1.01.
- **PredictIt:** 10% of gross profits on each winning trade plus 5% withdrawal fee. On a $100 coin-flip, total fees reach $20.68—the highest effective drag among regulated US platforms.

### Sportsbooks for Context

DraftKings and FanDuel embed a 4.5–5% hold into all standard two-way markets. This is implicit: the sum of implied probabilities from both sides of a market exceeds 1 by 4–5 percentage points. In a May 2026 test, prediction markets priced 0.3–1.4 percentage points tighter than sportsbooks on events covered by both. Annualized: $50,000/year at 4.5% sportsbook hold = ~$2,250 theoretical vig drag; same volume on Kalshi at a 1–2% fee blend = ~$500–$1,000 (`raw/research/house-edge-and-market-making/05-pm-vs-sportsbooks-vig.md`).

The sportsbook model is house-banked—the operator is the counterparty and has a financial incentive to restrict winning customers. Prediction markets are peer-to-peer; the platform is structurally indifferent to outcomes.

---

## Where the Effective Cost Is Lowest

*(synthesis)*

Ranking venues by all-in cost burden on a taker, from cheapest to most expensive:

1. **Polymarket Global — Geopolitics & World Events:** 0%. The cheapest available venue for politics, economics, and world-events markets.
2. **Polymarket US (all categories):** 0.10% flat taker fee. Lowest-cost regulated US venue at any probability.
3. **Kalshi — S&P 500 / Nasdaq-100:** ~0.875% at p = 0.50 (halved multiplier). The financial markets carve-out makes Kalshi competitive for macro traders.
4. **Kalshi standard:** ~1.75% at p = 0.50. Still below sportsbooks on events available at both.
5. **Robinhood / FanDuel / DraftKings:** $0.02–$0.04 per contract flat; effective rate of ~2–4% for typical position sizes.
6. **Sportsbooks (DraftKings/FanDuel):** 4.5–5% implicit hold, no explicit fee.
7. **PredictIt:** 10% profit + 5% withdrawal. The most expensive regulated retail venue.

At thin margins, venue selection is itself an edge.

---

## The Maker Advantage

Whelan et al. document a large and statistically significant return gap between makers and takers. Average post-fee returns:

- **Takers:** −31.46%
- **Makers:** −9.64%

Both lose money on average because both groups disproportionately hold cheap contracts affected by FLB. But the differential is stark: makers earn ~22 percentage points more than takers on average.

The mechanism is structural: makers post limit orders and accept execution uncertainty in exchange for better prices than takers pay. Takers pay a fee premium on top of an already-unfavorable price. The bid-ask spread effectively extracts from takers and partially compensates makers.

**The most important subset:** Makers who buy contracts priced at ≥50¢ earn **+2.6% average return** (statistically significant). This is the only price range where a Kalshi participant earns a positive expected return in the Whelan et al. data. This edge exists because high-price contracts are where the FLB works in the maker's favor: the event actually happens slightly more often than the taker's price implies.

**Caution on that +2.6%:** The standard deviation of returns on maker contracts priced ≥50¢ is 33%. Individual contract returns are highly variable. The positive expected return is real but requires a large sample of bets to reliably convert to profits. Whelan et al. note that rational investors facing proper risk aversion (as in Pratt-Zeckhauser) might rationally decline the strategy on a per-bet basis even if expected value is positive.

**Dataset caveat:** The Whelan data run through April 2025, before Kalshi introduced maker fees. Under the current regime (post-April 2025), makers pay up to 0.44% per contract. This erodes the +2.6% maker advantage on ≥50¢ contracts, though the magnitude of erosion depends on the specific contracts traded. Post-April 2025 maker economics on Kalshi require updated empirical analysis not yet available. See [[market-maker-handbook-prediction-markets]] for tactical detail on Kalshi market making under current fee conditions.

**FLB category signal for makers:** Crypto (ψ = 0.058) has the strongest FLB. A maker strategy targeting high-probability crypto contracts on Kalshi faces the most favorable theoretical setup but also the smallest and most volatile contract universe. Politics and Entertainment (ψ ≈ 0.020–0.022) have the weakest FLB, limiting the structural advantage for high-price makers in those categories.

---

## Strategic Implications

*(synthesis)*

**Venue selection is a first-order decision.** The spread between Polymarket Geopolitics (0%) and PredictIt (10%+) is more than 100× in fee rate. Even among competitive venues, Polymarket US at 0.10% versus Kalshi standard at ~1.75% at the midpoint represents a 17× difference. At moderate trading volume, fee drag dominates returns for any strategy without a large edge.

**Key implications for a systematic taker:**

- Use Polymarket for any Geopolitics/World Events market where prices are equivalent to Kalshi. The fee difference is decisive over any volume.
- On events available at both Kalshi and sportsbooks, prediction markets typically price 0.3–1.4 points tighter AND charge less total cost. Default to prediction markets when liquidity permits.
- Avoid cheap contracts (<10¢) as a taker. The Whelan data show average taker losses exceeding 60% in the 1–10¢ range, a combination of FLB and fees. The fee formula charges less in absolute terms at the extremes, but the behavioral disadvantage more than compensates.
- Kalshi S&P 500/Nasdaq-100 markets at the halved fee multiplier are the best-value Kalshi venue for macro traders.

**Key implications for a systematic maker:**

- The ≥50¢ maker advantage (+2.6% average return pre-April 2025) is the only documented positive-EV regime in the Whelan dataset. But it exists under a fee structure that no longer applies. Monitor whether new empirical work updates this estimate for the post-April 2025 maker-fee regime.
- The FLB is weakening over time (ψ: 0.048 in 2024 → 0.021 in 2025). A maker strategy premised on persistent FLB capture is competing against a shrinking inefficiency. The Whelan authors explicitly flag that publication of this finding may accelerate the decay.
- Maker advantages on Polymarket (zero maker fees, rebates funded by taker fees) are structurally cleaner than on Kalshi in the current fee regime. See [[polymarket-microstructure]] for order flow dynamics.

---

## Sources

- `raw/research/house-edge-and-market-making/10-kalshi-economics-whelan-2026.md` — Whelan, Bürgi & Deng (2026), "Makers and Takers: The Economics of the Kalshi Prediction Market." University College Dublin, January 2026. Dataset: 46,282 Kalshi contracts, 2021–April 2025.
- `raw/research/house-edge-and-market-making/01-kalshi-economics-voxeu-2026.md` — VoxEU summary of Whelan et al.
- `raw/research/house-edge-and-market-making/06-polymarket-trading-fees-v2.md` — Polymarket Help Center, "Trading Fees," captured June 2026.
- `raw/research/house-edge-and-market-making/07-defirate-pm-fees-comparison.md` — DeFiRate, "Prediction Market Fees: Kalshi, Polymarket, Robinhood & Coinbase," February 2026.
- `raw/research/house-edge-and-market-making/05-pm-vs-sportsbooks-vig.md` — Tech-insider, "Prediction Markets vs Sportsbooks: 4.5% Vig Gap," May 2026.
- `raw/research/house-edge-and-market-making/02-kalshi-fees-help.md` — Kalshi Help Center "Fees" page, captured June 2026. Confirms post-April 2025 maker fee mechanics: charged on execution only, not on cancellation.

## Related

- [[kalshi-market-maker-program]] — LP program structure (MM Agreement + LIP) and structural maker advantage
- [[market-maker-handbook-prediction-markets]] — A-S quoting framework adapted for prediction markets
- [[polymarket-lp-incentives]] — Polymarket maker rebates and LP reward structure
- [[polymarket-microstructure]] — order flow dynamics, maker-taker split, VPIN on Polymarket
- [[platform-comparison-kalshi-polymarket]] — per-venue fee comparison and structural differences
