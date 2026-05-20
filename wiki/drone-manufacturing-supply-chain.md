# Drone Manufacturing & Supply Chain

The structural / component layer that sits underneath [[canadian-drone-onshoring]]. Honest reading: **Canada's drone sector is an assembler economy, not an OEM economy.** Firms import the load-bearing subsystems (motors, batteries, carbon fibre, optics, NPUs/SoCs) and integrate them; no domestic supply chain exists for the components that actually determine performance. That structural fact — more than funding — is what gates a real Canadian drone industry.

## Assembler vs OEM *(synthesis, anchored in `11`, `13`)*

- Canadian drone firms predominantly **integrate foreign components**: motors, batteries, carbon fibre, cameras/optics, compute boards. The IP that matters (subsystems + airframe design) is mostly not built domestically (`11` — Ogden via BetaKit; ⚠ *sponsored feature* — use the framing, do not cite the "<20 manufacturers" count as hard fact).
- The Walrus (`13`) corroborates the pattern at industrial scale: 800 SkyRanger R70 drones supplied to Ukraine were built by **Teledyne FLIR**, a US-owned branch plant — emblematic of the foreign-dependency default.
- Licensing foreign designs is the symptomatic exit — it forfeits design knowledge and locks firms into long-run dependency (`11`).

## IP erosion via foreign acquisition *(`11` + corroborated)*

The validated-OEM → foreign-acquisition pattern is the central historical mechanism for how Canada loses its drone IP rather than scales it:

- **Aeryon Labs → FLIR Systems, $265M.** Independently corroborated (`11` hyperlinks a prior news source).
- **Deep Trekker** cited in the same lineage as a pre-acquisition Canadian OEM since absorbed (`11`).
- **Canadair CL-89 / CL-289** — Canada's original first-mover drone programs (1960s–90s) — sold to France and Germany in 1987, ending ~25 years of Canadian leadership (`13`). The current onshoring push is, in effect, a rebuild of that squandered position.

## The three-C framework *(`13` — One9 COO Smith)*

A useful diagnostic for what blocks scaling, in order:

| C | State in Canada | Implication |
|---|---|---|
| **Competency** | Strong (AI, cybersecurity, comms, sensors) | Not the bottleneck. The Walrus is explicit. |
| **Capital** | Weak — no defence-/deep-tech-specialised investment culture; SR&ED covers prototyping; **nothing bridges validation → production scale** | Primary bottleneck #1 |
| **Customers** | Weak — government as primary customer is "not reliable, not agile, complacently US-dependent, way too risk-averse"; JUSTAS ran ~33 years with no RFP | Primary bottleneck #2 |

## Software-over-hardware *(editorial, sourced from `13`)*

The Walrus's industrial-policy prescription: don't try to win on **disposable airframes** (China + Ukraine dominate volume + cost); concentrate R&D and capital on **AI / sensing / communications — the "brains"** — where Canadian competency is strongest. Consistent with this wiki's running finding that the consumer-blocking gap is onboard perception/autonomy, not the chassis (see [[drone-autonomy-state]]). Caveat: this is the article's editorial framing, well-argued but not a forecast.

## Named-company datapoints

Per wiki rules: company/PR claims tagged `claimed/unverified` until independently corroborated. Verifiable financials → keep with disclosure; pure PR → keep but tagged.

| Company | Locations | Manufacturing reality | Status / source |
|---|---|---|---|
| **Draganfly** | Saskatoon + Burnaby | **Assembly / integration / QC**, *not* full-stack component manufacture. Products: Heavy Lift, Commander 3 XL. Saskatoon facility announced Jul 2023. | *Operational* (2023 PR); publicly traded NASDAQ:DPRO / CSE:DPRO — financials verifiable on SEDAR+. (`10`) |
| **Volatus Aerospace** | Mirabel (planned) | 200,000 sq ft drone manufacturing hub announced (Oct 2025); serial production of proprietary + licensed platforms, "Canadian supply chain, full configuration control." | ⚠ **Claimed / unverified** — no operational reality, no construction timeline, no first-article date, no named platform models in the release. Independent corroboration required before any deployed-reality citation. (`08`) |
| **Canadian UAVs (Calgary)** | Alberta | BVLOS reconnaissance / situational-awareness platform + intelligence suite; "cost-effective, long endurance" UAS. Recipient of $3M repayable RDII funding (May 2026, PrairiesCan). | *Funded / corroborated by gov source* (`05`). Dual-use hardware; consumer-relevant. |
| **InDro Robotics** | Ottawa region | **InDro Forge** described as a rapid-prototyping / limited-production capability; **InDro Cortex Lite** described as a deployed dual-purpose autonomous brain. No volume / production-rate figures disclosed. | *Practitioner committee submission* (`09`) — policy advocacy, not a capacity disclosure. Volume claims need independent corroboration. |

