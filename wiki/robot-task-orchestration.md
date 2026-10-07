# Robot Task Orchestration: Prioritised Task Loops, Executives and Belief-Driven Action Selection

**Task orchestration** is the layer of a robot that decides *which of several concurrent goals to work on next, what physical action serves it, and how new sensor evidence changes that decision* — the part above navigation and perception that turns "map the room, find targets, profile objects, resolve conflicts, refine section X" into a sequence of stations and sensor sweeps. Robotics has organised this layer in five recurring ways: **layered architectures** with a reactive bottom and a deliberative top (3T, LAAS), **executives** that run and repair task networks (TDL, PLEXIL, T-REX), **reactive control structures** (behaviour trees, hierarchical state machines), **onboard planners/schedulers** (CASPER, MEXEC, the Mars 2020 scheduler, AEGIS), and **decision-theoretic selection** (information-gain utilities, POMDPs) — with **LLM planners** the newest layer on top. For our rover the question is concrete: the human wants a *loop of prioritised tasks*, each sensor observation fanned out to every task it informs, beliefs with certainty that are periodically *tested by prediction*, and stations chosen because one stop serves several tasks; done means *every LiDAR cluster and every visual detection is accounted for*. The literature's honest answer is that this shape already has a name — an **agenda over a shared blackboard, with utility-scored candidate actions** — and that the deliberate, deterministic version of it is what fielded autonomy (spacecraft, Mars rovers, MBARI AUVs) actually flies; POMDPs and LLMs are later layers, not the foundation (§7).

## Source

