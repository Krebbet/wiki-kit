# Home Tidying Robots

The household tidying robot is a well-defined research problem — pick up misplaced objects and put them in their "correct" location — but no fully autonomous, commercially shipping system exists for messy real homes. The research frontier (2023–2025) has converged on two hard sub-problems: **open-world object-category-to-receptacle mapping** (where does each thing go?) and **personalisation** (where does *this user* want it?). Ground robots (wheeled mobile manipulators) are the dominant platform; aerial approaches are absent from this literature. Our [[home-tidy-drone-prototype]] sits at the intersection of this tidying-robot landscape and the aerial manipulation gap documented in [[aerial-manipulation]].

## Source

- `raw/research/home-tidying-robots/03-01-arxiv-2305-05658.md` — TidyBot (Stanford/Princeton/Google, arXiv 2305.05658)
- `raw/research/home-tidying-robots/02-02-arxiv-2412-10447.md` — TidyBot++ (Princeton/Stanford, arXiv 2412.10447)
- `raw/research/home-tidying-robots/05-03-arxiv-2207-10106.md` — WRC2020 Partner Robot (U. Tokyo, arXiv 2207.10106)
- `raw/research/home-tidying-robots/06-04-arxiv-2412.13211.md` — ManiSkill-HAB (UCSD/Hillbot, arXiv 2412.13211)
- `raw/research/home-tidying-robots/04-05-arxiv-2404-14285.md` — LLM-Personalize (Microsoft/Edinburgh, arXiv 2404.14285)
- `raw/research/home-tidying-robots/01-06-1x-neo-home-robot.md` — 1X NEO (FAILED CAPTURE — JS-wall, marketing fragment only)

---

## 1. Landscape Summary

*Is anything shipping commercially? What is the research frontier?*

**Nothing is shipping** for general household tidying at consumer scale as of mid-2026. The landscape breaks into three tiers:

1. **Commercial humanoids** — companies like 1X Technologies (NEO), Figure, Apptronik, and Boston Dynamics are building full-body humanoids marketed at home tasks. Technical details are sparse; maturity is pre-ship or early-pilot. 1X NEO has an order page and a Hayward, CA factory described as "America's first vertically integrated high-volume humanoid factory" [src: 01-06-1x-neo-home-robot.md] — but no technical paper or validated results were capturable.

2. **Research mobile manipulators** — wheeled ground robots (TidyBot, TidyBot++, WRC systems) that have demonstrated real-world tidying at 65–85% success in controlled lab/competition settings. These are the most technically documented systems. None ship commercially.

3. **Simulation benchmarks** — Housekeep, HAB/ManiSkill-HAB, and related benchmarks define what "tidying" means quantitatively and provide reproducible evaluation. Real-robot results lag simulation by a wide margin on object count and environment diversity.

The research frontier in 2024–2025 is: (a) learning-based pick-and-place that generalises across object categories, (b) LLM-based personalisation that infers "where *this user* wants things" from few examples, and (c) platform democratisation (low-cost, open-source hardware to accelerate data collection).

---

## 2. Research Systems

### 2.1 TidyBot (Stanford/Princeton/Google, 2023)

**Task definition:** Pick up every object on the floor and place it in its correct receptacle (drawer, shelf, closet, bin), where "correct" is personalised to the user. [src: 03-01-arxiv-2305-05658.md]

**Hardware:** Custom wheeled mobile manipulator with robot arm. The novel element is the software stack, not the hardware. [src: 03-01-arxiv-2305-05658.md]

**Method:** Few-shot LLM summarisation for personalisation. The user provides a handful of example placements (e.g., "yellow shirts → drawer, dark purple shirts → closet"). A GPT-family LLM summarises these into a generalised rule ("light-coloured clothes → drawer, dark-coloured → closet"). An open-vocabulary image classifier (CLIP-family) grounds the nouns in the rule to detected objects on the floor. The robot then executes pick-and-place. The same summarisation mechanism also selects manipulation primitives (pick-and-place vs. pick-and-toss). [src: 03-01-arxiv-2305-05658.md]

**Results:** 91.2% accuracy on unseen objects in the benchmark dataset; 85.0% success rate on a real mobile manipulator in real-world test scenarios. [src: 03-01-arxiv-2305-05658.md]

