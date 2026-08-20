# Robot Arm Prototype Roadmap

Four-stage progression from a stationary workstation demo to a production-feasible drone-mounted arm. Synthesised from [[affordable-robot-arms]], [[onboard-grasp-perception]], [[tactile-manipulation]], [[close-range-depth-sensors]], [[aerial-manipulation]], and [[home-tidy-drone-prototype]].

**Goal:** Demonstrate pick-and-place of household objects, starting with known objects in a controlled workstation environment, ending with a drone-mounted arm and a review of production feasibility.

---

## Stage readiness summary

| Stage | Readiness | Primary blocker |
|---|---|---|
| **1 — Workstation, known objects, controlled** | **Start now** | Arm + sensor hardware acquisition; demo dataset collection |
| **2 — World-model integration (known objects from scene graph)** | After rover world model is operational | Software bridge: object fingerprint memory → arm goal generator |
| **3 — Drone-mounted arm** | Research lab demo: 1–2 yr; consumer-grade: 5–10+ yr | Aerial OVD F1 ~28%; payload ceiling ~150–450 g; all indoor demos mocap-gated |
| **4 — Production feasibility review** | After Stage 1 validates the unit | STS3215 servo fragility; per-unit assembly cost; no sensor miniaturisation for aerial yet |

---

## Stage 1 — Workstation pick-and-place

Operate an arm from a workstation to pick up known objects and drop them into labelled boxes. This is the minimal demo that closes the pick-and-place loop and generates training data for subsequent stages. See [[arm-starter-cost]] for the full cost breakdown with verified BOMs.

### Cost reality check

**Minimum viable Stage 1:** ~$630–880 (SO-ARM101 pair + webcam + existing laptop). **Validated Stage 1:** ~$1,664–2,464 (AhaRobot + D435 + D405). The full cost breakdown and comparison against ALOHA 2 ($20–27k) and TidyBot++ ($13–24k) is at [[arm-starter-cost]].

### Recommended arm

See [[affordable-robot-arms]] for the full comparison table.

**AhaRobot ($1,000–$1,800)** is the most validated open-source option: 7–10/10 success across six manipulation task categories (50–200 demos per task), ROS 2 Humble throughout, open-source CAD + code, 1.5 kg payload per arm, 0.7 mm repeatability, bimanual with floor-to-counter reach [src: affordable-robot-arms]. Bimanual is overkill for Stage 1 box-sorting, but the ROS 2 integration and validation record are the best in the sub-$2k tier.

**SO-ARM101 leader+follower pair ($600–1,000 BOM)** is the cheapest path to data collection for imitation learning — identical hardware for teleoperation and execution within the LeRobot/ACT ecosystem [src: affordable-robot-arms]. Payload ceiling ~100–150 g; suitable for lightweight household objects only.

**Cutting the Cord XLeRobot ($1,202 total):** if you want the arm to eventually be untethered, this build integrates a Jetson Orin Nano Super ($249) into the XLeRobot chassis, achieving 17 DoF, 1.0 kg/arm payload, ACT at 27.8 Hz, 98.7% pick-and-place success on 75 trials [src: arm-starter-cost]. The extra ~$400 over a bare SO-ARM101 pair buys the onboard GPU compute needed for Stage 2+.

**xArm 5 Lite ($4,500) or xArm 6 ($8,000)** for higher repeatability and payload if Stage 2 integration requires reliable deployment without per-session retraining. Metal gearboxes vs the STS3215 plastic gears that limit sub-$2k arms. See [[affordable-robot-arms]] for the mechanical bottleneck analysis.

### Compute requirements — the SmolVLA shift

As of mid-2025, the training and inference compute floor dropped significantly [src: arm-starter-cost]:

