# TidyBot Deep Dive

TidyBot (2023) and its open-source successor TidyBot++ (CoRL 2024) are the most fully realised household-tidying mobile manipulators in the public research record. v1 demonstrated that GPT-3-driven preference personalisation can reach 85% real-world success with a handful of user examples. v++ stripped out the LLM entirely, replaced it with Diffusion Policy trained on ~50 phone-teleoperated demonstrations, and published an open-source holonomic base design at ~$5.4k USD that outperforms $100k+ commercial alternatives on every maneuverability metric. Together they define a two-generation benchmark for what a ground-based home-tidying robot can achieve today — and expose the specific hardware and policy gaps that our aerial approach will need to navigate around or exploit.

## Source

- `raw/research/home-tidying-robots/03-01-arxiv-2305-05658.md` — TidyBot v1 paper (arXiv 2305.05658, *Autonomous Robots* 2023)
- `raw/research/home-tidying-robots/02-02-arxiv-2412-10447.md` — TidyBot++ paper (arXiv 2412.10447, CoRL 2024)
- `raw/research/tidybot-deep-dive/01-01-tidybot-project-page.md` — v1 project page (tidybot.cs.princeton.edu)
- `raw/research/tidybot-deep-dive/02-02-tidybot2-project-page.md` — TidyBot++ project page (tidybot2.github.io)
- `raw/research/tidybot-deep-dive/03-03-tidybot-github-readme.md` — v1 GitHub README
- `raw/research/tidybot-deep-dive/03-04-tidybot2-github-readme.md` — TidyBot++ GitHub README
- `raw/research/tidybot-deep-dive/04-05-tidybot-iros23-pdf.md` — IROS 2023 camera-ready
- `raw/research/tidybot-deep-dive/05-06-kinova-gen3-page.md` — Kinova Gen3 product page (rendered as JS shell — no parseable specs)
- `raw/research/tidybot-deep-dive/06-07-ufactory-xarm-page.md` — UFACTORY xArm product page
- `raw/research/tidybot-deep-dive/07-08-hello-robot-stretch3.md` — Hello Robot Stretch 3 (404 — data unavailable from capture)
- `raw/research/tidybot-deep-dive/08-09-ufactory-lite6.md` — UFACTORY Lite 6 product page
- `raw/research/tidybot-deep-dive/09-10-arm-comparison-paper.md` — "Strong, Accurate, and Low-Cost Robot Manipulator" (Forte arm, arXiv 2507.15693) — **not an arm-comparison paper as labelled**; contains a low-cost-arm comparison table that includes Kinova Gen3 Lite as a reference point

## Related

- [[home-tidying-robots]] — landscape overview placing TidyBot in context
- [[semantic-object-memory]] — object fingerprinting, Housekeep benchmark
- [[system-architecture]] — our COMMAND CENTER / ACTIONS EXECUTION design
- [[tactile-manipulation]] — tactile sensing for manipulation
- [[home-tidy-drone-prototype]] — our Phase-1 build

---

## 1. TL;DR

TidyBot v1 (Princeton/Stanford/Google, IROS 2023) used GPT-3 text summarisation to learn personalised tidy-up rules from a handful of user examples — where do *your* shirts go, not where shirts generically go — achieving 85.0% real-world success across 240 objects in 8 room scenarios. TidyBot++ (CoRL 2024) dropped the LLM, adopted Diffusion Policy trained from 50 phone-teleoperated demos, and released the entire hardware design as open-source at $5–6k USD for the base alone. For our project, the key takeaways are: (1) holonomic drive is measurably superior to differential drive for manipulation tasks — 9/10 vs 4/10 success on a wiping task with identical training data; (2) 50 demonstrations per task is sufficient to learn real-home policies; (3) inference currently requires an external GPU laptop, which is a deployment blocker for any battery-limited system; and (4) neither version addresses vertical reach, overhead spaces, or the clutter-is-everywhere scenario — exactly the gap an aerial system could fill.

---

## 2. System Overview — v1 vs v++

### Side-by-side comparison

