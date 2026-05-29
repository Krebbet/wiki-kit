# Tactile Manipulation

Tactile sensing provides contact-state feedback that [[onboard-grasp-perception|vision alone cannot deliver]]: force magnitude and distribution, slip onset, contact geometry at occluded surfaces, and friction estimation. This page surveys the research landscape — sensors, control methods, sim-to-real infrastructure, and zero-shot generalisation — motivated by the hypothesis that vision + tactile feedback on a gripper is a more reliable path to manipulation than vision alone.

## Source

| File | Paper | Venue / Date |
|---|---|---|
| `01-01-arxiv-2512-01106.md` | Lepora, "Tactile Robotics: Past and Future" | IJRR 2025 (survey) |
| `02-02-arxiv-2501-09468.md` | Donato et al., "Sensorimotor Control Strategies for Tactile Robotics" | Review 2025 |
| `05-03-arxiv-2312-13469.md` | Suresh et al., "NeuralFeels" | Science Robotics 2024 |
| `03-04-arxiv-2411-12503.md` | Li et al., "ManiSkill-ViTac 2025 Challenge" | ICRA 2025 workshop |
| `04-05-arxiv-2510-13324.md` | Helmut et al., "FARM: Tactile-Conditioned Diffusion Policy" | IEEE preprint 2025 |
| `07-06-arxiv-2408-06506.md` | Akinola et al., "TacSL" (NVIDIA) | IEEE T-RO 2025 |
| `06-07-arxiv-2409-12735.md` | Kasolowsky & Bäuml, "Fine Manipulation with Tactile Skin" | IROS 2024 |
| `08-08-arxiv-2601-02778.md` | ByteDance Seed, "Closing the Reality Gap" | Preprint Dec 2025 |

---

## 1. What Tactile Sensing Is

Tactile sensing measures properties of an object through physical contact. It is distinct from — but complementary to — visual sensing, in that it captures contact events that are invisible to a camera (occluded grasp surfaces, interior forces, slip at the fingertip) and is unaffected by poor lighting or object specularity.

The canonical definition from the literature: tactile sensing is "a form of sensing that can measure given properties of an object through physical contact between the sensor and the object" [src: `01-01-arxiv-2512-01106.md`], encompassing contact detection, force distribution, slip, shape, texture, temperature, and stiffness.

### Sensor classes

| Class | Operating principle | Representative product | What it measures |
|---|---|---|---|
| **GelSight-style / optical** | Internal camera views deformation of illuminated gel membrane | GelSight Mini, DIGIT, GelSlim | 3-D contact geometry, normal + shear force distribution (via FEATS or photometric stereo) |
| **Capacitive skin** | Pressure changes capacitance of taxel array | iCub fingertip (12 taxels), Pressure Profile Systems RoboTouch | Normal force spatial distribution |
| **Piezoresistive / FSR** | Force changes resistance | TekScan, Weiss Robotics 78-taxel | Force per taxel; moderate spatial resolution |
| **Barometric / multi-modal** | Impedance change + fluid pressure + vibration + temperature | SynTouch BioTac (19 taxels) | Normal force, vibration, temperature; discontinued ~2024 |
| **Piezoelectric** | Deformation generates charge | PVDF-based skins | Dynamic / vibration events; inherently dynamic (AC only) |
| **Taxel-based "tactile skin"** | Soft material bonded to sensor pad; multi-taxel contact area | TekScan sensor on DLR-Hand II (4×4 taxels) | Per-taxel normal force; sub-taxel precision achievable via model fitting |
| **Binary / proximity** | Digital contact detect + dense virtual array via FK | xHand virtual sensor array (120 per fingertip) | Contact presence + force-weighted contact centroid |
| **F/T wrist sensor** | Strain-gauge six-axis | ATI Mini45, SRI M3813A | Total force + torque at wrist; no spatial distribution |

The GelSight/DIGIT family (optical / vision-based tactile sensors) currently dominates research because their outputs are 2-D images compatible with standard computer vision pipelines [src: `01-01-arxiv-2512-01106.md`; `05-03-arxiv-2312-13469.md`].

Harmon's 1982 observation — "manipulation-related key events are not contained in visual data, specifically the geometric and dynamic reference data for adaptive and soft grasping" — remains apt [src: `01-01-arxiv-2512-01106.md`].

---

## 2. Hardware Landscape

### Named sensors with specifications

