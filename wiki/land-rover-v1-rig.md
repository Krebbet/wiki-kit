# Land-Rover v1 Rig — Cheapest Teleop Mapping Platform

The minimal, cheap ground-robot rig to carry the SVPRO stereo camera around an indoor room
so the [[home-tidy-drone-prototype]] perception/nav stack can be validated on a moving
platform. Scope: **simple + cheap, prove mechanisms** — manual drive from the laptop +
scripted autonomous moves, with the heavy SLAM ([[slam]]/RTAB-Map) running **on the laptop**,
not the robot. This page is the build reference; it supersedes the expensive aerial-oriented
buy list in [[home-tidy-drone-prototype]] *for the first ground build*.

> **Origin:** authored 2026-06-02 from three dispatched research runs (chassis/drivetrain/power;
> onboard-vs-offboard compute/comms; teleop + camera-streaming software), commissioned by the
> `drone-prototype` prototyper. Prices are vendor list June 2026, CAD ≈ USD × 1.37 (add 15–40%
> for Canadian shipping/duty on small electronics). Confidence high on the architecture and the
> bandwidth math; medium on exact per-build "feel" and runtime.

---

## TL;DR — the recommended v1 architecture

**Tether the camera to the laptop; put only a cheap microcontroller on the rover for motors.
No onboard Pi, no Jetson for v1.**

```
SVPRO cam ─(short USB)─► powered USB hub ON the chassis ─(5–10 m active USB-2.0 ext)─► LAPTOP ─► RTAB-Map
ESP32 on chassis ─WiFi (UDP)─► laptop teleop/script client ;  ESP32 ─GPIO─► TB6612 driver ─► drive motors
```

**Why:** the camera's full-resolution stream **cannot go over WiFi** (see §1, the crux). Tether
it on a wire it was designed for → full res, near-zero latency, RTAB-Map sees it as a local
camera, *and* it gives the finicky USB link ([[home-tidy-drone-prototype]] P-001) the powered,
mechanically-secured path it needs. Drive commands are tiny, so the ESP32's WiFi link never
contends with video. **Rover parts ≈ $275–320 CAD** on top of the laptop you already have —
vs ~$1,800–2,700 for the aerial-oriented build.

**The honest tradeoff:** a trailing 5–10 m tether = **one room at a time**, operator manages
cable slack. Fine for v1 single-room mapping; the upgrade path (§6) removes it.

---

## 1. The crux: full-res video does not fit WiFi

The SVPRO delivers **3840×1080 side-by-side, MJPG, 30 fps**. MJPEG is intraframe, so bitrate
scales with pixels × quality:
- 1080p MJPG@30 ≈ **~50 Mbps** in practice.
- The SVPRO frame is **2× the pixels of 1080p** → **~80–150 Mbps** compressed (scene/quality
  dependent).
- It rides USB 2.0 fine because UVC isochronous gets ~384 Mbps (80% of 480) — the stream sits
  well under that.

But **real Pi WiFi throughput is the wall:** Pi 4 ≈ 63 Mbps near the router; Pi 5 ≈ 217 Mbps
near the router but **drops to ~48 Mbps at ~25 ft** and can fall off the 5 GHz band — on a
*roving* robot through walls it's worse. So any architecture that **restreams full-res video
over WiFi chokes.** Two independent research runs converged on this.

Resolutions of the conflict:
- **(chosen) Tether the camera** → keep full res, no WiFi video at all.
- Downscale (e.g. 1920×540 @10–15 fps) MJPEG-over-WiFi from an onboard Pi → fits WiFi but
  throws away resolution the *already-marginal* passive stereo wants ([[passive-stereo-robustification]]).
- H.264-encode on a Pi (~12 Mbps) → fits WiFi but lossy re-compression hurts stereo matching +
  adds a GStreamer pipeline + Pi CPU. Only if a tether is truly impossible.

→ For v1, full-res quality matters more than untethered range. **Tether.**

---

## 2. Compute / comms — architectures evaluated

