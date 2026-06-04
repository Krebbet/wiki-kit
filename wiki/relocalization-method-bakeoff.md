# Relocalization Method Bake-Off (Passive-Stereo, Marker-Free, Indoor)

The `drone-prototype` make-or-break problem: build an indoor room map from a **passive USB stereo**
camera, save it, then in a **fresh pass recover absolute pose** (marker-free relocalization). The
prototype isolated exactly which gate of RTAB-Map's pipeline failed, picked the right alternative,
**and has now RUN it** — so this page is no longer a plan: it carries the **measured outcome
(EDA003–EDA009)**. Bottom line: **the bake-off is decided — a learned relocalization front-end
(hloc) clears the wall, and pooling several mapping passes builds the best anchor map.** *(synthesis
— cited external sources + the prototype's own measured results; sources in `docs/experiments-log.md`
EDA003–009 + each `eda/EDA00N-*/major-findings.md`.)*

## TL;DR — the result (proven, not planned)

- **The wall was the FRONT-END, not calibration.** RTAB-Map's classical ORB→RANSAC→PnP geometric
  verification collapses: **88% of right-place matches return 0 PnP inliers → ~2–4% cross-session
  reloc**, and it is **map-agnostic** (~2.1–4.1% no matter how the map is built — EDA006/009). Swap
  in **hloc (SuperPoint + LightGlue + NetVLAD → COLMAP SfM → pycolmap PnP)** on the *same* maps and
  the *same* fixed calibration, and the wall is gone: **EDA003 96%**, **EDA004 82.6% on fresh
  out-of-sample data**, with the 0-inlier failure mode **eliminated outright (0/910)**. Because
  intrinsics were held FIXED (no recalibration — the control), the gain isolates the learned
  feature/matcher/geometry front-end. **P-002 (calibration) demoted; pick #1 = hloc.**
- **Metric scale recovered AND validated against ground truth.** EDA005 recovered scale
  (≈0.833 m/SfM-unit, stable ~2%; ~34 cm GT-free loop-closure drift). EDA008 then validated it
  **absolutely against the human's tape measurement**: room **width 2.99 m vs GT 3.048 m = −1.9%**
  (~6 cm on 3 m) → the map is **metrically trustworthy to ~⅓ m**. **P-005 RESOLVED.**
- **Best anchor map = several overlapping passes POOLED into one SfM.** EDA006 found a single broad
  fixed-stride sweep is zero-sum (closes the coverage tail 52→87% but thins the body 96→72%, net
  −6 pp). **EDA009 resolved it: pool sweep4 ∪ sweep7 into ONE SfM → 93.6% overall (+11 pp), body
  96% AND tail 88%, no trade-off** — and the two same-room passes **co-registered automatically**
  (944/947 via NetVLAD), no explicit cross-session loop closure. See [[anchor-map-protocol]].

**Measured comparison metric:** cross-session relocalization rate (fraction of held-out probe
frames recovering a correct absolute pose) + PnP-inlier distribution on right-place matches, on the
*same* map/probe pairs RTAB-Map scored. Full numbers in §"Measured results" below.

## The 2 picks (as decided going in — pick #1 ran and won; pick #2 demoted)

1. **hloc (SuperPoint + LightGlue + NetVLAD retrieval)** — a learned **relocalization front-end**
   attacking the binding gate (geometric PnP verification). Same build-map→localize-query→PnP flow,
   learned features + matcher producing dense geometrically-consistent correspondences where
   ORB+RANSAC returns 0 inliers. ~14M params, < 2 GB VRAM (fits our 4 GB GPU, CPU-runnable offline),
   pip-installable, bundles `pycolmap`. **RAN — EDA003/004/006/009 (see below). Won decisively.**
2. **MASt3R-SLAM** — a learned **full-SLAM** alternative (CVPR 2025); dense-pointmap matching that
   bypasses sparse-triangulate→PnP. **DEMOTED, not run:** hloc already cleared the wall, so the
   higher-risk 4090-class full-stack contrast was unnecessary. Still the queued cross-check if a
   fundamentally-different geometry estimator is ever wanted (offline-only on our 4 GB GPU).

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
- Prototype measured failure decomposition + the run results: `drone-prototype/docs/mapping-report-v1.md`
  §4c–4e (overlap-then-geometry sequential gates; **88% of right-place matches get 0 PnP inliers**);
  **`docs/experiments-log.md` EDA003–009** + each `eda/EDA00N-*/major-findings.md` (the measured
  bake-off — hloc 82.6–96% vs RTAB ~2–4%, multi-sweep 93.6%, metric scale validated −1.9% vs GT);
  `docs/eda-mapping-state.md` (map-artifact + integration analysis); `data/ground-truth/room-dims.md`
  (the tape-measured GT); `docs/parked.md` (P-002 demoted, P-005 resolved); [[passive-stereo-robustification]].

## Related

[[anchor-map-protocol]] · [[slam]] · [[methods-reading-list]] · [[learned-slam]] · [[visual-inertial-slam]] ·
[[indoor-cluttered-slam]] · [[map-then-navigate]] · [[passive-stereo-robustification]] · [[slam-toolbox]] ·
[[2d-lidar-slam]] · [[imu-vio-integration-reality]] · [[home-tidy-drone-prototype]] · [[system-architecture]]

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
one of each. **The prototype ran (a) — hloc — and it cleared the bar; the measured results are
in §1b.**

