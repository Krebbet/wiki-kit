---
title: "FUDGE: Controlled Text Generation With Future Discriminators"
authors: "Kevin Yang, Dan Klein"
year: 2021
venue: "NAACL 2021"
arxiv: "2104.05218"
tags: [decoding-time-steering, classifier-guidance, bayesian-factorization, process-reward]
---

# FUDGE: Controlled Text Generation With Future Discriminators

FUDGE (Yang & Klein, 2021) steers a frozen generator $G$ toward a desired attribute $a$ by training a lightweight binary discriminator $B$ that operates on partial sequences. No gradient access to $G$ is required — only its output logits. The discriminator predicts future attribute satisfaction rather than present token-level fitness, which gives it a planning advantage over greedy reweighting schemes such as PPLM.

## Source

Yang, K., & Klein, D. (2021). FUDGE: Controlled Text Generation With Future Discriminators. *NAACL 2021*. arXiv:2104.05218.

## Method

At each decoding step $i$, FUDGE applies a Bayesian decomposition that exchanges $x_i$ and $a$ conditioned on the prefix $x_{1:i-1}$:

$$P(x_i \mid x_{1:i-1}, a) \;\propto\; P(a \mid x_{1:i}) \cdot P(x_i \mid x_{1:i-1})$$

$G$ supplies the prior $P(x_i \mid x_{1:i-1})$; discriminator $B$ supplies the likelihood update $P(a \mid x_{1:i})$. Products are computed in log-space and renormalised over the vocabulary. For efficiency, only the top-200 tokens from $G$ are evaluated per step. Multiple discriminators for independent attributes compose by summing their log-probabilities.

$B$ is trained on prefix-label pairs $(x_{1:i},\, a')$ derived from complete sequences: for each full example $(x_{1:n},\, a')$, every prefix $x_{1:i}$ becomes a training instance. This forces $B$ to predict whether $a$ will hold in the *completed* sequence, not just in the immediate next token.

## Claims

- **Couplet completion (Shakespeare sonnets, $n=154$):** FUDGE success 0.44 vs. fine-tune 0.21 vs. PPLM 0; diversity (Dist-1/2/3) comparable across methods.
- **Topic-controlled generation:** automated topic-success 0.59 (FUDGE) vs. 0.48 (PPLM) vs. 0.28 (fine-tune); human on-topic rating 78% vs. 45% (PPLM); fluency 4.30 vs. 4.05 (PPLM).
- **MT formality (English formal register):** BLEU 17.96 (FUDGE) vs. 16.98 (no-fine-tune baseline); style-transfer pipeline collapses to BLEU 7.87.
- **Speed:** ~15 min for 420 test generations on a single Quadro RTX 6000; PPLM requires hours for the same workload.
- **Data:** $B$ trained on $\sim10^7$ synthetic generations from $G$; cross-domain transfer demonstrated (formality discriminator generalises).

## Strengths

- **Future-oriented planning.** $B$ predicts attribute satisfaction of the *eventual* completion, not the next token. This allows FUDGE to choose sub-optimal local tokens (e.g., the adverb "pretty") that enable a strongly attribute-satisfying continuation later (e.g., rhyme word "clear" as the tenth syllable).
- **Principled derivation.** The per-step reweighting follows directly from Bayes' rule; no heuristic scaling of classifier gradients.
- **Model-agnostic, logits-only.** $G$ is fully frozen; only logit access is required, making FUDGE compatible with black-box or API-served generators that share tokenisation.
- **Modular composition.** Independent discriminators for distinct attributes compose by log-probability addition, requiring no joint training.

## Weaknesses

- **No hard guarantee.** Top-200 pruning and the approximation inherent in modelling $P(a \mid x_{1:i})$ mean outputs may not satisfy $a$.
- **Conditioning-strength scalar.** In practice, $B$'s log-probabilities are scaled by a hyperparameter $\lambda$ before adding to $G$'s logits; this violates the exact Bayesian factorisation.
- **Labelled attribute data required.** $B$ needs complete sequences annotated for $a$; few- or zero-shot scenarios are unaddressed.
- **Scale limited to GPT-2-Medium (345M).** Experiments do not test on larger generators; interactions between $B$ and larger $G$ are unknown.
- **Cold-start unaddressed.** When only one or a handful of labelled examples exist, training $B$ on $10^7$ generated prefixes is infeasible unless synthetic generation is tractable.

## Relevance to this wiki's project

FUDGE is a direct existence proof for the $R_w$ reward-at-inference strategy central to this wiki. It shows that a discriminator trained *once offline* can be deployed as a per-step Bayesian prior over $G$'s logits, steering generation toward a target concept without any weight update to $G$.

The partial-sequence discriminator $B$ is structurally identical to a *process reward model* applied token-by-token: it scores prefixes rather than complete outputs, bridging the PRM literature directly to decoding-time steering.

The Bayesian factorisation $P(x_i \mid x_{1:i-1}, a) \propto P(a \mid x_{1:i}) \cdot P(x_i \mid x_{1:i-1})$ is the token-level analogue of the ICL-Bayesian posterior argument: $G$ supplies the prior; $B$ supplies the likelihood update. This suggests training a concept-specific lightweight discriminator $B_c$ — possibly from synthetic prefixes generated around a single labelled example, mirroring FUDGE's $10^7$-generation protocol but at drastically reduced scale — as a single-sample-derived decoding-time prior.

## Connections to the wiki

- [[../process-reward-models/_overview]] — FUDGE's step-level discriminator IS structurally a process reward signal; direct bridge between PRM literature and decoding-time steering.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — FUDGE's top-200 pruning and sparse-selection both approximate the full reweighted distribution through truncation.
- [[../synthesis/proposed-method]] — $R_w$ existence proof; FUDGE's offline-train / inference-deploy split is the template.
- [[../in-context-learning-theory/icl-bayesian-inference]] — shared Bayesian factorisation structure at the token level.
- [[../concept-learning/_overview]] — concept-specific $B_c$ as a natural single-sample extension.

## Related

Within decoding-time-steering theme: [[pplm]] (FUDGE's direct ancestor — replaces gradient ascent through activations with a future-discriminator reweighting), [[gedi]] (CCLM-as-discriminator; different approximation, related Bayesian motivation), [[dexperts]] (contrastive expert/anti-expert logit arithmetic; no future-orientation), [[contrastive-decoding]], [[cd-improves-reasoning]], [[dola]], [[cfg-lm]], [[repe]], [[iti]], [[actadd]], [[caa]], [[linear-rep-hypothesis]].
