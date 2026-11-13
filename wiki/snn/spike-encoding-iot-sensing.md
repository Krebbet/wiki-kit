# Spike encoding across IoT sensing modalities

Hou et al. (SUSTech / Zhejiang; arXiv 2611.11317) compare SNN input encoders (direct, interleaved slicing, Haar, hybrid, level crossings) on six public tasks across WiFi, inertial, sEMG (surface electromyography) and tactile sensing, pairing task metrics with an FP32 45 nm arithmetic estimate and GPU/SoC rail energy measured on a Jetson AGX Orin. **Evidenced:** the arithmetic estimate and the measured rail rank encoders differently on a dense GPU backend; interleaving cuts measured ARIL energy about 6x. **Not evidenced:** anything on neuromorphic silicon. This is a simulated-estimate-plus-GPU-measurement study, not a neuromorphic hardware result.

## Key findings (with boundaries)

Measurement boundary for all "measured" numbers: frozen model replayed on Jetson AGX Orin (PyTorch 2.8, CUDA 12.6, FP32, TF32 off, batch 1), from a prepared host window to returned scores, including input preparation, encoding, transfers and state reset. Energy is integrated from the named supply rail (GPU/SoC) and includes background draw; whole-board energy is unavailable. The power instrument is not named. "Arithmetic estimate" covers only conv/linear MACs and accumulates at 0.9 pJ per AC and 4.6 pJ per MAC (45 nm, 0.9 V, FP32); memory, transfers, background power, encoding ops and neuron-state updates are excluded.

- **Fewer presented values cut measured cost (evidenced, one frozen model, seed 41).** ARIL (WiFi), 4 SNN steps: interleaving presents 9,984 values vs 39,936 for Direct. p50 latency 13.09 vs 26.50 ms; GPU/SoC rail 121.64 vs 725.98 mJ per window; arithmetic estimate down 83.77%. Mean dev accuracy equal at 88.93% over 5 seeds; contiguous slicing 73.04%. Resetting state between steps drops interleaved accuracy to 25.18%.
- **Compact repetition can match or beat interleaving (evidenced, 5 paired seeds, dev split).** Best dev accuracy: interleaving 88.39 +/- 1.41%, fixed phase repeated 89.82 +/- 1.74%, low-pass then repeated 90.54 +/- 1.02%. Device cost of these controls was not measured.
- **Arithmetic estimate and measured energy diverge (evidenced, UCI-HAR, one frozen seed).** Median rail energy Direct SNN / fixed Haar events / GAC SNN / continuous ANN: 231.68 / 258.19 / 239.20 / 113.48 mJ per window; latency 52.62 / 63.50 / 54.62 / 31.89 ms. Haar has a slightly lower arithmetic estimate than Direct but higher measured energy; the ANN has the highest estimate (reported as 2,866.36 per window, unit given as "J" in the text, probably uJ) and the lowest measured energy. The dense backend executes binary spikes as tensor operations, so sparsity does not become savings.
- **Same pattern for tactile level crossings.** Effective accumulations fall 37-40% yet latency and rail energy rise by 0.235 ms and 0.813 mJ per window (screwdriver, 3 seeds, +/-0.084 mJ).
- **Accuracy gains cost device energy.** MHEALTH cached weighted Haar: 76.13 to 84.29% dev accuracy (3 seeds) for +34.18 mJ and +8.24 ms per window. Widar3.0 hybrid: 76.47 to 77.69% (3 seeds), +40.03 mJ and +12.48 ms (one seed).
- **Overall accuracy hides error type.** uSkin screwdriver, epoch 40: level crossings raise accuracy 57.34 to 61.64% but lower slip recall 67.52 to 60.52% (FPR 48.14 to 37.75%). Per object (1 seed each) recall moves -2.45 (brush) and -23.00 points (SpoolSolder). At cross-entropy-selected checkpoints (epochs 1-3 for brush and SpoolSolder) the ranking reverses: level-crossing recall +17.75 / +6.23 / +24.63 points, with higher FPR. Encoder and checkpoint rule jointly set the operating point.
- **Per-user gains are small and uneven.** Ninapro DB6 day-3, same 10 users, 1 seed: level crossings 48.36 vs 46.98% (+1.39 points; 95% paired bootstrap over users 0.17 to 2.59); 8 of 10 users improve, 2 lose about 1.5 points. Added rail cost 0.457 +/- 0.320 mJ per window.

## Baseline honesty

- Positive: the paper separates estimate from measurement, names exclusions, reports its own negative results, and counterbalances replay blocks with telemetry coverage checks (at least 99% block coverage, no gap above 0.5 s).
- Thin statistics: most device comparisons use one frozen model from one seed (UCI-HAR, Widar, Ninapro, brush, SpoolSolder). Several effects sit near their stated variation. Accuracies are development-split, with checkpoints chosen on those splits, and absolute accuracy is low on Ninapro (about 47-48%) and uSkin (57-67%).
- Weak baselines: the only non-spiking comparator is a continuous ANN (UCI-HAR, uSkin screwdriver), which beats every SNN on rail energy in UCI-HAR (113.48 mJ vs 231.68 mJ; -51.02%) at 2.44 points lower accuracy than Direct SNN. No MCU, digital NPU or neuromorphic chip is measured, so nothing here shows event-driven savings; the dense GPU cannot exploit them by construction.
- The 45 nm FP32 estimate is a standard but optimistic convention, kept separate from measurements by the authors.

## Maturity

Academic characterisation study on public datasets (ARIL, Widar3.0, MHEALTH, UCI-HAR, Ninapro DB6, uSkin). arXiv preprint; peer-review status not stated. No deployed system, no closed-loop test (the authors flag a closed-loop slip experiment as future work), no code release link found.

## Blockers and open questions

- Estimates do not predict measured energy on dense backends; a measurement on sparsity-exploiting hardware (neuromorphic or event-driven FPGA) is missing.
- Encoding and event-conversion cost must be counted when hardware accepts only spikes.
- Runtime adaptation (changing input coverage, precision, steps) is unevaluated against the best static configuration after control costs.
- Device cost of repetition controls and selected tactile checkpoints is unmeasured.

(synthesis) For the wiki's viability question, this is weak evidence about neuromorphic hardware and useful evidence about toolchain maturity: on commodity GPUs the choice of encoder is a profiling problem, and spike-count or AC-count proxies cannot be trusted for ranking. It reinforces [[snn-energy-hardware-realistic]] from a different angle (measured dense GPU rather than a hardware-realistic simulator), with no contradiction.

## Source

- `raw/research/weekly-2026-11-12/01-spike-encoding-iot.md` (arXiv 2611.11317)
- Derived summary: `raw/research/weekly-2026-11-12/.ingest/01-spike-encoding-iot.summary.md`

## Related

- [[snn-energy-hardware-realistic]]
- [[snn-energy-breakeven-conditions]]
- [[snn-training-surrogate-gradients]]
- [[spiking-mmwave-isac-fpga]]
- [[spikeduet-mcu-sparse-snn]]
- [[../benchmarks/neurobench]]
- [[../conflicts/snn-energy-payoff]]
- [[../chips/hyvox-xylo-speaker-id]]
- [[../weekly-briefs/2026-11-12]] — brought in by the 2026-11-12 weekly sweep
