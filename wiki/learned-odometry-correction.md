# Learned Odometry Correction — Per-Episode Updatable Models for an Open-Loop Mecanum Rover

Residual learning (`Δ_true = f_kin(u) + g(u, ctx)`) on top of the measured affine timed model is the right frame for this rig: the fixed model is already 1σ ≈ 1 cm on 0.5 m, so the corrector only has to explain the *regime-dependent* part (battery sag, ramp, surface, lateral walk), which is small-data-friendly and keeps the failure mode benign (g → 0 is the fixed model). A rig-calibrated toy simulation says a 5–7-feature ridge corrector overtakes the fixed model after ~20–40 labelled moves **if** the regime variables (volts, surface proxy) are observed features, and barely at all if they aren't — features matter more than model class at this scale. GP / small-NN correctors (Brossard & Bonnabel 2019, Trivedi et al. ICRA 2024, Navone et al. 2023) become worth it at ~10²–10³ labelled increments and buy a per-move covariance; validate everything with leave-one-episode-out, never random-row CV.

## Problem statement for this rig

- Actuation: 4× brushed DC gearmotors on X-mounted mecanum wheels, open-loop PWM duty from an ESP32 (per-side today, per-wheel possible). No encoders yet (Hall A-channel ×4 planned), no IMU.
- Measured timed model ([[land-rover-v1-rig]]): steady speed `v ≈ 0.103 + 0.342·duty` m/s (affine), ~0.25 s ramp costing 4–6 cm per move, repeatability 1σ ≈ 1 cm on 0.5 m (4 %); rotation 94 °/s at ±0.6 tank duty, −11° ramp offset, ±2.3° at 90°, half-turns walk ~10 cm laterally.
- Labels: after the room is mapped ([[map-then-navigate]], [[anchor-map-protocol]]) each move gets a (Δx, Δy, Δθ) label from localizing the at-rest LiDAR scans against the locked map (~cm, ~1°), plus per-0.1 s scan-to-scan increments during motion (10 Hz RPLIDAR C1, 0.10 cm single-scan wall RMS — see [[2d-lidar-slam]]).
- Context features available now: commanded duties (L/R or per wheel), duration, ramp profile, start/stop timestamps, pack voltage (3S LiPo via servo bus), lift/tilt state. Later: encoder ticks. Cheap derived features: scan-to-scan residual during motion (vibration/surface proxy), time-since-episode-start (thermal).
- What the corrector must output: a mean correction **and** a covariance usable as the motion prior for scan matching ([[slam-toolbox]] and the [[measurement-selection-uncertainty]] page cover the consumer side).

## 1. Residual-learning framing — why not end-to-end

Learn `g(u, ctx) = Δ_label − f_kin(u)` rather than `Δ = h(u, ctx)`.

- Data efficiency: the residual has ~10× smaller magnitude and is smooth in the regime variables, so a linear/GP model fits it with tens, not thousands, of samples. Brossard & Bonnabel train Gaussian processes *on the residual between the original model and the ground truth* for wheel-odometry + gyro propagation and show the corrected models and EKF beat their originals on NCLT (Segway) and KAIST (car) *(demoed; ICRA 2019, code released)*. Trivedi et al. augment a kinematic skid-steer model with two GPs `g_v, g_ω` predicting the velocity disturbance, cutting normalized position error from 17.6–21.1 % (extended-differential-drive baseline) to 5.7–10.9 % across asphalt/grass/tile *(demoed on Jackal; ICRA 2024)*.
- Safe failure: with ridge/GP shrinkage, an unseen regime collapses g → 0 and you are back on the measured affine model; an end-to-end net extrapolates arbitrarily.
- Interpretability: the fitted coefficients (per-volt gain, per-surface ramp loss) are physics you can sanity-check and later fold back into the ESP32 feed-forward.
- The kinematic part for mecanum is the standard inverse-Jacobian (`v_x, v_y, ω` from four wheel speeds, geometry `l_x + l_y`); with open-loop duty the "wheel speed" is `v(duty)` from the affine fit. Known mecanum systematic errors (roller slip, lateral scale ≠ longitudinal scale, discontinuous roller contact) are exactly the low-dimensional residuals this frame targets — a GRU drift-compensator for a holonomic mecanum platform (Intelligent Service Robotics 2022) uses chassis accelerometer + wheel encoders as features for exactly this *(demoed)*.

