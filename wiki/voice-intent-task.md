# Voice → Intent → Task for Drones

Translating a spoken command into a drone action requires three chained steps: speech-to-text (STT) on noisy audio, intent extraction (LLM/VLM), and grounded task execution — each with its own latency and reliability budget. This is the wiki's least-covered capability requirement and one of the biggest open problems for consumer autonomy: real-flight language→trajectory pipelines exist in research but no consumer stack closes the loop from rotor-noise-corrupted audio to a safe, spatially-grounded maneuver entirely onboard.

## State of the art

### Speech-to-text (STT) front-end

- *demoed, on-device, generic* — **whisper.cpp** (ggml-org) runs OpenAI Whisper tiny (75 MiB, ~273 MB RAM) through large-v3 (2.9 GiB) in pure C/C++ with no runtime memory allocation; ARM NEON, Metal, CoreML, CUDA, Vulkan, and OpenVINO backends; integer quantization (Q5_0) cuts size further; demonstrated real-time on iPhone 13 and Raspberry Pi; VAD included. Not drone-specific; rotor-noise robustness untested. [12-whisper-cpp]
- *demoed, on-device, generic* — **PI-Whisper** augments Whisper with LoRA profile libraries indexed by speaker accent/age/gender, merged at inference; reduces WER by up to 13.7% relative on edge devices; cloud comparison baseline used but the LoRA-merge path is on-device. Not drone-specific. [09-arxiv-2406-15668]
- *gap* — No publicly available ASR model or dataset trained on speech recorded near operating rotors. All above systems assume clean or moderately noisy audio.

### Intent extraction: LLM command parsing on real drones

- *demoed, cloud-assisted, drone-specific* — **Tello STT→LLM pipeline** (UFG, 2024): wav2vec2 STT → Llama-3 LLM (JSON structured output) → DJI Tello function call. Three pipelines compared on a real Tello: (1) STT+LLM, (2) direct wav2vec2 classification, (3) Siamese network. STT+LLM most flexible but highest latency; Siamese network best flexibility/latency tradeoff. Dataset: 6 directional commands, indoor, no rotor noise. Inference times reported per pipeline but no end-to-end (audio capture → motor command) wall-clock figure published. [01-arxiv-2407-08658]
- *demoed, on-device (Ollama), drone-specific* — **PX4-ROS2-Ollama framework** (Southampton, 2025): LLMs (Gemma3, Qwen2.5, Llama-3.2, DeepSeek) and VLMs (Gemma3, Llama3.2-Vision, LLaVA1.6) served locally via Ollama on a custom quadcopter + PX4/ROS2. Gemma3/Qwen2.5/Llama-3.2 produced 100% valid flight commands; DeepSeek only 38%. VLMs achieved 97–100% binary object-presence detection. Best end-to-end mission success: 40% (Gemma3 LLM+VLM pair). Evaluated in Isaac Sim and real flight. No voice/STT front-end — text prompts only. [02-arxiv-2506-07509]
- *demoed, cloud, drone-specific* — **UAV-VLA** (Skoltech, 2025): satellite imagery + GPT + VLM → flight path + action set. Generates full mission plans in 5m24s, 6.5× faster than an expert operator; 34.22 m mean object-localization error (KNN). Text-input only; no voice; outdoor/large-scale missions. [06-arxiv-2501-05014]
- *claimed, sim + real, drone-specific* — **UAV-VLN** (BITS Pilani, 2025): LLM + vision model → sub-goals → task planner → drone; evaluated indoor and outdoor VLN; "significant improvements in instruction-following accuracy and trajectory efficiency." No ablation on STT. [08-arxiv-2504-21432]
- *speculated, generic-robot* — **BrainBody-LLM** (NYU, 2024): two-LLM (Brain/Body) hierarchy with closed-loop simulator feedback; 15% improvement over baselines in VirtualHome + Franka arm; not drone-specific but the dual-LLM + feedback-loop architecture is directly applicable to language→drone-task grounding. [10-arxiv-2402-08546]

### Language→trajectory benchmarks (real flight)

