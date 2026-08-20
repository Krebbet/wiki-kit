# NeuroBench

The field's attempt at an honest measuring stick, and this wiki's **canonical citation for how a neuromorphic energy number must be measured**. ~60 authors across ~40 institutions — Harvard, Intel Labs, SynSense, imec, TU Delft, Innatera, Prophesee, SpiNNcloud, Sony, NIST, Sandia and others — explicitly modelled on MLPerf. arXiv:2304.04640, published *Nature Communications* 2025-02-11.

Its stated diagnosis: the field "currently lacks standardized benchmarks, making it difficult to accurately measure technological advancements, compare performance with conventional methods, and identify promising future research directions," and prior attempts "have not seen widespread adoption due to a lack of inclusive, actionable, and iterative benchmark design."

## The boundary definition — use this

The single most load-bearing thing in the paper, and the rule this wiki adopts:

> **Algorithm-track complexity metrics are not energy numbers.** The paper states outright that footprint, sparsity and synaptic operations "are measured independently of the underlying hardware and therefore **do not explicitly correlate with post-deployment latency or energy consumption**."

Only the **system track** constitutes an efficiency measurement, and it defines the boundary precisely:

- **Idle power** — configured and ready, not sleeping
- **Active power** — running pre-processing or inference
- **Dynamic power** = Active − Idle
- **Dynamic energy** = Dynamic power × execution time
- **Data pre- and post-processing time and power must be included**, and reported separately from inference — an explicit contrast with "conventional system benchmarks whose measurements start from pre-processed data"

Measurement is **task-level** (the whole system under test), not kernel-level.

**Rule for this wiki:** any page citing a SynOps count or a sparsity fraction as though it were an energy result is misusing this framework by its own terms. Flag that pattern on sight during ingest. It is exactly the error [[../snn/snn-energy-hardware-realistic]] catches six algorithm papers making.

## Two tracks

**Algorithm track** (hardware-independent, v1.0, four tasks): Keyword few-shot class-incremental learning on the MSWC multilingual corpus; event-camera object detection on the Prophesee 1-megapixel automotive dataset; non-human-primate motor prediction from primate motor-cortex recordings; and chaotic function prediction on Mackey-Glass. Metrics: footprint (bytes), connection sparsity, activation sparsity, synaptic operations split into Dense / Eff_MACs / Eff_ACs, and a user-reported model execution rate.

**System track** (hardware-dependent, v1.0, two tasks): Acoustic Scene Classification and QUBO/Maximum Independent Set. Three metric categories — Correctness (**no threshold imposed**), Timing (MLPerf offline/single-stream/server scenarios), and Efficiency, which is **first-order here** rather than a secondary adjacent track as in MLPerf Power or Green500.

## Baseline results

**Acoustic Scene Classification** (DCASE 2020 subset, 4 classes, 1 s samples):

| System | Accuracy | Inference | Dynamic power | Dynamic energy |
|---|---|---|---|---|
| Arduino Nano 33 BLE (Cortex-M4F @ 64 MHz) | 79.64% | 45 ms | 20.75 mW | 0.934 mJ/inf |
| **SynSense Xylo Audio 2** | 79.90% | 84 ms | **0.341 mW** | **0.028 mJ/inf** |

**60.9× less dynamic inference power, 33.4× less dynamic inference energy at comparable accuracy** — and note the Xylo is *slower* (84 ms vs 45 ms). Xylo's analog front-end pre-processing was measured separately: 0.00017 mW idle, 0.015 mW active.

This is the wiki's best example of an efficiency claim done properly: named parts, matched accuracy, stated boundary, pre-processing disclosed separately, and the latency cost admitted.

**QUBO / Maximum Independent Set:** Intel Loihi 2 (one chip on a Kapoho Point board, Lava 0.8.0) vs an Intel Core i9-7920X running SA/Tabu D-Wave samplers, measured with Intel SoC Watch. **37.24× less power** than the best CPU solver. At ≤10⁻² s timeout Loihi 2 solves workloads 4× larger than the CPU. **But at ≥10 s timeout, the CPU running TABU achieves the best solution quality.** The paper claims a regime-dependent win, not a universal one.

**The sparsity trap, from their own baselines:** the RED ANN on event-camera detection has **0.634 activation sparsity but 87% of dense effective ops** — not the ~35% sparsity alone would imply. Batch normalization *before* weight multiplication densifies effective operations. The paper presents this as a caution that synaptic operations "must be considered in tandem" with sparsity, never sparsity alone. It applies to ANNs and SNNs equally.

Elsewhere in the algorithm track the sparsity story is better: the NHP motor-prediction SNN reaches 0.997–0.999 activation sparsity, giving 276–551 Eff_ACs against the ANN's 3836–6103 Eff_MACs at comparable R² (~0.57 vs ~0.59). And a cautionary counter-case: the keyword-FSCIL RSNN runs at 200 Hz over a 200-step sample, so its aggregate 7.30×10⁷ Eff_ACs **exceed** the ANN's per-execution ops despite higher sparsity.