| Sensor | Type | Resolution / taxels | Output | Notes |
|---|---|---|---|---|
| **GelSight Mini** | Optical gel | ~320×240 RGB image | RGB tactile image; force via FEATS | GelSight Inc; used in FARM, TacSL, ManiSkill-ViTac. $~650 |
| **DIGIT** | Optical gel | 240×320 RGB, 30 Hz | RGB tactile image | Meta / open-source; used in NeuralFeels |
| **GelSlim 3.0** | Optical gel | High-res | RGB tactile image | MIT; compact finger form-factor |
| **OmniTact** | Optical gel, multi-directional | — | RGB from 5 directions | ICRA 2020; for angled contacts |
| **SoftBubble** | Compliant gel; depth camera | Dense depth | Deformation field | Toyota Research; very compliant |
| **TekScan** (Kasolowsky & Bäuml) | Taxel-based skin | 4×4 taxels, 2.5 mm×2.5 mm per taxel, 4 mm grid | Per-taxel force; 0–255 range | Glued to DLR-Hand II cylindrical fingertip; 14,884 virtual tactile points at 0.25 mm resolution in sim [src: `06-07-arxiv-2409-12735.md`] |
| **BioTac** | Impedance + fluid | 19 taxels + vibration + temp | Multi-modal | SynTouch; discontinued; still cited in older papers [src: `01-01-arxiv-2512-01106.md`] |
| **xHand virtual sensor** | Distance-field tactile | 120 units/fingertip × 5 = 600 total | Contact force + force-weighted centroid per finger | ByteDance Seed; derived from FK distance, no physical sensor required [src: `08-08-arxiv-2601-02778.md`] |
| **SRI M3813A F/T** | Wrist F/T | 6-DoF | Force + torque | ManiSkill-ViTac hardware platform [src: `03-04-arxiv-2411-12503.md`] |

**FEATS** (Finite Element Analysis for Tactile Sensing) is a learning-based model trained on FEA-labeled data that converts GelSight Mini images into spatially-resolved normal and shear force distributions. Used as the observation signal in FARM [src: `04-05-arxiv-2510-13324.md`].

---

## 3. Control Approaches

### 3.1 Reactive / closed-loop force control

Slip detection and grip force adjustment are the foundational use case. The standard architecture maintains contact-force estimates from taxel arrays, detects incipient slip (3–6 timesteps before gross slip), and modulates grip-finger velocity or normal force. Approaches range from PID on force error to fuzzy controllers and impedance control [src: `02-02-arxiv-2501-09468.md`].

Tactile feedback can modulate finger velocity to prevent slippage without requiring prior knowledge of object geometry or friction coefficient [src: `02-02-arxiv-2501-09468.md`].

### 3.2 Tactile servoing

Tactile servoing maintains contact while sliding along a surface. A forward sensor model maps contact state to expected tactile image; the Tactile Jacobian maps the residual between desired and actual tactile images to corrective motion [src: `02-02-arxiv-2501-09468.md`]. This operates at high frequency (by necessity — gross slip can occur in a single sampling interval) and must run from touch, not vision.

### 3.3 Imitation learning with force-based action space (FARM)

FARM (Force-Aware Robotic Manipulation) is a diffusion policy [src: `04-05-arxiv-2510-13324.md`] that jointly predicts:
- Robot end-effector pose
- Target grip width
- **Target grip force** (continuous, not binary)

The policy is conditioned on: in-hand RGB image; grip width; FEATS-derived shear and normal force images (96×96×3); total normal force scalar; gripper pose. Trained from 30 human demonstrations per task, collected with a hand-held UMI gripper equipped with a GelSight Mini. The actuated robot gripper replicates the handheld geometry exactly for zero-retargeting deployment.

**Key results on real Franka Research 3** over 20 rollouts per task [src: `04-05-arxiv-2510-13324.md`]:

| Task | FARM (force dist.) | Force-Aware (scalar) | Tactile-Aware (raw img) | Vision-Only |
|---|---|---|---|---|
| Plant insertion (high-force) | **95%** | 95% | 65% | 85% |
| Grape picking (low-force) | **95%** | 85% | 60% | 0% |
| Screw tightening (dynamic, temporal) | **100%** | 10% | 40% | 0% |

The screw-tightening result is significant: a scalar force signal is insufficient; the spatial force distribution is required to maintain Allen-key alignment during tightening. Vision alone fails entirely because it cannot detect internal torque state.

### 3.4 Contact-rich RL with sim-to-real transfer

Multiple papers train RL policies in simulation using tactile observations and transfer zero-shot:

