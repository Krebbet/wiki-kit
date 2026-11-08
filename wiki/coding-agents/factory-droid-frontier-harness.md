# Factory Droid 1.0 — Building a Frontier Harness (2026-10-29)

Factory Research's Droid 1.0 post argues that a model-independent coding-agent harness, tuned continuously across every frontier model, beats each vendor's native harness on cost. Its largest change is making programmatic tool calling (a sandboxed JavaScript "Script" tool) the default, so one model request can drive hundreds of tool calls while raw results stay out of context. Around that sit an agent-driven improvement loop ("Agent Factory"), strict prompt-cache discipline, a 37% smaller base prompt, loop-level stuck/repeat rules, and large startup-latency cuts.

## Programmatic tool calling (Script mode)
- The model writes JS that runs in a sandbox with no file, network, or system access of its own; the program calls tools, independent calls run concurrently, printed output is capped and full results are logged for later search. Raw files and logs stay as program variables, so context holds only what the program prints.
- Long jobs: a program waits up to 5 minutes then returns partial output, or runs in the background with a dedicated check/wait/stop tool; Droid wakes the model when background work finishes (no polling requests).
- On by default for GPT-6.1/6/5.6 Sol variants, Claude Fable 5/5.1, Opus 5/5.5, and Kimi K3.
- Numbers: cost down 15% on Opus 5.5 vs direct calls, concentrated in the 12.5% of Scripts with 6+ calls. A unit-test-fix replay went from 10 to 5 model calls (56.8 s to 41.6 s). A 312-call Linear cleanup took 2 requests and about 61K tokens vs a modeled 36 requests and about 3.1M input tokens (direct side is an estimate at 3-10 calls per request). A 550-call CI sweep showed the model under 0.1% of results.

## Agent Factory (harness improvement loop)
Bring in each new model (automation tracks 20+), evaluate all models on the same tasks plus daily benchmarks and live-session friction, have agents find repeated failure causes, propose a change with a stated hypothesis, run a controlled experiment on every affected model family, and have an engineer review and merge. Goals must hold on every family: line-numbering reads cut Opus cost 22% on one task but raised GLM cost 8% and Kimi 32%, so it shipped as opt-in. Stated rationale: tuning against one model conflates progress with that model's quirks.

## Cache, prompt budget, bounded autonomy
- Cache: 98% of input read from cache over 20.4M production requests (91.5% token-weighted); 98.6% of requests strictly append-only, policed by a monitor that diffs consecutive requests. Newly discovered tools are appended at the end rather than inserted at the top.
- Prompt: first-request tokens 20,887 to 13,055 (-37%); up-front tool definitions 11 to 2 with on-demand loading; the system prompt grew 33%. Models audit the prompt for repeated or contradictory rules.
- Loop rules (in the harness, so provider-independent): 4 min stream silence is retried; 3 silent turns stop; 3 identical tool calls nudge, 6 stop; compaction summary budget raised 8K to 16K tokens.
- Latency: first paint 1,839 to 488 ms, quit 648 to 30 ms, per-session memory about 350 MB to about 20 MB via a shared daemon.

## Benchmark claims
Terminal-Bench 4 (Oct 23-28, 3 trials/task, high reasoning): with GPT-6.1 Sol, Droid +3.5 points over Codex at 12% lower cost; with Opus 5.5, +3.0 to 7.6 points over Cursor, OpenCode, Devin, and Claude Code at up to 24% lower cost, 26% less time and 17% fewer tokens than Claude Code. Disclosed adjustments: moderation-blocked Opus 5.5 trials rerun on Opus 5; Devin ask-user stops counted as pass if Codex passed.

## Authority note
Vendor-primary and competitor-comparative. Mechanism descriptions and production telemetry are usable as stated; the head-to-head benchmark and "up to 20% more efficient than native harnesses" claims are self-run, unreplicated, and partly adjusted in Droid's favor: collect-but-confirm. Direct-call figures in the Script examples are modeled.

## Source

- Factory Research, "Droid 1.0: Building a Frontier Harness," 2026-10-29 (factory.com/news/frontier-harness) — `raw/research/weekly-2026-11-08/04-factory-frontier-harness.md`.

## Related

- [[patterns/openai-gpt-5-6-agentic-primitives]] — vendor-native programmatic tool calling; Factory implements the same idea harness-side across vendors
- [[patterns/code-as-agent-harness]] — code as runtime substrate
- [[case-studies/cursor-agent-harness]] — per-model tuning and agent-driven harness improvement; a benchmark competitor here
- [[patterns/harness-design-space]] — design-space context
- [[patterns/agentic-harness-engineering]] — harness engineering practice
- [[patterns/sol-pi-harness-efficiency]] — same static-to-dynamic, token-cutting direction
- [[patterns/model-cost-routing]] — Factory Router auto model selection (not detailed in the post)
