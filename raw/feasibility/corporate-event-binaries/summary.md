---
category: corporate-event-binaries
assessed_on: "2026-05-16"
verdict: NARROW-YES
data_sources:
  - gamma-api: "?tag_slug=finance&active=true&closed=false&limit=30&order=volume24hr&ascending=false"
  - gamma-api: "?slug=spacex-ipo-by"
  - gamma-api: "?slug=anthropic-valued-higher-than-openai-in-2026"
  - gamma-api: "?slug=microstrategy-sell-any-bitcoin-in-2025"
  - raw: "raw/research/polymarket-broad-coverage-sweep/06-polymarket-finance-gamma.md"
  - raw: "raw/research/polymarket-broad-coverage-sweep/.ingest/06-polymarket-finance-gamma.summary.md"
  - wiki: "wiki/polymarket-strategy-matrix.md"
---

# Feasibility Assessment: Corporate Event Binaries (Finance narrow window)

## 1. Category Definition and Scope

**Category:** Corporate event binaries — a subset of the Finance tag (`tag_slug=finance`) covering corporate actions (IPOs, M&A, treasury sales) and private-market valuation comparisons, as opposed to the dominant Finance category types: commodity hit-price ladders, equity hit-price ladders, and macro event outcomes (Fed rate cuts, Treasury yields).

**In-scope markets (3 YES + 1 PARTIAL across 30 Finance events):**

| Slug | Description | Classification |
|---|---|---|
| `spacex-ipo-by` | SpaceX IPO by date (8-leg ladder) | YES |
| `in-which-month-will-spacex-ipo` | SpaceX IPO month picker (NegRisk 12-way) | YES |
| `anthropic-valued-higher-than-openai-in-2026` | Anthropic vs OpenAI valuation flip | YES |
| `microstrategy-sell-any-bitcoin-in-2025` | MicroStrategy sells any BTC (5-leg date ladder) | PARTIAL |

**Out-of-scope (26/30 Finance events):** Commodity hit-price ladders (WTI, Gold, Silver, NG), equity hit-price ladders (SPY, NVDA, TSLA, PLTR, AAPL, ABNB, HOOD), market-cap race NegRisk markets ("Largest Company"), macro date-ladders (Fed cuts, 10Y Treasury), and tail-event markets (bank failure). All quant-saturated; no retail-tractable edge.

---

## 2. Market Inventory and Live Data

### 2a. SpaceX IPO Date-Ladder (`spacex-ipo-by`)

**Capture date:** 2026-05-16

| Sub-market | Yes price | No price | Volume (all-time) |
|---|---|---|---|
| IPO by March 31, 2026 | 0.000 | 1.000 | $508,147 |
| IPO by April 30, 2026 | 0.000 | 1.000 | $627,524 |
| IPO by May 31, 2026 | 0.005 | 0.995 | $615,574 |
| IPO by June 15, 2026 | 0.673 | 0.327 | $141,079 |
| IPO by June 30, 2026 | 0.910 | 0.090 | $291,271 |
| IPO by August 31, 2026 | 0.961 | 0.039 | $59,165 |
| IPO by September 30, 2026 | 0.976 | 0.024 | $132,626 |
| IPO by December 31, 2026 | 0.986 | 0.014 | $130,455 |

- **Event-level volume (all-time):** $2,505,612
- **OI:** $622,885 | **Liquidity:** $206,970
- **24h vol:** $210,339 | **1wk vol:** $392,410
- **Comments:** 45 | NegRisk: False

**Market-implied probability structure:** Legs through April are resolved-NO (0.000). The June 15 / June 30 gap (67.3% to 91.0%) implies ~35% conditional probability on an IPO occurring June 15-30. August and September legs sit within ~5 pp of each other (96.1%/97.6%), implying very thin conditional probability after June.

### 2b. SpaceX IPO Month Picker (`in-which-month-will-spacex-ipo`)

- **Volume (all-time):** $361,295 | **OI:** $29,081 | **Liquidity:** $63,409
- **24h vol:** $21,423

| Month | Yes price | Volume |
|---|---|---|
| Feb 2026 | 0.000 | $2,071 |
| Mar 2026 | 0.000 | $51,009 |
| Apr 2026 | 0.000 | $37,594 |
| May 2026 | 0.003 | $73,211 |
| Jun 2026 | 0.930 | $111,364 |
| Jul 2026 | 0.061 | $19,291 |
| Aug 2026 | 0.005 | $11,181 |
| Sep 2026 | 0.005 | $11,674 |
| No IPO before 2027 | (residual) | — |

