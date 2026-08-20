# Camera ↔ LiDAR Spatiotemporal Calibration & Reconciling Two Trajectory Estimates

How to **pin the camera↔LiDAR space-time relationship** and then **reconcile two trajectory estimates of one walk** — the temporal (time-offset, possibly *drifting*) and spatial-extrinsic (mount transform) twin of the back-end reconciliation in [[trajectory-refinement-and-fusion.md]] and the map-side warp of [[lidar-sfm-map-alignment-methods.md]]. This page fills the **temporal** gap those two leave open and the **extrinsic-under-weak-motion** gap, then ties both to fusion SOTA. *(synthesis — assembled from the cited primary sources.)*

> **Our concrete problem (what this page is judged against).** A **hand-held, no-IMU**, consumer-cost rig (SVPRO USB stereo + 2D LiDAR) walked one room, logged with **approximate stdout-buffered time-sync** ([[land-rover-v1-rig]]). Two estimates of the same motion — a **2D-LiDAR SLAM** trajectory and a **monocular hloc-SfM** camera path (Umeyama-aligned into the LiDAR frame) — disagree by a **genuine smooth ~13 cm warp**, on top of a **confirmed ~−562/−650 ms time lag** that is **possibly drifting**, with a possible normalization/gauge trade-off. Motion is **mostly planar hand-walking** (low parallax, weak out-of-plane excitation). Goal: (a) detect/model the time offset incl. drift, (b) pin the extrinsic despite weak motion, (c) attribute the residual to the right sensor.

> **Read alongside:** [[trajectory-refinement-and-fusion.md]] (the robust two-trajectory back-end — this page is its *time-and-extrinsic* front-half), [[lidar-sfm-map-alignment-methods.md]] (the map-side smooth-warp twin), [[reconciling-competing-signals.md]] (cross-field robust fusion + over-pruning guard), [[lidar-visual-fusion-slam]] (the coupling spectrum), [[relocalization-method-bakeoff]] (hloc as the camera path), [[land-rover-v1-rig]] (the rig + buffered-sync source of the lag). Supersedes the stub [[camera-lidar-temporal-calibration-and-pose-interpolation]].

---

## 0. Framing: a time axis and a space transform, both partly unobservable for us

Two asynchronous trajectories of one motion differ along **four coupled axes**, and conflating them is the trap:

1. **A time offset `td`** — a constant shift between the two clocks (triggering + transmission + **buffering** latency). Our ~−562/−650 ms is large and dominated by **stdout buffering**, not hardware jitter.
2. **A *drift* in `td`** — clock skew (the two oscillators run at slightly different rates) or **variable buffering** (a flush stalls, the lag grows, then catches up). A drifting offset masquerades as a smooth trajectory warp — exactly our ~13 cm signature, so the two problems are **entangled** and must be separated.
3. **A spatial extrinsic** `T_CL` (the camera↔LiDAR mount transform) — for us, dominated by the **~+99° mount yaw** (project *SfM-not-extrinsic* / *yaw-is-time-varying* findings) and the **~7 cm scan-plane offset** ([[land-rover-v1-rig]]).
4. **A scale/gauge freedom** — monocular SfM has a free scale (and a 7-DOF Sim(3) datum) the LiDAR fixes; a wrong scale or unfixed gauge can absorb time/extrinsic error and hide it.

The whole method set below exists to **separate these four** so a residual is attributed to its true cause, never warped away. The binding rule from [[reconciling-competing-signals.md]] applies throughout: *down-weight and flag, never silently fit.*

---

## 1. Temporal calibration — estimating the time offset `td`

### 1a. Motion-based cross-correlation (the cheap, IMU-free first cut — best fit for us)

Align the **shared motion signal** the two sensors both observe and read off the lag from where they best correlate. No target, no extrinsic needed first.

