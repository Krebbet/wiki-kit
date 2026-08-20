# Per-Point Classification Against Fitted Primitives + Self-Consistency Error Band

How to take an accumulated room point cloud plus the artefacts we already derive from it — a fitted floor plan (wall lines, [[floorplan-reconstruction-methods]]) and a set of detected objects (centroids + footprints + labels, [[semantic-object-memory]]) — and **classify every single point** into one of five classes:

1. **wall** — explained by a fitted wall line/plane
2. **identified object** — explained by a labelled object primitive
3. **unidentified object** — a coherent cluster that is clearly an object but has no label
4. **unknown** — explained by *nothing* we have, but not obviously noise (needs diagnosis + disposition)
5. **noise** — sensor artefact, discard

Then: every assigned point is compared back against the primitive it was assigned to, and the residuals are aggregated into an **internal, self-consistent error band** — a per-primitive and whole-map number that says "given our own wall/object model, this is how tightly the points actually agree with it."

This page exists because the governing project principle — *"for every point we must be able to explain where it came from; if yes, does it fit our assumptions about co-located points; if no, is it noise or genuinely unexplained?"* ([[robust-evidence-mapping-principle]]) — is a **point-accounting** problem, not a segmentation-leaderboard problem. The wiki already covers the learned-segmentation leaderboard side ([[ov3d-instance-seg]], [[scene-graph-world-model]]); the **point-to-primitive assignment + leftover→unknown + self-consistency residual** framing is not covered anywhere and is what this page adds.


---

## Framing — this is an *assignment + accounting* problem, not segmentation from scratch

*(synthesis)* The usual 3D-segmentation literature ([[ov3d-instance-seg]]) starts from raw points and *invents* the segments. We are in a different, easier regime: **we already have the primitives** (wall lines from [[floorplan-reconstruction-methods]], object centroids/footprints/labels from the [[semantic-object-memory]] pipeline). The task is to *assign each point to the primitive that best explains it, within a tolerance, and account for the leftovers.* That inverts the usual difficulty ordering: the simplest methods (nearest-primitive within tolerance) are not a weak baseline here — they are the *natural* formulation, because the hard part (finding the primitives) is already done upstream.

Two consequences:

- **The "unknown" class is first-class, not an afterthought.** A point that is far from every wall line and outside every object footprint is, by construction, unexplained. Most learned segmenters force every point into a known class; here, "none of the above within tolerance" is the *default* outcome and we have to actively claim a point away from it. This is the right polarity for the project principle.
- **The error band is just the assignment residual, aggregated.** Once a point is assigned to a wall line, its perpendicular distance to that line *is* the residual. Aggregating residuals per primitive (and per class) gives an internal self-consistency band with no external ground truth required. This is "demonstrate, don't assert" (Commandment V) applied to the map itself.

---

## The decision cascade — one pass, in priority order

*(synthesis)* The five classes are resolved by a fixed-priority cascade. Each point is tested against the cheapest, most-confident explanation first; only unclaimed points fall through.

```
for each point p:
  1. NOISE GATE       statistical/radius outlier?            -> NOISE, stop
  2. WALL TEST        within tol_wall of a fitted wall line?  -> WALL (residual = perp dist)
  3. OBJECT TEST      inside an object footprint + height?    -> IDENTIFIED OBJECT (residual = dist to centroid/footprint)
  4. CLUSTER TEST     part of a coherent leftover cluster?    -> UNIDENTIFIED OBJECT
  5. else                                                     -> UNKNOWN  (diagnose)
```

- **Order matters.** Noise is gated first so a noise point never gets assigned to a wall and inflates that wall's error band. Walls before objects because wall lines are the most reliable primitive ([[robust-evidence-mapping-principle]] — many points agree on a wall) and objects often sit *against* walls.
- **Tolerances are the knobs.** `tol_wall` should be set from the *expected* depth noise (≈0.6 m slab at 3 m for passive stereo, [[floorplan-reconstruction-methods]]; much tighter for LiDAR, [[robust-evidence-mapping-principle]]), not hand-tuned. The residual band then validates whether the tolerance was honest.
- **"Unknown" is the residual of the whole cascade** — points explained by nothing. These get diagnosed (below), not silently dropped.

