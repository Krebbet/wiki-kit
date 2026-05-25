# Indoor / Cluttered-Environment SLAM

Classical VIO and LiDAR-inertial odometry (see [[visual-inertial-slam]], [[lidar-for-uav-autonomy]]) accumulate drift and lose loop-closure in GPS-denied interiors because symmetric floors, featureless walls, and moving occupants break appearance-based place recognition. This page surveys techniques that extend those foundations into home-scale cluttered spaces: object-level metric-semantic SLAM, neural radiance / Gaussian-splatting maps, multi-floor exploration, and semantic + WiFi loop closure.

---

## State of the art

### Object-level / metric-semantic SLAM

- *demoed* — **SlideSLAM** (Penn GRASP, 2406.17249): real-time decentralised metric-semantic SLAM for heterogeneous aerial+ground teams; object-level semantic landmarks (YOLO instance segmentation from RGB-D or LiDAR) replace dense point clouds in the factor graph, enabling storage-efficient maps and viewpoint-invariant inter-robot loop closure; validated onboard Falcon 250 UAVs and Scarab UGVs in cluttered indoor+outdoor environments. [01-arxiv-2406-17249]

- *demoed* — **3D Active Metric-Semantic SLAM** (Penn GRASP, 2309.06950): SWaP-constrained Falcon 250 UAV autonomously explores multi-floor GPS-denied buildings; Semantic Loop Closure (SLC) over sparse object-centroid factor graphs reduces position error by **83–93%** and yaw error by **40–75%** vs. VIO alone; full software stack (YOLO-v8 segmentation at 2 Hz, GTSAM back-end, COP-based exploration planner) runs real-time on Intel NUC i7; CPU load 42–53%, with semantic SLAM front-end taking ~34%. [02-arxiv-2309-06950]

### Multi-floor exploration and symmetric-interior loop closure

- *demoed* — **TWC-SLAM** (Shenzhen U., 2510.22754): multi-agent cooperative LiDAR SLAM (FAST-LIO2 front-end) fuses **text semantics** (PaddleOCR + Levenshtein distance) and **WiFi fingerprints** (MAC + RSS similarity) to disambiguate structurally identical corridors and rooms; in indoor environments with repetitive architecture and duplicate text signs, achieves 0.21 m end-point error vs. 1.69 m for point-cloud-only DCL-SLAM; the two-modal fusion is necessary because text-only yields false matches on duplicate emergency-exit signs, and WiFi-only fails from multipath. [05-arxiv-2510-22754]

- *demoed (benchmark)* — **NUFR-M3F dataset** (Northeastern U., 2306.08522): first continuous multi-floor indoor SLAM dataset (seven cameras, 128-ch LiDAR, IMU, multiple floors via elevator); benchmarks show all evaluated VO/VIO algorithms produce **wrong inter-floor loop closures** on symmetrical floors (5th/4th/2nd ISEC floors identical in layout), causing one floor's trajectory to shift into another; vision-only algorithms additionally fail at featureless white-wall corridors and glass surfaces; LiDAR odometry (LeGO-LOAM) is most robust per-floor but cannot handle elevator transits. [07-arxiv-2306-08522]

### 3D Gaussian Splatting SLAM (3DGS-SLAM)

- *demoed* — **GLC-SLAM** (Beihang U., 2409.10982): 3DGS SLAM with hierarchical loop closure (global NetVLAD place recognition + local geometric check to suppress false loops from repetitive chairs/tables); divides scene into 3D Gaussian submaps anchored to keyframes; direct map adjustment via keyframe-pose update avoids costly NeRF retraining; achieves 0.23 cm ATE on Replica (26% better than second-best), with lowest GPU memory (7.0 GiB) and fastest per-iteration time (18 ms mapping, 16 ms tracking) among tested dense RGB-D SLAM methods. [04-arxiv-2409.10982]

- *demoed* — **VIGS SLAM** (Yonsei U., 2501.13402): IMU preintegration used as initial guess for G-ICP point-cloud tracking, decoupling tracking from dense photometric loss and enabling large-scale indoor 3DGS SLAM (tested on 65 m × 65 m office with 12–60 walking people); reduces ATE from ~700 cm (GS-ICP SLAM baseline) to **25–47 cm** on uHumansV1; successfully renders people-free maps because ICP correspondences remain robust to dynamic movers. [09-arxiv-2501-13402]

