# Loihi 2 — acoustic anomaly detection for persistent machine monitoring

The wiki's first primary Intel Loihi 2 source. LANL, AeroVironment, the University of New Mexico and AFRL map a dense autoencoder to fixed-point integer arithmetic and deploy it on a 16-chip Loihi 2 VPX embedded system for one-class acoustic anomaly detection (machine condition monitoring), with directly measured latency, power, energy, memory and activity — not simulation. It fills a gap this wiki had flagged since bootstrap: Loihi 2 / Hala Point "named repeatedly, never sourced directly."

## Device / chip

Intel Loihi 2, evaluated as a **16-chip VPX embedded system** (VPX = a defense/aerospace embedded-computing form factor, consistent with AeroVironment/AFRL co-authorship). Process node and foundry are not stated. A single-chip Loihi 2 platform ("Oheo Gulch," per an Intel Labs tech brief) is discussed but **not directly measured** — its numbers are a scaled projection from prior work, explicitly caveated by the authors as needing direct measurement. Hala Point is not mentioned anywhere in this source.

## Workload

Not a temporally-coded spiking network trained by surrogate gradient or STDP — the "spiking" framing is loose. The deployed model is a **conventional dense autoencoder** (256→128→64→bottleneck→64→128→256, bottleneck 32 units clean / 12 units noisy, leaky-ReLU), trained off-chip in floating point (Adam), then quantized to fixed-point integers (8-bit weights, 24-bit accumulators/activations) and mapped onto Loihi 2's neuromorphic cores as an integer-arithmetic dataflow graph. Only inference runs on-chip; log-mel feature extraction stays off-chip/host-side — the authors call this "the principal limitation."

Task: one-class (normal-only training) acoustic anomaly detection. Datasets: ToyADMOS ToyCar (clean) and DCASE 2026 Task 2 ToyCar dev set (noisy, near-channel only).

## Measured numbers

**Detection accuracy** (Table 1): clean ToyADMOS AUC 0.9959; noisy DCASE 2026 source/target/pAUC = 0.7990 / 0.6466 / 0.6426, beating the published DCASE baseline (0.7728 / 0.5317 / 0.5825) on all three metrics. Caveat stated by the authors: the noisy result is development-set, not blind challenge-evaluation, since labeled dev data informed model configuration.

**Latency / power / energy** (Table 2, per-sample, autoencoder inference only, batch size 1, 1M measured inferences):

| Hardware | Latency (µs) | Total power (W) | Total energy (mJ) | Dynamic energy (mJ) |
|---|---|---|---|---|
| Loihi 2 VPX (16-chip), Ethernet I/O | 281.0 | 16.20 | 4.554 | 0.0426 |
| Loihi 2 VPX (16-chip), preloaded input | 48.3 | 16.89 | 0.816 | 0.0406 |
| Xeon E5-2660 v3 CPU (2014-era) | 420.3 | 77.96 | 32.769 | 20.156 |
| Tesla V100S GPU (2019-era) | 163.5 | 58.35 | 9.540 | 5.350 |

Core/memory footprint: 74 neuromorphic cores occupied; single-chip memory utilization 20.36%, system-wide 1.27%. Per-inference: ~3.0×10⁵ synaptic operations, 1.0×10⁴ neuron updates, 2.0×10⁴ input and output spike events.

## Baseline and comparison honesty — the headline number is boundary-dependent

This is the load-bearing finding for the wiki. The abstract's "two orders of magnitude lower than both a CPU and GPU" claim holds only for the **dynamic-energy-only** boundary:

- **Dynamic-only:** ~474–496× less than CPU, ~126–132× less than GPU.
- **Total energy** (same Table 2, static platform power included): **7.2–40.2× vs CPU, 2.1–11.7× vs GPU** — roughly an order of magnitude lower than the dynamic-only headline.

Static VPX power (16.05 W, measured) is dominated by an underutilized infrastructure running a model that occupies only 74 of ~2,048 available cores — it swamps the per-sample dynamic-energy advantage once counted. The abstract does not make this boundary distinction explicit; a reader taking only the abstract would over-credit the efficiency claim. This is a clean, same-paper, same-hardware illustration of exactly the measurement-boundary problem tracked in [[../conflicts/snn-energy-payoff]] — see that page for the full cross-source picture. (Scope note: because the deployed model is a fixed-point dense autoencoder rather than a trained SNN, treat this as chip/systems evidence for the boundary problem, not as an SNN-algorithm data point.)

Secondary baseline flags: both reference chips (2014 CPU, 2019 GPU) are old generations, not current efficient-inference silicon; batch size 1 on GPU is a worst-case underutilization scenario. GPU host-device transfer was explicitly excluded from GPU timing, disclosed by the authors as intentionally not disadvantaging the GPU.

## Maturity

Real, directly measured silicon (Keysight N6705C power analyzer, on-board probes) — a fielded/deployable defense-embedded form factor, not a lab bench demo or simulation. Single-chip numbers remain unvalidated projections.

## Commercial signal

Government-funded research (Los Alamos National Laboratory lead, DOE/NNSA Defense Nuclear Nonproliferation funding; AeroVironment and AFRL co-authors), not a vendor product announcement. No pricing, shipment, or customer claims. Signal is indirect: defense/national-lab interest in Loihi 2 for persistent low-power sensing, evidenced by funding and co-authorship, not by any commercial claim.

## Blockers stated

Feature extraction remains off-chip (named as the principal limitation); single-chip deployment unverified; only one machine class (ToyCar) evaluated; no online/on-chip adaptation to changing conditions.

## Novelty

Not a new device, neuron model, or training method — a systems recombination: applying an established reconstruction-autoencoder one-class approach to Loihi 2 for acoustic machine-condition monitoring, with (per the authors) the first evaluation combining this task on Loihi 2 with full measured latency/power/energy/memory/activity against CPU and GPU baselines.

## Reproducibility

No code, weights, or trained-model release. Datasets are public benchmarks (ToyADMOS, DCASE 2026 Task 2 dev set); the Loihi 2 deployment pipeline itself is closed.

## Source

- `raw/research/weekly-2026-08-20/02-loihi2-acoustic-anomaly-detection.md` — "Low-Power, Neuromorphic, Acoustic Anomaly Detection for Persistent Machine Monitoring" (arXiv:2608.18341, LA-UR-26-26527). Primary, government/academic.

## Related

- [[../conflicts/snn-energy-payoff]] — same-paper dynamic-vs-total energy split as boundary-clean evidence
- [[../benchmarks/neurobench]] — this paper's own dynamic/total/static power split parallels NeuroBench's system-track convention
- [[../players/roster]] — Intel/Loihi 2 entry
- [[../weekly-briefs/2026-08-20]] — brought in by the 2026-08-20 weekly sweep
