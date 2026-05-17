# Aerial Grasping

Vision-based onboard grasping is the consumer-relevant frontier: recent platforms demonstrate grasp speeds up to 2.0 m/s with no external infrastructure. Key gaps remain — per-object keypoint models (no zero-shot), a ~150–217 g payload ceiling, and mocap dependence for any dynamic target.

## Demonstrated systems

### Soft-drone tendon gripper (npj Robotics 2024)

Custom quadrotor with a 4-finger passively-closing foam gripper (tendon-driven, 1 motor/finger). [[drone-sensors-for-autonomy]] stack: RealSense D455 running ResNet-18 keypoint detection + TEASER++ pose estimation; [[visual-inertial-slam]] via Intel T265 VIO. Compute: Jetson Xavier NX + Pixhawk 4 Mini — fully **onboard**, no mocap. [src:03-soft-drone-grasping]

| Speed | Object | Success |
|-------|--------|---------|
| 0.5 m/s | bottle (60 g) | 10/10 |
| 0.5 m/s | med-kit (148 g) | 9/10 |
| 0.5 m/s | box (115 g) | 6/10 |
| 2.0 m/s | med-kit (vision-only) | 3/10 |
| outdoor | med-kit | 8/10 |

2.0 m/s is the fastest vision-only onboard grasp reported at publication. Payload ceiling ~150 g. Flight endurance ~3 min — see [[drone-power-budget]]. Moving-target grasp requires mocap. [src:03-soft-drone-grasping]

### Pneumatic soft gripper / landing-gear dual-use (arXiv 2311.00390)

Modular pneumatic gripper (4 silicone fingers) in two base configurations — H-base (cylindrical objects) and X-base (spherical). Gripper mass ~252–256 g; operates at +85/−25 kPa; grip time ~5 s. [src:05-pneumatic-soft-gripper]

Max in-flight payload **217 g** (exceeds prior 100–150 g class); static grip up to 330 g. H-base: 100% success on cylinders ≤200 g. Landing success: 100% flat surface, X-base 60% on 10° tilt. [src:05-pneumatic-soft-gripper]

Autonomy outsourced to VICON + NMPC — no onboard perception. Indoor/static only. Air-leak-by-design limits reuse rate. Complementary design point to the tendon-foam system above: pneumatic + rigid airframe + landing-gear dual-use vs. tendon + soft airframe + vision-onboard. [src:05-pneumatic-soft-gripper]

## Gripper-mechanism taxonomy

From the Frontiers 2021 review [src:07-grasping-perching-review] — six classes (grasping half only; perching mechanisms go to [[aerial-perching]]):

1. **Simple / underactuated grippers** — tendon-driven designs dominate; passive closing minimises actuation complexity.
2. **Arm-grippers** — articulated manipulator arms integrated with the airframe; see [[aerial-manipulation]] for control treatment.
3. **Tethered / net** — capture via thrown net or tether; suited to uncooperative or irregular targets.
4. **Reconfigurable frames** — airframe body IS the gripper; enables ~100% payload proportion.
5. **Adhesion** — gecko-inspired, electrostatic, magnetic, or vacuum; best suited to flat surfaces.
6. **Embedment / microspine** — spike or spine array embeds into soft/fibrous material.

Passive quick-release designs maximise payload-to-gripper-weight ratio (e.g. 56 N from a 0.5 kg hand; 9 g bistable gripper). TRL range 4–7 across the taxonomy. Hardware-design counterpart to the control-focused Ollero survey (see [[aerial-manipulation]]). [src:07-grasping-perching-review]

## Consumer gap

Three blockers for consumer deployment:

- **No zero-shot grasping.** Both demonstrated systems require per-object CAD models or pre-trained keypoint networks — unknown objects are out of scope. [src:03-soft-drone-grasping]
- **Payload ceiling.** Vision-onboard system tops at ~150 g; best pneumatic result is 217 g in-flight. Neither reaches typical consumer delivery payloads (500 g+). [src:03-soft-drone-grasping, 05-pneumatic-soft-gripper]
- **Mocap dependence for dynamic targets.** Fast (>0.5 m/s) or moving-target grasp currently relies on motion-capture infrastructure. [[drone-autonomy-state]] tracks how close onboard state estimation comes to closing this gap.

## Source
- `raw/research/aerial-manipulation/03-soft-drone-grasping.md` — npj Robotics 2024 paper: soft-drone tendon gripper with onboard vision, full benchmark numbers
- `raw/research/aerial-manipulation/05-pneumatic-soft-gripper.md` — arXiv 2311.00390: pneumatic landing-gear/gripper dual-use system, payload records
- `raw/research/aerial-manipulation/07-grasping-perching-review.md` — Frontiers 2021 review: grasping-mechanism taxonomy (TRL 4–7 survey)

## Related
- [[aerial-manipulation]] — parent topic; arm-gripper integration and control frameworks
- [[aerial-perching]] — perching half of the Frontiers 2021 review; grasping mechanisms enable perch-and-hold
- [[drone-sensors-for-autonomy]] — RealSense D455 + ResNet-18 stack; onboard perception gap
- [[visual-inertial-slam]] — T265 VIO used for state estimation in the tendon-gripper system
- [[drone-power-budget]] — ~3 min flight endurance constrains grasp mission radius
- [[drone-autonomy-state]] — dynamic-target grasp requires mocap today; tracks path to onboard closure
