# LangSmith Tuned Evaluators

LangChain vendor blog (2026-08-18/19) announces LangSmith Tuned Evaluators — turnkey, LangChain-managed judge models (starting with "Perceived Error") that auto-attach quality feedback to production agent traces, claimed to exceed frontier-model judge accuracy while cutting evaluation cost up to 82% (98% in some early-partner workloads). The product targets the same problem as [[patterns/sierra-monitor-eval-of-evals]]'s in-house monitor calibration — trustworthy, scalable production LLM-as-judge signal — but via the opposite build-vs-buy axis.

## What "tuned evaluators" are

Not general LLM-as-judge (bring-your-own-prompt, pick-a-frontier-model), but a catalog of finished, versioned, narrowly-scoped judge products. LangChain writes, tests, versions, and maintains the evaluator prompt and manages the judge model, credentials, benchmarking, and inference infrastructure end-to-end; teams just attach the evaluator to a LangSmith tracing project. Positioned explicitly against the "choose accuracy or coverage" tradeoff: frontier-model judges are accurate but too expensive to run on every trace (forcing sampling), while smaller general judges are cheap but low-trust.

## Perceived Error

The first Tuned Evaluator. Detects conversations with evidence an agent erred, misunderstood, or went off-track — explicit evidence (user correction, repeated request, rejected action) or inferred evidence (contradictory responses, acknowledged mistakes, persistent misunderstanding, unresolved outcome). Framed as a proxy for user-perceived quality since most users never leave explicit ratings. Uses a specialized model LangChain post-trained on labeled traces of conversational agents — not a general frontier model prompted as a judge.

**Claimed cost/accuracy advantage (collect-but-confirm):** the post-trained model "outperformed every frontier model in [LangChain's] benchmark" while reducing evaluation cost 82%; some early-partner workloads saw up to 98% cost reduction depending on thread composition. No specific accuracy numbers, benchmark name, or methodology disclosed — vendor-stated, self-benchmarked.

**Mechanics:** eligibility requires ≥2 human-AI message pairs plus reaching a configured idle period; evaluation completes within 12 hours of eligibility. Feedback (result + explanation) attaches to the trace/thread for use in analytics, coding-agent loops, CI, human review, and dataset curation.

**Availability:** live now for LangSmith Plus and Cloud Enterprise plans (US only); per-successful-evaluation billing (skipped/failed not charged). Vanta cited as an early-partner testimonial (qualitative only, no quantitative claim from Vanta itself).

## How this fits the wiki

- [[patterns/sierra-monitor-eval-of-evals]] — closest fit and opposite philosophy. Sierra's Monitors are calibrated in-house by the customer (team-labeled examples + multi-model agreement + rationale surfacing); LangSmith Tuned Evaluators sell the calibration work as a finished, vendor-managed product requiring no customer labeling/tuning. Same problem space, opposite build-vs-buy axis — worth a two-way cross-link from Sierra's page once it's next touched.
- [[patterns/agent-development-lifecycle]] — LangChain's own canonical Build→Test→Deploy→Monitor→Iterate framing names "Monitor" as a lifecycle phase; this is a concrete LangChain product instance of that phase, published ~3.5 months after the lifecycle piece.
- [[patterns/model-cost-routing]] — same vendor, same rhetorical move (large claimed cost reduction — 74% there vs. 82-98% here — via a smaller/specialized model substituting for frontier-model calls on a narrow task), applied to evaluation instead of agent routing rather than case-by-case coincidence.

## Source

- `raw/research/weekly-2026-08-23/04-langsmith-tuned-evaluators.md` — captured 2026-08-23 from `langchain.com/blog/introducing-langsmith-tuned-evaluators-starting-with-perceived-error` (~2026-08-18/19). **Vendor primary.** Cost/accuracy claims self-benchmarked, undisclosed methodology — collect-but-confirm.

## Related

- [[patterns/sierra-monitor-eval-of-evals]]
- [[patterns/agent-development-lifecycle]]
- [[patterns/model-cost-routing]]
