# The Age of Async Agents — Latent Space (Cognition + OpenInspect)

A Latent Space podcast episode (May 28 2026) featuring Cognition CPO Walden Yan and OpenInspect creator Cole Murray on the architecture, production realities, and emerging patterns of cloud and background coding agents. The episode covers the December 2025 model-capability inflection that made spec-to-PR workflows practical, Devin's internal brain/machine architecture, repo setup as the hardest unsolved operational problem, memory system design, multi-agent limitations, AI slop detection, and enterprise entry-point use cases.

## Source

- `raw/research/weekly-2026-05-31/01-latent-space-async-agents.md` — captured 2026-05-31 from `https://www.latent.space/p/cognition`.

## The December 2025 Inflection

Cole Murray dates the background-agent wave to a specific capability threshold reached around December 2025 with models Opus 4.5 and GPT 5.2:

> "We moved away from handholding the model and being able to actually more or less autonomously drive the model... We could pretty much go from a specification to a completed pull request, assuming the spec was good enough, with very little friction."

Walden Yan corroborates from Cognition's internal data: merged PR count grew 7x over roughly two to three months (collect-but-confirm), and Devin-authored commits rose from 16% (January 2026) to 80% (March 2026) of all Cognition repository commits (collect-but-confirm). Yan frames 2025 as a continuous ramp, with each leap — including Sonnet 3.7 — enabling the removal of scaffolding that compensated for lower model intelligence.

## Three-Wave Practitioner Periodisation

Yan and Murray describe three eras of AI coding tool adoption:

1. **Copilot/autocomplete** — developer remains in the loop; workflow bottlenecked on local IDE interaction.
2. **Local agents** — Claude Code, Windsurf, Cursor agents pane; one or many terminals running concurrently but still foreground.
3. **Async cloud agents** — agent orchestration for end-to-end development in the background; the current era.

This framing parallels Cursor's Michael Truell "third era" framing and Steve Yegge's eight-level adoption ladder (cited but not reproduced in the episode).

## Harness Architecture: In the Box vs. Out of the Box

The central architectural decision for background agent systems is whether the agent harness runs inside the sandbox ("in the box") or outside it ("out of the box").

**In the box**: simpler state management because all agent state is co-located in the sandbox; but all secrets must also live in that box, raising secret-exfiltration risk.

**Out of the box**: the "brain" (LLM inference, decision logic) runs on a separate control plane and makes tool calls into the sandbox ("the machine"). This is Devin's architecture. It is more complex — state must be managed across the control plane/sandbox boundary — but it is the preferred security posture because secrets can be scoped to the machine independently of the brain.

Walden Yan explains the practical benefit:

> "Whatever you put on the machine, that is the scope of basically what the agent is free to do. Only put the most scoped secrets on that machine, and then the brain is fully not accessible from the machine."

OpenInspect currently runs harness in the box (Cloudflare for control plane, Modal as primary sandbox provider, Daytona contributed, E2B on roadmap) and is planning a migration to out-of-box. The Anthropic Managed Agents architecture and OpenAI's equivalent are cited as out-of-box examples.

## Repo Setup: The Perennial Hard Problem

Both Yan (Cognition) and Murray (OpenInspect clients) independently name repo setup — keeping the agent's working environment current with dependencies, credentials, and runnable services — as the hardest recurring operational problem.

Requirements for agent-ready repo setup:
- Local DB and Docker Compose so agents can run and test without production credentials.
- Scoped secrets; "go talk to Bob" credential handoffs are not automatable.
- A `setup.sh` hook (OpenInspect supports this) that pre-installs dependencies, pre-snapshots the environment, and restores state on resume.
- Migration from production-only service integrations to local mocks, especially for microservice architectures.

**Older codebases carry more migration burden.** Companies that pre-date Docker or that never built local dev paths must migrate before agents can test reliably. Murray: "The older the company, the more you have to change."

**Docker alone is insufficient.** Containers are not true security boundaries, and Docker-in-Docker is problematic when agents need to run real applications. Full VMs are required for arbitrary application testing.

### VM Infrastructure Details (Cognition)

- Boot times on raw cloud VMs (EC2) were initially ~10 minutes per session; unacceptable for repeated down/up cycles.
- **BlockDev** was Cognition's custom file-system format: incremental diff-based VM snapshots so save/restore cost is proportional to the file-system diff, not the full disk. Now superseded by a newer internal system.
- NFS/S3-backed network file systems cause severe Grep slowness on agent VMs (each grep triggers network calls). Cognition replaced the network file system with a real local file system to fix this.
- **Nested virtualization** is used for Android emulation inside Firecracker microVMs (beta at recording time).

