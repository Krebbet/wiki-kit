# Agent libOS: Library-OS-Inspired Runtime for LLM Agents

Agent libOS is a research prototype from Tsinghua University that applies library-OS and capability-system concepts to define a structured runtime substrate for long-running LLM agents. Its central claim is that current agent frameworks conflate model-facing tool visibility with host-resource authority — a fragility that enables prompt injection, confused-deputy attacks, and uncontrolled side effects — and that this should be fixed at a stable runtime boundary below the tool layer, not by adding wrapper-level confirmation prompts.

## Core contributions

1. **"Tools are libc, primitives are the authority boundary"** — a design rule separating the model-facing action surface (which can evolve freely) from runtime primitive managers (which enforce capability checks, policy, blocking semantics, and audit). Visibility of a tool schema does not imply authority to touch the resource it wraps.

2. **AgentProcess model** — a schedulable execution subject with process identity, parent-child lineage, lifecycle state, a capability set, a tool table, per-process Object Memory namespace, working directory, checkpoint head, and audit records. Supports spawn, fork, exec, wait, signal, pause, resume, and exit with attenuating semantics: forked children do not inherit parent filesystem-write authority; exec cannot escalate to a target image's required capabilities.

3. **Runnable Python prototype** with async scheduling, namespace-local Object Memory, Deno/TypeScript JIT tools, shell and image-registry primitives, injectable Resource Provider Substrate, deterministic demo, and a 123-test regression suite.

4. **Architectural evaluation over execution accuracy** — the paper explicitly does not claim improved task success on SWE-bench or other planner benchmarks; it claims only that runtime enforcement properties are correctly implemented.

## Architecture

The system is organized as a four-layer stack:

- **Agent personality / application** — domain role, system instruction, task policy, planner behavior (can use any existing framework: ReAct, AutoGen, LangGraph, etc.)
- **Skills/Tools layer** — LLM-facing schemas and wrappers; "libc-like surface, not the trust boundary"
- **Agent libOS runtime** — processes, Object Memory namespaces, capabilities, human queues, syscall broker, events, checkpoints, audit, filesystem/shell/image/clock/process primitive managers
- **Resource Provider Substrate** — injectable providers for filesystem, clock/sleep, shell subprocesses, and future host services

**Capabilities** bind subject, resource, rights, constraints, issuer, lifetime, and revocation status. Revocation takes effect on the next primitive call — wrapper-level code cannot bypass it. Filesystem write policies: `always_allow`, `always_deny`, `ask_each_time`, `allow_once`. Under `ask_each_time`, a blocking human approval request is created; approval grants a single-use capability consumed by one successful primitive call.

**Object Memory** is a typed, capability-protected object graph with namespace-local names (names are not capabilities; knowing a name does not grant access). Object payloads live in volatile runtime memory; SQLite stores directory metadata. A materializer — not the model — converts the memory view into bounded textual context before each model call.

**Human approval** is a first-class blocking operation: a process enters `WAITING_HUMAN`, the runtime supervisor drains the approval queue, applies the decision, and resumes the pending action — analogous to a blocking system call on a terminal device. Approval previews use repr-escaped content to prevent injection of fake trusted instructions via untrusted file content.

**Shell primitive** accepts an argv array, not a command string; no shell expansion. Process-scoped shell policies: `always_deny`, `allowlist_auto_else_ask`, `blocklist_ask_else_auto`, `always_allow`. Matching is over tokenized argv, including inspection of interpreter chains.

**JIT TypeScript tools** run in Deno with all host permissions denied by default (no disk/network/env/subprocess/FFI). Static imports restricted to a jsr: allowlist; npm:, node:, eval, Function, Worker, WebAssembly entry points rejected during validation. The tool's only runtime entry point is a LibOSSyscallSession, which dispatches named syscalls through the same primitive managers — subject to the same capability checks, human approval rules, and audit as any built-in tool.

**Checkpoints** snapshot reconstructable state (process metadata, object-directory state, capability metadata, checkpoint heads). They do not roll back irreversible external effects; those must be represented as audit events and compensated explicitly.

