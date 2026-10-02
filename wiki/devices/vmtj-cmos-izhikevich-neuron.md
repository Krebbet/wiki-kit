# Voltage-controlled MTJ–CMOS Izhikevich-inspired neuron

The wiki's first spintronic entry: a voltage-controlled magnetic tunnel junction (V-MTJ) paired with 22 nm FD-SOI CMOS to produce five Izhikevich-style firing patterns at 145.44 fJ/spike average. It also carries a headline "up to 88.6% fewer spikes" claim — and that number comes from a *different* model than the one the energy figure comes from. This page exists mostly to keep those three boundaries (measured device, simulated circuit, software proxy) apart.

**The neuron was never fabricated.** One V-MTJ device was measured; the neuron is a circuit simulation; the SNN results use a software stand-in that is not shown to map onto the circuit.

## The device

An **MTJ** (magnetic tunnel junction) is two magnetic layers around a thin MgO barrier; resistance is low when the layers' magnetizations are parallel (P) and high when antiparallel (AP). Most MTJ neurons and synapses use spin-transfer torque (STT) switching, which needs high current and suffers endurance wear — the paper itself notes both.

This device uses **VCMA** (voltage-controlled magnetic anisotropy) instead: a voltage, not a current, lowers the energy barrier between states. Operated as a **thermally stochastic two-state element** — random telegraph noise flipping between P and AP — the mean dwell time falls roughly exponentially with applied voltage V_T, and an external magnetic-field bias sets P/AP occupancy.

Stack as fabricated: SAF reference / W 0.25 nm / CoFeB 0.8 nm / MgO 1.5 nm / CoFeB 1.6 nm / Mo 5 nm cap. Perpendicular anisotropy, 50 nm circular pillars, e-beam lithography and ion milling, sputtered on thermally oxidized Si. **This is a university lab process, not a foundry process.**

Compared with [[memristor-device-engineering]] (filamentary RRAM) and [[fefet-analog-imc]] (ferroelectric threshold shift), this device is volatile and stochastic by design: it is an excitability gate, not a stored weight.

## The circuit

The MTJ is only the **fast excitability gate** — the P state enables the membrane-charging PMOS P1. The **slow recovery variable is entirely CMOS**: recovery capacitor C_u, an N2 discharge path, a spike-triggered increment circuit, and a Schmitt-trigger enable (hysteresis).

CMOS: GlobalFoundries 22 nm FD-SOI (22FDX), V_DD = 0.8 V, MOM capacitors for C_v and C_u. Circuit-level simulation only.

⚠️ "Izhikevich-inspired" is loose. The paper's Eq. 5–9 describe a membrane current balance, a recovery capacitor and Schmitt-trigger hysteresis — **not** the Izhikevich quadratic equation. Five modes are shown in simulation: tonic bursting, tonic spiking, phasic bursting, phasic spiking, spike latency.

Recovery bias windows by mode: tonic bursting 600–650 mV, tonic spiking 300–350 mV, phasic spiking and spike latency 150–200 mV. Mode selection means setting V_bias, V_I.C, V_T and V_inc levels per pattern; that control overhead is not costed.

## Results

Three tiers, three different evidence types.

**Measured (single V-MTJ, room temperature, Fig. 2b–d):** resistance-time trace, dwell time vs voltage (approximately exponential), P/AP occupancy vs field. **No numeric dwell times, TMR or switching voltages are given in the text.** These measurements feed a compact model; they do not characterise the neuron.

**Circuit simulation (22FDX PDK, neuron only):**

| Mode | fJ/spike |
|---|---|
| Average over five modes | **145.44** |
| Tonic bursting (lowest) | 8.82 |
| Spike latency (highest) | 515.4 |

- The ~58× spread across modes means the mean is not a workload-weighted figure, and the very low tonic-bursting value may not be representative.
- **Boundary: neuron circuit only.** Excludes V_T drive generation, field bias source, synapses and routing.
- Dynamics are nanosecond-scale versus millisecond biological timescale (stated). No frequency or area figures.

**Software proxy (not the circuit).** Tonic- and phasic-bursting behaviour is emulated with Adaptive Exponential Integrate-and-Fire (AdEx) in snnTorch and compared against LIF in the same architecture: fully connected, one 3,000-neuron hidden layer, forward Euler dt = 1.0, T = 40, BPTT with a fast-sigmoid surrogate gradient (slope 40, see [[snn-training-surrogate-gradients]]), Adam lr 5e-5, cross-entropy on accumulated output spikes. Off-chip training; no on-chip learning.

| Task | LIF acc · spikes | Tonic burst acc · spikes | Phasic burst acc · spikes |
|---|---|---|---|
| MNIST | 97.80% · 9,326 | 97.59% · 5,177 | 97.59% · 3,449 (−63%) |
| Fashion-MNIST | 85.21% · 42,861 | 85.73% · 13,707 | 86.76% · 4,916 (−89%) |
| Breast Cancer | 97.39% · 765 | 97.39% · 444 | 97.39% · 328 |
| IRIS | 96.77% · 2,123 | 96.77% · 750 | 96.77% · 431 (−80%) |

The abstract's "up to 88.6%" is the Fashion-MNIST phasic reduction (about 88.5%). Welch's t-test p < 0.001 on spike counts; seed or run count not given in the text read.

