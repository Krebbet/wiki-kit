# Conflict: the SNN energy payoff

**Status:** open · **Opened:** 2026-08-20 · **Type:** same quantity, order-of-magnitude disagreement

Does spiking actually deliver the energy advantage it is sold on? Both sides are measuring "energy per inference relative to a conventional baseline." They differ by one to two orders of magnitude. The disagreement is **not about physics** — it is about the measurement boundary and the choice of baseline, which is why it is tractable rather than merely rhetorical.

## Position A — the claimed advantage

*Held by: vendors marketing neuromorphic silicon, and SNN algorithm papers estimating energy from operation counts.*

**Vendor claims in evidence:**

| Claim | Owner | Date | What's missing |
|---|---|---|---|
| "500× less energy and 100× faster" for sensor data processing | Innatera | ~Apr 2024 | No named baseline ("conventional approaches"), no workload, no units beyond the multiplier, no boundary, no third-party verification |
| `<300 mW` PCIe / `<200 mW` serial; "near-terabyte TOPS scale efficiency"; avoids "the wasteful always-on energy consumption of traditional AI accelerators" | BrainChip (AKD1500) | 2026-06-30 | No measurement conditions, no workload, no idle/active/peak boundary. No actual TOPS figure, no TOPS/W, no definition of "operation". No competing part named |

**Algorithm-paper claims in evidence.** Six recent SNN training papers estimate energy as `E_est = FLOPs × T × (1−Sparsity) × E_AC` and report improvement multipliers of **10× to 83×** over their own baselines (S-BP 10×, BNTT 20×, Direct 20×, TSSL 80×, LTH 15×, TDBN 83×).

**Device-level claims in evidence.** Memristor switching energies quoted at attojoule-to-femtojoule scale, and array figures up to 1309.1 TOPS/W — none stating whether peripheral power is included.

## Position B — the measured and capacity-matched advantage

*Held by: hardware-realistic re-measurement and first-principles energy modelling.*

**[[../snn/snn-energy-hardware-realistic]]** (arXiv:2309.03388) re-ran those same six papers on two hardware-realistic simulators. **Every estimate overstates**, by roughly 2× to more than 12×:

| Work | Claimed | SATA (digital) | SpikeSim (analog) |
|---|---|---|---|
| TDBN | 83× | **6.8×** | 25× |
| TSSL | 80× | 4.9× | 16× |
| LTH | 15× | **1.3×** | 2× |
| BNTT | 20× | 2.8× | 4× |

Measured gains remain **positive** — SNNs do save energy against those baselines — but far less than advertised.

**[[../snn/snn-energy-breakeven-conditions]]** (arXiv:2409.08290) goes further by enforcing **capacity matching**: an SNN with `T` timesteps is compared to a QNN with `⌈log₂(T+1)⌉`-bit activations, same architecture and mapping. Under that stricter test the SNN **usually loses**:

- Breakeven requires **T ≤ 5 and spike rate < ~5.7%** on typical neuromorphic hardware
- Trace-driven VGG16/CIFAR-10 wins only at T=3 (ratio 0.987); by T=7 it is 2.243× *worse*
- ResNet-18, RepVGG/ImageNet (2.232×), and Transformers all lose. Spiking Llama-2 7B at T=15: **3.793× worse**
- Against a bit-serial QNN, the SNN loses **10 of 12** configurations
- Its excluded control energy "may slightly bias the comparison in favour of the SNN" — the real picture is worse than reported

**[[../devices/memristor-array-integration-gap]]** supplies the analog-side version of the same objection: ADC/DAC conversion exceeds **70% of total system power**, and static leakage runs ~10 mW per 1k×1k crossbar at 1 V. Device-level aJ/fJ figures do not survive to system level — a point the review makes against its own numbers.

**[[../chips/loihi2-persistent-monitoring]]** (arXiv:2608.18341) supplies a same-paper illustration of the boundary effect from real silicon: its own headline "two orders of magnitude" claim is **dynamic-energy-only** (474–496× vs a CPU/GPU baseline), but the same table's **total-energy** multiplier — once static platform power is included — drops to **2.1–40.2×**. One paper, one Table 2, two very different numbers depending only on which boundary is drawn. (Scope caveat: the deployed model is a fixed-point dense autoencoder on Loihi 2 cores, not a trained SNN in the surrogate-gradient/STDP sense — cite as chip/systems evidence for the boundary problem, not as an SNN-algorithm data point.)

