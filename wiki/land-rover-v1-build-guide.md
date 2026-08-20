# Land-Rover v1 — Step-by-Step Build Guide

A beginner-friendly, do-this-then-that assembly walkthrough for the **v1 land rover** — the cheap
ground robot that carries the SVPRO stereo camera so it can drive itself around a mapped room. This
is the **build companion** to [[land-rover-v1-rig]] (which holds the *why* behind every part choice
and the full BOM); this page is the *how*, in order, with the reasoning for each step so you're never
wiring blind. *(synthesis — assembled from the rig spec, the `drone-prototype` rover firmware
`src/rover/esp32_motor_teleop.ino` + its README, and the parked v1-scope decisions P-001/P-003.)*

> **Read this first — what v1 actually is (honest scope).** v1's job is to prove ONE thing: *the
> laptop can drive the rover around the room over WiFi while the camera streams back for mapping.*
> To keep it cheap and fast, three things are **deliberately deferred** (all parked, all fine for a
> prototype):
> - **It drives skid-steer (tank-style), not true mecanum strafing.** The firmware sends one command
>   to the left wheels and one to the right — forward / back / spin-turn. Sideways strafing (the
>   reason mecanum wheels exist) needs 4 independent wheel commands + mixing — a firmware upgrade, not
>   a wiring one. You still *mount* mecanum wheels; they just roll like normal wheels for now.
> - **It's open-loop.** No wheel-encoder feedback yet, so "drive forward 0.5 m" drifts ±10–30% with
>   battery level and floor grip ([[land-rover-v1-rig]], parked **P-003**). Encoders are the first
>   upgrade.
> - **The camera is tethered to the laptop, not onboard.** All the SLAM compute stays on the laptop.
>
> If that framing is wrong for what you want, stop and say so *before* building (Commandment XIV).

---

## 0. The big picture — what you're building

Two independent signal paths share one battery. Burn this diagram into your head; every phase below
is just filling in one piece of it.

```
                          ┌─────────────────────  THE ROVER  ─────────────────────┐
                          │                                                        │
  ┌──────────┐  5 m USB   │   ┌────────────┐    USB     ┌─────────────┐            │
  │  LAPTOP  │◄═══════════╪═══│ powered hub │◄══════════│ SVPRO stereo│            │  ← PERCEPTION path
  │ RTAB-Map │  (tether)  │   │ (P-001 fix) │           │   camera    │            │    (camera → laptop)
  │  + hloc  │            │   └─────┬───────┘           └─────────────┘            │
  │          │            │         │ 5 V                                          │
  │  teleop  │──UDP WiFi──╪──►┌─────┴────┐   logic    ┌──────────┐  motor power    │  ← CONTROL path
  │  client  │  V,vx,wz   │   │  ESP32   │═══════════►│ TB6612   │═══► 4 motors     │    (laptop → wheels)
  └──────────┘            │   └──────────┘  (Dupont)  │ driver(s)│                 │
                          │         ▲                 └────┬─────┘                 │
                          │         │ 5 V                  │ 11.1 V                 │
                          │   ┌─────┴───────────────────────┴──────┐               │
                          │   │   3S LiPo  →  lever connectors      │  ← POWER       │
                          │   └────────────────────────────────────┘               │
                          └────────────────────────────────────────────────────────┘
```

