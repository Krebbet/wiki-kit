# Room Segmentation and Doorway Detection from 2D Occupancy Grids

How to automatically partition a 2D occupancy grid into distinct rooms, detect doorways and navigable openings, and assign semantic labels (kitchen, bedroom, hallway) from geometric and object-content cues. Directly addresses the gap in the prototype stack: SLAM Toolbox + 2D LiDAR produces a clean occupancy grid but has no built-in room partitioning or semantic labelling.

---

## The problem — three distinct sub-tasks

*(synthesis)* The problem decomposes into three independent but often pipelined tasks:

1. **Geometric segmentation** — partition the occupancy grid into connected regions that correspond to rooms. Input: the grid only. Output: a segmentation map where each cell is labelled with a room ID.
2. **Doorway/opening detection** — identify which gaps in walls are navigable passages (doors, archways). Input: the grid; optionally RGB or depth images. Output: door locations as point pairs or bounding boxes in the map frame.
3. **Semantic labelling** — assign functional labels (kitchen, bedroom, hallway, bathroom) to each segmented region. Input: segmented regions + object observations from those regions. Output: labelled rooms.

These are not the same problem. A system can do (1) without (2) or (3). Commercial products (Roborock, Dreame) do all three but expose only (3) to users. Research focuses mainly on (1) and (2); (3) is an emerging area, still mostly simulation-based.

---

## Geometric segmentation methods

### Survey background — three classical families [src: 05-rose2-room-seg]

The survey of Bormann et al. (the canonical room-segmentation benchmark) identified three main groups of approaches, all operating on the 2D occupancy grid alone:

| Family | Mechanism | Weakness |
|---|---|---|
| **Voronoi-based** | Segment using a Voronoi graph — spatial partition with maximal distance from obstacles. Narrow passages (doors) become critical points that divide regions. | Sensitive to clutter — furniture creates spurious narrow passages, fragmenting single rooms. |
| **Morphological** | Grow obstacles iteratively until connected free areas become separated. Distance-transform variant uses per-cell distance to nearest obstacle for segmentation. | Requires clean maps; performs poorly on cluttered, real-world SLAM outputs. |
| **Learning / local-appearance** | Classify grid cells from local sensory appearance (raw 2D scan features); harmonise neighbouring labels. | Fuses segmentation with semantic mapping; needs training data specific to the map type being segmented. |

All three families suffer accuracy degradation on real-world 2D LiDAR maps, because furniture, reflective surfaces, glass walls, and partial coverage create occupied cells that look like walls [src: 05-rose2-room-seg].

### ROSE² — frequency-domain clutter removal + wall detection [src: 05-rose2-room-seg]

ROSE² (RObust StructurE identification and ROom SEgmentation, IEEE RAL 2022, Luperto et al., Politecnico di Milano / Aalto) is the current SOTA for purely geometry-based room segmentation from cluttered 2D occupancy grids. Open-source ROS nodes available: `github.com/aislabunimi/ROSE2`.

**Key insight:** walls in human-made environments follow a limited number of *dominant directions*. These show up as radial ridges in the 2D DFT frequency spectrum of the occupancy grid. Furniture and clutter do not share these dominant directions.

**Pipeline (three steps):**

1. **Map cleaning** — compute 2D Discrete Fourier Transform of the occupancy grid. Identify dominant-direction ridges in frequency space. Generate a bandpass filter that retains only those ridges. Apply inverse DFT — each occupied cell gets a score indicating how much it contributes to the structural directions. Threshold to separate walls (high score) from clutter/furniture (low score). Produces clean map *M̄*.
2. **Wall detection** — run probabilistic Hough line transform on *M̄*. Cluster collinear segments by angular similarity and proximity into wall hypotheses. Merge segments lying on the same dominant direction.
3. **Room detection** — fit rooms as rectangular or polygonal regions bounded by the detected walls. Where a dividing wall is missing (open floor plan, partial mapping), fall back to a Voronoi topological graph of the free space: if the free-space graph becomes disconnected, split the region accordingly.

**ROSE² does not assume Manhattan environments** (right-angle only) — it handles non-Manhattan floor plans by detecting however many dominant directions are present.

**ROSE² requires no training** and can be applied to any 2D occupancy grid regardless of the SLAM backend [src: 05-rose2-room-seg].

