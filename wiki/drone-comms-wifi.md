# Drone Comms over Home WiFi (ROS 2 + MAVLink)

Getting ROS 2 telemetry/commands between a Jetson Orin companion and a flight controller reliable over consumer WiFi means defeating one root cause — DDS default discovery uses multicast, which home APs handle badly — and routing MAVLink-over-UDP to multiple endpoints cleanly. Two distinct layers: the **DDS/RMW layer** (companion ↔ ROS 2 graph, on-host and over WiFi) and the **MAVLink layer** (FC ↔ GCS/companion). Fix each separately.

---

## The core failure mode: DDS discovery over WiFi

ROS 2's default RMW (Fast DDS) uses the **Simple Discovery Protocol (SDP)**, which relies on **UDP multicast** to find peers. DDS runs two phases: SPDP (Simple Participant Discovery — "who's around") and SEDP (Simple Entity Discovery — exchange every reader/writer). Discovery traffic scales roughly **n·(n−1)·(r+w)** — quadratic in participants — and every participant must retain all discovery state regardless of interest. DDS was designed for wired LANs with plentiful bandwidth and rare loss. *[`06-zenoh-discovery-blog.md`]*

Over WiFi this breaks two ways:

- **Multicast is mishandled by APs.** WiFi treats multicast as low-rate broadcast; without help it fragments and floods. A documented multi-drone (PX4 + mocap → MAVROS) case saw the mocap stream "morse-code" drop — up to 1 s of total packet loss, enough to crash drones — triggered the instant a third vehicle joined, and reproducible by switching one drone from Ethernet to WiFi. Root cause: discovery multicast over WiFi. *[`11-ros2-wifi-igmp-discourse.md`]*
- **Quadratic metatraffic.** SDP makes every node announce itself and await replies from every other node — a flood that worsens with node count. *[`03-fastdds-discovery-server.md`, `04-vulcanexus-wifi.md`]*

Two classes of fix: keep DDS but **kill multicast discovery** (Discovery Server), or **replace the discovery/transport model** (Zenoh). A partial mitigation at the network layer is **IGMP snooping** on the AP — the router unwraps multicast into managed unicast-like delivery. Enabling it on an Asus GT-AX6000 eliminated most drops in the case above, though occasional sub-second dropouts remained. *[`11-ros2-wifi-igmp-discourse.md`]* It treats the symptom, not the protocol — prefer a discovery fix. *(synthesis)*

---

## Fix A — Fast DDS Discovery Server (unicast discovery)

Replaces distributed multicast SDP with a **client–server** model: a central server brokers discovery; nodes are clients that exchange discovery data over **unicast**, receiving only what they need. No multicast required — the property that matters for WiFi. Available since ROS 2 Eloquent; v2 (Fast DDS ≥2.0.2) adds topic-based filtering so nodes sharing no topic never discover each other. *[`03-fastdds-discovery-server.md`]*

Setup:

- Launch a server: `fastdds discovery --server-id 0` (default port **11811**, all interfaces). *[`03-fastdds-discovery-server.md`]*
- Point each node at it: `export ROS_DISCOVERY_SERVER=127.0.0.1:11811`. Multiple servers use a **semicolon-positional** list keyed by server-id (`;` per skipped id) — e.g. server-id 1 → `";<ip>:<port>"`. *[`03-fastdds-discovery-server.md`]*
- CLI introspection (`ros2 topic list`, etc.) needs **SUPER_CLIENT** mode (a client that receives *all* discovery info, not just its matches) via `ROS_SUPER_CLIENT=TRUE` or a `FASTRTPS_DEFAULT_PROFILES_FILE` XML profile + `--no-daemon`. *[`03-fastdds-discovery-server.md`, `04-vulcanexus-wifi.md`]*

The **Vulcanexus WiFi tutorial** is the canonical recipe and adds **Large Data mode** for high-bandwidth payloads (video, point clouds): UDP multicast for PDP discovery but TCP/SHM for large samples, via `export FASTDDS_BUILTIN_TRANSPORTS=LARGE_DATA`. When Large Data is set, the Discovery Server must use **TCP** transport. *[`04-vulcanexus-wifi.md`]* Recommended config (per-client JSON via `FASTDDS_ENVIRONMENT_FILE`):

