# The rover's floor / low-object check: visual first, LiDAR to resolve (drone-prototype, 2026-11-14 → 11-18)

What the rover's "is this patch of floor clear?" check became after a week of measured alternatives: the camera is
the cheap first test, the LiDAR resolves what it escalates. **Status: merged (PRs #311–#350). As of 2026-11-18 the
default gate is OBJECT-FIRST and `visualgate.mode` is "first" (a cleared box skips its LiDAR floor posture; 25 % of
cleared cells are still sampled by the LiDAR into a false-negative ledger). Live evidence is 7 spot checks on
11-18 plus replays. No 2 cm ground truth exists (truth is judged, mostly furniture); every miss rate below is capped by
where the truth discs sit (P-01592, P-01604).**

## Source

drone-prototype repo, master `a39f6b37`:
- EDA368 (current state, research, problems, proposal; D-00024), EDA369 (shared geometry + PREREG), EDA370 / EDA371 /
  EDA372 (candidates A / B / C), EDA373 (smallest set), EDA376 (floor banks, visual clear gate), EDA377 (floor vs
  non-floor separation), EDA378 (fused gate), EDA379 (stereo flatness), EDA380 (crop DINO on regions), EDA381 (camera
  height), EDA382 (LiDAR line continuity), EDA383 (cascade), EDA384 (independent measures), EDA385 (object-first check)
  under `eda/`
- diary entries 2026-11-14 (f)–(k), 2026-11-16 (e), (g) visual-first, 2026-11-17 (a)–(e), 2026-11-18 (a)–(b)
- parked P-01575…P-01617 (EDA368–373), P-01698…P-01705 (EDA376), P-01731…P-01755 (gate, cascade, object-first)
- research pages [[floor-object-detection-methods]] and [[visual-floor-anomaly-methods]]

## Step 1: three geometric candidates, pre-registered (11-14) — none works alone

Scored once on a held-out world (office-fresh1) under EDA369's pre-registration:
- **A, stereo floor-plane check:** fails at 0.9–1.1 m (matcher tail, p95 13.3 px vs a 2.5 px signal), so cut to the
  near field (< 0.6 m); there, miss 0.32, coverage 0.60, bare-floor false alarm 0.0008. The black diamond-plate mat
  breaks SGBM.
- **B, motion parallax:** coverage is the binding failure (0.028); it adds at most 0.012 recall.
- **C, change against the same place:** meets the false-alarm bars but misses obstacles that were already in the
  reference; coverage bounded by cross-day registration (235 of 356 looks did not register).
- **Smallest set (EDA373):** no set meets the bars; the s.7 rule leaves **A alone**. Remaining levers were capture
  changes, active light (line laser / depth camera) and 2 cm truth.
- Side findings: the six office worlds share one map frame to a few cm; the stereo over-reads lift moves by 1.10–1.14
  (camera height P-01584, later EDA381: the camera sits 3.9 cm higher than the extrinsic said).

## Step 2: a visual clear gate (11-16 → 11-17)

Human (binding): visual checks FIRST as the cheap clear, the LiDAR only for what the gate escalates, with a known
false-negative rate, starting in shadow mode.
- **EDA376:** DINOv2-S similarity to a bank of LiDAR-confirmed floor cells, per 0.1 m cell: bare floor cleared
  0.72–0.77, real items' own cell cleared 0.15–0.24. Colour/texture alone cannot separate obstacles (AUC 0.59 vs
  DINOv2 0.96).
- **EDA377 → EDA378, the fused gate:** DINOv2 block-8 patch kNN + Lab-LBP kNN + SegFormer P(floor + rug), each as a
  percentile in a reference floor distribution, averaged. AUC 0.954 (nested leave-one-world-out). A fixed threshold
  does not transfer between worlds: at a reference floor pass of 0.95, 35 % of audited items pass; at 0.90 (chosen),
  92 % floor pass and 13.3 % miss (P-01734).
- **Coverage from the frames actually taken** (11-17 a): the unit is the cell; a top-up frame is planned for cells
  no frame covered.
- **Self-mask** (11-17 d): near false alarms were the rover's own wiring; masking the chassis cut escalated
  should-clear cells 7 → 3 in the cascade.
- **Cascade (EDA383):** cells the fused score escalates are re-scored by DINOv2 on a crop of the cell against a
  crop-scale floor bank; nothing not-floor → scrapped as a false positive. A cable lying on cell boundaries is still
  cleared (P-01748).

## Step 3: object first (11-18)

Human rule: object detection first; any object → flatness measures (stereo, then LiDAR); no object → pass if ANY of
the three floor measures passes at 95 % internal certainty; else flatness.
- **EDA384:** naive Bayes over the measures ties the mean-of-percentiles (AUC 0.960 both). The live problem is not the
  combination: known floor fails every measure far more often than its design point, consistent with the steeper
  check views (−34° vs −16° in the reference). Stereo is asymmetric: a blob is near proof, "flat" barely helps (cords
  are flat).
- **EDA385:** on 1811 labelled + 113 live cells it matches the cascade on tall items and sends far fewer cords to the
  LiDAR (11 vs 42 of 61), at 6.4 % false item notes on floor. Cords are detected only ~25 % of the time (P-01754).
- **Live spot tests (11-18 b):** 7 checks; camera and LiDAR agreed on every box the LiDAR could judge. One "known
  empty" box held a black cable + tape strip the LiDAR never saw (below its floor cut); the object check flagged it,
  the old fused gate would have cleared it. Human then switched the mode to "first".

## The LiDAR side: line continuity (EDA382)

The global rule (any return > 2 cm above z = 0 is a hit) blocked the black rubber mat (~1.3 cm plus floor-cal pitch).
The ring rule walks each scan ring in order and excuses returns in a non-raised floor run (level ≤ 3 cm); it only ever
removes global-rule hits. Replay: both mat false alarms gone, 0 audited trays / objects lost, 1 cord at 2.2 cm lost.
Fitting a floor line or plane to measure against was tried in five variants and dropped: each traded litter trays
(a sloped side is a staircase of sub-2 cm steps) against the mat (P-01743).

## Related

- [[floor-object-detection-methods]]: shipping-robot practice and error modes (the research that started step 1)
- [[visual-floor-anomaly-methods]]: patch-level anomaly scoring, separation-calibrated bars, contaminated banks
- [[fast-visual-hazard-detection]] · [[floor-map-sensing-options]] · [[floor-lateral-term-and-surface-layer]]
- [[drone-beliefs-update]]: what a check's evidence does to object beliefs
- [[object-detector-measured-rates]]
