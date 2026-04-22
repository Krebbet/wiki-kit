---
source: "raw/research/radar-2026-04/02-huxley-godel.md"
slug: "02-huxley-godel"
summarized_on: "2026-04-22"
schema_version: 1
---

# Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine

## One-line
KAUST/Schmidhuber-group paper (arXiv 2510.21614) proposes Huxley-Gödel Machine (HGM), a tree-search self-improving coding agent that scores parents by aggregated descendant ("clade") performance instead of own benchmark score, claims to approximate the Gödel Machine under stated assumptions, and reaches human-level results on SWE-bench Lite.

<!-- DOMAIN-SLOT: takeaway-prompts -->
## Method
Self-improvement is formalized as iterative tree search over an archive of self-modified coding agents. The compound policy is split into three sub-policies: (i) selection (expand vs. evaluate), (ii) expansion (which parent to modify), (iii) evaluation (which agent to test). The key novelty is the expansion criterion: instead of using an agent's own benchmark score (as in Darwin Gödel Machine [DGM, Zhang et al. 2025] and Self-Improving Coding Agent [SICA, Robeyns et al. 2025]), HGM estimates Clade-Metaproductivity (CMP), defined as the aggregated success/failure counts over the entire subtree (clade) rooted at an agent: `CMP_hat(a) = n_success_C(a) / (n_success_C(a) + n_failure_C(a))`. Theorem 1 shows that under Assumption 1 (final-agent-only utility, repeatable trials, proofs free, unit-cost modifications), access to a true CMP oracle suffices to implement the Gödel Machine. Expansion and evaluation each draw an agent via Thompson Sampling over Beta posteriors with a monotonically increasing exploration scheduler τ; selection between expand/evaluate uses a UCB-Air-style rule (expand when `N_t^α >= |T_t|`, α=0.6). Evaluation is decoupled from expansion at the granularity of single agent–task pairs, enabling early stopping and asynchronous parallel execution (HGM-Async). Final agent picked via the ε-percentile of the Beta posterior (regularized incomplete beta function). Builds on Schmidhuber's Gödel Machine (2003), Success-Story Algorithm, infinite-armed bandits (UCB-Air, Wang et al. 2008), and Thompson sampling (Agrawal & Goyal 2012).

## Results
- **CMP estimator quality (Table 1, Pearson correlation with empirical CMP):** HGM weighted 0.778 vs. SICA 0.444, DGM 0.285 on SWE-Verified-60; HGM 0.626 vs. SICA 0.274, DGM 0.383 on Polyglot.
- **Self-improvement (Table 2, 800 evaluations, GPT-5/GPT-5-mini for SWE, Qwen3-Coder-480B/30B for Polyglot, initial agent at 40%/20.3%):** HGM 56.7% (+16.7) vs. DGM 53.3 (+13.3) vs. SICA 50.0 (+10) on SWE-Verified-60; HGM 30.5% (+10.2) vs. DGM 27.1 (+6.8) vs. SICA 25.4 (+5.1) on Polyglot.
- **Wall-clock:** HGM 517h vs. DGM 1231h on SWE-Verified-60 (2.38× faster); HGM 347h vs. DGM 2385h (6.86×) and SICA 572h (1.65×) on Polyglot.
- **Scaling to full SWE-bench Verified (8000 evals, stronger initial 53.2%):** HGM-discovered agent reaches 61.4%, top GPT-5-mini agent on the leaderboard, top-10 overall (competitive with Claude-3.7 systems costing ~5× more).
- **Generalization to SWE-bench Lite (Table 3):** HGM agent 40.1% filtered / 49.0% standard vs. SWE-agent+GPT-5-mini 39.6 / 47.6 vs. initial ancestor 34.8 / 44.0; second place on SWE-Lite leaderboard among checked submissions.
- **Backbone transfer to GPT-5 (Table 4):** HGM agent + GPT-5 reaches 47.8% filtered / 57.0% standard, on par with the SWE-agent leaderboard leader (48.3 / 56.7) — only 1 task behind on filtered.

## Applicability
Targets teams doing *agent design / scaffolding optimization*, not model training. Prerequisites: (1) a coding-agent harness whose source the agent can edit (DGM-style or SICA-style); (2) substantial LLM API budget — runs use 800–8000 task evaluations × GPT-5/GPT-5-mini calls, hundreds of CPU-hours; (3) a benchmark with cheap, repeatable, binary-graded trials (SWE-bench, Polyglot); (4) parallel CPU infrastructure to exploit HGM-Async. No model weights needed — works with any frontier API LLM as the backbone. Directly relevant to anyone running DGM/SICA-style loops; the CMP weighting is a drop-in replacement for the parent-selection heuristic.

