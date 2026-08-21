# Intel Loihi 2

The field's most-used research platform, and the reference point against which much of the published SNN energy literature is calibrated — which makes its architecture load-bearing well beyond Intel. Digital, fully asynchronous, no analog or memristive component anywhere. **Not for sale**: access is gated behind application to Intel's Neuromorphic Research Community (INRC), not open purchase or self-serve cloud.

Two things about Loihi 2 matter more than its spec sheet. Its **spikes are no longer one bit** — which quietly invalidates energy models calibrated on Loihi 1. And its **SDK was archived on 2026-05-13**, leaving the platform's reference toolchain frozen pending an unannounced replacement.

## Architecture

| Attribute | Value |
|---|---|
| Process | **Intel 4** — Intel's first product on that node |
| Neural cores | 128 programmable digital DSP-style cores, each with on-core connectivity memory |
| Embedded CPUs | 6 Lakemont x86 cores (standard C) for I/O, config, management |
| Interconnect | Asynchronous network-on-chip; asynchronous multi-chip scaling |
| Neurons / chip | up to **1,000,000** |
| Synapses / chip | up to **120,000,000** |
| Die | Higher transistor count than Loihi 1 at **half the die area** |

Per-core memory is not quantified in any captured source. Neither is chip power — see the gap section below.

**Programmable neuron models.** Loihi 2 moved past fixed leaky-integrate-and-fire: cores execute user-defined arithmetic/logic via microcode, supporting resonance, adaptation, custom threshold and reset behaviour. Program length, variable count and numerical precision trade against neuron capacity and energy — stated qualitatively, never quantified.

**On-chip learning.** Programmable spike-timing-dependent plasticity, and the platform is described as supporting **three-factor learning rules** (a superset of two-factor STDP, used for reward-modulated and eligibility-trace learning). Which rules are hardware-implemented versus merely expressible in microcode is not enumerated anywhere captured.

## Graded spikes — why Loihi-1-calibrated energy models don't transfer

Loihi 1 emitted **1-bit** binary spikes. Loihi 2 emits **graded spikes carrying up to 32-bit integer payloads**.

*(synthesis)* This is a bigger deal for this wiki than it looks. [[../snn/snn-energy-breakeven-conditions]] derives its headline result — SNNs beat a capacity-matched quantized ANN only below ~5.7% spike rate — using a "Typical Neuromorphic" hardware setting whose sparse-event movement cost (3.0 pJ/bit/hop) is **normalized from Loihi 1's reported per-event routing energy**. That parameter models the cost of routing a *one-bit event*. Loihi 2's actual signal is a multi-bit graded value, and the NoC was redesigned down to standard-cell pipelines for roughly 10× faster spike processing.

So the mechanism the parameter represents no longer matches the hardware it is named after. That does not tell us the threshold moves in a particular direction — a graded spike carries more information per event, so fewer events may be needed — but it does mean **any Loihi-1-derived routing cost applied to Loihi 2 needs re-derivation, not extrapolation.** Flagged on the breakeven page.

## Toolchain — archived

**Lava**, Intel's open-source Python SDK for Loihi 2, was **archived on 2026-05-13**. Intel's own notice:

> "Intel will not provide or guarantee development of or support for this project… All Lava repositories are archived. Stay tuned for announcements about our new SDK and next generation Loihi processor."

Read carefully, that is a platform transition and **not an exit** — a next-generation Loihi is explicitly promised. But as of 2026-08-21 the reference toolchain for the field's most-used research platform is read-only with no shipped replacement. Every captured source describing Loihi 2's software ecosystem predates the archival and describes the Lava-era situation. [[../benchmarks/neurobench]]'s stated plan to extend its harness to Lava is now aimed at an archived target.

## Hala Point — the large-scale system

Announced **~April 2024** (inferred: footnote testing dates, an ICASSP April 2024 citation, and "this year's Mobile World Congress"). Deployed at **Sandia National Laboratories**. Explicitly "a research prototype that will advance the capabilities of future commercial systems" — no price, no SKU, no general availability.

| Metric | Value |
|---|---|
| Loihi 2 chips | **1,152** |
| Neuromorphic cores | 140,544 |
| Neurons / synapses | up to 1.15 billion / 128 billion |
| Max power | **2,600 W** (whole 6U chassis; unclear whether Loihi-cores-only or inclusive of the 2,300+ ancillary x86 processors) |
| Peak throughput | up to **20 petaops** |
| Sustained | >380 trillion 8-bit synaptic ops/s; >240 trillion neuron ops/s |
| Bandwidth | 16 PB/s memory; 3.5 PB/s inter-core; 5 TB/s inter-chip |
| Headline efficiency | **>15 TOPS/W** (8-bit ops/s/W) |

