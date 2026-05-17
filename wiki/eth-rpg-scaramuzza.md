# ETH/UZH RPG — Scaramuzza Lab

ETH Zurich / University of Zurich Robotics & Perception Group, PI Davide Scaramuzza — the dominant institution in event-camera drone research by publication volume and benchmark ownership. The lab argues an explicit vision/event-first position against LiDAR for agile and dynamic flight, feeding the vision camp in [[lidar-vs-vision-autonomy]]. Open-source releases and the UZH-FPV dataset anchor most downstream [[event-cameras-for-uavs]] work. Sources: RPG event research overview and Scaramuzza ICCP 2024 keynote.

## Demonstrated Results

**Dynamic obstacle avoidance** — 3.5 ms total latency, objects up to 10 m/s (*demoed*, Science Robotics 2020).

**Monocular event-only static-obstacle avoidance** — counterintuitively, higher flight speed yields better avoidance performance due to richer event stream (*demoed*, CoRL 2024).

**Cluttered high-speed flight** — 9.8 m/s with single event camera via imitation learning (*demoed*).

**Attitude tracking** — >1600 deg/s, 1 kHz estimator, 12 ms end-to-end latency (*demoed*, ICRA 2020).

**Ultimate SLAM** — events + frames + IMU fusion (RA-L 2018): +130% trajectory accuracy over event-only, +85% over frame-only [[visual-inertial-slam|VIO]] (*demoed*).

**RAMP-VO** — end-to-end learned visual odometry (*demoed*, IROS 2024).

**UZH-FPV racing dataset** — drone-racing benchmark with event + frame + IMU + GPS ground truth (*demoed*/released, ICRA 2019); canonical dataset for [[event-cameras-for-uavs]] VO evaluation.

**Legged robotics crossover** — quadruped catching ball at 15 m/s, 83% success rate, inference on Jetson Orin (*demoed*).

## Keynote Findings (ICCP 2024)

From Scaramuzza's ICCP 2024 keynote (*demoed* results):

- Event-camera SLAM remains stable at 10 lux illumination; standard-camera SLAM fails at 50 lux — a 5× lighting-tolerance advantage.
- Single-motor-failure recovery: event camera succeeds in dim lighting; standard camera fails.
- AI drone defeated 2 world-champion FPV pilots in 15 of 25 races — **important caveat**: that racer used frame cameras + deep reinforcement learning, not event cameras. The AI system subsequently failed when hangar lighting changed; Scaramuzza uses this as the central failure-mode motivator for event cameras.

## Commercial Landscape (from keynote)

- **iniVation / Samsung** — DAVIS346 and DVXplorer shipping.
- **Prophesee / Sony** — EVK4 HD shipping; Qualcomm smartphone integration deal (*claimed*).
- **Omnivision** — entering market.
- **Samsung SmartThings Vision** — $180 consumer event-camera product.
- **Apple** — 100+ event-camera patents filed since 2019 (*claimed*).
- **NASA JPL** — Mars 2030 lava-tube mission, event cameras in testing (*claimed, not confirmed*).

## Stated Limitations

Acknowledged by Scaramuzza: no absolute intensity output (frame-camera pairing required for texture); classical CV algorithms need adaptation for event streams; SNN sim-to-real gap remains open; cost still high pending a killer consumer application.

## Position on LiDAR

Explicitly anti-LiDAR for agile/dynamic flight: "LiDARs and RGB cameras do not provide sufficient information to quickly and precisely react in a highly dynamic environment." Contrast with [[lidar-for-uav-autonomy]] HKU MaRS Lab position.

## Source
- `raw/research/autonomy-and-sensors/07-rpg-event-research.md` — RPG lab event-camera research overview
- `raw/research/autonomy-and-sensors/13-scaramuzza-iccp2024.md` — Scaramuzza ICCP 2024 keynote notes

## Related
- [[event-cameras]] — sensor physics and hardware the lab builds on
- [[event-cameras-for-uavs]] — application taxonomy; RPG is dominant contributor
- [[visual-inertial-slam]] — Ultimate SLAM fuses events with conventional VIO
- [[lidar-vs-vision-autonomy]] — lab anchors the vision/event camp
- [[drone-autonomy-state]] — broader autonomy deployment context
