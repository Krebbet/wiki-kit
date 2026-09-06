# Terminal-Universe: trajectory-to-environment reconstruction

Qwen Team/Alibaba arXiv paper (2609.04148, Sep 2026) proposing a pipeline that reconstructs executable terminal environments **from recorded agent trajectories** — rather than from repos or from-scratch generation — then re-queries each reconstructed environment along breadth (cross-workspace) and depth (multi-round) axes to synthesize verifiable SFT training data for terminal/coding agents. Core thesis: environments, not trajectories, are the scarce resource worth scaling. Headline benchmark deltas (+11.9 pts Terminal-Bench 2.1, +13.8 pts EvoCode-Bench v2) were verified against the paper body, not just the abstract.

## Mechanism

Three-stage environment reconstruction:
1. **Deterministic replay** — chronologically replays a trajectory's read/write/edit tool calls to recover each touched file's pre-agent-edit state, yielding a partial workspace. Agent-created files and their edits are withheld and recorded separately for later verification.
2. **Agentic completion** — a completion agent fills in missing files/dependencies without leaking the solution, raising mean file count from 2.9 to 22.4.
3. **Environment filtering** — an agentic judge labels each completed workspace sufficient/insufficient for its recovered task using read-only inspection tools; only sufficient workspaces proceed.

Re-querying then applies four variants: **Intent Recovery** (reconstruct the original task), **Single-WS** (new within-workspace tasks), **Cross-WS** (breadth — TF-IDF nearest-neighbor + LLM-judge dependency mining across workspaces), and **Multi-Round** (depth — a user agent extends solved tasks into up to 6 follow-up rounds with per-round verifier-authored acceptance tests). Every Single-WS/Cross-WS task gets an agent-authored pytest verifier; only trajectories where all tests pass are kept. Multi-Round is filtered at the round level (≥2 verified passing rounds retained). Terminal-Universe explicitly runs a 13-gram contamination check against Terminal-Bench and excludes all Terminal-Bench-derived source trajectories from training data.

## Scale and results (verified against paper body)

From 68,263 raw reconstructed environments, after contamination filtering, dedup, and the sufficiency judge, the paper reports **37,273 ("37.3k") fully sufficient environments** (38,294 Terminal-pool + 1,900 SWE-pool evaluated; sufficiency rates 93.5%/77.1% post-completion). The resulting SFT corpus is 31,977 demonstrations (25,386 Single-WS + 3,512 Cross-WS + 3,079 Multi-Round; ~1.42B training tokens).

Fine-tuning Qwen3.5-27B on the full mixture: **Terminal-Bench 2.1 58.1% vs. 46.2% base = +11.9 points**; Terminal-Bench 2.0 41.6→52.8 (+11.2); **EvoCode-Bench v2 MT@4 6.3→20.1 = +13.8 points**. Ablations: re-solving in reconstructed environments strongly beats imitating source trajectories (52.1 vs 36.7 avg); agentic completion adds +4.2 pts over replay-only; verifier filtering matters more for harder Cross-WS tasks (55.4 vs 53.2) than easier Single-WS (56.4 vs 56.0); under a matched data budget, adding *more environments* beats adding more queries or more solutions per environment/query (56.0 vs 53.8/53.9) — the paper's central empirical support for its "environments are the scarce resource" thesis.

## Reproducibility

No code or dataset release found anywhere in the captured paper — references and acknowledgements checked directly, no "code/data available at..." statement in Discussion, Limitations, or Conclusion. Treat as **not released / undetermined**. This is an internal Alibaba/Qwen Team paper using proprietary Qwen3.7-Max as teacher and Qwen3.5-27B as the trained model, both closed weights as far as the paper states.

## Source

- `raw/research/weekly-2026-09-06/06-06-terminal-universe.md` — arXiv 2609.04148, Qwen Team/Alibaba (Sep 2026). Marker-captured PDF; benchmark and scale figures verified line-by-line against body text and tables (§4.2, §5.2, §6), not trusted from the abstract alone.

## Related

- [[evaluation/swe-cycle]] — both address the gap between benchmark-provided pre-configured environments and real execution friction; Terminal-Universe's environment-reconstruction pipeline is a constructive answer to the problem SWE-Cycle diagnoses.
- [[conflicts/swe-bench-contamination]] — the paper's explicit 13-gram contamination check and Terminal-Bench-derived-trajectory exclusion is a positive contamination-hygiene data point for this open conflict's decontamination discussion.
- [[patterns/agentic-harness-engineering]] — sibling pattern in the "use agents to generate training/evolution data for other agents" family, here targeting environment/task-corpus generation rather than harness rewriting.
- [[evaluation/swe-explore]] — complementary evidence on workspace-state handling: exploration/localization vs. reconstruction.
- [[patterns/externalization-survey]] — the teacher-rollout-then-SFT-distill loop is another concrete instance of the weights↔context externalization arc.
