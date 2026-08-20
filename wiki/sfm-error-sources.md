# Sources of Error in Monocular / Visual SfM — Why the Camera Path Bows Away from Metric Truth

A diagnostic catalogue of **where monocular Structure-from-Motion (SfM) error comes from**, how each error *manifests*, how to *detect* it, and how to *mitigate / add metric grounding* — written to explain **why our hloc monocular SfM camera path disagrees with the metric 2D-LiDAR trajectory by a smooth, spatially-varying ~13 cm warp** (not random scatter, not a single jump). *(synthesis — assembled from the cited primary sources.)*

This is the **upstream, cause-side** companion to the three reconciliation pages, which assume the warp already exists and ask how to fuse it away:
> **Read alongside:** [[lidar-sfm-map-alignment-methods.md]] (how to *correct* a smooth ~13 cm SfM↔LiDAR warp once you know it's there — the map-side optimizer), [[trajectory-refinement-and-fusion.md]] (the two-trajectory back-end reconciliation), [[reconciling-competing-signals.md]] (cross-field robust fusion + over-pruning guards), [[relocalization-method-bakeoff.md]] (hloc as our camera front-end), [[camera-lidar-temporal-calibration-and-pose-interpolation.md]] (the time-sync / +99° extrinsic tie). **This page tells you which of those corrections is even appropriate** by naming the underlying error.

> **Our rig (what every "relevance" note is judged against).** Hand-held, **no-IMU**, approximate time-sync: SVPRO USB **stereo** (5.76 cm baseline) + 2D LiDAR. The camera path used downstream is **monocular hloc SfM** (SuperPoint+LightGlue → COLMAP-style incremental SfM/BA), Umeyama-aligned into the LiDAR frame (~0.14 m median, +99° mount yaw). The 5.76 cm baseline exists in hardware but the *trajectory* is reconstructed monocularly, so the **monocular error sources below apply in full** unless we actively exploit the stereo baseline (§9).

---

## 0. The one fact that constrains the diagnosis: the warp is *smooth*

A disagreement that is **smooth and low-frequency** (grows along the run, no sharp jumps) is the fingerprint of a **slowly-accumulating, gauge-/scale-type error**, not of a blunder or a mis-association. That single observation rules things in and out:

| Warp signature | Likely cause | Section |
|---|---|---|
| **Smooth bow, grows with path length** | scale drift + low-frequency trajectory deformation | §2, §3 |
| Constant offset + rotation, no growth | pure datum/gauge choice (alignment), benign | §1 |
| Sharp localized jump | mis-association / false loop / teleport (a *blunder* — see [[trajectory-refinement-and-fusion.md]] §2) | not this page |
| Sharp localized offset at a known occluder | **real** sensor difference, not error (scan-plane 7 cm above camera) | §10 |

So our ~13 cm warp is, by its shape, **§1 (gauge) + §2 (scale drift) + §3 (low-frequency deformation)** — amplified by §4–§8 conditions. The rest of the page is the evidence for that and what to do about it.

---

## 1. Gauge / datum freedom — the 7-DOF similarity, and why "origin error" is a fitting trade-off

**What it is.** A monocular SfM reconstruction is determined **only up to a 7-DOF similarity transform**: an arbitrary 3D rotation (3), translation (3), and **scale (1)** can be applied to all cameras and points **without changing the reprojection-error objective at all**. There is no information in the images that pins the absolute origin, orientation, or scale — this is *gauge freedom* (the "datum problem" in photogrammetry). Triggs et al.'s *Bundle Adjustment — A Modern Synthesis* devotes its gauge section to exactly this: the cost is **invariant to the 7-DOF similarity**, so the normal equations are **rank-deficient** by 7 and the solver must *choose* a gauge (a datum) to make the solution unique. [src: triggs-ba] For visual-inertial systems gravity + accelerometer scale removes most of it, leaving a **4-DOF gauge (3D position + yaw)**; **vision-only stays at the full 7 (or, with metric scale somehow supplied, 6).** [src: zhang-gauge-ral18, triggs-ba]

**How it manifests for us.** Our Umeyama/Sim(3) alignment of the SfM path into the LiDAR frame ([[trajectory-refinement-and-fusion.md]] §1) is precisely a **gauge choice**: it picks the 7-DOF similarity that minimizes *squared position error* between the two paths. Crucially:

- **The alignment cannot bend the path — it can only place it.** A rigid similarity has 7 knobs; it sets the global origin/orientation/scale but leaves any *internal* deformation (§3) untouched. So a smooth bow **survives** alignment and shows up as a spatially-varying residual.
- **"Origin error" is a fitting trade-off, not a real fault.** Where you fix the gauge **redistributes** the residual. A least-squares Sim(3) fit (Umeyama) **spreads** the residual to minimize total squared error — so the path looks "off at the origin and off at the end, least-bad in the middle," even though no single point is individually wrong. Anchor the gauge at the start instead and the residual **piles up at the far end** (classic drift look). Anchor it at the end and it piles at the start. **None of these is more "correct"** — they are the same reconstruction viewed under different datums. Triggs: gauge choice is a free modelling decision that changes the *appearance* and the *covariance* of the result, not its intrinsic geometry. [src: triggs-ba] Zhang et al. show empirically that **free-gauge, gauge-fixation, and gauge-prior formulations reach the same minimum cost and accuracy**, differing mainly in covariance and convergence speed — confirming the datum is a representational choice, not an error source. [src: zhang-gauge-ral18]

**How to detect it.** If the LiDAR↔SfM residual *changes character* when you re-anchor the alignment (start-aligned vs end-aligned vs least-squares Sim(3)), the apparent "where the error is" is a **gauge artifact**. The invariant, gauge-free quantities are **relative pose error (RPE)** over short sub-windows and the **internal shape** of the path — report those, not the alignment-dependent absolute offsets. [src: zhang-scaramuzza-2018]

**Mitigation / relevance.** Don't chase "origin error." Fix the gauge **once, deliberately** — anchor to the LiDAR frame (our metric truth) and hold the +99° extrinsic — and then judge everything by gauge-invariant residuals. The smooth warp that *remains* after a sensible gauge fix is the real signal (§2/§3) to correct downstream ([[lidar-sfm-map-alignment-methods.md]]).

---

## 2. Scale drift / scale ambiguity — the prime suspect for a growing smooth warp

**What it is.** A single camera **cannot recover metric scale**: a scene twice as large viewed twice as far away projects to identical images. SfM fixes a *relative* scale from parallax across the sequence, but **errors in the relative scale accumulate along the trajectory** — *scale drift* — "the main bottleneck that prevents monocular systems from attaining accuracy comparable to stereo." [src: chandraker-pami15, mpsfm-cvpr25] Because the error compounds with path length, the reconstruction is **locally fine but globally the wrong size**, and the size error **varies slowly along the path** — i.e. it presents as a **smooth, growing warp**, exactly our signature (§0).

**Conditions that make scale ill-conditioned.** Scale estimation degrades — toward singular — under:
- **Low parallax / small baseline-to-depth ratio** — little triangulation leverage, so scale is weakly observed and drifts fast. "Incremental SfM ... is typically prone to failure in low-parallax scenarios." [src: mpsfm-cvpr25]
- **Near-pure-translation along the viewing direction (forward motion)** — degenerate for scale recovery; "pure translation represents a degenerate case for scale recovery, particularly when motion is very close to pure translation." [src: degenerate-taxonomy] Forward motion is the classic ill-posed VO case. [src: rg-degenerate-motions]
- **Near-planar scenes / dominant single plane** — homography-degenerate; the essential-matrix scale is poorly constrained when points are coplanar (§4). [src: degenerate-taxonomy]

**How it manifests for us.** A hand-held walk through one room is **rich in exactly these bad conditions**: sweeping past blank/low-texture walls (low parallax), walking *toward* a wall (near-forward translation), and large coplanar wall regions (planar degeneracy). Each stretch where parallax is thin lets the local scale drift; the drifts integrate into the smooth bow we see against the metric LiDAR. **This is the most likely single explanation for the ~13 cm warp.**

**How to detect it.** (1) The warp **correlates with arc-length / path integral**, not with absolute position — plot residual vs cumulative distance. (2) The warp is **worse in low-texture / low-parallax segments** — overlay SfM feature density / triangulation angle and check the residual tracks the thin-parallax stretches. (3) A **single global scale factor partially flattens it** (drift is scale that *slowly changes*; a constant scale removes the mean, leaving the slope). (4) Compare to the LiDAR, which **is metric** — the ratio of inter-pose distances LiDAR/SfM trends along the run.

**Mitigation / metric grounding.** Supply a metric reference (§9): the **LiDAR itself is the scale anchor** (use it to set/regularize SfM scale, not the reverse); known-size objects or the ground-plane height (Chandraker's driving fix uses ground-plane geometry) [src: chandraker-pami15]; or the **stereo 5.76 cm baseline** (a metric ruler we already own — §9). Loop closure removes *accumulated* drift where the path revisits a place (§7).

---

## 3. Trajectory drift & low-frequency deformation — locally right, globally bowed

**What it is.** Even setting scale aside, accumulated small pose errors make a reconstruction that is **accurate over any short window but slowly deformed over the whole path** — it "bows." This is the same mechanism as scale drift generalized to all 6 DOF: each pairwise relative pose carries a little error, and integrating a chain of slightly-wrong relative poses produces a **smooth global bend** (low spatial frequency). Bundle adjustment minimizes *reprojection* error globally, which keeps the structure self-consistent but **does not pin the result to any external metric frame** (§1), so a self-consistent reconstruction can still be globally warped relative to reality. [src: triggs-ba, robust-mono-slam]

**Why the warp is *smooth* and not jagged.** BA couples neighbouring cameras through shared 3D points, so the error field is **spatially correlated / band-limited** — neighbouring poses err *together*. The result is a low-frequency deformation (a bow, a slow twist), which is exactly why the correction in [[lidar-sfm-map-alignment-methods.md]] is a **few-DOF spline/GP**, not a per-point field.

**How to detect it.** **RPE stays low** (local accuracy good) while **ATE grows** (global drift) — the textbook drift signature on the Zhang–Scaramuzza metrics. [src: zhang-scaramuzza-2018] If RPE is low everywhere but the path bows against the LiDAR, it's deformation, not blunders.

**Mitigation / relevance.** Anchor to an external metric frame (LiDAR), loop-close (§7), or co-optimize with metric constraints (§9). This is *our* warp's shape; the fix is the smooth, low-DOF trajectory-warp of [[lidar-sfm-map-alignment-methods.md]] §4.

---

## 4. Degenerate motions & configurations — the conditions that *make* §2/§3 bad

**What it is.** Certain motions/scenes make the two-view (and multi-view) geometry **rank-deficient or ambiguous** — "critical configurations" / "critical motion sequences":
- **Pure rotation** (no translation): the fundamental/essential matrix is undefined and **no 3D structure or scale can be triangulated**; only a homography is recoverable. "When the two cameras are related by pure rotation ... [it is] a critical configuration." [src: degenerate-taxonomy, rg-degenerate-motions]
- **Planar scene** (all points coplanar): the fundamental matrix is **not uniquely defined**; homography is preferred, and the F-based scale is unreliable. [src: degenerate-taxonomy]
- **Pure / near-pure translation, forward motion**: degenerate for scale (§2), epipole at the focus of expansion is poorly localized. [src: degenerate-taxonomy, rg-degenerate-motions]
- **Points on a ruled quadric through both camera centres**: classic critical surface — F ambiguous. [src: degenerate-taxonomy]

**How it manifests for us.** A hand-held room sweep routinely **panning** (near-pure rotation while looking around → no parallax, structure briefly unconstrained), **facing a single wall** (planar degeneracy), and **walking toward a wall** (forward translation). Each degenerate stretch is where scale/structure is locally unconstrained and the path is free to drift — **the generators of the §2/§3 smooth warp.** hloc/COLMAP guards some of this (it can prefer homography models and skip ill-conditioned pairs), but residual ill-conditioning still leaks into the trajectory.

**How to detect it.** Flag frames with **small triangulation angles**, **few/short-baseline matches**, or where the SfM solver fell back to a **homography model** / reported high pose covariance. These frames coincide with the warp's worst segments.

**Mitigation / relevance.** Add motion that breaks degeneracy (translate sideways for parallax), use monocular surface/normal priors (MP-SfM tackles low-parallax/planar with learned priors) [src: mpsfm-cvpr25], or — best for us — **let the LiDAR carry geometry through degenerate camera stretches** (it doesn't care about visual parallax), which is the loose-fusion regime of [[lidar-visual-fusion-slam.md]].

---

## 5. Bundle-adjustment behaviour — why low reprojection error ≠ correct metric pose

**What it is.** BA jointly optimizes poses + structure to minimize **reprojection error** via sparse Levenberg–Marquardt. [src: triggs-ba] Two facts matter for diagnosis:
- **Reprojection error is gauge-invariant and metric-blind.** A reconstruction can have **near-zero reprojection error and still be the wrong scale / globally warped**, because the 7-DOF similarity (§1) and slow deformation (§3) **leave reprojection unchanged**. *Low reprojection RMS is necessary but not sufficient for metric accuracy* — it certifies internal photometric consistency, not agreement with reality. This is why "the SfM looks great (sub-pixel reprojection) yet sits 13 cm off the LiDAR" is **not a contradiction**.
- **Local minima & initialization.** BA is non-convex; a poor initialization (common after a degenerate stretch, §4) can settle in a local minimum that is self-consistent but deformed. Gauge handling affects **convergence speed and the covariance**, not the minimum's cost — free-gauge can be slower / rank-deficient-Hessian, gauge-fixation conditions it. [src: zhang-gauge-ral18, triggs-ba]

**How to detect it.** Inspect SfM **reprojection RMS vs LiDAR residual** — if reprojection is low *everywhere* but the LiDAR residual bows, the error is metric/gauge, not a BA failure to converge. Check per-pose **covariance from BA**: high-covariance poses mark where structure was weak (§4).

**Mitigation / relevance.** Don't trust reprojection RMS as a metric-accuracy proxy. Add **metric constraints into the cost** (pose priors / soft constraints from LiDAR — §9) so BA's minimum is pulled toward the metric frame, not just photometric consistency. Hold the gauge (§1) for a well-conditioned Hessian.

---

## 6. Rolling shutter, motion blur, timing / sync — per-frame pose corruption on a hand-held rig

**What it is.** A **rolling-shutter (RS)** sensor exposes rows sequentially, so under motion each row sees a slightly different pose; treating the frame as global-shutter injects a **motion-dependent geometric distortion** that "causes state-of-the-art structure and motion algorithms to fail" and biases ego-motion. [src: rs-dso-eccv18, rs-mvo] **Motion blur** smears features, degrading match localization. **Timing / sync error** between camera and the metric reference assigns a pose to the **wrong instant**, an offset proportional to speed.

**How it manifests for us.** A **hand-held** capture has constant small shake (RS wobble + blur on fast pans) and our sync is only **approximate**:
- RS + blur mostly add **higher-frequency, motion-correlated noise** to per-frame pose — they inflate RPE and feature-match noise, and worsen the degenerate-stretch drift (§4), but are **less likely to be the primary cause of a smooth global bow**.
- **Timing skew, however, *can* look smooth/structured**: a constant time-offset places every SfM pose where the camera was Δt earlier; against the LiDAR this produces a **velocity-dependent, spatially-varying offset** — larger where you moved faster, smaller where you paused. On a variable-speed hand walk this is a **plausible secondary contributor** to a spatially-varying warp, and is **separable** from scale drift because it correlates with **speed**, not arc-length.

**How to detect it.** RS/blur: residual correlates with **angular rate / pan speed** and frame-to-frame intensity smear. Sync: residual correlates with **linear speed** and shifts coherently when you sweep an artificial Δt in the camera↔LiDAR association ([[camera-lidar-temporal-calibration-and-pose-interpolation.md]]) — the offset that minimizes LiDAR↔SfM residual *is* the sync error.

**Mitigation / relevance.** Estimate and remove the **time-offset** (sweep Δt, pick the residual minimum) before blaming scale; continuous-time / spline trajectories natively absorb RS and unsynced sensors [src: rs-dso-eccv18]; capture with gentler motion to cut blur/RS. No IMU means we can't model RS velocity directly — so **timing calibration is the high-value, low-cost fix** here.

---

## 7. Loop closure — the cheapest removal of accumulated drift

**What it is.** Re-observing an earlier place creates a **loop-closure constraint** that ties the drifted current pose back to the past one; pose-graph optimization then **distributes the accumulated error around the loop**, collapsing the smooth drift (§2/§3) into small residuals. It's the standard cure for low-frequency monocular drift. [src: robust-mono-slam]

**Relevance to us.** A single-room walk that **revisits viewpoints** (we re-cross the room) gives loop closures hloc can find. But loop closure removes drift **only on the closed portion** and **only fixes relative geometry, not absolute scale** (a loop can shrink uniformly and still close) — so it tightens the bow but **does not metricize** the path. Pair it with a metric anchor (§9). Note our LiDAR already loop-closes its own graph; the value here is closing the *camera* graph or, equivalently, the cross-sensor ties of [[trajectory-refinement-and-fusion.md]].

---

## 8. (Diagnostic summary) which sources most likely explain *our* 13 cm smooth warp

Ranked by fit to the smooth, growing, spatially-varying signature:

1. **Scale drift (§2)** — *prime suspect.* Smooth + growing + worse in low-parallax stretches is its exact fingerprint; hand-held room sweeps are scale-drift-prone.
2. **Low-frequency trajectory deformation (§3)** — the 6-DOF generalization; co-occurs with scale drift and explains the *shape* (band-limited bow) that justifies a few-DOF correction.
3. **Degenerate motion (§4)** — the *enabling condition* that lets §2/§3 happen (panning, facing walls, forward motion in a small room).
4. **Gauge/alignment artifact (§1)** — explains *where the error appears to sit*; partly cosmetic — re-anchoring moves it. Rule this out first (it's free).
5. **Timing/sync skew (§6)** — plausible *secondary*, separable because it tracks **speed** not arc-length; cheap to test and remove.
6. RS/motion blur (§6) — mostly higher-frequency noise; unlikely the main bow.

**Not this page:** sharp teleports / false loops are *blunders* handled in [[trajectory-refinement-and-fusion.md]]; the 7 cm scan-plane offset is a *real* difference (§10).

---

## 9. Adding metric grounding — the mitigation toolkit (and what fits our no-IMU rig)

| Method | What it fixes | Fit to our rig (stereo 5.76 cm baseline, 2D LiDAR, no IMU, approx sync) |
|---|---|---|
| **Loop closure (§7)** | accumulated drift (relative) | **Yes** where we revisit views; doesn't set absolute scale — pair with an anchor. |
| **IMU / VIO** | scale + gravity → reduces gauge to 4-DOF; absorbs RS via continuous-time | **N/A — we have no IMU.** This is *the* reason monocular error sources hit us in full; noted as the gap, not a fix. [src: zhang-gauge-ral18] |
| **Stereo baseline** | **metric scale directly** (known 5.76 cm) — kills scale ambiguity at the source | **Underused lever.** We reconstruct the *trajectory* monocularly but own a calibrated stereo pair; using stereo depth / a stereo scale constraint would metricize the path and remove §2 at the root. Short baseline ⇒ weak at long range, but excellent for near walls. |
| **Known-scale objects / ground plane** | absolute scale from a measured dimension | Chandraker uses ground-plane height for driving [src: chandraker-pami15]; we can use a tape-measured object or the known room/wall dimensions as a scale prior. |
| **Pose-prior / soft-constrained BA** | pulls BA's minimum toward a metric frame | **Strong fit.** Add **LiDAR poses as soft pose priors** into the SfM/pose-graph cost (the loose-fusion of [[lidar-visual-fusion-slam.md]] / [[trajectory-refinement-and-fusion.md]]) — metricizes without an IMU. |
| **Continuous-time / spline (or GP) trajectory** | RS, unsynced sensors, smooth drift correction | **Strong fit.** Absorbs approximate sync + RS *and* is the right low-DOF parameterization to correct the smooth warp ([[lidar-sfm-map-alignment-methods.md]] §4). [src: rs-dso-eccv18] |
| **Time-offset calibration (§6)** | sync skew | **Cheapest first test.** Sweep Δt in the camera↔LiDAR association, take the residual minimum ([[camera-lidar-temporal-calibration-and-pose-interpolation.md]]). |

**The rig-honest recommendation.** We have **no IMU**, so we lean on the **LiDAR as metric anchor** (scale + pose priors), our **own stereo baseline** (untapped metric scale), and a **continuous-time/few-DOF warp** to absorb sync + smooth drift. That is precisely the toolkit the downstream pages already build — this page's job is to confirm the warp is a *correctable scale/drift error*, not a blunder or a real sensor difference, so those corrections are the right ones.

---

## 10. The guard: some SfM↔LiDAR disagreement is *real*, not error

Not all disagreement is SfM error to be warped away. The **LiDAR scan plane sits ~7 cm above the stereo camera** (project rig finding, `data/calib/rig_geometry.json`), so the LiDAR images walls *behind* against-wall counters the camera never sees — a **true difference of observed quantity**, not a fault. The error-source diagnosis here must be paired with the **over-pruning guard** of [[reconciling-competing-signals.md]] §0 and [[lidar-sfm-map-alignment-methods.md]] §7: distinguish by *pattern* — a **smooth global field** is correctable SfM drift (this page); a **sharp localized offset at a known occluder** is a real difference to **flag, not warp.** Verify before correcting (project debugging discipline).

---

## Sources

- [src: triggs-ba] B. Triggs, P. McLauchlan, R. Hartley, A. Fitzgibbon, *Bundle Adjustment — A Modern Synthesis*, Vision Algorithms Workshop 2000 — gauge/datum freedom (7-DOF similarity, rank-deficient normal equations, inner constraints), reprojection cost, robust cost, sparse LM. https://lear.inrialpes.fr/people/triggs/pubs/Triggs-va99.pdf
- [src: zhang-gauge-ral18] Z. Zhang, G. Gallego, D. Scaramuzza, *On the Comparison of Gauge Freedom Handling in Optimization-Based Visual-Inertial State Estimation*, IEEE RA-L 3(3):2710–2717, 2018 — free-gauge vs gauge-fixation vs gauge-prior; vision-only 7-DOF / VI 4-DOF; same minimum/accuracy, differ in covariance & convergence. https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf
- [src: chandraker-pami15] S. Song, M. Chandraker et al., *High Accuracy Monocular SFM and Scale Correction for Autonomous Driving*, IEEE T-PAMI 2015 — scale drift as the monocular bottleneck; ground-plane scale correction. https://cseweb.ucsd.edu/~mkchandraker/pdf/pami15_monocularsfm.pdf
- [src: mpsfm-cvpr25] *MP-SfM: Monocular Surface Priors for Robust Structure-from-Motion*, CVPR 2025 — incremental SfM failure in low-parallax / low-overlap / high-symmetry; surface/normal priors. https://arxiv.org/abs/2504.20040 · code https://github.com/cvg/mpsfm
- [src: degenerate-taxonomy] *A Taxonomy of Structure-from-Motion Methods* (2025) — critical configurations: pure rotation (F undefined), planar scene (homography preferred), pure/near-pure translation degenerate for scale, ruled-quadric critical surfaces. https://arxiv.org/pdf/2505.15814
- [src: rg-degenerate-motions] *Degenerate motions in visual SLAM* (pure forward motion → ill-posed) — overview figure/discussion. https://www.researchgate.net/figure/Degenerate-motions-in-visual-SLAM-a-Pure-forward-motion-leads-to-an-ill-posed-problem_fig2_258224859
- [src: rs-dso-eccv18] D. Schubert, N. Demmel, V. Usenko, J. Stückler, D. Cremers, *Direct Sparse Odometry with Rolling Shutter*, ECCV 2018 — RS distortion degrades direct VO; continuous-time modelling. https://openaccess.thecvf.com/content_ECCV_2018/papers/David_Schubert_Direct_Sparse_Odometry_ECCV_2018_paper.pdf
- [src: rs-mvo] *Monocular Visual Odometry with a Rolling Shutter Camera*, 2017 (arXiv 1704.07163) — RS produces inaccurate ego-motion; RS-aware essential matrix. https://arxiv.org/abs/1704.07163
- [src: robust-mono-slam] *Robust Monocular SLAM for Egocentric Videos*, 2017 (arXiv 1707.05564) — monocular scale/gauge drift, loop closure for drift removal. https://arxiv.org/pdf/1707.05564
- [src: zhang-scaramuzza-2018] Z. Zhang & D. Scaramuzza, *A Tutorial on Quantitative Trajectory Evaluation for Visual(-Inertial) Odometry*, IROS 2018 — ATE (global) vs RPE (local), Sim(3)/SE(3) alignment; the gauge-invariant metrics to report. https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf
- [src: prototype] drone-prototype: hloc monocular SfM camera path (SuperPoint+LightGlue), Umeyama-aligned to LiDAR (~0.14 m / +99°), the smooth ~13 cm warp; stereo 5.76 cm baseline; scan plane ~7 cm above camera (`data/calib/rig_geometry.json`); no IMU; approximate time-sync.

## Related

- [[lidar-sfm-map-alignment-methods.md]] — how to **correct** the smooth warp this page diagnoses (low-DOF spline/GP, asymmetric-trust BA, ICP/GICP)
- [[trajectory-refinement-and-fusion.md]] — back-end reconciliation of the two trajectories; blunders/teleports (not this page's smooth error)
- [[reconciling-competing-signals.md]] — cross-field robust fusion + the over-pruning guard (real-difference vs error)
- [[lidar-visual-fusion-slam.md]] — loose back-end fusion; LiDAR carries geometry through degenerate camera stretches
- [[relocalization-method-bakeoff.md]] — hloc (SuperPoint+LightGlue) SfM front-end that produces the camera path
- [[camera-lidar-temporal-calibration-and-pose-interpolation.md]] — the time-sync (sweep Δt) and +99° extrinsic — the §6 timing-skew fix
- [[passive-stereo-robustification.md]] — texture/parallax dependence of the visual signal (the §2/§4 low-parallax conditions)
- [[indoor-cluttered-slam.md]] — symmetric-room / planar-wall conditions that drive degeneracy
