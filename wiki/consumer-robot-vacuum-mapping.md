# Consumer Robot Vacuum Floor Mapping (2023–2026)

Deep-dive into how production top-tier robot vacuums actually build and maintain floor plans — room segmentation, map update when furniture moves, multi-floor architecture, obstacle classification, and the gap vs a SLAM Toolbox + 2D LiDAR research build. Five specific vendors examined: Roborock S8 MaxV Ultra, Dreame L20 Ultra / X40 Ultra, iRobot Roomba j9+ / Combo j9+, Dyson 360 Vis Nav, Ecovacs Deebot X5 Pro. These are the closest production analogues to what we're building — millions of units, real home environments, maps that persist across sessions.

Companion to [[robot-vacuum-navigation]] (which covers the foundational sensor lineages and transfer-to-drone analysis). This page documents the five specific questions that page leaves open.

---

## Q1 — Room segmentation: what algorithm, what sensors drive it?

### The occupancy-grid pipeline

All LiDAR-equipped vacuums converge on the same segmentation pipeline: (1) build a 2D occupancy grid from LiDAR SLAM, (2) post-process it into semantic rooms. The sensor that drives this is the LDS/LiDAR turret — the same one used for SLAM — not a separate sensor.

**iRobot RoomsSeg** (presented at IROS 2017) is the most technically documented production approach. IEEE Spectrum coverage of the IROS paper describes it as: automated clutter removal on the occupancy grid → watershed segmentation → merging of segmented regions by semantic decision rules. The decision rules are explicit: corridors are "regions typically of similar width relative to the main direction of the corridor"; rooms are recognized based on "what large open regions are attached to each other, if the connections between them are larger than the average doorway." The paper reported that room-by-room cleaning (82% total time vs conventional, 63% path-following time, 66% turning time) is the efficiency payoff. RoomsSeg was designed to run entirely on-robot, avoiding cloud round-trips — at the time, "using the kind of CPU power that even old Roombas have" [`01-02-spectrum-irobot-roomsseg.md`].

**Roborock** does not publish the algorithm name but third-party analysis speculates GraphSLAM or particle filters for localization with a watershed-like step applied to the resulting occupancy grid for room division. The operator-facing experience mirrors iRobot: the robot auto-divides the map after a mapping run, then prompts the user to confirm/edit room labels in the app. The room-division step runs locally on the onboard NPU [`09-09-reversetobuild-roborock-slam.md`; `room-segmentation/01-roborock-nav-explainer.md`].

**The academic state of the art** is ROSE² (RObust StructurE identification and ROom SEgmentation), arXiv 2203.03519, Luperto et al. 2022. ROSE² is relevant because it characterizes exactly the failure mode that makes room segmentation hard in real home maps: "the lidar commonly placed close to the floor level perceives and adds to the map non-structural objects such as legs of tables and chairs, bags, noise due to reflections caused by mirrors and glass walls." ROSE² solves this by a two-step method:
1. **Map cleaning via DFT**: computes a 2D Discrete Fourier Transform of the occupancy map, identifies "dominant directions" (the finite set of wall orientations in human-built environments), retains only those frequencies, and scores each cell by its contribution to structure vs clutter. This filters out furniture legs, mirror reflections, etc.
2. **Room detection from clean map**: groups wall segments along dominant directions, builds a clean geometric floor-plan-like representation, then segments into rooms. The method requires no training on the specific environment and runs online [`10-10-rose2-room-segmentation-arxiv.md`].

The ROSE² paper frames this as still an "open problem" — implying that production vacuums all live with imperfect room segmentation on cluttered maps, and that the research community hasn't settled on a production-grade solution.

### Sensor split: LiDAR for rooms, camera for objects

A consistent pattern across all LiDAR-equipped vendors: the LiDAR/dToF turret handles SLAM + occupancy grid + room segmentation, while a **separate** front-facing camera (RGB or structured light) handles object/obstacle classification. These are architecturally decoupled layers, not a unified sensor.

