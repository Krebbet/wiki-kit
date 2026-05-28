# Drone System Architecture — Full Stack

Top-down design of all subsystems required for a home-tidy autonomous drone. The goal state: a consumer indoor drone that learns a house, accepts voice commands, and autonomously completes household tidying tasks. This page records the proposed architecture, critiques it, adds missing components, proposes a revised phased roadmap, and surfaces the hardest unsolved problems.

For the Phase-1 physical build (flight + SLAM + comms), see [[home-tidy-drone-prototype]].

---

## Proposed subsystems *(with critique)*

### 1. WORLD MAP

> *Internal representation of the total area — permanent vs movable vs living objects. Mostly stored and updated off-drone; some current-state snapshot lives onboard.*

**What's right.** The permanent / movable / living tripartition is the correct split; each class needs different handling. A static geometry layer (walls, fixed furniture) can be built once and kept stale. A movable-objects layer needs timestamps and confidence decay. A living-objects layer (people, pets) is safety-critical and ephemeral — it should never persist across flights, only be detected live.

**Gaps and concerns.**

- *Who builds the first map?* There needs to be an explicit **initial exploration mode** — the drone doing a room-by-room walkthrough before it can navigate. This is a precondition to everything else and it has no trigger in the current design.
- *Map update policy is underspecified.* A toy moved from the living room to the kitchen doesn't trigger a world-update naturally. The drone needs a *staleness* mechanism: every observed object has a confidence that decays with time; if the drone re-observes a location and an object is gone, it updates. If it doesn't re-visit, the object stays on the map with decaying confidence.
- *"Off drone vs onboard" split needs a protocol.* What exactly is on-drone? Probably: a compressed local occupancy map for obstacle avoidance (must survive WiFi dropout). The full semantic map lives in the Command Center. You need a defined sync protocol — delta diffs, not full-map pushes.
- *Semantic layers aren't one map.* In practice this is three or four distinct datastores: (a) geometric occupancy (for nav), (b) static-semantic (rooms, doors, furniture identity), (c) dynamic-object-memory (toys, cups, remotes — location + identity + last-seen), (d) people/pets (live, not persisted). Treat them that way from the start or you'll refactor painfully.

---

### 2. STATE UNDERSTANDING

> *Where am I right now? Probably SLAM. Should constantly challenge whether internal state aligns with world state. If misaligned: decide whether to update the world or update self.*

**What's right.** SLAM (LiDAR-inertial or visual-inertial) is the right answer for real-time pose estimation in a GPS-denied indoor environment. [[slam]] and [[fast-lio-mid360-orin]] are the relevant starting points. The self-challenge loop ("does my current pose prediction match what I observe?") is sound — this is essentially loop-closure + consistency checking.

**Gaps and concerns.**

- *"Update world model vs update STATE" is harder than it sounds.* If the drone rounds a corner and the hallway doesn't look like the map, there are three explanations: (a) the drone is lost (update pose), (b) something changed (update map), (c) the sensor is lying (sensor fault). These look identical from the drone's perspective. There is no clean rule; in practice SLAM systems resolve this via probabilistic hypotheses and loop closure — but the disambiguation policy needs to be explicit in the design.
- *Localization confidence is a first-class signal.* The STATE module needs to emit not just a pose estimate but a **confidence level**. When confidence drops below a threshold (e.g. long featureless corridor, dark room), the drone should degrade gracefully: slow down, seek features, or hold position — not blindly continue. This confidence monitor is a distinct subsystem that bridges STATE UNDERSTANDING and AUTONOMOUS NAVIGATION.
- *First requirement: just the minimal buy list.* Before full SLAM, the fiducials-first staging in [[home-tidy-drone-prototype]] is correct — AprilTag + optical-flow proves the EKF / FC integration on a known-good position source before SLAM enters the loop.

---

### 3. AUTONOMOUS NAVIGATION

> *Execute "go here" commands. Avoid obstacles. Interpret object types. Identify obstacles it can't overcome (closed door). Safe and non-destructive.*

**What's right.** The functional decomposition is correct: global planner (where to go), local planner (how to get there reactively), obstacle classification (can I pass? can I ask for help?). Closed-door detection as an "obstacle I can't overcome alone" is a good concrete example of the needed semantic awareness.

