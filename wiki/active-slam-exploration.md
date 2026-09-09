# Active SLAM and Autonomous Exploration for Indoor Ground Robots

**Active SLAM** is the problem of *controlling* a robot that is doing SLAM so as to reduce the uncertainty of its own pose estimate *and* of the map — i.e. deciding **where to drive next in order to map well**, and **when to stop**. It is the missing control layer above [[2d-lidar-slam]] / [[slam-toolbox]], which only tell you what to do with data once it arrives. This page covers the four things our first autonomous run needs: how candidate goals are generated (**frontiers**), how "how much would I learn by going there?" is actually computed cheaply (**information gain / next-best-view**), how localisation uncertainty enters the decision (the **exploration-vs-exploitation** tension that makes it *active SLAM* rather than mere coverage), and how a system decides a region is **sufficiently observed**. It closes with the parts specific to our rig — a slow tethered rover, RPLIDAR C1 in a ~1.1 m scan plane, **no wheel encoders**, accuracy prioritised over speed — and a recommended ladder. The literature's answer to the human's guiding principle ("*identify where our information is LACKING, gather it, update priors*") is precisely the utility-function taxonomy in §3; the honest headline is that the *stopping* half of that principle is an acknowledged **open problem** in the field, not a solved recipe [src: placed-survey].

## Source

| Tag | Work | Venue / Year |
|---|---|---|
| placed-survey | Placed, Strader, Carrillo, Atanasov, Indelman, Carlone, Castellanos — *A Survey on Active Simultaneous Localization and Mapping* (arXiv 2207.00254) | IEEE T-RO 2023 |
| asl-review-decade | Ahmed, Bakht, Hussain et al. — *Active SLAM: A Review on Last Decade* (arXiv 2212.11654) | Sensors 2023 |
| placed-laplacian | Placed & Castellanos — *A General Relationship Between Optimality Criteria and Connectivity Indices for Active Graph-SLAM* (arXiv 2110.01289) | IEEE RA-L 2022 |
| yamauchi97 | Yamauchi — *A Frontier-Based Approach for Autonomous Exploration* (Nomad 200, laser + sonar + IR) | CIRA 1997 |
| frontier-detect-compare | Quin, Alempijevic, Paul et al. — *Approaches for Efficiently Detecting Frontier Cells in Robotics Exploration* (Naive/NaiveAA/WFD/WFD-INC/EWFD/FTFD benchmark) | Frontiers in Robotics & AI 2021 |
| umari17 | Umari & Mukhopadhyay — *Autonomous Robotic Exploration Based on Multiple Rapidly-exploring Randomized Trees* (RRT frontier detector, ROS) | IROS 2017 |
| explore-lite-src | `robo-friends/m-explore-ros2` — `explore/config/params.yaml`, `explore/src/frontier_search.cpp` (read 2026-09) | ROS 2 pkg |
| fe-ros2-2025 | `mertgulerx/frontier_exploration_ros2` — modern C++ WFD + MRTSP exploration for ROS 2 Jazzy / Nav2 | 2025 |
| charrow-csqmi | Charrow, Kahn, Patil, Liu, Goldberg, Abbeel, Michael, Kumar — *Information-Theoretic Planning with Trajectory Optimization for Dense 3D Mapping* (CSQMI) | RSS 2015 |
| fsmi | Zhang, Henderson, Sze, Karaman — *FSMI: Fast Computation of Shannon Mutual Information for Information-Theoretic Mapping* (arXiv 1905.02238) | ICRA 2019 / IJRR 2020 |
| infopred | *Enhancing Exploration Efficiency using Uncertainty-Aware Information Prediction* (arXiv 2412.12825) — BNN map prediction beyond line-of-sight | 2024 |
| fuel | Zhou, Zhang, Chen, Shen — *FUEL: Fast UAV Exploration using Incremental Frontier Structure and Hierarchical Planning* (arXiv 2010.11561) | RA-L 2021 |
| heros | *HEROS: Hierarchical Exploration with Online Subregion Updating* (arXiv 2407.11326) — TARE/DSVP/FUEL comparison, raycast cost breakdown | 2024 |
| sae-lighthouses | *Lighthouses and Global Graph Stabilization: Active SLAM for Low-compute, Narrow-FoV Robots* (arXiv 2306.10463) — SLAM-aware exploration (SAE), real homes | ICRA 2023 |
| map-completeness | *Estimating Map Completeness in Robot Exploration* (doi 10.1007/s10514-025-10221-8) | Autonomous Robots 2025 |
| slam-toolbox-221 | `SteveMacenski/slam_toolbox` issue #221 — *Support mapping without odometry* (opened 2020-07-09, closed) | GitHub |
| stop-and-scan | *Occlusion-Aware Visibility Coverage for Robotic Stop-and-Scan 3D LiDAR Mapping* (MDPI Sensors 26(17):5430); *Stop-and-Go Mode: Sensor Manipulation as Essential as Sensor Development in TLS* | 2025 / 2013 |
| 2dliw | *2DLIW-SLAM: 2D LiDAR-Inertial-Wheel Odometry with Real-Time Loop Closure* (arXiv 2404.07644) — 2D motion degeneracy | 2024 |
| door-laser | *Laser-Based Door Localization for Autonomous Mobile Service Robots*; *Multi-LiDAR Mapping for Scene Segmentation in Indoor Environments* | PMC 2023 / 2022 |
| boustrophedon | Choset & Pignon — *Coverage Path Planning: The Boustrophedon Cellular Decomposition* (doi 10.1007/978-1-4471-1273-0_32) | FSR 1997/98 |
| husarion-explore | Husarion ROS/ROS 2 exploration tutorial — practical `explore_lite` failure notes | tutorial |

