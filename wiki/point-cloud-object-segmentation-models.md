# Point-Cloud Object Segmentation Models — The Cheapest "X Objects, Roughly Here" First Pass

How to get a **coarse object proposal / instance-seed** layer out of OUR room cloud: a rough **count + approximate location/extent** of distinct objects — "there are ~9 things, roughly here / here / here." This is explicitly **NOT** semantic labelling, **NOT** precise boundaries, **NOT** per-unit extents. It is the cheapest reliable step that answers *how many things and roughly where*, to seed the downstream pipeline ([[point-cloud-semantic-classification]] needs primitives to assign points to; the EDA095/100/115 seeded object map needs seeds).

This page exists because the wiki already covers the *learned-segmentation leaderboard* ([[ov3d-instance-seg]]) and the *point-accounting* framing ([[point-cloud-semantic-classification]]), but neither answers the narrow operational question: **for a single-plane 2D-XY LiDAR cloud + per-frame stereo, what is the honest cheapest object-proposal step, and which of the SOTA point-cloud segmentation models actually fit our data vs which simply do not run on it?** The headline answer is below; the mismatch analysis is the load-bearing content.


---

## TL;DR — the verdict up front

1. **Almost no SOTA 3D instance-segmentation model fits our data.** Mask3D, PointGroup, SoftGroup, ISBNet, OneFormer3D, OpenMask3D, Open3DIS, Open-YOLO 3D, FOLK all assume a **dense, colored, full-3D (with height) point cloud** from a structured-light/LiDAR RGB-D scan (ScanNet/S3DIS). Our **primary map cloud is single-plane 2D — XY only, no Z** ([[lidar-multiscan-capture-recipe]]). A 3D voxel/sparse-conv backbone (MinkowskiEngine) has *nothing to convolve* on a flat XY slice. These models do not under-perform on our data — they **structurally do not apply** to it.

2. **The object-part models (SAMPart3D, Point-SAM, PartSAM, S2AM3D) are the wrong scope entirely** — they segment ONE dense object mesh into PARTS (handle, leg, lid), not a room into object instances [src: sampart3d; point-sam; partsam]. Ignore them for this task.

3. **The one native-3D idea that maps onto our XY data is the BEV trick** — *SAM3D-for-detection* renders the cloud as a 2D bird's-eye image and detects/segments on that image [src: sam3d-detect]. We do not need their network: for our problem the BEV image + **classical 2D connected-components / watershed with per-wall cuts** is the cheapest viable proposal step and is the recommendation.

4. **For the stereo modality, lifting a 2D segmenter (SAM/SAM2) to the map is the honest route** — confirmed by SAM3D-for-scenes, SAMPro3D, and OV-MAP, all of which project 2D SAM masks into 3D precisely because a clean 3D cloud is unavailable [src: sam3d-scene; sampro3d; ovmap]. **We already do a version of this — EDA117** (stereo + per-frame SAM, lifted to the map) is a viable independent detector.

**Bottom line:** the cheapest viable first pass is **NOT a learned 3D model**. It is **(A) a BEV occupancy image of the cleaned 2D cloud → per-wall-cut connected-components / watershed for the count+location**, cross-checked by **(B) EDA117's stereo-SAM lift**. A learned 3D instance model is over-spec, mostly inapplicable to XY-only data, and gated by the depth-hole / no-Z problem — not by GPU.

---

## Restating the need precisely (so we don't over-scope)

| We WANT (coarse proposal) | We do NOT want here |
|---|---|
| approximate **count** of distinct objects | exact instance count to ±1 |
| approximate **location** (centroid) + rough extent (bbox / footprint blob) | precise per-object boundaries / masks |
| a **seed** the seeded pipeline (EDA095/100/115) and the point-accounting cascade ([[point-cloud-semantic-classification]]) can build on | semantic labels ("this is a chair") — that's [[semantic-object-memory]] / [[object-fingerprint-memory]]'s job downstream |
| something that **runs on our laptop** (no big GPU) and on **2D-XY + per-frame stereo** | a method needing a dense colored 3D scan |

