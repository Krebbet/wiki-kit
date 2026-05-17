# Neuromorphic Computing for Drones

Spiking neural networks (SNNs) running on neuromorphic hardware offer orders-of-magnitude lower energy-per-inference than GPU/CPU alternatives, making them the only plausible path to real autonomy on sub-30 g platforms where a Jetson Nano alone exceeds the airframe's total weight budget. The MAVLab group at TU Delft has provided the field's clearest through-line, from a 20 g stereo Delfly in 2013 to the first fully neuromorphic free-flying quadrotor in 2024. Despite compelling numbers, every published demonstration is still indoor, small-scale, and partial — honest limitations matter in a field prone to overclaiming.

---

## Why Neuromorphic on Drones

A 29 g Delfly needs ≈6 W total; a Jetson Nano weighs 85 g and draws 7.5 W — the conventional compute stack is heavier and hungrier than the drone itself. `[src:12-decroon-telluride2023]` SLAM algorithms require hundreds of MB of RAM; a typical nano-drone MCU has 192 KB. `[src:12-decroon-telluride2023]` See [[drone-power-budget]] for airframe-level energy budgets and [[nano-drone-compute]] for the conventional silicon baseline these numbers compare against.

Neuromorphic chips process sparse, event-driven spikes rather than dense frame tensors, so power scales with scene activity rather than frame rate — ideal for the low-light, high-speed, low-SNR conditions common in fast drone flight.

---

## The MAVLab Trajectory (2013–2024)

