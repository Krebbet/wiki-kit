# Humanoid and Mobile Manipulation Robot Perception for Indoor Tasks

What is publicly known about how commercially deployed (or near-deployed) mobile manipulation robots handle indoor semantic mapping and scene understanding? This page documents five platforms — **Boston Dynamics Spot + Orbit**, **Figure 02/03 (Helix)**, **1X NEO/EVE**, **Agility Robotics Digit**, and **Apptronik Apollo** — covering sensors, persistent mapping, object localization, cloud vs onboard compute, and what transfers to a simpler home-tidy ground robot. Focus is on what is shipping or in demonstrable near-deployment as of mid-2026, not pure research demos.

## Source

- `raw/research/humanoid-robot-perception/01-graphnav-tech-summary.md` — Spot SDK: GraphNav Autonomy Technical Summary (primary)
- `raw/research/humanoid-robot-perception/02-graphnav-map-structure.md` — Spot SDK: GraphNav Map Structure (primary)
- `raw/research/humanoid-robot-perception/03-graphnav-localization.md` — Spot SDK: GraphNav Localization (primary)
- `raw/research/humanoid-robot-perception/07-figure-helix-02.md` — Figure AI: Introducing Helix 02 (vendor primary)
- `raw/research/humanoid-robot-perception/08-figure-helix-v1.md` — Figure AI: Helix v1 VLA announcement (vendor primary)
- `raw/research/humanoid-robot-perception/10-orbit-5-robot-report.md` — The Robot Report: Orbit 5.0 features
- `raw/research/humanoid-robot-perception/11-agility-digit-botinfo.md` — BotInfo: Agility Robotics Digit deep-dive
- `raw/research/humanoid-robot-perception/12-semantic-mapping-survey-2025.md` — arXiv:2501.05750: Semantic Mapping in Indoor Embodied AI survey (SFU, 2025)
- `raw/research/humanoid-robot-perception/13-robotics247-spot-orbit-update.md` — Robotics 24/7: Spot + Orbit update (semantic navigation, laser scanning)
- `raw/research/humanoid-robot-perception/17-bd-deepmind-gemini.md` — Let's Data Science: Boston Dynamics integrates DeepMind Gemini Robotics-ER
- `raw/research/humanoid-robot-perception/18-apptronik-apollo-robot-report.md` — The Robot Report: Apptronik unveils Apollo

**Failed captures (bot-walled):** bostondynamics.com blog pages (Orbit product page, "See Your Facility", "Making Atlas See", fleet management blog, "Robot Fleet Management Lifts Off") all returned navigation fragments only. 1X NEO and 1X GTC 2026 pages returned near-empty extractions. The 1X GTC blog headline ("Inside 1X's Humanoid Robot Stack: Simulation, AI Training, and Onboard Compute with NVIDIA") confirmed the Jetson Thor claim but content was not recoverable. These gaps are noted where relevant below.

## Related

[[home-tidying-robots]], [[scene-graph-world-model]], [[semantic-object-memory]], [[indoor-cluttered-slam]], [[dynamic-object-handling]], [[map-then-navigate]], [[world-model-architecture]], [[object-fingerprint-memory]], [[mapping-stack-design]], [[onboard-grasp-perception]], [[tactile-manipulation]]

---

## 1. Boston Dynamics Spot + Orbit

Spot is the most technically documented of the five platforms, with a public SDK containing architecture-level details.

### 1.1 GraphNav: The Persistent Map Architecture

Spot's autonomous navigation uses **GraphNav**, a topological map system. [src: graphnav-tech-summary, graphnav-map-structure, graphnav-localization]

**Map representation:** The world is represented as a locally consistent graph of **waypoints and edges**. A waypoint is a place the robot has visited; it bundles a reference frame, name, unique ID, annotations, and a sensor data snapshot (feature clouds, AprilTag detections, imagery, terrain maps). Edges encode the directed relative pose between adjacent waypoints and any traversal parameters (e.g., stair annotations). [src: graphnav-map-structure]

**What "persistent" means:** Maps are **saved off-robot** (downloaded to a tablet, uploaded to Orbit, shareable between robots). They do NOT persist across reboots unless explicitly downloaded first. Maps are **fixed at record time** — the robot does not update the map while navigating. [src: graphnav-tech-summary]

