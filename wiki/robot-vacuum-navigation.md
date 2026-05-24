# Robot Vacuum Navigation

Precedent study: how mass-market robot vacuums localize, map, and systematically cover a home, and which parts of that stack transfer to an indoor home-tidy drone (FC + Jetson Orin + ROS2, GPS-denied). The headline lesson: cheap 2D laser-distance SLAM fused with wheel dead-reckoning is a *shipping-at-scale* proof that a home can be mapped and re-localized into with a sub-$30 sensor and a microcontroller-class compute budget — but the wheel-odometry crutch is exactly the input a flying robot does not have.

---

## Why vacuums are a precedent

Robot vacuums are the only mobile robot fleet that has shipped autonomy into *millions* of unstructured homes. iRobot quotes "close to double digit millions a year of Roombas sold" and "one of the largest installed fleets of machine-learning-capable devices in the world" [`03-spectrum-roomba-j7.md`]. The LiDAR-SLAM survey explicitly names indoor sweepers as the canonical 2D-LiDAR-SLAM application [`11-lidar-slam-survey-arxiv.md`]. So the navigation choices vacuums converged on are validated against the same hard problem a home drone faces: GPS-denied, cluttered, dynamic, low-light, consumer price point — minus the third dimension and the dead-reckoning luxury.

The stack splits into three layers that recur across every vendor: **localization+mapping** (LDS/LiDAR SLAM vs camera VSLAM), **obstacle avoidance** (structured-light / ToF, often a separate sensor from the nav layer), and **coverage + return-to-dock** behavior built on a persistent map.

---

## Sensor lineage 1 — spinning LDS / 2D LiDAR SLAM

The defining low-cost mass-market navigation sensor. *Shipping at scale.*

- **Neato XV-11 / D7 spinning LDS.** The Neato laser module is the seminal cheap LDS. The Hackaday/Hizook teardown traces it to a ~$30 BOM design (ICRA 2008 "A Low-Cost Laser Distance Sensor") that pairs a laser diode with an offset CMOS line-scan imager (a Panavision DLIS-2K) and triangulates — i.e. it is technically a triangulating rangefinder, not time-of-flight, but reports usable 360° range for mapping regardless [`06-hackaday-neato-lidar.md`]. A Neato employee "helped fit the SLAM algorithm on a microcontroller" — the key affordability proof [`06-hackaday-neato-lidar.md`].
- **Neato D7 teardown.** Single-plane scan at the height of the laser/sensor, optimal at ~2 ft range. Because the scan is one plane, the D7 needs "about a dozen other sensors" (bump switches, cliff, wheel encoders) to avoid getting stuck or lost — the LiDAR alone is not enough [`05-neato-d7-teardown.md`]. Wheel odometry is a magnetic encoder disk + Hall sensor giving 45° shaft resolution per wheel. The whole LiDAR module spins; power crosses the rotating joint by inductive coupling and data by an optical (LED/photodiode) link rather than a slip ring. Maps and no-go lines require the cloud connection; raw vacuuming works offline [`05-neato-d7-teardown.md`].
- **Roborock S8 dToF LDS.** Roborock pioneered LDS mass production from 2016 and pushed it as the standard sweeper config [`08-eejournal-roborock-tof.md`]. The S8 turret is a true **dToF** (direct time-of-flight) LDS spinning at ~300 RPM, generating a point cloud; dToF holds a static error margin with range whereas triangulation degrades with distance. SLAM is solved with probabilistic methods (the teardown speculates GraphSLAM / particle filters) and runs locally on an onboard NPU, though map storage often still pings the cloud [`04-roborock-s8-deepdive.md`].

This lineage maps directly onto the survey's 2D-LiDAR-SLAM canon: FastSLAM and GMapping (particle-filter), Karto (first open-source graph optimization), Hector (odometry-free Gauss-Newton — notable because it works *without* wheel encoders), Cartographer (5 cm grid, real-time loop closure), and SLAM Toolbox (lifelong/multi-session) [`11-lidar-slam-survey-arxiv.md`].

---

## Sensor lineage 2 — camera VSLAM

iRobot's path; trades laser hardware for a cheap camera plus compute. *Shipping at scale.*

