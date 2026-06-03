# Kalshi Market Maker Program

Kalshi runs two distinct tracks for liquidity providers: a formal Market Maker Agreement (professional, requires approval, carries 98%-per-hour quoting obligations across 80+ product codes) and the Liquidity Incentive Program (open to most US members, no formal agreement required, proximity-weighted reward pool). The two programs are mutually exclusive — holding a Market Maker Agreement disqualifies you from the LIP.

## Two Tracks: MM Agreement vs LIP

| Dimension | Market Maker Agreement | Liquidity Incentive Program (LIP) |
|---|---|---|
| **Eligibility** | All members who execute the Form Agreement; subject to Kalshi review of financial resources, trading experience, and business reputation | Most regular US members; excludes affiliates, MM agreement holders, IBs/FCMs and their customers, international users |
| **Obligation level** | 98% quoting availability per 1-hour increment; continuous two-sided markets; maximum spread and minimum size per Schedule II | No minimum obligation; scoring is purely proportional to your resting order contribution |
| **Reward type** | Reduced fees + adjusted position limits (exact amounts in Schedule II, not publicly disclosed) | Cash: pro-rata share of $10–$1,000/day per eligible market Time Period |
| **Capital requirement** | 10× the largest elected Minimum Size Within Spread (prima facie evidence of sufficient capital) | None specified beyond standard membership |
| **Application process** | Thorough review; execute Form Market Maker Agreement; no public self-signup portal documented | No application; all eligible members participate automatically by placing resting orders |
| **Program dates** | May 3, 2025 – May 3, 2027 | September 15, 2025 – September 1, 2026 |
| **Mutual exclusion** | Disqualifies you from LIP | Disqualifies you from holding an MM Agreement |

---

## Track 1: Formal Market Maker Agreement

### Eligibility and Application

Market maker status is granted following a thorough review of financial resources, trading experience, and business reputation; approval is conditional on the ability to meet ongoing liquidity obligations. Per the CFTC filing (April 21, 2025), prospective market makers must:

- Execute a Form Market Maker Agreement and comply with Kalshi Rule 4.1 (Eligibility to be Designated as a Market Maker) and Rule 4.2 (Designation as a Market Maker)
- Enable monitoring for API usage and possess the ability to consistently monitor API usage throughout elected availability periods
- Understand and implement rate limiting and throttling mechanisms, and have the ability to self-limit load
- Maintain sufficient capital on the exchange: **ten (10) times the largest elected Minimum Size Within Spread** is stated as prima facie evidence of sufficient capital

No public self-signup portal is documented. The process is a bilateral negotiation with Kalshi resulting in a signed agreement.

### Obligations

In each designated product during specified hours, market makers must:

- Quote continuous two-sided markets
- Maintain maximum bid/offer spreads
- Maintain minimum quote sizes

The specific conditions per product are set in Schedule II (Liquidity Conditions), which is executed individually and not publicly disclosed. The help center lists availability as **98% of each 1-hour increment** for all covered products.

**Covered products** (as of the help center capture, June 2026; Kalshi reserves the right to update this list at any time):

| Category | Product codes |
|---|---|
| Indices | KXINX, KXINXU, KXINXY, KXNASDAQ100, KXNASDAQ100U, KXNASDAQ100Y, KXINXMAXY, KXINXMINY, KXINXPOS |
| Crypto | KXBTC, KXBTCD, KXBTCMAX150, KXETH, KXETHD, KXDOGE, KXDOGED, KXSHIBA, KXSHIBAD |
| NBA | KXNBA, KXNBAEAST, KXNBAWEST, KXNBASERIES, KXNBAGAME, KXNBACOY, KXNBAMVP, KXNBAROY |
| NHL | KXNHL, KXNHLEAST, KXNHLWEST, KXNHLSERIES, KXNHLGAME |
| MLB | KXMLB, KXMLBAL, KXMLBNL |
| Golf / Tennis / Soccer / Other sports | KXPGATOUR, KXFOMENSINGLES, KXFOWOMENSINGLES, KXFOMENSSINGLES, KXFOWOMENSSINGLES, KXUSOMENSSINGLES, KXUSOWOMENSSINGLES, KXWMENSINGLES, KXWWOMENSINGLES, KXHEISMAN, KXINDY500, KXEPLGAME, KXEPLTOP4, KXUCL, KXUCLGAME, KXSERIEA, KXSERIEAGAME, KXBUNDESLIGA, KXBUNDESLIGAGAME, KXLALIGA, KXLALIGAGAME, KXLIGUE1, KXLIGUE1GAME, KXATPMATCH, KXWTAMATCH, KXMENWORLDCUP |
| NFL | KXSB, KXNFLGAME, KXNFLAFCCHAMP, KXNFLNFCCHAMP, KXNFLMVP, KXNFLOPOTY, KXNFLDPOTY, KXNFLOROTY, KXNFLDROTY, KXNFLCPOTY, KXNFLANYTD, KXNFLFIRSTTD, KXNFL2TD |
| College / NASCAR / UFC | KXNCAAMBGAME, KXNASCARRACE, KXUFCFIGHT |
| Economic | KXCPI, KXCPIYOY, KXFED, KXFEDDECISION, KXGDP, KXPAYROLLS, KXRATECUTCOUNT, KXU3 |
| Other | KXIPO, KXLLM1, KXMARMAD, KXAAAGASM |