**No global frame:** GraphNav has no global coordinate system (no GPS coordinates). Localization is always expressed as a pose relative to a specific waypoint, not a global frame. If two paths through the graph lead to the same physical location, accumulated transforms may disagree — this is the known local-consistency limitation. Anchorings (SDK 3.0+) allow waypoints and fiducials to be given global coordinates post-hoc, enabling map display relative to a blueprint or BIM model. [src: graphnav-map-structure]

**Sensors for localization:** Localization combines odometry, visual features, and geometric features from the robot's cameras. A **LiDAR payload** can be added; it augments onboard cameras and significantly improves localization in low-texture or dark environments ("feature deserts"). Without LiDAR, GraphNav depends on camera-visible texture; uniformly textured areas cause localization failure. [src: graphnav-tech-summary, graphnav-localization]

**Localization update rate:** At least twice per second. The robot switches its localization reference waypoint as it moves through the map. [src: graphnav-localization]

**Failure mode — "LOST":** If environment has changed significantly since recording, the robot declares STATUS_LOST and refuses to navigate. The robot cannot self-recover; an operator must re-initialize. A new map must be recorded after significant environment change. [src: graphnav-localization]

**Map creation:** Operators drive Spot manually to record the map (Autowalk on the tablet app). Waypoints are created automatically every ~2 meters, plus at corners/curves. Loop closure is performed via a map processing service (SDK 3.0+): odometry loop closures and fiducial loop closures are supported. [src: graphnav-map-structure]

**Semantic navigation (Spot 4.1):** Visual semantic context was integrated into Spot's navigation system in the Spot 4.1 release. Spot can now detect and avoid common hazards — carts, wires, ladders — by understanding the semantic category of obstacles, not just their geometry. This requires the **Spot Core I/O** companion compute module. [src: robotics247-spot-orbit-update]

### 1.2 Orbit: Fleet Management and Semantic Inspection

Orbit is Boston Dynamics' server-side fleet platform, connecting Spot data to facility operations. [src: orbit-5-robot-report, robotics247-spot-orbit-update]

**Site View:** 360° panoramic images captured by Spot's cameras are stitched into a visual history of the facility, queryable over time. Operators can do remote walkthroughs, compare site states, and create inspection missions directly from Site View imagery. This is the closest Spot comes to a persistent semantic map — it is a visual record, not a geometric model, but it is anchored spatially. [src: orbit-5-robot-report]

**AI anomaly detection (Orbit 5.0):** Vision-language prompts are used to analyze images at inspection points. The system can flag yes/no answers, numeric readings (gauge values), percentages, or descriptive text without manual review. Specific capabilities: debris/spill/corrosion detection, pallet status checks, thermal anomaly flagging via dynamic thresholding. [src: orbit-5-robot-report]

**Laser scanning integration:** A Leica BLK ARC 3D scanning payload allows Spot to perform repeatable autonomous 3D scans, processed in Orbit and exported for use in facility design/BIM tools. This is a separate modality from the inspection/anomaly detection stack. [src: robotics247-spot-orbit-update]

**DeepMind Gemini Robotics-ER integration (2026):** Boston Dynamics is integrating `Gemini Robotics-ER 1.6` into Spot and Orbit's AIVI-Learning stack. This adds spatial reasoning, multi-view understanding, instrument reading, and natural-language-driven task planning. The workflow uses conversational prompts to the model, with a tool layer that maps decisions to pre-authorized Spot SDK commands. This moves Spot from scripted Autowalk missions toward higher-level task planning. Early demos include gauge reading, pooled-water detection, and conveyor inspection. Execution gaps (imperfect grasps) remain. [src: bd-deepmind-gemini]

**Object detection for grasping:** Spot itself (the quadruped) does not have manipulation arms in its standard form. The Atlas humanoid (from Boston Dynamics) has grasping, with a dedicated per-object tracking system called **SuperTracker** that fuses kinematics, vision, and force — but this blog post was bot-walled and content could not be captured directly. The Gemini Robotics-ER integration demonstrates object retrieval tasks, implying grasping capability in the Atlas context.

---

## 2. Figure AI — Figure 02/03 with Helix

Figure is the most detailed on software architecture among the humanoid vendors with public technical posts. Hardware is Figure 02 (Helix v1) and Figure 03 (Helix 02).

### 2.1 Sensors

- **6 RGB cameras:** head cameras (the primary scene understanding input), palm cameras (in-hand visual feedback when objects occlude the head camera), and full-body coverage. No LiDAR. No depth cameras. Pure camera-based perception. [src: figure-helix-02, figure-helix-v1]
- **Tactile sensors:** embedded in each fingertip, sensitive to forces as small as 3 grams (e.g., paperclip). [src: figure-helix-02]
- **Full-body proprioception:** joint state, wrist pose, finger positions. [src: figure-helix-v1]