End-to-end learned odometry from raw LiDAR (DeepLO, DeepPCO, the Oregon State CNN-on-projected-scans work) is the comparison class, not the target: those need KITTI-scale training and a GPU and are outperformed indoors by classical scan matching, which this rig already has at 0.1 cm wall RMS *(demoed, outdoor 3D LiDAR)*. See [[learned-slam]] for that landscape.

## 2. Model classes, data needs, literature sample sizes

| Class | Inputs (this rig) | Output | Data to beat fixed model | Covariance | Update cost | Status |
|---|---|---|---|---|---|---|
| Per-episode affine refit (2 params/axis) | duty·T, T | Δ mean | ~10–20 moves/episode | residual variance (scalar) | closed form | shipping (any lab) |
| Ridge / Bayesian linear on hand features (5–10 feats) | + volts, ramp, surface proxy, interactions | Δ mean | ~20–40 moves across ≥3 regimes (toy sim, §7) | posterior predictive (analytic) | RLS O(d²) per move | shipping |
| GP on residual (SE/Matérn kernel, sparse) | 4–8 dim | Δ mean + σ | ~10²–10³ increments; Trivedi used 500 GMM-selected inducing points | native | streaming sparse GP (Bui et al. 2017) | demoed |
| Small 1-D CNN / attention on a window | N-step window of duties (+ encoders/IMU later) | Δ mean (σ if trained for it) | 10⁴–10⁵ samples: Navone 156,579 samples @ 25 Hz ≈ 104 min; AI-IMU 6,210-param CNN, 400 epochs, batches of 9× 1-min windows | learned noise scaling (AI-IMU) | mini-batch SGD, replay | demoed |
| Recurrent (GRU/LSTM) | same, sequential | Δ mean | same order as CNN | usually none | same | demoed (mecanum GRU) |
| Learned-noise-only (AI-IMU / RINS-W pattern) | window of IMU/encoders | **Q/R scaling for a KF**, not Δ | KITTI-scale sequences | by construction | SGD | demoed (car) |

Notes per class:

- **Linear/ridge.** The rig has one clean physical prior per feature: speed ∝ supply voltage at fixed duty (brushed DC, open loop), ramp loss ∝ (1 − duty-ish), lateral walk ∝ rotation angle. Ridge on `[1, duty·T, T, ΔV, ΔV·duty·T, surf, surf·duty·T]` per output axis is the whole model. Systematic odometry calibration by least squares on kinematic parameters (wheel radii, track — the UMBmark lineage, Antonelli et al.) is the same idea with fewer features; RLS with a forgetting factor is the standard online form (Ljung, *System Identification*).
- **GP.** Brossard & Bonnabel (ICRA 2019) — GP on residuals of the wheel/gyro propagation model, EKF built on the learned model; NCLT + KAIST *(demoed)*. Trivedi et al. (ICRA 2024) — SE kernel, 500-centre sparse set, inputs `(v, ω, v_ref, ω_ref)`, outputs `(g_v, g_ω)`, uncertainty pushed through the kinematics by sigma-point transform to yield a full pose covariance *(demoed)*. Skid-steer MPC with an *online sparse GP* velocity model (Ostafew-style, Wang et al. IFAC 2017) is the continual-update precedent *(demoed)*. Streaming sparse GP (Bui, Nguyen & Turner, NeurIPS 2017) gives principled sequential posterior + hyperparameter updates without catastrophic forgetting; GP-Localize shows constant time/memory per step online sparse GP for robot localization *(demoed)*.
- **Small NN.** AI-IMU dead-reckoning: a 2-layer 1-D temporal CNN (kernel 5, 32 channels, dilation 1 and 3 → window N = 15, 6,210 params) outputs *covariance scalings* for zero-lateral/zero-vertical-velocity pseudo-measurements inside an IEKF; trained by backprop through the filter on relative translation error, Adam 1e-4, dropout 0.5, 400 epochs, leave-one-sequence-out; 1.10 % translational error on KITTI *(demoed; IEEE T-IV 2020)*. RINS-W: RNN detects zero-velocity / no-lateral-slip situations as pseudo-measurements; 20 m final error over 21 km with a 10 °/h gyro *(demoed; IROS 2019)*. Navone et al. (2023): attention-based 1-D conv on a window of (wheel speeds, accel, gyro) → Δ pose, trained **online from a VIO (T265) teacher** in mini-batches of 32 with MAE loss on a Jackal; online training matched batch training and beat the EKF baseline (e.g. type-A round trajectories: m-ATE 0.69 m EKF → 0.29 m online) *(demoed)*. SlipOdometryNet: 176k-param 1-D residual CNN on encoders + commanded velocities, no IMU, 51–94 % ATE reduction vs kinematic baseline across four friction levels — but **Gazebo only** *(claimed)*. WING (2024): 1-D ResNet de-bias nets for IMU and wheel-encoder with output uncertainty, ground-manifold constraint; KAIST/NCLT *(demoed, car scale)*.
- **Learned kinematics for skid-steer** (closest analogue to a slipping mecanum): Okawara et al. put the full-linear wheel-odometry kinematic matrix *as states in the factor graph* with online covariance estimation (IEEE Access 2024), then replaced it with a neural kinematic model trained online on the same factor graph (RAS 2025) *(demoed, open source)*. Relevant pattern: the corrector's parameters are just more state, estimated jointly with the trajectory by the same LiDAR constraints that produce our labels.

## 3. Continual / per-episode updating

- **Closed form first.** Bayesian linear regression with Gaussian prior on `w` (Bishop PRML §3.3): posterior `Σ⁻¹ = Σ₀⁻¹ + XᵀX/σ², μ = Σ(Σ₀⁻¹μ₀ + Xᵀy/σ²)`; the prior mean `μ₀ = 0` *is* the fixed affine model. Per-episode update = one rank-n update. Add a forgetting factor λ ∈ [0.95, 0.995] on the information matrix (RLS-λ) to track slow drift (motor wear, battery aging) without discarding the prior.
- **Regime-aware, not row-aware.** Treat each episode (one battery charge, one floor) as a block. Keep one small replay buffer per regime (e.g. 30 moves) and refit on the union; this is the linear/GP equivalent of experience replay and prevents a single 200-move carpet episode from over-writing the hardwood coefficients. For an NN the same buffer feeds mini-batches; EWC (Kirkpatrick et al. PNAS 2017) is overkill at this parameter count.
- **GP updates.** Streaming sparse GP (Bui et al.) updates inducing-point posterior and hyperparameters sequentially; simpler: refit an exact GP on the replay union (≤ 2k points is milliseconds on a laptop) at episode end.
- **Hyperparameter and outlier hygiene.** Labels come from scan matching; gate them with the match's own covariance (Censi 2007 closed-form ICP covariance) and reject moves whose scan-to-map residual exceeds a threshold before they enter the buffer. Use MAE/Huber loss for anything iterative (Navone's choice for exactly this reason).
- **Honest validation (this project has been burned by random-CV optimism — see the project memory note `dont-overstate-accuracy-honest-validation` and [[measurement-selection-uncertainty]]).** Random row-wise CV leaks episode-level effects (voltage, floor) into the test fold and reports the *within-regime* error, which is the number the fixed model already achieves. Use: (a) leave-one-episode-out for "does it transfer to the next run?"; (b) forward-chaining (train on episodes 1..k, test on k+1) for "does the online update help?"; (c) leave-one-regime-out (all carpet episodes held out) for "does it extrapolate?" — expect it not to, and report that. Roberts et al. (Ecography 2017) is the canonical reference: block CV wherever dependence structure exists, *even if the model appears to account for it*. Report the fixed-affine baseline on every fold; a corrector that wins only on random CV is a negative result.

