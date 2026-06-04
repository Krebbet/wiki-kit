# Object-Fingerprint Memory — Model & Method Choices

Concrete model + method knowledge for the per-instance **object-fingerprint memory
bank**: as objects come in, segment + cut out each one, extract a feature vector, and
store a fingerprint (object-only images, metric dimensions, embeddings, provenance,
future handling fields) so a later view can be re-identified by nearest-neighbour
search. This page firms up the high-level proposal in [[semantic-object-memory]]
§"Instance-level object fingerprinting" with specific models, sizes, licenses, and
the re-ID match design — de-risked by a runnable prototype (`drone-prototype:src/objmem/`,
`docs/object-memory-design.md`).

The distinction from [[scene-graph-world-model]]: the scene graph tracks *category +
spatial relationships*; the fingerprint bank tracks *per-instance identity + accumulated
experience*. They are complementary layers.

## Model stack (recommended)

### Segmenter — find + cut out the object

| Model | Params | Open-vocab | License | Verdict |
|---|---|---|---|---|
| **Grounding-DINO + MobileSAM** | GDINO 172M + SAM **<10M** | Yes (text→box→mask) | Apache-2.0 (SAM side) | **Primary** for enrollment-time cut-out of arbitrary household items. Enrollment is off the hot path so GDINO's ~3 fps is acceptable; MobileSAM (~10 ms/img, NanoSAM on Jetson) gives a cheap clean mask. [`mobilesam-2306.14289`][`nanosam`] |
| **YOLO11n-seg** | **2.89M** (~11 MB) | No (fixed class) | **AGPL-3.0** | **Lighter fallback** / operation-time fast path when the object set is closed (fine-tuned). Real-time on Jetson. AGPL is a commercial-licensing flag. [`yolo11`] |
| FastSAM | 68M | class-agnostic | AGPL-3.0 | 4× slower + lower quality than MobileSAM; not preferred. [`mobilesam-2306.14289`] |
| YOLO-World / open-vocab | ~50–110M | Yes | varies | Open-vocab but weak zero-shot at novel views/clutter (best aerial F1 27.6% — see [[onboard-grasp-perception]]). |
| Detectron2 Mask R-CNN | ~44M | No | Apache-2.0 | Too heavy for edge; not recommended. |

**Open-vocab vs fixed-class:** household items are arbitrary, so a fixed COCO class
set misses most. Open-vocab transfers poorly at odd viewpoints, but for a **ground
robot** at table/floor height the viewpoint gap is small, making open-vocab viable —
unlike the aerial case in [[onboard-grasp-perception]].

### Embedder — the re-identification feature vector (load-bearing)

| Model | Params | Dim | Instance-level re-ID | License | Verdict |
|---|---|---|---|---|---|
| **DINOv2 ViT-S/14** | **21M** | **384** | **Strong** | Apache-2.0 | **Primary.** Self-supervised features carry instance-level info; real-time on Orin NX. [`dinov2-card`][`same-apple`][`insdet`] |
| DINOv2 ViT-B/14 | 86M | 768 | Strongest | Apache-2.0 | If S/14 under-discriminates. |
| CLIP ViT-B/32 | ~150M | 512 | **Weaker** (category-biased) | MIT | Great at category/semantics; collapses toward class → worse at separating two same-category instances. [`same-apple`][`insdet`] |
| SigLIP-base | ~200M | 768 | category-biased | Apache-2.0 | Same caveat as CLIP. |
| OSNet / ReID nets | ~2M | 512 | strong in-domain | varies | Needs household-object training data we lack. |

**DINOv2 > CLIP for re-ID — the core finding.** Re-ID needs *instance-level*
discrimination (two red balls are different objects), not category semantics. DINOv2's
self-supervised features distinguish two instances of the same type; CLIP's text-aligned
features collapse toward the shared category. Evidence: the NeurIPS 2023 "Are These the
Same Apple?" benchmark (18k images, 180 objects, varying pose/lighting) ranks DINOv2
patch-pooling top; the InsDet benchmark shows SAM + off-the-shelf DINOv2 beating
end-to-end-trained detectors by >10 AP. [`same-apple`][`insdet`]

## Fingerprint schema (one instance)