| Tag | Work | Venue / Year |
|---|---|---|
| gat98 | Gat — *On Three-Layer Architectures* (in Kortenkamp, Bonasso, Murphy eds., *AI and Mobile Robots*) | AAAI/MIT Press 1998 |
| 3t | Bonasso, Firby, Gat, Kortenkamp, Miller, Slack — *Experiences with an Architecture for Intelligent, Reactive Agents* (3T) | JETAI 9(2) 1997 |
| laas | Alami, Chatila, Fleury, Ghallab, Ingrand — *An Architecture for Autonomy* (LAAS: GenoM functional layer, executive, planner) | IJRR 17(4) 1998 |
| brooks86 | Brooks — *A Robust Layered Control System for a Mobile Robot* (subsumption) | IEEE J. Robotics & Automation 1986 |
| nilsson-tr | Nilsson — *Teleo-Reactive Programs for Agent Control* (priority-ordered condition→action rules) | JAIR 1, 1994 |
| tdl | Simmons & Apfelbaum — *A Task Description Language for Robot Control* (TDL) | IROS 1998 |
| plexil | Verma, Estlin, Jónsson, Pasareanu, Simmons, Tso — *Plan Execution Interchange Language (PLEXIL) for Executable Plans and Command Sequences* | i-SAIRAS 2005 |
| trex | McGann, Py, Rajan, Thomas, Henthorn, McEwen — *A Deliberative Architecture for AUV Control* (T-REX) | ICRA 2008 |
| trex-aamas | Py, Rajan, McGann — *A Systematic Agent Framework for Situated Autonomous Systems* | AAMAS 2010 |
| ingrand-ghallab | Ingrand & Ghallab — *Deliberation for Autonomous Robots: A Survey* | Artificial Intelligence 247, 2017 |
| remote-agent | Muscettola, Nayak, Pell, Williams — *Remote Agent: To Boldly Go Where No AI System Has Gone Before* | Artificial Intelligence 103, 1998 |
| bt-book | Colledanchise & Ögren — *Behavior Trees in Robotics and AI: An Introduction* (arXiv 1709.00084) | CRC Press 2018 |
| bt-survey | Iovino, Scukins, Styrud, Ögren, Smith — *A Survey of Behavior Trees in Robotics and AI* (arXiv 2005.05842) | RAS 2022 |
| bt-in-action | Ghzouli, Berger, Johnsen, Dragule, Wąsowski — *Behavior Trees in Action: A Study of Robotics Applications* (arXiv 2010.06256) | SLE 2020 |
| nav2 | Macenski, Martín, White, Ginés Clavero — *The Marathon 2: A Navigation System* (Nav2 BT navigator; arXiv 2003.00368) | IROS 2020 |
| btcpp | Faconti et al. — `BehaviorTree.CPP` v4 docs (ReactiveSequence/ReactiveFallback, halt semantics, blackboard ports) | software, read 2026 |
| smach | Bohren & Cousins — *The SMACH High-Level Executive* | IEEE RAM 17(4) 2010 |
| shop2 | Nau, Au, Ilghami, Kuter, Murdock, Wu, Yaman — *SHOP2: An HTN Planning System* | JAIR 20, 2003 |
| rosplan | Cashmore, Fox, Long, Magazzeni, Ridder, Carrera, Palomeras, Hurtós, Carreras — *ROSPlan: Planning in the Robot Operating System* | ICAPS 2015 |
| plansys2 | Martín, Clavijo, Fernández, Matellán, Rodríguez — *PlanSys2: A Planning System Framework for ROS2* (arXiv 2107.00376) | IROS 2021 |
| hpn | Kaelbling & Lozano-Pérez — *Integrated Task and Motion Planning in Belief Space* | IJRR 32(9-10) 2013 |
| casper | Chien, Knight, Stechert, Sherwood, Rabideau — *Using Iterative Repair to Improve the Responsiveness of Planning and Scheduling* (CASPER/ASPEN) | AIPS 2000 |
| ase | Chien et al. — *The EO-1 Autonomous Science Agent* | AAMAS 2004 |
| mexec | Troesch, Mirza, Hughes, Rothstein-Dowden, Fesq et al. — *MEXEC: An Onboard Integrated Planning and Execution Approach for Spacecraft Commanding* (ASTERIA CubeSat) | ICAPS IntEx/GR workshop 2020 |
| m2020-obp | Gaines, Chien, Rabideau et al. — *Onboard Planning for the Mars 2020 Perseverance Rover* (priority-first, non-backtracking scheduler) | ASTRA 2022 |
| m2020-ground | Yelamanchili, Rabideau, Agrawal, Wong, Gaines, Chien — *Ground and Onboard Automated Scheduling for the Mars 2020 Rover Mission* | IWPSS 2021 |
| cadre | *Planning, Scheduling, and Execution on the Moon: the CADRE Technology Demonstration Mission* (arXiv 2502.14803) | 2025 |
| oasis | Castaño, Estlin, Anderson, Gaines, Castaño, Bornstein, Chouinard, Judd — *OASIS: Onboard Autonomous Science Investigation System for Opportunistic Rover Science* | JFR 24(5) 2007 |
| aegis-mer | Estlin, Bornstein, Gaines, Anderson, Thompson, Burl, Castaño, Judd — *AEGIS Automated Science Targeting for the MER Opportunity Rover* | ACM TIST 3(3) 2012 |
| aegis-msl | Francis, Estlin, Doran, Johnstone, Gaines, Verma et al. — *AEGIS Autonomous Targeting for ChemCam on Mars Science Laboratory: Deployment and Results of Initial Science Team Use* | Science Robotics 2(7) 2017 |
| placed-survey | Placed et al. — *A Survey on Active SLAM* (arXiv 2207.00254) | IEEE T-RO 2023 |
| bircher-nbv | Bircher, Kamel, Alexis, Oleynikova, Siegwart — *Receding Horizon "Next-Best-View" Planner for 3D Exploration* | ICRA 2016 |
| delmerico-ig | Delmerico, Isler, Sabzevari, Scaramuzza — *A Comparison of Volumetric Information Gain Metrics for Active 3D Object Reconstruction* | Autonomous Robots 42, 2018 |
| bajcsy-revisit | Bajcsy, Aloimonos, Tsotsos — *Revisiting Active Perception* (arXiv 1603.02729) | Autonomous Robots 42, 2018 |
| semexp | Chaplot, Gandhi, Gupta, Salakhutdinov — *Object Goal Navigation using Goal-Oriented Semantic Exploration* (arXiv 2007.00643) | NeurIPS 2020 |
| aydemir | Aydemir, Pronobis, Göbelbecker, Jensfelt — *Active Visual Object Search in Unknown Environments Using Uncertain Semantics* | IEEE T-RO 29(4) 2013 |
| oo-pomdp | Wandzel, Oh, Fishman, Kumar, Wong, Tellex — *Multi-Object Search using Object-Oriented POMDPs* | ICRA 2019 |
| genmos | Zheng, Paul, Tellex et al. — *A System for Generalized 3D Multi-Object Search* (GenMOS; arXiv 2303.03178) | ICRA 2023 |
| pomdp-ir | Spaan, Veiga, Lima — *Decision-Theoretic Planning under Uncertainty with Information Rewards for Active Cooperative Perception* | JAAMAS 29, 2015 |
| rho-pomdp | Araya-López, Buffet, Thomas, Charpillet — *A POMDP Extension with Belief-dependent Rewards* (ρPOMDP) | NeurIPS 2010 |
| kaelbling98 | Kaelbling, Littman, Cassandra — *Planning and Acting in Partially Observable Stochastic Domains* | Artificial Intelligence 101, 1998 |
| pomcp | Silver & Veness — *Monte-Carlo Planning in Large POMDPs* (POMCP) | NeurIPS 2010 |
| despot | Somani, Ye, Hsu, Lee — *DESPOT: Online POMDP Planning with Regularization* | NeurIPS 2013 |
| pomdp-survey | Lauri, Hsu, Pajarinen — *Partially Observable Markov Decision Processes in Robotics: A Survey* (arXiv 2209.10342) | IEEE T-RO 2023 |
| hearsay | Erman, Hayes-Roth, Lesser, Reddy — *The Hearsay-II Speech-Understanding System: Integrating Knowledge to Resolve Uncertainty* (blackboard) | ACM Computing Surveys 12(2) 1980 |
| bb-control | Hayes-Roth — *A Blackboard Architecture for Control* (agenda of knowledge-source activation records, scheduler rates them) | Artificial Intelligence 26, 1985 |
| am-lenat | Lenat — *AM: An Artificial Intelligence Approach to Discovery in Mathematics as Heuristic Search* (agenda of tasks ranked by "worth", reasons accumulate priority) | Stanford PhD 1976 |
| utility-ai | Mark — *Behavioral Mathematics for Game AI*; Dill & Mark — *Improving AI Decision Modeling Through Utility Theory* | Course Tech 2009 / GDC 2010 |
| goap | Orkin — *Three States and a Plan: The A.I. of F.E.A.R.* (goal-oriented action planning) | GDC 2006 |
| doyle-tms | Doyle — *A Truth Maintenance System* | Artificial Intelligence 12, 1979 |
| atms | de Kleer — *An Assumption-Based TMS* | Artificial Intelligence 28, 1986 |
| probrob | Thrun, Burgard, Fox — *Probabilistic Robotics* (beam model, occupancy log-odds, innovation gating) | MIT Press 2005 |
| wong-da | Wong, Kaelbling, Lozano-Pérez — *Data Association for Semantic World Modeling from Partial Views* | IJRR 34(7) 2015 |
| pmtsdf | Schmid, Delmerico, Schönberger, Nieto, Pollefeys, Siegwart, Cadena — *Panoptic Multi-TSDFs* (arXiv 2109.10165) | ICRA 2022 |
| khronos | Schmid, Abate, Chang, Carlone — *Khronos: A Unified Approach for Spatio-Temporal Metric-Semantic SLAM in Dynamic Environments* (arXiv 2402.13817) | RSS 2024 |
| pocd | Qian, Chatrath, Yang, Servos, Schoellig, Waslander — *POCD: Probabilistic Object-Level Change Detection and Volumetric Mapping in Semi-Static Scenes* (arXiv 2205.01202) | RSS 2022 |
| dovsg | Yan et al. — *Dynamic Open-Vocabulary 3D Scene Graphs for Long-term Language-Guided Mobile Manipulation* (DovSG; arXiv 2410.11989) | RA-L 2025 |
| hydra | Hughes, Chang, Carlone — *Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization* (arXiv 2201.13360) | RSS 2022 |
| fremen | Krajník, Fentanes, Santos, Duckett — *FreMEn: Frequency Map Enhancement for Long-Term Mobile Robot Autonomy in Changing Environments* | IEEE T-RO 33(4) 2017 |
| saycan | Ahn et al. — *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances* (SayCan; arXiv 2204.01691) | CoRL 2022 |
| inner-mono | Huang et al. — *Inner Monologue: Embodied Reasoning through Planning with Language Models* (arXiv 2207.05608) | CoRL 2022 |
| cap | Liang et al. — *Code as Policies* (arXiv 2209.07753) | ICRA 2023 |
| progprompt | Singh et al. — *ProgPrompt: Generating Situated Robot Task Plans using LLMs* (arXiv 2209.11302) | ICRA 2023 |
| sayplan | Rana, Haviland, Garg, Abou-Chakra, Reid, Suenderhauf — *SayPlan: Grounding LLMs using 3D Scene Graphs for Scalable Robot Task Planning* (arXiv 2307.06135) | CoRL 2023 |
| conceptgraphs | Gu et al. — *ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning* (arXiv 2309.16650) | ICRA 2024 |
| hovsg | Werby, Huang, Büchner, Valada, Burgard — *Hierarchical Open-Vocabulary 3D Scene Graphs for Language-Grounded Robot Navigation* (HOV-SG; arXiv 2403.17846) | RSS 2024 |
| knowno | Ren et al. — *Robots That Ask For Help: Uncertainty Alignment for LLM Planners* (KnowNo; arXiv 2307.01928) | CoRL 2023 |
| llm-p | Liu et al. — *LLM+P: Empowering LLMs with Optimal Planning Proficiency* (arXiv 2304.11477) | 2023 |
| planbench | Valmeekam, Marquez, Olmo, Sreedharan, Kambhampati — *PlanBench* (arXiv 2206.10498) | NeurIPS 2023 D&B |
| llm-modulo | Kambhampati et al. — *LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks* (arXiv 2402.01817) | ICML 2024 |

