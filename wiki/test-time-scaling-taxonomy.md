# Test-Time Scaling in Reasoning LLMs: Inference Regimes, Evaluation, and Reproducibility

Case Western Reserve (Hariri et al., arXiv:2608.04001) formalizes "test-time scaling" (TTS) as budgeted inference over the implicit prefix tree of a **fixed** autoregressive model p_θ, splitting the design space into three structural regimes (single-trajectory, leaf-level, prefix-level), prescribing protocol-matched evaluation, and releasing ~1.95M reasoning traces plus a `Scorio` aggregation library. Not a new inference algorithm — a formalization, evaluation methodology, and empirical audit that unifies self-consistency, Best-of-N, MBR, beam search, MCTS/RAP/Tree-of-Thoughts, and DeepConf under one abstraction.

## Method

No weight updates anywhere in scope — Section 2.1 explicitly restricts to "budgeted inference algorithms built atop a fixed autoregressive model." Key constructs:

- **Prefix-tree formalization.** Budgeted inference operates over the implicit tree of token prefixes reachable from a prompt. Three regimes: (1) **single-trajectory sequential scaling** — one active path, extended/revised in place (budget-forcing, s1-style); (2) **leaf-level scaling** — sample N complete candidates, reduce via a terminal reducer (self-consistency, Best-of-N, MBR); (3) **prefix-level scaling** — search over unfinished prefixes (beam search, best-first, MCTS/RAP/Tree-of-Thoughts, value/PRM-guided decoding).
- **Decoding as energy–gate composition.** Any stochastic decoder = a token measure composed with a support gate (level/head-budget/objective gates). Proves parallel composition of mode-preserving head gates (top-k, nucleus, etc.) collapses to the single strictest gate — the one genuinely novel small technical result in the paper.
- **Evaluation separation.** Evidence extraction, fixed-bank decision rule, and causal stopping (across-rollout vs within-rollout) are distinct axes that must be evaluated end-to-end, not as isolated components — a stopping rule that peeks across rollouts breaks causal replay even if the reducer is unchanged.
- **Discovery–stability profile.** A unifying binomial/beta-binomial statistic from which Pass@k, pass^k, Maj@k, G-Pass@k, mG-Pass@k, and Geom@k all fall out as coordinates or simple functionals. Argued to be the correct primary object rather than any single scalar metric — reporting Pass@k alone hides the discovery/stability tradeoff visible in the full profile.
- **Reproducibility framework.** Distinguishes exact replay (same tokens/scores/seeds) from distributional reproducibility (statistically compatible re-estimate under reruns); requires protocol-consistent bootstrap/Wilson-interval uncertainty for any capability claim.

## Results