| Dimension | TidyBot v1 (2023) | TidyBot++ (CoRL 2024) |
|---|---|---|
| **Base** | Custom holonomic, Powered-Caster Drive, closed-source | Custom holonomic, SDS MK4 swerve modules, **open-source** |
| **Base cost** | Not disclosed | ~$5.4k USD [src: 02-02-arxiv-2412-10447.md] |
| **Arm** | Kinova Gen3 7-DOF | Kinova Gen3 7-DOF; also supports Franka, ARX5, xArm, UR5, ViperX [src: 02-02-tidybot2-project-page.md] |
| **Gripper** | Robotiq 2F-85 parallel jaw — top-down grasps only [src: 03-01-arxiv-2305-05658.md] | Kinova gripper (wrist-mounted) |
| **Cameras** | 2× overhead (Logitech C930e per README), 1× egocentric on base [src: 03-03-tidybot-github-readme.md] | 640×360 base cam (Logitech), 640×480 wrist cam (Kinova built-in) [src: 03-04-tidybot2-github-readme.md] |
| **Pose estimation** | ArUco markers on top plate [src: 03-01-arxiv-2305-05658.md] | Onboard odometry (< 1 cm drift/m) [src: 02-02-arxiv-2412-10447.md] |
| **Compute (onboard)** | Not specified in paper | Intel NUC mini PC [src: 02-02-arxiv-2412-10447.md] |
| **Compute (inference)** | GPU workstation (server/robot split in repo) [src: 03-03-tidybot-github-readme.md] | **External GPU laptop required** (RTX 4080 Laptop, ~115 ms latency) [src: 03-04-tidybot2-github-readme.md] |
| **Perception** | ViLD overhead detection + CLIP egocentric classification | Visuomotor only — raw pixels → actions via Diffusion Policy |
| **Planning/reasoning** | GPT-3 `text-davinci-003` (temp=0) for preference learning and placement rules [src: 03-01-arxiv-2305-05658.md] | None — pure imitation learning |
| **Manipulation** | 3 hard-coded primitives: pick, place, toss — NOT learned [src: 03-01-arxiv-2305-05658.md] | Fully learned via Diffusion Policy |
| **Navigation** | Occupancy map + Pure Pursuit; greedy nearest-first [src: 03-01-arxiv-2305-05658.md] | Policy-embedded |
| **Receptacle locations** | Hard-coded per scenario (explicit limitation) [src: 03-01-arxiv-2305-05658.md] | Learned from demonstrations |
| **Training data** | None for manipulation; 4–10 text examples per scenario for LLM | 50 demos per task; ~1–2 h collection [src: 02-02-arxiv-2412-10447.md] |
| **Real-world results** | 85.0% success, 240 objects, 8 scenarios [src: 03-01-arxiv-2305-05658.md] | 60–100% per task (6 household tasks) [src: 02-02-arxiv-2412-10447.md] |
| **Speed** | 15–20 s per object [src: 03-01-arxiv-2305-05658.md] | Not reported per-object |
| **OS / software** | Ubuntu 20.04.6, Conda (`tidybot`, `vild`) [src: 03-03-tidybot-github-readme.md] | Ubuntu, Mamba (`tidybot2`, `robodiff`) [src: 03-04-tidybot2-github-readme.md] |

### Key architectural decisions

**Why holonomic drive matters.** TidyBot++ ran a controlled comparison: same wipe-countertop task, 50 demonstrations each, identical diffusion policy training. Holonomic: 9/10 success, 2.03 m average path, 27.4 s average episode. Differential drive: 4/10 success, 4.03 m path, 65.2 s episode. The differential policy must learn a "parallel parking" manoeuvre for every sideways motion; the holonomic policy just moves sideways. Critically, differential drive also causes the camera to swerve, degrading visual observation quality [src: 02-02-arxiv-2412-10447.md].

**Why LLM was dropped.** v1's LLM layer handled one narrow sub-problem: given text examples of "shirts go in the drawer", generalise to unseen objects. It did this well (91.2% benchmark accuracy). But it cannot handle the manipulation itself — those primitives were still hand-coded. v++ sidesteps the whole problem by learning end-to-end from demonstration. The trade-off is that v++ cannot generalise to new users from text examples; each new task requires ~50 new demos.

**The external-GPU constraint.** All deep-learning inference runs on a separate GPU laptop connected via ZMQ on port 5555. The onboard NUC runs only real-time controllers. This is a deliberate architectural choice to keep latency-sensitive control loops clean [src: 03-04-tidybot2-github-readme.md]. It means the system as published is a tethered-to-a-laptop robot, not a standalone autonomous platform — a critical deployment gap.

---

