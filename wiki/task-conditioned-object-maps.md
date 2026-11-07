# Task-Conditioned Object Maps: Store Objects in 3D, Project Only What the Task Needs

How robots keep a store of known objects and turn it into the 2D layer a planner uses, and how to do that for the drone-prototype rover. The human's pattern (2026-11-07) is: **floor map → every object known on that map → the objects this task needs → project only those, each by its 3D shape and by what the task needs to know about where it sits.** Each step has a precedent, but the precedents never meet in one system. **Object stores** (Hydra, ConceptGraphs, HOV-SG, Clio, Khronos, DovSG) keep objects as boxes or point sets with relations such as "on". **Planners** never read those stores for collision. They plan on a maintained, identity-free costmap (Nav2 voxel layer, STVL, nvblox slice, elevation map) that projects *everything sensed* in a fixed height band. **Task-conditioned selection** exists, but at the wrong level for geometry. SayPlan and Taskography cut a scene graph down for a *symbolic* planner. Clio chooses which objects to *build* from a task list. VLMaps comes closest: it makes a different obstacle map per *embodiment* from a list of object categories. Hornung's PR2 projects one octree into *body-part* height layers, where "the table is only projected on the spine layer". **The full combination is not published as one pattern** as far as this search found: per-task selection of object *instances* from a persistent store, projected by their 3D parts against the body's height band, with support known. It is best described as **VLMaps' per-embodiment obstacle lists + Hornung's height-layer projection + MoveIt's task-specific collision scene, keyed by object identity**. The literature is clear about one condition: **task-conditioned object layers are only safe on top of a task-independent layer of raw sensed obstacles.** The object view can *add* caution or *relax* it only where measured evidence agrees. It must never be the only thing that blocks. On this rig that safety layer exists already (`HeightEvidence`, per 4 cm cell × height band). The biggest gap is concrete: **the bank's small-object keep-outs are z-blind.** `task_loop.known_keepouts` stamps every small bank object as a 0.12 m floor disc at its xy, with no height and no support, so a mug filed on the desk would block the floor under the desk. *(Research synthesis, 2026-11-07, dispatched by the drone-prototype lead; rig facts read from drone-prototype `docs/architecture/README.md`, `docs/architecture/object-understanding.md`, `src/drone/agent/{clearance,hostgate,keepouts}.py`, `src/rover/task_loop.py`, `data/objects/`.)*

## Source

Web research, 2026-11-07 (no raw captures). Primary sources were opened and are listed under **References**, cited inline as `[src: key]`. Two were already verified first-hand on [[tilting-2d-lidar-multiplane-capture]] and are cited from there: `hornung-multilayer` and `lu-layered-costmaps`. Rig context comes from the drone-prototype files named above, and from memories `rover-height`, `nav-clearance-and-relabel-decisions`, `questionable-until-identified`, `beliefs-must-clear`, `object-two-level-outline`, `collections-object-type`, `one-object-bank` and `plan-from-live-maps`.

## Related

[[scene-graph-world-model]], [[world-model-architecture]], [[semantic-object-memory]], [[object-fingerprint-memory]], [[locate-object-from-last-known-position]], [[ros2-nav2]], [[stop-and-go-navigation-on-a-locked-map]], [[mapping-stack-design]], [[indoor-obstacle-avoidance]], [[language-3d-scene-representations]], [[robot-vacuum-navigation]], [[consumer-robot-vacuum-mapping]], [[home-tidying-robots]], [[tilting-2d-lidar-multiplane-capture]], [[dynamic-object-handling]], [[fast-visual-hazard-detection]], [[robust-evidence-mapping-principle]]

---

## 0. The question in this rig's terms

