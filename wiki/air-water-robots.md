# Air-Water Robots

Aerial-aquatic hybrid drones exist as lab prototypes (TRL 3–4) capable of crossing the air-water interface, but the underlying physics conflict is severe enough that consumer viability is years away. Two 2024 papers illustrate where the field stands: a safety-framework survey (Kovac group) cataloguing why the problem is hard, and a diving-beetle-inspired mechanism demonstrating one concrete — if slow — answer.

## The Core Conflict

Flight and submersion want opposite things. Aerial efficiency demands low structural density and high lift-to-drag; neutral buoyancy underwater demands the inverse. Kinematic viscosity jumps ~15× at the air-water interface, producing violent deceleration during any plunge-dive entry. Propellers optimised for air deliver roughly 5% efficiency underwater; acoustic noise from spinning rotors also disturbs aquatic fauna and corrupts hydroacoustic sensor data. No single propulsion architecture handles both regimes without compromise. [evidence: `02-aerial-aquatic-safety-survey.md`, arXiv 2410.23722]

## Transition Strategies

Three transition archetypes have been identified [02]:

- **Plunge-diving** (fixed-wing): high entry speed, high impact loads — sensor-damage and contamination risk severe.
- **Seamless/multicopter**: gentler entry but propeller noise is ecologically disruptive and corrupts acoustic data.
- **Belly-landing** (animal-inspired, e.g. gannet/kingfisher): potentially lowest impact, but untested at robot scale.

A four-criterion design framework structures the trade-space: **Efficiency** (dual-mode energy), **Safety** (low ecological impact), **Embodied Automation** (VTOL + thrust-vectoring eliminates hand-launch; fixed-wing cruise range 2–10 km), **Adaptability** (morphing structures, e.g. folding wings). The Kovac-group prototype reached hover-only demonstration — no full entry/exit field cycle completed. [evidence: `02-aerial-aquatic-safety-survey.md`, maturity: TRL 3–4]

## A Mechanism Answer: Variable-Stiffness Arms

A diving-beetle-inspired platform uses gallium-alloy arms that are rigid during flight and melt to flexible rowing paddles underwater (~200 s heating time), driven by cable-actuated paddles rather than rotors to sidestep the underwater propeller efficiency problem. [evidence: `06-aerial-aquatic-varstiff.md`, arXiv 2409.09572]

Honest numbers:

| Parameter | Value |
|-----------|-------|
| Peak swim speed | 77 mm/s (0.077 m/s) |
| Flight endurance | 15.3 min (1550 mAh 6S) |
| Mass | 1.732 kg |
| Waterproof depth/duration | 500 mm / 70 min |
| Mode-switch latency | ~200 s |

The 200 s heating latency is a severe operational constraint. Transition control was deferred — no entry/exit cycle data collected. Flexible-arm flight stability under disturbance is unaddressed. Single-battery must serve both heating and motor loads simultaneously. [maturity: TRL 3]

The two papers are complementary: `02` frames *why the problem is hard*; `06` answers one slice of the impact/efficiency problem with a specific mechanism, while honestly exposing how much remains unsolved.

## Open Gaps

- GPS-denied underwater positioning and communications: unsolved at useful range.
- Dual-mode energy budget: no published system-level measurement accounting for heating, propulsion, and sensors across a full air-water-air mission cycle — see [[drone-power-budget]].
- Ecosystem impact of repeated interface crossings: under-studied.
- Full transition control loop (entry + underwater nav + exit): no field demonstration in either paper.
- Autonomous operation underwater (GPS-denied): blocks any practical deployment — see [[drone-autonomy-state]].

**Note:** Kovac et al., *Science Robotics* 2022 (the landmark air-water crossing paper) could not be captured — Spiral SPA returned nothing. Flag for manual download as a priority source gap.

## Consumer Relevance

Near-zero today. Plausible someday use-cases: autonomous lake/reservoir water-quality sampling, shoreline search-and-rescue, coastal habitat survey. Realistic pipeline: 5–10 years of research before anything approaching a deployable system, longer before consumer form-factor. The physics conflict is not an engineering oversight — it is fundamental.

## Source
- `raw/research/multimodal-locomotion/02-aerial-aquatic-safety-survey.md` — arXiv 2410.23722 (2024, Kovac group); safety/design framework survey for aerial-aquatic robots, transition taxonomy, four-criterion framework, prototype hover-only demo
- `raw/research/multimodal-locomotion/06-aerial-aquatic-varstiff.md` — arXiv 2409.09572 (2024); diving-beetle-inspired gallium-alloy variable-stiffness arms, swim/flight performance numbers, TRL 3 prototype

## Related
- [[multimodal-locomotion]] — parent topic; air-water crossing is a specific instance of cross-domain locomotion
- [[air-ground-hybrids]] — sibling hybrid class; shares the dual-propulsion energy trade-off problem
- [[drone-power-budget]] — dual-mode energy budget (heating + propulsion + sensors) is an open measurement gap
- [[drone-autonomy-state]] — GPS-denied underwater autonomy is the primary autonomy blocker for this class
- [[visual-inertial-slam]] — GPS-denied positioning, the aerial analogue to the unsolved underwater-localization problem
