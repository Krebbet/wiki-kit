# Open-Vocabulary 3D Instance Segmentation — 3D-Native Methods and Compute Feasibility

Open-vocabulary 3D instance segmentation (OV-3DIS) takes a 3D point cloud (or RGB-D sequence used to build one) and segments individual object instances using arbitrary text queries — no fixed class vocabulary. This page covers the **3D-native pipeline family**: OpenMask3D, Open3DIS, Open-YOLO 3D, FOLK, OV-MAP, and the Mask3D backbone, focusing on (1) GPU/VRAM envelope and robot-hardware feasibility, (2) accuracy vs the 2D GDINO+SAM+depth-projection approach, (3) failure modes on sparse depth, and (4) deployment status.

The wiki already covers ConceptGraphs/Hydra/DovSG/HOV-SG ([[scene-graph-world-model]]) and the 2D GDINO+MobileSAM pipeline ([[object-fingerprint-memory]]). This page complements those with the 3D-native branch and its compute trade-offs.

## Source

- `raw/research/ov3d-instance-seg/01-openmask3d.md` — Takmaz et al., "OpenMask3D: Open-Vocabulary 3D Instance Segmentation," NeurIPS 2023. arXiv:2306.13631.
- `raw/research/ov3d-instance-seg/02-open-yolo3d.md` — Boudjoghra et al., "Open-YOLO 3D: Towards Fast and Accurate Open-Vocabulary 3D Instance Segmentation," ICLR 2025 (Oral). arXiv:2406.02548.
- `raw/research/ov3d-instance-seg/03-open3dis.md` — Nguyen et al., "Open3DIS: Open-Vocabulary 3D Instance Segmentation with 2D Mask Guidance," CVPR 2024. arXiv:2312.10671.
- `raw/research/ov3d-instance-seg/04-folk.md` — Wu et al., "FOLK: Fast Open-Vocabulary 3D Instance Segmentation via Label-guided Knowledge Distillation," arXiv:2510.08849, 2025.
- `raw/research/ov3d-instance-seg/05-ov-map.md` — Kim et al., "OV-MAP: Open-Vocabulary Zero-Shot 3D Instance Segmentation Map for Robots," arXiv:2506.11585, 2025.
- `raw/research/ov3d-instance-seg/06-edge-ov-bench.md` — Park et al., "Real-time open-vocabulary perception for mobile robots on edge devices: a systematic analysis of the accuracy-latency trade-off," *Frontiers in Robotics and AI*, 2025. PMC12583037.
- `raw/research/ov3d-instance-seg/07-openmask3d-github.md` — OpenMask3D GitHub README (OPTIMIZE_GPU_USAGE flag).
- `raw/research/ov3d-instance-seg/08-mask3d.md` — Schult et al., "Mask3D: Mask Transformer for 3D Semantic Instance Segmentation," ICRA 2023. arXiv:2210.03105.

## Related

[[scene-graph-world-model]], [[object-fingerprint-memory]], [[world-model-architecture]], [[mapping-stack-design]], [[onboard-grasp-perception]], [[close-range-depth-sensors]], [[semantic-object-memory]], [[system-architecture]]

---

## Method taxonomy

*(synthesis)* Two pipeline architectures have emerged in this field:

**3D-proposal-then-embed:** Generate class-agnostic 3D masks using a 3D network (Mask3D backbone), then classify each mask by projecting it back into 2D RGB frames and extracting CLIP features per mask. Used by OpenMask3D, Open-YOLO 3D, FOLK.

**2D-guided 3D proposals + embed:** Additionally generate 3D proposals from 2D instance segmentation results (SAM masks projected into 3D point cloud) and fuse them with 3D network proposals. Used by Open3DIS. More accurate on small/ambiguous objects; pays a heavy SAM compute cost.

Both families require: a pre-built 3D point cloud (from SfM/TSDF/live reconstruction), camera poses and intrinsics, and RGB-D image frames associated with the reconstruction. They are **offline-batch** methods tested on ScanNet200 scene recordings — not online streaming systems.

---

## Mask3D — the backbone (closed-vocabulary, used by all)

[src: mask3d]

Mask3D is a closed-vocabulary 3D instance segmentation Transformer (ICRA 2023). It takes a voxelized point cloud through a sparse convolutional backbone (MinkowskiUNet) and a transformer decoder that iteratively refines instance queries to predict binary masks. Results on ScanNet200: AP 26.9 / AP50 36.2 / AP25 41.4. Inference time per scene: ~13.4 s on a single GPU.

