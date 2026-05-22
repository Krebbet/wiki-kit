# Polymarket LP Incentive Programs

Polymarket runs **three distinct liquidity-provider incentive programs**, each with a different funding source and reward formula. An LP can earn from all three simultaneously on the same market. The three are: **Liquidity Rewards** (platform-funded daily pool, proximity-weighted), **Maker Rebates** (taker-fee-funded, per-fill), and **Sponsor Market Rewards** (third-party-funded, daily-distributed). The Rewards landing page (`polymarket.com/rewards`) is the operator-facing queue showing live sponsor reward pools per market.

This page consolidates all three. Sources: `raw/research/polymarket-creation-and-secondary-market/05-help-sponsor-market-rewards.md`, `06-help-maker-rebates.md`, `07-help-liquidity-rewards.md`, `08-polymarket-rewards-landing.md` (all captured 2026-05-16).

## Program comparison at a glance

| Program | Funded by | Distribution | Eligibility | Minimum payout |
|---|---|---|---|---|
| **Liquidity Rewards** | Polymarket platform budget | Daily ~00:00 UTC | Limit orders within per-market max-spread band; both-sides rule below $0.10 mid | $1 USDC accrued |
| **Maker Rebates** | Taker fees from fee-enabled categories | Daily USDC | Limit orders that add liquidity and *get filled* (taken); fee-free categories (Geopolitics) excluded | $1 USDC accrued |
| **Sponsor Market Rewards** | Third-party USDC deposits | Daily 00:00 UTC | Same as Liquidity Rewards (proximity-weighted) | None (deposits as small as $0.1/day) |

## 1. Liquidity Rewards (platform-funded)

(Source: `raw/research/polymarket-creation-and-secondary-market/07-help-liquidity-rewards.md`.)

The platform-funded reward pool distributed daily to limit-order makers whose orders sit close to the market mid-price. **Distinct from Maker Rebates** (which is taker-fee-funded) and **Sponsor Rewards** (which is third-party-funded). This is the layer that mechanistically explains the uniform-grid depth profile and ~32 effective-makers observation in [[polymarket-microstructure]] SF2 / SF4.

### Mechanics

- **Computation:** proximity-weighted share of a per-market daily pool. Closer to mid-price = larger share. Order size also factors in.
- **Max-spread gate:** each market sets its own max-spread parameter (example: `±3¢`). Orders outside that band earn zero. Visible as blue-highlighted lines in the order-book UI.
- **Both-sides rule:** if market midpoint < `$0.10`, orders must appear on **both sides** to qualify. Blocks one-sided farming near resolution where prices are pinned to the rail.
- **Payout:** daily ~midnight UTC; `$1` minimum accrued before payout; sub-$1 amounts withheld and roll over.
- **Recent rollout:** CLOB v2 launched 2026-04-28 with a $1M liquidity-rewards program targeting Finance, Politics, and Culture (Falcon X / news context per [[platform-comparison-kalshi-polymarket]]; the help-center article does not mention the $1M figure directly).

### Operator reading

The max-spread gate is the **single most-load-bearing operational parameter** here. An LP placing wide-spread orders earns zero regardless of order size; an LP placing tight-spread orders is competing within a defined band of liquidity. The depth-profile observation in [[polymarket-microstructure]] SF2 (`depthL1 / depthL10 ≈ 0.137`, close to uniform-grid) is a direct consequence: LPs cluster at the inside spread because reward incentives reward that proximity.

## 2. Maker Rebates (taker-fee-funded)

(Source: `raw/research/polymarket-creation-and-secondary-market/06-help-maker-rebates.md`.)

The taker fees Polymarket collects in fee-enabled categories pool daily into a USDC rebate fund. The fund is redistributed to limit-order makers whose orders **actually get filled** (i.e., a taker hits their resting liquidity).

### Mechanics

**Per-fill fee-equivalent (the per-share contribution to the rebate pool):**

```
fee_eq = C × feeRate × p × (1 − p)
```

where:
- `C` = number of shares filled,
- `feeRate` = taker fee for that category (per Fee Structure V2 — see [[platform-comparison-kalshi-polymarket]]),
- `p` = fill price (implied probability).

