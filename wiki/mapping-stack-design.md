# Mapping Stack Design — From Relocalization Anchor to Full Room Model

What the current RTAB-Map stereo build actually produces, what it enables, what it cannot do, and the three structures that need to be built on top of it to support navigation, object interaction, and task planning. Intended as a handoff document for the prototyper. *(synthesis — grounded in drone-prototype EDA003–009 results and the mapping-report-v1.md arc; maps forward onto existing wiki design pages.)*

> **Read alongside:** [[world-model-architecture]] (the layered world-model design), [[anchor-map-protocol]] (how to build a good anchor map), [[relocalization-method-bakeoff]] (why hloc won).

---

## What the current map is

RTAB-Map stereo (with hloc front-end, per EDA003) produces a **relocalization anchor** stored in a `.db` file. It is three structures:

### 1 — Pose graph

A graph of keyframe nodes connected by edges. Each node is a camera position the system decided to remember; edges encode the geometric constraints between them.

- **Odometry edges** — frame-to-frame relative transforms from visual odometry (PnP on matched ORB features). Each is slightly wrong; errors accumulate along the chain.
- **Loop closure edges** — constraints added when the camera revisited a place and geometric verification confirmed it. These pull the trajectory back into a globally consistent shape. Room_sweep3: 365 nodes, 30.5 m, 12 loop closures.

After graph optimization (g2o), each node's pose is the globally consistent estimate — the drift corrected by all loop closure constraints jointly. The pose graph is a **corrected trace of where the camera was** — not just a raw odometry trail.

### 2 — Sparse 3D point cloud

Each keyframe node carries the 3D world positions of its ORB keypoints — corners and edges of textured surfaces that FAST detected. These are computed by:

1. SGBM dense disparity → depth `Z = fx·B/d` at each keypoint pixel
2. Unproject to camera space: `X = (u−cx)·Z/fx`, `Y = (v−cy)·Z/fy`
3. Transform to world frame using the node's optimized pose

The point cloud is **self-consistent with the pose graph** — the points agree with each other given the optimized trajectory. Their absolute accuracy depends on calibration quality and SGBM reliability. Blank walls and specular surfaces produce either no points (SGBM invalid) or wrong points (spurious far depth at 12–43 m).

**What this is:** a sparse set of identifiable world points, each placed at a known world position, used for pose recovery via PnP during relocalization.

**What this is not:** a geometric model of the room. No points on blank surfaces. No dense geometry. No surface normals. No object shapes. No room dimensions.

### 3 — DBoW2 appearance index

For each keyframe node, a bag-of-words vector over the node's descriptors. This is the fast lookup structure for gate 1 of relocalization: given a new camera frame, find which stored node looks most like it. Operates in descriptor space only — no geometry.

---

## What the current map enables and cannot do

| Can do | Cannot do |
|---|---|
| Relocalization — "where am I in this coordinate frame?" (96% cross-session rate with hloc, EDA003) | Tell you where the walls are |
| Drift-free absolute pose within the mapped room | Give room dimensions |
| Coordinate frame anchor for all downstream layers | Navigate around obstacles |
| Metric scale validated to −1.9% vs tape (EDA008) | Identify any objects |
| Multi-sweep coverage pooling (EDA009, 93.6% rate) | Detect free space for path planning |

The map is a **where am I** answer. Everything else — navigation, object finding, task planning — requires the three structures below built on top of it.

---

## Next step 1 — Floor Plan (2D occupancy grid)

**What it is.** A 2D grid where each cell is free, occupied, or unknown. Walls and large furniture appear as occupied columns. The floor is free space. This is what path planners (Nav2, move_base) consume to route the robot from A to B.

**Why RTAB-Map alone is insufficient.** RTAB-Map generates a 2D occupancy grid as a byproduct by projecting the 3D point cloud onto a horizontal plane — but blank walls leave gaps (no ORB corners → no 3D points → no occupied cells there). The floor plan will have holes at every smooth surface.

**How to get a clean floor plan — two options:**

