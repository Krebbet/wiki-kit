# Transformers Learn In-Context by Gradient Descent

von Oswald, Niklasson, Randazzo, Sacramento et al. (Google Research / ETH, ICML 2023) show that a *single linear self-attention layer* can be hand-constructed to implement exactly one step of gradient descent on a least-squares loss over the in-context tokens, and — more strikingly — that linear self-attention transformers *trained from scratch* on regression tasks converge to weights that match this construction (up to scaling). Stacking K layers ≡ K GD steps; trained K-layer models actually surpass plain GD by discovering an iterative curvature-correction variant they call GD++. With MLPs, the same equivalence extends to GD on deep representations (kernel regression). The paper frames trained transformers as *mesa-optimisers*.

## Method

Standard self-attention update `e_j ← e_j + Σ_h P_h V_h softmax(K_hᵀ q_{h,j})`; drop softmax → linear self-attention (LSA).

**Proposition 1.** Given tokens `e_j = (x_j, y_j)` and a one-head LSA layer, there exist `W_K, W_Q, W_V, P` such that the update on every token equals the GD-on-MSE update:
```
e_j ← (x_j, y_j − ΔW x_j),   ΔW = −(η/N) Σ_i (W_0 x_i − y_i) x_iᵀ
```
The construction encodes the learning rate η inside the projections; the test-token prediction is read out from the y-entry of the query token after a final sign flip.

**Empirics.** Train a 1-layer LSA transformer on linear regression with random teachers `W_τ ∼ N(0,I)`. Compare trained weights θ\* to constructed θ_GD via (a) cosine similarity & L2 of predictions, (b) interpolated weights (θ + θ_GD)/2, (c) OOD evaluation by varying input scale α. All three show near-perfect equivalence.

**Deep / recurrent variants.** Looped 2-layer and non-recurrent 5-layer LSA models exceed plain K-step GD; the gap closes against GD++ which interpolates inputs via `H(X) = I − γ X Xᵀ` (curvature precondition). Trained transformers re-align with GD++.

**Nonlinear extension (Prop. 2).** A Transformer block (MLP + attention) can be constructed to implement GD on a kernel `k(x,y) = m(x)ᵀ m(y)` induced by the MLP — i.e. linear regression on learned features. Verified on sine-wave regression.

## Claims

- Trained 1-layer LSA matches 1-step GD in prediction L2, cosine of input-sensitivities, and OOD scaling — Fig. 2.
- Looped 2-layer and 5-layer LSA outperform plain GD but precisely match GD++ (Fig. 3); residual gap fully explained by a single γ parameter per layer.
- With prepended MLPs, the model solves nonlinear sine-wave regression by GD on deep features (Fig. 4); behaviour matches a meta-learned MLP whose output layer is updated by one GD step.
- Token preprocessing layers learn to format raw inputs into the (x,y) concat structure assumed by Prop. 1 — resolving the original token-construction caveat.
- Connects to induction heads ([[induction-heads]]): induction-head copy is a degenerate case of LSA-as-GD when targets are token identities.

## Sample efficiency

ICL = in-forward-pass GD, so sample efficiency inherits GD's: one example shifts the implicit weight by `−η · (W x − y) xᵀ`. A single in-context demonstration is one gradient step from `W_0` (typically ≈ 0); for well-conditioned tasks this is already informative, and stacking K attention layers gives K free steps. The paper's experiments show non-trivial in-context regression error after a *single* example, dropping to optimal as N → context length. The K-layer case demonstrates that depth ≈ training steps — a single forward pass on one example is roughly equivalent to depth-many SGD updates with a meta-learned learning-rate schedule.

## Relevance to the project

If ICL is implicit GD, then explicit single-sample fine-tuning is the *external* counterpart of the *internal* update an in-context demonstration would have triggered. Two implications: (1) the optimal single-sample SGD step should structurally resemble the rank-1 update `−η (Wx−y) xᵀ` that LSA implements — David's method may benefit from constraining updates to that form (e.g. LoRA-style outer products with meta-learned η). (2) The success of GD++ over GD suggests *curvature preconditioning* is what attention-based meta-learners discover; a single-sample fine-tuner that ignores curvature is leaving signal on the table. The Transformer-block / kernel result implies the right "concept slot" is not raw weights but features, again pointing toward LoRA/feature-space updates.

## Source

- arXiv: 2212.07677
- Raw markdown: `../../../raw/research/single-sample-llm-learning/11-A-2-icl-as-gradient-descent.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/A-2-icl-as-gradient-descent.pdf`

## Related

- [[induction-heads]] — copy-circuit view; reduced to a special case of GD-in-attention here
- [[function-class-icl]] — empirical companion: trained transformers match optimal estimators for linear/sparse/NN function classes
- [[icl-bayesian-inference]] — competing distributional account
