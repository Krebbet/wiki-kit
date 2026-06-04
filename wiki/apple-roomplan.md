# Apple RoomPlan — Parametric Room Scanning with iPhone LiDAR

How Apple ships a production parametric room scanner on consumer hardware in under 60 seconds, what it produces, how the algorithm works, and what it implies for a floor-plan + object-library design that lacks iPhone LiDAR. This page is purely a reference artifact — a description of what Apple ships, not a design prescription for our prototype.

> **Read alongside:** [[mapping-stack-design]] (our floor plan + object library design), [[world-model-architecture]] (layered world model), [[passive-stereo-robustification]] (our sensor constraints), [[close-range-depth-sensors]] (our depth-sensor options).

---

## TL;DR

- **What it produces:** not a point cloud — a fully parametric `CapturedRoom` struct: walls/doors/windows/openings as 2D planar `Surface` objects, furniture as oriented 3D `Object` cuboids with category labels, all with confidence scores and unique IDs. Exported as USD/USDZ.
- **Algorithm:** two pipelines running entirely on-device (Apple Neural Engine). (1) Room Layout Estimation — a U-Net bird's-eye-view line detector operating on semantic+depth point cloud pseudo-images, then orthographic 2D detectors for doors/windows, lifted to 3D. (2) 3D Object Detection — local frustum-based detector + global scene detector + box fusion with wall snapping.
- **Sensors required:** iPhone 12 Pro+ or iPad Pro LiDAR Scanner + RGB camera + ARKit SLAM pose. The LiDAR is structural: RoomPlan is not available without it, and is not available on visionOS.
- **Speed and scale:** a typical room scans in **30–60 seconds**; Apple cites a 5-minute scan as long enough to cover rooms up to 15 m × 15 m. Recommended single-room maximum is ~9 m × 9 m (30 ft × 30 ft).
- **Accuracy:** Apple reports 95% precision/recall for walls/windows, 90% for doors, and 91%/90% average precision/recall for 3D object detection at 30% IoU. In practice (practitioner review) accumulated wall measurement error reaches ±5 cm per wall, 37 cm total deviation on a 6.45 m room. All walls reported as 16 cm thick regardless of real thickness.

---

## 1. What the output is — parametric primitives, not a point cloud

*(Source: `01-apple-ml-research-roomplan.md`, `08-wwdc22-roomplan-page.md`)*

The top-level data structure is `CapturedRoom`, a fully parametric Swift struct. It contains:

- **`walls`, `doors`, `windows`, `openings`** — each an array of `Surface` objects. Surfaces are **2D planar** structures with:
  - `dimensions` (width × height; depth = 0, no thickness)
  - `transform` (4×4 matrix — position and orientation)
  - `normal` (3D vector perpendicular to the plane)
  - `confidence` (Low / Medium / High, three discrete levels)
  - `curve` (radius + start/end angles for curved walls; nil for flat)
  - `completedEdges` (tracks scan coverage of each edge)
  - unique identifier

