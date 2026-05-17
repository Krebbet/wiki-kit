# Nano-Drone Compute

Conventional ultra-low-power RISC-V multicore (PULP/GAP family) fits DNN inference into <1–3.5% of a nano-drone's power budget without neuromorphic hardware. A generational lineage from ETH Zürich/Bologna — PULP-Dronet → PULP-Frontnet → GAP9Shield — demonstrates closed-loop onboard AI on a 27 g Crazyflie platform available as consumer/hobbyist COTS. This is the direct counterpoint to [[neuromorphic-computing-for-drones]]: the question is not capability but tradeoff.

## Platform Lineage

The three generations share the same Crazyflie 2.x airframe (~27 g) and PULP SoC philosophy: heterogeneous RISC-V multicore + hardware tiling + aggressive quantisation.

| Generation | Platform | SoC | AI Power | Rate | Task |
|---|---|---|---|---|---|
| PULP-Dronet (~2019) | Crazyflie 2.0 + PULP-Shield | GAP8 (8-core RISC-V) | 64–284 mW | 6–18 fps | Obstacle avoidance / DNN nav |
| PULP-Frontnet | Crazyflie 2.1 + AI-deck (4.4 g) | GAP8 | 8.6–86.6 mW | up to 134.7 fps | Human-relative pose CNN |
| GAP9Shield | Crazyflie 2.x + 6 g deck | GAP9 | <100 mW | 17 ms/frame YOLO | Object detect, SLAM, localisation |

### PULP-Dronet *demoed*

First fully-onboard closed-loop DNN navigation at nano scale. GAP8 8-core RISC-V with Fixed16 quantisation and AutoTiler memory tiling achieves 64 mW at 6 fps to 284 mW at 18 fps; camera adds 4–8 mW. Total drone draw ~7.6 W; motors alone ~7.3 W (~96%). Inference power is therefore 0.8–3.7% of total — endurance hit is dominated by added daughterboard weight, not AI power. 5.4× lower power than STM32H7 at equivalent throughput. Source: `01-nano-drone-dnn-engine.md`.

### PULP-Frontnet *demoed*

Same GAP8 + AI-deck (4.4 g add-on). Human-pose CNN quantised to 8-bit via DORY tiling: **134.7 fps at 86.6 mW**, 0.43 mJ/frame; power range 8.6–87 mW = **0.2–1.7% of ~5 W system**. Versus PULP-Dronet: 7.5× throughput at 32% of the power. Median position error 41 cm (vs 26 cm ideal); 100% task success over 18 runs. Same Benini/ETH-Bologna lineage. Source: `03-nano-uav-pose.md`.

### GAP9Shield *demoed*

6 g daughterboard replacing the AI-deck. GAP9 SoC: 150 GOPS, 330 µW/GOP, sleep 45 µW. Onboard tasks all stay under 100 mW: YOLO 17 ms/frame (1.59 mJ, ~94 mW), NanoSLAM 87.9 mW, MCL localisation 23 mW avg. Adds 5 MP colour camera, +20% RGB framerate, 20% lighter than AI-deck. Source: `02-gap9shield.md`.

## Key Thesis

Across all three generations, onboard AI consumes **<1–3.5% of total drone power** — well within the [[drone-power-budget]] — using only conventional quantised CNNs on RISC-V multicore. The Crazyflie + AI-deck/GAP9Shield stack is accessible COTS, making it the default hobbyist and research testbed for onboard-AI experimentation.

Neuromorphic paths (see [[neuromorphic-computing-for-drones]]) offer potential advantages in latency and event-driven efficiency but are not required to fit AI inference into nano-drone energy budgets. The practical question is task fit: frame-based cameras + DNN suffice for pose and obstacle tasks; [[event-cameras-for-uavs]] or neuromorphic become relevant when latency or bandwidth constraints tighten.

For SLAM specifically, GAP9Shield's NanoSLAM at 87.9 mW sits alongside conventional [[visual-inertial-slam]] pipelines — complementary rather than competing. Sensor modality choices are covered in [[drone-sensors-for-autonomy]]. Broader autonomy context: [[drone-autonomy-state]].

## Source
- `raw/research/onboard-ai-energy/01-nano-drone-dnn-engine.md` — PULP-Dronet: 64–284 mW GAP8 DNN nav on 27 g Crazyflie, first fully-onboard closed-loop demo
- `raw/research/onboard-ai-energy/03-nano-uav-pose.md` — PULP-Frontnet: 134.7 fps @ 86.6 mW human-pose CNN, 8-bit DORY quantisation
- `raw/research/onboard-ai-energy/02-gap9shield.md` — GAP9Shield: 6 g deck, 150 GOPS GAP9, all tasks <100 mW including YOLO and NanoSLAM

## Related
- [[drone-power-budget]] — the budget nano-AI must fit within; these demos confirm <3.5% consumption
- [[neuromorphic-computing-for-drones]] — the contrasting hardware path; PULP-RISC-V shows it is not strictly necessary
- [[drone-autonomy-state]] — broader autonomy capability landscape
- [[drone-sensors-for-autonomy]] — sensor modalities that feed these inference pipelines
- [[visual-inertial-slam]] — SLAM approaches GAP9Shield's NanoSLAM complements
