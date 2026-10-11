# Microsoft Execution Containers (MXC)

Microsoft Execution Containers (MXC 1.0.0, announced generally available 2026-10-07 on the Windows Developer Blog) is a policy-driven, cross-platform containment layer that enforces file, network, process and UI boundaries on agent workloads outside the agent's control. The stated thesis is "An agent cannot be its own security authority": the boundary is set by developer and organization and enforced independently of the model, generated code, plugin or tool. Entra agent identity and Agent 365 / Intune management for local agents are announced as "coming soon". Vendor-primary source: mostly trustworthy on mechanism and availability, but ecosystem-support claims and the absence of attack-resistance evidence warrant confirmation.

## Architecture

Developers declare workload requirements in one JSON config schema plus a multi-language SDK; MXC maps them to a chosen backend on Windows, macOS or Linux, separating requirements from platform-specific containment. Policy areas: containment type, process (command, args, cwd, env), file system (read-write, read-only, denied), network (inbound, outbound, host loopback) and user interface (desktop access). Worked example: a coding agent gets read/write on the repo and read-only on production server config; a write to server config is blocked regardless of what the model decides.

Four backends, a spectrum of isolation:

- **Process container** (Windows 11, macOS, Linux): AppContainer, Seatbelt or Bubblewrap; lightweight, for model-generated code and tool execution.
- **Session container** (Windows 11): separate Windows account and session with its own local agent identity and isolated desktop, clipboard, UI and input; for long-running or desktop agents.
- **WSL container** (Windows 11): Linux toolchains via WSL.
- **MicroVM** (Windows 11 and Linux, experimental): hardware-enforced isolation and full Linux compatibility for higher-risk work; compare [[deployments/cognition-cloud-agents]].

The post says each backend has distinct security properties but gives no per-backend threat model or escape analysis.

## Layered policy and modes

Workload policy from the developer is combined with organizational policy (Intune, "soon" for Windows 11 process containers), so the same agent can run under different enterprise boundaries without code changes. Agents are expected to handle stricter boundaries by explaining the block, requesting user or admin action, or choosing a safe alternative.

Three operating modes: **Enforcement** (ungranted access blocked), **Learning** (blocked and recorded to a JSON activity report) and **Permissive** (allowed and recorded, other OS or org restrictions still apply). Activity reports are Windows process containers only. The intended workflow is to observe access, then author least-privilege policy; the post suggests having a coding agent draft the initial policy for human review.

## Platform pillars and ecosystem

Containment (MXC, GA now), Identity (Entra separates agent from user activity so a compromised agent can be restricted without blocking the employee; not yet shipped) and Manageability (Agent 365 extended to local agents, Intune policy; soon). See [[deployments/microsoft-agent-365]]. Windows 365 support for MXC (agents on Cloud PCs) is GA.

Vendor-stated support already exists for GitHub Copilot, OpenClaw ([[memory/openclaw]]), OpenAI Codex, Replit, LM Studio and Unsloth AI. Anthropic Claude Code, Box, Egnyte, Heidi Health, Hermes Agent, Manus, Perplexity, Raycast and Simular are "will be releasing support" (announced, not shipped). Nvidia integrated OpenShell into MXC, adding file and inference-service policy, advanced network controls, credential management and OCSF auditing; see [[security/nvidia-open-agent-safety-platform]].

## Limits and open questions

- No performance numbers, no benchmarks, no evidence of resistance to deliberate escape; language is "designed to prevent".
- Session container and activity reports are Windows-only; MicroVM is experimental; Entra and Intune pieces are not yet available.
- Relevance: an OS-enforced policy layer independent of model behavior, a counterpart to classifier-gated permissions ([[governance/claude-code-auto-mode]]) and to network-egress containment ([[governance/anthropic-ai-native-sdlc]]). The sandbox-escape incidents in [[security/cyber-eval-sandbox-escapes]] were misconfigured boundaries, which declarative policy aims to address. [[patterns/agent-plugins-spec]] has no permission model; MXC could supply enforcement for plugins and tools.

## Source

- Microsoft Windows Developer Blog, "Microsoft Execution Containers: policy-driven containment for AI agents" (2026-10-07) — https://blogs.windows.com/windowsdeveloper/2026/10/07/microsoft-execution-containers-policy-driven-containment-for-ai-agents/
- Code, SDK, schema and samples: https://github.com/microsoft/mxc
- raw/research/weekly-2026-10-11/03-microsoft-execution-containers.md

## Related

- [[deployments/microsoft-agent-365]] — Entra agent identity and local-agent management continuation
- [[security/nvidia-open-agent-safety-platform]] — OpenShell integrated into MXC; out-of-band hardware monitor
- [[security/cyber-eval-sandbox-escapes]] — containment failures from misconfigured boundaries
- [[conflicts/auto-mode-prompt-injection-defense]] — OS-sandbox layer data point
- [[governance/claude-code-auto-mode]] — classifier-gated permissions; Claude Code listed as upcoming MXC adopter
- [[governance/anthropic-ai-native-sdlc]] — egress-allowlisted coding VMs
- [[deployments/cognition-cloud-agents]] — microVM isolation parallel
- [[patterns/agent-libos]] — capabilities enforced outside the agent
- [[patterns/agent-plugins-spec]] — plugin spec lacking a permission model
- [[memory/openclaw]] — OpenClaw named as an MXC-supported agent
