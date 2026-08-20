# Global Alignment Refinement via Wall/Plane Constraints — Sharpening a Floor Plan

After an initial pose-graph alignment of an accumulated LiDAR sweep, the *same* physical wall can show up as **two parallel point-bands** (two local density maxima tens of cm apart) because pose error accumulated and was never fully removed. The initial alignment is not the final alignment: a **refinement step** should detect that a band is double-defined, confirm the two sub-bands are one wall, and then **re-optimize poses so that the spread of every wall is minimized at once**. This page surveys the methods that do this — pose-graph refinement with plane/line constraints, planar bundle adjustment (BALM / BALM2 / Eigen-Factors / planar adjustment), globally-consistent scan refinement (ELCH), and the robust detection/association needed to know two bands are the same wall — and recommends a concrete recipe for our case (2D, ~6 walls, modest residual pose error). *(synthesis — assembled from the cited primary sources; sits downstream of [[learned-point-cloud-registration]] and [[2d-lidar-slam]].)*

> **Read alongside:** [[learned-point-cloud-registration]] (ICP/GICP front-end registration), [[2d-lidar-slam]] (Cartographer SPA / SLAM-Toolbox pose graph that produces the *initial* alignment), [[mapping-stack-design]] (where the floor plan sits in the stack), [[slam]] (the SLAM hub and loop-closure context).

---

## 1. The problem, framed correctly

The standard SLAM back-end ([[2d-lidar-slam]] §SPA, [[slam]]) optimizes a **pose graph**: nodes are scan/keyframe poses, edges are relative-pose constraints (odometry + loop closure). It produces a *globally consistent trajectory*, but it never looks at whether the **map points the trajectory implies are themselves consistent**. A "double wall" is exactly the failure that survives a converged pose graph: the loop-closure constraints were satisfied, yet the residual per-pose error is enough to smear one planar surface into two bands.

The fix is to add a **second objective that the pose graph ignores: structural self-consistency** — points that belong to one wall should fit one line/plane with minimal residual. This is the central idea behind *plane/line-constrained refinement* and *planar bundle adjustment*. The decision variables are still the poses (and optionally the plane parameters), but the cost is now driven by **the thickness of co-planar structure**, not by relative-pose edges.

Two ways to inject the structure:

- **As pose-graph factors** (loosely coupled): detect planes/lines, associate them across scans, add a factor that penalises a scan's points for deviating from the shared plane — solved in a factor-graph optimizer (GTSAM / g2o / Ceres) alongside the existing pose edges.
- **As bundle adjustment** (tightly coupled): jointly optimise poses *and* plane parameters (or analytically eliminate the planes) to directly minimise total point-to-plane spread — BALM / Eigen-Factors / planar adjustment.

---

## 2. Detecting and confirming a "double wall" (the front-end of refinement)

Before any optimization, we must (a) find planar/linear structure, (b) decide which detections are the *same* surface, and (c) flag the double-definition.

### 2.1 Extracting planes/lines

- **RANSAC plane/line fitting** — the workhorse; fit a model, count inliers, repeat. PCL `SACSegmentation` (3D planes) and any 2D line-RANSAC do this. Known weakness: RANSAC "may erroneously merge points from different planes, especially when planes have similar but distinct normal vectors, leading to biased plane parameters and unreliable uncertainty" [src: arxiv-2509.16832 (L2M-Reg)], so a geometric-consistency check after fitting is needed.
- **Region growing / normal+offset clustering** — group points by similar normal direction and similar perpendicular distance-to-origin; "clustering can be performed by discrete values of normal-orientation and of perpendicular distance to the origin" [src: emergentmind-ransac-plane-detection]. This is directly the (normal θ, offset ρ) parameterisation we want for walls.
- **Agglomerative Hierarchical Clustering (AHC / PEAC)** — for organized depth, divide into blocks, merge adjacent blocks while plane-fit MSE stays under threshold; runs >35 Hz on 640×480 [src: ieee-6907776 (Feng et al., ICRA 2014), github-ai4ce-peac]. Open source (`ai4ce/peac`).
- **2D line-segment SLAM** — for our planar floor-plan case, "line segments [are] principal elements of artificial environments"; line features are extracted from laser scans and combined with the grid [src: ieee-5354214]. Split-and-merge / IEPF on each scan gives wall segments directly in 2D.

