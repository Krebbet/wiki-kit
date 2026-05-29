# Learned Point Cloud Registration

Deep learning methods for point cloud registration (aligning one 3D scan to another) have made significant benchmark progress since 2019, but none have displaced classical ICP-family methods in deployed LiDAR-inertial SLAM systems. This page explains what the methods do, what the benchmarks show, why the lab-to-field gap persists, and what recent work is doing to close it.

## Source

| File | Paper | Year |
|---|---|---|
| `02-01-arxiv-2404-13830.md` | "Deep Learning-Based Point Cloud Registration: A Comprehensive Survey and Taxonomy" (Zhang et al.) | Apr 2024 / Feb 2025 |
| `01-02-arxiv-2409-10824.md` | "Evaluating and Improving Robustness of LiDAR Odometry Under Real-World Corruptions" (Yang et al.) | Sep 2024 |
| `07-03-arxiv-2603-16273.md` | "GenZ-LIO: Generalizable LiDAR-Inertial Odometry Beyond Indoor–Outdoor Boundaries" | Mar 2026 |
| `06-04-arxiv-1905-03304.md` | "Deep Closest Point: Learning Representations for Point Cloud Registration" (Wang & Solomon, ICCV 2019) | 2019 |
| `05-05-arxiv-2507-17531.md` | "When and Where Localization Fails: An Analysis of ICP in Evolving Environments" (Dannaoui et al.) | Jul 2025 |

## Related

- [[slam]] — SLAM hub; VIO/LIO front-ends; two-phase map-then-localize architecture
- [[learned-slam]] — neural LIO (DFLIOM/KN-LIO), learned VIO, GS-LIVO; the broader AI-SLAM landscape
- [[fast-lio-mid360-orin]] — FAST-LIO2 deployment (uses classical ICP/GICP-based registration)
- [[lidar-for-uav-autonomy]] — LiDAR classes and LIO algorithm lineage
- [[indoor-cluttered-slam]] — indoor SLAM failure modes where registration breaks down

---

## 1. What Point Cloud Registration Is

Point cloud registration is the sub-problem of finding a rigid transformation (rotation R ∈ SO(3), translation t ∈ ℝ³) that aligns a *source* scan to a *target* scan or map. Every frame-to-frame step in [[slam]]-based LiDAR odometry is a registration problem: align frame t to frame t−1, accumulate the transforms, and you have a trajectory.

In LiDAR-inertial odometry (LIO), the same operation is performed as scan-to-map matching: the incoming downsampled scan is registered against a local voxel map, with IMU pre-integration providing a motion prior. This is the inner loop of FAST-LIO2, KISS-ICP, and every other classical LIO system discussed in [[fast-lio-mid360-orin]] and [[lidar-for-uav-autonomy]]. [src: 07-03-arxiv-2603-16273.md]

Registration quality determines pose drift. Failure modes — local minima, poor initialization, degenerate geometry, corrupted scans — compound over time into unbounded trajectory error.

---

## 2. Classical Baseline: ICP/GICP/NDT

**Iterative Closest Point (ICP)** alternates between finding nearest-neighbor correspondences and solving the least-squares alignment (via SVD), repeating until convergence. The chicken-and-egg problem — good correspondences require good alignment and vice versa — makes ICP extremely prone to local optima when initial misalignment is large. [src: 06-04-arxiv-1905-03304.md]

Classical variants address specific weaknesses:
- **Point-to-Plane ICP** uses surface normals to constrain alignment; empirically more stable in semi-structured outdoor environments than point-to-point ICP, particularly where symmetric corridors or sparse features create ambiguous correspondences. [src: 05-05-arxiv-2507-17531.md]
- **GICP / G-ICP** treats correspondences as plane-to-plane, operating as a generalized least-squares estimator; used in DLIO and iG-LIO. [src: 07-03-arxiv-2603-16273.md]
- **KISS-ICP** (2023) demonstrates that well-engineered point-to-point ICP with adaptive thresholding, robust kernels, and motion compensation outperforms many learned alternatives in practice, earning a "2nd best KITTI odometry" result. [src: 01-02-arxiv-2409-10824.md]
- **NDT** (Normal Distribution Transform) partitions space into grid cells and models each as a Gaussian; avoids explicit correspondences.

