# Object and floor detector rates measured on the rover (EDA348, EDA356; with caveats)

These are the measured per-look miss and false-detection rates of the drone-prototype rover's evidence models: LiDAR
bodies, camera doors, windows, wall art, camera floor items, and the camera-only "only floor" check. They come from
production look functions replayed on recorded office worlds, scored against **judged** truth. The truth was judged by
eye from crops; it is not ground truth. The page is a reference for any design that needs a detector likelihood (e.g.
[[object-certainty-model]]). **Do not quote a rate without the caveat in its row.** All of them come from one office,
offline, and none were re-measured live.

## Source

drone-prototype repo, master `1fda3950` (2026-11-12):
- `eda/EDA348-object-reobservation/FINDINGS.md` §2 (PR #272): `rates.py`, 6 training worlds, office-fresh1 held out
- `eda/EDA356-camera-first-floor/FINDINGS.md` "Answer first" (PR #275): camera floor-check rates, train vs held out
- `eda/EDA355-object-certainty/WALLART.md` (branch `eda355-object-certainty`, PR #274, open): why the wall-art rate is not a detector rate
- parked P-01233, P-01236, P-01281, P-01291, P-01292, P-01310…P-01313

## Re-observation rates (EDA348)

| model | looks | misses | point miss rate | 90 % upper bound used | false "present" on bare wall | held-out fresh1 misses | caveat |
|---|---|---|---|---|---|---|---|
| body (LiDAR, furniture) | 335 | 15 | 0.045 | 0.48 (worst object: a see-through wire bin, 12/25) | not measured | 0/77 | furniture only; small-object LiDAR miss rate unmeasured (P-01281) |
| door (camera) | 31 | 2 | 0.065 | 0.146 | 1/49 | 1/7 | door/window truth never audited (P-01292) |
| window (camera) | 22 | 4 | 0.182 | 0.308 | 4/90 | 2/4 | as door |
| wall art (camera) | 12 | 7 | 0.583 | 0.745 | 1/6 | 6/7 | **truth contaminated; not a detector rate** (below) |
| floor item (camera) | - | - | - | 0.5 default | - | in-sample 21/54 = 0.39 | no held-out floor-item truth (P-01236) |

**The 58 % wall-art "miss rate" measures bad expectations, not the detector** (EDA355 Part B). Of the 13 traced misses,
9 are bad expectations: one "art" record is a door's knob plate, and one is real art filed at desk height from clipped
boxes. The other 4 are occlusions by the chair or desk above the LiDAR's top return. None is a detector failure on the
record's own art. The underlying cause is geometry: wall looks tilt only 0 / +10 deg from ~0.3 m, so the frame tops out
at 1.25 m (1.5 m range) to 1.58 m (2 m range), while the art hangs at 1.31–1.80 m. In the same frames, the detector found
only 3 of 6 real pieces in view, so it is not fine on art either. Re-measure on clean truth before using any wall-art
rate (P-01291).

## Camera "only floor" check (EDA356)

| per station look | train (6 worlds) | held out (office-fresh1) |
|---|---|---|
| P(sees only floor \| a blocking object is there), debiased | 0.54 (35/65, Wilson 0.42–0.65) | 0.43 (55/129, 0.34–0.51) |
| same, camera-independent truth (LiDAR bodies) | - | 0.60 (134/224, 0.53–0.66) |
| P(sees something \| bare floor) | 0.011 (4/349) | 0.007 (1/145) |

- **The camera misses about half of the blocking low objects per look, and almost never invents one on bare floor.**
- **Camera-sourced truth is optimistic.** The held-out camera-item rate (0.43) and the LiDAR-body rate (0.60) do not
  overlap: objects the camera never detected are absent from camera-sourced truth. On fresh1, camera-item rates
  understate misses about 1.4x per look and 2.7x at two looks.
- **Looks are not independent.** An object the detector cannot see is missed from every station, so the chance that all
  k looks miss falls far slower than 0.5^k. Held-out LiDAR bodies give M(4) = 0.25 and M(6) = 0.10.
- **The gate's config rates are deliberately conservative, not the table's.** Per k, the config M(k) is the **larger**
  of two upper bounds: the train camera items' 95 % bound and fresh1's camera-independent LiDAR-body bound. That gives
  [0.705, 0.571]. Because it uses fresh1's bodies, fresh1 is no longer fully held out for this one value.
- **Consequence:** under those config rates, the camera-first gate (built, switch OFF) fired on 0 of 20 unknown-floor
  blockers across four recorded worlds. With these rates the gate can clear priors only up to 0.084 at threshold 0.95.
  The 0.40 unknown-floor prior (`P_UNKNOWN`, a hand value) is therefore what blocks all 20. Even with the naive rates, 0
  fired, because of camera coverage. This is a finding, not a failure. The gate's 0 wrong clears means nothing, because
  it cleared nothing.
- No rug or other floor surface has rates (P-01312). Range and angle terms are unsupported (P-01313).

## How to use these numbers

- In a Bayesian filter, use posterior means (with the uncertainty in the decision threshold), not the 90 % upper
  bounds. Upper bounds plugged into a likelihood ratio can invert it ([[object-certainty-model]]).
- Temper correlated looks (same view, same occluder). A per-look rate multiplied k times overstates certainty.
- Quote held-out vs in-sample and camera-sourced vs independent truth next to every number.

## Related

- [[object-certainty-model]] · [[fast-visual-hazard-detection]] · [[floor-map-sensing-options]]
- [[point-cloud-object-segmentation-models]] · [[ov3d-instance-seg]]: the detector families behind the camera models
- [[measurement-selection-uncertainty]]
