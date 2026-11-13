# ECRAM volatile dynamics as short-term plasticity in a delay-feedback LIF neuron

A co-design paper that turns the decaying conductance response of an ECRAM into short-term plasticity (STP) inside a leaky-integrate-and-fire (LIF) neuron. **Only the single-device transients and variability are measured** (a MoS2 / PEO:LiClO4 ionically gated transistor); the neuron circuits, the headline "near 2 pJ" spike energy and the frequency-filtering results are simulation. No neuron, array or chip was fabricated. This is the wiki's second ECRAM source and the first with a mechanism and measured device data; the first (Noh et al., *Sci. Adv.*) is still not captured.

## Terms

- **ECRAM** (electrochemical RAM): a three-terminal ionically gated transistor. The gate-to-source bias moves ions in an electrolyte; the drain-to-source channel conductance is the stored state and is read separately. Read and write paths are decoupled, unlike two-terminal RRAM ([[memristor-device-engineering]]).
- **Short-term plasticity (STP):** synaptic strength that changes transiently with recent activity and decays back, as opposed to long-term weights. **Facilitation** is the strengthening case. Here, two forms: *synaptic facilitation* (a synapse strengthens from its own input spikes) and *intrinsic excitability modulation* (the neuron's output spikes strengthen all its input synapses, which acts like a lower firing threshold). **Short-term depression (STD)** is the weakening counterpart.
- **EDL regime vs doping regime:** low or short gate pulses build a reversible electric double layer at the electrolyte/channel interface, giving a transient conductance rise that relaxes. Higher or longer pulses cause electrochemical doping, a persistent (nonvolatile) shift. The paper uses the volatile regime on top of a programmed nonvolatile state; the crossover depends on the specific electrolyte/channel pair.
- **Conductance linearity:** how evenly spaced the conductance steps are across programming pulses. The paper cites ECRAM as more linear than memristors (background citation, not measured here).
- **1T1E synapse:** one NMOS switch in series with one ECRAM, the ECRAM analogue of 1T1R.

## Mechanism

Each synapse is a 1T1E cell. A pulse on the ECRAM gate transiently raises that synapse's conductance. Wiring the ECRAM gate to the synapse's own input gives synaptic facilitation; wiring all ECRAM gates of a neuron to that neuron's output gives excitability modulation. Only one configuration is active at a time. No extra circuit element is needed beyond the gate routing. A second ECRAM plus a current mirror gives STD (shown in the standalone synapse simulation).

The neuron is a delay-feedback LIF: a precharged membrane node, a positive-feedback inverter for spike generation, and a chain of current-starved inverters that sets spike width and refractory period independently. The same STP wiring is shown on a second, capacitive-refractory LIF topology, with modifications to slow it to millisecond operation.

## Evidenced (measured devices)

- Fabricated side-gated ECRAM, MoS2 channel, PEO:LiClO4 solid polymer electrolyte. Volatile transients measured with single gate pulses of about 2.2 s (the Fig. 8 caption says 2.5 s; capture ambiguity) at 0.1 to 2.5 V, drain current read at V_DS = 0.1 V; fitted by a double exponential (two Li+ populations).
- Variability from **three fabricated devices**, potentiation only: device-to-device 3.36%, cycle-to-cycle 2.77% (normalized standard deviation of output current).
- Device speed: this device shows no significant conductance rise for gate pulses much shorter than 1 ms. Earlier PEO devices responded to 7 ms pulses. 128 nonvolatile states come from the authors' prior work, not this paper.

## Simulated (not hardware)

All circuit results: Cadence, GlobalFoundries 55 nm PDK, 1.2 V devices, with a Verilog-A model fitted to the device data above.

| Regime | Input | Energy per output spike (simulated, whole circuit over one firing event) | Facilitation (spikes to fire drops by 1) |
|---|---|---|---|
| Delay-feedback, slow (1 ms spike) | 50 to 200 Hz | 2.4 to 2.6 nJ | neuronal mode: none at 50 Hz, partial at 1.25 s (100 Hz), full at 280 ms (200 Hz); synaptic mode: 540 / 170 / 70 ms at 50 / 100 / 200 Hz |
| Capacitive refractory (slow) | 100 Hz | about 8.2 nJ | neuronal: full after about 2.75 s; synaptic: full after 240 ms |
| Delay-feedback, "fast" | 100 kHz | 1.954 pJ (1.962 pJ with facilitation) | neuronal: full at 3.29 ms; synaptic: 2.19 ms partial, 3.72 ms full |

The "fast" row uses a **hypothetical faster ion conductor**: the paper scales the ionic timescales to what other literature reports for sub-microsecond to microsecond EDL formation and states this is not a prediction for the fabricated PEO device. The 2 pJ figure therefore belongs to a device nobody here built.

- STP adds essentially no energy (2.438 vs 2.439 nJ in the slow case; 1.954 vs 1.962 pJ in the fast case). The paper itself says the slow-regime energy exceeds previously reported CMOS LIF circuits.
- Monte Carlo (100 points; CMOS-only and CMOS plus ECRAM variability): functionality preserved; spread widens slightly with ECRAM variability (normalized energy spread 14.05% to 13.79% at state 1, 18.36% to 18.83% at state 128). Spike timing varies most at low conductance (near-threshold operation).
- Network level (snnTorch, normalized parameters, not hardware): facilitation-only synapses act as per-synapse high-pass filters, depression-only as low-pass, both together band-pass-like. The closed-form response matches simulation on a 1-D slice. A 10,000-sample Monte Carlo on the base weight shows gain, bandwidth and centre frequency move strongly with small weight variation; the authors say on-chip conductance tuning may be needed.

## Caveats the paper's numbers carry

- **Fast-regime energy is internally inconsistent.** Table 3 and the abstract give about 2 pJ per spike; the Monte Carlo at the same 100 kHz delay-feedback setup reports a mean of about 8 pJ (maximum 12 pJ), and Table 4 labels it fJ. The text does not reconcile this roughly 4x gap. Treat the energy as "pJ-scale, simulated, unreconciled".
- **Validation is in-sample.** The ionic parameters are extracted from the Fig. 8 transients and the model is then shown to reproduce the same transients. No held-out pulse width or amplitude is shown.
- **The effect is small and slow.** Facilitation changes the spike count needed to fire by one (for example 6 to 5), and in the slow regime needs over a hundred input spikes (1.2 s at 100 Hz) before it appears in neuronal mode. Relaxation of the device takes seconds.
- **"Negligible overhead" is argued for energy and component count; no area number is given** in the text. The delay-feedback path adds circuitry relative to a bare LIF, and the paper's own comparison table (check marks) did not survive capture.
- **No STP baseline.** Switched-capacitor and memristive STP circuits are dismissed qualitatively as area- or static-power-heavy; no measured or simulated head-to-head is given.
- **No task.** Workloads are constant-frequency spike trains into one neuron. Speech and biosignal use is motivation only.
- **Integration is not shown.** BEOL compatibility of solid electrolytes is a literature "potential"; the fabricated stack is planar MoS2/PEO. No endurance, retention or yield data for the volatile regime.
- **Reproducibility.** Data statement says all data are in the article. No code or model release is stated; the 55 nm PDK is proprietary.

## (synthesis)

- The paper reframes a nonideality (volatile conductance decay) as a feature, which is the opposite posture from [[analog-training-nonidealities]], where response-function asymmetry and drift are the failure mode. The two are compatible: STP here lives on top of a programmed nonvolatile state and avoids the doping regime. It says nothing on whether ECRAM updates are symmetric enough for training, so it does not move [[../conflicts/analog-onchip-training-viability]].
- It sits in the same evidence tier as [[vmtj-cmos-izhikevich-neuron]]: one measured device, a simulated neuron, a per-spike energy from simulation. Neither supports a system energy claim; compare with the boundary discipline in [[../snn/snn-energy-hardware-realistic]].
- The ECRAM row in [[../viability-ledger]] ("small array", Noh et al., primary not captured) is not corroborated by this source: it is single-device scale with a different electrolyte.

## Source

- `raw/research/weekly-2026-11-12/03-ecram-stp-neuron.md` (IOP *Neuromorphic Computing and Engineering* 6(4) 044012; doi 10.1088/2634-4386/aeb971). Derived summary: `raw/research/weekly-2026-11-12/.ingest/03-ecram-stp-neuron.summary.md`. The capture lost some Greek letters and units; figures used here are from the legible text and tables.

## Related

- [[memristor-device-engineering]] — RRAM-centred; its ECRAM stub predates this source and still stands for the Noh array claims
- [[analog-training-nonidealities]] — conductance linearity and response-function framing; this paper treats volatility as a resource, not a training nonideality
- [[vmtj-cmos-izhikevich-neuron]] — same pattern of one measured device plus simulated neuron energy
- [[cmos-rram-beol-integration]] — BEOL route that ECRAM solid electrolytes only "potentially" share
- [[../conflicts/analog-onchip-training-viability]] — not addressed by this source (no training)
- [[../snn/snn-energy-hardware-realistic]] — simulated per-spike energy versus measured system energy
- [[../viability-ledger]]
- [[../weekly-briefs/2026-11-12]] — brought in by the 2026-11-12 weekly sweep