- **Roomba 980 — ceiling-facing VSLAM.** A single ~75-cent camera aimed forward/up at ~45° tracks distinctive pixel features (corners) and fuses them with a new bottom-mounted odometry sensor plus gyro/IMU; VSLAM runs on custom DSPs rather than a full computer to hold cost [`01-spectrum-roomba980.md`]. The failure mode is explicit: under tables/couches/beds, trackable features vanish and the robot must re-localize or stitch a new map fragment to the old one [`01-spectrum-roomba980.md`].
- **Roomba i7 — persistent ("Imprint") maps.** Memory/processing/mapping upgrade that makes the map *persistent and re-usable* across runs — the enabler for selective room cleaning and resume-after-recharge. iRobot frames the generation-over-generation shift as increasingly software-driven [`02-spectrum-roomba-i7.md`].
- **Roomba j7 — front RGB camera for obstacle classification.** First Roomba with a *front-facing visible-light* camera doing on-robot object detection (cords, shoes, socks, pet waste, its own dock), trained on >1M labeled images from >1000 homes; a front LED aids low-contrast cord detection [`03-spectrum-roomba-j7.md`]. Classification is on-robot; only obstacle-query images leave the device (end-to-end encrypted), and a separate on-robot human detector deletes images containing people. iRobot CEO's thesis: "the primary sensor for a robot should be a vision system… the end state of a Roomba is going to be a hundred percent vision," with 3D range sensing only "a crutch" [`03-spectrum-roomba-j7.md`] — a direct, on-the-record statement of the vision-vs-LiDAR position relevant to [[lidar-vs-vision-autonomy]].

Note the architecture split: even on the camera-first j7, navigation/mapping and obstacle-classification are *different cameras for different jobs*. The Robot Report confirms the general VSLAM/LiDAR weakness: lose lighting (under furniture) and the map can't be read; relocalize-after-kidnap ("lift and place") requires wandering until a wall is re-traced [`09-robotreport-sensors.md`].

---

## Sensor lineage 3 — structured-light / ToF obstacle avoidance

A dedicated collision layer, decoupled from the navigation layer, increasingly a 3D ToF imager. *Shipping at scale.*

- **Dreame W10 Pro — Infineon REAL3 / pmd ToF camera.** A 3D ToF imager (~38,000 pixels, per-pixel distance) gives a tall vertical FoV to measure furniture height and slip under it, identify cords/shoes/slippers/socks, and — via pmd's per-pixel SBI (Suppression of Background Illumination) — work in strong sunlight, dim light, and varied reflectivity [`07-pmd-dreame-w10.md`].
- **Roborock Qrevo Slim — hybrid ToF (hToF) replacing the LDS turret.** Roborock + Infineon + pmd + OMS combine the REAL3 imager, dual-IR illumination, and pmd processing into one camera module that does SLAM + obstacle avoidance + cliff detection together — explicitly replacing the separate LDS turret and obstacle module. Eliminating the turret drops body height from ~100 mm to 82 mm. Open-source SLAM on hToF depth needs only **one Cortex-A55 core** for depth + SLAM out of eight available [`08-eejournal-roborock-tof.md`]. This is the convergence point: the nav and collision layers fold into a single low-compute 3D depth sensor.
- **Roborock S8 — structured-light "Reactive 3D" collision layer.** Projects an IR grid; pattern deformation flags 3D obstacles vs flat floor in zero-lux, deliberately chosen over an RGB camera for low-light reliability and privacy. Keeps the nav layer (LiDAR) and collision layer (structured light) separate [`04-roborock-s8-deepdive.md`].

---

## The dead-reckoning + sensor-fusion backbone

Every vacuum, regardless of nav lineage, leans on the same fusion recipe. *Shipping at scale.*

- **Wheel odometry is the dead-reckoning spine.** Magnetic wheel encoders + IMU/gyro give relative pose; the absolute sensor (LiDAR or VSLAM) corrects accumulated drift. The S8 deep-dive describes a Kalman filter that rejects wheel data when the IMU sees zero acceleration and the LiDAR sees a static wall — i.e. it catches wheel slip on rugs, "the difference between a robot that cleans in straight lines and one that wanders diagonally" [`04-roborock-s8-deepdive.md`].
- **IMU holds pose between absolute fixes** and detects the kidnap event (pick-up / rotation) [`09-robotreport-sensors.md`]. For non-SLAM budget vacuums, dead reckoning = wheel rotations + IMU + ToF object detection, full stop — no map at all [`09-robotreport-sensors.md`].
- **Embedded motor controllers** close the loop tightly enough to distinguish a 90° turn from an 88° turn; without that precision the pose diverges quickly [`09-robotreport-sensors.md`].

