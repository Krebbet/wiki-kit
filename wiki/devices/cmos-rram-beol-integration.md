# CMOS-RRAM BEOL integration (rapid-prototyping route)

Evidence that the foundry-access gate is not absolute: a university group can insert RRAM into the back-end-of-line of commercially fabricated CMOS wafers **without an embedded-RRAM foundry PDK**, and get a working 1T1R array out. University of Edinburgh (Prodromakis group), arXiv:2512.09791. The result matters for [[memristor-array-integration-gap]] because "no foundry offers analog CIM RRAM" is one of the strongest arguments that neuromorphic materials are far from commercial — this paper shows the gate is technically tractable by other routes, while being honest that its own route is not production-ready.

## What was actually built

**CMOS substrate:** commercial foundry (unnamed, proprietary process), **200 mm wafers, 180 nm 1P5M, 1.8/5 V**. Fabrication deliberately halted at metal-4 with only the foundry's own ILD-4 passivation — no further foundry BEOL. This is **monolithic** integration (RRAM built directly on the die's own metal-4), not chiplet or hybrid bonding.

**RRAM stack:** two-terminal MIM. Best CMOS-integrable stack **TiN/HfOₓN_y/TiN** — nitrogen-doped hafnia, ALD-deposited, 10 nm in single-device work, 5 nm in the 16×16 integration. Chosen over TiOₓN_y, plain TiOₓ and HfOₓ for lowest forming/switching voltage and quasi-analogue tunable resistance. An alternate **Pt/TiOₓN_y/Pt** (10/10/20 nm) was used for the up-scaled 0.5 Mbit array.

Material selection was done independently of CMOS, on 150 mm thermally-oxidised Si wafers:

| Stack | Active layer | Forming | Switching |
|---|---|---|---|
| TiOₓN_y/Pt | 25 nm | ~6.5 V | ~1 V |
| TiOₓ/Pt (reference) | 25 nm | ~9 V | ~1.5 V |
| **HfOₓN_y/TiN** (selected) | 10 nm | **~2–4 V** | **~1–3 V** |

**Cell:** 1T1R with pMOS select transistors, 5 V devices, active-low.

## The integration route

The paper's actual contribution is methodological — it positions itself as documenting the *journey*, arguing prior CMOS-RRAM papers (Li et al. Nat. Commun. 2023; Wan et al. Nature 2022; Zhang et al. Science 2023; Liu et al. Nat. Electron. 2025) are application-focused and give only key technical details of the integration itself.

The design point is explicitly "meeting in the middle" between full wafer-level stepper lithography and full per-die e-beam. Wafers are diced into **multi-reticle chips** (several reticle copies per chip, no carrier-substrate mounting) and patterned with maskless **optical direct-write lithography** or e-beam.

1. **Thin the foundry passivation** from ~850 nm (~650 nm SiO₂ capped with ~200 nm Si₃N₄, typical pre-90 nm dielectric) down to ~100 nm via 5% HF wet etch plus CMP re-planarisation. Final surface roughness Sa 0.21 nm / Sq 0.31 nm by AFM. This step exists because deep-trench topology defeats fine patterning.
2. Etch vias to expose CMOS metal-4.
3. Deposit and pattern RRAM bottom electrode, active layer, top electrode in sequence.
4. Fill etched trenches with a Ti/Al bilayer by e-beam evaporation, using a **"pseudo-via" approach that explicitly substitutes for damascene + metal CMP**. Al matches the 180 nm node's native interconnect metal; Cu/W noted as compatible at 130 nm and beyond but not used.

## Measured results — and the gaps

**16×16 1T1R crossbar (256 cells), 2×2 µm² TiN/HfOₓN_y/TiN.** Boundary: integrated array on CMOS.

- Pristine resistance: **MΩ range** (read at 0.5 V)
- Post-forming operating range: **10–100 kΩ** (read at 0.5 V) — the closest thing to an on/off window reported; not stated as a formal on/off ratio
- Forming: typically **1000 pulses × 1 ms at 2–3 V**, or by I-V sweep
- Programming: **100 µs pulses at 1–3 V**, or by I-V sweep
- Some devices remained **unformed** after one forming cycle. **No numeric yield given.** Attributed qualitatively to stochastic filament formation rather than process non-uniformity — but not confirmed.

**What is missing, and it is a lot:** no endurance cycling, no retention time, no device-to-device or cycle-to-cycle variability figure appears anywhere in the paper. For a wiki that tracks exactly those axes, this array is characterised only by resistance maps and switching waveforms.

**The larger arrays are structural only.** A 1 Mbit platform (4 independently-controlled 512×512 sub-arrays, ~1,048,576 cells) and a 0.5 Mbit array are shown by optical and SEM imaging — **no electrical characterisation at all**. E-beam patterning reached 400 nm openings (dose 342 µC/cm²) approaching full ~500×500 nm² cell density; optical DWL was limited to 1 µm openings and needed double patterning to resolve the top electrode at half-array density.

Four application chips (1T1R neural sensor interface, 9T4R analogue CAM, analog-domain NN-accelerator aggregator, 1T1R/2T1R radiation-hardened cells; RRAM 1–2 × 2 µm², TiN/HfOₓN_y/TiN 50/5/50 nm) are shown integrated — but functional performance is deferred to separate cited papers, not measured here.

