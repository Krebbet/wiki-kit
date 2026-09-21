# From 2D LiDAR to an Accurate Vector Floor Plan

The pipeline that turns a spinning 2D LiDAR into a metric, vectorized floor plan has five stages — **scan matching**, **pose-graph optimization**, **map accumulation**, **line extraction**, and **polygon assembly** — plus a sixth question that decides whether the plan is honest: telling a real doorway from a wall region that was simply never scanned. The first four stages are usually described as solved. This page argues that two of the load-bearing conclusions the field (and this project) has drawn from them are wrong.

**On closure:** the literature does not assemble polygons from *observed* corners. It partitions space with *extended* wall lines and selects a watertight subset by global optimization, so the corner never has to be seen. Turner & Zakhor's line-of-sight carving of a Delaunay triangulation is a near drop-in for our data and makes closure a type guarantee rather than an emergent hope — which means **E13 ("closed polygon is sensor-bound") is formulation-bound, not sensor-bound**.

**On the ceiling:** the two-layer architecture of pairwise registration followed by pose-graph optimization has a *measured* accuracy ceiling that a joint pose-and-map solve clears by a wide margin — pairwise registration *"only considers the overlap among two scans at a time, while the overlap is really shared by all scans,"* and pose-graph optimization ignores map consistency entirely. So part of what we have attributed to sensor limits is architecture. Alongside this: with no wheel odometry we are running PLICP in its documented worst case, most of the famous robust back-ends (DCS, max-mixtures, RRR) fail *silently* without an odometry backbone, and un-deskewed yaw at 30–60 °/s injects 8–16 cm at room ranges — a live candidate cause of an open project bug.

The page also covers the doorway question, for which the answer is specific and cheap (per-ray visibility labelling: `occupied` / `empty` / `occluded`), the Manhattan prior (test it, then soft-constrain — never snap), and the pitfalls, including a source-verified proof that our sensor's intensity channel is a hard-coded constant.

## Source

| Tag | Work | Venue / Year |
|---|---|---|
| censi-plicp | Censi — *An ICP variant using a point-to-line metric* (PLICP; `csm` / Canonical Scan Matcher) | ICRA 2008 |
| censi-crb | Censi — *On achievable accuracy for range-finder localization* (Cramér-Rao bound; degenerate corridor/circle cases) | ICRA 2007 |
| censi-icpcov | Censi — *An accurate closed-form estimate of ICP's covariance* | ICRA 2007 |
| olson-csm | Olson — *Real-Time Correlative Scan Matching* | ICRA 2009 |
| biber-ndt | Biber & Straßer — *The Normal Distributions Transform: a new approach to laser scan matching* | IROS 2003 |
| li-feature-scanmatch | Li, Zhong, Hu, Ai — *Feature-Based Laser Scan Matching and Its Application for Indoor Mapping* | Sensors 16(8):1265, 2016 |
| lv-thesis | Lv Jixin — *Scan Matching and SLAM for Mobile Robot in Indoor Environment* | Hokkaido Univ. thesis, 2016 |
| mclean-icet | McLean, Wilson et al. — *ICET Online Accuracy Characterization for Geometry-Based Laser Scan Matching* (arXiv 2306.08690) | NAVIGATION 71(2), 2024 |
| deschenes-deskew | Deschênes, Baril, Kubelka, Giguère, Pomerleau — *Lidar Scan Registration Robust to Extreme Motions* (arXiv 2105.01215) | CRV 2021 |
| kummerle-slam-metrics | Kümmerle, Steder, Dornhege, Ruhnke, Grisetti, Stachniss, Kleiner — *On Measuring the Accuracy of SLAM Algorithms* | Autonomous Robots 27(4), 2009 |
| occupancy-slam | *Occupancy-SLAM: joint optimisation of poses and the occupancy map* (arXiv 2502.06292) | 2025 (ext. of RSS 2022) |
| droeschel-ct-slam | Droeschel & Behnke — *Efficient Continuous-time SLAM for 3D Lidar-based Online Mapping* (arXiv 1810.06802) | ICRA 2018 |
| park-elastic-lidar | Park, Moghadam, Kim, Elfes, Fookes, Sridharan — *Elastic LiDAR Fusion: Dense Map-Centric Continuous-Time SLAM* (arXiv 1711.01691) | ICRA 2018 |
| razlaw-registration-eval | Razlaw, Droeschel, Holz, Behnke — *Evaluation of Registration Methods for Sparse 3D Laser Scans* | ECMR 2015 |
| hu-mapeval | Hu et al. — *MapEval* (arXiv 2411.17928) | 2025 |
| adolfsson-coral | Adolfsson, Castellano-Quero, Magnusson, Lilienthal, Andreasson — *CorAl: Introspection for robust radar and lidar perception* (arXiv 2205.05975) | Robotics & Autonomous Systems 2022 |
| pomerleau-review | Pomerleau, Colas, Siegwart — *A Review of Point Cloud Registration Algorithms for Mobile Robotics* | Found. & Trends in Robotics 4(1), 2015 |
| cartographer-icra2016 | Hess, Kohler, Rapp, Andor — *Real-Time Loop Closure in 2D LIDAR SLAM* (Google Cartographer) | ICRA 2016 |
| slam-toolbox-joss | Macenski & Jambrecic — *SLAM Toolbox: SLAM for the dynamic world* | JOSS 2021 |
| nguyen-line-comparison | Nguyen, Gächter, Martinelli, Tomatis, Siegwart — *A comparison of line extraction algorithms using 2D range data for indoor mobile robotics* | Autonomous Robots 2007 (ICRA/IROS 2005) |
| borges-aldon-split-merge | Borges & Aldon — *Line Extraction in 2D Range Images for Mobile Robotics* (split-and-merge / IEPF) | J. Intelligent & Robotic Systems 2004 |
| turner-zakhor-2014 | Turner & Zakhor — *Floor Plan Generation and Room Labeling of Indoor Environments from Laser Range Data* | VISIGRAPP/GRAPP 2014 |
| turner-zakhor-2012 | Turner & Zakhor — *Watertight As-Built Architectural Floor Plans Generated from Laser Range Data* | 3DIMPVT 2012 |
| adan-huber-2011 | Adán & Huber — *3D Reconstruction of Interior Wall Surfaces under Occlusion and Clutter* | 3DIMPVT 2011 |
| mura-2014 | Mura, Mattausch, Jaspe Villanueva, Gobbetti, Pajarola — *Automatic room detection and reconstruction in cluttered indoor environments with complex room layouts* | Computers & Graphics 2014 |
| fang-lafarge-2021 | Fang & Lafarge — *Floorplan generation from 3D point clouds: a space partitioning approach* | ISPRS J. Photogrammetry & Remote Sensing 2021 |
| floor-sp | Chen, Liu, Wu, Furukawa — *Floor-SP: Inverse CAD for Floorplans by Sequential Room-wise Shortest Path* | ICCV 2019 (arXiv 1908.06702) |
| heat | Chen, Qian, Furukawa — *HEAT: Holistic Edge Attention Transformer for Structured Reconstruction* | CVPR 2022 (arXiv 2111.15143) |
| roomformer | Yue, Kontogianni, Schindler, Engelmann — *Connecting the Dots: Floorplan Reconstruction Using Two-Level Queries* (RoomFormer) | CVPR 2023 |
| polyroom | Liu et al. — *PolyRoom: Room-aware Transformer for Floorplan Reconstruction* | ECCV 2024 (arXiv 2407.10439) |
| slibo-net | *SLIBO-Net: Floorplan Reconstruction via Slicing Box Representation with Local Geometry Regularization* | NeurIPS 2023 |
| floorsam | Wang et al. — *FloorSAM: SAM-Guided Floorplan Reconstruction with Semantic-Geometric Fusion* | arXiv 2509.15750 (2025) |
| bormann-room-seg | Bormann, Jordan, Li, Hampp, Hägele — *Room Segmentation: Survey, Implementation, and Analysis* | ICRA 2016 |
| thrun-topological | Thrun — *Learning metric-topological maps for indoor mobile robot navigation* (Voronoi critical points) | Artificial Intelligence 1998 |
| yamauchi-frontier | Yamauchi — *A Frontier-Based Approach for Autonomous Exploration* | CIRA 1997 |
| coughlan-yuille-mw | Coughlan & Yuille — *Manhattan World: Compass Direction from a Single Image by Bayesian Inference* | ICCV 1999 |
| schindler-dellaert-atlanta | Schindler & Dellaert — *Atlanta World: An EM Framework for Simultaneous Low-level Edge Grouping and Camera Calibration in Complex Man-made Environments* | CVPR 2004 |
| straub-mmf | Straub, Rosman, Freifeld, Leonard, Fisher — *A Mixture of Manhattan Frames: Beyond the Manhattan World* | CVPR 2014 |
| yunus-manhattanslam | Yunus, Li, Tombari — *ManhattanSLAM* (arXiv 2103.15068) | 3DV 2021 |
| li-structure-slam | Li, Brasch et al. — *Structure-SLAM: Low-Drift Monocular SLAM in Indoor Environments* (arXiv 2008.01963) | RA-L 2020 |
| jeong-fl-slam | Jeong et al. — *Linear Four-Point LiDAR SLAM for Manhattan World Environments* | RA-L 2023 |
| han-somaslam | Han, Hu, Yang, Kim, Kim — *SoMaSLAM: 2D Graph SLAM for Sparse Range Sensing with Soft Manhattan World Constraints* (arXiv 2409.15736) | 2024 |
| joo-optimal-mf | Joo, Oh, Kim, Kweon — *Globally Optimal Manhattan Frame Estimation in Real-time* | CVPR 2016 |
| montefloor | Stekovic, Rad, Fraundorfer, Lepetit — *MonteFloor: Extending MCTS for Reconstructing Accurate Large-Scale Floor Plans* (arXiv 2103.11161) | ICCV 2021 |
| kucner-rose | Kucner, Luperto, Lowry, Magnusson, Lilienthal — *Robust Frequency-Based Structure Extraction* (ROSE, arXiv 2004.08794) | ICRA 2021 |
| luperto-rose2 | Luperto, Kucner, Tassi, Magnusson, Amigoni — *ROSE²* (arXiv 2203.03519) | 2022 |
| beeson-evg | Beeson, Jong, Kuipers — *Towards Autonomous Topological Place Detection Using the Extended Voronoi Graph* | ICRA 2005 |
| anguelov-doors | Anguelov, Koller, Parker, Thrun — *Detecting and Modeling Doors with Mobile Robots* | ICRA 2004 |
| warberg-line-rooms | Warberg, Miksits, Barbosa — *Real-Time Line-Based Room Segmentation and Continuous Euclidean Distance Fields* (arXiv 2402.05236) | 2024 |
| fermin-leon-dude | Fermín-León, Neira, Castellanos — *Incremental contour-based topological segmentation for robot exploration* (DuDe) | ICRA 2017 |
| cueto-occupancy-rooms | Cueto Zumaya, Catalano, Peña-Queralta, Bessa — *Occupancy-Grounded Room Segmentation for Hierarchical 3D Scene Graphs* (arXiv 2606.13727) | 2026 |
| luperto-predict-layout | Luperto, Fochetta, Amigoni — *Exploration of Indoor Environments Predicting the Layout of Partially Observed Rooms* (arXiv 2004.06967) | AAMAS 2020 |
| sunderhauf-switchable | Sünderhauf & Protzel — *Switchable Constraints for Robust Pose Graph SLAM* | IROS 2012 |
| agarwal-dcs | Agarwal, Tipaldi, Spinello, Stachniss, Burgard — *Robust Map Optimization using Dynamic Covariance Scaling* | ICRA 2013 |
| olson-agarwal-maxmix | Olson & Agarwal — *Inference on networks of mixtures for robust robot mapping* | RSS 2012 |
| latif-rrr | Latif, Cadena, Neira — *Robust Loop Closing Over Time* / *RRR: Realizing, Reversing, Recovering* | RSS 2012 / ICRA 2013 |
| yang-gnc | Yang, Antonante, Tzoumas, Carlone — *Graduated Non-Convexity for Robust Spatial Perception* | RA-L 2020 |
| mangelson-pcm | Mangelson, Dominic, Eustice, Vasudevan — *Pairwise Consistent Measurement Set Maximization for Robust Multi-robot Map Merging* | ICRA 2018 |
| olson-scgp | Olson — *Recognizing places using spectrally clustered local matches* (SCGP; λ₁/λ₂ ambiguity test) | Robotics & Autonomous Systems 57(12), 2009 |
| neira-jcbb | Neira & Tardós — *Data association in stochastic mapping using the joint compatibility test* | IEEE T-RA 17(6), 2001 |
| sunderhauf-comparison | Sünderhauf & Protzel — *Switchable Constraints vs. Max-Mixture Models vs. RRR — A Comparison of three Approaches to Robust Pose Graph SLAM* | ICRA 2013 |
| choi-robust-indoor | Choi, Zhou, Koltun — *Robust Reconstruction of Indoor Scenes* (line process; all-pairs + joint solve) | CVPR 2015 |
| zhou-fgr | Zhou, Park, Koltun — *Fast Global Registration* | ECCV 2016 |
| liu-balm | Liu & Zhang — *BALM: Bundle Adjustment for LiDAR Mapping* (arXiv 2010.08215) | RA-L 6(2), 2021 |
| liu-balm2 | Liu, Liu, Zhang — *Efficient and Consistent Bundle Adjustment on LiDAR Point Clouds* (arXiv 2209.08854) | T-RO 39(6), 2023 |
| lu-milios | Lu & Milios — *Globally Consistent Range Scan Alignment for Environment Mapping* | Autonomous Robots 4(4), 1997 |
| grisetti-graphslam-tutorial | Grisetti, Kümmerle, Stachniss, Burgard — *A Tutorial on Graph-Based SLAM* | IEEE ITS Magazine 2(4), 2010 |
| tipaldi-flirt | Tipaldi & Arras — *FLIRT — Interest Regions for 2D Range Data* | ICRA 2010 (ext. ISER 2010) |
| tipaldi-gfp | Tipaldi, Spinello, Burgard — *Geometrical FLIRT Phrases for Large Scale Place Recognition in 2D Range Data* | ICRA 2013 |
| himstedt-glare | Himstedt, Frost, Hellbach, Böhme, Maehle — *Large Scale Place Recognition in 2D LIDAR Scans using Geometrical Landmark Relations* (GLARE) | IROS 2014 |
| lajoie-aliasing | Lajoie, Hu, Beltrame, Carlone — *Modeling Perceptual Aliasing in SLAM via Discrete-Continuous Graphical Models* (arXiv 1810.11692) | RA-L 2019 |
| kaess-isam2 | Kaess, Johannsson, Roberts, Ila, Leonard, Dellaert — *iSAM2: Incremental Smoothing and Mapping Using the Bayes Tree* (GTSAM) | IJRR 2012 |
| kummerle-g2o | Kümmerle, Grisetti, Strasdat, Konolige, Burgard — *g²o: A General Framework for Graph Optimization* | ICRA 2011 |
| rplidar-c1-specs | SLAMTEC — *RPLIDAR C1 Introduction and Datasheet* rev 1.0 (model C1M1-R2), 2023-10-13 | vendor |
| slamtec-sdk | SLAMTEC RPLIDAR SDK source (`sl_lidar_cmd.h`, `handler_capsules.cpp`) and `rplidar_ros/src/rplidar_node.cpp` | vendor source |
| koch-specular | Koch, May, Nüchter — *Detection and Purging of Specular Reflective and Transparent Object Influences in 3D Range Measurements* | ISPRS Archives XLII-2/W3, 2017 |
| foster-rfm | Foster, Johnson, Kuipers — *The Reflectance Field Map: Mapping Glass and Specular Surfaces in Dynamic Environments* | ICRA 2023 |
| yang-wang-mirrors | Yang & Wang — *Dealing with Laser Scanner Failure: Mirrors and Windows* | ICRA 2008 |
| jiang-glass-confidence | Jiang, Miyagusuku, Yamashita, Asama — *Online glass confidence map building using laser rangefinder for mobile robots* | Advanced Robotics 34(23), 2020 |
| weerakoon-cartographer-glass | Weerakoon, Herr, Blunt, Yu, Chopra — *Cartographer_glass: 2D Graph SLAM Framework using LiDAR for Glass Environments* (arXiv 2212.08633) | 2022 |
| mirdanies-sensors | Mirdanies & Saputra — *Experimental review of distance sensors for indoor mapping* | J. Mechatronics, Electrical Power & Vehicular Tech. 8, 2017 |
| jafri-scanner-calib | Jafri et al. — *Characterization and calibration of multiple 2D laser scanners* | PLOS ONE 17(8), 2022 |
| lim-erasor | Lim, Hwang, Myung — *ERASOR* (arXiv 2103.04316) | RA-L / ICRA 2021 |
| kim-removert | Kim & Kim — *Remove, then Revert* (Removert) | IROS 2020 |
| duberg-dufomap | Duberg, Zhang, Jia, Jensfelt — *DUFOMap: Efficient Dynamic Awareness Mapping* (arXiv 2403.01449) | RA-L 2024 |
| zhang-dynremoval-benchmark | Zhang, Duberg, Geng, Jia, Wang, Jensfelt — *A Dynamic Points Removal Benchmark in Point Cloud Maps* (arXiv 2307.07260) | ITSC 2023 |
| habibiroudkenar-dynahull | Habibiroudkenar, Ojala, Tammi — *DynaHull: Density-centric Dynamic Point Filtering in Point Clouds* (arXiv 2401.07541) | JINT 2024 |
| fox-markov-dynamic | Fox, Burgard, Thrun — *Markov Localization for Mobile Robots in Dynamic Environments* | JAIR 11, 1999 |
| hornung-octomap | Hornung, Wurm, Bennewitz, Stachniss, Burgard — *OctoMap* | Autonomous Robots 34(3), 2013 |
| liao-parse-geometry | Liao, Huang, Wang, Kodagoda, Yu, Liu — *Parse Geometry from a Line* (arXiv 1611.02174) | ICRA 2017 |
| lundell-hallucinating | Lundell, Verdoja, Kyrki — *Hallucinating Robots: Inferring Obstacle Distances from Partial Laser Measurements* (arXiv 1805.12338) | IROS 2018 |
| previtali-cluttered-rooms | Previtali, Barazzetti, Brumana, Scaioni — *Towards Automatic Indoor Reconstruction of Cluttered Building Rooms from Point Clouds* | ISPRS Annals II-5, 2014 |
| delhibabu-2dgrid | Delhibabu, Zhukova, Gizzatov — *2D grid map creation based on RGBD-camera and LiDAR data* | Scientific Reports 16, 2026 |
| marder-eppstein-marathon | Marder-Eppstein, Berger, Foote, Gerkey, Konolige — *The Office Marathon* | ICRA 2010 |
| vizzo-kiss-icp | Vizzo, Guadagnino, Mersch, Wiesmann, Behley, Stachniss — *KISS-ICP* (arXiv 2209.15397) | RA-L 8(2), 2023 |
| jia-2d-vs-3d-person | Jia, Hermans, Leibe — *2D vs. 3D LiDAR-based Person Detection on Mobile Robots* (arXiv 2106.11239) | IROS 2022 |
| meyer-delius-changing | Meyer-Delius, Beinhofer, Burgard — *Occupancy Grid Models for Robot Mapping in Changing Environments* | AAAI 2012 |

