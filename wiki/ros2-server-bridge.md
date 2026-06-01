# ROS 2 ↔ Server Bridge

How to get ROS 2 topics off the robot and into a Python (or other language) server process without running ROS 2 on the server. Three options with different tradeoffs between simplicity, performance, and server-side requirements.

## Source
- raw/research/ros2-server-bridge/01-mqtt-client-readme.md — mqtt_client ROS 2 package (ika-rwth-aachen)
- raw/research/ros2-server-bridge/02-rosbridge-protocol-spec.md — rosbridge v2.1 protocol specification
- raw/research/ros2-server-bridge/03-zenoh-ros2-integration.md — Zenoh ROS 2 integration (zenoh.io, 2021)
- raw/research/ros2-server-bridge/04-zenoh-mqtt-dds-benchmark.md — Protocol benchmark study (arXiv 2303.09419)

## Related
[[drone-comms-wifi]], [[ros2-nav2]], [[system-architecture]], [[home-tidy-drone-prototype]]

---

## Option comparison

*(synthesis)* table:

| | **rosbridge** | **mqtt_client** | **Zenoh** |
|---|---|---|---|
| Server-side library | `websockets` (Python) | `paho-mqtt` | `eclipse-zenoh` + `pycdr` |
| Server message format | JSON dict (field names match ROS msg) | CDR binary or plain string | CDR binary |
| CDR decoder needed? | No (normal mode) | No (primitive mode) / Yes (full msg) | Yes |
| Broker/router required | No | Yes (Mosquitto) | Optional (peer-to-peer mode exists) |
| ROS install on server | No | No | No |
| Throttle rate control | Yes (per subscription) | No | No |
| Multi-robot routing | Manual topic namespacing | Per-topic config | Native (key prefix + wildcard) |
| NAT traversal / internet | No | Via cloud broker | Yes (zenohd router in cloud) |
| Setup complexity | Low | Low | Moderate |
| Best fit | Development, dashboards, slow topics | Production telemetry, lightweight commands | Multi-robot, internet-scale |

---

## Option 1 — rosbridge (WebSocket + JSON)

**What it is:** A ROS 2 node that accepts WebSocket connections and translates rosbridge JSON messages to/from ROS topics, services, and actions. [src: rosbridge-protocol-spec]

**Robot side:** install `ros-$ROS_DISTRO-rosbridge-suite`; launch `rosbridge_websocket.launch.py`. [src: rosbridge-protocol-spec]

**Server side:** Python WebSocket client receives messages as JSON dicts. No decoder needed — a `sensor_msgs/Imu` arrives as `{"header": {...}, "linear_acceleration": {"x": 0.1, "y": ...}}`. [src: rosbridge-protocol-spec]

**Subscribe example (Python):**
```python
import websocket, json
ws = websocket.create_connection("ws://robot-ip:9090")
ws.send(json.dumps({"op": "subscribe", "topic": "/robot/pose", "type": "geometry_msgs/PoseStamped"}))
msg = json.loads(ws.recv())  # plain dict, no CDR
```

**Throttle rate:** set `throttle_rate` (ms) per subscription to rate-limit high-frequency topics [src: rosbridge-protocol-spec]

**Binary encoding:** CBOR-RAW mode sends raw CDR bytes for performance-sensitive topics (images, point clouds) [src: rosbridge-protocol-spec]

**Limitations [src: rosbridge-protocol-spec]:**
- JSON verbose for binary-heavy topics (images, point clouds) — use CBOR-RAW for those
- First-subscriber-wins on QoS when multiple clients subscribe to same topic
- Long-lived WebSocket; client must handle reconnect on network interruption
- No built-in auth in protocol (TLS at transport layer)

---

## Option 2 — mqtt_client (ROS 2 ↔ MQTT)

**What it is:** A ROS 2 component node that bridges configured ROS topics to/from an MQTT broker. [src: mqtt-client-ros2]

**Robot side:** `sudo apt install ros-$ROS_DISTRO-mqtt_client`; configure a YAML params file; connect to a Mosquitto broker (can run on home server). [src: mqtt-client-ros2]

**Server side:** `pip install paho-mqtt`; subscribe to the MQTT topic. [src: mqtt-client-ros2]

**Two payload modes [src: mqtt-client-ros2]:**
- **Primitive mode:** plain ASCII string — works for simple scalar telemetry without any decoder
- **CDR mode:** full ROS message serialized as CDR binary — requires `pycdr` on server for arbitrary message types

