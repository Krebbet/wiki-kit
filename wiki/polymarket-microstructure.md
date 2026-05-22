# Polymarket Microstructure

Cross-sectional tick-level study of 600 Polymarket markets (Feb 21 – Apr 15, 2026; 6.4M trades) establishes eight stylized facts about Polymarket's CLOB microstructure. The headline operational finding: trade-direction inference from the public WebSocket feed agrees with on-chain ground truth ~59 % of the time — near chance — invalidating any feed-only direction-dependent measure. On-chain `OrderFilled` events are mandatory for effective spread, Kyle's λ, Roll, Amihud, Abdi–Ranaldo, or any other aggressor-sign-dependent quantity. Source: Dubach (2026), Sections 1–7.

## Headline: feed-only direction inference fails

For 600 markets in the panel (4 disjoint 7-day windows on the top-100 stratum):

- Volume-weighted sign-agreement: `0.592` (95% CI `[0.542, 0.659]`, market-clustered bootstrap).
- Panel mean: `0.615`; panel median: `0.591`; IQR `[0.526, 0.681]`; p10–p90 `[0.464, 0.841]`.

A noisy `sign_t ∈ {−1, +1}` does not merely attenuate `M = E[sign_t · f(price_t, mid_t, size_t)]`; it can flip its sign entirely. Consequence:

- **Effective spread:** sign flips on **67% / 50%** of comparable markets across the two windows when feed-inferred sign is replaced by on-chain.
- **Kyle's λ:** sign flips on **60% / 43%**.

Operational rule: use `OrderFilled` aggressor sign (encoded in `makerAssetId` / `takerAssetId` — see [[polymarket-architecture]]) for any direction-dependent measure on Polymarket.

## The eight stylized facts (Dubach 2026, Sec. 5)

### SF1 — Longshot spread premium

Median quoted half-spread by mid-decile (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §5.1):

- Central decile `p ∈ [0.4, 0.6]`: ~200–400 bps half.
- Tail `p < 0.10`: 650–900 bps half (1300–1800 bps full).

This is an **order of magnitude larger** than racetrack and IEM longshot premia (typically a few percent of stake). Author's interpretation: structural inventory risk on binary contracts (bounded upside, asymmetric downside) rather than behavioral longshot bias. *Caveat:* in-sample cross-section; no out-of-sample test; no comparison to Kalshi or non-decentralised venues. Sample: 600 markets, Feb 21 – Apr 15, 2026.

### SF2 — Depth profile near uniform-grid

`depthL1 / depthL10` ratio (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §5.2):

- Median **0.137**; uniform-grid benchmark **0.1**; p10 **0.033**, p90 **0.428**.
- 546 markets analysed.

Implication: Polymarket's depth profile is closer to a uniform grid across price levels than the **top-of-book concentration** assumed by classical CLOB microstructure models. Strategy implication: marginal-impact estimates calibrated to traditional equity-market depth profiles will systematically overstate execution cost on Polymarket.

### SF3 — Block-clock alignment null

Trade-arrival distribution shows no statistically significant alignment with the Polygon block boundary (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §5.3). No exploitable timing signal at the block-clock level.

### SF4 — Maker concentration (HHI) is low

Volume-weighted Herfindahl across maker addresses per market (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §5.4):

- Median HHI: **0.031** → ~32 effective makers.
- p90 HHI: **0.119** → ~8 effective makers.
- Max HHI: **0.40** → ~3 effective makers (thin markets).

Implication: the deep top-100 is broadly contested; thin markets cluster into a few hands and are correspondingly less liquid.

### SF5 — Category-conditional spreads

Spreads vary materially by category; category FE absorbs a large share of the dispersion in subsequent regressions (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §5.5). When pricing or backtesting across categories, do not pool naively.

### SF6 — Archive ingestion latency

WebSocket-to-archive ingestion median latency **41.5 ms** (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §5.6). Practical implication: feed-derived timestamps are not chain-grade truth; co-ordinate at block timestamp level (±4 s, median 2 s) for any cross-source analysis.

### SF7 — Wash share is small (relative to crypto exchanges)

Lower-bound wash-share metric across markets:

- Median **1%**; p99 **10.6%**; max **22.2%**.

Compares favourably with crypto token-exchange benchmarks of 25–70 % cited in the paper. Trustworthy enough that aggregate volume statistics are a reasonable input to liquidity backtests, but discount thin-market volume by p99 to be safe.

### SF8 — Depth decays as resolution approaches

