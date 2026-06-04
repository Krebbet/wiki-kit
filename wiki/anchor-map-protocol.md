# Anchor-Map Protocol — how to build a good navigation-anchor map (passive stereo)

How to **capture and build** a reusable indoor navigation-anchor map with the project's passive USB
stereo rig, so that later cross-session relocalization is high-rate and the map is metrically
trustworthy. This is the *map-build* counterpart to [[relocalization-method-bakeoff]] (which settled
the *method* — learned front-end hloc beats classical RTAB-Map ORB→PnP). The guidance here is
**earned from the prototype's own measured runs** (EDA004/006/008/009), not borrowed. *(synthesis —
`drone-prototype/docs/experiments-log.md` EDA004/006/008/009 + each `eda/EDA00N-*/major-findings.md`
+ `data/ground-truth/room-dims.md`.)*

## TL;DR — the recipe

1. **Build the anchor map from SEVERAL overlapping free-hand passes, POOLED into one SfM** — not one
   "perfect" pass. This is the headline result (EDA009): pooling two same-room sweeps gave **93.6%**
   cross-session reloc (body 96% **and** coverage-tail 88%), beating either single sweep (+11 pp over
   one dense pass, +17 pp over one broad pass). Several *easy* passes beat one *hard* dense one.
2. **You do NOT need to manually align the passes.** The pooled SfM **co-registers them
   automatically** — NetVLAD retrieval over the merged image set proposes cross-sweep pairs and
   COLMAP fuses them into one connected model (944/947 keyframes registered in EDA009). No explicit
   cross-session loop closure, no manual seam-stitching.
