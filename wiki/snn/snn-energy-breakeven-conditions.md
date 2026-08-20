# SNN energy breakeven conditions vs quantized ANNs

The analytical companion to [[snn-energy-hardware-realistic]], and the more uncomfortable of the two. arXiv:2409.08290 builds a **capacity-matched comparator** — the "QNN-SNN twin" — plus a first-principles compute-and-data-movement energy model, then derives closed-form conditions for when spiking actually wins. Its answer: SNN energy superiority is real but **confined to a narrow regime**, and on most realistic trace-driven workloads the SNN *loses* to its capacity-matched quantized-ANN twin.

The paper's own framing: SNN efficiency is "not a given" and "not absolute" but "a conditional property emerging from a complex interplay of algorithmic choices and hardware realities." It replaces the general claim with quantitative operating-region boundaries.

## The capacity-matching fix

The methodological contribution. Prior comparisons pit an SNN against an *arbitrary* ANN, confounding energy with representational capacity. This paper enforces a match:

> **Theorem 1.** An SNN over `T` timesteps ↔ a QNN with activations quantized to `⌈log₂(T+1)⌉` bits, same architecture, weight datatype, and mapping. Exact when input current is in `[0, threshold)`, non-leaky, reset-by-subtraction.
>
> **Theorem 2 (input spike-rate bound).** `(1−γ)/T ≤ sr ≤ 1−γ`

Symbols used throughout: `T` = time window; `sr` = network-average spike rate; `γ` = QNN activation sparsity; `N_src` = fan-in; `k` = `E_MAC/E_ACC`.

The second omission it names is the one that decides everything: **SNNs require `T × sr` data accesses per weight per neuron-activation cycle, where an ANN fetches each weight once.** Event-driven sparsity does not eliminate repeated access; it multiplies it by T.

## Compute-only breakeven

Dropping the `O(1/N_src)` term: **`T·sr ≲ k(1−γ)`**

| SNN case | Spike rate | SNN wins if |
|---|---|---|
| Best | `sr = (1−γ)/T` | `k ≥ 1` — any positive MAC-vs-ACC premium |
| Average | `sr = (1−γ)(1/T+1)/2` | `k ≥ (1+T)/2` |
| Worst | `sr = 1−γ` | `k ≥ T` |

That is compute only. Data movement is where it goes wrong.

## The headline crossover

**Typical Neuromorphic hardware, T=5, 4-bit weights, N_src=4096: the SNN beats its QNN twin only if spike rate `sr < ~5.7%`.** General design recommendation: **T ≤ 5 and sr below ≈5.7%**.

Three modelled hardware settings, calibrated on a commercial **22 nm** standard-cell library (Design Compiler, TT, 0.80 V, 25 °C, 1 GHz) with SRAM energies from a memory compiler at the same corner:

| Setting | Sparse move `Ẽ_move` | Dense move `E_move` |
|---|---|---|
| Theoretical Minimum | 0 (isolates compute) | 0 |
| **Typical Neuromorphic** | **3.0 pJ/bit/hop** (normalized from Loihi 1's reported per-event routing energy, incl. metadata overhead) | 0.25 pJ/bit/hop (in-house 22 nm circuit-switched NoC) |
| Worst-Case Sparse | 1300 pJ/bit (one 64-bit DRAM read per spike) | ~20.3 pJ/bit |

`E_ACC = E_CMP = E_SUB = 0.05448 pJ`.

**Sensitivity of the 5.7% figure** (±50% on one parameter at a time): data movement dominates — varying move/weight energies shifts the crossover across **3.41%–10.80%**. Weight energy alone: 5.39%–6.08%. ACC/MAC energy: ≤0.05 percentage points. A ±1 percentage-point absolute error in `sr` changes the energy ratio by up to 17.39%.

*(synthesis)* So the threshold is really a statement about the interconnect, not the arithmetic. Which is the same conclusion [[snn-energy-hardware-realistic]] reaches by measurement and [[../devices/memristor-array-integration-gap]] reaches at the peripheral boundary. Three independent routes, one answer: **in neuromorphic, moving data is the whole cost**.

Other breakeven trends: at 8-bit weights and N_src=4096, breakeven `sr` falls from ≈0.297 (T=1) to ≈0.082 (T=3). Fan-in matters little at scale (0.057 at N_src=4096 vs 0.054 at N_src=64). Higher weight precision *widens* the SNN's window (breakeven sr 0.104 → 0.123 going 4-bit → 8-bit at T=2), because it inflates QNN MAC energy disproportionately.

**Sparse-vs-dense dataflow crossover:** at `sr ≈ 0.12–0.17` (weight-width dependent) the SNN's sparse-event movement cost exceeds dense broadcast cost. Above that, a spiking layer should switch to dense dataflow — i.e. stop being event-driven.

## Trace-driven results — the SNN mostly loses

Ratios are `E_SNN / E_QNN`. **Below 1.0 the SNN wins.**

**VGG16, khop=0.64:**

| T | CIFAR-10 | CIFAR-100 |
|---|---|---|
| 3 | **0.987** | 1.262 |
| 4 | 1.026 | 1.316 |
| 5 | 1.406 | 1.635 |
| 6 | 1.824 | 1.953 |
| 7 | 2.243 | 2.270 |
| 8 | 1.966 | 1.958 |

CIFAR-10 spike rates run 5.49% → 8.52% over T=3→8. Accuracy gap between twins is ≤~1.7 pp throughout — the comparison is fair.

**Other models:** ResNet-18/CIFAR-10 1.071 · VGG16/CIFAR-100 1.262 · ResNet-18/CIFAR-100 1.023 · **RepVGG/ImageNet 2.232**.

**Transformers are worse** (SST-2, khop=4.75): 0.996 (T=1) → 1.500 (T=3) → 2.338 (T=7) → **3.762 (T=15)**. In the dense regime both twins are dominated by dense movement, so the ratio collapses to `T / ⌈log₂(T+1)⌉`. Confirmed at LLM scale: **spiking Llama-2 7B, T=15 — measured 3.793 vs predicted 3.75.** All 7 GLUE tasks at 2-bit/T=3 sit at ≈1.500.

**Against a bit-serial QNN** (Stripes/Neural-Cache style), the SNN loses **10 of 12** configurations.

**TTFS coding** (sparse temporal coding) is the one bright spot: VGG16/CIFAR-10 wins 5 of 6 configs (ratios 0.732, 0.661, 0.790, 0.907, 1.001, 0.811); CIFAR-100 wins 2 of 6 with near-parity elsewhere.

## The hardware-overhead lever

The paper's clearest result, and the one that reframes the debate. Varying `η = Ẽ_move/E_move` across 12 VGG16 configs:

| η | SNN wins | Ratio range |
|---|---|---|
| 1 | **12 / 12** | 0.594–0.872 |
| 4 | 11 / 12 | 0.541–1.020 |
| **12** (≈ nominal, Loihi-normalized) | **1 / 12** | 0.987–2.270 |
| 64 | 0 / 12 | 1.316–2.282 |

*(synthesis)* Read that column. At today's typical neuromorphic sparse-event overhead the SNN wins one configuration in twelve; at unit overhead it wins all twelve. **The limiting factor is the routing fabric, not the algorithm.** That is a far more actionable finding than "SNNs are/aren't efficient" — it says the field's efficiency problem is a hardware-design problem with a known target, and it makes specialized low-overhead sparse-event accelerators (the paper cites LoAS, SpikeX, Bishop) the thing to watch rather than the next training-algorithm paper.

Routing hops matter correspondingly. Parity points for a typical SNN (T=4, sr=0.1) sit at khop ≈ 0.46 (no reuse) to ≈ 0.67 (SNN temporal reuse only). Real mappings: CanMore/mesh VGG16 ≈ 0.64 hops, SNEAP ≈ 1.5, **Allspark transformer ≈ 4.75** — which is why transformers fare so badly.

## Robustness checks

- **Weight sparsity** (bitmap encoding, zero-weight fraction 0–0.9): max relative change 0.10%, or 2.82% with ideal zero-weight compute gating. **Never flips the winner** in any of 12 configurations.
- **Structural cross-check** against Timeloop/Sparseloop on two audited configurations: both give exactly FW=1 (each unique weight fetched once) and FP=0 (no partial-sum spill) — zero deviation from the model's assumptions.
- **Input noise** (σ=2/255): spike rate and ratio barely move. At σ=8/255 accuracy drops 9.43/16.82 pp while the energy ratio shifts little — **accuracy degrades far faster than the energy ratio**.
- **Leak sweep** (λ=0.90–0.99): weaker leak → more firing → sr 5.657%→6.569% (CIFAR-10), ratio 1.121→1.301.

## Stated limitations

1. **Control energy is excluded**, assumed low for specialized dataflow architectures. Since event-driven execution needs extra scheduling and arbitration, this omission **biases the comparison in favour of the SNN** — the paper says so. The real picture is worse than reported.
2. **Neuron-level aggregation** — per-neuron leak, residual membrane state and clipping are aggregated to network level, so layer-wise variation may be missed. Results are "first-order estimates."
3. **Latency conclusions are explicitly weaker than energy conclusions** — routing, arbitration, synchronization and load imbalance are excluded; that section is qualitative.

For genuine efficiency the paper requires a *confluence*: low total spike-event count (low `T·sr`), hardware optimized for cheap sparse-event processing (low `Ẽ_move`), and a substantial MAC-to-ACC ratio (`E_MAC ≫ T·E_ACC`).

## How this sits against the sibling source

Not a contradiction — a sharpening. [[snn-energy-hardware-realistic]] measures six algorithm papers on two simulators and finds SNNs **always beat their own stated baselines**, just by far less than claimed (1.3–25× actual vs 10–83× estimated). This paper enforces **capacity matching** and finds the SNN often **loses outright**.

*(synthesis)* The difference is almost certainly the baseline, not a disagreement about physics. The Yale paper inherits each source paper's own non-standardised baseline; this one constructs a same-capacity QNN twin. Capacity-matching is the stricter and more honest test, and it is what moves the verdict from "wins by less than advertised" to "usually loses outside a narrow regime." Both agree on the mechanism — timesteps and data movement — and both agree the answer is conditional. Recorded as Position B evidence in [[../conflicts/snn-energy-payoff]].

## Practical guidance the paper offers

Aimed at compiler and training teams: minimise hop count in layer placement; keep weights on-chip across timesteps to exploit temporal reuse (up to T×); switch a layer to dense dataflow once `sr` exceeds ≈0.12–0.17; and in training, target **T ≤ 5 and sr < ~5.7%** via rate regularization, pruning, or sparser codes such as TTFS. Its blunt deployment implication: outside that regime, **"a well-optimized QNN is often the more energy-efficient choice."**

## Open questions

- Does the capacity-matched result hold on fabricated silicon? The model is anchored to **Loihi 1** routing energy; Loihi 2 and newer fabrics may sit closer to the favourable η.
- Control energy, excluded here, biases toward the SNN — how large is it?
- Do the specialized low-overhead accelerators (LoAS, SpikeX, Bishop) actually reach η≈1?

## Source

- `raw/research/neuromorphic-commercial-viability/07-snn-energy-reconsidered.md` — "Reconsidering the Energy Efficiency of Spiking Neural Networks Inference from Analytical Perspectives", arXiv:2409.08290. Analytical model, cross-checked against Timeloop/Sparseloop; energy constants from 22 nm synthesis. Not silicon measurement.

## Related

- [[snn-energy-hardware-realistic]] — the measured companion; stricter baseline here
- [[../conflicts/snn-energy-payoff]] — Position B evidence
- [[../benchmarks/neurobench]] — standardised measurement that would test these thresholds on real chips
- [[../devices/memristor-array-integration-gap]] — the same data-movement conclusion at the analog boundary
