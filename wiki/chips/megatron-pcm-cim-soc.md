# MEGATRON — 28nm analog PCM compute-in-memory / RISC-V SoC for edge GenAI

The wiki's first measured phase-change-memory (PCM) compute-in-memory chip on a foundry-embedded process. Bologna, Chips-IT and STMicroelectronics (arXiv 2609.35254) report a fabricated 28nm FD-SOI heterogeneous SoC: a 4Mi-cell (2M-parameter) analog PCM macro plus a RISC-V cluster. They claim 57.5 TOPS/W and 1.52 Mparam/mm² (macro-level, best-case GEMM, 4-bit-equivalent weights). The SmolLM-135M speedups are modelled on a hypothetical larger config, not measured on silicon. Non-spiking; it competes for the same edge-inference socket as neuromorphic hardware.

## Device / chip

Embedded PCM (ePCM; PCM = a cell whose resistance is set by amorphous/crystalline phase) in STMicroelectronics 28nm FD-SOI CMOS. Each weight is **2T2R** (two PCM cells encode the sign), 8 storage levels, **4-bit effective weight** (ENOB = 4). The macro was previously presented by Pasotti et al. (ESSERC 2025). It stores 8 alternative "scenarios" (layers) of a 512×512 matrix-vector multiply (MVM), 2M signed 4-bit weights total.

Compute: inputs are encoded as time intervals on wordlines; bitline voltage regulators counter PCM I-V non-linearity; currents are integrated and digitized by current-controlled-oscillator ADCs. An on-chip 32-bit MCU handles programming and calibration. Drift is handled by on-chip current-induced annealing (Antolini et al., IEEE TED 2025), which also supplies the noise model used in simulation.

Single supply: 0.80–0.90 V for the PCM macro, 0.55–0.90 V digital. Die 3.38 × 3.38 mm (~14.1 mm² SoC); heterogeneous-compute domain 6.1 mm²; PCM macro 1.34 mm². The PCM is in the actual SoC in ST's embedded process, not a stacked or BEOL add-on demo.

## Workload

Not spiking. Transformer / small-language-model (SLM) inference accelerator: prefill is GEMM, decode is MVM. Alongside the PCM macro sit an 8-core FlexV RISC-V cluster and a Softex softmax/GeLU accelerator. The target model is SmolLM-135M (one layer, 3.54×10⁶ params, sequence length 2048), evaluated on **MEGATRON-XL**, a hypothetical config with two multiplexed PCM macros and 8 MiB L2. This is a model, not silicon.

## Measured numbers

All silicon measurements at 25 °C, prototype test chip on a carrier board, FPGA-controlled. Digital blocks characterised by voltage/frequency sweep.

- **Density:** 1.49 Mparam/mm² (macro 1.34 mm²); headline 1.52 Mparam/mm² (comparison table uses 1.38 mm² AIMC area). The 1.49 vs 1.52 gap is unexplained (area definitions differ). 4-bit-equivalent.
- **PCM macro with digital interface** (8b input, 4b analog weight, 8b output; swept over 25/50/75% of max conductance and utilization): MVM 868 GOPS at 18.9 TOPS/W; **GEMM 2.64 TOPS at 57.5 TOPS/W**; 1.88 TOPS/mm².
- **Peak binary-equivalent** (scaled to 1b×1b): 83.2 TOPS, 1840 TOPS/W, 60.16 TOPS/mm².
- **Power:** 2–25 mW digital, 68 mW analog macro.
- **FlexV RISC-V:** up to 3.5 TOPS/W at 0.55 V (4×4-bit); 46 GOPS at 1.84 TOPS/W at 0.90 V; 480 MHz max at 0.90 V, 100 MHz at 0.55 V. The 8b×8b figure is 0.02 TOPS, 1.64 TOPS/W.
- **Softex:** up to 560 Mtoken/s; 25 Gtoken/s/W at 0.90 V, 63 Gtoken/s/W at 0.55 V (convention: 1 OP/token for softmax).
- **Not reported:** endurance, retention, drift over time on this chip, array-level variability or conductance linearity, temperature dependence (25 °C only), measured accuracy of any network on silicon, ADC power breakdown.

**Modelled, not measured** (SmolLM one layer on MEGATRON-XL; off-chip modelled as LPDDR6 at 60 GB/s, 5 pJ/bit): prefill ~60× speedup on static-weight layers; ~2.5× per-layer with Softex (~14× on nonlinearities); decode ~3.3× time/token; ~10.5× energy efficiency overall in the decode-dominated case. Accuracy is PyTorch (transformers + brevitas) W4A8 plus PCM-characterised noise on WinoGrande, HellaSwag, ARC-Challenge, with "no significant degradation" claimed. Exact numbers appear only in a figure, not in the text, and nothing was run on-chip.

## Baseline and comparison honesty

