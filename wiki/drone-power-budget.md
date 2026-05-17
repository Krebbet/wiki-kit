# Drone Power Budget — Is Onboard AI the Limiter?

Direct answer to a recurring question: for the large majority of consumer drones, **onboard-AI compute energy is not the binding limiter — propulsion dominates the power budget and battery energy density is the real ceiling.** Compute is a small slice (≈0.2–10% of total electrical power) whose *share grows as the drone shrinks*; only at sub-30 g insect/nano scale does compute weight-and-power become a genuine wall, and that is exactly where neuromorphic computing earns its case. This page consolidates the hard numbers; the neuromorphic relief path is detailed in [[neuromorphic-computing-for-drones]] and the conventional low-power path in [[nano-drone-compute]].

## The decomposition (hard numbers)

*(synthesis — each figure traces to the cited raw source)*

- **Fixed-wing, classical autopilot** (`07-power-tradeoff-uav`): a small electric UAV needs ~20–200 W/kg to fly; a 4.5 kg / 5 m-span example draws ~100 W total; a sub-1 kg lightweight ~40 W. The autopilot (compute + sensing) draws **1.5–5 W**, "negligible in large aircraft" — **~5% of total power in small UAVs, rising to ~10% in lightweight UAVs**. Adaptive (lower-clock) control can cut autopilot power 5–10× (≈4 W → 0.04–0.06 W). **Caveat:** this models *classical autopilot DSP at <200 Hz*, not DNN inference — AI-inference loads can multiply the avionics budget (flagged as an *open gap*).
- **27 g nano-quadrotor, conventional DNN** (`01-nano-drone-dnn-engine`, PULP-Dronet on Crazyflie 2.0 + GAP8): total system ~7.6 W, **motors ~7.3 W (~96%)**, electronics ~277 mW, the DNN inference deck adds only **64 mW (0.8%)** to **284 mW (3.5%)**. The endurance penalty of the deck is dominated by its *added mass*, not its power draw.
- **27 g nano-quadrotor, newer generation** (`03-nano-uav-pose`, PULP-Frontnet, same Crazyflie/GAP8 lineage): inference **8.6–87 mW = 0.2–1.7% of the ~5 W system**; 135 fps at 86 mW; 7.5× throughput at 32% the power of the prior generation.
- **27 g nano-quadrotor, full vision+SLAM** (`02-gap9shield`, GAP9 deck): YOLO, NanoSLAM, MCL all run **<100 mW** — well under 1% of the ~10–15 W propulsion envelope of that class.
- **Sub-30 g insect scale — the wall** (`12-decroon-telluride2023`): a 29 g Delfly flies on **6 W**; an Nvidia Jetson Nano is **85 g and 7.5 W** — the conventional compute module is *heavier than the airframe and burns more power than flight*. A room-scale SLAM map needs 100s of MB–GBs vs the Delfly MCU's 192 KB. This closes off conventional SLAM/deep-learning at this weight class. Explicitly **weight-class-specific** — a 3 kg drone runs a Jetson Xavier with no issue.

## Verdict *(editorial synthesis)*

The "is compute the limiter?" question has a **scope-dependent answer**, and the corpus contains a real (not strawman) tension between two framings:

- **"Compute is an already-solved sub-budget; propulsion + battery dominate"** — supported by `01`, `02`, `03`, `07`: conventional ultra-low-power SoCs (PULP/GAP8→GAP9) already fit AI inference into <1–3.5% of a nano-drone's power, and classical control optimisation alone recovers most of the rest. Neuromorphic is *one* path, not a necessity, for many tasks.
- **"At insect scale, compute is THE wall and neuromorphic is essential"** — supported by `12` (and the neuromorphic results in `04`/`06`/`13`): below ~30 g the conventional compute module's weight and power exceed the airframe's, and only neuromorphic (event camera + SNN on Loihi/Speck/Kraken) closes it — with measured savings of **3–4 orders of magnitude energy/inference vs a Jetson** (`04`: 27 µJ/inf; `06`: <50 mW closed-loop; `13`: 2.7 mW localisation, ground-robot, transfer-relevant).

