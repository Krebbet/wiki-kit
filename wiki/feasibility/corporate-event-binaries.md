# Feasibility — Corporate Event Binaries

Narrow Finance subset: SpaceX IPO date-ladder + month picker, Anthropic-vs-OpenAI valuation flip, MicroStrategy BTC-sale date-ladder. **NARROW-YES verdict** — Finance overall is 90% quant-saturated and off-limits; this 3–4 event subset is genuine domain-knowledge opportunity not covered by quant shops. Total deployable capital $60K–$175K across all events. Live Gamma API 2026-05-16.

## In-scope vs out-of-scope (Finance 30-event sweep)

**In-scope (3 YES + 1 PARTIAL):**

| Slug | Description | Verdict |
|---|---|---|
| `spacex-ipo-by` | SpaceX IPO by date (8-leg ladder) | YES |
| `in-which-month-will-spacex-ipo` | SpaceX IPO month picker (NegRisk 12-way) | YES |
| `anthropic-valued-higher-than-openai-in-2026` | Anthropic vs OpenAI valuation flip | YES |
| `microstrategy-sell-any-bitcoin-in-2025` | MicroStrategy sells any BTC (5-leg date ladder) | PARTIAL |

**Out-of-scope (26/30):** commodity hit-price ladders (WTI, Gold, Silver, NG), equity hit-price ladders (SPY, NVDA, TSLA, PLTR, AAPL, ABNB, HOOD), market-cap race ("Largest Company"), macro date-ladders (Fed cuts, 10Y Treasury), tail markets (bank failure). All quant-saturated.

## Live market state (2026-05-16)

**SpaceX IPO date-ladder (`spacex-ipo-by`, $2.5M all-time, $623K OI):**

| Leg | Yes | Vol_all |
|---|---|---|
| by March 31 | 0.000 | $508K (resolved NO) |
| by April 30 | 0.000 | $628K (resolved NO) |
| by May 31 | 0.005 | $616K |
| by June 15 | 0.673 | $141K |
| by June 30 | 0.910 | $291K |
| by August 31 | 0.961 | $59K |
| by September 30 | 0.976 | $133K |
| by December 31 | 0.986 | $130K |

Conditional P(IPO in June 15–30) = (0.910 − 0.673)/(1 − 0.673) = **72%**.

**SpaceX month picker (`in-which-month-will-spacex-ipo`):** June 93.0% / July 6.1% / Aug 0.5% / Sep 0.5%. Consistent with date-ladder.

**Anthropic vs OpenAI (`anthropic-valued-higher-than-openai-in-2026`, $78K all-time, $44K OI):** Yes = 0.890, No = 0.110. Anthropic last ~$61B (Mar 2025 Lightspeed); OpenAI last ~$300B (SoftBank early 2025). 89c Yes requires ~5× Anthropic step before year-end — strikingly high.

**MicroStrategy BTC sale (`microstrategy-sell-any-bitcoin-in-2025`, $27.25M all-time, $1.97M OI):**

| Leg | Yes |
|---|---|
| in 2025 | 0.000 (resolved NO) |
| by March 31 2026 | 0.000 (resolved NO) |
| by May 31 2026 | 0.595 |
| by June 30 2026 | 0.762 |
| by December 31 2026 | 0.905 |

Most volume of any corporate-event binary in Finance — significant sophisticated participation.

## Edge hypothesis

### SpaceX — SEC EDGAR S-1 monitoring

S-1 typically filed 2–6 weeks before pricing. DRS (confidential) public 15 days pre-pricing. EDGAR full-text search (`efts.sec.gov`) is free, real-time, machine-readable.

**Edge:** Binary — S-1 appears (confirming Yes legs) or doesn't (creating large NO edge on June 15/30 legs as deadline approaches). Information advantage window = 2–6 weeks between public S-1 and IPO pricing.

**Caveat on June 30 at 91c:** Possibly already pricing insider signals (banker conversations, confidential DRS). The S-1-monitoring edge assumes market is not fully efficient on public information — partially challenged by current price level.

### Anthropic vs OpenAI — VC funding announcement monitoring

