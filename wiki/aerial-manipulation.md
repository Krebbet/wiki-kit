# Aerial Manipulation — State and Consumer-Task Gaps

How drones physically interact with real objects: grasping, carrying, opening doors, pressing/contacting surfaces, perching. The honest synthesis: **the manipulation mechanics are largely solved in the lab — the blockers to consumer/home use are onboard perception, payload-to-weight, endurance, and safety-near-people, not the gripper or the arm.** This page is the overview/maturity map and the consolidated gap list; see [[aerial-grasping]], [[aerial-perching]], [[drone-contact-and-door-tasks]], and [[cooperative-aerial-manipulation]] for the detail.

## Field taxonomy *(synthesis; from the Ollero T-RO survey and the Frontiers grasping/perching review)*

- **Rigid serial arms** on multirotors — most studied; payload-to-weight and reaction-force control are the limiting factors (Ollero survey, *demoed*; industrial TRL ~5–6 for inspection).
- **Continuum / compliant arms** — dexterity in cluttered/constrained space (HKU "elephant trunk"; capture deferred — see Open items).
- **Soft / underactuated grippers** — adaptive grasp of varied objects; see [[aerial-grasping]].
- **Cable-suspended & cooperative** — multi-UAV lift; industrial-leaning, see [[cooperative-aerial-manipulation]].
- **Perching mechanisms** — claws, microspine, gecko/electro-adhesion; convert hover into a near-zero-power wait (up to ~15× endurance), see [[aerial-perching]].
- **Contact-tolerant morphology** — the body itself absorbs/uses contact (touch-and-go, surface push); see [[drone-contact-and-door-tasks]].

## Maturity map *(editorial)*

- **Demoed in the lab, consumer-relevant:** vision-only onboard grasping at 2 m/s of ~150 g objects ([[aerial-grasping]]); RL door-opening ([[drone-contact-and-door-tasks]]); a single platform (HI-ARM) doing door + room-to-room transport + perch + fine pinch ([[drone-contact-and-door-tasks]]); contact-tolerant surface push/touch.
- **Demoed but industrial-scope:** dual-arm petrochemical/bridge inspection, powerline manipulation (Ollero/GRVC — AEROARMS, AERIAL-CORE). Treated here as research foundation + gap evidence, not consumer content.
- **Field-deployed at scale:** none for consumer; closest is industrial inspection (TRL ~5–6).

## The consumer-task gap list *(synthesis — what blocks "carry an item from the kitchen to the family room" or "open a door")*

1. **Onboard semantic perception is the binding blocker.** Nearly every indoor manipulation demo (RL door-opening, HI-ARM household sequence, pneumatic-gripper grasps) localizes the target with external **motion-capture**. No mocap → no home use. Onboard handle/object detection is the missing layer.
2. **Payload-to-weight.** Demonstrated ceilings ~150 g (vision-only soft grasp) to ~450 g (HI-ARM); household objects are often heavier.
3. **Endurance.** 3–15 min flight; manipulation and the extra arm/gripper mass make it worse. Perching ([[aerial-perching]]) is the main mitigation.
4. **Safety near people.** Propeller hazard during close interaction is explicitly unsolved (Ollero names it directly).
5. **Generalization.** Per-object pretrained models; single door-handle geometries; controlled lighting/wind. No zero-shot.
6. **Autonomy & certification.** Most demos are scripted starts with fixed target poses; no autonomous navigate-to-object-then-act stack.

**Consumer reality:** the physics is proven; a home "fetch me that / open that door" drone is **plausibly 5–10+ years out**, gated by onboard perception + safety + endurance — not by the manipulator itself.

## Open items

- **Source deferred:** the HKU dexterous continuum-manipulator paper (Nature Comms 2025) failed automated capture (PMC reCAPTCHA + Europe PMC 500) — needs manual PDF download to ingest. Continuum/compliant ground is partially covered here via the Ollero survey and HI-ARM meanwhile.
- Note: **ETH ASL** (Siegwart — source behind the RL door-opening result) is a *different lab* from **[[eth-rpg-scaramuzza]]** (ETH RPG, Scaramuzza). Do not conflate.