### 2.2 Confirming two bands are the SAME wall (association / gating)

This is the load-bearing step — get it wrong and refinement fuses two genuinely different walls. The literature converges on a **normal + offset + topology** test:

- **Normal-and-offset threshold.** "Planes are first checked whether the plane normal difference is within 30° and distance to each other is smaller than 1 m, then find the plane matching with the most shared feature points" [src: arxiv-1809.03415 (Yang & Scherer, monocular object+plane SLAM)]. PAS-SLAM uses the same normal-angle + offset-distance + shared-point gate for planar association [src: arxiv-2402.06131 (PAS-SLAM)].
- **Mahalanobis gating (probabilistic).** "The most common criteria to determine data association rely on minimizing the squared Mahalanobis distance between observations and predictions"; "gating prunes potential pairings based on a threshold" [src: researchgate-221787350]. Using the *covariance* of the fitted plane (not a hard metric threshold) makes the gate scale-aware — a thin, well-determined band tolerates less offset than a noisy one.
- **Topology cross-check (our extra confidence).** Two bands are the same wall only if the floor-plan topology agrees: same normal orientation, offsets within the expected accumulated-drift budget (tens of cm, not metres), spatial overlap along the wall direction, and no *third* parallel structure between them (which would imply two real walls + a gap). This is the "robust-evidence" stance from project memory — confirm by agreement/redundancy, flag the rest unknown.

### 2.3 The double-wall signature, concretely

A double-defined wall is a single point band of thickness `x` (along its normal) whose 1-D density profile across the normal has **two clear local maxima at offsets `a` and `b`**, with `|a−b|` in the drift regime (≈0.1–0.5 m) and a saddle between them. Practically: take the band's points, project onto the fitted normal, build a 1-D histogram/KDE of the offset, and run peak detection. Two peaks separated by more than the single-wall noise width, but less than the room's smallest real wall-gap, and supported by the §2.2 gate → **double-wall**.

---

## 3. The refinement back-ends (method survey)

### 3.1 Pose-graph refinement with plane/line factors (GTSAM / g2o / Ceres)

Add the associated structure as **factors** in the existing factor graph. GTSAM natively supports planar SLAM (`Pose2`/`Pose3` + landmark factors) and "incorporates loop closing with landmark-plane merging in the global factor graph, where detected landmark planes are merged when they represent the same plane" [src: gtbook-PlanarSLAMExample, cmu-Hsiao18icra]. Hsiao et al.'s **dense planar-inertial SLAM with structural constraints** (ICRA 2018) is the canonical example: planes are landmarks, points contribute point-to-plane factors, and structural priors (parallel/perpendicular) are added [src: cmu-Hsiao18icra]. Strength: drops straight into the existing back-end; the plane is a first-class landmark you can also merge on loop closure. Weakness: you carry the plane parameters as extra state.

### 3.2 Planar bundle adjustment — minimise point-to-plane spread directly

This family is the **most direct answer to "minimise wall spread across all walls at once."**

- **BALM (Bundle Adjustment for Lidar Mapping)** — Zhou, Liu, Zhang, RA-L 2021. "Enforces feature points to lie on the same edge or plane by minimizing the eigenvalue of the covariance matrix" of the co-feature points, with closed-form 1st/2nd derivatives [src: researchgate-344733994, semanticscholar-balm]. The minimum eigenvalue of a band's scatter matrix **is** its thickness along the normal — minimising it over poses is literally minimising wall spread. Plane parameters are solved in closed form and removed from the optimisation.
- **BALM2 / "Efficient and Consistent Bundle Adjustment on Lidar Point Clouds"** — Liu, Liu, Zhang, **IEEE T-RO 2023**. Adopts the **point-cluster** representation: "encodes all raw points associated to the same feature by a compact set of parameters," so the solver "fundamentally avoids the enumeration of each raw point" during cost, derivatives, and uncertainty. Switches to a point-to-plane cost, converges fast, eliminates features ahead of time, removes the singularity. **Open-sourced** [src: arxiv-2209.08854]. This is the strongest off-the-shelf reference implementation.
- **Eigen-Factors** — Ferrer (Skoltech), IROS 2019 + Autonomous Robots 2025. "Solves PC SLAM using planes as the main geometric primitive… a closed-form gradient is derived by differentiating over the minimum eigenvalue with respect to poses." State variables are **only the poses** (planes estimated in closed form); cost is independent of the number of points (thanks to a summation matrix S), depending only on #planes and #poses [src: arxiv-2304.01055, skoltech-ferrer2019]. Conceptually identical objective to BALM; alternating/bilevel optimisation.
- **Plane / Bi-convex large-scale variants** — **GlobalPointer: Large-Scale Plane Adjustment with Bi-Convex Relaxation** (2024) targets convergence robustness for many-plane scenes [src: arxiv-2407.13537]; the **plane-extraction-for-BA** paper (2023) supplies the front-end planes [src: arxiv-2305.00287].

