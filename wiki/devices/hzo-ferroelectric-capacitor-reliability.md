# HZO ferroelectric capacitor reliability: access-rate-dependent endurance

NaMLab (TU Dresden, with Intel Foundry and other coauthors) show that switched-polarization loss in 5 nm Hf₀.₅Zr₀.₅O₂ (HZO) capacitors grows with the delay between pulses, not just with cycle count. They attribute it to electron transfer from oxygen-vacancy defects to the TiN electrode, which raises local switching thresholds (nucleation-limited switching). **Single stack, single capacitor per test, lab process**: this is FeRAM-type capacitor data, not FeFET data, and it is the wiki's only measured reliability evidence for ferroelectric HZO.

## Device

10 nm TiN / 5 nm HZO (ALD 300 °C) / 10 nm TiN on W/p-Si, 500 °C RTA, area ≈1963 µm². TiOxN1-x interfacial layers form at both electrodes; oxygen scavenging creates vacancies at the interface. Orthorhombic vs tetragonal phase is unresolved by GIXRD. No node, fab or BEOL process; the "product-relevant" framing rests only on the 5 nm thickness (the Micron 2023 IEDM FeRAM is cited as background, a claim not evidenced here).

## Measured (device level, ±2 V, 5 µs pulses)

- Remanent polarization 19.3 µC/cm² after 2·10⁶ bipolar cycles. Wake-up completes by ≈10⁴ cycles regardless of delay (200 ns–200 µs), Δ2Pr rising by at most 10–12 µC/cm².
- Polarization loss after wake-up is larger at longer delay (200 ns → 2 ms at room temperature). Unipolar non-switching cycling shifts coercive field without 2Pr loss; bipolar cycling gives 2Pr loss without a peak shift, so internal bias alone does not explain it. Values are figure-only.
- Temperature 25–135 °C at 2 ms delay: fitted τ₀ falls 111 → 53 ns; activation energy 0.09 eV (low T) / 0.04 eV (high T), far below the 0.5–1.2 eV cited for vacancy migration, hence the electron-transfer interpretation. Prior Micron work reports 0.2 eV.
- Model: Δ2Pr(N) = −α²·ln(N^β/τ₀)², α and β fixed, only τ₀ fitted per condition.

## Caveats

- The 10¹⁰-cycle figure is a model extrapolation, not a measurement; α and β are stack-dependent.
- The 200 ns and 2 µs fits are unconstrained (authors call them "purely indicative"; no loss observed there).
- The model does not reproduce the reduced degradation at extreme access rates reported by Micron; the authors attribute it to wake-up their capacitors lack.
- Delays above 2 ms and temperatures above 135 °C untested; no retention, array, variability, energy or speed data.
- Ab initio vacancy diffusion coefficients exceed experimental ones (acknowledged).

## Why it matters here

(synthesis) [[fefet-analog-imc]] reports no measured endurance or retention; this page supplies the mechanism-level reason ferroelectric endurance claims need an access-pattern boundary. Cycle-count-only endurance, as in separate endurance/retention tests, overstates performance for workloads with long idle gaps. It does not bear on the open conflicts.

## Source

- `raw/research/weekly-2026-10-15/04-hzo-access-rate-endurance.md` — arXiv 2610.20154. Funding acknowledged includes DFG, Saxon State, Samsung and Intel. No code or data release stated.

## Related

- [[fefet-analog-imc]] — same material family, system-level simulation only
- [[memristor-device-engineering]] — endurance/interface levers for RRAM, for contrast
- [[memristor-array-integration-gap]] — device reliability not surviving to system level
- [[cmos-rram-beol-integration]] — contrast: this is not a BEOL process
- [[../viability-ledger]]
- [[../weekly-briefs/2026-10-15]] — brought in by the 2026-10-15 weekly sweep