## 4. Uncertainty output — the motion prior for scan matching

The consumer wants `N(Δ̂, Σ)` per move (and per 0.1 s increment) in the robot frame.

- **Ridge/Bayesian-linear:** `Σ = σ²_res + xᵀ Σ_w x` per axis, plus a cross-axis term for the rotation→lateral walk (fit `Δy` on `Δθ` explicitly). Inflate `σ²_res` by the leave-one-episode-out ratio, not the in-sample ratio.
- **GP:** predictive variance directly; propagate to pose via sigma points as Trivedi et al. do, or linearize.
- **NN:** either train a heteroscedastic head (NLL loss) or learn a covariance scaling for a KF (AI-IMU pattern). At our data scale prefer the former only with ≥10⁴ samples; otherwise fall back to a Thrun-style `α₁..α₄` odometry motion model (Probabilistic Robotics ch. 5) whose α's are *fitted from the same residual buffer* — that is a 4-parameter learned covariance that any particle filter or [[slam-toolbox]] already consumes.
- Calibration check: fraction of labels inside the 1σ/2σ ellipse per held-out episode should be ≈ 0.39/0.86 (2-D); if the corrector is over-confident the scan matcher will trust a bad seed and latch to the wrong wall — the classic failure mode recorded in the project memory note `scan-to-consensus-seat-and-misaligned-tail` (crisp scan, wrong global pose).

## 5. Inputs that matter for an open-loop PWM rover, and the encoder transition

1. **Pack voltage.** Brushed-DC no-load speed is ∝ applied voltage; the L298N-class driver drops ~2 V on top, so the effective motor voltage is `duty·(V_batt − V_drop)`. Log `V_batt` at move start and end; feature `ΔV·duty·T`. Cheapest win: compensate in firmware (`duty' = duty·V_nom/V_batt`) and let the corrector learn only what's left.
2. **Ramp / profile.** Per-move ramp loss is ~0.25 s × steady speed. Log the ramp profile ID and its duration; feature `T` alone absorbs it linearly.
3. **Surface / traction proxy.** No IMU, so use the LiDAR: RMS of the scan-to-scan residual during motion, or spectral power of the per-0.1 s increment jitter, as a vibration stand-in (Brooks & Iagnemma classify terrain from wheel-frame vibration PSD; the same features from the scan-increment series are a zero-cost analogue). One-hot floor class from the map position is the fallback.
4. **Thermal / time.** Time since episode start and cumulative run time (motor heating raises winding resistance).
5. **Lift/tilt state, payload.** Categorical.
6. **Rotation geometry.** For turns, features `Δθ_cmd`, `sign(Δθ)`, and the lateral-walk regression `Δy ≈ c·Δθ`.
7. **Encoders arrive (Hall A-channel ×4):** replace `duty·T` with integrated tick distance per wheel in `f_kin`; the residual shrinks to slip and roller effects (what SlipOdometryNet and the mecanum-GRU model), and per-wheel tick asymmetry becomes the best surface/slip feature. Keep the *same* corrector interface; only the feature vector changes — and re-validate from scratch (leave-one-episode-out), because the residual distribution is new. When an IMU eventually lands, the AI-IMU / RINS-W pseudo-measurement pattern (zero lateral velocity except when the mecanum is commanded to strafe) is the next rung.

## 6. Concrete first implementation (≈100 lines, numpy only)

