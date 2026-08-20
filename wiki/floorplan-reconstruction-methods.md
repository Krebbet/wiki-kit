# Floorplan Reconstruction Methods — Beyond the Manhattan Rectangle Prior

Survey of five methods (ICCV 2017–NeurIPS 2025) relevant to improving the **EDA037 floorplan hypothesis algorithm** in drone-prototype. Each attacks one or more of EDA037's four documented weaknesses: greedy single-split topology search; Manhattan-only (0/90°) wall assumption; ~20% passive-stereo depth noise producing 0.6 m wall slabs; and hand-tuned thresholds with no principled global objective. All five methods are benchmarked on top-down 2D density maps or point clouds — the same data regime as EDA037.

**Related:** [[passive-stereo-room-mapping-campaign]] · [[mapping-stack-design]] · [[room-segmentation-floor-plan]] · [[apple-roomplan]] · [[stereo-dense-reconstruction]] · [[world-model-architecture]]

---

## Method comparison

| Method | Venue | Training? | Non-Manhattan | Noise target | EDA037 weakness addressed |
|---|---|---|---|---|---|
| **PolyFit** [src: 02-polyfit] | ICCV 2017 | ✗ geometry-only | ✓ arbitrary planes | σ = 0.6 m validated | Greedy splits → global BLP selection |
| **Progressive-X** [src: 03-progressive-x] | ICCV 2019 | ✗ geometry-only | ✓ any model class | 50% outlier ratio | Sequential fitting → joint simultaneous |
| **MonteFloor** [src: 04-montefloor] | ICCV 2021 | ✓ Structured3D | ✓ soft angle prior | Ambiguous density maps | Greedy search → MCTS global; hard Manhattan → soft prior |
| **RoomFormer** [src: 01-roomformer] | CVPR 2023 | ✓ Structured3D | ✓ native | Sparse/gappy clouds | Entire pipeline → learned end-to-end |
| **CAGE** [src: 05-cage-floorplan] | NeurIPS 2025 | ✓ Structured3D | ✓ native | Blurred density maps | Corner regression → edge regression; slab-tolerant closure |

---

## PolyFit — hypothesis-and-select via binary linear programming

*(Nan & Wonka, Visual Computing Center KAUST, ICCV 2017 [src: 02-polyfit])*

**Core idea:** cast 3D polygonal surface reconstruction as a *binary labelling* (face-selection) problem. RANSAC extracts candidate planar primitives; all pairwise plane intersections generate a large candidate face set; binary linear programming selects the optimal closed, manifold subset. No greedy steps, no user-specified topology — the BLP enforces watertight closure as a hard constraint.

**Three-term BLP objective** [src: 02-polyfit]:
1. **Data-fit** — confidence-weighted support (PCA eigenvalue ratio per plane); higher weight = crisper plane
2. **Model-complexity** — sharp-edge ratio penalty; suppresses overfitted bumps from noise
3. **Point-coverage** — α-shape coverage along each candidate face; penalises unwarranted blank regions

**Noise performance** [src: 02-polyfit]: Tested explicitly at Gaussian σ = 0.6 m on building-scale synthetic clouds — the same noise regime documented in [[passive-stereo-room-mapping-campaign]] (EDA016: ~20% per-pixel → ±0.6 m slab at 3 m). Reconstruction remains topologically correct at that level. A plane-refinement pre-pass (iterative angle-threshold merging with PCA refit, θ = 10°) removes RANSAC artefacts before candidate generation, reducing the candidate pool by ~3.4× and BLP runtime by >4×.

**Key constraint:** PolyFit operates on 3D planar surfaces. Applying it to EDA037's 2D problem requires collapsing to a 2D BLP: wall-plane candidates become 2D line hypotheses; the manifold constraint becomes a closed-polygon constraint. *(synthesis — 2D adaptation not validated in the paper)*

---

## Progressive-X — anytime joint multi-model fitting

*(Barath & Matas, Czech TU / MTA SZTAKI, ICCV 2019 [src: 03-progressive-x])*

