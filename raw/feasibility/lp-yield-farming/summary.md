# Feasibility Assessment: LP Yield Farming as Meta-Strategy

**Type:** Meta-strategy (yield extraction via simultaneous LP incentive programs, no required directional view)
**Date:** 2026-05-16
**Sources:** [[polymarket-lp-incentives]], [[market-maker-handbook-prediction-markets]], [[polymarket-strategy-matrix]], [[polymarket-microstructure]], Gamma API live pull 2026-05-16

---

## 1. Data Sources and Programmatic Observability

### Reward program parameters (per-market)

The Gamma API exposes the load-bearing LP parameters directly on every market object. No separate endpoint needed:

| Field | Meaning | Live example (Starmer June 2026) |
|---|---|---|
| `clobRewards[].rewardsDailyRate` | Platform Liquidity Rewards — USDC/day this market receives | 400 USDC/day |
| `rewardsMaxSpread` | Max-spread gate in cents — orders beyond earn zero | 3.5c |
| `rewardsMinSize` | Minimum order size in shares to qualify | 200 shares |
| `feeSchedule.rate` | Taker fee rate (determines Maker Rebate pool size) | 0.04 (politics) |
| `feeSchedule.rebateRate` | Fraction of taker fees returned as Maker Rebates | 0.25 |
| `feesEnabled` | Whether Maker Rebates are active | True |
| `holdingRewardsEnabled` | Separate holding-rewards layer (distinct from CLOB LP rewards) | False (most) |

**API endpoint:** `GET https://gamma-api.polymarket.com/events?active=true&closed=false&limit=N`

Full reward stack is queryable in one call. Filter `clobRewards[].rewardsDailyRate > 0 AND rewardsMaxSpread > 0` for active Liquidity Rewards markets. `rewardsMaxSpread` is the per-market max-spread gate that determines eligibility — orders outside the band earn zero from LR and SR regardless of size.

### Sponsor Market Rewards — `polymarket.com/rewards`

The rewards landing page is JavaScript-rendered. However, Sponsor Reward data also surfaces in the Gamma API `clobRewards` array — third-party sponsors appear as additional `clobRewards` entries alongside platform rewards. The `rewardsDailyRate` of a sponsored market reflects combined platform + sponsor allocation. This makes the Gamma API the single programmatic source for all three program parameters.

**Monitoring approach:**
- Poll `gamma-api.polymarket.com/events` every 15-60 min. Changes in `rewardsDailyRate` signal new sponsor deposits or platform program changes.
- Track `rewardsMaxSpread` per market — this is THE eligibility gate.
- `clobRewards[].endDate` exposes reward expiry dates. Most platform rewards show `endDate: 2500-12-31` (open-ended). Sponsor rewards with finite `endDate` are actionable signals for the sponsor-end depth pull.
- On-chain rewards contract: provides ground truth on deposits, cancellations, daily distributions — useful for reconciliation, not real-time quoting.

### Live observations (2026-05-16 Gamma API pull)

Top markets by Liquidity Rewards daily rate active today:

| Market | rewardsDailyRate | rewardsMaxSpread | rewardsMinSize | vol24h | deployed liq |
|---|---|---|---|---|---|
| Starmer out by Jun 30 2026 | **400 USDC/day** | 3.5c | 200 shares | $122,532 | $117,438 |
| Starmer out by May 31 2026 | **300 USDC/day** | 4.5c | 200 shares | $125,287 | $98,598 |
| Starmer out by Dec 31 2026 | **200 USDC/day** | 3.5c | 200 shares | $30,304 | $129,128 |
| FIFA World Cup — Spain | 0.001 USDC/day | 0 (no gate) | 0 | $69,841 | $616,246 |
| NBA Finals — OKC Thunder | 0.001 USDC/day | 0 (no gate) | 0 | $84,966 | $190,955 |

