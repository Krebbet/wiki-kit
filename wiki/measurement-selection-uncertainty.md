# Measurement Selection & Uncertainty Gating — Deciding Which Sensor Data to Trust

How a SLAM/mapping system decides **which of its own measurements to believe, which to down-weight, which to keep only partially, and which to flag as "I don't know"** — and how it turns that ledger of ignorance into a concrete instruction to *go measure something*. This is the algorithmic form of the project's governing rule ([[robust-evidence-mapping-principle]]) and of the human's guiding principle: *use only good data — select data that aligns well with priors, discover discrepancies, improve uncertainty; the algorithm should identify where information is lacking, determine what needs gathering, gather it, and update the priors.*

The page covers five mechanisms in the order a measurement meets them: (1) **observability / degeneracy detection** — the *pre-trust* test that asks whether the geometry constrains all DoF at all; (2) **measurement selection** — which constraints are worth keeping, by information-theoretic criteria; (3) **robust back-ends** — how the optimizer rejects the bad constraints it was nevertheless handed; (4) **covariance and entropy propagation** — how the system represents what it does *not* know; (5) **validation that avoids self-confirmation** — the guard against our own hard-won false-rescue failure. It closes with a concrete, computable gate set for our 2D-LiDAR pipeline. *(synthesis — assembled from the cited primary sources.)*

> **Read alongside:** [[weak-scan-registration-methods]] (what to *do* with a scan once you've detected it is under-constrained — this page is the *detection and gating* half of that page's *seating* problem), [[robust-evidence-mapping-principle]] (the governing rule this page operationalises), [[trajectory-refinement-and-fusion]] (the back-end that consumes the gated constraints), [[reconciling-competing-signals]] (what to do when two trusted sources disagree), [[lidar-sfm-map-alignment-methods]] (its §6 no-GT self-validation battery is the sibling of §5 here).

## Source

| Tag | Work | Venue / Year |
|---|---|---|
| zhang-icra2016-degeneracy | Zhang, Kaess, Singh — *On Degeneracy of Optimization-based State Estimation Problems* (degeneracy factor + solution remapping) | ICRA 2016 |
| arxiv-2410.10784 | Nubert et al. — *Probabilistic Degeneracy Detection for Point-to-Plane Error Minimization* | 2024 |
| rg-375903094-xicp | Tuna, Nubert, Nava, Khattak, Hutter — *X-ICP: Localizability-Aware LiDAR Registration for Robust Localization in Extreme Environments* (arXiv 2211.16335) | T-RO 2024 |
| arxiv-2408.11809 | *Informed, Constrained, Aligned: A Field Analysis on Degeneracy-aware Point Cloud Registration in the Wild* (TSVD vs inequality constraints vs Tikhonov) | 2024 |
| arxiv-2412.02901-superloc | *SuperLoc: The Key to Robust LiDAR-Inertial Localization Lies in Predicting Alignment Risks* (AirLab) | 2024 |
| arxiv-2608.15532-equivariance | Zhang et al. — *Degenerate in Whose Frame? An Equivariance Condition for Degeneracy Detection in LiDAR Registration* | 2026 |
| arxiv-2501.02580 | *LP-ICP: Localizability-Aware point-to-line + point-to-plane Registration* | 2025 |
| kretzschmar-stachniss-ijrr2012 | Kretzschmar & Stachniss — *Information-Theoretic Compression of Pose Graphs for Laser-Based SLAM* (mutual-information scan selection, Chow–Liu marginalization) | IJRR 2012 |
| khosoussi-reliable-graphs | Khosoussi, Giamou, Sukhatme, Huang, Dissanayake, Kelly — *Reliable Graphs for SLAM* / *Designing Sparse Reliable Pose-Graph SLAM* (arXiv 1611.00889) | IJRR 2019 / WAFR 2016 |
| arxiv-2103.13090-greedy-fs | Jiao, Zhu et al. — *Greedy-Based Feature Selection for Efficient LiDAR SLAM* (stochastic-greedy logDet under a cardinality constraint) | ICRA 2021 |
| zhao-vela-good-features | Zhao & Vela — *Good Feature Selection for Least-Squares Pose Optimization* / *Good feature matching* (Max-logDet submatrix selection, GF-ORB-SLAM2) | IROS 2018 / T-RO 2020 |
| suenderhauf-switchable | Sünderhauf & Protzel — *Switchable Constraints for Robust Pose Graph SLAM* | IROS 2012 |
| agarwal-dcs | Agarwal, Tipaldi, Spinello, Stachniss, Burgard — *Robust Map Optimization using Dynamic Covariance Scaling* | ICRA 2013 |
| olson-agarwal-maxmix | Olson & Agarwal — *Inference on Networks of Mixtures for Robust Robot Mapping* (max-mixtures) | RSS 2012 / IJRR 2013 |
| latif-rrr | Latif, Cadena, Neira — *Realizing, Reversing, Recovering (RRR)* | RSS 2012 / IJRR 2013 |
| icra13-robust-comparison | Sünderhauf & Protzel — *Switchable constraints vs. max-mixture models vs. RRR — a comparison of three approaches to robust pose graph SLAM* | ICRA 2013 |
| arxiv-1909.08605-gnc | Yang, Antonante, Tzoumas, Carlone — *Graduated Non-Convexity for Robust Spatial Perception* (GNC; MIT-SPARK `GNC-and-ADAPT`) | RA-L 2020 |
| mangelson-pcm | Mangelson, Dominic, Eustice, Vasudevan — *Pairwise Consistent Measurement Set Maximization (PCM)*; Forsgren, Kaess, Vasudevan, McLain, Mangelson — *Group-k Consistent Measurement Set Maximization* | ICRA 2018 / IJRR 2024 |
| censi-icpcov | Censi — *An Accurate Closed-Form Estimate of ICP's Covariance* | ICRA 2007 |
| arxiv-1909.05722-icpcov | Brossard, Bonnabel, Barrau — *A New Approach to 3D ICP Covariance Estimation* (`CAOR-MINES-ParisTech/3d-icp-cov`) | RA-L 2020 |
| coral-adolfsson | Adolfsson, Castellano-Quero, Magnusson, Lilienthal, Andreasson — *CorAl: Introspection for Robust Radar and Lidar Perception Using Differential Entropy* (arXiv 2205.05975, 2109.09820) | RAS 2022 / ECMR 2021 |
| mom-kornilova | Kornilova & Ferrer — *Be Your Own Benchmark: No-Reference Trajectory Metric on Registered Point Clouds* (MOM; `map-metrics` pip package) | ECMR 2021 |
| carrillo-uncertainty-criteria | Carrillo, Reid, Castellanos — *On the Comparison of Uncertainty Criteria for Active SLAM*; Carrillo, Latif et al. — *On the Monotonicity of Optimality Criteria during Exploration in Active SLAM* | ICRA 2012 / ICRA 2015 |
| arxiv-2212.11654-activeslam | Placed et al. — *Active SLAM: A Review on Last Decade* | T-RO 2023 |
| fsmi-karaman | Zhang, Henderson, Karaman, Sze — *FSMI: Fast Computation of Shannon Mutual Information for Information-Theoretic Mapping*; Charrow et al. — CSQMI; Julian et al. — Shannon MI for occupancy grids | IJRR 2020 / 2015 / 2014 |
| kerl-keyframe-entropy | Kerl, Sturm, Cremers — dense visual SLAM keyframe selection by **differential-entropy ratio** | IROS 2013 |
| huang-consistency | Huang, Mourikis, Roumeliotis — *Analysis and Improvement of the Consistency of EKF-SLAM*; Bailey et al.; Julier & Uhlmann (inconsistency is always **overconfidence**) | ICRA 2008 / IJRR 2009 |
| grimmett-introspection | Grimmett, Triebel, Paul, Posner — *Introspective Classification for Robot Perception* / *Knowing When We Don't Know* | IJRR 2016 / ICRA 2013 |
| arxiv-2209.15397-kissicp | Vizzo, Guadagnino, Mersch, Wiesmann, Behley, Stachniss — *KISS-ICP: In Defense of Point-to-Point ICP* (adaptive, motion-derived association threshold) | RA-L 2023 |
| cartographer-icra2016 | Hess, Kohler, Rapp, Andor — *Real-Time Loop Closure in 2D LIDAR SLAM* (Huber loss on the pose graph) | ICRA 2016 |

