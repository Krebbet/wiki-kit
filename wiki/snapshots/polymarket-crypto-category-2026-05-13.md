# Polymarket Crypto Category — Snapshot 2026-05-13

Point-in-time snapshot of `polymarket.com/crypto`, captured 2026-05-13. **261 active Crypto markets** with the top ~21 enumerated below. Bitcoin dominates by sub-bucket count (33 markets); Pre-Market is the single largest subcategory (115 of 261). Implied spot prices at capture: **BTC ~$81k, ETH ~$2,300, SOL ~$95, XRP ~$1.45**. Source: `raw/research/polymarket-market-content-and-sizing/04-polymarket-crypto-category.md`.

## Subcategory taxonomy

(Counts visible at capture. Subcategory totals sum to >261 because markets appear in multiple buckets — e.g., a Bitcoin Weekly market appears in both "Bitcoin" and "Weekly".)

| Subcategory | Count |
|---|---|
| All | 261 |
| **Pre-Market** | **115** |
| Weekly | 60 |
| Bitcoin | 33 |
| Monthly | 22 |
| Yearly | 22 |
| Ethereum | 21 |
| Solana | 13 |
| Daily | 11 |
| XRP | 11 |
| 1 Hour | 9 |
| MicroStrategy | 8 |
| 5 Min | 7 |
| 15 Min | 7 |
| 4 Hours | 7 |
| BNB | 6 |
| Dogecoin | 6 |
| ETF | 2 |

The time-horizon dimension (5m / 15m / 1h / 4h / Daily / Weekly / Monthly / Yearly) and the coin-bucket dimension are orthogonal; Pre-Market is its own structural category (token-launch / FDV / token-sale markets that resolve at a launch event rather than a recurring price tick).

## Price / directional markets (Live, top 17)

| # | Title | Type | Subcategory | Leading Outcome | Vol / notes |
|---|---|---|---|---|---|
| 1 | BTC Up or Down 5m | Up/Down | Bitcoin / 5 Min | 52% Up | $22M (series lifetime aggregate — not single instance) |
| 2 | Bitcoin above ___ on May 13? | Above/Below | Bitcoin / Daily | 72k: 100% Yes; 74k: 100% Yes | Resolved near-certainty |
| 3 | What price will Bitcoin hit in May? | Hit Price / Monthly | Bitcoin | ↑85k: 53% Yes; ↓75k: 39% Yes | Live |
| 4 | Ethereum above ___ on May 13? | Above/Below | Ethereum / Daily | 1,900: 100%; 2,000: 100% | Resolved near-certainty |
| 5 | Bitcoin price on May 13? | Price Range | Bitcoin / Daily | 80k-82k: 86% Yes; 78k-80k: 10% | Live |
| 6 | BTC Up or Down Daily | Up/Down | Bitcoin / Daily | 79% Up | Live |
| 7 | XRP price on May 13? | Price Range | XRP / Daily | 1.40-1.50: 97% Yes; 1.50-1.60: 4% | Live |
| 8 | What price will Bitcoin hit May 11-17? | Hit Price / Weekly | Bitcoin | ↓78k: 32%; ↑84k: 29% | Live |
| 9 | What price will Ethereum hit in May? | Hit Price / Monthly | Ethereum | ↓2,200: 63%; ↑2,600: 25% | Live |
| 10 | What price will Solana hit in May? | Hit Price / Monthly | Solana | ↑100: 66%; ↑110: 25% | Live |
| 11 | Ethereum price on May 13? | Price Range | Ethereum / Daily | 2,300-2,400: 67%; 2,200-2,300: 33% | Live |
| 12 | What price will Bitcoin hit on May 13? | Hit Price / Daily | Bitcoin | ↓81k: 100%; ↓80k: 44% | Live |
| 13 | What price will XRP hit in May? | Hit Price / Monthly | XRP | ↑1.60: 43%; ↓1.20: 14% | Live |
| 14 | What price will Ethereum hit May 11-17? | Hit Price / Weekly | Ethereum | ↑2,400: 40%; ↓2,200: 31% | Live |
| 15 | Solana price on May 13? | Price Range | Solana / Daily | 90-100: 98%; 100-110: 2% | Live |
| 16 | What price will XRP hit May 11-17? | Hit Price / Weekly | XRP | ↑1.50: 60%; ↑1.60: 11% | Live |
| 17 | What price will Dogecoin hit in May? | Hit Price / Monthly | Dogecoin | ↓0.10: 56%; ↑0.15: 11% | Live |

