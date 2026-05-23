# Safe Human/Pet-Proximate Indoor Flight

Making a small indoor drone safe around people and pets requires simultaneously managing kinetic-energy budget, rotor-contact hazard, and failure-mode behaviour. Regulatory precedent exists (FAA Operation Over People final rule) but targets outdoor commercial ops, not domestic environments; no equivalent indoor-proximity standard exists. The hardware design space ranges from sub-250 g caged/shrouded platforms that trivially meet Category 1 thresholds to research-grade compliant and tensegrity morphologies that tolerate collisions but impose efficiency and cost penalties that have not yet been solved for consumer price points.

---

## State of the Art

### Regulatory framework (FAA OOP, 86 FR 4314)

- *shipping* **Category 1 (≤0.55 lb / 250 g, no exposed rotating parts that lacerate skin):** no FAA declaration of compliance required; operator self-certifies. Weight and rotor-exposure are the only hard gates. [06-faa-oop-final-rule]
- *shipping* **Category 2 (>0.55 lb, no airworthiness cert):** impact energy must not exceed injury equivalent to **11 ft-lb** from a rigid object; no exposed parts capable of lacerating skin; declaration of compliance required. [06-faa-oop-final-rule]
- *shipping* **Category 3 (>0.55 lb):** impact injury limit raised to **25 ft-lb**; additional operational access controls required. [06-faa-oop-final-rule]
- *shipping* **Prop-stop-on-contact acknowledged as a valid mitigation path:** FAA notes waivers have been issued for designs combining motor-stop technology with soft/abrasion-only (non-laceration) exposed props; final rule explicitly recognises "rotor brake or similar approach" as potentially effective, contingent on demonstrated effectiveness across all failure scenarios. Skydio is named as an advocate for this path. [06-faa-oop-final-rule]
- *shipping* **ASTM F38 / ISO 21384-3 performance baselines:** ASTM F2910 design spec and F3322 parachute recovery are the primary referenced means of compliance accepted by FAA for OOP. Controlled tests show injury risk below 10% for a 1.2 kg aircraft but ~70% for an 11 kg model; energy-absorbing geometries significantly reduce that risk. [09-drone-safety-standards]

### Ducted/caged/shrouded platforms (no-exposed-rotor approach)

- *shipping* **Flyability Elios 3:** full spherical cage with reversing motors enabling recovery from inverted flip; SLAM-based stabilisation (LiDAR + computer vision, "FlyAware"); rated IP-44; up to 12 min flight. Industrial inspection target, not domestic, but represents the mature cage-drone form factor. [08-flyability-elios3]
- *demoed* **EPFL Dronistics PackDrone:** foldable caged drone (90% volume reduction when folded); cage protects people, parcel, and drone; 0.5 kg payload; field-deployed on campus and rural routes. Demonstrated safe proximity hand-off. Morphing Cargo Drone variant (IEEE RA-L 2020, DOI 10.1109/LRA.2020.2993757) explicitly targets safe flight in proximity of humans. [07-epfl-lis-dronistics]
- *demoed* **EPFL GearQuad:** dense grid cage fully encloses arms and props during human-proximate flight; arms retract into cage, extend for cruise (>20% aerodynamic efficiency gain when extended). "Safest drone for in-hand delivery" per EPFL LIS; "cage protects even the fingers of small children." [07-epfl-lis-dronistics]

### Collision-tolerant morphologies