`object_id`, `category`, multi-view object-only `image_paths`, `dimensions`
(width/height/distance metres from stereo depth + mask via pinhole; front-to-back
depth + confidence = mask depth-coverage), `embeddings` (**all** enrolled view-vectors)
+ unit-norm `embedding_mean`, `embedder_name`, `provenance` (created/last_seen ts,
n_observations, source frames), and stubbed `future` fields (material/deformable,
mass, belongs_location, name, owner, handling_policy, grasp history). Full JSON in
`drone-prototype:docs/object-memory-design.md` §3.

**Metric dimensions:** real_size = pixel_extent × median_object_depth / focal_length.
Confidence = fraction of the mask with valid stereo depth — honest about the ~48%
indoor coverage of the project's passive stereo.

## Memory bank + re-ID match flow

**Store:** sqlite (metadata) + vector index. **Index:** brute-force cosine at 100s of
objects (low-thousands of unit-norm vectors → sub-ms); **hnswlib** or FAISS for 1000s+.

**Match:** `frame → segment → crop → embed → kNN over stored view-vectors (max cosine
over all views of all objects) → best_sim ≥ threshold ? MATCH : "new"`. On a match,
fold the new view back in (extra view vector, fresher last_seen, higher-confidence
dimensions) so the record compounds with use.

**Same object, new angle/lighting:** multi-view storage + max-over-views matching is
the mechanism; DINOv2's pose/lighting robustness carries it. The prototype shows
multi-view enrollment lifting re-ID from ~67% → ~88% even with a weak classical
embedder.

**Threshold calibration:** embed labelled same/different-object pairs, set the cosine
threshold at the distribution crossover (favour precision — never merge two distinct
objects). Track the best-vs-2nd-best margin as a confidence signal; small margin →
request another view. Threshold is per-embedder.

**Clutter/occlusion:** partial masks skew embeddings + under-estimate size; gate
enrollment on min mask area + min depth-confidence, prefer clean isolated views,
down-weight low-confidence observations. Open issue.

## Prototype status (de-risking)

`drone-prototype:src/objmem/` runs the full loop end-to-end on synthetic multi-view
samples with a **classical placeholder embedder** (HSV histogram + ORB BoVW) — ~67%
single-view / ~88% multi-view re-ID, deliberately mediocre to expose why DINOv2 is
needed. DINOv2 + real segmenters are stubbed behind clean interfaces (env had
transformers 4.29 / no torchvision). Next step: real SVPRO captures + DINOv2 swap-in.

## Source

- `yolo11` — Ultralytics YOLO11 docs + Roboflow YOLO11 license page. YOLO11n-seg 2.89M params, ~11 MB, AGPL-3.0.
- `mobilesam-2306.14289` — Zhang et al., "Faster Segment Anything: Towards Lightweight SAM for Mobile Applications," arXiv:2306.14289. MobileSAM <10M params, ~10 ms/img, quality ≈ SAM; FastSAM 68M / ~40 ms.
- `nanosam` — NVIDIA NanoSAM (MobileSAM distilled for Jetson Orin + TensorRT, real-time).
- `dinov2-card` — facebookresearch/dinov2 MODEL_CARD. ViT-S/14: 21M params, 384-dim, Apache-2.0.
- `same-apple` — Sun et al., "Are These the Same Apple? Comparing Images Based on Object Intrinsics," NeurIPS 2023 Datasets & Benchmarks. DINOv2 patch-pooling top method for instance re-ID under pose/lighting; 18k images / 180 objects.
- `insdet` — Shen et al., "A High-Resolution Dataset for Instance Detection with Multi-View Instance Capture," arXiv:2310.19257. SAM + off-the-shelf DINOv2 > end-to-end InsDet by >10 AP.

## Related

[[semantic-object-memory]] — parent; high-level fingerprint proposal this page makes concrete.
[[scene-graph-world-model]] — complementary world-model layer (category + spatial relations).
[[onboard-grasp-perception]] — open-vocab detector domain-gap context; consumes fingerprints at grasp time.
[[close-range-depth-sensors]] — depth sensors; transparent/specular surfaces break the metric-dimension estimate.
[[system-architecture]] — WORLD MAP (dynamic-object-memory datastore) + M1 PERCEPTION PIPELINE this populates.
