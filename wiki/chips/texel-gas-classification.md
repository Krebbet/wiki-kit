# TEXEL chip — fly-inspired online gas classification

Groningen's BICS Lab pairs a fly-olfaction-style expand-and-sparsify network (fixed random binary projection, k-WTA, 1-bit Hebbian read-out) with 8 commercial MOX gas sensors for online classification of transient responses, and runs a binary hazardous-vs-benign version on its mixed-signal TEXEL chip with on-chip STDP. On-chip result: 74.6% accuracy, 482 nJ/inference (dynamic, read-out layer only, one core, off-chip encoding excluded), 27 µW chip static power. The abstract's "matches an optimised non-linear SVM" holds only for a 64-bit gradient-trained read-out, not the 1-bit variant on chip, and the on-chip result has no baseline on the same data.

## Chip and sensor setup

- **Chip:** TEXEL, a custom mixed-signal processor (subthreshold analog neurons, synapses and learning circuits) with on-chip STDP and binary plastic synapses. Described in an earlier paper (Greatorex et al., Nat. Commun. 2025), not re-described here. Process node and foundry are not stated in this source.
- **Resources used:** one core, 90 neurons × 58 synapses each, 54 plastic and binary. TEXEL hosts 180 neurons over two cores. Two read-out populations of 40 neurons each, drawn from "good" (non-spontaneously-active) neurons; the chip has defective or spontaneously firing neurons that must be screened out.
- **Off-chip front end:** 16 commercial MOX sensors (Winsen, Figaro, FIS, Ogam) on a custom PCB, 8 retained (strongest response). Chamber ~0.05 L, heater 5 V, ADC sampled at 1 Hz, Teensy 4.1 control, three Bronkhorst mass-flow controllers. Gases ethylene, CO, methane at 2000 ppm in air, plus 1:1 binary mixtures.
- **Pipeline:** 8 raw channels → 136-dim features (raw, first and second online derivatives, 56 pairwise differences, 56 ratios) → fixed random binary projection to 10,000 dims → k-WTA (k = 5000) → single feed-forward read-out. On-chip variant: HD length 2000, k = 200 (90% sparsity), encoding done off-chip.
- **Learning:** software uses a stochastic binary Hebbian rule (potentiate with probability p when pre-unit and teacher are active; weights start at 0, never depress; p = 0.01 or 0.1). On chip, teacher-spike-driven STDP, each binary synapse potentiates once only.
- Software experiments are rate/binary-vector computations, not spiking simulations. The SNN exists only in the on-chip demo.

## Measured numbers

**Software** (10 repetitions with independent random projections; train n = 600, test n = 300 presentations; 20 s per presentation, 1 Hz sampling; unitless test accuracy fraction):

| Task | Hebbian 1-bit | 64-bit GD read-out | Linear SVM | RBF SVM |
|---|---|---|---|---|
| Single gas (3 classes, chance 0.33) | 0.881 ± 0.014 | 0.952 ± 0.003 | 0.923 | 0.940 |
| Binary mixtures (6 classes) | 0.645 ± 0.017 | 0.791 ± 0.008 | 0.563 | 0.800 |

- SVM entries are single deterministic fits (std = 0); no significance test versus the network.
- Few-shot (single gas): 3 exposures (1 per class) 0.596 ± 0.109; 21 exposures 0.801 ± 0.050; 48 exposures 0.866 ± 0.037. Peak 0.887 ± 0.008 (p = 0.01, 375 exposures) and 0.886 ± 0.033 (p = 0.1, 105 exposures). At p = 0.1 accuracy declines at large training sets (authors attribute to interference between stored patterns).
- Time within exposure: accuracy at t = 0 is 0.385 ± 0.005 (single) and 0.176 ± 0.008 (mixtures), near chance. Latency is dominated by sensor time constants (20–40 s) and gas delivery, not the model.
- Input expansion (linear SVM, 100 repetitions): 8-dim raw z_sparse 0.840 / 0.533 (single / mixtures); 136-dim z_sparse 0.965 / 0.789; 136-dim dense 0.888 / 0.501. Redundant noisy derived features hurt dense inputs but help after sparse expansion.

**On chip** (binary task: CO = hazardous vs ethylene + methane; one core):

- Data: train 10 exposures (190 readings), class-balanced subset of 76 samples, single pass. Test 150 exposures (50 hazardous, 100 benign; 2,851 readings).
- **Accuracy 74.6%**, per sensor reading, at the Youden-index-maximising point of the ROC curve. The threshold is tuned on the reported ROC; as far as the text shows, the operating point is selected post hoc on the evaluated data.
- **Energy boundary (load-bearing):** **482 nJ per inference is dynamic energy only (Fig. 7e histogram of dynamic power), for the read-out layer only, on one core. Off-chip HD encoding, ADC, sensors, heater, MCU and host are excluded.** Inference window is output spikes summed over 250 ms.
- **27 µW is chip static (idle) power**, not system power.
- (synthesis) At the paper's 1 Hz sampling, 482 nJ × 1 Hz = 0.482 µW, about 1.8% of 27 µW, so chip-level power is almost entirely static; energy per classification depends on duty cycle, and no power-gating scheme is given.
- Not reported: ROC AUC, TPR/FPR at the operating point, on-chip versus software accuracy on the same task, sensor/ADC/MCU power, total system energy.