### 2.2 Architecture: System 0 / System 1 / System 2

Helix 02 uses a three-tier hierarchy, each operating at a different timescale: [src: figure-helix-02]

| Layer | Function | Rate | Size |
|---|---|---|---|
| **System 2 (S2)** | Scene understanding, language comprehension, semantic goal sequencing | 7–9 Hz | 7B parameter open-weight VLM |
| **System 1 (S1)** | Visuomotor policy — translates S2 latents + sensor inputs to full-body joint targets | 200 Hz | 80M parameter transformer |
| **System 0 (S0)** | Whole-body balance, contact, coordination | 1 kHz | 10M parameter neural network |

S2 is built on an internet-pretrained open-source VLM. It processes monocular robot camera images and robot state, distilling task-relevant semantics into a single continuous latent vector that conditions S1. S1 is a cross-attention encoder-decoder transformer initialized from simulation pretraining. S0 was trained entirely in simulation on >200,000 parallel environments with domain randomization; trained on >1,000 hours of retargeted human motion data. [src: figure-helix-v1, figure-helix-02]

### 2.3 Persistent Mapping — None

**Figure robots do not maintain persistent maps across sessions.** There is no discussion of SLAM, persistent maps, map-based localization, or between-session spatial memory anywhere in the Helix v1 or Helix 02 primary sources. The system is purely **egocentric** — it perceives the world through its onboard cameras each run and acts accordingly. Scene understanding (S2) operates at the level of "what objects are here and what should I do with them" without reference to a prior map. [src: figure-helix-v1, figure-helix-02] *(note: absence of evidence, not confirmed architectural decision — vendor may have proprietary map layer not disclosed)*

### 2.4 Object Detection and Localization for Grasping

Object identification is done in real-time from camera input by S2 (the VLM). No pre-mapped object locations are referenced. The system demonstrates zero-shot generalization: robots can pick up thousands of novel household objects — glassware, toys, tools, clothing — never seen during training, with natural language commands like "Pick up the [X]." Language grounding includes abstract concepts: "Pick up the desert item" correctly identifies a toy cactus. [src: figure-helix-v1]

Palm cameras provide in-hand visual feedback for objects occluded from head cameras. Tactile sensors provide force-modulated grasping feedback. These together enable tasks beyond pure vision-based policies: extracting individual pills from containers, dispensing precise syringe volumes, singulating small irregular objects from clutter. [src: figure-helix-02]

### 2.5 Onboard vs Cloud Compute

Helix runs **entirely onboard** on dual embedded GPUs (Figure 02 and Figure 03). S0 runs at 1 kHz — no cloud round-trip is possible at that rate. S2 runs asynchronously at 7–9 Hz as a background process; S1 runs at 200 Hz as a real-time process. The two share a latent vector via shared memory. This asynchronous split allows each system to run at its optimal frequency. Training introduced a temporal offset matching the deployment inference latency gap to minimize train/inference distribution shift. [src: figure-helix-v1, figure-helix-02]

*("Commercial-ready: the first VLA that runs entirely onboard embedded low-power-consumption GPUs" — direct quote from [src: figure-helix-v1])*

### 2.6 Deployment Status

Figure 02 and 03 are in pilot deployment (company-internal at BotQ manufacturing facility; targeted at home and industrial contexts). The 4-minute dishwasher task (61 sequential loco-manipulation actions, zero resets, zero human intervention) is claimed to be the longest-horizon fully autonomous humanoid task demonstrated as of January 2026. [src: figure-helix-02]

---

## 3. 1X Technologies — NEO and EVE

Technical disclosure from 1X is sparse. The 1x.tech website is bot-walled; the GTC 2026 blog title confirms the Jetson Thor claim but page content was not recoverable. The following draws from the Wikipedia entry and secondary trade press summaries.

**NEO (home humanoid):** Dual 8.85MP stereo fisheye cameras at 90 Hz; no LiDAR. 3D perception and SLAM via stereo fisheye. Onboard compute: NVIDIA Jetson Thor. Runs `Redwood AI`, 1X's proprietary VLA model, locally on-device. 4-microphone beamforming array for spatial sound and voice recognition. ~66 lb, multi-hour (≈4 h) battery. *(these specs appear in secondary trade press; primary capture failed)*