The survey's framing of *why* fusion is mandatory transfers directly: single sensors (LiDAR, camera, IMU) are "inaccurate and fragile," and 2D LiDAR alone cannot estimate full 6-DOF motion in degenerate/featureless environments (long corridors) — multi-source fusion is the dominant research trend [`11-lidar-slam-survey-arxiv.md`]. EKF-LOAM is the on-point exemplar: it fuses LiDAR SLAM *with wheel odometry and IMU* specifically for confined spaces with few geometric features [`11-lidar-slam-survey-arxiv.md`].

---

## Coverage, persistent maps, and dock-return — the consumer UX baseline

What the localization stack actually buys, and the bar a home drone's UX is implicitly measured against. *Shipping at scale.*

- **Systematic coverage replaces random bounce.** Pre-map vacuums bounced pseudo-randomly and couldn't cover more than ~3 rooms; with localization the 980 vacuums in straight lines, cleans a whole multi-room level, and crucially **remembers where it left off** [`01-spectrum-roomba980.md`]. (iRobot's hedge: random multi-pass coverage can clean carpet better — coverage completeness vs single-pass efficiency is a real tradeoff, not a settled win [`01-spectrum-roomba980.md`].)
- **Persistent saved maps + selective tasking.** The i7's persistent map enables "clean this specific room" and resume-after-charge [`02-spectrum-roomba-i7.md`]. Re-localization into a saved map is the load-bearing capability; "lift and place" breaks it until the robot re-traces a wall [`09-robotreport-sensors.md`].
- **Autonomous dock-return + recharge + resume.** Battery SoC (coulomb counters + thermistors) triggers return-to-base; after charge the robot drives back to its last position and continues [`09-robotreport-sensors.md`]. The i7+/j7+ Clean Base adds precision re-docking *and* auto-evacuation — iRobot calls aligning the robot's evacuation port to the dock port one of its hardest engineering problems [`02-spectrum-roomba-i7.md`]. Docking precision and auto-rearm are exactly the home-drone problems in [[precision-docking-recharging]].

---

## Indoor-UAV context — what changes in the air

The arXiv indoor-UAV work shows the same fusion recipe ported to a flying frame, and where it strains. *Demoed* (lab/confined-space).

- **Macquarie indoor UAV (RTAB-Map).** ZED 2i depth + IMU + RPLidar A1M8 (single-line 2D laser) on a Jetson Nano + Pixhawk/ArduPilot, all onboard, fused via RTAB-Map (appearance-based loop closure, multi-session) in ROS; switches to `Guided_No_GPS` mode when position error is in tolerance [`10-indoor-uav-fusion-arxiv.md`]. Results: navigation accuracy down to 0.4 m, map RMSE 0.13 m in a ~7×7×5 m space — and accuracy *monotonically improves* as you add modalities (mono cam 0.7 m → depth+IMU 0.5 m → +LiDAR 0.4 m), at the cost of more watts and grams [`10-indoor-uav-fusion-arxiv.md`]. The same 2D-LiDAR SLAM (Hector) that runs on vacuums runs here.
- **LiDAR-SLAM survey, aerial framing.** Hector SLAM is explicitly odometry-free and "appropriate for aerial" use — the algorithmic answer to a drone's missing wheel encoders [`11-lidar-slam-survey-arxiv.md`]. For UAV-grade 6-DOF the field has moved to tightly-coupled LiDAR-inertial odometry — LIO-SAM, FAST-LIO / FAST-LIO2 / Faster-LIO (iESKF, incremental voxels), Point-LIO for aggressive motion — and to LiDAR-visual-inertial (LVI-SAM, FAST-LIVO) when geometry alone degenerates [`11-lidar-slam-survey-arxiv.md`]. PULSAR even spins the entire UAV body to widen a single LiDAR's FoV [`11-lidar-slam-survey-arxiv.md`]. This is the bridge to [[fast-lio-mid360-orin]].

---

## Transfer to an indoor drone *(synthesis)*

Reading the vacuum stack against the Phase-1 home-tidy drone ([[home-tidy-drone-prototype]]). Claims above are sourced; the inferences here are mine.

1. **The existence proof is solid: a home is mappable with cheap 2D laser + dead-reckoning.** Vacuums prove — at fleet scale, at a $30 sensor and microcontroller compute budget — that 2D LDS SLAM fused with relative odometry produces a persistent, re-localizable home map. A drone does not need a Velodyne or a GPU-bound dense SLAM to map an apartment; the bar is much lower than the autonomous-car literature implies.