All four minimise the **same quantity** — the residual scatter of co-planar points — and all reduce dimensionality by solving the plane analytically. The difference is engineering: BALM2 is the maintained, open-source, T-RO-grade implementation.

### 3.3 Globally-consistent scan refinement without explicit planes — ELCH

**ELCH (Explicit Loop Closing Heuristic)** — Sprickerhof, Nüchter et al. (Würzburg/Osnabrück), 2009–2011. On detecting a loop it "dissociates the last scan, reassociates it to the map, and distributes the pose-error difference over the SLAM graph" — closing loops without iterating front-/back-end, "an order of magnitude faster" than full relaxation [src: uni-wuerzburg-elch, semanticscholar-elch-6dof]. This is the *geometry-spreading* alternative: it sharpens the map by redistributing residual error along the trajectory rather than by fitting explicit planes. Available in **3DTK (The 3D Toolkit)**. Good when the double-wall is loop-induced and you have no clean plane extraction; weaker than planar-BA when you *do* have clean walls and want them razor-sharp.

### 3.4 Iterative structure↔pose (EM / alternating) refinement

The general pattern under Eigen-Factors and any plane-landmark BA: **(E-step)** fix poses, fit/re-estimate each plane (and re-associate points → planes); **(M-step)** fix planes, optimise poses to reduce point-to-plane residual; iterate. This is the practical loop we will actually run; BALM2/Eigen-Factors give the closed-form M-step.

### 3.5 Map-domain post-processing (last resort)

Pure occupancy-grid sharpening — thinning, thresholding, ICP-based map alignment, or GAN-based artifact removal (TTOGM, arXiv 2504.19654) [src: arxiv-2504.19654, themoonlight-ttogm-review] — operates on the rendered grid, not the poses. It can cosmetically thin a wall but does **not** fix the underlying pose error and can hallucinate structure. Use only as a final cosmetic pass, never as the metric fix.

---

## 4. Method comparison

| Method | Primitive | Optimises | Minimises wall spread? | Library / availability | Fit for our case (2D, ~6 walls) |
|---|---|---|---|---|---|
| **Pose-graph + plane/line factors** | plane/line landmarks | poses + plane params | Indirectly (point-to-plane factors) | GTSAM (native PlanarSLAM), g2o, Ceres | Strong — drops into existing back-end; carries plane state |
| **BALM** (RA-L 2021) | edge/plane clusters | poses (planes closed-form) | **Yes — min eigenvalue = thickness** | Open source (BALM) | Strong concept; 3D-oriented |
| **BALM2 / Eff.&Consistent BA** (T-RO 2023) | point clusters | poses (planes eliminated) | **Yes — point-to-plane, point-cluster** | **Open source, maintained** | **Best reference impl.** |
| **Eigen-Factors** (IROS'19 / AuRo'25) | planes | **poses only** | **Yes — min eigenvalue, closed-form grad** | Author code (Skoltech) | Strong; clean theory, pose-only state |
| **GlobalPointer** (2024) | planes | poses + planes (bi-convex) | Yes (large-scale robustness) | Research code | Overkill for 6 walls |
| **ELCH** (2009–11) | raw scans | poses (error-spreading) | Indirectly (no plane fit) | 3DTK | Fallback if planes don't extract cleanly |
| **Map post-processing** (thinning/GAN) | occupancy grid | nothing (pixels) | Cosmetic only | OpenCV / TTOGM | Final cosmetic pass only |

