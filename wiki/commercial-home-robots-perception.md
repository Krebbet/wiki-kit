# Commercial Home Robot Perception Stacks

What is publicly known about the perception and mapping stacks of commercial home robots with meaningful autonomy *beyond* robot vacuums — Amazon Astro, Dyson 360 Vis Nav, Samsung Ballie, Matic, and Bear Robotics Servi. The framing question for this wiki: which architecture choices and lessons transfer to a ground robot doing home tidying tasks?

*Note: Dyson 360 Vis Nav and Matic are technically robot vacuums, but included here because their perception approaches are architecturally more ambitious than the commodity disc-vacuum field and directly relevant to a camera-only ground robot.*

---

## Amazon Astro

The highest-density primary technical record in this space. Amazon published two separate technical blog posts (Amazon Science, 2021) detailing Intelligent Motion.

### Sensor configuration

Astro has two distinct sensor subsystems with distinct roles [`01-astro-intelligent-motion.md`]:

- **Navigation sensors** — used for SLAM landmark tracking; identify positions of key landmarks in 3D space (corners of tables, doorframes). Purpose: figure out *where Astro is* relative to known landmarks.
- **Obstacle sensors** — build a detailed local distance map of immediate surroundings (couches, chairs, walls, stairs). Purpose: *path planning and collision avoidance*, not map-building.
- **Visible + infrared light** computer vision — gives "robust perception in dynamic environments and varying lighting conditions" [`01-astro-intelligent-motion.md`]. Specific sensor types (camera model, structured-light, ToF) are not disclosed.
- **Wheel encoders + IMU** — fused with navigation sensors for localization robustness [`02-astro-localization.md`].

Amazon does not publicly describe whether the navigation sensors include a LIDAR, depth camera, stereo pair, or some other modality. The periscope camera (a 12-megapixel, 132° FOV camera that extends to 42 inches for surveillance tasks) is documented in product pages but its role in navigation vs. security vs. person-following is not separated in the science blog posts.

### V-SLAM architecture

Astro's Intelligent Motion system is explicitly **visual SLAM (V-SLAM)** [`02-astro-localization.md`]:

- **Frontend:** visual odometry — extracts visual features from sensor data, establishes correspondences, tracks features frame-to-frame to estimate sensor movement.
- **Loop-closure detector** — matches current frame features against previously-seen features to correct accumulated visual odometry drift.
- **Nonlinear optimizer** — processes visual features, estimated sensor poses, and loop-closure information to obtain a global motion trajectory and map. Implements **bundle adjustment** — simultaneous refinement of 3D scene coordinates, relative motion estimates, and optical camera characteristics — computationally efficient enough to produce **6-DOF pose multiple times per second** on-device [`02-astro-localization.md`].
- **Long-term multi-layer mapping:** higher-level layer (which rooms Astro can visit) to lower-level layer (appearance of objects on the floor). Compression and pruning keep memory within onboard limits while preserving map utility [`02-astro-localization.md`].

All SLAM runs **on-device**. The 2D obstacle map plus derived map info (walls, rooms, boundaries, furniture, customer-provided room names) is sent to cloud *only at the completion of an exploration run* — not during navigation. Raw sensor data is discarded locally after processing [`01-astro-intelligent-motion.md`].

### Handling home dynamics

Astro's V-SLAM was explicitly designed around the dynamic home problem — a hard deviation from academic V-SLAM assumptions [`02-astro-localization.md`]:

- **Short-term dynamics:** pets, people.
- **Medium-term dynamics:** moved boxes, chairs, bags.
- **Long-term dynamics:** holiday decorations, furniture rearrangements, structural renovations.
- **Lighting changes:** sun moving through the day, lights turned on/off; must operate in total darkness.

Solution: deep learning trained on millions of image pairs (captured + synthesized) depicting similar scenes at different times of day, lighting conditions, occlusions, object movements. Produces lighting-invariant visual representations. Sensor fusion handles individual sensor failures: IMU saturation when crossing floor thresholds, wheel slip on rugs, lift-off events [`02-astro-localization.md`].

### Person following and room understanding