| Method | Core idea | What it needs | When it fails / for us |
|---|---|---|---|
| **Angular-velocity cross-correlation** (general signal-processing form) | Both sensors observe the **same rotational motion**; the temporal offset is the **argmax of the cross-correlation** of the two angular-velocity (or yaw-rate) traces. The standard recover-the-lag tool. [src: spatiotemporal-review-2025] | Two motion traces (here: LiDAR yaw-rate from scan-matching vs SfM yaw-rate from the camera path) and **enough rotation** to make the correlation peak sharp. | Pure translation → flat correlation, no peak. **For us:** hand-walking has plenty of yaw → a clean, sharp peak; **this is the recommended first estimator of our ~−600 ms lag.** Robust to the absolute extrinsic (rotation magnitude is frame-independent). |
| **Trace correlation + quadratic refinement** — Qiu | Cross-correlate camera vs IMU angular-velocity *traces*, then **fit a quadratic** around the peak for sub-sample resolution → mean offset error < 0.5 ms. [src: gyro-camera-align-survey] | Same motion traces; a parabola fit gives **sub-frame** `td`. | The sub-frame refinement is exactly what lifts a frame-quantised estimate to ms precision — directly portable to our yaw-rate traces. |
| **Curve registration in orientation space** — Kelly, Sukhatme | Treat time-delay as a **curve-registration** problem in SO(3): align the orientation curve from gyro integration with the one from camera observations; the delay is the registration shift. [src: gyro-camera-align-survey] | Orientation curves from both sensors. | Registration (vs raw cross-correlation) is more robust to noise/partial overlap — useful if our SfM yaw is patchy. |
| **3-D motion correlation via CCA** — (motion-correlation framework) | Use **Canonical Correlation Analysis** on the two 3-D angular-velocity vector streams to jointly recover **time offset *and* extrinsic rotation** in one shot, real-time. [src: spatiotemporal-review-2025, motion-corr-cca] | Two 3-D angular-velocity streams. | Solves `td` **and** the yaw extrinsic together from the same correlation — appealing for us since both are unknown. Needs reliable 3-D angular velocity (our 2D LiDAR gives mainly yaw-rate, so the 3-D version is partly degenerate — see §3). |

**Bottom line for us:** motion-based yaw-rate cross-correlation is the **right first estimator** — IMU-free, extrinsic-free, exploits the rotation we *do* have, and it is how the ~−562/−650 ms was (and should be) measured. Refine with a quadratic-peak fit.

### 1b. Continuous-time (B-spline / GP) joint estimation — `td` as an optimisation variable

Represent the trajectory as a **continuous function** so any sensor's measurement is a query at its native (offset-shifted) timestamp — `td` then enters the residual as a *differentiable variable* and is optimised jointly with poses and extrinsic.

| Method | Core idea | What it needs | For us |
|---|---|---|---|
| **Kalibr / continuous-time batch** — Furgale, Barfoot, Sastry | The **first** B-spline continuous-time calibrator: parameterise the trajectory by control points, embed `td` directly in the measurement model, solve a **maximum-likelihood batch** for extrinsic + `td` together. Achieves `td` error **< 0.04 ms** but needs **~300 s** of excitation — built for static high-precision rigs. [src: spatiotemporal-review-2025, kalibr-furgale] | A long, **well-excited** sequence (all axes); originally needs an IMU/target. | Gold-standard precision but **excitation-hungry**; our single planar room-walk under-excites it. Conceptual frame, not our turnkey tool. |
| **CLINS** — Lv, Zhang et al. | Continuous-time **cubic B-spline** trajectory for a LiDAR-inertial system; LiDAR point-to-plane + IMU factors jointly solve extrinsic, `td`, and control-point poses; **decouples deformation complexity from measurement rate** (asynchronous data = just query the spline). [src: clins] | Smooth motion; control-point density matched to motion bandwidth; (in original form) an IMU. | The B-spline machinery is reusable **without** an IMU if the LiDAR/SfM motion is smooth — but a knot-spaced spline can only model **smooth** `td` drift, which is the point (§2). |
| **Multi-LiDAR/camera + IMU continuous-time** — Lv, Zhang, Lu, Zhu, Wu 2025 | B-spline IMU trajectory; each camera/LiDAR measurement queries the spline at `t + td`; `td` per sensor optimised with the 6-DOF extrinsic. **"Any sensor interpolates its pose on the spline by timestamp without new variables."** [src: ct-multisensor-2025] | Rich motion (esp. rotation about the excitation axis); IMU-centric. | Explicitly notes **z-translation along the rotation axis is unobservable** under their figure-eight — the same planar-degeneracy caveat that bites us (§3). |
| **GP trajectory / white-noise-on-acceleration prior** — Barfoot, Tong, Anderson; GPTR | Trajectory as a **Gaussian Process** (WNOA/WNOJ kinematic prior); continuous, analytically differentiable, with **calibrated posterior variance**; `td` embeds the same way and the GP **regularises under-constrained motion**. [src: gp-traj-barfoot, gptr-2024] | A motion prior (kernel length-scale) instead of knot spacing. | The GP variance flags **where `td`/pose is well-constrained vs guessed** — a free self-validation field; the same WNOA prior used for the smooth-warp correction in [[lidar-sfm-map-alignment-methods.md]] §4. |

