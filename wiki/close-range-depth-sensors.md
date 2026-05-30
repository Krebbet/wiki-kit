# Close-Range Depth Sensors for Manipulation Perception

Research question: are there more directed, LiDAR-like sensors that give rich close-up depth readings in a narrower field of view — suited to robot arm manipulation and grasp pose estimation at 0.05–2 m range, where wide-FOV solid-state LiDAR (Livox MID360) gives too-sparse returns on small objects? Originally framed for drone manipulation; broadened to include ground-primary robot arm use cases (see §Implications).

Short answer: yes. Four sensor classes span the space from purpose-built arm cameras to PCB-scale miniature ToF arrays. The right choice depends on whether you need a 2D depth image (for grasp pose), presence/proximity detection near a gripper, noise models suitable for sim-to-real RL, or onboard neural inference without a host GPU.

---

## Sensor taxonomy

### (a) Stereo depth cameras — active structured-light / passive

Dense RGB-D cameras compute depth by matching features in two shifted images. Active variants project additional IR points to aid matching in low-texture scenes; passive variants (ZED 2) rely on texture and use neural networks for depth computation.

Key examples and specs (manufacturer-stated):

| Camera | Stereo tech | Ideal range (m) | Depth FOV | Max depth res | Weight | GPU needed | Price (USD) |
|--------|-------------|-----------------|-----------|---------------|--------|------------|-------------|
| RealSense **D405** | Active, global shutter | **0.07–0.5** | 87°×58° | 1280×720 @ 90 fps | ~60 g | No | est. ~$350 |
| OAK-D SR | Active, global shutter | **0.20–1.0** | — | 1 MP @ 120 fps | 72 g | No (RVC2 4 TOPS) | **$199** |
| RealSense D435 | Active | 0.3–3 | 87°×58° | 1280×720 | ~72 g | No | $314 |
| RealSense D455 | Active | 0.6–6 | 87°×58° | 1280×720 | ~124 g | No | $419 |
| ZED 2 | Passive | 0.3–20 | 110°×70° | 2208×1242 | ~175 g | Yes (CUDA) | $449 |
| OAK-D Pro | Active | 0.8–12 | 80°×55° | 1280×800 | ~97 g | No | $349 |

D435/D455/ZED 2/OAK-D Pro prices from [src: 02-02-arxiv-2501-07421.md]. D405 price not confirmed in captured sources — third-party estimate. OAK-D SR price $199 [src: 10-08-oak-d-sr-forum-discussion.md].

The stereo baseline governs the close-end of the useful range and depth-error growth: depth error grows quadratically with distance for fixed-baseline cameras; ZED 2 breaks this by computing depth via neural network [src: 02-02-arxiv-2501-07421.md].

#### Intel RealSense D405 — arm-manipulation specialist

The D405 is Intel's dedicated short-range depth camera, designed for robot arm, pick-and-place, and defect-inspection applications [src: 04-03-d405-realsenseai-product.md].

| Attribute | Value |
|-----------|-------|
| Ideal range | 7–50 cm |
| Min-Z (resolution-dependent) | 40 mm @ 424×240 · 70 mm @ 848×480 · 100 mm @ 1280×720 |
| Min object detection | 0.1 mm @ 7 cm |
| Depth accuracy | ±2% @ 50 cm |
| Depth FOV | 87°×58° |
| Max depth resolution | 1280×720 @ up to 90 fps |
| Image sensor | Global shutter |
| Dimensions | 42 × 42 × 23 mm (peripheral); 36.5 × 19.4 × 10.5 mm (D401 module) |
| Weight | ~60 g (third-party, unconfirmed primary) |
| Power (idle / streaming) | 35 mW / 1.55 W |
| IMU | No |
| Connectivity | USB 2.0 / USB 3.1 |
| Price | ~$350 est. |

[src: 04-03-d405-realsenseai-product.md, 05-04-d405-qviro-specs.md, 06-05-d405-digikey-forum.md]

**D435 vs D435i:** the "i" variant adds an onboard IMU (accelerometer + gyroscope), enabling visual-inertial odometry in RTAB-Map / ORB-SLAM3 without a separate IMU source. For room-mapping bench tests, D435i is preferred over bare D435 (~$20 premium). For a wrist-mount manipulation camera the IMU is irrelevant.