## Testing vs. Computer Use

Yan distinguishes testing from computer use: computer use is emitting the correct coordinates to click a button. Testing is reasoning about how to orchestrate a multi-service application, reproduce a feature with the right credentials and feature flags, and confirm that a cross-cutting change (frontend + backend + downstream service) actually works end to end. The testing problem is arbitrarily hard and sometimes requires orchestrating multiple frontier models together. Devin generates a video of the test run with annotated labels; Walden: "I know it works" — the "AGI moment" where a PR can be merged without reading the diff.

## MCP Limitations for Enterprise Integrations

Yan: MCP's simple tool-calling surface is insufficient for first-class enterprise integrations. Slack is the canonical example: an MCP server can post messages, but using Devin as a coworker in Slack requires bidirectional webhooks, natural conversational threading, and careful tuning to avoid spamming channels.

> "When the MCP spec starts to get too complicated, it starts to lose its original promise of being a simple one-step connect. Now we have to go figure out how to support all these different variations of things, and it starts to look a lot like just building the first-party integrations."

Walden says he would prefer an interface more expressive than MCP — bidirectional, not just a tool list. The MCP sampling mechanism exists in the spec but is unused in practice. This aligns with (but is a sharper critique than) the connector-vs-MCP-app distinction in [[deployments/anthropic-finance-agents]].

## Memory: Devin's Knowledge System

Devin's memory system is called Knowledge. Key design properties:

- **Auto-generation**: ~95% of memories are auto-generated (collect-but-confirm). When the user corrects Devin (e.g., "that's not how we use Git"), Devin prompts: "Do you want me to remember this for the future?" The user approves or rejects.
- **Retrieval is unsolved**: with thousands of memories, ensuring the right ones surface without flooding context is the main unresolved problem. Continuous eval work is required as models change.
- **Generation precision matters**: a one-off request ("open as draft PR") should not become a universal memory ("always open draft PRs").
- **File-system direction**: Cognition is exploring rebuilding memory as a file system the agent navigates natively, since models are now very good at file-system interfaces. Memory editing (not just pruning) is already supported — a stale memory can be updated rather than deleted.

Cole Murray's clients primarily address memory through skills and `CLAUDE.md`-style files. He cites the retrieval problem as the reason he has not built a memory system into OpenInspect.

## Always-On Agents as Permanent Product Owners

An emerging use case beyond coding: an always-on agent with a `memory.md` file that serves as a permanent PM for a specific product area or Slack channel. The agent:
- Maintains a live priority list.
- Tags the right humans when escalation is needed.
- Creates and triages tickets.
- Acts as a continuous interface between engineering, support, and product.

Yan: "Can we actually upstream above the engineering process and maybe it's just Devin creating tickets, which then maybe some humans do, but then maybe other Devins do."

## Multi-Agent Orchestration: The Working Regime

Swarms of collaborating agents add more chaos than capability in current practice. Cognition gave Devin an MCP to message and spawn other Devins; the result was "a really chaotic world." The working regime is:

- **Single agent or manager-subagent**: one Devin per task; manager-subagent for parallelism.
- **Isolated sandboxes**: each sub-agent gets its own VM with no shared state. "Figuring out how to segregate the work and have other Devins work on it in a relatively isolated sense, each with their own boxes, not sharing machines — that is the regime you have to create today."

Sub-agents invoked for lookup tasks (e.g., DeepWiki for codebase context) are more tool calls than true multi-agent collaboration. Yan distinguishes this from genuine multi-agent coordination and notes that models' newfound ability to push back on incorrect suggestions is the first promising signal that true multi-agent collaboration may become viable.

## Auto-Merge Vibe Coding and Codebase Entropy

Cognition's internal experiment (state-of-the-art as of December 2025 models, collect-but-confirm): uncontrolled auto-merge without code review produces an unworkable codebase within approximately **two weeks**. The failure mode is not a single error but entropy accumulation — a UI button ends up implemented in ten slightly different places; a small change requires coordinating all variants.

Murray's framing: "Your codebase regresses to your worst engineer, because that engineer who is very gung-ho about AI and is not auditing their code, their pattern starts cementing into the code, and now the AI is referencing their patterns." Recommended mitigation: scheduled deduplication and cleanup passes, either human or automated.

Module-boundary discipline is swyx's complementary recommendation: strict contracts between modules enforced by humans, loose autonomy within modules.

## AI Slop Detection

Identifiable AI code anti-patterns, with recommended enforcement tooling:

