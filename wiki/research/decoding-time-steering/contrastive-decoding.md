---
name: contrastive-decoding
description: Training-free decoding that subtracts amateur log-probs from expert log-probs inside a plausibility gate, surfacing concept-specific signal without weight updates.
type: research
---

# Contrastive Decoding: Open-ended Text Generation as Optimization

Li et al. (2022; arXiv:2210.15097) — Stanford, UW, CMU, JHU, FAIR. The method pairs a frozen large expert (e.g., OPT-13B) with a frozen small amateur (e.g., OPT-125M) and, at each decoding step, scores surviving tokens by $\log p_\text{EXP} - \log p_\text{AMA}$ inside a plausibility gate; beam search over this objective yields text that amplifies expert-specific knowledge while suppressing shared failure modes (repetition, incoherence). Zero additional training required. CD outperforms nucleus, top-k, typical, and contrastive search on MAUVE and coherence across Wikipedia, Wikinews, and BookCorpus domains, and is preferred by human raters over nucleus 2.6× on coherence and 1.4× on fluency. For this wiki it is the canonical operationalisation of $R_w$: expert contains target behavior, amateur encodes the baseline prior, and their difference surfaces the concept-specific signal at inference time.

## Source
- arXiv: 2210.15097
- Raw markdown: `raw/research/decoding-time-steering/03-01-contrastive-decoding.md`

## Method

**Plausibility gate.** At position $i$, restrict the vocabulary to tokens that survive the expert's soft plausibility filter:

$$V_\text{head}(x_{<i}) = \{ x_i \in V : p_\text{EXP}(x_i \mid x_{<i}) \geq \alpha \cdot \max_w\, p_\text{EXP}(w \mid x_{<i}) \}$$

with default $\alpha = 0.1$. Tokens scoring less than 10 % of the expert's mode are excluded. Removing this gate collapses MAUVE to 0.01 (Table 4) — the constraint is load-bearing, not cosmetic.

**CD objective.** Among surviving tokens, select by the contrastive log-ratio:

$$\mathcal{L}_\text{CD}(x_i \mid x_{<i}) = \log p_\text{EXP}(x_i \mid x_{<i}) - \log p_\text{AMA}(x_i \mid x_{<i})$$

Beam search is run over this objective (CD-search); a sampling variant (CD-sampling) also exists and exceeds standard baselines but falls short of CD-search on fluency and coherence. Both models are completely frozen — no gradient computation.

**Intuition.** Expert and amateur share failure modes (repetition, generic tokens); the difference cancels them out. Expert-specific knowledge (rare facts, precise continuations) has high $p_\text{EXP}$ and low $p_\text{AMA}$, so the difference amplifies exactly these tokens. The paper frames this as a pragmatic-communication model: the amateur acts as an informed-listener prior, and the expert communicates what the amateur cannot already predict.

## Claims

- CD beats nucleus, top-k, typical decoding, and contrastive search on MAUVE and coherence at 1.5B and 13B scale across Wikipedia, Wikinews, and BookCorpus (Table 1).
- Human raters prefer CD over nucleus 2.6× on coherence, 1.4× on fluency (Table 2).
- Larger expert–amateur scale gap monotonically improves quality (Figure 2); the gap itself is the signal source.
- Removing the plausibility constraint ($V_\text{head}$) collapses MAUVE to 0.01 (Table 4) — load-bearing.
- CD-sampling beats standard baselines but is weaker than CD-search on fluency and coherence.

## Strengths / Novelty

First principled training-free decoding objective formulated as an explicit optimisation problem over a logit difference. Prior contrastive methods (DExperts, PPLM) required either finetuned attribute models or gradient-based generation; CD needs only two off-the-shelf models of different sizes. The pragmatic-communication derivation gives the approach a grounded theoretical interpretation beyond the empirical "subtract small from large" intuition.

The plausibility gate design is non-trivial: it avoids the low-probability garbage tokens that would otherwise receive high contrastive scores (large $-\log p_\text{AMA}$ denominated by near-zero $p_\text{EXP}$), making the objective robust without extra hyperparameters beyond $\alpha$.

## Weaknesses / Limits

