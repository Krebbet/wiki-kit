# Teamknitt: Configurable LLM-Agent Teams

Teamknitt (arXiv 2611.12545, Goran Mitevski, 9 Nov 2026; physics.soc-ph + cs.MA) is a single-author system/idea paper proposing an open reference implementation for configuring, observing and human-intervening in teams of 1-16 LLM agents, using dynamical-systems and human-team theory as the organizing lens. **It reports no comparative results**; treat it as a conceptual framework, not evidence. Abstract-only capture.

## Design (from the abstract)

- **Configuration:** choose one of 14 deterministic routing topologies or a custom directed graph; a "sharing profile" limits what may travel along permitted routes; users bind sources, representations, work dependencies, handoffs and an expertise directory.
- **Observation:** member-level views (reports, behaviour) and system-level views (distributed problem-solving, differentiated transactive memory, interactive coordination, team dynamics).
- **Intervention:** explicit and human-led: reviewed reconfiguration between runs, planned disturbances, private feedback; claims are tracked as queued / applied / understood / improved (an auditability idea).
- **Hypotheses offered:** falsifiable claims on topology, information flow and intervention timing, including whether fractal scaling of inter-member communication output relates to team performance.
- **Code:** reference implementation v0.9.0 stated; URL unconfirmed in the capture. Paper licence CC BY-NC-ND 4.0.

## Wiki fit

- Makes team shape an explicit configuration dimension, whereas [[patterns/harness-design-space]] reports it as fixed in most harnesses; complements the classes in [[patterns/topology-taxonomy]].
- Contrasts with agent-designed topology in [[deployments/anthropic-dynamic-workflows]]: here topology is deterministic and human-configured.
- Its intervention layer targets the governance gap seen in [[security/multi-agent-turf-war]] and [[security/lean-swarm-cheating-whistleblowing]] (no human power to intervene mid-run); observation views could be applied to such failure modes.
- Observe/intervene tooling maps to the Monitor and Iterate phases of [[patterns/agent-development-lifecycle]]; sharing profiles are routing-level information-flow limits akin to [[patterns/agent-communication-protocols]].

## Caveats

Single-author, not peer reviewed, abstract-only capture (the 14 topologies and paper body not read). No threat model or adversarial evaluation.

## Source

- `raw/research/weekly-2026-11-15/04-teamknitt.md` (arXiv 2611.12545)

## Related

- [[patterns/topology-taxonomy]]
- [[patterns/harness-design-space]]
- [[patterns/agent-communication-protocols]]
- [[patterns/agent-development-lifecycle]]
- [[deployments/anthropic-dynamic-workflows]]
- [[security/multi-agent-turf-war]]
- [[security/lean-swarm-cheating-whistleblowing]]
