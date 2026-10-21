# Improvement rounds, 2026-10-21 (drone-prototype rover: walls, large objects, identification, reach)

**Status: project record, offline-only results.** On 2026-10-21 the human asked the rover prototype to run 3–6 rounds on
its own, improving processes already anchored in results: (1) wall hypotheses, their certainty and correction as new
evidence arrives; (2) large-object detection, certainty, dimensions and relocalisation; (3) object identification ("did
we correctly ID this object as X"); later (4) maximise the floor the rover can enter without giving up body clearance
or the guard. Three rounds merged (drone-prototype PRs #134–#141, EDA266–EDA272). **Every number below comes from
offline replays of recorded office runs** (office-full1, office-gap28, office-full2). None of these changes has run on
the rover yet. Librarian summary page: pointers and headline numbers only. The FINDINGS files are the record.

## Source

All paths are in the drone-prototype repo (`/home/david/drone/drone-prototype`), master at `06bce98` (PR #141).

- `eda/EDA266-wall-beliefs/FINDINGS.md`: round 1, walls (PR #134)
- `eda/EDA269-wall-markers/FINDINGS.md`: round 2, walls (PR #138)
- `eda/EDA267-large-objects-round1/FINDINGS.md`: round 1, large objects (PR #135)
- `eda/EDA272-heldout-objects/FINDINGS.md`: round 3, large objects + identification on office-full2 (PR #141)
- `eda/EDA268-identification/FINDINGS.md`: round 1, identification (PR #136)
- `eda/EDA271-id-answers/FINDINGS.md`: round 3, identification (PR #140)
- `eda/EDA270-reach/FINDINGS.md`: round 3, reach (PR #139)
- `docs/prototype-diary.md` entries dated 2026-10-21; shortcuts in `docs/parked.md` P-00180…P-00238; the human's open
  questions in `docs/hitl-queue.md` D-00011, D-00012.

## Related

- [[lidar-floorplan-extraction]]: the closed-outline floor plan these wall rounds extend
- [[door-aperture-detection]]: the doorway rule used for the NW diagonal with its door open
- [[semantic-object-memory]] and [[locate-object-from-last-known-position]]: object beliefs, relocalisation
- [[3d-shape-completion-for-object-footprints]]: the measured-vs-assumed object extent behind the two-level outline
- [[stop-and-go-navigation-on-a-locked-map]]: station validity and the guard the reach round relaxes
- [[robot-task-orchestration]]: the task loop that runs all of these as tasks
- [[robust-evidence-mapping-principle]]: the project rule that hidden walls follow (a hypothesis stays a gap until measured)

## The yardstick had to be fixed first

Every round-0 replay ran the large-object tracker with **no floor plan**. Its child process rebuilds the floor plan
from `floorplan_evidence.npz`, which the replay evaluator saved only at the end of a run. After the fix (save per
station, P-00184) the replays reproduce the live run's objects. All before/after numbers in the rounds are against
master plus this fix. **Any replay comparison made before EDA266 is invalid** (EDA266 §Step 0). Round 3 also used
office-full2 to tune the rules, so it is no longer a held-out world (P-00230). A fourth recorded world is needed for an
honest held-out score.

## Walls behind large objects (EDA266, EDA269)

| What | Result | Where |
|---|---|---|
| Bed face demoted to an object face; north wall inferred behind it | gap28: wall inferred **0.42 m** behind the face (human: 0.42). Over 12 recorded office worlds the bed face is the only line ever demoted | EDA266 §Results, §Does it generalise |
| Room now contains the murphy bed / slim bookshelf (full1) | 2/4 → 4/4 and 3/4 → 4/4. Bed belief certainty 0.29 → 0.57; bookshelf contested → confirmed (its returns are no longer stripped as wall) | EDA266 §Results, §The object loop |
| Hidden wall is honest about what it is | an outline piece of kind `hidden`, status `inferred`, counted as a gap until measured. Unresolved perimeter goes **up** by 1.2–1.4 m | EDA266 §Not solved |
| Side-panel wall markers | **negative result** on office data. A panel is seen in 4 of 12 worlds by one station each, and every scan line runs onto the floor before the panel ends. Panels give lower bounds only | EDA269 §(a) |
| NW diagonal wall with the door open | gap28 outline runs west wall → SW frame → doorway → hidden north wall. The closet behind the door leaves the outline (human question D-00012) | EDA269 §(b) |
| Fair reference score | the locked reference map also takes the bed face for a wall. Reported with and without that stretch | EDA269 §(c) |

Where only low returns place it, the hidden wall stays 12–17 cm short (P-00180, P-00185).

## Large objects (EDA267, EDA272)

| What | Result | Where |
|---|---|---|
| Desk model: front edge parallel to its wall; runs joined across gaps hidden from every station | full1 desk worst-dimension error **0.231 → 0.084 m** (after review fixes); gap28 0.094 → 0.094; desk still ~8 cm short | EDA267 §Re-measured |
| One detection = one instance (mask bleed) | duplicate office chair gone on both worlds; one real 'box' (hay bag) lost to the bleed rule | EDA267 §(c) |
| Certainty = geometry × class (LiDAR stations with ≥ 20 returns × camera share) | confirmed 6/15 → 8/14 (full1), 2/11 → 3/12 (gap28); 5 wrong one-camera confirmations blocked on gap28 | EDA267 §(d), §What the review fixes changed |
| Two-level outline (cuboid + measured detail with per-face provenance) | on every belief; the gallery draws the measured box | EDA267 §(a) |
| Relocalisation of movable classes | **unit tests only**: no recorded world has a moved object (P-00192) | EDA267 §Still open |
| Labels must fit their size in metres; cross-class duplicates merged | full2 failed checks **13 → 9**, murphy bed recovered (depth error 0.03 m), 'computer' beliefs 5 → 3. No regression on full1 / gap28 | EDA272 §Headline |

## Identification (EDA268, EDA271)

| What | Result | Where |
|---|---|---|
| Room vocabulary v2 (litter box, computer tower, vacuum / mop, air purifier + distractors) | full1: PC tower and litter box now named right. Wrong classes asserted without a flag: full1 4/13 → 1/15, gap28 6/11 → 0/11 | EDA268 §Finding 1–2 |
| `id_check` per belief (size + view votes + re-ask on crops) | **size is the only check that caught errors without ever doubting a right object**; the re-ask over-doubts (P-00201) and is opt-in live | EDA268 §Finding 3, §Round 1b |
| Answers change beliefs (`yes`/class = override, `no` = reject + re-open) | agent answered 14 sheet items from crops; gap28 beliefs 12 → 10 (chair parts merged); truth checks unchanged on all three worlds | EDA271 §Finding 1–2 |
| Doubt drives a look from a new bearing (≥ 45° off) | id looks for 4 of 7 (gap28) and 2 of 3 (full1) doubtful beliefs; the rest sit against walls with no free spot. Never moved the rover | EDA271 §Finding 3 |

Still open: size cannot tell an air purifier from a PC tower (P-00232). There is no "not an object" answer (P-00221).
The white cylinder's class is disputed between the builder (air purifier) and the human's earlier acceptance (trash
can). It is not scored until D-00011 is answered.

## Reach (EDA270)

A station is now valid when the moves of its own visit fit: arrival, a face turn as far as it fits, a turn back, and a
reverse of at most 0.30 m along the arrival line. The old rule needed a full 360° turn. Valid candidates rise
**325 → 458 (full1)** and **326 → 394 (full2)**, with 0 lost. On the real drive-posture returns, 44/47 and 22/29 new
spots pass. The limit has moved: 82–87 % of refusals are now "no verified path", caused by keep-out footprints and the
hard zone round unknown floor (P-00217). The run ends are not fixed. No round reports the drivable-area number the human
asked for in process (4).

## Cross-cutting lessons

- **Check the yardstick before the method.** The replay baseline was silently wrong (no floor plan), and EDA272's
  "held-out" world was used for tuning. Both were caught and stated in the FINDINGS. Both change how far the numbers
  can be trusted.
- **Walls and objects are coupled.** Once the bed face stopped being a wall, the bed and bookshelf beliefs improved
  without any extra work (EDA266 §The object loop). The reverse also held: with the current outline, the bed face read
  as a wall and the labeller stripped its points (P-00195).
- **Cheap physical checks beat learned re-asks** for identity. The size test never doubted a right object. The crop
  re-ask did.
- **Negative results are recorded** (side panels, EDA269 §(a)) rather than tuned away.
- **All offline.** Every FINDINGS ends with the live test that would settle it. Those are the next rover work.

## Open questions / stale flags

- The human's full report at the end of the rounds was not found in the repo on 2026-10-21 (librarian).
- The live runs office-full1 and office-full2 (2026-10-21) have no diary entry of their own.
- Human questions D-00011 (office truth: PC tower, duplicates, cylinder, litter boxes, who answers ID questions) and
  D-00012 (does the closet count as room).
