# Feasibility Assessment: Polymarket Crypto Short-Horizon Markets

**Date:** 2026-05-16  
**Scope:** BTC/ETH/SOL/XRP Up-Down (5m/15m/1h/4h), Daily Price Range, Monthly Hit Price  
**Status:** Structured quant domain — competitive, data-achievable, capital-constrained

---

## 1. Market Landscape

**Active markets (2026-05-13 snapshot):** 261 total crypto; short-horizon breakdown:

| Subcategory | Count | Character |
|---|---|---|
| 5 Min | 7 | Recurring binary; BTC series $22M lifetime aggregate |
| 15 Min | 7 | Same structure |
| 1 Hour | 9 | Same structure |
| 4 Hours | 7 | Same structure |
| Daily | 11 | Price-range bracket + Up-Down |
| Monthly | 22 | Hit-Price barrier ladder |
| Pre-Market | 115 | FDV / token-sale / token-launch (structurally distinct) |

**Volume profile (Gamma API, 2026-05-16):**
- BTC 5m series: $22M lifetime aggregate; per-instance volume is small (series recurs every 5 min, vol accrues over 100s of instances)
- Monthly Hit Price (BTC, May 2026): $17.1M aggregate across 11 sub-markets (May instance)
- Prior year BTC monthly hit: $37M (May 2025 resolved Yes at $110k)
- Daily Above/Below (BTC May 16): $2.7M single-day instance

**Implied spot at capture:** BTC ~$78k (per $78k sub-market at 67.2% Yes on May 16 pull)

**Key structural note:** The 5m/15m/1h/4h markets are *recurring*. Each instance is a fresh binary (Up/Down from previous close). Volume concentrates per-instance is small; the headline aggregate is the entire historical series lifetime. Per-round dollar depth is likely $5k–$50k.

---

## 2. Market Structure & Resolution Feed

**Critical finding from Gamma API (2026-05-16):** Polymarket's crypto price markets resolve via **Binance BTC/USDT 1-minute candle data** — NOT Chainlink or Pyth.

Confirmed verbatim from resolution rules:
- Monthly Hit Price: *"This market will immediately resolve to 'Yes' if any Binance 1 minute candle for Bitcoin (BTCUSDT) between [date range] has a final 'High' price of $[threshold] or higher."*
- Above/Below daily: *"Resolution source is Binance BTC/USDT 'High' / 'Close' prices at 1m chart settings"*
- OpenSea FDV (Pre-Market): *"The resolution source for this market is the most liquid price source available"* — explicitly vague, no named exchange or feed.

**Implication for arb risk:** The wiki's prior working assumption ([[uma-optimistic-oracle]] open follow-up) that crypto price markets use Chainlink or Pyth is **incorrect** for Bitcoin price markets. The feed is Binance public market data — specifically 1-minute candle High/Low/Close values. This eliminates Chainlink/Pyth index-vs-spot basis risk for BTC but introduces **Binance-specific feed risk** (Binance outage, maintenance window, or flash-spike on Binance vs. Coinbase/Kraken). A spread between Binance spot and other venues creates a genuine arb if Binance moves anomalously.

**Pyth / Chainlink role (per [[uma-optimistic-oracle]]):** Chainlink handles deterministic/financial events (FalconX Jan 2026); Pyth used for "some markets" (Grayscale Sep 2024). Neither is the resolution feed for BTC/ETH/SOL short-horizon price-tick markets confirmed in this corpus. The prior open follow-up in [[uma-optimistic-oracle]] can be partially closed: Binance is the named feed for BTC price markets.

**UMA oracle role:** UMA's OO handles dispute resolution but the *data source* is Binance, not UMA-provided feeds. Bond mechanics: $500 USDC.e proposer bond, $5 reward (per [[uma-optimistic-oracle]]).

**Resolution timing (5m markets):** The 5-minute Up-or-Down market resolves at the close of the 5-minute window using Binance 1m candle data (inferred from structure). UMA proposal happens post-close; 2-hour challenge window then applies. Capital is locked during the challenge window; annualized cost of capital matters for per-trade sizing.

---

## 3. Saturation Assessment

**This is THE most saturated domain on Polymarket for structured quant approaches.** Evidence:

1. **Institutional presence:** CEX market-makers (Jump Trading, Wintermute, GSR) operate quant shops with direct exchange connections, co-located systems, and sub-millisecond data pipelines. Any crypto prediction market with sufficient volume will attract their attention.

2. **The resolution feed is public Binance data.** Every market participant has equal access to the same feed. No competitive advantage from data access.