**Core idea:** discover all model instances (lines, planes, homographies) *jointly* rather than sequentially. The algorithm interleaves RANSAC-style hypothesis proposal with energy-minimisation-based consolidation, repeatedly proposing hypotheses, fast-rejecting with minhash Jaccard similarity, and integrating survivors into the kept set via α-expansion graph-cut label assignment.

**Key property — compound quality function** [src: 03-progressive-x]: the modified MSAC score (Eq. 3) zeroes the contribution of points already explained by the current compound model (all active instances). Each new wall proposal is scored *only* on genuinely unclaimed points. This eliminates double-claiming at corners — the documented EDA037 failure where points near a corner are claimed by both adjacent edges, distorting both fits.

**Automatic instance count** [src: 03-progressive-x]: termination fires when the probability of finding another model with ≥ m+1 inliers falls below 1−µ (RANSAC-derived criterion, Eq. 5). No user-specified wall count.

**Anytime property** [src: 03-progressive-x]: if interrupted, the returned instances are real and dominant. Suitable for time-budgeted drone hover passes.

**Key results** [src: 03-progressive-x]: 2D line fitting at 50% outlier ratio — 1 false-negative, 0 false-positives across all tested scenes (stair4/star5/star11). LiDAR plane+cylinder fitting: 33.7% vs 35.7% for next-best (Multi-X), 3 orders of magnitude faster (9.4 s vs 1407 s). Open-source: `github.com/danini/progressive-x`, pip-installable (`pygcransac`).

---

## MonteFloor — MCTS search over polygon topologies

*(Stekovic, Rad, Fraundorfer, Lepetit; Graz TU / École des Ponts ParisTech; ICCV 2021 [src: 04-montefloor])*

**Core idea:** replace greedy polygon construction with Monte Carlo Tree Search (MCTS). A Mask-RCNN proposes room segment candidates from the density map; Douglas-Peucker at multiple ε values generates a polygon proposal pool; MCTS uses UCB selection to jointly evaluate proposal sets, scoring them holistically against the density map rather than edge-by-edge. A differentiable winding-number renderer enables gradient-based vertex refinement within the MCTS loop.

**Soft angle prior** [src: 04-montefloor]: the angle regularization term uses a mixture-of-Gaussians over cosine(angle) that soft-snaps near-right angles to 90° but accepts any angle in [π/6, 5π/6]. Explicitly non-Manhattan: the paper states the method handles "Manhattan and non-Manhattan scenes with the same complexity." Floor-SP (the prior SOTA) requires a dominant Manhattan frame; MonteFloor does not.

**Differentiable polygon refinement** [src: 04-montefloor]: after MCTS selects a topology, gradient descent on vertex coordinates minimizes a composite loss (data fit + soft angle regularization + non-overlap). An L0 anchor term prevents drift from the density map evidence during refinement. This is qualitatively distinct from EDA037's snap-to-nearest-Manhattan-line post-processing — it is a principled continuous optimization of vertex positions.

**Key results** [src: 04-montefloor]: outperforms Floor-SP on Room, Corner, and Corner-Angle on Structured3D; ~11× faster (71 ± 40 s vs 785 ± 549 s). Cross-dataset generalization (Structured3D → Floor-SP domain) holds without retraining.

**Training dependency**: two learned components — Mask-RCNN (room masks from density maps) and a metric network (CNN scoring IoU between proposed plan and GT). Both trained on Structured3D; cross-domain use degrades but remains competitive.

---

## RoomFormer — end-to-end transformer from density map to polygon

*(Yue, Kontogianni, Schindler, Engelmann; ETH Zurich / ETH AI Center; CVPR 2023 [src: 01-roomformer])*

**Core idea:** reformulate floorplan reconstruction as a *single-stage structured prediction* problem. A Transformer with two-level queries — one level per room, one level per corner — directly predicts a variable number of closed room polygons from a 256×256 top-down density map. Hungarian matching makes the network end-to-end trainable. No hand-crafted intermediate stages.

**Input format** [src: 01-roomformer]: a 256×256 grayscale density map produced by projecting a 3D point cloud vertically and normalizing point counts per pixel. Directly compatible with EDA037's data pipeline (the SfM wall-point cloud + metric floor frame already defines this projection).

