# Sensor Mount — 2-DOF Tilt + Z-Lift Actuation (≈2026 USD)

**What this is:** the actuator-hardware buy-list and design for giving the rover's **sensor head** (the SVPRO
stereo camera + RPLIDAR C1 2D LiDAR) **two new degrees of freedom** on top of the existing rover yaw:

1. **Tilt** — pitch the sensor head up/down so the camera/LiDAR can look *up at high surfaces* (countertops,
   shelves, tabletops), not just straight ahead.
2. **Z-lift (vertical displacement)** — raise/lower the whole sensor head so it can rise to get a good view of
   what's on those high surfaces.

This is the **companion actuator spec** to [[land-rover-v1-build-guide]] (which now has a *§11* section that
folds these two axes into the build) and to [[land-rover-v1-rig]] (the fixed-mount BOM this extends).

> 🔴 **The load-bearing difficulty is NOT the actuators — it's that the sensor pose becomes a variable the
> mapping pipeline has to read every frame.** This is a **mapping robot**: every captured frame is tagged with
> the sensor's pose, and `data/calib/rig_geometry.json` currently encodes a *fixed* 7 cm LiDAR-above-camera
> offset. The moment the head tilts and lifts, that file stops being a constant and becomes a **function of the
> two actuator states** (`tilt_deg`, `lift_mm`). So the hard requirement on *every* component below is:
> **the tilt angle and the lift height must be KNOWN and REPEATABLE to good precision, readable per frame.**
> That forces **closed-loop / absolute-position / encoded** actuators — *not* open-loop hobby parts you can't
> read back. Each option below states its feedback/repeatability story explicitly. (Calibration implications in
> §D; rig-geometry change in §E.)

