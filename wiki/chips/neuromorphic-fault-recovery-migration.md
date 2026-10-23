# SpikeRelay: recovering permanent compute faults in neuromorphic many-core chips by migrating computation, not data

A Zhejiang University / SUSTech architecture paper proposing SpikeRelay, an online recovery scheme for diagnosed, permanent faults in a neuromorphic core's neuron-update datapath. Instead of retiring the faulty core and copying its weights and membrane state elsewhere, the faulty core stays on as a storage-and-router node and a healthy "rescue" core runs the LIF update remotely. Claimed headline: 100% recovery at 92.2% SRAM utilization and 50% fault rate vs 22.1% for the best baseline. **All results are from a cycle-level simulator modelled after Loihi (32x32 cores); nothing is run on silicon**, and no Loihi 2, SpiNNaker 2 or other real-hardware validation exists yet (authors list it as future work).

## What it is

Fault class (scoped narrowly): in-field, *diagnosed*, *permanent* compute-unit (ALU) faults from device aging, where the core's SRAM and NoC router remain intact. Faults that also hit storage or routing fall back to whole-core retirement. Transient faults are out of scope.

Mechanism (design, as described by authors):
- Recovery is control-plane only: pick a rescue core (need not be idle), switch the faulty core to storage-and-forwarding mode, install NoC forwarding rules. No weights or states move; recovery cost is constant-size metadata.
- In steady state the rescue core receives the forwarded spikes, reads neuron state and weights remotely from the faulty core's SRAM at addresses from a fixed metadata layout, runs the LIF update, writes state back, and emits spikes under the original logical neuron ID.
- Remote-access cost is mitigated by batch prefetching, double buffering and write coalescing. Rescue core holds only a small per-neuron weighted-input accumulator (4 B/neuron).
- Authors argue step-equivalence to fault-free execution under synchronous timesteps and the diagnosed-fault assumption (a design argument, plus accuracy tracking in simulation; not a hardware check).

## Evidence: simulation only

Setup (simulation): Loihi-modelled 32x32 array, 1,024 cores, 768 KB SRAM per core (a simulator parameter, not a claim about any shipped chip), cycle-level NoC model, 512 inference timesteps, faults injected uniformly at random among deployed cores at 0-50% rates, 5 seeds per configuration. Workloads: Spiking VGG-11 / CIFAR-100 (~58k neurons, 73.3% SRAM utilization); CIFAR10-Conv5 (~77k neurons, 85.8%); SpikeBERT / SST-2 (~84k neurons, 92.2%); synthetic dense stress cases at 95% and ~99.1%.