Cross-sectional regression `log(mean_depth_L10) = α + β · log(seconds_to_close)` on 322 markets (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §5.8, Table 3):

| Specification | β | HC3 SE | t | R² |
|---|---|---|---|---|
| Bivariate | 0.818 | 0.113 | 7.2 | 0.13 |
| Category FE | 0.550 | 0.143 | 3.85 | 0.22 |
| Category FE + log(volume) | 0.305 | 0.104 | 2.94 | 0.49 |

The volume-controlled coefficient `β ≈ 0.305` implies **~6 % less mean depth per 10× reduction in seconds-to-close**, after volume mediation absorbs ~40 % of the bivariate effect. *Caveat:* cross-sectional, not within-market; do not use to forecast a *given* market's depth trajectory in isolation. Strategy implication: late entries face systematically worse liquidity; size early, exit early. Cross-link to the within-market evolution evidence in [[polymarket-liquidity-evolution]].

## Glosten–Harris spread decomposition (Dubach 2026, Sec. 6)

Effective half-spread decomposed as `S_eff / 2 = c + φ`:

- `c` = transitory (order-processing + inventory) component, recovered as the realized half-spread at 60 s lag.
- `φ` = adverse-selection residual.

Applied to the top-100 stratum (97 / 100 markets converge): **median `c` ≈ 0** and **median `φ` ≈ 0** (effective half-spread ≈ `−0.0003` probability points). Interpretation: once feed sign-errors are removed, no systematic adverse-selection signal survives on the most-liquid stratum. Heuristic implication: top-100 makers face near-zero realized adverse-selection cost; the longshot spread premium of SF1 is therefore best read as inventory-bound, not information-bound.

## Kyle's λ on Polymarket — instability warning

Same paper (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §7.2, §7.4): standard `Δprice = λ · signed_volume` is fragile.

- Sign flips on **60 % / 43 %** of comparable markets across the two windows when on-chain direction replaces feed-inferred direction.
- Estimates vary by **orders of magnitude** across sample steps (1 s, 10 s, 60 s, 300 s).
- Roll's estimator is invariant to sample step; effective spread and Amihud stable to ±10–20 % at 60 s vs 1 s.

**Soft tension with [[polymarket-liquidity-evolution]]:** Tsang & Yang (2026) report a smooth monotonic Kyle's λ trajectory `0.53 → 0.01` over the 2024 Trump YES market lifespan. Reconciliation: Tsang & Yang use a 30-day rolling OLS on a single market with log-odds transformation; Dubach is a cross-sectional snapshot across 600 markets with cross-section-level sign-sensitivity. The two findings are not in formal conflict — they sample different objects — but a long-running market may exhibit a stable trajectory in its own λ while the cross-section at any instant remains sign-fragile across markets. Flag for revisit when more single-market trajectories are available.

## Math — direction-dependent measure general form

```
M = E[sign_t · f(price_t, mid_t, size_t)]
```

Effective half-spread: `f = price_t − mid_t`. A noisy `sign_t` can flip the sign of `M`, not merely attenuate it. This is the single-sentence justification for why feed-only direction inference is unusable on Polymarket.

## Math — Glosten–Harris (Sec. 6, Eq. 1)

```
S_eff/2 = c + φ
```

Symbols: `S_eff` effective spread in probability points; `c` transitory order-processing/inventory component; `φ` adverse-selection residual. References: Glosten & Harris (1988), Huang & Stoll (1997), Madhavan, Richardson & Roomans (1997).

## Math — SF8 depth-decay (Sec. 5.8)

```
log(mean_depth_L10) = α + β · log(seconds_to_close)
```

See Table 3 above for the three specifications and coefficients.

## Source

- `raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` — Dubach (2026), "The Anatomy of a Decentralized Prediction Market: Microstructure Evidence from the Polymarket Order Book". 30 billion WebSocket events over 52 days joined to on-chain `OrderFilled`; 600 markets (top-100 by USDC volume + random-500). All numerical findings above are extracted from Sections 5–7 and Tables 1–3.
- `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md` §3 — corroborating empirical bid-ask spreads by phase (pre-game 392 bps, in-game 1031 bps, post-game 7533 bps); cited under [[single-market-arbitrage-empirics]] for the post-game oracle-delay phantom-arb artefact.

## Related

- [[polymarket-architecture]]
- [[polymarket-liquidity-evolution]]
- [[single-market-arbitrage-empirics]]
- [[combinatorial-arbitrage-empirics]]
- [[logit-jump-diffusion-kernel]]
