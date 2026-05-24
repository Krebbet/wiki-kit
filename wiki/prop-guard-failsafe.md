# Prop Guards & Flight-Controller Failsafes (Build Reference)

Build-level companion to [[safe-indoor-flight]]: concrete physical-guarding hardware, the FAA energy ceiling a sub-250 g indoor craft must stay under, and the specific ArduPilot/PX4 failsafe parameters — plus why every "return home" action collapses to "land in place" without a position estimate.

For the survey-level design space (cages, tensegrity, compliant morphologies), see [[safe-indoor-flight]]; this page does not duplicate it.

---

## Physical guarding options

The goal indoors is to make rotor contact non-lacerating, since FAA Category 1 (the relevant target for a sub-250 g craft) gates on weight **and** absence of exposed rotating parts that lacerate skin (see Regulatory ceiling below). Options, lightest-to-heaviest:

- **Open prop + bumper rings** — minimal mass, minimal protection. Bumpers stop the airframe hitting a wall but leave the rotor disc exposed from above/below; *does not* clear the Category 1 laceration test. Reference baseline only.
- **Safety Rotor (contact-stop)** — *demoed* (UQ, Pounds & Deer, ICRA 2018). A passive plastic hoop spins around the rotor plane at a few tens of Hz, driven by hub friction on a low-friction bearing; IR reflectors on the hoop ping an IR detector. Any object reaches the hoop before the blade; hoop stall is detected and the motor is electrodynamically braked (windings shorted → generator → opposing torque). Measured: 0.0118 s trigger-to-deceleration; 90% of rotor KE dissipated in 0.0216 s, 99% in 0.032 s; full stop within ~0.06–0.077 s — rotor stopped before a 0.36 m/s "finger proxy" reached the rotor plane (open rotor destroyed the proxy). ~20–22 g and ~US$11–14 for four units retrofit. Passive-fail: power loss engages the brake. [05-spectrum-safety-rotor] [06-newatlas-safety-rotor]
- **Ducted / shrouded rotors** — *claimed/CFD* (MATEC, Kuantama & Tarca, 2017). A full duct (10 mm tip clearance, duct wall angle >90°, study used 105°) both guards the disc and adds thrust at high RPM: for a 406 mm two-blade rotor, ducting added 0.27–1.38 N (type α) to 0.73–2.1 N (types β/γ) above ~4000 rpm; below ~4000 rpm the gain is negligible. Mass budget: duct material must stay under ~140 gf/rotor (α) or ~214 gf/rotor (γ) to net positive on thrust-vs-weight. Ducting also lets the frame shrink (460 mm sq. usable at 5000 rpm vs. larger non-ducted). Takeaway for the build: a duct is a guard that *pays for itself* aerodynamically only at high disc loading, otherwise it is dead weight. [08-matec-ducted]
- **Coaxial ducted body (collision-tolerant form factor)** — *shipping* (Cleo Robotics Dronut X1). Two counter-rotating stacked rotors fully enclosed in a composite ducted body; rotors cannot harm bystanders nor be harmed by wall bumps; thrust-vectoring steering, 3D LiDAR obstacle avoidance, autonomous position hold; 425 g (15 oz), 165 mm tall, 4 m/s, ~12 min flight, US$9,800. Proof that a fully-enclosed indoor/GPS-denied craft exists commercially — but at ~425 g it is a Category 2/3 weight, not Category 1, and the price is industrial. [07-newatlas-dronut]

---

## Regulatory energy ceiling (FAA OOP)

The FAA Operation Over People final rule (14 CFR Part 107 subpart D) sets the only quantitative US precedent for flying over people. It targets outdoor commercial ops, not domestic indoor flight, but its thresholds are the de-facto safety yardstick for the prototype.

- **Category 1** — aircraft ≤ **0.55 lb (250 g)** including everything on board, **and** no exposed rotating parts that would lacerate human skin on impact. No declaration of compliance; operator self-certifies. This is the target the indoor build should aim for. [01-faa-oop-pdf]
- **Category 2** — > 0.55 lb, no airworthiness cert: impact must not exceed injury equivalent to **11 ft-lb** of kinetic energy from a rigid object, **and** no skin-lacerating exposed rotating parts; declaration of compliance + label required. [01-faa-oop-pdf]
- **Category 3** — > 0.55 lb: injury limit raised to **25 ft-lb**; additional operating restrictions (no open-air assemblies, site access controls). [01-faa-oop-pdf]

