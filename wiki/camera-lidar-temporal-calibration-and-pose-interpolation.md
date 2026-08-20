# Camera↔LiDAR Temporal Calibration and Per-Frame Pose Interpolation

> **⚠️ SUPERSEDED for object anchoring (flagged by librarian 2026-06-19, EDA129–132).** This page's load-bearing
> premise — that the **spatial extrinsic is already measured (yaw ≈ −2.2°)** and only the *temporal* problem
> remains — did **not hold up**. The camera↔LiDAR yaw could not be measured reliably on the kitchen sweep
> (EDA129/131: per-frame std 91–117°; the "global peak" jumped −64° → +149° by swapping raw vs cached scans),
> and the one clean static-calib value (**−5.6°**, not −2.2°) does **not transfer** to a moving sweep. The
> resolution (EDA132) was to **abandon the extrinsic entirely** and register each camera frame directly into the
> LiDAR map frame via **hloc-SfM** — decimetre-accurate object anchoring with **no extrinsic** (see
> `eda/EDA133-sfm-anchor-pass/PROGRESS_REVIEW.md`, parked **P-048**). See [[camera-lidar-spatiotemporal-calibration]]
> for the page that supersedes this one's spatial/extrinsic scope. The **temporal-offset** content below is
> still valid and was confirmed in practice (δt ≈ **−562…−580 ms**, recovered by motion cross-correlation, corr
> 0.98 — *not* raw timestamps). The **−2.2°/2 cm extrinsic** and the "drop frames onto a trusted trajectory via a
> known extrinsic" framing are **stale** — do not use them as load-bearing. Kept for the temporal method + the
> dead-end record.

How to get the **best per-frame camera pose** on our specific rig, where a 2D LiDAR's per-scan poses are already solved and **snapped to a world floor plan** (we trust them), the spatial camera↔LiDAR extrinsic is **already measured** (yaw ≈ −2.2°, planar offset ≈ 2 cm — essentially aligned), and the only open problems are **temporal**: (a) a residual hidden time-offset δt between the two streams, and (b) interpolating the camera pose at each camera frame's true time between the bracketing LiDAR scans.

