# Room Shape / Topology Recovery from Noisy Indoor Data — Getting the SHAPE Right Under Metric Noise

How to recover a **topologically-correct** room floor plan — the wall graph (ordered wall segments
+ corners), including **non-convex shapes (cut-ins, alcoves, niches, jogs)**, **doors/openings as
first-class elements**, and **permanent furniture placed in the plan** — from noisy indoor 3D /
point-cloud / free-space data, while *deliberately not requiring metric accuracy* (segment lengths can
be wrong as long as the layout is qualitatively right).

This page is the **shape-vs-metric synthesis**: it organises the method families by *what they give you
for SHAPE* and *how robust the shape is when the metric input is heavily corrupted* — the regime of
[[passive-stereo-room-mapping-campaign]] (the *same pixel* wobbles ~20% across frames → a 3 m wall lands
in a ±0.6 m slab, and free-carve overshoots blank walls ~3.7×). It is complementary to two existing
pages and does not repeat their per-method detail:

- [[floorplan-reconstruction-methods]] — deep per-method writeups of PolyFit, Progressive-X, MonteFloor,
  RoomFormer, CAGE (the density-map / point-cloud learned+classical pipeline, mapped onto the EDA037
  floorplan algorithm). **Read that page for the mechanics; this page for the shape/topology lens.**
- [[room-segmentation-floor-plan]] — partitioning a *2D occupancy grid* into rooms, doorway detection
  (Voronoi critical points + visual refinement), semantic labelling (ROSE², SeLRoS, Roborock patent).

**Related:** [[floorplan-reconstruction-methods]] · [[room-segmentation-floor-plan]] ·
[[passive-stereo-room-mapping-campaign]] · [[mapping-stack-design]] · [[apple-roomplan]] ·
[[stereo-dense-reconstruction]] · [[2d-lidar-slam]] · [[slam-toolbox]] · [[world-model-architecture]]

---

## The framing: SHAPE/TOPOLOGY is a separate, easier problem than METRIC accuracy

*(synthesis)* The central design choice on this page is to treat **topology** (how many walls, in what
cyclic order, with which corners and openings, and which jogs/alcoves) as the target, and to treat
**metric** (exact lengths and positions) as a "nice to have" that the noisy passive-stereo input cannot
currently deliver anyway. This buys real robustness, because most of the noise in our data is *metric*
(±0.6 m slab thickness, 3.7× overshoot) while the *topology* (a roughly-L-shaped room with a doorway in
the long wall and a couch against the south wall) is usually recoverable even from a smeared map.

Two ideas recur across the literature as the levers that make topology robust to metric noise:

1. **Fit lines/edges, recover corners by intersection — never localise corners directly.** A noisy or
   missing corner breaks a corner-based polygon; a noisy *edge direction* still defines the correct wall
   line, and intersecting adjacent edge-lines recovers the corner crisply (CAGE's central result, see
   [[floorplan-reconstruction-methods]]; same principle underlies Floor-SP and the cell-complex methods
   below). This directly defeats the ±0.6 m slab: a slab still has a well-defined long axis.
2. **Decide the wall *count* by a global model-selection objective, not greedily.** Whether the room is a
   rectangle, an L, or a U is a *model-complexity* decision. Greedy splitting overfits to noise; a
   global objective with an explicit complexity penalty (BLP, energy min-cut, MDL, MCTS) resists adding
   spurious walls to chase noise bumps. This is the answer to "how many walls/corners and where, without
   over-fitting."

The rest of the page is organised by method family, each scored on: **SHAPE** (non-convex / wall-count
decision), **doors**, **cut-ins/alcoves**, **furniture-in-plan**, **input assumptions**, **noise
robustness**, and **fit to our setup**.

---

## Capability matrix (the one-screen summary)