## Related

- [[weak-scan-registration-methods]] — the *treatment* half: once a scan is flagged under-constrained, how to seat it (object-as-landmark, GICP covariance trust, degeneracy-aware ICP). This page decides *whether* to trust; that one decides *how* to fix.
- [[robust-evidence-mapping-principle]] — the governing project rule (keep / noise / **flagged-unknown**); §5–§7 here are its computable form.
- [[trajectory-refinement-and-fusion]] — the pose-graph back-end that consumes gated constraints; its §2 and §6 (over-pruning hazard) are the direct companions to §3 here.
- [[reconciling-competing-signals]] — cross-field fusion when two *trusted* estimates disagree; this page is upstream of it (decide what is trusted first).
- [[lidar-sfm-map-alignment-methods]] — §6 of that page is the no-ground-truth self-validation battery; §5 here is its generalisation and its warning label.
- [[global-alignment-wall-refinement]] — the joint refinement whose objective must **not** be reused as its own validator.
- [[2d-lidar-slam]] — where the constraints come from (scan-to-submap + BBS loop closure + Huber SPA).
- [[point-cloud-denoising-methods]] — point-level evidence gating; this page is its constraint-level sibling.
- [[sfm-error-sources]] — degenerate *motion* (the camera-side twin of degenerate *geometry*).
- [[anchor-map-protocol]] · [[mapping-stack-design]] — where the gated products land.

---

## 0. Framing: three distinct failures, three distinct gates

"Bad data" is not one thing. Our own history contains three different failures that need three different tests, and conflating them is why a single "residual threshold" never worked:

| Failure | What is wrong | Symptom | The test that catches it |
|---|---|---|---|
| **Under-constrained geometry (degeneracy)** | The measurement genuinely does not constrain some DoF — one wall, or two parallel walls. Nothing is *wrong* with the data; the *problem* is rank-deficient. | Solution slides along the unconstrained axis; a large phantom error that looks like a real result. | **Eigen/observability analysis of the information matrix** — §1. Residual will look *fine*; only the spectrum reveals it. |
| **Outlier constraint** | A wrong association / false loop closure — the data is real but the correspondence is not. | One constraint drags the whole graph; a "teleport". | **Robust back-end + consistency-set maximization** — §3. |
| **Over-trusted good constraint** | The measurement is fine but its stated covariance is far too tight, so it out-votes better evidence. | Estimator is *inconsistent*: errors far outside the 1σ bounds it advertises. | **Covariance realism + NEES/NIS** — §4, §5. Standard result: estimator inconsistency is essentially always in the **overconfident** direction [src: huang-consistency]. |