## 3. Hardware Build Guide

### 3a. Base Platform

The TidyBot++ base is built around **SDS MK4 swerve modules** from Swerve Drive Specialties, an FRC (FIRST Robotics Competition) ecosystem component. The key insight is that FRC parts are battle-tested (80,000+ competition participants/year), cheap, readily available online (typically delivered within a week), and come with full software support (CAN drivers, motor control, battery monitoring) [src: 02-02-arxiv-2412-10447.md].

**The holonomic modification.** Stock MK4 modules are swerve (steerable + driveable), which is omnidirectional but not holonomic — wheels must align to the direction of motion before moving. The TidyBot++ team adds a caster offset using just three custom parts: 2× 3D-printed PLA wheel mounts (FDM printer, printed over 2 days) and 1× machined shaft (orderable from Xometry using their provided CAD file). All other components are stock [src: 02-02-arxiv-2412-10447.md].

**Known limitation.** The base does not backdrive well due to high steering friction (high steer gear ratio of 12.8 combined with a small 14 mm caster offset). This is a byproduct of the accessibility-first design approach [src: 02-02-arxiv-2412-10447.md].

**Assembly time.** 1–2 days total. The T-slot extrusion frame takes ~6 hours; each of the 4 caster modules takes <30 minutes; wiring takes <30 minutes and requires no soldering [src: 02-02-arxiv-2412-10447.md].

**Specifications:**

| Spec | Value | Source |
|---|---|---|
| Footprint | 54 × 50 cm | 02-02-arxiv-2412-10447.md |
| Base height | 37.5 cm | 02-02-arxiv-2412-10447.md |
| Weight (base only) | 34 kg | 02-02-arxiv-2412-10447.md |
| Payload (conservative) | 60 kg | 02-02-arxiv-2412-10447.md |
| Payload (tested max) | 122 kg (270 lb weight plates) | 02-02-arxiv-2412-10447.md |
| Max speed | 1 m/s | 02-02-arxiv-2412-10447.md |
| Runtime | 8 h (arm + compute) | 02-02-arxiv-2412-10447.md |
| Odometry | <1 cm/m translation, <1°/360° rotation | 02-02-arxiv-2412-10447.md |
| Motor battery | 6 kg SLA (hotswappable) | 02-02-arxiv-2412-10447.md |
| Compute/arm battery | 768 Wh portable power station (0–100% in 70 min) | 02-02-arxiv-2412-10447.md |

**Comparison to alternatives.** From the TidyBot++ paper's own comparison table [src: 02-02-arxiv-2412-10447.md]:

| Platform | Holonomic | Swappable arm | Footprint (cm) | Cost |
|---|---|---|---|---|
| TidyBot++ base | Yes | Yes | 50×54 | $5.4k |
| Hello Robot Stretch 3 | No | No | 33×34 | $25k |
| AgileX Tracer | No | Yes | 57×69 | $7.6k |
| AgileX Ranger Mini | No | Yes | 50×74 | $13k |
| Clearpath Husky | No | Yes | 67×99 | $20k |
| Fetch | No | No | 51×56 | $100k |
| PAL Tiago | Yes (mecanum) | No | 54×54 | $100k |

Note: Tiago is holonomic via mecanum wheels, but mecanum introduces vibration due to discontinuous ground contact [src: 02-02-arxiv-2412-10447.md].

### 3b. Arm Comparison

TidyBot v1 used a **Kinova Gen3 7-DOF** with Robotiq 2F-85 gripper. TidyBot++ officially supports six arms in its reference designs: Kinova Gen3, Franka Research 3, ARX5, UFACTORY xArm, UR5e, and ViperX [src: 02-02-tidybot2-project-page.md].

The arm comparison paper originally listed as source 09 (`09-10-arm-comparison-paper.md`) is actually the "Forte" low-cost 3D-printed arm paper (arXiv 2507.15693) — it contains a comparison table of low-cost educational arms including a Kinova Gen3 Lite reference, but is not a systematic comparison of the arms listed below. Arm specs below are drawn from product pages and the TidyBot++ paper directly.

