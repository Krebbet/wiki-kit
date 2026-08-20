# SNN energy: estimated vs hardware-realistic

The receipt for [[../conflicts/snn-energy-payoff]]. A Yale group (Bhattacharjee, Yin, Moitra, Panda; arXiv:2309.03388) took six recent SNN training-algorithm papers, re-ran each on two hardware-realistic simulators, and compared the energy-efficiency multiplier each paper *claimed* against what the hardware *delivers*. **Every one overstates.** The gap runs from roughly 2× to more than 12×.

The verdict is skeptical, not dismissive: measured improvements are always positive — SNNs do save energy on both digital and analog accelerators — they are just much smaller than advertised. Pair with [[snn-energy-breakeven-conditions]], which reaches a compatible conclusion analytically.

## The formula the paper says is wrong

Recent SNN algorithm papers estimate energy as:

```
E_est = FLOPs × Timesteps × (1 − Sparsity) × E_AC
```

where `E_AC` is the energy of one INT8 accumulate. The paper's objection, stated plainly: *"such energy evaluation is impractical as metrics such as FLOPs do not account for hardware overheads like memory access and data communication."*

The deeper problem is sparsity. Real digital systolic arrays and analog IMC crossbars **are ineffective at handling spike sparsity during memory fetches**. Sparsity is exploitable *inside* the PE compute unit only — buffer, SRAM and DRAM fetches happen whether or not the operand is a zero spike. The estimate credits energy savings the memory system never delivers.

## Table II — the measurement

CIFAR10, inference only. Each row's baseline is that paper's own stated comparison point, so the baselines are **not standardised across rows**.

| Work | Accuracy | Sparsity | T | **Estimated N×** | **SATA actual** | **SpikeSim actual** |
|---|---|---|---|---|---|---|
| S-BP | 89.3% | 90.0%¹ | 50 | 10× | 4.5× | 5.2× |
| BNTT | 90.3% | 90.5% | 20 | 20× | 2.8× | 4× |
| Direct | 90.5% | 90.0%¹ | 10 | 20× | 2.3× | 4× |
| TSSL | 91.4% | 90.1% | 5 | 80× | 4.9× | 16× |
| LTH | 93.2% | 97.5%² | 5 | 15× | **1.3×** | 2× |
| TDBN | 92.9% | 85.0% | 4 | **83×** | **6.8×** | 25× |

¹ 90% activation sparsity assumed — not reported by those papers.
² LTH's figure is **weight** sparsity, not activation sparsity. Not comparable to the other rows.

Read TDBN: **83× claimed, 6.8× measured** on the digital platform. And LTH: 97.5% weight sparsity yields **1.3×** on SATA, because systolic-array PEs do not turn weight sparsity into energy savings the way the estimate assumes.

The gap is widest where timesteps are high and where the sparsity being counted is the wrong kind.

⚠️ **Source inconsistency:** Table II's caption says all energy values are at 28 nm, but §IV states SpikeSim is calibrated at 65 nm. Unresolved in the paper. Both are recorded as stated.

⚠️ **Transcription note:** the absolute nJ figures in the captured PDF are corrupted by OCR exponent misplacement and were deliberately not transcribed. The N× multipliers — the paper's own primary comparison metric — extracted cleanly.

## The three omitted costs

1. **Repeated computation *and data movement* across timesteps.** The single largest bottleneck; cost scales roughly linearly with T on both platforms. Single-pass ANN inference has no analogue of this. A cited prior result (SpinalFlow) found a 16-timestep SNN can be **16× worse** than its ANN counterpart on a systolic array, purely from repeated per-timestep evaluation.
2. **LIF neuronal module overhead.** Membrane-potential storage and update costs **up to 61.6% of total computation-unit power** — roughly 2× the energy of the accumulate operations it exists to serve.
3. **Analog crossbar non-idealities.** RRAM read noise and IR-drop from interconnect parasitics accumulate error across timesteps. This is an SNN-specific liability: more timesteps means more accumulation.

## The platforms

Both are **simulators, not fabricated silicon.**

- **SATA** — sparsity-aware digital von-Neumann systolic array, 28 nm, three-level memory hierarchy (DRAM/SRAM/PE scratchpads), output-stationary and weight-stationary dataflows. PE = weighted-accumulation unit + LIF module.
- **SpikeSim / SpikeFlow** — monolithic analog in-memory-computing crossbar accelerator, RRAM devices, 65 nm, 64×64 crossbar tiles. DACs encode spikes as row voltages, weights are RRAM conductances, ADCs read column currents. H-trees carry partial sums; an inter-tile NoC carries spikes.