- **57.5 TOPS/W boundary.** Called "system-level" on linear layers by the authors, but it is the PCM macro plus digital interface at best-case GEMM utilization, 8b/4b/8b, no sparsity. It excludes any end-to-end LLM run and gives no ADC power breakdown. Single chip, measured; best read as macro-level.
- **SmolLM speedups are against the chip's own 8-core RISC-V cluster** (~20 GOPS-class) with weights streamed from LPDDR6. They are not against a GPU, NPU or commercial edge SoC, so the baseline is favourable.
- **One layer only.** The full 135M-parameter model is ~40× the capacity of one chip. "Fully on-chip SLM" is extrapolation, and MEGATRON-XL does not exist.
- **Prior-art comparison table mixes normalisations.** Binary-equivalent (1b×1b) scaling and mismatched node/precision are mixed. Peak 1840 TOPS/W is below ISSCC26 ReRAM (7219) and Diana (4200), and similar to ISSCC22 PCM (1436); "comparable energy efficiency" holds only after scaling, and the authors concede Diana is higher. They also note the ReRAM and PCM CiM-only chips benefit from 55% input sparsity, which MEGATRON does not assume.
- **Density claims** (2.44× vs ReRAM, 27.4× vs PCM, 32.3× vs Hermes) use 4-bit-equivalent normalisation and some values "derived from provided data". The 1.52 Mparam/mm² counts the macro only; SoC-level density (14.1 mm²) would be far lower.
- **Hermes 5.5× energy-efficiency claim** compares against a 14nm 64-tile full chip (IBM) using a macro-level MEGATRON number.
- **30× / 13× vs near-memory SoCs** compares analog peak against a digital baseline; the authors note digital keeps an iso-accuracy advantage (analog is 4-bit ENOB with noise).

## Maturity

Integrated, silicon-measured prototype test chip (ST 28nm FD-SOI), not sampling and not a product. The LLM workload is simulated only. The macro itself is previously published (ESSERC 2025).

## Commercial signal

University of Bologna, Chips-IT (Italian RISC-V/chip-design centre), STMicroelectronics (fab and PCM technology owner) and University of Pavia. No funding, customer, product date or roadmap stated; evidenced: fabrication on ST 28nm; claimed: nothing about commercialisation. Wiki-external context, not stated in the source: ST ships ePCM in automotive MCUs. The source's intro contains a truncated sentence ("STMicroelectronics technology for Edge GenAI combining ..."), an extraction gap.

## Blockers stated

- **Capacity:** non-volatile PCM storage caps the deployable model (2M parameters per macro), forcing a larger MEGATRON-XL for even one SmolLM layer.
- **Analog accuracy:** fully digital accelerators retain an iso-accuracy advantage.
- **Integration and scaling:** system-level PCM integration was neglected in prior work (the paper's motivation); scaling to advanced nodes is called a challenge.
- **Unstated but visible:** no endurance, retention or drift data; 25 °C only; one supply shared with digital.

## Novelty

Recombination plus integration: ST's PCM analog-in-memory-compute macro (Pasotti, ESSERC 2025) embedded in a RISC-V SoC with the Softex accelerator, plus SLM-oriented system modelling. Closest priors are Hermes (Le Gallo, Nat. Electron. 2023, IBM 14nm 64-tile PCM), Khwa ISSCC22 (40nm 2M-cell PCM CiM) and Diana (ISSCC22). New is high multilevel density in a 28nm production-grade embedded PCM, plus the system-level LLM decode analysis.

## Reproducibility

No code, weights or data release mentioned; closed silicon. The simulation uses a public stack (transformers, brevitas), but the noise model comes from Antolini et al. and is not released here.

## Wiki tensions

No direct contradiction with existing claims. [[../devices/memristor-array-integration-gap]] argues ADC/DAC dominate system power and device numbers do not survive to system level. This source reports 57.5 TOPS/W at macro-plus-digital-interface level with CCO ADCs but no ADC breakdown, so it neither confirms nor refutes. It is candidate evidence for the foundry gate in [[../devices/cmos-rram-beol-integration]]: PCM already sits in a commercial foundry process.

## Source

- `raw/research/weekly-2026-10-01/01-megatron-pcm-cim-soc.md` — "MEGATRON: a 28nm Analog PCM CiM/Digital System-on-Chip for Edge GenAI at 57.5 TOPS/W and 1.52 Mparam/mm2" (arXiv 2609.35254). Primary, academic/industry.

## Related

- [[../devices/memristor-array-integration-gap]] — measured integrated PCM chip with ADCs; no ADC power breakdown
- [[../devices/cmos-rram-beol-integration]] — PCM embedded in a commercial foundry (ST 28nm FD-SOI) process
- [[../devices/memristor-device-engineering]] — PCM (2T2R, 8 levels, 4-bit ENOB, drift annealing) as a non-RRAM device data point
- [[../devices/analog-training-nonidealities]] — inference-only here; noise-aware quantisation, no training
- [[ethereal-event-gnn-processor]] — 28nm academic silicon with a simulated-not-measured accuracy claim
- [[../players/ibm-northpole]] — LLM-class edge inference with weights on-chip; NorthPole digital, this analog PCM
- [[../snn/snn-energy-breakeven-conditions]] — non-spiking analog-CiM competitor that sets an energy/density bar for SNN hardware
- [[../viability-ledger]] — PCM analog-CiM row candidate
- [[../players/roster]] — STMicroelectronics / Chips-IT / Univ. Bologna as PCM CiM players
- [[../benchmarks/neurobench]] — headline TOPS/W with idiosyncratic boundaries, not NeuroBench-style
