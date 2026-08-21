# Training on analog devices: non-idealities and the algorithms that survive them

A blocker distinct from yield, and one the wiki previously conflated with it. [[memristor-array-integration-gap]] frames on-chip learning as a **yield-economics** argument — in-situ training is how you ship an imperfect array. This page adds the constraint underneath that: **plain gradient descent does not work on real analog devices at all**, regardless of defects, because of how their conductance responds to update pulses.

Two sources, and they meet in an unusually clean way: one is theory and simulation establishing the failure mode and its fix; the other is a fabricated array whose measured characteristics show the failure mode's precondition is present even in a device engineered to avoid it.

## The vocabulary

- **Response function** — how much a device's conductance actually changes per programming pulse, as a function of its current state. Ideal is linear and identical up and down.
- **Symmetry / asymmetry** — whether potentiation (up) and depression (down) produce equal-magnitude steps. Real devices are asymmetric; one direction is steeper.
- **Symmetry point** — the conductance where up and down steps balance. Analog SGD implicitly drifts toward it.
- **Tiki-Taka (TT, TTv2, TTv4/AGAD), Residual Learning (RL, RLv2)** — training algorithms designed for asymmetric devices. They use an auxiliary array to accumulate gradients and transfer periodically, rather than applying each update directly to the weight array.

## The failure mode

Simulation, AIHWKIT device model plus PyTorch, mean ± std over 3 runs. Fine-tuning an ImageNet-pretrained backbone with the final FC layer replaced by a simulated analog layer:

| Model / dataset | Digital SGD | **Analog SGD** | TT / RL | TTv2 | RLv2 |
|---|---|---|---|---|---|
| ResNet18 @ CIFAR10 | 95.43% | **84.47 ±3.40** | 94.81% | 95.31% | 95.12% |
| ResNet18 @ CIFAR100 | 81.12% | **68.98 ±1.01** | 76.17% | 78.56% | 79.83% |
| ResNet50 @ CIFAR100 | 83.98% | **79.88 ±1.26** | 80.80% | 82.82% | 83.90% |
| MobileNetV3S @ CIFAR100 | 78.94% | **51.79 ±1.05** | — | — | — |

The gap between Analog SGD and digital reaches **12.1 points** on ResNet18/CIFAR100, and **27 points** on MobileNetV3S. Tiki-Taka-family algorithms recover most of it; the v2 variants recover nearly all.

**And it gets worse than a gap.** Sweeping response-function steepness `γ_res` and dynamic range `τ` on an MNIST FCN, **Analog SGD collapses below 15% accuracy — the 10-class random-guess floor is 10%** — at `γ_res` = 1.0 and 2.0 across all tested `τ`. Under identical conditions, Tiki-Taka and Residual Learning hold **97.0–97.7%**.

**No defects are involved.** This is response-function asymmetry alone, on a nominally perfect array.

Notably, **cycle-to-cycle variation is not the problem.** Sweeping noise up to 120% — exceeding the response-function signal itself — leaves both Analog SGD and Tiki-Taka "not significantly affected," consistent with the paper's theorem that cycle-variation error is higher-order. Asymmetry is first-order; noise is not.

⚠️ **Simulation only.** AIHWKIT plus PyTorch on an RTX 3090. No physical chip, no hardware-in-the-loop, and the response-function parameters are **generic and swept, not fitted to any named device's measured curve.** That last point caps how directly these numbers transfer — which is exactly why the second source matters.

## What a real device actually looks like

**CMO/HfOx ReRAM** (conductive-metal-oxide over hafnium oxide), a fabricated **8×4, 32-cell** array at **130 nm**, BEOL-integrated. This stack is specifically promoted for *symmetric* conductance updates — the property that would make plain Analog SGD viable.

**Inference-relevant characteristics are genuinely good:**

| Metric | Value |
|---|---|
| Forming | ≈3.2 V, σ = 75 mV, **100% yield** across the array |
| HRS/LRS ratio | ≈15× |
| Stable states | **>32 (5-bit)**, ~10–90 µS range |
| Programming noise | <0.1 µS at 0.2% acceptance; <1 µS at 2% — claimed >10× better than PCM |
| Programming cost | ~89 pulses (0.2% range) vs ~11 pulses (2% range) |
| Relaxation @ 10 min | 35 states still distinguishable, 9.6% average overlap |
| Relaxation @ 1 hour | ≈ −0.7 µS average error across 400 states |

**Training-relevant characteristics are not:**