A fourth failure is procedural rather than geometric and is the reason §5 exists: **self-confirmation** — scoring a fix with the metric the fix optimised. A "rescue" that improves the objective is guaranteed to improve the objective; it is not evidence.

**A gate has three outcomes, never two.** Following [[robust-evidence-mapping-principle]]: *trust* (full-rank, consistent), *partial* (trust only the observable subspace — add the constraint with an anisotropic/rank-deficient covariance rather than discarding it), *unknown* (flag; do not silently drop and do not silently keep). The middle bucket is the one most pipelines lose, and it is exactly where our weak scans live.

---

## 1. Observability / degeneracy detection — the test *before* you trust a match

### 1.1 The object of study: the information matrix

Every least-squares registration (ICP point-to-line/plane, NDT, scan-to-submap) linearises to normal equations `H δx = -b` with

```
H = Σᵢ wᵢ Jᵢᵀ Jᵢ          (the information / approximate-Hessian matrix)
```

`H` is the whole story: its **eigenvectors** are the principal directions of the optimisation in state space, and its **eigenvalues** are how stiffly the data resists motion along each. A near-zero eigenvalue means the residual is flat along that eigenvector — the solver will move there for free, driven by noise. In SE(2) `H` is 3×3 (`x, y, θ` — *check the ordering convention in our code before touching this; the project has already lost sessions to a `(θ,x,y)` vs `(x,y,θ)` scramble*).

For a 2D scan, `Jᵢ` for a point-to-line residual is built from the reference line normal `nᵢ` and the lever arm, so `H`'s translational block is `Σ nᵢ nᵢᵀ` — **the spread of matched surface normals**. One wall (all normals parallel) ⇒ rank 1 ⇒ the along-wall translation is unobservable. That is the entire mechanism behind our "slides along the wall" failure, and it is computable in one line without running ICP at all.

### 1.2 Zhang's degeneracy factor and solution remapping (the canonical reference)

Zhang, Kaess & Singh define a **degeneracy factor** as the *stiffness of the solution with respect to disturbances in the constraints*, derived from the eigen-structure of the constraint geometry, and propose **solution remapping**: separate degenerate from well-conditioned directions and **solve only in the well-conditioned directions**, leaving the degenerate directions to be supplied by the prior/other sensors [src: zhang-icra2016-degeneracy]. This is the ancestor of every method below and of the `isDegenerate` branch in the LOAM family. Its weakness is a **fixed eigenvalue threshold** on `λ_min`, which must be re-tuned per sensor, per environment scale, and per point count.

### 1.3 The threshold problem — and three fixes

Naive metrics on `H` and where they break:

| Metric | Definition | Problem |
|---|---|---|
| `λ_min` threshold | smallest eigenvalue below a constant ⇒ degenerate | Scales with point count, weights, environment size, sensor noise — the constant does not transfer [src: arxiv-2410.10784] |
| **Condition number** `κ = λ_max/λ_min` | one scalar for the whole problem | Mixes rotation and translation units; a single scalar cannot say *which* DoF is lost [src: rg-375903094-xicp] |
| `det(H)` (D-optimality) | volume of the information ellipsoid | Same unit-mixing issue; one bad direction is masked by good ones |

Three fixes, in increasing order of quality:

1. **X-ICP (localizability-aware ICP)** — split `H` into rotational and translational blocks so the scale mismatch between radians and metres cannot hide a lost DoF; project the *normalised* point Jacobians onto each eigenvector, filter them by magnitude, and count how many points actually contribute. Classify each axis as **NONE / PARTIAL / FULL** degeneracy — three levels, not binary — then run a **constrained ICP** that enforces controlled updates along weakly-constrained directions. Requires no prior map and no environment-specific tuning [src: rg-375903094-xicp]. `LP-ICP` extends the same idea to the 2D-friendly point-to-**line** residual [src: arxiv-2501.02580].
2. **Probabilistic degeneracy detection (Nubert et al.)** — instead of thresholding the eigenvalue, ask *is the signal in direction `u` bigger than the noise in direction `u`?* Model point and normal noise, propagate to a noise variance on the Hessian, and compute `p_u = P(a_u ≥ s·ξ_u)` — the probability that the true eigenvalue exceeds `s` times the noise; `s = 10` targets ~10 % relative error. Parameters come **from the LiDAR datasheet** (they use σ_point ≈ σ_normal ≈ 1–1.5 cm), set once per platform, not per scene. Mitigation is a **smooth** attenuation rather than Zhang's hard on/off: the pseudo-inverse eigenvalue becomes `λ̂⁺_k = p_k · (1/λ̂_k)`, i.e. Tikhonov regularisation toward a zero prior in degenerate directions. Reported: 0.04 m APE vs 0.57 m for Zhang's hard remapping on a mine dataset [src: arxiv-2410.10784]. **This is the most directly transplantable method for us** — our RPLIDAR noise spec plays exactly the role of their σ.
3. **Frame-equivariance (the subtle trap)** — per-axis binary degeneracy labels are **not frame-independent**. `H` transforms by *congruence* (`H' = Aᵀ H A`), which preserves the nullity and the physical degenerate subspace but **not** the per-axis footprint; moving the body-frame origin by 1 m in a noise-free tunnel changes which axes get flagged. No fixed metric is equivariant; the **point-displacement metric** `M = Σᵢ Jᵢᵀ Jᵢ` (with the rotation column scaled by the lever arm) yields dimensionless, scene-scale-invariant eigenvalues bounded in `[0,1]` and does satisfy the equivariance condition. At realistic extrinsic magnitudes (0.1 m) binary labels flip <0.2 % of the time, but the resulting **pose corrections differ on 44.5–69.5 % of frame pairs**. Recommendation from the paper: **report the degenerate subspace as a twist subspace with dimensionless eigenvalues, not per-axis binary flags** [src: arxiv-2608.15532-equivariance]. Practically for us: normalise `H` before thresholding, and always store the *eigenvector*, not just the flag.