- *demoed* **Tensegrity aerial vehicles (UC Berkeley HiPeRLab, arXiv 2211.12045):** icosahedron tensegrity shell (six-rod, 20 cm rods) around a quadrotor; stiff-tensegrity design chosen to minimise buffer space and reduce vibration; survives high-speed impacts and can autonomously re-orient from arbitrary ground pose for re-launch. Validated in unknown forest environment with inertial-only navigation. [03-arxiv-2211-12045]
- *demoed* **EPFL tensegrity winged drone (SWIFT, Advanced Robotics Research 2025):** woodpecker-inspired fuselage (carbon fibre rods + elastic rubber cables replicating spongy bone) + shoulder tensegrity wing joints; head-on and wing-strike resilience validated in outdoor impact tests. Primarily fixed-wing for efficiency; impact contact forces do not propagate into electronics. [05-epfl-tensegrity-winged]
- *demoed* **SoBAR — Soft-Bodied Aerial Robot (ASU / arXiv 2204.13155):** pneumatically variable stiffness inflatable airframe; deflated for storage, inflated to fly; demonstrates repeated multi-direction collision recovery including head-on wall impacts. HFB bistable fabric grasper triggers on contact energy for perching. Thrust loss coefficient measured (max ~0.95 at arm-deflection angle); efficiency penalty not fully quantified against rigid baseline. [04-arxiv-2204-13155]
- *demoed* **Inflatable perching quadrotor (Univ. Tokyo, arXiv 2509.07496):** hybrid unilateral flexible arms (rigid during flight via locking mechanism, soft during perching via pneumatic inflation); perching on human forearm demonstrated; propellers stop ~0.2 s after arm contact confirmed (pressure reaches 19 kPa). First claimed aerial robot perching on a human body. [02-arxiv-2509-07496]

### Collision-tolerant survey findings

- *claimed* Survey of CT-MAVs (NTNU / UNR, arXiv 2212.03196) identifies taxonomy: rigid/stiff shrouds, elastic/compliant, origami-based, tensegrity, gimbal-based, bioinspired, expandable, morphing/foldable, bimodal aerial/ground, multi-linked. Sub-250 g elastic arthropod-exoskeleton-inspired design survives collisions up to 7 m/s. TIERCEL rigid CT-MAV: 6:1 thrust-to-weight, exploits contact to handle transparent/reflective surfaces. [01-arxiv-2212-03196]
- *claimed* Passive prop deformation ("Tombo" self-recovering propeller) as an alternative to full caging: prop deforms on collision and recovers. Not yet at consumer scale. [01-arxiv-2212-03196]

### The "Bumper Drone" compliant-morphology result

See [[drone-contact-and-door-tasks]] for the compliant-morphology contact result in the door-task context. That page notes physical-contact drones in lab settings but underscores that onboard semantic perception remains the deployment blocker — relevant to any indoor safety regime that depends on detecting people/pets rather than just surviving contact.

---

## Key Gaps

1. **No indoor-proximity safety standard.** FAA OOP governs outdoor over-people ops. No equivalent standard exists for confined domestic airspace where altitude is 0–3 m, obstacles are dense, and bystanders include pets. ASTM F38 / ISO 21384-3 are referenced by FAA but not scoped to indoor residential proximity. [06-faa-oop-final-rule, 09-drone-safety-standards]

2. **Fast electronic prop-stop at consumer price.** FAA acknowledges motor-stop-on-contact as a valid mitigation but requires demonstration "across all failure scenarios." The Tokyo inflatable-perching robot stops props in ~0.2 s after pressure confirmation — but that uses a pneumatic perch-detection trigger unavailable in a bare hovering drone. No consumer product has shipped a reliable prop-stop-on-proximity/contact that works for free-flight conditions, not perching. [02-arxiv-2509-07496, 06-faa-oop-final-rule]

3. **Soft-airframe efficiency penalty.** SoBAR shows thrust loss from arm bending (coefficient up to 0.95); inflatable structures require onboard pneumatics adding weight and complexity. No published paper quantifies the flight-time cost of compliant morphology vs. rigid baseline at matched mission profile. Tensegrity shells add structural mass but EPFL/Berkeley results suggest minimal flight-time impact — not yet validated at consumer-tier battery/motor combinations. [04-arxiv-2204-13155, 03-arxiv-2211-12045]