| Architecture | Works for this stream? | Cost (CAD) | P-001 USB story | Verdict |
|---|---|---|---|---|
| **Camera tethered to laptop + ESP32 motors** ★ | **Yes** — full res, sub-frame latency | ~$95–170 rover electronics | **Best** — powered hub on chassis, strain-relieved | **v1 pick** |
| Onboard Pi 4/5 restreams video over WiFi | Marginal — Pi 4 chokes; Pi 5 only near router | $130–160 + parts | Re-rolls the USB dice on a worse host | High-risk, high-effort; defer |
| `usbip` / network-USB device server | **No** — isochronous + 80–150 Mbps is usbip's weak spot; commercial boxes drop video frames + are wired anyway | $150–300 for the box | Adds another USB host | Skip |
| ESP32 *hosting* the camera | **No** — ESP32 cannot host a UVC camera, full stop | — | — | Impossible; ESP32 is motors-only |
| Onboard Jetson | Yes (overkill) | $340–680 | n/a | **Defer to v2** (see §6) |

**When a Jetson actually becomes necessary (v2+):** only when you want compute *in the loop
onboard* — laptop-out-of-the-loop real-time SLAM/autonomy, untethered multi-room operation, or
onboard neural perception at frame rate. None apply to v1's "prove mapping cheaply, SLAM on the
laptop" mandate. Jetson is the upgrade, not the v1 part.

---

## 2b. USB tether — the P-001 linchpin (deep dive, 2026-06-02)

The whole "tether the camera" architecture lives or dies on the USB link holding under motion.
A dedicated deep dive settled how to build it. **The trap is power, not bandwidth.**