No new SOTA claimed — this is an audit, not a leaderboard entry. Four data blocks, ~1.95M traces total (Table 1: 1,948,821; note the abstract says "2 billion," almost certainly a typo against the intro/table's "2 million" — flag if citing the trace count):

- **27 open-weight reasoning models × MMLU-Pro + BBH**, zero-shot CoT: 500,661 responses, MMLU-Pro 3.13–70.47%, BBH 25.97–82.20% across the roster.
- **20 model configs × 120 competition-math questions** (AIME'24/'25, HMMT'25, BrUMO'25), 80 seeded samples each (192,000 traces): median Pass@k rises 56.49% (k=1) → 82.08% (k=80), while median all-correct (pass^k) *falls* to 15.00% — headline discovery gains mask collapsing per-seed stability.
- Best single-response model (Qwen3-30B-A3B-Thinking-2507, 75.56% @k=1) reaches Pass@80=91.67%, but **mean-log-prob Best-of-N selection falls from 75.56% to 65.83%** as k grows — more sampling compute can *lower* accuracy when the selection score is misaligned with correctness. Plurality voting reaches 78.33%@k=80; a reference-assisted verifier reaches 89.17% (not a valid inference-time result — has gold access).
- **186 problems × 5 2025–26 competition sets** (Qwen3.6-35B-A3B + gpt-oss-20b): Pass@80 up to 94.62%; reference-free pointwise-verifier selection trails Pass@80 by 8–16 points.

## Applicability

Gives vocabulary/accounting to avoid conflating sample count, verifier calls, and search-controller cost under one "budget" number — directly useful for designing test-time-scaling ablations or benchmarks. Released `Scorio` package (majority_vote / best_of_n / softmax_weighted_vote / adaptive_consistency_stop) is a drop-in reducer library. Prescribes bootstrap/Wilson uncertainty, causal-only stopping-rule replay, and shared-bank-vs-end-to-end comparison discipline. No training infra needed — the trace corpus (HF: `harimo/scorio`) and `Scorio` library are directly consumable as-is.

## Novelty

Recombination/formalization, not a new algorithm: unifies self-consistency, Best-of-N, MBR, beam search, MCTS/RAP, ToT, DeepConf, and Adaptive-Consistency under one prefix-tree abstraction and one discovery–stability metric family, plus a reproducibility taxonomy specific to sampled inference. The energy–gate decomposition of decoders and the proof that parallel head-gate composition collapses to the strictest gate is a genuinely novel small technical result. Systematizes prior inference-time-compute-scaling treatments with a formal prefix-tree object, an evidence/decision/stopping decomposition, and a matching reproducibility protocol.

## Reproducibility

- Code: `Scorio` library (mohsenhariri.github.io/scorio/tts).
- Data: HuggingFace dataset `harimo/scorio` — 1.95M+ full reasoning traces with progressively richer verifier/token-level signals.
- Single-source capture, this week's arXiv posting — no independent reproduction yet.

## Scope note: scaling vs training

This paper's formalization requires a **fixed base model p_θ** throughout — no gradient updates, no persistent-state mutation, only budgeted sampling/search over the prefix tree of a frozen policy. Under this strict framing, methods that update weights or persistent state at inference time fall **outside** "test-time scaling" as defined here; they belong to a different axis, test-time *training*/adaptation:

- The [[test-time-training]] cluster (Titans/MIRAS, Hope/Nested Learning, In-Place TTT) writes fast-weight state via gradient "surprise" signals during inference — a parameter/state update, not a fixed-p_θ search.
- [[tempo-test-time-rl]] (TEMPO) performs EM-style critic recalibration and policy-gradient updates on the actor at test time — training, in this paper's terms, not scaling, even though it operates at inference time on unlabeled test questions.

The two lines are complementary, not contradictory — a TTT-trained policy could itself be wrapped in this paper's leaf-level or prefix-level search — but they are answers to different questions ("how do I get more out of a fixed model's distribution" vs "how do I update the model/state using the test distribution itself"). Don't conflate "test-time scaling" (this page) with "test-time training" ([[test-time-training]], [[tempo-test-time-rl]]) on the strength of the shared "test-time" prefix alone.

## Source

- `raw/research/weekly-2026-08-22/04-test-time-scaling-prefix-tree.md`

## Related

- [[test-time-training]] — naming/scope distinction (see above); fixed-model budgeted inference here vs fast-weight state updates there — not an overlapping mechanism.
- [[tempo-test-time-rl]] — naming/scope distinction (see above); TEMPO performs test-time *training* (EM-style critic recalibration, gradient updates), which this paper's taxonomy would classify as outside its fixed-model scope.
- [[reasonmaxxer]] / [[thought-anchors]] / [[high-entropy-tokens-rlvr]] — parallel, not overlapping: those discuss sparse high-value token positions during RL *training*; this paper's prefix-level search/continuation-value estimation is the inference-time analogue of "which positions matter."
- [[triattention]] — both discuss budget-vs-accuracy tradeoffs at fixed inference cost, but on different resource axes (KV-cache memory there vs sample/search compute here).
