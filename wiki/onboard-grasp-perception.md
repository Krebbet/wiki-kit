# Onboard Open-Vocabulary Perception & Grasping

Mocap-free identification and grasping of arbitrary household objects from a flying platform is the single hardest unsolved problem for autonomous aerial manipulation in domestic settings. Open-vocabulary detectors suffer severe domain-transfer failure on aerial viewpoints; every working onboard grasper to date relies on category-specific priors or operator-in-the-loop click-to-segment; and even the fastest edge-class detectors run at 3–8 fps on Jetson-class hardware at full quality. This page surveys the state of the research as of mid-2026, distinguishing onboard from offboard/mocap results throughout.

## State of the art

### Open-vocabulary detection — aerial domain gap

- **Severe domain-transfer failure is quantified** [*eval*]: best F1 on the 80-category LAE-80C aerial benchmark is 27.6% (OWLv2), with 69% false-positive rate; YOLO-World achieves F1 = 2.8%, Grounding DINO in global 80-class mode achieves F1 = 0.5%. All five models evaluated (Grounding DINO, OWLv2, YOLO-World, YOLOE, LLMDet) were tested zero-shot with no aerial fine-tuning. [src: 02-arxiv-2601-22164]

- **Semantic confusion is the primary bottleneck, not visual localization** [*eval*]: reducing Grounding DINO's prompt from 80 classes to the oracle set of ≈3.2 ground-truth classes per image yields a 15× improvement in F1 (0.5% → 7.4%), confirming that category overlap — not inability to see objects — is the limiting factor. [src: 02-arxiv-2601-22164]

- **Prompt engineering does not fix the gap** [*eval*]: prepending "Aerial view of" to class names raises precision to 92.6% but drops recall to 2.3% (F1 4.5% vs 7.4% baseline), and synonym expansion degrades results. The visual encoder is the root problem — text prompts cannot compensate for features learned exclusively on ground-level imagery. [src: 02-arxiv-2601-22164]

- **Dataset brittleness is severe** [*eval*]: the same models achieve F1 = 0.53 on clean object-centric DIOR images but collapse to F1 = 0.12 on FAIR1M (fine-grained, dense) — a 4.4× drop across imaging conditions within the same benchmark. [src: 02-arxiv-2601-22164]

- **UAV-specific pretraining partially closes the gap** [*demoed*]: YOLO-World-v2-L trained on the new UAVDE-2M dataset (2.4M instances, 1,800+ categories from UAV perspectives) achieves mAP 13.9 on VisDrone vs 8.59 with standard pretraining — a 62% gain. The CAGE cross-attention gated enhancement module deployed on NVIDIA Orin NX 16G achieves TensorRT FP16 inference at 22.90 ms/frame (≈44 Hz) for the S-scale model, meaningfully faster than vanilla YOLO-World-v2-S at 25.38 ms. [src: 07-arxiv-2509-06011]

- **Grounding DINO throughput on Jetson is inadequate for closed-loop manipulation** [*claimed*]: the LAE-80C benchmark table reports Grounding DINO at 3.2 fps (Swin-L, 218M params) on a server GPU; Jetson deployment via Roboflow Inference Server is documented but no manipulation-rate fps numbers are published for edge hardware. [src: 02-arxiv-2601-22164; 09-grounding-dino-jetson-deploy]

### Onboard grasping — category-specific priors required

- **First onboard-only, zero-shot, outdoor aerial grasping is demoed** [*demoed*]: ETH Zurich's Osprey platform achieves 85% average grasp success across 144 attempts on 9 household objects (bottle, plush toy, pouch, kitchen roll, ball, etc.) using onboard-only perception — Spectacular AI SLAM for localization + SAM2 video segmentation for target tracking + depth-based grasp point estimation. No mocap used at test time. Peak relative pose error during fast descent: 0.042 m. Platform cost: ~$1,274. The operator must click-select the target object in a live camera feed before flight; the system is not fully autonomous from a text command. [src: 01-arxiv-2409-07662]

