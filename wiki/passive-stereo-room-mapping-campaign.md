# Passive-stereo room-mapping campaign — what's achievable on existing data (EDA010–028)

**Durable findings of the 2026-06-07 autonomous research campaign** (drone-prototype). The campaign's
question: *using only the existing SVPRO passive-stereo captures (no new hardware, offline / no realtime
constraint), how much of the room-mapping + navigation mandate can be demonstrated, and where is the hard
wall?* This page is the cited, stable home for the conclusions; the live working record is the prototype's
`docs/research-campaign/` (method-log, problem-breakdown, solution-stacks, sensor-wishlist) and per-probe
`eda/EDA0NN-*/` dirs.


---

## Headline (one paragraph)

On existing passive-stereo data, **the core mandate is demonstrable end-to-end at toy scale with no new
hardware**: a relocalizable metric anchor map (hloc, 96% reloc, scale −1.9% vs tape) + a collision-free
A\* path planned on the achievable navigation map (EDA023/024 demo). The **one durable gap is crisp metric
walls / a clean room outline from passive vision** — confirmed by 7 independent probes + 1 fusion stack —
caused by ~20% per-pixel passive-stereo depth noise, not by software or trajectory choices. That gap is
**not a navigation blocker** (treating UNKNOWN space as blocked is a safe substitute for planning); it is a
map-completeness / wall-trustworthiness gap that needs either a perimeter-floor re-capture (free, existing
camera) or an active depth sensor (Gemini 2, $234) — see [[economical-ir-depth-cameras]].

---

## (a) Passive stereo gives free-space + floor, NOT crisp walls — the central durable result

Seven probes, each attacking the wall problem a different way, all land in the same place:

| Probe | Method | Result on walls |
|---|---|---|
| EDA010 | naive point-projection floor plan | fails (blank-wall wrong-fill) |
| EDA011 | free-space ray carving | navigable blob, area 3.7× true room — rays punch through blank walls |
| EDA013/015 | multi-frame accumulation (incl. loop-closed sweep) | 0 Manhattan walls, starburst blob; near-stationary 5-frame accumulation smears 6×7 m (27% plane inliers) |
| EDA014 | relative monocular depth (Depth-Anything-V2) + affine fit | ~32% rel. error at wall distance; held-out R² negative |
| EDA016 | **metric** monocular depth (DAv2 Metric-Indoor) | 15% pooled rel-error (metric *on average*) but **38% single-plane inliers** (need 70%); **~20% per-pixel noise** |
| EDA017 | room-from-structure via surface normals | starburst blob; normals are depth derivatives → amplify the noise (59.8° per-pixel swing) |
| EDA018 | room outline from reliable FLOOR extent | first *coherent* (non-starburst) region, but coverage-starved — traces the navigated swath, not the room |
| EDA021 | S-3 fusion stack (carve + floor + furniture, opposite-error bracket) | **refuted** — stack is *larger* than the room; opposite-error layers don't synthesize a wall none contains |

**Root cause (confound-free, EDA016):** the *same pixel* wobbles ~20% across frames at <4 cm camera motion
— ≈ identical for SGBM stereo (18.8%) and metric-mono (19.9%). A 3 m wall therefore lands in a **±0.6 m
slab**. Normals (spatial derivatives of depth) amplify it; stacking can't invent a wall edge the input never
contained. The **flip-condition** for any depth source to map walls: near-stationary accumulation must
collapse to a plane at **>~70% single-plane inliers** (passive stereo gets 27–47%).

**The one nuance worth keeping (EDA018):** the *floor-extent* method's limit is **coverage, not precision** —
the camera simply never imaged the floor out to the wall bases. That single sub-result is what makes a
**software-only (re-capture) fix plausible** for a floor map (see (d)).

**What passive stereo DOES give, rock-solid:** floor plane + gravity (RANSAC RMS **~1.7 cm**, drift-immune,
reproduces across rooms ~1.66–1.72 cm), and a coherent **free-space / navigable** region for planning.

