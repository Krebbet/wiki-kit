# Polymarket Geopolitics Category — Snapshot 2026-05-13

Combined snapshot of the **Geopolitics master category** (`polymarket.com/geopolitics`, 567 markets / 16 subcategories) and its largest active sub-vertical **Iran** (`polymarket.com/iran`, 184 markets / 12 subcategories). Captured 2026-05-13. Iran is the canonical date-ladder vertical: nearly every high-volume topic has 2–3 dated legs (May 31 / Jun 30 / Dec 31), creating an explicit term-structure of probabilities. Sources: `raw/research/polymarket-politics-and-niche-markets/02-polymarket-geopolitics-master.md`, `03-polymarket-iran-category.md`.

## Geopolitics master — subcategories (16, with counts)

| Subcategory | Count | URL slug |
|---|---|---|
| All | **567** | `/geopolitics` |
| Ukraine | 106 | `/geopolitics/ukraine` |
| Iran | 95 | `/geopolitics/iran` |
| Middle East | 74 | `/geopolitics/middle-east` |
| Israel | 73 | `/geopolitics/israel` |
| Ukraine Map | 62 | `/geopolitics/ukraine-map` |
| China | 49 | `/geopolitics/china` |
| Venezuela | 31 | `/geopolitics/venezuela` |
| Oil | 30 | `/geopolitics/oil` |
| Gaza | 17 | `/geopolitics/gaza` |
| Cuba | 10 | `/geopolitics/cuba` |
| Syria | 7 | `/geopolitics/syria` |
| Turkey | 5 | `/geopolitics/turkey` |
| Yemen | 2 | `/geopolitics/yemen` |
| Sudan | 2 | `/geopolitics/sudan` |
| Thailand-Cambodia | 2 | `/geopolitics/thailand-cambodia` |
| India-Pakistan | 2 | `/geopolitics/india-pakistan` |

(Iran shows as 95 here; the dedicated Iran subcategory landing page shows 184 — see Iran-vertical section below. The 95 figure on the Geopolitics page is likely a stricter scope filter; the 184 figure is the canonical Iran-vertical count.)

## Iran subcategory taxonomy (12 named, 184 total)

| Subcategory | Count |
|---|---|
| All Iran | **184** |
| U.S. x Iran | 40 |
| Oil | 30 |
| Iran Ceasefire | 28 |
| Iran Regime | 17 |
| Strait of Hormuz | 16 |
| Lebanon | 14 |
| Israel x Iran | 12 |
| Nuclear | 9 |
| Reza Pahlavi | 7 |
| Regional Spillover | 5 |
| Military Strikes | 3 |
| Kurds | 3 |

## Top markets (combined from both pages, 20 distinct event groups)

| Market | Cum. Vol | Leading | Odds | Resolution dates |
|---|---|---|---|---|
| US x Iran permanent peace deal | **$111M** | Dec 31 Yes | 63% | Jun 30 = 34% |
| **Kharg Island no longer under Iranian control** | **$42M** | No (both legs) | Jun 30 Yes 10% / May 31 Yes 5% | Jun 30 / May 31 |
| **Iranian regime fall by Jun 30** | **$39M** | No | 5% Yes | Jun 30 |
| US x Iran diplomatic meeting | $36M | Jun 30 Yes | 60% | Jun 30 / May 31 = 26% |
| Will the U.S. invade Iran before 2027? | $28M | No | 29% Yes | Dec 31 |
| Will China invade Taiwan by end of 2026? | $23M | No | 7% Yes | Dec 31 |
| Will the Iranian regime fall by May 31? | $19M | No | 1% Yes | May 31 |
| Will Reza Pahlavi enter Iran by...? | $18M | No | Dec 31 Yes 13% / Jun 30 Yes 3% | Dec 31 / Jun 30 |
| Trump announces US blockade of Hormuz lifted | $17M | Jun 30 Yes | 51% | Jun 30 / May 31 = 23% |
| Strait of Hormuz traffic normal by May 15 | $15M | No | < 1% Yes | May 15 |
| US obtains Iranian enriched uranium | $13M | No | Dec 31 Yes 27% / Jun 30 Yes 13% | Dec 31 / Jun 30 |
| Strait of Hormuz traffic normal by end of May | $13M | No | 8% Yes | end-May |
| Iran closes its airspace | $13M | No | Jun 30 Yes 47% / May 31 Yes 39% | Jun 30 / May 31 — **tightest spread** |
| Iran leader end of 2026? | $8M | Mojtaba Khamenei | 64% Yes / Reza Pahlavi 8% Yes | Dec 31 |
| Strait of Hormuz traffic normal by end of June | $5M | No | 32% Yes | Jun 30 |
| US strike on Cuba by Dec 31 | $2M | No | 37% Yes | Dec 31 |
| Putin out as President of Russia by Jun 30 | $2M | No | 2% Yes | Jun 30 |
| Israel and Indonesia normalize relations | $1M | No | Dec 31 Yes 14% / Jun 30 Yes 5% | Dec 31 / Jun 30 |
| Israel withdraws from Lebanon | $1M | No | Jun 30 Yes 10% / May 31 Yes 1% | Jun 30 / May 31 |
| Mohammed bin Salman out as Saudi leader | $821K | No | Dec 31 Yes 7% / Jun 30 Yes 2% | Dec 31 / Jun 30 |
| **Russia x Ukraine ceasefire agreement** | $179K | No | Dec 31 Yes 46% / Oct 31 Yes 29% | Dec 31 / Oct 31 — **NEW; thinly traded** |
| What Iranian demands will Trump agree to by May 31? | $955K | No (each) | Oil Sanction Relief 15%; Unfreeze Assets 14% | May 31 |
| Will France/UK/Germany strike Iran by Jun 30 | $1M | No | 5% Yes | Jun 30 |
| Will Israel launch ground operation in Iran by May 31 | $476K | No | 8% Yes | May 31 |