This is an *object-proposal / instance-seed* problem, not an instance-segmentation-leaderboard problem. That re-framing is what kills most of the model list.

---

## Our two data modalities (the filter everything must pass)

1. **2D (XY-only) accumulated cloud** from the single-plane 2D LiDAR sweep — ~300k–600k points (777k in EDA116 before cleaning), **heavily multi-view oversampled, NO height/Z**. This is the **primary map cloud**. Crucially: it is a *flat slice* at roughly one height (~1.1 m, memory `rig-lidar-stereo-offset`). No surface normals out of plane, no volumetric structure, no color.
2. **Stereo-camera RGB frames** — used per-frame; depth is Z²-limited and noisy (~48% coverage on textured indoor surfaces, [[passive-stereo-robustification]]). **Not** a clean fused 3D cloud.

Any "3D point-cloud segmentation model" must be checked against *both* of these — and **neither is a dense colored 3D scan**, which is what every ScanNet/S3DIS-trained model assumes.

---

## What we already TRIED (don't re-recommend these)

- **Classical density clustering (DBSCAN / region-growing) on the wall-removed 2D object band: FAILED** — EDA116, a clean negative. With walls removed, the against-wall cabinets/counters form a near-continuous **ring around the room perimeter**; DBSCAN bridges through the corners. At the proven eps=10 cm a single cluster holds **98%** of voxels; even eps≈4.5 cm never gets the largest cluster below ~37%. **Connectivity is the wrong primitive for against-wall objects in a small room** unless the band is cut per-wall first or seeded.
- **Seeded assignment works** (EDA095/100/115): detect candidates first, assign nearest-seed. But the seeds came from a 2D auto-mapper, not from cloud segmentation per se — i.e. the seeding step is exactly the gap this page is about.
- **Stereo + per-frame 2D SAM, lifted to the map** (EDA117): viable as an *independent* detector.

The EDA116 negative is the single most important fact for this page: **raw connectivity on the 2D object band does not yield the count.** The fix is to break the perimeter ring — which is exactly what per-wall cuts (BEV) or per-frame masks (stereo SAM) do.

---

## Comparison table — every candidate against OUR constraints