These are not contradictory — they are the same curve at different points: compute's *share* of the budget scales inversely with drone size, crossing from "negligible" to "dominant" somewhere around the tens-of-grams class. The honest consumer-relevant conclusion: **battery energy density and propulsion efficiency gate endurance for normal consumer drones; the neuromorphic question only becomes load-bearing if the consumer use-case demands palm-sized or smaller platforms.**

## Open gaps

- The cleanest power-decomposition source (`07`) predates heavy onboard AI-inference; no captured source gives a *modern DNN-inference* power decomposition for a mid-size consumer drone. Flagged for future research.
- Whether conventional low-power SoCs ([[nano-drone-compute]]) keep pace such that neuromorphic never becomes necessary for consumer scales is unresolved — see [[neuromorphic-computing-for-drones]].

## Multimodal locomotion as an endurance lever *(synthesis)*

If propulsion (not compute) is the binding power consumer, the highest-leverage move is to *stop flying when you don't have to*. Rolling costs roughly an order of magnitude less power than hovering, so air-ground hybrids convert the endurance ceiling dramatically (detail in [[air-ground-hybrids]], overview in [[multimodal-locomotion]]):

- **Single passive wheel** (~20 g, no actuator): **~77%** power saved sitting on the wheel, **61%** while rolling, vs hover — the minimal-hardware existence proof.
- **Roller-Quadrotor** (active wheel): **~41× longer ground operating time** and ~3.8× lower J/m than flight (rolling ~15.6 W vs flight ~658 W).
- **Tilt-Ropter** (2026, fully-actuated): **92.8% ground-power reduction** vs flight (47.4 W vs 653.6 W).

Together with [[aerial-perching]] (perch-and-stare ≈ 15× hover endurance), these are the two principal levers against the 3–15 min flight-time wall — and they matter far more for consumer endurance than shaving the sub-watt compute budget. Caveat: the ground-mode mechanism adds mass that *reduces* flight time, so the net win depends on the mission's fly/roll ratio.

## Source

- `raw/research/onboard-ai-energy/07-power-tradeoff-uav.md` — fixed-wing power decomposition, compute-share-vs-scale
- `raw/research/onboard-ai-energy/01-nano-drone-dnn-engine.md` — 27 g Crazyflie, 96% motors / sub-watt compute
- `raw/research/onboard-ai-energy/03-nano-uav-pose.md` — PULP-Frontnet, 0.2–1.7% compute share
- `raw/research/onboard-ai-energy/02-gap9shield.md` — GAP9 deck, <100 mW full vision+SLAM
- `raw/research/onboard-ai-energy/12-decroon-telluride2023.md` — the sub-30 g compute wall (de Croon)
- `raw/research/onboard-ai-energy/04-fully-neuromorphic-flight.md` — neuromorphic energy/inference figures
- `raw/research/onboard-ai-energy/06-colibriuav.md` — <50 mW closed-loop neuromorphic platform
- `raw/research/onboard-ai-energy/13-neuromorphic-localization.md` — 2.7 mW localisation (ground robot, transfer)

## Related

- [[nano-drone-compute]] — the conventional ultra-low-power SoC path (PULP/GAP lineage)
- [[neuromorphic-computing-for-drones]] — the neuromorphic relief path and its maturity limits
- [[neuromorphic-materials]] — memristor/in-memory compute (long-horizon, pre-deployment)
- [[drone-autonomy-state]] — where this verdict feeds the overall autonomy picture
- [[event-cameras-for-uavs]] — event sensing, the front-end half of the neuromorphic argument
- [[air-ground-hybrids]] · [[multimodal-locomotion]] — rolling-instead-of-hovering as the biggest endurance lever
- [[aerial-perching]] — the other principal endurance lever
