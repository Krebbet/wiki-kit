# Ground-Aerial Robots: Burst-Flight Platforms for Indoor Use

Platforms that spend most of their time on the ground and use flight selectively — to cross stairs, reach shelves, or escape impassable terrain — offer energy profiles 4–30× better than aerial-primary designs for bounded indoor tasks. Six platforms from 2023–2026 now collectively document the mechanical design space, the energy tradeoff calculus, and the first real-world stair-climbing results. Autonomous mode switching exists in simulation; hardware deployment remains limited to teleoperated or primitive rule-based controllers.

---

## 1. The Ground-Primary Concept *(synthesis)*

*This section synthesises across sources; claims labelled individually.*

For a home-tidy or domestic service robot, the dominant operating mode is slow traversal of flat floor space — picking up objects, carrying them between rooms, docking to charge. This is exactly where ground locomotion dominates: rolling costs roughly 1 W per metre on level surfaces while hovering costs 60 W per metre [src: 02-06-arxiv-2308-13972.md, Table 4.1 assumptions]. The energy case for staying on the ground is overwhelming.

Flight adds value in three specific scenarios that matter for home use:

1. **Stairs.** A typical interior stair step is 17–20 cm. This exceeds the wheel diameter of most compact platforms and creates the central discontinuous-terrain problem the literature addresses.
2. **Vertical reach.** Placing or retrieving an object from a shelf, counter, or elevated surface requires either a long arm or controlled ascent. Brief burst flight to a shelf height (1–2 m) costs far less energy than carrying a long arm everywhere.
3. **Geometric escape.** A ground robot that encounters a table leg, cable, or door threshold it cannot traverse can hop over it in a fraction of a second rather than navigating around it.

The asymmetry between these flight-value scenarios and the continuous rolling scenario makes the ground-primary-with-burst-flight concept compelling. The question the literature addresses is whether: (a) the mechanical penalty for carrying both systems is acceptable, and (b) mode switching can be made reliable enough to be autonomous.

---

## 2. Platform Taxonomy

The platforms in this corpus span a spectrum from "aerial quadrotor with cheap passive wheels" (aerial-primary) to "morphobot that can do anything" (maximally flexible). Positioning them:

```
Aerial-primary ←————————————————————→ Ground-primary
with rolling               mixed                with burst flight

Passive-wheel  DoubleBee   Duawlfin   ATMO   M4 MorphoBot
bi-copter      (bicopter+  (quad+     (quad  (full morpho-
[air-ground-   2 wheels)   drive-     +tilt  bot, 8 modes)
hybrids]                   train)     mech)
                                             ↑
                                         most relevant
                                         for home-tidy
                                         burst-flight concept
```

**DoubleBee** [src: 05-03-arxiv-2303-05075.md] and **DoubleBee + RL** [src: 06-04-arxiv-2603-26687.md] are the most studied platform in this corpus for stair-type discontinuous terrain — compact, well-characterised, and the subject of the only real stair-climbing hardware trial in these sources.

**Duawlfin** [src: 04-02-arxiv-2505-13836.md] is the lightest and mechanically simplest unified-actuation design — the same motors drive both flight and ground propulsion via one-way bearings and a differential drivetrain.

**ATMO** [src: 03-01-arxiv-2503-00609.md] is the most aerodynamically sophisticated: it studied the physics of mid-air transformation itself, not just the resulting locomotion.

**M4 MorphoBot** [src: 01-05-pmc-m4-nature-comms.md, 02-06-arxiv-2308-13972.md] is the most capable and heaviest, with the most elaborated autonomy pipeline in simulation. The primary paper is Nature Communications 2023 (Sihite et al., Caltech) [src: 01-05-pmc-m4-nature-comms.md]; the autonomy work is a 2023 Northeastern MS thesis [src: 02-06-arxiv-2308-13972.md].

---

## 3. Platform Details

### DoubleBee (NTU, 2023)

**Institution:** Nanyang Technological University (Singapore) — School of EEE  
**Year:** 2023 (IROS)  
**Maturity:** *demoed* (hardware, indoor + limited outdoor)