**Benchmark results on 10 cluttered real-world maps** [src: 05-rose2-room-seg]:

| Method | Precision | Recall | IoU (mean) |
|---|---|---|---|
| **ROSE²** | **89.02** | **93.93** | **73.3** |
| Morphological | 84.98 | 82.30 | 51.24 |
| Distance-based | 88.34 | 79.79 | 54.65 |
| Voronoi | 85.86 | 71.92 | 28.65 |

ROSE² more than doubles IoU vs Voronoi on cluttered maps (73.3 vs 28.65). On the standard benchmark dataset (clean + noise-added maps), ROSE² achieves 93.54 precision / 91.03 recall furnished; 93.26 precision / 97.58 recall unfurnished — without parameter changes [src: 05-rose2-room-seg].

**Limitation:** ROSE² gives room segments (boundaries + IDs) but no semantic labels. It needs a separate stage to say "this room is a kitchen."

### Active room segmentation with visual door detection — ICRA 2025 [src: 09-topology-visual-room-seg-icra2025]

*(CUHK Shenzhen / AIRS, Bao et al., ICRA 2025. Code: `github.com/FreeformRobotics/Active_room_segmentation`).*

Most prior methods are "offline" — they assume a complete, high-quality map already exists. The ICRA 2025 method is "active": the robot segments rooms incrementally *during* exploration, using a complementary loop between exploration and segmentation.

**Three-module framework:**

1. **Door extraction (two-stage)**:
   - *Stage 1 — occupancy map candidates:* Ray-casting from the robot's current position. Adjacent rays with gap length differences reveal potential doorway widths. Generates candidate door point-pairs.
   - *Stage 2 — visual refinement:* A deep neural network (trained DNN) predicts door bounding boxes from RGB images acquired at 12 viewpoints (every 30° of rotation) at each candidate position. Filters false positives that arise because occupancy-map gaps from furniture and wall gaps look the same geometrically.
2. **Within-room exploration:** Frontier-based exploration that stays within the current room until it is fully mapped, rather than greedily jumping to the largest global frontier.
3. **Topology map:** Rooms are nodes; edges store waypoints (the door location that connects two rooms). Room attributes: status (Explored / Exploring / Unexplored), entry waypoints, and metric coverage.

**Results on Gibson dataset** vs Voronoi-graph offline baseline: **+3.9% recall, +10.2% precision** for room segmentation [src: 09-topology-visual-room-seg-icra2025].

**Sensor requirement:** RGBD camera (RGB + depth) — the visual door detection module requires RGB images. Not achievable from a 2D occupancy grid alone.

**Key limitation clearly stated by the paper:** offline geometry-only methods "rely solely on occupancy maps as input" and "offer only limited geometric information, such as convexity or size. These constraints prove insufficient when confronted with cluttered indoor environments, where substantial furniture pieces like tables, sofas, or beds can mislead algorithms into fragmenting a single room into multiple segments." [src: 09-topology-visual-room-seg-icra2025]

---

## Doorway detection — dedicated methods

### Camera-based door-status detection [src: 11-door-status-detection]

*(Antonazzi, Luperto, Basilico, Borghese, University of Milan, 2022. Same group as ROSE².)*

Door-status detection = recognising (a) the presence of a door, and (b) whether it is open or closed. This is important because a closed door changes the *topology* of the navigable map.

**Problem framing:** Cast as object detection via deep learning. Two failure modes of naive OD for robots:
- Training datasets (COCO, ImageNet-scale) use human-viewpoint images. Robot-height cameras see doors from different angles, at partial occlusion, nested in walls. Distribution mismatch causes generalisation failures.
- A general detector trained once is suboptimal in persistent deployment — the robot sees the *same* doors, from the *same* angles, for its entire deployment lifetime.

**Solution — two-phase deployment:**
1. **General detector:** Trained on robot-perspective simulation data (photorealistic sim scenes, navigation paths sampled from robot kinematics). Produces a baseline door-presence + open/closed classifier.
2. **Environment-specific fine-tuning ("qualification"):** The robot collects images of its specific deployment doors during initial mapping. Fine-tunes the general detector on this small dataset. Substantially improves detection on the challenging cases specific to that environment (nested doors, doors similar to walls, partial occlusion).