## Related

[[2d-lidar-slam]] · [[slam-toolbox]] · [[room-shape-topology-methods]] · [[floorplan-reconstruction-methods]] · [[room-segmentation-floor-plan]] · [[global-alignment-wall-refinement]] · [[weak-scan-registration-methods]] · [[learned-point-cloud-registration]] · [[trajectory-refinement-and-fusion]] · [[robust-evidence-mapping-principle]] · [[mapping-stack-design]] · [[dynamic-object-handling]] · [[sensor-weaknesses-and-fixes]] · [[consumer-robot-vacuum-mapping]] · [[anchor-map-protocol]]

> **Rig results (2026-09-17 → 21).** The pipeline this page describes was run on the prototype rover in stop-and-scan mode — office mapped from campaign rests (EDA218) and then autonomously (EDA222 M2: 13 stations, heading p90 0.49°, asserted walls 0.2–0.6 cm, two runs agree to ~1 cm). What held and what the data reversed (register on walls + objects; select stations by quality not sparsity; a far wall looks like an object to one scan; optimiser residuals certify nothing — use own-wall heading and per-station layering; the C1 counts clockwise; rig self-occlusion zones) is folded into [[stop-and-scan-room-mapping]] §What this rig measured; the odometry side is in [[odometry-closed-loop-pipeline]] §What this rig measured. §3's closure question is still open on the rover: furniture flush to a wall is asserted as wall at the 1.1 m plane.

---

## 0. The five-stage pipeline, and where the difficulty actually is

*(synthesis)*

| Stage | Standard answer | Maturity | Our status |
|---|---|---|---|
| 1. Scan matching | Point-to-line ICP (PLICP) **downstream of a coarse pre-aligner** (correlative scan matching) | Solved | Point-to-line confirmed right; **but PLICP is a refiner, not a searcher — and with no odometry we run it as a searcher** (§1) |
| 2. Pose graph | Sparse nonlinear least squares + robust kernel | Solved *for the drift problem* | Done — **but pose-only optimization has a measured ceiling; joint pose+map is a further large win** (§2.4) |
| 3. Map accumulation | Probability grid (5 cm) or accumulated point cloud | Solved | Done — cleaned cloud, 2.5–2.6 cm wall residual |
| 4. Line extraction | **Ordered per-scan** split-and-merge / IEPF; RANSAC only with model selection | Solved | Done — robust consensus on the *accumulated* cloud, the weaker class (§3.1) |
| **5. Polygon assembly** | **Space partition + global labelling, *not* corner assembly** | **The real gap** | **E13 — unsolved** |
| 5b. Doorway vs unmapped | Per-ray visibility labelling (`occupied`/`empty`/`occluded`) | Partially solved; ceiling is real | **Unsolved for us** |

Two structural observations. First, stage 5 is where the field *diverged* into incompatible formulations — corner-assembly, space-partitioning, learned regression — and only space-partitioning is watertight by construction. Second, and less obvious: **stages 1 and 2 are "solved" only in the sense that the drift problem is solved.** The two-layer architecture of pairwise registration followed by pose-graph optimization has a measured accuracy ceiling that a joint pose-and-map solve clears by a wide margin (§2.4) — so some of what we have attributed to sensor limits may be architecture.

---

## 1. Scan matching for 2D LiDAR

### The three canonical algorithms

**PLICP — point-to-line ICP** (Censi, ICRA 2008) replaces the point-to-point residual with the distance from each source point to the *line* through its two nearest neighbours in the reference scan. A laser scan samples a piecewise-linear surface, so the correct correspondence target is the surface, not another sample of it. Censi's headline theoretical result is that the point-to-line minimization is equivalent to a Gauss–Newton step and therefore converges **quadratically** (`‖q_k − q_∞‖ < c‖q_{k−1} − q_∞‖²`) where plain ICP converges linearly, and that it terminates in a **finite** number of steps because point-to-segment correspondences form a finite set. [src: censi-plicp]

> **Both results are weaker than they are usually quoted.** Censi caveats the convergence rate himself: *"These theoretical results are obtained by considering idealized versions of the algorithms, which do not contain the necessary … 'hacks' that make them work in practice… the error function might not always be decreasing if some correspondences are discarded as outliers; moreover, the proof … assumes that the reference surface has bounded derivatives, which is not true in the case of the polyline."* And "finite steps" means the correspondence iteration reaches a fixed point **or a cycle** — not necessarily the right answer. [src: censi-plicp]

**CSM — correlative scan matching** (Olson, ICRA 2009) *exhaustively* evaluates `p(z | x, m)` over a discretized 3-DOF (Δx, Δy, θ) window against a rasterized log-probability grid. The acceleration is a two-level pyramid — Olson uses **3 cm and 30 cm** tables where each low-resolution cell holds the **maximum** of its children, which "guarantees that we will not miss maxima" — so the coarse level provides an admissible upper bound and prunes the fine search. Measured: a (0.5 m, 20°) window costs **246 ms naive → 8.4 ms multi-resolution**; a (4.0 m, 90°) loop-closure-sized window costs **65,282 ms → 86.1 ms**, a ~760× speedup that runs above 10 Hz. [src: olson-csm]

**NDT** (Biber & Straßer, IROS 2003) fits a Gaussian per cell and maximizes the summed likelihood by Newton's method — smooth, differentiable, correspondence-free, with four half-cell-shifted overlapping grids to blunt discretization artefacts (original cell size 100 cm). [src: biber-ndt] *(The paper is paywalled; these mechanics are from secondary sources and its own accuracy claims are unverified here.)*

| Method | Basin | Accuracy ceiling | Covariance | Best role |
|---|---|---|---|---|
| Point-to-point ICP | narrow | discretization-limited | approximate | baseline only |
| **PLICP** | **narrow — see below** | best local accuracy on planar indoor structure | over-optimistic [src: censi-icpcov] | **fine alignment, once seeded** |
| **CSM** | **whole search window** | grid resolution (~3 cm) | **principled, by construction** [src: olson-csm] | **initialization + loop-closure scoring** |
| NDT | wide | cell size; no principled cell-size choice | **badly over-confident** [src: mclean-icet] | coarse alignment / 3D |
| Ceres scan matcher (Cartographer) | narrow | bicubic interpolation beats grid resolution | yes | production local SLAM [src: cartographer-icra2016] |

### ★ PLICP is a good refiner and a poor searcher — and with no wheel odometry we are running it as a searcher

This is the most consequential finding in this section for our rig.

- **Censi's own worst case is large rotation.** In his Experiment 6 (±0.2 m, ±45° perturbation), PLICP put **24.81%** of trials in the >0.05 error bucket versus MbICP 0.75%, IDC 7.32%, and **plain ICP 5.78%** — i.e. PLICP is *less* robust than vanilla ICP to large rotational displacement. His fix is a coarse global pre-aligner (GPM) followed by PLICP, which recovers 99.79%. [src: censi-plicp]
- **On real indoor 2D data with a zero initial guess it fails outright half the time.** Li et al. drew 50 scan pairs from the Intel and MIT CSAIL benchmarks (success = e_x, e_y < 0.1 m and e_θ < 0.03 rad): **PLICP 66% success on Intel, 50% on MIT**, versus polar scan matching 82%/80% and their feature method 100%/100%. [src: li-feature-scanmatch]
- **And it fails to build a coherent map in a room the size of our kitchen.** Lv's thesis ran ICP and PLICP on a **4.5 m × 7 m cluttered office** with a robot making sharp turns: *"neither ICP nor PLICP give satisfactory scan matching results"*; for the corridor, *"[a]lthough PLICP shows a better matching result, several mismatching prevent it to find an accurate trajectory."* The fix that worked was an Iterative-Closest-Normal pre-rotation estimator run **before** PLICP, converging in a constant 3–5 iterations. [src: lv-thesis]

> *(project note — an actionable caution)* Every source that makes PLICP work pairs it with a **coarse pre-aligner**: Censi with GPM, Lv with ICN, Olson with correlative matching. We have **no wheel odometry**, so PLICP's first guess is uninformed — precisely the regime all three papers say it breaks in. Three concrete checks before drawing any conclusion about our matcher: (1) the ROS `laser_scan_matcher` falls through to a **zero-motion prediction** `(0,0,0)` when no odom/IMU/velocity source is configured; (2) its default **`max_iterations = 10`** is thin against PLICP's 7.2-iteration average, so it can stop unconverged silently; (3) `csm`'s **six-way perturbation restart** (re-run from `{±dt,0,0},{0,±dt,0},{0,0,±dθ}` when mean error exceeds a threshold) exists but ships **disabled** (`restart = 0`). All three are free robustness levers. [src: censi-plicp]

**The complementary caution: neither PLICP's nor NDT's self-reported covariance can be trusted.** Censi's own Monte-Carlo study (52 rays, σ = 0.03 m, 300 runs, three environments) found the Hessian estimate pessimistic in a square and moderately optimistic in corridor/circle, with **no estimator reliably conservative** [src: censi-icpcov]. NDT is worse: on the CODD dataset, predicted error bounds contained the actual error only **40% of the time (73/123) for NDT versus 93% (115/123) for ICET** in translation (77% vs 95% in rotation), because NDT *"mischaracterizes ambiguous measurements along flat surfaces as random noise"* [src: mclean-icet]. *(ICET's study is 3D-only; the containment percentages are the trustworthy part of it, not its RMSE table.)* **CSM's covariance is the exception** — because it evaluates a whole likelihood volume it captures *"both major sources of ambiguity: the noise of the sensor itself, and the uncertainty of which query points should associate to which parts of the model,"* against least-squares covariance which is *"conditioned on the data association"* and therefore *"far too confident."* Its one documented flaw: any high-probability region outside the sampled window is invisible to the fit, yielding over-confidence. [src: olson-csm]

**Observability has closed-form degenerate cases.** Censi's Cramér–Rao analysis gives two: **all sensed surfaces locally parallel (a corridor)** and **all concentric (a circle)**. Where the Fisher information is singular, its kernel is the direction of maximum uncertainty — the same "slide" mechanism as [[weak-scan-registration-methods]]. He is explicit that *"the CRB is valid, but weak, for scan matching"* because map uncertainty is unmodelled. [src: censi-crb]

### Why per-scan alignment saturates — and what to do instead

Once every scan sits at its individually optimal pose, the residual map error is **structural, not registrational**. Four escapes, in increasing power, all with measured support:

**1. Scan-to-map, not scan-to-scan.** The definitive indoor-2D comparison is Kümmerle et al., measuring absolute translational error on relative-pose relations across the Radish benchmarks:

| dataset | sequential scan matching | RBPF (GMapping) | **graph mapping** | scan-matching max |
|---|---|---|---|---|
| Aces | 0.173 ± 0.614 | 0.060 ± 0.049 | **0.044 ± 0.044** | 4.869 |
| Intel | 0.220 ± 0.296 | 0.070 ± 0.083 | **0.031 ± 0.026** | 1.168 |
| MIT Killian | 1.651 ± 4.138 | 0.122 ± 0.386 | **0.050 ± 0.056** | 19.467 |
| MIT CSAIL | 0.106 ± 0.325 | 0.049 ± 0.049 | **0.004 ± 0.009** | 3.570 |
| Freiburg 79 | 0.258 ± 0.427 | 0.061 ± 0.044 | **0.056 ± 0.042** | 2.280 |
| Freiburg hospital | 0.434 ± 1.615 | 0.637 ± 2.638 | **0.143 ± 0.180** | 15.584 |

[src: kummerle-slam-metrics] — **sequential scan-to-scan is 4–30× worse in the mean and 5–80× worse in the maximum than graph/scan-to-map on real indoor 2D data.** Note also that ROS `laser_scan_matcher` already mitigates this partially: it is scan-to-**keyframe**, swapping the reference only past `kf_dist_linear = 0.10 m` / `kf_dist_angular = 10°`.

**2. Deskew the scan.** See §6.4 — at our accuracy target this is not optional, and the dominant term is *yaw rate*, not speed.

**3. Joint optimization of poses *and* map, not poses alone.** This is the finding that most directly challenges our locked-map decision. **Occupancy-SLAM** (a 2D method) reports translation MAE/RMSE across three simulations of odometry 0.783/0.984, Cartographer 0.253/0.299, and joint pose+map **0.0064/0.0097** — and critically, **seeding the joint optimizer from Cartographer's already-converged poses still yields a large further improvement**. Their diagnosis: *"Cartographer performs pose graph optimization to adjust the coordinate frames of submaps only when loop closure is detected, leaving errors within the submaps uncorrected… pose graph optimization typically does not enhance the local details of maps, as it focuses solely on optimizing poses without jointly considering the map."* [src: occupancy-slam] *(Caveat: the ~40× figure is simulation, which flatters joint optimizers; their real-data gains are reported as occupancy AUC, not centimetres.)*

**4. Allow the trajectory to deform — a rigid pose per scan may be the wrong model.** Droeschel & Behnke show continuous-time refinement improving an already-converged map: Deutsches Museum mean map entropy (lower = crisper) Cartographer **−2.04**, rigid-pose baseline −2.12, continuous-time refinement *of Cartographer* **−2.34**, their cubic-B-spline per-scan-line interpolation **−2.42** [src: droeschel-ct-slam]. Elastic LiDAR Fusion reproduces full batch optimization to **0.041 m over 130 m in a 10 × 6 m meeting room** and 0.047 m over 330 m in a 20 × 20 m space, with surfel fusion *"up to three times less noisy"* than the raw cloud on floor patches [src: park-elastic-lidar]. Koide et al. warn about the shortcut, though: deformation-graph methods without full trajectory estimation *"may disrupt the global consistency of the map."*

> **Why a rigid per-scan fit cannot absorb intra-scan skew** — Deschênes et al. state the mechanism cleanly: *"ICP will thus find a transformation that distributes this alignment error throughout the whole reading… the rigid transformation T will not represent the actual displacement of the lidar… if a skewed reading is merged into the map, the newly added points will blur the overall structure."* [src: deschenes-deskew] This is the bridge between §6.4 and the saturation ceiling: some of what looks like an irreducible band may be un-deskewed motion that no rigid pose can remove.

### ★ How to grade the result — and how not to

Three independent sources say a crispness/band-thickness metric alone is the wrong scorecard:

- **It is structurally blind to global warp.** MapEval: MME *"does not reflect any global geometric property"*; existing metrics' *"evaluation scope is restricted to local shape analysis without considering any global geometry."* [src: hu-mapeval]
- **It can rank the *worse* map higher.** Razlaw et al. exhibit two maps of similar ATE where the visibly worse alignment scores the better MME, because large errors scatter points into sparse regions and degenerate the neighbourhood search. Their recommendation: *"only use metrics such as the MME and the MPV… in combination with trajectory errors such as the ATE."* [src: razlaw-registration-eval] **This independently corroborates the project's standing caution that self-scored fit metrics produce false rescues** (memory `scan-to-consensus-seat-and-misaligned-tail`).
- **Local and global accuracy can differ by two orders of magnitude on the same run.** Cartographer's Freiburg hospital result is **local 0.108 ± 0.194 m versus global 5.224 ± 6.623 m** [src: cartographer-icra2016].

**The right validation template is Cartographer's own tape-measure test.** On a sub-$30 Neato Revo LDS at 5 cm resolution they measured five straight spans against laser tape: 4.09→4.08 (−0.2%), 5.40→5.43 (+0.6%), 8.67→8.74 (+0.8%), 15.09→15.20 (+0.7%), 15.12→15.23 (+0.7%) m [src: cartographer-icra2016]. Absolute errors of 1–11 cm — and, more informatively, **a consistent +0.7% stretch on the long spans, i.e. a systematic scale/warp bias that no per-scan noise statistic would ever reveal.** This is the template our floor plan should be graded against.

*(One metric built for our regime: **CorAl** works in ℝ² as well as ℝ³ and targets sub-0.4 m indoor alignment — but its authors warn it *"may also be overly sensitive when used together with a registration method… that does not compensate movement distortion,"* so an un-deskewed scan reads as misaligned even when its pose is correct [src: adolfsson-coral]. Deskew first, then measure.)*

### One taxonomy correction

**CSM is not a competitor to PLICP — `csm` (the Canonical Scan Matcher) *is* the reference PLICP implementation.** Olson's *correlative* scan matcher is the distinct algorithm. The two are complementary halves of the standard coarse-to-fine architecture, which Pomerleau et al.'s survey confirms is the norm: *"reduce local minima possibilities with coarse alignment methods and continue with more precise but computationally more expensive methods."* [src: pomerleau-review] No published paper benchmarks PLICP vs NDT vs GICP vs point-to-point on indoor **2D** data; the ranking has to be assembled from the partial studies above.

---

## 2. Pose-graph SLAM and loop closure in a single small room

**The conclusion of this section is unusually strong: loop closure is the wrong lever for one densely-observed room, and most of the standard robust back-ends are actively *unsafe* without an odometry backbone.** Four independent lines of evidence follow.

### 2.1 In one small room, loop-closure detection is structurally inapplicable

**SLAM Toolbox's loop closure literally cannot fire.** `MapperGraph::FindPossibleLoopClosure` first calls `FindNearLinkedScans` — a breadth-first traversal of the pose graph returning every scan reachable through graph links within `loop_search_maximum_distance` (default **3.0 m**) — and then **clears the candidate chain** if the candidate appears in that set (*"a linked scan cannot be in the chain"*). In a 5 × 5 m room every scan is graph-linked and within 3 m of every other scan, so the chain is cleared on every iteration and **no chain of ≥ `loop_match_minimum_chain_size` (10) ever accumulates**. The mechanism presumes a re-visit that is *spatially near but graph-distant*, which cannot exist in a single densely-connected room. *(Read from `karto_sdk/src/Mapper.cpp`.)*

**Cartographer's submap trade-off has no valid setting in one room.** Its own tuning documentation states the governing tension: *"Submaps must be small enough so that the drift inside them is below the resolution, so that they are locally correct. On the other hand, they should be large enough to be distinct for loop closure to work properly."* In a kitchen, a submap large enough to be *distinct* is the whole room, and one small enough to be drift-free is indistinct. Compounding this, the defaults `max_constraint_distance = 15 m` and `fast_correlative_scan_matcher.linear_search_window = 7 m` both **exceed the room diameter**, so every node is a candidate against every submap and candidate generation degenerates to "everything." [src: cartographer-icra2016]

**Both systems also require an odometry input we do not have.** SLAM Toolbox demands a valid `odom_frame → base_frame` transform as a hard prerequisite; with no wheel encoders and no IMU it must be synthesized from laser odometry before the stack will run at all.

### 2.2 The "score" that gates a loop closure is an overlap fraction, not a statistic

Worth knowing before trusting any published threshold. Cartographer's branch-and-bound score is, in source, the **mean occupancy probability of the submap grid under the transformed scan points** — a normalized overlap in ~[0,1], with no noise model, no DOF, and no covariance. The same threshold doubles as the B&B pruning bound (the search is seeded with `best score ← min_score`), which is what makes it fast. Validation is the threshold **and nothing else**: `ComputeConstraint`'s three steps are *"1. Fast estimate… 2. Prune if the score is too low. 3. Refine,"* after which the constraint is added with **fixed weights** (`loop_closure_translation_weight = 1.1e4`, `rotation 1e5`) rather than a data-driven covariance. Defaults: `min_score = 0.55`, `huber_scale = 1e1`, `branch_and_bound_depth = 7`.

SLAM Toolbox's "response" has the same shape — the fraction of scan points landing on occupied cells of a **deliberately smeared** correlation grid (`correlation_search_space_smear_deviation: 0.1`), which raises the response for near-misses, i.e. it is tuned for recall over discrimination. It does add two gates Cartographer lacks: a **variance gate** on the positional covariance computed from the response surface (*"was the correlation peak sharp?"*), and a **coarse-then-fine** re-match, with the fine threshold (`loop_match_minimum_response_fine: 0.45`) stricter than the coarse (`0.35`).

> **Two widely over-cited numbers, corrected.** (1) Cartographer's precision table (Aces 98.1%, Intel 97.2%, MIT Killian 93.4%, MIT CSAIL 94.1%, **Freiburg 79 99.8%, Freiburg hospital 77.3%**) counts a true positive as a constraint not violated by more than 20 cm/1° **after solving** — it is *precision-only, self-scored against its own optimized solution*, and the paper states **no recall is reported** because *"the data sets contain no ground truth for them."* (2) The SLAM Toolbox JOSS paper contains **no accuracy numbers at all** — every claim in it is an assertion. [src: cartographer-icra2016, slam-toolbox-joss]

Cartographer's authors are also candid about the tuning dead end on their worst dataset: *"The precision can be improved by raising the minimum score for loop closure detection, **but this decreases the solution quality in some dimensions according to ground truth.**"* There is no setting that buys both.

### 2.3 Most robust back-ends assume an odometry backbone — and fail *silently* without one

This table is the single most decision-relevant thing on the page for our rig. Each method's breakdown behaviour was measured, and the failures are not graceful.

| Mechanism | Measured strength | **Behaviour without an odometry backbone** |
|---|---|---|
| **Huber alone** (what Cartographer ships; SLAM Toolbox ships `loss_function_ = NULL` by *default*) | — | Insufficient: on Manhattan3500 with only **100** injected false closures, *"current back-ends like g2o are not able to converge to a correct solution… despite being supported by so called robust cost functions like the Huber function"* [src: sunderhauf-switchable] |
| **Switchable Constraints** | 2,500 trials, 0→1000 outliers, **exactly 2 failures**; survived a **111.9% outlier ratio** on Intel; recall >99.99% at 100% precision; quality flat over 0.3 ≤ ξ ≤ 1.5 [src: sunderhauf-switchable] | Best of the family, but its documented failure is **groups of mutually-consistent false positives** in *"degenerate environments consisting of distinctive parts that are only sparsely interconnected"* — which is what parallel cabinet fronts generate |
| **DCS** | Converges with **5,000 outliers**; ≤6 iterations vs SC's 15–20; Bicocca **1.56 s vs RRR's 314 s** [src: agarwal-dcs] | ⚠️ **Scored TPR = 0.0 — it turned off *every* inter-map factor** when it lacked a good initialization [src: mangelson-pcm]. Its authors explain why: on pose graphs *"every node is constrained by two odometry edges **which are not subjected to being an outlier**"*; remove that guarantee and the family degrades [src: agarwal-dcs] |
| **Max-Mixtures** | Manhattan online with 4000 false edges: MSE **0.83 vs 896**; robustness improves monotonically with node degree [src: olson-agarwal-maxmix] | ⚠️ **The worst pick for us.** On two *outlier-free* datasets it rejected **all 26 loop closures on `Ring` and all 901 on `RingCity`** — zero recall on clean data — because *"the maximum likelihood selection scheme… is prone of picking the wrong mixture component when the error of the initial guess (i.e. according to odometry) is very high"* [src: sunderhauf-comparison] |
| **RRR** | Bicocca P=1.0 / R=0.65 / RMSE **1.0 m** vs raw BoW 55.5 m; O(n) in clusters vs JCBB's O(2ⁿ) [src: latif-rrr] | ⚠️ **Not applicable.** Its χ² apparatus measures how much the **odometry** must deform to accept a cluster; its stated assumption is *"the errors in odometry links are small."* No odometry ⇒ no test statistic |
| **GNC** | **Current standard practice** (ships as `gtsam::GncOptimizer`, GM and TLS). On the 2D indoor laser pose graphs: **INTEL 70–80%**, **CSAIL robust to 90%** outliers, with GNC-TLS dominating; iteration count roughly *constant* in outlier rate; 22–23 ms vs RANSAC's 218 ms at 80% outliers [src: yang-gnc] | ✅ **Starts convex** by schedule (`μ = c̄²/(2r²_max − c̄²)` for TLS, annealed ×1.4), so it needs no inlier guess. Authors note DCS and PCM *"errors gradually increase with the percentage of outliers"* while GNC stays flat |
| **PCM** | City10000 with internally-consistent aliased outliers: **Trans. MSE 0.276 / TPR 0.997 / FPR 0.001**, vs RANSAC-1% 5.688 and DCS 183,077.9. Real NCLT at **~91% outlier fraction**: PCM 10 TP / 3 FP, **DCS 0 TP** [src: mangelson-pcm] | ✅ **Initialization-free.** Its metric composes the transform around the 4-link loop `(⊖z_ik) ⊕ x̂_ij ⊕ z_jl ⊕ x̂_lk`, whose normalized squared error follows **χ² with DOF = state dimension → χ²₃ in 2D** — so the threshold is set from theory, not tuning. Insensitive to γ below ~85% likelihood |
| **SCGP + the λ₁/λ₂ test** | Intel 875 poses / 15,611 hypotheses → 12,900 accepted, **715 rejected as *ambiguous***; DLR with GT association **2,043 good accepted, 0 bad** [src: olson-scgp] | ✅ **The alarm we specifically want.** Soft consistency `A_ij = exp(−TᵀΣ_T⁻¹T)`, dominant eigenvector for the cluster — and because the **second** eigenvector is an orthogonal, genuinely *different* explanation of the data, **λ₁/λ₂ is an ambiguity metric; Olson rejects the whole hypothesis set when λ₁/λ₂ < 2** |

Olson names our failure mode directly: *"In indoor environments (**where there is often repeated structure**), the probability of an incorrect match increases with the uncertainty of the prior. These hypotheses can be incorrect when physically distinct environments are similar looking."* His organizing principle is the one to build on — **correct hypotheses all agree with each other, because there is only one true configuration, whereas incorrect hypotheses tend to be incorrect in different ways** [src: olson-scgp].