**Observation:** FIFA/NBA sub-markets show near-zero platform rewards with `rewardsMaxSpread=0` — effectively in a reward holding pattern. The Starmer cluster carries 300-400 USDC/day per leg with explicit spread gates, consistent with active Liquidity Rewards targeting. FIFA ($234M event liquidity) is capacity-saturated: 60 sub-markets, most `clobRewards=[]`, spread = 0.001 (1 tick), institutional domination.

Gamma API also reveals a fourth yield layer not yet in the wiki: `holdingRewardsEnabled: True` appears on select FIFA sub-markets but not NBA/NHL/Starmer. Mechanics unknown — an open research gap.

---

## 2. Modeling: Optimal Quoting Under the 3-Program Stack

### The combined yield objective

Per market m, daily yield:

```
LP_yield(m) = LR_share(m) + MR_share(m) + SR_share(m)
```

Per [[polymarket-lp-incentives]]:
- LR_share: proximity-weighted share of `rewardsDailyRate` pool
- MR_share = (fee_eq_yours / fee_eq_total) x rebate_pool; where `fee_eq = C x feeRate x p x (1-p)`
- SR_share: same proximity weighting as LR, applied to sponsor pool

### The max-spread gate constraint

`rewardsMaxSpread` defines an eligibility band around mid. The key identity:

```
eligible_quote iff |p_quote - p_mid| <= rewardsMaxSpread / 100
```

For Starmer June 30 (rewardsMaxSpread = 3.5c, mid = 0.265):
- Eligible bid: [0.23, 0.265]; Eligible ask: [0.265, 0.30]
- Competitive proximity-weighting favors placement at the inside spread, not the gate boundary.

### A-S quoting adapted for LP yield farming

The [[market-maker-handbook-prediction-markets]] A-S framework (Eqs. 8-9):

```
Reservation:   r_x = x_t - q_t * gamma * sigma_b^2 * (T-t)        (8)
Half-spread:   2*delta_x = gamma*sigma_b^2*(T-t) + (2/k)*log(1+gamma/k) (9)
```

Under LP yield farming, proximity-weighted reward share adds a tightening pull to the spread objective. The reward share for an order at price p relative to mid p_m decays with distance; if approximately linear within the gate:

```
reward_share ∝ (rewardsMaxSpread - |p - p_m|) / rewardsMaxSpread
```

Tighter quotes → larger proximity weight → larger LR/SR share. But tighter quotes increase fill probability and adverse-selection exposure (Glosten-Harris phi from [[polymarket-microstructure]] Sec. 6).

**The practical LP yield quoting rule:**

```
target_spread = max(tick_size, min(rewardsMaxSpread, A-S_optimal_spread))
```

The reward incentive pulls spread toward tick-size; inventory risk and adverse selection push it wider; `rewardsMaxSpread` is the hard outer bound on eligibility.

**Inventory skew is load-bearing.** A pure LP farmer who fails to manage inventory accumulates directional exposure on whichever side gets hit. Apply:

```
Inv. cap: |q_t| <= q_max ∝ 1 / max{S'(x_t), epsilon}
```

At the rails (p near 0 or 1), inventory cap tightens exactly when Maker Rebates also shrink (the `p(1-p)` term in `fee_eq` goes to zero). The three programs together naturally incentivize quoting near center (p in [0.35, 0.65]) — this is not accidental; it is structural alignment between inventory risk tolerance and reward rate.

### Yield estimation (Starmer June 30 example)

- LR pool: $400/day, total deployed liq: $117K. At 10% pool share (~$11.7K deployed): $40/day = 0.34% daily = ~124% annualized raw LR yield.
- MR pool: vol24h = $122K x 0.04 taker rate x 0.25 rebate rate = $1,220/day total MR pool. At 10% fill share: $122/day additional.
- Combined (LR + MR, 10% share): ~$162/day on $11.7K deployed = 505% annualized raw (before adverse selection and operational costs).

These raw yields are pre-adverse-selection and pre-operational-cost. They do not survive uninformed quoting at scale.

---

## 3. Secondary Structure: Sponsor-End Depth Pull

No classical structural arbitrage — this is yield extraction. One defined secondary opportunity on sponsor lifecycle:

