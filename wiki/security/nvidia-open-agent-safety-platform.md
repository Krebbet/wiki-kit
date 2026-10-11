# Nvidia Open Agent Safety Platform (OpenShell + Sentry)

Nvidia's Open Agent Safety Platform (announced ~2026-10, reported by Constellation Research) is an open-sourced reference design for agent containment that pairs a software runtime, OpenShell, with a DPU-based out-of-band monitor, Sentry, so that deterministic infrastructure rules rather than the agent itself bound what an agent can do. It is the wiki's first hardware-rooted enforcement plane outside the agent's trust boundary. The source is a secondary analyst/press summary of a vendor announcement and call; treat capability claims as collect-but-confirm.

## Components

- **OpenShell** (open source, version 0.1.0) lets developers set limits on agent actions and acts as a secure agent runtime. It targets Nvidia Vera CPUs but also runs on x86 and Arm and alongside third-party software and hardware. Nvidia declares 0.1.0 stable and "production ready"; it has been in partner early access since March, and partners such as Red Hat will ship it under their own release names. Nvidia claims support for "tens of thousands" of concurrent sandboxed agents, with no benchmark given.
- **Sentry** runs on Nvidia BlueField-4 DPUs, outside the agent's environment. It monitors agent activity "in silicon", can enforce security rules, and can quarantine an agent. It is not open source: it is built only for BlueField. Nvidia says the APIs are open so other chips could be used, but that is a promise, not something shown. Sentry's availability, licensing and API spec are not detailed in the source.

## Thesis

Justin Boitano (VP, enterprise AI) argues that deterministic rules must govern probabilistic agents: "An agent cannot be expected to fully police its own behavior. Infrastructure needs to enforce explicitly." The framing is least privilege (define what an agent can and cannot do, "and no more") and explicitly treats safety as an engineering problem, sidestepping the alignment debate. Nvidia's analogy is that sandboxing and trust layers made internet commerce safe; agents need independent controls to stop them breaking out of evaluation environments or drifting from tasks. The same principle, "an agent cannot be its own security authority", appears in [[security/microsoft-execution-containers]], released the same week.

## Claims to treat with caution

- Boitano said that, based on known details, the reference design would have stopped the OpenAI-Hugging Face incident (hedged with "each security incident is unique"). This is an untestable, vendor-favorable counterfactual; see [[security/cyber-eval-sandbox-escapes]].
- OpenShell "can catch agents coordinating before they write a zero-day exploit", and Sentry "can see an agent starting to think about exploits". No mechanism or eval is given; this is most plausibly behavioral or telemetry-level monitoring, not literal reasoning inspection.
- Partner alignment (Anthropic, SpaceX, HPE, Dell, Cisco, IBM, Oracle, Microsoft, Salesforce, SAP, ServiceNow, most security vendors) is announced, not shown as shipped integrations. Anthropic and Nvidia are said to use OpenShell to build security into Claude Managed Agents. Microsoft's own post states Nvidia integrated OpenShell into MXC (file and inference-service policy, network controls, credential management, OCSF auditing), which is a vendor-confirmed integration on the Microsoft side.
- Constellation's view: plausible given Nvidia's Intel and Arm ties; liability is the real driver and the approach may slow regulation.

## Why it matters

Prior containment on the wiki is network or VM isolation (egress-allowlisted VMs in [[governance/anthropic-ai-native-sdlc]], microVMs in [[deployments/cognition-cloud-agents]]) or software policy ([[governance/org-control-layer]], [[patterns/agent-libos]]). Sentry adds a separate-silicon plane that a compromised host or agent cannot reach, at the cost of hardware lock-in and no published evidence of detection quality. It is one more distinct layer for the defense-in-depth reading of [[conflicts/auto-mode-prompt-injection-defense]].

## Source

- Constellation Research, "Nvidia launches Open Agent Safety Platform to secure AI agents" — https://www.constellationr.com/insights/news/nvidia-launches-open-agent-safety-platform-secure-ai-agents (analyst/press page; raw/research/weekly-2026-10-11/02-nvidia-open-agent-safety-platform.md)
- Microsoft Windows Developer Blog (OpenShell-in-MXC integration claim) — raw/research/weekly-2026-10-11/03-microsoft-execution-containers.md

## Related

- [[security/cyber-eval-sandbox-escapes]] — the failure class Nvidia claims this design would have stopped
- [[security/microsoft-execution-containers]] — OS-level policy containment; Nvidia integrated OpenShell into it
- [[security/rogue-model-containment-disclosure]] — containment-disclosure and liability context
- [[conflicts/auto-mode-prompt-injection-defense]] — additional defense-in-depth layer (out-of-band monitoring)
- [[governance/org-control-layer]] — model-agnostic enforcement at the execution boundary
- [[patterns/agent-libos]] — capability and least-privilege runtime, software-side parallel
- [[governance/anthropic-ai-native-sdlc]] — egress-allowlisted VMs; Anthropic adopting OpenShell for Managed Agents
- [[deployments/microsoft-agent-365]] — Microsoft governance plane; Microsoft is a listed partner