The only head-to-head of SC/MM/RRR declines to crown a winner: *"we would have preferred to report that one of the three evaluated algorithms performed clearly superior… **However, this is not the case.**"* [src: sunderhauf-comparison]

**The χ² gate, concretely.** A 2D scan-to-scan constraint is 3-DOF, and a residual composed around a cycle is still a single SE(2) pose, so the test statistic is **χ²₃**: 90% → 6.251, **95% → 7.815**, **99% → 11.345**, 99.9% → 16.266. Use it as an outlier *prior*, not as the decision — Neira & Tardós's central point is that individual compatibility does **not** imply joint compatibility, *"because the predicted measurements are always correlated because they are affected by the same robot position error,"* and IC's discriminating power collapses precisely as pose uncertainty grows relative to sensor noise [src: neira-jcbb].

### 2.4 "Verify each pair harder" is empirically capped — the joint solve is where the precision is

The closest published analogue to our problem is Choi, Zhou & Koltun: one indoor scene, ~50 fragments, all pairs tested, no reliable odometry across fragments. **Pairwise registration precision across six algorithms was 1.6% / 8.9% / 10.4% / 7.1% / 14.0% / 19.6% — the best under 20%.** Their diagnosis is our diagnosis: *"limited discriminative power of surface geometry… **This aliasing permits reasonable recall but limits precision.** Some false positive alignments are very plausible when considered independently."* Their conclusion was to stop trying: *"**rather than attempt to develop a pairwise surface registration procedure with high recall and near-perfect precision**, we show that these characteristics can be achieved by a **global analysis of the scene**."* [src: choi-robust-indoor]

And the joint solve delivered, at almost no cost in recall:

| | before pruning (Recall / Precision) | after joint line-process solve |
|---|---|---|
| Living room 1 | 61.2 / 27.2 | 57.6 / 95.1 |
| Living room 2 | 49.7 / 17.0 | 49.7 / 97.4 |
| Office 1 | 64.4 / 19.2 | 63.3 / 98.3 |
| Office 2 | 61.5 / 14.9 | 60.7 / **100.0** |
| **Average** | **59.2 / 19.6** | **57.8 / 97.7** |

[src: choi-robust-indoor] — **5× precision for 1.4 points of recall.** The mechanism is a continuous **line process** `l_ij ∈ [0,1]` per putative alignment, optimized *jointly with the poses* and pruned at `l_ij < 0.25`: the same math family as switchable constraints and GNC, but with dense surface residuals rather than abstract pose residuals in the objective. Final surface accuracy 0.04–0.05 m, essentially at the ground-truth-trajectory bound.

Two follow-ons matter. **Fast Global Registration** shows the exhaustive intermediate pairwise stage is *"computationally wasteful"* — scaled Geman–McClure over FPFH correspondences with graduated non-convexity, correspondences computed **once and never recomputed**, matched the pipeline's 0.05 m on 47–57 fragments in **82 s vs 5,220 s** [src: zhou-fgr]. And **BALM/BALM2** show what joint refinement does to *map* quality specifically: minimize point-to-plane/line residuals over all scans jointly with the **plane parameters eliminated in closed form**, leaving only poses as unknowns [src: liu-balm]. BALM2's headline is the number to hold up against our 2.5 cm band — an inspected physical plane had **σ = 6.8 cm before and σ = 1.7 cm after**, and the authors note *"the standard deviation of 1.7 cm… is **exactly the ranging accuracy of the lidar sensor**, which confirms that our method achieves a mapping accuracy at the lidar noise level **as if the sensor had no motion**."* It achieved 4.2 cm ATE on VIRAL with **LiDAR only**, beating a stereo+IMU+LiDAR+UWB fusion at 4.7 cm, and its NEES ≈ 1 over 100 Monte Carlo runs means **its own covariance is trustworthy** — something no scan-match "response" score can offer. [src: liu-balm2]

Their framing of why the two-layer architecture caps out is the cleanest statement of the whole problem:

> *"the pairwise scan registration only considers the overlap among two scans at a time, while the overlap is really shared by all scans and should be registered concurrently. Moreover, the pose graph optimization only considers constraints from the relative poses, **while the mapping consistency indicated by the raw points is completely ignored.** Consequently, it is usually difficult to produce (or even be aware of) a globally consistent map."* [src: liu-balm2]

**The historical point is worth internalizing: the original pose graph *was* the dense all-pairs formulation.** Lu & Milios (1997) built a network over all scan pairs and solved it globally; as the graph-SLAM tutorial confirms, *"Lu and Milios were the first to refine a map by globally optimizing the system of equations… However, it took several years to make this formulation popular due to the comparably high complexity."* The sparse-chain-plus-sparse-loop-closure architecture that Cartographer and Karto inherit is **a later computational compromise** — and it is one we do not need to make on ~1,000 scans in one room. [src: lu-milios, grisetti-graphslam-tutorial]

### 2.5 Skip descriptor-based place recognition entirely

For completeness: 2D LiDAR place recognition does exist and is mature — **FLIRT** (multi-scale curvature detector + polar occupancy histogram; recall at precision 0.95 of **fr079 0.98, intel 0.96, csail 0.89**, scan-to-scan match in **200–450 µs**) [src: tipaldi-flirt], **Geometrical FLIRT Phrases** (>85% recall at 99% precision in <1 s across six datasets) [src: tipaldi-gfp], and **GLARE** (93% recall at 99% precision over 6.5 km, no vocabulary or training) [src: himstedt-glare]. Scan Context does **not** transfer — its bin encoding is the max *height* of points in a bin, which a single-ring 2D scan does not have.

But none of it is worth building here, for four reasons. The problem these methods solve — sub-linear retrieval over 10,000+ scans across kilometres — does not exist at ~1,000 scans in one room, where **exhaustive all-pairs costs roughly 500,000 pairs × 200–450 µs ≈ 2–4 minutes offline, once** [src: tipaldi-flirt]. Candidate generation is not our failure mode; proximity gives ~100% recall by construction, and descriptor retrieval can only *reduce* that (85–93% ceiling) in exchange for speed we do not need. Our environment is these descriptors' documented worst case — GLARE's authors report it *"is slightly worse than GFP on the indoor dataset (intel-lab)… due to **lower variance in relative distances of co-occurring landmarks and the high self-similarity in man-made environments in terms of spatial relations**"* [src: himstedt-glare], and GFP's authors state that *"2D range data offer limited variability in the descriptor space… The most meaningful information is indeed the spatial arrangement of the points"* [src: tipaldi-gfp]. And the real risk is a confidently-wrong match, which no front-end fixes.

*(One idea worth a look if global localization is ever needed: **Free-Space Features** — describing free space rather than surfaces, which is far more distinctive than cabinet-front geometry in a repetitive kitchen. Claimed, not quantified.)*

### 2.6 Solver choice is a features decision, not a performance one

At our scale it is milliseconds in any library: g2o solves Intel (943 poses / 1837 constraints) in **2.5–2.8 ms**; iSAM2 averages **1.74 ms** per incremental step on Intel; Cartographer solves **11,456 nodes / 35,300 edges in ~0.3 s**; SLAM Toolbox's maintainer stopped compiling three of its four solver plugins because *"They don't outperform Ceres."* [src: kummerle-g2o, kaess-isam2, cartographer-icra2016]

| | g2o | **GTSAM** | Ceres |
|---|---|---|---|
| SE(2) types built in | ✅ `VertexSE2` / `EdgeSE2` | ✅ `Pose2` / `BetweenFactor` | ✗ hand-write the residual |
| Robust machinery | 9 kernels incl. **`RobustKernelDCS`** | Huber/Cauchy **+ `GncOptimizer` (GM, TLS)** | 7 kernels — **no GNC, no DCS** |
| Marginal covariance | limited | ✅ `Marginals::marginalCovariance` | ✅ `ceres::Covariance` — generic `(JᵀJ)⁻¹`, not SLAM marginals |
| Incremental | batch | ✅ iSAM2 | batch |

