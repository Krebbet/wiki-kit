# Semantic Mapping & Object-Location Memory

Semantic object-location memory is a persistent spatial representation that encodes not only *where objects are* but *where they belong* — the cognitive substrate for instructions like "tidy the toys" or "return the mug to the kitchen." The dominant architecture is the 3D scene graph: a layered structure linking geometry, objects, rooms, and buildings, queryable by language. Open-vocabulary CLIP-fused variants (ConceptGraphs, HOV-SG) extend this to arbitrary object classes without retraining; 3D Gaussian Splatting (3DGS) semantic SLAM is emerging as a photorealistic alternative. Nearly all mature results come from ground robots; aerial deployment of full semantic graphs has one published end-to-end demo.

---

## State of the art

**3D scene graphs — ground-robot results (drone-relevance by transfer)**

- *demoed* **Hydra** (MIT SPARK, 2022) builds a real-time hierarchical 3D scene graph (mesh → places → rooms → buildings) incrementally from visual-inertial input using a local ESDF and persistent homology room segmentation *(corrected 2026-06-01 from journal paper arXiv:2305.07154 — the RSS 2022 conference paper used community detection; the IJRR 2024 journal version uses persistent homology on the places graph + flood-fill)*; loop-closure corrects all layers simultaneously via embedded deformation graphs; evaluated in apartment, office, and subway environments. **Ground-robot.** [`01-arxiv-2201-13360`]

- *demoed* **Kimera-Multi** (MIT SPARK, 2021) extends metric-semantic SLAM to multi-robot teams; each agent builds a local semantic mesh; distributed graduated non-convexity merges maps under limited bandwidth; evaluated on outdoor ground-robot trajectories up to 800 m per robot; produces globally consistent semantic 3D mesh. **Ground-robot.** [`02-arxiv-2106-14386`]

**Open-vocabulary CLIP-fused 3D scene graphs — ground-robot results (drone-relevance by transfer)**

- *demoed* **ConceptGraphs** (multi-institution, 2023) fuses class-agnostic 2D instance masks into a 3D graph enriched with CLIP/LLM-generated language tags and spatial relations; no 3D dataset fine-tuning required; enables natural-language pick-and-place and traversability queries on wheeled and legged robots. **Ground-robot.** [`03-arxiv-2309-16650`]

- *demoed* **HOV-SG** (Freiburg/UTN, 2024) adds a three-level hierarchy (objects → rooms → floors) to open-vocabulary 3D mapping; achieves 75% reduction in representation size vs. dense open-vocabulary maps; demonstrated on language-conditioned navigation in real multi-story buildings. **Ground-robot.** [`04-arxiv-2403-17846`]

- *demoed* **Tag Map** (ETH RSL, CoRL 2024) replaces embedding-heavy maps with a text-tag database built from large image-classification models; matches open-vocabulary map localization precision/recall at two-to-four orders of magnitude less memory; grounds an LLM for conversational object retrieval on a real robot. **Ground-robot.** [`11-arxiv-2409-15451`]

**3DGS semantic SLAM — ground/lab results (drone-relevance by transfer)**

- *demoed* **Go-SLAM** (Purdue/ARL, 2024) assigns per-Gaussian object identifiers via Grounding DINO + SAM; supports open-vocabulary natural-language object queries; runs PRM path planning to queried 3D coordinates; shows 17–35% IoU gains over baselines in lab scenes; Figure 1 explicitly depicts a drone navigating to a queried object. **Primarily ground/lab; drone shown in figure but full aerial validation not reported.** [`05-arxiv-2409-16944`]

**Aerial scene-graph result — the one directly aerial paper**

- *demoed* **UAV VSLAM + Situational Graphs** (SnT Luxembourg, 2024) integrates a marker-assisted VSLAM framework onto a real RGB-D UAV; reconstructs indoor maps enriched with corridors, rooms, doors, and walls as a multi-layered situational graph in GPS-denied environments; validated in real indoor flights. **Aerial — direct result, not transfer.** Object-category vocabulary is limited to fiducial-marker-labeled structural elements, not arbitrary household objects. [`09-arxiv-2402-07537`]

**"Where things belong" benchmarks and LLM task planning — ground-robot results (drone-relevance by transfer)**

