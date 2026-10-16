# IGZO 2T0C four-level readout: reference-threshold calibration

The wiki's first page on IGZO (indium-gallium-zinc oxide) 2T0C gain-cell memory as a multilevel weight store. A single-author preprint classifies DC sweeps from 37 isolated IGZO transistors and shows that re-estimating three sensing thresholds from about 8 reference devices cuts four-level misclassification from ≈4.3% to 0.15%. **Nothing was measured on a 2T0C cell, a pulsed write, or an array**; the "error" is misclassified interpolated points, not memory read errors.

## Background

A **2T0C** cell has no capacitor: a write transistor charges the gate of a read transistor, which stores the value as a current. IGZO is attractive because its very low off-state leakage holds the charge, and it can be deposited at low temperature for BEOL stacking (the source's framing, citing prior work). Four current levels per cell give 2 bits; two cells make an INT4 weight.

## What was measured (evidenced, device level)

- 107 DC transfer sweeps from 37 isolated TFTs, W/L = 3/0.5 µm, VD = 1 V, VG swept 3 → −1 V in 0.05 V steps (Agilent B1500A). Not pulsed operation, not inference.
- Target currents for states 00/01/10/11: 0.225 / 1.670 / 5.490 / 10.300 µA.
- Device-resolved operating points cut across-device current SD by 49.4–52.4% versus a shared gate bias (n = 35, second sweep).
- Frozen thresholds mis-classify 4.3% of held-out points. Thresholds re-estimated from k reference devices (mean of 2,000 random draws, third sweep): k=1 15.0%, k=2 5.0%, k=4 1.08%, **k=8 0.15%**, k=16 <0.01%.
- Cost bound: at least 4 cells per reference device, so k=8 is 32 reference cells = 12.5% of a proposed 256-cell data bank. A cell-count bound only; comparators, DAC/mirrors, trim and control are excluded.

## Caveats (the boundary)

- The emulation assumes all four labeled currents of a reference device are available at update time; a real cell holds one state at a time.
- The 2,000 draws resample one 35-device batch; they are not independent devices. 0/140 in leave-one-out is not a zero bit-error rate.
- INT4 proxy (0.862 → 0.160 LSB RMS) is a deterministic error propagation under a uniform weight prior and independent cells, not a network accuracy.
- Circuit feasibility is pre-layout ngspice only (binary decisions correct 2,700/2,700 and 2,400/2,400), with no area, energy or delay.
- No retention, endurance, array, energy or latency data. The authors list pulse-written 2T0C data, array data and update cost as open.

## Why it matters here

(synthesis) It is a small instance of the lab-to-system gap in [[memristor-array-integration-gap]]: device-statistics gains are bought with reference-cell overhead and peripheral circuitry that device-level numbers omit. Evidence level: single device, DC only.

## Source

- `raw/research/weekly-2026-10-15/02-igzo-partitioned-readout.md` — arXiv 2610.16255, Shenzhen University of Advanced Technology, single author. Parsing/figure scripts said to be available; raw measurement files subject to data owners' release decision.

## Related

- [[memristor-array-integration-gap]] — peripheral/reference overhead the device numbers omit
- [[optoelectronic-rram-photonic-programming]] — the other IGZO entry (32-device array)
- [[fefet-analog-imc]] — another multilevel analog memory where sensing decides the system-level payoff
- [[cmos-rram-beol-integration]] — BEOL-compatible oxide memory context
- [[memristor-device-engineering]] — multilevel-state and variability comparison
- [[../viability-ledger]]
- [[../weekly-briefs/2026-10-15]] — brought in by the 2026-10-15 weekly sweep