**Relevance to occupancy grid:** The qualified detector can annotate door locations on the map during the mapping phase. A robot running SLAM can simultaneously accumulate door-detection events and fuse them into the occupancy map as semantic annotations [src: 11-door-status-detection].

### Geometry-only doorway detection (LiDAR-only)

*(synthesis)* From the ROSE² and ICRA 2025 papers, the canonical geometry-only doorway detection method — still widely used — is the **Voronoi critical-point method** (Thrun et al., first applied in the 1990s): extract the Voronoi graph of free space; narrow points (local minima of the free-space width) in the graph correspond to potential doorway locations. The free-space width at a Voronoi node is directly readable from the occupancy grid as the distance to the nearest obstacle.

Limitation: this method cannot distinguish a doorway from a gap between pieces of furniture at the same width. Clutter-rich home environments produce many false doorway candidates. The ICRA 2025 method directly addresses this by adding visual refinement [src: 09-topology-visual-room-seg-icra2025].

---

## Semantic labelling — assigning room types

### SeLRoS — LLM-augmented segmentation (Purdue 2024) [src: 06-selros-llm-room-seg]

*(Kim & Min, Purdue SMART Lab, arXiv 2403.12920, 2024. Code: `sites.google.com/view/selros`)*

**Pipeline — three stages:**

1. **Geometric room segmentation** — run a classical 2D map segmentation algorithm (SeLRoS uses VRF — Voronoi Random Field) to get an initial segmentation map *S*. VRF is chosen because it is modular; any segmenter can be swapped in.

2. **Object mapping** — for each segmented room *s*, take the room centroid. Acquire visual data (RGB image) at that point. Run an object detector (Detic used here) to list objects present. Accumulate per-room object lists *Os*.

3. **Semantic integration** — a two-phase LLM query:
   - *Room-Level Query:* For each room, construct a prompt including: observed objects, room area, room shape (bounding rectangle), adjacency relationships to neighbours. Ask the LLM: "What type of room is this?" Prompt explicitly instructs the LLM to use general architectural priors ("a typical house has one kitchen") to resolve ambiguity.
   - *Environment-Level Query:* Aggregate all per-room responses. Present all rooms' semantic info to the LLM simultaneously. Ask it to review and flag whether adjacent segments with the same label are actually one room split by furniture over-segmentation, or distinct rooms of the same type (e.g., two bedrooms).

**Key feature — over-segmentation correction:** The second LLM pass is specifically designed to merge rooms that were fragmented by furniture. The LLM's world knowledge about typical home layouts (one kitchen, two bedrooms, etc.) combined with adjacency and size information lets it flag merges that geometry alone cannot detect.

**Experimental validation:** 30 ProcTHOR-generated 3D home environments in AI2-THOR simulation. Evaluated qualitatively and quantitatively [src: 06-selros-llm-room-seg].

**Sensor requirement:** RGB camera for object detection (the object-mapping stage). The geometric stage works from the 2D map only. The LLM semantic-integration stage works from the object list + geometric properties — it does not see images directly.

**Limitation:** Simulation-only evaluation. All 30 environments are procedurally generated; real-world deployment not shown. Object detection accuracy is a gating factor — an empty hallway produces no objects and relies entirely on geometry + architectural priors.

### Semantic region mapping without object recognition (Stanford ASL, ICRA 2024) [src: 07-semantic-regions-no-obj-recog]

*(Bigazzi, Baraldi, Kousik, Cucchiara, Pavone, Stanford ASL / Unimore, arXiv 2403.07076, ICRA 2024)*

**Motivation:** Object-based room labelling fails when an object appears in unexpected rooms (fridge in a garage), when regions lack many objects (hallways), or when regions are not clearly delimited (open kitchen + living room). This work labels rooms from *scene appearance* directly — no object detection required.

**Method:**
- A CLIP model is fine-tuned on robot-viewpoint indoor images (multi-modal contrastive loss, small training set). This gives a region classifier that maps an RGB frame to a distribution over region labels (bedroom, kitchen, etc.).
- The robot explores the environment. At each timestep, the region classifier runs on the current camera frame. The classification probabilities are projected into the global occupancy map (egocentric → world frame).
- The global semantic map stores a *probability distribution* over region labels at each cell, updated by Bayesian fusion across all views.

