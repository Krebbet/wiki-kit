# Home Tidying and Rearrangement Benchmarks

A reference map of the major simulation benchmarks for household tidying and rearrangement — ALFRED, TEACh, AI2-THOR Rearrangement, Housekeep, BEHAVIOR-1K, and HomeRobot OVMM — covering how each defines "tidy," what metrics they use, what SOTA methods achieve, what perception they assume, and how far sim numbers are from real-robot performance. Companion to [[home-tidying-robots]] (which covers the real-robot systems) and [[semantic-object-memory]] (which covers the Housekeep benchmark's commonsense layer in depth).

---

## 1. Task Definition Taxonomy

The benchmarks divide into four distinct definitions of "tidy":

| Definition | Benchmarks | What the agent must know |
|---|---|---|
| **Restore to initial state** | AI2-THOR Rearrangement (RoomR) | Memorise the pre-shuffled state during a walkthrough; restore it in the unshuffle phase |
| **Place to commonsense receptacle** (no explicit goal) | Housekeep, BEHAVIOR-1K (tidying tasks) | Infer where each object belongs from human-preference data or LLM commonsense — no goal specification given |
| **Pick-and-place to specified receptacle** (language-specified goal) | HomeRobot OVMM, ManiSkill-HAB TidyHouse | Given natural-language command "pick X, place on Y"; success = object reaches Y |
| **Instruction-following with manipulation** | ALFRED, TEACh | Follow natural-language instructions (high-level goal + step-by-step sub-instructions) that may include heating, slicing, cleaning as preconditions to placing |

**The critical distinction for our project** *(synthesis)*: "Restore to initial state" (RoomR) and "place to commonsense receptacle" (Housekeep/BEHAVIOR-1K) are the two most relevant definitions for a home tidy drone. RoomR measures whether the agent can return things to where they were — which is one valid interpretation of "tidy." Housekeep measures whether the agent can infer where things *should* go without being told — which is closer to what a consumer product must do.

---

## 2. Benchmark Reference Table

| Benchmark | Year | Simulator | Task definition | Metric(s) | Real-robot? |
|---|---|---|---|---|---|
| **ALFRED** | CVPR 2020 | AI2-THOR | Instruction-following: 7 task types (place, pick-and-place, heat, cool, clean, examine, stack); natural-language high-level goal + step sub-instructions; egocentric RGB | Task Success (binary); Goal-Condition Success (% of sub-goals reached) | No |
| **TEACh** | AAAI 2022 | AI2-THOR | Dialogue-driven household tasks; Commander with oracle info + Follower that executes; 3 benchmarks: EDH, TfD, TATC | Task Success; Goal-Condition Success; Path Weighted variants | No |
| **AI2-THOR Rearrangement (RoomR)** | CVPR 2021 | AI2-THOR | Restore scene to walkthrough state; 2 tracks: 1-Phase (parallel walkthrough+unshuffle) and 2-Phase (sequential; harder) | SUCCESS (all objects correct); %FixedStrict (fraction fixed without moving wrong objects); %Energy (partial credit); #Changed | No |
| **Housekeep** | ECCV 2022 | iGibson | Agent spawned in untidy house; must infer misplaced objects and rearrange to human-preferred locations without explicit goal; 1,799 objects, 268 categories, 372 annotators | Object Success Rate (OS); Episode Success Rate (ES); Sub-Object Success (SOS) | No |
| **BEHAVIOR-1K** | CoRL 2022 / arXiv 2024 | OMNIGIBSON | 1,000 activities grounded in human-preference survey (1,461 participants); most relevant to tidying: StoreDecoration, CollectTrash, CleanTable; long-horizon; rigid+deformable+liquid physics | Task Success Rate; Efficiency (distance, time, disarrangement) | Limited (one pilot study, CollectTrash only) |
| **HomeRobot OVMM** | CoRL 2023 + NeurIPS 2023 challenge | Habitat | Pick any novel object from start receptacle, place on goal receptacle; open-vocabulary; natural-language goal specification | Overall Success (object on goal receptacle); Partial Success (4-stage sub-goal chain); Steps taken | Yes — Hello Robot Stretch; real-world challenge component |

---

## 3. SOTA Methods and Success Rates

### 3.1 ALFRED

**Baseline (seq2seq, CVPR 2020):** Task Success <5% on seen environments; ≈0.5% on unseen environments. [src: 05-alfred-benchmark.md]

**Human performance:** ≈91% Task Success (unseen test). [src: 05-alfred-benchmark.md]

The seq2seq model in the original paper "performs poorly on ALFRED, suggesting that there is significant room for developing innovative grounded visual language models." Subsequent SOTA (not in primary paper) has improved significantly — leaderboard methods using transformer-based architectures with explicit object tracking reach 30–50% task success on seen environments. The unseen-environment gap is the canonical hard problem: the benchmark rewards generalisation specifically.

**Perception:** RGB only (egocentric). No depth required. Low-level actions are discrete (grid-based movement). Interaction masks are pixelwise — agent selects a pixel of the target object. [src: 05-alfred-benchmark.md]

### 3.2 TEACh

**Baseline (EDH task, paper's best model — "+PM Both" seq2seq):** Task Success ≈4.0% on test-seen, 0.4% on test-unseen. Goal-Condition Success ≈9.4% on test-seen, 7.0% on test-unseen. [src: 04-teach-benchmark.md]

**Human performance:** Task Success 91.0% (unseen). Goal-Condition Success 94.5% (unseen). [src: 04-teach-benchmark.md]

The ≈87 percentage-point gap between human and baseline on test-unseen is the largest human-machine gap across the benchmarks covered here.

**Perception:** RGB egocentric (AI2-THOR). Commander has oracle access to object locations and a map — but the Follower (the executing agent) only has egocentric vision. [src: 04-teach-benchmark.md]

**What makes it hard:** Free-form dialogue, not turn-based; instructions are interleaved with actions; task completion may require resolving ambiguity from chat context across many steps. Not a pure pick-and-place task — sub-tasks like "boil potato", "make coffee", and "prepare breakfast" chain manipulation primitives. [src: 04-teach-benchmark.md]

### 3.3 AI2-THOR Rearrangement (RoomR)

**Baselines (paper, CVPR 2021):**
- Best 1-Phase (RN18+ANM, IL): Train SUCCESS 4.8%, Val 5.2%, Test **3.2%**; %FixedStrict test 8.9%
- Best 2-Phase (RN18+ANM, PPO+IL): Test SUCCESS **0.3%**; %FixedStrict test 1.4%
- Heuristic Expert (oracle state access): Val SUCCESS 88.0%; %FixedStrict 93.1%

[src: 03-ai2thor-rearrangement.md]

The gap between learned baselines (3.2% SUCCESS 1-Phase) and the oracle heuristic expert (88%) is the defining gap of this benchmark. The paper explicitly states that "solving this challenging interactive task that involves navigation and object interaction is beyond the capabilities of the current state-of-the-art techniques." [src: 03-ai2thor-rearrangement.md]

**Challenge 2022 (external results):** Best team achieved 24.47% %FixedStrict on the test set — substantial improvement over the 2021 baselines, but still far below the oracle expert. [src: 08-ai2thor-rearrangement-challenge.md]

**Perception:** RGB + AGENTPOSITION + INWALKTHROUGH sensors. No depth required at inference — depth is permitted during training but not required. Agents must infer 3D object poses from monocular RGB. [src: 03-ai2thor-rearrangement.md]

**Task definition details:** "Tidy" means "restore to the state recorded during walkthrough." The metric SUCCESS requires all object 3D bounding boxes to have IOU ≥ 0.5 with goal poses AND openness state within ±0.2. This is strict — partial placement is not counted as success. %FixedStrict is the primary metric for partial credit without penalising collateral damage. [src: 03-ai2thor-rearrangement.md]

### 3.4 Housekeep

**LLM-based modular baseline (full non-oracle system):** Object Success Rate (OS) = 30% on seen / 23% on unseen; Episode Success Rate (ES) ≈1–4% (compounding errors across 4 required rearrangements per episode). [src: 07-housekeep.md]

**Oracle planner + oracle navigation (upper bound):** OS = 100%; ES = 65–63% — the ceiling is limited by the imprecision of the "magic pointer" interaction primitive, not by the planning module. [src: 07-housekeep.md]

**Key insight from the results:** "With average 4 rearrangements necessary per episode and OS at 46% [with LLM ranker], ES will be 0.46^4 ≈ 0.045." [src: 07-housekeep.md] Episode-level success is a product of per-object success rates — it collapses rapidly with episode length.

**Perception:** RGB-D. The published baseline additionally uses privileged semantic instance segmentation and relationship sensors to focus on the planning/commonsense component. The authors acknowledge: "In the future, these sensors can be easily swapped with their learned counterparts." [src: 07-housekeep.md]

**Real robot:** None. Simulation only (iGibson, Fetch robot, "magic pointer" grasping abstraction). [src: 07-housekeep.md]

### 3.5 BEHAVIOR-1K

**RL-Prim.Hist. (paper's best sim baseline on three activities):** Task Success — StoreDecoration 55±5%, CollectTrash 63±3%, CleanTable 88±2%. [src: 01-behavior-1k.md]

**RL-VMC (end-to-end visuomotor control):** Task Success = 0% across all three tasks — fails completely. [src: 01-behavior-1k.md]

**Key simulation note:** The RL baselines use an "assistive pick primitive" that creates a rigid connection if all fingers contact the object — grasping is not learned and not a source of failure in simulation. This artificially inflates sim success rates. [src: 01-behavior-1k.md]

**Sim-to-real gap (CollectTrash pilot study):**
- Simulation: ~40% success (50 runs, RL-Prim. policy)
- Real world, optimal policy (human-directed action selection): ~22% success (27 runs)
- Real world, learned policy: **0% success** (26 runs)

"The visual discrepancy results from unmodeled effects such as the real camera's poor dynamic range and imperfect object modeling (e.g. wooden texture and surface reflectivity of tables)." Additionally, ~40% of real-world failures stem from grasping — which was bypassed in simulation. [src: 01-behavior-1k.md]

**Perception:** RGB-D from onboard sensors (Tiago bi-manual mobile manipulator); YOLOv3 for object detection; particle filter + two LiDAR for navigation in the real-world pilot. [src: 01-behavior-1k.md]

**Real robot:** Limited. One pilot study with a Tiago robot on CollectTrash only, in a controlled mock apartment. Not a reproducible or scalable evaluation. [src: 01-behavior-1k.md]

### 3.6 HomeRobot OVMM

**Baseline (heuristic modular stack), NeurIPS 2023 competition simulation:**
- Baseline heuristic: 0.8% Overall Success; 17.7% Partial Success
- Baseline RL: 0.0% Overall Success
- Best competition team (Melnik et al.): **10.8% Overall Success**, 32.8% Partial Success

[src: 06-homerobot-challenge-lessons.md]

**Real-world challenge (top 3 teams):**
- Winner (UniTeam, Melnik et al.): **33.3% Overall Success**, 100.0% Partial Success
- Rulai: 0.0% Overall Success, 66.6% Partial Success
- KuzHum: 0.0% Overall Success, 33.3% Partial Success

[src: 06-homerobot-challenge-lessons.md]

**Note on sim vs real discrepancy here:** The real-world top team (33.3%) *outperforms* the simulation winner (10.8%). This is because the real-world challenge was run in a controlled environment on a small set of 3 episodes — small sample size, and the qualification bar (top 3 from simulation) selected for capable teams. This is not evidence that real > sim in general; it is a small-sample artifact. [src: 06-homerobot-challenge-lessons.md]

**HomeRobot paper (pre-competition) real-world baselines:** "Our baselines achieve a 20% success rate in the real world." [src: 02-homerobot-ovmm.md]

**Hardware:** Hello Robot Stretch (wheeled, single telescoping arm, ~$25k). This is the designated real-world platform. The software stack is open-source and designed for reproducibility across labs. [src: 02-homerobot-ovmm.md]

**Perception:** Open-vocabulary — RGB-D from Hello Robot Stretch onboard cameras. No privileged simulator state at inference. The competition explicitly found: "open-vocabulary perception methods were still the main bottleneck for real-world embodied AI, with a very large number of methods failing in challenging real and simulated scenarios." [src: 06-homerobot-challenge-lessons.md]

---

## 4. The Five Questions Answered

### (1) How does each benchmark define "tidy"?

Three distinct definitions exist in the literature:

**Restore-to-initial-state:** AI2-THOR Rearrangement (RoomR). The agent memorises object positions during a walkthrough, is removed while objects are shuffled, then must restore them. "Tidy" = the room matches the walkthrough state. This is objective and measurable but requires a prior "clean" reference — it cannot handle an already-messy starting state. [src: 03-ai2thor-rearrangement.md]

**Commonsense placement without instructions:** Housekeep, BEHAVIOR-1K. No goal is specified. The agent must use human-preference data or LLM commonsense to decide where each object belongs. "Tidy" = objects are in human-preferred locations. This is the most operationally relevant definition for a real consumer device — and the hardest to define precisely for evaluation. [src: 07-housekeep.md, 01-behavior-1k.md]

**Open-vocabulary pick-and-place to specified receptacle:** HomeRobot OVMM. The goal is given as a language command ("pick X from Y, place on Z"). "Tidy" is operationally defined per-task by the command. This sidesteps the hard problem of *deciding* what to tidy but isolates the manipulation+navigation challenge. [src: 02-homerobot-ovmm.md]

**Instruction-following with state changes:** ALFRED, TEACh. These are richer than tidying — they include cooking, cleaning, heating as prerequisites. "Tidy" is one possible outcome but the benchmark includes many non-tidying tasks. These are best understood as general household-task benchmarks, not tidying benchmarks specifically. [src: 05-alfred-benchmark.md, 04-teach-benchmark.md]

### (2) SOTA methods and success rates

| Benchmark | Best reported method | Success rate | Notes |
|---|---|---|---|
| ALFRED | Seq2seq+PM Both (paper) | 4.0% (seen) / 0.4% (unseen) Task Success | Later transformer-based SOTA higher; paper baseline captures the floor |
| TEACh EDH | +PM Both seq2seq | 4.0% / 0.4% Task Success (seen/unseen) | 91% human; massive gap |
| AI2-THOR RoomR | RN18+ANM IL (1-Phase) | 3.2% SUCCESS test; 8.9% %FixedStrict | Challenge 2022 best: 24.47% %FixedStrict |
| Housekeep | LLM modular baseline (full) | 30% OS / ~4% ES (unseen) | Oracle upper bound: 63% ES |
| BEHAVIOR-1K | RL-Prim.Hist. | 55–88% task success (sim, 3 activities) | 0% real robot with learned policy |
| HomeRobot OVMM | Competition winner (Melnik et al.) | 10.8% (sim); 33.3% (real, 3 episodes) | 20% baseline real-world (paper) |

### (3) Are any SOTA methods runnable on real robot hardware?

**HomeRobot OVMM** is the only benchmark with a sustained, reproducible real-robot component. The NeurIPS 2023 competition evaluated three teams in a real apartment on a Hello Robot Stretch. The competition framework provides a Docker-based stack meant for cross-lab reproducibility. [src: 06-homerobot-challenge-lessons.md]

**BEHAVIOR-1K** conducted one pilot study with a Tiago robot, but this was not a competition or reproducible benchmark — it was an ablation study of sim-to-real sources. [src: 01-behavior-1k.md]

**ALFRED, TEACh, AI2-THOR Rearrangement, Housekeep:** Simulation-only. No real-robot track exists or has been run. [src: 05-alfred-benchmark.md, 04-teach-benchmark.md, 03-ai2thor-rearrangement.md, 07-housekeep.md]

**TidyBot (outside these benchmarks):** The only system in the broader tidying-robot landscape with a strong real-robot result is TidyBot (see [[home-tidying-robots]]), which achieves 85% on its own evaluation — but TidyBot is a system paper, not a benchmark, and its evaluation is internal to the paper, not a public leaderboard.

### (4) What perception stack do competitive methods assume?

| Benchmark | Perception at inference | Privileged state used? |
|---|---|---|
| ALFRED | RGB egocentric | No depth. No ground-truth object labels. Pixelwise interaction mask from RGB. |
| TEACh | RGB egocentric (Follower); Commander has oracle map/location | Commander is oracle; Follower is RGB-only. Most methods train only the Follower. |
| AI2-THOR Rearrangement | RGB + agent position + INWALKTHROUGH flag | No depth required. No ground-truth object state. |
| Housekeep (paper baseline) | RGB-D + **privileged** semantic instance seg + relationship sensor | Yes — paper baseline uses privileged sensors; intended to be swapped for learned versions |
| BEHAVIOR-1K (paper baseline) | RGB-D for policy; YOLOv3 detection for object localisation | Assistive-pick primitive in sim (privileged grasping contact detection) |
| HomeRobot OVMM | RGB-D (Hello Robot onboard cameras); open-vocabulary detection | No privileged state at inference |

**Pattern:** Simulation-only benchmarks (ALFRED, TEACh, RoomR, Housekeep) permit privileged signals that don't exist on real hardware — perfect navigation affordances, ground-truth segmentation, oracle interaction masks. The only benchmark enforcing real perception throughout is HomeRobot OVMM. BEHAVIOR-1K uses a hybrid: real RGB-D for navigation/detection, but an assistive pick primitive that bypasses the hardest real-world manipulation challenge.

### (5) Sim-to-real gap: what is it?

**BEHAVIOR-1K (CollectTrash, best available data):**
- Sim: ~40% (learned policy)
- Real (optimal/oracle action selection): ~22%
- Real (learned policy): **0%**

The gap between sim-optimal and real-optimal (~40% → ~22%) isolates actuation error. The gap between real-optimal and real-learned (22% → 0%) isolates visual domain shift. Grasping failure (~40% of real-world failures) is the single largest error source; it does not appear in sim because the assistive-pick primitive bypasses it. [src: 01-behavior-1k.md]

**HomeRobot OVMM (challenge lessons):** The competition found "open-vocabulary perception methods were still the main bottleneck for real-world embodied AI." Classical robotics stacks required less tuning than RL-based systems in real-world deployment. [src: 06-homerobot-challenge-lessons.md]

**General pattern** *(synthesis)*: Across all benchmarks, the sim-to-real gap is driven by three sources in roughly descending order of severity: (1) grasping — bypassed in simulation via sticky/assistive primitives, catastrophically fails on real hardware; (2) visual domain shift — simulated textures, lighting, and camera properties differ from real sensors in ways that break learned policies; (3) navigation error — planning assumes perfect localisation in sim, compounds into manipulation failures in the real world.

---

## 5. TidyBot Evaluation Metric and Real Hardware Success

TidyBot (Stanford/Princeton/Google, IROS 2023) uses its own internal evaluation, not a public benchmark. The evaluation consists of:

- **Benchmark accuracy:** 91.2% on a dataset of 96 scenarios × 4 room types × 1,076 unique object names. Metric: whether the LLM-generated rule assigns the correct receptacle to an unseen object. [src: [[home-tidying-robots]] → arXiv 2305.05658]

- **Real-robot success rate:** 85.0% across 240 objects in 8 room scenarios (3 runs each). Breakdown: object localisation 92.5% + egocentric classification 95.5% + LLM receptacle+primitive selection 100% + manipulation primitive execution 96.2% = end-to-end 85.0%. [src: [[home-tidying-robots]] → arXiv 2305.05658; [[tidybot-deep-dive]]

This is the highest published real-robot tidying success rate in the literature, achieved on a custom wheeled manipulator in a lab/home-like environment. The evaluation is self-contained (not a public competition), the manipulation primitives are hard-coded (not learned), and receptacle locations are hard-coded per scenario. See [[tidybot-deep-dive]] for the full evaluation protocol.

---

## 6. Cross-Benchmark Themes *(synthesis)*

**No benchmark targets the "what needs tidying" sub-problem.** ALFRED and TEACh give the agent an explicit goal. Housekeep and BEHAVIOR-1K give the agent an untidy scene but tell it which objects exist. None require the agent to first *detect* whether a room is untidy and *decide* what to prioritise — the "what needs doing" cognition layer. This is the gap our project must solve that no existing benchmark measures.

**Commonsense placement ("where does this go?") remains unsolved in the fully-autonomous case.** Housekeep's best non-oracle result is ~4% episode success (all objects correctly placed in one episode). The compounding error across sequential rearrangements is the core reason — even 30% per-object accuracy yields <5% episode accuracy for a 4-object episode. This suggests that per-object success needs to be very high (>90%) before episode-level "room is tidy" success becomes practical.

**Grasping is the dominant real-world blocker, not perception or planning.** BEHAVIOR-1K's sim-to-real study is the most carefully designed analysis: with an optimal policy, ~40% of real-world failures were grasping failures — a category that was completely masked in simulation. This holds for any benchmark that uses "magic grasp" or assistive-pick primitives.

**The useful benchmark for our project is HomeRobot OVMM:** it is the only one with (a) open-vocabulary perception, (b) a real-robot track, (c) natural-language goal specification, and (d) a public competition track with reproducible evaluation. Its 10.8% simulation / 20% real baseline gives the most honest current ceiling for a system like ours.

**RoboTHOR:** RoboTHOR (AllenAI) provides a sim-to-real *navigation* platform using identical floor plans in simulation and a physical apartment. The 2021 challenge was sim-only due to COVID. Its navigation-only scope (ObjectNav, not rearrangement or manipulation) makes it less relevant for tidying than the benchmarks above, though it is the most carefully validated sim-to-real navigation platform in the field.

---

## 7. Implications for Our Project *(synthesis)*

1. **Our success metric should be Housekeep-style, not RoomR-style.** The restore-to-initial-state definition (RoomR) requires an a priori reference state — meaning the robot must have previously seen the room "tidy." A consumer device cannot assume this. Housekeep-style commonsense placement (infer where things go from user examples or LLM) is the correct frame. TidyBot's real-robot 85% personalised placement is the current performance reference.

2. **Episode success at 85% per-object gives ~44% per 4-object episode.** (0.85^4 ≈ 0.52; accounting for real error independence this is likely lower.) This is the realistic capability floor for a Phase 1 system. The benchmark literature shows that even 30% per-object collapses to ~4% episode success. We should report per-object success initially, not episode success.

3. **The grasping problem dominates.** Across all benchmarks that tested real hardware, grasping failure is the #1 cause of real-world failure not present in simulation. Our [[onboard-grasp-perception]] page identifies that aerial OVD at ~28% F1 is the current ceiling for open-world detection from drones — the same wall exists and is likely worse in the aerial case.

4. **HomeRobot OVMM's Hello Robot Stretch at 20% real-world baseline** is the honest SOTA for an open-vocabulary pick-and-place system on real hardware. Our Phase 1 should aim for parity with this (pick one specified object, place on specified receptacle) before attempting commonsense placement.

5. **Privileged sim signals don't transfer.** No benchmark that uses oracle navigation, privileged segmentation, or assistive-pick primitives produces results that generalise to real hardware. We should not build on any benchmark number that uses privileged signals.

---

## Source

- `raw/research/tidy-benchmarks/01-behavior-1k.md` — arXiv 2403.09227 · *BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation* · Stanford + multi-inst., CoRL 2022 / arXiv 2024.
- `raw/research/tidy-benchmarks/02-homerobot-ovmm.md` — arXiv 2306.11565 · *HomeRobot: Open-Vocabulary Mobile Manipulation* · Georgia Tech / FAIR Meta AI, CoRL 2023.
- `raw/research/tidy-benchmarks/03-ai2thor-rearrangement.md` — arXiv 2103.16544 · *Visual Room Rearrangement* · AllenAI / UW, CVPR 2021. Introduces RoomR dataset and 4-metric evaluation framework.
- `raw/research/tidy-benchmarks/04-teach-benchmark.md` — arXiv 2110.00534 · *TEACh: Task-driven Embodied Agents that Chat* · Amazon Alexa AI / U Illinois, AAAI 2022.
- `raw/research/tidy-benchmarks/05-alfred-benchmark.md` — arXiv 1912.01734 · *ALFRED: A Benchmark for Interpreting Grounded Instructions for Everyday Tasks* · MIT / Allen AI / UW, CVPR 2020.
- `raw/research/tidy-benchmarks/06-homerobot-challenge-lessons.md` — arXiv 2407.06939 · *Towards Open-World Mobile Manipulation in Homes: Lessons from the NeurIPS 2023 HomeRobot OVMM Challenge* · Multi-institution, 2024.
- `raw/research/tidy-benchmarks/07-housekeep.md` — arXiv 2205.10712 · *Housekeep: Tidying Virtual Households using Commonsense Reasoning* · Georgia Tech / Meta AI, ECCV 2022.
- `raw/research/tidy-benchmarks/08-ai2thor-rearrangement-challenge.md` — ai2thor.allenai.org/rearrangement · *AI2-THOR Rearrangement Challenge 2022* · AllenAI. Challenge results page (2022 winner: 24.47% %FixedStrict).

---

## Related

- [[home-tidying-robots]] — real-robot systems: TidyBot, TidyBot++, WRC2020, ManiSkill-HAB
- [[tidybot-deep-dive]] — TidyBot v1+v++ hardware, methods, cost
- [[semantic-object-memory]] — Housekeep commonsense layer; ConceptGraphs; scene graph architectures
- [[onboard-grasp-perception]] — aerial OVD gap; open-world grasping limits
- [[system-architecture]] — our full cognitive stack; where benchmarks connect
- [[world-model-architecture]] — the map form factor that must support tidying tasks
- [[home-tidy-drone-prototype]] — Phase 1 build plan; how benchmark targets inform requirements