## Novelty
Refinement / recombination, not a fundamentally new paradigm. The novelty is the *selection metric* (clade-aggregated success rate) and the formal claim that this approximates the Gödel Machine under Assumption 1. The tree-search scaffolding (DGM, SICA), Thompson sampling, UCB-Air, and the Gödel Machine itself are all prior work. The closest prior work is Darwin Gödel Machine (Zhang et al. 2025a, arXiv 2505.22954) and SICA (Robeyns et al. 2025, arXiv 2504.15228); HGM differs by replacing greedy benchmark-score parent selection with descendant-aggregated CMP and decoupling evaluation from expansion for asynchronous execution. Conceptual debt to Huxley's clade notion (1957) and Good's intelligence-explosion speculation (1966).

## Reproducibility
Code released: `https://github.com/metauto-ai/HGM` (stated in abstract). Initial agent adopted from official DGM implementation. Algorithm fully specified (Algorithm 1 in Appendix B). Hyperparameters disclosed (ε=1, α=0.6, scheduler τ = B/b). Benchmarks are public (SWE-bench Verified, SWE-bench Lite, Polyglot). No released agent weights since the artifact is an agent scaffold, not a model. No paperswithcode entry verified from the source. Reproduction cost is non-trivial due to the LLM API budget required.

## Adoption
Too early to gauge. The paper engages directly with two recent self-improving-agent works (DGM, SICA, both 2025) and claims top-10 on SWE-bench Verified plus second place on SWE-bench Lite leaderboards (as of late October 2025). KAUST + Schmidhuber lab gives it visibility. No citation count or independent reproduction visible from the source itself.

## Conflicts
Implicitly contests the DGM/SICA premise that "higher benchmark score implies higher self-improvement potential" — the paper coins this the *Metaproductivity-Performance Mismatch* and shows weak Pearson correlations (0.27–0.44) for the baselines' selection metric. No direct contradiction with anything currently in the wiki (wiki has only `reference-sources`); flag for `wiki/conflicts/` is not warranted yet but should be revisited once DGM or SICA pages exist.
<!-- /DOMAIN-SLOT -->

## Cross-ref candidates
- [[darwin-godel-machine]] — direct baseline; HGM replaces DGM's greedy selection metric and beats it on SWE-Verified-60 (+3.4%) and Polyglot (+3.4%) with 2.4–6.9× less CPU. (Page does not yet exist.)
- [[self-improving-coding-agent]] — second baseline (SICA); HGM beats it and runs reliably where SICA hit context-window failures. (Page does not yet exist.)
- [[godel-machine]] — theoretical anchor (Schmidhuber 2003); HGM claims to approximate it under Assumption 1. (Page does not yet exist.)
- [[swe-bench]] — primary evaluation benchmark (Verified + Lite). (Page does not yet exist.)
- [[thompson-sampling-for-llm-agents]] — HGM's expansion/evaluation policy is Thompson sampling over Beta posteriors with a temperature scheduler. (Page does not yet exist.)
- [[mcts-for-agent-search]] — paper situates HGM relative to UCT/MCTS and infinite-armed bandits (UCB-Air). (Page does not yet exist.)
- [[self-improving-agents]] — natural umbrella page covering Schmidhuber's lineage (SSA, Fitness-Monotonic Execution, Gödel Machine, DGM, SICA, HGM). (Page does not yet exist.)

## Conflict flags
(none) — wiki currently contains no claims this source could contradict.

## Proposed page shape
- New page: `huxley-godel-machine` — dedicated page summarizing CMP, the MPM observation, the algorithm, and the SWE-bench results.
- New page: `self-improving-agents` (umbrella) — situate HGM alongside Gödel Machine, DGM, SICA, Gödel Agent, STOP; tag with the open question "does clade-metric self-improvement generalize beyond coding-agent scaffolding?"
- New page: `metaproductivity-performance-mismatch` (concept page) — short, references the empirical correlations table; useful as a citation target for future selection-metric discussions.
- Stub pages worth seeding for cross-ref hygiene: `darwin-godel-machine`, `self-improving-coding-agent`, `godel-machine`, `swe-bench`.
