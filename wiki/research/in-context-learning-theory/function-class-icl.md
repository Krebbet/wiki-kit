# What Can Transformers Learn In-Context? A Case Study of Simple Function Classes

Garg, Tsipras, Liang, Valiant (Stanford, NeurIPS 2022) reframe ICL as the well-defined problem "can we train a model to in-context learn a *function class* F?" Given prompts `(x_1, f(x_1), …, x_k, f(x_k), x_query)` with f sampled from F and x's i.i.d., they train a 9.5M-param GPT-2 from scratch to predict `f(x_query)`. Trained transformers match the *optimal* estimator on linear functions (least squares), match Lasso on sparse linear, beat XGBoost on depth-4 decision trees, and match a 2-layer MLP-on-the-fly for 2-layer NN regression. Out-of-distribution prompt shifts degrade performance gracefully, ruling out memorisation.

## Method

**Training objective** (Eq. 2): minimise expected squared error of `M_θ(P^i)` against `f(x_{i+1})` over all prompt prefixes `P^i`, averaged over fresh prompts at every step.

**Architecture.** Decoder-only GPT-2: 12 layers, 8 heads, 256-d embeddings, 9.5M params. Inputs and outputs projected into the latent space via learned linear maps; final scalar read out by another linear map. Trained from scratch — *not* fine-tuned LM, no text.

**Curriculum.** Start with prompts of length 11 in a 5-d subspace, increase subspace dim and prompt length every 2k steps until ambient d and length 2d+1. Crucial for d ≥ 50.

**Function classes.** d = 20 throughout. (a) Linear: `w ∼ N(0,I)`, `f(x) = wᵀx`. (b) Sparse linear: same but only s = 3 non-zero coords. (c) Depth-4 decision trees with axis-aligned splits at threshold 0. (d) 2-layer ReLU NNs with 100 hidden units.

**OOD probes.** Skewed-covariance inputs, label noise, low-d subspace, scaled prompts, in-context vs. query in different orthants, query orthogonal to in-context inputs, query equals an in-context input.

## Claims

- **Linear regression.** Trained TF achieves error 0.02 at k = d and 0.0006 at k = 2d in-context examples, matching least squares (which is optimal); >>better than nearest-neighbour or simple averaging baselines. Fig. 2.
- **Memorisation ruled out.** Even when training is restricted to 10k distinct weight vectors, model reaches near-optimal error; best-train-vector baseline is ≥ 0.5. Prompt input space is 800-d, so prompt-level memorisation is astronomically unlikely.
- **Sparse linear.** Matches Lasso (TF 0.58/0.09 vs Lasso 0.62/0.08 at k = 5/10). One forward pass ≈ iterative L1-regularised solver.
- **Decision trees.** TF reaches error 0.12 at k = 100; greedy 0.80, XGBoost 0.62. Significant beat against tuned baselines.
- **2-layer NNs.** Matches a 2-layer NN trained on the in-context examples by Adam (TF & baseline 0.17 at k = 100). The same model also in-context learns linear functions (transfer across classes).
- **OOD robustness.** Performance degrades gracefully under skewed covariance, label noise, and orthant mismatch; full collapse only under extreme scale shifts (e.g. ×1/3 or ×3 input scaling). Figs. 4, 6.
- **Capacity ↔ dimension.** Bigger models handle higher-d problems and generalise better OOD; effect persists where in-distribution gain is small.
- **Phase change.** Without curriculum, training shows a long flat loss followed by a sharp drop — explicitly compared to the [[induction-heads]] phase change.

## Sample efficiency

The trained model recovers an optimal *learning algorithm* in its forward pass: for linear regression, k = d examples suffice for near-zero error, k = 2d for essentially exact recovery. For sparse linear (s = 3 of d = 20), it nearly matches the information-theoretic floor of Lasso with O(s log d) examples. Critically, even **a single in-context example** moves the predictor's gradient w.r.t. `x_query` substantially toward the projected ground truth (Fig. 3b). The model's best-case sample efficiency in-context is bounded by the optimal estimator for the class — i.e. it has *learned the correct prior over F*.

The outer training loop, however, sees ~32M distinct prompts; a low-data ablation shows non-trivial ICL with only 1k distinct functions or 100k prompts — meta-training is data-hungry, but *much* less so than naively expected.

## Relevance to the project

This paper is the cleanest demonstration that in-context examples convey *learning-algorithm-quality* information, not just exemplar information. For David's project: (1) it sets a sample-efficiency floor — a single explicit fine-tune step on one example can match what one in-context example does *only if* the fine-tuner encodes the right inductive bias for the task family. (2) The OOD robustness results show that meta-trained algorithms generalise well *within* a family; this argues for fine-tuning at the level of *concept families* (e.g. all linear-style associations, all tree-style classifications) rather than per-task. (3) The decision-tree result — TF beats XGBoost — hints that meta-learned algorithms can outperform classical ones on concept structure that humans haven't characterised; single-sample fine-tuning may inherit that capability if the base model has the right meta-priors.

## Source

- arXiv: 2208.01066
- Raw markdown: `../../../raw/research/single-sample-llm-learning/13-A-4-function-class-icl.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/A-4-function-class-icl.pdf`

## Related

- [[icl-as-gradient-descent]] — mechanistic explanation for why this works on regression-style classes
- [[induction-heads]] — phase-change analogue at the linguistic level
- [[icl-bayesian-inference]] — predicts exactly the kind of optimal-Bayes-estimator behaviour observed here