- *demoed* — **VIGS-SLAM ETH** (ETH Zürich, 2512.02293): tightly coupled visual-inertial 3DGS SLAM with windowed IMU optimization, time-varying bias modeling, and loop closure with consistent Gaussian map updates; targets motion blur, low texture, and exposure variation; evaluated on five challenging datasets including a self-captured retail sequence. [03-arxiv-2512-02293]

### Dynamic-obstacle avoidance

- *demoed* — **End-to-end DRL obstacle avoidance** (HKU ArcLab, 2503.14352): LiDAR point-cloud encoded into stacked 36×36 2-D range images (36 historical frames); single ResNet+MLP neural network generates horizontal acceleration commands; avoids pedestrians and random-direction balls at up to **6 m/s** with 3.4–5.2 ms inference vs. 11–35 ms for optimisation-based methods; real-world platform: 240 mm quadrotor, Livox Mid-360, Morefine M6S (Intel N100); limited to horizontal plane avoidance. [06-arxiv-2503-14352]

- *demoed* — **RD-VIO** (Zhejiang U., 2310.15072): VIO with IMU-PARSAC for moving-keypoint rejection (two-stage: IMU-guided landmark match then intra-keypoint match) and deferred-triangulation for pure-rotation frames; targeted at mobile AR with large dynamic objects; outperforms VINS-Mobile in dynamic scenes. [08-arxiv-2310-15072]

### Large-scale VIO robustness / failure recovery

- *demoed* — **Amazon grocery-store SLAM** (Amazon AWS, 11-amazon-indoor-mapping): visual-inertial SLAM (SVIn2 + OKVIS-style sliding-window) augmented with a health tracker (covisibility of features across frames, velocity-divergence check, conditioned initialization) and continuous session merging; maps grocery stores of **1700–3700 m²** over 60–80 min without manual intervention; ORB-SLAM3 and VINS-Fusion fail or produce extreme distortion in all three stores; nearest competitor (VINS-Fusion) loses track at 63 min in the hardest store. [11-amazon-indoor-mapping]

- *speculated* — **10-arxiv-2508-01965** (Mill Hill Garage, 2025): review of indoor drone property assessment emphasises 3DGS active-reconstruction for viewpoint selection and BIM integration; no SLAM benchmark data; consumer product framing. [10-arxiv-2508-01965]

---

## Key gaps

- **Featureless / repetitive surfaces.** All vision-based methods degrade on plain white walls, glossy floors, and glass; IMU bridging is short-lived (< 1 s). LiDAR degrades in featureless corridors similarly. No tested system handles all failure modes without human tuning. [07-arxiv-2306-08522, 11-amazon-indoor-mapping]

- **Symmetric-interior false loop closures.** Identical floor layouts defeat bag-of-words and point-cloud descriptors; semantic SLC requires distinguishable objects (chairs, not blank corridors). WiFi+text fusion (TWC-SLAM) helps for text-rich environments but is absent from most home interiors. [05-arxiv-2510-22754, 07-arxiv-2306-08522, 02-arxiv-2309-06950]

