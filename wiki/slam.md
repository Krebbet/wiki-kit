# SLAM (Simultaneous Localization and Mapping)

The problem of a robot estimating its own pose (localization) while building a map of an unknown environment at the same time — onboard and GPS-denied. SLAM is the substrate for indoor/GPS-denied drone autonomy on this wiki; this page is a navigation hub tying together the SLAM cluster, since the term is used as assumed-known across many pages. *(synthesis — assembled from existing wiki pages, not a new raw source.)*

## Decomposition

As the wiki uses the term, SLAM is three jobs running concurrently:

- **State estimation (localization)** — the pose/velocity filter or optimizer. OKVIS2 sliding-window optimization at 15 Hz ([[visual-inertial-slam]]); FAST-LIO2's iterated-EKF ([[fast-lio-mid360-orin]]).
- **Mapping** — the persistent geometric/semantic model. supereight2 octree submaps ([[visual-inertial-slam]]); the ikd-tree point map ([[fast-lio-mid360-orin]]); object-level / 3D-Gaussian-splat maps ([[indoor-cluttered-slam]]).
- **Loop closure** — re-recognizing a visited place to correct accumulated drift. Trajectory anchoring ([[visual-inertial-slam]]); semantic loop closure cutting position error 83–93% ([[indoor-cluttered-slam]]).

**Odometry vs full SLAM:** pose estimation without a reusable global map + loop closure is *odometry* (VIO, LIO); add loop closure and a persistent map and it is full SLAM (e.g. FAST_LIO_SLAM extends the FAST-LIO2 odometry front-end — [[fast-lio-mid360-orin]]).

## Sensor front-ends

The choice of front-end is the wiki's central open conflict ([[lidar-vs-vision-autonomy]]):

| Front-end | Sensors | Example pipeline | Strength | Weakness |
|---|---|---|---|---|
| **VIO / VI-SLAM** | camera(s) + IMU | OKVIS2 ([[visual-inertial-slam]]) | light/cheap; rich semantics | fails on featureless/low-light surfaces; short depth range (~6.5 m, *claimed*) |
| **LiDAR-inertial (LIO)** | LiDAR + IMU | FAST-LIO2 ([[fast-lio-mid360-orin]]) | lighting-independent cm geometry; thin-obstacle detection | heavier/pricier; no colour/semantics |

Event cameras are a third sensing path for high-speed/low-light regimes where stereo depth fails ([[event-cameras]]). Cross-sensor SWaP/capability comparison: [[drone-sensors-for-autonomy]].

## On a drone

SLAM output is not the end — the estimated pose is fused into the flight controller's state estimator (ArduPilot EKF3 / PX4 EKF2 via MAVROS `vision_pose`) so the aircraft can hold position, fly waypoints, and take off / land GPS-denied ([[slam-fc-integration]]). Onboard compute gates which methods are deployable: LIO and semantic-landmark methods run on drone-class compute, and as of 2025 even dense 3D-Gaussian-Splatting SLAM has been *demoed* real-time on a Jetson Orin NX (GS-LIVO, ~20 Hz) — it is no longer desktop-only ([[learned-slam]], [[nano-drone-compute]], [[fast-lio-mid360-orin]]). Learning-based SLAM/odometry/depth methods are surveyed in [[learned-slam]].

## Two-phase architecture: map-then-localize

Full SLAM runs two modes that serve different purposes and should not be conflated:

| Mode | Trigger | Rate | Purpose |
|---|---|---|---|
| **Mapping (discovery)** | First entry into a new space | One-off per room | Build the reference: geometry, landmarks, Gaussian scene, or fiducial positions |
| **Localization (working)** | Subsequent entries / ongoing flight | High-rate (20–100 Hz) | Match current frame against the fixed reference → absolute pose with no drift accumulation |

This is the correct architecture for a room-aware autonomous robot. Each incoming sensor frame is matched against the persistent reference model to give an absolute pose — not against the previous frame. Pure frame-to-frame tracking (odometry only) gives a *relative* pose that drifts without bound; localization against a fixed map gives an *absolute* pose that does not. This distinction is why loop closure matters: it replaces a drifted odometry estimate with an absolute one anchored to the map.

**In practice both modes run in parallel.** Matching against a dense 3D reference model (e.g. a GS-LIVO Gaussian scene — [[learned-slam]]) is expensive at frame rate; high-rate IMU/VIO odometry bridges the gaps between map re-matches. The map provides the absolute anchor; odometry provides the high-frequency bridge. This is the same architecture consumer robots already use: iRobot's persistent "Imprint" maps + wheel odometry between re-observations ([[robot-vacuum-navigation]]), or Amazon Kiva's fiducial grid + dead-reckoning between barcode reads ([[warehouse-robot-navigation]]).

**Failure modes specific to the localization phase** (distinct from odometry failure):
- *Symmetric rooms* — identical layouts produce false place matches; semantic disambiguation required ([[indoor-cluttered-slam]]).
- *Stale reference* — a reference built with furniture in one position fails when the room has changed; triggers the "world changed vs I'm lost" ambiguity ([[system-architecture]]).
- *Kidnap* — externally repositioned with no visual overlap → relocalization fails until a known landmark is re-observed ([[robot-vacuum-navigation]]).
- *Featureless surfaces* — blank walls, glossy floors degrade both visual loop closure and VIO feature tracking; LiDAR-inertial geometry matching is more robust ([[indoor-cluttered-slam]]).

## Maturity and indoor failure modes

Outdoor onboard SLAM is robustly *demoed* (sub-0.5% drift forest flight — [[visual-inertial-slam]]). Indoor/home SLAM is harder and carries open failure modes — featureless walls, symmetric-room false loop closures, sustained dynamic movers (people/pets), and multi-floor transitions — surveyed in [[indoor-cluttered-slam]]. This is why the [[home-tidy-drone-prototype]] Phase-1 plan stages a **fiducials-first** V1 (AprilTag/ArUco + optical-flow hold, [[gps-denied-hover-land]]) before bringing marker-free SLAM into the flight loop — the same lesson consumer and industrial robots already encode ([[robot-vacuum-navigation]], [[warehouse-robot-navigation]]).

## Source

Synthesis hub assembled from existing wiki pages (each carries its own raw-source citations):
- [[visual-inertial-slam]], [[lidar-for-uav-autonomy]], [[fast-lio-mid360-orin]], [[indoor-cluttered-slam]], [[slam-fc-integration]], [[drone-sensors-for-autonomy]], [[lidar-vs-vision-autonomy]].

## Related
- [[visual-inertial-slam]] — VIO / VI-SLAM front-end (OKVIS2, stereo+IMU)
- [[lidar-for-uav-autonomy]] — LiDAR-inertial front-end and the LiDAR-necessary thesis
- [[fast-lio-mid360-orin]] — concrete LIO build (FAST-LIO2 + MID360 on Orin)
- [[indoor-cluttered-slam]] — home-scale SLAM and its open failure modes
- [[slam-fc-integration]] — how SLAM pose reaches the flight controller's EKF
- [[gps-denied-hover-land]] — the fiducials-first alternative to full SLAM for V1
- [[drone-sensors-for-autonomy]] — sensor SWaP/capability comparison
- [[lidar-vs-vision-autonomy]] — the open LiDAR-vs-vision conflict
- [[drone-autonomy-state]] — deployment-maturity context
- [[learned-slam]] — the AI/learning-based methods layer (neural LIO, learned VIO, edge 3DGS-SLAM, depth foundation models, learned place recognition)
- [[nano-drone-compute]] — onboard-compute envelope that gates SLAM methods