**TacSL** (Nvidia, [src: `07-06-arxiv-2408-06506.md`]): asymmetric actor-critic + distillation. Critic sees privileged state (contact forces, object pose); actor sees only tactile images + robot state. Peg placement 91.4% success zero-shot on real robot with "Diff+ColorAug" input (difference between current and nominal tactile image). Peg insertion 82.7% zero-shot. Tactile policies are also robust to lighting changes where a wrist camera would degrade [src: `07-06-arxiv-2408-06506.md`].

**TacSkin fine manipulation** (DLR/TUM, [src: `06-07-arxiv-2409-12735.md`]): RL (SAC) in PyBullet with a novel tactile skin model. Marble rolling: tracking error reduced from ~5 mm without tactile to <1 mm with tactile (sub-taxel precision, taxel spacing = 4 mm). Bolt rolling: policy completely fails without tactile feedback; succeeds 11/12 runs with 100% directional accuracy. Zero-shot sim-to-real on DLR-Hand II.

**ByteDance Seed Zero-Shot** ([src: `08-08-arxiv-2601-02778.md`]): force-adaptive grasping on 12-DoF xHand. Force command tracking linear over [0, 1] range. In-hand rotation: 25.1 consecutive 90° successes with full tactile+torque observation vs. 1.1 without any contact sensing. Ablation shows contact force + force-weighted contact centroid are both individually necessary.

### 3.5 MPC and predictive control

Model Predictive Control over video-predicted tactile sequences: a GelSight-based MPC for marble manipulation (predicts next tactile state, plans action sequences over a horizon) was demonstrated at ICRA 2019. DIGIT-based marble manipulation uses a learned forward dynamics model + MPC [src: `02-02-arxiv-2501-09468.md`].

---

## 4. Visuotactile Fusion

### NeuralFeels (Science Robotics 2024) [src: `05-03-arxiv-2312-13469.md`]

Hardware: Allegro hand + 4 DIGIT sensors (one per finger) + Intel D435 RGB-D camera.

**What it does**: Online neural SLAM — builds a neural signed-distance field (SDF) of an unknown in-hand object while simultaneously tracking its pose. Vision provides global context; touch fills in occluded surfaces and refines estimates.

**Key quantitative results** (70 experiments, 350 seeds):
- Final reconstruction F-score: **81%** (novel objects)
- Average pose drift: **4.7 mm** (novel objects), **2.3 mm** (known CAD)
- Multimodal vs. vision-only: **+15.3%** reconstruction (sim), **+14.6%** (real), **+21.3%** pose tracking (sim), **+26.6%** (real)
- Under heavy occlusion: **up to 94.1% improvement** in pose tracking at worst-case camera viewpoints
- Tactile transformer depth prediction error: **0.042 mm** on simulated test set

The key insight: touch is "local vision" — it can be modelled as a perspective camera with a centimeter-scale field of view [src: `05-03-arxiv-2312-13469.md`]. Under occlusion (the gripper blocking the camera), touch becomes the dominant signal.

### ManiSkill-ViTac 2025 [src: `03-04-arxiv-2411-12503.md`]

Challenge platform: Dual GelSight Mini + Intel RealSense D415 + Robotiq Hand-E gripper + SRI 6-DoF F/T. Simulation in SAPIEN using Incremental Potential Contact (IPC) for FEM-accurate elastomer deformation. Tasks: peg insertion (3 shape pairs), lock opening (4 key/lock pairs). Reference policy: TD3 with Shared Weight Encoder over marker flow + relative motion. Track 2 adds vision (RGB, depth, point cloud) to the tactile observations.

The challenge represents the first open benchmark with standardised real-hardware evaluation for visuotactile manipulation.

---

## 5. Sim-to-Real

Sim-to-real for tactile is substantially harder than for cameras because the sensor involves contact mechanics (elastomer deformation), illumination (GelSight), and sensor-to-sensor manufacturing variation.

### TacSL approach [src: `07-06-arxiv-2408-06506.md`]

**Speed**: 200× faster than Taxim (CPU baseline) for tactile image generation; 428× faster for force field generation (10×10 taxels, 32768 parallel envs at 1.54M FPS). Runs inside NVIDIA Isaac Simulator with full GPU parallelisation.

**Transfer techniques**:
1. Soft-contact parameter randomisation (stiffness κ ∈ [150–350])
2. Spatial image augmentation (translation + zoom)
3. Color randomisation (brightness, contrast, saturation, hue)
4. "Diff" input: difference between current and nominal tactile image beats raw RGB