**Gaps and concerns.**

- *"Interpret types of objects" is a perception problem, not a navigation problem.* Whether the path is blocked by a closed door vs a box it could push vs a cat it must avoid requires semantic labels from the PERCEPTION PIPELINE (a missing subsystem — see below). Navigation should consume those labels, not generate them.
- *Recovery behaviours need to be specified.* What does the drone do when it can't reach its goal? Options: wait, backtrack, re-plan with the obstacle marked, call the Command Center, return to base. This decision tree needs to be designed; leaving it as "identify obstacles it can't overcome" without recovery behaviours leads to the drone silently stalling.
- *Safety hierarchy must be explicit.* Obstacle avoidance is not just a navigation concern — it overlaps with the SAFETY ARBITER (see missing components below). The safety layer runs at higher priority than navigation; they must not be conflated.

---

### 4. ACTIONS EXECUTION

> *Pick up and place simple objects. V1 focus: only physical manipulation capability, not task reasoning. User thinking: just the "can pick up and place" layer.*

**What's right.** Splitting physical manipulation from task-level understanding is the right architectural call. The manipulation layer is a real-time control problem (grasp, lift, carry, place); the task-level problem (what to pick up, where it goes) belongs in the Command Center. Keeping V1 scoped to known/light objects is correct — [[aerial-grasping]] shows even lab-grade drone grippers top out at ~150–217 g payload with known objects.

**Design principle: land-then-grasp preferred over hover-grasp.**

When a landing surface is available near the target object, the drone should land, grasp from the ground, then take off — rather than hovering while grasping. This is a significant simplification:

- Hovering grasp requires stable position hold to ±2–5 cm while the gripper exerts force — extremely hard with propwash and CoM shifts.
- Landed grasp reduces to a static manipulation problem: the platform is stable, the gripper moves to the object, no active flight control required during contact.
- Power consumption drops to near-zero for the drone motors during the grasp phase.
- Grasp verification is easier (no aerodynamic noise contaminating force/weight sensors).

**Implication for the task sequence:** the TASK SEQUENCER should always check whether a landing zone exists near the target object before committing to a hover-grasp approach. Floor-level objects on open floor → land. Elevated objects (shelf, table) where no landing surface exists nearby → hover-grasp (the hard path, treated as an exception not the default). This preference should be a standing policy in the COMMAND CENTER's task-planning logic.

**Gaps and concerns.**

- *A mid-layer is missing: task decomposition into action sequences.* Even "pick up this toy, put it in this bin" requires: detect toy → check for landing zone → land or hover-approach → grasp → verify grasp → take off → fly to bin → land or hover-place → release → verify release → take off. This is not ACTIONS EXECUTION (motor commands) or COMMAND CENTER (high-level intent) — it's a **task executor / sequencer** that lives between them. Related to IMMEDIATE TASK LOAD but distinct from it.
- *Grasp verification is unsolved and critical.* The drone needs to know if the pick succeeded (did the gripper close on the object?). Force/torque sensing or weight estimation post-grasp is the typical approach, but it's not in the current design. Failed grasps with no verification lead to the drone "delivering" nothing and reporting success.
- *The manipulation-nav interaction is underspecified.* Flying with a grasped object changes the aerodynamics and CoM. The nav/attitude controller needs to know payload is loaded. This is a hardware + firmware concern that should be flagged early.
- *Onboard perception for grasp targeting is the hardest unsolved piece.* See Critical Challenges below.

---

### 5. INTERNAL HEALTH CHECK

> *Battery, WiFi, internal state. If something is wrong: take action or safely shut down.*

**What's right.** A watchdog / health monitor is standard practice in embedded autonomy stacks and the right instinct. Charging awareness is critical given [[drone-power-budget]]'s 3–15 min endurance ceiling. WiFi-loss handling is important given the split architecture.

**Gaps and concerns.**

