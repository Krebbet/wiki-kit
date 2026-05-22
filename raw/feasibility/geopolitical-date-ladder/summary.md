# Feasibility Assessment: Geopolitical Date-Ladder Markets (Iran Cluster + Ukraine/Israel/China-Taiwan)

**Produced:** 2026-05-16  
**Scope:** Iran vertical (US-Iran peace, Strait of Hormuz, regime fall, airspace, blockade, uranium); comparable Ukraine / Israel / China-Taiwan structures  
**Data sources:** Gamma API live pull 2026-05-16; wiki snapshots 2026-05-13; [[llm-forecasting-by-domain]]; [[polymarket-strategy-matrix]]; [[uma-optimistic-oracle]]

---

## 1. Market Universe and Current Prices

### Iran Cluster — live legs (2026-05-16)

| Event | Leg | Yes Price | Volume (leg) | Event Total Vol | Liquidity |
|---|---|---|---|---|---|
| **US x Iran permanent peace deal** | May 31 | **0.105** | $24.1M | $116.8M | $2.25M |
| | Jun 30 | **0.305** | $9.4M | | |
| | Jun 15 | **0.185** | $15.7K | | |
| | Jul 31 | **0.385** | $1.3K | | |
| | Dec 31 | **0.665** | $1.8M | | |
| **Kharg Island — not Iranian control** | May 31 | **0.041** | $6.7M | $42.9M | $522K |
| | Jun 30 | **0.085** | $2.6M | | |
| **Iranian regime fall** | May 31 | **0.011** | $20.4M | $40.1M | $886K |
| | Jun 30 | **0.045** | $40.1M | | |
| **Blockade lifted (Trump announces)** | May 22 | **0.090** | $1.2M | ~$18M | — |
| | May 31 | **0.200** | $3.2M | | |
| | Jun 30 | **0.490** | $585K | | |
| **Strait of Hormuz — traffic normal** | May 15 | **0.001** | $17.4M | ~$38M | $2.0M |
| | end-May | **0.039** | $14.1M | | $517K |
| | end-Jun | **0.285** | $6.1M | | $563K |
| **US obtains Iranian enriched uranium** | May 31 | **0.065** | $12.5M | ~$13.5M | — |
| | Jun 30 | **0.115** | $247K | | |
| | Dec 31 | **0.265** | $573K | | |
| **Iran closes its airspace** | May 31 | **0.390** (snapshot) | — | $13M | — |
| | Jun 30 | **0.470** (snapshot) | — | | |

_Iran airspace prices from 2026-05-13 snapshot; live API slug resolution returned empty — direct market page capture needed to confirm current prices._

### Comparable verticals — indicative

| Event | Price | Volume | Notes |
|---|---|---|---|
| China invades Taiwan by Dec 31 | ~7% Yes | $23M | Single-leg, snapshot |
| Russia-Ukraine ceasefire by Oct 31 | ~29% Yes | $179K | Thinly traded, NEW at snapshot |
| Russia-Ukraine ceasefire by Dec 31 | ~46% Yes | $179K | Same event group |
| Will US invade Iran before 2027? | ~32% Yes | $28.6M | Single-leg Dec 31 |
| Iran regime fall by May 31 | 1.05% Yes | $20.4M | Separate from Jun 30 leg |

---

## 2. Term-Structure (Monotonicity) Analysis

Structural constraint: for any date-ladder event, `P(by T1) <= P(by T2)` for `T1 < T2`. Violations are Market Rebalancing Arbitrage (MRA) candidates per [[arbitrage-taxonomy]] Def. 3. Conditional incremental probability for the (T1, T2] window uses the Saguillo formula: `P(event in (T1,T2] | not by T1) = (P2 - P1) / (1 - P1)`.

### Live monotonicity — no violation detected as of 2026-05-16

