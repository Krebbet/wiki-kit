# DroneVLA — VLA-Based Aerial Manipulation (PoC)

arXiv 2601.13809. A proof-of-concept coupling a **minimalist binary-action VLA** (TinyVLA-inspired) with Grounding DINO detection and human-aware A* navigation for a fetch-and-handover task. Navigation/perception validated in real flight; the VLA itself validated **only in Unity simulation**, not in the real loop.

## Key takeaways *(maturity: TRL ~2–3, concept/sim)*

- **VLA:** bespoke TinyVLA variant (6-layer ViT-Tiny encoder, 4-layer text transformer, 2-layer MLP head); **binary action space only** (gripper Open/Close) — not a generalist foundation model.
- **Platform:** custom quadrotor + 1-DoF parallel gripper (Dynamixel AX-12A) + RealSense RGB-D; OrangePi onboard; VLA inference **offboard** on a ground-station RTX GPU (<5 ms), ROS2 over Wi-Fi.
- **Results:** navigation/perception 10/10 real trials (mean localization error 0.070 m, RMSE 0.084 m); VLA grasping 10/10 **in Unity sim only** — paper explicitly states the VLA was not in the real flight-control loop. Relies on Vicon ground-truth pose.

## Tech gaps

Binary open/close only (no pose/velocity control; full 5-DoF = future work); VLA never closed-loop on real hardware; Vicon-dependent; downwash interference unsolved; single rigid object, 10 near-identical trials. Consumer-relevance ≈ zero — an architecture template, not a system.

## Source

- `raw/research/weekly-2026-05-17/03-dronevla.md` — DroneVLA, arXiv 2601.13809

## Related

- [[aerial-manipulation]] — parent cluster; see its VLA-driven aerial manipulation note
- [[air-vla]] — companion this week; AIR-VLA is the broad benchmark, DroneVLA the narrow system PoC
- [[aerial-grasping]] · [[drone-contact-and-door-tasks]] — task scope
- [[drone-autonomy-state]] — offboard-reasoning pattern; pre-commercial maturity
