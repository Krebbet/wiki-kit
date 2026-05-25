# Learned SLAM, Odometry & Depth

The AI-methods layer of the SLAM cluster: learning-based LiDAR-inertial odometry, deep visual SLAM, monocular metric-depth foundation models, neural/Gaussian map representations, and learned place recognition — filtered for edge deployability on a Jetson Orin NX/Nano companion. This page complements [[slam]] (concept hub), [[fast-lio-mid360-orin]] (the classical-LIO build path), and [[indoor-cluttered-slam]] (the indoor problem and classical/semantic systems); reference those for foundations rather than re-reading them here. The headline for this build: real-time 3D Gaussian-Splatting SLAM is now demonstrated on-board the exact Orin NX target, breaking the prior assumption that radiance-field SLAM is desktop-GPU-only.

## Landscape

SLAM has moved through three eras — hand-crafted geometry, then deep learning, and most recently Neural Radiance Fields (NeRF) and 3D Gaussian Splatting (3DGS) as scene representations — with the inflection point at iMAP (2021); 2024 publication volume in NeRF/3DGS-SLAM is sharply up *(survey)*. The recurring tension for an edge build is that radiance-field maps deliver photorealistic, dense, gap-filling reconstructions but historically demanded heavy GPU memory and compute, while classical explicit maps (point cloud, surfel, patch) are real-time-cheap but feature-hungry and non-photorealistic *(survey, GS-LIVO)*. The methods below are the subset that close that gap enough to matter on-board.

## Learned LiDAR-inertial odometry (DFLIOM, KN-LIO)

These keep the LIO skeleton ([[fast-lio-mid360-orin]] is the classical baseline) and inject learning at the point-selection or map-representation layer.

**DFLIOM** replaces hand-crafted edge/plane feature extraction with a light-weight learned feature extractor that scores points by saliency and uniqueness, then registers against only the most informative subset. Extending the authors' prior DLIOM, it achieves comparable-or-better localization using **~20% of the dense points**, reporting a **2.4% decrease in localization error and 57.5% decrease in memory usage vs DLIOM** *(claimed)*. The shared-weights network is small enough to infer in real-time; the extra feature-extraction time is offset by cheaper downstream registration, sustaining real-time operation at **20 Hz LiDAR** on the authors' setup. Evaluated on a desktop (i9-13900K, RTX 4090, 64 GB) — no Jetson port reported *(demoed, desktop)*. The memory-reduction angle is the directly relevant lesson for long indoor missions on a memory-bound Orin.

**KN-LIO** couples geometric kinematics with an online neural field: it represents the map as a neural point cloud, decodes point-to-surface SDF residuals via a small MLP, and fuses them in an IESKF (offered in semi-coupled and tightly-coupled variants), reconstructing a dense mesh as a by-product. It claims pose accuracy on par with or superior to SOTA LIO plus markedly better dense-mapping accuracy than pure-LiDAR neural reconstruction *(claimed)*. Demonstrated on drone (VIRAL), construction-site (HILTI 2022), and Newer College datasets — i.e. validated on aggressive aerial motion *(demoed)*. Real-time relies on GPU-accelerated spatial division; the captured source does not give an Orin/per-scan figure, so treat edge-readiness as unproven here.

## Learned visual / visual-inertial SLAM (DPV-SLAM / DPVO)

**DPVO** (Deep Patch Visual Odometry, NeurIPS 2023) is a sparse-patch deep VO frontend: instead of dense optical flow it tracks a small patch graph, which is what makes it cheap. **DPV-SLAM** (ECCV 2024) extends DPVO to full monocular SLAM on a *single GPU* by adding two loop-closure mechanisms — a proximity loop closure (camera-proximity, runs inside the patch-graph budget) and an optional classical backend (DBoW2 image retrieval + pose-graph optimization for large loops). Adding loop closure costs only a small hit: **60→50 FPS and 4 GB→5 GB GPU memory** *(claimed)*. It runs at **1x–4x real-time** with **5–7 GB** total overhead, hitting ~**50 FPS on EuRoC and ~39 FPS on KITTI** (2.5x and 3.9x real-time), matching DROID-SLAM accuracy at **2.5x the speed using a fraction of the memory (5 GB vs 20 GB; 50 vs 20 FPS)** *(demoed)*. Trained only on synthetic data with strong zero-shot generalization. Caveat: those FPS/VRAM figures are desktop-class GPU; no Orin numbers are captured, and 5–7 GB is tight on an 8 GB Orin Nano. Monocular-only, so it needs metric scale from elsewhere (IMU/LiDAR) for this build — see [[visual-inertial-slam]].

## Real-time Gaussian-Splatting SLAM on edge (GS-LIVO — the standout)