- **All current onboard graspers need per-object bootstrapping or operator input** [*claimed*]: the ETH system requires a human to designate the target via a click; the FlyAware system requires a text string naming the object class (fed to Grounded SAM); no published system autonomously selects what to grasp from open-vocabulary language without operator involvement during flight. [src: 01-arxiv-2409-07662; 06-arxiv-2601-22686]

- **SAM2 onboard tracking is feasible but memory-constrained** [*demoed*]: Osprey uses SAM2 for segmentation and tracking across frames; the paper notes SAM2 memory and compute increase with frame count, limiting use to short-term sequences (<400 frames) on the Odroid H3+ compute platform. [src: 01-arxiv-2409-07662]

### Onboard perception with LLMs for inertia estimation

- **GPT-4v used onboard (via API) for pre-grasp inertia estimation** [*demoed*]: FlyAware (Sun Yat-sen / HKUST) uses Grounded SAM to detect a text-named object, IST-Net for 9D pose + size at 3–5 m standoff (90.6% average size accuracy on 8 objects), then calls GPT-4 API to estimate density, volume scale factor, and MoI scale factor from a cropped image and object name. Post-grasp, a disturbance observer refines mass online. Real-world experiments validate stable flight after grasping unknown payloads. This is offboard inference (API call), not edge-compute inference. [src: 06-arxiv-2601-22686]

- **OWG pipeline achieves open-vocabulary tabletop grasping from free-form language** [*demoed*]: University of Groningen's OWG pipeline (GPT-4v + SAM segmentation + GR-ConvNet grasp synthesis) achieves 80.8% average mIoU for open-ended grounding on cluttered indoor OCID scenes — 27.7% above the next best zero-shot method (SoM/GPT-4v at 53.1%). Real-robot success: 83.3% isolated, 50.0% cluttered (6 trials each). All experiments are on a stationary robot arm, not aerial. The pipeline requires server-class inference (GPT-4v API) — not onboard-only. [src: 04-arxiv-2406-18722]

### Contact-aware onboard perception

- **First mocap-free onboard contact-rich manipulation pipeline** [*demoed*]: PSU/CMU's system augments VINS-Fusion VIO with contact-consistency factors that activate only during physical contact, achieving 66.01% reduction in velocity estimation error at contact vs vanilla VINS-Fusion (RMSE 0.0121 vs 0.0356 m/s). IBVS + hybrid force-motion control regulates 5 N contact force against a wall target — all onboard, no mocap for control. Used on a fully-actuated hexarotor (Tarot T960 + ModalAI VOXL 2). Object localization uses a color-based detector targeting a known circular fiducial, not open-vocabulary recognition. [src: 03-arxiv-2602-08251]

### VLA transfer to aerial manipulation

- **AirVLA: π0 VLA fine-tuned for aerial pick-and-place** [*demoed*]: Stanford/Physical Intelligence fine-tune the π0 foundation VLA on 270 teleoperated aerial demos + 50 Gaussian Splatting synthetic trajectories. With payload-aware guidance injected into the flow-matching sampler at inference time, pick-and-place success reaches 50% (vs 0% naive, 23.5% with RTC only). Compositional navigate-then-grasp achieves 62% overall conditioned success. Experiments use mocap for localization — explicitly acknowledged as a gap for future onboard VIO replacement. Object detection is handled by VLA visual representations, not a separate open-vocabulary detector. [src: 08-arxiv-2603-25038]

- **VLA dynamics gap is the core aerial transfer blocker** [*demoed*]: AirVLA finds that visual representations transfer from fixed-base manipulators to aerial platforms, but flight dynamics do not — naive fine-tuning alone achieves 0% place success. Physics-informed guidance at inference time (payload-aware vertical compensation) is required. Out-of-distribution object generalization is partial: 70% pick success on sandwich, 10% on bag of chips. [src: 08-arxiv-2603-25038]