### Benefits

Qualifying market makers receive reduced fees and certain adjusted position limits. The exact amounts and position limit adjustments are governed by the individual Schedule II and are not publicly disclosed. Any fee reductions or other program benefits are conditional on maintaining sufficient liquidity and orderly markets.

### Program Terms

- **Effective period:** May 3, 2025 – May 3, 2027 (may be extended or terminated by Kalshi)
- **Scope:** All Kalshi markets
- **Intra-firm trading** (direct or indirect) is excluded from any financial incentives
- **Monitoring and revocation:** Kalshi's Chief Regulatory Officer can revoke participant status if participation is found to be abusive or inconsistent with the program's purpose
- **Prior agreements:** Members with an existing market maker agreement can elect covered products under the new Agreement after first opting out of any identical covered product under the prior agreement; new Agreement terms supersede prior terms for that product
- **FCM partners:** Webull Financial LLC, Robinhood Derivatives LLC, Direct Access USA LLC

---

## Track 2: Liquidity Incentive Program (LIP)

### Who Can Participate

The LIP is open to most regular US Kalshi members. Excluded categories (per the CFTC filing, February 2026):

- Kalshi affiliates and employees
- Members who have executed a Market Maker Agreement with Kalshi
- Introducing Brokers, Futures Commission Merchants, and their customers when transacting via the IB or FCM
- International, non-US users (ineligible for rewards)

### How It Works

During a LIP-eligible Time Period, Kalshi takes one snapshot of the order book per second, with the exact snapshot time drawn from a random uniform distribution (changed periodically to ensure unpredictability). The snapshot is excluded if either side of the book lacks qualifying bids sufficient to meet the Target Size — two-sided liquidity is required. This two-sided requirement was added by amendment on February 28, 2026 (CFTC filing, February 2026).

**Scoring algorithm:**

For each snapshot, Kalshi identifies Qualifying Yes Bids and Qualifying No Bids — the set of resting bids from the best price inward until the cumulative size reaches the Target Size. Each qualifying bid is scored:

```
Score(bid) = Discount_Factor ^ (Reference_Price − Price(bid)) × Size(bid)
```

A bid at the reference price (best bid) receives full credit. Bids further away are penalized exponentially by the Discount Factor. Each bid's score is then normalized against all qualifying bids on that side:

```
Normalized_Score(bid) = Score(bid) ÷ Σ Score(b) for all b in qualifying bids
```

A user's Snapshot LP Score is the sum of their Normalized Qualifying Yes Scores and Normalized Qualifying No Scores across all their resting orders in that snapshot.

After the Time Period ends, each user's Snapshot LP Scores are summed and divided by the total of all participants' scores to produce a Time Period LP Score. Payment:

```
Payment ≈ Time_Period_LP_Score × Time_Period_Reward
```

Minimum payout: $1.00, rounded down to the nearest cent. Amounts below $1.00 are not paid.

**Schedule parameters (per Time Period):**

| Parameter | Constraint |
|---|---|
| Time Period | ≤ 31 days |
| Target Size | 100–20,000 contracts |
| Discount Factor | ≤ 1.00 |
| Time Period Reward | $10–$1,000 per calendar day |

**Example** (from Kalshi help center): Maintain 500 contracts at best bid for 50% of snapshots. If you represent 20% of qualifying liquidity in a $100/day reward period, you earn $20 for that day.

### Program Dates