- *demoed, real-flight, drone-specific* — **UAV-Flow / Flying-on-a-Word (Flow)** (Beihang/NUS/CUHK, 2025): first real-world benchmark for language-conditioned fine-grained UAV trajectory control. 30K real-world episodes across 3 campuses, 10K sim episodes; atomic language instructions paired with expert pilot trajectories via imitation learning. VLA models outperform VLN baselines; spatial grounding identified as primary bottleneck. First real-world VLA deployment on a UAV in open environments. [03-arxiv-2505-15725]
- *claimed, sim-only, drone-specific* — **ASMA** (Purdue, 2025): vision-language navigation + scene-aware Control Barrier Functions (CBF) + MPC for safety-aware drone navigation. Deployed on Parrot Bebop2 in Gazebo/ROS; 64–67% higher success rate vs CBF-less VLN with only 1.4–5.8% longer trajectories. RGB-D camera provides scene-aware safety margin. Architecture directly addresses misheard/misunderstood command safety via formal safety constraints, but sim-only validation. [05-arxiv-2409-10283]

### Onboard VLA inference

- *demoed, real-flight, drone-specific* — **VLA-AN** (Zhejiang U / Differential Robotics, 2024): onboard VLA for aerial navigation; 2–3 Hz real-time inference on a 100 TOPS compute board; geometric safety correction module; 3D-GS synthetic dataset (100K trajectories, 1M multimodal samples); three-stage training (SFT → navigation → RL fine-tune); 8.3× inference throughput improvement vs baseline; >90% avg success rate in sim+real. Text-conditioned, no voice front-end. [04-arxiv-2512-15258]
- *demoed, sim-only, drone-specific* — **AerialVLA** (UESTC, 2026): minimalist end-to-end VLN/VLA; dual-view perception; fuzzy directional prompting from onboard sensors only (no oracle path or external detector); unified 3-DoF control + intrinsic landing signal; ~3× success rate of leading baselines in unseen environments on TravelUAV benchmark. Sim-only. [07-arxiv-2603-14363]

### Empirical landscape (developer/researcher gap)

- *claimed, survey* — **LLM×UAV empirical study** (UESTC/PKU/ZJU, 2025): systematic review of 997 papers + 1,509 GitHub projects. Top three LLM tasks in UAV: Single-UAV Task Reasoning & Planning, Control Logic & Command Generation, Natural Language Command Parsing. Only 19.05% of developer teams have deployed LLM-UAV projects; 59.6% have not attempted; 82.7% of developers prefer onboard control modes. Technical maturity of all tasks rated below 3/5. Safety (45.2%) and insufficient LLM performance (51.6%) are top barriers. [11-arxiv-2509-12795]

## Key gaps

1. **End-to-end latency uncharacterized.** No published paper measures wall-clock time from audio capture through STT → LLM → motor command on a real drone. Individual stage latencies exist (Tello study measures per-pipeline inference, VLA-AN reports 2–3 Hz VLA throughput) but the full pipeline number is absent.
2. **No fully on-device STT+LLM on consumer-class hardware.** whisper.cpp runs on-device; Ollama-served LLMs run on-device on a ground companion computer. Neither has been demonstrated together on a sub-250g flight controller. The PX4-Ollama work runs the LLM on a connected laptop, not onboard.
3. **No rotor-noise ASR dataset.** Every STT evaluation uses clean or lightly augmented audio. A drone's own motors generate broadband noise that degrades ASR; the Tello study collected commands without the drone running. No quantitative WER-under-rotor-noise figure exists.
4. **Spatial grounding of spoken object references.** "Fly to the red chair near the window" requires associating spoken noun phrases with specific instances in the drone's current view and semantic map. UAV-Flow identifies spatial grounding as the primary bottleneck; [[semantic-object-memory]] is the necessary complement, but the STT→intent→grounded-object link is not closed in any real-flight system.
5. **Misheard-command safety barely studied.** ASMA provides formal CBF-based safety *after* a command is interpreted, but the consequence of a misheard or hallucinated command arriving at the flight controller is unstudied in real hardware. The Tello pipeline has no rejection or confirmation mechanism for low-confidence transcriptions.
6. **Intent ambiguity resolution.** Consumer voice commands are elliptical ("go there", "get that"). None of the surveyed systems handle clarification dialogues or partial-command rejection gracefully on real hardware.
7. **Generalization beyond directional commands.** The Tello study covers 6 directional words. UAV-VLA and PX4-Ollama handle higher-level missions but via text, not voice. Language→fine-grained trajectory (Flow) is real-flight demonstrated only for atomic instructions, not compound household tasks (relevant to [[home-tidy-drone-prototype]]).

## Source