**Maturity:** *Demoed* — real-robot, lab/home-like environment. Not commercially available. The LLM runs offboard (cloud API). [src: 03-01-arxiv-2305-05658.md]

**Key insight:** LLM summarisation provides generalisation from very few user examples without collecting large preference datasets. This maps directly to the COMMAND CENTER personalisation concept in [[system-architecture]].

---

### 2.2 TidyBot++ (Princeton/Stanford/Dexterity, Dec 2024)

**Task definition:** Common real household manipulation tasks — opening a fridge, wiping a countertop, loading a dishwasher, taking out trash, loading laundry, watering a plant — in a real apartment home. Not limited to floor cleanup; broader mobile manipulation. [src: 02-02-arxiv-2412-10447.md]

**Hardware:** Open-source, $5–6k holonomic mobile base with four powered-caster swerve modules (adapted from FIRST Robotics Competition MK4 modules) plus a Kinova Gen3 arm and Intel NUC compute. The powered-caster mechanism provides full holonomy — independent control of all three planar degrees of freedom (x, y, rotation) simultaneously. A WebXR smartphone teleoperation interface enables data collection without specialised hardware. [src: 02-02-arxiv-2412-10447.md]

**Method:** Imitation learning (diffusion policy) from 50–100 smartphone-teleoperated demonstrations per task. Holonomic drive is central to the claim: it simplifies task execution by eliminating nonholonomic constraints and enables stable position-space representations for policy learning. [src: 02-02-arxiv-2412-10447.md]

**Results:** Open fridge 10/10; wipe countertop 9/10; load dishwasher 7/10; take out trash 10/10; load laundry 7/10; water plant 6/10. Head-to-head on wipe countertop: holonomic base 9/10 vs. differential drive 4/10 with identical data. [src: 02-02-arxiv-2412-10447.md]

**Maturity:** *Demoed* in a real apartment home. Open-source hardware design, BOM, CAD files, and code released at `tidybot2.github.io`. Not shipping commercially. [src: 02-02-arxiv-2412-10447.md]

**Canadian connection:** Uses Kinova Gen3 arm (Kinova Robotics, Boisbriand, Quebec). [src: 02-02-arxiv-2412-10447.md]

**Key insight:** Low-cost, holonomic, open-source hardware can unlock high-performance policies with small datasets. The $5–6k base cost benchmark is relevant framing for our project's cost targets.

---

### 2.3 World Robot Challenge 2020 — Partner Robot (University of Tokyo, 2022)

**Task definition:** Competition benchmark. Task 1 (15 min): pick up ~20 objects scattered on floor and tables, place them in designated bins by object category (Food, Kitchen, Shape, Tool, Task, Unknown; fixed category-to-place mapping). Task 2 (5 min): navigate to adjacent room, pick specified objects from a shelf, deliver to a person waving their hand. [src: 05-03-arxiv-2207-10106.md]

**Hardware:** Toyota HSR (Human Support Robot) — a commercial research mobile manipulator (~$300k). Modified with Intel RealSense D435 (hand camera, replacing original), vision-based tactile sensor on one fingertip, Xtion depth camera (head), 2D LiDAR (foot), stereo camera, 6-axis force/torque sensor in wrist, microphone. Heavy DNN inference offloaded to external GPU PC over ~1 Gbps WiFi. [src: 05-03-arxiv-2207-10106.md]

**Method:** Data-driven system using Mask R-CNN + UOIS for object detection, CLIP with custom prompts for classification, grasp-pose FCN (0.43 s inference), segmentation FCN for drawer/surface detection, Keypoint R-CNN for human hand-wave detection. Object-centric stateful system (async object manager) prevents DNN bottleneck. Online fine-tuning during competition: classifier fine-tuned on 748 lab + 556 competition-venue images across rounds. Two-layer costmap: 2D LiDAR for large obstacles + RGB-D for low-height objects (small balls, t-shirts). [src: 05-03-arxiv-2207-10106.md]

**Results:** 2nd prize of 5 teams. Object recognition: 92% overall across categories. Grasp success: 65% overall (Shape category: 100%; Tool category: 45%). Average time per successful object: 56.2 seconds. Best trial: 11 objects cleared in task 1. Task 2 navigation success: 4 of 6 trials. [src: 05-03-arxiv-2207-10106.md]

