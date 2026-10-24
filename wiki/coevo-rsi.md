# CoEvo-RSI — Model–Harness Co-Evolution

NUS / A*STAR / SenseTime (arXiv:2610.25078). Meta-agent loop that co-evolves an agent harness and its model, keeping an archive of harnesses *and* checkpoints with "bidirectional historical inheritance". SFT-only (no RL), Qwen3.5-9B base. Frames the problem as *brain–body mismatch* (harness demands behaviours the model hasn't learned, or restricts ones it has) and adds the TIMR diagnostic. Code at github.com/SuJQ0722/CoEvo-RSI (unverified here). Headline wins are narrower than the abstract suggests.

## Method
- TIMR (Turn-level Interface Mismatch Rate): violating turns (unavailable tool calls, interface-contract violations, malformed outputs) / total turns; cheap proxy for one aspect of mismatch.
- Meta-agent (DeepSeek-V4.1-Flash in Codex) over incumbent pair (H_t, θ_t) plus archive of harnesses, checkpoints, histories.
  - Harness inheritance: a Curator writes K hypotheses from archive evidence; K editors each pick any historical base harness (not necessarily parent/latest) and produce offspring.
  - Model inheritance: per offspring harness, pick a checkpoint or TIES-merge archived checkpoints; score by task performance and TIMR.
  - Pair-specific adaptation: rejection-sampled SFT (≤3 samples/task, first verifier-accepted) with harness fixed. Promote best of {incumbent, inherited, adapted} subject to a gain margin; failures archived.
- 10 rounds, K=8, 1-epoch full-parameter SFT (lr 5e-6) on 4×H100. Derives from Meta-Harness, DGM ([[huxley-godel-machine]]), HarnessForge / Co-Harness / WHALE.

## Results
- Failure attribution (held out; Who / When): Who&When Hand 68.39/29.31 (best harness baseline 66.30/25.90; base 37.93/15.52); Algo 62.17/44.71 — *below* best baselines (68.25 Who, 47.62 When); Pro 69.43 Who vs Qwen3.8-Max 65.03; TraceElephant 70.78 Who vs DeepSeek-V4-Pro 56.62 (+14.16).
- "When" accuracy often lags (TraceElephant 28.92 vs GSPO 38.36); GRPO/GSPO under the initial harness beat it on When for Pro and TraceElephant.
- Role-aware text-to-SQL: Spider Safe-EX 80.85, violation rate 1.57% (base 5.72%); BIRD (OOD) Safe-EX 60.15 vs 74.86 best baseline, lowest violation rate (possibly conservative refusal). HomeBench valid multi-device 75.51 vs DeepSeek-V4-Pro 75.10.
- Ablations (Algo): harness-only TIMR >1% in 8/10 rounds; model-only near-zero TIMR but SA ≤35%; latest-only regresses at round 4; full recovers by reusing round-4 weights with new harnesses.

## Caveats
- Abstract's "surpasses DeepSeek-V4-Pro" holds for Who only; some baseline numbers copied from papers; ablations on one benchmark; summary read only through the main results (appendices, cost analysis not reviewed). Paper has its own "RSI or overfit?" section and concedes the pair is task-family-specific.
- Harness-only evolution with a frozen model (e.g. [[memoharness]], [[skillopt]]) accrues interface mismatch per its ablation — a nuance, not a contradiction.

## Source
- raw/research/weekly-2026-10-24/03-coevo-rsi.md (arXiv:2610.25078)

## Related
- [[self-evolving-agent-harness]] — taxonomy; CoEvo-RSI is a co-evolving instance
- [[macaron-v1]] — harness as co-optimised training target
- [[memoharness]] — frozen-model harness optimisation (counterpoint)
- [[skillopt]] — text-space optimisation, frozen model
- [[gepa-reflective-prompt-evolution]] — reflective evolution without weight updates
- [[huxley-godel-machine]] — archive-of-agents lineage
- [[polar-rl-harness]] — RL under a fixed harness
- [[evolution-fine-tuning]] — SFT on own search trajectories
- [[ai-agents-open-ended-research]] — scope caution on RSI
- [[co-cheating-crossfit]] — self-evolving agents on Qwen3.5-4B/9B
