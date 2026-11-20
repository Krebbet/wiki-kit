# Device-informed STDP on a threshold memristor model (simulation)

ArXiv 2610.xxxx-series preprint "State-Dependent Memristor Dynamics for Device-Informed STDP in SNNs" (arXiv 2611.00119, 2026-10-28) couples local STDP commands (programming polarity + magnitude via a "programming coordinate") to a literature-derived threshold-memristor state-update equation, trains the first FC layer with it, and uses a backprop-trained readout. **Evidenced (HSPICE compact-model simulation + network-level software experiments; no fabricated devices):** the device-informed update changes what local STDP learns and how it fails. **Not evidenced:** any physical pulse-accurate programming; the network-level mapping is a "validation-selected, reduced-order abstraction" by the authors' own statement.

## Results and boundary

| Result | Value | Boundary |
|---|---|---|
| Hybrid (STDP→memristor state update + BP readout) | 95.15 ± 0.17% MNIST, 85.92 ± 0.23% Fashion-MNIST | class-balanced test subsets, simulation, compact-model abstraction |
| vs direct clipped "ideal" STDP (seed-matched) | +2.69 / +1.54 pts (95.02/84.79 vs 92.33/83.25%) | same protocol; Holm-corrected p=1.1e-4 |
| Direct-input linear readout | 92.65% / 84.05% | so STDP layer adds ~2.5 pts on MNIST over raw pixels |
| Normalisation off | Hybrid 94.31 / 83.91% vs ideal STDP 90.74 / 82.25% | epoch-wise column normalisation is algorithmic, **not a physical memristor operation**; needs extra circuitry |

- **Asymmetry:** potentiation-dominant update asymmetry (A+ ≫ A−) caused rapid loss of feature selectivity on MNIST (collapse persisted); single-polarity programming did worse than normalisation-only, bidirectional nominal amplitude did better.
- **Faults:** endpoint (stuck) faults present *during* training cost far less accuracy than the same faults injected after training — i.e. fault-aware (in-situ) learning absorbs them; consistent with [[analog-local-learning-imperfect-synapses]].
- Ideal signed-weight BP beat Hybrid in every configuration; device-programmed ("Memristor") BP was similar to Hybrid at 1024 hidden / batch 128 without normalisation, with larger seed variance when normalised.

## Assessment

(synthesis) Another data point that local-learning accuracy on analog synapses is dominated by *update asymmetry and state dependence* — the same linearity/symmetry blocker tracked in [[analog-training-nonidealities]] — and that MNIST-class accuracies say little about viability. Small-scale benchmark (MNIST/FMNIST, reduced crossbar); no array endurance, retention or variability measurement.

**Maturity:** simulation only.

## Source

- `raw/research/weekly-2026-11-19/02-memristor-stdp-state-dependent.md` (arXiv 2611.00119)

## Related

- [[analog-local-learning-imperfect-synapses]]
- [[analog-training-nonidealities]]
- [[memristor-device-engineering]]
- [[../conflicts/analog-onchip-training-viability]]
- [[../weekly-briefs/2026-11-19]] — brought in by the 2026-11-19 weekly sweep
