# SLAM Reading List — indoor & outdoor, AI methods (LiDAR + camera)

Curated for the **home-tidy indoor drone** project: ArduPilot/PX4 flight controller + **Jetson Orin NX/Nano** companion, ROS 2, GPS-denied, **Livox MID360 + IMU** as primary sensing and RGB/stereo cameras secondary. Priority is **edge-deployable, AI/learning-based SLAM using LiDAR and/or cameras**. Both indoor and outdoor methods are included; **indoor cluttered/featureless robustness is the hard problem**.

Compiled 2026-05-24. Two tiers:

- **Part A — Foundations already in our wiki** ✅ — captured + synthesized; start here, every entry is traceable to a wiki page.
- **Part B — Latest & greatest (research sweep)** 🔎 — found via a web sweep on 2026-05-24, **not yet captured/ingested** into the wiki. Treat as candidates; verify before relying on them. Low-confidence items flagged.

**Legend:** `LiDAR` · `cam-mono` · `cam-stereo` · `LVI` (LiDAR-visual-inertial) · `event` | edge = plausibly real-time on Jetson-class compute (✓ verified on Jetson / ~ likely / ✗ desktop-GPU-only / ? unknown).

---

## Priority reading path (if you only do a few)

1. **GS-LIVO** (Part B §3/§5) — real-time Gaussian-map LiDAR-visual-inertial SLAM **verified on Jetson Orin NX** with our exact sensor suite, code from the FAST-LIO lab. The single closest match to this build.
2. **`wiki/fast-lio-mid360-orin.md`** ✅ (Part A) — the concrete classical-LIO build path you start from (FAST-LIO2 + MID360 + Orin).
3. **`wiki/slam.md`** ✅ — the concept hub (localization + mapping + loop closure; VIO vs LIO; odometry vs SLAM).
4. **`wiki/indoor-cluttered-slam.md`** ✅ — why indoor is hard (featureless walls, symmetric-room aliasing, dynamic movers, multi-floor) and what current systems do about it.
5. **Depth Anything V2** (Part B §4) — closes our standing learned-monocular-depth gap; proven 40+ FPS on Orin NX via TensorRT.
6. **NeRF/3DGS-SLAM survey** (Part B §8) — the map of the radiance-field-SLAM landscape; read to situate everything in §2/§3/§7.

> **Landscape shift — now ingested & corrected (2026-05-25):** our wiki previously stated 3DGS-SLAM is desktop-GPU-only. The sweep found multiple real-time-on-Jetson results (GS-LIVO, RTGS, MemGS, VIGS-Fusion). **GS-LIVO has been captured and ingested into [`wiki/learned-slam.md`](wiki/learned-slam.md), and the outdated claim has been corrected on [`wiki/slam.md`](wiki/slam.md) and [`wiki/indoor-cluttered-slam.md`](wiki/indoor-cluttered-slam.md)** (GS-LIVO: Jetson Orin NX, 48.3 ms/frame ≈ 20 Hz).

---

## Part A — Foundations already in our wiki ✅

Each links to the synthesizing wiki page (which carries full raw-source citations).

### Core concepts (read first)
- [`wiki/slam.md`](wiki/slam.md) — what SLAM is; localization + mapping + loop closure; VIO vs LiDAR-inertial; how pose reaches the flight controller.
- [`wiki/drone-sensors-for-autonomy.md`](wiki/drone-sensors-for-autonomy.md) — sensor → purpose → maturity → SWaP tradeoff across camera/event/LiDAR/IMU/GNSS/radar.
- [`wiki/lidar-vs-vision-autonomy.md`](wiki/conflicts/lidar-vs-vision-autonomy.md) — the open LiDAR-vs-vision debate; the central architectural fork.