**Results:** Outperforms an object-based mapping system and a pretrained scene classifier baseline in photorealistic simulation. Evaluated in HM3D/Matterport-class simulators [src: 07-semantic-regions-no-obj-recog].

**Sensor requirement:** RGB-D camera (depth used for projection; RGB for classification). Not achievable from a 2D occupancy grid alone — requires active camera observation during a sweep pass.

### Confusion-based sub-room labelling (Orebro/Carlos III, 2026) [src: 08-rethinking-semantic-classification]

*(Mozos, Hernandez, Gomez, Barber, Orebro University / Carlos III Madrid, arXiv 2603.08512, 2026)*

This paper challenges the conventional single-label-per-room paradigm. Its argument: a kitchen that has a table and chairs might also function as an office; forcing a single label loses useful information.

**Method:**
- Appearance-based classifier: VGG16 trained on Places365. Classifies each robot viewpoint.
- Object-based classifier: histograms of object categories found in each area (from NYU Depth V2 statistics).
- Each classifier produces a full-room semantic map. These are merged. Areas where the two classifiers agree are confidently labelled. Areas where they disagree ("confusions") are retained as multi-label sub-regions.

**Key claim:** For the task of *object search*, retaining confusions improves efficiency. The robot knows that a "living room / office confusion" area is a likely place for a laptop. Forcing it to "living room" would send the robot past that area for queries about office objects [src: 08-rethinking-semantic-classification].

**Result:** Fewer viewpoints and less covered area needed to find objects not in their most probable room location (the hard case), both in simulation and real environments [src: 08-rethinking-semantic-classification].

**Sensor:** Camera required (VGG16 on visual frames). Not grid-only.

---

## What shipping consumer products do

### Roborock — LiDAR + neural network + flood-fill (patent) [src: 10-10-roborock-room-seg-patent]

US patent US20220051459A1 ("System and method of automatic room segmentation for two-dimensional laser floorplans") describes the architectural approach:

1. The 2D LiDAR scan data is converted to a 2D image (the occupancy grid as a pixel image).
2. A trained **neural network** classifies each pixel as `room-inside`, `room-outside`, or `noise`. Separately, pixels are sub-classified by room type (bathroom, bedroom, hallway, etc.) — the NN does both geometry and semantics in one pass.
3. A **flooding algorithm** propagates labels from the NN-classified seed pixels to neighbouring unlabelled `room-inside` pixels — flood-fill from confident seeds.
4. The segmentation can use one or more of: morphological segmentation, Voronoi segmentation, distance-based segmentation — as alternatives to or post-processing on the NN output.
5. **Vision-based sensor** identifies doors and windows in an image stream; these are overlaid on the occupancy map as geometric wall elements, used to cut room boundaries before segmentation. A sink, dishwasher, bed, or shower observed by the camera contributes to the room label directly.
6. Room labels output include "kitchen", "living room", "hallway", etc. — assigned automatically [src: 10-10-roborock-room-seg-patent].

**Key takeaway:** Roborock's shipping system requires a camera (for door/window/object detection) in addition to the 2D LiDAR. The "laser floorplan" alone is insufficient — the patent explicitly shows that the 2D scan generates ambiguous room boundaries when a door is open during scanning, and that camera-based door identification resolves that ambiguity [src: 10-10-roborock-room-seg-patent].

### iRobot — VSLAM + object classification (Roomba j7)

The iRobot approach (described in [[robot-vacuum-navigation]]) uses a ceiling-facing camera for navigation SLAM and a front-facing RGB camera for object/obstacle classification. Room segmentation in iRobot's "Imprint" persistent maps relies on the accumulated VSLAM trajectory and floor coverage patterns rather than an explicit wall-detection algorithm. Semantic room labelling is user-assigned in the app (the robot proposes room regions by coverage continuity; the user labels them). The j7's on-robot object detector (trained on >1M images from >1000 homes) classifies obstacles (cords, shoes, pet waste) but does not automatically label room types [src: `robot-vacuum-navigation/03-spectrum-roomba-j7.md`].

### Dreame — camera + ToF for object/obstacle layer; LiDAR for nav

