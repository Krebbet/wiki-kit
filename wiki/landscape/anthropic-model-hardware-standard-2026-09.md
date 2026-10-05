# Anthropic Model Hardware Standard (MHS) — Research Preview (2026-08-27)

Anthropic opened a research preview of the **Model Hardware Standard (MHS)** — a model-agnostic protocol letting AI agents directly read sensors and write to actuators to operate physical lab and manufacturing equipment (robotic arms, microscopes, liquid handlers, lasers), including autonomous recovery from hardware errors. Developed with **HHMI Janelia Research Campus**; shared first with scientific research labs and advanced manufacturers, with a stated intent to eventually open-source the standard. This is a genuinely new technical primitive — an **agent-to-physical-hardware control protocol** — distinct from software-only tool-use/MCP patterns.

## What MHS actually does

- **Standardized driver layer**: translates between an OS and any hardware device with a programmable interface, using simple "read"/"write" primitives (e.g., "get temperature," "set temperature"). Devices become network-discoverable without bespoke per-device integration code.
- **Natural-language device onboarding**: the driver embeds tags a human can fill in via plain language (or by being interviewed by an agent) — device characteristics not derivable from code alone (e.g., a robot arm's weight, relevant for safe manipulation). This auto-generates a reference file covering what the device can measure, adjust, and its enforced safety limits — everything an agent needs to operate a device it has never seen before.
- **Three control mechanisms**: MCP, CLI, and code files (APIs) — used together, letting an agent orchestrate multiple devices via a single line of code.
- **Explore-then-compile pattern**: Anthropic reports Claude interacts with new hardware "in an exploratory manner, much as a scientist would" — e.g., adjusting a laser, observing camera feedback, iterating — then **packages what it learned into a deterministic code script** so the calibrated procedure can run as a single command without per-step reasoning thereafter. Reduces integration time from weeks/months to hours/minutes per Anthropic's claim.
- **Runtime supervision model**: once devices are connected, the agent sequences steps across instruments, monitors results, adjusts parameters in real time, and can chain driver commands into code files for long-running or faster-than-reasoning-speed operation, without needing to reason at every step.

## Early partner deployments (Anthropic-reported)

- **Genentech** — BCA protein-assay automation coordinating a liquid handler, robotic arm, and plate reader.
- **UW Baker/Pinglay labs** — remote instrument dashboard; agent-supervised qPCR that watches amplification curves and halts at the right moment; collision-free robotic-arm/liquid-handler plate handoffs.
- **Carnegie Mellon** — serial dilution dose-response experiments ~3x faster, orchestrating a liquid handler, plate reader, robotic arm, and cameras across three computers with incompatible interfaces.
- **HHMI Janelia** — unified a microscopy rig that previously required seven different vendor programs with no shared interface.
- **QuEra Computing** — agent-built controller recovers a quantum-laser frequency "lock" **99.3% of the time without human intervention**.
- **Tetsuwan Scientific** — qPCR workflow for citizen-science pollution profiling, integrated with its ResearchOS platform.
- Hardware/software vendors reportedly building native MHS support into their equipment (partner list not fully specified in the source); AWS is separately building MHS support into Strands Robots (per source).

## Why it's novel-mechanism significant

- **Extends agentic control from software into physical actuation.** Prior agent-protocol standardization (MCP, A2A) governs software tool-calling and inter-agent messaging; MHS is the first widely-shared standard for an agent to directly operate real-world hardware with safety-limit enforcement built into the device-description layer.
- **Raises the stakes of MCP's security posture.** MHS lists MCP as one of its three control mechanisms — meaning MCP's documented RCE/supply-chain weaknesses (see [[mcp-rce-supply-chain-2026-05]]) now sit upstream of physical-actuator control in labs and factories, not just software state. An MCP-based compromise in an MHS-connected environment has a materially different blast radius (a misdirected robotic arm or laser, not just data exposure).
- **Protocol-governance pattern parallel.** Anthropic's stated path toward open-sourcing MHS mirrors the neutral-governance trajectory of Google's A2A joining the Agentic AI Foundation (see [[google-a2a-agentic-foundation-2026-08]]) — another data point in "which agent protocols become industry standards, and under whose governance."
- **Distinct physical-AI mechanism vs. Prometheus.** Complements rather than overlaps [[prometheus-physical-ai-2026-06]]: Prometheus is agentic *design* of physical systems (jet engines, drug compounds, chips) as a modeling/simulation exercise; MHS is agentic *real-time operation* of already-existing physical hardware. Both are 2026 "physical AI" category entries but at different points in the physical-system lifecycle.

## Anthropic's own candor on limitations

Notably self-disclosed (unusual for a launch post): Claude's physical and spatial reasoning has limitations that MHS's explore-then-compile pattern is partly designed to route around — the agent verifies empirically (camera feedback) rather than relying purely on model-internal physical reasoning before compiling a deterministic script.

## Build-vs-buy signal

- **In-house equivalent** would require building a device-driver abstraction layer, a natural-language-to-machine-readable device-description pipeline, and safety-limit enforcement per device class — nontrivial integration engineering that MHS is explicitly positioned to collapse into a shared standard.
- **Lock-in risk**: low at this stage — MHS is stated to be model-agnostic and multi-protocol (MCP/CLI/API), and Anthropic states an intent to open-source it. Real lock-in risk, if any, would emerge from whichever vendor's *driver ecosystem* (device compatibility breadth) becomes dominant, not from the protocol itself.

## Hype-vs-reality delta

- All capability claims and partner results are Anthropic-published, without independent verification. No pricing, GA date, or broader availability details given — this is a **research preview**, gated to "a first group of scientific research labs and advanced manufacturers."
- No safety-incident or misuse-case discussion in the launch material itself, despite the launch explicitly covering physical-hardware control with error-recovery — a notable gap given this wiki's ongoing safety-incident tracking (see [[agent-safety-incidents-2026-08]]).

## Source

- `raw/research/weekly-2026-09-02/03-anthropic-model-hardware-standard.md` (Anthropic news, "Previewing the Model Hardware Standard," 2026-08-27)

## Related

- [[../llms/anthropic-claude-family|anthropic-claude-family]] — Claude model family; agentic-capability context
- [[prometheus-physical-ai-2026-06]] — parallel physical-AI category, design vs. operation distinction
- [[mcp-rce-supply-chain-2026-05]] — MCP security posture, now extended into physical-actuator blast radius
- [[google-a2a-agentic-foundation-2026-08]] — parallel protocol-governance / open-standard trajectory
- [[aws-bedrock-agentcore-june-2026]] — AWS building native MHS support into Strands Robots
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C17 — MCP-fluency-with-isolation)