### 1c. Online / filter-based `td` estimation — for a *changing* offset

| Method | Core idea | What it needs | For us |
|---|---|---|---|
| **VINS-Mono online temporal calibration** — Qin & Shen (IROS 2018) | Model `td` by **shifting feature observations along the image timeline** at **feature velocity**; add `td` as a state in the sliding-window optimisation, re-estimated every window. [src: qin-shen-temporal] | A VIO/sliding-window estimator; feature velocity (optical-flow) per frame. | The canonical "estimate `td` live" recipe; the **feature-velocity reprojection-shift** model is reusable even though we have no IMU — shift SfM observations vs LiDAR poses. Treats `td` as **slowly-varying** (re-solved per window) → naturally tracks slow drift. |
| **Universal online temporal calibration** — (2025) | Generalises Qin & Shen to any optimisation-based VINS; keeps `td` a windowed state. [src: universal-temporal-2025] | Optimisation back-end. | Confirms the windowed-`td` pattern is the standard way to absorb a drifting offset offline-or-online. |

---

## 2. The *time-varying / drifting* offset — detecting and modelling it (our key open question)

This is the gap the other pages don't cover. A constant-`td` assumption is the usual modelling choice — and the usual mistake when the offset drifts.

- **Why it drifts.** Two causes, both plausible for our rig: **clock skew** (the camera and LiDAR oscillators run at slightly different ppm, so the offset accumulates **linearly** with time) and **variable buffering** (stdout flush stalls → the lag jumps, then relaxes — a **non-linear, bursty** drift). Clock-skew literature treats the offset as offset+skew and **tracks both with a Kalman filter** under a dynamic clock model, the standard cure for low-precision clocks with time-varying drift. [src: clock-skew-kalman] A **linear** drift ⇒ fit `td(t) = td₀ + α·t` (constant skew); a **non-linear/bursty** drift ⇒ a time-varying state.
- **The constant-`td`-is-wrong finding (most on-point for us).** **TON-VIO** (Mar 2024) shows that existing methods *"oversimplify the time offset as a constant value with white Gaussian noise — conditions seldom satisfied"* in real dynamic motion, and that **time-varying** `td` is what causes positioning drift. It models `td` as a **trajectory over time** (LSTM time-offset prediction network) rather than a scalar. [src: ton-vio] The transferable lesson without the neural net: **promote `td` from a scalar to a low-DOF function of time** (a few B-spline knots / a GP / a linear-skew term) and estimate it.
- **How to *detect* a drift (cheap, do this first).** Run the §1a cross-correlation in a **sliding window** along the run and plot `td(window)`. **Flat ⇒ constant offset** (a single scalar is fine); a **steady ramp ⇒ clock skew** (fit the slope); a **step/bump ⇒ buffering stall** (segment there). This directly tests "is the lag drifting?" before committing to a model, and tells the smooth-warp work in [[lidar-sfm-map-alignment-methods.md]] whether the ~13 cm is **time** (drifting `td`) or **space** (SfM scale drift) — the disambiguation that separates the two pages' problems.
- **Modelling, matched to the detected shape.** Constant → scalar `td`; linear skew → `td₀ + α·t`; smooth wander → a **low-knot B-spline / long-length-scale GP** `td(t)` (§1b), which is **structurally incapable of high-frequency over-fit** (the DOF-cap guard, [[lidar-sfm-map-alignment-methods.md]] §7). Bursty buffering → **change-point segment** the run (CUSUM on the windowed-`td` series, [[reconciling-competing-signals.md]] §7) and a piecewise-constant `td`.
- **The time-vs-warp confound (binding caveat).** A constant scale error, a constant `td`, and a constant velocity are partially **aliased** — a wrong scale can hide a time offset and vice-versa. **Break the alias with rotation:** the cross-correlation `td` from yaw-rate (§1a) is **scale-independent**, so measure `td` from rotation *first*, fix it, *then* fit scale/warp — don't co-estimate them blind.