```python
# residual_corrector.py — Bayesian ridge on hand features, per-episode update, covariance out.
import numpy as np

FEATS = ["one", "dutyT", "T", "dV", "dV_dutyT", "surf", "surf_dutyT"]

def f_kin(duty, T, ramp=0.25, v0=0.103, k=0.342):
    """Measured affine timed model (m). Vector-safe."""
    return (v0 + k * duty) * np.maximum(T - ramp, 0.0)

def feats(duty, T, volts, surf, v_nom=11.4):
    dV = volts - v_nom
    return np.stack([np.ones_like(duty), duty * T, T, dV, dV * duty * T, surf, surf * duty * T], 1)

class ResidualCorrector:
    """One Bayesian-ridge per output axis (dx, dy, dth). Prior mean 0 == fixed model."""
    def __init__(self, d=len(FEATS), tau2=0.05**2, sigma2=0.01**2, forget=0.99):
        self.P0 = np.eye(d) / tau2            # prior information
        self.P = {a: self.P0.copy() for a in "xyt"}
        self.b = {a: np.zeros(d) for a in "xyt"}
        self.s2 = {a: sigma2 for a in "xyt"}  # residual variance (updated from held-out episodes)
        self.forget = forget

    def update_episode(self, X, R):           # X: (n,d) feats, R: (n,3) label - f_kin
        for i, a in enumerate("xyt"):
            self.P[a] = self.forget * self.P[a] + (1 - self.forget) * self.P0 + X.T @ X / self.s2[a]
            self.b[a] = self.forget * self.b[a] + X.T @ R[:, i] / self.s2[a]

    def predict(self, x):                     # x: (d,) -> mean(3,), cov(3,3)
        mu, var = [], []
        for a in "xyt":
            S = np.linalg.inv(self.P[a]); w = S @ self.b[a]
            mu.append(x @ w); var.append(self.s2[a] + x @ S @ x)
        return np.array(mu), np.diag(var)

def leave_one_episode_out(episodes, make=ResidualCorrector):
    """episodes: list of (X, R). Returns RMS per axis for fixed model vs corrector on each held-out episode."""
    out = []
    for k, (Xk, Rk) in enumerate(episodes):
        m = make()
        for j, (X, R) in enumerate(episodes):
            if j != k: m.update_episode(X, R)
        pred = np.array([m.predict(x)[0] for x in Xk])
        out.append((np.sqrt((Rk**2).mean(0)), np.sqrt(((Rk - pred)**2).mean(0))))
    return out   # each row: (fixed-model RMS, corrected RMS) — corrector must win on the median row
```

Usage per episode: collect moves → localize at-rest scans against the locked map → `R = label − f_kin` → gate by scan-match covariance → `update_episode` → run `leave_one_episode_out` on the buffer → only if the corrector wins on the median held-out episode does it become the motion prior for the next episode. Log both RMS columns per episode in the diary.

## 7. How many labelled moves before it beats the fixed affine model — a rig-calibrated toy

Simulation (numpy, seed 0, 200 reps): truth = measured affine model × hidden voltage gain (assumed +6 %/V, **not yet measured**) × hidden surface factor (assumed −3 % speed, +30 % ramp loss on one of two floors) + 1 cm process noise; labels add 0.7 cm LiDAR-localization noise; training = 8 episodes at random voltages/floors, test = a **held-out episode** (block CV). Ridge corrector on the 7 features above, λ = 0.01.

| labelled moves (total) | fixed affine RMS | ridge residual RMS (surface observed) | ridge residual RMS (surface **unobserved**) |
|---|---|---|---|
| 5 | 2.6 cm | 2.3 cm | 3.5 cm |
| 10 | 2.7 cm | 2.2 cm | 3.5 cm |
| 20 | 2.7 cm | 1.5 cm | 2.7 cm |
| 40 | 2.6 cm | 1.2 cm | 2.5 cm |
| 80 | 2.7 cm | 1.1 cm | 2.3 cm |
| 160 | 2.5 cm | 1.1 cm | 2.3 cm |