- *The "take action to fix it" scope needs bounding.* Low battery → RTL to dock is clear. WiFi lost → continue autonomously on onboard task queue is clear. But "WiFi lost mid-task while holding a grasped object" or "battery low mid-grasp" require specific policies. The health check must interface with both AUTONOMOUS NAVIGATION (trigger safe RTL) and IMMEDIATE TASK LOAD (checkpoint task state before shutdown).
- *Hardware fault monitoring is missing.* Motor currents, ESC temps, camera failure, LiDAR driver crash, IMU sanity checks. These should all be in scope for Internal Health Check and feed into the SAFETY ARBITER.
- *The health monitor should know about capability state, not just power state.* "Is the gripper functional?" "Is the camera clean/unobstructed?" "Is the SLAM converged?" These affect whether a task is even executable.

---

### 6. ADVANCED UNDERSTANDING AND REASONING (COMMAND CENTER)

> *Off-drone brains. World state + state understanding + user commands → complex tasks. Memory of objects, difficulty, history. LLM-based.*

**What's right.** Off-loading heavy reasoning off the drone is correct — compute and latency constraints on an aerial platform are severe. An LLM-based planner that holds long-term semantic memory ("this toy was hard to pick up because it's round") and orchestrates multi-step tasks is exactly the right model for this layer. The comparison to [[semantic-object-memory]] is relevant.

**Gaps and concerns.**

- *Latency is the enemy.* An LLM round-trip over WiFi for each navigation decision is not viable. The Command Center must operate at the *task level*, not the *action level*. It emits task plans ("pick up the red ball, put it in the bin by the TV"), not moment-to-moment commands. The drone executes locally. Violating this will produce an architecture that falls apart the moment WiFi degrades.
- *What is the Command Center's state-update frequency?* If the drone finishes a grasp and reports back, does the Command Center update the world model immediately? What if a partial update arrives (drone picked up object but WiFi drops before "placed")? The consistency model needs to be designed.
- *Context window / memory management.* An LLM planner is not an infinite-memory device. You need explicit memory tooling: a semantic object store, a task history, a map snapshot, passed as structured context. [[semantic-object-memory]] covers some of this.
- *The Command Center needs a sim mode.* Before real-hardware deployment, the Command Center should be testable against a simulated drone that reports fake sensor data. Without this, integration testing is blind.

---

### 7. IMMEDIATE TASK LOAD

> *On-drone complement to Command Center. A queue of immediate actions, loaded with context from Command Center. Drone loops on this queue, executes based on current state.*

**What's right.** This is the right pattern — a pre-loaded mission context that survives WiFi dropout. Related to a behaviour tree or mission queue in standard robotics stacks. The drone shouldn't be waiting for LLM approval for each step.

**Gaps and concerns.**

- *Task queue + current state divergence needs a policy.* What if the drone reaches step 3 ("pick up the red ball") and the ball isn't where the Command Center said it would be? The task queue can't just stall — it needs an escalation path: (a) re-search the area, (b) mark item not found, skip to next, (c) abort task and call home. The design should specify this.
- *Context richness vs. freshness tradeoff.* A richer IMMEDIATE TASK LOAD (all objects, all locations) is better for robustness, but it's stale the moment the Command Center generates it. Fast-moving objects (people, pets) should never be in the task load — they must be live-detected. Slow-moving objects (toys, cups) can be in it with timestamps.

---

### 8. TASK COMMUNICATION LOOP

> *Bidirectional drone↔Command Center loop until task completion. Drone reports progress and proof; Command Center gives further instruction and final sign-off.*

**What's right.** This is the right pattern for long-horizon tasks with uncertainty. Treating task completion as a protocol (not a one-shot command) is correct; the drone isn't reliable enough to run multi-step tasks silently.

**Gaps and concerns.**

- *What constitutes "proof"?* A photo of the placed toy? A weight-sensor reading (object dropped successfully)? An RGB frame showing the bin? This is both a UX design question and a perception problem. If proof generation requires a capable vision pipeline, it may block V1 before the pipeline is ready.
- *Partial completion is the common case.* The loop should be designed assuming the task will frequently be interrupted (battery, WiFi, blocked path, object not found). State persistence across interruptions — "I placed 3 of 5 toys; on next charge cycle, retrieve the remaining 2" — is non-trivial and should be designed early.

---

## Missing components

### M1. PERCEPTION PIPELINE

