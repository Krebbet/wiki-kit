# Beyond the Best Guess: Improving LLM Solution Coverage with Evolution Strategies

Cognizant AI Lab (Hayes, Meyerson, Qiu, Miikkulainen et al., arXiv:2608.12679, Aug 2026). The most comprehensive scale/family sweep of Evolution Strategies (ES) vs. RL/GRPO post-training to date on solution coverage: ES beats GRPO on pass@k across Qwen2.5-Instruct and Qwen3 models from **1.5B to 32B**, while matching or exceeding RL on pass@1. RL narrows the output distribution around high-reward answers ("distribution collapse"); ES broadens it.

## Method

ES: population-based, gradient-free weight-space optimization (Salimans et al. 2017 formulation) via the authors' own ES-at-Scale library (Qiu et al. 2025, arXiv:2509.24372) — population size 30 suffices, no backprop, no gradient. Contrasted against RLVR/GRPO (Shao et al. 2024) run via VERL. Novel diagnostic apparatus: pass@k via the unbiased low-variance estimator (Chen et al. 2021); accuracy-distribution binning (fraction of k samples correct per prompt); progression/regression counts (prompts flipped correct/incorrect vs. base model); Shannon entropy over final-answer distributions at failure/regression cases; self-consistency/majority-voting accuracy as a non-verifiable-domain test-time-scaling proxy.

## Results

**GSM8K**: ES beats RL/GRPO on pass@k for Qwen2.5-1.5B/3B/7B-Instruct and Qwen3-1.7B/4B/8B; crossover ~k=2, gap grows with k. RL plateaus and is eventually overtaken by the *base* model at large k (replicating Yue et al. 2025); ES is never overtaken by base.

**MATH** (Qwen2.5-Math-7B/14B/32B vs. SOTA RL checkpoints SimpleRL-Zoo/OatZero on MATH500, Olympiad Bench, Minerva): ES beats both RL checkpoints for k>1, advantage persists/grows to 32B.

**Accuracy-distribution analysis**: RL increases the frequency of "unsolvable across all k" prompts relative to base — a hard ceiling on pass@k; ES decreases it. Progression/regression for Qwen2.5-Math-7B: MATH500 ES 6 progressions/3 regressions vs. RL 3/17; Olympiad Bench 56/15 vs. 33/49; Minerva 22/6 vs. 16/40 — ES wins on both axes simultaneously, not a diversity/capability tradeoff. Total regressions across the three benchmarks: ES 24 vs. RL 106.

**Entropy**: >25% of RL regressions have near-zero entropy (confidently wrong); ES regression entropy is materially higher (uncertain, not confidently wrong). Self-consistency voting: ES overtakes RL as k grows; RL's max-probability answer is worse than the *base* model on 2 of 3 benchmarks.

## Applicability

RLVR-style post-training for math/code/science domains where test-time-scaling / pass@k / best-of-n / self-consistency is the deployment regime, not just pass@1 chat quality. Needs a verifiable reward signal and an ES training stack (population ~30, no gradient/backprop infra). Demonstrated at both small (1.5B) and large (32B) scale across two model families — not gated on large scale, unlike [[eggroll]]'s framing.

## Novelty

Not a new algorithm — an empirical/diagnostic application of an already-published method (ES-at-Scale) to solution coverage specifically. Contribution: mechanistic explanation (progression/regression decomposition + answer-entropy analysis showing RL fails "confidently and narrowly" while ES fails "with preserved uncertainty") and direct confirmation/extension of Yue et al. 2025's "base model beats RL at large k" finding — ES doesn't exhibit that failure mode at any tested scale. Closest prior work: Qiu et al. 2025 (ES-at-Scale), Yue et al. 2025 (base-outperforms-RL-at-large-k), Hoy et al. 2026 (arXiv:2604.01499, concurrent ES-vs-GRPO geometry paper), Bahlous-Boldi et al. 2026 VPO (multi-objective RL diversity fix that trades pass@k for pass@1 — this paper's ES does not).

## Reproducibility

Code: github.com/conorfhayes/beyond-the-best-guess. Models/checkpoints: huggingface.com/collections/conorfhayes/beyond-the-best-guess. Public libraries (ES-at-Scale, VERL), public baselines (SimpleRL-Zoo, OatZero), public benchmarks (GSM8K, MATH500, Olympiad Bench, Minerva).

## Adoption

Too new to assess independently (captured week of publication). Signals of an active surrounding ES-for-LLM research program from the same lab/collaborators: Hoy et al. 2026, Sarkar et al. 2025 (EGGROLL), Schweighofer et al. 2026 (ES vs. forgetting in fine-tuning), Xu et al. 2026 (Quantized ES).

## Conflicts

Primary evidentiary update to [[conflicts/grpo-vs-evolution-strategies]] — see that page. Adds a comprehensive multi-scale (1.5B–32B), transformer-substrate (Qwen) pro-ES data point that weakens the conflict's prior "ES-beats-GRPO only feasible at 14B+" framing (which was substrate-dependent, tied to [[eggroll]]'s constant-state-RNN throughput argument). This paper's claim is on a different axis — solution coverage/pass@k, not wall-clock efficiency — and holds on ordinary transformers at every scale tested, including 1.5B.

Possible secondary, unresolved tension with [[rlvr-incentivizes-reasoning]] (Position E in [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]), which argues via CoT-Pass@K (not standard pass@k) that RLVR shows a "persistent advantage at all K" once guessing is controlled for. This source uses the standard pass@k estimator and finds RL-trained models overtaken by the base model at large k — the two papers may be measuring different things (CoT-Pass@K vs. raw pass@k) rather than strictly contradicting. Left unresolved pending a source that reconciles the two metrics directly.

## Source

- `raw/research/weekly-2026-08-29/01-es-solution-coverage.md` — arXiv:2608.12679. Captured 2026-08-29.

## Related

- [[conflicts/grpo-vs-evolution-strategies]] — primary target; new pro-ES Position A data point on the transformer/solution-coverage axis.
- [[eggroll]] — sibling ES-for-LLM-post-training paper; EGGROLL's axis is wall-clock efficiency at 14B+ on RWKV, this paper's axis is solution coverage across 1.5B–32B on Qwen — complementary, not overlapping.
- [[evolution-fine-tuning]] — same "evolutionary approaches to LLMs" cluster, different mechanism (SFT on evolutionary-search trajectories to internalize discovery capability, vs. direct ES weight-space optimization here).
- [[gepa-reflective-prompt-evolution]] — prompt-space evolution (no weight updates) vs. this paper's weight-space ES; both beat GRPO, different substrates.
- [[rlvr-incentivizes-reasoning]] — possible metric-definition tension flagged above (CoT-Pass@K vs. raw pass@k), not yet resolved.
- [[spurious-rewards-rlvr]] / [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — loosely related: this paper's distribution-collapse framing for RL is part of the same broader "how does RLVR reshape the output distribution" debate.
- [[watchlist]] — Qiu et al. 2025 ES-at-Scale, Hoy et al. 2026, Schweighofer et al. 2026, Xu et al. 2026 referenced but not captured.
