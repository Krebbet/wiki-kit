# Precision Docking & Recharging

Closing the endurance loop for autonomous drones requires three sub-problems solved in sequence: dock relocalization, precision landing, and energy transfer. Industrial drone-in-a-box (DIB) systems have largely solved the first two via RTK GNSS + visual-fiducial landing (±cm), and ship with contact-charging as standard; consumer/indoor scale remains fragmented — low-cost IR-beacon guidance works at microdrone scale but no integrated stack exists. The gap between "lab-demoed precision landing" and "autonomous rearm without GPS" is the key unsolved problem for indoor home robotics.

---

## State of the art

### Industrial drone-in-a-box (outdoor, RTK-available)

- **DJI Dock 2 / DJI Dock (M30 series)** — *shipping at scale* — fully weatherproof station; RTK + downward visual-fiducial landing; contact-pad charging; automated lid; LTE/Wi-Fi uplink. Marketed for utility inspection, surveillance. (Note: vendor page — treat specs as marketing claims.) [`07-dji-dock2-specs.md`]

- **Skydio Dock X10** — *shipping at scale* — proprietary VSLAM for GPS-denied environments; ~45 min full recharge cycle; NDAA-compliant US manufacture; used in DoD perimeter security and infrastructure inspection. [`10-drone-in-box-deepdive.md`]

- **Hextronics Global** — *shipping at scale* — robotic arm performs battery swap in <90 s from a 6-pack magazine; DJI Mavic/M30-compatible; claimed "lowest cost per flight hour in industry." (Vendor claim.) [`10-drone-in-box-deepdive.md`]

- **Percepto Air Max, Easy Aerial SAMS-T, Sunflower Labs Beehive** — *shipping at scale* — range of DIB vendors from full-autonomy industrial to lightweight residential; all use RTK/GNSS + visual fiducial for precision landing; DIB market projected $3.38 B by 2032 at 13.7% CAGR. [`10-drone-in-box-deepdive.md`]

- **Autonomous powerline recharging (University of Southern Denmark)** — *demoed* — passive split-core current-transformer gripper on a Tarot 650 Sport; perches on live 3-phase overhead cable; electromagnetic grip + inductive energy harvest; demonstrated multiple contiguous hours of flight/charge/takeoff cycles in outdoor environment; guidance uses mmWave radar + visual camera; no RTK required post-acquisition. [`06-arxiv-2403-06533.md`]

### Precision landing — fiducial and IR approaches

- **Visual + IR fiducial landing (Reykjavik University)** — *demoed* — gimbal-mounted multi-payload camera (wide, zoom, IR) tracks AprilTag markers; achieves average landing error 0.19 m across 26 tests; max approach range 168 m horizontal / 102 m altitude with zoom camera; active (heated) IR AprilTags and passive high-reflectivity IR AprilTags demonstrated for day/night landing; no AGL or range sensor required. [`01-arxiv-2403-03806.md`]

- **AIRA (Columbia / Northwestern)** — *demoed* — low-cost (<$83, <18 g) 3-photodiode array on microdrone (Crazyflie-class); IR bulb at landing station; gradient-following guidance without pattern recognition; landing error <10 cm from up to 11.1 m away; works in partial NLOS / low-light; energy cost µW vs mW for camera methods. Targets palm-sized drones that cannot run vision compute. [`02-arxiv-2407-05619.md`]

### Wireless / inductive charging

- **Wireless drone docking station (University of Zagreb)** — *demoed* — three off-the-shelf magnetic-resonant WPT modules (12 V / 3 A each); series receiver configuration achieves 96.5 W output at 56.6% efficiency; pyramid-shaped dock eliminates coil misalignment by passive alignment; coil gap tolerance ≤10 mm. [`03-arxiv-2309-05433.md`]

- **Detuned SS-IPT with solenoid coils (Rowan University)** — *demoed* — solenoid ferrite coils in drone legs land on cylindrical transmitter on ground vehicle; 245 kHz switching, 88.2% efficiency at 48.2 W (well-aligned, 10 mm gap); detuned primary limits fault current at zero coupling; tolerates ±50 mm misalignment in Y, ±10 mm in X. [`04-arxiv-2405-12359.md`]

- **IPT general** — *shipping at scale (industrial)* — review notes near-field IPT can exceed 90% efficiency at high power (kW) but is severely sensitive to coil misalignment; a primary engineering challenge is SWaP-C tradeoff for onboard receiver; LCC/LCL topologies improve misalignment tolerance. [`05-arxiv-2511-13122.md`]

- **Capacitive power transfer (CPT)** — *speculated* — lower eddy losses, lighter couplers than IPT, but requires mm-scale air gap; not practical where landing height varies. [`05-arxiv-2511-13122.md`]

- **Far-field (laser, microwave)** — *speculated* — laser power transfer <15% efficiency; microwave <10%; safety / atmospheric attenuation unresolved for consumer scale. [`05-arxiv-2511-13122.md`]

### Consumer-indoor microdrone recharging

- **Crazyflie brushless contact-charging pad (Bitcraze)** — *demoed* — spring-contact pad integrated on main PCB of Crazyflie Brushless; replaces earlier Qi deck; requires motion-capture or Lighthouse positioning for precision landing; announced for limited prototype release; autonomous demo requires external positioning infrastructure. [`09-crazyflie-charging-pad.md`]

