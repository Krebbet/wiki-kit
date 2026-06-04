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
| [[close-range-depth-sensors]] | Sensor landscape for 0.05–2 m depth perception: D405 (7–50 cm arm specialist), OAK-D SR (30 cm–1 m + onboard AI), D435/D455/ZED 2/OAK-D Pro, PMD Flexx2, miniature ToF arrays; D3RoMa for transparent/specular surfaces; two-camera ground-robot recommendation. |
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
| [[ros2-nav2]] | ROS 2 Nav2 full architecture: BT navigator, 5 action servers, costmap layers (STVL), TEB controller, SLAM integration, marathon benchmark (37.4 mi, 0 collisions); SLAM method comparison for indoor navigation. |
| [[slam-toolbox]] | SLAM Toolbox: default ROS 2 2D SLAM; graph-based pose-graph over OpenKarto + Ceres; sync/async/pure-localization modes; multi-session mapping; 24,000 m² real-time on mobile CPU. |
| [[2d-lidar-slam]] | 2D LiDAR SLAM hardware (RPLiDAR S2/A3 specs) + Cartographer architecture (BBS loop closure, SPA) + algorithm comparison table; ATE benchmark numbers for indoor ground robot navigation. |
| [[user-comms-layer]] | User communication layer: entry points (phone/speaker), STT, LLM intent parser, command router, response/TTS; prototype build order and drone-app repo structure. |
| [[map-then-navigate]] | Two-phase indoor robot autonomy: DWFE frontier exploration → save map → AMCL localization → semantic traversal. Pipeline, DWFE algorithm (7.8% more area, 12% less distance), greedy TSP revisit, F1 80–100% on indoor objects. |
| [[dynamic-object-handling]] | Dynamic objects in three timescales: DynaSLAM (clean map building, 93–97% ATE improvement), STVL vs. object-oriented grid (real-time costmap), POCD (between-session change detection, 80% precision), iRobot lifelong maps (1.41% failure rate, production-deployed). |
| [[scene-graph-world-model]] | 3D scene graph world brain: Hydra 5-layer hierarchy (mesh→objects→places→rooms→building), ConceptGraphs build pipeline (SAM+CLIP+LLaVA+GPT-4, node precision 0.71 / edge 0.88), HOV-SG query routing (NL→hierarchy→Voronoi, 56% real-world nav SR), DovSG dynamic updates (27× faster than full reconstruction, 35% long-term task SR). |
| [[ros2-server-bridge]] | ROS 2 ↔ Python server bridge options: rosbridge (WebSocket+JSON, no CDR), mqtt_client (MQTT, primitive or CDR mode), Zenoh (CDR, multi-robot, NAT traversal). Latency table (MQTT 45 µs, Zenoh-p2p 16 µs). Recommendation: rosbridge for dev, mqtt_client for production. |
| [[safe-indoor-flight]] | Human/pet-proximate safety: ducted/caged props, collision-tolerant/inflatable/tensegrity, FAA OOP energy limits. |
| [[semantic-object-memory]] | Semantic 3D scene graphs + "where things belong" (Hydra/ConceptGraphs/Housekeep); mostly ground-robot, transfer to drones. |
| [[home-tidying-robots]] | State-of-the-art ground-robot tidying systems (TidyBot, TidyBot++, WRC2020, benchmarks); personalisation methods; gap table vs our aerial approach. |
| [[tidybot-deep-dive]] | Full deep-dive on TidyBot v1 + v++: hardware BOM, arm comparison table, external-GPU inference constraint, LLM vs diffusion-policy methods, and alignment with/gaps against our project. |
| [[drone-commercial-verticals]] | Index of consumer/commercial verticals + cross-vertical gaps (BVLOS, unit economics, acceptance). |
| [[drone-inspection-use-case]] | Infrastructure/energy/telecom inspection — Percepto@Chevron, Skydio Dock@utilities; shipping at scale. |
| [[drone-delivery-use-case]] | Last-mile logistics — Zipline 2M+ deliveries; unit economics still subsidized (Amazon ~$63 vs $10 price). |
| [[drone-agriculture-use-case]] | Precision ag/spraying — DJI Agras 600k units, XAG 20M+ ha; the clearest ROI-positive vertical. |
| [[drone-mapping-surveying-use-case]] | Photogrammetry/survey — DroneDeploy/Pix4D/Propeller; most mature vertical, lowest reg friction. |
| [[bvlos-regulation]] | US/Canada/EU BVLOS compared — Canada operationally ahead (in-effect Nov 2025); EASA SORA 2.5; FAA Part 108 slipped. |
| [[drone-battery-energy]] | Energy-density futures — Amprius 450 Wh/kg, hydrogen BVLOS, hybrid; the propulsion-futures contest. |
| [[slam]] | Hub: what SLAM is (localization + mapping + loop closure), VIO vs LiDAR-inertial front-ends, how pose reaches the FC, indoor failure modes. |
| [[learned-slam]] | AI/learning-based SLAM layer: neural LIO, learned VIO, edge 3DGS-SLAM (GS-LIVO on Orin), monocular metric-depth foundation models, learned place recognition. |
| [[passive-stereo-robustification]] | Consumer-cost ladder for robust passive-stereo indoor SLAM without expensive LiDAR: honest featureless-surface limit (IMU bridges <1 s), robustifier ladder (IMU→VIO, dense RGB-D, learned front-end, robustness engineering, active stereo), active-stereo geometry (dumb projector, independent vs co-mounted IR), pattern-as-calibration-validator, cheaper-than-D435i hardware ladder ($12 pico → $80–150 OV9281+IR DOE → $334 D435i). |
| [[imu-vio-integration-reality]] | Should the rover add an IMU, and what does it really cost? The chip is ~$5 but the binding cost is camera–IMU **time-sync** to ~1 ms on a two-clock rig (USB camera + ESP32/WiFi, no HW trigger); the IMU bridges <1 s starvation, is **not** a white-wall or PnP-gate fix (hloc cleared that), so it's off the critical path. Buy-nothing-yet; if escalating, the D435i ($334) bundles synced IMU + active stereo + calibration over a bare-IMU sync rabbit hole. |
| [[methods-reading-list]] | Curated, prioritised paper list for the methods we actually run, each tagged with its role in OUR pipeline: Tier 1 RTAB-Map + hloc (the head-to-head); Tier 2 the learned-feature stack that clears the wall (SuperPoint, LightGlue/SuperGlue, NetVLAD, COLMAP); Tier 3 ORB-SLAM3 (what we left) + MASt3R-SLAM/DUSt3R (queued pick #2); Tier 4 calibration (Zhang, Kannala-Brandt, de-prioritised). "If you read three: hloc, SuperPoint, RTAB-Map." |
| [[relocalization-method-bakeoff]] | The marker-free passive-stereo relocalization bake-off, **decided with the prototype's own measured data (EDA003–009):** RTAB-Map's classical ORB→PnP front-end collapses (88% 0-inlier, ~2–4% reloc, map-agnostic); a learned front-end **hloc (SuperPoint+LightGlue+NetVLAD→SfM→PnP)** clears it on the SAME maps + SAME fixed calibration (96% EDA003, 82.6% fresh EDA004) → the wall was the front-end, calibration demoted (P-002). Metric scale validated −1.9% vs tape-measured GT (EDA008, P-005 resolved). MASt3R-SLAM demoted (hloc sufficed). |
| [[anchor-map-protocol]] | How to **build** a good navigation-anchor map with passive stereo: the **multi-sweep recipe** — pool several overlapping free-hand passes into ONE SfM (EDA009: 93.6% reloc, body 96% AND tail 88%, no density/coverage trade-off; passes co-register automatically via NetVLAD). Why one "perfect" pass caps out (EDA004 tail / EDA006 zero-sum). Metric scale validated to ~⅓ m. Forward recommendations: export the RTAB occupancy grid, straighter full-length sweeps, vocab-tree pairing at scale. |
| [[object-fingerprint-memory]] | Per-instance object-fingerprint memory bank — model/method choices (segmenter GDINO+MobileSAM; **embedder DINOv2 ViT-S/14 > CLIP for instance re-ID**), fingerprint schema, re-ID match flow + threshold calibration. De-risked by the runnable prototype (EDA007: multi-view re-ID 88%, DINOv2 lifts recall@P=1.0 0.58→0.96; synthetic data saturates the metric → real same-colour captures OBJMEM-7 are the pending human-gated validation). |
| [[land-rover-v1-build-guide]] | Step-by-step v1 rover build walkthrough (companion to [[land-rover-v1-rig]]): big-picture diagram, parts/tools check, phased assembly (chassis → solder driver → power distribution w/ the multimeter gate → ESP32↔TB6612 signal pinout → flash firmware → wheels-up motion test → camera tether bench-test → vibration gate), each step with motivating "why". Honest v1 scope: skid-steer not mecanum-strafe, open-loop (no encoders, P-003), tethered camera. |
| [[camera-calibration-and-self-calibration]] | Wide-FOV stereo calibration (OpenCV): rational vs cv2.fisheye, the focal/baseline degeneracy (fronto-parallel poses) and how tilt+depth coverage + a known-distance anchor break it, verification (planarity/known-distance); + online self-correcting calibration survey (OpenVINS, OKVIS2-X, VINS-Fusion, Kalibr-reference, DSO photometric), observability/degenerate-motion catch, and the MVP for the prototype's relocalization wall. |
| [[learned-point-cloud-registration]] | DL methods for point cloud registration (DCP→GeoTransformer→PARE-Net): benchmark SOTA, deployment gap analysis (generalization, corruption robustness, latency), GenZ-LIO as classical gap-closer. |
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
| [[cheap-lidar-pricing-guide]] | Full pricing tier table ($16 vacuum salvage → $249 Unitree L1 → $550 Livox MID-360); commercial viability thresholds for a tidy bot; 2D vs 3D tradeoff analysis. |

---
