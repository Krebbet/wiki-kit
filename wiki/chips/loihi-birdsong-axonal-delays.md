# Loihi 1 — birdsong syllable recognition with axonal-delay template matching

Penn State / McGill (Tavares, Sargent, Sakata, Jin) recognize Bengalese finch syllables in continuous audio using SVM "feature neurons" plus axonal-delay template matching, and run the template-matching, collision and recognition stages on **Intel Loihi 1** (not Loihi 2). The front end (feature and binary neurons) runs on a CPU, so the system is hybrid. Headline claims: constant ~17 ms per syllable independent of template count, and 8.71 J / 0.75 W for the Loihi network. Neither has a conventional baseline or a full-system boundary; no numeric Loihi WER is given. Research prototype, 8 birds on-chip.

## Chip / setup

- **Loihi 1**, not Loihi 2. The source's energy probe is explicitly Loihi 1's; Loihi 2 appears only as context and as future work (resonate-and-fire spectral analysis). Process node, board and chip count are not stated.
- Features used: LIF neurons, two-compartment (dendrite + soma) "plateau" neurons, 6-bit synaptic delays (max 62 timesteps), integer decay (0-4096) and weights (dendritic 1-255). These are Loihi 1 specifics. Timestep = one spectrogram frame (3.3 ms, 300 Hz).
- Pipeline (evidenced): 32-band gammatone spectrogram (1-10 kHz) -> ~37 ms windows (11 frames, 352-dim) -> Gaussian-kernel SVM feature neurons (trained off-chip) -> onset/offset spikes -> delay-line template matching on-chip; AdaBoost-selected linear "binary neurons" (CPU-computed spikes) resolve similar-syllable collisions.
- Few-shot memorization of spike patterns: N = 5, 10, 20, 40 exemplars per type. No gradient-based SNN training.
- Task: continuous labeling and segmentation, 4-19 syllable types per bird, calls and noise present.

## Measured numbers

- **Accuracy, CPU software:** WER below 5% with 10-40 exemplars per type (converged by ~20). Mean over 10 independently trained systems; 8 own birds plus 11 from a public dataset (Koumura and Okanoya). Per-bird values in figures only. WER ignores boundary errors.
- **Accuracy, Loihi:** "comparable" to CPU, "slightly higher" WER (Fig. 5e). **No numeric Loihi WER in the text.** Run on the 8-bird own dataset only.
- **Throughput, on-chip:** ~17 ms per annotated syllable, flat from 5 to 40 exemplars per type. This is **throughput** (total test-set execution time / syllable count), **not response latency**, and it **excludes CPU-side generation of feature-neuron and binary-neuron spikes**. The network's intrinsic delay is the largest onset template delay + 2 timesteps (independent of template count); end-to-end real-time latency of the full hybrid system is not reported.
- **Speedup vs CPU:** "two to three orders of magnitude" at 40 exemplars per type. CPU hardware and absolute times are not stated.
- **Energy (Loihi 1 energy probe):** 40 templates per type, 80 s of audio processed in 11.63 s (~7x faster than real time), **8.71 J**, stated dynamic power **0.75 W**. Boundary: Loihi network only, excluding the CPU front end. Single configuration, single measurement. Whether static power is in the 8.71 J is not stated. **No CPU/GPU energy baseline**, so no efficiency ratio can be derived.
- Design parameters (not results): template neuron fires at >=60% aligned spikes; plateau UP-state ~217 ms (65 timesteps); recognition refractory ~67 ms (20 timesteps); delays compressed by 62/Dmax when over the 6-bit limit.

## Baseline and comparison honesty

- The only comparator is the authors' own CPU implementation of the same template-matching algorithm, whose search time grows superlinearly with template count (CPU model and threading undescribed). The speedup is against a naive serial search, not a competitive conventional recognizer. No comparison to other birdsong annotators or neuromorphic audio systems.
- The 17 ms and 0.75 W / 8.71 J figures both leave out the front end, which is the expensive part. This is the same exclude-the-front-end boundary problem tracked in [[../conflicts/snn-energy-payoff]]; the figures support neither side of that debate.
- Delay time compression (62/Dmax) coarsens timing for long templates; the WER effect is not quantified.
- Constant throughput up to 40 templates per type is an assumption beyond that; the authors state scaling "requires hardware can be scaled".
- Funding includes an Intel gift for neuromorphic research (claimed in acknowledgments; authors state no role in design or publication).

## Maturity

Algorithm demonstrated in software on 19 birds; on-chip stages on Loihi 1 research hardware on 8 birds; front end CPU-only. Research prototype, below integrated-chip level, no product path stated.

## Commercial signal

None evidenced: no players, customers, design wins or dates. Intel is a funder (claimed) and Loihi the platform (research access). Large-vocabulary speech recognition is the authors' conjecture only; no speech results.

## Blockers stated

- Not fully neuromorphic: feature and binary neurons run on CPU.
- Transfer to continuous speech is "an open question"; syllables are stereotyped and few; no syntactic information.
- 6-bit delay field (62 timesteps) forces time compression; many templates need hardware that can host them.
- Plateau UP-state duration grows (logarithmically) with the number of matching templates, unrelated to syllable duration.
- Acoustic variability causes missing/spurious feature spikes; feature-neuron redundancy needs pruning.

## Novelty

Recombination and refinement, not a new mechanism. Closest prior work: Schafer and Jin 2014 (feature-neuron spike-sequence coding, spoken digits), Jin 2008 (dendritic plateau decoding), Unnikrishnan, Hopfield and Tank 1991 (axonal-delay digit recognition). New here: SVM onset/offset spiking events, continuous recognition with insertions/deletions, binary discrimination neurons, and a Loihi 1 implementation with two-compartment plateau neurons and collision circuitry.

## Reproducibility

No code, weights or Loihi configuration release stated. Own 8-bird dataset described, no availability statement; the 11-bird set is public. Splits (60%/40% file-level, fixed seed, 10 training sets per condition) described. No independent reproduction.

(synthesis) Read as a delay-line algorithm demonstration on Loihi 1, not an energy or latency result: the two efficiency-flavoured numbers are boundary-limited and baseline-free.

## Source

- raw/research/weekly-2026-10-29/03-loihi-birdsong-delays.md (arXiv:2610.38564, 2026-10-28)

## Related

- [[../players/intel-loihi2]]
- [[loihi2-persistent-monitoring]]
- [[loihi2-onchip-q-learning]]
- [[neuroml2loihi-celegans]]
- [[../conflicts/snn-energy-payoff]]
- [[../snn/snn-energy-hardware-realistic]]
- [[../snn/snn-energy-breakeven-conditions]]
- [[../benchmarks/neurobench]]
- [[../viability-ledger]]
- [[../devices/event-cameras]]
- [[../weekly-briefs/2026-10-29]] — brought in by the 2026-10-29 weekly sweep
