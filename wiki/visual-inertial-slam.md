# Visual-Inertial SLAM

TUM/Imperial paper (arXiv 2403.09596) demonstrates large-scale outdoor forest MAV autonomy using only stereo cameras + IMU — no LiDAR, no GNSS, all compute onboard (*demoed*). Direct counter to [[lidar-for-uav-autonomy]]'s thesis that LiDAR is necessary for high-speed GPS-denied flight; authors acknowledge LiDAR "superior performance" on depth but argue the cost/weight/scalability tradeoff favors vision in forest environments. Feeds the vision camp in [[lidar-vs-vision-autonomy]].

## Sensor Configuration

- **Stereo depth**: Intel RealSense D455 IR stereo + IMU. No [[lidar-for-uav-autonomy|LiDAR]] (weight/cost/power ruled out), no GNSS (forest canopy occlusion).
- **Depth method**: fine-tuned CNN for stereo matching — standard stereo matching fails outdoors at range. Depth capped at 6.5 m (vs LiDAR tens-to-hundreds of metres; *claimed* limitation).
- Depth inference: 217 ms/frame (5 Hz) — the compute bottleneck for the full pipeline.

## Pipeline

**State estimation** — OKVIS2 VI-SLAM running at 15 Hz, sliding-window optimization with loop closure.

**Mapping** — supereight2 octree submaps keyed to keyframes; submaps deform elastically with state updates on loop closure. Novel contribution: *trajectory anchoring* — elastic weighted deformation propagation that keeps the global map consistent after loop closure without rigid re-integration.

**Planning** — Informed RRT* over the covisibility graph built from active keyframes.

## Results

**Real forest** (467 trees/ha density):
- 226 m mission length, <0.5% drift, peak 4 m/s, 0 collisions.

**Simulation** (varying forest density):
- 12/12 collision-free missions, up to 2363 m trajectories.

**Mission completion comparison** (trajectory anchoring vs baselines):
- Trajectory anchoring: 95%
- Rigid correction: 75%
- No loop closure: 40%

**Compute**: Jetson Orin NX 16 GB, fully onboard. SLAM runs decoupled at 15 Hz; depth CNN at 5 Hz is the binding constraint.

## Limitations vs LiDAR

Authors' own *claimed* concessions:
- Vision SLAM drift is spatially non-constant (LiDAR loop-correction is geometrically simpler and more precise).
- 6.5 m effective depth range vs LiDAR's long range — matters for obstacle lookahead at higher speeds.
- Depth inference is the compute bottleneck; LiDAR point clouds arrive at higher frequency without GPU inference.
- State-of-the-art autonomous forest flight "typically relies on LiDAR" — this paper's explicit framing of its own novelty.

## Source
- `raw/research/autonomy-and-sensors/03-vislam-no-lidar.md` — arXiv 2403.09596 (TUM/Imperial), stereo+IMU-only forest MAV autonomy, no LiDAR/GNSS

## Related
- [[slam]] — overview hub: localization + mapping + loop-closure decomposition, VIO vs LIO
- [[lidar-for-uav-autonomy]] — direct counterpart; HKU MaRS Lab argues LiDAR is necessary
- [[event-cameras]] — alternative sensing for high-speed/low-light where stereo depth fails
- [[lidar-vs-vision-autonomy]] — debate page this paper feeds
- [[drone-sensors-for-autonomy]] — cross-sensor SWaP and capability comparison
- [[drone-autonomy-state]] — deployment maturity context
