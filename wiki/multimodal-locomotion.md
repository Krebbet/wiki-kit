# Multi-Modal Locomotion — Drones That Also Drive, Walk, or Swim

Robots that combine flight with another medium (ground, water) to do effectual real-world work. The honest synthesis: **air-ground hybrids are a genuinely strong idea — they buy order-of-magnitude endurance gains because rolling costs ~10–40× less power than hovering — and a drone-with-arm-and-wheels (AirCrab) and an 8-mode morphing platform (M4) both physically exist.** The blockers to consumer use are the same recurring ones: the weight/cost overhead of dual-mode hardware, onboard perception (mocap-dependency), and autonomy. Air-water hybrids are far less mature. See [[air-ground-hybrids]] and [[air-water-robots]] for detail; the energy case is folded into [[drone-power-budget]].

## Design taxonomy *(synthesis; backbone: TU Delft survey, 64 prototypes, ~20 yr)*

- **Monolithic additive** — fixed airframe + an appended ground mechanism (passive/active wheel, cage, legs). Most prevalent; the most consumer-plausible (low parts count, off-the-shelf frames). *demoed*.
- **Monolithic adaptive (morphing)** — the body reconfigures between modes (collapsible frames, sprawling bodies, appendage-repurposing as in M4). Research-grade. *demoed*/*claimed*.
- **Multi-vehicle** — separate robots cooperate/dock (aerial carrier + ground bot). Research-grade.

## Why combine modes — the energy rationale

Flight is enormously more power-hungry per metre than rolling; combining modes lets a fixed battery cover far more ground or loiter far longer. Hard datapoints (detail + table in [[air-ground-hybrids]], cross-linked into [[drone-power-budget]]):

- Single passive wheel: **~77%** power saved sitting / **61%** rolling vs hover (foundational, minimal-hardware).
- Roller-Quadrotor: **~41× ground operating time**, ~3.8× lower J/m than flying.
- Tilt-Ropter (2026 SOTA): **92.8% ground-power reduction** vs flight.

This makes hybrid locomotion — alongside [[aerial-perching]] — one of the two principal levers against the 3–15 min flight-endurance ceiling that gates consumer manipulation/observation drones.

## Multi-modal + manipulation (the "arm + wheels" question)

- **AirCrab** — quadrotor + active wheel + 3-DoF arm; ground contact roughly *halves* manipulation error vs hovering (1.0 cm vs 2.0 cm RMSE). Closest existing proof of "land, roll, and do a precise task". Detail in [[air-ground-hybrids]], cross-linked to [[aerial-manipulation]] / [[drone-contact-and-door-tasks]].
- **M4 Morphobot** — appendage-repurposing landmark; one of its 8 modes is loco-manipulation. Research prototype (6 kg, ~3 kW in flight).

## Consumer-plausibility verdict *(editorial)*

- **Most plausible near-term:** additive **passive-wheel** designs — a ~$1 wheel for a 60–77% endurance gain, no extra actuators. Constraint: flat surfaces, can't self-land unaided.
- **Promising but heavier:** actively-driven-wheel / tilt-rotor hybrids (Roller-Quadrotor, Tilt-Ropter) — bigger capability, more mass/complexity, all still mocap-localised in the lab.
- **Landmark but not a product:** M4 (6 kg research platform); AirCrab (manual, two operators, 90 g payload).
- **Research curiosity:** air-water ([[air-water-robots]]) — ~200 s mode-switch, ~0.08 m/s swim.

## The recurring gap

Every consumer-blocking issue here is shared with [[aerial-manipulation]]: **dual-mode hardware adds mass that eats flight time**, and **onboard perception/autonomy is missing — nearly every demo is motion-capture-localised**. The mechanics work; the perception+autonomy+weight stack does not yet.

## Open items

- **LEONARDO** (leg-rotor bipedal-flying hybrid, Caltech) appears only via journalism in this corpus — no primary captured. Flagged as a follow-up if leg-rotor hybrids warrant deeper coverage.
- **Kovac aerial-aquatic** (Science Robotics 2022) capture failed (Spiral SPA returned nothing) — manual-download follow-up; air-water covered meanwhile by the safety survey + variable-stiffness platform in [[air-water-robots]].

## Source

- `raw/research/multimodal-locomotion/01-multimodal-survey.md` — TU Delft landscape survey (taxonomy, energy rationale, gaps)
- `raw/research/multimodal-locomotion/07-aircrab.md` — AirCrab aerial-ground manipulator (the arm+wheels bullseye)
- `raw/research/multimodal-locomotion/13-m4-morphobot.md` — Caltech M4, appendage-repurposing, 8 modes

## Related

- [[air-ground-hybrids]] — the energy spine + platform detail (passive wheel, Roller-Quadrotor, Tilt-Ropter, M4, AirCrab, FSTAR, LEONARDO)
- [[air-water-robots]] — amphibious hybrids (far less mature)
- [[drone-power-budget]] — hybrid locomotion as an endurance lever (energy figures land here)
- [[aerial-perching]] — the other principal endurance lever
- [[aerial-manipulation]] · [[drone-contact-and-door-tasks]] — where AirCrab/M4 loco-manipulation connects
- [[drone-autonomy-state]] — the mocap-dependency / autonomy gap, shared across topics
