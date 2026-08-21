---
setup_approved: 2026-08-19
seeded: false
last_reviewed: 2026-08-20
---

# Watchlist

Persistent radar for this wiki: things identified as worth tracking but not yet captured into a page. Populated by `/weekly-brief` (up to 10 entries per run as surplus beyond the ≤5 captures) or by hand. **Intentionally empty at setup** — do not pre-seed.

**Format:** under each section header, one bullet per item: `- <title> — <≤12-word why / status>`. No URLs, no multi-sentence descriptions. This is a scannable ledger, not a summary.

**Lifecycle:** added by the weekly brief or by the user; promoted to full ingest when ≥2 watchlist entries converge on a theme, when an item becomes load-bearing for one of the four standing questions, or when the user tags it. Captured items get struck through with a `*(captured YYYY-MM-DD)*` note and removed within a few weeks. Retired silently after 90 days without promotion.

**Sections:** created on first use. Expected shapes for this wiki — *Devices & materials*, *Chips & systems*, *Algorithms & toolchains*, *Benchmarks*, *Players & funding*, *Programmes & policy*. The brief adds under the most relevant existing header; if none fits, it creates a new one.

---

## Devices & materials

- Cross-family comparison (PCM / FeFET / MRAM / ECRAM) — no captured source covers it; RRAM-only so far
- Rao et al. 2048-level (11-bit) 256×256 foundry-CMOS memristor array — RTN denoising; cited secondhand only
- STELLAR chip (Zhang et al.), 160k cells monolithic CMOS — cited secondhand; primary not captured
- Nature Materials: high-accuracy memristor analogue computing (s41563-026-02600-y) — ⚠️ paywalled, abstract-only capture
- Adv. Intelligent Systems: memristors for IMC and SNNs (aisy.202500806) — ⚠️ Cloudflare bot-wall, capture failed twice
- TetraMem/UMass hyperdimensional in-memory computing, Nat. Comms. s41467-026-76067-5 — 95.24% accuracy, ~90% resource reduction claimed; ⚠️ abstract-only capture twice (incl. `--js`), no boundary stated, real MX100 hardware kit so worth a retry
- Nanoparticle Networks for Neuromorphic Computing (arXiv:2607.27844) — physical-substrate device, SiO₂-thickness-tuned memory type
- IOP NCE Vol. 6: nanofluidic memristive reservoir computing (Kinavuidi et al., art. 014021) — publication date inside/outside this week's window unconfirmed

## Chips & systems

- ~~Loihi 2 / Hala Point — named repeatedly, never sourced directly~~ *(captured 2026-08-20, [[../chips/loihi2-persistent-monitoring]] — Hala Point itself still unsourced)*
- Innatera Pulsar / T1 current status — only source is ~2 years stale; did Q2-2025 high-volume happen?
- SynSense Xylo Audio 2 — the wiki's best measured result; no vendor-primary source captured
- Analog IMC competitors (EnCharge, Mythic, Rain, Axelera) — in scope, entirely unresearched
- Fault-Tolerant Spike-Time Interface for Approximate Agreement in Distributed Neuromorphic Systems (arXiv:2608.18151) — multi-chip fault tolerance, less-common angle
- EventKitchen stereo event-camera dataset (arXiv:2608.04865) — new benchmark-adjacent dataset, modest novelty

## Algorithms & toolchains

- LoAS, SpikeX, Bishop — specialized sparse-event accelerators; the η≈1 target
- SATA and SpikeSim — open benchmarking harnesses, likely to recur across sources
- NIR (Neuromorphic Intermediate Representation) — gates NeuroBench's closed-algorithm category
- TTFS coding — the one SNN coding scheme that wins most capacity-matched configs
- A²SG: Adaptive Asymmetric Surrogate Gradients (arXiv:2606.11236) — claims ~6× lower training compute overhead vs a leading comparator
- AIGOR modular event-driven SNN inference architecture (arXiv:2607.03191) — compiler/architecture toolchain contribution
- "Time to standardize event-based vision processing" (Nature Sensors, s44460-026-00100-9) — proposed Event-SP standardization framework for event cameras
- IOP NCE Vol. 6: structural plasticity (Jadia et al., art. 014020) — publication date inside/outside this week's window unconfirmed

## Players & funding

- BrainChip September 2026 quarterly — next yield and volume checkpoint
- TSMC 22 nm eRRAM — the only foundry-node claim in evidence; no independent benchmark

## Programmes & policy

- Lava (Intel) successor SDK — still unannounced as of 2026-08-20; re-checked this run, no change from the `retired` status in [[reference-sources]]

## Related

- [[reference-sources]] — where the radar's inputs come from
- [[index]] — wiki-wide page catalog
