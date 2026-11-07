# Fast Visual Hazard Detection — the "Something Is Off Ahead" Trigger Loop

How to build a **fast, live visual safety/attention loop** for the drone-prototype rover: a separate process that looks at the view ahead at ≥3 checks/s (Jetson-class target; 10+ ideal), fires a gentle HOLD when it sees something unexplained (a person, the ~20 cm office rabbit *below* the 0.334 m LiDAR plane, a new or moved object), and lets RESOLVE ("can I keep going?") and RESUME take over. The answer from deployed practice is consistent: **every shipping system splits a class-agnostic geometric layer that does the stopping from a small classifier that only changes the policy** (wider berth, wait, photograph, ask a human); nobody lets the classifier be the thing that stops the robot. For this rig the human's *expectation-subtraction* idea maps onto an established, cheap pattern — **free-space violation**: render what the map and object bank say should be in front of the camera, take stereo depth, and fire on persistent 3D blobs above the floor plane in space that should be empty. Semantics (person/pet detector, fingerprint re-ID) run on the *remainder* to choose the resolve outcome. The trigger path is affordable (~20–50 ms per check on an Orin Nano, est.); NeRF/3DGS rendering, road-anomaly segmenters, industrial anomaly models and event cameras are all the wrong tool here. *(Research synthesis, 2026-11-05, dispatched by the drone-prototype lead. Rig facts from drone-prototype `docs/architecture/capability-contract.md`; rig-specific numbers marked "est." are derivations, not measurements.)*

## Source

Web research, 2026-11-05 (three dispatched research jobs; no raw captures). Primary links are cited inline at each claim. Rig context: drone-prototype `docs/architecture/capability-contract.md` (D6), memories `moving-objects-behaviour`, `people-pets-object-class`, `office-has-a-rabbit`, `consumer-cost-sensing-tenet`.

## Related

[[dynamic-object-handling]], [[commercial-home-robots-perception]], [[consumer-robot-vacuum-mapping]], [[robot-vacuum-navigation]], [[indoor-obstacle-avoidance]], [[object-fingerprint-memory]], [[semantic-object-memory]], [[stop-and-go-navigation-on-a-locked-map]], [[passive-stereo-robustification]], [[sensor-weaknesses-and-fixes]], [[economical-ir-depth-cameras]], [[event-cameras]], [[ros2-nav2]], [[system-architecture]], [[robust-evidence-mapping-principle]]

---

## 0. The problem, in this rig's numbers

