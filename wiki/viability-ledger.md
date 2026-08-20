# Commercial viability ledger

*(synthesis throughout — this page is the wiki's own reading of the sourced evidence, not a claim any single source makes.)*

Standing question #3: **when do neuromorphic materials become commercially viable, and for what?** This page tracks a falsifiable answer per technology and per application, with the specific blocker gating each date and the leading indicator that would move it.

Built from 8 sources in one research run (2026-08-20). It is thin by construction — a row exists only where captured evidence supports it, and every date carries an owner. **No row here is a forecast.** Where the honest answer is "nobody has shown this end to end," the row says so.

## Ladder

`paper` → `single device` → `small array` → `full crossbar / integrated chip` → `foundry tape-out` → `sampling` → `production shipments` → `volume, yield-mature` → `commodity`

## Per-technology status

| Technology | Rung reached | Best evidence | Gating blocker | Would move the date |
|---|---|---|---|---|
| **Digital event-based neuromorphic** (BrainChip Akida) | **production shipments** | AKD1500 shipping from GlobalFoundries 22FDX to multiple customers, defence + wearables, 2026-06-30 | Yield below expectations (**unquantified**); environmental qualification incomplete; ~US$1.9M trailing revenue vs ~US$5.3M/qtr outflow | A quantified yield figure; qualification pass; a measured efficiency number at a stated boundary |
| **Digital neuromorphic research platforms** (Loihi 2, Xylo) | **sampling / in-research-use** | Both measured as NeuroBench system-track baselines with disclosed power boundaries | Not a commercial-availability question; these are research/eval parts | Multi-vendor head-to-head submissions |
| **Oxide RRAM as embedded NVM** | **foundry product** | TSMC 40 nm RRAM platform (2019); 2nd-gen 22 nm eRRAM (2024), claimed to rival embedded STT-MRAM | — (this is shipping) | Independent benchmark vs STT-MRAM |
| **Oxide RRAM as analog compute-in-memory** | **integrated chip (lab)** | STELLAR: 160,000 cells monolithically integrated with CMOS, 35× vs digital accelerators on named tasks | ADC/DAC >70% of system power; array yield 89–100% and material-dependent; largest tabled array 128×64 | An announced foundry PDK for analog CIM; a peripheral-inclusive TOPS/W figure |
| **RRAM via non-foundry BEOL insertion** | **small array, electrically validated** | 16×16 1T1R on 180 nm/200 mm foundry CMOS; 10–100 kΩ post-forming window | No yield, endurance, retention or variability data at all; 1 Mbit array shown **structurally only**; pseudo-via must become damascene before volume | Electrical characterisation of the 1 Mbit array |
| **2D-material memristors** | **small-to-medium array (lab)** | up to 64×64 h-BN arrays; early 3D monolithic stacking demos | **BEOL/FEOL thermal-budget mismatch** — FEOL needs 900–1200 °C, 2D materials decompose above 400–800 °C, BEOL caps below ~400 °C. Physical, not merely engineering-hard | A low-temperature route at scale (one exists: MBE-grown HfSe₂ transferred at ≤150 °C) |
| **Ferroelectric memristors** | **single device / mechanism** | Covered only in review outlook | Film uniformity sensitive to thickness and grain size; annealing poorly BEOL-compatible | Any array-level data |
| **Phase-change memristors** | **single device / mechanism** | Covered only in review outlook | Thermal crosstalk between adjacent cells; switching power. Both worsen with density | Any array-level data |
| **MRAM / ECRAM** | **not covered** | — | — | ECRAM is not mentioned in any captured source. Gap on the [[watchlist]] |

## Per-application status

| Application | Status | Evidence |
|---|---|---|
| **Always-on audio / keyword sensing** | **Working, measured, deployed-adjacent** — the strongest case in the wiki | Xylo Audio 2 vs Arduino at matched accuracy: 60.9× less dynamic power, 33.4× less dynamic energy, boundary disclosed. Latency cost admitted (84 ms vs 45 ms) |
| **Defence / wearables edge inference** | **Shipping, unmeasured** | AKD1500 production shipments; no performance figure at a stated boundary |
| **Event-vision / automotive** | **Datasets and models exist; no deployment evidence** | Prophesee 1MP automotive dataset is a NeuroBench algorithm-track task |
| **Combinatorial optimization (QUBO)** | **Regime-dependent win** | Loihi 2: 37.24× less power than best CPU solver; solves 4× larger workloads at ≤10⁻² s. **But CPU/TABU wins on solution quality at ≥10 s** |
| **Large-scale CV and language** | **Losing** | Capacity-matched: RepVGG/ImageNet 2.232× worse; spiking Llama-2 7B at T=15 **3.793× worse**. Transformers degrade as `T/⌈log₂(T+1)⌉` |
| **Analog CIM as a GPU/NPU replacement** | **Not demonstrated end to end** | No peripheral-inclusive system figure exists in any captured source |

## The three real gates

*(synthesis)* Across every source, the same three constraints recur:

1. **Data movement, not arithmetic.** Three independent routes converge: measured simulation (repeated per-timestep movement is the largest bottleneck), analytical modelling (the 5.7% breakeven shifts across 3.41%–10.80% on data-movement cost alone, while MAC/ACC energy moves it ≤0.05 pp), and the analog device literature (ADC/DAC >70% of system power). **Neuromorphic's efficiency problem is an interconnect and conversion problem.** The strongest single datapoint: dropping sparse-event overhead η from 12 to 1 flips an SNN from winning 1-of-12 configurations to 12-of-12.
2. **Yield and variability, not device physics.** Champion device numbers are excellent (10¹² cycles endurance, 11-bit conductance resolution). Array yields run 89–100% and are material- and process-dependent; the largest tabled array is 8,192 cells. BrainChip's yield shortfall on a *mature 22 nm digital* node is the sharpest illustration — this is not exotic-materials risk, it is manufacturing.
3. **Measurement credibility.** As of 2026-08-20 **no vendor in this wiki has published an efficiency number at a stated measurement boundary against a named baseline.** [[benchmarks/neurobench]] defines the protocol and the vendors co-author it; nobody has submitted. Until that changes, every roadmap date rests on unaudited claims. See [[conflicts/snn-energy-payoff]].

## Honest bottom line

**For always-on, natively-sparse, ultra-low-power sensing: viable now.** The Xylo result is real, measured, and boundary-disclosed, and AKD1500 is shipping into defence and wearables. This is a niche, and it is a genuine one.

**For anything resembling general edge inference: not demonstrated, and the trend is unfavourable.** Under capacity-matched comparison the SNN loses on most realistic CV workloads and loses badly on transformers.

**For analog compute-in-memory as a mainstream accelerator: no credible near-term date.** Oxide RRAM ships as embedded NVM today — a genuinely different product from analog CIM, and conflating the two is the most likely way to overstate progress. Analog CIM tops out at chip-scale lab demonstrations, gated on peripheral energy overhead with no announced foundry PDK.

**The date is not the useful question.** No source here supports one. The useful question is whether the specific gates move — and each has a named leading indicator in the table above.

## Leading indicators to watch

1. A NeuroBench **system-track submission** from any vendor currently making unquantified claims.
2. A **quantified AKD1500 yield figure** — September 2026 quarterly is the next checkpoint.
3. An announced **foundry PDK for analog CIM RRAM**, as distinct from embedded NVM.
4. **Electrical characterisation** of a ≥1 Mbit integrated RRAM array.
5. A specialized sparse-event accelerator (LoAS, SpikeX, Bishop) demonstrating **η ≈ 1** in silicon.
6. Whether **Innatera hit its Q2-2025 high-volume milestone** — a dated, resolvable roadmap claim.

## Source

Synthesised from all eight sources in `raw/research/neuromorphic-commercial-viability/`. Each row traces to the page cited beside it; no claim here originates on this page.

## Related

- [[players/roster]] · [[players/brainchip]] — who
- [[devices/memristor-array-integration-gap]] · [[devices/memristor-device-engineering]] · [[devices/cmos-rram-beol-integration]] — what gates the materials
- [[snn/snn-energy-breakeven-conditions]] · [[snn/snn-energy-hardware-realistic]] — what gates the algorithms
- [[benchmarks/neurobench]] — what would make any of this checkable
- [[conflicts/snn-energy-payoff]] — the open dispute underneath every row