```json
{
  "ROS_DISCOVERY_SERVER": "TCPv4:[<wifi_ip>]:42100",
  "ROS_SUPER_CLIENT": "TRUE",
  "FASTDDS_BUILTIN_TRANSPORTS": "LARGE_DATA"
}
```

Server launch in that tutorial: `fastdds discovery -t <wifi_ip> -q 42100`. *[`04-vulcanexus-wifi.md`]* Note: >100 participants per host can exhaust unicast port allocation (`mutation_tries` default 100) and >119 collide with the next domain's ports — raise `mutation_tries` via XML if scaling. *[`03-fastdds-discovery-server.md`]* For a single indoor drone this never bites. *(synthesis)*

---

## Fix B — Zenoh RMW / zenoh-plugin-ros2dds

Zenoh attacks the model itself, and its discovery design suits lossy/wireless links: it (1) advertises only **resource interests**, not individual publishers/subscribers; (2) **generalizes** resources (e.g. collapse `/mybot/sensor/*` to `/mybot/**`) to compress discovery; (3) uses wire-efficient discovery messages; (4) runs reliability **between runtimes**, not per reader/writer pair. Measured against DDS on a Turtlebot SLAM + RViz2 over WiFi: **97.4%** discovery-traffic reduction baseline, **99.3%** with resource generalization, up to **99.97%** with generalization + warm start. *[`06-zenoh-discovery-blog.md`]* This is why Zenoh users report large gains over WiFi.

Two ways to adopt Zenoh, targeting different points:

- **`rmw_zenoh_cpp` (native RMW)** — swap the whole RMW. `sudo apt install ros-<distro>-rmw-zenoh-cpp`, then `export RMW_IMPLEMENTATION=rmw_zenoh_cpp`. **Multicast discovery is disabled by default** in the node session config; nodes discover via a **Zenoh router's gossip** instead — so you must run the router: `ros2 run rmw_zenoh_cpp rmw_zenohd`. From Jazzy on, key expressions embed the **RIHS01 message-type hash** (REP-2016), breaking interop with Humble and earlier. *[`01-ros2-zenoh.md`]*
- **`zenoh-plugin-ros2dds` / `zenoh-bridge-ros2dds` (bridge)** — keep DDS on-robot, bridge the ROS 2 graph over Zenoh between hosts. Typical deploy: one bridge on the drone, one on the operator host; connect with `zenoh-bridge-ros2dds -e tcp/<robot-ip>:7447` (default listen port **7447**; v0.11.0+ defaults to *router* mode, no autoconnect — connect statically via `-e`). Relays full ROS graph (topics/services/actions visible via `ros2 topic/service/action list`), supports per-bridge namespacing, and is more compact than raw DDS discovery between bridges. Bridge relies on **CycloneDDS** (`RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`); you **must prevent direct DDS between bridged hosts** (use `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`, distinct `ROS_DOMAIN_ID`, or a `CYCLONEDDS_URI` restricting interfaces) or you get duplicate/looping traffic. Config via JSON5 (`-c`). *[`05-zenoh-plugin-ros2dds.md`]* The older generic `zenoh-plugin-dds` was the drop-in measured in the discovery blog; the ros2dds variant adds ROS-graph awareness and tooling support. *[`05-zenoh-plugin-ros2dds.md`, `06-zenoh-discovery-blog.md`]*

---

## MAVLink ↔ ROS 2 bridge on the FC side

Above is the *DDS/RMW* layer (Orin ↔ ROS 2 nodes). The FC speaks **MAVLink**; bridging uORB ↔ ROS 2 happens at the autopilot.

### PX4 — uXRCE-DDS (default) and Zenoh (experimental)