| Metric | Value |
|---|---|
| Usable analog states under open-loop pulsing | **22 average** (range 16–33) — versus >32 for inference |
| **Symmetry-point skew** | **61%** — "the down response is steeper than the up response" |
| **Noise-to-signal ratio at the symmetry point** | **90%** |

*(synthesis)* **This is the finding.** A device engineered for symmetric updates measures **61% asymmetry and 90% NSR** on real silicon. The theory paper says asymmetry in that neighbourhood is what breaks plain Analog SGD. And the CMO/HfOx authors never test plain SGD — they go directly to **AGAD/TTv4**, an algorithm built specifically to tolerate asymmetry, and their own ablation names symmetry (not defects, not noise, not state count) as the dominant accuracy lever.

Two independent sources, one theoretical and one experimental, converging: **asymmetry is the binding constraint on analog on-chip training, and the answer is algorithmic, not material.** Nobody has engineered it away; they have routed around it.

Note also the split between the two tables. Inference wants many stable distinguishable states — 32+, achieved. Training wants small, symmetric, low-noise *incremental* steps — 22 states, 61% skew, 90% NSR. **The same device is good at one job and poor at the other**, and a paper reporting only the inference numbers would look far more encouraging than one reporting both.

## What "on-chip training" meant here

Less than the phrase implies, and worth stating plainly because the title will be cited.

The only physical hardware is that **single 8×4, 32-cell array**, characterised electrically — forming, switching, weight transfer, relaxation, open-loop pulse response. **Every neural-network result — MNIST, LSTM, and all 64×64 and 512×512 scale claims — is `aihwkit` simulation calibrated to that one small array. No network was trained or run on the fabricated chip.**

Two further caveats that should travel with the numbers:

- The **20× / 3× MVM-accuracy improvement** over Wan et al. (Nature 2022) compares this paper's **simulated projection** against Wan et al.'s **hardware-measured** value. A maturity mismatch, not a like-for-like result.
- The **10-year retention figure is a linear extrapolation in log(time)** from measurements out to one week — flagged by the paper itself as a projection.
- **Endurance is never measured.** Write-cycle count appears nowhere in this paper's own results; the endurance advantage is inherited from cited prior work without a number. For a page about *training* — which writes constantly — that is the most conspicuous gap of all.

## Why this matters beyond the device

*(synthesis)* [[../snn/snn-training-surrogate-gradients]] establishes that on-chip learning is *architecturally* constrained: BPTT's O(NT) memory and non-local gradient transport cannot run on a local, event-driven substrate, so hardware learning is restricted to three-factor and local rules. This page adds a second, independent constraint from the device side: even having chosen a local rule, **plain gradient descent fails on real conductance response curves**, and you need Tiki-Taka-class correction on top.

So on-chip learning is squeezed from both ends — the architecture forbids the standard algorithm, and the physics breaks the naive local one. That both constraints have known answers (DCLL-family rules; Tiki-Taka-family updates) is the encouraging part. That neither has been demonstrated together on real silicon at scale is the gap.

## Open questions

- **Has anyone trained a network on a fabricated analog array**, rather than in simulation calibrated to one? No source in this wiki has.
- What is the endurance of a device under Tiki-Taka-style training, which writes far more often than inference?
- Do the Tiki-Taka results hold when response-function parameters are fitted to a *measured* device rather than swept generically?
- Can any material process actually deliver symmetry, or is algorithmic correction permanent?

## Source

- `raw/research/neuromorphic-seed-sweep/12-analog-training-nonideal.md` — "Analog In-memory Training on General Non-ideal Resistive Elements: The Impact of Response Functions", arXiv:2502.06309. Theory plus AIHWKIT simulation; no hardware. ⚠️ pymupdf capture — Tables 7 and 8 are column-garbled; only the values cited above were legible with confidence.
- `raw/research/neuromorphic-seed-sweep/16-cmo-hfox-onchip-training.md` — "All-in-One Analog AI Hardware: On-Chip Training and Inference with Conductive-Metal-Oxide/HfOx ReRAM Devices", arXiv:2502.04524. One fabricated 8×4 array at 130 nm; all network results simulated. ⚠️ pymupdf capture after repeated marker failures — a device paper whose evidence is normally figure-borne; all numbers above are from body text.

## Related

- [[../conflicts/analog-onchip-training-viability]] — the open dispute this page anchors
- [[memristor-array-integration-gap]] — the yield-economics argument this page qualifies
- [[memristor-device-engineering]] — conductance linearity and the state-count/linearity trade-off
- [[../snn/snn-training-surrogate-gradients]] — the architectural constraint on on-chip learning
- [[fefet-analog-imc]] — another device family with no endurance data