**Non-Manhattan handling** [src: 01-roomformer]: Structured3D explicitly contains both Manhattan and non-Manhattan layouts; RoomFormer imposes no orthogonality constraint in its architecture. Polygon corners take arbitrary (x, y) positions.

**Noise robustness** [src: 01-roomformer]: qualitative results show substantially better handling of sparse/gappy input than HEAT (the prior SOTA). The multi-scale deformable attention encoder aggregates local and global context, bridging density gaps. Robustness is *learned*, not modelled explicitly — contingent on training data resembling the test distribution.

**Key results** [src: 01-roomformer]: Structured3D — Room F1 97.3, Corner F1 87.2, Angle F1 81.2 (SOTA at time of publication). Cross-dataset (trained on Structured3D, tested on SceneCAD without fine-tuning): Room IoU 74.0 vs prior SOTA 52.5 (+21.5 IoU). Inference 0.01 s per scene.

---

## CAGE — edge-centric polygon reconstruction (NeurIPS 2025)

*(Liu et al.; Wuhan University of Technology / University of Twente / others; NeurIPS 2025 [src: 05-cage-floorplan])*

**Core idea:** represent each wall as a *directed edge token* (2 endpoints + binary validity flag) rather than as a corner vertex. Endpoints can land anywhere along the wall — not at the precise corner — which makes the representation tolerant of smeared, thick, or partially-occluded wall evidence. Closed polygon vertices are recovered by geometric intersection of adjacent edge lines, not by snapping endpoints together.

**Why edges beat corners under noise** [src: 05-cage-floorplan]: a single noisy or missing corner breaks a corner-based polygon; a noisy edge direction still defines the correct wall line, and intersection with the adjacent edge recovers the corner position. The paper states: "edges are empirically more stable in sparse or noisy conditions since they encode directionality explicitly, whereas corner-based methods require precise vertex localization." Ablation: replacing the corner module with the edge module alone raises Corner F1 85.5% → 89.0% and Angle F1 79.5% → 83.2%.

**Denoising training strategy** [src: 05-cage-floorplan]: perturbed queries inject controlled Gaussian noise (scale ~0.4× density-map extent) onto ground-truth edge coordinates, with random validity flips (probability γ). The decoder is trained to recover clean edges from corrupted inputs — explicitly teaching noise-robustness to inputs matching the passive-stereo slab regime.

**Edge-intersection closure** [src: 05-cage-floorplan]: four geometric intersection types (line × line in 2D) are used to recover polygon vertices from adjacent edge predictions. Deterministic and stable even when endpoint predictions are offset.

> *(editorial caveat)* CAGE's training data is Structured3D (synthetic photo-realistic) and ScanNet RGB-D — both substantially higher-quality than raw passive-stereo SfM clouds. The claim "edge representation recovers clean geometry from blurred density maps" is architecturally sound but has not been validated on passive-stereo–derived density maps specifically. The 0.6 m wall-slab problem documented in [[passive-stereo-room-mapping-campaign]] may still limit the quality of the density map fed to CAGE, regardless of the representation choice. *(end editorial)*

**Key results** [src: 05-cage-floorplan]: Structured3D — Room F1 99.1%, Corner F1 91.7%, Angle F1 89.3% (current SOTA, surpassing FRI-Net by +3.9 Corner F1). Cross-dataset (Structured3D → SceneCAD): Room IoU 85.6% — best generalization of all compared methods.

---

## Applicable improvements to EDA037

*(synthesis — all items below are editorial interpretation of the sources, not source claims)*

The five methods collectively suggest **four levers**, ordered by implementation cost:

### Lever 1 — Edge-fitting closure (CAGE insight, no training needed)

EDA037 currently fits corner positions and then closes the polygon. CAGE's result (ablation: +3.5 Corner F1 from edge vs corner representation) argues for reframing: fit *directed edges* (line direction + two extent endpoints) and close via line-line intersection. The implementation change is small — `fit_line_segment_manhattan` already produces a line; the change is to return the line's *infinite direction + offset* rather than clipped endpoints, and intersect adjacent lines to recover vertices. This directly addresses the wall-slab problem: endpoints on a 0.6 m slab still define the correct wall direction; intersection extracts the crisp corner.

### Lever 2 — Progressive-X joint wall-line detection (no training, pip-installable)

