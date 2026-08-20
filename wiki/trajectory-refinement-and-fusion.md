# Trajectory Refinement & Fusion (reconciling two pose estimates + joint map/pose refinement)

How to take **two independent trajectory estimates of the *same* motion** and the floor plan, and tighten them into **one mutually-consistent solution** — while **robustly flagging/rejecting the irreconcilable scans/frames without over-pruning** into an unrealistic fit. This is an **offline, local-refinement** problem: good initial estimates already exist, so the tooling is back-end optimization + robust outlier handling, **not** from-scratch SLAM. Sits alongside [[slam]] (concept hub), [[2d-lidar-slam]] (our LiDAR geometry baseline + pose graph), [[lidar-visual-fusion-slam]] (where the two sensors meet — we fuse loosely, at the back-end), [[relocalization-method-bakeoff]] (hloc as the camera path), and [[global-alignment-wall-refinement]] (the wall/floor-plan refinement this trajectory work feeds).

> **Our concrete problem (what this page is judged against).** A handheld, **no-IMU**, consumer-cost rig (2D LiDAR + USB stereo) walked **one room**: ~1900 LiDAR keyframes, ~1050 camera frames. We have **two estimates of the same walk**: (A) a **2D-LiDAR SLAM pose graph** (scan-to-submap ICP + loop closure + Huber pose-graph) and (B) an **hloc monocular SfM camera path** (Umeyama-aligned into the LiDAR frame). They agree to **~0.14 m median position** and a stable **~+99° yaw offset** (the camera↔LiDAR mount yaw — see [[camera-lidar-temporal-calibration-and-pose-interpolation]], and the project *SfM-not-extrinsic* finding: register the camera into the LiDAR frame via hloc-SfM, not a measured yaw extrinsic). They **disagree more in the latter part of the run**, where the LiDAR pose-graph shows **~8 "teleport" artifacts** — rank-deficient scans latching onto parallel walls (a textbook *degenerate-direction* failure, see §6). Goal: (a) one consistent solution over both trajectories + the floor plan; (b) reject the few bad scans/frames **without** over-pruning the good ones into a fit that looks clean but is geometrically false.

---

## 0. The shape of the answer (offline, two good initials)

The problem decomposes into three layers that map cleanly onto mature tooling:

1. **One graph, both estimates as constraints.** Put both trajectories into a **single pose graph / factor graph** and let a back-end optimizer reconcile them. The LiDAR pose-graph edges are already there; the camera SfM path enters as a **second odometry/relative-pose chain** plus the cross-sensor tie constraints. Optimize once (§1, §3).
2. **A robust back-end so the ~8 bad scans switch themselves off** instead of dragging the whole solution. This is the well-studied "robust pose-graph SLAM back-end" literature — switchable constraints, DCS, max-mixtures, GNC, RRR/PCM consistency, robust kernels (§2, §4).
3. **Guard against over-pruning** — the same robust machinery, mis-tuned, will reject *good* constraints and converge to a degenerate (e.g. collapsed-yaw) solution. The literature has explicit guards (§6).

Because we have **good initials and a single small room (~1900 keyframes)**, this is a **batch, offline, single Levenberg–Marquardt/GNC solve** — not incremental SLAM. The incremental machinery (iSAM2) is available but not needed; we want the most accurate batch fixed point, not real-time updates.

---

## 1. Fusing two trajectory estimates of the same motion

The two estimates live in (nearly) the same metric frame after a one-time alignment; the job is to combine them, not to re-survey.

