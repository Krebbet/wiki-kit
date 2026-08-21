# Player roster

Who is actually in neuromorphic hardware, and what each has in hand versus on paper. The distinction this page enforces: **silicon-in-hand** (a named part, on a named node, at a named fab, shipping to customers) versus **paper-only** (announced, funded, or published, with no verifiable shipping product). A funding round is evidence of belief, not of silicon.

Seeded 2026-08-20 from the first research run. Coverage is thin and deliberately so — a row appears only when a captured source supports it. Absence from this table means "not yet researched", not "not a player".

## Status ladder

`paper` → `sampling` → `production shipments` → `volume, yield-mature` → `self-funding`

## Roster

| Player | Product | Node / fab | Status | Last verified | Evidence quality |
|---|---|---|---|---|---|
| [[brainchip]] (ASX:BRN) | Akida AKD1500 | 22FDX @ GlobalFoundries | **production shipments** — yield below expectations, not yet self-funding (~US$1.9M trailing revenue vs ~US$5.3M/qtr outflow) | 2026-06-30 | Vendor primary + company-disclosed quarterly. Node and fab named and checkable. No performance figure carries a measurement boundary. |
| Innatera Nanosystems | Spiking Neural Processor T1 | not disclosed | **unknown — stale record.** Claimed production "later this year" and high-volume delivery "Q2 2025" *as of ~April 2024*. Both dates are now in the past; outcome unknown from any captured source. | ~2024-04 ⚠️ | Trade press only. No node, no fab, no independently measured figure. |

### Innatera — why the row is deliberately empty

The only captured Innatera source is a funding brief estimated at **~April 2024** (the capture recorded no publication date; the vintage was reconstructed from internal evidence — T1 unveiled "in January", $16M closed "in March", $5M top-up "this month", and a still-future "Q2 of 2025" delivery target).

What it supports as evidenced:

- **$21M extended Series A** — $16M (March) plus a $5M top-up from new investors. Investors in the original tranche: EIC Fund, MIG Capital, Matterwave Ventures, Delft Enterprises.
- Founded 2018, Rijswijk, Netherlands; TU Delft spinout.
- T1 combines a proprietary event-driven engine, a RISC-V CPU, and a CNN accelerator, described as "analog-mixed signal". Target sockets: wearables, smart home, consumer electronics.

What it does **not** support: any performance claim. The source's only comparative figure — **"500× less energy and 100× faster"** — has no named baseline ("conventional approaches"), no workload, no units beyond the multiplier, no measurement boundary, and no third-party verification. It is a vendor marketing line restated by a journalist. Recorded as Position A evidence in [[../conflicts/snn-energy-payoff]], not as a fact about Innatera silicon.

A dedicated Innatera page is deliberately **not** created from this source alone. It should be opened when a second, technical source lands — a T1/Pulsar datasheet, a node/fab disclosure, or a shipping-status update.

## Named but not yet researched

Encountered in captured sources without enough evidence for a row. Each is a research target, not a claim:

- **Intel** (Loihi 2) — appears as a NeuroBench system-track baseline platform and as a co-author institution. Now has one direct primary source: [[../chips/loihi2-persistent-monitoring]] (2026-08-20 weekly sweep) — a 16-chip VPX system running acoustic anomaly detection. Still short of a full row: no yield, volume, or pricing disclosure captured.
- **SynSense** (Xylo) — appears as a NeuroBench system-track baseline platform and as a co-author institution.
- **imec**, **TU Delft**, **Harvard** — NeuroBench co-author institutions.
- **Prophesee**, **SpiNNcloud**, **Sony** — NeuroBench co-author organisations.
- **GlobalFoundries** — foundry, evidenced via BrainChip's 22FDX relationship.
- **TSMC** — the only foundry-node-level embedded-RRAM claim in the device literature captured so far (40 nm RRAM 2019; 22 nm eRRAM 2024, per [[../devices/memristor-array-integration-gap]]).
- **University of Edinburgh (Prodromakis group)** — the CMOS-RRAM prototyping route in [[../devices/cmos-rram-beol-integration]].

## Open questions

- Did Innatera hit its Q2-2025 high-volume milestone? This is now a resolvable pass/fail on a dated roadmap claim — exactly the kind of credibility datapoint this roster exists to keep.
- No analog in-memory-compute competitor (EnCharge, Mythic, Rain, Axelera) has been researched yet, despite being in scope where they compete for the same edge sockets.
- No Chinese player (Tianjic and successors) is covered at all.

## Source

- `raw/research/neuromorphic-commercial-viability/01-brainchip-akd1500-shipments.md` — BrainChip press release, 2026-06-30.
- `raw/research/neuromorphic-commercial-viability/02-innatera-21m-round.md` — DatacenterDynamics, "Neuromorphic processor startup Innatera raises $21m". ⚠️ No publication date in the capture; vintage estimated ~April 2024 from internal evidence.
- `raw/research/neuromorphic-commercial-viability/03-brainchip-yield-cash.md` — Kalkine, BrainChip June-2026 quarter commentary.

## Related

- [[brainchip]] — the one player with a full record so far
- [[../conflicts/snn-energy-payoff]] — where vendor efficiency claims are held to account
- [[../viability-ledger]] — per-technology timeline these players feed