- **Roborock S8 MaxV Ultra**: dToF LDS at ~300 RPM for SLAM and room mapping; "Reactive 3D" structured-light IR grid (not RGB) for floor-level obstacle detection. Choice rationale per reversetobuild analysis: structured light works at zero-lux (where RGB is blind), and avoids a live video feed (privacy) [`09-09-reversetobuild-roborock-slam.md`].
- **Ecovacs X5 Pro Omni**: dToF laser mapping (no top-turret — integrated into D-shaped front) for SLAM; AIVI 3D 2.0 (960P star-light RGB camera + RGBD sensors) for obstacle classification. Ecovacs terms their navigation model "AINA 2.0 Intelligent Navigation Model" — combining deep learning and reinforcement learning with the dToF sensor for real-time navigation [`14-14-ecovacs-mapping-explainer.md`; `08-09-techradar-ecovacs-x5-pro.md`].
- **Dreame X40 Ultra/L20 Ultra**: LiDAR + "3DAdapt" dual-laser 3D structured light for obstacle avoidance. Dreame claims the structured-light system identifies "up to 200 types of obstacles." Map precision quoted as 2–5 cm [`04-05-dreame-lidar-navigation-blog.md`; `05-06-dreame-multifloor-blog.md`].
- **Dyson 360 Vis Nav**: Camera-only (no LiDAR). A 360-degree fisheye camera on top drives SLAM ("Simultaneous Localization and Mapping system") combined with 26 external obstacle detection sensors and an LED light ring for low-light operation. Consequence: first mapping run takes ~30 minutes for a small 2-room space vs a couple of minutes for LiDAR-based rivals [`07-08-techhive-dyson-vis-nav.md`; `12-12-ambient-dyson-vis-nav.md`].

---

## Q2 — Furniture moving: how long/how many runs before the map updates?

This is where production systems differ significantly from the clean academic story.

**iRobot Roomba (j-series)** uses a "Clean Map Report" update flow: after a clean, the app shows a Clean Map Report which the user can then "apply" to update the Imprint Smart Map. The robot does not update autonomously in real-time. iRobot's documented position: "General clutter such as a pet laying on the floor, shoes, or toys, or minor changes such as a kitchen chair being moved out of the cleaning environment should have no impact on your Imprint Smart Map." For significant furniture rearrangement, iRobot recommends running a "Clean All" job and using the resulting Clean Map Report to update the persistent map. The robot learns the new layout "within several cleaning runs" — a community-sourced consensus of 2–3 runs before map stabilizes [`robot-vacuum-navigation` existing sources; search results corroborating].

**Dreame** documents a "map broken/shifted" troubleshooting guide that reveals the fragility model: if the robot is "lifted mid-clean," it corrupts the pose estimate; if sensors are dusty, the map drifts; if the dock is moved or placed incorrectly (not flush against a wall, or in a narrow niche), the SLAM anchor point is disturbed from the first run. For non-destructive furniture moves, Dreame's guidance is that maps "auto-adjust" over subsequent cleans — but the mechanism (adaptive update during localization) is not documented technically [`06-07-dreame-map-moved-fix.md`].

**The common production architecture** (from reversetobuild analysis of Roborock): SLAM runs locally, building a live map each run. The *persistent saved map* is a stored reference. When re-localizing, the robot matches the live scan against the stored map using ICP or a similar scan-matching step. If furniture has moved, the live scan diverges from the stored reference at those locations, and the map update depends on whether the robot treats divergences as transient (ignore) or persistent (update). Production systems are conservative — they do not overwrite the stored map aggressively, to avoid corrupting a good anchor from a single anomalous run [`09-09-reversetobuild-roborock-slam.md`].

**Practical answer**: minor furniture moves (chair moved out of kitchen, pet in a new spot) → no map impact, robot navigates around the obstacle using its live obstacle-avoidance layer. Major rearrangement (sofa moved, new wall, room restructured) → requires 2–5 runs for the map to stabilize, or a manual "remap" trigger. The robot does not have a change-detection step analogous to POCD (see [[dynamic-object-handling]]); it simply re-localizes as best it can and incrementally overwrites map regions where sufficient new evidence accumulates. *(synthesis)*

