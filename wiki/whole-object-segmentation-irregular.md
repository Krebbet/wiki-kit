# Whole-Object Segmentation of Irregular, Multi-Part Objects — SAM Prompting, Depth Membership, Part-to-Whole Grouping

How to get **one mask covering the whole object** — not its head, not its skirt — when the object is irregular,
multi-coloured and multi-material (a plush toy lying on its side, a bag, a heap of cloth), and the robot already
knows **where the object is in 3-D** from its LiDAR. Written for the drone-prototype discovery routine
(2026-10-06): MobileSAM prompted by a projected 3-D extent box + a few projected LiDAR chord points segments
compact objects (spray can, bottle) well but returns a **part** of the Minnie Mouse plush, and Grounding DINO
splits the same plush into "ball", "shoe", "bag" (drone-prototype `eda/EDA249-look-compare/FINDING.md`, diary
2026-10-06). The page answers: what SAM's prompt interface actually allows and how it behaves on multi-part
objects; how 3-D geometry (LiDAR footprint, stereo depth) can decide *membership* while SAM decides *edges*;
which part-to-whole and multi-view methods exist; which open-vocabulary detectors/segmenters handle long-tail
"stuffed toy"-like objects and at what cost; and what is specific to deformable household objects.

> **Read alongside:** [[point-cloud-object-segmentation-models]] (room-level object *proposals*; the SAM-lift
> family in 3-D), [[ov3d-instance-seg]] (open-vocab 3-D instance seg compute envelope),
> [[object-fingerprint-memory]] (GDINO + MobileSAM as the enrolment cut-out — this page is the fix for its
> failure on multi-part objects), [[3d-shape-completion-for-object-footprints]] (what to do with the mask
> afterwards), [[language-3d-scene-representations]] (Gaussian/NeRF grouping methods),
> [[robust-evidence-mapping-principle]] (membership by agreement of independent evidence).

**Status labels used below:** *(published)* = stated in a paper/repo, not reproduced here; *(demoed-here)* =
measured on this rover; *(synthesis)* = this page's own combination of published pieces; *(speculative)* =
plausible, untested anywhere we know of.

---

## TL;DR

1. **SAM is behaving as designed, and part of the miss is our call pattern.** SAM's three multimask outputs
   are trained for *single-click* ambiguity (whole / part / subpart); with more than one prompt SAM was trained
   to emit **one** unambiguous mask, and the official notebook says multimask is "intended for ambiguous input
   prompts" while "when specifying a single object with multiple prompts, a single mask can be requested by
   setting `multimask_output=False`" [src: sam; sam-nb]. Our `wholeseg.py` asks for 3 masks with a box + 12 positives + 8 negatives, i.e.
   reads the tokens SAM never trained for that case. MobileSAM shares SAM's prompt encoder and mask decoder, so
   all of this transfers [src: mobilesam]. *(published; the consequence for our code is synthesis)*
2. **More points is not monotonically better.** Gains flatten and can **decline** past ~10–20 points (medical
   study; domain caveat) [src: sam-brats]; spread points (max-distance / max-entropy sampling) beat clustered
   ones [src: samaug]. A box + 5–10 spread positives + floor negatives, then **1–2 rounds of mask-input
   refinement** (feeding the previous low-res logits back, which is how SAM was trained interactively)
   [src: sam] is the best-practice single call. *(published)*
3. **The real lever is to let geometry decide membership and SAM decide edges.** A multi-colour plush is one
   object in 3-D (contiguous, above the floor, inside the measured footprint) even when it is five objects in
   colour. Every unseen-object instance segmentation (UOIS) line that works on novel clutter leans on depth for
   *which pixels belong together* and RGB for *where the boundary is*: UOIS-Net (depth-only initial masks,
   RGB refinement) [src: uoisnet; uoisnet3d], UCN / MSMFormer (RGB-D embeddings + mean-shift)
   [src: ucn; msmformer], ZISVFM (SAM on **colourised depth** for object-agnostic proposals) [src: zisvfm].
   *(published)*