**Recommendation: GTSAM.** For repeated cabinet fronts the robust-outlier machinery is the only axis that matters, and GTSAM is the one library shipping GNC. Its `Marginals::marginalCovariance` also tells you **which poses are actually pinned down** — information no scan-match "response" score contains. *(Ceres' own header disclaims the whole question: "In general, there isn't a principled way to select a robust loss function.")*

### 2.7 What to build instead

*(synthesis, but each clause is evidenced above)*

1. **Frame it as multiview bundle registration, not SLAM.** The right ancestors are Lu & Milios 1997 and Choi/Zhou/Koltun 2015 — not Cartographer or Karto.
2. **Brute-force or proximity-gated all-pairs scan matching.** Affordable and ~100% recall by construction. No place recognition.
3. **Keep a continuous robust weight per constraint, never a binary accept/reject.** GNC-TLS via `gtsam::GncOptimizer`, or a line process pruned at `l_ij < 0.25` after convergence.
4. **Eliminate the geometry analytically.** BALM-style: unknowns become poses only, with wall and cabinet-front *lines* solved in closed form. This maps directly onto the project's existing `docs/object-line-fit-algorithm.md` spec.
5. **Add two cheap, initialization-free ambiguity alarms:** PCM's composed-loop χ²₃ consistency test, and **Olson's λ₁/λ₂ ≥ 2** — the latter is designed precisely to shout *"this hypothesis set is ambiguous"* when parallel cabinet fronts offer two equally good global explanations.
6. **Do not use DCS, max-mixtures, or RRR here.** All three assume the odometry backbone we do not have, and all three fail silently (see §2.3).
7. **Watch the cubic term.** BALM2's complexity carries an `M_p³` in pose count, so at the thousands-of-scans scale sub-select exemplar scans or marginalize.

---

## 3. Occupancy grid / point cloud → closed vector polygon (our E13)

This is the section that matters. The literature contains **four distinct formulations** of "line soup → polygon", and they are not interchangeable — they differ in whether closure is a *hope*, a *penalty*, or a *hard constraint*.

### 3.1 Line extraction — the input to all four

The canonical benchmark is Nguyen et al., who compared six algorithms (split-and-merge, incremental/line-tracking, line-regression, RANSAC, Hough transform, EM) on 100 real scans from an 80 m × 50 m office environment against ground truth, on speed, complexity, correctness and precision [src: nguyen-line-comparison]. The conclusions have held up for twenty years:

- **Split-and-merge (IEPF)** is the fastest by a wide margin — reported around **1470–1780 Hz** on their data — because it is divide-and-conquer and exploits the *ordering* of a laser scan [src: nguyen-line-comparison, borges-aldon-split-merge].
- **Incremental** has the **lowest false-positive count**, which the paper flags as the property that matters most for SLAM (a spurious wall is worse than a missed one) [src: nguyen-line-comparison].
- **RANSAC and Hough underperform** on 2D scan data specifically because they **discard the sequential ordering** of the returns, so they happily fit a line through points on two different walls [src: nguyen-line-comparison].

> *(synthesis — relevant to us)* This is a caution on our own robust-consensus fitting: a consensus/RANSAC-family fit over an *accumulated cloud* has no scan ordering to exploit and is therefore in the weaker of the two classes. Where we can, run extraction **per-scan** (ordered, split-and-merge) and merge the resulting segments across scans, rather than fitting the merged cloud. This also makes each segment carry the pose that observed it — which §3.3 needs.

### 3.2 Formulation A — corner assembly (what degrades; what we currently do)

Extract wall segments, intersect neighbouring segments to get corners, chain corners into a ring. This is the intuitive route and it is the one that breaks, for a structural reason: **the ring is only as good as the weakest junction**, and a single missing or occluded junction leaves the ring open, with no mechanism to recover. There is no global objective — closure is an emergent hope.

The measured symptom in this project (EDA069/EDA070) is exactly this: kitchen 12 walls / 5 corners / closed-fraction 0.375; living room 19 / 2 / 0.105; and room-segmentation + furniture-gating moved measured closure **0.375 → 0.389 and 0.105 → 0.0**. The project's conclusion was "closure is sensor-bound — the 2D plane never saw the corners." **The literature's position is that this conclusion follows from the formulation, not from the sensor.** No space-partitioning method requires a corner to be observed; corners are *derived* by intersecting extended lines inside a partition of the plane.

The naive raster variant — trace the free-space contour with `findContours` and simplify with Douglas–Peucker — is worth calibrating against. In the PolyRoom benchmark, a plain Douglas–Peucker baseline scores **Room F1 95.5** but only **Corner F1 80.7** and **Angle F1 55.8** on Structured3D [src: polyroom]. In other words: contour tracing gets the *region* roughly right and the *geometry* badly wrong. It is a good sanity outline and a bad floor plan. (Detail on RDP tolerance behaviour: [[room-shape-topology-methods]] §Family 1.)

### 3.3 Formulation B — space partition + labelling (**watertight by construction**; the recommended fix)

The idea: build a partition of the plane into cells whose boundaries are the candidate walls, label every cell `interior` or `exterior`, and export the **boundary between the two labels** as the polygon. Because the interior is a union of whole cells of a simplicial/polygonal complex, its boundary is a closed curve *by construction* — you cannot produce a dangling wall or an unclosed ring. Closure stops being an outcome and becomes a type guarantee.

**The 2D-LiDAR-native instance is Turner & Zakhor** [src: turner-zakhor-2014, turner-zakhor-2012], and it is close to a drop-in for our data:

1. **Wall samples.** Project returns to the horizontal plane, bin into a quadtree at resolution *r* (**5 cm** works "in even the most cluttered environments"). Each sample stores its 2D position, its height range, **and the set of scanner poses that observed it** — the poses are load-bearing later. From a 3D cloud, require a sample to have vertical coverage over a height *H* (they use **H = 2 m**) so that furniture and cubicle walls are excluded automatically. [src: turner-zakhor-2014]
2. **Delaunay triangulation** of the wall samples. Every triangle starts labelled `exterior`.
3. **Line-of-sight carving.** For each wall sample *p* and each pose *s* that observed it, every triangle the segment (*s*, *p*) crosses is relabelled `interior` — nothing solid can lie along a ray that produced a return. The segment is **truncated** if another wall sample lies between *s* and *p*, so fine structure is never carved away. The same carving is applied along **pose-to-pose** segments, since the platform traversed that space. [src: turner-zakhor-2014]
4. **Export.** The interior/exterior boundary *is* the floor plan — watertight, by the simplicial-complex argument. [src: turner-zakhor-2012]
5. **Rooms by graph cut.** Seed triangles = local maxima of the Delaunay circumradius (the circumradius is a local free-space-width estimate); propagate labels by **min-cut on the triangulation dual**, with edge weight = shared-edge length. Minimizing the cut minimizes inter-room boundary length, i.e. **rooms are separated at the narrowest throats — doorways**. Merge two rooms whose shared border exceeds **2.44 m** (96 in — twice the ADA maximum door width), and iterate to convergence. [src: turner-zakhor-2014]
6. **Simplification.** Boundary-restricted **QEM** (quadric error metrics) collapse, stopped when the induced error would exceed the sampling resolution *r*, and **frozen at vertices shared by two rooms** so doorway detail survives. [src: turner-zakhor-2014]

Reported cost: a full 2.5D extruded model from 2D wall samples in **under 10 s** for their largest models at 5 cm resolution, with the carving step streamable during acquisition [src: turner-zakhor-2014].

The same "partition then globally label" idea appears in three other places worth knowing:

- **Mura et al.** extract candidate wall planes with an *occlusion-aware* process, use them to induce a space partition, and separate rooms by a **robust heat-diffusion process** over that partition — handling highly concave layouts and discovering the number of rooms without being told it [src: mura-2014].
- **Fang & Lafarge** decompose the floor plane into a polygonal partition and **select the wall edges by energy minimization**, explicitly replacing corner detection with a space-partition data structure "offering high robustness to imperfect data"; validated on RGB-D *and* LiDAR clouds including non-rectangular scenes [src: fang-lafarge-2021]. See [[room-shape-topology-methods]] §Family 2 and [[floorplan-reconstruction-methods]] for the PolyFit/KSR cousins.
- **PolyFit**'s binary-linear-programming face selection is the 3D ancestor of the same pattern (hypothesize primitives → globally select a watertight subset) — written up in [[floorplan-reconstruction-methods]].

### 3.4 Formulation C — global search over polygon topology

If you want the polygon itself to be the optimization variable, **Floor-SP** casts floorplan reconstruction as **room-wise coordinate descent, where each room's outline is a shortest-path problem on a corner/edge graph** — a cycle in the graph is a closed polygon, so again closure is structural. Its objective has a data term (from a CNN), a **consistency term forcing adjacent rooms to share corners and walls**, and a **model-complexity term**; notably it "does not require corner/edge primitive extraction," and was evaluated on 527 production RGBD scans of apartments/houses **including many non-Manhattan units** [src: floor-sp]. **MonteFloor** replaces the greedy search with **Monte Carlo Tree Search** over room-proposal subsets and uses a *soft* angle prior rather than a Manhattan snap ([[floorplan-reconstruction-methods]]).

*(synthesis)* The transferable idea for a single room without any learning: define a **corner-candidate graph** whose nodes are pairwise intersections of extended fitted wall lines and whose edge costs measure how much LiDAR evidence supports the segment between two candidate corners (plus a per-corner complexity penalty), then find the **minimum-cost cycle**. A cycle is closed by definition; occluded corners are *inferred* intersections that cost little because their flanking evidence is strong.

### 3.5 Formulation D — learned polygon regression

Current SOTA maps a **256×256 top-view point-density image** to a vectorized polygon end-to-end [src: polyroom]. Structured3D results:

| Method | Venue | Room F1 | Corner F1 | Angle F1 |
|---|---|---|---|---|
| Douglas–Peucker baseline | — | 95.5 | 80.7 | 55.8 |
| Floor-SP | ICCV 2019 | 88. | 76. | 75. |
| MonteFloor | ICCV 2021 | 95.0 | 82.5 | 80.5 |
| HEAT | CVPR 2022 | 95.4 | 82.5 | 78.3 |
| RoomFormer | CVPR 2023 | 97.3 | 87.2 | 81.2 |
| SLIBO-Net (Manhattan) | NeurIPS 2023 | **98.4** | 85.4 | 84.4 |
| **PolyRoom** | ECCV 2024 | 98.3 | **90.2** | **85.2** |

[src: polyroom]

Two readings matter. First, the *angle* column is where the classical baseline collapses (55.8) and where learning buys the most — angle correctness is the topology-and-regularity signal, and it is precisely what corner assembly gets wrong. Second, **PolyRoom beats Manhattan-assuming SLIBO-Net on corner F1 by 4.8 points while matching it on rooms** [src: polyroom] — i.e. at current model quality the Manhattan prior is no longer buying accuracy (see §4).

**FloorSAM** (2025) is the most directly relevant recent system for *our* data type: it builds a top-down LiDAR **density map** with grid filtering and adaptive-resolution projection, uses **SAM zero-shot** segmentation with adaptive prompt points and multistage filtering to get room masks, then does joint mask + point-cloud analysis for contour extraction, regularization and topology recovery [src: floorsam]. It reports better accuracy/recall/robustness than traditional methods on the Giblayout and ISPRS datasets, "especially in noisy and complex settings" — but the abstract does not publish the numbers, so treat this as **claimed, not verified**. Its value to us is the architecture: a foundation model supplies the *region* topology and classical geometry supplies the *metric* edges. That is a plausible route for a one-room prototype with no training budget.

> *(synthesis)* All learned methods here are trained on **Structured3D** (synthetic, whole-apartment, mostly rectilinear). A single kitchen captured on one horizontal scan plane is out of distribution on layout, scale, and noise. Use them as an oracle to check a classical result, not as the pipeline.

### 3.6 Verdict on E13

| Formulation | Closure guarantee | Needs training | Needs observed corners | Fit for us |
|---|---|---|---|---|
| A — corner assembly | none | no | **yes** | **This is what fails.** |
| A′ — contour + RDP | closed but wrong geometry (Angle F1 55.8) | no | no | Sanity outline only |
| **B — space partition + labelling** | **hard constraint** | **no** | **no** | **Recommended** |
| C — global topology search | structural (cycle) | Floor-SP yes; hand-rolled variant no | no | Good second step |
| D — learned regression | soft (loss) | yes, OOD for us | no | Cross-check only |

The claim "closure is sensor-bound" is **true only for Formulation A**. Turner & Zakhor's carving builds the interior region from *rays*, not from corners, so an occluded corner simply becomes a Delaunay triangle labelled interior by a ray that passed on either side of it — no observation of the corner is required at any point in the pipeline [src: turner-zakhor-2014].

---

## 4. Manhattan / rectilinear priors: when they help, when they corrupt

### The two assumptions

**Manhattan World** (Coughlan & Yuille, ICCV 1999) assumes the scene is built on a grid of **three mutually orthogonal directions**, plus a secondary assumption that the camera is roughly horizontal. Measured on real images: 23/25 indoor scenes recovered the compass angle within **5°**, 22/25 outdoor within 10° [src: coughlan-yuille-mw]. **Atlanta World** (Schindler & Dellaert, CVPR 2004) relaxes this precisely: **multiple orthogonal *pairs* of horizontal directions, all sharing one vertical (gravity) axis**, each extra pair costing exactly one extra angle parameter [src: schindler-dellaert-atlanta]. The 2D-LiDAR analogue is "walls come from *N* dominant azimuths, not necessarily 2" — and for an indoor floor plan Atlanta is almost always the right prior while Manhattan is the over-commitment.

Notably, Schindler & Dellaert themselves showed the corruption directly: fitting a 3-pair scene with only 2 pairs "caused some edges to be grouped together although they are clearly not parallel," and they suggested their framework "could potentially be used in a model selection scheme" [src: schindler-dellaert-atlanta]. *(Shown qualitatively on figures; the model-selection scheme was proposed, never implemented.)*

### What the prior buys — real numbers

A dominant-direction estimate is a *global* yaw reference, and yaw error is what integrates into position drift. The measured gains are large **where the assumption holds**:

| System | Prior | Measured effect |
|---|---|---|
| FL-SLAM (4-point ToF LiDAR, hard MW) | walls forced parallel to global X/Y | 92.3 m closed-loop corridor final drift **0.350 m** vs Graph-SLAM 1.055 m, L-SLAM 38.4 m; 52.0 m open-loop ATE RMSE **0.660 m** vs 1.990 m [src: jeong-fl-slam] |
| ManhattanSLAM (RGB-D, mixture of MFs) | MF tracking on/off ablation | TAMU Corridor-A drift **0.53 m with** vs **0.77 m without** — the constraint removed ~31% of drift, but a Manhattan Frame was found in only **401 of 2658 frames** [src: yunus-manhattanslam] |
| Structure-SLAM | weak MW, **rotation decoupled from translation** | Drift is dominated by rotation error; get rotation from lines + normals under a weak MW assumption, solve translation separately [src: li-structure-slam] |
| SoMaSLAM (2D graph SLAM, sparse beams, **soft** MW) | penalised, not enforced | 4-beam Intel Lab **0.13 ± 0.21 m** vs 2.80 ± 8.98 m baseline; rotational **2.71 ± 3.01°** vs 15.19 ± 36.00°; MIT Killian 0.91 m vs 17.84 m [src: han-somaslam] |

### What it costs — and why a hard snap is the wrong shape

**Ordinary rooms are not Manhattan, and the evidence is quantitative.** ManhattanSLAM reports, per sequence, how many frames yield a *detectable* Manhattan Frame: TUM **fr2/xyz 0 of 3669 frames**, fr1/xyz 1/798, fr1/desk 1/613, fr2/desk 26/2965 — and on exactly those sequences both hard-MW baselines record **tracking failure** while non-MW methods run fine (ORB-SLAM2 ATE 0.010–0.040 m). On synthetic MW-rendered ICL-NUIM, by contrast, MFs were found in most frames [src: yunus-manhattanslam]. Straub et al. make the same point from annotation: on NYU-Depth-V2 (1449 indoor scenes) **human annotators routinely labelled 2–3 Manhattan frames per ordinary room**, and their sampler matched the annotated frame count in 80–84% of scenes [src: straub-mmf]. A rotated desk or a half-open door is enough to break a single frame [src: han-somaslam].

**A hard snap does not merely fail to help — it invents geometry.** SoMaSLAM shows the hard-MW FL-SLAM on a non-rectilinear library "fails to detect the non-MW features … and instead creates walls that align with the initially declared Manhattan world" [src: han-somaslam]. *(Shown in a figure; no error metric attached.)*

**And you cannot snap to a direction you do not know precisely.** Joo et al. benchmarked Manhattan-frame estimators against NYUv2 ground truth: MPE 20.87°, MMF 12.50°, ES 3.60°, RMFE 3.27°, exhaustive branch-and-bound **2.50°** (117 s), their real-time BnB **2.63°** (0.07 s) [src: joo-optimal-mf]. Even a *globally optimal* estimator lands at ~2.5° on real indoor data. A hard snap therefore bakes in ≥2° of systematic error, which propagates into intersected corners as roughly (wall length × tan 2°) ≈ **17 cm on a 5 m wall**. *(The estimator error is measured [src: joo-optimal-mf] on 3D normals — treat it as an optimistic bound for 2D; the corner-displacement figure is arithmetic.)*

**The floor-plan literature has converged on soft.** MonteFloor's angle regulariser `L_ang` places a mixture-of-Gaussians prior over `cos α` that **discourages flat angles (0°/180°), encourages 90°/270°, and leaves a uniform density over every other angle** — explicitly "different from enforcing Manhattan World conditions as other angles are also accepted." Its ablation: removing `L_ang` drops the ≤5° angle metric from **0.86/0.75 → 0.73/0.68** precision/recall while the *room* metric is unchanged at 0.96/0.94 [src: montefloor]. Roughly 13 points of angular fidelity for free. Independently, PolyRoom — with no Manhattan assumption — beats Manhattan-assuming SLIBO-Net by **+4.8 corner F1** on Structured3D, the most favourable possible ground for the prior [src: polyroom].

### Recommended discipline — test, then soft-constrain

**Step 1 — gate on structure, with a published threshold.** ROSE (Kucner et al., ICRA 2021) gives the cheap, ground-truth-free test we want. Take the 2D DFT of the occupancy/projection image, unfold the amplitude into polar (φ, ρ), form the **cumulative amplitude** `A_C(φ) = Σ_ρ A(φ,ρ)`, and select peaks by **prominence at 50% of relative peak height**. Two decisions fall out: if **no peak survives**, "the map does not contain any dominant directions and is not suitable for further processing"; and the scalar **W = mean scaled cumulative amplitude / mean peak amplitude** measures how structured the map is — ≈0 strongly structured, ≈1 unstructured. Their rule of thumb is **W < 0.2 ⇒ trust the extraction, W > 0.4 ⇒ it has almost certainly failed**, backed by correlations of W with declutter precision of R = −0.566 / −0.826 / −0.863 at 20 / 100 / 180 clutter obstacles [src: kucner-rose]. This also separates pose-graph-optimised maps from odometry-distorted ones.

> **Two warnings from the same paper that apply directly to us.** (1) Median clutter-labelling precision was **>95% on every test environment except `csail`, "a peculiar building with few straight walls"** — the method is not applicable to curved walls. (2) **"If the noise is systematic — e.g. offsetting the position of the walls with a fixed value — the 'fake structure' will be scored equally high as the true one"** [src: kucner-rose]. Given the project's known coherent low-frequency trajectory bow (memory `lidar-cloud-locally-crisp-band-is-bow`, `eda110-refinement-injected-turn-offsets`), a high W-score is **not** proof the extracted directions are the true ones.

**Step 2 — extract directions from the FFT, not raw Hough.** ROSE is explicit that "the Hough transform is not generally suitable for detecting structure" *until* the frequency-domain declutter has run — Hough alone latches onto furniture edges. ROSE² uses the correct order: FFT declutter → probabilistic Hough → cluster by angular coefficient → DBSCAN on spatial proximity → project each segment to its nearest dominant direction → merge collinear wall clusters separated by **less than a doorway width** [src: kucner-rose, luperto-rose2].

**Step 3 — soft-constrain, length-weighted.** SoMaSLAM's residual is the formulation to copy directly. Gate on `|θ₂ − θ₁ − kπ/2| < ε` for k ∈ ℤ, |k| ≤ 2; if it fires, add a landmark–landmark residual `e(l₁,l₂) = θ₂,ideal − θ₂` with information matrix **Ω = (len₁ + len₂)·I** — so long walls constrain hard and short furniture edges barely constrain at all. Violations are penalised, never enforced. One implementation detail they measured: making **one** landmark (not both) the free variable matters — the two-variable form silently dropped 13.8% of landmark–landmark constraints (4832 → 4166 on MIT Killian) and hurt accuracy [src: han-somaslam].

**Step 4 — accept only on an independent gate.** Compare constrained vs free fits by BIC on the wall-residual likelihood *and* report the **held-out wall band**. If the prior increases it, revert — the same accept-only-if-it-improves rule the project already uses (`docs/locked-map.md` step-f). Wall directions are **axial** (mod 180°, or mod 90° under MW), so any averaging must use **doubled angles** — double, take the vector mean, halve. *(Standard directional statistics, Mardia & Jupp; ROSE sidesteps it by working in the FFT's already-symmetric (φ, ρ) space.)*

**Step 5 — or skip the test entirely and detect-or-fall-back.** ManhattanSLAM's pragmatic design is to check per-frame whether an MF exists and switch to unconstrained point/line/plane tracking when it does not; its Table I shows this is best-or-near-best on *both* MW and non-MW sequences (average ATE 0.014 m on ICL-NUIM vs 0.040 m for hard-MW Structure-SLAM) [src: yunus-manhattanslam].

---

## 5. Room segmentation and the doorway problem

### 5.1 Segmentation families, with the benchmark numbers

Bormann et al. (ICRA 2016) is the canonical benchmark and the reference open-source implementation (ROS `ipa_room_segmentation`). It implements **four** methods — morphological, distance-transform, Voronoi-graph, and feature-based — on **20 office floor plans at 0.05 m/cell, each in an unfurnished *and* a furnished variant**, 100 m² to >1000 m². (Voronoi Random Fields is surveyed but never benchmarked.) [src: bormann-room-seg]

| | morphological | distance transform | **Voronoi** | feature-based |
|---|---|---|---|---|
| unfurnished — recall | **98.1 ± 2.4** | 96.9 ± 2.8 | 95.0 ± 2.3 | 89.2 ± 11.8 |
| unfurnished — precision | 88.5 ± 9.2 | 88.4 ± 9.3 | **94.8 ± 5.0** | 90.4 ± 8.0 |
| **furnished — recall** | 84.6 ± 7.2 | 76.1 ± 12.3 | **86.6 ± 5.2** | 85.1 ± 7.2 |
| **furnished — precision** | 90.5 ± 8.1 | 88.4 ± 8.5 | **94.5 ± 5.1** | 87.1 ± 14.5 |
| runtime (single core) | 1.6 ± 2.6 s | 1.8 ± 2.7 s | 13.0 ± 15.3 s | 269.3 ± 196.7 s |
| segments, unfurn. → furn. | 22.8 → 29.5 | 24.7 → **38.2** | 37.9 → 43.1 | 32.6 → 30.6 |

[src: bormann-room-seg]

**The clutter penalty is the headline**: furniture costs morphological 13.5 points of recall and distance-transform 20.8, and inflates their segment counts — which Bormann reads as "instability of these approaches under clutter." Named failure modes: morphological and distance-transform segments **grow into the corridor** and fuse room groups; **Voronoi over-segments corridors**; feature-based always merges two rooms that touch without a corridor between them. **On furnished maps Voronoi is the best all-round choice** — morphological wins on recall only when the map is clean.

Two families sit above this benchmark and are worth knowing:

- **Frequency-domain declutter first — ROSE²**, the current state of the art on cluttered/partial 2D occupancy maps. Pipeline: ROSE declutter → Hough walls snapped to dominant directions → representative lines → **faces** (convex cells cut by line intersections) → rooms by DBSCAN over faces, with edge weight `w(e) ∈ [0,1]` = the fraction of that edge actually covered by *observed* wall segments (edges below 0.1 coverage are discarded). On **10 cluttered real maps, mean IoU: ROSE² 73.3 ± 17.8, distance-transform 54.7 ± 14.7, morphological 51.2 ± 12.3, Voronoi 28.7 ± 10.6**; single-map extremes 95.1 vs 27.3/67.3/63.4. On the Bormann 20-map benchmark with **no parameter change**: 93.5 ± 5.5 precision / 91.0 ± 3.5 recall furnished [src: luperto-rose2].
- **Circumradius seeds + min-cut** (Turner & Zakhor): Delaunay circumradius local maxima as room seeds, min-cut on the triangulation dual with edge weight = shared-edge length, merge any pair sharing more than **2.44 m** (96 in — twice the ADA maximum door width), iterate to convergence [src: turner-zakhor-2014]. **Diffusion on a wall-induced partition** (Mura et al.) is the same idea with heat diffusion and automatic room-count discovery [src: mura-2014].

> *(synthesis — direct read-across)* We run Voronoi throat detection (EDA068 found a 0.66 m doorway) and hit the documented clutter weakness in EDA070 (living room → 1 real room + 3 spurious nooks). Bormann's numbers say Voronoi is nevertheless the **best** of the classical four under furniture, so the fix is not to abandon it but to change what we do with it: **(a)** apply the 2.44 m merge rule and a minimum-area rule *inside* the iteration rather than post-filtering; **(b)** seed from circumradius local maxima and let a min-cut choose the boundary, instead of cutting at every local narrowing — the cut then minimizes total boundary length rather than firing on each furniture gap; **(c)** declutter in the frequency domain before extracting walls at all, which is the single biggest measured jump in the literature (Voronoi 28.7 → ROSE² 73.3 IoU on cluttered maps) [src: luperto-rose2, bormann-room-seg, turner-zakhor-2014].

### 5.2 Clipping the map to *one* room

Turner's pipeline contains a directly reusable rule: after each round of room partitioning, **if no triangle of a room is intersected by the scanner path, that room was never entered** — its geometry is a superficial glimpse through a doorway, so it is **removed from the model entirely**, the seeds are recomputed, and labelling restarts [src: turner-zakhor-2014]. For "separate the kitchen from what is visible through the doorway" this is the whole answer: trajectory-driven, no semantics, one rule.

The complementary approach is to **decompose free space at constrictions** rather than flood-filling to walls — DuDe works on the free-space contour, separates at "natural constrictions such as doorways, narrow passages, and openings between adjacent areas," and is incremental so it tolerates partial maps [src: fermin-leon-dude]. **Its constriction threshold is the single most dangerous parameter**: an independent ablation reports F1 of **0.436 / 0.163 / 0.025** at d_thr = 1.5 / 3.0 / 6.0 m, with severe under-segmentation (rooms silently merged *through* doorways) in 0/3, 3/3, 3/3 scenes [src: cueto-occupancy-rooms].

That same study is a useful reality check on how well any of this works on real 3D-derived maps: occupancy-grounded room anchoring on 12 Matterport3D scenes scored recall 0.379, precision 0.518, F1 0.427, mIoU 0.364 (vs Hydra 0.152 / 0.703 / 0.241 / 0.323), with the authors' own caveat that "more than half of the ground-truth rooms remain unmatched on average" and that **"recall is bounded by decomposition granularity: recovering more rooms requires finer decomposition, not a different anchoring strategy"** [src: cueto-occupancy-rooms]. Reusable region-tracking rules from it: match to the prior region by IoU > 0.20, centroid shift < 1.5 m, area ratio ∈ [0.25, 4.0], retain unmatched regions for 3 updates, and **reject an entire decomposition if total free area or region count drops more than 15%**.

### 5.3 Doorway vs unmapped wall — what actually works, and what does not

**Start with the honest ceiling: 2D geometry alone cannot fully decide.** Two canonical results:

- Yamauchi's frontier formulation labels every cell **open** (P < prior), **unknown** (P = prior), or **occupied** (P > prior), with a **frontier** = the boundary between open and unknown, kept if larger than roughly the robot's diameter [src: yamauchi-frontier]. But his own Figure 1 says it plainly: **"Frontier 0 and frontier 1 correspond to open doorways, while frontier 2 is the unexplored hallway."** Three frontiers, identical geometric signature, different meanings.
- Anguelov et al., using laser range plus motion cues, **misclassified 2 of 7 doors as walls**; of these, one "never changed state, and hence is **indistinguishable from a wall under our model**." They recovered it only by learning width and colour from the doors that *did* move and transferring that appearance model — which then found 4 doors that never opened. Their robustness sweep is also a warning for us: doors found degraded 5 → 4 → 3 → 2 as pose noise went 0 → 2 cm/0.3° → 4 cm/0.6° → 6 cm/0.9° (with **0 false positives throughout**) — **door detection is very sensitive to trajectory error** [src: anguelov-doors].

**Lever 1 — keep the three-way visibility label (the biggest single win).** Adán & Huber label every cell of a candidate wall surface with **one of three** labels, not two:

- **occupied (F)** — a return landed here;
- **empty (E)** — a ray *passed through* here and terminated beyond;
- **occluded (O)** — no ray reached here at all.

Labelling is done **per scan by ray tracing** from that scan's origin, then integrated across all *K* scans with the rule that **a cell is occluded only if it is occluded from every viewpoint** [src: adan-huber-2011]. A real aperture is **empty**; an unmapped wall region is **occluded**. Binary occupancy grids destroy exactly this distinction by collapsing `empty` and `occluded` into "not occupied" — which is why a doorway and a never-scanned wall look identical in a standard grid.

On top of the three-way labelling they train an **SVM** on label-pattern and depth-edge features to detect rectangular openings. On a two-storey, 40-room building (225 scans, >3 billion points) where on average **35% of wall area was occluded, 15% fell within an opening, and 50% was unoccluded surface**, the detector found **93.3% of openings (70/75) at 10 cm voxels and 91.8% at 5 cm** at the best F-measure threshold; failures concentrated in severe occlusion and in closets whose doors were shut. The honest caveat, stated in the paper: opening-boundary accuracy was **5.39 cm mean absolute error (σ 5.70 cm, 2.56% relative)**, and only **36%** of boundaries fell within the 2.5 cm AEC tolerance. [src: adan-huber-2011]

So: **the three-way label reliably tells you *whether* there is an aperture; it does not give you a centimetre-accurate doorway width, and it cannot see a closed door at all.**

**Lever 2 — gate candidates on a door-width interval.** Warberg et al. split a wall segment `l₁` at its intersection with a non-parallel `l₂` when the closest endpoint of `l₂` lies within `[d_min, d_max]` of `l₁`, using **[0.8 m, 3.0 m]** as the doorway interval, with the split at least one minimum-segment-length from either endpoint; rooms then come from a **visibility graph** over line segments (edge only if unoccluded, max length 8 m) partitioned by spectral clustering at a Fiedler-value threshold of 0.18 [src: warberg-line-rooms]. *(The paper reports only computation time — no segmentation accuracy — and its environment is a simulated straight-walled building. Take the width interval, not the endorsement.)*

**Lever 3 — hypothesise the missing wall from the direction lattice, and split on free-space topology.** This is the closest published answer to our unsolved case. ROSE² handles the situation where **neither side of a dividing wall was ever observed**: walls cannot separate the two regions, so it falls back to the **Voronoi topological graph** — if the nodes assigned to a candidate room do not form a *connected* sub-graph, split it, preferring an existing representative line as the cut and otherwise cutting along a dominant direction that separates the components. The resulting room polygons then "**predict the presence of walls that complete the rooms even when they are not observed (yet) by the robot (e.g. due to occlusion)**" [src: luperto-rose2]. In other words: an unobserved boundary is *inferred* from the wall-direction lattice, while a genuine passage is identified by free-space *connectivity* — the two are distinguished by topology, not by whether points were seen.

**Lever 4 — go and look again.** Beeson et al. document our exact failure mode in print: "Occasionally, the robot may not observe specific pieces of the local surround… **Since Voronoi branches that touch unknown space are not pruned, this causes gateways to appear along these branches.**" Their remedy is not an algorithm — **the robot spins in place** to re-observe the surround, recomputes, and re-checks whether a real place exists [src: beeson-evg]. Combined with Anguelov's finding that a never-opened door is model-indistinguishable from a wall [src: anguelov-doors], the literature's consistent verdict since 1997 is that the residual ambiguity is resolved by **another observation**, not by more inference — which for us means a capture-protocol change, not an algorithm.

**Lever 5 — predicting the unobserved layout is worth doing.** Luperto et al. reconstruct the layout of partially-observed rooms and use it to estimate information gain at frontiers, giving a **10.1% exploration-time speedup** (3440 s → 3090 s over 10 runs × 10 buildings, 12.8% with early stopping, 19.1–30.5% on their showcase building), with layout estimates already usable at **20–60% coverage** [src: luperto-predict-layout]. For us this matters less as a speedup and more as evidence that room-completion from partial data is reliable enough to act on.

---

## 6. Known pitfalls

### 6.0 The sensor, from the datasheet — including two properties we had not accounted for

| Item | RPLIDAR C1 (model C1M1-R2) |
|---|---|
| Range | **0.05–12 m at 70% reflectance; 0.05–6 m at 10% reflectance** |
| Accuracy | **±30 mm** · Resolution 15 mm |
| Sample rate | 5 kHz · Scan frequency 8–12 Hz (10 typ.) |
| Angular resolution | **0.72°** |
| **Scan field flatness** | **0°–1.5°** |
| Laser | 905 nm, 20 W peak, 1.4 ns pulse, Class 1 · Ambient limit 40,000 lux |

[src: rplidar-c1-specs]

Two consequences we had not been accounting for:

- **★ The "scan plane" is a shallow cone, not a plane.** At 0–1.5° flatness the vertical spread is *(derived)* **2.6 cm at 1 m, 5.2 cm at 2 m, 7.9 cm at 3 m, 10.5 cm at 4 m, 15.7 cm at 6 m**. At counter distance the slice is ~8–10 cm thick. That is a genuine and previously-unmodelled contributor to apparent wall-band thickness, and it is *range-dependent* — exactly the signature of a low-frequency bow.
- **The coordinate frame is left-handed, angle increasing clockwise, x-axis dead ahead** [src: slamtec-sdk]. Given this project's history with the `(θ,x,y)` scramble (memory `verify-each-step-debugging`), this deserves an explicit round-trip test rather than an assumption.

Accuracy is warranted only for 10–90% reflectance; the datasheet notes that outside that band *"the accuracy of point cloud data might decrease slightly"* [src: rplidar-c1-specs]. The physical reason is amplitude-dependent timing bias ("walk error") in pulsed-ToF leading-edge discrimination, which produces a **systematic range offset at a dark/bright material boundary** rather than extra noise.

### 6.1 ★ Our intensity channel is a hard-coded constant — proven in vendor source

The project memory recorded the RPLIDAR `quality` channel as binary 0/47 in the kitchen sweep. That is not a quirk of one capture. In the SLAMTEC SDK's dense-capsule handler:

```c
hqNode.quality = dist_q2 ? (0x2F << RPLIDAR_RESP_MEASUREMENT_QUALITY_SHIFT) : 0;   // SHIFT = 2
```

and the ROS driver publishes `scan_msg->intensities[i] = (float)(nodes[i].quality >> 2)`, so `(0x2F << 2) >> 2 = 0x2F = **47**` for every valid return and **0** for every invalid one. The dense wire format itself carries no quality byte at all — `_sl_lidar_response_dense_cabin_nodes_t` is a bare `sl_u16 distance`. [src: slamtec-sdk] The datasheet's introduction claims the C1 provides *"reflectivity data,"* but its own Data Output table lists exactly four fields: distance, angle, start signal, checksum — **no intensity field** [src: rplidar-c1-specs].

**This is a hard-coded literal, and it will never be anything else on this hardware.** The consequence is architectural: every intensity-based glass detector is structurally unavailable to us, and so is the multi-echo family (one distance per sample, no second echo).

### 6.2 Glass, mirrors, specular surfaces

**The physics gives three outcomes selected by incidence angle:** a point on the object plane, a point *behind* it, or a point on a *reflected* object [src: koch-specular].

**Glass is nearly invisible; mirrors localize well.** Koch et al. measured a real glass door of two panes each **88 × 198 cm** detected only over a patch of **31.1 × 23.9 cm** — the region hit near perpendicular *(derived: ~4% of the glass area; at 2–3 m standoff the visible half-width subtends only 3.0–4.4°)*. The same paper recovered a 60 × 40 cm **mirror** as 60.5 × 41.9 cm — essentially its true extent [src: koch-specular]. Independent corroboration of the angular window: the specular spike is ~1.25–2.5° wide on a 0.25° scanner [src: weerakoon-cartographer-glass]. And directly on our sensor family: *"the RPLidar sensor **cannot detect the transparent object at all tested distances**"* (5 mm glass) [src: mirdanies-sensors].

**How badly a standard occupancy grid handles this — the best measured result.** Foster et al. logged 4.5 M rays from two 2D LiDARs on an autonomous wheelchair across a campus with flat, curved and stained glass, and found *"approximately half of the rays in the dataset go through or reflect off a shiny surface"* [src: foster-rfm]:

| Method | Recall diffuse | **Recall glass** | Motion removed | **Reflection removed** |
|---|---|---|---|---|
| **Standard occupancy grid** | 98.3% | **51.6%** | 100% | **75.4%** |
| Basic RFM | 99.8% | 99.8% | 91.8% | 9.0% |
| RFM + motion + reflection removal | 98.5% | **98.7%** | 99.7% | **98.2%** |

A plain occupancy grid discards **half the glass returns** and admits **a quarter of the phantom reflected geometry**. Their mechanism statement is the one to internalize: *"lidar light bouncing off of glass only returns to the sensor from a small number of directions, [so] observations detecting the glass are vastly outnumbered by those missing it."*

> **★ The Reflectance Field Map is the right method for our rig, specifically because of §6.1.** It is *"sensor-agnostic and has no reliance on either intensity or multi-return measurements"* — it works from ray geometry and viewing direction alone. It is 2D-native, open source, and runs a full update in **10.3 ms** at 5 cm / 2° resolution. [src: foster-rfm] The intensity-based alternatives are all closed to us: glass confidence maps report >95% of glass correctly mapped with <5% classification error but take **intensity, distance and incident angle** as network inputs [src: jiang-glass-confidence]; `Cartographer_glass` needs an intensity threshold that its own authors had to re-tune per building (`thresh` 1300 / 3000 / 8000 across three settings) [src: weerakoon-cartographer-glass].

**Mirrors in the 2D map** produce three distinct artefacts: near-normal full reflection (a solid false surface), dropout at long virtual travel distance, and geometry mapped *behind* the mirror plane — plus **robot self-detection on the mirror surface**. The classical detector needs the mirror to be *framed*: *"the proposed method can miss a mirror without any frame. In this case, the mirror is invisible to laser scanners."* [src: yang-wang-mirrors]

### 6.3 Dynamic objects — and why filtering is the wrong response

**How long a transient survives, derived from Cartographer's own defaults** (`hit_probability = 0.55`, `miss_probability = 0.49`): log-odds +0.2007 per hit, −0.0400 per miss ⇒ **5.0 misses to cancel one hit** [src: cartographer-icra2016].

| Person behaviour | Hits deposited | Clear passes to return to p = 0.5 | Time at 10 Hz |
|---|---|---|---|
| Walks through (1–2 hits/cell) | 2 | 11 | 1.1 s |
| Pauses 1 s | 10 | 51 | 5.1 s |
| **Pauses 3 s** | 30 | **151** | **15.1 s** |

*(derived)* — **a walking person largely self-erases if the robot keeps observing the area; a person who pauses for a few seconds is effectively permanent in a single-pass map.** Worse, ROS `slam_gmapping` uses a pure counting model with **no decay and no clamping** (`occ = hits/visits`, occupied above 0.25), so a cell hit *n* times needs **3n additional clean pass-throughs** to clear. Meyer-Delius et al. state the general rule: *"the number of observations needed by the occupancy grid to correctly represent the new static cells is approximately the same as the number of previous observations."* [src: meyer-delius-changing]

**Free-space carving is destructive to the map you are trying to build.** On SemanticKITTI, an aggressive occupancy filter (OctoMap at 0.2) rejects ~99.9% of dynamic points but preserves only **20.8–38.2% of the static map** [src: lim-erasor]. And the methods do not transfer indoors: on a semi-indoor set (single VLP-16, two people moving around the sensor), static-kept/dynamic-removed/harmonic-mean scores were Removert **99.96 / 12.15 / 34.85**, ERASOR 94.90 / 66.26 / 79.30, plain OctoMap 88.97 / 82.18 / 85.51, and DUFOMap **99.64 / 83.00 / 90.94** [src: zhang-dynremoval-benchmark, duberg-dufomap]. ERASOR's ground-contact assumption collapses entirely on a low indoor sensor (82% false positives in a 750 m² / ~100-person indoor study) [src: habibiroudkenar-dynahull]. Both benchmarks name the *standing* person as the failure: *"people are standing in the same place for an extended period, making it challenging to remove them using the default parameters."*

> **★ The second-order damage is the real one, and no point filter can undo it.** DynaHull's indoor study found that *"the points were not accurately registered due to the presence of a noticeable number of outliers (humans and other dynamic objects). This has caused **walls or other stationary features to appear as artificially thickened** due to cumulative mapping errors."* [src: habibiroudkenar-dynahull] **People corrupt the poses, not just the points** — the same failure class as our wall-band and trajectory-bow. The classical result is the same: with visitors present, *"more than half of all measurements were corrupted for extended durations of time,"* and position-tracking failure went from 1.6% to **26.8%** [src: fox-markov-dynamic]. **Practical rule: if people walked through a capture, re-run the capture rather than filter it.**

*(One caution on the obvious fix: Fox et al. also measured that filtering readings which disagree with your belief makes *recovery* from a genuine localization failure an order of magnitude slower — 1779 s vs 237 s. Gating scans by agreement with a prior map has this cost.)*

**No published 2D person detector applies to our mount.** Every 2D person-detection dataset and detector is trained at ankle or lower-leg height, where a person is two small convex blobs with a characteristic gap; the best reported figures are AP 47.6% against all annotated people and 77.2% against those actually visible in the scan plane [src: jia-2d-vs-3d-person]. At **1.1 m the C1 cuts the torso** — one wide arc, geometrically indistinguishable from a chair back or a counter edge. *(This is a real gap in the literature, not an oversight in our search.)*

### 6.4 Motion distortion — yaw rate, not speed, and it scales with range

Deschênes et al. give the formula: for a sweeping sensor of period τ, the residual injected by treating a scan as instantaneous is **`r_v ≈ σ_v·τ/2`** (translation) and **`r_ω ≈ σ_ω·τ·d/2`** (rotation), where `d` is the **mean range** — *"approximately the displacement of the lidar in the middle of its scan."* [src: deschenes-deskew]

At **10 Hz (τ = 0.1 s)**, mid-scan residual `r_ω` versus the full-revolution smear `ω·τ·d` (the two bracket the effect within a factor of 2):

| Yaw rate | Δθ per sweep | mid-scan @3 m | full smear @4 m |
|---|---|---|---|
| 10 °/s | 1.0° | 2.6 cm | 7 cm |
| 30 °/s | 3.0° | **7.9 cm** | **21 cm** |
| 60 °/s | 6.0° | **15.7 cm** | **42 cm** |

Translation, by contrast, contributes only **1.0 cm at 0.2 m/s** and 3.0 cm at 0.3 m/s. *(derived)* **Rotation dominates translation whenever ω > v/r** — at 0.2 m/s and 4 m range that crossover is only **2.9 °/s**. Any turn faster than a few degrees per second makes rotation the dominant skew term at indoor ranges.

> **★ A concrete, testable root-cause hypothesis for an open project bug.** The EDA200 finding (memory `eda110-refinement-injected-turn-offsets`) is that a contiguous turn segment at **yaw 28–67 °/s** carries an injected **+11–17 cm** lateral offset, currently attributed to the wall-prior refinement. The mid-scan formula predicts **7–17 cm at 3 m** over exactly that yaw range, and the full-smear bound predicts more. Un-deskewed intra-scan rotation is a live alternative (or additional) cause, it is cheap to test, and the residual it predicts is range-dependent and bow-shaped — which is what EDA172 characterized.

**We already have what deskewing needs.** The Slamtec ROS driver sets `time_increment = scan_time/(N−1)` and stamps the message at the **start** of the sweep, so per-point timestamps exist [src: slamtec-sdk] — but if the header stamp is used for every point, the **full** `ω·τ·d` applies rather than half of it. KISS-ICP's ablation shows a plain **constant-velocity** prior is enough (KITTI translational error 0.91 → 0.49 without/with deskew, and the constant-velocity prior **matched or beat an IMU**), with the authors concluding *"more sophisticated techniques are unnecessary for most robotic odometry estimation"* [src: vizzo-kiss-icp]. *(Scaling caveat: KITTI is a car at up to 25 m/s — 50–100× our per-sweep translation. Take the ordering and the method, not the 2× magnitude.)*

**Why a rigid per-scan pose cannot absorb it:** *"ICP will thus find a transformation that distributes this alignment error throughout the whole reading… if a skewed reading is merged into the map, the newly added points will blur the overall structure."* [src: deschenes-deskew]

### 6.5 ★ The scan-plane height problem — the counter is *false free space*, not a missed obstacle

The standard framing ("obstacles above or below the plane are missed") **understates our case**. Our plane sits at ~1.1 m, about **20 cm above a 0.9 m counter**. The ray passes over the worktop and terminates on the wall behind, so every intervening cell is ray-traced to **free with high confidence**. The map does not merely omit the counter — it **positively certifies the counter's footprint as drivable floor**.

*(derived)* At 0.60 m counter depth: **3 m of counter run = 1.8 m² of phantom free floor; 5 m = 3.0 m²; 8 m = 4.8 m².** *(I found no paper stating this specifically for a horizontal counter — it is worth writing up as an original observation.)* The right fix is not a better 2D map but the **free / occupied / unknown trichotomy** of §5.3: a cell behind a counter has no evidence either way and should be **unknown**.

**But the failure is not one-directional, and the project has measured the opposite case.** The kitchen's true back wall at v = 1.78 m is **occluded by against-wall cabinets** and carries only **~2,075 returns** seen through gaps, while **~40,887 returns at v = 1.119 m are the cabinet/appliance FRONTS**. A naive consensus fit latched onto the dense object fronts and produced the wrong wall line (`docs/locked-map.md`, EDA124/EDA122). **At a single scan height, return density is not evidence of wall-ness** — the densest planar band in a kitchen is usually the furniture.

**No single height works.** Liao et al. simulated horizontal 2D scanners on real indoor scans and found *"the laser scanner set at 20 cm fails to detect the upper stove and the seat of the chairs… while the laser scanner set at 80 cm misses the lower garbage bins as well as the seats"* — two heights, two disjoint sets of misses [src: liao-parse-geometry]. Lundell et al. state the canonical consequence: a robot on raw 2D laser *"would see the legs of the table but not the tabletop itself, allowing it to plan and execute a trajectory through the table causing a collision"* [src: lundell-hallucinating].

**Measured magnitude.** In a 10 × 10 m indoor facility with 20 physically-placed obstacles at surveyed coordinates, LiDAR-only obstacle **recall was 60.0%, rising to 95.0% when fused with an RGB-D camera** (F1 0.72 → 0.92), with the named misses being glass partitions, wire mesh, and *"low obstacles: pallets below the laser scan plane"* [src: delhibabu-2dgrid]. *(N = 20, one warehouse-like environment, and the 40% miss mixes material failures with height failures — do not read 60% as a pure scan-plane number.)* Separately, ROSE²'s benchmark quantifies how far a cluttered 2D map's apparent walls are from the building's true structure: naive extraction scores IoU **28.7–54.7** against ground-truth structure [src: luperto-rose2].

**Three mitigations, in order of cost:**

1. **Project the *ceiling*, not the mid-height slice.** Previtali et al.'s empirical finding is that *"the acquisition of the ceiling surface, due to its location, is generally less influenced by clutter and occlusion than other surfaces in the room"* [src: previtali-cluttered-rooms]. This inverts our problem into a lever: **1.1 m is the worst possible zone** — above the counters (room reads too large) and below the ceiling (upper cabinets and tall appliances make it locally too small). A ceiling plane recovered from the stereo camera would give the architectural boundary far more cleanly.
2. **Score wall candidates by viewpoint diversity, not return density.** A wall is visible from many widely-separated poses; a cabinet front from a narrow arc. This is [[robust-evidence-mapping-principle]] applied to line selection, and it is the direct fix for the v = 1.119 / v = 1.78 failure.
3. **Multi-height passes.** The 2-DOF tilt/lift mast already on the project's build list ([[sensor-mount-2dof-tilt-lift]]) is the real fix; two heights (e.g. 0.4 m and 1.4 m) separate "wall" (present at both) from "furniture front" (present at one). **The "we can't afford 3D" objection is dead at kitchen scale** — OctoMap stores a 43.7 × 18.2 × 3.3 m corridor at 5 cm in **41.6 MB pruned, 24.7 MB max-likelihood, 0.67 MB on disk** [src: hornung-octomap]. That paper also warns against the 2.5D shortcut for our exact use case: *"While this is sufficient for path planning and navigation with a fixed robot shape, the map does not represent the actual environment, **e.g. for localization**."* Our map is a navigation *anchor* map, i.e. used for localization. The 26-mile Office Marathon reached the same conclusion in practice, requiring *"an efficient Voxel-based 3D mapping algorithm that explicitly models unknown space"* [src: marder-eppstein-marathon].

*(One discretization trap to avoid, documented in OctoMap: when a scanner sweeps a flat surface at a shallow angle, a cell measured occupied in one scan is updated free in the next after the sensor rotates. The fix is to update each volume at most once per scan — exactly what a 2D LiDAR grazing a counter edge from a moving rover will do.)* [src: hornung-octomap]

### 6.6 The sensor is not the accuracy limit — the systematic term is

Two facts about the noise floor:

**dToF sigma is roughly flat with distance; triangulation sigma is not.** Measured side by side: RPLidar A1 (triangulation) **±12 mm at 2.4 m → ±40 mm at 6 m**, versus a Hokuyo ToF unit **±13 mm → ±15 mm → ±15 mm at 2.4 / 6 / 12 m** [src: jafri-scanner-calib]. A separate study found the A1's error **95% correlated with distance** (a ~9.3% distance-proportional scale bias) while a ToF unit's error showed no strong distance correlation [src: mirdanies-sensors]. **The C1 is dToF, so do not carry A-series noise models across.** Both studies also found *specularity, not colour*, to be the dominant surface variable — shiny vinyl produced the largest variation while red/blue/white/green were indistinguishable [src: jafri-scanner-calib].

**And the arithmetic says the sensor has enormous headroom.** *(derived — total-least-squares line fit, per-point σ = 30 mm, 0.72° step)*:

| Standoff | Wall | N per scan | σ_offset | σ_angle |
|---|---|---|---|---|
| 2 m | 3 m | 102 | **3.0 mm** | 0.20° |
| 3 m | 3 m | 74 | **3.5 mm** | 0.23° |
| 4 m | 3 m | 57 | **4.0 mm** | 0.26° |
| 4 m | 1 m | 20 | 6.7 mm | 1.34° |

> **Read this table honestly: these are noise *floors*, not predictions.** They assume independent zero-mean error. EDA172 established that the residual within a scan is a **coherent low-frequency bow**, which does not average down as 1/√N. Averaging ten scans would nominally reach ~1.2 mm; our observed ~2 cm band is more than an order of magnitude above that. **The gap between 3 mm of theory and 2 cm of reality is entirely systematic, and no amount of N will close it.** The value of the table is to prove the sensor is not the limitation — the candidates are scan-cone thickness (§6.0), un-deskewed rotation (§6.4), the wrong-surface problem (§6.5), and pose-only optimization (§2.4).

**What a cheap 2D LiDAR floor plan actually achieves, as a bar:** Cartographer on a sub-$30 Neato Revo LDS, tape-measured against five spans, gave absolute errors of **1–11 cm with a consistent +0.7% stretch on the long spans** [src: cartographer-icra2016]. That is a *bias*, not noise, and no repeatability check would catch it — which is why §1 recommends grading against tape-measured spans rather than band thickness.

---

## 7. Recommended pipeline for our case

*(synthesis — 2D LiDAR only, one room, no wheel odometry, accuracy over speed)*

```
per-scan  →  DESKEW: interpolate pose across the 100 ms revolution      [§6.4]
          →  ordered split-and-merge line extraction (per scan)         [§3.1]
          →  CSM coarse alignment  →  PLICP fine  (never PLICP alone)   [§1]
          ↓
graph     →  ALL-PAIRS scan matching over overlapping pairs (~2-4 min offline)
          →  continuous robust weights: GNC-TLS (gtsam::GncOptimizer)
             or a line process pruned at l_ij < 0.25                    [§2.3, §2.4]
          →  ambiguity alarms: PCM composed-loop chi2_3 (95% = 7.815)
             + Olson lambda1/lambda2 >= 2                               [§2.3]
          →  NOT DCS / max-mixtures / RRR — all assume odometry         [§2.3]
          ↓
refine    →  JOINT pose + map: BALM-style line factors with the line
             parameters eliminated in closed form; accept only if the
             HELD-OUT wall band improves                                [§2.4, locked-map step-f]
          ↓
label     →  per-scan ray tracing; keep the THREE-WAY label
             occupied / empty / occluded, integrated over all poses     [§5.3]
          ↓
polygon   →  Delaunay triangulation of wall samples
          →  line-of-sight carving (pose→sample, truncated at occluders;
             plus pose→pose along the trajectory)
          →  interior/exterior boundary = CLOSED polygon, by construction [§3.3]
          ↓
rooms     →  frequency-domain declutter (ROSE) BEFORE wall extraction
          →  circumradius-local-maximum seeds → min-cut on the dual
          →  merge across borders > 2.44 m; DROP any room the trajectory
             never entered                                              [§5.1, §5.2]
          ↓
simplify  →  boundary-restricted QEM, stop at error = r; freeze shared vertices
          →  ROSE W-ratio test (W < 0.2 trust / W > 0.4 reject) → SOFT
             length-weighted angle prior, accepted on held-out band     [§4]
          ↓
export    →  wall polygon + apertures labelled from EMPTY runs;
             UNSCANNED runs exported as "unknown", never as wall
          →  VALIDATE against tape-measured spans, not band thickness   [§1]
```

Ordered by expected value per unit of effort:

1. **Keep the three-way visibility label** (§5.3). Nearly free — we already ray-cast for free-space carving — and it is the only thing that separates a doorway from an unmapped wall. Do this first; it also feeds steps 2 and 5.
2. **Replace corner-assembly with Delaunay + line-of-sight carving** (§3.3). The E13 fix. A few hundred lines, no training, runs on the sweep we already have, directly A/B-able against the current assembler.
3. **Measure the deskew error, then deskew** (§6.4). The formula predicts **7–17 cm at 28–67 °/s** — which brackets the unexplained EDA200 turn-segment offsets. This is a cheap test of a live bug, not just an accuracy tweak.
4. **Drop un-entered rooms by trajectory intersection** (§5.2). One rule; solves "what's visible through the doorway" with no semantics.
5. **Try a joint pose+map (BALM-style) refinement before accepting the locked map as final** (§2.4). BALM2 took an inspected plane from **σ 6.8 cm → 1.7 cm**, and Occupancy-SLAM showed that seeding a joint solve *from already-converged poses* still improves substantially. Our 2.5 cm band against a 0.13 cm local crispness is exactly the signature this addresses.
6. **Score wall candidates by viewpoint diversity, not return density** (§6.3). Fixes the v = 1.119 vs v = 1.78 wrong-wall failure.
7. **Frequency-domain declutter (ROSE) before wall extraction** (§5.1). The single biggest measured jump in the room-segmentation literature — Voronoi 28.7 → ROSE² 73.3 IoU on cluttered maps.
8. **Soft, length-weighted angle prior gated on the ROSE W-ratio and the held-out band** (§4), never a hard Manhattan snap.
9. **Re-grade everything against tape-measured spans** (§1). A band-thickness metric is blind to global warp and can rank the worse map higher.
10. **Capture hygiene beats filtering** (§6.3). A person who pauses 3 s needs ~15 s of continuous line-of-sight to erase, and dynamic objects corrupt the *poses* — which no post-hoc point filter can undo. If people walked through a capture, re-run it.
11. **If glass or mirrors are in scope, use the Reflectance Field Map** (§6.2) — it is the one method that needs neither intensity nor multi-echo, which §6.1 proves we will never have.
12. **Consider recovering the room boundary from the *ceiling* instead** (§6.5). Ceiling surfaces are far less occluded than any mid-height slice, and 1.1 m is provably the worst zone. This is a stereo-camera job, not a LiDAR one.

**What this does *not* change:** point-to-line is the right metric, and our robust wall-prior refinement is the right *shape* of gate. The changes are (a) what feeds PLICP, (b) what the graph optimizes, and (c) everything downstream of line extraction.

---

## 8. Where our current approach diverges from the literature

*(synthesis — the honest list)*

| Our approach | Literature position | Verdict |
|---|---|---|
| Point-to-line ICP as the metric | Censi's PLICP is the accuracy-optimal 2D metric [src: censi-plicp] | ✅ Correct |
| **PLICP run without a coarse pre-aligner** (no odometry ⇒ uninformed first guess) | PLICP is *less* robust than plain ICP at ±45° (24.8% gross failures); 66%/50% success at zero-init on Intel/MIT; **failed to map a 4.5 × 7 m cluttered office**. Every source that makes it work pairs it with GPM / ICN / correlative matching [src: censi-plicp, li-feature-scanmatch, lv-thesis] | ⚠️ **We are running it in its documented worst case** |
| Trusting scan-match self-reported covariance | Censi: no ICP covariance estimator is reliably conservative; NDT bounds contain the truth only **40%** of the time. Only CSM's volume-fit covariance is principled [src: censi-icpcov, mclean-icet, olson-csm] | ⚠️ Don't gate on it |
| Pose graph + ICP2D backbone | Standard, and it solves the *drift* problem [src: cartographer-icra2016] | ✅ Correct as far as it goes |
| **Pose-only optimization treated as the accuracy ceiling** ("locked map") | Pairwise-then-pose-graph *"only considers the overlap among two scans at a time, while the overlap is really shared by all scans"* and *"the mapping consistency indicated by the raw points is completely ignored"*; BALM2 took a plane from **σ 6.8 → 1.7 cm**; Occupancy-SLAM improves substantially even when **seeded from converged poses** [src: liu-balm2, occupancy-slam] | ❌ **The ceiling is architectural, not sensory — worth one joint-solve experiment before the lock stands** |
| Grading refinement on wall-band thickness | MME *"does not reflect any global geometric property"*; a documented case where the **worse** map scores better; Cartographer local 0.108 m vs global 5.22 m on the same run [src: hu-mapeval, razlaw-registration-eval, cartographer-icra2016] | ❌ **Pair it with tape-measured spans** — independently corroborates our own "false rescues" memory |
| Robust consensus line fitting on the **accumulated** cloud | RANSAC/Hough underperform on 2D range data because they **discard scan ordering**; ordered split-and-merge is faster *and* more correct [src: nguyen-line-comparison] | ⚠️ Weaker class than necessary — extract per-scan, merge after |
| Wall-prior refinement gated on held-out band | Matches accept-only-if-improves practice | ✅ Right shape |
| Polygon by **assembling observed corners** | No modern method does this; closure comes from a space partition or a graph cycle [src: turner-zakhor-2014, fang-lafarge-2021, floor-sp] | ❌ **Wrong formulation — this is E13** |
| "Closure is sensor-bound" | True for corner assembly only; ray-carving needs no observed corner [src: turner-zakhor-2014] | ❌ **Does not survive a change of formulation** |
| Voronoi throat cutting for room segmentation | Voronoi is nonetheless the *best* classical method under furniture (86.6/94.5 recall/precision furnished); the fix is seeds+min-cut and frequency-domain declutter first (28.7 → 73.3 IoU) [src: bormann-room-seg, luperto-rose2, turner-zakhor-2014] | ⚠️ Swap the formulation, keep the goal |
| Binary occupancy for free space | Collapses `empty` and `occluded`, destroying the doorway/unmapped distinction [src: adan-huber-2011] | ❌ **Keep three labels** |
| Dense return count as wall evidence | Viewpoint diversity / agreement is the reliability signal ([[robust-evidence-mapping-principle]]) | ⚠️ Caused the wrong-wall pick; fixable |
| No deskewing at 10 Hz | `r_ω ≈ ω·τ·d/2` predicts **7.9 cm at 30 °/s** and **15.7 cm at 60 °/s** at 3 m range; a rigid pose cannot absorb it, and the driver already provides per-point timestamps [src: deschenes-deskew, slamtec-sdk] | ❌ **Live candidate cause of the EDA200 turn offsets** |
| Modelling the scan as a **plane** | Datasheet scan-field flatness is **0°–1.5°** — a cone, spreading 7.9 cm vertically at 3 m and 10.5 cm at 4 m [src: rplidar-c1-specs] | ⚠️ **Unmodelled, range-dependent contributor to the wall band** |
| Treating the 2D map's free space as drivable | The ray passes *over* a 0.9 m counter and certifies its footprint as free — 1.8–4.8 m² of phantom floor per kitchen; the fix is free/occupied/**unknown**, not a better 2D map [src: hornung-octomap, delhibabu-2dgrid] | ❌ **Actively wrong, not merely incomplete** |
| Ruling out 3D on cost grounds | OctoMap stores a 43.7 × 18.2 × 3.3 m corridor at 5 cm in **41.6 MB pruned / 0.67 MB on disk**; and its authors warn 2.5D *"does not represent the actual environment, e.g. for localization"* — which is exactly our anchor-map use [src: hornung-octomap] | ⚠️ **The memory objection is dead at kitchen scale** |
| Expecting reflectivity from the `quality` channel | It is `0x2F << 2` in the vendor SDK — a hard-coded 47 [src: slamtec-sdk] | ✅ Memory was right; **now source-proven, and it closes off four of five glass-detection families** |

**Robust back-ends we should *not* adopt, despite their reputations** — all three assume an odometry backbone we lack, and all fail silently: **DCS** (scored TPR = 0.0, disabling every constraint, without a good initialization), **max-mixtures** (rejected 26/26 and 901/901 *correct* closures on clean data with a poor initial guess), **RRR** (its χ² statistic measures odometry deformation). Use **GNC-TLS** (starts convex, needs no inlier guess) plus the initialization-free **PCM** and **λ₁/λ₂** ambiguity checks instead. [src: mangelson-pcm, sunderhauf-comparison, latif-rrr, yang-gnc, olson-scgp]

---

## 9. Reading list

1. **Turner & Zakhor, GRAPP 2014** — *Floor Plan Generation and Room Labeling of Indoor Environments from Laser Range Data*. The single most actionable paper for us: 2D wall samples + scanner poses → Delaunay → line-of-sight carving → watertight boundary → min-cut rooms → QEM simplification, in under 10 s. **This is the E13 fix.** Read §3–§5. [src: turner-zakhor-2014]
2. **Choi, Zhou & Koltun, CVPR 2015** — *Robust Reconstruction of Indoor Scenes*. The closest published analogue to our situation (one indoor scene, all-pairs registration, no reliable odometry) and the strongest evidence that verifying pairs harder is a dead end: pairwise precision under 20% across six algorithms, lifted to **97.7% by a joint line-process solve** at a cost of 1.4 points of recall. Read §3 and Table 2. [src: choi-robust-indoor]
3. **Adán & Huber, 3DIMPVT 2011** — *3D Reconstruction of Interior Wall Surfaces under Occlusion and Clutter*. The occupied/empty/occluded three-way labelling, what it buys (93.3% opening detection) and what it costs (5.39 cm boundary error; only 36% within 2.5 cm). Read §III-B and §IV. [src: adan-huber-2011]

Optional, in priority order: **Liu, Liu & Zhang, T-RO 2023** (BALM2) for what a joint pose+map solve does to map quality — plane σ 6.8 → 1.7 cm, *"as if the sensor had no motion"* — if the locked-map decision is ever revisited [src: liu-balm2]; **Deschênes et al., CRV 2021** for the two-line deskew formula and the EDA200 hypothesis [src: deschenes-deskew]; **Nguyen et al., Autonomous Robots 2007** for why ordered split-and-merge beats RANSAC/Hough on scan data [src: nguyen-line-comparison]; **Kucner et al., ICRA 2021** (ROSE) for the W-ratio "is this map structured enough to snap?" test with published thresholds [src: kucner-rose].

---

## 10. Open gaps — in this page and in the literature

*(honest scope note)*

**Unverified in our sources:** Biber & Straßer's original NDT numbers (paywalled); HectorSLAM's accuracy claims (no open-access copy located); Bosse & Zlot's 2D place-recognition precision/recall (paywalled — the only available characterization is a competitor's); Hähnel et al.'s dynamic-mapping numbers (paywalled); Lu & Milios's full text (the description here is confirmed via the graph-SLAM tutorial, not the original). Whether a genuinely 2D Scan Context variant exists is an *absence of evidence*, not an exhaustive search.

**Genuine gaps in the published literature** — each is a cheap original measurement we could make on our own data:

1. **No paper compares a 2D-LiDAR floor plan against a 3D-derived ground truth as a function of slice height.** The nearest proxies are 60% obstacle recall [src: delhibabu-2dgrid] and 28.7–54.7 IoU for naive structure extraction on cluttered 2D maps [src: luperto-rose2].
2. **No paper quantifies the "counter certifies false free space" effect** for a horizontal work surface. Our derivation (§6.5) appears to be original.
3. **No paper measures 2D-laser return density or detection rate on table and chair legs.**
4. **No paper measures cells-corrupted-per-person-pass in a 2D grid**, nor the false-wall failure mode specifically; DynaHull is the only work measuring a *consequence* (wall thickening via registration drift).
5. **No 2D person-detection dataset or detector exists for a torso-height (~1.1 m) scan plane** — all published work sits at ankle or lower-leg height [src: jia-2d-vs-3d-person].
6. **Lundell et al. hold a per-ray 2D-vs-fused discrepancy record and never publish its magnitude** [src: lundell-hallucinating] — the single cheapest novel number available to us.
