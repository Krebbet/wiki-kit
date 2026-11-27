# 3D NAND analog compute-in-memory macro (IBM / Micron)

IBM Research, Micron and University of Patras (arXiv:2611.27479, preprint) hybrid-bonded a 14 nm FinFET logic die onto a custom 3D NAND wafer and **measured** analog matrix-vector multiply (MVM) at roughly 3–4-bit weight-equivalent precision with 8-bit inputs: 4.8M weights/mm² (on an **estimated** 5 mm² macro area) and up to 4.2 TOPS/W (tile; power breakdown not itemised). Non-spiking; in scope as an analog IMC competitor.

## Terms

- **Hybrid bonding:** direct copper-pad bonding of two dies, giving dense vertical connections.
- **CCO ADC:** current-controlled-oscillator analog-to-digital converter.

## Hardware

- Chip-on-wafer Cu hybrid bond; up to 2048 CCO ADCs on the logic die; ~700 MHz local controller; external FPGA drives the test.
- 4 NAND tiles of 512×256 weights per tier; cells programmed to 1-of-16 conductances; 4 devices per signed weight. First 48 tiers characterised.

## Measured results and their operating points

| Metric | Value | Condition |
|---|---|---|
| Energy efficiency | 4.2 TOPS/W | tile label; 360 ns MVM; x8w3-equivalent error |
| Peak throughput | 2.92 TOPS | same |
| Area efficiency | 0.58 TOPS/mm² | 360 ns; **estimated** 5 mm² |
| Weight density | 4.8M weights/mm² | 24M weights / estimated 5 mm² |
| MVM error σ | ~2.0–2.85% across tiers | synthetic data; integration time unstated |
| CIFAR-10 / CIFAR-100 | 95.96% / 76.57% (FP software 96.39% / 79.8%) | WideResNet-16-8, 11M weights on chip; **550 ns**, not 360 ns; non-MVM ops in software |

No single configuration shows the headline efficiency, density and accuracy together.

## Baseline honesty

The paper calls efficiency "similar" to earlier non-volatile AIMC, but in its own comparison table 4.2 TOPS/W is the lowest entry (PCM 14 nm 9.76–20, RRAM 65 nm 20.7, NOR Flash 40 nm 5.2, SRAM 16 nm 62.84; nodes, precisions and tasks differ). The advantage is density (~12× over the NOR entry, ~35× over SRAM, by ratio of table values). No GPU or digital-accelerator comparison.

## Not reported

Endurance, retention, drift, read/program disturb, temperature, programming time or energy, yield, ADC power share, end-to-end latency or energy per inference.

## Assessment

(synthesis) Measured, integrated macro at lab-prototype maturity; no product or date. It moves the weight-capacity axis, which small RRAM/PCM macros ([[../chips/megatron-pcm-cim-soc]]) have not, but leaves the peripheral-power question in [[memristor-array-integration-gap]] open because the power figure is not broken down. Funded under DARPA OPTIMA.

## Source

- `raw/research/weekly-2026-11-26/01-3d-nand-cim-macro.md` (arXiv:2611.27479)

## Related

- [[memristor-array-integration-gap]]
- [[fefet-analog-imc]]
- [[../chips/megatron-pcm-cim-soc]]
- [[../players/ibm-northpole]]
- [[../viability-ledger]]
- [[../weekly-briefs/2026-11-26]] — brought in by the 2026-11-26 weekly sweep