**No publicly disclosed SLAM architecture or persistent map system** is documented in any capturable source. 1X's marketing describes "conversational memory across interactions" and "multimodal sensing" but provides no architectural specifics. Given the camera-only sensor suite (no LiDAR, fisheye stereo), the SLAM is presumably visual-inertial or visual-only. No public disclosure on whether maps persist across sessions.

**EVE (wheeled industrial):** Earlier platform, targeted at logistics/security/healthcare. Less public disclosure than NEO.

---

## 4. Agility Robotics — Digit

### 4.1 Sensors

Digit's primary perception suite is **torso-mounted** (providing a stable vantage point protected from damage). Sensor suite: [src: agility-digit-botinfo]

- LiDAR (3D mapping, distant obstacle detection)
- 4× Intel RealSense depth cameras (360° spatial awareness, local terrain mapping)
- RGB cameras (visual perception)
- MEMS IMU + gyroscope (balance)
- Force sensors in each arm (compliant manipulation)

### 4.2 Navigation Architecture

Digit is described as capable of autonomous navigation "without needing pre-mapped routes" [src: agility-digit-botinfo]. The combination of LiDAR (generates high-resolution 3D maps of working environment) and depth cameras (maps local terrain) is described as enabling real-time adaptation. No public documentation of the underlying SLAM algorithm or whether maps persist across sessions has been captured.

**Amazon deployment (2024):** Amazon fulfillment centers. Task: picking up and moving empty totes from conveyor system to nearby cart. Amazon emphasized Digit's compatibility with human-scale environments. [src: agility-digit-botinfo]

**GXO Logistics** is a second major deployment partner. [src: agility-digit-botinfo]

### 4.3 Object Detection for Grasping

The initial Amazon deployment task is described as "tote moving" — a structured, well-defined object class. Object detection generalization for open-world household objects is not claimed. This is consistent with a "logistics-first" design philosophy: pick one task, do it well, add tasks via software update. [src: agility-digit-botinfo]

### 4.4 Cloud vs Onboard

No public disclosure on inference distribution between onboard and cloud for Digit's perception stack.

---

## 5. Apptronik — Apollo

### 5.1 Sensors

Apollo uses **stereo vision cameras** ("two eyes") as its primary perception input for obstacle avoidance and navigation. Force sensing is used for human proximity response — Apollo slows down as humans approach, using vision + force sensing to assess proximity, similar to collaborative robot (cobot) behavior. [src: apptronik-apollo-robot-report]

No LiDAR is mentioned in the captured primary source. Sensor disclosure is minimal relative to Digit.

### 5.2 Navigation and Manipulation

Apollo's initial deployment scope is "gross manipulation" — moving boxes, totes, and crates using two hands without requiring full dexterity. Partners: Mercedes-Benz, GXO Logistics, Jabil (also a manufacturing partner). Tasks include unloading trailers, pallet handling, lineside delivery. [src: apptronik-apollo-robot-report]

Apollo's Astra predecessor (a humanoid torso R&D platform) was used to develop the perception and grasping primitives carried forward into Apollo. No public technical documentation on SLAM or map architecture is available in captured sources.

### 5.3 Cloud vs Onboard

Not publicly disclosed in captured sources.

---

## 6. Cross-Platform Comparison *(synthesis)*

*[SYNTHESIS] The following section interprets and compares the platforms. Claims trace to captured sources as noted.*

### 6.1 Persistent Maps vs Egocentric Perception

| Platform | Persistent map? | Evidence quality |
|---|---|---|
| **Spot (GraphNav)** | Yes — explicit, downloadable, shareable across robots | High (primary SDK docs) |
| **Figure (Helix)** | No — pure egocentric VLA, no map reference in any source | Medium (absence of evidence; source is vendor blog) |
| **1X NEO** | Unknown — no disclosed architecture | Low (bot-walled, no primary capture) |
| **Agility Digit** | Unconfirmed — "no pre-mapped routes needed" claim exists but no map persistence claim | Medium (trade press) |
| **Apptronik Apollo** | Unknown — no disclosed architecture | Low (minimal disclosure) |

**Key finding:** Spot is the only platform with publicly documented persistent map architecture. The humanoid platforms (Figure, 1X, Digit, Apollo) are either camera-only egocentric systems or do not disclose their map architecture. This is consistent with their respective contexts: Spot is deployed to fixed facilities where a persistent route map is the core value proposition; humanoids are targeting environments where human-like generalization without pre-mapping is the desired property.

