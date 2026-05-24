# GPS-Denied Hover & Precision Landing (Indoors)

Build reference for the two GPS-denied primitives a Phase-1 indoor drone needs: **stable position hold** (optical-flow + downward rangefinder, ArduPilot FlowHold/Loiter) and **precision landing onto a marker** (ArduPilot precision-landing fed by a fiducial detector). Carries this project's **fiducials-first** thesis: a printed AprilTag/ArUco pad + optical-flow hold is a far lower-risk V1 than LiDAR-SLAM-based landing.

## Optical-flow position hold

An optical-flow sensor is a downward-facing mouse-style camera: it compares pixel shifts between frames to estimate horizontal *velocity* over the ground, giving position hold without GPS or a Lidar downward beam. The most common chip is the **PMW3901** (e.g. Holybro PMW3901, UART); newer 2-in-1 boards (MicoAir **MTF-01P**, 12 m lidar) combine flow + ranging on one board to cut wiring. Both ArduPilot and PX4 have native drivers. *(shipping at scale — hobby/commercial flight stacks)*

Raw flow is pixel rate; converting to ground speed requires distance-to-ground, so **flow is almost always paired with a downward rangefinder** (ToF / lidar). Hard limits: works best **under ~3 m** over *textured* surfaces; smooth/polished floors, repeating-pattern carpet, water and featureless surfaces confuse it; very dark or direct-sun lighting degrades it (typical indoor light is fine); and with no GPS to bound it, the estimate **drifts over time** — good for short holds and landing, not long missions. *(claimed — unmannedtech primer)*

### ArduPilot modes

- **FlowHold** — holds position on flow *alone*, no Lidar required: the flow sensor estimates both height-above-surface and velocity. Pilot flies lean angles directly (PosHold-like); releasing sticks brakes to a stop. ArduPilot **explicitly warns** it often wobbles / holds unstably and recommends adding a rangefinder + regular **Loiter** instead. Soon after takeoff or on large height changes it wobbles while relearning height. Tuning: `FHLD_BRAKE_RATE`, `FHLD_FILT_HZ`, `FHLD_FLOW_MAX`, `FHLD_QUAL_MIN` (below this quality it degrades to AltHold), `FHLD_XY_P/I/IMAX/FILT_HZ`. *(shipping — but ArduPilot-deprecated for serious use)*
- **Loiter / PosHold** — the recommended GPS-denied hold: flow for `VELXY`, **downward rangefinder for height**, barometer for `POSZ`. Downward rangefinders are auto-used in any height-controlled mode (AltHold, Loiter, PosHold) up to `RNGFNDx_MAX`, then it hands off to baro. *(shipping)*

### Sensor setup (PMW3901, ArduPilot)

Wire flow to a UART, then: `FLOW_TYPE=1` (PMW3901 serial), `SERIALx_PROTOCOL=9` (optical flow / MAVLink), `RNGFNDx_TYPE` = your ToF device, `FLOW_ENABLE=1`. Allow non-GPS nav and disable GPS arming checks (uncheck "All"/"GPS", keep the rest). Compensate mount offset with `FLOW_POS_X/Y/Z`.

**EKF3 source switch (the core GPS-denied config):** `EK3_SRC1_POSXY=0` (None), `EK3_SRC1_VELXY=5` (OpticalFlow), `EK3_SRC1_POSZ=1` (Baro), `EK3_SRC1_VELZ=0`, `EK3_SRC1_YAW=1` (Compass), `EK3_SRC_OPTIONS=0`. Also set `EK3_FLOW_DELAY` per sensor. Calibrate flow scalars (`FLOW_FXSCALER`/`FYSCALER`) in-flight (`RCx_OPTION=158`) with GPS, or via log (`OF.flowX` vs `OF.bodyX` vs `IMU.GyrX`); a 3-position switch on `RCx_OPTION=90` lets the pilot hot-swap GPS↔flow EKF sources. **Safety mechanism:** with flow as the only horizontal source the vehicle won't climb above `RNGFNDx_MAX` in position-controlled modes (else EKF failsafe trips out of range). First test flights need ≥15 m clear space — bad flow estimates send it to max lean angle fast. *(shipping — ArduPilot docs)*

