# DIY Active-IR-Stereo Depth Rig — Concrete Parts Shortlists (≈2026 USD)

**What this is:** a buy-list for a *homemade RealSense* — an **IR dot/speckle pattern projector + a pair of IR-capable cameras** wired into a passive-stereo pipeline to recover **camera-based 3D depth** (object/obstacle extent, table-tops, clutter — not just the flat 2D wall outline). The projector paints texture on blank walls so the stereo matcher can triangulate; the cameras must *see* that 850 nm pattern (most webcams, including the existing SVPRO, block it with an IR-cut filter).

> **Scope note — this is the SECONDARY sensor.** The **primary floor-map sensor is already chosen: a ~$95 Slamtec RPLIDAR C1 360° 2D LiDAR** ([[floor-map-sensing-options]]). The C1 is texture-independent (DTOF) and solves the blank-wall *wall-outline* problem by construction — it does NOT need this rig. This DIY active-IR-stereo rig is **only** for getting **3D depth of objects/obstacles** (the dimension a 2D LiDAR can't see — it sees only its scan plane). Build this rig only if/when camera-based 3D object depth is wanted on top of the LiDAR floor map.

> **Read first — the cheaper turnkey alternative:** [[economical-ir-depth-cameras]] concludes that a **used/new Orbbec Gemini 2 ($234)** gives the *same* active-IR-stereo capability factory-aligned, with the projector + IR-pass filtering + IMU + Linux/ROS built in, zero calibration/sync work. This DIY page exists because the human explicitly asked for the homemade-parts route; the honest verdict (§6) is that **the DIY rig is only worth it if the parts come in well under a used depth cam AND the integration time is acceptable** — for a disposable Phase-1 prototype it usually is not.


---

## TL;DR

- **Genuine consumer dot/speckle IR projectors are scarce.** Almost everything on Amazon/AliExpress sold as "IR illuminator," "850 nm IR board," or "night-vision" is a **FLOOD** — uniform IR light that adds **zero texture** and is **useless for stereo**. Real *field-of-dots* projectors (VCSEL/laser + DOE) are mostly **machine-vision / OEM components** (RFQ, MOQ, reflow-mount), not retail plug-ins.
- **The most prominent cheap, correct dot projector for a maker is a used Microsoft Kinect v1 (model 1414, ~$9–25 used).** Its built-in ~830 nm Class-1 random-speckle projector is a real DOE field-of-dots — salvage the projector (or use the whole sensor). This is the headline cheap path. Second is a **salvaged "RealSense D435 IR projector replacement" module off AliExpress (~$10–25)**; third is a hobbyist **ams-OSRAM BELICE-850 breakout (Electromaker APDE-00, est. ~$30–60)**.
- **For the camera pair, the clean answer is an OV9281 mono *global-shutter* USB stereo module with NO IR-cut filter** — e.g. the **ELP/SVPRO dual-lens OV9281 binocular** (one USB cable, hardware-synced, IR-sensitive, global shutter, est. ~$70–110), or **2× Arducam/Innomaker OV9281 mono modules (~$20–36 each)**. These genuinely see 850 nm.
- **AVOID for the camera pair:** HuskyLens / any "AI vision" camera (mono + AI overhead, wrong tool), and "night-vision USB cameras with built-in IR LEDs" (that LED ring is a **flood**, and many such cams have a *switchable IR-cut filter* that defeats the point). You want **plain, dumb, IR-sensitive sensors**.
- **Cheapest viable build ≈ $80–135** (used Kinect v1 projector ~$10–25 *or* AliExpress salvaged IR DOE ~$10–25, + ELP OV9281 NoIR stereo ~$70–110, + an 850 nm IR band-pass filter ~$10). **Honest verdict (§6): a used Orbbec Gemini 2 ($234) or used RealSense D435 (~$100–180) is usually the smarter buy** — the DIY saving is ~$100 and it costs real stereo-calibration + IR-filter + sync fiddling.

---

## (A) IR dot/speckle PATTERN projectors

**CRITICAL FILTER applied:** every entry below is a **structured dot/speckle field** (random dots ≫ grid). FLOOD "IR illuminators" and "night-vision" emitters are **excluded** — they add no texture. Line-only lasers (1-D method) are also excluded. Prefer **850 nm** (indoor standard, ~15–40% more silicon-sensor sensitivity; 940 nm is fully invisible but dimmer to the sensor). **Eye safety: Class 1 only** for a home robot — and because IR is invisible there's no blink reflex, so never point a non-Class-1 IR emitter at faces.

| # | Candidate / where to buy | ≈2026 price | λ | Pattern | Coverage / FOV / range | Eye-safety | Notes |
|---|---|---|---|---|---|---|---|
| **A1** | **Used Microsoft Kinect v1 (model 1414), eBay/Bonanza** — salvage the IR projector, or use the whole sensor | **~$9–25 used** | ~830 nm | **Random speckle (real DOE)** — the canonical structured-light projector | designed for ~0.5–4 m room depth; wide FOV | **Class 1** (consumer toy, eye-safe) | **The prominent cheap correct option.** Real field-of-dots. Caveats: model **1414** (Xbox 360, proprietary 12 V + USB plug — needs the AC adapter/breakout); bulky; if you run the whole sensor its SDK (libfreenect/OpenNI) is community-maintained, no clean ROS2. Best used as a *projector donor* feeding the OV9281 pair below. Avoid Kinect v2 (ToF, not a dot projector) for this purpose. |
| **A2** | **AliExpress "RealSense D435 infrared projector replacement"** module | **~$10–25** | 850 nm | **VCSEL + DOE random dots** (real field) | matched to D435 (~0.3–3 m room) | Class 1 (RealSense projector is ~150 mW Class 1) | Cheapest *new* correct field-of-dots. Sold as a D4xx repair part. Verify the listing shows a **dot pattern**, not a flood LED, before buying — listing quality varies. Needs its own small drive board / current source. |
| **A3** | **ams-OSRAM BELICE-850 breakout — Electromaker "Dot Projector" (APDE-00)** | est. **~$30–60** (price not shown in listing; confirm) | 850 nm | **VCSEL + DOE, high-contrast dots** (the Face-ID-class part) | compact, wide; designed for ~0.2–4 m stereoscopic depth | **Class 1**, eye-safe by design | The maker-friendly *new* part: a genuine ams-OSRAM 3D-sensing dot projector on a small breakout. Tiny emitter (lens ~2.5 mm), low drive (≤7 mA @ 3 V). The cleanest "buy a real dot projector new" option if in budget. |
| **A4** | **Lasermate 850 nm DOE laser modules** — `MDOE850A200R303` (30k dots) / `MDOE850B200R103` (10k dots, adjustable focus), or bare DOE `DOE-RD10K850A` (10k random dots, 59°×46°) | **RFQ** (component; not retail-listed) | 850 nm | **Random-dot DOE**, 10k–30k dots | e.g. 67.7°×53.4° (R303); ~room range | IEC 60825 compliant (class set by configured power) | Correct and high-quality but **RFQ/MOQ components**, awkward and slow for a one-off bench. Listed for completeness / if scaling to a product. |
| ❌ | AliExpress "850 nm **focusable dot** laser module" (~$5–15) | $5–15 | 850 nm | **SINGLE DOT** | n/a | varies (often Class 3R) | **WRONG TOOL** — one spot, not a field. You need thousands of dots from a DOE. |
| ❌ | "850/940 nm **IR illuminator** board," Waveshare/Amazon IR LED boards, "night-vision" emitters | $5–30 | 850/940 | **FLOOD (uniform)** | wide | varies | **EXCLUDE** — uniform light adds **no texture**; gives the stereo matcher nothing to lock onto. The single most common mis-buy. |

**Read-out (A):** the dot-projector half is the hard, scarce half — genuine consumer dot projectors barely exist; the market is flooded (literally) with useless illuminators. The realistic cheap-and-correct picks are **A1 (used Kinect v1, ~$9–25)**, **A2 (salvaged D435 IR projector, ~$10–25)**, or **A3 (BELICE-850 breakout, ~$30–60 new)**. All are 850/830 nm Class-1 random-dot fields suitable for ~1–4 m room range.

---

## (B) Cheap IR-capable CAMERA pairs (no IR-cut filter)

You need **two matched, IR-sensitive ("NoIR" / no IR-cut filter) sensors** that can be used as a stereo pair. Global shutter is preferred for a moving robot (no rolling-shutter skew) but rolling shutter is acceptable for a static-capture v1. **USB/UVC is best for the laptop rig** (plug-and-play, no MIPI/HAT plumbing). The OV9281 is the sweet spot: 1 MP **mono global-shutter**, sold **without an IR-pass/cut filter** (genuinely IR-sensitive), and available as a **single-USB synchronized binocular**.

| # | Candidate / where to buy | ≈ price (each / kit) | IR-sensitive? | Shutter | Res / interface | Stereo sync | Notes |
|---|---|---|---|---|---|---|---|
| **B1** | **ELP / SVPRO dual-lens OV9281 binocular USB** (Amazon `B0D9VY8JG4`; SVPRO-branded `B0DGL5ZXNQ`) | est. **~$70–110 kit** (price not shown in snippet; confirm on listing) | **YES — no IR-pass/cut filter, IR-sensitive** (vendor-stated) | **Global** | 2× OV9281 mono, 2560×800 combined @120 fps; **USB 2.0 / UVC** | **Hardware-synced, single USB cable** | **Best prototype pick.** Plug-and-play on Linux (UVC, no driver), one cable, factory-mounted baseline, global shutter, IR-sensitive out of the box. (Note: SVPRO *is* the ELP brand — this is the IR-capable sibling of the existing camera, which has an IR-cut filter and is rolling-ish.) |
| **B2** | **2× Arducam OV9281 mono USB** (Amazon `B096M5DKY6` / `B08Q2WXQL6`) | **~$26 each** (~$52 pair) | **YES — NoIR, IR-sensitive** (vendor-stated) | **Global** | OV9281 mono, 1280×800; **USB 2.0 / UVC** | **No built-in HW sync** — two independent UVC devices; software-trigger or accept small skew | Cheap and genuinely IR-sensitive, but **two separate USB cameras** = you must handle sync/calibration yourself. Fine for static capture; sync matters more when moving. |
| **B3** | **2× Innomaker OV9281 mono USB** (Amazon `B0CLRN9QRC`; inno-maker.com) | **~$19–49 each** | **YES — no IR-pass filter, IR-sensitive** (vendor-stated) | **Global** | OV9281 mono, 720p–800p; **USB 2.0/UVC**, has **external-trigger** pin | External-trigger pin → can be **HW-synced** with wiring | Like B2 but the trigger pin lets you hardware-sync a pair with effort. Good middle option. |
| **B4** | **2× Raspberry Pi NoIR (OV5647/IMX219) MIPI** | ~$10–30 each | YES (NoIR) | **Rolling** | color, MIPI CSI (not USB) | needs Pi + CamArray/dual-CSI; not laptop-friendly | Cheapest sensors, but **MIPI not USB** (needs a Pi + sync HAT), **rolling shutter**, and color (mono is better for IR stereo matching). Only if already on a Pi rig. |
| ❌ | **HuskyLens / any "AI vision" camera** | $45+ | (mono, AI board) | — | — | — | **WRONG CHOICE** — single sensor + onboard AI you don't need; not a dumb stereo pair. The search surfaces these; ignore them. |
| ❌ | **"Night-vision USB camera with built-in IR LEDs"** | $15–40 | partly | rolling | mono/color | — | **WRONG CHOICE** — the LED ring is a **FLOOD** (no texture), and many such cams have a **switchable mechanical IR-cut filter** that blocks 850 nm in the mode you'd use. Buy a plain IR-sensitive sensor + a *separate* dot projector instead. |

**Read-out (B):** the camera half is **easy and cheap** — the OV9281 is purpose-built (mono, global shutter, sold NoIR). **B1 (ELP/SVPRO OV9281 binocular, single synced USB)** is the clear prototype pick: plug-and-play, hardware-synced, IR-sensitive, global shutter. Steer firmly away from HuskyLens/AI cams and "night-vision-with-flood" webcams — both are the wrong tool.

---

## (C) Gotchas (the four ways this goes wrong)

1. **Pattern, not flood.** A projector must paint **dots/speckle**, not uniform light. "IR illuminator" / "night-vision LED" = flood = zero stereo texture = useless. This is the #1 mis-buy and it dominates consumer search results.
2. **Camera, not projector — and not an AI camera.** The camera pair must be **plain, dumb, IR-sensitive sensors** (no IR-cut filter). HuskyLens / AI-vision cams (mono + AI overhead) and night-vision cams (flood + switchable IR-cut) are the wrong tools.
3. **No IR-cut filter + add an IR band-pass filter.** The sensors must lack the IR-cut filter (so they see 850 nm). For best contrast, add an **850 nm band-pass filter** (~$10) over each lens so the camera rejects ambient visible light and the dots pop — this is the mechanism that takes RealSense from ~3 m to ~10 m on a white wall ([[dot-projector-options]] §1). Without it the rig still works but with less range/contrast.
4. **Eye safety = Class 1 only.** Home robot near people/pets → Class 1 IR only. The Kinect v1, RealSense projector, and ams-OSRAM BELICE are all Class 1. IR is invisible (no blink reflex), so this matters more, not less — never run a non-Class-1 IR emitter (e.g. a bright "focusable" laser) near faces.

Plus the integration tax you're signing up for: **stereo calibration** of the pair ([[camera-calibration-and-self-calibration]]), **time-sync** of the two views (free if you use the single-USB synced B1 module; real work for B2/B3 pairs on a moving robot), and **mounting** projector + cameras on a rigid baseline.

---

## (D) Recommendation

**Cheapest viable DIY build (≈ $80–135):**
- **Projector:** used **Kinect v1 (model 1414) as projector donor (~$10–25)** *or* AliExpress **salvaged D435 IR DOE projector (~$10–25)**. (Buy the **BELICE-850 breakout (~$30–60)** instead if you want a clean *new* part.)
- **Cameras:** **ELP/SVPRO OV9281 binocular USB (~$70–110)** — single synced cable, global shutter, IR-sensitive.
- **Plus:** 2× **850 nm band-pass filter (~$10)**.
- **Total ≈ $90–145**, global shutter, real field-of-dots, Class 1.

**More robust build:** swap the salvaged projector for the **ams-OSRAM BELICE-850 (A3)** (factory dot quality, guaranteed Class 1) and add the band-pass filters; budget ~$120–180. Still cheaper than turnkey, with better dot contrast and eye-safety provenance.

---

## (E) Honest verdict — is the DIY rig worth it vs a used depth cam?

**Usually not, for a Phase-1 prototype.** The DIY rig's all-in parts cost (~$90–145) lands *right next to* a **used Intel RealSense D435 (~$100–180 on eBay/Back Market)** and only ~$100 under a **new Orbbec Gemini 2 ($234)** — both of which give the *identical* active-IR-stereo capability **factory-calibrated, time-synced, IR-filtered, with a maintained Linux/ROS SDK and an IMU**, in one cable, today. The DIY route trades that ~$100 saving for: sourcing a *genuine* dot projector (the scarce half), stereo-calibrating the pair, time-syncing two views, fitting band-pass filters, and building a rigid mount — exactly the work [[economical-ir-depth-cameras]] §3 prices as "real engineering."

**When the DIY rig *does* make sense:** (a) you already have a junk-drawer Kinect v1 and OV9281 cams → near-zero cost, good learning exercise; (b) you specifically want **global shutter** (the OV9281 pair beats the D435's sensor for a fast-moving robot); (c) you're prototyping toward a **custom product BOM** where the ams-OSRAM/Lasermate components matter. Otherwise: **buy a used RealSense D435 (~$100–180) or new Gemini 2 ($234) and skip the integration tax.** And remember the framing — **none of this is needed for the floor map; the RPLIDAR C1 ($95) already owns that.** This rig is purely the optional camera-based-3D-object-depth upgrade.

---

## Source

Web (≈2026, accessed 2026-06-09; verify prices before purchase — listing prices were not all visible in search snippets and are flagged "confirm"):

**(A) Projectors:**
- Used Kinect v1 model 1414 pricing (~$9–25 used) — pricecharting.com/game/xbox-360/kinect-sensor; ebay.com Xbox-360-Kinect-Sensor-Only listings; bonanza.com model-1414 listing (~$8.98). Kinect 1414 vs 1473 (1414 = Xbox 360, proprietary connector + AC adapter; structured-light IR random-dot projector) — kinecthesia.com/archive/the-difference-between-kinect-1414-and-1473
- AliExpress "RealSense D435 infrared projector replacement" (~$10–25, 850 nm VCSEL+DOE) — aliexpress search; RealSense projector ~150 mW Class 1 (per [[dot-projector-options]])
- ams-OSRAM BELICE-850 dot projector, Electromaker APDE-00 ("most compact dot-projector for stereoscopic imaging," 850 nm, high-contrast dots, ≤7 mA @ 3 V) — electromaker.io/shop/product/dot-projector; ams-osram.com/.../ams-belice-sd; mouser.com BELICE-850 datasheet DS000618; octopart.com APDE-00
- Lasermate 850 nm DOE modules + bare DOE (DOE-RD10K850A: 10,000 random dots, 59°×46°, 850 nm; MDOE850A200R303: 30k dots; MDOE850B200R103: 10k dots adjustable focus) — lasermate.com/optics/diffractive-optical-element/doe-rd10k850a/; lasermate.com/lasers/laser-modules/structured-light-laser-modules/
- (Excluded) AliExpress 850 nm single-dot "focusable" lasers = wrong tool; Waveshare/Amazon "IR illuminator boards" = flood — waveshare.com/infrared-led-board.htm (flood, confirmed)

**(B) Cameras:**
- ELP / SVPRO dual-lens OV9281 binocular USB (OV9281 mono global shutter, 2560×800@120fps, **no IR-pass filter, IR-sensitive**, 83° lens, dual-lens sync over one USB) — amazon.com/dp/B0D9VY8JG4; SVPRO-branded amazon.com/es/dp/B0DGL5ZXNQ; product is the IR-capable sibling of the SVPRO (svpro.cc = ELP brand)
- Arducam OV9281 mono USB module (~$25.99, NoIR/IR-sensitive, global shutter) — amazon.com/dp/B096M5DKY6; arducam.com OV9281 USB pages
- Innomaker OV9281 mono USB ($19–49, no IR-pass filter, global shutter, external-trigger pin) — inno-maker.com/product/u20cam-9281m/; amazon.com/dp/B0CLRN9QRC
- (Excluded) HuskyLens/AI cams (mono + AI, wrong tool); ELP "night-vision USB camera with 850 nm IR LEDs + IR-CUT filter" = flood + switchable cut filter, wrong tool — amazon.com/dp/B0BVFMN1Y1

**(C) Turnkey comparison:**
- Used Intel RealSense D435/D435i (~$100–180 used) — ebay.com d435 / d435i listings; backmarket.com refurbished D435 (up to 70% off new, 1-yr warranty)
- New Orbbec Gemini 2 $234, RealSense D435i $334 — per [[economical-ir-depth-cameras]]

Wiki cross-refs: [[economical-ir-depth-cameras]] (turnkey vs DIY pricing, Gemini 2 $234 top pick), [[dot-projector-options]] (projector physics + eye-safety deep-dive, IR+band-pass ~3 m→10 m), [[floor-map-sensing-options]] (RPLIDAR C1 $95 = primary floor-map sensor), [[passive-stereo-robustification]] §4–6 (active-stereo geometry + hardware ladder), [[camera-calibration-and-self-calibration]] (stereo calibration), [[sensor-weaknesses-and-fixes]].

*(synthesis — assembled 2026-06-09 from current vendor/marketplace listings + the wiki's existing sensor pages; several retail prices were not visible in search snippets and are given as ranges flagged "confirm.")*

## Related

[[economical-ir-depth-cameras]] (turnkey vs DIY pricing) · [[dot-projector-options]] (projector-component physics deep-dive) · [[floor-map-sensing-options]] (the RPLIDAR C1 primary floor path) · [[passive-stereo-robustification]] §4–6 (active-stereo geometry, the hardware ladder) · [[sensor-weaknesses-and-fixes]] · [[camera-calibration-and-self-calibration]] (stereo cal)
