# Odometry Dataset Design and Derived Ground Truth from the Locked Map

**Summary.** Log every motion as a *closed episode* — rest-scan → command → telemetry → rest-scan — with host-stamped, ESP32-stamped and sync-recoverable times; once the LOCKED map exists, each **at-rest** scan becomes a pose label by scan-to-map registration (sub-cm at rest on this rig, a *relative* label between two nearby rests is better than an absolute one), while scans taken **in motion** are only interpolable, never labels. The few-parameter speed law needs ~40 moves per (direction × duty × surface) cell for a 1 % slope; a learned corrector needs an hour-plus of diverse motion *and* the encoders. Log the causes of variance now (applied duty ramp, battery volts, mast state, surface tag, deadman events) or they are unrecoverable later.

> **Scan-plane note (librarian, 2026-09-24).** The "~1.1 m" scan plane on this page is the **June capture rig** (a tripod carrying the stereo camera, `data/calib/rig_geometry.json`). The **prototype rover** scans at **0.2972 m** — sd 0.5 mm, seven independent down angles at open floor, drone-prototype `eda/EDA228-actuator-verification/FINDING.md` (2026-09-24; an earlier 0.337 m was wall hits read as floor). The §Validity row "the map is a horizontal slice at ~1.1 m" should read **0.2972 m**; the mast-state gate itself is unchanged. §Deskewing's "no encoders, no IMU" premise is also superseded — encoders landed 2026-09-15 and closed-loop velocity 2026-09-17. Canonical statement and the tilt consequences: [[tilting-2d-lidar-multiplane-capture]] §CORRECTION.

> **Read alongside:** [[odometry-self-calibration-classical]] and [[learned-odometry-correction]] (the consumers of these labels), [[weak-scan-registration-methods]] (degeneracy-aware ICP — the labeller), [[global-alignment-wall-refinement]] (why the locked map carries a ~2 cm bow), [[camera-lidar-temporal-calibration-and-pose-interpolation]] (δt recovery by motion cross-correlation — the same trick works host↔ESP32), [[land-rover-v1-rig]] (the ESP32/TB6612 open-loop drive), [[2d-lidar-slam]] (Cartographer scan-matcher family), [[measurement-selection-uncertainty]]. *(research page — sources cited inline; web-researched 2026-09-14; project facts from the prototype repo, flagged as such.)*

---

## 0. Framing: two regimes, only one of them labellable

The rig's mapping style is stop-and-scan: short open-loop moves, scan at rest. That splits every logged sample into two classes with different fates:

| Regime | Sensor state | Can the locked map label it? | Label type |
|---|---|---|---|
| **At rest** (wheels stopped, LiDAR spinning, ≥1 full revolution after settle) | undistorted scan, static rig | **Yes** — scan-to-map registration, at-rest accuracy limited by map bias + geometry, not by noise | absolute SE(2) pose + covariance; and *relative* pose between consecutive rests (the odometry label) |
| **In motion** (any wheel PWM ≠ 0, or < settle time after stop) | skewed scan (§1.3), vibration, mast sway | **No** as a direct label — only by interpolating between the bracketing rest labels under a motion model, which is circular when the motion model is the thing being learned | interpolated pose with `label_source="interp"`, wide covariance; usable for sanity, not for fitting |

Consequence for data design: **the unit of labelled data is the move** (rest_i → rest_{i+1}), not the scan. Everything logged during a move (duty ramp, ESP32 telemetry, battery, camera frames) is a feature of that move; the label is Δpose between two certified rest scans. This is exactly the "relative-pose per segment" convention of the odometry benchmarks (§2).

---

## 1. Derived ground truth: registering rest scans against the final map

### 1.1 Method family and achievable accuracy

