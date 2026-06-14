# LiDAR + Visual Fusion SLAM (front-end fusion, and whether it helps our rig)

How systems combine LiDAR geometry with camera (mono/stereo) appearance in the SLAM **front-end**, the coupling spectrum (loosely → tightly), classical vs learned registration, and — the load-bearing question for this prototype — **whether fusing both sensors in the initial-map front-end is likely to improve our INITIAL room map now**, on a **handheld, no-IMU-grade, consumer-cost** rig. This page sits alongside [[slam]] (concept hub), [[2d-lidar-slam]] (our geometry baseline), [[visual-inertial-slam]] (the camera+IMU front-end), [[fast-lio-mid360-orin]] (the LIO/LIV build path), and [[learned-slam]] (the AI-methods layer, incl. GS-LIVO and iBTC). Read those for foundations rather than re-deriving them here.

> **Our current method (the thing this page is judged against).** LiDAR-first geometry — scan-to-scan / scan-to-submap ICP + pose-graph + loop closure (the "EDA064" pose graph) — with monocular **hloc** SfM camera poses used only to **cross-validate** the LiDAR trajectory and to **back-project object labels** (semantics). Camera = loop-closure + semantics; LiDAR = geometry. Core measured learning on file: **LiDAR-first for geometry (ATE 0.024 m vs visual 0.163 m); don't make passive stereo do geometry** ([[2d-lidar-slam]] ATE table, [[relocalization-method-bakeoff]]). This is *de facto* a **loosely-coupled** fusion already — geometry from LiDAR, appearance/semantics from camera, joined at the back-end, not the front-end.

---

## The coupling spectrum

The design choice is **where** the two sensors meet:

- **Independent / cross-validation (what we do).** Each sensor runs its own estimator; the camera result checks or augments the LiDAR result but is not fed into the LiDAR front-end. Cheapest, most robust to one sensor failing, no cross-sensor calibration/sync burden on the front-end. Our hloc-cross-val + label back-projection is exactly this.
- **Loosely-coupled.** One sensor's pose seeds the other's optimizer. The canonical form is **V-LOAM** (Zhang & Singh, ICRA 2015): high-rate visual odometry gives a motion prior, then low-rate LiDAR scan-matching refines it and builds the map — and notably **it needs no IMU** [src: zhang-singh-vloam]. LiDAR points are also commonly projected into the image to **give depth to visual features** (depth-enhanced VO; "[[stereo-dense-reconstruction|RGB-L]]"-style dense-depth-from-LiDAR). The sensors stay in separate estimators; the data are not jointly optimized [src: stereo-lidar-loose-2024, vloam-scale-2023].
- **Tightly-coupled.** LiDAR, (IMU,) and visual residuals enter **one** estimator — a single iterated-EKF or a single factor graph — and are optimized jointly. Highest accuracy and robustness when it works; highest integration cost; in practice **assumes a hardware-synced IMU** to bridge between LiDAR scans and camera frames (R3LIVE, FAST-LIVO2, LVI-SAM, OKVIS2-X, the Boche/Leutenegger 2024 system) [src: fastlivo2-tro2025, r3live-arxiv, lvisam-icra2021, boche-icra2024, okvis2x-arxiv].

The IMU is the hinge. Tightly-coupled LiDAR-**visual** fusion is almost always LiDAR-visual-**inertial** (LVI): the IMU is what makes the tight coupling pay off (it deskews LiDAR, predicts the next frame, and carries the state through the < 1 s gaps where one modality starves — [[indoor-cluttered-slam]]). Without an IMU you are effectively back in the loosely-coupled / cross-validation regime, where V-LOAM lives.

---

## Method comparison

