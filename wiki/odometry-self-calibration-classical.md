# Classical Self-Calibrating Odometry for a Small Indoor Rover

**Summary.** Open-loop timed motion on this rig is already a usable odometry prior (1σ ≈ 1 cm / 0.5 m move, ±2.3° / quarter-turn) — the error that matters is *systematic* and lives in ~6–8 parameters (affine speed law, ramp loss, rotation rate + ramp offset, per-side gain mismatch, lateral strafe scale, rotation-induced lateral walk). Every classical method below (UMBmark → Antonelli LS → Censi → Kümmerle/g2o) reduces to the same thing: a *reference displacement* (external measurement, or LiDAR scan matching) minus the *model prediction* gives a residual that is **linear in the parameters** if you parametrize sensibly, so a recursive least-squares update with forgetting is the whole algorithm. The LiDAR scan-to-locked-map pose is the reference this rig should use; the α1–α4 noise model is fitted from the same residuals; degeneracy (corridor-like scans, the 25° blind sector) is the one caveat that needs an explicit gate.

Scope: **non-learned** methods only. Encoders (Hall ×4) are treated as the *next* sensor; everything is written so the same estimator absorbs them. No IMU by design ([[imu-vio-integration-reality]] for why).

## Related

[[learned-odometry-correction]] (the model-based rungs above this) · [[odometry-dataset-and-derived-gt]] (the data + labels this consumes) · [[land-rover-v1-rig]] · [[land-rover-v1-build-guide]] · [[2d-lidar-slam]] · [[slam-toolbox]] · [[camera-lidar-spatiotemporal-calibration]] · [[camera-calibration-and-self-calibration]] · [[lidar-multiscan-capture-recipe]] · [[home-tidy-drone-prototype]]

---

## 1. Parametric motion models — which few parameters matter

### 1.1 Open-loop timed model (what we have today, no encoders)

Per move, command = (duty vector `d`, duration `T`). Measured on the rig (R3): steady speed `v(d) = 0.103 + 0.342·d` m/s (affine, floor ≈ 0.16 m/s at `d = 0.18`), duty slewed at 1.5/s → ~0.25 s ramp costing −4…−6 cm per move; rotation 94 °/s at ±0.6 tank duty with −11° ramp offset; ±0.5° at 1/8 turn, ±2.3° at 1/4 turn; half-turns walk ~10 cm laterally.

The minimal model that reproduces every one of those numbers, per motion primitive:

| Primitive | Prediction (body frame) | Parameters | Maps to measured |
|---|---|---|---|
| Straight (fwd/back) | `Δx = (v0 + g·d)·T − c_v` ; `Δy = s_y·Δx` ; `Δθ = κ·Δx` | `v0, g` (affine law), `c_v` (ramp loss, m), `κ` (curvature from per-side gain mismatch, rad/m), `s_y` (mecanum lateral drift per metre) | `v0=0.103, g=0.342, c_v≈0.05`; `κ`,`s_y` unmeasured yet |
| Strafe (L/R) | `Δy = k_lat·[(v0 + g·d)·T − c_v]` ; `Δx = s_x·Δy` ; `Δθ = κ_lat·Δy` | `k_lat` (lateral scale, mecanum strafes *less* than the wheel model says), `s_x`, `κ_lat` | unmeasured; expect `k_lat` 0.8–0.9 |
| Spin in place | `Δθ = (ω0 + h·d)·T − c_ω` ; `(Δx,Δy) = (a_x, a_y)·|Δθ|` | `ω0, h` (affine rate), `c_ω` (ramp offset), `(a_x,a_y)` (systematic walk per rad) | `94°/s @0.6`, `c_ω=11°`; walk 10 cm / half-turn → `|a| ≈ 3 cm/rad` if systematic |

That is 8 parameters for straight+spin, 11 with strafe. `κ` and `s_y` are the open-loop analogues of UMBmark's `E_d` (wheel-diameter ratio → curved path) and `E_b` (wheelbase → rotation scale) [Borenstein96]; `k_lat` is the FTC/Road Runner `LATERAL_MULTIPLIER`, a shipping practice for mecanum drive-encoder localization (tune until `StrafeTest` distance matches) [RoadRunner]. The affine floor (`v0 > 0`) is stick-slip/deadband of brushed gearmotors under PWM; open-loop PWM speed tracks supply voltage, so `v0, g, ω0, h` drift with battery sag [Wevolver-PWM] — treat them as slowly time-varying (forgetting factor), not constants.