**Consistency check vs date-ladder:** June month-picker at 93.0% is consistent with date-ladder June 30 leg at 91.0% (slight upward bias in month-picker likely reflects NegRisk normalization). July at 6.1% is the residual for any post-June timing.

### 2c. Anthropic vs OpenAI Valuation (`anthropic-valued-higher-than-openai-in-2026`)

- **Volume (all-time):** $78,478 | **OI:** $44,459 | **Liquidity:** $18,473
- **24h vol:** $17,295 | **1wk vol:** $29,420
- **Comments:** 15 | NegRisk: False
- **Current price:** Yes = 0.890, No = 0.110
- **Resolution:** "Yes" if at any point Anthropic's most recent valuation (public or private) exceeds OpenAI's most recent valuation by December 31, 2026 ET. Private valuations count if explicitly confirmed by a completed funding round.

**Current state:** Anthropic last valued at ~$61B (post-money, March 2025 Lightspeed round). OpenAI last valued at ~$300B (SoftBank-led round, early 2025). Current Yes price of 89c is strikingly high given a ~5x valuation gap — implies the market believes a large Anthropic round valuing it above $300B is likely before year-end 2026.

### 2d. MicroStrategy Sells Any Bitcoin (`microstrategy-sell-any-bitcoin-in-2025`)

- **Volume (all-time):** $27,252,127 | **OI:** $1,970,800 | **Liquidity:** $218,360
- **24h vol:** $562,238 | **1wk vol:** $12,220,038
- **Comments:** 575 | NegRisk: False

| Sub-market | Yes price | No price | Volume (all-time) |
|---|---|---|---|
| Sells any BTC in 2025 | 0.000 | 1.000 | $17,976,158 |
| Sells by March 31, 2026 | 0.000 | 1.000 | $2,710,380 |
| Sells by May 31, 2026 | 0.595 | 0.405 | $2,687,550 |
| Sells by June 30, 2026 | 0.762 | 0.237 | $2,704,063 |
| Sells by December 31, 2026 | 0.905 | 0.095 | $1,174,944 |

**Market state:** The 2025 and Q1 2026 legs have resolved NO (0.000). May 31 leg at 59.5% is the live near-term bet. June 30 leg at 76.2% has the highest live OI relative to its volume tier. December 2026 leg at 90.5% implies near-certainty of at least one BTC sale before year-end. The $27M all-time volume is the largest of any corporate-event binary in the Finance tag by ~10x, indicating substantial sophisticated participation.

---

## 3. Edge Hypothesis

### 3a. SpaceX IPO — S-1 Monitoring Edge

**Thesis:** SEC EDGAR full-text search reveals S-1 filing status before any public announcement. For an IPO to occur by June 30, SpaceX must file an S-1 with the SEC — typically 2-6 weeks before pricing. An operator monitoring EDGAR for any Space Exploration Technologies Corp. filing gains a 2-6 week heads-up window.

**Signal chain:**
1. EDGAR full-text search (efts.sec.gov) — free, real-time, machine-readable
2. DRS (Drafted Registration Statement, confidential S-1) is not public until 15 days before pricing; the public S-1 filing is the hard signal
3. If no S-1 by mid-June, June 30 leg (currently 91c Yes) should compress toward zero — creating a NO leg opportunity

**Edge type:** Binary — either the S-1 appears (confirming Yes legs) or does not appear (creating large NO edge on near-term legs). Timing of S-1 filing also constrains month-picker pricing.

**Information advantage window:** 2-6 weeks between S-1 public filing and IPO pricing. Market cannot compress to 1.000/0.000 until the IPO actually prices — so the information advantage window is real.

**User domain relevance:** The user has stated interest in space/aerospace domain. Monitoring EDGAR for SpaceX S-1 is a single free data source, automatable.

### 3b. Anthropic vs OpenAI — VC Funding Announcement Edge

**Thesis:** Private valuations are set at funding rounds. The information event is the announcement of a new Anthropic funding round with a stated valuation exceeding OpenAI's last round (~$300B). VC funding round data is semi-public: term sheets are private, but closing announcements appear on Crunchbase, PitchBook, TechCrunch, and company blog posts within days of close.

**Current gap:** Anthropic ~$61B vs OpenAI ~$300B. For Yes to resolve, Anthropic needs a ~5x valuation step in one or more new rounds. The 89c Yes price implies the market believes this is very likely — possibly the market knows something about an imminent large round, or it is systematically miscalibrated.

**Edge type:** Monitoring the announcement network (Crunchbase free tier, TechCrunch, Anthropic blog). If no large round closes, the 89c Yes price is mispriced toward NO at 11c. If a round is announced, the Yes price jumps toward 1.000 — early entry (pre-announcement) captures the spread.

