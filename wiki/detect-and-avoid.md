# Detect and Avoid

Detect-and-avoid (DAA) is the capability enabling a UAS to satisfy the "see-and-avoid" obligation without a human pilot in the loop — the technical and regulatory crux of scalable BVLOS autonomy. Two primary sources inform this page: FAA NPRM 14 CFR Part 108 (*proposed rule*) and the ASTM F3442/F3442M-23 standard. **Important limitation: only the Scope section of ASTM F3442/F3442M-23 was captured in our source (source 12); performance thresholds, alerting logic, and specific numerical requirements are paywalled and NOT available. Claims about F3442 on this page are scope-level only.**

## ASTM F3442/F3442M-23 — Scope (from captured section)

Applicability:
- UA ≤25 ft maximum dimension, <100 kt airspeed.
- "Lower-risk" airspace: JARUS low/medium-risk categories; Class G/E below ~1200 ft AGL; Class B/C/D below ~400–500 ft (LAANC floor).
- Assumes no ATC separation service — DAA system is the sole conflict resolution mechanism.
- Day and night, VMC and IMC.

Traffic scope — crewed aircraft avoidance only:
- In-scope: rotorcraft, general aviation, crop dusters, ultralights, light sport aircraft (LSA), IFR and VFR traffic. Explicitly NOT transport-category aircraft in their primary operating environment.
- Out of scope (explicitly deferred): UA-to-UA separation, terrain avoidance, obstacle avoidance, bird/wildlife, weather avoidance.

Detection mix: cooperative (ADS-B In, electronic conspicuity) and non-cooperative (radar, CV, acoustic — architecture-agnostic).

Actors addressed: DAA system designers/integrators, sensor suppliers, UA developers, ground control station and flight-control system designers.

**The specific safety performance thresholds defined by F3442 are NOT in our source capture.** Any threshold numbers cited elsewhere should be verified against the full standard.

## FAA NPRM Part 108 — DAA Requirements (*proposed rule*)

From [[faa-part-108-bvlos]]:
- §108.825: DAA required.
- §108.195: cooperative detection (ADS-B Out, electronic conspicuity) required.
- Cat 5 (metro ≥2,500 people/cell) and Class B/C: equipage-agnostic, all-aircraft detection required — including non-cooperative.
- Standards pathway: ASTM F3442, RTCA ACAS sXu MOPS, ASTM F3548-21 (UTM). Performance-based; no mandated sensor.

**Explicit standards gap (NPRM fn.71):** ACAS sXu MOPS currently has no standardized drone-side non-cooperative detection sensor means of compliance. This is an unresolved gap in the regulatory pathway for Cat 5 urban operations.

DAA modalities acknowledged in practice by the NPRM: radar, cameras, ADS-B In. The NPRM does not mandate a specific sensor but the gap in non-cooperative MOPS means only the cooperative (ADS-B) path is fully standardized today.

The FAA also deferred updating §91.113 to make detect-and-avoid legally equivalent to see-and-avoid — leaving the legal foundation of fully autonomous avoidance unresolved at the time of NPRM publication.

## Synthesis *(synthesis)*

Cooperative detection (ADS-B In / electronic conspicuity) is largely a solved problem — standards exist (RTCA DO-260B, ASTM F3586), hardware is mature, and the regulatory path is clear. The open problem for autonomous BVLOS at urban scale is reliable non-cooperative detection: identifying aircraft that do not broadcast ADS-B (low-altitude VFR GA, ultralights, gliders, helicopters in certain operations). Candidate sensors — onboard radar, computer vision, acoustic arrays — exist in research and some commercial form, but no consensus performance standard (MOPS) for the drone-side sensor has been finalized. Until that gap closes, Cat 5 metro BVLOS operations requiring all-aircraft detection lack a complete standards-based compliance path.

This is the primary near-term technical and regulatory bottleneck for fully autonomous commercial BVLOS at scale. See [[drone-sensors-for-autonomy]] for the sensor modality options. See [[lidar-vs-vision-autonomy]] for the radar/LiDAR vs. vision-only tradeoffs relevant to non-cooperative detection.

The [[anduril-lattice]] sensor fusion stack (Sentry radar + optical towers) demonstrates a non-cooperative detection architecture relevant to the civilian DAA sensor gap, though it was not designed to meet FAA standards. [[skydio-autonomy-stack]] does not engage the DAA problem — its obstacle avoidance is designed for proximate obstacle avoidance, not airspace separation from crewed aircraft.

## Source
- `raw/research/autonomy-and-sensors/04-faa-part108-nprm.md` — FAA NPRM 14 CFR Part 108; DAA requirements, standards references, and the non-cooperative sensor gap.
- `raw/research/autonomy-and-sensors/12-astm-f3442-daa.md` — ASTM F3442/F3442M-23 Scope section only; performance thresholds paywalled and absent from capture.

## Related
- [[faa-part-108-bvlos]] — the regulatory framework that mandates DAA and identifies the non-cooperative gap.
- [[drone-sensors-for-autonomy]] — sensor modalities for meeting non-cooperative detection requirements.
- [[anduril-lattice]] — defence-origin radar + optical sensor fusion stack; non-cooperative detection approach relevant to civilian DAA sensor gap.
- [[drone-autonomy-state]] — where DAA bottlenecks fit in the broader autonomy capability timeline.
- [[lidar-vs-vision-autonomy]] — radar/LiDAR vs. vision debate directly relevant to non-cooperative DAA sensor choice.