DoubleBee is a bicopter (two tilting-propeller brushless motors) combined with two actively driven wheels, forming a two-wheel self-balancing robot when grounded [src: 05-03-arxiv-2303-05075.md]. Total weight **2.78 kg**, including a 5300 mAh 6S LiPo. Dimensions 51×36×12 cm excluding propellers. Two APC 10×4.5 in propellers, 880 KV motors, 30:1 gear metal drive wheels 120×60 mm.

**Ground locomotion:** Balance-bot style; propeller thrusts provide additional control inputs decoupled from translation — the "decoupled mode" enables control of pitch angle independently from wheel torques. This allows the robot to pass under low barriers by tilting to near-horizontal, then rise upright, which a conventional balance bot cannot do [src: 05-03-arxiv-2303-05075.md, Fig. 2].

**Flight:** Bicopter configuration with servo-mounted tilting propellers, controlling roll via differential thrust and pitch/yaw via tilt angle. Bicopter is cited as the most energy-efficient uniaxial multi-rotor configuration [src: 05-03-arxiv-2303-05075.md, Section I].

**Mode switching:** Throttle-based scaling factor C smoothly transitions control authority from wheel motors to servo tilt angles as throttle increases from idle to hover level [src: 05-03-arxiv-2303-05075.md, eq. 17–18]. No autonomous triggering — manual pilot command.

**Power comparison:** DoubleBee shows the lowest energy consumption in both high-power (decoupled) and power-saving (ground) modes compared to SytaB and single-passive-wheel alternatives in the same bicopter class [src: 05-03-arxiv-2303-05075.md, Fig. 5].

**Indoor suitability:** Demonstrated in indoor mission crossing under a low barrier, around a fence, over an obstacle, and through a door. Outdoor demonstration on steep grass slope in decoupled mode followed by take-off from the slope and flight across a small cliff [src: 05-03-arxiv-2303-05075.md, Fig. 10].

---

### DoubleBee + Energy-Aware RL (CMU + NTU, 2026)

**Institution:** Carnegie Mellon University + Nanyang Technological University  
**Year:** 2026 (arXiv 2603.26687, March 2026)  
**Maturity:** *demoed* (hardware gap-climbing; sim stair traversal)

Same DoubleBee hardware, new RL-trained controller. Key contribution: replacing the rule-based decoupled mode with a single continuous policy trained in Isaac Lab to coordinate all three actuator groups (propellers, wheels, tilting servos) under an explicit electrical-energy objective [src: 06-04-arxiv-2603-26687.md].

**Stair/gap results (simulation):** Inverted-pyramid staircase, step heights 0.01–0.126 m. Hybrid RL policy achieves >55% success rate vs 0% for wheels-only (fails at stair edge) and ~30% plateau for propellers-only. Hybrid RL reduces average energy by approximately **4×** versus propellers-only control, stabilising around 1500 J vs ~6000 J [src: 06-04-arxiv-2603-26687.md, Fig. 3].

**Gap-climbing results (hardware):** 8 cm gap (taller than the 6 cm wheel diameter). RL policy succeeds in 3 of 5 trials. Average power **119 W** versus 192 W for successful rule-based decoupled climb (Decouple 1) — a **38% reduction** in average power and 37.7% reduction in total energy over the same 3.1 s trial window [src: 06-04-arxiv-2603-26687.md, Section VII-B].

**Emergent behaviour:** The learned policy discovers "thrust-assisted driving" — brief propeller bursts during wheel climbing phases rather than sustained high thrust. The policy rarely uses thrust exceeding body weight. It deliberately accelerates on approach to use momentum to overcome the step edge, then reduces thrust after clearing it [src: 06-04-arxiv-2603-26687.md, Fig. 4 and Section VI].

**Failure modes:** Robot gets mechanically stuck with one wheel above, one below the step edge (asymmetric contact); forward pitch-fall on aggressive approach. Both failure modes also observed in simulation — sim-to-real consistency [src: 06-04-arxiv-2603-26687.md, Section VII-C].

**Indoor suitability:** Gap-climbing is directly relevant to interior stair lips and door thresholds. The 8 cm gap tested approximates a typical UK/EU stair step edge overhang or a tall door threshold, not a full stair height.