### The number that matters most: spikes are not energy

*(synthesis)* The paper places a circuit-sim fJ/spike figure next to an algorithm-level spike reduction, inviting a combined benefit that **was never computed**. The paper only says fewer spikes "provide a potential pathway" to lower energy; it never multiplies spikes by fJ/spike. A spike-count cut also ignores the burst neuron's added recovery circuitry. This is the same gap [[snn-energy-hardware-realistic]] flags, and a further instance of the pattern in [[../conflicts/snn-energy-payoff]].

Two further reasons to discount the 88.6%:

- The LIF baseline spike counts are very high (42,861 on Fashion-MNIST at T = 40 with 3,000 hidden neurons) with large SD. No spike-rate regularisation is mentioned, so the baseline may be untuned for sparsity, which inflates the reduction.
- **Hardware parameters are not shown to map onto the AdEx parameters actually used.** The proxy tests "do bursting neurons sparsify spikes", not "does this circuit do so".

Also: compared against conventional LIF only. No comparison to other MTJ, memristive or CMOS Izhikevich neuron circuits on energy or area.

## What is missing

- **No endurance, no retention, no device-to-device variability, no array-level numbers.**
- **No fabricated neuron.** No co-integrated V-MTJ + CMOS silicon. The paper cites 3D V-MTJ/CMOS BEOL co-integration (ref [38], Duffee et al., Newton 2026, in press) but does not demonstrate it. Compare [[cmos-rram-beol-integration]] for what that route looks like for RRAM.
- **The external magnetic-field bias is not addressed as an integration problem.** It is a required input to set P/AP occupancy.
- **Stochastic dwell-time variability** is unaddressed, though the device is stochastic by construction and the neuron's timing depends on it.
- No synapse or array design.
- **No code, netlists, device data or model parameters released.** The software part is approximately replicable from the Methods hyperparameters (PyTorch, snnTorch); the circuit and MTJ compact model are not.

## Maturity

**Single measured device plus simulated circuit plus software proxy.** One lab-fabricated 50 nm V-MTJ; a schematic-level neuron in the 22FDX PDK; an AdEx SNN in snnTorch. No neuron fabricated, no array, no chip, no tape-out. Ladder position: **below "small array"** — device characterisation plus schematic-level design.

Commercial signal: none. Academic work (UW-Madison, Northwestern, GMU) funded by US DOE (DE-SC0026035, DE-SC0026260, DE-SC0026325) and NSF (CCF-2319617, 2539714). No industry partners, products or dates. The only industry tie is the GlobalFoundries 22FDX PDK used in simulation — the node the wiki records for [[brainchip]]'s Akida AKD1500 — but there is no relationship between the two.

## Novelty

Recombination and refinement. The authors claim the first V-MTJ/CMOS Izhikevich-inspired neuron: a VCMA stochastic switch as fast excitability element, with a CMOS recovery and Schmitt-trigger circuit for multi-pattern firing. Closest prior work: STT-MTJ stochastic spiking neurons (refs 33–37), a spintronic integrate-fire-reset neuron (Yang et al. 2022, ref 29), a ferroelectric quasi-LIF neuron (ref 27), a stochastic phase-change neuron (ref 28), and the authors' own Izhikevich-inspired temporal dynamics work (ref 39, ICONS 2025). VCMA dwell-time tuning is from Athas et al. (ref 40).

Contrast with [[hippocampus-bioinspired-memristor]], which also uses Izhikevich neurons in hardware but on a real 20,000-device crossbar with silicon data; this paper has neuron-level evidence only, and that simulated.

## Open questions

- What does an end-to-end energy figure look like — spikes × fJ/spike including bias, drive and field sources — for the bursting modes actually used?
- Does the AdEx proxy's sparsity gain survive when run with the circuit's actual dynamics and parameters?
- Does the LIF advantage persist against a sparsity-regularised LIF baseline?
- How is the magnetic-field bias supplied on-chip, and can V-MTJ be BEOL co-integrated at 22FDX?
- What is the device-to-device and cycle-to-cycle spread of dwell time, and what does it do to firing patterns?

## Source

- `raw/research/weekly-2026-10-01/03-vmtj-cmos-izhikevich-neuron.md` — "A Voltage-controlled MTJ-CMOS Neuron Emulating Tunable Izhikevich-Inspired Dynamics", arXiv 2609.32031 (UW-Madison / Northwestern / GMU). Evidence types: single-device measurement, 22FDX circuit simulation, AdEx software proxy.

## Related

- [[memristor-device-engineering]] — RRAM; this page is the wiki's first spintronic device entry
- [[fefet-analog-imc]] — the other simulation-heavy device page, with the same reliability silence
- [[cmos-rram-beol-integration]] — the BEOL co-integration route V-MTJ assumes but does not show
- [[snn-energy-hardware-realistic]] — spike counts are not energy
- [[snn-training-surrogate-gradients]] — the BPTT / fast-sigmoid training used for the software proxy
- [[hippocampus-bioinspired-memristor]] — Izhikevich neurons on a real crossbar, for contrast
- [[../conflicts/snn-energy-payoff]] — another algorithm-level sparsity claim paired with a device-level energy number
- [[brainchip]] — same 22FDX node, PDK only here
- [[../viability-ledger]]