### Autonomous navigation to charging station (GPS-denied)

- SLAM-based path planning to dock (*speculated / lab-only*): SLAM builds map; A\* / Dijkstra finds dock; works in simulation and structured indoor environments; no deployed consumer product. [`05-arxiv-2511-13122.md`]

---

## Key gaps

1. **Dock relocalization without RTK/mocap at indoor scale.** All demoed consumer-scale precision landings (Crazyflie, AIRA) depend on external positioning (Lighthouse, mocap) or a known fixed IR beacon position. No system closes the loop using onboard SLAM alone to relocalize to a dock in an unknown/changed room.

2. **No integrated consumer docking stack.** Industrial DIB systems integrate guidance + landing + charging + rearm as a single product. Consumer equivalents do not: IR-beacon guidance (AIRA) is separate from wireless charging (Qi deck / Zagreb WPT), which is separate from dock-seek autonomy.

3. **Wireless charging misalignment at landing.** Near-field IPT/WPT requires ≤10 mm coil gap; passive alignment (pyramid dock, funnel legs) partially compensates but adds mass and constrains drone footprint. No lightweight, form-factor-neutral solution exists for sub-250 g indoor drones.

4. **Battery swap at small scale.** Robotic battery swap (Hextronics) requires mechanical precision exceeding what small-drone frames allow; contact-pad charging is slow (30–60 min for typical Li-Po); the time-to-rearm matters for room-coverage tasks.

5. **Dock detection in cluttered indoor environments.** Fiducial markers (AprilTag) require line-of-sight and adequate lighting; IR beacons saturate in sunlit rooms. No sensor modality reliably detects the dock across full home environment variability.

6. **SWaP-C of onboard receiver hardware.** For sub-100 g drones, adding IPT receiver coils + BMS + rectifier is prohibitive; AIRA's 18 g photodiode approach is the current lightweight extreme but gives only directional guidance, not full pose.

---

## Source

| File | ID / Vendor | Title | Notes |
|---|---|---|---|
| `raw/research/precision-docking-recharging/01-arxiv-2403-03806.md` | arXiv 2403.03806 | *A Precision Drone Landing System using Visual and IR Fiducial Markers and a Multi-Payload Camera* | Kyas et al.; avg 0.19 m error, zoom + IR AprilTags, 168 m range |
| `raw/research/precision-docking-recharging/02-arxiv-2407-05619.md` | arXiv 2407.05619 | *AIRA: A Low-cost IR-based Approach Towards Autonomous Precision Drone Landing and NLOS Indoor Navigation* | 3-photodiode, <$83, <10 cm error, microdrone-class |
| `raw/research/precision-docking-recharging/03-arxiv-2309-05433.md` | arXiv 2309.05433 | *Design and Validation of a Wireless Drone Docking Station* | Zagreb; 3-module WPT, 96.5 W / 56.6%, pyramid passive alignment |
| `raw/research/precision-docking-recharging/04-arxiv-2405-12359.md` | arXiv 2405.12359 | *Design and Analysis of a Detuned Series-Series IPT System with Solenoid Coil Structure for Drone Charging Applications* | Solenoid-leg coils, 88.2% @ 48.2 W, ±50 mm misalignment tolerance |
| `raw/research/precision-docking-recharging/05-arxiv-2511-13122.md` | arXiv 2511.13122 | *A Comprehensive Review of Advancements in Powering and Charging Systems for Unmanned Aerial Vehicles* | Survey: WPT types, BMS, fleet mgmt, research gaps |
| `raw/research/precision-docking-recharging/06-arxiv-2403-06533.md` | arXiv 2403.06533 | *Autonomous Overhead Powerline Recharging for Uninterrupted Drone Operations* | USD; passive gripper + current-transformer harvest; multi-hour outdoor demo |
| `raw/research/precision-docking-recharging/07-dji-dock2-specs.md` | vendor · DJI | *DJI Dock 2 — Specs* | Marketing page; JS-rendered, minimal extractable spec data; treat as claimed |
| `raw/research/precision-docking-recharging/09-crazyflie-charging-pad.md` | vendor · Bitcraze | *Crazyflie Brushless Charging Pad* | Contact-pad prototype; requires Lighthouse/mocap for landing; limited release |
| `raw/research/precision-docking-recharging/10-drone-in-box-deepdive.md` | editorial · DroneU | *Drone in the Box Systems in 2025: Deep Dive* | Vendor comparison; marketing-adjacent; treat autonomy claims as reported |

---

## Related

[[home-tidy-drone-prototype]] (parent — research assignment #2) · [[aerial-perching]] (perch-and-stare as alt endurance lever, no charging infrastructure needed) · [[drone-power-budget]] (why docking matters — typical 15–30 min Li-Po limits) · [[drone-autonomy-state]] (where dock-seek sits in the autonomy stack) · [[drone-sensors-for-autonomy]] (sensor suite for dock relocalization) · [[indoor-cluttered-slam]] (mapping prerequisite for GPS-denied dock-seek)