| Pattern | Language | Likely cause | Enforcement |
|---|---|---|---|
| `hasattr` / `getattr` on objects | Python | Reward-hacking: code avoids raising exceptions | Semgrep lint rule: fail PR on `getattr` |
| Backwards-compatibility re-exports | Python/TS | Reward-hacking: avoids modifying import sites | Semgrep |
| Untyped tuples (`dict[str, Any]`) | Python | Avoiding type errors | Linting |
| Verbose inline PRD comments (Opus 4.7+) | Any | Model explains rationale, alternatives, and trade-offs in every function | Configurable verbosity setting (planned) |

The `getattr` pattern is so common at Murray's clients that it is now a standard PR-blocking lint rule. The backwards-compat re-export pattern appears in both GPT models and Claude 4.6.

Walden's observation on verbose commentary: it may be directionally correct for self-maintaining systems (inline specs that future agents can consume), but it is currently too noisy. The **GitAI** concept — storing agent prompts in Git metadata alongside code so future agents and reviewers can access decision rationale — is the cleaner version of this direction.

## SRE Auto-Triage: The Highest-ROI Enterprise Entry Point

Murray: the most common and highest-ROI enterprise entry use case is SRE auto-triage — the agent is the first responder on alerts (Slack, Datadog, Sentry). It does not necessarily resolve the issue; it collects context, queries production logs and databases, applies playbooks, and produces a trajectory plus an initial PR candidate. OpenInspect supports a trigger for this; the flow is "alert → agent trajectory → PR, fully autonomously."

Additional enterprise entry points:
- **Non-engineers creating PRs via Slack** (PMs, marketing, support).
- **Continuous security scanning** — ongoing autonomous security review.
- **Customer support context gathering** — agent cross-references logs and code to produce complete bug context before engineering engagement.

Typical AI agent spend range cited by Murray: **$1k–$5k per engineer per year** across his clients (collect-but-confirm).

## Hybrid Model Routing ("Smartfind")

An emerging pattern Walden Yan coined internally at Cognition ("Smartfind"): sub-frontier models handle the bulk of agent steps for speed and cost; frontier models are called out for the hardest sub-tasks. As frontier models become more expensive and capable, and sub-frontier models catch up on routine tasks, hybrid routing becomes the dominant cost-optimization strategy.

## Windsurf 2.0 and the Local-Cloud Handoff

Cognition's Windsurf 2.0 positions the local IDE as a command center for managing both local foreground agents and background cloud agents. The design intent: a user should never have to leave the local window to orchestrate agents, pull a background task to foreground for testing, or approve and push. Local agents and cloud agents are deliberately parameterized differently: local agents are faster and more interactive; cloud agents run fully autonomously until they have a complete report and test video.

Cognition also sells beyond Devin: compute infrastructure, onboarding and adoption engineering, enterprise integrations, and VPC/on-prem/FedGovCloud deployment.

## Related

- [[deployments/cognition-cloud-agents]] — primary prior source on Devin infrastructure; this episode is a richer and more recent primary-source extension.
- [[deployments/cursor-cloud-agents]] — harness architecture parallels; Cursor's three-way state decoupling vs. Devin's brain/machine separation; both name repo setup as a hard problem.
- [[patterns/topology-taxonomy]] — the three-wave async-agent framing adds practitioner-confirmed periodisation; multi-agent swarm failure corroborates manager-subagent finding.
- [[patterns/effective-harnesses]] — VM infrastructure decisions, repo setup as a first-class harness concern, local testing pre-conditions.
- [[patterns/harness-design-space]] — harness in/out of box adds a named architectural dimension.
- [[memory/memory-architectures]] — Devin's Knowledge system (auto-prompt on correction, ~95% auto-generated, file-system direction) is a production instance.
- [[patterns/sierra-context-engineering]] — context engineering term: Walden Yan acknowledges co-usage of the term; the original Cognition "Don't Build Multi-Agents" post is the primary citation.
- [[case-studies/notion-token-town]] — both sources independently conclude MCP alone is insufficient for first-class Slack/enterprise workflows.
- [[deployments/openai-symphony]] — both Symphony and Devin arrive at manager-subagent as the working multi-agent regime; OpenInspect's open-source positioning contrasts with OpenAI's zero-human-review greenfield approach.
- [[security/adr-uber-mcp-detection]] — Devin's brain/machine separation and scoped-secrets model is the architectural answer to the threat surface the ADR targets.
- [[case-studies/willison-vibe-agentic-convergence]] — Walden's two-week auto-merge experiment provides a concrete timeline for the quality-signal collapse Willison discusses.
- [[deployments/anthropic-finance-agents]] — connector-vs-MCP-app distinction aligns with Devin's first-party Slack integration rationale.
