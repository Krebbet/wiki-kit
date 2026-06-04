# Sensor Weaknesses Behind Relocalization Failure — and the Cheapest Fix

The `drone-prototype` does **marker-free relocalization** with a cheap passive USB stereo camera (the SVPRO). It *works* but is low-robustness: in the most diagnostic probe, **88 % (113/129) of correct-place appearance matches still get 0 PnP inliers** — geometric pose verification collapses even when the place-recognition front-end found the right map location (`drone-prototype` diary 2026-06-03, `reloc_test2`; EDA001/EDA002). This page answers, through a **sensor lens**: *which sensor weaknesses cause that geometry failure, ranked by impact; which cheap sensor change fixes it, ranked by ease/cost/impact; and the single highest-leverage change.* It honors the consumer-cost tenet — **passive/active stereo or *cheap* LiDAR only, never an expensive 3D LiDAR** (MID360-class is out; `docs/00-framing.md` Product tenet, human ruling 2026-06-01).

It complements [[passive-stereo-robustification]] (the *software/algorithm* robustifier ladder) by isolating what is **rooted in the sensor itself** and cannot be tuned away in software. *(synthesis — built from the prototype's own measured field findings + existing wiki pages, with raw-source citations carried through and new external sources cited inline.)*

## Source

- `drone-prototype` field findings — `docs/prototype-diary.md` (2026-06-01 step-3, 2026-06-02, 2026-06-03 `reloc_test2` / re-calibration degeneracy), `docs/parked.md` P-001/P-002, `eda/EDA001-relocalization/major-findings.md`, `eda/EDA002-pipeline-walkthrough/major-findings.md`, `docs/mapping-report-v1.md` §4c–4e. Measured SVPRO regime: [[home-tidy-drone-prototype]] "SVPRO characterization (measured)".
- Stereo depth-error law Δz ∝ z²·δd /(f·B): Luxonis depth docs; rc_visard stereo-matching docs [src-web: docs.luxonis.com/hardware/platform/depth, doc.rc-visard.com].
- Rolling-shutter corrupts SLAM geometry / PnP: Schubert et al. "Direct Sparse Odometry with Rolling Shutter" (ECCV 2018); Saurer et al. "Minimal Solution to the Rolling Shutter Pose Estimation Problem" (IROS 2015); Dai et al. "Rolling Shutter Camera Relative Pose: Generalized Epipolar Geometry" (CVPR 2016); FRAMOS / FPV-Labs global-vs-rolling notes [src-web].
- Active-IR stereo paints texture on blank walls — white-wall depth range ~3 m → ~10 m with projector + IR filtering: Intel RealSense "Projectors for D4xx" white paper; RealSense tuning docs [src-web: realsenseai.com/.../WhitePaper_on_Projectors..., dev.realsenseai.com/docs/projectors].
- VIO/IMU as motion prior across feature-poor frames: ORB-SLAM3 (arXiv 2007.11898) via [[visual-inertial-slam]], [[indoor-cluttered-slam]] (IMU bridging < 1 s) [src: 07-arxiv-2306-08522].
- Camera prices: D435i $334 (Intel RealSense store, 2026); OAK-D Pro $349–399 / OAK-D SR $199 ([[close-range-depth-sensors]]); Arducam OV9281 mono global-shutter ~$26–36/cam (Arducam/Amazon, 2025–26) [src-web].

## Related

[[passive-stereo-robustification]] · [[close-range-depth-sensors]] · [[drone-sensors-for-autonomy]] · [[indoor-cluttered-slam]] · [[visual-inertial-slam]] · [[cheap-lidar-pricing-guide]] · [[event-cameras]] · [[home-tidy-drone-prototype]] · [[system-architecture]]

---

## 1. The failure, in one picture

Relocalization is a two-gate pipeline; the prototype isolated each gate with two different probes (diary 2026-06-03):

1. **Gate 1 — appearance recall** ("did the place-recognition front-end propose the right map location?"). A better-overlap probe (`reloc_test2`, re-viewing the mapped path) **solved this** — 137/141 rejections had a real appearance match (M ≥ 20).
2. **Gate 2 — geometric verification** ("does a PnP solve on the matched 3D↔2D points produce enough inliers to confirm the pose?"). This is **the binding wall**: **88 % of right-place matches get 0 PnP inliers**, with a concrete corruption signature — e.g. one same-place pair had 110 appearance matches but **23 of 96 points were spurious-far** (depth reading 12–25 m on textureless surface) — `04b` figure, EDA002.

PnP needs **metrically consistent 3D points**. The geometry gate fails because the sensor delivers 3D points that are **noisy, spurious-far, or wrongly scaled** — all sensor-rooted. The rest of this page ranks those roots.

## 2. Ranked sensor weaknesses behind the geometry failure

Ranked by measured impact on *this* relocalization failure (most load-bearing first). *(synthesis; each row cites its evidence.)*

| # | Sensor weakness | Mechanism → why it breaks PnP geometry | Evidence | Software-fixable? |
|---|---|---|---|---|
| **1** | **Passive-stereo texture starvation → spurious-far depth** | No texture on white walls/glass/glossy floor ⇒ no left↔right match ⇒ either a hole *or* a confidently-wrong **far** disparity-near-zero reading. Those bad 3D points enter the PnP point set and poison the solve. This is the direct cause of the 0-inlier wall. | Center-of-room read ~19 m where a wall stood (step-3); 23/96 points spurious-far to 25 m on a 0-inlier pair (EDA002 `04b`); 48 % coverage, blank-wall dropout (SVPRO char.) | **No** — software can mask/gate bad depth but cannot *create* a feature on a blank wall. The signal is missing at the sensor. |
| **2** | **Calibration degeneracy / unverified metric scale** | Wide-FOV lenses are degeneracy-prone: an offline solve trades focal length against baseline, giving a low-reprojection-RMS *but wrong-scale* depth. Stereo RMS ~2.45 px also sets the disparity-noise floor; via Δz ∝ z²·δd/(f·B) (see §3) that floor becomes **16–33 % depth error at 5 m** — enough to fail the inlier threshold even on a correct match. | Re-cal diverged (baseline 660 mm rational model; 5-coeff gave fx 1307→1670 +28 % impossible-for-fixed-lens, depth +5.6 % vs validated −1.0 %) — reverted (diary 2026-06-03). P-002. **Re-promoted to #1 lever with evidence.** | **Partly** — a better offline solve helps but is *degeneracy-prone on this lens*; an online self-cal or a hardware-calibrated camera removes the problem. |
| **3** | **Rolling shutter (likely) + motion blur** | During motion the top and bottom rows are exposed at different times, so a single frame is **geometrically inconsistent** — straight lines bend, feature positions shift by rows. A global-shutter PnP/triangulation model applied to rolling-shutter data yields "erroneous, distorted results"; a single fast head-turn injects >2 cm of frame-internal geometric error. Blur additionally smears the corner the descriptor relies on. | Motion blur was a measured finding (diary, sharpness gauge added); SVPRO is rolling-shutter-likely. Rolling-shutter→SLAM-geometry degradation: Schubert ECCV 2018, Saurer IROS 2015, Dai CVPR 2016 [src-web]. | **No** (for the sensor) — software RS-correction needs a motion model and is imperfect; a **global-shutter sensor removes the cause**. |
| **4** | **No IMU → no motion prior** | With no inertial constraint, a feature-poor or blurred frame has nothing to bridge it; the pose hypothesis is unconstrained and the PnP must succeed from vision alone. An IMU gives a metric-scaled motion prior that brackets the pose search and survives brief starvation. | IMU bridges < 1 s of feature starvation [src: 07-arxiv-2306-08522]; ORB-SLAM3 VI "survives long periods of poor visual information" [arXiv 2007.11898]. SVPRO has **no IMU**. | **N/A** — this is a *missing sensor*, the cheapest to add (§4 rung 1). |
| **5** | **Short baseline (≈57.8 mm) + wide-FOV / modest resolution** | Depth precision scales with baseline and focal length; the SVPRO's 57.8 mm baseline and wide lens (large GSD) make far-field disparity tiny, so depth error grows fast with range (§3). Wide FOV spreads pixels thin, raising the disparity-noise floor. | Baseline 57.8 mm, fx≈1307 px (SVPRO char.). Either larger baseline or larger focal length improves depth accuracy [src-web: Luxonis depth docs]. | **No** — baseline and FOV are fixed by the hardware. |
| 6 | **L/R sync / USB flakiness** | Unsynced or dropped frames break the instantaneous-pair assumption stereo depends on, and a mid-run USB dropout kills relocalization outright. Lower-tier than 1–3 for the *geometry* failure but a real robustness tax. | P-001 (camera drops off USB bus under load; only enumerates via powered dock). | Partly — a watchdog + pinned cabling mitigates; not the geometry root. |

**Takeaway:** the geometry failure is dominated by weaknesses **1 (texture starvation/spurious-far depth)** and **2 (calibration/scale)**, amplified by **3 (rolling shutter/blur)** during motion. Crucially, **#1, #3, #5 are not software-fixable** — they are missing or corrupted *signal at the sensor*. That is what makes a cheap sensor change the highest-leverage move.

## 3. Why bad depth fails PnP — the precision law (quantified for the SVPRO)

Stereo depth error follows **Δz = z²·δd /(f·B)** (z = range, δd = disparity error in px, f = focal px, B = baseline) — it grows **quadratically with range** and inversely with baseline·focal [src-web: Luxonis/rc_visard]. Plugged into the SVPRO's measured f≈1307 px, B≈57.8 mm:

| Range z | δd = 0.5 px (good) | δd = 1 px (≈ the 2.45 px RMS regime, conservative) |
|---|---|---|
| 1 m | 0.007 m (0.7 %) | 0.013 m (1.3 %) |
| 2 m | 0.026 m (1.3 %) | 0.053 m (2.6 %) |
| 3 m | 0.060 m (2.0 %) | 0.119 m (4.0 %) |
| 5 m | 0.165 m (3.3 %) | **0.331 m (6.6 %)** |
| 8 m | 0.424 m (5.3 %) | **0.847 m (10.6 %)** |

The SVPRO's stereo RMS is ~2.45 px (P-002), so its effective δd is *worse* than the 1 px column — putting room-scale (3–8 m) 3D points at **4–16 %+ depth error before any spurious-far blowups**. PnP's inlier test is a metric reprojection threshold; a 3D point landmark map built at that noise floor cannot reproject tightly enough to pass — **exactly the 88 % 0-inlier wall.** This is the quantitative bridge from "noisy sensor" to "geometry gate fails," and it points at the two cheap fixes that move δd and B: **add texture (kills spurious-far)** and **fix/verify scale (calibration or a factory-calibrated camera)**.

## 4. Ranked cheap sensor fixes (consumer-cost)

Ordered by **leverage = impact ÷ (cost × effort)**. All honor the consumer-cost tenet.

| Rank | Fix | Fixes weakness… | Cost | Integration effort | Consumer-cost? | Honest caveat |
|---|---|---|---|---|---|---|
| **1** | **Active stereo — add a cheap IR dot projector** (paint texture on blank walls) | **#1 directly** (spurious-far depth & blank-wall holes) | **~$12–50** (visible pico/laser-dot bench stand-in; ~$20–50 IR DOE for product) | Low–medium — projector is *uncalibrated scene paint*, the stereo pipeline is unchanged (depth comes only from the camera pair); but the **SVPRO can't see 850 nm IR** without conversion, so the cheap path is a *visible* speckle for bench proof (§4 of [[passive-stereo-robustification]]). | **Yes** — it is exactly what a D435i/OAK-D *is*. | Coverage-bounded: shadows, range² falloff, out-of-cone surfaces still drop. A fixed projector lights one region; a roaming robot needs a co-mounted IR module. |
| **2** | **Add a cheap MEMS IMU → VIO** | **#4** (motion prior) + bridges **#3** blur | **~$5–15** | Medium — needs IMU↔camera time-sync + extrinsics, then RTAB-Map/ORB-SLAM3 VI mode. | **Yes** | **Bridges < 1 s** of starvation — not a white-wall cure; complements, doesn't replace, fix #1. |
| **3** | **Global-shutter stereo camera** (e.g. dual **Arducam OV9281**, mono, 850 nm-capable) | **#3** (rolling shutter) + **#5** (better lens/baseline choice) + enables IR for #1 | **~$52–80** (2×~$26–36) **+ HAT/sync** | Medium–high — build-it-yourself rig, own calibration, own sync. | **Yes** | DIY: you own calibration (the degeneracy risk #2 follows you) and sync. Mono (no color) — fine for SLAM. |
| **4** | **Wider-baseline / higher-res / better-lens passive stereo** | **#5** (precision), partial #1 | ~$50–200 | Medium (new camera + recalibrate) | Yes | Improves far-field precision but **does nothing for the blank-wall texture problem (#1)** — the headline failure. Low leverage. |
| **5** | **Turnkey RealSense D435i** — active IR stereo + IR dot projector + **BMI055 IMU** + **factory calibration**, works out-of-box with RTAB-Map/ORB-SLAM3 | **#1 + #2 + #3 + #4 in one box** (active IR kills spurious-far; factory cal removes degeneracy/scale; global-shutter-class behavior; onboard IMU) | **$334** | **Lowest** — plug in, run; no calibration, no sync, no rig. | **Yes** — order of magnitude under a MID360-class 3D LiDAR. | $334 vs ~$12 for the bench projector; OAK-D Pro ($349–399) is pricier (skip); OAK-D SR ($199) is a short-range arm camera, not a room nav sensor ([[close-range-depth-sensors]]). |

**Active-stereo evidence (why fix #1 is the cure for the headline failure):** active IR stereo "overlays the scene with a semi-random texture that facilitates finding correspondences, in particular… texture-less surfaces like indoor dimly lit white walls" — and the measured effect is large: a blank-wall depth range that is **~3 m passive can extend to ~10 m with the projector on + IR filtering** [src-web: RealSense projector white paper, tuning docs]. That is precisely the mechanism that removes spurious-far disparity-near-zero readings — the #1 corruptor of the PnP point set.

## 5. The single highest-leverage cheap sensor change

**Add active stereo (an IR dot projector) — and the lowest-risk way to get it is the turnkey RealSense D435i ($334).**

Reasoning, on the evidence:

- The **geometry gate is the binding wall** (88 % 0-inlier on right-place matches), and its dominant corruptor is **spurious-far / missing depth from passive texture starvation** (weakness #1) — measured directly (23/96 points spurious-far to 25 m on a 0-inlier pair). **No software tier fixes a feature that isn't there**; active illumination *adds the missing signal*, and is documented to convert blank-wall depth from unusable to usable [src-web].
- A **DIY projector + the SVPRO is the cheapest bench proof (~$12–50)** and is the right *first* spend to validate the mechanism on our exact failure surfaces. But it carries our two persistent sensor liabilities — **calibration degeneracy (P-002)** and **rolling shutter** — which independently feed the geometry failure (#2, #3) and which the SVPRO cannot shed.
- The **D435i collapses fixes #1, #2, #3, #4 into one $334 module with factory calibration** — it simultaneously removes the spurious-far depth (active IR), the scale/degeneracy debt (factory cal), the rolling-shutter motion artifacts (global-shutter-class imager), and the missing motion prior (onboard IMU). It is the single change that attacks **four of the top five ranked weaknesses at once**, out-of-box with our existing RTAB-Map/ORB-SLAM3 stack, and still an order of magnitude under any disallowed 3D LiDAR.

**Recommended sequence (cheapest-first, evidence-gated):** (1) bench-prove active stereo with a ~$12–50 visible speckle projector on the SVPRO, aimed at the *measured* failure surfaces, and re-run the relocalization probe — does the 0-inlier rate drop? (2) If active stereo is confirmed as the lever, buy the **D435i ($334)** to get active IR + factory calibration + IMU + global-shutter in one turnkey module rather than fighting DIY calibration/sync. This mirrors [[passive-stereo-robustification]] §6/§7: *measure the failure regime, then aim the projector precisely, then buy the turnkey module only as far as the measured failure forces.*

## 6. What this does NOT fix (honesty)

- Active stereo is **coverage-bounded** — shadows, range² IR falloff, and surfaces outside the projector cone still drop out; a *truly* blank gallery wall at long range remains the worst case (real homes have clutter/texture, which helps).
- An IMU **bridges < 1 s** of starvation — it rescues blur and brief blank patches, not a sustained white-wall corridor [src: 07-arxiv-2306-08522].
- **Symmetric-interior false loop closures** (identical rooms) are a *place-recognition* problem, not a depth/geometry one — no sensor swap here fixes it ([[indoor-cluttered-slam]] §Key gaps).
- A better sensor **raises the floor but doesn't remove the need** for the algorithm robustifiers (depth gating of spurious-far points, appearance-recall tuning, health tracking) in [[passive-stereo-robustification]] — sensor and software fixes are complementary.
