# Language-Embedded 3D Scene Representations

Open-vocabulary querying of 3D scenes without per-object training — LERF, ConceptFusion, LangSplat, Feature3DGS, OpenGaussian, and the 2025 OpenLex3D benchmark that evaluates them. These methods embed CLIP or other vision-language features into a 3D representation (NeRF or 3DGS) so that a text query like "find the red mug" returns a 3D relevancy map or a specific Gaussian point without requiring a per-class detector or labelled bounding boxes.

> **Scope note.** The wiki already covers ConceptGraphs / HOV-SG / DovSG as *scene-graph* approaches ([[scene-graph-world-model]]). This page covers the *dense-field* approaches — language embedded directly into a NeRF volume or per-Gaussian attribute — and how they compare to our explicit object-library design ([[object-fingerprint-memory]], [[world-model-architecture]]).

---

## Method landscape

### LERF — Language Embedded Radiance Fields (ICCV 2023, UC Berkeley)

[src: lerf-2303.09553]

**Mechanism.** LERF augments a NeRF (Nerfacto backbone in Nerfstudio) with a parallel language field `Flang(x, s)` that takes 3D position and a physical scale parameter and outputs a CLIP embedding at that location. During training, a multi-scale CLIP feature pyramid is pre-computed from image crops at `smin = 0.05 m` to `smax = 0.5 m` in 7 increments. The language field is supervised by volume-rendering these embeddings along training rays. DINO features are used as a regularizer (shared backbone) to smooth patchy boundaries. The language field is view-independent (same CLIP vector from any angle at a given position), averaging over all views automatically.

**Querying.** Given a text query, LERF renders dense relevancy maps across 30 scale increments (0–2 m) and selects the scale with peak relevancy. Relevancy is computed via softmax comparison against canonical phrases ("object", "things", "stuff", "texture"). This scale-sweep at query time is the source of slowness.

**Compute.** Training: ~45 minutes on an NVIDIA A100 (~20 GB VRAM). Query: ~31 s per text query at 988×731 resolution (scale sweep across 30 values). Real-time relevancy rendering is possible *within* the trained Nerfstudio viewer once scale is fixed.

**Localization results (LERF dataset, custom scene captures):**

| Scene | LSeg (3D) | OWL-ViT | **LERF** |
|---|---|---|---|
| waldo kitchen | 13.0% | 42.6% | **81.5%** |
| figurines | 8.9% | 38.5% | **79.5%** |
| teatime | 28.1% | 75.0% | **93.8%** |
| bouquet | 50.0% | 66.7% | **91.7%** |
| ramen | 15.0% | **92.5%** | 62.5% |
| **Overall** | **18.0%** | **54.8%** | **80.3%** |

**Failure modes (from §5):** (1) "bag-of-words" CLIP behaviour — "not red" activates similarly to "red"; (2) visually similar objects trigger false positives ("zucchini" fires on similarly-shaped vegetables); (3) objects without side views get embeddings blurred into surroundings; (4) spatial/global reasoning weak ("table" activates only on edges, not the whole surface); (5) requires NeRF-quality multi-view capture with known calibrated cameras — a casual monocular sweep is insufficient.

**Input compatibility.** Requires a set of calibrated posed RGB images. Depth is not needed for the language field (NeRF produces its own geometry). Stereo frames are usable as calibrated RGB input if poses are provided (e.g., via SLAM). No active sensor required.

---

### ConceptFusion (RSS 2023, MIT + UMontréal + UToronto + CMU)

[src: conceptfusion-2302.07241]

**Mechanism.** Not a NeRF or 3DGS method. ConceptFusion builds an explicit **point cloud** where each point stores a pixel-aligned CLIP embedding. The key contribution is a zero-shot mechanism to compute pixel-aligned features from image-level CLIP (which only outputs a global embedding): for each frame, a class-agnostic instance segmenter generates region proposals; each region's local embedding (`f_L`) is fused with the global image embedding (`f_G`) using a cosine-similarity weighting. These pixel-aligned features are then fused into the 3D map using standard TSDF/dense-mapping fusion (Curless–Levoy style). The result is a dense point cloud where each point has a CLIP embedding vector.

**Querying.** Cosine similarity between the query embedding (text, image, audio, or click) and the per-point feature vectors. Sub-millisecond per query (just vector dot products over the point cloud).

