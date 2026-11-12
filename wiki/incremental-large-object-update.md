# Incremental large-object update under a memory cap (drone-prototype EDA353)

How the rover's large-object identification was made to fit a 1.5 GB process cap. Detection is open-vocabulary DINO +
SAM, voted into 2 cm voxels across camera frames and carved by LiDAR free space. The fix changes the update from
recomputing over the full history at every station to an incremental fold of only the new observation. The pattern is
general: any multi-view voxel-voting step whose state grows with station count can be kept bounded this way. **Status:
replay-verified only; PR #277 is in a review fix round on 2026-11-12, so the numbers may still move. It has not run
live (P-01257).**

## Source

drone-prototype repo, branch `eda353-object-identification` (PR #277, open):
- `eda/EDA353-object-identification/FINDINGS.md` "Answer first", §1 (where the memory went), §2 (what changed)
- `src/drone/agent/largeobj/incremental.py`, `largeobj/models.py --serve` (on the branch)
- parked P-00150, P-01015 (resolved in replay on that branch), P-01250…P-01259

## The diagnosis: one function, not the model

The update was OOM-killed from station ~35 on office-cont1. Stage-by-stage RSS sampling put almost all of it in one
place: `shape.free_voxels` built every (voxel, ray) pair of every observation at once, as a python dict of tuples. It
reached 1.3 GB at station 20. Label voting was 149 MB. Two hidden costs also came out of the profile: an ID check that
spent 195 s of a 199 s update re-deriving points, and a floor-plan rebuild with 2.2 M percentile calls.

## The method

| piece | full recompute (before) | incremental (after) |
|---|---|---|
| free-space counts | every ray at once (dict of tuples) | built 60 k rays at a time (exact: a ray counts once per voxel); kept per observation; summed as sorted int64 keys |
| class votes | every voxel against every frame, every station | kept; a new observation adds its voxels, old frames vote only on new voxels, new frames vote on all |
| occlusion | occluder cloud re-projected per frame per belief | each frame's depth buffer kept (a min, so new returns fold in exactly) |
| frame masks | all in memory | bit-packed per observation, loaded only for frames holding the object's class |
| detector | new process per vocabulary per station (~2 GB, ~8 s load each) | one long-lived worker, loaded once, 480 px input (0.96 GB peak) |
| bounds | 4 GB scope, 1200 s | 1200 MB / 120 s per update, ≤ 4 observations folded per update, a detection backlog; every wait polls the soft stop |

**The measured result (replay):** 95 office-cont1 stations, peak 443 MB, median 9.9 s per station. Before: 1319 MB at
k = 20, then OOM-killed. 51 office-fresh1 stations, peak 266 MB. Soft stop 0.13–0.35 s with an ingest in flight.

## What the incremental form gives up (P-01250, P-01253)

- A frame-voxel pair is voted once, with the occluders known at that time. A later occluder does not un-vote it.
- Memory is bounded, but time still grows linearly with the station count (rays, frames, ID-check views).
- Detection costs ~29 s per observation (median; 82 s max) on 2 CPU threads, at a resolution not measured against labels (P-01251, P-01252).

## Related

- [[point-cloud-object-segmentation-models]] · [[ov3d-instance-seg]] · [[3d-shape-completion-for-object-footprints]]
- [[object-certainty-model]] · [[semantic-object-memory]]
- [[stop-and-scan-room-mapping]]: the station-by-station capture this update runs after
