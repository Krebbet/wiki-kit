# Cooperative Aerial Manipulation

Multiple drones combining force or dexterity to handle loads or tasks neither could manage alone. As of 2024 the field is overwhelmingly industrial/lab and motion-capture-bound; TRL 3–4 across schemes. The clearest consumer-scale cooperative glimpse is FlyCroTug — see [[drone-contact-and-door-tasks]].

## Cooperative schemes

Four architectures surveyed in arXiv 2403.14347 (2024):

**Cable-suspended multi-UAV lift** — most researched. Two to four quadrotors share a rigid payload via cables. Demonstrated outdoors up to **4 kg**; quasi-static trajectories, adaptive controllers reaching max **1.6 m/s²**. [src:02-cooperative-aerial-manip §3.1]

**Multi-DoF cooperative arms** — two hexarotors each carrying a 2–3 DoF manipulator arm act in concert. Lab/Vicon only; RRT\*+DMP motion planning emerging but onboard execution is nascent. [src:02-cooperative-aerial-manip §3.2]

**Rigid attachment** — quadrotors bolted or magnetically latched directly to payload faces. Up to **3.2 kg** demonstrated, lab setting. Simpler coordination but reconfiguration is manual. [src:02-cooperative-aerial-manip §3.3]

**Flexible payload** — six quadrotors mounted on a flexible ring structure, LQR control, slow transport (~**0.13 m/s**). Highest redundancy; lowest agility. [src:02-cooperative-aerial-manip §3.4]

## The motion-capture wall

Near-universal VICON/OptiTrack dependency is the shared blocker across all four schemes. [src:02-cooperative-aerial-manip §5] Onboard-only state estimation at manipulation accuracy remains unsolved — see [[drone-autonomy-state]] and [[drone-sensors-for-autonomy]]. Without marker-free pose feedback, none of these systems transfer to unstructured environments.

## Consumer relevance

Honest read: **industrial**, not consumer. Payload capacities overlap household-item weights, but platform cost far exceeds object value and no scheme operates without a motion-capture rig. Heavy-lift swarms are commercially viable only in logistics/construction contexts.

The more consumer-plausible cooperative direction is **anchored force multiplication** — the FlyCroTug paradigm (two palm-size drones, gecko + microspine adhesion, cooperative tug of 40× combined mass) rather than multi-UAV heavy lift. That line of work is teleoperated and small-scale, but requires no costly infrastructure. Details on [[drone-contact-and-door-tasks]].

Timeline estimate: 5–10 years minimum before cooperative aerial manipulation reaches consumer-safe indoor use, contingent on solving motion-capture dependency, wind robustness, simultaneous 3D-trajectory + precision, and unknown payload mass/inertia. [src:02-cooperative-aerial-manip §6]

## Gaps

- Motion-capture dependency — field deployment impossible without it
- Wind robustness untested for multi-UAV coupled dynamics
- Simultaneous 3D-trajectory tracking + manipulation precision unsolved
- Unknown payload mass/inertia at runtime degrades controllers
- Human-proximity safety unaddressed [src:02-cooperative-aerial-manip §6]

## Source
- `raw/research/aerial-manipulation/02-cooperative-aerial-manip.md` — arXiv 2403.14347, 2024 comparative survey of cooperative aerial manipulation schemes

## Related
- [[aerial-manipulation]] — parent topic; single-UAV manipulation context
- [[drone-contact-and-door-tasks]] — FlyCroTug cooperative door-opening detail
- [[drone-autonomy-state]] — manipulation autonomy maturity; mocap dependency documented
- [[drone-sensors-for-autonomy]] — onboard estimation gap blocking markerless cooperative work
