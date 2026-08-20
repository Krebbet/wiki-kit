# Building a 3D Map from Stereo Images when the Camera Poses are Already Known

**Research question:** Our rig already has a tight camera trajectory (poses good to ~cm, from 2D-LiDAR SLAM — see [[2d-lidar-slam]], [[lidar-visual-fusion-slam]]). Given those poses, how do we turn the per-frame **stereo** image information into a usable 3D map — a navigable room shell + an object/anchor layer — when the walls are largely textureless and the captures are motion-blur-heavy handheld sweeps?

This page is the **known-pose** companion to the existing wiki coverage. It does **not** re-derive SfM/pose estimation (we don't need it), the passive-stereo failure regime ([[passive-stereo-room-mapping-campaign]], [[passive-stereo-robustification]], [[sensor-weaknesses-and-fixes]]), the per-object dense-mesh path ([[stereo-dense-reconstruction]] §5 GS2Mesh), or whether to push fusion into the SLAM front-end ([[lidar-visual-fusion-slam]] — answer: no). It covers the one thing those pages don't: **given good poses, how do you fuse noisy stereo depth into a clean 3D map, and which method to use.**

> **Read alongside:** [[stereo-dense-reconstruction]] (TSDF mechanics + compute + VPP coverage fix), [[passive-stereo-room-mapping-campaign]] (the measured ~20% per-pixel wall-depth noise that bounds all of this), [[mapping-stack-design]] (where this map sits), [[robust-evidence-mapping-principle|robust-evidence principle]] (use the reliable signal, flag the rest unknown), [[point-cloud-denoising-methods]] (the outlier filters referenced in §3).

---

## TL;DR

- **Known poses delete the hard half of the problem.** No SfM, no bundle adjustment, no scale ambiguity, no drift to close. Every method below collapses to: *project per-frame stereo depth into a world frame using the supplied extrinsic, then fuse.* The only remaining question is *how to fuse noisy depth robustly* — a confidence/consistency problem, not a geometry problem. *(synthesis)*
- **For our case, TSDF/point-cloud fusion is the right family** — not MVS, not surfels. We already have depth per frame (SGBM / speckle channel); we just integrate it along the trajectory. ([Open3D RGBD integration](https://www.open3d.org/docs/release/tutorial/pipelines/rgbd_integration.html))
- **The weighted-average TSDF is itself a noise filter** — it does a running weighted average of a truncated SDF plus space carving, which "is great in addressing Gaussian noise and producing smooth surface output" ([Open3D docs](https://www.open3d.org/docs/release/tutorial/pipelines/rgbd_integration.html), after [Curless & Levoy 1996], [Newcombe et al. 2011 / KinectFusion]). But it cannot average away a *systematic* fan or spurious-far reads — those need pre-filtering and confidence weighting first.
- **MVS with known poses is real and easy to run** (COLMAP `patch_match_stereo`/`stereo_fusion`, OpenMVS `DensifyPointCloud`, MVSNet-family take poses as input) — but it re-solves dense matching we already do, and shares the same textureless-wall failure. Use it only as a quality benchmark, not the production path.
- **Crucial honesty for our rig:** stereo depth on blank walls is the *unreliable* signal (campaign result: ±0.6 m slab at 3 m, 27–47% plane inliers vs the 70% needed). So the recommended pipeline **fuses only confident stereo, filters the rest, and keeps the LiDAR as the metric wall/floor anchor** — stereo *adds* object/clutter geometry the LiDAR's single scan plane misses, it does not become the room outline.

---

## 1. Why known poses change everything

The classic stereo-to-3D-map pipeline is *SfM → dense MVS → fusion*. The SfM stage (feature matching, incremental/global bundle adjustment, scale recovery) is the expensive, fragile, drift-prone half — and the half that **passive stereo on blank walls is worst at** ([[lidar-visual-fusion-slam]] §"the camera is the weak geometry source"). When the trajectory is **given**, that entire stage disappears:

- **No correspondence search across frames** — each frame's depth is back-projected directly with its known `T_world_cam`.
- **No scale ambiguity** — poses are metric (cm-grade, from the LiDAR pose graph).
- **No drift / no loop closure** — global consistency is inherited from the pose source.
- **No multi-view *pose* estimation** — at most multi-view *depth-consistency* checks (cheap, local).

What remains is purely a **fusion + filtering** problem: take N metrically-posed, individually-noisy depth maps and combine them into one clean surface. That is exactly the regime TSDF and point-cloud fusion were designed for. *(synthesis)*

This is *not* the same as the [[lidar-visual-fusion-slam]] question (should the camera feed the LiDAR front-end? — no). Here the poses are already final; we are only deciding how to **paint stereo geometry onto a finished trajectory**.

---

## 2. Volumetric TSDF fusion along a known trajectory (the workhorse)

TSDF (Truncated Signed Distance Function) fusion is the KinectFusion lineage ([Newcombe et al., ISMAR 2011], building on [Curless & Levoy, SIGGRAPH 1996]). It is the **default for known-pose depth fusion** and is directly supported in Open3D.

### Mechanics

A voxel grid stores, per voxel, a running weighted average of the signed distance to the nearest surface (truncated to ±`sdf_trunc`) plus an accumulated weight. For each frame you call integrate with the depth image, intrinsics, and the **inverse camera pose** (the world→cam extrinsic):

```python
# Legacy API — Open3D ScalableTSDFVolume
volume = o3d.pipelines.integration.ScalableTSDFVolume(
    voxel_length=4.0/512,          # ~7.8 mm voxels
    sdf_trunc=0.04,                # 4 cm truncation
    color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
volume.integrate(rgbd, intrinsic, np.linalg.inv(T_world_cam))   # extrinsic = world->cam
mesh = volume.extract_triangle_mesh()        # Marching Cubes
pcd  = volume.extract_point_cloud()
```
([Open3D RGBD integration tutorial](https://www.open3d.org/docs/release/tutorial/pipelines/rgbd_integration.html); [`ScalableTSDFVolume` API](https://www.open3d.org/docs/latest/python_api/open3d.integration.ScalableTSDFVolume.html))

The **modern tensor API** is `o3d.t.geometry.VoxelBlockGrid` (CUDA-accelerated, sparse block hashing — scales to large scenes), with the same `integrate(block_coords, depth, intrinsic, extrinsic, depth_scale, depth_max, trunc_voxel_multiplier)` call and a matching `ray_cast(...)` to render depth/color/normal/**weight** back out, with a `weight_threshold` to suppress low-confidence voxels ([VoxelBlockGrid API](https://www.open3d.org/docs/latest/python_api/open3d.t.geometry.VoxelBlockGrid.html); [Ray casting tutorial](https://www.open3d.org/docs/release/tutorial/t_reconstruction_system/ray_casting.html)).

### The parameters that matter (and how noise sets them)

| Param | Meaning | Tuning for our noisy stereo |
|---|---|---|
| `voxel_length` | voxel edge size | Open3D's own caveat: *"Lowering this value makes a high-resolution TSDF volume, but the integration result can be susceptible to depth noise"* ([docs](https://www.open3d.org/docs/release/tutorial/pipelines/rgbd_integration.html)). With ~20% per-pixel noise, go **coarser** (~2–3 cm), not finer — fine voxels just etch the noise in. |
| `sdf_trunc` | truncation band (±) | Set **≥ the depth noise envelope** so multi-frame averaging actually overlaps and cancels. Too tight and noisy reads never average; too wide and thin structure is lost. ~3–5 cm is the usual indoor start. |
| `depth_max` | max integrated depth | **Clamp aggressively** (e.g. 3–4 m). Passive SGBM's spurious-far reads (campaign: ~19 m where a wall stood) are the single most damaging failure for TSDF — carving false free-space *behind* the real wall. Clamping kills most of them. |
| weight / `weight_threshold` | confidence accumulation | The averaging is the noise filter; raise the ray-cast `weight_threshold` so only voxels seen consistently across frames survive — this is the "agreement = reliability" lever. |

### What it buys, and what it cannot fix

- **Buys:** Gaussian per-pixel depth noise is smoothed by the weighted average; "carving" removes free space between camera and surface, cleaning floaters; the output is a watertight mesh or clean point cloud with no extra registration step ([Open3D docs](https://www.open3d.org/docs/release/tutorial/pipelines/rgbd_integration.html)). Integration is cheap (~100 Hz on a GTX-1070-class GPU — [[stereo-dense-reconstruction]] §2); the **bottleneck is the stereo depth step, not fusion**.
- **Cannot fix:** TSDF averages, it does not reject *correlated* error. A wall that lands in a ±0.6 m slab every frame averages to a 0.6 m-thick blur, not a crisp plane ([[passive-stereo-room-mapping-campaign]] §a — this is the documented wall result). And it integrates *whatever depth you give it* — so the leverage is **upstream** (confidence-filter the depth, add speckle texture) not in the fusion params. This is the same conclusion [[stereo-dense-reconstruction]] reaches: *"the upgrades that matter are upstream (better disparity) not downstream (better fusion)."*

---

## 3. Point-cloud fusion + outlier/confidence filtering (the lighter alternative)

If you don't need a watertight mesh — and for a **nav + anchor** map you mostly don't — you can skip the voxel grid and fuse in point-cloud space: back-project every confident depth pixel through `T_world_cam`, accumulate one big cloud, then clean it. This is more transparent (you can see exactly which points survive each filter) and pairs naturally with the robust-evidence principle.

The cleaning ladder (all in Open3D / PCL; see [[point-cloud-denoising-methods]] for the full treatment):

1. **Voxel downsample** — collapse to one point per ~2 cm voxel. Cuts redundancy and gives every later filter a uniform density to reason about.
2. **Statistical Outlier Removal (SOR)** — drop points whose mean neighbour distance is an outlier (kills sparse floaters from spurious matches).
3. **Radius Outlier Removal (ROR)** — drop points with too few neighbours in radius `r` (kills the isolated spray that blank-wall mismatches produce).
4. **Multi-view / free-space consistency** — keep a point only if multiple frames agree it's a surface, and **carve** points that another view sees *through* as free space ([visibility-based fusion, Merrell et al. ICCV 2007](https://people.inf.ethz.ch/pomarc/pubs/MerrellICCV07subm.pdf); [Häne et al. IROS 2011](https://people.inf.ethz.ch/pomarc/pubs/HaeneIROS11.pdf)). With known poses this is direct: render the accumulated cloud into each pose and check occupancy vs free.
5. **Disparity-support confidence** — at the depth source, weight/keep pixels by their cost-curve peak ratio (left-right consistency, uniqueness). Low-support pixels are exactly the textureless-wall guesses; drop them before they ever enter the cloud. "Accumulating evidence from multiple views allows detection and fixing of inconsistencies at occlusions and frustum edges" ([SfM-guided multi-view fusion, arXiv 2503.14483](https://arxiv.org/html/2503.14483v1)).

The throughline is **agreement = reliability**: a point that survives downsample → SOR/ROR → multi-view consistency has been vouched for by redundancy. That *is* the [[robust-evidence-mapping-principle]] applied to stereo.

---

## 4. Depth-map fusion vs surfel maps — which suits known poses

Two ways to hold the fused surface:

- **Volumetric / TSDF (depth-map fusion):** voxels store SDF + weight. Globally consistent by construction once poses are fixed; great Gaussian-noise smoothing; watertight mesh out. Best when poses are **known/already-optimized** — which is us.
- **Surfel maps (ElasticFusion lineage):** each surface element is a disc (position, normal, radius, confidence); no enclosing volume, so thin objects reconstruct well and memory scales with *surface*, not volume ([Wang et al., "Real-time Scalable Dense Surfel Mapping", arXiv 1909.04250](https://arxiv.org/pdf/1909.04250)).

The deciding distinction for us: ElasticFusion is **map-centric** — it deforms the surfel map *as part of* online tracking/loop-closure, which "works well with small-sized region reconstruction" but is built for the *jointly estimating poses while mapping* case. **Pose-graph systems** (where the trajectory is known or separately optimized, then surfels/voxels are deformed to match) "have more advantages in sensor fusion" ([surfel-vs-TSDF discussion, arXiv 1909.04250](https://arxiv.org/pdf/1909.04250); [S3LAM, arXiv 2507.20854](https://arxiv.org/html/2507.20854v1)). Since our poses come **separately** from the LiDAR pose graph and are final, we are squarely in the pose-graph regime → **TSDF (or plain point-cloud fusion) fits; the map-centric surfel deformation machinery is solving a problem we don't have.** *(synthesis)*

---

## 5. MVS with known poses — usable, but not our production path

Multi-View Stereo *can* consume known poses directly (it normally gets them from COLMAP SfM; you can substitute your own). Three families:

- **PatchMatch MVS (COLMAP / OpenMVS).** The standard dense pipeline: `colmap image_undistorter` → `patch_match_stereo` (per-view depth maps by PatchMatch, with photometric + geometric consistency across views) → `stereo_fusion` into a dense cloud; or hand the sparse model + images to OpenMVS `DensifyPointCloud` ([COLMAP tutorial](https://colmap.github.io/tutorial.html); [OpenMVS Usage wiki](https://github.com/cdcseacave/openMVS/wiki/Usage)). To use **our** poses, write them as the COLMAP `images.txt`/`cameras.txt` sparse model (skip `mapper`) and run dense from there.
- **Plane-sweep / classical MVS.** Sweep a family of fronto-parallel depth planes, score photo-consistency per pixel, pick the best — the textbook known-pose dense matcher and the conceptual core of the learned methods below.
- **Learned MVSNet-family.** [MVSNet (ECCV 2018)](https://openaccess.thecvf.com/content_ECCV_2018/papers/Yao_Yao_MVSNet_Depth_Inference_ECCV_2018_paper.pdf) takes N posed images, builds a cost volume by **differentiable homography warping into the reference frustum** (plane-sweep, but learned features), regularizes with 3D convs, regresses a depth map — *poses are an input, not an output*. Successors target our exact weakness: textureless/occluded regions via monocular cues, perspective-aware features, region-aware cost volumes ([Region-aware MVSNet CVPR 2023](https://openaccess.thecvf.com/content/CVPR2023/papers/Zhang_Multi-View_Stereo_Representation_Revist_Region-Aware_MVSNet_CVPR_2023_paper.pdf); [MC-MVSNet](https://www.sciencedirect.com/science/article/abs/pii/S0031320326001317)).

**Why not as the production path:** MVS re-solves dense correspondence we already get from SGBM/the speckle channel, costs much more compute, and **shares the identical textureless-wall failure** — learned MVS helps at the margins but doesn't manufacture geometry the input never contained ([[passive-stereo-room-mapping-campaign]] §d2 makes the same point about learned floor-plan methods). Run COLMAP/OpenMVS MVS **once as an upper-bound benchmark** on a captured sequence (cf. the EDA046 RoomFormer-benchmark logic) to know what the best dense stereo can do on our data; then build production on the cheaper TSDF/point-cloud fuse.

---

## 6. Handling textureless surfaces (the load-bearing problem for us)

This is where the known-pose simplification stops helping — poles don't add texture. The fixes, in the order to reach for them:

1. **Use the speckle channel, not grayscale.** When the red-speckle IR projector is on, recover depth from the [derived speckle channel](memory) (EDA036, `src/depth/speckle_channel.py`) — it is the project's standing rule for wall/depth work and the ideal input here. Active speckle is the *direct* cure for the blank-wall starvation ([[passive-stereo-robustification]] §4: "spray artificial texture so passive matching gets features").
2. **Virtual Pattern Projection (VPP), no hardware.** Inject sparse confident depth seeds and hallucinate IR-like texture into both images before matching; off-the-shelf RAFT-Stereo error >1px drops 19.2%→6.7% with 5% seeds, no retraining ([[stereo-dense-reconstruction]] §3). The seeds can come from the LiDAR scan plane projected into the image — a natural fit given known poses + known LiDAR↔camera extrinsics.
3. **Confidence-weight, then fuse.** Carry per-pixel disparity confidence into the TSDF weight / the point-cloud keep-mask (§§2–3) so blank-wall guesses are down-weighted, not averaged in at full strength.
4. **Plane priors / RANSAC.** The floor reconstructs rock-solid (RANSAC plane RMS ~1.7 cm, drift-immune — [[passive-stereo-room-mapping-campaign]] §a); fit it explicitly and snap near-floor points to it. Wall *planes* can be RANSAC-fit **where stereo gives ≥~70% single-plane inliers** (the campaign "flip condition") and **left UNKNOWN otherwise** rather than rendered as a 0.6 m blur. Edge-aware / bilateral depth filtering before fusion preserves real depth edges while smoothing within surfaces.
5. **Fall back to LiDAR geometry for the shell.** When stereo can't clear the flip condition on a wall (the common case for us), the wall comes from the **LiDAR**, not from stereo — keep stereo for the object/clutter layer the LiDAR's single ~1.1 m scan plane can't see ([rig LiDAR-stereo offset](memory): scan plane ~7 cm above the camera). This is the robust-evidence split made concrete.

---

## 7. Practical libraries & rough recipes

| Tool | Known-pose recipe | Output | When |
|---|---|---|---|
| **Open3D RGBD integration** (`ScalableTSDFVolume` / `VoxelBlockGrid`) | per-frame: `integrate(rgbd, K, inv(T_world_cam))`; then `extract_triangle_mesh` / `extract_point_cloud`, or `ray_cast` with `weight_threshold` | TSDF mesh / cloud | **Production fuse for us.** Cheapest, depth-source-agnostic, the noise-averaging is built in. ([docs](https://www.open3d.org/docs/release/tutorial/pipelines/rgbd_integration.html)) |
| **Open3D point-cloud filters** | accumulate back-projected cloud → `voxel_down_sample` → `remove_statistical_outlier` → `remove_radius_outlier` | clean cloud | When you want a transparent, inspectable fuse (object/anchor layer). See [[point-cloud-denoising-methods]]. |
| **COLMAP MVS** | write our poses as the sparse model → `image_undistorter` → `patch_match_stereo` → `stereo_fusion` | dense cloud | One-shot **upper-bound benchmark** on our data. ([tutorial](https://colmap.github.io/tutorial.html)) |
| **OpenMVS** `DensifyPointCloud` | feed sparse model + undistorted images | dense cloud / mesh | Same role as COLMAP MVS; richer mesh/texture tooling. ([wiki](https://github.com/cdcseacave/openMVS/wiki/Usage)) |
| **RTAB-Map** (dense RGB-D mode) | feed stereo depth + our poses (localization/external-odom mode) | OctoMap / dense cloud / mesh | If we want the turnkey map→save→relocalize loop; see [[passive-stereo-robustification]] §7. |
| **MVSNet-family** | N posed images → cost volume → depth maps → TSDF fuse | depth maps → mesh | Research lever for textureless regions; not yet a production dependency. |

All of the above run on a 4 GB consumer GPU (TSDF on CPU even); the compute table is in [[stereo-dense-reconstruction]] §8.

---

## 8. Recommended for this project

**Robust-evidence fusion: trust confident stereo, filter the rest, keep the LiDAR as the metric anchor.** Concretely, the minimal known-pose pipeline for our noisy-textureless-stereo + good-poses + want-a-clean-nav+anchor-map case:

1. **Depth source = speckle channel when projector is on, else SGBM**, each pixel carrying a confidence (disparity support / left-right consistency). Clamp `depth_max` to ~3–4 m to kill spurious-far reads. *(directly attacks the #1 TSDF-corrupting failure)*
2. **Confidence-filter per frame** — drop low-support pixels (the blank-wall guesses) *before* fusion.
3. **Fuse along the known trajectory** with Open3D — TSDF (`VoxelBlockGrid`, ~2–3 cm voxels, ~4 cm trunc, raise `weight_threshold`) for a mesh, or accumulate + `voxel_down_sample` → SOR → ROR for an inspectable cloud. The weighted average + carving cleans the Gaussian noise; multi-view consistency carves the floaters.
4. **Layer it correctly — don't let stereo be the room outline.** Floor + gravity from the rock-solid RANSAC plane; **walls from the LiDAR** (stereo walls only where they clear the ~70% single-plane flip condition, UNKNOWN otherwise); **stereo's job is the object/clutter geometry above and below the single LiDAR scan plane** — the layer the LiDAR physically can't see. This is the nav-shell-from-LiDAR + anchor-layer-from-stereo division the campaign and [[lidar-visual-fusion-slam]] already endorse.
5. **Keep LiDAR as the metric truth.** Cross-validate the fused stereo geometry against the LiDAR scan/pose graph; where they disagree on a wall, the LiDAR wins. Stereo *enriches* the map; it does not define the shell.

The single highest-leverage upstream move remains **adding texture** (speckle channel / VPP seeds from the projected LiDAR points) — that lifts the confident-stereo fraction, which is the only thing that makes any of the downstream fusion produce more wall and less UNKNOWN. *(synthesis, grounded in the campaign findings and the robust-evidence principle)*

---

## Sources

- [Open3D — RGBD integration tutorial](https://www.open3d.org/docs/release/tutorial/pipelines/rgbd_integration.html) — `ScalableTSDFVolume`, `voxel_length`/`sdf_trunc`, integrate-with-pose, weighted-average + carving; cites [Curless & Levoy 1996] and [Newcombe et al. 2011 / KinectFusion].
- [Open3D — `ScalableTSDFVolume` API](https://www.open3d.org/docs/latest/python_api/open3d.integration.ScalableTSDFVolume.html)
- [Open3D — `VoxelBlockGrid` API](https://www.open3d.org/docs/latest/python_api/open3d.t.geometry.VoxelBlockGrid.html) and [Ray casting in a Voxel Block Grid](https://www.open3d.org/docs/release/tutorial/t_reconstruction_system/ray_casting.html) — modern tensor TSDF, `weight_threshold`.
- [Merrell et al., *Real-Time Visibility-Based Fusion of Depth Maps*, ICCV 2007](https://people.inf.ethz.ch/pomarc/pubs/MerrellICCV07subm.pdf) — multi-view consistency + free-space carving from depth maps.
- [Häne et al., *Stereo Depth Map Fusion for Robot Navigation*, IROS 2011](https://people.inf.ethz.ch/pomarc/pubs/HaeneIROS11.pdf) — stereo depth fusion for a nav map.
- [SfM-guided Monocular Depth for MVS, arXiv 2503.14483](https://arxiv.org/html/2503.14483v1) — multi-view consistency / evidence accumulation for fusion.
- [Wang, Gao & Shen, *Real-time Scalable Dense Surfel Mapping*, arXiv 1909.04250](https://arxiv.org/pdf/1909.04250) — surfel vs TSDF; map-centric vs pose-graph trade-off.
- [S3LAM: Surfel Splatting SLAM, arXiv 2507.20854](https://arxiv.org/html/2507.20854v1) — surfel mapping context.
- [COLMAP tutorial](https://colmap.github.io/tutorial.html) — `image_undistorter` / `patch_match_stereo` / `stereo_fusion` dense MVS.
- [OpenMVS Usage wiki](https://github.com/cdcseacave/openMVS/wiki/Usage) — `DensifyPointCloud` PatchMatch / SGM dense.
- [Yao et al., *MVSNet*, ECCV 2018](https://openaccess.thecvf.com/content_ECCV_2018/papers/Yao_Yao_MVSNet_Depth_Inference_ECCV_2018_paper.pdf) — learned MVS, poses as input, differentiable plane-sweep cost volume.
- [Zhang et al., *Region-Aware MVSNet*, CVPR 2023](https://openaccess.thecvf.com/content/CVPR2023/papers/Zhang_Multi-View_Stereo_Representation_Revist_Region-Aware_MVSNet_CVPR_2023_paper.pdf) and [MC-MVSNet](https://www.sciencedirect.com/science/article/abs/pii/S0031320326001317) — textureless-region MVS improvements.
- Project-internal (carried via wiki): [[passive-stereo-room-mapping-campaign]] (±0.6 m wall slab, 70% flip condition, 1.7 cm floor), [[stereo-dense-reconstruction]] (TSDF compute, VPP), [[lidar-visual-fusion-slam]] (LiDAR-first geometry), [[robust-evidence-mapping-principle]].

---

## Related

[[stereo-dense-reconstruction]] · [[passive-stereo-room-mapping-campaign]] · [[passive-stereo-robustification]] · [[lidar-visual-fusion-slam]] · [[mapping-stack-design]] · [[point-cloud-denoising-methods]] · [[robust-evidence-mapping-principle]] · [[sensor-weaknesses-and-fixes]] · [[2d-lidar-slam]] · [[world-model-architecture]] · [[floorplan-reconstruction-methods]] · [[anchor-map-protocol]]
