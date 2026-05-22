# Feasibility — Geopolitical Date-Ladder (Iran Cluster)

Iran vertical (US-Iran peace, Strait of Hormuz, regime fall, airspace, blockade, uranium) plus Ukraine/Israel/China-Taiwan comparables. **YES, with conditions.** Iran dominates geopolitics volume ~10:1 over other clusters combined. Geopolitics is LLM-strong (Brier 0.14 best across domains per [[llm-forecasting-by-domain]]). Multi-leg monotonicity arb watchlist (airspace 8pp slack, uranium 5pp slack), IMF Portwatch as real-time oracle for Hormuz legs. Live Gamma API 2026-05-16.

## Rubric (snapshot)

| Dimension | Notes |
|---|---|
| Data | Reuters/Bloomberg wires; GDELT free; IMF Portwatch free + = Hormuz resolution oracle; Maxar paid for Kharg; IAEA for uranium |
| Modeling | Saguillo term-structure decomposition + LLM news-catalyst (CWR 50.0% PolyBench Table 6); $500 lot alpha ceiling |
| Saturation | Iran near-saturated on consensus; news-catalyst window shrinking with OSINT-to-market pipelines |
| Resolution risk | **HIGH** on consensus-based markets (peace deal, regime fall, airspace, Kharg); LOW on Portwatch-keyed Hormuz |

## Top markets — Iran cluster (live 2026-05-16)

| Event | Leg | Yes | Vol (leg) | Event total | Liq |
|---|---|---|---|---|---|
| **US-Iran permanent peace deal** | May 31 | **0.105** | $24.1M | $116.8M | $2.25M |
|  | Jun 30 | **0.305** | $9.4M |  |  |
|  | Dec 31 | **0.665** | $1.8M |  |  |
| **Strait of Hormuz traffic normal** | end-May | **0.039** | $14.1M | ~$38M | $517K |
|  | end-Jun | **0.285** | $6.1M |  | $563K |
| **Iranian regime fall** | May 31 | **0.011** | $20.4M | $40.1M | $886K |
|  | Jun 30 | **0.045** | $40.1M |  |  |
| **Blockade lifted (Trump announces)** | May 22 | **0.090** | $1.2M | ~$18M | — |
|  | May 31 | **0.200** | $3.2M |  |  |
|  | Jun 30 | **0.490** | $585K |  |  |
| **US obtains Iranian enriched uranium** | May 31 | **0.065** | $12.5M | ~$13.5M | — |
|  | Jun 30 | **0.115** | $247K |  |  |
|  | Dec 31 | **0.265** | $573K |  |  |
| **Iran closes airspace** (2026-05-13 snapshot) | May 31 | **0.390** | — | $13M | — |
|  | Jun 30 | **0.470** | — |  |  |
| **Kharg Island — not Iranian control** | May 31 | **0.041** | $6.7M | $42.9M | $522K |
|  | Jun 30 | **0.085** | $2.6M |  |  |

## Term-structure (Saguillo monotonicity)

Constraint: `P(by T1) ≤ P(by T2)` for `T1 < T2`. Conditional incremental: `P(event ∈ (T1,T2] | not by T1) = (P2 − P1)/(1 − P1)`.

| Event | T1 | P1 | T2 | P2 | P(window) | Slack |
|---|---|---|---|---|---|---|
| US-Iran peace | May 31 | 10.5% | Jun 30 | 30.5% | **22.3%** | 20.0pp |
| US-Iran peace | Jun 30 | 30.5% | Dec 31 | 66.5% | **51.8%** | 36.0pp |
| Blockade lifted | May 22 | 9.0% | May 31 | 20.0% | **12.1%** | 11.0pp |
| Blockade lifted | May 31 | 20.0% | Jun 30 | 49.0% | **36.3%** | 29.0pp |
| Hormuz traffic | end-May | 3.9% | end-Jun | 28.5% | **25.6%** | 24.6pp |
| Uranium seized | May 31 | 6.5% | Jun 30 | 11.5% | **5.3%** | 5.0pp |
| Kharg Island | May 31 | 4.1% | Jun 30 | 8.5% | **4.6%** | 4.4pp |
| Regime fall | May 31 | 1.1% | Jun 30 | 4.5% | **3.4%** | 3.4pp |
| **Iran airspace** (snap) | **May 31** | **39.0%** | **Jun 30** | **47.0%** | **13.1%** | **8.0pp** |

