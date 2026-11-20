# Model-inversion leakage in memristive SNNs depends on hardware state (simulation)

Sorrentino and Covi (Univ. Groningen; arXiv 2610.39688, v2, 2026-10-29) ask whether privacy leakage measured on a software SNN carries over after the model is mapped to a non-ideal memristive crossbar. They introduce **SDMI** (Spiking Domain Model Inversion: Expectation-over-Transformation plus surrogate gradients, to invert through stochastic analog behaviour and non-differentiable spikes). **Evidenced (simulated memristive-substrate models, four datasets; no fabricated hardware):** leakage does not track accuracy or variability monotonically.

## Findings

- At comparable accuracy, **neuron-threshold perturbations raise reconstruction fidelity (SSIM) by up to 51.8%** relative to the memristive baseline.
- **Weight noise reduces leakage** (−35.7% reconstruction similarity) under the same inversion procedure.
- Spike deletion degrades accuracy comparably to threshold shift but leaves reconstruction ≈ baseline; spike-level perturbations mainly cost utility.
- Conclusion: hardware variability is not inherently privacy-preserving; leakage is a property of the deployed hardware state (including reliability faults), not inferable from accuracy.

Boundary: attacker is white-box on a simulated device model; SSIM numbers are relative changes, absolute fidelity and per-dataset values were not extracted here (see source). Device non-ideality models are generic ReRAM-style (NeuroSim-lineage references), not measured from a specific array.

## Assessment

(synthesis) Peripheral to the viability timeline but a new axis for edge-deployment claims: "analog noise gives you privacy for free" is not supported, and fault drift over device lifetime changes the leakage profile. Pairs with [[../devices/analog-training-nonidealities]] as another case where nonidealities have non-monotonic, non-obvious effects.

**Maturity:** simulation only; no commercial signal.

## Source

- `raw/research/weekly-2026-11-19/03-memristive-snn-model-inversion.md` (arXiv 2610.39688)

## Related

- [[../devices/analog-training-nonidealities]]
- [[../devices/memristor-device-engineering]]
- [[spike-encoding-iot-sensing]]
- [[../weekly-briefs/2026-11-19]] — brought in by the 2026-11-19 weekly sweep