| Event | T1 | P1 | T2 | P2 | P(window) = (P2-P1)/(1-P1) | Slack (pp) |
|---|---|---|---|---|---|---|
| **US-Iran peace deal** | May 31 | 10.5% | Jun 30 | 30.5% | (0.305-0.105)/(1-0.105) = **22.3%** | 20.0 pp |
| | Jun 30 | 30.5% | Dec 31 | 66.5% | (0.665-0.305)/(1-0.305) = **51.8%** | 36.0 pp |
| **Blockade lifted** | May 22 | 9.0% | May 31 | 20.0% | (0.200-0.090)/(1-0.090) = **12.1%** | 11.0 pp |
| | May 31 | 20.0% | Jun 30 | 49.0% | (0.490-0.200)/(1-0.200) = **36.3%** | 29.0 pp |
| **Hormuz traffic normal** | end-May | 3.9% | end-Jun | 28.5% | (0.285-0.039)/(1-0.039) = **25.6%** | 24.6 pp |
| **Uranium seized** | May 31 | 6.5% | Jun 30 | 11.5% | (0.115-0.065)/(1-0.065) = **5.3%** | 5.0 pp |
| | Jun 30 | 11.5% | Dec 31 | 26.5% | (0.265-0.115)/(1-0.115) = **16.9%** | 15.0 pp |
| **Kharg Island** | May 31 | 4.1% | Jun 30 | 8.5% | (0.085-0.041)/(1-0.041) = **4.6%** | 4.4 pp |
| **Regime fall** | May 31 | 1.1% | Jun 30 | 4.5% | (0.045-0.011)/(1-0.011) = **3.4%** | 3.4 pp |
| **Iran airspace** (snapshot) | May 31 | 39.0% | Jun 30 | 47.0% | (0.47-0.39)/(1-0.39) = **13.1%** | **8.0 pp** <- tightest |

**Watchlist priority:** Iran airspace ladder remains the tightest cross-leg spread at 8 pp slack. The uranium ladder (May-Jun) is similarly compressed at 5 pp. Any single news event pushing the near leg upward by ~4-5 pp could induce an inversion. Monitor both daily.

**Notable shift vs 2026-05-13 snapshot:** Peace deal Jun 30 dropped from 34% to 30.5%, Dec 31 rose from 63% to 66.5%. Blockade-lifted Jun 30 fell from ~51% to 49%; May 31 fell from ~23% to 20%.

---

## 3. LLM Forecasting Edge Assessment

**Domain tier: STRONG.** Per [[llm-forecasting-by-domain]]:
- GPT-5 Brier 0.14 on Geopolitics (best across domains); ECE 0.09
- GPT-4.1 88% accuracy on Geopolitics
- PolyBench (arXiv 2604.14199): Politics positive-CWR for all 3 charted models

**News augmentation:** Marginal noise for Geopolitics — Claude-3.7 84%->80% with news context; GPT-5 holds at 84%. Recipe: LLM base-model reasoning primary; news context optional with strict cutoff enforcement to avoid temporal leakage.

**Strongest signal type:** `news_catalyst` tag achieves CWR 50.0% in PolyBench Table 6 — breaking-news shifts not yet absorbed by the market. Iran events (ceasefire talks, nuclear negotiation rounds, diplomatic meeting announcements) fit precisely.

**Scalability constraint:** LLM alpha decays at ~$500 lot size due to CLOB depth exhaustion. Iran markets carry $166K-$2.25M in liquidity — depth sufficient for small positions but alpha degrades logarithmically beyond $500.

**Failure modes relevant to geopolitics:**
- **Rumour overweighting:** Unverified wire reports on Iran deal progress can shift LLM posteriors as if confirmed. Wire journalism on Iran talks is often speculative.
- **Definition drift:** LLM may interpret "permanent peace deal" through colloquial lens vs contract-specific resolution criteria. Resolution source must be pinned before generating signal.

---

## 4. Data Sources and Signal Pipeline

### Recommended sources (tiered by quality and access)