---

## Handling the UNKNOWN class — diagnosis + disposition

*(synthesis)* "Unknown" is not a dustbin; it is a queue with a triage rule. For each unknown point/cluster, ask the three project-principle questions in order:

| Diagnosis | Test | Disposition |
|---|---|---|
| **Under-fitted wall** | unknown cluster is thin, planar, collinear with map edge, but no wall line was fit there | feed back to [[floorplan-reconstruction-methods]] as a missed wall hypothesis → re-fit |
| **Under-detected object** | coherent blob, object-scale, off-floor, but no label/footprint | promote to **unidentified object**; queue for the [[semantic-object-memory]] detector / a camera re-look |
| **Genuinely unexplained structure** | persists across sweeps ([[robust-evidence-mapping-principle]] redundancy), coherent, but matches no wall/object model | keep as **unknown**, flag for human/scene-graph; do *not* discard |
| **Residual noise that passed the gate** | sparse, no cross-sweep support, high local roughness | reclassify → **noise**, discard |

The key disposition principle from [[robust-evidence-mapping-principle]]: **reliability = agreement/redundancy.** An unknown point that *recurs* across multiple sweeps is genuine-unexplained; one that appears once is almost certainly noise that slipped the gate. Multi-sweep fusion (EDA033, the 2nd software nav-map win) gives us exactly this redundancy signal for free.

---

## The self-consistency error band — internal, no ground truth

*(synthesis)* Once points are assigned, the band is computed entirely from residuals against *our own* primitives:

- **Per-wall:** for all points assigned to wall line *L*, residual `rᵢ = perpendicular distance(pᵢ, L)`. Report `RMS(r)`, `p95(|r|)`, and inlier fraction. A thin RMS = crisp wall; a fat RMS = the "0.6 m slab" passive-stereo failure ([[floorplan-reconstruction-methods]]) made measurable.
- **Per-object:** residual = distance to footprint boundary / centroid; report spread vs the object's expected extent.
- **Whole-map self-consistency:** the *fraction of points explained* (wall + identified + unidentified) vs unknown vs noise — a single accountability number. "94% of points explained, 4% unknown-recurring, 2% noise" is a defensible map-quality statement with no external GT.
- **Mahalanobis option:** when a primitive has a covariance (e.g. PCA of wall-inlier spread), score each point by Mahalanobis distance instead of raw Euclidean — this *is* a per-point statistical "does it fit?" test and yields a calibrated reject threshold (χ² quantile) for the unknown gate. *(synthesis — standard but not yet validated on our data.)*

This band is the concrete output of "does it fit our assumptions about co-located points?": points assigned to the same primitive *are* the co-located set, and the residual distribution *is* the fit check.

---

## Ordered experiment list — simplest → most advanced

Each entry: what it buys us · how it yields UNKNOWN + an error band · rough compute cost.

### E1 — Statistical/radius outlier removal (the noise gate) — **DO FIRST, trivial**
`remove_statistical_outlier(nb_neighbors, std_ratio)` removes points whose mean neighbour-distance is >k σ above the cloud average; `remove_radius_outlier(nb_points, radius)` removes points with too few neighbours in a sphere [src: open3d-outlier]. CPU, milliseconds on a room-scale cloud, no GPU. **Buys:** the NOISE class, cheaply and defensibly. **Unknown/band:** removed points = class-5 noise; the kept/removed split is itself a reportable number. **Cost:** negligible (Open3D `pip install open3d`).

### E2 — Geometric nearest-primitive assignment (point-to-line / point-to-footprint within tolerance) — **THE RECOMMENDED BASELINE**
For each surviving point: perpendicular distance to each fitted wall line (2D, trivial closed form); point-in-polygon test against each object footprint + height band. Assign to the nearest primitive *if within tolerance*, else → UNKNOWN. **Buys:** all five classes in one O(N·P) pass (N points, P primitives; P is tens, so effectively O(N)). **Unknown/band:** "within tolerance" gives UNKNOWN for free; residual = the assignment distance, aggregated → the error band directly. **Cost:** pure NumPy/CPU, sub-second on a room cloud. This is the honest formulation of our actual problem and the first thing to build.