| Method | Coupling | Sensors | IMU needed? | Maturity | Fits our handheld no-IMU consumer rig? |
|---|---|---|---|---|---|
| **Our current** (LiDAR pose-graph + hloc cross-val + label back-project) | Loose / independent | 2D LiDAR + mono camera (shared clock) | No | Working on our data (EDA064) | **This is the baseline** — geometry 0.024-class, camera adds loop-closure + semantics |
| **V-LOAM** (Zhang & Singh, ICRA 2015) | Loose | mono/RGB-D + 3D LiDAR | **No** | Classic, widely reproduced; KITTI top-tier in its day | **Closest fusion candidate** — visual motion prior → LiDAR refine; no IMU; but designed for 3D LiDAR + forward motion |
| **CamVox** (ISEE, ICRA 2021) | Loose (LiDAR-assisted visual) | camera + Livox + IMU | Yes (HW-synced) | Open-source, demoed | Partial — idea (LiDAR depth into ORB-SLAM2) is portable, but it banks on a synced IMU and Livox |
| **RGB-L / depth-enhanced VO** | Loose | camera + LiDAR | No | Several reproductions | Idea portable: project LiDAR into image → metric depth for visual features. We don't need it — LiDAR already owns geometry |
| **LVI-SAM** (Shan, ICRA 2021) | Tight (factor graph, GTSAM) | camera + 3D LiDAR + IMU | **Yes** | Mature, widely used | No — needs IMU + 3D LiDAR; vision/LiDAR sub-systems can run solo but joint mode is inertial |
| **R3LIVE / R3LIVE++** (HKU-MARS) | Tight (error-state IKF) | camera + LiDAR + IMU | **Yes** | Mature, open-source | No — IMU-centric; targets radiance-colour reconstruction |
| **FAST-LIVO2** (HKU-MARS, T-RO 2025) | Tight (single ESIKF) | camera + LiDAR + IMU | **Yes** | SOTA, open-source | No (now) — IMU load-bearing; heaviest compute; see [[fast-lio-mid360-orin]] |
| **Boche & Leutenegger** (TUM, ICRA 2024) | Tight (factor graph, OKVIS2 lineage) | camera + LiDAR + IMU | **Yes** | SOTA pose accuracy; occupancy submaps | No (now) — IMU-required; the OKVIS2-X line is the camera+IMU path we already cite ([[visual-inertial-slam]]) |
| **GS-LIVO** (T-RO 2025) | Tight (IESKF) + 3DGS map | camera + LiDAR + IMU | **Yes** | Real-time on Orin NX ([[learned-slam]]) | No (now) — IMU + 3DGS; a Phase-2 dense-map target, not an initial-map front-end |
| **Learned cross-modal registration** (2D3D-MatchNet 2019; CMRNext, EEPNet-V2 2025) | Front-end module | camera ↔ LiDAR | No (registration only) | Research-grade; mostly autonomous-driving | No (now) — solves image↔point-cloud *registration/calibration*, not a full handheld initial-map front-end; immature for indoor consumer use |

Sources for the table rows are listed in **Sources** below.

---

## Why tight fusion is unlikely to help our INITIAL map *now*

Four reasons, grounded in our constraints rather than in the method literature's strengths:

1. **The IMU is the missing ingredient, and we deliberately don't have one.** Every tightly-coupled LVI system in the table (R3LIVE, FAST-LIVO2, LVI-SAM, Boche/Leutenegger, GS-LIVO) is **inertial** — the IMU is what makes joint optimization across the LiDAR/camera rate mismatch worthwhile. Our rig is a handheld USB stereo + 2D LiDAR on a **shared clock but no IMU-grade odometry**, and [[imu-vio-integration-reality]] already records the project decision: *the binding cost of adding an IMU to this rig is time-synchronisation, not the $5 chip, and it is not on the critical path*. Adopting a tight-fusion front-end would force us to solve the very sync/IMU problem we parked — to improve a map our LiDAR-first method already produces at 0.024-class geometry.

2. **The thing fusion would improve is the thing the camera can't do here.** Front-end fusion buys you robustness on **geometrically degenerate** scans (long featureless corridors where LiDAR aliases) by adding visual constraints, and metric depth for visual features. But on our rig the *camera* is the weak geometry source — passive stereo collapses on the blank textureless indoor walls that are the home's dominant surface ([[indoor-cluttered-slam]], and the EDA010/EDA011 floor-plan probes in [[mapping-stack-design]]: rays punch through textureless walls, "no occupancy-grid cleverness fixes bad depth"). Feeding a weak, wall-blind visual front-end **into** the LiDAR geometry risks degrading the one estimate that currently works, not strengthening it. The principle on file — *use the reliable signal, flag the rest unknown* (robust-evidence mapping) — says keep geometry on the reliable sensor.