**Watchlist priority:** Iran airspace (tightest at 8pp); uranium (5pp). Any 4–5pp adverse move closes the gap → inversion = direct Long MRA per [[arbitrage-taxonomy]] §3. Monitor both daily.

## Data sources

| Source | Cost | Signal | Notes |
|---|---|---|---|
| Reuters / Bloomberg wires | Paid ($$$) | Breaking diplomatic | Primary news-catalyst; leakage risk if uncritical |
| AP API | Paid ($) | Authoritative official | Best for verification |
| GDELT Project | Free | Structured CAMEO event extraction (Iran codes 010-030) | 100+ languages; 15-min cadence |
| **IMF Portwatch** | Free | Shipping transit | **= resolution oracle for Hormuz traffic-normal (7-day MA ≥ 60 threshold)** |
| Maxar / Planet Labs | Paid ($$$) | Satellite | Visible change-of-control for Kharg |
| OSM conflict overlays | Free | Geospatial crowd-updated | Lower-reliability for classified positions |
| Twitter/X OSINT | Free | @IranIntl_En, @WarMonitor3, @Intel_Sky | Precedes wire 10–60min; high false-positive |
| IAEA reports | Free | Enrichment levels | Quarterly cadence (too slow for near-term legs) |
| ISW / CSIS / RAND | Free | Calibration anchors | Qualitative; not market-probability-ready |

**Pipeline:** GDELT CAMEO Iran filter → LLM probability update (no raw news injection) → Portwatch pull for Hormuz legs → confidence-weighted Kelly with calibration correction per [[llm-epistemic-calibration]].

## Modeling spine

**LLM news-catalyst (PolyBench Table 6, CWR 50.0%):**
- GPT-5 Brier 0.14 on Geopolitics (best across domains); ECE 0.09 per [[llm-forecasting-by-domain]].
- News augmentation: marginal noise — Claude-3.7 84%→80%; GPT-5 holds 84%. Recipe: base reasoning primary; news context optional with strict cutoff to avoid temporal leakage.
- Strongest signal type: `news_catalyst` tag CWR 50.0% — breaking-news shifts not yet absorbed.
- Failure modes: rumour overweighting (unverified wire reports); definition drift (colloquial vs contract-specific interpretation).
- Alpha ceiling: ~$500/lot per [[llm-forecasting-by-domain]] (CLOB depth exhaustion).

**Per-market fundamentals:**

- **US-Iran peace deal:** Dec 31 at 66.5% implies more-likely-than-not this year — substantially above historical precedent (no US-Iran formal deal since 1979). LLM anchored to base rates would shade 30–45%. **Possible short on Dec 31** if calibration confirms — but UMA dispute risk very high (peace-deal definition).
- **Regime fall:** Resolution requires dissolution of Supreme Leader / Guardian Council / IRGC clerical control. Daily hazard ~0.15% consistent with market. Well-calibrated on definitional bar.
- **Hormuz traffic normal:** Portwatch is both signal source AND resolution oracle. Rising 7-day MA approaching 60 in final 7–10 days converts binary to near-certain — exploitable in final week.
- **Blockade lifted:** Discrete announcement event; news-catalyst dominates. Resolution risk: tweet vs formal statement.
- **Uranium obtained:** Most explicit resolution definition ("officially announces or confirms"). IAEA verification as external anchor.

## Structural-arb opportunities

1. **Airspace ladder inversion (primary watchlist):** 8pp slack. Position for inversion if slack closes to ≤2pp.
2. **Uranium ladder inversion (secondary):** 5pp slack. Single IAEA/State Dept announcement could close gap.
3. **Peace deal Dec 31 short:** 66.5% vs estimated calibrated LLM ~35–45%. Relative-value: short Dec 31 / long Jun 30 hedge. Caveat: UMA dispute = two-sided bet.
4. **Hormuz near-real-time oracle:** If Portwatch 7-day MA rises above ~55 by May 25, May 31 leg at 3.9% becomes a long before market reprices.

## Resolution risk (UMA dispute exposure)