**The sponsor-end depth pull:**
1. During sponsorship: LPs flood, spreads compress to tick-size, depth concentrates inside `rewardsMaxSpread`.
2. When sponsor rewards expire: exogenous LP withdrawal, spreads re-widen, remaining liquidity thinner and potentially stale.

**Tracking:** `clobRewards[].endDate` in Gamma API. Platform rewards (`endDate: 2500-12-31`) are permanent. Sponsor rewards with finite `endDate` within 1-7 days are the actionable signals.

**Exploitation windows:**
- As LP farmer: enter before sponsor pools launch (before depth concentrates), earn larger share from thin competition, reduce as HFT capital arrives.
- As directional trader: use sponsor-compressed spreads for low-cost directional execution; plan exit before `endDate`.

---

## 4. Microstructure Regime: You Are the Microstructure

LP yield farming does not exploit the microstructure — it constitutes it.

**SF2 (uniform-grid depth profile, depthL1/depthL10 = 0.137) is caused by LP farmers.** The proximity-weighted Liquidity Rewards program directly produces the clustering [[polymarket-microstructure]] documents. Entering this strategy means replicating the behavior that created SF2 — which also means you are priced into the equilibrium, not exploiting a departure from it.

**SF4 (HHI = 0.031, ~32 effective makers on top markets) means yield is contested.** On thin markets (p90 HHI = 0.119, ~8 effective makers), pools are less contested — this is where retail LP edge concentrates.

**Adverse selection is not the primary risk.** Glosten-Harris decomposition in [[polymarket-microstructure]] Sec. 6: median phi ≈ 0 on top-100 stratum. Consistent with the structural argument: LP farmers are mostly trading against other LP farmers adjusting positions, not against informed directional flow. However:
- phi ≈ 0 is a cross-sectional average; individual fill events near scheduled announcements can be informative.
- VPIN-style toxicity guards remain mandatory (A-S Sec. 4.5). The `phi ≈ 0` average does not protect against tail adversarial events.

**Inventory accumulation is the primary P&L risk**, not adverse selection — consistent with `c ≈ 0, phi ≈ 0`. An LP quoting both sides symmetrically in a market that moves 20c carries a large directional position. Critically: the Maker Rebate fills that generate MR income are exactly the fills that accumulate inventory.

**SF8 (depth decay with resolution approach):** `beta ≈ 0.305` (volume-controlled), i.e., ~6% less depth per 10x reduction in seconds-to-close. For LP yield farming: reduce quote size and `q_max` as resolution approaches; the reward/risk ratio deteriorates as inventory risk increases and depth thins.

---

## 5. Competition and Saturation

Sophisticated MMs (Jump, Wintermute-class) are almost certainly active in top-100 markets. Evidence:
- SF4 median HHI = 0.031 across top-100.
- FIFA sub-markets: spread = 0.001 (1 tick), `rewardsMaxSpread = 0` or 2.5c — consistent with HFT-level saturation.
- NBA OKC: spread = 0.01 (1 tick for this tick-size class).

**Retail LP edge concentrates in three places:**

1. **Esports sponsor pools:** ~$3,412 USDC per Valorant BO3 series ([[polymarket-lp-incentives]] 2026-05-16); HHI likely at p90+ range (few effective makers). Institutionals focus on top-100 by volume; esports is structurally under-covered.

2. **Mid-cap political date-ladders with active LR:** Starmer cluster — $300-400 USDC/day with $98-129K deployed. Large reward/capital ratio; not yet saturated to 1-tick spread across all legs.

3. **Cross-program optimization:** Running LR + MR + SR simultaneously, with explicit MR fill-rate awareness, beats single-program LPs at equal capital. Most retail LPs optimize for proximity (LR) only, ignoring MR fill-rate dimension.

**Saturation signal:** spread = tick-size AND `rewardsMaxSpread` loose AND multiple active maker addresses. When these three co-occur, yield per dollar of capital has equilibrated to near-zero marginal return on additional capital. This is the exit signal.

---

## 6. Capital Intensity and Operational Profile

