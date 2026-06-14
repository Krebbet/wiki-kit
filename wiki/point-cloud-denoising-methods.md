# Point-Cloud Denoising Methods — Cleaning Generic Artifacts Before the Floor-Plan Fit

How to clean an accumulated 2D/3D point cloud (handheld LiDAR + stereo sweep) of artifacts **by generalizable criteria, not hand-picked coordinates**, so the cleaning transfers to a new room. This page exists because the existing sensor pages explain *why* the cloud is noisy and how to add missing signal, but none gives the **outlier-removal / denoising recipe** that runs after alignment and before the floor-plan + object fit. Three artifact types are in scope from the kitchen sweep: **(1) window-glass scatter**, **(2) operator self-return residual**, **(3) generic sensor noise / outliers**. *(synthesis — assembled from the existing wiki sensor pages + external algorithm sources cited inline; verify parameters on our own data before trusting.)*

Governing project principle (human): **for every point we keep we must be able to explain where it came from; if not, it is noise or it is unexplained — flag it, do not silently keep it.** This page treats denoising as *evidence gating* in that spirit — keep points that agree with redundant evidence (a surface, a cluster, a stable structure across scans), drop or flag the rest. See [[robust-evidence-mapping-principle]].

## Source

Synthesis page; load-bearing facts cited inline to source:
- **Why the cloud is noisy (our own field findings):** [[sensor-weaknesses-and-fixes]] §2 (spurious-far depth on textureless/glass surfaces, ~48% coverage), [[passive-stereo-robustification]] §1 (blank-wall / glass / glossy-floor dropout; spurious *far* depth), [[stereo-dense-reconstruction]] §1 (spurious far depth 12–43 m). The **operator self-return** drop window (~182° behind the rig) is the prototype's existing fixed-bearing mask — this page handles the *residual* after that mask.
- **Open3D classical filters** — `remove_statistical_outlier`, `remove_radius_outlier`, `voxel_down_sample`, `cluster_dbscan` [src-web: open3d.org/docs/release/tutorial/geometry/pointcloud_outlier_removal.html; open3d.org/docs/latest/tutorial/Basic/pointcloud.html].
- **Glass / reflective-noise filtering** — Gao et al., "Reflective Noise Filtering of Large-Scale Point Cloud Using Multi-Position LiDAR Sensing Data," *Remote Sensing* 13(16):3058, 2021 [src-web: mdpi.com/2072-4292/13/16/3058]; IDSOR "Intensity- and Distance-Aware Statistical Outlier Removal" [src-web: arxiv 2602.05876]; DDIOR / weather-robust ROR survey [src-web: encyclopedia.pub/entry/44702; arxiv 2304.06312].
- **Dynamic-point (operator) removal** — ERASOR (Lim et al., ICRA 2021, arXiv 2103.04316); Removert (Kim & Kim, IROS 2020); dynamic-points benchmark arXiv 2307.07260 [src-web].
- **Learned denoising** — Score-Based Point Cloud Denoising / ScoreDenoise (Luo & Hu, ICCV 2021, arXiv 2107.10981); PointCleanNet (Rakotosaona et al. 2020); Total Denoising (Hermosilla et al., ICCV 2019); Noise2Score3D (arXiv 2503.09283) [src-web].

## Related

[[sensor-weaknesses-and-fixes]] · [[passive-stereo-robustification]] · [[stereo-dense-reconstruction]] · [[robust-evidence-mapping-principle]] · [[floorplan-reconstruction-methods]] · [[room-segmentation-floor-plan]] · [[learned-point-cloud-registration]] · [[mapping-stack-design]] · [[speckle-channel-standing-rule]]

---

## 1. The three artifacts, in evidence terms

Cleaning works best when each artifact is named by the *property that betrays it*, not by where it happens to be — that is what makes a criterion generalize to a new room.

