# User Communication Layer

How users interact with the home robot system. Sits entirely outside `drone-core` — a separate prototype repo (`drone-app`) that calls the server-side world brain via a well-defined API. See [[system-architecture]] § User Interface and [[voice-intent-task]] for the NLU research landscape.

---

## Pipeline architecture

```
Entry Point
    ↓
Voice Capture / STT
    ↓
Intent Parser  ←── world registry (rooms, known objects)
    ↓
Command Router
    ↓
drone-core API (robot nav goals / world queries)
    ↓
Response Synthesizer
    ↓
Entry Point (TTS / screen)
```

---

## Layer 1 — Entry points

Where voice commands originate. Each has a different integration cost.

| Entry point | Mic access | Integration | Notes |
|---|---|---|---|
| **Phone app** (iOS/Android) | Direct, push-to-talk or wake-word | Low | Can also show map + status; prototype target |
| **Smart speaker** (Alexa / Google Home) | Wake-word | High — custom Skill/Action, cloud routing | Adds ~300–800 ms cloud latency; privacy cost |
| **Sonos speaker** | None (output only) | Medium — Sonos HTTP Control API (LAN) | Good for TTS playback; no microphone in most models |
| **Web dashboard** | Browser mic or text | Low | Manual override, monitoring, no STT needed |

**Prototype target:** phone web-app (push-to-talk, no cloud dependency, no app-store friction for early iteration).

---

## Layer 2 — Voice capture / STT

| Option | Latency | Privacy | Notes |
|---|---|---|---|
| **Whisper small (local)** | ~0.5 s | Full | Runs on laptop/server; prototype target |
| Whisper medium (local) | ~2 s | Full | Better accuracy, acceptable for non-realtime queries |
| Deepgram (cloud) | ~200 ms | Cloud | Lower latency; requires internet |
| Google STT (cloud) | ~300 ms | Cloud | Battle-tested; quota costs |
| Porcupine (wake word only) | <100 ms | Full | Offline wake-word detection; pairs with any STT |

**Prototype target:** Whisper small on the home server. Wake word optional for V1; PTT avoids it.

---

## Layer 3 — Intent parser

Maps free-form text to a structured command. Three approaches:

- **LLM-based** (Claude Haiku): flexible, handles novel phrasings; grounded via system prompt containing current room list and known objects from world registry. Best for prototype — adapts without retraining as the world model grows.
- **Rule-based NLU** (Rasa, Snips): deterministic, ~10ms latency, poor generalization. Only viable once the command set is frozen.
- **Hybrid**: LLM for intent + rule-based slot filling for known entities. Production path.

**Output schema:**
```json
{
  "intent": "navigate" | "find_object" | "query_state" | "cancel" | "report",
  "target": { "type": "room" | "object" | "location", "name": "kitchen" },
  "params": {}
}
```

**Prototype target:** Claude Haiku with system-prompt grounding from world registry. Schema validated at parse time; malformed output → ask for clarification, never guess.

---

## Layer 4 — Command router

Maps parsed intent to a `drone-core` API call. This layer is the explicit contract between `drone-app` and `drone-core`; the interface is defined in `drone-core/shared/`.

| Intent | API call | Notes |
|---|---|---|
| `navigate` | `POST /robot/navigate { goal: room_name }` | Server converts room name → pose; dispatches to robot |
| `find_object` | `GET /world/object/{name}` → navigate to last-seen location | Two-step: query then nav |
| `query_state` | `GET /world/state?room={name}` | Returns expected vs actual, missing/moved objects |
| `cancel` | `POST /robot/stop` | Robot halts and holds position |
| `report` | `GET /world/recent_changes` | What changed since last session |

Protocol for V1: HTTP REST. Production path: MQTT pub/sub (same topics the robot already uses).

---

## Layer 5 — Response synthesizer + TTS

Converts API responses to natural language.

- **Template-based** for navigation confirmations: "Heading to the kitchen."
- **LLM-generated** for rich state queries: "The living room has 3 items out of place: ..."
- **TTS options:** pyttsx3 (local, ~50ms, robotic), ElevenLabs (cloud, high quality), browser Web Speech API (no install).

**Prototype target:** template strings for nav; Claude Haiku one-liner for state queries; browser TTS.

---

## Prototype build order

1. **Mock drone-core** — stub REST server that returns canned responses. Decouples app development from robot hardware entirely.
2. **STT → intent parser → router** — phone mic → Whisper → Claude → HTTP POST to stub. Full pipeline working on a laptop.
3. **Live drone-core integration** — swap stub for real world API once drone-core has a running server.
4. **Entry point expansion** — add Sonos TTS output, smart speaker wake word, dashboard view.

---

## Open questions

- **Multi-user commands:** whose command wins? Single-user assumed for prototype; priority queue with last-in-wins is the simplest policy.
- **Ambiguous commands** ("tidy up" without a room): LLM should respond with a clarification question, not a guess. Clarification round-trip adds ~1–2 s; acceptable.
- **Mid-task override:** "stop" must reach the robot within one control cycle regardless of what the app layer is doing. The `POST /robot/stop` path must bypass any queuing.
- **Sonos mic integration:** most Sonos devices have no mic. Voice-from-Sonos requires an Alexa/Google device in the same room, or a phone as the mic and Sonos as the speaker only.

---

## Repo: drone-app

Directory structure:
```
drone-app/
  voice/        # STT, wake word, entry-point adapters
  intent/       # LLM/NLU parser + schema validation
  router/       # maps parsed intent to drone-core API calls
  feedback/     # response synthesis + TTS
```

Interface contract lives in `drone-core/shared/` — `drone-app` consumes it, does not define it.