Numbers (all simulator, authors' own baselines):
- Recovery success: 100% on the three real workloads across 0-50% fault rate. Best baseline 22.1% at 92.2% utilization / 50% faults (baseline identity not given in the text read).
- Dense-Stress (~99.1% utilization): migration baselines (RescueSNN, HyCA-adapted) collapse near 5% fault rate; SpikeRelay holds 100% to 40%, then ~90% at 45% and ~74% at 50%, limited by free SRAM (~7.4 KB/core free vs ~10 KB buffer needed for a faulty core's 2,497 neurons).
- Recovery latency: 3-97 cycles (real workloads) and 3-58 cycles (Dense-Stress) vs 10^4-10^5 cycles (RescueSNN, CompleteMigration) and ~10^6 cycles (HyCA-adapted). Cycles, not seconds; no clock frequency stated.
- Data migrated: zero for SpikeRelay; RescueSNN exceeds 150 MB on SpikeBERT at ~25% fault rate.
- Accuracy (CIFAR10-Conv5): near-constant for SpikeRelay across 0-50% faults; migration baselines degrade sharply beyond 20-25% fault rate. Exact accuracy values only in a figure, not read as a table here.
- Runtime cost: "bottleneck-core overhead remains about 27% at a 50% fault rate" after optimization, assuming contention-free NoC transport; the authors call this a lower bound. A "within the timestep budget" claim is made but the budget is not quantified in the text read.
- Motivating numbers: 0.1% per-core fault rate across a 4,096-core TrueNorth-class system gives 98% chance of at least one fault (arithmetic on an independence assumption, not a measured field rate). Paper reports CIFAR-10 accuracy falling by more than half at a 30% fault rate in its multi-core experiments (simulation, conditions unstated beyond that).

## Caveats and honesty notes

- **Fault rates of 5-50% are stress-test values, not field-realistic.** The 98% motivating figure assumes a 0.1% per-core rate that is itself an assumption; no aging-failure data from a real chip is cited as measurement here.
- **Baselines are authors' re-implementations** inside one simulator (HyCA "adapted" with spare cores at 6.25% of total; LEA as replica scheme). The "22.1%" and "collapse" comparisons depend on those adaptations; RescueSNN-type methods are fault-aware remapping, not designed for this simulator.
- **Fault model is favourable**: it presumes clean diagnosis and an intact SRAM/router. Real aging often co-degrades SRAM and interconnect; the paper's answer is fallback to retirement.
- **Internal inconsistency**: buffer is said to be "about 500x smaller per neuron than full migration" in Section 5, and "10,000x buffer reduction" in the Discussion. Boundaries for the two ratios are not reconciled (boundary unstated).
- **Synchronous-timestep assumption**: asynchronous event-driven cores (the paper names Loihi 2) would need event-ordered queues, which the authors expect to give back part of the buffer saving. Loihi-*modelled* therefore does not mean Loihi 2 compatible.
- Remote reads add steady-state NoC traffic and latency; on real silicon this contention is unmeasured.
- Fixed SRAM metadata layout and a forwarding rule at the faulty router are required hardware/firmware support; whether shipping chips (Loihi 2, SpiNNaker 2) expose these is not shown.

## Maturity

Architecture proposal with simulator evaluation. No RTL, no silicon, no vendor involvement stated. Relevance is as a *leading indicator* for the "long-lifetime deployment / reliability" blocker, not as a deployable feature.

## Commercial signal

None. Academic (Zhejiang University, SUSTech). Funding and code availability not established from the portions read (unstated).

## (synthesis)

- Reliability is a gap in this wiki: device pages cover endurance and variability of analog synapses ([[../devices/memristor-array-integration-gap]], [[../devices/hzo-ferroelectric-capacitor-reliability]]), but digital many-core chips such as Loihi 2 and SpiNNaker are usually discussed only on energy and latency. This paper argues the operating-lifetime fault model for *digital* near-memory cores is largely unexplored; (synthesis) that is a reason to treat "years-long unattended edge deployment" in [[../viability-ledger]] as lacking evidence on the digital side too, not only the analog side.
- (synthesis) The idea (separate compute from co-located storage so one survives the other) is architecture-level and plausibly transfers to in-memory-compute parts, as the authors suggest; no evidence is given for that transfer.
- (synthesis) Time-to-impact depends on whether a vendor ships hardware hooks. None has been shown.

## Source

- `raw/research/weekly-2026-10-22/02-neuromorphic-fault-migration.md` -- "Migrate Computation, Not Data: Fault Recovery in Neuromorphic Many-Core Systems" (Cao, Jiang, Yu, Du, Pan, Zhu, Deng; arXiv:2610.26985). Academic primary, captured via arXiv PDF. Read: abstract, introduction, Sections 2-8; reference list and figure data not read.

## Related

- [[../weekly-briefs/2026-10-22]] — brought in by the 2026-10-22 weekly sweep
- [[../players/intel-loihi2]] — the simulator is "Loihi-class"; no Loihi 2 hardware validation
- [[../chips/loihi2-persistent-monitoring]] — deployed Loihi 2 system, the sort of long-running use that fault recovery would matter for
- [[../chips/spinnaker-event-pinball-closed-loop]] — SpiNNaker board (SpiNN-5) many-core platform; the paper names SpiNNaker 2 as a similar execution model
- [[../chips/brainscales2-chiplet-interconnect]] — multi-chip scale-out, where core/chip fault counts compound
- [[../players/ibm-northpole]] — TrueNorth-lineage 4,096-core scale used in the paper's fault-probability argument
- [[../devices/memristor-array-integration-gap]] — analog-side reliability counterpart
- [[../benchmarks/neurobench]] — no fault-tolerance track; recovery claims are outside its reporting standard
- [[../viability-ledger]] — reliability evidence for long-lifetime edge deployment
