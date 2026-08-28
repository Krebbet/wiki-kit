# BrainChip (ASX:BRN)

Publicly listed Australian vendor of the Akida fully-digital, event-based neuromorphic processor family. As of the June 2026 quarter BrainChip is one of the few neuromorphic companies with a named product shipping in production volume from a named foundry on a named node — the AKD1500, built by GlobalFoundries on 22FDX — which makes it the wiki's strongest single datapoint for the "shipping niche now" side of the [[../conflicts/snn-energy-payoff|commercial timeline]] question. The same quarter also disclosed that initial production yield ran **below expectations** and that cash fell to US$20.3M against roughly US$5.3M/quarter of operating outflow. Shipping has started; it is not yet yield-mature and not yet self-funding.

## Product — Akida AKD1500

**What it is (evidenced — this is a product-specification claim, the tier vendor documents are authoritative for):**

| Attribute | Value |
|---|---|
| Architecture | Fully digital, event-based neuromorphic processor (Akida family) |
| Foundry / node | GlobalFoundries, 22 nm Fully Depleted SOI (22FDX) |
| Device class | Mature planar-CMOS-derivative logic. **No** emerging-memory device stack — no RRAM, PCM, FeFET or BEOL integration is involved |
| Interfaces | PCIe; serial (SPI/I²C) |
| Delivery formats | Packaged silicon and bare die (for direct-to-substrate / MCM integration) |
| Target sockets | Sub-watt edge inference; defence and wearables |

Not disclosed anywhere in the captured sources: die size, transistor count, on-chip memory capacity, core count.

**Performance figures (claimed by BrainChip, 2026-06-30 — boundary unstated):**

- `< 300 mW` in PCIe mode, `< 200 mW` in serial mode. Stated as chip-level power envelopes. **No measurement conditions given** — no workload, clock, voltage, ambient temperature, or which functional blocks are active; no idle-vs-active-inference-vs-peak boundary.
- "near-terabyte operations-per-second (TOPS) scale efficiency". This is not a number. There is no TOPS figure, no TOPS/W figure, and no definition of "operation" (MAC? synaptic op? spike event?).

No accuracy, latency, throughput, or benchmark result appears in any captured source. Nothing here is independently verifiable from the sources; there is no datasheet, code, or third-party benchmark.

**Baseline honesty:** the press release asserts the chip avoids "the wasteful always-on energy consumption of traditional AI accelerators" without naming a single competing part, stating a workload, or giving a comparable wattage. No GPU, NPU, or rival neuromorphic chip is named or benchmarked against. This is precisely the class of claim the [[../conflicts/snn-energy-payoff]] file exists to hold to account.

## Maturity and the yield disclosure

Highest rung reached: **production shipments**, with a named fab and node — the top of this wiki's maturity ladder short of volume maturity. But two things in the same quarter qualify it:

- **Environmental qualification is still in progress.** The announcement itself states the chip "undergoes comprehensive industrial and military-grade qualification" and will "undergo rigorous qualification testing for an array of extreme thermal and environmental screening tiers" — i.e. commercial availability was declared before reliability validation completed. Pass/fail status is not disclosed.
- **Initial production yield was below expectations** (June 2026 quarter). Company-disclosed, but **no numeric yield figure exists in any captured source** — only the qualitative admission, with no root cause. This is the single most wiki-relevant number in the whole BrainChip story and it is unquantified.

Shipment volume and customer identities are likewise undisclosed; "production quantities" and "multiple customers" carry no counts.

**Update, 1H CY2026 half-year report (period ended 30 June 2026):** a specific unit count now exists — BrainChip states it shipped a **first production batch of 2,000 AKD1500 units** during the half, described as the transition from pre-production to commercial-scale manufacturing. This is evidenced (company-reported) but is explicitly a "first batch," not a cumulative or lifetime total — the earlier open question about total unit volumes is only partly answered. No root cause for the below-expectations yield accompanies this figure.

## Financial position

Company-disclosed figures, via a trade-press rollup of the June 2026 Appendix 4C quarterly (reported ~2026-07-27). These are **one level removed from primary** — the outlet paraphrases rather than quotes the filing, and links no primary document. Verify against BrainChip's actual ASX filings before relying on them.

| Metric | Value | As of |
|---|---|---|
| Cash | ~US$20.3M (down from ~US$25.3M) | 30 Jun 2026 (vs 31 Mar 2026) |
| Operating cash outflow | ~US$5.3M/quarter | Mar 2026 quarter |
| Customer cash receipts | ~US$0.66M/quarter | Mar 2026 quarter |
| Trailing annual revenue | ~US$1.9M | "mid-2026" — period boundary ambiguous in the source; unclear whether TTM ends March or June 2026 |

*(synthesis)* ~US$20M cash against ~US$5M/quarter burn implies roughly four quarters of runway at an unchanged burn rate. **Neither the company nor the outlet states this** — it is arithmetic on their disclosed numbers, and it ignores any financing, revenue growth, or cost change.

**Hygiene note:** an A$21.5M placement figure circulating in older discussion dates to **2017** and is unrelated to the current funding position. The outlet raised this specifically to debunk it. Do not let it enter any funding total as current.

### 1H CY2026 half-year P&L (added 2026-08-27, weekly sweep)