- **uXRCE-DDS** (PX4 v1.14+, replaces the old Fast-RTPS bridge): a **client on PX4** ↔ **Micro XRCE-DDS Agent on the companion**, over serial or **UDP**, exposing uORB as ROS 2 topics (`/fmu/out/*` pubs, `/fmu/in/*` subs). Agent: `MicroXRCEAgent udp4 -p 8888` (PX4 client is XRCE v2.x — **incompatible with agent v3.x**; match versions, e.g. Jazzy↔v2.4.3). Client config via params: `UXRCE_DDS_CFG` (port: TELEM2/Ethernet/Wifi), `UXRCE_DDS_PRT` (default 8888), `UXRCE_DDS_AG_IP` (agent IP, int32-encoded), `UXRCE_DDS_DOM_ID`. Topic set is fixed at build time by `dds_topics.yaml`; ROS 2 side must use the matching `px4_msgs`. **QoS caveat:** PX4 publishers are BEST_EFFORT — ROS 2 subscribers must override the RELIABLE default or they won't match. *[`07-px4-uxrce-dds.md`]*
- **PX4 Zenoh-Pico** (v1.17, experimental): a Zenoh-Pico **client on the FMU** ↔ **`zenohd` router on the companion** over UART/TCP/UDP, an alternative to uXRCE-DDS that connects straight into `rmw_zenoh`. Set `RMW_IMPLEMENTATION=rmw_zenoh_cpp`, run `ros2 run rmw_zenoh_cpp rmw_zenohd`, enable `ZENOH_ENABLE=1`; default daemon IP `10.41.10.1`, set via `zenoh config net client tcp/<ip>:7447#iface=eth0`. Requires `CONFIG_MODULES_ZENOH=y` in firmware (flash-constrained — may need to drop the uxrce_dds_client module). Per-publisher CC/reliability/priority tunables (`ZENOH_PUB_*`). The PX4 ROS 2 Interface Library works over Zenoh unchanged. *[`02-px4-zenoh.md`]* Note: Zenoh bridge does **not** support `subscriptions_multi` demux routing — those topics are ignored. *[`07-px4-uxrce-dds.md`]*

### ArduPilot — native ROS 2 via AP_DDS

ArduPilot supports ROS 2 natively through **AP_DDS**, using a Micro-XRCE-DDS path (micro-ROS-Agent + Micro-XRCE-DDS-Gen). ROS 2 **Humble only** currently. Workspace built via `vcs import` from ArduPilot's `ros2.repos` + colcon. *[`08-ardupilot-ros2.md`]*

---

## MAVLink transport: routing UDP to multiple endpoints

Separate from DDS: a single FC serial link must feed **multiple consumers** (GCS, companion programs, loggers). Two tools.

- **mavlink-router** — reads MAVLink from a UART and fans it out to N UDP/TCP endpoints. Config (`/etc/mavlink-router/main.conf`): a `[UartEndpoint]` (e.g. `/dev/serial0`, baud matched to `SER_TEL1_BAUD`) plus `[UdpEndpoint]`s; TCP server defaults to **5760**, GCS UDP convention **14550**. Run/forward: `mavlink-routerd -e <gcs_ip>:14550`; multiple `-e` route to several destinations at once (e.g. `-e <gcs_ip>:14550 -e 127.0.0.1:14550` feeds both a remote GCS and a local consumer). Productionize as a systemd unit. **Don't point both mavlink-router and another tool at the same `/dev/tty*`** — route to localhost and have the second tool read UDP instead. *[`09-mavlink-router-bellergy.md`]*
- **MAVProxy forwarding** — `--out <ip>:14550`, repeatable for many GCS; e.g. `mavproxy.py --master=/dev/ttyACM0 --out 127.0.0.1:14550 --out <remote>:14550`. TCP is **not recommended** for forwarding (lag, bad for joystick control). MAVProxy auto-connects to a local autopilot, so `mavproxy.py --out 127.0.0.1:14550` suffices on the companion. MAVProxy itself can be the router (`--out=udp:<ip>:14550`) so you don't need both — but don't run both against the same serial device. *[`10-mavproxy-forwarding.md`, `09-mavlink-router-bellergy.md`]*

---

## Build notes (home-tidy drone)

*(synthesis / recommendation — for the indoor Orin + ROS 2 + MAVLink FC build)*