### 1.4 Mitigation: what to do with a detected degeneracy

The largest field study to date compares **TSVD** (truncate the degenerate singular values), **inequality constraints**, and **Tikhonov regularisation** (linear and non-linear) and concludes that **active in-solver mitigation is necessary** — leaning on external odometry or sensor fusion alone is *not* sufficient — and that **soft-constrained** (regularised) approaches beat hard truncation in complex ill-conditioned scenes when the parameters are set by heuristic [src: arxiv-2408.11809]. Combined with Nubert's smooth attenuation, the consensus is clear: **soft > hard**. Do not binary-kill a direction; damp it in proportion to how badly it is observed.

**SuperLoc** pushes the check *earlier*: it evaluates the localizability of the **raw sensor measurements before optimisation**, turning degeneracy detection from a post-hoc Hessian inspection into a *predictive alignment-risk* assessment, with no heuristic thresholds, and actively pulls in a pose prior from another odometry source *before* the failure happens — reporting a 49.7 % accuracy improvement in caves/corridors/staircases [src: arxiv-2412.02901-superloc]. For our offline pipeline the "predictive" framing matters less than the fact that **the normal-spread test is computable from the raw scan without running the fit** — which makes it a cheap pre-screen over all ~1900 keyframes.

---

## 2. Measurement selection — which constraints are worth keeping

Degeneracy detection asks "is this measurement usable?". Selection asks the harder question: "given a budget, which subset of usable measurements should I keep?" The literature answers with **optimal experimental design** criteria on the information matrix.

### 2.1 The criteria

For an estimate with covariance `Σ = H⁻¹` [src: carrillo-uncertainty-criteria, arxiv-2212.11654-activeslam]:

- **A-optimality** — minimise `tr(Σ)`, the average variance.
- **D-optimality** — minimise `det(Σ)` (equivalently maximise `log det H`), the *volume* of the uncertainty ellipsoid.
- **E-optimality** — minimise `λ_max(Σ)`, the worst direction.
- **Shannon entropy** — for a Gaussian, a monotone function of `det Σ`, so closely related to D-opt.

Carrillo, Reid & Castellanos compared these directly and found **D-optimality gives the most useful uncertainty signal**, more so than A-optimality [src: carrillo-uncertainty-criteria]. Two caveats matter to us: (a) **monotonicity** — A-opt and E-opt do not preserve monotonicity in dead-reckoning scenarios unless spatial uncertainties are propagated in a *differential* representation, in which case all of A/D/E-opt and entropy do [src: carrillo-uncertainty-criteria]; (b) all of them collapse a matrix with **mixed units** (m² and rad²) into one scalar, so a well-observed heading can mask a lost translation — the same unit trap as §1.3, and the reason X-ICP splits blocks.

### 2.2 Selecting *scans* — information-theoretic pose-graph compression

Kretzschmar & Stachniss select the **subset of laser scans that maximises the mutual information between the measurements and the map**, discard the rest, and marginalise out the corresponding nodes — using an approximate **Chow–Liu tree** marginalisation to keep the graph sparse instead of filling in a dense clique [src: kretzschmar-stachniss-ijrr2012]. This is the canonical "which scans actually earn their place" algorithm, and it is a direct answer to the human's "if we need a large swath of scans for initialising something, okay" — you take the swath, then keep the informative core and *marginalise* the rest rather than deleting them.

**Note the fill-in trap:** naive marginalisation of a node makes its neighbours densely connected and can turn a sparse graph into an intractable one; the Chow–Liu tree approximation (and later consistent-sparsification / factor-descent work) exists specifically to prevent this.

### 2.3 Selecting *constraints* — graph-theoretic reliability

Khosoussi et al. show the **D-criterion in 2D pose-graph SLAM is closely approximated by the weighted number of spanning trees (tree-connectivity)** of the graph — a purely graph-theoretic quantity that is far cheaper to evaluate than `det H` and **needs no metric knowledge of the trajectory at all**. Tree-connectivity is *monotone log-submodular*, so a plain greedy selection has provable near-optimality guarantees; they give a greedy/convex-relaxation pair for designing sparse but reliable pose graphs under a measurement budget [src: khosoussi-reliable-graphs]. Practical reading for us: **a loop closure that adds a new independent cycle is worth far more than one that parallels an existing cycle** — and you can rank candidates by that *before* computing any covariance.

### 2.4 Selecting *points/features* within a scan