## Related

- [[2d-lidar-slam]] — the estimator this control layer sits on top of (Cartographer submaps/BBS/SPA; RPLIDAR hardware table incl. our C1).
- [[slam-toolbox]] — the intended back-end; note its **odom→base_link TF requirement**, which is a hard constraint for us (§6).
- [[ros2-nav2]] — the goal executor. Nav2 ships **no** exploration behaviour; frontier exploration is always a third-party node driving `NavigateToPose`.
- [[robot-vacuum-navigation]] / [[consumer-robot-vacuum-mapping]] — the only mass-deployed indoor precedent; they do **systematic coverage**, not information-driven exploration (§5).
- [[map-then-navigate]] — the two-phase architecture this page's "phase 1" belongs to.
- [[robust-evidence-mapping-principle]] — the project's own principle; §7 maps it onto the literature's utility functions.
- [[room-segmentation-floor-plan]] · [[floorplan-reconstruction-methods]] — what the exploration output feeds.
- [[weak-scan-registration-methods]] — why single-wall views are *unobservable*, which is exactly what a bad exploration policy will hand you (§6).
- [[indoor-cluttered-slam]] · [[indoor-obstacle-avoidance]] · [[dynamic-object-handling]] — clutter, safety and the door-state problem.
- [[mapping-stack-design]] · [[home-tidy-drone-prototype]] · [[anchor-map-protocol]].

---

## 1. The canonical decomposition

Nearly every deployed system, and the survey's own taxonomy, splits active SLAM into **three sequential stages** [src: placed-survey]:

| Stage | Question | Typical answer |
|---|---|---|
| **1. Identification** | What are the candidate goals? | Frontiers; sampled viewpoints (RRT/RRT*); **plus revisit candidates** in active-SLAM-proper methods |
| **2. Utility computation** | What is the expected cost/benefit of each? | Distance − information gain; entropy reduction; a TOED optimality criterion on the pose-graph |
| **3. Action selection** | Which do I execute? | Enumerate (small candidate sets) or optimise (MPC / trajectory optimisation) |

The survey is explicit that stage 1 exists **"solely to reduce the computational burden"**, and that solving the three stages separately rather than jointly "can produce suboptimal results and lead to undesired behaviors" [src: placed-survey]. The theoretically-correct formulation is a POMDP — 7-tuple (X, A, O, T, ρ_o, β, γ), maximising `E[Σ γ^t β(x_t,a_t)]` — which is intractable, so everyone approximates with the three-stage pipeline [src: asl-review-decade].

There is a **fourth stage that the literature under-serves**: *deciding to stop*. §4.

---

## 2. Frontier-based exploration

### 2.1 The classic (Yamauchi 1997)

A **frontier** is the boundary between known-free and unknown space. The canonical cell-level definition: *"cells of an occupancy grid that are freespace and which have at least one neighboring cell that has an unknown state"* [src: frontier-detect-compare, yamauchi97].

The original algorithm on a Nomad 200 (laser rangefinder + 16 sonar + 16 IR): a **BFS over the whole grid** collects frontier cells into a queue, a **second BFS over those cells** groups them into connected frontier *regions*, region **centroids** are ordered by Euclidean distance from the robot, and the robot drives to the **nearest** one [src: yamauchi97, frontier-detect-compare]. Repeat until no frontiers remain. That "nearest frontier, greedily, until exhaustion" loop is still the production default 29 years later.

### 2.2 Frontier detection algorithms — the part that actually costs CPU

Re-running a full-grid BFS every scan does not scale. The systematic benchmark [src: frontier-detect-compare]:

| Algorithm | Complexity | Mechanism | Notes |
|---|---|---|---|
| **Naive** | O(\|M\|) — whole map | Scan every cell | >1 s on a 200×200 m @ 5 cm map — **cannot hold a 2 Hz SLAM update rate** |
| **NaiveAA** | ~O(\|A\|), active area only | Scan only cells touched by the last scan | Recommended as the *new benchmark* — trivially simple, fast enough |
| **WFD** (Wavefront Frontier Detector) | O(\|F\|) | BFS outward from robot pose | Slower than the incremental variants |
| **WFD-INC** | O(\|A\|) | WFD bounded to the active area | Cost proportional to scan coverage, not map size |
| **EWFD** (Expanding-Wavefront) | O(\|A\|) best / O(\|F\|) worst | Seeds BFS from *previous* frontier cells | **Best for corridors / narrow paths** |
| **FTFD** | O(\|A\|) best / O(\|F\|) worst | Uses scan perimeter + ray endpoints only | **Best for open spaces** |
| **FFD** (Fast Frontier Detector) | — | Bresenham line over scan | Less accurate at max sensor range (Bresenham artefacts); must run after *every* scan |
| **RRT-based** (Umari & Mukhopadhyay) | sampling | Local + global RRTs, biased toward unexplored space | Generalises past 2D image-processing detectors to n-D [src: umari17] |