**Config example (YAML):**
```yaml
mqtt_client:
  ros__parameters:
    broker:
      host: home-server.local
      port: 1883
    bridge:
      ros2mqtt:
        - ros_topic: /robot/pose
          mqtt_topic: drone/pose
          primitive: false   # CDR mode
        - ros_topic: /robot/battery
          mqtt_topic: drone/battery
          primitive: true    # plain string
      mqtt2ros:
        - mqtt_topic: drone/goal
          ros_topic: /robot/goal
```

**Disconnect buffering:** available when `client_id` is set [src: mqtt-client-ros2]

**Limitations [src: mqtt-client-ros2]:**
- CDR mode requires pycdr on server for complex message types
- Requires a running MQTT broker (single point of failure unless clustered)
- No per-topic throttle rate control at bridge level

---

## Option 3 — Zenoh (zenoh-bridge-dds)

**What it is:** Mirrors the robot's DDS graph onto a zenoh key-space; no ROS 2 message definitions needed. Forwards raw CDR payloads under keys matching `/rt/<topic_name>`. [src: zenoh-ros2-integration]

**Robot side:** run `zenoh-bridge-dds` alongside the ROS 2 stack. [src: zenoh-ros2-integration]

**Server side:** `pip install eclipse-zenoh pycdr`; subscribe to key `/rt/<topic>`. [src: zenoh-ros2-integration]

**Three deployment topologies [src: zenoh-ros2-integration]:**
1. **Direct TCP:** server connects directly to bridge's TCP listener (port 7447) — simplest, no router
2. **Cloud router:** both bridge and server connect as clients to a `zenohd` instance (e.g. on a VPS) — enables NAT traversal, remote access
3. **Distributed routers:** multiple interconnected zenohd instances for high-availability

**Multi-robot:** run separate bridges with key prefix flags (`-s /bot-1`, `-s /bot-2`); server subscribes to `/**/pose` wildcard [src: zenoh-ros2-integration]

**Limitations [src: zenoh-ros2-integration]:**
- CDR decoding mandatory — no primitive/plain-text mode
- Blog is from 2021; current zenoh Python API differs — check eclipse-zenoh/zenoh-python for current usage
- Tighter DDS/CycloneDDS coupling than rosbridge's protocol abstraction

---

## Latency reference numbers

From arXiv 2303.09419 *(conflict of interest: authored by ZettaScale, Zenoh's developer; Zenoh v0.7.0-rc tested on 100 GbE — not representative of home WiFi)* [src: zenoh-mqtt-dds-benchmark]:

| Protocol | Multi-machine latency (64B payload) |
|---|---|
| Zenoh peer-to-peer | 16 µs |
| Zenoh brokered (zenohd) | 41 µs |
| CycloneDDS (UDP multicast) | 38 µs |
| MQTT (Mosquitto) | 45 µs |
| Kafka | 84 µs |

*(synthesis)* At home WiFi/LAN scale (1 Gbps or 300 Mbps WiFi), round-trip latency is dominated by the network (1–10 ms), not the protocol overhead. All three options are effectively equivalent in practice for a home robot → server bridge. Protocol selection should be driven by server-side integration simplicity and operational requirements, not latency.

---

## Recommendation for this project

*(synthesis)*

**Phase 1 development:** rosbridge. Zero server-side friction — JSON dicts, standard WebSocket library, no CDR. Use `throttle_rate` to tame high-frequency topics like `/odom`. Run `ros2 launch rosbridge_server rosbridge_websocket_launch.xml`.

**Phase 1 production telemetry:** mqtt_client with primitive mode for scalars (battery, pose as string), CDR mode for structured types if needed. Mosquitto runs on the home server as a single Docker container.

**Future multi-robot or internet access:** Zenoh with cloud zenohd router. Deferred — adds complexity and CDR requirement.

For the [[system-architecture]] workstream C interface: define message schemas as Python dataclasses or protobuf messages in `drone-core/shared/`. The rosbridge/MQTT bridge translates ROS messages to these schemas on receipt. The server world brain consumes only the Python objects, not raw ROS messages.

See [[drone-comms-wifi]] for DDS-over-WiFi failure modes that are upstream of this bridge layer (must solve DDS discovery before the bridge is useful).