## Component-level gaps *(synthesis — what isn't covered in this corpus)*

The supply-chain audit, by component category, looks like this against the captured sources:

- **Motors (brushless / outrunners) — imported.** No captured source names a Canadian motor manufacturer at drone-relevant scale. *(gap; future research)*
- **Batteries — predominantly imported cells.** Volatus has *announced* domestic battery supply (`08`, also referenced in the weekly-brief watchlist), but the cell-vs-pack-assembly distinction matters: pack assembly is plausible domestically, **cell-level fab is not corroborated anywhere in this corpus**. Treat "Canadian battery supply" claims with scepticism until BOM-level evidence emerges. Cross-link [[drone-power-budget]] — endurance is propulsion-bound and battery energy density is the ceiling.
- **Optics / image sensors — imported.** No Canadian sensor fab; consumer/industrial CMOS is Sony/onsemi/etc. (See [[drone-sensors-for-autonomy]].)
- **Compute / NPUs / SoCs — entirely imported.** Jetson, Qualcomm, GAP/PULP, Loihi — none Canadian. The closest Canadian capability is design-house / software-integration, not silicon. (See [[nano-drone-compute]], [[neuromorphic-computing-for-drones]].)
- **Carbon fibre — imported** (`11`).

The corpus does **not** contain a BOM-level supply-chain audit; this list is the visible state from the captured sources, not a comprehensive audit. Flagged as a future research thread.

## Drivers that *could* shift the structure

- **DJI ~70% global consumer market share** framed as a disruption / kill-switch risk if banned (`07`, `11`) — opens a non-China alternative slot. Doesn't, by itself, close the component-supply gap; only the integration/airframe slot.
- **The 2026 federal funding wave** ([[canadian-drone-onshoring]]) is mostly aimed at integration-and-commercialization, not subsystem-level fab. Whether DI Assist money reaches actual component manufacturers will determine if the structural picture moves.
- **Transport Canada's Safety Assurance Declaration** path (CAR 901.194 / Std 922) is a structural advantage for a domestic OEM that holds the declaration over an importer who may not — a regulatory moat for whoever scales (`04` via [[canadian-drone-onshoring]]).

## Open items

- BOM-level supply-chain audit per component category (motors, batteries, optics, NPUs, carbon fibre, comms radios).
- Independent corroboration of the Volatus Mirabel buildout (lease/equipment/first-article).
- Aeryon→FLIR primary documents (acquisition terms, IP disposition).
- Canadian compound-semiconductor / NPU design-house mapping (if any).

## Source

- `raw/research/canadian-onshoring/11-betakit-canada-drone-altitude.md` — structural-gap narrative (⚠ sponsored feature)
- `raw/research/canadian-onshoring/13-walrus-canada-drone-race.md` — historical arc, three-C framework, software-over-hardware
- `raw/research/canadian-onshoring/09-indro-defence-strategy-view.md` — practitioner policy-layer gaps (low evidentiary weight)
- `raw/research/canadian-onshoring/10-draganfly-saskatoon-expansion.md` — Draganfly facility datapoint (verifiable)
- `raw/research/canadian-onshoring/08-volatus-mirabel-hub.md` — Volatus Mirabel hub (claimed/unverified)
- `raw/research/canadian-onshoring/05-alberta-defence-mfg-backgrounder.md` — Canadian UAVs $3M RDII datapoint
- `raw/research/canadian-onshoring/07-gowling-2025-drones-canada.md` — DJI/supply-chain-security context

## Related

- [[canadian-drone-onshoring]] — parent / funding wave / market baseline / consolidated gaps
- [[drone-autonomy-state]] — the "software-over-hardware" thesis lands here: brains > airframes
- [[drone-power-budget]] — battery/propulsion is the endurance ceiling; cell-level fab is the unanswered supply question
- [[drone-sensors-for-autonomy]] — optics/sensor sourcing is entirely foreign
- [[nano-drone-compute]] · [[neuromorphic-computing-for-drones]] — compute is fully imported; no Canadian silicon