- **`objects`** — an array of 3D `Object` items. Objects are **oriented bounding boxes** (cuboids, not axis-aligned):
  - `dimensions` (full 3D: width × height × depth)
  - `transform` (4×4 — position + orientation matching the object's own axis)
  - `confidence` (same three levels)
  - `category` (see §3 for the 16-category taxonomy)
  - unique identifier

The output is exported to **USD / USDA / USDZ**, compatible with Cinema 4D, Blender, AutoCAD, Shapr3D. This is a **semantic CAD model** — each element is typed, dimensioned, and individually editable — not a raw point cloud or mesh.

**iOS 17 additions (WWDC23):** polygon walls (non-rectangular `polygonCorner` array for slanted/beamed walls), floor as polygon, room `sections` (livingRoom / bedroom / bathroom / kitchen / diningRoom with position + floor assignment), `parent` relationships (window → wall, dishwasher → storage), object `attributes` (e.g. stool vs dining chair vs office chair within the "chair" category), and `ModelProvider` for replacing bounding boxes with matched 3D asset models.

---

## 2. Algorithm — how it builds the model

*(Source: `01-apple-ml-research-roomplan.md`)*

RoomPlan runs **two independent ML pipelines** on the Apple Neural Engine (ANE), in real time during the scan:

### 2a. Room Layout Estimation (RLE) — walls, openings, doors, windows

**Stage 1 — Walls and openings (bird's-eye view line detection):**

1. ARKit provides a **semantic point cloud** — each 3D point carries a semantic class label (wall, floor, furniture, etc.) from ARKit's scene understanding.
2. The point cloud is converted to two pseudo-image representations projected into bird's-eye view:
   - **Semantic map**: HxWxK vector (K = number of semantic classes) — semantic class density per bird's-eye pixel.
   - **Z-slicing map**: HxWxZ voxel grid (H=W=512, Z=12, voxel resolution 3 cm × 3 cm × 30 cm). This supports rooms up to 15 m × 15 m × 3.6 m.
3. Both maps are concatenated and fed to a **U-Net** backbone with 2D depth-separable convolutions. Outputs: a **corner map** (which pixels are wall/opening corners) and an **edge map** (likelihood of each pixel being a wall or opening edge). Architecture follows end-to-end wireframe parsing.
4. Detected corners are enumerated into line proposals, then a **line-verification network** classifies which proposals are real walls vs openings.
5. Detected 2D lines are **lifted to 3D** using estimated wall height via post-processing.

**Stage 2 — Doors and windows (orthographic 2D detection):**

For each wall detected in Stage 1, the algorithm generates **projection maps** (semantic map, RGB map, point-distance map) by projecting the semantic/RGB/distance of each point cloud to its nearest wall — effectively an orthographic "unfolding" of each wall face.

These 14-channel inputs (semantic HxWx10 + RGB HxWx3 + distance HxWx1) are fed to a **2D orthographic detector** based on EfficientNet architecture. This is a single-shot 2D object detector that finds door/window bounding boxes on each wall face. The 2D detections are then lifted to 3D using the wall geometry and camera position.

The orthographic projection removes viewpoint variability (the scan angle to any given wall varies as the user moves), which is the key design choice enabling view-invariant detection.

**Reported accuracy:** 95% precision and recall for walls/windows; 90% for doors (evaluated at 2D IoU matching condition).

### 2b. 3D Object Detection (3DOD) — furniture and appliances

The 3DOD pipeline consists of **three components**: a local detector, a global detector, and a box fusion step.

**Local detector (runs during scan, online):**

1. A 7.2 m × 4.8 m × 3.6 m frustum is accumulated from RGB-D frames + camera poses → a **wide frustum semantic point cloud**.
2. Voxelized at 15 cm resolution → 48 × 32 × 24 voxels. Feature per voxel: 35-dim (xyz, normalized-z, semantic features).
3. Fed to a **3D Convolution U-Net** (3 downsampling + 3 upsampling layers). Outputs per voxel:
   - Objectness score (2 channels)
   - Object center offset (3 channels, xyz)
   - Object type (N=16 channels)
   - Size (4×S channels, S=16 size templates + 3 scale-regression offsets)
   - Orientation (2×H channels, H=12 angle bins)
4. Outputs are **aggregated and tracked over time** during the scan — the user sees bounding boxes growing in real time.

**Global detector (runs after scan completes):**

Takes the **entire reconstructed scene** (not a frustum) as input. Trained on a subset of 4 categories (storage, sofa, table, bed — large items where global context matters). Provides contextual disambiguation: e.g., a set of connected kitchen cabinets that the local detector saw as multiple objects may be unified into one by the global detector.

**Box fusion:**

Combines local + global detector outputs, then applies wall-informed adjustments:
- Aligns detected objects to nearby walls (clips bounding boxes to wall surfaces)
- Enforces no-intersection-with-walls constraint
- Handles pair-object relationships (e.g., two sofa boxes → L-shaped sofa clipped to 90 degrees)

**Reported accuracy:** 91% average precision / 90% average recall across 16 categories at 3D IoU 30%. Eight categories (refrigerator, stove, bed, sink, toilet, bath, sofa, washer/dryer) achieve >93% precision and recall. Hardest category: chair (83% precision / 87% recall, due to occlusion and crowding).

---

## 3. Furniture taxonomy — the 16 categories

*(Source: `01-apple-ml-research-roomplan.md`, `04-itjim-roomplan-api.md`)*

The local 3DOD detector recognises exactly **16 categories**:

| Group | Categories |
|---|---|
| Furniture | sofa, table, chair, bed, storage |
| Kitchen | refrigerator, oven, stove, dishwasher, sink |
| Bathroom | bathtub, toilet, washer/dryer |
| Other | fireplace, stairs, TV |

These are detected as **bounding-box cuboids with type labels** — not mesh shapes. The global detector covers a subset (storage, sofa, table, bed).

**What RoomPlan does NOT identify:** air conditioners, boilers, shelves, wall lamps, decorative elements, anything not in these 16 categories. Unrecognised objects are absent from the model.

---

## 4. Sensors and compute — the hardware requirements

*(Source: `01-apple-ml-research-roomplan.md`, `08-wwdc22-roomplan-page.md`)*

**Required sensors:**
- **LiDAR Scanner** — mandatory. Available on iPhone 12 Pro, 13 Pro, 14 Pro, 15 Pro, 16 Pro series, and iPad Pro (2020+). RoomPlan is not available on non-LiDAR iPhones or on visionOS.
- **RGB camera** — used for the semantic/RGB point cloud inputs and ARKit visual tracking.
- **ARKit** — provides the SLAM pose (camera position + orientation in world frame), the semantic point cloud (each point carries a semantic label from ARKit's scene segmentation), and AR tracking quality.

**Compute:** All three neural networks (wall+opening U-Net, door/window EfficientNet, 3D Conv U-Net for 3DOD) run entirely on the **Apple Neural Engine (ANE)** — not the CPU or GPU. Apple applied quantization, pruning, and architecture search to meet ANE power/latency targets. Goal: avoid CPU/GPU thermal throttling during a 5-minute scan.

**Lighting requirement:** minimum 50 lux (typical lit room at night). Below this, RoomPlan provides a coaching prompt "Turn up the light."

**Failure modes for sensors:** floor-to-ceiling mirrors and glass cause LiDAR failures (absorbed or reflected laser light → gaps or phantom objects). Very dark surfaces cause depth failures. High ceilings may exceed LiDAR range.

---

## 5. Scan speed and quality in practice

*(Source: `01-apple-ml-research-roomplan.md`, `04-itjim-roomplan-awful.md`, `08-wwdc22-roomplan-page.md`)*

**Speed:** Typical room: 30–60 seconds. Apple's stated ceiling: 5 minutes for a 15 m × 15 m room. The recommended maximum for a single scan is 9 m × 9 m.

**Real-time feedback:** During scanning, the API provides live coaching instructions via delegate callbacks: "slow down," "move farther away," "turn up the light," "focus on textured areas." These come from lightweight MLP models (dozens of parameters) monitoring luminance, camera linear velocity, and depth quality. Accuracy of the coaching classifiers: ~90%.

**Post-processing:** After the user stops scanning, `RoomBuilder.capturedRoom(from:)` runs an async post-processing step ("within just a few seconds") that beautifies objects and finalises the model.

**Quantified accuracy (Apple):** 95%/95% precision/recall walls, 90%/90% doors, 91%/90% average 3DOD.

**Quantified accuracy (practitioner, it-jim):** Wall length errors accumulate — ±5 cm per wall, total deviation of 37 cm on a 6.45 m measured room. All exterior walls reported as 16 cm thick (not measured). Structures over ~50 cm thick are split into two thin walls.

**Known limitations (source: `04-itjim-roomplan-awful.md`):**

| Limitation | Detail |
|---|---|
| No ceiling data | Ceiling not captured at all — affects volume calculations, lighting design |
| 16 cm wall thickness | All walls output as ~16 cm regardless of actual thickness |
| ±5 cm per-wall error | Accumulates across multi-wall rooms |
| Rectangular simplification | Semicircular arches, sloped ceilings → primitive rectangles |
| No height variation | Moldings, baseboards, steps within a room ignored |
| Reflective surfaces | Mirrors, glass → gaps or phantom objects in the model |
| Door representation | Open/closed door not visually distinguished from opening in 3D model; swing direction not captured |
| Max room ~9 m × 9 m | Longer scans risk thermal throttling and tracking drift |
| Single floor only | Multi-story buildings require separate scans per floor |
| Automatic wall angle snap | Walls snapped to perpendicular even if real geometry is not |

---

## 6. Multi-room scanning (iOS 17+, WWDC23)

*(Source: `09-wwdc23-roomplan-page.md`)*

In iOS 17, RoomPlan gained **MultiRoom support** via the `StructureBuilder` API:

**Challenge:** each room scan has its own local coordinate system (ARSession restarts between rooms → different world origins).

**Two solutions for a shared coordinate frame:**
1. **Continuous ARSession:** set `pauseARSession: false` when stopping a room scan, then start the next scan with the same running ARSession. All rooms share one coordinate frame automatically.
2. **ARSession relocalization:** save `ARWorldMap` to disk after the first scan; load it before the next scan → ARKit relocalization aligns the new scan's coordinate frame to the saved map's frame. Suitable for returning to the same location days later.

Once all rooms are in the same coordinate frame, `StructureBuilder.capturedStructure(from: [CapturedRoom])` merges them into a single `CapturedStructure` with merged walls/doors/windows/openings/objects (deduplicating shared walls between adjacent rooms).

**MultiRoom limits (Apple's stated guidance):** Single-floor residential only; recommended maximum total area: 2,000 sq ft (~186 m²). Good lighting ≥50 lux throughout.

**Practical merging issues (practitioner):** The automatic merge introduces distortions — floors from different rooms are combined into a single plane, level differences and steps are ignored, and each room's simplification errors compound in the merged model.

---

## 7. Apple Vision Pro — separate architecture, not RoomPlan

*(Source: Apple Developer Forums (captured: `07-apple-forums-roomplan-accuracy.md`); Apple developer documentation search)*

**Key finding: RoomPlan is not available on visionOS.** Vision Pro does not expose the RoomPlan API.

Vision Pro uses ARKit for room understanding through two distinct mechanisms:
- **Plane detection:** detects horizontal and vertical planes (floors, walls, tables) as `PlaneAnchor` objects.
- **Scene reconstruction:** builds a continuous mesh of the surroundings as `MeshAnchor` objects — a geometric mesh, not a parametric model.
- **RoomAnchor:** a visionOS-specific anchor that groups plane anchors into a room representation with wall/floor classifications.

Vision Pro does not produce a RoomPlan-style semantic parametric model from a scan gesture. Its room model is maintained continuously and passively, not via an explicit "scan the room" gesture, and it produces a geometric mesh, not bounding boxes with furniture type labels.

*(Editorial: the Vision Pro architecture reflects different design goals — persistent spatial anchoring for overlay content rather than a one-shot room capture for export. The sensor suite differs too: Vision Pro has 12 cameras and multiple depth sensors, but the RoomPlan algorithm is not ported to it as of 2024-2025.)*

---

## 8. What we can learn — transfer to passive stereo + 2D LiDAR

*(synthesis — cross-source interpretation, not source claims)*

This section draws out design-space lessons for our prototype, which has **passive stereo** + **2D LiDAR** (no 3D LiDAR, no iPhone LiDAR, no ARKit).

### 8a. What RoomPlan requires that we don't have

| RoomPlan ingredient | Our situation |
|---|---|
| 3D LiDAR (ToF, 1–5 m range, 360° azimuth × 60°+ elevation) | We have **2D LiDAR** (single horizontal scan plane) |
| ARKit semantic point cloud (every point labeled by ARKit) | We have **stereo disparity** only — no ARKit, no semantic labels as input |
| Apple Neural Engine (dedicated NN accelerator on iPhone SoC) | We have CPU + GPU (Orin/Pi) |
| RGB-D per-frame semantic labels as 3D input to U-Net | We would need a separate semantic segmentation step |
| Vertical coverage of full room (LiDAR shoots up/sideways/down) | 2D LiDAR gives one horizontal slice |

### 8b. What transfers cleanly

**The bird's-eye-view line detection idea transfers.** RoomPlan's wall-finding approach (project to bird's-eye view → detect lines) is essentially what SLAM Toolbox does with 2D LiDAR: accumulate a top-down occupancy grid and let scan-to-map ICP find wall lines. Our [[2d-lidar-slam]] / [[slam-toolbox]] pipeline is the "poor person's RLE" — same geometric output (wall lines in 2D), same bird's-eye projection, different sensor. The key limitation is we get one horizontal slice not a full vertical wall plane.

**The "semantic point cloud as input" idea is adaptable.** RoomPlan feeds ARKit semantic labels as extra channels to its U-Net. We could do the same: run a 2D semantic segmenter (MobileNet-class) on each stereo frame, project valid stereo depth pixels with their semantic labels into a top-down grid, and accumulate. This is exactly what the "Option B" dense projection in [[mapping-stack-design]] does — minus the semantic labels. Adding semantic labels to the depth projection would make wall pixels distinguishable from furniture pixels.

**The two-stage local + global detector idea transfers.** For our object library: a per-view local detector (GroundingDINO / YOLO-World) running on frustum-width crops is equivalent to RoomPlan's local 3DOD — then a post-scan global pass over all keyframe detections to consolidate. The difference is we detect open-vocabulary (any object), while RoomPlan is limited to its 16 categories.

**The bounding-box output format is exactly what we're building.** Our object library schema (per-instance `{label, map_pose, metric_dims, embedding, confidence}`) is functionally identical to RoomPlan's `Object` struct — a typed, dimensioned, positioned bounding box. We add the DINOv2 instance embedding for re-identification across sessions, which RoomPlan lacks (it has no session persistence model).

**The "snap to wall" fusion logic is valuable.** RoomPlan's box fusion clips detected objects to wall surfaces and enforces no-intersection-with-walls. Our object library's 3D bounding box poses would benefit from the same: once we have a 2D floor plan (from SLAM Toolbox), detected objects can be snapped to their nearest wall face, reducing pose noise and improving placement plausibility.

### 8c. The vertical dimension gap

RoomPlan's 3D LiDAR gives it **full vertical coverage** — it knows object heights, distinguishes wall height from ceiling height, and detects windows at the correct elevation. Our 2D LiDAR gives one horizontal slice. We bridge this gap with **stereo depth** for the vertical dimension — but stereo is sparse on blank surfaces. This is precisely why EDA010 showed the "basic Option B" dense projection fails for floor plan walls: no stereo points on smooth wall surfaces → no occupied cells at the correct wall locations. RoomPlan would not have this problem (its LiDAR hits every surface regardless of texture).

### 8d. The ceiling gap

RoomPlan explicitly does not capture ceilings. We have the same gap and the same consequence: no volume estimation, no overhead clearance map for drone flight. For a ground robot, this is fine. For an indoor drone, ceiling clearance is safety-critical. This is a gap RoomPlan and our prototype share.

### 8e. What RoomPlan sets as the production ceiling

RoomPlan on iPhone 12 Pro+ (2020 hardware) achieves in a consumer product:
- **Sub-60-second full-room parametric capture**, with live coaching
- **91/90% precision/recall** for 16 furniture categories in 3D
- **±5 cm** wall measurement accuracy in practice (worse than the stated lab numbers, but usable)
- **All on-device** on ANE, no cloud, no external compute

This is the ceiling for what iPhone LiDAR + ARKit + ANE can do. Our passive-stereo + 2D LiDAR regime sits well below this: we get walls from 2D LiDAR (one slice, no elevation), we get furniture detection from open-vocabulary detectors on RGB frames (no depth-guided 3D voxelization), and we get metric poses from stereo depth (sparse, noisy on blank surfaces). The gap is real and quantified; closing it requires either adding a 3D LiDAR (Unitree L1 at $249 gives 3D coverage) or accepting a weaker floor plan.

---

## Source

- `raw/research/apple-roomplan/01-apple-ml-research-roomplan.md` — Apple ML Research: "3D Parametric Room Representation with RoomPlan" (`machinelearning.apple.com/research/roomplan`). Primary algorithm description. Captured 2026-06-04.
- `raw/research/apple-roomplan/04-itjim-roomplan-awful.md` — it-jim: "RoomPlan is Awful and it's Great!" Practitioner accuracy review: measurement errors, wall thickness, mirror failures, merging distortions. Captured 2026-06-04.
- `raw/research/apple-roomplan/04-itjim-roomplan-api.md` — it-jim: "Apple RoomPlan API Integration for Innovative AR Apps." CapturedRoom schema, surface/object data properties, integration patterns. Captured 2026-06-04.
- `raw/research/apple-roomplan/08-wwdc22-roomplan-page.md` — WWDC22 session 10127 transcript: "Create parametric 3D room scans with RoomPlan." CapturedRoom struct definition, RoomCaptureView/Session API, best practices, hardware requirements. Captured 2026-06-04.
- `raw/research/apple-roomplan/09-wwdc23-roomplan-page.md` — WWDC23 session 10192 transcript: "Explore enhancements to RoomPlan." MultiRoom, StructureBuilder, ARWorldMap relocalization, polygon walls, object attributes, ModelProvider, VoiceOver. Captured 2026-06-04.
- `raw/research/apple-roomplan/02-apple-dev-roomplan-overview.md` — Apple Developer: RoomPlan overview page. USD/USDZ export, use cases. Captured 2026-06-04.

## Related

- [[mapping-stack-design]] — our floor plan + object library design (the "poor-person's RLE" via SLAM Toolbox + GroundingDINO object detection)
- [[world-model-architecture]] — layered world model (structural anchor + semantic object layer + change detection)
- [[slam-toolbox]] — our 2D-LiDAR-based wall detection (analogous to RoomPlan's RLE for flat floor-plane geometry)
- [[2d-lidar-slam]] — hardware and algorithm for our floor plan
- [[passive-stereo-robustification]] — why we can't replicate RoomPlan's 3D LiDAR wall coverage with passive stereo alone
- [[scene-graph-world-model]] — ConceptGraphs/Hydra/HOV-SG (richer semantic scene representations than RoomPlan's flat object list)
- [[object-fingerprint-memory]] — our per-instance re-ID bank (adds session-persistent identity that RoomPlan lacks)
- [[close-range-depth-sensors]] — our sensor options for depth perception
- [[indoor-cluttered-slam]] — indoor SLAM on difficult surfaces (texture-less walls, mirrors — the same failure modes RoomPlan has)
- [[home-tidy-drone-prototype]] — the prototype this informs