## Date-ladder term structure — monotonicity checks (all currently no-arb)

The dominant structure here is date-ladder (Structure 2 in [[polymarket-market-structures]]). At capture, every observed ladder satisfies `P(by T_1) ≤ P(by T_2)` for `T_1 < T_2` — **no live arb violations**. Worked conditional probabilities:

| Event | Near Pr | Far Pr | Conditional P(event in far-only window) |
|---|---|---|---|
| US-Iran peace deal | Jun 30 = 34% | Dec 31 = 63% | (0.63 − 0.34) / (1 − 0.34) ≈ **44%** |
| Strait of Hormuz normal | end-May = 8% | end-June = 32% | (0.32 − 0.08) / (1 − 0.08) ≈ **26%** |
| Iranian regime fall | May 31 = 1% | Jun 30 = 5% | (0.05 − 0.01) / (1 − 0.01) ≈ **4%** |
| Trump blockade lifted | May 31 = 23% | Jun 30 = 51% | (0.51 − 0.23) / (1 − 0.23) ≈ **36%** |
| Iran closes airspace | May 31 = 39% | Jun 30 = 47% | (0.47 − 0.39) / (1 − 0.39) ≈ **13%** — **tightest spread to watch** |
| US-Iran diplomatic meeting | May 31 = 26% | Jun 30 = 60% | (0.60 − 0.26) / (1 − 0.26) ≈ **46%** |

Iran airspace at 39% / 47% is **8 percentage points** of slack — a small inversion under news flow could trigger an MRA opportunity per [[arbitrage-taxonomy]] Def. 3. Watch this spread.

## Volume concentration

Top-3 markets account for $192M of visible vol on this snapshot: US-Iran peace deal $111M + Kharg Island $42M + Iranian regime fall (Jun 30) $39M. The Iran cluster (all Iran-related markets summed) constitutes the bulk of geopolitics volume at this date — consistent with [[polymarket-bet-content-trends]] which documented Iran-strike $73M and Khamenei spike $39M as the largest geopolitical contracts in Polymarket history.

**Anomaly:** Ukraine has 106 markets (highest count in Geopolitics) but the headline Russia-Ukraine ceasefire market is only **$179K** at capture (tagged NEW). The mismatch suggests the Ukraine market count is broadly distributed with no single high-volume anchor at present, in contrast to Iran's concentrated activity around a few flagship events.

## Resolution mechanism (per page FAQ)

> "Each Geopolitics market has a clearly defined resolution source and criteria published on the market page. When the event concludes — for example, when a result is officially reported, a deadline passes, or an authoritative source confirms the outcome — the market resolves and winning shares pay out $1 each. Markets in categories such as Elections, Economy, and Geopolitics typically rely on official government, regulatory, or primary-source reporting for resolution."

Per-market rules require individual market page reads. **Geopolitics fee-free status** (per Fee Structure V2 cited in [[platform-comparison-kalshi-polymarket]]) is **not visibly confirmed** on the category landing page — neither asserted nor contradicted here.

## Cross-references

- [[polymarket-market-structures]] — Iran is the canonical exemplar of Structure 2 (date-ladder).
- [[arbitrage-taxonomy]] — monotonicity violations across dated legs are Market Rebalancing Arbitrage candidates; airspace ladder is the watchlist anchor.
- [[polymarket-bet-content-trends]] — historical Iran-strike $73M and Khamenei spike $39M context.
- [[uma-optimistic-oracle]] — resolution backbone.
- [[llm-forecasting-by-domain]] — Geopolitics is the strongest-tier LLM-forecasting domain; this snapshot enumerates the active markets where LLM signal is most reliable.
- [[platform-comparison-kalshi-polymarket]] — Fee Structure V2 (Geopolitics = fee-free in the documented schedule).

## Source

- `raw/research/polymarket-politics-and-niche-markets/02-polymarket-geopolitics-master.md` — `polymarket.com/geopolitics` captured 2026-05-13.
- `raw/research/polymarket-politics-and-niche-markets/03-polymarket-iran-category.md` — `polymarket.com/iran` captured 2026-05-13.