- **Start:** September 15, 2025
- **End:** September 1, 2026 (or earlier if Kalshi amends or terminates)
- Kalshi can end or modify the program at any time

### Expected Yield

The LIP reward pool ranges from $10 to $1,000 per calendar day per eligible market. The actual yield to an individual participant depends on their share of total qualifying liquidity across all participating members. No per-participant yield estimate is available from the captured sources.

For comparison, see [[polymarket-lp-incentives]] for an analysis of the comparable Polymarket LP program, where rough estimates on the Starmer cluster were in the range of $200–$400/day for active participants. Kalshi's LIP pool sizes are in a similar order of magnitude, but actual per-participant yields are not computed in any captured source and should not be extrapolated directly.

---

## The Structural Maker Advantage (Whelan, Bürgi & Deng 2026)

Beyond the two formal programs, there is academic evidence that the maker role itself carries a structural return advantage on Kalshi, independent of any LP incentive.

Whelan, Bürgi and Deng (2026) — "Makers and Takers: The Economics of the Kalshi Prediction Market" — analyzed transaction-level data on 46,282 Kalshi contracts from 2021 through April 2025. Key findings:

**Overall return differential:**

| Role | Average post-fee return |
|---|---|
| Makers | −9.64% |
| Takers | −31.46% |

Both groups lose on average, but Makers lose far less. The difference is statistically significant at extremely high confidence levels.

**Maker returns by price range:**

- Makers on contracts priced **≥ 50¢**: **+2.6% average return** (positive)
- Makers on contracts priced **< 10¢**: statistically significant negative returns (large losses, though less severe than for Takers in the same range)

**Maker share by price range** (from Table 10 of the paper):

| Price range | Maker share of total observations |
|---|---|
| 1¢–10¢ | 43.5% |
| 11¢–20¢ | 46.7% |
| 21¢–30¢ | 48.9% |
| 31¢–40¢ | 47.8% |
| 41¢–50¢ | 49.5% |
| 50¢–59¢ | 50.4% |
| 60¢–69¢ | 52.2% |
| 70¢–79¢ | 51.1% |
| 80¢–89¢ | 53.3% |
| 90¢–99¢ | 56.5% |

Makers disproportionately occupy the high-price end, where returns are favorable. Takers are disproportionately concentrated in cheap contracts, where losses are severe.

**Mechanism — Favorite–Longshot Bias (FLB):** Kalshi prices exhibit a systematic FLB: low-priced contracts win less often than their prices imply; high-priced contracts win more often. Makers, by posting resting limit orders, self-select into better prices than Takers and are not forced to execute at the current ask. The model in the paper (adapted from Whelan 2025) shows that agents with moderately strong beliefs become Makers to obtain a better price, while those with the most extreme beliefs take immediately. This sorting mechanism, combined with a modest bias toward overestimating small probabilities (β ≈ 0.09 in the calibration), reproduces the observed maker-taker return gap.

**Critical caveat — fee regime:** During the Whelan et al. dataset period (2021–April 2025), **Makers paid zero fees**. Kalshi began charging Makers fees starting in April 2025. The +2.6% average return for Makers on ≥50¢ contracts was earned under the zero-fee maker regime. Under the current fee structure, the maker advantage is directionally preserved (the FLB mechanism is unaffected by fees) but the absolute return figures will be lower. The magnitude of the reduction depends on the specific fee rates charged to Makers post-April 2025, which are not captured in the source material.

**Risk caveat:** The standard deviation of Maker returns on contracts ≥50¢ is **33%** — large relative to the 2.6% average. This is a probabilistic edge with high variance per trade, not a guaranteed return. A large number of trades is needed to reliably realize the positive expected value; the expected utility argument against this (Samuelson 1963) is also noted by the authors.

---

## Strategic Considerations

*(synthesis)*

**Which track to pursue?**

The MM Agreement is designed for participants with serious quoting infrastructure. The 98%-per-hour availability requirement across 80+ product codes is an institutional obligation — missing it forfeits incentives. The capital requirement (10× minimum size per elected product) and the API monitoring/rate-limiting requirements signal that this track is not intended for retail-scale participants. If you do not have automated quoting infrastructure and the capital to continuously meet spread conditions across dozens of markets simultaneously, the MM Agreement is not the right path.

The LIP is the retail path. Any eligible US member can participate immediately by placing resting limit orders in eligible markets. The scoring mechanism naturally rewards participants who provide tight, consistent liquidity — but there is no penalty for doing less. The per-day pool ($10–$1,000) is modest relative to major financial markets, so returns are commensurate with the liquidity depth you can provide relative to other participants.

