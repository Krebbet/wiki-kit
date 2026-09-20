# SoL-Pi: RSI-Inspired Auto-Research for Harness Token Efficiency

arXiv paper (2609.20519, submitted 2026-09-17, NVIDIA-affiliated per capture metadata) introducing SoL-Pi: a recursive-self-improvement-inspired auto-research system that searched ~152 proposed directions across ~535 executable environments to discover four reusable harness-level mechanisms — Action Fusion, Online Context Compact, ObservationPack, and Evidence-Preserving Reducer — that together cut recorded coding-agent token traffic 44.7–49.0% and API cost by about a third, at 93.7–94.3% of baseline task score, with no model training required and demonstrated zero-shot transfer across backends.

## The four mechanisms

All four are implemented as open extensions to the Pi harness (github.com/earendil-works/pi, formerly pi-mono), which also serves as the primary baseline throughout:

- **Action Fusion** (action execution) — the baseline harness issues a file-edit tool call, then a separate follow-up command (test/build/run) in the next turn. Action Fusion extends file-mutation tools with an optional follow-up-command field so both execute together and return a single observation, eliminating a model round trip. Commands whose choice depends on inspecting the mutation result stay separate. Prompt-only triggering proved unreliable in development, so the team exposed the fused action directly in the tool schema instead.
- **Online Context Compact** (context management) — at each plan-step completion boundary, the harness estimates remaining model requests from observed request rate and unfinished-step count, then runs a cost gate comparing projected input-token savings from compacting against the estimated cost of rewriting the prompt cache (using cache-write/cache-read price ratio). Later compactions require a larger margin to account for unrecovered prior rewrite costs.
- **ObservationPack** (observation handling) — tool outputs ≥10 KiB are archived locally and sent in full for the next two provider requests only; from the third request on, the harness substitutes a stable handle, size, and a short head/tail excerpt, with the agent able to page back to full content via the handle. It recognizes Evidence-Preserving Reducer's receipt marker and skips those results to avoid double-processing.
- **Evidence-Preserving Reducer** (delegated reading) — for build/test logs ≥4 KiB from a predefined command set, the harness archives the exact output and delegates extraction to a cheaper auxiliary model (GPT-5.6 Luna, high effort) into a compact "receipt." A deterministic verifier checks schema, source hash, exit status, exact quotes, and size; on failure, suspected credentials, or no size reduction, it falls back to the full log. The auxiliary model only extracts evidence — the main agent retains all diagnosis/action-selection responsibility.

The four mechanisms target complementary overhead sources: edit+verify round trips, plan-boundary context bloat, repeated large-observation resends, and verbose log re-reading. Capability tolerances and efficiency metrics were fixed before the search began and held out of the optimizing agent's control to prevent gaming.

## Results

On the 51-task public EdgeBench split (held out from search): the full 4-mechanism stack uses 1.10B total tokens — 49.0% fewer than the Pi baseline — while retaining 93.7% of baseline average score (42.0 vs. 44.8), at 33.2% lower token cost. A single-best-mechanism-per-backend variant (ObservationPack alone under GPT-5.6 Sol, Action Fusion alone under Opus 5) instead *raises* average score 44.8→47.2 (+5.3%) while still cutting token traffic 6.1%.

**Zero-shot transfer**: the harness, developed and searched only on GPT-5.6 Sol trajectories, transfers to Opus 5 with no re-search — retaining 94.3% of baseline score while cutting token traffic 44.7% and API cost 33.5%. Stated dollar framing: estimated hourly savings of $8.75–$13.50 vs. native Codex/Claude Code harnesses, $4.36–$5.71 vs. Pi (2026-08-17 API prices).

Further evaluations: on Terminal-Bench 4 (63 CPU-only tasks), SoL-Pi solves fewer tasks than Codex/Pi (15 vs. 18) but at 26.3% lower total model cost and 11.6% lower cost-per-solved-task. On IMO 2026 formal proofs (GPT-5.6 Sol xhigh, Lean 4-verified), SoL-Pi passes 3/6 problems at the lowest cost-per-passed-problem of the three harnesses compared. In a 20-worker kernel-optimization swarm, the SoL-Pi-worker configuration is 26.8% cheaper than the Pi-baseline-worker swarm and is one of two configurations (with a single non-swarm Codex agent) to pass all 8 official speed thresholds.

Search scale: ~152 proposed directions across six proposal families (context, progress, tools, delegation, prompt/policy, improvement-and-evaluation); 535 executable search environments (495 GitHub issue–PR repository tasks + 40 synthetic Terminal-Bench-2-style verifier tasks); >3,000 runs; >60,000 agent–environment interactions.

## Reproducibility

All four mechanisms are open extensions to the existing Pi harness. The captured full text does not itself surface a dedicated SoL-Pi code-release repository — treat "code released" as unconfirmed pending a direct check. EdgeBench is partially open (51 of 134 tasks public); Terminal-Bench 4, the IMO 2026 formal-statement sets, and the kernel-optimization benchmark are all cited with links in the paper's references.

## Related

- [[patterns/agentic-harness-engineering]] — parallel observability/trajectory-feedback-driven harness-evolution system; AHE is cited in SoL-Pi's related work as a peer method with cross-task/cross-model transfer evaluation, while SoL-Pi runs a much larger-scale search targeting token efficiency specifically rather than capability lift.
- [[patterns/autodesign-meta-harness]] — parallel recursive harness-rewriting-from-rollout-feedback approach; SoL-Pi differentiates with an explicit broad-to-deep funnel plus independent held-out validation, designed to avoid the overfitting failure mode a cited critique paper found in prior evolved-harness work.
- [[patterns/anthropic-context-engineering]] — direct mechanism overlap: Anthropic's JIT-retrieval + compaction + structured-note-taking triad maps onto ObservationPack and Online Context Compact; SoL-Pi adds a quantified, auto-discovered cache-rewrite-cost gate that Anthropic's framing states only qualitatively.
- [[patterns/self-gc-context]] — parallel lifecycle/archival context-management mechanism (fold/mask/prune-with-sidecar-recovery), gated here by an explicit token-savings-vs-cache-rewrite-cost economic model rather than an indexed-object lifecycle.
- [[patterns/direct-corpus-interaction]] — ObservationPack's "stable handle + excerpt now, full content on demand" scheme shares DCI's core move of avoiding persistent full-content storage in context, applied to tool observations rather than document corpora.
- [[patterns/claude-platform-cost-optimization]] — same cost-efficiency goal via a different mechanism: Anthropic's levers operate within one vendor's harness via a skill, while SoL-Pi discovers cross-cutting mechanisms via automated search with demonstrated cross-backend transfer.
- [[patterns/model-cost-routing]] — orthogonal cost lever (routing to cheaper models vs. fixed-model harness-level token reduction), though Evidence-Preserving Reducer's delegation to a cheaper auxiliary model echoes routing at a narrow scale.
- [[evaluation/continualskillbench]] — that page's skepticism toward self-improving-agent narratives is the type of overfitting/no-real-transfer critique SoL-Pi's held-out validation is explicitly designed to rebut.
- [[patterns/harness-design-space]] — SoL-Pi's four mechanisms are concrete, quantified instances of that survey's design dimensions (context, tools/observation handling), discovered via automated search rather than manual census.

## Source

- `raw/research/weekly-2026-09-20/02-sol-pi-harness-efficiency.md` — captured 2026-09-20 from arXiv:2609.20519 (full text via HTML capture; the initial PDF capture only surfaced the abstract landing page and was re-captured). Author byline not present in the captured text; NVIDIA affiliation per capture metadata, collect-but-confirm.
