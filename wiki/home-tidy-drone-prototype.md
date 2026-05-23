# Home-Tidy Drone — Prototype Feasibility & Plan

A concrete consumer use-case integration: a single indoor drone that (R1) docks/recharges autonomously, (R2) learns and navigates a house, (R3) takes voice commands, and (R4) picks up and sorts household objects ("clean up the toys"). This page maps each requirement to wiki-demonstrated capability, flags the blockers, lists follow-up research, and — in a clearly-marked beyond-wiki section — a minimal-prototype build. **Headline verdict (synthesis):** R2 (navigation) and R1 (localization/landing primitives) are achievable today; R4 (manipulation) only for *known, light* objects in a structured setup; **R3 (voice) and fully-autonomous arbitrary-object cleanup are the frontier gaps.** A constrained lab prototype is buildable now; the consumer-grade version is this wiki's 5–10+ yr horizon.

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
| Depth camera | Intel RealSense D455 | **$685 firm** (DigiKey CA, in stock) | R2 depth |
| VIO camera | **T265 is discontinued (EOL 2022)** → Stereolabs ZED Mini | **$579 firm** (Stereolabs CA) | R2 VIO; ROS 2 + Jetson |
| LiDAR (alt route) | Livox MID-360 | ~$5,850 *est* (no CA distributor; US reseller + ~$200 import) | alt R2; pick per [[lidar-vs-vision-autonomy]] |
| Gripper (DIY) | servo + silicone/foam + tendon + print | ~$50 *est* | R4, light known objects (~150 g) |
| Dock (DIY) | Qi/contact charge module + AprilTag | ~$35–50 *est* | R1; integration is beyond-wiki |
| Battery + charger | 4S 1500 mAh LiPo + balance charger | ~$110–130 *est* | power |
| Misc | cables, mounts, 128 GB SD, Wi-Fi | ~$80–100 *est* | — |
| Software | ROS 2 + SLAM (OKVIS2-/FAST-LIO-class *(wiki)*) + off-the-shelf open-vocab detector | $0 (OSS) | ties it together |

**Subtotals:** nano/bench path (Crazyflie + Jetson + D455 + ZED Mini, no LiDAR) ≈ **$3,050–3,350 CAD**; full payload + LiDAR path ≈ **$8,900–9,500 CAD** (the MID-360 dominates). Discontinued: RealSense T265 → ZED Mini substitute. Firm prices: Jetson module, Pixhawk 6C, D455, ZED Mini (DigiKey/epicfpv/Stereolabs CA); the rest are USD-converted estimates.

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
