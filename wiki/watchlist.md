---
setup_approved: true
# Approved 2026-05-17 by the user after reviewing this file + reference-sources.md.
maintained_by: weekly-brief
scope: ai-drone consumer
---

# Watchlist

The wiki's radar. `/weekly-brief` reads/extends this; the email's "Other watchlist references" section is grouped by the `##` headers below. Keep entries to one line; cap 10 additions per run. Seeded 2026-05-17 from the four research threads ingested to date.

## Open conflicts / decisions to track

- LiDAR-vs-vision autonomy — OPEN conflict ([[lidar-vs-vision-autonomy]]); watch for a head-to-head high-speed outdoor avoidance benchmark or solid-state-LiDAR unit-economics data that would resolve it.
- Non-cooperative detect-and-avoid standard — watch ASTM F38 / RTCA / FAA for a consensus performance MOPS; gates urban autonomous BVLOS.

## Autonomy & perception

- Event-camera drone SOTA — track ETH RPG / TU Delft for new agile-flight, low-light, or onboard-only results.
- VIO/SLAM without LiDAR or GNSS — outdoor, fully-onboard results that strengthen the vision camp.
- Learned depth / monocular perception on UAVs — the standing gap behind most "needs mocap" demos.

## Onboard compute & energy

- Neuromorphic drone control — maturity watch (Loihi/Speck/Kraken); flag any full sensor-to-actuator onboard loop or outdoor result.
- Memristor / in-memory edge AI — long-horizon; flag only a credible drone-deployable demonstration (currently TRL ~2–3).
- Ultra-low-power SoC lineage (PULP/GAP) — new generation or a modern DNN-inference power decomposition for a *mid-size* consumer drone (current gap).

## Physical interaction & manipulation

- Onboard (mocap-free) aerial grasping/manipulation — the binding consumer blocker; flag any vision-only handle/object detection in the loop.
- HKU dexterous continuum manipulator (Nat. Comms 2025) — **manual-download follow-up** (PMC reCAPTCHA + Europe-PMC 500 blocked auto-capture).
- ASTM F3442/F3442M-23 DAA thresholds — **manual-download follow-up** (paid standard; preprints.org review also bot-blocked).

## Multimodal locomotion

- Air-ground hybrids — endurance-lever results (passive-wheel/active-wheel/tilt-rotor); new energy numbers extend [[drone-power-budget]].
- LEONARDO (Caltech leg-rotor biped) — **primary-capture follow-up** (only journalism in-corpus; Science Robotics primary not yet captured).
- Kovac aerial-aquatic (Science Robotics 2022) — **manual-download follow-up** (Imperial Spiral SPA returned no content).

## Regulation & operations

- FAA Part 108 BVLOS — track NPRM → final-rule status (EO 14307 mandated ~Feb 2026 final rule; confirm whether issued and what changed on autonomy/DAA).
- EASA / Transport Canada / CAAC BVLOS & DAA rulemaking — consumer-operations-relevant changes.

## Manufacturing & onshoring

- Canadian drone onshoring — main thread now ingested ([[canadian-drone-onshoring]], [[drone-manufacturing-supply-chain]]); ongoing monitoring of ISED / NRC IRAP / AIAC / CCAA signals.
- Drone Innovation Hub operational status (Ottawa/Mirabel) — watch for facility opening, first cohort, actual $ allocation breakdown vs the announced $105M/3yr.
- IRAP "Defence Industry Assist" $241M uptake — does dual-use/consumer SME money actually flow, or stay in defence primes?
- Volatus Mirabel buildout — independent (non-Volatus-IR) corroboration of lease/equipment/first-article production.
- Aeryon → FLIR acquisition primary documents — terms + IP disposition (currently only secondhand BetaKit).
- BOM-level Canadian supply-chain audit (motors, batteries, optics, NPUs, comms radios, carbon fibre) — the component-by-component gap currently unmapped.
- Canada BVLOS rule text — 2025 CARs reform / DAA standard (currently only signalled in Gowling; no captured rule text).

<!-- weekly-brief appends overflow entries below, newest run first -->

### Run 2026-05-17
**Regulation & operations**
- FCC/DJI Covered List — comment deadline 11 May; FCC signalled no softening; ~96.7% US ops on DJI, market-structure inflection.
- FAA Part 108 — no final rule in window; EO-mandated ~Feb/Mar 2026 target appears slipped (track next).

**Onboard compute & energy**
- ADLINK + Qualcomm ~15 TOPS edge-AI drone kit (Embedded World 2026) — integrated flight-control + onboard inference board.
- DJI Enterprise Onboard-AI Challenge 2026 — platform push validating onboard (vs cloud) inference; finalists imminent.

**Manufacturing & onshoring**
- Canada onshoring momentum — Alberta investment backgrounder; InDro scaling Canadian content 50%→80%; Volatus domestic battery supply.

**Physical interaction & manipulation**
- VLA-for-aerial-manipulation subfield crystallising (AIR-VLA + DroneVLA captured; watch for sim-to-real / onboard-inference follow-ons).
