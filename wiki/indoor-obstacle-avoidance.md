# Indoor Obstacle Avoidance and Local Planning

Onboard obstacle avoidance for cluttered indoor flight splits into two tiers: flight-controller-native reactive/simple planners (ArduPilot, PX4) that consume sector-binned distance data, and research-grade companion-computer local planners (EGO-Planner, EGO-Swarm, FASTER) that optimize dynamically-feasible trajectories in real time. For a Jetson-Orin home-tidy build, the practical pattern is FC-native collision-stop as a safety floor plus an Orin-resident gradient/convex planner for actual cluttered navigation.

## Tier 1 — Flight-Controller-Native Avoidance

The FC tier is reactive and cheap: it bins range data into angular sectors and either stops/slides near obstacles or probes for an open heading. It runs on the autopilot itself, needs no map, and works in GPS-denied modes that hold position from vision/optical-flow. *(shipping at scale)* for stop/slide; reactive path-probing *demoed* indoors.

### ArduPilot

**BendyRuler** (`OA_TYPE`=1) is a reactive local planner: it probes many headings out to `OA_BR_LOOKAHEAD` (typ. 5 m) and picks a sufficiently-open direction that still progresses toward the goal, holding `OA_MARGIN_MAX` (typ. 2 m) clearance. `OA_BR_TYPE`=1 searches horizontally; `OA_BR_TYPE`=2 adds vertical (up/down/back) for short obstacles in tight spaces. Obstacle database params (`OA_DB_SIZE`, `OA_DB_EXPIRE`, `OA_DB_ALT_MIN`) track sensed objects; `OA_DB_ALT_MIN` rejects ground returns near home. Active only in AUTO/GUIDED/RTL.

**Dijkstra + BendyRuler** (`OA_TYPE`=3) fuses a global Dijkstra shortest-path around known fences with BendyRuler as the reactive fallback when a proximity obstacle appears mid-path. Dijkstra is too expensive for proximity-driven replanning, so it handles fences only; BendyRuler handles dynamic obstacles. AUTO/GUIDED/RTL only.

**Simple avoidance** (Stop/Slide via `AVOID_BEHAVE`) works in Loiter and AltHold without path planning. In Loiter (GPS/vision velocity known) it shortens the pilot/guided velocity vector so the vehicle cannot be driven into an obstacle, stopping at `AVOID_MARGIN`. In AltHold (no velocity estimate) it converts obstacle distance to a lean angle (`AVOID_DIST_MAX`, `AVOID_ANG_MAX`) that the pilot can override.

**OA code architecture:** `AP_Proximity` collects raw distances and consolidates them into 8 sectors (45° each, sector 0 = forward), building a 2D-vector fence at conservative distance. `AC_Avoidance` consumes that fence and adjusts (shortens) the desired velocity from `AC_Loiter`/Guided. Empty sectors are filled from adjacent ones, yielding a protective "cup"-shaped fence. Sensors feed in via MAVLink `DISTANCE_SENSOR` (single distance, `orientation` 0–7/24/25) or `OBSTACLE_DISTANCE` (array, up to 72 distances) at 10–50 Hz; `PRX_TYPE`/`PRX1_TYPE` enables the source.

**RealSense depth integration:** A non-ROS Python script (`d4xx_to_mavlink.py` from `thien94/vision_to_mavros`) on a companion computer turns a D435/D435i depth image into `OBSTACLE_DISTANCE`. It applies librealsense post-processing filters, divides the camera HFOV into 72 rays, samples depth along one pitch-compensated horizontal line (ATTITUDE-corrected), and streams at ≥10 Hz (~15 Hz typical). FC config: `SERIAL2_PROTOCOL`=2, `SERIAL2_BAUD`=921, `PRX1_TYPE`=2 (MAVLink), `AVOID_ENABLE`=7. Camera mounts forward-only; reference companion is an UP Squared running APSync (RPi4 unsupported). Tunables: `obstacle_line_height_ratio` (raise the scan line off the ground), `obstacle_line_thickness_pixel` (noise robustness). Pairs with a T265 for non-GPS pose. *(demoed)* in Loiter/AltHold square-pattern flights.