**Information advantage window:** Between a round's close and its public announcement (typically 1-7 days for large AI rounds). More actionable: if no announcement by Q3 2026, the No leg at 11c becomes increasingly mispriced downward.

**Complication:** OI is $44K with $18K liquidity. Maximum bet size is constrained. The market is thin.

### 3c. MicroStrategy BTC Sale — On-Chain Treasury Monitoring Edge

**Thesis:** MicroStrategy's Bitcoin addresses are known and trackable. Any BTC outflow from MSTR treasury addresses is visible on-chain before any SEC filing (8-K or 10-Q). The information window between an on-chain transfer and an SEC disclosure can be hours to days.

**MSTR treasury monitoring:**
- MicroStrategy's known BTC holdings are disclosed in 8-K filings and 10-Q/10-K schedules
- Primary custody addresses are publicly known from MSTR's own disclosures and blockchain analytics (Arkham, Nansen, Glassnode)
- Any outflow from these addresses is an on-chain YES signal hours before SEC disclosure

**Edge type:** On-chain data advantage. A monitor watching MSTR treasury wallets sees a sale before it becomes public corporate disclosure, and before the market moves.

**Complication:** The May 31 leg at 59.5% has $2.7M all-time volume, indicating sophisticated participants (including on-chain analytics firms) are already active. This is the PARTIAL classification — edge exists but is partially captured.

**Remaining opportunity:** The June 30 leg at 76.2% still has live OI ($2.7M all-time). If no sale by May 31 (leg resolves NO), the June 30 leg will reprice — and an on-chain monitor would be ahead of that repricing.

---

## 4. Data Sources

| Source | Cost | Latency | What it provides |
|---|---|---|---|
| SEC EDGAR full-text search (efts.sec.gov) | Free | Real-time | S-1, S-1/A, DRS status for any issuer; automatable via API |
| Crunchbase free tier | Free (limited) | Days | Funding round closings, valuation data; ~5 free lookups/day |
| Crunchbase Pro | ~$49/mo | Same-day | Unlimited lookups; funding alert emails; portfolio monitoring |
| PitchBook | Enterprise paid | Hours | Private valuation data, term sheet signals |
| Arkham Intelligence | Free tier available | Real-time | On-chain wallet labeling including known MSTR addresses |
| Nansen | Paid ($150+/mo) | Real-time | On-chain labeled wallets; smart-money alerts |
| Glassnode | Paid ($29+/mo) | Real-time | On-chain entity clustering; MSTR entity tracking |
| Etherscan / Polygon scan | Free | Real-time | Raw on-chain data; manual monitoring only |
| VC Twitter / announcement networks | Free | Hours | TechCrunch, company blog RSS; announcement wave |

**Minimum viable setup (free tier):**
1. EDGAR EFTS alert for "Space Exploration Technologies" filings — covers SpaceX S-1
2. Crunchbase free tier daily check + TechCrunch RSS — covers Anthropic valuation announcements
3. Etherscan alert on known MSTR treasury addresses — covers MicroStrategy BTC sale (manual or via free Arkham)

**Enhanced setup (~$200/mo):**
- Crunchbase Pro for Anthropic/OpenAI funding alerts
- Arkham or Nansen for MSTR on-chain monitoring with automated alerts

---

## 5. Saturation Assessment

**Finance category overall:** Heavily quant-saturated. 25/30 events are commodity futures ladders, equity price ladders, or macro event markets — all covered by professional quant shops with live CME/exchange feeds. These are explicitly out of scope.

**Corporate event binaries specifically:**

| Market | Quant saturation | Domain-knowledge saturation | Net assessment |
|---|---|---|---|
| SpaceX IPO date-ladder | Low | Low-medium | EXPLOITABLE |
| SpaceX month picker | Low | Low-medium | EXPLOITABLE |
| Anthropic vs OpenAI valuation | Low | Medium | PARTIALLY EXPLOITABLE |
| MicroStrategy BTC sale | Medium-high | Medium | PARTIALLY EXPLOITABLE |

**Rationale for lower saturation:** Equity/crypto quant shops focus on liquid, continuously-priced assets. They have no structural advantage in monitoring SEC EDGAR for specific corporate S-1 filings or in tracking private valuation rounds. MSTR on-chain monitoring is the highest-saturation of the three — blockchain analytics firms are active, and the $27M all-time volume confirms significant professional participation. Still, the information edge for an alert retail operator is moderate rather than zero.

**Key structural insight:** These markets sit in a "domain knowledge gap" — they require corporate-action monitoring workflows that quant shops do not systematically deploy. They are under-covered relative to macro and commodity events.

