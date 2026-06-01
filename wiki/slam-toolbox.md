# SLAM Toolbox

SLAM Toolbox is the default SLAM vendor for ROS 2, replacing GMapping. It is a graph-based 2D laser-scanner SLAM system built on OpenKarto (SRI International) with the original Sparse Bundle Adjustment optimizer replaced by Google Ceres, and measurement matching restructured for a 10× speed-up enabling multi-threaded processing. It supports synchronous, asynchronous, and pure-localization operation modes; multi-session mapping; kinematic map merging; and manual pose-graph manipulation tools. At 1.75 cm mean precision error (simulation, with pre-built map), it is the best-performing SLAM method in the task-driven indoor navigation benchmark — outperforming both 3D LiDAR methods (FAST-LIO2, LIO-SAM) and stereo visual methods at real-world long-path navigation.

## Source

- `raw/research/ros2-nav2/01-slam-toolbox-joss.md` — SLAM Toolbox JOSS 2021 (Macenski & Jambrecic)
- `raw/research/ros2-nav2/04-task-driven-slam-bench.md` — Task-driven SLAM benchmark, arXiv 2409.16573 (Du et al., updated Mar 2025)

## Related

[[ros2-nav2]] · [[slam]] · [[learned-slam]] · [[fast-lio-mid360-orin]] · [[system-architecture]] · [[home-tidy-drone-prototype]]

---

## Overview

SLAM Toolbox was selected as the default ROS 2 SLAM vendor to fill the gap left by the abandonment of Cartographer [src: slam-toolbox-joss]. The prior ROS 1 default, GMapping, is filter-based — unsuitable for large spaces, fails loop closure at industrial scale, and cannot reinitialize across sessions [src: slam-toolbox-joss]. HectorSLAM provides no loop closure, making it unreliable for large or featureless spaces [src: slam-toolbox-joss]. Cartographer was the only prior package that could map large spaces in real-time on mobile CPUs, but **Google abandoned and no longer maintains it** [src: slam-toolbox-joss].

SLAM Toolbox is built on **OpenKarto** (Konolige et al., SRI International, 2010), a graph-based 2D SLAM library. Key modifications vs. the original [src: slam-toolbox-joss]:

- Measurement matching restructured → **10× speed-up**, enabling multi-threaded processing
- Sparse Bundle Adjustment optimizer replaced with **Google Ceres** (faster, more flexible)
- Ceres exposed as a **runtime-loaded plugin** — swappable without modifying core code
- Serialization/deserialization added for multi-session support
- K-D tree search and new processing modes for localization and multi-session mapping

Demonstrated scale: maps up to **24,000 m² (250,000 ft²)** in real-time on mobile Intel CPUs by non-expert technicians [src: slam-toolbox-joss].

---

## Operation modes

| Mode | Description | When to use |
|---|---|---|
| **Synchronous** | Buffers measurements and adds all to the SLAM problem; may lag real-time under high processing load | Offline processing or when map quality is paramount over real-time responsiveness |
| **Asynchronous** | Only processes a new measurement when the last is complete and update criteria are met; never lags real-time; may skip measurements if processing is slow | Default for deployment; preserves real-time localization quality |
| **Pure localization** | Rolling buffer matched against prior session(s); elastic pose-graph deformation — embraces environmental changes, then reverts as measurements expire; can also serve as lidar odometry with no prior map | Deployment against a finished map; also usable as lightweight lidar odometry |

[src: slam-toolbox-joss]

**Elastic pose-graph deformation** (pure-localization mode): the current session's nodes are added to the pose-graph with constraints against the prior session. As rolling-buffer measurements expire, the graph reverts to its prior state for that region — adapting to temporary changes without permanently corrupting the map [src: slam-toolbox-joss].

---

## Multi-session and map management

**Serialization** saves the complete raw data + pose-graph (not submaps, unlike Cartographer). This enables [src: slam-toolbox-joss]:

- **Multi-session mapping**: reload a prior session, continue refining or expanding the pose-graph
- **Kinematic map merging**: merge multiple serialized maps into a composite map
- **Manual pose-graph manipulation**: interactively move nodes and laser scans to resolve challenging loop closures or fix a rotated map — exposed via a 3D visualizer plugin

The serialization-over-submaps choice is a deliberate design decision: storing raw scan data permits novel tooling and more accurate multi-session refinement than Cartographer's submap-only representation [src: slam-toolbox-joss].

---

## Performance

| Metric | Value | Source |
|---|---|---|
| Max map scale (real-time, mobile CPU) | 24,000 m² | [src: slam-toolbox-joss] |
| Measurement matching speed-up vs. OpenKarto | 10× | [src: slam-toolbox-joss] |
| N-AUC w/ map, real-world indoor navigation | **0.93** | [src: task-driven-slam-bench] |
| N-AUC short-path | 0.94 | [src: task-driven-slam-bench] |
| Mean position precision error w/ map (simulation) | **1.75 cm** | [src: task-driven-slam-bench] |

SLAM Toolbox shows **minimal performance improvement from adding a pre-built map** compared to other methods — because its scan-to-map registration design is already well-suited for indoor scenarios, and its continuous pose-graph-based global map management inherently maintains precision [src: task-driven-slam-bench].

---

## Comparison to alternatives

| System | Status | Loop closure | Multi-session | Indoor scale | Notes |
|---|---|---|---|---|---|
| **SLAM Toolbox** | Active (ROS 2 default) | Yes (graph-based) | Yes (serialization) | 24,000 m² real-time | OpenKarto + Ceres; 10× speed-up |
| Cartographer | **Abandoned (Google)** | Yes (submap graph) | Partial (submaps only) | Large | Unusual complexity; no maintenance; pure-localization mode exists but limited |
| GMapping | Unmaintained | Weak (particle filter) | No | Small–medium | Filter-based; fails loop closure at industrial scale |
| HectorSLAM | Maintained | **None** | No | Small | No odometry required; fails large/featureless spaces |

[src: slam-toolbox-joss]

---

## Notes on 3D LiDAR vs 2D LiDAR for indoor use

The task-driven benchmark (arXiv 2409.16573) directly compares SLAM Toolbox (2D LiDAR) against FAST-LIO2 and LIO-SAM (3D LiDAR-inertial) for indoor repeated-navigation precision [src: task-driven-slam-bench]:

- **SLAM Toolbox outperforms both 3D LiDAR methods** on indoor navigation. FAST-LIO2 and LIO-SAM are designed for exploration (looser navigation demands) and outdoor structured scenes where 3D geometric loop closure is robust. These properties do not transfer to compact indoor rooms where 2D scan-to-map registration is more discriminative.
- In long-path real-world tests, both LIO methods failed the initial mapping phase entirely — their N-AUC scores for that test are not reported as complete results [src: task-driven-slam-bench].
- On short paths, LIO-SAM N-AUC = 0.86 vs. SLAM Toolbox 0.94 [src: task-driven-slam-bench].

*(synthesis)* **Implication for the project:** The [[fast-lio-mid360-orin]] setup (FAST-LIO2 + MID360) is well-motivated for 3D obstacle avoidance and outdoor mapping, but should **not** be relied on as the primary navigation localization source indoors. For the ground-robot Phase-1 prototype, SLAM Toolbox driving the 2D occupancy grid and feeding Nav2 (see [[ros2-nav2]]) is the benchmark-supported choice for repeatable room-to-room navigation. The MID360 can still contribute to STVL costmap obstacle detection without being the SLAM pose source.
