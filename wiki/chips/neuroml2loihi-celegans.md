# NeuroML2Loihi — NeuroML to Loihi 2 compiler, C. elegans case study

Rosen, Gaurav and Yi (Virginia Tech) release NeuroML2Loihi (N2L), a Python layer that parses NeuroML/LEMS model files and emits a Lava LIF + Dense process network that runs on Loihi 2 hardware or the CPU-only Lava simulator. Case study: 302-neuron c302 C. elegans networks, run on one real Loihi 2 chip and compared with NEURON/CoreNEURON on a Jetson AGX Orin. Claimed: 514-1211x lower latency and 1.8-1.9x lower mean power. The evidenced picture is narrower: the energy comparison is chip-total vs host idle-subtracted, voltage fidelity is weak, and every model needs hand-tuned scale and decay parameters. It builds on Lava, which the wiki records as archived ([[../players/intel-loihi2]]).

## Toolchain (what the compiler actually does)

- **Front end:** `.nml` (neurons, synapses, stimuli) is parsed to a NetworkX graph; the `.xml` LEMS file gives duration, timestep and recorded neurons. Both are stated by the paper.
- **Mapping layer:** a tag-to-Lava-process dictionary (`register_mapping()`); e.g. `iafCell` to LIF, `expTwoSynapse` to Dense. Only LIF and Dense are used in the evaluated runs, so this is not a general NeuroML compiler: other cell/synapse types need user-written Lava processes (stated as extensibility, not demonstrated).
- **Back end:** all neurons vectorised into one LIF process, recurrently wired to one Dense process via the adjacency matrix. Hardware recording uses Dense to Receiver plus StateProbe processes for spikes, and a StateProbe on `v` for voltage. Outputs reuse c302's `.dat` format for direct comparison.
- **Backends:** Loihi 2 hardware or Lava CPU simulator, switchable; no hardware needed to use the tool.
- **Manual step (limit):** NeuroML mV-scale models become integer fixed-point. Input scale (4), recurrent scale (320 = 10 x 2^5), decay d_u = 49, d_v = 8 and the maximum threshold 131,071 were set by grid search. The paper says a comparison run is needed whenever a new model is deployed; automatic derivation is future work. Connection weights are anatomical synapse counts, not measured strengths.

## Setup

Kapoho Point single-chip board (128 neurocores, 6 Lakemont x86 cores). Models: Minimal (2 PLM neurons, no connections), Active (18 neurons, 125 synapses), Full (302 neurons, 3119 synapses; muscles excluded). 300 ms biological time at 0.02 ms steps = 15,000 timesteps, constant PLM stimulation, 25 seeds. Claimed first full 302-neuron C. elegans model on a single neuromorphic chip (unverified by the wiki).

## Measured numbers (real Loihi 2 hardware; mean +/- as reported, 25 seeds)

| Model | Loihi latency | NEURON latency | Speedup | Loihi energy | NEURON energy | Loihi power | NEURON power |
|---|---|---|---|---|---|---|---|
| Minimal | 0.0243 s | 12.47 s | 514x | 0.0122 J | 11.65 J | 0.505 W | 0.939 W |
| Active | 0.0242 s | 18.62 s | 768x | 0.0123 J | 18.11 J | 0.505 W | 0.978 W |
| Full | 0.0258 s | 31.19 s | 1211x | 0.0131 J | 28.52 J | 0.507 W | 0.919 W |

Memory (Loihi SRAM mapped): Minimal 0.0017 MB / 3 cores; Active 0.0054 MB / 3 cores; Full 0.657 MB / 9 cores (38.9 % mean occupancy of mapped cores' 192 KB each). Neurons grow 16.8x Active to Full, memory 121x: synapse storage dominates.

## Measurement boundary

- **Loihi latency:** on-chip execution window from the power profiler; setup, compilation and host I/O are not counted (the paper calls it a proxy for pure inference latency). Flat across scale (<6 %).
- **NEURON latency:** simulation-loop time only; model generation and compilation excluded. Setup cost on both sides is outside the headline.
- **Loihi energy:** trapezoidal integral of total board power including static draw, over the execution window. Not clear from the paper whether this is the whole board or chip rails only (boundary partly unstated).
- **NEURON energy:** Jetson CPU + GPU rails (INA3221, 49-50 Hz) with a 30 s idle baseline subtracted, i.e. dynamic only, at 15 W mode. The authors argue this favours the Jetson, so the gap is a lower bound; Total (non-subtracted) tables are in supplementary S8-S10, not seen here.
- **Energy is mostly latency:** power ratio is only 1.8-1.9x; the energy ratio (Loihi at 0.046-0.105 % of NEURON) comes from short run time. The authors say this themselves.
- **Baseline choice (synthesis):** NEURON with a fixed-step GPU backend on a 15 W edge SoC for 302 neurons is a weak, unoptimised baseline; no CPU cluster, event-driven simulator or other neuromorphic backend (SpiNNaker, BrainScaleS-2) was run.
- **Fidelity cost (synthesis):** Loihi time is for the tuned-integer LIF approximation, not equivalent dynamics; speed is bought with the mismatch below.

## Fidelity (evidenced, deterministic: SD 0 across seeds)

Spiking only occurs in PLM neurons. Against NEURON: Victor-Purpura ratio to a rate-matched Poisson baseline 0.286 (cost 1 s^-1) and 0.456 (50 s^-1); van Rossum ratio 0.725; 1.0 spike/neuron count difference. Voltage (affine-mapped to mV, Pearson): Minimal -0.144, Active and Full 0.433 (13 of 18 active neurons compared). Spike timing is moderately faithful; subthreshold voltage is weak. The authors attribute it to the LIF/Dense vs IAF/ExpTwoSynapse primitive mismatch, not hardware.

## Maturity and limits

Real silicon, measured, research board; one chip, 300 ms runs, one stimulus pattern, tiny network (max 302 neurons of 1,048,576 supported). Scaling beyond one chip and denser connectivity untested. Authors' own scaling warning: synaptic density, not neuron count, drives mapped memory. Code is open source (github.com/DRosen766/NeuroML2Loihi; Zenodo DOI 10.5281/zenodo.21431945). Depends on Lava and INRC-gated hardware, so toolchain longevity is a risk (synthesis; see [[../players/intel-loihi2]]).

## Source

- `raw/research/weekly-2026-10-22/04-neuroml2loihi.md` — arXiv 2610.25424, "Small-scale neural simulation of Caenorhabditis elegans on Loihi-2 using NeuroML2Loihi". Funding not examined.

## Related

- [[../weekly-briefs/2026-10-22]] — brought in by the 2026-10-22 weekly sweep
- [[../players/intel-loihi2]] — Loihi 2 entry; Lava SDK archived 2026-05-13
- [[loihi2-onchip-q-learning]] — another Lava-on-Loihi-2 research result, also dynamic-vs-total boundary issues
- [[loihi2-persistent-monitoring]] — Loihi 2 with measured board power and a boundary-dependent headline
- [[../benchmarks/neurobench]] — standardised comparison that this paper's ad hoc baseline lacks
- [[../viability-ledger]] — Loihi 2 stays a research platform
