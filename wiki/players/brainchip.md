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

## Partnerships

All named as claimed partnerships; the outlet's own caveat is that they carry **no publicly disclosed production volumes or revenue commitments**, and some contain termination provisions.

- Parsons — strategic agreement, defence/aerospace (October 2025)
- Raytheon-linked US Air Force neuromorphic radar initiative (dating to April 2025)
- EDGEAI — smart-metering licensing (March 2026)
- MicroIP (Taiwan) — production-module partnership (June 2026)

## Open questions

- What is the actual AKD1500 yield figure, and what is the root cause? *(unquantified in all sources)*
- Did environmental/military qualification complete, and did it pass?
- Any TOPS/W figure with a stated measurement boundary, or any third-party benchmark — e.g. a [[../benchmarks/neurobench]] system-track submission or MLPerf Tiny entry?
- Unit volumes and named customers behind "multiple customers".
- The September 2026 quarterly is the next disclosure checkpoint for yield improvement and H2-2026 volume.

## Source

- `raw/research/neuromorphic-commercial-viability/01-brainchip-akd1500-shipments.md` — BrainChip press release, "Commercial Availability and Production Shipments of AKD1500 Neuromorphic Processors", 2026-06-30. Vendor primary; tier 3 (authoritative for what the product is, not for how good it is).
- `raw/research/neuromorphic-commercial-viability/03-brainchip-yield-cash.md` — Kalkine, "BrainChip (ASX:BRN) Starts Shipping Silicon — But the Cash Clock Is Ticking". Trade/financial commentary; tier 5 (event pointer only). Separates its bull and bear cases explicitly, which is to its credit, but paraphrases filings without linking them.

## Related

- [[roster]] — where BrainChip sits against the other players
- [[../conflicts/snn-energy-payoff]] — BrainChip's unquantified power and efficiency claims are Position A evidence
- [[../benchmarks/neurobench]] — the measurement protocol that would settle those claims