Scope: inference only, two accelerator archetypes, CIFAR10 / Tiny ImageNet, VGG/ResNet, RRAM-only for the analog case. Not validated against measured silicon.

## What fixes it

The paper is constructive — each mitigation is measured:

| Technique | Result | Platform |
|---|---|---|
| **DT-SNN** — dynamic per-input early exit on timesteps | 2.54× lower EDP vs fixed T=4 at similar accuracy; average T drops to **2.14** | SpikeSim, Tiny ImageNet |
| DT-SNN | 46.5% lower total inference energy vs fixed T=4 | SATA, VGG9/CIFAR10 |
| **SNN-tailored dataflow** (weight-stationary, tick-batch) vs output-stationary | **62.5% memory-movement energy saved**; benefit grows with T | SATA, VGG9/Tiny ImageNet, T=4 |
| **LIF sharing** (1 LIF neuron per n channels), C#4 | 75.1% reduction in LIF unit power | SATA |
| LIF sharing, C#2 / C#4 | 1.38× / 2.41× LIF-area reduction | SpikeSim, ResNet18/Tiny ImageNet |
| **Non-ideality-aware weight encoding** (bias toward high-resistance RRAM states) | +40.13 percentage points non-ideal accuracy | SpikeSim, VGG16 4-bit/Tiny ImageNet |
| ...plus **non-ideality-aware BN adaptation** (re-estimate BN stats under noisy activations, weights frozen) | accuracy loss down to **1.22%** vs ideal software baseline | same |

Also measured: on SpikeSim with VGG16/Tiny ImageNet, raising timesteps 1→4 gives **10.4× higher energy-delay product**. Timesteps are the dominant cost knob.

*(synthesis)* Every mitigation here attacks timesteps or the LIF module — i.e. the two things that make an SNN an SNN. The efficiency story is not "spiking is cheap" but "spiking is cheap **if** you can keep T very small and amortise the neuron state." That is the same conclusion [[snn-energy-breakeven-conditions]] reaches from first principles, and it is a narrower claim than the field's marketing.

## Position on analog vs digital

The paper takes an implicit side, and it cuts both ways. Analog IMC (SpikeSim) shows **higher measured multipliers** than the digital systolic array for the same algorithms — TDBN 25× vs 6.8×, TSSL 16× vs 4.9×. But analog carries an **accuracy tax digital does not**: non-ideality-driven loss, mitigated only down to 1.22% with combined weight-encoding and BN adaptation.

So: analog realises more of the theoretical energy win, and pays for it in accuracy robustness. Compare with the peripheral-overhead argument in [[../devices/memristor-array-integration-gap]] — note these are different objections. The Yale paper models crossbar *non-idealities*; the memristor review argues ADC/DAC *conversion* exceeds 70% of system power. Both discount analog, for different reasons, at different boundaries.

## Reproducibility

Both tools are open-sourced by the same lab — `github.com/Intelligent-Computing-Lab-Yale/SATA` and `.../SpikeSim`. BNTT baseline models from `.../BNTT-Batch-Normalization-Through-Time`. The other five baselines' model provenance is not detailed beyond citation.

*(synthesis)* This matters more than usual: the paper's claim is that everyone else's measurement methodology is wrong, and it ships the alternative methodology as runnable code. That is the right way to make this argument, and it is why this source sits at tier 2 rather than tier 1 despite being simulation rather than silicon.

## Open questions

- Does the estimate-vs-actual gap hold on **fabricated** neuromorphic silicon — Loihi 2, Akida, Xylo — rather than simulators? A [[../benchmarks/neurobench]] system-track submission would answer it.
- Training energy is unevaluated, despite SATA being nominally a training accelerator.
- Does the gap hold beyond CV workloads, on the sparse event-driven tasks neuromorphic is actually pitched for?

## Source

- `raw/research/neuromorphic-commercial-viability/06-snn-energy-hardware-perspective.md` — "Are SNNs Truly Energy-efficient? — A Hardware Perspective", arXiv:2309.03388, Bhattacharjee, Yin, Moitra, Panda (Yale). Simulation-based; tier 2 (open harness, independent re-measurement of others' claims).

## Related

- [[snn-energy-breakeven-conditions]] — the analytical companion; compatible conclusion, different method
- [[../conflicts/snn-energy-payoff]] — Position B evidence
- [[../benchmarks/neurobench]] — the standardised protocol that would replace ad-hoc estimation
- [[../devices/memristor-array-integration-gap]] — the analog-overhead argument at the system boundary