**Why two paths?** The camera is a high-bandwidth sensor (full-res MJPG won't fit over home WiFi), so
it rides a wired tether straight to the laptop. The motors only need tiny velocity commands, so they
go over WiFi. Keeping them separate is what lets v1 skip an onboard computer entirely.

---

## 1. Lay out the parts & tools (10 min — don't skip)

Pull everything from the BOM ([[land-rover-v1-rig]] §"Exact product") onto the table and check it off.
The build stalls halfway if a connector or the soldering iron is missing. The **must-have tools**:

- **Soldering iron + solder + flux** — exactly *one* unavoidable solder job (driver headers + motor
  leads; Dupont jumpers can't carry motor current).
- **Multimeter** — the single most important tool here. You will verify **5 V and polarity before
  anything sensitive gets connected**. This is what stops the magic smoke.
- Wire strippers, flush cutters, precision screwdrivers (+ hex keys), zip ties, heat-shrink.

**Mental model of the parts:**
| Part | What it is, in one line |
|---|---|
| Chassis (Hiwonder 4WD mecanum) | The body + 4 geared motors + wheels |
| ESP32 | The tiny brain — talks WiFi, makes timing signals. **Cannot power motors itself.** |
| TB6612 driver | The "muscle relay" — takes the ESP32's weak logic signals + battery power, and actually pushes current through the motors |
| 3S LiPo (11.1 V) | The fuel tank. Respect it — LiPos can burn. |
| 5 V buck converter | Steps 11.1 V down to the 5 V the ESP32 wants |
| Powered USB hub + 5 m active tether | Gives the camera *local* clean 5 V and a reliable data path to the laptop (the **P-001** fix) |

---

## 2. Phase 1 — Assemble the chassis (mechanical)

Follow the **Hiwonder kit's own printed/online instructions** for the mechanical build — mounting the
4 motors in their brackets, pressing on the mecanum wheels, and stacking the deck plates. This guide
doesn't duplicate that (the kit does it well); two things that *matter for us*:

- **Mecanum wheel roller direction.** Each mecanum wheel has angled rollers. On a proper mecanum
  chassis the four wheels form an **"X" pattern** when viewed from above (front-left & rear-right
  rollers point one way; front-right & rear-left the other). Get this right now even though v1 won't
  strafe — so the future mecanum-mixing upgrade "just works." *Why: wrong roller orientation makes
  strafing physically impossible later.*
- **Leave the top deck accessible.** You'll be mounting the ESP32, driver, hub, and battery up there
  and re-checking wiring a lot. Don't permanently close it.

✅ **Done when:** all 4 wheels spin freely by hand, nothing rubs, the deck is solid.

---

## 3. Phase 2 — Prep the motor driver (the one solder job)

The TB6612 ships as a bare board with **loose header pins**. Solder the headers on, and solder the
**motor + power wires** to their pads (these carry real current — Dupont can't).

> 🔰 **New to soldering? Read §3a first — it's a ~20-minute skill and these joints are forgiving.** The single
> best prep is to skim one *photo* guide before you start a real joint:
> - **[SparkFun — How to Solder: Through-Hole](https://learn.sparkfun.com/tutorials/how-to-solder-through-hole-soldering/all)** — the best beginner photos of good vs bad joints.
> - **[Adafruit — How To Solder Headers](https://learn.adafruit.com/how-to-solder-headers)** — the breadboard-jig trick + step-by-step header photos.
> - **[SparkFun TB6612FNG Hookup Guide](https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide/all)** — this exact board's pinout/photos. *(A pre-soldered "with Headers" variant exists — but yours has loose pins, so you're soldering.)*
>
> **Practice on a spare header strip or scrap board first** — do 3–4 throwaway joints to find the rhythm before you touch the driver.

```
   TB6612FNG  (one board = TWO motor channels: "A" and "B")
   ┌─────────────────────────────────┐
   │ VM   VCC  GND  STBY              │   VM   = motor power  (→ 11.1 V battery)
   │ PWMA AIN1 AIN2 ...               │   VCC  = logic power  (→ ESP32 3V3)
   │ PWMB BIN1 BIN2 ...               │   STBY = enable       (→ ESP32 GPIO25)
   │ AO1 AO2   BO1 BO2                │   AO1/AO2 = motor A leads ; BO1/BO2 = motor B leads
   └─────────────────────────────────┘
```

### 3a. Soldering 101 (read if you're new)

**Tools & consumables:**
- **Temperature-controlled iron** with a **conical or small chisel tip ~1–2 mm** (about the width of a pad). A
  fixed-temp "pencil" iron works, but control is easier to learn on a dialed iron.
- **Solder: thin 0.6–0.8 mm rosin-core.** **Leaded 60/40** is the easiest for a beginner (melts lower, flows
  nicer); **lead-free** is safer but fussier — either is fine, just wash your hands after.
- **Damp sponge or brass wool** to wipe the tip, a **"helping hands"/vise** to hold the board, and **flux**
  (optional, but it really helps the high-current pads flow). Good light + a small fan to push fumes away.

**Set the iron to ≈325–375 °C (≈620–700 °F).** *If you see smoke rising off the solder, turn it down.*

**The core motion — per joint, ~2–4 seconds total:**
1. **Tin the tip:** melt a little solder on the tip and wipe most off — a shiny tip transfers heat far better
   than a dry one. Re-tin before each joint.
2. **Heat the joint, not the solder:** press the **side near the tip** against **both the pad and the pin at
   once** for ~1–2 s. Heating with the very point is slow and gives cold joints.
3. **Feed solder into the *joint*** (where pin meets pad), **not onto the iron** — ~1 cm of 0.7 mm wire per pin.
   It should melt instantly and **flow** around the pin, not sit in a ball.
4. **Pull the solder away first, then the iron.** Don't linger — too long melts the plastic header or loosens
   the neighbouring pins.

**What a good joint looks like (the #1 thing to learn):**

```
   GOOD                 COLD / STARVED        BLOB (too much)        BRIDGE (shorted)
   shiny cone, wets      dull, grainy ball     big round glob,        solder spans TWO
   pad + pin             that doesn't grip     pin barely wetted      pads = a short

        /\                    o                   ( O )                ___   ___
       /  \                  (ball on             (round)            |  x | x  |
      /____\ ← fillet         top of pad)         _______            |  x===x  | ← joined!
     ──┴──  pin             ___pad___             __pad__            |__|   |__|
```

A good joint is **shiny, concave, cone-shaped** — *"a volcano or Hershey kiss, not a ball or clump"* (SparkFun).
- **Dull / grainy / cracked** = a **cold joint** (didn't get hot enough) → reheat it until it flows and goes shiny.
- **A ball sitting *on top* of the pad without wetting it** = not enough heat or flux → add flux, heat the pad more.
- **Solder touching two pins** = a **bridge / short** → add flux and **drag the clean hot tip** across the gap, or
  soak it up with **solder wick**. Eyeball every adjacent-pad gap when you're done.

**Safety:** the tip is **~350 °C and burns instantly** — park it in its stand *every* time, never test heat by
touch. Don't breathe the fume plume (work in air, fan it away). **Wash your hands afterward**, especially with
leaded solder.

### 3b. The two jobs on this board

Two kinds of joint — do the easy one first to warm up:

1. **Header pins (logic side — easy).** Snap the strip to the right lengths (score + bend, or use pliers).
   **Use a breadboard as a jig:** push the header's long pins into a breadboard, sit the driver board on top so
   the short pins poke through the pad holes **dead vertical**, then solder. **Tack ONE pin at each end first**,
   check the board sits flat and the header is straight (reheat that one pin to nudge it if not), *then* solder
   the rest. This jig trick is what keeps headers from ending up crooked.
2. **Motor + power wires (high-current — needs more heat).** The **VM, GND, and motor-output pads
   (AO1/AO2, BO1/BO2)** connect to wide copper / the ground plane, so they **sink heat and the solder "blobs up"
   instead of flowing** — that's expected, not you doing it wrong. Give them **a second or two longer**, add a dab
   of **flux**, and **pre-tin both the wire end and the pad** before joining them. **Pre-tin stranded wire** so it
   doesn't fray. These carry the real motor current — that's why they're soldered, not Duponted.

**Why a driver at all?** The ESP32's pins put out a few milliamps at 3.3 V — nowhere near enough to
turn a 12 V geared motor. The TB6612 is an **H-bridge**: the ESP32 tells it *direction* (IN1/IN2) and
*speed* (a PWM signal), and the driver switches the full battery current to the motor accordingly.

> ⚠️ **Current caveat (real, from the rig spec).** The TB6612 is light-duty (~1.2 A/channel
> continuous). So in v1 we wire **one motor per channel** and use **both boards** — board 1 = left
> side (front-left on channel A, rear-left on channel B), board 2 = right side. Each side's two
> channels get the *same* command (see Phase 4), so the two left wheels always move together. *Why
> not parallel two motors onto one channel? That doubles the current through one H-bridge and cooks
> it on a stall.* If a driver ever gets hot or cuts out, that's its protection tripping — back off the
> speed cap, or fall back to the controller board included with the Hiwonder kit.

✅ **Done when:** every header pin is a **shiny cone** (no dull/grainy cold joints), there are **no bridges**
between adjacent pads (eyeball each gap), each board sits **flat and square**, and the motor + power wires are
solidly soldered to **VM/GND** and **AO1/AO2 · BO1/BO2** — confirmed with a **gentle tug test** (a good joint
won't budge).

---

## 4. Phase 3 — Power distribution (multimeter gates this phase)

Now we fan the battery out to three consumers. **Do this with the battery DISCONNECTED**, then test
before connecting the ESP32.

```
 3S LiPo ─►[Deans pigtail]─►[lever connectors]─┬─► VM of BOTH TB6612 boards      (motors, 11.1 V)
 (11.1 V, T-plug)                              ├─► 5 V buck converter ─► ESP32    (brain, 5 V)
                                               └─► powered hub feed  (+1000 µF 35 V cap across it) ─► camera
```

- The **1000 µF cap** across the hub feed is a small energy reservoir — it smooths the voltage dip
  when the motors yank current, so the camera's USB rail doesn't brown out mid-frame.
- **Lever (Wago-style) connectors** let you branch the battery to 3 places without soldering a power
  bus — easy to undo when something's wrong.

> 🔴 **THE MULTIMETER GATE — do not skip, do not connect the ESP32 until this passes:**
> 1. Connect the battery. Measure the **buck converter output**: it must read **5.0 V ± 0.2**.
> 2. Confirm **polarity** — red probe on the pin you'll feed to ESP32 5V, black on GND. A reversed
>    buck output kills the ESP32 instantly.
> 3. Only once both are correct, power off, then wire the buck's 5 V/GND to the ESP32's 5V/GND pins.
>
> *Why this gate exists: a mis-set buck or a swapped wire is the #1 way to destroy the board, and
> you can't see voltage — you have to measure it.*

✅ **Done when:** buck reads a stable 5.0 V, polarity verified, ESP32 powers on (its LED lights) from
the battery with no motors wired yet.

---

## 5. Phase 4 — Signal wiring: ESP32 → TB6612 (Dupont jumpers)

These are *logic* signals (tiny current), so plain Dupont jumpers are fine. **This pinout is the one
the firmware actually uses** — match it exactly or edit the `// TUNE` pin lines in the `.ino`.

| ESP32 pin | → TB6612 pin | What the signal does |
|---|---|---|
| **GPIO 25** | STBY (both boards) | Master enable. LOW = driver asleep (motors dead) |
| **GPIO 26** | AIN1 | LEFT side direction bit 1 |
| **GPIO 27** | AIN2 | LEFT side direction bit 2 |
| **GPIO 14** | PWMA | LEFT side **speed** (20 kHz PWM, 0–255) |
| **GPIO 33** | BIN1 | RIGHT side direction bit 1 |
| **GPIO 32** | BIN2 | RIGHT side direction bit 2 |
| **GPIO 12** | PWMB | RIGHT side **speed** (PWM) |
| **3V3** | VCC (both boards) | Logic supply for the driver |
| **GND** | GND (both boards) | **Common ground — easy to forget, nothing works without it** |

**Fan-out for 4 wheels on 2 boards (v1 skid-steer):** the firmware only produces a *left* trio
(26/27/14) and a *right* trio (33/32/12). Drive **both channels of the left board** from the left
trio, and **both channels of the right board** from the right trio:

```
ESP32 LEFT trio (26,27,14) ─┬─► board1 AIN1/AIN2/PWMA  → front-left motor
                            └─► board1 BIN1/BIN2/PWMB  → rear-left  motor   (same command → wheels move together)
ESP32 RIGHT trio (33,32,12) ┬─► board2 AIN1/AIN2/PWMA  → front-right motor
                            └─► board2 BIN1/BIN2/PWMB  → rear-right motor
GPIO25 → STBY on both ;  3V3 → VCC on both ;  GND → GND on both
```

> **Why direction + a separate speed wire?** IN1/IN2 set which way current flows (forward/reverse/
> brake); PWMA/PWMB rapidly switch it on/off at 20 kHz so the *average* power — and thus the speed —
> is whatever fraction you ask for. 20 kHz is above hearing, so the motors don't whine.

> **(Optional, future) Encoder wires.** The Hiwonder motors have quadrature encoders (extra wires per
> motor). v1 **does not use them** (open-loop, P-003) — leave them unconnected or tuck them away. When
> you do the closed-loop upgrade, they'll go to spare ESP32 GPIOs read by the hardware pulse counter.
> *Wiring them in is the ~1-day first upgrade; it's what makes "drive exactly 0.5 m" accurate.*

✅ **Done when:** all 8 logic wires + VCC/GND are seated, and you can trace each one back to the table.

---

## 6. Phase 5 — Flash the firmware

1. Open `src/rover/esp32_motor_teleop.ino` in the **Arduino IDE** (board: *ESP32 Dev Module*; the
   CP2102 USB-C port). Use a **data** USB-C cable, not charge-only.
2. Edit the three `// TUNE` lines at the top: your **WiFi SSID/password**, and confirm the **pins**
   match Phase 5's table.
3. Upload. Open the **Serial Monitor** (115200 baud) — it prints `rover IP: 192.168.x.y`. **Write
   that IP down**; the laptop talks to it.

**How control works (so you know what "good" looks like):** the laptop sends ~15 UDP packets/sec like
`V,0.2,0.0` (drive forward 0.2 m/s, no turn). A **deadman timer** stops the motors if no packet
arrives for 300 ms — so a WiFi dropout or a closed laptop lid fails *safe* (rover stops), not *wild*.

✅ **Done when:** the serial monitor shows a WiFi IP and `UDP listening on 4210`.

---

## 7. Phase 6 — First motion test (wheels UP, on a stand)

**Put the rover on a box so the wheels spin free** — you do not want a wiring mistake driving it off
the bench.

1. `python src/rover/teleop_client.py --host <esp32-ip>` (keyboard/gamepad).
2. Nudge forward. **Check each wheel:** all four should spin the *same* direction for "forward." A
   wheel spinning backwards = its two motor leads (AO1/AO2) are swapped — just reverse them.
3. Test turn (left wheels forward, right wheels back = spin) and stop (deadman: stop sending → wheels
   halt within 300 ms).

✅ **Done when:** forward / reverse / spin-turn all behave, and releasing the control stops the rover.

---

## 8. Phase 7 — Mount the camera + the tether bench-test (the make-or-break)

Mount the camera **low, central, and stiff** on the L-bracket (vibration is the enemy — see Phase 8),
the powered hub on the deck, and run the 5 m active tether to the laptop. **Power the hub first, then
plug the camera.**

Then run the **tether bench-test** ([[land-rover-v1-rig]] §7) *before* trusting any drive:

1. **Enumerate:** `lsusb` shows `32e4:0035`; `dmesg -w` shows **no** disconnect / over-current lines.
2. **15-min sustained stream** at full res — pass = full frame count, zero `dmesg` drops.
3. **Power-stress:** run the motors *while* streaming — the camera must not drop.

> **Why so paranoid about USB?** This is **P-001** — the camera intermittently dropped off the bus on
> marginal power, and a mid-run sensor dropout kills SLAM. The powered hub + cap exist to fix it; this
> test proves they did. *A dropout here is a finding worth stopping for, not powering through.*

✅ **Done when:** 15 min of streaming with motors running and **zero** USB drops.

---

## 9. Phase 8 — The vibration gate (don't trust the build until this passes)

Drive a **slow straight line** across the room, then **review the recorded camera footage frame by
frame** (use the recorder's `sharp` gauge / `make_kitti_dataset` + a glance at the frames).

- **Pass:** frames are crisp; `sharpness` stays healthy (≳ 40).
- **Fail:** motion blur / smear → stiffen or foam-dampen the camera mount, slow the speed cap
  (`V_MAX` in the firmware), and re-test.

> **Why this is a hard gate.** We *proved* this session that motion blur destroys relocalization —
> blurry frames are exactly where the geometry falls apart. A rover that drives but blurs every frame
> is useless as a mapping platform. **Blur is a build failure, not a nuisance.**

✅ **Done when:** a slow drive yields a clean, sharp image sequence the SLAM pipeline can map.

---

## 10. What's intentionally NOT in v1 (your upgrade backlog)

Logged so nobody mistakes a deferred choice for a bug:

1. **Mecanum strafing** — needs 4-channel firmware + mixing (the wheels & boards are already there).
2. **Closed-loop odometry** — wire the encoders, read them on the ESP32, publish odometry to RTAB-Map
   (parked **P-003**; also helps bridge feature-poor frames).
3. **Cut the tether** — move capture onboard (Pi 5 → later Jetson Orin); see [[land-rover-v1-rig]] §6
   upgrade path and [[system-architecture]]'s "map survives WiFi dropout" invariant.

---

## 11. Phase 9 (optional add-on) — the 2-DOF sensor head: tilt + Z-lift

By default the sensor head (camera + LiDAR) sits at a **fixed height, looking straight ahead** — the only
"rotation" is the whole rover yawing. This add-on gives the *mount itself* two extra degrees of freedom so it
can **look up at and rise to high surfaces** (countertops, shelves, tabletops), not just what's at deck level:

1. **Tilt** — pitch the head up/down (a bus servo).
2. **Z-lift** — raise/lower the head on a vertical lead-screw (a closed-loop stepper).

> 📖 **Design rationale, actuator trade-offs, and the calibration math live in [[sensor-mount-2dof-tilt-lift]].**
> *This* section is the **as-built guide** — the finalized parts, the exact assembly order, wiring, and the
> per-frame pose readout the mapping needs. Where the two disagree, **this page is the as-built truth** (the
> sister page's BOM still lists a separate TMC2209 driver — superseded; see the BOM note below).

> 🔴 **The hard part is NOT the actuators — it's that the sensor pose is now a VARIABLE.** This is a mapping
> rover: every frame is tagged with the sensor's pose, and `data/calib/rig_geometry.json` currently encodes a
> *fixed* 7 cm LiDAR-above-camera offset. With tilt+lift, that offset and the sensor heights become a **function
> of the two actuator states** — so the build **must read back the *measured* tilt angle and lift height per
> frame** (not the commanded values). That's why every actuator here is **closed-loop / absolute / homed**, never
> open-loop. See [[sensor-mount-2dof-tilt-lift]] §D/§E for the calibration + rig-geometry consequences.

### 11.0 — Quick reference sheet (the whole add-on at a glance)

**Finalized BOM (as-built).** Cross-checked for compatibility and double-buys (2026-06-18):

| Part | Role | Key spec | Status |
|---|---|---|---|
| STS3215 12 V 30 kg bus servo + bracket | **Tilt** actuator | TTL serial bus; 12-bit mag encoder (~0.088°/step); 30 kg·cm | buy |
| Waveshare Bus Servo Adapter (A) | **Tilt** bus bridge | UART↔half-duplex bus + servo power; **no MCU**; **9–12.6 V**; driven by the rover ESP32 | buy |
| MKS SERVO42C + NEMA17 (buy the **motor-included** bundle, not the PCBA-only board) | **Z-lift** actuator | closed-loop: integrated FOC driver + 14-bit encoder; **7–28 V**; step/dir **or** UART | buy |
| Redrex T8 365 mm lead-screw + brass nut + 5→8 mm coupler | **Z-lift** transmission | non-back-drivable; ~300 mm screw | buy |
| MGN12H 300 mm linear rail + carriage | **Z-lift** guide | anti-rotation + load; **~255 mm usable travel**; 780 N dyn. | buy |
| Optical endstop (×6 pack, use 1) | **Lift homing** (absolute zero) | ⚠ 5 V output → level-shift to ESP32 3.3 V (or use a mechanical microswitch) | buy |
| Rover's existing **ESP32** (the TB6612 drive board) | **Single head controller** — tilt (UART→adapter) + lift (step/dir) + endstop | ~6 spare GPIO incl. a free UART | **HAVE** |
| 3S LiPo 11.1 V motor rail + 1000 µF cap | Head power | 11.1 V is in-range for both the servo and the SERVO42C (7–24 V) | **HAVE** |
| Brackets: nut↔carriage↔head plate + mast frame | Mechanical glue | print/fab to fit | **FAB** |
| ~~TMC2209 stepper driver~~ | — | **❌ NOT NEEDED** — the SERVO42C has its own integrated driver; nothing to plug a TMC2209 into | **DROP** |

> ⚠️ **BOM correction vs the sister page / older revisions of this guide:** the lift uses the **MKS SERVO42C**, an
> all-in-one closed-loop servo-stepper (motor + driver + encoder + STM32). It **replaces** the plain NEMA17 +
> TMC2209 combo — **do not also buy a TMC2209.** A TMC2209 is only for a *bare* stepper on a printer mainboard,
> which this build no longer uses.

**Control architecture — ONE controller.** The Bus Servo Adapter (A) is a dumb UART↔bus bridge (no MCU), so the
**rover's existing ESP32 owns everything** — wheels (Phase 5), tilt (UART through the adapter), and lift (step/dir).
One brain ⇒ one WiFi/UDP endpoint ⇒ the per-frame `{tilt_deg, lift_mm}` pose tag is timestamped together for free:

```
                ┌──────────────── rover's ESP32 (TB6612 board) ────────────────┐
                │  also runs the wheels (Phase 5) · ONE WiFi/UDP endpoint       │
                └───┬───────────────────┬───────────────────────┬──────────────┘
          UART(TTL) │            STEP/DIR │                endstop │ (level-shifted)
            ┌───────┴────────┐   ┌────────┴─────────┐   ┌──────────┴─────────┐
            │ Bus Servo      │   │  MKS SERVO42C    │   │ optical home switch │
            │ Adapter (A)    │   │ (closed-loop Z)  │   └────────────────────┘
            └───────┬────────┘   └──────────────────┘
              bus   │  (tilt angle read back on the same bus)
            ┌───────┴────────┐
            │ STS3215 tilt   │
            └────────────────┘

  → ESP32 publishes MEASURED {tilt_deg (servo encoder), lift_mm (steps-from-home)} → laptop tags each frame
```

**Assembly flow (each step detailed below):**

| # | Step | Detail in |
|---|---|---|
| S1 | Build the lift: rail + screw parallel on the mast; couple SERVO42C→screw; join brass-nut↔carriage with a plate | §11a |
| S2 | Add the home switch: optical endstop at bottom-of-travel + a flag on the carriage | §11a |
| S3 | Mount the tilt servo on the carriage; bolt the camera+LiDAR L-bracket to its horn (keep the 7 cm offset rigid) | §11b |
| S4 | Route cabling across the moving Z — drag-chain / service loop + strain relief | §11c |
| S5 | Wire power: 11.1 V motor rail → HAT + SERVO42C, isolated from the 5 V camera rail, 1000 µF cap | §11d |
| S6 | Wire control (all on rover ESP32): UART → Adapter(A) → STS3215; step/dir → SERVO42C; ← endstop (level-shifted) | §11d |
| S7 | Firmware: home-on-boot, publish *measured* {tilt_deg, lift_mm}, capture stop→tilt→lift→settle→grab | §11e |
| S8 | Bring-up: bench-test each axis → home → **re-run the vibration gate (Phase 8) at full extension** | §11f |

**Top gotchas (don't learn these the hard way):**
- ❌ **Don't buy/socket a TMC2209** — redundant with the SERVO42C's integrated driver.
- 🛒 **Buy the SERVO42C *with motor*, not the "PCBA" SKU** — a "PCBA" listing is the controller board only (no NEMA17); the bundle is cheaper all-in and skips magnet alignment.
- ⚡ **Optical endstop is 5 V, the ESP32 is 3.3 V-max** — level-shift the signal (or swap in a mechanical microswitch wired contact-to-GND).
- 🔋 **Adapter (A) wants 9–12.6 V** — a near-empty 3S sags toward its ~9 V floor; don't run the head on a depleted pack.
- 🧵 **Spend a free ESP32 UART on the adapter** (e.g. UART2 on GPIO17/16) and keep the stepper pins clear of it.
- 🔌 **Confirm the 5→8 mm coupler is in the Redrex box** before assembling (NEMA17 5 mm shaft → T8 8 mm screw).
- 📐 **Pose tag must be MEASURED, not commanded** — home the lift on boot; the SERVO42C's closed loop makes commanded≈achieved, and tilt reads the servo's encoder register.
- 〰️ **Re-run the vibration gate at FULL mast extension** — a tall moving mast fights the "low, stiff, central" rule.

### 11a. Mechanical assembly (S1–S2) — the lift mast

```
   ┌───────── SENSOR HEAD (camera + LiDAR + powered hub) ─────────┐
   │   tilts on the STS3215 bus-servo pivot  (pitch up/down)      │   ← tilt axis (§11b)
   └───────────────────────────┬─────────────────────────────────┘
                               │  bolted to the MGN12H CARRIAGE
   ╔═══════════════╗   ┌───────┴───────┐
   ║ MGN12H RAIL   ║   │ carriage plate │── brass nut (driven by the screw)
   ║ (anti-rotate, ║◄──┤   (FAB part)   │
   ║  carries load)║   └───────┬───────┘
   ╚═══════╤═══════╝           │ T8 lead-screw (turns → carriage rides up/down)
           │            ┌──────┴──────┐
           │            │ 5→8 coupler  │
        ┌──┴────────────┴─────────────┴──┐
        │  MKS SERVO42C (NEMA17, closed)  │  ← turns the screw; holds with power off
        └──────────────┬─────────────────┘
                ┌───────┴────────┐
                │  ROVER DECK    │   ← rigid mast base, foam-isolated
                └────────────────┘
```

**S1 — Build the lift mechanism:**
- **Mount the MGN12H rail and the T8 screw parallel and plumb** on a rigid mast upright bolted to the deck. The
  rail takes *all* the load and stops rotation; the screw only provides the up/down force. (Never let the screw be
  the only vertical support — it will whip and wobble, blowing the vibration gate.)
- **Couple the SERVO42C to the screw with the 5→8 mm coupler** (NEMA17 5 mm shaft → T8 8 mm screw). Motor at the
  bottom is simplest; add a top bearing block for the screw's free end if the mast is tall.
- **Join the brass nut to the MGN12H carriage with a FAB plate** so when the screw turns, the carriage (constrained
  by the rail) translates instead of the nut spinning. This plate is the key printed/machined part.
- **Travel check:** 300 mm rail − ~45 mm carriage ≈ **~255 mm usable** — more than the 150–200 mm reach target. The
  365 mm screw is longer than the rail; travel is rail-limited, which is fine. Add **soft limits in firmware** so you
  never drive the carriage into either end.

**S2 — Add the home switch (absolute zero):**
- Mount the **optical endstop at the bottom of travel** and a small **flag/vane on the carriage** that breaks its
  beam at the home position. The lift has no absolute height reference until it touches home — every power-up **homes
  down to the switch, sets `lift_mm = 0`, then moves up**.
- ⚡ **Logic-level gotcha:** these RAMPS optical endstops are **5 V** and output a **5 V HIGH**, which exceeds the
  ESP32's 3.3 V GPIO limit. Power it at 3.3 V if it'll run there, add a level-shifter / resistor divider on the
  signal, **or** just substitute a **mechanical microswitch** (wired NO → GND with the ESP32's internal pull-up) —
  the simplest, level-safe option.

### 11b. Tilt subsystem (S3) — STS3215 + Bus Servo Adapter (A)

- **Mount the tilt servo at the head's pitch pivot on the carriage**, and bolt the camera+LiDAR L-bracket to the
  servo horn. **Keep the LiDAR↔camera 7 cm offset rigid *on the head*** so only the head's pose changes, never the
  inter-sensor geometry.
- The **Bus Servo Adapter (A)** is a passive UART↔half-duplex-bus bridge (no MCU) that also injects servo power. The
  **rover's ESP32 drives the STS3215 through it over UART** and reads back the **measured tilt angle** (the servo's
  12-bit encoder register, ~0.088°/step) on the same bus — no separate WiFi endpoint; the tilt rides the rover's
  existing UDP telemetry (Phase 5).
- Torque budget: 30 kg·cm easily pitches a light camera+LiDAR head; keep the head's mass close to the pivot to
  minimise the moment and the settling time.
- **LiDAR caveat:** a tilted 2D LiDAR no longer cuts a clean horizontal floor slice. **Keep tilt≈0 for floor
  mapping**; use tilt only for looking *up* at surfaces, or re-derive the intersected plane
  ([[floor-map-sensing-options]]).

### 11c. Cable management across the moving Z (S4)

- The camera USB, LiDAR USB/serial, and the servo TTL all cross the moving joint and **must survive repeated raising/
  lowering without snagging or yanking a connector** — the #1 USB failure mode (**P-001**).
- Use a small **cable drag-chain (e-chain)** or a **service loop + spiral wrap** anchored top and bottom, with a
  **strain-relief P-clip at the head.** The powered hub (the P-001 fix) can ride **on the moving head** (shortest
  sensor cables; service-loop the long laptop tether) or stay on the deck with a service loop up to the head.

### 11d. Power + control wiring (S5–S6)

```
 11.1 V motor rail (NOT the camera 5 V rail) ─┬─► Bus Servo Adapter (A) ─ bus ─► STS3215 tilt servo   ~0.2–0.5 A
   (+1000 µF bulk cap across the head feed)   └─► MKS SERVO42C ──────────────► NEMA17 lift screw       ~0.5–1.5 A moving, ~0 holding

 CONTROL — all on the rover's ESP32:
   rover ESP32 ── UART (TTL) ──► Adapter (A) ── bus ──► STS3215   ;   tilt angle ◄── STS3215 encoder register (same bus)
   rover ESP32 ── STEP/DIR (3.3 V) ──► SERVO42C                   ;   lift_mm = steps from home (closed loop ⇒ commanded≈achieved)
   rover ESP32 ◄── endstop (level-shifted) ── optical home switch
```

**S5 — Power:**
- **Feed both the Adapter (A) and the SERVO42C from the 11.1 V motor rail, isolated from the camera 5 V rail**
  (brownout discipline — same rule as Phase 4), with a **1000 µF bulk cap** across the head feed. ⚠️ The **Adapter (A)
  wants 9–12.6 V**: a full 3S (12.6 V) is fine, but a **near-empty pack sags toward its ~9 V floor**, so don't run the
  head on a depleted battery. The SERVO42C is relaxed (**7–28 V**).
- Budget **~1–2 A @ 12 V peak for the servo + ~0.5–1.5 A for the stepper while moving, ≈0 holding** — intermittent
  (the head moves only between captures), so the runtime hit on the 3S pack is marginal. Size the head wiring and
  cap for the *combined* peak.

**S6 — Control (everything on the rover's ESP32):**
- **Tilt:** wire a **free hardware UART** (e.g. UART2 — TX=GPIO17, RX=GPIO16) to the Adapter (A)'s UART pins; the
  adapter handles the half-duplex bus + servo power. The ESP32 both commands the STS3215 and reads its encoder over
  this single link.
- **Lift:** drive the SERVO42C **STEP / DIR / EN** on output-safe GPIOs (e.g. **13 / 4 / 18** — avoid the strapping
  pins and the Phase-5 motor pins), and read the **home switch on GPIO19** (it supports an internal pull-up, so a
  plain microswitch-to-GND works; if you keep the *optical* endstop, level-shift its 5 V output first). Confirm
  against your actual board before soldering.
- **Why step/dir is enough for a *measured* pose:** the SERVO42C is closed-loop — it will not silently lose steps
  (it errors/stalls instead), so after homing, **commanded step-count = true height** to encoder resolution. That
  satisfies the "measured ≠ commanded" rule without extra sensing. For belt-and-suspenders readback, query the
  SERVO42C's 14-bit encoder over its **UART** instead of (or alongside) step/dir.

### 11e. Firmware + the per-frame sensor-pose readout (S7) — load-bearing

1. **Calibrate the actuator→sensor transforms once** (tilt pivot position/axis vs camera; lift travel direction/offset;
   home-switch offset; backlash) — see [[sensor-mount-2dof-tilt-lift]] §D.
2. **`data/calib/rig_geometry.json` becomes pose-DEPENDENT** — the 7 cm offset + sensor heights become functions of
   `(tilt_deg, lift_mm)`; full per-frame pose = `base ∘ lift(lift_mm) ∘ tilt(tilt_deg) ∘ sensor_extrinsics`
   (§E of that page has the JSON sketch).
3. **Home on boot:** the lift drives down to the endstop, zeroes, then is free to move. Without this the lift height
   is unknown and every frame's pose tag is wrong.
4. **The rover ESP32 publishes *measured* pose** — `tilt_deg` (servo encoder register, read back over the adapter)
   and `lift_mm` (steps-from-home, closed-loop-guaranteed) — into its existing telemetry at ≥ the capture rate, so
   each captured frame is tagged with the achieved pose. **Commanded ≠ achieved** (except the SERVO42C makes them
   equal once homed). One controller ⇒ both values share a timestamp natively.
5. **Capture-while-settled rule for v1:** **stop → tilt → lift → settle → grab**, not capture-while-moving. A settled
   head makes the pose tag unambiguous, sidesteps motion blur, and keeps the per-frame tag trivially correct.
   Continuous-motion capture (with tight time-sync) is a later upgrade.
6. **Tilted 2D LiDAR ≠ horizontal slice:** off-horizontal tilt breaks the clean floor-plan slice — keep LiDAR
   floor-mapping at tilt≈0, or re-derive the intersected plane ([[floor-map-sensing-options]]).

### 11f. Bring-up & test sequence (S8)

1. **Bench each axis powered but un-mounted first** — confirm the servo sweeps and reports its angle; confirm the
   SERVO42C turns the screw both directions and the carriage rides the rail smoothly end-to-end (set firmware soft
   limits *before* going full travel).
2. **Verify homing:** power-cycle → the lift seeks the endstop, stops, zeroes. Repeat 5× — the homed zero must be
   repeatable (the switch+flag are what give you the ~0.05 mm repeatability target).
3. **Verify the pose telemetry:** move to a few `{tilt_deg, lift_mm}` targets and confirm the *measured* values in
   the stream match a ruler/protractor on the rig.
4. 🔴 **Re-run the vibration gate (Phase 8) at FULL mast extension** (worst-case wobble), not just retracted — a tall
   moving mast is the *opposite* of the "low, stiff, central" rule. Stiffen the rail / foam-isolate the head / lower
   the speed cap until a slow drive at full height yields a crisp image sequence.

✅ **Done when:** the head tilts and lifts to commanded targets, **homes to an absolute zero on boot**, reports its
**measured** `{tilt_deg, lift_mm}` per frame, holds position with power off (lead screw), and the **vibration gate
(Phase 8) re-passes at full extension**.

---

## Source

Assembled from the rig spec ([[land-rover-v1-rig]]), the `drone-prototype` rover firmware `src/rover/esp32_motor_teleop.ino` + its README, and the parked v1-scope decisions P-001/P-003.

## Related

[[land-rover-v1-rig]] · [[sensor-mount-2dof-tilt-lift]] · [[passive-stereo-robustification]] ·
[[imu-vio-integration-reality]] · [[map-then-navigate]] · [[system-architecture]] ·
[[home-tidy-drone-prototype]] · [[drone-comms-wifi]]