- **Single-drone indoor, one AP, no Internet hop:** the failure mode is discovery multicast, not bandwidth. The lowest-friction reliable path is **Fast DDS Discovery Server** on the Orin (`ROS_DISCOVERY_SERVER` on all nodes + GCS laptop). Add `FASTDDS_BUILTIN_TRANSPORTS=LARGE_DATA` (TCP server) only if streaming camera/point-cloud frames off-board. *(synthesis)*
- **If discovery/latency stays flaky or you add a second host:** move to **Zenoh** — `rmw_zenoh_cpp` if you control all ROS 2 nodes, or a **`zenoh-bridge-ros2dds`** pair (drone + laptop) to bridge only across WiFi while keeping DDS local. Zenoh's interest-based model is the better fit for lossy WiFi and its discovery savings are large. *(synthesis)*
- **Layer separation matters:** the DDS fix (Discovery Server / Zenoh) governs the ROS 2 graph on the Orin and across WiFi; it does **not** touch the FC link. The FC↔Orin bridge is uXRCE-DDS (PX4 default) or AP_DDS (ArduPilot); MAVLink fan-out to GCS is mavlink-router. Don't conflate them — a multicast fix won't help a MAVLink routing problem and vice versa. *(synthesis)*
- **Version traps to pre-check:** XRCE client v2.x ↔ agent version (not v3.x); Zenoh RIHS01 hash → Jazzy-only key compat; ArduPilot ROS 2 = Humble only; avoid simultaneous global+local Fast DDS installs (nondeterministic, segfaults). *[`07-px4-uxrce-dds.md`, `01-ros2-zenoh.md`, `08-ardupilot-ros2.md`]*
- **IGMP snooping** on the AP is a useful belt-and-suspenders even with a discovery fix in place, but is not a substitute. *[`11-ros2-wifi-igmp-discourse.md`]*

---

## Source

- `01-ros2-zenoh.md` — ROS 2 Jazzy docs: installing/using `rmw_zenoh_cpp`, multicast-discovery-disabled-by-default, router gossip, RIHS01 hash — https://docs.ros.org/en/jazzy/Installation/RMW-Implementations/Non-DDS-Implementations/Working-with-Zenoh.html
- `02-px4-zenoh.md` — PX4 docs: Zenoh-Pico client + `zenohd` router middleware (experimental, v1.17), `RMW_IMPLEMENTATION`/`ZENOH_ENABLE`/network config — https://docs.px4.io/main/en/middleware/zenoh
- `03-fastdds-discovery-server.md` — ROS 2 Jazzy tutorial: Fast DDS Discovery Server (unicast, no-multicast), `ROS_DISCOVERY_SERVER`, SUPER_CLIENT, mutation_tries — https://docs.ros.org/en/jazzy/Tutorials/Advanced/Discovery-Server/Discovery-Server.html
- `04-vulcanexus-wifi.md` — Vulcanexus WiFi tutorial: solving ROS 2 over WiFi with Discovery Server + Large Data mode, JSON env-file config — https://docs.vulcanexus.org/en/jazzy/rst/tutorials/core/wifi/wifi_issues_tutorial/wifi_issues_tutorial.html
- `05-zenoh-plugin-ros2dds.md` — eclipse-zenoh/zenoh-plugin-ros2dds README: bridge vs plugin, CycloneDDS dependency, port 7447, namespacing, anti-loop config — https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds
- `06-zenoh-discovery-blog.md` — Zenoh blog "Minimizing Discovery Overhead in ROS2": DDS SPDP/SEDP quadratic scaling, Zenoh interest/generalization model, 97–99.97% WiFi discovery reduction — https://zenoh.io/blog/2021-03-23-discovery/
- `07-px4-uxrce-dds.md` — PX4 docs: uXRCE-DDS bridge (client↔agent), `UXRCE_DDS_*` params, ports 8888, QoS mismatch, dds_topics.yaml, version compat — https://docs.px4.io/main/en/middleware/uxrce_dds
- `08-ardupilot-ros2.md` — ArduPilot dev docs: native ROS 2 via AP_DDS / micro-ROS-Agent, Humble-only, workspace install — https://ardupilot.org/dev/docs/ros2.html
- `09-mavlink-router-bellergy.md` — Bellergy guide: install/configure mavlink-router, UART→UDP fan-out, `-e` multi-endpoint, systemd, mavproxy coexistence — https://bellergy.com/6-install-and-setup-mavlink-router/
- `10-mavproxy-forwarding.md` — ArduPilot MAVProxy docs: telemetry forwarding via repeatable `--out <ip>:14550`, TCP-not-recommended — https://ardupilot.org/mavproxy/docs/getting_started/forwarding.html
- `11-ros2-wifi-igmp-discourse.md` — ROS Discourse thread: multicast-over-WiFi discovery drops in multi-drone PX4/MAVROS, IGMP snooping as mitigation — https://discourse.openrobotics.org/t/ros2-wifi-multicast-multi-robot-and-igmp-snooping/28516

## Related

- [[home-tidy-drone-prototype]]
- [[slam-fc-integration]]
- [[fast-lio-mid360-orin]]
- [[drone-autonomy-state]]
- [[voice-intent-task]]
- [[precision-docking-recharging]]
