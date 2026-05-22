# Polymarket Niche Categories — Snapshot 2026-05-13

Combined snapshot of two exotic verticals captured 2026-05-13: **Aliens** (Pop Culture > Aliens, 4 active markets visible) and **Science** (20 active markets per FAQ, $58.7M aggregate vol). These are the wiki's primary documented examples of "non-sports, non-mainstream" Yes/No bets. Notable structural finding: **conditional cross-market bundling** (the "Kevin Warsh" market group). Sources: `raw/research/polymarket-politics-and-niche-markets/05-polymarket-aliens-category.md`, `06-polymarket-science-predictions.md`.

## Aliens — 4 active markets (Pop Culture subcategory)

| # | Title | Type | Vol | Leading | Odds | Notes |
|---|---|---|---|---|---|---|
| 1 | Will the US confirm that aliens exist by...? | Date-ladder | **$38M** | Dec 31 Yes | 15% | Sep 30 = 11% |
| 2 | What will happen before Kevin Warsh is confirmed? | **Conditional bundle** | $734K | both legs No | < 1% / < 1% | Fed rate cut leg + alien disclosure leg in one event |
| 3 | Trump declassifies new UFO files by...? | Date-ladder | $21K | Dec 31 Yes | 91% | May 31 = 34%; very thin |
| 4 | Aliens.gov confirmed immigration website? | Simple binary | $182K | (50-50 split) | 49% Yes | near coin-flip |

**Market-count caveat.** Prior research/search snippets cited "105 markets" in Aliens; the live landing at 2026-05-13 shows only 4 active. Most likely explanation: the 105 figure was all-time (active + resolved); the live page is currently-trading only. Recorded as a snapshot-detail conflict, not a data error.

### Date-ladder no-arb check — "Will the US confirm aliens exist"

Two legs:
- Sep 30 = 11% Yes
- Dec 31 = 15% Yes

`P(by Sep 30) = 11% ≤ P(by Dec 31) = 15%` — monotonic, **4 pp slack, no-arb compliant**. Implied conditional probability of disclosure in Q4 alone: `(0.15 − 0.11) / (1 − 0.11) ≈ 4.5%`.

### The "Kevin Warsh" conditional bundle (novel structure)

`"What will happen before Kevin Warsh is confirmed?"` ($734K vol, cross-listed under Geopolitics too — `raw/.../02-polymarket-geopolitics-master.md`) bundles two structurally-unrelated longshot Yes/No legs:

- **Fed rate cut** (before Warsh confirmation) — < 1% Yes
- **US confirms aliens exist** (before Warsh confirmation) — < 1% Yes

The legs share an icon, a vol display, and the "before Warsh" wrapper. The bundling is a *narrative* framing, not a logical dependency: the two legs are independently resolvable. This is the canonical example of [[polymarket-market-structures]] Structure 6 — *conditional cross-market bundle*. Operational implication: a scraper that filters Aliens by primary-category tag will miss this leg entirely; the alien-disclosure component is reachable only via the Geopolitics or Fed-policy filter.

### Resolution criteria (US-aliens) — partial

Polymarket FAQ on this page uses the standard rule language ("when the event concludes... officially reported, deadline passes, authoritative source confirms"). The widely-cited specific criterion — *"the President, any Cabinet member, any member of Joint Chiefs of Staff, or any US federal agency definitively states that extraterrestrial life or technology exists"* — was not reproduced verbatim in this capture; it comes from prior search context and should be verified against the live market page before being cited as authoritative wiki text. This is another instance of the per-market resolution-rule gap (`master_notes.md` 2026-05-12).

## Science — 20 active markets, $58.7M aggregate

Cross-tagged with Weather, Aliens, Tech, Elon Musk, SpaceX. Dominant sub-clusters: natural-disaster counts, climate ranking, disease counts, space/IPO events.

| Title | Vol | 24h | Liq | Leading | Odds | Ends |
|---|---|---|---|---|---|---|
| Will the US confirm that aliens exist by...? | $38M | $300K | $2M | Dec 31 | 15% | 8 mo |
| SpaceX Starship Flight Test 12 | $2M | $74K | $31K | (success) | 96% | Jun 30 |
| 2026 May 1st, 2nd, 3rd hottest on record? | $86K | $48K | $48K | 1st hottest | 52% | 27 days |
| New pandemic in 2026? | $369K | — | $41K | No | 14% Yes | 8 mo |
| How many 5.5+ earthquakes May 11–17? | $19K | — | $9K | >9 | 17% | 3 days |
| Where will 2026 rank among hottest years? | $3M | — | $63K | 2nd | 57% | 8 mo |
| May 2026 Temperature Increase (ºC) | $21K | — | $23K | 1.15–1.19 ºC | 45% | 27 days |
| 9.0 or above earthquake before 2027? | $189K | — | $11K | No | 3% Yes | 8 mo |
| How many 6.5+ earthquakes May 11–17? | $19K | — | $12K | 0 | 58% | 3 days |
| Measles cases in U.S. by May 31? | $37K | — | $13K | >1900 | 88% | 17 days |
| Largest IPO by market cap in 2026? | $2M | — | $84K | SpaceX | 87% | 8 mo |
| SpaceX IPO Closing Market Cap (Lower Strikes) | $946K | — | $62K | 2.0T+ | 62% | >1 yr |
| Will the Doge-1 Lunar Mission launch before 2027? | $800K | — | $25K | No | 7% Yes | 8 mo |
| 10.0 or above earthquake before 2027? | $601K | — | $15K | No | 6% Yes | 8 mo |
| Another 7.0+ earthquake by...? | $24K | — | $1.5K | May 30 | 51% | 17 days |
| How many 7.0+ earthquakes by June 30? | $2M | — | $2.8K | 8+ | 81% | 2 mo |
| Measles cases in U.S. in 2026? | $8M | — | $17K | >2000 | 99% | 8 mo |
| FDA approves Retatrutide this year? | $564K | — | $2.6K | No | 16% Yes | 8 mo |
| How many Tornadoes in the US in 2026? | $72K | — | $5.6K | 1250+ | 63% | 8 mo |
| How many large volcano eruptions (VEI≥4) in 2026? | $1M | — | $35K | 0 | 59% | 11 mo |

