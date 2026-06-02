# Home-Tidy Drone — Prototype Feasibility & Plan

A concrete consumer use-case integration: a single indoor drone that (R1) docks/recharges autonomously, (R2) learns and navigates a house, (R3) takes voice commands, and (R4) picks up and sorts household objects ("clean up the toys"). This page maps each requirement to wiki-demonstrated capability, flags the blockers, lists follow-up research, and — in a clearly-marked beyond-wiki section — a minimal-prototype build. **Headline verdict (synthesis):** R2 (navigation) and R1 (localization/landing primitives) are achievable today; R4 (manipulation) only for *known, light* objects in a structured setup; **R3 (voice) and fully-autonomous arbitrary-object cleanup are the frontier gaps.** A constrained lab prototype is buildable now; the consumer-grade version is this wiki's 5–10+ yr horizon.

## Phase 1 pivot — ground robot for perception/nav prototype *(added 2026-05-30)*

**Platform:** Pivoted from aerial drone to a ground robot chassis for Phase 1 iteration. Aerial drone remains the long-term target; ground platform eliminates flight-safety, endurance, and vibration constraints so the perception / nav / world-model stack can be validated quickly and cheaply. Findings transfer directly — the sensor stack, SLAM pipeline, ROS 2 architecture, and server-side world brain are identical. The drone replaces the chassis in Phase 2.

