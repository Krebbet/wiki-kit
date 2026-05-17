# Dream to Fly — Model-Based RL for Vision-Based Drone Flight

ETH RPG (Scaramuzza lab), arXiv 2501.14377, ICRA 2026. A DreamerV3 world-model RL agent trained **from raw 64×64 RGB pixels to control commands** — no LiDAR, no depth, no state estimation, no imitation-learning bootstrap — flying agile gate courses up to **9 m/s** with real-quadrotor dynamics validation via hardware-in-the-loop. A load-bearing Position-B datapoint for [[lidar-vs-vision-autonomy]].

## What it does

- **Architecture** (*demoed*): DreamerV3 — RSSM world model + actor-critic trained in imagination. Policy input is **RGB pixels only** (64×64); IMU lives only in the low-level Betaflight controller, not in the learned policy.
- **Results** (*demoed*): converges on all three sim tracks within ~20 M env steps; **PPO and SAC fail to achieve meaningful reward after 20 M interactions** — model-based RL strictly dominates model-free on this pixel-input task. Real-world (HIL) Figure-8 at peak **9 m/s**.
- Emergent perception-aware behaviour: the policy spontaneously orients the camera toward gates with no viewing-direction reward term.

## Conflict relevance

Strong **Position-B** (vision-sufficient) entry for the open [[lidar-vs-vision-autonomy]]: a single onboard RGB camera, raw pixels → control, no LiDAR/depth/VIO, is sufficient for agile flight (≤9 m/s) on structured gate courses. **Asterisk:** real-world deployment uses *rendered* images (Habitat) over HIL, not an actual camera feed — the real-optics/motion-blur/exposure gap is untested. File as strong Position-B with the real-camera gap noted.

## Tech gaps

Real-camera transfer undemonstrated (HIL renders only); **240 h training on a Quadro RTX 8000** (impractical for consumer/hobbyist); structured known-geometry tracks only (no unstructured/GPS-denied/outdoor); world-model tuning difficulty is an open MBRL challenge.

## Source

- `raw/research/weekly-2026-05-17/01-dream-to-fly.md` — ETH RPG, arXiv 2501.14377 (ICRA 2026)

## Related

- [[lidar-vs-vision-autonomy]] — supplies Position-B (vision-sufficient) evidence, with the real-camera asterisk
- [[eth-rpg-scaramuzza]] — same lab; extends RPG's pixel-to-control flight line
- [[visual-inertial-slam]] — contrast: this paper deliberately avoids VIO/state estimation
- [[drone-autonomy-state]] — first claimed RL-from-scratch pixel→command system on real quadrotor dynamics
