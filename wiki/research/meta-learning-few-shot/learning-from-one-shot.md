# Learning from One and Only One Shot

Yu, Mineyev, Varshney, Evans (arXiv:2201.08815, 2022). A nativist, white-box model that classifies images from 1–10 examples per class with *no pretraining* by learning a "general-appearance" similarity built from canvas (geometry) and color (intensity) distortions. Plain 1-NN in this similarity space reaches near-human Omniglot one-shot accuracy and beats neural baselines in tiny-data MNIST/EMNIST.

## Method
- *Distortable canvas*: every image is a smooth function M : R² → R₊ painted on an elastic canvas; transformations α : R² → R² (canvas) and χ : R₊ → R₊ (color) deform it.
- Two distortions: D_C(M, χ∘M'∘α) = ||a M'(α) + b − M(id)||² (color discrepancy after affine recolor); D_V(α) = log-ratio edge-distortion measuring how non-conformal α is on the canvas lattice (Eq. 3).
- Two dual general-appearance distances:
  - D_C-distance: min D_C s.t. D_V(α) ≤ ε.
  - D_V-distance: min D_V s.t. D_C ≤ ε.
- Solved via *Abstracted Multi-level Gradient Descent (AMGD)*: a chain of coarser→finer anchor lattices Ĝ paired with a chain of decreasing color-blur radii ρ_c. Each (Ĝ, ρ_c)-step warm-starts the next, escaping the curse of vanishing gradients caused by D_V's many invariances.
- Inference: 1-NN under D_C-distance for classification; k-means-style clustering with multi-flow optimization for unsupervised archetype generation.
- Output is interpretable: the gradient trajectory yields a *transformation flow* (animation) showing how one image morphs into another.

## Claims
- MNIST tiny-data: 80% accuracy from the *first training image per class* (10 examples total); 90% from first 4 per class — beats TextCaps, SVM, k-NN baselines (Fig. 2a).
- EMNIST-letters tiny-data: dominates all baselines for small N; advantage narrows as N grows because 1-NN is fragile to label noise (Fig. 2b).
- Omniglot one-shot 20-way: 6.75% error with no background set or stroke data — near human (4.5%); only BPL (3.3%) does better and uses background + strokes (Fig. 3).
- QuickDraw only-one-shot 15-way (no pretraining): 34.2% accuracy vs human 39.7% ± 4.6%; beats CNN, ViT, k-NN; pairwise Fleiss' κ between model and humans matches inter-human agreement (Fig. 4).
- Unsupervised archetype generation: k-means in the learned similarity space recovers human-intuitive cluster centroids (e.g., two stylistic ways of writing "7"; four giraffe-doodle archetypes) (Fig. 5).

## Sample efficiency
"Only-one-shot" is stricter than standard few-shot learning: a single labeled example per class *and no pretraining/background set*. Efficiency comes entirely from a hand-built *innate prior* — the distortable-canvas model encodes humans' visual invariances (translation, rotation, scaling, smooth deformation) directly into the similarity metric, so no statistical learning of those invariances from data is needed. The price is domain narrowness: the prior fits abstract visual tasks (characters, doodles) and is not obviously suited to photorealistic images (the authors propose an "emoji-fication" preprocessing stage as future work).

## Sample efficiency
(See above.) The crucial lesson: for sufficiently restricted domains, an *explicit prior* can replace meta-training entirely, achieving one-shot generalization that gradient-based or metric-based meta-learners require thousands of episodes to approximate.

## Relevance to the project
This paper is the strongest empirical case that *single-sample learning* is achievable when the inductive bias is right — and that the bias does not need to be learned from a meta-distribution. For LLMs, the analogous question is: does a pretrained LLM already contain the "innate priors" (linguistic, conceptual, compositional) that play the role of the distortable-canvas model? If yes, then David's project — single-sample concept-based fine-tuning — is doing for LLMs what 1-NN-on-D_C does here: leveraging a rich pre-existing similarity structure so that one example pins down a concept region. What is missing/needed: (a) LLMs lack an interpretable analogue of the transformation flow, so updates are harder to diagnose; (b) the model is a *classifier*, not a generator — generative concept updates require a different distortion notion (likely a divergence between conditional output distributions); (c) the paper's k-NN approach is non-parametric, whereas David wants weight updates that *internalize* the concept.

## Source
- arXiv: 2201.08815
- Raw markdown: `../../../raw/research/single-sample-llm-learning/08-08-learning-from-one-shot.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/08-learning-from-one-shot.pdf`

## Related
- [[maml]] — opposite philosophy: learn the prior from a meta-distribution; here, encode it by hand.
- [[prototypical-networks]] — both rely on a similarity space + simple classifier; protonets learn the metric, this paper engineers it.
- [[../in-context-learning-theory/_overview]] — LLM in-context generalization as the "innate-prior" analogue.
- [[../test-time-training/_overview]] — alternative route to single-example adaptation in deep models.
