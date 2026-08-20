# Economical Active-IR Depth Cameras for Blank-Wall Room Mapping

Research question: the prototype proved passive stereo (the SVPRO) **cannot recover depth on blank, textureless walls** — the "floor-map problem" (`drone-prototype` EDA010/EDA011; [[sensor-weaknesses-and-fixes]], [[passive-stereo-robustification]]). The diagnosed cure is **active IR stereo**: an IR dot/speckle projector paints texture on the wall and an IR-sensitive stereo pair triangulates depth on it — removing ambient-light wash-out and the spurious-far disparity-near-zero readings that collapsed PnP. A cheap *visible-red* speckle projector fails at room range (red is nearly invisible to grayscale matching and washes out in ambient light), which forces the move to IR. The human wants **the most economical IR active-depth option — explicitly cheaper than the wiki's current recommendations** (Unitree L1 $249, RealSense D435i $334), without breaking the bank at the prototype stage.

This page is the dedicated, current-pricing (≈2026 USD) answer. It complements [[passive-stereo-robustification]] §6 (which already sketches the hardware ladder) and [[close-range-depth-sensors]] (manipulation-range cameras), and it explicitly re-prices the recommendation against the LiDAR path in [[cheap-lidar-pricing-guide]].


> **Decision update (2026-06-07 campaign, [[passive-stereo-room-mapping-campaign]] §(d)):** an active-IR depth sensor is now an **upgrade** (wall-trustworthy / larger-room nav map), **not** required to unblock navigation — Goal 2 (collision-free path on the relocalizable map) is demonstrable on existing passive data (EDA023/024). Cheapest path to trustworthy walls is software/capture first: a **perimeter-floor re-capture with the existing camera** (hug walls, camera angled down at the floor-wall junction) — try before buying. If hardware is bought, the **Gemini 2 ($234)** below remains the top pick.

> **What the wiki currently recommends (the prices to beat):**
> - [[sensor-weaknesses-and-fixes]] / [[passive-stereo-robustification]] §6 rung D: turnkey **RealSense D435i — $334** (active IR stereo + IR projector + IMU + factory calibration).
> - [[cheap-lidar-pricing-guide]] Tier 2: **Unitree L1 3D LiDAR — $249** (the floor-map / blank-wall fix via direct ranging, not stereo).
> - [[passive-stereo-robustification]] §6 rung C: a DIY **OV9281 NoIR stereo + 850 nm IR DOE projector ≈ $80–150** is named as the "product-shaped budget answer" but was never costed against real 2026 listings — this page does that.

---

## 1. Why infrared, not visible-red (the constraint that drives the choice)

Active stereo works because **depth comes only from the camera-pair geometry**; the projector is uncalibrated "scene paint" that gives the matcher something to lock onto on a blank wall ([[passive-stereo-robustification]] §4). For that paint to survive at room range it must be:

- **High-contrast against ambient light.** Visible-red dots wash out under normal room lighting; an 850 nm IR pattern read through an **IR band-pass filter** suppresses ambient light and lifts dot contrast dramatically. RealSense's own measurement: a blank-wall depth range of **~3 m passive extends to ~10 m with the projector on + IR filtering** [src-web: RealSense projector white paper / tuning docs, via [[sensor-weaknesses-and-fixes]]].
- **Invisible to occupants** (a roaming home robot lighting up a visibly red room is a non-starter). 850 nm is faintly visible as a dim red glow at the emitter; **940 nm** is fully invisible but loses some sensor sensitivity. 850 nm is the indoor standard; 940 nm is preferred for outdoor/sunlight rejection [src-web: Digigram VCSEL DOE product page — "850nm for indoor, 940nm for outdoor"].

This is exactly how RealSense D4xx, Orbbec Gemini, OAK-D Pro and the original Kinect work. The decision is therefore **which IR-active package gives blank-wall depth at 0.5–5 m, on Linux/ROS, for the least money** — not whether to go IR.

---

## 2. Off-the-shelf active-IR depth cameras (projector built in)

All-in-one modules: IR-sensitive stereo pair **plus** an integrated IR dot projector, factory-calibrated, single USB cable, vendor SDK. Prices ≈2026 USD.