### PX4

**Collision Prevention** slows/stops the vehicle in acceleration-based Position mode (`MPC_POS_MODE`=Acceleration based). It fuses all sources into a 72-sector (docs also cite 36) map around the vehicle, restricts velocity so the craft stops within `CP_DIST`, and — critically — **blocks motion in any direction lacking sensor data** unless `CP_GO_NO_DATA`=1. Key params: `CP_DIST` (min distance, negative disables), `CP_DELAY` (sensor + setpoint-tracking delay, ext-vision ~0.2 s), `CP_GUIDE_ANG` (auto-nudge around obstacles, ~30° good balance). Velocity limiting respects the jerk-optimal controller (`MPC_JERK_MAX`, `MPC_ACC_HOR`, `MPC_XY_VEL_P_ACC`). No range data 0.5 s → no movement; 5 s → HOLD. Sources: FC-attached rangefinders (`distance_sensor` topic), rotary lidars (SF45, 320°, write `obstacle_distance` directly), or a companion via ROS2/`OBSTACLE_DISTANCE` (~10 Hz, tested at 4 m/s). Companion path is noted **untested/archived**.

**ROS2 offboard control** is the bridge for an Orin planner to command PX4. Via uXRCE-DDS + `px4_ros_com`/`px4_msgs`, a node streams `OffboardControlMode` + `TrajectorySetpoint` (NED frame — no implicit ENU conversion) at ≥2 Hz, then sends `VehicleCommand` to switch to offboard and arm. Setpoints (`x,y,z,yaw`) can be driven by another node's output. This is how a companion-side planner closes the loop with PX4.

**PX4-Avoidance** (ROS1 Noetic, **unmaintained/archived**) ships three standalone nodes: `local_planner` (3DVFH+/VFH+\* vector-field histogram, lower compute, no global memory), `global_planner` (octomap occupancy-grid graph search, needs accurate global pose), and `safe_landing_planner` (terrain flatness from downward pointcloud z-stats). Input is `sensor_msgs/PointCloud2` (official camera: RealSense D435); MAVROS bridges PX4↔ROS. Enable with `COM_OBS_AVOID`. Tested companions: local on Intel NUC / Jetson TX2 / Intel Atom; global on Odroid. Healthy processed-cloud rate 10–20 Hz. Use USB2 for the camera to avoid GPS/RF interference.

## Tier 2 — Companion-Computer Local Planners

These run on the Orin-class companion, build a local map, and optimize a smooth, dynamically-feasible trajectory replanned at multi-Hz when new obstacles appear. They command the FC via offboard setpoints (Tier-1 PX4/ArduPilot offboard interface). All ZJU/MIT work is open-source ROS. *(demoed)* in real cluttered/forest flight; not *shipping at scale* in consumer products.

### EGO-Planner (arXiv 2008.08835)

ESDF-free gradient-based local planner. Insight: building a Euclidean Signed Distance Field is the bottleneck (~70% of planning time per EWOK) yet the trajectory covers only a sliver of the ESDF's updated volume. Instead of querying a precomputed ESDF, EGO formulates the collision penalty by comparing a colliding B-spline segment against an A\*-found collision-free guiding path, storing obstacle info only when the trajectory hits *new* obstacles. It optimizes smoothness + collision + dynamical-feasibility terms over a cubic uniform B-spline (~25 control points, ~7 m horizon, ~0.3 m spacing) with an L-BFGS solver (beats BB and truncated-Newton on speed/success), then re-allocates time and anisotropic-curve-fits if dynamic limits are violated. **Total planning ~1 ms** *(claimed)*, >1 order of magnitude faster than ESDF methods (Fast-Planner, EWOK), at slightly higher energy cost. Real-world tests used a RealSense D435 with a modified ROS driver strobing the laser emitter every other frame for clean depth + binocular images. ROS package `ZJU-FAST-Lab/ego-planner` (built on Fast-Planner; LBFGS-Lite; ROS1 16.04–20.04). Note: authors recommend EGO-Swarm even for single-drone use (`drone_id`=0); ROS2 lives on the swarm repo's `ros2_version` branch.