---

### Duawlfin (UC Berkeley, 2025)

**Institution:** UC Berkeley, Dept. Mechanical Engineering (HiPeRLab)  
**Year:** 2025 (arXiv 2505.13836, May 2025)  
**Maturity:** *demoed* (hardware indoor + outdoor)

Duawlfin weighs **~800 g** — the lightest platform in this corpus by a large margin. It uses a single unified actuation system: standard quadrotor A2212 1400 KV motors with 8045 propellers, one-way bearings so motors can drive ground drivetrain in reverse without spinning propellers, and a belt-pulley differential drivetrain [src: 04-02-arxiv-2505-13836.md].

**Ground locomotion:** Differential drivetrain driven by motor pairs in reverse rotation. Bidirectional. No additional actuators. Ball casters front and rear for stability.

**Flight:** Standard quadrotor. Only 3.23% increase in hover power and figure-8 trajectory tracking power vs baseline quadrotor without drivetrain — the added inertia from pulleys/belts is minimal [src: 04-02-arxiv-2505-13836.md, Table IV].

**Mode switching:** Motor direction reversal in software. Mode switch completes in **0.1 s** [src: 04-02-arxiv-2505-13836.md, Fig. 8]. No physical reconfiguration.

**Energy results (ground vs flight):** At 1.0 m/s circular path, ground mode consumes **3.9 W** versus flight's **124.6 W** — over **30× lower**. At 2.0 m/s: 14.9 W ground vs 188.8 W flight [src: 04-02-arxiv-2505-13836.md, Table II]. Slope climbing maintains 4.0–5.4 W mean power across 5°–30° inclines [src: 04-02-arxiv-2505-13836.md, Table III].

**Slope capability:** Successfully climbs slopes to 30°; tire slip begins beyond this. A 30° incline significantly exceeds ADA ramp standards (max 4.76°) and most interior ramp requirements [src: 04-02-arxiv-2505-13836.md, Section IV-B].

**Outdoor multi-terrain demo:** Ground locomotion on sidewalk → mode switch to flight → fly over bush → land. Manual FPV control in flight mode [src: 04-02-arxiv-2505-13836.md, Fig. 8].

**Indoor suitability:** 800 g, 0.1 s mode switch, 30× energy ratio — strong candidate for indoor delivery or lightweight tidying missions where the robot can recharge frequently. No autonomous mode switching demonstrated; propeller cage/guard not described.

---

### ATMO (Caltech, 2025)

**Institution:** California Institute of Technology — Aerospace Engineering  
**Year:** 2025 (arXiv 2503.00609, March 2025)  
**Maturity:** *demoed* (hardware, controlled indoor arena with mocap)

ATMO (Aerially Transforming Morphobot) weighs **5.5 kg**. It transforms mid-air via a single brushed DC motor actuating a worm-gear linkage that tilts all four wheel-thruster appendages simultaneously. Tilt angle φ ranges from 0° (quadrotor) to 90° (drive). Height 16 cm / width 65 cm in aerial config; 33 cm / 30 cm in ground config [src: 03-01-arxiv-2503-00609.md].

**Ground locomotion:** Differential drive via two belt-pulley systems. Wheels are the same appendages as thrusters, repurposed.

**Flight:** Conventional quadrotor when φ=0. Thrust-to-weight ratio 2.1:1. Critical tilt angle φc=60° (where vertical thrust equals gravity). In-flight tilt limited to 50° to keep 35% thrust reserve for disturbance rejection [src: 03-01-arxiv-2503-00609.md, Methods].

**Mode switching — mid-air transformation:** The key contribution is transforming *while airborne* near the ground, using a Model Predictive Controller (MPC) with a blending factor α(z,φ) that shifts the cost function from flight objectives to transition objectives as altitude and tilt angle change [src: 03-01-arxiv-2503-00609.md, eq. blending factor]. Transition phase begins at z*=0.45 m.

**Ground-effect discovery:** Load cell testing shows up to ~20% additional thrust boost from ground effect at φ=50° tilt. At φ=70°, ground effect *reverses* (suction), making this angle dangerous for landing [src: 03-01-arxiv-2503-00609.md, Fig. 3(C)]. The MPC exploits the positive ground effect at φ≤60° to land past the critical angle.

