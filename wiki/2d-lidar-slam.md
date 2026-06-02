# 2D LiDAR SLAM for Ground Robots

2D LiDAR SLAM builds a planar occupancy grid map while simultaneously localizing the robot within it, using a spinning laser scanner whose returns are projected onto a single horizontal plane. It is the standard approach for indoor ground robot navigation because 2D planar geometry is sufficient for single-floor environments, scan-matching on probability grids is computationally cheap enough for mobile CPUs, and the sensor class (RPLiDAR, Hokuyo, SICK) is mature, cheap, and lightweight. This page covers the two main hardware options for the Phase-1 ground robot (RPLiDAR S2 and A3), the Cartographer algorithmic architecture (local scan matching → submaps → BBS loop closure → SPA), and a head-to-head comparison against [[slam-toolbox]] (the production-default choice).

## Source

- `raw/research/2d-lidar-slam/05-cartographer-icra2016.md` — Cartographer primary paper (ICRA 2016, Google)
- `raw/research/2d-lidar-slam/04-slam-comparison-indoor-2025.md` — arXiv 2501.09490
- `raw/research/2d-lidar-slam/01-rplidar-s2-specs.md` — SLAMTEC RPLiDAR S2 spec sheet
- `raw/research/2d-lidar-slam/02-rplidar-a3-specs.md` — SLAMTEC RPLiDAR A3 spec sheet

## Related

[[slam-toolbox]] · [[ros2-nav2]] · [[slam]] · [[learned-slam]] · [[home-tidy-drone-prototype]] · [[close-range-depth-sensors]]

---

## Hardware — RPLiDAR options

| Model | Technology | Range | Sample rate | Scan freq | Price (USD) | Notable | BOM notes |
|---|---|---|---|---|---|---|---|
| **YDLIDAR X3** | Triangulation | 0.12–8 m | 3 KHz | 5–10 Hz | ~$65 [src: kaiaai-2d-lidar-list] | Cheapest viable; 135 g | Budget entry for ground robot prototyping |
| **YDLIDAR X4** | Triangulation | 0.12–10 m | 5 KHz | 6–12 Hz | ~$70–90 [src: kaiaai-2d-lidar-list, budget-lidar-under-100] | 180 g; ROS2 driver | Good range/price ratio for SLAM Toolbox |
| **LDROBOT D500** | dToF | 0.2–30 m | — | 8–12 Hz | ~$70–90 [src: budget-lidar-under-100] | 120 g, 70 mm dia × 40 mm; USB-CDC | dToF better on reflective floors vs triangulation |
| **RPLIDAR A1** | Triangulation | 0.2–12 m | 8 KHz | 5.5–10 Hz | ~$99 [src: budget-lidar-under-100] | — | Long-standing budget benchmark; rplidar_ros |
| **RPLIDAR C1** | DTOF fusion | 0–12 m | 5 KHz | 10–20 Hz | ~$94–96 (Amazon/Waveshare) | Reflectivity + 2.5D output | New SLAMTEC DTOF targeting home robots; Class 1 laser |
| **S2** | dToF | 30 m (90% refl.) / 10 m (10% refl.) | 32,000 Hz | 10 Hz | — [not in retail comparison sources] | IP65; angular res 0.1125°; S2E adds network port | Backward-compatible with A-series [src: rplidar-s2-specs] |
| **A3** | Triangulation + RPVision | 25 m (optimized) | 16,000 Hz | Configurable | — [not in retail comparison sources] | Brushless OPTMAG motor; dual indoor/outdoor | Backward-compatible with A-series [src: rplidar-a3-specs] |

**Notes on pricing:** Prices added 2026-06-01 from `raw/research/cheap-lidar/` captures. S2 and A3 pricing was not in the budget comparison sources; check SLAMTEC distributor pricing directly. Both S2 and A3 share the interface port with the A-series [src: rplidar-s2-specs, rplidar-a3-specs]. ROS 2 driver: `rplidar_ros` supports A1/A2/A3/S1/S2/S3 [src: rplidar-a3-specs]. See [[cheap-lidar-pricing-guide]] for the full cross-vendor pricing table including 3D options.

*(synthesis)* For the Phase-1 ground robot, the **A3** (triangulation, 25 m, brushless motor for longevity) is the budget-standard choice for indoor SLAM. The **S2** (dToF, 30 m, IP65) adds outdoor capability and a higher sample rate (32k vs 16k Hz) for a modest price premium. Both are well below the weight and cost of the Livox MID360 and are sufficient for 2D occupancy grid SLAM. The S2's dToF technology is less affected by surface reflectivity than triangulation-based sensors, which may matter for glossy floors.

---

## Cartographer architecture

Cartographer (Hess et al., ICRA 2016, Google) is a 2D and 3D SLAM system structured as two loosely coupled subsystems: local SLAM (scan matching against a growing submap) and global SLAM (pose-graph optimization triggered by loop closure). The split allows real-time local tracking while global consistency is recovered asynchronously.

### Local scan matching

Incoming scans are matched against the **active submap** using Ceres nonlinear least-squares on a bicubically interpolated 5 cm probability grid. The objective minimizes:

$$\min_\xi \sum_k \left(1 - M_\text{smooth}(T_\xi h_k)\right)^2$$

where ξ is the scan pose, T_ξ transforms each scan point h_k, and M_smooth is the bicubic interpolation of the probability grid. The result is pixel-subaccurate scan alignment within the current submap. Drift accumulates over time — global optimization corrects it. [src: cartographer-icra2016]

### Submap structure