This page is the *temporal* companion to the spatial/fusion pages and deliberately does **not** re-derive them. Read for foundations: [[lidar-visual-fusion-slam]] (the coupling spectrum and *why* we keep geometry on the LiDAR), [[imu-vio-integration-reality]] (the two-clock no-hardware-trigger reality of this rig), [[camera-calibration-and-self-calibration]] (the *spatial* online-calibration survey, incl. the observability/degeneracy catch this page reuses), [[2d-lidar-slam]] (the LiDAR poses we trust), [[visual-inertial-slam]] (the IMU-bearing alternative we don't have). *(research page — sources cited inline; web-researched 2026-06, verify before load-bearing use.)*

> **What's NEW here vs the existing wiki.** The fusion page answers *should we fuse, and where* (answer: loosely, geometry on LiDAR). The IMU page answers *why we have no IMU and what one costs*. The calibration page surveys *spatial* self-calibration. **None** of them covers the concrete problem we now have: **the spatial extrinsic is solved, the LiDAR poses are world-snapped, and we just need to drop each jittery camera frame onto that trusted trajectory at the right time.** That is a *temporal-calibration + trajectory-interpolation* problem, and it is unusually tractable because one sensor (LiDAR) is already the trusted reference — we are not doing joint SLAM, we are *resampling* a known trajectory.

---

## 1. The problem, stated precisely for our rig

Givens:
- **LiDAR trajectory** `T_L(t_k)` at scan times `t_k` (10 Hz, clean), each a world-frame 2D pose `(x_k, y_k, θ_k)` we trust (SLAM-solved + floor-plan-snapped → [[2d-lidar-slam]]).
- **Known extrinsic** `T_LC` (LiDAR→camera), yaw ≈ −2.2°, offset ≈ 2 cm. So at any LiDAR scan, the camera pose is fully determined: `T_C(t_k) = T_L(t_k) · T_LC`.
- **Camera frames** at save-times `s_j` (~5.4 fps but **jittery**: 142–210 ms inter-frame, occasional ~300 ms gaps). No IMU.
- **A shared `time.monotonic()` clock**, BUT the LiDAR `t_ms` is stamped **at parse time** and lags true acquisition by an unknown, possibly-jittery buffer delay; the camera `s_j` is stamped at save (small lag). → A **residual hidden time-offset δt** the timestamps cannot reveal.

Wanted, for each camera frame *j*: its world pose `T_C(s_j_true)`, where `s_j_true = s_j + δt` is its *true* acquisition time on the LiDAR clock.

Two sub-problems, in order:
1. **Estimate δt** — the constant (or slowly-varying) offset that aligns the camera clock to the LiDAR clock (§3).
2. **Interpolate** the camera pose at `s_j_true` between the bracketing LiDAR scans `t_k ≤ s_j_true ≤ t_{k+1}`, *on the manifold* (§4).

The structure that makes this easy: **we have a trusted reference trajectory.** Unlike a VIO system that must estimate δt *and* the trajectory jointly, we already have the trajectory (LiDAR) — δt becomes a 1-D alignment of the camera's *motion signal* against the LiDAR's, and interpolation is a *resample of a known curve*, not a state estimate. This is closer to **trajectory-matching temporal calibration** than to online VINS calibration [src: motion-correlation-2020, trajmatch-2023].

---

## 2. Why timestamps alone are not enough (the hidden lag)

The two clocks are nominally shared, so the *naive* answer is "just use `s_j` directly against `t_k`." The catch is the **acquisition-to-timestamp lag differs between the streams and is not constant**:

- The LiDAR `t_ms` is stamped when the host **parses** a completed scan packet — after an unknown serial/USB buffering delay that can itself jitter (driver wakeups, batching). True photon/laser time is *earlier* than the stamp by an unknown amount.
- The camera `s_j` is stamped at save, also after exposure + USB + MJPG-decode latency (tens of ms, jittery — the same effect documented for the SVPRO in [[imu-vio-integration-reality]] §2).

So there is a **residual δt = (camera lag) − (LiDAR lag)** that the recorded timestamps *cannot* reveal, because each timestamp already bakes in its own lag. This is exactly the regime temporal calibration is built for: *"timestamps of each sensor typically suffer from triggering and transmission delays"* — the misalignment must be recovered from the **data**, not the clocks [src: qin-shen-td-2018]. When this δt is ignored, the error it injects into the camera pose is **proportional to the platform's velocity at that instant** — negligible when stationary, worst during fast rotation (§5).

---

## 3. Estimating δt without a hardware trigger — motion correlation

The workhorse for "two asynchronous sensors, no trigger, recover the lag from data" is **cross-correlation of a shared motion signal**, most robustly **angular velocity** [src: motion-correlation-2020, event-temporal-2025, mdpi-spatiotemporal-2025].

### 3.1 The core idea (angular-rate cross-correlation)

Both sensors observe the *same* rigid-body rotation, so both can produce an **angular-rate time series**:
- **From the LiDAR trajectory:** `ω_L(t_k) = Δθ_k / Δt_k` — differentiate the (trusted, world-snapped) heading. Clean, since the LiDAR poses are good.
- **From the camera:** `ω_C(s_j)` from **frame-to-frame visual rotation** — recover inter-frame yaw from optical flow / essential-matrix or a 2-frame relative-pose estimate; the median/global flow rotation is enough. (We do **not** need metric VO — only the *rotation rate*, which passive stereo can give even on weak texture far better than it gives metric depth.)

Resample both to a common fine grid (cubic interpolation), then find the lag δt that **maximizes the cross-correlation** of `ω_L` and `ω_C`:

> δt\* = argmax_δ  corr( ω_L(t),  ω_C(t + δ) )

*"The most straightforward approach to estimating the temporal offset between two signals is to identify the peak of their cross-correlation"*; *"the cross-correlation method determines the delay by maximizing the correlation between the … angular velocity sequences"* [src: motion-correlation-2020, event-temporal-2025]. Practically: enumerate δ over a plausible window (e.g. ±500 ms) at a coarse step (~10 ms), then **parabolic/sub-sample interpolation around the peak** for sub-step resolution [src: event-temporal-2025].

### 3.2 Why angular velocity (not translation)

Angular rate is the **observable that makes δt identifiable**: rotation produces a large, sharply-timed, scale-free signal both sensors see identically, whereas translation is entangled with scale and is weaker on slow indoor motion. The correlation-based methods explicitly assume rotational excitation: *"the method assumes … rotational platform motion, making angular velocity the primary kinematic observable … this rotational constraint provides the observability needed to decouple temporal offset"* [src: event-temporal-2025]. **Implication for capture:** include a segment with brisk yaw (turning in place) so δt is well-excited (§6). On a pure-straight constant-velocity stretch δt is **poorly observable** — the same degeneracy family as the VINS calibration analysis (constant-velocity / single-axis motion starves calibration directions, [[camera-calibration-and-self-calibration]] §5 / [src: yang-degeneracy-2023]).

### 3.3 The optimization-based alternative (VINS-Mono "Online Temporal Calibration")

If we ever want δt estimated *online* and fused into a joint estimate rather than precomputed, the reference method is **Qin & Shen, "Online Temporal Calibration for Monocular Visual-Inertial Systems"** (the feature behind VINS-Mono's `estimate_td`) [src: qin-shen-td-2018]. The trick: model the **feature's velocity on the image plane**, so a small time shift `td` moves each observed feature by `(velocity × td)`; the reprojection residual becomes a *differentiable function of `td`*, and `td` is added as a **state in the sliding-window optimizer** and refined jointly with poses and feature depths. *"Calibrate temporal offset by jointly optimizing time offset, camera and IMU states, as well as feature locations"* [src: qin-shen-td-2018]. It needs sufficient motion to be observable (same caveat as §3.2). Kalibr does the offline batch equivalent: it embeds the temporal offset directly as an optimization variable in a **continuous-time B-spline** model of the sensor states [src: kalibr-furgale, mdpi-spatiotemporal-2025].

**For us, the cross-correlation method (§3.1) is the right first tool** — it is a one-time 1-D alignment against a trajectory we already trust, no joint estimator needed. The optimization route is the escalation if δt turns out to drift over a session.

### 3.4 Does δt transfer from the IMU-camera literature to LiDAR-camera?

Yes — the *idea* transfers cleanly, because all of it reduces to **align a common motion signal**. IMU-camera methods correlate gyro angular rate against visual angular rate; we substitute the **LiDAR-trajectory angular rate** for the gyro. The LiDAR-camera and trajectory-matching literature does exactly this [src: motion-correlation-2020, trajmatch-2023, mdpi-spatiotemporal-2025]. The one thing the LiDAR can't give that an IMU can is *intra-scan* rate at >100 Hz; but at 10 Hz the LiDAR heading rate is still far denser than our ~5.4 fps camera, so it is the *camera* that limits temporal resolution, not the LiDAR.

---

## 4. Interpolating the camera pose on the manifold

Once `s_j_true = s_j + δt` is known, find the bracketing scans `t_k ≤ s_j_true ≤ t_{k+1}`, let `α = (s_j_true − t_k)/(t_{k+1} − t_k) ∈ [0,1]`, and interpolate the **world camera pose**. Two correctness rules:

### 4.1 Interpolate on SE(2)/SO(2), not on raw `(x,y,θ)`

- **Translation:** linear interpolation (lerp) of `(x,y)` is fine for small Δt at 10 Hz.
- **Rotation: do NOT lerp `θ` naively** — heading is circular and wraps at ±π. We have *already been bitten by `θ ∈ [−π,π]` wrap-around*. The correct interpolation is the **geodesic / SLERP on SO(2)**, equivalently:

  > θ(α) = θ_k ⊕ α · ( θ_{k+1} ⊖ θ_k )

  where `⊖` is the **wrapped angle difference** mapped to `(−π, π]` (`atan2(sin(Δ),cos(Δ))`) and `⊕` re-wraps. This is the SO(2) `log`/`exp` pair: take the *shortest-arc* difference in the Lie algebra, scale, re-exponentiate [src: mrpt-lie, ethz-ct-survey]. For the full pose this is the SE(2) (or SE(3) if we ever lift to 3D) interpolation `T(α) = T_k · exp(α · log(T_k⁻¹ · T_{k+1}))` — *"interpolation of the Lie group follows a smooth geodesic … with ξ = log(g₀⁻¹g₁)"* [src: liegroups-slerp, ethz-ct-survey].

  Naive linear `θ` interpolation fails catastrophically across the wrap (e.g. `θ_k=179°, θ_{k+1}=−179°` lerps through 0° instead of the true 2° arc) — this is the exact bug class to guard against.

### 4.2 Order of operations

Interpolate the **camera** pose, having first applied the extrinsic. Either is valid since `T_LC` is a fixed rigid transform:
- compute `T_C(t_k) = T_L(t_k)·T_LC` and `T_C(t_{k+1}) = T_L(t_{k+1})·T_LC`, then geodesically interpolate between them; **or**
- geodesically interpolate `T_L` then right-multiply by `T_LC`.
Both give the same answer for a rigid extrinsic; pick whichever is clearer in code.

### 4.3 When two-point interpolation isn't enough — continuous-time

Linear (two-knot) interpolation assumes constant velocity between scans — fine at 10 Hz for slow indoor motion, the regime we're in. It breaks when **(a) there are real gaps** (the ~300 ms camera holes, or a missed LiDAR scan), or **(b) acceleration within the interval is significant** (a sharp turn straddling one interval). Then move to a **continuous-time trajectory**: fit a smooth curve through *all* the LiDAR poses and evaluate it at any `s_j_true`. Two representations [src: ethz-ct-survey, gp-vs-spline-2024]:

- **Cumulative B-spline on SE(2)/SE(3)** — piecewise-polynomial, C²-continuous, **local** support (each query depends on only k nearby control points), convex-hull. The standard choice; libraries: **kontiki/cline** (Python-friendly continuous-time SfM, cubic SE(3) B-splines), **basalt** (TUM, spline VIO + strong calib tooling), **GTSAM** (factor-graph backbone) [src: kontiki-docs, coco-lic-2023, ethz-ct-survey]. B-splines assume a **fixed knot spacing**, which is slightly awkward for *jittery* sampling.
- **Gaussian-Process trajectory** (e.g. white-noise-on-jerk / WNOA on SE(3)) — represents the trajectory as a GP, query at any time via interpolation; **handles irregular/sparse sampling naturally without committing to a knot grid**, which fits a jittery low-rate stream better than a uniform spline [src: barfoot-wnoj-2018, gp-vs-spline-2024]. Heavier to implement.

**For our case the honest call (§6): start with two-point geodesic SE(2) interpolation; escalate to a B-spline only if gaps/fast-turn segments visibly hurt** — and only to GP if irregular sampling makes the spline knot grid fight the data. Continuous-time is *over-engineering* for a clean 10 Hz reference trajectory + slow motion; it earns its keep exactly at the gaps.

---

## 5. Validation — how to know δt and the interpolation are right

Three complementary checks, chosen so each isolates a different failure (δt is unobservable when still, bites hardest when rotating):

1. **Stationary segment (δt-irrelevant control).** Hold the rig still for a few seconds. Here the interpolated camera pose must be *constant regardless of δt* — any pose variation across frames exposes a bug in the interpolation/extrinsic, **not** δt. Use this to validate the pipeline mechanics with δt factored out.
2. **Fast-rotation segment (δt-sensitive test).** Turn briskly in place. This is where a wrong δt bites most (error ∝ angular velocity, §2): **sweep δt and minimize a consistency error** — the residual between camera-derived inter-frame rotation and the LiDAR inter-frame rotation at the matched times. The δt that minimizes it should match the cross-correlation peak (§3.1); agreement of two independent estimators is the confirmation. This also catches the wrap-around bug (it blows up the residual across ±π).
3. **Reprojection / map-consistency.** Back-project a feature or object seen in multiple frames using the interpolated poses; with correct δt + interpolation the back-projections should **agree in the world/floor-plan frame** (low scatter). This is the end-to-end check that the pose is actually usable for the mandate (label back-projection onto the floor plan → [[lidar-visual-fusion-slam]]). Drifting/smeared back-projections during turns ⇒ revisit δt or escalate interpolation (§4.3). The flat-wall / known-geometry consistency idea from [[camera-calibration-and-self-calibration]] §3 applies here too.

A practical bonus check: the cross-correlation peak in §3.1 should be **sharp and unimodal** when there's enough rotation; a flat/broad peak means the motion didn't excite δt — recapture with more yaw, don't trust the number.

---

## 6. Recommended minimal pipeline for THIS project

Grounded in our exact givens (trusted 10 Hz world-snapped LiDAR poses + measured extrinsic + jittery ~5.4 fps camera + no IMU). **Simplest-first; escalate only on evidence.**

**Step 0 — sanity, with δt = 0.** Wire up the geodesic interpolation (§4.1) and the extrinsic, set δt = 0, and run the **stationary-segment** check (§5.1). Get the mechanics + wrap-around handling correct *before* touching δt. (Given the timestamps share a clock, δt may already be small.)

**Step 1 — estimate δt by angular-rate cross-correlation (§3.1).** Build `ω_L` from differenced LiDAR heading and `ω_C` from frame-to-frame visual rotation (optical-flow/essential-matrix yaw — rotation only, no metric depth needed). Resample to a common grid, cross-correlate over ±500 ms, parabolic-refine the peak. **Require a brisk-yaw segment** in the data so δt is observable. Confirm the peak is sharp.

**Step 2 — interpolate per frame on SE(2) (§4).** For each camera frame: `s_j_true = s_j + δt`, bracket with LiDAR scans, geodesic-interpolate `T_L` (shortest-arc heading), right-multiply by `T_LC`. Done — that's the per-frame camera pose.

**Step 3 — validate (§5).** Stationary control, fast-rotation δt-sweep (must agree with Step 1's peak), reprojection/back-projection consistency on the floor plan.

**Escalate only if validation fails:**
- Broad/ambiguous cross-correlation peak ⇒ recapture with more rotation (don't reach for fancier estimators first).
- δt appears to **drift within a session** ⇒ move to the **VINS-Mono-style online `td`** as a slow state (§3.3), or re-estimate δt per sub-segment.
- **Gaps (~300 ms) or fast turns** visibly smear back-projections ⇒ replace two-point interpolation with a **cumulative SE(2) B-spline** through the LiDAR poses (kontiki/basalt/GTSAM, §4.3); go **GP/WNOA** only if the jitter makes a uniform knot grid fight the data.

**What NOT to do:** don't build a joint LiDAR-visual continuous-time estimator up front (that's [[lidar-visual-fusion-slam]]'s tight-fusion regime, gated on the IMU we deliberately don't have). We already *trust* the LiDAR trajectory — the task is to **resample a known curve at the right time**, which is a 1-D alignment + a manifold interpolation, not SLAM. Keep geometry on the reliable sensor; let δt + geodesic interpolation be the whole of the temporal layer.

---

## Sources

Web-researched 2026-06; verify before load-bearing use.

- [src: qin-shen-td-2018] T. Qin & S. Shen, *Online Temporal Calibration for Monocular Visual-Inertial Systems*, IROS 2018, **arXiv 1808.00692** — image-plane feature-velocity model makes the time offset `td` a differentiable state, jointly optimized with pose/features in the sliding window (the VINS-Mono `estimate_td` feature). https://arxiv.org/abs/1808.00692
- [src: motion-correlation-2020] *Real-Time Temporal and Rotational Calibration of Heterogeneous Sensors Using Motion Correlation Analysis*, IEEE T-RO 2021 — recover time offset by maximizing cross-correlation of angular-velocity sequences; no hardware trigger. https://www.researchgate.net/publication/347175410
- [src: event-temporal-2025] *Temporal and Rotational Calibration for Event-Centric Multi-Sensor Systems*, **arXiv 2508.12564** (2025) — CCA/cross-correlation of angular rates at coarse step + interpolation refinement; SO(3) cumulative cubic B-spline continuous-time refinement; rotation needed for observability. https://arxiv.org/html/2508.12564v1
- [src: mdpi-spatiotemporal-2025] *Camera, LiDAR, and IMU Spatiotemporal Calibration: Methodological Review and Research Perspectives*, MDPI Sensors 25(17):5409 (2025) — survey of HW-trigger vs motion-correlation vs continuous-time temporal calibration; states Kalibr embeds the offset as an optimization variable in a B-spline model. https://www.mdpi.com/1424-8220/25/17/5409
- [src: trajmatch-2023] *TrajMatch: Towards Automatic Spatio-temporal Calibration … through Trajectory Matching*, **arXiv 2302.02157** — temporal offset from correlation between two trajectories (post-processing trajectory matching). https://arxiv.org/pdf/2302.02157
- [src: kalibr-furgale] P. Furgale et al., **Kalibr** — continuous-time B-spline batch estimator for camera–IMU spatial + **temporal** offset; offline gold standard (≈0.04 ms offset error, ~300 s convergence). https://github.com/ethz-asl/kalibr
- [src: yang-degeneracy-2023] Yang, Geneva, Huang, *Online Self-Calibration for VINS: Models, Analysis and Degeneracy*, IEEE T-RO 2023 / **arXiv 2201.09170** — constant-velocity / single-axis motion starves calibration observability (the degeneracy this page's "need rotation" caveat inherits). https://arxiv.org/abs/2201.09170
- [src: ethz-ct-survey] *Continuous-Time State Estimation Methods in Robotics: A Survey* (ETH) — B-spline vs GP continuous-time trajectory representations; SE(3) geodesic interpolation; locality/C² of cumulative B-splines. https://www.research-collection.ethz.ch/handle/20.500.11850/  (ETH Research Collection)
- [src: gp-vs-spline-2024] *Continuous-Time Trajectory Estimation: A Comparative Study Between Gaussian Process and Spline-based Approaches*, **arXiv 2402.00399** — GP handles irregular/sparse sampling without a fixed knot grid; B-spline locality vs GP tradeoffs. https://arxiv.org/pdf/2402.00399
- [src: barfoot-wnoj-2018] *A White-Noise-On-Jerk Motion Prior for Continuous-Time Trajectory Estimation on SE(3)*, **arXiv 1809.06518** — GP/WNOJ trajectory prior, query at any time; suits asynchronous/irregular sampling. https://arxiv.org/pdf/1809.06518
- [src: kontiki-docs] **kontiki** (Hovrén) — Python toolkit for continuous-time structure-from-motion; cubic SE(3) B-spline trajectories with knot spacing + time offset. https://github.com/hovren/kontiki · https://hovren.github.io/kontiki/
- [src: coco-lic-2023] *Coco-LIC: Continuous-Time Tightly-Coupled LiDAR-Inertial-Camera Odometry using Non-Uniform B-spline*, **arXiv 2309.09808** — continuous-time fusion of asynchronous LiDAR/camera/IMU (the tight-fusion endpoint we are NOT building now). https://arxiv.org/pdf/2309.09808
- [src: mrpt-lie] MRPT — *Lie Algebra methods for SO(2),SO(3),SE(2),SE(3)* — log/exp and geodesic interpolation reference incl. SE(2). https://docs.mrpt.org/reference/latest/group__mrpt__poses__lie__grp.html
- [src: liegroups-slerp] ReSim / ECE276A SE(3) notes — geodesic interpolation `T(α)=T₀·exp(α·log(T₀⁻¹T₁))`, SLERP on SO(3) as `exp(τ·log(g₀⁻¹g₁))`. https://docs.resim.ai/open-core/transforms/using_liegroups/
- Cross-refs (raw citations carried through): [[lidar-visual-fusion-slam]], [[imu-vio-integration-reality]], [[camera-calibration-and-self-calibration]] §5 (observability/degeneracy), [[2d-lidar-slam]], [[visual-inertial-slam]].

## Related

- [[lidar-visual-fusion-slam]] — the coupling spectrum; why geometry stays on the LiDAR and we fuse loosely (the *spatial/architecture* companion to this *temporal* page)
- [[imu-vio-integration-reality]] — the two-clock, no-hardware-trigger, lagged-timestamp reality of this exact rig (the source of the hidden δt)
- [[camera-calibration-and-self-calibration]] — the *spatial* online-calibration survey; §5 observability/degeneracy that this page's "need rotation to excite δt" inherits
- [[2d-lidar-slam]] — the world-snapped 10 Hz LiDAR poses we treat as the trusted reference trajectory
- [[visual-inertial-slam]] — the IMU-bearing path (OKVIS2) that would replace this whole layer with a synced clock; we don't have it
- [[mighty]] — the only prior B-spline/continuous-time-trajectory mention in the wiki (planning, not estimation)
- [[home-tidy-drone-prototype]] — the parent build this serves
