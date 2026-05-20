# Reference Sources — weekly-brief configuration

Per-wiki customisation for `/weekly-brief`. The skill reads this file fully before its trend scan; the `## Scope`, `## Selection priority`, and `## Local conventions` sections **override** the skill's generic-ML defaults (this is an AI×drone wiki, not an LLM-trends wiki).

## Scope

This wiki covers the **intersection of AI and drones (UAVs/UAS), scoped to consumer/commercial uses**. In scope: onboard AI for drones (perception, planning/control, VIO/SLAM, event/neuromorphic), drone hardware/propulsion/sensors, physical interaction (grasping, perching, door/contact tasks), multi-modal locomotion (air-ground/air-water), regulation (FAA/EASA/Transport Canada/CAAC, BVLOS, DAA), operational economics, R&D, and drone manufacturing/supply chain with attention to **Canadian onshoring**.

**Defence-space material is in scope ONLY as transferable technology** that could apply to consumer use (e.g. a sensor-fusion or autonomy method) — never defence procurement/politics/ethics, and never a "defence-vs-consumer" framing. Skip pure-defence, weapons, and ISR content. (Standing user guidance — see assistant memory `feedback-consumer-focus`.)

## Selection priority

Replaces the skill's default signal hierarchy. Rank candidates by, in order:

1. **Drone/robotics domain fit** — the paper or release must bear on UAV autonomy, perception, manipulation, multimodal locomotion, onboard compute/energy, or drone regulation/operations. A generic LLM/CV/RL paper with no aerial-robotics hook is **out of scope** even if trending.
2. **Multiple independent signals** — surfaced by ≥2 of: arXiv cs.RO trending, a tracked named-group page, a robotics-venue accept, IEEE Spectrum robotics, reputable drone industry press.
3. **Technical novelty over volume** — one new mechanism > many reframings.
4. **Conflict load-bearing** — prioritise anything that supplies a position for an open `wiki/conflicts/*.md` (currently: `lidar-vs-vision-autonomy`).
5. **Consumer-relevance** — favour work plausibly transferable to consumer/prosumer/commercial use; down-rank pure industrial-inspection-only or pure-defence unless the *method* transfers.
6. **Reproducibility** — code released > promised > closed.

Skip: vendor product PR without technical depth, "drones will deliver everything by [year]" hype, regurgitated press releases, defence-vs-consumer narrative pieces.

## Brief emphasis & exclusions

Controls the *shape* of the email, not just source selection. The 2026-05-17 run drifted by giving regulatory/market/industrial-policy news headline billing — these rules close that.

- **Headline-first = technical research.** The `# Trends` bullets and `# Top 3` MUST center this wiki's technical threads: onboard AI/autonomy, perception (VIO/SLAM/event/neuromorphic), aerial manipulation, multimodal locomotion, onboard compute/energy, and open conflicts. A paper/method, not a news item, should occupy every Top-3 slot whenever any technical candidate cleared the bar.
- **Regulatory / market / onshoring = context only.** FAA/EASA/Transport-Canada rule status, market sizing, funding waves, and Canadian-onshoring news are legitimate *watchlist + at most ONE* `# Trends` context bullet — **never a Top-3 slot** and never more than one trends bullet, unless a concrete transferable *technology* is the story.
- **Defence/geopolitics = watchlist-line max.** DJI/FCC-ban politics, NATO, "defence industrial strategy" qua politics, procurement programs: a single watchlist line at most, never a headline or Top-3, unless there is a specific consumer-transferable technical method. No defence-vs-consumer framing anywhere in the brief.
- **Product-launch / vendor PR:** watchlist-line max; never a Top-3.
- **Thin/quiet week → prefer the short empty-run email** over padding with market/regulatory news. If zero technical-research candidates clear the domain-fit + signal bar, send the 3-line empty-run note (skill step 9). Do not manufacture a full brief from news.

## Watched sources (trend-scan set — cheapest to most expensive)

- **arXiv** `cs.RO` recent + `cs.CV`/`cs.LG` filtered for `UAV|drone|aerial|quadrotor|MAV` — primary signal.
- **alphaXiv trending**, filtered to robotics/aerial entries only.
- **Named research groups** (new-publication pages): ETH RPG (Scaramuzza), TU Delft MAVLab (de Croon), Caltech CAST / GALCIT (Chung/Gharib), UPenn GRASP (Kumar), EPFL LIS (Floreano) & Imperial Aerial Robotics (Kovac), Stanford ASL, U-Toronto UTIAS (Schoellig/Waslander), Seville GRVC (Ollero — industrial, mine for transferable method only).
- **Robotics venues**: ICRA, IROS, RSS, CoRL, T-RO, RA-L, *Science Robotics*, *Nature Communications/Machine Intelligence* (robotics).
- **Industry/regulatory** (consumer-relevant): IEEE Spectrum (robotics/drones), DroneDJ, sUAS News; FAA / EASA / Transport Canada / CAAC rulemaking pages (Part 108 status, DAA standards, ASTM F38).
- **Company technical blogs**: Skydio, Zipline, Wing, Auterion, Parrot.
- **Canadian onshoring**: ISED, NRC IRAP, AIAC, CCAA (low-frequency; check monthly not weekly).
- **Community pulse (low weight)**: r/drones, r/robotics hot — narrative signal only, never a sole source.

## Local conventions

- **Capture engine:** the workstation GPU is power/clock-capped and often busy — default PDF capture to `--engine pymupdf` (text-faithful; figures lower-fidelity), not `marker`. Re-capture with `marker` later only if a specific figure matters.
- **Bot-walled hosts** (use manual-download fallback; don't burn retries): IEEE Xplore, ScienceDirect, MDPI, `cdnsciencepub.com`, `preprints.org`, `nature.com` (use the PMC/Europe-PMC mirror), and **PMC itself can intermittently serve a reCAPTCHA** — verify PMC captures are real content, not a challenge page. Prefer arXiv.
- **YouTube:** capture transcripts **one at a time**, never in a parallel batch (parallel pulls trigger HTTP 429).
- **Paths:** always pass capture `--out` relative to the repo root, or prefix with `cd "$(git rev-parse --show-toplevel)" &&` — shell cwd drifts in long runs.
- **Capture cap:** hard limit 5/run (skill default); surplus → `watchlist.md` (cap 10/run).
- **Scope guard:** before writing any page from a defence-origin source, strip procurement/politics/ethics framing; keep only the transferable technology. No new defence-vs-consumer `conflicts/` files.