- **Training:** ACT trains in ~2–4 hours on a single RTX 3090 (50 demos). SmolVLA (450M) trains on any consumer GPU and is ~40% faster to train than π0; total project compute ~30k GPU hours for pretraining (single-GPU fine-tuning is feasible) [src: arm-starter-cost].
- **Inference:** SmolVLA deploys on CPU or any consumer-grade GPU (runs on MacBook). On Jetson Orin Nano: ACT 27.8 Hz (real-time), SmolVLA 1.4 Hz (adequate for controlled tabletop tasks) [src: arm-starter-cost].
- **Implication:** TidyBot++'s external-RTX-4080-laptop requirement is no longer structural. A laptop with any RTX GPU (3060+) or even CPU inference is sufficient for Stage 1.

### Visual systems

| Role | Sensor | Range | Note |
|---|---|---|---|
| **Close-approach / grasp** | **D405** (~$350) | 7–50 cm | Arm-manipulation specialist; 0.1 mm object detection at 7 cm; D435 minimum range (30 cm) misses the final approach envelope [src: close-range-depth-sensors] |
| **Scene / wider context** | **D435** ($314) or **OAK-D SR** ($199) | 0.3–3 m | Sub-1 cm error at ≤1 m on household objects; OAK-D SR adds 4 TOPS onboard inference; D435 best for complex curved shapes at close range [src: close-range-depth-sensors] |
| **Minimum (prove loop only)** | USB webcam (~$30–80) | 0.3–3 m | For Stage 1 known objects where grasp-pose precision isn't yet the bottleneck; upgrade to D405 when needed |
| **Transparent/specular fallback** | **D3RoMa** post-processing on D435 output | — | Improves transparent grasp rate 25%→63%, specular 33%→83%; 3.19 s per inference = one-shot grasp-pose estimation only [src: close-range-depth-sensors] |

Two-camera architecture is standard practice for ground-robot manipulation: navigation/SLAM sensor handles room-scale geometry; wrist/eye-in-hand camera handles the 7–50 cm approach envelope.

### Detection and grasp models

| Function | Model | Notes |
|---|---|---|
| Object detection | **GDINO + SAM** (server GPU) or **YOLO-World-v2 TensorRT** (Orin NX, 22.9 ms) | For Stage 1 controlled objects: YOLO fine-tuned on your specific object set avoids the aerial-OVD gap entirely; zero-shot OVD best-case aerial F1 is ~28% [src: onboard-grasp-perception] |
| Grasp pose estimation | **AnyGrasp / GraspNet-1B / FoundationPose** | All consume depth images from D405/D435; no LiDAR preprocessing |
| Policy / control | **ACT** or **SmolVLA** via LeRobot | ACT: 30–50 demos, 7–10/10 on AhaRobot [src: affordable-robot-arms]; SmolVLA: 450M, CPU-deployable, 90% in-distribution on SO-101 [src: arm-starter-cost] |
| Transparent objects | **D3RoMa** one-shot depth pass | Budget a ~20–30% failure rate on glass/ceramic objects without it |

### Auxiliary sensor systems

| Sensor | Purpose | When to add |
|---|---|---|
| **Sensorless current readback** (STS3215 `Present_Current` register) | Grip-force proxy, zero additional hardware; Nori Bot approach — 0 servo burn-outs over 4 weeks [src: affordable-robot-arms] | Built-in to STS3215 arms; enable immediately |
| **GelSight Mini / DIGIT** (~$650–900) | Tactile feedback for deformable/unknown objects; FARM diffusion policy: 0%→95% on grape picking vs vision-only [src: tactile-manipulation] | Phase 2 upgrade if Stage 1 shows grip failures on soft or irregular objects |
| **F/T wrist sensor** (ATI Mini45) | Object weight estimation for unknown-mass payloads | Skip for Stage 1 known objects; add for Stage 2 world-model-driven operation |

---

## Stage 2 — World model integration

The scene graph / object fingerprint memory pipeline ([[world-model-architecture]], [[object-fingerprint-memory]]) tracks known objects' positions in the home. Stage 2 connects this to the arm: the world model says "cup is at pose X"; the arm's task planner converts that into an approach trajectory.

**Prerequisites:**
- Rover world model validated (object registry operational with DINOv2 re-ID fingerprinting)
- Stage 1 arm pick-and-place closed-loop working
- Software bridge: pose in world-frame → arm goal pose → ACT/policy execution

