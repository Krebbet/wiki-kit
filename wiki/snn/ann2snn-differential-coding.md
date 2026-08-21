# Training-free ANN-to-SNN conversion: differential coding

The conversion branch of the training taxonomy ([[snn-training-surrogate-gradients]]), developed to the point where it matters for energy. ANN-to-SNN conversion has historically needed **large T** — tens to hundreds of timesteps — to match source-ANN accuracy, which is exactly the regime where [[snn-energy-breakeven-conditions]] says SNNs lose. This paper (arXiv:2503.00301) pushes CNN conversion to **T = 4–8** with no retraining.

The verdict for this wiki is genuinely mixed, and the mixedness is the finding: **CNNs move into the favourable regime; transformers confirm that they cannot.**

## Two mechanisms, and only one of them is the title

**Differential coding.** Standard rate coding lets the decoded value decay by `(t−1)/t` each step, so late spikes contribute less and precision converges slowly. Differential coding instead accumulates spikes as **direct corrections to a running encoded value**, with no decay term — once the running estimate is close enough to the target activation, the neuron simply stops firing.

**Multi-threshold (MT) neurons.** Multi-level spiking neurons with `2n` thresholds (n positive, n negative, powers of two via bit-shift), emitting at most one spike *plus an index* per timestep. At `n=1` this reduces to a standard IF neuron with one added negative threshold.

⚠️ **The paper's own ablation shows MT neurons do most of the work, not differential coding.** At `n=1`, ResNet34 still needs **T ≈ 64** to reach 74.11% — squarely the historical large-T regime. It is `n=4`/`n=8` that buys T=4–8 parity. Anyone citing "differential coding achieves low-T conversion" is citing half the mechanism.

*(synthesis)* And MT neurons weaken the premise that makes spikes cheap. A multi-threshold neuron transmits **a threshold index alongside each spike** — not a plain single-bit AER event. That is the same move [[../players/intel-loihi2]] made with graded spikes, and it points somewhere uncomfortable: the interventions that make spiking competitive on accuracy at low T are the ones that make a "spike" carry more than one bit. At what point is this a low-precision digital accelerator wearing spiking vocabulary?

## Results

Energy ratio = `E_SNN/E_ANN`. ⚠️ **Baseline is the full-precision source ANN**, via an analytical Horowitz-2014 model (E_MAC 4.6 pJ, E_AC 0.9 pJ, MACs_SNN assumed ≈ 0) — **not** the capacity-matched quantized ANN that [[snn-energy-breakeven-conditions]] uses. That is a materially more favourable comparator, so these ratios overstate the SNN's relative advantage.

**CNNs — inside the favourable regime**

| Model (ANN acc.) | Config | Accuracy | Δ | Energy ratio |
|---|---|---|---|---|
| VGG16 (73.25%) | n=4, **T=4** | 72.72% | −0.53 pp | **0.15** |
| VGG16 | n=4, T=8 | 73.17% | −0.08 pp | 0.22 |
| ResNet18 (71.49%) | n=4, T=4 | 70.07% | −1.42 pp | 0.14 |
| ResNet34 (76.42%) | n=4, T=8 | 76.04% | −0.38 pp | 0.37 |
| ResNet34 | **n=1, T=64** | 74.11% | −2.31 pp | **0.97** |

That last row is the control, and it is the most informative one in the table: without MT neurons, you need T=64 and the energy advantage almost vanishes.

**Transformers — the ratio crosses 1.0**

| Model (ANN acc.) | Config | Accuracy | Energy ratio |
|---|---|---|---|
| ViT-Small (81.38%) | T=4 | 81.11% | 0.62 |
| **ViT-Small** | **T=8** | 81.43% (parity) | **1.05** ⚠️ |
| ViT-Base (84.54%) | T=8 | 84.23% | 0.92 |
| **EVA02-Base** (88.69%) | **T=8** | 88.46% | **1.17** ⚠️ |
| **EVA02-Small** (85.73%) | **T=8** | 85.64% | **1.21** ⚠️ |

**Across every transformer model, the energy ratio crosses 1.0 between T=6 and T=8 — exactly where accuracy first reaches near-parity.** The converted SNN costs *more* energy than simply running the source ANN, by the paper's own optimistic accounting, against its own favourable baseline.