### LiDAR-inertial odometry (LIO) — our build's primary path · `LiDAR`
- **FAST-LIO2** — arXiv [2107.06829](https://arxiv.org/abs/2107.06829); code [hku-mars/FAST_LIO](https://github.com/hku-mars/FAST_LIO/tree/ROS2). iterated-EKF + ikd-tree; ~5 ms/scan on ARM. edge ✓. → synthesis: [`wiki/fast-lio-mid360-orin.md`](wiki/fast-lio-mid360-orin.md).
- **Point-LIO** — high-rate point-wise LIO; [overloadsc/Point-LIO-Mid360](https://github.com/overloadsc/Point-LIO-Mid360). edge ✓.
- **LI-Init** (target-free LiDAR-IMU extrinsic+temporal calibration, IROS 2022) — [hku-mars/LiDAR_IMU_Init](https://github.com/hku-mars/LiDAR_IMU_Init).
- **FAST_LIO_SLAM** (adds Scan-Context + GTSAM loop closure) — [gisbi-kim/FAST_LIO_SLAM](https://github.com/gisbi-kim/FAST_LIO_SLAM); **spark-fast-lio** (ROS2 + KISS-Matcher loop closure) — [MIT-SPARK/spark-fast-lio](https://github.com/MIT-SPARK/spark-fast-lio).
- **HKU MaRS LiDAR-UAV survey 2025** — arXiv [2509.10730](https://arxiv.org/abs/2509.10730). → [`wiki/lidar-for-uav-autonomy.md`](wiki/lidar-for-uav-autonomy.md) (the "LiDAR-necessary" position).

### LiDAR-visual-inertial (LVI) fusion · `LVI`
- **FAST-LIVO2** (MID360 + fisheye, ROS2 fork) — [Rhymer-Lcy/FAST-LIVO2-ROS2-MID360-Fisheye](https://github.com/Rhymer-Lcy/FAST-LIVO2-ROS2-MID360-Fisheye).
- **LiDAR-Visual-Inertial-SLAM on Orin NX** (MID360 + IMX219, Humble + CUDA + Docker) — [valentinomario/LiDAR-Visual-Inertial-SLAM](https://github.com/valentinomario/LiDAR-Visual-Inertial-SLAM). edge ✓.
- → both summarized in [`wiki/fast-lio-mid360-orin.md`](wiki/fast-lio-mid360-orin.md).

### Visual-inertial SLAM (camera + IMU) · `cam-stereo`
- **OKVIS2 forest VI-SLAM** — arXiv [2403.09596](https://arxiv.org/abs/2403.09596) (TUM/Imperial): stereo+IMU-only, no LiDAR/GNSS, 226 m forest mission <0.5% drift, fully onboard Orin NX. Learned stereo-depth CNN front-end (the camera-camp counterpoint). → [`wiki/visual-inertial-slam.md`](wiki/visual-inertial-slam.md).

### Indoor / cluttered-environment SLAM (the hard case) — synthesized in [`wiki/indoor-cluttered-slam.md`](wiki/indoor-cluttered-slam.md)
- **SlideSLAM** — arXiv [2406.17249](https://arxiv.org/abs/2406.17249) · decentralized object-level metric-semantic SLAM (air+ground teams). `LiDAR`/`cam`
- **3D Active Metric-Semantic SLAM** — arXiv [2309.06950](https://arxiv.org/abs/2309.06950) · multi-floor exploration; semantic loop closure cuts position error 83–93%. `cam`
- **GLC-SLAM** — arXiv [2409.10982](https://arxiv.org/abs/2409.10982) · 3DGS SLAM w/ hierarchical loop closure (suppresses repetitive-furniture false loops). `cam` · edge ✗ (desktop)
- **VIGS SLAM** — arXiv [2501.13402](https://arxiv.org/abs/2501.13402) (large-scale, dynamic people) · **ETH VIGS-SLAM** [2512.02293](https://arxiv.org/abs/2512.02293). `cam`
- **TWC-SLAM** — arXiv [2510.22754](https://arxiv.org/abs/2510.22754) · text + WiFi fusion to break symmetric-corridor aliasing (FAST-LIO2 front-end). `LiDAR`
- **RD-VIO** — arXiv [2310.15072](https://arxiv.org/abs/2310.15072) · dynamic-keypoint rejection + pure-rotation handling. `cam-mono`
- **NUFR-M3F dataset** — arXiv [2306.08522](https://arxiv.org/abs/2306.08522) · benchmark exposing symmetric-floor false loops + elevator-transit failures. (dataset)
- **End-to-end DRL avoidance** — arXiv [2503.14352](https://arxiv.org/abs/2503.14352) · LiDAR range-image → acceleration; 6 m/s, 3.4–5.2 ms inference on N100. `LiDAR` · edge ✓
- **Amazon large-scale indoor mapping** — VIO health-tracker + session merging (grocery stores 1700–3700 m²). `cam`

### Learned end-to-end control (SLAM-free pixel→action) · `cam-mono`
- **Dream-to-Fly** — arXiv [2501.14377](https://arxiv.org/abs/2501.14377) (ETH RPG, ICRA 2026): DreamerV3 model-based RL, pixels→control, no LiDAR, ≤9 m/s. The "skip explicit SLAM" position. → [`wiki/dream-to-fly.md`](wiki/dream-to-fly.md).

### Event-camera perception (alternative high-speed/low-light front-end) · `event`
- [`wiki/event-cameras.md`](wiki/event-cameras.md), [`wiki/event-cameras-for-uavs.md`](wiki/event-cameras-for-uavs.md), [`wiki/eth-rpg-scaramuzza.md`](wiki/eth-rpg-scaramuzza.md) — µs-latency, >120 dB dynamic range; RPG agile-flight results.

### Turning SLAM into flight
- [`wiki/slam-fc-integration.md`](wiki/slam-fc-integration.md) — external SLAM pose → ArduPilot EKF3 / PX4 EKF2 via MAVROS `vision_pose`; frames, `EK3_SRC`, delay tuning, divergence pitfalls.

---

## Part B — Latest & greatest (research sweep 2026-05-24, not yet ingested) 🔎

Web-sweep candidates. arXiv IDs confirmed unless flagged **(low-confidence — verify)**. Prioritized for edge + LiDAR/camera + this build.

### 1. Learning-based / neural LiDAR-inertial odometry · `LiDAR`
- **★ KN-LIO** — arXiv [2501.04263](https://arxiv.org/abs/2501.04263) · ESKF front-end + learned neural-SDF map (a "neural FAST-LIO"). edge ~ (decoder cost unclear). *repo low-confidence.*
- **DFLIOM** — arXiv [2410.02961](https://arxiv.org/abs/2410.02961) · learned registration-relevant features; 20 Hz, **57.5% memory cut** vs SOTA — the edge angle. edge ~.
- **DELO** (WACV 2024) — arXiv [2308.07153](https://arxiv.org/abs/2308.07153) · deep *evidential* LiDAR odometry — emits uncertainty (knows when it's untrustworthy in featureless rooms). edge ?.
- *Reality check: fully end-to-end neural LIO that beats FAST-LIO2 on Jetson does not yet exist; the above are classical-with-learned-pieces.*

### 2. Deep / learned visual-inertial odometry · `cam-mono` (+IMU)
- **★ DPV-SLAM** (ECCV 2024) — arXiv [2408.01654](https://arxiv.org/abs/2408.01654); code [princeton-vl/DPVO](https://github.com/princeton-vl/DPVO) · DPVO + loop closure; 60 FPS / 4.9 GB on RTX-3090, ~2.5× faster than DROID-SLAM — lightest credible learned VO to port to Orin (needs TensorRT/quantization). edge ~.
- **MASt3R-SLAM** (CVPR 2025 Highlight) — arXiv [2412.12392](https://arxiv.org/abs/2412.12392); code [rmurai0610/MASt3R-SLAM](https://github.com/rmurai0610/MASt3R-SLAM) · foundation-model dense SLAM, no calibration needed; 15 FPS on strong GPU. edge ✗ (watch for distilled variants).
- **Adaptive VIO** (CVPR 2024) — arXiv [2405.16754](https://arxiv.org/abs/2405.16754) · online continual learning; self-tunes to unseen rooms. edge ~.
- **RWKV-VIO** (Sensors 2025) — [mdpi 25/18/5737](https://www.mdpi.com/1424-8220/25/18/5737) · linear-attention end-to-end VIO chosen for efficiency. edge ~. *code unverified.*
- *Direction-of-travel: SLAM-Former (arXiv 2509.16909), one-transformer SLAM — desktop-only, watch only.*

### 3. Real-time 3DGS / neural-implicit SLAM on edge — **the area that moved most**
- **★ GS-LIVO** (IEEE T-RO 2025) — arXiv [2501.08672](https://arxiv.org/abs/2501.08672); code [HKUST-Aerial-Robotics/GS-LIVO](https://github.com/HKUST-Aerial-Robotics/GS-LIVO) · `LVI` · **edge ✓ Jetson Orin NX 16 GB, 48.3 ms/frame**; IESKF + Gaussian map. *"First real-time Gaussian SLAM for embedded."* **Closest match to this build.**
- **RTGS** (MICRO 2025) — arXiv [2510.06644](https://arxiv.org/abs/2510.06644); code [UMN-ZhaoLab/RTGS](https://github.com/UMN-ZhaoLab/RTGS) · `cam` RGB-D · ≥30 FPS on edge GPU, 82.5× energy efficiency (pruning + dynamic downsampling). edge ✓.
- **GS-LIVM** (ICCV 2025) — arXiv [2410.17084](https://arxiv.org/abs/2410.17084); code [xieyuser/GS-LIVM](https://github.com/xieyuser/GS-LIVM) · `LVI` photorealistic mapping companion to GS-LIVO. edge ~.
- **MemGS** (2025) — arXiv [2509.13536](https://arxiv.org/abs/2509.13536) · `cam` RGB-D · >30 FPS on AGX Orin 64 GB; tackles the VRAM wall. edge ✓. *code unverified.*
- **VIGS-Fusion** (HAL preprint 2025) — [hal-05192786](https://hal.science/hal-05192786v1) · `cam`-VI · 14 FPS **onboard a small quadrotor** — closest published flying-platform match. **(low-confidence — preprint, code unverified.)**

### 4. Monocular / stereo metric-depth foundation models · `cam-mono`
- **★ Depth Anything V2** (NeurIPS 2024) — arXiv [2406.09414](https://arxiv.org/abs/2406.09414); code [DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2); **Jetson path** [IRCVLab/Depth-Anything-for-Jetson-Orin](https://github.com/IRCVLab/Depth-Anything-for-Jetson-Orin) · **40+ FPS on Orin NX via TensorRT**. Closes our standing mono-depth gap. edge ✓.
- **Metric3D v2** (TPAMI 2024) — arXiv [2404.15506](https://arxiv.org/abs/2404.15506); code [YvanYin/Metric3D](https://github.com/YvanYin/Metric3D) · zero-shot metric depth **+ surface normals** (planar-structure bonus indoors). edge ~ (heavy).
- **UniDepth V2** (2025) — arXiv [2502.20110](https://arxiv.org/abs/2502.20110); code [lpiccinelli-eth/UniDepth](https://github.com/lpiccinelli-eth/UniDepth) · infers intrinsics at inference; robust if the camera changes. edge ~.
- **Prompt Depth Anything** (Dec 2024) — arXiv [2412.14015](https://arxiv.org/abs/2412.14015); [project](https://promptda.github.io/) · uses **low-res LiDAR to prompt** 4K metric depth — a natural MID360+camera fusion pattern. edge ~.
- **Mono metric depth via VIO rescaling for aerial nav** (Sep 2025) — arXiv [2509.08159](https://arxiv.org/abs/2509.08159) · fixes mono scale-ambiguity via VIO; **15 Hz onboard a quadrotor**. edge ✓. *repo unconfirmed.*

### 5. LiDAR-visual-inertial fusion SLAM beyond FAST-LIVO2 · `LVI`
- **★ GS-LIVO** — see §3 (top LVI pick too; Jetson-verified, your sensor suite).
- **LVI-Fusion** (Remote Sensing 2024) — [mdpi 16/9/1524](https://www.mdpi.com/2072-4292/16/9/1524) · robust to texture-less / illumination-varying scenes (your indoor failure modes). edge ~. *code verify.*
- **Detection-first tightly-coupled LVI in dynamic environments** (Measurement 2024) — [ScienceDirect S0263224124013915](https://www.sciencedirect.com/science/article/abs/pii/S0263224124013915) · handles moving people/pets. edge ~.
- *Note: 2025 LVI energy has shifted into Gaussian-map systems (§3), not new ESIKF variants.*

### 6. Learned loop closure / place recognition (symmetric/featureless indoor)
- **★ IS-CAT** (Sensors 2024) — [mdpi 24/2/582](https://www.mdpi.com/1424-8220/24/2/582) · `LiDAR` · intensity+spatial cross-attention, **validated on featureless indoor** data — squarely the hard problem. edge ~.
- **iBTC** (RA-L/IROS 2024) — code [hku-mars/iBTC](https://github.com/hku-mars/iBTC) · `LVI` · camera-assisted descriptor to disambiguate LiDAR-symmetric corridors; **same lab as FAST-LIO → easy integration.** edge ✓.
- **R2SCAT-LPR** (Remote Sensing 2025) — [mdpi 17/6/1057](https://www.mdpi.com/2072-4292/17/6/1057) · `LiDAR` BEV · rotation-robust (drone revisits at arbitrary yaw). edge ~.
- **OverlapTransformer** (RA-L 2022, mature baseline) — arXiv [2203.03397](https://arxiv.org/abs/2203.03397); code [haomo-ai/OverlapTransformer](https://github.com/haomo-ai/OverlapTransformer) · `LiDAR` · the cheap, fast learned-LPR baseline to benchmark against. edge ✓.

### 7. Foundation-model / VLM-aided semantic SLAM & open-vocab mapping · `cam`
- **★ OVO-SLAM** (Nov 2024) — arXiv [2411.15043](https://arxiv.org/abs/2411.15043) · online open-vocabulary 3D segments (CLIP-merge) on ORB-SLAM2 / Gaussian backbones — cleanest path to "find the toy / find the laundry." edge ~.
- **OpenVox** (Feb 2025) — Bayesian open-vocab instance voxel map. **(low-confidence — verify arXiv ID ~2502.)**
- **LEGO-SLAM** (Dec 2025) — language-embedded Gaussian open-vocab SLAM; 16-D feature compression for real-time. **(low-confidence — verify ID ~2512.)**
- **OpenMonoGS-SLAM** (Dec 2025) — arXiv [2512.08625](https://arxiv.org/abs/2512.08625) · open-vocab semantic SLAM from a single camera, no depth. **(low-confidence — very recent.)**
- **Learning from Feedback: foundation-model semantic enhancement for object SLAM** (Nov 2024) — arXiv [2411.06752](https://arxiv.org/abs/2411.06752) · object-centric SLAM refined by FM feedback. edge ~.

### 8. Surveys & benchmarks (read to situate the above)
- **★ How NeRFs and 3DGS are Reshaping SLAM: a Survey** — arXiv [2402.13255](https://arxiv.org/abs/2402.13255); list [awesome-NeRF-and-3DGS-SLAM](https://github.com/3D-Vision-World/awesome-NeRF-and-3DGS-SLAM). The map of radiance-field SLAM (70+ systems).
- **Survey on Collaborative SLAM with 3DGS** — arXiv [2510.23988](https://arxiv.org/abs/2510.23988) (multi-agent / multi-session).
- **A Frontier Review of Semantic SLAM for the Open World** (Sensors 2025) — [mdpi 25/16/4994](https://www.mdpi.com/1424-8220/25/16/4994) (companion to §7).
- **NeRF & Gaussian Splatting SLAM in the Wild** — arXiv [2412.03263](https://arxiv.org/abs/2412.03263) (reality check on §3).
- **SLAM&Render benchmark** (2025) — 3DGS/SLAM intersection benchmark. **(low-confidence — verify arXiv ID.)**

---

## Ingested (2026-05-25) → [`wiki/learned-slam.md`](wiki/learned-slam.md) ✅

The top-candidate shortlist below was captured and ingested into the new **[`wiki/learned-slam.md`](wiki/learned-slam.md)** synthesis page:

1. **GS-LIVO** (2501.08672 + repo) ✅ — Jetson-verified LVI Gaussian SLAM; corrected our "3DGS desktop-only" claim.
2. **Depth Anything V2** (2406.09414 + Jetson repo) ✅ — closes the learned-mono-depth gap with a real Orin deployment.
3. **DPV-SLAM / DPVO** (2408.01654 + repo) ✅ — lightest learned visual SLAM to attempt on Orin.
4. **iBTC** (HKU-MARS repo) ✅ — learned place recognition for symmetric/featureless indoor. **IS-CAT** (Sensors/MDPI) ✗ — bot-walled; **manual-download follow-up** (download the PDF from mdpi.com/1424-8220/24/2/582 and drop into `raw/research/learned-slam/`).
5. **NeRF/3DGS-SLAM survey** (2402.13255) ✅ — landscape framing in `learned-slam`.
6. **DFLIOM** (2410.02961) and **KN-LIO** (2501.04263) ✅ — the neural-LIO edge.

**Still uncaptured (next candidates if you want to go deeper):** the §3 edge-3DGS cluster beyond GS-LIVO (RTGS, MemGS, VIGS-Fusion), the §4 depth models beyond DAv2 (Metric3D v2, UniDepth V2, Prompt Depth Anything), and the §7 open-vocab semantic-SLAM group (OVO-SLAM et al.). Say the word to capture any of these.

---

*Provenance: Part A entries trace to captured sources cited on the linked wiki pages. Part B is an uncaptured web research sweep (2026-05-24) — candidates, not yet verified against captured content; low-confidence flags mark items whose arXiv ID or code repo was not confirmed.*
