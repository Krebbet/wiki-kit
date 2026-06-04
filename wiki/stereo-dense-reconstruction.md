# Dense 3D Reconstruction from Passive Stereo — Methods, Gaps, and Paths Forward

**Research question:** Can the prototype's passive stereo camera (57.8 mm baseline SVPRO, ~48% SGBM depth coverage) produce dense 3D geometry — TSDF volumes, meshes, or dense point clouds — suitable for home-tidy tasks? If not, what are the upgrade paths?

This page covers: (1) the quality gap between passive stereo and RGB-D for dense reconstruction; (2) TSDF/mesh pipeline mechanics and compute requirements; (3) per-object dense reconstruction on demand; (4) Virtual Pattern Projection (VPP) as the main depth-coverage fix; (5) depth completion as a learned alternative; (6) the GS2Mesh path for object reconstruction without depth sensors.

> **Read alongside:** [[mapping-stack-design]] (why dense volumetric is the wrong form factor for the prototype's current regime), [[world-model-architecture]] (the layered world model that avoids dense maps), [[passive-stereo-robustification]] (the consumer-cost robustifier ladder).

---

## TL;DR

- **TSDF/mesh from passive stereo works**, but ~50% SGBM coverage causes hollow walls, missing ceilings, and blank-room interiors. The result is not usable as a floor plan or room model without supplementation. *(synthesis, grounded in EDA010 findings in [[mapping-stack-design]])*
- **The quality gap vs RGB-D is large for featureless surfaces** — where an active stereo sensor fills blank walls (via IR speckle), passive SGBM returns NaN. TSDF simply skips invalid pixels; walls don't appear.
- **TSDF integration itself is cheap** — Open3D TSDF runs ~100 Hz on a GTX 1070 (~4 GB GPU). The bottleneck is the stereo disparity step, not the volumetric fusion.
- **VPP (Virtual Pattern Projection)** is the most promising depth-coverage fix: inject 1–5% sparse depth seeds into a pre-processing step that hallucinates IR-pattern-like texture onto blank image regions. Error rate on Middlebury-21: RAFT-Stereo 19.22% → 6.65% (>1px, no retraining) with 5% seeds. *(source: 01, 02)*
- **Per-object dense reconstruction on demand** — 5–20 views, ~10 minutes — is feasible with the GS2Mesh pipeline (3DGS → rendered stereo pairs → TSDF mesh). No depth sensor required; blank-wall problem disappears because 3DGS inpaints color. Achieves 0.70 Chamfer Distance on DTU in ~12 min on a single GPU. *(source: 07)*
- **Jetson Orin 16 GB can run most of these pipelines.** RAFT-Stereo and IGEV-Stereo inference run on any CUDA device with ≥4 GB VRAM. Open3D TSDF has a CUDA path. The ceiling is MASt3R/InstantSplat (needs ~6 GB VRAM).
- **An active speckle projector materially closes the gap** — but VPP + sparse seeds from existing geometry achieves a similar effect without hardware. Structured-light is bounded to ~3–5 m indoors and fails outdoors.

---

## 1. The quality gap: passive stereo TSDF vs RGB-D TSDF

### What RGB-D gives a TSDF pipeline

An active stereo RGB-D sensor (RealSense D435i, OAK-D SR) projects a fixed IR speckle pattern onto the scene. This artificially textures blank walls, glass, and low-contrast floors, giving the stereo matching algorithm correspondence anchors everywhere. Measured depth coverage: ~95%+ for most indoor surfaces.

The Open3D TSDF pipeline takes each depth frame + pose + intrinsics and integrates via weighted average into a voxel block grid. Where depth is valid and consistent across multiple frames, surface confidence grows; holes fill in. The result is a smooth, gap-free room mesh *(source: 06)*.

### What passive stereo gives (our prototype)

The SVPRO SGBM pipeline produces ~48% valid depth pixels per frame (measured, EDA010 in [[mapping-stack-design]]). The invalids cluster on blank walls, ceilings, bright windows, specular floors, and any surface without texture contrast. These are exactly the room boundaries that matter for navigation and floor planning.

When this is fed to Open3D TSDF:
- **Occupied near-field cells are correct** — furniture and textured surfaces reconstruct well.
- **Far walls are absent or show spurious far depth** — blank walls show no TSDF integration, or worse, erroneous integration at 12–43 m (spurious far depth from SGBM). EDA010 found that 74% of occupied cells clustered within 1.5 m of the camera path, with no clean wall lines at room boundary.
- **The floor plan is unusable** without active stereo or a 2D LiDAR (see [[mapping-stack-design]] §Next step 1).

*(synthesis, grounded in EDA010 results and [[passive-stereo-robustification]] §1)*

**Quantified gap (editorial summary from sources):** For textured objects (books, furniture, clutter), passive stereo TSDF is competitive with RGB-D. For featureless planar surfaces (painted walls, white ceilings), the gap is total — passive stereo produces nothing; RGB-D produces a clean surface.

---

## 2. TSDF/mesh pipeline mechanics and compute

### Open3D TSDF API

Open3D's Voxel Block Grid (`o3d.t.reconstruction`) is the standard reference implementation *(source: 06)*:

```python
vbg.integrate(frustum_block_coords, depth, depth_intrinsic, extrinsic, depth_scale, depth_max)
```

It accepts any float32 or uint16 depth image — stereo-derived depth (from SGBM, RAFT-Stereo, IGEV) feeds in directly with no adapter. The TSDF itself does not care whether depth came from an RGB-D sensor or a stereo matcher.

**Performance (from Open3D docs):**
- Optimized path: **~100 Hz on GTX 1070** (~4 GB VRAM class). [src: 06-open3d-tsdf-integration.md]
- Prototype implementation: **~25 Hz** on same hardware.
- CUDA and CPU paths both available.

**The bottleneck is not TSDF — it is stereo depth.** SGBM (CPU, OpenCV): ~5–30 fps depending on resolution and window size. RAFT-Stereo/IGEV-Stereo (GPU): ~10–30 fps on a 4 GB GPU at 640×480. The fusion pipeline is fast enough at ~100 Hz; the depth source sets the real framerate.

### Compute by platform (editorial)

| Platform | TSDF (Open3D) | RAFT-Stereo inference | IGEV-Stereo inference | Notes |
|---|---|---|---|---|
| Desktop RTX 3090 (24 GB) | ~100 Hz (CUDA) | ~15–30 fps | ~15–25 fps | Training platform for VPP (single 3090, batch 2) [src: 02] |
| Desktop GTX 1070 (8 GB) | ~100 Hz (CUDA) | ~8–15 fps | ~8–12 fps | [src: 06] — documented speed |
| Consumer 4 GB GPU (1060/2060) | ~25–80 Hz (CUDA) | ~5–10 fps | ~5–8 fps | RAFT-Stereo memory-efficient; 4 GB is the practical floor |
| Jetson Orin (16 GB unified) | CUDA path available | fp16 inference viable | fp16 viable | No benchmarks in captured sources; likely ~3–8 fps at 640×480 |
| Jetson Orin (4 GB module) | CUDA limited | Constrained | Constrained | Not the 16 GB module; DPV-SLAM was borderline at 8 GB [src: passive-stereo-robustification] |

*(table is editorial synthesis — no captured source provides Jetson Orin TSDF benchmarks directly)*

### ElasticFusion / BundleFusion / KinectFusion — stereo adaptation

KinectFusion (Microsoft Research, 2011) is the ancestor of all real-time TSDF pipelines. It was built for RGB-D (Kinect v1 depth sensor) and assumes depth coverage ~95%. Stereo-adapted variants exist:
- **StereoFusion** (prior literature): swap the Kinect depth with stereo depth, run unchanged. Works on textured scenes; fails on blank walls for the same reasons as above.
- **BundleFusion** (Stanford, 2017): adds global loop closure and online re-integration. Designed for RGB-D; adapting to stereo inputs is straightforward but the coverage gap persists. No captured primary source in this research; referenced in search results as "best RGB-D reconstruction" but quality comparison to stereo is not quantified in captured sources.

**The fundamental constraint is not the fusion algorithm — it is input depth coverage.** Any TSDF system fed ~50% coverage produces reconstructions with the same blank-wall holes. The upgrades that matter are upstream (better disparity) not downstream (better fusion). *(synthesis)*

---

## 3. VPP — Virtual Pattern Projection (the main fix for coverage)

### What it is

Virtual Pattern Projection (VPP) is a preprocessing step for any stereo pipeline *(sources: 01, 02 — University of Bologna)*. Given:
- A calibrated stereo image pair (IL, IR)
- A sparse set of depth seeds — even 1% pixel density

VPP converts each seed's depth to a disparity value, then coherently paints a small pixel pattern at the corresponding epipolar positions in BOTH images. The stereo matcher then sees the pair as if a physical IR projector had been applied: blank walls now have artificial texture anchors.

**The stereo matcher is unchanged** — VPP acts on the images before any processing. Any matcher (SGBM, RAFT-Stereo, IGEV, PSMNet) benefits without retraining.

### Benchmark results

From Bartolomei et al. ICCV 2023 (Midd-14, 5% depth seeds, off-the-shelf networks — no retraining):

| Method | Error >3px (baseline) | Error >3px (VPP) | Guided stereo |
|---|---|---|---|
| RAFT-Stereo | 12.48% | **4.35%** | 7.85% |
| PSMNet | 24.29% | **13.06%** | 24.03% |
| rSGM | 29.41% | **10.86%** | 17.03% |

[src: 02-active-stereo-no-projector-iccv2023.md, Table 3]

From journal extension (Midd-21, no retraining):

| Method | Error >1px (baseline) | Error >1px (VPP) | Guided stereo |
|---|---|---|---|
| RAFT-Stereo | 19.22% | **6.65%** | 18.82% |
| PSMNet | 44.75% | **21.38%** | 44.40% |

[src: 01-vpp-stereo-depth-fusion-2024.md, Table reproduced from paper]

VPP outperforms guided stereo (which concatenates depth seeds as input to the network) in virtually all off-the-shelf settings. The key: VPP acts at the image level, not the network architecture level.

### Seed source for our prototype

The sparse seeds do not need to come from an external sensor. Options:
1. **SGBM's own confident pixels** (~48% in our case) — bootstrap. Feed these as seeds, re-run SGBM or RAFT-Stereo with VPP augmentation on the same frame. This is a self-bootstrapping loop.
2. **Prior frame depth** — use confident pixels from adjacent frames, transformed by odometry, as seeds for the current frame.
3. **Separate cheap depth sensor** — a cheap IR dot projector paired with a small ToF at ~1% coverage is sufficient per the paper.

*(editorial — not directly stated in sources; the bootstrapping approach is plausible but not evaluated in the VPP paper)*

### GPU cost

VPP preprocessing is CPU-side image arithmetic (weighted splatting). Zero GPU cost added to the chosen stereo matcher. The GPU cost is whatever RAFT-Stereo/IGEV already costs (~4–8 GB VRAM, ~5–15 fps). [src: 01, 02]

---

## 4. Depth completion as an alternative

Depth completion takes a sparse depth map + RGB image and infers a dense depth map. This is complementary to VPP:
- VPP: augment images → run stereo → more coverage.
- Depth completion: take sparse stereo output → learn dense prediction.

The Guo et al. (2023) approach *(source: 08)* uses monitored distillation with a stereo teacher: AS2D module extracts global features from sparse depth, with self-supervised multi-view consistency. Outperforms SOTA on KITTI.

**Key limitation:** Evaluated on KITTI (outdoor, structured). Indoor blank-wall completion is harder — there is no texture in the region of interest for the network to anchor on. Domain adaptation to indoor home environments would be required. The paper does not address this. [src: 08-sparse-depth-guided-depth-completion.md]

**When to use depth completion vs VPP:**
- VPP: better for improving the stereo matching process itself. Works regardless of scene type. No training required.
- Depth completion: better when you want to post-process an existing sparse depth map without re-running stereo. Requires domain-appropriate training.

*(editorial)*

---

## 5. Per-object dense reconstruction on demand

### The use case

The home-tidy robot encounters an unknown object and needs its 3D shape for grasping or placement. It can orbit the object 5–20 times from different angles (drone or ground rover). Can it build a usable mesh?

### GS2Mesh pipeline (recommended path)

GS2Mesh *(source: 07 — Technion)* is the clearest path to per-object mesh without a depth sensor:

1. **Capture** ~10–20 photos of the object (any camera, any angles). COLMAP for SfM poses — or InstantSplat (below) for pose-free capture.
2. **3DGS optimization** (~7k iterations sufficient for small objects → ~7 min).
3. **Render synthetic stereo pairs** from the 3DGS model (left at training pose, right displaced by b = 7% scene radius).
4. **DLNR stereo matching** on rendered pairs → depth profiles. Blank-wall problem disappears — 3DGS inpaints photorealistic color even on textureless surfaces, giving the stereo matcher something to match.
5. **TSDF fusion** (Open3D) + Marching Cubes → triangle mesh.

**Results (DTU benchmark, Chamfer Distance):**
- GS2Mesh: **0.70 mean** (30k 3DGS iterations), or nearly identical with 7k iterations in ~12 min total.
- Competitive with Neuralangelo (0.61) which takes >12 hours.
- Better than SuGaR (1.47), 2DGS (0.80). [src: 07-gs2mesh-surface-from-gaussians.md]
- Also evaluated on in-the-wild smartphone videos.

**Compute:** 3DGS ~6–8 GB VRAM; DLNR stereo ~4 GB VRAM; Open3D TSDF CPU or CUDA. All runnable on a 4 GB consumer GPU at slightly reduced speed (reduce resolution/iterations). [src: 06, 07]

### InstantSplat for pose-free sparse-view capture

If the robot cannot run COLMAP (no dense baseline), InstantSplat *(source: 04 — UT Austin / Nvidia Research)* reconstructs from **2–3 unposed images** in ~7.5 seconds using MASt3R dense stereo priors + Gaussian Bundle Adjustment.

- SSIM: 0.3755 → **0.7624** vs COLMAP+3DGS at 3-view on Tanks and Temples. [src: 04-instantsplat-2024.md]
- 20x speedup over COLMAP+3DGS.
- Compatible with 3D-GS, 2D-GS, Mip-Splatting.
- Hardware: tested on A100; MASt3R requires ~6 GB VRAM at resolution 512.

**Combined path: InstantSplat (fast 3DGS from 5–20 unposed frames) → GS2Mesh (stereo+TSDF mesh) = per-object mesh in ~15 min, no depth sensor required.** *(editorial synthesis of sources 04 + 07)*

---

## 6. ASGrasp and active stereo for transparent/specular objects

For transparent and specular objects (glass bottles, chrome hardware), passive stereo fails completely — the surface provides no matching cues. ASGrasp *(source: 03 — Samsung R&D / Peking University, ICRA 2024)* solves this differently:

**Key insight:** The RealSense D400 family exposes raw IR left+right images BEFORE its built-in stereo matching step. These carry the original IR signal even for transparent/specular objects. A learned RAFT-style network operating on RGB + left IR + right IR directly produces accurate depth + occluded second-layer depth.

**Results:** >90% transparent-object grasping success in simulation and real world; on-par with perfect-depth upper bound for first-layer; surpasses perfect-depth when second-layer (occluded) geometry is used. [src: 03-asgrasp-icra2024.md]

**Hardware constraint:** Requires an active stereo camera that exposes raw IR streams (D415, D435, D435i). Our SVPRO is passive — no IR channel. This is a hardware upgrade path, not a software fix.

**What this means for our prototype:**
- For most home objects (books, cups, toys): passive stereo + VPP is sufficient.
- For transparent objects (glass, clear containers): need active stereo (D435i) + ASGrasp-style learned matcher.
- The D435i ($334) provides active stereo + exposed IR pairs + calibrated IMU — the single upgrade that unlocks both VPP and ASGrasp. *(cross-reference: [[passive-stereo-robustification]] §hardware ladder)*

---

## 7. Active speckle projector — does it close the gap?

An external IR dot projector (DOE + IR LED, ~$12–$80) sprays random speckle onto the scene, providing texture for passive stereo to match against. This is exactly how RealSense D400 series works internally.

**What VPP shows us about speckle projectors:** VPP achieves the same effect — injecting matching texture — without hardware, using 1% sparse seeds. The comparison:

| Approach | Hardware cost | Works outdoor/sunlight? | Range | Calibration needed? |
|---|---|---|---|---|
| Physical speckle projector (IR DOE) | $12–$80 | No (washed out) | ~3–5 m | Co-mounted + calibrated to camera |
| VPP + sparse seeds | $0 (SW) | Yes | Any | Calibrated stereo rig only |
| RealSense D435i (integrated) | $334 | No | ~0.3–6 m | Factory calibrated |

[src: 01, 02, passive-stereo-robustification §4]

**Quantified gap closure (from VPP paper, Midd-21, RAFT-Stereo-vpp):**
Error >1px: 19.22% (no augmentation) → 6.65% (VPP, 5% seeds). A physical projector achieving similar coverage would give similar error rates — the papers on active stereo (RealSense class) report ~95% depth coverage vs ~50% passive, consistent with the ~3x error reduction seen in VPP. [src: 01, 02]

**Honest answer:** A physical speckle projector does materially close the gap — perhaps 40–50% error reduction on blank-wall-heavy indoor scenes. VPP achieves comparable improvement without the hardware, contingent on having any seed depth source. For the prototype, VPP + SGBM bootstrapping is the right first experiment before buying hardware. *(editorial)*

---

## 8. What runs on a 4 GB consumer GPU

| Component | 4 GB GPU compatible? | Notes |
|---|---|---|
| Open3D TSDF integration | Yes | ~100 Hz GTX 1070 [src: 06] |
| SGBM (OpenCV) | Yes (CPU) | No GPU needed |
| RAFT-Stereo (inference) | Yes | Memory-efficient implementation; ~5–8 fps at 640×480 |
| IGEV-Stereo (inference) | Yes | 35% less memory than RAFT-Stereo per search results |
| VPP preprocessing | Yes (CPU) | Image arithmetic only |
| 3DGS optimization (7k iters) | Borderline | Standard 3DGS uses ~6–8 GB; reduce resolution/steps |
| DLNR stereo on rendered pairs | Yes | ~4 GB [src: 07] |
| MASt3R/InstantSplat | No (6 GB) | Requires MASt3R at res 512 [src: 04] |
| ASGrasp (RAFT-style) | Yes | Same memory class as RAFT-Stereo [src: 03] |
| Depth completion (AS2D) | Yes | Lightweight inference [src: 08] |

*(editorial synthesis — no single captured source provides a complete 4 GB GPU compatibility table)*

---

## 9. Comparison to existing wiki coverage

The existing wiki ([[world-model-architecture]], [[mapping-stack-design]]) already notes "dense volumetric (TSDF / per-point CLIP) is the wrong form factor for us" for the full-room scenario. This page does NOT contradict that conclusion — it documents WHY (coverage gap) and WHEN dense reconstruction IS appropriate (per-object, on-demand, GS2Mesh path).

Specific additions this page makes:
- VPP quantified benchmark numbers (first appearance in wiki).
- GS2Mesh as the per-object reconstruction path (not previously covered).
- InstantSplat as the pose-free sparse-view path (not previously covered).
- ASGrasp as the transparent-object active stereo path (not previously covered).
- Explicit compute table by GPU class.
- The "VPP bootstrapping with own SGBM seeds" option *(editorial — not in sources)*.

---

## Source

| File | Paper / URL | Role |
|---|---|---|
| `01-vpp-stereo-depth-fusion-2024.md` | Bartolomei et al. IJCV 2024, arXiv 2406.04345 | VPP journal paper — benchmark numbers |
| `02-active-stereo-no-projector-iccv2023.md` | Bartolomei et al. ICCV 2023, arXiv 2309.12315 | VPP conference paper — original results |
| `03-asgrasp-icra2024.md` | Shi et al. ICRA 2024, arXiv 2405.05648 | Active stereo + transparent object grasp |
| `04-instantsplat-2024.md` | Fan et al. 2024, arXiv 2403.20309 | Sparse-view pose-free 3DGS |
| `05-vppstereo-project-page.md` | vppstereo.github.io | VPP project page (thin) |
| `06-open3d-tsdf-integration.md` | Open3D docs | TSDF pipeline API + performance |
| `07-gs2mesh-surface-from-gaussians.md` | Wolf et al. 2024, arXiv 2404.01810 | 3DGS → stereo → TSDF mesh |
| `08-sparse-depth-guided-depth-completion.md` | Guo et al. 2023, arXiv 2303.15840 | Depth completion from sparse stereo |

Raw sources: `raw/research/stereo-dense-reconstruction/`

---

## Related

[[passive-stereo-robustification]] · [[mapping-stack-design]] · [[world-model-architecture]] · [[close-range-depth-sensors]] · [[learned-slam]] · [[indoor-cluttered-slam]] · [[onboard-grasp-perception]] · [[sensor-weaknesses-and-fixes]] · [[imu-vio-integration-reality]] · [[methods-reading-list]]