**Implication for a sub-250 g indoor craft:** weight alone clears Category 1, so the binding constraint is the *laceration* clause, not the energy number. That makes contact-stop (Safety Rotor) or a duct/cage the load-bearing safety feature — an open prop fails Cat 1 regardless of how light the craft is. The 11/25 ft-lb energy figures only become the governing constraint if the build grows past 250 g (as the Dronut-class form factor does).

---

## Flight-controller failsafes

Both stacks trigger a configurable mode change on radio loss, low battery, and (PX4) position loss. The critical indoor caveat: **every "return" action degrades to "land in place" when there is no usable position estimate.** Indoors there is no GPS; position comes from optical-flow / VIO / SLAM (see [[gps-denied-hover-land]] and [[slam-fc-integration]]). If that estimate is unavailable, RTL/SmartRTL/Return cannot run.

### ArduPilot (Copter)

- **Radio failsafe** — triggers after `RC_FS_TIMEOUT` (default 1 s) of lost RC, or throttle pulled below `FS_THR_VALUE`. Action set by `FS_THR_ENABLE`: 0 disabled, 1 RTL (falls back to **Land** if GPS position unusable), 3 always Land, 4/5 SmartRTL→RTL/Land. Disarmed → no action; armed-and-landed → immediate disarm; Stabilize/Acro at zero throttle → immediate disarm. `FS_OPTIONS` bitmask modifies behavior (e.g. continue landing). [02-ardupilot-radio-failsafe]
- **Battery failsafe** — requires a power module. Triggers when voltage < `BATT_LOW_VOLT` (default 10.5 V) for `BATT_LOW_TIMER` (default 10 s), or remaining capacity < `BATT_LOW_MAH` (~20% of pack is a good value). Action `BATT_FS_LOW_ACT`: 1 Land, 2 RTL-**else-Land-if-no-position**, 3/4 SmartRTL fallbacks, 5 Terminate (disarm — dangerous). Two-layer: set `BATT_CRT_VOLT`/`BATT_CRT_MAH` + `BATT_FS_CRT_ACT` (e.g. LOW=RTL, CRT=Land). Once tripped, only a reboot resets it. [03-ardupilot-batt-failsafe]

### PX4

- **Failsafe model** — most failsafes first enter **Hold** for `COM_FAIL_ACT_T` (operator override window), then escalate. Action ladder by severity: Warn → Hold → Return → Land → Disarm → Terminate; if multiple fire, the most severe wins. [04-px4-safety]
- **Manual control (RC) loss** — `COM_RC_LOSS_T` timeout; action chosen in QGC Safety (Hold/Return/Land/Disarm/Terminate); `COM_RCL_EXCEPT` exempts specified modes. [04-px4-safety]
- **Low battery** — three-level: `BAT_LOW_THR` (warn), `BAT_CRIT_THR` (Return), `BAT_EMERGEN_THR` (Land), action via `COM_LOW_BAT_ACT`. Flight-time-aware variants `COM_FLTT_LOW_ACT` (return when just enough charge for a safe return) and `COM_FLT_TIME_MAX` (hard max time). [04-px4-safety]
- **Position-loss failsafe** — the indoor-critical one. Triggers when the EKF position estimate is invalidated: a sensor-fusion timeout (GNSS, optical flow, VIO, airspeed all count as position sources) or horizontal inaccuracy over threshold. For multicopters in hover the action is to descend/land — there is no "return" without position. `EKF2_NOAID_TOUT` bounds how long it coasts with no aiding source. [04-px4-safety]
- **Geofence** — `GF_*` virtual cylinder/polygon; could bound a room, but is only as good as the position estimate feeding it (`GF_SOURCE`). [04-px4-safety]

---

## Build notes *(synthesis)*