### Matek 3901-L0X (flow + short-range lidar)

The **MatekSys 3901-L0X** is a light flow sensor with an integrated short-range ST VL53L0X-class lidar, talking **MSP** over serial. Mount lens-down, arrow forward, on the underside. Config: `FLOW_TYPE=7` (MSP), `FLOW_FXSCALER=-800`, `FLOW_FYSCALER=-800`, `SERIALx_PROTOCOL=32` (MSP), `SERIALx_BAUD=115`. Onboard lidar (optional): `RNGFND1_TYPE=32` (MSP), `RNGFND1_MAX=1.2`. **Caveat (ArduPilot):** the onboard lidar is *very* short range — they strongly recommend a separate longer-range lidar for the height channel and note the onboard one especially struggles outdoors. For an indoor sub-2 m drone the integrated lidar may suffice, but range headroom is tight. *(shipping — Matek hardware; ArduPilot-supported)*

## Precision landing / docking onto a marker

ArduPilot **Precision Landing** and **Precision Loiter** use an external "landing target" reference to hit **centimetre-level** accuracy on touchdown or hover. Target position arrives via MAVLink `LANDING_TARGET` messages from a companion computer, or from the IR-LOCK sensor + beacon + rangefinder. In **Land** mode (or final stage of **RTL**) a detected target overrides the GPS solution for the final descent. *(shipping — ArduPilot core feature)*

**Quick start params:** `PLND_ENABLED=1` (reboot to expose the rest), `PLND_TYPE` selects source (1=MAVLink `LANDING_TARGET`, 2=IR-LOCK, 3=Gazebo, 4=SITL, 0=off), `PLND_ORIENT`/`PLND_YAW_ALIGN` for mount, `PLND_CAM_POS_X/Y/Z` + `PLND_LAND_OFS_X/Y` for offsets. Loss/retry behaviour: `PLND_STRICT` (0=just land, 1=retry then land, 2=retry then hover — for boats/water), `PLND_RET_MAX`, `PLND_RET_BEHAVE`, `PLND_ALT_MIN/MAX`, `PLND_XY_DIST_MAX`. Precision **Loiter** reuses the same backend — enable via aux-function switch **39** — and is the recommended way to confirm tracking before committing to a landing. Note: a valid horizontal position estimate + steady attitude + clean rangefinder are prerequisites; poor EKF or noisy AGL degrades it.

### Marker paths (companion-computer / fiducial)

- **BlueOS Precision Landing extension** *(ArduPilot 4.7+)* — a downward camera gimbal lands on an **AprilTag** pad. Print a `tag36h11` tag (online generator works); install the extension on the companion computer, set AprilTag family/ID + FOV, "Test Detection", then "Run" (persistent). FC side: `PLND_ENABLED=1`, `PLND_TYPE=1` (MAVLink). **A rangefinder is required.** Debug via dataflash `PL` messages: `Heal`=link health, `TAcq`=target acquired, `pX/pY`=offsets. *(demoed — official extension)*
- **Raspberry Pi + OpenCV ArUco** (Landmark lab-notes, engineering-grade DIY) — Pi cam → OpenCV ArUco → compute bearing (and optionally pose) → `LANDING_TARGET` at 10–50 Hz (start 20 Hz) over MAVLink2 → ArduPilot. **Angles-only + downward rangefinder** is the recommended simple pipeline (`position_valid=0`, rely on rangefinder AGL); full-pose (`solvePnP` → `tvec` → body-frame x,y,z, `position_valid=1`) is the tighter, more complex option. Dict `DICT_6X6_100`/`5X5_100`, tag printed at known side (e.g. 0.20 m) on rigid matte board with white border; ArUco *board* (grid) extends acquisition altitude. Serial: `SERIALx_PROTOCOL=2` (MAVLink2) + matching baud; `RNGFND1_ORIENT=Down`. *(demoed — DIY guide)*
- **Landmark Precision Landing System** — commercial camera module + fiducial pad, cm-level landing/hover, sold as a kit (LandmarkLanding.com). The plug-and-buy version of the above. *(shipping — commercial product)*
- **goodrobots/vision_landing** — open-source monocular ArUco/AprilTag precision-landing for ArduCopter; **no rangefinder needed** (distance from marker pose estimation). Multi-marker concentric pads (large tag for high lock-on → smaller tags at low altitude, with a debounce filter `markerhistory`/`markerthreshold` to stop oscillation between tags). Aruco recommends `ARUCO_MIP_36h12`; smaller-grid dicts (e.g. AprilTag `16h5`) give larger elements → better from altitude. **Discontinued / academic-interest only — the authors explicitly warn it behaves dangerously; learning reference, not flight code.** *(claimed — abandoned project)*
- **IR-LOCK** — dedicated `PLND_TYPE=2` sensor + IR beacon path, rangefinder-assisted; the non-vision-companion route. *(shipping — commercial sensor)*

