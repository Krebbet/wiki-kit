# FeFET analog in-memory computing

The wiki's first substantive FeFET source, closing what was the largest device-family gap — the memristor review this wiki holds is RRAM-only and dismisses ferroelectric devices in a two-line outlook. It also lands directly on the wiki's central analog finding, that ADC/DAC conversion eats the theoretical win, with a design whose whole point is to compute the shift-add in the analog domain rather than paying for it digitally.

**Everything here is simulation.** No CurFe or ChgFe array has been fabricated. That governs how much weight any number below can carry.

## The device

A **FeFET** is a MOSFET with a ferroelectric HfO₂ layer in the gate stack. A write pulse sets the ferroelectric polarization, which shifts the transistor's threshold voltage (V_t) — that shift *is* the stored value. Because V_t is continuously tunable, the device gives **multi-level analog storage** rather than a binary cell.

Three terminals, CMOS-compatible, high on/off ratio, near-zero standby power. Those are general FeFET properties cited to prior work, not re-measured here.

Structurally this differs from RRAM in a way that matters: RRAM ([[memristor-device-engineering]]) is a two-terminal filamentary device whose conductance is set by forming and rupturing a conductive path. FeFET is a three-terminal field-effect device with no filament, so it does not inherit RRAM's forming-voltage spread or sneak-path problem — but it brings its own, chiefly film uniformity and CMOS thermal-budget compatibility.

## The two designs

Both on a 128×128-bit array in 16 banks, supporting 1–8-bit unsigned inputs and 4/8-bit signed weights in two's complement.

**CurFe (current mode)** — `1nFeFET1R` cells, each FeFET paired with a fixed drain resistor (5 MΩ / 2.5 MΩ / 1.25 MΩ / 0.625 MΩ across the four bit positions) that binary-weights the on-state current per bit position. A trans-impedance amplifier sums currents across a block, producing the partial-MAC **and** the 4-bit shift-add in a single analog summation.

**ChgFe (charge mode)** — an SLC pFeFET holds the weight sign bit; MLC nFeFETs hold the rest. Each bitline has a pre-charge transistor and a 50 fF capacitor, and both MAC and shift-add happen by charge sharing among those capacitors — **no separate binary-weighted computation capacitors**, which is the contrast with prior analog-shift-add SRAM designs that need extra proportional capacitors.

*(synthesis)* The shared idea is to fold the shift-add — normally a digital operation requiring conversion — into the same analog summation that does the MAC. If conversion overhead is the thing killing analog in-memory compute, doing more work per conversion is the structurally right attack.

## Results

**Circuit level** — SPICE (Cadence Spectre), commercial **40 nm** CMOS PDK (foundry unnamed). **The 5-bit SAR-ADC is inside these numbers**, which is better disclosure than most:

| Design | TOPS/W @ 8b/8b | TOPS/W @ 4b/8b |
|---|---|---|
| **ChgFe** | **14.47** | 12.92 |
| **CurFe** | 12.18 | 12.41 |
| SRAM 6T+LMC (28 nm) | 9.26 | — |
| SRAM 8T (65 nm) | — | 9.40 |
| SRAM 6T+LLC (28 nm) | 6.90 | — |
| ReRAM 1T1R (22 nm) | 3.60 · 4.72 · 6.53 | — |

Headline: **1.56× more efficient than the best prior SRAM design, 2.22× more than the best prior ReRAM design**, at 8b/8b, node-normalized.

⚠️ All comparators were published at different nodes (22/28/65 nm) and rescaled to 40 nm assuming **energy ∝ node²** — an assumed law the paper does not validate against measured cross-node data. Read the inter-design comparison as directional, not controlled.

The paper does show real comparison discipline in one place: it **excludes a prior design's 41.67 TOPS/W figure from its own headline** because that design exploits input sparsity the others don't, flagging the unfairness itself. Worth crediting — it is the opposite of the unnamed-baseline pattern in [[../conflicts/snn-energy-payoff]].