- **Good features / Max-logDet (Zhao & Vela).** Formulate feature selection as **submatrix selection** on the information matrix, preserving its spectral attributes; the `Max-logDet` matrix-revealing metric performs best and is tied directly to the conditioning of the least-squares pose problem. Selection improves pose-tracking *accuracy* while adding little overhead, and ties matching effort to the selection [src: zhao-vela-good-features]. The key counter-intuitive result: **using fewer, better-chosen features is more accurate than using all of them**, because bad features contribute correlated, mis-weighted residuals.
- **Greedy feature selection for LiDAR SLAM (Jiao et al.).** The same idea for LiDAR: a combinatorial optimisation under a cardinality constraint that preserves the information matrix's spectral attributes, solved in real time with a **stochastic-greedy** algorithm — plus a general strategy to **evaluate environmental degeneracy and change the feature count online** to avoid ill-conditioned estimation [src: arxiv-2103.13090-greedy-fs]. That last part is the link between §1 and §2: *degeneracy sets the selection budget*.
- **Keyframe selection by entropy ratio (Kerl et al.).** Compute the **differential-entropy ratio** `α` between the motion estimate from the last keyframe and the current estimate; when `α` exceeds ~0.9, the frame does not meaningfully reduce uncertainty and is not made a keyframe [src: kerl-keyframe-entropy]. A cheap, principled substitute for fixed distance/time keyframe rules.
- **Adaptive association thresholds (KISS-ICP).** Rather than a hand-tuned correspondence distance, estimate the association threshold **online from the observed motion profile / historical motion deviation**. This gives on-par-or-better performance with a *single fixed parameter set* across automotive, UAV, segway, and handheld LiDAR platforms (0.50 % relative translational error on KITTI) [src: arxiv-2209.15397-kissicp]. The transferable lesson: **derive gate thresholds from measured statistics of the run, not from constants**.

---

## 3. Robust back-ends — rejecting the bad constraints you kept anyway

Selection is imperfect, so the optimiser must survive surviving outliers.

| Method | Mechanism | Verdict |
|---|---|---|
| **M-estimators (Huber / Cauchy / Tukey)** | Replace the quadratic with a sub-quadratic loss so large residuals are down-weighted | The cheap baseline; already what Cartographer's SPA uses to survive false loop closures [src: cartographer-icra2016]. Down-weights but never *removes*; a strong outlier still bends the solution. |
| **Switchable constraints (SC)** | Add a per-constraint continuous **switch variable** `s ∈ [0,1]` to the optimisation, with a prior pulling it toward 1; the optimiser turns bad constraints off | In the head-to-head, SC achieved the **smallest mean RMSE across all trials** and a **99.99 % recall rate**, resolving every trial [src: icra13-robust-comparison, suenderhauf-switchable]. Cost: one extra variable per constraint. |
| **Dynamic covariance scaling (DCS)** | Closed-form scaling of each constraint's covariance, derived as the analytic optimum of the SC switch — same effect, no extra variables | Substantial speed-up over SC **without increasing the number of variables**; a single free parameter Φ [src: agarwal-dcs]. **Best effort/benefit ratio.** |
| **Max-mixtures** | Model each constraint as a max of Gaussians (a "correct" narrow one + a "null" wide one), keeping the problem a max-likelihood one solvable with Gauss-Newton | **Best median RMSE**, but a lower recall rate produced bad trajectories on some trials [src: icra13-robust-comparison, olson-agarwal-maxmix]. Great when it works, occasionally catastrophic. |
| **RRR (Realizing, Reversing, Recovering)** | Cluster loop closures topologically, test clusters against the odometry backbone, accept/reject whole clusters | Handles simple datasets, but **discards correct loop closures** on slightly more complex ones [src: icra13-robust-comparison, latif-rrr] — i.e. it over-prunes, our named hazard. |
| **GNC (graduated non-convexity)** | Start from a convex surrogate of the robust cost and *graduate* it toward the true non-convex robust cost, using the Black–Rangarajan duality between robust costs and outlier processes; wraps any non-minimal solver | Robust to **70–80 % outliers**, outperforms RANSAC, more accurate than specialised local solvers and faster than global ones; **minimally tuned** and needs no initial guess [src: arxiv-1909.08605-gnc]. Reference implementation: MIT-SPARK `GNC-and-ADAPT`. **The modern default.** |
| **PCM (pairwise consistent measurement set maximization)** | Build a graph whose nodes are candidate constraints and whose edges join *mutually consistent* pairs (Mahalanobis test on the loop residual); the **maximum clique** is the largest internally consistent set | Significantly outperforms DCS, SCGP and RANSAC; does **not** require a good initialisation or an odometry backbone; real-time via max-clique solvers [src: mangelson-pcm]. Extended to `group-k` consistency over k-uniform hypergraphs. |

**Practical recommendation.** GNC and PCM are complementary and are the two to build on. **PCM is philosophically the closest thing in the literature to our own robust-evidence principle** — it defines reliability as *mutual agreement among measurements*, exactly "what many observations agree on", and returns an explicit consistent set rather than a soft weight. Use **PCM as an admission gate** on loop closures / re-seating hypotheses, then **GNC (or DCS if you want a 20-line change) inside the solver** for whatever survives. Keep Huber as the always-on floor.

**The over-pruning counter-pressure is real and named in the same literature** — RRR's failure mode is discarding *correct* closures [src: icra13-robust-comparison]. Any gate must be reported with the count and the *reason* for every rejection, and re-examined when the rejected set is large: a gate that throws away a third of the data has made a claim about the data that needs its own evidence.

---

## 4. Covariance and entropy — representing what you do *not* know

### 4.1 The pose side, and why ICP covariance lies

`Σ = H⁻¹` (optionally scaled by residual variance) is the standard per-match covariance, and Censi's closed-form ICP covariance is the classic derivation, accounting for wrong convergence, under-constrained situations, and sensor noise [src: censi-icpcov]. **It is systematically over-optimistic.** Closed-form linearised estimates are ill-founded when point re-associations happen at a scale smaller than the actual error — which experiments show is often the case — and point-cloud alignment is known to be **overconfident**: the true error is inconsistent with the reported bounds [src: arxiv-1909.05722-icpcov].