The `p × (1 − p)` term comes from Polymarket's fee normalization: fees are smaller near the rails (p ≈ 0 or 1) because absolute fee-in-cents shrinks as price flattens; this is structurally why thin-market makers face a tail-price-floor effect (very small trades may collect zero fee → zero rebate contribution).

**Daily rebate to a maker:**

```
daily_rebate = (your_fee_eq / total_fee_eq_in_market) × rebate_pool_for_market
```

**Competition is strictly per-market** — your rebate share is computed against other makers on the same market only.

### Rebate-rate parameters (% of fee-pool returned as rebate)

| Category | Rebate % | feeRate (taker) | Net rebate-per-share at `p = 0.5` |
|---|---|---|---|
| Crypto | **20%** | 0.072 | **0.0036** |
| Sports | 25% | 0.030 | 0.001875 |
| Finance / Politics / Tech / Mentions | 25% | 0.040 | 0.0025 |
| Economics / Culture / Weather / Other | 25% | 0.050 | 0.003125 |
| Geopolitics / World Events | (excluded — fee-free) | 0 | 0 |

**Reading:** Crypto dominates rebate-per-share despite its lower 20% rebate rate, because its `feeRate` (0.072) is ~2.4× higher than the next-highest category. Sports is the *worst* rebate-per-share economy in absolute terms (low fee, normal 25% rebate) — but the on-platform sports volume is so much higher (per [[platform-comparison-kalshi-polymarket]]) that the *aggregate* sports rebate pool may still be the largest.

**Open conflict flag:** the `feeRate` values above are extracted from the help-center capture and should be cross-checked against the Fee Structure V2 table in [[platform-comparison-kalshi-polymarket]] (Sacra source, March 2026). They appear to match.

### Operator reading

Maker Rebates reward a different behavior from Liquidity Rewards. Liquidity Rewards pays you for **posting**; Maker Rebates pays you only when your order **fills**. An LP who posts tight-spread orders that don't fill earns from Liquidity Rewards but nothing from Maker Rebates. An LP whose orders fill earns from both, plus any active Sponsor Rewards stacked on top. The combined LP-yield calculation for a given market is therefore:

```
LP_yield = liquidity_rewards_share + maker_rebate_share + Σ active_sponsor_rewards_share
```

all computed per-market against your liquidity share.

## 3. Sponsor Market Rewards (third-party-funded)

(Source: `raw/research/polymarket-creation-and-secondary-market/05-help-sponsor-market-rewards.md`.)

**Anyone with USDC can sponsor any market** to pay rewards to its LPs. This is the closest analog to "creating a market" available to a retail user — Polymarket's market-creation gate (see [[polymarket-market-taxonomy]] "Market creation pipeline") means users can only suggest new markets, not create them; *but* users **can** unilaterally boost liquidity into existing markets via sponsorship.

### Mechanics

- **Pick a market:** any active market.
- **Set budget and duration:** `daily_rate × days` USDC. Example: $500 over 10 days = $50/day.
- **Minimum:** `$0.1` per day.
- **Distribution:** proportional to LP liquidity share, daily at 00:00 UTC. Same scoring formula as native Liquidity Rewards.
- **Daily underrun:** if LPs don't fully earn the daily pool (e.g., low activity day), unused portion returned to sponsor at 00:00 UTC. **Sponsor never overpays the daily rate.**
- **Auto-refund on early resolution:** unused balance returned automatically (pro-rated). Example: $500 over 10 days, market resolves after 5 → $250 spent, $250 refunded.
- **Stacking:** multiple sponsors on the same market stack additively; LPs earn from the combined pool plus native rewards.
- **One active sponsorship per wallet per market.** No mid-flight top-up — must wait for current to end or cancel.
- **Custody:** fully on-chain in the Rewards smart contract; Polymarket has zero withdrawal rights.

### Cancellation — partial refund only

If you cancel mid-cycle:

- Today's allocation (cancellation time → next 00:00 UTC) is **irrevocable**. It remains in the pool for LPs; whatever LPs don't earn from it is returned to you at 00:00 UTC.
- Everything from the next 00:00 UTC onward is refunded immediately.

This prevents the attack of briefly sponsoring → attracting liquidity → cancelling before any payout actually happens.

### FAQ-verbatim — does the sponsor earn anything?

Polymarket's own statement: *"There are no rewards for the Sponsor providing funds to the Rewards Pool. The primary incentive to sponsor rewards is to drive liquidity into that market."*