### E3 — KNN / region-growing label propagation on existing labels
Seed from E2's confident assignments; propagate labels to nearby unclaimed points by k-NN majority vote or Euclidean region-growing (grow a region while neighbour distance < ε and normal deviation < θ). **Buys:** recovers points just outside E2's hard tolerance that clearly belong (object edges, wall fringes), shrinking the unknown set without lowering the global tolerance. **Unknown/band:** a point reached by no seed within ε stays UNKNOWN; growth distance contributes to the residual. **Cost:** CPU; k-d tree query, fast (Open3D/scipy `cKDTree`).

### E4 — Classical segmentation: RANSAC plane = wall, Euclidean clustering = objects
`SACSegmentation`(SACMODEL_PLANE) or Open3D `segment_plane` extracts wall planes directly from points; `EuclideanClusterExtraction`/DBSCAN clusters the non-plane remainder into object candidates [src: pcl-cluster, open3d-outlier]. **Buys:** an *independent, bottom-up* check on E2 — does the geometry agree with the upstream floor plan and object set? Disagreements flag bad primitives. Also generates **unidentified-object** clusters (class 3) for the diagnosis queue. **Unknown/band:** points in no plane and no cluster → UNKNOWN; RANSAC inlier-distance = wall residual, mirroring E2's band. **Cost:** CPU, seconds; standard PCL/Open3D, no GPU. Pairs naturally with [[floorplan-reconstruction-methods]] RANSAC-based methods (PolyFit, Progressive-X) which already score points by *unclaimed* support.

### E5 — Learned closed-vocab 3D semantic/instance segmentation (PointNet++ / KPConv / MinkowskiNet sparse-conv)
Per-point semantic labels from a trained network. SPVNAS reports 8–23× compute reduction / 3× speedup over MinkowskiNet and KPConv at higher accuracy [src: spvnas]; Mask3D (the OV-3DIS backbone) needs ≥8 GB VRAM and ~13 s/scene ([[ov3d-instance-seg]]). **Buys:** richer per-point semantics than geometry alone; a learned prior that can label points geometry can't. **Unknown/band:** closed-set nets force every point into a known class — UNKNOWN must be added via a softmax-confidence / max-logit reject threshold (see E7). **Cost:** GPU required (≥4–8 GB); training data needed (these are *not* zero-shot on our domain). Heavy relative to E1–E4; over-spec for the current 5-class problem.

### E6 — Open-vocabulary / learned 3D (OpenScene, OV3D, FOLK / Open-YOLO-3D)
Per-point CLIP-aligned features → arbitrary text-queried labels. OpenScene is a sparse-conv net predicting per-point open-set features from multi-view-fused CLIP supervision; OV3D aligns points to text via images [src: openscene-ov3d]. FOLK is the lightest 3D-native OV inference (~3.6 s/scene, est. ≥4–6 GB) but needs re-distillation on our domain ([[ov3d-instance-seg]]). **Buys:** would *populate* the labels that classes 1–2 assume, closing the loop with [[semantic-object-memory]]. **Unknown/band:** open-vocab cosine similarity gives a natural "below-threshold ⇒ none-of-the-above" UNKNOWN. **Cost:** GPU; offline-batch; passive-stereo depth holes (~48% coverage) are the binding constraint, not compute ([[ov3d-instance-seg]] §failure modes).

### E7 — Open-set / OOD 3D segmentation (explicit unknown-rejection methods)
Methods built specifically to *reject* the unknown: 3DOS benchmark (semantic novelty on point clouds), Adversarial Prototype Framework (CVPR 2023), probability-driven open-world 3D semseg (2024) [src: open-set-3d]. **Buys:** a principled, calibrated UNKNOWN class — exactly our class 4 — rather than a hand-set threshold. **Unknown/band:** this *is* the unknown class, learned. **Cost:** GPU + training; research-stage. Relevant only if E2–E4's geometric unknown proves insufficient — which is unlikely given we already have the primitives.

---

## Recommended first baseline

**Build E1 → E2 first, on CPU, in NumPy + Open3D.** Concretely:

1. **E1 noise gate:** Open3D `remove_statistical_outlier` (e.g. `nb_neighbors=20, std_ratio=2.0`) → class 5.
2. **E2 cascade:** for each surviving point, perpendicular distance to every wall line; if `< tol_wall` (set from expected depth noise) → WALL (record residual). Else point-in-footprint + height-band test against each object → IDENTIFIED OBJECT (record residual). Else → leftover.
3. **E3-lite cleanup:** DBSCAN/Euclidean cluster the leftovers; a coherent object-scale cluster → UNIDENTIFIED OBJECT (class 3); the rest → UNKNOWN (class 4).
4. **Error band:** per-wall RMS/p95 of perpendicular residuals; whole-map % explained / % unknown-recurring / % noise.
5. **Unknown diagnosis:** run the triage table; recurring-across-sweeps unknowns are kept, single-sweep ones are demoted to noise.

This is sub-second, no GPU, no training, fully reproducible — and it directly operationalises the project principle. E4 (RANSAC/Euclidean) is the **first follow-up** as an independent cross-check on the upstream primitives. E5–E7 (learned) are deferred: they are the right tool for *generating* labels ([[semantic-object-memory]], [[ov3d-instance-seg]]) but over-spec for *accounting* points against primitives we already hold, and all are gated by GPU + passive-stereo depth-hole limits already documented.

---

## Source

- [src: open3d-outlier] Open3D — *Point cloud outlier removal* tutorial (`remove_statistical_outlier`, `remove_radius_outlier`). https://www.open3d.org/docs/release/tutorial/geometry/pointcloud_outlier_removal.html
- [src: pcl-cluster] Point Cloud Library — *Euclidean Cluster Extraction* + *SACSegmentation / SACMODEL_PLANE* tutorials. https://pointclouds.org/documentation/tutorials/cluster_extraction.html
- [src: spvnas] Tang et al., *Searching Efficient 3D Architectures with Sparse Point-Voxel Convolution (SPVNAS)*, ECCV 2020 — 8–23× compute reduction / 3× speedup vs MinkowskiNet & KPConv. https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123730681.pdf
- [src: kpconv] Thomas et al., *KPConv: Flexible and Deformable Convolution for Point Clouds*, ICCV 2019. https://geometry.stanford.edu/lgl_2024/papers/tqdmgg-KPconv-iccv19/tqdmgg-KPconv-iccv19.pdf
- [src: openscene-ov3d] Jiang et al., *Open-Vocabulary 3D Semantic Segmentation with Foundation Models (OV3D)*, CVPR 2024; OpenScene (per-point CLIP-fused open-set features). https://openaccess.thecvf.com/content/CVPR2024/papers/Jiang_Open-Vocabulary_3D_Semantic_Segmentation_with_Foundation_Models_CVPR_2024_paper.pdf
- [src: open-set-3d] *3DOS: Benchmarking Semantic Novelty Detection on Point Clouds* (arXiv 2207.11554); Li et al., *Open-Set Semantic Segmentation for Point Clouds via Adversarial Prototype Framework*, CVPR 2023; *A Probability-Driven Framework for Open World 3D Point Cloud Semantic Segmentation* (arXiv 2404.00979).

*Captures: 2026-06-14. Existing wiki coverage of the learned-segmentation branch: [[ov3d-instance-seg]] (OV-3DIS compute/VRAM envelope, FOLK/Open-YOLO-3D, passive-stereo depth-hole failure modes), [[scene-graph-world-model]] (ConceptGraphs per-frame point-cloud→object pipeline incl. DBSCAN denoise + geometric+semantic association), [[room-segmentation-floor-plan]] (Roborock NN classifies pixels as room-inside/room-outside/noise — the closest prior 5-class analogue), [[floorplan-reconstruction-methods]] (RANSAC primitive fitting + unclaimed-point scoring).*

## Related

[[floorplan-reconstruction-methods]] · [[room-segmentation-floor-plan]] · [[semantic-object-memory]] · [[ov3d-instance-seg]] · [[scene-graph-world-model]] · [[robust-evidence-mapping-principle]] · [[passive-stereo-robustification]] · [[learned-point-cloud-registration]]