Why classical methods still dominate deployed systems:

1. They run deterministically at sensor rate (10–20 Hz) on CPUs — no GPU required.
2. They have no train/test distribution mismatch: ICP does not assume anything about the scene, only that geometry exists.
3. They are interpretable: failure modes (too few inliers, degenerate normals, large initial error) are diagnosable at runtime.
4. Decades of field experience and tuned implementations exist in PCL, libpointmatcher, Open3D.

---

## 3. DL Methods — What Works in the Lab

### 3.1 DCP and the 2019 Turning Point

**Deep Closest Point (DCP, ICCV 2019)** is the foundational learning-based registration method. [src: 06-04-arxiv-1905-03304.md] It replaces ICP's three components with learned counterparts:

1. **DGCNN embedding** — per-point features capturing local k-NN geometry (outperforms simpler PointNet-only features by ~5× on rotation MSE).
2. **Cross-attention (Transformer) module** — computes task-specific contextual features by attending each point in X to all points in Y; makes features dependent on *both* clouds simultaneously.
3. **Differentiable SVD** — outputs the rigid transformation directly from the soft correspondence matrix; end-to-end differentiable.

**DCP benchmark results on ModelNet40 (full train/test):** RMSE(R) = 1.14°, RMSE(t) = 0.0018 (DCP-v2), versus ICP RMSE(R) = 29.9°. [src: 06-04-arxiv-1905-03304.md] DCP is also fast: 0.008 s per pair at 1024 points (vs. 15 s for Go-ICP), and robust to Gaussian noise.

However: DCP was trained and tested on **ModelNet40 CAD object models** with rotations uniformly sampled in [0°, 45°]. These are clean, complete, isolated objects — very different from partial, noisy, outdoor LiDAR scans.

### 3.2 Successor Methods — A Rich Taxonomy

The 2024 survey [src: 02-01-arxiv-2404-13830.md] categorizes over 100 DL-PCR methods published 2017–2025 into five supervised tracks:

**By registration procedure component improved:**
- *Descriptor extraction*: FCGF (fully-convolutional sparse), SpinNet (cylindrical equivariance), GeoTransformer (geometric structure encoding)
- *Overlap prediction*: Predator (first overlap-attention model, 88.5% Registration Recall on 3DMatch vs. 88.2% for CoFiNet), RORNet
- *Similarity matrix optimization*: PRNet, SHM (soft-to-hard Sinkhorn)
- *Outlier filtering*: PointDSC (spatial compatibility), MAC (maximal cliques), SC²-PCR++
- *Transformation estimation*: RANSAC-based or SVD-based

**Key architectural trend: Transformers** dominate since 2022. GeoTransformer (2023) encodes distance/angle within the attention framework and achieves 91.3% Registration Recall on 3DMatch, 73.1% on the harder low-overlap 3DLoMatch (60% at 250 correspondences for Predator by comparison). [src: 02-01-arxiv-2404-13830.md]

**Best results on 3DMatch benchmark (Registration Recall at 5000 correspondences):**

| Method | 3DMatch RR (%) | 3DLoMatch RR (%) |
|---|---|---|
| FCGF (2019) | 85.0 | 40.3 |
| Predator (2021) | 89.5 | 60.8 |
| GeoTransformer (2023) | 91.7 | 73.0 |
| SIRA-PCR (2023) | 93.7 | 74.4 |
| Diff-Reg (2024) | 94.3 | 73.2 |
| PARE-Net (2024) | 94.2 | 73.7 |

[src: 02-01-arxiv-2404-13830.md]

**Best results on KITTI (outdoor driving, Registration Recall):** Nearly every method reaches ≥99.8% RR on KITTI — the benchmark is saturated at the coarse level. Differentiators are RRE and RTE: PARE-Net achieves RRE = 0.23°, RTE = 4.9 cm; DCATr achieves the best rotation error at 0.22°. [src: 02-01-arxiv-2404-13830.md]

