# LiDAR for UAV Autonomy

2025 HKU MaRS Lab survey (arXiv 2509.10730, authors of FAST-LIO) argues LiDAR is becoming the superior enabling sensor for high-speed GPS-denied UAV autonomy. The case rests on active cm-level depth independent of lighting, wire-detection capability, and dense fast point clouds that vision-inertial systems cannot match at range or speed. Solid-state units have dropped below 500 g/$1,500, making airborne deployment practical at scale.

## Sensor Classes

**2D LiDAR** — altitude hold and landing only (*shipping at scale*, legacy role).

**Mechanical 3D spinning** — Velodyne VLP-16, Ouster OS1-128; SLAM, mapping, obstacle avoidance (*shipping at scale*).

**Solid-state 3D** — Livox Avia ~500 g/$1,500; MID360 ~265 g/$700. Enables agile GNSS-denied flight at >20 m/s (*shipping at scale* on research fleets). Primary driver of the current autonomy frontier.

**FMCW** — per-point velocity readout, 100–300 m range, fog-resilient (*demoed*); cost $1,500–$10,000 currently gates UAV adoption.

## Sensor Tradeoffs vs Vision

LiDAR: active cm-level depth, lighting-independent, detects thin wires, dense fast point clouds; penalty is weight, cost, no texture, scatter in rain/fog.

Camera/[[visual-inertial-slam|VIO]]: better SWaP, semantic texture; no direct depth, motion blur, lighting failures. Intel D435i depth caps at 3–5 m vs LiDAR's tens-to-hundreds of metres — the survey treats this gap as categorically disqualifying for high-speed avoidance. See [[lidar-vs-vision-autonomy]].

PULSAR is cited as the only successful self-rotating UAV platform; LiDAR handles the rotation-induced motion blur that defeats frame cameras.

## Algorithm Lineage

**Odometry/SLAM:** LOAM (2014) → FAST-LIO/FAST-LIO2 (ESIKF + ikd-tree, 2021–22) → Point-LIO (2023) → FAST-LIVO2 (LiDAR + cam + IMU, 2024); Swarm-LIO2 (2024, multi-UAV).

**Planning:** two-stage front/back-end standard. MINCO/GCOPTER + safe flight corridors (SFC) are state-of-the-art; benchmarks: 13.7 m/s cluttered (SFC+MINCO), 20 m/s safety-assured (SUPER, *Science Robotics* 2025).

**Mapping:** OctoMap/ROG-Map/D-Map discrete representations preferred airborne; continuous ESDF too compute-heavy. All pipelines run fully onboard on PX4/ArduPilot autopilots.

## Maturity

- *Shipping at scale*: infrastructure inspection (wind turbines, bridges, power lines), precision agriculture.
- *Demoed*: high-speed agile flight, multi-UAV swarms.
- *Speculated*: widespread autonomous delivery, pending further cost reduction.

## Source
- `raw/research/autonomy-and-sensors/01-lidar-uav-survey.md` — HKU MaRS Lab 2025 survey (arXiv 2509.10730) on LiDAR-based UAV autonomy algorithms and hardware

## Related
- [[visual-inertial-slam]] — vision-only counterpoint; authors concede LiDAR depth range superiority
- [[event-cameras]] — alternative sensing modality for agile low-light flight
- [[drone-sensors-for-autonomy]] — cross-sensor comparison and SWaP tradeoffs
- [[lidar-vs-vision-autonomy]] — debate page; this survey anchors the LiDAR-necessary camp
- [[drone-autonomy-state]] — current deployment maturity across the full autonomy stack
