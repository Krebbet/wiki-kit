# Door and Aperture Detection

A **transformable opening** is a place where the world's geometry is allowed to change state: a doorway whose leaf can be open, ajar or closed; a cased archway that is permanently open; a curtain; a movable screen. Detecting these is a different problem from mapping walls and obstacles, because the thing to be recorded is not a surface but a *hypothesis about a surface that may or may not be there next time*. This page collects the geometry, the sensing, and the map-representation literature for finding them from a mobile robot — with the emphasis on the specific case that blocks this project: a single-plane 2D LiDAR at ~1.1 m, plus a stereo camera, mapping one room.

The blocker is precise. Our mapping stack sees a run of missing returns along a wall line and cannot tell whether it is *an aperture* (a real passage, free space continues beyond it) or *a wall region the sensor never got a look at* (occlusion, grazing incidence, absorbing surface). Both look identical in an occupancy grid: unknown cells bounded by wall. Because it cannot tell, it refuses to treat the gap as traversable and never explores through it. The literature has a clean answer — **ray termination beyond the wall plane** — and it is cheap to implement (see [The occlusion-vs-aperture test](#the-occlusion-vs-aperture-test-the-core-discriminator)).

## Source

- `10.3390/s23115247` — Müller, Müller, Ahmed, Gross, "Laser-Based Door Localization for Autonomous Mobile Service Robots", *Sensors* 23(11):5247, 2023 (TU Ilmenau; LaserDoors dataset)
- `10.3390/rs10111754` — Nikoohemat, Peter, Oude Elberink, Vosselman, "Semantic Interpretation of Mobile Laser Scanner Point Clouds in Indoor Scenes Using Trajectories", *Remote Sensing* 10(11):1754, 2018
- `10.3390/rs10111815` — Elseicy, Nikoohemat, Peter, Oude Elberink, "Space Subdivision of Indoor Mobile Laser Scanning Data Based on the Scanner Trajectory", *Remote Sensing* 10(11):1815, 2018
- `arXiv:2103.11491` — Xu, Feng, Vela, "Potential Gap: Using Reactive Policies to Guarantee Safe Navigation", RA-L 2021 (radial vs swept gaps)
- `arXiv:2210.05022` — Asselmeier et al., "Dynamic Gap: Safe Gap-based Navigation in Dynamic Environments", 2022
- Mozos, Stachniss, Burgard, "Supervised Learning of Places from Range Data using AdaBoost", ICRA 2005
- Adán & Huber, "3D Reconstruction of Interior Wall Surfaces under Occlusion and Clutter", 3DIMPVT 2011
- Antonazzi, Luperto, Basilico, Borghese, "Development and Adaptation of Robotic Vision in the Real World: The Challenge of Door Detection", *Journal of Field Robotics*, 2025 — `arXiv:2401.17996` (and `arXiv:2203.03959`)
- Tibebu, Roche, De Silva, Kondoz, "LiDAR-Based Glass Detection for Improved Occupancy Grid Mapping", *Sensors* 21(7):2263, 2021
- Krajník, Fentanes, Santos, Duckett, "FreMEn: Frequency Map Enhancement for Long-Term Mobile Robot Autonomy in Changing Environments", *IEEE T-RO* 33(4), 2017
- Bormann, Jordan, Li, Hampp, Hägele, "Room Segmentation: Survey, Implementation, and Analysis", ICRA 2016
- **Full citation-key table at the foot of this page** — every `[src: key]` below resolves there.

## Related

[[drone-contact-and-door-tasks]] · [[semantic-object-memory]] · [[indoor-cluttered-slam]] · [[dynamic-object-handling]] · [[room-segmentation-floor-plan]] · [[floorplan-reconstruction-methods]] · [[2d-lidar-slam]] · [[robust-evidence-mapping-principle]] · [[sensor-weaknesses-and-fixes]] · [[map-then-navigate]] · [[room-shape-topology-methods]] · [[scene-graph-world-model]]

---

## The geometric signatures in a 2D scan

A single horizontal scan sees a doorway as a **range discontinuity pair** — two jump edges of the right separation, with something (or nothing) between them. The literature converges on four cues, all cheap:

| Cue | Definition | Typical threshold | Notes |
|---|---|---|---|
| **Jump edge / range discontinuity** | \|L(i+1) − L(i)\| > τ between consecutive beams | τ = 2·r_ins, twice the robot's inscribed radius [src: potential-gap] | Marks a gap *boundary*. Two of them bracket a candidate aperture. |
| **Max-range run** | A contiguous interval I where L(j) = d_max for all j ∈ I, with Cartesian endpoint separation > 2·r_ins [src: potential-gap] | same | The scan "sees out" — nothing returned within range. Strong aperture evidence in a small room; weak in a large one. |
| **Aperture width** | Cartesian distance between the two jump-edge endpoints | 0.735–1.110 m as a weak classifier band [src: rule-based-door-laser]; d_max = 1.10 m as a hard upper bound [src: rule-based-door-laser] | Residential interior doors are ~0.76–0.91 m leaf; the *clear opening* is a few cm less than the frame. |
| **Depth of gap / recess** | How far behind the wall line the returns beyond the gap fall | door leaf thickness ~35–45 mm; frame reveal = wall thickness | Distinguishes a doorway (deep, continues) from a shallow niche or a picture recess. |

**Doorways are the hardest place class to recognise from a single scan.** Mozos, Stachniss and Burgard boosted nine single-valued, rotation-invariant scan features (mean and s.d. of consecutive-beam differences, mean and s.d. of beam length, **number of gaps at several difference thresholds**, number of beams lying on extracted lines, distance and angular separation of the two smallest local minima) plus a second polygonal feature set, into an AdaBoost place classifier over {room, corridor, doorway, hallway} [src: mozos-adaboost-2005]. Overall recognition >89%, and 93.94% on the three-class Freiburg building-79 test using the `room→doorway` decision list — but every decision list that put the **doorway classifier first** collapsed to ~80%: `doorway-corridor` 80.68%, `doorway-room` 80.49%, `corridor-doorway` 80.10% [src: mozos-adaboost-2005]. The reason is structural, not a tuning failure: a scan taken *in* a doorway looks like a room from one half and a corridor from the other, so doorway is the class that must be decided last, after the confident classes have been peeled off. Later work makes the same complaint — doorway locations "occur between rooms and corridors with laser scan features resembling both" and are typically handled by a *separate* doorway routine bolted onto the place classifier [src: 2dlasernet].

The two smallest local minima (features 8 and 9 above) are worth calling out on their own: **in a doorway they are the two door jambs**, and their Euclidean separation is directly the aperture width. That is the cheapest single door feature in the whole literature.

### Gap taxonomy: swept vs radial — and why it maps onto our problem

Potential Gap gives the cleanest formalisation of "a gap" from a 360° scan, and it happens to encode exactly the ambiguity we care about [src: potential-gap]. Detection has two triggers:

1. a large interval of `d_max` readings whose Cartesian endpoints are more than 2·r_ins apart;
2. an instantaneous range change |L(i+1) − L(i)| > 2·r_ins.

Gaps found by trigger (2) are **automatically radial**. The rest are classified by the dominant direction of the chord between the two gap sides. The distinction is about *visibility*, not width:

- **Swept gaps** subtend a large angular sweep and "face" the robot. They "provide information both about passage **to** the gap, as well as **through** the gap" [src: potential-gap].
- **Radial gaps** have large range variation over little angular difference — they are oriented sideways to the robot, and have **bad line-of-sight visibility properties**; the follow-on work notes that radial gaps "can cause safety risks due to their low visibility beyond the gap arc" [src: dynamic-gap].

*(synthesis)* Read that as a direct statement of our blocker: **a radial gap is a gap you are looking at edge-on, and edge-on you cannot see what is behind it.** A doorway observed from a grazing angle *is* a radial gap and is genuinely indistinguishable from an occlusion shadow at that viewpoint. Potential Gap's answer is to *convert* radial gaps to swept gaps by pivoting the representation about the nearer gap point and merging [src: potential-gap]; ours should be to **go and look at it face-on**, because a swept gap of the right width, with returns beyond it, is an aperture and nothing else. This is a viewpoint-selection problem before it is a classification problem.

### Door keypoints: hinge, lock point and opening angle

For a robot that must *act* on the door, the state of the art in 2D-laser door modelling is Müller et al.'s LaserDoors work [src: laserdoors-2023]. The door model is three keypoints in the horizontal scan — **hinge point**, **lock point** (the frame side opposite the hinge), and **corner point** (the free end of the visible door panel). The opening angle falls out of comparing the fitted door-panel line to the hinge→lock baseline; no separate estimator is needed.

Their heuristic method, viewed from outside: RANSAC the longest line (the panel), find orthogonal frame lines left and right, intersect to get hinge and lock; once the door is opened far enough, the panel's endpoint back-solves the hinge. Viewed from inside with the door closed and flush with the wall, the panel line is the wall line, so they instead take perpendicular point-to-line residuals, estimate the noise variance, and call the **first point outside μ ± 3σ** the hinge — a 4 mm frame-to-leaf gap is enough to trip it [src: laserdoors-2023].

| Method | Mean keypoint error | Notes |
|---|---|---|
| Heuristic RANSAC line-fit | **4.0 cm** (3.4 cm for closed/unlatched) | Outside views 3.86 cm, inside 4.17 cm |
| DoorPointNet (PointNet on 144 2D points) | **2.0 cm** | Best, with door width/depth/side fed in as side-channel features |
| 1D-CNN, supervised (150-bin range histogram) | **2.0 cm** | Comparable to DoorPointNet |
| 1D-CNN, unsupervised (two-view consistency) | **5.0 cm** | Outside 3.3 cm, inside 5.1 cm |

All numbers from [src: laserdoors-2023]. Read them with three caveats the authors state plainly:

- **The door location is assumed known.** "Usually, mapping takes place at the beginning, where doors … can be registered in a database"; at runtime the robot's localisation supplies a coarse pose with deviation limited to **±10 cm and ±10°**, and the algorithm only *refines*. This is door **localisation**, not door **discovery**.
- **The learned methods do not transfer across sensors.** Networks trained on a SICK S300 at 0.5° angular resolution could not handle a SICK TIM571 at 0.33° without retraining.
- **Fully-open doors are the failure case for the heuristic**: at large opening angles the panel points run nearly parallel to the line of sight, endpoint detection fails, and "large displacements occur more often".
- Dataset: **LaserDoors**, 1,250 raw samples from 20 doors (public buildings and private homes), each door recorded from both sides at three lateral positions across four opening states (closed, unlatched, partly open, fully open), 30 scans averaged per sample; augmented to 100k samples by jittering the virtual scanner ±20 cm / ±10°, varying angular resolution, and adding Gaussian noise. Publicly available for academic use. Kinect Azure RGB-D frames are included but were not used in the evaluation. [src: laserdoors-2023]

---

## The occlusion-vs-aperture test (the core discriminator)

This is the section that answers our blocker, and the answer is not in the 2D SLAM literature — it is in the **indoor 3D reconstruction** literature, which has had to separate "hole in the wall because there is a door" from "hole in the wall because a filing cabinet was in the way" for fifteen years.

### The formalisation

Adán & Huber set the pattern: identify candidate planar surfaces, **label the occluded regions of each surface**, detect openings by supervised learning, then inpaint the occluded regions [src: adan-huber-2011]. The key move is that occlusion is labelled *first and explicitly*, as its own class, rather than being lumped in with "no data". Their known weakness is the mirror image of ours: only the **open** parts of doors and windows were found; **closed** door leaves were labelled as wall.

Nikoohemat et al. make the test explicit and cheap, and it is the version to copy [src: nikoohemat-2018]. For each wall, voxelise the wall surface (they use **10 cm** voxels) and cast a ray from **each scanner trajectory position** to **each point it measured at that timestamp** — the timestamp pairing matters, "from every point on the trajectory only the measured points at that specific time are evaluated". Every wall voxel then gets exactly one of four labels:

| Label | Ray-geometry condition | Meaning |
|---|---|---|
| **Occupied** | the measured point lies *on* the wall surface | wall, confirmed |
| **Occluded** | the measured point lies *in front of* the wall surface | something blocked the view; the wall behind is **unknown** |
| **Open** | the measured point lies *behind* the wall surface | the beam went **through** — an aperture |
| **Unknown** | no ray intersects this voxel at all | never looked at |

The one-line statement of the discriminator: *"a laser beam, crossing a wall surface with the opening, hits the objects behind the surface"*, whereas occlusion leaves no measured points beyond the wall boundary [src: nikoohemat-2018].

**This is the test.** "Free space beyond" is not measured as free space — it is measured as **a return that terminated on the far side of the wall plane**. A negative-information / free-space-carving formulation says the same thing in occupancy-grid terms: cells along a beam before the hit are carved free, cells beyond the hit are left *unknown*, because the beam never reached them [src: ism-standard]. So a wall region the sensor never observed accumulates **Unknown** or **Occluded** voxels and no through-rays; a real aperture accumulates **Open** voxels with through-rays whose endpoints are metres past the wall plane. The two are not confusable once you keep the ray, and only the ray-terminus test separates them — a gap width test alone will not.

### The supporting priors and thresholds

Nikoohemat's pipeline wraps that test in filters worth stealing wholesale [src: nikoohemat-2018]:

| Filter | Value | Purpose |
|---|---|---|
| Wall voxel grid | 10 cm | opening-detection resolution |
| False-opening rejection | require **≥80%** of the candidate region's voxels labelled *open* | kills clutter-induced holes |
| Door centre height band | 0.8–1.10 m above floor | where a door's clear opening reliably is |
| Door frame top band | 1.80–2.10 m | finds the lintel |
| Open-door confirmation | **≥70%** empty voxels in the neighbourhood | confirms the leaf is not in the opening |

Reported: **80% of doors and >85% of rooms correctly detected** across four mobile-laser-scanner datasets, seven storeys [src: nikoohemat-2018, elseicy-2018].

Note the door centre band, **0.8–1.10 m** — our RPLIDAR C1 sits at ~1.1 m, at the very top of it. That is a lucky coincidence, not a design: a 2D scan at 1.1 m cuts the door aperture at close to its widest and above most floor clutter, which is the best single height available for this test.

### The trajectory prior: a door is where you walked through a wall

The second, almost embarrassingly simple discriminator: **the sensor's own trajectory is a certificate of traversability.** Elseicy et al. use the scanner trajectory jointly with the point cloud to subdivide indoor space into storeys, staircases, doorways and rooms — "the doors that are traversed by the operator during the scanning are identified by processing only the interesting spots of the point cloud with the help of the trajectory", after which space labels propagate from the annotated trajectory to the full cloud [src: elseicy-2018].

*(synthesis)* If the robot (or the human carrying the rig) passed through a gap in a wall line, that gap is an aperture, with certainty, at the width of the passage plus the robot's footprint. This is free, retrospective, and requires no new capture — and for a capture that entered the room through the door, it labels at least one aperture with no ambiguity at all. It is the highest-confidence door evidence available to us and we are not using it.

Its limits are equally clear: it only ever finds doors you **went through**. A door you never used, or a closed door, is invisible to it [src: nikoohemat-2018].

---

## Representing a thing that changes state

There are three separate representational stances in the literature, and they are almost never combined. Naming them is the fastest way to see the hole.

| Stance | Examples | What it gets right | What it cannot do |
|---|---|---|---|
| **(a) Door as derived topology** — never stored, re-derived from geometry each run | Voronoi critical points [src: thrun-1998], room-segmentation survey [src: bormann-2016], Hydra [src: hydra-2022], S-Graphs 2.0 [src: sgraphs2-2025] | Cheap; gives a room graph for free | No door entity, no state. A run with the door open and a run with it shut produce **different room graphs**, and nothing records why |
| **(b) State in the cell** — occupancy cells that model their own dynamics | iMac [src: imac-2012], HMM lifelong localisation [src: tipaldi-2013], FreMEn [src: fremen-2017] | Handles door dynamics beautifully and is statistically principled | Has no notion of "door" — it learns that *some cells flicker*, not that a doorway exists |
| **(c) State on the object** — the door is a thing with an articulation model | Kinematic graphs [src: sturm-2011], OPD [src: opd-2022], MoMa-LLM [src: momallm-2024] | Knows a door is a 1-DOF revolute object whose geometry is *expected* to change | Needs the door to be detected and recognised as an object first |

*(synthesis)* The unoccupied slot is a **door node that carries both an articulation prior and a temporal state model, wired in as the edge that gates the room graph** — (a) ∪ (b) ∪ (c). For a one-room prototype we need only the skeleton of that: an aperture entity, on a wall, with a state field and a confidence, that navigation reads.

### (a) Doors as derived topology

The origin is Thrun's metric-topological mapping [src: thrun-1998]: take the Voronoi diagram of free space, find **critical points** (local minima of clearance), draw **critical lines** through them, and the resulting partition maps isomorphically to a graph — regions become nodes, critical lines become arcs. Narrow passages *are* the critical lines, so "door = edge between rooms" falls out. Bormann et al.'s room-segmentation survey implements and compares four families of this idea (morphological, distance-transform, Voronoi-graph, feature-based); **every one of them is parameterised by an assumed doorway width**, and runtimes are 1–2 s (morphological / DT) to ~13 s (Voronoi) [src: bormann-2016]. See [[room-segmentation-floor-plan]] and [[room-shape-topology-methods]].

Hydra does the same in 3D: places come from the GVD sparsified out of the ESDF, and rooms come from **pruning place nodes whose obstacle distance falls below a dilation threshold** — the stated insight being that "inflating obstacles causes small openings like doors to close" [src: hydra-2022]. Elegant, and it means a closed door and an open door yield different maps with no trace. S-Graphs 2.0's four layers (keyframes / walls / rooms / floors) likewise have no door entity [src: sgraphs2-2025]. Outside robotics, OGC **IndoorGML** does give doors a name — `CellSpaceBoundary` plus a `Transition`, dualised into a node-relation graph for routing — but it is a static schema with no state attribute [src: indoorgml].

### (b) State in the cell

- **iMac** (independent Markov chain occupancy grid): each cell is a two-state Markov chain whose entry and exit are **two Poisson processes** with rates learned online under recency weighting; the cell stores expected occupancy *and* expected dynamics, so a doorway cell has high transition rates and a wall cell ~0 [src: imac-2012]. Validated on production laser-guided-vehicle logs.
- **Lifelong localisation in changing environments**: a Rao-Blackwellized particle filter coupled to a per-cell **HMM** over a dynamic occupancy grid, exploiting the HMM's stationary distribution and **state holding time** [src: tipaldi-2013]. Holding time is literally the "how long does this door stay shut" parameter.
- **FreMEn** is the most on-point paper in this whole section, because **its canonical worked example is a door** [src: fremen-2017]. Binary states (door open/closed, room vacant/occupied, landmark visible/occluded) are modelled by their **frequency spectra**: an order-1 model already captures "open in the afternoon, not at night"; ~3 more spectral components capture weekly periodicity. Compression up to **1:100,000**, experiments over months to years, with measured gains in localisation robustness, path planning, and object search.
- **Temporary maps** keep a static reference map for pose tracking while a temporary local map absorbs observations from unexpected objects [src: meyerdelius-2010].

### (c) State on the object

Sturm, Stachniss and Burgard's kinematic-graph framework is the formal version of the prior *"this is a door; a 1-DOF revolute change in its geometry is expected, not a map error"* — objects (doors, cabinets, dishwashers, fridges) are graphs whose vertices are parts and whose edges are kinematic relations, with parametric (revolute / prismatic / rigid) and non-parametric edge models estimated from noisy pose observations, plus model selection and generalisation to unseen objects [src: sturm-2011]. **OPD** predicts openable parts plus **motion type, axis and origin** from a single image, with OPDSynth/OPDReal datasets [src: opd-2022].

**MoMa-LLM** is the strongest demonstrated stateful-door system [src: momallm-2024]: its dynamic scene graph carries an explicit `opened`/`closed` attribute; detected door positions cut the Voronoi graph via a **mixture of Gaussians over observed door locations**, splitting the navigation graph into room components; when a door opens, the occupancy map updates and the Voronoi + room segmentation are **recomputed** at the next reasoning step. Reported 97.7% success / 87.2 AUC-E over 7 iGibson scenes × 25 episodes, and **80% over 10 episodes** in a real 4-room apartment. Closest 2D-SLAM analogue is Passage-Aware Structural Mapping, which models doors as **planar entities embedded within walls**, classified traversable / non-traversable from traversal evidence plus geometric opening validation — but it is a short paper with qualitative office sequences only and no dynamic state [src: passage-aware-2026].

Perception-side door-state classifiers exist and are cheap: an occupancy-grid CNN that recognises **closed doors, open corridors and intersections** from bitmap patches [src: nikdel-2019], and a real-time **open / closed / semi-open** 2D+3D classifier benchmarked on a Jetson Nano across PointNet, FastFCN, FC-HarDNet, SegNet, BiSeNet, DetectNet, AlexNet and GoogLeNet, with a RealSense D435 dataset released [src: ramoa-2021].

---

## What happens when the door closes

Practically, in ROS 2 Nav2: the **static layer is populated only from the `/map` topic and is never updated from live sensor data**; only the obstacle / voxel layers mark and clear from `/scan` by raytracing [src: nav2-costmap]. So a newly-closed door remains **free space to the global planner from anywhere outside sensor range**, turns lethal only on approach, and is discovered as a replan/recovery loop rather than as a map fact. The failure is bidirectional and well attested in the tracker: obstacles that never clear, obstacles cleared too eagerly when reversing, and frequent "Navigation failed" [src: nav2-issues].

Commercial floor robots **do not model door state at all — they push it onto the user.** iRobot and Roborock both instruct the owner to open every door to every area they might ever want cleaned *before* the mapping run; a room lost behind a closed door requires a full re-scan, not an incremental patch [src: roborock-support]. See [[consumer-robot-vacuum-mapping]] and [[robot-vacuum-navigation]].

iRobot's own research map is instructive about how a shipping product dodges the problem [src: irobot-lifelong-2020]. The semantic map is **walls, dividers, rooms, clutter, occupancy pixels** — doors are *not* entities; they are a constraint ("dividers must be attached to a wall") and are stood in for by **dividers**. The paper explicitly names "opening and closing of doors" as a cause of room-shape drift, and fixes it by *re-placing dividers*, not by modelling state. Cross-mission semantic transfer error over **25 robots / 425 missions** in real homes: **20.92% baseline → 11.06%** with meta-occupancy → **1.41%** with meta-dividers.

That the prior matters for *decisions*, not just bookkeeping, is shown concretely in belief-space path-tree optimisation: at an **80% prior probability that a door is open** the optimal policy attempts the direct route with branch points at each door observation; at **50%** it takes the longer certain route [src: belief-pathtree-2022].

---

## Other transformable structures

Furniture is handled by class, not by transformation. The working taxonomy across the change-detection literature is **semi-static** (present but relocatable — chairs, boxes) versus **clutter / movable** (filtered out entirely). Representative machinery:

- **POCD** — per-object state jointly modelling a **stationarity score** and a TSDF change measure, Bayesian-updated from geometric and semantic evidence; high-stationarity objects regenerate the map, low-score objects are discarded [src: pocd-2022].
- **OASIS-Map** — dense patch-level semantic correspondences for appeared / disappeared / moved objects; F1 **0.783** on car-park object replacement, **0.667** on 3RScan moved-object association [src: oasis-map].
- Feature-based lifelong mapping in semi-static environments [src: rosen-lifelong] and detection/tracking of general movable objects in large 3D maps [src: ambrus-2017]. See [[dynamic-object-handling]].

**Curtains, blinds, folding screens and shower curtains are a genuine gap.** No work was found that treats a deformable transformable structure as a map element; curtains appear in the literature only as a vacuum-entrapment and map-distortion nuisance [src: dreame-support]. For our purposes a curtain across an opening is the worst case of all: it is a soft, moving, partially-transmissive surface at exactly LiDAR height that gives inconsistent returns run to run, and it will fail the ray-terminus test intermittently rather than cleanly.

---

## Door detection from vision

Vision is the complement to the LiDAR test: it cannot certify that a passage exists (no depth-beyond guarantee from a bounding box), but it *can* tell a doorway from a wall gap, read the door's **state**, and confirm identity — which is precisely the gate our own working knowledge already demands before labelling any LiDAR cluster.

### Classical / geometric

| Work | Cue set | Reported result | Caveat |
|---|---|---|---|
| Chen & Birchfield, CVPR-W 2008 [src: chen-birchfield-2008] | Canny → length-adaptive line segmentation → vertical pairs, **concavity** (a slim "U" plus a recession test of 2–10 px between the extended wall/floor line and the door bottom), bottom-edge intensity profile, colour/texture; AdaBoost | **90% detection at 0.05 FP/image** on 309 images from **20 buildings**; live corridor run **97.7% detection, 0.008 FP per metre driven** | Fails on dark doors **flush with the wall** (no concavity), and on distracting horizontal edges |
| Murillo et al., RAS 2008 [src: murillo-2008] | Probabilistic shape (4 corners, aspect ratio, reference λ_r = 0.4 frontal) × Lab-colour appearance; vanishing-point-grouped lines → Harris corners → 4-corner hypotheses; learned from **10** labelled images | 76 doors: **88% found, 100% of frontal views**, 79% pixel-level OK — but **39% false-positive pixels** | FP rate driven by images with no door at all; fails on small/far/occluded doors |
| Yang & Tian, CVPRW 2010 [src: yang-tian-2010] | Deliberately appearance-free: generic geometric model from edges + corners plus side-constraints to reject bookshelves/cabinets/elevators | **91.9% detection at 2.9% FP** (author-reported) | Test-set size not verifiable in an open copy |
| Hensler, Blaich, Bittel, Eurobot 2009 [src: hensler-2009] | **Seven** weak classifiers fused by AdaBoost — door width (from laser, bounded **0.735–1.2 m**), concavity (laser), bottom texture, colour-vs-wall, door gap, knob, frame | AdaBoost **recall 0.721, precision 0.917, F 0.807**; >90% of doors on a moving robot. Per-classifier: knob 0.90 recall / 0.51 precision, width 0.90 / 0.32, **colour-vs-wall 0.066 recall — useless alone** | Named failure: **glass doors** (laser passes through), plus wall patches that fire width+gap+texture+knob together |

*(synthesis)* Two things carry over to us. First, **door width from the laser is the highest-recall single cue and the lowest-precision one** (0.90/0.32) — exactly our situation, and exactly why it must be fused rather than trusted. Second, the **concavity/recession cue is the strongest purely-visual door signal**, and it is a depth cue in disguise: the leaf is inset from the wall face. Our stereo pair at ~1.0 m can measure that inset directly instead of inferring it from a 2–10 px image offset.

### Learned detectors and datasets

| Dataset / model | Size | Result | Notes |
|---|---|---|---|
| **DoorDetect** + YOLO [src: arduengo-2021] | 1213 Open Images, 4 classes (handle / door / cabinet door / refrigerator door), 1013 train / 200 test | **mAP 45%** (vs YOLO-COCO 55%), 6 fps on a GTX 1080 | Authors are honest that this is ~10 points below general detection |
| **DeepDoors2** [src: ramoa-2021] | 3000 RGB + 3000 aligned depth (RealSense D435), 1000 each **open / closed / semi-open**, 2400/300/300 | State classification **AlexNet 98.33%** at 227×227 (55 FPS) — but only **56.67%** at 480×640 input. Detection: BiSeNet 38/40 TP with 4/40 FP (2 FPS); DetectNet 28/40 TP, 10/40 FP (**7 FPS on a Jetson Nano**); SegNet degenerate (always "door") | **The 3D route lost badly**: PointNet state classification 0.494/0.433 accuracy vs the 2D pipeline's 0.983 |
| Door-handle RGB-D regression [src: handle-scirep-2024] | 5000 annotated handle images (D435) | On a **handle absent from training**: **1.5 cm position error, 5° from the door normal**, 16 FPS / 16 MB | Predecessor line reports 95% success over 100 door-opening attempts, 1.98 mm knob error — but requires a specific camera-to-handle angle |

### The number that matters: cross-building generalisation

Antonazzi, Luperto, Basilico and Borghese quantify the gap everyone else elides [src: antonazzi-2022, antonazzi-jfr-2025]. A DETR **trained on DeepDoors2** and tested on four **real robot deployments** scores **AP 5 (closed) / 18 (open)**. The same architecture trained on ~5500 images of a **simulated robot's-eye view** (Gibson + Matterport3D, cameras at 0.1 m and 0.7 m, poses sampled on a Voronoi navigation graph) scores **13 / 31** — *simulated-from-the-robot's-viewpoint beats real-from-a-human-viewpoint*, because viewpoint distribution matters more than photorealism. **Fine-tuning on target-environment data lifts it to 53/55 → 65/70 → 72/78** for 25 / 50 / 75% qualification data, with the **largest gain from the first and smallest** qualification round. Per-environment mAP for general detectors sits in the **0–30** range.

They also argue mAP is the wrong metric for a robot and add **TP% / FP% / BFD%** (background false detections), on the grounds that a geometrically sloppy but semantically right box costs a robot nothing, whereas a confidently *wrong door status* costs it a replan.

*(synthesis)* The operational reading for us is blunt: **do not expect an off-the-shelf door detector to work in our kitchen.** Published headline numbers (90–98%) are in-domain; the honest out-of-the-box figure for a new building is AP ~5–30. But the same work says a **small** amount of target-environment fine-tuning recovers most of it — and we have exactly that: a densely-captured single room with a locked map. If we ever need a learned detector, the plan is a handful of labelled frames from our own capture, not a general model.

### RGB-D / stereo-specific, and door state

- **Arduengo's RGB-D door model** [src: arduengo-2021]: CNN ROI → voxel downsample + statistical outlier removal → **RANSAC plane fit** for the door plane normal; a *second* RANSAC inside the handle ROI splits door-plane inliers from handle outliers, handle position = outlier centroid, orientation from bbox aspect ratio. Articulation is then a Bayesian posterior over **revolute vs prismatic**; grasp-and-open succeeded **26/30 (87%)** with no prior knowledge.
- **Quintana et al.** is the closest thing to a gold standard for aperture detection in 3D and is the only method that classifies **door state implicitly, from the opening angle** [src: quintana-2016]. On a labelled voxel space (20 cm voxels) per wall plane it builds a binary data/no-data image of the wall, fuses colour and depth edge images, extracts vertical/horizontal lines, enumerates rectangles, and keeps those sitting on the floor with door-like dimensions. Simulated 5-room scene (6 doors, 9 windows, 27×21 m, mean wall occlusion 14%): **all doors found, precision 0.979 / recall 0.949, F₁ 0.988**. Real robot in an 8×34 m hall: **18/18 doors, mean precision 0.9948, recall ≈0.97**, still working at **38–39% wall occlusion**. Caveats: 35 point clouds from essentially one building, offline, and the state classification assumes **the sensor is in front of the door**.
- **Vision + 2D laser fusion for door pose** [src: arw-2022]: YOLO door bbox → back-project the bbox left/right edges as rays → keep the laser points inside the ray fan → fit the door line. Detector mAP@0.5 = 90.1% (in-domain). Line fit over 20 real doors, summed |x|+|y|+|θ| error: **naive 0.3212 ± 0.1774, least-squares 0.1167 ± 0.0667, RANSAC 0.0311 ± 0.0062** — RANSAC is a **10×** improvement and statistically significant. Continuously re-estimating the goal pose while driving beat one-shot estimation. *This is the cheapest published recipe for exactly our sensor pair.*
- **Floor-plane-anchored hypotheses** [src: rgbd-fisheye-2024]: RANSAC floor plane from depth, propagated into a fisheye image to extend free space; door hypotheses from vertical lines standing on the segmented floor, verified by a **cross-ratio** recovering true door height against a 2.00 m prior, which rejects windows and frames. Tuned to **zero false positives**, so they report coverage only: two-line hypotheses 56.67% / 86.67% (2.07 s), one-line 95% / ~40% (6.90 s). The trade is instructive — the geometric hypothesis stage gets good coverage or good precision, rarely both.

### Opening angle and hinge side

Thin literature, three concrete sources. Quintana derives state from the **shape of the gap** in the wall plane [src: quintana-2016]. Arduengo does not measure the angle at all but *infers the articulation* by Bayesian model selection over revolute vs prismatic while pulling [src: arduengo-2021]. The most explicit algorithm is Calvert's [src: calvert-2026]: two persistent YOLOv8 detections (opening mechanism, door panel) with depth attached; the **vector between mechanism centroid and panel centroid defines panel orientation** under a vertical-hinge assumption; a nominal hinge is placed at a fixed offset along the panel width, and a **vertical 3D capsule is swept around candidate angles**, counting contained points on GPU, to find the latch-side frame post. Hinge side comes from the panel frame relative to the viewpoint; **the sign of the opening angle relative to the hinge side gives push vs pull**, and for a closed door a second capsule depth-check looks for a **panel recess** — recess present → push side, absent → pull side.

*(synthesis)* Note the convergence: Chen & Birchfield's 2008 monocular **concavity/recession** cue and Calvert's 2026 depth **recess capsule** are the same physical fact — *the leaf is inset on the push side* — measured eighteen years apart, once in pixels and once in depth. If we only ever implement one visual door cue, it should be that one.

---

## Practical failure modes

### Glass and mirrors

A LiDAR beam meeting a specular or transparent surface produces one of three outcomes, and which one depends on the surface **and the incidence angle**: a return from the pane itself, a return from **behind** it (transmission), or a return from a **reflected** object elsewhere in the room [src: koch-2017]. Koch et al. concede that discriminating transparent from specular **is not solvable in a single scan** and needs multi-scan post-filtering; their mitigation uses multi-echo returns plus ICP to find the reflective plane and then masks the plane and everything behind it.

The load-bearing number is the angle window. Glass returns usable energy only near-normal: "intensity peaks on a glass surface are only detectable where the LiDAR laser beams are **perpendicular** to the glass surface", and all intensity-based methods "suffer from low accuracy when the distance **or incidence angle** of the laser beam increases" [src: tibebu-2021]. Zhao et al. restate it: the peak "rapidly decreases" with angle until the return is too weak to detect [src: zhao-2020].

| Cue | Method | Reported | Needs intensity? |
|---|---|---|---|
| Intensity peak near normal | Wang & Wang, glass detection in SLAM [src: wang-2017] | — | **Yes** |
| Visible-angle gating (grid updated only when the cell is viewed from a known diffuse-like angle range) | VisAGGE [src: visagge-2013] | **94.90%** glass correctly detected (per Tibebu's benchmark table) | Partly |
| **Range deviation between neighbouring beams** (rolling-window std-dev, then distance+intensity filter) | Tibebu et al. [src: tibebu-2021] | **96.2%** mean accuracy (96.3 / 96.5 / 95.9), VLP-16 at **90 cm** height | **No** — works off-normal |
| Dual / multi-echo (strongest vs last return disagree ⇒ nearest point is probably glass) | [src: zhao-2024] | **96.53%** reflection removal vs 74.96% single-frame prior; indoor precision **99.82%** vs 94.07% | No |
| Sonar fusion, mirror evidence taken at **depth discontinuities** | Yang & Wang, ICRA 2008 [src: yang-wang-2008] | — | No |

The mirror "fake room" failure has a canonical treatment: a Bayesian framework that detects and **tracks** mirrors from LiDAR alone and folds the result into occupancy-grid mapping and localisation [src: yang-wang-2011]. Zhao et al. give the constructive inverse — **mirror the reflection points back across the detected pane** to recover the true geometry [src: zhao-2020]. For 2D LiDAR specifically, Damodaran et al. show indoor 2D maps rendered "inaccurate, unreliable, and noisy" by reflection, penetration and diffusion [src: damodaran-2023].

**What this means for our rig, concretely.** Our own verified finding is that the **RPLIDAR quality channel in the kitchen sweep is binary (0/47 — a validity flag, not reflectivity)**. That kills every intensity-peak glass method in the table above, outright. The surviving cues for us are **range inconsistency between neighbouring beams** [src: tibebu-2021] and **geometric inconsistency across viewpoints** — plus the stereo channel, since glass has visual texture and frame edges the LiDAR lacks. Vendor context: the RPLIDAR A1 datasheet conditions its 0.15–6 m range on **"white objects"** and is a triangulation system; the C1 quotes 12 m at **70% reflectivity** with fusion-type dToF [src: slamtec-c1]. Dark surfaces shorten effective range; clear panels pass the pulse and return from whatever is behind, so **the barrier itself appears weak or missing** — which is exactly an aperture signature. A glass door is therefore our single most dangerous false positive: it will look like a passage, and it is a wall. See [[sensor-weaknesses-and-fixes]].

### Partially open doors and the 2D scan plane

Good news, from the LaserDoors work [src: laserdoors-2023]:

- **A door leaf in the scan plane reads as a clean line segment** — "the typical line shape of a door in the scan", with the free end "clearly delimited at the door corner". A door at 45° reads as a slanted wall segment, and *that is the signal, not the artefact*. The opening angle is the angle between the door line and the hinge→lock baseline.
- **Scan height is explicitly not critical** for the leaf: "the exact height of the scan plane depends on the robot hardware, but due to the **vertically oriented faces** of walls and door, this is not critical." At 1.1 m we are well inside a ~2.03 m leaf. What *is* height-sensitive is the handle, not the leaf.
- Their scan segmentation used a **15 cm** consecutive-range threshold to build line strips.

Bad news: **the closed door seen from inside, flush with the wall.** Then the only evidence is a depth *outlier* at the panel→frame and frame→wall transitions, and there is "**no general threshold** that works for all doors"; the authors tuned to a **4 mm** frame gap with a SICK TIM571 at 0.33° [src: laserdoors-2023]. That is far below RPLIDAR-class resolution, so **expect flush closed doors to be invisible to our LiDAR**, full stop. They must come from vision (the concavity/recess cue) or from a prior.

Prior art they cite is worth stealing: Shi et al. filter candidates by "reasonable door widths"; **Endres et al. segment the panel line to get the opening angle and recover the hinge as the pivot of the arc motion** — *a door that swings is identifiable by its arc*, which is a strong cue whenever we have multiple passes [src: laserdoors-2023].

### Archways vs doors — not solved by any standard segmenter

None of the four room-segmentation families implemented in Bormann's survey knows what a door is; they all find **narrow passages**, door or not [src: bormann-2016]:

- **Voronoi-graph** (after Thrun & Bücken): compute the GVD, prune to a skeleton; a point with exactly **two** closest obstacle pixels is a *critical point* candidate; critical lines join it to its two nearest obstacle points. "Critical lines with a **large angle** occur frequently at doors", small-angle ones are dropped as wall corners. Merging heuristics use hard priors: areas **< 12.5 m²** with one neighbour and **<75%** wall border merge; regions **< 2 m²** merge with a neighbour touching **≥20%** of their border; merge if a shared border is ≥20%/10%; merge if **>40%** of the perimeter touches another segment.
- **Morphological**: iterative erosion until connected regions separate — literally splitting on narrow necks.
- **Distance transform**: sweep the threshold; the room count peaks just before the threshold equals the local maxima **at doors**, at which point neighbours merge through the door connections; take t* maximising room count.
- **Feature-based** (Mozos): 33 geometric features from a simulated 360° scan at every free pixel, AdaBoost into room / corridor / **door** labels — the one line of work that treats "door" as a learned class, and it needs representative training data.

*(synthesis)* **Door-vs-archway is a leaf-detection problem, not a segmentation problem.** The three available routes are: learn it (Mozos-style), detect the **leaf** as an extra ~35 mm-thick line segment attached at one end to the frame at a non-wall angle, or detect the **swing arc** across passes. For a home robot the distinction matters — an archway's aperture is permanent map geometry, a door's is a state.

### Gap semantics done properly: the Gap Navigation Tree

Tovar, Murrieta-Cid and LaValle give the cleanest formalism for *what a gap means* [src: gnt-2007]. A gap is a **depth discontinuity** in the boundary as seen from the robot; the robot has a "gap sensor" with **no geometric information other than the angular order** of gaps. The Gap Navigation Tree maintains them under four critical events — **appear / disappear / merge / split** — and the semantics are exactly our question: a gap **encodes what is hidden behind it**; "the robot has not yet seen what is behind" it. A gap that **disappears** on approach was an occlusion boundary; a gap that **splits** revealed new structure. That is principled unknown-vs-occluded bookkeeping with no metric map at all, and it is the right mental model even if we implement the metric version.

Reactive-navigation cousins, for completeness: Follow-the-Gap builds a gap array from consecutive range differences and steers to the widest gap's centre, blended with the goal heading [src: ftg-2012]; Nearness Diagram navigation segments the nearness diagram into valleys at discontinuities and classifies each as wide or narrow **relative to robot size** [src: nd-2004]; Yamauchi's frontier is the boundary between mapped free space and unknown space, and **a beam that passes through the aperture carves free cells beyond it, converting unknown→free** — the operational statement of the aperture test [src: yamauchi-1997].

### Door dimension priors

| Region / standard | Leaf width | Height |
|---|---|---|
| US residential interior passage, typical | **762 mm** (30 in) | 2032 mm |
| US interior, common set | 457 / 610 / 660 / 711 / 762 / 914 mm | 2032 mm |
| US exterior, typical | 914 mm (36 in) | 2032 mm |
| **DIN 18101 (1985)** | **610 / 735 / 860 / 985 / 1110 mm** (most common **860 mm**) | 1985 mm leaf, 2010 mm nominal |
| DIN 18101 (2014) | 485–1360 mm range | 1610–2735 mm range |
| UK | 762 mm | 1981 mm |
| Australia | 820 mm | 2040 mm |
| India | 800 mm internal / 1000 mm external | 2045 mm |
| South Africa | 813 mm | 2032 mm |

**Leaf thickness:** interior **~35 mm** (1⅜ in), exterior **~44 mm** (1¾ in) [src: door-standards].

*(synthesis)* Practical prior for a 2D detector in a home: **an interior residential aperture is 0.61–0.92 m wide, overwhelmingly ~0.76 m (US/UK) or ~0.86 m (DE)**; the *clear* opening is a few cm less than the frame. Note that the widely-cited laser door-width band **0.735–1.110 m** [src: rule-based-door-laser, hensler-2009] is exactly the DIN 18101 (1985) series — it is a European prior, and it will miss narrow North American doors (610–711 mm). Set our band from the local standard, not from the paper. A leaf crossing the scan plane is a **~35 mm-thick** segment, thinner than any wall, which is itself a discriminator given our sub-centimetre per-scan precision.

**Unverified in this pass:** the ADA §404.2.3 32 in / 815 mm clear-width figure, and the builder rough-opening convention (door width + 2 in). Do not quote either without checking.

---

## Recommended method for this project

*(synthesis — 2D LiDAR scan plane at 1.07–1.12 m per `data/calib/rig_geometry.json`, stereo ~7 cm below it, one room, accuracy over speed, offline batch processing acceptable.)*

Two facts about our scan plane are worth stating before the recipe. **1.07–1.12 m sits at the top of Nikoohemat's 0.8–1.10 m door-centre band** [src: nikoohemat-2018] — it cuts a door aperture near its widest and above nearly all floor clutter. And height is not a risk for the *leaf* anyway: door and wall faces are vertical, so any plausible scan height intersects a ~2.03 m leaf [src: laserdoors-2023]. Height is only critical for the handle, which we do not need.

**Stage 0 — trajectory certificates (free, do this first).** Every wall crossing made by the capture trajectory is a certified aperture at that width [src: elseicy-2018]. Our capture entered the kitchen; that crossing labels at least one door with no ambiguity and no new data. It costs one polyline-vs-wall-segment intersection test against the locked EDA110 trajectory. Use it as ground truth to calibrate every threshold below.

**Stage 1 — per-wall ray bookkeeping (the discriminator).** For each locked wall segment, bin the wall into 10 cm cells along its length. For every scan point in the refined cloud, take the ray from that scan's sensor pose to the point, intersect with the wall line, and increment the intersected cell's counter for one of `occupied` / `occluded` / `open` / `unknown` by the sign of (point-range − wall-intersection-range) [src: nikoohemat-2018]. Require **≥80% `open`** over a contiguous run before calling it an aperture, and record per-cell ray counts so "unknown" is visibly distinct from "open with 3 rays".

**Stage 2 — width and shape gating.** Keep runs whose Cartesian width falls in **0.60–1.15 m** for a door — set the band from the *local* standard, since the much-quoted 0.735–1.110 m band is the DIN 18101 series and misses narrow North American doors [src: rule-based-door-laser, door-standards] — and flag wider runs as *cased opening / archway* rather than rejecting them. Confirm each candidate's two boundary jump edges are the two smallest local minima of the scan taken from in front of it [src: mozos-adaboost-2005].

**Stage 3 — viewpoint audit before you believe a negative.** Score each candidate by whether it was ever observed **face-on** (swept gap) rather than edge-on (radial gap) [src: potential-gap, dynamic-gap]. Any wall run that only ever appears as a radial gap is *undecided*, not *wall* — that distinction is the whole fix for "refuses to explore". This is also the actionable output: it tells the rover exactly where to stand to resolve each undecided run.

**Stage 4 — visual confirmation, per our own standing rule.** A LiDAR cluster is not an object and a LiDAR gap is not a door until a pose-filtered camera frame is looked at (`docs/working-knowledge.md`; we already produced a phantom "garbage can" that was in fact the window-door). Gate every candidate aperture through a stereo frame: check for a frame/jamb pair and a floor-line continuity change, and label state as open / closed / semi-open [src: ramoa-2021]. The stereo camera at ~1.00–1.05 m also gives the leaf-vs-frame plane separation that a single 2D scan line cannot.

**Stage 5 — record it as a transformable entity.** Store an `aperture` on the wall with: endpoints, width, state ∈ {open, closed, ajar, unknown}, evidence type (trajectory-certified / ray-certified / visually-confirmed), ray counts, and last-observed timestamp. `objects_v3.json` already carries 4 "doors"; upgrading those to this schema is the smallest useful change. Navigation should treat `open` as traversable, `unknown` as a **frontier to go and resolve** (not as wall), and `closed` as a soft obstacle that decays [src: fremen-2017, tipaldi-2013].

**Deliberately out of scope for us:** hinge/lock keypoint regression [src: laserdoors-2023] — that is for a robot that opens doors, we only need to know a passage exists; and learned door detectors, which do not transfer across sensors and would need our own training data.

### What NOT to do

- **Do not classify by gap width alone.** It cannot separate an unobserved wall run from a doorway, and that is precisely our failure. Width is a *filter applied after* the ray test, never the test.
- **Do not trust the free-space channel of the occupancy grid as "free space beyond".** Cells beyond a hit are unknown, not free [src: ism-standard]. The evidence for an aperture is a *return that landed past the wall plane*, not an absence.
- **Do not accept a negative from a grazing viewpoint.** A radial gap carries almost no information about what is behind it [src: dynamic-gap].
- **Do not let a closed door become a wall.** Adán & Huber's failure — closed leaves labelled as wall — is exactly the state we would bake in [src: adan-huber-2011], and it is unrecoverable once the map is locked. Our LiDAR *cannot* see a flush closed door (the evidence is a ~4 mm frame gap [src: laserdoors-2023]); that class of door must come from vision or a prior, and its absence from the LiDAR must never be read as "wall confirmed".
- **Do not forget glass is the dangerous false positive.** A glass door transmits, so rays land *beyond* the wall plane and it passes the aperture test perfectly while being impassable [src: tibebu-2021, slamtec-c1]. Our binary quality channel rules out every intensity-based glass cue, so the only defences are neighbouring-beam range deviation [src: tibebu-2021], cross-viewpoint geometric inconsistency, and the stereo frame. **Any aperture the rover has not physically driven through should stay "unconfirmed", not "open".**

---

## Open questions

- We have never tested what our rig returns off the glass in the kitchen's window-door. Until we do, every glass claim on this page is borrowed, not measured.
- A curtain or blind across an opening has no treatment in the literature and would give intermittent returns at exactly scan height. If one exists in a target room, it is a research problem, not a tuning problem.
- Nobody has published a map that carries a door node with *both* an articulation prior and a temporal state model. If we build one, it is genuinely new ground rather than a re-implementation.

---

## Citation keys

Every `[src: key]` above resolves here.

### 2D LiDAR geometry, gaps and apertures

| Key | Reference |
|---|---|
| `laserdoors-2023` | Müller, Müller, Ahmed, Gross, "Laser-Based Door Localization for Autonomous Mobile Service Robots", *Sensors* 23(11):5247, 2023 — `10.3390/s23115247`; **LaserDoors** dataset (public, academic use) |
| `nikoohemat-2018` | Nikoohemat, Peter, Oude Elberink, Vosselman, "Semantic Interpretation of Mobile Laser Scanner Point Clouds in Indoor Scenes Using Trajectories", *Remote Sensing* 10(11):1754, 2018 — `10.3390/rs10111754` |
| `elseicy-2018` | Elseicy, Nikoohemat, Peter, Oude Elberink, "Space Subdivision of Indoor Mobile Laser Scanning Data Based on the Scanner Trajectory", *Remote Sensing* 10(11):1815, 2018 — `10.3390/rs10111815` |
| `adan-huber-2011` | Adán & Huber, "3D Reconstruction of Interior Wall Surfaces under Occlusion and Clutter", 3DIMPVT 2011 (CMU Robotics Institute) |
| `potential-gap` | Xu, Feng, Vela, "Potential Gap: Using Reactive Policies to Guarantee Safe Navigation", RA-L / IROS 2021 — `arXiv:2103.11491` |
| `dynamic-gap` | Asselmeier, Ahuja, Zaro, Abuaish, Zhao, Vela, "Dynamic Gap: Safe Gap-based Navigation in Dynamic Environments", 2022 — `arXiv:2210.05022` |
| `gnt-2007` | Tovar, Murrieta-Cid, LaValle, "Distance-Optimal Navigation in an Unknown Environment Without Sensing Distances", *IEEE T-RO* 23(3):506–518, 2007 — Gap Navigation Tree |
| `ftg-2012` | Sezer & Gokasan, "A novel obstacle avoidance algorithm: 'Follow the Gap Method'", *RAS* 60(9):1123–1134, 2012 |
| `nd-2004` | Minguez & Montano, "Nearness Diagram (ND) Navigation: Collision Avoidance in Troublesome Scenarios", *IEEE T-RA* 20(1):45–59, 2004 |
| `yamauchi-1997` | Yamauchi, "A frontier-based approach for autonomous exploration", CIRA 1997 |
| `mozos-adaboost-2005` | Martínez Mozos, Stachniss, Burgard, "Supervised Learning of Places from Range Data using AdaBoost", ICRA 2005, pp. 1730–1735 |
| `2dlasernet` | "2DLaserNet: A deep learning architecture on 2D laser scans for semantic classification of mobile robot locations", 2021 |
| `rule-based-door-laser` | "Rule-Based Door Detection Using Laser Range Data in Indoor Environments", IEEE 2015 — door-width band 0.735–1.110 m, d_max 1.10 m |
| `ism-standard` | Standard inverse sensor model / occupancy-grid ray casting: cells before the hit → free, cells beyond the hit → **unknown** (Thrun, Burgard, Fox, *Probabilistic Robotics*) |
| `door-standards` | National door-dimension standards (US common set, DIN 18101 1985/2014, UK, AU, IN, ZA); leaf thickness 35 mm interior / 44 mm exterior |

### Vision

| Key | Reference |
|---|---|
| `chen-birchfield-2008` | Chen & Birchfield, "Visual Detection of Lintel-Occluded Doors from a Single Image", IEEE Workshop on Visual Localization for Mobile Platforms @ CVPR 2008 |
| `murillo-2008` | Murillo, Guerrero, Košecká, Sagüés, "Visual door detection integrating appearance and shape cues", *Robotics and Autonomous Systems* 56(6):512–521, 2008 |
| `yang-tian-2010` | Yang & Tian, "Robust door detection in unfamiliar environments by combining edge and corner features", CVPRW 2010 (and Tian & Yang, ICCHP 2010) — 91.9% / 2.9% is author-reported, test-set size unverified |
| `hensler-2009` | Hensler, Blaich, Bittel, "Real-time Door Detection Based on AdaBoost Learning Algorithm", Eurobot 2009; extended ICAART 2010 / Springer CCIS 2011 (camera + laser fusion) |
| `arduengo-2021` | Arduengo, Torras, Sentis, "Robust and adaptive door operation with a mobile robot", *Intelligent Service Robotics*, 2021 — `arXiv:1902.09051`; **DoorDetect** dataset |
| `ramoa-2021` | Ramôa, Lopes, Alexandre, Mogo, "Real-time 2D–3D door detection and state classification on a low-power device", *SN Applied Sciences* 3:590, 2021 — **DeepDoors2** dataset |
| `handle-scirep-2024` | "Neural network-based algorithm for door handle recognition using RGBD cameras", *Scientific Reports* 14, 2024 — `10.1038/s41598-024-66864-7` |
| `antonazzi-2022` | Antonazzi, Luperto, Basilico, Borghese, "Enhancing Door-Status Detection for Autonomous Mobile Robots during Environment-Specific Operational Use" — `arXiv:2203.03959` |
| `antonazzi-jfr-2025` | Same group, "Development and Adaptation of Robotic Vision in the Real World: The Challenge of Door Detection", *Journal of Field Robotics*, 2025 — `arXiv:2401.17996` |
| `quintana-2016` | Quintana et al., "Door Detection in 3D Colored Laser Scans for Autonomous Indoor Navigation", IPIN 2016; extended in *Automation in Construction*, 2018 |
| `arw-2022` | "Door Pose Estimation and Robot Positioning for Autonomous Door Opening", Austrian Robotics Workshop 2022 (Würzburg) — YOLO bbox → laser ray fan → RANSAC line |
| `rgbd-fisheye-2024` | "Floor extraction and door detection for visually impaired guidance" — `arXiv:2401.17056` |
| `calvert-2026` | Calvert, "A System for Fast, Resilient, and Adaptable Loco-Manipulation Behaviors on Humanoid Robots", PhD dissertation, 2026 — `arXiv:2606.26425` (hinge side, push-vs-pull recess check) |

### Maps that change state

| Key | Reference |
|---|---|
| `thrun-1998` | Thrun, "Learning metric-topological maps for indoor mobile robot navigation", *Artificial Intelligence* 99(1), 1998 |
| `bormann-2016` | Bormann, Jordan, Li, Hampp, Hägele, "Room Segmentation: Survey, Implementation, and Analysis", ICRA 2016 (ROS code: `ipa320/ipa_coverage_planning`) |
| `hydra-2022` | Hughes, Chang, Carlone, "Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization", RSS 2022 — `arXiv:2201.13360` |
| `sgraphs2-2025` | Bavle et al., "S-Graphs 2.0", *T-RO* 2025 — `arXiv:2502.18044` |
| `indoorgml` | OGC IndoorGML — doors as `CellSpaceBoundary` + `Transition`, dualised to a node-relation graph (OGC 19-004) |
| `imac-2012` | Saarinen, Andreasson, Lilienthal, "Independent Markov chain occupancy grid maps for representation of dynamic environment", IROS 2012 |
| `tipaldi-2013` | Tipaldi, Meyer-Delius, Burgard, "Lifelong localization in changing environments", *IJRR* 32(14):1662–1678, 2013 |
| `meyerdelius-2010` | Meyer-Delius, Hess, Grisetti, Burgard, "Temporary maps for robust localization in semi-static environments", IROS 2010 |
| `fremen-2017` | Krajník, Fentanes, Santos, Duckett, "FreMEn: Frequency Map Enhancement for Long-Term Mobile Robot Autonomy in Changing Environments", *IEEE T-RO* 33(4), 2017 |
| `sturm-2011` | Sturm, Stachniss, Burgard, "A Probabilistic Framework for Learning Kinematic Models of Articulated Objects", *JAIR* 41, 2011 |
| `opd-2022` | Jiang, Mao, Savva, Chang, "OPD: Single-view 3D Openable Part Detection", ECCV 2022 (oral) |
| `momallm-2024` | Honerkamp, Büchner, Despinoy, Welschehold, Valada, MoMa-LLM, *RA-L* 2024 — `arXiv:2403.08605` |
| `passage-aware-2026` | Tourani et al., "Passage-Aware Structural Mapping for RGB-D Visual SLAM", 2026 — `arXiv:2604.24707` (short paper, qualitative only) |
| `nikdel-2019` | Nikdel & Vaughan, occupancy-grid CNN for closed doors / open corridors / intersections, 2019 — `arXiv:1903.03669` |
| `irobot-lifelong-2020` | Narayana, Kolling, Nardelli, Fong (iRobot), "Lifelong Update of Semantic Maps in Dynamic Environments", 2020 — `arXiv:2010.08846` |
| `pocd-2022` | Qian, Chatrath et al., "POCD: Probabilistic Object-Level Change Detection and Volumetric Mapping in Semi-Static Scenes", RSS 2022 — `arXiv:2205.01202` |
| `oasis-map` | Oh, Tao, Chebrolu, Fallon, "OASIS-Map", 2026 — `arXiv:2607.14899` |
| `rosen-lifelong` | Rosen, Mason, Leonard, "Towards Lifelong Feature-Based Mapping in Semi-Static Environments", ICRA 2016 |
| `ambrus-2017` | Ambruş et al., detection and tracking of general movable objects in large 3D maps — `arXiv:1712.08409` |
| `nav2-costmap` | Nav2 costmap layer semantics — static layer sourced only from `/map`, never updated from live sensor data |
| `nav2-issues` | `ros-navigation/navigation2` issues #545, #5544 (obstacles never clear), #5476 (cleared too eagerly), #1248 ("Navigation failed") |
| `roborock-support` | iRobot / Roborock owner guidance: open every door before the mapping run; a room lost behind a closed door needs a full re-scan |
| `belief-pathtree-2022` | Path-tree optimisation in belief space — door-open prior 80% → direct route with branch points; 50% → longer certain route — `arXiv:2204.04444` |
| `dreame-support` | Vendor support notes on curtains as an entrapment and map-distortion nuisance |

### Glass, mirrors and sensor behaviour

| Key | Reference |
|---|---|
| `koch-2017` | Koch, May, Nüchter, "Detection and Purging of Specular Reflective and Transparent Object Influences in 3D Range Measurements", *ISPRS Archives* XLII-2/W3:377–384, 2017 |
| `tibebu-2021` | Tibebu, Roche, De Silva, Kondoz, "LiDAR-Based Glass Detection for Improved Occupancy Grid Mapping", *Sensors* 21(7):2263, 2021 — `10.3390/s21072263` |
| `zhao-2020` | Zhao, Yang, Schwertfeger, "Mapping with Reflection", SSRR 2020 — `arXiv:1909.12483` |
| `zhao-2024` | Journal successor to the above, *Sensors* 24(15):4794, 2024 — `arXiv:2406.10494` (multi-echo) |
| `wang-2017` | Wang & Wang, "Detecting glass in SLAM", *Robotics and Autonomous Systems* 88:97–103, 2017 |
| `visagge-2013` | Foster, Sun, Park, Kuipers, "VisAGGE: Visible Angle Grid for Glass Environments", ICRA 2013, 2213–2220 |
| `yang-wang-2008` | Yang & Wang, "Dealing with laser scanner failure: mirrors and windows", ICRA 2008 |
| `yang-wang-2011` | Yang & Wang, "On Solving Mirror Reflection in LIDAR Sensing", *IEEE/ASME Transactions on Mechatronics* 16(2):255–265, 2011 |
| `damodaran-2023` | Damodaran, Mozaffari, Alirezaee, Ahamed, "Experimental Analysis of the Behavior of Mirror-like Objects in LiDAR-Based Robot Navigation", *Applied Sciences* 13(5):2908, 2023 (abstract-level only) |
| `slamtec-c1` | SLAMTEC RPLIDAR C1 product page (12 m at 70% reflectivity, fusion-type dToF, 0.05 m blind zone) and RPLIDAR A1M8 datasheet (0.15–6 m conditioned on "white objects", triangulation) — see [[cheap-lidar-pricing-guide]] |
