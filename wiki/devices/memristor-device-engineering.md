# Memristor / RRAM device engineering

How a resistive-switching cell is made to behave: the material systems, the switching mechanisms, and the four engineering levers — doping, electrode choice, interface/barrier layers, and pulse protocol — that turn a lab curiosity into something with usable endurance, retention and analog resolution. Sourced from a 2026 open-access IOP review (~160 refs) whose organising argument is **co-design**: device-level optimisation and operation-level optimisation are usually pursued separately, and that separation is itself a root bottleneck. This page covers the device level; the array and system level, where most of these gains get eaten, is [[memristor-array-integration-gap]].

**Scope warning.** Despite "memristor" in the title, this source is effectively RRAM-only. Ferroelectric and phase-change get brief contrast paragraphs in the outlook; **ECRAM is not mentioned at all**. The cross-family comparison this wiki wants — RRAM vs PCM vs FeFET vs MRAM vs ECRAM on common axes — does not exist here and is an open gap on the [[../watchlist]].

## Terms

- **1T1R / 1S1R / 1R** — one transistor + one resistive element per cell; one selector (nonlinear/threshold device) + one resistor; or a bare crossbar cell. The selector exists to block leakage and sneak paths. 1R is cheapest and most sneak-path-prone.
- **Forming voltage** — the higher-than-normal voltage needed on first use to electroform the initial conductive filament. Spread in the forming process is a named root cause of downstream device-to-device variability.
- **FEOL / BEOL** — front-end-of-line (transistor fabrication, 900–1200 °C) vs back-end-of-line (metal interconnect, capped below ~400 °C). RRAM is inserted in the BEOL. The thermal-budget gap between these stages is the central integration blocker for 2D materials.
- **ECM / VCM** — electrochemical metallization (cation-driven filament) and valence-change mechanism (oxygen-vacancy-driven). The two dominant filamentary switching modes.
- **D2D / C2C** — device-to-device and cycle-to-cycle variability.

## Material families

**Binary and complex oxide (filamentary) RRAM** — HfO₂, TaOₓ, TiO₂, SnO₂. The review calls this "the most mature" system and the CMOS/BEOL-compatible workhorse. Switches via ECM/VCM filament formation, plus non-filamentary conduction modes (Schottky emission, Poole-Frenkel, space-charge-limited conduction, trap-assisted tunneling). This is the only family in the source with named foundry-node status — see [[memristor-array-integration-gap]].

**2D-material memristors** — MoS₂, h-BN, graphene, InSe, HfSe₂, BiOI, PtTe₂, used as switching layers, cathodes, or barrier layers. The pitch is atomic thinness (single-layer MoS₂ = 0.7 nm, h-BN = 0.33 nm) and van der Waals stacking, which imposes no lattice-matching requirement and so permits 3D stacking. Positioned as *complementary* to oxide rather than competing: oxide for high-density storage and reliability, 2D for energy-efficient edge and 3D-stacked neuromorphic.

**Ferroelectric memristors** — polarization-flip switching. High endurance, ultralow energy, multi-state capable. Blocked by film-uniformity sensitivity to thickness and grain size, and by annealing temperatures poorly compatible with CMOS BEOL. Covered only briefly.

**Phase-change memristors** — crystalline/amorphous transition, CMOS-compatible, nanosecond switching. Limited by thermal crosstalk between adjacent cells and elevated switching power, both of which worsen with density. Covered only briefly.

**Volatile threshold-switching (TS) memristors** — resistance snaps back when voltage is removed. Used to emulate leaky-integrate-and-fire neuron dynamics (the spontaneous switch-back matches LIF behaviour) and as entropy sources for TRNG/PUF hardware security.

**SAW-guided reconfigurable 2D memristor** *(added 2026-08-20, weekly sweep — thin evidence, see caveat)* — a monolayer-MoS₂ memristor combined on one platform with a surface-acoustic-wave (SAW) device (Kim et al., ACS Nano 2026, KAIST/Sungkyunkwan/Ajou/Hanyang/UMass Amherst/U. Tokyo). The mechanism is novel among this page's entries: **two independently addressable plasticity channels on one device** — electrical pulsing drives long-term plasticity (the usual filamentary route), while non-contact acoustic (SAW) stimulation drives short-term plasticity, without electrical contact. Reported qualitatively: stability beyond 10,000 s, and a downstream reservoir-computing task at 96.1% accuracy (task/baseline unstated). ⚠️ **Evidence caveat:** the primary (ACS Nano) is paywalled with no accessible preprint found; this entry is sourced from a Semiconductor Engineering relay post, which does not carry switching voltage, endurance, retention, or on/off-ratio figures — so unlike every other row in Table 1 below, this device **cannot yet be placed in that table**. Treat as a novelty flag, not a comparable data point, until the primary is captured.

