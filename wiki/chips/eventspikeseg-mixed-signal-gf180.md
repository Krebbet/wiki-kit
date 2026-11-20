# EventSpikeSeg: mixed-signal event-camera segmentation in GF180 (architecture study)

Iran Univ. of Science and Technology's EventSpikeSeg (arXiv 2611.18524, 2026-11-13, preprint) maps a 25-population spiking encoder–decoder for six-class event-camera semantic segmentation (DSEC) onto capacitor-based analog membrane storage plus shared analog update circuits in the open GF180MCU 180-nm PDK. **Evidenced (transistor-level simulation of extracted/laid-out modules, nothing fabricated):** 41.711 µW biased neuron core, 3.338 pJ positive-terminal energy for a 1.4 µs cell read, 0.531 mV drift of the selected state over a 5 ms extracted-tile hold. **The load-bearing finding is the state inventory, not the power number.**

## What was built

- **Workload:** 143,824 synaptic weights (~150k parameters) but **30,976,000 resident membrane states** (54,630,400 logical state identities) at 440×640. Parameter count says almost nothing about area/bandwidth for a spatially expanded recurrent SNN; the state does. (synthesis) This is the event-vision analogue of the KV-cache point: weights are cheap, persistent state is the cost.
- **Mapping:** 64-state capacitor banks, chronological 5-ms model updates (10 bins per 50 ms label window), digital event/address services, shared analog service modules (storage replication separated from compute replication).
- **Evidence level:** native component layouts and a hierarchical GDS "research assembly" (not a compact tape-out), 74 operating points over 22 module families, with transistor simulations distinguished from digital-library estimates.

## Numbers and their boundary

| Quantity | Value | Boundary |
|---|---|---|
| Neuron-core power | 41.711 µW | biased PLIF core, nominal, SPICE simulation; not system |
| Cell read energy | 3.338 pJ (positive terminal), 1.4 µs read | single cell, simulation |
| State drift | 0.531 mV over 5 ms hold | extracted tile, simulation, nominal (no mismatch) |
| mIoU, software checkpoint | 27.976% | held-out 6-class DSEC split; **software, not hardware** |
| mIoU, SPICE-calibrated behavioural forward pass | 24.26% vs 26.22% matched PyTorch | one full-resolution frame; compact 5-fF bank variant, assumed 1 mV RMS storage noise, external count/voltage calibration |

Authors state: physical full-network operation, system energy, mismatch robustness, and full-population real-time deadlines are **unverified**; no energy comparison to published processors is claimed. mIoU in the mid-20s is low in absolute terms (the task is hard at 6 merged classes).

## Assessment

(synthesis) Useful as an honest *negative-space* result: it quantifies why dense-prediction SNNs on analog capacitor memory hit a storage-replication wall (tens of millions of states × capacitor area), which is the same blocker pattern as [[../devices/memristor-array-integration-gap]] but on the volatile-state side. Compare measured-silicon neighbours [[ethereal-event-gnn-processor]] and [[dynapse-neuromodulation-gain-reservoir]]; this page is simulation/layout only. Code is public (github.com/st-amirr/EventSpikeSeg); circuit evidence is supplementary and not a one-command reproduction.

**Maturity:** paper-only architecture study on an open PDK; no silicon. No commercial signal.

## Source

- `raw/research/weekly-2026-11-19/01-eventspikeseg.md` (arXiv 2611.18524)

## Related

- [[../devices/event-cameras]]
- [[ethereal-event-gnn-processor]]
- [[dynapse-neuromodulation-gain-reservoir]]
- [[../devices/memristor-array-integration-gap]]
- [[../snn/snn-energy-hardware-realistic]]
- [[../viability-ledger]]
- [[../weekly-briefs/2026-11-19]] — brought in by the 2026-11-19 weekly sweep