TU Delft MAVLab (Guido de Croon's group) is the principal research lineage; it is **distinct from ETH RPG** (Davide Scaramuzza) — see [[eth-rpg-scaramuzza]] for the Zurich lab's parallel autonomy work.

| Year | Milestone | Notes |
|------|-----------|-------|
| 2013 | 20 g Delfly stereo, FSM control | `[src:12-decroon-telluride2023]` |
| 2018 | First DVS-in-loop optic-flow divergence landing, 5 m/s | `[src:12-decroon-telluride2023]` |
| 2019 | STDP optic-flow SNN | Simulation only `[src:12-decroon-telluride2023]` |
| 2021 | Loihi "Luigi" 35-neuron controller in loop | `[src:08-mavlab-loihi-landing.md]` |
| 2024 | First fully neuromorphic vision→control on free-flying quadrotor | de Croon/Paredes-Vallés, *Science Robotics* `[src:04-fully-neuromorphic-flight]` |
| 2024 | SNN raw-IMU→motor attitude estimation | On Teensy 4.0, not neuromorphic HW `[src:05-neuromorphic-attitude]` |

---

## Hardware Case Studies

### Intel Loihi — MAVLab Quadrotor (2024)

The landmark result: a 5-layer ~28,800-neuron SNN for vision paired with a linear control layer, running on two Kapoho Bay Loihi chips with a DAVIS240C event camera. `[src:04-fully-neuromorphic-flight]`

**Measured numbers:**
- **27 µJ/inference** (canonical operating point; 7–20 µJ at slow/medium settings) `[src:04-fully-neuromorphic-flight]`
- Network marginal power: **7–12 mW** `[src:04-fully-neuromorphic-flight]`
- Real-flight loop rate: **200 Hz** (I/O-limited — USB between camera and chip is the bottleneck) `[src:04-fully-neuromorphic-flight]`
- Benchmark throughput: 274–1637 inf/s depending on sparsity `[src:04-fully-neuromorphic-flight]`
- Jetson Nano comparison: ~75,000–86,000 µJ/inference — **3–4 orders of magnitude more** per inference, 1–2 orders slower `[src:04-fully-neuromorphic-flight]`

> **Correction note:** The figure "~0.94 W" sometimes attributed to this system is Loihi board *idle* power, not inference cost. This corrects a secondhand figure that appeared on [[event-cameras-for-uavs]]. `[src:04-fully-neuromorphic-flight]`

**Honest limits:** indoor static environment only; no outdoor or ascent testing; controller is linear (not fully neuromorphic end-to-end — terminates at PX4 flight controller); no direct AER bus (USB I/O bottleneck caps 200 Hz); field-of-view constrained to 4×32×32-px corners by Loihi memory. High-contrast carpet required — untested on grass; crashes in near-dark. `[src:04-fully-neuromorphic-flight,12-decroon-telluride2023]`

### Intel Loihi — MAVLab Divergence Landing (2021, abstract only)

Dupeyroux/de Croon: first fully embedded Loihi in a flying robot; 35-neuron 3-layer SNN for optic-flow divergence landing. Sim↔Loihi RMSE 0.005 g thrust; 99.8%/99.7% spike match, bridging the sim-to-real gap. *Treat as corroborating data point — source available as abstract only.* `[src:08-mavlab-loihi-landing]`

### SNN Attitude Control on Conventional Silicon (2024)

De Croon/MAVLab ran a raw-IMU→motor SNN at **500 Hz** on a Teensy 4.0 ARM Cortex-M7. `[src:05-neuromorphic-attitude]`

- RMSE 3.03° (SNN) vs 2.67° (PID) — but the PID receives pre-computed attitude, making the comparison unfair to the SNN `[src:05-neuromorphic-attitude]`
- **No measured power**; estimated ~2.5× more operations than PID on conventional silicon `[src:05-neuromorphic-attitude]`
- **Key takeaway:** running SNN weights on a conventional MCU yields *no energy relief* at low-level control; the energy advantage only materialises when perception and control co-locate on a neuromorphic chip. Neuromorphic HW (Loihi) was too large for the 35 g frame — a hardware gap, not an algorithm failure. `[src:05-neuromorphic-attitude]`

### Kraken SoC — ColibriUAV

A purpose-built drone SoC integrating RISC-V, an SNE SNN accelerator, and a CUTIE ternary-DNN accelerator. `[src:06-colibriuav]`

- Full closed-loop event→PWM: **46.98 mW avg** (35.6 mW nominal) `[src:06-colibriuav]`
- SAER event interface: **7,200 effective frames/s at 10.7 mW** — roughly 100× lower power than USB-DVS (>1 W) `[src:06-colibriuav]`
- End-to-end latency: 163 ms (131 ms of that is unoptimised preprocessing) `[src:06-colibriuav]`
- **Limits:** demonstrated on a frame/testbed only — no flight test; SNN benchmark only, no navigation task; preprocessing latency dominates and is not yet optimised. Supersedes prior >1 W DVS-drone platforms on efficiency. `[src:06-colibriuav]`

### SynSense Speck — LENS (Ground Robot; Transfer Pending)

A DVS+SNN single chip (Speck) used for visual place recognition over an 8 km dataset replay on a **ground robot** — drone applicability is by technology transfer, not demonstrated. `[src:13-neuromorphic-localization]`

- **2.7 mW average**, 327 mJ total vs Jetson Nano 2,968 mJ (8.9×) and i7 61,427 mJ (188×) `[src:13-neuromorphic-localization]`
- 753 neurons / 44k params / 179 KB on-chip; Recall@1 0.88 vs 0.81 (SAD baseline) `[src:13-neuromorphic-localization]`
- Live on-robot testing limited to ~25–40 m of route `[src:13-neuromorphic-localization]`

This is the closest thing to a deployable neuromorphic localization chip; relevance to [[visual-inertial-slam]] on drones is speculative until airborne validation.

---

## SNN Families and Hardware Landscape

From the 2025 Purdue/Roy survey `[src:09-neuromorphic-robotic-vision-survey]`:

**SNN approaches:** leaky-integrate-and-fire (LIF), ANN→SNN conversion, surrogate-gradient training, and hybrids (Spike-FlowNet, Fusion-FlowNet, GNN-based).

**Chip landscape:** Intel Loihi/Loihi2, SpiNNaker, IBM TrueNorth, Tianjic, SynSense Speck; emerging NVM-based in-memory compute (NVM-IMC). See [[neuromorphic-materials]] for substrate-level developments.

> **Important:** The 2025 survey *explicitly declines* to publish a cross-chip energy-per-inference table. Any such table from secondary sources should be treated with caution. Numbers here are cited only from the primary experimental papers above. `[src:09-neuromorphic-robotic-vision-survey]`

---

## Maturity and Honest Limitations

| Limitation | Detail |
|-----------|--------|
| Indoor-only | All flight demonstrations to date; no outdoor, wind, or varied lighting `[src:04-fully-neuromorphic-flight,12-decroon-telluride2023]` |
| Degraded FOV | Loihi constraint forces 4×32×32-px corner features — not full-frame perception `[src:12-decroon-telluride2023]` |
| Controller underperforms PI | SNN attitude controller loses to PID/PI even in controlled conditions `[src:05-neuromorphic-attitude,12-decroon-telluride2023]` |
| No full sensor-to-actuator chain | State-of-the-art ends at PX4 or conventional motor driver; fully neuromorphic pipeline not closed `[src:04-fully-neuromorphic-flight]` |
| Hovering hard | No motion = no events from an event camera; hover is neuromorphically blind `[src:12-decroon-telluride2023]` |
| End-to-end RL "prohibitive" | De Croon's own assessment of on-chip RL training `[src:12-decroon-telluride2023]` |
| Toolchain/benchmark gaps | No standardised cross-platform benchmark; NeuroBench nascent; compiler/toolchain fragmentation `[src:09-neuromorphic-robotic-vision-survey]` |
| No demonstrated superiority in mainstream apps | Survey's honest conclusion `[src:09-neuromorphic-robotic-vision-survey]` |
| Jetson energy comparison caveat | de Croon flags the comparison "not fair" — different precision, task, and stack `[src:12-decroon-telluride2023]` |
| Ground-robot transfer gap | Speck/LENS numbers are compelling but untested in flight `[src:13-neuromorphic-localization]` |

The field is advancing but remains pre-deployment: every result is a proof-of-concept or feasibility step. The 2024 *Science Robotics* paper is the highest-fidelity demonstration and still indoor-only with a linear controller.

---

## Source

- `raw/research/onboard-ai-energy/04-fully-neuromorphic-flight.md` — de Croon/Paredes-Vallés, *Science Robotics* 2024; first fully neuromorphic vision→control on a free-flying quadrotor (PRIMARY)
- `raw/research/onboard-ai-energy/05-neuromorphic-attitude.md` — de Croon/MAVLab 2024; SNN raw-IMU→motor attitude estimation on Teensy 4.0
- `raw/research/onboard-ai-energy/06-colibriuav.md` — ColibriUAV; Kraken SoC with SNE+CUTIE accelerators, event→PWM closed loop
- `raw/research/onboard-ai-energy/08-mavlab-loihi-landing.md` — Dupeyroux/de Croon; first embedded Loihi in a flying robot (abstract only)
- `raw/research/onboard-ai-energy/09-neuromorphic-robotic-vision-survey.md` — Purdue/Roy PMC 2025; SNN families, HW landscape, honest maturity assessment
- `raw/research/onboard-ai-energy/12-decroon-telluride2023.md` — de Croon Telluride 2023 talk (auto-caption); MAVLab 2013–2023 arc with admitted gaps
- `raw/research/onboard-ai-energy/13-neuromorphic-localization.md` — LENS, *Science Robotics*; SynSense Speck visual place recognition on ground robot (transfer to drone untested)

## Related

- [[drone-power-budget]] — airframe energy envelope that motivates neuromorphic compute
- [[nano-drone-compute]] — conventional silicon baseline; the comparison target for energy numbers here
- [[event-cameras]] — sensor physics underlying event-driven neuromorphic pipelines
- [[event-cameras-for-uavs]] — UAV-specific event camera deployments; ~0.94 W Loihi figure corrected here
- [[neuromorphic-materials]] — substrate and device-level developments feeding future chip generations
- [[drone-autonomy-state]] — where neuromorphic fits in the broader autonomy stack
- [[visual-inertial-slam]] — localization workload that Speck/LENS targets; drone transfer speculative
- [[eth-rpg-scaramuzza]] — Zurich RPG lab; related autonomy research, distinct from TU Delft MAVLab