**Multi-modal.** Supports text, image, audio (via AudioCLIP), and click-based queries — the only method in this group with audio/image querying.

**Compute.** Online incremental build from RGB-D (tested with Jackal robot + offboard processing). No NeRF training step. Build is real-time given an RGB-D stream + pre-computed CLIP features. Query is fast (cosine similarity over point cloud, CPU-feasible).

**Results on UnCoCo (78 household/office objects, 500K+ text queries):**

| Method | 3D mIoU | IoU>0.25 | IoU>0.5 |
|---|---|---|---|
| LSeg-3D (supervised) | 0.128 | 16.7% | 9.7% |
| OpenSeg-3D (supervised) | 0.289 | 36.1% | 27.8% |
| MaskCLIP-3D (zero-shot) | 0.091 | 9.1% | 1.3% |
| **ConceptFusion (zero-shot)** | **0.446** | **69.4%** | **45.8%** |

ConceptFusion outperforms supervised methods by >40% mIoU on long-tailed household/office objects.

**Input compatibility.** Requires RGB-D (depth from stereo, ToF, or LiDAR). Passive stereo is explicitly mentioned as a valid depth source. No GPU required for the map build itself (CLIP feature extraction needs GPU, but that is a pre-processing step per frame).

**Failure modes.** Dense per-point features aggregate across context scales, producing noisier predictions than object-centric methods. OpenLex3D benchmark (2025) found ConceptFusion produces more "clutter" category errors than object-centric methods like ConceptGraphs — co-visible objects bleed into each other's embeddings.

---

### LangSplat — 3D Language Gaussian Splatting (CVPR 2024, Tsinghua + Harvard)

[src: langsplat-2312.16084]

**Mechanism.** Replaces NeRF with 3DGS. Each Gaussian is augmented with three language embeddings `{f_s, f_p, f_w}` (subpart, part, whole) derived from CLIP features. Instead of storing 512-dim CLIP vectors directly (which would blow up memory by ×35), a scene-specific autoencoder compresses CLIP features to a 3-dimensional latent space per Gaussian. SAM provides the segmentation hierarchy: each training image is segmented into 3 levels (whole/part/subpart) by SAM, and CLIP features are extracted per mask with precise boundaries — eliminating the blurry multi-scale crop approach of LERF.