### 6.2 Sensor Choices

| Platform | Cameras | Depth/LiDAR | IMU | Tactile |
|---|---|---|---|---|
| **Spot** | Onboard cameras + optional payloads | LiDAR payload (optional, improves localization) | Yes (internal) | No (standard) |
| **Figure (Helix)** | 6 RGB cameras (head + palm) | None | Yes (proprioception) | Fingertip tactile sensors |
| **1X NEO** | Dual 8.85MP stereo fisheye @ 90 Hz | None | — | — |
| **Agility Digit** | RGB cameras + 4× RealSense depth | LiDAR (torso-mounted) | MEMS IMU + gyro | Force sensors in arms |
| **Apptronik Apollo** | Stereo cameras | None (not disclosed) | — | Force sensing |

**Pattern:** The warehouse/logistics-first robots (Digit, Spot) include LiDAR. The dexterity-first humanoids targeting homes (Figure, 1X NEO) are camera-only. Apollo sits between — stereo vision without LiDAR but with force sensing.

### 6.3 Object Detection Architecture

| Platform | Approach | Generalization |
|---|---|---|
| **Spot + Orbit** | VLP prompts at pre-defined inspection points; real-time semantic hazard avoidance (carts/wires/ladders) | Task-specific prompt engineering |
| **Figure (Helix)** | VLM (S2) real-time open-vocabulary detection; zero-shot to novel objects via language | High — demonstrated on thousands of novel household objects |
| **1X NEO** | Undisclosed ("Redwood AI" VLA) | Unknown |
| **Agility Digit** | Structured task (tote moving); object class highly constrained | Low generality by design |
| **Apptronik Apollo** | Gross manipulation (box/tote) | Low generality by design |

### 6.4 Cloud vs Onboard

| Platform | Inference location | Evidence |
|---|---|---|
| **Spot + Orbit** | Orbit runs on cloud OR on-premise VM; Spot onboard handles navigation; semantic AI (Gemini ER) requires cloud/network | [src: orbit-5-robot-report, bd-deepmind-gemini] |
| **Figure (Helix)** | Fully onboard dual embedded GPUs; no cloud required for inference | [src: figure-helix-v1] |
| **1X NEO** | Onboard Jetson Thor; "large neural networks locally on the robot" | Secondary press; primary not capturable |
| **Agility Digit** | Undisclosed | — |
| **Apptronik Apollo** | Undisclosed | — |

The contrast is sharp: Figure's Helix and 1X NEO commit explicitly to onboard inference as a commercial readiness requirement (no latency acceptable for 1 kHz control). Spot + Orbit offloads semantic reasoning to Orbit (cloud/on-premise server), keeping only navigation onboard.

---

## 7. Transfer to a Home-Tidy Ground Robot *(synthesis + editorial)*

*[SYNTHESIS] The following five lessons are interpretive, tracing to source findings above. They are editorial judgements about transferability, not claims from the sources.*

### L1: Persistent map = the right answer for a known home

Spot's GraphNav model — record once, reuse across sessions, share across robots — is directly applicable to a home robot that operates in a fixed environment. The home changes slowly; a persistent map with a change-detection layer (see [[dynamic-object-handling]] and [[world-model-architecture]]) is the right architecture. Figure's purely egocentric approach may be fine for a general-purpose robot that must work in any home, but for a robot that operates in one home repeatedly, a persistent map beats re-perceiving from scratch every session.

