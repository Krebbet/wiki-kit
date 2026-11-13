# Walls seated on their own hits (drone-prototype EDA357)

How the rover's floor-plan walls drifted 3.5–8 cm outward, and the fix that puts each wall line back on the returns
that support it. The pattern applies to any occupancy-grid → RANSAC-line floor plan: a grid that only ever marks
cells occupied, never frees them behind a wall, will spill outward, and a merge that keeps the outermost line turns
the spill into a ratchet. **Status: merged (PR #281, 2026-11-13), switch `mapping.seat_walls` default ON
(`DRONE_SEAT_WALLS=0` reverts). Offline on scratch copies of 8 recorded worlds, all in one office. Not yet run in a
second room (P-01360).**

## Source

drone-prototype repo, master:
- `eda/EDA357-wall-ratchet/FINDINGS.md`; diary entry 2026-11-12 "walls sit on their own hits"
- `src/drone/agent/floorplan.py` (`FloorPlanTask._seat`, `_seat_bins`, `_seat_fit`); `config/mapping.json`
- parked P-01255 (the symptom, now resolved), P-01360…P-01367 (what is still open)

## The mechanism (traced, not guessed)

1. Nothing frees a cell behind a wall, so each wall's occupied band spills outward over the stations.
2. RANSAC fits the spill as short lines 4.5–6 cm behind the true wall.
3. `_merge_duplicates` kept the OUTERMOST of two near-parallel lines.

So every outward merge left the wall 3.5–8 cm outside all of its stations' returns (4 to 35 stations per wall).
Unmerged walls sat at 0–2 cm. Pose error and the LiDAR lever were ruled out. A visible symptom: large-object "bodies"
chained along the east wall were really wall returns (P-01255).

## The fix

- The merge keeps the best-supported line, not the outermost.
- `_seat` moves each boundary line (offset and angle) onto the station-weighted robust centre of its supporting cells.
  It picks the outermost straight surface with ≥ 0.5 m support and records the uncertainty.
- A recess guard (review B2): an enclosed outer surface needs ≥ 50 % of the station-weighted support. Without it a
  mid-wall recess ≥ 0.5 m moved a whole wall out.

## Evidence: independent first, self-scored second

| check | before | after | kind |
|---|---|---|---|
| agreement with the locked September map | 2.4–7.7 cm | ≤ 1.2 cm on all 8 worlds (4 held out) | **independent** |
| bodies hugging the September map's walls | 7, 9, 9, 5, 5 | 1, 2–3, 0, 0 | **independent** |
| per-station worst wall offset | 2.8–8.0 cm | ≤ 0.8 cm | self-scored (same returns the seat used) |
| bodies hugging the seated walls | 5–8 | 0 | self-scored |

The review (PR #281 B1) caught the self-scored rows being quoted as the headline. Read the independent rows first.
Outlines stayed closed; drivable area moved ±0.05 m².

## Open

- One room only; the hallway run is the generalisation test (P-01360).
- Bank cuboids of the litter box and vacuum reach ~9 cm behind the seated walls (P-01361).
- A face 4–6 cm in front of a wall can become one slanted RANSAC line (P-01362); RANSAC fits unweighted cells (P-01365).
- The NW doorway frames are found or missed by the RANSAC seed, before and after (P-01364).

## Related

- [[lidar-floorplan-extraction]] · [[room-segmentation-floor-plan]] · [[stop-and-scan-room-mapping]]
- [[global-alignment-wall-refinement]] (retired June approach to the same "two parallel bands" symptom)
- [[incremental-large-object-update]] (the bodies that hugged the walls)
