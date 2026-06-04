# World-Model Architecture — the map form factor for a home-tidy robot

**What is the "best form factor for the map" for our prototype — how it stores dynamic objects and
updates itself as the environment changes?** This page answers that design question. It is the
**form-factor / world-model design page**: it takes what the prototype has *proven* (a metric
relocalization anchor + a per-instance object memory) and lays out the **layered world model** that
turns "a map for localizing" into "a map for tidying."

It builds on, and does not repeat:
[[anchor-map-protocol]] (how to *build* the anchor), [[relocalization-method-bakeoff]] (which
front-end won), [[object-fingerprint-memory]] (the per-instance re-ID bank),
[[scene-graph-world-model]] + [[dynamic-object-handling]] + [[semantic-object-memory]] (the design-space
research), and [[system-architecture]] (where this sits in the full stack — the WORLD MAP subsystem).
Grounded in `drone-prototype/docs/eda-mapping-state.md` and EDA003–009.

> **This is a design/research artifact, not a settled spec.** The form-factor call is the human's /
> product-owner's. The **Open decisions for the human** section at the bottom flags what still needs a
> ruling; everywhere else, *proven* and *speculative* are kept separate.

---

## TL;DR

- **A home-tidy map is not one map — it's a layered world model.** A tidy robot must *locate itself*,
  *know where objects are*, *notice when they move*, and *plan a tidy*. No single representation does
  all of that well. The right form factor is **three layers with different update rates**: a slow
  **structural/anchor layer**, a fast-changing **object layer**, and an **update/change-detection
  mechanism** that reconciles them on revisit.
- **We have already proven two of the three layers in isolation** — they have just never been
  connected. The **hloc anchor** (metric-validated to ~2 % vs tape, EDA008) is the structural layer;
  **objmem** (DINOv2 per-instance re-ID, EDA007) is the object layer. The missing piece is **anchoring
  objmem instances into the map's metric frame** and adding the **revisit/change-detection loop**.
- **Dense volumetric (TSDF / per-point CLIP) is the wrong form factor for us** — our passive stereo is
  ~48 % depth-coverage and 4 GB GPU; dense semantic maps are memory-hungry and depth-hungry (see
  "Why not dense"). We want a **sparse-anchor + sparse-object-list (scene-graph-lite)** hybrid, which
  is exactly what our two proven artifacts already are.
- **The hard part is not storage — it's change over time:** data-associating an object seen today to
  the instance stored last week, and telling "it moved" apart from "I'm looking from a new angle / it's
  occluded / I'm slightly mislocalized." That is where the design risk concentrates (C2 in
  [[system-architecture]]). We say honestly where sparse passive stereo limits us.

---

## 1. How the map is put together TODAY (the proven foundation)

*(This is the crisp summary of `drone-prototype/docs/eda-mapping-state.md` — read that for the full
artifact inspection. Stated here so the architecture builds on fact, not aspiration.)*

The prototype produces **two geometric map artifacts, both built for localization, neither storing
objects or handling change**:

| Artifact | Built | Scale | What it is | Role |
|---|---|---|---|---|
| **hloc SfM model** (COLMAP `cameras/images/points3D.bin`) | offline batch | up-to-scale → **metric** once anchored | sparse 3D feature points (SuperPoint) + registered keyframe poses + LightGlue tracks | **The relocalization anchor** — `frame → 6-DOF pose` service. Reloc 93.6 % multi-sweep (EDA009) |
| **RTAB-Map `.db`** (SQLite) | online | metric (57.6 mm stereo baseline) | keyframes + poses + DBoW2 vocab + loop-closure graph + a 3D occupancy grid | **Nav substrate** — metric poses + (un-exported) traversability grid |

**Four facts that make the world model now buildable:**

