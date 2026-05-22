# Polymarket Liquidity Evolution

Tsang & Yang (2026) track Polymarket's 2024 U.S. Presidential Election markets over Jan–Nov 2024 and document a clean liquidity-maturation pattern: arbitrage-deviation half-life collapses from **~2 hours in April 2024 to 0.74 minutes by October 2024** on the Trump YES market; Kyle's λ falls from **0.53 → 0.01** on the same market. Implication for strategy: profitable arb windows live in the mid-maturity phase (weeks-to-months before resolution, after the market lists but before liquidity deepens). In a fully-matured market the deviation closes faster than retail human execution.

## Sample and scope

- Platform: Polymarket. Markets: 2024 U.S. Presidential Election event (Trump YES is the headline series; Harris and Biden YES tracked alongside).
- Time period: Jan 1 – Nov 6, 2024 (Fox News projection of Trump win at 2024-11-06 06:46:00 UTC used as a natural cutoff for the sample, not as the formal resolution timestamp).
- Data: on-chain Polygon `OrderFilled` + `OrdersMatched` from the `NegRiskCTFExchange`. Source: `raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §3, §5, §7.
- In-sample, observational; no out-of-sample forecast test.

## Arbitrage-deviation half-life

Construct 5-minute VWAP `δ_t^m = P_t^{m, YES} + P_t^{m, NO} − 1` per market `m`. Fit AR(1) per calendar month: `δ_t^m = α^m + ρ^m · δ_{t-1}^m + ε_t^m`. Half-life:

```
τ_{1/2}^m = − ln(2) · Δ / ln(ρ^m),   Δ = 5 min
```

Empirical trajectory by month (`raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §5):

| Market | Peak half-life | When | Final half-life | When |
|---|---|---|---|---|
| Trump YES | ~2 hours | April 2024 | 0.74 min | October 2024 |
| Trump YES | — | — | 0.67 min | November 2024 |
| Harris YES | >30 hours | March–April 2024 (pre-Biden-withdrawal) | a few minutes | Fall 2024 |
| Biden YES | ~3 hours | March–April 2024 | ~8 minutes | July 2024 |

**Strategy reading.** [[arbitrage-taxonomy]]'s Market Rebalancing Arbitrage requires the deviation to persist long enough for a non-atomic CLOB execution to clear both legs. Early-2024 windows (hours) were trivially exploitable; by October 2024, the window had compressed to ~40 seconds — below conservative human execution latency, leaving only programmatic actors with sub-second order placement.

## Kyle's λ — price impact maturation

Procedure (`raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §7):

1. Trade direction inferred via tick rule: `d_n = sign(p_n − p_{n−1})`; ties carry forward last non-zero direction (Lee & Ready 1991).
2. Signed order flow `q_n = d_n · tx_n` (transaction size in $M USDC).
3. Hourly aggregation: VWAP price `p^VWAP_t`, net flow `Q_t = Σ_{n∈t} q_n`.
4. Log-odds transformation `θ_t = ln(p_t / (1 − p_t))`; first-difference `Δθ_t = θ_t − θ_{t−1}`.
5. Rolling OLS over 30-day = 720-hour window: `Δθ_τ = λ_T · Q_τ + ε_τ`. Output: time series `{λ̂_t}`.

Applied to Trump YES only (most liquid market in the event):

| When | λ̂ | Implied Δp per $1M net buy at p=0.5 |
|---|---|---|
| End of July 2024 | ~0.53 | ~13.25 pp |
| After September 2024 | ~0.04 | ~1.00 pp |
| October 2024 | ~0.01 | ~0.25 pp |

Approximation used:

```
Δp_t ≈ p_t (1 − p_t) · Δθ_t = p_t (1 − p_t) · λ̂_t · ΔQ_t
```

derived from `dθ/dp = 1 / (p(1 − p))`. **Manipulation susceptibility** at λ = 0.53 is ~50× higher than at λ = 0.01 for the same $ size, illustrating why thin early markets are both arb-rich and manipulation-prone. The October episode of large-account two-sided inflows was *not* one-sided manipulation: the trader-disagreement measures (exposure dispersion `D_t`, headcount polarization `P_t^N`, volume-weighted polarization `P_t^V` — see Source §4.3) are consistent with heterogeneous beliefs rather than coordinated push.

**Soft tension with [[polymarket-microstructure]]:** Dubach (2026) finds Kyle's λ is sign-fragile and orders-of-magnitude unstable across sample steps in a cross-section of 600 markets. Tsang & Yang report a smooth monotonic trajectory on a single high-liquidity market with on-chain direction and 30-day rolling windows. Reconciliation: different objects (single market over time vs cross-section at instant) and different inference procedures (rolling-window OLS at 1-hour aggregation vs cross-sectional regression at 1 s / 10 s / 60 s / 300 s). The trajectory is informative about *this* market's maturation; do not generalise λ values to other markets without re-estimating.

## Volume mismeasurement — methodology aside

Naive aggregation of `OrderFilled` reports $958.48M of Trump-market volume in October 2024 vs **$391.03M exchange-equivalent under decomposition** — overstatement factor **~2.45×**. From July–November, raw `OrderFilled` exceeds the decomposed gross-activity `V^G` by 60–88 % and exceeds exchange-equivalent `V^E` by more than 2× (`raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §3.3).

