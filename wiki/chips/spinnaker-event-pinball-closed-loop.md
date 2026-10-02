# SpiNNaker event-camera pinball: closed-loop TDE spiking motion detector

A lab demonstrator, not a chip: a hand-wired, learning-free spiking network (~24.6k neurons, Temporal Difference Encoder motion detectors) on a SpiNNaker SpiNN-5 board (Univ. Lille / CTU Prague) that tracks a ball from a Prophesee EVK4 event camera and plays simulated pinball in closed loop. Claimed headline: 56.1% hit rate vs 25.6% human mean, 21.7 ms reaction time, ~148 µW "dynamic power". The 148 µW is an **estimate from an assumed 8 nJ/synaptic event, not a measurement**, and excludes idle/baseline board power; the hit rate is per flipper activation, so "beats humans" mostly means "more selective than humans".

## What it is

Fully spiking, no trained parameters. Pipeline: adaptive event-count accumulation (AECP; 500 events or 16.7 ms max, positive events only) → 3×3 Gaussian conv, stride 2 (128→64) → receptive-field segmentation (22×22 map) → 8 direction-selective populations built from Temporal Difference Encoders (facilitation delay 2 ms, trigger delay 1 ms) with winner-take-all → 36-neuron Gaussian-weighted angle readout. Speed comes from the winning population's mean firing rate via host-side regression; position from the filter map. The strike policy (constant-velocity extrapolation, fire flipper if predicted position enters the strike region) runs on the **host CPU**, with events streamed over Ethernet. Perception is on SpiNNaker; decision is not on-chip.

Platform: 48-chip SpiNN-5 board generation (PyNN/sPyNNaker toolchain), not SpiNNaker2, though the paper's naming ("SpiNNaker-5") is ambiguous; no process node stated. Camera: EVK4-HD (1280×720), 128×128 px ROI. No memristive or novel device. The task is a custom Pygame simulator on a 60 Hz monitor observed by the real DVS, in two flipper regimes (binary gate: flipper exists only on the triggered frame; solid flipper: persistent collider).

## Measured numbers (system-level unless noted)

- Network: 24,620 neurons (input 16,384; filter-map 4,096; segment-map 484; DS 3,612; DS WTA 8; angle WTA 36).
- Latency: ~5 ms internal network latency (**derived from configured synaptic delays**, 1+1+2+1 ms, not independently timed) + 16.7 ms accumulation window = ~21.7 ms reaction time; control rate ≥ 60 Hz. Camera, Ethernet and host-CPU policy latency are **not** in this sum.
- Power: ~148 µW = 2,472 nJ per 16.7 ms window = 309 spikes × **assumed** 8 nJ/synaptic event (cites prior SpiNNaker power models). **Not measured on the board.** Excludes idle board power, system-services baseline, and per-neuron simulation cost from the paper's own power model. Spike counts come from the minimal simulator with the ball always in view (called an upper bound); spikes are counted as synaptic events, with fan-out not accounted.
- Direction accuracy (minimal simulator, 0–1000 px/s, 8 directions): 31.8–88.6% depending on receptive-field size and accumulation window. **Deployed config (3×3, 16.7 ms): 68.5%**; 5×5 at 16.7 ms: 82.7%; best 88.6% (5×5, 100 ms) is not real-time.
- Speed estimate at deployed config: r = 0.873, R² = 0.761, MAE = 0.374 (normalised units, not px/s). Weak-to-moderate fit.
- Angle readout: evaluated qualitatively only; no numeric angular error.
- Closed loop, binary-gate regime (10 runs × 100 balls, vs 10 humans × 100 balls): agent 64 hits / 114 actions = **56.1% hit rate**; humans 58.3 hits / 282.1 actions = 25.6% (range 9–61%).
- Solid-flipper regime (20 humans × 30 balls; agent swept over 9 strike-region sizes): human hit rate ~0.6 (precise group) to ~0.2–0.35 (aggressive); agent "spans" that range. Read off a figure only, no table.
- Physical demonstrator: qualitative video only, no numbers.

## Baseline and comparison honesty