**Querying.** Three relevancy maps (one per SAM level) are rendered; the highest-scoring level is selected. Query time: **0.28 s/query** at 988×731 (vs. LERF's 30.93 s) — a 119× speedup at this resolution, and **199× speedup at 1440×1080**.

**Training compute.** ~25 minutes on an NVIDIA RTX-3090; **~4 GB GPU memory** during training. Scene has ~2.5 M Gaussians after 30,000 RGB training iterations + 30,000 language feature iterations.

**Results vs. LERF (LERF dataset):**

| Scene | LERF localization | **LangSplat localization** |
|---|---|---|
| ramen | 62.0% | **73.2%** |
| figurines | 75.0% | **80.4%** |
| teatime | 84.8% | **88.1%** |
| waldo kitchen | 72.7% | **95.5%** |
| **Overall** | **73.6%** | **84.3%** |

3D semantic segmentation IoU (LERF dataset): LERF 37.4% → LangSplat **51.4%** overall.

**4 GB GPU claim — important caveat.** The ~4 GB figure is for training a **single small tabletop scene** (~2.5 M Gaussians). Larger indoor rooms (multiple rooms, 10+ M Gaussians) will require more. The 4 GB figure is cited for the training stage (holding gradient state); inference/query may be runnable with less.

**Failure modes (inferred from mechanism).** Same SAM dependency as 3DGS-SLAM: SAM accuracy degrades on textureless, transparent, or reflective objects. The autoencoder compresses to d=3 dimensions — this is extreme and may lose discriminative power for semantically similar objects. Requires known camera poses (same as LERF). No depth sensor required.

---

### Feature3DGS (CVPR 2024 Highlight, UCLA + UT Austin)

[src: feature3dgs-2312.03203]

**Mechanism.** A general framework for distilling any 2D foundation model feature into 3DGS. Each Gaussian learns a semantic feature (CLIP-LSeg, SAM features, or any others) in addition to color. To avoid the memory/speed collapse of high-dimensional per-Gaussian features, Feature3DGS learns a low-dimensional structured feature field that is upsampled via a lightweight convolutional decoder after rasterization.

**Key numbers.** Up to **2.7× faster** feature field distillation and rendering over NeRF-based methods. Up to **23% improvement on mIoU** for semantic segmentation tasks. Parallel Gaussian rasterizer supports arbitrary-dimension features.

**Scope.** More of a *framework* than a standalone query system. Demonstrates CLIP-LSeg and SAM integration for semantic segmentation and language-guided editing. Does not directly address "find the mug" query accuracy in home scenes.

**Input compatibility.** Same as base 3DGS — requires posed RGB images. No depth required.

---

### OpenGaussian (NeurIPS 2024, Peking University + Baidu)

[src: opengaussian-2406.02058]

**Key diagnosis.** Existing 3DGS language methods (LangSplat, Feature3DGS) focus on 2D pixel-level parsing — rendering a feature map and then doing 2D image-space similarity. OpenGaussian identifies two failures for 3D point-level tasks: **(1) weak feature expressiveness** (dimensionality reduction to fit in GPU memory loses discriminability between similar objects); **(2) inaccurate 2D-3D correspondence** (alpha-blending rendering prevents one-to-one 2D↔3D association, causing performance mismatch between 2D and 3D).

**Solution.** Train instance features at the 3D Gaussian point level (not rendered to 2D first) using SAM masks without cross-frame associations. Use a two-stage coarse-to-fine codebook for feature discretization. Associate full-dimensional lossless CLIP features to each 3D instance cluster via an IoU + feature distance metric. This avoids dimensionality compression and enables true 3D point-level selection (including occluded objects).

**Benefit.** Can select Gaussians for an occluded object (not visible in any current camera view). Enables click-based 3D object selection. Provides better 3D robotic task compatibility.

**Compute tradeoff.** By storing lossless CLIP features at instance level (not per-Gaussian), memory per Gaussian stays manageable — but the method requires the coarse-to-fine codebook computation after scene reconstruction.

---

### OpenLex3D Benchmark (NeurIPS 2025 D&B, Oxford + Montréal + Freiburg)

[src: openlex3d-2503.19764]

**What it is.** The first evaluation benchmark designed for open-vocabulary 3D representations. Provides human-annotated labels for 3812 objects across 23 indoor scenes (Replica, ScanNet++, HM3D). Each object has **13× more labels per scene** than the original datasets — capturing synonyms, depictions, visually similar objects, and clutter categories.

**Methods evaluated.** OpenMask3D, ConceptGraphs, ConceptGraphs (GPT), HOV-SG, Kassab2024, ConceptFusion, OpenScene.

**Top-5 synonym frequency (semantic segmentation) — Replica:**

| Method | Synonyms ↑ | Depictions | Vis. Similar | Clutter | Missing | Incorrect |
|---|---|---|---|---|---|---|
| OpenScene | **0.85** (best on Replica) | … | … | … | … | … |
| OpenMask3D | 0.83 | … | … | … | … | … |
| ConceptGraphs | 0.82 | … | … | … | … | … |
| HOV-SG | 0.82 | … | … | … | … | … |
| ConceptFusion | 0.76 | … | … | … | … | … |

*(Note: detailed per-column numbers are in Table 2; above shows the pattern. HOV-SG leads on HM3D (mR 0.88); OpenMask3D leads on Replica/ScanNet++ AP retrieval.)*

**Object retrieval (AP50, Replica):** OpenMask3D+NMS **17.0%**, ConceptGraphs 11.3%, HOV-SG 11.7%. All methods are low — object retrieval across full scenes is a hard unsolved problem.

**Key finding.** Dense methods (ConceptFusion, OpenScene) produce noisier predictions because per-pixel features aggregate context across scales — small objects on tables are confused with table features. Object-centric methods (OpenMask3D, ConceptGraphs) score better on synonyms but fail on cluttered ScanNet++. No single method dominates across both segmentation and retrieval tasks.

**Failure category analysis.** Clutter (co-visible object feature bleed) is the hardest category across all methods, suggesting that segmentation quality and crop scaling are the bottleneck — not the CLIP backbone itself.

---

## Cross-source synthesis

*(This section is editorial — my interpretations across sources, not any single source's claims.)*

### SOTA as of 2025: What wins open-vocab indoor queries?

*(synthesis)* The trajectory is: LERF (NeRF, 80% localization, slow) → LangSplat (3DGS, 84% localization, 119-199× faster, ~4 GB GPU) → OpenGaussian (3DGS, true 3D point-level, handles occlusion). For the specific task of "find object X" in a home scene, **LangSplat is the practical 2024/2025 leader** for speed/accuracy tradeoff. OpenGaussian is architecturally superior for 3D robotics but less benchmarked end-to-end.

The OpenLex3D benchmark shows that **no single method is SOTA across all tasks** — object-centric methods (ConceptGraphs, OpenMask3D) win on synonym precision, dense methods win on some retrieval metrics. For our "find the mug" use case, the object-centric approach that ConceptGraphs represents is more relevant (and it's already covered in [[scene-graph-world-model]]).

### Compute compatibility with our 4 GB GPU + passive stereo

*(synthesis)* The news is mixed:

| Requirement | Reality |
|---|---|
| Build compute (offline OK) | LangSplat: ~25 min on RTX-3090, **~4 GB during training for a small tabletop scene**. Multi-room home: likely 8–16 GB+. |
| Query compute | LangSplat: 0.28 s/query (real-time feasible). ConceptFusion: sub-ms (just cosine sims). LERF: 31 s/query (too slow). |
| Passive stereo input | All methods need posed RGB images + camera calibration. Depth only needed for ConceptFusion. A passive-stereo SLAM output (poses + RGB frames) feeds all of them. |
| 4 GB GPU at query time | LangSplat: yes (rendering only, no gradient state). LERF: exceeds 4 GB even for training. |

The 4 GB constraint is **barely feasible for LangSplat on small scenes but not for full-home reconstruction**. ConceptFusion is the most friendly — GPU only needed for per-frame CLIP inference, not for a global training step.

### Comparison to explicit object library approach

*(synthesis)* This is the central architectural question for our project.

| Dimension | Dense language field (LangSplat) | Explicit object library ([[object-fingerprint-memory]]) |
|---|---|---|
| Query mechanism | Cosine sim over rendered feature field; returns 3D heatmap | DINOv2 kNN over per-instance embedding bank; returns specific instance |
| Instance identity | **None** — category semantics, not per-instance fingerprint | **Per-instance** — DINOv2 distinguishes two identical mugs |
| Update on object move | Must retrain/update the Gaussian field (expensive) | Update pose record only (cheap) |
| Memory for 20–50 objects | Entire scene must be stored as 3DGS (~GB scale) | ~50 records + embeddings (KB scale) |
| Occlusion during query | LERF/LangSplat: fails on fully occluded objects. OpenGaussian: handles partially. | Retrieves stored position (object memory), not current view |
| Lighting sensitivity | CLIP features partially robust, but large changes degrade; SAM masks degrade on specular/textureless | DINOv2 is more robust to lighting than CLIP for instance re-ID |
| "Find the mug" accuracy | 84% localization (LangSplat, LERF benchmark scenes) | ~88%+ multi-view re-ID on synthetic (EDA007; real-capture pending OBJMEM-7) |
| Scalability to new objects | Zero-shot — any new object queryable immediately | Requires enrollment sweep (build fingerprint first) |
| Two identical mugs | Cannot distinguish them (same CLIP embedding) | Can distinguish if DINOv2 embeddings differ (e.g., different wear patterns) |

**Bottom line for home tidy (20–50 objects):** The explicit object library wins on **instance identity** (critical for "which mug belongs to David") and **dynamic updates** (much cheaper to move one record than retrain a Gaussian field). Dense language fields win on **zero-shot flexibility** — no enrollment needed. For a curated home where objects are enrolled once and revisited, the explicit approach is better-suited.

The two approaches are **complementary, not competing**: a language field answers "where is something like a mug?" for coarse localization or novel objects; the object library answers "where is *that specific mug*?" for precision tasks. An architecture could use ConceptFusion-style dense embedding for initial discovery + our DINOv2 fingerprint bank for precise re-ID.

### Failure modes common to all language field methods

*(synthesis from all sources)*

| Failure mode | Evidence |
|---|---|
| Textureless surfaces | LERF §5: objects near surfaces without side views get embeddings blurred to surroundings. LangSplat inherits SAM's failure on textureless objects. |
| Similar-looking objects | LERF: "zucchini" fires on other long green vegetables. CLIP's "bag-of-words" means "red mug" and "blue mug" may score similarly if shape dominates. |
| Lighting changes | Scene-specific training means the CLIP features are baked for the lighting at capture time. Strong lighting changes require re-training. ConceptFusion (online incremental) is more robust since it fuses features over time. |
| Spatial reasoning | LERF §5: "table" activates only on edges, not the whole surface. Queries like "the mug to the left of the kettle" are not supported natively. |
| Small objects on tables | OpenLex3D: all methods score worst on "clutter" category — small objects whose features bleed into co-visible neighbors. |
| Dynamic scenes | All offline-trained methods (LERF, LangSplat, Feature3DGS) require re-training when objects move. Not designed for lifelong household scenes. |

### Is this an alternative or complement to the object fingerprint memory?

*(synthesis)* **Complement, not alternative.** The object fingerprint memory ([[object-fingerprint-memory]], [[world-model-architecture]]) is the right primary approach for our specific use case because:

1. We need **per-instance identity** (two red mugs are different objects) — language fields cannot provide this.
2. We need **cheap dynamic updates** — moving an object in a language field requires field re-training; in the object library it's a pose update.
3. We have a **4 GB GPU constraint and passive stereo** — LangSplat is barely feasible for small scenes, not multi-room.

Where a language field *does* add value:
- **Novel object discovery**: a language field enables "find a charging cable" without ever enrolling a charging cable. The object library requires prior enrollment.
- **Zero-shot query on unexpected objects**: "find the thing that makes coffee" works in a language field without coffee-maker being in the vocabulary at enrollment time.
- **Open-vocabulary tidy target specification**: "put things that look like toys in the toy bin" is a language query, not an instance-lookup.

**Practical recommendation** *(synthesis)*: for the home-tidy prototype at our compute/sensor constraints, implement the explicit object library first (lower compute, instance-aware, already partially built). Add ConceptFusion-style dense CLIP embedding as a *discovery layer* if novel-object handling becomes a bottleneck — it is the friendliest option computationally (no per-scene training, just incremental SLAM + CLIP inference).

---

## Source

- `raw/research/language-3d-scene/01-lerf-2303.09553.md` — Kerr et al., "LERF: Language Embedded Radiance Fields," ICCV 2023. arXiv:2303.09553.
- `raw/research/language-3d-scene/02-feature3dgs-2312.03203.md` — Zhou et al., "Feature 3DGS," CVPR 2024 Highlight. arXiv:2312.03203.
- `raw/research/language-3d-scene/03-langsplat-2312.16084.md` — Qin et al., "LangSplat: 3D Language Gaussian Splatting," CVPR 2024. arXiv:2312.16084.
- `raw/research/language-3d-scene/04-conceptfusion-2302.07241.md` — Jatavallabhula et al., "ConceptFusion: Open-set Multimodal 3D Mapping," RSS 2023. arXiv:2302.07241.
- `raw/research/language-3d-scene/05-opengaussian-2406.02058.md` — Wu et al., "OpenGaussian," NeurIPS 2024. arXiv:2406.02058.
- `raw/research/language-3d-scene/06-openlex3d-2503.19764.md` — Kassab et al., "OpenLex3D," NeurIPS 2025 D&B. arXiv:2503.19764.

## Related

[[scene-graph-world-model]] — ConceptGraphs/HOV-SG/DovSG: the object-centric complement (category-level, not per-instance).
[[object-fingerprint-memory]] — Our explicit per-instance fingerprint approach; why it wins over dense fields for home tidy.
[[world-model-architecture]] — Why dense volumetric / per-point CLIP is the wrong form factor for our passive-stereo 4 GB regime.
[[semantic-object-memory]] — Design space survey; the memory-scaling gap of per-point CLIP fields.
[[learned-slam]] — 3DGS SLAM methods (GS-LIVO, GLC-SLAM) — the reconstruction layer these language fields build on top of.
[[indoor-cluttered-slam]] — Indoor 3DGS context and compute requirements.
[[onboard-grasp-perception]] — Open-vocabulary detection for aerial manipulation (a related but different challenge).
[[mapping-stack-design]] — Where language query fits in the three-layer stack (object library is Tier 2; language field is an alternative formulation).