1. **The anchor works and is reusable.** Build → save → fresh-load → relocalize runs end-to-end; the
   learned front-end clears the geometric-verification wall (0 % zero-inlier vs RTAB-Map's 88 %); pooled
   multi-sweep maps hit **93.6 %** cross-session reloc ([[relocalization-method-bakeoff]],
   [[anchor-map-protocol]]).
2. **The anchor is METRIC and validated.** hloc SfM × scale 0.833 recovers room width **−1.9 % vs
   tape-measured GT** (EDA008). *This is the enabling fact for the object layer*: an object's stereo
   depth can now be placed in the map frame in **real metres**, not arbitrary SfM units.
3. **A per-instance object memory exists and works** — but standalone. objmem segments → embeds
   (DINOv2 ViT-S/14, 384-dim) → re-IDs an object across views (recall@P=1.0 0.58→0.96 with DINOv2,
   EDA007). It stores {id, embedding(s), metric dims, provenance} per instance ([[object-fingerprint-memory]]).
4. **The gap is the connection.** objmem instances have **no pose in the map frame** — today it is a
   flat instance database with no spatial anchor and no notion of "this object moved." Both maps are
   **static + geometric**. A home-tidy world model needs objects *and* change. That is what the rest of
   this page designs.

---

## 2. The recommended form factor — a layered world model

The home-tidy task decomposes into four jobs — *locate self*, *know where objects are*, *notice
movement*, *plan a tidy* — that change at radically different rates. Walls move ~never; a sofa moves
monthly; a cup moves hourly; a pet moves by the second. **Bind things that change at the same rate into
the same layer, and you stop rebuilding the slow stuff every time the fast stuff moves.** This is the
central form-factor decision, and it matches the [[system-architecture]] §1 tripartition
(permanent / movable / living) and iRobot's production lesson (keep the semantic layer separate from
geometry, [[dynamic-object-handling]]).

```
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  LAYER 3 — UPDATE / CHANGE-DETECTION  (runs on every revisit; §4)             │
  │  relocalize → re-detect → data-associate → classify add/moved/removed → version │
  │            ▲ writes/versions ▼                         ▲ reads pose ▼            │
  ├────────────┴───────────────────────────┬──────────────┴───────────────────────┤
  │  LAYER 2 — SEMANTIC OBJECT LAYER        │  LAYER 1 — STRUCTURAL / ANCHOR LAYER  │
  │  (objmem instances, map-frame poses)    │  (the proven hloc anchor + grid)      │
  │  changes: hourly–daily                  │  changes: rarely (re-map on big change)│
  │                                         │                                       │
  │  per instance:                          │  • hloc SfM: sparse feature points +  │
  │   {instance_id,                         │    keyframe poses  → frame→pose        │
  │    map_pose (x,y,z[,R]) METRIC,         │  • metric scale 0.833 (EDA008)        │
  │    dinov2_embedding(s) (384-d),         │  • RTAB occupancy grid → traversability│
  │    metric_dims (w,h,d,conf),            │    (for Nav2 path planning)           │
  │    category, last_seen_ts,              │                                       │
  │    confidence, state,                   │  DEFINES THE COORDINATE FRAME every    │
  │    belongs_location (tidy target)}      │  object pose is expressed in.          │
  └─────────────────────────────────────────┴───────────────────────────────────────┘
            │ live frame → pose            ▲ metres
            ▼                              │
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  LAYER 0 — LIVE / EPHEMERAL  (never persisted; safety-critical)               │
  │  people, pets, the robot itself, things moving NOW → costmap only, decayed     │
  │  ([[dynamic-object-handling]] STVL / object-oriented grid; never written to L2) │
  └──────────────────────────────────────────────────────────────────────────────┘
```

### Layer 1 — Structural / relocalization anchor *(PROVEN — reuse as-is)*

The proven hloc anchor, plus the RTAB occupancy grid for traversability. **This layer defines the
coordinate frame**: every object pose in Layer 2 is `T_map_object`, expressed in the anchor's metric
frame. It changes rarely — you do **not** rebuild it when a cup moves; you rebuild it only on a
structural change (furniture rearranged, room added), per the iRobot reject-and-revert pattern
([[dynamic-object-handling]] lifelong). Build recipe: [[anchor-map-protocol]] (multi-sweep pooling).

