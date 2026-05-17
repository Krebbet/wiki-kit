# Event Cameras

Per-pixel asynchronous sensors that emit ⟨x, y, polarity, timestamp⟩ events on luminance change rather than capturing full frames at fixed intervals. The 2024 survey (arXiv 2408.13627, ASU/UPenn/UMD) characterizes their advantages as high temporal resolution, extreme dynamic range, low latency, and near-zero motion blur — properties that make them attractive for high-speed and low-light robotics where frame cameras fail. Commercial hardware is now field-grade for automotive applications; drone deployment remains largely research-stage. See [[event-cameras-for-uavs]] for the UAV-specific application taxonomy.

## Core Specifications

All figures *demoed* unless noted:

| Property | Event cameras | Frame cameras |
|---|---|---|
| Temporal resolution | >10,000 equiv. fps | typically 30–240 fps |
| Latency | <1 ms (iniVation) to 100–220 µs (Prophesee) | >1 ms |
| Dynamic range | >120 dB | ≤95 dB |
| Low-light threshold | 0.05–0.08 lux | much higher |
| Power | as low as 0.5 W (Prophesee EVK4 HD) | varies |

## Algorithm Families

All *demoed* in research settings:

- **Spiking/recurrent architectures** — RVT (Recurrent Vision Transformer), STNet
- **Graph networks** — AEGNN (Asynchronous Graph-based Neural Nets for Events)
- **Contrast maximization** — ego-motion estimation from event streams
- **Optical flow** — EV-FlowNet
- **Fusion** — event+IMU, event+frame (EFNet), event+[[lidar-for-uav-autonomy|LiDAR]]; treated as complementary rather than competitive for [[lidar-vs-vision-autonomy]], though LiDAR may be redundant on tight-SWaP drones

## Hardware Landscape

*Shipping at scale* as sensors; full onboard compute integration is nascent:

- **iniVation** — DVXplorer, DAVIS346 (events + frame), DVXplorer S Duo (onboard Jetson Nano — only unit with integrated compute)
- **Prophesee** — EVK4 HD (1280×720, 0.5 W), GenX320 (36 µW)
- **Lucid, Celepixel CeleX5, Insightness** — niche/industrial variants

Most sensors require an external host GPU or CPU for real-time processing. The DVXplorer S Duo is the only shipping unit with onboard compute.

## Simulation and Datasets

Simulators are mature: ESIM, v2e, CARLA-DVS. Automotive datasets are field-grade; drone-specific datasets are mapped in [[event-cameras-for-uavs]]. No standardized benchmark metric yet exists across the field.

## Maturity Assessment

Almost entirely research/lab for robotics. Automotive (ADAS) is the leading commercial application. Drone deployment requires further SWaP reduction and onboard inference hardware. See [[drone-sensors-for-autonomy]] for cross-sensor SWaP comparison.

## Source
- `raw/research/autonomy-and-sensors/02-event-camera-survey.md` — 2024 general event-camera survey (arXiv 2408.13627, ASU/UPenn/UMD) covering physics, hardware, and algorithm families

## Related
- [[event-cameras-for-uavs]] — UAV-specific application taxonomy, datasets, neuromorphic results
- [[eth-rpg-scaramuzza]] — dominant research lab; most demoed UAV results originate here
- [[visual-inertial-slam]] — frame+IMU baseline that event cameras aim to outperform in degraded conditions
- [[drone-sensors-for-autonomy]] — SWaP and capability comparison across sensor modalities
- [[lidar-vs-vision-autonomy]] — debate on whether event cameras can displace LiDAR for agile flight
