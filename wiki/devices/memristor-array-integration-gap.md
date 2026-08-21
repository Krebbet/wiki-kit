# Memristor array integration and the lab-to-fab gap

The single most load-bearing page for this wiki's central question. Device-level memristor numbers are genuinely impressive — attojoule-to-femtojoule switching energies, 10¹² cycle endurance, 11-bit analog resolution (see [[memristor-device-engineering]]). Almost none of that survives to system level. The 2026 IOP co-design review is unusually candid about why, and **flags its own optimism**: it reports the aJ/fJ switching figures and then states in §4.1 that they "often suffer significant degradation" at array and system level. This page is the itemised gap.

## The headline: peripherals eat the win

Two system-level numbers from the review dominate everything else on this page:

- **ADC/DAC signal conversion accounts for >70% of total system power** in ≥8-bit or high-speed applications. Stated as a general claim, not attributed to a single paper. Boundary: system.
- **Static leakage does not go away just because the memory is non-volatile.** At 10 pA/cell leakage, a 1k×1k crossbar at 1 V draws **~10 mW static power**. This is the review's own arithmetic, not a cited measurement, and it worsens as dielectric thickness scales down — especially for 2D materials with narrowed bandgaps.

*(synthesis)* An analog crossbar's whole thesis is that computing in the analog domain avoids the data movement and MAC energy a digital accelerator pays. If converting between analog and digital costs more than 70% of system power, the thesis is load-bearing on the converters, not the memristors. This is the same structural failure the [[../snn/snn-energy-hardware-realistic]] paper measures from the algorithm side, and it is why [[../conflicts/snn-energy-payoff]] is framed around measurement boundary rather than device physics.

There is a third, less-quoted trade-off in the same direction: **achieving 4-bit resolution (16 states) requires multi-level pulse sequences that degrade effective energy efficiency by 2–3 orders of magnitude versus binary switching.** Precision and energy are directly opposed at the device level, before any peripheral cost.

## Array performance after optimisation

The review's Table 2. **Boundary: array.** Note that no TOPS/W figure here states whether peripheral (ADC/DAC/driver) power is included — a conspicuous omission given the review's own §4.1 argument that peripherals dominate.

| Array | Scale | Yield | Uniformity | Efficiency | Precision | Cell | Application |
|---|---|---|---|---|---|---|---|
| Ta/HfO₂/Pd | 128×64 | 99.8% | / | 119.7 TOPS/W | 5–8 bit | 1T1R | Analog signal/image processing |
| Au(Ag)/h-BN/Au(Ag) | 64×64 | 98% | C2C 1.53%, D2D 5.74% | / | 4–5 bit | 1R | Image classification |
| TiN/TaOₓ/HfOₓ/TiN | 128×16 | 99.99% | / | 11 TOPS/W | 5 bit | 1T1R | Handwritten-numeral recognition |
| TiN/HfOₓ/Pt | 160 cells | / | / | / | 3 bit | 1T4R | In-memory computing |
| Ti/HfSe₂/Au | 32×32 | 89% | / | 1309.1 TOPS/W | 3 bit | 1S1R | Image classification |

**Read the scale column first.** The largest entry is 128×64 = 8,192 cells. The most energy-efficient entry (1309.1 TOPS/W) is a 32×32 array — 1,024 cells — at 3-bit precision with 89% yield. Yield ranges 89%–100% across materials and studies, which says yield is process- and material-dependent and **not yet uniformly solved at any real scale**.

Chip-scale, the review's best exhibit is **STELLAR** (Zhang et al.): 160,000 memristor cells monolithically integrated with CMOS, claiming **35× energy-efficiency improvement vs digital accelerators** on motion-control and image-classification tasks. Task-named, which is better than most; the digital baseline part is not specified.

## The eleven blockers

As itemised by the review:

1. **Array yield** — most "large-scale" arrays are ≤256×256; yields 89%–100% depending on process and material.
2. **D2D and C2C variability** — constrains Hopfield-network training time, storage precision, and TRNG probability distributions. Forming-process-induced spread in V_th/V_hold named as a root cause.
3. **Sneak-path / crosstalk currents** in bare 1R crossbars — requires 1T1R, 1S1R, complementary voltage division, or self-rectifying materials. All add area and circuit complexity.
4. **Peripheral circuit overhead** — ADC/DAC >70% of system power (above).
5. **Static leakage** — ~10 mW per 1k×1k crossbar at 1 V (above).
6. **Energy-precision trade-off** — 2–3 orders of magnitude efficiency loss to reach 4-bit (above).
7. **BEOL/FEOL thermal-budget mismatch for 2D materials** — FEOL dopant-activation anneals need 900–1200 °C; most 2D materials decompose above 400–800 °C in air; BEOL interconnect caps below ~400 °C, too low for high-quality 2D synthesis. Named as *the* core reason 2D-memristor CMOS integration remains hard. One workaround cited: Jain et al., MBE-grown wafer-scale 2D HfSe₂ transferred at ≤150 °C onto Si selectors.
8. **3D-stacking thermal crosstalk** — Joule heating propagates between stacked layers; needs high-thermal-conductivity materials (graphene heat spreaders) or new dissipation structures.
9. **2D-material manufacturing defects** — thickness non-uniformity, wrinkling, microvia formation over large areas causing switching-voltage fluctuation and shorts. Conventional ion implantation is called insufficient for atomic-scale doping. Ambient oxidative degradation of ultrathin layers needs encapsulation, unsolved.
10. **Family-specific fabrication gaps** — ferroelectric: film uniformity sensitive to thickness/grain size, annealing poorly BEOL-compatible. Phase-change: thermal crosstalk and switching power, both worsening with density.
11. **No cross-scale co-design framework** — named as the root bottleneck. Device, circuit and algorithm are not jointly optimised in most reported work, so a gain at one level is undone at another.

## Foundry status — the actual viability gate

This is where a commercial-viability date would have to come from, and the source supports very little:

| Claim | Owner | Date | Tier |
|---|---|---|---|
| 40 nm RRAM platform | TSMC | 2019 | Claimed by the review; no independent benchmark given |
| 2nd-gen 22 nm eRRAM, "rivals embedded STT-MRAM" | TSMC | 2024 | Claimed; no quantitative comparison in this source |
| "Reported progress on RRAM-based chips" | Samsung, Unity | — | Vague. No node, product, or metric. Weak signal. |

**The critical distinction:** TSMC's embedded RRAM is **embedded non-volatile memory, not neuromorphic compute.** Everything neuromorphic-specific in this review tops out at chip-scale lab demonstrations (STELLAR, 160k cells) — not products. A foundry shipping eRRAM as a flash replacement does not mean a foundry shipping analog compute-in-memory. Conflating the two is the most likely way to overstate how close this is.

*(synthesis)* On this evidence the honest reading of the commercial timeline is: oxide RRAM as embedded NVM is a real foundry product today; oxide RRAM as an analog neuromorphic compute substrate is at chip-scale demo, gated on peripheral energy overhead and array yield, with no announced foundry PDK. 2D-material memristors are a further step back, gated on a thermal-budget problem that is physical rather than merely engineering-difficult. Nobody in this source has shown analog CIM end to end at product scale.

## On-chip learning as defect tolerance

The review takes a fairly explicit side on the on-chip-learning-necessity dispute, via a pairing:

- **Li et al. (in-situ, SGD-based)** — training *on* an 11%-defective Ta/HfO₂/Pt array reached **91.71% MNIST**; simulation held **>60% accuracy even at 50% stuck-off devices**.
- **Jeon et al. (static, offline-programmed)** — a defect-free 1 kb array got 100% on an MNIST subset, but collapsed to **68.5%** at 30% open-circuit defects and **49.8%** at 50%.

The argument: at realistic yields, in-situ learning is the viable defect-tolerance path, because offline-programmed arrays degrade catastrophically with the defect rates real fabrication produces. Related: a **sign-backpropagation** algorithm (error-sign-only updates, no precise gradients, no write-verify) cut computational complexity 98% and gave 100× energy efficiency vs conventional backprop while holding >93% accuracy despite asymmetric switching.

