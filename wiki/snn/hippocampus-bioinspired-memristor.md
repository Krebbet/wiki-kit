# Bio-realistic neuronal-diversity SNNs on memristor hardware

A George Washington University / George Mason University demo (Kilgore, Kopsick, Ahmed, Ascoli & Adam; arXiv:2609.16429) downscales a biologically-realistic 89,226-neuron rodent CA3 hippocampal SNN model down to 179 Izhikevich neurons across 3 cell types (160 pyramidal, 12 MFA ORDEN, 7 basket) and maps it onto the "Daffodil" FPGA + memristor-crossbar prototyping board (20,000 devices, 32 kernels of 25×25). The claim is narrowly and correctly scoped: **first** demonstration of *neuronal-diversity*, biologically-realistic **resting-state (periodic) dynamics** on memristive hardware — not the first SNN-on-memristor demo generally, and not a task-trained network. This is a new category for the wiki: no training (no surrogate gradient, no STDP, no ANN-to-SNN conversion) — the network is tuned to match dynamical statistics, not to classify anything.

## What it does

The full-scale CA3 model (Kopsick et al. 2023, same group) is downscaled via log-domain power-law scaling (exponent 2/3 for neuron population, 1 for synapse count) to a target size, then an Optuna hyperparameter search (2,000 trials) tunes connection probabilities and background input current against a 4-term objective: activity score (0.4) + periodicity score (0.4) + firing-rate-match (0.1) + minimal-connectivity-change (0.1). Conductances are written once to the memristor array — no on-chip learning is demonstrated (explicitly deferred). A custom greedy blocking algorithm maps the sparse biological connectivity matrix onto fixed hardware kernel blocks; empirically, 12×1 and 5×1 blocks outperformed square blocks at preserving the target periodicity.

## Measured numbers

- Scale: 179 neurons, 17,996 synapses (simulation) mapped to **18,316 physical memristors** (extra devices from block-mapping overhead).
- Objective score (0–1, paper-defined, not a standard benchmark) for the final network: CARLsim6 software tune 0.9201 → simulated (non-noisy) hardware model 0.7807 → **physical hardware 0.8679**. Physical hardware beats the simulated-device model but slightly trails the pure-software tune — hardware noise, in this specific narrow comparison, *improves* the score relative to the noiseless hardware model.
- Device write error (90 target conductance levels) and read error (5,760 reads): "near-zero mean, larger std for write than read" — no numeric σ given in the body text.
- Hardware run: 3,000 ms of simulated network activity took **10 days of wall-clock time** (100 ms per read operation, no kernel-level parallelization).
- Spiking distribution on hardware: pyramidal cells produced 71.7% of all transmissions over the 3,000 ms trial; MFA ORDEN cells had the highest per-neuron rate (7,887 events/neuron).
- E:I ratio 89:11 by neuron count; spiking-activity split 80:20 (CARLsim) vs 83:17 (physical hardware).
- Stuck devices: "a substantial portion" pinned at high conductance — no percentage given.

**Power: explicitly incomplete.** The paper's only energy figures (average power per device read, per-neuron power) are presented graphically only, and the text states they **exclude DACs, ADCs, and other IO** — i.e. the one energy claim in the source is device-only and admittedly leaves out the part of the system this wiki's own [[../devices/memristor-array-integration-gap]] page identifies as typically >70% of system power. No J/synaptic-op or J/inference figure is given. This reinforces, rather than contradicts, that page's thesis — a second primary source making the same omission transparently.

## Baseline and comparison honesty

The central comparison (physical hardware 0.8679 vs. simulated-hardware-model 0.7807 vs. software CARLsim 0.9201) is internally consistent and boundary-honest — same network, same scoring function throughout. The paper is also self-critical about cross-version drift: it flags that the full-scale network's "perfect" firing-rate score is an artifact of originally being fit with CARLsim4, while this work uses CARLsim6, which produces different firing-rate outputs. No GPU/Loihi/SpiNNaker energy comparison is attempted against this system's own numbers — the GPT-3-training-energy framing in the introduction is scene-setting, not a measured claim about this system.

## Maturity

Single prototyping-board demonstration — "first generation memristive device platform," in the authors' own words. FPGA + mixed-signal daughterboard + 20,000-device crossbar (Daffodil, originally published 2021 by the same group). No foundry, process node, or ASIC tape-out. Several rungs below even a lab-scale integrated chip; the 10-day runtime for one 3-second-simulated trial underscores how far this is from throughput-viable.

## Blockers stated

- Stuck devices (pinned high, unprogrammable) — worked around via baseline-current subtraction at init, not solved; authors say it "needs to be addressed at the device fabrication level."
- Device read/write variability requiring per-device calibration.
- 25×25 kernel size forces structured, non-random connection blocks, reducing synaptic diversity relative to the ideal random network — the direct algorithmic cost of the crossbar constraint.
- No kernel-level parallelization; DAC/ADC overhead described as "considerable" and excluded from the power estimate — the throughput bottleneck behind the 10-day runtime.
- Firing-rate score collapses toward 0 at the smallest, most-homogeneous scales — smaller downscaled networks compensate for realism loss with elevated firing rates, a limitation of the scaling methodology itself.
- No on-chip learning demonstrated; explicitly future work (target conductance chosen mid-range partly in anticipation of this).

## Commercial signal

None — purely academic (GWU/GMU), funded by DOE Office of Science ASCR and AFOSR. No companies, partnerships, or availability dates.

## Reproducibility

Code and analysis scripts are public: https://github.com/ADAM-Lab-GW/Downscaled-CA3-Tuning (data via Git LFS in the same repo). A substantive release — source control plus docs — though no independent reproduction has been reported yet.

## Source

- `raw/research/weekly-2026-09-24/02-hippocampus-memristor-snn.md` — "Scaled Hippocampus-inspired Neural Networks on Neuromorphic Memristive Hardware" (Kilgore, Kopsick, Ahmed, Ascoli & Adam; arXiv:2609.16429). Academic primary, captured via arXiv PDF.

## Related

- [[../devices/memristor-array-integration-gap]] — this source's own DAC/ADC/IO-excluded power figure reinforces that page's ">70% of system power" finding
- [[snn-energy-hardware-realistic]] / [[../conflicts/snn-energy-payoff]] — another SNN-on-real-hardware paper that stops short of a full-stack energy claim; reinforces rather than resolves the open conflict
- [[snn-training-surrogate-gradients]] — contrast, not extension: this network is hyperparameter-tuned to dynamical statistics via Optuna, not trained to a task via surrogate gradient or STDP
- [[../weekly-briefs/2026-09-24]] — brought in by the 2026-09-24 weekly sweep