| Market | Resolution source | Dispute risk | Key ambiguity |
|---|---|---|---|
| US-Iran peace deal | Credible reporting consensus | **HIGH** | "Permanent"? Treaty vs executive agreement? |
| Regime fall | Credible reporting + broad consensus | **HIGH** | "Dissolved/incapacitated" — subjective for partial collapses |
| Blockade lifted | Trump official announcement | MEDIUM | Tweet vs formal statement; announced vs implemented |
| Hormuz traffic normal | IMF Portwatch (objective ≥60 threshold) | **LOW** | Portwatch is authoritative and transparent |
| Uranium obtained | Official US government announcement | MEDIUM | "Officially confirms" vs reported-but-unconfirmed |
| Airspace closed | Credible reporting | **HIGH** | Partial vs full? Military vs civilian? |
| Kharg Island control | Credible reporting consensus | **HIGH** | Transient vs permanent seizure? |

**FIDE precedent per [[uma-optimistic-oracle]]:** Chess championship case (both players declared winners of different sections; UMA forced to pick) is directly analogous to Iran-deal market where parties sign a document but disputants disagree it meets "permanent peace" bar. UMA DVM vote arbitrates; outcomes not predictable from fundamentals.

**Bond economics:** $500 proposer / $750 disputer; winning side net ~$250. Disputed resolution delays 4–6 days; market pins near 50–50.

**Mitigation:** Check per-market resolution criteria pre-entry. Portwatch-keyed markets have materially lower resolution risk than consensus-based.

## Ukraine / Israel / China-Taiwan comparables

| Cluster | State | Verdict |
|---|---|---|
| China-Taiwan | Single leg Dec 31 ~7% Yes, $23M | LLM-edge only; saturated; **no structural arb** |
| Ukraine-Russia ceasefire | Oct 31 ~29%, Dec 31 ~46%, $179K (thin) | Conditional Oct–Dec window 24.0%; thin → spread dominates; **too thin for structural arb execution** |
| Israel-Lebanon withdrawal | Jun 30 10%, May 31 1%, $476K–$1M | Jun-only conditional 9.1%; slack wide → low priority |
| Israel-Indonesia normalization | Dec 31 14%, Jun 30 5% | Thin |

**Cross-cluster ranking:** Iran dominates ~10:1 by volume. Iran is the correct primary cluster.

## Decision-tree mapping

1. **Q1 YES-theme?** YES — Geopolitics strong-tier LLM domain per [[llm-forecasting-by-domain]].
2. **Q2 Data source?** YES — GDELT free, Portwatch free + oracle, IAEA free, wire feeds paid optional.
3. **Q3 Structural-arb?** YES — monotonicity Σ-check on Iran cluster; airspace 8pp / uranium 5pp watchlist; Portwatch as real-time near-resolution signal.
4. **Q4 Microstructure?** Liquidity adequate ($166K–$2.25M); $500 CLOB alpha ceiling binding.

## Deployment plan

**Mode 1 — Structural monitoring (daily):** Monotonicity Σ-check across Iran cluster. Priority airspace (8pp) + uranium (5pp). Position for inversion if slack ≤2pp. Portwatch 7-day MA daily for Hormuz legs — days-of-advance signal before resolution.

**Mode 2 — News catalyst (event-driven):** LLM probability update on breaking developments (negotiation rounds, IAEA announcements, military movements). Compare to current price; entry if delta >5pp. Size ≤$500/trade to stay within CLOB alpha ceiling.

**Avoid:** Dec 31 peace deal short (above calibrated estimate but UMA risk very high). All consensus-ambiguous markets without per-market criteria check. Ukraine ceasefire at $179K (too thin for structural execution).

## Open follow-ups

1. Build GDELT CAMEO Iran filter pipeline + 15-min ingestion cadence.
2. Portwatch 7-day MA daily pull for Hormuz legs (free, JSON API).
3. Compute calibrated LLM prior on US-Iran peace deal Dec 31 — confirm short candidacy vs UMA risk.
4. Per-market resolution-criteria sweep before any entry on consensus-based markets.

## Source

- `raw/feasibility/geopolitical-date-ladder/summary.md` (2026-05-16)
- Gamma API live pull 2026-05-16: iran tag + individual event slugs
- [[snapshots/polymarket-geopolitics-category-2026-05-13]]

## Related

- [[polymarket-strategy-matrix]]
- [[llm-forecasting-by-domain]]
- [[arbitrage-taxonomy]]
- [[uma-optimistic-oracle]]
- [[polymarket-microstructure]]
- [[llm-epistemic-calibration]]
- [[snapshots/polymarket-geopolitics-category-2026-05-13]]
- [[feasibility-review]]