OpenMask3D, Open-YOLO 3D, FOLK, and Open3DIS all use Mask3D as the class-agnostic proposal stage — they strip its class labels and add open-vocabulary classification on top.

---

## OpenMask3D (NeurIPS 2023)

[src: openmask3d]

**Architecture:** Two stages. (1) Mask3D (frozen, trained on ScanNet200) generates M class-agnostic binary masks. (2) Mask-feature computation: for each mask, select top-k (k=5) views with highest mask visibility; in each view, use SAM (ViT-H) to refine the 2D mask projection; crop at 3 multi-scale levels; pass through CLIP ViT-L/14@336px to get per-crop feature vectors; average-pool across crops and views → one 512-d CLIP vector per 3D instance. At query time, cosine similarity between text embedding and mask features → retrieval in ~1–2 ms.

**Accuracy on ScanNet200 val (312 scenes):**

| Method | AP | AP50 | AP25 | head | common | tail |
|---|---|---|---|---|---|---|
| Mask3D (closed-vocab, supervised) | 26.9 | 36.2 | 41.4 | 39.8 | 21.7 | 17.9 |
| OpenScene 2D Fusion + masks | 11.7 | 15.2 | 17.8 | 13.4 | 11.6 | 9.9 |
| **OpenMask3D** | **15.4** | **19.9** | **23.1** | 17.1 | 14.1 | **14.9** |

OpenMask3D outperforms other open-vocabulary methods especially on tail categories (rare objects). On Replica: AP 13.1 / AP50 18.4 / AP25 24.2 (out-of-distribution generalization test).

**Compute:** Mask-feature computation of a ScanNet scene takes **5–10 minutes on a single GPU**. The paper does not specify minimum VRAM; the GitHub README includes an `OPTIMIZE_GPU_USAGE` flag that "minimizes GPU memory footprint" at the cost of additional slowdown [src: openmask3d-github]. SAM ViT-H requires ~7 GB VRAM alone; the MinkowskiUNet backbone adds further; realistically **≥12 GB VRAM** is required for the default pipeline.

**Limitations noted in paper [src: openmask3d]:** Per-mask features are image-derived so cannot encode globally occluded parts or spatial relationships. 5–10 min/scene latency makes it offline-only. Mask quality (from Mask3D) is the binding performance constraint — oracle masks lift AP to 29.1 (surpassing supervised Mask3D at 26.9), confirming the 3D proposal quality is the bottleneck, not the feature computation.

---

## Open3DIS (CVPR 2024)

[src: open3dis]

**Architecture:** Adds a "2D-Guided-3D Instance Proposal Module" on top of the 3D network proposals. 2D open-vocab segmenter (Grounding DINO or SAM) generates masks per frame; these are projected into 3D point-cloud regions using depth; agglomerative clustering across frames merges them into coherent 3D proposals. These 2D-derived proposals are fused with Mask3D/ISBNet 3D proposals, then CLIP features are extracted pointwise (per-point feature aggregated across multi-scale crops across views).

The key motivation: OpenMask3D's pure 3D proposals fail on small/geometrically ambiguous objects (tissue boxes, narrow items) because Mask3D's 3D backbone cannot resolve them. The 2D-guided proposals recover these.

**Accuracy on ScanNet200 val:**

| Method | Proposal source | AP | AP50 | AP25 | time/scene (s) |
|---|---|---|---|---|---|
| OpenMask3D | Mask3D | 15.4 | 19.9 | 23.1 | 553 |
| Open3DIS | ISBNet only | 18.6 | 23.1 | 27.3 | 57.7 |
| Open3DIS | ISBNet + 2D | **23.7** | **29.4** | **32.8** | 360 |

The 2D-guided variant is ~1.5× better AP than OpenMask3D but costs 360 s/scene (full SAM over all frames). The 3D-only Open3DIS variant at 57.7 s/scene is faster than OpenMask3D while being more accurate.

**Compute:** A100 40 GB GPU used; the 2D-guided SAM-heavy variant is compute-intensive. Not runnable on 4 GB consumer GPU.

---

## Open-YOLO 3D (ICLR 2025 Oral)

[src: open-yolo3d]