- **LiteVLA-H: compact dual-rate VLA on Jetson AGX Orin** [*demoed*]: 256M-parameter VLA achieves action token emission at 50.65 ms / 19.74 Hz (outer-loop guidance) and semantic description at 149.90 ms / 6.67 Hz on a single Jetson AGX Orin. 94.4% of first-action latency is multimodal pre-fill — reducing output token count does not help; reducing visual token count and caching prompt structure are the correct optimization directions. Task success in simulated runway navigation: 84.1%. Hardware obstacle course: 81.3%. No object manipulation evaluated, only navigation. [src: 05-arxiv-2605-00884]

## Key gaps

- **No open-vocabulary, fully-autonomous aerial object selection without operator input**: every working system requires either a human click (SAM2-based), a text class name, or a fixed target (fiducial, colored circle). A drone that autonomously decides "the cup on the table" from scene understanding alone does not exist.

- **OVD domain gap is architectural, not lexical**: all five benchmarked state-of-the-art detectors fail catastrophically at aerial viewpoints. Domain-adaptive pretraining (UAVDE-2M) partially helps but achieves only mAP 13.9 on VisDrone — still far below what's needed for reliable household-object identification from flight altitude. Fine-tuning on household-object aerial datasets does not yet exist. [src: 02-arxiv-2601-22164; 07-arxiv-2509-06011]

- **Edge compute throughput wall**: Grounding DINO (218M, Swin-L) runs at 3.2 fps on server hardware; no published fps on Jetson for the models that achieve acceptable OVD quality. YOLO-World-class models (22–25 ms on Orin NX TensorRT) achieve real-time rates but with dramatically worse zero-shot accuracy. The gap between accuracy-sufficient and compute-feasible models is not yet bridged. [src: 02-arxiv-2601-22164; 07-arxiv-2509-06011; 09-grounding-dino-jetson-deploy]

- **SAM2 memory growth limits continuous operation**: onboard tracking with SAM2 accumulates memory per frame, capping practical use at <400 frames on current Jetson-class compute. Re-initialization requires human click input. [src: 01-arxiv-2409-07662]

- **Mocap dependency in VLA work**: AirVLA and similar systems use motion capture for localization during experiments and acknowledge VIO replacement as future work. No published VLA aerial manipulation result uses only onboard state estimation end-to-end. [src: 08-arxiv-2603-25038]

- **Payload dynamics break naive VLA transfer**: post-grasp inertia change causes altitude sag that neither OVD systems nor vanilla VLAs handle. FlyAware addresses this with pre-grasp vision-based inertia estimation + post-grasp DOB adaptation, but uses API-based LLM inference (not onboard edge compute). [src: 06-arxiv-2601-22686; 08-arxiv-2603-25038]

- **Grasp planning from VLA is category-biased**: AirVLA generalizes to novel objects only partially (10–70% pick success depending on geometry) and fails completely on bags of chips. OWG achieves strong grounding but is a static-arm, server-compute system. No onboard aerial system generalizes grasp pose across arbitrary household object geometries. [src: 08-arxiv-2603-25038; 04-arxiv-2406-18722]

- **VLA onboard inference rate vs. manipulation bandwidth**: LiteVLA-H at 19.74 Hz outer-loop is approaching the floor for reactive aerial guidance, but semantic perception runs at only 6–7 Hz and manipulation (grasp pose refinement) is slower still. The pre-fill bottleneck (~48 ms) means any aerial VLA providing both navigation and manipulation reasoning simultaneously will struggle to close the loop fast enough. [src: 05-arxiv-2605-00884]

## Source