Open productization gaps carried from the anchor work (not new): the front-end is offline-batch (→ put
SuperPoint+LightGlue under RTAB-Map's online back-end), uses research-only weights (→ DISK/ALIKED), and
the occupancy grid must be **exported on every build** (EDA008 found it NULL).

### Layer 2 — Semantic object layer *(half-proven — objmem exists; anchoring is NEW)*

objmem, but each instance now carries a **metric pose in the Layer-1 frame**. This is the connection
that EDA008 unlocked. One instance record (extending the [[object-fingerprint-memory]] schema with the
**bold** fields):

```jsonc
{
  "instance_id": "obj_0007",
  "map_pose":     {"xyz_m": [2.31, 0.42, 1.05], "frame": "hloc_map_v3", "cov": 0.18},  // NEW — metres in anchor frame
  "embeddings":   [[...384...], ...],          // DINOv2, multi-view (re-ID key)
  "metric_dims":  {"w": 0.11, "h": 0.12, "d": null, "conf": 0.46},  // conf = mask depth-coverage
  "category":     "mug",
  "last_seen_ts": 1717..., "confidence": 0.9,
  "state":        "present",                   // NEW — present | moved | removed | uncertain
  "version":      3,                           // NEW — bumped by Layer-3 on each change
  "belongs_location": "blue toy bin",          // tidy target (LLM/Housekeep prior; stubbed)
  "history":      [ /* {ts, pose, state, grasp_outcome} */ ]   // NEW — append-only audit trail
}
```

**How a detection gets a map-frame pose** (the new mechanic, all from proven pieces):

```
live frame ──┬─► hloc relocalize ───────────────► T_map_camera  (6-DOF, metres; Layer 1)
             └─► objmem segment+embed+depth ─────► object: crop, embedding,
                                                   object_centroid in CAMERA frame (metres,
                                                   from stereo depth × mask; objmem already does this)
                          compose:  T_map_object = T_map_camera · object_centroid_camera
                                   ─────────────────────────────────────────────
                                   object now has a METRIC pose in the map frame
```

Both halves already run in the prototype — the only new code is the compose step and storing the pose.
This is a **scene-graph-lite** representation: an object *list* with metric poses + per-instance
identity, **not** a dense per-point semantic field. It is the cheap, sparse-stereo-appropriate cousin of
ConceptGraphs' object nodes ([[scene-graph-world-model]]) — we keep their {id, centroid, extent, tag}
node and add our DINOv2 **instance** fingerprint (which ConceptGraphs/Hydra lack — they track category,
not instance, [[semantic-object-memory]] §"Instance-level fingerprinting").

### Layer 0 — Live / ephemeral *(design rule, not a datastore)*

People, pets, the robot, anything moving now: **detect live, feed the costmap, never persist to Layer 2**
([[system-architecture]] §1; [[dynamic-object-handling]] fast-dynamic = STVL/object-oriented grid). The
form-factor rule: *only slow-moving objects (toys, cups, remotes) get a fingerprint; fast movers never
do.* Keeps Layer 2 from filling with ghosts of a walking person.

### Why NOT dense volumetric / per-point semantic (the form-factor rejection)

The literature's richest maps are dense — TSDF meshes (Hydra/Kimera), per-point CLIP fields
(ConceptGraphs dense variant), 3DGS. **They are a poor fit for our regime, and here is why:**

| Dense approach | Why it fails *our* constraints |
|---|---|
| TSDF / occupancy-dense mesh | Needs dense, reliable depth. Our passive stereo is **~48 % coverage** on indoor surfaces (blank walls/low-texture starve it). A TSDF over half-missing depth is full of holes — fine as a coarse Nav grid (RTAB already gives that), useless as the *object* representation. |
| Per-point CLIP semantic field | Memory blows up with map size ([[semantic-object-memory]] key gap; survey flags memory as the #1 unsolved issue). On **4 GB GPU** this is a non-starter at multi-room scale. |
| 3DGS semantic SLAM | Photoreal + heavy; research-stage; needs good depth/coverage we don't have. |

**Our sparse passive-stereo regime *wants* a sparse representation**, and we already have the two right
ones: a **sparse feature anchor** (localization) + a **sparse object list** (semantics). The scene-graph
research is the right *design pattern* (hierarchy, language-queryable nodes, local updates); we adopt the
pattern at the **sparse, instance-fingerprint** end of it, not the dense end. This is also why
**Tag Map** / **HOV-SG** (orders-of-magnitude smaller than dense maps, [[semantic-object-memory]]) are the
relevant references for us, not dense ConceptGraphs.

---

## 3. The object-storage model (how dynamic objects live in the map)

Pulling the storage decisions together:

- **One record per physical instance**, keyed by `instance_id`, re-identified by **max-cosine over
  multi-view DINOv2 embeddings** (proven, [[object-fingerprint-memory]]). Two identical red balls are
  two records — instance identity is the whole point for tidy (different owner / target bin / grasp
  history).
- **Pose is metric, in the anchor frame**, with a covariance/confidence (compounded reloc error +
  stereo-depth error). Stored as `T_map_object`; **decoupled from the anchor** so the anchor never gets
  rewritten when an object moves (the layer-separation payoff).
- **Store is sqlite (metadata + pose, queryable by room/owner/category/state) + a vector index**
  (brute-force at 100s of objects, hnswlib/FAISS at 1000s+) — exactly objmem's current design, plus the
  pose/state/version columns. Crops as PNGs.
- **Confidence decays with time-since-last-seen** ([[system-architecture]] §1 staleness;
  [[dynamic-object-handling]] POCD stationarity score). An object not re-observed stays on the map with
  *decaying* confidence rather than vanishing — so the robot can still go look for it, but knows the
  belief is stale.
- **History is append-only** (audit trail of pose/state/grasp outcomes) — this is what makes the record
  *compound with use* (objmem's design intent) and gives tidy-planning the grasp-difficulty prior.
- **`state` ∈ {present, moved, removed, uncertain}** is set by Layer 3, not at enrollment.

**Serving the tidy task** directly from this store:
- *Locate objects* → query by category/owner/`belongs_location`; return `map_pose` → Nav2 goal on the
  Layer-1 grid.
- *Detect movement* → Layer 3 sets `state=moved` and bumps `version` (next section).
- *Plan a tidy* → "objects where `map_pose` ≠ `belongs_location`" = the to-tidy list (the Housekeep/
  RoboTidy framing, [[semantic-object-memory]]); each carries grasp history from `history`.

---

## 4. The update / change-detection mechanism (how the map updates itself)

This is the home-tidy crux and the hardest part. The mechanism runs **on every revisit** (cadence
below) and is a direct adaptation of **POCD between-session change detection**
([[dynamic-object-handling]]) to our sparse-stereo, instance-fingerprint world model:

```
ON REVISIT (per region the robot re-enters):
  1. RELOCALIZE         hloc → T_map_camera         (Layer 1; the frame is fixed & trusted)
  2. RE-DETECT          objmem segment+embed+depth → live object set with map-frame poses (§2)
  3. DATA-ASSOCIATE     match live objects ↔ stored instances by a JOINT cost:
                          embedding cosine (identity)  +  map-pose distance (geometry)
                          +  category agreement.   (POCD uses ICP+Hungarian; we add the
                          DINOv2 embedding term — our identity signal is stronger than POCD's.)
  4. CLASSIFY each stored instance in the current view frustum:
        matched, pose ≈ stored      → UNCHANGED   (refresh last_seen, fold view in)
        matched, pose moved > τ_move → MOVED       (update pose, state=moved, version++, history+)
        in-frustum but NOT detected  → REMOVED?    (decay confidence; only commit REMOVED after
                                                    N consecutive misses — guards occlusion)
        live object, no match        → ADD         (enroll new instance)
  5. VERSION & RECONCILE  write changes as a new map_version; keep history; never silently overwrite.
                          On a structural mismatch (the *scene*, not an object, changed) → flag for
                          Layer-1 re-map, reject-and-revert if inconsistent (iRobot pattern).
```

**Cadence.** Opportunistic + on-demand, not a fixed clock: (a) **opportunistically** whenever the robot
relocalizes through a region during any task — every pass is a free change-detection sweep; (b)
**on-demand** before a tidy task (re-scan target rooms so the plan is fresh); (c) a **periodic full
sweep** (the exploration/patrol mode, [[system-architecture]] M3) to catch changes in unvisited regions.
Fast movers (Layer 0) are never reconciled here.

**Reconciliation rules** (the policies that keep the map honest):
- *Confidence, not deletion.* A missed object decays; it is only marked `removed` after **N consecutive
  misses from viewpoints that should have seen it** — single-frame absence is occlusion until proven
  otherwise.
- *Geometry gate on identity.* A strong embedding match at an implausible distance is treated as
  *uncertain*, not an instant teleport — protects against re-ID false positives and reloc error.
- *Structural vs object change.* If many anchor features in a region fail to verify (not just objects
  missing), that is a *structural* change → Layer-1 concern (re-map), not a flurry of object updates.
  Disambiguating this is **C2 in [[system-architecture]]** ("lost vs world-changed") and is genuinely
  hard — see open problems.

---

## 5. Honest limits — what sparse passive stereo imposes (proven vs speculative)

**Proven (carry as fact):**
- The anchor + reloc + metric scale are real and measured (EDA003–009). Object→map-frame pose is
  mechanically available *today* (reloc pose ∘ stereo depth) — **the §2 compose step is the only
  un-built piece, and both its inputs are proven.**
- DINOv2 instance re-ID works on synthetic data; **multi-view max-cosine** is the right matcher
  ([[object-fingerprint-memory]]).

**Speculative / unproven (do NOT assert these as working):**
- **The whole Layer-3 loop is unbuilt and untested on real captures.** Data association *over time*,
  the moved/removed/occluded disambiguation, and the `τ_move` / N-miss thresholds are all designed here,
  not measured. POCD's 80 % precision / 3 % FPR (warehouse, dense RGB-D) is the *reference ceiling*, not
  our number.
- **Pose accuracy bounds change detection.** Reloc is consistent to ~⅓ m (EDA005/008). `τ_move` must sit
  *above* that error floor — so we can reliably detect "the cup moved 1 m," **not** "the cup shifted
  10 cm." Sparse stereo's pose noise sets a **minimum detectable motion**; small tidies may be invisible.
- **~48 % depth coverage** makes object poses noisy/absent on low-texture or distant objects (metric-dim
  `conf` already exposes this). Some objects simply won't get a trustworthy pose.
- **objmem is validated only on synthetic, colour-distinct objects** — the discriminating case (two
  same-category instances) is the pending real-capture validation (OBJMEM-7). Re-ID over a *real* home's
  visual change (lighting, clutter, partial views) is unmeasured.
- **No multi-room hierarchy yet.** This page designs the single-room object layer; rooms/floors
  (HOV-SG-style routing) are a later add.

---

## 6. Open decisions for the human / product-owner *(the form-factor call is yours)*

These are genuine forks, not things to settle in a research page:

1. **How rich does Layer 2 get — flat instance list vs full scene graph?** This page recommends
   **scene-graph-lite** (object list + metric pose + instance fingerprint), deferring rooms/relations
   hierarchy. A richer HOV-SG/Hydra hierarchy buys language-routed queries ("the cup in the kitchen") at
   real compute cost on 4 GB. *Decision: how much hierarchy is worth it for the prototype?*
2. **On-robot vs off-robot split.** [[system-architecture]] wants the anchor + a compressed grid on-robot
   (survives WiFi dropout) and the full object/semantic store off-robot (Command Center). *Decision:
   does the prototype keep one local store for now, or design the on/off split from the start?*
3. **Change-detection aggressiveness (the precision/recall dial).** `τ_move`, the N-miss-before-removed
   count, and re-map triggers trade false "it moved" alarms against missing real changes. A tidy robot
   that hallucinates moves is annoying; one that misses them leaves mess. *Decision: which way to bias —
   and is the iRobot reject-and-revert safety valve mandatory?*
4. **What is the next prototype step?** The cheapest high-value build is **anchor objmem into the map
   frame** (the §2 compose step) and demonstrate **one object placed in the metric map + one revisit
   detecting it moved**. That proves Layers 1+2 connected and the spine of Layer 3 on real data — the
   honest next milestone. *Decision: green-light that as the next prototype segment?*
5. **"Belongs location" / tidy target source.** The tidy plan needs a *where-it-belongs* prior
   (Housekeep/LLM). Out of scope to build now, but the schema reserves it. *Decision: is tidy-planning in
   scope for the prototype, or is "world model that knows what moved" the prototype's endpoint?*

---

## Related

[[anchor-map-protocol]] — how to *build* Layer 1 (multi-sweep recipe). ·
[[relocalization-method-bakeoff]] — why hloc is the anchor front-end. ·
[[object-fingerprint-memory]] — Layer 2's per-instance re-ID bank (schema + matcher). ·
[[scene-graph-world-model]] — the design-space (Hydra/ConceptGraphs/HOV-SG/DovSG); we adopt the
sparse end of it. ·
[[dynamic-object-handling]] — Layer 0/3 mechanisms (STVL, POCD, iRobot lifelong). ·
[[semantic-object-memory]] — parent; instance-fingerprint proposal + key gaps. ·
[[system-architecture]] — where this sits (WORLD MAP subsystem; §1 tripartition; C2). ·
[[map-then-navigate]] · [[home-tidy-drone-prototype]].

---

*Author: eda-scientist (design/architecture pass), 2026-06-04. Grounded in
`drone-prototype/docs/eda-mapping-state.md`, EDA003–009, `src/objmem/`,
`docs/object-memory-design.md`. Cites design-space research already in this wiki; no new external
research was needed — the gap was synthesis into a layered form factor, not new sources.*