The key GraphNav lesson: **do not attempt to maintain a global consistent frame**. A waypoint-relative, locally-consistent pose graph (like GraphNav, or like RTAB-Map's pose graph — see [[mapping-stack-design]]) is the right form factor. Global consistency is unnecessary and expensive.

**GraphNav failure mode to avoid:** The "LOST" state from environment change requiring full re-recording. Our system's answer to this is the POCD-style change-detection loop in [[world-model-architecture]] — relocalize, detect what changed, update only the affected region, version-stamp.

### L2: Camera-only is viable for manipulation; LiDAR helps navigation

Figure's 6-camera-only approach demonstrates that camera-only perception is sufficient for open-vocabulary manipulation of household objects at high success rates. The key is: enough cameras (including palm cameras for occluded views), plus a VLM capable of real-time scene understanding.

For navigation in a home environment (avoiding obstacles, navigating corridors), LiDAR simplifies localization in low-texture environments. Digit's torso-mounted LiDAR + RealSense depth combination reflects this: LiDAR for long-range navigation/mapping, depth cameras for local manipulation perception. A home tidy robot on a budget can use a 2D LiDAR for navigation (see [[cheap-lidar-pricing-guide]], [[2d-lidar-slam]]) plus close-range depth (see [[close-range-depth-sensors]]) for grasping.

### L3: The two-tier compute architecture is the right model

Figure's S1/S2 split (fast reactive control at 200 Hz + slow semantic reasoning at 7–9 Hz) mirrors the architecture our project targets: a fast local reactive loop on the robot, with slower semantic task planning on a server. The Spot + Orbit split is the same at a different level — Spot handles real-time navigation; Orbit handles fleet-level semantic analysis on a server.

For our project (see [[system-architecture]]): onboard compute handles reactive obstacle avoidance + SLAM; server (home PC/NUC) handles scene graph maintenance, LLM task planning, and between-session map updates. No cloud dependency for real-time operation.

### L4: The "logistics-first" vs "home-first" design tension is real

Digit and Apollo deliberately sacrifice object-class generalization to achieve commercial deployment on a constrained task set. Figure and 1X NEO pursue open-vocabulary generalization at the cost of deployment maturity. For a home-tidy robot, the correct answer is **language-grounded open-vocabulary detection at grasp range** — the TidyBot insight (see [[home-tidying-robots]]) — not a fixed class list. The object domain of a home is too diverse. Figure's Helix approach (VLM-grounded zero-shot picking) is the right architecture at the manipulation layer.

### L5: The semantic inspection (Orbit) model is the right model for the robot's server layer

Orbit's AIVI-Learning approach — Spot captures images at pre-defined inspection points; Orbit analyzes them via vision-language prompts; anomalies are flagged with semantic labels — is structurally identical to what a home tidy robot's server brain should do: robot visits rooms on a patrol schedule; server analyzes images for objects out of place; server routes tasks back to robot. The Gemini Robotics-ER integration (natural language task planning driving API calls) is the advanced version of this.

The practical transfer: VLP prompts at named locations ("kitchen counter", "living room floor") are a tractable entry point for semantic monitoring. Full scene-graph reconstruction (see [[scene-graph-world-model]]) is the richer version but requires more compute.

---

## 8. The Semantic Mapping Survey Context

The arXiv 2501.05750 survey (SFU, Raychaudhuri & Chang, 2025) categorizes semantic map representations along two axes: **structure** (topological graph, spatial grid, dense geometric, hybrid) and **semantic encoding** (explicit labels vs implicit learned features). [src: semantic-mapping-survey-2025]

Key finding from the survey: *"The field is moving towards developing open-vocabulary, queryable, task-agnostic map representations, while high memory demands and computational inefficiency still remain as open challenges."* [src: semantic-mapping-survey-2025]

This maps directly to the platforms above: Spot's GraphNav is a topological graph with explicit waypoint annotations (classical structure); Figure's Helix is a pure implicit learned-feature system (no persistent map); the research systems in [[scene-graph-world-model]] (ConceptGraphs, Hydra, DovSG, HOV-SG) are the frontier hybrid approaches that combine both.

---

## 9. Known Gaps in Public Disclosure

*(editorial — flags where source coverage is thin)*

1. **Figure's between-session state:** Nothing in the Helix v1 or Helix 02 posts addresses how Figure robots handle returning to the same environment across sessions — whether they re-perceive from scratch or have any form of persistent state. This is the central gap in the Figure documentation.

2. **1X NEO's full stack:** The 1x.tech website is consistently bot-walled. The technical architecture of Redwood AI (their VLA), the SLAM algorithm, and any persistent map system are not publicly documented in any capturable source.

3. **Agility Digit's SLAM algorithm:** The torso-mounted LiDAR + RealSense suite is disclosed; the algorithm (whether it's SLAM Toolbox, RTAB-Map, or a proprietary stack) is not.

4. **Apptronik Apollo's full perception stack:** The Robot Report unveiling article is primarily about form factor and business strategy. Sensor and software architecture are not disclosed.

5. **Boston Dynamics Atlas humanoid perception (SuperTracker):** The "Making Atlas See the World" blog post (primary source for Atlas's per-object tracking system) was bot-walled in all capture attempts. This page is the primary technical source for Atlas's manipulation perception and is the missing piece for a complete Boston Dynamics picture.