| Source | Type | Cost | Signal quality | Notes |
|---|---|---|---|---|
| **Reuters / Bloomberg wire feeds** | Real-time news | Paid ($$$) | High — breaking diplomatic developments | Primary for `news_catalyst` signal; temporal-leakage risk if used uncritically |
| **AP API** | Wire news | Paid ($) | High — authoritative official reports | Best for official statement verification |
| **GDELT Project** | Structured news events | Free | Medium — event extraction with lag | 100+ languages; Iran CAMEO codes 010-030 for peace/conflict; 15-min update cadence |
| **IMF Portwatch** | Shipping transit data | Free | Definitive for Hormuz markets | **Also the resolution oracle** for traffic-normal markets (7-day MA >= 60 threshold) |
| **Maxar / Planet Labs** | Satellite imagery | Paid ($$$) | High for Kharg Island, military posture | Visible-change-of-control evidence for Kharg Island market |
| **OpenStreetMap conflict overlays** | Geospatial | Free | Low-latency qualitative | Crowd-updated; less reliable for classified/recent military positions |
| **Twitter/X OSINT lists** | Social OSINT | Free (curated) | Medium — early signal, noisy | @IranIntl_En, @WarMonitor3, @Intel_Sky; precedes wire 10-60 min on Iran; high false-positive rate |
| **IAEA reports** | Nuclear inspections | Free | High for uranium markets | Authoritative on enrichment levels; quarterly cadence (too slow for near-term legs) |
| **ISW / CSIS / RAND** | Think-tank analysis | Free | High for calibration baseline | Use as prior calibration anchors; not market-probability-ready without translation |

**Pipeline architecture:** GDELT CAMEO event filter (Iran codes) -> LLM probability update (no raw news injection) -> Portwatch pull for Hormuz legs -> confidence-weighted Kelly with calibration correction per [[llm-epistemic-calibration]].

---

## 5. Predictive Edge — Fundamentals by Market

### US-Iran peace deal ($116.8M event)

Term structure: May 31 = 10.5%, Jun 30 = 30.5%, Dec 31 = 66.5%. Implied conditional: 22.3% for the Jun-only window; 51.8% for H2 conditional on not by Jun 30.

**Base-rate anchor:** No US-Iran formal peace agreement since 1979. Dec 31 at 66.5% implies more-likely-than-not resolution this calendar year — substantially above any historical precedent. LLM forecasters anchored to base rates would shade 30-45% for Dec 31, suggesting a short-Dec 31 relative value trade if confirmed via calibration.

**Resolution criteria risk (HIGH):** "Permanent peace deal" must be defined in per-market criteria. JCPOA 2.0 vs formal treaty vs executive agreement has 2-3x probability difference. UMA dispute risk elevated if agreement signed but crowd disagrees on qualification — analogous to FIDE chess case per [[uma-optimistic-oracle]].

### Iranian regime fall ($40.1M Jun 30, $20.4M May 31)

May 31 = 1.1%, Jun 30 = 4.5%. Resolution criteria (from Gamma API): requires dissolution of Supreme Leader's office, Guardian Council, and IRGC clerical control — a very high bar. Daily hazard ~0.15% consistent with market. LLM news-catalyst signals (protests, military defections) are the primary movers. Market is well-calibrated on the definitional bar.

### Strait of Hormuz — traffic normal

End-May = 3.9%, End-Jun = 28.5%. IMF Portwatch is both signal source and resolution oracle — the trader can monitor the resolution criterion in real time. A rising 7-day MA approaching 60 in the final 7-10 days converts the binary to near-certain; exploitable in the final week before resolution.

### Blockade lifted

May 31 = 20.0%, Jun 30 = 49.0%. Discrete presidential announcement event — news catalyst dominates. Jun 30 near-coin-flip with high liquidity. Resolution criteria risk: tweet vs formal statement ambiguity needs per-market verification.

### Uranium obtained

May 31 = 6.5%, Jun 30 = 11.5%, Dec 31 = 26.5%. May-Jun conditional only 5.3% — tight. Most explicit resolution definition ("officially announces or confirms possession"). IAEA verification is the external anchor. News catalyst from nuclear negotiation outcome is primary driver.

---

## 6. Structural Arbitrage Opportunities

### Airspace ladder — primary watchlist