*(synthesis)* Why not model ramp as a time constant `τ` instead of a distance `c_v`? Because `c_v = v(d)·τ/2` is what the residual sees; keeping `c_v` as a free parameter keeps the model **linear in the unknowns** given regressors `(T, d·T, −1)`. Same for `c_ω`.

### 1.2 Encoder odometry (Hall A-channel ×4, planned)

Differential/skid form: `Δ = J · [Δθ_L, Δθ_R]ᵀ`. The classical 3-parameter set is `(r_L, r_R, b)` or, equivalently, Censi's `J11, J12, J21, J22` (velocity Jacobian); only the ratios `r_L/b`, `r_R/b` are directly observable from rotation, so `r` and `b` are strongly correlated [Censi13 §VI]. Skid-steer extensions add slip: the *extended differential drive* has per-side slip `α_l, α_r ∈ [0,1]` plus ICR coordinates `(x_v, y_l, y_r)` (5 params; symmetric variant `α, b̂` = 2 params) [Mandow07, Baril20]; the *full linear* model is an unconstrained 3×2 `J` (6 params) and was the most accurate of four skid-steer models on both concrete and snow, with the 2-parameter symmetric model close behind for heading and less prone to overfitting [Baril20 Table I]. Okawara et al. put the 6-parameter full-linear `J` as a state node in a factor graph and calibrate it online against LiDAR (demoed, code released) [Okawara24].

Mecanum (X-mount) inverse kinematics is 4×3: `ω_i = (1/r)[v_x ∓ v_y ∓ (l_x+l_y)·ω]`; forward odometry is the pseudo-inverse. Han et al. identify the roller sliding as the dominant mecanum position-error source and reduce a diagonal-move return error from 1.52 m to 0.03 m with a 3-parameter slip/friction correction (demoed, one platform) [Han10]. Practical reduced set for us: 4 per-wheel gains, 1 effective `(l_x+l_y)`, 1 lateral scale `k_lat` → 6 parameters, again linear in the unknowns per primitive.

### 1.3 Surface classes

