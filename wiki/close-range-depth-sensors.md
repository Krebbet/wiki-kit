# Close-Range Depth Sensors for Drone Manipulation Perception

Research question: are there more directed, LiDAR-like sensors that give rich close-up depth readings in a narrower field of view — suited to drone manipulation and grasp pose estimation at 0.5–2 m range, where wide-FOV solid-state LiDAR (Livox MID360) gives too-sparse returns on small objects?

Short answer: yes. Three sensor classes span the space from cm-accurate dense stereo depth to PCB-scale miniature ToF arrays. The right choice depends on whether you need a 2D depth image (for grasp pose), presence/proximity detection near a gripper, or noise models suitable for sim-to-real RL.

---

## Sensor taxonomy

### (a) Stereo depth cameras — active structured-light / passive

Dense RGB-D cameras compute depth by matching features in two shifted images. Active variants (Intel RealSense D435, D455; Luxonis OAK-D Pro) project additional IR points to aid matching in low-texture scenes; passive variants (StereoLabs ZED 2) rely on texture and use neural networks for depth computation.

Key examples and specs (manufacturer-stated) [src: 02-02-arxiv-2501-07421.md]:

| Camera | Stereo tech | Ideal range (m) | Depth FOV | Max depth res | Weight | GPU needed |
|--------|-------------|-----------------|-----------|---------------|--------|------------|
| RealSense D435 | Active | 0.3–3 | 87°×58° | 1280×720 | ~72 g | No |
| RealSense D455 | Active | 0.6–6 | 87°×58° | 1280×720 | ~124 g body | No |
| ZED 2 | Passive | 0.3–20 | 110°×70° | 2208×1242 | ~175 g | Yes (CUDA) |
| OAK-D Pro | Active | 0.8–12 | 80°×55° | 1280×800 | ~97 g body | No |

Prices (at publication, USD): D435 $314, OAK-D Pro $349, D455 $419, ZED 2 $449 [src: 02-02-arxiv-2501-07421.md].

The stereo baseline governs the close-end of the useful range and depth-error growth: depth error grows quadratically with distance for fixed-baseline cameras; ZED 2 breaks this by computing depth via neural network [src: 02-02-arxiv-2501-07421.md].

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

The [[home-tidy-drone-prototype]] Phase-1 build already includes an Intel RealSense D455 as the budget depth path. The Rustler et al. results clarify the D455's limitations:

- **0.6 m minimum range**: the D455 goes blind inside 60 cm. If the gripper approach goes closer than this, a supplementary sensor is needed for the final phase of approach.
- **D455 is worse than D435 on complex curved objects at close range.** For household objects (the target), D435's smaller baseline is an advantage in the 0.3–0.6 m range that D455 cannot cover at all. *(This is a mild conflict with the prototype plan, which chose D455 for its larger ideal range — the two cameras are complementary, not competing, for close-range manipulation.)*
- **ZED 2 ruled out** for drone use: requires CUDA GPU (incompatible with SWaP constraints per [[payload-budget]]).

**Recommended sensor path for close-range manipulation perception:**

1. **Phase-1 bench test (0.5–2 m range):** D435 or D455 for grasp pose inputs. D435 is preferred for complex household object reconstruction at <100 cm; D455 is preferred for navigation depth at 0.6–3 m. Carry both if payload permits, or D455 for navigation + D435 for manipulation perception.

2. **Gripper proximity / collision avoidance (<30 cm):** A miniature ToF array (AMS TMF8820, VL53L5CX, VL53L8CX or similar) mounted near the gripper can handle the close-approach phase where stereo depth becomes unreliable. Requires solving the self-detection problem as documented in Sifferman et al. [src: 01-01-arxiv-2509-16122.md].

3. **If sim-to-real RL is used for locomotion or grasp control:** The PMD Flexx2 noise model [src: 03-03-arxiv-2412-15040.md] is directly applicable. The Flexx2's 0.1–2.4 m Mode 5 range maps to our target zone; its 13 g, 570–680 mW profile is borderline for a small drone but feasible.

**Open question for the user:** does the Phase-1 plan need a second depth camera (D435 for manipulation, D455 for nav), or is a single D455 + miniature ToF array for proximity sufficient?

---

## Source

Raw files in `raw/research/close-range-depth-sensors/`:

- `01-01-arxiv-2509-16122.md` — Sifferman, Gupta, Gleicher. "Efficient Detection of Objects Near a Robot Manipulator via Miniature Time-of-Flight Sensors." arXiv:2509.16122. Accepted IEEE RA-L, September 2025.
- `02-02-arxiv-2501-07421.md` — Rustler, Volprecht, Hoffmann. "Empirical Comparison of Four Stereoscopic Depth Sensing Cameras for Robotics Applications." arXiv:2501.07421 / IEEE Access, April 2025.
- `03-03-arxiv-2412-15040.md` — Cai, Plozza, Marty, Joseph, Magno (ETH Zurich). "Noise Analysis and Modeling of the PMD Flexx2 Depth Camera for Robotic Applications." arXiv:2412.15040. IEEE, 2024.
- `04-st-vl53l5cx-datasheet` — **capture failed** (ST.com timeout). VL53L5CX specs referenced indirectly via cross-citations in the Sifferman paper. Key cross-check: ST also make VL53L8CH (cited directly in Sifferman et al., ref [7]) and VL6180X (ref [43]).

---

## Related

- [[drone-sensors-for-autonomy]] — full sensor reference map; where close-range depth sensors fit in the broader stack
- [[lidar-for-uav-autonomy]] — LiDAR classes, SLAM stacks; why MID360 is the nav sensor and why it is not suited to close-range manipulation
- [[onboard-grasp-perception]] — grasp pose estimation pipelines that consume the depth data this page surveys
- [[home-tidy-drone-prototype]] — Phase-1 build plan; currently specifies D455; this page informs the manipulation-perception sensor choice
- [[payload-budget]] — weight and power constraints that gate sensor selection
