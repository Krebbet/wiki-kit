# Recirculation

Google DeepMind (Mozer, Siddiqui, Sawyer, Sanyal, Liu; arXiv:2608.17981, preprint under review) introduces recirculation, a training-free, inference-time architectural modification that leaks a mixture of deep-layer activation back down to a shallow layer at every generation step, giving an off-the-shelf transformer depth-*and*-step recurrence for state tracking. A lightly-tuned, weight-frozen "adaptive" variant cuts perplexity 23% and GSM8k pass@128 error ~21% on Gemma3.

## Method

Formalizes one-iteration recurrence as a convex mixture at each unrolling step `t`:

`z_{t+1,t,d} = α·f(z_{t,t,s}) + β·z_{t,t,d}`

where `s`/`d` are fixed source/destination layer indices, `f` is an L2-renormalization of the source vector to match the destination's norm, and `β = 1−α`. Two transformer stacks run per input step (one is a warm-up pass), so recurrence spans both depth and sequence step — contrast with looped transformers (Universal Transformers-style, cf. [[hyperloop-transformers]]), which recur only in depth via shared-weight blocks. No weights modified; only layer indices and α/β are hyperparameters, found via grid search per model size. Cost: negligible extra decode latency, but prefill must run token-by-token serially — this is the main deployment tax.

Adaptive recirculation keeps the base model frozen and trains a small MLP that maps token-specific source/destination embeddings to token-conditional, vector-valued α and β. Trained on as few as 250 documents (arXiv/C4/PG19) or a few thousand MMLU examples. Beats four other ablations and matches/exceeds full fine-tuning of the augmented architecture, without touching backbone weights.

## Results

Perplexity (10 LM datasets, Gemma3 1B/4B/12B): reductions up to 16% for 1B/4B, up to 35% for 12B; 9/10 datasets improve at all three scales. Adaptive recirculation raises mean reduction to 23.0% (vs 8.5% for basic recirculation) and matches full fine-tuning (23.0% vs 21.6%) while leaving weights untouched.

Cross-family check (Ministral3-3B, Pythia-1B, Qwen3-1.7B, Phi2-2.7B): same sweet-spot pattern appears but effect size is far smaller (~5% vs <0.5%) — gains are architecture/training-procedure dependent, possibly tied to Gemma's Peri-LN.

Recirculation (14.21% PPL reduction) vs temperature tuning (temp=1.2, 8.48%): combined effect is 19.55%, near-additive — rules out "it's just softmax sharpening."

Recirculation vs looping (matched training-free comparison): training-free looping does not produce robust benefits for Gemma3 at small/mid scale (consistent with prior training-free-looping literature, which reports gains only at larger scale); recirculation helps across all three scales tested.

GSM8k (Gemma3 4B, zero-shot CoT): recirculation improves both pass@1 (sharpening) and pass@128 (expansion); adaptive recirculation yields 8.8% and 20.9% error-rate reductions respectively — the headline "~21%" figure is the pass@128 adaptive number.

Token-level analysis: benefit is a power function of lag `k` (largest at short lags); harmful at earliest context positions (`t<10`), but only for the 1B model. Adverbs/adjectives/verbs benefit most.

## Applicability

Any pretrained decoder-only transformer with access to residual-stream activations between layers. No training required for the base variant — just a small grid search (2 layer indices + α) on ~1.5M tokens or less. Caveats:

1. Requires serial prefill — real latency cost for long-context inputs.
2. Hyperparameters are dataset/task-dependent; no automatic task→hyperparameter mapping yet.
3. Gains are Gemma-family-outsized; expect much smaller wins on other architectures absent further tuning.

Adaptive variant needs a small tuning set and light MLP training — single-GPU-afternoon cost, not a large compute investment.

## Novelty

The leak-and-mix operation itself is simple; the contribution is identifying a previously-unexploited region of design-affordance space — depth+step recurrence — provably distinct from looped transformers (depth-only recurrence, cf. [[hyperloop-transformers]]) and from CoT/thinking-token recurrence (token-level, coarser-grained). The sharpest novelty claim: training-free looping fails to help small/mid-scale Gemma3 while recirculation succeeds across all three scales tested. Adaptive recirculation (frozen-weight, learned mixing matching full fine-tuning) supports an "affordance-first, train-second" methodology the authors advocate more generally — cf. [[test-time-training]] and [[in-place-ttt]] for other instances of that pattern.

## Reproducibility

No code, weights, or PapersWithCode entry as of capture. Preprint explicitly marked "under review" (Google DeepMind + UT Austin). No third-party reproduction; one internal replication (Gemma3 1B heatmap reproduced independently in PyTorch/HuggingFace vs. the original JAX implementation) is a within-paper check only, not external validation.

## Adoption

Brand-new preprint (captured 2026-08-22) — no citation or community signal yet.

## Source

- `raw/research/weekly-2026-08-22/06-recirculation-inference-time-recurrence.md` — arXiv:2608.17981.

## Related

- [[hyperloop-transformers]] — both are depth-recurrence takes on the transformer stack, but hyperloop-transformers trains a shared-block looped architecture from scratch with loop-level mHC, while recirculation is training-free. Nuance: this paper finds training-free looping alone gives no robust benefit for small/mid-scale Gemma3 (only helping at larger scale, per prior literature) — looping needs to be trained in to pay off; recirculation is a different, training-free depth+step mechanism that works at inference time without that requirement.
- [[test-time-training]] — parallel inference/adaptation-time enhancement to a frozen or lightly-adapted model without full retraining; different mechanism (activation mixing vs. fast-weight/TTT updates).
- [[in-place-ttt]] — parallel: both are drop-in, training-free-or-nearly-so modifications to a pretrained checkpoint with no architecture change. Recirculation's adaptive variant (frozen backbone + small trained MLP) is structurally close to in-place-ttt's "repurpose existing components, no full retrain" ethos.
- [[gram-recursive-reasoning]] / [[hrm]] / [[hrm-text]] — reference frame for classifying recurrent/looped-reasoning models; recirculation is inference-time-only and much cheaper than HRM/GRAM's trained dual-timescale recurrence.