> Verification note: arXiv ids and venues for pmtsdf, khronos, pocd, dovsg, mexec, m2020-obp and aegis-msl were re-checked by web search on 2026-10-07. The remaining entries are standard, widely-cited references given from the literature; page numbers and minor author lists were not re-verified.

## Related

- [[active-slam-exploration]] — the utility-function taxonomy (identification → utility → selection) that this page generalises from "where to map next" to "which task's action next".
- [[measurement-selection-uncertainty]] — the "which measurement reduces the uncertainty I care about" question; here it becomes the per-task value term in the agenda score.
- [[scene-graph-world-model]] — the natural *blackboard* for the agenda: rooms, walls, clusters, objects and their certainty live there (§5).
- [[robust-evidence-mapping-principle]] — "reliability = agreement"; the belief-certainty and prediction-test machinery in §5 is the operational form of it.
- [[map-then-navigate]] — the current two-phase architecture; the agenda replaces the hard phase boundary with tasks whose priorities shift as the map matures.
- [[ros2-nav2]] — the BT navigator (§2) is the obvious executor for the aux "go to / plan a path" tasks.
- [[locate-object-from-last-known-position]] · [[object-fingerprint-memory]] · [[dynamic-object-handling]] — consumers of the object-belief side.
- [[language-3d-scene-representations]] — ConceptGraphs/HOV-SG-style maps that an LLM layer would query (§6).

---

## 1. Classic robot architectures: who decides, at what rate

### 1.1 The three-layer consensus

By the late 1990s most fielded mobile-robot architectures had converged on **three layers** [src: gat98]:

| Layer | 3T name | LAAS name | Time scale | What it holds |
|---|---|---|---|---|
| **Controller** (reactive) | skills | functional layer (GenoM modules) | ms | servo loops, obstacle guard, sensor drivers; little or no state |
| **Sequencer / executive** | sequencer (RAPs) | executive / supervisor | s | which skill is active, monitors, failure recovery, task decomposition at run time |
| **Deliberator** | planner | decisional layer (planner + supervisor) | s–min | goals, long-horizon plans, resource reasoning |