- **Scan-to-map ICP / point-to-line against wall lines** — what the project already has (rank/eigen degeneracy test + "certifiable" seat metric, EDA-series). Censi's joint-calibration paper reports scan-matching (PLICP) precision **~1 mm and tenths of a degree for 5–10 cm displacements** on a Hokuyo URG-04LX with 3 mm range σ [src: Censi 2013, censi.science/pub/research/2012-joint_calibration.pdf] — *demoed*. Our C1 single-scan wall RMS is 0.10 cm (project measurement), so the same order applies at rest.
- **Correlative scan matching (Olson CSM)** — exhaustive multi-resolution search over a pose window against a rasterised likelihood field; robust when the prior is weak (a move whose open-loop estimate is off by several cm) and gives a *sampled* posterior from which covariance falls out directly [src: Olson ICRA 2009, april.eecs.umich.edu/pdfs/olson2009icra.pdf] — *demoed*, used inside Cartographer's loop-closure branch-and-bound [[2d-lidar-slam]]. Good as the **global initialiser** for a rest scan, then refine with the line-ICP.
- **Particle-filter MCL (amcl-like)** — the ROS default; on the Deutsches-Museum global-localization test, AMCL 0.09 m / 0.78°, Cartographer 0.06 m / 0.73° [src: arXiv:2404.07644 Table 4] — *demoed*, but those are museum-scale, in-motion numbers. With a mocap reference, AMCL trajectory error in motion reached **up to 0.12 m** and grew with path speed and with LiDAR occlusion [src: Springer 2025, doi:10.1007/978-3-031-91463-8_33] — *demoed*. **Do not use a filter as the labeller**; its in-motion numbers are an order worse than what a static scan against a crisp line map gives.
- **What to expect on this rig at rest (synthesis):** random part ≈ mm (noise 0.10 cm, ~500 rays/rev at 0.72°, 5 kHz [src: SLAMTEC C1 datasheet]); systematic part = the locked map's own error — a coherent ~2 cm wall bow, not noise ([[global-alignment-wall-refinement]], memory `lidar-cloud-locally-crisp-band-is-bow`). The bow is a *function of location*, so it **largely cancels in the relative label** between two rests a few decimetres apart that see the same walls. Hence: absolute label ≈ 1–2 cm class, **relative (per-move) label ≈ few mm** class — *claimed*, to be verified by the check in §1.4.

### 1.2 What makes a rest scan unlabellable (and the flag to attach)

| Cause | Detection at label time | Flag |
|---|---|---|
| **Degenerate geometry** (one wall, corridor-like, along-wall slide) | eigen ratio of the ICP Hessian below threshold — Zhang/Kaess/Singh's degeneracy test, solve only well-conditioned directions [src: ICRA 2016 doi:10.1109/ICRA.2016.7487211]; Censi's closed-form ICP covariance handles the under-constrained corridor/circle cases explicitly [src: Censi ICRA 2007, ieeexplore 4209579] | `valid=false, reason="degenerate"`, or `valid=partial` with the unobservable axis named |
| **Dynamic objects / people** | residual outliers clustered in a sector; fraction of rays with map-distance > 3σ | `valid=false` if inlier fraction < ~0.7; else keep, record `inlier_frac` |
| **Self-occlusion sector (25°)** | known mask; only a problem when it hides the *constraining* wall — shows up as degeneracy above | folds into `degenerate` |
| **Glass / mirrors** | phantom returns behind the wall line, or dropouts; intensity-based glass detection exists but needs reflectivity, and 2D LiDAR "phantom walls" are a documented failure [src: arXiv:2212.08633; PMC8038001] | map-side: mask glass sectors once; scan-side: `reason="glass_sector"` |
| **Mast tilt ≠ level / lift ≠ mapping height** | read from rig state at scan time; the map is a horizontal slice at ~1.1 m, a tilted plane intersects the room differently | `valid=false, reason="mast_state"` unless within the tolerance the map was built at |
| **Not actually at rest** (scan started < settle time after stop, or during a ramp) | telemetry: any duty ≠ 0 within [t_scan_start − settle, t_scan_end] | `valid=false, reason="in_motion"` — the most common one; §1.3 |
| **Battery brown-out / LiDAR restart** | scan gaps, revolution period ≠ 100 ms | `reason="sensor"` |

### 1.3 Motion distortion — why in-motion scans are not labels

A spinning 2D LiDAR measures rays sequentially; ICP assumes them simultaneous, so a revolution taken while translating at *v* is skewed by *v·T_rev* between first and last ray, and while yawing at *ω* by *ω·T_rev* [src: Hong/Ko/Kim VICP, ICRA 2010, ieeexplore 5509312] — *demoed*. At 10 Hz (T_rev = 0.1 s):