## (b) Trajectory drift (R0b) is software-solved by hloc SfM poses — adopt as the default trajectory source

RTAB-Map's ORB-odometry-with-rare-closures front-end fails to loop-close on **2 of 3** test rooms
(room_sweep3 drifts 15 m; living room 5.6 m, 0/162 closures) — the same brittle ORB front-end hloc already
beats 48× on relocalization. Replacing the trajectory source with **hloc SfM global poses** (SuperPoint +
LightGlue → global bundle adjustment) fixes it:

- **EDA027 (room_sweep3, the hardest sweep):** start→end drift **15.34 m → 0.15 m (~100×)**; trajectory bbox
  fits *inside* the tape-GT room; 330/335 keyframes registered.
- **EDA028 (living room, 2nd independent room):** drift **5.62 m → 1.39 m**, fake drift-walls removed, loop
  closes where RTAB couldn't.

**Pipeline recommendation (durable): adopt hloc SfM poses as the default offline map-build trajectory
source**, replacing RTAB odometry. Drift-immune layers (floor plane, per-keyframe object placement) were
always fine; this unblocks the *trajectory-dependent* layers (nav extent, cross-room accumulation).

**Two limits now cleanly disentangled — do not conflate them:**
1. **Drift (R0b)** → FIXED in software by hloc poses. Generalizes across rooms.
2. **Per-pixel wall-depth noise** → NOT fixed by poses (EDA027 accumulation with perfect hloc poses still
   overshoots 13×9 m — that's the depth fan, not drift). Needs active depth / re-capture.

**Honest caveat (EDA028, the most useful one):** correct poses gave a *smaller* connected nav region
(22.5→11.2 m²) because RTAB drift had been *inflating* free-space by stretching the map. **A more correct
map is not always a larger nav region** — the win is correctness, not size.

## (c) The achievable world model + the navigation demo (mandate Goals 1 & 2, on existing data)

**Goal 1 — relocalizable anchor map:** ✅ hloc 96% cross-session reloc (EDA003) vs RTAB ~2%; metric scale
−1.9% vs tape GT (EDA008). See [[relocalization-method-bakeoff]] / [[anchor-map-protocol]].

**Goal 2 — plan a collision-free path on that map:** ✅ runnable demo (`src/demo/nav_demo.py`, <5 s CPU,
13.2 m A\* path). Key chain:
- **EDA022:** does nav even need crisp walls? No — the navigable rim is 86% bounded by *sensed* obstacles;
  UNKNOWN-as-blocked is a safe substitute. The wall gap is reframed as a free-space *quality* gap.
- **EDA023 (capstone):** the fragmentation that looked like a blocker was carve **noise** (15,430 carve
  cells vs 818 furniture). Clean obstacle layer = furniture footprints only → largest connected nav region
  **6.0 m² → 39.6 m² (6.6×)**, 82% of traversable area in one region, A\* 6/6, across realistic chassis
  sizes. Software-fixable; no new hardware.
- **EDA024:** robust to relocalization noise — **100% valid collision-free paths at ~⅓ m reloc noise**
  (EDA008's actual error), with region-aware snap.

**World-model layers achievable now:**
- structural/anchor layer (hloc metric anchor) ✅
- floor + gravity ✅ (~1.7 cm)
- free-space / nav costmap ✅ (carve `is_free` + furniture footprints, UNKNOWN-blocked)
- object footprint layer ⚠️ good-enough as a semantic-anchor / tidy-target map: YOLO11-seg auto-detect →
  T_map_object placement (683 anchors, no hand-boxing), DINOv2 re-ID → 40 persistent footprint instances.
  Named ceiling: furniture appearance is a weak re-ID separator in-the-wild (over-split on big/sectional
  furniture); not an instance-accurate counter. See [[object-fingerprint-memory]] / [[world-model-architecture]].
- **walls** ❌ the only structural gap — and not a nav blocker (see above).

## (d2) Learning-based floorplan methods — promising but unvalidated on passive-stereo data

*(editorial, added 2026-06-09 after research into CAGE/RoomFormer/MonteFloor/PolyFit/Progressive-X — see [[floorplan-reconstruction-methods]])*

Several 2021–2025 methods (RoomFormer CVPR 2023, CAGE NeurIPS 2025, MonteFloor ICCV 2021) claim robustness to blurred/noisy top-down density maps using learned representations — most notably CAGE's edge-centric formulation which claims to "recover regular polygons even in severely occluded regions." These claims are made against Structured3D (synthetic photo-realistic) and ScanNet RGB-D — both substantially higher-quality inputs than raw passive-stereo SfM clouds.

**The passive-stereo caveat stands:** the root cause documented here (the *same pixel* wobbles ~20% across frames → ±0.6 m slab at 3 m, see EDA016) degrades the *density map* fed to any downstream method, not just classical edge detectors. A learned method may be better at inferring wall geometry from a blurred density map, but the blurring itself is not solved by the representation. The "flip-condition" (>~70% single-plane inliers) applies regardless of what the downstream polygon-fitter does with the result.

**Actionable:** EDA046 (proposed in [[floorplan-reconstruction-methods]]) — run pretrained RoomFormer on our SfM density maps as an upper-bound benchmark *before* committing to fine-tuning. This distinguishes "learned methods help on our noise regime" from "learned methods overfit to their training domain."

## (d) D-00002 reframed — depth sensor is an UPGRADE, not a nav-unblock; perimeter re-capture first

The campaign changes the standing hardware decision (`docs/hitl-queue.md` D-00002):

- A 2D-LiDAR / depth camera is now an **upgrade** (to a wall-trustworthy, scalable, larger-room nav map),
  **NOT** required to unblock navigation — Goal 2 is demonstrable on existing data (EDA023/024).
- **Cheapest path to trustworthy walls is software/capture, try it first:** a **perimeter-floor re-capture
  with the existing passive camera** — hug the walls, camera angled down at the floor-wall junction — feeding
  the EDA018 floor-extent algorithm (M-020). Could yield a ~RoomPlan-class (~37 cm) floor outline with no new
  hardware, because EDA018 showed the floor-map limit is *coverage*, not precision.
- **If hardware is bought:** the recommendation is the **Orbbec Gemini 2 ($234)** (active-IR stereo + IMU +
  Linux/ROS, Class-1 eye-safe) — $100 under the D435i, $15 under the Unitree L1, and it solves blank walls
  directly. Full pricing rationale: [[economical-ir-depth-cameras]] (Top pick) and [[dot-projector-options]].
  M-020 (floor-extent) is the algorithm to pair with either path.

---

## Pointers (where the detail lives)

- **Live working record:** drone-prototype `docs/research-campaign/method-log.md` (every method M-001…M-028
  with numbers), `problem-breakdown.md`, `solution-stacks.md`, `sensor-wishlist.md`; entry point
  `docs/research-campaign/README.md`.
- **Per-probe artifacts + figures:** `eda/EDA0NN-*/` (e.g. EDA023 clean costmap, EDA027/028 hloc poses,
  EDA029 error-analysis figs).
- **Demo:** `src/demo/nav_demo.py` + `src/demo/README.md`.
- **Diary (narrative of record):** `docs/prototype-diary.md`. Hardware decision: `docs/hitl-queue.md` D-00002.

## Source

drone-prototype research campaign, 2026-06-07 (EDA010–028, capstone reached). Probe numbers are the
prototype's own measured data. Detailed pointers: `docs/research-campaign/method-log.md` (M-001…M-028),
`problem-breakdown.md`, `solution-stacks.md`, `sensor-wishlist.md`, `docs/prototype-diary.md`,
`docs/hitl-queue.md` D-00002.

## Related

[[passive-stereo-robustification]] · [[stereo-dense-reconstruction]] · [[anchor-map-protocol]] · [[relocalization-method-bakeoff]] · [[economical-ir-depth-cameras]] · [[world-model-architecture]] · [[sensor-weaknesses-and-fixes]] · [[cheap-lidar-pricing-guide]]
