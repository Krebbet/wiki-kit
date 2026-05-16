---
title: "The Linear Representation Hypothesis and the Geometry of Large Language Models"
authors: "Kiho Park, Yo Joong Choe, Victor Veitch"
year: 2024
arxiv: "2311.03658"
venue: "ICML 2024"
tags: [theory, linear-representation, steering, probing, geometry, causal-inference]
theme: decoding-time-steering
role: theory-anchor
---

# The Linear Representation Hypothesis and the Geometry of Large Language Models

The first rigorous formalisation of the linear representation hypothesis (LRH): the claim that high-level concepts are represented as *directions* in an LLM's representation space. Park, Choe, and Veitch give counterfactual-grounded definitions in both the unembedding (output/word) space and the embedding (input/context) space, prove that each space connects to a distinct algorithmic operation (probing and steering respectively), and introduce a **causal inner product** under which both spaces unify. The result is a single axiomatic framework that simultaneously justifies linear probing, linear steering, and the use of mean-difference vectors as concept estimators — all derived from the same counterfactual object.

## Source

Park, K., Choe, Y. J., & Veitch, V. (2024). *The Linear Representation Hypothesis and the Geometry of Large Language Models.* ICML 2024. arXiv:2311.03658.

Code: [github.com/KihoPark/linear_rep_geometry](https://github.com/KihoPark/linear_rep_geometry)

## Method / Framework

### The LLM bilinear form

A language model maps context $x$ to an **embedding vector** $\lambda(x) \in \Lambda \simeq \mathbb{R}^d$ and each output word $y$ to an **unembedding vector** $\gamma(y) \in \Gamma \simeq \mathbb{R}^d$. The next-token distribution is:

$$P(y \mid x) \propto \exp\!\bigl(\lambda(x)^\top \gamma(y)\bigr).$$

Two distinct spaces, connected only via this bilinear inner product. Both can host a linear representation of a concept; they need not agree under Euclidean geometry.

### Concepts as causal latent variables

A **concept** $W$ is a binary latent variable caused by context $X$ and causing output $Y$. It is specified by a set of counterfactual output pairs $\{Y(W=0), Y(W=1)\}$ — e.g., $(Y(0),Y(1)) \in \{(\text{"king"},\text{"queen"}),(\text{"man"},\text{"woman"}),\ldots\}$ for male$\Rightarrow$female.

Two concepts $W$ and $Z$ are **causally separable** if $Y(W=w, Z=z)$ is well-defined for each $w,z$ — they can vary freely and in isolation.

### Unembedding representation (Definition 2.1)

$$\bar{\gamma}_W \text{ is an unembedding representation of } W \iff \gamma(Y(1)) - \gamma(Y(0)) \in \mathrm{Cone}(\bar{\gamma}_W) \text{ a.s.}$$

where $\mathrm{Cone}(v) = \{\alpha v : \alpha > 0\}$. Unique up to positive scaling; the sign encodes the ordering of the concept.

### Embedding representation (Definition 2.3)

$\bar{\lambda}_W$ is an **embedding representation** of $W$ if for any context-embedding pair $\lambda_0, \lambda_1 \in \Lambda$ such that (i) $P(W=1\mid\lambda_1)/P(W=1\mid\lambda_0) > 1$ and (ii) $P(W,Z\mid\lambda_1)/P(W\mid\lambda_1) = P(W\mid\lambda_0)$ for every causally separable $Z$:

$$\lambda_1 - \lambda_0 \in \mathrm{Cone}(\bar{\lambda}_W).$$

Condition (i) requires the pair to be concept-relevant; condition (ii) requires it to be off-target-neutral.

### Causal inner product (Definition 3.1)

Let $\bar{\Gamma}$ be the space of differences of unembedding vectors ($d$-dimensional real vector space). A **causal inner product** $\langle\cdot,\cdot\rangle_C$ on $\bar{\Gamma}$ satisfies:

$$\langle \bar{\gamma}_W, \bar{\gamma}_Z \rangle_C = 0 \quad \text{for any causally separable pair } (W,Z).$$

Causally separable concepts are orthogonal by construction — a semantic constraint on the geometry, not an empirical observation.

**Explicit estimator.** Under Assumption 3.3 (a word sampled uniformly from the vocabulary expresses causally separable concepts independently), the causal inner product has the closed form:

$$\langle \bar{\gamma}, \bar{\gamma}' \rangle_C := \bar{\gamma}^\top \mathrm{Cov}(\gamma)^{-1} \bar{\gamma}', \qquad \forall\, \bar{\gamma}, \bar{\gamma}' \in \bar{\Gamma},$$

where $\mathrm{Cov}(\gamma)$ is the covariance of unembedding vectors drawn uniformly over the vocabulary. This is estimable directly from the unembedding matrix without any labelled data.

The Euclidean inner product ($M = I_d$) is a causal inner product only if $\mathrm{Cov}(\gamma)^{-1} \propto I_d$ — not guaranteed and typically false. Euclidean geometry on representation space is generically wrong.

**Practical steering vector.** The embedding representation is recovered from the unembedding representation via:

$$\bar{\lambda}_W := \mathrm{Cov}(\gamma)^{-1} \bar{\gamma}_W.$$

In the transformed space with $A = M^{1/2}$, the Euclidean inner product coincides with the causal inner product, and $\bar{g}_W = \bar{l}_W$ — the two representations collapse to the same object.

## Claims

**Theorem 2.2 (Measurement).** Let $\bar{\gamma}_W$ be the unembedding representation of $W$. Then for any context embedding $\lambda \in \Lambda$:

$$\mathrm{logit}\; P\!\bigl(Y = Y(1) \mid Y \in \{Y(0),Y(1)\},\, \lambda\bigr) = \alpha\, \lambda^\top \bar{\gamma}_W,$$

where $\alpha > 0$ (a.s.) depends on the particular counterfactual pair $\{Y(0),Y(1)\}$ but not on $\lambda$. The unembedding representation is the ideal linear probe direction: it predicts concept membership on the logit scale and does not absorb spurious correlations with causally separable concepts.

**Lemma 2.4 (Duality).** Let $\bar{\lambda}_W$ be the embedding representation of $W$, and let $\bar{\gamma}_W$, $\bar{\gamma}_Z$ be the unembedding representations of $W$ and any causally separable $Z$. Then:

$$\bar{\lambda}_W^\top \bar{\gamma}_W > 0 \qquad \text{and} \qquad \bar{\lambda}_W^\top \bar{\gamma}_Z = 0.$$

The embedding direction is the dual of the unembedding direction under the LM's bilinear form. Conversely, any $\bar{\lambda}_W$ satisfying these conditions (given a spanning set of separable concepts) is the embedding representation of $W$.

**Theorem 2.5 (Intervention).** Let $\bar{\lambda}_W$ be the embedding representation of $W$, and let $Z$ be causally separable from $W$. Then:

$$P\!\bigl(Y = Y(W,1) \mid Y \in \{Y(W,0),Y(W,1)\},\; \lambda + c\bar{\lambda}_W\bigr) \text{ is \emph{increasing} in } c,$$
$$P\!\bigl(Y = Y(1,Z) \mid Y \in \{Y(0,Z),Y(1,Z)\},\; \lambda + c\bar{\lambda}_W\bigr) \text{ is \emph{constant} in } c.$$

Adding $\bar{\lambda}_W$ to the context embedding increases $P(W=1)$ while leaving every causally separable concept unchanged. This is the formal justification for linear steering vectors.

**Theorem 3.2 (Unification).** Suppose for any concept $W$ there exist $d-1$ mutually causally separable concepts $\{Z_i\}$ whose unembedding representations together with $\bar{\gamma}_W$ span $\mathbb{R}^d$. Under a causal inner product, the Riesz isomorphism

$$\bar{\gamma} \;\mapsto\; \langle \bar{\gamma}_W, \cdot \rangle_C$$

maps each unembedding representation $\bar{\gamma}_W$ to its embedding representation $\bar{\lambda}_W$:

$$\langle \bar{\gamma}_W, \cdot \rangle_C = \bar{\lambda}_W^\top.$$

Probes and steering vectors are the same object, built from the same counterfactual mean — no separate probe-training step is needed.

**Theorem 3.4 (Explicit causal inner product).** Under Assumption 3.3, if $\langle\cdot,\cdot\rangle_C = \bar{\gamma}^\top M \bar{\gamma}'$ and concept directions $G = [\bar{\gamma}_{W_1},\ldots,\bar{\gamma}_{W_d}]$ form a basis, then:

$$M^{-1} = GG^\top \qquad \text{and} \qquad G^\top \mathrm{Cov}(\gamma)^{-1} G = D,$$

for some diagonal $D$ with positive entries. Choosing $D = I_d$ gives $M = \mathrm{Cov}(\gamma)^{-1}$ and the closed-form estimator in (3.3). The $d$ diagonal degrees of freedom in $D$ are unconstrained by causal orthogonality — the inner product is not unique, but Euclidean is ruled out unless $\mathrm{Cov}(\gamma)^{-1} \propto I_d$.

## Strengths

- **First causal, counterfactual-grounded formalisation.** Previous treatments of the LRH were either empirical analogies (Mikolov-style arithmetic) or informal claims. Park et al. ground every definition in a causal model, giving the hypothesis genuine theoretical content.
- **Unification.** Subspace, measurement (probing), and intervention (steering) notions were previously treated as distinct or even competing. Theorems 2.2, 2.5, and 3.2 show they are three views of the same object.
- **Tractable geometry.** The causal inner product is estimable from the unembedding matrix alone — no labelled pairs, no probe training, no access to internals beyond the final projection layer.
- **Euclidean geometry is ruled out.** The framework gives a principled reason why cosine similarity and Euclidean projection on raw activations are unreliable, and provides a substitute.
- **Empirical validation.** Tested on LLaMA-2-7B across 27 concepts (morphological, semantic, language-pair). Counterfactual pairs align with the estimated concept direction; concept directions act as probes; steering vectors shift only the target concept.

## Weaknesses

- **Binary concepts only.** The formal framework handles $W \in \{0,1\}$. Multi-valued or continuous concepts (e.g., degree of formality, numeric magnitude) are not treated.
- **Assumption 3.3 is post-hoc verified.** The vocabulary-level causal independence assumption is checked empirically for the 27 test concepts but is not guaranteed for arbitrary correlated semantic axes.
- **Non-unique inner product.** The free diagonal $D$ means the causal inner product is a class, not a single object. The choice $D = I_d$ is adopted for tractability with no principled motivation — a different $D$ could yield different orthogonality structure.
- **Decoder-only, single layer.** Experiments use LLaMA-2-7B with representations taken from the final layer before the unembedding projection. Cross-layer interactions, encoder models, and cross-attention are untreated.
- **Empirical exceptions.** The concept thing$\Rightarrow$part fails the linear representation test — not every semantically plausible concept has a direction.

## Relevance to this wiki's project

This paper is the load-bearing theory anchor for the decoding-time-steering theme, and connects to the project's central question at three joints:

1. **Formal warrant for $R_w$.** The project's proposed method posits a representation $R_w$ for a concept $W$ that can be added to context to steer output. Theorem 2.5 is the exact formal statement that this is possible without disturbing causally separable concepts. The single-sample challenge is whether one counterfactual pair yields a reliable estimate of $\bar{\gamma}_W$, and whether the Riesz map reliably recovers $\bar{\lambda}_W = \mathrm{Cov}(\gamma)^{-1}\bar{\gamma}_W$.

2. **Concept axes for concept-learning.** The CBM concept axis is formally $\bar{\gamma}_W$ under Definition 2.1. RCE subspaces are multi-dimensional extensions of the same cone structure. Park provides the axiomatic ground floor.

3. **Bridge to ICL-Bayesian inference.** The posterior sufficient statistic $\lambda(x)^\top \bar{\gamma}_W$ (Theorem 2.2) is the algebraic bridge between Bayesian ICL and activation geometry — the same linear functional that an in-context demonstration shifts is the one the Bayesian posterior tracks.

## Connections to the wiki

- [[../concept-learning/concept-bottleneck-models]] — CBM's named concept axes are $\bar{\gamma}_W$ under Definition 2.1; Park provides the axiomatic grounding CBM assumes.
- [[../concept-learning/recursive-concept-evolution]] — RCE subspaces extend the 1-d cone structure to multi-valued concept hierarchies; the causal inner product determines when two such subspaces are genuinely orthogonal.
- [[../concept-learning/_overview]]
- [[../in-context-learning-theory/icl-bayesian-inference]] — Theorem 2.2 shows the Bayesian posterior sufficient statistic is $\lambda(x)^\top \bar{\gamma}_W$; activation geometry and probabilistic ICL theory meet here.
- [[../synthesis/proposed-method]] — $R_w$ extension: Theorem 2.5 is the formal underpinning; single-sample estimation of $\bar{\gamma}_W$ is the open question.
- [[repe]] — Zou et al. (RepE) is the empirical framework; Park is the theory. RepE's "reading vectors" are empirical estimators of $\bar{\gamma}_W$.
- [[iti]] — Inference-Time Intervention's probe-identified directions are the measurement representation of Theorem 2.2; Park explains why ITI probes work.
- [[actadd]] — Activation Addition adds a single-pair difference vector; Park's Theorem 2.5 is the formal warrant for why this can shift a concept cleanly.
- [[caa]] — Contrastive Activation Addition averages mean-differences across many pairs; this is the sample-mean estimator of $\bar{\gamma}_W$ under Definition 2.1.
- [[contrastive-decoding]]
- [[cd-improves-reasoning]]
- [[dexperts]]
- [[gedi]]
- [[fudge]]
- [[pplm]]
- [[dola]]
- [[cfg-lm]]

## Related

- Mikolov et al. (2013) — word2vec analogy arithmetic; the empirical precursor to Definition 2.1.
- Elhage et al. (2022) — "Toy Models of Superposition"; the mechanistic interpretability context for LRH.
- Wang et al. (2023) — causal abstraction framework; Park adopts their latent-variable formalisation of concepts.
- Turner et al. (2023) — activation addition; empirical precursor to Theorem 2.5.
- Nanda et al. (2023) — linear probing; empirical precursor to Theorem 2.2.