**Unsupervised methods** (correspondence-free and correspondence-based) address the labeling bottleneck. They typically use Chamfer Distance as a self-supervised signal. Performance lags supervised methods by 5–15 percentage points on 3DMatch.

---

## 4. Why DL Isn't Deployed: The Specific Gaps

This is the core question. The literature across all five sources converges on a consistent set of barriers.

### 4.1 Generalization — The Training Distribution Problem

Supervised DL-PCR methods "rely on labeled training data to guide the training process... obtaining such annotated data in real-world scenarios is both challenging and costly." [src: 02-01-arxiv-2404-13830.md] The typical training pipeline uses ModelNet40 (40 CAD categories) or 3DMatch/3DLoMatch (indoor RGB-D). Neither matches outdoor UAV LiDAR data.

When tested on unseen *categories* (category-split experiment), DCP-v2 RMSE(R) degrades from 1.14° to 3.15° — a 2.8× increase. [src: 06-04-arxiv-1905-03304.md] For outdoor scenes this gap is far larger: the distribution of outdoor LiDAR data (sparse, large-scale, unstructured vegetation, varying point density with range) is fundamentally different from the training benchmarks.

The survey identifies **synthetic-to-real transfer** as a central unresolved challenge: "methods based on generative adversarial networks and diffusion models face several challenges, including unstable training, slow data generation, and discrepancies between synthetic and real-world data distributions." [src: 02-01-arxiv-2404-13830.md]

### 4.2 Robustness to Real-World Corruptions

The RobustLOL study [src: 01-02-arxiv-2409-10824.md] is the most direct evidence of the deployment gap. It evaluates five LiDAR odometry systems (two classical, three learning-based) under 18 synthetic real-world corruptions (weather, noise, density perturbations):

**Key finding:** Under corruptions, odometry position errors escalate from 0.5% to **more than 80%**. Learning-based systems are *more sensitive* than classical ones:

- **DeLORA** (learning-based): sensitive to rain, fog, Gaussian/uniform/impulse noise in Cartesian coordinates, density decreases, cutouts, and layer deletions — RPEtrans increases substantially.
- **KISS-ICP** (classical, direct): highly sensitive only to *background noise* (uniformly distributed spurious points), where RPEtrans rises from <0.6% to >80% — a single, well-understood failure mode that a detection-and-filter pipeline can fix.
- **MULLS** (classical, feature-based): sensitive mainly to *local density decrease* at high severity (RPEtrans 0.3% → >18%).
- **NeRF-LOAM** (neural): shows "substantial instability" with non-monotonic corruption-severity response — results vary across *identical re-runs* due to random network initialization. [src: 01-02-arxiv-2409-10824.md]

The study proposes two mitigations: (1) a lightweight detection-and-filter pipeline (CNN corruption classifier → bilateral filter) that restores KISS-ICP to near-clean performance; (2) fine-tuning DeLORA on corrupted data reduces errors by up to 35.8% across corruption types. But this second approach requires knowing in advance which corruptions will be encountered — an assumption that breaks in novel environments.

### 4.3 Environmental Change — Scan-to-Map Mismatches Over Time

The ICP-in-evolving-environments study [src: 05-05-arxiv-2507-17531.md] introduces a weekly multi-temporal outdoor dataset (Feb–Apr 2025, natural forest + semi-urban). Key findings for localization:

- **Short-term changes accumulate**: vegetation growth causes median map-change of 1.6–8.7% in natural environments over a few weeks; a single parked truck can cause 9.5% local change in semi-urban settings.
- **Point-to-Plane ICP** consistently outperforms Point-to-Point ICP in evolving environments: translation error stays within 0.1–0.2 m vs. occasional 0.25 m for PtP; rotation error stays below 1° vs. occasional peaks for PtP.
- Both ICP variants fail at **symmetric corridors** (vegetation lining path = ambiguous lateral correspondence), **flat featureless ground**, and **sudden object changes** (parked cars, new branches). [src: 05-05-arxiv-2507-17531.md]

