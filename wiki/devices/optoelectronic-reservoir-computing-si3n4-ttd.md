# Optoelectronic reservoir computing with an on-chip true-time-delay (Si3N4)

A first for the wiki: delayed-feedback reservoir computing (DFRC), a physical-substrate computing paradigm distinct from spiking networks, gets its first entry here via a Ben-Gurion/Lancaster group paper (arXiv:2609.05907, Sep 2026) that replaces the fiber spool or FPGA digital buffer conventionally used to close a DFRC feedback loop with a foundry-fabricated silicon-nitride (Si3N4) true-time-delay (TTD) photonic chip. The reservoir still classifies and predicts correctly at a feedback gain **>40× below** prior optoelectronic reservoirs — the paper's central result — but this is a single delay-line device on a lab bench, not an integrated photonic system.

**Maturity ceiling, stated up front:** only the delay element is on-chip. The laser, modulator, EDFA, photodetector, and feedback electronics are discrete bench instruments coupled by fiber and free-space optics. No CMOS/BEOL integration, no packaging, no array or wafer-scale statement, no code/data release. Single foundry-fabricated PIC, academic funding only.

## Device / material

Si3N4-on-insulator photonic integrated circuit, fabricated on the **LIGENTEC AN350** multi-project-wafer platform (a real commercial MPW shuttle, not an in-house academic process) — the wiki's foundry-named angle for this entry. Eight cascaded Archimedean-spiral waveguides give ≈1.76 m of on-chip optical path (1 µm core, 350 nm guiding layer, TE mode at 1550 nm) on a single reticle, plus a 5 mm straight reference waveguide for calibration.

This is a **passive, nonresonant true-time-delay** element — delay comes from modal group-velocity propagation, not a resonant or slow-light structure, giving broadband phase linearity. Everything else in the system — CW laser, EDFA, Mach–Zehnder intensity modulator (Thorlabs LN81S-FC), photodetector, FPGA-based masking/readout (Moku:Go) — is discrete lab equipment, not integrated with the delay chip.

## Measured numbers

All experimental unless marked calculated; boundary is single-device, bench-level throughout.

- **Delay:** calculated passive group delay 11.63 ns (1.45 ns/spiral) at group index n_g = 1.981. Using the effective index instead of the group index would underestimate this by ~19% — a stated methodology point.
- **Loss:** ≈23.2 dB spiral excess loss (first-generation layout), 2.0 dB/ns loss-per-delay figure of merit. The paper names this its principal engineering blocker.
- **Loop gain:** G = 0.0223 with the chip in the loop — stated as >40× below the G≈1 regime of the founding optoelectronic-DFRC papers (Paquot 2012, Larger 2012) and 23× below the same group's own prior FPGA-delay work (Morozko et al. 2025, G≈0.52).
- **Waveform classification** (sine vs. square): WER = 0 across all 5 folds; best-fold NMSE = 0.074, mean NMSE = 0.0913.
- **Subcarrier phase encoding** (a device-specific variant exploiting the waveguide's true optical phase, not possible with a digital delay buffer): best-fold NMSE = 0.0767, mean NMSE = 0.0992, WER = 0.
- **Japanese Vowels** 9-class speaker classification: WER = 0.0898, NMSE = 0.3778 (experimental); matched noise-free simulation WER = 0.0670 — a ~2.3-point experimental-vs-simulation gap attributed to hardware noise.
- **Mackey–Glass** one-step prediction: best-fold NMSE = 0.0082, mean NMSE = 0.0112 — described by the authors as "within ~8%" of Paquot et al. 2012's fiber-spool result (NMSE 0.0076).

## Algorithm / workload

Classic delayed-feedback reservoir computing (Appeltant 2011 / Paquot 2012 / Larger 2012 lineage): one physical nonlinear node (the modulator) is expanded into an N-dimensional virtual reservoir by time-multiplexing the feedback delay loop. Only the linear readout is trained (ridge regression); hyperparameters were tuned via Bayesian search (TPE) run directly on the hardware. Four benchmark tasks, none drawn from [[../benchmarks/neurobench]] or any spiking-network suite: binary waveform classification, the phase-encoding variant, Japanese Vowels speaker classification, and Mackey–Glass chaotic-series prediction.

## Baseline and comparison honesty

Mixed, and worth flagging rather than repeating the paper's framing uncritically. The paper is upfront and repeated about the central handicap (G=0.0223, "40× below" the comparison baselines) — that's good practice. But the headline "within 8%" / "less than half the WER" comparisons are each against **different apparatus and, in two of three cases, a different research group** (fiber spool, FPGA digital delay, speckle plate) — not a controlled ablation of the TTD chip against an equivalent delay technology on the same setup. The two headline comparisons also use best-fold numbers against a single external figure whose own fold statistics aren't reproduced, while mean-fold numbers are reported alongside but not used in the comparison sentence. None of this is independently checkable — see Reproducibility.

## Maturity

Single foundry-fabricated PIC (the delay element only) inside a discrete-component bench system. Not an integrated photonic chip, not an array, no packaging, no yield/wafer statement. Explicitly first-generation; the paper's own next step is a lower-loss "more-integrated" second-generation device, not a named process or foundry migration. Earliest rung on this wiki's maturity ladder: single device, bench demonstration.

## Commercial signal

None beyond the foundry used. LIGENTEC SA is named as the MPW platform (AN350) that fabricated the chip — a commodity shuttle run, not a reservoir-computing-specific partnership. Funding is an Israel Science Foundation grant. No companies, customers, or availability dates.

## Blockers stated

- **23.2 dB excess insertion loss** in the spiral delay line — named explicitly as the principal engineering objective for the next generation, and the direct cause of the low feedback gain.
- Phase-comparison metrology was limited by residual electrical pickup below the noise floor after attenuation — the delay value's consistency check comes from the reservoir experiment itself, not independent metrology.
- **Code and data are not public** — "may be obtained from the corresponding author upon reasonable request."
- Not integrated with the laser, modulator, or detector — full photonic integration is future work.

## Novelty

Refinement of an established sub-field, not a new mechanism: Archimedean-spiral Si3N4 TTD layouts were already established by this group's own prior work. The genuine new contribution is applying a foundry-fabricated TTD chip inside a reservoir-computing feedback loop (succeeding the same group's 2025 FPGA-digital-delay version) and demonstrating a **phase-encoding scheme** that only a physical waveguide — not a digital buffer — can support, since it exploits true accumulated optical phase rather than stored amplitude samples.

## Reproducibility

Closed. Code and data are explicitly not publicly available; no dataset or reservoir-state matrices released, no independent replication.

## Source

- `raw/research/weekly-2026-09-17/03-optoelectronic-reservoir-computing.md` — Murad, Watad, Karabchevsky, "Optoelectronic Reservoir Computing with an On-Chip True-Time-Delay Element," arXiv:2609.05907, submitted 5 Sep 2026. Primary, academic preprint.

## Related

- [[optoelectronic-rram-photonic-programming]] — a **different** technology despite the shared "optoelectronic" label: that page is memristive RRAM written by light (stored conductance state); this page is a passive delay-line property inside a reservoir-computing loop (no memristive element). Related by photonic substrate, not by mechanism — do not conflate.
- [[../benchmarks/neurobench]] — a contrast case: this source's four benchmarks are legacy reservoir-computing tasks compared informally across different papers' apparatus, exactly the measurement-boundary problem NeuroBench exists to close.
- [[../weekly-briefs/2026-09-17]] — brought in by the 2026-09-17 weekly sweep
