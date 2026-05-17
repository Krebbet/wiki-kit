# Neuromorphic Materials for Drone AI

Memristive and analog non-volatile devices promise in-memory compute that eliminates the von Neumann memory-bandwidth energy penalty. Device-level benchmarks reach sub-fJ synaptic energies. **Honest verdict: TRL 2–3 for any drone deployment; 5–10+ year horizon. Not a near-term lever — use [[nano-drone-compute]] or [[neuromorphic-computing-for-drones]] for actionable SWaP reduction today.**

---

## Why It Could Matter

Standard digital inference on MCU/NPU silicon pays a recurring energy tax moving weights and activations between memory and compute (von Neumann bottleneck). In-memory compute on a memristor crossbar performs MAC operations where data sits, cutting that traffic to near-zero in principle. For [[drone-power-budget]]-constrained platforms where inference energy dominates, this is the theoretical draw.

---

## Device Families (materials layer)

All figures below are **device-level bench measurements** — not system-level inference energy. Flag accordingly when citing.

| Family | Representative material | Best synaptic energy | Status |
|---|---|---|---|
| RRAM / ReRAM (filamentary) | HfAlOx, binary oxides, perovskites, 2D h-BN / MoS₂, organics | **4.28 aJ** (HfAlOx RRAM) | Lab / early prototype |
| PCRAM (phase-change) | GST chalcogenide; superlattice variant | — (superlattice: 25–30× power cut vs bulk GST) | Partially commercialised (embedded cache); NOT in neuromorphic weight arrays |
| MRAM / STT / SOT | CoFeB/MgO MTJ | — | Partially commercialised (cache/SRAM replacement) |
| Ferroelectric FTJ | HfZrO₂ | — | CMOS-compatible process; research stage |

Biological synapse baseline: ~10 fJ. The headline 4.28 aJ figure (HfAlOx) is >2,000× below biology — at device level only; ADC/DAC peripherals and crossbar parasitic losses consume the headroom at system level.

A NbO₂ neural circuit demo on a robot obstacle-avoidance task showed >50× latency reduction and ~5% of GPU power. A 5-layer memristor CNN demonstrated ~2 orders of magnitude less energy than GPU on MNIST. Both are narrow, controlled benchmarks with no generalisation to aerial perception. [Source: `10-memristor-materials-review.md`]

---

## Architectures and Demonstrated Tasks (system layer)

ANN, CNN, RNN, BNN, and SNN topologies have been mapped onto 1T1R and 1S1R memristor crossbars using STDP and supervised learning rules. Demonstrated tasks:

- MNIST digit classification
- Binary image classification
- Pavlovian conditioning

**All toy-scale. No drone perception, navigation, or control task has been demonstrated on a memristor system.** Per-spike energy figures: <30 aJ on MoS₂ optoelectronic synapses, <200 fJ on BN flexible devices — again device-level.

Photonic memristive integration (Taichi chip): 160 TOPS/W claimed, optical domain. Early research context.

System / chip TRL: 3–4. Drone-deployable TRL: 2–3. [Source: `11-memristor-ann-edge.md`]

---

## Commercial and Fab Status

Partial milestones exist but none support neuromorphic weight-array production:

- **Knowm** — commercial memristor devices, research-oriented
- **Crossbar Inc.** — RRAM DNN accelerator, embedded storage focus
- **Tsinghua** — integrated memristor CNN chip (research fab)
- PCRAM and STT-MRAM are in volume production as cache/SRAM replacements, not as analog synaptic arrays

Critical blockers for fabbing neuromorphic arrays:

1. No PDK or EDA models for memristor devices — standard chip design flows do not support them
2. CMOS back-end integration unsolved: memristive material deposition temperatures are thermally incompatible with standard BEOL
3. No production process design kit = no fabless path

---

## Why Not Near-Term for Drones

Even if device physics were production-ready today, drone deployment would still face:

| Problem | Detail |
|---|---|
| Device variability | Cycle-to-cycle and device-to-device stochasticity degrades inference accuracy; requires compensation circuits |
| PCRAM drift | Resistance state drifts post-write; problematic for stored weights |
| Crossbar sneak paths | Off-state leakage through unselected cells; requires 1S1R selectors, adding area and process steps |
| ADC/DAC overhead | Analog crossbar outputs must be digitised; peripheral CMOS can dominate system energy, erasing device-level gains |
| Endurance | Filamentary RRAM endurance (10⁶–10⁸ cycles) lags SRAM; write-heavy online learning stresses this |
| No SWaP qualification | Zero published data on vibration, thermal cycling, or altitude-pressure effects on device retention |
| Toolchain absence | No compiler, scheduler, or mapping tool targets memristor crossbars for real inference workloads |
| Task gap | All demos are toy datasets; object detection, optical flow, or SLAM on memristor hardware — not demonstrated |

**TRL 2–3. Realistic drone-relevant deployment: 5–10+ years, contingent on solving CMOS integration and toolchain gaps.** For actionable energy reduction today, see [[nano-drone-compute]] (low-power MCU/NPU silicon) and [[neuromorphic-computing-for-drones]] (Intel Loihi 2, SpiNNaker — chip-level, not material-level).

---

## Source

- `raw/research/onboard-ai-energy/10-memristor-materials-review.md` — PMC 2025 review of RRAM, PCRAM, MRAM, FTJ device families; device-level energy benchmarks; NbO₂ robot demo; materials/process maturity assessment
- `raw/research/onboard-ai-energy/11-memristor-ann-edge.md` — PMC 2026 review of ANN/CNN/RNN/BNN/SNN on memristor crossbars; demonstrated tasks; commercial players; CMOS integration barriers; system TRL assessment

---

## Related

- [[drone-power-budget]] — the SWaP constraint that makes in-memory compute attractive in principle
- [[neuromorphic-computing-for-drones]] — chip-level neuromorphic (Loihi 2, SpiNNaker); deployable today vs materials-layer TRL 2–3
- [[nano-drone-compute]] — the actual near-term path: low-power MCU/NPU silicon (Hailo, Kneron, GAP9)
- [[drone-autonomy-state]] — operational context; highlights the gap between lab demos and flight-ready autonomy
