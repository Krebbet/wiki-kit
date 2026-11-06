# Multi-weight SOT domain-wall MTJ synapses on a 300 mm line

UT Austin + imec (arXiv 2611.08405, 2026-11-05, preprint) get up to 8 resistance levels from elongated spin-orbit-torque magnetic tunnel junctions fabricated on imec's 300 mm MRAM pilot line. **Evidenced (single-device probe-station data):** 8 states in the best device only, TMR cut to 30–45% (control 80%), no endurance or retention measured. **Simulated:** an MNIST crossbar scores 96.1% *if every device had 8 states*, but 48.6% (best case) with measured device-to-device spread. The 96.1 and 48.6 figures come from different configurations — not a clean before/after.

## Terms

- **MTJ:** two magnetic layers around a thin MgO barrier; low resistance when magnetisations are parallel, high when antiparallel. Normally bistable (1 bit).
- **SOT:** switching current runs in an adjacent heavy-metal track (β-W here), separating write and read paths.
- **DW (domain wall):** boundary between up/down regions in the free layer; its position gives intermediate resistance.
- **TMR:** (R_high − R_low)/R_low, the read window.

## Device

- Perpendicular SOT-MTJ, W(3.5 nm) track / CoFeB(0.9) / MgO / CoFeB(1.1)… with synthetic-antiferromagnet reference; top-pinned. imec 300 mm MRAM pilot line, PVD, 30 min 300 °C anneal in 1 T, 193 nm immersion litho + ion-beam etch, Cu dual-damascene electrodes on W-via bottoms. Process optimised for **conventional binary MRAM**; the authors blame it for the TMR loss in elongated pillars.
- Four configs × 32 devices on one wafer (stats on 20 each): control 60 nm circular (TMR 80.2%); L350 350×70 nm (44.8%); L400 400×90 nm (39.1%); L600 600×120 nm (30.5%). RA = 10.9 Ω·µm².
- **Mechanism (hypothesised, partly simulated):** a compensation voltage on the top electrode (50% of pulse amplitude) makes the junction voltage non-uniform in the ~5× elongated pillar; edge STT leakage nucleates a DW. Mumax3 shows *no domains* without the compensation drive — so multi-level behaviour depends on the drive scheme, not geometry alone.

## Measured (device level, room temperature)

- States: L400 reaches 8 in **one** device at 0 Oe in-plane field; each config ≥6 states in two devices at 50/0/−50 Oe; control stays at 2. "Up to eight" is a best-device maximum.
- Access is stochastic: complete-switch probability <20% near zero field (control ~50%); reaching a level needs write-verify, up to 25 cycles assumed.
- Write 10 ns / 1.5 pJ (L350, L400), 30 ns / 1.7 pJ (L600) per Table 2; text gives 1.47, 1.17 and 6.67 pJ per programming cycle — **unreconciled, energy boundary unstated** (device-level).
- Write noise 0.44–0.77%; D2D CoV 5.1–5.7% on the *binary endpoints only*.
- **Not measured:** endurance (the 10¹⁴ figure is a literature citation for generic MRAM), retention, drift, temperature dependence. No arrays, no peripherals.

## Simulated workload (CrossSim)

MNIST inference with a small pretrained CNN (unquantised 97.5%); differential bit-cell (two devices/weight); weights quantised to measured state counts. 96.1% = L400 with all devices assumed at 8 states, no variation (extrapolated from one device); L350 69.7% and L600 79.9% under the same assumption (≈6 states); 48.6% = best with-variation case (L350 at 50 Oe, from a supplementary sweep not in the capture). "Suitable for backprop training" is asserted, not shown.

## Assessment

(synthesis) The honest content is the variability result: even before peripherals, a 10-point-plus accuracy loss from device spread and 8-level access that only one device achieved. Competing analog devices (ECRAM, PCM, RRAM) show 12–128 states; the binary SOT-MRAM reference is faster and lower-noise. Value of the work: an MRAM-class stack with MRAM-class endurance *if* levels, read window and stochasticity are fixed — all open. Relates to the programming-asymmetry problem in [[analog-training-nonidealities]] and the lab-to-fab gap in [[memristor-array-integration-gap]]; the wiki's other spintronic page is [[vmtj-cmos-izhikevich-neuron]] (neuron side). Funding: imec MRAM industrial affiliation + NanoIC pilot line (consortium interest, no product). Data on request, no code.

## Source

- `raw/research/weekly-2026-11-05/02-dw-mtj-synapses.md` (arXiv 2611.08405)

## Related

- [[vmtj-cmos-izhikevich-neuron]]
- [[analog-training-nonidealities]]
- [[memristor-array-integration-gap]]
- [[memristor-device-engineering]]
- [[../conflicts/analog-onchip-training-viability]]
- [[../viability-ledger]]
- [[../players/roster]] — imec, UT Austin (Incorvia group)
- [[../weekly-briefs/2026-11-05]] — brought in by the 2026-11-05 weekly sweep