*(synthesis)* This is the cleanest confirmation in the wiki of the transformer half of [[../conflicts/snn-energy-payoff]]. It is not a hostile analysis — it is a conversion paper, motivated to show conversion works, using a baseline that flatters the SNN, and it still lands above 1.0 precisely at the accuracy the method exists to achieve. Independent methods now agree: [[snn-energy-breakeven-conditions]] found spiking transformers degrading as `T/⌈log₂(T+1)⌉` and a spiking Llama-2 7B at 3.79× worse; this finds ratios of 1.05–1.21 at parity. **Transformers do not convert into an energy win.**

The paper is candid about why transformers fare worse: its threshold-iteration method (a closed-form calibration solve, requiring one forward pass over a dataset to get per-ReLU statistics — calibration, not fine-tuning) is *"not suitable"* for transformers. They fall back to a fixed statistical threshold at `c=4, n=8`. Non-ReLU operations — GeLU, SiLU, LayerNorm, Softmax, matmul — need "differential graded units" that track a running proxy for the unconverted activation and emit a correction each step.

**Detection and segmentation** follow the CNN pattern: FCOS-ResNet50 reaches 39.2 mAP at T=8 (ratio 0.75); FCN-ResNet50 reaches 64.5 mIoU at T=8 (ratio 0.63).

**Against prior conversion work**, the CNN gain is real: TS needs T=64 for VGG16, QCFS T=64 for ResNet34, MST T=128–512 for Swin-T, STA T=32–256 for ViT-B/32. An 8–16× reduction in T. Though the paper notes one prior method (ECMT) already reached T=8–10 on transformers, so this is not the sole low-T result.

## What is not reported

**No spike rate. No spike count.** Anywhere. Only the derived energy ratio. The agent confirmed by text search — not a figure-only omission.

*(synthesis)* That is a significant gap for this wiki specifically, because spike rate is the variable [[snn-energy-breakeven-conditions]] thresholds on (`sr < ~5.7%`). Without it, these results cannot be placed on that page's axes, and the two analyses cannot be reconciled quantitatively — only directionally. It also means the paper's own energy model, which derives spike counts from an untabulated "statistical spike emission rate η", cannot be independently checked.

**Analytical, not measured.** The same MAC/AC-counting style that [[snn-energy-hardware-realistic]] demonstrated overstates real hardware savings by up to an order of magnitude — it omits memory access and data movement, which every measured result in this wiki finds dominant. The true hardware ratios are likely worse than shown, on both the CNN and transformer rows.

## Where this leaves the energy question

*(synthesis)* Combining this with the rest of the wiki, the picture sharpens into something more useful than "SNNs are/aren't efficient":

- **CNNs, converted, low T, MT neurons:** plausibly a genuine win, though the margin needs re-testing against a capacity-matched quantized baseline and on real hardware.
- **Transformers, converted:** not a win, by two independent methods, one of them motivated to find one.
- **Attention-free recurrent architectures natively mapped:** a preliminary measured win, per [[../players/intel-loihi2]] — but not iso-accuracy.

The dividing line is not spiking versus not-spiking. It is **whether the architecture has a dense global mixing operation** — attention — that has to be evaluated repeatedly across timesteps.

## Open questions

- Spike rates. Without them these results cannot be placed on the breakeven axes.
- What do the CNN ratios become against a capacity-matched quantized ANN rather than full precision?
- What do they become on measured hardware rather than a MAC/AC model?
- Do MT neurons remain cheap on real event-driven hardware, given they transmit an index per spike?

## Source

- `raw/research/neuromorphic-seed-sweep/15-differential-coding-ann2snn.md` — "Differential Coding for Training-Free ANN-to-SNN Conversion", arXiv:2503.00301. Analytical energy model; GPU simulation. ⚠️ pymupdf capture — no figures.

## Related

- [[snn-energy-breakeven-conditions]] — the thresholds these results cannot quite be placed against
- [[snn-energy-hardware-realistic]] — why analytical MAC/AC counting overstates
- [[snn-training-surrogate-gradients]] — the taxonomy this branch belongs to
- [[../conflicts/snn-energy-payoff]] — the transformer rows are Position B evidence
- [[../players/intel-loihi2]] — graded spikes, the same more-than-one-bit move