> ✅ **AS-BUILT (finalized 2026-06-18) — read this first.** The buy-list below was a *design/options* study; the
> rover's actual 2-DOF head was specced from it with two refinements. **The as-built truth is
> [[land-rover-v1-build-guide]] §11**; this page is retained for the *rationale/trade-offs* behind each choice.
> Finalized parts (≈$143):
> - **Tilt:** Feetech/Waveshare **STS3215** bus servo (unchanged) — but driven through the **Waveshare Bus Servo
>   *Adapter (A)*** (a passive UART↔bus bridge, no MCU, 9–12.6 V), **not** the ESP32 *HAT*.
> - **Z-lift:** **MKS SERVO42C** — an *all-in-one closed-loop servo-stepper* (NEMA17 + FOC driver + 14-bit encoder
>   + STM32, 7–28 V). It **replaces** the separate "closed-loop NEMA17 **+ TMC2209**" below — there is **no TMC2209**.
>   On a **T8 lead-screw + MGN12H 300 mm rail**, homed to an optical endstop.
> - **Controller:** **ONE** — the rover's *existing* ESP32 drives wheels + tilt (UART→adapter) + lift (step/dir),
>   on one WiFi/UDP endpoint. (The old plan's "HAT as head controller / TMC2209 on its GPIO" is superseded.)
> - **Buy the SERVO42C "+Motor" bundle, not the "PCBA" SKU** (PCBA = board only, no motor).


---

## TL;DR

- **Tilt: use a serial-bus servo with a built-in 12-bit magnetic absolute encoder** — the **Feetech/Waveshare
  STS3215-class** servo (~$10–30). It reports its own angle back over the same TTL wire that commands it
  (position/speed/load/temperature), so "what angle am I at?" is a register read — exactly the per-frame pose
  readout the mapping needs, with no extra sensor. A plain hobby PWM servo is the wrong tool: you command it but
  **cannot read it back**, and its ±1–2° slop is unmodelled. (Sources: RobotShop/Amazon/Waveshare STS3215.)
- **Z-lift: a lead-screw + closed-loop (encoder) stepper on a linear rail** is the precision/repeatable pick.
  A lead screw is **non-back-drivable** (the head doesn't sag under its own weight when power is cut) and
  **homing to a limit switch gives an absolute zero**; step-counting from that home gives height to ~0.05 mm.
  Use a **closed-loop NEMA17** (encoder on the motor) so missed steps are caught, and a **TMC2209** driver for
  *silent, low-vibration* motion (vibration blurs frames — the project's #1 enemy). A potentiometer-feedback
  12 V linear actuator is the cheaper/simpler alt but coarser and lower-precision.
- **Controller:** the rover's **existing ESP32** runs both new axes and publishes `{tilt_deg, lift_mm}` telemetry
  alongside the existing motor teleop. *(As-built: tilt goes over UART through a passive **Bus Servo Adapter (A)**;
  lift is a self-contained **MKS SERVO42C** on step/dir — see the AS-BUILT banner. The HAT + TMC2209 option below
  was the original design.)*
- **Baseline build total ≈ $150–210** on top of the existing rover. Cheaper ≈ $90–120 (hobby-grade, accept
  coarser pose). Nicer ≈ $300–380 (NEMA17 closed-loop + MGN12 rail + bus servo + absolute encoders).
- **The real cost is integration, not parts:** stereo/LiDAR-to-actuator calibration, per-frame pose tagging,
  cable management across a moving Z axis, and re-validating the vibration gate ([[land-rover-v1-rig]] §3) with
  a *taller, moving* mast. Budget the engineering, not the BOM.

---

## (A) Component CATEGORIES — functional blocks + the "known repeatable pose" story

There are six functional blocks: **(1) tilt mechanism, (2) Z-lift mechanism, (3) motor driver, (4) controller/MCU,
(5) position feedback, (6) structure + cable management + power.** Feedback (5) is woven into (1)/(2) because the
*choice* of actuator usually *is* the feedback story.

### A1. Tilt (pitch) mechanism

| Option | How it satisfies "known + repeatable pose" | Trade-offs |
|---|---|---|
| **★ Serial-bus servo w/ built-in absolute magnetic encoder** (Feetech STS3215 / Waveshare ST3215, 12-bit/0.088° magnetic encoder) | **Reads its own absolute angle back over TTL** — position/speed/load/temp feedback on the same wire that commands it. Per-frame readout = a register poll. **This is the right answer.** ~0.1° resolution; absolute (knows angle on power-up after one-key midpoint set). | ~$10–30. Metal-gear backlash is small but non-zero (model it once). 7.4 V/12 V variants. Needs a bus driver board (A4). Hold-torque continuous → mild heat. |
| Hobby PWM servo + **external AS5600 magnetic encoder** on the tilt axis | The servo is open-loop, but a **$6 AS5600 12-bit absolute encoder** on the pivot shaft gives an independent, *absolute*, contactless angle read (I²C/PWM). Pose is known from the *encoder*, not the servo command. | Cheaper servo, but you wire + read a separate sensor and mount a diametric magnet on the shaft. More parts, more calibration. Servo slop is irrelevant *because you read the encoder*, not the command. |
| Hobby PWM servo, command-only (no feedback) | **Fails the requirement.** You command an angle; you cannot *read* the achieved angle. ±1–2° unmodelled error per frame → corrupts the pose tag. | Cheapest, smallest. **Do not use for a mapping head** — only acceptable if pose precision genuinely doesn't matter (it does here). |
| Brushless gimbal motor + AS5600 (FOC) | Smoothest, zero-cogging, vibration-friendly *if* well-tuned; AS5600 gives absolute angle. | Overkill: needs an FOC driver (SimpleFOC/ODrive-class) + tuning. Continuous hold torque is weak unless geared. Reserve for a "nicer" build only if vibration on a hobby servo proves limiting. |

**Read-out (A1):** the bus servo with its **built-in absolute encoder is the clean pick** — it *is* the feedback
solution, one wire, ~$10–30. Everything else either bolts a separate encoder on (AS5600 route) or fails the
readback requirement (command-only PWM).

### A2. Z-lift (vertical displacement) mechanism

| Option | How it satisfies "known + repeatable pose" | Trade-offs |
|---|---|---|
| **★ Lead-screw (T8) + closed-loop stepper, on a linear rail, homed to a limit switch** | **Home to a limit switch → absolute zero; step-count from home → height to ~0.05 mm.** Closed-loop encoder on the motor catches any missed steps so the count never silently drifts. **Non-back-drivable** lead screw = head holds height with power off (no sag, no creep between frames). The repeatability gold standard. | ~$30–80. Slowish (T8×8 → 8 mm/rev). Needs a home cycle at power-up. Stepper *vibration* must be tamed (→ TMC2209 driver, A3). |
| Belt-driven Z (MGN12 rail + stepper, 3D-printer-style) | Same home-switch + step-count absolute story; faster than a lead screw. | Belt **stretch/backlash** is a pose-error source (worse than a screw); **back-drivable** → needs the motor energized or a brake to hold height (head can sag when idle). Use only if lift speed matters more than hold. |
| 12 V linear actuator w/ **built-in potentiometer** feedback | The potentiometer gives an **absolute** stroke read (analog → ADC); telescoping, self-contained, non-back-drivable gearbox holds position with power off. Simple. | ~$130–160. **Coarser** (pot linearity/noise → typ. ±0.5–1 mm, sometimes worse) and lower resolution than an encoded screw. Bulky/heavy; fixed stroke. Good *cheap-and-simple*, not *precise*. |
| Scissor lift / rack-and-pinion mast | Mechanically compact (scissor) or tall-reach (mast). | Both add **backlash + flex** (the moving sensor wobbles → vibration/pose error). Hard to instrument for absolute height. **Not recommended** for a precision mapping head. |

**Read-out (A2):** **lead-screw + closed-loop stepper + limit-switch home** is the repeatable, non-sagging,
high-resolution pick. The **potentiometer linear actuator** is the legitimate *cheaper/simpler* fallback if you
accept ±0.5–1 mm height error. Belt-Z, scissor, and rack-mast all add backlash/flex that fights the vibration gate.

### A3. Motor driver

| Option | Notes |
|---|---|
| **★ TMC2209** (for the lift stepper) | **Silent, 256-microstep interpolation → low vibration** (StallGuard sensorless-homing bonus). Vibration blurs frames — this is why TMC2209 over a noisy A4988/DRV8825. 3.3 V/5 V logic → ESP32-compatible. ~$5–9. |
| **Bus Servo Driver HAT / board** (for the tilt servo) | The Waveshare Bus Servo Driver HAT integrates an **ESP32 + the RS485/TTL bus-servo circuit**; it both drives the STS3215 *and* reads its feedback, and ships with Wi-Fi/web + open-source demo. ~$26. Doubles as controller (A4). |
| (Closed-loop integrated stepper) | A NEMA17 with **integrated driver + encoder** (all-in-one) removes a discrete driver but costs more (~$40–70) and usually wants 24–48 V. Tidy for a "nicer" build. |

### A4. Controller / MCU

The rover already runs an **ESP32 motor-teleop firmware** over UDP/JSON ([[land-rover-v1-build-guide]] §6). The
2-DOF head adds one more controller responsibility: **command both axes and publish `{tilt_deg, lift_mm}` in the
telemetry stream** so each captured frame can be pose-tagged.

- **★ Recommended:** the **Waveshare Bus Servo Driver HAT (integrated ESP32, ~$26)** runs the tilt servo natively
  and adds GPIO for the lift stepper's STEP/DIR + the limit switch — one board, both axes, same Wi-Fi/UDP idiom.
- Alt: keep the *existing* drive ESP32 for motors, add a **second small ESP32/Arduino** dedicated to the head
  (cleaner separation, one more WiFi endpoint or a UART link). Either way the head controller must timestamp and
  emit the pose at ≥ the capture rate (30 fps → emit at ~30 Hz, or latch-on-capture).

**Pose-readout requirement (all options):** the controller must make the *measured* tilt angle (from the servo's
encoder register, or the AS5600) and the *measured* lift height (step-count-from-home, or the actuator pot) available
to the laptop **per frame** — not the *commanded* values. Commanded ≠ achieved; the mapping must tag the achieved pose.

### A5. Position feedback (the requirement, made explicit)

| Feedback element | Axis | Gives | ~Cost |
|---|---|---|---|
| **Built-in 12-bit magnetic absolute encoder** (in the bus servo) | tilt | absolute angle, ~0.088°, over TTL | $0 (included) |
| **AS5600 12-bit magnetic absolute encoder** breakout | tilt (alt) | absolute angle, contactless, I²C/PWM | ~$6 |
| **Limit/home switch** (microswitch or optical) | lift | absolute zero reference for the step-count | ~$2–5 |
| **Closed-loop encoder on the lift stepper** | lift | catches missed steps → count stays true | included in closed-loop motor |
| **Built-in potentiometer** (in linear actuator) | lift (alt) | absolute stroke, analog | $0 (included) |

**Why absolute (or homed) matters:** a *relative* encoder loses its zero on every power cycle; the mapping needs
the pose to be correct the instant capture starts. The bus servo is absolute by construction; the lift gets its
absolute zero from a **home cycle to the limit switch** at power-up, then counts. The potentiometer route is
absolute too (just coarser).

### A6. Structure, cable management, power

- **Structure (mast + rail).** The Z-axis rides a **linear rail (MGN12)** or the lead-screw's own guide rods.
  **Stiffness is a hard constraint:** the existing rig mounts the camera "low, stiff, central" *precisely because
  motion blur kills the SLAM* ([[land-rover-v1-rig]] §3, the **vibration gate**). A tall moving mast is the
  *opposite* of that — so the rail/mast must be rigid, short as the reach allows, and the head foam-isolated.
  **The vibration gate must be re-run with the mast at full extension** (worst-case wobble), not just retracted.
- **Cable management across a moving Z axis (the sane-cabling problem).** Two sensor cables (camera USB, LiDAR
  USB/serial) plus the tilt-servo TTL must survive repeated raising/lowering without snagging, kinking, or
  yanking a connector (connectors are the failure point — [[land-rover-v1-rig]] §2b). Use a **small cable drag-chain
  (e-chain)** or a **service loop with a spiral wrap** anchored at top and bottom; keep a strain-relief P-clip at
  the head so a cable tug never loads the camera/LiDAR plug. The powered-hub-at-the-camera topology (P-001 fix)
  still applies — the hub can ride **on the moving head** (shortest sensor cables) with the long active tether as
  the service-loop'd run, *or* stay on the deck with a service loop up to the head.
- **Power budget.** Small, but **isolate it from the camera rail** (brownout discipline, [[land-rover-v1-rig]] §3 /
  [[drone-power-budget]]). Rough draws: a **bus tilt servo** ~0.2–0.5 A @ 7.4–12 V holding/moving (more on a
  stall); a **NEMA17 lift stepper** ~0.5–1.5 A @ 12 V while moving, ~idle when homed-and-holding (lead screw holds
  mechanically — you can even de-energize). A **12 V linear actuator** ~0.5–1.5 A while moving, ~0 idle. Budget
  **~1–2 A @ 12 V peak** for the head, fed from the motor/12 V rail (not the camera 5 V rail), with a bulk cap.
  This is well within the existing 3S LiPo; it shortens runtime only marginally (the head moves intermittently).

---

## (B) Concrete BUY LIST

Prices ≈2026 USD, verify before purchase (marketplace prices move). Style follows [[diy-active-ir-stereo-parts]]:
categorized, honest, with a "pick this." Three tiers — **cheaper**, **★ baseline (recommended)**, **nicer**.

### ★ Baseline — what to actually buy for the prototype

| # | Block | Pick | ~Price | Why this |
|---|---|---|---|---|
| **B1** | Tilt servo | **Feetech STS3215** serial-bus servo (12-bit magnetic encoder, TTL feedback, 19–30 kg·cm) — RobotShop / Amazon (RCmall) | **$10–29** | Built-in absolute encoder = per-frame angle readout on one wire. The SO-ARM100 ecosystem part → well-documented, cheap. |
| **B2** | Tilt+head controller | **Waveshare Bus Servo Driver HAT** (integrated ESP32 + RS485/TTL bus circuit, Wi-Fi demo) | **~$26** | Drives + reads the STS3215 *and* hosts the head firmware; same UDP idiom as the rover. Spare GPIO drives the lift stepper. **(AS-BUILT: replaced by the passive Bus Servo Adapter (A) ~$16, driven by the rover's existing ESP32 — see banner.)** |
| **B3** | Z-lift motor | **Closed-loop NEMA17 + T8 lead-screw** (integrated linear actuator, ~150–200 mm travel, encoder) — StepperOnline LMD17-class / Iverntech/MybotOnline T8 | **~$30–60** | Non-back-drivable screw (no sag); closed-loop catches missed steps; homed step-count → ~0.05 mm height. |
| **B4** | Z-lift driver | **TMC2209** stepper driver module | **~$6–9** | Silent + 256-microstep interpolation → *low vibration* (the blur enemy). StallGuard sensorless homing optional. **(AS-BUILT: dropped — the MKS SERVO42C has its own integrated FOC driver; no TMC2209.)** |
| **B5** | Home switch | Mechanical/optical **limit switch** (×1, +1 spare) | **~$3–5** | Absolute zero for the lift; home at power-up. |
| **B6** | Linear guide | **MGN12 200 mm rail + carriage** (Gulfcoast/Sienci) *or* the lead-screw's own guide rods | **~$15–25** | Rigid Z guidance so the head doesn't wobble (vibration gate). Skip if the actuator is self-guided. |
| **B7** | Cable mgmt | Small **cable drag-chain (e-chain)** + spiral wrap + P-clips | **~$10–18** | Sane cabling across the moving Z (camera USB + LiDAR + servo TTL). |
| **B8** | Structure/power | Printed/L-bracket head mount, foam isolation pad, 1000 µF cap, wiring off the 12 V rail | **~$10–20** | Stiff head mount; brownout isolation from the camera rail. |
| | | **Baseline total** | **≈ $120–180** | one tilt axis + one Z axis, both with absolute/homed pose readout |

> If the chosen NEMA17 actuator is **self-guided** (its own rods), you can drop **B6** and land near **$110–155**.
> Add a spare STS3215 and you're at the top of the range.

### Cheaper alternative (hobby-grade, coarser pose — ≈ $90–120)

| Block | Pick | ~Price | The compromise |
|---|---|---|---|
| Tilt | Hobby metal-gear PWM servo (e.g. MG996R-class) **+ AS5600 absolute encoder** ($6) on the pivot | ~$12–20 | Pose comes from the *AS5600*, not the servo command — still absolute, but more parts/wiring + a shaft magnet to mount. |
| Z-lift | **12 V linear actuator w/ built-in potentiometer** (150–200 mm stroke) | ~$130–160* | Self-contained, non-back-drivable, absolute pot read — but **coarser (±0.5–1 mm)** and bulky. *(\*This single part can dominate the tier; an open-loop stepper + AS5600-on-screw is a cheaper-but-fiddlier sub-alt.)* |
| Driver/controller | Existing ESP32 + a cheap motor/servo driver | ~$5–10 | Reuse the rover MCU; one more PWM/ADC channel. |
| **Honest note** | | | This tier *works* but trades pose precision (pot noise, servo-slop-via-encoder) and is **not obviously cheaper** once the pot actuator is counted — the baseline's bus-servo+stepper is better value. |

### Nicer alternative (best precision/smoothness — ≈ $300–380)

| Block | Pick | ~Price | The upgrade |
|---|---|---|---|
| Tilt | **Bus servo + redundant AS5600** on the output, *or* a geared brushless gimbal (SimpleFOC) + AS5600 | ~$40–70 | Cross-checked absolute angle / zero-cogging smooth tilt (vibration-friendly). |
| Z-lift | **Integrated closed-loop NEMA17 (driver+encoder onboard, 24–48 V) on an MGN12 lead-screw rail** | ~$70–120 | All-in-one closed loop, higher torque/speed, true missed-step recovery. |
| Driver | (Integrated — none separate) + a clean 24 V buck for the lift rail | ~$15 | — |
| Controller | Dedicated **ESP32-S3** head board, latch-on-capture pose timestamping | ~$10–15 | Tight time-sync of pose to frame (the per-frame tag done properly). |
| Structure | **Stiff MGN12 + machined head plate + e-chain + ferrites** | ~$60–90 | Maximum rigidity (best vibration-gate margin) + clean cabling. |
| **Total** | | **≈ $300–380** | only if the baseline's vibration/precision proves limiting |

---

## (C) Recommended baseline — honest verdict

**Buy the baseline: a Feetech/Waveshare STS3215 bus servo for tilt (its built-in 12-bit absolute encoder *is* the
per-frame angle readout) and a closed-loop lead-screw Z-lift homed to a limit switch (non-sagging, ~0.05 mm
repeatable height).** *(As-built refinement — see the AS-BUILT banner: the lift is an all-in-one **MKS SERVO42C**
that folds the NEMA17 + driver + encoder into one part, so **no separate TMC2209**; tilt is driven via a passive
**Bus Servo Adapter (A)** from the rover's **existing ESP32** — the single head controller — not a dedicated
Waveshare HAT.)* All-in ≈ **$120–180**.
The bus servo collapses "actuate + read angle" into one cheap part, and the lead-screw's home-then-count gives
absolute height without an expensive linear encoder. This is the cheapest build that *actually satisfies the
known-repeatable-pose requirement* — the cheaper hobby tier muddies the pose, the nicer tier is margin you buy
**only if** the vibration gate or precision proves limiting in practice. **Don't gold-plate the actuators; the
money and risk are in the integration (§D/§E), not the BOM.**

---

## (D) Calibration / integration implications — the load-bearing part

A moving sensor pose is the real cost. What the pipeline must now do:

1. **Per-frame pose tagging.** Today each frame implicitly carries the *fixed* rig geometry. With 2 DOF, the
   capture loop must record `(tilt_deg, lift_mm)` **measured** (encoder/home-count, not commanded) **for every
   frame**, time-synced to the image/scan. The head controller emits these at ≥ capture rate; the laptop latches
   the latest (or, better, the actuator state *at the capture instant*).
2. **`rig_geometry.json` becomes pose-DEPENDENT (§E).** The 7 cm LiDAR-above-camera offset and the absolute
   sensor heights stop being constants and become **functions of the two actuator states**.
3. **Calibrate the actuator-to-sensor transform once.** You need the static transforms from each actuator's
   measured value to the sensor optical frame: the tilt pivot's position+axis relative to the camera, and the
   lift carriage's travel direction+offset. Calibrate these once (e.g. tilt through known angles against a
   checkerboard / AprilTag at known height; lift through known travel against a tape/board). Backlash and the
   home-switch offset get measured here too. After that, every frame's full pose = `base_rover_pose ∘
   lift(lift_mm) ∘ tilt(tilt_deg) ∘ sensor_extrinsics`.
4. **SLAM/hloc consumption.** The relocalization stack ([[relocalization-method-bakeoff]], hloc) already wants
   accurate per-frame camera poses; feeding it the tilt+lift-corrected extrinsics is the *same* mechanism, just
   with two more joints in the chain. The LiDAR floor-map likewise needs the tilted scan-plane height
   ([[floor-map-sensing-options]]) — and note **tilting the 2D LiDAR off-horizontal changes what its scan plane
   intersects** (it no longer cuts a clean horizontal slice of the room), which the floor-map logic must account
   for (or only run the LiDAR floor-map at tilt=0).
5. **Time-sync is the subtle trap.** A moving head means a *stale* pose tag is a *wrong* pose tag. Latch pose to
   the capture instant; if the head is moving while capturing, either capture only when settled (simplest) or
   timestamp both streams tightly (the [[imu-vio-integration-reality]] two-clock sync lesson applies).

**Practical rule for v1:** **capture in "stop-tilt-lift-settle-then-grab" steps**, not while the head is in
motion. A settled head makes the pose unambiguous, sidesteps motion blur, and makes the per-frame tag trivially
correct. Continuous-motion capture is a later upgrade.

## (E) What changes in `data/calib/rig_geometry.json`

Today (fixed): a single constant `lidar_above_stereo_m: 0.07` plus a note that camera_height ≈
lidar_scan_plane_height − 0.07. With 2 DOF this file must gain the **pose-dependent** model — sketch:

```jsonc
{
  "lidar_above_stereo_m": 0.07,           // still the rigid camera↔LiDAR offset on the head
  "actuated": true,
  "tilt": {
    "axis": "pitch",
    "encoder": "stsbus_12bit_abs",        // or "as5600"
    "pivot_offset_m": [..],               // tilt pivot position in the head frame (calibrated, §D.3)
    "zero_deg_offset": 0.0,               // encoder reading at true-horizontal (calibrated)
    "sign": 1
  },
  "lift": {
    "axis": "z",
    "feedback": "stepcount_from_home",    // or "actuator_pot"
    "home_switch_offset_m": ..,           // height of homed (zero) position above rover deck (calibrated)
    "mm_per_step": ..,                    // = lead / (steps_per_rev * microsteps)
    "travel_range_m": [0.0, 0.20]
  },
  // camera/LiDAR absolute heights are no longer constants — derive per frame:
  // camera_height(tilt,lift) = deck + home_switch_offset + lift_mm + f_tilt(pivot_offset, tilt_deg)
  "note": "Per-frame pose = base ∘ lift(lift_mm) ∘ tilt(tilt_deg) ∘ sensor_extrinsics; see sensor-mount-2dof-tilt-lift.md §D"
}
```

The pipeline reads the *measured* `tilt_deg`/`lift_mm` for each frame and composes the transform. The existing
"scan plane passes above ~0.9 m counters" reasoning (the reason this whole DOF upgrade exists — to *also* look up
at counters with the camera) now varies with lift+tilt instead of being a single ~1.07–1.12 m constant.

## (F) Limitations / risks

- **Vibration is the headline risk.** A tall, moving mast directly opposes the "low/stiff/central" rule that the
  vibration gate enforces ([[land-rover-v1-rig]] §3). **Re-run the vibration gate at full mast extension.** Mitigate
  with a rigid rail, short reach, foam isolation, TMC2209 silent stepping, slow ramps, and **capture-while-settled**.
- **Backlash & sag.** Bus-servo gear backlash (small, model it) and any belt/scissor/rack route (large — avoid).
  The lead screw's non-back-drivability is the antidote to sag; a belt-Z would need a brake.
- **Cable fatigue across the moving Z.** Repeated lift cycles fatigue cables and stress connectors (the #1 USB
  failure mode, P-001). The drag-chain/service-loop + strain relief is not optional.
- **Pose-tag staleness.** A moving head with a stale pose tag silently corrupts the map. The capture-while-settled
  rule and tight time-sync are the guard.
- **Calibration drift.** The actuator-to-sensor transform can drift if the mount flexes or the home switch shifts;
  re-home each session and spot-check tilt zero against a known target.
- **Power/runtime.** Minor (~1–2 A @ 12 V intermittent) but must be **rail-isolated** from the camera 5 V to avoid
  reintroducing brownouts.
- **Tilted 2D LiDAR ≠ horizontal slice.** Off-horizontal tilt breaks the clean floor-plan slice; keep LiDAR
  floor-mapping at tilt≈0 or re-derive the intersected plane.

---

## Source

Web (≈2026, accessed 2026-06-16; verify prices before purchase — several marketplace prices are ranges):

**Tilt (serial-bus servo + encoder):**
- Feetech STS3215 12-bit magnetic-encoder serial-bus servo, position/speed/load/temp TTL feedback, ~$10–29 (vs Dynamixel XM430 ~$115) — robotshop.com (FeeTech 12V 30kg·cm STS3215); amazon.com (RCmall STS3215 + controller, B0F87XY6F2 / B0GHN8PYWZ); alibaba.com STS3215 listings.
- Waveshare ST3215 serial-bus servo (programmable 360° magnetic encoder, two-way feedback) ~$9–20; **Bus Servo Driver HAT (integrated ESP32 + RS485/TTL, Wi-Fi demo) ~$26** — amazon.com B0G2576KKN; waveshare.com bus-servo-driver-hat-a.htm + wiki.
- AS5600 12-bit magnetic absolute encoder breakout (PWM/I²C, for pan/tilt) ~$6 — amazon.com B09KGXW9B2 / B0981DM4S7; diymore.cc; ams-osram.com AS5600 datasheet.

**Z-lift (lead-screw stepper / linear actuator):**
- NEMA17 + T8 lead-screw integrated linear actuators (100–310 mm), RepRap Z-axis class — amazon.com (Iverntech B0B8DDG2X4, MybotOnline B07VGBSCRY, MOONS' B07L3P6ZXH); StepperOnline LMD17S13WF15-120 (with sensor); ebay.com 265358943378.
- Closed-loop NEMA17 stepper + encoder (catches missed steps), integrated-driver options 24–48 V — omc-stepperonline.com (17HS15-1504-ME1K, closed-loop kit); amazon.com B0DF4L19XZ / B0GDG4P8XN / UIM4247CA B0D4VMY28T; oyostepper.com.
- MGN12 200 mm linear rail kits (Z-axis) ~$15–25 — amazon.com B09HRJPHGB; sienci.com linear-guide-rails; gulfcoast-robotics.com MGN12 kits.
- 12 V linear actuator w/ built-in potentiometer feedback, 150–200 mm stroke, ~$130–160 — amazon.com B0FLBR1PJK / B0B34M9DP1; pololu.com #2341/#2353 (feedback actuators); electric-linear-actuators.com 200 mm w/ pot.

**Driver:**
- TMC2209 silent stepper driver (256-microstep interpolation, StallGuard sensorless homing, 3.3–5 V logic → ESP32) — circuitdigest.com TMC2209+Arduino; hackster.io TMC2209 guide; oshwlab.com 4-axis ESP32+TMC2209; forum.arduino.cc TMC2209 silent-driver thread.

Wiki cross-refs: [[land-rover-v1-build-guide]] (the build this modifies — §11), [[land-rover-v1-rig]] (fixed-mount
BOM + the vibration gate + P-001 USB/cable lessons), [[home-tidy-drone-prototype]], [[system-architecture]],
[[drone-power-budget]] (brownout/power discipline), [[floor-map-sensing-options]] (the RPLIDAR C1 on this head),
[[diy-active-ir-stereo-parts]] (buy-list style model), [[imu-vio-integration-reality]] (two-clock time-sync lesson),
[[relocalization-method-bakeoff]] (the hloc pose consumer). Rig calibration: `drone-prototype` repo
`data/calib/rig_geometry.json` (the file that becomes pose-dependent, §E).

*(synthesis — assembled 2026-06-16 from current vendor/marketplace listings + the wiki's rig/power/build pages;
several retail prices are given as ranges flagged "verify".)*

## Related

[[land-rover-v1-build-guide]] · [[land-rover-v1-rig]] · [[home-tidy-drone-prototype]] · [[system-architecture]] · [[drone-power-budget]] · [[diy-active-ir-stereo-parts]] (buy-list style model) · [[floor-map-sensing-options]] (the RPLIDAR C1 this head carries)