- `raw/research/voice-intent-task/01-arxiv-2407-08658.md` — arXiv 2407.08658 · "Evaluating Voice Command Pipelines for Drone Control: From STT and LLM to Direct Classification and Siamese Networks" · Three pipelines on a real Tello; STT+Llama-3 vs direct classification vs Siamese; flexibility/latency tradeoffs quantified.
- `raw/research/voice-intent-task/02-arxiv-2506-07509.md` — arXiv 2506.07509 · "Taking Flight with Dialogue: Enabling Natural Language Control for PX4-based Drone Agent" · Open-source PX4+ROS2+Ollama framework; LLM/VLM families benchmarked in sim and on real quad; 40% mission success best case.
- `raw/research/voice-intent-task/03-arxiv-2505-15725.md` — arXiv 2505.15725 · "UAV-Flow Colosseo: A Real-World Benchmark for Flying-on-a-Word UAV Imitation Learning" · First real-flight language→trajectory benchmark; 30K episodes; VLA > VLN; spatial grounding is the bottleneck.
- `raw/research/voice-intent-task/04-arxiv-2512-15258.md` — arXiv 2512.15258 · "VLA-AN: An Efficient and Onboard Vision-Language-Action Framework for Aerial Navigation in Complex Environments" · 2–3 Hz onboard VLA on 100 TOPS board; geometric safety correction; >90% sim+real success; 8.3× throughput gain.
- `raw/research/voice-intent-task/05-arxiv-2409-10283.md` — arXiv 2409.10283 · "ASMA: An Adaptive Safety Margin Algorithm for Vision-Language Drone Navigation via Scene-Aware Control Barrier Functions" · CBF+MPC safety layer on VLN drone; 64–67% success improvement; sim-only (Gazebo).
- `raw/research/voice-intent-task/06-arxiv-2501-05014.md` — arXiv 2501.05014 · "UAV-VLA: Vision-Language-Action System for Large Scale Aerial Mission Generation" · Satellite imagery + GPT → flight paths; 6.5× faster than human planner; text-input only.
- `raw/research/voice-intent-task/07-arxiv-2603-14363.md` — arXiv 2603.14363 · "AerialVLA: A Vision-Language-Action Model for UAV Navigation via Minimalist End-to-End Control" · Fuzzy directional prompting; no oracle/external detector; ~3× baseline success on TravelUAV; sim-only.
- `raw/research/voice-intent-task/08-arxiv-2504-21432.md` — arXiv 2504.21432 · "UAV-VLN: End-to-End Vision Language guided Navigation for UAVs" · LLM + vision → sub-goals → planner; indoor+outdoor VLN; sim + limited real evaluation.
- `raw/research/voice-intent-task/09-arxiv-2406-15668.md` — arXiv 2406.15668 · "PI-Whisper: Designing an Adaptive and Incremental ASR System for Edge Devices" · LoRA-profile-based Whisper adaptation; 13.7% WER reduction on edge; not drone-specific.
- `raw/research/voice-intent-task/10-arxiv-2402-08546.md` — arXiv 2402.08546 · "Grounding LLMs For Robot Task Planning Using Closed-loop State Feedback" · BrainBody-LLM dual-LLM hierarchy + feedback; 15% success improvement on Franka arm; generic-robot, applicable architecture.
- `raw/research/voice-intent-task/11-arxiv-2509-12795.md` — arXiv 2509.12795 · "When Large Language Models Meet UAV Projects: An Empirical Study from Developers' Perspective" · 997-paper SLR + 1,509 GitHub projects + 52-developer survey; documents academia-industry gap and safety/performance barriers.
- `raw/research/voice-intent-task/12-whisper-cpp.md` — github.com/ggml-org/whisper.cpp · "Port of OpenAI's Whisper model in C/C++" · On-device STT; tiny–large models; ARM/Metal/CUDA/Vulkan; quantization; VAD; demonstrated on iPhone 13 and Raspberry Pi.

## Related

- [[home-tidy-drone-prototype]] — parent research assignment; voice is the primary UX modality for indoor household task delegation
- [[air-vla]] — sim-only VLA for aerial manipulation; voice front-end not covered but shares the language→action pipeline; spatial grounding findings complement UAV-Flow
- [[dronevla]] — companion VLA-aerial-manipulation work; same gap: no voice STT stage
- [[drone-autonomy-state]] — overall autonomy SOTA; voice→intent sits at the "natural language interface" layer above the control stack documented there
- [[semantic-object-memory]] — grounding spoken object references ("the red chair") requires an object memory that persists across frames; the two problems are tightly coupled