Information event = announcement of new Anthropic round above OpenAI's $300B last mark. Term sheets private; closing announcements appear on Crunchbase/PitchBook/TechCrunch/Anthropic blog within days.

**Edge:** Monitor announcement network. 89c Yes either implies imminent round insider signal OR market is mispriced. Information advantage window = 1–7 days between round close and announcement. More actionable: if no announcement by Q3 2026, No at 11c becomes increasingly mispriced downward.

**Complication:** $18K liquidity — exiting $10K position pre-resolution costs 5–10%.

### MicroStrategy — On-chain treasury monitoring

MSTR Bitcoin custody addresses are publicly known (10-K disclosures + Arkham/Nansen entity tagging). Any BTC outflow visible on-chain hours-to-days before SEC 8-K/10-Q disclosure.

**Edge:** On-chain data advantage; monitor sees sale before market repricing. $2.7M volume on May 31 leg implies sophisticated on-chain analysts already present (hence PARTIAL not YES).

## Data sources

| Source | Cost | Latency | What it provides |
|---|---|---|---|
| SEC EDGAR full-text (`efts.sec.gov`) | Free | Real-time | S-1, S-1/A, DRS status for any issuer; automatable |
| Crunchbase free tier | Free (5/day) | Days | Funding round closings, valuation data |
| Crunchbase Pro | ~$49/mo | Same-day | Unlimited lookups; alerts |
| PitchBook | Enterprise | Hours | Private valuation + term sheet signals |
| Arkham Intelligence | Free tier | Real-time | On-chain wallet labeling (MSTR addresses) |
| Nansen | $150+/mo | Real-time | Smart-money alerts |
| Glassnode | $29+/mo | Real-time | Entity clustering; MSTR tracking |
| Etherscan / Polygonscan | Free | Real-time | Raw on-chain; manual monitoring |
| TechCrunch / Anthropic blog RSS | Free | Hours | Announcement wave |

**Minimum viable (free tier):**
1. EDGAR EFTS alert for "Space Exploration Technologies" S-1/S-1-A filings.
2. Etherscan wallet watcher on known MSTR Bitcoin custody addresses (cross-ref Arkham entity).
3. Arkham Intelligence free account — alert on MicroStrategy entity for BTC outflow.
4. TechCrunch + Anthropic blog RSS — keyword alert on "funding"/"valuation"/"Series".
5. Crunchbase free tier — weekly Anthropic + OpenAI funding search.

**Enhanced (~$200/mo):** Arkham Pro alerts; Crunchbase Pro alerts; Nansen or Glassnode for MSTR entity behavior.

## Saturation

| Market | Quant saturation | Domain saturation | Net |
|---|---|---|---|
| SpaceX IPO date-ladder | Low | Low-med | EXPLOITABLE |
| SpaceX month picker | Low | Low-med | EXPLOITABLE |
| Anthropic vs OpenAI | Low | Medium | PARTIALLY EXPLOITABLE |
| MicroStrategy BTC sale | Med-high | Medium | PARTIALLY EXPLOITABLE |

**Why lower saturation:** Equity/crypto quant shops focus on liquid continuously-priced assets. They have no structural advantage in monitoring SEC EDGAR for specific corporate S-1 filings or tracking private valuation rounds. MSTR on-chain is highest-saturation (blockchain analytics firms active; $27M volume confirms professional participation). Still moderate edge for alert retail operator.

**Structural insight:** These markets sit in a "domain knowledge gap" — corporate-action monitoring workflows quant shops don't systematically deploy. Under-covered relative to macro and commodity events.

## Sizing

| Market | OI | Liq | Max bet |
|---|---|---|---|
| SpaceX IPO ladder (all legs) | $623K | $207K | $10K–$50K/active leg |
| SpaceX month picker | $29K | $63K | $5K–$15K/leg |
| Anthropic vs OpenAI | $44K | $18K | $5K–$10K (thinnest) |
| MSTR May 31 leg | ~$400K | ~$50K | $20K–$50K |
| MSTR June 30 leg | ~$400K | ~$50K | $20K–$50K |