## VLA-driven aerial manipulation (emerging) *(added 2026-05-17)*

A foundation-model subfield is crystallising around language-conditioned aerial manipulation — *demoed in simulation, pre-commercial*. Two complementary 2026 works: [[air-vla]] is the first systematic **benchmark** (mainstream VLA/VLM models on a sim UAV+7-DoF arm; best model ~42/100, heavy reliance on an external global camera) and [[dronevla]] a narrow **system PoC** (binary-action VLA, navigation real but the VLA validated only in sim). Net: VLA transfer to aerial manipulation is feasible in simulation but the maturity gap — onboard inference, sim-to-real, the perennial external-camera/mocap dependency — is unclosed. Reinforces this page's core gap: the manipulation isn't the blocker, the perception/autonomy stack is.

## Mechanism comparison — small-drone scope (palm-size to ~1 kg) *(added 2026-05-20 via /query)*

Consolidated view across this wiki's detail pages — which mechanism wins for which interaction goal at small/consumer scale. Numbers + caveats live on the detail pages; this is the map.

| Goal | Best mechanism | Exemplar | Detail |
|---|---|---|---|
| **Pick up a light object, fully onboard** (no mocap) | Soft tendon gripper + onboard vision | npj 2024 soft drone — 2.0 m/s vision-only, ~150 g | [[aerial-grasping]] |
| **Pick up a heavier object** (≤217 g) where you can land | Pneumatic soft gripper + landing-gear dual-use | arXiv 2311.00390 — 217 g in-flight (mocap-bound) | [[aerial-grasping]] |
| **Multi-task on one small platform** (transport + door + pinch + perch) | Hand-like multi-DOF tendon gripper | HI-ARM 556 g — broadest single-platform task set | [[drone-contact-and-door-tasks]] |
| **Attach to a surface / perch-and-stare** | Electroadhesive / microspine / gecko / claws (mode per surface) | Electroadhesive pad: 1.3 kg on ceiling ~100 min vs ~7 min hover (~15× endurance) | [[aerial-perching]] |
| **Manipulate an object heavier than the drone** | Anchor-then-tug, cooperative | FlyCroTug — palm-size, 40× body-mass via anchor (vs ~5× in flight), teleop | [[cooperative-aerial-manipulation]], [[drone-contact-and-door-tasks]] |
| **Touch / press a surface** (button, switch, contact-inspection) | Contact-tolerant compliant morphology | Bumper Drone 700 g — sustained wall-push with PID only | [[drone-contact-and-door-tasks]] |
| **Max payload-to-gripper-mass ratio** | Reconfigurable frame / passive quick-release | Frame-is-gripper: ~100% payload proportion; e.g. 9 g bistable gripper, 56 N from 0.5 kg hand | [[aerial-grasping]] |

The recurring blocker across the table (consumer-deployable for indoor pick-and-place is 5–10+ years out): every indoor object/handle/surface pose comes from external motion-capture in the captured corpus — the gripper isn't what's missing, **onboard semantic perception is**. The mechanisms most defensible *today* are those that don't need it: contact-tolerant morphology and anchor-then-tug under teleoperation in structured/known environments.

## Source

- `raw/research/aerial-manipulation/01-ollero-arm-survey.md` — canonical IEEE T-RO 2022 aerial-manipulation survey (taxonomy, gaps)
- `raw/research/aerial-manipulation/07-grasping-perching-review.md` — Frontiers 2021 grasping+perching hardware-design review
- `raw/research/aerial-manipulation/11-ollero-lecture2021.md` — Ollero 2021 lecture (post-survey updates, explicit gap list)

## Related

- [[aerial-grasping]] · [[aerial-perching]] · [[drone-contact-and-door-tasks]] · [[cooperative-aerial-manipulation]] — the detail pages
- [[drone-autonomy-state]] — manipulation autonomy lags flight autonomy; the mocap-dependency gap
- [[drone-sensors-for-autonomy]] — the onboard-perception gap that blocks consumer manipulation
- [[drone-power-budget]] — endurance ceiling that perching mitigates
