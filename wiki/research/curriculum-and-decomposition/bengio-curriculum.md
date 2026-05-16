# Curriculum Learning

Bengio et al. (ICML 2009) formalize curriculum learning as the strategy of ordering training examples from easy to hard to improve convergence speed and generalization in non-convex neural network optimization. They frame this as a continuation method: progressively annealing from a smoothed/simplified loss toward the target loss, guiding optimization into better basins of attraction.

## Method

Bengio et al. model curricula as reweighting schemes over a training distribution. At each stage λ in [0,1], a weight function W_λ(z) assigns lower weight to "difficult" examples and higher weight to "easy" ones. The curriculum is formalized as a sequence of distributions Q_λ where Q_λ(z) ∝ W_λ(z)P(z), with constraints that entropy increases monotonically and example weights are non-decreasing. This satisfies the continuation method principle: optimize an easy (smoothed) criterion first, then gradually move toward the true target by increasing λ, with the intuition that the easy version reveals the global landscape and guides weights into a basin of attraction for better local minima.

Empirically, they test this on two domains: (1) **shape recognition** — a 3-layer neural network classifies 32×32 images of geometric shapes (rectangle, ellipse, triangle) using a two-stage curriculum: first train on "BasicShapes" (restricted shape variations: squares, circles, equilateral triangles), then on full "GeomShapes"; (2) **language modeling** — a ranking-based model predicts the next word, with curriculum stages that grow vocabulary incrementally (5k words, then +5k at each pass through Wikipedia, until 20k).

The core principle: start small with simpler concept subsets, let weights settle into a good region, then expand to the full target distribution.

## Claims

- **Convergence speed (online):** Perceptron trained with curriculum (examples sorted by easiness: number of irrelevant features or margin) converges faster than random order; curriculum significantly outperforms no-curriculum across 500 random seeds with statistically significant differences (Sec. 4.2, Fig. 1).

- **Generalization on shapes:** Two-stage curriculum on shape recognition yields median test error ~13–14% (switch epoch 64, Fig. 3, Sec. 5) vs. ~17% baseline (no curriculum). Distribution of errors over 20 seeds shows curriculum advantage is robust and statistically significant; curriculum benefit persists even when controlling for total examples seen by training on union of easy+hard sets.

- **Language modeling:** Curriculum (incremental vocabulary) achieves final test log-rank of 2.78 vs. 2.83 (no curriculum) on 20k-word Wikipedia task. Difference is small but statistically significant; curriculum crosses baseline error after ~1 billion updates, shortly after switching to full vocabulary (Sec. 6.2, Fig. 5).

- **Regularization effect:** Curriculum acts as a regularizer — test set benefit appears disproportionate to training set benefit, similar to unsupervised pre-training (Sec. 2, 7).

- **Continuation method link:** Curriculum guides non-convex optimization into basins of attraction of better local minima, not just faster wall-clock convergence (Sec. 3, Discussion).

- **Convex case:** Even in convex settings (Perceptron on clean Gaussians), "easy" examples (correctly classified by Bayes classifier) yield lower generalization error (16.3% vs 17.1%, Sec. 4.1).

## Relevance to the project

**Continuation-method fit:** RCL's strategy of decomposing a concept into learned prerequisites aligns with the continuation method frame Bengio et al. propose. If a student first learns a small sub-concept (e.g., "has two legs"), the learned weights sit in a favorable basin; adding compositional structure (e.g., "has two legs AND four-legged" → "quadruped") from that basin may be easier than learning the full structure cold. The easy-to-hard contract is satisfied: simpler concepts (fewer distinguishing features, smaller hypothesis space) come first, reducing the "noise" or confusion from irrelevant dimensions in the weight space.

**Non-convex optimization intuition:** Bengio's core insight is that curriculum learning helps escape poor local minima in non-convex landscapes. For RCL, this suggests that training a small subnetwork on a single-sample concept first "primes" the weight initialization and gradient flow for larger, compositional concepts. The basin of attraction argument predicts that a model trained to 100% accuracy on a narrow concept should transition more smoothly to a richer concept than one randomly initialized. Whether RCL achieves the same regularization effect (better test error) remains empirically open.

**Limitations & gaps:** Bengio's experiments use hand-authored curricula (easier shapes, vocabulary growth); the paper does not address _learned_ curricula driven by student failures, which is RCL's core novelty. Bengio's tasks are pre-LLM (shape classification, small-vocabulary language modeling); modern LLMs may have different optimization landscapes. His vocabulary-growth curriculum is simple ordering; RCL's recursive decomposition is conceptually richer (prerequisite structure, not just ordering). Finally, Bengio does not explore RL-style settings with sparse rewards or active failure-driven curriculum selection—RCL's RL motivation (learn from dense single-sample signals) is orthogonal to these supervised experiments.

## Source

- Venue: ICML 2009 (Proceedings of the 26th International Conference on Machine Learning)
- Authors: Yoshua Bengio, Jérôme Louradour, Ronan Collobert, Jason Weston
- Raw markdown: `../../../raw/research/rcl-gap-fillers/05-bengio-curriculum.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[curriculum-survey]] — 2022 survey extending Bengio's frame across 200+ papers; cite this for downstream developments
- [[acl-deep-rl-survey]] — RL-specific descendant; ACL signals replace easy-to-hard with learning-progress
- [[../synthesis/recursive-concept-learning]] — the continuation-method theoretical frame; RCL's "decompose to prereqs first" is a learned, failure-driven instance of Bengio's easy-to-hard ordering
- [[../single-sample-rl-finetuning/_overview]] — the wiki's "1-shot RLVR" frame is the limit case of Bengio's curriculum: just one example, but with massive prior structure substituting for the easy-to-hard ramp
