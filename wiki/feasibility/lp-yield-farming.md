# Feasibility — LP Yield Farming as Meta-Strategy

Three-program stack (Liquidity Rewards + Maker Rebates + Sponsor Market Rewards) per [[polymarket-lp-incentives]]. **Structurally sound at the right scale.** Retail edge is real but narrow — Esports sponsor pools + mid-cap political date-ladders — and requires inventory-aware quoting discipline. Uninformed quote-posting will be eaten by adverse selection on fill events. Live Gamma API 2026-05-16 confirms all load-bearing parameters surface in `clobRewards[]`.

## Top targets (live 2026-05-16)

| Market | rewardsDailyRate | rewardsMaxSpread | rewardsMinSize | vol_24h | deployed_liq |
|---|---|---|---|---|---|
| Starmer out by Jun 30 2026 | **400 USDC/day** | 3.5¢ | 200 shares | $122.5K | $117.4K |
| Starmer out by May 31 2026 | **300 USDC/day** | 4.5¢ | 200 shares | $125.3K | $98.6K |
| Starmer out by Dec 31 2026 | **200 USDC/day** | 3.5¢ | 200 shares | $30.3K | $129.1K |
| FIFA World Cup — Spain | 0.001 USDC/day | 0 (no gate) | 0 | $69.8K | $616.2K |
| NBA Finals — OKC Thunder | 0.001 USDC/day | 0 (no gate) | 0 | $85.0K | $191.0K |

FIFA ($234M event liq) capacity-saturated; 60 sub-markets, most `clobRewards=[]`, spread = 0.001 (1 tick), institutional domination. **Starmer cluster is the strongest current target.**

**Fourth yield layer discovered**: `holdingRewardsEnabled: True` on select FIFA sub-markets (not NBA/NHL/Starmer). Mechanics unknown — open research gap.

## Gamma API exposes all parameters

All three programs surface in a single endpoint call:

```
GET https://gamma-api.polymarket.com/events?active=true&closed=false&limit=N
```

| Field | Meaning |
|---|---|
| `clobRewards[].rewardsDailyRate` | LR pool USDC/day (sponsor + platform combined) |
| `rewardsMaxSpread` | Max-spread gate in cents — orders beyond earn zero |
| `rewardsMinSize` | Minimum order size in shares to qualify |
| `feeSchedule.rate` | Taker fee rate (drives MR pool size) |
| `feeSchedule.rebateRate` | Fraction of taker fees returned as MR |
| `feesEnabled` | Whether MR is active |
| `holdingRewardsEnabled` | Separate fourth-layer holding-rewards (distinct from LR) |
| `clobRewards[].endDate` | Reward expiry (`2500-12-31` = open-ended platform; finite = sponsor) |

## Modeling spine

### Combined daily yield

```
LP_yield(m) = LR_share(m) + MR_share(m) + SR_share(m)

LR_share : proximity-weighted share of rewardsDailyRate pool
MR_share = (fee_eq_yours / fee_eq_total) × rebate_pool
           fee_eq = C × feeRate × p × (1 − p)
SR_share : same proximity weighting as LR, applied to sponsor pool
```

### Max-spread gate

```
eligible_quote iff |p_quote − p_mid| ≤ rewardsMaxSpread / 100
```

For Starmer June 30 (rewardsMaxSpread = 3.5¢, mid = 0.265):
- Eligible bid range: [0.230, 0.265]; eligible ask range: [0.265, 0.300].
- Competitive proximity-weight favors inside spread, not the gate boundary.

### A-S quoting adapted for LP yield (Eqs. 8–9 from [[market-maker-handbook-prediction-markets]])

```
Reservation:   r_x = x_t − q_t · γ · σ_b² · (T−t)
Half-spread:   2δ_x ≈ γ σ_b² (T−t) + (2/k) log(1 + γ/k)

target_spread = max(tick_size, min(rewardsMaxSpread, A-S_optimal_spread))
```

Reward incentive pulls spread toward tick-size; inventory risk + adverse selection push wider; `rewardsMaxSpread` is hard outer bound.

### Inventory skew (load-bearing)

```
|q_t| ≤ q_max ∝ 1 / max{S'(x_t), ε}
```

At rails (p near 0 or 1), inventory cap tightens exactly when MR also shrinks (the `p(1−p)` term goes to zero). The three programs together naturally incentivize quoting near center `p ∈ [0.35, 0.65]` — structural alignment between inventory tolerance and reward rate.

### Yield estimation — Starmer June 30 example

- **LR:** $400/day pool, $117K deployed liq. 10% pool share (~$11.7K deployed) → **$40/day = 0.34% daily = ~124% annualized raw LR**.
- **MR:** vol_24h $122.5K × 0.04 taker × 0.25 rebate = $1,220/day total MR pool. At 10% fill share: **$122/day additional**.
- **Combined (LR + MR, 10% share):** ~$162/day on $11.7K = **~505% annualized raw** (pre-adverse-selection, pre-operational-cost).

