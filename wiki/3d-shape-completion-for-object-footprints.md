# 3D Shape Completion for Object Footprints — Method Survey & Recommendation

How to turn a **partial observation of an indoor object** (a coarse oriented H×W×D box + sparse one-sided
points + a few RGB views) into a **dense, complete 3D point cloud / shape** for the object-anchoring layer.
A methods page: surveys the four deep-learning families, ranks them for *our* regime, and recommends a
concrete first build. Grounded in the drone-prototype object pipeline (EDA127/132/133) and researched
2026-06 (EDA135).

> **Read alongside:** [[apple-roomplan]] (the production ceiling — RoomPlan outputs *boxes*, not shapes),
> [[mapping-stack-design]] (where the object layer sits), [[object-fingerprint-memory]] (per-instance memory
> the shape feeds), [[stereo-dense-reconstruction]] / [[stereo-3d-mapping-known-poses]] (the observed-point
> source), [[robust-evidence-mapping-principle]] (build from the reliable signal, flag the rest unknown).

---

## TL;DR

- **The problem is *completion-from-very-partial*, not reconstruction.** Per object we have: a decimetre
  oriented **H×W×D box** (W,D from multi-view bbox-edge triangulation, H camera-limited), **partial surface
  points** (one ~1.1 m horizontal 2D-LiDAR slice + noisy stereo, camera-facing side only, the **wall-facing
  back fully occluded**), and a few **SfM-posed RGB views**. We want the whole shape — including the
  unobserved back.
- **The box + category label are strong priors.** The single most important selection axis is: *does the
  method exploit the known box and category, and can it invent the unobserved back?* Most academic methods
  do neither.
