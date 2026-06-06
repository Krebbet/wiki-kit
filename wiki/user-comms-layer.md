# User Communication Layer

How the five system entities communicate with each other and with the user. The core transport is the home WiFi LAN; internet connects to cloud services. For prototype scope, cloud is stubbed locally.

## Related

[[system-architecture]] · [[voice-intent-task]] · [[ros2-server-bridge]] · [[drone-comms-wifi]] · [[comms-prototype-mandate]]

---

## Five entities

```
┌──────────────┐     WiFi LAN     ┌──────────────────────────────┐
│    DRONE     │◄────────────────►│      WORLD BRAIN             │
│  (robot)     │  rosbridge/MQTT  │   (laptop / workstation)     │
└──────────────┘                  │   SLAM · maps · object lib   │
                                  │   REST API · WebSocket push  │
                                  └──────────┬───────────────────┘
                                             │ HTTP REST
                                             │ WebSocket (status)
                                  ┌──────────▼───────────────────┐
                                  │       APP LAYER              │
                                  │  STT · intent · router · TTS │
                                  │  web UI · webhook adapters   │
                                  └──────┬────────────┬──────────┘
                                         │            │
                          ┌──────────────▼──┐  ┌─────▼──────────┐
                          │   USER / PHONE  │  │  GOOGLE HOME   │
                          │  push-to-talk   │  │  voice command │
                          │  status display │  │  webhook POST  │
                          └─────────────────┘  └────────────────┘

                                   ┌────────────────┐
                                   │    CLOUD       │
                                   │  (stub in V1)  │
                                   │  model updates │
                                   │  remote access │
                                   └────────────────┘
```

---

## Entity roles and data ownership

| Entity | Runs on | Owns | Communicates via |
|---|---|---|---|
| **Drone** | Robot onboard (Pi/laptop tether) | Sensor streams, current pose, task queue | rosbridge WebSocket → World Brain |
| **World Brain** | Home laptop / workstation | Maps, object library, user preferences, room labels, task history | REST API (app ↔ brain), rosbridge (brain ↔ robot) |
| **App Layer** | Same machine as World Brain (prototype) | STT pipeline, intent parser, Google Home webhook, web UI server | HTTP REST + WebSocket to World Brain; WebSocket to phone browser |
| **User / Phone** | Phone browser | — | WebSocket (status) + HTTP (commands + audio upload) |
| **Google Home** | Google cloud | — | HTTPS POST webhook → App Layer |
| **Cloud** | Remote (stub in prototype) | Model weights, backup maps, remote access | HTTPS (app → cloud) |

---

## Data hierarchy — what lives where

| Data | Owner | Storage | Update frequency |
|---|---|---|---|
| Occupancy grid (2D floor plan) | World Brain | Local disk (`.pgm`) | Per mapping session |
| SLAM pose graph | World Brain | Local disk (RTAB-Map `.db`) | Real-time during nav |
| Object library (labels, 3D bbox, DINOv2 embeddings) | World Brain | Local DB (SQLite / JSON) | Per semantic sweep |
| Room labels and layout | World Brain | Local config | User-set, persists across sessions |
| User preferences ("socks go in bedroom") | World Brain | Local config | User-set |
| Current robot pose | Drone → World Brain | In-memory (World Brain) | ~10 Hz continuous |
| Robot status (battery, task, mode) | Drone → World Brain | In-memory | ~1 Hz + events |
| Active task queue | Drone | On-robot memory | Per task dispatch |
| Voice audio | Phone → App | Transient (not stored) | On command |
| Parsed intent | App | Transient | On command |
| Task history / completion log | World Brain | Local DB | Per task |
| Cloud model weights | Cloud → World Brain | Local cache | Rare (async) |
| Remote map backup | World Brain → Cloud | Cloud storage | Per session (opt-in) |

**On-robot minimum:** current map tile for local obstacle avoidance + active task queue. Everything else lives in World Brain. Drone must be safe at WiFi dropout — it holds its last task state and pauses/RTL rather than continuing blind.

---

## Communication channels

### Drone ↔ World Brain (rosbridge WebSocket)

Primary bridge for prototype. rosbridge runs on robot; World Brain connects as a WebSocket client. JSON messages — no CDR decoder needed for prototype.

Topics the World Brain subscribes to from robot:
- `/robot/pose` → PoseStamped (10 Hz, throttled)
- `/robot/battery` → BatteryState (1 Hz)
- `/robot/status` → String (task, mode, error)
- `/robot/camera/compressed` → CompressedImage (throttled, app preview only)

Topics World Brain publishes to robot:
- `/robot/goal` → PoseStamped (navigate to room centroid)
- `/robot/cmd` → String (stop, cancel, dock)

See [[ros2-server-bridge]] for rosbridge vs MQTT vs Zenoh tradeoff — prototype uses rosbridge; production path uses MQTT (Mosquitto on home server).

### World Brain ↔ App Layer (HTTP REST + WebSocket)

The explicit contract boundary. App Layer is in a separate process (or repo) and must not know ROS internals.