### IR-fiducial research (long-range / nighttime, day+night)

Kyas/Springer/Guðmundsson (arXiv 2403.03806) land a DJI Matrice 350 (H20T multi-payload camera + Raspberry Pi 4 / DJI Payload SDK) on AprilTag pads using a **gimbal-mounted, multi-payload camera** and a high-level search→approach→descend→recover **control policy**. Key idea: depend *primarily on the direction (pan/tilt) to the pad*, deliberately **avoiding AGL, range, marker size, and full 6-DoF pose** (whose orientation is ambiguous and error-prone). Results: 26 landings, **avg error 0.19 m**, visual+zoom from up to **168 m horizontal / 102 m altitude** (far beyond prior work). Novelty: **IR AprilTags** — an active *heated* tag and a *passive* unpowered high-reflectivity tag (reflects cold sky → reads dark) — enabling day **and** night landing without IR beacons, plus a search/re-acquisition policy that recovers when the pad is obscured. *(demoed — outdoor field tests, Iceland)*

Takeaway for an indoor build: the long-range/IR mechanics are out of scope, but two transferable lessons land — (1) **angles/direction to the marker is enough**; avoid brittle 6-DoF pose, matching the Pi+ArUco "angles-only + rangefinder" pipeline; (2) **a loss-recovery policy** (re-acquire instead of aborting) is what makes marker landing reliable, mirroring ArduPilot's `PLND_STRICT` retry logic.

## Build notes — fiducials-first *(synthesis / recommendation)*

For the [[home-tidy-drone-prototype]] Phase-1 (indoor stable hover + reliable takeoff/land, no GPS), the recommended V1 stack:

1. **Hold:** PMW3901 (or Matek 3901-L0X) optical flow + a downward rangefinder, EKF3 sourced `VELXY=OpticalFlow` / `POSZ=Baro`, flown in **Loiter** — *not* FlowHold (ArduPilot itself deprecates flow-only hold as wobbly). Sub-3 m indoor altitude and a textured floor are exactly flow's sweet spot; a smooth/polished floor is the main failure mode to design around.
2. **Land:** a **printed AprilTag/ArUco pad** + companion-computer detector (BlueOS extension if on ArduPilot 4.7+, else the Pi+OpenCV `LANDING_TARGET` path) feeding `PLND_ENABLED=1, PLND_TYPE=1`, **angles-only + downward rangefinder**.