**No new hardware required for Stage 2.** The camera stack from Stage 1 is sufficient for the close-approach phase; the world model provides coarse pose to begin from.

---

## Stage 3 — Drone-mounted arm

The mechanics of drone manipulation are solved in the lab. The blockers to anything beyond a mocap-gated demo are well-quantified ([[aerial-manipulation]], [[onboard-grasp-perception]]):

1. **Onboard semantic perception is the binding blocker.** Every indoor drone manipulation demo with object-level tasks uses external motion-capture for target localisation. Best onboard-only result: ETH Osprey, 85% success / 144 trials, but requires operator click-to-select target before flight. No published system autonomously selects and grasps arbitrary household objects from onboard vision alone [src: onboard-grasp-perception].
2. **Payload ceiling ~150–450 g.** Demonstrated ceilings: ~150 g (vision-only soft grasp), ~217 g (pneumatic in-flight, mocap-bound), ~450 g (HI-ARM multi-task, mocap-bound) [src: aerial-manipulation, aerial-grasping].
3. **Aerial OVD F1 ~28%.** Best zero-shot aerial object detector (OWLv2) achieves 27.6% F1 on the LAE-80C benchmark; semantic confusion, not visual localization, is the root cause [src: onboard-grasp-perception].

**Stage 3 achievable lab path** (fiducials-first, matching rover V1 de-risking strategy):
- Fiducial-tagged objects at known poses — eliminates OVD gap
- Operator-click-to-grasp (Osprey pattern) — eliminates autonomous selection gap
- Land-then-grasp preferred over in-flight grasping: vibration-free contact, no aerodynamic disturbance during grasp, tactile sensing (if added) calibrated correctly [src: tactile-manipulation]
- Lightweight wrist camera (D405 / OAK-D SR at 60–72 g) for close-approach depth

---

## Stage 4 — Production feasibility

[[affordable-robot-arms]] documents the mechanical ceiling: all sub-$2k arms use **Feetech STS3215 servos** (plastic gears, 1:345 reduction, ~35 N·cm holding torque). This servo is the bottleneck for production use — fragility under high-torque cycling, limited payload headroom, no factory-level encoder. Moving above $3k brings metal gearboxes and closed-loop control.

The Forte arm ($212/unit at batch of 25) shows that NEMA 17/23 steppers + capstan drives achieve 0.467 mm repeatability and 0.63 kg payload at low unit cost [src: affordable-robot-arms]. It demonstrates the build-vs-buy tradeoff is real once batch scaling enters the picture, though it requires a 3D printer and has no encoder feedback.

The wiki does not yet cover production engineering for custom arm designs. Stage 4 analysis needs a dedicated research run on actuator options (BLDC + harmonic drive vs stepper + capstan vs servo) and per-unit cost at 100–1,000 units.

---

## Source

This page is a synthesis from:
- [[affordable-robot-arms]] — arm tier landscape, AhaRobot/SO-ARM/Forte specs and success rates
- [[onboard-grasp-perception]] — OVD aerial domain gap (F1 ~28%), ETH Osprey onboard grasp result
- [[tactile-manipulation]] — FARM diffusion policy, GelSight Mini, zero-shot unknown-object grasping
- [[close-range-depth-sensors]] — D405/D435/OAK-D SR specs and benchmarks; D3RoMa transparent objects
- [[aerial-manipulation]] — drone manipulation maturity map, payload/endurance/mocap blockers
- [[home-tidy-drone-prototype]] — Phase 1 rover pivot, fiducials-first staging principle

## Related

- [[affordable-robot-arms]] — full arm comparison table and tier analysis
- [[onboard-grasp-perception]] — vision systems for manipulation; the OVD blocker
- [[tactile-manipulation]] — tactile sensing upgrade path
- [[close-range-depth-sensors]] — wrist/eye-in-hand camera selection
- [[aerial-manipulation]] — drone-mounted arm context and maturity map
- [[aerial-grasping]] — drone gripper mechanisms and payload budgets
- [[home-tidy-drone-prototype]] — parent build plan
- [[world-model-architecture]] — Stage 2 world-model integration prerequisite
