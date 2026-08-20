# Perimeter-capture recipe — for clean room-SHAPE recovery

**Why this exists.** EDA054 proved that the recovered floor-plan *shape* depends on the **capture path** as much as the sensor: a sweep that **loops through the room interior** makes a *multi-lobe* free-space region → the shape extractor traces a complex over-segmented outline (the corridor's 14 "walls"). A **perimeter-tracing** sweep makes a *single-lobe* free region → a clean wall ring. This recipe is the capture protocol that gives the shape method its best chance — and it costs nothing (existing SVPRO camera, no LiDAR needed). It applies equally to a future 2D-LiDAR pass.

## The path: ONE smooth loop around the perimeter
- **Trace the perimeter, don't cross the interior.** Walk a single continuous loop ~1–1.5 m from the walls, keeping the room's interior consistently on one side. Do **not** loop back through the middle or criss-cross — that's what creates the multi-lobe free region.
- **Close the loop** — end where you started, so hloc closes it → drift-free poses.
- **Slow + smooth** — each wall section should be seen over several frames; avoid motion blur.

## The aim: face the walls, catch the floor–wall junction
- Point the camera **outward at the wall you're passing** (not at the floor, not the ceiling, not across the room), angled **slightly down** so it catches the **floor–wall junction** — that base line is the cleanest wall evidence.
- **Pause and pan slowly at every corner** so *both* adjoining walls are captured in the same pass — corners are where the topology is defined; a rushed corner becomes ambiguous.

## Capture every structural element
- **Cut-ins / alcoves / niches:** trace *into and along* their faces — don't skip past a niche or it gets smoothed into a straight wall.
- **Doors / openings:** pass each opening and **pause facing it** so the camera sees *through* it (free space flows through → the door detector fires) — but **don't walk through** into the next room; keep the loop inside the target room.
- **Don't skip a wall** — every wall needs at least one frontal view; an unseen wall falls back to a low-confidence "prior" placeholder.

## Texture / exposure
- Watch the live **ORB feature-count gauge** in `record_sequence.py`; pan across textured features. Blank walls starve it — the **$30 red speckle projector ON** helps there (and the floor–wall junction is textured regardless).
- Blur-fighting exposure in a lit room: `--exposure 5000 --gain 200`, tune live with `-/=` and `[/]`.

## Commands
```bash
# 1) record one perimeter loop (live ORB gauge; q=stop, space=pause, -/= exposure, [/] gain):
python3 src/slam/record_sequence.py --name <room>_perimeter --exposure 5000 --gain 200 --fps 10
# 2) rectify/ingest:
python3 src/slam/make_kitti_dataset.py data/slam/<room>_perimeter
```
Then re-run the shape method (EDA053/054 pipeline) on the new sweep — a single-lobe free region should give a clean wall count without algorithm changes.

## Validation expectation
A perimeter sweep of the corridor should collapse its over-segmented count toward the real ~4–8 walls (the EDA054 residual was capture-geometry, not algorithm). If it doesn't, the remaining residual is the ±0.6 m passive depth (→ the 2D-LiDAR, D-00002), but the *shape/topology* should already be right.

## Source

EDA054 (capture-path → free-space-topology finding), 2026-06-10.

## Related

[[room-shape-topology-methods]] · [[floor-map-sensing-options]] · [[anchor-map-protocol]] · [[lidar-multiscan-capture-recipe]]
