# Two-state synapses for Equilibrium Propagation

Liu and Grollier (CNRS/Thales, Laboratoire Albert Fert) show in theory and software that a synapse with a **volatile state w** and a **non-volatile state M** can carry Equilibrium Propagation's (EqProp) free-vs-nudged comparison in its own dynamics, matching standard EqProp on MNIST. No device was built, simulated at device level, or measured; the paper's contribution is a device requirement spec. It is the wiki's first EqProp / local-contrastive-learning source and an alternative route to the SGD-on-analog-array problem in [[../conflicts/analog-onchip-training-viability]].

## Mechanism

EqProp trains an energy-based network by relaxing it twice (free, then weakly nudged toward the target) and updating each weight from the difference of local products, with no separate backward pass. Here the volatile state relaxes toward ρ(uᵢ)ρ(uⱼ) and the non-volatile M accumulates the change: phase-based dM = (η/β)(w_nudged − w_free); continual form integrates dw/dt under a global gate. Variant A uses effective weight g·w + M (energy-coupled); Variant B uses M only, so w can be switched off at inference (hardware-oriented, but its success is empirical since it breaks the common-energy derivation).

## Stated device requirements

1. Volatile state with finite relaxation time. 2. Non-volatile state dominating the conductance. 3. Transfer of the *change* of the volatile state (not its value) to the non-volatile state, gated by a global signal (magnetic field or temperature suggested). 4. Reset between examples. Existing eligibility-trace devices transfer instantaneous value, not the derivative, so no known device has the required coupling.

## Results (simulated, software, MNIST, 784-512-10 MLP, MSE, 10 runs)

| Scheme | Test error |
|---|---|
| EqProp phase-based (reference from Ernoult et al. 2020, not re-run) | 2.00 ± 0.13 % |
| Two-state A / B, phase-based | 2.01 ± 0.09 % / 1.98 ± 0.07 % |
| Continual EqProp (reference) | 2.28 ± 0.16 % |
| Two-state A / B, continual | 2.24 ± 0.11 % / 2.30 ± 0.09 % |

Differences are within one SD: the claim is "no degradation", not improvement. One hidden layer, MNIST only; no energy, area, endurance or retention numbers; continual runs use gradient clipping. All non-idealities (imperfect transfer, finite retention, variability, response asymmetry) are ideal and listed as future work, so the paper says nothing about the asymmetry problem in [[analog-training-nonidealities]]. Part of the text was edited with a generative model (disclosed).

## Reproducibility

Code released (github.com/neurophysics-cnrsthales/two_state_synapses_ep); MNIST public; hyperparameters in the paper's tables.

## Source

- `raw/research/weekly-2026-10-15/03-twostate-synapse-eqprop.md` — arXiv 2610.18058. Funding: ERC GrenaDyn, ANR PEPR IA.

## Related

- [[../conflicts/analog-onchip-training-viability]] — adds a non-SGD local-learning route, paper-only
- [[analog-training-nonidealities]] — the device non-idealities this paper leaves ideal
- [[memristor-device-engineering]] — volatile/non-volatile coexistence in one device
- [[memristor-array-integration-gap]] — no peripheral accounting here
- [[reciprocal-tau-cell-log-domain-learning]] — another EqProp-style circuit, SPICE-only
- [[../snn/snn-training-surrogate-gradients]] — comparison point for local learning vs BPTT
- [[../viability-ledger]] — on-chip learning stays paper-only
- [[../weekly-briefs/2026-10-15]] — brought in by the 2026-10-15 weekly sweep