Astro can distinguish **person-obstacles** from **avoid-obstacles** and follow a person instead of routing around them, even when the person moves in and out of Astro's field of view. Person-following uses computer vision signals (approximate position, direction the person faces), the stored map, and inputs from navigation + depth sensors for proxemics-aware path planning at "socially appropriate distance" [`01-astro-intelligent-motion.md`].

Room understanding: the stored map contains room boundaries and customer-provided room names — sufficient for "go to this room" tasking. Semantic labelling of rooms is user-applied (via app), not vision-inferred from appearance.

### Path planning

Intelligent Motion generates **several hundred potential paths several times per second**, evaluates each, and selects. Evaluation factors: likelihood of environmental changes, smoothness, obstacle probability. Novel dimensionality reduction + probabilistic planning methods claimed [`01-astro-intelligent-motion.md`].

---

## Dyson 360 Vis Nav

Camera-only SLAM; no LiDAR. The only widely-deployed consumer robot vacuum using a panoramic fisheye for navigation (vs. the LDS-SLAM canon).

### Sensor configuration [`07-dyson-360-vis-nav-launch.md`, `10-dyson-360-vis-nav-ambient-review.md`]

- **360° fisheye camera** — 1080p, 30 fps. Captures full panoramic view. Core SLAM sensor.
- **8 LED sensors** — illumination for the fisheye camera (low-light operation support).
- **26 sensors total** — breakdown: dust detection (piezo sensor), obstacle avoidance sensors, wall-detection sensors (wall-follow for edge cleaning).
- **Optical flow sensors** — used alongside the camera and distance sensors for navigation [`10-dyson-360-vis-nav-ambient-review.md`].

No depth sensor (ToF, structured-light, stereo) is disclosed. The fisheye is the only image sensor documented for navigation. The 26-sensor total implies a dense array of 1D range sensors (IR distance, ultrasonic, or cliff sensors) for obstacle avoidance — distinct from the navigation camera.

Note from independent review: the camera is **not used for smart object avoidance** (cables, pet mess). Obstacle avoidance is handled by the dedicated obstacle sensors, not vision-based classification [`10-dyson-360-vis-nav-ambient-review.md`]. This mirrors the vacuum industry pattern of separate nav-layer and collision-layer.

### SLAM approach

"Dyson Simultaneous Localisation and Mapping (SLAM)" — proprietary, camera-only visual SLAM using the fisheye images. Position accuracy: "within 71mm" (Dyson claim) [`07-dyson-360-vis-nav-launch.md`]. The SLAM system must visit a space to include it on the map — no pre-scanning (confirmed by independent reviewer comparison to LiDAR which can scan ahead) [`10-dyson-360-vis-nav-ambient-review.md`].

Map storage: supports multiple floor maps (one per floor/area). Initial mapping run required before zone cleaning. Zones can be labelled, assigned power modes, scheduled. Map is used for room-level cleaning selection and "avoid area" no-go zones.

Mapping speed: slower than LiDAR-based robots per independent review (camera processing vs. instant scan) [`10-dyson-360-vis-nav-ambient-review.md`]. Robot behaviour during navigation: pauses mid-run (motor powers down briefly) — reviewer interpreted as computational planning time.