---

## 3. Spatial extrinsic calibration camera↔LiDAR — and why our motion under-constrains it

### 3a. The method families

| Family | Core idea | What it needs | For us |
|---|---|---|---|
| **Motion-based / hand-eye `AX = XB`** — survey: Tsai-Lenz lineage | Estimate each sensor's **ego-motion** independently (A = camera motion, B = LiDAR motion), solve `AX = XB` for the extrinsic `X`, refine. The targetless workhorse. [src: targetless-survey, cross-modality-techrxiv] | Both ego-motions + **sufficient rotation *and* translation** excitation; hardware time-sync (or a jointly-estimated `td`). | Directly applicable (we have two ego-motions) **but** hits the planar-degeneracy wall below — and needs the §1 `td` solved first or jointly. |
| **Targetless feature alignment** (edge / plane / mutual-information) | Align **cross-modal structure** — project LiDAR edges/planes into the image and maximise alignment (edge correlation, **mutual information**, or cross-modality structure consistency). [src: cross-modality-techrxiv, mutual-info-calib] | Overlapping FoV; co-observed edges/planes; a decent initial guess. | A **2D** LiDAR sees a single scan line, not a depth image → only **line/plane-where-the-scan-cuts** features are available; appearance alignment is thin. Weaker for us than for 3-D-LiDAR rigs. |
| **CCA motion-correlation (rotation)** — §1a | Recovers the **extrinsic rotation** alongside `td` from angular-velocity correlation. [src: motion-corr-cca] | 3-D angular velocity. | Gives the yaw extrinsic cheaply; the **+99° mount yaw** is the dominant unknown, so this is high-value — but our 2D LiDAR yields mainly yaw-rate (one rotation axis), limiting the full 3-D rotation solve. |

### 3b. Observability — why planar, low-parallax hand motion under-constrains the extrinsic (binding for us)

Motion-based calibration is only as observable as the **motion excites it**. The degenerate cases are well-documented and *all bite our rig*:

- **No rotation ⇒ translation extrinsic is unobservable.** Hand-eye `AX = XB` *"presents a particular degeneration when sensor motions lack rotation"* — common for ground vehicles on straight roads — *"deteriorating translational calibration."* [src: cross-modality-techrxiv] We have yaw but little else.
- **Planar motion ⇒ roll, pitch, and z-translation are unobservable.** *"In ground-robot planar-motion scenarios, the absence of excitation along the vertical (z) axis renders roll and pitch rotations and the z-translation unobservable."* [src: planar-degeneracy] Our hand-walk is near-planar → the **~7 cm scan-plane height offset (z)** ([[land-rover-v1-rig]]) is **exactly the unobservable DOF** — it must be **measured directly**, not solved from motion.
- **Low parallax ⇒ weak metric translation.** Monocular SfM translation is scale-soft under low parallax; that softness propagates straight into the translation extrinsic estimate.
- **Rotation about a single axis ⇒ only translation ⊥ to it is observed** (the §1b figure-eight caveat: *"z-translation along the rotation axis is insignificant/unobservable"*). [src: ct-multisensor-2025]

