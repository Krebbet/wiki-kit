# 3D Scene Graph World Model

A 3D scene graph is a hierarchical spatial data structure that encodes a robot's environment as layered nodes — from raw geometry up through objects, navigable places, rooms, and buildings — connected by typed edges (spatial, semantic, topological). For a home service robot's server-side world brain, it is the right representation because: (1) it is structured and language-queryable (LLM planners consume JSON node lists; NL queries route via cosine similarity at each layer); (2) it is hierarchical (pruning search to a single room before scoring objects reduces false positives and context-window cost); (3) it supports dynamic updates without full reconstruction; and (4) it fuses metric geometry with semantic labels in a single representation. This page covers four reference systems — ConceptGraphs, Hydra, DovSG, and HOV-SG — and synthesises a recommended architecture for the home robot server brain.

## Source
- `raw/research/server-world-graph/01-conceptgraphs.md` — ConceptGraphs (arXiv 2309.16650, ICRA 2024)
- `raw/research/server-world-graph/04-hydra-foundations.md` — Foundations of Spatial Perception / Hydra (arXiv 2305.07154, IJRR 2024, MIT SPARK)
- `raw/research/server-world-graph/03-dovsg-dynamic.md` — DovSG (arXiv 2410.11989, RAL 2025)
- `raw/research/server-world-graph/02-hierarchical-scene-graph-nav.md` — HOV-SG (arXiv 2403.17846, 2024)

## Related
[[semantic-object-memory]], [[map-then-navigate]], [[dynamic-object-handling]], [[system-architecture]], [[ros2-nav2]], [[home-tidy-drone-prototype]], [[user-comms-layer]]

---

## Hierarchy structure

*(synthesis)* Two reference designs from the literature, both suitable for a home robot:

### Hydra — 5-layer graph [src: hydra-foundations]

| Layer | Nodes represent | Key attributes | Built from |
|---|---|---|---|
| 1 — Mesh | Metric-semantic 3D mesh | Each vertex carries semantic label | Voxblox TSDF active window (8 m radius); marching cubes |
| 2 — Objects/Agents | One node per object cluster | Centroid, bbox, semantic label, mesh vertices; agent node = VIO keyframe pose graph | Euclidean clustering on mesh vertices per semantic class |
| 3 — Places | Sparse free-space GVD graph | Each node = obstacle-free 3D location with radius; edges = traversable connections | GVD of TSDF brushfire; used directly for path planning |
| 4 — Rooms | One node per room | Centroid, bbox, semantic label (neural tree GNN) | Persistent homology on places graph + flood-fill; edges connect adjacent rooms |
| 5 — Building | Single anchor node | Mean of room centroids | Aggregated from room layer |

### HOV-SG — 4-layer graph [src: hierarchical-scene-graph-nav]

Root → Floor → Room → Object. Each level carries CLIP feature embeddings for cosine similarity matching. Floor detection by height histogram peak-finding (100% accuracy). Room segmentation by Watershed of BEV floor mask. Objects by SAM + CLIP pipeline.

*(synthesis)* For the home robot server brain: the Hydra 5-layer structure (with the places layer providing the navigable free-space graph) is the richer representation. HOV-SG's query routing architecture (next section) is the cleaner implementation.

---

## Building the graph — ConceptGraphs pipeline

Per-frame incremental build from posed RGB-D [src: conceptgraphs]:

1. SAM → class-agnostic 2D instance masks
2. CLIP image encoder → per-mask semantic feature vector (unit-normalized)
3. Depth projection → 3D point cloud per detection (DBSCAN denoised, 2.5 cm voxel)
4. Object association: geometric similarity (nearest-neighbour ratio, 2.5 cm threshold) + semantic similarity (cosine distance); greedy-assign if score > δ_sim=1.1, else new node
5. Object fusion: running-average CLIP feature; voxel-merge point clouds
6. (Post-hoc) LLaVA captioning on 10 best views per object → GPT-4 summarisation → per-node tag + caption
7. (Post-hoc) GPT-4 edge generation: for each MST pair, LLM derives spatial relationship label

Graph output: JSON list of nodes {object_id, bbox_center, bbox_extent, object_tag, caption} — ready for LLM planning queries [src: conceptgraphs]

### Graph accuracy [src: conceptgraphs]

| Metric | ConceptGraphs | Notes |
|---|---|---|
| Node precision | 0.71 | Human-rated on Replica |
| Edge precision | 0.88–0.91 | Notably higher than node precision |
| Open-vocab segmentation (mAcc) | 40.63% | vs ConceptFusion 24.16% |
| LLM negation retrieval R@1 | 0.80 | vs CLIP 0.26 |
| LLM affordance retrieval R@1 | 0.57 | vs CLIP 0.43 |

---

## Language query routing — HOV-SG pipeline

How "find the cup near the sofa in the kitchen" routes through the hierarchy [src: hierarchical-scene-graph-nav]:

1. **Parse:** GPT-3.5/4 converts NL query to structured triple [floor, room, object] via few-shot prompt
2. **Floor match:** CLIP embedding of floor token scored via cosine similarity against all floor nodes
3. **Room match:** CLIP embedding of room token scored against the 10 representative view embeddings of each room on the selected floor; max-cosine wins
4. **Object match:** CLIP embedding of object token scored against all object nodes within the selected room
5. **Navigate:** Object node 3D centroid → Voronoi action graph → path to goal

**Why the hierarchy helps:** without it, all objects across all floors are scored simultaneously (hundreds of candidates). With it, the search is pruned to tens of objects in one room. [src: hierarchical-scene-graph-nav]

