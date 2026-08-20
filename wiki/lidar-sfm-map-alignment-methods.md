# LiDAR ↔ SfM Map Alignment & Fusion — the Asymmetric-Trust Warp Problem

How to fuse a **2D-LiDAR map** and a **monocular SfM reconstruction** of the *same room* into **one self-consistent world map**, under an **asymmetric trust model**: the **LiDAR range measurements are rigid and accurate** — only each scan's *placement* (its rigid pose, and optionally tilt/height) may be corrected, never the measured ranges — while the **SfM is the noisy, deformable estimate** that earns only loose/soft constraints and may be *warped* to agree. The two currently disagree by a **smooth ~13 cm warp** (a low-frequency scale/drift field, not random scatter); we want them (a) mutually aligned, (b) more accurate vs reality, and (c) **self-validated** that the fused result is actually better, not just smoother. *(synthesis — assembled from the cited primary sources.)*

> **Read alongside:** [[sfm-error-sources.md]] (the *cause-side* page — **why** the SfM produces this smooth ~13 cm warp: scale drift, gauge freedom, degenerate motion; it tells you this warp is a correctable scale/drift error rather than a blunder, so the corrections here are the right ones), [[trajectory-refinement-and-fusion.md]] (the two-trajectory back-end reconciliation this warp problem is the *map-side* twin of), [[reconciling-competing-signals.md]] (the cross-field robust-fusion / over-pruning framing — LiDAR-rigid vs SfM-soft is exactly its "asymmetric reliability" case), [[lidar-visual-fusion-slam.md]] (where the two sensors meet; we fuse loosely at the back-end), [[stereo-3d-mapping-known-poses.md]] (how the SfM cloud is produced), and [[global-alignment-wall-refinement.md]] (the wall/plane self-consistency objective the fused map feeds into).

---

## 0. Framing: a soft cloud, a rigid cloud, and a low-DOF warp between them

The disagreement is **smooth** (~13 cm, growing through the run — the signature of accumulated SfM **scale drift**, not noise). That single fact dictates the whole solution shape:

- **It is correctable with very few degrees of freedom.** A smooth warp does not need a per-point deformation field; it needs a *low-frequency* correction (a handful of spline/GP control points, or a global similarity + slow gradient). Fitting a high-DOF field to a low-DOF error is the **over-fitting trap** (§7).
- **The trust is asymmetric, so the optimizer must be asymmetric.** The standard symmetric registration objective ("move both clouds to meet in the middle") is *wrong* here — it would corrupt the accurate LiDAR. The LiDAR is the **fixed target / anchor**; the SfM is the **moving, deformable source**. Every method below is adopted in that one-directional form: warp SfM → LiDAR, never the reverse.
- **Two clouds with very different character.** LiDAR is **dense, planar-structured, low-noise** on walls; SfM is **sparse, textured-feature-driven, noisier, scale-soft**. Methods that exploit LiDAR's planarity (point-to-plane, GICP) and tolerate SfM's sparsity/outliers (robust kernels, trimming, GMM) are favoured.

The answer therefore splits into three layers: a **non-rigid alignment** of the SfM cloud onto the LiDAR (§1–2), a **local correspondence engine** that respects LiDAR planarity (§3), the **few-DOF smooth correction** that is the right parameterisation of *this* warp (§4), the **asymmetric-trust optimizer** that ties it together (§5), and the **self-validation** that proves it helped (§6) — with the over-fitting guard threaded throughout (§7).

---

## 1. Non-rigid point-set registration — warp the SfM cloud onto the LiDAR cloud

These treat alignment as deforming one point set to another, and are the most direct "make the SfM agree with the LiDAR" tools.