## ECRAM — a stub, and an admission

*Added 2026-08-21.* **Electrochemical RAM (ECRAM)** is a distinct family this wiki has almost no evidence on. Mechanism differs fundamentally from RRAM: ion insertion into a channel modulates its conductance, rather than forming and rupturing a filament. That is claimed to give more deterministic, symmetric programming — the property [[analog-training-nonidealities]] identifies as the binding constraint on on-chip training.

The wiki's only ECRAM source is a **1.6 KB trade-press relay of a two-sentence abstract**, supporting exactly four claims: a **4K-scale ECRAM cross-point array** fabricated, an **8×4 sub-array at 100% yield**, and qualitative "low" cycle-to-cycle and device-to-device variation with "excellent" switching. Training used the **Tiki-Taka v2** algorithm.

**Do not cite ECRAM for anything beyond those four items.** No quantified variability, retention, endurance, on/off ratio or training-accuracy figure is available. The primary — Noh et al., *Sci. Adv.* 10, eadl3350, June 2024 — is on science.org, which this wiki has confirmed **unreachable** (capture hangs, exit 124 on three separate attempts). It sits on the [[../watchlist]] as known-inaccessible.

## Single-device performance after optimisation

The review's own Table 1, reproduced. **Boundary: single device.** These are the numbers that do *not* survive to system level — see [[memristor-array-integration-gap]].

⚠️ The capture lost the table's reference-number column to HTML→markdown extraction (empty bracket artifacts). Per-row attribution below is inferred from surrounding prose and marked as such; `/` means not reported in the original.

| Structure | Endurance (cycles) | Retention (s) | On/Off | Speed (ns) | States | Voltage (V) | Attribution (inferred) |
|---|---|---|---|---|---|---|---|
| Ag/BiOI/Pt | ~50 | >2×10⁴ | ~10⁵ | <10⁶ | 2 | 0.05 | Lei et al. — 0.05 V SET, 100 fJ/switch |
| G/MoS₂₋ₓOₓ/G | ~10⁷ | ~10⁵ | ~10² | <100 | 2 | 0.5 | Wang et al. — stable to 340 °C, 1000 bends |
| Au/h-BN/Au | >500 | ~10⁴ | >10⁷ | <40 | 4 | 1 | Mao et al. |
| Ag/h-BN/Ag | ~10⁴ | ~10⁵ | ~4×10⁹ | / | 2 | 0.16 | possibly Chen et al., wafer-scale h-BN |
| TiN/HfO₂/HfO₂:Al/Pt | ~10⁶ | ~10⁴ | ~10² | / | 2 | 1 | Al-doped HfO₂ interface layer |
| ITO/Bi:SnO₂/TiN | ~10⁷ | >10⁴ | ~10 | / | 2 | 0.5 | Bi-doped SnO₂, coaxial filament |
| Hf/HfO₂/TiN | ~10¹⁰ | >10⁸ | ~100 | / | 2 | <2 | Chen et al. — Hf/Ti oxygen-scavenging cap |
| Ag₆₃Cu₃₇/HfOₓ/Pt | / | / | / | <10 | 2 | 0.13–0.22 | Wang et al., alloy electrode |
| Ag-Cu/α-Si/p⁺-Si | ~3000 | ~600 | ~10² | / | **512** | <2 | Yeon et al., Ag-Cu alloy channel (nonlinearity α = 0.3) |
| G/α-In₂Se₃/h-BN/Cr-Au | ~10³ | ~10⁴ | ~10⁹ | / | 32 | 4–7 | Liu et al., h-BN barrier |
| Ag/ZrO₂/G/Pt | ~10⁶ | ~10⁴ | ~10¹⁰ | SET<30, RESET<10 | 2 | <1 | Liu et al., graphene lateral-diffusion barrier |
| Pt/BN:SiO₂/HfO₂/BN:SiO₂/TiN | ~10¹² | / | ~10² | / | 4 | <1.5 | BN/SiO₂ interlayer confining O ions |
| Ag/TaOₓ/TaOy/TaOₓ/Ag | ~10⁶ | ~2×10⁴ | ~10¹⁰ | SET<100, RESET<500 | 2 | <1 ⚠️ | Sun et al., symmetric selector |
| Au/WS₂/WSe₂/Au | ~5600 | >10³ | ~10⁵ | / | 2 | 2 | not discussed in body — as-tabled only |

⚠️ **Internal inconsistency in the source:** the Ag/TaOₓ/TaOy/TaOₓ/Ag row is tabled at <1 V, but the review's body text states <0.2 V operating voltage for the same device. Unresolved.