3. **We already get the loosely-coupled win without the cost.** Our method **is** loosely-coupled fusion: LiDAR geometry + hloc camera poses for cross-validation + camera semantics for object labels. That is exactly the division of labour V-LOAM and CamVox are reaching for (geometry from LiDAR, appearance from camera), implemented at the back-end where it is cheap and where a camera failure can't corrupt the trajectory. The marginal gain of moving that join into the front-end is small for a single-room initial map and is gated on sync we don't have.

4. **Initial-map quality is not our bottleneck.** The mandate is a navigation-anchor map of one room. Our measured ATE (0.024-class from the LiDAR baseline) is already at the level where the *open* gaps are crisp metric walls and object identity — neither of which front-end LiDAR-visual fusion addresses (walls are a passive-stereo depth limit; objects are a detection/segmentation problem → [[mapping-stack-design]], [[indoor-cluttered-slam]]). Fusion would chase trajectory accuracy we don't lack.

### When it *would* become worth revisiting

- **If/when we add a hardware-synced IMU** (e.g. the D435i path in [[imu-vio-integration-reality]], or onboard compute that removes the WiFi clock hop) — then **FAST-LIVO2 / GS-LIVO** become the right target, and that is correctly a **Phase-2** dense-map / onboard-flight decision ([[fast-lio-mid360-orin]], [[learned-slam]]), not an initial-map change now.
- **If LiDAR loop-closure aliases** in a long symmetric corridor, the cheap fix is **iBTC** (LiDAR+camera fused *place recognition*, a drop-in loop-closure module — [[learned-slam]]) — i.e. fuse at the **loop-closure** layer, not the odometry front-end. This is consistent with what we already do (camera = loop-closure + semantics).
- **Loosely-coupled depth-enhanced VO (RGB-L style)** could in principle give the camera metric depth from LiDAR — but only helps if we wanted the *camera* to carry geometry, which we explicitly don't.

---

## Bottom-line recommendation

**Not worth it now.** Do **not** move LiDAR+visual fusion into the initial-map front-end this phase. Every tightly-coupled LiDAR-visual system that would plausibly raise accuracy is **inertial** (R3LIVE, FAST-LIVO2, LVI-SAM, the TUM/OKVIS2 line, GS-LIVO), and our handheld consumer rig deliberately has **no IMU** — adopting tight fusion would force us to first solve the time-synchronisation problem [[imu-vio-integration-reality]] already parked as off-critical-path, in order to improve a map our **LiDAR-first + hloc-cross-val** method already delivers at 0.024-class geometry. We are *already* doing the loosely-coupled fusion that V-LOAM/CamVox reach for — LiDAR geometry, camera loop-closure + semantics — at the back-end, where it's cheap and where a wall-blind passive-stereo front-end can't corrupt the trajectory. Keep geometry on the reliable sensor (LiDAR), keep the camera on loop-closure + labels, and **revisit tight LVI fusion (FAST-LIVO2 / GS-LIVO) only in Phase 2, once a hardware-synced IMU or onboard compute is in the rig** — at which point it becomes a dense-map / onboard-flight upgrade, not an initial-map fix. *(Honest uncertainty: this is a single-room, slow-motion, good-light regime; if a later full-circuit sweep shows the LiDAR front-end aliasing in long symmetric corridors, the right response is camera-fused **loop closure** ([[learned-slam|iBTC]]), not front-end odometry fusion.)*

---

## Sources

