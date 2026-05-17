# AIR-VLA — VLA Benchmark for Aerial Manipulation

arXiv 2601.21602. The first systematic **benchmark + simulation dataset** (not a model) evaluating mainstream vision-language-action / VLM models on a simulated UAV + 7-DoF arm. Entirely sim (NVIDIA Isaac Sim / PhysX 5); no real-world trials. Maps the gap for language-conditioned aerial manipulation more than it closes it.

## Key takeaways *(maturity: TRL ~2–3, sim-only)*

- **Testbed, not a model:** evaluates π0 / π0.5 / π0-FAST, ACT, Diffusion Policy, and VLM planners (Qwen3-VL-8B, Qwen2.5-VL, GLM-4V, InternVL3-5, Molmo, LLaVA-OV) fine-tuned on aerial-manipulation data.
- **Platform:** simulated quadrotor + Franka Panda 7-DoF arm (12-DoF total). Tasks: pick, place, twist, drawer open/close across 4 suites (Base, Object & Spatial, Semantic, Long-Horizon).
- **Data:** 3,000 teleop sim episodes; 30–50 trajectories/task fine-tune.
- **Best model (π0.5) sim scores (/100):** Base 45.3, Object/Spatial 42.3, Semantic 40.2, Long-Horizon 37.1; **overall ~42.0** (*claimed*, sim). ACT/Diffusion Policy ≈14 (≈no completion). Best VLM planner (Qwen3-VL) 23.3% success.
- **Sensor finding:** removing the fixed third-person global camera drops π0.5 42.0→34.5; UAV disturbance barely matters (−1.0). 3D spatial understanding is the primary bottleneck.

## Tech gaps

Sim-only, no sim-to-real; heavy dependence on an external global camera (onboard-only degrades sharply — fatal for deployment); no onboard-compute/latency path; even best models ~42/100 in controlled sim. "Tell a drone to fetch X" remains firmly pre-commercial.

## Source

- `raw/research/weekly-2026-05-17/02-air-vla.md` — AIR-VLA benchmark, arXiv 2601.21602

## Related

- [[aerial-manipulation]] — parent cluster; see its VLA-driven aerial manipulation note
- [[dronevla]] — companion VLA-aerial-manipulation work this week (benchmark vs system)
- [[aerial-grasping]] · [[drone-contact-and-door-tasks]] — the pick/place/twist/drawer tasks map here
- [[drone-autonomy-state]] — the ~42/100 sim score is a concrete state-of-field datapoint
- [[drone-sensors-for-autonomy]] — the global-camera dependency finding