Key distinction from D435: the D405 uses a **smaller baseline with global shutter** optimised for the 7–50 cm envelope. The D435's minimum range (30 cm) excludes the final approach phase; the D405 captures it. D405 is not suited for distances >50 cm — a navigation camera handles everything beyond that range.

Practical note: Min-Z varies by resolution. At full 1280×720, the floor is 10 cm; at 848×480, it drops to 7 cm. Applications requiring the closest approach should use 848×480 or lower [src: 06-05-d405-digikey-forum.md].

#### Luxonis OAK-D SR — short-range with onboard AI

The OAK-D SR (Short Range) is Luxonis's dedicated arm/bin-picking camera, with a 20 mm baseline optimised for 30 cm–1 m and an onboard RVC2 neural inference chip [src: 02-04-oak-d-sr-docs-luxonis.md, 03-05-oak-d-sr-docs-hardware.md].

| Attribute | Value |
|-----------|-------|
| Ideal range | 30 cm – 1 m |
| MinZ (800P) | 20 cm |
| MaxZ | ~3 m (±10%) |
| Stereo baseline | 20 mm |
| Max depth resolution | 1 MP @ 120 fps (global shutter) |
| Onboard processor | RVC2 — 4 TOPS total / 1.4 TOPS AI |
| Encoding | H.264, H.265, MJPEG; 4K/30 or 1080p/60 |
| IMU | BNO085 9-axis |
| Dimensions | 56 × 36 × 25.5 mm |
| Weight | 72 g |
| Power | 2.5–3 W base; up to ~5 W with AI + stereo + encoder |
| Connectivity | USB-C (USB 3.2 Gen1, 5 Gbps) |
| Housing | Industrial aluminium + Gorilla Glass |
| Price | $199 |

[src: 02-04-oak-d-sr-docs-luxonis.md, 03-05-oak-d-sr-docs-hardware.md, 10-08-oak-d-sr-forum-discussion.md]

Key distinction: the RVC2 chip runs object detection, segmentation, and custom models **onboard without a host GPU** — relevant for a robot where inference budget is tight. Trade-off vs D405: 20 cm minimum range vs 7 cm for D405; on the other hand the OAK-D SR works down to ~1 m where the D405 becomes unusable.

### (b) ToF cameras — active, dense arrays

Dense ToF cameras emit modulated infrared light and measure round-trip phase/time across an array of pixels. Unlike stereo depth, accuracy does not degrade quadratically with distance; instead, error grows roughly linearly (or with a polynomial in distance and incidence angle).

Key example: **PMD Flexx2** [src: 03-03-arxiv-2412-15040.md]:

| Attribute | Value |
|-----------|-------|
| Resolution | 224×172 pixels |
| Depth FOV | 56°×44° |
| Max FPS | 60 Hz |
| Range | 0.1–7.0 m |
| Weight | 13 g |
| Dimensions | 72×19×11 mm |
| Power | 570–680 mW |
| Illumination | 940 nm IR |
| Measurement principle | ToF (iToF) |

Operating modes span 0.1–2.4 m (Mode 5, up to 60 fps) and 0.1–7.0 m (Mode 9, up to 30 fps) [src: 03-03-arxiv-2412-15040.md].

Its predecessor, the PMD Camboard Pico Flexx (8 g, 224×171, 62°×45°, 0.1–4 m, 45 fps), showed comparable results to the Kinect V2 despite its far smaller size [src: 03-03-arxiv-2412-15040.md].

### (c) Miniature ToF arrays — PCB-scale, sparse

Single-pixel or low-resolution (≤8×8) direct ToF sensors use SPAD (single-photon avalanche diode) technology. They are very small (<20 mm³), lightweight (<1 g), and power efficient (<10 mW per measurement) [src: 01-01-arxiv-2509-16122.md].

Key example: **AMS TMF8820** (used in Sifferman et al. experiments):
- 3×3 pixel array; 30° diagonal FOV (9 non-overlapping zones)
- Each pixel FOV: 10° diagonal (when using single zone as configured)
- Range: up to ~90 cm in the experimental configuration (bins 1–80)
- Frame rate: 3.5 Hz (limited by I²C histogram data bandwidth)
- Reports raw transient histograms — not just distance estimates
- Bin-to-distance calibration: distance (m) = 0.01387·i_peak − 0.1825 [src: 01-01-arxiv-2509-16122.md]

