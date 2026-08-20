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

## Chips & systems

- Innatera Pulsar / T1 current status — only source is ~2 years stale; did Q2-2025 high-volume happen?
- Loihi 2 / Hala Point — named repeatedly, never sourced directly
- SynSense Xylo Audio 2 — the wiki's best measured result; no vendor-primary source captured
- Analog IMC competitors (EnCharge, Mythic, Rain, Axelera) — in scope, entirely unresearched

## Algorithms & toolchains

- LoAS, SpikeX, Bishop — specialized sparse-event accelerators; the η≈1 target
- SATA and SpikeSim — open benchmarking harnesses, likely to recur across sources
- NIR (Neuromorphic Intermediate Representation) — gates NeuroBench's closed-algorithm category
- TTFS coding — the one SNN coding scheme that wins most capacity-matched configs

## Players & funding

- BrainChip September 2026 quarterly — next yield and volume checkpoint
- TSMC 22 nm eRRAM — the only foundry-node claim in evidence; no independent benchmark

## Related

- [[reference-sources]] — where the radar's inputs come from
- [[index]] — wiki-wide page catalog