All the active-area variants (NaiveAA, WFD-INC, EWFD, FTFD) run in **<0.5 s** on the 200×200 m @ 5 cm real-world map — faster than the SLAM update itself [src: frontier-detect-compare].

**Trap:** EWFD and FTFD **cannot detect "pockets"** of enclosed unknown space, because they assume the sensor FOV prevents unknown regions from becoming encapsulated [src: frontier-detect-compare]. For a single room with furniture that occludes small pockets (under a table, behind a bin — exactly our case at a 1.1 m scan plane), that assumption is wrong. *(synthesis: use NaiveAA or WFD-INC for a single room; the map is tiny and the "efficient" detectors buy us nothing while costing correctness.)*

### 2.3 `explore_lite` — what the ROS 2 default actually does

`explore_lite` (`m-explore-ros2`) is greedy frontier exploration driving Nav2. Verified from source [src: explore-lite-src]:

**Frontier cell test** (`isNewFrontierCell`) — note this is the **inverse** of Yamauchi's convention: it marks a cell as a frontier if the cell is `NO_INFORMATION` **and** at least one of its **4-connected** neighbours is `FREE_SPACE`. Frontier cells are *unknown* cells adjacent to free space, not free cells adjacent to unknown.

**Cost function** (`frontierCost`) — the entire "intelligence" of the package is two terms:

```
cost = potential_scale · frontier.min_distance · resolution
     − gain_scale     · frontier.size         · resolution
```

`min_distance` is the distance to the **closest cell** of the frontier (not its centroid); `size` is the frontier's cell count — a **pure proxy for information gain**. Lowest cost wins.

**Defaults** (`params.yaml`) [src: explore-lite-src]:

| Parameter | Default | Meaning |
|---|---|---|
| `planner_frequency` | **0.15 Hz** | Frontiers recomputed / goal reconsidered every ~6.7 s |
| `progress_timeout` | **30.0 s** | Abandon + blacklist the current goal if no progress |
| `potential_scale` | **3.0** | Weight on distance (drives greedy-nearest behaviour) |
| `orientation_scale` | **0.0** | Heading-change penalty — **disabled by default** |
| `gain_scale` | **1.0** | Weight on frontier size |
| `transform_tolerance` | 0.3 s | TF lookup slack |
| `min_frontier_size` | **0.75 m** | Frontiers smaller than this are discarded |
| `return_to_init` | true | Drive home when frontiers are exhausted |

With `potential_scale = 3.0` vs `gain_scale = 1.0`, the default policy is **overwhelmingly "go to the nearest frontier"**; frontier size only breaks near-ties. *(synthesis: this is worth knowing before assuming explore_lite is doing information-theoretic reasoning — it is not.)*

**Reported failure modes** [src: husarion-explore, explore-lite-src]:
- *"All frontiers traversed/tried out"* immediately at startup — too little free space mapped to move in any direction. The standard fix is to **spin in place under teleop first** to seed the map.
- Oscillation / repeatedly re-attempting unreachable goals — mitigated only by `progress_timeout` blacklisting, which is a crude symptom fix.
- Goal thrash: at 0.15 Hz replanning, a frontier that gets consumed mid-drive leaves the robot driving to a stale goal.
- Termination is **frontier exhaustion only** — there is no accuracy-aware or coverage-quality criterion whatsoever.

### 2.4 The 2025 state of the practice

`frontier_exploration_ros2` shows where the engineering has actually moved [src: fe-ros2-2025]:

- **Decision-map preprocessing before detection**: bilateral filter on the occupancy grid (`sigma_s` 2.0 spatial, `sigma_r` 30.0 range), re-threshold, then circular dilation of free space by 1 cell. This kills spurious frontiers from sensor noise while preserving narrow passages — *sensor noise generating phantom frontiers is a real, addressed problem*.
- **Clusters smaller than `min_frontier_size_cells` = 5 are rejected.**
- **Non-greedy ordering** via a Minimum-Ratio TSP cost `M(i,j) = (w_d · d(V_i,V_j)) / (w_s · P(V_i,V_j))` with `P` = cluster size and `d` discounted by the sensor range `r_s`; default `w_d = w_s = 1.0`. Solved either greedily or by **bounded-horizon bitmask DP** (top 15 candidates, horizon 10, dispatch only the first, replan on map update).
- **Active-goal preemption**: cancel the current frontier if the *visible reveal gain* from the target pose drops below threshold (checked every 2.0 s).
- **Frontier suppression**: temporarily blacklist a frontier area after N failed attempts, TTL 90 s.
- Benchmark, 1,500 m² warehouse: greedy-MRTSP **36.60 m / 63 s** vs nearest-frontier **37.72 m / 73 s** vs `m_explore_ros2` **50.73 m / 96 s**; CPU 7.4% / 4.0% / 2.4%. Up to **99.9% coverage** across maze, dense-obstacle and open-space layouts.

