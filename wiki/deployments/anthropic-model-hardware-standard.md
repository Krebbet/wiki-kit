# Anthropic — Model Hardware Standard (MHS)

Anthropic's 2026-09-06 research-preview announcement of the Model Hardware Standard (MHS): a shared driver/discovery specification letting AI agents safely operate physical lab and manufacturing instruments — microscopes, liquid handlers, robotic arms, lasers — developed with HHMI Janelia and piloted across biotech, robotics, and quantum-computing partners. This is the wiki's **first source on physical-world/embodied agent tooling**; no existing page covers robotics, lab automation, or physical-actuator safety, so it likely seeds a new cluster rather than folding into an existing one.

## What the standard specifies

MHS is a standardized **driver layer**, not an agent framework in itself. It:
1. Exposes a simple read/write primitive set that any programmable device can implement.
2. Makes devices network-discoverable in a standard format.
3. Auto-generates a natural-language-derived reference file per device (capabilities, adjustable parameters, safety limits) from user/agent-authored tags — replacing tacit knowledge and paper manuals.

Agents then control hardware via three mechanisms: **MCP, CLI, or code files (APIs)**, letting an agent reason step-by-step online or compile a learned sequence into a deterministic script/code file for fast, long-running execution without per-step reasoning. Domain is explicitly physical instruments across science, robotics, electronics, and manufacturing — lab benches and factory floors, not general software tools.

## Pilot evidence (vendor/partner-reported, collect-but-confirm)

Six named partner writeups, no independent benchmark methodology disclosed:
- **Genentech** — BCA protein-assay proof-of-concept across a liquid handler, robotic arm, and plate reader.
- **UW Baker/Pinglay labs** — qPCR agent-supervision with collision-free robotic-arm/liquid-handler handoff.
- **CMU** — serial-dilution dose-response experiments across 3 computers with incompatible interfaces run **~3x faster**.
- **HHMI Janelia** — unified a 7-vendor-program microscopy rig.
- **QuEra** — **99.3% autonomous laser-lock recovery** in a quantum computer, no human intervention.
- **Tetsuwan** — qPCR citizen-science pollution monitoring.

Additional hardware/software vendors building MHS support: AWS (Strands Robots), Automata (LINQ), Danaher, Doosan Robotics, MBF Bioscience (ScanImage), QIAGEN, Tecan, Universal Robots, Hugging Face (LeRobot), Raspberry Pi (Camera MHS Driver).

## Self-flagged limitations

Anthropic names its own gaps: Claude's physical/spatial reasoning is limited (text/image-only grounding) and still needs expert oversight — in the Genentech pilot, the agent needed guidance to recognize sample foaming as a physical, not software, failure. MHS doesn't yet work with hardware lacking any programmable interface. The standard is pre-open-source and invite/waitlist-gated as a research preview. A "physical safety roadmap" is explicitly still being developed, not shipped.

## Relationship to MCP

MHS names MCP as one of its three control mechanisms and is described as model-agnostic, accessible by "any agent harness ... using standard protocols, such as [MCP]." It is a **sibling protocol that layers alongside MCP**, not a competitor: MHS standardizes physical-device discovery and safety semantics — actuator safety limits, device manipulation metadata, hardware fault recovery — a layer MCP does not address. [[deployments/mcp-infrastructure]] covers auth, context bloat, governance, and audit trails for *software* tool ecosystems; MHS extends the same "agents discovering and safely operating external systems" theme to physical hardware. MHS's not-yet-open-source status, plus a planned safety-eval program, echoes the AAIF open-standards trajectory MCP already went through (see [[governance/aaif]]) — though no open-sourcing commitment or AAIF involvement is stated yet, so this parallel is speculative.

## Source

- `raw/research/weekly-2026-09-06/04-04-anthropic-model-hardware-standard.md` — Anthropic, "Previewing the Model Hardware Standard" (anthropic.com/news, 2026-09-06). Vendor primary.

## Related

- [[deployments/mcp-infrastructure]] — sibling standardization effort; MHS extends the agent-external-system-operation boundary from software tools to physical/actuated hardware.
- [[governance/aaif]] — MCP's own open-standards trajectory; a speculative parallel for MHS's stated (but not yet committed) open-sourcing intent.