## Results / Evidence

The evaluation is systems-artifacts-oriented, not benchmark-driven (author-credible; Tsinghua CS, single-author preprint arXiv 2606.03895, 2026).

All 12 property categories in the 123-test regression suite pass:

| Property | Result |
|---|---|
| Tool visibility is not authority | Pass |
| Workspace containment (path escape rejected) | Pass |
| Fork/spawn attenuation (no inherited write authority) | Pass |
| Namespace isolation (same local names resolve independently per process) | Pass |
| Memory cleanup on exit (scratch objects released, explicit results retained) | Pass |
| Per-use approval (ask_each_time blocks, grants once, re-prompts on next use) | Pass |
| Human and child-wait resumption (no spurious tool failures) | Pass |
| Async sleep (two processes alternate cooperatively) | Pass |
| Deno JIT syscall isolation (libos.syscall only; cannot bypass capabilities) | Pass |
| Image registration authority (requires filesystem + image-registry capability) | Pass |
| Resource Provider Substrate injectability | Pass |
| Wrapper purity (built-in tools do not call host APIs directly) | Pass |

No task-success, latency, cost, or human-workload measurements are reported; the author explicitly flags these as requirements for a "stronger empirical paper."

## Implications for harness engineering

**Reframe the trust boundary.** Most harnesses today use tool wrappers as both the action surface and the effective security boundary. Agent libOS demonstrates that these should be separate layers. Practically: if you want revocable authority, you need primitive-level checks, not wrapper-level guards.

**Capability attenuation on fork/spawn.** Multi-agent topologies that fork subtasks should explicitly scope down authority at fork time. Implicitly passing the parent's full capability set to children is the confused-deputy pattern at the orchestrator level.

**Human approval as a scheduler primitive.** Treating human approval as a blocking runtime operation (rather than an ad hoc callback or polling loop) makes it composable with async scheduling — other agents continue running while one waits on a human.

**JIT tool generation needs sandboxed execution.** If agents can generate and register new tools at runtime (Voyager-style skill accumulation), those tools need a deny-by-default execution environment with a narrow syscall surface back into the runtime. The Deno + syscall-broker pattern is a concrete implementation of this.

**Object Memory over raw transcripts.** Typed, provenance-bearing objects with namespace-local names and explicit materialization give the runtime control over what enters the model's context window — enabling compaction, access control, and audit without relying on the model to self-manage its context.

**Audit completeness.** Audit records should answer: which process acted, which primitive, which resource, which authority allowed/denied, which human decision was involved. This enables post-hoc forensics for long-running agents and is necessary before deploying agents with irreversible side effects in production.

**Current limitations to watch:** Deno JIT sandbox is not production-grade (Docker/Firecracker still needed for stronger deployments); checkpoint rollback of external effects is unimplemented; context management (compaction, paging, retrieval) is preliminary; audit log is a flat stream without indexed queries; distributed scheduling is future work.

## Source
- arXiv: 2606.03895 — Yingqi Zhang, "Agent libOS: A Library-OS-Inspired Runtime for Long-Running, Capability-Controlled LLM Agents," Tsinghua University, 2026. Implementation: [github.com/yingqi-z20/Agent-libOS](https://github.com/yingqi-z20/Agent-libOS)

## Related
- [[patterns/harness-design-space]] — Agent libOS proposes a new substrate layer below existing harness frameworks, sitting between model-facing tools and host resources
- [[patterns/code-as-agent-harness]] — the "tools as libc" rule and JIT TypeScript tool generation are closely related to code-as-substrate patterns
- [[patterns/effective-harnesses]] — runtime primitive authority boundary has direct implications for practical harness safety and approval patterns
- [[patterns/moss-production-self-evolution]] — capability-gated JIT image/tool registration is related to runtime self-extension and skill accumulation
- [[patterns/topology-taxonomy]] — fork/exec/spawn process tree defines a structured multi-agent topology with explicit lineage and authority attenuation
- [[deployments/cognition-cloud-agents]] — production agent deployments would benefit from the audit, revocation, and human-queue primitives described here
