# MCL cold-start localiser in shadow mode (drone-prototype EDA360)

Results of running Monte Carlo localisation (a particle filter over the locked 2-D LiDAR map) beside the rover's own
ICP cold start, logging both answers and acting on neither. **Status: merged (PR #288, 2026-11-13), switch
`localise.mcl_shadow` default OFF (`DRONE_MCL_SHADOW`). Replay only, one room. The live check L-S5 (two cold
starts with the shadow on) is queued in the drone-prototype `docs/next-run-plan.md` §2.2. MCL is not adopted.**

## Source

drone-prototype repo, master:
- `eda/EDA360-mcl-shadow/FINDINGS.md`; diary entry 2026-11-12/13 "MCL cold-start localiser in SHADOW mode"
- `src/drone/nav/mcl.py`, `nav/mcl_shadow.py` (rule 15z); `tests/test_mcl_shadow_eda360.py`
- parked P-01390…P-01399; earlier test EDA338 (MCL + small_gicp)

## Design

After the live answer, the shadow runs MCL in its own child process (nice 19, 500 MB cap, self-timeout) and appends
both answers to `mcl_shadow.jsonl`. It never acts. Measured cost: MCL 0.14 s median vs the ICP cold start 14.4 s
(max 199 s); the real child 0.38 s wall, 88 MB.

## Results: measured vs agreement (keep them apart)

The reference for most captures is the run's own **accepted live ICP fix**, and accepted fixes can be wrong (one
was: P-01398). So "agrees" below means agreement with our localiser, not truth.

| set | n | result | kind |
|---|---|---|---|
| seeded localisations | 2355 | 2181 agree, 174 undecided, 0 decided off the fix (0 in 11 775 over 5 seeds); pose 2.0 cm / 0.66° median | agreement with accepted ICP fixes |
| cold starts with a seeded reference | 80 | 80 right, 0 wrong | **measured against a seeded reference** |
| cold starts judged by ICP inlier ranking | 57 | agree | agreement only (near-circular) |
| cold starts undecided | 12 | top mode on the mirror, mostly draw luck | — |
| our ICP cold start's 63 refusals | 63 | MCL resolves 56 (14 vs a later accepted fix, 42 by ICP agreement only) | mixed |

- Mirror pairs are the dominant hazard: 110 / 149 cold captures carry one. MCL decides the mirror wrongly in about
  1 % of re-draws on mirror-prone captures (2 in 170; P-01391). That blocks adoption without a stability rule.
- The replay found a real live wrong accept (blind3, 2026-10-07, P-01398) that MCL got right. That case led to the
  far check: [[relocalisation-far-check]].

## Limits

One room (P-01395). The shadow is single-scan; bearings' looks and moves are not shadowed (P-01390). Tilted
relocalisations cannot be replayed (P-01393). Live CPU cost on the rover laptop not measured (P-01396). The seed-0
replay is not bit-reproducible (rng keyed by case order).

## Related

- [[open-source-rover-stack-options]] (where MCL was proposed) · [[relocalization-method-bakeoff]] (June passive-stereo bake-off)
- [[stop-and-go-navigation-on-a-locked-map]] · [[relocalisation-far-check]] · [[camera-vote-uninitialised-mask]]
