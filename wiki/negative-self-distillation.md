# Negative Self-Distillation (NSD): Learning to Reason by Avoiding Flaws

UVA/Stanford (arXiv:2609.11699): a label-free, fully self-bootstrapped post-training framework that trains a reasoning LLM to diverge from a self-generated "negative teacher" — itself conditioned to reason carelessly — instead of imitating a privileged-information teacher. Fixes On-Policy Self-Distillation's (OPSD) tendency to suppress uncertainty and self-correction, without needing gold answers. Sibling of [[anti-self-distillation]] (shares the same problem framing and even the same cited prior-work arXiv ID) but via a distinct mechanism.

## Method

Two components:

1. **Negative condition generation.** For unlabeled problem x, the student samples an initial rollout y_init, then (conditioned on x and y_init) generates an adaptive negative instruction n — e.g. "act as a careless reasoner" — no gold answer used. n conditions a frozen copy of the same weights into a "negative teacher" π_neg; a frozen π_ref conditioned only on x is also instantiated.
2. **Gated unlikelihood training.** Naive unlikelihood training (Welleck et al. 2020) conflates flawed-reasoning tokens with ordinary grammatical tokens, causing gradient blow-ups. NSD instead computes a token-level gate G_t = max(0, π_neg(y_t) − π_ref(y_t)) that isolates only tokens whose likelihood is abnormally boosted by the negative condition. The suppression loss is a sigmoid-bounded unlikelihood penalty L_GU = G_t · 1/(2−π_θ(y_t)), plus a forward-KL anchor to π_ref for stability (α=0.01 weight). Total: L_NSD = L_GU + α·L_KL.

Only one student rollout per sample is needed (vs. n=8 for GRPO-style baselines); π_ref/π_neg forward passes are parallelizable and need only top-k=32 logprobs (vs. OPSD's top-k=128-style full-vocab alignment). Three alternative negative-conditioning strategies (offline solution-aware, question-only, even random irrelevant-Wikipedia-text) are all competitive with the online default — the gating mechanism, not the specific negative content, does the work.

Derives from: On-Policy Distillation (Agarwal et al. 2024, external teacher) → OPSD (Zhao et al. 2026a, ground-truth-conditioned self-teacher — NSD's main foil) → unlikelihood training (Welleck et al. 2020, the base objective NSD modifies).

## Results

Trained on MATH (gold labels discarded), 2 epochs, Qwen3-1.7B/4B/8B; evaluated Avg@8 non-thinking on AIME24/25/26, HMMT25, AMC23, OlympiadBench, MATH-500. NSD Δ-Avg over base: **+2.3% (1.7B), +7.5% (4B), +6.0% (8B)** — best of all baselines at every scale. Baselines: OPSD† (uses gold labels) only +1.1/+1.0/+0.3; Intuitor (RLIF) −0.5/+1.3/+1.9; TTRL +0.3/+0.2/−0.1. NSD's p-values are <10⁻⁴–0.001 vs. baselines' 0.05–0.57 — baseline gains are often statistically indistinguishable from noise.

Reflection-token frequency ("Wait"-style tokens, Qwen3-4B): baseline 3.6, OPSD 2.2 (suppressed), Intuitor 0.8 (suppressed), **NSD 7.5** — more than doubles baseline rather than suppressing it. Efficiency: ~60% rollout-time reduction from n=1 vs n=8 rollouts. Ablation: removing the KL anchor causes mid-training distributional collapse (~step 120).

## Novelty

A refinement/recombination: reuses unlikelihood training and the OPSD self-teacher setup, but the combination — self-generated per-sample negative condition + reference-vs-negative gating + sigmoid-bounded unlikelihood — is new. Closest prior work is [[anti-self-distillation]] (Shen et al. 2026, arXiv:2605.11609, cited directly by this paper), which shares the exact motivation (self-distillation suppresses high-entropy/reflective tokens) but a different mechanism (PMI/JSD-ascend with entropy-gated activation vs. NSD's reference-vs-negative-teacher gate). **NSD does not benchmark directly against AntiSD or against [[u-opsd-unsupervised-self-distillation]]** (also cited, arXiv:2608.06296, exact match) — its baselines are OPSD/Intuitor/TTRL only, so its claim of SOTA within the label-free self-distillation family is unverified against those two close siblings.

## Applicability

Any RLVR-style reasoning post-training on math/verifiable domains wanting to avoid needing gold answers (for privileged-teacher self-distillation) or an external tokenizer-compatible stronger teacher. Requires a base model capable of generating coherent negative conditioning — paper flags this fails for very weak/small models. Single-node, 6–8 GPU scale demonstrated; no multi-sample GRPO rollout budget needed. Gains grow with scale since negative-condition quality scales with model capability.

## Reproducibility

Code: github.com/Prongcan/NSD. Weights: HF collection PassionPrc/nsd-negative-self-distillation. No independent reproduction yet (concurrent with this ingest).

## Source

`raw/research/weekly-2026-09-12/03-negative-self-distillation.md` (arXiv:2609.11699)

## Related

- [[anti-self-distillation]] — closest prior work by shared arXiv citation (2605.11609); same problem framing, different mechanism (PMI/JSD-ascend+entropy-gate vs. NSD's negative-teacher-gate+bounded-unlikelihood). Sibling, not superseding.
- [[u-opsd-unsupervised-self-distillation]] — exact arXiv match (2608.06296) cited by NSD as a label-free OPD approach; parallel strategy NSD doesn't benchmark against directly.
- [[rlsd-self-distilled-rlvr]] — another OPSD-privileged-info fix (decouples direction/magnitude); same cluster, different fix axis.
- [[dopd-dual-on-policy-distillation]] / [[flux-opd]] — other recent OPD-cluster refinements extending the same OPSD lineage.
- [[high-entropy-tokens-rlvr]] / [[delta-token-credit]] / [[token-gradient-cancellation]] — parallel token-level gating/credit-assignment mechanisms in RLVR; NSD's G_t gate is a distillation-side analog.
- [[reasonmaxxer]] / [[thought-anchors]] — corroborate the sparse/high-entropy-token-matters framing motivating NSD's gating design.

**Note for maintainers:** the OPD/OPSD cluster now has 10+ member pages (this one included) with no cluster-overview page, unlike [[test-time-training]]'s comparison-table treatment of the TTT cluster. Candidate for a future session to build one, given the mechanism-vs-mechanism distinctions (gating axis, teacher construction, what's being decoupled) are getting hard to track page-by-page.