### EGO-Swarm (arXiv 2011.04183)

Decentralized, asynchronous multi-UAV extension of EGO-Planner using only onboard resources — no external localization, no pre-built map. Adds two pieces over EGO-Planner: a lightweight **topological trajectory generation** front-end to escape local minima (a known failure of pure gradient methods when the camera can't see behind an obstacle), and a **decentralized swarm framework** robust to unreliable, bandwidth-limited comms. Agents broadcast new collision-free trajectories; reciprocal avoidance is a weighted swarm-collision penalty in the same optimization. Relative VIO drift between agents is corrected via agent detection in depth images. Plans in "several ms." Real-world: indoor at 1.5 m/s, forest at 1.5–2 m/s, drone radius 0.2 m. Single-agent system inherits EGO-Planner's hardware. Repo `ZJU-FAST-Lab/ego-planner-swarm` (has the ROS2 branch). For a single home drone this is the recommended entry point. *(synthesis: the topological front-end is the relevant upgrade for a one-drone indoor build; swarm/broadcast machinery is unused.)*

### FASTER (arXiv 2001.04420)

Convex-decomposition MIQP planner optimizing for **speed without sacrificing safety**. Partitions space into free-known (F), occupied-known (O), unknown (U). It plans a fast trajectory through F∪U (free-known *and* unknown) while always retaining a **safe back-up trajectory** that terminates and stops inside known-free space — so a feasible safe option exists indefinitely (MPC-style safety guarantee), avoiding the conservative "stop in free-known only" limit. Front-end is Jump Point Search (JPS) on a uniform grid; a convex decomposition builds overlapping polyhedra around the JPS path; the **MIQP** (solved with **Gurobi**, a commercial solver) lets the solver choose interval *and* time allocation rather than ad-hoc fixing them. Hardware: velocities up to **7.8 m/s** in unknown cluttered environments (2× prior SOTA); platform was a Qualcomm SnapDragon Flight + **Intel NUC i7DNK** + **RealSense D435** — perception on the RealSense, mapper+planner on the NUC, control on the SnapDragon. Repo `mit-acl/faster` (ROS Kinetic/Melodic; uses JPS3D + DecompROS). *(demoed)* outdoor/forest at high speed.

## Map representations and what runs where

- **No map (sector bins):** ArduPilot `AP_Proximity` 8 sectors, PX4 72-sector `obstacle_distance`. Reactive only; runs on the FC.
- **Occupancy / octomap:** PX4-Avoidance global planner, FASTER's known/unknown decomposition. Needs good global pose; companion-side.
- **ESDF:** classic gradient planners (Fast-Planner, EWOK). Expensive — the cost EGO explicitly removes.
- **ESDF-free guiding-path:** EGO-Planner/Swarm. Cheapest map-based option; ~1 ms plans; companion-side.
- **Convex polytope decomposition:** FASTER. Companion-side; requires a (commercial) MIQP solver.

## Build notes *(synthesis / recommendation)*

For the Phase-1 indoor home-tidy build (PX4/ArduPilot FC + Jetson Orin + ROS2), a two-layer stack is the pragmatic call:

- **Safety floor on the FC:** enable PX4 Collision Prevention (or ArduPilot simple Stop/Slide) as a hard reactive backstop independent of the companion. It catches companion crashes/hangs — relevant given Orin compute can stall. Keep `CP_GO_NO_DATA`=0 (default-deny in unsensed directions) for an indoor build with limited FOV.
- **Navigation on the Orin:** EGO-Swarm (single-agent, `drone_id`=0, ROS2 branch) is the best-fit local planner — ESDF-free ~ms planning suits Orin's budget, the topological front-end handles the dead-ends a cluttered house produces, and it's MIT/Apache-style open ROS. FASTER is faster but pulls in a **Gurobi license dependency** and targets high speeds irrelevant indoors; PX4-Avoidance is archived/ROS1. EGO-Swarm → PX4 closes via ROS2 offboard `TrajectorySetpoint` (mind NED vs ENU).
- **Sensor:** RealSense D435/D435i is the common denominator across every Tier-1 and Tier-2 option here (depth + the emitter-strobe driver trick for EGO). A forward depth camera gives ~<90° FOV → an unsensed-direction policy and/or added side/rear coverage is needed for free indoor motion. Pose for the planners comes from a VIO/SLAM source, not GPS (see related pages). Budget Orin VRAM/CPU for depth + VIO + planner concurrently.
- **Open gap:** none of the Tier-2 planners is *shipping at scale* in a consumer indoor product; all are research/demo maturity. Reliability of VIO-fed local planning in featureless/low-light indoor scenes is the practical risk, not the planner math.

## Source

- `01-ardupilot-bendyruler.md` — ArduPilot BendyRuler OA params and horizontal/vertical types — https://ardupilot.org/copter/docs/common-oa-bendyruler.html
- `02-ardupilot-dijkstra.md` — Dijkstra+BendyRuler fusion (`OA_TYPE`=3) — https://ardupilot.org/copter/docs/common-oa-dijkstrabendyruler.html
- `03-ardupilot-oa-code.md` — OA code architecture: `AP_Proximity` sectors, `AC_Avoidance`, DISTANCE_SENSOR ingest — https://ardupilot.org/dev/docs/code-overview-object-avoidance.html
- `04-ardupilot-realsense.md` — RealSense D435 → `d4xx_to_mavlink.py` OBSTACLE_DISTANCE pipeline, FC params, tuning — https://ardupilot.org/copter/docs/common-realsense-depth-camera.html
- `05-px4-collision-prevention.md` — PX4 Collision Prevention algorithm, CP_* params, sector map, companion/rangefinder sources — https://docs.px4.io/main/en/computer_vision/collision_prevention
- `06-px4-ros2-offboard.md` — PX4 ROS2 offboard control (OffboardControlMode/TrajectorySetpoint, NED, uXRCE-DDS) — https://docs.px4.io/main/en/ros2/offboard_control
- `07-px4-avoidance.md` — PX4-Avoidance local/global/safe-landing planners, MAVROS message flow, companions — https://github.com/PX4/PX4-Avoidance
- `08-ego-planner-arxiv.md` — EGO-Planner paper: ESDF-free gradient B-spline optimization, ~1 ms, L-BFGS — https://arxiv.org/pdf/2008.08835
- `09-ego-planner-gh.md` — EGO-Planner repo: build, CUDA local_sensing, emitter-strobe RealSense driver — https://github.com/ZJU-FAST-Lab/ego-planner
- `10-ego-swarm-arxiv.md` — EGO-Swarm paper: decentralized topological planning, VIO-drift correction, indoor 1.5 m/s — https://arxiv.org/pdf/2011.04183
- `11-faster-arxiv.md` — FASTER paper: convex-decomposition MIQP, safe back-up trajectory, 7.8 m/s, NUC+D435 — https://arxiv.org/pdf/2001.04420
- `12-faster-gh.md` — FASTER repo: Gurobi MIQP dependency, JPS3D/DecompROS, build/launch — https://github.com/mit-acl/faster

## Related

- [[drone-autonomy-state]]
- [[drone-sensors-for-autonomy]]
- [[lidar-for-uav-autonomy]]
- [[visual-inertial-slam]]
- [[indoor-cluttered-slam]]
- [[safe-indoor-flight]]
- [[detect-and-avoid]]
- [[home-tidy-drone-prototype]]
- [[slam-fc-integration]]
- [[fast-lio-mid360-orin]]
- [[gps-denied-hover-land]]
- [[payload-budget]]
- [[robot-vacuum-navigation]]
- [[lidar-vs-vision-autonomy]]