**Maturity:** *Demoed* — real competition environment, not simulated. Second prize in a standardised global competition. [src: 05-03-arxiv-2207-10106.md]

**Key insight:** Competition-style tidying uses fixed category-to-place rules (no personalisation). The tactile sensor helped confirm grasp state on thin/small objects where vision alone was insufficient — consistent with [[tactile-manipulation]] findings.

---

### 2.4 ManiSkill-HAB (UCSD/Hillbot, ICLR 2025)

**Task definition:** Three long-horizon household rearrangement tasks using a simulated Fetch mobile manipulator in ReplicaCAD apartment scenes: TidyHouse (move 5 objects to open receptacles), PrepareGroceries (move items to/from fridge), SetTable (move bowl from drawer + apple from fridge to dining table). [src: 06-04-arxiv-2412.13211.md]

**Hardware:** Simulation only — Fetch robot, ManiSkill3/GPU acceleration, ReplicaCAD scenes, YCB objects. [src: 06-04-arxiv-2412.13211.md]

**Method:** GPU-accelerated simulation with realistic low-level grasping (replacing prior "magical grasp" teleport). Key contribution: automated event labeling and trajectory categorisation enables rule-based filtering of RL demonstrations without human labelling — scalable controlled data generation. RL and IL baselines provided for 150 policies trained on 1.83 billion environment samples. [src: 06-04-arxiv-2412.13211.md]

**Results:** 4300+ simulation samples per second with 2 RGB-D cameras rendering — 3x faster than Habitat 2.0 at a fraction of GPU memory. Benchmark infrastructure only; end-task success rates are in appendix tables, not headlined. [src: 06-04-arxiv-2412.13211.md]

**Maturity:** *Sim-only* — benchmark infrastructure. Published ICLR 2025. No real-robot validation. [src: 06-04-arxiv-2412.13211.md]

---

### 2.5 LLM-Personalize (Microsoft/Edinburgh, 2024)

**Task definition:** Household object rearrangement in multi-room, partially observable simulated environments (Housekeep benchmark). Agent must explore, discover misplaced objects, and rearrange them to match a human preference dataset. [src: 04-05-arxiv-2404-14285.md]

**Hardware:** Simulation only — simulated first-person agent in Housekeep 3D environment. GPT-3.5-family LLM for planning (cloud API). Off-the-shelf simulator controller for low-level actions. 1000-timestep episodes. [src: 04-05-arxiv-2404-14285.md]

**Method:** Two-phase optimisation pipeline. Phase 1: imitation learning (supervised fine-tuning from demonstrations) to bootstrap executability and initial preference alignment. Phase 2: reinforced Self-Training (ReST) — iterative exploration, collect positive examples (correct placements per preference dataset), supervised fine-tuning. Dynamic scene graph built from egocentric observations during exploration (not given a priori). [src: 04-05-arxiv-2404-14285.md]

**Results:** >30% improvement in rearrangement success rate over baseline LLM planners. Example: Scene 1 baseline −3.6% → after IL 17.6% → grows further after self-training. Performance stabilises after ~2 self-training iterations (overfitting risk). [src: 04-05-arxiv-2404-14285.md]

**Maturity:** *Sim-only* — no real-robot demonstration. Research paper (2024). [src: 04-05-arxiv-2404-14285.md]

**Key contrast with TidyBot:** TidyBot uses zero-fine-tuning LLM summarisation for a specific user's few examples. LLM-Personalize uses RL fine-tuning against a benchmark's aggregate human-preference dataset — more computationally expensive but potentially more robust over complex multi-room plans. [src: 03-01-arxiv-2305-05658.md, 04-05-arxiv-2404-14285.md]

---

## 3. The Personalisation Problem

*How do existing systems handle "Lulu goes on Charlie's bed"?*

This is the central design problem for any home tidying system. Three distinct approaches exist:

**A. Few-shot LLM summarisation (TidyBot):** User provides ~5 example placements as text. LLM summarises them into a generalised rule. No model fine-tuning. Fast setup (minutes). Generalises well within a session (91.2% on unseen objects in benchmark). Limitation: rules are text-grounded; novel object types may not fit any learned category. The approach maps directly to our COMMAND CENTER personalisation concept in [[system-architecture]]. [src: 03-01-arxiv-2305-05658.md]