---

## Q3 — Multi-floor handling: what is the architecture?

### The stored-map-per-floor model

Every top-tier vendor uses the same architecture: each floor is a separate stored 2D map; the robot carries all saved maps; re-localization on startup determines which map is active.

**Capacity**: Dreame supports 4–5 floor maps in cloud-synced storage; Ecovacs X5 Pro Omni supports 4 floors (from spec sheet) [`08-09-techradar-ecovacs-x5-pro.md`; `05-06-dreame-multifloor-blog.md`].

**Floor recognition**: better models do this passively via SLAM — the robot starts up, does a short localization scan, and matches against its candidate maps to identify which floor it's on. Dreame's X50 Ultra is specifically cited as using "landmark detection" for automatic floor recognition. Cheaper models require a manual floor selection in the app [`05-06-dreame-multifloor-blog.md`].

**The dock problem**: the dock is the SLAM reference anchor (the robot bootstraps its pose from returning to dock). Most systems require the dock to be physically on the floor being cleaned — you can't leave the dock on Floor 1 and vacuum Floor 2 without moving it. Dyson 360 Vis Nav is an outlier: it requires the dock to be moved for multi-floor, and cannot create a map for a new location without relocating the dock. Dreame's multi-floor guide confirms: "you don't need to relocate the dock to the new floor" for the mapping step itself, but the cleaning return-to-home requires a dock on that floor [`05-06-dreame-multifloor-blog.md`; `12-12-ambient-dyson-vis-nav.md`].

**Workflow**: the recommended Dreame setup is: place robot on dock Floor 1, enable multi-floor mapping in app, map Floor 1, pick up robot, carry to Floor 2, create new map, carry back. Each floor gets its own named map. The robot selects the active map when placed on a floor — or you select manually in the app [`05-06-dreame-multifloor-blog.md`].

**No automatic inter-floor relationship**: the 3–5 stored maps are independent 2D maps with no spatial relationship to each other. There is no 3D volumetric representation tying floors together. The robot has no concept of "which room is above which other room." *(synthesis)*

---

## Q4 — Furniture and obstacle classification: can they distinguish a table leg from a wall?

### At SLAM layer: no