Designed and evaluated for open-ended generation; does not address reasoning, math, or instruction following in this paper — that extension is the sibling O'Brien et al. 2023 ([[cd-improves-reasoning]]). The second model inference pass imposes latency proportional to amateur forward passes per step. Empirical improvements are tightest when expert and amateur are from the same model family (same tokenizer, compatible probability spaces); cross-family amateur pairings are untested. Operates at the token level only — no compositional or structured concept steering across a generation.

## Relevance to this wiki's project

**$R_w$ operationalisation.** CD is the cleanest existing instantiation of the hypothesis that concept-specific signal lives in the *difference* between a model that has acquired a concept and one that has not. Expert = post-concept model; amateur = pre-concept baseline; the logit difference is $R_w$ made computational. This directly motivates decode-time steering as a zero-weight-update path to single-sample concept injection.

**Invisible Leash Theorem C.1.** The $V_\text{head}$ gate enforces the same support-inclusion constraint as Theorem C.1 of [[../self-play/invisible-leash]]: tokens outside the expert's high-probability region are excluded, exactly as any policy gradient method stays within the support of the base model. CD operationalises this constraint at decode time rather than at training time.

**BOLT coverage wall.** The CD objective amplifies low-but-nonzero expert probabilities — the paper's "1961" example has $p_\text{EXP} \approx 0.1$ but is the correct completion. RLVR would under-reinforce this token because coverage-wall effects (Theorem 7 of [[../rl-optimizers/bolt-kl-rlvr-boltzmann]]) bound one-shot reinforcement to the reference pass-rate regime. CD bypasses the coverage wall entirely: no training, no pass-rate dependence.

**Rethinking-RL 0%-shifted finding.** The contrastive mechanism is consistent with [[../rlvr-mechanics/rethinking-rl-sparse-selection]]'s observation that RLVR shifts zero probability mass outside the base model's top-5 support. CD works *within* that support but reweights it — demonstrating that the base distribution already contains the target behavior and that extraction, not expansion, is the operative step.

**ICL-Bayesian posterior.** The amateur-as-prior framing maps onto [[../in-context-learning-theory/icl-bayesian-inference]]: the expert's in-context posterior minus the amateur's prior isolates the concept-specific likelihood update, exactly as Bayesian ICL characterises in-context learning as prior correction.

## Connections to the wiki

- **[[../synthesis/proposed-method]]** — CD's logit-difference is the decode-time analogue of the proposed method's concept-signal extraction; the $V_\text{head}$ gate formalises the support constraint the proposed method inherits.
- **[[../rlvr-mechanics/rethinking-rl-sparse-selection]]** — 0%-shifted-outside-base-top-5 finding: CD reweights within existing support rather than expanding it, validating extraction over expansion.
- **[[../rl-optimizers/bolt-kl-rlvr-boltzmann]]** — BOLT's coverage-wall (Theorem 6/7) is what CD sidesteps; CD demonstrates extraction of rare-but-correct tokens that RLVR would miss at $N=1$.
- **[[../self-play/invisible-leash]]** — $V_\text{head}$ is Theorem C.1's support constraint operationalised at the decode step.
- **[[../in-context-learning-theory/icl-bayesian-inference]]** — amateur-as-prior / expert-as-posterior maps directly onto the Bayesian ICL framing of in-context learning.
- **[[../concept-learning/_overview]]** — CD provides a token-level mechanism for surfacing concept-specific signal; cross-reference for the concept-extraction thread.
- **[[cd-improves-reasoning]]** — direct extension of CD to reasoning and math tasks (O'Brien et al. 2023); the sibling page in this theme.
- **[[dexperts]]** — product-of-experts cousin; uses finetuned attribute LMs rather than scale contrast.
- **[[dola]]** — layer-contrastive sibling; contrasts early vs. late transformer layers within one model rather than two separate models.
- **[[cfg-lm]]** — classifier-free guidance analogue; conditioning direction rather than model-size contrast.

## Related

- [[cd-improves-reasoning]]
- [[dexperts]]
- [[dola]]
- [[cfg-lm]]
- [[gedi]]
- [[fudge]]
- [[pplm]]
- [[repe]]
- [[iti]]
- [[actadd]]
- [[caa]]
- [[linear-rep-hypothesis]]
- [[../synthesis/proposed-method]]
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]]
- [[../self-play/invisible-leash]]
- [[../in-context-learning-theory/icl-bayesian-inference]]
- [[../concept-learning/_overview]]