| Family | Non-convex SHAPE / how it picks wall count | Doors as topology | Cut-ins / alcoves | Furniture in plan | Input it wants | Noise robustness | Fit to us |
|---|---|---|---|---|---|---|---|
| **Concave-hull / α-shape boundary** | Boundary traced from points; α controls concavity (no explicit count) | ✗ (a door reads as a concavity, not labelled) | ✓ if α tuned | ✗ (furniture pollutes the hull) | 2D projected points or free-space cells | Low–med: very sensitive to α + outliers | **High as a first pass** — trivial on our free-space boundary |
| **Occupancy-grid → vectorized polygon** (contour + Douglas-Peucker) | Polygon vertices = simplified contour; ε sets vertex count | ✗ (gap = vertex, not a door) | ✓ naturally | ✗ (furniture = occupied = boundary) | 2D occupancy grid | Med: ε trades detail vs noise | **High for the incoming LiDAR**; rough on free-carve |
| **Cell-complex / space-partition** (KSR, Fang-Lafarge, PolyFit-2D) | Plane/line primitives partition the plane; **energy min-cut / BLP picks the wall subset** → wall count emerges, watertight | △ opening = unselected face (recoverable) | ✓ arbitrary angles, non-convex | △ via separate primitive class | planar primitives from cloud | **High** (PolyFit validated at σ=0.6 m) | **High** — principled, no training |
| **Primitive-fit + model selection** (RANSAC + MDL, Progressive-X) | MDL / RANSAC stopping picks #lines; joint fit avoids double-claim at corners | ✗ directly | ✓ each wall fit independently | △ separate models | 2D boundary points | **High** at 50% outliers (Progressive-X) | **High** — `pygcransac` drop-in |
| **Manhattan / Atlanta layout fit** | Snap to 1 (Manhattan) or *k* dominant directions (Atlanta) | ✗ | △ (cut-ins OK if axis-aligned; Atlanta allows angled walls) | ✗ | dominant-direction histogram | High *if* the world matches the assumption | Med — most rooms ≈ Manhattan but not all |
| **Learned floor-plan** (RoomFormer, HEAT, MonteFloor, Floor-SP, CAGE) | Network/MCTS predicts variable #rooms+corners; non-Manhattan native | △ some predict openings; mostly walls only | ✓ native | ✗ (layout only; furniture is a separate head) | **256² density map** (clean) | Learned, **but OOD on our passive data** | **Low now / benchmark-only** (domain gap) |
| **Semantic structural mapping** (SceneCAD, Structured3D-semantics) | Layout planes from corner→edge→quad hierarchy | ✓ (doors/windows are layout classes in Structured3D) | ✓ | **✓ — CAD/footprint placed jointly with layout** | RGB-D scan | Med (real ScanNet) | **Low now** (needs RGB-D + training), **concept is the target** |

Legend: ✓ first-class · △ partial/derivable · ✗ not addressed.

---

## Family 1 — Free-space / boundary tracing (the simplest, and the best fit for our data *today*)

This is the family that directly answers research question 4 ("is the free-space boundary a good *shape*
signal despite metric overshoot?"). **Yes — for shape, with caveats.**

### Concave hull / α-shape

The **α-shape** generalises the convex hull: it is a family of piecewise-linear curves where the
parameter α controls how concave the boundary may be. Large α → convex; small α → tightly hugs
concavities and can even open holes. The convex hull *cannot* capture concavity or cut-ins; the α-shape
can, which is exactly what a non-convex room needs ([floor-plans-from-point-clouds (GRAPP 2019)],
[alphashape PyPI]). Building-footprint extraction explicitly uses α-shapes because they "capture building
shape with high accuracy."

- **SHAPE:** good — recovers an L / U / jogged outline if α is tuned. **No explicit wall-count
  decision** — the polygon vertex count falls out of α and point density, which is also its weakness
  (under-tuned α invents jagged spurious corners from noise).
- **Doors / cut-ins:** a real doorway and an alcove both read as *concavities*; the method cannot tell
  them apart or *label* a door — that needs a separate opening detector (Family 5).
- **Furniture:** a couch against a wall pollutes the hull — its footprint becomes part of the "room
  boundary," pulling the wall inward. (This is the furniture-as-occluder problem; see Family 7 for how to
  use it *constructively* instead.)
