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
| [[close-range-depth-sensors]] | Sensor landscape for 0.5–2 m depth perception (stereo RGB-D, dense ToF, miniature ToF arrays); quantitative benchmarks; implications for drone grasp-approach perception. |
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
| [[ground-aerial-robots]] | Ground-primary burst-flight platforms: DoubleBee (2.78 kg bicopter+wheels), Duawlfin (800 g unified actuation, 30× energy ratio), ATMO (5.5 kg mid-air morphing), M4 primary paper + autonomy pipeline; RL stair-climbing (38% power reduction, 3/5 hardware success); all demoed but mocap-dependent. |
| [[air-water-robots]] | Amphibious hybrids — research-curiosity maturity (≥200 s mode-switch, ~0.08 m/s swim). |
| [[dream-to-fly]] | ETH RPG, ICRA 2026 — DreamerV3 pixel→control, no LiDAR, ≤9 m/s; Position-B for the lidar-vs-vision conflict. |
| [[air-vla]] | First VLA benchmark for aerial manipulation (sim-only; best ~42/100; global-camera-dependent). |
| [[dronevla]] | Binary-action VLA fetch-and-handover PoC; navigation real, VLA sim-only. |
| [[canadian-drone-onshoring]] | State of Canadian capacity (thin, assembler-economy) + 2026 funding wave + gaps; consumer/dual-use scope. |
| [[drone-manufacturing-supply-chain]] | Assembler-vs-OEM economy, IP erosion, three-C framework, named-company datapoints, component-level gaps. |
| [[system-architecture]] | Full cognitive-stack architecture for the home-tidy drone: all subsystems, critique, missing components (perception pipeline, safety arbiter, exploration mode), phased roadmap, and 6 critical challenges. |
| [[home-tidy-drone-prototype]] | Feasibility & build plan for an indoor dock+navigate+voice+pick-up drone; requirements→tech→gaps→buy list. |
| [[onboard-grasp-perception]] | Open-vocab detection + grasp-pose for drones; aerial OVD ~28% F1, all onboard graspers category-specific (the central blocker). |
| [[tactile-manipulation]] | Tactile sensing for manipulation: sensor classes (GelSight/DIGIT, taxel skins, F/T), FARM diffusion policy, NeuralFeels visuotactile SLAM, TacSL sim-to-real, zero-shot unknown-object grasping; relevance to land-then-grasp drone architecture. |
| [[precision-docking-recharging]] | Industrial drone-in-a-box ships (RTK+fiducial); consumer-indoor IR-beacon/wireless docking far less mature. |
| [[indoor-cluttered-slam]] | Indoor/home SLAM beyond outdoor demos: object-level, multi-floor, symmetric-room loop closure, 3DGS, dynamic movers. |
| [[voice-intent-task]] | Voice→intent→task for drones: on-device STT + LLM grounding; real-flight benchmarks; latency/grounding/safety gaps. |
| [[safe-indoor-flight]] | Human/pet-proximate safety: ducted/caged props, collision-tolerant/inflatable/tensegrity, FAA OOP energy limits. |
| [[semantic-object-memory]] | Semantic 3D scene graphs + "where things belong" (Hydra/ConceptGraphs/Housekeep); mostly ground-robot, transfer to drones. |
| [[home-tidying-robots]] | State-of-the-art ground-robot tidying systems (TidyBot, TidyBot++, WRC2020, benchmarks); personalisation methods; gap table vs our aerial approach. |
| [[drone-commercial-verticals]] | Index of consumer/commercial verticals + cross-vertical gaps (BVLOS, unit economics, acceptance). |
| [[drone-inspection-use-case]] | Infrastructure/energy/telecom inspection — Percepto@Chevron, Skydio Dock@utilities; shipping at scale. |
| [[drone-delivery-use-case]] | Last-mile logistics — Zipline 2M+ deliveries; unit economics still subsidized (Amazon ~$63 vs $10 price). |
| [[drone-agriculture-use-case]] | Precision ag/spraying — DJI Agras 600k units, XAG 20M+ ha; the clearest ROI-positive vertical. |
| [[drone-mapping-surveying-use-case]] | Photogrammetry/survey — DroneDeploy/Pix4D/Propeller; most mature vertical, lowest reg friction. |
| [[bvlos-regulation]] | US/Canada/EU BVLOS compared — Canada operationally ahead (in-effect Nov 2025); EASA SORA 2.5; FAA Part 108 slipped. |
| [[drone-battery-energy]] | Energy-density futures — Amprius 450 Wh/kg, hydrogen BVLOS, hybrid; the propulsion-futures contest. |
| [[slam]] | Hub: what SLAM is (localization + mapping + loop closure), VIO vs LiDAR-inertial front-ends, how pose reaches the FC, indoor failure modes. |
| [[learned-slam]] | AI/learning-based SLAM layer: neural LIO, learned VIO, edge 3DGS-SLAM (GS-LIVO on Orin), monocular metric-depth foundation models, learned place recognition. |
| [[slam-fc-integration]] | External SLAM/VIO pose fused into ArduPilot EKF3 / PX4 EKF2 via MAVROS vision_pose — frames, EK3_SRC params, delay tuning, divergence pitfalls. |
| [[fast-lio-mid360-orin]] | Deploying FAST-LIO2 LiDAR-inertial odometry with a Livox MID360 on a Jetson Orin under ROS 2 — driver, IMU quirks, calibration, variants, compute. |
| [[indoor-obstacle-avoidance]] | Two-tier indoor avoidance: FC-native reactive (ArduPilot BendyRuler/Dijkstra, PX4 Collision Prevention) + companion planners (EGO-Planner/Swarm, FASTER). |
| [[mighty]] | MIT-ACL Hermite-spline UAV trajectory planner; joint spatiotemporal optimization, −9.3% compute / −13.1% travel vs MINCO, 6.7 m/s onboard (MID360+DLIO). |
| [[drone-comms-wifi]] | Defeating DDS multicast-discovery failures over home WiFi (Discovery Server, Zenoh RMW/bridge) and routing MAVLink-over-UDP to multiple endpoints. |
| [[prop-guard-failsafe]] | Build-level guard/failsafe choices for the indoor prototype: physical rotor guarding, FAA OOP energy ceiling, ArduPilot/PX4 failsafe params. |
| [[gps-denied-hover-land]] | GPS-denied indoor build reference: optical-flow Loiter hold + AprilTag/ArUco precision landing; argues fiducials-first over LiDAR-SLAM for V1. |
| [[payload-budget]] | Component masses, payload→flight-time trade, and thrust/throttle targets sizing the Phase-1 indoor drone's sensor+compute budget on the X500 V2. |
| [[robot-vacuum-navigation]] | Precedent: mass-market robot-vacuum localization/mapping/coverage stacks (LDS-SLAM, VSLAM, ToF) and what transfers to a GPS-denied indoor drone. |
| [[warehouse-robot-navigation]] | Precedent: Amazon/Kiva fleet nav — fiducial-grid + central planner beat per-robot autonomy at scale; lessons for a fiducials-first indoor drone V1. |
| [[lidar-vs-vision-autonomy]] | **Conflict (OPEN):** is LiDAR necessary for drone autonomy, or do vision/event cameras suffice? |

---
