# Local learning with imperfect analog synapses (CwSG)

Dupuis, Renaudineau, ..., Vianello, Klein and Querlioz (Paris-Saclay C2N, CEA-Leti, Aix-Marseille) propose Channel-wise Spatial Gradient learning (CwSG), a forward-only, layer-local rule for convolutional layers that is trained with single, unverified, sub-1 V pulses on PCM or filamentary-memristor (FM) differential pairs. **All learning results are simulation**: networks are trained in software, with the weight updates replaying *measured* single-device conductance trajectories from 1,189 PCM and 1,268 FM devices. No network was trained on an array, and no energy, latency or area number is reported. The claim is that changing what each layer rewards (spatial variation instead of activation amplitude) makes training robust to write noise that wrecks backpropagation (BP). It bears directly on [[../conflicts/analog-onchip-training-viability]].

## Mechanism

- Each conv layer's output channels are split into class groups (class-to-channel encoding, from the CwC method). The per-class "goodness" is the discrete Dirichlet energy (squared finite-difference spatial gradient) of the group's feature maps; a softmax over goodness gives a local cross-entropy loss. A spatially uniform map scores exactly zero, whereas CwC's amplitude goodness rewards it.
- Layers train greedily: earlier layers frozen, later layers not evaluated. Inference uses only the last layer's goodness scores. No transposed weight read, no inter-layer error transport, no network-wide activation storage (only the active layer's buffers).
- Weights are differential pairs W = s(G+ − G−). One fixed-amplitude soft pulse goes to G+ or G− (or nothing), so updates are ternary and sign-only. StoSignSGD fires each pulse with probability growing with |gradient|, recovering the gradient in expectation with fixed-size writes.
- (Synthesis) The sign-only robustness argument (author-given, explicitly not a formal guarantee): the CwSG goodness derivative sums to zero over a feature map, so the Hebbian factor can take either sign, whereas CwC's non-negative factor drifts net-downward under sign updates (9:1 non-target to target for 10 classes).
- RMSnorm, ReLU, gradient formation, goodness evaluation, random-number generation and the repeated forward passes through frozen layers are digital/peripheral and run at full precision in the simulation.

## Evidenced (simulation, algorithmic, no device model)

CNN-7, 5 seeds, mean test accuracy, full-precision weights:

| Update rule | Method | MNIST | Fashion-MNIST | CIFAR-10 |
|---|---|---|---|---|
| SGD | BP | 99.51 | 93.27 | 86.28 |
| SGD | CwC | 99.18 | 91.07 | 77.77 |
| SGD | CwSG | 99.34 | 92.70 | 83.66 |
| SignSGD | BP | 99.15 | 88.60 | 60.65 |
| SignSGD | CwC | 98.24 | 90.17 | 74.41 |
| SignSGD | CwSG | 98.71 | 91.22 | 83.26 |

