# Optoelectronic RRAM: photonic programming of memristive arrays

A distinct programming modality from everything else on [[memristor-device-engineering]]: instead of writing a resistive-switching cell with a voltage pulse, an optoelectronic RRAM (ORRAM) device is written with light. The wiki's first source on this axis is a Strathclyde/Edinburgh academic device paper (arXiv, 2026-08-17) demonstrating a 32-device IGZO-based ORRAM array optically SET by a bump-bonded µLED array and electrically RESET, including a small-scale parallel-programming demo and a toy temporal-encoding task. Two independent watched sources (arXiv direct, Semiconductor Engineering relay) surfaced this the same week.

**Maturity ceiling, stated up front:** 32 stand-alone devices on a chip, 4 programmed in parallel via free-space optics, no crossbar interconnect, no CMOS-integrated ORRAM (only the µLED driver is CMOS), no foundry, no endurance or retention data, no energy-per-operation figure, purely academic (UK/EU public funding). This is a mechanism demonstration, not a system.

## Device / material

Two-terminal metal-insulator-metal stack: Ti(5nm)/Pt(12nm) bottom electrode, a dual-stack active layer of 12.5nm oxygen-rich IGZO on 12.5nm IGZO (both RF-sputtered from an InGaZnO₄ target), ITO(20nm)/Ti(5nm)/Pt(50nm) top electrode, on 200nm thermal SiO₂ over a 150mm p-type Si wafer. 32 stand-alone devices per chip; active areas from 60×60 µm² down to 1 µm² are offered by the mask, though the tested devices are the larger option. Two anneal variants: non-annealed (higher optical sensitivity) and 350°C/60min-annealed (lower intrinsic resistance, lower optical sensitivity). Switching is **electroforming-free**.

**Switching mechanism** is the genuinely distinct part: photoionization of oxygen vacancies at an oxygen-deficient/oxygen-rich IGZO homojunction modulates a tunnelling barrier width. This is neither filamentary ion migration (RRAM) nor a phase transition (PCM) — it's an optical/electronic-trap mechanism.

**Optical source:** a bespoke GaN µLED array (40×10 pixels, 80×80 µm each, 100 µm pitch, 450nm), flip-chip bump-bonded to a custom CMOS driver chip programmed via FPGA. The CMOS integration is on the **µLED driver only** — the ORRAM array itself sits on a plain Si/SiO₂ die, and the two are coupled via free-space optics (lenses, beamsplitter, microscope objective), not monolithically stacked or co-packaged.

No foundry or BEOL integration path is stated; fabrication is a university cleanroom process.

## Measured numbers

All device-level, single-chip; no array-wide statistics beyond the 4-device parallel test below.

- Resistance range: up to 10¹⁰ Ω in I-V sweeps, exceeding the measurement instrument's resolution (device-level).
- Electrical WRITE: 100 excitation + 200 read pulses; recovery to near-initial resistance in ~0.1s (volatile, short-term).
- Optical WRITE: 60 excitation + 400 read pulses; optical power densities 53.1–1156 mW/cm²; conductance change up to 0.2 µS, >55% relative resistance change from a single µLED. Recovery is >250s and **incomplete** within that window — optical fading memory persists roughly **2500× longer** than the electrical relaxation.
- Optical-SET / electrical-RESET: 200 electrical RESET pulses recover 80% of initial resistance in 10s; full recovery not achieved with the tested parameters.
- Toy 4-bit temporal-pattern encoding (single device, self-defined task, not a benchmark): 87.5% classification accuracy (14 of 16 patterns distinguished); read-noise ±0.35% std dev; extrapolated (not demonstrated) to ~6-bit / ~85-state capacity.
- Parallel programming, 4 devices under identical nominal optical stimulus: resistance changes of −33.3%, −46.9%, −61.5%, −25.6%. **This spread is attributed by the authors to free-space optical misalignment (off-axis µLEDs losing ~75% power), not intrinsic device-to-device variability** — it is not a σ/µ figure comparable to the D2D numbers on [[memristor-device-engineering]].
- No endurance (cycles-to-failure), no long-term temperature-controlled retention, no energy-per-operation (J/pulse), no chip- or system-level power figure. The authors report none of these — an explicit gap, not an omission of the summary.

## Baseline and comparison honesty

No quantified comparison against other RRAM technologies, GPUs, or prior ORRAM work. The paper extends a cited prior optical SET/RESET result (Hu et al. 2021) to spatially-multiplexed parallel programming, but doesn't re-run or numerically benchmark against it. The 4-device variability spread is honestly attributed to setup optics rather than claimed as a device metric — good practice, but it also means no clean array-level variability statistic exists for this device family yet.

## Novelty

Refinement/recombination, not a new switching mechanism — the IGZO ORRAM material system and optical SET/electrical RESET behavior were already reported. The new contribution is systems-level: pairing a CMOS-bump-bonded GaN µLED array (adapted from the same group's display/optical-wireless-comms work) with the ORRAM array to achieve simultaneous, spatially-multiplexed, crosstalk-free parallel optical programming of multiple independent devices, plus a first demonstration of fading-memory-based temporal bit-pattern encoding on this platform.

## Reproducibility

Raw electrical/optical trace data openly deposited (University of Strathclyde KnowledgeBase, DOI 10.15129/6e778ca4-f780-4681-a877-97c1a8793c05). No code/weights to release — no ML training occurred. Fabrication and setup are documented in enough procedural detail for expert replication, but this is not a released hardware/software toolchain.

## Commercial signal

None. Academic-only: University of Strathclyde (Institute of Photonics) and University of Edinburgh (Institute for Integrated Micro and Nano Systems), funded by UK EPSRC, EU Pathfinder Open, UK Multidisciplinary Centre for Neuromorphic Computing, and UKRI IKC in Neuromorphic Hardware. No company, funding round, design win, or availability date of any kind.

## Blockers stated

- The free-space optical setup does not scale as-is; the authors flag that array-to-array coupling needs co-designed µLED pitch and optical magnification matched to the ORRAM array pitch beyond the demonstrated 4 parallel channels.
- Off-axis µLEDs suffer distortion and ~75% optical power loss versus on-axis devices, directly degrading programming uniformity.
- Electrical RESET does not fully restore initial resistance with tested parameters.
- Instrumentation resolution limits measurement above ~10¹⁰ Ω and contributes enough read noise that 2 of 16 temporal patterns are indistinguishable.
- No endurance or retention characterization was performed at all.

## Source

- `raw/research/weekly-2026-08-27/01-optoelectronic-igzo-rram-uled.md` — Adair, Robertson et al., "Parallel Spatial Photonic Programming of Optoelectronic IGZO RRAM with a compact µLED Array", arXiv:2608.16807, posted 2026-08-17. Primary, academic preprint.

## Related

- [[memristor-device-engineering]] — the material-family and switching-mechanism landscape this device extends with an optically-programmed category; its comparison table has no equivalent row for this device given the missing endurance/retention/energy data
- [[memristor-array-integration-gap]] — parallels the CMOS-integration question from the opposite direction: here the µLED *driver* is CMOS-integrated while the ORRAM itself is not, adding an optical-alignment integration boundary on top of the existing ADC/DAC gap
- [[event-cameras]] — the optical-*sensing* counterpart; this device is optical-*writing*, and the source explicitly motivates ORRAM as bringing memristive technology into applications that sense and process in the optical domain
- [[../weekly-briefs/2026-08-27]] — brought in by the 2026-08-27 weekly sweep