- **Fit to us:** **high as a first-pass shape estimate.** Our free-carve already produces a confidently
  free region; its boundary is a navigable outline. `pip install alphashape`, project the free cells /
  boundary points to 2D, sweep α. The known failure — free-carve **overshoots blank walls ~3.7×**
  (EDA011) — means the α-shape outline will be *metrically too big*, but its *topology* (where the
  cut-ins and the doorway-gap are) is informative. Use it for SHAPE, not for lengths.

### Occupancy-grid → vectorized polygon (contour + Ramer-Douglas-Peucker)

The robotics-standard route from a 2D grid to a polygon: extract the free-space boundary contour
(OpenCV `findContours` on the occupancy image), then **Douglas–Peucker (RDP)** line-simplification to
collapse the staircased contour into a small set of vertices ([static-free-space-OGM (arXiv 1801.00600)],
[floor-plan-vectorization (Springer 2020)]). The RDP tolerance ε is the single shape/noise knob: larger ε
= fewer vertices = smoother (drops detail, including small alcoves); smaller ε = keeps cut-ins but also
keeps noise wiggles. A **rectilinear-polygon** variant ("min-vertex best-fit rectilinear polygon within
tolerance") is preferred over plain RDP when you want clean right-angle corners and to "remove steps at
non-parallel walls."

- **SHAPE:** non-convex naturally (a contour follows jogs); **vertex count set by ε**, not a principled
  objective — so it over/under-fits with the threshold like the α-shape.
- **Doors / cut-ins:** a doorway gap becomes two extra vertices, not a labelled opening; cut-ins are kept
  if ε is small enough.
- **Fit to us:** **this is the natural shape extractor for the incoming 2D LiDAR's occupancy grid** (see
  "What the LiDAR changes"). On the free-carve grid today it works but inherits the 3.7× overshoot.

> *(synthesis)* Both boundary-tracing methods are **threshold-driven, not model-selection-driven** — they
> answer "where is the boundary" but punt on "how many walls *should* there be." That is why, for a
> trustworthy topology, you graduate from a traced boundary to a *fitted* one (Families 2–3).

---

## Family 2 — Cell-complex / space-partitioning (the principled "watertight by construction" route)

These methods **partition the plane (or 3D space) into convex cells using detected primitives, then
select the subset of cell faces that form the surface by global energy minimisation.** Topology
(closure, manifoldness) is a *hard constraint*, so the output is watertight by construction — you cannot
get a dangling wall or an unclosed room. This is the most robust *classical* answer to "decide the wall
count without over-fitting."

### KSR — Kinetic Shape Reconstruction (Bauchet & Lafarge, TOG 2020 / CGAL 6.1)

Planar primitives extracted from the cloud are grown kinetically at constant speed until they collide,
partitioning the bounding volume into **convex polyhedra**; the final surface is the subset of faces
chosen by an **energy formulation trading data-fidelity against low complexity, solved via min-cut**
([Kinetic Shape Reconstruction (TOG 2020)], [CGAL Kinetic Surface Reconstruction]). "Planar components
(beams, walls, windows) are captured by large facets, freeform objects (tables) by a low number of
facets." Watertight is guaranteed because the result is a union of cell volumes. **Now shipping in CGAL**
(Kinetic Space Partition + Kinetic Surface Reconstruction packages, [CGAL 2024 announcement]).

### Fang & Lafarge — Floorplan from point clouds via space partitioning (ISPRS J. 2021)