**Novel algorithm**: AACD (Asymmetric Actor-Critic Distillation) — a pretrained low-dimensional critic accelerates RL with high-dimensional image inputs; needed when standard AAC fails to learn with full image augmentation.

### TacSkin sim model [src: `06-07-arxiv-2409-12735.md`]

Decouples physics from tactile response. A rigid-body simulator provides contact normal and force; a ray-cast equilibrium model then computes correct penetration depth that satisfies force balance. Avoids the "sudden jump" artifact of other methods. Self-contained calibration uses only the robot's own joints and torque sensors — no external test bench.

### ByteDance Seed approach [src: `08-08-arxiv-2601-02778.md`]

For hands without physical torque sensors (most commodity hands): a one-time current-to-torque calibration maps motor current linearly to equivalent simulated torque, bridging the actuation gap without expensive joint-level sensors. Actuator model includes backlash, torque-speed saturation, and randomised friction.

### TACTO simulator [src: `05-03-arxiv-2312-13469.md`]

TACTO (Meta AI) simulates DIGIT and GelSight by compositing real-world template images with rendered depth. Used in NeuralFeels; can simulate contacts on arbitrary YCB objects. Tactile transformer trained entirely in TACTO achieves 0.042 mm depth prediction error and transfers to real DIGIT sensors.

### ManiSkill-ViTac simulation [src: `03-04-arxiv-2411-12503.md`]

FEM-based elastomer deformation (IPC method) — intersection-free, inversion-free, supports Neo-Hookean hyperelastic material. Higher fidelity than rigid-body approximations; smaller sim-to-real gap claimed for the challenge tasks.

---

## 6. Zero-Shot / Unknown Objects

The central question for deployment is: does tactile help when the object is not in any training set?

**NeuralFeels** explicitly evaluates on novel objects (no prior shape). Reconstruction F-score 81%, pose drift 4.7 mm — achieved without category priors [src: `05-03-arxiv-2312-13469.md`]. Touch fills in occluded geometry that vision cannot observe.

**FARM** demonstrates grape picking (0% vision-only → 95% FARM). The grape is a novel deformable object not pre-catalogued; the force distribution captures the compliance interaction [src: `04-05-arxiv-2510-13324.md`].

**ByteDance Seed** shows force-adaptive grasping of irregularly shaped objects **not seen during training** (gamepad, bowl with complex geometry). The policy generalised from a training set of standard geometric objects to these unseen shapes via domain randomisation over friction, mass, and shape [src: `08-08-arxiv-2601-02778.md`].

**TacSL** peg insertion 82.7% zero-shot; peg-in-gripper pose/orientation randomised (±π/12 rotation, ±12.5 mm position) — this is partially unknown-object territory in the sense that the exact contact state is unknown at grasp time [src: `07-06-arxiv-2408-06506.md`].

**Key limitation noted in NeuralFeels**: tactile-only tracking performs poorly without global visual context; touch disambiguates vision but does not replace it [src: `05-03-arxiv-2312-13469.md`].

**Donato et al. review** [src: `02-02-arxiv-2501-09468.md`] gives a framework: for objects with unknown geometry and unknown physical properties ("unknown object"), the full sensorisation table prescribes proximity + contact + force + slip + texture/stiffness sensors. For unknown objects, online friction estimation (not fixed offline coefficient) is required.

---

## 7. Maturity Summary Table

| Capability | Maturity | Source |
|---|---|---|
| Slip detection and grip force adjustment | **demoed** (well-established, many papers) | `02-02-arxiv-2501-09468.md` |
| GelSight / DIGIT sensor hardware | **shipping** (~$650–$900) | `04-05-arxiv-2510-13324.md`, `05-03-arxiv-2312-13469.md` |
| Force distribution estimation from GelSight (FEATS) | **demoed** (open-source) | `04-05-arxiv-2510-13324.md` |
| Diffusion policy with explicit force action space (FARM) | **demoed** (3 real tasks, 20 trials each) | `04-05-arxiv-2510-13324.md` |
| Visuotactile SLAM for novel in-hand objects (NeuralFeels) | **demoed** (70 real trials) | `05-03-arxiv-2312-13469.md` |
| Zero-shot sim-to-real peg insertion with tactile (TacSL) | **demoed** (82.7% on real Franka) | `07-06-arxiv-2408-06506.md` |
| Fine manipulation (marble/bolt) learned in sim, zero-shot transfer | **demoed** (DLR-Hand II, IROS 2024) | `06-07-arxiv-2409-12735.md` |
| Force-adaptive grasping of unknown objects, zero-shot 5-finger hand | **demoed** (Dec 2025, ByteDance xHand) | `08-08-arxiv-2601-02778.md` |
| Tactile simulation (TacSL) at RL-training speed | **shipping** (open-source, Isaac Simulator) | `07-06-arxiv-2408-06506.md` |
| Open challenge benchmark (ManiSkill-ViTac 2025) | **demoed** (ICRA 2025 workshop) | `03-04-arxiv-2411-12503.md` |
| Tactile on an aerial platform | **absent** from the literature | — |

