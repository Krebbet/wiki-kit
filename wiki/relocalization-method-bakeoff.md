# Relocalization Method Bake-Off (Passive-Stereo, Marker-Free, Indoor)

A focused SOTA survey + **decision** for the `drone-prototype` make-or-break problem: build an
indoor room map from a **passive USB stereo** camera, save it, then in a **fresh pass recover
absolute pose** (marker-free relocalization). The current method (**RTAB-Map stereo**) *works*
but at low robustness — and the prototype has now **isolated exactly which gate fails**, which
changes what an alternative must beat. This page surveys the 2023–2026 candidates, **selects the
2 best to actually run against our recorded data**, and gives each a concrete "ready to run"
plan (Docker/install + data adapter + comparison metric). *(synthesis — survey of cited external
sources + the prototype's own measured failure decomposition.)*

## TL;DR — the 2 picks

1. **hloc (SuperPoint + LightGlue + NetVLAD retrieval)** — a learned **relocalization front-end**.
   It attacks the *exact* gate the prototype isolated as binding: **geometric pose verification
   (PnP inliers)**. Same build-map→localize-query→PnP-with-inliers flow we already measure, but
   with learned features + a learned matcher that produce dense, geometrically-consistent
   correspondences where ORB+RANSAC returns 0 inliers. Lightweight (SuperPoint+LightGlue ≈ 14M
   params, < 2 GB VRAM — **fits our 4 GB GPU, and is CPU-runnable offline**), pip-installable,
   bundles `pycolmap`. Can stand alone *or* slot under RTAB-Map. **Lowest-risk, highest-relevance.**
2. **MASt3R-SLAM** — a learned **full-SLAM** alternative (CVPR 2025). Its premise is robust *dense
   pointmap* matching from a 3D-reconstruction foundation model, which **bypasses the brittle
   sparse-feature→triangulate→PnP geometry** that fails for us; it has built-in image-retrieval
   relocalization + loop closure, ingests an image folder + `intrinsics.yaml`, and we can hand it
   metric scale from our calibrated stereo baseline. **Caveat (honest):** built/benchmarked on an
   RTX 4090; on our 4 GB GPU it is **offline-only at reduced resolution** — fine for a bake-off
   (we don't need real-time), but the heavier, higher-risk pick.

**What to install/run:** `pip install -e` hloc (+ its InLoc/SfM pipeline) and MASt3R-SLAM (conda,
torch 2.5.1/CUDA 11.8, downloads MASt3R weights). Both consume the KITTI-style folders we already
produce (`make_kitti_dataset.py`). Comparison metric = **cross-session relocalization rate**
(fraction of held-out probe frames that recover a correct absolute pose) on the *same*
`s3_map` + `reloc_test2` pair RTAB-Map scored, plus **PnP / pose-verification inlier counts** on
the right-place matches (the number RTAB-Map gets 0 on 88% of the time).

## Source

- [src: hloc-repo] hloc / Hierarchical-Localization (CVG/ETH). Build-SfM-then-localize pipeline;
  SuperPoint + SuperGlue/LightGlue + NetVLAD; outputs PnP pose + RANSAC inlier log; pip-installable,
  bundles `pycolmap` (no separate COLMAP since v1.3); InLoc indoor pipeline example.
  https://github.com/cvg/Hierarchical-Localization
- [src: lightglue-repo] LightGlue: Local Feature Matching at Light Speed (ICCV 2023). ~14M params,
  ~44 ms/pair (22 FPS) on RTX4080-12GB; adaptive depth/width; FlashAttention + mixed precision.
  https://github.com/cvg/LightGlue · paper https://openaccess.thecvf.com/content/ICCV2023/papers/Lindenberger_LightGlue_Local_Feature_Matching_at_Light_Speed_ICCV_2023_paper.pdf
- [src: superpoint] SuperPoint self-supervised interest point detector & descriptor (used as hloc's
  default local feature). Learned descriptors are robustly more illumination/viewpoint invariant
  than BRIEF/ORB. https://github.com/magicleap/SuperPointPretrainedNetwork
- [src: mast3r-slam-repo] MASt3R-SLAM (CVPR 2025, Murai/Dexheimer/Davison, Imperial). Real-time dense
  SLAM with 3D-reconstruction priors; incremental image-retrieval DB → real-time relocalization +
  loop closure; calibrated intrinsics via `intrinsics.yaml`; image folder / video / RealSense input;
  15 FPS on RTX 4090. https://github.com/rmurai0610/MASt3R-SLAM · paper https://arxiv.org/abs/2412.12392
- [src: dpv-slam] DPV-SLAM / DPVO (ECCV 2024, Princeton-VL). Deep patch monocular SLAM, single-GPU,
  proximity + DBoW2 loop closure; 5–7 GB VRAM. https://github.com/princeton-vl/DPVO ·
  paper https://arxiv.org/pdf/2408.01654 — surveyed in [[learned-slam]].
- [src: orbslam3] ORB-SLAM3 (TRO 2021). Atlas multi-map, MLPnP relocalization, pure-localization mode,
  stereo/stereo-inertial. https://arxiv.org/abs/2007.11898
- [src: eigenplaces] EigenPlaces (ICCV 2023): viewpoint-robust VPR, 50% smaller descriptors / 60%
  less train-GPU than prior SOTA. https://arxiv.org/pdf/2308.10832
- [src: anyloc] AnyLoc (RA-L 2023): DINOv2-VLAD universal VPR; **highest recall across indoor
  datasets**, +5% over MixVPR / +20% over CosPlace (R@1), no retraining. arXiv 2308.00688.
- [src: rtabmap-superpoint] introlab/rtabmap issue #1221 + #957: using SuperPoint/SuperGlue inside
  RTAB-Map requires OpenCV built **with CUDA + Torch**; otherwise it silently falls back to GFTT/ORB
  and the Torch feature "cannot be used." https://github.com/introlab/rtabmap/issues/1221
- Prototype measured failure decomposition: `drone-prototype/docs/mapping-report-v1.md` §4c–4e
  (overlap-then-geometry sequential gates; **88% of right-place matches get 0 PnP inliers** once
  overlap is achieved), `docs/parked.md` P-002 (calibration), [[passive-stereo-robustification]].

## Related

[[slam]] · [[methods-reading-list]] · [[learned-slam]] · [[visual-inertial-slam]] · [[indoor-cluttered-slam]] ·
[[map-then-navigate]] · [[passive-stereo-robustification]] · [[slam-toolbox]] · [[2d-lidar-slam]] ·
[[home-tidy-drone-prototype]] · [[system-architecture]]

---

## 1. The problem an alternative must beat (what the prototype isolated)

This is **not** "find a better SLAM" in the abstract — the prototype has already narrowed the
failure to a specific stage, and a candidate is only interesting if it moves *that* stage
(`mapping-report-v1.md` §4c–4e):

- **Relocalization is two sequential gates:** (1) **appearance recall** — the place-recognition
  index must *propose* the right map location for the live frame; (2) **geometric verification** —
  PnP/RANSAC must confirm the pose from 2D–3D correspondences.
- RTAB-Map (stereo) clears gate 1 once the probe re-views the mapped path (a *purpose-built*
  `reloc_test2` got an appearance match for ~97% of rejected frames), but then **fails gate 2
  catastrophically: 113/129 ≈ 88% of right-place matches return 0 PnP inliers** despite 100+
  appearance matches per frame. End-to-end cross-session rate ≈ **2–14%**.
- **Why gate 2 fails (diagnosed, not guessed):** strong 2D matches + zero pose inliers is the
  signature of **noisy / wrong triangulated 3D points** — prototype-grade stereo calibration
  (P-002, 2.45 px RMS) and **spurious far depth** on textureless surfaces (a blank wall read as
  12–43 m). An *offline* ORB+stereo+PnP re-run recovered 73/145 inliers on a pair RTAB-Map
  rejected — i.e. the geometry is often *solvable*, lost on brittle features + thresholds.

**So the bar for a candidate:** improve **geometric pose verification under passive-stereo, low-
texture, prototype-calibration conditions** — either by (a) better local features + matcher that
survive where ORB dies (front-end swap), or (b) a fundamentally different geometry estimator that
doesn't lean on sparse triangulated points (dense-pointmap full SLAM). The two picks are exactly
one of each.

## 2. Survey — the 2023–2026 candidate field

### Bucket A — full SLAM stacks

| Method | Sensor / scale | Reloc + save-map? | Fits our 4 GB GPU? | Verdict for us |
|---|---|---|---|---|
| **RTAB-Map (stereo)** — *incumbent* | passive stereo, CPU | ✅ native `.db` save + DBoW2 appearance reloc | ✅ CPU | Baseline. Gate-1 OK, **gate-2 (PnP) is the wall** [src: prototype]. |
| **ORB-SLAM3** | stereo / stereo-inertial | ✅ Atlas multi-map, MLPnP reloc, pure-localization mode [src: orbslam3] | ✅ CPU | Same **sparse-ORB→PnP** family that's failing us; prior bench note: **fails long-path room mapping** (`mapping-report-v1.md` §1). Swapping *its* features for SuperPoint needs a custom build — same pain as RTAB-Map. Not a fresh lever. |
| **MASt3R-SLAM** (CVPR 2025) | monocular/calibrated, dense | ✅ image-retrieval DB → real-time reloc + loop closure [src: mast3r-slam-repo] | ⚠️ offline-only, reduced res (4090-class native) | **Dense pointmap matching bypasses sparse-PnP** — directly targets our gate-2 mechanism. **PICK #2.** |
| **DPV-SLAM / DPVO** (ECCV 2024) | **monocular**, deep patch VO | ✅ proximity + DBoW2 loop closure [src: dpv-slam] | ❌ **5–7 GB VRAM** | Monocular (needs external metric scale), and its VRAM exceeds our 4 GB. Strong method, wrong fit *this* hardware. Already covered in [[learned-slam]]. |
| **DROID-SLAM** | mono/stereo, dense flow | loop closure, no clean save/reload reloc | ❌ ~**20 GB VRAM** | Heaviest; MASt3R-SLAM supersedes it on accuracy at a fraction of the memory [src: mast3r-slam-repo]. Out. |
| **VINS-Fusion / OKVIS2 / Basalt** | stereo + **IMU** | VIO-class; loop closure varies | ✅ CPU | **We have no IMU yet.** VIO is rung-1 of [[passive-stereo-robustification]] but is a *different* robustification axis (bridging starvation), not a fix for the cross-session **PnP** gate. Park until an IMU is on the rig. |
| GS-LIVO / VIGS / GLC-SLAM (3DGS) | need LiDAR or RGB-D + big GPU | — | ❌ | LiDAR-inertial or desktop-GPU dense 3DGS — outside the passive-stereo + 4 GB envelope ([[learned-slam]], [[indoor-cluttered-slam]]). |

### Bucket B — relocalization / VPR front-ends (the part actually failing)

| Method | Role | Fits us? | Verdict |
|---|---|---|---|
| **hloc (SuperPoint + LightGlue + NetVLAD)** | full reloc front-end: retrieval → learned match → PnP | ✅ < 2 GB VRAM / CPU-capable [src: lightglue-repo] | Directly replaces the failing ORB→PnP path with learned features + matcher; outputs the **exact PnP-inlier metric** we measure. **PICK #1.** |
| **LightGlue** alone | learned matcher (SuperGlue successor) | ✅ ~14M params, 22 FPS [src: lightglue-repo] | The matching engine inside pick #1; not a standalone system. |
| **NetVLAD / EigenPlaces / AnyLoc / MegaLoc** | global descriptor for **gate-1 recall** | ✅ | Fixes the *recall* gate (the §4d limiter), not the *geometry* gate. **AnyLoc (DINOv2-VLAD) is best-recall indoors** [src: anyloc]; EigenPlaces is the cheap viewpoint-robust option [src: eigenplaces]. Use as the retrieval stage **inside hloc** — not a separate bake-off entry. |
| learned local features (SuperPoint, DISK, ALIKED, XFeat) | robust keypoints for PnP | ✅ | The lever for **gate-2**; SuperPoint is hloc's default. Bundled into pick #1. |

**Reading of the field:** the cleanest, lowest-risk experiment is a **learned relocalization
front-end (hloc)** that swaps the failing ORB→PnP stage for SuperPoint+LightGlue while keeping the
build→save→localize structure identical to RTAB-Map — an apples-to-apples gate-2 comparison. The
strongest *full-stack* contrast that fits our hardware (offline) is **MASt3R-SLAM**, whose dense-
pointmap geometry is a fundamentally different bet on the same failure. DPV-SLAM and DROID-SLAM are
ruled out by VRAM; ORB-SLAM3 is the same sparse-PnP family we're already failing; VIO/3DGS/LiDAR
methods are off-axis for the passive-stereo + no-IMU + 4 GB envelope. Hence the pairing below.

## 3. PICK #1 — hloc (SuperPoint + LightGlue + retrieval)

**Why this one.** Our binding constraint is **gate-2: PnP geometric verification on right-place
matches (88% 0-inlier)**. hloc is purpose-built for exactly this loop — build an SfM reference from
mapping images, then for each query image retrieve candidate references (NetVLAD/AnyLoc), match
with **SuperPoint+LightGlue**, and solve **PnP, logging RANSAC inliers** [src: hloc-repo]. Learned
features + a learned matcher produce far more *geometrically consistent* correspondences on low-
texture / mildly-miscalibrated stereo than ORB+nearest-neighbour, which is the documented reason
ORB→PnP collapses for us. It is also the **lowest-risk** option: SuperPoint+LightGlue is ~14M
params and < 2 GB VRAM — **runs on our RTX 3050 4 GB, and even CPU-only offline** [src: lightglue-repo].
It can be run **standalone** (its own SfM map + localizer) or, later, **slotted under RTAB-Map** as
the feature/matcher (the [[passive-stereo-robustification]] rung-3 idea) — but standalone is the
clean bake-off.

**Install (clean, pip).**
```bash
git clone --recursive https://github.com/cvg/Hierarchical-Localization hloc
python -m pip install -e ./hloc          # bundles pycolmap; COLMAP not required since v1.3 [src: hloc-repo]
# torch with CUDA 11.8 (driver 535 on the box supports it); CPU-only also works, slower
```
GPU: optional but helps; fits our 4 GB. License: Apache-2.0 (hloc) / SuperPoint+SuperGlue weights
are **research-only / non-commercial** — fine for a Phase-1 prototype, flag for any product use
(swap to LightGlue+DISK/ALIKED, which are permissive, before commercialising).

**Data adapter (we already have 90% of it).** hloc consumes **plain image folders** + camera
intrinsics; no IMU, no special container. We already emit rectified left/right PNGs + KITTI
`calib.txt`. Plan:
- **Reference (map) images:** the **left** frames of the mapping sweep (`room_sweep3` / `s3_map`),
  e.g. 1-in-N subsampled keyframes.
- **Query images:** the **left** frames of the relocalization probe (`reloc_test2`) — the *same*
  pair RTAB-Map scored, so the comparison is apples-to-apples.
- **Intrinsics:** pull `fx, fy, cx, cy` straight from our KITTI `P0` (left rectified projection
  matrix); feed as a COLMAP `PINHOLE`/`SIMPLE_PINHOLE` camera. A ~10-line writer alongside the
  existing `src/slam/make_kitti_dataset.py`.
- **Metric scale:** SfM-from-left-only is up-to-scale. Two clean ways to get metric pose: (a) seed
  COLMAP triangulation with **stereo depth** (our SGBM/baseline `B=57.8 mm`) so the reference map is
  metric; or (b) compare in a Sim(3)-aligned frame for the *rate* metric (which doesn't need metric
  scale — see below). Start with (b), add (a) if we want metric pose error.

**Run (build → save → relocalize).**
```bash
# 1. extract features on reference images (SuperPoint) + build retrieval DB (NetVLAD)
# 2. SfM triangulation -> reference COLMAP model  (THIS IS THE SAVED MAP)
# 3. for each query frame: retrieve top-K refs, LightGlue match, PnP -> pose + inliers
python -m hloc.pipelines.<inloc-style>   # adapt the InLoc / 7-Scenes pipeline scripts [src: hloc-repo]
```
The reference COLMAP model **is** the persistable map (save the folder; a fresh process reloads it
to localize new queries — the mandate's build→save→relocalize, mirrored).

**Effort:** ~0.5–1 day (mostly the intrinsics/keyframe adapter; the pipeline scripts exist).

## 4. PICK #2 — MASt3R-SLAM

**Why this one.** It's the full-stack alternative that bets *differently* on geometry: instead of
sparse keypoints → triangulate → PnP (our failure path), it matches **dense pointmaps** predicted
by the MASt3R two-view 3D-reconstruction prior, with tracking, local fusion, loop closure, and an
**incremental image-retrieval DB enabling real-time relocalization** [src: mast3r-slam-repo]. That
dense-geometry front-end is robust on exactly the low-texture / weak-calibration regime where our
sparse PnP dies, and it **outperforms ORB-SLAM and DROID-SLAM** on accuracy at a fraction of
DROID's memory [src: mast3r-slam-repo]. It takes an **image folder + `intrinsics.yaml`**, so it
ingests our left-frame sequences directly with our calibrated intrinsics, and we can hand it metric
scale from the stereo baseline.

**The honest caveat (GPU).** Built/benchmarked on an **RTX 4090** (15 FPS) [src: mast3r-slam-repo];
no published 4 GB figure, and dense pointmaps are memory-heavy. On our **RTX 3050 4 GB** expect to
run **offline only, at reduced resolution** (`--img-size 512` exists [src: mast3r-slam-repo]) and
possibly to hit OOM at full res — mitigations: smaller `--img-size`, subsample frames, shorter
clips. **For a bake-off this is acceptable** — we need a *relocalization-rate comparison*, not
real-time. If it won't fit even downsampled, that itself is a finding (a 4090-class method is not
deployable on our consumer-cost compute) and we fall back to reporting hloc-only. **This is the
higher-risk pick; sequence it after hloc.**

**Install (conda).**
```bash
git clone --recursive https://github.com/rmurai0610/MASt3R-SLAM
# conda env: torch 2.5.1 + CUDA 11.8  (matches driver 535 on the box) [src: mast3r-slam-repo]
pip install -e .            # downloads MASt3R checkpoints on first run
```
No official Docker (unofficial forks exist). License: check repo (research-leaning); flag for
product use. CUDA 11.8/12.1/12.4 wheels offered.

**Data adapter.** Minimal: MASt3R-SLAM reads a **folder of RGB images** + an `intrinsics.yaml`.
- Point it at the **left** frames of `room_sweep3` (map) and `reloc_test2` (probe).
- Write `intrinsics.yaml` from our KITTI `P0` (`fx fy cx cy`, width/height).
- For metric scale, scale the recovered trajectory by the known stereo baseline, or Sim(3)-align
  for the rate metric.

**Run (build → save → relocalize).** Run once on the mapping clip to build the map + retrieval DB;
then run the probe clip and read out **relocalization events** (the system snaps the live frame
onto the stored trajectory). If save/reload across processes isn't exposed, run map+probe in one
session but only *score* frames in the held-out probe segment — equivalent for the rate metric.
Watch VRAM with `nvidia-smi`; drop `--img-size` on OOM.

**Effort:** ~1–2 days (env + CUDA wrangling + the VRAM-fit dance is the real cost).

## 5. The comparison — same data, same metric as RTAB-Map

Run both picks on the **identical** map/probe pair RTAB-Map already scored, so numbers are directly
comparable to `mapping-report-v1.md` §4e:

| Map (reference) | Probe (held-out) | Why |
|---|---|---|
| `room_sweep3` / `s3_map` | `reloc_test2` | The overlap-fixed pair where RTAB-Map's gate-1 (recall) is OK and **gate-2 (PnP) is the isolated wall (88% 0-inlier)** — so any gain is attributable to geometry, not luck. |

**Primary metric — cross-session relocalization rate:** fraction of probe frames that recover a
**correct** absolute pose (pose consistent with the map within a tolerance, e.g. via Sim(3)-aligned
position error < threshold, or RTAB-Map's own success criterion for parity). RTAB-Map's number on
this pair is **≈ 2%** (and ~11–14% on the easier `reloc_test1`).

**Secondary / diagnostic metric — pose-verification inlier counts:** for the *right-place* matches,
report the **PnP / pose-RANSAC inlier distribution** — directly comparable to RTAB-Map's "88% get 0
inliers." This is the cleanest read of whether the new front-end actually fixes gate-2: if hloc
turns those 0-inlier frames into 30–100-inlier solves, the diagnosis (sparse-feature/calibration-
limited geometry) is confirmed and the front-end swap is the fix.

**Tertiary (if metric scale wired):** absolute pose error (cm) of relocalized frames vs the
map-frame ground-truth trajectory.

## 6. Decision summary + sequencing

- **Run hloc first** (low-risk, fits hardware, directly measures the failing PnP gate). If it lifts
  the relocalization rate and the inlier distribution, the prototype's central open problem has a
  concrete cure — and the path is *swap the feature/matcher front-end* (keep RTAB-Map's proven
  save/reload back-end, per [[passive-stereo-robustification]] rung-3), not abandon RTAB-Map.
- **Then MASt3R-SLAM** (higher-risk full-stack contrast; the VRAM fit is itself a consumer-cost
  finding). If dense-pointmap geometry clears the gate where sparse PnP can't, that's evidence the
  geometry — not just the calibration — is the lever.
- **Not run (and why):** DPV-SLAM / DROID-SLAM (VRAM > 4 GB), ORB-SLAM3 (same sparse-PnP family,
  custom build to swap features = same cost as fixing RTAB-Map), VIO stacks (no IMU yet; off-axis),
  3DGS/LiDAR (outside passive-stereo + 4 GB envelope). All parked, not dead — revisit when an IMU
  lands on the rig or compute grows.

*Cross-refs: `drone-prototype/docs/mapping-report-v1.md` §4c–4e (failure decomposition),
`docs/parked.md` P-002, `docs/data-collection-todo.md`, [[passive-stereo-robustification]],
[[learned-slam]].*
