# SpikeDuet: CPU plus matrix accelerator for sparse SNNs on a commodity MCU

Bhatti and Siddiqi (LUMS / TU Delft) deploy small trained SNNs (snnTorch LIF, inference only) on a Silicon Labs EFR32MG24 microcontroller, splitting each affine layer between the Cortex-M33 CPU (event-driven, skips silent inputs) and the on-chip Matrix Vector Processor (MVP, a dense FP16 accelerator). **Measured on the physical chip**, the heterogeneous build is 1.27-1.87x faster and uses 11-34% less energy per inference than an optimized sparse-CPU baseline on five of six networks; the smallest stays CPU-optimal. The wiki-relevant point: the speedup comes from conventional compiler and scheduling tricks on off-the-shelf silicon with no neuromorphic hardware involved, which bears on [[../conflicts/snn-energy-payoff]].

## Mechanism

- **Engine selection per layer.** A planner picks sparse-M33, dense-MVP, or "range-sparse" MVP (groups adjacent active columns into contiguous ranges, bridging gaps when cheaper than a new launch) using spike-activity profiles, hardware-calibrated cycle models and the 256 KiB SRAM budget. Sparse-M33 cost is about 2.5 cycles per active input per output neuron with SRAM-resident weights, roughly double from Flash.
- **Function-preserving neuron reordering.** Permuting hidden neurons (and inversely permuting the next layer) leaves the function unchanged but puts co-active neurons adjacent, so the MVP needs fewer launches. No retraining; spike activity and M33 work are unchanged. Orders come from training-split co-activity (hierarchical clustering plus local swaps).
- **Asynchronous scheduling.** MVP affine work for timestep t overlaps M33 LIF updates from earlier timesteps; outputs are unchanged.

## Evidenced (measured on EFR32MG24, 39 MHz, inference only)

Latency from the Cortex-M33 DWT cycle counter; energy = measured supply current at 3.3 V times latency. Baseline = optimized sparse Cortex-M33 (FP32, hot columns pinned in SRAM where weights sit in Flash). Test sets are small: 40 SHD, 70 per SSC network, 108 per Braille network inputs.

| Network | M33 sparse (ms) | Dense MVP (ms) | Best heterogeneous (ms) | Speedup | Energy M33 / hetero (mJ) |
|---|---|---|---|---|---|
| SHD 700-64-20 | 48.75 | 83.93 | 37.98 | 1.28x | 0.37 / 0.31 (-16%) |
| SSC-64 | 59.28 | 100.56 | 46.67 | 1.27x | 0.44 / 0.39 (-11%) |
| SSC-128 | 131.85 | 190.79 | 84.11 | 1.57x | 0.97 / 0.74 (-23%) |
| SSC-192 | 209.40 | 390.47 | 112.07 | 1.87x | 1.53 / 1.01 (-34%) |
| Braille-192 | 31.26 | 55.64 | none (CPU stays optimal) | 1.00x | 0.24 (0%) |
| Braille-384 | 89.93 | 208.53 | 66.14 | 1.36x | 0.64 / 0.56 (-13%) |

- **Dense MVP loses everywhere:** 1.4-2.3x slower than sparse M33. Sparsity exploitation on the CPU is the baseline to beat, not dense execution.
- **Locality flips the preferred engine.** Braille-384 Linear1: sparse M33 36,101 cycles/timestep; MVP in trained order 41,916 (1.16x worse); after reordering 31,123 (0.86x). Reordering cut mean launches per timestep from 10.1 to 5.8. Reordering alone gave 14.7% lower blocking latency (97.01 to 82.78 ms) and 22.4% lower asynchronous latency (85.19 to 66.14 ms).
- **Counterexample:** Braille-192 reordering cut ranges per timestep from 3.49 to 2.19 but the MVP still cost 7,383 cycles vs 5,604 on M33 (1.32x). Locality is necessary, not sufficient.
- **SSC width scaling.** First-hidden-layer spike density falls 12.2%, 8.8%, 7.1% for widths 64, 128, 192 (width also changes learned activity and accuracy, so the paper calls this corroboration, not an isolated experiment). Measured post-reorder Linear1 MVP-to-M33 cycle ratio: 1.02 at width 128, 0.83 at 192. Models predicted per-engine costs within 6% and end-to-end latency within 4.1% (SSC-128) and 1.7% (SSC-192).
- **Correctness.** Zero bitwise mismatches of sparse kernels vs dense recomputation (4,000 SHD and 7,000 SSC-64 timesteps). Emulated FP16/FP32 accuracy shift vs FP32 reference: -0.49, -0.05, +0.15, +0.05, -0.12 percentage points (SHD, SSC-64/128/192, Braille-384).
- Best configuration is not always the reordered one: under async scheduling SSC-128/192 keep the trained order with only Linear0 on the MVP, because leaving Linear1 on the M33 lets it overlap.

## Claimed / stated limits

- Authors claim the first automated snnTorch-to-C flow targeting a CPU plus on-chip dense accelerator; I did not check this against prior art.
- Energy boundary: supply current at 3.3 V times latency on one MCU. What else shares that rail (radio, regulator losses, idle between inferences) is **(boundary unstated)**. Sample sizes per network are tens to ~100 inputs; no error bars are reported on latency or energy.
- Single chip family; "future work will extend to other accelerator-equipped MCUs." No comparison against a dense quantized ANN or a TinyML (TFLite Micro / MCUNet) build of the same task, so this says nothing about whether the SNN is the right model on this part. No comparison against neuromorphic silicon.
- Disclosed: Claude was used for grammar and text refinement. Code released at github.com/chaselab-lums/spikeduet.

## Bearing on snn-energy-payoff

*(synthesis)* This is **Position B-adjacent evidence, with a twist.** It does not test the energy-payoff claim directly (no ANN baseline, no neuromorphic comparison), but it shows that the sparse-event benefit is capturable on commodity silicon via software: the sparse-CPU baseline already exploits spikes, and the extra 11-34% comes from an accelerator the SNN was not designed for. That undermines the premise that SNNs *need* neuromorphic silicon to realise sparsity gains at the tens-of-kilohertz-to-mJ MCU tier. Caveats cut the other way: the gains are modest, fragile (the smallest network gets nothing, and the winning engine depends on activity locality, memory placement and concurrency), and the absolute workloads are tiny. It also echoes the conflict page's point that sparsity pays inside the compute path but is eroded by data movement, since the MVP's launch overhead (about 454 cycles per launch, 88 per column pair on the 64-output layer) is exactly a sparse-fragmentation cost. It leaves unresolved whether a purpose-built part such as the Xylo result in [[../benchmarks/neurobench]] beats this tier at matched accuracy.

## Source

- `raw/research/weekly-2026-10-22/03-spikeduet.md` - arXiv 2610.24677, Bhatti and Siddiqi.

## Related

- [[../weekly-briefs/2026-10-22]] — brought in by the 2026-10-22 weekly sweep
- [[../conflicts/snn-energy-payoff]] — bears on whether SNN sparsity needs neuromorphic silicon
- [[snn-energy-breakeven-conditions]] — capacity-matched comparison this paper does not run
- [[snn-energy-hardware-realistic]] — why operation-count estimates overstate; here energy is measured
- [[../benchmarks/neurobench]] — the protocol and Xylo baseline this MCU tier should be compared against
- [[../chips/loihi2-persistent-monitoring]] — another measured edge result with a boundary caveat
- [[../viability-ledger]] — commodity-MCU deployment as a competing socket