**Demonstrated manoeuvres:** (1) Dynamic wheel landing: descent + forward motion while tilting → land on wheels → continue driving. Final tilt at landing φg=65° (past critical angle of 60°). (2) Driving takeoff + dynamic wheel landing. (3) Landing on 25° slope and continuing to drive [src: 03-01-arxiv-2503-00609.md, Fig. 6].

**Limitations:** Experiments conducted in Caltech CAST flight arena using OptiTrack motion capture for state estimation. No outdoor or VIO-only demonstration. At 5.5 kg, heavier than most home-use candidates.

**Comparison to M4:** ATMO reduces postural actuators from 12 (M4) to 1, simplifying the morphing mechanism [src: 03-01-arxiv-2503-00609.md, Section Results].

**Indoor suitability:** The smooth mid-air transformation is conceptually ideal for stairs. However, the 5.5 kg mass, mocap dependency, and lab-only validation make this research-stage only.

---

### M4 MorphoBot — Primary Paper (Caltech, 2023)

**Institution:** California Institute of Technology — Aerospace Engineering and ECE  
**Year:** 2023 (Nature Communications, PMC10300070)  
**Maturity:** *demoed* (hardware, partial; full 8-mode autonomy declared future work)

The M4 (Multi-Modal Mobility Morphobot) is the landmark multi-modal platform in this field, published in Nature Communications [src: 01-05-pmc-m4-nature-comms.md]. Note: the PMC capture failed (reCAPTCHA block); the summary below is drawn from the M4 autonomy thesis which extensively describes the primary platform [src: 02-06-arxiv-2308-13972.md] and from prior wiki coverage.

M4 weighs approximately **6 kg**. Four identical shrouded propeller assemblies repurpose as: wheels (drive mode), thrusters (flight mode), and legs (segway/balance modes). The tire assembly alone weighs ~1600 g (29% of total mass) [existing coverage, air-ground-hybrids].

**Locomotion modes:** 8 total — fly, roll, crawl, crouch, balance, tumble, scout, loco-manipulate. All use the same four appendages with different configurations [src: 02-06-arxiv-2308-13972.md, Fig. 1.5].

**Ground locomotion:** Differential drive in wheel mode, Ardupilot flight controller in aerial mode [src: 02-06-arxiv-2308-13972.md, Section 3.1.1].

**Autonomy pipeline:** RealSense depth camera → 2.5D elevation mapping (Elevation Mapping Cupy / ETH RSL) → CNN traversability estimation → multimodal costmap → modified 3D A* path planner with per-node locomotion flags → waypoint follower [src: 02-06-arxiv-2308-13972.md, Fig. 3.6].

**Energy cost model (used in path planner):** Aerial travel: 60 W/m, Ground travel: 1 W/m, Morphing: 30 W per transition [src: 02-06-arxiv-2308-13972.md, Table 4.1]. At 1 m/s these become 60 J/m and 1 J/m respectively — a **60:1 ratio**.

**Path planner results (simulation):** Three test scenarios. Test Case 3 (maze environment): M4 ground path uses 60 J, pure aerial drone uses 734 J — **92% energy reduction** [src: 02-06-arxiv-2308-13972.md, Table 4.1]. Caveat: these use the assumed energy model, not measured hardware values.

**Autonomous mode switching:** The traversability CNN determines when terrain drops below threshold 0.5, triggering aerial locomotion flag. Mode selector sequences ground→flight transitions via ardupilot MAVROS. Only wheel↔fly two-mode autonomy demonstrated in simulation; the full 8-mode autonomous system is declared future work [src: 02-06-arxiv-2308-13972.md, Section 5.1].

**Maturity gap:** The autonomy thesis is simulation-only (Gazebo + Ardupilot SITL). The traversability CNN (7-layer architecture) was too slow for real-time operation on Jetson-class hardware and excluded from the scope [src: 02-06-arxiv-2308-13972.md, Section 3.2.2]. Real-robot deployment remains future work as of August 2023.