**The Whelan finding as context for maker strategy:**

The structural maker advantage documented by Whelan et al. applies regardless of which formal program you are in (or whether you are in any program at all). Any participant posting limit orders at favorable prices in the ≥50¢ range is operating on the beneficial side of the FLB. The LIP can be understood as Kalshi making this maker-side participation economically attractive to a broader pool of participants by adding a cash subsidy on top of the underlying trading edge. The two sources of maker return — the FLB edge and the LIP subsidy — are additive but independent.

**The capital cost of liquidity provision:**

Both tracks require capital to be held on the Kalshi exchange. Posted limit orders are capital-at-risk: they earn the maker-side return only when matched and resolved. During the period they rest in the book, that capital is committed. Participants should account for the opportunity cost and the exchange-custody risk of having funds on Kalshi.

**Contrast with Polymarket:**

Polymarket's LP program is accessible without any formal agreement or approval process — builder tooling is publicly accessible (see [[polymarket-lp-incentives]]). Kalshi's two-tier structure is more formal at the top end, with the LIP serving as the open-access equivalent. See [[platform-comparison-kalshi-polymarket]] for a broader comparison of the two platforms.

For the Avellaneda-Stoikov quoting framework applicable to prediction market making, see [[market-maker-handbook-prediction-markets]].

For the underlying house edge analysis that motivates why certain Kalshi price ranges are more favorable for makers, see [[prediction-market-house-edge]].

---

## Open Gaps

- **Schedule II terms not public.** The specific spread requirements, minimum sizes, and fee rebate amounts for each covered product under the MM Agreement are set in individual Schedule II attachments executed between Kalshi and each market maker. These are not published.
- **Exact fee reduction amounts unknown.** The help center states "reduced fees and certain adjusted position limits" but provides no figures. The CFTC filing references "predetermined incentives" but defers to Schedule II.
- **Application process not documented.** No public portal or formal application form has been captured. The process appears to be initiated by direct contact with Kalshi, but this is not confirmed in any source.
- **Individual vs. institutional eligibility unstated.** Whether the MM Agreement is available to individual retail traders or only to institutional entities is not stated in any captured source. The review criteria (financial resources, trading experience, business reputation) and the API infrastructure requirements suggest institutional participants, but this is not explicit.
- **Post-April 2025 maker fee rates not captured.** Whelan et al. note that Kalshi began charging Makers fees in April 2025. The current maker fee schedule is not in any captured source, making it impossible to restate the Whelan return figures on a current-fee basis.
- **LIP per-participant yield not computed.** No source provides an estimate of what an individual participant actually earns from the LIP, since this depends on the total competing liquidity across all participants.

---

## Sources

- `raw/research/house-edge-and-market-making/09-kalshi-mm-program-cftc-2025.md` — CFTC filing, Kalshi Market Maker Program Terms (April 21, 2025)
- `raw/research/house-edge-and-market-making/03-kalshi-mm-program-help.md` — Kalshi Help Center: Market Maker Program (captured June 2026)
- `raw/research/house-edge-and-market-making/04-kalshi-liq-incentive-help.md` — Kalshi Help Center: Liquidity Incentive Program (captured June 2026)
- `raw/research/house-edge-and-market-making/08-kalshi-liq-incentive-cftc-2026.md` — CFTC filing, Amendment to August 2025 Liquidity Incentive Program (February 11, 2026)
- `raw/research/house-edge-and-market-making/10-kalshi-economics-whelan-2026.md` — Whelan, Bürgi & Deng (2026), "Makers and Takers: The Economics of the Kalshi Prediction Market," University College Dublin (January 2026)
- `raw/research/house-edge-and-market-making/01-kalshi-economics-voxeu-2026.md` — VoxEU summary of Whelan et al. (2026)

## Related

- [[prediction-market-house-edge]] — full fee comparison + Whelan FLB findings across all venues
- [[market-maker-handbook-prediction-markets]] — A-S quoting framework, inventory caps, toxicity guards
- [[polymarket-lp-incentives]] — comparable LP program on Polymarket (three-track, no formal agreement)
- [[platform-comparison-kalshi-polymarket]] — structural/fee/volume comparison between the two platforms
- [[feasibility/lp-yield-farming]] — feasibility assessment of yield-farming as a strategy on Polymarket
