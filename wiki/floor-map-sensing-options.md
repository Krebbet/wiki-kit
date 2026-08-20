# Cheap + DIY Sensing Options for a 2D Room Floor-Map

Research question: the prototype proved that **passive stereo (the SVPRO) cannot give crisp walls** for a navigation-anchor floor-map — clutter and textureless walls collapse the disparity/PnP on blank surfaces (EDA campaign; [[passive-stereo-room-mapping-campaign]], [[sensor-weaknesses-and-fixes]]). The team weighed an **Orbbec Gemini 2 (~$234 active-IR depth camera)** as the fix ([[economical-ir-depth-cameras]]), but the human judged $234 too expensive and asked: **is there a better-value option, with some DIY work, for the specific goal of a 2D wall-outline floor-map on a cheap indoor home robot?**

This page answers *that* narrow goal — a **2D floor polygon / wall outline** usable as a nav anchor — not "best depth sensor in general." The crucial reframing: a 2D wall outline does **not** need a 3D depth camera. It needs **one good horizontal ranging plane**. That is exactly what a cheap robot-vacuum-class **2D LiDAR** delivers, at well under half the Gemini 2's price, and it sidesteps the blank-wall problem entirely (a laser rangefinder does not care about texture).


> **Bottom line (2026-06-08):** For a 2D wall-outline floor-map, the best value is a **robot-vacuum-class 360° 2D LiDAR** — **LDROBOT LD19 / FHL-LD19 (~$99)** or **Slamtec RPLIDAR C1 (~$95)**: 360°, 12 m, DTOF (texture-independent → solves blank walls by construction), single-cable UART/USB, mature ROS2 drivers, near-zero DIY. This **beats the Gemini 2 ($234) by ~$135** for this goal. The **cheapest-first experiment** (≈$10–30, no buy) is a **DIY line-laser swept across the room, detected in the existing calibrated camera** to triangulate a wall cross-section — a poor-man's single-plane LiDAR to validate the floor-map pipeline before any purchase. The honest trade-off: a 2D LiDAR sees **only its scan plane** — no table-tops, no 3D object/obstacle extent — so it is a *floor-map / nav* sensor, not an object-mapping sensor. The project already plans to read 3D obstacle/object extent from the passive stereo + scene layers; the LiDAR's job is just the trustworthy wall polygon.

---

## 1. 2D LiDAR — the prime candidate (and the recommendation)

A spinning 360° 2D laser scanner returns range vs. angle in one horizontal plane. Run that through `slam_toolbox` / Cartographer and you get an occupancy grid; trace the occupied cells and you have the wall polygon ([[2d-lidar-slam]], [[slam-toolbox]]). **Why it fits the goal so well:**

- **Texture-independent.** A laser rangefinder measures time-of-flight (DTOF) or triangulation off the surface directly — a **blank white wall is its *easiest* target**, the exact case where passive stereo failed. This is the single biggest reason to prefer LiDAR over any camera for the wall-outline goal.
- **Robot-vacuum economics.** This sensor class is mass-produced for Roomba/Roborock-style vacuums, which is why 360° modules now sell for ~$95–142. ≤10 m range is plenty for a home room ([[robot-vacuum-navigation]]).
- **Near-zero DIY.** Single cable, a USB-UART adapter usually in the box, a maintained ROS2 node, and it drops straight into the existing SLAM stack.

### Current modules (≈2026 USD — verify before buying; LiDAR pricing moves)