4. **No animal-specific hazard data.** All injury-threshold research (11 ft-lb / 25 ft-lb categories; blunt-impact test methods) is calibrated against human skin and human Abbreviated Injury Scale. Pet-specific data (cat eye anatomy, dog ear sensitivity, bird fragility at proximate rotor wash) is absent from the literature. [06-faa-oop-final-rule, 09-drone-safety-standards]

5. **GPS-denied fail-safe reliability.** ISO 21384-3 defines return-to-home, controlled descent, and geofence enforcement as standard fail-safe modes — all GPS-dependent. Indoors, drones rely on VIO/SLAM-based localisation; link-loss or sensor failure fail-safe logic for GPS-denied environments is not standardised and not validated at consumer tier. Elios 3 uses LiDAR SLAM and offers "Return-to-Signal" along recorded trajectory — a professional solution with no consumer equivalent. [08-flyability-elios3, 09-drone-safety-standards]

---

## Source

| File | Source | Title | Notes |
|------|--------|--------|-------|
| `raw/research/safe-indoor-flight/01-arxiv-2212-03196.md` | arXiv 2212.03196 | *Collision-tolerant Aerial Robots: A Survey* | Taxonomy of CT-MAV designs; elastic, tensegrity, origami, morphing |
| `raw/research/safe-indoor-flight/02-arxiv-2509-07496.md` | arXiv 2509.07496 | *Flexible Morphing Aerial Robot with Inflatable Structure for Perching-based Human-Robot Interaction* | First perch-on-human demo; prop-stop timing data |
| `raw/research/safe-indoor-flight/03-arxiv-2211-12045.md` | arXiv 2211.12045 | *Design and control of a collision-resilient aerial vehicle with an icosahedron tensegrity structure* | Stiff tensegrity quadrotor; re-orientation controller; forest validation |
| `raw/research/safe-indoor-flight/04-arxiv-2204-13155.md` | arXiv 2204.13155 | *A Soft-Bodied Aerial Robot for Collision Resilience and Contact-Reactive Perching* | SoBAR inflatable airframe; thrust-loss characterisation; perching |
| `raw/research/safe-indoor-flight/05-epfl-tensegrity-winged.md` | EPFL infoscience (2025) | *Collision-Resilient Winged Drones Enabled by Tensegrity Structures* | SWIFT woodpecker-inspired winged drone; fuselage + wing-joint tensegrity |
| `raw/research/safe-indoor-flight/06-faa-oop-final-rule.md` | FAA 86 FR 4314 (gov) | *Operation of Small Unmanned Aircraft Systems Over People — Final Rule* | **Regulatory primary.** Category 1–4 thresholds; kinetic energy limits; prop-stop language |
| `raw/research/safe-indoor-flight/07-epfl-lis-dronistics.md` | EPFL LIS (vendor/lab) | *Dronistics — Human-Friendly Drone Delivery System* | PackDrone cage; GearQuad retractable-arm dense cage; field deployments |
| `raw/research/safe-indoor-flight/08-flyability-elios3.md` | Flyability (vendor) | *Elios 3 — Digitizing the inaccessible* | Commercial caged inspection drone; SLAM stabilisation; Return-to-Signal fail-safe |
| `raw/research/safe-indoor-flight/09-drone-safety-standards.md` | Kite Compliance / kitecompliance.ai | *Inside the Flight Envelope: How Safety Standards Shape Drone Design* | ASTM F38 / ISO 21384-3 overview; injury-risk data by mass; parachute compliance path |

---

## Related

- [[home-tidy-drone-prototype]] — parent research assignment; safe proximity flight is a prerequisite for any domestic autonomous tidy drone
- [[drone-contact-and-door-tasks]] — Bumper Drone and compliant-morphology contact results; all indoor contact tasks rely on lab motion-capture, not onboard safety systems
- [[aerial-manipulation]] — grasping mechanics that interact with compliant airframe design tradeoffs
- [[drone-autonomy-state]] — onboard sensing stack; GPS-denied localisation directly sets fail-safe reliability bounds