Iran airspace: May 31 = 39%, Jun 30 = 47% (2026-05-13). Slack = 8 pp. A 4-5 pp adverse move on the near leg could induce P(May 31) > P(Jun 30), a hard monotonicity violation and mechanical long-MRA per [[arbitrage-taxonomy]] Def. 3. Action: monitor near leg daily; position for inversion arb if slack closes to <=2 pp.

### Uranium ladder — secondary watchlist

May 31 = 6.5%, Jun 30 = 11.5%. Slack = 5 pp. A single IAEA or State Dept announcement could close this gap.

### Peace deal — Dec 31 short

Dec 31 at 66.5% vs estimated calibrated LLM prior of ~35-45% based on historical base rates. If confirmed via calibration sweep, short Dec 31 / long Jun 30 (as hedge) is the relative value trade. Caveat: resolution risk makes this a two-sided bet (the short could win for the wrong reason if UMA resolves ambiguously).

### Hormuz near-real-time oracle

If Portwatch 7-day MA rises above ~55 by May 25, the May 31 leg at 3.9% becomes a long before market reprices — a days-to-close window trade.

---

## 7. Competitor / Saturation Analysis

**Think tanks (CSIS, RAND, ISW, Eurasia Group, Stratfor):** Publish qualitative Iran probability assessments. These inform sophisticated traders. However, think-tank outputs are qualitative ranges ("medium risk"), not calibrated prediction-market probabilities. The translation layer is lossy and inconsistent across analysts. LLM-driven systematic calibration has an edge in *consistency*, not in raw information access.

**Probability-translation gap:** The most differentiated available edge. Think tanks do not publish date-ladder conditional probabilities or Saguillo-style term-structure decompositions. This layer is unoccupied.

**OSINT community:** Active on Twitter/X; often ahead of wire by 10-60 minutes on Iran developments. The `news_catalyst` window is shrinking as OSINT-to-market pipelines mature among sophisticated players.

**Depth constraint:** $500 per-trade alpha ceiling (CLOB depth exhaustion) limits absolute P&L regardless of edge quality. This is not a full-time-trading market; it is a supplementary strategy.

---

## 8. Resolution Risk Assessment

### Per-market UMA dispute exposure

| Market | Resolution source | Dispute risk | Key ambiguity |
|---|---|---|---|
| US-Iran peace deal | Credible reporting consensus | **HIGH** | What constitutes "permanent"? Treaty vs executive agreement? |
| Regime fall | Credible reporting + broad consensus | **HIGH** | "Dissolved/incapacitated/replaced" bar is high but subjective for partial collapses |
| Blockade lifted | Trump official announcement | **MEDIUM** | Tweet vs formal statement; "announced" vs "implemented" |
| Hormuz traffic normal | IMF Portwatch (objective threshold) | **LOW** | Objective 7-day MA >= 60; Portwatch is authoritative and transparent |
| Uranium obtained | Official US government announcement | **MEDIUM** | "Officially confirms" — reported but not formally confirmed scenario |
| Airspace closed | Credible reporting | **HIGH** | Partial vs full closure? Military vs civilian airspace? |
| Kharg Island control | Credible reporting consensus | **HIGH** | Transient vs permanent seizure? |

**FIDE analogy per [[uma-optimistic-oracle]]:** Chess championship case (both players declared winners of different sections; UMA forced to pick one) is directly analogous to an Iran-deal market where parties sign a document but disputants disagree it meets "permanent peace" bar. UMA DVM vote becomes arbiter; vote outcomes are not predictable from market fundamentals alone.

**Bond economics:** $500 proposer bond / $750 disputer bond; winning side net gain ~$250. Disputed resolution delays 4-6 days and may temporarily pin market at 50-50.

**Mitigation:** Check per-market resolution criteria before entering. Portwatch-keyed markets (Hormuz traffic) carry materially lower resolution risk than consensus-based ones.

---

## 9. Ukraine / Israel / China-Taiwan Comparables

### China-Taiwan

Single leg: Dec 31, ~7% Yes, $23M. Not a date-ladder — no cross-leg monotonicity to exploit. LLM edge present (Geopolitics-strong). Saturated at $23M volume. Recommendation: predictive-edge only, no structural arb.