| Fact | Value | Consequence |
|---|---|---|
| Speed | 0.10 m/s autonomy, turns 0.5 rad/s | 3 checks/s = one look per **3.3 cm** of travel; a 3-of-5 debounce at 5 Hz costs 0.6 s = 6 cm. Measured stop envelope 1–5 cm (drone-prototype EDA220). Rate is not the bottleneck; **detection range and false triggers are**. |
| LiDAR plane | 0.334 m, one plane, guard box ahead | Already the geometric safety layer *in the plane*. Blind below it: the rabbit, a lying person (ISO 3691-4's 70 × 400 mm lying test piece, [fabrico](https://www.fabrico.io/blog/iso-3691-4-driverless-industrial-trucks/)), toys, shoes. |
| Stereo camera | SVPRO USB, 3840×1080 side-by-side, baseline 62.12 mm, at ~0.26 m, forward only | The only sensor that can see below the plane while driving. Passive: starves on texture (drone-prototype measured ~48 % SGBM coverage, [[stereo-dense-reconstruction]]). |
| Compute | laptop now, Jetson-class later | Every number below is quoted with its hardware. Many "Orin Nano" figures are the **Orin Nano Super** (same 8 GB board, higher clocks); the original Orin Nano is ~1.4–1.7× slower ([Jetson AI Lab](https://www.jetson-ai-lab.com/archive/benchmarks.html)). |

Depth resolution of the pair (est.): ΔZ ≈ Z²·Δd/(f·B). At half resolution (f ≈ 500 px), B = 0.062 m, Δd ≈ 0.25 px → **~0.8 cm at 1 m, ~3.2 cm at 2 m**. Height-above-floor noise is worse than ΔZ because a 0.26 m camera sees the floor at a grazing angle. Rough expectation: a 15–20 cm rabbit is reliably separable from the floor out to ~2–3 m; 3–5 cm items only within ~1–1.5 m. At 0.10 m/s a 1.5 m look-ahead is 15 s, which is plenty. Minimum range (est.): Z_min = f·B/d_max ≈ 500·0.062/128 ≈ 0.24 m at half res. The near-field band under the bumper (footprint front 0.198 m) is outside the camera's view; anything that walks in there sideways is invisible to it. **All of these need measuring on the rig.**

---

## 1. What deployed systems do

### 1.1 The universal split: geometry stops, classes steer

| Domain | Geometric, class-agnostic layer (stops) | Classifier (changes the policy) | On detection | Status |
|---|---|---|---|---|
| **iRobot j7/j9** | bumper/cliff sensors | front RGB camera + LED, on-device; only ~4 class groups shipped (shoes/socks, cords, pet waste), trained on >1 M images from >1000 homes ([IEEE Spectrum](https://spectrum.ieee.org/irobot-roomba-j7)) | steers around without stopping, sends a photo, the **user** picks a permanent or temporary keep-out ([Spectrum](https://spectrum.ieee.org/irobot-roomba-j7), [review](https://www.iphoneincanada.ca/2021/10/27/irobot-roomba-j7-review/)); a commercial guarantee on one class (pet waste) ([PopSci](https://www.popsci.com/technology/irobot-roomba-new-pet-poop-feature/)) | shipping |
| **Roborock ReactiveAI / StarSight 2.0** | 3D structured light / QVGA ToF (21,600 pts) | RGB, "dozens" → 108 claimed types incl. "unexpected objects" ([9to5google](https://9to5google.com/2022/04/08/roborock-s7-maxv-smart-robot-vacuum/), [Roborock](https://global.roborock.com/pages/roborock-saros-10r)) | avoid, mark on map | shipping / counts claimed |
| **Ecovacs AIVI 3.0** | 3D sensing | ~18 types; vendor admits it degrades in weak light and on "complex backgrounds / unusual shapes" ([Ecovacs FAQ](https://help.ecovacs.com/uk/support/faq-detail?id=416)) | touches known-safe objects lightly to clean close | shipping |
| **Dreame OmniSight** | binocular 120° cameras + structured light | 280–320+ types, 10 mm objects, "0.1 s reaction" ([Dreame blog](https://www.dreametech.com/blogs/blog/best-robot-vacuum-with-obstacle-avoidance)) | avoid | claimed (marketing) |
| **Matic** | 5–6 RGB/IR cameras, no LiDAR, on-device nets on Jetson Orin | avoids >~1 inch obstacles, recognises pets/children/people ([Matic](https://maticrobots.com/innovation)) | avoid | claimed; see [[commercial-home-robots-perception]] |
| **Amazon Astro** | IR + ToF obstacle sensors ([iFixit](https://www.ifixit.com/Device/Amazon_Astro)) → local depth map incl. stairs; "several hundred potential paths several times a second" | person classification | keeps a "socially appropriate distance" from people or follows them, predicting out-of-view motion ([Amazon Science](https://www.amazon.science/blog/astros-intelligent-motion-brings-state-of-the-art-navigation-to-the-home)) | shipping (no rates published) |
| **Warehouse AMR** (OTTO, ISO 3691-4 / R15.08) | **safety-rated 2D LiDAR**: outer warning field slows, inner protective field cuts motor power; fields switched by speed ([OTTO](https://ottomotors.com/blog/amrs-safe-around-people), [Pilz](https://www.pilz.com/en-NZ/company/press/messages/articles/239220)) | **non-safety** 3D depth cameras "supplement" for obstacles above/below the LiDAR plane; LiDAR tracking of movers → re-route ([OTTO](https://ottomotors.com/blog/amrs-safe-around-people)) | stop / slow; uncovered directions (OTTO 100 reversing) are handled by *procedure*, not sensors | shipping, certified PL d |
| **Vision people-detection add-ons** (Blaxtair) | — | 3D camera tells people from obstacles | **alerts the operator, does not stop the machine** ([Blaxtair](https://blaxtair.com/en/solutions/blaxtair-pedestrian-detection)); a competitor reports AI-camera misses on sitting/crouching/occluded people ([SEEN, biased](https://seen-safety.squarespace.com/ai-cameras-for-mhe)) | shipping |
| **Starship** | 9 cameras, 4 radars, 8 ultrasonics, ~4 mph, "every sensor is quite crappy" at a $2,250 target ([MIT TR](https://www.technologyreview.com/2018/01/30/145935/why-sidewalk-delivery-robots-still-need-safety-drivers-too/)) | pedestrians, cyclists, "unexpected obstacles" | **stops and requests remote assistance** on corner cases ([R&A News](https://roboticsandautomationnews.com/2018/12/04/insight-how-neural-networks-are-powering-autonomous-delivery/20096)) | shipping |
| **Kiwibot / Serve** | stereo (Kiwi); Ouster LiDAR + ultrasonics on Jetson (Serve) | — | remote supervisors set waypoints / take unforeseen cases ([TechCrunch](https://techcrunch.com/2020/07/21/kiwibot-delivery-robots-head-to-san-jose-with-new-partners-shopify-and-ordermark/), [Robotics 24/7](https://www.robotics247.com/article/serve_robotics_launches_level_4_autonomous_robots_for_sidewalk_deliveries)) | shipping |
| **Skydio 2 / DJI** | 6 × 200° nav cameras → TX2 at 30 fps, ~1 M 3D pts/s; misses < ½-inch wires, mirrors, windows; **hovers** when tracking is lost ([Spectrum](https://spectrum.ieee.org/skydio-2-review-this-is-the-drone-you-want-to-fly)); DJI default response is **Brake** ([Space.com](https://www.space.com/technology/drones/obstacle-avoidance-what-is-it-how-to-use-it-effectively-and-when-it-might-fail)) | subject tracking | brake/hover, then bypass | shipping |
| **Automotive** | Tesla occupancy network: class-agnostic voxel occupancy + flow, built for unidentified obstacles ([Tesmanian](https://www.tesmanian.com/blogs/tesmanian-blog/tesla-found-a-solution-to-general-obstacle-detection-with-the-use-of-occupancy-networks)); Mobileye free space from segmentation + ground-plane geometry ([CES 2020](https://d1io3yog0oux5.cloudfront.net/_30f8d843824dfbccc3bd0b0cd772d41f/intel/db/861/7795/pdf/Mobileye-CES-2020-presentation.pdf)); Subaru EyeSight brakes on stereo depth alone ([Subaru](https://www.subaru.co.jp/en/news/archives/press/2010/10_04_22e.html)) | vehicle/pedestrian classes | brake | shipping |
| **Waymo fleet response** | — | — | remote agents answer mostly multiple-choice questions and never steer; the car can reject the advice; ~70 agents for ~3000 cars ([TechCrunch 2026](https://techcrunch.com/2026/03/25/waymo-robotaxi-roadside-assistance-emergency-first-responders)) | shipping |

**Lessons that transfer** *(synthesis)*:
1. **Brake-and-hold is the default reaction** of slow or hovering platforms (DJI Brake, Skydio hover, Starship stop-and-ask, AMR protective field). Re-routing comes *after*, for tracked movers or once a human or app decides. This matches the human's HOLD → RESOLVE → RESUME design.
2. **Shipped class lists are small.** iRobot shipped ~4 groups; the 100–300 counts are marketing. Unknowns fall back to the depth layer: slow down, give a wider berth, log them.
3. **"Ask a human" is a first-class resolve outcome** everywhere (iRobot photo → user, Starship, Kiwibot, Waymo). The multiple-choice form that Waymo uses fits the rover's "unsure → ask" outcome.
4. **Published detection rates and latencies for home robots don't exist.** Dreame's 0.1 s is marketing. Our own numbers will have to come from recorded runs.

### 1.2 The classic recipe for "unknown thing on the floor" with stereo

- **v-disparity** (Labayrade, Aubert, Tarel 2002): a row-wise disparity histogram turns the ground plane into a line, obstacles show up as off-line structure, and it estimates camera height and pitch on non-flat ground. Real-time on 2002 hardware ([paper](https://typeset.io/pdf/real-time-obstacle-detection-in-stereovision-on-non-flat-b82kjjsnt1.pdf), [review](https://arxiv.org/pdf/1807.02752)). *demoed*
- **Stixels**: a column-wise obstacle representation ([Badino 2009](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Badino2009DAGM.pdf)); GPU stixels at 26 fps on a Tegra X1 ([arXiv 1707.05397](https://arxiv.org/pdf/1707.05397.pdf)). *demoed*
- **Lost and Found** (Pinggera et al., IROS 2016): local statistical tests in disparity space ("obstacle plane vs free-space plane"), 20 Hz on 2 MP stereo, obstacles **down to 5 cm high at 20 m** with an automotive baseline ([arXiv 1609.04653](https://arxiv.org/abs/1609.04653v1)). Fused with a semantic FCN on stixels: >90 % detection up to 50 m at 22 Hz ([Ramos et al., ICRA 2017](https://arxiv.org/abs/1612.06573v1)). *demoed* — this is the closest published analogue of "a rabbit on the floor ahead".
- **Indoor robots**: per-frame RANSAC floor-plane fits, with obstacles as outliers, are standard. Patents use the fit as a self-check of the depth sensor and note that planar LiDAR misses low floor items ([US 9886035](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9886035), [US 11460854](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11460854)).

### 1.3 Expectation subtraction in the literature: "free-space violation"

The human's "detect things minus things we expect, hope for the null set" already exists in robotics as the **free-space violation** test:
- **Dynablox** incrementally estimates *high-confidence free space* while modelling sensing, state-estimation and mapping limits. Anything that enters that space is dynamic, with no class training (people, doors, rolling balls). 86 % IoU at 17 FPS ([arXiv 2304.10049](https://arxiv.org/abs/2304.10049)). *demoed*
- **nvblox** (Isaac ROS) ships the same idea on the GPU: a high-confidence freespace layer, a dynamic occupancy layer for what enters it, decay toward 0.5, and an optional people-segmentation layer ([nvblox docs](https://nvidia-isaac-ros.github.io/concepts/scene_reconstruction/nvblox/technical_details.html)). *shipping (SDK)*
- **Object-level change detection** between patrols, against an object-oriented metric-semantic map, is robust to lighting and viewpoint ([PMC9459894](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9459894/), [LiSTA, arXiv 2403.02175](https://arxiv.org/pdf/2403.02175.pdf)). It is a between-session tool, not a ≥3 Hz trigger.
- **Image-pair change detection** is weak and pairing-bound: ChangeSim indoor category mIoU is only 23–26 ([arXiv 2103.05368](https://arxiv.org/pdf/2103.05368)). The patrol "anomaly with reference" benchmark is UMAD ([arXiv 2408.12527](https://arxiv.org/abs/2408.12527)). The VLM semantic-difference work on a Fetch robot publishes no latency and is VLM-scale ([arXiv 2309.16552](https://arxiv.org/abs/2309.16552)).

**Implication** *(synthesis)*: do the subtraction in **3D geometry**, not in pixels. The "expected" side is cheap for this rig: the locked/live 2D map walls extruded to height, the object bank's two-level outlines (cuboid), the floor plane, and the live LiDAR plane. That is a ray-cast depth image of a few boxes and walls, not a rendered photo.

---

## 2. Fast building blocks — published latencies

All figures are as published, with their conditions. "—" means not found. TRT = TensorRT.

### 2.1 Detectors (COCO mAP50-95)

| Model | mAP | Laptop / desktop CPU | Jetson Orin | Source |
|---|---|---|---|---|
| **YOLO26n** (Jan 2026, NMS-free) | 40.9 | CPU ONNX 38.9 ms; **OpenVINO FP32 3.3–9.1 ms on Core Ultra laptop CPUs** (258V 3.33, 358H 4.09, 155H 9.13) | **Orin Nano Super TRT FP16 4.57 ms, INT8 3.80 ms**; Orin NX 16 GB FP16 4.13 ms; PyTorch 15.6 ms | [Ultralytics YOLO26](https://docs.ultralytics.com/models/yolo26/), [Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/), [OpenVINO](https://docs.ultralytics.com/integrations/openvino/) |
| YOLO11n | 39.5 | CPU ONNX 56.1 ms | — | [Ultralytics](https://docs.ultralytics.com/models/yolo11/) |
| YOLOv8n | 37.3 | CPU ONNX 80.4 ms | Orin Nano Super TRT FP16 4.43 ms, INT8 3.49 ms | [Ultralytics](https://docs.ultralytics.com/models/yolov8/), [benchmarks repo](https://github.com/hokwangchoi/jetson-orin-nano-benchmarks) |
| YOLOv10-N | 38.5 | — | 1.84 ms (T4) | [THU-MIG](https://github.com/THU-MIG/yolov10) |
| NanoDet-Plus-m | 27.0 @320 | ~12 ms ARM CPU (ncnn) | — | [nanodet](https://github.com/RangiLyu/nanodet) |
| PP-PicoDet-S | 30.6 @320 | 123–150 FPS on Snapdragon 865 | — | [arXiv 2111.00902](https://arxiv.org/abs/2111.00902) |
| EfficientDet-Lite0 / SSD-MobileNetV2 | 25.7 / 22.1 | Pixel 6 CPU 29–61 ms / 36 ms | — | [MediaPipe](https://developers.google.com/edge/mediapipe/solutions/vision/object_detector) |

**COCO has no rabbit class.** It has cat, dog and teddy bear. The office rabbit is today mislabelled "stuffed toy" (memory `people-pets-object-class`), which matches. LVIS and Objects365 do have rabbit ([LVIS](https://arxiv.org/pdf/2201.02605)), and Open Images likely does ([Ultralytics OIv7](https://docs.ultralytics.com/datasets/detect/open-images-v7)). That gives three options: an open-vocabulary model, an Objects365/OIv7-trained checkpoint, or fine-tuning a nano detector on our own rabbit frames.

**Plain PyTorch or ONNX on the CPU is 30–80 ms; OpenVINO on a recent Intel CPU is 3–10 ms.** The laptop's CPU model decides which applies, so measure it.

### 2.2 Open-vocabulary "lite"

| Model | Quality | Speed | Note |
|---|---|---|---|
| **YOLOE-v8-S** | 27.9 LVIS AP (text prompt), +3.5 over YOLO-Worldv2-S | 305.8 FPS T4 TRT; 64 FPS iPhone 12 | **re-parameterises to a plain YOLO graph with zero overhead** once the vocabulary is fixed, so it runs at nano-YOLO speed; also has a prompt-free mode ([YOLOE](https://github.com/THU-MIG/yoloe)) |
| YOLO-World-S | 18.5–26.2 LVIS AP | 74 FPS V100; **no published Orin number** | `set_classes()` bakes an offline vocabulary into an exportable YOLO ([Ultralytics](https://docs.ultralytics.com/models/yolo-world)) |
| NanoOWL (OWL-ViT B/32, TRT) | 28 mAP | 95 FPS **AGX** Orin; Orin Nano "TBD" | [NanoOWL](https://github.com/NVIDIA-AI-IOT/nanoowl) |
| OWLv2 | — | ~400+ ms on Jetson | too slow ([NVIDIA forum](https://forums.developer.nvidia.com/t/nanoowl-inference-takes-more-time-than-nanoowl-official-github-shows/293051)) |
| Grounding DINO | — | 4.1 FPS Orin Nano, 6.2 Super ([Jetson AI Lab](https://www.jetson-ai-lab.com/archive/benchmarks.html)); 1.5 Edge 10.7 FPS Orin NX but API-only ([arXiv 2405.10300](https://arxiv.org/abs/2405.10300)) | resolve-time only, not trigger-time |

**Use for this rig** *(synthesis)*: a fixed vocabulary of {person, rabbit, cat, dog, shoe, cable, bag, toy, box, …} baked into YOLOE or YOLO-World gives a nano-speed detector that includes "rabbit". A closed list still cannot catch *the truly unknown*; that is the geometric layer's job.

### 2.3 Fingerprints / re-ID (for subtracting the *known*)

| Model | Speed | Source |
|---|---|---|
| CLIP ViT-B/32 | 196 FPS Orin Nano, 314 FPS Super | [Jetson AI Lab](https://www.jetson-ai-lab.com/archive/benchmarks.html) |
| DINOv2-base/14 | 75 FPS Orin Nano, 126 FPS Super | same |
| DINOv2 ViT-S/14 | ~10 ms FP16 on Orin Nano ([arXiv 2609.14247](https://arxiv.org/pdf/2609.14247)); 1.1 s on a phone CPU at 448² ([LiteRT card](https://huggingface.co/litert-community/DINOv2-ViT-S14-LiteRT)) | **no laptop-CPU number found; measure** |
| OSNet (person re-ID) | >10× smaller than ResNet-50 re-ID ([arXiv 1905.00953](https://arxiv.org/pdf/1905.00953v3)); detection + re-ID up to 29 FPS on the original Jetson Nano ([embedded.com](https://www.embedded.com/?p=4463084)) | |
| NanoSAM (crop masks) | ~27 ms full pipeline Orin Nano vs 146 ms MobileSAM | [NanoSAM](https://github.com/NVIDIA-AI-IOT/nanosam) |
| ORB | ~15–16 ms per 1000 features at VGA on one core (ORB-SLAM-era figure, secondary source) | [Rublee 2011](https://mlanthology.org/iccv/2011/rublee2011iccv-orb) |

Embedding a few remainder crops per check costs ~10 ms each on an Orin. That is affordable **on the remainder only**, not on every frame region. Caveat already in the wiki: raw DINOv2 in-the-wild instance top-1 is 47 % against a ~43–50 % chance floor ([[locate-object-from-last-known-position]]). Fingerprints separate *the* rabbit from *a* chair in a small household gallery; they are not a safety signal. No edge pet re-ID source was found.

### 2.4 Stereo depth (the generic, class-free detector)

| Method | Speed | Source |
|---|---|---|
| OpenCV StereoBM | 6.4 ms at 640×512, 128 disp, i7 | [OpenCV Q&A](https://answers.opencv.org/questions/73044/revisions) |
| OpenCV StereoSGBM | no clean published VGA number; **measure** (expect tens of ms on CPU at VGA, est.) | [perf test](https://sources.debian.org/src/opencv/4.5.1%2Bdfsg-5/modules/calib3d/perf/perf_stereosgbm.cpp) |
| Isaac ROS SGM (VPI) graph | **Orin Nano 66 fps / 17 ms** | [isaac_ros_benchmark](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_benchmark) |
| Isaac ROS ESS (learned) | full 576p: Orin Nano Super 34.8 FPS / 30 ms; **light 288×480: 82 FPS / 13 ms** (an older node-level table says ~5 FPS on the original Orin Nano, treat as unoptimised) | [ESS](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_dnn_stereo_depth) |
| ESMStereo-S | 91 FPS AGX Orin TRT FP16 | [arXiv 2506.21091](https://arxiv.org/html/2506.21091) |
| HITNet / LightStereo-S / BGNet+ | 20 / ~17 / 35 ms on a desktop GPU; no Orin Nano numbers | [LightStereo](https://arxiv.org/html/2406.19833v3) |

Learned stereo (ESS-light) matters here because it **fills textureless floor and walls better than SGM**. Passive SGM starvation is this rig's best-documented weakness ([[sensor-weaknesses-and-fixes]]). If it falls short, the cheap escalation is an IR dot projector ([[economical-ir-depth-cameras]]).

### 2.5 Monocular depth, flow, segmentation

- **Monocular depth**: Depth Anything 3-Small at 640×480 runs 43+ FPS (~23 ms) on Orin NX with TRT ([ROS discourse](https://discourse.openrobotics.org/t/depth-anything-3-ros-2-wrapper-development/51030)); MiDaS-small 8 FPS on the original Nano ([README](https://huggingface.co/spaces/FazeNCode/MiDaS/blame/3590500d03026a669c500c677f226b2ea7938929/MiDaS-master/ros/README.md)). Relative depth only. Useful as a **texture-free hole filler** fused with stereo, not as the metric source.
- **Optical flow**: DIS runs 300–600 Hz on one core at 1024×436 ([arXiv 1603.03590](https://arxiv.org/abs/1603.03590)); VPI OFA hardware dense flow runs ~30–50 FPS at 1080p on Orin NX ([forum](https://forums.developer.nvidia.com/t/dense-optical-flow-is-slow-on-jetson-orin-nx-16gb/271594)); NeuFlow ~30 FPS on Orin Nano ([arXiv 2403.10425](https://arxiv.org/abs/2403.10425)).
- **Segmentation**: PIDNet-S 93 FPS on RTX 3090 ([arXiv 2206.02066](https://arxiv.org/pdf/2206.02066)); PP-LiteSeg-T 274 FPS on 1080Ti ([arXiv 2204.02681](https://arxiv.org/pdf/2204.02681)); Isaac PeopleSemSegNet 1.8 ms on Orin Nano ([isaac_ros_benchmark](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_benchmark)). No published floor-segmentation numbers on Orin Nano. A learned floor mask is an option if the geometric floor fit is noisy, but it is a second-stage refinement.

### 2.6 Moving-camera change detection

Static pixels follow the flow predicted by rigid ego-motion, so independent movers leave a residual in flow or in reprojected depth ([arXiv 1707.01307](https://arxiv.org/pdf/1707.01307)). Known failure modes ([survey, arXiv 2001.05238](https://arxiv.org/pdf/2001.05238)):
- parallax in deep scenes
- light switches
- **auto-exposure and white balance**, which matter because the SVPRO needs seconds to settle
- jitter and camouflage

Do the residual **in depth, not intensity**, and gate on persistence. It catches only *movers*. **Big simplification for this rover:** it is a stop-and-scan robot, so it spends much of its time stationary at stations (sweeps, relocalisation). With the camera still, plain frame differencing has no ego-motion to compensate. "Something moved while I stood here" is nearly free and catches the rabbit hopping past.

### 2.7 What does not fit (and why)

| Approach | Verdict | Evidence |
|---|---|---|
| NeRF / 3DGS "expected image" render + photometric diff | **Too heavy and too fragile.** 3DGS runs 2–5 FPS on *AGX* Orin on large real scenes ([arXiv 2507.21572](https://arxiv.org/pdf/2507.21572)); faster variants (SEELE ~20 FPS, GauRast) are AGX-class or need hardware changes ([arXiv 2503.16681](https://arxiv.org/html/2503.16681v2)). The Orin Nano is much smaller, and a photometric diff inherits every lighting and exposure failure. Render expected **depth** from boxes and walls instead. | demoed |
| Road-anomaly segmenters (RbA, Mask2Anomaly) | **Wrong domain and too slow.** RbA leads SegmentMeIfYouCan but takes ~0.18 s per image on an **A100** ([arXiv 2211.14293](https://arxiv.org/pdf/2211.14293)); Mask2Anomaly has no FPS published ([ICCV 2023](https://openaccess.thecvf.com/content/ICCV2023/papers/Nandan_Unmasking_Anomalies_in_Road-Scene_Segmentation_ICCV_2023_paper.pdf)). Trained on road inlier classes, so they need retraining for a home floor. | demoed |
| Industrial anomaly models (PatchCore, EfficientAD) | **Fixed-viewpoint methods.** PatchCore 119 ms and EfficientAD 34.7 ms on Jetson ([arXiv 2605.24251](https://arxiv.org/pdf/2605.24251)), but every new viewpoint looks novel. Memory banks keyed per station pose are *speculative*. DeepAnomaly worked over a homogeneous field ([PMC5134563](https://pmc.ncbi.nlm.nih.gov/articles/PMC5134563)); a cluttered room is not homogeneous. | demoed (wrong regime) |
| Event cameras | **Not now.** Microsecond latency buys nothing at 0.10 m/s, and on a moving robot almost every edge fires, so ego-motion compensation is back ([arXiv 2507.14500](https://arxiv.org/pdf/2507.14500)). Prophesee GenX320 RPi5 kit is informally ~$300–400 ([Hackster](https://www.hackster.io/news/event-based-vision-pioneer-prophesee-launches-a-genx320-starter-kit-for-the-raspberry-pi-5-8c3a48ad0ef1)); DVXplorer Micro is €2,400 academic ([iniVation](https://shop.inivation.com//products/dvxplorer-micro-academic-rate)). A possible later "moved while stationary" sensor. See [[event-cameras]]. | shipping (sensor), speculative (use) |
| VLM per frame | Resolve-time only (seconds), never the trigger. | — |

---

## 3. Safety-architecture pattern for the separate fast process

- **Simplex / run-time assurance**: an untrusted advanced controller, a verified simple safe controller, and a switch that acts on predicted boundary violation ([arXiv 2110.03506](https://arxiv.org/pdf/2110.03506), [Black-box Simplex](https://arxiv.org/pdf/2102.12981)).
- **Nav2 Collision Monitor**: an independent node *below* the planner that filters `cmd_vel` and bypasses costmaps. It has stop and slowdown polygons with a `min_points` threshold as the debounce, and the most aggressive action wins ([Nav2 docs](https://docs.nav2.org/configuration/packages/collision_monitor/configuring-collision-monitor-node.html)). This is the closest off-the-shelf analogue of a LiDAR guard plus a visual trigger feeding one arbiter. See [[ros2-nav2]].

**Recommended shape for the rover** *(synthesis, fits drone-prototype rule 1 T1 jobs and the child-process cognition split of PR #205)*:
1. **Own process, own watchdog, no imports from cognition.** It publishes a HOLD *request* to the body's arbiter. The LiDAR guard stays the hard stop, and the visual trigger is a **gentle hold** that RESUME can continue, as the human specified. Stale frames, a failed floor fit or a camera timeout publish `uncertain`. While driving that means hold; in manual mode it means warn only.
2. **Asymmetric hysteresis.** Fire on K-of-N (e.g. 3-of-5 at 5 Hz) with a minimum blob size and point count. Clear only after M consecutive clean checks *plus* RESOLVE's verdict. This is the anti-nuisance-stop lever the human asked for ("don't get locked into over-caution").
3. **Semantics only relax or route a hold; they never create the safety guarantee.** A person detection with no geometric blob may still hold, since a detector hit is cheap evidence. "Known object, at its bank position" turns a geometric remainder into a no-op.
4. **Trigger readings stay out of the map and the bank** (human answer 6). The visual trigger's blobs carry a `transient` tag that ingest honours.

---

## 4. Candidate architectures for this rover

All three run as one separate fast process feeding HOLD → RESOLVE → RESUME. They are **staged, not exclusive**: A is the core, B adds labels, C adds motion. Rates marked *est.* are budgets assembled from §2, not measurements.

### A. Geometric expectation subtraction (stereo free-space violation) — **the core**

- **Sensors:** stereo pair at reduced resolution (e.g. 640×360 per eye); pose from the live localiser plus odometry; floor plane; the live LiDAR plane.
- **Pipeline:**
  1. Disparity: SGBM on the laptop; VPI-SGM or ESS-light on a Jetson.
  2. Per-frame RANSAC floor fit, seeded by the calibrated camera height and pitch. The fit doubles as a sensor-health check.
  3. Height-above-floor mask over a forward corridor (footprint width plus margin, ~0.3–2 m ahead, heights from ~3 cm up to the robot height 0.53 m).
  4. Subtract the **expected geometry**: map walls, bank objects (cuboid outlines, inflated by the pose-error band) and the live LiDAR-plane returns already handled by the guard.
  5. Connected-component blobs with a K-of-N persistence → HOLD.
- **Rate:**
  - Laptop CPU: ~5–10 Hz *est.*, dominated by SGBM. Measure it.
  - Orin Nano: SGM 17 ms or ESS-light 13 ms + a few ms of CPU geometry → **20–50 Hz est.**
- **Catches:** anything solid ≥ ~5–10 cm tall within ~1.5–2 m: the **rabbit below the LiDAR plane**, people's legs and feet, a lying person, new boxes and bags, a moved chair. No classes needed. This is how Subaru, Lost and Found and the OTTO depth cameras work.
- **Misses or fails:**
  - Textureless or dark objects on a plain floor (SGM holes; the rabbit on a dark mat).
  - Glass and mirrors.
  - Cords, tape and flat items under ~3 cm (which the human already rules drivable).
  - Anything beside the robot, outside the forward field of view.
  - The band under the bumper.
  - **False remainders from localisation or bank error**: a 5 cm pose error makes a known chair look "new". Hence the tolerance band, and why rule `plan-from-live-maps` matters.
- **Cost:** lowest. OpenCV plus the existing calibration, extrinsic, localiser and bank. No model downloads. About one EDA plus one module.

### B. A + nano detector + fingerprint re-ID on the remainder — **the labels**

- **Added models:**
  - A fixed-vocabulary detector every frame or every other frame: YOLOE-S or YOLO-World-S re-parameterised with {person, rabbit, cat, dog, toy, shoe, bag, box, cable}, or YOLO26n fine-tuned with our own rabbit and person frames.
  - DINOv2-S or CLIP-B/32 embeddings **only on the remainder blobs and detections**, matched against the bank and a people/pets gallery (memory `people-pets-object-class`).
- **Rate:**
  - Detector: 3–10 ms OpenVINO on a recent Intel CPU (30–80 ms in plain ONNX), ~4–5 ms TRT FP16 on Orin Nano Super.
  - Embeddings: ~5–10 ms each on Orin.
  - Total on Orin with A: **~10–20 Hz est.** On the laptop, ~3–8 Hz *est.*, depending on whether OpenVINO applies.
- **Catches (beyond A):**
  - A person or pet *anywhere in view*, including far away or partly occluded, before they enter the corridor.
  - Textureless people and pets where stereo starves.
  - Gives RESOLVE its class: person → wait or replan; rabbit → plan around; known object → no-op; unknown → no-go plus a discovery task.
- **Misses or fails:**
  - Detector false positives (posters, the rabbit's stuffed-toy look-alikes) and misses on sitting or crouching people ([SEEN critique](https://seen-safety.squarespace.com/ai-cameras-for-mhe)).
  - Any class outside the vocabulary (A covers those).
  - Fingerprints are weak identity evidence (47 % raw DINOv2 instance top-1).
  - "Rabbit" quality in open-vocabulary models is unmeasured on our frames.
- **Cost:** moderate. One small model export (~5–25 MB, not "large") plus a labelling pass on recorded frames. Do not add it until A's remainder rate on recorded runs is known.

### C. Motion layer: stationary differencing + ego-compensated depth residual — **the movers**

- **Sensors:** stereo depth (or the left image while stationary), IMU and encoder odometry.
- **Pipeline:**
  - Stationary (at stations, during holds): frame-to-frame depth or image differencing with exposure locked or normalised.
  - Moving: reproject the previous depth with odometry, take the residual, then K-of-N.
  - Optional: DIS flow on the CPU or the Orin OFA for a flow residual.
- **Rate:** a few ms on top of A (reuses A's disparity); DIS hundreds of Hz.
- **Catches:** the rabbit or a person **moving** (even far out or beside the corridor); "is it still moving?" for RESOLVE; whether a hold self-resolved.
- **Misses or fails:**
  - Static new objects (A covers those).
  - Parallax and auto-exposure false positives while moving.
  - Odometry error (the rover crabs 6.6 %/m), so moving-mode residuals need generous tolerances.
- **Cost:** low for the stationary version; moderate for the moving version.

### Summary

| | A geometric subtraction | B + detector / re-ID | C motion |
|---|---|---|---|
| Rabbit below LiDAR plane, in corridor | yes, if textured | yes (if "rabbit" works) | if it moves |
| Person | legs and feet in corridor | **yes, anywhere** | if moving |
| New / moved object | **yes** | only in vocabulary | no |
| Needs classes or models | no | yes | no |
| Laptop rate (est.) | 5–10 Hz | 3–8 Hz | +few ms |
| Orin Nano rate (est.) | 20–50 Hz | 10–20 Hz | +few ms |
| Main false-trigger source | pose / bank error, SGM holes | look-alikes | parallax, exposure |

**Recommended order** *(synthesis)*:
1. Build **A** first and measure its remainder ("null set") rate on recorded office runs, with the human and the rabbit present and absent.
2. Add **C-stationary**, which is nearly free.
3. Add **B's detector** for the person/pet class that RESOLVE needs.
4. Add fingerprint re-ID last.

This mirrors every shipping system (geometry stops, classes steer) and keeps the trigger path model-free, so it cannot be silently broken by a detector miss.

---

## 5. Open questions (measure on the rig)

1. **SVPRO stereo floor separation**: the real minimum detectable height vs range at 0.26 m on the hardwood and on the rubber mat (memory `office-two-surfaces`), and SGBM coverage on the office floor. Does a dark rabbit on a dark mat survive?
2. **Camera field of view and near-field blind band**: the camera pitch and the closest visible floor distance. Is a side-approaching rabbit visible before it reaches the footprint?
3. **Laptop CPU rates**: SGBM at 640×360, YOLO26n under OpenVINO vs ONNX, DINOv2-S. None of these has a published number for this CPU.
4. **Null-set rate**: how often does expectation subtraction leave a false remainder from localisation and bank error, per metre driven? This sets K-of-N and the tolerance band.
5. **"Rabbit" in open vocabulary**: YOLOE / YOLO-World recall on our rabbit frames vs fine-tuning a nano model.
6. **Auto-exposure behaviour** during driving (needed for C).
7. **Hardware escalation trigger**: if passive stereo starves on the floor, the IR dot projector rung ([[economical-ir-depth-cameras]]) is the consumer-cost fix; a 3D LiDAR is out ([[passive-stereo-robustification]]).
8. **Jetson variant**: Orin Nano vs Nano Super vs NX numbers differ 1.4–2×. Pin it before treating any Orin number above as a budget.

Weak or unverified figures excluded from this page: a DINOv2-L 8.7 ms on Orin Nano claim (implausible), a RAFT-small Orin figure from a glossary site, and a YOLO-World-Edge Orin number from a non-public host.