3. **Why it works — density × coverage, and they compound (they don't trade off).** A *single*
   fixed-stride sweep is zero-sum: broaden it to cover the tail and you thin the body (EDA006: tail
   52→87% but body 96→72%, net −6 pp). Pooling escapes the trade because the union carries both each
   sweep's coverage *and* ~2× keyframe density where they overlap — median PnP inliers jumped
   82/60 → **198** (2.4–3.3× richer geometry) on the merged map.
4. **Capture passes that graze the end walls / full room extent**, and prefer **straighter,
   full-length sweeps** over bent L/hairpin paths (see Forward recommendations).

## Why "one good pass" is the wrong mental model (the measured arc)

The instinct is to capture one careful, dense, full-room sweep. The prototype tested that and it
**caps out**:

- **EDA004** — two independent free-hand passes of the same room (sweep4 map, sweep6 probe). hloc
  localized the body at 85–100% but the **trajectory tail collapsed (seg7 36%, seg8 58%, seg9 62%)**.
  Diagnosed as a **map-coverage gap**, not blur (the failing tail was *sharper* than the body;
  r(sharpness, inliers) ≈ −0.13; 88–93% of failures contiguous = a region, not random hard frames).
  hloc fixes geometry, **not coverage** — it cannot manufacture viewpoints the mapping pass never saw.
- **EDA006** — fix the tail with a *broader* single sweep (sweep7, +doorway). The tail closed
  (52→87%) **but the body thinned** (96→72%) because a fixed keyframe budget spread over ~2× the path
  → keyframe density 19.4 → 13.3 kf/m (−32%), **net −6 pp overall**. So *extent alone, at fixed
  budget, is zero-sum* — **density became the live variable.**
- **EDA009** — stop choosing. **Pool sweep4 ∪ sweep7 into ONE SfM** (417 + 530 = 947 keyframes). It
  won outright: **93.6% overall, body 96.1% AND tail 88.0%**, per-segment tracking or beating the
  better single map in every bin. The merge gets the dense body from sweep4 *and* the tail coverage
  from sweep7 — **the gains compound.**

**Generalizable principle:** *coverage* is a precondition (capture every viewpoint you'll later
relocalize from) and *density* multiplies quality (more keyframes near a viewpoint → richer, more
geometrically-consistent correspondences → higher PnP-inlier counts). Pooling several overlapping
passes buys both at once, and the SfM stitches them for free.

## Metric scale — recovered and validated (so the anchor is trustworthy)

A passive-stereo monocular-left SfM map is **up-to-scale**; it must be anchored to be a metric
navigation substrate. The prototype both recovered scale and validated it against the real room:

- **EDA005 (GT-free):** align the hloc SfM to RTAB-Map's stereo-metric frame (Sim(3)) → scale
  **≈ 0.833 m/SfM-unit** (stable to ~2%), **loop-closure drift ~34 cm** median (p90 56).
- **EDA008 (vs ground truth):** the human tape-measured the space; the map's room **width recovers
  2.99 m vs GT 3.048 m = −1.9%** (~6 cm on 3 m). *Consistency was correctness* — no hidden scale
  bias. The anchor is **metrically good to ~⅓ m**, adequate for room-level navigation.
- **Honest residual:** the long axis under-reads GT by ~6% — **proven to be a coverage artifact**
  (the camera path never reached the far walls), not a scale error (both independent maps agree on
  scale yet both fall short). This is exactly the coverage lesson above, surfacing in the metric.

GT record: `data/ground-truth/room-dims.md` (two in-line rooms, ~9.5 m long, blue 3.05 m / red
3.20 m). Resolved P-005.

## Forward recommendations (durable guidance for the next map builds)

1. **Pool multiple overlapping passes** — the core recipe. 3+ sweeps likely push toward ~100%
   (EDA009 follow-up), but **build cost grows ~quadratically** with #sweeps (SfM pair count); at
   scale, cap pairs with **retrieval/vocab-tree pairing** rather than exhaustive matching.
2. **Capture straighter, full-length sweeps that graze the end walls.** EDA008's bent **L/hairpin**
   capture forced a *local-perpendicular* width measurement (a global short-axis was invalid) and
   left the long axis coverage-limited. A straight full-length sweep gives unambiguous global
   dimension recovery and a clean second metric confirmation.
3. **Export the RTAB-Map occupancy grid on every build.** EDA008 found `Admin.opt_map` was **NULL**
   (no optimized occupancy grid exported) → all dimension/wall measurement had to ride on the
   **cluttered raw feature cloud** (features land on furniture, not the wall plane; caps width
   resolution at ~0.3–0.5 m and the 6-inch room step was not cleanly resolvable). The occupancy grid
   is also the **traversability substrate for Nav2 path planning** — export it.
4. **Mind keyframe density, not just extent.** A broad sweep at a fixed stride thins density; if you
   must use one pass, raise the keyframe rate to keep the body dense while covering the tail
   (untested at scale — pooling is the proven escape).
5. **Two known open integration gaps** (not map-build, but they gate productization): the learned
   front-end is **offline batch SfM** today → put SuperPoint+LightGlue under RTAB-Map's *online*
   back-end; and it uses **research-only weights** (SuperPoint/SuperGlue) → swap to permissive
   **DISK/ALIKED** before any product use.

## The map artifact (what you get out, and how it's used)

Two artifacts, two roles (full inspection in `drone-prototype/docs/eda-mapping-state.md`):

- **RTAB-Map `.db`** (online, **metric** from the 57.6 mm stereo baseline): keyframes + 6-DOF poses
  + DBoW2 visual vocabulary + loop-closure graph + a 3D occupancy grid in one SQLite file. The
  **anchor + nav substrate** (frame→pose service + traversable grid; the self-contained artifact that
  must survive WiFi dropout, per [[system-architecture]]). Its weak point is the ORB→PnP frame→pose.
- **hloc SfM model** (offline batch, **up-to-scale** until anchored): COLMAP `cameras/images/points3D.bin`
  with SuperPoint-described points and LightGlue tracks. The **strong frame→pose localization
  reference** for the learned front-end. No grid, no native metric scale.

**Target = combine them:** RTAB-Map's metric grid + save/reload back-end, with the hloc learned
front-end doing the frame→pose. That is the documented integration path
([[passive-stereo-robustification]] rung-3; [[relocalization-method-bakeoff]] §6).

## Related

[[relocalization-method-bakeoff]] · [[map-then-navigate]] · [[slam]] · [[system-architecture]] ·
[[methods-reading-list]] · [[passive-stereo-robustification]] · [[indoor-cluttered-slam]] ·
[[home-tidy-drone-prototype]] · [[world-model-architecture]] (this anchor is Layer 1 of the
home-tidy world model — how objects + change layer on top)

---

*Cross-refs: `drone-prototype/docs/experiments-log.md` (EDA004/006/008/009),
`eda/EDA004-hloc-generalization/`, `eda/EDA006-coverage-test/`, `eda/EDA008-absolute-scale-gt/`,
`eda/EDA009-multisweep-map/` (each `major-findings.md`), `docs/eda-mapping-state.md`,
`data/ground-truth/room-dims.md`, `docs/parked.md` (P-005 resolved).*
