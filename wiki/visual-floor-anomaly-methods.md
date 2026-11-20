# Visual Floor Anomaly Methods: Floor Banks, Thresholds, Features

Research page (2026-11-17, a research subagent wrote it for the prototyper; revised the same day after a citation-verification pass). The question: the rover keeps a **floor bank** of DINOv2-S mean-patch-embedding descriptors from LiDAR-confirmed flat 0.1 m floor cells. Cosine similarity groups them online into "regions". A camera cell passes when its top-3 similarity to its best region beats that region's 2nd-percentile leave-one-out agreement. What does prior work say about doing this better? The human asks for two things: (1) **separation-based** bars, and (2) a **two-level** test: floor *types* (hardwood, black rubber mat) separated against all *other* types, with *regions* inside each type. A cell that fails its region test may still pass at type level.

Companion pages: [[floor-object-detection-methods]] (what shipping robots do and the error modes) and [[fast-visual-hazard-detection]] (geometric expectation subtraction). This page covers only the **appearance model**.

> **Bottom line.** The anomaly-detection literature (PatchCore, PaDiM, AnomalyDINO, Dinomaly, MuSc), the self-supervised traversability literature (Ulrich & Nourbakhsh, WVN, GONet, V-STRONG, Maier et al.) and NP classification agree on six points that bear on our findings:
> (a) **score per patch and aggregate by max/top-k**, never by mean-pooling a region first, because pooling dilutes a thin cable;
> (b) **middle ViT layers** (and their *key* facet) carry local texture/material, while final layers carry context, and context is what split our hardwood into "regions";
> (c) a **self-labelled bank is contaminated** unless the labels are cleaned (the LiDAR can't see a cable, so it calls the cable "floor");
> (d) a **threshold from the normal data alone** controls only false alarms. An empirical quantile *doesn't even do that reliably*: in NP simulations the naive choice exceeds its target about half the time. Separation needs a negative set, synthetic if necessary, and an order-statistic rule;
> (e) an **independent second vote** (same-frame neighbours, or classic colour/texture) catches what one bank misses;
> (f) the earliest floor-appearance robot already proposed **one model per surface type**, the human's type level.

Citation status: **[v]** means title/authors/venue or the cited claim was checked against the arXiv abstract or HTML, the publisher page, or the PDF on 2026-11-17. Every entry on this page is now [v] unless marked *(unverified)*.

---

## 1. Diagnosis: our findings mapped to the literature

| Our finding | Literature explanation | Source |
|---|---|---|
| Regions are *context* clusters (hardwood split by its surroundings; between-region sim 0.61–0.80 vs within 0.89–0.94) | "Shallow features mostly contain positional information, while in deeper layers, this is reduced in favor of more semantic features". Amir et al. use **mid-layer keys**, which have "less sensitivity to background clutter" than tokens, queries or values. For pixel OOD with DINOv2, the final layer is less informative and early layers lack abstraction. Dinomaly takes "the middle 8 layers of 12-layer ViT-Base". | [v] Amir et al., *Deep ViT Features as Dense Visual Descriptors*, [arXiv 2112.05814](https://arxiv.org/abs/2112.05814); [v] [arXiv 2508.00587](https://arxiv.org/abs/2508.00587); [v] Dinomaly (CVPR 2025), [arXiv 2405.14325](https://arxiv.org/abs/2405.14325) |
| The bank absorbed cables, tape and cells next to objects | The self-supervision signal can't see the anomaly: LiDAR flatness is blind to anything under ~2 cm, so those cells get labelled "floor". Ulrich & Nourbakhsh admit a reference area only after the robot has **driven over it** (≥1 m straight, heading change <18°). WVN likewise labels only the traversed footprint. | [v] Ulrich & Nourbakhsh, AAAI 2000 ([pdf](https://cdn.aaai.org/AAAI/2000/AAAI00-133.pdf)); [v] WVN, [arXiv 2305.08510](https://arxiv.org/abs/2305.08510) |
| A loose catch-all region passes a litter tray | In a kNN memory bank, one diffuse cluster raises everyone's nearest-neighbour similarity. PatchCore **re-weights a score when the nearest neighbour is itself an outlier in the bank** (it checks the local density). SoftPatch filters noisy bank patches with an outlier score before the coreset step. | [v] PatchCore (CVPR 2022), [arXiv 2106.08265](https://arxiv.org/abs/2106.08265); [v] SoftPatch (NeurIPS 2022), [arXiv 2403.14233](https://arxiv.org/abs/2403.14233) |
| Thresholds come from agreement (2nd-percentile LOO), not separation | NP classification: "common practices that directly limit the empirical type I error to no more than α do not satisfy the type I error control objective". In their simulation, **only about half** of the classifiers built from empirical-quantile or 5-fold-CV thresholds met α. | [v] Tong, Feng & Li, *Neyman-Pearson classification algorithms and NP-ROC*, Science Advances 4(2) 2018, [arXiv 1608.03109](https://arxiv.org/abs/1608.03109), R package `nproc` |
| A 0.1 m cell gets one mean-pooled embedding | AnomalyDINO and PatchCore score **each patch** against the bank and aggregate by max, or by the mean of the top 1% (AnomalyDINO). A 2026 paper names this the "signal dilution barrier" of pooled DINOv2 scoring. | [v] AnomalyDINO (WACV 2025), [arXiv 2405.14529](https://arxiv.org/abs/2405.14529), [code](https://github.com/dammsi/AnomalyDINO); [v] [arXiv 2606.09933](https://arxiv.org/abs/2606.09933) |

## 2. Prior work, condensed

### 2.1 Self-supervised traversability and floor segmentation
- **Ulrich & Nourbakhsh 2000, "Appearance-Based Obstacle Detection with Monocular Color Vision"** (AAAI) [v]. The ancestor of our method, and **it detected a cable on the floor** (their Fig. 1).
  - Features: HSI hue and intensity histograms of a trapezoid reference area. A pixel is an obstacle if its hue *or* intensity bin is below a threshold. Hue is valid only above minimum intensity and saturation.
  - Labels: only from reference areas the robot later drove across.
  - Lighting change: the static ("regular") mode gave "several false positives if the lighting conditions are different than during training". The adaptive mode keeps a **dynamic queue of only the 10 most recent** reference histograms, OR-ed with the static set.
  - Failures: a shadow cast from an adjacent room; a yellow leg the same colour as the floor; the bottom of a wall made of floor material. In the prior work they review, shiny floors, carpet boundaries, shadows and highlights all caused false positives.
  - Their proposed improvement: "a set of learned histograms for **each type of surface**", combined with localisation for room-specific sets, and other colour spaces (normalised RGB, opponent) plus texture measures.
- **Maier, Bennewitz et al., IROS 2012** [v] ([pdf](https://www.hrl.uni-bonn.de/papers/maierd12iros.pdf)). A depth sensor's ground-plane estimate labels the image online, and a monocular classifier is retrained continuously. This is the closest analogue to our LiDAR-labelled bank. Indoor, low-height platform.
- **GONet (Hirose et al. 2018)** [v] ([arXiv 1803.03254](https://arxiv.org/abs/1803.03254)). Indoor traversability from "many positive images ... but just a small set of negative images". It trains a GAN on positives plus a small negative set. Data: ~24 h of video from 25+ indoor environments, fisheye mono or stereo, **datasets open-sourced**. Same data asymmetry as ours.
- **Wild Visual Navigation (Frey, Mattamala et al., RSS 2023)** [v] ([arXiv 2305.08510](https://arxiv.org/abs/2305.08510)). DINO/STEGO features over **SLIC superpixels (~100 per image)**, plus a small MLP trained online from walked footprints. Feature-reconstruction error serves as the confidence for separating *unknown* from *traversable*. STEGO improved fidelity and training stability.
- **Seo et al. 2023, "Learning off-road terrain traversability with self-supervisions only"** [v] ([arXiv 2305.18896](https://arxiv.org/abs/2305.18896)). Footprint positives plus unlabelled data, framed as a one-class / PU problem.
- **V-STRONG (ICRA 2024)** [v] ([arXiv 2312.16016](https://arxiv.org/abs/2312.16016)). SAM-encoder features with contrastive learning. **SAM masks extend sparse trajectory labels** and bound them at object edges.
- **Depth-guided Free-space Segmentation for a Mobile Robot (Sevastopoulos et al. 2023)** [v] ([arXiv 2311.01966](https://arxiv.org/abs/2311.01966)). Indoor work: positive-only pseudo-labels from texture homogeneity plus depth, superpixels aligned with DPT features, then a SegFormer fine-tune.

### 2.2 Anomaly and novelty detection with patch features
- **PatchCore** [v] (Roth et al., *Towards Total Recall in Industrial Anomaly Detection*, CVPR 2022, [arXiv 2106.08265](https://arxiv.org/abs/2106.08265), [code](https://github.com/amazon-science/patchcore-inspection)).
  - Bank: mid-level patch features with local neighbourhood aggregation, reduced by **greedy k-center coreset** (stays strong at 1%).
  - Scoring: NN distance, density re-weighted; the image score is the max over patches.
- **PaDiM** [v] (Defard et al., *PaDiM: a Patch Distribution Modeling Framework for Anomaly Detection and Localization*, ICPR 2020 workshop, [arXiv 2011.08785](https://arxiv.org/abs/2011.08785)).
  - Model: a multivariate Gaussian per patch position over multi-layer CNN embeddings, scored by Mahalanobis distance.
  - Fit for us: the position-specific part doesn't suit a moving camera. **One Gaussian per class (floor type) with shrinkage covariance** transfers directly.
- **AnomalyDINO** [v]. Frozen DINOv2 patches, cosine kNN to the nominal bank, top-1% mean aggregation, and augmentations in the bank. Training-free, works from 1–16 references, and it is the closest recipe to ours. One-shot MVTec AUROC rose from 93.1 to 96.6.
- **Dinomaly** [v] (Guo et al., *The Less Is More Philosophy in Multi-Class Unsupervised Anomaly Detection*, CVPR 2025). Middle 8 of 12 ViT-B layers.
- **MuSc** [v] (Li et al., *Zero-Shot Industrial Anomaly Classification and Segmentation with Mutual Scoring of the Unlabeled Images*, ICLR 2024, [arXiv 2401.16753](https://arxiv.org/abs/2401.16753)). "Normal image patches typically have a relatively large number of similar patches in other unlabeled images, while the abnormal ones only have a few."
- **INP-Former** [v] (CVPR 2025, [arXiv 2503.02424](https://arxiv.org/abs/2503.02424)). Normal prototypes drawn from the test image itself. Like MuSc, the query and its references share lighting and context.
- **WinCLIP** [v] (Jeong et al., CVPR 2023, [arXiv 2303.14814](https://arxiv.org/abs/2303.14814)). CLIP needs window/patch ensembling to localise anomalies (MVTec zero-shot segmentation 85.1 AUROC [v]; full-shot patch-kNN methods are far higher, a figure from the author's knowledge). A weak choice for texture.
- **Synthetic anomalies, for building a negative set without real hazards.** CutPaste [v] (Li et al., CVPR 2021, [arXiv 2104.04015](https://arxiv.org/abs/2104.04015)); DRAEM [v] (Zavrtanik et al., ICCV 2021, [arXiv 2108.07610](https://arxiv.org/abs/2108.07610)).

### 2.3 Open-set thresholds with few negatives
- **NP umbrella algorithm** [v] (Tong, Feng & Li 2018, above).
  - Rule: use a **left-out** set of the protected class (one not used to fit the scorer), sort its scores, and take the order statistic at rank k* = min{k : Σ_{j≥k} C(n,j)(1−α)^j α^(n−j) ≤ δ}. Then P(error > α) ≤ δ.
  - Sample size: a valid k exists only when (1−α)^n ≤ δ, i.e. **n ≥ ln δ / ln(1−α)**. That means **59** left-out samples for α=δ=0.05, **29** for α=0.10, δ=0.05, and **45** for α=0.05, δ=0.10 (derived from their Algorithm 1).
  - **Applied to us:** make *hazards* the protected class when the goal is a bounded **miss rate**. Make *floor* the protected class when the goal is a bounded false-stop rate. Either way the sample counts above set how many examples each region or type needs before its bar is trustworthy. Below them, fall back to the parent level (type) or to "unknown, check first".
- **Conformal outlier p-values** [v] (Bates, Candès, Lei, Romano, Sesia, *Testing for Outliers with Conformal p-values*, Annals of Statistics 51(1) 2023, [arXiv 2104.08279](https://arxiv.org/abs/2104.08279)). They need **floor-only** calibration data and give valid per-cell p-values for "is this an outlier vs the floor". They control false alarms (and FDR across many cells per frame), **not misses**. Good for the floor side when negatives are scarce.
- **OpenMax** [v] (Bendale & Boult, *Towards Open Set Deep Networks*, [arXiv 1511.06233](https://arxiv.org/abs/1511.06233); CVPR 2016 per the author's knowledge, *venue unverified*). Fits extreme-value (Weibull) models to per-class distance distributions (Meta-Recognition). The Weibull detail is from the full paper, which wasn't re-read.
- **Hierarchical Novelty Detection for Visual Object Recognition** [v] (Lee et al., CVPR 2018, [arXiv 1804.00722](https://arxiv.org/abs/1804.00722)). It classifies a novel sample to its **nearest known superclass**, top-down or flattened, with confidence-calibrated classifiers and a leave-one-out strategy. This is the formal precedent for "fails its region, passes its type".

### 2.4 Small-obstacle data for robot vacuums and similar
- **Vacuum Objects** [v] (iRobot; described in Pantazis & Salvaris, ECCVW 2022, [arXiv 2208.07654](https://arxiv.org/abs/2208.07654)). 12 classes including cables, socks, shoes, clothes and pet waste; 261,695 train / 27,626 test boxes; 640×480 at ~10 Hz from hundreds of homes. **Not public**: "the dataset ... cannot be released".
- **GONet indoor traversability datasets** [v] (above). Public, positive-heavy, indoor. The closest public set to our camera geometry.
- **Lost and Found** [v] (Pinggera et al., IROS 2016, [arXiv 1609.04653](https://arxiv.org/abs/1609.04653)). Local patch hypothesis tests (free space vs obstacle) in stereo disparity reach 5 cm obstacles at 20 m. 2,000+ annotated frames.
- **SegmentMeIfYouCan** [v] (Chan et al., NeurIPS 2021 Datasets & Benchmarks, [arXiv 2104.14812](https://arxiv.org/abs/2104.14812)). A RoadObstacle track with pixel-wise metrics plus component-wise metrics "insensitive to object sizes". Exact metric names were not re-checked; the author's knowledge says AUPRC, FPR95, sIoU, PPV and mean F1.
- **Gap:** this pass found **no public indoor floor-level dataset of cables, socks or pet waste** from vacuum makers. Roborock, Ecovacs and Dreame publish product claims, not papers or data. Our own logged hazards plus synthetic pastes remain the evaluation set.

## 3. Features: material and texture under lighting change

| Option | Evidence | CPU cost (rough estimate, unmeasured) | Verdict |
|---|---|---|---|
| **DINOv2-S/14 middle layers (≈5–9 of 12); try tokens *and* keys; with registers** (`dinov2_vits14_reg`) | Mid-layer keys trade position against semantics and resist background clutter [v Amir]. Middle layers are best for pixel OOD [v 2508.00587] and are Dinomaly's choice [v]. Registers remove "high-norm tokens ... in low-informative background areas" [v Darcet et al., *Vision Transformers Need Registers*, [arXiv 2309.16588](https://arxiv.org/abs/2309.16588)], which describes plain floor. | Same as today: hook the hidden states and keys in one forward pass. | **Test first.** |
| **DINOv3 ViT-S/16 (distilled)** [v] ([arXiv 2508.10104](https://arxiv.org/abs/2508.10104)) | Gram anchoring prevents dense-feature degradation. Distilled ViT-S and ConvNeXt variants are released. | Similar to DINOv2-S. | Test second, as a drop-in. |
| **Orderless pooling of mid-level features** (Fisher-vector / VLAD-style, or simply a per-cell histogram over a small k-means codebook of patch features) | D-CNN: FV pooling of **conv-layer** (not FC) features gives 82.3% on FMD materials and handles arbitrary region shapes [v Cimpoi, Maji, Vedaldi, CVPR 2015, [arXiv 1411.6836](https://arxiv.org/abs/1411.6836)]. The texture vocabulary comes from DTD [v Cimpoi et al., *Describing Textures in the Wild*, [arXiv 1311.3618](https://arxiv.org/abs/1311.3618)]. | Cheap on top of the patches. | Use as the **type-level** descriptor (material), not for the anomaly score. |
| DINOv2-B | Better features, ~4× the FLOPs of S. | Probably >150 ms per 448 px frame on a laptop CPU. | Only if S fails the layer sweep. |
| AM-RADIO [v] (Ranzinger et al., CVPR 2024, [arXiv 2312.06709](https://arxiv.org/abs/2312.06709)) | Distils CLIP, DINOv2 and SAM into one backbone (E-RADIO is efficient). | Heavy for the B/L variants. | Later. |
| SAM encoder | V-STRONG uses it, but it takes seconds per frame on CPU. | Too slow. | MobileSAM **masks** only. |
| CLIP patch tokens | WinCLIP needed window ensembling and still trails patch-kNN. | — | Skip. |
| **Classic: normalised-RGB/opponent chromaticity + rotation-invariant LBP** (Ojala et al., TPAMI 2002, *unverified this pass*) | Ulrich & Nourbakhsh: hue and saturation are "less sensitive to illumination changes than the intensity band", and they proposed other colour spaces plus texture. LBP tolerates monotone grey-level change. | Under 1 ms per cell. | **An independent second vote.** |

**Lighting and context in the material literature.** MINC [v] (Bell et al., *Material Recognition in the Wild with the Materials in Context Database*, CVPR 2015, [arXiv 1412.0623](https://arxiv.org/abs/1412.0623)) reports 85.2% patch-level material accuracy vs 73.1% for full-scene per-pixel prediction. Scene factors (lighting, geometry, clutter, neighbouring objects) make in-context material recognition harder than isolated patches. That supports keeping the receptive field local (middle layers, small cells) and letting the *bank* handle lighting variety: an adaptive recent-window plus a static set, as in Ulrich & Nourbakhsh.

**Resolution pitfall.** A 14 px ViT patch is far coarser than a cable 1–2 m away seen from 30 cm height. Options: a higher-resolution crop of the near-field strip, or FeatUp [v] (Fu et al., *FeatUp: A Model-Agnostic Framework for Features at Any Resolution*, ICLR 2024, [arXiv 2403.10516](https://arxiv.org/abs/2403.10516)). Both cost CPU, so measure first.

## 4. Two-level (type plus region) design: what the literature supports

- **Type level = material.** Proposed as early as Ulrich & Nourbakhsh ("a set of learned histograms for each type of surface"). Build types from **texture features** (orderless-pooled middle layers plus chromaticity/LBP), not from final-layer context. Model each type as a **Gaussian with shrinkage covariance (PaDiM-style Mahalanobis)** or a small kNN bank. The human names or confirms the types; agglomerative clustering on texture features proposes them.
- **Region level = local appearance.** A kNN bank per type (AnomalyDINO-style, patch-level). Regions within a type explain lighting and wear.
- **Fallback rule** (precedent: Lee et al. 2018). A sample can be novel at the leaf and known at the parent. **Pitfall:** separation measured *between floor types* says nothing about floor vs litter tray. The type bar must **also** be set against a **non-floor negative set**, or the fallback becomes the new catch-all.
- **Bars from separation, with sample-size rules.** For each level, keep a left-out positive set (other sessions) and a negative set:
  - other floor types;
  - LiDAR-confirmed object, wall and tray cells;
  - CutPaste/DRAEM-style **pasted cable, sock and tape crops** on floor cells;
  - logged real hazards.

  Pick the bar by the NP order-statistic rule at the target miss rate (≥29–59 negatives per bar), or by conformal p-values on the floor side. Report AUROC and **FPR at 95% TPR** per region and type. A region whose positives and negatives overlap is flagged as untrusted, never loosened. A region with too few samples defers to its type.

## 5. Ranked methods to test on our data

| # | Change | Expected benefit | Laptop-CPU cost |
|---|---|---|---|
| 1 | **Per-patch kNN scoring, cell score = max (or top-k mean) over its patches**, replacing mean-pooled cell descriptors. The bank stores patches; coreset it. | Thin cables and tape stop being averaged away. This is the single largest lever in the anomaly literature. | A bank of 10⁴–10⁵ × 384 floats is tens of MB. Flat cosine kNN is a few ms per frame. |
| 2 | **Separation-calibrated bars**: negative set (LiDAR non-floor + pasted cables, socks and tape + logged hazards); threshold by the **NP order-statistic rule** (≥59 negatives per bar for α=δ=0.05; ≥29 for α=0.1) or conformal p-values; under-sampled regions defer to their type. Replaces the 2nd-percentile LOO bar, which is the "naive empirical" rule NP shows fails about half the time. | Thresholds with a stated miss/false-stop guarantee. Exposes regions (the catch-all) that can't separate. | Offline. Seconds. |
| 3 | **Layer and facet sweep**: DINOv2-S-reg layers 4–11, tokens vs **keys**, single and concatenated, plus DINOv3-S. Choose by item 2's separation AUROC. | Removes the "context cluster" effect. Hardwood should collapse to one type. | One forward pass with hooks. The sweep is offline. |
| 4 | **Bank hygiene**: drop cells within ~0.15–0.2 m of objects or keep-outs; require ≥2 sessions/views that agree; SoftPatch/LOF trimming before the k-center coreset; PatchCore density re-weighting. Prefer cells the chassis **drove over** (the Ulrich/WVN footprint rule). This removes >2 cm items but *not* flat cables, so multi-view agreement is still needed. | Stops the bank learning cables and tape. Shrinks the catch-all. | Negligible. |
| 5 | **Two-level type → region model** (section 4): orderless-pooled texture features plus a Gaussian per type, a kNN bank per region, and a type fallback gated against non-floor negatives. | Implements the human's spec without a new catch-all. | Negligible. |
| 6 | **Same-frame mutual scoring (MuSc-style)** against the frame's other floor-predicted patches; require agreement with the bank. | Cancels lighting and context. An independent vote. Matches "floor like its neighbours = assumed safe". | O(N²) over ~1–2k patches, a few ms. |
| 7 | **Classic vote**: chromaticity (normalised RGB/opponent or hue-sat) + rotation-invariant LBP per cell vs the type model, with a recent-window plus static bank as in Ulrich & Nourbakhsh. | Cheap, independent of the ViT, proven on cables on plain floors. Weak on patterned rugs and floor-coloured objects. | Under 1 ms per cell. |
| 8 | **Near-field resolution boost** (high-res strip crop or FeatUp). | Cables at 1–2 m span more than one patch. | 2–4× the forward cost on the strip. Measure first. |

## 6. Pitfalls others report

- **Pooling dilutes small anomalies.** Every patch-level anomaly-detection method scores before it aggregates.
- **Deep-layer features encode context and semantics.** Nearby objects make identical floor look different (our regions). MINC shows in-context material recognition is harder than isolated patches.
- **Appearance-only fails on floor-coloured objects** (Ulrich & Nourbakhsh's yellow leg). It produces false positives on shadows, highlights, shiny floors and carpet boundaries. Keep the LiDAR/stereo resolve step ([[floor-object-detection-methods]]).
- **A static appearance model breaks under a lighting change.** Ulrich & Nourbakhsh needed an adaptive queue of only the 10 most recent references. Expect the same between morning and evening sessions.
- **Self-labels inherit sensor blind spots.** With LiDAR labels, anything under the scan's resolution is a false positive in the bank, and footprint labels don't fix flat items.
- **Empirical-quantile and CV thresholds overshoot their target about half the time** (NP simulation). Small per-region sample counts make this worse.
- **Memory banks drift toward permissiveness** as they grow. Use coreset plus density re-weighting, and cap the bank per region.
- **DINOv2 without registers** puts high-norm artefacts in exactly the low-information regions where floor lives.
- **Benchmarks are optimistic.** MVTec is fixed-pose and fixed-light. Robot results (WVN, V-STRONG) are outdoor and coarse. The vacuum datasets are private. Validate on our own logged hazards with pre-registered metrics ([[floor-object-detection-methods]] §3).

## Source
Inline citations above (PatchCore, PaDiM, AnomalyDINO, Dinomaly, MuSc, Ulrich & Nourbakhsh, WVN, GONet, V-STRONG, Maier et al., NP classification; research subagent for the drone-prototype prototyper, 2026-11-17, citation-verified the same day). Project context: drone-prototype EDA376 / EDA377 (floor banks, floor vs non-floor separation); the outcome on the rover is in [[floor-check-visual-first]].

## Related
- [[floor-object-detection-methods]]: shipping-robot practice, error modes, ranked sensor options
- [[fast-visual-hazard-detection]]: geometric free-space violation, fast detectors
- [[floor-map-sensing-options]]
- [[floor-check-visual-first]]: what the rover built from this (fused gate, cascade, object-first check)