- `raw/research/onboard-grasp-perception/01-arxiv-2409-07662.md` — arXiv 2409.07662 · *An Open-Source Soft Robotic Platform for Autonomous Aerial Manipulation in the Wild* · ETH Zurich Osprey platform; onboard-only SAM2 + SLAM grasp pipeline; 85% success across 144 real-world trials, no mocap at test time (CoRL 2024)
- `raw/research/onboard-grasp-perception/02-arxiv-2601-22164.md` — arXiv 2601.22164 · *Do Open-Vocabulary Detectors Transfer to Aerial Imagery? A Comparative Evaluation* · First systematic benchmark of 5 OVD models on LAE-80C; best F1 = 27.6%; semantic confusion dominates; prompt engineering fails
- `raw/research/onboard-grasp-perception/03-arxiv-2602-08251.md` — arXiv 2602.08251 · *Aerial Manipulation with Contact-Aware Onboard Perception and Hybrid Control* · PSU/CMU; contact-consistent VIO + IBVS + hybrid force control; 66% velocity error reduction at contact; no mocap for control
- `raw/research/onboard-grasp-perception/04-arxiv-2406-18722.md` — arXiv 2406.18722 · *Towards Open-World Grasping with Large Vision-Language Models* · OWG pipeline; GPT-4v + SAM + grasp synthesis; 80.8% mIoU grounding; stationary arm, server inference only (CoRL 2024)
- `raw/research/onboard-grasp-perception/05-arxiv-2605-00884.md` — arXiv 2605.00884 · *LiteVLA-H: Dual-Rate Vision-Language-Action Inference for Onboard Aerial Guidance and Semantic Perception* · 256M VLA on Jetson AGX Orin; 19.74 Hz action / 6.67 Hz semantic; pre-fill dominant latency characterization (ICML 2026 submission)
- `raw/research/onboard-grasp-perception/06-arxiv-2601-22686.md` — arXiv 2601.22686 · *FlyAware: Inertia-Aware Aerial Manipulation via Vision-Based Estimation and Post-Grasp Adaptation* · Pre-grasp GPT-4 inertia estimation + DOB adaptation; first vision-based inertia estimation for aerial manipulators; API-based, not edge-local
- `raw/research/onboard-grasp-perception/07-arxiv-2509-06011.md` — arXiv 2509.06011 · *Light-Weight Cross-Modal Enhancement Method with Benchmark Construction for UAV-based Open-Vocabulary Object Detection* · CAGE module + UAVDE-2M dataset; YOLO-World-v2-L mAP 8.59→13.9 on VisDrone; Jetson Orin NX TensorRT 22.90 ms
- `raw/research/onboard-grasp-perception/08-arxiv-2603-25038.md` — arXiv 2603.25038 · *π, But Make It Fly: Physics-Guided Transfer of VLA Models to Aerial Manipulation* · AirVLA; π0 fine-tuned for aerial pick-and-place; payload-aware guidance; 50% place success; mocap-dependent localization (Stanford/Physical Intelligence)
- `raw/research/onboard-grasp-perception/09-grounding-dino-jetson-deploy.md` — Roboflow · *Deploy Grounding DINO to NVIDIA Jetson* · Deployment how-to via Roboflow Inference Server + Docker; no published fps figures for the manipulation-grade model configurations

## Related

- [[home-tidy-drone-prototype]] — parent use-case; onboard open-vocabulary grasping is research assignment #1 for the home-tidy scenario
- [[aerial-grasping]] — cross-reference: soft-drone onboard grasp (Osprey/ETH covered here); do not duplicate hardware details
- [[aerial-manipulation]] — broader manipulation taxonomy; contact-rich tasks, force control, and fully-actuated platforms covered there
- [[drone-contact-and-door-tasks]] — contact-aware VIO and force regulation pipelines are shared infrastructure
- [[air-vla]] — AIR-VLA benchmark and dataset for aerial manipulation VLA systems, cited as concurrent work in sources
- [[dronevla]] — VLA-AN and related aerial VLA navigation approaches; complementary to manipulation-focused work here
- [[drone-sensors-for-autonomy]] — onboard compute (Jetson AGX Orin, VOXL 2, Odroid H3+), camera selection, and edge inference constraints