Dyson does not publish technical details of the SLAM algorithm itself (no science blog equivalent to Amazon's).

---

## Matic

The most technically transparent camera-only home robot in this set — co-founders published detailed technical reasoning. Still primarily a floor-cleaning robot, but the perception architecture is the most directly transferable to a ground tidying robot.

### Sensor configuration [`03-matic-vision-first.md`, `04-matic-design.md`, `08-matic-stealth-launch.md`]

- **5 RGB cameras with near-IR capability** — sole sensor suite for SLAM and navigation.
- **No IMU** — explicitly stated by co-founder: "We don't even use an IMU at the moment" [`03-matic-vision-first.md`].
- **No LiDAR, no depth sensor.**
- **IR LED illuminators** on crown (top) and back cameras — invisible to humans, illuminate space for grayscale camera operation in total darkness. Night cleaning is fully supported.
- **Camera height:** approximately 8 inches from floor (elevated above disc-robot ant's-eye level, giving a crawling-child-like vantage point for better floor and obstacle visibility).

Compute: **Nvidia Jetson Orin Nano, 4 GB RAM**. All processing on-device; nothing leaves the home. Earlier interview reference to "equivalent to an iPhone 6" compute was pre-hardware-finalization; Jetson Orin is the shipping platform [`03-matic-vision-first.md`, `09-matic-techcrunch-2023.md`].

### SLAM architecture

Hybrid classical + neural network approach [`03-matic-vision-first.md`]:

- **Image-to-voxel neural network:** images → depth estimation → 1 cm³ voxel representation → 3D map rebuilt on the fly ("Google Street View-like 3D map").
- **Absolute map** (not relative-to-dock): dock is just another landmark in the map, not the reference origin. Enables relocalization from any starting position regardless of where the robot is placed. This contrasts with typical robots that build maps relative to the dock and fail if placed away from it.
- **Long-term SLAM:** map persists and updates. The robot can re-localize into a known map even if placed mid-room with the crown covered and moved.

Co-founder's assessment of open-source SLAM: "70-80% accurate" at time of founding (2017-2020); Matic rebuilt from scratch in fall 2020. Their claim: 10x better than SOTA or open-source alternatives — unverified externally [`03-matic-vision-first.md`].

Precision claimed: 1.5 cm [`09-matic-techcrunch-2023.md`] (Dalal's stated claim; not independently verified).

### Architecture rationale *(from primary source, not synthesis)*

Co-founder Mehul Nariyawala articulated the vision-only bet explicitly [`03-matic-vision-first.md`]:

> "The indoor world, specifically homes, is built by humans for humans to fit our perception system. It's optimized for a vision-based system."

The sensor-minimization logic: each additional sensor adds 2-3 software engineers permanently, increases manufacturing complexity, adds failure points, and raises calibration burden. 5 cameras = sole sensor type = complexity asymptotes in software, enabling OTA improvements without hardware changes.

Privacy: no cloud processing, no data collection; this was "non-negotiable" and drove the on-device architecture choice (along with latency requirements) [`03-matic-vision-first.md`].

Roadmap: floor cleaning is step 1; manipulation and tidying are explicitly on the roadmap. Co-founder references vision of a "Rosie the Robot" via staged progression: perception → manipulation → full home tasks [`03-matic-vision-first.md`].

---

## Samsung Ballie

Least technically documented; most of what is publicly known comes from CES 2024 press release and reporting.

### Sensor configuration [`05-ballie-ces2024-techcrunch.md`]

- **Spatial LiDAR sensor** — for navigation and obstacle avoidance (confirmed in TechCrunch CES 2024 report).
- **Front and rear cameras** — described as "built-in front [and] rear camera" for environmental sensing, user pattern detection, and projector-function (1080p projector with two lenses).
- No specification of depth cameras, ToF, or stereo confirmed in available sources.

### Navigation and mapping

Maps floor plan, identifies where smart devices might be located inside a home [`05-ballie-ces2024-techcrunch.md`]. Claims to "detect and analyze its surroundings and learn recurring user patterns." Details of the mapping algorithm, cloud vs. onboard processing, or semantic room understanding are not disclosed in captured sources.

Samsung's 2025 announcement of a Gemini AI integration (Google Cloud partnership) suggests cloud-reliance for higher-level intelligence, but the navigation stack specifics remain opaque. Ballie has been repeatedly delayed (not yet commercially shipping as of 2026).

---

## Bear Robotics Servi

Commercial service robot for restaurants, not homes. Included for architecture comparison: the only robot in this set that is both fully deployed at commercial scale and uses a documented sensor fusion stack.

### Sensor configuration and approach [`06-bear-robotics-servi.md`]

- **LiDAR** — primary navigation sensor; "intelligent LiDAR navigation" is the lead product description.
- **Cameras** — used alongside LiDAR for obstacle detection. FAQ: "LiDAR and cameras to map its environment."
- **Ultrasonic sensors** — documented for Servi Plus variant.

Architecture is **classical LiDAR-SLAM**: maps the restaurant on installation, navigates against the map, rerouts in real time around dynamic obstacles. Installation in "as little as 14 minutes" for a 1,000 sq ft space.

Fleet management: cloud-based centralized Fleet Control Suite for multi-robot orchestration, behavioral data tracking, remote troubleshooting. Not privacy-preserving by design — commercial context makes this appropriate.

**Scope note:** Servi operates in structured commercial environments (restaurant with known table layouts, limited human flow patterns, no stairs, no pets). This is significantly easier than home navigation. The LiDAR-SLAM stack is conservative and appropriate for the use case, not a technology bet.

---

## Cross-Source Themes *(synthesis)*

These are interpretive claims derived from patterns across the captured sources, not statements from any single source.

### 1. Vision-only vs. LiDAR is a live split

Three of the five robots above use LiDAR (Ballie, Servi, and indirectly through Astro's undisclosed "navigation sensors"). Two commit fully to camera-only (Dyson 360 Vis Nav, Matic). The Matic founder explicitly frames the choice as a deliberate architectural philosophy — sensors drive exponential complexity, cameras-only keeps the stack manageable. Dyson chose vision-only for different reasons (the brand's vacuum-first identity; no published architectural rationale). Amazon's Astro is the most opaque — V-SLAM confirmed but sensor modalities not disclosed.

The split maps to [[lidar-vs-vision-autonomy]]: neither camp has decisively won in commercial home robot deployment.

### 2. Two separate sensor layers (nav vs. collision) are the norm

Astro, Dyson, and commodity vacuums (see [[robot-vacuum-navigation]]) all separate:
- **Navigation/SLAM layer** — builds the persistent map, localizes.
- **Obstacle avoidance layer** — local reactive collision avoidance, decoupled from map-building.

Dyson's review explicitly confirms the fisheye camera does *not* handle cable/pet-mess avoidance — that's the 26-sensor array. This pattern is load-bearing: the obstacle layer runs at higher frequency and lower latency than the SLAM layer.

### 3. Persistent absolute maps are the differentiator

The commodity vacuum baseline is relative-to-dock maps that break when the robot is displaced (see [[robot-vacuum-navigation]]). Matic's "absolute map" innovation (dock as just another landmark) and Astro's multi-layer long-term map both represent the next generation of persistent home maps — relocalize from any starting point, survive furniture moves and lighting changes.

### 4. Semantic room understanding is shallow and user-labelled in all cases

None of these robots *infer* room identity from appearance alone (e.g., recognizing "this is a kitchen" from visual appearance). Room identity is user-labelled via app in Astro and Dyson. Ballie claims pattern learning but no mechanism is disclosed. The hard semantic room understanding problem — identifying which room this is from appearance, without user labelling — remains unsolved in commercially deployed systems. This contrasts with the research frontier in [[scene-graph-world-model]] (Hydra, ConceptGraphs).

### 5. Cloud vs. onboard is a design value, not a capability constraint

Matic and Astro both run SLAM fully on-device, citing privacy and latency. Matic is the most radical (literally zero cloud processing without opt-in). Astro processes navigation on-device but pushes the derived map to cloud for app display and storage. Servi uses cloud fleet management. The technical capacity for full on-device operation exists at consumer compute (Jetson Orin Nano, 4GB); the choice is privacy philosophy.

### 6. What transfers to a home tidying ground robot *(editorial)*

Ordered by transferability:

1. **Matic's camera-only SLAM architecture is the most directly transferable.** The image-to-voxel NN producing 1cm³ voxels + absolute map on 4GB Jetson Orin Nano is the closest published stack to what a ground tidying robot would need. Vision-only = no LiDAR cost or weight; on-device = no cloud latency or privacy risk. The obstacle: it is not open-source and Matic's "10x better than SOTA" claim is unverifiable.

2. **Astro's multi-layer long-term map design is the right conceptual model.** Room-level understanding + object-level understanding in separate map layers with different update rates — this is what [[world-model-architecture]] describes for our project.

3. **The nav-layer / collision-layer split should be preserved.** Do not combine SLAM-quality map-building with reactive obstacle avoidance in the same sensor+algorithm. The Dyson failure mode (camera used for nav only, separate array for collision) is actually *correct separation* — the reviewer who noted cables aren't avoided via camera was describing architecture, not a flaw.

4. **Absolute maps (dock as just another landmark) are strictly better** than relative-to-dock maps for a home robot that moves between docking sessions. This is consistent with the anchor map protocol ([[anchor-map-protocol]]) — building maps that can be re-entered from any starting position.

5. **Ballie and Servi transfer least.** Ballie is vaporware (repeated delays, no shipping product). Servi is structured commercial environment with LiDAR — correct for restaurants, over-engineered with wrong assumptions for home.

---

## Source

| File | Origin | Title | Notes |
|---|---|---|---|
| `raw/research/commercial-home-robots/01-astro-intelligent-motion.md` | Amazon Science · amazon.science/blog | *Astro's Intelligent Motion brings state-of-the-art navigation to the home* | Primary: V-SLAM architecture, sensor layers, person-following, path planning, privacy model |
| `raw/research/commercial-home-robots/02-astro-localization.md` | Amazon Science · amazon.science/blog | *How does Astro localize itself in an ever-changing home?* | Primary: V-SLAM internals (frontend, loop closure, bundle adjustment), sensor fusion (encoders+IMU), dynamic-home challenge, multi-layer map |
| `raw/research/commercial-home-robots/03-matic-vision-first.md` | maticrobots.com/blog | *Inside Matic's 7-Year Journey To Create Vision-Only Robots That See the World Like Humans* | Primary (co-founder AMA): 5-camera no-IMU no-LiDAR stack, Jetson Orin 4GB, image-to-voxel NN, absolute map, IR night vision, SLAM rebuild |
| `raw/research/commercial-home-robots/04-matic-design.md` | maticrobots.com/blog | *Reimagining Home Cleaning with Matic: The Design* | Primary (company blog): sensor overview, Jetson Orin, on-device voxel map, IR+RGB cameras, camera height rationale |
| `raw/research/commercial-home-robots/05-ballie-ces2024-techcrunch.md` | TechCrunch · techcrunch.com | *Samsung brings back Ballie, its home robot, at CES 2024* | Press coverage: spatial LiDAR, front/rear cameras, floor plan mapping, 1080p projector, user-pattern learning |
| `raw/research/commercial-home-robots/06-bear-robotics-servi.md` | bearrobotics.ai | *Servi: Hospitality's Best AI Robot Waiter Assistant* | Vendor page: LiDAR+cameras, cloud fleet management, 14-min install, restaurant-specific structured-env nav |
| `raw/research/commercial-home-robots/07-dyson-360-vis-nav-launch.md` | dyson.com | *Dyson launches the most powerful robot vacuum with six times the suction of any other* | Primary (Dyson press release): 360° fisheye SLAM, 26 sensors, 71mm accuracy, piezo dust sensor, no LiDAR |
| `raw/research/commercial-home-robots/08-matic-stealth-launch.md` | maticrobots.com/blog | *Matic comes out of stealth with $30M in funding* | Primary (CEO blog): 5-RGB-camera SLAM, on-device 3D map, privacy non-negotiable, first autonomous indoor robot claim |
| `raw/research/commercial-home-robots/09-matic-techcrunch-2023.md` | TechCrunch · techcrunch.com | *Matic's robot vacuum maps spaces without sending data to the cloud* | Press: 1.5cm precision claim, on-device only, floor-cleaning-as-mapping-vehicle framing, competitive context |
| `raw/research/commercial-home-robots/10-dyson-360-vis-nav-ambient-review.md` | The Ambient · the-ambient.com | *Dyson 360 Vis Nav review* | Independent review: fisheye+8 LED+26 sensors confirmed, camera not used for smart obstacle avoidance, mapping speed vs LiDAR, multiple map support |

---

## Related

[[robot-vacuum-navigation]] (vacuum-precedent nav stacks; nav-layer / collision-layer split established there) · [[scene-graph-world-model]] (research frontier for semantic room understanding these commercial systems fall short of) · [[world-model-architecture]] (the multi-layer map model — Astro's approach confirmed the direction) · [[lidar-vs-vision-autonomy]] (the open conflict; this page adds commercial evidence) · [[home-tidying-robots]] (ground-robot tidying systems; TidyBot etc.) · [[slam]] (SLAM hub) · [[indoor-cluttered-slam]] (the hard version of the problem) · [[anchor-map-protocol]] (absolute-map / multi-sweep approach for our project) · [[mapping-stack-design]] (what our rover is building toward) · [[close-range-depth-sensors]] (what Astro's undisclosed obstacle sensors might look like) · [[drone-sensors-for-autonomy]]