| Camera | Active IR projector? | Stereo baseline | Depth range (ideal) | IMU | USB / Linux / ROS | ≈2026 price | Notes |
|---|---|---|---|---|---|---|---|
| **Orbbec Gemini 2** | **Yes — 850 nm active stereo IR** | 50 mm | 0.15–10 m (ideal **0.2–5 m**), ≤2 % @ 2 m | **Yes** | USB-C 3.0; Orbbec SDK + ROS/ROS2 wrapper | **$234** | **Best all-in-one value.** Direct turnkey match to our use case; built-in projector, IMU, factory cal [src-web: store.orbbec.com/products/gemini-2; orbbec.com Gemini 2 specs]. |
| RealSense **D435** | Yes — IR dot projector | 50 mm | 0.3–3 m (max ~10 m) | No | USB-C; librealsense + realsense-ros | ~$314 | The classic active-IR room camera; D435i adds IMU [src-web: intel.com D435i specs; [[close-range-depth-sensors]]]. |
| RealSense **D435i** | Yes — IR dot projector | 50 mm | 0.3–3 m (max ~10 m) | **Yes (BMI055)** | USB-C; librealsense + realsense-ros | **$334** | The wiki's current turnkey rec; Gemini 2 undercuts it by **$100** with the same capability set [src: [[sensor-weaknesses-and-fixes]]; intel.com]. |
| RealSense D455 | Yes | 95 mm | 0.6–6 m | Yes | same | $419 | Wider baseline → better far-field; over budget. |
| Luxonis **OAK-D Pro** | **Yes — IR dot projector + flood** | 75 mm | 0.7–12 m | Yes | USB-C; DepthAI (Linux/ROS); onboard AI | **$429** | Active IR + onboard NN inference, but **pricier than D435i** — skip on cost [src-web: shop.luxonis.com/products/oak-d-pro]. |
| Luxonis OAK-D Lite | **No projector** | 75 mm | passive only | No | DepthAI | $169 | Cheap, but **passive** — does NOT solve the blank-wall problem. Disqualified. |
| RealSense **D405** | **No projector** (passive, short-range) | ~18 mm | 0.07–0.5 m | No | librealsense | $272 | Arm-manipulation specialist; passive; wrong range. Not a room sensor [src-web: store.intelrealsense.com D405]. |
| RealSense D421 (module) | **No projector** (passive) | 50 mm | stereo | No | librealsense | ~$80 (10-pack = $800) | Bare passive module; no projector → no blank-wall fix [src-web: store.intelrealsense.com D421; therobotreport.com]. |
| Microsoft **Kinect Azure** | Yes (ToF, not stereo) | — | 0.5–5.5 m | Yes | discontinued | EOL | **Discontinued Oct 2023**; lineage → Orbbec Femto. Avoid for a new build [src-web: therobotreport.com; b2bnn.com migration guide]. |
| Original **Kinect v1/v2** | Yes (v1 structured light, v2 ToF) | — | ~0.5–4.5 m | — | salvage; community SDKs | ~$20–40 used | Salvage-cheap and IR-active, but **bulky, USB-power-hungry, dead SDKs, no clean ROS2** — false economy for a mobile prototype. |
| Occipital Structure Core | Yes — IR projector | ~58 mm | 0.3–5 m | Yes | USB; Structure SDK | ~$400+ (niche) | Capable but niche/pricey; over budget. |

**Read-out:** among turnkey "just buy it and it works on Linux" modules, the **Orbbec Gemini 2 at $234** is the cheapest that actually has a built-in IR projector and covers our 0.2–5 m room range with an IMU — **$100 under the D435i** and **$15 under the Unitree L1**, while solving the blank-wall problem by the same active-IR mechanism the wiki already endorsed.

---

## 3. IR stereo camera + separate IR projector (the DIY parts path)

Cheaper *in parts* than any all-in-one: buy an **IR-sensitive (no IR-cut) global-shutter stereo module** and add a **standalone 850 nm IR dot projector**. Global shutter is a real bonus over the SVPRO's rolling shutter for a moving robot.

**IR-sensitive stereo camera (no IR-cut filter):**

| Module | Sensor | IR-sensitive | Shutter | Sync | Interface | ≈2026 price |
|---|---|---|---|---|---|---|
| Arducam OV9281 mono module (×2) | OV9281 1 MP mono | **Yes (NoIR mono)** | Global | needs CamArray HAT for hw-sync | MIPI CSI | ~$26–36 / cam [src-web: arducam.com OV9281 module pages] |
| Arducam OV9281 stereo bundle (2× cam + CamArray HAT) | OV9281 ×2 | Yes | Global | **hw-synced** | MIPI CSI (1 slot) | ~$90–130 kit [src-web: robotshop / arducam.com OV9281 stereoscopic bundle] |
| **ELP dual-lens OV9281 USB stereo** | OV9281 ×2 | **Yes — no IR-pass/cut, IR-sensitive** | Global | hw-synced, single USB | **USB 2.0/UVC (plug-and-play)** | ~$70–110 [src-web: amazon.com ELP OV9281 binocular B0D9VY8JG4] |
| Goobuy USB3 OV9281 dual | OV9281 ×2 | Yes (mono) | Global | µs hw-sync | USB 3.0 | ~$120 [src-web: okgoobuy.com OV9281 stereo] |