| Fact (drone-prototype, master 2026-11-07) | Consequence for the pattern |
|---|---|
| Rover 0.32 × 0.29 m, top just under **0.53 m**. UNDER needs a measured underside **≥ 0.58 m** from 2 stations, with every band below it seen empty. DRIVE-OVER means ≤ 6 cm (`clearance.py`, rule 15a). | The body's height band is **[0.06, 0.58] m**. Anything wholly outside that band cannot block the rover, *if* the space inside the band was seen. |
| `HeightEvidence` keeps, per 4 cm cell, `flat_n` / `body_n` / `over_n` and **`seen_n` per band** (6–13, 13–20, 20–35, 35–47, 47–53, 53–58 cm), with clocks and gone-detection (rules 15a, 15o). | This is already a task-independent **3D safety layer** projected to 2D by height band, the same thing Hornung's layers and the Nav2 voxel column do (§2). |
| Bank large records carry one **cuboid** (`L, W, H, yaw, base_z`) plus a hull (`bottom_m`, `top_m`). The desk `obj-0012` is 1.45 × 0.74 × 0.75 m with `base_z` 0. | A desk stored as one solid box from 0 to 0.75 m says "blocks the floor". The object store **cannot express "open underneath"**. Only `config/object_classes.json` `host.open_under` does, per class. |
| Bank large cuboids **do not feed keep-outs**. Large-object keep-outs come from per-world LiDAR target bodies (rules 15i, 15q). | Large objects are already projected from *evidence*, not from the store. That is the safe direction. |
| Small bank objects **do** feed keep-outs: `known_keepouts` gives every `kind=small` record a disc, `r_m` 0.12, at `last_floorplan_position.xy_m`, with **no z and no support check**. `refute_known` can only drop it on LiDAR floor evidence (rules 15n, 15p, 15r). | **The bug the human describes.** A small object filed on the desk top becomes a floor keep-out under the desk. Support lives only as free text (`context.support`, e.g. "hardwood floor, about a hand's width from…"). |
| `hostgate.py` walks a camera ray over host footprints. An open host takes a box only within 8 cm of its top or above it, and a ray under a desk reaches the floor. Collections store `host {bank, cls, part, height_m, open_under}` (EDA309). | Support inference **exists at filing time for collections**. It is not stored as a structured field on small records, and it is not used at projection time. |

---

## 1. How object stores represent objects

### 1.1 The systems

| System | Object representation | Relations | Persistence / change | How a planner uses it | Status |
|---|---|---|---|---|---|
| **Hydra** (5 layers: mesh → objects → places → rooms → building) | object nodes on a metric-semantic mesh; **places** = free-space nodes from a GVD | layer-to-layer containment | incremental | navigation runs on the **places** layer, not on object geometry ([[scene-graph-world-model]]) | demoed |
| **ConceptGraphs** | per node: **3D point cloud + bounding box**, a visual feature and a caption | edges from **3D-box IoU → minimum spanning tree → an LLM labels each edge** ("a on b", "b in a", "may be stored in") [src: conceptgraphs] | per build | LLM planner over a JSON node list | demoed |
| **HOV-SG** | open-vocab object nodes in floors/rooms | hierarchy | static | NL → floor → room → object, then a Voronoi graph ([[scene-graph-world-model]]) | demoed, 56 % real nav SR |
| **Clio** | task-relevant object clusters + **places (GVD) + mesh kept regardless of task** | hierarchy | online, onboard | Dijkstra through place nodes to the target object [src: clio] | demoed (Spot) |
| **Khronos** | spatio-temporal objects: a fast window for short-term dynamics, a slow process for long-term change [src: khronos] | — | presence over time | the map reflects the scene "over time" | demoed (RSS 2024) |
| **DovSG** | voxels + objects, with **local** subgraph updates (1 min vs 27 min for a full rebuild) | recomputed only for the changed region | dynamic | LLM task planning ([[scene-graph-world-model]]) | demoed |
| **SayPlan** | 3DSG with assets/objects in rooms | hierarchy | static | the LLM **expands/contracts** a *collapsed* graph to find "the task-relevant subgraph"; a classical **Dijkstra** path planner connects the nodes it picks [src: sayplan, sayplan-site] | demoed: 36 rooms, ~140–150 objects |
| **MoveIt planning scene** | world collision objects (shape primitives / meshes) + attached objects + an octomap | **Allowed Collision Matrix**: per pair, "ignore collisions between certain objects" [src: moveit-ps] | per planning call | the manipulation planner checks *this* scene | shipping (ROS standard) |
| **VLMaps** | dense CLIP features on a top-down grid, **no instances** | — | static | **per-embodiment obstacle maps generated on the fly** from a category list (§3) [src: vlmaps] | demoed (ICRA 2023) |

**Representation.** Every system that plans *motion* against objects stores either an **oriented box plus a point set** (ConceptGraphs) or **primitive / mesh collision objects** (MoveIt). Pure-box stores lose concavity: a desk is a slab plus legs, and a box of it is a solid block. That is why manipulation stacks put meshes or composite primitives into the planning scene, and why the human's standing decision is a **two-level outline**: an external cuboid plus the detailed measured shape (memory `object-two-level-outline`). For navigation, the detailed shape needed is small: **parts with z-intervals** (top slab [0.72, 0.75] m; legs/panels [0, 0.72] m at their footprints). This is Triebel's multi-level-surface idea applied per object ([[tilting-2d-lidar-multiplane-capture]] §4b).

