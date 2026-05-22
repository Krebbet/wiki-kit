# Feasibility — Crypto Short-Horizon

BTC/ETH/SOL Up-Down (5m/15m/1h/4h), Daily Price Range, Monthly Hit Price, Pre-Market FDV. **Maximum-saturation quant territory** with zero retail LLM edge and near-zero retail quant edge vs CEX market-makers (Jump, Wintermute, GSR). The only retail-accessible niches are Pre-Market FDV (token launches, domain-knowledge-dependent) and far-OTM monthly hit-price strikes where vol-skew may mis-price. Live Gamma API 2026-05-16.

## Subcategory verdict matrix

| Sub-domain | Verdict | Reason |
|---|---|---|
| 5m / 15m Up-Down (BTC/ETH/SOL) | **AVOID** | Maximum saturation; sub-second latency required; institutional LP presence; zero info edge on Binance-resolved binary |
| 1h / 4h Up-Down | **AVOID** | Same structure; lower latency pressure but identical saturation profile |
| Daily Price Range (bracket) | **MARGINAL** | Bracket Σ-check for MRA per [[arbitrage-taxonomy]] only; directional same saturation |
| Monthly Hit Price (near-ATM) | **AVOID** | Institutionally covered; HAR-RV table-stakes |
| Monthly Hit Price (far-OTM) | **CONDITIONAL** | Implied-vol skew vs RV skew may diverge; calibration-scanner edge; low capital at far-OTM |
| Pre-Market FDV (token launch) | **CONDITIONAL** | Domain-knowledge edge; resolution-source vagueness is a risk; best retail crypto opportunity |

## Market landscape (2026-05-13 snapshot, 261 total crypto markets)

| Subcategory | Count | Volume profile |
|---|---|---|
| 5 Min | 7 | BTC series $22M lifetime aggregate; per-instance $5K–$50K |
| 15 Min | 7 | Same structure |
| 1 Hour | 9 | Same structure |
| 4 Hours | 7 | Same structure |
| Daily | 11 | Daily Above/Below BTC May 16: $2.7M single-instance |
| Monthly Hit Price | 22 | BTC May 2026: $17.1M aggregate across 11 sub-markets; May 2025 resolved Yes at $110K, $37M |
| Pre-Market | 115 | Structurally distinct: FDV/token-sale/token-launch |

## Critical resolution-feed finding

**Polymarket BTC price markets resolve via Binance BTC/USDT 1-minute candle data — NOT Chainlink or Pyth.** Verbatim from Gamma API resolution rules (2026-05-16):

> "This market will immediately resolve to 'Yes' if any Binance 1 minute candle for Bitcoin (BTCUSDT) between [date range] has a final 'High' price of $[threshold] or higher."

> "Resolution source is Binance BTC/USDT 'High' / 'Close' prices at 1m chart settings"

**Closes the [[uma-optimistic-oracle]] open follow-up** on crypto resolution feed: Binance for BTC short-horizon markets. **OpenSea Pre-Market FDV uses "most liquid price source"** — explicitly vague, no named exchange, elevated UMA dispute risk.

**Implications:**
- Eliminates Chainlink/Pyth index-vs-spot basis risk for BTC.
- Introduces Binance-specific feed risk (outage, maintenance, flash-spike vs Coinbase/Kraken).
- UMA OO ($500 USDC.e bond, $5 reward per [[uma-optimistic-oracle]]) handles dispute; data source is Binance, not UMA.
- 2h challenge window post-resolution locks capital — annualized cost-of-capital matters for per-trade sizing on 5m markets.

## Edge sources evaluated

| Edge | Verdict | Reason |
|---|---|---|
| LLM/textual | None | Crypto LLM-weak; CWR deeply negative; tick-driven not text-driven per [[llm-forecasting-by-domain]] |
| HAR-RV vol forecast | Table-stakes | Forecasts range, not direction; size-down during high-vol; institutional default |
| Avellaneda-Stoikov LP quoting | Net-negative without sub-second latency | Final 60s of 5m window is pick-off territory; VPIN toxicity guards mandatory |
| Pyth on-chain feed arb | N/A | Pyth not the BTC resolution feed |
| Chainlink feed basis | N/A | Chainlink not the BTC resolution feed |
| Binance feed anomaly arb | Viable, narrow | Cross-venue spread when Binance prints anomalously; rare; institutions already monitor |
| Binance WebSocket | Table-stakes | `wss://stream.binance.com:9443/ws/btcusdt@kline_1m`; same as resolution feed |

**A-S framework adapted for 5m window** ([[market-maker-handbook-prediction-markets]] Eqs. 8–9):
```
r_x = x_t − q_t · γ · σ_b² · (T−t)         # reservation
2δ_x ≈ γ σ_b² (T−t) + (2/k) log(1 + γ/k)   # half-spread
```
As T−t → 0 in final 60s, anyone with sub-second feed picks off any LP without equivalent latency.

## Monthly Hit Price — barrier option framework

```
P(touch K) ≈ N[(log(K/S) − μT) / (σ√T)] +
              exp(2μ log(K/S)/σ²) · N[(−log(K/S) − μT)/(σ√T)]
σ from HAR-RV on Binance history
μ from CME futures curve (risk-neutral drift)
```
ATM = institutionally covered. **Far-OTM:** σ_imp backed out from each sub-market may diverge from realized vol skew. Scanner that computes σ_imp per strike vs RV skew forecast identifies mispricings. Retail-achievable. CME hedge is partial directional only (not the barrier payoff); calendar basis adds risk.

## Pre-Market FDV — the retail niche

**Examples (2026-05-16):**