**Indoor suitability:** The 60:1 aerial-to-ground energy ratio is the most dramatic data point in this corpus for the energy case. The autonomy pipeline (elevation map → traversability → mode flag → path plan) is the closest to a complete indoor navigation stack, but currently sim-only and at 6 kg.

---

## 4. Mode Switching: How Existing Systems Decide

### Manual / teleoperated switching
All hardware-validated experiments in this corpus use manual mode switching: the pilot increases throttle to take off (DoubleBee, ATMO), reverses motor direction (Duawlfin), or commands morphing via radio (ATMO). No real-world autonomous trigger has been demonstrated [src: 03-01-arxiv-2503-00609.md; 04-02-arxiv-2505-13836.md; 05-03-arxiv-2303-05075.md].

DoubleBee's transition is throttle-governed: a scaling factor C blends servo tilt (aerial) vs wheel motor (ground) control based on commanded throttle level, providing smooth handoff [src: 05-03-arxiv-2303-05075.md, eq. 17–18]. Duawlfin's transition is a simple motor direction reversal completing in 0.1 s [src: 04-02-arxiv-2505-13836.md].

### Rule-based autonomous (simulation only)
The M4 autonomy pipeline [src: 02-06-arxiv-2308-13972.md] implements the field's most complete autonomous mode-selection stack: traversability score (CNN from elevation map) below 0.5 → assign aerial locomotion flag → modified A* prefers ground nodes when traversable, selects aerial nodes otherwise. Validated in Gazebo simulation with three obstacle scenarios. Not yet deployed on hardware.

### Learning-based (limited hardware transfer)
The CMU/NTU RL controller [src: 06-04-arxiv-2603-26687.md] learns a continuous policy that blends all actuators without discrete mode boundaries. The "mode switch" is emergent — the policy applies brief thrust bursts during difficult ground traversal rather than committing to full flight. This is the closest existing system to the "burst flight" concept: propeller use is calibrated to exactly what the task requires, not a binary switch. Hardware validation exists (3/5 gap-climbing success), but the policy runs on an external desktop GPU at 50 Hz and requires a motion capture system for state estimation — far from autonomous onboard deployment [src: 06-04-arxiv-2603-26687.md, Section VII-A].

### What autonomous switching requires (gaps)
The M4 traversability work identifies key requirements: elevation map from depth sensor, traversability CNN, costmap with locomotion flags, path planner with mode-annotated waypoints. The CNNs in these papers run too slowly for Jetson-class hardware in real time and use optic-flow or mocap for localization. The [[SLAM]] problem during mode transitions — when the robot is partly on the ground and partly airborne — remains unsolved for consumer-grade sensors.

---

## 5. Stair Navigation: What the Sources Actually Say

Stair navigation appears in four of the six sources:

**DoubleBee + RL [src: 06-04-arxiv-2603-26687.md]** — the only real hardware stair/gap result in this corpus. An 8 cm step (taller than wheel diameter) was climbed in 3/5 trials with a 38% power reduction vs rule-based controller. The step geometry — a single vertical face of 8 cm — approximates a door threshold or stair-edge lip, not a full flight of stairs. Multi-step staircase traversal is declared future work.

**DoubleBee [src: 05-03-arxiv-2303-05075.md]** — outdoor demonstration includes "steep grass field in decoupled mode before taking off on a slope and flying across a small cliff." The cliff is traversed by flying; the slope is climbed in decoupled mode with wheels + thrust assist. No interior stair geometry tested.

**M4 autonomy [src: 02-06-arxiv-2308-13972.md]** — Test Case 1 is explicitly a "step environment where the ground heights are different." In simulation, M4 uses wheels to approach, detects non-traversable step (via costmap), morphs to aerial, hops the step, lands, and continues in wheel mode. Then reverses for the step down. The 3D path planner reduces energy vs a pure aerial drone (994 J vs 1151 J) [src: 02-06-arxiv-2308-13972.md, Table 4.1]. This is **simulation only**.

**Duawlfin [src: 04-02-arxiv-2505-13836.md]** — slope climbing to 30° tested, but no stair geometry. The outdoor multi-terrain demo uses flight to traverse a bush that ground cannot handle, but the terrain geometry is not a stair.

