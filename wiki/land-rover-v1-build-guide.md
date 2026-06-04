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

```
   TB6612FNG  (one board = TWO motor channels: "A" and "B")
   ┌─────────────────────────────────┐
   │ VM   VCC  GND  STBY              │   VM   = motor power  (→ 11.1 V battery)
   │ PWMA AIN1 AIN2 ...               │   VCC  = logic power  (→ ESP32 3V3)
   │ PWMB BIN1 BIN2 ...               │   STBY = enable       (→ ESP32 GPIO25)
   │ AO1 AO2   BO1 BO2                │   AO1/AO2 = motor A leads ; BO1/BO2 = motor B leads
   └─────────────────────────────────┘
```

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

✅ **Done when:** both boards have clean, shiny solder joints (no bridges between pads), motor leads
attached to AO1/AO2 and BO1/BO2.

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

## Related

[[land-rover-v1-rig]] · [[passive-stereo-robustification]] · [[imu-vio-integration-reality]] ·
[[map-then-navigate]] · [[system-architecture]] · [[home-tidy-drone-prototype]] · [[drone-comms-wifi]]