| Method | Core idea | Applies to our asymmetric case | Self-validates? |
|---|---|---|---|
| **Coherent Point Drift (CPD)** — Myronenko & Song, IEEE T-PAMI 2010 | Treat alignment as **probability-density estimation**: one cloud's points are GMM centroids fit to the other by EM-maximised likelihood; centroids are forced to **move coherently** (motion-coherence regulariser) to preserve topology. Closed-form rigid M-step; non-rigid M-step regularises the displacement field. Accurate and robust to outliers/missing points; a fast variant is linear-time. [src: arxiv-0905.2635, stanford-nips2006-cpd] | Set the **LiDAR as the fixed GMM target and the SfM as the moving source**, run *non-rigid* CPD with **strong motion-coherence weight λ** so only a smooth warp is allowed — a near-perfect match to a ~13 cm smooth field. CPD's built-in **uniform-outlier component (w)** absorbs SfM points with no LiDAR counterpart (object/clutter points the LiDAR can't see) instead of dragging the warp. | Indirectly — the GMM **likelihood / negative-log-likelihood** is a fit score; rising likelihood under fixed λ is evidence of better alignment. Not a correctness proof on its own (see §6). |
| **GMM-based registration (GMMReg / JRMPC)** | Generalise CPD: represent *both* clouds as GMMs and minimise an L2 / divergence between the mixtures (no hard correspondences). | Lets us **down-weight SfM** by inflating its component variances (soft, noisy) while keeping LiDAR components tight (trusted) — a clean knob for asymmetric trust at the density level. | Same as CPD — divergence value is a relative fit metric, not a correctness proof. |
| **Thin-Plate-Spline Robust Point Matching (TPS-RPM)** — Chui & Rangarajan 2003 | **Softassign** (fuzzy correspondences) + **deterministic annealing** + a **TPS** warp; the annealing schedule (temperature T) goes coarse→fine and the method can **reject a fraction of points as outliers** automatically. [src: sciencedirect-tps-rpm-revisit, researchgate-tps-rpm] | TPS gives an explicit smooth warp field with a tunable **bending-energy regulariser** (the over-fit knob); anneal from near-rigid to mildly non-rigid so the warp can't get spikier than the data demands. Caveat: classic TPS-RPM handles outliers in *one* set well, both sets poorly [src: researchgate-grpm] — fine here since LiDAR (target) is clean. | The bending energy itself is a **smoothness diagnostic** — a warp that needs high bending energy to fit is over-fitting (§7). |

---

## 2. Deformation graphs / As-Rigid-As-Possible (ARAP) — deform smoothly while staying locally rigid

| Method | Core idea | Applies to our asymmetric case | Self-validates? |
|---|---|---|---|
| **Embedded Deformation graph** — Sumner et al., SIGGRAPH 2007 | Attach a sparse set of **control nodes**, each carrying a local affine/rigid warp; any point is deformed by **blending nearby nodes**. Two energy terms: a **rigid term** (keep each node's transform as-rigid-as-possible) and a **smooth term** (neighbouring nodes agree). Decouples deformation complexity from cloud resolution. [src: researchgate-44250275-embedded-deformation, emergentmind-ed-graph] | Lay a **coarse node graph over the SfM cloud only** (LiDAR stays fixed); a strong rigid+smooth weight forces the correction toward a **globally near-similarity warp with slow spatial variation** — exactly a 13 cm drift field. Node count is the explicit DOF budget (keep it small). | The **rigid-term residual per node** is a local diagnostic: nodes forced far from rigid flag where the warp is straining (real disagreement vs over-fit). |
| **ARAP / locally-rigid registration (SPaM, GraphSCNet)** | Formulate the global non-rigid warp as an **aggregation of locally-rigid transforms**; rigidity terms over a correspondence/deformation graph prune bad matches and keep local shape. "Non-rigid deformations are usually locally rigid / local-shape-preserving." [src: frontiers-spam, arxiv-2303.09950-graphscnet] | The locally-rigid prior is **physically right for a room**: walls are rigid; only the SfM's global scale/registration drifts. We want a warp that is *rigid everywhere locally* and only bends slowly — ARAP encodes precisely that. | Local-rigidity residual = a built-in "is this deformation physically plausible" check. |

---

## 3. ICP variants — local SfM-slice ↔ LiDAR-scan / cloud alignment (the correspondence engine)

These are the **inner loop** that any of the above warps calls to find correspondences and do the rigid/local fit; chosen to exploit LiDAR planarity and tolerate SfM sparsity/outliers.

| Method | Core idea | Applies to our asymmetric case | Self-validates? |
|---|---|---|---|
| **Point-to-plane ICP** | Minimise distance from source point to the **tangent plane** of the target surface (uses target normals); more robust to local minima and faster-converging than point-to-point on 2.5D/planar data. [src: rss05-gicp, learnopencv-icp] | LiDAR walls are clean planes/lines with good normals → use **SfM-point-to-LiDAR-plane** so sparse SfM points slide *along* walls (where SfM is uninformative) and are pinned only across them (where LiDAR is authoritative). Encodes the asymmetric trust geometrically. | Per-correspondence point-to-plane **residual field** (§6). |
| **Generalized-ICP (GICP)** — Segal, Malik, Thrun, RSS 2009 | **Plane-to-plane**: model a local covariance at *both* points and minimise a covariance-weighted (Mahalanobis) distance; robust to incorrect correspondences and varying density, same speed as ICP. [src: rss05-gicp, wiki-hanzheteng-gicp] | The covariance per point is **the asymmetric-trust knob at the correspondence level**: give SfM points **large, anisotropic covariances** (soft, uncertain) and LiDAR points **tight covariances** (trusted) → the fit naturally moves SfM to LiDAR and not vice-versa. Best-matched single ICP variant for us. | Mahalanobis residual distribution is a calibrated consistency score. |
| **Trimmed / robust ICP (Tr-ICP, coarse-to-fine trimmed GICP)** | Use only the best-overlapping fraction of correspondences each iteration (trimming) and/or a robust kernel; "gradually eliminates incorrect correspondences," strong for **low-overlap** cases. [src: ieee-9007699-trimmed-gicp, researchgate-339462469] | SfM has **partial overlap** with the LiDAR (covers textured regions, misses blank walls; adds clutter the LiDAR never sees). Trimming lets the alignment ignore the non-overlapping SfM tail **without hand-segmenting** it. **Over-pruning guard lives here** — too-aggressive trim → degenerate fit (§7). | The trimmed-overlap ratio + residual on the retained set are diagnostics. |

---

## 4. Continuous-time / spline / GP trajectory correction — the right parameterisation of *this* warp

The 13 cm warp is smooth in **time/arc-length along the SfM trajectory** (scale drift accumulates with path). Correcting the **trajectory** (few DOF) rather than per-point is the most economical and the least over-fit-prone route.

| Method | Core idea | Applies to our asymmetric case | Self-validates? |
|---|---|---|---|
| **B-spline continuous-time trajectory** (cubic / non-uniform B-spline) — CLINS, Coco-LIC | Represent the trajectory as a **continuous B-spline** over a few control poses; a smooth low-DOF curve naturally models slow drift, with control points placed by motion dynamics. [src: arxiv-clins, researchgate-coco-lic] | Model the SfM **scale/pose correction as a low-knot spline in arc-length**, with the LiDAR as anchor — a dozen control points capture a smooth 13 cm field while being structurally **incapable** of high-frequency over-fit. The knot count *is* the DOF budget (§7). | Few DOF + held-out frames (§6) = directly testable: does the spline cut LiDAR↔SfM residual on *unseen* frames? |
| **Gaussian-Process trajectory / GP regression correction** — Traj-LIO; GP for sparse LiDAR | Trajectory as a **GP** (e.g. white-noise-on-acceleration prior); query the pose continuously, with a kernel that enforces smoothness; GPR also used to mitigate sparse/uneven observations. [src: arxiv-traj-lio] | A GP over the **SfM-vs-LiDAR offset** vs arc-length gives a smooth correction **with calibrated uncertainty** — the posterior variance flags where the correction is well-constrained (dense overlap) vs guessed (blank wall). Smoothness is set by the kernel length-scale, not a per-point fit. | **Built-in**: the GP **predictive variance** is a self-validation field; **GP marginal likelihood** does principled length-scale selection, resisting over-fit. |

---

## 5. Loosely-coupled bundle adjustment with per-sensor covariance — the asymmetric-trust optimizer

This is the **back-end** that ties §3's correspondences and §4's parameterisation into one solve, and is where the asymmetric trust is *enforced numerically*.

- **Loosely-coupled, per-sensor covariance weighting.** Process each sensor's estimate, then fuse in a back-end (factor graph / least squares) where **each modality's covariance scales its contribution** — so the abundant, accurate LiDAR factors dominate and the sparse, soft SfM factors are deliberately light. "Scaling the measurement covariance ensures each modality contributes comparable information rather than being implicitly weighted by its measurement count." [src: sciencedirect-mls-als-fusion, nature-lidar-qr] This is *the* mechanism for LiDAR-heavy / SfM-light trust.
- **Robust kernels (Huber / Cauchy / GNC).** Wrap residuals in a robust kernel so a few gross SfM blunders (mis-association, scale slip) **switch themselves down** instead of bending the whole warp; "applying robust kernel weighting significantly improves accuracy." [src: arxiv-2409.01856-robust-lidar-ba] Graduated Non-Convexity (GNC) gives a tuning-free anneal from convex→robust.
- **Adaptive / hierarchical covariance.** Adjust each factor's weight from **residual statistics and observation quality** — e.g. down-weight SfM in regions where its local covariance (or GP variance, §4) is large. [src: doi-sensors-26051653]
- **Asymmetric form for us.** Treat **LiDAR scan placements as the rigid skeleton** (tight priors; only pose + tilt/height free), the **SfM as soft observations of the same geometry** (loose, robust-kernelled), and solve once in a batch LM/GNC. This is the map-side mirror of [[trajectory-refinement-and-fusion.md]]'s pose-graph reconciliation; combine with the wall-spread objective of [[global-alignment-wall-refinement.md]] so the warp is also pulled toward making walls crisp.

**How it self-validates:** per-sensor **leave-one-out** (drop SfM, re-fit; the LiDAR-only map should barely move — proves SfM isn't corrupting it) and the **robust-kernel weight distribution** (a healthy fit down-weights a *few* outliers, not a large fraction — a large fraction means over-pruning, §7).

---

## 6. Self-consistency / cross-validation — "are they aligned, AND is the result more correct?"

Alignment can look better (smoother, lower residual) while being *less* correct (warped to a degenerate fit). These metrics separate the two, and most need **no ground truth** — essential here.

- **Residual field (point-to-plane / Mahalanobis), spatially mapped.** Don't report just a mean — map the residual **over space**: a residual that collapses *everywhere uniformly* is genuine alignment; one that collapses only where DOF were spent (and stays high elsewhere) is local over-fit.
- **Map crispness / surface-thickness metrics (no GT).** **Mean Map Entropy (MME)** and **consistency / point-disparity error** quantify how "crisp" overlapping surfaces are — a correctly-fused map has thinner walls. [src: arxiv-2301.02297-self-consistency, arxiv-2106.11351-no-reference] These are the same wall-spread signal as [[global-alignment-wall-refinement.md]]. **Caveat (built-in over-fit trap):** point-disparity is "susceptible to map-to-map error — an erroneous group of well-aligned submaps yields low disparity despite being wrong" [src: arxiv-2301.02297-self-consistency]; crispness alone can be gamed by a degenerate warp, so pair it with held-out residual.
- **Leave-one-sensor-out.** Fit using LiDAR only, predict SfM; and vice-versa. If fusing genuinely helps, **each predicts the other's held-out data better than its own prior** — the cleanest correctness signal without GT.
- **Held-out-frame / k-fold cross-validation on the warp.** Fit the §4 spline/GP on a subset of correspondences, measure residual on the **held-out** ones. A correction that helps held-out frames is real; one that only helps fitted ones is over-fit. (GP marginal likelihood does this implicitly.)
- **Reprojection error (camera side).** After warping, **re-project SfM-registered 3D into the camera frames** — true geometric improvement lowers reprojection error; a warp that only smooths the cloud but worsens reprojection is moving points away from where the images say they are.
- **Map-to-map distance vs an independent anchor.** Where a sparse trusted anchor exists (the LiDAR walls, or the SfM-localised fridge hit to 0.45 m of GT in the project record), measure distance of the fused map to it as an external check.

---

## 7. The over-pruning / over-fitting guard (binding — woven through every section)

The central failure mode: **deform/trim until the fit looks clean but is geometrically false.** Guards:

- **Match DOF to the error's frequency content.** The warp is smooth/low-frequency → use **few control points / long GP length-scale / strong CPD coherence / high TPS bending-energy weight**. "It proved extremely difficult to find a regularization weight that simultaneously avoided degeneracy and excessive rigidity" [src: arxiv-2510.18658-morphmodes] — so don't search per-point; **cap the DOF structurally** (a 12-knot spline simply cannot over-fit a 13 cm field).
- **Coarse-to-fine annealing, stop early.** TPS-RPM/CPD anneal from near-rigid; **stop when held-out residual stops improving**, not when training residual bottoms out.
- **Trim/robust fraction is bounded.** A healthy robust fit rejects a *small* fraction; a large rejected fraction means the warp is fitting noise — cap the trim ratio and alarm if exceeded (mirrors [[reconciling-competing-signals.md]]'s down-weight-don't-delete and the project robust-evidence principle).
- **Respect real, sensor-specific disagreement.** Some LiDAR↔SfM disagreement is *true* (LiDAR scan plane ~7 cm above the camera sees walls behind against-wall counters the camera never images — project rig finding). The guard must **flag these as real differences, not warp them away.** Distinguish via the residual *pattern*: smooth global field = correctable drift; sharp localized offset at a known occluder = real, keep both.
- **Cross-validate, don't self-certify.** Crispness can be gamed (§6 caveat); always confirm with leave-one-sensor-out or held-out residual before declaring the fused map "more correct."

---

## 8. Recommendation for our case (priority order)

Smooth ~13 cm warp · sparse noisy SfM cloud + dense accurate LiDAR · asymmetric trust:

1. **B-spline / GP trajectory-warp correction (§4)** — *first.* The error is a smooth drift in arc-length; correct the *trajectory* with ~12 knots / a long-length-scale GP. Lowest DOF, structurally over-fit-proof, and the GP gives a free uncertainty field. **Self-validates** via held-out-frame residual + GP marginal likelihood.
2. **Loosely-coupled BA with per-sensor covariance + robust kernel (§5)** — *the optimizer that hosts #1.* LiDAR placements rigid/heavy, SfM soft/light, Huber/GNC on SfM residuals. **Self-validates** via leave-one-sensor-out and the robust-weight distribution.
3. **GICP as the correspondence engine (§3)** — give SfM points large anisotropic covariances, LiDAR points tight ones; encodes the asymmetric trust at the match level and feeds residuals to #2. **Self-validates** via the Mahalanobis residual distribution.
4. **Non-rigid CPD, LiDAR-fixed, high coherence λ (§1)** — *if a trajectory parameterisation underfits a spatially (not temporally) varying warp.* Direct cloud→cloud warp with an outlier component for SfM clutter. **Self-validates** via GMM likelihood + held-out residual.
5. **Embedded-deformation graph / ARAP, coarse node set (§2)** — *fallback for a spatially-structured warp*; locally-rigid is the physically-right prior for a room. **Self-validates** via per-node rigid-term residual.

Across all: judge by **§6 no-GT self-consistency (map crispness + leave-one-out + reprojection)**, and enforce the **§7 DOF cap + bounded-trim guard** so we never deform to a degenerate fit.

---

## Sources

| Tag | Work | Year |
|---|---|---|
| arxiv-0905.2635 / stanford-nips2006-cpd | Myronenko & Song — *Point-Set Registration: Coherent Point Drift* (T-PAMI; NIPS 2006) | 2006/2010 |
| sciencedirect-tps-rpm-revisit / researchgate-tps-rpm | Yang — *The TPS-RPM algorithm: a revisit*; Chui & Rangarajan original | 2003 / 2011 |
| researchgate-grpm | Generalized Robust Point Matching (G-RPM) — outliers in both sets | — |
| researchgate-44250275-embedded-deformation / emergentmind-ed-graph | Sumner, Schmid, Pauly — *Embedded Deformation for Shape Manipulation* (SIGGRAPH) | 2007 |
| frontiers-spam | *SPaM: soft patch matching for non-rigid pointcloud registration* | 2023 |
| arxiv-2303.09950-graphscnet | *Deep Graph-based Spatial Consistency for Robust Non-rigid Registration* (GraphSCNet) | 2023 |
| rss05-gicp / wiki-hanzheteng-gicp | Segal, Malik, Thrun — *Generalized-ICP* (RSS) | 2009 |
| learnopencv-icp | ICP / point-to-plane explainer | — |
| ieee-9007699-trimmed-gicp / researchgate-339462469 | *A Coarse-to-Fine Generalized-ICP Algorithm With Trimmed Strategy* | 2020 |
| arxiv-clins / researchgate-coco-lic | CLINS; Coco-LIC — continuous-time B-spline LiDAR(-inertial-camera) | 2021/2023 |
| arxiv-traj-lio | *Traj-LIO* — sparse Gaussian-Process multi-LiDAR-IMU state estimator | 2024 |
| sciencedirect-mls-als-fusion | Robust MLS–ALS fusion with local geometric uncertainty (per-sensor covariance) | 2026 |
| nature-lidar-qr | LiDAR-inertial SLAM w/ visual QR — loosely-coupled covariance fusion | 2025 |
| arxiv-2409.01856-robust-lidar-ba | *Robust Second-order LiDAR Bundle Adjustment* (robust kernel / MSG metric) | 2024 |
| doi-sensors-26051653 | Adaptive multi-sensor fusion w/ eigenvalue degradation detection | 2026 |
| arxiv-2301.02297-self-consistency | *Improving Self-Consistency in Underwater Mapping* (point-disparity, MME, map-to-map caveat) | 2023 |
| arxiv-2106.11351-no-reference | *Be Your Own Benchmark: No-Reference Trajectory Metric on Registered Point Clouds* | 2021 |
| arxiv-2510.18658-morphmodes | *MorphModes* — degeneracy-vs-stiffness regularization trade-off | 2025 |

## Related

- [[sfm-error-sources.md]] — the cause-side diagnosis: why monocular SfM bows (scale drift / gauge / degenerate motion); confirms this warp is correctable error, not a blunder
- [[trajectory-refinement-and-fusion.md]] — the two-trajectory back-end reconciliation; this page is its map-side twin
- [[reconciling-competing-signals.md]] — cross-field robust fusion + the over-pruning guard (asymmetric reliability)
- [[lidar-visual-fusion-slam.md]] — where the two sensors meet; loose back-end fusion
- [[stereo-3d-mapping-known-poses.md]] — how the SfM cloud is produced
- [[global-alignment-wall-refinement.md]] — the wall/plane crispness objective the fused map feeds
