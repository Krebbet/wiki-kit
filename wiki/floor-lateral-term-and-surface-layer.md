# The rover-fixed sideways floor term and the floor surface layer (drone-prototype EDA359)

Two results about measuring floor height with a tilting 2-D LiDAR. (1) The sideways ("lateral") floor slope the
per-station floor calibration fits at down tilts is mostly a property of the rover, not of the floor. (2) A smooth
floor-surface layer can be the height reference instead of each station's own plane. **Status: merged (PR #283,
2026-11-13); the surface layer is behind `floor.floor_surface_on`, default OFF (`DRONE_FLOOR_SURFACE`). Offline on
recorded worlds only. The real confirmation is the live plan L1 / L2 (`eda/EDA359-floor-selfcal/LIVE_PLAN.md`), not
yet run.**

## Source

drone-prototype repo, master:
- `eda/EDA359-floor-selfcal/` (FINDINGS, PREREG, LIVE_PLAN); diary entry 2026-11-12 "the lateral floor term is rover-fixed"
- `src/drone/floorsurface.py`; `clearance.HeightEvidence.ingest`
- parked P-01380…P-01389, P-01430; background EDA342 (floor surface model), EDA298 (tilt floor calibration)

## Result 1: the lateral term is rover-fixed (honest version)

- **What passed (pre-registered):** reversal pairs, the same floor patch seen from opposite headings, keep
  −4.66 cm/m at −20° tilt (CI −5.05…−4.38; 119 pairs, effective n ≈ 19 stations) of the observed −5.12 cm/m.
  A real floor slope would flip sign under reversal. So most of the term is fixed to the rover: head, rig or chassis.
  Which of those is not shown.
- **What failed:** the pre-registered confirmations. The agreement rule failed in its angle form (reversal −7.2° vs
  tilt-difference −3.9° vs GMRF −2.5…−1.5°). Held-out test 1 had 2 pairs instead of the ~1259 sized for (that count
  had included walls; floor-only it is 0).
- **Caveats:** the pre-registration was not blind (EDA342 had already seen −4.3). A post-hoc heading-constant
  estimate (−5.07; held-out days −4.87) is a weak second method because it is close to the observed value itself.
  The real floor slope is ~1 cm/m (IMU). The split between a yaw term and a constant is not established (P-01380,
  P-01382). Adopting a self-calibrated per-tilt term waits on live L1 in two rooms (P-01381).

## Result 2: the floor surface layer

- EDA342's GMRF over active cells only, with Rao-Blackwellised marginal sd (1.6 s vs 32 s exact).
- Causal: a station joins the surface only after its own heights are judged.
- On the held-out world a new station's floor fits the surface better than its own plane (|r| p50 2.12 → 1.53 mm,
  92 % of stations). Decisions move only at the 2 cm drive-over line: 8–19 cells per world turn drive-over, 4–6 the
  other way.
- **Caveats:** with the surface ON, floor-level returns lose the weak-window +4 cm caution (P-01384; live L2 must
  judge it). The surface's sd does not see model error (P-01385). Wide flat objects left in place still become floor
  (P-01388). Worlds recorded before floorcal get no surface reference.
- A trap worth knowing: a whole-ring plane fit returns the scan plane itself (every return of one posture lies on
  it), so it gave the same answer on every ring with 100 % inliers. The fix was a pitch-leak correction.

## Related

- [[floor-map-sensing-options]] (stale, passive-stereo premise) · [[tilting-2d-lidar-multiplane-capture]]
- [[camera-calibration-and-self-calibration]] · [[odometry-self-calibration-classical]] (same self-calibration idea)
- [[spin-centre-rigid-point]] (another rover-fixed term found in the logs the same night)