2. **The drone loses the single most load-bearing vacuum input: wheel odometry.** Every vacuum's drift correction rests on wheel encoders giving cheap, reliable relative pose between absolute fixes — and even then needs an IMU/LiDAR cross-check to reject slip. A drone has *no* contact odometry. It must substitute: (a) **optical flow** (downward camera, the closest analog to wheel odometry); (b) **LiDAR-inertial odometry** (LIO — LIO-SAM / FAST-LIO class) as the absolute+relative backbone; and/or (c) **fiducials** (AprilTag-class) for bounded re-localization, especially near the dock. Hector SLAM and the LIO family exist precisely because they drop the wheel-encoder assumption — they are the algorithmic transfer path.

3. **2D is not enough in the air — but the *fusion architecture* still transfers.** Vacuums get away with a single horizontal scan plane because they live on the floor; a hovering drone needs 6-DOF and altitude, so 2D LDS becomes 3D LIO (the survey's degenerate-corridor warning applies doubly to a featureless room at hover height). What transfers is the *recipe*: an absolute mapping sensor drift-corrected by a high-rate IMU, with a separate cheap depth/ToF layer for collision — the same nav-layer / collision-layer split Roborock and iRobot both ship.

4. **The collision layer is a solved, cheap, transferable module.** The Infineon/pmd REAL3 hToF result is the standout for SWaP: SLAM + obstacle avoidance + cliff detection in one compact zero-lux module needing a *single Cortex-A55 core*. A sub-100 mm vacuum already carries this; it is directly adoptable as a drone's forward obstacle sensor and is far lighter than the ZED-class stereo the Macquarie UAV used.

5. **Vision-first vs LiDAR-first is genuinely contested, and the consumer trend leans both ways at once.** iRobot bets pure vision; Roborock keeps dToF/structured-light for low-light and privacy and is now folding nav+collision into one ToF imager. For an indoor drone that must hover reliably under furniture and at night, the low-light robustness of (d)ToF is a strong argument against vision-only — but vision is what gives semantic obstacle classification (j7-style cord/shoe/clutter detection), which a *tidy* drone needs more than a vacuum does. The likely answer is hybrid, mirroring the eventual vacuum convergence. See [[lidar-vs-vision-autonomy]], [[visual-inertial-slam]], [[lidar-for-uav-autonomy]].

6. **Persistent maps + dock-return define the consumer UX floor.** Vacuums set the expectation a home robot must meet: build a map once, re-localize into it every run, take "clean this room" commands, and autonomously return to dock, recharge, and resume. For the drone this maps onto saved-map re-localization ([[slam-fc-integration]] for the map↔FC handoff), semantic room/object memory ([[semantic-object-memory]]), and precision auto-docking ([[precision-docking-recharging]]). The j7's >1M-image obstacle dataset also previews the data-flywheel a fleet of home drones would need — and the on-robot human-detector/auto-delete privacy pattern is a ready-made template.

7. **Hardest unsolved transfer: GPS-denied hover/land stability under the same constraints.** Vacuums never have to *stay up*; pose error just makes them wander, not fall. A drone must hold a stable hover and land on the same cheap sensor budget while bleeding battery faster than any vacuum. That is the binding constraint, treated in [[gps-denied-hover-land]] and [[indoor-cluttered-slam]].

---

## Source

| File | Origin / Vendor | Title | Notes |
|---|---|---|---|
| `raw/research/robot-vacuum-navigation/01-spectrum-roomba980.md` | IEEE Spectrum · spectrum.ieee.org/irobot-brings-visual-mapping-and-navigation-to-the-roomba-980 | *iRobot Brings Visual Mapping and Navigation to the Roomba 980* | Ceiling/forward 75¢-camera VSLAM on DSPs; straight-line coverage; resume-after-charge; multi-pass vs single-pass tradeoff |
| `raw/research/robot-vacuum-navigation/02-spectrum-roomba-i7.md` | IEEE Spectrum · spectrum.ieee.org/qa-irobot-roomba-i7 | *Q&A: How iRobot Engineered Its New Roomba i7+ and Clean Base* | Persistent "Imprint" maps; selective room cleaning; auto-evacuation dock; software-driven generations |
| `raw/research/robot-vacuum-navigation/03-spectrum-roomba-j7.md` | IEEE Spectrum · spectrum.ieee.org/irobot-roomba-j7 | *With New Roomba j7, iRobot Wants to Understand Our Homes* | Front RGB camera, on-robot obstacle classification (>1M images); CEO vision-first thesis; on-robot human-detector privacy pattern |
| `raw/research/robot-vacuum-navigation/04-roborock-s8-deepdive.md` | reversetobuild.com/roborock-s8-lidar-slam-algorithm-analysis | *Roborock S8 Deep Dive: Inside the SLAM & LiDAR Architecture* | dToF LDS @300 RPM; Kalman fusion (LDS+encoder+IMU) rejecting wheel slip; structured-light "Reactive 3D" collision layer; local NPU SLAM |
| `raw/research/robot-vacuum-navigation/05-neato-d7-teardown.md` | MicrocontrollerTips · microcontrollertips.com/teardown-d7-robot-vacuum-from-neato-robotics-faq | *Teardown: D7 robot vacuum from Neato Robotics* | Single-plane spinning LDS (inductive power, optical data link, no slip ring); Hall-encoder wheel odometry; ~dozen aux sensors; cloud-gated maps |
| `raw/research/robot-vacuum-navigation/06-hackaday-neato-lidar.md` | Hackaday · hackaday.com/2011/09/12/digging-deep-into-the-neatos-lidar-module | *Digging Deep Into The Neato's LIDAR Module* | XV-11 module teardown; ~$30 BOM triangulating rangefinder (DLIS-2K imager); SLAM fit onto a microcontroller |
| `raw/research/robot-vacuum-navigation/07-pmd-dreame-w10.md` | pmdtechnologies (press) · pmdtec.com | *Advanced obstacle avoidance and smart navigation in DREAME's W10 Pro* | Infineon REAL3 3D ToF (~38k px); tall vertical FoV; pmd SBI for sun/dim/varied-reflectivity; cord/shoe/sock ID |
| `raw/research/robot-vacuum-navigation/08-eejournal-roborock-tof.md` | EEJournal (press) · eejournal.com | *Roborock uses hybrid Time-of-Flight by Infineon and pmd for sweeping/mopping robots* | hToF (Qrevo Slim) replaces LDS turret; SLAM+OA+cliff in one module; 1 Cortex-A55 core; 100→82 mm height; LDS mass-prod since 2016 |
| `raw/research/robot-vacuum-navigation/09-robotreport-sensors.md` | The Robot Report (Invensense/TDK) · therobotreport.com/sensor-breakdown-how-robot-vacuums-navigate-and-clean | *Sensor breakdown: how robot vacuums navigate* | VSLAM/LiDAR vs dead-reckoning; IMU + wheel encoders; kidnap relocalization; ToF/ultrasonic; dock-return + recharge + resume; SoC sensing |
| `raw/research/robot-vacuum-navigation/10-indoor-uav-fusion-arxiv.md` | arXiv 2410.20599 (ICST 2023) · arxiv.org/html/2410.20599v1 | *Sensor Fusion for Autonomous Indoor UAV Navigation in Confined Spaces* | ZED 2i + IMU + RPLidar on Jetson Nano + Pixhawk; RTAB-Map; 0.4 m nav / 0.13 m RMSE; accuracy scales with added modalities; Guided_No_GPS |
| `raw/research/robot-vacuum-navigation/11-lidar-slam-survey-arxiv.md` | arXiv 2311.00276 · arxiv.org/pdf/2311.00276 | *LiDAR-based SLAM for robotic mapping: state of the art and new frontiers* | 2D/3D/spinning-actuated taxonomy; sweepers = canonical 2D-SLAM; Hector (odom-free, aerial); FAST-LIO/LIO-SAM/EKF-LOAM; fusion-mandatory framing |

---

## Related

[[home-tidy-drone-prototype]] (parent — the build this precedent informs) · [[gps-denied-hover-land]] (the binding aerial constraint vacuums never face) · [[fast-lio-mid360-orin]] (the LIO backbone that substitutes for wheel odometry) · [[precision-docking-recharging]] (dock-return + recharge + resume as consumer UX baseline) · [[indoor-cluttered-slam]] (same problem, in 3D and dynamic) · [[slam-fc-integration]] (map↔flight-controller handoff) · [[visual-inertial-slam]] · [[lidar-for-uav-autonomy]] · [[drone-sensors-for-autonomy]] (sensor menu for the air) · [[semantic-object-memory]] (j7-style object/room memory) · [[indoor-obstacle-avoidance]] (the decoupled collision layer) · [[lidar-vs-vision-autonomy]] (iRobot vision-first vs Roborock ToF-first, on the record)
