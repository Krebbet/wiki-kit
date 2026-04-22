# Escalation vs Approval

A **design lever** surfaced by the Stanford 51-deployment playbook (2026-03). Given a deployment where AI cannot handle 100% of cases, the choice between:

- **Approval model** — AI proposes, human approves every output before it takes effect.
- **Escalation model** — AI acts autonomously on most cases; human reviews *exceptions* flagged by the system.

has an outsized effect on realized value. Stanford's finding: the escalation model produces **71% median productivity gains** vs **30% for approval-gated** across their 51 mature deployments — a >2× gap.

*(Evidence class: academic-synthesis survey result, published March 2026. Single-study finding; not independently replicated at time of capture.)*

## Why the escalation model wins in the data

From the Stanford synthesis:

- **Throughput.** Approval gates each case on a human's attention; escalation gates only the exceptions. Volume × decision-latency compounds.
- **Human attention on the hard cases.** Reviewers see only flagged exceptions, applying judgment where it matters rather than rubber-stamping routine.
- **AI improvement loop works better.** With approval, human edits happen silently pre-deployment; with escalation, exceptions surface as training signal.
- **Signals scale with volume.** Exception review naturally produces a labelled dataset of edge cases.

## Preconditions for choosing escalation safely

Stanford's sample is success-weighted. The escalation model is not unconditionally safe. Preconditions visible in the deployments that made it work:

- **Reliable exception detection.** The system must identify its own low-confidence cases. Uncertainty-aware routing (see [[slm-agents#architecture-slm-default-llm-fallback]]) is the technical underpinning.
- **Exception-review capacity.** Sufficient reviewer staffing to absorb the exception volume. This is where [[klarna|Klarna's architecture]] held up but the *capacity plan* failed.
- **Low cost of occasional fast errors.** Some verticals (financial-services disputes, medical diagnosis) have asymmetric cost structures where one high-stakes mistake outweighs many routine wins. Approval may be forced there.
- **Regulatory headroom.** Approval may be legally required in specific regulated flows regardless of productivity math.

## When approval is the right call

- Regulatory or compliance mandate requires a human in the loop per decision.
- The cost distribution of errors is heavy-tailed (one mistake is catastrophic).
- AI confidence calibration is unreliable or unknown — you cannot distinguish exceptions from non-exceptions.
- Early rollout phase where the AI is still learning the problem shape. Start with approval; move to escalation once error-rate and exception-detection are well-characterized.

## The Klarna cautionary tale

[[klarna|Klarna]] used an escalation-like architecture (AI autonomous, hand-off to humans on complexity) but cut human capacity below the level needed to absorb the AI's residual failures. Result: AI failures in dispute-resolution and account-access became customer-visible because there weren't enough humans to escalate to.

**Escalation as architecture ≠ escalation as sufficiency.** Capacity planning is a first-class concern.

## Wiki-lever mapping

- Complements [[slm-agents]] (technical routing) with the *organizational* routing layer.
- Complements [[measurement-vs-architecture]] — the escalation-vs-approval choice is itself measurable.
- Implied by [[failure-modes#metric-masked-quality-degradation]] — escalation capacity planning is part of what the Klarna metrics missed.

## Source

- `raw/research/production-slm-case-studies/06-stanford-enterprise-ai-playbook-51.md` — Stanford 51-deployment playbook (primary source for the quantitative claim).
- `raw/research/production-slm-case-studies/02-promptlayer-klarna-human-hybrid.md` — Klarna correction (cautionary counter-example).

## Related

- [[stanford-51-enterprise-playbook]]
- [[klarna]]
- [[slm-agents]]
- [[measurement-vs-architecture]]
- [[failure-modes]]