Gat's central argument is about **state**: the bottom layer should hold almost none, the middle layer holds *memories of the past* (what has been tried, what's running), the top layer holds *predictions of the future* [src: gat98]. 3T used Firby's RAPs as the sequencer — a library of *reactive action packages*, each a set of alternative methods with success conditions, chosen at run time from the current world state [src: 3t]. LAAS added formal machinery: GenoM generates functional modules with declared requests and posters, and a verified execution-control layer between modules and the decisional layer refuses requests that would violate safety constraints [src: laas].

Two older lines feed into this. **Subsumption** [src: brooks86] layers behaviours with fixed suppression priority (higher layers override lower) — priority is *structural*, not computed. **Teleo-reactive programs** [src: nilsson-tr] are an ordered list of `condition → action` rules re-evaluated continuously; the first true condition fires. Their design rule — each rule's action should make a rule *higher in the list* true — is exactly the regression-from-goal structure behaviour trees later formalised (§2), and the *continuous re-evaluation* is how they get preemption for free.

*(synthesis)* Our rover already has this split informally: the firmware guard and motor loops are the controller layer; `drone.patrol` / `discover_object` / `discover_all` are sequencer-level scripts; and the human currently *is* the deliberator. The proposed task loop is the deliberator plus a cleaner executive — it should not reach into the controller layer.

### 1.2 Executives: TDL, PLEXIL, T-REX, Remote Agent

The executive is where interleaving actually happens. Four lineages matter:

- **TDL** (CMU) extends C++ with *task trees*: tasks spawn subtasks, with synchronisation constraints ("start after X completes", "terminate when Y"), monitors that fire on conditions, and exception handlers that propagate up the tree [src: tdl]. It is the ancestor of "an executive is a tree of running tasks with constraints between them".
- **PLEXIL** (NASA ARC/JPL) is a deliberately small, verifiable language of hierarchical *nodes*, each with start/end/repeat/skip/pre/post/invariant conditions; it was built as an *interchange* format so that a planner or a human can emit plans that a lightweight executive runs deterministically [src: plexil]. Its point is predictability: every node's lifecycle is a fixed state machine, so behaviour can be model-checked.
- **Remote Agent** (Deep Space 1, 1999) combined a constraint-based planner/scheduler, a smart executive and model-based fault diagnosis (Livingstone) on a real spacecraft — the first closed-loop onboard deliberation in flight [src: remote-agent].
- **T-REX** (MBARI, for Dorado AUVs) is the most relevant for our "many interleaved tasks" shape. The agent is a set of **teleo-reactors**, each owning a set of *timelines* (state variables over time) and running its own sense-plan-act loop at its own horizon and latency; reactors exchange *observations* and *goals* through shared timelines, and a single *tick* synchronises everyone [src: trex, trex-aamas]. A mission reactor deliberates over hours, a navigation reactor over minutes, an executive reactor over seconds. Crucially, **observations propagate to every reactor whose timelines they touch** — the "distribute each sensor observation to every task it informs" requirement is a first-class design feature of T-REX, and the AUV used it to adaptively re-plan sampling when an onboard detector flagged a feature of interest (e.g. a plume) [src: trex].

The survey of deliberation functions [src: ingrand-ghallab] frames all of these as instances of six functions — **planning, acting, observing (situation assessment), monitoring, goal reasoning, learning** — and argues that the hard engineering is in the *integration*, especially *goal reasoning* (deciding which goals to pursue as the world changes) and *monitoring* (detecting that an expectation was violated). Our "resolve conflicting beliefs" and "determine target validity" tasks are monitoring/goal-reasoning functions in that vocabulary.

*(synthesis)* T-REX's decomposition maps unusually cleanly onto the proposed design: each task (floor plan, targets, object Y, conflicts) is a reactor owning its slice of the belief state; observations are posted once and consumed by every reactor whose timeline they update; a mission-level reactor arbitrates which reactor's goal gets the robot body next. We don't need T-REX's temporal-constraint planner (our tasks have no hard deadlines), but we should copy the **observation fan-out + per-task belief ownership + single arbiter** structure.

---

## 2. Behaviour trees vs hierarchical state machines

### 2.1 Behaviour trees

A **behaviour tree (BT)** is a rooted tree ticked at a fixed rate; leaves are actions/conditions returning SUCCESS / FAILURE / RUNNING; internal **Sequence** nodes (→) succeed when all children succeed, **Fallback/Selector** nodes (?) succeed when any child succeeds, plus **Parallel** and decorators [src: bt-book]. Colledanchise & Ögren show BTs generalise subsumption, teleo-reactive programs and decision trees, and argue the key property is **modularity**: a subtree has one entry and two-ish outcomes, so it can be moved or reused without rewiring transitions — the thing that makes large FSMs unmaintainable [src: bt-book]. The survey [src: bt-survey] and the empirical study of open-source robotics BTs [src: bt-in-action] find BTs now dominate ROS-based mobile robotics task layers, often mixed with FSMs at the top.

**Priority and preemption.** In a BT, priority is **positional**: in a Fallback, the leftmost child is tried first. With *reactive* control nodes — BehaviorTree.CPP's `ReactiveSequence` / `ReactiveFallback` — conditions to the left are **re-ticked every cycle**, and if a higher-priority branch becomes runnable the currently RUNNING lower branch is **halted** [src: btcpp, bt-book]. That is how a BT expresses "obstacle guard beats everything; battery-low beats exploration". The Nav2 navigator is a BT: `NavigateToPose` runs a `PipelineSequence` of replan-at-rate → follow-path inside a `RecoveryNode` whose fallback branch cycles clear-costmap / spin / wait / back-up recoveries [src: nav2]. The **blackboard** (typed key-value ports) is how nodes share data such as the goal and path [src: btcpp].