---

## 6. Market Depth and Sizing Constraints

**Per-event OI and liquidity caps:**

| Market | OI | Liquidity | Max single bet (no significant slippage) |
|---|---|---|---|
| SpaceX IPO by — all legs | $622,885 | $206,970 | ~$10K-$50K per active leg |
| SpaceX month picker | $29,081 | $63,409 | ~$5K-$15K per leg |
| Anthropic vs OpenAI | $44,459 | $18,473 | ~$5K-$10K total market |
| MicroStrategy May 31 leg | est. ~$400K OI | est. ~$50K liquid | ~$20K-$50K |
| MicroStrategy June 30 leg | est. ~$400K OI | est. ~$50K liquid | ~$20K-$50K |

**Key constraint:** These are thin markets. The Anthropic/OpenAI market ($78K all-time volume, $18K liquidity) is the thinnest — a $10K bet moves the market meaningfully. Total deployable capital across all events simultaneously: $60K-$175K at reasonable Kelly sizing.

**Sizing strategy:** These are not volume markets. They are high-EV, low-capacity opportunities. Portfolio value comes from being right on binary events, not from scale.

---

## 7. Time-to-Resolution and Decay

| Market | Resolution deadline | Current price | Weeks remaining |
|---|---|---|---|
| SpaceX IPO by May 31 | 2026-05-31 | 0.005 Yes | 2 — near-zero, effectively closed |
| SpaceX IPO by June 15 | 2026-06-15 | 0.673 Yes | 4 — active |
| SpaceX IPO by June 30 | 2026-06-30 | 0.910 Yes | 6 — active |
| SpaceX IPO by Aug-Dec | 2026-08 to 12-31 | 0.961-0.986 Yes | 11-32 — near-resolved YES |
| SpaceX month picker June | 2026-12-31 | 0.930 Yes | 32 — active |
| Anthropic vs OpenAI | 2026-12-31 | 0.890 Yes | 32 — mid-cycle |
| MicroStrategy May 31 | 2026-05-31 | 0.595 Yes | 2 — most urgent |
| MicroStrategy June 30 | 2026-06-30 | 0.762 Yes | 7 — follow-on |

**Actionable near-term windows:**
1. MicroStrategy May 31 leg (2 weeks): 59.5% Yes. On-chain monitoring is the immediate signal.
2. SpaceX June 15 / June 30 legs (4-6 weeks): 67.3% / 91.0% Yes. EDGAR S-1 monitoring is the signal.
3. Anthropic/OpenAI (full year): 89% Yes. Slow-moving; check quarterly against funding announcements.

---

## 8. Risk Factors

### Resolution ambiguity

- **SpaceX IPO:** Resolution requires "first sale of stock to the public on any recognized stock exchange." A Starlink spin-off IPO would NOT count. Direct listings qualify per the market description.
- **Anthropic/OpenAI valuation:** Resolution counts "private valuation as established in a completed funding round" confirmed "explicitly" by the company. Leaked term sheets, media estimates, and secondary-market prices do NOT count. This is a hard binary on official disclosure.
- **MicroStrategy BTC sale:** "Sells any of its Bitcoin" — even a trivial amount resolves YES. Resolution sources include MSTR corporate announcements AND on-chain data. Favorable for the on-chain monitoring edge — no resolution ambiguity.

### Counterparty / liquidity risk

- Thin markets mean exit before resolution may require accepting significant slippage.
- The Anthropic/OpenAI market has only $18K liquidity — exiting a $10K position pre-resolution could cost 5-10%.

### Information timing risk

- SpaceX S-1 filing and pricing can occur rapidly (standard S-1 review ~30 days from first filing to acceleration). A June 30 IPO would require an S-1 filed by early June — within the remaining 3-week window as of 2026-05-16.
- Anthropic funding rounds can be announced with little warning. The 89c Yes price may already reflect insider awareness of an imminent round.

### Model risk

- The SpaceX June 30 leg at 91c is striking. If the market is pricing off specific insider signals (banker conversations, EDGAR confidential DRS filings not yet public), a retail operator monitoring public EDGAR alone may be systematically late. The S-1 monitoring edge assumes the market is NOT already fully efficient on public information — which the 91c price partially challenges.
- MicroStrategy at $27M all-time volume is the most participated corporate-event binary in the Finance tag. Assume sophisticated on-chain analysts are present.

---

## 9. Verdict Matrix