- **Pick the failsafe action assuming you have no position fix.** Indoors, configure ArduPilot `FS_THR_ENABLE`/`BATT_FS_LOW_ACT` and PX4 `COM_RC_LOSS_ACT`/`COM_LOW_BAT_ACT` so that the *practical* outcome is **Land** — the RTL/Return options self-degrade to Land without GPS anyway, so do not rely on RTL behavior. A controlled descent-in-place is the indoor safe state. Validity of even "Land" depends on a working flow/VIO/SLAM estimate per [[gps-denied-hover-land]].
- **The laceration clause, not the energy number, is the gate** for a sub-250 g build. Spend the safety budget on making rotor contact survivable (Safety Rotor contact-stop, or a duct/cage) before chasing the 11 ft-lb figure, which only binds above 250 g.
- **Contact-stop vs. duct is a mass/thrust tradeoff.** Safety Rotor is ~22 g for four rotors and passive-fail-safe, but adds latency (~0.06 s stop) and needs reset after a trigger. A duct is heavier and only nets thrust above ~4000 rpm, but is fully passive with no reset. For a small low-RPM indoor rotor a duct is likely dead weight; contact-stop or a light cage is the better fit. Cross-check against [[payload-budget]] and [[drone-power-budget]].
- The Dronut X1 is the existence proof for a fully-enclosed GPS-denied indoor craft, but at 425 g / US$9,800 it is a reference point, not a build target.

---

## Source

- `raw/research/prop-guard-failsafe/01-faa-oop-pdf.md` — FAA *Operation of Small UAS Over People* final rule (14 CFR Part 107 subpart D); Category 1/2/3 weight, kinetic-energy (11/25 ft-lb), and exposed-rotating-parts laceration thresholds — https://www.faa.gov/sites/faa.gov/files/2021-08/OOP_Final%20Rule.pdf
- `raw/research/prop-guard-failsafe/02-ardupilot-radio-failsafe.md` — ArduPilot Copter Radio Failsafe docs; `FS_THR_ENABLE`/`FS_THR_VALUE`/`RC_FS_TIMEOUT`/`FS_OPTIONS`, RTL→Land-without-GPS fallback — https://ardupilot.org/copter/docs/radio-failsafe.html
- `raw/research/prop-guard-failsafe/03-ardupilot-batt-failsafe.md` — ArduPilot Copter Battery Failsafe docs; `BATT_LOW_VOLT`/`BATT_LOW_MAH`/`BATT_FS_LOW_ACT`, two-layer critical thresholds — https://ardupilot.org/copter/docs/failsafe-battery.html
- `raw/research/prop-guard-failsafe/04-px4-safety.md` — PX4 Safety Configuration; failsafe action ladder, RC-loss/low-battery/position-loss/geofence params (`COM_*`, `BAT_*`, `EKF2_NOAID_TOUT`) — https://docs.px4.io (Safety Configuration page)
- `raw/research/prop-guard-failsafe/05-spectrum-safety-rotor.md` — IEEE Spectrum on UQ Safety Rotor; passive contact-stop hoop, braking-latency/KE-dissipation figures, hot-dog/finger-proxy bench test — https://spectrum.ieee.org/quadrotor-safety-system-stops-propellers-before-you-lose-a-finger
- `raw/research/prop-guard-failsafe/06-newatlas-safety-rotor.md` — New Atlas on Safety Rotor; <0.06 s stop, ~20 g, ~US$11 retrofit cost — https://newatlas.com/safety-rotor/54777/
- `raw/research/prop-guard-failsafe/07-newatlas-dronut.md` — New Atlas on Cleo Robotics Dronut X1; coaxial ducted body, 425 g, GPS-denied/LiDAR, specs and price — https://newatlas.com/drones/dronut-x1-drone/
- `raw/research/prop-guard-failsafe/08-matec-ducted.md` — MATEC Web of Conferences (IMT Oradea 2017), Kuantama & Tarca, *Quadcopter thrust optimization with ducted-propeller*; CFD thrust gain vs. duct mass and RPM — https://www.matec-conferences.org/articles/matecconf/pdf/2017/40/matecconf_imtoradea2017_01002.pdf

---

## Related

- [[safe-indoor-flight]] — survey-level companion: cages, ducts, tensegrity/compliant collision-tolerant designs and OOP context at a higher level
- [[gps-denied-hover-land]] — why failsafe "return/land" depends on an indoor position estimate; the controlled-descent safe state
- [[slam-fc-integration]] — feeding flow/VIO/SLAM position into the flight controller so failsafes have a usable estimate
- [[home-tidy-drone-prototype]] — parent build; physical safety is the Phase-1 gating constraint
- [[payload-budget]] — guard/duct mass vs. usable payload
- [[drone-power-budget]] — duct thrust gain and contact-stop draw against the power budget
- [[indoor-obstacle-avoidance]] — avoid-contact layer that precedes survive-contact guarding