**What BTs do badly** for our problem: (i) priority is *static* — the tree layout encodes a fixed order, and expressing "object Y now outranks map section X because its certainty is low and we happen to be next to it" requires either rewriting the tree or putting a computed choice inside a node; (ii) BTs have no native notion of *multiple goals served by one action*; (iii) the many-condition re-tick model gets expensive and hard to read once the number of candidate tasks is data-dependent (one task per unexplained cluster). The standard game-industry fix is a **utility selector** node: a composite that scores its children each tick and runs the highest-scoring one [src: utility-ai] — i.e. a scored agenda embedded as one node of a BT.

### 2.2 Hierarchical state machines (SMACH)

**SMACH** (Willow Garage, PR2) builds hierarchical state machines in Python: states return outcomes, containers (StateMachine, Concurrence, Iterator) nest, userdata flows between states; it was the PR2's "plug into the outlet" and "fetch a drink" executive [src: smach]. Preemption is explicit — a state must poll `preempt_requested()` and a `Concurrence` container can terminate siblings when one child finishes. HSMs make *mode* explicit (MAPPING / DISCOVERING / DOCKED), which is good for the human-readable "what is it doing" question, but every new task or interrupt adds transitions, and dynamic task sets (N clusters) fit badly.

*(synthesis)* For orchestration of *data-dependent* task sets, both BTs and HSMs are better as the **executor of a chosen action** (go to station, run sweep, recover) than as the **chooser**. The field's own practice agrees: Nav2 uses a BT to *execute* navigation and expects an external node to choose goals ([[active-slam-exploration]] §2 notes no exploration ships in Nav2).

---

## 3. Task-level planners and onboard planning/scheduling

### 3.1 HTN and PDDL in ROS

**HTN planning** (SHOP2) decomposes abstract tasks into subtasks via author-written *methods* until primitive actions remain, which makes domain expertise ("to profile an object: approach, sweep the lift, view from ≥2 bearings, fit") directly encodable [src: shop2]. **ROSPlan** wraps PDDL planners in ROS: a knowledge base of facts, a problem generator, a planner, and a dispatcher that executes actions and *re-plans when an action fails or the knowledge base changes* [src: rosplan]; PlanSys2 is the ROS 2 successor, dispatching through BTs [src: plansys2]. Kaelbling & Lozano-Pérez's **HPN in belief space** is the one to know for us: it plans hierarchically over *belief fluents* such as "the robot *knows* object O is at pose P to within ε with probability ≥ δ", and inserts **look actions** whose purpose is to make such a fluent true, re-planning in the now as the belief updates [src: hpn]. That is precisely "observe to raise certainty until a threshold, then act".

The pain is well-known: classical planners assume a closed world and deterministic effects, so in perception-heavy tasks most of the effort goes into keeping the symbolic state in sync with the probabilistic one and into re-planning loops [src: ingrand-ghallab].

### 3.2 Spacecraft and rover onboard planning

The most mature fielded instance of "a prioritised set of activities, re-planned onboard as evidence arrives" is JPL's lineage:

- **ASPEN / CASPER**: ASPEN is a ground constraint-based scheduler; CASPER is its onboard, *continuous* version, using **iterative repair** — rather than re-planning from scratch, it keeps a current plan and, when a new goal, a state update or a conflict arrives, applies local repair moves (move, delete, add activity) that reduce conflicts, so it can respond in seconds [src: casper]. On EO-1 the **Autonomous Science Agent** flew it for years: onboard classifiers detected events (flood, volcano, ice breakup) in images, posted *new observation goals*, and CASPER re-planned the next orbits to observe them — goal generation from detection, closed onboard [src: ase].
- **MEXEC** (ASTERIA CubeSat; prototyped for Europa Clipper fail-operational requirements) integrates task-network planning and execution in one flight-software component: it plans from *goals and intent* rather than time-tagged sequences and re-plans when execution diverges [src: mexec]. The CADRE lunar rovers (2024–25) carry a related planning/scheduling/execution stack for multi-rover coordination [src: cadre].
- **Mars 2020 onboard scheduler**: Perseverance flies a **priority-first, non-backtracking** scheduler: ground sends a set of activities with priorities, constraints and resource models; onboard, activities are placed greedily in priority order, and the schedule is regenerated during the sol when actual energy or durations differ from prediction [src: m2020-obp, m2020-ground]. The design choice is telling — **deterministic, priority-ordered, explainable, bounded compute** — chosen over optimal search because operators must be able to predict and audit what the rover will do.

### 3.3 AEGIS: noticing targets in transit and spawning observations

**OASIS** (Castaño et al.) prototyped the pattern on JPL rovers: during traverse, analyse navcam images for rocks, rank them by science interest (albedo, shape, novelty) against goals the scientists set, and *insert new observation activities* into the plan if resources allow — with the onboard planner (CASPER) deciding whether there is energy/time to pay for the detour [src: oasis]. **AEGIS** is the flight descendant: on Opportunity (MER, 2010) it picked targets for the Pancam from navcam images after a drive [src: aegis-mer]; on Curiosity (MSL, since May 2016) it selects ChemCam LIBS targets from navcam images autonomously, choosing the targets that best match parameters scientists specify (size, brightness, shape), and measures them *without Earth in the loop*. Over 2.5 km of new terrain it picked the scientists' preferred target class >93 % of the time versus ~24 % expected from blind targeting [src: aegis-msl]. A second mode refines pointing of human-chosen targets by a few milliradians [src: aegis-msl]. AEGIS was also carried to Perseverance's SuperCam.