- *demoed* **Housekeep** (Georgia Tech/Meta AI, 2022) benchmark: embodied agent must tidy a simulated house by inferring misplaced objects *without explicit goal specification*, using a dataset of 1,799 objects across 268 categories, 585 placements, 105 rooms from 372 annotators; LLM-fine-tuned planner generalizes to unseen objects. Establishes the commonsense "where things belong" ground truth needed for autonomous tidying. **Simulation/ground.** [`07-arxiv-2205-10712`]

- *demoed* **RoboTidy** (HUST/HKU, 2025) benchmark: 500 photorealistic 3DGS household scenes, 6.4k manipulation + 1.5k navigation trajectories; formalizes tidying as an Action(Object, Container) list parsed by a VLM; real-world bimanual mobile robot validated; VLN success markedly lower than R2R, underlining difficulty. **Ground-robot sim-to-real.** [`08-arxiv-2511-14161`]

- *demoed* **LLM Memory-Augmented Household Agent** (TU Wien/AIT, 2025) combines Grounded SAM + LLaMA-3.2-Vision for object detection, RAG for persistent object-location memory across sessions, and a three-agent LLM orchestration (routing / planning / knowledge-base); Qwen2.5 best on specialized agents; evaluated in three real household scenarios; avoids explicit scene-graph maintenance in favor of language-only memory. **Ground-robot.** [`10-arxiv-2504-21716`]

**Survey**

- *claimed* Semantic mapping for indoor embodied AI survey (SFU, 2025) identifies the field's trajectory toward open-vocabulary, queryable, task-agnostic maps while flagging high memory demands and computational inefficiency as the primary unresolved challenges. [`06-arxiv-2501-05750`]

---

## Instance-level object fingerprinting *(architectural proposal)*

The existing scene-graph literature (Hydra, ConceptGraphs, HOV-SG) tracks object *categories* and *locations* but does not maintain per-instance identity across sessions. A stronger architecture for the home-tidy use case:

**Discovery phase:** when the drone first encounters an object, run a lightweight visual embedding model (candidates: DINOv2, SigLIP, MobileNet-class) on the RGB crop. Store the embedding vector as the object's **fingerprint** alongside its properties: estimated location, category label, grasp history, difficulty notes, "belongs to" assignment, last-seen timestamp.

**Operations phase:** when the drone observes an object in real time, embed it and run nearest-neighbour search against the fingerprint library. A match retrieves all accumulated properties for that specific instance — not just its category. Example: "this is the round red ball from Charlie's room; previous attempts found it hard to grasp because it rolls; it belongs in the blue toy bin."

**Why this matters over category-only memory:**
- Two identical-looking objects (two red balls) can have different ownership, location, and grasp history
- Properties from prior inspections (weight estimate, surface texture, graspability, known difficulty) improve real-time execution without re-learning
- The library compounds over time: each successful or failed grasp enriches the record for that instance

**Implementation sketch:**
- Embedding model: DINOv2-small or SigLIP-base — both run on Jetson Orin NX at real-time rates
- Vector store: FAISS (CPU, in-memory for a household-scale library of ~1k–10k objects) or SQLite-vec
- Properties record: JSON blob per object (category, room, bin/destination, grasp_attempts, grasp_success_rate, difficulty_notes, owner)
- Sync: fingerprint library lives in the COMMAND CENTER; a compressed "working set" for the current room is pushed to IMMEDIATE TASK LOAD before each task

This is complementary to scene-graph approaches (Hydra, ConceptGraphs): the scene graph tracks spatial relationships; the fingerprint library tracks per-instance identity and accumulated experience. See [[system-architecture]] (COMMAND CENTER, WORLD MAP) and [[home-tidying-robots]] (TidyBot personalisation — category-level; this extends to instance-level).

See [[scene-graph-world-model]] for a full technical deep-dive on both systems plus DovSG (dynamic updates) and HOV-SG (query routing architecture).

## Key gaps

- **Memory and compute cost at scale.** Dense open-vocabulary maps (per-point CLIP embeddings) do not scale to large or multi-room environments; Tag Map reduces storage by orders of magnitude but loses relational structure. No method cleanly solves the memory-vs-richness tradeoff for a resource-constrained drone. [`06-arxiv-2501-05750`; `11-arxiv-2409-15451`]

- **Aerial deployment unproven for semantic graphs.** The single aerial scene-graph paper (2402.07537) relies on fiducial markers and does not support arbitrary object categories. ConceptGraphs/HOV-SG class results exist only on ground robots; transfer to a moving, vibrating, compute-limited UAV is unvalidated.