Readings: (a) break-even ≈ 20 moves, saturating by 40–80, when the regime variables are *observed*; (b) with the surface unobserved the corrector needs ≥ 20 moves just to stop hurting and never gets below ~2.3 cm — the unexplained regime variance dominates, exactly the random-CV trap in reverse. The effect sizes are assumptions; the shape is not. Replace the assumed 6 %/V and 3 % with measured values (two-voltage, two-floor calibration runs, ~20 moves each) before trusting any absolute number. Script: `scratchpad/sim.py` in the session that authored this page (regenerable from the description above).

## Recommendation for this rig — a ladder from simplest to model-based

1. **Firmware voltage compensation** (`duty' = duty·V_nom/V_batt`) + measured ramp constant. Zero learning; removes the largest suspected systematic. Verify by re-running the 0.5 m repeatability at 10.8 V and 12.4 V.
2. **Per-episode affine refit** of `(v0, k)` and the rotation constants by least squares on that episode's labels; keep the map-localized labels + features in a per-episode buffer from day one.
3. **Bayesian ridge residual corrector** (§6) with `[dutyT, T, ΔV, ΔV·dutyT, surf, surf·dutyT]`, prior = fixed model, RLS-λ update, leave-one-episode-out gate. Expect it to pay off at ~20–40 moves *only if* a surface proxy is logged — add the scan-increment jitter feature before anything else. Output the analytic covariance as the scan-matching prior; check 1σ/2σ coverage per episode.
4. **Fitted Thrun α₁..α₄** from the same buffer as the fallback covariance for any consumer that can't take a full Σ.
5. **Sparse GP on the residual** (SE kernel, ≤ 500 inducing points, refit at episode end) once the buffer exceeds ~300 moves or per-0.1 s increments are used as samples (10³–10⁴ quickly). Buys non-linear duty/voltage interactions and native σ; Trivedi-style sigma-point propagation for pose covariance.
6. **Encoders land → swap `f_kin`**, keep the corrector; residual becomes slip/roller; per-wheel tick asymmetry becomes the slip feature. Re-validate from zero.
7. **Small 1-D CNN / attention on windows** (Navone-style, online from the LiDAR teacher, MAE loss, replay buffer) only when ≥ 10⁴ labelled increments exist across ≥ 3 floors and the GP's held-out error has plateaued above the label noise. Add an IMU before this rung; without inertial data the window carries little the ridge doesn't.

Never promote a rung on random-CV evidence; the gate at every rung is the median held-out-episode RMS vs the fixed affine model, plus covariance coverage.

## Sources