The pattern to take is the **division of labour**: a cheap detector runs on data the robot collects *anyway* (post-drive navcam), generates *candidate* observations scored against an explicit, human-authored preference function, and the scheduler admits them only if they fit the resource budget. Detection never commandeers the robot; it *proposes*, the scheduler *disposes*.

*(synthesis)* "Find targets (unexplained LiDAR clusters + camera)" is our AEGIS: every station's sweep is post-drive navcam; any unexplained cluster becomes a *proposed* task (profile / validate) with a score, and the arbiter decides whether it is worth a detour now or later. "Determine target validity" is the analogue of AEGIS's science-filter: a cheap test before an expensive observation.

---

## 4. Utility and information-gain action selection: one action, several goals

### 4.1 Next-best-view and information gain

Active SLAM and active reconstruction pick the next view by maximising **expected information gain minus cost** over a candidate set (frontier centroids, sampled viewpoints) [src: placed-survey, bircher-nbv]. Delmerico et al. compare volumetric IG formulations for object reconstruction — counting unknown voxels, entropy, occlusion-aware visibility, rear-side/proximity terms — and find the choice of formula matters less than counting **occlusion and visibility correctly** [src: delmerico-ig]. Bajcsy's *active perception* framing — choose sensor configurations *because of what you want to know* — is the umbrella [src: bajcsy-revisit].

### 4.2 Object search and semantic exploration

Object search adds *semantic priors*: Aydemir et al. plan search over a probabilistic map of where object classes are likely given room/place categories [src: aydemir]; SemExp learns a policy that picks long-term exploration goals on a semantic map [src: semexp]. Tellex's group formulates **multi-object search as an object-oriented POMDP**, where the belief factorises per object and one observation updates every object's belief — directly the "one observation serves many tasks" structure, with the planner (POMCP-style) choosing views that maximise *joint* expected reward across objects [src: oo-pomdp, genmos].

### 4.3 How "one action serves many goals" is actually scored

Three formulations recur:

1. **Sum of per-goal information rewards.** POMDP-IR adds explicit "commit" actions whose reward depends on the belief (reward for correctly asserting a hypothesis), and ρPOMDP generalises reward to any belief function (e.g. negative entropy) [src: pomdp-ir, rho-pomdp]. With factored beliefs, the expected reward of a view is the **sum over every belief it informs** — a station near three uncertain items naturally wins.
2. **Weighted multi-objective utility.** Most practical systems write `U(a) = Σ_k w_k · ΔI_k(a) − λ · cost(a)` with hand-set weights (exploration vs exploitation, coverage vs localisation quality) [src: placed-survey]. Weights are the knob; they are also the main source of tuning pain.
3. **Utility AI (game industry).** Each candidate action carries *considerations* (normalised 0–1 response curves over inputs such as distance, uncertainty, staleness), multiplied (with a compensation factor) into a score; the highest-scoring action runs, rescored every cycle [src: utility-ai]. GOAP adds a lightweight planner to chain actions toward the chosen goal [src: goap]. These are explicitly built for *debuggability* — designers inspect per-consideration scores.

### 4.4 Blackboards and agendas

The **blackboard architecture** (Hearsay-II) is the classical answer to "many specialists, one shared evolving hypothesis space, opportunistic control": knowledge sources watch a shared blackboard of hypotheses at several abstraction levels; when a change matches a knowledge source's trigger, a **knowledge-source activation record (KSAR)** is posted to an **agenda**; a scheduler rates KSARs and runs the best [src: hearsay]. Hayes-Roth's BB1 made control itself a blackboard problem — the scheduler's rating policy is explicit, inspectable data [src: bb-control]. Lenat's AM ran an **agenda of tasks with numeric worth**, where each task carries a list of *reasons*, and a task proposed again for a new reason has its priority *raised* [src: am-lenat] — the earliest form of "a task that serves several goals floats to the top".

*(synthesis)* The human's design is a near-verbatim blackboard + agenda: tasks = knowledge sources; beliefs-with-certainty = blackboard hypotheses; "distribute each observation to every task it informs" = blackboard change triggers; "few stations, each serving several tasks" = AM-style priority accumulation across reasons, or the factored information-reward sum. The literature's only addition is to score **candidate actions (stations)**, not tasks: generate candidate stations, ask every task "what would you gain from a sweep here?", sum, subtract travel/risk cost, pick the max.

---

## 5. Belief maintenance: certainty, prediction tests, conflicts, change

### 5.1 Probabilistic beliefs and prediction tests

The standard tools are in *Probabilistic Robotics*: occupancy log-odds accumulate evidence additively; a **beam/ray model** predicts the range a sensor should read given the map; and the **innovation** (measured − predicted) is gated by its covariance (a χ²/Mahalanobis test) to accept, reject or flag a measurement [src: probrob]. "If the wall is there I should read x" is exactly a predicted-measurement innovation test, and its batch form — normalised innovation squared over many rays — is how a filter detects that its *model* (not just a reading) is wrong. Wong, Kaelbling & Lozano-Pérez treat object-level world modelling as **data association over partial views**, maintaining a distribution over how many objects exist and which detection belongs to which, rather than committing early [src: wong-da] — the right formal frame for "is this cluster object A, object B, or new?".