**Architecture:** Drops SAM entirely. (1) Mask3D generates class-agnostic 3D proposals. (2) An open-vocabulary 2D object detector (YOLO-World XL) generates bounding boxes with class labels across all RGB frames. (3) Construct "Low Granularity Label Maps" per frame (fill bounding-box regions with predicted class label). (4) Project each 3D mask into the top-k most visible frames; collect labels from the label maps at projected points; majority-vote → class assignment.

Insight: the 3D mask projection onto image coordinates already preserves instance boundaries; running SAM in 2D is therefore redundant — a YOLO bounding box is sufficient to label the 3D mask.

**Accuracy on ScanNet200 val (same setting, Mask3D proposals, single A100 40 GB):**

| Method | AP | AP50 | AP25 | head | common | tail | time/scene (s) |
|---|---|---|---|---|---|---|---|
| OpenMask3D | 15.4 | 19.9 | 23.1 | 17.1 | 14.1 | 14.9 | 553.9 |
| Open3DIS (ISBNet+2D) | 23.7 | 29.4 | 32.8 | 27.8 | 21.2 | 21.8 | 360.1 |
| **Open-YOLO 3D** | **24.7** | **31.7** | **36.2** | **27.8** | **24.3** | **21.6** | **21.8** |

Open-YOLO 3D is **~16× faster than OpenMask3D** and **~16× faster than Open3DIS-with-2D** while matching or exceeding their accuracy. On Replica: AP 23.7 / AP50 28.6 (best among 3D-network-only variants).

