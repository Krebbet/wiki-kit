# Event cameras (event-based vision sensors)

The sensor half of neuromorphic, and the part with the strongest claim to being commercially real today. Event cameras matter to this wiki for a specific structural reason: **they are what makes a workload natively sparse.** Every finding elsewhere in the wiki says spiking hardware wins only at low event rates on sparse, event-driven data — [[../snn/snn-energy-breakeven-conditions]] puts the threshold near a 5.7% spike rate. An event camera is the front end that produces exactly that kind of data, because it emits nothing when nothing changes.

Instead of sampling every pixel on a clock, each pixel independently reports a brightness change when it crosses a threshold, asynchronously. Data rate becomes a function of scene motion rather than of frame rate.

## Sensor families

- **DVS (Dynamic Vision Sensor)** — silicon-retina-inspired; capacitance-coupled brightness-change detection, resets after each measurement. Smallest pixels, but event-only output: no static-scene image.
- **ATIS (Active Time-Image Sensor)** — dual sub-pixel measuring absolute brightness *and* change. ~2× DVS pixel area; wide dynamic and static range, but the absolute-brightness and event streams can misalign under high-speed motion.
- **DAVIS (Dynamic and Active Vision Sensor)** — shared pixel outputs both absolute brightness and events. ~5% larger pixel than DVS, slower sampling.

Pipeline: CMOS photodiode → readout → logarithmic brightness computation → per-pixel threshold-triggered event circuit → asynchronous output.

## Commercial sensors

Real parts from real vendors — the reason event vision ranks above analog compute-in-memory on the [[../viability-ledger]].

| Supplier | Model | Resolution | Dynamic range | Pixel | Power |
|---|---|---|---|---|---|
| Prophesee | **GENX320** | 320×320 | >120 dB | 6.3 µm | **3 mW** |
| Prophesee | EVK4 HD | 1280×720 | >86 dB | 4.86 µm | typ. 0.5 W |
| Prophesee | EVK5 HD | 1280×720 | >110 dB | 4.86 µm | typ. 0.5 W |
| iniVation | DVXplorer | 640×480 | 90–120 dB | 9.0 µm | max 12 W |
| iniVation | DVXplorer Micro | 640×480 | 110 dB | 9.0 µm | <140 mA @ 5 V |
| iniVation | DAVIS346 | 346×260 | 120 dB | 18.5 µm | typ. 180 mA @ 5 V |
| CelePixel | CeleX-V | 1280×800 | not stated | 9.8 µm | 400 mW |
| Lucid Vision | TRT009S-EC (Sony IMX636) | 1280×720 | 120 dB | 4.86 µm | not stated |

Prophesee's EVK4/EVK5 build on the **Sony IMX636** lineage; GENX320 targets AR/VR headsets, drones and embedded agents. CelePixel's official site is inactive though its repos remain. Lucid prioritises industrial robustness (GigE + PoE) over low power.

**Peak event throughput:** iniVation DVXplorer >1 Mev/s · Sony IMX636 (Prophesee Gen4.1) >10 Mev/s · CelePixel Taurus up to 240 Mev/s.

⚠️ **Power spans 4,000×.** From 3 mW (GENX320) to a maximum 12 W (DVXplorer). Any claim of the form "event cameras use ~0.5 W" is citing one example, not a family property — the survey itself does exactly this, quoting 0.5 W generically while its own table shows the full spread.

## Where the advantage is real

Against conventional frame cameras, as reported by the survey (a **secondary source** propagating vendor and paper figures — it re-measures nothing):

| Property | Event camera | Frame camera |
|---|---|---|
| Temporal resolution | microsecond-level | <30 Hz effective |
| Latency | sub-millisecond | >30 ms (from ~20 ms global exposure) |
| Dynamic range | **140 dB** ⚠️ *or* >120 dB | ~60 dB |
| Data rate | scales with scene motion | fixed (1 MP × 30 fps = 30 M pixels/s) |

⚠️ **The survey contradicts itself on dynamic range** — 140 dB in one passage, >120 dB in another, both attributed generically to event cameras. Not reconciled. The vendor table above is the more trustworthy source.

**Motion-dependent data rate, measured** (DAVIS 346, from drone flight): 298 events/ms in normal flight (2–4 m/s) · 945 events/ms under rapid translation (18–25 m/s) · **1,437 events/ms under rapid rotation** (75–95°/s).

*(synthesis)* That last row is the honest version of the sparsity story. Event output is sparse **when the scene is quiet** and becomes a torrent under aggressive ego-motion — precisely the conditions a drone or vehicle encounters when perception matters most. So "event cameras reduce data 1000×" is a claim about the average case, and the worst case is where the power budget actually has to be sized. The wiki should treat data-reduction claims as workload-conditional, exactly as it treats SNN energy claims.

