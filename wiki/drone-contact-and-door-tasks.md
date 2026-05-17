# Drone Contact and Door Tasks

Physics of door-opening, object transport, and surface-pressing by drones is demonstrated in lab settings across multiple platforms. All indoor demos rely on external motion-capture for object/environment pose; onboard semantic perception remains the deployment blocker. Consumer-ready autonomous contact tasks are 5–10+ years out; teleoperation is the realistic near-term path.

---

## Door Opening

Three distinct approaches have been demonstrated, none deployable without lab infrastructure:

**ETH ASL — RL-trained omnidirectional MAV with hook** [^04]

ETH ASL (Siegwart group) is a distinct lab from [[eth-rpg-scaramuzza]] (ETH RPG, Scaramuzza); conflating them is a common error.

An omnidirectional fully-actuated MAV with a rigid hooked stick was trained via PPO (RL) and benchmarked against MPPI to open a cabinet door. Key numbers:

- RL: 100% success at hook distances 0–1.4 m, completes in <10 s, tolerates ±9 cm handle-observation error, runs at 200 Hz onboard. [^04]
- MPPI: degrades with hook distance, takes 20–45 s, fails at larger distances. [^04]
- Sim→real: zero-shot achieves partial opening (~0.4 rad); full 90° requires action-saturation retraining. Zero-shot door-closing behavior emerged without explicit training. [^04]
- Pose: motion-capture only — no onboard perception. [^04]
- Gaps: hook-in-loop handle only (no lever or knob), no nav-to-door, OMAV is a ~$50k research prototype. [^04]

**HI-ARM — 5-DOF tendon gripper quadrotor** [^09]

556 g quadrotor with a single-actuator tendon-driven hand (palm-grasp and fingertip-pinch modes):

- Door-opening: grasps handle, pushes ~30° with handle constraint, ~55° without; peak force 8.2 N. [^09]
- Autonomy: dual-mode (autonomous task-planner + teleoperation); onboard Radxa ZERO + ArduPilot. [^09]
- Indoor object-pose via motion-capture; outdoor uses RealSense T261 for ego-pose only. [^09]
- Single door type demonstrated; no force feedback (fragile-object handling unproven). [^09]

**FlyCroTug — cooperative teleop, no AI** [^10]

Two palm-size drones open a door cooperatively (Stanford BDML / EPFL, Science Robotics 2018):

- One anchors to glass via gecko adhesive and grips the handle; the other hooks under the door anchored to carpet via microspines. [^10]
- Drones tug 40× their body mass when anchored, vs ~5× in free flight. [^10]
- 5-minute demonstrated flight; fully teleoperated — no AI or autonomy. [^10]
- Authors explicitly argue teleop + low-level autonomy is the realistic near-term path. [^10]

See [[cooperative-aerial-manipulation]] for the anchoring-force mechanics.

---

## Object Transport

HI-ARM provides the broadest consumer task set in the corpus, all lab-demonstrated: [^09]

- Palm-grasp transport: 153 g bottle at 1.1 m/s. [^09]
- Fingertip-pinch: objects <1 g (napkin), <3 cm positional error. [^09]
- Multi-task household sequence: box (75 g) → bottle (134 g) → snack (60 g) → perch, <2 cm tracking error throughout. [^09]
- Cross-river transport and teleop retrieval for a mobility-impaired user: 46.2 m range, 256 ms latency. [^09]
- Outdoor perching: motors near-zero power during perch vs ~160 W hover, relevant to [[drone-power-budget]]. [^09]

Honest caveat: all indoor grasping tasks relied on external motion-capture for object pose. The platform carries no onboard semantic perception. See [[drone-sensors-for-autonomy]] for the sensor gap.

See [[aerial-grasping]] for gripper taxonomy and payload physics.

---

## Surface Contact / Pressing

**Bumper Drone — embodied compliant contact** [^06]

700 g quadrotor with 3D-printed TPU compliant horns (mass-spring-damper geometry) enables wall-contact without crashing:

- Passively absorbs collisions; sustains wall-pushing at ~15° pitch with a standard PID controller only. [^06]
- Pitch oscillation reduced 38% (elastic vs rigid horns); peak force ~5 N per horn. [^06]
- Reframes contact as a control modality rather than a fault condition — relevant to button-press, surface-inspection, and switch-toggling tasks. [^06]
- Gaps: manual RC only (no autonomous contact loop), force quantification noisy, flat-wall only, 700 g custom build. [^06]

---

## Consumer Reality

Every indoor contact demo in the corpus is mocap-dependent. The platforms do not know where the door handle, object, or button is without an external positioning system. Bridging this gap requires onboard depth + semantic perception robust to cluttered home environments — an unsolved integration problem; see [[drone-sensors-for-autonomy]].

Realistic timelines: supervised teleoperation (FlyCroTug model) is deployable now for simple structured tasks in known environments. Autonomous door-opening or object retrieval in an arbitrary home is a 5–10+ year research horizon. The ~$50k OMAV and custom HI-ARM hardware are not consumer products. The Bumper Drone contact-as-control framing is the most hardware-accessible result, but lacks any autonomy stack.

See [[aerial-manipulation]] for the broader manipulation landscape and [[drone-power-budget]] for endurance constraints that bound all contact-task flight time.

---

## Sources

- `raw/research/aerial-manipulation/04-learning-open-doors.md` — ETH ASL, IROS 2023 (arXiv 2307.15581): RL vs MPPI for omnidirectional MAV cabinet-door opening
- `raw/research/aerial-manipulation/09-hand-like-flying-robot.md` — HI-ARM, Nature Communications 2026: 5-DOF tendon gripper quad, broadest consumer task set
- `raw/research/aerial-manipulation/10-spectrum-doors.md` — IEEE Spectrum on FlyCroTug, Stanford BDML/EPFL, Science Robotics 2018: cooperative gecko+microspine door-opening
- `raw/research/aerial-manipulation/06-bumper-drone.md` — arXiv 2602.18976, 2025: compliant TPU-horn quad for embodied wall-contact

[^04]: `raw/research/aerial-manipulation/04-learning-open-doors.md`
[^09]: `raw/research/aerial-manipulation/09-hand-like-flying-robot.md`
[^10]: `raw/research/aerial-manipulation/10-spectrum-doors.md`
[^06]: `raw/research/aerial-manipulation/06-bumper-drone.md`

---

## Related

- [[aerial-manipulation]] — parent topic; manipulation taxonomy and hardware survey
- [[aerial-grasping]] — gripper designs and payload physics underlying transport tasks
- [[aerial-perching]] — HI-ARM outdoor perch; power savings vs sustained hover
- [[cooperative-aerial-manipulation]] — FlyCroTug anchoring-force mechanics and multi-robot coordination
- [[drone-sensors-for-autonomy]] — perception gap blocking autonomous contact tasks indoors
- [[eth-rpg-scaramuzza]] — ETH RPG (Scaramuzza); distinct from ETH ASL (Siegwart) which produced the door-opening RL work
- [[drone-power-budget]] — endurance constraints bounding contact-task flight time; HI-ARM perch power data