Dreame (e.g., W10 Pro) uses a 3D ToF imager (Infineon REAL3, ~38,000 pixels) for obstacle classification and an LDS turret for SLAM. Room segmentation is LiDAR-map-based with user-verified labels. The ToF camera's object identification contributes to obstacle avoidance, not to room type labelling, which remains user-assigned or heuristic [src: `robot-vacuum-navigation/07-pmd-dreame-w10.md`].

*(synthesis)* The consumer products surveyed (Roborock, iRobot, Dreame) all require at least one camera in addition to LiDAR for any meaningful semantic room labelling. Manual user labelling remains the dominant path for room names in these products; automatic labelling from object content is in patents but not widely deployed as a shipping feature.

---

## Sensor requirements — what each stage needs

*(synthesis)*

| Task | 2D occupancy grid only | + Camera (RGB or RGBD) required |
|---|---|---|
| Geometric room segmentation (boundaries) | **Yes** — ROSE² works purely from the grid | Yes — accuracy improves with visual door detection (ICRA 2025) |
| Doorway detection (geometry-only, Voronoi critical-points) | **Yes** — high false-positive rate from furniture | — |
| Doorway detection (visual refinement) | — | Yes — deep learning on RGB images reduces false positives |
| Door open/closed status detection | No | **Yes** — requires visual observation of the door |
| Semantic room labelling from objects | No (no objects observable without camera) | **Yes** — SeLRoS: object detection → LLM integration |
| Semantic region labelling from appearance | No | **Yes** — finetuned CLIP or VGG16 on RGB frames |
| Consumer product room labelling | Partial (user assigns labels) | Usually yes (Roborock patent uses camera for door/object ID) |

**The LiDAR-only floor plan gives you:** clean wall outlines + room boundaries (with ROSE²) + door *candidate* locations (geometry-only Voronoi). It does not give you semantic labels or open/closed door status.

---

## Research vs shipping — gap analysis

*(synthesis)*

| Dimension | Research SOTA | What ships |
|---|---|---|
| Geometric segmentation | ROSE² — 73.3 IoU on cluttered maps, no training needed, any SLAM backend | Proprietary NN + flood-fill (Roborock patent); Voronoi/morphological in older products |
| Doorway detection | ICRA 2025: RGBD + DNN + ray-casting, 10% precision gain over geometry-only | Geometry-based doorway detection + user-drawn dividers in app |
| Semantic room labelling | SeLRoS: LLM + object detection, simulation-only; Stanford ASL: CLIP-based, sim-only | Manual user labelling is dominant; Roborock patent describes NN-based auto-labelling |
| Open/closed door status | Qualified DNN with environment-specific fine-tuning | Not shipped in consumer vacuums (doors assumed static) |
| Open-floor-plan failure | Both research and shipping products fail here — no wall = no segmentation cue | User draws room dividers manually |
| Real-world deployment | ROSE² tested on real cluttered maps; SeLRoS/Stanford simulation only | Fleet-scale (millions of homes) — but with heavy user-correction |

The largest gaps: (a) automatic semantic labelling in real (not simulated) homes, especially open-floor plans where walls do not separate rooms; (b) shipping systems do not automatically detect doorways — users draw room dividers; (c) no shipping consumer product tracks door open/closed state.

---

## Implications for the prototype

*(synthesis)* The prototype builds a 2D occupancy grid from SLAM Toolbox + Unitree L1 LiDAR ([[mapping-stack-design]], [[slam-toolbox]]). From that grid alone, the following can be added **without any extra hardware:**

