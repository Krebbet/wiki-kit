# OpenAI: How Agents Are Transforming Work

Internal Codex adoption data from OpenAI documenting the transition from AI-assisted work to agent-dominant workflows across all departments, including non-technical ones. Published June 26, 2026 alongside an accompanying economic analysis.

## Key Claims

- **Codex now accounts for 99.8% of OpenAI's weekly output tokens** (mid-2026), up from under 10% through August 2025 — a near-complete platform switch in under a year.
- **Non-developer adoption dwarfs developer adoption**: individual non-developer Codex users grew 137×, organizational non-developer users grew 189×, internal OpenAI non-developers 12× since August 2025.
- **Task horizon is shifting toward long-delegation**: 80.6% of sampled individual users made at least one request estimated to exceed 30 minutes of human work; 70.2% exceeded one hour; 25.6% exceeded eight hours.
- **Power users run parallel agent orchestration at scale**: 99th-percentile users generated >60 cumulative agent-hours per day across multiple parallel agents by June 2026.
- **Cross-functional task bleed is documented**: over one-fourth of Codex work by non-engineering departments (Legal, Finance, Recruiting) was classified as engineering or coding tasks — agents lower the cost of crossing task-type boundaries.

## Adoption Timeline (Internal OpenAI)

By April 2026, Legal, Finance, and Recruiting had each crossed over to Codex as their primary AI tool. Intensity growth June 2026 vs. November 2025:
- Research: 56×
- Customer Support: 32×
- Engineering: 27×
- Legal: 13×

Average lawyer and recruiter generates >85% of output tokens on Codex as of mid-2026.

## Methodology Caveats

- Task horizon is estimated via LLM-as-judge on Codex transcripts; thresholds are directional, not independently validated.
- Individual-level data comes from a 0.1% random sample — numbers are directional rather than census-level.
- Internal OpenAI data reflects an unusually early-adopter environment; external generalization is uncertain.

## Comparison to Peer Studies

This is the largest-scale internal observational study on agent adoption to date. The [[anthropic-internal-study]] (132-engineer study, May 2026) captured the engineer-role-shift thesis at smaller scale; OpenAI's data extends the scope to non-technical departments and quantifies task-horizon distribution at population scale. The adoption inflection point (August 2025) is consistent with Willison's November 2025 "wiped out by 11am" account ([[case-studies/willison-cognitive-cost]]) — the transition happened slightly earlier at OpenAI than in the broader community.

## Source

- Raw: `raw/research/weekly-2026-06-28/01-openai-agents-transforming-work.md`
- Primary URL: https://openai.com/index/how-agents-are-transforming-work/
- Captured: 2026-06-28

## Related

- [[anthropic-internal-study]] — 132-engineer Claude adoption study; engineer-as-orchestrator shift at smaller scale
- [[case-studies/willison-cognitive-cost]] — practitioner account of the same transition
- [[deployments/cognition-cloud-agents]] — Devin/Cognition; comparable cloud coding agent deployment
- [[deployments/microsoft-agent-365]] — cross-functional non-engineering agent deployment (governance angle)
- [[patterns/topology-taxonomy]] — power-user parallel-agent pattern is a fan-out topology instantiation
- [[patterns/agent-development-lifecycle]] — Build→Test→Deploy→Monitor cycle reflected in department-by-department adoption curve