**System level** — NeuroSim v1.4 (an architectural DNN-accelerator simulator, modified by the authors; **unrelated to [[../benchmarks/neurobench]]** despite the similar name), modelling H-tree interconnect and buffers:

- **1.37×** higher energy efficiency than the best prior system-level analog-IMC realization, on CIFAR10-ResNet18.
- VGG8/CIFAR10 software baseline 92%; **5-bit ADC is the minimum precision** before significant accuracy loss.
- ChgFe trails CurFe by <0.5% accuracy at 4b/4b, and is slower (longer charge-sharing settling per MAC) — stated qualitatively, not quantified.

### The number that matters most: 1.56× → 1.37×

Going from circuit level to system level, the advantage **erodes from 1.56× to 1.37×** — in the authors' own accounting. Roughly a quarter of the claimed gain disappears once interconnect and buffers are modelled.

*(synthesis)* This is the same shape as every other analog result in this wiki, just smaller and more honestly reported. [[memristor-array-integration-gap]] records ADC/DAC conversion exceeding 70% of system power; here a design that explicitly attacks conversion overhead still loses ~25% of its edge at the system boundary. The paper gives **no power breakdown by block** — array versus ADC versus accumulation versus TIA — so it cannot confirm or refute the >70% figure directly. It corroborates the *direction* while leaving the magnitude untested.

That breakdown is the single most useful thing a follow-up could publish.

## What is missing

- **No endurance figure. No retention figure. No measured variability.** Device variability is *assumed* — σ = 40 mV threshold spread, and an on/off ratio of 10⁵ — both **imported from prior fabricated FeFET work by other groups**, not measured for this array.
- **No fabrication.** The FeFET compact model (Preisach-type) is calibrated against real prior device measurements, and the paper shows measured characteristics of a fabricated nFeFET from earlier published work for plausibility — but the 128×128 array, its ADCs, TIAs and accumulation logic are simulated circuit blocks. No tape-out, no sampling, no named foundry commitment.
- Absolute ResNet18/ImageNet accuracy appears only in a figure, and the figure is legible in this capture (marker succeeded here) but the values are not given as text.

*(synthesis)* The reliability silence is becoming a pattern rather than an oversight. Across this wiki's device sources, papers report efficiency and accuracy and stay quiet on endurance, retention and variability — the axes that actually gate productisation. A design can be 14 TOPS/W and still be unshippable if it survives 10³ writes or drifts in a week. This page records the gap rather than treating the efficiency number as the whole story.

## Maturity

**Simulation only, both boundaries.** Circuit: SPICE on a 40 nm PDK with an experimentally-calibrated FeFET compact model. System: NeuroSim architectural simulation. Ladder position: **below "small array"** — there is no array. What exists is a credible design study on a device family with real fabricated precedent elsewhere.

## Open questions

- Power breakdown by block — what fraction is the ADC? This would directly test the >70% finding.
- Endurance, retention, and *measured* variability for a fabricated CurFe/ChgFe array.
- Does the analog shift-add survive fabrication, where charge sharing meets real capacitor mismatch?
- How does FeFET compare to RRAM, PCM, MRAM and ECRAM on common axes? Still no cross-family source in the wiki.

## Source

- `raw/research/neuromorphic-seed-sweep/10-fefet-analog-imc.md` — "Energy Efficient Dual Designs of FeFET-Based Analog In-Memory Computing with Inherent Shift-Add Capability", arXiv:2410.19593. Captured with marker, so figures are present. ⚠️ Table 1 is column-misaligned in the extraction; the design→number pairing above was reconstructed from surrounding prose and figure captions, which corroborate it.

## Related

- [[memristor-device-engineering]] — RRAM, the two-terminal alternative
- [[memristor-array-integration-gap]] — the >70% conversion-overhead finding this page partially corroborates
- [[analog-training-nonidealities]] — what happens when you try to train on devices like these
- [[../conflicts/snn-energy-payoff]] — the comparison-honesty standard this paper mostly meets
- [[../viability-ledger]]