Kümmerle et al. found the *same* wheel radii on carpet and concrete but a clearly higher standard deviation of the odometry-edge residual on carpet — i.e. surface changes the **noise** (α's) before it changes the **means**, and that noise can be stored per map region [Kuemmerle11 §IV-B]. Baril's snow-vs-concrete parameters differ substantially (`α` 0.94 → 0.86; `b̂` 4.46 → 3.08 m) because the skid mechanism itself changes [Baril20]. For a single hard-floor room: one parameter set, per-region α's.

---

## 2. Classical calibration procedures

| Method | Reference | Parameters | Data needed | Status |
|---|---|---|---|---|
| **UMBmark** bidirectional square path | [Borenstein96] | `E_d = D_R/D_L`, `E_b = b_actual/b_nominal` | 4×4 m square, stop after each 4 m leg, 4 on-spot 90° turns, **5 runs CW + 5 CCW**, measure return position externally | shipping (textbook) |
| Least-squares odometry calibration | [Antonelli05], [Antonelli07] | 3 params linear in `(r_L, r_R, b)` combos | arbitrary paths, external final-pose measurement per run, batch LS | demoed |
| Simultaneous odometry + sensor-pose calibration | [Censi13] | `r_L, r_R, b` + laser `(ℓ_x, ℓ_y, ℓ_θ)` | scan-to-scan matching only, **no external truth**; ~3500 scan pairs per subset; canonical inputs `±(1,1), ±(1,−1), ±(1,0), ±(0,1)` | demoed, code released |
| Simultaneous calibration, localization, mapping (g2o hyper-graph) | [Kuemmerle11], [Kuemmerle12] | `r_L, r_R, b` + laser pose as graph nodes | normal SLAM data; **sliding window of 50 most recent odometry edges** for non-stationary params | demoed on 3 platforms |
| EKF augmented-state self-calibration | [Martinelli07] | systematic + non-systematic odometry error params in the filter state | localization run against a known map | demoed |
| Online incremental ML self-calibration | [Roy99] | translational + rotational systematic error terms (abstract-level) | robot's own sensors during operation; ≥10× systematic-error improvement claimed | demoed (1999) |
| Fast systematic + stochastic calibration | [Kelly04] | systematic params + noise (stochastic) params | single known ground-truth point, path-dependence exploited | demoed |
| OptiOdom (any steering geometry) | [Sousa22] | kinematic params, iRprop− optimizer | position-only truth (OptiTrack), suggested path, 4 robots | demoed, code released |

**UMBmark formulae** (what everything else generalizes) [Borenstein96 §4]: from the CW/CCW return-error centroids `x_cg,cw`, `x_cg,ccw`, side `L`:
`β = (x_cg,cw − x_cg,ccw)/(−4L)` (deg) → `R = (L/2)/sin(β/2)` → `E_d = (R + b/2)/(R − b/2)`; `α = (x_cg,cw + x_cg,ccw)/(−4L)` → `E_b = 90°/(90° − α)`; corrections `c_L = 2/(E_d+1)`, `c_R = 2/(1/E_d + 1)`, `b_new = E_b·b`. Reported 317 mm → 21 mm (15×) on their TRC LabMate, eight experiments, all runs used. The two error *types* are the important idea: **Type A** (wheelbase) changes total rotation the same way CW and CCW; **Type B** (unequal diameters) curves straights and flips sign with direction. Bidirectional paths separate them; a unidirectional square does not.

**Censi's structure** [Censi13 §V]: (1) estimate `J21, J22` (the rotation row) by linear LS on the heading residuals only — closed form; (2) given those, solve `J11, J12` and the sensor pose from the translation residuals; (3) repeat N times with outlier rejection (drop the largest-residual fraction each pass). Accuracy reached the Cramér–Rao bound; disjoint data subsets agreed within the CRB error bars. **Observability requirement**: any trajectory that "sufficiently excites" the parameters — straight-only or constant-curvature-only is degenerate; both wheel-only motions and turns in place are needed. Kümmerle states the same: straight-line-only or circle-only trajectories cannot observe the laser pose [Kuemmerle11 §III-A].

**Kümmerle's online variant** [Kuemmerle11]: odometry edge error `e_i = (x_{i+1} ⊖ x_i) ⊖ K(u_i, k)` with `k` a graph node; marginal covariance of `k` from the Cholesky factor of `H` monitors convergence; parameters are re-estimated on a sliding window so wheel radii tracked a 40 kg load being added/removed (`r_r` 0.1251 → 0.1231 m, a change that "has a crucial effect" on the trajectory). This is the pattern to copy: *the same factor is both the motion constraint and the calibrator*.

---

## 3. LiDAR-scan-matching-supervised calibration (no external truth)

**Reference displacement.** PL-ICP (point-to-line, closed-form step, quadratic convergence) is the standard 2D matcher; Censi's CSM is the reference implementation [Censi08]. Its covariance is available in closed form from the error-function Hessian and the measurement covariance, accurate enough for online use [Censi07]. Censi's Khepera experiments rated scan matching at ~1 mm and tenths of a degree for 5–10 cm displacements with a Hokuyo URG (3 mm 1σ ranges) [Censi13 §VI-A] — our C1 has 0.10 cm single-scan wall-fit RMS, so expect the same order per move.

**Scan-to-map beats scan-to-scan for this rig.** With the locked room map ([[lidar-floorplan-extraction]] products) the reference pose is absolute, so calibration residuals do not accumulate matcher drift, and stop-and-scan (scan at rest) removes motion distortion entirely. Use scan-to-scan only during the *first* mapping pass.

**Degeneracy caveats (binding).**
- Corridor-like or single-wall scans are unobservable along the wall; scan matchers then "shorten corridors" and a large search window makes it worse — Kümmerle's Fig. 1 motivation [Kuemmerle11]. Gate on the minimum eigenvalue of the matcher Hessian (degeneracy factor) and update only the well-conditioned directions [Zhang16]; Okawara freezes the kinematic-parameter node (fixation factor, covariance 1e-10) while the point cloud is degenerate and calibrates only in feature-rich stretches [Okawara24 §III-F].
- The 25° self-occlusion blind sector: fine in a room (≥2 non-parallel walls remain visible) but check the Hessian, do not assume.
- Reference covariance `Σ_ref` from [Censi07] must weight the residual; an unweighted fit lets one degenerate move dominate.
- Sensor bias/drift: Censi observed URG range readings drifting 20 mm over 5 min (battery/temperature) [Censi13 §VI-A]; the C1 has no such report here but the wall-fit RMS is the check.

**Per-episode fit** = Antonelli's batch LS with the matcher as the "external" measurement; **online fit** = the same in recursive form with forgetting (Kümmerle's sliding window is the batch equivalent). Both are ~100 lines once the model is linear in its parameters (§1.1).