### The 15 TOPS/W figure does not survive scrutiny

Two problems, both recorded here because this figure will be quoted at you.

**It contradicts Intel's own arithmetic.** 20 petaops at 2,600 W is **≈7.7 TOPS/W** — roughly *half* the headline. The two numbers come from different, unreconciled characterisations (general peak-ops capacity versus a specific benchmark), and neither states whether power was measured at the same operating point. The release does not explain the gap.

**The benchmark behind it is synthetic and favourable.** Per the footnote: a **14,784-layer MLP** at 2,048 neurons/layer, 8-bit weights, **stimulated with random noise** rather than any real workload, **pruned to 10:1 sparsity**, using sigma-delta neurons at **10% activation rate**. Every one of those choices pushes toward the low-activity regime where event-driven hardware looks best. It is not a named model, not a real task, and not a [[../benchmarks/neurobench]]-style measurement.

A separate footnoted claim — "100 times less energy… as much as 50 times faster than conventional CPU and GPU architectures" — cites two external small-scale edge-workload papers, **not any Hala Point measurement**. Recorded as Position A evidence in [[../conflicts/snn-energy-payoff]].

## LLM inference on Loihi 2 — measured, and genuinely interesting

The most substantive real-silicon result Intel's platform has produced, and it needs its caveats attached or it will be misread.

**What was run:** the **MatMul-free LLM** (Zhu et al. 2024), 370M parameters, on **24 of 32 chips** of an "Alia Point" system. Ternary weights, 24-bit fixed-point activations, W8A16 quantization. Trained entirely **off-chip**; the contribution is post-hoc quantization plus hand-written microcode mapping.

**This is not a spiking transformer.** There is no self-attention anywhere — token mixing is an MLGRU linear recurrence (`hₜ = fₜ⊙hₜ₋₁ + (1−fₜ)⊙cₜ`), architecturally an SSM/RNN cousin. No surrogate gradients, no STDP, no spike-rate coding of activations. Loihi 2 is used here as a generic low-precision, locally-stateful, asynchronous fabric — exploiting per-core local memory for recurrent state and event-driven messaging for ternary zero-skipping.

**Measured, system power both sides, batch 1, inference only:**

| | Loihi 2 (24 chips) | Jetson Orin Nano 8GB (FP16) |
|---|---|---|
| Generation throughput | **41.5 tok/s** | 12.6–15.4 tok/s |
| Generation energy | **405 mJ/token** | 719–1,200 mJ/token |
| Prefill throughput | 6,632 tok/s | 627–3,861 tok/s |
| Prefill energy | 3.7 mJ/token | 4.4–17.9 mJ/token |
| Time-to-first-token (500 tok) | **99 ms** | 659 ms |

Loihi's throughput and efficiency are **constant across sequence length** (500–16,000 tokens) because compute is per-token recurrent with state resident in local memory. That flat scaling, not the absolute numbers, is the architecturally interesting result.

Against an **H100** running the same model: 3× throughput and ≥14× less energy per token on generation. But the H100 **beats Loihi on prefill throughput** (11.4k–84.6k tok/s), and at 16k-token sequences the H100 reaches 0.9 mJ/token — clearly better than Loihi's flat 3.7.

### Three caveats that must travel with those numbers

1. **Not iso-accuracy.** The MatMul-free model scores **39.6** zero-shot average; Qwen2.5-500M scores **51.1** — **29% better** with only 35% more parameters. The efficiency win is partly a quality sacrifice. (Quantization itself is nearly free: W8A16 costs 0.4% versus the FP16 baseline.)
2. **The multi-chip penalty is severe, and honestly disclosed.** Single-chip *estimate*: 71.3 tok/s at **59 mJ/token**. 24-chip *measured*: 41.5 tok/s at **405 mJ/token** — **6.9× worse energy per token**, because during generation only one chip is dynamically active per step while all 24 draw static power. Prefill degrades far less (1.32×) since it pipelines across chips.
3. **The full model was not run.** Embedding and un-embedding (lm_head) layers were never implemented on-chip. Un-embedding alone needs **7 more chips** (31 of 32 for the full 370M model). Every figure above covers only the 24 recurrent blocks.

*(synthesis)* Caveat 2 is the one that generalises. It is the **same data-movement conclusion this wiki has now reached at four independent scales** — ADC/DAC conversion in analog arrays, per-timestep memory traffic in digital SNN accelerators, NoC routing energy in the analytical model, and now chip-to-chip static power and communication in a real multi-chip system. Every time neuromorphic efficiency is measured rather than modelled, the loss shows up in moving data, never in the arithmetic.