Company-disclosed figures for the half-year ended 30 June 2026, via a Motley Fool Australia relay of the ASX filing (one level removed from primary; verify against the actual filing before relying on them). **The 30 Jun 2026 cash balance below (US$20,304,971) matches the quarterly-rollup figure above exactly** — same balance date, same underlying filing, different accounting lens (half-year P&L vs quarterly cash-flow statement).

| Metric | 1H CY2026 | 1H 2025 | Change |
|---|---|---|---|
| Revenue | US$1,222,745 | (not given, % only) | +19% YoY |
| Net loss after tax | US$12,015,897 | US$9,360,251 | +28% YoY (widened) |
| Operating expenses | US$13,647,140 | (not given, % only) | +33% YoY |
| Cash and equivalents | US$20,304,971 | — | as at 30 Jun 2026 |

**Do not conflate operating expenses (P&L, half-year) with operating cash outflow (cash-flow statement, quarterly, ~US$5.3M/quarter above) to recompute runway** — they are different accounting measures and the source does not do this arithmetic itself. No updated runway figure is available from this source; the ~4-quarter *(synthesis)* estimate above still rests on the Mar 2026 quarterly cash-flow figure, not on this half-year opex number.

New commercial detail from the same report: IP licensing deals signed with **EDGEAI** and **ASICLAND** during the half (revenue described as "potential," not yet broken out), a new **MicroIP** ecosystem partnership, and the **LDA Capital financing facility concluded** during the period with obligations "substantially settled" — removing a prior funding mechanism with no stated replacement. AKD2500 is tracking toward a "late-2026 development milestone" (claimed, owner BrainChip, no exact date).

## Partnerships

All named as claimed partnerships; the outlet's own caveat is that they carry **no publicly disclosed production volumes or revenue commitments**, and some contain termination provisions.

- Parsons — strategic agreement, defence/aerospace (October 2025)
- Raytheon-linked US Air Force neuromorphic radar initiative (dating to April 2025)
- EDGEAI — smart-metering licensing (March 2026)
- MicroIP (Taiwan) — production-module partnership (June 2026)
- IBM — **Symphony Community Akida Bundle** (claimed by BrainChip, 2026-08-20): a free, open-source (GitHub) integration letting Akida processors be scheduled as a managed resource alongside GPUs/CPUs inside IBM Spectrum Symphony Community Edition. This is a distinct commercial-signal shape from the rest of the list — it's a software-orchestration integration, not a silicon design win, and its stated significance is extending Akida's addressable market from edge devices toward on-prem **enterprise servers**. No customer, deployment, or performance number attached; treat "equal footing with GPUs" as BrainChip's own framing, not an independent benchmark.

## Open questions

- What is the actual AKD1500 yield figure, and what is the root cause? *(unquantified in all sources)*
- Did environmental/military qualification complete, and did it pass?
- Any TOPS/W figure with a stated measurement boundary, or any third-party benchmark — e.g. a [[../benchmarks/neurobench]] system-track submission or MLPerf Tiny entry?
- Named customers behind "multiple customers", and whether the 2,000-unit first batch has fully shipped to them.
- Root cause of the below-expectations yield — still unquantified and unaddressed even in the 1H CY2026 report.
- Any TOPS/W figure with a stated measurement boundary, or any third-party benchmark — e.g. a [[../benchmarks/neurobench]] system-track submission or MLPerf Tiny entry?
- Actual quarterly cash-flow outflow for the Jun 2026 quarter, to update the runway synthesis on a like-for-like basis with the Mar 2026 figure.
- The September 2026 quarterly is the next disclosure checkpoint for yield improvement and H2-2026 volume.

## Source

- `raw/research/neuromorphic-commercial-viability/01-brainchip-akd1500-shipments.md` — BrainChip press release, "Commercial Availability and Production Shipments of AKD1500 Neuromorphic Processors", 2026-06-30. Vendor primary; tier 3 (authoritative for what the product is, not for how good it is).
- `raw/research/neuromorphic-commercial-viability/03-brainchip-yield-cash.md` — Kalkine, "BrainChip (ASX:BRN) Starts Shipping Silicon — But the Cash Clock Is Ticking". Trade/financial commentary; tier 5 (event pointer only). Separates its bull and bear cases explicitly, which is to its credit, but paraphrases filings without linking them.
- `raw/research/weekly-2026-08-20/04-brainchip-symphony-ibm-bundle.md` — BrainChip press release, "BrainChip Launches Symphony Community Akida Bundle for IBM's Workload Management Solution", 2026-08-20. Vendor primary.
- `raw/research/weekly-2026-08-27/03-brainchip-h1-cy2026.md` — Motley Fool Australia, "BrainChip shares: Half-year results show revenue up, loss widens", 2026-08-26. Relay of BrainChip's ASX half-year filing; tier 4 (one level removed from primary, no filing linked).

## Related

- [[roster]] — where BrainChip sits against the other players
- [[../conflicts/snn-energy-payoff]] — BrainChip's unquantified power and efficiency claims are Position A evidence
- [[../benchmarks/neurobench]] — the measurement protocol that would settle those claims
- [[../weekly-briefs/2026-08-20]] — brought in by the 2026-08-20 weekly sweep
- [[../weekly-briefs/2026-08-27]] — brought in by the 2026-08-27 weekly sweep