---

## 4. Fusing the timed/odometry prior with scan matching

**EKF/UKF vs pose graph.** Martinelli's EKF puts the odometry parameters in the state alongside pose [Martinelli07]; Censi argues filtering "with such large and heterogeneous state" raises observability/linearization issues and prefers batch ML with closed-form solutions [Censi13 §I]. Pose graph (g2o/GTSAM) with a parameter node is the modern default [Kuemmerle11, Okawara24]. For a stop-and-scan single room the honest answer is: neither is needed for *localization* (scan-to-locked-map is near-GT); the fusion question is only (a) the prior for the matcher's initial guess and (b) fallback when the matcher is degenerate. A 3-state EKF (pose) with the timed model as process and the matcher as measurement is enough; run the parameter RLS **outside** the filter on accepted residuals to avoid Censi's coupling problem.

**Odometry factor covariance from Thrun's sample motion model** [Thrun05 §5.4, Table 5.6]. Decompose each move into `δ_rot1, δ_trans, δ_rot2`; noise variances
`Var(rot1) = α1·δ_rot1² + α2·δ_trans²`, `Var(trans) = α3·δ_trans² + α4·(δ_rot1² + δ_rot2²)`, `Var(rot2) = α1·δ_rot2² + α2·δ_trans²`.
(MRPT and MATLAB `odometryMotionModel` ship this exact parametrization [MRPT-motion].)

**Fitting α from residuals.** After the systematic model is fitted, the residual `r = Δ_ref − f(u; θ̂)` is zero-mean; regress squared components on squared commanded quantities with non-negative LS:
`r_trans² ≈ α3·δ_trans² + α4·(δ_rot1²+δ_rot2²)`, `r_rot² ≈ α1·δ_rot² + α2·δ_trans²`.
This is Kelly's "stochastic calibration" done with scan matching as truth [Kelly04]. Seeded from R3 numbers: straight 1σ 1 cm on 0.5 m → `α3 ≈ (0.01/0.5)² = 4e-4`; quarter-turn ±2.3° (≈1σ 0.04 rad on 1.57 rad) → `α1 ≈ 6.5e-4`; half-turn 10 cm walk, if it is *not* systematic, → `α4 ≈ 0.1²/π² ≈ 1e-3 m²/rad²`; `α2` (heading noise from translation) unmeasured, start 1e-4. Re-fit per surface region (Kümmerle's finding, §1.3).

---

## 5. Data needs and failure modes

**How much data (from the papers).** UMBmark: 10 runs × 4 legs (40 straights, 40 turns) at 4 m scale [Borenstein96]. Censi: ~3500 scan pairs per data subset, closed trajectories built from the four canonical inputs so it runs unattended in a confined space [Censi13 §VI]. Kümmerle: 50-edge sliding window tracks a step change [Kuemmerle11]. Baril: split the truth trajectory by a *spatial* horizon (not temporal — removes zero-command outliers), sum of Mahalanobis end-pose errors as loss [Baril20 §IV]. *(synthesis)* With ~8 linear parameters and 3 residual components per move, ~20 moves per primitive class (straight ±, spin ±, strafe ±) is a well-conditioned per-episode fit; ~60–80 short moves total, i.e. one mapping episode. Include **both signs** of every primitive (Type A/B separation) and a range of `d` and `T` (else `v0`/`g` and `c_v`/`g` are collinear).