**No direct return for sponsoring.** The incentive is purely *strategic*: a sponsor wants more liquidity on a specific market because they intend to trade size into it themselves and need a deep book to do so without paying the longshot-spread premium (see [[polymarket-microstructure]] SF1).

### Live data from `polymarket.com/rewards` 2026-05-16

(Source: `raw/research/polymarket-creation-and-secondary-market/08-polymarket-rewards-landing.md`.)

At capture, **Esports — specifically Valorant — dominated the active Sponsor Rewards queue**:

| Market type | Max spread | Min shares | Reward pool |
|---|---|---|---|
| Valorant BO3 match winner (Esports World Cup China Qualifier) | ±2¢ | 250 | 2,132 USDC each |
| Valorant per-map markets | ±2¢ | 250 | 320 USDC each |
| Valorant Games Total O/U | ±2¢ | 250 | 640 USDC each |
| CS2 map markets | ±4¢ | 50 | 10 USDC |
| R6S match markets | ±2¢ | 500 | 10–27 USDC |

A typical Valorant BO3 series bundle (winner + per-map + games O/U): **~$3,412 USDC total reward pool per match series**. 56 pages of markets in the full queue at capture — esports operators are spending materially on liquidity acquisition.

## Operator-side strategy notes

(Editorial synthesis, not source claims.)

- **Stacked sponsorship is a queryable signal of artificially deep books.** A market with multiple active sponsors visible on `polymarket.com/rewards` will have compressed arb spreads for the sponsorship duration. Cross-link to [[arbitrage-taxonomy]] — sponsor-induced depth may *temporarily* close MRA opportunities that would otherwise be exploitable.
- **Liquidity Rewards' max-spread gate is the structural reason Polymarket has SF4 depth concentration.** If you're modelling depth dynamics on a Polymarket market, the per-market max-spread parameter is a load-bearing input.
- **The combined LP-yield calculation is per-market** — no cross-market netting. An LP wanting to optimize cumulative yield should target markets where (a) all three programs are active, (b) the sponsor stack is large, (c) competition (other makers) is thin.
- **Sponsor mechanism is the closest retail-accessible "create-a-market" lever.** If you can't get Polymarket to list your suggested market via the @polymarket Twitter channel (see [[polymarket-market-taxonomy]]), you can still concentrate liquidity into an existing market by sponsoring it.

## What this page does NOT cover

- **Reward queue authentication** — `polymarket.com/rewards` likely shows additional per-LP earnings / leaderboards behind a wallet-connect, which the capture-script flow can't reach. The 56-page market queue we have is the public surface only.
- **Historical reward payouts** — no time-series of total rewards paid across all programs. Would need on-chain analysis of the Rewards smart-contract transactions to reconstruct.
- **Optimal-quoting strategy under all 3 programs.** The combined `LP_yield` formula above is correct in shape, but the optimal-spread-and-size choice depends on per-market max-spread, current sponsor pool, fill probability — non-trivial. This is the natural application target for [[market-maker-handbook-prediction-markets]] adapted for Polymarket's specific reward structure.

## Source

- `raw/research/polymarket-creation-and-secondary-market/05-help-sponsor-market-rewards.md` — Polymarket Help Center "Sponsor Market Rewards"; full FAQ extracted (cancellation flow, auto-refund, stacking, custody, sponsor-return-is-zero).
- `raw/research/polymarket-creation-and-secondary-market/06-help-maker-rebates.md` — Polymarket Help Center "Maker Rebates Program"; per-fill fee-equivalent formula, per-category rebate % and feeRate.
- `raw/research/polymarket-creation-and-secondary-market/07-help-liquidity-rewards.md` — Polymarket Help Center "Liquidity Rewards"; max-spread gate, both-sides rule, daily payout.
- `raw/research/polymarket-creation-and-secondary-market/08-polymarket-rewards-landing.md` — Polymarket Rewards landing page snapshot 2026-05-16; live Esports queue (~$3,412/Valorant series).

## Related

- [[polymarket-architecture]]
- [[polymarket-market-taxonomy]]
- [[polymarket-microstructure]]
- [[platform-comparison-kalshi-polymarket]]
- [[market-maker-handbook-prediction-markets]]
- [[arbitrage-taxonomy]]