### Ukraine-Russia ceasefire

Oct 31 ~29%, Dec 31 ~46%, only $179K volume (NEW tag). Conditional for Oct-Dec window: (0.46-0.29)/(1-0.29) = **24.0%** — meaningful but thinly traded (spread dominates). Volume anomaly: Ukraine has 106 markets but no high-volume anchor; ceasefire at $179K is dramatically under-trafficked vs Iran ($116M). Either sophisticated traders have left (negative signal) or market is undertracked (opportunity). Needs fresh volume check.

### Israel cluster

Israel-Lebanon withdrawal (Jun 30 = 10%, May 31 = 1%), Israel-Indonesia normalization (Dec 31 = 14%, Jun 30 = 5%). Low volume ($476K-$1M). Date-ladder structure present but thin. Jun-only conditional for Lebanon withdrawal: (0.10-0.01)/(1-0.01) = **9.1%**. Slack is wide (9 pp) — low priority for arb monitoring vs Iran.

### Cross-cluster ranking

Iran dominates geopolitics volume concentration by ~10:1 over Ukraine + Israel + China-Taiwan combined. Iran is the correct primary cluster for date-ladder strategy. Comparable verticals are either single-leg, thinly traded, or far from inversion risk.

---

## 10. Verdict and Deployment Recommendation

**Feasibility: YES, with conditions.**

**Deploy in two modes:**

**1. Structural monitoring (daily):** Run monotonicity sigma-check across Iran cluster legs daily. Priority watchlist: airspace (8 pp slack) and uranium (5 pp slack). Position for inversion arb if slack closes to <=2 pp. Pull Portwatch 7-day MA daily for Hormuz traffic legs — near-real-time oracle signal with days-of-advance notice before resolution.

**2. News catalyst (event-driven):** LLM probability update on breaking developments (negotiation rounds, IAEA announcements, military movements). Compare to current market prices; if delta >5 pp, enter position. `news_catalyst` CWR = 50.0% (PolyBench Table 6) is the benchmark. Size <=\$500 per trade to stay within CLOB alpha ceiling.

**Avoid / caution:**
- Dec 31 peace deal leg at 66.5%: likely above calibrated LLM estimate; short opportunity but UMA resolution risk is very high.
- All consensus-based ambiguous markets (peace deal, airspace, Kharg Island): check per-market resolution criteria before entry.
- Ukraine ceasefire at $179K volume: too thin for structural arb execution.

---

**One-line verdict:** Iran date-ladder cluster is the strongest structural geopolitics opportunity on Polymarket — LLM-strong domain, multi-leg monotonicity arb watchlist (airspace 8 pp, uranium 5 pp), IMF Portwatch real-time oracle signal for Hormuz legs, and news-catalyst CWR edge — partially offset by elevated UMA resolution risk on consensus-based markets and an ~\$500 CLOB alpha ceiling per trade.

---

## Source

- Gamma API live pull 2026-05-16: events endpoint, iran tag, individual event slugs (peace deal, blockade, uranium, Hormuz, regime fall)
- `wiki/snapshots/polymarket-geopolitics-category-2026-05-13.md` — 2026-05-13 Iran category snapshot; airspace prices 39%/47%
- `wiki/llm-forecasting-by-domain.md` — Geopolitics strong-tier; news-augmentation recipe; PolyBench Table 6 CWR
- `wiki/polymarket-strategy-matrix.md` — Date-ladder strategy entry; monotonicity sigma-check protocol
- `wiki/uma-optimistic-oracle.md` — Resolution mechanics; FIDE chess precedent; dispute risk taxonomy

## Related

- [[polymarket-strategy-matrix]]
- [[llm-forecasting-by-domain]]
- [[arbitrage-taxonomy]]
- [[uma-optimistic-oracle]]
- [[polymarket-microstructure]]
- [[llm-epistemic-calibration]]
- [[snapshots/polymarket-geopolitics-category-2026-05-13]]