**B. RL fine-tuning (LLM-Personalize):** Fine-tune the LLM planner itself against a human preference reward signal using imitation learning + iterative self-training. More complex setup; >30% improvement over baseline planners in simulation. Requires a training loop — not immediate personalisation. Best suited for a household preference *dataset* (aggregate of many users) rather than a single user's preferences. [src: 04-05-arxiv-2404-14285.md]

**C. Fixed category-to-place rules (WRC2020):** Competition systems define a fixed mapping per object category. No user personalisation at all — "Food items go in bin A." Operationally simple but not scalable to a real home where every user is different. [src: 05-03-arxiv-2207-10106.md]

**The benchmark for personalisation:** Housekeep (Kant et al., 2022) is the standard evaluation — a 3D simulated household benchmark with collected human preference data. LLM-Personalize is currently the state-of-the-art method on it. ManiSkill-HAB's TidyHouse task is built on top of HAB, which uses the same benchmark family. See also [[semantic-object-memory]] for Housekeep coverage and ConceptGraphs as a spatial-semantic approach.

**Our project's personalisation challenge** goes further than any of these: "Lulu goes on Charlie's bed" is a *named-entity* preference tied to spatial semantics (a specific location in a specific room). TidyBot's LLM summarisation handles this class of rule well in principle — "stuffed animals go on Charlie's bed" is exactly the generalised-rule form it produces. What's missing is the spatial grounding of "Charlie's bed" as a persistent landmark in the map, which is addressed by [[semantic-object-memory]] (Hydra/ConceptGraphs spatial scene graphs).

---

## 4. Benchmark Landscape

| Benchmark | Type | What it measures | Year | Notes |
|---|---|---|---|---|
| **TidyBot eval** | Real-robot | Personalised pick-and-place to correct receptacle; unseen objects | 2023 | 91.2% text benchmark; 85% real robot [src: 03-01-arxiv-2305-05658.md] |
| **WRC Partner Robot** | Real competition | Object recognition, grasp success, task completion rate, time/object | 2021 | 5 teams; best result 65% grasp, 56 s/object [src: 05-03-arxiv-2207-10106.md] |
| **Housekeep** | Simulation | Object rearrangement aligned to human preference dataset; multi-room, partially observable | 2022 | Used by LLM-Personalize; see [[semantic-object-memory]] [src: 04-05-arxiv-2404-14285.md] |
| **HAB (Habitat 2.0)** | Simulation | Long-horizon navigation+manipulation (TidyHouse, PrepareGroceries, SetTable) | 2021 | Fetch robot, magical grasp (inflated results) |
| **ManiSkill-HAB** | Simulation | HAB + realistic low-level grasping; 4300 SPS GPU-accelerated | 2025 | ICLR 2025; fixes magical-grasp inflation [src: 06-04-arxiv-2412.13211.md] |

**What's missing from benchmarks:** No aerial/drone variant exists. All benchmarks assume ground-robot reach (floor to ~1.5m). No benchmark addresses multi-floor or stair-climbing. No benchmark for "find it first" — all benchmarks give the agent knowledge of which objects need moving. No benchmark for operating around children or pets.

---

## 5. Comparison to Our Project *(synthesis — labelled)*

*[SYNTHESIS] The following section interprets the literature relative to our home-tidy drone project. It represents editorial judgement, not claims sourced from the papers above.*

**Where our drone/ground-primary approach fits:**

The existing tidying-robot literature is entirely ground-robot, with a single hardware form factor: wheeled mobile base + robot arm. The aerial dimension is absent. This means:

1. **We inherit the software stack almost wholesale.** TidyBot's LLM summarisation pipeline, TidyBot++'s diffusion policy approach, LLM-Personalize's ReST fine-tuning — all of these are hardware-agnostic at the planning layer. Our COMMAND CENTER (see [[system-architecture]]) can adopt TidyBot-style personalisation directly.

2. **The grasping problem is harder for us, not easier.** The best real-world ground robot (TidyBot++ on easy household tasks) achieves 60–100% success. WRC2020 (harder, messier task set) achieved 65% grasp success. Our [[onboard-grasp-perception]] page identifies that aerial/onboard open-world grasping has not yet been demonstrated at commercial quality. The gap between 65–85% ground-robot success and drone grasping is the central hardware challenge.