**Note the spread.** Nominally similar oxide stacks differ by four orders of magnitude in endurance (Hf/HfO₂/TiN at ~10¹⁰ vs TaOₓ variants at ~10⁶). Endurance is a property of the specific stack and process, not of "RRAM".

### Other named device-level figures

- **Endurance ceiling** — Jiang et al. (2016), Ta/HfO₂/Pt: >1.2×10¹¹ cycles under 100 ns pulses.
- **On/off ratio ceiling** — Yoon et al., 1D1R TiO₂ Schottky-diode + unipolar RRAM: 1.4×10⁹.
- **Analog resolution** — Rao et al.: **2048 distinct conductance levels (11-bit)** in a 256×256 array integrated on commercial-foundry CMOS, enabled by a pulse protocol that denoises **random telegraph noise (RTN)**. Array-level, and the strongest precision result in the source.
- **Drift** — Sharma et al., Ru-complex molecular memristor: conductance drift <0.1% over 10⁷ cycles, single-pulse weight updates, 460× energy-efficiency improvement vs digital (baseline unnamed).
- **LIF neuron element** — Yan et al.: V_th = 0.18 V (SET) / −0.1 V (RESET), 5.3 ns response, 10⁻⁹ W.

RTN deserves emphasis: the review describes it as a fundamental and only-recently-understood noise source requiring dedicated denoising protocols. *(synthesis)* That implies conductance-precision claims published before RTN mitigation may not generalise — a reason to date-check any multi-level-cell precision number.

## The four engineering levers

- **Doping** — Al-doped HfO₂ and Bi-doped SnO₂ appear in Table 1 as interface/filament-control strategies. Bi doping produces a coaxial filament structure.
- **Electrode engineering** — oxygen-scavenging caps (Hf/Ti) push endurance to ~10¹⁰; alloy electrodes (Ag₆₃Cu₃₇) drop operating voltage to 0.13–0.22 V with <10 ns switching.
- **Interface and barrier layers** — graphene as a lateral-diffusion barrier, h-BN as a tunneling barrier, BN:SiO₂ interlayers to confine oxygen-ion motion (~10¹² cycles, the highest endurance in the table).
- **Pulse protocol** — the operation-level half of co-design. RTN-denoising sequences buy 11-bit resolution; multi-level pulse trains buy analog states at a cost detailed in [[memristor-array-integration-gap]].

## Precision, linearity, and why SNNs may care less

For backprop-style ANN training in hardware, the review states large architectures (ResNet-scale) need **≥8-bit-equivalent precision** to converge, which demands many linear, symmetric conductance states. Real devices have narrow linear/symmetric regions, forcing a state-count vs linearity trade-off.

**SNNs appear markedly more tolerant.** Kim et al.'s memristor-synapse SNN held **>89% MNIST accuracy under extreme asymmetric nonlinearity** (V_LTP = V_LTD = 10). The review uses this to argue spiking relaxes the linearity and symmetry requirements that ANN-style hardware imposes.

*(synthesis)* If that generalises beyond MNIST, it is one of the better technical arguments for spiking on analog substrates specifically — not that SNNs are more efficient in the abstract, but that they tolerate the exact device non-idealities analog memristors cannot shed. It is a single small-task result and should not be leaned on until reproduced at scale.

## Source

- `raw/research/neuromorphic-commercial-viability/04-memristor-codesign-review.md` — "Memristor devices for next-generation computing: from performance optimization to application-specific co-design", IOPscience, 2026, open-access CC-BY 4.0, ~160 refs. **Secondary source** — a review aggregating others' measurements; figures are attributed to underlying work where the review names it.
- `raw/research/weekly-2026-08-20/05-semieng-research-bits-aug18.md` — Semiconductor Engineering, "Research Bits: Aug. 18" (2026-08-18), relaying Kim et al., ACS Nano 2026 (SAW-guided MoS₂ memristor; primary paywalled, no preprint found).

## Related

- [[memristor-array-integration-gap]] — where these device-level numbers go to die
- [[cmos-rram-beol-integration]] — a route onto CMOS without an embedded-RRAM foundry PDK
- [[../snn/snn-energy-hardware-realistic]] — crossbar non-idealities as a measured energy cost
- [[../conflicts/snn-energy-payoff]] — device-level efficiency figures as Position A evidence
- [[optoelectronic-rram-photonic-programming]] — a distinct optically-programmed device family not covered by this page's material-family taxonomy
- [[../weekly-briefs/2026-08-20]] — brought in by the 2026-08-20 weekly sweep
- [[../weekly-briefs/2026-08-27]] — brought in by the 2026-08-27 weekly sweep