Replace the sequential per-edge fitting loop with Progressive-X (`pygcransac`) running on the 2D boundary-point set. All wall lines are discovered jointly; the compound quality function eliminates double-claiming at corners; automatic termination determines the wall count from data. This is a near-drop-in replacement for EDA037's `estimate_dominant_axis` + `init_rectangle` + greedy-split chain. Implementation: `pip install pygcransac`; pass `VanishingPoint` or `Line2D` model class; input the outermost-return boundary points.

### Lever 3 — Soft angle prior replacing hard Manhattan snap (MonteFloor idea, no training)

Replace `fit_line_segment_manhattan`'s hard axis-snap (`max(axis_dirs, key=lambda d: abs(d @ edge_dir))`) with a soft penalty that encourages 90° angles but accepts any angle. MonteFloor's mixture-of-Gaussians prior over cosine(angle) with a 90°-peaked component is the principled form; a simpler implementation is to allow any wall direction and add a cost term `λ * (1 - |d @ nearest_axis|)` that penalises non-Manhattan angles without forbidding them. This unblocks L-shaped rooms, bay windows, and angled partitions.

### Lever 4 — PolyFit-style global BLP scoring (no training, replaces MDL gate)

Replace EDA037's per-edge `MDL_PENALTY` gate with PolyFit's three-term BLP objective over all candidate wall hypotheses simultaneously: data-fit (PCA eigenvalue ratio of support points), complexity (segment count penalty), coverage (fraction of boundary points within tolerance of any selected segment). Solve as an integer linear program over the candidate set (e.g. via `scipy.optimize.milp` or `pulp`). This is a global optimum rather than a sequential greedy gate.

### Lever 5 — RoomFormer/CAGE inference benchmark (training required, validation only)

Run pretrained RoomFormer (weights at `github.com/ywyue/RoomFormer`) with no fine-tuning on EDA037's SfM density maps. Use as an upper-bound benchmark: if pretrained RoomFormer on our density maps achieves meaningfully better polygon quality than the classical levers above, it motivates fine-tuning on our data. If it does not — because the training domain (clean synthetic Structured3D) is too far from passive-stereo SfM — then the classical improvements are the productive path and learning is a later-stage investment.

---

## Source

| File | Origin |
|---|---|
| `raw/research/floorplan-hypothesis-methods/01-roomformer.md` | arXiv 2211.15658, CVPR 2023 — Yue et al., ETH Zurich. Captured 2026-06-09 (marker engine). |
| `raw/research/floorplan-hypothesis-methods/02-polyfit.md` | ICCV 2017 — Nan & Wonka, KAUST. CVF open-access. Captured 2026-06-09 (marker engine). |
| `raw/research/floorplan-hypothesis-methods/03-progressive-x.md` | arXiv 1906.02290, ICCV 2019 — Barath & Matas. Captured 2026-06-09 (marker engine). |
| `raw/research/floorplan-hypothesis-methods/04-montefloor.md` | arXiv 2103.11161, ICCV 2021 — Stekovic et al., Graz TU. Captured 2026-06-09 (pymupdf; figures unavailable). |
| `raw/research/floorplan-hypothesis-methods/05-cage-floorplan.md` | arXiv 2509.15459, NeurIPS 2025 — Liu et al., Wuhan UT. Captured 2026-06-09 (pymupdf; figures unavailable). |

## Related

[[passive-stereo-room-mapping-campaign]] — the wall-slab root cause (20% noise → ±0.6 m) that all methods must contend with  
[[mapping-stack-design]] — floor plan as "Next step 1" in the prototype stack  
[[room-segmentation-floor-plan]] — 2D occupancy-grid segmentation methods (ROSE², Voronoi); different pipeline from the density-map methods here  
[[apple-roomplan]] — iPhone LiDAR + ANE production ceiling (sub-60s, ±5 cm); the hardware-rich benchmark  
[[stereo-dense-reconstruction]] — why passive-stereo walls are sparse/noisy (SGBM ~50% coverage → hollow walls)  
[[world-model-architecture]] — layered world model context for where the floor plan fits  
[[anchor-map-protocol]] — the hloc SfM pipeline that produces the point cloud these methods consume