**The fix the literature uses — and our route:**
1. **Add a geometric constraint for the unobservable DOF.** **GRIL-Calib**'s **Ground-Plane-Motion (GPM)** constraint recovers full 6-DOF *including the theoretically unobservable z/roll/pitch* by adding a ground-plane observation. [src: planar-degeneracy] **For us:** **measure the 7 cm scan-plane offset directly** (it's a fixed rig dimension — already in `data/calib/rig_geometry.json`) rather than asking near-planar motion to reveal it.
2. **Use the SfM-into-map route for yaw, not a motion-solved extrinsic.** The project *SfM-not-extrinsic* finding already concluded the kitchen yaw was unmeasurable from motion and the calib value didn't transfer — register the camera **into the LiDAR frame via hloc-SfM** and read the +99° as the residual ([[relocalization-method-bakeoff]], [[trajectory-refinement-and-fusion.md]] §1). The **yaw-is-time-varying** finding means **re-measure per capture**, never reuse.
3. **Excite what you can.** If a re-capture is on the table, add **deliberate out-of-plane tilt and varied yaw** segments — even a little vertical excitation lifts the z/roll/pitch observability toward what GPM otherwise has to assume.

---

## 4. Reconciling the two trajectory estimates & attributing the residual

(The mechanics live in [[trajectory-refinement-and-fusion.md]] and [[reconciling-competing-signals.md]]; here is the **time-and-extrinsic-aware** layer on top.)

- **Trajectory alignment vs scene-geometry alignment — two different anchors.** **Umeyama / Sim(3)** aligns the **paths** (minimise pose-to-pose error) — fast, but a rigid global fit that **can't bend** the camera path to local LiDAR truth and **will absorb a `td`/scale error into a spurious rotation/scale**. **Cloud-to-cloud / shared-static-structure** alignment (ICP/GICP on the SfM cloud ↔ LiDAR cloud, or on co-observed walls) aligns the **geometry**, independent of timing. **Run both and compare:** if path-alignment and geometry-alignment disagree, the gap is a **timing/scale** artefact, not a real spatial offset — a free cross-check ([[lidar-sfm-map-alignment-methods.md]] §6 reprojection check is the camera-side twin). [src: zhang-scaramuzza-eval]
- **Constrained Umeyama as a calibration alarm.** Align with the **+99° yaw as a hard constraint**, solving only the residual offset; a **large residual rotation ⇒ the yaw or the `td` is wrong**, not the data ([[reconciling-competing-signals.md]] §0). This turns the alignment step into a `td`/extrinsic sanity test.
- **Pose-graph fusion with the right covariances.** Add both chains to one factor graph with **honest, calibrated covariances** (LiDAR tight, SfM loose) — under-stated SfM covariance makes the solver "resolve" a real `td`/warp by smearing it. Per-sensor covariance + robust kernel is the asymmetric-trust optimiser ([[trajectory-refinement-and-fusion.md]] §2–3, [[lidar-sfm-map-alignment-methods.md]] §5).
- **Attributing a residual to one sensor — what GT it needs.** A bare two-trajectory disagreement **cannot** say *which* is wrong (the gauge is shared). To attribute:
  - **An independent anchor** — tape-measured wall positions / the SfM-localised fridge to 0.45 m of GT ([[trajectory-refinement-and-fusion.md]]); whichever trajectory the anchor agrees with is the trusted one *there*.
  - **A degeneracy/observability check** — a LiDAR rank-deficient against parallel walls (Zhang-Kaess-Singh) is *the* one to distrust *in its degenerate direction*; let the camera supply that DOF ([[trajectory-refinement-and-fusion.md]] §6).
  - **The drift signature** — a residual that **grows with arc-length** points at **SfM scale drift**; one that **grows with wall-clock time** points at **clock skew (`td` drift)**. Plotting the residual against **both** axes separates them — the single most useful attribution test for our entangled problem.

---

## 5. Visual–LiDAR fusion SOTA & which coupling fits a no-IMU rig