**Storage and query cost.** At 50–100 objects (the human's 2026-10-02 decision: files, no DB) a linear scan with a bbox prefilter costs microseconds. Selection exists in the literature for **LLM context** (SayPlan: token limits) and **symbolic planning** (Taskography: "neither classical nor learning-based planners are capable of real-time planning over full 3DSGs" [src: taskography]). It is **not** there for geometry. Projecting 100 cuboids into a 4 cm grid is cheap, so on this rig selection buys *correctness and clarity*, not speed.

### 1.2 Support relations ("on", "in", "under")

- **The classic formulation** is Silberman et al. (ECCV 2012, NYU Depth v2: 1449 RGBD images, 464 scenes). Every region is supported *from below* or *from behind* by a visible region, by a hidden one, or is the ground. Regions get **structure classes**: ground / furniture / **prop** ("small objects that can be easily carried") / structure. The strong baseline is a plain rule: **a prop is supported from below by the region directly beneath it**, and furniture by the nearest floor. It scores **72.0 % (type-agnostic) / 57.7 % (type-aware)** on ground-truth regions, against 75.9 / 72.6 % for their joint LP. On *automatically segmented* regions everything falls to **45.8 / 41.4 %** (rules) and **55.1 / 54.5 %** (LP). The named failure is a **floor misclassification cascade**: a rug labelled as floor makes the walls and bed take it as their support [src: silberman].
- **ConceptGraphs** gets "a on b" from box overlap + MST + an LLM [src: conceptgraphs]. That is geometry proposing and language naming.
- **Our `hostgate`** is the Silberman "directly beneath" rule done in 3D: the camera ray meets a host footprint at the right height. It has the open-host refinement the rule lacks: a ray under a desk is a floor item.

**Lesson for z uncertainty.** Support beats raw z. An object's height from a 0.26–0.46 m camera looking up at a desk edge is poor (EDA309: a desk-top item gets certainty factor ≥ 0.15). Once the host is known, though, `z_base = host top` is known to the host's measured accuracy. So store **support as a link** (host id + part) **plus a z-interval**, and let the interval fall back to the host's top when the object's own z is weak. Where the link is uncertain, the object must be projected **as if it could be on the floor** (questionable, see §5.5), not dropped.

### 1.3 Persistence and staleness

Already covered on [[locate-object-from-last-known-position]]: a last-known position is a hint with growing covariance (SLiM: a noisy static prior made search *worse* than no prior), and records should store presence intervals and the observing viewpoint (Khronos, STAR). For projection this means: **a stale object's footprint must not be relaxed by its stored shape alone.** Relaxing (drive-under, drive-over) needs *current* sensed evidence. The rig already enforces this through the HeightEvidence clocks and `gone` (rule 15o).

---

## 2. How 3D is projected into a 2D navigation layer

| Method | Projection rule | Overhang / under-table handling | Identity? |
|---|---|---|---|
| **Nav2 voxel layer** | 3D voxel column → 2D. Only returns with `min_obstacle_height` (default 0.0) ≤ z ≤ `max_obstacle_height` (default 2.0) are marked. `mark_threshold` (default 0) is the "minimum number of voxels in a column to mark as occupied"; `unknown_threshold` (default 15) is the number of empty voxels for "unknown" [src: nav2-voxel] | set `max_obstacle_height` to the robot top and a table top is ignored. **The space under it is NOT required to be seen empty.** | none |
| **STVL** | separate height windows for marking (`min/max_obstacle_height`) and frustum clearing (`min_z/max_z`). Voxels decay (linear / exponential / persistent), and decay is faster outside the sensor frustum. Six RGBD cameras cut move_base CPU from 80–110 % to 20–50 % on a 5th-gen i7 [src: stvl] | same band rule | none |
| **nvblox** | 2D ESDF slice of obstacles between `esdf_slice_min_height` and `esdf_slice_max_height`. A forum fix for low boxes sets the band to **0.06–0.65 m** [src: nvblox-forum] | same | people/dynamic layers |
| **Hornung PR2 multi-layer** | octree → **per body-part layers** (base, spine+head, arms). A cell is free only if every height in its layer is free, occupied if one is, unknown otherwise. "**the table is only projected on the spine layer**" [src: hornung-multilayer] | arms over a table, base under it, as **different layers for different body parts** | none |
| **Elevation mapping / grid_map** | 2.5D: one elevation + variance per cell. Variance carries pose uncertainty, with Mahalanobis-gated fusion and ray-traced visibility cleanup. grid_map holds "any number of layers" and converts to OccupancyGrid / costmap_2d / OctoMap [src: elevmap, gridmap] | **cannot** represent an overhang (one height per cell). MLS / multi-layer is needed ([[tilting-2d-lidar-multiplane-capture]] §4b) | none |
| **Layered costmaps** (Lu et al.) | semantically separated layers combined in order. Built because a tilting laser's obstacles "at different heights could be inappropriately removed by clearing observations" in one monolithic map [src: lu-layered-costmaps] | — | context layers (proxemics) |
| **Nav2 keepout filter + vector objects** | **shapes (polygons, circles) with UUIDs**, added/removed at runtime (`AddShapes` / `RemoveShapes` / `GetShapes`), rasterised into an OccupancyGrid mask for the Keepout Filter [src: nav2-vector]. Filters can be toggled on and off | — | **yes, a UUID per shape**. The nearest Nav2 has to "objects in the costmap". |
| **NavPatch** (arXiv 2026-09) | a VLM at 0.2 Hz names categories and an action: **ADD** (weakly sensed obstacle, e.g. a low cable), **REMOVE** (compliant object the geometry blocks, e.g. a curtain), **EXTEND** (needs a keep-out larger than its footprint, e.g. a cone). Evidence is accumulated (quality ≥ 0.40, a 1.5 s window, commit at E ≥ 1.0) into **2D cell patches overlaid on the costmap** at 5 Hz. 70 → 86 % success, false commits 68.4 → 40.7 % [src: navpatch] | none: 2D cells only, no height bands | by category |
| **Robot vacuums** (Roborock Saros 10 RetractSense) | LDS map + an **upward ToF range-finder** "to detect the height of low spaces"; the LiDAR turret retracts so the robot (7.98 cm) fits under [src: roborock] | **measure the underside directly, then decide**. This is the shipping version of our UNDER rule. | none |

**The universal rule:** project a return or shape **only if its z-interval intersects the body's height band**. Everyone does this, on *sensed points*. **Nobody in this list does it on object identity**, except Nav2 vector objects (2D only) and NavPatch (2D only).

**Where the rig is already stricter than the norm.** A Nav2 voxel layer with `max_obstacle_height` = 0.53 frees the floor under a table without asking whether the space below was *seen*. Our UNDER rule needs a measured underside ≥ 0.58 m from 2 stations *and* every band below seen empty by 2 stations. That is the [[robust-evidence-mapping-principle]] applied to the third dimension, and it should stay.

---

## 3. Task-conditioned map views

| Mechanism | What is conditioned | On what | Maintained or at query time |
|---|---|---|---|
| **VLMaps multi-embodiment** | which **categories** are obstacles: "a large mobile robot may need to navigate around a table … while a drone can directly fly over it". The union of the selected categories' masks is **intersected with the height-filtered projection O** (points with t1 ≤ z ≤ t2), which removes false obstacles on the floor [src: vlmaps] | the embodiment (fixed per robot) | **at query time** ("generated on the fly") from one shared map |
| **Hornung multi-layer** | which **height band** an obstacle lands in | the robot's body parts | maintained (projected down from the octree) |
| **MoveIt planning scene + ACM** | which **object pairs** are allowed to touch (e.g. gripper ↔ the target being grasped) | the current manipulation task | per planning request |
| **SayPlan / Taskography SCRUB** | which **subgraph / object set** reaches the planner. SCRUB is "guaranteed to produce a minimal sufficient object set" [src: taskography] | the task goal | at query time |
| **Clio** | which objects are **built at all**, and at what granularity: CLIP similarity to the task (α = 0.23) + agglomerative information bottleneck. 1,883 primitives → 49 objects; 71 % Spot grasp success on laptop compute. **Places and mesh are kept for every task** [src: clio] | a task list given up front | at build time |
| **Lu layered costmaps / Nav2 filters** | which **context layers** are active (proxemics, speed zones, keep-outs) | the situation | maintained, toggled |
| **NavPatch** | which **category actions** apply (add / remove / extend) | the scene + navigation rules | maintained overlay |

**Level of detail by task**, as practised: navigation needs footprints in the body band. Manipulation needs the target's full shape, its host's top surface and its near neighbours (MoveIt). Search needs *likely locations*, not geometry (SayPlan, [[locate-object-from-last-known-position]]). The pattern across all of them: **one persistent store; views are derived, and the derivation is cheap enough to do at request time.** The one thing nobody derives at request time is the **safety layer**. It is always maintained from sensors. Clio is the extreme case: it throws away objects that are irrelevant to the task, yet it still keeps the places/mesh layer for everything.

---

## 4. The proposed pattern vs the literature

### 4.1 The pattern, stated precisely

1. **Active floor map**: the live floor plan (walls, free / unknown, doors), the substrate.
2. **Object store**: every object known on that map (the bank), each with a 3D representation, a support relation and a confidence.
3. **Task-conditioned selection**: the objects *this* task needs (navigate to X, find X, check a questionable zone, look at desk-top items, later grasp X).
4. **Selective projection**: only the selected objects are written into the floor map. Each is written **by its 3D representation** (parts × z-intervals against the body band) and **by the current need for placement understanding** (a mug on the desk is irrelevant to driving under the desk but central to "look at the mug"; the desk's legs matter to driving, its top to looking).

### 4.2 Step by step: what typical systems do instead

| Step | Typical practice | Closest prior | How the human's step differs |
|---|---|---|---|
| 1. Floor map as substrate | Universal: a static layer / occupancy grid (Nav2 static layer, SLAM Toolbox, vacuum LDS maps) | Nav2 static layer; Hydra places | Same. Not new. |
| 2. Store of all known objects | Scene graphs (Hydra, ConceptGraphs, HOV-SG, DovSG, Khronos) | ConceptGraphs node = point cloud + bbox + caption, with "on" edges [src: conceptgraphs] | Same in kind. Ours adds per-object support with a z-interval and a re-ID template; ConceptGraphs' "on" is an LLM label, not a projection input. |
| 3. Task-conditioned selection | **Not done for navigation geometry.** Done for LLM context (SayPlan), symbolic planning (Taskography SCRUB) and map building (Clio) | **SayPlan** (task-relevant subgraph) and **Clio** (task-relevant objects) | They select to cut **tokens / planning time / map size**. The human selects to decide **what may change the planner's grid**, which is a different purpose. |
| 4. Projection by 3D shape and placement need | Maintained costmaps project **every sensed point** in a fixed height band with **no identity** (voxel layer, STVL, nvblox, elevation maps) | **VLMaps** (per-embodiment category lists → obstacle map, intersected with a height-filtered projection) [src: vlmaps]; **Hornung** (body-part height layers) [src: hornung-multilayer]; **MoveIt** (task-specific collision objects + ACM) [src: moveit-ps]; **Nav2 vector objects** (identity-tagged 2D shapes) [src: nav2-vector] | VLMaps conditions on the **embodiment**, not the task; on **categories**, not instances; and its height filter is one global band, not per-object parts. Hornung conditions on **body parts** with no identity. MoveIt is the full pattern **for manipulation** (a planning scene of chosen objects, per-task allowed contacts) but not projected into a floor map. Nav2 vector objects have identity but no height. |

### 4.3 Is it new?

**The parts are all known. The combination for floor navigation from an instance-level store is not a named pattern in what this search found.** The honest framing:

- In manipulation, it is **known as the MoveIt planning scene**: a task-curated set of collision objects with shapes, plus the allowed-collision matrix [src: moveit-ps].
- In navigation, the nearest named thing is **VLMaps' multi-embodiment obstacle maps** [src: vlmaps]. The human's pattern is that idea with *task* in place of embodiment, *instances* in place of categories, and *per-part z-intervals* in place of one height filter.
- The projection mechanics are **Hornung's multi-layer projection** [src: hornung-multilayer] and the **Nav2 voxel column rule** [src: nav2-voxel], applied to stored shapes instead of raw points.
- "Task-relevant subgraph" (SayPlan) and "task-driven scene graph" (Clio) are the established names for step 3, but in other uses.

So "**a task-conditioned planning scene for a mobile base**" or "**VLMaps-style on-the-fly obstacle maps, per task and per instance**" are fair names. Claiming it as a new paradigm would overstate it. Claiming it is standard practice would also be wrong: shipped navigation stacks do not do it (§2).

### 4.4 Pros and cons, with evidence

**Where task-conditioned projection wins**

- **Context-dependent clearance.** The desk is drive-under for "go to the far wall" and a host surface for "look at the mug". One maintained costmap must pick one answer. VLMaps exists precisely because a table is an obstacle for one robot and not for another [src: vlmaps]. Hornung shows the same table belonging to one body layer and not another [src: hornung-multilayer].
- **Clutter and false blocking.** Every relaxation this project has shipped (rules 15a–15r) exists because *projecting everything* blocked floor that was drivable (memories `keepouts-too-generous`, `beliefs-must-clear`). Projecting only what intersects the body band, and keeping off-band items (desk-top items) out of the floor grid by construction, removes a whole class of these. The z-blind bank disc (§0) is a live example.
- **Explainability.** Each blocked cell can name the object, the part and the reason ("desk leg, 0–0.72 m"). Nav2 vector objects carry UUIDs for this reason [src: nav2-vector]. The human's drivable-breakdown page (memory `drivable-breakdown-visuals`, one rule per cell) already depends on it.
- **Compute.** Small here (§1.1). Real for LLM planners (SayPlan, Taskography) and for large stores.

**Risks**

- **Safety by omission.** An obstacle left out of the task view is invisible to the planner. *Every* system in §2–3 that relaxes or curates keeps a **task-independent sensed layer**: Clio keeps the mesh and places for all tasks [src: clio]; VLMaps intersects category masks with the *sensed* height projection [src: vlmaps]; NavPatch overlays patches *on* the costmap, never in place of it [src: navpatch]. Rule: **selection may only remove cost that the sensed layer does not also assert.**
- **Staleness.** A stored shape describes the past. Using a stored desk's "open under" to free cells today is wrong if a box was pushed under it yesterday. Relaxing must be gated on **current evidence** (the UNDER rule's two stations, `seen_t`, `gone`).
- **Selection errors.** Taskography's SCRUB is "*minimal sufficient*" only because a symbolic problem can be checked [src: taskography]. A geometric "what matters here" cannot be proven sufficient, so selection must be **conservative by default**: include every object whose body-band projection touches the planning corridor.
- **Support errors.** Support inference is 41–55 % type-aware on real segmentations [src: silberman]. A mug wrongly put "on the desk" when it is on the floor under the desk would be dropped from the floor. So "on a host" may only *remove an object-store keep-out* where the sensed layer also shows the floor clear in the bands the object would occupy.

### 4.5 What must be true for it to be safe, and the minimal experiment

**Conditions:**

1. **A sensed safety layer, outside the task's control.** `HeightEvidence` body-band returns + the live guard + the visual trigger stamp the grid whatever the task view says. Task views *add* object footprints and may *relax* only cells that the sensed layer itself relaxes (UNDER / DRIVE-OVER / gone).
2. **Relaxing is evidence-gated, not shape-gated.** A stored part above the band frees nothing on its own. The floor under it is free only where the UNDER rule passed *this run* (or since the last return there).
3. **Uncertain support falls back to the floor.** An object whose support certainty is below a threshold is projected as a floor disc, **questionable** (rule 15h: plan through, check first), never certain and never dropped.
4. **Selection is conservative for navigation.** Every bank object whose body-band footprint lies within the planning region + `HARD_INVISIBLE_M` is included. Task-specific selection narrows only *non-navigation* layers (look targets, grasp scene).
5. **Every projection writes its reason** (object id, part, band, rule) for audit and for the live view.

**Minimal experiment (replay only):**

1. Take the 4 office worlds used by EDA311/315 and the real bank.
2. Add synthetic records: a mug **on the desk** (support host `obj-0012`, top), a mug **on the floor under the desk**, and a book on the bookshelf.
3. Build the planner grid three ways:
   - **A**, today: z-blind discs.
   - **B**, z-aware projection: support-on-host objects skipped *only where* the sensed layer shows those cells' floor bands clear; uncertain support kept as questionable.
   - **C**, B + task selection (navigate vs look-at-mug).
4. Report:
   - drivable m² and questionable m²;
   - the standing safety invariant: **0 freed cells within `HARD_M` of a current corroborated return / walls / large objects** (as EDA311/315 measure it);
   - that the floor-under-desk mug **still blocks** in B and C (because its LiDAR or camera evidence is in the body band), and the desk-top mug never blocks;
   - plan success across the desk.

Expected result: B frees the under-desk floor that A blocks with the desk-top mug, B and C keep the invariant, and C changes only the look-target layer.

---

## 5. Recommendation for our rover

### 5.1 Architecture: store → select → project → compose

```
data/objects (bank, record v2)                 sensed layer (task-independent, always on)
  shape: cuboid (outer) + parts[]                HeightEvidence per 4 cm cell x band
         part = {footprint, z_lo, z_hi,          + live guard + visual-trigger zones
                 kind: slab|leg|panel|body}      + floor plan (walls, unknown)
  support: {on: floor|host|wall|unknown,                     |
            host: obj-NNNN, part: top|shelf_k,               |
            z_base: [lo,hi], certainty, from}                |
  confidence / last_seen / permanence                        |
        |                                                    |
   select(task, region)  ── TaskView ──>  project(view, band=[0.06,0.58])
        |                                     per object, per part:
        |                                       part z-interval ∩ band = ∅  -> no floor cost
        |                                       on host & support certain   -> no floor cost
        |                                         (only where sensed bands below are seen clear)
        |                                       support uncertain           -> floor disc, QUESTIONABLE
        |                                       else                        -> footprint keep-out (tiers as today)
        v                                     every stamp carries (obj, part, band, rule)
   non-nav layers (look targets,                       |
   host-top items, grasp scene) <-- by task            v
                                       keepouts.py compose  ->  Navigator grid (unchanged contract)
```

- **Store.** Extend record v2 rather than add a store (rule 21: files).
  - `support` becomes a **structured field**: `on`, `host`, `part`, `z_base` interval, `certainty`, `from` (hostgate / human / floor-ray). It is written by `hostgate` at filing for small objects too, as it already is for collections.
  - `shape.parts` gives open hosts their real structure. For the desk: a top slab at the measured top, with legs/panels **only where LiDAR body-band returns were measured** under it. Until parts are measured, the class flag `host.open_under` + the HeightEvidence UNDER cells *are* the parts (do not invent legs).
- **Select.** One pure function `task_view(task, region, bank, world)`, a reader in `drone/world/` (rule 23: a leaf, like `bank.py`):
  - **navigation**: every object whose body-band footprint touches the region (conservative, §4.5 condition 4);
  - **find/look X**: X + its host + co-hosted neighbours as *look* layers;
  - **check questionable**: the questionable bodies in reach;
  - **later, grasp**: a MoveIt-style scene of X, its host top and its neighbours.
- **Project.** Replace `known_keepouts`' z-blind disc with `project(record, band, height_evidence)` following the rules in the diagram. Large objects stay evidence-projected as today. Bank cuboids never stamp cost; they only label cells (explainability) and seed re-ID.
- **Compose.** `keepouts.py` unchanged in contract. It receives the projected keep-outs with their `obj`/`part`/`rule` tags. **The sensed layer always wins** (§4.5 condition 1).
- **Live view.** The rover-service app shows the composed grid with **layer toggles**: sensed / bank-projected / task-view / questionable. Hovering a cell names the object, part, band and rule. Desk-top items are drawn as "on desk (0.75 m)", not on the floor. This is the human's "useful live view", and it reuses the drivable-breakdown idea (one rule per cell).

### 5.2 Cost and complexity

| Piece | Size | Risk |
|---|---|---|
| Structured `support` on small records + hostgate at filing | small: hostgate exists, the field is new (`schema.migrate`, additive) | support errors → mitigated by condition 3 |
| z-aware `project()` replacing the bank disc | small (~100 lines + tests) | must not free cells the sensed layer keeps → the EDA311/315 invariant test |
| `task_view()` selector | small for navigation (conservative = nearly everything in the region); medium for look / grasp layers | none for navigation, if conservative |
| Measured `parts` for open hosts (desk legs from body-band returns) | medium: segment a host's evidence cells by band | parts from one run are partial → keep as evidence, not truth |
| Live-view layers + per-cell reasons | medium (app work) | none to safety |

### 5.3 What to prototype first

**The z-aware bank projection, as an EDA in replay (the §4.5 experiment), behind a flag** (e.g. `keepouts.BANK_SUPPORT_Z`):

1. a structured `support` field filled by `hostgate` for small records;
2. `known_keepouts` skips a host-supported, support-certain small object **only where** `HeightEvidence` shows the floor bands under its disc seen clear, and stamps it questionable otherwise;
3. the replay battery with the synthetic desk-top / under-desk mugs and the standing 0-freed-cells invariant.

It is the smallest change that fixes the human's concrete example, and it tests the pattern's safety condition directly. The task selector and the live-view layers come after, once the projection rule is proven.

### 5.4 Open questions for the human

1. **Is a host-supported item ever a navigation concern?** For example, something overhanging the desk edge into the rover's band, or an item that could fall. Proposed: no, unless its own z-interval reaches below 0.58 m.
2. **Support certainty threshold.** Below what certainty does a desk-top item fall back to a questionable floor disc? Proposed: any support not confirmed from ≥ 2 stations or by the human.
3. **Parts for the desk.** Measure legs/panels from LiDAR body-band returns (automatic, partial), or let the human sketch them once in the app?
4. **Task views in the live view.** Should the app show the *current task's* view by default, or always the full composed grid with the task view as an overlay? Proposed: the full composed grid by default (safety-first), with the task view as a toggle.
5. **Scope of selection.** Should non-navigation tasks (look/find) ever *add* floor cost, e.g. a standoff ring around a fragile item on the floor? NavPatch's EXTEND is the precedent [src: navpatch]. This links to collections' `care` properties.

---

## References

- [conceptgraphs] Gu, Kuwajerwala, Morin et al., *ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning*, ICRA 2024. https://arxiv.org/abs/2309.16650 (edge construction read in the HTML version)
- [clio] Maggio, Chang, Hughes, Trang, Griffith, Dougherty, Cristofalo, Schmid, Carlone, *Clio: Real-time Task-Driven Open-Set 3D Scene Graphs*, arXiv:2404.13696. https://arxiv.org/abs/2404.13696
- [khronos] Schmid, Abate, Chang, Carlone, *Khronos: A Unified Approach for Spatio-Temporal Metric-Semantic SLAM in Dynamic Environments*, RSS 2024. https://arxiv.org/abs/2402.13817
- [sayplan] Rana, Haviland, Garg, Abou-Chakra, Reid, Suenderhauf, *SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning*, CoRL 2023. https://arxiv.org/abs/2307.06135
- [sayplan-site] SayPlan project page (expand/contract API, Dijkstra path planner). https://sayplan.github.io/
- [taskography] Agia, Jatavallabhula, Khodeir, Miksik, Vineet, Mukadam, Paull, Shkurti, *Taskography: Evaluating robot task planning over large 3D scene graphs*, CoRL 2021 (PMLR 164). https://arxiv.org/abs/2207.05006
- [vlmaps] Huang, Mees, Zeng, Burgard, *Visual Language Maps for Robot Navigation*, ICRA 2023, §III-C (multi-embodiment obstacle maps). https://arxiv.org/abs/2210.05714 (PDF read)
- [moveit-ps] MoveIt 2 docs, *Planning Scene* tutorial (Allowed Collision Matrix). https://moveit.picknik.ai/main/doc/examples/planning_scene/planning_scene_tutorial.html
- [silberman] Silberman, Hoiem, Kohli, Fergus, *Indoor Segmentation and Support Inference from RGBD Images*, ECCV 2012, Table 2. https://cs.nyu.edu/~fergus/datasets/indoor_seg_support.pdf (PDF read)
- [nav2-voxel] Nav2 docs, *Voxel Layer* parameters. https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/core_servers/costmap_2d/costmap_plugins/voxel/
- [stvl] Macenski, *spatio_temporal_voxel_layer* README. https://github.com/SteveMacenski/spatio_temporal_voxel_layer
- [nvblox-forum] NVIDIA developer forum, *Issues with nvblox layer in nav2 costmap* (esdf_slice_min/max_height). https://forums.developer.nvidia.com/t/issues-with-nvblox-layer-in-nav2-costmap/308347
- [nav2-vector] Nav2 docs, *Navigating with Vector Objects* (AddShapes / RemoveShapes / GetShapes → Keepout Filter mask). https://docs.nav2.org/rolling/tutorials/general_tutorials/navigation2_with_vector_objects/navigation2_with_vector_objects/
- [elevmap] ANYbotics, *elevation_mapping* README. https://github.com/ANYbotics/elevation_mapping
- [gridmap] ANYbotics, *grid_map* README. https://github.com/ANYbotics/grid_map
- [navpatch] Sun, Tao, Wang, Wang, Chen, *NavPatch: Evidence-Guided Object-Level Costmap Correction with Vision-Language Models*, arXiv:2609.14543 (2026-09). https://arxiv.org/abs/2609.14543 (HTML read)
- [roborock] Roborock newsroom, *Roborock Saros 10 … RetractSense Navigation System* (upward ToF range-finder for low-space height). https://newsroom.roborock.com/gl/news/roborock-launches-roborock-saros-10-ultra-slim-robotic-vacuum-flagship-with-retractsense-navigation-system
- [hornung-multilayer], [lu-layered-costmaps]: see [[tilting-2d-lidar-multiplane-capture]] References (read first-hand there).