The biggest gap in the current architecture. There is no subsystem that converts raw sensor data (camera images, LiDAR point clouds) into the semantic labels that WORLD MAP, AUTONOMOUS NAVIGATION, and ACTIONS EXECUTION all depend on.

The perception pipeline: **raw sensors → object detection → semantic classification → world model update**.

This has two distinct tracks:
- *Navigation perception:* what type of thing is in my path? (door, furniture, person, pet, small object) — needed by AUTONOMOUS NAVIGATION for traversability.
- *Manipulation perception:* what is this object, where is its grasp point, can I pick it up? — needed by ACTIONS EXECUTION. This is the harder track. [[onboard-grasp-perception]] is the relevant open research page.

Without explicitly naming this layer, it falls between subsystems and becomes nobody's problem.

### M2. SAFETY ARBITER

A hard real-time layer, higher priority than every other subsystem, that enforces minimum-safety guarantees regardless of what the navigation, task executor, or Command Center is requesting:

- Collision prediction: if the drone is about to hit something in the next N seconds, stop or brake regardless.
- Kill-switch pass-through: operator kill immediately overrides all autonomy.
- Geofencing: the drone cannot leave a configured safe zone, regardless of what the task queue says.
- Living-object proximity: human or pet within D meters → freeze motion, regardless of task.

This is not the same as obstacle avoidance in AUTONOMOUS NAVIGATION — that's a planner. The SAFETY ARBITER is a reactor that fires on hardware-rate sensor data and overrides everything. It must be designed as a separate, always-on, auditable module.

### M3. EXPLORATION / MAP INITIALISATION

Before the drone can navigate to "the kitchen," it needs to have mapped the kitchen. The current design assumes a world map exists but doesn't specify how it was built. An explicit **exploration mode** is needed:

- Triggered once per new home / after major layout change.
- Drone autonomously surveys all accessible rooms.
- Builds the initial geometric map (SLAM) and semantic map (room labelling, doorways, landmarks).
- User reviews and annotates ("this room is the kitchen").

This is a distinct operational mode, not a feature of navigation or world map. Frontier-based or coverage-based exploration is the standard approach ([[slam]]).

### M4. TASK SEQUENCER / EXECUTOR

Between COMMAND CENTER (high-level task: "tidy toys in living room") and IMMEDIATE TASK LOAD (action queue) there needs to an explicit **task decomposition and sequencing layer**. This:

- Breaks a high-level goal into an ordered sequence of primitive operations (navigate, approach, grasp, carry, place, verify).
- Handles precondition checking at each step ("is the object still where I expect it?").
- Manages retries and escalation.
- Lives on the drone (offline-capable) but is seeded by the Command Center.

Without this, COMMAND CENTER and IMMEDIATE TASK LOAD are doing different halves of the same job with no clean interface.

### M5. USER INTERFACE / COMMAND SURFACE

How does the user actually interact with this system? The architecture focuses on drone-side and command-center-side logic, but the user interaction surface is unspecified:

- Voice command capture (phone? smart speaker? on-device mic?).
- Visual feedback (app? web dashboard? LEDs on drone?).
- Intervention: how does the user override a task in progress?
- Trust and transparency: user should be able to see what the drone is doing and why.

[[voice-intent-task]] covers the voice-to-intent pipeline; the broader UX surface is an open design question.

---

## Revised phased roadmap

Building on the [[home-tidy-drone-prototype]] Phase-1 plan (flight + SLAM + comms, fiducials-first), here is the full-stack phasing:

| Phase | Core subsystems built | Milestone | Key dependency |
|---|---|---|---|
| **Phase 0 (current)** | SAFETY ARBITER, STATE UNDERSTANDING (fiducials/SLAM), AUTONOMOUS NAVIGATION (room-scale), INTERNAL HEALTH CHECK (basic) | Drone autonomously navigates from A→B in known room over WiFi; safe failsafe | LiDAR + SLAM + FC integration (see [[home-tidy-drone-prototype]]) |
| **Phase 1** | EXPLORATION / MAP INIT, WORLD MAP (geometric), PERCEPTION PIPELINE (nav-track: traversability labels) | Drone builds map of whole flat; correctly labels doorways, furniture, floor; re-navigates without re-mapping | SLAM + semantic nav perception |
| **Phase 2** | COMMAND CENTER (v1, LLM), TASK COMMUNICATION LOOP (v1), USER INTERFACE (voice commands) | User says "go to the kitchen" → drone navigates and confirms; Command Center holds room-level world state | Off-drone LLM + WiFi task loop + voice-to-intent |
| **Phase 3** | ACTIONS EXECUTION (gripper), TASK SEQUENCER, IMMEDIATE TASK LOAD (v1), PERCEPTION PIPELINE (manipulation-track: known objects + grasp poses) | Drone picks up a known tagged toy and places it in a tagged bin, reports completion with photo | Gripper + onboard manipulation perception [[onboard-grasp-perception]] |
| **Phase 4** | WORLD MAP (dynamic objects), INTERNAL HEALTH CHECK (full capability monitoring), COMMAND CENTER (object memory, task history) | "Tidy 3 toys" → drone autonomously completes multi-object sequence; remembers object locations across sessions | Semantic object memory [[semantic-object-memory]] + grasp verification |
| **Phase 5** | PERCEPTION PIPELINE (arbitrary objects — open-vocab), COMMAND CENTER (learning from difficulty, LLM reasoning over object properties) | Open-vocabulary tidying: handles novel household objects without prior tagging | Zero-shot grasp-pose estimation — current research frontier |

**Each phase gate must hold under WiFi dropout** — the drone should safely hold/RTL if the Command Center is unreachable at any phase. The split between on-drone (SAFETY ARBITER, STATE UNDERSTANDING, AUTONOMOUS NAVIGATION, IMMEDIATE TASK LOAD) and off-drone (COMMAND CENTER, WORLD MAP, TASK COMMUNICATION LOOP) must be enforced from Phase 0.

---

## Critical challenges — earliest focus areas

These are the hardest problems. They need early attention because each one could force an architectural pivot.

### C1. Onboard manipulation perception without motion-capture *(blocker for Phase 3+)*

Every manipulation demo in the research corpus uses external motion capture to localise objects. The drone has no equivalent — it must use onboard cameras to estimate object position and grasp pose in real time, under vibration, with a moving platform. Open-vocabulary object detection (YOLO-World, GroundingDINO) can locate objects in an RGB image; converting that to a 3D grasp pose requires either a depth camera (RealSense) + pose estimation or a learned grasp-pose network. Neither is validated in real flight at consumer scale. **This is the single hardest technical gap.** See [[onboard-grasp-perception]].

*Why it could force a pivot:* if onboard grasp perception proves too unreliable for safety (grasping a pet toy vs. a pet), the system falls back to fiducial-marked objects indefinitely — which constraints the commercial value proposition.

### C2. State reconciliation: lost vs world-changed *(blocker for reliable autonomy)*

The architecture's "challenge whether STATE aligns with WORLD STATE" loop requires the drone to distinguish "I am lost" from "the world has changed." In a living home this is common: furniture moves, doors open and close, objects appear and disappear. SLAM drift and real world-change produce identical symptoms from onboard sensors. Getting this wrong silently corrupts the world map. This likely requires probabilistic multi-hypothesis tracking and explicit change-detection logic — neither is off-the-shelf in standard SLAM stacks. [[learned-slam]] is relevant.

### C3. WiFi-dropout graceful degradation *(architectural constraint)*

The off-drone / on-drone split works only if the drone can survive an arbitrary WiFi outage at any point in task execution. Mid-task dropout while holding a grasped object, mid-grasp approach, or mid-navigation are the hard cases. Every state transition in the IMMEDIATE TASK LOAD must be safe to pause and resume, or safe to abort. This constraint should be a design invariant from Phase 0, not retrofitted later.

### C4. Payload × endurance × compute tradeoff *(physical design constraint)*

The current Phase-0 build budgets roughly 600–800 g useful payload. Add: Jetson Orin NX (~260 g), LiDAR MID360 (~265 g), battery (450–600 g), gripper (~80–150 g) — and the X500 airframe is at its limit before structural hardware. Flight time with full payload will be at the low end of the 3–15 min range ([[drone-power-budget]]). Every Phase 3+ feature adds weight or power. This is the hard physical ceiling that doesn't get solved by software. See [[payload-budget]].