- Brossard & Bonnabel, "Learning Wheel Odometry and IMU Errors for Localization," ICRA 2019. https://ieeexplore.ieee.org/document/8794237 · code https://github.com/CAOR-MINES-ParisTech/lwoi · HAL hal-01874593
- Brossard, Barrau & Bonnabel, "AI-IMU Dead-Reckoning," IEEE T-IV 2020, arXiv:1904.06064. https://arxiv.org/abs/1904.06064
- Brossard, Barrau & Bonnabel, "RINS-W: Robust Inertial Navigation System on Wheels," IROS 2019, arXiv:1903.02210. https://arxiv.org/abs/1903.02210
- Trivedi et al., "A Probabilistic Motion Model for Skid-Steer Wheeled Mobile Robot Navigation on Off-Road Terrains," ICRA 2024, arXiv:2402.18065. https://arxiv.org/abs/2402.18065
- Navone, Martini, Angarano & Chiaberge, "Online Learning of Wheel Odometry Correction for Mobile Robots with Attention-based Neural Network," 2023, arXiv:2303.11725. https://arxiv.org/abs/2303.11725
- "Slip-Aware Wheel Odometry for 4-Wheeled Skid-Steer Mobile Robots Using a Compact 1-D Convolutional Neural Network" (SlipOdometryNet), Research Square preprint rs-9959755 (simulation only). https://www.researchsquare.com/article/rs-9959755/v1
- "Drift compensation of a holonomic mobile robot using recurrent neural networks," Intelligent Service Robotics 2022. https://doi.org/10.1007/s11370-022-00430-w
- Okawara et al., "Tightly-Coupled LiDAR-IMU-Wheel Odometry with Online Calibration of a Kinematic Model for Skid-Steering Robots," IEEE Access 2024, arXiv:2404.02515. https://arxiv.org/abs/2404.02515
- Okawara et al., "Tightly-Coupled LiDAR-IMU-Wheel Odometry with an Online Neural Kinematic Model Learning via Factor Graph Optimization," RAS 2025, arXiv:2407.08907. https://arxiv.org/abs/2407.08907
- WING: "Wheel-Inertial Neural Odometry with Ground Manifold Constraints," 2024, arXiv:2407.10101. https://arxiv.org/abs/2407.10101
- Wang et al., "Path Tracking for a Skid-steer Vehicle using MPC with On-line Sparse Gaussian Process," IFAC-PapersOnLine 2017. https://www.sciencedirect.com/science/article/pii/S240589631731635X
- Bui, Nguyen & Turner, "Streaming Sparse Gaussian Process Approximations," NeurIPS 2017, arXiv:1705.07131. https://arxiv.org/abs/1705.07131 · code https://github.com/thangbui/streaming_sparse_gp
- Xie, Low et al., "GP-Localize: Persistent Mobile Robot Localization using Online Sparse Gaussian Process Observation Model," arXiv:1404.5165. https://arxiv.org/abs/1404.5165
- Censi, "An accurate closed-form estimate of ICP's covariance," ICRA 2007, DOI 10.1109/ROBOT.2007.363961. https://censi.science/research/robot-perception/icpcov/
- Roberts et al., "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure," Ecography 40:913–929, 2017, DOI 10.1111/ecog.02881.
- Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks," PNAS 2017 (EWC). https://www.pnas.org/doi/10.1073/pnas.1611835114
- Brooks & Iagnemma, "Vibration-based terrain classification for planetary exploration rovers," IEEE T-RO 21(6):1185–1191, 2005.
- Antonelli, Chiaverini & Fusco, "A calibration method for odometry of mobile robots based on the least-squares technique," IEEE T-RO 2005 (UMBmark lineage). https://www.researchgate.net/publication/3450234
- Thrun, Burgard & Fox, *Probabilistic Robotics*, MIT Press 2005, ch. 5 (odometry motion model, α₁..α₄).
- Bishop, *Pattern Recognition and Machine Learning*, 2006, §3.3 (Bayesian linear regression); Ljung, *System Identification: Theory for the User*, 1999 (RLS with forgetting).
- Cho, Kim & Kim, "DeepLO: Geometry-Aware Deep LiDAR Odometry," arXiv:1902.10562; Nicolai et al., "Deep Learning for Laser Based Odometry Estimation" (Oregon State) — end-to-end comparison class only.
- Toy simulation (this page §7): numpy script with the rig's measured constants; assumptions flagged inline.

## Related

- [[odometry-self-calibration-classical]] — the few-parameter model this corrects; [[odometry-dataset-and-derived-gt]] — the logging spec and derived labels it trains on
- [[land-rover-v1-rig]] · [[land-rover-v1-build-guide]] — the hardware and measured timed model
- [[map-then-navigate]] · [[anchor-map-protocol]] — where the labels come from
- [[2d-lidar-slam]] · [[slam-toolbox]] · [[measurement-selection-uncertainty]] — the scan-matching consumer of the motion prior
- [[learned-slam]] — end-to-end learned odometry landscape (comparison class)
- [[trajectory-refinement-and-fusion]] · [[reconciling-competing-signals]] — joint refinement once the corrector's residuals feed back
- [[sensor-weaknesses-and-fixes]] · [[imu-vio-integration-reality]] — what an IMU would add to rung 7
