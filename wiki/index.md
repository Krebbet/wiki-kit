# Wiki Index

Neuromorphic computing end to end: materials and devices, spiking neural networks, the chips and sensors that integrate them, and the industry deciding when any of it becomes commercially viable.

Catalog of all pages in this wiki. Updated on every ingest.

---

## Overview & meta

| Page | Summary |
|---|---|
| [[viability-ledger]] | **Start here.** Per-technology and per-application commercial-viability status, the blocker gating each, and the leading indicator that would move it. Synthesis over everything below. |
| [[reference-sources]] | The radar — watched feeds, journals, conferences, vendors, programmes and benchmarks, plus this wiki's scope, selection priority and brief conventions. Consulted by `/weekly-brief`, evolved by `/lint`. |
| [[watchlist]] | Identified-but-not-yet-captured ledger. Weekly-brief overflow lands here; entries graduate to full pages when they become load-bearing. |

---

## Players & industry

| Page | Summary |
|---|---|
| [[players/roster]] | Who is in neuromorphic hardware and what each has in hand versus on paper. Silicon-in-hand vs paper-only, with last-verified dates. |
| [[players/brainchip]] | BrainChip (ASX:BRN) — Akida AKD1500 shipping from GlobalFoundries 22FDX into defence and wearables. Yield below expectations, ~1 year of cash runway. The wiki's strongest "actually shipping" datapoint. |

---

## Devices & materials

| Page | Summary |
|---|---|
| [[devices/memristor-device-engineering]] | Material families, switching mechanisms, and the four engineering levers (doping, electrodes, interface layers, pulse protocol). Single-device comparison table — endurance to 10¹², 11-bit conductance resolution. |
| [[devices/memristor-array-integration-gap]] | Why those device numbers don't survive to system level: ADC/DAC >70% of system power, static leakage, the energy-precision trade-off, and eleven itemized lab-to-fab blockers. The most load-bearing device page for the viability question. |
| [[devices/cmos-rram-beol-integration]] | Inserting RRAM into commercial CMOS BEOL without a foundry embedded-RRAM PDK. 16×16 1T1R validated on 180 nm; larger arrays structural only. Evidence the foundry gate is tractable, not that it's solved. |

---

## Spiking neural networks

| Page | Summary |
|---|---|
| [[snn/snn-energy-hardware-realistic]] | Six SNN algorithm papers re-measured on hardware-realistic simulators. Every one overstates: 10–83× claimed vs 1.3–25× actual. The three omitted costs — timestep data movement, LIF overhead, crossbar non-idealities. |
| [[snn/snn-energy-breakeven-conditions]] | Capacity-matched analytical comparison against quantized ANNs. SNNs win only at T ≤ 5 and spike rate < ~5.7%; they lose on most realistic workloads, and by 3.8× on spiking Llama-2 7B. |

---

## Benchmarks

| Page | Summary |
|---|---|
| [[benchmarks/neurobench]] | The field's MLPerf analogue, ~40 institutions. Defines the measurement boundary this wiki adopts: complexity metrics are **not** energy numbers; only system-track idle/active/dynamic power counts. Xylo 60.9× vs Arduino at matched accuracy. |

---

## Conflicts

| Page | Summary |
|---|---|
| [[conflicts/snn-energy-payoff]] | **Open.** Vendor and algorithm-paper claims (10–100×) against hardware-realistic and capacity-matched accounting (1.3–25×, often worse than a quantized ANN). Separated by measurement boundary and baseline capacity. Resolution condition: a NeuroBench system-track submission. |

---
