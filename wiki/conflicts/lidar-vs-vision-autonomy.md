# Conflict: Is LiDAR necessary for drone autonomy, or do vision/event cameras suffice?

**Status: OPEN** (no user ruling; both camps documented from the founding `autonomy-and-sensors` corpus.)

The single dominant contested claim across the autonomy-and-sensors corpus. It is not a strawman — there is strong, recent, credible evidence on both sides, and the disagreement is partly real and partly a scope dispute (mission regime).

## Position A — LiDAR is the superior/necessary enabling sensor

- **`01-lidar-uav-survey.md`** (HKU MaRS Lab, 2025, authors of FAST-LIO): camera depth (Intel D435i 3–5 m) is *categorically inferior* to LiDAR (tens–hundreds of m) for high-speed obstacle avoidance; cameras suffer motion blur on self-rotating UAVs where LiDAR does not — PULSAR cited as the only successful autonomous self-rotating UAV. Frames vision-based SAR/delivery as a *gap to be corrected*, not evidence of vision sufficiency. See [[lidar-for-uav-autonomy]].
- Strongest where: long range, high speed, GNSS-denied mapping, lighting-independence, thin-obstacle (wire) detection.

## Position B — vision/event cameras suffice (and win on SWaP/cost)

- **`03-vislam-no-lidar.md`** (TUM/Imperial): explicitly "state-of-the-art autonomous drone flying in forests typically relies on LiDAR," then *demonstrates* large-scale outdoor forest autonomy with only stereo + IMU, fully onboard, 0 collisions (1 real mission + 12/12 sim). Concedes LiDAR is superior on depth but argues cost/weight/scalability. See [[visual-inertial-slam]].
- **`02/06/07/13` (ETH RPG / Scaramuzza cluster):** event cameras give µs latency, >120 dB dynamic range, near-zero motion blur at ~0.5 W; demoed 3.5 ms dodging, 9.8 m/s cluttered flight, low-light flight to 10 lux. Explicit anti-LiDAR stance for agile/dynamic flight: *"LiDARs and RGB cameras do not provide sufficient information to quickly and precisely react in a highly dynamic environment."* See [[eth-rpg-scaramuzza]], [[event-cameras]], [[event-cameras-for-uavs]].
- **`08-skydio-autonomy-intro.md`:** a *commercially shipping* vision-only (6-camera, no LiDAR) autonomy product — an existence proof for consumer/prosumer regimes (vendor claim, 2020). See [[skydio-autonomy-stack]].
- **`weekly-2026-05-17/01-dream-to-fly.md`** (ETH RPG, ICRA 2026): DreamerV3 model-based RL, raw 64×64 RGB pixels → control, **no LiDAR/depth/VIO**, agile gate flight ≤9 m/s with real-quadrotor dynamics (HIL). Strong Position-B — *asterisk:* real-world runs use rendered images, not a real camera feed, so the real-optics gap is unresolved. See [[dream-to-fly]].

## Where the camps actually agree *(synthesis)*

The disagreement narrows once mission regime is fixed — it is closer to a scope dispute than a contradiction:

- **LiDAR wins:** long-range sensing, mapping-heavy missions, lighting-independence, self-rotating/aggressive platforms, safety-critical thin-obstacle detection.
- **Vision/event wins:** SWaP-constrained and cost-sensitive platforms, agile low-latency reaction, GNSS-denied where weight matters, consumer/prosumer unit economics.
- Both concede the other's strong regime. The genuinely contested middle is **high-speed obstacle avoidance in unstructured outdoor environments**, where 01 says vision's depth range is disqualifying and 03 + the RPG work say it is not.

## Commercial home robots — additional evidence *(from [[commercial-home-robots-perception]])*

The commercial home robot field (2021–2025) shows the same split at product level:

- **Vision-only camp (Position B):** Dyson 360 Vis Nav (fisheye-only SLAM, shipping), Matic (5-camera no-IMU/LiDAR, Jetson Orin 4GB, shipping). Both successful for the indoor slow-navigation regime.
- **LiDAR camp (Position A):** Samsung Ballie (spatial LiDAR, not yet shipped), Bear Robotics Servi (LiDAR+cameras, shipping commercially in restaurants).
- **Undisclosed:** Amazon Astro (V-SLAM confirmed, sensor modalities undisclosed).

Neither camp has a decisive commercial win in home robots. The indoor slow-navigation regime (< 0.5 m/s, structured home environment) is distinctly easier than high-speed outdoor avoidance — Vision-only *works* here (Dyson, Matic), but this doesn't resolve the contested outdoor/high-speed middle.

## What would resolve it

- A head-to-head benchmark on the contested middle (high-speed outdoor avoidance) with matched platforms.
- Evidence on unit economics at commercial scale (does LiDAR's cost/weight actually block deployment, or has solid-state LiDAR closed the gap? — `01` notes Livox MID360 at ~265 g/$700).
- A user ruling, or more sources, to move this from `open` to resolved.

## Source

- `raw/research/autonomy-and-sensors/01-lidar-uav-survey.md` — Position A
- `raw/research/autonomy-and-sensors/03-vislam-no-lidar.md` — Position B (vision)
- `raw/research/autonomy-and-sensors/02-event-camera-survey.md` — Position B (event)
- `raw/research/autonomy-and-sensors/06-event-vision-uav-review.md` — Position B (event/UAV)
- `raw/research/autonomy-and-sensors/07-rpg-event-research.md` — Position B (RPG)
- `raw/research/autonomy-and-sensors/13-scaramuzza-iccp2024.md` — Position B (RPG keynote)
- `raw/research/autonomy-and-sensors/08-skydio-autonomy-intro.md` — Position B (commercial, vendor)

## Related

- [[lidar-for-uav-autonomy]] · [[visual-inertial-slam]] · [[event-cameras]] · [[event-cameras-for-uavs]] · [[eth-rpg-scaramuzza]] · [[skydio-autonomy-stack]]
- [[drone-sensors-for-autonomy]] · [[drone-autonomy-state]] — where this tension propagates
- [[commercial-home-robots-perception]] — commercial evidence for both camps in the home robot domain (2021–2025)