**Localization within graph:** particle filter scores current RGB CLIP features against room view embeddings; converges in ~10 frames [src: hierarchical-scene-graph-nav]

### HOV-SG navigation results [src: hierarchical-scene-graph-nav]

| Environment | Query type | Success rate |
|---|---|---|
| HM3DSem simulation | (object, room, floor) | 37.32% |
| HM3DSem simulation | (object, room) | 40.41% |
| Boston Dynamics Spot, real office | Object navigation | 56.1% |
| Boston Dynamics Spot, real office | Room navigation | 55.6% |
| Boston Dynamics Spot, real office | Floor navigation | 100% |

*(synthesis)* Floor routing is solved. Room routing is ~55%. Object routing in a known room is ~56–40%. These numbers establish the current capability floor for a home robot.

---

## Dynamic updates — DovSG

When the environment changes, DovSG updates only the local subgraph rather than rebuilding the full graph [src: dovsg-dynamic]:

**4-stage local update:**
1. Relocalize: ACE scene-specific MLP → coarse global pose → LightGlue feature matching → colored ICP → precise transform
2. Remove stale voxels: reproject each stored voxel; delete if depth or color deviates beyond threshold
3. Update low-level memory: new RGB-D frames → Recognize-Anything → Grounding DINO → SAM2 → CLIP → DBSCAN → fuse into object set
4. Update scene graph: diff old vs new object set → remove affected node edges → recompute spatial relationships for changed region only

**Performance [src: dovsg-dynamic]:**

| Metric | DovSG | ConceptGraphs | Ok-Robot |
|---|---|---|---|
| Local update time (40 m², 1200 frames) | 1 min | 27 min | 20 min |
| Memory (40 m², 1 cm voxels) | 0.15 GB | 0.15 GB | 2 GB |
| Scene change detection accuracy | 94–95% | — | — |
| Long-term task success | 35% | — | 5% |

*(synthesis)* The 27× speedup over full reconstruction makes incremental updates feasible on an always-on home server. The 35% long-term task success vs 5% baseline confirms that local graph maintenance is load-bearing for multi-session operation.

---

## Compute requirements

Table from all four papers [src: conceptgraphs, hydra-foundations, dovsg-dynamic, hierarchical-scene-graph-nav]:

| System | Required models | Hardware tested | Mapping speed | Online? |
|---|---|---|---|---|
| ConceptGraphs | SAM, CLIP, LLaVA-7B, GPT-4 (API) | Jackal + offboard desktop for captioning | Offline captioning; incremental association | Partial |
| Hydra | MobileNetV2 or HRNet (segmentation), GTSAM | Xavier NX onboard (1 Hz) | ~5 Hz TSDF; ~1 Hz graph | Yes — Xavier NX |
| DovSG | RAM + Grounding DINO + SAM2 + CLIP + ACE + LightGlue + GPT-4o (API) | xARM6 + Agilex mobile base | Offline initial; 1 min local update | Partial |
| HOV-SG | SAM ViT-H, CLIP ViT-H-14, GPT-3.5 (API) | Boston Dynamics Spot + workstation | Offline batch | No |

Note: every system requires a GPU-class machine for the vision models. HOV-SG and ConceptGraphs require cloud LLM API calls for parsing/captioning. Hydra is the only fully onboard real-time system — but room classification accuracy is lower (27–47%) [src: hydra-foundations].

---

## Practical limitations for home deployment

*(synthesis)* Table of known failure modes across all four systems:

| Limitation | Which systems | Mitigation |
|---|---|---|
| Open floor-plan room segmentation fails | Hydra, HOV-SG | Fiducial room markers OR manual room annotation |
| Room classification accuracy low (~27–47%) | Hydra | Use HOV-SG's view-embedding approach (73–84%) instead |
| Offline mapping only | HOV-SG, ConceptGraphs (partial) | Use Hydra for live mapping; add CG-style features as post-hoc layer |
| Cloud API dependency (GPT-4/GPT-3.5) | ConceptGraphs, DovSG, HOV-SG | Local LLM (Llama-3, Mistral) for query parsing; OpenAI API for offline captioning |
| Context window bottleneck at scale | ConceptGraphs | Hierarchical routing (HOV-SG) prunes context before LLM sees it |
| Static scene assumption | ConceptGraphs, HOV-SG | Layer DovSG's local update mechanism on top |
| Long-term task SR still low (35–56%) | All | Active research gap; establish baseline before expecting production quality |

---

## Implications for the project

*(synthesis)* Recommended server world brain architecture, combining the best of each system:

1. **Hydra for live mapping layer:** run onboard or on home server; builds mesh + objects + places in real-time. Use MobileNetV2 for segmentation on Jetson. Provides the navigable places graph and object-level nodes.
2. **HOV-SG hierarchy for query routing:** floor → room → object → Voronoi path. The query decomposition (NL → GPT parse → cosine similarity at each level) is the routing engine for [[user-comms-layer]] voice commands.
3. **DovSG local update for dynamic maintenance:** when robot detects a change (object missing, object moved), trigger a local subgraph update. 1-min latency for a room-sized area.
4. **ConceptGraphs JSON schema for LLM interface:** the {object_id, bbox_center, bbox_extent, object_tag, caption} schema is directly usable as the COMMAND CENTER's world-state serialisation for LLM task planning.

See [[system-architecture]] workstream B (server world view) and [[map-then-navigate]] for the exploration phase that populates the graph.