- **No single active extension cable can power this camera.** Active USB-2.0 repeater cables
  pass only **250–450 mA** of bus power (Tripp Lite U026 = 250 mA; Plugable USB2-10M = 450 mA),
  and active *optical* cables often pass **zero** (Logitech Strong explicitly won't power a
  bus-powered webcam). A dual-sensor MJPEG stereo cam draws **~350–600 mA** — at/above every
  cable's ceiling, and this unit *already* browns out (P-001). A bare long cable makes P-001
  **worse**. (Second issue: cheap repeaters don't cleanly re-clock isochronous UVC traffic —
  Plugable itself doesn't recommend its active cable with webcams.)
- **The fix — powered hub AT THE CAMERA END.** Topology:
  **laptop → active extension → self-powered USB hub *on the chassis* → short cable → camera.**
  The camera draws its current from the hub's *local* 5 V source, so the long cable's voltage
  drop and the laptop port's stinginess become irrelevant to the camera's power rail — directly
  killing P-001's believed root cause. The hub also re-drives the bus close to the device, so
  the fragile last hop is short. **This is FTC robotics' standard recipe** for UVC cameras on
  vibrating competition robots — the closest real-world analog to this rig. Putting the hub at
  the *laptop* end does nothing for P-001.
- **Hub pick:** **self-powered** (not bus-powered), USB 2.0 is sufficient, per-port ≥0.9 A,
  rugged/mountable. Best fit: **Coolgear/USBGear USBG-4U2ML** (4-port industrial USB 2.0, 7–24 V
  **terminal block** so it wires straight off a buck/battery, steel case, mountable; screw-lock
  variant USBG-4SU2MLA for vibration immunity). Cheap fallback: the Anker/Atolla 5 V powered
  hubs FTC uses (~$20–35 CAD, less rugged).
- **Power the hub off its OWN rail** (brownout isolation), but **mind the hub's input voltage**:
  the **Coolgear USBG-4U2ML terminal block wants 7–24 VDC, NOT 5 V** (it regulates 5 V to the
  ports internally). So feed it from a **dedicated 7–12 V source isolated from the motor rail** —
  a small separate 2S/3S 18650 pack, or a USB-C PD bank + a 9–12 V PD-trigger board — with a
  470–1000 µF bulk cap. (The simple "5 V power-bank straight to the hub" plan only works if you
  instead pick a **5 V-input** hub like the Anker/Atolla fallback.) Budget ~0.5–0.75 A at 5 V on
  the port side for camera+hub. **Watch the power-bank low-current auto-shutoff** (most banks cut
  out below ~50–75 mA when idle) — pick a bank with an always-on/trickle mode or add a bleed
  load; the inline USB meter verifies steady draw.
- **Mechanical (connectors are the failure point, not the wire):** anchor the long cable to a
  **chassis strain-relief point** so a tether yank never loads the camera plug; **screw-lock
  USB** connectors; **ferrite chokes** both ends; a **service loop** at chassis entry; keep the
  camera→hub cable short and captive. Operator walks the tether slack for v1 single-room.
- **Simplest single-kit alternative (test first):** a **USB-over-Cat5e extender kit** (StarTech
  USB2001EXTV — powered RX box with its own 5 V, real isochronous re-clocking) replaces the
  cable+hub with fewer connectors. **But** cheap extenders warn "1080p webcam not supported," and
  our stream is *2× 1080p* — so it **must be bench-tested at full 3840×1080 before trusting**.
- **Bench test before committing (and again under motion)** — see §7. Pass = full frame count,
  no `dmesg` USB disconnects across a 15-min stream and a 10-min drive while flexing the tether.
- **Residual risk ~10–25%.** If the camera drops *even on a clean, still bench with local power*,
  the fault is the **unit itself** (flaky USB PHY/solder), not the path → escalate P-001 as a
  **hardware fault** (RMA / different sample), a Commandment-XIII checkpoint, not a quiet retry.
  *Cheap de-risker:* measure the real camera draw with a ~$10 inline USB power meter during the
  bench test to size the hub precisely.

## 3. Chassis / drivetrain / power

The #1 mechanical requirement is **slow, smooth, low-vibration motion** (motion blur — not
feature starvation — is this camera's limiting factor; see the mapping report). The single most
important mechanical choice is **gearing/RPM, not chassis brand**: pick low-RPM gearmotors
(~100–200 RPM, ≤~0.5 m/s) so you crawl smoothly in the usable part of the PWM curve.

### Chassis SKUs
| Tier | SKU | ~CAD | Encoders | Payload | Note |
|---|---|---|---|---|---|
| **★ Recommended (mecanum, holonomic)** | Hiwonder Large Metal 4WD, 8V/12V encoder, **mecanum** wheels (RobotShop RM-HIWO-02R) | ~$185–215 | **Yes (quadrature)** | ~1.9 kg | **Chosen 2026-06-02 (human):** holonomic motion simplifies nav/path-planning (no turn-then-drive; decouple camera heading from travel — good for SLAM viewpoints) + available + encoders + best payload. **Trade: roller VIBRATION** (our #1 problem is motion blur) → see the vibration gate below. Needs mecanum-mixing firmware (vx,vy,ω). |
| Rubber-wheel alt (no encoders) | Waveshare WAVE ROVER (onboard ESP32+WiFi+3S UPS) | ~$125 CAD | **No** | 0.8 kg | In stock CA; integrates the ESP32+WiFi+battery (simplest electronics). Open-loop only. Differential. |
| Rubber+encoder alt (low stock) | DFRobot Baron-4WD w/ Encoder (ROB0025) | ~$71 CAD / $50 USD | **Yes (optical)** | 0.8 kg | Rubber+encoder+differential, but discrete-electronics build, tight payload, shaky stock. The ideal Yahboom 520-encoder (B0BR9Q95KD) proved **not actually buyable**. |

> **Vibration gate (mecanum, load-bearing):** the FIRST post-assembly test is to drive a slow line on
> hard floor + carpet and **review the camera footage for blur**. Mecanum roller buzz feeds our #1
> problem (motion blur). If footage is clean at slow speed → mecanum is a clear win (holonomic nav +
> encoders + payload). If it buzzes → foam-isolate the camera mount low/central, drop speed, or
> reconsider. Don't lock the build until this passes.
| Cheapest "it moves" | Generic 4WD acrylic kit **with encoders** + TB6612 + 2S pack | ~$112 | single-channel | marginal near 1–2 kg | Buzzy plastic TT motors, flexy deck — log as a known weak point, expect to upgrade |
| Most integrated | Waveshare WAVE ROVER (onboard ESP32+WiFi+UPS) | ~$137 | **No** | **0.8 kg (tight!)** | Near-teleop out of box, but no odometry + shared-rail brownout risk + payload may be exceeded |
| Reference ceiling | Yahboom ROSMASTER X3 | ~$900 | yes | high | Full ROS2 base — violates "cheap/disposable"; ceiling only |

### Component picks
- **Motor driver: TB6612FNG** (or DRV8833 if motors ≤10 V). **NOT L298N** — its 1.5 V drop runs
  hot and makes low-speed PWM coarse/non-linear, hurting smooth crawl.
- **Wheels: mecanum chosen for v1 (2026-06-02, human)** — the general rule favors rubber/standard
  (mecanum rollers are buzzy on hard floor + slip more), BUT the holonomic benefit (simpler nav/path-
  planning, decoupled camera heading) + the only available encoder+payload option being mecanum
  tipped the call. Vibration is the risk → the vibration gate above. Odometry slip matters little
  (camera is primary SLAM). For a pure-smoothness build, rubber/standard wheels remain the safer pick.
- **Encoders matter** — quadrature wheel encoders give odometry to fuse with visual SLAM (bridges
  feature-poor/blank-wall moments and makes scripted moves repeatable). Buy a chassis that
  includes them rather than retrofitting.
- **Differential / skid-steer drive** — simplest kinematics, matches SLAM/odometry math.

### Power — the brownout trap
Motors + computer on **one rail** browns out the computer (motor inrush sags the rail; a reset
mid-map kills the run). **Split the rail:**
- Simplest for a prototype: **two batteries** — a 10,000 mAh USB-PD power bank for the laptop-end
  hub/camera if needed, and a separate **2S/3S 18650 pack** for the motors. Zero coupling, easy
  to debug/hot-swap.
- Or one battery + a dedicated 5 V buck (UBEC) for the logic rail + a 470–1000 µF bulk cap across
  the motor supply to soak inrush.

Runtime: a 2200–3000 mAh 2S pack ≈ **45–90 min** of intermittent slow indoor driving.

### Smooth-motion rules (SLAM-critical)
1. Low-RPM gearmotors + **software speed cap** well below max.
2. **PWM accel/decel ramping** in firmware — eases velocity in/out, big payoff for blur.
3. No steppers (jerky/vibrate); don't run DC motors so slow they cog — use high gear reduction.
4. Rubber wheels + rigid metal deck; mount the camera **low, stiff, central** (not on a tall
   flexy mast); a little foam isolation under the mount helps.
5. Closed-loop (encoder) speed control → matched steady wheel velocity → straighter lines, less
   heading drift, smoother footage.

---

## 4. Software stack — lightest thing that works

**Do NOT use ROS 2 for v1** — the project's own [[drone-comms-wifi]]/[[ros2-server-bridge]] pages
document that DDS-over-WiFi discovery is a known multi-hour yak-shave, and it buys no latency
advantage at home-WiFi scale. Build the 50-line version; take ROS 2 when Nav2/`tf`/multi-node
actually pays (Phase 2).

| Layer | v1 pick |
|---|---|
| **Teleop link** | Plain **UDP socket**, ESP32 (or laptop→Pi) parses `{vx, wz, seq}` at 10–20 Hz. UDP "drop don't queue" is right for teleop. **Deadman watchdog: no command for ~300 ms → stop motors.** |
| **Laptop input** | `pygame` USB gamepad (left-Y→linear, right-X→angular) + keyboard fallback |
| **Scripted moves** | Same socket, add verbs: `{"type":"move","dist_m":0.5}`, `{"type":"turn","deg":90}`, `stop`. **Open-loop timed** for v1 (±10–30% drift); **encoder closed-loop** as the first upgrade (+~1 day) — highest-value, gives repeatable moves + wheel odometry. |
| **Camera intake** | Tethered → camera is a **local `/dev/video*` on the laptop**, consumed by the existing OpenCV pipeline **unchanged** (split at midpoint, honor the 180° rotation + L/R swap). No streaming server needed. |

Minimal command API sketch (JSON over UDP):
```
{"v":1,"type":"vel","vx":0.2,"wz":0.0}   # continuous teleop
{"v":1,"type":"move","dist_m":0.5}        # scripted forward
{"v":1,"type":"turn","deg":90}            # scripted turn
{"v":1,"type":"stop"}
# rover→laptop telemetry ~10 Hz: {"enc_l":..,"enc_r":..,"done":true}
```

**Effort:** ~1–2 days to a driving rover + live laptop stream; +0.5 day scripted moves; +1 day
encoders/odometry. Dominated by motor-driver wiring + tuning, not code.

**Note — if you DO later stream over WiFi** (Pi upgrade path), the OpenCV stale-frame trap is
mandatory to fix: run capture in a thread that keeps only the latest frame (vanilla
`VideoCapture(url)` buffers and falls seconds behind). Source-stamp frames on the capture device,
not at laptop receipt. Not needed for the tethered v1.

---

## 5. Bill of materials — recommended v1

| Item | Pick | ~CAD |
|---|---|---|
| Chassis + encoder motors | Hiwonder Large Metal 4WD, **mecanum, 12V encoder** (pairs with the 3S LiPo; 8V variant = RM-HIWO-02R) | ~175–215 |
| Motor driver | **2× TB6612FNG** (mecanum = 4 independent wheel channels; 1 board = 2 ch) — or use the Hiwonder kit's included controller board if WiFi-drivable | 12–20 |
| Motor controller / WiFi | ESP32 dev board (runs mecanum mixing vx,vy,ω → 4 wheels) | 8–14 |
| Camera tether (data) | Tripp Lite **U026-10M** active USB-2.0 repeater (or 5 m U026-05M) — *data only, NOT powering the cam* | 30–40 |
| Powered hub (chassis end, camera power — P-001 fix) ★ | **Waveshare USB3.2-Gen1-HUB-4U** — 4-port metal hub, self-powered **7–36 V DC terminal**, 2 A/port, wall-mount, **on Amazon ~$18–30** (preferred: cheaper + no US import). Alt: Coolgear USBG-4U2ML (USB 2.0, US import ~$125–145). | ~25–40 |
| Hub power (motor-isolated) | **7–12 V** for the hub's DC terminal (Waveshare 7–36 V / Coolgear 7–24 V — NOT a plain 5 V bank, see §2b): small 2S/3S pack OR a buck off the LiPo + 1000 µF bulk cap | ~20–30 |
| Motor battery | 3S LiPo 11.1 V (full speed) or 2S 18650 pack (slower) + balance charger | ~50 |
| Tether mechanical | screw-lock USB, ferrite chokes, P-clamp/strain relief, inline USB power meter | ~45 |
| Sundries | wiring, mount bracket | ~12 |
| **Rover subtotal** | | **~$540–685 CAD landed** (incl. US-import duty on the industrial hub; cheap 5 V-hub variant ~$120 less) |

> Earlier "~$300–360" was parts-only at optimistic prices; the procurement pass below lands it at
> **~$540–685 CAD** once Canadian retail + US-import duty on the industrial hub + a 3S battery +
> charger + real sundry prices are counted.

### Procurement — confirmed Canadian SKUs (June 2026)
Click-to-buy from a dispatched procurement pass. ✅ = price/stock confirmed on page; ~ = estimate.
| Item | SKU | Retailer | CAD | Stock |
|---|---|---|---|---|
| Chassis 4WD + encoder ★ | Hiwonder Large Metal 4WD, **mecanum**, encoder (RM-HIWO-02R) | RobotShop CA / Hiwonder | ~185–215 | available |
| Chassis — rubber alt (no enc.) | Waveshare WAVE ROVER (onboard ESP32+WiFi+UPS) | PiShop.ca | **125** | ✅ in stock |
| **Powered hub** ★✅ | **Waveshare USB3.2-Gen1-HUB-4U** (self-powered 7–36 V, 2 A/port, metal) | **Amazon** | ~25–40 | ✅ (no US import) |
| Powered hub (alt) | Coolgear USBG-4U2ML ($70.49 USD, USB 2.0) | coolgear.com | ~125–145 landed | US import |
| Active USB ext ✅ | Tripp Lite **U026-10M** | DigiKey Canada | **74.05** | ✅ in stock |
| ESP32 ✅ | ESP32 WROOM-32 DevKit | PiShop.ca | **6.95** | ✅ in stock |
| Motor driver ✅ | Adafruit TB6612 (PID 2448) | PiShop.ca | **10.95** | ✅ in stock |
| Hub power bank | Anker PowerCore 10K (+ 9–12 V trigger if PD) | Amazon.ca | ~30–40 | in stock |
| Motor battery + charger | 3S LiPo 11.1 V + SKYRC e3 | Amazon.ca | ~50–65 | in stock |
| Sundries | USB meter, ferrites, P-clamps | Amazon.ca | ~40–55 | in stock |

**Procurement watch-outs:**
- **CHASSIS — sourcing history (so we don't relitigate it).** The ideal rubber-wheel+encoder combo
  proved **not buyable** in Canada (Yahboom 520-encoder B0BR9Q95KD listed but unavailable; DFRobot
  Baron rubber+encoder but 0.8 kg payload + shaky stock; WAVE ROVER rubber but no encoders). Hiwonder's
  encoder chassis is **mecanum-only**. **Decision (human, 2026-06-02): go mecanum** (Hiwonder Large
  Metal 4WD encoder, RM-HIWO-02R) for the holonomic nav benefit + it being the available encoder+payload
  option. **Confirm at checkout it's the encoder ("8V/12V Encoder Geared Motor") variant**, not a plain-DC
  one. The firmware must do **mecanum mixing (vx, vy, ω)**, not differential. Honor the **vibration gate**
  (§3) before locking the build.
- **Coolgear hub is a US import** — no CA reseller found; order coolgear.com/usbgear.com or
  Amazon.com; budget duty/tax + 1–2 wk lead. AC adapter not included (fine — fed from a battery).
- **Power-bank auto-shutoff** (see §2b) — verify steady draw with the inline meter.
| Laptop (ground station) | already owned | $0 |
| Jetson / Pi | **deferred** | $0 |

---

## 5b. FINAL as-bought BOM + tools (2026-06-03)

The exact parts purchased after the item-by-item review (supersedes the earlier estimates). Across
Amazon.ca + RobotShop + PiShop; ~$480–520 CAD total.

| Item | Exact product (as bought) | ~CAD |
|---|---|---|
| Chassis | Hiwonder Large Metal 4WD, **12V Encoder, mecanum** (RobotShop) | ~200 |
| Motor driver | **2× TB6612FNG module** (generic or Adafruit — same chip; 2 boards = 4 ch for mecanum) — ⚠️ light-duty, see caveat | 8–22 |
| MCU | ESP32-WROOM-32 DevKit, USB-C, **CP2102** (classic — NOT the ESP32-P4) | 14 |
| Powered hub (P-001 fix) | **Waveshare USB3.2-Gen1-HUB-4U** (self-powered 7–36 V, metal) | 37 |
| Camera tether (data) | Tripp Lite **U026-016** (5 m active repeater, USB-A M/F) | 46 |
| USB power meter | YOJOCK USB tester (USB-**A**, 4–30 V) — for the P-001 brownout check | 16 |
| Battery | 3S **11.1 V** 3300 mAh 50C LiPo, Deans T-plug (2-pack) — has balance lead | 38 |
| Charger | BUBUCAM **B3AC** 2S–3S balance charger (charges via balance lead) | 20 |
| ESP32 power | DKARDU 5 V buck (4.5–24 V → 5 V 3 A, 10-pk) — LiPo → ESP32 | 15 |
| Hub-feed cap | 1000 µF **35 V** low-ESR electrolytic (across LiPo→hub feed) | 12 |
| Battery interface | 5-pair Deans T-plug **pigtails, 14 AWG** (bare wire → lever connectors) | 7 |
| Power distribution | Lever (Wago-style) connectors, 24–12 AWG | 25 |
| Signal wiring | Dupont jumper kit (M-F/M-M/**F-F**, 20 cm) — ESP32↔TB6612 logic | 9 |
| Camera mount | Small stainless **L-brackets** (zip-tie/P-clip the camera to it) | 9 |
| Cable mgmt | P-clip assortment + clip-on **ferrites** (tether EMI) | 48 |

**Power wiring:**
```
3S LiPo (T-plug) ─► Deans pigtail (bare wire) ─► lever connectors ─┬─► 2× TB6612  (motors)
                                                                   ├─► 5V buck ─► ESP32
                                                                   └─► Waveshare hub (+1000µF 35V cap) ─► camera @5V
camera ─► hub (USB-A) ─► U026-016 (5m active) ─► laptop ─► RTAB-Map
```

**⚠️ Watch-item — TB6612 vs the 12 V motors:** the TB6612 is light-duty (1.2 A/ch cont., 3.2 A peak).
The Hiwonder 12 V geared motors are fine at slow indoor speed under the firmware speed cap, but a
stall (hitting a wall) or aggressive driving will current-limit / warm the driver (protective, not
destructive). Fallback: the Hiwonder kit's **included controller board** is sized for those motors.

### Tools needed for the build
**Must-have:**
- **Soldering iron + solder (+ flux)** — the Adafruit TB6612 ships with loose header pins to solder
  on, and motor/power wires solder to its pads (Dupont can't carry motor current). The one
  unavoidable solder job. *(Solderless alternative: a screw-terminal motor driver instead of the TB6612.)*
- **Multimeter** — verify buck output = 5 V and **polarity** BEFORE connecting the ESP32; check the
  hub feed + continuity. Stops the magic smoke. (The USB tester only covers the camera USB rail.)
- **Wire strippers**, **flush cutters**, **precision screwdriver set** (+ hex/Allen keys; kit may include).

**Recommended:** zip ties (lots), heat-shrink + lighter/heat gun (insulate solder joints), double-
sided foam tape (mount modules), needle-nose pliers.
**Likely already have:** USB-C **data** cable (flash the ESP32), printer (calibration checkerboard).

### Assembly order
> 📖 **Full step-by-step walkthrough with wiring diagrams + the reasoning for each step:**
> [[land-rover-v1-build-guide]] (beginner-friendly build companion). The checklist below is the
> summary; the build guide is the do-this-then-that.

1. Assemble chassis (motors, wheels, deck).
2. Solder headers on the 2× TB6612; wire motor + power leads.
3. Power distribution: Deans pigtail → lever connectors → TB6612 / buck / hub-feed (+ cap). **Multimeter-check 5 V + polarity before connecting the ESP32.**
4. ESP32 ↔ TB6612 (Dupont, logic pins); flash `esp32_motor_teleop.ino` (set mecanum mixing — 4 wheels).
5. Mount camera low/stiff/central on the L-bracket; hub on chassis; run the tether.
6. **Bench-test the USB tether** (§7) — stream + flex, watch for dropouts (P-001).
7. **VIBRATION GATE (mecanum):** drive a slow line, review camera footage for blur. Don't trust the build until this passes (§3).

---

## 6. Upgrade path

1. **v1 (this page):** tether + ESP32 motors, laptop runs RTAB-Map.
2. **Tether annoying / want multi-room:** move camera capture to a **Pi 5**, MJPEG **pass-through**
   over 5 GHz (accept near-router throughput, keep the robot close), ESP32/Pi still drives motors.
3. **v2 untethered autonomy:** **Jetson Orin Nano** onboard running RTAB-Map + Nav2; laptop
   becomes an optional ground station. This is where [[system-architecture]]'s "onboard map must
   survive WiFi dropout" invariant kicks in.
4. ROS 2 migration (Phase 2): socket client → `teleop_twist_joy`→`cmd_vel`; Pi motor server →
   `cmd_vel` node; tether/mjpg → `usb_cam` + `image_transport` compressed; budget the
   DDS-over-WiFi fix ([[drone-comms-wifi]]).

---

## 7. Cheap empirical checks before committing

**Tether bench-test protocol (the make-or-break — run before committing, then again under motion):**
Assemble the full chain (laptop → active ext → externally-powered hub → camera; power the hub first).
1. **Enumerate:** `lsusb` shows `32e4:0035`; `v4l2-ctl --list-devices` shows the pair; `dmesg -w`
   in another terminal shows **no** disconnect / descriptor-read / over-current lines.
2. **Sustained stream (15 min):** stream full-res MJPG and count drops —
   `v4l2-ctl -d /dev/videoN --set-fmt-video=width=3840,height=1080,pixelformat=MJPG` then
   `--stream-mmap=3 --stream-count=27000 --stream-to=/dev/null` (≈15 min @30 fps). Pass = full
   frame count, no `dmesg` disconnects. (This also pins the real **MJPEG bitrate** vs the 80–150
   Mbps estimate, and the real **camera current draw** via an inline USB meter.)
3. **Power-stress:** re-plug the camera mid-stream → clean re-enumerate <1 s; run the motors and
   confirm **no** correlation between motor activity and `dmesg` USB events (rails isolated).
4. **Motion/flex (the differentiator):** mount on the chassis, drive ≥10 min while streaming and
   logging `dmesg -w | ts > usb_events.log`. **Pass = zero `usb disconnect` across the drive** while
   flexing the tether, turning, and tugging slack. Hand-wiggle each connector to find intermittents.
5. **Log results to the diary** (frames delivered, drops, `dmesg` events per config) — demonstrate,
   don't assert (Commandment V).

**If it drops even on a clean still bench → the camera unit is the fault, not the path** → escalate
P-001 as a hardware fault (RMA / different sample), don't quietly retry. Fallbacks in order:
repeater-cable+hub flakes on isoch timing → **StarTech Cat5e extender**; camera-is-faulty → RMA;
mobility untenable → the parked onboard-Pi + downscaled/H.264-over-WiFi path (§1, last resort).

**Chassis check:** drive a straight 3 m line on carpet *and* hardwood; check odometry drift and
review camera footage for blur, before locking the chassis/motor choice.

---

## Related
- [[home-tidy-drone-prototype]] — Phase-1 build plan + the (expensive, aerial-oriented) buy list this page supersedes for the first ground build; P-001 USB finding
- [[system-architecture]] — the platform-agnostic cognitive stack the rover carries; ground-robot pivot note (2026-05-30)
- [[passive-stereo-robustification]] — why full-res stereo quality matters (don't downscale away the texture)
- [[imu-vio-integration-reality]] — should the rig carry an IMU? (sync is the cost, not the chip; buy-nothing-yet)
- [[slam]] · [[map-then-navigate]] — the mapping the rig exists to serve
- [[drone-comms-wifi]] · [[ros2-server-bridge]] — the DDS-over-WiFi cost that justifies sockets-first for v1

## Sources
Chassis/power: Pololu Romi #3500/#3543; Hiwonder Large Metal 4WD; Waveshare WAVE ROVER (PiShop);
Yahboom ROSMASTER X3; Zbotic L298N-vs-DRV8833-vs-TB6612 comparison; Hackaday FET-vs-L298N;
Adafruit/PiShop UBEC; RPi forums power/brownout threads. Compute/comms: Tom's Hardware Pi 5 WiFi;
MagPi Pi 4 benchmarks; USB/IP USENIX paper; Microchip USB 2.0 isochronous bandwidth; Silex
network-USB webcam limits; Tripp Lite 15 m active USB; Logitech Strong (no bus power);
camera-streamer (ayufan). Software: jacksonliam/mjpg-streamer; raspivid_mjpeg_server (kig);
GStreamer H.264 latency thread; lewisroberts MJPEG@30; OpenCV stale-frame fix (Atomic Spin / OpenCV #13145);
pygame joystick; Articulated Robotics teleop; donskytech ESP32 WebSocket; Random Nerd ESP32 WiFi car.
(Full URLs in the `drone-prototype` session research handback, 2026-06-02.)