| Market | Edge type | Edge strength | Capacity | Recommended action |
|---|---|---|---|---|
| SpaceX IPO date-ladder (June legs) | EDGAR S-1 monitoring | MEDIUM | $10K-$50K per leg | Monitor EDGAR; if no S-1 by June 1, consider NO on June 15/30 legs |
| SpaceX month picker (June leg) | Same edge | MEDIUM | $5K-$15K | Complementary to date-ladder; June at 93c is consensus — watch for repricing if no S-1 |
| Anthropic vs OpenAI | VC announcement monitoring | LOW-MEDIUM | $5K-$10K | 89c Yes is suspicious — either smart money or mispriced. Hold small No ($2K-$5K) as hedge; monitor Crunchbase weekly |
| MicroStrategy May 31 | On-chain MSTR monitoring | MEDIUM-HIGH | $20K-$50K | Set up Arkham/Etherscan alert now; most actionable near-term event |
| MicroStrategy June 30 | Same edge | MEDIUM | $20K-$50K | Follow-on from May 31 resolution; reprice window post-May |

**Overall category verdict: NARROW-YES**

Finance is 90% quant-saturated and off-limits. The 3-4 corporate-event binaries identified are genuine domain-knowledge opportunities not covered by quant shops. Total capacity is modest ($60K-$175K across all events). The highest-quality near-term signal is MSTR on-chain monitoring (2 weeks to May 31 resolution); the highest-quality medium-term signal is EDGAR S-1 monitoring for SpaceX (4-6 weeks to June deadlines). The Anthropic/OpenAI market is the lowest-confidence opportunity — thin, slow-moving, and the 89c Yes price is not obviously mispriced without knowing more about Anthropic's current fundraising status.

---

## 10. Implementation Checklist

**Free-tier setup (can be done today):**

- [ ] SEC EDGAR EFTS daily alert for "Space Exploration Technologies" S-1 and S-1/A filings: `https://efts.sec.gov/LATEST/search-index?q=%22Space+Exploration+Technologies%22&forms=S-1,S-1%2FA`
- [ ] Etherscan wallet watcher on known MSTR Bitcoin custody addresses (source: MicroStrategy 10-K treasury disclosure; cross-ref Arkham entity list for "MicroStrategy")
- [ ] Arkham Intelligence free account — set alert on MicroStrategy entity for any BTC outflow
- [ ] TechCrunch RSS + Anthropic blog RSS — keyword alert on "funding", "valuation", "Series"
- [ ] Crunchbase free tier — search Anthropic and OpenAI funding rounds weekly

**Paid-tier enhancements:**

- [ ] Arkham Pro (alerts tier) — automated MSTR treasury outflow notification
- [ ] Crunchbase Pro (~$49/mo) — Anthropic/OpenAI portfolio monitoring with funding alerts
- [ ] Nansen or Glassnode ($29-$150/mo) — MSTR entity tagging with on-chain behavioral analytics

**Monitoring schedule:**

| Signal | Frequency | Source |
|---|---|---|
| EDGAR S-1 for SpaceX | Daily alert | EDGAR EFTS email |
| MSTR BTC wallet outflows | Real-time alert | Arkham/Etherscan |
| Anthropic funding announcements | Weekly | Crunchbase + TechCrunch RSS |
| SpaceX date-ladder leg prices | Weekly (or at EDGAR signal) | Gamma API |
| MicroStrategy legs repricing | After May 31 resolution | Gamma API |

**Entry/exit rules:**

- SpaceX NO position: Enter only if no public EDGAR S-1 by June 1, 2026, on June 15 and June 30 legs. Size <= $10K per leg.
- MicroStrategy: Set Arkham/Etherscan alert immediately. If BTC outflow detected, buy YES. If no outflow by May 25, consider NO on May 31 leg. Size <= $20K.
- Anthropic: Hold small No position ($2K-$5K) as a low-conviction hedge. Monitor Crunchbase weekly for any Anthropic round above $200B valuation.

---

## Source

- `raw/research/polymarket-broad-coverage-sweep/06-polymarket-finance-gamma.md` — Finance category top-30 Gamma API capture, 2026-05-16
- `raw/research/polymarket-broad-coverage-sweep/.ingest/06-polymarket-finance-gamma.summary.md` — Ingest summary with per-event tractability classification
- `wiki/polymarket-strategy-matrix.md` — Strategy matrix context for corporate-event binaries
- Gamma API direct market data for slugs: `spacex-ipo-by`, `anthropic-valued-higher-than-openai-in-2026`, `microstrategy-sell-any-bitcoin-in-2025`

## Related

- [[polymarket-strategy-matrix#corporate-event-binaries--finance-narrow-window]]
- [[llm-forecasting-by-domain]]
- [[polymarket-market-structures]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
- [[arbitrage-taxonomy]]