**Markets cited in prior search snippets but NOT in this capture:**
- "Hantavirus pandemic in 2026?" (cited $2.9M vol, 9% odds)
- "Will Jesus Christ return before 2027?" (cited 2% odds)

These were not visible in the 2026-05-13 capture scroll. Most likely the Hantavirus market resolved or was moved to a sibling category; Jesus-return may live under a different filter. Flagged as data gap.

### Sub-cluster structure (volume aggregates)

- **Natural-disaster counts** (earthquakes 5.5+ / 6.5+ / 7.0+ / 9.0+ / 10.0+, tornadoes, volcanoes): ~$2.85M; mostly bracket-bin (Type 4) on Poisson-modelable rates.
- **Climate ranking** (year rank among hottest, monthly temperature increase): ~$3.1M; bracket-bin on continuous physical variables — NOAA-anchored resolution.
- **Disease counts** (measles cases, new pandemic): ~$8.4M; bracket-bin on CDC-tracked counts.
- **Space / IPO** (SpaceX Flight Test, SpaceX IPO, Doge-1 lunar, largest IPO): ~$5.75M; mix of simple binary (Flight Test) and bracket bins (IPO market cap).
- **FDA approvals** (Retatrutide): single binary, $564K, thin.

### Cross-market consistency on earthquakes

The earthquake magnitude ladder (`5.5+`, `6.5+`, `7.0+`, `9.0+`, `10.0+`) creates a structural monotonicity constraint within any time window: `P(at least one 5.5+) ≥ P(at least one 6.5+) ≥ ... ≥ P(at least one 10.0+)`. Annual markets at capture: 9.0+ before 2027 = 3% Yes; 10.0+ before 2027 = 6% Yes (!). This **violates monotonicity** — `P(10.0+) = 6% > P(9.0+) = 3%`. Either the leading-outcome labels in the captured scroll are flipped, the markets resolve on different observables (e.g., 10.0+ = "anywhere globally"; 9.0+ = "in a specific region"), or there's a genuine combinatorial-arb candidate per [[arbitrage-taxonomy]] Def. 3. **Investigation needed**; flag for next research run with a deeper capture of the individual market pages.

### Modeling note — Science is structurally Poisson territory

Most Science markets (earthquakes, tornadoes, volcanoes, disease counts) resolve on observable count statistics from canonical authorities (USGS, NOAA, CDC, WHO). Poisson or negative-binomial rate models calibrated to historical data dominate the structured-forecasting playbook here. PolyBench (see [[llm-forecasting-by-domain]]) did not separately characterize Science as a domain tier; structural-model edge is the more plausible attack than LLM-text-forecasting edge for this vertical.

## Cross-references

- [[polymarket-market-structures]] — Aliens "Kevin Warsh" market is the canonical Structure 6 (conditional bundle) example; date-ladder structure recurs throughout; Science earthquake ladder is a Structure 4 (bracket bins) example with a potential cross-market consistency violation.
- [[mention-markets]] — Aliens is one of the 14 Pop Culture subcategories.
- [[arbitrage-taxonomy]] — earthquake magnitude monotonicity violation flagged here is MRA-candidate territory.
- [[combinatorial-arbitrage-empirics]] — earthquake ladder is multi-market dependence (same physical observable, different thresholds).
- [[llm-forecasting-by-domain]] — Science likely structured-model territory rather than LLM-text territory.
- [[polymarket-bet-content-trends]] — Aliens $38M and Science aggregate provide concrete numbers for the long-tail content claim.

## Source

- `raw/research/polymarket-politics-and-niche-markets/05-polymarket-aliens-category.md` — `polymarket.com/pop-culture/aliens` captured 2026-05-13.
- `raw/research/polymarket-politics-and-niche-markets/06-polymarket-science-predictions.md` — `polymarket.com/predictions/science` captured 2026-05-13.