- **Two structural facts decide everything:**
  1. **Point-cloud completion nets** (PCN…AdaPoinTr) and **prior-free implicit recon** (ConvONet, POCO, SAP,
     NKSR) **cannot invent the occluded back.** Completion nets are ShapeNet-unit-normalized object priors
     that ignore our box and don't generalize to real metric appliance partials; prior-free implicit methods
     *interpolate observed surface* but have no prior to draw an unseen back from (and SAP/NKSR need oriented
     normals our one-sided noisy points can't supply).
  2. **The only families that hallucinate the back** are **category-prior auto-decoders** (DeepSDF — but no
     appliance weights ship, needs per-category training) and **image-to-3D generative** (TripoSR, Shap-E,
     Hunyuan3D — RGB priors invent a plausible full shape, but it's *not faithful to observed points* and is
     scale-free).
- **For most of our objects (fridge, oven, dishwasher, cabinet, counter) the shape is ≈ the box.** A
  **parametric box surface sampled in the H×W×D extent** captures essentially all recoverable geometry —
  parameter-free, never fails, no library, no GPU. **This is the recommended first build.**
- **Recommendation:** build the **category→template→scale-to-box→snap-to-observed-points** route, with a
  **parametric box** for box-like categories and a **canonical ABO/GSO template** (anisotropically scaled +
  light non-rigid snap) for *structured* categories (chair, table, sofa, shelf) where the box over-claims
  occupied volume. Reserve **TripoSR** (image-to-3D, MIT, runs ~4 GB) as the prior for irregular objects
  where no template fits. The learned point-cloud-completion and prior-free implicit families are **not
  recommended** for this regime.

---

## 1. Our regime vs what the methods assume

| Our reality | What most published methods assume |
|---|---|
| Real **metric** objects (decimetre box known) | Single object **normalized to unit cube/sphere**, scale discarded |
| **One-sided** partial: front face + one LiDAR slice; back fully occluded against wall | Clean synthetic partials from **multiple back-projected depth views** (symmetric coverage) |
| **Appliances/counters** (fridge, oven, dishwasher) | ShapeNet cats — **chairs/tables/cabinets yes, appliances poorly represented** |
| **Known category label + oriented box** = strong priors | No exogenous conditioning — box and category are **ignored** |
| Noisy stereo + sparse LiDAR, **no reliable oriented normals** | Clean points, often with normals |

These four shifts — scale, one-sidedness, category, no-normals — are exactly what break the academic
completion/recon families on our data. The two priors we *do* have (box + category) are exactly what those
families don't accept. That mismatch drives the ranking below.

---

## 2. The four method families

### 2a. Point-cloud completion (partial → complete) — **NOT recommended here**

PCN (3DV'18, FoldingNet decoder), TopNet (CVPR'19, tree decoder), **PoinTr** (ICCV'21, geometry-aware
transformer over point proxies), **AdaPoinTr** (T-PAMI'23, + denoising queries — SOTA on PCN), SnowflakeNet
(ICCV'21, skip-transformer point growth), **SeedFormer** (ECCV'22, Patch-Seeds, 12.8 MB weights). Newer:
CRA-PCN (AAAI'24), PointSea (2025), DWCNet (2025, denoising-while-completing).

- **All trained on the PCN/ShapeNet synthetic regime:** ~31 k CAD models normalized to `[-1,1]`, **2,048-pt
  partial → 8,192/16,384-pt GT**, clean synthetic partials. They are **object-centric shape priors**.
- **Generalization to real furniture/appliances: poor and documented.** PoinTr is explicitly reported to
  "fail to complete missing parts" off-domain; the Building-PCC benchmark shows ShapeNet-trained nets
  generalize badly to real LiDAR-partial scenes. KITTI checkpoints exist but are **cars only**.
- **The box is wasted** — every one ignores an external H×W×D box; it's only usable by us for the
  normalization crop, not as conditioning.
- **Compute:** all fit our 4 GB at inference (AdaPoinTr ~30 M params; SeedFormer 12.8 MB); CPU works. Repos
  MIT ([PoinTr/AdaPoinTr](https://github.com/yuxumin/PoinTr), [SeedFormer](https://github.com/hrzhou2/seedformer)).
- **Verdict:** a **likely-negative spike.** If forced to use this family, **AdaPoinTr** (denoising queries
  best-match our stereo noise; Projected_ShapeNet checkpoint closest to real-ish partials). Treat any output
  as a *plausibility hint, not metric geometry.* The only path that genuinely fits real furniture + RGB is
  the **2D-diffusion-prior** completion (ComPC, [arxiv 2404.06814](https://arxiv.org/pdf/2404.06814)) — but
  that's Gaussian-splatting + diffusion and **won't fit 4 GB** at usable speed.

### 2b. Implicit-surface reconstruction (fit a watertight surface) — **partially useful (front only)**

| Method | Type | Prior | Invents occluded back? | Normals? | Weights |
|---|---|---|---|---|---|
| **DeepSDF** (CVPR'19) | SDF, **auto-decoder** (latent optimized at test time) | **Category** | **YES** — latent opt completes from partial (cf. MV-DeepSDF on partial sweeps) | No | MIT code, **no appliance weights** |
| ONet (CVPR'19) | Occupancy, global code | Category | Yes, but blurry/generic | No | MIT, ShapeNet |
| **ConvONet** (ECCV'20) | Occupancy, **local conv features** | **Prior-free** | **NO** — interpolates only | No | MIT, ships ShapeNet+room weights |
| **POCO** (CVPR'22) | Occupancy, point-conv | **Prior-free** | **NO** | optional | ShapeNet (verify license) |
| SAP (NeurIPS'21) | Diff. Poisson | Prior-free | NO | **requires** | MIT |
| NKSR (CVPR'23) | Neural kernel field | Prior-free | NO | wants normals | model **CC-BY-SA** |

- **The decisive split:** **prior-free local methods (ConvONet, POCO, SAP, NKSR) cannot invent the occluded
  back** — no prior to draw it from → a hole or arbitrary closure. SAP/NKSR additionally **need oriented
  normals** our one-sided noisy points can't supply. They are **excellent at densifying/denoising the
  *observed front* surface**, nothing more.
- **Only the category-prior auto-decoder completes the back:** **DeepSDF** infers a complete watertight SDF
  from partial points by test-time latent optimization (needs no normals, runs trivially on 4 GB). Cost: you
  must **train per furniture category** (no appliance weights ship anywhere) and it's brittle far from the
  training distribution.
- **Verdict:** use ConvONet/NKSR only as a **front-surface densifier**, not a completer. DeepSDF is the only
  named "completes-the-back" pick but its per-category training cost is not worth it for our prototype vs the
  template route (§2d), which gives the same back-from-prior far more cheaply.

### 2c. Single/few-image → 3D generative — **the back-hallucination prior; TripoSR is the 4 GB pick**

These invent a *plausible complete* shape from web-scale RGB priors — good at closing the unseen back of a
fridge/cabinet, but **not faithful to observed points** and **scale-free** (our box fixes scale cleanly).
**None accept an observed point cloud as conditioning** — you align/snap after generation.

| Model | In→Out | License | VRAM (4 GB?) | Note |
|---|---|---|---|---|
| **TripoSR** | image→mesh, <1 s | **MIT** | ~6 GB default, **reducible to ~4 GB / CPU** | **best 4 GB pick** — single feed-forward, most reducible |
| Hunyuan3D-2 *mini* (0.6B) | image→mesh | restricted community | ~5–6 GB (GPU-Poor fork closer) | best quality-per-VRAM, right at the edge, shape-only |
| Shap-E | text/image→SDF mesh | MIT | ~2–3 GB weights | lowest VRAM, **blobby** furniture |
| Point-E | text/image→point cloud | MIT | very light | sparse/noisy, superseded |
| SF3D, InstantMesh, TRELLIS, Stable-Zero123, Wonder3D, CRM, LRM family | — | varies | **6–24 GB+, do NOT fit 4 GB** | cloud / bigger GPU only |

- **Strength for us:** generative back-hallucination + our metric box = the scale anchor these models lack
  ([SVMR-for-robotics](https://arxiv.org/pdf/2505.17966) finds scale is exactly their weak point — which we
  supply). **Weakness:** invents proportions/handles not faithful to our points → must rigidly fit + clip to
  box + non-rigid-snap so observed geometry dominates and the model only fills the unseen back.
- **Verdict:** **TripoSR** ([repo](https://github.com/VAST-AI-Research/TripoSR), MIT) as the fallback prior
  for **irregular objects no template fits**. Measure actual VRAM at reduced marching-cubes resolution before
  committing.

### 2d. Retrieval + deformation (template → scale-to-box → fit) — **RECOMMENDED**

Lineage: Scan2CAD (CVPR'19), Mask2CAD/Patch2CAD, ROCA (CVPR'22), Vid2CAD, FastCAD (ECCV'24), and the
deform-aware thread — Uy et al. **deformation-aware retrieval** (ECCV'20) and **joint retrieval+deformation**
(CVPR'21), PatchRD (ECCV'22). **Key insight:** these networks spend their capacity estimating **pose + scale**
— *the hard, failure-prone part* — which **we already have for free** from the oriented box. So we can **skip
the trained retriever entirely**; retrieval collapses to "pick the canonical template for this category" and
deformation to "anisotropic scale-to-box + light non-rigid snap to the front face." Partial/back-occluded is
exactly the regime template methods were built for — the *template supplies the unseen geometry*.

**Asset libraries (2026 status):**

| Library | Cats | License | Free in 2026? |
|---|---|---|---|
| **ABO** (Amazon Berkeley Objects) | cabinet/chair/table + home goods | **CC BY-NC** | **YES**, public S3, no registration |
| **Google Scanned Objects** | household items | **CC BY 4.0** (most permissive) | **YES**, public |
| 3D-FUTURE | designer furniture | research ToU | gated (email) |
| ShapeNet / PartNet | all classic cats | research-only | **gated, unreliable downloads** — avoid |

Use **ABO** (curate ~10–15 canonical meshes, one per category); **GSO** as the permissive fallback. Keep
ABO's **CC BY-NC** as a productization flag. Non-rigid fit toolkit is mature: **Amberg optimal-step N-ICP**,
**ARAP**, anisotropic N-ICP (per-axis scale = our scale-to-box step).

**Appliances ≈ boxes.** For fridge/oven/dishwasher/washer/microwave/cabinet/counter a **parametric box
surface sampled across the H×W×D extent** captures essentially all recoverable geometry — parameter-free,
never fails to retrieve, no library/license needed. A retrieved template only adds cosmetic detail (handles,
panels) our partial points can't constrain anyway. **Reserve the template path for structured categories**
(chair, table, sofa, stool, shelf) where the box over-claims occupied volume (a table is a thin top + legs +
a lot of air) — there the template is what says "most of this box is empty."

---

## 3. Ranked recommendation for this use case

| Rank | Approach | Why | Effort |
|---|---|---|---|
| **1** | **Parametric box** sampled in H×W×D (box-like cats) | Captures ~all recoverable appliance geometry; no GPU, no library, never fails; uses both priors directly | **hours** (numpy; smoke-tested) |
| **2** | **Canonical template → anisotropic scale-to-box → non-rigid snap** (structured cats) | Box over-claims volume for leggy furniture; template supplies the air + unseen back from a category prior | **1–2 days** (ABO meshes + N-ICP/ARAP) |
| **3** | **TripoSR** image-to-3D prior, fit to box + points (irregular, no-template objects) | Hallucinates a plausible full shape incl. back; MIT; runs ~4 GB; box fixes its scale weakness | **~1 day** (env + per-object align) |
| 4 | DeepSDF (category auto-decoder) | Only academic method that completes the back without RGB; but needs per-category training, no appliance weights | weeks (training) — **not for prototype** |
| ✗ | Point-cloud completion (AdaPoinTr…) | ShapeNet-unit object prior, ignores box, poor real/appliance generalization | likely-negative spike |
| ✗ | Prior-free implicit (ConvONet/POCO/NKSR) | Cannot invent occluded back; SAP/NKSR need normals we lack — *front densifier only* | n/a as completer |

**Honesty rule (binding, per [[robust-evidence-mapping-principle]]):** the observed front/footprint is
*measured*; the inferred back is *prior-derived*. Emit them with that provenance flagged — never present a
hallucinated back as observed geometry.

---

## 4. Feasibility (env checked 2026-06, EDA135)

- **GPU:** RTX 3050, **4 GB VRAM** (hard constraint) — `torch 2.12+cu126`, CUDA available, in anaconda base.
  No open3d (install if needed for meshing).
- **Rank-1 (box) runs today, no GPU:** smoke-tested — sample a box surface, scale to H×W×D, snap to a
  synthetic partial in <1 s with numpy+scipy (`eda/EDA135-shape-completion-research/smoke_box_template.py`).
- **Rank-2 (template+N-ICP):** ABO downloads free today (public S3, `--no-sign-request`); ~10–15 meshes;
  N-ICP/ARAP are CPU-fine.
- **Rank-3 (TripoSR):** MIT weights on HF; ~6 GB default → reduce marching-cubes resolution or CPU-fallback
  to fit 4 GB — **measure before committing**. Hunyuan3D-2-mini GPU-Poor fork is the quality upgrade if 3050
  allows.
- **No method in any family ships pretrained weights that directly accept our (box + one-sided points +
  category) input** — every route is an *assembly* of a prior + our priors + an alignment step, not a
  one-model load. That's the headline feasibility finding.

---

## 5. Concrete first build

**Build the box-prior dense footprint (Rank 1) first**, wired to the EDA133 anchor outputs (per object:
category label + oriented H×W×D box + triangulated centroid + observed points):

1. Per object, take category + oriented box.
2. **Box-like category** → sample a dense surface across the H×W×D extent in the box's oriented frame
   (optionally a slightly recessed front face). Output the dense point cloud, flag the back as box-inferred.
3. Validate against observed front/LiDAR points (nearest-template-point residual) — already smoke-tested.
4. **Then** add Rank-2 (ABO template + anisotropic scale + light non-rigid snap) for the first *structured*
   category (table/chair) to show where the box is insufficient.

This gives a dense complete footprint for the bulk of our objects in hours, exploits both priors directly,
needs no GPU, and never fails to "retrieve." It is the robust-evidence-principle answer: build from the
reliable measured signal (footprint, box), draw the unobserved back from the strongest cheap prior, and flag
provenance. TripoSR (Rank 3) is the escalation for objects neither a box nor a template captures.

---

## Sources

Researched 2026-06 (EDA135), 4 parallel surveys. Repos/papers cited inline above. Key:
- Completion: [PoinTr/AdaPoinTr (MIT)](https://github.com/yuxumin/PoinTr), [SeedFormer](https://github.com/hrzhou2/seedformer), real/sim gap [Building-PCC](https://arxiv.org/html/2404.15644), [DWCNet 2025](https://arxiv.org/html/2507.16743v1), [ComPC 2024](https://arxiv.org/pdf/2404.06814)
- Implicit: [DeepSDF](https://arxiv.org/pdf/1901.05103), [MV-DeepSDF](https://arxiv.org/pdf/2309.16715), [ConvONet](https://github.com/autonomousvision/convolutional_occupancy_networks), [POCO](https://github.com/valeoai/POCO), [SAP](https://github.com/autonomousvision/shape_as_points), [NKSR](https://github.com/nv-tlabs/NKSR)
- Image-to-3D: [TripoSR (MIT)](https://github.com/VAST-AI-Research/TripoSR), [Shap-E](https://github.com/openai/shap-e), [Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2), [Hunyuan3D-2GP](https://github.com/deepbeepmeep/Hunyuan3D-2GP), [InstantMesh](https://github.com/TencentARC/InstantMesh), [TRELLIS](https://github.com/microsoft/TRELLIS), [SVMR-for-robotics](https://arxiv.org/pdf/2505.17966)
- Retrieval+deform: [Scan2CAD](https://github.com/skanti/Scan2CAD), [ROCA](https://openaccess.thecvf.com/content/CVPR2022/papers/Gumeli_ROCA_Robust_CAD_Model_Retrieval_and_Alignment_From_a_Single_CVPR_2022_paper.pdf), [Uy joint retrieval+deformation](https://github.com/mikacuy/joint_learning_retrieval_deformation), [FastCAD](https://arxiv.org/pdf/2403.15161), [PatchRD](https://arxiv.org/pdf/2207.11790)
- Assets: [ABO](https://registry.opendata.aws/amazon-berkeley-objects/), [Google Scanned Objects](https://research.google/blog/scanned-objects-by-google-research-a-dataset-of-3d-scanned-common-household-items/), [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl)

## Related

- [[apple-roomplan]] — production room scanner; outputs object *boxes*, not shapes (our box is the same prior)
- [[mapping-stack-design]] — where the object/shape layer sits in the world model
- [[object-fingerprint-memory]] — per-instance memory the dense shape feeds
- [[robust-evidence-mapping-principle]] — measured vs inferred provenance discipline
- [[stereo-dense-reconstruction]] · [[stereo-3d-mapping-known-poses]] — the observed-point source
- [[home-tidy-drone-prototype]] — the prototype this informs