Brossard, Bonnabel & Barrau's reframing is the one to internalise: **"the covariance of ICP" is only meaningful *relative to the initialisation uncertainty*.** ICP's output uncertainty fully depends on how good the initial guess was; a covariance quoted without reference to that is a category error [src: arxiv-1909.05722-icpcov]. Their practical estimator (code: `3d-icp-cov`) samples: perturb the initial pose according to the *prior* uncertainty, re-run the registration, and take the **sample covariance of the converged poses**. For us this is both cheap and directly actionable — it is `N` re-runs of a fit we already have, and it produces a covariance that *includes* the basin-of-attraction effects the closed form misses.

### 4.2 The map side — where the map itself is thin

Pose covariance says where the *trajectory* is weak; it says nothing about where the *map* is missing. That is occupancy entropy:

- **Map entropy** — sum of per-cell Bernoulli entropies over the occupancy grid; cells near `p = 0.5` are the unknown ones. Used directly as the exploration utility in the entropy branch of active SLAM [src: arxiv-2212.11654-activeslam].
- **Shannon mutual information (MI)** between a candidate future measurement and the map (Julian et al.) is the principled "how much would measuring *here* tell me" — but its evaluation is expensive, scaling quadratically in grid resolution and linearly in the range-integration resolution because there is no analytic solution [src: fsmi-karaman].
- **CSQMI** (Cauchy–Schwarz quadratic MI, Charrow et al.) and **FSMI** (Zhang, Henderson, Karaman, Sze) are the fast approximations that made this practical on compute-limited platforms; FSMI computes the gain for all cells in `O(|Θ||M|)` for `|Θ|` beams and `|M|` cells [src: fsmi-karaman].

**Keep two ledgers, not one.** The active-SLAM review draws precisely this distinction: TOED criteria on the **pose-graph covariance** (task-driven) versus **map entropy / KLD** on the occupancy grid (information-driven), and notes information-theoretic approaches are generally *preferred* because TOED requires both pose and map uncertainty as covariance matrices and is expensive [src: arxiv-2212.11654-activeslam]. A joint entropy over trajectory *and* map is the principled combination.

---

## 5. Validation that does not confirm itself — the false-rescue guard

**This is the section our project paid for.** We once "rescued" badly-posed scans by optimising the very metric used to judge the rescue. A fit that improves its own objective is a tautology, not a result. Three families of defence:

### 5.1 Independent (registration-objective-free) alignment metrics

- **CorAl** — compute **differential entropy of the point clouds separately and of the joint cloud**, and compare. A correctly aligned pair has joint entropy consistent with the separate entropies; a misaligned pair has a joint cloud that is *more spread* than its parts. Because the quantity is an entropy of the merged geometry rather than a residual of the fit, **it is independent of whatever objective produced the pose**. Reported up to **98 % accuracy** at classifying alignment error in urban settings and up to **96 %** when trained in a *different* environment, beating prior methods on the ETH LiDAR benchmark and the Oxford/MulRan radar datasets [src: coral-adolfsson]. This is the single best off-the-shelf answer to our false-rescue problem.
- **MME (mean map entropy)** — the older single-cloud entropy metric, and a **cautionary tale**: it "cannot be used as a general alignment quality measure as it is also affected by measurement noise, sample density and environment geometry", and does not generalise across structured and semi-structured environments [src: coral-adolfsson]. It rewards *any* densification or smoothing, including a wrong one that collapses the cloud. **Do not use MME alone as our no-GT score.** CorAl's dual (separate + joint) construction exists precisely to cancel these confounds.
- **MOM (mutually orthogonal metric)** — a **no-reference trajectory metric** computed from the point clouds registered by the trajectory, restricted to a subset of points on **mutually orthogonal surfaces** (with an extraction algorithm provided). It correlates significantly with Relative Pose Error, is validated on CARLA and KITTI, and ships as a pip package (`map-metrics`) [src: mom-kornilova]. The orthogonal-surface restriction is not incidental — it is the same rank-condition insight as §1, used to make the *metric* well-conditioned.

### 5.2 Held-out data and the right kind of cross-validation

- **Held-out constraints.** Fit the pose graph without constraint `c`, then evaluate `c`'s residual. A constraint the optimiser never saw is honest evidence; a constraint it optimised is not.
- **Held-out geometry (our version).** Fit a scan using only the **wall** returns, then score on the **object** returns, and vice versa. Cross-class held-out scoring is nearly free for us and directly tests whether a fix generalises.
- **Block / extrapolation CV, not random CV.** Standing project rule, and it is the statistically correct one here: consecutive scans are strongly correlated, so a random split leaks the answer. Split by contiguous trajectory blocks.
- **Leave-one-out fragility.** Report how much a conclusion moves when a single scan/anchor is removed. Large swings mean the estimate is supported by one observation, i.e. not redundant, i.e. by the project's own principle not yet reliable.

### 5.3 Consistency statistics — NEES / NIS

The right question for a covariance is not "is it small" but "does the observed error match it".