No learned methods were included in this study — a deliberate choice reflecting that current benchmarks do not cover the short-horizon temporal variation dimension. This represents an unevaluated gap for DL methods.

### 4.4 Latency and Compute

DCP at 1024 points takes 0.008 s per pair (fast in the learning-based context) but this is on a desktop GTX 1070. [src: 06-04-arxiv-1905-03304.md] More powerful transformer-based methods (GeoTransformer, PARE-Net) are heavier. At the 10–20 Hz scan rate demanded by LIO front-ends, the allowed time budget per registration step is 50–100 ms. On embedded hardware (Jetson Orin NX), this is achievable for lightweight networks, but requires careful profiling and may conflict with simultaneous navigation and planning workloads.

The survey does not report embedded-hardware latency for modern methods — all evaluations run on RTX 4090. [src: 02-01-arxiv-2404-13830.md]

### 4.5 Data Generation and Label Cost

Supervised methods require ground-truth transformation labels between point cloud pairs. For indoor scenes, RGB-D datasets with reconstruction-based poses exist (3DMatch). For outdoor LiDAR at scale, high-accuracy ground truth is expensive (RTK GNSS, survey-grade scanners), and the diversity required to cover deployment environments is enormous. This limits the effective training set. [src: 02-01-arxiv-2404-13830.md]

### 4.6 Degenerate Geometry — Classical Methods Also Struggle Here

It is worth noting that *classical methods also fail* in geometrically degenerate environments. The evolving-environments study and GenZ-LIO both document that point-to-plane ICP fails in corridors (insufficient lateral constraints), flat ground (no vertical constraints), and waterway environments (missing water-surface returns). [src: 07-03-arxiv-2603-16273.md, 05-05-arxiv-2507-17531.md] DL methods have not been shown to solve these structural failures — they inherit them, or introduce different ones.

---

## 5. Recent Attempts to Close the Gap

### 5.1 GenZ-LIO (2026) — Adaptive Classical, Not Learned

GenZ-LIO [src: 07-03-arxiv-2603-16273.md] is notable precisely because it improves deployment robustness *without* learned registration. Its three contributions address concrete deployment barriers:

1. **Scale-aware adaptive voxelization**: A PID-derived feedback controller adjusts voxel size dynamically as the robot moves between indoor (confined, dense points) and outdoor (open, sparse points) spaces. Fixed voxel sizes cause FAST-LIO2 and most other classical LIO systems to diverge in confined staircases or stairwell-to-hallway transitions. GenZ-LIO achieves **0.00% divergence across 42 sequences** from 10 datasets (FAST-LIO2 diverges on several of these). [src: 07-03-arxiv-2603-16273.md]

2. **Hybrid-metric state update**: Combines point-to-plane (reliable in structured, planar environments) and point-to-point (reliable in unstructured, non-planar environments) residuals within a single ESIKF update, weighted by per-correspondence uncertainty. This mitigates LiDAR degeneracy in waterway and off-road sequences where pure point-to-plane methods suffer drift.

3. **Voxel-pruned correspondence search**: Reduces computational overhead of point-to-point matching by ~30–50% without accuracy loss.

The approach is deployable today: no GPU, no training data, deterministic behavior.

### 5.2 RobustLOL Fine-Tuning (2024)

The corruption fine-tuning approach [src: 01-02-arxiv-2409-10824.md] shows that a learned odometry system (DeLORA) can be made substantially more robust through data augmentation with corruption types, reducing RPEtrans by up to 35.8%. This is not a full solution — it requires advance knowledge of expected corruption types — but it suggests that pre-deployment corruption-profiling of the target environment and subsequent model fine-tuning is a viable engineering path.

### 5.3 SIRA-PCR and Pretrain-Based Methods (2023)

