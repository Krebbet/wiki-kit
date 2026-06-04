# Camera Calibration and Self-Calibration (Stereo, Wide-FOV)

How to calibrate the prototype's wide-FOV USB stereo camera (SVPRO) well enough to be a trustworthy **navigation anchor-map sensor**, and — the main ask — how a cheap stereo robot could **tighten its own calibration during operation over its lifetime** (online / self-correcting calibration). Calibration is the suspected bottleneck for the prototype's relocalization make-or-break: RTAB-Map's geometric pose verification needs metric-accurate 3D, and loose calibration poisons that 3D before SLAM ever runs. This page is a *new* research page; the existing wiki only touches calibration tangentially ([[passive-stereo-robustification]] §5 has the "speckle as calibration **validator**" insight, and parked **P-002** logs the unresolved calibration debt). *(research page — sources cited inline.)*

## Why this page exists (the concrete failure)

The prototype hit two real, instructive calibration failures (`drone-prototype` prototyper-log 2026-06-01 16:30):

1. **The 8-coeff `CALIB_RATIONAL_MODEL` DIVERGED** — on 12 sparse, partly-blurry frames it produced a nonsensical solve (stereo RMS ~4042 px, baseline ~198 mm). Too many distortion parameters for too little, badly-distributed data → overfit / numerical blowup.
2. **A 5-coeff solve hit a FOCAL/BASELINE DEGENERACY** — `fx` came out ~+28 % wrong and metric depth ~6 % off, because **the calibration poses lacked depth variation** (the board was held near-fronto-parallel at roughly one distance). This is not a solver bug; it is a fundamental observability gap (§2).

Both are textbook wide-FOV-stereo calibration traps. The fix for the offline solve is **input quality, not solver tuning**; the durable fix for a robot that lives in a home is **online self-calibration** (§4–6).

## Related

[[passive-stereo-robustification]] · [[slam]] · [[visual-inertial-slam]] · [[indoor-cluttered-slam]] · [[close-range-depth-sensors]] · [[map-then-navigate]] · [[home-tidy-drone-prototype]] · [[system-architecture]]

---

## 1. The geometry that makes calibration load-bearing

Stereo depth is

> **z = f · b / d**  (d = disparity, f = focal length in px, b = baseline)

so depth error propagates as **ε_z = z² /(f·b) · ε_d** [src: NasuhcaN/Medium, e-con Systems]. Two consequences that frame everything below:

- **Any error in f or b scales depth multiplicatively.** The prototype's +28 % `fx` error directly explains the ~6 %+ depth error — and depth error is *quadratic in range*, so a wall at 4 m is far worse hit than the checkerboard at 0.8 m. Noisy/biased 3D is exactly what defeats RTAB-Map's geometric loop-closure verification — the relocalization wall.
- **f and b are entangled** — see §2. You cannot trust the baseline (and therefore absolute scale) unless the calibration *geometry* forces f and b apart, or you pin one of them with an external metric reference (a known-distance measurement, §3).

## 2. Why the focal/baseline degeneracy happens — and how to break it

