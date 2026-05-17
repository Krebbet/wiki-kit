# Drone Sensors for Autonomy

A reference map of the sensors used on AI-navigated and autonomous (or partially autonomous) drones, and what each is for. The field splits into **proprioceptive** sensors (IMU, GNSS/RTK, barometer, magnetometer — ego-state) and **exteroceptive** sensors (cameras, event cameras, LiDAR, radar, acoustic, ADS-B — perceiving the world). The central design tension across the corpus is **LiDAR vs vision/event** for the exteroceptive depth/avoidance role; see [[lidar-vs-vision-autonomy]].

## Sensor → purpose → maturity

*(synthesis — table compiled across sources; each row's claim is traceable to the cited page)*

| Sensor | Primary purposes | Maturity | Key tradeoff |
|---|---|---|---|
| **RGB / fisheye cameras** | Obstacle avoidance, subject tracking, 3D mapping, VIO | *Shipping at scale* (Skydio: 6× 4K fisheye, 360°) — see [[skydio-autonomy-stack]] | Best SWaP + semantic texture; no direct depth, motion blur, fails in low light / featureless scenes |
| **Stereo cameras + IMU (VI-SLAM)** | GPS-denied outdoor localization, dense mapping, planning | *Demoed*: full forest autonomy, 0 collisions, onboard ([[visual-inertial-slam]]) | Cheap/light; learned depth capped ~6.5 m, depth inference is the compute bottleneck |
| **Event cameras** | Low-latency obstacle dodging, high-speed flight, low-light/HDR, VIO | Sensors *shipping at scale*; drone use mostly *demoed*/lab ([[event-cameras]], [[event-cameras-for-uavs]]) | µs latency, >120 dB DR, near-zero blur, ~0.5 W; no absolute intensity (needs paired frame camera), CV algos need adaptation |
| **2D LiDAR** | Altitude hold, autonomous landing, coarse mapping | *Shipping at scale* (legacy) | Cheap/simple; largely superseded by 3D |
| **Mechanical 3D LiDAR** (Velodyne VLP-16, Ouster OS1-128) | SLAM, high-res mapping, obstacle avoidance | *Shipping at scale* ([[lidar-for-uav-autonomy]]) | Lighting-independent cm depth, detects thin wires; heavy, costly, no texture |
| **Solid-state 3D LiDAR** (Livox Avia ~500 g/$1.5k; MID360 ~265 g/$700) | Agile GNSS-denied nav, swarms; enables >20 m/s | *Shipping at scale* in research fleets ([[lidar-for-uav-autonomy]]) | Lighter/cheaper than mechanical; narrower/non-repetitive FOV |
| **FMCW LiDAR** | Per-point radial velocity, long-range (100–300 m), fog-resilient | *Demoed* | Velocity + range + weather robustness; cost $1.5k–$10k gates UAV use |
| **IMU** | Ego-motion, attitude, tight fusion with all vision/LiDAR odometry | *Shipping at scale* (universal) | Indispensable but drifts; always fused |
| **GNSS / RTK** | Global position, precision waypoint/landing | *Shipping at scale* | cm-level with RTK; denied indoors / under canopy / contested — drives all GPS-denied autonomy work |
| **Radar** (incl. on-tower) | Detect-and-avoid, non-cooperative traffic detection | *Demoed* / fielded in defence ([[anduril-lattice]]) | All-weather, long range; coarse angular resolution |
| **ADS-B In / electronic conspicuity** | Cooperative detect-and-avoid (DAA) | *Proposed rule* baseline for BVLOS ([[detect-and-avoid]], [[faa-part-108-bvlos]]) | Cooperative only — blind to non-broadcasting aircraft (the open DAA gap) |
| **Acoustic** | Low-cost passive non-cooperative DAA | *Demoed* (acknowledged modality, no consensus standard) | Cheap/passive; short range, noise-limited on a drone |

## What drives sensor choice

- **Mission environment** — GNSS-denied (forest, indoor, contested) eliminates GPS reliance and forces VIO/LIO ([[visual-inertial-slam]], [[lidar-for-uav-autonomy]]).
- **Speed/agility** — high-speed and dynamic-obstacle work pushes toward µs-latency event cameras ([[eth-rpg-scaramuzza]]) or dense LiDAR; conventional frame cameras' latency/blur become limiting.
- **SWaP + cost** — payload, endurance and unit economics favour cameras; LiDAR is the heavier/costlier but lighting-independent option. This is the crux of [[lidar-vs-vision-autonomy]].
- **Regulatory** — BVLOS at scale requires a certifiable DAA sensor stack; the unsolved piece is *non-cooperative* detection ([[detect-and-avoid]]).

## Source

- `raw/research/autonomy-and-sensors/01-lidar-uav-survey.md` — LiDAR sensor classes, tradeoffs, maturity
- `raw/research/autonomy-and-sensors/02-event-camera-survey.md` — event-camera specs/vendors
- `raw/research/autonomy-and-sensors/03-vislam-no-lidar.md` — stereo+IMU sensor suite, depth limits
- `raw/research/autonomy-and-sensors/06-event-vision-uav-review.md` — event-vision UAV applications
- `raw/research/autonomy-and-sensors/08-skydio-autonomy-intro.md` — Skydio camera-only suite (vendor)
- `raw/research/autonomy-and-sensors/11-mittr-anduril-demo.md` — fielded radar/optical sensor fusion
- `raw/research/autonomy-and-sensors/04-faa-part108-nprm.md` — DAA sensor/equipage requirements
- `raw/research/autonomy-and-sensors/12-astm-f3442-daa.md` — DAA standard scope (partial: scope only, thresholds paywalled)

## Related

- [[drone-autonomy-state]] — what these sensors enable, by maturity
- [[lidar-vs-vision-autonomy]] — the central LiDAR-vs-vision sensor debate
- [[lidar-for-uav-autonomy]] — LiDAR sensor classes and SLAM stack
- [[event-cameras]] / [[event-cameras-for-uavs]] — event-sensor detail
- [[visual-inertial-slam]] — camera+IMU autonomy without LiDAR
- [[detect-and-avoid]] — the DAA sensor problem for BVLOS
- [[aerial-manipulation]] — onboard object/handle perception is the binding gap for drone manipulation
