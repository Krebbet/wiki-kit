# ETHEREAL: event-driven graph neural network processor

The wiki's first entry in a category distinct from both SNN chips and analog memristive accelerators: a fabricated, digital CMOS ASIC (TU Delft / KU Leuven / UZH / UPenn, TSMC 28 nm via the academic University Shuttle Program) that processes event-camera (DVS) output natively as a sparse spatiotemporal graph, rather than densifying events back into frames first. Headline, **silicon-measured**: 25.6 µs latency and 1.7 µJ per event on the DAGr-GNN workload at 640×480 DVS resolution — claimed as 10–1000× better than prior event-driven GNN and SNN hardware. Funded in part by **Prophesee** (event-camera vendor already tracked on [[../players/roster]]) via a Dutch HTSM-TKI programme.

## What it is

Each new DVS event becomes a node in an evolving spatiotemporal graph; message-passing uses spline convolution (Fey et al., CVPR 2018) to encode relative event position into learned weights via bilinear spline coefficients — up to 2× the accuracy of linear graph convolution at up to 8× more compute. The chip splits work into a memory-bound 3D (x,y,t) stage and a compute-bound 2D stage after temporal pooling, backed by 1.25 MB of on-chip SRAM (an 8-way associative 3D spatiotemporal cache + a 16-bank 2D-interleaved scratchpad) and eight parallel 4×64 MAC-array "message-passing" cores. No embedded non-volatile memory — pure SRAM + digital logic, unlike every device-family page elsewhere in this wiki.

The underlying algorithm (SplineCNN) and workload (DAGr-GNN, Gehrig & Scaramuzza, *Nature* 2024) are both prior work; ETHEREAL's contribution is the hardware architecture — specifically the split 3D/2D memory hierarchy and an 8-core neighbor-parallel spline-convolution datapath with reconfigurable linear/spline MAC modes.

## Measured numbers (chip-measured unless noted)

- Process/area/power: TSMC 28 nm, 3.7 mm² die, up to 250 MHz @ 0.95 V (Table I lists 280 MHz), supply range 0.6–1 V, total power 63.2 mW.
- System-level per-event latency: 17.8–36.5 µs; energy: 1.1–2.3 µJ (both @0.95V, precision-dependent).
- Headline (DAGr-GNN on DSEC, 640×480): **25.6 µs latency, 1.7 µJ/event.**
- 3D cache: hit rate up to 58% → 2.4× reduction in read external-memory accesses; cache-miss path runs 10× slower than the hit path.
- Pipelining graph-building with other ops cuts total latency 1.8×.
- Normalized peak throughput 16 TOPS/b, peak efficiency 113 TOPS/W/b — **linearly normalized to 1-bit precision, not an as-measured operating point.**

## Baseline and comparison honesty — several boundary issues

- **GPU baseline is FP64 on an A100.** FP64 is not a realistic inference precision; comparing a 4–8b custom ASIC against FP64 inflates the apparent gap (140 ms → 25.6 µs, 400 mJ → 1.7 µJ) well beyond what a properly-configured FP16/INT8 GPU baseline would show. The paper doesn't flag this mismatch.
- **The headline "comparable accuracy" claim is not chip-measured end-to-end.** Only latency/energy/power come from real silicon; accuracy (N-CARS 86.7%, N-Caltech101 48.1%, DSEC 7.6%) is explicitly footnoted as "end-to-end accuracy simulated with HW model... measured end-to-end validity on synthetic data."
- **Accuracy actually trails the GPU baseline on every dataset shown** (86.7 vs 90.7 N-CARS; 48.1 vs 52.6 N-Caltech101; 7.6 vs 12.4 DSEC) — "comparable accuracy" glosses over a consistent deficit traded for latency/energy.
- **The 10–1000× headline spans a heterogeneous table**: different years (2021–2026), different tech nodes (14/28/40 nm/FPGA/A100), different max resolutions (≤240×180 for prior work vs. 640×480 here) — not a matched-resolution, matched-precision comparison. One comparator figure (3.8× spline-skipping gain) is explicitly extrapolated from a cited reference, not measured chip-vs-chip.

This is the same comparison-honesty pattern already catalogued in [[../snn/snn-energy-hardware-realistic]] and [[../conflicts/snn-energy-payoff]] — heterogeneous baselines, unstated precision mismatch, boundary-shifted accuracy — here for a non-spiking GNN accelerator rather than an SNN.

## Maturity

Fabricated test chip via TSMC's academic University Shuttle Program (MPW access, not a standalone commercial tape-out). Electrical/timing/power are silicon-measured; task accuracy stops at hardware-model simulation on synthetic data — not yet demonstrated end-to-end on live DVS camera input on the chip itself. No packaging for product use, no further foundry engagement stated.

## Blockers stated

- 3D-layer memory-boundedness only partially solved (58% cache hit rate ceiling; a miss costs 10×).
- Spline convolution's 8× compute cost over linear graph convolution requires dedicated multi-cycle MAC hardware to hold area overhead below 30%.
- Explicit precision/accuracy tradeoff, and accuracy trails the GPU baseline even at the reported operating points.
- No resolution of the simulated-vs-real-hardware accuracy validation gap.

## Commercial signal

Academic only. Prophesee (evidenced, funder via HTSM-TKI) and TSMC (evidenced, academic fab access) are named, but neither is a customer or product-adoption signal. No product name, customers, or availability date.

## Reproducibility

No code, RTL, dataset splits, or trained-weight release mentioned. Independent reproduction would require re-fabrication access via TSMC's University Shuttle Program.

## Source

- `raw/research/weekly-2026-09-24/04-ethereal-event-gnn-processor.md` — "ETHEREAL: A 25-µs/inf Event-driven Graph Neural Network Processor" (Kneip, Verhelst, Frenkel, Scaramuzza et al.; arXiv:2609.15241, accepted ESSCIRC 2026). Academic primary, captured via arXiv PDF.

## Related

- [[../devices/event-cameras]] — extends that page's "processing gap" note (most pipelines densify events back into frames); ETHEREAL is a concrete, chip-measured counterexample that keeps data sparse end-to-end
- [[../snn/snn-energy-hardware-realistic]] — parallel comparison-honesty case study (heterogeneous-baseline multiplier claims), though the accelerator here is GNN, not SNN
- [[../conflicts/snn-energy-payoff]] — the pattern this source's headline multiplier fits, even though it isn't itself an SNN energy claim
- [[../players/roster]] — Prophesee funding link; TU Delft already listed as a NeuroBench co-author institution
- [[../viability-ledger]] — a chip-measured microsecond-latency/microjoule datapoint for edge event-vision processing
- [[../weekly-briefs/2026-09-24]] — brought in by the 2026-09-24 weekly sweep