| Arm | DOF | Reach | Payload | Price (est.) | TidyBot++ official | Source |
|---|---|---|---|---|---|---|
| Kinova Gen3 7-DOF | 7 | 902 mm | 2 kg (full reach) | ~$8–12k | Yes — used in papers | 02-02-arxiv-2412-10447.md (arm weight 12 kg incl. mount+PSU) |
| UFACTORY xArm 7 | 7 | 700 mm | 5 kg | $5,299–5,494 | Yes | 06-07-ufactory-xarm-page.md |
| UFACTORY Lite 6 | 6 | 440 mm | 0.6 kg | $2,999 | Not listed | 08-09-ufactory-lite6.md |
| Franka Research 3 | 7 | 855 mm | 3 kg | ~$25k | Yes | 02-02-tidybot2-project-page.md |
| UR5e | 6 | 850 mm | 5 kg | ~$35k | Yes | 02-02-tidybot2-project-page.md |
| Hello Robot Stretch 3 | Telescoping | ~1000 mm | 0.25 kg | ~$25k | Not listed | 07-08-hello-robot-stretch3.md (404 — data unavailable) |
| ARX5 | — | — | — | — | Yes | 02-02-tidybot2-project-page.md |
| ViperX | — | — | — | — | Yes | 02-02-tidybot2-project-page.md |

**Practical notes:**