These raw yields do not survive uninformed quoting at scale.

## Secondary structure — sponsor-end depth pull

No classical structural-arb — this is yield extraction. One defined secondary opportunity per [[polymarket-strategy-matrix]]:

1. **During sponsorship:** LPs flood, spreads compress to tick, depth concentrates inside `rewardsMaxSpread`.
2. **When sponsor expires:** Exogenous LP withdrawal, spreads re-widen, remaining liquidity thinner and potentially stale.

**Tracking:** `clobRewards[].endDate`. Platform (`2500-12-31`) = permanent; sponsor with finite `endDate` within 1–7 days = actionable signal.

**Exploitation windows:**
- **As LP farmer:** Enter before sponsor launches (before depth concentrates); earn larger share from thin competition; reduce as HFT capital arrives.
- **As directional trader:** Use sponsor-compressed spreads for low-cost directional execution; plan exit before `endDate`.

## Microstructure: you are the microstructure

LP yield farming does not exploit microstructure — it constitutes it.

- **SF2 (uniform-grid depth, L1/L10 = 0.137):** Caused by LP farmers per [[polymarket-microstructure]]. Entering replicates equilibrium, not exploits departure.
- **SF4 (HHI = 0.031, ~32 effective makers top-100):** Yield contested at top. On thin markets (p90 HHI = 0.119, ~8 makers), pools less contested — **retail edge concentrates here**.
- **Adverse selection is NOT primary risk.** Glosten-Harris median φ ≈ 0 on top-100 stratum per [[polymarket-microstructure]] §6 — consistent with LP-vs-LP flow. But:
  - φ ≈ 0 is cross-sectional; individual fill events near scheduled announcements can be informative.
  - VPIN toxicity guards remain mandatory ([[market-maker-handbook-prediction-markets]] §4.5).
- **Inventory accumulation is primary P&L risk** (consistent with c ≈ 0, φ ≈ 0). LP quoting both sides symmetrically in a market that moves 20¢ carries large directional position. Critical: MR-generating fills are exactly the fills that accumulate inventory.
- **SF8 (depth decay):** β ≈ 0.305 (vol-controlled) → ~6% less depth per 10× reduction in seconds-to-close. Reduce quote size and `q_max` as resolution approaches.

## Saturation

Sophisticated MMs (Jump-class, Wintermute-class) almost certainly active in top-100. Evidence:
- SF4 median HHI = 0.031 top-100.
- FIFA sub-markets: spread = 0.001 (1 tick), `rewardsMaxSpread = 0` or 2.5¢ — HFT-saturated.
- NBA OKC: spread = 0.01 (1 tick).

**Retail LP edge concentrates in three places:**

1. **Esports sponsor pools:** ~$3,412 USDC per Valorant BO3 series per [[polymarket-lp-incentives]] 2026-05-16. HHI likely at p90+ range (few effective makers). Institutionals focus on top-100; esports structurally under-covered.
2. **Mid-cap political date-ladders with active LR:** Starmer — $300–400/day with $98–129K deployed. Large reward/capital ratio; not yet saturated to 1-tick spread.
3. **Cross-program optimization:** Running LR + MR + SR simultaneously with explicit MR fill-rate awareness beats single-program LPs at equal capital. Most retail LPs optimize for proximity (LR) only, ignoring MR.

**Saturation signal:** spread = tick-size AND `rewardsMaxSpread` loose AND multiple active maker addresses. When all three co-occur, yield per dollar = exit signal.

## Capital intensity profile

| Dimension | LP Yield Farming | Predictive-Edge |
|---|---|---|
| Capital req | High — rewards scale with deployed | Low — edge in sizing |
| Holding period | Continuous quote maintenance | Discrete enter/hold/exit |
| P&L driver | Daily reward accrual | Resolution outcome |
| Primary risk | **Inventory accumulation** | Resolution miss |
| Operational overhead | Quote mgmt, fill monitoring, rebalancing | Model updates, position tracking |
| Compounding | Reward reinvestment | Kelly growth on correct calls |

**Capital floor for three-program stack on mid-sized market:** ~$25K–$100K per market to hold material reward share while absorbing fill inventory without breaching `q_max`.

## Targeting logic (Gamma API filter)

```
rewardsDailyRate > threshold          # active reward pool
AND rewardsMaxSpread > 0              # explicit spread gate
AND liquidityNum < saturation_cap     # under-LP'd
AND volume24hr > volume_floor         # sufficient flow for MR income
AND feesEnabled = True                # MR active
```

**Today's candidate (2026-05-16):** Starmer date-ladder cluster — all three legs `rewardsDailyRate = 200–400 USDC/day`, `rewardsMaxSpread = 3.5–4.5¢`, deployed liq $98–129K (not saturated), vol $30–125K/day. Fee type `politics_fees`, rate 4%, rebate 25%.

**Second tier:** Active Esports sponsor markets (require separate query or finite-`endDate` scan).