| Model | Tech | Range | Scan / sample rate | Interface | ROS2 driver | ≈2026 price | DIY effort | Note for 2D floor-map |
|---|---|---|---|---|---|---|---|---|
| **LDROBOT LD06 / LD19 (FHL-LD19)** | DTOF | 0.02–12 m | 10 Hz / 4.5 kHz | UART (+USB adapter) | **Official** `ldlidar_stl_ros2`; also linorobot/Myzhar | **~$99** | Very low | **Top value.** Walnut-size, 30k-lux light resistance, mass-vacuum part. LD19≈LD06 with better far accuracy (±10 mm @ 3–12 m). |
| **Slamtec RPLIDAR C1** | DTOF fusion | 0.05–12 m | 10–20 Hz / 5 kHz | UART (+USB adapter) | **Official** `rplidar_ros` (sllidar) | **~$95** | Very low | **Co-top value.** Class-1 eye-safe, explicitly marketed for home robots; reflectivity/"2.5D" output; strongest vendor support + docs. |
| LDROBOT STL-27L | DTOF | 0.03–25 m | 10 Hz / 21.6 kHz | UART (+USB adapter) | Official `ldlidar_stl_ros2` | ~$142 | Very low | Higher sample rate + longer range than needed for one room; pay up only if you want denser scans. |
| LDROBOT D500 / LD19P | DTOF | 0.2–30 m | 8–12 Hz | UART/USB-CDC | Official | ~$70–90 | Very low | Dev-kit form; DToF good on glossy floors. |
| Slamtec RPLIDAR A1 | Triangulation | 0.2–12 m | 5.5–10 Hz / 8 kHz | UART (+USB adapter) | Official `rplidar_ros` | ~$99 | Very low | The long-standing budget benchmark; triangulation is slightly worse than DTOF on dark/glossy surfaces. C1 supersedes it at the same price. |
| YDLIDAR T-mini Plus | DTOF | 0.05–12 m | 6–12 Hz / 4 kHz | UART (+USB adapter) | Official (ROS1/ROS2) | ~$96–126 | Very low | Tiny (38 mm), strong-light resistant, vacuum-targeted. Solid alternative to LD19/C1. |
| YDLIDAR X2 / X3 / X4 | Triangulation | ~8–10 m | 5–12 Hz / 3–5 kHz | UART/USB | Official | ~$65–90 | Very low | Cheapest spinning option; triangulation, shorter effective range; fine for a small room. |
| LDROBOT LD20 / FHL-LD19 Plus | DTOF | 0.02–**25–30 m** | 10–13 Hz | UART (+USB adapter) | Official | ~$120–150 | Very low | "2× LD19" long-range variants; range overkill for one room. |
| Vacuum-LDS salvage (Neato XV-11, LDS-006, LDS-01RR) | Triangulation | ~3–8 m | ~2 kHz | UART | Community `kaiaai/LDS` | **~$16 used** | Medium (reverse-eng. wiring/driver) | Cheapest of all; prototype-only, not production-clean. Good if you want to spend ~$0 and already have a junk vacuum. |

**Recommendation within the class:** **LDROBOT LD19 (~$99)** or **Slamtec RPLIDAR C1 (~$95)** — pick on which has the better stock/price the week you buy. Both are 360° DTOF, 12 m, eye-safe, single-cable, with **official maintained ROS2 drivers**, and both are texture-independent so they solve the blank-wall failure by construction. The C1 has the strongest vendor docs/support and explicit home-robot positioning; the LD19 is the cheapest mass-vacuum part with equally good community + official ROS2 support. Avoid paying up for STL-27L/LD20-class range (25–30 m) — a single home room never needs it. *(synthesis)*

---

## 2. DIY line-laser triangulation reusing the existing calibrated camera — the cheapest-first experiment

**Idea:** project a **horizontal line laser** across the room, detect the bright line in the existing (already calibrated) camera image, and triangulate each illuminated pixel against the known camera↔laser-plane geometry → a single horizontal **wall cross-section profile**. Sweep/rotate the rig (or the robot) and you accumulate a poor-man's single-plane LiDAR. This is the same physics as a vacuum's structured-line collision sensor and as industrial laser-triangulation profilometers (see Sources). **Cost ≈ $10–30** for a line-laser module (we already own the camera).

