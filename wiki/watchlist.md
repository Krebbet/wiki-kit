---
setup_approved: 2026-08-19
seeded: false
last_reviewed: 2026-09-17
---

# Watchlist

Persistent radar for this wiki: things identified as worth tracking but not yet captured into a page. Populated by `/weekly-brief` (up to 10 entries per run as surplus beyond the ≤5 captures) or by hand. **Intentionally empty at setup** — do not pre-seed.

**Format:** under each section header, one bullet per item: `- <title> — <≤12-word why / status>`. No URLs, no multi-sentence descriptions. This is a scannable ledger, not a summary.

**Lifecycle:** added by the weekly brief or by the user; promoted to full ingest when ≥2 watchlist entries converge on a theme, when an item becomes load-bearing for one of the four standing questions, or when the user tags it. Captured items get struck through with a `*(captured YYYY-MM-DD)*` note and removed within a few weeks. Retired silently after 90 days without promotion.

**Sections:** created on first use. Expected shapes for this wiki — *Devices & materials*, *Chips & systems*, *Algorithms & toolchains*, *Benchmarks*, *Players & funding*, *Programmes & policy*. The brief adds under the most relevant existing header; if none fits, it creates a new one.

---

## Devices & materials

- Noh et al. ECRAM Tiki-Taka (Sci. Adv. eadl3350) — ⚠️ science.org hangs; the wiki's only ECRAM primary
- Tiki-Taka retention-aware zero-shifting — same paper, same access problem
- Li et al. in-situ defect-tolerance training — **read this to settle [[conflicts/analog-onchip-training-viability]]**
- A fabricated CurFe/ChgFe FeFET array with endurance and retention data
- Event-camera survey Fig. 6 & 7 (power-vs-latency across ~15 accelerators) — lost to pymupdf; needs marker re-capture

- Cross-family comparison (PCM / FeFET / MRAM / ECRAM) — no captured source covers it; RRAM-only so far
- Rao et al. 2048-level (11-bit) 256×256 foundry-CMOS memristor array — RTN denoising; cited secondhand only
- STELLAR chip (Zhang et al.), 160k cells monolithic CMOS — cited secondhand; primary not captured
- Nature Materials: high-accuracy memristor analogue computing (s41563-026-02600-y) — ⚠️ paywalled, abstract-only capture
- Adv. Intelligent Systems: memristors for IMC and SNNs (aisy.202500806) — ⚠️ Cloudflare bot-wall, capture failed twice
- TetraMem/UMass hyperdimensional in-memory computing, Nat. Comms. s41467-026-76067-5 — 95.24% accuracy, ~90% resource reduction claimed; ⚠️ abstract-only capture twice (incl. `--js`), no boundary stated, real MX100 hardware kit so worth a retry
- Nanoparticle Networks for Neuromorphic Computing (arXiv:2607.27844) — physical-substrate device, SiO₂-thickness-tuned memory type
- IOP NCE Vol. 6: nanofluidic memristive reservoir computing (Kinavuidi et al., art. 014021) — publication date inside/outside this week's window unconfirmed
- Mott/CDW device family (1T-TaS2) — in-scope, uncaptured; anchor on device-level oscillator work (Liu/Balandin/Khitun), not the atomic-scale characterization-only source that surfaced it
- KAIST noise-tunable memristor "probabilistic neuron" — noise-as-resource vs noise-as-defect framing is interesting, but source is a two-sentence relay with zero numbers, no primary access (Wiley-blocked)
- Nb:SrTiO3 resistive switching mechanism study (arXiv:2608.23430) — new oxide/interface family, mechanism-focused not breakthrough-numbers
- Half-unit-cell (6Å) 2D Ga2O3 ferroelectricity, 0.8V switching, BEOL-compatible on Si (Nature Electronics, doi 10.1038/s41928-026-01694-1) — ⚠️ paywalled, abstract-only capture per structural check; strong scope-fit (CMOS-voltage-scale, BEOL-integrated) if the body can ever be obtained
- RACE-AIMC: risk-aware ensemble inference across heterogeneous analog IMC accelerators (arXiv:2609.03149) — statistical framework for device-to-device variability, not a measured chip; touches the [[../devices/memristor-array-integration-gap]] theme
- Nature Electronics News & Views on a room-temperature correlated-microwave-signal thin-film magnetic source — low confidence on neuromorphic relevance from abstract alone; needs the underlying paper's title/abstract to judge oscillator/coupled-oscillator-computing fit

## Chips & systems