**Avoid:** FIFA sub-markets (institutional saturation); Geopolitics (fee-free → zero MR pool).

## Risk register

| Risk | Mechanism | Mitigation |
|---|---|---|
| **Inventory accumulation** | One-sided fills → directional exposure; adverse resolution = full loss | A-S inventory skew (Eq. 8); `q_max` cap; cancel-replace if mid drifts >2 ticks |
| Adverse selection | Informed hits quote before public info | VPIN imbalance trigger; pause pre-announcements; widen as resolution approaches (SF8) |
| Reward program change | Platform reduces `rewardsDailyRate` | Monitor field daily; treat reward position as provisional |
| Spread gate tightening | Platform narrows `rewardsMaxSpread`; existing quotes invalidated | Monitor field; immediate requote inside new band |
| Sponsor cancellation | Third-party cancels mid-cycle | Irrevocability rule limits this; factor early-termination into IRR |
| Fee-category zero (Geopolitics) | Fee-free → zero MR income | Exclude from MR calc; still eligible for LR/SR |
| Both-sides rule near resolution | Markets below $0.10 mid require both-side quotes | Exit or maintain both-side; inventory cap tightens |
| Oracle delay spread blowout | Post-resolution spreads spike ~7,500 bps per [[polymarket-microstructure]] NBA data | Cancel all quotes 15–30min before expected resolution |
| Competition saturation | HHI drops → reward share per dollar < capital cost | Re-allocate to lower-HHI; use spread=tick as saturation signal |
| Holding rewards mechanics unknown | `holdingRewardsEnabled: True` on select markets | Do not model; treat as upside optionality |

## Decision-tree mapping

1. **Q1 YES-theme?** Mixed — meta-strategy, not predictive. Yields are real on under-LP'd markets.
2. **Q2 Data source?** YES — Gamma API exposes LR + MR + SR + spread gate in one call.
3. **Q3 Structural-arb?** No classical arb; sponsor-end depth pull is the only documented secondary opportunity.
4. **Q4 Microstructure?** Yield farming **constitutes** microstructure (SF2 caused by LPs); not exploitable departure but participation in equilibrium.

## Implementation phasing

**Phase 1 — Monitoring (no capital):**
- Gamma API poller every 15min; filter `rewardsDailyRate > 1 AND rewardsMaxSpread > 0`; rank by `rewardsDailyRate / liquidityNum`.
- Track `rewardsMaxSpread` changes per market as policy-shift signals.
- `clobRewards[].endDate` monitor for sponsor expiry alerts within 7 days.
- Cross-validate Gamma API vs `polymarket.com/rewards` (Playwright-rendered) — differences reveal sponsors not yet in `clobRewards`.

**Phase 2 — Single-market paper deployment:** Target one Starmer date-leg. Quote via A-S with inventory skew; `rewardsMaxSpread` as outer bound. Toxicity guards: cancel on VPIN threshold; pause 24h before key political events. P&L attribution: LR / MR / SR / adverse-selection / inventory carry.

**Phase 3 — Multi-market stack:** Scale to 3–10 markets; aggregate reward income vs capital. Cross-market inventory netting where correlated ([[market-maker-handbook-prediction-markets]] §4.4).

## Open questions

1. **Maker HHI on targeted markets** — Gamma API doesn't expose per-market maker concentration. Need on-chain `OrderFilled` maker-address analysis to estimate competition in Starmer/Esports clusters before committing capital.
2. **Fill rate empirics** — What fraction of quotes inside `rewardsMaxSpread` actually fill on mid-cap political markets? MR is zero without fills. Requires on-chain `OrderFilled` backtest.
3. **Reward program stability** — `endDate: 2500-12-31` suggests open-ended, but $1M CLOB v2 program (launched 2026-04-28) has implicit budget. Track total daily payout vs announced program size.
4. **Holding rewards mechanics** — `holdingRewardsEnabled: True` on select FIFA sub-markets. Fourth yield layer not yet in wiki.
5. **Sponsor vs platform decomposition** — Gamma `clobRewards` rolls platform + sponsor into `rewardsDailyRate`. Distinguishing programmatically may require on-chain sponsor-deposit events.

## Source

- `raw/feasibility/lp-yield-farming/summary.md` (2026-05-16)
- [[polymarket-lp-incentives]] — three-program mechanics, formulas, Esports sponsor data 2026-05-16
- [[market-maker-handbook-prediction-markets]] — A-S quoting, inventory cap, toxicity guards
- [[polymarket-microstructure]] — SF2/SF4 depth profile, Glosten-Harris φ=0, SF8 depth decay
- Gamma API live pull 2026-05-16: `events?active=true&closed=false&limit=30`

## Related

- [[polymarket-lp-incentives]]
- [[market-maker-handbook-prediction-markets]]
- [[polymarket-microstructure]]
- [[polymarket-strategy-matrix]]
- [[polymarket-architecture]]
- [[arbitrage-taxonomy]]
- [[polymarket-liquidity-evolution]]
- [[feasibility-review]]