Related parts referenced in Sifferman et al. [src: 01-01-arxiv-2509-16122.md]:
- AMS OSRAM TMF882X family
- ST Microelectronics VL53L8CH (datasheet capture attempted but timed out; see §Source)
- ST VL6180X (proximity + ambient light, single-pixel)

Note: VL53L5CX (ST) is a closely related 8×8 SPAD array (64 zones, 61° diagonal FOV, 0.02–4 m range, up to 60 Hz, 2.4 mm × 7.0 mm package) — datasheet capture failed (ST website timeout); key specs sourced from cross-references in captured materials.

---

## Quantitative benchmarks

### Stereo depth cameras — planar surface accuracy

Measured at 0.6–4.0 m, 30 fps, default settings, ~420 lx, all cameras on the same host [src: 02-02-arxiv-2501-07421.md]:

| Camera | Bias at range | Standard deviation | Notes |
|--------|---------------|--------------------|-------|
| D435 | 1.87% at 2 m | 0.75% at 2 m | Degrades sharply above 3 m; best at close range |
| D455 | 0.13% at 4 m | 3.05% at 4 m | SD exceeds manufacturer spec at 4 m |
| ZED 2 | 0.22% at 2 m | 0.17% at 2 m | Best overall; neural-network depth |
| OAK-D Pro | 1.65% at 4 m | 1.47% at 4 m | Quantised "layers" at distance |

All cameras: bias <2 cm and SD <0.5 cm up to 100 cm [src: 02-02-arxiv-2501-07421.md].

### Stereo depth cameras — object perception (YCB + doll, Chamfer Distance)

At 60–150 cm (table-top manipulation range) all four cameras achieve Chamfer Distance ~1 cm on household objects. Beyond 150 cm, ZED 2 stays best (~2 cm at 300 cm); D435 degrades to ~5.5 cm at 300 cm [src: 02-02-arxiv-2501-07421.md].

At ≤150 cm (our target range): D435 best for complex curved shapes (pitcher, football); ZED 2 best for planar/simple shapes; OAK-D Pro produces quantised depth layers that hurt complex-shape Jaccard similarity [src: 02-02-arxiv-2501-07421.md].

### PMD Flexx2 — axial noise model

Axial noise (depth-direction σ in metres) is modelled as Gaussian, function of distance z (m) and incidence angle θ [src: 03-03-arxiv-2412-15040.md]:

σ_z(z, θ) = a + b·z + c·z² + d·z^2.7 · (θ² / (π/2 − θ)²)

Coefficients (Mode 5 30fps): a=0.002362, b=−0.001041, c=0.000753, d=0.000185.

- Model fit (average KL divergence across all modes): **0.015 nats** — very good Gaussian fit [src: 03-03-arxiv-2412-15040.md]
- Noise increases with distance at incidence angles ≥15°
- Mode 5 30fps has the lowest axial noise among tested modes at angles >15°
- Mode 9 30fps has lower noise at 0° incidence (direct facing)

Lateral noise (pixel-position uncertainty) standard deviations:
- Mode 5 30fps: σ_x = 0.864 pixel
- Mode 5 60fps: σ_x = 1.098 pixel
- Mode 9 30fps: σ_x = 1.649 pixel

Lateral noise does not trend clearly with distance or angle [src: 03-03-arxiv-2412-15040.md].

### AMS TMF8820 miniature ToF — object detection accuracy

In arm-mounted configuration (sensor mounted along UR5 link, facing end-effector), using raw transient histograms rather than on-sensor distance estimates [src: 01-01-arxiv-2509-16122.md]:

- **Average absolute distance error: 2.08 cm** (on objects 1–28 cm from sensor)
- True positive rate (TPR): **78.9%** on mixed object set (finger, hand, 1/2/4 cm foamboard) at 0–28 cm
- On-sensor distance estimates alone: limited to <5 cm range due to self-detection masking — cannot detect objects further than the robot surface in the pixel
- Self-detection false positive rate (FPR) at full sampling density: **~0.01** (1%)
- Ambient light degradation: FPR rises sharply at 1000 lux halogen; stable under fluorescent at 500 lux [src: 01-01-arxiv-2509-16122.md]

---

## Manipulation-specific findings

### Close-range object detection with miniature ToF arrays (Sifferman et al., arXiv 2509.16122)