3. **The personalisation problem is identical.** The same "where does Lulu go?" question faces any home robot. TidyBot's approach (few-shot LLM summarisation → generalised rules → open-vocab detection) is directly applicable. Our project does not need to solve personalisation from scratch; we adopt and extend this approach with spatial landmark grounding.

4. **Our aerial advantage is coverage, not manipulation.** Ground robots are blocked by stairs, toys on stairs, narrow passages, and furniture undersides. A drone can survey the entire home from above, prioritise tasks, and access locations a wheeled base cannot reach. This suggests a **hybrid architecture**: drone for surveying/prioritising + ground robot (or land-then-grasp drone approach) for manipulation. Our [[home-tidy-drone-prototype]] already proposes a land-then-grasp architecture as Phase 1.

5. **The $5–6k TidyBot++ base cost** is a useful competitor anchor. Our Phase-1 build should aim for a total system cost in the same order of magnitude to stay credible as a consumer-accessible prototype.

**What the literature validates about our approach:**
- LLM-based personalisation from few examples is proven at 85–91% accuracy (TidyBot).
- Imitation learning from ~50–100 demonstrations per task is sufficient for good household task policies (TidyBot++).
- Open-vocabulary object detection for floor-object identification is the correct perception approach (TidyBot's CLIP usage).
- A 65% grasp success rate is a realistic baseline for a well-engineered real-world system — we should target this initially, not 95%+.

---

## 6. Gap Table

What every existing system lacks that our project must solve:

| Gap | Why existing systems don't have it | Our project's challenge |
|---|---|---|
| **Aerial platform** | All systems are ground robots (wheels); no published aerial tidying robot exists | Phase 1: land-then-grasp on [[home-tidy-drone-prototype]]; aerial survey + ground manipulation hybrid |
| **Stair-crossing** | Ground robots are floor-locked | Drone inherently crosses floors; picking up from stairs requires land-then-grasp at variable angles |
| **Open-world object detection at grasp range** | TidyBot uses CLIP for classification; WRC uses Mask R-CNN + CLIP. None extend to novel objects not in training | [[onboard-grasp-perception]] gap: aerial OVD ~28% F1; no onboard aerial grasper is category-agnostic |
| **Spatial personalisation ("Charlie's bed")** | TidyBot maps categories→receptacle-types; no persistent spatial landmark binding | Need [[semantic-object-memory]] integration: named location → 3D map coordinate |
| **Failure recovery from grasp failure** | WRC: retry with restart (slow); TidyBot++: not evaluated on failure modes | Drone after failed grasp has different recovery path than ground robot |
| **Operating around children/pets** | WRC has human-avoidance; no system addresses dynamic small obstacles | [[safe-indoor-flight]] constraints apply; drone propwash near children is a safety concern |
| **Endurance for whole-home tasks** | Ground robots: plugged-in or large battery; no endurance constraint | Drone: ~10–20 min flight; dock-and-recharge architecture required per [[home-tidy-drone-prototype]] |
| **Grasping non-flat-floor objects** | All systems assume objects on floor or standard-height surfaces | Drone must grasp from arbitrary heights, including mid-air or on sloped stairs |
| **Real-time personalisation from voice** | TidyBot uses text-only input; WRC uses no personalisation | [[voice-intent-task]] integration needed for "Lulu goes on Charlie's bed" spoken command |
| **Multi-floor coordination** | All systems are single-floor | Drone surveys multi-floor; task assignment across floors requires multi-floor [[indoor-cluttered-slam]] |

---

## Related

- [[home-tidy-drone-prototype]] — our Phase-1 build plan; this page is the prior-art context for it
- [[semantic-object-memory]] — "where things belong" semantics; Housekeep benchmark; ConceptGraphs
- [[aerial-manipulation]] — drone manipulation gaps; why aerial tidying is harder than ground
- [[system-architecture]] — full cognitive stack; COMMAND CENTER personalisation concept
- [[onboard-grasp-perception]] — vision-only grasping limits; open-world detection gap
- [[tactile-manipulation]] — tactile sensing for manipulation; WRC2020 used tactile fingertip
- [[voice-intent-task]] — voice→intent pipeline for spoken personalisation commands
- [[safe-indoor-flight]] — safety constraints for operating around children and pets
- [[indoor-cluttered-slam]] — indoor mapping for multi-room tidying tasks