| Motion | Skew across one revolution | Verdict vs. a ~3 mm relative-label budget |
|---|---|---|
| 0.05 m/s creep | 5 mm | marginal |
| **0.15 m/s** (our nominal) | **15 mm** | not labellable rigidly |
| 30°/s yaw | 3° | not labellable |

Deskewing needs a velocity estimate for the revolution — VICP estimates it inside the ICP loop, Cartographer/LOAM from odometry/IMU — but on this rig the velocity *is the unknown* (no encoders, no IMU), so deskewing with the open-loop model and then fitting the open-loop model to the result is circular. Rule: **label only rest scans; require ≥ 1 full revolution after the last duty→0 plus a settle margin (recommend 300 ms: a 110 g LiDAR on a 1.1 m mast sways after a stop).** In-motion scans stay in the log for later (encoders arrive → deskew becomes legitimate).

### 1.4 Per-label uncertainty, and validating the labeller

- Attach a 3×3 covariance per label: Censi closed-form ICP covariance (accounts for correspondence dependence and under-constraint) [src: Censi 2007], or, cheaper and already in hand, the certified-seat metric + Hessian eigenvalues from the existing degeneracy test.
- **Validate the labeller once, cheaply:** (i) re-label the *same* rest scan from 10 perturbed initial guesses → spread must be ≪ claimed σ; (ii) return-to-start episodes (closed loops) → Σ Δlabels must close to ~mm; (iii) Censi's consistency check — split logs into subsets and require calibration estimates to agree within the CRB-derived bounds [src: Censi 2013]. This is the honest-validation standard the project already holds itself to (memory `dont-overstate-accuracy-honest-validation`).
- KITTI dropped its 5–50 m evaluation segments in 2013 because GPS ground-truth error dominated short segments and biased the numbers [src: cvlibs.net/datasets/kitti/eval_odometry.php]. Same logic here: with a ~3 mm relative-label σ, a 0.1 m move has 3 % label noise; **prefer 0.5–1 m moves (or aggregate) for the speed-law fit**, and store label σ so the fitter can weight.

---

## 2. Conventions worth copying at small scale

- **Metrics:** ATE (global, after alignment) and RPE (relative, per segment length) from the TUM RGB-D benchmark [src: Sturm et al. IROS 2012, cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf]; KITTI's per-segment relative translation (%) and rotation (°/m) over fixed lengths [src: cvlibs KITTI odometry]. For us: **RPE per move** is the primary; ATE over an episode is the sanity check. `evo` (MichaelGrupp/evo) consumes TUM-format `t x y z qx qy qz qw` text files — emit that from the label table for free tooling.
- **Ground-truth accuracy hierarchy** (for calibrating expectations): EuRoC uses a Leica MS50 laser tracker (1 mm, 20 Hz) and Vicon (sub-mm/deg, 100 Hz) [src: Burri et al. IJRR 2016, doi:10.1177/0278364915620033]; the learned wheel-odometry paper below settles for a RealSense T265 (< 1 % drift over a loop) [src: arXiv:2303.11725]. Our derived GT sits between: worse absolute than mocap, comparable relative.
- **Association by timestamp:** TUM associates streams by nearest stamp within a tolerance (20 ms default in its scripts); we do the same host-side after the clock model of §3.
- **On-disk format for a Python-only host** — recommended: one directory per episode, **`events.jsonl`** (every command/ack/telemetry/battery/mast/guard line, one JSON object each, host-stamped) + **`scans.npz`** (arrays: `t_host_start`, `t_host_end`, `t_lidar`, `angles`, `ranges`, `quality`, `rev_idx`) + **`frames/`** (stereo JPEG with host stamp in filename and a `frames.jsonl` index) + **`manifest.json`** (schema version, firmware git sha, host code sha, rig-calibration hash, map id, surface tag, operator notes). Raw episodes are **immutable**; derived labels go to a sibling `labels/<map_id>/<labeller_version>/labels.jsonl`, never into the episode.
- **Alternative — MCAP:** rosbag2's default storage is now MCAP [src: github.com/ros2/rosbag2 rosbag2_storage_mcap], and the `mcap` PyPI library writes JSON-schema channels with no ROS present [src: mcap.dev/guides/python/json] — *shipping*. Worth it only if Foxglove playback is wanted; jsonl+npz is greppable and enough for a few-hundred-line host.