The arm-mounted miniature ToF problem is dominated by **self-detection**: when sensors face along the arm, the robot itself occupies the pixels and standard distance-threshold filtering cannot see past it to detect approaching objects. The proposed solution — building a probabilistic model of the robot's expected transient histogram at each joint state, then detecting deviations at runtime — achieves 2.08 cm localisation error and 78.9% TPR [src: 01-01-arxiv-2509-16122.md].

Critical practical note: this method requires **~10 hours of reference data capture per sensor position** (overnight), though future work at coarser joint-space sampling could reduce this by an order of magnitude [src: 01-01-arxiv-2509-16122.md].

The sensor was configured for one 10° FOV zone (vs. the full 30° diagonal), limiting unwanted detections. Maximum range in this configuration: ~90 cm [src: 01-01-arxiv-2509-16122.md].

Non-line-of-sight (NLOS) effects on specular (metal) robot surfaces cause false positives from objects outside the direct FOV; covering the robot arm in masking tape mitigates this [src: 01-01-arxiv-2509-16122.md].

**Drone relevance:** miniature ToF arrays have been used on nano/micro drones for obstacle avoidance and NanoSLAM (cited as prior work in Sifferman et al.) [src: 01-01-arxiv-2509-16122.md]. The self-detection problem is structurally analogous to a drone gripper/arm occluding the sensor FOV during approach.

### Stereo depth cameras for table-top grasping (Rustler et al., arXiv 2501.07421)

For table-top manipulation tasks at ≤1 m range, the **D435 is the recommended camera** — best price/performance at close range, sub-1 cm error below 100 cm, and the most commonly used camera in the robot-manipulation literature [src: 02-02-arxiv-2501-07421.md].

ZED 2 is the overall best camera across all distances but requires a CUDA GPU — a weight and power penalty incompatible with the [[payload-budget]] constraints of a small drone. Its passive stereo also degrades in low light, which matters for indoor flying [src: 02-02-arxiv-2501-07421.md].

D455 excels at flat-surface estimation (its wider baseline helps planes) but performs *worse* than D435 on complex curved objects at close range — relevant for grasping irregular household items [src: 02-02-arxiv-2501-07421.md]. The D455's minimum ideal range of 0.6 m means it may not image objects in the final 60 cm of gripper approach.

OAK-D Pro's quantised depth layers make it unsuitable for complex household objects, though its on-board AI modules (object detection, keypoint detection) could be useful for coarser-grained tasks [src: 02-02-arxiv-2501-07421.md].

### Transparent and specular surface depth failure (Wei et al., D3RoMa, arXiv 2409.14365)

Standard stereo depth cameras — including D435, D415, L515 — fail catastrophically on transparent (glass bottles, cups) and specular (stainless steel, porcelain) surfaces. RGB pixel values from foreground and background blend through transparent objects; SGM and standard stereo matching have no mechanism to handle this. The failure mode is not degraded accuracy — it is missing or wildly wrong depth for the entire object [src: 12-07-d3roma-depth-sensing-2409.14365.md].

**D3RoMa method:** reformulates stereo depth estimation as image-to-image translation using a denoising diffusion model (DDPM). The model takes a raw disparity map (from SGM or sensor) + stereo pair as input; iterative denoising produces a clean disparity map guided by photometric consistency loss (SSIM + edge-aware smoothness). Trained on HISS, a synthetic dataset of 10,000+ stereo pairs with 350+ transparent/specular/diffuse objects rendered in Isaac Sim with realistic IR pattern simulation [src: 12-07-d3roma-depth-sensing-2409.14365.md].

**Results (real tabletop grasping):**

| Object class | Raw depth | Baseline (ASGrasp) | D3RoMa |
|---|---|---|---|
| Transparent | 25% | 43% | **63%** |
| Specular | 33% | 63% | **83%** |
| Diffuse | 70% | 50% | 78% |
| **Overall** | 45% | 50% | **77%** |

Mobile manipulation (Franka 7-DOF, real home): D3RoMa 0.80–1.00 across material types vs raw 0.22–0.67 [src: 12-07-d3roma-depth-sensing-2409.14365.md].

**Limitation:** inference is 3.19 s at 640×360 with 10 diffusion steps — orders of magnitude slower than 10–40 ms for classical stereo. Acknowledged by authors; accelerated samplers suggested as mitigation but not solved [src: 12-07-d3roma-depth-sensing-2409.14365.md].