| Slug | Vol | Sub-markets | Structure |
|---|---|---|---|
| Predict.fun FDV | $5M | 11 | $50M–$300M+ thresholds; "most liquid price source" |
| Printr public sale | $6.8M | 16 | Commitment tiers; resolves vs sale.printr.money |
| OpenSea FDV | $6M | 7 | $100M–$5B; "most liquid price source" |

**Why less saturated than price-tick:**
1. Resolution-source vagueness deters institutional MMs.
2. FDV depends on total supply (finalized at TGE), VC lockup, launch-day float — project-specific, non-fungible.
3. Edge needs domain knowledge, not crypto price feeds.
4. Low secondary-market liquidity makes delta-hedging impossible.
5. Jump/Wintermute/GSR do not run prediction-market books on FDV (their edge is systematic, not project-DD-based).

**Information sources:**
- Pre-launch whitelisted sale price × total supply → implied valuation floor.
- VC round valuation (Crunchbase, PitchBook) → comp anchor.
- Token unlock schedules (tokenomist.ai) → effective circulating supply at TGE.
- Community sentiment (Discord size, Twitter engagement, waitlist oversubscription).
- Comparable launches: Predict.fun $88M FDV → $50M Yes 93%, $100M Yes 88%.

**Edge hypothesis:** Operator with domain knowledge of a specific token (active ecosystem participant) has genuine information advantage vs generic quant. Closer to VC / early-stage investing edge than market-microstructure.

**Risk flag:** "Most liquid price source" undefined. If token launches on thin DEX with whale spike then dumps, UMA voters determine which source applies. Genuine dispute-risk exposure unique to Pre-Market.

## Saturation

- **5m/15m/1h/4h Up-Down:** Maximum tier. Equivalent to betting EUR/USD tick direction against a professional dealer desk. Recurring structure = sustained institutional LP presence. SF1 longshot premium (650–900 bps half-spread at tails) per [[polymarket-microstructure]] is the *residual* after compression. Maker rebate structurally lower for crypto (20% vs 25% other categories per [[polymarket-lp-incentives]]).
- **Daily / Monthly near-ATM:** Same.
- **Far-OTM monthly:** Lower saturation in vol-skew calibration layer; legitimate niche for small vol-pipeline operator.
- **Pre-Market FDV:** Lowest saturation. The retail niche.

## Capital + infrastructure

| Component | 5m/15m | Monthly Hit | Pre-Market FDV |
|---|---|---|---|
| Per-instance depth | $5K–$50K | $1M–$2M per strike | $300K–$700K per strike |
| Meaningful capital | $10K–$100K/series | $10K–$100K/strike | $5K–$50K/strike |
| Latency req | Sub-second | Minutes acceptable | Days–weeks |
| Modeling | A-S + HAR-RV | Barrier calibration | Comparables + project DD |
| Hedging | Impossible | Partial CME futures | None |
| Dispute monitor | Required (2h UMA) | Required | Required + higher dispute risk |
| Dev complexity | High | Medium | Low |
| Competitive moat | None vs institutions | Vol-skew scanner (niche) | Domain knowledge |

## Risks

1. **Feed concentration:** 100% Binance BTC/USDT for BTC resolution. Maintenance windows (~30min monthly) during active market = ambiguous resolution.
2. **UMA dispute (Pre-Market FDV):** "Most liquid price source" disputable for tokens on multiple DEXes.
3. **Wiki correction:** [[uma-optimistic-oracle]] prior assumption of on-chain feeds was incorrect for BTC price-tick markets — Binance is the named feed. Removes oracle manipulation risk; adds Binance-specific feed risk.
4. **Adverse selection (5m final 60s):** Without sub-second Binance feed, LP quoting in final window is net-negative EV.
5. **Lower LP rebate:** Crypto 20% vs 25% other categories per [[polymarket-lp-incentives]].
6. **No Pyth/Chainlink arb path:** On-chain oracle arb (DeFi-style) does not apply — resolution is off-chain Binance.

## Decision-tree mapping

1. **Q1 YES-theme?** Mixed — Pre-Market FDV YES; 5m/15m/1h/4h NO (saturated commodity quant).
2. **Q2 Data source?** YES — Binance WebSocket free; tokenomist.ai/Crunchbase free for FDV; CME futures for monthly hedge.
3. **Q3 Structural-arb?** Daily bracket Σ-check only; no ladder monotonicity in single-instance structures.
4. **Q4 Microstructure?** Saturated regime; only LP-yield-farming-equivalent edge with sub-second latency.

## Open follow-ups

1. Build far-OTM monthly vol-skew scanner: compute σ_imp per strike from market price; compare to HAR-RV skew forecast.
2. Pre-Market FDV pipeline: tokenomist.ai unlock schedules + Crunchbase comp + comparable-launch FDV anchors.
3. Binance feed anomaly detector: cross-venue (Binance vs Coinbase vs Kraken) spread monitor for 1m candle High/Low events.
4. Capture closed monthly Hit Price markets to backtest barrier calibration vs realized resolution.

## Source

- `raw/feasibility/crypto-short-horizon/summary.md` (2026-05-16)
- [[snapshots/polymarket-crypto-category-2026-05-13]]
- Gamma API live pulls (2026-05-16): crypto/bitcoin/pre-market tag slugs; Monthly Hit Price resolution rules (Binance BTC/USDT 1m candles confirmed); OpenSea FDV vague resolution

## Related

- [[uma-optimistic-oracle]]
- [[llm-forecasting-by-domain]]
- [[polymarket-strategy-matrix]]
- [[market-maker-handbook-prediction-markets]]
- [[polymarket-microstructure]]
- [[arbitrage-taxonomy]]
- [[polymarket-lp-incentives]]
- [[snapshots/polymarket-crypto-category-2026-05-13]]
- [[feasibility-review]]