| Method | What it does | How it applies to us |
|---|---|---|
| **Umeyama / Sim(3) alignment** (Umeyama 1991) | Closed-form SVD solve for the SE(3)+scale transform minimizing squared position error between two trajectories. The standard first step for monocular SfM (unknown scale + frame) before comparison or fusion. [src: umeyama-1991, evo-metrics] | **Already our step**: the hloc path is Umeyama-aligned into the LiDAR frame (that's where the ~0.14 m / ~+99° numbers come from). It gives the *initial* registration; it does **not** fuse — it's a rigid global fit that can't bend the camera path to local LiDAR truth. It's the input to the graph, not the answer. |
| **evo-style trajectory evaluation** (Zhang & Scaramuzza 2018; `evo`) | ATE (absolute trajectory error, global consistency, after Sim(3)/SE(3) alignment) and RPE (relative pose error, local drift over sub-intervals). The de-facto VO/SLAM eval toolkit. [src: zhang-scaramuzza-2018, evo-metrics] | **Our measurement + diagnostic tool.** Compute per-segment ATE/RPE between the two estimates: the ~8 teleports show up as **local RPE spikes** in the latter run while early-run RPE stays low. Use it both to *locate* the bad scans and to *score* the fused result against each input (did fusion improve or just average?). |
| **Add both as constraints in one pose graph** (the canonical fusion form) | Treat each estimate as a chain of relative-pose factors in a single graph; add **cross-trajectory tie factors** (camera frame *i* ↔ nearest LiDAR keyframe, through the fixed +99° mount yaw) so the optimizer balances both against each other and the floor plan. This is multi-session / map-merging mechanics applied to two sensors of one walk. [src: g2o, gtsam-intro, mangelson-pcm] | **The core move.** This is *loosely-coupled back-end fusion* — exactly the regime [[lidar-visual-fusion-slam]] argues is right for our no-IMU rig (geometry from LiDAR, camera as a second constraint chain). The camera path *votes* on the latter-run geometry where the LiDAR teleports; weighted by its covariance, it pulls the bad LiDAR poses back without us hand-editing them. |
| **Trajectory averaging / pose-graph merging** (Carlone et al.; multi-session SLAM) | When two estimates of one path exist, merge their graphs and re-optimize rather than picking one; relative-pose averaging on SE(3)/SO(3). | Frames the fusion as "merge two sessions that happen to be the same walk." Justifies one combined optimize over choosing a winner per segment. |

**Key idea for us:** Umeyama is the *initialization*; the *fusion* is one pose graph holding both chains + cross-ties + floor-plan/wall constraints, solved robustly. The +99° yaw is a **fixed, well-measured extrinsic** (project *SfM-not-extrinsic* finding — [[relocalization-method-bakeoff]], [[camera-lidar-temporal-calibration-and-pose-interpolation]]), so the cross-ties are tight, not free parameters.

---

## 2. Robust back-end optimization (so bad scans/false loops switch off)

Plain least-squares is **not robust**: a single false loop closure or teleport edge, squared, can dominate the cost and warp the whole trajectory. The robust-back-end literature replaces or augments the cost so gross outliers are down-weighted or switched off **during** optimization, without front-end perfection.

| Method | Mechanism | Robustness / notes | How it applies to us |
|---|---|---|---|
| **Switchable Constraints (SC)** — Sünderhauf & Protzel, IROS 2012 | Each suspect (loop-closure) factor gets a continuous **switch variable** the optimizer can drive toward 0, deactivating the edge. Topology becomes part of the optimization. | Handles up to **~1000 false loop closures**; foundational. [src: sc-iros2012, sc-project] | Wrap our **loop-closure edges and the cross-trajectory ties** (and optionally the suspect latter-run LiDAR odometry edges) in switches. The ~8 teleport-causing edges get switched off automatically; we read the switch values to *report* which scans were rejected (auditable, not silent). |
| **Dynamic Covariance Scaling (DCS)** — Agarwal et al., ICRA 2013 | Closed-form generalization of SC: scales each edge's information matrix by a factor that shrinks as its residual grows. One extra scalar per edge; **no runtime cost** over LM; more robust to *bad initialization* than SC. [src: dcs-icra2013, dcs-comparison] | **Cheapest first thing to try.** Drop-in over our existing Huber pose graph; one global parameter (Φ). Because it tolerates poor initials, it's forgiving if the teleports made the LiDAR initial locally wrong. |
| **Max-Mixtures** — Olson & Agarwal, RSS 2012 / IJRR 2013 | Model each constraint as a **mixture** (e.g. a tight Gaussian + a wide "null/uniform" component covering the false-positive probability); optimize the max-component. Keeps the problem a Gaussian-per-step LM. [src: maxmix-ijrr2013, sc-comparison] | Lets each loop-closure / cross-tie carry an explicit "this might be a false positive" component — natural for our wall-aliasing loops, which *look* plausible but are wrong. |
| **Graduated Non-Convexity (GNC)** — Yang, Antonante, Tzoumas & Carlone, RA-L 2020 | Solve with a surrogate cost annealed **from convex → the true robust (e.g. Geman-McClure/TLS) cost**, so it finds the robust optimum **without a good initial guess** and without RANSAC. Robust to **70–80% outliers**; available in GTSAM. [src: gnc-ral2020, gnc-code] | **Best-in-class robust solver, and we don't even need its no-initial-guess superpower** — we *have* good initials, so GNC will converge fast and certifiably down-weight the teleport edges. Strong recommendation as the back-end robust kernel; pairs with GTSAM (§3). |
| **RRR (Realizing, Reversing, Recovering)** — Latif, Cadena & Neira, RSS 2012 / IJRR 2013 | **Consistency-based, not down-weighting**: cluster loop closures, run χ² tests of each cluster against odometry and against other clusters; make a **binary** keep/reject and can **undo** a past wrong acceptance. [src: rrr-rss2012, rrr-ijrr2013] | Good for *auditing*: groups our latter-run bad loops and tests them against the (mostly-good) odometry backbone + the camera chain. Binary decisions are easy to report in the diary. Complements DCS/GNC (use one to optimize, RRR-style consistency to explain *why* an edge was dropped). |
| **PCM (Pairwise Consistency Maximization)** — Mangelson et al., ICRA 2018 | Find the **largest pairwise-internally-consistent set** of inter-map measurements via a **max-clique** solve — does **not** assume a good initialization or odometry backbone. Beats DCS/SCGP/RANSAC for map merging. [src: mangelson-pcm] | Directly applicable to vetting the **cross-trajectory tie set** (camera↔LiDAR) as a map-merge problem: keep only the largest mutually-consistent set of ties, discarding the ones the teleports would have created. |
| **Robust kernels (M-estimators)** — Huber, Cauchy, Geman-McClure; **Barron's adaptive loss** (CVPR 2019) | Replace squared residual with a kernel that flattens for large residuals (Huber: quadratic→linear; Cauchy/Geman-McClure: redescending, fully discounts gross outliers). Barron's single loss **generalizes** Charbonnier/Cauchy/Geman-McClure with a continuous shape parameter α that can be **fit/adapted**. [src: barron-cvpr2019, barron-code, triggs-ba] | We **already** use Huber. Huber is mild (never fully discounts) — the teleports may survive it. Stepping to a **redescending** kernel (Cauchy/Geman-McClure) inside GNC fully rejects them; **Barron's loss** lets us *tune robustness on a continuum* (α near 2 = least-squares for the good early run, α→−∞ = Geman-McClure for the suspect latter run) instead of guessing a kernel. |

**The progression that fits us:** start with **DCS** (one-line upgrade over Huber, free), and if the teleports need a harder hand, run **GNC with a Geman-McClure/TLS kernel** in GTSAM. Use **PCM** to vet the cross-sensor ties and **RRR-style χ²** to *explain/report* the rejected scans.

---

## 3. Joint optimization over poses + structure/map (BA & factor graphs)

| Method / tool | What it is | How it applies to us |
|---|---|---|
| **Bundle Adjustment** — Triggs et al., "A Modern Synthesis" 2000 | Jointly optimize camera poses **and** 3D structure to minimize reprojection error; sparse Levenberg–Marquardt exploiting the block (camera/point) structure; covers cost-function/robustness choice and **gauge (datum) freedom**. [src: triggs-ba] | The hloc camera path **came from** an SfM BA already. We don't re-do full BA; we treat the SfM poses as a constraint chain. BA matters as the **conceptual frame**: our fused solve is a *pose-graph* BA (structure marginalized) + floor-plan/wall residuals — and Triggs' gauge-freedom warning explains why we must **fix one frame** (the LiDAR map) and the +99° extrinsic, or the solve drifts. |
| **g2o** — Kümmerle et al., ICRA 2011 | General graph-optimization framework (Gauss-Newton / LM / dogleg) for pose-graph SLAM **and** BA; problems specified in a few lines; built-in robust kernels. [src: g2o] | A ready batch back-end for the combined graph. Has Huber/Cauchy/DCS kernels out of the box. Lighter-weight if we want one offline LM solve over both chains. |
| **GTSAM** (factor graphs) + **iSAM2** — Dellaert; Kaess et al., IJRR 2012 | Factor-graph library; iSAM2 does **incremental** smoothing via the Bayes tree (fluid relinearization, incremental reordering). GTSAM ships **GNC, robust kernels, Sim(3), between-factors**. [src: gtsam-intro, isam2-ijrr2012, gnc-code] | **The recommended back-end.** Express the LiDAR chain, the camera chain, the cross-ties, and floor-plan/wall constraints as factors; solve **batch** (LevenbergMarquardtOptimizer) with a **GNC wrapper** — exactly the robust offline solve we want. **iSAM2's *incremental* feature we deliberately skip** — for a fixed 1900-keyframe offline refinement, a single batch solve is more accurate and simpler. |
| **When local refinement of good initials is the right tool** | If you already have a near-correct trajectory and just need consistency + outlier removal, **batch pose-graph optimization (not SLAM)** is correct: it's a few LM iterations to a fixed point, with robust kernels handling the few bad edges. | **Exactly us.** We are not localizing or building from scratch; we are tightening two good estimates. The right tool is a one-shot robust batch factor-graph solve, which is why GTSAM-batch + GNC (not iSAM2, not RTAB-Map re-run) is the pick. |

---

## 4. Loop-closure detection + geometric verification, gated without over-discarding

The teleports are, in effect, **false constraints from geometric self-similarity** (parallel walls look alike to a 2D scan-matcher). The literature gates such constraints by *consistency*, not by trusting any single match.

- **Geometric verification (RANSAC + inlier count).** The standard second gate after appearance retrieval: confirm a proposed match by fitting a transform and counting inliers; **zero/low inliers ⇒ reject** (see [[slam]] §RANSAC/PnP, [[relocalization-method-bakeoff]]). For our 2D scans, the analog is **scan-match residual + the rank/condition of the ICP normal matrix** — a parallel-wall match is *rank-deficient* (slides freely along the wall), which is detectable (§6). [src: triggs-ba, zhang-degeneracy]
- **Consistency-based gating (RRR, PCM).** Don't gate one loop at a time — accept the **largest mutually-consistent set** (PCM max-clique) or **χ²-consistent clusters** (RRR) against the odometry/camera backbone. Correct loops agree with each other and with the backbone; the ~8 bad ones don't, and get isolated as a small inconsistent minority. [src: rrr-rss2012, mangelson-pcm]
- **Spectral / clustering verification.** Cluster candidate closures and keep the dominant consistent component (the SC/DCS/max-mixtures family does this softly via the optimizer; RRR/PCM does it discretely). [src: sc-comparison, maxmix-ijrr2013]
- **The "don't over-discard" rule built in.** Conservative front-end thresholds reject true loops; the modern answer is to **let the back-end decide** (switchable/DCS/GNC) so a true-but-marginal loop that's *consistent with everything else* is kept, while a confident-looking *inconsistent* loop is dropped. The decision uses **global consistency**, not per-edge confidence. [src: aeros, sc-iros2012]

**For us:** the camera chain is the independent backbone the LiDAR's wall-aliased loops must agree with. A latter-run LiDAR edge that disagrees with the (locally reliable) camera path **and** with the early-run LiDAR is the one to switch off — and we can *name* it in the diary.

---

## 5. LiDAR-visual fusion at the back-end & multi-session alignment

- **Loosely-coupled back-end fusion is our regime** ([[lidar-visual-fusion-slam]]): no IMU ⇒ no tight LVI; the camera contributes a **second constraint chain + loop-closure/relocalization**, joined at the pose-graph back-end where a wall-blind passive-stereo front-end can't corrupt geometry. This whole page is the *mechanics* of that join. [src: gtsam-intro, mangelson-pcm]
- **Multi-session / map-merging alignment** (PCM, multi-session GTSAM/Kimera-Multi lineage): the formal tools for merging two graphs into one frame with robust inter-graph ties. Our "two estimates of one walk" is a degenerate (fully-overlapping) multi-session merge — so the merge tooling applies directly, and the cross-ties are dense rather than sparse. [src: mangelson-pcm, isam2-ijrr2012]
- **Robust-evidence principle** (standing project principle): use the parts many observations agree on; flag the rest unknown. The fused trajectory should be **most confident where both sensors + multiple loops agree** (early run) and should **widen uncertainty / defer to the camera** where the LiDAR aliases (latter run) — which is exactly what a covariance-aware robust solve produces.

---

## 6. The over-pruning hazard (and how the literature guards against it)

Robust estimators that reject too aggressively converge to **clean-looking but degenerate** solutions — e.g. throwing away the latter-run constraints entirely and letting the trajectory **collapse or free-rotate** along the unconstrained direction. Guards on file:

1. **Degeneracy/rank analysis instead of blind rejection** — Zhang, Kaess & Singh, ICRA 2016, *On Degeneracy of Optimization-Based State Estimation*. Detect **degenerate directions** in the problem's information matrix and **only solve in well-conditioned directions** ("solution remapping") — leaving the under-constrained DOF to other evidence rather than fitting noise. [src: zhang-degeneracy] → **Directly our teleport mechanism.** A scan against two parallel walls is rank-deficient *along* the walls. The fix isn't to delete the scan — it's to recognize it constrains only the across-wall direction and let the **camera chain** supply the along-wall DOF. This is the single most on-point guard for us.
2. **Adaptive / continuously-tuned robustness** — Barron's adaptive loss (CVPR 2019) and **AEROS** (Ramezani et al., Front. Robot. AI 2022) adapt the kernel shape **per-edge / online** instead of a fixed hand-tuned threshold, so the optimizer doesn't globally over-flatten and discard good data. [src: barron-cvpr2019, aeros] → Tune robustness *down* on the agreeing early run, *up* on the suspect latter run, on a continuum.
3. **Keep the consistent majority, not the empty set** (PCM max-clique, RRR χ²): these select the **largest** consistent set, structurally preventing collapse to "reject everything" — they keep as much as is mutually consistent. [src: mangelson-pcm, rrr-rss2012]
4. **GNC's annealing** moves from convex (keeps all data) toward robust gradually, so it doesn't prematurely declare inliers as outliers; the convex start is itself an anti-over-pruning guard. [src: gnc-ral2020]
5. **Gauge fixing + a held extrinsic** (Triggs): fix the LiDAR map frame and the +99° mount yaw so the solver can't absorb rejection into a global drift/rotation that hides an unrealistic fit. [src: triggs-ba]
6. **Score against held-out evidence (evo):** after the robust solve, **re-check ATE/RPE against the camera path and against tape-measured GT** ([[relocalization-method-bakeoff]] validated metric scale to −1.9%). If pruning improved residuals but worsened agreement with independent GT, it over-pruned. [src: zhang-scaramuzza-2018, evo-metrics] → **Our acceptance test:** a good fusion lowers latter-run RPE *and* stays consistent with GT; a clean-but-collapsed fit will diverge from GT.

---

## Bottom-line recommendation

Build **one batch factor graph** (GTSAM) holding the LiDAR pose-graph chain, the hloc camera chain, dense **cross-ties through the fixed +99° extrinsic**, and the floor-plan/wall constraints; fix the LiDAR map frame (gauge). Solve **batch** (not iSAM2 — we don't need incremental) with **GNC + a redescending kernel (Geman-McClure/TLS)**; or, as the cheap first cut, **DCS** dropped over the existing Huber graph. Vet the cross-sensor and loop ties with **PCM (max-clique consistency)**; **report** which scans were switched off (switch values / RRR-style χ²) so the diary names the rejected ~8, not silently fits around them. Crucially, treat the teleports as a **degeneracy** (Zhang/Kaess/Singh): the rank-deficient parallel-wall scans constrain only across-wall, so let the **camera chain supply the along-wall DOF** rather than deleting the scans. Guard against over-pruning by keeping the **largest consistent set** (not the empty set), starting GNC convex, and **scoring the result with evo against tape-measured GT** — a good fusion lowers latter-run RPE *and* stays consistent with GT; a clean-but-collapsed fit diverges from GT. *(Honest uncertainty: 2D-scan rank-deficiency detection is less turnkey than the 6-DOF degeneracy literature assumes; if the per-scan condition number is noisy, fall back to letting the camera-chain ties + DCS/GNC down-weight the teleports implicitly.)*

---

## Sources

- [src: umeyama-1991] S. Umeyama, *Least-Squares Estimation of Transformation Parameters Between Two Point Patterns*, IEEE T-PAMI 13(4), 1991 — closed-form SE(3)+scale (Sim(3)) alignment by SVD. https://web.stanford.edu/class/cs273/refs/umeyama.pdf
- [src: zhang-scaramuzza-2018] Z. Zhang & D. Scaramuzza, *A Tutorial on Quantitative Trajectory Evaluation for Visual(-Inertial) Odometry*, IROS 2018 — ATE/RPE, Sim(3) alignment for monocular. https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf
- [src: evo-metrics] M. Grupp, *evo* — Python trajectory evaluation (ATE, RPE, Umeyama/Sim(3) alignment). https://github.com/MichaelGrupp/evo (Metrics wiki: https://github.com/MichaelGrupp/evo/wiki/Metrics )
- [src: sc-iros2012] N. Sünderhauf & P. Protzel, *Switchable Constraints for Robust Pose Graph SLAM*, IROS 2012. https://nikosuenderhauf.github.io/assets/papers/IROS12-switchableConstraints.pdf
- [src: sc-project] N. Sünderhauf, *Switchable Constraints for Robust SLAM* (project page + vertigo code). https://nikosuenderhauf.github.io/projects/switchableConstraints/
- [src: sc-comparison] N. Sünderhauf & P. Protzel, *A Comparison of Three Approaches to Robust Pose Graph SLAM* (SC vs DCS vs max-mixtures), ICRA 2013. https://nikosuenderhauf.github.io/assets/papers/ICRA13-comparisonRobustSLAM.pdf
- [src: dcs-icra2013] P. Agarwal, G. D. Tipaldi, L. Spinello, C. Stachniss, W. Burgard, *Robust Map Optimization using Dynamic Covariance Scaling*, ICRA 2013. http://www2.informatik.uni-freiburg.de/~spinello/agarwalICRA13.pdf
- [src: dcs-comparison] P. Agarwal et al., *Experimental Analysis of Dynamic Covariance Scaling for Robust Map Optimization Under Bad Initial Estimates*, ICRA 2014. http://www2.informatik.uni-freiburg.de/~spinello/agarwalICRA14.pdf
- [src: maxmix-ijrr2013] E. Olson & P. Agarwal, *Inference on Networks of Mixtures for Robust Robot Mapping*, RSS 2012 / IJRR 32(7), 2013. https://april.eecs.umich.edu/pdfs/olson2013ijrr.pdf
- [src: gnc-ral2020] H. Yang, P. Antonante, V. Tzoumas, L. Carlone, *Graduated Non-Convexity for Robust Spatial Perception: From Non-Minimal Solvers to Global Outlier Rejection*, IEEE RA-L 2020 (arXiv 1909.08605). https://arxiv.org/abs/1909.08605
- [src: gnc-code] MIT-SPARK, *GNC-and-ADAPT* reference implementation (GNC is also in GTSAM). https://github.com/MIT-SPARK/GNC-and-ADAPT
- [src: rrr-rss2012] Y. Latif, C. Cadena, J. Neira, *Robust Loop Closing Over Time*, RSS 2012. https://www.roboticsproceedings.org/rss08/p30.pdf
- [src: rrr-ijrr2013] Y. Latif, C. Cadena, J. Neira, *Robust loop closing over time for pose graph SLAM*, IJRR 32(14), 2013 (incremental iRRR). http://webdiis.unizar.es/~ylatif/papers/IJRR.pdf
- [src: mangelson-pcm] J. G. Mangelson, D. Dominic, R. M. Eustice, R. Vasudevan, *Pairwise Consistent Measurement Set Maximization for Robust Multi-Robot Map Merging*, ICRA 2018 (max-clique consistency). https://ieeexplore.ieee.org/document/8460217/
- [src: barron-cvpr2019] J. T. Barron, *A General and Adaptive Robust Loss Function*, CVPR 2019 (arXiv 1701.03077) — generalizes Cauchy/Geman-McClure/Charbonnier with a continuous shape parameter. https://arxiv.org/pdf/1701.03077
- [src: barron-code] J. Barron, *robust_loss_pytorch* / google-research robust_loss. https://github.com/jonbarron/robust_loss_pytorch
- [src: triggs-ba] B. Triggs, P. McLauchlan, R. Hartley, A. Fitzgibbon, *Bundle Adjustment — A Modern Synthesis*, Vision Algorithms Workshop 2000 — joint pose+structure LM, robust cost, gauge freedom. https://lear.inrialpes.fr/people/triggs/pubs/Triggs-va99.pdf
- [src: g2o] R. Kümmerle, G. Grisetti, H. Strasdat, K. Konolige, W. Burgard, *g2o: A General Framework for Graph Optimization*, ICRA 2011. https://cse.sc.edu/~yiannisr/774/2015/g2o.pdf · code https://github.com/RainerKuemmerle/g2o
- [src: gtsam-intro] F. Dellaert, *Factor Graphs and GTSAM: A Hands-on Introduction* (+ gtsam.org tutorial). https://gtsam.org/tutorials/intro.html
- [src: isam2-ijrr2012] M. Kaess, H. Johannsson, R. Roberts, V. Ila, J. Leonard, F. Dellaert, *iSAM2: Incremental Smoothing and Mapping Using the Bayes Tree*, IJRR 31(2), 2012. https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf
- [src: zhang-degeneracy] J. Zhang, M. Kaess, S. Singh, *On Degeneracy of Optimization-Based State Estimation Problems*, ICRA 2016 — degenerate-direction detection + solution remapping. https://www.cs.cmu.edu/~kaess/pub/Zhang16icra.pdf
- [src: aeros] M. Ramezani et al., *AEROS: AdaptivE RObust Least-Squares for Graph-Based SLAM*, Front. Robot. AI 2022 (arXiv 2110.02018) — online adaptive robust kernel. https://arxiv.org/pdf/2110.02018
- [src: prototype] drone-prototype: the LiDAR pose graph (EDA064 lineage, scan-to-submap ICP + loop closure + Huber), hloc SfM camera path Umeyama-aligned to LiDAR (~0.14 m / +99°), the ~8 latter-run teleports — carried via [[2d-lidar-slam]], [[relocalization-method-bakeoff]], [[camera-lidar-temporal-calibration-and-pose-interpolation]] (incl. the SfM-not-extrinsic finding).

## Related

- [[sfm-error-sources.md]] — why the monocular SfM path bows away from metric truth (scale drift / gauge / degenerate motion); the cause-side diagnosis upstream of this reconciliation
- [[slam]] — concept hub: localization + mapping + loop-closure; RANSAC/PnP verification primitives
- [[2d-lidar-slam]] — our LiDAR geometry baseline and the pose graph this refines (ATE 0.024-class)
- [[lidar-visual-fusion-slam]] — where the two sensors meet; why we fuse **loosely at the back-end** (no IMU) — this page is the mechanics of that join
- [[relocalization-method-bakeoff]] — hloc (SuperPoint+LightGlue) as the camera path; validated metric scale (−1.9% vs GT) used as the over-pruning acceptance check
- [[global-alignment-wall-refinement]] — the wall/floor-plan refinement the fused trajectory feeds
- [[camera-lidar-temporal-calibration-and-pose-interpolation]] — the +99° mount-yaw extrinsic the cross-ties run through
- [[indoor-cluttered-slam]] — symmetric-room / parallel-wall aliasing failure modes that cause the teleports
- [[learned-slam]] — learned place-recognition (iBTC) as a complementary loop-closure gate