**Implication for household manipulation:** transparent drinking glasses, clear storage bins, shiny ceramic mugs, and reflective kitchen items are common household objects. A manipulation system relying solely on raw stereo depth will fail on a significant fraction of the target object set. D3RoMa is a drop-in depth replacement — no gripper or sensor modification — but its latency makes it unsuitable for real-time closed-loop use today. Near-term path: use D3RoMa for grasp pose estimation (one-shot per object, not per-frame), then switch to lightweight tracking.

### ToF camera noise characterisation for sim-to-real RL (Cai et al., arXiv 2412.15040)

The PMD Flexx2 noise model (§Quantitative benchmarks) was developed specifically to reduce the sim-to-real gap for exteroceptive RL controllers on a quadrupedal robot (Unitree Go1). The camera was validated in a mobile-robot proximity context, not manipulation, but the noise models are directly applicable to any legged or aerial robot carrying the sensor [src: 03-03-arxiv-2412-15040.md].

The paper explicitly contrasts ToF with stereo: "ToF cameras… offer multiple benefits over classic stereo-based depth cameras" — referencing accuracy at mid-range, lighting independence, and not requiring baseline-dependent depth computation [src: 03-03-arxiv-2412-15040.md].

The Flexx2's 570–680 mW power draw is higher than the AMS TMF8820 (<10 mW per measurement) but far lower than any LiDAR, and its 13 g weight is compatible with a lightweight manipulator arm [src: 03-03-arxiv-2412-15040.md].

---

## Comparison to wide-FOV LiDAR

*(synthesis)*

The [[lidar-for-uav-autonomy]] page documents the Livox MID360's strengths for SLAM: wide FOV (~360°×59°), 40 m range, ~200,000 pt/s, LiDAR-inertial odometry integration (FAST-LIO2). But for close-range object pose estimation these strengths become weaknesses:

1. **Point density at close range is sparse for small objects.** The MID360's non-repetitive scan pattern distributes points over the full FOV; a 10 cm household object at 0.5 m receives only a few tens of points per scan cycle, far too sparse for reliable grasp pose estimation without temporal accumulation that creates latency.

2. **Wide FOV is a liability near a gripper.** At approach distance, the drone body, arm, and gripper fill a large fraction of the scan; filtering the robot's own structure (the same self-detection problem as miniature ToF) is complex on sparse point clouds.

3. **Dense depth cameras give a 2D image.** A 224×172 ToF frame or a 1280×720 stereo depth map can be processed by standard 6-DoF grasp pose networks (GraspNet, FoundationPose, AnyGrasp) without the point-cloud preprocessing step required for LiDAR. See [[onboard-grasp-perception]].

