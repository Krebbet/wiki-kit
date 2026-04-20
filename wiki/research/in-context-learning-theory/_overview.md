# In-Context Learning: Theory & Mechanism

ICL is the closest analogue in current LLMs to "single example imprints a concept": one to a few demonstrations in the prompt change downstream behaviour without any weight update. Three competing-but-compatible mechanistic accounts dominate the literature: (1) **circuit-level** — induction heads copy `[A][B]…[A]→[B]`; (2) **algorithmic-level** — attention layers run gradient descent on an implicit loss over the in-context tokens; (3) **distributional-level** — the LM does Bayesian inference over latent pretraining concepts. The function-class line shows transformers can be *trained from scratch* to in-context learn classes optimally, providing the empirical playground where these accounts are tested. This theme assembles the foundational papers and threads them to the project's central question: *what does a single example actually teach a model?*

## Pages

- [[induction-heads]] — Olsson et al. 2022 (Anthropic). The phase-change paper: induction heads form, ICL emerges, loss bumps — all in the same training window.
- [[icl-as-gradient-descent]] — von Oswald et al. 2023 (Google/ETH). 1-layer LSA = 1 GD step on MSE; trained models match the construction; mesa-optimisation.
- [[icl-bayesian-inference]] — Xie et al. 2022 (Stanford). HMM-mixture pretraining ⇒ posterior concentration over latent concepts; ICL = implicit Bayes.
- [[function-class-icl]] — Garg et al. 2022 (Stanford). Trained transformers in-context learn linear / sparse / NN / decision-tree classes at near-optimal rates.

## Cross-cutting synthesis

### The mechanism debate

| View | "What is ICL?" | What it predicts | Where it wins |
| --- | --- | --- | --- |
| Induction heads | Content-addressable copy circuit | Sharp training-time phase change; fails without ≥2 layers; copies rare tokens | Strong causal evidence in small models; explains the phase change at scale |
| ICL = GD | Mesa-optimised gradient descent in the forward pass | K layers ≈ K SGD steps; out-of-distribution generalisation should track GD's; depth helps | Exactly matches optimal estimators on regression; explains why deeper TFs beat plain GD (curvature correction) |
| Bayesian inference | Posterior selection over latent concepts θ | Per-token information matters, not just labels; long examples help; example ordering matters | Explains why ICL works despite distribution shift; predicts ordering-sensitivity, zero-shot > few-shot edge cases |

These are not mutually exclusive. von Oswald explicitly reduces induction heads to a special case of LSA-as-GD (token-identity targets). GD-as-MAP under a Gaussian prior reconciles GD with Bayes. The induction phase-change is the moment the *prior* (Bayesian) or the *meta-optimiser* (GD) becomes well-formed enough to consume in-context examples productively.

### Method × claim × sample-cost comparison

| Paper | Probe domain | Mech. evidence | Sample efficiency (test-time) | Sample efficiency (training) |
| --- | --- | --- | --- | --- |
| Induction heads | LM pretraining (1L–13B) | Ablation + co-perturbation | 1 prior `[A][B]` suffices for copy | Phase change at 2.5–5e9 tokens |
| ICL = GD | Synthetic regression (LSA TF, ≤5 layers) | Explicit weight construction matched by trained weights | Optimal in N(=context length) for linear; K layers = K free GD steps | 500k SGD steps, fresh tasks |
| Bayesian | GINC HMM mixture (small TF / LSTM) | Posterior-concentration proof + GINC empirics | Exponential in n (count) and linear in k (per-example length) | Fits any well-specified concept family |
| Function class | Synthetic regression (GPT-2 9.5M) | Behavioural matching of optimal estimators | k = d for linear; k ≈ s log d for sparse; k ≈ 100 for trees | ~32M prompts, but 1k distinct fns suffices |

### What ICL implies for explicit single-sample fine-tuning

Across all four accounts the same skeleton appears: a single example exerts its effect through a *low-rank, structured update* that interacts with a meta-learned prior. Implications for David's method:

1. **Update structure should mirror the implicit ICL update.** GD-in-attention says the implicit update is rank-1 outer product `(Wx − y) xᵀ` with a meta-learned η — i.e. LoRA-shaped, not full-weight. Single-sample fine-tunes that respect this structure should be most efficient.
2. **The base model must be past the phase change.** Induction-heads work argues that single-shot fine-tuning a *pre-phase-change* model will not generalise — the model has no copy/abstraction circuit to read the imprint.
3. **Long, structured examples beat short ones.** Bayesian theory makes per-token information explicit (Theorem 2). A single example of 1000 tokens carries more posterior signal than ten examples of 10 tokens.
4. **Concept-family scoping.** Function-class ICL is near-optimal *within* a trained family; explicit fine-tuning probably inherits this — better to fine-tune across a family than per-task.
5. **Curvature matters.** GD++ outperforms plain GD; explicit single-sample SGD without a preconditioner is leaving signal on the table.

## Open questions

- Are the three accounts genuinely unifiable, or do large LMs run a *mixture* of mechanisms? (Olsson §6 explicitly flags this.)
- Does the rank-1 GD update generalise to softmax (non-linear) attention beyond the regression toy setting?
- For a base model past the induction phase change, what is the minimum-token explicit fine-tune that matches one in-context demonstration?
- Bayesian theory predicts ordering-sensitivity; does single-sample fine-tuning inherit a parallel "presentation-order" failure mode?
- Function-class results are on synthetic d = 20 problems — do the optimal-estimator-matching properties survive at LM scale and natural-language input distributions?

## Related themes

- [[meta-learning-few-shot]] — MAML and Prototypical Networks; the explicit-fine-tune analogue of ICL's implicit meta-learning.
- [[test-time-training]] — Akyürek et al.'s TTT and Algorithm Distillation: hybrid of explicit weight updates and ICL, narrowing the gap this theme studies.
- [[rlvr-mechanics]] — RL-side methods that also rely on dense per-step signal (cf. L2T's information-gain reward).

## Source

This overview synthesises the four pages above. No new external sources.

## Related

- [[induction-heads]]
- [[icl-as-gradient-descent]]
- [[icl-bayesian-inference]]
- [[function-class-icl]]