- **NIS** (normalised innovation squared) gates a single measurement: `NIS = νᵀ S⁻¹ ν` against a `χ²` quantile at the measurement's DoF. This is standard association gating — and it is what PCM's pairwise test is doing between constraint pairs [src: mangelson-pcm].
- **NEES** (normalised estimation error squared) validates the *estimator*: `NEES = (x̂-x)ᵀ Σ⁻¹ (x̂-x)`; averaged over `N` independent trials, a consistent 3-DoF estimator gives `mean NEES ≈ 3`, with a 95 % acceptance region of `χ²_{3N}(0.025)/N .. χ²_{3N}(0.975)/N` — for `N = 20` that is roughly **2.0 – 4.2**. Above the band ⇒ overconfident; below ⇒ needlessly conservative.
- **Two warnings.** (i) The classical result is that SLAM estimator inconsistency is essentially *always* overconfidence, traced to orientation uncertainty [src: huang-consistency] — so the prior should be that our covariances are too tight, not too loose. (ii) NIS/NEES are `χ²`-distributed *only for a correctly tuned estimator*, so passing a `χ²` test is necessary, not sufficient; and after **gating**, the accepted-measurement statistics are conditioned on the selection event, so the post-gate NEES need not follow the unconditional `χ²` reference. Do not gate and then validate on the same statistic without accounting for the selection.

### 5.4 Introspection as a learned layer

Where an analytic gate is unavailable, the introspection literature learns one: a classifier's **introspective capacity** is its ability to attach an appropriate confidence to any test case, and introspective models have been demonstrated for stereo depth and visual SLAM specifically to avoid dangerous decisions from confidently-wrong perception [src: grimmett-introspection]. For our pipeline this is a later-stage option (predict "will this scan seat correctly" from cheap scan features, trained on the cases we have adjudicated), not a first move — but it is the natural home for the LLM-judgment pivots the project already uses at ambiguity seams.

---

## 6. From "what we don't know" to "what to measure"

*(Path planning is out of scope here — see the exploration research. This is the selection/uncertainty half of the loop.)*

The closing of the human's loop needs three things, all of which the sections above supply:

1. **A scalar utility over candidate future measurements.** D-optimality on the pose-graph covariance is the recommended pose-side criterion [src: carrillo-uncertainty-criteria]; Shannon MI / CSQMI / FSMI over the occupancy grid is the map-side criterion [src: fsmi-karaman]. Use both, kept separate, and reconcile at the decision rather than by summing incommensurable units [src: arxiv-2212.11654-activeslam].
2. **A direction, not just a magnitude.** This is where §1 pays off twice: the degeneracy eigenvector tells you *which* DoF is unobserved, so the request is not "gather more data near here" but "**gather a measurement whose Jacobian spans direction `u`**" — for a wall-slide, a view of a surface whose normal is *along* the wall (a perpendicular wall, a cabinet face, an appliance edge). Store the eigenvector with every partially-trusted constraint and the query becomes mechanical.
3. **A prior-update rule that records provenance.** Each new measurement either (a) agrees with the prior ⇒ the redundancy raises confidence, (b) disagrees within its stated uncertainty ⇒ ordinary fusion, or (c) disagrees *beyond* both uncertainties ⇒ a genuine discrepancy: neither estimate may be quietly averaged away; flag it and gather more, per [[reconciling-competing-signals]]. Case (c) is the "discovers discrepancies" clause of the guiding principle, and it is precisely the bucket [[robust-evidence-mapping-principle]] insists stays open.

A useful reframing: **degeneracy detection is a next-best-view generator for free.** Every under-constrained scan is a labelled request for a specific measurement. That turns our existing pile of ~2/3-unrescuable corner scans from a liability into a capture list.

---

## 7. Recommended gate set for our pipeline (concrete)

Computed **per scan**, cheapest first, all recorded to a per-scan quality table so that rejections are auditable rather than silent.

**Stage A — raw-scan pre-screen (no fit required).**