- **Sim-to-real gap for tidying.** RoboTidy reports VLN success rates "markedly lower" than standard navigation benchmarks even in simulation; real-world transfer of full tidy pipelines (detect misplaced → infer correct location → plan pick-and-place) has not been shown on any aerial platform. [`08-arxiv-2511-14161`]

- **Long-term map maintenance under object change.** Scene graphs built from a single exploration pass become stale as objects move. RAG-based language memory (2504.21716) addresses this partially but has no geometric ground truth; updating 3D scene graphs incrementally after manipulation is an open problem.

- **No commonsense "where things belong" integration with aerial manipulation.** Housekeep and RoboTidy assume ground manipulators. Connecting the commonsense placement prior (LLM-informed) to a drone that must plan grasp approach from above remains a research-level gap. [`07-arxiv-2205-10712`]

---

## Source

- `raw/research/semantic-object-memory/01-arxiv-2201-13360.md` — arXiv 2201.13360 · *Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization* · Real-time hierarchical 3D scene graph from VIO, MIT SPARK.
- `raw/research/semantic-object-memory/02-arxiv-2106-14386.md` — arXiv 2106.14386 · *Kimera-Multi: Robust, Distributed, Dense Metric-Semantic SLAM for Multi-Robot Systems* · Distributed multi-robot metric-semantic mesh SLAM, MIT SPARK.
- `raw/research/semantic-object-memory/03-arxiv-2309-16650.md` — arXiv 2309.16650 · *ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning* · CLIP-fused open-vocabulary 3D graph enabling language-queried robot planning.
- `raw/research/semantic-object-memory/04-arxiv-2403-17846.md` — arXiv 2403.17846 · *Hierarchical Open-Vocabulary 3D Scene Graphs for Language-Grounded Robot Navigation (HOV-SG)* · Three-level open-vocab scene graph with 75% size reduction vs. dense maps.
- `raw/research/semantic-object-memory/05-arxiv-2409-16944.md` — arXiv 2409.16944 · *Go-SLAM: Grounded Object Segmentation and Localization with Gaussian Splatting SLAM* · Per-Gaussian object IDs + open-vocabulary query + path planning; drone depicted.
- `raw/research/semantic-object-memory/06-arxiv-2501-05750.md` — arXiv 2501.05750 · *Semantic Mapping in Indoor Embodied AI — A Survey* · Comprehensive survey; flags memory cost and compute as primary open challenges.
- `raw/research/semantic-object-memory/07-arxiv-2205-10712.md` — arXiv 2205.10712 · *Housekeep: Tidying Virtual Households using Commonsense Reasoning* · Benchmark for LLM-guided tidying without explicit goal specification; 1,799 objects, 268 categories.
- `raw/research/semantic-object-memory/08-arxiv-2511-14161.md` — arXiv 2511.14161 · *RoboTidy: A 3DGS Household Tidying Benchmark for Embodied Navigation and Action* · 500 photorealistic 3DGS scenes; VLA+VLN unified tidying benchmark with real-world transfer.
- `raw/research/semantic-object-memory/09-arxiv-2402-07537.md` — arXiv 2402.07537 · *UAV-assisted Visual SLAM Generating Reconstructed 3D Scene Graphs in GPS-denied Environments* · Only directly aerial paper; marker-based VSLAM with multi-layer situational graph on a real UAV.
- `raw/research/semantic-object-memory/10-arxiv-2504-21716.md` — arXiv 2504.21716 · *LLM-Empowered Embodied Agent for Memory-Augmented Task Planning in Household Robotics* · RAG-based object-location memory + LLM agent orchestration; avoids explicit scene graph.
- `raw/research/semantic-object-memory/11-arxiv-2409-15451.md` — arXiv 2409.15451 · *Tag Map: A Text-Based Map for Spatial Reasoning and Navigation with Large Language Models* · Text-tag map 2–4 orders of magnitude smaller than embedding maps; LLM-grounded navigation.

---

## Related

[[home-tidy-drone-prototype]] — parent; this map is the target representation for the tidy-drone research assignment.
[[indoor-cluttered-slam]] — metric geometry layer that semantic graphs layer on top of.
[[onboard-grasp-perception]] — object detection pipeline that populates the semantic map at runtime.
[[voice-intent-task]] — natural-language frontend that queries this map to resolve object goals.
[[drone-contact-and-door-tasks]] — structural semantic entities (doors, rooms) produced by the aerial scene-graph paper (2402.07537).
