# Aerial Perching

Perching converts a power-hungry hover into a near-zero-power wait — the single biggest endurance lever for consumer manipulation and observation drones. A drone that can land on a structure eliminates continuous thrust, cutting energy up to ~15× vs sustained hover and extending effective mission time from minutes to hours. See [[drone-power-budget]] for the endurance arithmetic.

## Perching mechanisms

Three physical modes cover the design space [07-grasping-perching-review.md]:

**Grasping-based** — claws and bird-inspired tendon mechanisms. Best fit: cylindrical substrates (branches, poles). Same end-effectors as [[aerial-grasping]]; grasping is the enabling sub-skill. TRL 4–6.

**Embedding-based** — insect-inspired microspines that hook rough planar surfaces (concrete, bark). Require only ~10% of UAV thrust to hold position against a wall. TRL 3–5.

**Attaching-based** — smooth or rough planar surfaces via:
- Dry/gecko adhesive (humidity degrades performance)
- Electrostatic / electroadhesive pads
- Vacuum suction
- Magnets (ferrous surfaces only)

Key quantitative: an electroadhesive pad held a 1.3 kg quadrotor on a ceiling for ~100 min; the same drone's battery supports only ~7 min of flight. That is the perch-and-stare case in one number. [07-grasping-perching-review.md]

TRL across mechanisms: 3–6. Demonstrations exist for each mode; autonomous attach-detach-reattach cycles remain limited.

## Bio-inspired and hybrid approaches

Ollero's group models approach trajectories on eagle prey-intercept guidance — closed-loop homing toward a landing target rather than waypoint sequencing [11-ollero-lecture2021.md].

**Perch-then-roll hybrid** locomotion: land, fold rotors, roll on wheels to reposition, re-launch. Demonstrated. Cuts energy vs flying between inspection points on a structure.

**Flapping-wing perching** prototype uses an event camera to suppress wing-beat motion blur during terminal approach — conventional frame cameras alias at flapping frequencies. Hovering on a flapping platform is described as "almost impossible"; perching replaces hover as the rest state. Full flapping-wing manipulation (ERC "Griffon" project) remains speculative.

## Why it matters for consumer use

**Perch-and-stare inspection/monitoring** — a drone perched on a tower, roof edge, or tree branch can watch, sense, or stream indefinitely (constrained only by battery self-discharge, not thrust). Replaces repeated flight sorties.

**Perch-then-manipulate** — parking on a surface before a manipulation attempt decouples the disturbance problem: the platform is mechanically grounded, so the arm does not fight hover dynamics. Relevant to [[drone-contact-and-door-tasks]] and [[aerial-manipulation]] more broadly.

**Mission extension arithmetic** — a 7 min hover budget becomes ~100 min of useful sensor time if the drone can attach. For consumer inspection products this changes the economics of battery swaps and operator attention.

## Gaps

- Onboard power electronics for electroadhesion are bulky; integrated solutions at sub-2 kg class undemonstrated.
- Humidity and surface contamination degrade dry and gecko adhesives unpredictably outdoors.
- Transition control (approach → attach → detach → re-hover) requires reliable contact detection; current autonomy is limited (requires [[drone-autonomy-state]] advances).
- Substrate diversity: most demos target a single surface type per mechanism; multi-surface perching on a single platform unsolved.
- Structural load during perch-then-manipulate: forces from the arm transfer into the attachment point; mechanism strength rarely co-designed with manipulation payload.

## Source
- `raw/research/aerial-manipulation/07-grasping-perching-review.md` — Frontiers 2021 review, perching half: three-mode taxonomy, electroadhesive 100-min ceiling experiment, energy comparison vs hover
- `raw/research/aerial-manipulation/11-ollero-lecture2021.md` — Ollero 2021 lecture: eagle-intercept guidance, perch-then-roll hybrid, flapping-wing perching with event camera

## Related
- [[aerial-manipulation]] — parent topic; perching is a prerequisite for stable contact tasks
- [[aerial-grasping]] — grasping end-effectors double as perching mechanisms on cylindrical substrates
- [[drone-power-budget]] — quantitative endurance case for perch-and-stare vs continuous hover
- [[drone-autonomy-state]] — autonomous attach/detach cycles require perception and transition control advances
- [[drone-contact-and-door-tasks]] — perch-then-manipulate strategy applies directly to contact tasks