### 5.2 Truth maintenance

Symbolic AI's answer to conflicting beliefs is the **truth maintenance system**: each belief records its *justifications* (which observations/inferences support it), so when a supporting observation is retracted or contradicted, dependent beliefs are retracted automatically (Doyle's JTMS) [src: doyle-tms]; the **ATMS** keeps *all* consistent assumption sets alive simultaneously, labelling each belief with the minimal assumption sets under which it holds — multiple hypotheses without committing [src: atms]. Modern robotics rarely uses TMSs by name, but the provenance idea is pervasive: factor-graph SLAM is effectively a probabilistic justification network (a factor *is* a justification), and outlier-robust back-ends "retract" factors that conflict with the consensus.

### 5.3 Object permanence and change in long-term maps

- **Panoptic Multi-TSDFs** represent the map as a set of per-object *submaps*, each with its own TSDF and lifecycle; on revisit, submaps are checked for consistency against new observations and marked *persistent*, *absent* or *changed*, and only inconsistent submaps are re-integrated [src: pmtsdf].
- **POCD** keeps a per-object probabilistic state — a **stationarity score** and a TSDF change measure — updated with a Bayesian rule using geometric and semantic evidence, so an object's "it moved" belief rises or falls with evidence rather than flipping on one frame [src: pocd].
- **Khronos** factorises spatio-temporal mapping into a fast process tracking short-term dynamics in an active window and a slow factor-graph process that reasons about long-term change on revisits, producing a 4-D map whose objects have appearance/disappearance times [src: khronos]. Hydra builds the layered scene graph it sits on [src: hydra].
- **DovSG** maintains an open-vocabulary scene graph and **locally updates** only the affected subgraph when the robot observes a change, reporting ~30 % higher long-term task success than static-map baselines [src: dovsg].
- **FreMEn** models periodic state changes (doors, occupancy) as frequency spectra, giving *predictions* of state that the robot can test and use to schedule observations when uncertainty is highest [src: fremen].

**How conflicts are detected and resolved across these systems:** (i) *prediction vs observation* at the geometric level (ray-casting a submap and comparing with the depth/scan); (ii) *evidence accumulation* with hysteresis (stationarity scores, log-odds) so a single noisy disagreement does not flip a belief; (iii) *object-level, not cell-level* bookkeeping so a conflict names *what* is wrong; (iv) resolution by **re-observation** when the posterior is ambiguous — i.e. the conflict spawns an observation task.

*(synthesis)* That last point closes the loop with §4: an unresolved conflict is just a belief with high entropy, so "resolve conflicting beliefs" does not need its own planner — it is a high-value term in the station score. The "periodically test beliefs against predictions" requirement is the cheap version of (i), run on every sweep as a free by-product: each scan is ray-cast against the current map and object hypotheses, and agreement/disagreement updates each belief's certainty. This is also the project's [[robust-evidence-mapping-principle]] made operational.

---

## 6. LLM / VLM task planners for home robots

- **SayCan** scores each skill by *LLM usefulness × learned value-function feasibility*, so the language model proposes and the affordance model vetoes [src: saycan].
- **Inner Monologue** feeds success detection, scene descriptions and human answers back into the LLM prompt as text, letting it re-plan after failures [src: inner-mono].
- **Code as Policies** / **ProgPrompt** have the LLM write programs over a robot API, which is more compositional and inspectable than free text [src: cap, progprompt].
- **SayPlan**, **ConceptGraphs**, **HOV-SG** ground the LLM in a **3D scene graph** it can query/expand (SayPlan uses semantic search over a collapsed graph plus an iterative replanning loop with a scene-graph simulator to verify plans) [src: sayplan, conceptgraphs, hovsg].
- **KnowNo** uses conformal prediction over LLM options so the robot *asks for help* when the option set is ambiguous [src: knowno].
- **LLM+P** and **LLM-Modulo** argue the LLM should translate to a formal problem or propose candidates that *external verifiers* check; PlanBench shows unaided LLMs perform poorly on classical planning instances, especially when names are obfuscated [src: llm-p, llm-modulo, planbench].

**Where they help:** open-vocabulary judgement calls — "is this cluster plausibly a chair leg or a cable?", "which detections probably belong to one object?", naming objects, ranking semantic plausibility, explaining the plan to a human. **Where they fail:** long-horizon consistency, numeric trade-offs (distance vs information), keeping track of many beliefs and their certainties, and reproducibility (sampling, model updates) [src: planbench, llm-modulo]. **Cost/latency:** each decision is a network call of the order of seconds and a non-trivial cost per call; fine for a slow rover making ~tens of station decisions per session, but a poor fit for anything inside the tick loop. Every successful system above keeps the LLM **out of the control loop** and **behind a verifier** (affordance values, a planner, a scene-graph simulator, conformal sets).

*(synthesis)* The project memory already settles this pattern ("classical bedrock + LLM pivots at ambiguity seams"); the literature agrees. The LLM belongs at the *validity* and *identity* seams (determine target validity; resolve conflict when the geometry is ambiguous), returning a structured verdict into the blackboard — not choosing stations.

---

## 7. Recommendation for our single-room prototype

### 7.1 The four options

