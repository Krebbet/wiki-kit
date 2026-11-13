# Why in-place spins shift the rover centre: one rigid point (drone-prototype EDA361)

A mecanum rover that spins in place does not end where it started: its centre moves 1–2 cm, and the direction of
the shift depends on the turn direction. EDA361 shows that one fixed point explains this, and that LiDAR data alone
cannot say whether that point is a real rotation-centre offset or an error in the LiDAR lever. **Status: merged (PR
#286, 2026-11-13); the correction is built behind `body.spin_centre_on`, default OFF (`DRONE_SPIN_CENTRE`). Offline on
recorded episodes. A floor-mark test is needed before turning it ON (P-01420; drone-prototype `docs/next-run-plan.md`
§2.4).**

## Source

drone-prototype repo, master:
- `eda/EDA361-spin-centre/FINDINGS.md`; diary entry 2026-11-13 "why spins shift the rover centre"
- `config/body.json` (`spin_centre_on`, `camera_from_centre_m`); `bodymodel.NAV_LEVER_M`; `tests/test_spin_centre_eda361.py`
- parked P-01420…P-01425; background EDA350 (central odometry, PR #279 open), EDA219 / EDA223 / EDA282 (lever fits)

## The identity

A rotation-centre offset q and a lever error dl give the same centre shift after a turn θ:

`shift = (I − R(θ)) (q − dl)`

So spins, or anything that uses LiDAR alone, can only measure q − dl. A floor mark does NOT separate (a) from (b)
either: it separates a physical offset from a registration-frame offset (see below). Nothing planned separates (a) from
(b).

## Model choice: decided by extrapolation, not random CV

Candidates: one rigid point (2 numbers), per-direction scrub, and a constant / sync term. Random-style
cross-validation could not separate rigid from scrub (CI spans 0). Held-out tests that extrapolate did:

| held-out test | rigid | alternatives |
|---|---|---|
| leave one episode out | 1.79 cm | 1.86 / 2.41 |
| leave a period out | 2.13 | 2.31 |
| train ≤ 90°, test > 90° | 2.47 | 3.32 |

CW and CCW give the same point within 0.1 cm pooled. The earlier "direction effect" (EDA350) is the odd sin θ term of
one point, not scrub. Fix quality and slip add residual noise (r −0.34, 0.22) but cannot make the mean shift
(P-01424).

## What it changes, honestly

- Pooled over 338 spins at −15° tilt: p = (−1.67, +0.46) cm, so the lever would become (5.77, 2.74) cm. This is close
  to EDA282's set-up sample (5.8, 3.4).
- The point moved over time: ~0 on 09-22/23, then ~−1.5 cm forward from 10-07 on, stable for five weeks (P-01423).
  Any config value is a snapshot.
- Held out: post-spin centre error rms 2.79 → 1.79 cm; relocalise prior p50 1.74 → 1.13 cm.
- For ICP-registered poses the lever cancels, so ON changes only dead-reckoned poses, the footprint and hard-coded
  constants (review). The floor-mark test separates a physical offset from a registration-frame one, not (a) from a
  mis-taped lever.
- Tilt dependence is suggested, not established (P-01421).

## Related

- [[mecanum-wheel-handedness]] · [[odometry-self-calibration-classical]] · [[odometry-closed-loop-pipeline]]
- [[floor-lateral-term-and-surface-layer]] (another rover-fixed term found the same night)