---

## 3. Timestamps and clock sync (host monotonic ↔ ESP32 millis)

- **Offset estimation:** NTP/Cristian-style ping — host sends `P,<seq>` at t1, ESP32 replies with its millis t2 (=t3), host receives at t4; offset ≈ t4 − (t3 + RTT/2), error ≤ half the asymmetry of the two legs [src: arXiv:1709.08296 §sync model; Cristian's algorithm]. Do **50 pings at episode start and end**, keep the **minimum-RTT** samples (least queueing), fit **offset + drift** (a line) across the session — crystal drift is tens of ppm, i.e. tens of ms per hour, so a single offset is not enough for a 30-min session (*claimed*, typical crystal spec; measure it — the fit gives it for free). USB-CDC RTTs are ~1–5 ms, so offset error ≲ 2 ms.
- **Cross-check by motion:** the camera↔LiDAR δt on this rig (−562…−580 ms) was recovered by cross-correlating motion signals, not from stamps [[camera-lidar-temporal-calibration-and-pose-interpolation]]. Same trick host↔ESP32: correlate duty-onset edges with the first LiDAR scan that shows motion blur/rest-residual jump.
- **Log both ends of every command:** `t_host_send`, `t_esp_rx` (ESP millis in the ack), `t_esp_applied` (when the PWM actually changed, after any ramp), `t_esp_done`, `t_host_ack_rx`. Command latency is then measured, not assumed.
- **LiDAR revolution stamps:** the SDK delivers per-revolution packets; stamp `t_host_start` at first-ray receipt and `t_host_end` at the last, and keep the revolution counter. Serial buffering makes the host stamp late by a bounded amount — the ping RTT distribution bounds it.
- **What a 50 ms misalignment costs** (arithmetic): at 0.15 m/s → **7.5 mm**; at 30°/s → **1.5°**. Both are the same size as the odometry noise being modelled (1σ ≈ 1 cm / 0.5 m; ±2.3° at 90°), so the timing budget must be **≤ 10 ms** (1.5 mm, 0.3°) to be negligible. The "Syncline" analysis formalises the same point — time-sync error maps directly into fusion error in proportion to velocity [src: arXiv:2209.01136]. **Rest-to-rest labels sidestep this entirely** (only *which* rest scan brackets the move matters, and that is unambiguous at 100 ms per revolution) — another reason the move is the unit.

---

## 4. How much data

| Target | Evidence from the literature | Translated to this rig |
|---|---|---|
| **Systematic (few-parameter) calibration** | UMBmark: 4 m square, **5 runs CW + 5 runs CCW**, endpoint error measured; bidirectional runs are what separates the compensating error sources [src: Borenstein & Feng 1995/96, umbmark.pdf]. Censi: canonical inputs (straight, spin, one-wheel) pieced into closed loops so the robot runs unattended; **~3500 scan-match samples per subset, 3 subsets per configuration**, agreement across subsets checked against the CRB [src: Censi 2013]. Omni/mecanum-class: **36 straight + curved trajectories** (flower pattern) gave 82 % endpoint-error reduction on a 3-wheel omni [src: Palacín et al. Appl. Sci. 2022 12(5):2606] | Our affine speed law per axis: 2 params × (fwd, back, strafe-L, strafe-R) + rotation = ~10 params. For a 1 % slope on a 0.15 m/s law, with per-move σ ≈ 1 cm ⊕ label σ ≈ 0.3 cm and move durations spread over 1–6 s, SE(slope) = σ/(√n·sd(t)) → **n ≈ 40 moves per (direction × duty) cell**; rotations: (2.3°/0.5°)² ≈ **20 per direction**. One surface, 4 directions × 2 duties + 2 rotation directions ≈ **400 moves ≈ 1–1.5 h** at ~10 s/move incl. settle+scan. Diminishing returns past ~60/cell unless a new *condition* (surface, voltage band) is added. |
| **Learned corrector** | Attention-net wheel-odometry corrector on a Jackal: 156,579 training samples at 25 Hz (**~104 min**) random teleop + 61,456 test samples (**~41 min**) of adversarial motions (tight curves, hard braking, spins), GT = T265, batch 32; **60 % m-ATE and 42–76 % segment-error improvement** over the EKF [src: arXiv:2303.11725] — *demoed*. | Needs *continuous* labels and *continuous* inputs (encoders/IMU at 25 Hz). With stop-and-scan + no encoders we have neither; the learnable object today is the **per-move endpoint residual** (≈ 400 samples, tabular regression on duty, duration, volts, surface) — fine for a GBM/GP, not a sequence net. Defer the sequence learner until Hall encoders ×4 land. |
| **Path diversity** | UMBmark's whole point is both directions; Censi's is exciting every parameter; the Jackal test set deliberately covers the regimes where odometry is worst. | Log: both directions per axis, ≥ 2 duty levels, short and long moves, **battery from full to cutoff within a session** (voltage is a covariate, §5), each surface as its own tag, and a few *combined* moves (translate+rotate) as held-out tests, not training. |

Rule of thumb from the table: **the first 400 rest-bracketed moves on one surface are worth more than any amount of in-motion logging** on this rig.

---

## 5. Log the causes of variance, not just the outcome

| Signal | Why |
|---|---|
| **Commanded vs applied duty per wheel, incl. the ramp profile** (every duty change as an event with ESP millis) | Open-loop distance depends on the integral of the *applied* duty; a ramp of even 100 ms shifts a 1 s move by ~5–10 %. Existing telemetry frame `T,<t_ms>,<ticks×4>,<duty×4>` (repo `src/rover/odom_listener.py`) already carries duty — log every frame, not a summary. |
| **Battery voltage, sampled at move start and end** (and continuously if cheap) | Brushed-DC speed ∝ V·duty; PWM equivalent voltage = V_batt × duty, so speed drifts as the pack sags [src: Adafruit brushed-DC PWM guide; RobotShop PWM fundamentals]. A 3S pack spans ~12.6→11.1 V under load (≈ 12 %) — that is the largest single unmodelled term in "affine speed law". Censi likewise saw 20 mm range drift over 5 min he attributed to battery/temperature [src: Censi 2013]. |
| **Mast tilt + lift state** at every scan | §1.2 validity; also a covariate for centre-of-mass and wheel loading. |
| **Surface tag** (hardwood/tile/carpet/rug edge) per episode, operator-entered | Slip is terrain-dependent; mecanum roller slip is the dominant error source and is not a kinematic constant [src: ResearchGate 220755973; 339267725]. |
| **Guard / deadman / e-stop / brown-out events** | A move cut short by the guard is a *censored* sample — must be excluded or modelled as such, not silently fitted. |
| **Scan-match residuals per rest scan** (RMS, inlier fraction, Hessian eigenvalues, certified-seat score) | The validity flag of §1.2 and a quality covariate; also detects map drift over sessions (furniture moved). |
| **LiDAR revolution period and dropout count** | Sensor health; period ≠ 100 ms flags voltage sag on the 5 V rail. |
| **Camera frames with host stamps, both eyes, during moves** | Not labels now; later, a visual-odometry cross-check of the interpolated in-motion poses, and the only signal that sees people/dynamics. |
| **Operator notes + episode intent** (`calib_straight`, `map_step`, `test_combo`) | Lets the fitter select training vs held-out by intent, not by hindsight. |

---

## Recommendation for this rig — a logging spec

Everything below is host-side Python; one directory per episode; `events.jsonl` is the spine.

| Signal | Rate | Format / fields | Why |
|---|---|---|---|
| Clock sync pings | 50 at episode start, 50 at end, 10 every 5 min | `{"ev":"ping","seq","t_host_send","t_esp_ms","t_host_rx"}` | offset + drift line, ≤ 2 ms; §3 |
| Command | per command | `{"ev":"cmd","id","verb","params","t_host_send"}` | intent + send time |
| Ack / applied / done | per command | `{"ev":"ack","id","t_esp_rx_ms","t_esp_applied_ms","t_esp_done_ms","t_host_rx"}` | measured latency and actual move window |
| ESP telemetry frame | every frame the firmware emits (≥ 20 Hz target) | `{"ev":"tel","t_esp_ms","t_host_rx","duty":[4],"ticks":[4]}` | applied duty ramp; ticks ready for encoders |
| Battery volts | at each cmd start/end + 1 Hz | `{"ev":"vbat","t_esp_ms","v"}` | voltage covariate; §5 |
| Mast state | at each scan start + on change | `{"ev":"mast","t_host","tilt_deg","lift_mm"}` | scan validity; §1.2 |
| LiDAR scan | every revolution (10 Hz), always on | `scans.npz`: `rev_idx, t_host_start, t_host_end, angles, ranges, quality`; plus `{"ev":"scan","rev_idx","t_host_start","t_host_end","n_pts"}` in jsonl | rest scans = labels; in-motion kept for later deskew |
| Stereo frames | during moves ≥ 5 Hz, at rest 1 frame | `frames/<t_host_ns>_{L,R}.jpg` + `frames.jsonl` | VO cross-check later; dynamics |
| Guard / e-stop / deadman | on event | `{"ev":"guard","kind","t_host","t_esp_ms"}` | censoring |
| Rest marker | after every stop: settle 300 ms, then ≥ 1 clean revolution | `{"ev":"rest","rest_id","rev_idx_used","t_host"}` | the labellable anchor; §0 |
| Episode manifest | once | `manifest.json`: `schema_ver, fw_sha, host_sha, calib_hash, map_id, surface, intent, notes, t_host_epoch_ref` | reproducibility, immutability |
| Derived labels (separate tree) | per rest + per move, re-runnable | `labels/<map_id>/<labeller_ver>/labels.jsonl`: `{"rest_id","pose":[x,y,yaw],"cov":[3×3],"valid","reason","inlier_frac","eig":[3],"seat_score"}` and `{"move_id","rest_from","rest_to","dpose","dcov","valid"}` | never mutate raw; labels versioned by map + labeller |

**Collection plan (first campaign, one surface):** 400 rest-bracketed moves as in §4 (4 directions × 2 duties × ~40, plus ~20 rotations each way), run as unattended closed loops in a 2 × 2 m clear patch (Censi's pattern), battery from full to cutoff, mast level. Then run the labeller, the three validation checks of §1.4, and only then fit. Repeat per surface. Do not collect in-motion labels until encoders exist.

---

## What this rig measured (2026-09-15) — prototype feedback

*Source: drone-prototype `eda/EDA216-odometry-labels/FINDING.md` (labels + rung-1 fit on 684 rest-bracketed moves from three EDA215 campaigns, office lane, 2026-09-15). Measured, not claimed.*

- **Labeller that worked = pairwise ICP on consecutive rests**, seeded from the commanded motion, **two independent initialisations that must agree** (2 cm / 2°), rms ≤ 7 cm, inliers ≥ 0.85 → 674 / 684 valid. The §1 design above (register each rest to the *map*, then difference) **failed in practice**: in a near-symmetric 1 × 2.8 m lane a few rests snapped into a 90°/180°-rotated basin *with a 4 mm rms*, giving 10 cm labels and 14° heading sd. A good residual is not a good pose; a relative label must be measured as a relative quantity. Pairwise rms is set by point spacing (3–4 cm), so the gate belongs to the method, not the noise.
- **Encoders vs time, leave-one-episode-out over 490 translations:** ticks **2.19 cm** (`dx = k·mean_ticks`, k = 0.2848 mm/tick) vs the fixed timed model **3.07 cm** (a per-speed affine refit gave no gain, 3.12 cm). Spins: 3.15° from ticks vs 3.9° timed (rate 85 °/s, −16° ramp offset at tank 0.6).
- **Effective mecanum rolling circumference 0.282 m** vs geometric 0.3047 m (**−7 %**): rollers compress and scrub. Use the measured value for odometry, keep the geometric one for the record.
- Straight-move heading walk sd 4.6° is mostly tick asymmetry (residual 1.75°) but with the **opposite sign to differential-drive intuition** — flagged for a controlled test, not explained.
- Battery volts sat at 10.8–11.3 V across all three campaigns → the voltage regressor (§5) has no leverage until a full-pack→cutoff campaign is run.

## Sources

- Censi, Franchi, Marchionni, Oriolo — *Simultaneous Calibration of Odometry and Sensor Parameters for Mobile Robots*, IEEE T-RO 2013 — https://censi.science/pub/research/2012-joint_calibration.pdf (canonical inputs, ~3500 samples/subset, 1 mm scan-match precision, CRB consistency check)
- Censi — *An accurate closed-form estimate of ICP's covariance*, ICRA 2007 — https://ieeexplore.ieee.org/document/4209579/
- Olson — *Real-Time Correlative Scan Matching*, ICRA 2009 — https://april.eecs.umich.edu/pdfs/olson2009icra.pdf
- Zhang, Kaess, Singh — *On degeneracy of optimization-based state estimation problems*, ICRA 2016 — https://doi.org/10.1109/ICRA.2016.7487211
- Hong, Ko, Kim — *VICP: Velocity updating iterative closest point algorithm*, ICRA 2010 — https://ieeexplore.ieee.org/document/5509312/
- 2DLIW-SLAM (AMCL 0.09 m/0.78° vs Cartographer 0.06 m/0.73°, Deutsches Museum) — https://arxiv.org/abs/2404.07644
- *Challenges of Mobile Robots in Motion: … AMCL Using Motion Capture Systems*, Springer 2025 — https://doi.org/10.1007/978-3-031-91463-8_33
- Borenstein & Feng — *UMBmark* — https://www.valentiniweb.com/piermo/robotica/doc/Borenstein/umbmark.pdf
- Palacín, Rubies, Clotet — flower-shaped calibration trajectories, Appl. Sci. 2022 12(5):2606 — https://www.mdpi.com/2076-3417/12/5/2606
- Nazzaro et al. — *Online Learning of Wheel Odometry Correction … Attention-based Neural Network* — https://arxiv.org/abs/2303.11725
- Sturm et al. — *A Benchmark for the Evaluation of RGB-D SLAM Systems* (ATE/RPE), IROS 2012 — https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf
- KITTI odometry evaluation protocol (segment-length change 2013) — https://www.cvlibs.net/datasets/kitti/eval_odometry.php
- Burri et al. — *The EuRoC MAV datasets*, IJRR 2016 — https://doi.org/10.1177/0278364915620033
- `evo` trajectory evaluation — https://github.com/MichaelGrupp/evo
- rosbag2 MCAP default storage — https://github.com/ros2/rosbag2/blob/rolling/rosbag2_storage_mcap/README.md ; MCAP Python JSON writing — https://mcap.dev/guides/python/json
- SLAMTEC RPLIDAR C1 datasheet (5 kHz, 10 Hz, 0.72°) — https://static.generation-robots.com/media/slamtec-rplidar-c1-datasheet.pdf
- Clock offset via request/reply (NTP/Cristian model, RTT/2 asymmetry error) — https://arxiv.org/pdf/1709.08296 ; Syncline model of time-sync impact on fusion — https://arxiv.org/html/2209.01136v2
- Cartographer-glass (2D SLAM in glass environments) — https://arxiv.org/pdf/2212.08633 ; LiDAR glass detection for OGM — https://pmc.ncbi.nlm.nih.gov/articles/PMC8038001/
- Brushed-DC PWM/voltage dependence — https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-and-brushed-dc-motors ; https://community.robotshop.com/blog/show/fundamental-of-pwm-speed-control-for-brushed-dc-motor-1
- Mecanum slip as dominant error — https://www.researchgate.net/publication/220755973 ; https://www.researchgate.net/publication/339267725
- Project facts (repo `drone-prototype`): telemetry frame `src/rover/odom_listener.py`; odometry 1σ ≈ 1 cm / 0.5 m, rotations ±2.3° at 90°; C1 wall RMS 0.10 cm; locked-map bow [[global-alignment-wall-refinement]].
