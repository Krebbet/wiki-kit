# Dynamic Object Handling

How indoor robots cope with a world that changes: objects moving during a navigation session (fast dynamics), objects moved between sessions (semi-static), and room-level changes across many runs (lifelong). Three distinct problem classes requiring three distinct mechanisms.

## Source
- raw/research/dynamic-slam-nav/01-dynaslam.md — DynaSLAM (RAL/IROS 2018)
- raw/research/dynamic-slam-nav/03-pocd-change-detection.md — POCD (RSS 2022, U of Toronto)
- raw/research/dynamic-slam-nav/04-lifelong-semantic-map.md — iRobot lifelong maps (2020)
- raw/research/dynamic-slam-nav/05-object-oriented-grid-mapping.md — Object-oriented grid mapping (arXiv 2309.08324, 2023)

## Related
[[slam]], [[slam-toolbox]], [[ros2-nav2]], [[map-then-navigate]], [[semantic-object-memory]], [[system-architecture]]

---

## Taxonomy

*(synthesis)* Three distinct timescales, each requiring a different mechanism:

| Class | Example | Timescale | Mechanism |
|---|---|---|---|
| **Fast-dynamic** | Person walking, ball rolling | Seconds | Real-time costmap clearing (STVL / object-oriented grid) |
| **Semi-static** | Chair pushed, bag left on floor | Hours–days | Between-session change detection (POCD) |
| **Lifelong** | Furniture rearranged, new room added | Weeks–months | Multi-session map maintenance (iRobot approach) |

---

## Fast-dynamic: real-time costmap

### Nav2 STVL (baseline)

[[ros2-nav2]] already documents STVL (Spatio-Temporal Voxel Layer): voxels age out after a configurable decay time. Simple, sensor-agnostic, per-cell independent. Limitation: a vacated vehicle takes 120–150 scans to clear at η=0.5 [src: object-oriented-grid-mapping].

### Object-oriented grid mapping (C-NDT-OM)

Core idea: instead of clearing cells independently, all cells belonging to the same semantic cluster are updated together. Free-space observations anywhere in a cluster propagate to occluded cells in the same cluster [src: object-oriented-grid-mapping].

Key results [src: object-oriented-grid-mapping]:
- Vacated vehicle cleared in **4 scans** vs. 120–150 for standard per-cell decay
- **~35% fewer residual dynamic voxels** in high-dynamics sequences (KITTI 01, 04)
- Marginally worse in low-dynamics sequences (mean 0.293 vs. 0.238) — conservative membership can overzealously merge nearby same-class objects
- Localization ATE: marginally better overall

Implementation: extends NDT-OM with per-cell cluster index, membership δ (χ² test vs. cluster aggregate), and semantic-label distribution. Region-growing over voxels with same semantic label defines clusters [src: object-oriented-grid-mapping].

**vs. STVL:** STVL uses temporal decay (time-based, per-cell); C-NDT-OM uses evidence propagation (geometry-based, per-cluster). C-NDT-OM requires semantic segmentation of the point cloud; STVL works with any depth source. For the project's LiDAR + RGB-D setup, C-NDT-OM is feasible but adds a segmentation dependency. *(synthesis)*

---

## Building a clean static map: DynaSLAM

If the map is built while people are present, dynamic objects corrupt it — leaving ghost furniture or missing walls. DynaSLAM prevents this by removing dynamic content before it enters ORB-SLAM2 [src: dynaslam].

**Two-stage masking front-end:**
1. Mask R-CNN segments 19 COCO dynamic classes (person, bicycle, car, motorcycle, bus, train, truck, boat + 10 animal classes) — removed regardless of whether they are currently moving [src: dynaslam]
2. Multi-view geometry depth-change test (RGB-D only): projects keypoints from 5 most-overlapping keyframes; labels pixels dynamic if projected depth differs > 0.4 m from measured depth; region-growing expands the mask [src: dynaslam]

Combined mask fed to ORB-SLAM2; feature extraction restricted to unmasked pixels only [src: dynaslam].

**Results on TUM RGB-D walking sequences [src: dynaslam]:**

| Sequence | ORB-SLAM2 ATE (m) | DynaSLAM ATE (m) | Improvement |
|---|---|---|---|
| w_halfsphere | 0.351 | 0.025 | 93% |
| w_xyz | 0.459 | 0.015 | 97% |
| w_rpy | 0.662 | 0.035 | 95% |

**Compute caveat:** Not real-time as published. Total pipeline ~600 ms/frame (multi-view geometry: 236–334 ms; background inpainting: 184–208 ms; Mask R-CNN: ~195 ms on Tesla M40) [src: dynaslam]. *(synthesis)* For a home robot doing Phase 1 exploration at walking pace, offline or near-real-time processing is acceptable — the map is built once, not continuously.