**ATMO [src: 03-01-arxiv-2503-00609.md]** — slope landing at 25° demonstrated; stair traversal not specifically addressed.

**Summary:** Real stair climbing on hardware has been attempted for a single 8 cm step edge, succeeding 3/5 trials. Full stair flight of multiple 17–20 cm steps remains simulation-only or not yet attempted.

---

## 6. Implications for the Home-Tidy Use Case *(synthesis)*

*This section is editorial synthesis; not directly derived from any single source.*

### What ground-primary with burst flight changes vs the current plan

The current Phase-1 prototype plan (`[[home-tidy-drone-prototype]]`) is aerial-primary (X500 V2 frame, Pixhawk, Jetson, MID360 LIDAR). The `[[system-architecture]]` notes a "land-then-grasp preferred" principle in the ACTIONS EXECUTION layer. Adding a ground locomotion capability would shift the platform from "drone that occasionally hovers over objects" to "wheeled robot that occasionally hops."

**Energy budget.** The 60:1 aerial-to-ground energy ratio [src: 02-06-arxiv-2308-13972.md] means a platform rolling between rooms and ascending stairs by flight could operate 20–30× longer per charge than an aerial-primary design at the same battery capacity. This changes the charging frequency assumption from "frequent dock returns" to "occasional returns" — meaningful for an unsupervised home tidying mission.

**Stair handling.** The current aerial-primary plan can navigate stairs by flying (the MID360 + Jetson stack supports 3D mapping). The ground-primary alternative must fly for stairs, but the flight is brief (seconds, not minutes) and the platform spends the vast majority of time rolling. The DoubleBee + RL result [src: 06-04-arxiv-2603-26687.md] confirms that a single-step hop is achievable with a learned policy, but a full staircase (12–16 steps) has not been demonstrated.

**Object manipulation.** Aerial-primary platforms use hover to position an arm. Ground-primary platforms use the floor as a stable base. The AirCrab result in `[[air-ground-hybrids]]` shows that ground contact halves end-effector RMSE (1.02 cm vs 2.00 cm). A compact wheeled base with a short arm or gripping mechanism is mechanically simpler than a hovering arm.

**Size and safety.** The lightest ground-primary platform with both modes demonstrated is Duawlfin at 800 g [src: 04-02-arxiv-2505-13836.md]. DoubleBee is 2.78 kg [src: 05-03-arxiv-2303-05075.md]. The current X500 V2 frame plan runs ~1.5–2 kg dry. A compact wheeled robot at 800–1500 g is meaningfully safer near humans and pets than a hovering 2+ kg aerial platform.

### What it does not solve

**Autonomous mode switching on consumer sensors.** Every system in this corpus uses motion capture, OptiTrack, Vicon, or an external GPU for state estimation. The traversability CNN (M4) runs too slowly for Jetson-class hardware. The RL policy (CMU/NTU) uses mocap for deployment. The [[SLAM]] problem during ground-to-air transitions — wheel odometry failing, IMU integrating, optical flow unreliable near the ground — is unsolved.

**Propeller safety near humans.** Burst flight in a domestic environment requires exposed spinning propellers near pets, children, and furniture. All platforms in this corpus either operate in controlled lab environments or outdoor spaces. No platform here has addressed domestic propeller safety (guards, variable-pitch stop, shrouding).

**Mapping and obstacle avoidance on the ground.** The current aerial-primary plan uses the MID360 LiDAR for 3D mapping optimised for airborne operation. A ground-primary platform needs a different sensor configuration: close-range depth perception for wheel-height obstacles (see `[[close-range-depth-sensors]]`), and the mapping pipeline needs to handle the robot footprint changing when it transitions to flight mode.

**Maturity gap.** No platform in this corpus ships commercially. The most mature (DoubleBee hardware results) still requires motion capture and manual mode switching. The gap from demoed to deployable in a domestic environment is substantial.

### Direction