**Failure modes.**
- *Battery sag*: open-loop speed ∝ supply → `v0, g, ω0, h` drift within an episode; forgetting factor λ≈0.95–0.98 plus battery-voltage regressor if the ESP32 reports it [Wevolver-PWM].
- *Surface change*: means may stay, noise rises (carpet) [Kuemmerle11]; skid parameters shift on low-μ surfaces [Baril20]; slippage detection needs sensor redundancy the differential-drive literature gets from gyros [Parlangeli24] — we get it from the scan-match residual jumping outside `Σ_ref + Σ_α`.
- *Mecanum lateral slip*: strafe under-travel and diagonal drift are the dominant errors [Han10]; keep `k_lat, s_x, s_y` free and expect them to be the least stable parameters.
- *Ramp/latency*: `c_v, c_ω` absorb the 0.25 s slew only for moves ≫ 0.25 s; sub-0.3 s moves are nonlinear in `T` — forbid or model separately.
- *Affine floor*: no continuous speed below ~0.16 m/s; "slow" means shorter `T`, not lower `d`.
- *Degenerate reference* (§3): freeze the parameter update, keep the pose filter running.
- *Non-systematic rotation walk*: if `(a_x,a_y)` do not converge across episodes the 10 cm walk is noise → move it into `α4` and stop modelling it.

---

## 6. Concrete parameter set and update rules (≈200 lines of Python)

```python
# state per primitive class p ∈ {fwd, strafe, spin}: theta_p (linear params), P_p (RLS covariance)
# fwd:    Δx = [T, d*T, -1] @ [v0, g, c_v];        Δy = s_y*Δx;   Δθ = κ*Δx
# strafe: Δy = k_lat*([T, d*T, -1] @ [v0, g, c_v]); Δx = s_x*Δy;   Δθ = κ_lat*Δy
# spin:   Δθ = [T, d*T, -1] @ [ω0, h, c_ω];         (Δx,Δy) = (a_x,a_y)*|Δθ|
# init from R3: v0=0.103 g=0.342 c_v=0.05 ; ω0,h from 94°/s@0.6 (h≈ω/0.6 if ω0≈0) c_ω=0.19 rad
# α = [α1,α2,α3,α4] = [6.5e-4, 1e-4, 4e-4, 1e-3]

def rls_update(theta, P, phi, y, sigma2, lam=0.97):      # one scalar residual channel
    k = P @ phi / (lam*sigma2 + phi @ P @ phi)
    theta = theta + k * (y - phi @ theta)
    P = (P - np.outer(k, phi @ P)) / lam
    return theta, P

def after_move(cmd, ref_delta, ref_cov, hessian_min_eig):
    # ref_delta = scan-to-locked-map pose change (body frame); ref_cov from Censi-07 closed form
    if hessian_min_eig < EIG_MIN:            # Zhang-16 / Okawara-24 gate: degenerate scan → no update
        return
    d, T = cmd.duty, cmd.duration
    if T < 0.3: return                        # ramp-dominated, nonlinear in T
    phi = np.array([T, d*T, -1.0])
    if cmd.kind == "fwd":
        theta_v, P_v = rls_update(theta_v, P_v, phi, ref_delta.x, ref_cov[0,0] + a3*ref_delta.x**2)
        dx = phi @ theta_v
        kappa, s_y = rls_update_scalar(kappa, ref_delta.th, dx), rls_update_scalar(s_y, ref_delta.y, dx)
    elif cmd.kind == "spin":
        theta_w, P_w = rls_update(theta_w, P_w, phi, ref_delta.th, ref_cov[2,2] + a1*ref_delta.th**2)
        ...  # (a_x, a_y) as scalar RLS on |Δθ|; drop if P stays large after an episode
    # residuals after the systematic update feed the α fit (batch, end of episode):
    R.append((ref_delta - predict(cmd), decompose(cmd)))   # (r_rot1, r_trans, r_rot2), (δ_rot1, δ_trans, δ_rot2)

def fit_alpha(R):   # non-negative LS, Thrun Table 5.6 structure
    A_t = [[dt**2, dr1**2 + dr2**2] for ...]; b_t = [r_t**2 ...]      → α3, α4
    A_r = [[dr**2, dt**2] for ...];            b_r = [r_r**2 ...]      → α1, α2
    return scipy.optimize.nnls(A_t, b_t)[0], scipy.optimize.nnls(A_r, b_r)[0]
```