| Artifact | Tell-tale property (the generalizable criterion) | Why coordinate-deletion fails |
|---|---|---|
| **1. Window-glass scatter** | A blob of returns that is **off any fitted wall plane**, with **high local radial dispersion** (returns spread in depth where a flat surface should be), often **low/anomalous intensity**, and **inconsistent across viewpoints/scans** (a real surface is stable; glass virtual points move). | The window is at different coordinates in every room; only the *physics* (specular + partial transmission → scattered, plane-violating, view-dependent returns) transfers. |
| **2. Operator self-return residual** | Points that are **close to the sensor**, **move with the rig** (present near the trajectory, absent from the static map built by other passes), i.e. **dynamic / non-repeatable across the sweep**. The bulk is already masked by the fixed ~182° rear bearing window; the residual is the spillover at the mask edges and from arms/shoulders outside it. | The operator is not at a fixed coordinate; they are defined by *being attached to the moving sensor* — a dynamic-point, not a location, criterion. |
| **3. Generic sensor noise / outliers** | **Sparse stray points with few neighbors** (radius/statistical outliers), **mixed/edge pixels** floating between surfaces, isolated specks far from any structure. | Random by nature; no coordinate list exists — must be gated by local density / neighbor statistics. |

---

## 2. Classical methods (the workhorses — all in Open3D/PCL)

These are the first-line tools; they are cheap, deterministic, parameter-tunable, and ship in **Open3D** (`open3d.geometry.PointCloud`) and **PCL** (`pcl::*`).

