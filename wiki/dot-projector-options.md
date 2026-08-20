# Dot / Speckle Projector Options for Wall Texturing — Product Survey (≈2026 USD)

**Research question:** Our ~$30 visible-RED laser speckle projector textures a blank wall for the passive stereo pair *up close*, but at room range (2–5 m) too few dots stay bright/detectable — per-dot returned brightness falls as **1/Z²**, and red dots on light walls have poor contrast. What is a **better, still-cheap** projector that puts **more / brighter / better-distributed** dots that stay detectable at 0.5–5 m on indoor walls? This page surveys actual purchasable projector products with dot counts, optical power, wavelength, FOV, eye-safety class, and ≈2026 prices, evaluated against the real physics levers, and recommends a pick.

> **Read alongside:** [[economical-ir-depth-cameras]] (the *camera* side — turnkey active-IR cameras have the projector built in; **Orbbec Gemini 2 $234** is the recommended all-in-one buy), [[passive-stereo-robustification]] §4–§6 (why a "dumb" projector works + the hardware ladder), [[stereo-dense-reconstruction]] §7 (physical projector vs the zero-hardware VPP alternative), [[sensor-weaknesses-and-fixes]] (the projector as the #1 cure for spurious-far depth). This page is the *projector-component* deep-dive those pages defer to.

---

## TL;DR

- **The physics says brute-force brightness barely helps.** For a DOE projector the dot *count* and *FOV* are fixed by the optic and are roughly **distance-invariant in angular density** — so "more usable dots at distance" is really about **total dot count, per-dot power, wavelength/contrast vs ambient, and FOV (coverage vs density)**, not "throw it further." RealSense's own number: **doubling laser power buys only √2 ≈ 1.41× range** [src-web: RealSense tuning docs]. You cannot out-power the 1/Z² wall cheaply.
- **The single biggest lever is wavelength + an IR band-pass filter, not more dots.** Switching from visible red to **850 nm IR read through an IR-pass filter** suppresses ambient light and lifts dot contrast dramatically: RealSense measured a blank-wall depth range of **~3 m (passive) → ~10 m (projector + IR filter)** [src-web: RealSense projector white paper / tuning docs]. That is a far bigger win than any visible-laser upgrade, and it is *why every commercial active-stereo camera uses IR, not visible.* **The current red projector is the wrong wavelength, not just the wrong power.**
- **Single-dot AliExpress "focusable laser dot" modules are the wrong tool** (you need a *field* of dots from a DOE, not one spot) — already flagged in [[economical-ir-depth-cameras]]. The right component is a **VCSEL/laser + DOE** that splits one beam into thousands of dots.
- **For the prototype bench, the cheapest correct upgrade is a salvaged RealSense/Kinect-clone IR DOE projector (~$10–25 on AliExpress)** + an IR-capable camera — but our SVPRO can't see 850 nm, so this only pays off paired with the IR-camera move ([[economical-ir-depth-cameras]] Pick B), or just buy the **Gemini 2 ($234)** and get the projector for free, factory-aligned.
- **If we stay visible-light** (no IR camera yet): a **650 nm 30,000-dot DOE module (Lasermate MDOE650A10R303-class)** gives 3× the dots of a typical cheap red speckle and a clean 80°×64° pattern; a **green (520–532 nm) DOE** would be more visible to the silicon sensor and higher-contrast on light walls — but green DOE *field* modules are scarce/pricey and the ambient-wash problem remains. Visible is a debugging convenience, not the endgame.
- **A pico/DLP video projector can paint an arbitrary dense random texture** and is genuinely useful for *bench* validation (controllable PNG pattern), but it is **bulky, power-hungry (10s of W), focus-limited across depth, and washes out in ambient light at range** — not a product-shaped "texture the room" device. Laser DOE wins on brightness-at-distance and size; the pico wins only on pattern flexibility for debugging.

---

## 1. The physics levers (what actually moves "usable dots at 2–5 m")

A diffractive (DOE) projector takes one laser beam and a fixed diffraction grating splits it into a fixed pattern of N dots spread over a fixed field of view (FOV). Critically:

- **Angular dot density is fixed by the optic.** As the wall recedes, the dot grid scales up with it — the *number of dots landing on a given wall* stays roughly constant within the FOV (the pattern just covers a bigger area). So "the dots spread out and disappear with distance" is **not** the dominant failure; the dominant failure is **per-dot brightness and contrast**.
- **Per-dot returned brightness falls as 1/Z².** A dot at 4 m returns ¼ the irradiance of the same dot at 2 m. This is the real range wall, and it is brutal: **2× power → only √2× range** [src-web: RealSense tuning — "a 2x power improvement gives only sqrt(2)=1.41x improvement in range"]. Buying brightness is a losing game.
- **Contrast vs ambient is the cheaper lever.** A red dot competes with all the room's ambient red/white light. An **850/940 nm IR dot read through an IR band-pass filter** lets the camera reject nearly all ambient light, so even a dim dot stands out — this is how RealSense turns ~3 m into ~10 m on a white wall [src-web: RealSense projector white paper]. Wavelength + filter beats raw power.
- **Dot count vs FOV is a coverage/density tradeoff.** More dots = denser matchable texture but each dot is dimmer (same total power split more ways) and a wider FOV spreads the same dots thinner. The sweet spot for room mapping is a moderate FOV (~60–90°) at ~5k–30k dots, matching the camera's own FOV so dots aren't wasted off-frame.

**Conclusion the rest of the page is built on:** the highest-leverage cheap upgrade is **go IR + IR-pass filter** (a wavelength/contrast fix), *then* pick a moderate-FOV DOE in the 5k–30k dot range. Chasing a brighter *visible* laser fights the 1/Z² wall head-on and loses.

---

## 2. Visible laser DOE speckle projectors (red & green)

Visible projectors are useful for **bench debugging** (you can see the pattern, sanity-check coverage by eye) but inherit the ambient-wash + 1/Z² problem the current red unit already shows. Listed for completeness and for the "stay visible for now" path.

| Product / class | λ | Dots | Power / drive | FOV | Eye safety | ≈2026 price | Notes |
|---|---|---|---|---|---|---|---|
| **Current prototype unit** (generic red speckle) | ~650 nm red | low (≈1k-class) | ~tens of mW | narrow | likely **Class 3R/3B** (caution) | ~$30 | The unit that fails at room range. Few dots, poor red contrast on light walls, washes out at 2–5 m. |
| **Lasermate MDOE650A10R103** | 650 nm red | **10,000** | 24 mA @ 3 V (low-power class, focus/power adjustable) | not stated | IEC 60825 compliant (class set by configured power) | RFQ (component; not retail-listed) | Clean DOE 10k-dot field; far more dots than the current unit [src-web: lasermate.com MDOE650A10R103]. |
| **Lasermate MDOE650A10R303** | 650 nm red | **30,000** | 24 mA @ 3 V | **80°×64°** | IEC 60825; "low distortion, high uniform pattern" | RFQ (component) | 3× the dots, room-matched FOV. The best *visible* field-of-dots option found [src-web: lasermate.com MDOE650A10R303]. |
| Green DOE dot module (e.g. Lasermate MDOE-G / odicforce 520 nm DOE; scarce) | **520–532 nm green** | varies (1k–10k DOE; many green "dot" parts are *single-dot*) | mW-class | varies | varies; green Class-1 ceiling is **<0.39 mW** (very dim) [src-web: Quarton VLM-520-03 Class-1] | scarce; module ~$30–120, DOE field versions niche | **Green is more visible to silicon sensors and higher-contrast on light walls** — the best *visible* wavelength in principle. But field-of-dots green DOEs are rare, and a Class-1 green is too dim to texture a far wall; a usable green is Class 3R+. |
| ❌ Quarton VLM-520 / VLM-650 "dot" modules | 520/650 nm | **1 (single dot)** | <0.39 mW (Cl.1) – few mW (Cl.3R) | n/a | Class 1 to 3R | ~$20–40 (Amazon) | **Wrong tool** — alignment single-dot lasers, not a speckle field [src-web: amazon.com Quarton VLM-520]. |

**Read-out (visible):** if we must stay visible (no IR camera yet), the **Lasermate MDOE650A10R303 (650 nm, 30k dots, 80°×64°)** is the upgrade over the current red unit — 30× the dots and a room-matched FOV. **Green would be better on contrast** but field-of-dots green DOE modules are scarce and a bright-enough green is not eye-safe. **None of these escape the ambient-wash / 1/Z² ceiling — visible is a debugging path, not the fix.**

---

## 3. IR laser DOE dot projectors (850 / 940 nm) — the right answer

This is what every commercial active-stereo camera (RealSense, Orbbec, OAK-D Pro) uses internally, for the contrast reason in §1. **Needs an IR-capable camera** — our SVPRO has an IR-cut filter and cannot see 850 nm; covered in the [[economical-ir-depth-cameras]] camera thread. λ choice: **850 nm = indoor standard** (faint red glow at the emitter, ~15–40% more sensor sensitivity), **940 nm = fully invisible + better sunlight rejection but dimmer to silicon** [src-web: RealSense docs; Digigram VCSEL DOE].

### 3a. Real component-grade modules (concrete specs)

| Product | λ | Dots | Optical power | FOV | Eye safety | ≈2026 price | Notes |
|---|---|---|---|---|---|---|---|
| **ams-OSRAM BELAGO1.1** (AQAA-20 eval) | 940 nm | **~5,000** random | (datasheet) | wide | **Eye-safe (Cl.1), ITO interlock**, IEC 60825 | eval board via Mouser, ~$50–150 class; bare COB cheaper at MOQ | Focus-free, high-contrast; the phone Face-ID-class part [src-web: ams-osram.com BELAGO1.1; mouser.com AQAA-20]. |
| ams-OSRAM **BELAGO1.2** | 940 nm | **~15,000** | (datasheet) | wide | Cl.1 eye-safe | component / MOQ | Higher dot count successor [src-web: ams-osram.com BELAGO1.2]. |
| ams-OSRAM **BELICE-SD / BELICE-850** | 850 nm | **~10,000** (pair) | (datasheet) | wide | Cl.1 eye-safe | eval board (electromaker APDE-00 / Mouser); ~$40–120 class | 850 nm sibling; available as a breakout for makers [src-web: ams-osram.com BELICE-SD; electromaker.io dot-projector]. |
| **Lasermate MDOE850A200R303** | 850 nm | **30,000** | drive 230 mA @ 2.1 V | (R30 optic) | IEC 60825 | RFQ (component) | Plain laser-diode + DOE module (Ø8×15 mm), R&D-friendly form [src-web: lasermate.com structured-light]. |
| Lasermate **MDOE940A200R613** | 940 nm | **61,000** | 270 mA @ 3 V | (R61 optic) | IEC 60825 | RFQ | Highest dot count in the family — dense texture for short range [src-web: lasermate.com structured-light]. |
| **Lasermate VDOE850COB9K / VDOE940COB11K** (VCSEL COB) | 850 / 940 nm | **9,072 / 11,664** | up to **800 mW–1.2 W** | 52°×69° | IEC 60825 | RFQ (reflow COB) | Product-grade VCSEL+DOE; bare COB ~3.5 mm, reflow-mount [src-web: lasermate.com VDOE...]. |
| **Coherent 940 nm SMT dot projector** | 940 nm | **600 – 13,000** (config) | up to 5.5 W array | 67°×53° to 130°×110° | "excellent eye safety" (Cl.1 target) | OEM / RFQ | Auto/robotics-grade; designed-to-order dot count + FOI [src-web: coherent.com 940 SMT dot projector]. |
| Metalenz/Vertilite **Starlight**; Himax dot projector | 940 nm | ~18,000 / varies | — | — | Cl.1 | OEM | Meta-optic / WLO single-element projectors; future product-form, not buyable retail [src-web: metalenz.com Starlight]. |

### 3b. The cheap, *buyable-today* IR field-of-dots options

The component modules above are RFQ/MOQ parts — awkward for a bench. The practical cheap routes (per [[economical-ir-depth-cameras]] §3):

| Option | What it is | ≈2026 price | Verdict |
|---|---|---|---|
| **Salvaged RealSense / Kinect-clone IR projector** | Sold on AliExpress as "D435 infrared projector replacement" — a real VCSEL+DOE field of dots, 850 nm | **~$10–25** | **Cheapest correct field-of-dots projector.** Needs an IR camera to be useful. |
| ❌ AliExpress "850 nm focusable dot laser" | **Single-dot** alignment laser | ~$5–15 | **Wrong tool** — one spot, not a field [src-web: aliexpress 850 nm dot modules]. |
| 850 nm machine-vision pattern projector (Smart Vision Lights SXP30-850 / MV Direct ODSXP30-850) | Clean industrial DOE pattern | **$200–400+** | Correct but erases the parts savings; over budget. |
| **Just buy a Gemini 2** ($234) | Projector built into a factory-aligned active-IR camera | $234 | **Best value** — the projector "for free," no sourcing/alignment ([[economical-ir-depth-cameras]] Pick A). |

---

## 4. Pico / DLP / LCD video projector as a "texture the room" device

A small video projector can display an **arbitrary dense random PNG** — maximum pattern flexibility. Worth weighing honestly:

| Dimension | Laser DOE projector | Pico/DLP video projector |
|---|---|---|
| Brightness at 2–5 m | High (collimated laser dots) | **Low** — lumens spread over a large image; washes out vs ambient at range |
| Focus across depth | **Focus-free** (laser dots stay sharp at any distance) | Focused at one plane; **defocuses across a slanted/curved wall** |
| Ambient/IR rejection | IR + band-pass filter rejects ambient | Visible only; **no ambient rejection** |
| Pattern flexibility | **Fixed** by the DOE | **Arbitrary** — any random texture, animatable (good for debugging) |
| Size / power | Fingernail VCSEL, **<1 W** | Palm-sized, **10s of W**, fan, battery drain |
| Cost | $10–30 (salvaged IR) to ~$234 (camera w/ built-in) | budget DLP **~$250** (AAXA P8 $249, P400 $269) [src-web: projectorreviews.com] |
| Invisibility to occupants | IR = invisible | Visible projected image in the room = non-starter for a product |

**Verdict:** a pico projector is a useful **bench debugging tool** (controllable visible PNG — already what early prototyping used, per [[passive-stereo-robustification]] §4), but it is **not a viable product-form "texture the room" device**: too bulky/power-hungry, focus-limited across depth, no ambient rejection, and visibly lights the room. The laser DOE (ideally IR) wins on every product-relevant axis except pattern flexibility.

---

## 5. Eye safety (home robot near people & pets) — read this

Laser class is set by emitted power **and** how the beam is spread (a DOE spreading power over thousands of dots/wide FOV lowers the per-dot hazard vs a collimated single beam of the same total power).

- **Class 1 — eye-safe, no hazard under normal use.** The required bar for a home product. Commercial IR dot projectors (ams-OSRAM BELAGO/BELICE, Coherent, RealSense's own ~150 mW projector) are engineered to **Class 1** — often with an **ITO interlock** that cuts the laser if the DOE cracks (prevents a raw collimated beam escaping) [src-web: ams-osram BELAGO; RealSense]. **All recommended IR options here are Class 1.**
- **Class 1 visible is very dim.** A Class-1 *visible* dot laser is **<0.39 mW (green) / ~<1 mW (red)** [src-web: Quarton VLM-520/940 Class-1] — too dim to texture a far wall. So a bright-enough *visible* speckle projector is typically **Class 3R (≤5 mW, caution)** or **3B (hazardous)**. **Our current ~$30 red unit is almost certainly Class 3R/3B** — a real reason to move off bright visible lasers for a home robot, independent of the contrast argument.
- **IR is the eye-safety-friendlier path** *because* the contrast win (§1) lets a **low-power (Class 1)** IR projector do the job a bright (Class 3R) visible one couldn't — the IR-pass filter does the heavy lifting, not raw power. **Caveat:** IR is *invisible*, so the blink/aversion reflex doesn't trigger — Class-1 compliance and the DOE interlock matter more, and never run a non-Class-1 IR emitter near faces.

**Bottom line:** buy **Class 1 only** for anything that ships near people/pets. The commercial IR projectors and the active-IR cameras (Gemini 2, RealSense) all meet this; the bright visible-laser path generally does not.

---

## 6. Recommendation

**The current red projector's problem is wavelength/contrast first, dot-count/power second.** Ranked, cheapest-correct first:

1. **Best value — buy the projector built into a camera: Orbbec Gemini 2 ($234).** Factory-aligned 850 nm VCSEL+DOE active-stereo projector + IR stereo + IMU + IR filtering, Class 1, no sourcing or alignment. Solves the room-range failure by the exact IR+filter mechanism in §1. This is the same conclusion as [[economical-ir-depth-cameras]] — the projector question and the camera question collapse into one buy.
2. **Cheapest bench parts — salvaged RealSense/Kinect-clone 850 nm IR DOE projector (~$10–25)** + the IR-camera move (ELP/Arducam OV9281 NoIR, [[economical-ir-depth-cameras]] Pick B) + an IR band-pass filter. Lowest sticker price; costs calibration/sync effort. Real field-of-dots, Class-1-class part.
3. **If forced to stay visible (no IR camera yet) — Lasermate MDOE650A10R303 (650 nm, 30,000 dots, 80°×64°), RFQ.** 30× the dots and a room-matched FOV vs the current unit; a meaningful bench upgrade. **But it does not beat the ambient-wash / 1/Z² ceiling** — treat as a stopgap, not the fix. A green DOE would contrast better but isn't cheaply available as a field-of-dots in an eye-safe form.
4. **Skip:** single-dot AliExpress lasers (wrong tool), bright Class-3R visible speckle units (eye-safety + still wash out), $200–400 industrial IR pattern projectors (erase the savings — just buy the Gemini 2), and pico/DLP video projectors as a *product* device (bench-only).

**One-line answer for the prototype:** stop trying to out-brighten a red laser against the 1/Z² wall — **move to IR + an IR-pass filter, and the cheapest way to get a correct, Class-1, factory-aligned IR dot projector is to buy it inside the Orbbec Gemini 2 ($234)**; the ~$10–25 salvaged IR DOE projector is the DIY-bench alternative once an IR camera is in hand. *(Note: [[stereo-dense-reconstruction]] §3 — VPP achieves a similar coverage gain in software with zero projector hardware, and is worth trying before any hardware spend.)*

---

## Sources

| Source | Role |
|---|---|
| RealSense projector white paper (`realsenseai.com/.../WhitePaper_on_Projectors_for_RealSense_D4xx_1.0.pdf`) | white-wall ~3 m→10 m range gain; pattern density; IR filtering |
| RealSense tuning docs (`dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance`, `dev.intelrealsense.com/docs/projectors`) | 150 mW nominal (max 360 mW); **2× power → √2 range**; white-wall projector tuning |
| Lasermate structured-light page (`lasermate.com/products/lasers/laser-modules/structured-light/`) + MDOE650A10R303, MDOE850A200R303, MDOE940A200R613, VDOE850COB9K, VDOE940COB11K, VDOE940COB10K | visible & IR DOE module dot counts / FOV / drive |
| ams-OSRAM BELAGO1.1 / 1.2 (`ams-osram.com/.../ams-belago1-1-dot-projector`, `.../ams-belago1-2-...`); BELICE-SD (`.../ams-belice-sd`); Mouser AQAA-20; electromaker.io APDE-00 | IR dot counts (5k/15k/10k), Class-1 + ITO interlock, eval-board availability |
| Coherent 940 nm SMT dot projector (`coherent.com/components-accessories/sensing-lasers/940-smt-dot-projector`) | 600–13,000 dots config, FOV range, eye-safety |
| Quarton VLM-520 / VLM-940 (`amazon.com` Quarton listings) | Class-1 visible/IR power ceilings; single-dot = wrong tool |
| Metalenz/Vertilite Starlight (`metalenz.com/...starlight-projector...`) | meta-optic 18k-dot 940 nm (future product-form) |
| Basler Stereo RandomDot projector (`baslerweb.com/.../stereo-camera-randomdot-projector`) | LED (5500K) random-dot projector, IEC 62471 — alt to laser DOE |
| projectorreviews.com / pico projector reviews | budget DLP pico pricing (AAXA P8 $249, P400 $269) |
| AliExpress 850 nm dot-laser & "D435 IR projector replacement" listings | single-dot trap; salvaged IR DOE ~$10–25 |

---

## Related

[[economical-ir-depth-cameras]] · [[passive-stereo-robustification]] · [[stereo-dense-reconstruction]] · [[sensor-weaknesses-and-fixes]] · [[close-range-depth-sensors]] · [[camera-calibration-and-self-calibration]] · [[home-tidy-drone-prototype]] · [[system-architecture]]
