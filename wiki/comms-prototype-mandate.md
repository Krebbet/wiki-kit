# Communications Prototype Mandate

Mandate for the `drone-app` prototype — the first end-to-end implementation of the communication layer connecting all five system entities over home WiFi.

## Related

[[user-comms-layer]] · [[system-architecture]] · [[voice-intent-task]] · [[ros2-server-bridge]]

---

## What we are building

A working prototype of the full communication layer between:
- **Drone** (stub robot process mimicking Land Rover v1 telemetry)
- **World Brain** (FastAPI server: world model, command routing, robot bridge)
- **App Layer** (STT pipeline, intent parser, webhook adapters)
- **User / Phone** (browser web-app: push-to-talk, status display)
- **Google Home** (voice command via local webhook)

No cloud infrastructure. Everything runs on the home WiFi LAN. Stub robot until hardware integration in Phase 3.

## Why now

Before writing any robot behaviour code, we need to know:
1. Whether WiFi is a viable transport for all the data flows we need (latency, bandwidth, reliability)
2. What the latency budget actually is for voice → robot action
3. Whether Google Home → local webhook is a usable path
4. What data structures need to live where

Getting this wrong architecturally is expensive to fix later. This prototype answers those questions with measured data, not assumptions.

---

## Success criteria (by priority)

### P1 — Must prove before anything else

| # | Criterion | How measured |
|---|---|---|
| P1.1 | Voice command (phone PTT) → robot acknowledges in < 3 s end-to-end on LAN | Stopwatch + server logs |
| P1.2 | Stub robot pose updates received at World Brain at ≥ 5 Hz with < 50 ms jitter | Benchmark script |
| P1.3 | POST /robot/stop reaches stub robot in < 200 ms from app (bypasses LLM) | Benchmark script |
| P1.4 | World Brain REST API responds to status queries in < 100 ms | Benchmark script |
| P1.5 | WebSocket status push reaches phone at 1 Hz with < 100 ms lag | Browser devtools |

### P2 — Must characterise before architecture lock-in

| # | Criterion | How measured |
|---|---|---|
| P2.1 | Measured WiFi round-trip latency for command messages (< 1 KB) | `benchmarks/latency.py` |
| P2.2 | Measured throughput for compressed camera feed (MJPEG, 640×480, 10 fps) | `benchmarks/throughput.py` |
| P2.3 | Connection reliability under 30-min continuous run (drop rate, reconnect time) | `benchmarks/reliability.py` |
| P2.4 | Latency budget broken down by stage: upload, STT, LLM intent, routing | Server-side timing logs |

### P3 — Voice entry points working

| # | Criterion | How measured |
|---|---|---|
| P3.1 | Phone PTT → Whisper → Claude → command → response display works end-to-end | Manual test |
| P3.2 | Google Home Routine → local webhook → same intent pipeline works | Manual test |
| P3.3 | Both entry points produce identical structured intent for the same spoken command | Log comparison |

### P4 — Data hierarchy validated

| # | Criterion | How measured |
|---|---|---|
| P4.1 | All data structures defined as Pydantic schemas in `shared/schemas.py` | Code review |
| P4.2 | Stub world model (5 rooms, 10 objects) correctly served via REST API | API test |
| P4.3 | Robot state (pose, battery, task) correctly propagated from stub → World Brain → phone | Manual test |

---

## Priority order for implementation

1. **Shared schemas** — define all data models first; everything else depends on them
2. **World Brain server** — FastAPI app with stub world model + REST API endpoints
3. **Stub robot** — fake telemetry publisher; accepts goals; reports completion
4. **World Brain ↔ Stub Robot** — WebSocket bridge (rosbridge-style protocol)
5. **Phone web-app** — PTT button, status display, command send
6. **Voice pipeline** — Whisper STT + Claude Haiku intent parser
7. **WiFi benchmarks** — latency, throughput, reliability measurement scripts
8. **Google Home webhook** — HTTPS POST endpoint + ngrok for dev
9. **WebSocket status push** — live robot state → phone browser

Do not start #5 before #4 is working. Do not start #6 before #5 is working. Benchmarks (#7) can run in parallel with #5–6 using the stub robot.

---

## Out of scope for this prototype

- Cloud infrastructure (stubbed with local canned responses)
- Real robot hardware integration (Land Rover v1 → Phase 3 of build order in [[user-comms-layer]])
- Real RTAB-Map world model (stub world model only)
- App store / native mobile app (browser web-app only)
- Multi-user (single user assumed throughout)
- Google Actions SDK / OAuth (local webhook only)
- Production HTTPS (ngrok or self-signed cert acceptable)

---

## Key constraints to measure (WiFi)

These measurements will drive architecture decisions about what must be on-robot vs. what can live in World Brain:

| Measurement | Why it matters |
|---|---|
| Round-trip latency for 1 KB command | Sets floor for command → acknowledge time |
| Round-trip latency for 10 KB status payload | Determines if full world state can be pushed per-cycle |
| Throughput for 640×480 MJPEG at 10 fps | Whether camera preview is viable over WiFi |
| Latency variance (jitter) over 10-min run | Determines if pose updates need onboard buffering |
| Reconnect time after dropout | How long robot must hold position if WiFi lost |
| Max concurrent WebSocket connections | Whether multiple phones can be supported |

---

## Repo: drone-app

See `/home/david/drone/drone-app/` for the scaffolded prototype.

Structure:
```
drone-app/
├── README.md
├── shared/schemas.py       # Pydantic data models — source of truth
├── server/                 # World Brain (FastAPI)
├── robot/                  # Stub robot process
├── voice/                  # STT + intent pipeline
├── app/                    # Web UI + Google Home webhook
└── benchmarks/             # WiFi constraint measurement
```

Quick start: `docker-compose up` — runs World Brain + stub robot + app layer locally.

---

## Open architecture decisions this prototype resolves

1. **Is WiFi reliable enough for 10 Hz pose updates?** → Answered by P2.2 benchmark
2. **Is Whisper small fast enough on LAN for <3s total latency?** → Answered by P1.1 + P2.4
3. **Does Google Home webhook add unacceptable latency?** → Answered by P3.2 test
4. **What minimum data does the robot need onboard to survive WiFi dropout?** → Answered by P2.3 + reliability test
5. **Is the REST API sufficient or do we need MQTT pub/sub from day one?** → Answered by P2.1 jitter measurement