4. **Part-to-whole grouping is a solved pattern when geometry is available**: over-segment with SAM's
   automatic mode, then merge parts by 3-D evidence — SAM3D / SAI3D / Open3DIS / SAMPro3D merge 2-D masks via
   3-D projection, MaskClustering merges masks that **other views see together** (view-consensus rate)
   [src: sam3d; sai3d; open3dis; sampro3d; maskclustering]. Pure-2-D part→whole (Semantic-SAM granularity
   levels) helps but has no notion of "this is one physical object" [src: semsam]. *(published)*
5. **Detectors are the wrong tool for the mask.** Open-vocab detectors box what they can name; a plush on its
   side is a long-tail pose of a long-tail class, so part-level boxes ("ball", "shoe") are expected, and
   Grounded-SAM inherits them [src: gsam; gdino]. Use detectors (or Claude) to **name a crop**, not to
   **delimit** it. SAM 3 (concept prompts, "stuffed toy" → all instances) is the one model aimed squarely at
   this, but it is 848 M params / ~3.4 GB [src: sam3; sam3-size] — too heavy for the laptop's current disk/RAM.
6. **Recommendation:** fix the prompt call (R0, an hour), add a **stereo-depth membership mask** inside the
   LiDAR footprint prism and use it to select/merge SAM part masks (R1, one EDA), then **carve across stations**
   so masks from 3–5 views must agree on one 3-D object (R2). Models later. Details at the end.

---

## 1. What SAM-family models accept, and how they behave on multi-part objects

### 1.1 The prompt interface (SAM, MobileSAM, EfficientSAM, SAM-HQ, SAM 2 image mode)

| Prompt / knob | What it is | Notes for whole objects |
|---|---|---|
| **Points** (`point_coords`, `point_labels` 1/0) | positive / negative clicks | Single click → ambiguous by design → 3 masks. Negatives are the cheapest way to cut floor/background leakage [src: sam] |
| **Box** (`box`, xyxy) | one box per call in `SamPredictor` (batched boxes via `predict_torch`) | SAM does notably better with a box than with points alone [src: sam-brats]. A box larger than the object invites "biggest salient thing in the box" |
| **Mask input** (`mask_input`, 1×256×256 **logits**) | a previous low-res mask fed back as a dense prompt | SAM's interactive training sampled new points from the error region and fed the previous logits back for up to 11 iterations [src: sam]. It is *not* designed for arbitrary binary masks — pass the logits SAM itself returned, or a soft logit map, not a 0/1 image (the notebook only documents passing back SAM's own `low_res_logits`) |
| **`multimask_output`** | 3 masks (tokens 1–3) vs 1 mask (token 0) | Three masks because "whole, part, subpart" usually suffice for nested single-click ambiguity; **with >1 prompt SAM trained only the single-mask output**, because ambiguity is rare with multiple prompts [src: sam]. Notebook: multimask is "intended for ambiguous input prompts"; for one object with multiple prompts "a single mask can be requested" with `False`, and returned low-res logits "can be passed to the next iteration" [src: sam-nb] |
| **Predicted IoU / stability score** | the model's self-score per mask | Ranks masks by *SAM's* confidence — on a multi-part object the confident mask is often the most uniform-coloured part. Rank by our own geometric evidence instead (§2) |
| **Automatic mask generator** | grid of points (`points_per_side`), filtered by `pred_iou_thresh`, `stability_score_thresh`, NMS, optional crop layers, `min_mask_region_area` [src: sam-repo] | Over-segments on purpose — the right **input** to a part-to-whole merge (§3) |

Model-specific deltas:

- **MobileSAM** — distils SAM's ViT-H image encoder into a ~5 M TinyViT and *keeps SAM's prompt encoder and mask
  decoder* [src: mobilesam]. Prompt semantics and ambiguity behaviour are SAM's; encoder quality on fine/low-
  contrast boundaries is lower (authors' comparisons are mostly qualitative). *(published)*
- **EfficientSAM** — ViT-Tiny/Small encoders pretrained with masked-image SAM-feature reconstruction (SAMI);
  same promptable interface, better than MobileSAM at similar size on the authors' benchmarks [src: effsam].
- **SAM-HQ** — adds a high-quality output token + global-local feature fusion; targets thin structures and
  fine boundaries; a Light HQ-SAM variant on TinyViT exists [src: samhq]. It improves *edges*, not
  *part-vs-whole choice*. *(published)*
- **SAM 2 / 2.1** — image mode has the same prompt types; video mode adds a memory bank so a prompt on one
  frame **propagates** to later frames [src: sam2]. Tiny (~39 M) to Large (~224 M) checkpoints in the repo
  [src: sam2-repo]. A station's tilt sequence is a short video of a static object: one good whole-object
  prompt could propagate through the other tilts. *(speculative for our use; published mechanism)*
- **Semantic-SAM** — trained jointly on SA-1B + object + part datasets with a multi-choice loss, so **one click
  returns masks at several granularities** (repo: up to 6) with semantic labels for object vs part
  [src: semsam]. The closest thing to an explicit "give me the object level" knob. *(published)*
- **SAM 3** — concept prompts (noun phrase and/or image exemplar) → masks + identities for **all** matching
  instances; presence head decouples recognition from localisation; ~2× prior systems on the SA-Co benchmark
  [src: sam3]. 848 M params, ~3.4 GB checkpoint, 16 GB VRAM recommended by third-party install guides
  [src: sam3-size]. *(published; size from secondary sources)*

### 1.2 Why a multi-part object returns a part *(published mechanism + synthesis)*

- SAM's training data (SA-1B) annotates masks at **every** granularity; the model learnt that a click on a
  red skirt plausibly means "the skirt" [src: sam]. A plush with high-contrast colour regions and seams is
  exactly the input where part masks are the high-confidence answer.
- Points placed by **LiDAR chords** lie along one or two horizontal lines at fixed heights; when those lines
  cross one part (the head at chord height), the positives all say "this part". Spread, not count, is what
  disambiguates [src: samaug].
- Asking for 3 masks with many prompts reads untrained tokens (§1.1), so the "whole" slot is not reliably the
  whole object. *(synthesis from [src: sam])*
- Ranking by SAM's IoU score favours the most self-consistent region — usually a uniformly coloured part.

### 1.3 Best practice for one SAM call on a known-location object *(published pieces; combination = synthesis)*

1. **Box = tight projected extent**, not inflated; inflation invites the floor/background.
2. **5–10 positives, spread** over the *object's area* (farthest-point sampled over a membership mask, §2) —
   not along one chord line [src: samaug; sam-brats].
3. **Negatives on the floor ring** just outside the footprint and on any adjacent object; never inside the
   footprint prism.
4. `multimask_output=False` when giving box + several points [src: sam-nb].
5. **Iterate 1–2×**: pass the returned low-res logits as `mask_input`, add a positive at the largest
   *missed-object* region (inside membership mask, outside current mask) and a negative at the largest
   *leak* region — the training-time loop [src: sam].
6. **Score candidates by external evidence** (coverage of the membership mask, leakage outside the footprint
   prism), never by SAM's IoU head. This is already the logic of drone-prototype `src/drone/discover/wholeseg.py`
   *(demoed-here as code; result on plush pending)*.
7. Alternative when one call cannot get the whole: **union of per-part calls** (one point cluster per part,
   single-click multimask, pick the level that stays inside the prism) — also already in `wholeseg.py`.

---

## 2. Geometry decides membership: depth/LiDAR-derived object masks

### 2.1 What the robot already knows *(demoed-here)*

Per object: LiDAR chord points on the near face at known heights (several tilts, several stations), a
measured footprint (plush1: 30–33 × 14–23 cm, height 14.6 cm), the floor plane (rover scan-plane height and
tilt calibration, [[tilting-2d-lidar-multiplane-capture]]), and calibrated stereo per frame with the
camera↔LiDAR extrinsic. `wholeseg.py` already turns this into a **MUST zone** (projected chord points) and a
**MAY zone** (footprint cells extruded floor→top, projected, closed).

### 2.2 Classical geometric grouping *(published, decades old)*

- **Ground-plane removal → Euclidean clustering → project to image** is the standard tabletop/floor
  pipeline (PCL Euclidean cluster extraction after RANSAC plane removal [src: pcl-cluster]; Rusu et al.'s
  domestic mobile-manipulation segmentation [src: rusu2009]). An object on the floor is "everything above
  the plane, connected in 3-D, within the footprint". It is colour-blind — exactly the property a
  multi-colour plush needs.
- **Depth-discontinuity / organised connected components** (Trevor et al.) segment organised depth images
  into planes and clusters in real time by comparing neighbouring pixels' 3-D distance/normal
  [src: trevor2013]. Same membership-by-continuity idea, works on a per-frame depth image.
- **Visual hull / space carving** (Laurentini) — the object is the intersection of the back-projected
  silhouettes from several views [src: laurentini]. With known station poses, masks from 3–5 stations carve a
  hull; any frame's part-only mask is then corrected by re-projecting the hull. See §3.3.

### 2.3 Unseen-object instance segmentation (UOIS): learned RGB-D whole-object masks *(published)*

| Method | Mechanism | Relevance to a floor object with a known footprint |
|---|---|---|
| **UOIS-Net / UOIS-Net-3D** [src: uoisnet; uoisnet3d] | Stage 1 on **depth only** (3-D centre voting) → rough object masks; stage 2 refines with RGB. Trained on synthetic tabletop scenes | The "depth for membership, RGB for edges" split, published. Tabletop, top-down-ish viewpoint; our low oblique view is out of domain |
| **UCN** [src: ucn] | Per-pixel RGB-D embeddings (metric loss) + von Mises–Fisher mean-shift; discovers object count | Embedding pulls multi-colour parts together if they are geometrically contiguous — the property we need. Repo released (IRVLUTD) |
| **MSMFormer** [src: msmformer] | Mean-shift as a differentiable transformer (hypersphere attention), RGB-D | Same family, end-to-end; competitive with UCN |
| **UOAIS-Net** [src: uoais] | Amodal (visible + occluded) masks, RGB-D | Occlusion-aware; useful when another object overlaps |
| **ZISVFM** [src: zisvfm] | SAM on **colourised depth** → object-agnostic proposals; self-supervised ViT attention filters non-objects; K-medoids → point prompts → SAM on RGB | Training-free; the cleanest recipe for "use depth to propose, SAM to cut" |
| **Depth-NOCTIS** (BMVC 2025 workshop) [src: noctis] | Grounded-SAM-2 proposals + DINOv2 + geometric-consistency score from depth | Depth used as a *consistency check* on proposals |

Caveats *(synthesis)*: all are evaluated on tabletop clutter (OCID/OSD-style) with active depth; passive
stereo on our rig has holes on textureless surfaces ([[passive-stereo-robustification]]), and an object lying
*on* the floor has a contact band where "above the plane" is within depth noise. The footprint prism from
LiDAR bounds both problems: holes inside the prism are filled by the prism; the contact band is decided by
SAM's edge.

### 2.4 Combining depth membership with SAM *(synthesis; each step published)*

```
footprint prism (LiDAR, multi-station)  ─┐
stereo depth (this frame) ──► 3-D pts ──► keep: above floor + h_min, inside prism ──► G  (geometric mask)
                                                                                     │
SAM automatic masks inside the box ──► parts {p_i} ──► accept p_i if |p_i ∩ G| / |p_i| ≥ τ (and p_i ⊂ MAY)
                                                                                     │
whole = ∪ accepted p_i  (∪ G-holes bridged by morphology)  ∩ MAY ──► optionally re-prompt SAM with
        spread positives over `whole` + mask_input = logits of the best single-call mask
```

This is the ZISVFM/UOIS split rearranged around the measurements we already have: G answers "is this pixel
object?" independent of colour, SAM answers "where exactly is the boundary?". The same grouping works with
LiDAR-only evidence (MUST zone instead of G) when stereo depth fails, at lower coverage.

---

## 3. Part-to-whole grouping and multi-view consistency *(published)*

### 3.1 Merging 2-D parts by 3-D evidence

- **SAM3D** — lifts per-frame SAM masks to 3-D and merges across adjacent frames bottom-up; training-free
  [src: sam3d].
- **SAI3D** — superpoints in 3-D + SAM masks across views as affinity, then region growing; explicitly about
  merging SAM's over-segmentation into instances [src: sai3d].
- **Open3DIS** — 2-D-guided 3-D proposals: 2-D masks lifted and merged with 3-D superpoint proposals
  [src: open3dis].
- **SAMPro3D** — places prompts in 3-D and projects them into every frame, so all frames segment the *same*
  physical thing; filters/merges by cross-view consistency [src: sampro3d].
- **MaskClustering** — a graph over all 2-D masks; two masks belong to one instance if a large share of
  *other* views contain both (view-consensus rate); iterative clustering; training-free, SOTA on
  ScanNet++/ScanNet200/Matterport at publication [src: maskclustering]. For a plush: the head mask in
  station 1 and the skirt mask in station 2 merge if station 3's view contains both inside one mask.
- **Gaussian Grouping** — per-Gaussian identity features supervised by SAM masks associated across views;
  the grouping is 3-D-consistent by construction [src: gaussgroup]. Heavy (3DGS training); see
  [[language-3d-scene-representations]].
- **PartSLIP** — the inverse direction: GLIP part detections on multi-view renders fused into a 3-D part
  segmentation [src: partslip]. Shows that part labels from 2-D detectors are view-dependent and need
  multi-view voting — the same reason GDINO's "ball/shoe/bag" should be read as parts, not objects.

All assume dense posed RGB-D sequences; we have a few stations with known poses, which is enough for the
**voting** idea but not for the dense-reconstruction parts of these pipelines *(synthesis)*.

### 3.2 Pure-2-D granularity control

Semantic-SAM's multi-granularity click is the 2-D alternative: ask for the coarsest level whose mask stays
inside the footprint prism [src: semsam]. Not demoed on lying plush; its object/part labels come from
COCO/PASCAL-Part/PACO-style data, i.e. mostly rigid everyday objects and people/animals.

### 3.3 Carving across stations *(synthesis; mechanism = visual hull [src: laurentini])*

Back-project each station's chosen mask into the footprint grid (or a 1 cm voxel prism above it); keep cells
that are inside the silhouette in ≥ k of the stations that see them. Project the carved volume back into
every frame → a **consensus whole-object mask** per frame. A station whose SAM mask covered only the head
is outvoted by stations whose masks covered the whole; a station whose mask leaked onto the floor is clipped
by the others. This is also an honest *check*: if no consistent hull exists, the masks disagree about what
the object is, and that should be reported rather than averaged ([[robust-evidence-mapping-principle]]).

---

## 4. Open-vocabulary detection + segmentation for long-tail objects

| Model | What it does | Parts vs wholes | Cost (laptop) |
|---|---|---|---|
| **Grounding DINO** (T: ~172 M) [src: gdino] | text → boxes | Boxes what matches the phrase; for an unusual pose of a long-tail class, parts that look like other nouns win ("ball", "shoe") *(demoed-here, EDA249)* | GPU ok; ~3 fps class on edge (see [[object-fingerprint-memory]]) |
| **Grounded-SAM / Grounded-SAM-2** [src: gsam; gsam2] | GDINO (or Florence-2) boxes → SAM/SAM 2 masks (+ tracking) | Inherits the detector's box granularity — a part box gives a part mask | GDINO + SAM2-tiny fits the GPU |
| **OWLv2** [src: owlv2] | open-vocab detection, self-trained on web-scale pseudo-boxes; image-exemplar queries | Strong on rare classes in LVIS; image-conditioned query ("find things like this crop") is useful for re-ID | ViT-B/16 ~150 M; GPU ok |
| **YOLO-World** [src: yoloworld] / **YOLOE** [src: yoloe] | real-time open-vocab detection; YOLOE adds instance seg, visual prompts and a prompt-free mode | Same part/whole behaviour as other detectors; YOLOE-S +3.5 AP over YOLO-Worldv2-S on LVIS | Small (S/M) models; fastest option |
| **Florence-2** (0.23 B / 0.77 B) [src: florence2] | unified seq2seq: caption, OD, phrase grounding, referring-expression segmentation (polygon) | Can be asked for a caption of the crop and a referring segmentation of it; polygon masks are coarse | Base fits easily |
| **SAM 3** [src: sam3] | concept prompt → all instances, masks + IDs, image + video | Trained on 4 M concept labels with hard negatives; the most likely to return "the stuffed toy" as one instance | 848 M / ~3.4 GB [src: sam3-size] — disk-blocked now |
| **VLM (Claude) on crops** | describe / name a crop | Names wholes well when the crop *is* the whole — so it needs the mask first *(demoed-here, EDA249: in-session describing)* | API |

Take-away *(synthesis)*: on this rover the detector's job is **naming and patrol proposals**, cross-checked by
LiDAR; the **extent** comes from geometry + SAM. EDA249's false "stuffed toy" in 7/8 plush-free frames is a
reminder that detector confidence on long-tail classes is not evidence of presence.

---

## 5. Deformable / soft household objects *(published, thin)*

- Most robot deformable-object perception is **cloth-specific** and segments *regions* for grasping (edges,
  corners) rather than whole-object identity, e.g. cloth-region segmentation for grasp selection
  [src: clothregion].
- Recent garment pipelines simply use **Grounded-SAM-2 for the mask + a learned stereo network
  (FoundationStereo) for depth** to build the garment point cloud [src: kit-garment] — i.e. the field's
  current answer is "foundation segmenter + good depth", the same split as §2.
- Plush toys specifically: no robot-perception work found that treats them as a class; they behave like
  articulated multi-part objects (distinct coloured parts, soft seams) in 2-D and like a single blob in 3-D —
  which is why the geometric membership route (§2) is the right primary *(synthesis)*.
- Shape/description downstream: SAM 3D Objects reconstructs a full textured mesh from one masked image
  [src: sam3d-objects] — a candidate for [[3d-shape-completion-for-object-footprints]]'s Rank-3 slot for
  irregular objects, **given a correct whole-object mask**. Per the diary, irregular/deformable objects
  should store a data-driven footprint (per-band hull / height grid) rather than a parametric outline.

---

## Recommendation for this rover

Ranked by effort → payoff. Every step reports its numbers per frame and per station (must-coverage, leakage,
cross-station agreement) so a failure is visible, per the project's honest-validation rule.

| # | Step | Effort | Expected payoff | Status |
|---|---|---|---|---|
| **R0** | **Fix the SAM call in `wholeseg.py`.** (a) Box + many points → `multimask_output=False` [src: sam; sam-nb]. (b) Cap positives at ~6–10, spread by FPS over the MAY∩(evidence) area, not along chord lines [src: samaug; sam-brats]. (c) Tight box = projected extent, not MAY bounds + margin. (d) Add 1–2 refinement rounds with `mask_input` = previous logits + a positive in the largest missed region + a negative in the largest leak [src: sam]. Keep the existing candidate scoring by coverage/leakage | ~1 h | Likely fixes part of the plush miss; zero new dependencies | published mechanism; untested here |
| **R1** | **Stereo-depth membership mask G** per frame: stereo points above floor + ~1.5 cm and inside the LiDAR footprint prism (+ margin). Use G (i) as a dense MUST zone (replaces sparse chords), (ii) as the area to spread prompts over, (iii) to **accept SAM automatic-mode parts** with ≥ τ of their pixels in G and union them (§2.4) | 1 EDA | The core fix for multi-colour objects: membership no longer depends on colour | synthesis of UOIS-Net / ZISVFM pattern; untested here |
| **R2** | **Carve across stations** (§3.3): back-project each station's mask into the footprint voxel prism, keep cells inside ≥ k silhouettes, re-project to correct each frame; report disagreement | 1 EDA | Turns 3–5 noisy masks into one consistent object; gives a data-driven footprint/hull for the record | visual hull (published); untested here |
| **R3** | **Drop-in model swaps** to test behind the same scorer: SAM-HQ-light (edges), EfficientSAM-S, SAM 2.1-tiny image mode (and video mode across a station's tilt sequence), Semantic-SAM "coarsest level inside prism" | ½ day each | Marginal unless R0–R2 still leave parts; check disk first | published models |
| **R4** | **ZISVFM-style proposals** (SAM on colourised stereo depth) when R1's G is too holey | 1 EDA | Depth-driven proposals independent of texture | published, training-free |
| **R5** | Learned UOIS (UCN/MSMFormer, released code) — only if R1–R2 fail; out-of-domain viewpoint and passive depth | 2+ EDAs | Unknown | published, domain risk |
| — | **Not now:** SAM 3 (disk/RAM), 3DGS grouping (Gaussian Grouping), dense 3-D lifting stacks (SAI3D/Open3DIS/MaskClustering at full scale). Detectors stay for naming/patrol, never for extent | — | — | — |

Measurement plan for R0–R2 *(synthesis)*: on the plush1 frames and the earlier spray/bottle runs, report per
frame (must-coverage, leakage outside MAY, area) for the current call vs R0 vs R1, and per object the
cross-station IoU of re-projected masks. The compact objects are the regression guard: R0–R2 must not worsen
them.

---

## Source

Primary (arXiv / repos):
- [src: sam] Kirillov et al., "Segment Anything," ICCV 2023, arXiv:2304.02643 — 3 masks for whole/part/subpart; IoU head; single-mask output trained when >1 prompt; interactive training with mask-logit feedback.
- [src: sam-nb] facebookresearch/segment-anything, `notebooks/predictor_example.ipynb` — multimask for single point; `multimask_output=False` for multiple points / box+point; `mask_input` from previous logits. https://github.com/facebookresearch/segment-anything/blob/main/notebooks/predictor_example.ipynb
- [src: sam-repo] facebookresearch/segment-anything, `SamAutomaticMaskGenerator` parameters. https://github.com/facebookresearch/segment-anything
- [src: mobilesam] Zhang et al., "Faster Segment Anything: Towards Lightweight SAM for Mobile Applications," arXiv:2306.14289.
- [src: effsam] Xiong et al., "EfficientSAM: Leveraged Masked Image Pretraining for Efficient Segment Anything," arXiv:2312.00863.
- [src: samhq] Ke et al., "Segment Anything in High Quality," NeurIPS 2023, arXiv:2306.01567.
- [src: sam2] Ravi et al., "SAM 2: Segment Anything in Images and Videos," arXiv:2408.00714. [src: sam2-repo] https://github.com/facebookresearch/sam2 (checkpoint sizes).
- [src: sam3] Carion et al., "SAM 3: Segment Anything with Concepts," ICLR 2026, arXiv:2511.16719. [src: sam3-size] third-party install guides (848 M params, ~3.4 GB): https://codersera.com/blog/how-to-run-sam-3-locally-2026/ — secondary.
- [src: sam3d-objects] SAM 3D Team, "SAM 3D: 3Dfy Anything in Images," CVPR 2026, arXiv:2511.16624.
- [src: semsam] Li et al., "Semantic-SAM: Segment and Recognize Anything at Any Granularity," ECCV 2024, arXiv:2307.04767.
- [src: sam-brats] "Segment Anything Model for Brain Tumor Segmentation," arXiv:2309.08434 — box ≫ points; 20–30 points decline vs fewer (medical domain).
- [src: samaug] Dai et al., "SAMAug: Point Prompt Augmentation for Segment Anything Model," arXiv:2307.01187 — spread (max-distance / max-entropy) point sampling.
- [src: uoisnet] Xie et al., "The Best of Both Modes: Separately Leveraging RGB and Depth for Unseen Object Instance Segmentation," CoRL 2019, arXiv:1907.13236.
- [src: uoisnet3d] Xie et al., "Unseen Object Instance Segmentation for Robotic Environments," T-RO 2021, arXiv:2007.08073.
- [src: ucn] Xiang et al., "Learning RGB-D Feature Embeddings for Unseen Object Instance Segmentation," CoRL 2020, arXiv:2007.15157; code https://github.com/IRVLUTD/UnseenObjectClustering
- [src: msmformer] Lu et al., "Mean Shift Mask Transformer for Unseen Object Instance Segmentation," arXiv:2211.11679; https://irvlutd.github.io/MSMFormer
- [src: uoais] Back et al., "Unseen Object Amodal Instance Segmentation via Hierarchical Occlusion Modeling," ICRA 2022, arXiv:2109.11103.
- [src: zisvfm] "ZISVFM: Zero-Shot Object Instance Segmentation in Indoor Robotic Environments with Vision Foundation Models," arXiv:2502.03266.
- [src: noctis] Depth-NOCTIS, BMVC 2025 DIFA workshop. https://bmva-archive.org.uk/bmvc/2025/assets/workshops/DIFA/Paper_5/paper.pdf
- [src: pcl-cluster] PCL tutorial, Euclidean Cluster Extraction. https://pcl.readthedocs.io/projects/tutorials/en/latest/cluster_extraction.html
- [src: rusu2009] Rusu et al., "Close-range Scene Segmentation and Reconstruction of 3D Point Cloud Maps for Mobile Manipulation in Domestic Environments," IROS 2009.
- [src: trevor2013] Trevor et al., "Efficient Organized Point Cloud Segmentation with Connected Components," SPME workshop (ICRA) 2013.
- [src: laurentini] Laurentini, "The Visual Hull Concept for Silhouette-Based Image Understanding," IEEE TPAMI 16(2), 1994.
- [src: sam3d] Yang et al., "SAM3D: Segment Anything in 3D Scenes," arXiv:2306.03908.
- [src: sai3d] Yin et al., "SAI3D: Segment Any Instance in 3D Scenes," CVPR 2024, arXiv:2312.11557.
- [src: open3dis] Nguyen et al., "Open3DIS: Open-Vocabulary 3D Instance Segmentation with 2D Mask Guidance," CVPR 2024, arXiv:2312.10671.
- [src: sampro3d] Xu et al., "SAMPro3D: Locating SAM Prompts in 3D for Zero-Shot 3D Instance Segmentation," arXiv:2311.17707.
- [src: maskclustering] Yan et al., "MaskClustering: View Consensus based Mask Graph Clustering for Open-Vocabulary 3D Instance Segmentation," CVPR 2024, arXiv:2401.07745.
- [src: gaussgroup] Ye et al., "Gaussian Grouping: Segment and Edit Anything in 3D Scenes," ECCV 2024, arXiv:2312.00732.
- [src: partslip] Liu et al., "PartSLIP: Low-Shot Part Segmentation for 3D Point Clouds via Pretrained Image-Language Models," CVPR 2023, arXiv:2212.01558.
- [src: gdino] Liu et al., "Grounding DINO," arXiv:2303.05499. [src: gsam] Ren et al., "Grounded SAM," arXiv:2401.14159. [src: gsam2] https://github.com/IDEA-Research/Grounded-SAM-2
- [src: owlv2] Minderer et al., "Scaling Open-Vocabulary Object Detection," NeurIPS 2023, arXiv:2306.09683.
- [src: yoloworld] Cheng et al., "YOLO-World," CVPR 2024, arXiv:2401.17270. [src: yoloe] Wang et al., "YOLOE: Real-Time Seeing Anything," arXiv:2503.07465.
- [src: florence2] Xiao et al., "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks," CVPR 2024, arXiv:2311.06242.
- [src: clothregion] Qian et al., "Cloth Region Segmentation for Robust Grasp Selection," IROS 2020. https://www.ri.cmu.edu/publications/cloth-region-segmentation-for-robust-grasp-selection
- [src: kit-garment] Hohensee et al. 2026 (KIT H2T), garment perception with FoundationStereo + Grounded SAM 2. https://h2t.iar.kit.edu/pdf/Hohensee2026.pdf

Internal (drone-prototype): `docs/prototype-diary.md` 2026-10-06 (plush1 / obj-0003), `eda/EDA249-look-compare/FINDING.md`
(detector vs Claude; plush split into ball/shoe/bag), `src/drone/discover/wholeseg.py` (MUST/MAY zones, box+points
and parts-union candidates, coverage/leakage scoring).

*Researched 2026-10-06 (dispatched research, web search + reading; no models run). Numbers are as published; none
reproduced on the rover.*

## Related

[[point-cloud-object-segmentation-models]] · [[ov3d-instance-seg]] · [[object-fingerprint-memory]] ·
[[semantic-object-memory]] · [[3d-shape-completion-for-object-footprints]] · [[language-3d-scene-representations]] ·
[[tilting-2d-lidar-multiplane-capture]] · [[passive-stereo-robustification]] · [[locate-object-from-last-known-position]] ·
[[robust-evidence-mapping-principle]]