- [src: zhang-singh-vloam] J. Zhang & S. Singh, *Visual-LiDAR Odometry and Mapping: Low-drift, Robust, and Fast* (V-LOAM), ICRA 2015 — loosely-coupled visual-motion-prior → LiDAR-refine, **no IMU required**. https://ieeexplore.ieee.org/document/7139486 ; and *Real-time depth-enhanced visual odometry*, Autonomous Robots 2017. https://doi.org/10.1007/s10514-015-9525-1
- [src: vloam-scale-2023] *Visual-LiDAR Odometry and Mapping with Monocular Scale Correction and Visual Bootstrapping*, arXiv 2304.08978 (2023) — modern V-LOAM-lineage, loosely-coupled. https://arxiv.org/pdf/2304.08978
- [src: camvox-icra2021] Zhu, Zheng et al., *CamVox: A Low-cost and Accurate Lidar-assisted Visual SLAM System*, ICRA 2021 (arXiv 2011.11357) — LiDAR depth injected into ORB-SLAM2; Livox + (HW-synced) IMU; auto LiDAR-camera calibration. https://arxiv.org/abs/2011.11357 · code https://github.com/ISEE-Technology/CamVox
- [src: stereo-lidar-loose-2024] *Stereo and LiDAR Loosely Coupled SLAM Constrained Ground Detection*, Sensors 2024, 24(21):6828 — loosely-coupled stereo+LiDAR, no joint optimization. https://www.mdpi.com/1424-8220/24/21/6828
- [src: lvisam-icra2021] T. Shan et al., *LVI-SAM: Tightly-coupled LiDAR-Visual-Inertial Odometry via Smoothing and Mapping*, ICRA 2021 — factor graph (GTSAM); vision/LiDAR can run solo, joint mode needs IMU. https://github.com/TixiaoShan/LVI-SAM
- [src: r3live-arxiv] J. Lin & F. Zhang, *R3LIVE / R3LIVE++: A Robust, Real-time, Radiance reconstruction package with a tightly-coupled LiDAR-Inertial-Visual state Estimator* (HKU-MARS), arXiv 2209.03666 — error-state IKF, IMU-centric. https://arxiv.org/pdf/2209.03666
- [src: fastlivo2-tro2025] C. Zheng et al., *FAST-LIVO2: Fast, Direct LiDAR-Inertial-Visual Odometry*, IEEE T-RO vol. 41, pp. 326–346, 2025 — single ESIKF tightly coupling IMU+LiDAR+image. https://doi.org/10.1109/TRO.2024.3502198
- [src: boche-icra2024] S. Boche, S. Barbas Laina, S. Leutenegger (TUM), *Tightly-Coupled LiDAR-Visual-Inertial SLAM and Large-Scale Volumetric Occupancy Mapping*, ICRA 2024 (arXiv 2403.02280) — OKVIS2-lineage factor graph; correspondence-free probabilistic LiDAR residuals; **IMU required**. https://arxiv.org/abs/2403.02280
- [src: okvis2x-arxiv] *OKVIS2-X: Open Keyframe-based Visual-Inertial SLAM Configurable with Dense Depth or LiDAR, and GNSS*, arXiv 2510.04612 (2025) — the configurable OKVIS2 line, visual-inertial core. https://arxiv.org/pdf/2510.04612
- [src: cross-modal-reg-2025] *2D3D-MatchNet* (ICRA 2019); *CMRNext* (IEEE T-RO 2025, arXiv); *EEPNet-V2: Patch-to-Pixel cross-modal registration*, arXiv 2503.15285 (2025) — learned image↔point-cloud registration/calibration front-ends (not full handheld SLAM). https://arxiv.org/pdf/2503.15285
- [src: prototype] drone-prototype EDA064 pose graph; EDA010/EDA011 floor-plan probes; EDA003 hloc bake-off — carried via [[mapping-stack-design]], [[relocalization-method-bakeoff]], [[2d-lidar-slam]] (ATE 0.024 LiDAR vs 0.163 visual).

## Related

- [[slam]] — concept hub: localization + mapping + loop-closure; VIO vs LIO front-ends
- [[2d-lidar-slam]] — our LiDAR geometry baseline and the 0.024-vs-0.163 ATE comparison
- [[visual-inertial-slam]] — the camera+IMU (OKVIS2) front-end; metric scale for visual methods
- [[fast-lio-mid360-orin]] — the LIO/LIV build path (incl. FAST-LIVO2 fork) for a future IMU-equipped rig
- [[learned-slam]] — GS-LIVO (tight LVI on Orin), iBTC (LiDAR+camera fused loop closure), DPV-SLAM
- [[indoor-cluttered-slam]] — featureless-wall + symmetric-corridor failure modes that motivate (and limit) fusion
- [[imu-vio-integration-reality]] — why our rig has no IMU and what adding one really costs (the hinge for tight fusion)
- [[mapping-stack-design]] — where the initial map sits; the EDA010/011 passive-stereo depth limit
- [[relocalization-method-bakeoff]] — hloc as the camera front-end we cross-validate with
- [[lidar-vs-vision-autonomy]] — the LiDAR-vs-vision conflict this fusion question lives inside
- [[passive-stereo-robustification]] — the consumer-cost ladder (IMU→VIO→active stereo) that gates fusion
- [[home-tidy-drone-prototype]] — the parent build this serves