| Endpoint | Method | Purpose |
|---|---|---|
| `/command` | POST | Structured intent → robot action |
| `/robot/stop` | POST | Emergency stop (bypasses all queuing) |
| `/world/state` | GET | Full world state (rooms, objects, poses) |
| `/world/rooms` | GET | Room list with labels |
| `/world/objects` | GET | Object library snapshot |
| `/world/objects/{name}` | GET | Single object by label |
| `/robot/status` | GET | Current robot pose + task + battery |
| `/ws/status` | WebSocket | Push: robot status at 1 Hz + events |

Command schema (POST /command):
```json
{
  "intent": "navigate" | "find_object" | "query_state" | "cancel" | "report" | "tidy_room",
  "target": { "type": "room" | "object" | "location", "name": "kitchen" },
  "params": {},
  "source": "phone" | "google_home" | "dashboard"
}
```

### Phone ↔ App Layer

- **Voice**: browser records audio (PTT) → base64 → `POST /voice/upload` → Whisper STT → Claude intent → `/command`
- **Status**: WebSocket `/ws/status` → live robot position, task, battery on phone screen
- **Map**: `GET /world/map` → PNG floor plan with robot position overlay

### Google Home ↔ App Layer

Simplest path: **Google Home Routine → local webhook**.

1. Create a Google Home Routine triggered by "Hey Google, [phrase]"
2. Routine action: call webhook URL `https://<local-ip>/google-home/webhook` (or ngrok tunnel during dev)
3. Webhook body: Google sends `{"query": "tidy the living room"}`
4. App Layer extracts `query`, runs same Claude intent pipeline as phone voice
5. Routes to `/command`

This requires:
- App Layer running on HTTPS (self-signed cert OK for dev; `uvicorn --ssl-*` or ngrok)
- Google Home app configured with the Routine on the user's Google account
- No Google Actions SDK, no OAuth, no cloud deployment needed

Alternative path (proper, for production): Google Home Action with local fulfillment SDK — enables "Hey Google, ask [app name] to…" but requires Actions project + OAUTH2 + cloud endpoint. Deferred to post-prototype.

### Cloud ↔ World Brain (stub in prototype)

Not built in prototype. World Brain has stub endpoints that mimic cloud behaviour returning canned responses. Production targets:
- `POST /cloud/maps/sync` — upload floor plan backup
- `GET /cloud/models/check` — check for model weight updates
- `GET /cloud/remote/status` — remote monitoring dashboard

---

## Voice pipeline

```
User speaks
    │
    ▼ (phone PTT / Google Home wake-word)
Audio capture
    │
    ▼
STT — Whisper small (local, ~0.5s)
    │  input: wav bytes
    │  output: text transcript
    ▼
Intent parser — Claude Haiku
    │  system prompt: current room list + known object names
    │  input: transcript
    │  output: structured intent JSON (validated against schema)
    ▼
Command router
    │  maps intent → POST /command to World Brain
    ▼
World Brain executes → publishes to robot via rosbridge
    │
    ▼
Response synthesizer
    │  template ("Heading to kitchen") or Haiku one-liner for queries
    ▼
TTS — browser Web Speech API
    │
    ▼
User hears response
```

Latency budget (phone → response):
- Audio upload: ~100 ms (LAN)
- Whisper small: ~500 ms
- Claude Haiku intent: ~300–600 ms
- Command routing: ~50 ms
- Robot acknowledgment: ~100 ms
- TTS: ~200 ms
- **Total: ~1.3–1.6 s** (LAN, no cloud STT)

Emergency stop (`cancel` intent) must bypass the LLM — direct `POST /robot/stop` from router as soon as intent is classified, before full pipeline completes.

---

## Prototype build order

**Phase 1 — Prove the layer (no hardware)**
1. World Brain stub server (FastAPI) with canned world state
2. Stub robot process: publishes fake pose/battery on schedule, accepts goals
3. Phone web-app: PTT → Whisper → Claude → command → response display
4. WiFi benchmark suite: latency, throughput, reliability measurements

**Phase 2 — Add voice entry points**
5. Google Home webhook endpoint on app layer (ngrok for dev)
6. Sonos TTS output via HTTP Control API (LAN only)
7. Live status WebSocket push to phone

**Phase 3 — Live robot integration**
8. Swap stub robot for real rosbridge connection to Land Rover v1
9. World Brain connects to real RTAB-Map world model
10. Map preview on phone (floor plan + robot dot)

**Phase 4 — Entry point hardening**
11. Google Home Routine tested end-to-end
12. Multi-command session (clarification round-trip)
13. Mid-task override tested (stop during navigation)

---

## Open questions

- **Google Home latency:** webhook path adds Google cloud round-trip (~200–500 ms) before reaching local server. Acceptable for task commands; not for stop.
- **Multi-user:** last-in-wins for prototype; priority queue policy deferred.
- **WiFi dropout mid-task:** robot must RTL or hold-position; World Brain must checkpoint task state.
- **Audio privacy:** Whisper runs locally; Google Home wake-word goes through Google cloud. If that's unacceptable, phone PTT is the fallback.
- **ngrok vs router port-forward:** ngrok is simplest for dev but requires account and internet. Router port-forward + DDNS is the production path for local-only operation.
