# Prototypical Networks for Few-shot Learning

Snell, Swersky, Zemel (NeurIPS 2017). Prototypical networks classify a query point by computing distances to per-class *prototypes* — the mean of embedded support examples — in a learned non-linear embedding space. The inductive bias is deliberately simple (one Gaussian-like cluster per class) and outperforms more elaborate meta-learners.

## Method
- Embedding f_φ : R^D → R^M (4 conv blocks for image benchmarks).
- Class prototype: c_k = (1/|S_k|) Σ_{(x_i,y_i)∈S_k} f_φ(x_i) (Eq. 1).
- Predictive distribution: p_φ(y=k | x) ∝ exp(−d(f_φ(x), c_k)) softmax over distances (Eq. 2).
- Trained episodically: each episode samples N_C classes and N_S support + N_Q query points; minimize negative log-likelihood of true class via SGD/Adam.
- Equivalent to mixture density estimation with an exponential family when d is a regular Bregman divergence (squared Euclidean → spherical Gaussian); choice of distance encodes a class-conditional density assumption.
- With squared Euclidean distance the model is a *linear* classifier in embedding space (Eq. 7–8); all non-linearity lives in f_φ.
- Zero-shot variant: replace c_k with g_ϑ(v_k), a learned embedding of class meta-data.

## Claims
- Omniglot 5-way 1-shot/5-shot: 98.8% / 99.7%; 20-way 1-shot/5-shot: 96.0% / 98.9% (Table 1) — beats matching nets (cosine) and neural statistician.
- MiniImageNet 5-way 1-shot/5-shot: 49.42% / 68.20% (Table 2) — large margin over matching nets (43.56% / 55.31%) and meta-learner LSTM (43.44% / 60.60%).
- CUB-200 zero-shot 50-way: 54.6% with GoogLeNet features vs prior 50.9% best (Table 3).
- Distance and "way" matter: Euclidean ≫ cosine, and training with higher way than test improves accuracy (Fig. 2, Table 5–6). Matching one-shot is identical to prototypical one-shot (single support point ≡ prototype).

## Sample efficiency
"Few-shot" = N-way K-shot episodes with K ∈ {1, 5}. Sample efficiency comes from (a) the strong inductive bias that classes form unimodal clusters in embedding space, (b) episodic meta-training that mimics the test-time evaluation protocol, and (c) the simplicity of nearest-prototype classification, which avoids overfitting that more parameter-rich meta-learners (matching nets FCE, meta-learner LSTM) suffer in the K=1 limit.

## Relevance to the project
Prototypical networks epitomize the *metric-based* branch of meta-learning: instead of preparing weights for fast SGD adaptation, learn an embedding in which classes are linearly separable by simple cluster statistics. The transfer to LLMs is more abstract than MAML's: an LLM's residual stream already encodes representations in which task/concept "prototypes" can be implicitly assembled from in-context exemplars (cf. ICL-as-Bayesian-inference, induction heads). David's single-sample method aligns with the prototypes intuition that *one well-chosen example defines a concept region*; the missing pieces for LLMs are (a) what counts as a "prototype" when the input is text and the output is a generation, not a class label, and (b) whether training the LLM to behave prototypically can be done without an episodic meta-distribution, which David's setup explicitly lacks. Most directly, the Bregman/exponential-family interpretation suggests that *any* concept-update method should be analyzable as implicit density estimation in representation space.

## Source
- Venue: NeurIPS 2017. arXiv: 1703.05175
- Raw markdown: `../../../raw/research/single-sample-llm-learning/15-B-2-prototypical-networks-snell.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/B-2-prototypical-networks-snell.pdf`

## Related
- [[maml]] — gradient-based meta-learning counterpart; comparable accuracy, very different mechanism.
- [[learning-from-one-shot]] — single-shot k-NN in a hand-crafted similarity space, no meta-training at all.
- [[../in-context-learning-theory/_overview]] — LLMs as implicit prototype learners over in-context support sets.