The **ELP USB OV9281 binocular** is the most prototype-friendly: UVC plug-and-play on Linux (no MIPI/HAT plumbing), global shutter, IR-sensitive out of the box.

**Standalone 850 nm IR projector — the catch:** *(full projector-product survey with dot counts, power, FOV, eye-safety class and ≈2026 prices in [[dot-projector-options]]):*

- **Do NOT buy a cheap AliExpress "850 nm focusable dot module" (~$5–15).** Those are **single-dot lasers** — the wrong tool. Active stereo needs a *field* of dots (a DOE/diffractive speckle), not one spot [src-web: aliexpress 850 nm laser dot modules — single-dot].
- A real **VCSEL + DOE dot projector** (ams-OSRAM BELAGO1.1/1.2, BELICE-SD; Digigram; Engage Photonics) projects 5k–15k dots at 850/940 nm — but these are **bare COB/SMT components** (~3.5×3.5 mm, reflow-mount), not a consumer plug-in, and sold through Mouser/distributors at component MOQs [src-web: ams-osram.com BELAGO; digigram.com.tw VCSEL DOE; mouser.com BELAGO]. Usable for a *product*, awkward for a *bench*.
- **Practical cheap field-of-dots options for a prototype:** (a) a **salvaged RealSense/Kinect-clone IR projector module** off AliExpress (~$10–25, sold as D435 "infrared projector replacement"); (b) an 850 nm **machine-vision structured-pattern projector** (Smart Vision Lights SXP30-850 / Machine Vision Direct ODSXP30-850) — clean DOE pattern but **$200–400+**, which erases the parts savings; (c) reuse our **existing visible pico/speckle projector** only for short-range bench validation (it already showed the mechanism works close-up).

**Parts-path all-in cost:** ELP OV9281 stereo (~$70–110) + a salvaged IR DOE projector (~$10–25) ≈ **$80–135** — genuinely cheaper than the Gemini 2, *if* the DIY integration is acceptable.

---

## 4. The single cheapest viable path (recommendation)

Two honest answers depending on how much integration pain is acceptable; both beat the current wiki recs.

### Pick A (recommended) — Orbbec Gemini 2, **$234**, turnkey
The cheapest **zero-integration** active-IR option that just works. Built-in 850 nm IR projector, 0.2–5 m room range, IMU, USB-C, Orbbec SDK + ROS/ROS2. **$100 under the D435i**, **$15 under the Unitree L1**, and it attacks the blank-wall failure by the exact mechanism the wiki diagnosed as the cure. No calibration, sync, or projector sourcing. **This is the recommended buy** for the prototype's active-stereo step: it removes the D435i's price premium without giving up turnkey reliability.

