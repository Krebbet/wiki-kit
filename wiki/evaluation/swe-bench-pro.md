# SWE-bench Pro

SWE-bench Pro is a Scale AI benchmark of 1,865 real-world software engineering tasks sourced from GPL-licensed and private startup codebases, designed to resist data contamination and expose the true capability gap between frontier models and production agentic coding. While top models score 70%+ on the saturated SWE-bench Verified, they achieve only 23–59% on Pro—a gap that reflects the benchmark's substantially harder problem scale (patches averaging 107 lines across 4 files) and contamination-resistant sourcing from private repositories and copyleft open-source projects.

## What's new

- **Contamination-resistant sourcing**: tasks drawn from GPL/copyleft open-source repos and 18 private startup codebases, creating legal and access barriers against inclusion in training corpora.
- **Three-subset architecture**: Public set (731 tasks, GPL repos, public leaderboard), Private set (276 tasks, proprietary codebases, separate leaderboard), and Held-out set (858 tasks, reserved for internal evaluation).
- **Human-augmented problem specification**: unstructured commits and issue metadata refined by professional engineers across three human-in-the-loop checkpoints—environment construction, issue/requirements augmentation, and test verification.
- **Reproducible evaluation**: each task runs in a purpose-built Docker container; a patch resolves only when new fail-to-pass tests pass AND pre-existing pass-to-pass tests still pass (no regressions).

## Performance signal

- **Top-line public-set scores**: gpt-5.4 (xHigh) 59.1%, Muse Spark 55.0%, claude-opus-4-6 (thinking) 51.9%, gemini-3.1-pro (thinking) 46.1%, claude-opus-4-5 45.9%; older/smaller models collapse (GPT-4o-class ~5–16%, Llama/Codestral <12%).
- **Pro vs Verified gap**: top models score 70%+ on Verified but only 23–59% on Pro, rendering Verified scores ineffective for differentiating frontier-model capability in realistic engineering tasks.
- **Private-set penalty confirms generalization gap**: performance drops sharply on proprietary codebases (Claude Opus 4.1 falls from 22.7% → 17.8%; GPT-5 from 23.1% → 14.9%), confirming public-set scores still overstate real-world applicability.
- **Per-language and per-repo heterogeneity**: top models are more consistent across languages and repositories; smaller models show erratic per-repo variance hidden by average resolve rates, a signal for model selection in diverse enterprise codebases.

## Reproducibility

- Public set and eval harness are open-source on GitHub at `scaleapi/SWE-bench_Pro-os`; trajectory viewer hosted on Transluce.
- Private and held-out sets are access-gated; results on the private leaderboard are published but data itself is not released.
- Older leaderboard entries (capped cost, 50-turn limit) are grayed out and separated from the main table to preserve run comparability.
- Paper available at `scale.com/research/swe_bench_pro`.

## Why it matters

- **SWE-bench Verified is effectively saturated**: the benchmark gap is large enough that Verified scores no longer meaningfully differentiate frontier models for coding-agent evaluation purposes.
- **Contamination is a first-class concern**: GPL licensing and private-codebase gating operationalize contamination defense at the dataset-construction level rather than relying on honor-system claims.
- **Patch scale predicts failure**: performance degrades monotonically with lines-changed and files-touched, giving practitioners a concrete predictor of where agents will fail in production (large, multi-file refactors).
- **Top-model consistency vs small-model erraticism**: heterogeneity in per-repo variance has direct implications for model selection and scaffold design for coding agents working across diverse enterprise codebases.

## Source

- `raw/research/weekly-2026-04-22/01-swe-bench-pro.md` (captured 2026-04-22 from https://labs.scale.com/leaderboard/swe_bench_pro_public)

## Related

- [[benchmarks]] — parent eval page; Pro is the next-gen variant.
- [[failure-modes]] — per-language / per-repo resolution patterns surface failure classes and patch-scale degradation curves.
- [[agentic-engineering]] — top-model consistency vs small-model erraticism informs scaffold design.
- [[production-deployments]] — private-codebase subset results are the closest proxy for production conditions.
- [[error-analysis]] — per-language and per-repo breakdowns are ready-made error-analysis artifacts.
- [[topology-taxonomy#long-horizon-context-loss]] — patch-scale degradation and the public-vs-private gap are the empirical anchor of the long-horizon-context-loss synthesis.
- [[agents-md-eval]] — sister benchmark testing the *intervention* side (does adding AGENTS.md help?) where Pro tests the *contamination* side.
- [[airs-bench]] — sister benchmark for autonomous research agents (full scientific pipeline); Pro is the coding-agent peer.
