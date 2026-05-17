# Wiki Index

AI × drones — capability stack, hardware, regulation, manufacturing (with Canadian onshoring focus), physical-interaction modalities, and the path to mass commercial deployment.

Catalog of all pages in this wiki. Updated on every ingest.

---

## Overview

| Page | Summary |
|---|---|
| [[drone-autonomy-state]] | Synthesis: narrow autonomy shipping, agile autonomy demoed, BVLOS regulation still being written. |
| [[drone-sensors-for-autonomy]] | Reference map — sensor → purpose → maturity → tradeoff (camera, event, LiDAR, IMU, GNSS, radar, ADS-B, acoustic). |
| [[lidar-for-uav-autonomy]] | LiDAR sensor classes (2D/mechanical/solid-state/FMCW), LIO algorithm lineage, benchmarks; LiDAR-necessary position. |
| [[event-cameras]] | Event-camera fundamentals: µs latency, >120 dB DR, vendors, algorithm families. |
| [[event-cameras-for-uavs]] | UAV-specific event-vision applications, dataset map, neuromorphic-on-drone results. |
| [[eth-rpg-scaramuzza]] | ETH/UZH RPG (Scaramuzza) lab profile — demoed event-camera drone results, latency figures, AI-vs-human race. |
| [[visual-inertial-slam]] | Stereo+IMU forest autonomy without LiDAR/GNSS; OKVIS2, dense submaps, trajectory anchoring. |
| [[skydio-autonomy-stack]] | Skydio 6-camera "Spatial AI" vision-only autonomy (vendor, 2020-era; read critically). |
| [[anduril-lattice]] | Defence-origin multi-asset autonomy + sensor fusion; single-operator fleet control model (potential consumer-transfer tech). |
| [[faa-part-108-bvlos]] | FAA Part 108 NPRM — permits mostly/fully autonomous BVLOS; ~Feb 2026 final-rule deadline. |
| [[detect-and-avoid]] | DAA requirements; ASTM F3442 scope (partial); cooperative solved, non-cooperative is the open gap. |
| [[drone-power-budget]] | Is onboard AI the limiter? No for most drones (propulsion dominates); a wall only at sub-30 g scale. |
| [[nano-drone-compute]] | Conventional ultra-low-power path: PULP/GAP8→GAP9, AI inference at <1–3.5% of a nano-drone's power. |
| [[neuromorphic-computing-for-drones]] | SNN + neuromorphic HW (Loihi/Speck/Kraken) flown/benchmarked; MAVLab arc; real savings but lab-stage. |
| [[neuromorphic-materials]] | Memristor/in-memory compute — promising at device level but TRL ~2–3, 5–10+ yr from drone use. |
| [[aerial-manipulation]] | How drones interact with objects: state + the consumer-task gap list (perception/payload/endurance/safety). |
| [[aerial-grasping]] | Vision-only onboard grasping (2 m/s, ~150–217 g) + gripper-mechanism taxonomy. |
| [[aerial-perching]] | Perching mechanisms; perch-and-stare gives ~15× endurance — the big consumer energy lever. |
| [[drone-contact-and-door-tasks]] | Door-opening (RL, HI-ARM, FlyCroTug), object transport, surface-contact; all mocap-gated indoors. |
| [[cooperative-aerial-manipulation]] | Multi-drone lift/force; industrial-leaning + the FlyCroTug consumer-scale glimpse. |
| [[multimodal-locomotion]] | Drones that also drive/walk/swim; air-ground hybrids buy ~10–40× endurance; AirCrab/M4 exist. |
| [[air-ground-hybrids]] | Energy spine: passive-wheel 77%, Roller-Quadrotor 41×, Tilt-Ropter 92.8%; AirCrab arm+wheels; M4. |
| [[air-water-robots]] | Amphibious hybrids — research-curiosity maturity (≥200 s mode-switch, ~0.08 m/s swim). |
| [[lidar-vs-vision-autonomy]] | **Conflict (OPEN):** is LiDAR necessary for drone autonomy, or do vision/event cameras suffice? |

---