| Dimension | LP Yield Farming | Predictive-Edge |
|---|---|---|
| Capital requirement | High — rewards scale with deployed capital | Low — edge is in position sizing |
| Holding period | Continuous (maintain quotes) | Discrete (enter/hold/exit) |
| P&L driver | Daily reward accrual | Correct directional resolution |
| Primary risk | Inventory accumulation | Resolution miss |
| Operational overhead | Quote management, fill monitoring, rebalancing | Model updates, position tracking |
| Compounding | Reward income reinvested | Kelly growth on correct calls |

**Capital floor estimates:**

- Esports Valorant BO3 ($3,412/series, ~2-day window): to earn 10% pool share requires roughly $10-50K deployed within `rewardsMinSize` and `rewardsMaxSpread` constraints. At 10%: ~$341/series x frequency.
- Starmer June 30 ($400/day, $117K deployed): 10% pool share requires ~$11.7K; generates ~$40/day LR + ~$122/day MR pool (at 10% fill share: ~$12/day MR). Total: ~$52/day on $11.7K.
- **Minimum viable capital for a three-program stack on a mid-sized market: ~$25K-100K per market** to hold a material reward share while absorbing fill inventory without breaching `q_max`.

---

## 7. Targeting Logic: Market Selection

**Queryable filter using Gamma API fields:**

```
rewardsDailyRate > threshold          # active reward pool
AND rewardsMaxSpread > 0              # explicit spread gate (LR program live)
AND liquidityNum < saturation_cap     # under-LP'd
AND volume24hr > volume_floor         # sufficient flow for MR income
AND feesEnabled = True                # MR program active
```

**Today's candidates (2026-05-16):**

The Starmer date-ladder cluster is the strongest current signal: all three legs have `rewardsDailyRate = 200-400 USDC/day`, `rewardsMaxSpread = 3.5-4.5c`, deployed liquidity $98-129K/leg (not saturated), and volume $30-125K/day. Fee type: `politics_fees`, rate 4%, rebate 25%.

Second tier: active Esports sponsor markets (require separate query to `polymarket.com/rewards` or finite-`endDate` scan of Gamma API).

Avoid: FIFA sub-markets (institutional saturation), Geopolitics (fee-free, zero MR pool).

---

## 8. Risk Register

| Risk | Mechanism | Mitigation |
|---|---|---|
| **Inventory accumulation** | One-sided fills → directional exposure; adverse resolution = full loss | A-S inventory skew (Eq. 8); `q_max` cap; cancel-replace if mid drifts >2 ticks |
| **Adverse selection** | Informed trader hits quote before public information | VPIN-style imbalance trigger; pause before scheduled announcements; widen as resolution approaches (SF8) |
| **Reward program change** | Platform reduces `rewardsDailyRate` or terminates program | Monitor field daily; treat reward-funded position as provisional |
| **Spread gate tightening** | Platform narrows `rewardsMaxSpread`, invalidating existing quotes | Monitor field; any reduction requires immediate requote inside new band |
| **Sponsor cancellation** | Third-party cancels mid-cycle; today's allocation irrevocable | Irrevocability rule already limits this; factor potential early termination into IRR |
| **Fee-category zero** | Geopolitics markets fee-free → zero MR income | Exclude from MR calculation; still eligible for LR/SR |
| **Both-sides rule near resolution** | Markets below $0.10 mid require both-side quotes | Exit or maintain both-side quotes; inventory cap tightens at same threshold |
| **Oracle delay spread blowout** | Post-resolution spreads spike to ~7,500 bps ([[polymarket-microstructure]] NBA data) | Cancel all quotes 15-30 min before expected resolution |
| **Competition saturation** | HHI drops → reward share per dollar drops below capital cost | Re-allocate to lower-HHI markets; use spread=tick as saturation signal |
| **Holding rewards mechanics unknown** | `holdingRewardsEnabled: True` on select markets; yields unknown | Do not model until mechanics are researched; treat as upside optionality |

---

## 9. Implementation Sketch