## Beyond SNNs: the same boundary problem in AIMC and photonic computing

*(added 2026-08-20, weekly sweep)*

**"Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing"** (Kanjo & De Silva, arXiv:2608.03514, accepted MICRO 2026) is a methodology paper, not a new measurement — but its argument is this conflict generalised beyond spiking. Its own Table 1 lines up three literature chip-scale results (an IBM PCM 34-tile accelerator @14nm, an IBM PCM 64-core accelerator @14nm, and a >16,000-component photonic accelerator) specifically to show that differing, unstated measurement boundaries make published TOPS/W figures **non-comparable across papers**, independent of any dispute about the underlying physics. It explicitly names [[../benchmarks/neurobench]] as the right framework for closing that gap.

This matters for the ruling below: it means the boundary problem this page tracks is not an artefact of how SNN papers happen to report numbers — it recurs identically in analog in-memory compute and photonic accelerators, which strengthens the case that the fix is a *measurement discipline* (system-track, boundary-stated reporting), not something specific to spiking's marketing culture.

## New evidence — 2026-08-21 seed sweep

**Position A gains three claims, all with the same defect:**

| Claim | Owner | What's missing |
|---|---|---|
| "100× less energy… 50× faster than conventional CPU and GPU architectures" | Intel (Hala Point release, ~Apr 2024) | Cites **two external small-scale edge papers**, not any Hala Point measurement. No baseline hardware, workload or methodology in the release |
| "46.9× faster" / "72.7× more energy efficient" / "25× more energy efficient" | IBM (NorthPole) | GPU baseline **never named** — no model, generation, node or precision. No absolute watts or joules. No accuracy delta for the 4-bit quantization |
| "up to ~20× better performance per watt across various AI workloads" | EnCharge (EN100) | No baseline, no workload, no precision. Extends the pattern into **non-spiking analog IMC** |

**And Intel's headline contradicts its own arithmetic.** Hala Point's 20 petaops at 2,600 W is **≈7.7 TOPS/W** — about half its stated ">15 TOPS/W". The 15 figure comes from a synthetic benchmark: a 14,784-layer MLP **stimulated with random noise**, pruned 10:1, sigma-delta neurons at 10% activation. Not a real workload. See [[../players/intel-loihi2]].

**Position B gains its cleanest confirmation yet.** [[../snn/ann2snn-differential-coding]] converts transformers training-free and finds the energy ratio **crossing 1.0 exactly where accuracy reaches parity** — ViT-Small 1.05, EVA02-Base 1.17, EVA02-Small 1.21 at T=8. The converted SNN costs *more* than the source ANN. That comes from a conversion paper, motivated to show conversion works, measuring against a full-precision baseline more generous than the capacity-matched one. It still loses.

**A same-paper boundary flip, measured on silicon.** [[../chips/loihi2-persistent-monitoring]] reports ~474–496× versus CPU on **dynamic energy only**, and **7.2–40.2×** on total energy — same table, same hardware, an order of magnitude apart. Static power (16.05 W of ~16.2 W) dominates because the model occupies 74 of ~2,048 cores. This is the single cleanest illustration in the wiki that the boundary *is* the claim.

*(synthesis)* One qualification worth stating: NorthPole and the MatMul-free LLM result are **not spiking**. Their numbers belong to the boundary-honesty dispute, not to SNN evidence — do not merge them into spike-rate comparisons.

## What separates the positions

Three things, all methodological:

1. **Measurement boundary.** Position A quotes device-level or compute-only figures; Position B counts memory access, data movement, neuron-state overhead and peripheral conversion. The costs Position A omits are not second-order — repeated per-timestep data movement is named as the single largest bottleneck, and the LIF module alone reaches 61.6% of computation-unit power.
2. **Baseline capacity.** Position A compares against an unmatched or unnamed baseline. Position B's capacity-matched twin removes the confound, and it is precisely that stricter baseline that flips the verdict from "wins by less" to "usually loses."
3. **What sparsity buys.** Position A credits sparsity with proportional energy savings. Both Position B sources show sparsity is exploitable *inside* the compute unit but not in memory fetches — and [[../benchmarks/neurobench]]'s own RED-ANN baseline demonstrates it directly: 0.634 activation sparsity yielding 87% of dense effective ops, because normalization before weight multiply re-densifies them.