## Methodological fixes it claims

1. **Fairer baselines.** Prior neuromorphic audio benchmarking (Blouw et al., NICE'19) compared against a *server-class* CPU; NeuroBench compares against an Arduino embedded microprocessor — matching the device's actual competitive tier instead of an oversized strawman.
2. **Sparsity ≠ efficiency**, demonstrated with the RED-ANN case above.
3. **Algorithm-track numbers declared non-comparable to real energy** — targeting the common practice of citing SynOps or sparsity as if they were energy claims.
4. **Unconstrained algorithm choice with mandatory correctness reporting.** Unlike MLPerf Inference's closed category (same trained model across all systems), submissions may use any algorithm — because "the tight coupling between an algorithm and its system implementation in many existing neuromorphic hardware solutions" makes closed-category comparison unworkable today. That is a candid admission that neuromorphic systems are not yet interchangeable enough for MLPerf's gold-standard method.
5. **Mandatory transparency reports and audits** for official system-track submissions, because "platform diversity poses difficult challenges for completely consistent hardware measurement methodologies." The paper concedes it cannot yet *force* measurement consistency — only disclosure.

## Stated limitations

Unusually forthright, and directly relevant to what this wiki tracks:

- **Analog and continuous-time execution is undefined.** Algorithm-track metrics assume digital, time-stepped execution. As of v1.0 the hardware-independent track **cannot fairly score genuinely analog neuromorphic approaches** — a real gap given that analog in-memory compute is squarely in this wiki's scope. Only the system track captures analog hardware, and only at whole-system power level.
- **Neuron-update cost is excluded** from the synaptic-operations metric — leak, reset and adaptation dynamics are not counted, only synapse-level MAC/AC. This is exactly the cost [[../snn/snn-energy-hardware-realistic]] measures at up to 61.6% of computation-unit power.
- **Model execution rate "is currently not well-defined for models operating under event-based or continuous-time contexts"** — awkward for a neuromorphic benchmark.
- Pre/post-processing cost is not captured in algorithm-track metrics at all.
- No correctness threshold on system-track submissions; a closed-algorithm category awaits NIR (Neuromorphic Intermediate Representation) maturing.
- v1.0 task suite is narrow. IMU sensing and closed-loop/embodied sensorimotor tasks are named as future work, not built.

## Is it credible as a referee?

*(synthesis)* The governance is genuinely broad — ~40 institutions, national labs, and direct vendor participation from Intel, SynSense, Innatera, Prophesee, SpiNNcloud and Sony. The harness is open source, the datasets are pinned, submissions require structured reports and face audits. That is real infrastructure, not a paper.

The caveat is structural and worth stating plainly: **the only two system-track baselines each come from a participating vendor's own hardware** — Xylo from SynSense, Loihi 2 from Intel. Vendor participation is evidence of buy-in, but it also means there is not yet a multi-vendor head-to-head, and no third party has independently measured anyone. Until a vendor submits against a *competitor's* device on the same task, the referee has convened but has not yet officiated a match.

So: credible framework, correct boundary discipline, insufficient submissions. The measurement to watch for is a **NeuroBench system-track submission from BrainChip, Innatera, or another vendor whose public claims are currently unquantified** — that is the specific event that would settle [[../conflicts/snn-energy-payoff]].

## Reproducibility

Harness open-source: `github.com/NeuroBench/neurobench` (algorithm track) and `github.com/NeuroBench/system_benchmarks` (system track). PyTorch-based, extensible to snnTorch and SpikingJelly, with stated future extension to Lava and Fugu. Datasets pinned with download scripts (MSWC 630 MB subset vs the 124 GB full corpus; NHP Primate Reaching via Zenodo DOI; Mackey-Glass series pre-computed for run-to-run reproducibility despite floating-point sensitivity). QUBO best-known-solution targets computed via D-Wave Tabu up to 5000 nodes, with a call for community PRs beyond. Leaderboard at `neurobench.ai`, described as under active development. No software licence was stated in the captured content.

## Source

- `raw/research/neuromorphic-commercial-viability/05-neurobench.md` — "NeuroBench: A Framework for Benchmarking Neuromorphic Computing Algorithms and Systems", arXiv:2304.04640 → *Nature Communications*, 2025-02-11. Tier 2 (community benchmark, open harness, peer-reviewed).

## Related

- [[../conflicts/snn-energy-payoff]] — NeuroBench's system track is the named resolution condition
- [[../snn/snn-energy-hardware-realistic]] — the estimation error NeuroBench's boundary rules forbid
- [[../snn/snn-energy-breakeven-conditions]] — thresholds a system-track submission could test on silicon
- [[../players/brainchip]] — a vendor whose claims a submission would settle
- [[../players/roster]] — Intel, SynSense, Innatera, Prophesee, SpiNNcloud, Sony as participants