**What gets removed:** All persons/vehicles even when stationary. Parked cars are incorrectly excluded (marginal accuracy cost in low-dynamic scenes). For a home robot this is correct behavior: the long-term map should show only furniture, not visiting people [src: dynaslam].

---

## Semi-static: between-session change detection (POCD)

For objects that move between robot sessions — a chair pushed to a different corner, a bag left on the floor — the static map from Phase 1 becomes stale. POCD detects and corrects these changes on each revisit [src: pocd-change-detection].

**Object state representation:** Each mapped object carries a joint distribution: geometric change magnitude l ~ N(μ,σ²) and stationarity score v ~ Beta(α,β). Both updated via Bayesian inference on each traversal [src: pocd-change-detection].

**Change detection pipeline [src: pocd-change-detection]:**
1. Semantic segmentation of RGB frame → per-pixel labels
2. RGB-D clustering → per-object observations (pose, point cloud, bounding box, semantic class)
3. Point-to-plane ICP + Hungarian algorithm associates observations to mapped objects (cost = distance² + angle + class mismatch)
4. TSDF-diff change magnitude Δ computed: mean |TSDF(observation) − TSDF(model)| over intersection voxels
5. Bayesian update of (μ,σ,α,β); objects in frustum but undetected receive max pseudo-change Δ_max
6. If E[v] < θ_stat: erase object from global map; recreate at new position when next observation arrives

**Results (TorWIC warehouse dataset) [src: pocd-change-detection]:**

| Method | Precision | Recall | FPR |
|---|---|---|---|
| POCD | **80.2%** | 78.7% | **3.0%** |
| Panoptic Multi-TSDFs | 77.4% | 78.9% | 4.2% |
| Fehr et al. | 76.3% | 76.6% | 3.8% |
| Kimera (vanilla) | 60.6% | 74.2% | 7.7% |

Runtime: 4.57 FPS average on 24-core AMD Ryzen CPU (bottleneck: O(n³) Hungarian association scales poorly with object count) [src: pocd-change-detection].

**Semi-static vs. fast-dynamic:** POCD erases and recreates moved objects rather than tracking them continuously. Dynamic classes (e.g., robot itself) receive strong downward stationarity updates each frame. Not designed for real-time tracking of moving objects — see STVL / C-NDT-OM above [src: pocd-change-detection].

*(synthesis)* POCD's stationarity score maps directly to the server-side object registry in [[system-architecture]] workstream B: each object in the registry carries a confidence that it is still at its recorded position, decayed on each visit. The Hungarian-assignment step is the "scene diff engine."

---

## Lifelong: multi-session semantic map maintenance

From iRobot's production deployment across thousands of consumer floor-cleaning robots, 425 real-home missions [src: lifelong-semantic-map].

**What is maintained:** Semantic layer (rooms, walls, dividers, clutter) separate from the geometric occupancy map. Moved furniture becomes "clutter" rather than corrupting wall estimates [src: lifelong-semantic-map].

**Map update policy [src: lifelong-semantic-map]:**
- After every mission: room vertices and divider endpoints tracked via vSLAM are transferred to the new map
- Walls and clutter re-classified from the new occupancy map using transferred room boundaries as prior
- Success judged by per-room precision-recall > 50%; if failed, a meta-layer applies corrections:
  - Meta-occupancy: adds synthetic wall-difference pixels to reconnect broken segments
  - Meta-dividers: adds synthetic divider corrections for door-state changes
- If resolution still fails: reject and revert to last valid semantic map

**Results [src: lifelong-semantic-map]:**

| Method | Semantic update failure rate |
|---|---|
| Baseline transfer only | 20.92% |
| + Meta-occupancy | 11.06% |
| + Meta-occupancy + meta-dividers | **1.41%** |

*(synthesis)* The reject-and-revert safety valve is the key production pattern: never present an inconsistent map to the user. The meta-layer correction (fix semantics without touching geometry) maps to the [[system-architecture]] server-side world view: geometric map is ground truth, semantic layer is derived and correctable.

---

## Implications for the project

*(synthesis)*

| Problem | Recommended approach | Notes |
|---|---|---|
| People walking during Phase 1 map build | DynaSLAM-style masking (or offline Mask R-CNN pass on recorded bag) | Not real-time; run as post-process on rosbag |
| Moving ball / pet during navigation | STVL temporal decay (already in Nav2) or C-NDT-OM if semantic labels available | STVL sufficient for slow-moving home obstacles |
| Chair pushed between sessions | POCD stationarity score per object in server registry | Run as batch update at session start |
| Room-level changes across weeks | iRobot meta-layer pattern; semantic layer separate from geometric map | Reject-and-revert safety valve is essential |

Phase 1 map build should be done in an unoccupied home (no people/pets) to get a clean structural map. Dynamic handling during operation is then layered on top via the costmap (fast) and the server registry (slow). See [[map-then-navigate]] for the pipeline.
