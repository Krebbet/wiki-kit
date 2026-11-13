# Starting in an unmapped room: the room as a parameter (drone-prototype EDA362, + PR #294)

What it took to let the rover start in a room it has no map of, after every part of the stack had quietly assumed
"the office". **Status: merged (PR #290 and the follow-up PR #294, 2026-11-13). Offline only: sim rig, recorded
office episodes replayed as if unmapped, scratch roots. Never run end to end on the rover (P-01449). The first
hallway run is the test (drone-prototype `docs/next-run-plan.md` §4). The relaxed acceptance rule `prior_room` is a
human decision still pending (P-01445).**

## Source

drone-prototype repo, master:
- `eda/EDA362-new-room/FINDINGS.md`; diary entries 2026-11-13 "the room as a parameter" and "the visual triggers and every bank reader filter by room AND frame"
- `config/rooms.json`, `src/drone/rooms.py` (README rule 27; `record_frame` / `record_in`), `drone/nav/roommap.LiveRoomMap`
- `tests/test_rooms_eda362.py`, `tests/test_vtrigger_frame.py`; parked P-01440…P-01449, P-01480…P-01487

## The lesson: "office-named" was not the problem; "wrong elsewhere" was

34 office assumptions were traced. The live-path ones were wrong in any other room: the start always localised on
the office map; bank positions became keep-outs at the same coordinates in any room; sightings were stamped with the
office map; the visual triggers loaded every room's cuboids. The 11-12 "fresh" run had not re-mapped at all: all 341
relocalisations registered against the locked office map.

## The design

- **Room registry.** Every former office constant reads `config/rooms.json`. The office's live inputs are
  byte-identical to before (8 / 8 hashes).
- **New-room start.** The start capture is the origin. A live room map grows from the run's own fixes and is exported
  at the end, never locked automatically.
- **Records carry room AND frame.** One rule (`rooms.record_in`): no room = the default room; no frame stamp = its
  room's locked map; never a match when either frame is unknown. Safety readers (trigger cuboids, keep-outs) treat
  an unsaid frame as the locked map; agent readers stay lenient for old worlds (PR #294). Without the frame, an
  office record would "explain" a real obstacle at the same numbers in another room and suppress its stop.

## Evidence (replay, office only)

Three office runs replayed as if unmapped: a fix was accepted at every scored stop, but only the stops the September
map also fixed can be checked (218 / 20 / 25). On those: median 0.95 / 0.77 / 1.08 cm, max 5.6 cm, heading max 2.3°,
no drift trend. Unchecked fixes still grow the map. One run stalled after 2 scans because the strong-fix bar (180
correspondences) was calibrated on a dense 29-station map. Hence `prior_room`: on a run's own map only, also accept
the best unambiguous basin (rms ≤ 2 cm, ≥ 50 % of the scan). It is a relaxation of the human's fix rule, ON for
new-room runs only, pending the human.

## Open

No cross-room task or door link yet (P-01440, P-01444). The room map never forgets (P-01441). Corridor degeneracy
unmeasured (P-01442). The floor-plan raster is ±2.8 m about the origin, so start the hallway near its middle
(P-01443). The export is a raw map (P-01447).

## Related

- [[stop-and-scan-room-mapping]] · [[stop-and-go-navigation-on-a-locked-map]] · [[map-then-navigate]]
- [[relocalisation-far-check]] (new-room fixes pass it too) · [[room-segmentation-floor-plan]]