3. **Spread evidence from [[polymarket-microstructure]]:** SF1 longshot premium (650–900 bps half-spread at tails) is the *residual* after saturation has compressed mid-market spreads. The 5m/15m markets near 50/50 (BTC Up-or-Down 52% Up observed in snapshot) will have the tightest spreads on the platform.

4. **Recurring structure = sustained institutional LP provisioning.** A recurring 5m series that has accumulated $22M lifetime aggregate attracts permanent quant LP presence. This is not a one-off thin market.

5. **Maker rebate structurally lower on crypto:** Per [[polymarket-lp-incentives]], crypto markets carry 20% maker rebate vs. 25% for other categories. LP economics favor other domains.

6. **$22M lifetime aggregate across hundreds of instances → per-instance depth is modest but the *series* is institutionally covered.** Jump/Wintermute/GSR will run the LP book at near-zero spread and extract rebates.

**Saturation conclusion:** 5m/15m/1h/4h directional crypto markets = maximum saturation tier. Equivalent to betting on EUR/USD tick direction against a professional dealer desk.

---

## 4. Edge Sources Evaluated

### 4.1 LLM / Textual Signal
**Per [[llm-forecasting-by-domain]]:** Crypto is LLM-weak with deeply negative CWR despite models maintaining 0.8–0.9 confidence. News augmentation marginally helps Finance/Sports but not Crypto (domain is inherently tick-driven, not text-driven). Zero deployable LLM edge on short-horizon price direction.

### 4.2 Realized-Volatility Forecasting (HAR-RV)
HAR-RV uses lagged RV at daily/weekly/monthly horizons to forecast next-period RV. Applied to 5m prediction markets: forecasts whether the next 5m will be high-vol or low-vol but **cannot forecast direction**. RV forecasting gives range-of-outcomes distribution, not directional signal. Use case: size down during high-vol instances (pick-off risk increases). Available but table-stakes for any institutional operator.

### 4.3 Microstructure / Order Flow (Avellaneda-Stoikov)
Per [[market-maker-handbook-prediction-markets]] (Eqs. 8-9):

```
Reservation: r_x = x − q · γ · σ_b² · (T − t)
Half-spread: 2δ_x ≈ γ σ_b² (T − t) + (2/k) log(1 + γ/k)
```

For a 5m market: `T − t` collapses from ~300s to 0 as the window closes. The VPIN-style toxicity guards ([[market-maker-handbook-prediction-markets]] §4.5) become the critical control — anyone who can observe the last Binance 1m candle before the market closes will pick off any LP without equivalent feed latency. Without sub-second data feed, LP quoting in the final ~60 seconds of each 5m window is net-negative EV.

### 4.4 Pyth Network / On-Chain Feed Arb
**Not applicable.** Confirmed resolution feed is Binance 1m candles, not Pyth, for BTC price markets. Monitoring Pyth vs. Binance spread would only matter if a confirmed Pyth-resolved market exists in this category — unconfirmed in current corpus.

### 4.5 Chainlink Feed Basis
**Not applicable.** Same conclusion as 4.4. Chainlink is not the resolution feed for these markets.