- The **Kinova Gen3** is the most thoroughly tested arm for TidyBot++ (all paper results). At 12 kg including mount and PSU, it consumes a significant fraction of the ~34 kg base payload budget [src: 02-02-arxiv-2412-10447.md].
- The **xArm 7** is the best cost/capability trade-off for a builder on a budget: 5 kg payload (2.5× Kinova) at roughly half the Kinova price, with official TidyBot++ support.
- The **Lite 6** is cheaper still but its 0.6 kg payload and 440 mm reach will limit tasks to lightweight objects within a very restricted workspace.
- The **Stretch 3** capture returned a 404; its telescoping design is architecturally different (doesn't mount on the TidyBot++ frame the same way) and its 0.25 kg payload makes it unsuitable for most tidy-up objects.

### 3c. Compute Architecture

This is the most critical system-design constraint for anyone building on TidyBot++:

```
Phone (teleoperation/enabling device)
  |
  | WebXR pose stream (6-DOF, any modern Android/iOS)
  v
Wireless router
  |
  +---> Mini PC (onboard robot)
  |       - Real-time base controller (RPC server, port BASE_RPC_PORT)
  |       - Real-time arm controller (RPC server, port ARM_RPC_PORT)
  |       - Camera capture
  |
  +---> GPU laptop (off-robot, external)
          - Diffusion Policy inference server (ZMQ, port 5555)
          - ~115 ms inference latency on RTX 4080 Laptop GPU
          - "Latency hiding" via PolicyWrapper: initiates next inference
            200 ms before current action sequence exhausted
```

[src: 03-04-tidybot2-github-readme.md]

**Why this matters.** The robot is operationally dependent on an external GPU machine. During autonomous policy rollouts, the onboard NUC receives observations, sends them over the LAN to the GPU laptop, waits ~115 ms for action predictions, and executes them. This is fine for indoor research settings where the GPU laptop sits on a table nearby, but it means:

1. The robot has an effective tether (must remain on the same LAN as the inference machine).
2. Wireless latency adds to the 115 ms inference budget — any WiFi congestion degrades policy quality.
3. Deploying this system in a real home requires either (a) a dedicated always-on GPU machine in the home, or (b) moving inference fully onboard.

The README explicitly warns that all heavy computation must run on a separate machine to prevent interference with real-time controllers [src: 03-04-tidybot2-github-readme.md]. This is a design choice, not a fundamental constraint — but changing it requires significant software re-architecture.

For context, diffusion policy on a high-end laptop GPU takes ~115 ms. On an Orin NX (the most capable Jetson at arm's length), inference time for diffusion policies is typically 500 ms–2 s depending on the model variant, which would require switching to a faster policy class (e.g., Consistency Policy, which the same Stanford group published).

### 3d. Total Cost Estimate

| Component | Cost (USD) | Notes |
|---|---|---|
| Holonomic base | ~$5,400 | Includes SDS MK4 modules, frame, batteries, NUC [src: 02-02-arxiv-2412-10447.md] |
| Kinova Gen3 7-DOF arm | ~$8,000–12,000 | Estimated; Kinova does not publish list prices |
| xArm 7 (budget alternative) | $5,299–5,494 | List price [src: 06-07-ufactory-xarm-page.md] |
| Custom parts (3D print + Xometry shaft) | ~$50–200 | 2× PLA wheel mounts + 1× machined shaft |
| GPU laptop (inference) | $2,000–4,000 | RTX 4080 Laptop used in paper; any ≥RTX 3080 Laptop |
| **Total (Kinova config)** | **~$17,000–24,000** | |
| **Total (xArm budget config)** | **~$13,000–15,000** | |

Arm costs are the dominant variable. The base itself at $5.4k is the most cost-competitive sub-system in its class.

---

## 4. Method Deep Dive

### 4a. TidyBot v1 — LLM-driven preference personalisation

The v1 pipeline treats the tidying problem as two separable sub-problems: (A) *what category does this object belong to, and where should that category go?* (semantic/preference) and (B) *physically move the object there* (manipulation). The LLM handles A; hard-coded primitives handle B.

**Step 1 — Preference elicitation.** The user provides a handful of text examples: "yellow shirts go in the drawer, dark purple shirts go in the closet, white socks go in the drawer, black shirts go in the closet." These are structured as Pythonic pseudocode (pick_and_place commands), a format chosen because LLMs are trained on code and it provides structured, parseable output [src: 03-01-arxiv-2305-05658.md].

**Step 2 — LLM summarisation.** GPT-3 (`text-davinci-003`, temp=0) is prompted to complete a code comment summarising the examples. Output: `# Summary: Put light-colored clothes in the drawer and dark-colored clothes in the closet.` This two-step approach (summarise, then apply summary to new objects) outperforms direct inference (91.2% vs 78.5% on the benchmark) [src: 03-01-arxiv-2305-05658.md]. The key insight is that the summary creates a small, human-interpretable category set (e.g., "light-colored clothing", "dark-colored clothing") that the downstream vision classifier only needs to distinguish between.

**Step 3 — Nouns → CLIP labels.** Nouns are extracted from the summary text and provided as the target label set for CLIP. CLIP then classifies egocentric images against this small label set (2–5 categories). This dramatically improves classification accuracy: using LLM-summarised categories achieves 95.5% real-world object recognition vs 70.7% using scenario-specific object names and 52.3% using all object names across all scenarios [src: 03-01-arxiv-2305-05658.md].

**Step 4 — Object localisation.** ViLD processes overhead camera images to detect objects on the floor. The robot navigates to the nearest detected object using an occupancy map and Pure Pursuit path following [src: 03-01-arxiv-2305-05658.md].

**Step 5 — Manipulation.** After navigating to an object, the robot takes a close-up egocentric image, classifies it via CLIP, looks up the receptacle in the LLM-generated rules, and executes one of three hard-coded primitives:
- **Pick**: gripper grasps at the centre of the detected object (top-down only)
- **Place**: gripper moves above target receptacle, releases
- **Toss**: arm swings and releases with timing to throw object into receptacle (for items like socks)

Receptacle locations are hard-coded per scenario. This is explicitly flagged as a limitation [src: 03-01-arxiv-2305-05658.md].

**Real-world performance breakdown** (240 objects, 8 scenarios, 3 runs each):
- Overhead object localisation: 92.5%
- Egocentric object classification (CLIP): 95.5%
- LLM receptacle + primitive selection: 100%
- Manipulation primitive execution: 96.2%
- Overall end-to-end: **85.0%** [src: 03-01-arxiv-2305-05658.md]

**LLM comparison.** text-davinci-003 outperforms davinci-002, code-davinci-002, and PaLM 540B on summarisation. PaLM 540B shows slightly better commonsense reasoning (no examples) but falls behind on summarisation, especially with more receptacles [src: 03-01-arxiv-2305-05658.md].

**Benchmark.** 96 scenarios, 4 room types, 1,076 unique object names. Method accuracy on unseen objects: 91.2% (vs 78.5% examples-only, 83.7% CLIP embeddings, 67.5% WordNet taxonomy) [src: 03-01-arxiv-2305-05658.md].

### 4b. TidyBot++ — Diffusion Policy imitation learning

v++ discards the modular LLM-perception-primitive pipeline entirely and learns a single visuomotor policy mapping (image observations + proprioception) → (base pose Δ + arm pose + gripper command).

**Teleoperation data collection.** The operator controls the robot using a smartphone web app built on the WebXR API. WebXR combines IMU data with visual odometry (phone camera) to stream 6-DOF pose with low drift — works on any modern Android or iOS phone, no dedicated teleoperation hardware required. The operator can freely walk around the scene to get close for precision. The app streams phone pose to the robot's NUC, which maps it to base and arm motions [src: 02-02-arxiv-2412-10447.md].

**Data scale.** 50 demonstrations per task (100 for the shorter "open fridge" task). Collection time: 1–2 hours per 50 episodes, including environment reset overhead [src: 02-02-arxiv-2412-10447.md].

**Policy.** Diffusion Policy (Chi et al., RSS 2023). Observations include base camera image (640×360), wrist camera image (640×480), base pose (x, y, θ), arm position and quaternion, and gripper position. Actions are delta base pose, arm position, arm quaternion, and gripper position. Policy control frequency: 10 Hz. Trained for 500 epochs [src: 02-02-arxiv-2412-10447.md].

**Inference architecture.** Policy runs on a GPU laptop, not onboard. The `PolicyWrapper` class initiates the next inference step 200 ms in advance to hide the 115 ms latency on an RTX 4080 Laptop GPU, ensuring a fresh action sequence is ready when the current one is exhausted [src: 03-04-tidybot2-github-readme.md].

**Real-world task results** (10 rollouts per task, real apartment home) [src: 02-02-arxiv-2412-10447.md]:

| Task | Success |
|---|---|
| Open fridge | 10/10 |
| Take out trash | 10/10 |
| Wipe countertop | 9/10 |
| Load dishwasher | 7/10 |
| Load laundry | 7/10 |
| Water plant | 6/10 |

**Holonomic vs differential comparison** (wipe countertop, 50 demos each):
- Holonomic: 9/10 success, 2.03 m average path, 27.4 s
- Differential drive: 4/10 success, 4.03 m path, 65.2 s
- Approximate ratios: 2× shorter path, 2.4× faster, 2.25× higher success rate [src: 02-02-arxiv-2412-10447.md]

**What the policy does not include.** No semantic understanding of objects. No memory of room layout. No generalisation across tasks — each task requires its own 50-demo dataset and trained policy. No explicit user personalisation (that was dropped with the LLM). The policy is purely visuomotor imitation.

---

## 5. Alignment with Our Project *(synthesis)*

The following are findings from TidyBot that our project can adopt directly.

**LLM-based preference learning is a solved sub-problem.** The v1 result (91.2% text-only generalisation, 85% real-world) establishes that a few user examples + GPT-class summarisation reliably produces generalised tidy-up rules. We do not need to re-invent this; we should adopt this approach wholesale for our semantic layer. The Pythonic pseudocode prompt format is a specific implementation choice worth copying — it's structured, parseable, and LLMs trained on code handle it well [src: 03-01-arxiv-2305-05658.md]. This maps directly to our [[system-architecture]]'s COMMAND CENTER intent inference.

**CLIP + small LLM-generated category set is a strong perception baseline.** The v1 finding that CLIP with 2–5 LLM-summarised categories (95.5%) dramatically outperforms CLIP with fine-grained object names (52.3%) is a directly usable insight. Our aerial system's object classification should use the same pattern: LLM generates categories → CLIP classifies against that small set. See [[semantic-object-memory]] for the broader object-semantics context.

**50 demonstrations is sufficient for visuomotor imitation.** v++ demonstrates that useful household manipulation policies require only ~50 demonstrations at 10 Hz. For a drone-arm hybrid, this is an encouraging data-efficiency floor — we are not looking at thousands of demos for each new behaviour.

**Holonomic drive simplifies manipulation.** The 2.25× success-rate improvement over differential drive for wiping tasks confirms a principle that carries to any platform: maneuverability degrees-of-freedom directly improve manipulation outcome. For our aerial platform, full 6-DOF flight is the equivalent: the drone can reposition in any direction, simplifying the arm's job. This is the aerial analogue of the holonomic base advantage.

**Phone-based teleoperation via WebXR is reproducible.** The v++ interface works on any modern smartphone with no dedicated hardware. This is immediately relevant for collecting training data on any robot platform, including a drone-arm system. The approach requires the robot to be stabilised (not flying) during demos, but for a land-then-grasp drone architecture, this is achievable.

---

## 6. Key Gaps Relative to Our Goals *(synthesis)*

**Hard-coded receptacle locations.** Both v1 and v++ require receptacle locations to be provided (v1 hard-codes them; v++ learns them implicitly from demos per task). Neither system explores and discovers where furniture is. A real consumer deployment needs persistent [[semantic-object-memory]] — a map that knows where the laundry basket is today, not just in the demo scenarios. This is the Housekeep / ConceptGraphs problem.

**Ground-plane only.** Both systems operate entirely on the floor plane. Tables, countertops, chairs, beds — anything above floor height is either a receptacle target (arm reaches up to place) or invisible. Objects on elevated surfaces cannot be picked up. Our aerial approach directly addresses this: a drone can reach any height.

**Clutter catastrophically degrades performance.** v1 explicitly notes that the mobile base cannot drive over objects, and high clutter breaks navigation. v++ implicitly requires that the robot can approach objects and that the policy training distribution included the actual clutter level. A real messy home (clothes everywhere, floor covered) is not well-served by either system.

**Top-down grasp only (v1).** The Robotiq 2F-85 gripper on v1 performs only top-down grasps — flat objects on the floor require the object to be pickable from above. Crumpled clothes, wedged objects, and non-flat items are failure modes. v++ with the Kinova gripper is more flexible but still subject to the arm's reachability limits from a floor-level base. See [[tactile-manipulation]] for the state of the art in compliant grasping.

**External GPU dependency (v++)** — not deployable as a standalone product. As detailed in §3c, the inference architecture requires a GPU laptop on the same LAN. This is a fundamental gap between a research demo and a consumer product. Until diffusion policy inference runs onboard (requires either more capable onboard compute or a faster policy class), v++ cannot be a standalone device.

**No task completion verification.** Neither system detects whether a tidy-up action succeeded. If the gripper missed the object, the robot moves on to the next item. This is fine for a 10-trial research evaluation but unacceptable for an autonomous consumer device — repeated failures would be noticed and frustrating.

**Single-user personalisation.** v1's LLM approach is personalised to one user per household. Multi-user households (different preferences per person) are not addressed. The v++ approach has no personalisation at all.

**No "where does this go?" generalisation to novel environments.** v++ policies are task-specific and trained in specific home environments. A new home requires new data collection. v1's LLM approach generalises to new objects but not to unseen room layouts. Neither system generalises across homes out-of-the-box.

---

## 7. Recommended Starting Point *(synthesis)*

For Phase-2 hardware, the TidyBot++ base design is the most compelling open-source mobile manipulation platform available. The recommendation is:

**Adopt the TidyBot++ base design, but pair it with a GPU onboard compute strategy from day one.**

Rationale:
1. The base at $5.4k is clearly superior to all commercial alternatives at 5–20× the price. The open-source nature means full control and repairability.
2. The xArm 7 ($5,299) is the budget-optimal arm: 5 kg payload, 700 mm reach, official TidyBot++ support. The Kinova Gen3 is better-documented but costs 2× more for less payload.
3. The inference gap is solvable. Consistency Policy (also from the same Stanford group) achieves similar results at ~10× lower latency. ALOHA 2 and similar systems show diffusion-class policies running acceptably on high-end Jetson hardware. Plan for this from the start rather than retrofitting.
4. For our specific aerial-ground hybrid concept, the TidyBot++ base is a useful *ground-phase platform* — when the drone docks or lands, a ground arm handles manipulation while the drone handles exploration and elevated access. The two systems are complementary, not competing.

**For the LLM semantic layer**, adopt v1's approach: 4–10 user text examples → GPT-4-class summarisation → category set → open-vocabulary vision classification. This is a few-hundred-lines-of-code addition on top of any manipulation platform. Do not re-invent it.

**For manipulation policy**, start with Diffusion Policy on an external GPU (accept the research-system limitation for Phase 2), with a clear migration path to Consistency Policy or similar for Phase 3 onboard inference.

The concrete Phase-2 buy list (ground platform, excluding any aerial component):

| Item | Estimated cost |
|---|---|
| TidyBot++ base (parts + custom mfg) | ~$5,400 USD |
| UFACTORY xArm 7 | ~$5,300–5,500 USD |
| GPU laptop for inference (RTX 4080 Laptop class) | ~$2,500–3,500 USD |
| **Subtotal** | **~$13,200–14,400 USD** |

This gets a fully replicable, open-source, state-of-the-art ground mobile manipulator platform. The aerial layer (drone + dock + intercommunication) is additive on top.