| | (a) Deterministic scored agenda + blackboard | (b) Behaviour tree with utility nodes | (c) Belief-space / POMDP planning | (d) LLM-driven prioritisation |
|---|---|---|---|---|
| **Effort to first run** | Low: a belief store, task classes with `value_at(station)`, a scoring loop | Low–medium: BT.CPP/py_trees + a utility selector node; still needs (a)'s scores inside | High: factored belief model, observation models per task, POMCP/DESPOT tuning; models will be wrong at first | Low to prototype, high to make reliable (prompting, state serialisation, verifiers) |
| **Debuggability** | Best: every decision is a table of per-task contributions; replayable from logs | Good for *execution* (tree visualisers); the choice is still opaque unless the utility node logs its scores | Poor: sampled tree search, decisions hard to explain; non-deterministic unless seeded | Poor: non-reproducible, explanations are post-hoc text |
| **"One observation serves many tasks"** | Native: observation posted once to the blackboard, every task updates its belief; station score = Σ task gains | Only via the utility node — the BT structure itself has no notion of it | Native and principled (factored belief, summed information reward) — its real strength | Only if the prompt contains all beliefs; no guarantee it is accounted for consistently |
| **Priority / preemption** | Re-score after every sweep; safety and aux tasks as hard gates outside the score | Excellent: reactive fallback gives hard-priority preemption (guard, battery, lift fault) | Implicit in the reward; safety still needs a separate layer | Unreliable for safety; must be gated |
| **Fits our cadence (slow, station-based, not real-time)** | Yes | Yes | Yes (compute is affordable at station rate) | Yes (latency acceptable) |
| **Fielded precedent** | AEGIS + M2020 scheduler (priority-first), blackboards, utility AI | Nav2, most ROS 2 robots | Mostly research (object search, manipulation) | Research demos |

### 7.2 Recommendation

**Build (a), executed by a thin (b), with (c)'s scoring idea and (d) at the seams later.**

1. **Blackboard (the belief store).** One object-centric store — walls/sections, LiDAR clusters, camera detections, objects, conflicts — each item with `certainty`, `provenance` (which observations support/contradict it, TMS-style [src: doyle-tms]), `last_tested`, and a `status` (unexplained / hypothesised / confirmed / rejected). It is the [[scene-graph-world-model]].
2. **Observation fan-out.** Every sweep is posted once; each task's `ingest(obs)` updates the items it owns. The *prediction test* runs here by default: ray-cast the current map and object hypotheses into the new scan, update certainty by agreement (§5.1) [src: probrob, pocd]. Disagreements beyond a gate create or strengthen a **conflict** item.
3. **Tasks as knowledge sources.** Floor plan (discover/refine section X), targets (AEGIS-style proposal from unexplained clusters/detections [src: aegis-msl]), object profile Y, target validity, conflict resolution. Each exposes `value_at(station) ∈ [0,1]`: the expected certainty gain on its items from a sweep at that station (use a cheap visibility/ray count, not a full IG integral — [src: delmerico-ig] says visibility handling matters most).
4. **Arbiter (the agenda).** Generate candidate stations (frontier-like + around high-entropy items + current pose), score `U(s) = Σ_tasks w_t · value_t(s) − λ·travel(s) − μ·risk(s)`, pick the max, log the full per-task breakdown. This is Lenat/Hayes-Roth priority accumulation and the factored information-reward sum in deterministic form [src: am-lenat, bb-control, pomdp-ir]. Priority-first, non-backtracking, re-scored after each sweep — the M2020 design choice for the same reason: predictable and auditable [src: m2020-obp].
5. **Executor.** Aux tasks (locate self, plan path, go to) are *not* agenda items competing on score; they are the means the arbiter uses, plus hard gates (guard, lift fault, self-localisation below threshold → "locate self" preempts). That is naturally a small BT or the existing scripts; Nav2's BT is the model if we move onto ROS 2 [src: nav2, btcpp].
6. **Termination.** Done when no item is `unexplained` and every item's certainty is above its threshold *or* it is marked unreachable/parked — i.e. "every cluster and detection accounted for" is a query on the blackboard, not a separate heuristic.

### 7.3 Staged path

| Stage | Add | Trigger to move on |
|---|---|---|
| **S0** | Blackboard + fan-out + prediction tests, *no* autonomy: human picks stations, the system prints the score table it *would* have used | Score table agrees with human choices most of the time; disagreements are explainable |
| **S1** | Arbiter picks stations; deterministic, logged; weights hand-set | A full room run ends with everything accounted for or parked |
| **S2** | LLM/VLM at the seams only — target validity, identity/association, conflict adjudication when geometry is ambiguous — returning structured verdicts with a confidence that enters the belief like any other observation [src: knowno, llm-modulo] | Seam verdicts beat the classical rule on a held-out set |
| **S3** | Two-step lookahead or POMCP over the *same* factored belief and reward, only if S1 visibly wastes stations (greedy myopia is the known failure of one-step utility [src: placed-survey, pomdp-survey]) | Measured station savings vs S1 on replayed logs |
| **S4** | Learn weights / value functions from logged runs (SayCan-style affordance learning, [src: saycan]) | Enough runs logged |

*(synthesis)* The reasons to start deterministic are specific to us: the project's standing rules require *verified, explainable* decisions and honest validation; the per-task score table is exactly the evidence a reviewer needs; the cadence (a few dozen stations per room) makes greedy-with-replanning nearly as good as lookahead; and every later layer — POMDP lookahead, LLM seams, learned weights — reuses the same blackboard and the same per-task `value_at`, so nothing in S0–S1 is thrown away. The one thing to design in from day one is the **factored, per-item belief with provenance**, because that is what makes "one observation serves many tasks" and "test beliefs by prediction" fall out of the architecture rather than being bolted on.