**Why fiducials-first beats LiDAR-SLAM landing for V1:** a fiducial pad is a *single, unambiguous, high-contrast* target — detection is a solved CV problem (OpenCV ArUco/AprilTag), the ArduPilot ingest path (`LANDING_TARGET` → `PLND_*`) is shipping and well-documented, and the same printed marker doubles as the future dock for [[precision-docking-recharging]]. LiDAR-SLAM-based landing instead requires a full onboard map + global-localization + a designated landing region — strictly more compute, more failure surface, and more tuning, with no accuracy win at the pad ([[lidar-for-uav-autonomy]], [[visual-inertial-slam]]). This mirrors the project-wide pattern: every demonstrated indoor manipulation/landing system replaces an unsolved perception problem with a *known fiducial or mocap* — fiducials are the controlled, debuggable crutch. Markers de-risk localization *now*; full SLAM-based landing is a later removal of that crutch, not a V1 requirement. *(synthesis — this project's thesis)*

Sequencing within Phase-1: prove flow-Loiter hold first (it's the harder, drift-prone half), then bolt on precision-land/Loiter over a tag on top of a working hold — `PLND` needs a valid horizontal estimate to function, so the hold loop is the foundation.

## Source

- `01-ardupilot-optflow-setup.md` — ArduPilot optical-flow sensor testing/calibration + EKF3 source params + arming-check changes — https://ardupilot.org/copter/docs/common-optical-flow-sensor-setup.html
- `02-ardupilot-flowhold.md` — FlowHold mode (flow-only hold) + `FHLD_*` tuning + ArduPilot's wobble warning — https://ardupilot.org/copter/docs/flowhold-mode.html
- `03-ardupilot-matek-3901.md` — MatekSys 3901-L0X flow+short-range-lidar (MSP) wiring + params — https://ardupilot.org/copter/docs/common-mateksys-optflow-3901L0X.html
- `04-ardupilot-precland.md` — Precision Landing & Loiter: `PLND_*` params, target sources, loss/retry behaviour, MAVLink `LANDING_TARGET` + AprilTag — https://ardupilot.org/copter/docs/precision-landing-and-loiter.html
- `05-ardupilot-precland-blueos.md` — BlueOS Precision Landing extension (AprilTag, gimbal cam, ArduPilot 4.7+) setup + `PL` debug fields — https://ardupilot.org/copter/docs/precision-landing-blueos.html
- `06-ardupilot-precland-landmark.md` — Landmark commercial precision-landing system (camera module + fiducial pad) — https://ardupilot.org/copter/docs/precision-landing-landmark.html
- `07-landmark-aruco-blog.md` — engineering-grade Raspberry Pi + OpenCV ArUco precision-landing DIY guide (angles-only vs full-pose, `LANDING_TARGET`, param quick-sheet) — https://landmarklanding.com/blogs/landmark-lab-notes/ardupilot-precision-landing
- `08-vision-landing-gh.md` — goodrobots/vision_landing: open-source monocular fiducial landing (discontinued), multi-marker pads, dictionary trade-offs — https://github.com/goodrobots/vision_landing
- `09-ardupilot-rangefinders.md` — rangefinder landing page: downward rangefinders for altitude/precision-land, `RNGFNDx_MAX` handoff to baro — https://ardupilot.org/copter/docs/common-rangefinder-landingpage.html
- `10-fiducial-ir-arxiv.md` — Kyas et al., precision drone landing with visual + active/passive IR AprilTags, multi-payload gimbal camera, direction-only control policy (0.19 m avg error, 168 m/102 m) — https://arxiv.org/pdf/2403.03806
- `11-unmannedtech-optflow.md` — optical-flow primer: how flow works, PMW3901/MTF-01P, GPS-vs-flow regimes, ArduPilot setup, limitations — https://www.unmannedtechshop.co.uk/blogs/knowledge-base/optical-flow-sensors-drones-autonomous-indoor-flight

## Related

- [[home-tidy-drone-prototype]] — the Phase-1 indoor build this page is the GPS-denied-hover/land reference for
- [[precision-docking-recharging]] — the same printed marker becomes the recharge dock; precision-land is the docking primitive
- [[drone-sensors-for-autonomy]] — where optical-flow + rangefinder sit in the indoor sensor stack
- [[lidar-for-uav-autonomy]] — the heavier SLAM-based-landing alternative this page argues against for V1
- [[visual-inertial-slam]] — full vision-localization route; fiducials de-risk the localization problem ahead of it
- [[safe-indoor-flight]] — flow-Loiter hold + tethered first flights as part of safe indoor bring-up
- [[lidar-vs-vision-autonomy]] — the broader sensor-architecture conflict; fiducials-first is the landing-specific corollary