## Where the sides actually agree

Worth recording, because the dispute is narrower than it looks:

- **Neither Position B source claims SNNs never win.** Both identify a genuine favourable regime: short time windows, low spike rates, sparse-friendly interconnect.
- **[[../benchmarks/neurobench]] supplies a properly-measured Position-A-shaped result**: SynSense Xylo Audio 2 vs an Arduino at matched accuracy — **60.9× less dynamic power, 33.4× less dynamic energy**, boundary disclosed, pre-processing reported separately, and the 84 ms vs 45 ms latency cost admitted. Large wins are achievable; they are just rarer and more conditional than the marketing implies.
- **The limiting factor may be the hardware, not the algorithm.** Reducing sparse-event movement overhead `η` from its nominal Loihi-1-normalized value of 12 down to 1 flips the SNN from winning 1 of 12 configurations to **12 of 12**. That reframes the whole dispute: the problem is the routing fabric, and it has a known target.

## Resolution condition

**A [[../benchmarks/neurobench]] system-track submission from a vendor whose claims are currently unquantified** — BrainChip, Innatera, or a peer — measured against a same-tier conventional baseline at matched accuracy, with idle/active/dynamic power separated and pre/post-processing disclosed.

That is a specific, achievable event. NeuroBench defines exactly the protocol, the vendors in question are already co-authors on the framework, and the two existing system-track baselines (Xylo, Loihi 2) show the measurement is practical. Its absence is itself informative: **as of 2026-08-20 no vendor in this wiki has published an efficiency figure at a stated measurement boundary against a named baseline.**

Secondary conditions that would move the needle: measured silicon (not simulation) confirming the estimate-vs-actual gap; a peripheral-inclusive TOPS/W figure for any analog crossbar; or a specialized sparse-event accelerator (LoAS, SpikeX, Bishop) demonstrating η≈1 in hardware.

## Ruling

**None yet — deliberately.** *(synthesis)* The evidence does not currently support either position as stated. It supports a third, narrower claim: *spiking wins decisively in a specific regime (very short time windows, very low spike rates, sparse-event-optimized interconnect, and workloads that are natively sparse and event-driven), and loses to a well-optimized quantized ANN outside it.* Both Position B sources converge on this independently, by different methods, and the Xylo result shows the favourable regime is real and reachable rather than theoretical.

What is **not** supported is any unconditioned multiplier — "500×", "83×", "near-terabyte TOPS scale" — quoted without a boundary. Those should be recorded in this wiki as claims with an owner and a date, never as facts.

## Source

- `raw/research/neuromorphic-commercial-viability/02-innatera-21m-round.md` — Innatera 500×/100× claim (⚠️ ~Apr 2024 vintage)
- `raw/research/neuromorphic-commercial-viability/01-brainchip-akd1500-shipments.md` — BrainChip power and efficiency claims
- `raw/research/neuromorphic-commercial-viability/06-snn-energy-hardware-perspective.md` — estimated vs measured, six algorithm papers
- `raw/research/neuromorphic-commercial-viability/07-snn-energy-reconsidered.md` — capacity-matched breakeven analysis
- `raw/research/neuromorphic-commercial-viability/05-neurobench.md` — the measurement protocol and the Xylo/Loihi baselines
- `raw/research/neuromorphic-commercial-viability/04-memristor-codesign-review.md` — peripheral overhead at the analog boundary
- `raw/research/weekly-2026-08-20/01-beyond-peak-tops-per-watt.md` — arXiv:2608.03514, the boundary problem generalised to AIMC/photonic
- `raw/research/weekly-2026-08-20/02-loihi2-acoustic-anomaly-detection.md` — arXiv:2608.18341, same-paper dynamic-vs-total illustration

## Related

- [[../snn/snn-energy-hardware-realistic]] · [[../snn/snn-energy-breakeven-conditions]] — Position B
- [[../benchmarks/neurobench]] — the adjudicator
- [[../players/brainchip]] · [[../players/roster]] — Position A claimants
- [[../devices/memristor-array-integration-gap]] — the analog-side objection
- [[../chips/loihi2-persistent-monitoring]] — same-paper dynamic-vs-total illustration
- [[../viability-ledger]] — what this dispute gates
- [[../weekly-briefs/2026-08-20]] — brought in by the 2026-08-20 weekly sweep