- IBM NorthPole *Science* paper (doi 10.1126/science.adh1174) — ⚠️ science.org hangs; primary for the 25× claim
- NorthPole IEEE HPEC 2024 paper (modha.org) — likely names the unnamed GPU baselines
- Intel's replacement SDK + next-generation Loihi — announced, undated, unshipped
- TianjicX (Science Robotics, scirobotics.abk2948) — ⚠️ science.org hangs
- Lynxi — commercialising the Tianjic lineage; entirely unresearched
- iniVation, CelePixel, Sony IMX636 — event-sensor vendors, unresearched

- ~~Loihi 2 / Hala Point — named repeatedly, never sourced directly~~ *(captured 2026-08-20, [[chips/loihi2-persistent-monitoring]] — Hala Point itself still unsourced)*
- Innatera Pulsar / T1 current status — only source is ~2 years stale; did Q2-2025 high-volume happen?
- SynSense Xylo Audio 2 — the wiki's best measured result; no vendor-primary source captured
- Analog IMC competitors (EnCharge, Mythic, Rain, Axelera) — in scope, entirely unresearched
- Fault-Tolerant Spike-Time Interface for Approximate Agreement in Distributed Neuromorphic Systems (arXiv:2608.18151) — multi-chip fault tolerance, less-common angle
- EventKitchen stereo event-camera dataset (arXiv:2608.04865) — new benchmark-adjacent dataset, modest novelty

## Algorithms & toolchains

- Systematic surrogate-gradient function comparison — the 2019 "doesn't much matter" claim is still uncontrolled
- **SNN training energy vs ANN training energy** — no source in this wiki addresses it
- Any network trained on a *fabricated* analog array rather than simulation calibrated to one
- MatMul-free / attention-free architectures on neuromorphic substrates — the one measured win
- DCLL-family local learning rules beyond DVS-Gestures scale

- LoAS, SpikeX, Bishop — specialized sparse-event accelerators; the η≈1 target
- SATA and SpikeSim — open benchmarking harnesses, likely to recur across sources
- NIR (Neuromorphic Intermediate Representation) — gates NeuroBench's closed-algorithm category
- TTFS coding — the one SNN coding scheme that wins most capacity-matched configs
- A²SG: Adaptive Asymmetric Surrogate Gradients (arXiv:2606.11236) — claims ~6× lower training compute overhead vs a leading comparator
- AIGOR modular event-driven SNN inference architecture (arXiv:2607.03191) — compiler/architecture toolchain contribution
- "Time to standardize event-based vision processing" (Nature Sensors, s44460-026-00100-9) — proposed Event-SP standardization framework for event cameras
- IOP NCE Vol. 6: structural plasticity (Jadia et al., art. 014020) — publication date inside/outside this week's window unconfirmed
- Syn2Logic: end-to-end neuromorphic design automation (arXiv:2608.25536) — compiler/toolchain, unverified vs a real chip
- NeuRehab: RL+SNN rehab automation framework (IOP NCE, art. ae9215) — claims deployment on dedicated low-power hardware, measured-vs-simulated unverified
- Free-probability kernels for zero-rollout reservoir-computing hyperparameter selection (arXiv:2608.20998) — RC toolchain maturity angle
- Gradient-tunneling STDP-compatible feedback learning for neural microcircuits (arXiv:2609.08070, submitted Nature Machine Intelligence) — on-chip/local-learning weight-transport angle, simulation-only, comparable-not-breakthrough vs leading SNN online methods
- NMTK (NeuroMorphicToolKit) v0.6.5 — single-maintainer first public release claiming near-universal SNN-framework interop (snnTorch/Brian2/Lava/Nengo/Rockpool/PyNN/Akida via NIR); ⚠️ treat as unverified until independent adoption is seen, not an established toolchain like snnTorch/Rockpool/Nengo

## Benchmarks

- ANTShapes: event-based neuromorphic object classification benchmark dataset (arXiv:2608.27150) — new dataset, modest novelty, NeuroBench-adjacent

## Players & funding

- BrainChip Q2 FY2026 investor webinar (11 Sept 2026) held — AKD2500 Dec-2026 tape-out on schedule, Akida 1500 25% inventory sold, ~$20M cash runway, yield issues still under investigation; ⚠️ every capture attempt (investing.com ×2) hit a 403 — only secondary-relay content available, no clean primary this run; next quarterly (Sept 2026) is still the yield/volume checkpoint
- TSMC 22 nm eRRAM — the only foundry-node claim in evidence; no independent benchmark
- dorsaVi 22nm RRAM-CMOS validation chip fab start — ⚠️ single small-cap-stock-tipster source (smallcaps.com.au), unverified against any primary; dorsaVi's known business is biomechanical sensors, not chips — treat as unconfirmed until a second source corroborates

## Programmes & policy

- Lava (Intel) successor SDK — still unannounced as of 2026-08-20; re-checked this run, no change from the `retired` status in [[reference-sources]]

## Related

- [[reference-sources]] — where the radar's inputs come from
- [[index]] — wiki-wide page catalog