- **Geometric room segmentation:** ROSE² (`github.com/aislabunimi/ROSE2`) provides ROS nodes that accept a standard 2D occupancy grid and output segmented rooms. This is a direct drop-in on the SLAM Toolbox output. Expected IoU ~73% on real cluttered environments (the prototype's home environment is likely more cluttered than the office maps in the ROSE² benchmark — calibrate expectations).
- **Doorway candidates:** Voronoi critical-point extraction from the free-space graph gives approximate door locations. False-positive rate from furniture is high; these are candidates to be verified, not confirmed door locations.

To add **semantic labels** and **visual door confirmation**, a camera pass is required:

- During the semantic sweep (Phase 2, [[map-then-navigate]]), run an object detector (GroundingDINO or Detic) at each room centroid and collect an object list per ROSE²-segmented room.
- Feed {room segments, object lists, adjacency, sizes} to a local LLM (Llama 3 / Mistral) using SeLRoS-style hierarchical prompting.
- The LLM assigns room labels and flags over-segmentation merges.
- Door open/closed status can be inferred from the RGB frames using a door-status detector (fine-tuned on the prototype's specific doors) — relevant because the prototype must plan paths through doors.

This maps naturally onto the existing [[map-then-navigate]] two-phase pattern: Phase 1 (SLAM Toolbox) produces the grid; ROSE² runs on that grid; Phase 2 sweep adds objects + LLM labels.

**Open problem — open floor plans:** If the prototype's home has a kitchen-living-room open plan (no wall between them), ROSE² will not segment them as separate rooms — there is no wall or narrow passage to detect. The only options are: (a) manually draw a divider in the app (what consumer vacuums do); (b) use the CLIP/VGG-based appearance classifier (Stanford ASL method) to assign soft semantic labels even without a hard boundary; (c) accept that the prototype labels it as one large room and relies on object locations (oven = kitchen side, sofa = living-room side) for task routing. Option (b) or (c) is more autonomous; both require the camera pass.

---

## Source

| File | Origin | Notes |
|---|---|---|
| `raw/research/room-segmentation/05-05-rose2-room-seg.md` | arXiv 2203.03519, IEEE RAL 2022 — Luperto et al., Politecnico di Milano / Aalto | ROSE²: geometry-only room segmentation from cluttered occupancy grids; benchmark results |
| `raw/research/room-segmentation/06-06-selros-llm-room-seg.md` | arXiv 2403.12920, 2024 — Kim & Min, Purdue | SeLRoS: LLM + object detection for semantic room labelling; over-segmentation correction |
| `raw/research/room-segmentation/07-07-semantic-regions-no-obj-recog.md` | arXiv 2403.07076, ICRA 2024 — Bigazzi et al., Stanford ASL | CLIP-based semantic region mapping without object detection; appearance-based labels |
| `raw/research/room-segmentation/08-08-rethinking-semantic-classification.md` | arXiv 2603.08512, 2026 — Mozos et al., Orebro / Carlos III | Confusion-based sub-room semantic labelling; object search task proof-of-concept |
| `raw/research/room-segmentation/09-09-topology-visual-room-seg-icra2025.md` | ICRA 2025 — Bao et al., CUHK Shenzhen / AIRS | Active room segmentation: RGBD door extraction + within-room frontier + topology map |
| `raw/research/room-segmentation/10-10-roborock-room-seg-patent.md` | US patent US20220051459A1 — Google Patents | Roborock (claimed) — NN + flood-fill; camera for door/object ID; auto semantic labels *(patent — claims, not confirmed deployed reality)* |
| `raw/research/room-segmentation/11-11-door-status-detection.md` | arXiv 2203.03959, 2022 — Antonazzi et al., University of Milan | Door-status detection: general DNN + environment-specific fine-tuning; robot-viewpoint training |
| `raw/research/room-segmentation/01-roborock-nav-explainer.md` | Roborock newsroom | LiDAR SLAM framing + Reactive AI 2.0 structured-light collision layer |

## Related

[[mapping-stack-design]] — floor plan as "Next step 1"; EDA010 showing basic SGBM Option B not usable  
[[slam-toolbox]] — the SLAM backend whose output ROSE² would consume  
[[map-then-navigate]] — Phase 1 (build grid) + Phase 2 (semantic sweep) pattern that feeds the labelling stage  
[[scene-graph-world-model]] — Hydra's room layer (persistent-homology + flood-fill) + HOV-SG's Watershed BEV segmentation; both require 3D mesh input, heavier than 2D grid  
[[robot-vacuum-navigation]] — consumer vacuum nav stack; iRobot Imprint maps; Roborock LDS SLAM  
[[semantic-object-memory]] — the object library that would be queried by room label  
[[world-model-architecture]] — layered world model: anchor + semantic object layer + change detection  
[[dynamic-object-handling]] — POCD (between-session change detection) which interacts with room-level understanding  
[[home-tidy-drone-prototype]] — the build this analysis feeds into