**Sensor in hand:** SVPRO 1080P 60FPS USB stereo camera (3840×1080 side-by-side, UVC). Passive stereo — no active IR; depth via stereo matching. Usable for fiducial detection, passive visual odometry, and 2D object detection today. Metric depth for manipulation requires adding D435 (see [[close-range-depth-sensors]]). **Hands-on characterization (measured, not spec-sheet):** see *"SVPRO characterization (measured)"* under *What can start now* below — enumerates at 3840×1080 SBS MJPG @**30 fps over USB 2.0** (not the spec'd 60), baseline ≈57.8 mm, ~48% indoor depth coverage.

### Four workstreams

Phase 1 splits into four independently buildable workstreams:

**(A) Robot-side** — sensor drivers, localization (visual SLAM / wheel odometry), local map publisher, object detector (YOLO-World on RGB), navigation executor (receives goal poses from server, runs local path planner).

**(B) Server-side world view** — map store (persists geometric map across sessions), object registry (known objects, expected vs actual locations), scene diff engine (present / missing / moved), static/dynamic classifier, world state API.

**(C) Robot ↔ server comms** — pose stream (robot → server, ~10 Hz), detection events (robot → server on new detection), map increments, goal commands (server → robot), state sync on reconnect, heartbeat/watchdog. Protocol: ROS 2 DDS for robot-local topics; thin MQTT or gRPC bridge to server. See [[drone-comms-wifi]] for DDS-over-WiFi failure modes.

**(D) User communication layer** — voice entry point (phone) → STT (Whisper) → intent parser (Claude Haiku) → command router → drone-core API → TTS response. Entirely separate repo (`drone-app`); calls server world API. See [[user-comms-layer]].

### Repo split

| Repo | Contains | Can build in isolation |
|---|---|---|
| `drone-core` | `robot/` (ROS 2 packages), `server/` (world brain service), `shared/` (message/API schemas) | No — robot and server share interface definitions |
| `drone-app` | Voice, intent, router, feedback | Yes — mock drone-core API with a stub server |

### What can start now (SVPRO camera in hand, no robot chassis)

| Task | Block |
|---|---|
| AprilTag / ArUco fiducial detection + pose | A |
| Stereo camera calibration (intrinsics + extrinsics) | A |
| UVC → ROS 2 camera node (`usb_cam` / `v4l2_camera`) | A |
| Object detection pipeline (YOLO-World on RGB, laptop) | A |
| Passive stereo depth test (SGBM / RAFT-Stereo, textured scenes) | A |
| Object registry schema + DB design | B |
| Scene diff engine (mock detections) | B |
| World state API design | B |
| ROS 2 topic schema + message type definitions | C |
| MQTT/gRPC bridge design | C |
| STT → intent parser → router pipeline (mock drone-core) | D |

### What is blocked on chassis hardware

Navigation executor, wheel odometry / IMU fusion, full SLAM-to-nav closed loop, live detection → registry updates, real-time comms testing.

### SVPRO characterization (measured) *(drone-prototype Session 1, 2026-06-01)*

First hands-on validation of the SVPRO against the visual front-end (capture → calibrate → metric depth). Source: `drone-prototype` repo — `docs/prototype-diary.md` (2026-06-01), `docs/parked.md` P-001/P-002. These are *measured* facts that correct/extend the spec-sheet line above; tag maturity = **demonstrated at toy scale**.

**Device & stream (measured):**
- Enumerates as `3D USB Camera` USB id **`32e4:0035`** (a non-integrated UVC device; appears as a single `/dev/videoN` capture node + a sibling non-capture node).
- Delivers true **3840×1080 side-by-side stereo, MJPG, @30 fps** at full native resolution — *not* the spec-sheet 60 fps, because the working data path runs at **USB 2.0 (480 Mbit/s)**. 30 fps is adequate for handheld mapping.
- Mounted **upside-down** in this rig; because the frame is side-by-side, a single full-frame 180° rotation both un-inverts *and* swaps L/R correctly (an inverted rig puts the physical-left camera in the raw-right half). Handle orientation once, centrally, then split at midpoint.
- **Stereo baseline ≈ 57.8 mm** (recovered from calibration; metric scale cross-checked to within +3.3–3.7 % of tape at ~1.14 m).
- Calibration achievable to prototype grade: **mono RMS ≈ 0.8 px, stereo RMS ≈ 1.9–2.45 px** (5-coeff distortion model; the wide-lens `CALIB_RATIONAL_MODEL` diverges without many more edge-covering poses). Not yet metrology-grade — see P-002.

**Passive-stereo indoor reality (the failure regime, measured):**
- Dense SGBM depth gives **~48 % pixel coverage** on a real cluttered room scene (range ~0.5–15 m), good on textured surfaces.
- **Drops out entirely on blank walls / ceiling / bright windows** (no-depth black holes) — the expected passive-stereo indoor Achilles' heel (consistent with [[indoor-cluttered-slam]]).
- **Spurious *far* depth on textureless far surfaces** is the dangerous mode: a blank wall can read ~19 m ("clear ahead" where there is actually an obstacle) — safety-relevant; active depth ([[close-range-depth-sensors]]) is the production answer.

**USB data-path gotcha (integration risk → P-001):** the camera ships with a USB-C→USB-A cable, but a USB-C-only laptop (TB4) + a naive USB-A→USB-C adapter produces **zero kernel events** (a silently non-data path). It only enumerated through a **powered USB-C dock** (Belkin 6-in-1), and even then the camera↔dock link **dropped off the bus unprompted under load** and recovered on replug. A robot using this sensor needs a pinned, mechanically-secured, known-data USB/power path plus a sensor-dropout watchdog (the INTERNAL HEALTH CHECK subsystem in [[system-architecture]]).

## Phase 1 — first prototype: core comms + autonomous navigation *(revised 2026-05-24 — fiducials-first staging)*

Scope cut to **two goals**; manipulation / voice / dock / semantic cleanup deferred — but the WiFi link is architected so they bolt on later. **Thesis:** a drone that safely auto-navigates a household (take off → traverse → land at locations) *and* rides the home WiFi becomes the platform for every future feature (mapping, voice, objects). Software assumed open-source / self-built (ArduPilot/PX4, ROS 2, FAST-LIO2, OpenVINS/VINS-Fusion); established systems only where clearly best.

### Phase-1 requirements
- **P1 — Comms backbone:** companion computer joins home WiFi (station mode); bidirectional command + telemetry/feedback to a ground-station laptop; built to later offload mapping/voice/AI.
- **P2 — Onboard SLAM + state estimation:** build & localize in GPS-denied indoor space, fully onboard.
- **P3 — Autonomous position/movement control:** position hold, waypoints, safe **takeoff + landing** at chosen indoor spots.
- **P4 — Safe near people/pets:** prop guards/ducts, low speed, hardware kill-switch, tethered first flights ([[safe-indoor-flight]]).
- **P5 — WiFi is supervisory, not flight-critical:** nav must survive WiFi dropout (autonomy stays onboard).

### Sensing decision *(wiki-sourced)*
Indoor homes are the *worst case* for pure vision: blank walls + repetitive/symmetric rooms starve VIO features and variable lighting degrades cameras, while LiDAR scan-matching stays robust and catches thin obstacles (chair/table legs) cameras miss ([[indoor-cluttered-slam]], [[lidar-vs-vision-autonomy]], [[drone-sensors-for-autonomy]]). Camera depth (3–6.5 m) is plenty for rooms but texture/light-dependent ([[visual-inertial-slam]]).

| Sensor | Pros (indoor) | Cons | Verdict |
|---|---|---|---|
| **Unitree L1 ($249) + IMU → LIO** | true 3D (360°×90°), ceiling/table/stair detection; lighting-independent; Unitree explicitly targets "sweeping robots"; 0.05 m blind zone | 230 g, 6 W (needs 12 V DC-DC on battery); binary SDK (longevity risk); 2/3 units worked in one independent test | **Recommended for Phase-1 ground robot nav loop** — see [[cheap-lidar-pricing-guide]] |
| **Solid-state LiDAR (Livox MID360) + IMU → FAST-LIO2** | lighting-independent cm geometry; thin-obstacle detection; robust on blank walls; FAST-LIO2 ecosystem mature | ~265 g, ~$480–550 (AliExpress) / $749 retail; no colour/semantics | **Recommended for UAV (Phase 2)** and higher-accuracy ground builds; overkill for Phase-1 ground robot |
| **Depth+RGB camera (RealSense D435) + VIO** | cheaper/lighter; RGB for future features; best close-range accuracy (<1 cm at ≤1 m on household objects per [[close-range-depth-sensors]]) | blank-wall/low-light depth noise; IR washes out in window sun | budget alternative |
| **Stereo/mono VIO only** | lightest/cheapest; rich semantics | weakest on featureless indoor; needs texture+light | not for safety-critical nav alone |

**Recommendation (Phase-1 ground robot):** **Unitree L1 ($249) + IMU for the navigation/safety loop, plus a cheap RGB camera for future semantic features.** The L1 delivers true 3D coverage at a price point compatible with a commercial-tier tidy bot (~$1,000–$2,000 retail target). For the UAV (Phase 2), MID360 + FAST-LIO2 remains the target — the mature FAST-LIO2 ecosystem and higher point density justify the premium for aerial use. Budget path: 2D LiDAR (YDLIDAR X4 ~$70–90 or LDROBOT D500 ~$70–90) + supplemental ToF, accepting planar-only nav — see [[cheap-lidar-pricing-guide]] for full tier analysis. D435 preferred over D455 for close-range manipulation work: achieves <1 cm error at ≤1 m, works down to ~16 cm; D455 has a 0.6 m minimum range that excludes the final grasp-approach envelope (see [[close-range-depth-sensors]]).

### Architecture
Flight controller (Pixhawk → ArduPilot/PX4) does low-level stabilisation + arming/RTL/kill. **Companion computer (Jetson Orin NX/Nano)** runs ROS 2 + SLAM and feeds external-vision pose to the FC EKF (MAVROS `vision_pose`), issuing setpoints ([[nano-drone-compute]] for the onboard-compute envelope). Companion joins home WiFi (station); ground-station laptop runs QGroundControl + ROS 2 over the same WiFi for commands/telemetry. **Nav loop is fully onboard; WiFi carries supervisory + future-offload traffic only.**

### Revised buy list *(CAD; beyond-wiki — my recommendation; verify before purchase)*
| Item | Pick | CAD | Note |
|---|---|---|---|
| Airframe | indoor-safe quad ~400–500 mm + prop guards (e.g. Holybro X500 V2 + guards) | ~$355 + guards | must lift ~600–800 g; smaller = safer but less payload |
| Flight controller | Holybro Pixhawk 6C | ~$245 | ArduPilot/PX4 |
| Companion compute | Jetson Orin NX 16 GB (budget: Orin Nano 8 GB) | ~$1,525 NX | runs FAST-LIO2 + ROS 2 |
| LiDAR (nav) — ground robot Phase 1 | **Unitree L1 PM** | **~$340 CAD** (≈$249 USD) | true 3D 360°×90°, 0.05 m blind zone, built-in IMU; needs 12 V DC-DC converter (~$10–15 CAD); [[cheap-lidar-pricing-guide]] |
| LiDAR (nav) — UAV Phase 2 | Livox MID360 | ~$655–750 CAD (≈$480–550 USD AliExpress) | FAST-LIO2 ecosystem; see [[fast-lio-mid360-orin]]; *updated from earlier ~$1,000 est* |
| RGB cam (future features, WiFi-streamed) | CSI/USB cam (Arducam/RPi-cam class) | ~$40–80 | decoupled from nav loop |
| WiFi | Jetson onboard WiFi or USB AX dongle | $0–40 | home-WiFi station mode |
| Battery + charger | 4S/6S LiPo + balance charger | ~$120–150 | |
| Ground station | your laptop + QGroundControl + ROS 2 | $0 | OSS |
| Misc | guards, anti-vib mount, cables, 128 GB SD | ~$100–150 | |

**Subtotal (Phase-1 ground robot):** Unitree L1 path ≈ **$2,300–2,700 CAD** (Orin NX + Pixhawk + L1 + cam + battery + misc); budget (Orin Nano + D435, 2D YDLIDAR X4 ~$95 CAD) ≈ **$1,800–2,100 CAD**. Phase-2 UAV with MID360 ≈ **$2,800–3,300 CAD** (L1 replaced by MID360 ~$700 CAD). *Updated 2026-06-01: L1 at $249 replaces MID360 as Phase-1 recommendation; MID360 AliExpress price revised to ~$480–550 USD.*

### Staging principle — fiducials-first *(synthesis, added 2026-05-24)*
Two mass-market precedents say *don't start with full SLAM*. Robot vacuums shipped on cheap 2D LiDAR + wheel dead-reckoning (and earlier, pure bump-and-random) before any VSLAM; Amazon/Kiva run 100,000s of robots on a **floor-fiducial grid + a central planner**, not per-robot autonomy ([[robot-vacuum-navigation]], [[warehouse-robot-navigation]]). A drone has no wheel odometry, but the lesson transfers: replace the unsolved indoor-localization problem with **printed AprilTag/ArUco markers + optical-flow hold** for V1 — which ArduPilot's optical-flow `Loiter`/`FlowHold` + precision-landing already support out of the box ([[gps-denied-hover-land]]). This de-risks the hard EKF-integration and flight-safety work ([[slam-fc-integration]]) on a *known-good* position source before SLAM enters the loop. MID360 + FAST-LIO2 ([[fast-lio-mid360-orin]]) stays the target for marker-free traversal — it's milestone **6**, not the first thing you debug in flight.

### Staged experiments / milestones
1. **Safe-flight bench** — ArduPilot + QGC; prop guards/ducts; tethered manual hover; verify kill-switch + failsafes ([[safe-indoor-flight]], [[prop-guard-failsafe]]).
2. **Comms backbone (P1)** — Jetson on home WiFi; ROS 2 + MAVROS FC↔Jetson↔laptop; arm/takeoff from laptop + live telemetry. Solve DDS-over-WiFi discovery (Zenoh / FastDDS Discovery Server) + MAVLink-over-UDP routing early ([[drone-comms-wifi]]).
3. **Fiducial + optical-flow hover (P2/P3, no SLAM)** — Matek 3901-L0X optical-flow `Loiter`; AprilTag/ArUco precision takeoff/land onto a printed pad ([[gps-denied-hover-land]]). **This is the fiducials-first V1** — proves the flight + EKF + safety loop without SLAM.
4. **SLAM handheld (no flight)** — MID360 + FAST-LIO2 on Jetson; walk the house; check map + drift ([[fast-lio-mid360-orin]]).
5. **Sim loop** — SITL + Gazebo/Isaac; vision-pose→setpoint loop before real flight.
6. **Onboard SLAM position hold (P2+P3, marker-free)** — FAST-LIO2 pose → EKF3 external nav; GPS-denied hover with no fiducials ([[slam-fc-integration]]).
7. **Single-room autonomy** — waypoint + takeoff/land; reactive obstacle stop ([[indoor-obstacle-avoidance]]).
8. **Multi-room traverse** — land at named locations; confirm payload/endurance margin holds ([[payload-budget]]).
9. **End-to-end thesis** — laptop sends "go to X" over WiFi → onboard nav executes.

### Follow-up research — now ingested *(each has a page, 2026-05-24)*
- ROS 2 ↔ ArduPilot/PX4 external-vision-pose integration (MAVROS `vision_pose`, EKF3 ext-nav, frames, divergence) → [[slam-fc-integration]].
- FAST-LIO2 / Point-LIO on Jetson Orin + MID360 (driver, IMU quirks, calibration, compute) → [[fast-lio-mid360-orin]].
- Indoor local-planner / obstacle-avoidance stacks (BendyRuler/Dijkstra, EGO-Planner, FASTER) → [[indoor-obstacle-avoidance]].
- WiFi-station comms (DDS-over-WiFi discovery, MAVLink-over-IP, dropout) → [[drone-comms-wifi]].
- Prop-guard / failsafe low-energy indoor safety → [[prop-guard-failsafe]].
- GPS-denied precision takeoff/landing (optical-flow + fiducial; seeds the later dock [[precision-docking-recharging]]) → [[gps-denied-hover-land]].
- Payload/endurance budgeting for Jetson+LiDAR mass on the frame → [[payload-budget]].
- Precedent studies — how consumer & industrial robots already solve indoor nav → [[robot-vacuum-navigation]], [[warehouse-robot-navigation]].

*This Phase-1 section supersedes the broad "Beyond the wiki" buy list below for the **first** build; the rest of the page remains the long-term scope.*

## Requirements

| ID | Requirement | Implicit sub-requirements |
|---|---|---|
| **R1** | Locate & return to a charging station; auto-RTL on low battery / when idle | precision landing, dock recognition, recharge loop, endurance budgeting |
| **R2** | Operate indoors; autonomously learn house layout & navigate | GPS-denied SLAM, semantic mapping, obstacle avoidance, relocalization |
| **R3** | Accept voice commands (phone or other) | speech→intent, task grounding |
| **R4** | Pick up common household objects, place in specific locations | object detection, grasp-pose, payload, place/sort memory |
| **(R5)** | *Implicit:* safe around people/pets indoors; enough endurance per task | prop-guarding, contact tolerance, fail-safe |

## Capability mapping *(strictly wiki-sourced)*

| Req | What the wiki shows is available | Maturity | Source |
|---|---|---|---|
| **R1 — localize dock** | Visual place recognition (LENS, SynSense Speck) at 2.7 mW — recognise a previously-visited location | *demoed* (on a ground robot; drone-relevance by transfer) | [[neuromorphic-computing-for-drones]] |
| **R1 — land on dock** | Optic-flow-divergence autonomous landing (35-neuron SNN on Loihi) | *demoed* | [[neuromorphic-computing-for-drones]] |
| **R1 — why dock at all** | Flight endurance 3–15 min; propulsion is 85–96% of power; perching/ground rest as the endurance lever | *shipping/demoed* | [[drone-power-budget]] · [[aerial-perching]] |
| **R2 — map+navigate, no GPS** | VI-SLAM + dense submaps + trajectory anchoring, fully onboard (OKVIS2 + supereight2; Jetson Orin NX) | *demoed* (outdoor forest; indoor-cluttered untested in-corpus) | [[visual-inertial-slam]] |
| **R2 — alt sensor route** | LiDAR-inertial SLAM (FAST-LIO2/Point-LIO); solid-state Livox MID360 (265 g/$700); NanoSLAM onboard <100 mW | *demoed* / *shipping* (inspection) | [[lidar-for-uav-autonomy]] · [[nano-drone-compute]] |
| **R2 — sensor decision** | Sensor→purpose map; the LiDAR-vs-vision choice is an OPEN conflict scoped by regime | contested | [[drone-sensors-for-autonomy]] · [[lidar-vs-vision-autonomy]] |
| **R3 — voice→action** | Language-conditioned action exists *only* as VLA (AIR-VLA benchmark ~42/100; DroneVLA PoC) | *sim-only / pre-commercial* | [[air-vla]] · [[dronevla]] |
| **R4 — grasp** | Soft tendon gripper, vision-only onboard, 2 m/s, ~150 g; pneumatic gripper 217 g | *demoed* | [[aerial-grasping]] |
| **R4 — transport/place** | Hand-like 5-DOF gripper (HI-ARM) — palm-grasp + fingertip pinch, multi-object household sequence | *demoed* (mocap-bound) | [[drone-contact-and-door-tasks]] · [[aerial-manipulation]] |
| **R5 — safe contact** | Contact-tolerant compliant morphology (Bumper Drone) — collisions as control, not faults | *demoed* (manual RC) | [[drone-contact-and-door-tasks]] |

## Gap analysis *(wiki-sourced — the blockers)*

1. **Onboard semantic perception without motion-capture — THE blocker.** Every indoor manipulation demo in the corpus localizes objects with external mocap; none carry mocap-free object/handle/location perception ([[aerial-manipulation]], [[drone-contact-and-door-tasks]], [[drone-sensors-for-autonomy]]). R4 is gated on this.
2. **No zero-shot grasping.** Both demonstrated grippers need per-object CAD/keypoint models — "common household objects" of arbitrary shape are out of scope ([[aerial-grasping]]). Directly blocks "clean up *the toys*" (varied, unknown items).
3. **Payload ceiling ~150–217 g** ([[aerial-grasping]]) — many toys/objects exceed this.
4. **Endurance 3–15 min** ([[drone-power-budget]]) — forces R1's dock and bounds how much cleanup happens per sortie.
5. **Voice front-end uncovered.** The wiki has no speech-recognition / voice-UI content; the closest (VLA language-conditioning) is sim-only ~42/100 ([[air-vla]], [[dronevla]]). R3 is the least-supported requirement.
6. **No integrated dock-find→precision-land→recharge loop.** The *primitives* (place recognition, optic-flow landing) exist ([[neuromorphic-computing-for-drones]]) but the closed autonomous-recharge loop is not a demonstrated system in-corpus.
7. **Indoor safety near people/pets.** Propeller hazard during close interaction is explicitly unsolved ([[aerial-manipulation]]); contact-tolerant design mitigates collisions only ([[drone-contact-and-door-tasks]]).
8. **Indoor-cluttered SLAM specifically.** The strongest fully-onboard nav result is an *outdoor forest* demo ([[visual-inertial-slam]]); cluttered-home performance is untested in-corpus.

## Follow-up research assignments *( ingested 2026-05-23 — each now has a page )*

1. [[onboard-grasp-perception]] — open-vocab object detection + grasp-pose; the mocap-replacement / central blocker (gap #1, #2).
2. [[precision-docking-recharging]] — the closed find→land→recharge loop (gap #6).
3. [[indoor-cluttered-slam]] — indoor/cluttered-home VIO-LIO vs the outdoor demos (gap #8).
4. [[voice-intent-task]] — voice→intent→task pipelines / on-device speech + grounding (gap #5).
5. [[safe-indoor-flight]] — ducted/caged props, contact-tolerant design, consumer indoor safety (gap #7).
6. [[semantic-object-memory]] — semantic mapping + object-location memory ("where do toys belong"); supports R4.

## Beyond the wiki — minimal-prototype build *(NOT wiki-sourced; my recommendation; outside-knowledge, flagged per /query rules)*

> Everything in this section is build advice that exceeds the wiki's source corpus. Wiki-named components are tagged *(wiki)*; the rest is my recommendation and should be verified before purchase.

**De-risking principle:** v1 should *delete the unsolved problems*. Use known/tagged objects, an AprilTag-marked dock, and structured rooms — i.e. replace the missing zero-shot perception (gap #1/#2) with fiducials, exactly as every wiki demo replaces it with mocap. Prove the loop, then remove crutches.

Canadian retail prices (CAD, May 2026; firm = found at a Canadian retailer, *est* = USD×~1.37). Build as **two tiers** — a nano/bench path (prove nav + dock + voice cheaply) and a payload path (adds R4 manipulation + optional LiDAR).

| Subsystem | Pick (SKU) | CAD | Why / note |
|---|---|---|---|
| Airframe — bench | Crazyflie 2.1+ (Bitcraze) | ~$325 *est* | nano nav/dock experiments only; can't lift a gripper |
| Airframe — payload | Holybro X500 V2 ARF (+ prop guards) | ~$355 *est* (ARF sold out; frame-only ~$170 + motors/ESC ~$120–150) | payload class for R4 |
| Compute | NVIDIA Jetson Orin NX 16 GB (dev kit / module) | ~$1,525 *est* / module **$1,539 firm** (DigiKey CA) | onboard SLAM + perception |
| Flight controller | Holybro Pixhawk 6C (PX4/ArduPilot) | **$245 firm** (epicfpv.ca) | autopilot + RTL primitives |
| Depth camera | Intel RealSense D435 | ~$580 *est* (D455 was $685 firm; D435 ~$100 less) | R2 depth; preferred over D455 for close-range manipulation (<1 cm at ≤1 m, works to ~16 cm min range vs D455's 0.6 m floor) — see [[close-range-depth-sensors]] |
| VIO camera | **T265 is discontinued (EOL 2022)** → Stereolabs ZED Mini | **$579 firm** (Stereolabs CA) | R2 VIO; ROS 2 + Jetson |
| LiDAR (alt route) | Livox MID-360 | ~$5,850 *est* (no CA distributor; US reseller + ~$200 import) | alt R2; pick per [[lidar-vs-vision-autonomy]] |
| Gripper (DIY) | servo + silicone/foam + tendon + print | ~$50 *est* | R4, light known objects (~150 g) |
| Dock (DIY) | Qi/contact charge module + AprilTag | ~$35–50 *est* | R1; integration is beyond-wiki |
| Battery + charger | 4S 1500 mAh LiPo + balance charger | ~$110–130 *est* | power |
| Misc | cables, mounts, 128 GB SD, Wi-Fi | ~$80–100 *est* | — |
| Software | ROS 2 + SLAM (OKVIS2-/FAST-LIO-class *(wiki)*) + off-the-shelf open-vocab detector | $0 (OSS) | ties it together |

**Subtotals:** nano/bench path (Crazyflie + Jetson + D435 + ZED Mini, no LiDAR) ≈ **$2,950–3,250 CAD**; full payload + LiDAR path ≈ **$8,800–9,400 CAD** (the MID-360 dominates). Discontinued: RealSense T265 → ZED Mini substitute. Firm prices: Jetson module, Pixhawk 6C, ZED Mini (DigiKey/epicfpv/Stereolabs CA); D435 price is USD-converted estimate — verify before purchase.

**Honest expectation (beyond-wiki):** a v1 that docks, maps a room, takes a phone voice command, and relocates *known, tagged, sub-150 g* objects to a *tagged* bin is achievable as a lab build. "Autonomously clean up arbitrary toys by voice" is the consumer end-state and depends on the six research assignments above — it is *not* buildable from current wiki-attested capability.

## Source

- `(wiki)` [[drone-autonomy-state]] · [[visual-inertial-slam]] · [[lidar-for-uav-autonomy]] · [[nano-drone-compute]] — R2 navigation/SLAM
- [[neuromorphic-computing-for-drones]] — R1 place-recognition + optic-flow landing primitives
- [[drone-power-budget]] · [[aerial-perching]] — endurance / why-dock
- [[aerial-grasping]] · [[drone-contact-and-door-tasks]] · [[aerial-manipulation]] — R4 manipulation + small-drone mechanism map
- [[air-vla]] · [[dronevla]] — R3 language-conditioned action (sim-only)
- [[drone-sensors-for-autonomy]] · [[lidar-vs-vision-autonomy]] — sensor architecture decision

## Related

- [[aerial-manipulation]] — manipulation mechanism comparison + the mocap-dependency gap
- [[drone-autonomy-state]] — control-model paradigms; demoed ≠ shipping ≠ legal
- [[drone-power-budget]] — endurance ceiling driving the dock requirement
- [[lidar-vs-vision-autonomy]] — the open sensor-architecture conflict this prototype must pick a side of
- [[passive-stereo-robustification]] — consumer-cost ladder for making the SVPRO passive stereo robust enough for the anchor map (robustifiers → active IR stereo; cheaper-than-D435i hardware path)