The ground-primary burst-flight architecture is likely the correct long-term direction for an indoor domestic service robot. It changes the energy equation dramatically, enables manipulation from a stable base, and reduces the continuous safety exposure from spinning rotors. However, the immediate next step for Phase-1 — a manually operated aerial platform to develop the AI stack — is not made wrong by this literature. Building the manipulation and navigation AI on the aerial platform first, then migrating to a ground-primary frame in Phase 2, is a viable path. The DoubleBee frame (or a variant) is a natural candidate for Phase 2.

---

## 7. Maturity Summary Table

| Platform | Institution | Year | Mass | Ground mechanism | Flight | Mode switch | Stair demo | Maturity |
|---|---|---|---|---|---|---|---|---|
| DoubleBee | NTU | 2023 | 2.78 kg | 2 active wheels, balance-bot | Bicopter (tilting props) | Throttle-based (manual) | Single step edge (8 cm) via RL follow-on | *demoed* |
| DoubleBee + RL | CMU+NTU | 2026 | 2.78 kg | Same | Same | Learned continuous (no discrete modes) | 3/5 success on 8 cm step | *demoed* |
| Duawlfin | UC Berkeley | 2025 | ~800 g | Differential drivetrain (one-way bearings) | Quadrotor | Motor reversal, 0.1 s | None | *demoed* |
| ATMO | Caltech | 2025 | 5.5 kg | Differential drive (belt-pulley) | Tilt-rotor quadrotor (mid-air transform) | Manual (MPC-controlled transition) | Slope landing 25° | *demoed* |
| M4 MorphoBot | Caltech | 2023 | ~6 kg | Wheeled drive (repurposed props) | Quadrotor (repurposed props) | Sim-autonomous (traversability CNN) | Sim-only, step environment | *demoed* (sim autonomy) |
| M4 Autonomy | Northeastern | 2023 | ~6 kg | Same | Same | Modified A* with mode flags (sim-only) | Sim-only | *sim-only* (autonomy) |

---

## Source

- `raw/research/dual-mode-robots/03-01-arxiv-2503-00609.md` — arXiv 2503.00609 (Caltech, Mar 2025): ATMO mid-air transforming morphobot, MPC transition controller, ground-effect aerodynamics
- `raw/research/dual-mode-robots/04-02-arxiv-2505-13836.md` — arXiv 2505.13836 (UC Berkeley, May 2025): Duawlfin unified actuation, 30× energy saving at 1 m/s, 0.1 s mode switch
- `raw/research/dual-mode-robots/05-03-arxiv-2303-05075.md` — arXiv 2303.05075 (NTU, IROS 2023): DoubleBee bicopter+wheels, decoupled control, power comparison
- `raw/research/dual-mode-robots/06-04-arxiv-2603-26687.md` — arXiv 2603.26687 (CMU+NTU, Mar 2026): Energy-aware RL for DoubleBee on stair-like terrain, 38% power reduction vs rule-based, 4× vs propellers-only in sim
- `raw/research/dual-mode-robots/01-05-pmc-m4-nature-comms.md` — PMC10300070 / Nature Comms 2023 (Caltech): M4 MorphoBot primary paper (capture blocked by reCAPTCHA; data from thesis source)
- `raw/research/dual-mode-robots/02-06-arxiv-2308-13972.md` — arXiv 2308.13972 (Northeastern, Aug 2023): M4 traversability estimation and 3D path planning, autonomous mode switching pipeline (simulation)

## Related

- [[air-ground-hybrids]] — overlapping platforms (M4, TiltRopter, passive-wheel bi-copter); see that page for Roller Quadrotor and AirCrab details
- [[multimodal-locomotion]] — parent topic; energy case for ground locomotion
- [[home-tidy-drone-prototype]] — current Phase-1 build; the ground-primary direction is a Phase-2 candidate
- [[system-architecture]] — ACTIONS EXECUTION "land-then-grasp preferred" principle; ground-primary extends this to the full mission profile
- [[payload-budget]] — weight constraints relevant to drivetrain mass penalty
- [[SLAM]] — mode-transition localisation is the central unsolved problem
- [[close-range-depth-sensors]] — sensing stack for ground-mode obstacle avoidance
- [[drone-autonomy-state]] — autonomous mode switching state-of-the-art