*Option A — 2D LiDAR + SLAM Toolbox.* Add a 2D spinning LiDAR (RPLiDAR S2 ~$200, or Unitree L1 for 3D coverage) and run SLAM Toolbox alongside the stereo pipeline. SLAM Toolbox uses scan-to-map ICP — it doesn't need texture, just geometry. Walls show up as clean occupied lines regardless of surface appearance. The wiki benchmarks SLAM Toolbox at **0.93 N-AUC** indoor (1.75 cm mean precision error in simulation) — the best indoor repeated-navigation performer in the TaskSLAM-Bench comparison, beating 3D LiDAR methods for this use case. ([[slam-toolbox]], [[ros2-nav2]], [[2d-lidar-slam]])

*Option B — Voxel projection from SGBM.* Use the SGBM depth frames directly — for each keyframe, project the valid depth pixels down onto a horizontal occupancy grid and accumulate across all keyframes. Cheaper (no extra hardware) but has the blank-wall gaps. A speckle projector (active stereo) would fill those gaps on indoor textured-but-smooth surfaces. ([[passive-stereo-robustification]])

> **PROBED ON REAL DATA (2026-06-04, drone-prototype EDA010) — basic Option B (point-projection) is NOT usable here.** Fusing 122 keyframes of `room_sweep3` dense SGBM depth (19.8 M points) into a top-down occupancy grid, even with multi-view voting (≥4 distinct keyframes per cell to suppress radial smear), produced **no clean wall lines** — occupied cells hug the camera path (median 0.92 m, 74% within 1.5 m of the path), i.e. near-field furniture reconstructs but the **far textureless walls are absent / lost in spurious-far-depth smear**. Caveat: tests the *basic point-projection* only (no free-space carving, no WLS, no active stereo). See `eda/EDA010-floorplan-probe/`.

> **PROBED AGAIN (2026-06-04, drone-prototype EDA011) — free-space CARVING also fails to recover walls; it's a DEPTH problem.** The proper fix (ray-carve free/occupied/unknown, walls = free/unknown boundary; + distinct-keyframe voting + morphological close) was run on the same data. It recovers a **single coherent navigable free-space region** (usable for *local obstacle avoidance / where-can-I-drive* — the Nav2 STVL model) but **NOT a metric floor plan**: vs tape GT (~9.5 × ~3.1 m corridor, ~29 m²) the carved free region is **17.9 × 11.6 m, 108 m² = 3.7× the true area**, with **width overshot 3.7×** — rays punch *through* the textureless walls. Multi-view voting can't fix it because the spurious-far-depth artifact is **correlated across adjacent keyframes**. Root cause = **wrong depth on textureless walls**; no occupancy-grid cleverness fixes bad depth. See `eda/EDA011-freespace-carving/`.

**Recommendation for the prototype (updated by EDA010 → corrected by EDA011).** ~~Start with Option B~~ ~~Prefer Option A (Unitree L1)~~ — both probes show passive-stereo floor-plan recovery is a **depth** problem (no texture → no/false disparity on walls), and EDA010's "L1 required" steer **overstated the case**. The L1 ($249 USD, on the buy list) remains the **pragmatic clean-walls path** but is **NOT yet proven necessary**. **Before buying the L1, run the untested no-new-hardware contender: learned monocular depth (Depth Anything v2 / Metric3D), which gets depth on blank walls — EDA012.** Other passive cures: active speckle projector (~$30) and WLS disparity filtering. Free-space carving alone already gives a usable *navigable-space* costmap even without clean walls. ([[cheap-lidar-pricing-guide]], [[passive-stereo-robustification]], [[home-tidy-drone-prototype]])

**What it enables.** Path planning, room boundary awareness, safe zones, docking station placement, doorway detection.

**Open problem.** Dynamic objects (chairs moved, doors opened) corrupt a static floor plan. DynaSLAM builds clean static maps by filtering moving objects during the mapping sweep. POCD detects between-session changes. ([[dynamic-object-handling]])

---

## Next step 2 — Object Library

