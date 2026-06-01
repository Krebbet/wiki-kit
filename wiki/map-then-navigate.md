# Map-Then-Navigate

The two-phase approach to indoor robot autonomy: first build a complete geometric map via exploration, then switch to localization-only mode and navigate within that known map. Standard pattern for home service robots; avoids the accuracy degradation from simultaneous SLAM during active navigation.

## Source
- raw/research/dynamic-slam-nav/02-modular-exploration-semantic.md — arXiv 2409.15493

## Related
[[slam-toolbox]], [[ros2-nav2]], [[2d-lidar-slam]], [[slam]], [[dynamic-object-handling]], [[system-architecture]], [[home-tidy-drone-prototype]]

---

## Why separate mapping from navigation

Loop-closure corrections applied to detected objects slow down mapping as object count grows — concurrent semantics degrades throughput [src: modular-exploration-semantic]. Localization pose quality is higher when navigating in a finished map vs. during active SLAM [src: modular-exploration-semantic].

At 30 FPS data replay: concurrent mapping + semantics (Khronos) maps 3 objects; sequential approach maps 79 [src: modular-exploration-semantic].

*(synthesis)* This mirrors the [[robot-vacuum-navigation]] and [[warehouse-robot-navigation]] precedents: robot vacuums shipped on geometric-only maps first; Amazon Kiva uses a pre-mapped grid, not live SLAM.

## Phase 1 — Exploration and map building

Frontier-based exploration: robot navigates to unexplored boundaries of the known map until no frontiers remain.

**DWFE (Dynamic Window Frontier Exploration)** from the paper: searches local radius first; if frontier count below threshold, expands to global radius; terminates when global count also below threshold [src: modular-exploration-semantic]. Result vs. standard frontier baseline: 7.8% more area covered, 12% less distance traveled, in 1440 m² simulated hospital over 20 runs [src: modular-exploration-semantic].

Navigation to frontiers via ROS move_base; speed capped at 0.6 m/s, 0.7 m inflation radius [src: modular-exploration-semantic]. Phase 1 uses GMapping (2D LiDAR SLAM, 0.1 m/pixel occupancy grid); robot exploration trajectory recorded at 0.25–1 Hz for use in Phase 2 [src: modular-exploration-semantic].

Termination: frontier count below global threshold OR Tmax elapsed; completed map saved to disk [src: modular-exploration-semantic].

*(synthesis)* For the project's ground robot, [[slam-toolbox]] async mapping mode replaces GMapping; the frontier exploration pattern is identical regardless of SLAM backend.

## Phase 2 — Localization and semantic updating

After map is saved, robot localizes via AMCL (Adaptive Monte Carlo Localization) within the pre-built occupancy grid [src: modular-exploration-semantic].

Revisit trajectory planned from recorded phase-1 waypoints: subsampled to 2 m minimum separation, then greedy TSP tour [src: modular-exploration-semantic]. At each waypoint: GroundingDINO (open-vocabulary detection) + MobileSAM (segmentation) on RGB-D frames [src: modular-exploration-semantic].

Detected objects projected to map frame via camera intrinsics + depth + robot pose transforms [src: modular-exploration-semantic]. Semantic graph updated: existing nodes removed if not re-detected within FoV; new nodes added for unmatched detections [src: modular-exploration-semantic]. Object association threshold: 0.7 m per-category [src: modular-exploration-semantic].

Phase 2 in Environment A (8500 m²): 35 min revisit vs. 150 min initial exploration [src: modular-exploration-semantic].

## Phase transition

Transition is automatic: occurs immediately after Phase 1 saves the map [src: modular-exploration-semantic].

*(synthesis)* In [[slam-toolbox]] terms: switch from `online_async_launch.py` (async mapping mode) to `localization_launch.py` (pure localization mode). The map file written at Phase 1 end is the SLAM Toolbox serialized pose-graph.

*(synthesis)* In [[ros2-nav2]] terms: Phase 1 runs SLAM Toolbox as the map→odom TF source (no nav2_amcl); Phase 2 loads the saved map via nav2_map_server and switches to AMCL for localization.

## Performance (real-world results)

Table from [src: modular-exploration-semantic]:

| Environment | Size | Exploration time | Revisit time | Object F1 (sample) |
|---|---|---|---|---|
| Env A (corridors) | ~8500 m² | 150 min | 35 min | Table 0.80, Chair 0.87, Door 0.87 |
| Env B (laboratory) | 117 m² | 4 min | 2 min | Person 1.00, Chair 1.00, TV 0.67 |

## Failure modes and open questions

- Occlusion during revisit: objects behind furniture may not be detected even on planned trajectory [src: modular-exploration-semantic]
- Lighting changes between mapping and revisit degrade detection confidence [src: modular-exploration-semantic]
- GMapping/AMCL drift in long corridors — *(synthesis)* mitigated by using [[slam-toolbox]] which has better loop closure than GMapping
- Dynamic objects during Phase 1 corrupt the geometric map — see [[dynamic-object-handling]] for the DynaSLAM approach to clean map building
- *(synthesis)* For the project: Phase 1 should be run once per room in a clean state (no people moving). Phase 2 runs are the "working" sessions.
