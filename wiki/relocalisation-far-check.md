# The far check: catching a wrong "strong" relocalisation (drone-prototype EDA363)

A rule for scan-to-map relocalisation with a local search. If an accepted fix lands far from its prior, search
again round the full circle under the same acceptance rule before trusting it. **Status: merged (PR #291,
2026-11-13); rule 15za, `localise.far_check`, default ON (`DRONE_FAR_CHECK=0` reverts). Replay only, one room, and it
is proven on ONE known wrong accept (P-01460). Live check queued in drone-prototype `docs/next-run-plan.md` §2.5b.**

## Source

drone-prototype repo, master:
- `eda/EDA363-wrong-accept/FINDINGS.md`; diary entry 2026-11-13 "live localiser wrong-accepts"
- `localise.far_check`; tests through `Navigator.relocalise` / `stop_and_localise` on recorded captures
- parked P-01398 (the wrong accept), P-01460…P-01466

## The failure, traced to the search

On 2026-10-07 (run blind3) the rover never moved, yet the navigator accepted a wrong "strong" fix and later re-fixed
88 cm / 90° away. The cause was the search, not the scan:
- the start guess was 139.5° off the truth;
- the local registration seeds only ±90° around its prior, so the true basin (246 inliers) was never tried;
- a wrong basin (182 inliers, rms 0.88 cm) passed as "strong". Its runner-up (136) was not strong, so no ratio test
  applied.

The replay reproduces every logged basin exactly. MCL in shadow got this case right ([[mcl-shadow-localiser]]).

## How rare (counted)

3993 accepted relocalisations (210 episodes, 09-22 → 11-13): 1 detected wrong accept (a same-ticks contradiction) in 792 multi-fix groups. A
full-circle re-search of 593 replayed fixes finds a stronger basin elsewhere only for blind3. EDA363 found 0
camera-caused wrong accepts, but it counted accepts only. EDA364 later found 3 camera-caused refusals
([[camera-vote-uninitialised-mask]]).

## The rule

An accepted fix > 25 cm or > 10° from its prior is re-registered round the full circle → kept / switched / refused.
Replay: blind3 switched onto the truth (0.4 cm from the later re-fix); 35 / 35 other triggered fixes kept; 0
refused. Cost: one extra registration on ~1 % of stops (not timed live, P-01465).

Rejected alternatives, with reasons: ratio gates (lose 146–653 good fixes); wheels-still agreement (refuses the right
re-fix and is blind to a first fix); a second posture (agrees with the wrong basin); an up-tilt bar (a symptom fix).

## Limits

n = 1 positive. The "switched" path ran once, at ratio 0.74, just under the 0.75 ambiguity bar; a slightly worse
scan would have been refused, not switched. Wrong accepts near their prior are not triggered (P-01461); the count found 0 of 360 random near-prior fixes with a
stronger basin round the full circle, a 95 % upper bound of about 0.8 %. A wrong
bearings / camera accept becomes a prior the far check cannot see through (P-01462; EDA364 proposes a post-accept
verify). 10 % of recorded captures no longer reproduce their logged registration (P-01464).

## Related

- [[stop-and-go-navigation-on-a-locked-map]] · [[mcl-shadow-localiser]] · [[camera-vote-uninitialised-mask]]
- [[new-room-start]] (new-room fixes pass the far check too)