| Aspect | Assessment for a 2D floor-map |
|---|---|
| **What it gives** | One horizontal range profile per frame → wall/obstacle cross-section at the laser height; accumulate over a sweep → 2D outline. Texture-independent (the laser *is* the texture) — directly attacks the blank-wall failure. |
| **Cost** | Line-laser module **~$10–30** (650 nm red, or 850 nm IR for invisibility — IR needs the camera's IR-cut removed or an IR-sensitive cam). Camera already owned. |
| **Accuracy / range** | Triangulation is very accurate up close (sub-mm at bench range) but accuracy **degrades with distance squared**; at room range (3–5 m) with a short camera-laser baseline it is coarse but usable for a wall outline. Longer baseline → better far accuracy but bulkier rig. |
| **Ambient-light limit** | The real catch. A cheap visible-red line **washes out under normal room lighting** at multi-metre range — the same ambient-wash that the [[economical-ir-depth-cameras]] page flagged for visible-red dot projectors. Mitigations: a narrow band-pass filter matched to the laser + short camera exposure, or go to 850 nm IR with an IR-pass filter. Works best dim/at-distance-limited. |
| **Calibration effort** | Must calibrate the **laser-plane pose relative to the camera** (one-time): image the line on a known plane at several depths, fit the laser plane in camera frame. Medium effort but a well-trodden recipe (laser-displacement / structured-light calibration). |
| **DIY effort** | Medium. Line detection (per-column bright-pixel sub-pixel peak) + plane-triangulation is ~100 lines; the calibration rig and ambient-light tuning are the time sinks. |

**Verdict: yes — viable and the right *first* experiment.** It is near-zero cost, reuses owned hardware, validates the entire floor-map → polygon → nav-anchor pipeline on *texture-independent* data, and tells you whether a single horizontal ranging plane is enough for the nav map **before** spending on a LiDAR. Its limitations (ambient-light wash, calibration fuss, no 360° in one shot) are exactly the limitations the ~$95 LiDAR removes — so treat it as a **cheap proof-of-concept that de-risks the LiDAR buy**, not as the shipping sensor. *(synthesis)*

---

## 3. Cheap ToF options (single-zone / multi-zone / ToF cameras)

Solid-state ToF chips are cheap but **narrow-FoV and short-range** — they measure a small cone in front, not a 360° plane, so they need mechanical scanning to build a room outline.

| Sensor | Output | Range | FoV | Interface | ≈2026 price | Scanning needed for floor-map? | Note |
|---|---|---|---|---|---|---|---|
| **VL53L1X** | 1 zone (single distance) | up to ~4 m | ~27° (programmable ROI) | I²C breakout | ~$12–15 | **Yes** — single beam; must pan | Vacuum collision-sensor class; not a mapper on its own. |
| **VL53L5CX** | **8×8 multi-zone** | 2–400 cm | ~63–65° diagonal | I²C breakout | ~£16 / ~$20 | Yes (covers a 65° cone; pan to fill 360°) | Cheapest "depth-ish" array; 64 zones at 60 Hz. Coarse but real multi-point. |
| **VL53L8CX / L9** | 8×8 multi-zone | longer / better ambient | ~65° | I²C/SPI | ~$25–35 | Yes | Newer L5 successors; better ambient + range. |
| ST **TMF8828** (AMS) | 3×3 / up to 8×8 histogram | up to ~5 m | ~63° | I²C | ~$15–25 breakout | Yes | Multi-object-per-zone histogram dToF; similar role to VL53L5CX. |
| **ToF *cameras*** (full 2D depth) | dense depth image | — | wide | USB | mostly **> $150** | No (full frame) but pricey | Sub-$150 standalone ToF cameras are scarce/unreliable; the cheap depth path is active-IR *stereo* (§4), not a standalone ToF cam. |

**Read-out:** the cheap ToF *chips* (VL53L5CX, TMF8828) are genuinely cheap (~$20) and texture-independent, but each sees only a ~65° cone to ~4 m — to make a room outline you must **build a panning mount** (a servo sweeping a VL53L5CX is a known DIY "scanning LiDAR" hack). That mechanical scanner ends up **more DIY work for less coverage and shorter range** than just buying a $95 spinning 2D LiDAR that already does 360° to 12 m. ToF chips are the right answer for a cheap *collision/cliff* sensor layer, **not** for the primary floor-map. *(synthesis)*

---

## 4. Active-stereo / structured-light depth cameras — the low-end reference (and why it's more than this goal needs)

Covered in depth in [[economical-ir-depth-cameras]]; summarized here for the floor-map decision.

| Camera | Active IR? | Range | ≈2026 price | For a 2D floor-map |
|---|---|---|---|---|
| **Orbbec Gemini 2** | Yes (850 nm active stereo) | 0.15–10 m | **$234** | The prior pick. Solves blank walls, but a *full 3D camera* for a *2D outline* — overspend for this goal. |
| RealSense D435 / D435i | Yes (IR dot projector) | 0.3–3 m (max ~10) | ~$314 / $334 | The "what the papers use" reference; pricier than Gemini 2. |
| Orbbec Astra / Astra Pro | Yes (structured light) | 0.6–8 m | ~$150–200 | Older structured-light; cheaper than Gemini 2 but aging SDK; still a 3D cam for a 2D job. |
| Kinect v1/v2 (salvage) | Yes (SL / ToF) | ~0.5–4.5 m | ~$20–40 used | Salvage-cheap and IR-active, but bulky, USB-hungry, dead SDKs, no clean ROS2 — false economy. |
| DIY OV9281 NoIR stereo + IR DOE projector | Yes | room | ~$80–135 | The cheapest *active-stereo* path ([[economical-ir-depth-cameras]] §3); cal+sync DIY; still gives 3D, more than the outline needs. |

**Why a depth cam is more than a 2D floor-map needs:** a depth camera reconstructs a full 3D point cloud (table-tops, object extent, overhead clutter) — valuable for *object* mapping and 3D obstacle avoidance, but for a **wall-outline floor polygon** you only consume one horizontal slice of it. You pay $234+ for 3D and throw most of it away. The **price floor for a turnkey active-IR depth cam is ~$150–234** (Astra → Gemini 2); a 2D LiDAR delivers the wall outline more robustly (no IR-projector range limits, true 360° in one spin) for **~$95**. The depth cam only wins if the project also wants 3D extent from this *same* sensor — but the project already gets 3D/object extent from the passive stereo + scene layers ([[system-architecture]], [[stereo-dense-reconstruction]]), so the floor-map sensor does not need to. *(synthesis)*

---

## 5. Decision

| Need | Best value | Price | Why |
|---|---|---|---|
| **2D wall-outline floor-map (the goal)** | **LDROBOT LD19 or RPLIDAR C1** (360° DTOF 2D LiDAR) | **~$95–99** | Texture-independent (solves blank walls), 360°×12 m in one spin, official ROS2, near-zero DIY. **−~$135 vs Gemini 2.** |
| **Cheapest-first experiment (no buy)** | **DIY line-laser + existing calibrated camera** | **~$10–30** | Validates the floor-map → polygon → nav-anchor pipeline on texture-independent data before any purchase; de-risks the LiDAR buy. |
| Cheap collision/cliff layer (not the map) | VL53L5CX 8×8 / TMF8828 ToF | ~$20 | Cheap, texture-independent, but ~65° cone — needs panning; wrong tool for the primary outline. |
| If 3D object/obstacle extent wanted from one sensor | Orbbec Gemini 2 (active-IR stereo) | $234 | Full 3D; overspend if only the 2D outline is needed. See [[economical-ir-depth-cameras]]. |

**Recommended path:** (1) run the **~$10–30 line-laser experiment first** to prove a single horizontal ranging plane yields a usable wall polygon on our blank walls and to exercise the SLAM/polygon code; then (2) if a real sensor is bought, get the **LD19 / RPLIDAR C1 (~$95–99)** rather than the Gemini 2 — same blank-wall fix, true 360°, ~$135 cheaper, drops into the existing `slam_toolbox` stack.

**Honest trade-off (state it plainly):** a **2D LiDAR sees only its single scan plane** — it will *not* see table-tops, chair seats, low floor clutter below/above the plane, or any 3D object extent. It is a **floor-map / wall-outline / nav sensor, not an object-mapping sensor.** That is acceptable *here* because the mandate's floor-map goal is exactly a 2D wall polygon for a nav anchor, and the project reads 3D object/obstacle extent from the separate passive-stereo + scene-graph layers ([[system-architecture]], [[scene-graph-world-model]]). If the team later wants the *floor-map sensor itself* to also carry 3D obstacle avoidance, revisit the Gemini 2 / Unitree L1 3D-LiDAR tier ([[cheap-lidar-pricing-guide]]) — a different, more expensive sensor-class decision. *(synthesis)*

---

## Source

Web (≈2026, accessed 2026-06-08):
- LDROBOT LD06/LD19/STL-27L official ROS2 driver — github.com/ldrobotSensorTeam/ldlidar_stl_ros2; community drivers github.com/linorobot/ldlidar, github.com/Myzhar/ldrobot-lidar-ros2
- LDROBOT LD06 (~$99, DTOF, 0.02–12 m, 10 Hz, 4.5 kHz), LD19 (10 mm acc @ 3–12 m), STL-27L (~$142, 0.03–25 m, 21.6 kHz) — specs via kaiaai/awesome-2d-lidars (github.com/kaiaai/awesome-2d-lidars), inno-maker.com/product/lidar-ld06, dfrobot.com/product-2726.html (STL-27L)
- FHL-LD19 (12 m, 30k-lux resistant, ROS/ROS2 SDK, ~walnut size) and FHL-LD19 Plus (25 m, "2× LD19") — youyeetoo.com/products/fhl-ld19-lidar-sensor; amazon.com FHL-LD19 Plus (B0DG8MCGVG); LD19 retail ~$99–135 across AliExpress/RobotShop/DFRobot
- Slamtec RPLIDAR C1 (DTOF fusion, 12 m, 360°, 5 kHz, Class-1 eye-safe, ROS/ROS2, home-robot positioning) — slamtec.com/en/c1; robotshop.com RPLIDAR C1; waveshare.com/rplidar-c1.htm; ~$94–96 Amazon/Waveshare (per [[cheap-lidar-pricing-guide]])
- Slamtec RPLIDAR A1 (triangulation, 0.2–12 m, ~$99) — slamtec.com/en/lidar/a1
- YDLIDAR T-mini Plus (DTOF, 0.05–12 m, 4 kHz, 6–12 Hz, UART+USB adapter, ROS1/ROS2, strong-light resistant, ~38 mm) — ydlidar.com/product/ydlidar-t-mini-plus; amazon.com YDLIDAR T-mini Plus (B0DWSKYLT8); robotshop.com; retail ~$96–126
- YDLIDAR X2/X3/X4 (triangulation, ~$65–90) — per kaiaai/awesome-2d-lidars and [[cheap-lidar-pricing-guide]]
- Vacuum-LDS salvage (Neato XV-11, LDS-006, LDS-01RR, ~$16 used) + community driver — github.com/kaiaai/awesome-2d-lidars (kaiaai/LDS)
- Laser line triangulation principle / accuracy / ambient-light robustness — at-sensors.com/knowledge-base/laser-triangulation-measuring-principle; ncbi.nlm.nih.gov/pmc/articles/PMC7146149 (uncertainty study); arxiv.org/pdf/1907.12172 (stereo + structured IR laser ring, mm-level); photonfocus.com (3D laser profiling)
- VL53L5CX (8×8 multizone dToF, 2–400 cm, ~63–65° diagonal, 60 Hz) — st.com VL53L5CX; pololu.com/product/3417; shop.pimoroni.com (~£16); sparkfun.com Qwiic ToF Imager
- VL53L1X (single-zone, ~4 m, ~27° ROI, ~$12–15) and TMF8828 (3×3/8×8 histogram dToF, ~5 m) — st.com / ams.com product pages; common breakout pricing
- Active-IR depth cams (Gemini 2 $234, D435/D435i, Astra, Kinect salvage, DIY OV9281+IR-DOE) — see [[economical-ir-depth-cameras]] (full current pricing + sources, accessed 2026-06-07)

Wiki cross-refs: [[economical-ir-depth-cameras]] (active-IR depth-cam pricing + the Gemini 2 prior rec), [[cheap-lidar-pricing-guide]] (full 2D/3D LiDAR pricing table, Unitree L1 3D tier), [[2d-lidar-slam]] (RPLIDAR/LDROBOT SLAM stack, Cartographer/SLAM-Toolbox), [[passive-stereo-room-mapping-campaign]] (the blank-wall finding that motivates this page), [[sensor-weaknesses-and-fixes]] / [[passive-stereo-robustification]] (why passive stereo fails on walls), [[dot-projector-options]] (IR projector survey), [[system-architecture]] / [[scene-graph-world-model]] (where 3D object extent comes from instead).

*(synthesis — assembled 2026-06-08 from current vendor/distributor listings + the wiki's existing sensor pages. Verify prices before purchase; LiDAR and breakout pricing moves. Prices given as ranges where listings disagreed.)*

## Related

[[economical-ir-depth-cameras]] · [[cheap-lidar-pricing-guide]] · [[2d-lidar-slam]] · [[passive-stereo-room-mapping-campaign]] · [[sensor-weaknesses-and-fixes]] · [[passive-stereo-robustification]] · [[close-range-depth-sensors]] · [[dot-projector-options]] · [[robot-vacuum-navigation]] · [[slam-toolbox]] · [[system-architecture]] · [[home-tidy-drone-prototype]]