## Event / regulatory / token-launch markets

| # | Title | Type | Vol | Odds |
|---|---|---|---|---|
| 18 | Clarity Act signed into law in 2026? | Regulatory | $754K | 63% Yes |
| 19 | Opensea FDV above ___ one day after launch? | Token launch | $6M | $100M-tranche: 72% Yes |
| 20 | Predict.fun FDV above ___ one day after launch? | Token launch | $5M | $50M: 93%; $100M: 88% |
| 21 | Printr public sale total commitments? | Token sale | $7M | >$6M: 3%; >$3M: 3% |

These four event markets together represent ~$19M visible vol; structurally distinct from the directional / price-level flow above (different resolution path: FDV at TGE, sale tally close, legislative signing — not a price-feed timestamp).

## Implied spot levels at capture (read from price markets)

- **BTC: ~$81k** (above 72k and 74k at 100%; price-range 80k-82k at 86%)
- **ETH: ~$2,300** (above 1,900 and 2,000 at 100%; price-range 2,300-2,400 at 67%)
- **SOL: ~$95** (price-range 90-100 at 98%)
- **XRP: ~$1.45** (price-range 1.40-1.50 at 97%)

## Operating-regime observations

- **Pre-Market is the largest subcategory by count (115/261).** This is the operationally distinct vertical — token-launch FDV, token-sale total commitments, regulatory approvals. None of these are price-tick markets; they all resolve at a discrete event with potentially heavy information-asymmetry exposure (insiders vs retail on a token launch).
- **The high-frequency (5m / 15m / 1h / 4h) buckets together hold only 30 markets** but the BTC 5m series alone has $22M lifetime aggregate volume — pure microstructure flow, recurring every 5 minutes. Per-instance volume is much smaller; the headline aggregate is series-level.
- **Crypto is LLM-weak per [[llm-forecasting-by-domain]].** PolyBench reports models maintain confidence 0.8–0.9 on Crypto domain despite "deeply negative" CWR. Operational map: the 21 markets enumerated here are the candidates where **human/quant edge** (not LLM-text edge) would be the more promising approach. The 5m/15m/1h Up-or-Down markets in particular are pure technical-feed strategies — no semantic edge applies.
- **Resolution source ambiguity.** The FAQ on the landing page references "official government, regulatory, or primary-source reporting" for Elections/Economy/Geopolitics but does **not** name the price feed used for crypto price markets. Individual market pages required to confirm. Open follow-up — the kit-level `tools/capture_polymarket_market.py` per `master_notes.md` 2026-05-12 would address this.

## Cross-references

- [[polymarket-bet-content-trends]] — the synthesis page; this snapshot is its crypto-vertical anchor.
- [[llm-forecasting-by-domain]] — Crypto domain LLM-weak; this snapshot enumerates the specific markets.
- [[polymarket-market-taxonomy]] — adds the time-horizon subcategory dimension (5m–Yearly) not previously documented.
- [[snapshots/polymarket-top-markets-2026-05-13]] — cross-market snapshot from the same capture date.

## Source

- `raw/research/polymarket-market-content-and-sizing/04-polymarket-crypto-category.md` — Polymarket primary page `polymarket.com/crypto`, captured 2026-05-13. 21 of 261 markets visible on landing (others behind "Show more markets" UI control). Subcategory taxonomy is exhaustive.
