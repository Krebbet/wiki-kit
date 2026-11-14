# One pose owner, and why a Kalman filter did not help (drone-prototype EDA350 build + EDA367)

How the rover's pose ("where am I, how sure") is produced since 2026-11-14, and what a held-out test said about
adding a Kalman filter. **Status: merged (PRs #305, #306, #307, #308, #309, 2026-11-14). Proved offline on recorded
episodes only: the rover was not driven. The PoseService S0–S3 is the live code path on master. The mean move model is
built behind `pose.mean_model`, default OFF; its offline gain (TEST p95 4.26 → 3.44 cm) is POST HOC (the
pre-registered spin-only form failed). Its first properly pre-registered test is a live SHADOW run, still owed
(P-01570). The refit heading sigma is ON.**

## Source

drone-prototype repo, master `1395f64d`:
- `eda/EDA350-central-odometry/PROPOSAL.md` (requirements, design, migration stages S0–S7; PR #279) and `BUILD.md`
  (S0–S3 as built, replay numbers; PR #305)
- `eda/EDA367-pose-kalman/FINDINGS.md` (the Kalman EDA; PR #307), `PREREG.md`, `BUILD.md` and `SHADOW_PREREG.md`
  (D1 + D3 as built; PR #308)
- `src/drone/pose/{se2,service,replay,mean_model}.py`, `config/pose.json`
- diary entries 2026-11-12 (EDA350 proposal), 2026-11-14 (PoseService S0-S3; PR #305 review; EDA367; EDA367 D1 + D3)
- parked P-01330…P-01340 (the proposal's measured gaps), P-01530…P-01549 (build), P-01560…P-01568 (EDA367),
  P-01570…P-01574 (mean model); human decision D-00023

## The problem it solved

Before the build there were **four** pose integrators that shared no state (EDA350): the Navigator, the rover
service's manual-mode LivePose, PoseClock and the firmware's own tick pose. In manual mode the service used wheel
heading only. Measured against ICP fixes over 46 episodes, that heading was p95 8.8 deg (max 36 deg per segment); the
Navigator's IMU heading was p95 1.0 deg. In task mode the service's "pose now" stayed frozen at the move's start.

## What was built (S0–S3)

- `drone.pose.service.PoseService`, hosted by the rover service. It is the one owner of the pose. `LivePose` is now a
  view of it, and the Navigator is its client.
- Every relocalisation fix, weak stop, cold start or distrust is a **ledgered correction**.
- Manual moves take the IMU heading. MCL can offer poses, but only as a shadow producer. The lane frame is retired.
- Replay checks (56 episodes, MEASURED, `build_replay.py`):
  - The service reproduces the Navigator's own logged prior on 1169 / 1175 fixes, within 0.1 cm / 0.05 deg (max 0.39 cm).
  - The old and new LivePose views agree on 2736 / 2736 snapshots.
  - Manual heading vs ICP drops from p95 7.33 deg (wheels) to 1.46 deg (IMU).
  - In-move pose vs the tick path drops from p95 38.7 cm (frozen) to 2.97 cm. This is agreement with the wheels, not
    accuracy.
- **A gate that cannot fire.** The sigma gate (decision 6) cannot refuse a fix with the shipped config. The EDA363 far
  check ([[relocalisation-far-check]]) re-searches every fix more than 0.25 m / 10 deg from the prior, and far-checked
  fixes are exempt. So "0 of 1175 refused" follows from the code; it was not measured. The human kept this as
  option (a) (D-00023 D4, P-01540).
- Not built: S4 `pose_at` (P-01535), S5 sensor poses from config (P-01536), S7 EKF (shelved, D-00023 D2). `here()`
  still returns degrees (P-01530). No live run yet (P-01531, P-01532, P-01549).

## The Kalman question (EDA367): the filter does not help, the mean model does

Split by date: TRAIN 11-03..07 (657 fixes), TEST 11-10..13 (518 fixes, 15 episodes, cluster bootstrap over episodes).
The yardstick is the ICP fix, which is not ground truth (P-01563).

- **The filter itself gains nothing measurable.** Same process model, filter vs replace-on-fix, paired on TEST:
  - position mean −0.001 cm [−0.013, +0.021];
  - heading −0.010 deg [−0.022, −0.002] (real, but tiny).

  The reason: one fix is about 0.24 cm / 0.18 deg, one move about 1.4 cm / 0.5 deg, and the rover relocalises after
  nearly every move. The fitted EKF gain is about 0.9–0.96 for position (median 0.89 after one move, 0.96 after two or more; heading 0.63
  after one move), which is the same as replacing the pose with the fix. **At this
  fix cadence a Kalman filter is replace-on-fix with extra steps.** Revisit only if fixes become sparse or the
  localiser starts to emit a covariance.
- **The gain is the mean move model.** These are biases the tick model leaves in its mean:
  - legs: −3.7 % along, −2.6 cm/m lateral;
  - spins: rotation about a centre per direction (the [[spin-centre-rigid-point]] term);
  - CCW IMU scale −0.26 %.

  TEST position p95 drops from 4.26 to 3.44 cm (dp95 [−1.21, −0.43]).
- **Read that pass as post hoc.** The pre-registered model had the spin and IMU-scale terms only, and it fails the
  bar: p95 3.97 cm, dp95 [−0.80, +0.03]. The leg terms and the keep rule were added after PREREG.md, fitted on TRAIN
  only and frozen before any TEST scoring. The live shadow run (`SHADOW_PREREG.md`, frozen `score_shadow.py`) is the
  first properly pre-registered test of the full model.
- **Sigma:**
  - The refit fixes heading calibration: 2-sigma coverage 69 → 92 % as an innovation.
  - Position stays at 85–89 % against a 90–98 % bar (P-01565).
  - An innovation gate would refuse about 6 % of good fixes, so it does not replace the far check.

## Switches (config/pose.json, rule 26)

| key | values | default | env |
|---|---|---|---|
| `pose.mean_model` | off / shadow / on | **off** | `DRONE_POSE_MEAN_MODEL` |
| `pose.heading_sigma` | refit / phase_a | **refit** | `DRONE_POSE_HEADING_SIGMA` |

"shadow" logs the modelled pose next to the live one at every move and fix (Navigator `odom_move` `mm_estimate`,
`nav relocalise` `prior_mm`) and changes nothing else. Position sigma is unchanged by either heading setting. With "off", the EDA350 replay is byte-identical to before the
build.

## Transferable lessons

- With a tight fix after every move, look at the **process-model mean** before you build a filter. A filter only
  blends; it cannot remove a bias that the prediction itself carries.
- Before you quote a counterfactual ("0 refused"), check that it could have fired at all (PR #305 B1).
- If you add model terms after a pre-registration, call it a deviation, even when the new terms are fitted on TRAIN
  only. Score the registered form next to the extended one (PR #307 B1).

## Related

- [[odometry-closed-loop-pipeline]] (the 09-17 calibration view, now historical for the pose path)
- [[spin-centre-rigid-point]] · [[relocalisation-far-check]] · [[mcl-shadow-localiser]] · [[hard-values-in-config]]
- [[odometry-self-calibration-classical]] · [[learned-odometry-correction]]