---

## 8. Relevance to Aerial Manipulation

*[Synthesis — editorial label]*

The papers surveyed here are ground-robot and arm results. None involve aerial vehicles. The transfer analysis below applies the [[system-architecture|land-then-grasp preferred]] principle from the drone architecture.

### What transfers directly

**Land-then-grasp changes the problem in the drone's favour.** Once the drone has landed and the arm is deployed, the manipulation problem is essentially the same as a ground robot's: a fixed-base (or compliant-base) arm interacting with a household object. All the RL policies, diffusion policies, and sim-to-real recipes from these papers apply without modification to the landed configuration.

Specifically:
- **FARM** (diffusion policy + GelSight Mini + FEATS) requires only a gripper with one GelSight Mini sensor and a wrist camera. This is directly integrable into a [[aerial-grasping|lightweight gripper design]]. At 30 Hz sensing and ~50 Hz control, latency is compatible with a brief landed-grasp episode.
- **TacSL** sim-to-real recipes (soft-contact parameter randomisation, image augmentation, AACD algorithm) are tool-agnostic and directly applicable to training a drone-gripper policy.
- **Slip detection and friction estimation** (Donato et al. review) directly solves the "known-objects-only" limitation noted in [[onboard-grasp-perception]]. An unknown object can be grasped if the gripper can detect and react to incipient slip, without a pre-trained object category model.
- **NeuralFeels visuotactile SLAM** addresses the core finding in [[onboard-grasp-perception]]: aerial OVD achieves only ~28% F1 at aerial viewpoints, and all onboard graspers are category-specific. Touch fills in contact geometry that the aerial camera cannot see during the close-approach phase.

### What is harder in the drone context

1. **Weight and size budget.** GelSight Mini is ~25 g and ~30×20×15 mm. This is compatible with a lightweight gripper, but a full Allegro-hand-style multi-fingered system (as used in NeuralFeels) is not feasible at sub-250 g total payload. **Recommendation**: single-sensor two-finger gripper with one GelSight Mini on one jaw (as in FARM).

2. **Wiring and interface.** GelSight Mini uses USB. A drone gripper needs a compact, vibration-tolerant connection to onboard compute.

3. **Vibration during flight.** Tactile sensors calibrated at rest will drift if the drone vibrates during approach. The landed configuration eliminates this problem entirely — another argument for land-then-grasp.

4. **In-flight tactile.** The ByteDance Seed paper's in-hand rotation results (25.1 consecutive successes) apply to a static base. A drone hovering while grasping would need to decouple gripper forces from aerodynamic disturbances — an unsolved problem in the aerial-grasping literature. The [[aerial-grasping]] page notes all current systems are sub-250 g payload and category-specific; none have tactile.

### Recommended architecture for a Phase-2 prototype

*(Synthesis: not from sources)*

Land → settle (0.5 s for vibration decay) → contact approach guided by [[close-range-depth-sensors|D435 depth]] → close gripper → GelSight Mini activates → FARM-style diffusion policy controls grip force closed-loop → lift. The tactile policy needs no knowledge of the object class, only shape (from NeuralFeels-style online reconstruction) and force feedback.

The key open question the wiki cannot currently answer: **Can a GelSight Mini survive repeated drone takeoffs/landings without gel degradation?** Gel wear under vibration is documented as a sensor lifespan concern [src: `07-06-arxiv-2408-06506.md`] but no UAV-specific test exists.

---

## Related

- [[onboard-grasp-perception]] — vision-only baseline; the gap this page addresses
- [[aerial-grasping]] — drone-specific grasping mechanisms and payload budgets
- [[close-range-depth-sensors]] — sensor benchmarks at grasp range; D435 recommended
- [[system-architecture]] — full drone stack; land-then-grasp preferred in ACTIONS EXECUTION section
- [[home-tidy-drone-prototype]] — prototype plan where tactile sensing is a Phase-2 capability candidate