## The processing gap

The central unresolved tension, and the reason event sensing hasn't yet delivered on neuromorphic compute: **most pipelines convert event streams into dense frames so conventional CNNs can process them — discarding the sparsity that motivated the sensor.**

This is the same failure mode [[../benchmarks/neurobench]] documents at the algorithm level, where its RED-ANN baseline shows 0.634 activation sparsity yielding 87% of dense effective operations because normalization re-densifies them. Sparsity at the input does not survive to sparsity in the compute unless the whole pipeline is built for it.

Accelerator datapoints the survey reports:

- **Speck** (SynSense sensing-and-compute SoC, sensor plus asynchronous event-driven compute): **0.70 mW** at real-time operation. No task or accuracy stated alongside — the figure is uninterpretable on its own, though the magnitude is striking.
- **Reconfigurable CNN SoC** (65 nm): 593.4 nJ per inference. Task unspecified.
- **EventBoost** (Zynq SoC, event-image fusion): +24.33% accuracy over SOTA for drone localization, 30 ms end-to-end.
- **BioDrone** (FPGA): per-frame latency from ~20 ms (CPU) to **2.2 ms**, accuracy within 1–2% of the CPU baseline.

For scale, the survey frames the mobile compute budget: Snapdragon 8Gen3 NPU ~30 TOPS INT8 at 5–7 W · Jetson Orin NX ~100 TOPS at 15–25 W · RTX 4090 >1.3 POPS INT8 at 450 W.

⚠️ Figure 7 of the survey plots power versus latency across ~15 named accelerator works — exactly the comparison this wiki wants — and **it is unrecoverable in this capture** (pymupdf fallback after marker failed under machine load; 7 figure references broken). Same for Figure 6 on denoising cost/performance. Flagged for re-capture on the [[../watchlist]].

## Deployment — the strongest evidence, still vendor-claimed

Prophesee's automotive page names two integrations:

- **Xperi / DTS** — in-cabin driver monitoring, described as a world-first neuromorphic DMS, claiming low-light performance and detection of saccadic eye movement and micro-expressions.
- **Terranet / Mercedes-Benz** — VoxelFlow, for ADAS and autonomous driving perception.

Both are **claimed by the vendor and uncorroborated here** as shipping or in production. Neither is confirmed by an independent source in this wiki.

⚠️ That page carries **zero quantified performance claims of any kind** — every capability (dynamic range, low light, high-speed detection, flickering-LED detection) is a bare heading with no number, no units, no conditions. That is itself the finding: the commercially loudest part of neuromorphic markets on capability language alone.

*(synthesis)* Even so, this is the best deployment evidence the wiki has for anything neuromorphic. Named partners at named automotive OEMs beats a research prototype. It moves the event-vision row on the ledger from "no deployment evidence" to "named design-win claims, vendor-sourced, unverified" — a qualified upgrade, not a flip.

## Stated blockers

Noise (a major research topic in its own right — denoising algorithms are a whole survey section), lack of texture and absolute intensity in event-only sensors, dataset scarcity, benchmark immaturity, tooling gaps, and real-time I/O bottlenecks moving events into compute.

## Open questions

- Are Xperi/DTS or Terranet/Mercedes actually in production, and at what volume?
- Does any deployed pipeline preserve sparsity end to end, or do they all densify to frames?
- What is Speck's 0.70 mW figure measured on — which task, what accuracy?
- Figure 7's power-vs-latency comparison across ~15 accelerators — needs a marker re-capture.
- iniVation and CelePixel are unresearched as companies.

## Source

- `raw/research/neuromorphic-seed-sweep/13-event-camera-survey.md` — "Event Camera Meets Mobile Embodied Perception: Abstraction, Algorithm, Acceleration, Application", arXiv:2503.22943. Survey; secondary. ⚠️ pymupdf capture — figures unavailable, 7 broken refs; the source also contradicts itself on dynamic range and quotes a family-wide power figure its own table refutes.
- `raw/research/neuromorphic-seed-sweep/08-prophesee-automotive.md` — Prophesee Metavision automotive product page. Vendor primary; tier 3, marketing register, no quantified claims.

## Related

- [[../snn/snn-energy-breakeven-conditions]] — why native sparsity is the precondition for any SNN energy win
- [[../benchmarks/neurobench]] — event-camera detection is an algorithm-track task; the RED-ANN sparsity trap
- [[../players/roster]] — Prophesee, iniVation, CelePixel, Sony
- [[../viability-ledger]] — the event-vision row this page upgrades
