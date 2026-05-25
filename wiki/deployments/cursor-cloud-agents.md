# Cursor — Cloud Agents (Engineering Retrospective)

Cursor's engineering retrospective on one year of building cloud agents identifies three load-bearing architectural lessons: (1) development-environment quality is the single largest determinant of agent output quality and degrades *silently* — no crash, just worse results — making environment provisioning the primary infrastructure investment; (2) agent loop, machine state, and conversation state must be kept as fully decoupled components, which is the mechanism enabling heterogeneous pod types, independent pod lifecycle management, and retry-safe streaming; (3) the harness is not converging on a stable form but on a progressively emptier one — logic migrates from harness into agent-controlled tools as models improve. The post also describes migrating from a fragile work-stealing scheduler to Temporal-based durable execution, which moved reliability from one 9 to two 9s, and names the entire environment-provisioning stack as "enterprise IT for agents."

## Development environment as silent quality determinant

Cloud agents cannot inherit the developer's laptop environment. Every dependency, credential, network permission, and tool must be explicitly provisioned. When provisioning is incomplete the agent continues running and producing output — degradation is silent, not a crash. Cursor frames this as increasingly consequential: as base model capability has improved, the ceiling on quality is now set more by environment completeness than by model reasoning.

The infrastructure Cursor identifies as required:
- User-authored tooling for building the agent's development environment
- Hibernate/resume pipelines between messages to avoid burning compute at idle
- Checkpoint/restore/fork pipelines for VM images
- Network access with secret redaction and per-agent network policies
- Credential management integrated with the harness and client

Future direction: self-healing environments where agents detect missing secrets, blocked network access, or broken toolchains and act to repair them — linked to a separate "autoinstall" research direction.

## Three-way state decoupling

Cursor's canonical architecture separates three components that earlier cloud agent designs collapsed together:

- **Agent loop** — the Temporal workflow; lives entirely outside the VM.
- **Machine state** — the VM filesystem and process state; managed independently of the agent loop.
- **Conversation state** — append-only storage that streams conversation updates to web and desktop clients; handles retries by allowing the client to detect partial output, rewind the stream, and display new data after a failed-then-retried step.

Because the agent loop lives in Temporal rather than on the VM, pod lifecycles can be managed independently. This decoupling directly enables two pod types Cursor now operates: readonly VMs and prewarmed VMs. It also enables resumability — if a pod is preempted or fails, the Temporal workflow resumes against a freshly restored VM without replaying conversation state.

## Progressive harness retreat

The harness is an evolving artifact, not a stable product. Cursor's trajectory: as models improve, logic previously embedded in harness code (hardcoded repo-layout handling, hardcoded CI-log injection) migrates into agent-controlled tools and agent reasoning.

Concrete before/after examples:
- **CI Autofix (earlier):** harness grabbed job failure logs and wrote them into the VM directly. **CI Autofix (current):** harness hands the agent the GitHub CLI and writes large outputs to files the agent can search. Notification logic became substantially simpler.
- **Multi-repo (a year ago):** required hardcoded harness behavior to navigate cross-repo layouts. **Multi-repo (current):** agent receives repo layout and branch/PR tools and decides the approach itself.

The direction is "get out of the way" — harness scaffolding remains only where models are not yet ready for autonomous operation. Computer-use is the current example: a dedicated subagent type with its own model routing, custom prompting, and screen recording exists because models are not yet ready to drive computer-use autonomously; scaffolding persists, but agent controls invocation. VNC and Chrome belong to the shared environment accessible by both parent and subagent; parent can also directly execute Playwright scripts.

## Temporal durable-execution migration

Cursor's original architecture used work-stealing: worker nodes picked up tasks and looped agents to completion. This was fragile — the early cloud agent beta operated at approximately one 9 of reliability (~90%). Migrating to Temporal for durable execution is described as the single biggest reliability improvement, moving Cursor past two 9s.

Workflow architecture also evolved: from "eternal" long-lived agent workflows (one workflow per session, never exits) to multiple shorter workflows that exit after a single task. The shorter-lived design simplifies version upgrades since in-flight workflows no longer block deploys. Activities were also split out from monolithic workflow logic to better capture timeouts and retries as async tool calls, subagent invocations, and inference-provider outages changed the underlying assumptions about activity duration.

Cursor reports (collect-but-confirm): >50 million actions/day across >7 million unique workflows on Temporal.

## Scale and internal adoption

Cursor reports (collect-but-confirm): >40% of PRs merged to the Cursor monorepo now come from cloud agents, described as growing. This is a vendor-self-reported internal metric — no independent verification.

## Source

- `raw/research/weekly-2026-05-25/01-cursor-cloud-agents.md` — captured 2026-05-25 from the Cursor engineering blog, "What we've learned building cloud agents." Analyst summary at `raw/research/weekly-2026-05-25/.ingest/01-cursor-cloud-agents.summary.md`. **Primary vendor engineering writeup** — architectural descriptions of what Cursor built and decided are trustworthy; reliability metrics and PR-share figures are vendor self-reported (collect-but-confirm).

## Related

- [[case-studies/cursor-agent-harness]] — companion Cursor harness-evaluation writeup (CursorBench, Keep Rate, LLM-judge, per-model tool-format provisioning); this page extends it with cloud-deployment architecture, durable execution, and state-decoupling framing
- [[deployments/cognition-cloud-agents]] — direct peer: microVM + hypervisor-level snapshotting vs Temporal-based durable execution; both solve the async gap but via different mechanisms
- [[patterns/effective-harnesses]] — both describe harness retreat as models improve; Cursor names it "get out of the way," the effective-harnesses page names try-too-much and declare-done-prematurely failure modes
- [[deployments/openai-symphony]] — peer cloud deployment; Symphony = Elixir orchestrator with multi-Codex; Cursor = Temporal with dedicated VM environments; both report high agent PR share (collect-but-confirm)
- [[deployments/shopify-simgym]] — peer cloud-scale agent deployment with different workload (shopper-bot simulation vs software development)
- [[patterns/agentic-harness-engineering]] — both treat harness as an evolving artifact; AHE evolves via observability loop; Cursor via progressive trust transfer to agent
- [[patterns/externalization-survey]] — Cursor's state-decoupling trifecta (agent loop / machine state / conversation state) is a concrete instantiation of the externalization-survey's harness externalization arc
- [[patterns/topology-taxonomy]] — decoupled state enabling heterogeneous pod types and parent-subagent topologies is a new concrete cloud-deployment topology instance