For the purposes of building and maintaining the floor plan map, **no** — the 2D LiDAR cannot distinguish a table leg from a wall. Both register as occupied cells in the occupancy grid. This is the central complaint in the ROSE² paper: "the sensor perceives and adds to the map non-structural objects such as legs of tables and chairs, bags, noise due to reflections caused by mirrors and glass walls. Consequently, detecting the structural features, like walls, in such maps could be challenging." The academic fix (ROSE²) uses frequency-domain analysis to infer which occupied cells are likely structural (walls) vs non-structural (furniture). Production vacuums handle this via the room-segmentation decision rules (e.g., iRobot's RoomsSeg heuristics) rather than a principled structural inference step [`10-10-rose2-room-segmentation-arxiv.md`; `01-02-spectrum-irobot-roomsseg.md`].

The practical consequence: the stored floor plan map is "cluttered" — it contains furniture legs, bags, and reflective-surface artifacts as occupied cells. This is tolerated because the robot re-localizes against this same cluttered reference each run, so the map is internally consistent even if not geometrically clean.

### At obstacle-avoidance layer: yes, for named categories

The front-facing camera + AI classifies specific object types, separate from the SLAM map:

- **Roborock S8 MaxV Ultra** (previous-gen S7 MaxV style): RGB camera + 3D structured light + NPU runs YOLOv8-class object detection, identifying shoes, socks, cables, pet waste as specific obstacle classes [`room-segmentation/01-roborock-nav-explainer.md`].
- **Ecovacs AIVI 3D 2.0**: "auto-grade 960P star-light level camera and RGBD sensors" — claims recognition of 30+ types of common indoor obstacles. But per 6-month reviewer: "not great at recognizing cables, shoelaces or small items like pieces of paper towel" in practice [`14-14-ecovacs-mapping-explainer.md`; `08-09-techradar-ecovacs-x5-pro.md`].
- **Dreame 3DAdapt**: claims "up to 200 types of obstacles" with dual-laser 3D structured light. [`05-06-dreame-multifloor-blog.md`].
- **Dyson 360 Vis Nav**: the 360° fisheye camera is used for navigation/SLAM, **not** for smart object avoidance. Per two independent reviews: the obstacle detection is poor — a drying rack caused repeated failed attempts and eventual stuck, a charging cable was sucked up. "Although there's a camera here, it's not used for smart object avoidance, such as cables and pet mess" [`07-08-techhive-dyson-vis-nav.md`; `12-12-ambient-dyson-vis-nav.md`].

**The table-leg problem specifically**: table legs register in the occupancy grid as isolated point clusters (not walls). SLAM-layer navigation routes around them as obstacles. The obstacle-avoidance camera may or may not classify them as "table legs" — but in practice it routes around them as unknown obstacles if they're not in the named-category list. The ROSE² paper proposes filtering table legs *out* of the structural map, not classifying them — the distinction matters: production systems tolerate furniture legs in the map; researchers propose removing them for cleaner floor plans. *(synthesis)*

---

## Q5 — Gap between production robot vacuum maps and SLAM Toolbox + 2D LiDAR

This is the most relevant question for our build. The honest answer is: **smaller than the academic literature implies for occupancy grid quality, larger for semantic/structural understanding.**

### Where production maps are comparable

**Raw occupancy grid accuracy**: Dreame claims 2–5 cm room-layout accuracy for LiDAR-equipped models; the reversetobuild analysis of the Roborock S8 describes the same dToF sensor physics. A SLAM Toolbox + RPLiDAR A3 build on known benchmarks achieves 1–5 cm ATE in indoor environments (see [[2d-lidar-slam]]). So at the raw map-accuracy level, production robot vacuums are in the same range as a research SLAM Toolbox build — the sensor physics are the same (Time-of-Flight ranging, GraphSLAM/particle-filter backend).

**Loop closure**: production vacuums run loop closure (Roborock's approach is described as GraphSLAM or particle filter variants that match current scans against the growing map). SLAM Toolbox uses Ceres-based pose graph optimization with Stein Variational gradient descent. Both solve the drift-correction problem; neither has a clear accuracy advantage at home scale.

**Sensor fusion**: production vacuums fuse LiDAR + wheel encoders + IMU via Kalman filter — the same architecture as EKF-SLAM Toolbox configurations. The key is that the wheel encoders provide continuous dead-reckoning between LiDAR fixes. A drone lacks wheel encoders and must substitute optical flow or LIO (see [[robot-vacuum-navigation]] §Transfer).

### Where SLAM Toolbox builds are ahead

**Map cleanliness / semantic structure**: SLAM Toolbox produces a raw occupancy grid. Production vacuums apply proprietary post-processing (RoomsSeg, Roborock room-division heuristics) to produce labeled room maps. These post-processors are what production vacuums have *on top of* a SLAM Toolbox-equivalent baseline — and as ROSE² documents, they are imperfect at handling cluttered environments.

**Multi-session lifelong mapping**: SLAM Toolbox has built-in multi-session map merging (serialize/deserialize, localization-only mode) tested at 24,000 m² real-time (see [[slam-toolbox]]). Production vacuums handle this by storing separate per-floor maps and re-localizing into them, but don't publish the re-localization success rate under changing conditions.

**Transparency and tunability**: SLAM Toolbox is open-source and tunable (all parameters exposed, ROS 2 compatible, benchmarked). Production vacuum SLAM is closed-source, runs on proprietary NPUs, and cannot be integrated with external planners like Nav2 without reverse-engineering (Valetudo project attempts this).

### Where production vacuums are ahead

**Robustness at consumer scale**: millions of units, every home environment, firmware updated automatically, continuous fleet learning from failed runs. A SLAM Toolbox research build has never been tested in 10 million homes.

**Obstacle avoidance integration**: production systems co-design the SLAM map layer and the obstacle-avoidance camera layer in one product, with the obstacle layer providing real-time updates that don't touch the persistent map (transient obstacle avoidance). A SLAM Toolbox build requires separately integrating a costmap layer (Nav2 STVL or equivalent, see [[ros2-nav2]]).

**Compute efficiency**: Roborock's hToF design (converged LiDAR + obstacle + cliff detection in one module) runs SLAM on a single Cortex-A55 core (per the Roborock Qrevo Slim analysis in [[robot-vacuum-navigation]]). SLAM Toolbox on a Jetson Orin uses multiple cores. The compute gap is closing but production-grade efficiency on a $30 sensor with <1 core is still ahead of research builds at equivalent cost.

### The real gap *(synthesis)*

The gap is not in the SLAM algorithm or raw map accuracy — both achieve 2–5 cm indoor accuracy. The gap is in:

1. **Semantic room labeling**: production vacuums have proprietary pipelines to convert raw occupancy grids into named rooms; SLAM Toolbox produces only grid cells. Adding ROSE²-style room segmentation, or a scene-graph layer (see [[scene-graph-world-model]]), is required to close this gap.

2. **Persistent map update policy**: production vacuums have tuned policies for when to update the saved map vs when to treat a divergence as a transient obstacle. SLAM Toolbox in pure localization mode refuses to update the map at all; in mapping mode it updates unconditionally. A principled change-detection layer (POCD-style, see [[dynamic-object-handling]]) is needed for the same behavior.

3. **The wheel-encoder problem for drones**: vacuums get their dead-reckoning from wheel encoders + IMU. Drones must substitute optical flow or LIO. This is not a gap in map quality per se but in the localization backbone — the drone's map will be comparable in principle once LIO is running (see [[fast-lio-mid360-orin]]).

---

## Vendor summary table

| Vendor / Model | SLAM sensor | Obstacle classifier | Multi-floor maps | Map update on furniture move | Room segmentation | Notes |
|---|---|---|---|---|---|---|
| Roborock S8 MaxV Ultra | dToF LDS, ~300 RPM; GraphSLAM/particle filter | Structured-light IR grid ("Reactive 3D"); no RGB | Yes (≥4 floors) | 2–5 runs; no live remap | Watershed/proprietary; on-robot NPU | SLAM local; map storage cloud (AWS) |
| Dreame L20/X40 Ultra | LiDAR + 3DAdapt dual-laser 3D structured light | 3DAdapt + RGB camera; 200 obstacle types claimed | 4–5 floors; auto-recognize on flagship (X50) | "Auto-adjusts" over subsequent cleans; landmark detection on X50 | Proprietary; on-robot | Map 2–5 cm claimed accuracy |
| iRobot Roomba j9+ | Ceiling-facing VSLAM (camera) | Front RGB camera + >1M labeled images; 30+ object classes | Yes (Imprint Smart Maps) | Manual: run Clean All → apply Clean Map Report to update | RoomsSeg (watershed + semantic rules; IROS 2017) | Vision-only; loses map under furniture in low light |
| Dyson 360 Vis Nav | 360° fisheye camera VSLAM; 26 sensors; LED ring | **None** (navigation camera not used for object avoidance) | Yes; dock must move per floor | Map rebuilds from scratch after dock move | Manual zone split (user prompted) | Worst obstacle avoidance of group; best suction; camera mapping 30 min vs 2 min LiDAR |
| Ecovacs Deebot X5 Pro | dToF (integrated, no top turret); AINA 2.0 nav model | AIVI 3D 2.0: 960P starlight RGB + RGBD; 30+ obstacle types | 4 floors | Adapts over runs; minor tweaks needed after first scan | Proprietary; room division needed after first scan | Struggles with cables/flat small objects in practice |

---

## Source

| File | Origin / Vendor | Title | Notes |
|---|---|---|---|
| `raw/research/consumer-robot-vacuum-mapping/01-02-spectrum-irobot-roomsseg.md` | IEEE Spectrum | *iRobot Testing Software to Make Sense of All Rooms in a House* | RoomsSeg IROS 2017: watershed + semantic rules; 82% efficiency gain; runs on old Roombas |
| `raw/research/consumer-robot-vacuum-mapping/04-05-dreame-lidar-navigation-blog.md` | Dreame US (vendor) | *LiDAR Navigation in Robot Vacuums Explained* | LiDAR vs camera vs gyro comparison; 2–5 cm accuracy; retractable turret designs |
| `raw/research/consumer-robot-vacuum-mapping/05-06-dreame-multifloor-blog.md` | Dreame US (vendor) | *Robot Vacuums for Multi-Floor Homes: Complete Guide* | Multi-floor architecture: 4–5 maps, landmark detection (X50), dock-per-floor workflow |
| `raw/research/consumer-robot-vacuum-mapping/06-07-dreame-map-moved-fix.md` | Dreame US (vendor) | *Why Your Robot Vacuum Map Is Broken And What You Can Do About It* | Map failure modes: dock mis-placement, sensor dust, reflective surfaces, kidnap during clean |
| `raw/research/consumer-robot-vacuum-mapping/07-08-techhive-dyson-vis-nav.md` | TechHive (independent review) | *Dyson 360 Vis Nav review: A major disappointment* | Camera-only nav; 30 min mapping; poor obstacle avoidance; no smart avoidance; 32 min battery |
| `raw/research/consumer-robot-vacuum-mapping/08-09-techradar-ecovacs-x5-pro.md` | TechRadar (independent review, 6-month test) | *Ecovacs Deebot X5 Pro Omni review* | dToF + AIVI 3D 2.0; 4 floors; adapts to furniture movement; struggles with cables/small items |
| `raw/research/consumer-robot-vacuum-mapping/09-09-reversetobuild-roborock-slam.md` | reversetobuild.com (engineering analysis) | *Mapping the Unknown: The Robotics Behind Roborock S8* | dToF physics; Kalman sensor fusion; Reactive 3D structured light vs RGB privacy; cloud map storage |
| `raw/research/consumer-robot-vacuum-mapping/10-10-rose2-room-segmentation-arxiv.md` | arXiv 2203.03519 (Luperto et al., Politecnico di Milano / Örebro, 2022) | *Robust Structure Identification and Room Segmentation of Cluttered Indoor Environments from Occupancy Grid Maps* | ROSE²: DFT-based clutter removal + dominant-direction wall detection; table legs as core failure mode; runs online, no environment-specific training |
| `raw/research/consumer-robot-vacuum-mapping/12-12-ambient-dyson-vis-nav.md` | The Ambient (independent review) | *Dyson 360 Vis Nav review* | Camera SLAM; dock must move per floor; no obstacle avoidance from camera; powerful suction |
| `raw/research/consumer-robot-vacuum-mapping/14-14-ecovacs-mapping-explainer.md` | Ecovacs US (vendor) | *How Does Robot Vacuum Mapping Work* | AINA 2.0 deep learning + RL + dToF; AIVI 3D 2.0 spec; TrueMapping 2.0 (100 m² in 6 min) |
| `raw/research/room-segmentation/01-roborock-nav-explainer.md` | Roborock Newsroom (vendor) | *Understanding How Robot Vacuums Navigate* | LiDAR mass-production since 2016; Reactive AI 2.0 (S7 MaxV): 3D structured light + RGB + NPU |

---

## Related

[[robot-vacuum-navigation]] (foundational sensor lineage and drone-transfer analysis) · [[slam-toolbox]] (the SLAM Toolbox baseline this page compares against) · [[2d-lidar-slam]] (2D LiDAR SLAM algorithms and benchmarks) · [[dynamic-object-handling]] (POCD-style change detection — the missing persistent-map-update layer) · [[scene-graph-world-model]] (semantic room/object layer on top of occupancy grid) · [[indoor-cluttered-slam]] (SLAM in cluttered/dynamic home environments) · [[mapping-stack-design]] (what to build on top of a SLAM baseline for tidy-drone) · [[world-model-architecture]] (the full layered map design for home tidy) · [[ros2-nav2]] (Nav2 costmap layer for real-time obstacle handling)