### 4.6 Binance Feed Anomaly Arb
**Potentially viable, extremely narrow.** If Binance BTC/USDT shows a momentary anomalous spike or dip (thin-book print that doesn't appear on Coinbase/Kraken), a prediction market position on that 1m candle High would mis-resolve. Real-time monitoring of Binance vs. cross-venue spread with positioning when anomalous Binance prints occur is a genuine edge but:
- Requires near-co-located Binance data feed
- Anomalous prints are rare; opportunity frequency very low
- Institutional players already monitor this for own book protection

### 4.7 Coinbase Advanced Trade API / Binance WebSocket
Both free and real-time. Binance WebSocket (`wss://stream.binance.com:9443/ws/btcusdt@kline_1m`) delivers exactly the candle data Polymarket uses for resolution. Table-stakes data infrastructure — necessary but no competitive advantage vs. any other operator with basic quant setup.

---

## 5. Monthly Hit Price — Separate Assessment

Monthly Hit Price (e.g., "What price will Bitcoin hit in May?") is structurally distinct from 5m Up-Down:
- **Longer horizon:** 30-day window, resolves at month end
- **Barrier option structure:** Binary barrier resolves Yes if *any* 1m Binance candle High crosses threshold during the month
- **Multiple strikes:** ~11 sub-markets per month (upside + downside)
- **Volume:** $17.1M aggregate (May 2026), $37M (May 2025) — meaningful depth

**Modeling framework:** Binary barrier options. Fair probability of touching level K given spot S_0, drift μ, vol σ, horizon T:

```
P(touch K) ≈ N[(log(K/S) - μT) / (σ√T)] + exp(2μ log(K/S) / σ²) · N[(-log(K/S) - μT) / (σ√T)]
```

**Edge evaluation:**
- Calibrating σ (HAR-RV from Binance history) and μ (risk-neutral drift from CME futures curve) is straightforward
- ATM strikes are institutionally covered; vol calibration is well-known
- **Far-OTM strikes:** Implied vol (backed from barrier option price) may diverge from realized vol skew. A scanner that computes σ_imp from each sub-market price and compares to RV skew forecast would identify mis-priced strikes. Retail-achievable.
- **CME futures hedge:** Partial directional hedge available (not the barrier payoff, but the expected final level). Calendar basis between CME and Binance adds basis risk.

**Saturation:** Near-ATM = institutionally covered. Far-OTM = potentially less saturated. Legitimate niche for small operators with a vol-calibration pipeline.

---

## 6. Pre-Market FDV Subcategory — The Retail Niche

Pre-Market is 115 of 261 crypto markets and is **structurally distinct** from price-tick markets:

**Market examples (2026-05-16 Gamma API):**
- Predict.fun FDV: $5M total vol, 11 sub-markets ($50M–$300M+ FDV thresholds), "most liquid price source" resolution
- Printr public sale: $6.8M total vol, 16 sub-markets (commitment tiers), resolves vs. sale.printr.money
- OpenSea FDV: $6M total vol, 7 sub-markets ($100M–$5B FDV), "most liquid price source" resolution

**Why less saturated than price-tick markets:**
1. Resolution source vagueness ("most liquid price source") creates dispute risk; institutional market-makers price conservatively or avoid entirely
2. FDV outcome depends on total supply (often finalized at TGE), VC lockup structure, launch-day float — non-fungible project-specific information
3. Edge requires domain knowledge of specific token project, not just crypto price feeds
4. Low secondary-market liquidity makes delta-hedging impossible — pure directional exposure, not hedge-able
5. Jump/Wintermute/GSR do not systematically run prediction-market books on FDV markets (their edge is systematic, not project-DD-based)

**Information sources for FDV markets:**
- Pre-launch whitelisted sale price × total supply → implied valuation floor
- VC round valuation (Crunchbase, PitchBook) → comp anchor
- Token unlock schedules (tokenomist.ai) → effective circulating supply at TGE
- Community sentiment (Discord size, Twitter engagement, waitlist oversubscription)
- Comparable launches: Predict.fun $88M FDV → sub-market $50M Yes at 93%, $100M at 88%

**Retail edge hypothesis:** Operator with domain knowledge of a specific token (e.g., active ecosystem participant) has genuine information advantage over generic quant shops. This is closer to VC / early-stage investing edge than market-microstructure edge.

**Risk flag:** Resolution source vagueness is a two-sided risk. "Most liquid price source" is undefined — if the token launches on a thin DEX with a whale-driven spike then dumps, UMA voters determine which price source applies. Genuine dispute-risk exposure unique to Pre-Market markets. Higher UMA dispute probability than for Binance-resolved markets.

---

## 7. Capital Requirements & Sizing

**Short-horizon Up-Down (5m/15m/1h/4h):**
- Per-instance estimated depth: $5k–$50k (from $22M lifetime ÷ hundreds of instances)
- LP capital for meaningful participation: $10k–$100k per series
- UMA challenge-window capital lock: $500 per proposal + position capital locked ~2 hours post-resolution
- Lot-size alpha ceiling: ~$500 (per [[llm-forecasting-by-domain]] PolyBench data for LLM strategies); quant depth constraint applies equally

**Monthly Hit Price:**
- Sub-market depth: $1M–$2M per strike (from $17.1M ÷ 11 sub-markets)
- Meaningful position sizes possible: $10k–$100k per strike without excessive market impact
- More viable for capital deployment than 5m markets

**Pre-Market FDV:**
- $5M–$7M per event; 7–16 sub-markets per event → $300k–$700k per strike
- Reasonable for retail-scale positions ($5k–$50k per sub-market)

---

## 8. Infrastructure Requirements

| Component | Short-Horizon | Monthly Hit Price | Pre-Market FDV |
|---|---|---|---|
| Data feed | Binance WebSocket (free) | Binance historical + HAR-RV | Token project research |
| Latency requirement | Sub-second (pick-off risk) | Minutes acceptable | Days-weeks |
| Modeling | HAR-RV + A-S quoting | Barrier option calibration | Comparables + project DD |
| Hedging | Impossible | Partial via CME futures | None possible |
| Dispute monitoring | Required (2hr UMA window) | Required | Required + higher dispute risk |
| Dev complexity | High (real-time quoting engine) | Medium (batch calibration) | Low (research workflow) |
| Competitive moat | None vs. institutions | Vol-skew scanner (niche) | Domain knowledge |

---

## 9. Risk Factors

1. **Feed concentration risk:** 100% resolution dependency on Binance BTC/USDT creates single-point-of-failure. Binance maintenance windows (~30 min monthly) during an active market window create ambiguous resolution; UMA voters would likely resolve "No" for incomplete candle period, but not codified.

2. **UMA dispute risk (Pre-Market FDV):** "Most liquid price source" is disputable. For tokens launching simultaneously on multiple DEXes, price source choice is not deterministic. Expect opportunistic disputes on large-FDV markets.

3. **Chainlink/Pyth mis-assumption (corrected here):** Prior wiki assumption ([[uma-optimistic-oracle]] open follow-up) that crypto price markets use on-chain feeds is incorrect for BTC/ETH/SOL price-tick markets. Resolution is Binance centralized data. Removes oracle manipulation risk; adds Binance-specific feed risk.

4. **Adverse selection / pick-off:** Final 60 seconds of each 5m window is pick-off territory for any LP without real-time Binance 1m candle feed. Without sub-second latency to Binance, LP quoting in the final window is net-negative EV.

5. **Lower LP rebate:** Crypto market maker rebate is 20% vs. 25% for other categories ([[polymarket-lp-incentives]]). LP economics structurally disadvantaged vs. sports/politics.

6. **No Pyth/Chainlink arb path:** The on-chain oracle arb opportunities that exist in DeFi prediction markets (e.g., Augur, Polymarket v1) do not apply here — the resolution feed is off-chain Binance data.

---

## 10. Verdict

| Sub-domain | Verdict | Reason |
|---|---|---|
| 5m/15m Up-Down (BTC/ETH/SOL) | **Avoid** | Maximum saturation, sub-second latency required, institutional LP presence, no information edge possible on Binance-resolved binary |
| 1h/4h Up-Down | **Avoid** | Same structure, slightly lower latency pressure but same saturation profile |
| Daily Price Range (bracket) | **Marginal** | Bracket Σ-check for MRA per [[arbitrage-taxonomy]] is the only realistic play; directional edge has same saturation problem |
| Monthly Hit Price (near-ATM strikes) | **Avoid** | Institutionally covered, HAR-RV vol forecasting is table-stakes infrastructure |
| Monthly Hit Price (far-OTM strikes) | **Conditional** | If implied vol skew diverges from RV skew, a calibration-pipeline edge exists. Worth building a scanner. Low capital at far-OTM. |
| Pre-Market FDV (token launch) | **Conditional** | Domain knowledge + project DD is the edge. Resolution-source vagueness is a risk. Best opportunity in the crypto category for retail. |

**One-line verdict:** Crypto short-horizon price-tick markets are maximum-saturation quant territory with zero retail LLM edge and near-zero retail quant edge vs. CEX market-makers; the only retail-accessible niches are Pre-Market FDV (token-launch, domain-knowledge-dependent) and far-OTM monthly hit-price strikes where vol-skew mis-pricing may persist.

---

## Sources

- [[snapshots/polymarket-crypto-category-2026-05-13]] — market counts, subcategory taxonomy, volume data, implied spot levels
- [[llm-forecasting-by-domain]] — Crypto LLM-weak; CWR deeply negative; all Weak-tier domains
- [[polymarket-strategy-matrix]] — crypto short-horizon edge assessment; Pre-Market niche flag
- [[market-maker-handbook-prediction-markets]] — A-S quoting framework; VPIN toxicity guards; P&L attribution
- [[uma-optimistic-oracle]] — UMA OO mechanics; $500 bond; Chainlink/Pyth secondary oracle documentation; resolution-feed open question (partially resolved here for BTC price markets)
- Gamma API live pull (2026-05-16): crypto/bitcoin/pre-market tag slugs; BTC monthly hit price resolution rules (Binance BTC/USDT 1m candles confirmed); OpenSea FDV resolution source (vague — "most liquid price source"); Predict.fun FDV and Printr sale market structures

## Related

- [[uma-optimistic-oracle]]
- [[llm-forecasting-by-domain]]
- [[polymarket-strategy-matrix]]
- [[market-maker-handbook-prediction-markets]]
- [[polymarket-microstructure]]
- [[arbitrage-taxonomy]]
- [[polymarket-lp-incentives]]
- [[snapshots/polymarket-crypto-category-2026-05-13]]