**The mechanism (this is the prototype's exact bug).** When a planar calibration target's normal is aligned with the optical axis (**fronto-parallel**) and the board sits at roughly one distance, the **focal length can trade off freely against the camera-to-board depth (Z)** in the extrinsic — a bigger `f` and a more-distant board reproject to the *same* image, so the optimizer cannot tell them apart. *"When a planar target's normal is aligned with the camera optical axis, focal length can freely trade off with the Z component (depth distance)... it is impossible to learn the focal length"* [src: Tangram Vision, NFOV calibration]. In a stereo rig that ambiguous `f` then drags the baseline `b` with it (both feed the same `z = f·b/d`), so you get a wrong `fx` **and** a wrong scale that partly cancel in reprojection RMS — the residual looks "okay" while the metric depth is silently off. This is why a low reprojection RMS is **necessary but not sufficient**; it does not certify metric accuracy.

**How varied depth/pose coverage breaks it.** Tilting the board introduces **foreshortening**: a tilted board occupies a *range* of depths in one view, so `f` is now constrained by perspective — *"when the board is tilted away from the camera, focal length becomes observable through foreshortening, because the board exists at a variety of depths"* [src: Tangram Vision]. Practical rule: capture a **wide spread of board-to-camera angles**, with the dihedral angle between image plane and board around **~45°**, plus genuine **near/far depth variation**, plus coverage of the **image corners** (where wide-FOV distortion lives) [src: Tangram Vision]. The prototype's recapture directive ("~20 sharp/still/edge-covering poses") was the right instinct — but it must explicitly include **tilt and depth variation**, not just edge coverage, or the degeneracy survives.

**How to pin/constrain parameters instead.** Two complementary levers:
- **Reduce the model** to what the data can support (don't solve 8 distortion coeffs on 12 frames — that caused failure #1). Fix tangential to zero (`CALIB_ZERO_TANGENT_DIST`) for a well-built rig; fix the principal point if it's near image center; assume `fx = fy` (`CALIB_FIX_ASPECT_RATIO`).
- **Pin the metric anchor externally.** Because baseline uniquely sets absolute scale, an absolute range measurement (tape-measured known distance, or a ToF reading) can fix scale that the planar target alone leaves ambiguous — *"the baseline distance scales the absolute depth readings, and this scaling factor could be uniquely determined using absolute range finding"* [src: Correcting Decalibration, arXiv 2001.05267]. For the prototype this is the **known-distance verification** of §3, used as a *constraint*, not just a check.

## 3. Practical offline stereo calibration for a wide-FOV lens (OpenCV)

**Distortion model — pick by FOV, don't default to rational.**

| Model | OpenCV | Params | Best for | Caveat |
|---|---|---|---|---|
| Standard Brown–Conrady | `calibrateCamera` (k1,k2,p1,p2,k3) | 5 | mild/moderate distortion | underfits strong barrel of a wide lens |
| **Rational** | `CALIB_RATIONAL_MODEL` | 8 (k1..k6,p1,p2) | wide lenses "between fisheye and normal" [src: Iamgouri/Medium] | **data-hungry & unstable** — diverged on the prototype's 12 sparse frames; needs many well-distributed sharp poses |
| **Fisheye (Kannala–Brandt)** | `cv2.fisheye.calibrate` | 4 (k1..k4) | very wide / true fisheye [src: OpenCV fisheye docs] | different rectification path; fewer params → often *more stable* than rational on a very wide lens |

Guidance: *"For wide-view lenses between fisheye and conventional, the `CALIB_RATIONAL_MODEL` flag works better"* — **but** *"the standard `calibrateCamera` will fail or give poor results on heavily distorted images"* and the literature consensus is to **experiment with multiple models** rather than assume one [src: Iamgouri/Medium, Manthan/Medium]. **For the SVPRO specifically:** if the rational model keeps diverging, try `cv2.fisheye` — its 4-param Kannala–Brandt model is *fewer* knobs and is the model designed for exactly this FOV regime; it frequently calibrates more robustly than an under-constrained 8-coeff rational solve.

**Capture protocol (the part the prototype got wrong):**
1. **Sharp + still** — gate on a sharpness metric and stillness before saving a frame (the prototype already added this). Motion blur was the root cause of the residual 2.2 px / 11 px in the first solve.
2. **Tilt + depth variation** — the degeneracy-breaker. ~45° dihedral angles, near and far, not all fronto-parallel (§2).
3. **Full-frame coverage incl. corners** — wide-FOV distortion is largest at the edges; corners must be sampled or k4–k6 are unconstrained.
4. **Enough frames** — ~20–40 *good* poses beats 12 sparse ones; more is needed for the 8-coeff rational model.
5. **Measure the printed square in mm** — sets metric scale (the prototype's placeholder 25 mm scales baseline/depth linearly; an unmeasured square = an unknown global scale).

**Target residuals (prototype bar, OpenCV reprojection RMS):** mono **< ~0.5 px** is achievable and good; **< 1 px** is the prototype's working bar; **stereo RMS** ideally **< ~0.5–1 px**. The prototype's 2.2 px mono / 11 px stereo (then improved) are *too high* for trustworthy metric depth. **Crucial caveat:** low RMS ≠ correct metric scale (§2) — a degenerate-pose solve can show low RMS and still have +28 % `fx`. RMS validates the *fit*, not the *geometry*.

**Jig vs handheld.** Handheld is fine for a prototype **if** the protocol above is followed; the failure was handheld-while-moving, not handheld per se. A rigid jig or a board on a stand helps guarantee stillness and lets you script tilt/depth coverage; for metrology-grade baseline a fixed jig + measured distances is better.

**How to VERIFY (independent of reprojection RMS):**
- **Known-distance / planarity test** — image a flat wall at a *tape-measured* distance, reconstruct, and check (a) the reconstructed plane is flat and (b) it sits at the true distance. This is the standard depth-camera QA step (Intel RealSense "Tare"), and is the [[passive-stereo-robustification]] §5 **flat-wall planarity test** — the candidate path to retire **P-002**. The projected-speckle trick from that page densifies the correspondences on a blank wall so the planarity check has signal.
- **Baseline cross-check** — compare the solved baseline against a physically measured inter-lens distance; a large mismatch flags the §2 degeneracy.
- **Epipolar/rectification check** — after rectification, matched points should share a row (zero vertical disparity); residual vertical disparity exposes bad extrinsics. Dense speckle matches make this check strong on otherwise-blank scenes ([[passive-stereo-robustification]] §5).

> RTAB-Map ships a built-in stereo calibration GUI (chessboard → export YAML, then "Rectify image") [src: RTAB-Map Stereo-mapping wiki] — usable as a cross-check against the prototype's OpenCV solve.

---

## 4. Online / self-correcting calibration — the survey (the main ask)

**The core idea.** SLAM already recovers structure: the *same* 3D points are seen from *many* views. That redundancy over-determines the geometry, so the **calibration parameters can be added as unknowns to the same bundle adjustment / filter that estimates pose** and refined continuously from ordinary operating data — no checkerboard. This is "self-calibration": the robot exploits the structure SLAM recovers to tighten its own intrinsics/extrinsics/distortion over its life [src: SLAM-based self-calibration, MDPI Sensors 2020; Online Continuous Stereo Extrinsic Estimation, Hansen/CMU]. Maturity is real but uneven, and **observability/degeneracy (§5) is the catch that governs whether it works.**

### What estimates what online — methods table

| System | OSS / usable on stereo | What it calibrates ONLINE | Mechanism | Maturity |
|---|---|---|---|---|
| **OpenVINS** (rpng) | ✅ open, stereo + IMU | camera **intrinsics + distortion**, cam–IMU **extrinsics**, **time offset**; (RS readout) | EKF state-augmentation — params are part of the filter state [src: OpenVINS docs, gs-calibration] | Mature research platform; online cal "out of the box" |
| **VINS-Fusion** (HKUST) | ✅ open, stereo + IMU | cam–IMU **extrinsics**, **time offset** (intrinsics less so) | sliding-window BA with extrinsics in state | Mature, widely deployed |
| **OKVIS2 / OKVIS2-X** (ETH-MRL) | ✅ open, stereo + IMU (+depth/LiDAR/GNSS) | cam–IMU **extrinsics** (intrinsic+extrinsic spatiotemporal of all sensors in -X) "to compensate for poor prior calibration and/or calibration varying over time" | keyframe BA / relative-pose-graph errors extended with extrinsic poses [src: OKVIS2-X, arXiv 2510.04612] | Active; online extrinsic cal "substantially improves accuracy" |
| **Basalt** (TUM-VI) | ✅ open, stereo + IMU | cam–IMU extrinsics, time offset (intrinsics in its offline calib tool) | factor-graph VIO + a strong offline calib pipeline | Mature; strong calibration tooling |
| **Kalibr** (ETH-ASL) | ✅ open — **OFFLINE reference** | full multi-cam intrinsics+extrinsics, cam–IMU spatial+**temporal**, IMU intrinsics, rolling-shutter | batch spline-based optimization over an AprilTag board [src: Kalibr wiki/repo] | The de-facto **offline** VI-calibration gold standard — the *reference* an online method should match |
| **SLAM-based stereo self-cal** (binocular rig, real-time) | research code | stereo **extrinsics** in real time, intrinsics assumed known | online BA with pose priors as soft constraints; "within 10 s under normal driving" [src: MDPI Sensors 2020; High-Precision Markerless, arXiv 1903.10705] | Demonstrated; extrinsic-focused (handles thermal/mechanical drift) |
| **DSO online photometric cal** (TUM) | ✅ open | **photometric**: response function, vignette, exposure (not geometry) | KLT-track-based nonlinear optimization, realtime [src: arXiv 1710.02081] | Mature; *"without photometric calibration DSO entirely fails"* |

**Two families, two jobs:**
- **Geometric self-calibration** (intrinsics/distortion/extrinsics/scale) — fixes the prototype's actual problem (noisy metric 3D). Best fits: **OpenVINS** (estimates intrinsics+distortion+extrinsics online) and **OKVIS2-X** (extrinsics + spatiotemporal). Pure-stereo (no IMU) self-cal exists but is mostly **extrinsic-only** with intrinsics assumed known — and crucially, **monocular/stereo-without-IMU self-calibration cannot pin absolute scale**, so the baseline/depth-scale degeneracy of §2 is *not* automatically cured without a metric anchor (IMU, known size, or ToF).
- **Photometric self-calibration** (exposure/vignette/response) — orthogonal; matters for *direct/intensity-based* methods and for the prototype's motion-blur/exposure findings, not for the geometric depth-scale problem.

---

## 5. Observability — the catch (what motions/scenes are required, and the degeneracies)

Online self-calibration only works **if the motion excites the parameters.** This is the single most important honest caveat — and it is the *same* class of problem as the prototype's offline degeneracy (§2), just during operation.

From the definitive observability analysis (Yang, Geneva, Huang — *Online Self-Calibration for VINS: Models, Analysis, and Degeneracy*, IEEE T-RO 2023 / arXiv 2201.09170):
- With full sensor calibration, a VINS has exactly **4 unobservable directions** — global **yaw + 3-DoF translation** (the usual gauge freedoms). **All sensor calibration parameters (camera intrinsics, IMU intrinsics, cam–IMU extrinsics, time offset) ARE observable — but only under fully-excited 6-axis motion** [src: arXiv 2201.09170].
- **Degenerate motions make specific parameters unobservable.** The paper identifies *primitive* degenerate motions whose combinations are also degenerate. Concretely: **one-axis rotation is degenerate for cam–IMU translation** (Mirzaei & Roumeliotis), and insufficiently-excited motion (e.g. **no/low rotation, constant velocity / no acceleration, single-axis motion, planar-only motion**) starves the calibration directions [src: arXiv 2201.09170]. *"Degenerate motions can and do have a significant negative impact on the estimator,"* and **under-actuated robots are most at risk** — a wheeled ground rover that mostly drives flat and straight is close to a degenerate motion profile.

**Direct implication for our land-rover (`[[land-rover-v1-rig]]`):** a ground robot that drives mostly forward on a plane, with little roll/pitch and constant speed, **does not excite the calibration parameters well** — naive "always-on" online calibration could *drift* rather than tighten. Mitigations: (a) keep good priors and let online cal only *refine* within tight bounds; (b) seed from a solid offline calibration (§3); (c) opportunistically calibrate during informative motion (turns, accelerations, varied-depth scenes) and freeze it during degenerate stretches; (d) for stereo, **extrinsic** online cal is far more robust than full-intrinsic online cal and handles the most common real drift (thermal/mechanical baseline shift) [src: MDPI Sensors 2020; Hansen/CMU]. Scene matters too: textured, depth-varied scenes give the structure that constrains intrinsics; blank fronto-parallel walls re-create the §2 ambiguity.

---

## 6. Mapping to our problem — does this fix the relocalization wall, and the MVP

**Would online self-cal plausibly fix the relocalization geometry wall?** **Partly, and it's the right long-term direction — but it is not a magic bullet, and not the *first* fix.**
- The wall is *noisy/biased 3D from loose calibration*, and a wrong baseline/`fx` is exactly the kind of error online geometric self-cal (OpenVINS-style) is built to remove **provided the motion excites it (§5)**. So yes, over a robot's life, self-cal is the principled way to "tighten its own calibration."
- **But** the prototype's headline failure (§2 degeneracy, wrong scale) is *also* curable far more cheaply by **fixing the offline capture protocol (tilt + depth + corners) and adding a known-distance metric anchor (§3)** — and absolute scale specifically needs a metric reference regardless of how clever the self-cal is (a no-IMU stereo rig cannot self-recover absolute scale [src: arXiv 2001.05267]). **Do the offline fix first; it removes the current wall at lowest cost.**
- Online self-cal then earns its keep for **drift over the robot's life** — thermal expansion, knocks, mounting creep change the baseline/extrinsics, and an offline calibration goes stale. This is the lifelong-autonomy case the human asked about, and where OKVIS2-X / OpenVINS shine.

**Minimal viable version to prototype (cheapest first):**
1. **Offline first (now):** re-solve with tilt+depth+corner coverage, try `cv2.fisheye` if rational keeps diverging, add the **known-distance + flat-wall planarity verification** as a *constraint and acceptance gate* (retires **P-002**, validates metric scale). This alone likely clears the current wall.
2. **Then online EXTRINSIC self-cal (MVP):** add an IMU (already rung-1 of the [[passive-stereo-robustification]] ladder) and run a VIO that does online **cam–IMU extrinsic + time-offset** calibration — **OpenVINS** is the lowest-friction open stereo+IMU platform with online cal out of the box, with **OKVIS2** as the SLAM-grade alternative. Extrinsic-only is the robust, observable-friendly subset that handles real mechanical drift without risking intrinsic blow-up on degenerate ground-rover motion.
3. **Later / optional:** enable online **intrinsic+distortion** refinement only with tight priors and only when motion is informative; add **online photometric cal** (DSO-style) if a direct/intensity front-end is adopted or exposure/blur (already a logged finding) keeps hurting tracking.

The IMU does double duty: it is rung-1 robustification *and* the sensor that makes online geometric self-calibration observable and absolute-scale-recoverable. That convergence is the strongest argument for adding it next.

---

## Sources

Papers / libraries (web-researched 2026-06; verify before load-bearing use):
- Yang, Geneva, Huang. *Online Self-Calibration for Visual-Inertial Navigation: Models, Analysis, and Degeneracy.* IEEE T-RO 2023 / **arXiv 2201.09170** — observability of full VI calibration; 4 unobservable directions; primitive degenerate motions. https://arxiv.org/abs/2201.09170
- Geneva et al. **OpenVINS** — research VINS platform with online camera intrinsic/extrinsic + time-offset calibration. https://docs.openvins.com/gs-calibration.html
- **OKVIS2-X**: Open Keyframe-based VI-SLAM with online intrinsic+extrinsic spatiotemporal calibration. **arXiv 2510.04612**. https://github.com/ethz-mrl/okvis2
- **Kalibr** (ETH-ASL) — offline multi-cam + cam–IMU spatial/temporal calibration (the offline reference). https://github.com/ethz-asl/kalibr
- **VINS-Fusion** (HKUST) — sliding-window VIO with online extrinsic/time-offset calibration.
- SLAM-Based Self-Calibration of a Binocular Stereo Rig in Real-Time. **MDPI Sensors 2020, 20(3):621.** https://www.mdpi.com/1424-8220/20/3/621
- Hansen et al. *Online Continuous Stereo Extrinsic Parameter Estimation* (CMU RI). https://publications.ri.cmu.edu/storage/publications/pub_files/2012/6/2171.pdf
- *High-Precision Online Markerless Stereo Extrinsic Calibration.* **arXiv 1903.10705.** https://arxiv.org/pdf/1903.10705
- *Correcting Decalibration of Stereo Cameras in Self-Driving Vehicles.* **arXiv 2001.05267** — baseline = absolute-scale anchor; needs external range to fix uniquely. https://arxiv.org/pdf/2001.05267
- Bergmann, Wang, Cremers. *Online Photometric Calibration of Auto-Exposure Video for VO & SLAM.* **arXiv 1710.02081** — response/vignette/exposure online; DSO fails without it. https://arxiv.org/abs/1710.02081
- Tangram Vision — *Narrow-FOV Calibration Made Easy(er)* — fronto-parallel focal↔depth ambiguity; tilt/foreshortening breaks it; ~45° dihedral guidance. https://www.tangramvision.com/blog/nfov-calibration-made-easier
- OpenCV docs — **Fisheye camera model** (Kannala–Brandt, 4 params). https://docs.opencv.org/4.x/db/d58/group__calib3d__fisheye.html
- OpenCV calibration practical guides (rational vs fisheye, wide-FOV) — Iamgouri / Manthan Sharma (Medium).
- RTAB-Map **Stereo-mapping** wiki (built-in stereo calibration GUI). https://github.com/introlab/rtabmap/wiki/Stereo-mapping
- Depth geometry z=f·b/d and ε_z=z²/(fb)·ε_d — e-con Systems; NasuhcaN (Medium).

Cross-refs to existing wiki (their own raw citations carried through): [[passive-stereo-robustification]] §5 (speckle as calibration validator; flat-wall planarity / P-002), [[visual-inertial-slam]] (stereo+IMU stack), [[land-rover-v1-rig]] (ground-rover degenerate-motion risk).
