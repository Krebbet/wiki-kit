# Huxley-Gödel Machine

KAUST/Schmidhuber-group paper (arXiv:2510.21614) proposing **HGM**, a tree-search self-improving coding agent that scores parents by aggregated descendant ("clade") performance instead of own benchmark score, claims to approximate the Gödel Machine under stated assumptions, and reaches human-level results on SWE-bench Lite.

## Method

Self-improvement formalized as iterative tree search over an archive of self-modified coding agents. The compound policy splits into three sub-policies: (i) selection (expand vs evaluate), (ii) expansion (which parent to modify), (iii) evaluation (which agent to test).

Key novelty is the **expansion criterion**. Instead of using an agent's own benchmark score (as in Darwin Gödel Machine [DGM, Zhang et al. 2025] and Self-Improving Coding Agent [SICA, Robeyns et al. 2025]), HGM estimates **Clade-Metaproductivity (CMP)**:

```
CMP_hat(a) = n_success_C(a) / (n_success_C(a) + n_failure_C(a))
```

Aggregated success/failure counts over the entire subtree (clade) rooted at an agent.

**Theorem 1**: under Assumption 1 (final-agent-only utility, repeatable trials, proofs free, unit-cost modifications), access to a true CMP oracle suffices to implement the Gödel Machine.

Expansion and evaluation each draw an agent via Thompson Sampling over Beta posteriors with a monotonically increasing exploration scheduler τ. Selection between expand/evaluate uses a UCB-Air-style rule (`expand when N_t^α >= |T_t|`, α=0.6). Evaluation is **decoupled** from expansion at the granularity of single agent–task pairs, enabling early stopping and asynchronous parallel execution (HGM-Async). Final agent picked via the ε-percentile of the Beta posterior.

Builds on Schmidhuber's Gödel Machine (2003), Success-Story Algorithm, infinite-armed bandits (UCB-Air, Wang 2008), Thompson sampling (Agrawal & Goyal 2012).

## Results

- **CMP estimator quality (Table 1, Pearson correlation with empirical CMP):** HGM weighted **0.778** vs SICA 0.444, DGM 0.285 on SWE-Verified-60; HGM **0.626** vs SICA 0.274, DGM 0.383 on Polyglot. This is the empirical hook for the **Metaproductivity-Performance Mismatch (MPM)** observation.
- **Self-improvement (Table 2; 800 evaluations; GPT-5/GPT-5-mini for SWE, Qwen3-Coder-480B/30B for Polyglot; initial agent at 40%/20.3%):**
  - SWE-Verified-60: HGM **56.7%** (+16.7) vs DGM 53.3 (+13.3) vs SICA 50.0 (+10).
  - Polyglot: HGM **30.5%** (+10.2) vs DGM 27.1 (+6.8) vs SICA 25.4 (+5.1).
- **Wall-clock:** HGM 517h vs DGM 1231h on SWE-Verified-60 (**2.38× faster**); HGM 347h vs DGM 2385h (**6.86×**) and SICA 572h (**1.65×**) on Polyglot.
- **Scaling to full SWE-bench Verified (8000 evals; stronger initial 53.2%):** HGM-discovered agent reaches **61.4%**, top GPT-5-mini agent on the leaderboard, top-10 overall (competitive with Claude-3.7 systems costing ~5× more).
- **Generalization to SWE-bench Lite (Table 3):** HGM agent **40.1%** filtered / **49.0%** standard vs SWE-agent+GPT-5-mini 39.6 / 47.6. Second place on SWE-Lite leaderboard among checked submissions.
- **Backbone transfer to GPT-5 (Table 4):** HGM agent + GPT-5 reaches **47.8%** filtered / **57.0%** standard, on par with the SWE-agent leaderboard leader (48.3 / 56.7) — only 1 task behind.

## Applicability

Targets teams doing *agent design / scaffolding optimization*, not model training.

Prerequisites:
1. A coding-agent harness whose source the agent can edit (DGM-style or SICA-style).
2. Substantial LLM API budget — runs use 800–8000 task evaluations × GPT-5/GPT-5-mini calls, hundreds of CPU-hours.
3. A benchmark with cheap, repeatable, binary-graded trials (SWE-bench, Polyglot).
4. Parallel CPU infrastructure to exploit HGM-Async.

No model weights needed — works with any frontier API LLM as the backbone. The CMP weighting is a **drop-in replacement for the parent-selection heuristic** in DGM/SICA-style loops.

## Novelty

Refinement / recombination, not a fundamentally new paradigm. The novelty is the *selection metric* (clade-aggregated success rate) and the formal claim that this approximates the Gödel Machine under Assumption 1. Tree-search scaffolding (DGM, SICA), Thompson sampling, UCB-Air, and the Gödel Machine itself are all prior work.

Closest prior: DGM (Zhang 2025a, arXiv:2505.22954) and SICA (Robeyns 2025, arXiv:2504.15228). HGM differs by replacing greedy benchmark-score parent selection with descendant-aggregated CMP, and decoupling evaluation from expansion for asynchronous execution. Conceptual debt to Huxley's clade notion (1957) and Good's intelligence-explosion speculation (1966).

## Reproducibility

Code released: <https://github.com/metauto-ai/HGM>. Initial agent adopted from official DGM implementation. Algorithm fully specified (Algorithm 1, Appendix B). Hyperparameters disclosed (ε=1, α=0.6, scheduler τ = B/b). Benchmarks public. No released agent weights since the artifact is a scaffold, not a model. Reproduction cost is non-trivial due to LLM API budget required.

## Adoption

KAUST + Schmidhuber lab gives visibility. Engages directly with two recent self-improving-agent works (DGM, SICA, both 2025) and claims top-10 on SWE-bench Verified plus second place on SWE-bench Lite leaderboards (late October 2025). No citation count or independent reproduction visible in the source.

## Source

- `raw/research/radar-2026-04/02-huxley-godel.md` — HGM paper PDF (arXiv:2510.21614). Captured 2026-04-22.

## Related

- [[watchlist]] — DGM, SICA, Gödel Machine, SWE-bench, Thompson sampling references not captured.
