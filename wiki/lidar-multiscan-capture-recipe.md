# Multi-position LiDAR capture for floor-plan ring closure

How to capture a 2D LiDAR floor scan from **2–3 positions** in a room so the partial single-viewpoint
scans can be **registered and merged into a closed wall ring**. This is the operating procedure behind the
EDA058 multi-scan registrar; do this for any room where one static scan leaves walls occluded (i.e. most
rooms).

## Why multi-position (the finding)

A single static 2D LiDAR scan gives **crisp** wall lines — 0.2–0.5 cm inlier band, texture-independent —
which removed the passive-stereo campaign's ±15 cm data bottleneck (EDA057). But from one standing spot you
only see the walls **not occluded from that spot**: EDA057's corridor scan (operator in the room centre,
surrounded by furniture) saw **2 of ~6 walls and 0 corners**; the kitchen saw an L-corner + 2 fragments.
The remaining limit is **coverage**, not data quality — and the fix is a **move**: capture from a second
(third) position and align the scans on their crisp wall constraints.

EDA058 validated that this alignment **mechanically works**: registering two partial scans on matched-wall
orientation + offset recovers the relative pose to **sub-degree / sub-cm**, and merging re-closes a fuller
ring without smearing the lines. The one requirement the capture must satisfy is **constrained overlap**
(below).

## The command

```
python3 src/slam/lidar_capture.py --multi 3 --out data/slam/lidar/<room>_multi
```

This captures from N positions, prompting `MOVE the sensor to position k ... press Enter` between each, and
saves `<room>_multi_pos0.npz`, `_pos1.npz`, ... (each with its own `.csv` + top-down `.png`). Then register
+ merge with `eda/EDA058-lidar-multiscan/lidar_multiscan.py`. (Single capture is still the default with no
`--multi`.) Remember the port must be readable: `sudo chmod a+rw /dev/ttyUSB0` (C1 @ 460800).

## The recipe (rules that make registration succeed)

1. **2–3 positions per room, chosen so every wall is seen end-to-end from *somewhere*.** A wall that is
   only ever seen in a near fragment (or always occluded) cannot be recovered full-length. Pick positions
   that between them give each wall a clear, end-to-end line of sight — typically near opposite corners /
   diagonal ends of the room, not all clustered in one area.
2. **Keep overlap — each new position MUST re-see ≥2 NON-PARALLEL walls already seen from a prior
   position.** This is the hard constraint. Registration solves rotation + 2D translation from matched
   walls; **two non-parallel shared walls fully pin the transform** (rank 2). If the only shared walls are
   parallel (e.g. two positions along a corridor both seeing just the two side walls), the translation
   **along** the walls is **unobservable** — the scans cannot be locked together along that axis (EDA058
   §3c). So always make sure each consecutive pair of positions shares a *corner* or two walls at an angle.
3. **Avoid standing dead-centre surrounded by furniture.** The operator's own body + nearby furniture
   occlude the walls behind them; from the room centre you often see only near wall stretches and no
   corners (EDA057 corridor). Stand **off-centre, ideally near a corner**, so two long walls are seen
   end-to-end and meet in a confirmed corner (EDA057 kitchen showed this works).
4. **Sensor at a steady, constant height** across all positions (the scan is a single horizontal plane;
   changing height changes which surfaces — skirting, table edges, shelf fronts — the plane intersects, and
   that breaks wall correspondence). Hold it level; a tripod / fixed mount is ideal.
5. **Keep each capture static** (a few seconds, ~20 revolutions overlaid → dense, sub-cm walls). Don't move
   the sensor *during* a capture; move *between* captures.
6. **Small, simple moves between positions.** A near-square room has a ±90° registration ambiguity that the
   registrar flags but cannot fully resolve from geometry alone (EDA058 §3a); a small, roughly-known
   rotation between positions keeps you on the correct branch.

## Quick checklist

- [ ] Each wall seen end-to-end from at least one position.
- [ ] Each consecutive position pair shares **≥2 non-parallel** walls (a corner).
- [ ] Off-centre / near-corner stances, not room-centre-surrounded-by-furniture.
- [ ] Constant sensor height, held level, static per capture.

## Source

- EDA057 (`eda/EDA057-lidar-floorshape/eda-findings.md`) — single static scan gives sub-cm walls but a
  partial ring (coverage limit).
- EDA058 (`eda/EDA058-lidar-multiscan/eda-findings.md`) — wall-constraint registration + merge mechanics
  validated (sub-degree / sub-cm); the constrained-overlap requirement comes from its §3b/§3c.

## Related

[[2d-lidar-slam]] · [[anchor-map-protocol]] · [[home-tidy-drone-prototype]] · [[perimeter-capture-recipe]]