**GS-LIVO** (IEEE T-RO 2025) is the directly load-bearing result for this build: a tightly-coupled LiDAR-Inertial-Visual SLAM whose map *is* a 3D Gaussian field, claimed as **"the first real-time Gaussian-based SLAM framework deployable on resource-constrained embedded systems"** and **"the first real-time Gaussian-based SLAM system with online map updates deployed on an ARM-based embedded platform"**, demonstrated on **NVIDIA Jetson Orin NX (16 GB)** — the exact companion class for this build. All in C++/CUDA.

Design (extract): a **global Gaussian map** stored as **hash-indexed voxels in a recursive octree** for sparse-volume, multi-scale coverage; a **sliding window of Gaussians** (config: 20,000 Gaussians) optimized incrementally so only in-window Gaussians touch the GPU — this is the memory/compute trick that makes it fit; LiDAR-visual joint initialization; photometric-gradient optimization; and an **IESKF with sequential updates** tightly coupling LiDAR + image measurements (a redesign of the FAST-LIVO2 visual pipeline computing photometric loss on the current rendered frame). Map updates run >10 Hz indoors / ~3 Hz outdoors.

**Embedded deployment facts (Orin NX 16 GB, root voxel 0.5 m, 2 subdivision layers, 256×216 image):**
- optimization: **15.3 ms** per frame
- map maintenance: **18.9 ms** per frame
- **total pipeline: 48.3 ms/frame** (~20 Hz) at **PSNR 23.52 dB**
- per-component processing overhead averages ~**23 ms indoor / ~71 ms outdoor**
- total processing stays **below ~90–100 ms** in both indoor and outdoor large-scale runs at 10 Hz

The desktop comparison (TABLE IV, i9-13900KF + RTX 4090) makes the edge claim concrete: prior Gaussian-SLAM systems on the same indoor sequences ran at **541–851 ms/frame using 17–21 GB**, while **GS-LIVO ran at 48.5–63.4 ms using 1.2–1.5 GB** *(demoed)* — roughly a 10x speed and >10x memory reduction. It was further wrapped into a full autonomous-navigation stack (Gaussian map → 2D occupancy grid, A* global planning, LQR tracking) on a mobile chassis *(demoed)*. Note the Orin work was on a ground vehicle/handheld rig, not in flight, so airborne SWaP/vibration on a drone remains to be shown for this build.

## Monocular metric-depth foundation models (Depth Anything V2 + Jetson)

**Depth Anything V2** (NeurIPS 2024) is a monocular-depth foundation model trained by replacing all labeled real images with precise synthetic images, scaling a synthetic-only teacher, and distilling into smaller students via large-scale pseudo-labeled real images. It offers scales from **25M to 1.3B parameters**, produces finer and more robust depth than V1 and faster inference than SD-based models, and can be **fine-tuned with metric-depth labels** to emit metric (not just relative) depth *(demoed)*. For a LiDAR-primary build this is a secondary/complementary cue — dense depth fill-in for the RGB/stereo cameras in regions the Livox misses (thin structures, glass, close range).

Edge reality from the **Depth-Anything-for-Jetson-Orin** port (TensorRT, measured on **Orin 8 GB**, ViT-Small): **23.5 ms @ 308×308, 39.2 ms @ 364×364, 47.7 ms @ 406×406, 98.0 ms @ 518×518**, with **626–689 MB** memory across those input sizes *(demoed)*. Critically: **Base and Large models do not fit on the 8 GB Orin** (memory-limited) — only the Small model is viable on Nano-class hardware. So budget the small ViT at ~20–40 FPS depending on resolution, and expect the 16 GB Orin NX to extend that ceiling.

## Learned place recognition / loop closure (iBTC)

**iBTC** (RA-L 2024, HKU-MARS) is an image-assisting Binary-and-Triangle-Combined descriptor for place recognition that fuses LiDAR and camera measurements, improving on the LiDAR-only BTC/STD descriptors. The motivating failure mode is exactly the indoor one: **long, geometrically self-similar corridors where LiDAR-only loop detection aliases** ([[indoor-cluttered-slam]] covers symmetric-corridor aliasing in depth) — adding camera appearance disambiguates them *(claimed)*. It runs as a ROS (Melodic) node consuming undistorted LiDAR scans + poses and undistorted images + poses, emitting loop-closure transforms — i.e. a drop-in loop-closure module for a LIO frontend rather than a full SLAM system. The pairing it implies is a candidate fit for this build's Livox MID360 + RGB sensor set *(synthesis)*.

## Build notes

*(synthesis — recommendations, not claims from any single source)*