SIRA-PCR [src: 02-01-arxiv-2404-13830.md] pre-trains on the synthetic FlyingShapes dataset and applies simulation-to-real domain adaptation, achieving 93.2% Registration Recall on 3DMatch (top-3 overall). This addresses the training data cost barrier by generating synthetic pairs rather than requiring real-world ground truth. However, SIRA-PCR is evaluated on the 3DMatch indoor benchmark — its outdoor LiDAR performance is untested.

### 5.4 Point-TTA (Test-Time Adaptation)

Point-TTA [src: 02-01-arxiv-2404-13830.md] uses a meta-auxiliary learning framework to update model parameters during inference using self-supervised auxiliary tasks (point cloud reconstruction, feature learning, correspondence classification). This allows adaptation to unseen data distributions without retraining, partially addressing the generalization barrier.

---

## 6. Implications for Our SLAM Stack

*This section is synthesis and editorial judgment.*

**Should FAST-LIO2 (classical) remain the choice for Phase-1?**

Yes, clearly. The evidence from all five sources converges on this conclusion:

1. No DL-PCR method has been deployed in a flying LiDAR system at scan rate on embedded hardware. GenZ-LIO (the most deployment-ready system in the sources) is itself classical, building on FAST-LIO2's ESIKF architecture.

2. FAST-LIO2's known failure modes (fixed voxel size in scale-variant scenes, pure point-to-plane degeneracy in unstructured outdoor environments) are addressed by GenZ-LIO — a direct drop-in upgrade if needed. This is a lower-risk improvement path than switching to a learned front-end.

3. Learning-based robustness to corruptions requires domain-specific fine-tuning. For an indoor home drone operating in a known environment, the relevant corruption types (low dust, reflective surfaces, sparse features near floor) can be characterized and added to training data if we ever switch — but the baseline classical system does not require this.

4. The deployment gap is structural, not just a maturity issue. The fundamental problem is that learned features encode assumptions about training geometry; ICP encodes no such assumptions. For Phase-1 (fiducials-first, then LiDAR-SLAM), ICP-family registration is the right default.

**When would a learned registration component make sense?**

- When the deployment environment has a large initial misalignment problem (DCP showed it can serve as initialization for ICP, which then polishes the result [src: 06-04-arxiv-1905-03304.md]).
- For long-term loop closure (place recognition + coarse re-localization after GPS denial), where learning-based global descriptors (NetVLAD-style) outperform classical approaches — this is adjacent to registration but distinct.
- Once a method achieves <5 ms per scan on Jetson Orin NX, generalizes across indoor/outdoor without fine-tuning, and shows comparable corruption robustness to KISS-ICP. That point has not been reached as of early 2026.

---

## 7. Maturity Table

| Method class | Representative | Benchmark performance | Embedded hardware | Real-world deployed |
|---|---|---|---|---|
| ICP (point-to-point) | KISS-ICP | Competitive KITTI; less robust to background noise | Yes (CPU) | Yes (widely) |
| ICP (point-to-plane) | FAST-LIO2 | Top-tier KITTI, indoor benchmarks | Yes (CPU) | Yes (widely) |
| Adaptive classical LIO | GenZ-LIO | 0% divergence on 42 sequences; 2nd ATE | Yes (CPU) | Research prototype |
| DL: attention-based | DCP (2019) | RMSE(R) 1.1° on ModelNet40 | Possible on GPU | Lab only |
| DL: transformer | GeoTransformer | 91.3% RR on 3DMatch | Not benchmarked on edge | Lab only |
| DL: best overall | PARE-Net / Diff-Reg | 94.2–94.3% RR on 3DMatch | Not benchmarked on edge | Lab only |
| DL: learning-based LO | DeLORA | Competitive clean KITTI; −36% under fine-tuned corruptions | Untested on UAV hardware | Lab only |
| Neural: NeRF-based | NeRF-LOAM | Competitive but non-deterministic across runs | Requires 24 GB VRAM | Lab only |

Sources: [src: 02-01-arxiv-2404-13830.md, 01-02-arxiv-2409-10824.md, 06-04-arxiv-1905-03304.md, 07-03-arxiv-2603-16273.md]