### Pick B (cheapest absolute) — DIY ELP OV9281 NoIR stereo + salvaged IR DOE projector, **≈ $80–135**
The lowest sticker price and **global shutter** (better than the SVPRO and the D435i's rolling-ish behavior for a moving camera). The cost is real engineering: source a genuine *field-of-dots* IR projector (not a single-dot laser), stereo-calibrate, time-sync, and add an IR band-pass filter. This is [[passive-stereo-robustification]] §6 rung C, now priced. Choose it only if the ~$100 saving over the Gemini 2 is worth the calibration/sync work — for a disposable Phase-1 prototype that wants a result fast, it usually is **not**.

### What to avoid
- **OAK-D Lite ($169), RealSense D405 ($272), D421 module** — cheap but **passive / no projector**; they do **not** fix blank walls.
- **OAK-D Pro ($429), D455 ($419), Structure Core (~$400+)** — capable but **pricier than the D435i**; no reason to pay more.
- **Kinect Azure / v1 / v2** — discontinued or salvage-only; bulky, power-hungry, no clean ROS2 — false economy.
- **AliExpress single-dot 850 nm laser** — wrong tool; you need a DOE speckle field.

---

## 5. How this compares to the current wiki path

| Option | ≈2026 price | Blank-wall depth? | Turnkey? | vs current rec |
|---|---|---|---|---|
| **Orbbec Gemini 2 (this page)** | **$234** | **Yes (active IR stereo)** | **Yes** | **−$100 vs D435i, −$15 vs L1** |
| DIY OV9281 NoIR + IR DOE (this page) | **$80–135** | Yes (active IR stereo) | No (cal/sync/filter) | **−$200 vs D435i**, cheapest |
| RealSense D435i (wiki rec) | $334 | Yes | Yes | baseline turnkey rec |
| Unitree L1 3D LiDAR (wiki rec) | $249 | Yes (direct ranging, not stereo) | Yes | different sensor class |

**Bottom line:** the wiki's turnkey active-IR rec (D435i, $334) is **overpriced for what we need** now that the **Orbbec Gemini 2 ($234)** exists — same capability set (active 850 nm IR stereo + IMU + factory cal + Linux/ROS), $100 cheaper, and it also undercuts the Unitree L1. For the most economical turnkey active-IR depth, **switch the default recommendation to the Gemini 2**; keep the DIY OV9281+IR-DOE path (~$80–135) as the absolute-cheapest, integration-heavy fallback, and keep the D435i only as the "it's-what-the-papers-use" reference camera. The Unitree L1 remains the answer if the project later decides direct LiDAR ranging beats active stereo (a separate sensor-class decision — see [[cheap-lidar-pricing-guide]], [[2d-lidar-slam]]).

---

## Source

Web (≈2026, accessed 2026-06-07):
- Orbbec Gemini 2 — store.orbbec.com/products/gemini-2 ($234); orbbec.com/products/stereo-vision-camera/gemini-2/ (850 nm active stereo IR, 0.15–10 m, ≤2 % @ 2 m, 50 mm baseline, IMU, USB-C, Orbbec SDK)
- Intel RealSense D435i specs — intel.com/.../intel-realsense-depth-camera-d435i/specifications.html; store.intelrealsense.com/buy-intel-realsense-depth-camera-d435i.html ($334 per [[sensor-weaknesses-and-fixes]])
- RealSense D405 ($272, passive) / D421 (passive module, 10-pack $800) — store.intelrealsense.com; therobotreport.com/intel-realsense-d421-offers-low-cost-depth-sensing-for-robots/
- Luxonis OAK-D Pro ($429, IR dot projector, 75 mm baseline, 0.7–12 m) — shop.luxonis.com/products/oak-d-pro; OAK-D Lite ($169, passive) — shop.luxonis.com/products/oak-d-lite-1
- Arducam OV9281 mono NoIR global-shutter modules (~$26–36) and stereo bundle + CamArray HAT — arducam.com OV9281 pages; robotshop.com Arducam stereoscopic kit
- ELP dual-lens OV9281 mono global-shutter USB stereo, IR-sensitive (no IR-pass/cut) — amazon.com B0D9VY8JG4; Goobuy USB3 OV9281 dual — okgoobuy.com/OV9281-global-shutter-camera.html
- Standalone IR dot/DOE projectors: ams-osram.com BELAGO1.1/1.2 + BELICE-SD (VCSEL, 5k–15k dots, 850/940 nm); digigram.com.tw VCSEL DOE (850 nm indoor / 940 nm outdoor); enphotonics.com random-pattern projectors; machinevisiondirect.com ODSXP30-850 / SXP30-850 (850 nm pattern, $200–400+); aliexpress 850 nm focusable single-dot modules (the wrong tool)
- Azure Kinect discontinued Oct 2023, lineage → Orbbec Femto — therobotreport.com/microsoft-ending-production-of-azure-kinect-developer-kit/; b2bnn.com/2026/05/azure-kinect-discontinued-a-developers-migration-guide/

Wiki cross-refs: [[sensor-weaknesses-and-fixes]] (D435i $334, active-IR cure mechanism, ~3 m→~10 m blank-wall range), [[passive-stereo-robustification]] §4/§6 (active-stereo geometry + hardware ladder rungs A–D), [[close-range-depth-sensors]] (D405/D435/OAK-D specs + prices), [[cheap-lidar-pricing-guide]] (Unitree L1 $249).

*(synthesis — assembled 2026-06-07 from current vendor listings + the wiki's existing sensor pages; verify prices before purchase, as camera/component pricing moves.)*

## Related

[[passive-stereo-room-mapping-campaign]] · [[sensor-weaknesses-and-fixes]] · [[passive-stereo-robustification]] · [[close-range-depth-sensors]] · [[stereo-dense-reconstruction]] · [[cheap-lidar-pricing-guide]] · [[2d-lidar-slam]] · [[system-architecture]] · [[home-tidy-drone-prototype]]