**Compute:** Single A100 40 GB used for experiments. The key speedup is eliminating SAM (which dominated the 5–10 min/scene cost in OpenMask3D). The remaining bottleneck is Mask3D (3D backbone, ~13 s) + YOLO-World inference over all frames (~seconds). The authors do not report minimum VRAM explicitly; Mask3D + YOLO-World XL together require **≥8 GB VRAM** (Mask3D's MinkowskiUNet is the heavy piece).

**Limitations [src: open-yolo3d]:** The bounding-box label map is "low granularity" — when two objects overlap in the 2D projection (one behind the other), the larger one's bounding box can contaminate the smaller one's label. Also: all methods assume dense, well-posed RGB-D captures; the ScanNet dataset uses a structured-light depth sensor (Intel RealSense-class) with high coverage.

---

## FOLK (arXiv 2025)

[src: folk]

**Architecture:** Knowledge-distillation approach. Teacher: a multi-view CLIP embedding extractor similar to OpenMask3D (projects 3D Mask3D proposals to diverse viewpoint images → extracts CLIP features per instance; adds viewpoint-diversity selection and density-guided mask completion). Student: a lightweight VL-adapter on top of Mask3D's point-wise features — a two-layer MLP that maps average-pooled 3D instance features into CLIP embedding space. Label-guided distillation filters inconsistent 2D views and trains the student to produce 3D embeddings that match the teacher's CLIP embeddings. **At inference:** only the distilled 3D student runs — no 2D images needed, no SAM, no CLIP encoder. Classification is purely from the 3D point cloud.

**Accuracy on ScanNet200 val:**

| Method | AP | AP50 | AP25 | head | common | tail | time/scene (s) |
|---|---|---|---|---|---|---|---|
| OpenMask3D | 15.4 | 19.9 | 23.1 | 17.1 | 14.1 | 14.9 | 553.9 |
| Open3DIS (ISBNet+2D) | 23.7 | 29.4 | 32.8 | 27.8 | 21.2 | 21.8 | 360.1 |
| Open-YOLO 3D | 24.7 | 31.7 | 36.2 | 27.8 | 24.3 | 21.6 | 21.8 |
| **FOLK** | **26.6** | **35.7** | **41.4** | **30.2** | **25.0** | **24.0** | **3.64** |

FOLK is the current SOTA on ScanNet200 (AP 26.6, AP50 35.7, surpassing the second-best by 4% AP50). Inference is ~3.6 s/scene — **6.0× faster than Open-YOLO 3D** and **152× faster than OpenMask3D**. On Replica, Open-YOLO 3D leads (AP50 28.6 vs FOLK 27.9), but FOLK is 5.7× faster.

**Why so fast:** At inference, FOLK is just Mask3D (class-agnostic proposals, ~13 s → but with FOLK's optimized proposal setup, ~3.6 s total) + a VL-adapter MLP. No 2D image processing at inference time.

**Compute at inference:** Mask3D backbone + a 2-layer MLP. This is the **lightest inference footprint** of any OV-3DIS method. Mask3D requires a GPU (sparse convolution via MinkowskiEngine); the VL-adapter is negligible. Estimated minimum VRAM for inference: **≥4–6 GB** — Mask3D's sparse 3D UNet is memory-efficient. (Note: training the distillation requires running the teacher, which costs the full CLIP+multi-view pipeline — but that is one-time training on a labelled dataset, not per-robot-deployment inference.) The student-only inference path is genuinely lightweight.

**Key caveat [src: folk]:** The student was trained and evaluated on ScanNet200 (indoor RGB-D scenes). Generalization to a new robot's domain (novel objects, different sensor characteristics, different viewpoints) requires re-distillation using the teacher on new data — this is not zero-shot.

---

## OV-MAP (arXiv June 2025)

[src: ov-map]

**Architecture:** Designed for mobile robots. The motivation is that per-voxel methods (LERF, ConceptFusion, OpenScene) blur instance boundaries because CLIP features from adjacent voxels bleed. OV-MAP is a zero-shot method that does not require a trained 3D instance segmentation model (no Mask3D). Pipeline: (1) Use a class-agnostic 2D segmentation model (e.g. SAM) to generate 2D masks per frame; (2) supplement raw depth with "synthetic depth" back-projected from the point cloud (addresses depth holes/missing coverage); (3) project 2D masks into 3D space using the supplemented depth → generate candidate 3D masks; (4) 3D mask voting mechanism over mesh-segmented areas to merge and refine; (5) assign CLIP label from the highest-scoring 2D view per instance.

Key advantage: **no supervised 3D segmentation model is needed** — the system adapts to any scene with RGB-D and a point cloud. The supplemented depth step explicitly addresses depth holes.

**Results on ScanNet200:** "superior zero-shot performance" claimed vs OpenMask3D/ConceptFusion, with real-world robot validation. Specific AP numbers not extracted from the captured text (paper is a 7-page conference paper with result figures; the body text states improvements over prior methods).

**Relevant to our regime:** The "synthetic depth from point cloud" hole-filling step directly addresses the sparse passive-stereo coverage problem. This is the only paper in the set that explicitly acknowledges and mitigates depth-hole failure modes. Real-world robot experiments conducted (Fig. 1 shows a mobile robot with OV-MAP-labeled 3D map). **Research stage** — no deployed production system.

---

## Edge-device 2D OV perception benchmark (Frontiers 2025)

[src: edge-ov-bench]

This study benchmarks **2D open-vocabulary detect-then-segment pipelines** (not 3D-native) on NVIDIA Jetson AGX Orin 64 GB at MAXN mode + TensorRT. Hardware: JetPack 6.0, CUDA 12.2, TensorRT 8.6.2. Evaluated on RefCOCO+ referring expression benchmark (mIoU metric).

Pipelines tested: NanoOWL (OWLViT TensorRT-optimized) + NanoSAM or EfficientViT-SAM; YOLO-World (PyTorch, no TensorRT conversion) + NanoSAM or EfficientViT-SAM.

**Key Jetson Orin results:**

| Pipeline | Best FPS | mIoU | Notes |
|---|---|---|---|
| NanoOWL (patch32, FP16) + EfficientViT-SAM-L0 (FP16/best) | **47.5 FPS** | **84.6%** | Real-time; limited to noun-phrase queries |
| YOLO-World-S (PyTorch) + EfficientViT-SAM-L0 | 26.7 FPS | — | Complex language capable; not TensorRT-convertible |
| NanoOWL (patch32, FP16) + NanoSAM | ~25 FPS | ~stable | Robust to FP16 quantization; never catastrophically fails |
| YOLO-World-S baseline latency | 26 ms/frame | — | No TensorRT = sub-optimal |

**Failure modes on Jetson [src: edge-ov-bench]:** EfficientViT-SAM encoder at FP16 produces catastrophic mIoU=0 failures for L2/XL0/XL1 variants — complete mask collapse with no graceful degradation. NanoSAM (knowledge-distillation-based) is **robust to all precision levels** — never catastrophically fails. YOLO-World cannot be TensorRT-converted without losing zero-shot capability.

**Implication for 3D-native methods on Jetson Orin:** The 3D-native methods (OpenMask3D, Open3DIS, Open-YOLO 3D, FOLK) have not been benchmarked on Jetson Orin. The Jetson AGX Orin 64 GB (used in this study) is a different product from the Orin NX 16 GB in our prototype budget — the AGX Orin has 2048 CUDA cores and 64 GB LPDDR5 unified memory vs the NX's 1024 CUDA cores and 16 GB. Mask3D's MinkowskiEngine sparse convolution has not been reported to run on Orin class hardware in any of the captured papers.

---

## Comparison table — all OV-3DIS methods

*(synthesis from all sources)*

| Method | AP (ScanNet200) | AP50 | Time/scene | Min GPU (est.) | Offline-only? | Online streaming? |
|---|---|---|---|---|---|---|
| OpenMask3D [src: openmask3d] | 15.4 | 19.9 | 5–10 min | ≥12 GB (SAM ViT-H) | Yes | No |
| Open3DIS-3D [src: open3dis] | 18.6 | 23.1 | 57.7 s | ≥16 GB (SAM+Mask3D) | Yes | No |
| Open3DIS-2D [src: open3dis] | 23.7 | 29.4 | 360 s | ≥24 GB | Yes | No |
| Open-YOLO 3D [src: open-yolo3d] | 24.7 | 31.7 | 21.8 s | ≥8 GB | Yes | No |
| FOLK (inference) [src: folk] | 26.6 | **35.7** | **3.6 s** | **≥4–6 GB (est.)** | Yes | No |
| Mask3D (closed-vocab) [src: mask3d] | 26.9 | 36.2 | 13.4 s | ≥8 GB | Yes | No |

GPU estimates are *(synthesis)* based on component model sizes reported in the papers; no paper directly measured minimum VRAM. None of these methods has been deployed in a production consumer robot. All require pre-built 3D point clouds with camera poses.

---

## Comparison to our 2D GDINO+SAM+depth-projection pipeline

*(synthesis — cross-source comparison)*

Our current [[object-fingerprint-memory]] pipeline (GDINO+MobileSAM → crop → DINOv2 embed → stereo depth for metric pose) is a 2D approach that builds a sparse object library frame-by-frame. The OV-3DIS methods above build a global 3D segmentation over a full pre-built scene point cloud.

**Accuracy:** On ScanNet200, the best OV-3DIS method (FOLK) reaches AP50 35.7 on a high-quality structured-light dataset. Our pipeline has not been benchmarked on ScanNet — it targets a different task (per-instance re-ID + metric pose, not mAP on held-out classes). The 2D pipeline's core weakness (aerial detection AP ~28% F1 at odd viewpoints, [[onboard-grasp-perception]]) is a viewpoint/resolution problem, not a 3D-segmentation-quality problem.

**Compute:** Our 2D pipeline runs GDINO (~172M) + MobileSAM (<10M) + DINOv2 ViT-S (~21M) per frame. On 4 GB VRAM with FP16, this is feasible at ~3–5 fps. None of the OV-3DIS methods is designed to run on 4 GB VRAM; FOLK at inference is the closest but its MinkowskiEngine backbone has not been profiled on 4 GB.

**Depth requirement:** Our 2D pipeline uses depth only to compute metric object poses (stereo depth × projected mask centroid). OV-3DIS methods use depth to build the full point cloud and back-project 2D masks — they require dense, well-posed depth for the 3D reconstruction to be coherent. With ~48% passive-stereo coverage (walls, floors, low-texture surfaces all give sparse/zero depth), the reconstructed point cloud will have significant holes, directly harming 3D segmentation quality.

**Latency:** Our 2D pipeline can process frames incrementally and is designed for online operation. All OV-3DIS methods are offline-batch (process a full scene recording, not a live stream).

**Conclusion *(synthesis)*:** For our home-tidy rover at 4 GB GPU + passive stereo + live operation, the 2D pipeline remains the right choice. OV-3DIS methods become relevant if/when: (a) GPU upgrades to ≥8 GB (FOLK inference), or (b) an active-stereo sensor provides dense depth, or (c) an offline mapping pass can tolerate 3–10 s/scene batch processing after each exploration sweep.

---

## Failure modes on sparse/incomplete depth

*(synthesis from all sources + [[world-model-architecture]] constraints)*

All OV-3DIS methods that use 3D point cloud proposals (OpenMask3D, Open-YOLO 3D, FOLK) inherit Mask3D's reliance on a **well-populated 3D point cloud**. The following failure modes apply to our ~48% passive-stereo coverage regime:

| Failure mode | Root cause | Which methods | Severity |
|---|---|---|---|
| Missing objects in point cloud | Blank walls, low-texture surfaces return no stereo depth → zero points at that surface | All Mask3D-based | High: objects on white walls or glass surfaces simply absent from the 3D reconstruction |
| Over-merged instances | Depth holes between adjacent objects create false point-connectivity → Mask3D merges two separate objects | OpenMask3D, Open-YOLO 3D, FOLK | Medium: common with stacked objects on shelves |
| 2D reprojection noise | Depth noise inflates per-point 3D coordinates; CLIP crops from noisy reprojections are blurry/misaligned | All | Medium |
| CLIP feature contamination from co-visible objects | When the 2D crop bounding the masked object also contains background, CLIP features are diluted | OpenMask3D (noted in limitations); FOLK mitigates with dense mask completion | Medium |
| Open3DIS 2D-guided proposals degrade | SAM-derived 2D masks from sparse depth cannot be reliably back-projected → noisy 3D candidates | Open3DIS with 2D | High on blank surfaces |
| OV-MAP depth supplementation path | OV-MAP explicitly synthesizes depth from point cloud to fill holes — the only method designed for this — but the synthesized depth accuracy depends on the quality of the existing point cloud | OV-MAP | Lower than others; specifically designed for this regime |

**Passive stereo on blank walls:** our measured ~48% depth coverage means ~52% of points on typical indoor surfaces (blank walls, white ceilings) return no depth. Mask3D's 3D backbone cannot segment objects that are not represented as point clusters. This is the central barrier to 3D-native methods in our regime.

---

## Production deployment status

*(synthesis)*

**Research only:** All methods in this page — OpenMask3D, Open3DIS, Open-YOLO 3D, FOLK, OV-MAP — are research papers with public code (or code forthcoming per FOLK). None is reported as deployed in a production consumer robot system. All benchmarks are on academic ScanNet200/Replica/S3DIS datasets recorded with high-quality structured-light or LiDAR depth sensors.

**Closest to production (2D pipeline):** The Jetson Orin edge benchmark [src: edge-ov-bench] tests real Jetson AGX Orin hardware with TensorRT-optimized pipelines and establishes the 2D OV pipeline as capable of 47 FPS at 84.6% mIoU — a credible production deployment target. The 3D-native methods have no equivalent hardware benchmark.

**ConceptGraphs/Hydra/DovSG/HOV-SG** (covered in [[scene-graph-world-model]]) are also research-stage on consumer hardware, though Hydra was demonstrated onboard a Jetson Xavier NX at 1 Hz — the only real-time 3D graph system.

---

## Implications for this project

*(synthesis)*

1. **FOLK is the most promising 3D-native method for our stack** — inference requires only Mask3D + a lightweight MLP, eliminating the SAM and CLIP inference bottleneck. Estimated ≥4–6 GB VRAM at inference. The barrier is whether MinkowskiEngine sparse 3D convolution can be profiled/optimized for Jetson Orin NX 16 GB. This is a concrete open engineering question, not a fundamental impossibility.

2. **Passive-stereo depth coverage (~48%) is the binding constraint** for any 3D-native method, not the GPU budget. Even FOLK's fast inference produces no objects where the point cloud is empty. OV-MAP's depth-hole-filling strategy is the most relevant mitigation, but remains research-stage.

3. **4 GB GPU is not viable for any current OV-3DIS method on a live stream.** FOLK inference may be the first to cross that threshold as model optimization matures (INT8 quantization, TensorRT, pruning) — but no evidence yet from the captured sources.

4. **The 2D GDINO+MobileSAM pipeline remains the right choice** for live incremental object enrollment at 4 GB GPU. OV-3DIS is the right choice for post-hoc batch processing of a completed exploration sweep — generating a fully segmented 3D object map — if the GPU can be upgraded.

5. **Depth-hole mitigation is load-bearing** for any shift toward 3D-native methods. The active-stereo path ([[passive-stereo-robustification]] §hardware ladder) or a dense depth sensor upgrade should precede a 3D-native method adoption, not follow it.

---

*Captures: 2026-06-04. Sources: NeurIPS 2023, CVPR 2024, ICLR 2025, arXiv 2025, Frontiers in Robotics and AI 2025.*
