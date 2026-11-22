# Self-HPO: Harness-Policy Co-Optimization for Coding Agents

Microsoft Research (arXiv 2610.22791; code github.com/MSR-Orchard/Self-HPO, models huggingface.co/self-hpo). Alternates a **harness step** (the current policy analyzes its failures and proposes K=6 harness candidates; best kept) with a **policy step** (GRPO + Balanced Adaptive Rollout, 50 updates under that harness). Tasks never solved become the next search set. Claims joint optimization beats harness-only and policy-only baselines on three SWE benchmarks. Authors' own runs; collect-but-confirm.

## Setup and results

- Qwen3.5-35B-A3B, seed harness mini-SWE-agent, 2,484 Python training tasks, two rounds.
- avg@3 (SWE-Verified / Multilingual / Pro): base 61.0 / 54.2 / 58.3 (avg 57.8) → Self-HPO 69.5 / 59.7 / 65.2 (avg 64.8). RLVR (policy-only) avg 61.9; Self-Harness (harness-only) 60.1. Gains transfer out-of-distribution despite Python-only training.
- With Opus 4.8 as external harness proposer: 71.6 on Verified (avg 66.3) vs Meta-Harness 69.1. SFT distillation from Opus trajectories falls *below* base OOD (avg 54.6).
- Ablations (Verified, ref 71.6): SFT in P-step −4.4, RFT −1.1, fixed search set −1.5, self-proposer −2.1.
- **Complementarity:** harness alone +3.5, policy alone +3.4, together +8.5 (1.6 above additive).
- Gains concentrate on Easy/Medium tasks; −2.2 on already-resolved tasks; zero-success GRPO groups fall to 6.5% (vs 11–17% for RLVR).
- **What evolved:** mostly runtime wrapper logic — budget-valve warnings, empty-patch guard, a pre-submission grounding pause, patch-apply fallback — largely submission-hygiene fixes.

## Caveats

One base model and one seed harness; Python-only training; std devs ~0.5–1.9 (some gaps within noise); two rounds; fixes may be partly SWE-format specific.

## Source

- `raw/research/weekly-2026-11-22/04-harness-policy-optimization.md` — arxiv.org/pdf/2610.22791 (marker, captured 2026-11-22).

## Related

- [[patterns/harness-self-evolution-survey]] — Self-HPO breaks the survey's weight-fixed scope
- [[patterns/agentic-harness-engineering]] — harness-only evolution (Terminal-Bench)
- [[patterns/autodesign-meta-harness]] · [[patterns/moss-production-self-evolution]] — other harness-rewrite systems
- [[patterns/skillos]] — opposite split (trains curator, frozen executor)
- [[patterns/sdar]] — policy-side RL for multi-turn agents
- [[patterns/externalization-survey]] — supports complementarity of harness and weights
- [[evaluation/continualskillbench]] — mild tension: agent-driven maintenance ≈ plain ICL there (different artifact)
- [[patterns/topology-taxonomy]]