*(synthesis)* This reframes on-chip learning. The usual argument for it is adaptivity or biological fidelity; here it is a **yield-economics** argument — in-situ training is how you ship an array that isn't perfect. If it holds, it couples the learning-rule question to the manufacturing question, and both to whether analog CIM can ever be cost-competitive. Caveat: MNIST-scale, single-source.

### ⚠️ This reading is now disputed

*Added 2026-08-21.* The yield-economics argument above rests on Li et al., recorded here as **"in-situ, SGD-based"**. New evidence shows plain Analog SGD collapsing **below 15% accuracy from conductance response-function asymmetry alone, with no defects present**, where Tiki-Taka-class algorithms hold 97%. And a device *engineered* for symmetric updates measures **61% symmetry-point skew** on real silicon.

If Li et al. genuinely used plain SGD, their result depends on a favourable device response function and is **device-specific, not a general property of in-situ training**. See [[../conflicts/analog-onchip-training-viability]] — open, with "read Li et al. and establish the actual update rule" as the decisive resolution step. The claim above is left as written pending that check, rather than rewritten on inference.

## Corroboration from FeFET

*Added 2026-08-21.* [[fefet-analog-imc]] offers partial independent support for the peripheral-overhead finding. A FeFET design built specifically to fold shift-add into the analog domain — attacking conversion cost directly — still sees its advantage **erode from 1.56× at circuit level to 1.37× at system level** in the authors' own accounting, once interconnect and buffers are modelled. Roughly a quarter of the gain lost at the system boundary.

It cannot confirm or refute the >70% figure specifically: its circuit-level TOPS/W **does** include the 5-bit ADC, but it publishes no power breakdown by block. It corroborates the direction while leaving the magnitude untested. That breakdown remains the single most useful thing a follow-up could publish.

## Baseline honesty in this source

Mixed, and worth recording because this wiki will cite it:

- **Good:** STELLAR's 35× at least names the tasks. Rao et al.'s 11-bit result names the array size and the foundry process. Tang et al.'s 3D MoS₂ MNIST result gives an explicit named digital baseline (98.02% vs 98.24% GPU).
- **Bad:** "20-fold" and "72.8%" system energy reductions (He et al., Kang et al.) don't say whether the baseline is a GPU, an ASIC, or an idealised digital estimate. He et al.'s optoelectronic in-sensor array claims ">20× energy reduction vs GPU baseline" with no absolute GPU numbers.
- **Notable:** the review flagging its own aJ/fJ figures as not surviving to system level is a rare and creditable move for a review, and is the reason this page can be written at all.

## Open questions

- What is peripheral-inclusive TOPS/W for any of these arrays? No source captured so far states it.
- Is there any announced foundry PDK for analog compute-in-memory RRAM, as opposed to embedded NVM?
- Do the in-situ defect-tolerance results survive beyond MNIST-scale?
- Cross-family comparison (PCM, FeFET, MRAM, ECRAM) on these same axes — absent here, on the [[../watchlist]].

## Source

- `raw/research/neuromorphic-commercial-viability/04-memristor-codesign-review.md` — "Memristor devices for next-generation computing: from performance optimization to application-specific co-design", IOPscience, 2026, open-access CC-BY 4.0. Secondary source; figures attributed to underlying work where named. ⚠️ The capture lost the tables' reference-number column to HTML→markdown extraction — re-fetch the original if per-row citation precision is needed.

## Related

- [[memristor-device-engineering]] — the device-level numbers this page discounts
- [[cmos-rram-beol-integration]] — a prototyping route around the missing foundry PDK
- [[../snn/snn-energy-hardware-realistic]] — the same peripheral-overhead story, measured from the algorithm side
- [[../conflicts/snn-energy-payoff]] — the dispute this page's §4.1 evidence feeds
- [[../viability-ledger]] — where the foundry-status rows land
