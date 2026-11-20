# One belief update for objects: drone.beliefs (drone-prototype, 2026-11-18 → 11-20)

How the rover now creates and updates what it believes about objects, and what the first live run showed. Since
2026-11-19 the area check files new beliefs and updates existing ones through ONE package, `src/drone/beliefs/`
(human 2026-11-19: "update belief should be the sole source of how we update a belief, same with the new belief
function"). **Status: merged (PRs #351–#356, 2026-11-18 → 11-20). Live on the AREA CHECK only; the other creators and
updaters (camera floor items, LiDAR targets, large objects, registry filing from world runs, station re-observation)
still use their own code (P-01765). One live run (11-20, 5 checks, objects moved overnight). Positions are compared
with camera / stereo estimates, not tape-measured truth.**

## Source

drone-prototype repo, master `a39f6b37`:
- diary entries 2026-11-18 (c) check belief update, (d) check belief fixes 2–5, (e) belief-update steps + auto
  part-of merge; 2026-11-19 (f) drone.beliefs v1; 2026-11-20 (a) geometry V4 + belief view, (b) first live V4 run
- `src/drone/beliefs/` (`check.py`, `update.py`, `new.py`, `geometry.py`, `camgeo.py`, `vlm.py`, `store.py`),
  `config/objects.json` `beliefs_cfg`, `objects.check_belief_mode`
- parked P-01756…P-01762 (check-belief build and merge), P-01765 (v1), P-01766 (V4 + belief view), P-01767 (live run)
- earlier: `src/drone/agent/checkbeliefs.py`, `beliefsteps.py` (the 11-18 path, now behind `check_belief_mode`
  "visual" / "legacy")

## The principle (human, 2026-11-16 → 11-18)

- Every reading that can move a belief is used, in both directions. A failed check is **explained through beliefs**,
  never by blocking a region: the evidence updates the known things the camera saw, and block evidence that nothing
  explains spawns a new, uncertain belief (P(exists) 0.3, P-01756).
- LiDAR-only things and walls explain evidence but are not updated by a check.
- Merges are automatic when geometry and appearance agree (11-18 e): the chair's base, filed again as a "toy car"
  floor item, was folded into the chair (DINOv2 cosine 0.650 vs a bar of 0.55, calibrated on one check, P-01762).

## The pipeline (one check)

`drone.beliefs.check.run`, in its own memory-capped subprocess:

1. **Hypothesis check (v4):** which beliefs should be in view.
2. **Evidence:** map-first alignment on measured walls, then LiDAR clusters and stereo points per belief.
3. **Vision:** cluster-placed crops, object-only DINOv2 fingerprints, open-vocabulary label reads, filing crops.
4. **Update** per belief: predict (permanence process noise) → measure → associate → update location, dims, label,
   reference images, existence → write-through to the registry / world records.
5. **New beliefs:** `drone.beliefs.new.new_belief` is the check's only creator. Birth geometry is the measured
   extent; a camera-only birth gets a nominal 5 cm radius marked unmeasured.

## Identity: reference images first, the VLM when unsure

- Each belief keeps up to 6 **reference images** (diverse: cosine < 0.93 to the ones it has; lit; the first, filing
  view is always kept).
- **Association:** a look belongs to a belief on a clear visual match (DINOv2 cosine ≥ 0.65 to its references and
  ≥ 0.03 better than any other belief's), or on a geometric fit (Mahalanobis gate × measurement quality × belief
  certainty ≥ 0.25). One evidence cluster goes to one belief; the loser becomes a twin / merge candidate.
- **Visual cases:** a = same thing, b = a different thing replaced it, c = the old belief was a false positive (its
  references never showed an object), d = same thing, wrong label or shape. Clear cosine cases decide on their own;
  the rest go to the VLM.
- **Session VLM questions.** The VLM backend "session" writes each question (text + image paths) to
  `data/beliefs/<world>/vlm_queue/<qid>.json`; Claude in the working session answers from the images between checks
  (22 answered on 11-20). A pending question means the look is not applied (conservative); answers apply at the
  **next** look. Two forms: A (references vs now) and an escalated B (plus context images, with a "more" option).
  Nearby beliefs are shown as neutral tags N1, N2…, so the VLM can answer `same_as` (a duplicate → merge). The
  "api" backend is written but has never run (P-01765).
- **Question ids must belong to the belief, not the run** (live finding 11-20): a run-keyed id made a new question
  every check that was never read, and an "_n" suffix that changed with the neighbour set orphaned answers. Fix:
  `<id>__verify<n>` / `<id>__classify<n>`, n advancing once answered; `same_as` tags resolve against the neighbour
  list stored with the question (PR #356 review B2).

## The filing gate (live finding 11-20)

A just-filed belief takes its first ("filing") reference image only when the look's evidence is **inside its own
gate and not a twin**. Without the gate, a provisional belief 16 cm from a moved cup (d² 24, outside its gate) filed
the cup's crop as its own reference, then out-matched the cup's real belief visually (0.83) and the cup's belief was
treated as its twin.

## Geometry V4 (11-20 a)

- ONE dims function (object-frame voxels, axis intervals, log-space prior, silhouettes, footprint outlines) and ONE
  location function (`fuse`: anisotropic noise, correlated looks, own-scatter floor, consensus); each look is
  registered against the **world-fixed** voxel shape.
- Camera geometry (`camgeo`): a box-prompted MobileSAM mask + masked stereo + a metric height interval from the top
  pixel's ray. The prompt is the belief's own measured cluster box when there is no own-label detection.
- Replay of the 15 live checks of 11-19 (VLM off): location vs hand-picked references 0.8–6.0 cm (references good to
  ~3–5 cm); cup 0.072 × 0.077 × 0.154 m; ~72 s per check, 0 crashes.
- General fixes the replays forced: foreign returns (inside another belief's footprint) carve free space but never
  join a belief; register against the world-fixed shape (registering against the belief's own centre crept the bed
  +1 cm per look); registration noise from the spread of near-best shifts (a flat face lets a look slide); height from
  the top-pixel ray (the box height is foreshortened); a stereo height counts only if the top-ray or LiDAR agrees; a
  "move" must be bigger than the thing.
- Limits (P-01766): floor-standing things only (base ≤ 10 cm); the stereo height model saturates ~0.10 m.

## First live run (11-20 b): a relocation test

Objects had been moved overnight; 5 checks of 11-19's areas.
- The cup (moved ~17 cm) ended as a belief RELOCATED 0.16 m, ~2 cm from its stereo position, but under a different id:
  the old cup belief merged away (identity did not travel).
- The flashlight was taken over by a neighbouring belief; its fused location sits ~17 cm short of its centre with a
  2 cm sigma (overconfident: located on its 5 near-end LiDAR returns).
- Four beliefs were retired as floor by the VLM (mat edges, bed foot pads).
- Four fixes from the run: mislocated things enter the two-look move rule; belief-scoped question ids; the filing
  gate; cluster boxes clipped to the image (an off-frame box crashed one check's whole update).
- **Honest limits:** identity did not travel with the moves because records filed before drone.beliefs have no
  reference images (back-fill owed); the helicopter is not separated from the vacuum head beside it; the update took
  270–330 s in the check host vs 75 s by hand (not diagnosed). Localisation still used the locked map, against the
  active-map rule (P-01767).

## Related

- [[object-certainty-model]]: the EDA355 certainty model; drone.beliefs keeps its own existence log-odds and a second
  state store beside the records until every updater moves over (P-01765 N3)
- [[object-fingerprint-memory]]: the June per-instance fingerprint design; DINOv2 ViT-S is still the embedder
- [[locate-object-from-last-known-position]]: why a record needs where it was seen from
- [[floor-check-visual-first]]: the floor / low-object check that feeds the area check
- [[object-detector-measured-rates]] · [[incremental-large-object-update]] · [[task-conditioned-object-maps]]