**Phase 1 — Monitoring (no capital at risk):**
- Gamma API poller: fetch all events every 15 min, filter `rewardsDailyRate > 1 AND rewardsMaxSpread > 0`, rank by `rewardsDailyRate / liquidityNum`.
- Track `rewardsMaxSpread` changes per market as policy-shift signals.
- Build `clobRewards[].endDate` monitor for sponsor expiry alerts within 7 days.
- For sponsor discovery: cross-validate Gamma API against `polymarket.com/rewards` (Playwright-rendered) — differences reveal sponsor rewards not yet surfaced in `clobRewards`.

**Phase 2 — Single-market paper deployment:**
- Target: one Starmer date-leg.
- Quote via A-S with inventory skew; use `rewardsMaxSpread` as outer bound.
- Toxicity guards: cancel on VPIN threshold; pause 24h before key political events.
- P&L attribution: LR accrual / MR accrual / SR accrual / adverse selection cost / inventory carry.

**Phase 3 — Multi-market stack:**
- Scale to 3-10 markets; aggregate reward income vs. aggregate capital.
- Implement cross-market inventory netting where correlated events allow beta-hedge ([[market-maker-handbook-prediction-markets]] Sec. 4.4).

---

## 10. Verdict and Open Questions

### One-line verdict

**Structurally sound yield strategy at the right scale; retail edge is real but narrow (Esports sponsor pools + mid-cap political date-ladders) and requires inventory-aware quoting discipline — uninformed quote-posting will be eaten by adverse selection on fill events.**

### Extended verdict

The three-program stack is mathematically stackable. The Gamma API exposes all load-bearing parameters. Raw yields on under-LP'd markets are economically significant (Starmer: ~124% annualized LR yield at 10% pool share). The `phi ≈ 0` Glosten-Harris finding from [[polymarket-microstructure]] confirms adverse selection does not systematically erode LP yield on liquid prediction markets — inventory risk dominates.

Hard constraints: capital-intensive; A-S quoting with toxicity guards is required, not optional; top-100 markets are saturated; reward rates can change without notice.

### Open questions

1. **Maker HHI on targeted markets** — Gamma API does not expose per-market maker concentration. Need on-chain `OrderFilled` maker-address analysis to estimate competition in Starmer/Esports clusters before committing capital.
2. **Fill rate empirics** — What fraction of quotes inside `rewardsMaxSpread` actually fill in mid-cap political markets? MR income is zero without fills. Requires on-chain `OrderFilled` backtest.
3. **Reward program stability** — The `endDate: 2500-12-31` suggests open-ended commitment, but the $1M CLOB v2 program (launched 2026-04-28) has an implicit budget constraint. Track total daily payout vs. announced program size.
4. **Holding rewards mechanics** — `holdingRewardsEnabled: True` on select FIFA sub-markets is a fourth yield layer not yet in the wiki. Mechanics unknown; treat as upside optionality until researched.
5. **Sponsor vs. platform reward decomposition** — Gamma API `clobRewards` appears to roll platform and sponsor rewards together in `rewardsDailyRate`. Distinguishing the two programmatically (to track sponsor `endDate` vs. platform open-ended programs) may require cross-referencing `polymarket.com/rewards` or on-chain sponsor deposit events.

---

## Source

- [[polymarket-lp-incentives]] — three-program mechanics, formulas, live Esports sponsor data 2026-05-16
- [[market-maker-handbook-prediction-markets]] — A-S quoting framework, inventory cap, toxicity guards
- [[polymarket-strategy-matrix]] — sponsor-end depth pull, edge taxonomy
- [[polymarket-microstructure]] — SF2/SF4 depth profile, Glosten-Harris phi=0, SF8 depth decay
- Gamma API live pull 2026-05-16: `https://gamma-api.polymarket.com/events?active=true&closed=false&limit=30`

## Related

- [[polymarket-lp-incentives]]
- [[market-maker-handbook-prediction-markets]]
- [[polymarket-microstructure]]
- [[polymarket-strategy-matrix]]
- [[polymarket-architecture]]
- [[arbitrage-taxonomy]]
- [[polymarket-liquidity-evolution]]