- **GS-LIVO is the closest match to this hardware**: LiDAR-Inertial-Visual, C++/CUDA, real-time on the literal Orin NX 16 GB target, and it consumes exactly the Livox + IMU + camera triad. It is the strongest evidence that Gaussian-map SLAM belongs in the on-board plan, not just on a desktop. Open risk: demonstrated on ground/handheld, not airborne.
- **DFLIOM's lesson is portable even without its code on Orin**: learned point-selection to cut LIO memory ~50% directly addresses the Orin memory ceiling on long indoor missions; pair the idea with the [[fast-lio-mid360-orin]] baseline.
- **Depth Anything V2 (Small, TensorRT)** is the realistic monocular-depth add-on — only the Small model fits 8 GB; fine-tune for metric depth if used for obstacle ranging, and treat it as camera-side fill-in to LiDAR, consistent with [[lidar-vs-vision-autonomy]].
- **DPV-SLAM is monocular and desktop-benchmarked**; its 5–7 GB footprint is borderline on Orin Nano and it needs external metric scale. Lower priority than the LIV stack for a LiDAR-primary build.
- **iBTC** is a sensible learned/descriptor-based loop-closure module to bolt onto the LIO frontend to fix corridor aliasing; verify the ROS Melodic → ROS 2 path.
- **KN-LIO** is promising (neural-field LIO validated on aggressive drone motion) but edge-timing is unproven in the captured source — watch, don't commit.

## Source

- `raw/research/learned-slam/01-gs-livo-arxiv.md` — GS-LIVO (IEEE T-RO 2025): real-time Gaussian-map LiDAR-Inertial-Visual SLAM; embedded-deployment timing/memory facts and the first-real-time-embedded-Gaussian-SLAM claim. https://arxiv.org/pdf/2501.08672
- `raw/research/learned-slam/02-gs-livo-repo.md` — GS-LIVO GitHub: module overview, "real-time on both high-end GPUs and edge devices", Orin NX 16 GB vs RTX 4090 test split. https://github.com/HKUST-Aerial-Robotics/GS-LIVO
- `raw/research/learned-slam/03-depth-anything-v2-arxiv.md` — Depth Anything V2 (NeurIPS 2024): synthetic-trained monocular depth foundation model, 25M–1.3B scales, metric-depth fine-tuning. https://arxiv.org/pdf/2406.09414
- `raw/research/learned-slam/04-depth-anything-jetson.md` — Depth-Anything-for-Jetson-Orin: TensorRT FPS/memory on Orin 8 GB (Small only; 23.5–98.0 ms; Base/Large OOM). https://github.com/IRCVLab/Depth-Anything-for-Jetson-Orin
- `raw/research/learned-slam/05-dpv-slam-arxiv.md` — DPV-SLAM (ECCV 2024): deep patch monocular SLAM with loop closure; 50/39 FPS, 5–7 GB, 1x–4x real-time. https://arxiv.org/pdf/2408.01654
- `raw/research/learned-slam/06-dpvo-repo.md` — DPVO/DPV-SLAM GitHub: patch-graph VO frontend, install/run, classical loop-closure backend (DBoW2 + DPRetrieval). https://github.com/princeton-vl/DPVO
- `raw/research/learned-slam/07-ibtc-repo.md` — iBTC (RA-L 2024, HKU-MARS): LiDAR+camera fused place-recognition/loop-closure descriptor, ROS node I/O. https://github.com/hku-mars/iBTC
- `raw/research/learned-slam/08-nerf-3dgs-slam-survey.md` — Tosi et al. survey "How NeRFs and 3DGS are Reshaping SLAM": evolution timeline and landscape framing. https://arxiv.org/abs/2402.13255
- `raw/research/learned-slam/09-dfliom-arxiv.md` — DFLIOM: learned-feature LiDAR-inertial odometry; ~20% of points, 2.4% error / 57.5% memory reduction vs DLIOM, 20 Hz. https://arxiv.org/pdf/2410.02961
- `raw/research/learned-slam/10-kn-lio-arxiv.md` — KN-LIO: geometric-kinematics + neural-field (online SDF) coupled LIO; IESKF; VIRAL/HILTI/Newer College. https://arxiv.org/pdf/2501.04263

## Related

- [[slam]] — concept hub for the SLAM cluster
- [[fast-lio-mid360-orin]] — the classical-LIO build path these methods augment or replace
- [[indoor-cluttered-slam]] — the indoor problem and classical/semantic systems
- [[visual-inertial-slam]] — VIO foundations; metric scale for monocular methods (DPV-SLAM, Depth Anything)
- [[lidar-for-uav-autonomy]] — LiDAR-inertial stack extended by the learned LIO methods here
- [[lidar-vs-vision-autonomy]] — sensor trade-offs framing the LiDAR-primary vs camera-fill-in choice
- [[nano-drone-compute]] — Orin NX/Nano compute and memory ceilings that gate these methods
- [[drone-sensors-for-autonomy]] — the Livox MID360 + IMU + RGB/stereo sensor set these consume
- [[home-tidy-drone-prototype]] — parent build this page serves