**What it is.** A persistent catalogue of every identified object in the room: semantic label, 3D bounding box (position + dimensions in the anchor map's coordinate frame), appearance embedding for re-identification across sessions, and a last-seen timestamp.

**Why it matters for tidying.** The floor plan tells the robot where it can move. The object library tells it what's there and where things belong — the semantic layer that converts "navigate to coordinate X" into "find the red mug and bring it to the kitchen counter."

**How to build it — map-then-sweep pattern** ([[map-then-navigate]])**:**

1. **Mapping pass** — build the geometric anchor map (pose graph + sparse cloud + floor plan) with the robot moving through the room.

2. **Semantic sweep** — navigate the recorded trajectory again. At each keyframe pose, run:
   - **Open-vocabulary detection** — GroundingDINO or YOLO-World on the RGB frame → bounding boxes + semantic labels (no per-object training required)
   - **Instance segmentation** — SAM (Segment Anything) for pixel masks
   - **3D projection** — use the SGBM depth map + the keyframe's pose to project the detection's depth distribution into world coordinates → 3D centroid + bounding box
   - **Re-identification embedding** — DINOv2 descriptor of the cropped object patch for cross-session identity matching

3. **Object association** — merge detections across keyframes that refer to the same physical object (distance threshold + embedding similarity). Each unique object becomes one entry in the library.

**EDA007 validated** DINOv2 lifting cross-session object recall@P=1.0 from 0.58 → 0.96 on the prototype's object fingerprinting work. Same-colour-confusion (two identical mugs) remains an open problem — spatial location + embedding together is better than either alone. ([[semantic-object-memory]])

The wiki's ConceptGraphs pipeline does this end-to-end: SAM + CLIP + LLaVA builds a 3D scene graph with node precision 0.71 / edge precision 0.88. HOV-SG adds natural-language query routing (56% real-world navigation success rate). ([[scene-graph-world-model]])

**What the library entry contains:**

```
object_id:    uuid
label:        "red coffee mug"
position:     (x, y, z) in map frame   ← centroid of 3D bounding box
dimensions:   (w, d, h) in metres
embedding:    DINOv2 256-float vector  ← for cross-session re-ID
last_seen:    timestamp + sweep_id
confidence:   float (decays if not re-observed)
```

**What it enables.** "Find the red mug" (embedding search), "what's out of place" (compare current positions to expected positions), persistent object memory across sessions, grasp target specification.

**Open problem.** Aerial open-vocabulary detection is at ~28% F1 — significantly worse than ground-robot results, because drone viewpoints are oblique and training data is ground-camera-centric. The ground robot prototype sidesteps this entirely. ([[onboard-grasp-perception]])

---

## Next step 3 — 3D Map

**The level-of-detail question is real** — the right answer depends on what you're doing with it. Three tiers:

### Tier 1 — Voxel occupancy (navigation-grade)

3D extension of the floor plan. Space divided into small voxels (e.g. 5 cm cubes), each marked free/occupied/unknown. Enough to know where the drone can fly without hitting anything — chairs, table legs, overhanging shelves. Nav2's STVL (Spatio-Temporal Voxel Layer) builds this in real time from depth camera input and handles dynamic updates (a person walking through decays out of the map). ([[ros2-nav2]])

**Cost:** essentially free if you already have the depth camera running. Update rate: real-time. Storage: sparse voxel grid.

**Limitation:** no surface detail, no object identity, no colour.

### Tier 2 — Dense point cloud / TSDF (inspection-grade)

Every surface represented as a dense point cloud or Truncated Signed Distance Field. Built by fusing SGBM depth frames across all keyframes using their optimized poses — every valid depth pixel becomes a 3D point, accumulated and merged. Gives you approximate object shapes, dimensions, surface normals.

**Needed for:** reasoning about grasp approach angles, measuring object size to check against payload limit, detecting if a surface is flat enough to land on.

**Cost:** offline compute (minutes per room), not real-time. The SGBM depth already exists — this is just a fusion step.

**Limitation:** still inherits SGBM's blank-wall holes. A speckle projector fills those. ([[passive-stereo-robustification]])

### Tier 3 — 3D Gaussian Splatting (photorealistic)

The room as millions of small Gaussian splats — photorealistic novel-view synthesis from any camera angle, plus a collision-checkable geometric representation. GS-LIVO has demoed real-time 3DGS-SLAM on a Jetson Orin NX at ~20 Hz. GLC-SLAM achieves 0.23 cm ATE on Replica with 7 GB GPU memory. ([[learned-slam]], [[indoor-cluttered-slam]])

**Needed for:** photorealistic rendering for UI/inspection, very precise geometric queries, sim-to-real transfer training data.

**Not needed for:** tidying. The use case doesn't require photorealism.

**Cost:** heaviest compute — currently desktop/Orin-class, not microcontroller. Defer until compute is free or the use case demands it.

### Recommendation

| Use case | Tier needed |
|---|---|
| Navigation, obstacle avoidance | Tier 1 (voxels) — implement now |
| Grasp approach, object sizing | Tier 2 per-object dense cloud — build on demand for detected objects, not for the whole room |
| Photorealistic rendering | Tier 3 — defer |

Build Tier 2 **per-object** rather than for the whole room: when the object library identifies a target object, run a focused dense reconstruction of just that object's bounding volume using the keyframes that observed it. This is cheap (small volume, few frames) and gives you what the manipulation layer needs without the cost of a room-scale dense map.

---

## How the layers stack

```
VOICE COMMAND / LLM TASK PLANNER
        ↓  "find the mug, bring it to the kitchen"
OBJECT LIBRARY          ← "where is the mug, what does it look like"
        ↓
FLOOR PLAN (2D occupancy) ← "plan a path to the mug's location"
        ↓
3D MAP (voxels, per-object dense) ← "avoid obstacles, plan grasp approach"
        ↓
POSE GRAPH + SPARSE CLOUD ← "where am I in this coordinate frame"
        ↓
SENSOR STREAM (stereo frames, LiDAR)
```

Each layer builds on the one below. The anchor (pose graph + sparse cloud) is the prerequisite for everything — which is why the 96% hloc relocalization result is the right first win before building upward.

**The prototyper's next concrete steps:**

1. Wire the RTAB-Map `.db` anchor map into a Nav2 costmap (STVL) using the SGBM depth stream → Tier 1 voxel occupancy
2. Add a semantic sweep pass after each mapping build → object library stub (even GroundingDINO + depth projection is enough to start)
3. The floor plan + object library together unlock the first end-to-end task loop: voice command → object lookup → Nav2 path plan → navigate to object

---

## Source

- `drone-prototype/docs/mapping-report-v1.md` — the measured RTAB-Map arc (sweep1→sweep3→reloc_test2→EDA003)
- `drone-prototype/eda/EDA003-hloc-bakeoff/` — hloc 96% result, fixed-calibration control
- `drone-prototype/eda/EDA007-object-fingerprint/`, `EDA008-metric-pose/`, `EDA009-multi-sweep/` — object re-ID, metric scale, multi-sweep coverage
- *(synthesis)* — this page assembles those results with the wiki's design-space research into a concrete forward plan

## Related

- [[world-model-architecture]] — the layered world-model form-factor design (slow anchor + fast object layer + change detection)
- [[anchor-map-protocol]] — how to build a good multi-sweep hloc anchor map
- [[relocalization-method-bakeoff]] — why hloc (SuperPoint+LightGlue) at 96% vs RTAB-Map at 2%
- [[slam]] — SLAM hub; RTAB-Map two-gate architecture and per-frame mapping pipeline
- [[slam-toolbox]] — the recommended 2D LiDAR SLAM for clean floor plans
- [[ros2-nav2]] — Nav2 architecture; STVL for Tier 1 voxel occupancy; TaskSLAM-Bench results
- [[scene-graph-world-model]] — ConceptGraphs / HOV-SG / DovSG for the object library
- [[semantic-object-memory]] — persistent object-location memory design
- [[dynamic-object-handling]] — DynaSLAM (clean map building) + POCD (between-session change detection)
- [[map-then-navigate]] — the two-phase exploration + semantic sweep pattern
- [[passive-stereo-robustification]] — filling blank-wall SGBM holes with active stereo
- [[onboard-grasp-perception]] — the open-vocabulary detection blocker for aerial use
- [[learned-slam]] · [[indoor-cluttered-slam]] — Tier 3 (3DGS) context and compute requirements
- [[system-architecture]] — where these layers sit in the full cognitive stack (WORLD MAP subsystem §1)
- [[home-tidy-drone-prototype]] — the prototype plan this feeds into