**No turnaround-time or cost figures appear anywhere**, despite "rapid-prototyping" and "cost-effective" in the title and abstract. Those are framing claims, not quantified.

## Comparison honesty

The comparisons made are process-methodological — this route versus the group's own prior wafer-level singulated-chip process (JMEMS 2020), and optical DWL versus e-beam on resolution/pitch/cost/speed.

**No comparison is made to industrial embedded-RRAM foundry offerings** on yield, variability, endurance, or cost. That is a real gap given the paper's stated goal of a route to volume production: the "seamless transition from R&D to volume production" claim is asserted, never benchmarked against any volume-fab metric.

*(synthesis)* And there's an unstated leap: inferring "the methodology scales to high density" from optical and SEM images of the 1 Mbit array, with no functional yield data at that density. The paper says up-scaling is "contingent on several processing factors" but never reports whether the up-scaled array actually switches. Structural demonstration is not electrical demonstration.

## Blockers the authors state

Creditably explicit:

- The 16×16 demonstration "does not examine integration uniformity and repeatability, and their potential influence to device characteristics."
- Unformed devices after one forming cycle; cause not conclusively identified.
- Deep-trench passivation topology is incompatible with high-density patterning, motivating the CMP thinning step — itself nontrivial. Etch-induced topology matching the underlying metallisation was observed and only partly understood ("the cause of this effect is unclear").
- Optical DWL cannot resolve full 1 Mbit density; needs e-beam or double patterning, each adding cost and complexity.
- **The pseudo-via metal fill must be replaced by damascene + metal CMP for volume production** — the authors say so directly, and it undercuts the "seamless" framing: a required process change before scale-up is not seamless.
- TiN top-electrode native oxide requires an added Pt capping layer.
- FIB cross-sections showed CMOS passivation over-etch partially attacking the underlying metal-4. Authors judge it "unlikely to be of any significance" but do not quantify the impact on yield or resistance.

## Maturity

| Sub-demonstration | Rung |
|---|---|
| Single device / material development | Mature — multiple stacks on 150 mm test wafers |
| Small integrated crossbar | **16×16 1T1R, electrically validated** |
| Large integrated crossbar | 1 Mbit / 0.5 Mbit — **structural only, not electrically validated** |
| Application-specific chips | RRAM physically integrated; function reported elsewhere |
| Combined CMOS+RRAM foundry tape-out | **No.** Foundry supplied front-end CMOS only; all RRAM BEOL work done in a university ISO4 cleanroom |

Anchor point for the ledger: **180 nm, 200 mm, 1T1R, 16×16 electrically validated, no yield/endurance/retention data.**

## Reproducibility

Unusually high process detail — specific tool models (Karl Suss MA8 Gen2, DMO MicroWriter ML3 Pro, RAITH EBPG, Veeco Fiji Gen2 ALD, Angstrom Nebula/EvoVac, JLS RIE80, Presi Mecapol E460 CMP, Tescan VEGA3, Park NX20 AFM, ArC Instruments ArC TWO), photoresists and thicknesses, spin speeds, bake schedules, per-layer exposure doses, etch chemistries and powers, deposition rates and base pressures. Another comparably-equipped cleanroom could closely replicate the RRAM-side process.

Against that: the foundry and its 180 nm process are unnamed, and **no masks, layout files, or code are released** — only descriptions and images. Funding is EPSRC (FORTE, ProSensing) and the Royal Academy of Engineering; no industry or foundry partner appears as co-author or sponsor.

## Position on the viability question

Evidence that the CMOS/BEOL integration gate is **technically tractable without a foundry embedded-RRAM PDK** — but not evidence that this route is production-ready. No yield at scale, no endurance, no retention, no variability, no cost, no schedule, and an acknowledged process change required before volume fab. The "volume production" language is aspirational.

*(synthesis)* The useful reframing: foundry PDK availability gates *commercial* deployment, not *research* iteration. A route like this decouples academic progress from foundry roadmaps, which should raise the rate of published array-scale results without moving any product date. When reading a new memristor array paper, ask which kind of fab it came from — the answer changes what the result implies about timelines.

## Open questions

- Does the 1 Mbit array switch? Electrical characterisation is the obvious follow-up from this group.
- Yield, endurance, retention and variability for the 16×16 — none reported.
- How does this route compare to TSMC/UMC/SkyWater embedded ReRAM PDKs on yield and cost? Never benchmarked.
- Does the pseudo-via → damascene transition preserve the device characteristics?

## Source

- `raw/research/neuromorphic-commercial-viability/08-cmos-rram-rapid-prototyping.md` — "A Rapid-prototyping CMOS-RRAM Integration Strategy", arXiv:2512.09791, University of Edinburgh (Prodromakis group). Primary, peer-review status not established from the capture.

## Related

- [[memristor-array-integration-gap]] — the foundry-access gate this paper routes around
- [[memristor-device-engineering]] — HfOₓN_y/TiN in the wider stack landscape
- [[../viability-ledger]] — maturity anchor point
- [[../players/roster]] — Edinburgh/Prodromakis as a named group