### 2.1 Statistical Outlier Removal (SOR) — generic noise
Removes points whose mean distance to their *k* nearest neighbors exceeds the cloud-wide mean by more than a number of standard deviations. Best for **sparse stray points and the diffuse halo** of mixed pixels.
- **Open3D:** `pcd.remove_statistical_outlier(nb_neighbors, std_ratio)` — `nb_neighbors` = neighbors used for the per-point average distance; `std_ratio` = how many σ above the global mean before a point is dropped (lower = more aggressive). A benchmarked sweet spot is **`nb_neighbors=30, std_ratio≈1.5–2.0`** [src-web: open3d outlier-removal tutorial].
- **PCL:** `pcl::StatisticalOutlierRemoval` (`setMeanK`, `setStddevMulThresh`).
- **Failure mode:** in **density-varying** clouds (LiDAR near-vs-far, our stereo's 48% patchy coverage) a single global σ over-trims sparse-but-real far structure and under-trims dense noise blobs (e.g. the glass scatter blob is *dense* — SOR keeps it). Tune on, or apply after, density normalization.

### 2.2 Radius Outlier Removal (ROR) — generic noise, density-explicit
Drops any point with fewer than `nb_points` neighbors inside a sphere of `radius`. More directly a *density* gate than SOR.
- **Open3D:** `pcd.remove_radius_outlier(nb_points, radius)`.
- **PCL:** `pcl::RadiusOutlierRemoval`.
- **Failure mode:** a fixed radius is wrong for clouds with strongly varying density — it nukes thin real structure (a far wall edge) while sparing dense artifact blobs. Pick `radius` from the local point spacing; pairs well after a voxel downsample that equalizes density.

### 2.3 Voxel-grid downsampling — normalize density first
Replaces all points in each voxel with their centroid. Not a denoiser per se, but it **equalizes density** (making SOR/ROR thresholds behave consistently across the room) and removes duplicate/over-dense returns from overlapping passes.
- **Open3D:** `pcd.voxel_down_sample(voxel_size)`. **PCL:** `pcl::VoxelGrid`.
- **Failure mode:** too-large a voxel erases the very wall thinness the floor-plan fit needs; centroiding **blends** a thin true surface with adjacent noise. Use a voxel ≪ wall-slab thickness.

### 2.4 DBSCAN cluster-size gating — glass blobs & detached junk
Density-based clustering; label every point, then **keep clusters by size / extent and drop the rest** (small detached clusters = noise; a compact off-wall blob = the glass scatter). This is the most generic structural gate: a real surface joins a large connected cluster; sensor junk forms tiny islands.
- **Open3D:** `labels = pcd.cluster_dbscan(eps, min_points)` — `eps` = neighbor distance defining a cluster, `min_points` = min points to seed a cluster; **label `-1` = noise**. Then count points per label and discard clusters below a size/extent threshold (e.g. <100 pts, or footprint below a floor-area minimum) [src-web: open3d Basic/pointcloud tutorial].
- **PCL:** `pcl::EuclideanClusterExtraction` (`setClusterTolerance`, `setMinClusterSize`).
- **Failure mode:** `eps` too large **merges the glass blob into the adjacent wall** (then size-gating can't separate it); too small **shatters a real sparse wall** into sub-threshold fragments that get deleted. Gate by *physical* size (m² footprint, height extent), not raw point count, so it transfers between rooms of different density.

### 2.5 Plane fit + off-plane / radial-dispersion test — the glass-specific gate
The criterion that actually distinguishes glass scatter from a real wall: **fit wall planes (RANSAC), then flag returns that sit off every plane AND show high local depth (radial) dispersion.** Glass produces returns scattered in range where a planar surface should be flat; reflective-noise work confirms reflective/virtual points are **off-surface and view-inconsistent** and are best caught by combining geometry with **intensity** (glass returns are anomalously low/odd) and **multi-view consistency** (a virtual point is not seen, or appears elsewhere, from a second sweep position) [src-web: Gao et al. 2021 multi-position reflective-noise filtering; IDSOR intensity+distance-aware SOR; DDIOR].
- **Open3D:** `pcd.segment_plane(distance_threshold, ransac_n, num_iterations)` for the wall planes; then a custom residual + local-variance test on the off-plane remainder.
- **Failure mode:** real off-wall objects (a stool, clutter) are *also* off-plane — so this gate must run on the region *near a detected window/wall plane* and lean on dispersion + view-inconsistency, not "off-plane" alone, or it eats furniture. Multi-view consistency is the strongest discriminator if multiple sweep positions exist ([[speckle-channel-standing-rule]] / multi-sweep fusion already give us redundant viewpoints).

### 2.6 Dynamic / moving-point removal — the operator residual
The operator is a **dynamic object attached to the sensor**; the generic class of fixes removes points that are **not consistently observed as static** across the sweep:
- **ERASOR** (ICRA 2021, arXiv 2103.04316): bins space egocentrically and compares **pseudo-occupancy ratios** between a query scan and the map; dynamic bins (transiently occupied) are cleared via region-wise ground-plane fitting. Fast (one-shot, ~10× ray-tracing), cleanest map in the benchmark — but **assumes dynamic objects are ground-contacting**, so it is tuned for vehicles/pedestrians, not a rig-held-at-chest operator [src-web: ERASOR; benchmark arXiv 2307.07260].
- **Removert** (IROS 2020): compares **range images** of a new scan vs the global map; range differences = dynamic. Retains the most static points but leaves residue near object centers [src-web].
- **Visibility / ray-casting removal** (e.g. Raymoval, OctoMap-style free-space carving): a point seen *through* (i.e. free space was observed beyond it on another pass) is dynamic and removed.
- **Failure mode:** all of these need **multiple observations of the same volume from different times/poses** to declare a point transient — they cannot judge a single-pass return. For our residual, the cheaper and more robust first move is a **geometric operator-shell mask** (drop returns within a small radius/height band co-moving with the sensor, extending the existing 182° bearing window into a full near-body exclusion volume), then let multi-sweep occupancy consistency clean the rest. Treat ERASOR/Removert as the principled upgrade once multi-sweep registration is solid ([[learned-point-cloud-registration]]).

---

## 3. Learned point-cloud denoising (know it exists; not first-line for us)

Neural denoisers **displace** noisy points back onto the latent clean surface rather than deleting them:
- **ScoreDenoise / Score-Based Point Cloud Denoising** (Luo & Hu, ICCV 2021, arXiv 2107.10981): models the noisy cloud as a clean distribution convolved with noise and does **gradient ascent on a learned score (log-density gradient)** to move points to the surface. Strong on Gaussian surface noise.
- **PointCleanNet** (2020): a two-stage net — first **classify & remove outliers**, then regress per-point displacement to denoise; iterative.
- **Total Denoising** (ICCV 2019): **unsupervised** (noisy data only) via a spatial prior — relevant because we have no clean ground-truth cloud.
- **Noise2Score3D** (2025): unsupervised Tweedie-formula denoising, estimates the score from noisy data alone.

**Why not first-line here:** they target **surface-noise smoothing** (jitter on a known object), are trained largely on clean CAD/object benchmarks, need a GPU, and tend to **hallucinate a surface** where ours has none (blank wall / spurious-far) — violating the "explain every kept point" principle. They do **not** natively reject *structured* artifacts (a glass blob, the operator) — those are outliers/dynamics, not surface jitter. Park as a possible final polish on per-object clouds (cf. GS2Mesh per-object path in [[stereo-dense-reconstruction]] §5), not for room-cloud artifact removal.

---

## 4. Artifact → method → library → failure-mode map

| Artifact type | Recommended method(s) | Library function | Expected failure mode |
|---|---|---|---|
| **Generic noise / sparse outliers** | Voxel-grid downsample → **SOR**, then **ROR** | `voxel_down_sample`; `remove_statistical_outlier(nb_neighbors=30, std_ratio≈1.5–2.0)`; `remove_radius_outlier(nb_points, radius)` (PCL: `VoxelGrid`, `StatisticalOutlierRemoval`, `RadiusOutlierRemoval`) | Global thresholds over-trim sparse *real* far structure in density-varying clouds; fixed radius wrong across the room — normalize density (voxel) first |
| **Mixed/edge pixels (stereo)** | SOR + **DBSCAN size gate** (edge specks form tiny clusters) | `remove_statistical_outlier`; `cluster_dbscan(eps, min_points)` + per-cluster size filter | DBSCAN `eps` too large merges specks into real surface; too small shatters thin walls |
| **Window-glass scatter** | **RANSAC wall planes** + off-plane & **radial-dispersion** test + **intensity** anomaly + **multi-view consistency**; DBSCAN to isolate the compact blob | `segment_plane(...)` + custom residual/variance test; `cluster_dbscan`; IDSOR/DDIOR-style intensity gate (custom) | Eats real off-wall furniture if it keys on "off-plane" alone; needs dispersion + view-inconsistency. `eps` merge can hide the blob in the wall |
| **Operator self-return residual** | **Co-moving near-body exclusion volume** (extend the 182° mask to a radius+height shell) → **dynamic-point removal** across sweeps (ERASOR / Removert / visibility carving) | custom geometric mask on rig-frame; ERASOR / Removert (research code); OctoMap ray-carving | Dynamic removers need multi-pass observation of the same volume; ERASOR assumes ground-contacting dynamics (operator is chest-height) — mask is the robust single-pass fallback |
| **Surface jitter (per-object polish, later)** | Learned denoisers (optional, Phase-2) | ScoreDenoise / PointCleanNet / Total Denoising (GPU) | Hallucinate surface where signal is genuinely absent; don't reject structured artifacts; GPU + trained-domain dependence |

---

## 5. Recommended FIRST cleaning pipeline (generalizes to a new room)

Ordered, criteria-based (no hand-picked coordinates). Each step states the evidence it gates on, so it transfers to a new room. Run **after** alignment, **before** the floor-plan + object fit.

1. **Operator near-body exclusion (rig-frame, not world-frame).** Extend the existing fixed ~182° rear-bearing mask into a **co-moving exclusion volume**: drop returns within a small radius and chest-height band defined *relative to the sensor pose at each timestamp*. This is the robust single-pass operator fix and generalizes because it is defined on the rig, not on room coordinates. *(criterion: attached-to-moving-sensor)*
2. **Voxel-grid downsample** to a voxel ≪ wall-slab thickness (e.g. a few cm). Equalizes density across overlapping passes so the later neighbor-statistics behave consistently room-to-room, and collapses duplicate returns. *(criterion: redundancy/density normalization)*
3. **Statistical Outlier Removal** (`nb_neighbors=30, std_ratio≈2.0` as a starting point, tune on our cloud) to strip the diffuse halo of sparse stray points and mixed/edge pixels. *(criterion: neighbor-distance agreement)*
4. **Radius Outlier Removal** with `radius` set from the post-voxel point spacing to clear the remaining low-density specks SOR's global σ missed. *(criterion: local density)*
5. **DBSCAN clustering + physical-size gate.** Cluster, then keep clusters above a **physical footprint/height** threshold (m², not raw count) — deletes detached junk islands and isolates the compact glass-scatter blob as its own small/odd cluster. *(criterion: connected structural support)*
6. **Glass-scatter rejection on the off-plane remainder.** RANSAC-fit the wall planes; among points off every plane and *near a wall/window plane*, flag those with **high local radial (depth) dispersion** + **anomalous intensity** + (if multi-sweep available) **view-inconsistency**, and drop them. Lean on multi-sweep redundancy here — it is the strongest, most generalizable glass discriminator. *(criterion: plane-violating + view-inconsistent + intensity-anomalous)*
7. **(Optional, later)** dynamic-point removal (ERASOR/Removert/visibility carving) once multi-sweep registration is solid, to clean any operator/transient residue step 1's mask missed. Learned per-object denoisers reserved for Phase-2 object polish only.

**Honesty / evidence principle:** keep a count (and ideally a kept/dropped overlay) of what each step removes — under the "explain every kept point" rule, a step that silently deletes a large fraction of real structure (or keeps a known artifact) is a finding to surface, not a knob to crank. Validate parameters on our kitchen cloud against the locked GT before trusting them on a new room. *(synthesis.)*