*(synthesis: the ~28% distance saving over `explore_lite` comes from **ordering** — not from information theory. For one room at low speed, distance efficiency is nearly irrelevant to us; the *preprocessing* and *preemption* ideas are the transferable parts.)*

### 2.5 Known failure modes of frontier exploration (summary)

| Failure | Cause | Mitigation in the literature |
|---|---|---|
| Assumes **perfect localisation** | Frontier utility ignores robot pose uncertainty; "high uncertainty in the robot state estimation leads to wrong expected map uncertainties" (Bourgault et al. 1998) [src: placed-survey] | Add pose-uncertainty term → §3 |
| **Never revisits** | No mechanism to trade coverage for loop closure; drift compounds | Add revisit candidates (Stachniss 2008, Valencia et al.) [src: placed-survey] |
| **Noise frontiers** | Speckle in the grid creates 1-cell "unknown" islands | `min_frontier_size`; bilateral-filtered decision map [src: fe-ros2-2025] |
| **Pockets missed** | EWFD/FTFD detectors structurally cannot see enclosed unknowns | Use active-area or full detectors [src: frontier-detect-compare] |
| **Greedy myopia / backtracking** | Nearest-first leaves regions half-done; TARE shows this explicitly, "several instances of backtracking as some rooms... are left unexplored" [src: heros] | Hierarchical / global tour ordering (FUEL, MRTSP) |
| **Non-orthogonal geometry** | Grid/4-connectivity assumptions degrade on angled walls | — (acknowledged, largely unaddressed) |
| **Stops at frontier exhaustion regardless of quality** | Coverage ≠ accuracy | §4 |

---

## 3. Next-best-view and information gain — computing "how much would I learn?"

### 3.1 The quantity being approximated

The exact objective is the **mutual information** between the future measurement and the joint (pose, map) belief — the *expected reduction in joint entropy* [src: placed-survey]:

```
I(a) ≜ H[p(x,m | h)] − E[ H[p(x,m | h, ẑ, a)] ]
```

with, for a Gaussian pose belief and a discrete occupancy grid respectively:

```
H[p(x)]                  = ½ · ln( (2πe)^ℓ · det(Σ_r) )
H[p(m | x,h,ẑ,a)]        = − Σ_c θ_c log θ_c
```

Related measures used in practice: **Kullback-Leibler divergence** `D_KL(A‖B) = Σ A(x) log(A(x)/B(x))` (captures both distribution-shape change and mean shift), and **Rényi entropy**, of which Shannon is the α→1 case and **quadratic** (α=2) is the computationally cheap case [src: placed-survey, asl-review-decade].

### 3.2 The cheap-computation ladder (this is the practical content)

Nobody evaluates the exact integral. The realistic options, cheapest first:

| Level | Method | Cost | What it captures |
|---|---|---|---|
| 0 | **Frontier cell count** as gain proxy (`explore_lite`, FUEL's frontier information structure) | ~free | Size of the unknown boundary only |
| 1 | **Raycast unknown-cell count**: cast the sensor's beams from the candidate pose through the current grid, count unknown cells hit before an occupied one | cheap-ish, but see warning | Visibility-aware coverage gain |
| 2 | **CSQMI** — Cauchy-Schwarz Quadratic MI, from Rényi quadratic entropy (Charrow et al.) | ~2× the cost of FSMI | A true MI surrogate; behaves like Shannon MI, computes much faster; used to select **paths**, not just destinations, which avoids the local minima of myopic gradient-following [src: charrow-csqmi] |
| 3 | **FSMI** — Fast Shannon MI (Zhang, Henderson, Sze, Karaman) | fastest exact-Shannon | Key insight: **the integral over the sensor beam can be evaluated analytically** for Gaussian sensor noise, removing the numerical integration. **>3 orders of magnitude** faster than prior Shannon-MI computation and **~2× faster than CSQMI** [src: fsmi] |
| 4 | **Learned map prediction** — predict occupancy *beyond line of sight*, then compute MI on the prediction | NN inference | See §3.4 |

**Warning, load-bearing:** raycast-based gain is not cheap at scale. In DSVP, *"more than 90% of the runtime"* is consumed by raycast-based gain computation — counting unknown voxels and checking sensor visibility — which produces "long iteration times, leading to delayed decision-making" [src: heros]. Budget for this before designing around it. *(synthesis: for a single ~4×5 m room at 5 cm resolution — ~8,000 cells — a full raycast sweep over even a few hundred candidate poses is trivially affordable. The DSVP warning is about large 3D volumes; it does not bind us. We can afford level 1 or 2 immediately.)*

### 3.3 The unknown-cell trap

Every unknown grid cell sits at p = 0.5, which is **maximum entropy**. A naive MI/entropy objective therefore rewards staring at the largest blob of unknown, regardless of whether anything is learnable there. As the prediction paper puts it, unknown grids at 0.5 occupancy probability *"signify an absence of information"*, so *"predicted future measurements for unknown areas greatly differ from reality, leading to inaccurate assessments"* [src: infopred]. This is the mechanism behind the classic complaint that information-theoretic exploration drives robots at big empty voids.

The broadly-adopted practical fix, verified by Stachniss et al. and now near-universal, is simply to **combine a distance/cost term with the information term** rather than maximise information alone [src: placed-survey] — which is exactly the `explore_lite` cost function, and exactly the MRTSP ratio.

### 3.4 Predicting information beyond line of sight

The survey names *"prediction beyond line-of-sight"* as an open problem: traditional ray-casting is insufficient, and neural scene completion (autoencoders, VAEs) is emerging but *"integration into active SLAM is yet to be done"* [src: placed-survey]. The 2024 concrete instance [src: infopred]: crop the occupancy grid to 256×256 px around each frontier, run a **U-Net with MC dropout** (a Bayesian NN, trained on 2D indoor layouts) to predict occupied/free for the unknown cells, take **10 stochastic forward passes** to get epistemic variance, then compute FSMI on the *predicted* map while probabilistically discounting high-uncertainty predictions. Result: **21–40% faster exploration** across four simulated environments (e.g. 157.54 s vs 269.91 s baseline).

*(synthesis: this is the literature's version of the human's "align to priors, then discover discrepancies". For us the prior is not a learned U-Net but the **room's structure** — a rectilinear wall hypothesis, the [[floorplan-reconstruction-methods]] line model. Predicting "the wall probably continues to that corner" and then measuring whether it does is the same mechanism, and is a far better fit for us than a trained network.)*

---

## 4. Active SLAM proper — when localisation uncertainty enters

This is what separates *active SLAM* from *coverage*. The survey's framing: for a robot with **high uncertainty, potential loop-closure areas encode more information than frontiers**, and the goal "goes beyond simply covering the workspace" [src: placed-survey].

### 4.1 TOED optimality criteria

Uncertainty is a covariance matrix Σ (or its inverse, the Fisher information matrix Y); to rank actions you need a **scalar**. The Theory of Optimal Experimental Design supplies Kiefer's family [src: placed-survey, asl-review-decade]:

| Criterion | Kiefer p | Scalarisation | Geometric meaning |
|---|---|---|---|
| **T-opt** | p = 1 | `trace(Σ)` / mean eigenvalue | Average variance |
| **A-opt** | p = −1 | harmonic mean of eigenvalues | Average variance (harmonic) |
| **D-opt** | p = 0 | `det(Σ) = Π ζ_i` | **Volume** of the uncertainty ellipsoid |
| **E-opt** | p → ±∞ | `max ζ_i` | Longest ellipsoid axis (worst case) |

**Critical property:** the survey stresses that **only D-optimality guarantees monotonicity** under the Kiefer formulation (Carrillo et al.) — i.e. adding an observation cannot make the criterion look worse [src: placed-survey]. A/E/T-opt can rank actions inconsistently. *If you implement exactly one uncertainty criterion, implement D-opt.*

### 4.2 Graph-Laplacian shortcut — the thing that makes this affordable

Computing det(Σ) requires inverting/factorising the information matrix, which is why uncertainty-aware exploration was long considered too slow. Khosoussi et al. (2016) and Placed & Castellanos closed this: the FIM of a graph-SLAM system decomposes as `Y = Σ_j E_j ⊗ Σ_j⁻¹`, and under constant per-edge uncertainty simplifies to **`Y = L ⊗ Φ̄`** where **L is the pose-graph Laplacian** — so optimality criteria become **pure graph-connectivity indices** [src: placed-laplacian]:

| Criterion | Equivalent graph index |
|---|---|
| **T-opt** | ∝ average pose-graph degree `d̄` |
| **D-opt** | ∝ `(n · t(𝒢))^(1/n)`, where `t(𝒢)` = **number of weighted spanning trees** |
| **A-opt** | ∝ `n² · K(𝒢)⁻¹`, `K` = **Kirchhoff index** |
| **E-opt** | ∝ **algebraic connectivity** `α(𝒢)` |

Measured over 10 datasets (2D and 3D): **2% median approximation error** for D-opt, **<0.5%** for T-opt, **~10× speedup (mean 90.1% time reduction)**, and — the headline — on the *Garage* dataset (1,661 poses, 2,615 edges) the traditional FIM computation took **1,549.9 min vs 11.70 min** via the Laplacian, with **identical optimisation trends** [src: placed-laplacian].

*(synthesis: this means "will going there make my pose graph better?" costs a **graph** computation, not a **covariance** computation. For a one-room graph of a few hundred nodes it is essentially free — this is the single most actionable result on this page for building an accuracy-driven explorer.)*

### 4.3 The exploration/exploitation tension

The canonical statement (Thrun & Möller): the agent must *"switch between two opposite principles — exploring new areas and revisiting those already seen"* [src: placed-survey]. Timeline of the idea [src: placed-survey]:

| Year | Work | Contribution |
|---|---|---|
| 1988 | Bajcsy | Formal definition of active perception |
| 1997 | Yamauchi | Frontier concept |
| 1998 | Fox et al. / Bourgault et al. | Goal-ID → utility → selection pipeline; frontier methods ignore robot uncertainty |
| 1999 | Feder et al. | **First** to choose actions maximising knowledge of *both* map and pose |
| 2002 | Davison & Murray | Coins "active SLAM" |
| 2008 | Stachniss et al. | **"Regions where sensor readings overlap may be more informative than new frontiers"** — put revisit candidates in the same candidate set as frontiers |
| 2013 | Carrillo et al. | Shannon–Rényi entropy analysis; restores D-opt via Kiefer |
| 2016 | Khosoussi et al. | Graph Laplacian ↔ D-opt/E-opt duality |
| 2020+ | Chaplot et al.; Niroui et al.; Placed & Castellanos | Deep-RL coverage; DRL + frontier hybrids; SE(n) graph generalisations |

The **modern practical recipe** is not exotic: put **frontiers and revisit poses into one candidate list**, score both with a utility that mixes distance, map information gain, and a pose-uncertainty term, and let the argmax decide when to stop exploring and go re-close a loop [src: placed-survey].

### 4.4 SAE / "lighthouses" — the closest precedent to our situation

The most directly relevant paper for a consumer-grade, low-compute, limited-FoV robot [src: sae-lighthouses]: *"Instability in a SLAM system can lead to poor-quality maps and subsequent navigation failures during or after exploration. This becomes particularly noticeable in consumer robotics, where compute budget and limited field-of-view are very common."* Their **SLAM-aware exploration (SAE)** contributes (i) **lighthouses** — panoramic views with high visual information content, used to maintain map stability *locally in their neighbourhoods* — and (ii) a **final global pose-graph stabilization** pass at the end of exploration. Evaluated on real home environments (ICRA 2023).

*(synthesis: "designated high-information panoramic stations, plus a deliberate final stabilisation pass" is almost exactly the stop-and-scan architecture §6 recommends for us, arrived at from a different direction. Strong corroboration.)*

---

## 5. Termination — how a system decides a region is "done"

The survey is blunt: **when to stop performing active SLAM is an open challenge** (flagged since Cadena et al. 2016), most methods use **ad-hoc thresholds**, and resolving it remains *"urgent"* for practical deployment [src: placed-survey].

| Criterion | Form | Used by / notes |
|---|---|---|
| **Frontier exhaustion** | no candidate frontiers remain | `explore_lite`, `frontier_exploration_ros2` [src: explore-lite-src, fe-ros2-2025]. Simplest and most common; says nothing about quality |
| **Coverage threshold** | % of area known > T, or largest unexplored region < T% | Stachniss et al. [src: placed-survey]. "Often unrealistic to set a specific percentage of coverage as the termination point" [src: map-completeness] |
| **Map entropy threshold** | stop when map entropy < T, or when entropy stops decreasing while area stops growing | Widely used; the least upper bound of average map entropy under an independence assumption is a usable threshold [src: map-completeness] |
| **Minimum utility threshold** | stop when best candidate's utility < T | Papachristos et al. [src: placed-survey]. Also used *per-goal* as preemption [src: fe-ros2-2025] |
| **Uncertainty/covariance bound** | particle-cloud volume reduction; covariance/optimality-criterion bound | Early FastSLAM variants [src: placed-survey]; the natural home of the D-opt criterion of §4 |
| **Soft/hard occupancy thresholds** | soft → ignore invalid frontiers; hard → stop entirely | Two-tier scheme [src: map-completeness] |
| **Time limit** | wall-clock cap | Carrillo et al., Placed et al. [src: placed-survey] — i.e. the honest fallback |
| **Learned map-completeness estimator** | estimate P(map is complete) from map features, stop when confident | Autonomous Robots 2025; **saves >35% of total exploration time** by stopping when further exploration is not expected to add relevant detail [src: map-completeness] |

*(synthesis — what "sufficiently observed" should mean for us: **not** "every cell has been seen once". Our accuracy target is a crisp wall/floor plan, so the right per-region termination test is an **evidence-redundancy** test in the sense of [[robust-evidence-mapping-principle]]: has this wall segment been observed from **≥N sufficiently-different viewpoints**, do those observations **agree** to within our band tolerance, and is the residual spread stable? A region whose scans agree at 0.7 cm from three viewpoints is done; a region seen once at grazing incidence from 6 m is not, even though the occupancy grid marks it "known". This is not the literature's default criterion — the literature stops on *coverage*, we should stop on *agreement*.)*

---

## 6. Doing this well at low speed with no wheel odometry — our specific situation

### 6.1 Hard constraint: SLAM Toolbox needs an odom→base_link TF

*"Odom is currently required as an odom→base tf"* in `slam_toolbox`, and odometry is required for every ROS SLAM package **except Cartographer** [src: slam-toolbox-221]. Issue #221 ("Support mapping without odometry", opened 2020-07-09) is closed without the feature. The community workaround is a **laser odometry** node (`laser_scan_matcher`, `rf2o_laser_odometry`) publishing odom→base, with `slam_toolbox`'s own scan matcher then refining it into the pose graph [src: slam-toolbox-221]. Note `laser_scan_matcher` is unmaintained beyond ROS Kinetic.

So our options are: **(a)** `rf2o`/scan-matcher → `slam_toolbox`; **(b)** Cartographer, which runs odometry-free but is abandoned by Google (see [[2d-lidar-slam]]); **(c)** HectorSLAM, odometry-free by design but with **no loop closure** — unusable for an accuracy-first map. *(synthesis: (a) is the path, and it makes the exploration policy's job harder, because the *only* thing holding the pose together is scan geometry.)*

### 6.2 With scan-matching-only odometry, geometry choice *is* the odometry

2D LiDAR SLAM *"frequently encounters challenges related to motion degeneracy, particularly in geometrically similar environments"*; feature-scarce, repetitive environments such as long corridors *"lead to ambiguity in scan matching, resulting in potential inaccuracies in pose estimation"* [src: 2dliw]. The reference result for the fix is telling — 2DLIW-SLAM reaches RMSE 0.027 m *specifically because* it tightly couples **wheel odometry** into the front end, which is exactly the input we do not have [src: 2dliw].

This connects directly to a finding we already own: a scan seeing **one wall is laterally unobservable** and slides along it ([[weak-scan-registration-methods]]). **A frontier policy that drives the robot down the middle of a wall, or into a spot where only one flat surface is visible, is actively manufacturing unobservable poses.** *(synthesis: for us, the candidate-scoring function must include a **geometric-observability term** — prefer poses that see **two non-parallel surfaces** — not just information gain. This is a genuinely different utility term from anything in §3, and it matters more for us than mutual information does.)*

### 6.3 Move slowly is not enough — move *discretely*

Terrestrial-laser-scanning and mobile-mapping practice: **stop-and-scan** platforms *"must remain stationary during each acquisition, with dense scans aligned offline rather than registered incrementally in real time"*; when the sensor moves during acquisition, *"any base motion introduces distortion and registration error"*. Hybrid **"continuous stop-and-go"** systems exist explicitly to *"harvest the accuracy and stability of stop-and-go systems while maintaining speed from full-kinematic systems"*, capturing high-quality scans at stops and lower-quality data while moving [src: stop-and-scan].

*(synthesis — the important arithmetic for us: the RPLIDAR C1 spins at 10 Hz. A pure **rotation in place at 30°/s skews a single revolution by 3°**, which at 4 m range is a ~21 cm tangential smear — vastly larger than the ~0.7 cm band we are chasing. Translation at 0.2 m/s costs 2 cm per revolution. **Rotation, not translation, is the enemy**, and rotation is exactly what a frontier policy makes the robot do constantly. Note also `orientation_scale = 0.0` in `explore_lite` — the stock policy places **zero** penalty on heading change.)*

### 6.4 Consequence: the right architecture for us is a station graph, not a chase

*(synthesis)* Combining §6.1–6.3 and the SAE precedent (§4.4), the natural design for our rig is:

1. Plan a **discrete next station**, not a continuous frontier chase.
2. Drive there with the LiDAR treated as odometry-only (accept the smeared scans; do not insert them as map keyframes).
3. **Stop. Settle. Capture N full revolutions stationary.** These are the map-quality scans.
4. Score the next station on: information gain **+** geometric observability (≥2 non-parallel surfaces) **+** overlap with already-trusted scans (for seatability) **−** rotation cost **−** travel cost.
5. Periodically insert a **revisit** station at a previously-scanned, geometry-rich pose to close a loop, chosen by the D-opt/spanning-tree criterion (§4.2).
6. Finish with an explicit **global stabilisation pass** (SAE's "final stabilization strategy") before freezing the map.

This is slower than `explore_lite` by a large factor and better on every axis we care about. Speed is not in our mandate.

---

## 7. Practical implementations and what actually works indoors

| System | What it is | Reality check |
|---|---|---|
| **`explore_lite` / `m-explore-ros2`** | Greedy nearest-frontier, drives Nav2 | The de-facto default. Two-term cost, no uncertainty awareness, terminates on frontier exhaustion. Needs a seeded map (spin first) or it declares "all frontiers traversed" immediately [src: explore-lite-src, husarion-explore] |
| **`frontier_exploration_ros2`** (2025) | WFD + filtered decision map + MRTSP ordering + preemption, ROS 2 Jazzy/Nav2 | 99.9% coverage across maze/dense/open layouts; 28% shorter path than `m-explore` at 3× the CPU (7.4% vs 2.4%) [src: fe-ros2-2025] |
| **Nav2 itself** | Navigation stack | Ships **no** exploration behaviour. Every explorer is a third-party node issuing `NavigateToPose` goals. See [[ros2-nav2]] |
| **FUEL** | Incremental **frontier information structure** + 3-level hierarchy (global coverage tour → local viewpoint refinement → min-time trajectory) | The reference design for "maintain frontier state incrementally instead of re-detecting". UAV-oriented but the FIS idea transfers [src: fuel] |
| **TARE / DSVP** | Local-global exploration frameworks | TARE shows **backtracking**: rooms left unexplored, requiring a return trip. DSVP spends **>90% of runtime** on raycast gain evaluation [src: heros] |
| **Robot vacuums** | Systematic **coverage**, not exploration | Wall-follow the perimeter first, then **boustrophedon cellular decomposition** — sweep a slice, start a new cell when slice connectivity changes, cover each cell with back-and-forth zigzag [src: boustrophedon]; path lines aligned to the longest room wall to minimise turns. Persistent multi-session maps. See [[robot-vacuum-navigation]] |

*(synthesis: note the split. The **research** line optimises information; the **shipped-at-scale** line — vacuums — does deterministic geometric coverage with wall-following and persistent maps, and does not do information-theoretic exploration at all. For an accuracy-first single-room map, the vacuum answer — perimeter first, then interior, deterministically — is a serious baseline and probably beats greedy frontier chasing for us, because a wall-following perimeter pass is exactly the trajectory that keeps two non-parallel surfaces in view and keeps range short.)*

---

## 8. Doors and "transformable" objects in a 2D scan plane

Our mandate includes identifying door-like transformable objects. What 2D-LiDAR methods exist [src: door-laser]:

- **Gap detection on the raw scan**: check the distance between **consecutive** scan points; a candidate opening is flagged when that distance falls in a pre-defined range — **0.5–1.5 m** is the cited band for doorways. An **open** doorway is confirmed when the region beyond the boundary contains **no points, or very few** (sensor noise only).
- **Door leaf as a line segment**: door candidates appear as clusters forming relatively straight lines of a specified length, **assuming the door is not flush with the wall** — an open or ajar leaf protrudes from the wall plane.
- **Occupancy-grid method**: extract a small local grid, detect **gaps between parallel lines** via edge detection + Hough transform; a 2D occupancy grid "improves significantly the door detection and segmentation" and supports adding topological structure to the grid [src: door-laser].

*(synthesis, and this is the interesting part for our principle: a door is **detectable as a discrepancy between visits**. If a wall segment reads "occupied" on pass 1 and "free, with a leaf segment protruding 0.8 m into the room" on pass 2, the correct inference is not "noise" and not "moved furniture" — it is a **hinged transformable**. Under the human's principle, exploration should therefore deliberately **re-observe candidate gaps** rather than accept the first reading. That makes door detection an *active* task with its own information-gain term, and it is a use of the revisit machinery in §4.3 for a semantic rather than a metric purpose. At our 1.1 m scan plane both jambs and the leaf are in-plane, so this is directly available — see [[dynamic-object-handling]] and [[drone-contact-and-door-tasks]].)*

---

## 9. Synthesis — what to build, in order

*(synthesis — the whole of this section is a project recommendation, not a citation.)*

**Mapping the human's principle onto the literature:**

| Human's phrase | Literature construct | Where |
|---|---|---|
| "select data that aligns well with priors" | scan-to-map registration gating; observability-aware candidate scoring | §6.2, [[weak-scan-registration-methods]] |
| "discovers discrepancies" | prediction-vs-measurement residual; beyond-line-of-sight map prediction | §3.4 |
| "identify where information is LACKING" | frontier detection + map entropy + **pose-graph D-optimality** | §2, §3, §4.2 |
| "determine what information needs to be gathered" | utility function over candidate goals (gain − cost − uncertainty) | §1 stage 2, §4.3 |
| "improves uncertainty / update priors" | joint entropy reduction; loop closure; final global stabilisation | §4.4 |
| *(implicit)* "know when you're done" | **open problem** — everyone uses ad-hoc thresholds | §5 |

**Recommended ladder for our rig:**

- **A — Deterministic perimeter + interior stations (do this first).** Wall-follow the room perimeter at fixed spacing with stop-and-scan stations, then a coarse interior grid of stations. No frontier logic at all. This is the vacuum answer (§7), it maximises two-surface visibility, and it gives a clean, reproducible baseline map to measure everything else against. Terminate on the station list being exhausted, plus the agreement test below.
- **B — Frontier layer on top.** Add NaiveAA/WFD-INC frontier detection on the 5 cm grid to find what the fixed station set missed (pockets behind furniture). Reuse `explore_lite`'s cost form but **re-weight it**: raise `orientation_scale` off 0.0 (rotation is our dominant error source, §6.3), drop `min_frontier_size` toward ~0.4 m for a single room, and re-tune `potential_scale`/`gain_scale` away from the 3.0/1.0 nearest-first bias.
- **C — Observability + information gain term.** Add level-1 raycast gain (affordable at our map size, §3.2) and a hard **≥2 non-parallel surfaces** term. This is the single highest-value custom term for a no-odometry rig and it does not exist in any off-the-shelf package.
- **D — Uncertainty-driven revisit.** Add revisit candidates to the same list, scored by the **spanning-tree / D-optimality** Laplacian criterion (§4.2). Cheap, principled, monotonic, and it is the only thing in the literature that actually answers "should I go somewhere new or go re-close a loop?".
- **E — Termination on agreement, not coverage.** Per-wall-segment: ≥N viewpoints, spread of independent observations within band tolerance, residual stable. Plus a final global stabilisation pass before freezing.

**What would be naive:** dropping in `explore_lite` + `slam_toolbox` and calling the resulting map an anchor map. That stack (i) requires an odometry source we do not have, (ii) has zero pose-uncertainty awareness, (iii) has zero rotation penalty on a rig where rotation is the dominant distortion, (iv) terminates on frontier exhaustion, which is a coverage test and not an accuracy test, and (v) will happily park the robot facing a single flat wall, which is the one geometry that makes scan-matching-only localisation unobservable.