### C5. Safety around people and pets *(social + regulatory constraint)*

A drone with a gripper operating autonomously in a lived-in home is a different safety category than outdoor inspection or controlled lab demos. Propeller strike at close range is severe. The SAFETY ARBITER (living-object proximity enforcement) and the choice of ducted/caged propellers ([[prop-guard-failsafe]]) must be non-negotiable from the start. The cost of a human or pet injury is architectural: one incident would rightly end the project.

### C6. Grasp verification *(operational reliability)*

If the drone can't reliably know whether a grasp succeeded (did the object actually lift?), the whole manipulation stack is unreliable. Force/torque sensing on a drone gripper is underspecified, adds weight, and may require custom hardware. Vision-based verification (check if object is in the gripper via camera) is noisy under motion. This is not a research problem but an engineering one — it needs to be solved before Phase 3 goes beyond lab conditions.

---

## Summary: how the subsystems connect

```
                  ┌──────────────────────────────────┐
                  │       COMMAND CENTER (off-drone)  │
                  │  LLM planner · world model         │
                  │  object memory · task history       │
                  └───────────┬──────────────▲─────────┘
                    task plan │              │ status/proof
                  TASK COMMUNICATION LOOP (WiFi)
                    task plan │              │ status/proof
                  ┌───────────▼──────────────┴─────────┐
                  │         IMMEDIATE TASK LOAD          │
                  │    on-drone task queue + context     │
                  └───────────┬──────────────────────────┘
                              │
                  ┌───────────▼──────────────────────────┐
                  │        TASK SEQUENCER / EXECUTOR       │
                  │  step decomposition · retry · verify   │
                  └──┬───────────┬───────────┬────────────┘
                     │           │           │
          ┌──────────▼──┐  ┌─────▼──────┐  ┌▼─────────────────┐
          │  AUTONOMOUS  │  │  ACTIONS   │  │ INTERNAL HEALTH  │
          │  NAVIGATION  │  │ EXECUTION  │  │     CHECK        │
          │  go to X     │  │ grasp/place│  │ battery/wifi/hw  │
          └──────┬───────┘  └─────┬──────┘  └────────┬─────────┘
                 │                │                   │
          ┌──────▼───────────────▼───────────────────▼─────────┐
          │                  SAFETY ARBITER                       │
          │   collision · proximity · geofence · kill-switch      │
          └──────────────────────────┬──────────────────────────┘
                                     │
          ┌──────────────────────────▼──────────────────────────┐
          │              STATE UNDERSTANDING (SLAM)               │
          │  pose estimate · confidence · consistency check       │
          └──────────────────────────┬──────────────────────────┘
                                     │
          ┌──────────────────────────▼──────────────────────────┐
          │              PERCEPTION PIPELINE                       │
          │  nav-track: traversability · manipulation-track: grasp│
          └──────────────────────────┬──────────────────────────┘
                                     │
          ┌──────────────────────────▼──────────────────────────┐
          │               WORLD MAP (synced to CC)                │
          │  geometric · semantic-static · dynamic-objects        │
          └─────────────────────────────────────────────────────┘
```

---

## Related

- [[home-tidy-drone-prototype]] — Phase-1 physical build plan; buy list; fiducials-first staging
- [[slam]] · [[fast-lio-mid360-orin]] · [[indoor-cluttered-slam]] — STATE UNDERSTANDING detail
- [[onboard-grasp-perception]] — PERCEPTION PIPELINE, manipulation track (the C1 blocker)
- [[semantic-object-memory]] — object memory for COMMAND CENTER
- [[drone-comms-wifi]] · [[slam-fc-integration]] — TASK COMMUNICATION LOOP + STATE UNDERSTANDING integration
- [[safe-indoor-flight]] · [[prop-guard-failsafe]] — SAFETY ARBITER physical prerequisites
- [[indoor-obstacle-avoidance]] — AUTONOMOUS NAVIGATION local planner options
- [[voice-intent-task]] — USER INTERFACE voice pipeline
- [[drone-power-budget]] · [[payload-budget]] — physical constraint ceiling (C4)
- [[precision-docking-recharging]] — INTERNAL HEALTH CHECK → autonomous recharge loop