The 2D specialisation that is most directly on-target. It **decomposes the floor plane into a polygonal
partition and selects the edges belonging to walls by energy minimisation** — explicitly replacing the
fragile corner-detection step with a space-partition data structure, "offering high robustness to
imperfect data" ([Fang-Lafarge JPRS 2021 (VCC/Shenzhen)], [ScienceDirect S0924271621000538]). Demonstrated
on **both RGB-D and LiDAR** point clouds from simple to complex (non-rectangular) scenes; competitive
geometric accuracy with simpler output (fewer vertices) than prior work.

- **SHAPE:** arbitrary angles, non-convex; **wall count emerges from the min-cut complexity term** — the
  principled decision we want.
- **Doors / openings:** an opening is a region the energy chooses *not* to fill with a wall face;
  recoverable as a gap, though not semantically labelled "door."
- **Furniture:** handled as separate (small-facet) primitives in KSR; in the 2D floor variant furniture
  must be removed first or it competes for wall faces.
- **Noise:** the headline selling point — robust to "imperfect data," validated on real LiDAR.
- **Fit to us:** **high.** No training. The 2D energy-min formulation is the natural successor to a
  traced boundary. (PolyFit, the BLP cousin validated at σ=0.6 m — our exact noise — is written up in
  [[floorplan-reconstruction-methods]]; PolyFit and KSR/Fang-Lafarge are the same family: hypothesise
  primitives → globally select a watertight subset.)

---

## Family 3 — Primitive fitting with explicit model selection (RANSAC/MDL, Progressive-X)

The lightest principled route: fit wall *lines* to the boundary points and let an information criterion
decide how many.

- **RANSAC + MDL:** RANSAC proposes plane/line primitives; **Minimum Description Length picks how many**
  by minimising (bits to describe the model) + (bits to describe the data given the model) — the formal
  cure for overfitting the wall count ([Yang & Förstner, Plane Detection in Point Cloud Data],
  [modelselection.org/mdl]). "MDL is essential for deciding how many planes exist… avoids detecting wrong
  planes due to complex geometry."
- **Progressive-X (ICCV 2019):** discovers all wall lines *jointly*; its compound quality function zeroes
  points already explained, **eliminating double-claiming at corners**, and a RANSAC-derived stopping
  rule sets the line count automatically. Validated on 2D line fitting at **50% outlier ratio**
  (`pygcransac`, pip-installable). Full writeup: [[floorplan-reconstruction-methods]].

- **SHAPE:** non-convex via independent per-wall lines; **count from MDL / RANSAC stopping** (principled).
- **Doors / furniture:** not addressed directly — a door is just a region with no supporting line;
  furniture lines may be mis-fit as walls unless filtered.
- **Fit to us:** **high, low-effort.** `pygcransac` on the 2D boundary point set is close to a drop-in for
  the EDA037 greedy split chain.

---

## Family 4 — Manhattan / Atlanta-world layout fitting (cheap priors, but assumption-bound)

- **Manhattan world:** assume all walls align to *one* orthogonal frame (0/90°). Snapping to it is the
  cheapest possible regulariser and crushes metric noise, but it **cannot represent a 45° wall, a bay, or
  an angled partition** — and EDA037's Manhattan-only assumption is a documented weakness
  ([[floorplan-reconstruction-methods]]).
- **Atlanta world:** the generalisation — *one* vertical frame but **multiple horizontal directions**, so
  each wall may have its own angle and must be extracted independently ([AtlantaNet (ECCV 2020)],
  [Globally optimal Atlanta direction (arXiv 1904.12717)]). This handles a room whose walls meet at, say,
  120° (kitchen islands, angled hallways) that Manhattan would mangle.

- **SHAPE:** Manhattan handles axis-aligned cut-ins/L-rooms; Atlanta adds angled walls. Neither *decides*
  the count — they constrain *directions*, and pair with a count method (Families 2–3).
- **Fit to us:** **medium.** Use the Manhattan/Atlanta direction prior as a *soft* snap (MonteFloor's
  mixture-of-Gaussians-over-cosine, [[floorplan-reconstruction-methods]] Lever 3) on top of a count
  method — gets the regularisation benefit without forbidding the occasional angled wall. Most home rooms
  are ≈Manhattan, so the prior is usually right and cheap.

