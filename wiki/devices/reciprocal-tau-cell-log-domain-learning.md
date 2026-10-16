# Reciprocal τ-cell: log-domain circuit for on-chip learning

Jin and Chaffey (University of Sydney) propose a weak-inversion, log-domain CMOS circuit in which symmetric connections let a second, latched run of the same network yield the gradient. **Everything is transistor-level SPICE (ngspice, SKY130 typical corner); there is no layout or silicon**, and several blocks (comparator, switches, current sources/DACs, the d·x products) are ideal in simulation.

## Circuit

A τ-cell is a current-mode leaky integrator (translinear loop plus capacitor, τ = nCU_T/I₀). A connection is two transistors whose signed weight is a ratio of bias currents set by a 6-bit digital code; one code drives both directions, so W = Wᵀ by construction. The network is a continuous-time ReLU equilibrium network (monDEQ-style): the equilibrium is the solution of a convex quadratic program. Learning is EqProp-like: a free run, then two latched runs give d = (I − W_AA)⁻¹ê exactly for any error amplitude that keeps active cells on, and the update is −η(dᵢxⱼ + dⱼxᵢ). Static vector-to-vector tasks only.

## Simulated numbers (SKY130, 1.8 V, C = 1 pF, I₀ = 5 nA)

- Cell τ: 51 / 11 / 2.9 µs at I₀ = 1 / 5 / 20 nA. Copy error within ±2% over 0.5–60 nA.
- Six cells, ten pairs: 0.26 µW (inference circuit, ideal sources excluded; not a learning-energy figure).
- Gradient error 1.9% vs finite-difference gradient of the same simulated circuit, six cells. With 20 pA rms readout noise, latching holds 1.3% at 14 nA error amplitude where the unlatched version fails (36–52% at 10–14 nA).
- Threshold-offset mismatch: median gradient error 1.3% → 3.1% at 1 mV; 7.9% / 6.7% / 16% (cell / connection / all) at 3 mV, 5 draws each. SKY130 predicts ≈1.3 mV for these devices.
- Iris (4-6-3, 42 pairs, ≈600 transistors, 30 epochs): circuit 90.0% test, same as software exact-gradient 90.0%.
- Mismatch recovery: software weights copied into mismatched circuits keep median 86.7% at 3 mV and 76.7% at 5 mV (worst draw 53%); learning in situ lifts the four worst draws from 53–63% to 88–96%.

## Caveats

Iris with 30 test samples gives ≈3.3-point resolution; the recovery baseline is software weights copied with no mismatch-aware retraining, and the "four worst" draws were selected after the fact. Only threshold mismatch, typical corner. A current DAC per pair (dominant area) and a translinear multiplier per weight are still needed, so the learning loop is not closed in transistors. Connection mismatch breaks symmetry, which no rescaling fixes in loops of three or more cells; calibration of cell offsets is claimed, not shown. Code/netlist release not mentioned.

## Relevance to the open conflict

(synthesis) It is a simulation-only data point that in-situ learning can absorb circuit mismatch. It does **not** settle [[../conflicts/analog-onchip-training-viability]]: weights are digitally coded bias currents, with no asymmetric or nonlinear analog memory device, so the response-asymmetry failure in [[analog-training-nonidealities]] never arises.

## Source

- `raw/research/weekly-2026-10-15/05-reciprocal-tau-cell.md` — arXiv 2610.20018. Builds on the τ-cell (van Schaik and Jin 2003) and Chaffey's linearised monDEQ work (arXiv 2509.13793). No commercial signal; targets low-power edge learning (claimed, undated).

## Related

- [[../conflicts/analog-onchip-training-viability]] — simulated counter-example on mismatch, not on asymmetry
- [[analog-training-nonidealities]] — contrast: digital weights sidestep response asymmetry
- [[two-state-synapse-equilibrium-propagation]] — the device-side counterpart of EqProp-style learning
- [[memristor-array-integration-gap]] — DAC-per-pair overhead echoes the peripheral cost theme
- [[../chips/megatron-pcm-cim-soc]] — silicon-measured analog CIM, for contrast
- [[vmtj-cmos-izhikevich-neuron]] — another simulated-circuit entry
- [[../snn/snn-training-surrogate-gradients]] — non-spiking local alternative to BPTT
- [[../weekly-briefs/2026-10-15]] — brought in by the 2026-10-15 weekly sweep
