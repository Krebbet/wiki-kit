# Hafnia BEOL synaptic weights on commercial XFAB XP018 CMOS

ETH Zurich (Integrated Systems Laboratory) post-process two-terminal ferroelectric hafnia synaptic weights (W/TiN/WOx/[HfO2-ZrO2]/Mo) into the back-end-of-line (BEOL, the metal/dielectric layers above the transistors) of as-delivered commercial XFAB XP018 180 nm CMOS dies. Evidence is single-device analog potentiation/depression (LTP/LTD, gradual conductance increase/decrease under pulses) on test structures, plus NMOS that still work after a 500 °C anneal. The system-level result (anneal temperature changes MNIST accuracy under plain SGD) is software-only simulation. No 1T-1R cell, no array, no on-silicon training.

## Device

- Stack, top to bottom: 20 nm DC-sputtered W / 3 nm ALD TiN / 2 nm WOx (45 PEALD cycles at 360 °C) / 5 nm [HfO2-ZrO2]x5 multilayer ("HZO-ML", PEALD at 300 °C, five supercycles) / 20 nm sputtered Mo bottom electrode. ALD layers deposited without breaking vacuum.
- Two-terminal ferroelectric resistive synapse (not a FeFET, not yet 1T-1R). Conductance is set by the fraction of ferroelectric domains polarised toward a given electrode.
- Host: as-delivered XP018 dies; AlCu pads exposed through 2 µm SiN passivation, 200 nm RF-sputtered SiO2 isolation, contacts via post-process vias and 150 nm W metallisation. Optical lithography throughout; no foundry engineering run.
- Crystallisation by rapid thermal anneal (RTA): 60 s in Ar, 30 °C/s ramp, at 450 °C or 500 °C. The anneal is the BEOL bottleneck (thinner films need more thermal budget); the source says 500 °C conventionally exceeds the BEOL budget and treats it as an explored parameter. 180 nm was chosen for robustness to high temperature.
- Test structures: synapses of 2000-5000 µm²; NMOS of W/L = 0.22/0.18, 0.5/0.18, 2/2 µm.
- The weight update likely mixes domain reversal with charge trapping and ionic redistribution (source's own caveat), so it is not purely ferroelectric.

## Measured numbers

All single-device or single-transistor. Evidenced unless marked.

NMOS after full processing with the 500 °C anneal (Vd = 1.8 V; one reference die vs two processed dies P1, P2):
- Off-state drain current at Vg = 0 at or below the 20 pA measurement floor, no increase resolved vs reference.
- 0.22/0.18 µm: Vth 394 mV (ref), 421 (P1), 453 (P2); SS (subthreshold swing) 83/89/86 mV/dec; Id,sat 115.2/107.9/112.5 µA.
- 0.5/0.18 µm: Vth 507/531/516 mV; Id,sat 198.0/187.9/188.6 µA.
- 2/2 µm: Vth 584/588/588 mV; Id,sat 98.4/99.0/100.3 µA (under 2 % change).
- Short-channel devices: Id,sat down 6 %, Vth up by up to 60 mV. Reference die-to-die spread was not measured, so these shifts cannot be separated from natural spread (source acknowledges).

Synapses, 450 °C (read at -0.5 V after a 500 µs write pulse):
- Write window -1.6 V to 1.2 V (25 mV amplitude-incremented ramp); abstract says "below 1.8 V".
- Wake-up (field cycling that opens the usable window): 1000 cycles on one device; dynamic range up 3x, median cycle-to-cycle variability 5 % to 1.5 % of the window.
- Device-to-device variability 1.8 % (5000 µm² devices).
- Cycle-to-cycle variability: three discrepant figures in the source, not reconciled. Body Section III.D: below 1 % over four consecutive cycles. Abstract: "below 3 %". Source summary: "below 1.5 %" (matches the post-wake-up median). Treat the headline as imprecise, roughly 1-3 % depending on boundary.
- Relaxation (read at -0.5 V, 3 devices, 2 h): LRS and HRS drift toward each other by 7.5 ± 0.4 % and 9.5 ± 0.6 %. Only 2 h measured.
- Ferroelectric evidence: non-switching current density independent of area; rectification ratio 9 at ±1 V; PUND (positive-up-negative-down pulse test of remanent polarisation) at 100 kHz, 8-cycle average, one device: 2Pr = 22.1 µC/cm²; 1/|Vc| linear in log(t_write) over 500 ns-500 µs, consistent with the Merz law (coercive voltage vs pulse width).
- Loop offset -0.4 V between branch centres, independent of pulse width. Peak LTP/LTD slope (normalised conductance change per normalised pulse) 4.5-5.4, similar to the group's prior work [9].

Synapses, 500 °C (one chip):
- Loop offset -0.1 V; write window 2.8 V narrows to 2.4 V (-1.2 V to 1.2 V); cycle-to-cycle variation 2.3 % over 4 cycles; peak slope below 3 (about half the 450 °C value).

Simulation, software-only (IBM AIHWKit, PiecewiseStepDevice fitted to measured LTP/LTD; MLP 784-256-128-10, MNIST, batch 64, lr 0.5, 50 epochs, 3 seeds). Not on-device training:
- MP-SGD (mixed-precision, digital accumulator), real device parameters: 97.0 ± 0.1 % at both 450 and 500 °C.
- Plain analog SGD, ideal parameters: 80.0 ± 1.7 % (450 °C) vs 87.0 ± 0.2 % (500 °C), a 7-point gap.
- Plain SGD, real parameters: 69.0 ± 1.7 % vs 82.0 ± 2.9 %, a 13-point gap.
- Variability parameters were identical for both chips (dw_min_std 0.041, dw_min_dtod 0.494), so only update-curve shape differs.

Not reported: endurance beyond 1000 cycles, retention beyond 2 h, array data, energy per operation, speed outside 500 ns-500 µs, on/off ratio (rectification ratio 9 is the only ratio), temperature dependence.

## Baseline and comparison honesty

- Every system-level number is simulated from a piecewise fit to single-device curves; nothing was trained on silicon.
- Equal simulation parameters across anneals isolate curve shape but ignore the measured variability difference (2.3 % vs about 1-1.5 % cycle-to-cycle).
- 450 vs 500 °C is one chip each; N = 3 for retention, 1 for PUND and wake-up.
- NMOS compatibility rests on two processed dies and one reference die per geometry, on test structures separate from the ferroelectric devices. No die shows a synapse and its own NMOS measured together.
- 180 nm AlCu BEOL tolerates heat far better than advanced nodes, so the 500 °C result does not transfer to scaled nodes (source says this motivated the node choice).
- Comparison to prior work [9] is limited to peak-slope similarity.

## Maturity

Single-device, on test structures 2000-5000 µm², much larger than a realistic synapse. NMOS survive on the same die. No 1T-1R cell, no array, not a foundry-integrated process. Source lists 1T-1R characterisation as future work.

## Commercial signal

None in the source: no customers, dates or commercial players beyond the foundry (XFAB XP018; wafer and chip design supplied by Prof. Erika Covi and Bojian Zhang). Funding (acknowledgments): SNSF Starting Grant ROSUBIO (218438), Swiss SERI via SwissChips, Horizon Europe Chips JU via ViTFOX (101194368). Claimed positioning: commercial-CMOS post-processing avoids dedicated foundry engineering runs.

## Blockers

Stated by the source:
- 500 °C exceeds the conventional BEOL thermal budget.
- W/TiN electrodes (as in [9]) failed to show synaptic function on fully processed wafers; Mo plus a WOx interlayer was needed.
- Wake-up cycling required.
- Relaxation drift of 7.5-9.5 % in 2 h (possible ionic origin at Mo/WOx interfaces).
- Loop asymmetry (-0.4 V at 450 °C), possibly electrode work-function difference.
- Linearity, symmetry and retention must improve (e.g. work-function engineering) to close the plain-SGD vs MP-SGD gap.
- Microscopic origin of the 500 °C behaviour change is "not established".

(synthesis) Nothing here addresses array-level yield or scaling to realistic cell area; see [[memristor-array-integration-gap]].

## Novelty

Claimed first integration of two-terminal ferroelectric synaptic weights in the BEOL of as-delivered commercial 180 nm CMOS dies, with a new WOx/[HfO2-ZrO2] bilayer between TiN and Mo. Refines the group's earlier middle-of-line W-via integration on 180 nm [9] (Begon-Lours et al., Adv. Electron. Mater. 2024): post-processing on finished dies, and swapped electrodes. The source also cites BEOL FeFET at 22 nm [6] and ferroelectric capacitors at 130 nm [7] and 180 nm [8].

(synthesis) A ferroelectric counterpart to the RRAM rapid-prototyping route in [[cmos-rram-beol-integration]]; the simulated 69-87 % plain-SGD spread with curve shape supports the update-shape sensitivity theme in [[analog-training-nonidealities]].

## Reproducibility

No code, data or device files mentioned. AIHWKit is public and Table II parameters are listed, but the measured LTP/LTD curves behind the fit are not stated as released. Process steps carry thicknesses and temperatures, so fabrication is reproducible in principle. No independent reproduction.

## Source

- `raw/research/weekly-2026-10-29/01-hafnia-beol-cmos.md` — "Back-End-Of-Line Integration of 2-Terminal Ferroelectric Hafnia Synaptic Weights on Commercial CMOS Process", arXiv:2610.37530, ETH Zurich, v1 2026-10-27. Primary; peer-review status not established from the capture.

## Related

- [[cmos-rram-beol-integration]] — parallel BEOL post-processing on commercial 180 nm CMOS, RRAM instead of ferroelectric
- [[fefet-analog-imc]] — ferroelectric hafnia family; this is the two-terminal variant, with measured single-device data
- [[hzo-ferroelectric-capacitor-reliability]] — related 5 nm HZO film; this source has only 1000-cycle data
- [[analog-training-nonidealities]] — simulated SGD sensitivity to update-curve shape
- [[memristor-device-engineering]] — electrode and interlayer levers (Mo, WOx)
- [[memristor-array-integration-gap]] — small-area test structures only, no 1T-1R or array
- [[../conflicts/analog-onchip-training-viability]] — MP-SGD vs analog-SGD gap depends on update linearity
- [[../viability-ledger]] — ferroelectric hafnia BEOL status
- [[../weekly-briefs/2026-10-29]] — brought in by the 2026-10-29 weekly sweep
