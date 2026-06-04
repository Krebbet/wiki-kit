# Methods Reading List (the papers behind what we actually run)

A curated, prioritised reading list for the methods in the `drone-prototype` relocalization pipeline —
each paper tagged with **the role it plays in OUR system**, so you read it for what it explains here,
not in the abstract. The companion analysis is [[relocalization-method-bakeoff]] (which digests these
against our own measured results — read it alongside the papers). *(synthesis — citations assembled
from the bake-off survey + the prototype's EDA003/EDA004 findings; canonical references added where the
survey only linked repos.)*

> **Why this list exists.** EDA003 showed the relocalization wall was the **feature/matcher front-end**
> (RTAB-Map's ORB→PnP), not calibration — a learned front-end (hloc) cleared it 96% vs 2% on the same
> data. So the load-bearing reading is the **learned-features stack** (Tier 2), not the SLAM backend.

## Tier 1 — the two methods in our head-to-head

1. **RTAB-Map** — Labbé & Michaud, *"RTAB-Map as an open-source lidar and visual SLAM library for
   large-scale and long-term online operation,"* J. Field Robotics 2019; foundational loop-closure in
   *"Appearance-Based Loop Closure Detection for Online Large-Scale and Long-Term Operation,"* IEEE
   T-RO 2013. PDFs at `introlab.3it.usherbrooke.ca`. Repo: https://github.com/introlab/rtabmap
   → **Our baseline.** Explains the `.db` map, DBoW2 appearance-based loop closure (gate 1), and the
   ORB→PnP geometric verification (gate 2) that returns 0 inliers on 88% of right-place matches.

2. **hloc / Hierarchical-Localization** — Sarlin et al., *"From Coarse to Fine: Robust Hierarchical
   Localization at Large Scale,"* CVPR 2019 — arXiv **1812.03506**. Repo:
   https://github.com/cvg/Hierarchical-Localization
   → **The method that won (96%).** The retrieve → match → PnP structure is exactly what
   `src/slam/hloc_bakeoff.py` runs.

## Tier 2 — the hloc components (why learned features clear the wall)

3. **SuperPoint** — DeTone, Malisiewicz, Rabinovich, *"SuperPoint: Self-Supervised Interest Point
   Detection and Description,"* CVPRW 2018 — arXiv **1712.07629**. Repo:
   https://github.com/magicleap/SuperPointPretrainedNetwork
   → **The crux of our finding.** Learned keypoints/descriptors replacing ORB — why they survive
   viewpoint/lighting change where ORB returns 0 inliers.

4. **LightGlue** — Lindenberger, Sarlin, Pollefeys, *"LightGlue: Local Feature Matching at Light
   Speed,"* ICCV 2023 — arXiv **2306.13643** ([openaccess PDF](https://openaccess.thecvf.com/content/ICCV2023/papers/Lindenberger_LightGlue_Local_Feature_Matching_at_Light_Speed_ICCV_2023_paper.pdf)).
   Repo: https://github.com/cvg/LightGlue. Read its predecessor **SuperGlue** (Sarlin et al., CVPR
   2020 — arXiv **1911.11763**) first for the foundation.
   → **The learned matcher** producing the dense, geometrically-consistent correspondences (median
   296 inliers vs ~0 for ORB). ~14M params, runs under 2 GB VRAM — fits our 4 GB GPU.

5. **NetVLAD** — Arandjelović et al., *"NetVLAD: CNN architecture for weakly supervised place
   recognition,"* CVPR 2016 — arXiv **1511.07247**.
   → **Gate 1 (retrieval).** How a live frame finds its neighborhood in the map before matching.

6. **COLMAP — "Structure-from-Motion Revisited"** — Schönberger & Frahm, CVPR 2016; + *"Pixelwise View
   Selection for Unstructured Multi-View Stereo,"* ECCV 2016. Site/repo: https://colmap.github.io
   → **How the hloc map is built** (the SfM model *is* the saved map) and the PnP that recovers pose.
   `pycolmap` is the binding we call.

## Tier 3 — context: what we left behind, and what's queued

7. **ORB-SLAM3** — Campos et al., *"ORB-SLAM3: An Accurate Open-Source Library for Visual,
   Visual-Inertial and Multi-Map SLAM,"* IEEE T-RO 2021 — arXiv **2007.11898**.
   → The canonical **sparse-ORB→PnP family** — the lineage of the wall we got around.

8. **MASt3R-SLAM** — Murai et al., CVPR 2025 — arXiv **2412.12392** (repo:
   https://github.com/rmurai0610/MASt3R-SLAM), built on **DUSt3R** (Wang et al., CVPR 2024 — arXiv
   **2312.14132**) and **MASt3R** (Leroy et al., ECCV 2024 — arXiv **2406.09756**).
   → Our queued **pick #2** — dense pointmap matching that bypasses sparse triangulation+PnP entirely;
   the orthogonal cross-check to hloc. (Offline-only on our 4 GB GPU — see [[relocalization-method-bakeoff]].)

## Tier 4 — calibration foundations (optional, now de-prioritised)

9. **Zhang**, *"A Flexible New Technique for Camera Calibration,"* IEEE TPAMI 2000; **Kannala & Brandt**,
   *"A Generic Camera Model and Calibration Method for Conventional, Wide-Angle, and Fish-Eye Lenses,"*
   IEEE TPAMI 2006. Background for [[camera-calibration-and-self-calibration]].
   → Why the focal/baseline degeneracy bit us. Lower priority now that EDA003 showed calibration was
   **not** the bottleneck — read only to understand that detour.

## If you read just three

**#2 (hloc) · #3 (SuperPoint) · #1 (RTAB-Map)** — that trio explains the entire RTAB-Map-vs-hloc result
and why a front-end swap (not calibration grinding) is the path forward.

## Related

[[relocalization-method-bakeoff]] · [[learned-slam]] · [[slam]] · [[visual-inertial-slam]] ·
[[camera-calibration-and-self-calibration]] · [[passive-stereo-robustification]] ·
[[home-tidy-drone-prototype]] · [[system-architecture]]