## Baseline and comparison honesty

- **1-bit versus 64-bit read-out.** The headline "outperforms linear SVM on mixtures" is the 1-bit Hebbian read-out (0.645 vs 0.563), but it trails the RBF SVM by about 15 points (0.645 vs 0.800). "Matches an optimised non-linear SVM" is true only for the 64-bit gradient-descent read-out (0.791 vs 0.800), which is not the binary local-learning variant on chip. On single gases the 1-bit read-out is below the linear SVM (0.881 vs 0.923).
- **Software fairness.** Same sequential 600/300 split for network and SVMs; SVM hyperparameters grid-searched per dataset (RBF C ~2.2e7, gamma 1e-12 / 1e-11, extreme values, grid extended after the optimum hit the lower edge). Network pHD and s were also grid-searched on the same task and reused; selection-versus-test separation is not stated, so mild tuning leakage is possible.
- **No on-chip baseline.** The 74.6% is not compared with the software network, an SVM, or a majority-class predictor on the same data. (synthesis) With 50/100 class counts, always predicting "benign" scores ~66.7% (derived from stated counts), so 74.6% is only ~8 points above trivial. Note the operating point maximises Youden's J, not accuracy.
- **Cross-paper power comparison is not like-for-like.** The paper cites a sparse HD projection on RISC-V PULPv3 at 2 mW and a comparable pipeline on ARM Cortex-M4 at 20 mW (Montagna et al. 2018: different task, classifier and hardware). Its "end-to-end on the order of 2 mW" is not measured in this paper, and the 482 nJ / 27 µW figures cover the chip read-out only. Do not read these as a chip-versus-MCU result.
- "Sub-mW insect brain" is cited from other work, not tested.

## Maturity

Research mixed-signal chip running a small demo: one core, 2 × 40 read-out neurons, binary two-class task, 150 test exposures, lab gas rig. Software results are a lab benchmark (3 gases and mixtures, 8 sensors). No in-field test, no multi-session drift test, no product. Sensor-drift motivation is argued, not tested.

## Commercial signal

Academic: University of Groningen BICS Lab / CogniGron, with an author affiliated to the Institute of Neuroinformatics UZH/ETH. Funding: CogniGron and Ubbo Emmius Funds. No company, customer, design win or availability date; no competing interests declared. Claimed applications (no partner named): portable multi-gas safety detectors, residential alarms, indoor air quality, automotive cabin sensing, mobile robots.

## Blockers stated

- Interference between stored prototypes at higher potentiation probability. Binary weights potentiate once with no depression, so continual learning needs a stop-learning or depression mechanism (authors' suggestion, untested).
- 1-bit read-out is weak on hard mixtures (0.645 vs 0.800 RBF SVM).
- MOX response time and gas delivery set a floor on time-to-prediction; near-chance accuracy at t = 0.
- Sensor drift and recalibration, the stated field problem, is not solved; only argued addressable by few-shot on-chip re-learning.
- Chip constraints force shorter HD codes (2000), off-chip encoding and screening of spontaneously active neurons.
- Low-dimensional (8-channel) inputs deviate strongly from the theoretical kernel (MSE ~1e-2 for 8 inputs vs ~1e-4 for 136).

## Novelty

Refinement and recombination. Expand-and-sparsify (fly LSH, Dasgupta et al. 2017), its count-sketch/novelty reading, and fly-olfaction gas sensing with spiking networks (Diamond et al. 2016) all exist. New here: an evaluation protocol with random sequences and no baseline-recovery cycles (labels from transients); the feature-dimension/CLT analysis showing redundant derived features help the sparse kernel; and the run on TEXEL with binary STDP on real sensor data.

## Reproducibility

No code, data, weights or harness release mentioned. TEXEL is a research chip, not generally accessible. The sensor rig is custom but parts are listed, so it is rebuildable in principle. 10 seeds (100 for the input-expansion table). No independent reproduction.

## Source

- raw/research/weekly-2026-10-29/02-texel-gas-classification.md — arXiv:2610.36999, Pina, Greatorex, Chicca et al., University of Groningen BICS Lab, 2026-10-27/28.

## Related

- [[../players/roster]]
- [[../snn/snn-energy-breakeven-conditions]]
- [[../conflicts/snn-energy-payoff]]
- [[../benchmarks/neurobench]]
- [[spinnaker-event-pinball-closed-loop]]
- [[../snn/spikeduet-mcu-sparse-snn]]
- [[../snn/multi-depth-temporal-fusion]]
- [[loihi2-onchip-q-learning]]
- [[loihi2-persistent-monitoring]]
- [[../weekly-briefs/2026-10-29]] — brought in by the 2026-10-29 weekly sweep