- **The coupling spectrum.** **Loosely-coupled**: each sensor estimates motion separately, fused at a back-end filter/graph (V-LOAM: VIO gives a motion prior + scale, LiDAR refines & de-drifts). **Tightly-coupled**: raw measurements jointly optimised (LIC-Fusion, R2LIVE, Coco-LIC, TCP-VLOAM) — higher accuracy/robustness **but typically IMU-centric**. [src: vloam-scale, coupling-survey]
- **Monocular scale fix without an IMU.** **V-LOAM-style** systems **recover monocular depth/scale from co-projected LiDAR points** and use high-rate camera poses to reduce LiDAR drift — *the* IMU-free way to make a monocular path metric, by borrowing the LiDAR's scale. [src: vloam-scale] This is our regime: the LiDAR is the metric anchor; the camera supplies high-rate, texture-rich relative motion.
- **No IMU ⇒ loosely-coupled back-end fusion is the robust choice.** Tight LVI leans on the IMU to bridge between LiDAR sweeps and bound scale; without one, the safe, robust design is **two independent front-ends + a robust back-end graph** — exactly the [[trajectory-refinement-and-fusion.md]] / [[lidar-visual-fusion-slam]] conclusion. The camera is a **second constraint chain + relocalisation**, joined where a wall-blind passive-stereo front-end can't corrupt LiDAR geometry.

---

## 6. Recommendation for our case (priority order)

Smooth ~13 cm warp · confirmed ~−600 ms lag, possibly drifting · planar low-parallax hand motion · no IMU · buffered sync:

1. **Detect drift first (§2):** sliding-window yaw-rate cross-correlation → plot `td(window)`. Flat / ramp / step decides everything downstream. **Cheapest, most decisive single experiment.**
2. **Measure `td` from rotation (§1a):** full-run yaw-rate cross-correlation + quadratic-peak refine — **scale-independent**, so it pins the lag without contaminating it with the warp. Fix `td` (or `td(t)`) **before** touching scale.
3. **Pin the extrinsic the observable way (§3b):** **measure** the 7 cm z-offset directly (it's geometrically unobservable from our planar motion); take **yaw from SfM-into-map**, re-measured per capture (never reuse — *yaw-is-time-varying*). Don't motion-solve the full 6-DOF from a near-planar walk.
4. **Reconcile time-aware (§4):** align paths (constrained Umeyama, yaw as alarm) **and** geometry (GICP on shared walls); disagreement ⇒ timing/scale artefact. Attribute the residual by plotting it vs **arc-length** (SfM scale drift) **and vs wall-clock** (clock skew).
5. **Fuse loosely (§5):** LiDAR-metric anchor + SfM second chain in a robust factor graph with honest covariances ([[trajectory-refinement-and-fusion.md]]); the smooth residual then feeds the map-side warp ([[lidar-sfm-map-alignment-methods.md]]).

Across all: **separate time from space from scale before fusing** — measure `td` from rotation, the z-extrinsic from the ruler, yaw from SfM — and **flag, never silently fit** ([[reconciling-competing-signals.md]]).

---

## Sources

| Tag | Work | Year |
|---|---|---|
| spatiotemporal-review-2025 | *Camera, LiDAR, and IMU Spatiotemporal Calibration: Methodological Review and Research Perspectives*, Sensors 25(17):5409 | 2025 |
| motion-corr-cca | *Real-Time Temporal and Rotational Calibration of Heterogeneous Sensors Using Motion Correlation Analysis* (CCA on 3-D angular velocity) | 2020 |
| gyro-camera-align-survey | Qiu (trace-correlation + quadratic refine); Kelly & Sukhatme (curve registration in orientation space) — as surveyed in [spatiotemporal-review-2025] | — |
| kalibr-furgale | P. Furgale, J. Rehder, R. Siegwart / T. Barfoot — Kalibr continuous-time camera-IMU spatiotemporal calibration (B-spline, `td` as variable) | 2013/2016 |
| clins | J. Lv, K. Hu, J. Xu, Y. Liu et al. — *CLINS: Continuous-Time Trajectory Estimation for LiDAR-Inertial System* (arXiv 2109.04687) | 2021 |
| ct-multisensor-2025 | Y. Lv, Y. Zhang, C. Lu, J. Zhu, S. Wu — *Targetless Intrinsics and Extrinsic Calibration of Multiple LiDARs and Cameras with IMU using Continuous-Time Estimation* (arXiv 2501.02821) | 2025 |
| gp-traj-barfoot | T. Barfoot, C. H. Tong, S. Särkkä — *Batch Continuous-Time Trajectory Estimation as Exactly Sparse Gaussian Process Regression* (arXiv 1412.0630); WNOA/WNOJ priors | 2014 |
| gptr-2024 | *GPTR: Gaussian Process Trajectory Representation for Continuous-Time Motion Estimation* (arXiv 2410.22931) | 2024 |
| qin-shen-temporal | T. Qin & S. Shen — *Online Temporal Calibration for Monocular Visual-Inertial Systems*, IROS 2018 (arXiv 1808.00692; VINS-Mono `estimate_td`) | 2018 |
| universal-temporal-2025 | *Universal Online Temporal Calibration for Optimization-based Visual-Inertial Navigation Systems* (arXiv 2501.01788) | 2025 |
| clock-skew-kalman | *Tracking Low-Precision Clocks with Time-Varying Drifts Using Kalman Filtering*, IEEE/ACM Trans. Networking; clock offset+skew dynamic model | 2011 |
| ton-vio | *TON-VIO: Online Time Offset Modeling Networks for Robust Temporal Alignment in High Dynamic Motion VIO* (arXiv 2403.12504) — constant-`td` is wrong; model `td(t)` | 2024 |
| targetless-survey | *Automatic Targetless LiDAR-Camera Calibration: A Survey* | 2022 |
| cross-modality-techrxiv | *Targetless LiDAR-Camera Calibration via Cross-Modality Structure Consistency* (hand-eye degenerate-motion problem) | 2023 |
| mutual-info-calib | *From Chaos to Calibration: A Geometric Mutual Information Approach to Target-Free Camera-LiDAR Extrinsic Calibration* (arXiv 2311.01905) | 2023 |
| planar-degeneracy | GRIL-Calib / ground-planar-motion (GPM) constraint — planar-motion z/roll/pitch unobservability and its fix | 2023/2024 |
| vloam-scale | *Visual-LiDAR Odometry and Mapping with Monocular Scale Correction and Visual Bootstrapping* (arXiv 2304.08978); V-LOAM lineage | 2023 |
| coupling-survey | LIC-Fusion / R2LIVE / Coco-LIC / TCP-VLOAM — loosely-vs-tightly-coupled visual-LiDAR(-inertial) fusion | 2019–2024 |
| zhang-scaramuzza-eval | Z. Zhang & D. Scaramuzza — *A Tutorial on Quantitative Trajectory Evaluation for VIO* (ATE/RPE, Umeyama) | 2018 |
| prototype | drone-prototype: ~−562/−650 ms buffered lag, +99° mount yaw, 7 cm scan-plane offset, ~13 cm warp — carried via [[land-rover-v1-rig]] (rig + scan-plane offset + buffered sync), [[relocalization-method-bakeoff]] | — |

## Related

- [[trajectory-refinement-and-fusion.md]] — the robust two-trajectory back-end; this page is its time-and-extrinsic front-half
- [[lidar-sfm-map-alignment-methods.md]] — the map-side smooth-warp twin (is the 13 cm time or space?)
- [[reconciling-competing-signals.md]] — cross-field robust fusion, χ²/CUSUM drift detection, the over-pruning guard
- [[lidar-visual-fusion-slam]] — the coupling spectrum; why no-IMU ⇒ loosely-coupled
- [[relocalization-method-bakeoff]] — hloc SfM camera path; the SfM-into-map (not extrinsic) route for yaw
- [[land-rover-v1-rig]] — the rig: the stdout-buffered sync (~−600 ms lag) and the 7 cm scan-plane z-offset = the planar-motion-unobservable DOF (measure it directly)
- [[camera-lidar-temporal-calibration-and-pose-interpolation]] — superseded stub; this page replaces it
