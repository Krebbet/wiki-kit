# HyVox: Xylo Audio 3 + MCU open-set speaker ID

UMass Amherst's HyVox (arXiv 2611.03735, 2026-11-01, preprint) splits few-shot speaker identification across a SynSense Xylo Audio 3 dev kit (spiking embedding network) and an STM32L476 MCU (gallery + cosine scoring). **Evidenced (on-device measurement, power-measurement setup not stated in the text):** 1.63 mJ dynamic / 3.8 mJ total per 3-s audio window vs 22.1–43.5 mJ total for int8 ANNs on a *different* MCU (STM32U575). That is 5.8× total and 13.5× dynamic against the most efficient baseline, which is itself 2.7 top-1 points *more* accurate at n=20. A purchasable-hardware datapoint for [[../conflicts/snn-energy-payoff]] that sits inside the wiki's hardware-realistic range.

## What was built

- **Chip:** Xylo Audio 3 (digital neuromorphic; ≤1,000 spiking neurons, 31,744 int8 recurrent synapses, integer bit-shift decays, event caps, one-step delay per hidden-to-hidden connection). Host: STM32L476, both clocked 50 MHz. See [[../players/roster]] (SynSense).
- **Network:** 29.0k-synapse / 832-neuron backbone (compressed 6.5×) with learned per-neuron time constants across fast/medium/slow timescales, plus a 32-neuron readout whose 32 spike counts are the only chip→MCU interface. Enrolment writes a prototype (no weight update); rejection is a threshold.
- **CAST (chip-accurate spiking training):** trains through a differentiable replica of the chip's integer neuron update, derived from the vendor's cycle-accurate simulator. Naively mapping a bit-shift-QAT model to the chip loses 31.1 top-1 points on VoxCeleb1 test speakers; after CAST the chip differs from PyTorch by 0.4 top-1 / 0.1 EER. (Sim-to-chip gap is the real obstacle for ML engineers deploying SNNs; this one is the cleanest quantification in the wiki.)

## Numbers and their boundary

| Quantity | HyVox | int8 ANN baselines (STM32U575) |
|---|---|---|
| Latency per 3-s window | 961.9 ms | 1,659.7–3,413.4 ms |
| Idle power | 2.30 mW | 0.05 mW |
| Dynamic energy / inference | 1.63 mJ | 22.0–43.3 mJ |
| Total energy / inference | 3.8 mJ | 22.1–43.5 mJ |

- **Boundary:** system level (chip + host MCU incl. 0.16 ms cosine scoring and host idle), inference only. Excludes the dev kit's USB/host overhead, which the authors call "not part of a deployed system" — an unverified idealisation.
- **Idle dominates:** ~2.2 mJ of the 3.8 mJ is idle power, hence 5.8× total vs 13.5× dynamic. At 2.30 mW idle, the chip loses to a 0.05 mW MCU on a duty-cycled always-on budget; the authors say as much.
- **Accuracy (Common Voice, 20 accent-homogeneous households, unseen speakers):** 99.6% top-1 / 5.5% EER (2 enrolled) → 94.9% / 13.2% (20 enrolled). The strongest ANN baseline reaches 99.6% / 2.4% at n=20 (at 7.6× the total energy). **Not iso-accuracy**; the headline ratio is against a baseline 2.7 points ahead.
- **Inputs differ** (AFE-16 spikes vs MFCC-40 for ANNs): a system comparison, not like-for-like compute. No digital-NPU or other-neuromorphic energy comparison.

## Assessment

(synthesis) One of the few results where the energy figure is measured on shipping neuromorphic silicon with the host and idle power counted, which is why the advantage (5.8–11.4×) is modest next to simulation-based claims of 10–83× in [[../snn/snn-energy-hardware-realistic]]. Consistent with, not contradicting, the conditions in [[../snn/snn-energy-breakeven-conditions]]. Open: open-set EER rises with gallery size (the authors note security-critical use needs a second factor); long-term voice drift untested; no code/data release found.

**Maturity:** prototype on a commercial dev kit; small eval (20 households). No commercial signal (funding, design win) stated.

## Source

- `raw/research/weekly-2026-11-05/01-hyvox.md` (arXiv 2611.03735)

## Related

- [[../conflicts/snn-energy-payoff]]
- [[../snn/snn-energy-hardware-realistic]]
- [[../snn/snn-energy-breakeven-conditions]]
- [[../snn/spikeduet-mcu-sparse-snn]] — also MCU-hosted and measured
- [[texel-gas-classification]] — dynamic-only vs system boundary contrast
- [[../benchmarks/neurobench]]
- [[../viability-ledger]]
- [[../players/roster]]
- [[../weekly-briefs/2026-11-05]] — brought in by the 2026-11-05 weekly sweep