Outlier handling: Censi's loop — after a batch fit, drop the top 5–10 % residuals and refit, 2–3 passes [Censi13 §V-C]; online, reject any residual with Mahalanobis distance > 3 under `Σ_ref + Σ_α` (that rejection is also the slip detector). Convergence monitor: diagonal of `P_p` (Kümmerle's marginal covariance) — stop updating a channel when it drops below its target and restart when residual variance jumps.

**Encoder upgrade path.** Replace regressor `phi = [T, d*T, −1]` with encoder-integrated `[Δθ_L, Δθ_R]` (or the four wheel counts) and the *same* RLS estimates `J`'s rows (Censi's step 1 = heading row first). Keep the timed model as a sanity prior; the 6-parameter mecanum set of §1.2 is the ceiling before overfitting — Baril's 6-parameter full-linear model was best but "can suffer from overfitting", the 2-parameter symmetric model nearly as good [Baril20].

---

## Recommendation for this rig

1. **Now (no encoders)**: implement §6 as-is with scan-to-locked-map as reference during stop-and-scan mapping. Log `(cmd, ref_delta, ref_cov, min_eig)` per move; fit batch per episode first (Antonelli-style LS), switch on RLS only once two episodes agree within `P` (Censi's subset-consistency test).
2. **Calibration episode**: ~60–80 short moves in the room, forward *and* backward, spin *both* directions at 1/8–1/4 turns, strafe both ways, `d ∈ {0.2, 0.4, 0.6}`, `T ∈ {0.5, 1, 2} s`. Return to start (Censi's closed loop) so the same map region is used — bidirectionality is what separates the UMBmark Type A/B terms.
3. **Model**: 8 linear parameters (`v0, g, c_v, κ, s_y, ω0, h, c_ω`) + 3 strafe (`k_lat, s_x, κ_lat`) + optional walk `(a_x, a_y)`; α1–α4 refit per episode from residuals. Do not add slip/ICR parameters until encoders exist.
4. **Gates**: no update when `T < 0.3 s`, when matcher Hessian min-eig is below threshold, or when the residual exceeds 3σ (log as slip event). Forgetting λ≈0.97 to track battery sag; add measured battery voltage as a regressor if the ESP32 can report it.
5. **Validation (binding per project standards)**: leave-one-episode-out prediction error on held-out moves, not in-sample residuals; report both the systematic fit and the fitted α's; cross-check `κ` and `k_lat` against a physical tape measurement once.
6. **When encoders arrive**: same estimator, regressors swapped; expected gain is mainly in *within-move* prediction (matcher initial guess) and in surviving degenerate scans, not in the stop-and-scan accuracy which the map already supplies.

## Sources

- [Borenstein96] Borenstein & Feng, "Measurement and Correction of Systematic Odometry Errors in Mobile Robots", IEEE T-RA 12(6):869–880, 1996. PDF: https://johnloomis.org/ece445/topics/odometry/borenstein/paper58.pdf (UMBmark procedure §3.3, formulae §4, results Table I)
- [Antonelli05] Antonelli, Chiaverini, Fusco, "A calibration method for odometry of mobile robots based on the least-squares technique: theory and experimental validation", IEEE T-RO 21(5):994–1004, 2005. https://ui.adsabs.harvard.edu/abs/2005ITRob..21..994A
- [Antonelli07] Antonelli & Chiaverini, "Linear estimation of the physical odometric parameters for differential-drive mobile robots", Autonomous Robots 23(1):59–68, 2007. https://link.springer.com/article/10.1007/s10514-007-9030-2
- [Censi13] Censi, Franchi, Marchionni, Oriolo, "Simultaneous calibration of odometry and sensor parameters for mobile robots", IEEE T-RO 29(2):475–492, 2013, doi:10.1109/TRO.2012.2226380. PDF: https://censi.science/pub/research/2012-joint_calibration.pdf ; code http://purl.org/censi/2011/calibration
- [Censi08] Censi, "An ICP variant using a point-to-line metric", ICRA 2008. https://censi.science/pub/research/2008-icra-plicp.pdf ; CSM https://censi.science/software/csm/
- [Censi07] Censi, "An accurate closed-form estimate of ICP's covariance", ICRA 2007, pp. 3167–3172. https://censi.science/research/robot-perception/icpcov/
- [Kuemmerle11] Kümmerle, Grisetti, Burgard, "Simultaneous Calibration, Localization, and Mapping", IROS 2011. PDF: http://ais.informatik.uni-freiburg.de/publications/papers/kuemmerle11iros.pdf
- [Kuemmerle12] Kümmerle, Grisetti, Burgard, "Simultaneous Parameter Calibration, Localization, and Mapping", Advanced Robotics 26(17):2021–2041, 2012. https://www.researchgate.net/publication/221067624
- [Martinelli07] Martinelli, Tomatis, Siegwart, "Simultaneous localization and odometry self calibration for mobile robot", Autonomous Robots 22(1):75–85, 2007. https://link.springer.com/article/10.1007/s10514-006-9006-7
- [Roy99] Roy & Thrun, "Online self-calibration for mobile robots", ICRA 1999, vol. 3, pp. 2292–2297. https://www.semanticscholar.org/paper/07e97d4efacaa1e2422f2d8d034f4a433a55f9e0 (abstract-level only)
- [Kelly04] Kelly, "Fast and Easy Systematic and Stochastic Odometry Calibration", IROS 2004, vol. 4, pp. 3188–3194. https://www.ri.cmu.edu/publications/fast-and-easy-systematic-and-stochastic-odometry-calibration/
- [Thrun05] Thrun, Burgard, Fox, *Probabilistic Robotics*, MIT Press 2005, ch. 5 (odometry motion model, Table 5.6). https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf
- [MRPT-motion] MRPT "Probabilistic motion models" (Thrun α parametrization as shipped). https://www.mrpt.org/tutorials/programming/odometry-and-motion-models/probabilistic_motion_models/
- [Mandow07] Mandow, Martínez et al., "Experimental kinematics for wheeled skid-steer mobile robots", IROS 2007, pp. 1222–1227. https://ieeexplore.ieee.org/document/4399139
- [Pentzer14] Pentzer, Brennan, Reichard, "Model-based prediction of skid-steer robot kinematics using online estimation of track instantaneous centers of rotation", J. Field Robotics 2014, doi:10.1002/rob.21509
- [Baril20] Baril et al., "Evaluation of Skid-Steering Kinematic Models for Subarctic Environments", CRV 2020, arXiv:2004.05131. PDF: https://norlab.ulaval.ca/pdf/Baril2020.pdf
- [Okawara24] Okawara et al., "Tightly-Coupled LiDAR-IMU-Wheel Odometry with Online Calibration of a Kinematic Model for Skid-Steering Robots", arXiv:2404.02515 (IEEE Access). https://arxiv.org/abs/2404.02515
- [Zhang16] Zhang, Kaess, Singh, "On degeneracy of optimization-based state estimation problems", ICRA 2016, pp. 809–816, doi:10.1109/ICRA.2016.7487211
- [Han10] Han, Kim, Lee, "The sources of position errors of omni-directional mobile robot with Mecanum wheel", IEEE SMC 2010, pp. 581–586. https://www.semanticscholar.org/paper/4a015a84c2a76d60085876cfcee6145ab3bbb85e
- [Sousa20] Sousa, Petry, Moreira, "Evolution of Odometry Calibration Methods for Ground Mobile Robots", ICARSC 2020, pp. 294–299. https://ieeexplore.ieee.org/document/9096154/
- [Sousa22] Sousa, Petry, Costa, Moreira, "OptiOdom: a Generic Approach for Odometry Calibration of Wheeled Mobile Robots", J. Intell. Robot. Syst. 2022, doi:10.1007/s10846-022-01630-3
- [Parlangeli24] Parlangeli, "Online Odometry Calibration for Differential Drive Mobile Robots in Low Traction Conditions with Slippage", Robotics 13(1):7, 2024. https://iris.unisalento.it/retrieve/da2fee85-7092-4f22-a94c-af6f4d9f3530/robotics-13-00007-v2%20(1).pdf
- [RoadRunner] Road Runner (FTC) tuning docs — `LATERAL_MULTIPLIER` / StrafeTest for mecanum drive-encoder localization. https://learnroadrunner.com/straight-test.html , https://rr.brott.dev/docs/v1-0/tuning/
- [Wevolver-PWM] "DC Motor Speed Control: PWM Techniques for Brushed and BLDC Drives" (open-loop PWM does not compensate supply variation). https://www.wevolver.com/article/dc-motor-speed-control-pwm-techniques-for-brushed-and-bldc-drives