| # | Quantity | Gate | Rationale |
|---|---|---|---|
| A1 | Valid return count `n` after the refined-cloud noise mask | `n ≥ 200` (tune from the run's own distribution) | Below this, nothing downstream is meaningful |
| A2 | **Normal-direction spread**: eigenvalues `μ₁ ≥ μ₂` of `Σ nᵢnᵢᵀ` over matched/segmented surface normals | `μ₂/μ₁ ≥ 0.05` ⇒ translationally observable; `< 0.02` ⇒ **rank-1, flag** | Direct 2D form of the translational block of `H`; catches the wall-slide *before* any ICP [src: zhang-icra2016-degeneracy, rg-375903094-xicp] |
| A3 | Modal check on the normal histogram over `[0°,180°)` | ≥2 modes separated by ≥30°, each holding ≥10 % of the normal mass | Human-legible version of A2; also gives the *names* of the constraining surfaces |
| A4 | Angular span / lever arm of returns about the sensor | span ≥ 90° | Guards the rotational block |
| A5 | Yaw rate at scan time | flag `> 25 °/s` | Project finding: turn segments (28–67 °/s) are where the EDA110 refinement injected 11–17 cm — deskew or distrust |

**Stage B — post-fit observability and residual.**

| # | Quantity | Gate | Rationale |
|---|---|---|---|
| B1 | Eigen-decomposition of the **normalised** `H` (point-displacement metric `Σ JᵀJ`, rotation column scaled by lever arm ⇒ dimensionless eigenvalues in `[0,1]`) | store `λ₁,λ₂,λ₃` **and the eigenvectors**; never store a bare per-axis flag | Frame-equivariance: per-axis binary labels are not frame-independent [src: arxiv-2608.15532-equivariance] |
| B2 | **Per-direction SNR probability** `p_u = P(λ_u ≥ 10·σ_u)` with `σ_u` from RPLIDAR point/normal noise (~1–2 cm) | `p_u ≥ 0.95` ⇒ observable; `0.5–0.95` ⇒ **PARTIAL**; `< 0.5` ⇒ **degenerate** | Datasheet-derived, so it transfers across scenes and point counts, unlike a fixed `λ_min` [src: arxiv-2410.10784] |
| B3 | Condition number `κ = λ_max/λ_min` of the normalised `H` | `κ > 30` ⇒ investigate; `κ > 100` ⇒ treat as rank-deficient | Coarse scalar back-stop for B2; report it, don't decide on it alone |
| B4 | Inlier/overlap fraction against the locked map at an **adaptive** association radius (derived from the run's own motion-deviation statistics, KISS-ICP style) | `≥ 0.6`; also require `≥ 100` absolute inliers | Fixed radii don't transfer [src: arxiv-2209.15397-kissicp] |
| B5 | Robust residual (median / MAD of point-to-line distance) | median `≤ 2 cm`, consistent with the measured 2 cm wall band | Necessary but **never sufficient** — a degenerate fit has a *good* residual |

**Stage C — uncertainty, not a point estimate.**

| # | Action |
|---|---|
| C1 | **Do not report `H⁻¹` as the covariance.** Estimate `Σ` by sampling: perturb the initial pose by the prior uncertainty, re-run the fit `N ≈ 20–50` times, take the sample covariance [src: arxiv-1909.05722-icpcov]. Report `Σ` *together with* the initialisation uncertainty it is conditioned on. |
| C2 | If a closed-form `Σ` must be used for speed, **inflate it** and record the inflation factor; calibrate the factor against C1 on a subset. Assume overconfidence is the default error [src: huang-consistency, censi-icpcov]. |
| C3 | For **PARTIAL** scans, emit an **anisotropic / rank-deficient constraint** — huge variance along the degenerate eigenvector, tight along the observed ones — rather than discarding the scan. Soft (Tikhonov-style) damping beats hard truncation [src: arxiv-2408.11809, arxiv-2410.10784]. |

**Stage D — set-level admission and back-end.**

| # | Action |
|---|---|
| D1 | Run **PCM** over the candidate constraint set (pairwise Mahalanobis consistency ⇒ max clique) before optimising; keep the consistent set, and *log the excluded ones with their inconsistency value* [src: mangelson-pcm] |
| D2 | Optimise with **GNC** (or DCS as the low-effort version) over Huber [src: arxiv-1909.08605-gnc, agarwal-dcs] |
| D3 | Rank candidate loop closures / re-seatings by **information gain**: prefer constraints that add an independent cycle (tree-connectivity ↑) over ones that parallel an existing cycle [src: khosoussi-reliable-graphs] |
| D4 | If keeping a swath of scans for initialisation: keep it, then **select by mutual information and marginalise (Chow–Liu) rather than delete** [src: kretzschmar-stachniss-ijrr2012] |

**Stage E — validation (mandatory, and separate from the fit).**

| # | Action |
|---|---|
| E1 | Score every re-seating with **CorAl** (separate vs joint differential entropy) — a metric that is *not* the ICP objective [src: coral-adolfsson] |
| E2 | Add one physically independent check: **free-space / ray consistency** (does the seated scan's rays pass through cells the locked map calls occupied?). Independent of any point-distance objective |
| E3 | **Held-out geometry**: fit on walls, score on objects; and the reverse |
| E4 | **Block CV** over contiguous trajectory segments — never random CV |
| E5 | **NEES** over the adjudicated set: target mean ≈ 3 for SE(2), 95 % band ≈ 2.0–4.2 at `N = 20`. Out of band ⇒ the covariances are wrong, and the gates built on them are wrong |
| E6 | Report **rejection counts and reasons**, and re-examine any gate rejecting a large fraction — the RRR over-pruning failure is the named hazard [src: icra13-robust-comparison] |
| E7 | **Never** use MME (single-cloud entropy) alone as the no-GT score: it is confounded by density, noise and geometry and rewards collapse [src: coral-adolfsson] |

**Disposition, per the three-bucket rule:** `TRUST` (A+B all pass) → into the locked set. `PARTIAL` (B2 says one direction is weak) → into the graph as a rank-deficient constraint, *plus* a logged capture request naming the missing eigenvector. `UNKNOWN` (A2/A3 rank-1, or E-stage disagreement) → flagged, excluded from geometry, **retained in the record** — never silently dropped.

---

## 8. What this does *not* solve (honesty)

- **A gate cannot create information.** A one-wall scan is unobservable along the wall; every method in §1 either detects it, damps it, or asks another sensor for the missing direction. None recovers it. The fix is a *measurement*, not an algorithm.
- **Independent metrics are less independent than they look.** CorAl and free-space consistency are independent of the *ICP objective*, but both still depend on the same point cloud and the same noise mask. They are a much stronger test than self-scoring, not a ground truth. Real GT remains the only settlement.
- **Thresholds in §7 are starting points calibrated from the cited papers and our own measured band (2 cm wall, 0.13–0.20 cm local crispness), not derived constants.** Every one of them should be re-derived from the run's own distributions (the KISS-ICP lesson) and the chosen values recorded with the run.
- **Selection interacts with the estimate it feeds.** Gating changes the statistics of what survives, so post-gate consistency tests are conditioned on the selection event and must be interpreted accordingly. Aggressive gating can manufacture a beautifully consistent estimate of a biased subset — which is the false-rescue failure wearing a different hat.