- **Sustained dynamic movers (people, pets).** Current approaches either filter dynamic points reactively (RD-VIO's IMU-PARSAC) or rely on ICP robustness (VIGS SLAM); neither maintains semantic identity of dynamic objects across sessions. 3DGS methods silently remove transient objects from maps, which is useful for mapping but removes safety context.

- **Multi-floor transition.** Elevator rides remove visual and LiDAR features simultaneously; IMU alone drifts in seconds. No published system handles the full continuous multi-floor trajectory reliably; the NUFR-M3F dataset documents this as an open problem. [07-arxiv-2306-08522]

- **Onboard compute for dense methods.** The RGB-D 3DGS-SLAM variants here (GLC-SLAM, VIGS SLAM) run on desktop GPUs (RTX 3090, RTX A5000). **Update (2025): no longer a blanket limit** — GS-LIVO has *demoed* real-time Gaussian-Splatting LiDAR-inertial-visual SLAM on a Jetson Orin NX 16 GB (48.3 ms/frame ≈ 20 Hz; 1.2–1.5 GB vs 17–21 GB for desktop GS-SLAM), albeit on a ground/handheld rig, not in flight ([[learned-slam]]). Semantic-landmark methods (SlideSLAM, Active MS-SLAM) run on Intel NUC i7 onboard but sacrifice map density. See [[nano-drone-compute]], [[learned-slam]].

- **Lighting variability.** Sunlight through windows, glare, and exposure changes cause VIO front-end failures in grocery-store and library datasets; no tested system adapts exposure-robustly without manual tuning. [11-amazon-indoor-mapping]

- **Confined-space safety / prop-strike.** Dynamic-avoidance work (DRL, 2503.14352) operates in open arenas; integration with tight-corridor SLAM and safe-flight volumes for home interiors is unaddressed. See [[safe-indoor-flight]].

---

## Source

| File | arXiv / Source | Title | One-line |
|---|---|---|---|
| `raw/research/indoor-cluttered-slam/01-arxiv-2406-17249.md` | arXiv 2406.17249 | SlideSLAM: Sparse, Lightweight, Decentralized Metric-Semantic SLAM for Multi-Robot Navigation | Decentralised object-level SLAM for heterogeneous aerial+ground teams, indoor+outdoor. |
| `raw/research/indoor-cluttered-slam/02-arxiv-2309-06950.md` | arXiv 2309.06950 | 3D Active Metric-Semantic SLAM | SWaP UAV explores multi-floor buildings with active semantic loop closure, 83–93% drift reduction. |
| `raw/research/indoor-cluttered-slam/03-arxiv-2512-02293.md` | arXiv 2512.02293 | VIGS-SLAM (ETH) | Tightly coupled VI-3DGS SLAM with windowed IMU, bias modeling, and loop closure. |
| `raw/research/indoor-cluttered-slam/04-arxiv-2409-10982.md` | arXiv 2409.10982 | GLC-SLAM | 3DGS SLAM with hierarchical loop closure; fastest per-iteration, lowest memory among dense RGB-D methods. |
| `raw/research/indoor-cluttered-slam/05-arxiv-2510-22754.md` | arXiv 2510.22754 | TWC-SLAM | Multi-agent LiDAR SLAM fusing text semantics + WiFi to resolve symmetric-corridor aliasing. |
| `raw/research/indoor-cluttered-slam/06-arxiv-2503-14352.md` | arXiv 2503.14352 | Flying in Highly Dynamic Environments with End-to-end Learning | DRL quadrotor avoids pedestrians and 6 m/s balls via stacked LiDAR range images. |
| `raw/research/indoor-cluttered-slam/07-arxiv-2306-08522.md` | arXiv 2306.08522 | Challenges of Indoor SLAM: A multi-modal multi-floor dataset | NUFR-M3F benchmark exposing symmetric-floor aliasing and elevator-transit failures. |
| `raw/research/indoor-cluttered-slam/08-arxiv-2310-15072.md` | arXiv 2310.15072 | RD-VIO: Robust Visual-Inertial Odometry for Mobile Augmented Reality in Dynamic Environments | IMU-PARSAC removes dynamic keypoints; handles pure-rotation degenerate motion. |
| `raw/research/indoor-cluttered-slam/09-arxiv-2501-13402.md` | arXiv 2501.13402 | VIGS SLAM: IMU-based Large-Scale 3D Gaussian Splatting SLAM | IMU preintegration enables large-scale 3DGS SLAM with dynamic people; 25–47 cm ATE in 65 m² office. |
| `raw/research/indoor-cluttered-slam/10-arxiv-2508-01965.md` | arXiv 2508.01965 | From Photons to Physics: Autonomous Indoor Drones and the Future of Objective Property Assessment | Review of drone-based property assessment; 3DGS active-reconstruction for BIM. |
| `raw/research/indoor-cluttered-slam/11-amazon-indoor-mapping.md` | Amazon Science | Large-scale Indoor Mapping with Failure Detection and Recovery in SLAM | VIO health-tracker + session merging maps grocery stores up to 3700 m² where ORB-SLAM3 fails. |

---

## Related

- [[slam]] — overview hub for the SLAM cluster
- [[home-tidy-drone-prototype]] — parent; research assignment #3
- [[visual-inertial-slam]] — OKVIS2, FAST-LIO2 foundations cross-referenced here
- [[lidar-for-uav-autonomy]] — LiDAR-inertial stack extended by cluttered-indoor constraints
- [[lidar-vs-vision-autonomy]] — sensor trade-offs relevant to featureless-wall failure modes
- [[nano-drone-compute]] — onboard compute constraints that gate 3DGS-SLAM deployment
- [[semantic-object-memory]] — persistent object-level maps built on top of metric-semantic SLAM
- [[drone-sensors-for-autonomy]]
- [[drone-autonomy-state]]
- [[onboard-grasp-perception]]
- [[precision-docking-recharging]]
- [[voice-intent-task]]
- [[safe-indoor-flight]]