- Under SignSGD BP loses 25.6 points on CIFAR-10; CwSG loses 0.4.
- Injected Gaussian write noise (CIFAR-10, SignSGD, simulation): at sigma_eff = 0.01 CwSG holds 61.5% (CNN-7) and 70.4% (CNN-12); BP is near chance by sigma_eff = 0.03 (CNN-7) / 0.01 (CNN-12).
- With StoSignSGD BP recovers to 84.3% (CNN-7) and leads CwSG by up to 6.9 points at sigma_eff <= 0.01; CwSG leads by more than 10 points from sigma_eff = 0.03. So the robustness edge only appears at high noise. Pulses per weight: 39,100 (SignSGD) vs 2,303 (BP, StoSignSGD) and 1,046 (CwSG).
- On an MLP the 1-D difference objective gave no systematic advantage (authors' negative control): the method needs spatially structured feature maps.

## Evidenced (simulation replaying measured device trajectories)

Device boundary: 1T1R arrays in BEOL of 130 nm CMOS. PCM: 300 nm "Wall" cells, 4 kb array, 10,000 identical soft-SET pulses (WL 1.0 V, BL 0.5 V, 100 ns, 700 ns fall), mean step +14.9 nS, saturating near 190 uS. FM: HfOx, 128x64 array, 300 nm devices, 5,000 soft-RESET pulses (BL 0, SL 0.9 V, 600 ns), starting near 90 uS, mean step -3.2 nS. Both have heavy-tailed steps. Weights use measured trajectories reused across the network (no trajectory paired with itself); the training itself is software, single-device statistics only, no array parasitics. CNN-7W, StoSignSGD, batch 256, 5 seeds.

| Task / device | CwSG | BP | Pulses per device (CwSG vs BP) |
|---|---|---|---|
| SVHN, PCM | 82.5% | 82.2% | 6.4 vs 378 (59x fewer) |
| SVHN, FM | 84.9% | 31.5% | 1,688 vs 3,279 |
| CIFAR-10, PCM | 58.6% | 50.0% | 5.1 vs 62 |
| CIFAR-10, FM | 59.4% | 40.2% | 1,415 vs (BP count not stated in main text) |
| MNIST, PCM | similar | similar | 16.2 vs 8.0 (CwSG uses more) |

- Full-precision SVHN baselines: 93.6% (CwSG) and 95.1% (BP), so on-device accuracy is 11 to 13 points below the software ceiling for both.
- Converters (simulation, PCM, SVHN): 8-bit forward DAC/ADC stays within 1 point of ideal for CwSG and for BP with an FP32 backward pass. BP with quantized backward interfaces is near chance at 6 bits and about 8 points below the ideal-backward control at 8 bits. CwSG needs no second converter bank. No converter energy or area is computed.
- Small batches (MNIST, simulation): at batch size 1 CwSG reaches 91.1% on PCM vs 72.3% BP, and 93.2% on FM vs 56.5% BP. On SVHN batch 1, PCM CwSG 41.1% (BP near chance); on FM both near chance.
- PCM vs FM (authors): PCM needs far fewer pulses (about 264x and 277x fewer on SVHN/CIFAR-10); FM gives +2.4 and +0.8 points accuracy.

## Claimed / not shown

- "Analog training becomes a problem of credit assignment" and "algorithmic design rather than hardware compensation alone" is framing, resting on two datasets of device statistics and small CNNs (claimed).
- Pulse-count reductions are described as translating to programming-energy savings, but no energy is measured or modelled; the authors themselves say peripheral arithmetic, memory traffic, RNG and extra frozen-layer forward passes must be counted first. Pulse counts are not energy.
- Authors list as open: closed-loop training on an integrated crossbar with parasitics and the local-learning periphery; at least one channel per class per supervised layer (narrow layers vs many classes); no endurance/retention analysis (FM trajectories grow markedly variable beyond roughly 2,000 to 3,000 pulses; PCM saturates).
- Comparisons are against a specific BP implementation (fixed-pulse, no compensation); the paper cites but does not run mixed-precision digital accumulation or auxiliary-array schemes, which are the actual competing fixes for analog BP.
- Peer-review status not stated in the capture; code released at github.com/INTEGNANO/LL-CwSG, device data on request. LLMs used for copyediting (disclosed).

## Source

- `raw/research/weekly-2026-10-22/01-analog-local-learning.md` — arXiv 2610.27910. Funding: France 2030 / ANR (PEEL, PEIA). Supplementary notes not captured.

## Related

- [[../weekly-briefs/2026-10-22]] — brought in by the 2026-10-22 weekly sweep
- [[../conflicts/analog-onchip-training-viability]] — adds simulation evidence that a different learning rule survives realistic PCM/FM step statistics where BP does not (see Position framing there); still no array-level run
- [[analog-training-nonidealities]] — the asymmetry, noise and saturation non-idealities this paper replays from measured devices
- [[memristor-array-integration-gap]] — 1T1R BEOL arrays here; no yield/defect study
- [[memristor-device-engineering]] — soft-pulse programming regime of FM and PCM
- [[two-state-synapse-equilibrium-propagation]] — another non-BP local rule, but ideal-device software only
- [[reciprocal-tau-cell-log-domain-learning]] — circuit-level local learning, SPICE-only
- [[../snn/snn-training-surrogate-gradients]] — BPTT baseline that local rules aim to replace
- [[../viability-ledger]] — on-chip learning remains paper/sim-only
