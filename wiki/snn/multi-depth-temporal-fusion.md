# Multi-depth temporal fusion (local STDP/R-STDP SNN)

A Padua preprint (Attar, Cicciarella, Rossi; arXiv 2609.37047) trains a four-layer convolutional time-to-first-spike (TTFS) SNN with **local rules only** — layerwise unsupervised STDP for the backbone, R-STDP for the readout, no backprop, no surrogate gradients — and adds a deterministic fusion of early, intermediate and deep spike-latency codes (MDTF). It claims +18.2 pp on Fashion-MNIST and +29.2 pp on CIFAR-10 over a prior STDP/R-STDP baseline. **Simulation only: no energy, latency, power or hardware figures anywhere.** Code is released.

The contrast case to [[snn-training-surrogate-gradients]]: BPTT's non-locality is why on-chip training is hard, and this is the no-gradient alternative. The accuracy ceiling is low, and the headline gain is confounded by a new hand-built front end.

## The method

- **Front end (deterministic, label-free):** local patch decorrelation (zero-phase covariance whitening fit on training patches), signed-context gate, polarity split, calibration, then latency coding (stronger response = earlier spike, weak = silent). Event data (N-MNIST): denoise, 5 temporal bins × 2 polarities, log compression, local normalisation, then latency coding. Statistics are fitted on the training split and frozen.
- **Backbone:** S1–S4 convolutional spiking layers, one spike per feature, layerwise unsupervised STDP with winner selection; each layer frozen and cached before the next. Min-latency pooling.
- **MDTF (the contribution):** final code `H = [H1, TopK(H2), agreement(H2,H4)]`. The agreement term keeps the earlier of two events at the same feature location only if the intermediate and deep latencies match within 0.001 normalised latency. No learned parameters, no plasticity. Rationale: local learning cannot recover information an earlier stage suppressed, so depth is treated as spike-time *routing* with deep features admitted only by temporal agreement.
- **Readout:** one fully connected spiking layer, 4–8 prototypes per class, global winner-take-all by earliest spike. "R-STDP" here is graded and margin-based, uses class labels per sample, and applies anti-STDP to the most-violating wrong classes — closer to a supervised margin loss in spike times than a binary reward. Updates are online, but only after the backbone is frozen.

## Results (software test accuracy)

Mean ± std over **readout seeds only**; backbone-seed variance not stated.

| Dataset | Accuracy | Events/sample | Density |
|---|---|---|---|
| MNIST | 96.6 ± 0.6 | 994.5 | 5.71% |
| Fashion-MNIST | 86.3 ± 0.7 | 1,182.3 | 6.79% |
| CIFAR-10 | 62.5 ± 0.4 | 3,100.6 | 12.6% |
| N-MNIST | 95.1 ± 0.6 | 1,992.7 | 8.07% |

Versus the Mozafari 2019 STDP/R-STDP baseline: MNIST 97.0 → 96.7 (no gain, acknowledged), F-MNIST 68.2 → 86.3, CIFAR-10 33.3 → 62.5, N-MNIST 22.0 → 95.0. The N-MNIST +73 pp compares against a raw-event "direct-transfer diagnostic" with no preprocessing and is not a real baseline.

## What the evidence supports

- **Confounded gain.** The front-end ablation shows raw-intensity latency coding collapses to chance (MNIST 9.8, F-MNIST 10.0, CIFAR-10 9.8) while the full front end reaches 96.7 / 86.3 / 62.5. The gain over the baseline is not cleanly attributable to MDTF; its own contribution is shown only as figure-level pp changes versus the P-only route.
- **Weak ceiling.** 62.5% CIFAR-10 and 86.3% F-MNIST are far below BP-trained SNNs and ANNs (>90% / >93%). The paper frames this as a local-learning result but gives no ceiling reference and no comparison to surrogate-gradient SNNs, conversion (see [[ann2snn-differential-coding]]) or a same-size ANN.
- **"Data efficiency" means sparse, not sample-efficient.** Accuracy rises monotonically from 100 to 30k training examples with no saturation, and has no baseline curve. The spike-budget Pareto (accuracy vs fraction of events kept, readout retrained) is an event-count proxy, not energy.
- **"Fully local" is hybrid.** Thresholds, top-k, margins and epochs are tuned per dataset (App. A Tables 6–8) and static-image statistics are fitted dataset-wide.

## Energy relevance

*(synthesis)* No energy claim is made, so this does not enter [[../conflicts/snn-energy-payoff]]. It is an instance of the pattern in [[snn-energy-hardware-realistic]]: a sparsity or event-count figure standing in for energy with no memory-system or hardware boundary. The 5.7–12.6% activity density and one spike per feature sit near the neighbourhood of the break-even spike-rate in [[snn-energy-breakeven-conditions]], but there is no timestep- or capacity-matched ANN comparison to place it on either side.

N-MNIST is saccade-converted MNIST, not a real sensor, and the front end densifies events back into 5 × 2 frames — the gap noted in [[../devices/event-cameras]]. NeuroBench system-track metrics ([[../benchmarks/neurobench]]) are not reported.

## Maturity and commercial signal

Algorithmic proof-of-concept on ≤32×32 benchmarks; below "single device". No hardware mapping, no device model (cf. [[../devices/analog-training-nonidealities]] for what STDP-class updates would face on real synapses). Hardware appears only as motivation and future work ("direct activity and energy measurements"). No funding, partners or products; Loihi and DYNAP-SE2 are background citations. No commercial gating variable in [[../viability-ledger]] moves.

## Reproducibility

Code released: `github.com/aidinattar/multi-depth-temporal-fusion-snn`. Datasets public (MNIST, F-MNIST, CIFAR-10, N-MNIST); full per-dataset hyperparameters in App. A. Not stated: weights, backbone-seed variance. Authors disclose ChatGPT use for language editing only.

## Open questions

- Does MDTF's gain survive when the baseline gets the same front end?
- Does the sparse code deliver measured energy savings on fabricated silicon, or only the event-count proxy?
- Does the routing idea scale to larger event-based tasks and recurrent architectures (the authors' stated future work)?

## Source

- `raw/research/weekly-2026-10-01/05-multi-depth-temporal-fusion.md` — "Multi-Depth Temporal Fusion for Feedforward, Locally Trained Spiking Neural Networks", arXiv 2609.37047, Attar, Cicciarella, Rossi (Univ. Padua). Preprint; software simulation only; code released.

## Related

- [[snn-training-surrogate-gradients]] — the gradient-based taxonomy this sidesteps
- [[ann2snn-differential-coding]] — the conversion route the paper cites and does not compare against
- [[snn-energy-hardware-realistic]] — the "proxy metric, not energy" pattern
- [[snn-energy-breakeven-conditions]] — the spike-rate threshold this density sits near
- [[../conflicts/snn-energy-payoff]] — context only; no energy claim made here
- [[../benchmarks/neurobench]] — system-track metrics not reported
- [[../devices/event-cameras]] — saccade-converted N-MNIST, events densified to frames
- [[../devices/analog-training-nonidealities]] — device stress on local update rules
- [[../viability-ledger]] — no gating variable moved