- **Hit rate is hits / activations, not hits / balls.** An agent that fires rarely scores high. Raw hits are roughly human-level (64 vs 58.3 per 100 balls); the best human hit rate (61%) and top hit counts (127, 112) exceed the agent. The authors concede action economy "does not isolate perception from task difficulty".
- **Human baseline is small and unstable**: 10 (binary) and 20 (solid) keyboard players, variable engagement; the authors call the mean unstable. The binary-gate regime is acknowledged to penalise humans. The abstract says "nearly double" while the body says "more than double" for 2.19×, and the headline picks the most favourable regime.
- **Power comparison is not like-for-like.** The paper's comparison table sets assumed, dynamic-only 148 µW against others' reported total or measured platform power (SpiNN-3 goalkeeper 2 mW; Akida ~4.5 mW; Pico 700 mW). The "lowest dynamic power among spiking and neuromorphic systems" claim therefore compares unlike boundaries. No SpiNNaker idle/board power is given (a SpiNN-5 board is order watts, stated as a note in the source summary, not a paper figure).
- **Latency comparison mixes boundaries**: single forward pass (Akida 2.2 ms, Loihi 2 1458 ms; third-party figures from a table-tennis study, not verified here) vs closed-loop reaction time (21.7 ms). The authors acknowledge direct comparison is "inherently difficult".
- **No frame-based, GPU or CPU baseline** of the same task, despite motivating the work against frame cameras.
- **Scene is not native events**: a 60 Hz rendered monitor imposes a sampling ceiling at high speeds; the physical rig is qualitative.
- The strike-policy sweep shows one threshold parameter tunes style, not that perception is good.

Same unstated-measurement-boundary pattern catalogued in [[../snn/snn-energy-hardware-realistic]] and [[../conflicts/snn-energy-payoff]]: here the omitted costs are board idle/baseline power and per-neuron simulation cost, and the per-event energy is assumed.

## Maturity

Lab demonstrator: board-level system with a real DVS, simulation-in-the-loop game, physical rig as proof-of-concept video only. Not a chip, not a product. Perception on SpiNNaker, decision on host PC, events over Ethernet.

## Blockers stated

- 60 Hz display limits temporal sampling at high ball speed; single-scale receptive field trades slow vs fast motion sensitivity (multi-scale suggested).
- Real-time constraint forces a 16.7 ms window, giving 68.5% direction accuracy vs the 88.6% non-real-time ceiling.
- Quantitative physical-hardware evaluation, a learned policy, a more compact network and iCub integration are all future work.
- Power is an estimate, not measured.

## Commercial signal

None. Academic (Lille CRIStAL, CTU Prague), funded by French ANR PEPR IA (France 2030), IRCICA, and Czech GACR programmes. The authors themselves note SpiNNaker is not the lowest-power neuromorphic platform available (claimed, by authors).

## Novelty

Recombination: TDE/sEMD motion detectors (Milde, D'Angelo, Gutierrez-Galan prior art) applied to a small fast target, adding a 36-neuron angle readout and AECP packaging. Claims the first TDE-SNN to jointly estimate fine angle and velocity and close the loop on pinball. Closest prior work: air hockey on SpiNN-5 (10.09 ms), goalkeeper on SpiNN-3 (6.5 ms, 2 mW), table tennis on Akida.

## Reproducibility

Good: network and simulator code on Lille GitLab (bioinsp/NeuromorphicPinball) and GitHub (PinBallSimulator), data on university Nextcloud, demo video public. SpiNN-5 board and Prophesee EVK4 are accessible. Human-study data in the paper's Table 4.

## Source

- `raw/research/weekly-2026-10-01/04-spinnaker-event-pinball.md` — "Can Spiking Neural Networks play pinball? A neuromorphic motion detector for target tracking" (Fatahi, Pryjmakova, Boulet, D'Angelo; arXiv:2609.24403). Academic primary, captured via arXiv.

## Related

- [[../devices/event-cameras]] — Prophesee EVK4 front end; keeps processing spiking end to end (contrast with the "densify events into frames" pipelines), though events are accumulated into packages first
- [[../chips/ethereal-event-gnn-processor]] — parallel event-driven DVS processing approach (GNN ASIC vs hand-wired SNN on a many-core board)
- [[../conflicts/snn-energy-payoff]] — the 148 µW figure is an assumed-per-event, dynamic-only estimate with baseline costs excluded
- [[../snn/snn-energy-hardware-realistic]] — same failure mode (omitted overhead)
- [[../snn/snn-training-surrogate-gradients]] — contrast: zero training, hand-designed delays and weights
- [[../benchmarks/neurobench]] — the 148 µW boundary fails a measured idle/active/dynamic system-track reporting standard
- [[../players/brainchip]] — Akida 2.2 ms / ~4.5 mW table-tennis comparator (third-party figure)
- [[../players/intel-loihi2]] — Loihi 2 1458 ms / ~100 mW forward-pass comparator (third-party figure)
- [[../players/roster]] — SpiNNaker has no roster or player page yet
- [[../viability-ledger]] — edge event-vision closed-loop control: demonstrator maturity only
