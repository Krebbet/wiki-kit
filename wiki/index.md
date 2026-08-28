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
| [[players/intel-loihi2]] | Intel Loihi 2 — the field's most-used research platform, INRC-gated, not for sale. Graded 32-bit spikes (not 1-bit) invalidate Loihi-1-calibrated energy models. **Lava SDK archived 2026-05-13.** Hala Point's 15 TOPS/W contradicts Intel's own 20 petaops / 2,600 W arithmetic (≈7.7). |
| [[players/ibm-northpole]] | IBM NorthPole — brain-inspired, fully digital, **not spiking**, no off-chip DRAM. 3B-param LLM at 28,356 tok/s on 16 cards. Every headline multiplier (46.9×, 72.7×, 25×) cites an unnamed GPU. |
| [[players/brainchip]] | BrainChip (ASX:BRN) — Akida AKD1500 shipping from GlobalFoundries 22FDX into defence and wearables; first 2,000-unit production batch shipped 1H CY2026. Yield below expectations, revenue up 19%/loss up 28% YoY. The wiki's strongest "actually shipping" datapoint. |

---

## Devices & materials

| Page | Summary |
|---|---|
| [[devices/memristor-device-engineering]] | Material families, switching mechanisms, and the four engineering levers (doping, electrodes, interface layers, pulse protocol). Single-device comparison table — endurance to 10¹², 11-bit conductance resolution. |
| [[devices/memristor-array-integration-gap]] | Why those device numbers don't survive to system level: ADC/DAC >70% of system power, static leakage, the energy-precision trade-off, and eleven itemized lab-to-fab blockers. The most load-bearing device page for the viability question. |
| [[devices/fefet-analog-imc]] | FeFET analog in-memory compute — polarization switching, multi-level storage, analog shift-add. 14.47 TOPS/W with the ADC counted. Advantage erodes 1.56× → 1.37× at system level. **Simulation only; no endurance, retention or measured variability.** |
| [[devices/analog-training-nonidealities]] | Why plain gradient descent fails on analog devices: response-function asymmetry, not defects. Analog SGD collapses below 15% where Tiki-Taka holds 97%. A device engineered for symmetry measures 61% skew on real silicon. |
| [[devices/event-cameras]] | Event-based vision sensors — the front end that makes workloads natively sparse. Real commercial parts from 3 mW to 12 W. Named automotive design wins (vendor-claimed). The processing gap: most pipelines densify events back into frames. |
| [[devices/cmos-rram-beol-integration]] | Inserting RRAM into commercial CMOS BEOL without a foundry embedded-RRAM PDK. 16×16 1T1R validated on 180 nm; larger arrays structural only. Evidence the foundry gate is tractable, not that it's solved. |
| [[devices/optoelectronic-rram-photonic-programming]] | Optoelectronic RRAM (ORRAM) — memristive cells written with light, not voltage. 32-device IGZO array, µLED-array optical SET / electrical RESET, optical fading memory ~2500× longer than electrical relaxation. Academic-only; no endurance, retention, or CMOS-integrated ORRAM yet. |

---

## Chips & systems

| Page | Summary |
|---|---|
| [[chips/loihi2-persistent-monitoring]] | Intel Loihi 2 — acoustic anomaly detection on a 16-chip VPX system. The wiki's first primary Loihi 2 source. Headline "two orders of magnitude" efficiency claim is dynamic-energy-only (474–496×); boundary-honest total-energy figure is 2.1–40.2×. |

---

## Spiking neural networks

| Page | Summary |
|---|---|
| [[snn/snn-energy-hardware-realistic]] | Six SNN algorithm papers re-measured on hardware-realistic simulators. Every one overstates: 10–83× claimed vs 1.3–25× actual. The three omitted costs — timestep data movement, LIF overhead, crossbar non-idealities. |
| [[snn/snn-training-surrogate-gradients]] | How SNNs are trained at all. The Heaviside derivative annihilates gradients; surrogate gradients patch only the backward pass. Taxonomy of the four approaches, and why BPTT's O(NT) memory and non-local transport rule it out on-chip. 2019 vintage. |
| [[snn/ann2snn-differential-coding]] | Training-free conversion at T=4–8. CNNs reach the favourable regime; **transformers cross energy ratio 1.0 exactly where accuracy reaches parity** — the converted SNN costs more than the ANN. Multi-threshold neurons, not differential coding, do most of the work. |
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
| [[conflicts/analog-onchip-training-viability]] | **Open.** Does in-situ training rescue imperfect analog arrays? The yield-economics argument rests on SGD-based training that fails on realistic response curves with no defects present. Resolution: read Li et al. and establish the actual update rule. |
| [[conflicts/snn-energy-payoff]] | **Open.** Vendor and algorithm-paper claims (10–100×) against hardware-realistic and capacity-matched accounting (1.3–25×, often worse than a quantized ANN). Separated by measurement boundary and baseline capacity. Resolution condition: a NeuroBench system-track submission. |

---