---

## Family 5 — Doors / openings as first-class topological elements

A door is a *navigable gap in the wall ring* — and the hard part is telling it apart from (a) an
occlusion / blank-wall dropout (no points, but it's a wall) and (b) a furniture gap.

- **Open-door = rectangular hole in a wall plane; closed-door = sub-region of the wall plane.** The
  canonical point-cloud detector finds **rectangular data-holes in fitted wall planes** for open doors,
  and processes rectangular surface sub-regions for closed doors ([door-detection-3D-point-clouds
  (Automation in Construction 2017)], [windows-doors-extraction (MDPI Buildings 2023)]). **Voxel-based
  visibility analysis distinguishes "occluded" from genuinely "empty"** wall regions — the key trick to
  not mistake a blank-wall dropout (occluded) for a real opening (empty / see-through).
- **Geometry-only from a grid: Voronoi critical points** — narrow points (local minima of free-space
  width) in the Voronoi graph are doorway candidates; cheap but high false-positive from furniture gaps
  ([[room-segmentation-floor-plan]]).
- **Free-space flow-through:** if confidently-free space passes *through* a gap in the wall ring into
  another free region, that gap is very likely a door — our free-carve, which overshoots through openings,
  is actually a *positive* signal here (it flows through real doorways).
- **Visual refinement** (ICRA 2025 active segmentation; door-status DNN) resolves the
  furniture-gap-vs-door ambiguity and reads open/closed status — needs RGB ([[room-segmentation-floor-plan]]).

- **Fit to us:** **geometry-only candidates now** (Voronoi critical points + free-space flow-through on
  the carve/grid), with the **visibility "occluded-vs-empty" test** as the discriminator to avoid calling
  blank-wall dropouts "doors." Visual confirmation is a later RGB pass. With the LiDAR, the wall ring is
  crisp enough that the rectangular-hole / gap-in-ring detector becomes directly usable.

---

## Family 6 — Learned floor-plan reconstruction (high ceiling, but OOD on our data today)

End-to-end networks that map a top-down **density map** (256², point-counts-per-pixel) to a vectorized
plan. Detailed mechanics, metrics, and our-data caveats are in [[floorplan-reconstruction-methods]];
summarised here for the shape/topology lens:

- **RoomFormer (CVPR 2023):** transformer, two-level queries (room / corner), predicts a variable number
  of closed polygons; non-Manhattan native; Structured3D Room F1 97.3 / Corner F1 87.2.
- **HEAT (CVPR 2022):** reconstructs a **planar graph** by detecting corners then classifying edge
  candidates between them with holistic edge attention — a clean "edges decide the topology" formulation;
  non-Manhattan; from a point-density image ([HEAT project page], [HEAT (arXiv 2111.15143)]).
- **MonteFloor (ICCV 2021):** **MCTS over polygon topologies** + soft (non-Manhattan) angle prior +
  differentiable refinement — the explicit global topology *search*.
- **Floor-SP (ICCV 2019):** room-wise **shortest-path loops** via coordinate descent; objective =
  data + adjacent-room consistency + **model-complexity term**; no corner/edge primitive extraction;
  validated on **527 real apartments including many non-Manhattan units** ([Floor-SP (ICCV 2019)],
  [floor-sp project]).
- **CAGE (NeurIPS 2025):** edge-centric (directed-edge tokens, corners by intersection) — the most
  noise-robust representation in the family; Structured3D Room F1 99.1.

- **SHAPE / doors / cut-ins:** all handle variable room count and non-Manhattan natively; some predict
  openings, most predict walls only. Topology is their strength.
- **Furniture:** layout only — furniture is a *separate* prediction head, not placed in the plan by these.
- **Fit to us:** **low *now*, benchmark-only.** Their density-map input assumes clean ScanNet /
  Structured3D quality. Our ~20%-per-pixel noise *degrades the density map itself* — the slab is in the
  input, not just the fitter — so a learned method may infer better from a blurred map but does **not**
  un-blur it (see [[passive-stereo-room-mapping-campaign]] §d2). **Use pretrained RoomFormer/CAGE as an
  upper-bound probe** (proposed EDA046) before any fine-tuning investment.

---

## Family 7 — Semantic structural mapping: furniture *in* the plan (the target architecture)

This family answers research question 3: detecting large static furniture and **placing it in the floor
plan as a structural element**, and using **wall-adjacent furniture to define the boundary behind it.**

- **SceneCAD (ECCV 2020):** **jointly** predicts CAD-object alignments *and* the layout, from an RGB-D
  scan, with a message-passing GNN modelling object↔object and object↔layout relations. Layout planes are
  built hierarchically — **corners (heatmap + NMS) → edges (corner-pair binary classification) → valid
  quads of four connected edges** — and modelling the global layout *improves* the object alignment
  (50.05% → 61.24% on ScanNet) ([SceneCAD (ECCV 2020)], [SceneCAD GitHub]). This is the architecture our
  world model is aiming at: structure + furniture, co-estimated, mutually constraining.
- **Structured3D semantics:** the synthetic dataset that trains most of Family 6 carries doors, windows,
  and furniture as labelled layout/semantic classes — which is why the learned methods *could* emit doors
  and furniture given the right heads.
- **Furniture-as-occluder, used constructively:** "Room Envelopes" (2025) and occluded-surface-completion
  work explicitly model that walls are commonly hidden behind couches/wardrobes, and **infer the wall
  line behind the furniture** ("detected lines between disconnected walls = occlusion lines"); a
  wall-adjacent large object thus *defines* the boundary that the sensor never saw
  ([Room Envelopes (arXiv 2511.03970)], [Behind the Veil (arXiv 2404.03070)]).

- **Fit to us:** **the concept is exactly our target; the methods need RGB-D + training now.** But we
  already have the pieces to do a *lightweight, classical* version (see recommendation): YOLO11-seg
  furniture footprints + T_map_object placement already exist (EDA023/024,
  [[world-model-architecture]], [[object-fingerprint-memory]]); a couch footprint whose back edge is
  collinear with neighbouring wall fragments *is* the wall behind it. This turns our "furniture pollutes
  the boundary" problem (Family 1) into "wall-adjacent furniture *completes* the boundary."

---

## Recommendation — the simplest robust path to a topologically-correct room shape on OUR data

*(synthesis — editorial, not a source claim)*

**Goal restated:** a qualitatively-correct wall graph (ordered segments + corners), with doors and
cut-ins/alcoves marked and permanent furniture placed in it — *not* metric lengths.

### On the passive-stereo + free-carve + object-detection data we have *today*

A **three-stage classical pipeline, no training, all pip-installable**, that leans on model-selection for
the topology and treats every metric number as provisional:

1. **Boundary from free-space (shape signal), not from walls.** Take the confidently-free region from the
   carve, project to 2D, extract its outer boundary. Use it for **shape only** — accept the ~3.7×
   overshoot; the *topology* (where the cut-ins and doorway-gaps sit) is the informative part. (Family 1.)
   This is the honest move given EDA011/016: our walls are slabs but our free-space *boundary* is a
   coherent outline.
2. **Fit the wall graph with explicit model selection — edges, not corners.** Run **Progressive-X
   (`pygcransac`) or RANSAC+MDL** on the boundary point set to get wall *lines* jointly, with the count
   chosen by the stopping/MDL criterion; **recover corners by intersecting adjacent lines** (CAGE
   principle). Add a **soft Manhattan/Atlanta angle prior** (penalise, don't forbid, off-axis walls) so
   most corners snap to 90° while a genuine angled wall survives. Equivalently, the **2D space-partition +
   energy-min** (Fang-Lafarge / PolyFit-2D) gives the same topology with a watertight guarantee — pick
   whichever is less code. (Families 2–4.) This is where the *robust shape under noise* actually comes
   from: edges + global count selection beat the slab.
3. **Doors and furniture as overlays on the closed ring.** Doors: **Voronoi critical points +
   free-space-flow-through**, filtered by the **occluded-vs-empty visibility test** so blank-wall
   dropouts aren't mislabelled openings (Family 5). Furniture: take the **YOLO11-seg footprints we
   already produce**, place them by `T_map_object`, and where a large static footprint (couch, cabinet)
   sits against a boundary gap, **use its back edge to complete the wall behind it** (Family 7's
   constructive use of occlusion).

**Why this is the simplest *robust* choice:** it never asks the noisy data for a corner location or a wall
length; it asks only for *line directions* and a *global count*, both of which survive the ±0.6 m slab. It
needs no GPU, no training, and no data we don't already have. Skip the learned floor-plan nets for now —
their density-map input is OOD on our noise (run pretrained RoomFormer/CAGE only as an *upper-bound
benchmark*, EDA046, to decide if fine-tuning is ever worth it).

**Hardest residual risk:** the free-carve overshoot means stage 1's boundary is metrically inflated, so
stage 2's *lengths* will be wrong even when the *shape* is right — which is acceptable under our explicit
shape-not-metric mandate, but means this pipeline yields a *topology map*, not a survey. Don't oversell it
as metric.

### What the incoming 2D LiDAR changes

The LiDAR is the single biggest unblocker, because it replaces the inflated, slab-thick free-carve
boundary with a **crisp, metrically-true occupancy grid** ([[2d-lidar-slam]], [[slam-toolbox]],
[[mapping-stack-design]]):

- **Stage 1 becomes metric, not just topological.** The grid boundary is real, so
  **occupancy-grid → vectorized polygon (contour + RDP / rectilinear simplification)** now gives a
  *correct-length* outline, and α-shape/contour overshoot disappears. Family 1 graduates from
  "shape only" to "shape + metric."
- **Stage 2 gets clean input.** Wall lines fit tightly (LiDAR range noise is cm-class, not ±0.6 m), so
  RANSAC/MDL/Progressive-X and the space-partition methods produce trustworthy corners; **ROSE²** (DFT
  clutter removal + Hough walls + Voronoi fallback, [[room-segmentation-floor-plan]]) becomes directly
  applicable for multi-room segmentation.
- **Stage 3 doors get easier.** Crisp walls make the **rectangular-gap-in-the-wall-ring** door detector
  usable, and the occluded-vs-empty test is sharper (LiDAR sees the floor under the gap).
- **What it does *not* fix:** the LiDAR is a single horizontal slice — it sees furniture *legs* and the
  wall slice at sensor height, so **furniture footprints and wall-behind-furniture still come from the
  camera/object layer** (Family 7). The LiDAR gives the wall ring; the camera gives the furniture in it.
  Fusing the two is the world-model job ([[world-model-architecture]]).

**Net:** today, ship the classical edge-fit + model-selection topology pipeline and label it a *shape*
map (honest about metric). When the LiDAR lands, the *same* three-stage structure survives but stage 1
becomes metric and stage 2/3 get trustworthy — so building it now on the carve is not throwaway work.

---

## Sources

All accessed 2026-06-10 via web search/fetch unless noted; figures/PDFs flagged where access was limited.

**Boundary tracing**
- Floor plans from 3D point clouds (concave boundary + α-shape), GRAPP 2019 — hpi.de/doellner; researchgate.net/publication/329523403
- alphashape — pypi.org/project/alphashape
- Static Free Space Detection with OGM, arXiv 1801.00600 — free-space polygon + Douglas-Peucker
- Floor Plan Recognition and Vectorization (UNet + Faster-RCNN + RDP), Springer 2020 — link.springer.com/chapter/10.1007/978-981-15-6648-6_2

**Cell-complex / space-partition**
- Bauchet & Lafarge, *Kinetic Shape Reconstruction*, ACM TOG 2020 — dl.acm.org/doi/10.1145/3376918; Inria hal-02924409
- CGAL *Kinetic Surface Reconstruction* + announcement — doc.cgal.org/latest/Kinetic_surface_reconstruction; cgal.org/2024/05/29
- Fang & Lafarge, *Floorplan generation from 3D point clouds: a space partitioning approach*, ISPRS J. Photogrammetry & RS 2021 — vcc.szu.edu.cn/research/2021/FloorPlan; sciencedirect.com/science/article/abs/pii/S0924271621000538 (full PDF access-denied; details from abstract + VCC page)
- (PolyFit, ICCV 2017 — same family, written up in [[floorplan-reconstruction-methods]])

**Primitive fitting + model selection**
- Yang & Förstner, *Plane Detection in Point Cloud Data* — ipb.uni-bonn.de/pdfs/Yang2010Plane.pdf (RANSAC+MDL)
- MDL principle — modelselection.org/mdl
- (Progressive-X, ICCV 2019 — written up in [[floorplan-reconstruction-methods]])

**Manhattan / Atlanta**
- AtlantaNet (ECCV 2020) — link.springer.com/chapter/10.1007/978-3-030-58598-3_26
- *Globally optimal vertical direction estimation in Atlanta World*, arXiv 1904.12717

**Doors / openings**
- *Door detection in 3D coloured point clouds of indoor environments*, Automation in Construction 2017 — sciencedirect.com/science/article/abs/pii/S0926580516302400 (rectangular data-holes; open vs closed)
- *Windows and Doors Extraction from Point Cloud Data*, MDPI Buildings 2023 — mdpi.com/2075-5309/13/2/507 (semantic + material; visibility occluded-vs-empty)
- (Voronoi critical points + visual door refinement, ICRA 2025; door-status DNN — [[room-segmentation-floor-plan]])

**Learned floor-plan**
- HEAT (CVPR 2022) — heat-structured-reconstruction.github.io; arXiv 2111.15143; github.com/woodfrog/heat
- Floor-SP (ICCV 2019) — arXiv 1908.06702; jcchen.me/floor-sp; github.com/woodfrog/floor-sp (527 real apartments, non-Manhattan)
- (RoomFormer/MonteFloor/CAGE — full writeups in [[floorplan-reconstruction-methods]])

**Semantic structural mapping (furniture in plan)**
- SceneCAD (ECCV 2020) — arXiv 2003.12622; github.com/skanti/SceneCAD (joint CAD-align + layout; corner→edge→quad)
- *Room Envelopes* synthetic dataset, arXiv 2511.03970 (structure behind occluders)
- *Behind the Veil: occluded-surface completion*, arXiv 2404.03070

## Related

[[floorplan-reconstruction-methods]] — per-method mechanics of PolyFit / Progressive-X / MonteFloor / RoomFormer / CAGE + EDA037 improvement levers (read for the algorithms)  
[[room-segmentation-floor-plan]] — 2D-grid room partitioning, Voronoi/visual door detection, ROSE², semantic labelling  
[[passive-stereo-room-mapping-campaign]] — why our walls are ±0.6 m slabs and the carve overshoots 3.7× (the noise this page must survive)  
[[mapping-stack-design]] — where the floor plan sits in the prototype pipeline  
[[2d-lidar-slam]] · [[slam-toolbox]] — the incoming LiDAR grid that turns the shape map metric  
[[apple-roomplan]] — the hardware-rich production ceiling (LiDAR + ANE, ±5 cm) for calibration of expectations  
[[world-model-architecture]] · [[object-fingerprint-memory]] — the furniture/object layer that places furniture *in* the plan and completes walls behind it