The decomposition splits each transaction into six components (Yes/No × trade / mint / burn) and aggregates into:

```
V^E_{YES}(T)  = Σ trade_vol_τ + min(Σ mint_vol, Σ burn_vol)        — exchange-equivalent
F_{YES}(T)    = Σ mint_vol_τ − Σ burn_vol_τ                        — net fresh capital
V^G_{YES}(T)  = V^E_{YES}(T) + |F_{YES}(T)|                        — gross activity
```

Inputs: on-chain `OrderFilled` and `OrdersMatched` from the `NegRiskCTFExchange` (binary markets use `CTFExchange` — see [[polymarket-architecture]]). Conversion events excluded by design.

Operational implication: any strategy or sizing decision that consumes platform-reported volume is consuming a 2–3× overstatement. Use the `V^E` decomposition (or its `V^G` variant) for serious liquidity assessment. The methodology is portable to any tokenized prediction market with mint/burn primitives; see the formal equations in the source's §3.2 (Eqs. 1–12).

## When in a market's life to act

Composite picture from the half-life trajectory and λ trajectory:

- **Listing → first few weeks** (thin): λ high (manipulation susceptibility), arb half-life large (hours), but order-book depth shallow — both arb and informed-trading are size-constrained even though prices are sticky.
- **Mid-maturity** (a few weeks in, before peak attention): half-life on the order of minutes, λ decreasing, depth growing — *the window where the [[arbitrage-taxonomy]] strategies extract the most $-weighted profit*.
- **Peak attention** (close to resolution): half-life sub-minute, λ near 0.01, depth at its highest — purely programmatic execution dominates; manual operators are crowded out.
- **Post-resolution proposal** (oracle-waiting window, sports-NBA observation in `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md`): makers withdraw, bid-ask explodes (~7,500 bps observed for NBA), apparent arb signals are mostly stale-order artefacts — see [[single-market-arbitrage-empirics]] for the post-game filter.

## Source

- `raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` — Tsang & Yang (2026), "The Anatomy of a Blockchain Prediction Market: Polymarket in the 2024 U.S. Presidential Election". On-chain Polygon data; transaction-level accounting framework; AR(1) half-life estimation; rolling-OLS Kyle's λ; trader-disagreement measures.
- `raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §7 — cross-sectional λ-instability evidence used in the soft-tension flag above.
- `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md` §3 — post-game oracle-window spread behaviour (cross-link, not primary source).

## Related

- [[polymarket-microstructure]]
- [[polymarket-architecture]]
- [[arbitrage-taxonomy]]
- [[single-market-arbitrage-empirics]]