## Measured system power — and the static-power problem

**Corrected 2026-08-21.** An earlier version of this page said no measured power figure existed in any captured source. That is no longer true: the 2026-08-20 weekly sweep ingested a primary source with directly measured power on a **16-chip Loihi 2 VPX** system — see [[../chips/loihi2-persistent-monitoring]]. Keysight N6705C power analyzer, on-board probes, 1M measured inferences.

| Configuration | Latency | Total power | Total energy | **Dynamic** energy |
|---|---|---|---|---|
| Loihi 2 VPX, Ethernet I/O | 281.0 µs | 16.20 W | 4.554 mJ | 0.0426 mJ |
| Loihi 2 VPX, preloaded input | 48.3 µs | 16.89 W | 0.816 mJ | 0.0406 mJ |
| Xeon E5-2660 v3 (2014) | 420.3 µs | 77.96 W | 32.769 mJ | 20.156 mJ |
| Tesla V100S (2019) | 163.5 µs | 58.35 W | 9.540 mJ | 5.350 mJ |

The advantage depends **entirely on the boundary**: dynamic-energy-only gives ~474–496× versus CPU, while total energy on the same table gives **7.2–40.2×**. Roughly an order of magnitude, from the same measurement.

**Static VPX power is 16.05 W of the ~16.2 W total** — a nearly-idle infrastructure running a model occupying **74 of ~2,048 available cores**.

*(synthesis)* That independently confirms, from a completely different workload and research group, the mechanism behind the LLM paper's 6.9× multi-chip penalty above: on Loihi 2 at system scale, **static power from underutilised chips swamps the dynamic energy advantage.** Two unrelated sources, one running an autoencoder on a 16-chip VPX box and one running an LLM on 24 chips, arrive at the same conclusion — the per-operation efficiency is real, and the system around it eats the win.

This is now the most important practical fact on this page. Loihi 2's efficiency case depends on **filling the machine**. A sparsely-mapped model on a large system loses, no matter how cheap its spikes are.

**Still missing:** a per-chip figure. Both sources report *system* power for multi-chip boards; neither decomposes to watts, pJ/spike, or pJ/synaptic-op for a single Loihi 2 die. Single-chip numbers in both papers are unvalidated projections.

Three comparative claims on the community reference page — "up to 10× faster spike processing" than Loihi 1, "47×" more efficient spectrogram encoding via resonate-and-fire neurons, ">90×" computation reduction for event-camera optical flow — all lack stated baselines, workloads and measurement boundaries. They read as inherited from cited papers rather than independently reproduced.

## Open questions

- What is Intel's replacement SDK, and when? What is "next generation Loihi"?
- Any chip-level power figure at a stated boundary?
- Does the graded-spike change move the [[../snn/snn-energy-breakeven-conditions]] threshold, and in which direction?
- A [[../benchmarks/neurobench]] system-track submission — Loihi 2 already appears there as a QUBO baseline, so the plumbing exists.
- What does Loihi 2 look like on a **fully utilised** system? Every measured result so far runs a model occupying a small fraction of available cores, which is the worst case for the static-power problem.

## Source

- `raw/research/neuromorphic-seed-sweep/04-on-loihi2.md` — Open Neuromorphic community reference page. Secondary; undated, and describes the now-archived Lava toolchain.
- `raw/research/neuromorphic-seed-sweep/03-intel-hala-point.md` — Intel Newsroom, Hala Point announcement, ~April 2024. Vendor primary; tier 3.
- `raw/research/neuromorphic-seed-sweep/11-loihi2-llm.md` — "Neuromorphic Principles for Efficient Large Language Models on Intel Loihi 2", arXiv:2503.18002. Measured on N3C1 silicon. ⚠️ Captured with pymupdf (marker failed under machine load) — figures unavailable; all figures above are from body text and Tables 1–3.

## Related

- [[roster]] · [[ibm-northpole]] — the digital-neuromorphic counterpart, which went further and dropped spiking entirely
- [[../snn/snn-energy-breakeven-conditions]] — the graded-spike caveat and the attention-free refinement
- [[../conflicts/snn-energy-payoff]] — the Hala Point claims as Position A
- [[../chips/loihi2-persistent-monitoring]] — measured power on a 16-chip VPX system; the static-power finding
- [[../benchmarks/neurobench]] — where Loihi 2 already appears as a system-track baseline
- [[../viability-ledger]]