Front-end registration baselines (ICP/GICP/NDT, and why classical still wins) are covered in [[learned-point-cloud-registration]]; this page is strictly the **structural refinement layer above** a converged pose graph.

---

## 5. Recommended approach for OUR case

Constraints: **2D** floor plan, **~6 walls**, **modest** residual pose error (tens of cm), goal = **minimise each wall's spread**, want a **joint** optimisation, and the data is **already-accumulated** (offline refinement, not real-time). The robust-evidence principle from project memory applies: build from the walls many scans agree on; flag the rest unknown.

**Recommendation: a 2D Eigen-Factor / BALM-style joint refinement, formulated as point-to-line spread minimisation over the surviving LiDAR points, with explicit double-wall detection as the front-end.** Rationale:

1. It minimises *exactly* the quantity we care about — the cross-wall thickness (the smaller eigenvalue of each wall's 2-D point scatter) — summed over all walls, in one optimisation. That is the "minimise spread across ALL walls at once over surviving LiDAR data" the mandate asks for.
2. Pose-only state (planes/lines solved in closed form) keeps the problem tiny: a handful of scan-segment poses × 6 line constraints. Trivial to solve with Ceres or even hand-rolled Gauss-Newton.
3. We don't need BALM2's point-cluster machinery for 6 walls; we borrow its *objective* (point-to-line eigenvalue cost) and Eigen-Factors' *pose-only* formulation, implemented small.
4. ELCH is the fallback if line extraction is too noisy to associate reliably; GTSAM plane-factors are the fallback if we'd rather reuse a factor-graph optimiser we already have.

**What stays fixed:** the loop-closure topology from the initial pose graph (don't re-litigate loop closures); we only refine the residual within the established graph — the initial alignment is the *prior*, not the final answer.

---

## 6. Concrete recipe: double-wall detection → confirm-same-wall → joint refit

A prototype-able pipeline for the 2D case (everything below is a line, the 2D analogue of a plane; "normal" = wall outward direction, "offset" ρ = signed distance to origin):

**Stage A — Extract wall lines (per pose-segment).**
1. Split the accumulated sweep into the *pose segments* whose error we'll adjust (e.g. per-keyframe or per-submap groups from the initial pose graph).
2. In each segment, fit line segments to the points (split-and-merge / IEPF, or 2D RANSAC). Record each as `(normal θ, offset ρ, support points, endpoints, fit covariance)`.

**Stage B — Detect a double-defined wall.**
3. Cluster all line detections across segments by `(θ, ρ)` (normal-orientation + offset bins, §2.2). Within a cluster, project member points onto the cluster normal → 1-D offset histogram/KDE.
4. **Double-wall test:** ≥2 clear local maxima at offsets `a`,`b` with `|a−b|` in the drift band (≈0.1–0.5 m), a saddle between them, and both peaks well-supported. Flag the cluster `double`.

**Stage C — Confirm two bands are ONE wall (gate).**
5. Apply the normal+offset+overlap gate: normal difference < ~15–30°, offset gap below the smallest real wall-gap in the room, and the two bands **overlap along the wall direction** (same physical extent). Optionally a Mahalanobis gate using the fit covariances (§2.2).
6. Topology cross-check: no third parallel line lies between them; the merged line is consistent with the floor-plan polygon (a closed ~6-wall loop). Pass → the two bands are one wall; assign both bands' points a single shared line-landmark ID. Fail → keep them separate, flag `ambiguous` (don't merge on weak evidence).

**Stage D — Joint refit (minimise spread over ALL walls).**
7. Build the cost: for every confirmed wall `j`, let `S_j` be the scatter matrix of all points assigned to it (across all segments, transformed by their segment poses). The wall's spread is the **smaller eigenvalue** `λ_min(S_j)` (point-to-line residual). Total cost `= Σ_j λ_min(S_j)` (BALM/Eigen-Factor objective).
8. Decision variables: the per-segment pose corrections `{ΔT_i}` (SE(2)), initialised at identity (initial alignment = prior). Anchor one segment (or add a soft prior to the initial poses) to fix gauge.
9. Optimise with Gauss-Newton / Ceres using the closed-form gradient of `λ_min` w.r.t. poses (Eigen-Factor derivation); the line parameters are re-derived from `S_j` each iteration (the E-step), poses updated (the M-step), iterate to convergence.
10. Re-render the occupancy grid from the corrected poses. Each confirmed wall should now collapse to a single thin band; verify the two former peaks merged and total Σλ_min dropped. Optionally one cosmetic thinning pass (§3.5) — but the metric win must come from the pose refit, not the pixels.

**Validation:** report, per wall, before/after `λ_min` (band thickness) and peak count; report total spread reduction; sanity-check that the closed-wall polygon area/dimensions still match tape GT (don't shrink walls into each other). This mirrors the EDA-style before/after scorecard already used in this repo.

---

## Source

| Tag | Work | Venue / Year |
|---|---|---|
| arxiv-2209.08854 | Efficient & Consistent Bundle Adjustment on Lidar Point Clouds (BALM2; point cluster) — Liu, Liu, Zhang | IEEE T-RO 2023 (open source) |
| researchgate-344733994 | BALM: Bundle Adjustment for Lidar Mapping — Zhou, Liu, Zhang (min-eigenvalue cost) | IEEE RA-L 2021 |
| arxiv-2304.01055 | Eigen-Factors: a Bilevel Optimization for Plane SLAM of 3D Point Clouds — Ferrer et al. | AuRo 2025 / IROS 2019 |
| arxiv-2407.13537 | GlobalPointer: Large-Scale Plane Adjustment with Bi-Convex Relaxation | 2024 |
| arxiv-2305.00287 | An Efficient Plane Extraction Approach for Bundle Adjustment on LiDAR Point Clouds | 2023 |
| cmu-Hsiao18icra | Dense Planar-Inertial SLAM with Structural Constraints — Hsiao, Westman, Kaess | ICRA 2018 (GTSAM) |
| gtbook-PlanarSLAMExample | GTSAM by Example §2.4 Planar SLAM | GTSAM docs |
| arxiv-1809.03415 | Monocular Object and Plane SLAM in Structured Environments — Yang & Scherer (plane association gate) | RA-L 2019 |
| arxiv-2402.06131 | PAS-SLAM: Visual SLAM for Planar Ambiguous Scenes (plane association) | 2024 |
| researchgate-221787350 | Dealing with Data Association in Visual SLAM (Mahalanobis gating) | — |
| uni-wuerzburg-elch / semanticscholar-elch-6dof | ELCH explicit loop-closing heuristic — Sprickerhof, Nüchter et al. (3DTK) | 2009–2011 |
| ieee-6907776 / github-ai4ce-peac | Fast Plane Extraction via Agglomerative Hierarchical Clustering (PEAC) — Feng et al. | ICRA 2014 (open source) |
| ieee-5354214 | RBPF grid SLAM enhanced by line matching (2D line features) | IEEE |
| arxiv-2509.16832 | L2M-Reg (RANSAC false-merge caveat) | 2025 |
| emergentmind-ransac-plane-detection | RANSAC-based plane detection (normal+offset clustering) | survey |
| arxiv-2504.19654 | TTOGM: 2-D deep-learning refined occupancy grid (cosmetic post-proc) | 2025 |

## Related

- [[weak-scan-registration-methods]] — the **single-weak-scan, locked-target** sibling of this page: how to *seat* one stubborn weak-wall/rich-object scan into an already-locked reference (observability-aware GICP, object-as-landmark, global init), where this page sharpens *all* walls jointly
- [[learned-point-cloud-registration]] — the front-end registration layer (ICP/GICP/NDT and learned methods) that produces the per-scan alignment this page refines
- [[2d-lidar-slam]] — Cartographer SPA / SLAM-Toolbox pose graph that produces the *initial* (non-final) alignment
- [[slam]] — SLAM hub; loop-closure and map-then-localize context
- [[mapping-stack-design]] — where the sharpened floor plan sits in the world-model stack