Total deployable across all events simultaneously: **$60K–$175K at reasonable Kelly sizing**. High-EV / low-capacity profile.

## Time-to-resolution

| Market | Deadline | Weeks remaining | Status |
|---|---|---|---|
| MicroStrategy May 31 | 2026-05-31 | **2** | Most urgent |
| SpaceX IPO by June 15/30 | 2026-06-15 / 30 | **4–6** | EDGAR window |
| MicroStrategy June 30 | 2026-06-30 | 7 | Follow-on post-May |
| Anthropic vs OpenAI | 2026-12-31 | 32 | Slow-moving |
| SpaceX IPO by Aug-Dec | 2026-08 to 12-31 | 11–32 | Near-resolved YES |

## Risks

### Resolution ambiguity

- **SpaceX IPO:** Requires first sale of stock to public on recognized exchange. Starlink spin-off does NOT count. Direct listings qualify.
- **Anthropic/OpenAI:** Private valuation must be "established in a completed funding round" with explicit company confirmation. Leaked term sheets, media estimates, secondary-market do NOT count.
- **MSTR BTC sale:** "Sells any of its Bitcoin" — even trivial amount resolves YES. MSTR announcements OR on-chain data both count. Favorable for monitoring edge — no resolution ambiguity.

### Counterparty / liquidity

- Thin markets → exit pre-resolution costs slippage. Anthropic/OpenAI $18K liq is most binding.

### Information timing

- SpaceX S-1 → pricing can be ~30 days. June 30 IPO would need S-1 by early June — within 3-week window from 2026-05-16.
- Anthropic rounds announceable with little warning. 89c may reflect insider awareness.

### Model risk

- 91c on SpaceX June 30 may reflect insider information not public. Operator monitoring public EDGAR alone may be systematically late.

## Decision-tree mapping

1. **Q1 YES-theme?** YES — corporate-action timing is a domain-knowledge edge type per [[polymarket-strategy-matrix]].
2. **Q2 Data source?** YES — EDGAR (free + real-time); Arkham/Etherscan (free + real-time); Crunchbase/TechCrunch (free + days lag).
3. **Q3 Structural-arb?** Date-ladder monotonicity (SpaceX, MSTR); P(by T1) ≤ P(by T2). NegRisk month-picker Σ-check across SpaceX 12-way.
4. **Q4 Microstructure?** Thin markets; limit orders for entry; 5% taker fee on Finance category.

## Entry/exit rules

- **SpaceX NO position:** Enter only if no public EDGAR S-1 by June 1, 2026, on June 15 + June 30 legs. Size ≤$10K/leg.
- **MicroStrategy:** Set Arkham/Etherscan alert now. BTC outflow detected → buy YES. No outflow by May 25 → consider NO on May 31 leg. Size ≤$20K.
- **Anthropic:** Hold small No ($2K–$5K) as low-conviction hedge. Monitor Crunchbase weekly for Anthropic rounds above $200B valuation.

## Open follow-ups

1. EDGAR EFTS daily alert configured for "Space Exploration Technologies" filings.
2. Etherscan + Arkham wallet watcher on MSTR known custody addresses (source: 10-K treasury disclosure).
3. SpaceX June 30 leg at 91c — reconcile with public EDGAR status; if no S-1 by June 1, take NO position size ≤$10K.
4. Crunchbase Pro decision: $49/mo for alerts vs free-tier weekly check.
5. Backtest Anthropic 11c No position vs realized announcement cadence for AI labs.

## Source

- `raw/feasibility/corporate-event-binaries/summary.md` (2026-05-16)
- `raw/research/polymarket-broad-coverage-sweep/06-polymarket-finance-gamma.md`
- Gamma API direct queries: `spacex-ipo-by`, `anthropic-valued-higher-than-openai-in-2026`, `microstrategy-sell-any-bitcoin-in-2025`

## Related

- [[polymarket-strategy-matrix]]
- [[llm-forecasting-by-domain]]
- [[polymarket-market-structures]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
- [[arbitrage-taxonomy]]
- [[feasibility-review]]