| Model / method | Input it assumes | Fits our 2D-XY + stereo data? | Compute footprint | Gives rough count + location? | License |
|---|---|---|---|---|---|
| **Mask3D** [src: mask3d] | dense colored full-3D scan (voxels), ScanNet200-trained | **NO** — sparse-conv 3D backbone needs volumetric (Z) structure; flat XY slice has none | ≥8 GB VRAM, ~13 s/scene | yes IF input matched (it doesn't) | MIT |
| **PointGroup / SoftGroup / ISBNet** | dense colored 3D scan + per-point offsets/normals | **NO** — same Z/volumetric assumption; clustering on 3D offsets | GPU (≥6–8 GB) | yes IF input matched | Apache/MIT |
| **OneFormer3D** | dense colored 3D scan, unified sem+inst | **NO** — same | GPU (≥8 GB) | research |
| **OpenMask3D** [src: ov3d-wiki] | dense 3D scan + posed RGB + SAM ViT-H + CLIP | **NO** (3D) — and ≥12 GB, 5–10 min/scene | ≥12 GB, offline | yes (overkill) | MIT |
| **Open3DIS / Open-YOLO 3D** [src: ov3d-wiki] | dense 3D scan + posed RGB | **NO** (3D); A100-class | ≥8–24 GB | yes (overkill) | research |
| **FOLK** (lightest 3D-native) [src: ov3d-wiki] | Mask3D proposals on dense 3D scan | **NO** — still Mask3D backbone → needs dense 3D; not zero-shot on our domain | ≥4–6 GB, 3.6 s | yes (overkill) | research |
| **OV-MAP** [src: ovmap] | RGB-D + 2D SAM + point cloud; **synthesizes depth to fill holes** | **PARTIALLY** — 2D-mask-lift design tolerates sparse depth; still wants posed RGB-D, no XY-only mode | GPU (SAM) | yes | research |
| **SAM3D-for-scenes** [src: sam3d-scene] | point cloud + **posed RGB**; projects 2D SAM masks into 3D, no training | **PARTIALLY** — this IS the lifting route; needs posed RGB | SAM-grade GPU per frame | yes (this is EDA117's family) | Apache |
| **SAMPro3D** [src: sampro3d] | posed RGB-D frames; locates SAM prompts in 3D, training-free | **PARTIALLY** — lifting route; wants RGB-D | SAM-grade GPU | yes | research |
| **SAM3D-for-detection (BEV)** [src: sam3d-detect] | renders cloud → **2D BEV image**, segments on it | **YES (conceptually)** — BEV is the one native idea that fits XY-only data | their net needs GPU; **the BEV idea itself is free** | yes — boxes on BEV = count+location | research |
| **SAMPart3D / Point-SAM / PartSAM / S2AM3D** [src: sampart3d; point-sam; partsam] | **single dense object mesh** → PARTS | **NO — wrong task** (parts of one object, not room instances) | GPU | no (parts, not instances) | varies |
| **Classical: BEV occupancy image → per-wall-cut connected-components / watershed** | the 2D-XY cloud we already have | **YES** — native to our data, CPU-only | **CPU, sub-second**, no GPU, no training | **yes — exactly count + blob location** | n/a (Open3D/scipy/skimage) |
| **EDA117: per-frame stereo SAM → lift masks to map** | our stereo frames (already have) | **YES — already built & viable** | MobileSAM-grade (~4 GB, runs) | yes — independent detector | (MobileSAM Apache) |

**The pattern:** every YES/PARTIALLY is either a **2D-to-something-lift** (BEV image, or per-frame SAM masks) or **classical on the 2D image**. Every native-3D model is a NO on input grounds, *before* compute even enters. Compute is the second barrier; **the dense-colored-3D input assumption is the first and fatal one.**

---

## Why native-3D models structurally fail on our cloud (the mismatch, stated plainly)

The SOTA 3D instance segmenters are trained on **ScanNet/S3DIS**: dense, colored, full-3D RGB-D scans with high coverage from a structured-light sensor ([[ov3d-instance-seg]] notes ScanNet uses an Intel-RealSense-class sensor). Three of our properties each break them independently:

1. **No Z (single-plane LiDAR).** A sparse-3D conv backbone (MinkowskiEngine / SPVNAS) operates on a *voxel grid with vertical extent*. Our LiDAR cloud is a ~flat XY slice — there is no vertical structure to convolve. An instance like "chair" is defined by its 3D shape; in our slice it is a few short arcs of returns at one height. The model has never seen, and cannot represent, this input.
2. **No color.** OpenMask3D/Open3DIS/FOLK all lean on CLIP features from RGB crops to even *propose* and certainly to *describe* instances. Our LiDAR cloud has no color; the stereo color is per-frame, not fused per-point.
3. **Sparse / depth-holed (stereo branch).** Even if we built a *3D* cloud from stereo, ~48% coverage means ~52% of typical surfaces (blank walls, white ceilings) return no points — Mask3D-based methods cannot segment objects absent from the cloud ([[ov3d-instance-seg]] §failure modes). OV-MAP's depth-synthesis hole-filling is the only design that confronts this, and it is research-stage and still wants posed RGB-D.

**Conclusion:** these are excellent models for the data they were built for; **we do not have that data and the consumer-cost tenet means we never will** (no expensive dense 3D LiDAR). Re-recommending them would be dishonest about our regime.

---

## The two routes that DO fit, in detail

### Route A (recommended primary) — BEV occupancy image → per-wall-cut connected-components / watershed
The honest native operation on a **2D-XY cloud** is to treat it as a **2D image** (the SAM3D-for-detection BEV insight [src: sam3d-detect], minus their network):

1. **Clean the cloud** first ([[point-cloud-denoising-methods]] pipeline: operator mask → voxel → SOR/ROR → keep object band), and **remove wall points** using the *fitted wall lines* ([[floorplan-reconstruction-methods]]).
2. **Rasterize** the surviving object-band points into a **BEV occupancy / density image** (e.g. 1–2 cm/pixel grid, value = point count or binary).
3. **Cut the perimeter ring per-wall.** The EDA116 failure is the against-wall band forming one connected ring. Use the fitted wall lines to **slice the band into per-wall segments** (project points to their nearest wall, split at corners) *before* connectivity — this is the missing primitive EDA116 identified.
4. **Connected components** (skimage `label`) or **watershed** (skimage `watershed` seeded by local-density maxima — the same family robot vacuums use for *room* segmentation, [[consumer-robot-vacuum-mapping]] / [[room-segmentation-floor-plan]] ROSE²) on the per-wall-cut image → each component = one object proposal.
5. **Count = number of components above a physical-size floor; location = component centroid; extent = component bbox/blob.** Done — that is the coarse "X things, roughly here."

Cost: **CPU, sub-second, no GPU, no training, fully reproducible** (Open3D + scipy + scikit-image). This directly operationalises the need and uses primitives we already compute. Watershed on the density image specifically helps where two against-wall objects touch — a density saddle splits them where pure connectivity merges them.

### Route B (recommended cross-check, already built) — per-frame stereo SAM, lifted to the map
This is the **2D-mask-lift** route that the literature (SAM3D-for-scenes, SAMPro3D, OV-MAP) converges on precisely *because* a clean 3D cloud is unavailable [src: sam3d-scene; sampro3d; ovmap]. **EDA117 already does a version of it** and is viable as an independent detector. A learned model would improve it at two seams, both lightweight upgrades — not new 3D models:

- **SAM2 instead of per-frame SAM** [src: sam2] — SAM2's memory propagates a mask across frames as a *tracklet*, so the same physical object gets a consistent instance across the sweep before lifting, reducing the merge/split ambiguity EDA117 resolves by clustering lifted masks. Runs at MobileSAM-class cost.
- **Promptable proposals** — seed SAM/SAM2 with Route-A's BEV component centroids (cross-modal agreement = the [[robust-evidence-mapping-principle]] reliability signal: an object both routes find is high-confidence).

Route B needs only the GPU we already use for MobileSAM (~4 GB, anaconda env, memory `dual-python-env-and-sam`) — no MinkowskiEngine, no dense 3D cloud.

---

## What would actually be the cheapest viable first pass (the verdict)

**Build Route A.** A **BEV occupancy/density image of the cleaned, wall-removed object band, cut per-wall by the fitted wall lines, then connected-components (or density-seeded watershed), keeping components above a physical-size floor.** It is CPU-only, sub-second, training-free, native to our 2D-XY cloud, and it directly fixes the EDA116 negative (the per-wall cut breaks the perimeter ring that defeated raw DBSCAN). Centroids = locations, component count = object count.

**Cross-check with Route B (EDA117 stereo-SAM lift), already built.** Where both agree, the proposal is high-confidence ([[robust-evidence-mapping-principle]]); where only one fires, flag it. SAM2-tracklets is the one cheap learned upgrade worth trying.

**Do NOT reach for a learned 3D instance model.** Mask3D/FOLK/OpenMask3D et al. are over-spec, require dense colored 3D input we do not and will not have (consumer-cost tenet), and are gated by the no-Z / depth-hole problem, not by GPU. They are the right tool only IF a future active-stereo or dense-depth sensor lands AND an offline batch pass is acceptable — a Phase-2 question, not this one.

**Rough effort to try Route A:** small — one EDA. Reuse the EDA116 cleaned object cloud and EDA110 wall lines (both exist), rasterize to a BEV grid, project-to-nearest-wall + corner-split, `skimage.measure.label` / `skimage.segmentation.watershed`, size-gate, plot centroids over the floor plan. No new dependencies beyond scikit-image in the numpy-1.x env (memory `dual-python-env-and-sam`). Half a day. Route B already exists (EDA117); the SAM2-tracklet upgrade is a separate, optional follow-up.

---

## Source

- [src: mask3d] Schult et al., "Mask3D: Mask Transformer for 3D Semantic Instance Segmentation," ICRA 2023, arXiv:2210.03105.
- [src: ov3d-wiki] [[ov3d-instance-seg]] — this wiki's OV-3DIS compute/VRAM/accuracy synthesis (OpenMask3D, Open3DIS, Open-YOLO 3D, FOLK, OV-MAP, Mask3D), incl. ScanNet200 numbers and passive-stereo depth-hole failure modes. Primary sources cited there.
- [src: ovmap] Kim et al., "OV-MAP: Open-Vocabulary Zero-Shot 3D Instance Segmentation Map for Robots," arXiv:2506.11585, 2025 — 2D-SAM-mask projection + synthetic-depth hole-filling (the only method designed for sparse depth).
- [src: sam3d-scene] Yang et al., "SAM3D: Segment Anything in 3D Scenes," arXiv:2306.03908 — projects 2D SAM masks into 3D via posed RGB, training-free (the 2D-lift family).
- [src: sampro3d] Xu et al., "SAMPro3D: Locating SAM Prompts in 3D for Zero-Shot 3D Instance Segmentation," arXiv:2311.17707 — training-free, locates SAM prompts in 3D, aligns projected masks across frames. https://mutianxu.github.io/sampro3d/
- [src: sam3d-detect] "SAM3D: Zero-Shot 3D Object Detection via Segment Anything Model," arXiv:2306.02245 — renders the cloud as a 2D **Bird's-Eye-View** image and segments on it (the BEV insight relevant to our XY-only cloud).
- [src: sam2] Ravi et al., "SAM 2: Segment Anything in Images and Videos," Meta, 2024 — memory-based temporal mask propagation (tracklets across frames). https://docs.ultralytics.com/models/sam-2
- [src: sampart3d] Yang et al., "SAMPart3D: Segment Any Part in 3D Objects," arXiv:2411.07184 — **single-object PART** segmentation (wrong scope for room instances). https://github.com/Pointcept/SAMPart3D
- [src: point-sam] Zhou et al., "Point-SAM: Promptable 3D Segmentation Model for Point Clouds," ICLR 2025 — promptable, but object/part-scale and needs dense input. https://point-sam.github.io/
- [src: partsam] "PartSAM: A Scalable Promptable Part Segmentation Model Trained on Native 3D Data," arXiv:2509.21965 — native-3D PART segmentation (wrong scope).
- Internal negatives/positives: `eda/EDA116-cloud-object-seeds/` (DBSCAN perimeter-ring failure — the clean NEGATIVE that motivates per-wall cuts), `eda/EDA117-stereo-sam-objects/` (stereo+SAM lift — viable independent detector), `eda/EDA095/EDA100/EDA115` (seeded object map — works given seeds).

*Captures: 2026-06-16. This page is the object-PROPOSAL companion to [[ov3d-instance-seg]] (the OV-3DIS leaderboard/compute envelope) and [[point-cloud-semantic-classification]] (point→primitive accounting). Where those answer "which learned model & how heavy" and "how to assign points to primitives we already hold," this one answers "what is the cheapest honest way to GET the rough count+location seeds on our 2D-XY + stereo data" — and finds the answer is classical-on-BEV + the existing stereo-SAM lift, not a learned 3D model.*

## Related

[[ov3d-instance-seg]] · [[point-cloud-semantic-classification]] · [[point-cloud-denoising-methods]] · [[floorplan-reconstruction-methods]] · [[room-segmentation-floor-plan]] · [[semantic-object-memory]] · [[object-fingerprint-memory]] · [[robust-evidence-mapping-principle]] · [[consumer-robot-vacuum-mapping]]
