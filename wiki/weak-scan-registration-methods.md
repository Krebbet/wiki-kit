# Seating Weak-Wall / Rich-Object 2D-LiDAR Scans into a Locked Reference Cloud

How to register a **single 2D-LiDAR scan that sees little usable wall but plenty of furniture/appliance returns** (cabinet, oven, fridge) crisply — to **sub-cm** — into a **locked, trusted reference cloud** (the majority of scans that *did* see ≥2 walls and are already well-seated). Plain wall-ICP fails on these scans: a scan that touches one short, **bowed** wall is **laterally unobservable** (it slides along the wall) and the bow biases the fit; the rich *object* returns carry the missing constraint but classical scan-to-map ICP doesn't preferentially exploit them. This page surveys the methods that *do* seat such scans — ICP variants tuned for asymmetric/locked targets, **degeneracy/observability-aware ICP** (the core mechanism), **global / correspondence-free** registration (FGR, FPFH+RANSAC, TEASER++, 4PCS/Super4PCS, Go-ICP), **object-as-landmark** seating, and **free-DOF** (tilt/height) registration — and recommends what to try first for our case. *(synthesis — assembled from the cited primary sources.)*

> **Read alongside:** [[global-alignment-wall-refinement]] (the *joint, multi-scan* wall-spread refinement — BALM/Eigen-Factors/ELCH; this page is its **single-weak-scan, locked-target** sibling), [[lidar-sfm-map-alignment-methods]] (the asymmetric-trust *warp* problem — GICP covariance trust, robust kernels, self-validation; reuse its §3/§5/§6 machinery here), [[learned-point-cloud-registration]] (ICP/GICP/NDT baselines + why classical still wins), [[2d-lidar-slam]] (the pose-graph back-end), [[trajectory-refinement-and-fusion]] (the trajectory-side twin).

---

## 0. Framing: what makes these scans hard, stated precisely

A scan that sees **2+ non-parallel walls** is **fully constrained in SE(2)** — two independent line normals pin both translation axes and the heading; it locks crisply and joins the trusted reference. A scan that sees **one short/bowed wall** is **rank-deficient**: the wall's normal constrains the *across-wall* offset and (weakly) the heading, but leaves the *along-wall* translation **unobservable**. Wall-only ICP then **slides** the scan freely along that direction and converges to whatever the noise/bow nudges it toward — the classic **degenerate geometry** failure [src: arxiv-2410.10784, arxiv-2408.11809]. Two compounding problems:

1. **The missing DOF is real, not a tuning issue.** No amount of ICP iteration recovers an unobservable direction; you must *add a constraint* (an object return that the reference also contains) or *detect-and-freeze* the unobservable direction so the solver doesn't move along it.
2. **The bow biases the constrained DOF.** A single wall that is itself a low-frequency bow (project finding: the LiDAR band is a coherent ~2 cm bow, not noise — [[global-alignment-wall-refinement]], memory `lidar-cloud-locally-crisp-band-is-bow`) means even the across-wall offset is fit to a curved primitive, so point-to-line ICP seats it a little wrong.

The locked reference changes the problem shape favourably: it is a **fixed, trusted target** (asymmetric trust — never move it, only seat the new scan), and it is **dense and rich** (it contains the same cabinets/appliances the weak scan sees). So the right move is **register the weak scan against the *whole* locked cloud — walls *and* objects — with an observability-aware solver**, not against an extracted wall alone. The object returns supply exactly the along-wall constraint the wall lacks.

---

## 1. ICP family — which variants help, which don't, on a locked target

All ICP variants share the inner loop (find correspondences → solve rigid fit → iterate); they differ in the error metric and robustness. Against a **locked, dense, object-rich** target the ranking shifts from the generic SLAM ranking:

| Variant | Metric | Why it helps (or not) for a weak-wall/rich-object scan vs locked cloud | Failure mode |
|---|---|---|---|
| **Point-to-point ICP** | source pt → nearest target pt | Baseline. Uses *all* returns including objects, so it does pick up object constraints — but isotropic distance lets it still slide along a wall and is slow to converge. | Slides on the unobservable DOF; sensitive to partial overlap / object clutter the reference lacks. |
| **Point-to-plane ICP** | source pt → target tangent **plane/line** | More stable and faster on planar/2.5-D structure; consistently beats point-to-point in structured indoor scenes [src: arxiv-2507-17531, learnopencv-icp]. On a 2D wall it pins the across-wall DOF well. | **By itself makes the slide WORSE** on a single wall — it actively frees motion *along* the line (zero residual there), so objects must supply the other axis. Use it *with* object returns, never on the wall alone. |
| **Generalized-ICP (GICP / plane-to-plane)** — Segal, Malik, Thrun, RSS 2009 | covariance-weighted (Mahalanobis) plane-to-plane | **Best single classical pick.** Per-point covariances are the **asymmetric-trust + anisotropy knob**: tight covariances on crisp object faces (trust them to pin the slide), loose/anisotropic covariances along the bowed wall (let it slide *there*, where it's uninformative). Robust to density variation and imperfect correspondences. [src: rss05-gicp, wiki-hanzheteng-gicp] | Still needs *some* non-parallel structure (an object face transverse to the wall) to be observable; covariance mis-set can over-trust the bow. |
| **Trimmed / robust ICP (Tr-ICP, coarse-to-fine trimmed GICP)** | best-overlap fraction + robust kernel (Huber/Tukey/Cauchy/GNC) | **Essential** here: the weak scan sees objects the reference *does* contain but also clutter/moved items it doesn't; trimming + robust kernels reject the non-overlapping tail automatically without hand-segmentation, strong for **low-overlap** seating. [src: ieee-9007699-trimmed-gicp] | Over-aggressive trim → throws away the very object points that carry the constraint → degenerate slide returns. Bound the trim ratio. |
| **Symmetric ICP** — Rusinkiewicz, SGP 2019 (a "Symmetric Objective Function for ICP") | residual symmetric in both surfaces' normals | Wider convergence basin and less bias on curved/edge structure than point-to-plane — useful against the **bowed** wall and rounded appliances where one-sided point-to-plane is biased. [src: rusinkiewicz-symmetric-icp] | A polish/accuracy gain, not a fix for unobservability — still needs object constraints for the slide. |
| **NDT (Normal Distributions Transform)** — Biber & Straßer 2003 (2D, native) | likelihood vs per-cell Gaussians | Correspondence-free, **more robust to a poor initial pose** than ICP and naturally represents the surface as a smooth field; 2D-NDT is the original formulation, directly applicable to our planar scans. [src: semanticscholar-ndt-biber, ndt2d-github] | Cell discretization can blur thin object faces; still rank-deficient on a single wall (the field is flat along it). Good *coarse* seat, hand off to GICP to polish. |

**Takeaway:** the ICP-family answer for our case is **GICP with per-point anisotropic covariances + a bounded robust-trim, run against the whole locked cloud (walls + objects)** — and crucially **observability-aware** (§2), so the solver never moves along the wall-slide direction on its own.

---

## 2. Degeneracy / observability-aware ICP — *the* core mechanism for weak scans

This is the most important and most directly applicable family, and the one the existing wiki pages don't cover. The idea: **detect which DOF the scan actually constrains, and stop the solver from updating the unconstrained ones** (or down-weight them), so a single-wall scan can't slide and a rich-object scan uses its objects to seat the rest.

- **X-ICP — Localizability-Aware LiDAR Registration** (Tuna, Nubert et al., ETH RSL, T-RO 2024). Analyses the **optimization Hessian / constraint-contribution per DOF** to detect *which* translational/rotational directions are well-constrained ("localizable") and which are degenerate, then **constrains the update in the ill-conditioned directions** (or pulls them from a prior) instead of letting ICP drift. Designed for exactly the "geometrically extreme" case where there isn't enough structure in some axis. [src: rg-375903094-xicp, superloc-airlab]
- **LP-ICP — Localizability-aware point-to-line + point-to-plane** (2025). Combines **point-to-line *and* point-to-plane** residuals and runs a localizability analysis on each; the point-to-line term **exploits the richer geometry of edges/corners** — exactly what furniture corners and appliance edges give a 2D scan — to add constraints a plane-only metric misses. Directly the "use the object edges to seat the scan" idea. [src: arxiv-2501.02580]
- **Probabilistic degeneracy detection for point-to-plane** (Nubert et al., 2024). A **principled, threshold-light** test for whether the point-to-plane problem is degenerate along each direction, using the noise model rather than a hand-tuned eigenvalue cutoff (eigenvalue thresholds "lack generalizability across sensors/environments"). Tells you *honestly* when a scan is unobservable and by how much. [src: arxiv-2410.10784]
- **Field analysis of degeneracy-aware registration** ("Informed, Constrained, Aligned", 2024) — a practical survey of how to *inform* (detect), *constrain* (freeze/prior the bad DOF), and *align* in the wild; good recipe-level guidance for wiring this in. [src: arxiv-2408.11809]

**How it applies to us, concretely.** Build the point-to-plane/line Hessian `H = Σ aᵢaᵢᵀ` over the weak scan's correspondences to the locked cloud (`aᵢ` = the per-correspondence Jacobian row). Eigen-decompose `H`: a near-zero eigenvalue's eigenvector **is** the slide direction. Then either (a) **freeze** that DOF (project the update to the well-conditioned subspace — X-ICP style), or (b) **soft-prior** it from the trusted neighbouring scans / trajectory. The object returns are what *raise* the small eigenvalue (an appliance face transverse to the wall adds a normal in the slide direction) — so this framework also tells you, per scan, **whether the objects are enough to seat it** before you trust the result. This is the principled version of the project's `scan-to-consensus seat` finding (single-face scans seatable, corner-scans under-determined — memory `scan-to-consensus-seat-and-misaligned-tail`).

**Cost to try:** low. The Hessian/eigen-analysis is ~20 lines of numpy on top of any ICP you already have (scipy `linalg.eigh`); no new dependency. **Highest value-per-hour on this list.**

---

## 3. Global / correspondence-free registration — when there's no initial pose, or ICP keeps sliding into the wrong basin

If a weak scan's prior pose is poor (or you want a pose **independent of the drifting trajectory** to seat it from scratch), a global method finds a coarse pose without initialization. All of these would then hand off to GICP (§1) to polish to sub-cm. They shine precisely because **objects give distinctive local geometry** that walls don't.

| Method | Core idea | Fit for our case | Cost-to-try |
|---|---|---|---|
| **FPFH + RANSAC** (Open3D `registration_ransac_based_on_feature_matching`) | Fast Point Feature Histograms describe local geometry; match features, RANSAC for the consistent rigid set. | The workhorse coarse-align. FPFH on **object surfaces** (corners, curved appliance faces) is far more distinctive than on a blank wall → objects drive the match. Standard, well-documented. | Low **if Open3D installed** (it isn't yet in either env — see §6). |
| **FGR — Fast Global Registration** (Zhou, Park, Koltun, ECCV 2016; Open3D native) | Optimizes over **all** FPFH correspondences at once with a robust (Geman-McClure) estimator — **no RANSAC, no initialization**; ~0.2 s, accuracy "comparable with ICP." [src: open3d-fgr] | Strong coarse seat from object features; faster and often better than FPFH+RANSAC. Good default global stage. | Low (Open3D). |
| **TEASER++** (Yang, Shi, Carlone, T-RO 2021; MIT-SPARK) | **Certifiably robust**: graduated non-convexity + truncated least squares; tolerates **>99% outlier** correspondences, runs in ms, **can register without correspondences**, and **certifies global optimality**. Tested with FPFH *and* learned features on scan-matching. [src: arxiv-2001.07715, github-teaserpp] | **Best-in-class for low overlap / mostly-wrong matches** — exactly the weak-scan regime where most FPFH matches are junk. Python bindings (`teaserpp_python`). Gives a trust certificate, which fits the project's honest-validation stance. | Medium — separate build (C++/pybind), but pip/conda recipes exist. |
| **4PCS / Super4PCS** (Aiger 2008 / Mellado, Aiger, Mitra, SGP 2014) | Match **4-point coplanar congruent bases** between clouds via affine-invariant ratios; **Super4PCS** adds smart indexing for **linear** time. Works at **~25% overlap, 20% outliers**, arbitrary initial pose. [src: ucl-super4pcs, github-super4pcs] | Robust coarse align at **low overlap with no features/normals needed** — useful if FPFH is unreliable on our sparse 2D returns. Open-source C++ (`Super4PCS`), also in PCL. | Medium. |
| **Go-ICP** (Yang, Li, Campbell, Jia, T-PAMI 2016) | **Branch-and-bound over SE(3)** → globally optimal ICP, no initialization. | Guarantees the global optimum but **slow** and still optimizes the *same* objective — so on a genuinely unobservable single-wall scan it finds the global optimum of an *ill-posed* cost (still slides). Use only when overlap is decent but init is unknown. | Medium; rarely worth it over FGR/TEASER here. |
| **Place-recognition / geometric-landmark descriptors** (2D-LiDAR scan-context, geometrical landmark relations) | Pose-invariant signatures of co-occurring landmarks for fast scan→database matching. [src: rg-285989743] | Overkill for seating within one known room, but the *landmark-relation* idea feeds §4. | — |

**Note:** global methods give a **coarse** seat (cm-level), never sub-cm — they are the *initializer* that breaks ICP out of the wrong basin; the crisp seat still comes from GICP + observability-awareness.

---

## 4. Object-as-landmark seating — make the furniture a first-class constraint

Instead of treating object returns as undifferentiated points, **extract each object (cabinet/oven/fridge) as a landmark** and register the weak scan by matching its objects to the *same* objects in the locked reference. This is the most direct exploitation of "rich object content," and the literature supports it for 2D indoor LiDAR.

- **Semantic-feature 2D-LiDAR localization** — extract higher-level features (object/segment instances, corners, vertices) from the 2D scan and match them to a prior map rather than raw points; vertices and corners act as representative feature points in a voxelized map-matching process. [src: rg-362007847]
- **Object-landmark pose-graph relocalization** — detect objects, match to a landmark dictionary, add **object↔object factors** to a pose graph; robust in changing/cluttered indoor environments where raw-scan matching drifts. [src: arxiv-2308.05443, asce-jccee-5301]
- **InstaLoc-style instance matching** — match object **instances** between a scan and a prior map for indoor localization (the 3D analogue; the principle — instances as anchors — transfers to our 2D footprints).

**How it applies to us, concretely.** We already have an object layer in the campaign (cabinet/oven/fridge footprints from the staged-anchor / object-localization EDAs). Treat each appliance footprint as a 2D landmark with a pose/extent in the locked map. For a weak scan: (1) segment its object returns into the same instances; (2) form **point-to-object-edge / centroid correspondences** to the locked landmarks; (3) solve SE(2) (optionally SE(2)+tilt+height, §5) for the scan pose. An appliance that presents **two transverse faces** (e.g. a fridge corner) single-handedly makes the scan fully observable — it supplies *both* the across-wall and along-wall normals the lone wall couldn't. This is the structural fix for the "corner-scans can't seat both faces against walls" finding: **let the objects, not a second wall, be the second constraint.** Pair with the point-to-line localizability term (§2 / LP-ICP) so object **edges** are exploited, not just faces.

**Failure mode:** object association errors (matching the wrong cabinet) inject a confident-but-wrong constraint — gate associations (normal+offset+overlap, the same gate as [[global-alignment-wall-refinement]] §2.2) and use a robust kernel so a bad object match down-weights itself. Moved/clutter objects the reference lacks must be trimmed (§1).

---

## 5. Free-DOF registration — releasing scan-plane tilt + height

The mandate asks whether to **free the scan-plane tilt + height** when seating. The rig has the 2D scan plane ~7 cm above the camera and slightly tilted (memory `rig-lidar-stereo-offset`); a per-scan tilt/height error reprojects the planar scan onto the wrong slice of the 3D room, which *looks like* a lateral/curvature error in 2D. Freeing those DOF can absorb it — **but only when observable**, else it overfits.

- **Observability governs it.** Tilt/height become observable only if the scan sees structure with **vertical variation that the locked 3D reference also constrains** — e.g. an appliance face at known height, a wall whose return-height changes across the scan. A flat single-wall scan **cannot** observe its own tilt/height (the same rank-deficiency as §0, now in the extra DOF). So **gate the extra DOF on the §2 degeneracy test**: free tilt/height only for scans whose Hessian shows those directions are constrained; otherwise hold them at the rig nominal. This is the standard "extra DOF help when observable, overfit when not" result from degeneracy-aware registration [src: arxiv-2408.11809, arxiv-2410.10784] and the self-/online-calibration observability literature ([[camera-calibration-and-self-calibration]]).
- **Parameterize minimally.** Add tilt (1 rotation) + height (1 translation) to the SE(2) pose → a 5-DOF per-scan solve against the *3D* locked cloud (point-to-plane in 3D). Keep a **tight prior at the rig nominal** so the solve only deviates when the data demands (the [[lidar-sfm-map-alignment-methods]] §5 asymmetric/robust-prior pattern). Validate with leave-one-out: freeing tilt/height should *reduce* held-out residual, not just training residual — else it's overfit (memory `dont-overstate-accuracy-honest-validation`).

**Verdict for us:** free tilt/height **per-scan, observability-gated, with a tight nominal prior**, and only after the in-plane seat (§1–4) is solid. Treat it as the *last* refinement, validated by held-out residual.

---

## 6. Practical: libraries available in our envs

| Capability | Library | Status in our envs |
|---|---|---|
| ICP / point-to-plane / GICP / FGR / FPFH+RANSAC / coloured-ICP | **Open3D** | **NOT currently importable** in either `/usr/bin/python3.10` (scipy/sklearn/numpy 1.25) or anaconda (torch 2.12/cv2). Would need `pip install open3d` — pick the env whose numpy ABI matches (Open3D wheels track a numpy major). Verify before relying on it. |
| Hand-rolled ICP / GICP / observability Hessian / NDT-2D | **numpy + scipy** (`scipy.spatial.cKDTree`, `scipy.linalg.eigh`, `scipy.optimize`) | **Available now** in python3.10. The §2 observability-aware GICP is ~100 lines here with **no new dependency** — the recommended first build. 2D-NDT is a small script (ref impl exists [src: ndt2d-github]). |
| TEASER++ (certifiable global) | `teaserpp_python` | Not installed; separate C++/pybind build (conda-forge / source). Medium effort. |
| Super4PCS / 4PCS | `Super4PCS` (C++), or via **PCL** | Not installed; C++ build. |
| FPFH features without Open3D | **PCL** (python-pcl) or compute by hand | Not installed. |
| Robust kernels / GNC, factor graphs (object-landmark pose graph) | scipy.optimize (Huber); GTSAM/g2o if a pose graph is wanted | scipy now; GTSAM is a separate build. |

**Bottom line:** the highest-leverage methods (§1 GICP-with-covariances, §2 observability-aware ICP) are buildable **today in python3.10 with scipy alone**. Open3D/TEASER++ are worth installing only if the scipy prototype shows we need a stronger global initializer.

---

## 7. Recommended to try first — shortlist mapped to the campaign

Ordered by value-per-hour for **our** case (locked reference, weak wall, rich objects, sub-cm goal, scipy-only today):

1. **Observability-aware GICP against the *whole* locked cloud (walls + objects).** §2 + §1. Build the per-correspondence point-to-plane/line Hessian, eigen-detect the slide direction, **freeze or soft-prior** it, and solve the rest with anisotropic per-point covariances + bounded robust-trim. *Why first:* it is the direct fix for the slide, needs **no new dependency** (scipy), and tells you per-scan whether the objects are enough to seat it. **Maps to:** the staged-anchor / scan-seating EDAs (the `scan-to-consensus seat` work) — this is the principled upgrade of that seat. *Cost:* ~½–1 day.
2. **Object-as-landmark seating.** §4. Match the weak scan's cabinet/oven/fridge returns to the *same* locked-map footprints; an appliance corner supplies the second constraint a lone wall can't. *Why:* directly exploits "rich object content"; structurally fixes corner-scans. **Maps to:** the object-localization / footprint-anchor EDAs (reuse the existing object layer as landmarks). *Cost:* ~1 day on top of #1 (reuses the same solver, swaps correspondences).
3. **A global initializer for poorly-prior'd scans — FGR (Open3D) or TEASER++.** §3. Only for scans whose trajectory prior is too far for ICP to latch; objects make FPFH features distinctive enough to drive it. TEASER++ if most correspondences are outliers (very low overlap) and you want a trust certificate. *Why third:* only needed when #1's basin is wrong; requires installing Open3D/TEASER++. **Maps to:** seating scans the trajectory drift placed badly. *Cost:* ½ day + install.
4. **Free tilt + height, observability-gated, tight nominal prior.** §5. The *last* refinement, only for scans whose §2 test shows those DOF are observable, validated by **held-out residual** not training residual. *Why last:* absorbs the rig tilt/height error but overfits if applied blindly. **Maps to:** the pose-refinement EDAs. *Cost:* ½ day.
5. **(Polish / fallback)** Symmetric ICP for the bowed wall + rounded appliances (§1); 2D-NDT as a coarse, init-robust pre-align (§1); robust kernel / GNC everywhere (reuse [[lidar-sfm-map-alignment-methods]] §5).

**Across all:** the locked reference is **never moved** (asymmetric trust); validate every seat with **no-GT self-consistency** — per-scan residual *field* (uniform collapse = real seat; collapse only where DOF were spent = overfit), leave-one-out, and map-crispness — exactly the [[lidar-sfm-map-alignment-methods]] §6 battery, and run the project's standard 4-comparison refinement battery after each test (memory `refinement-comparison-battery`).

---

## Source

| Tag | Work | Venue / Year |
|---|---|---|
| rss05-gicp / wiki-hanzheteng-gicp | Segal, Malik, Thrun — *Generalized-ICP* | RSS 2009 |
| arxiv-2507-17531 | Dannaoui et al. — *When and Where Localization Fails: ICP in Evolving Environments* (point-to-plane > point-to-point) | 2025 |
| ieee-9007699-trimmed-gicp | *A Coarse-to-Fine Generalized-ICP with Trimmed Strategy* (low-overlap) | 2020 |
| rusinkiewicz-symmetric-icp | Rusinkiewicz — *A Symmetric Objective Function for ICP* | SGP 2019 |
| semanticscholar-ndt-biber / ndt2d-github | Biber & Straßer — *The Normal Distributions Transform* (2D NDT); `rsasaki0109/NormalDistributionTransform2D` | 2003 / impl |
| arxiv-2410.10784 | Nubert et al. — *Probabilistic Degeneracy Detection for Point-to-Plane Error Minimization* | 2024 |
| rg-375903094-xicp / superloc-airlab | Tuna, Nubert et al. — *X-ICP: Localizability-Aware LiDAR Registration* | T-RO 2024 |
| arxiv-2501.02580 | *LP-ICP: Localizability-Aware point-to-line + point-to-plane Registration* | 2025 |
| arxiv-2408.11809 | *Informed, Constrained, Aligned: Field Analysis on Degeneracy-aware Registration* | 2024 |
| open3d-fgr | Zhou, Park, Koltun — *Fast Global Registration* (Open3D tutorial) | ECCV 2016 |
| arxiv-2001.07715 / github-teaserpp | Yang, Shi, Carlone — *TEASER: Fast and Certifiable Point Cloud Registration* (MIT-SPARK, >99% outliers, correspondence-free, certifiable) | T-RO 2021 |
| ucl-super4pcs / github-super4pcs | Mellado, Aiger, Mitra — *Super4PCS: Fast Global Pointcloud Registration via Smart Indexing* (~25% overlap) | SGP 2014 |
| (Go-ICP) | Yang, Li, Campbell, Jia — *Go-ICP: Globally Optimal Solution to 3D ICP* | T-PAMI 2016 |
| rg-362007847 | *Localization Through 2D-LiDAR Semantic Features for Indoor Robot* | 2022 |
| arxiv-2308.05443 / asce-jccee-5301 | *Occupancy-Grid→Pose-Graph BIM-based 2D-LiDAR Localization*; *Pose-Graph Relocalization with Object-Landmark Dictionary* | 2023 |
| rg-285989743 | *Large-scale Place Recognition in 2D LiDAR via Geometrical Landmark Relations* | — |
| arxiv-2302.07433 | *A Survey on Global LiDAR Localization* | 2023 |

## Related

- [[global-alignment-wall-refinement]] — the **joint, multi-scan** wall-spread refinement (BALM / Eigen-Factors / ELCH); this page is its **single-weak-scan, locked-target** sibling. Use that one to sharpen *all* walls at once; use this one to *seat a stubborn scan* into an already-locked map.
- [[lidar-sfm-map-alignment-methods]] — asymmetric-trust warp + GICP covariance trust + robust kernels + no-GT self-validation battery; reuse its §3/§5/§6 wholesale here.
- [[learned-point-cloud-registration]] — ICP/GICP/NDT baselines and why classical still beats DL-PCR in deployment.
- [[2d-lidar-slam]] — the pose-graph back-end that produced the locked reference.
- [[trajectory-refinement-and-fusion]] — the trajectory-side twin of this map-side seating problem.
- [[camera-calibration-and-self-calibration]] — observability / degenerate-motion analysis for freeing extra DOF (the §5 tilt/height story).