For SLAM and navigation (the MID360's actual job), the wide FOV and long range are correct. For the gripper-approach phase (the final 0.5–2 m), a dedicated close-range depth sensor is the right complement — not a replacement.

---

## Implications for the prototype

*(synthesis)*

The form factor has shifted from aerial-primary to **ground-primary robot arm** (see [[home-tidy-drone-prototype]] and [[system-architecture]]). This changes sensor constraints significantly: weight ceiling is lifted, two cameras are standard practice, and ZED 2 (previously ruled out for drone use due to CUDA GPU requirement) is now viable.

### Ground robot + arm — two-camera architecture

A ground manipulator uses two cameras for two distinct jobs:

| Role | Sensor | Range used | Rationale |
|------|--------|------------|-----------|
| **Navigation / SLAM** | Livox MID360 (preferred) or D435i | 0.5–10 m | Wide FOV, robust indoor SLAM; handles room-scale geometry |
| **Arm / wrist manipulation** | **D405** (preferred) or OAK-D SR | 0.07–0.5 m | Purpose-built for the grasp-approach envelope; D435 bottoms out at 30 cm |

The D405 is the correct manipulation camera for a ground robot arm. It covers 7–50 cm with 0.1 mm detection at 7 cm — exactly the approach envelope where D435 is unreliable and D455 is completely blind. The OAK-D SR ($199) is the budget alternative with built-in neural inference; its 20 cm minimum range excludes the final 13 cm the D405 covers but its onboard RVC2 can run object detection without a host GPU [src: 02-04-oak-d-sr-docs-luxonis.md, 04-03-d405-realsenseai-product.md].

### Transparent/specular surface risk

Standard stereo depth fails on a significant subset of household objects (glasses, stainless steel mugs, shiny ceramics). The D3RoMa method improves transparent grasp success from 25% to 63% and specular from 33% to 83%, but at 3.19 s per inference — only viable for one-shot grasp pose estimation, not real-time tracking [src: 12-07-d3roma-depth-sensing-2409.14365.md]. Budget a failure rate for transparent/specular objects in Phase-1 unless D3RoMa depth inference is added to the grasp pipeline.

### Drone (aerial) path — unchanged

For any aerial phase, the original recommendation stands: D435 for manipulation perception + miniature ToF array (AMS TMF8820, VL53L5CX) for proximity/collision avoidance in the final 30 cm approach [src: 01-01-arxiv-2509-16122.md]. ZED 2 remains ruled out for aerial use (CUDA GPU, 175 g).

### Sim-to-real RL

If RL locomotion or grasp control uses simulated depth input, the PMD Flexx2 noise model [src: 03-03-arxiv-2412-15040.md] is directly applicable. The Flexx2's 0.1–2.4 m Mode 5 range and characterised Gaussian noise model reduce the sim-to-real gap for exteroceptive controllers.

---

## Source

Raw files in `raw/research/close-range-depth-sensors/`:

- `01-01-arxiv-2509-16122.md` — Sifferman, Gupta, Gleicher. "Efficient Detection of Objects Near a Robot Manipulator via Miniature Time-of-Flight Sensors." arXiv:2509.16122. Accepted IEEE RA-L, September 2025.
- `02-02-arxiv-2501-07421.md` — Rustler, Volprecht, Hoffmann. "Empirical Comparison of Four Stereoscopic Depth Sensing Cameras for Robotics Applications." arXiv:2501.07421 / IEEE Access, April 2025.
- `03-03-arxiv-2412-15040.md` — Cai, Plozza, Marty, Joseph, Magno (ETH Zurich). "Noise Analysis and Modeling of the PMD Flexx2 Depth Camera for Robotic Applications." arXiv:2412.15040. IEEE, 2024.
- `04-st-vl53l5cx-datasheet` — **capture failed** (ST.com timeout). VL53L5CX specs referenced indirectly via cross-citations in the Sifferman paper.

Raw files in `raw/research/arm-cameras/`:

- `04-03-d405-realsenseai-product.md` — Intel RealSense D405 product page (realsenseai.com). Specs: FOV, range, accuracy, power, dimensions.
- `05-04-d405-qviro-specs.md` — Qviro aggregator specs page for D405. Weight (60 g, unconfirmed primary), application use cases.
- `06-05-d405-digikey-forum.md` — DigiKey forum technical reference. Resolution-dependent Min-Z table (40–100 mm), USB 2.0 streaming limits.
- `07-06-librealsense-github.md` — Intel librealsense SDK 2.0 repository. D405 supported in D400 series; cross-platform wrappers.
- `08-07-d405-announcement-github.md` — Official D405 announcement (Intel RealSense GitHub, March 2022). Range 7–50 cm confirmed.
- `02-04-oak-d-sr-docs-luxonis.md` — Luxonis OAK-D SR official docs (docs.luxonis.com). Specs: range, power, connectivity, onboard AI.
- `03-05-oak-d-sr-docs-hardware.md` — Luxonis OAK-D SR hardware specification sheet. Dimensions, weight, IMU, thermal limits.
- `10-08-oak-d-sr-forum-discussion.md` — Luxonis community launch announcement. Price $199 confirmed; positioning vs OAK-D S2.
- `12-07-d3roma-depth-sensing-2409.14365.md` — Wei, Geng, Chen et al. (PKU/Berkeley/Stanford). "D3RoMa: Disparity Diffusion-based Depth Sensing for Material-Agnostic Robotic Manipulation." arXiv:2409.14365, September 2024. Diffusion-based depth for transparent/specular surfaces; real robot grasping experiments.

---

## Related

- [[drone-sensors-for-autonomy]] — full sensor reference map; where close-range depth sensors fit in the broader stack
- [[lidar-for-uav-autonomy]] — LiDAR classes, SLAM stacks; why MID360 is the nav sensor and why it is not suited to close-range manipulation
- [[onboard-grasp-perception]] — grasp pose estimation pipelines that consume the depth data this page surveys
- [[home-tidy-drone-prototype]] — Phase-1 build plan; currently specifies D455; this page informs the manipulation-perception sensor choice
- [[payload-budget]] — weight and power constraints that gate sensor selection