## 1b. Measured results — hloc vs RTAB-Map, on our own data (EDA003–EDA009)

The bake-off was **run**, on the prototype's recorded living/dining-room sweeps. Every row holds
intrinsics FIXED to our rectified calibration (the control that isolates the front-end); RTAB-Map
and hloc see the same rectified pixels. Sources: `docs/experiments-log.md` (EDA003–009) +
`eda/EDA00N-*/major-findings.md`.

| EDA | Map → probe (held-out) | hloc reloc | RTAB-Map reloc | Right-place 0-PnP-inlier (hloc) | What it proved |
|---|---|---|---|---|---|
| **003** | sweep3 → reloc_test2 | **96.0%** (311/324) | ~2% | **0%** (0/324), median 295 inliers | The wall is the ORB→PnP **front-end**, not calibration — same map+calib, ~48× lift. |
| **004** | sweep4 → sweep6 (fresh) | **82.6%** (753/912) | **4.1%** | **0%** (0/910), median 82 | Breakthrough **generalizes** out-of-sample (~20×). Residual fails = a **coverage** tail (seg7-9 36–62%), not blur (r≈−0.13). |
| **006** | sweep7 (broad) → sweep6 | 76.6% (699/912) | **2.1%** | 0%, mean reproj 1.48 px | Broad sweep **closes the tail (52→87%)** but **thins the body (96→72%)** → net −6 pp. Density became the live variable. RTAB **map-agnostic**. |
| **009** | **sweep4 ∪ sweep7 pooled** → sweep6 | **93.6%** (854/912) | — (settled) | 0% (0/911), median 198 | **Pooling sweeps wins outright:** body 96% **AND** tail 88%, +11 pp; the two passes **co-register automatically** (944/947). |

**Metric scale (EDA005 → EDA008):** the hloc SfM is up-to-scale; aligning it to RTAB-Map's
stereo-metric frame recovers **≈0.833 m/SfM-unit** (stable ~2%), GT-free **loop-closure drift ~34 cm**
(median, p90 56). EDA008 then anchored it to the human's **tape measurement**: room **width 2.99 m
vs GT 3.048 m = −1.9%** — *consistency was correctness*, no hidden scale bias; the anchor is good to
~⅓ m, adequate for room-level navigation. (`data/ground-truth/room-dims.md`; **P-005 RESOLVED**.)

**Reading:** for **mandate-1 (a reusable navigation-anchor map), relocalization is essentially
proven.** The front-end that was the wall is solved (0-inlier mode eliminated), the rate is high
(93.6% on the best map), the map is metrically trustworthy, and the recipe for building a good
anchor is known (pool overlapping passes — [[anchor-map-protocol]]). Open: online/under-RTAB-Map
integration (offline batch SfM today) + permissive weights (research-only SuperPoint/SuperGlue →
DISK/ALIKED for product). The detailed map-artifact + integration analysis is in
`drone-prototype/docs/eda-mapping-state.md`.

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

*(This was the plan; it was executed — see §1b for the actual measured numbers. Kept here for the
methodology.)* Run both picks on the **identical** map/probe pair RTAB-Map already scored, so numbers
are directly comparable to `mapping-report-v1.md` §4e:

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

## 6. Decision summary + outcome

- **hloc ran first and WON** (EDA003/004/006/009): it lifted relocalization from ~2–4% to 82.6–96%
  and **eliminated the 0-inlier failure mode** (0/910). The cure is confirmed: *swap the
  feature/matcher front-end* (keep RTAB-Map's proven metric save/reload back-end, per
  [[passive-stereo-robustification]] rung-3), **not** abandon RTAB-Map and **not** grind
  calibration. The forward path is the **online integration** — put SuperPoint+LightGlue under
  RTAB-Map's live back-end (or run hloc as an offline-map + live-localize service) with permissive
  weights. Map-build recipe in [[anchor-map-protocol]].
- **MASt3R-SLAM demoted, not run:** hloc already cleared the wall, so the higher-risk 4090-class
  full-stack contrast was unnecessary. Keep as the queued cross-check if a fundamentally-different
  geometry estimator is ever wanted; the 4 GB VRAM fit would itself be a consumer-cost finding.
- **Not run (and why):** DPV-SLAM / DROID-SLAM (VRAM > 4 GB), ORB-SLAM3 (same sparse-PnP family,
  custom build to swap features = same cost as fixing RTAB-Map), VIO stacks (no IMU yet; off-axis —
  see [[imu-vio-integration-reality]]), 3DGS/LiDAR (outside passive-stereo + 4 GB envelope). All
  parked, not dead — revisit when an IMU lands on the rig or compute grows.

*Cross-refs: `drone-prototype/docs/experiments-log.md` (EDA003–009), `eda/EDA00N-*/major-findings.md`,
`docs/eda-mapping-state.md` (map-artifact + integration analysis), `docs/mapping-report-v1.md` §4c–4e
(original failure decomposition), `docs/parked.md` (P-002 demoted, P-005 resolved),
[[anchor-map-protocol]], [[passive-stereo-robustification]], [[learned-slam]].*