Each submap is a fixed-resolution (default **5 cm**) probability grid M: ℝ² → [p_min, p_max]. Hit/miss probabilities are updated via an odds formulation. A fixed number of consecutive scans are inserted per submap; once no further scans will be added, the submap is marked **finished** and precomputed max-pooled grids at heights h = 0, 1, 2, … are generated for efficient branch-and-bound loop closure scoring. [src: cartographer-icra2016]

### Branch-and-bound loop closure

When a submap is finished, all (scan, submap) pairs within spatial proximity become loop closure candidates. The **Branch-and-Bound Scan Matching (BBS)** algorithm finds the pixel-accurate optimal pose within a configurable search window (default ±7 m translation, ±30° rotation) without exhaustive search. Depth-first search with upper bounds derived from precomputed coarser grids prunes the tree — each node costs O(K) where K = number of scan points. Candidates whose score exceeds a threshold become pose-graph constraints with associated covariance. [src: cartographer-icra2016]

### Sparse Pose Adjustment (SPA)

All finished submap poses and scan poses are jointly optimized via nonlinear least squares (Ceres) with **Huber loss**. SPA runs every few seconds; typical solve time ~0.3 s. The Huber loss makes the optimizer robust to false-positive loop closure constraints — spurious matches are down-weighted rather than breaking the solution. [src: cartographer-icra2016]

### Performance numbers

From Radish dataset benchmarks and in-house Google tests [src: cartographer-icra2016]:

| Metric | Value | Environment |
|---|---|---|
| Translational RMSE | ~0.024 m | Intel lab |
| Translational RMSE | ~0.040 m | MIT Killian Court |
| Loop closure precision | 99.8% | Freiburg building 79 |
| Loop closure precision | 77.3% | Freiburg hospital |
| Wall-clock for 2253 m trajectory | 360 s (5.3× faster than real-time) | Xeon E5-1650 |
| Minimum viable scanner | Sub-$30, 2 Hz, 5 cm resolution (Revo LDS experiment) | — |

---

## Comparison: Cartographer vs SLAM Toolbox

| Dimension | Cartographer | SLAM Toolbox | Notes |
|---|---|---|---|
| **Map representation** | Submaps (probability grids, precomputed for BBS) | Pose-graph + raw scans (full serialization) | SLAM Toolbox serializes raw data; Cartographer stores submaps only [src: slam-toolbox-joss, cartographer-icra2016] |
| **Loop closure** | Branch-and-bound scan-to-submap (BBS) | Scan-to-map registration (k-d tree) | Different formulations; both produce pose-graph constraints [src: slam-toolbox-joss, cartographer-icra2016] |
| **Global optimization** | SPA (Ceres, Huber loss) | Google Ceres (same library, different formulation) | [src: slam-toolbox-joss, cartographer-icra2016] |
| **Multi-session** | No native support | Yes — serializes and reloads full pose-graph | Key differentiator [src: slam-toolbox-joss] |
| **Pure localization mode** | No | Yes — elastic pose-graph deformation | [src: slam-toolbox-joss] |
| **ROS 2 default** | No (replaced) | Yes — default since ROS 2 Foxy | [src: slam-toolbox-joss] |
| **Maintenance status** | **Abandoned by Google (~2021)** | Actively maintained | Critical for production use [src: slam-toolbox-joss] |
| **Large-scale demonstrated** | 250,000 ft² | ~24,000 m² (≈250,000 ft²) | Comparable scale [src: cartographer-icra2016, slam-toolbox-joss] |

*(synthesis)* Cartographer's BBS loop closure is architecturally elegant and the ICRA 2016 paper is the clearest exposition of the submap/BBS/SPA design. However, SLAM Toolbox's multi-session support and pure-localization mode make it the correct default for a home robot that must resume operations across reboots and sessions. Cartographer's abandonment by Google means no ROS 2 maintenance and no bug fixes; SLAM Toolbox is the production path. The architectural deep-dive here is useful for understanding what SLAM Toolbox's loop closure is doing at a conceptual level — the mechanisms are related.

---

## ATE benchmark numbers (indoor)

From arXiv 2501.09490 [src: slam-comparison-indoor-2025]:

| System | Sensor | RMSE ATE (m) | Notes |
|---|---|---|---|
| **Cartographer** | 2D lidar | **0.024** | Best overall; reference for lidar baseline |
| RTAB-Map | stereo | 0.163 | Best visual; good fallback if no lidar |
| ORB-SLAM (stereo) | stereo | 0.190 | Most stable visual method |
| ORB-SLAM (mono) | monocular | 0.166 | |
| LSD-SLAM | monocular | 0.301 | |
| ZEDfu | stereo | 0.726 | Worst visual |
| PTAM / SVO / DPPTAM | monocular | failed | Lost track in monochrome office environment |

**Methodology note:** Visual SLAM ATE was measured against a Hector SLAM trajectory used as a ground-truth proxy — not an independent physical ground truth. Numbers are relative, not absolute. SLAM Toolbox was not tested — the paper predates it. Hardware is Kinetic-era (Jetson TX1). [src: slam-comparison-indoor-2025]

*(synthesis: numbers are useful as relative comparisons between visual methods; for absolute SLAM Toolbox performance see [[ros2-nav2]] task-driven benchmark: N-AUC 0.93, precision 1.75 cm in simulation)*

---

## Notes on GMapping and HectorSLAM

**GMapping:** Filter-based (particle filter), no loop closure at industrial scale, fails large spaces, cannot reinitialize across sessions — not recommended for home robot use. Was the ROS 1 default before SLAM Toolbox. [src: slam-toolbox-joss]

**HectorSLAM:** No loop closure — unsuitable for large or complex environments. Used as a ground-truth proxy in arXiv 2501.09490 only because of good local accuracy in small loops; not a production choice. [src: slam-toolbox-joss, slam-comparison-indoor-2025]
