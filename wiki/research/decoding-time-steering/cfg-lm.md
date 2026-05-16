---
name: cfg-lm
description: Ports diffusion's classifier-free guidance to autoregressive LMs via two forward passes per step — conditional and unconditional — extrapolating logits in the conditioning direction; no fine-tuning required. Achieves LAMBADA SoTA with LLaMA-7B over PaLM-540B at γ=1.5.
type: research
---

# Stay on Topic with Classifier-Free Guidance

Sanchez et al. (2023; arXiv:2306.17806) — EleutherAI / University of Geneva / USC / IIIT Hyderabad / Hexaglobe. CFG, born in text-to-image diffusion, transfers cleanly to autoregressive language models: run two forward passes per decoding step (one conditioned on the prompt, one with the prompt stripped), then extrapolate the logit distribution in the conditioning direction by guidance strength $\gamma$. Because decoder-only LMs handle both $P(w \mid c)$ and $P(w)$ natively via their finite context window, no conditioning-dropout training — required for diffusion — is needed. The result is a zero-training, architecture-agnostic knob that amplifies prompt adherence at inference time and composes with Chain-of-Thought and Self-Consistency.

## Source

- arXiv: 2306.17806
- Raw markdown: `raw/research/decoding-time-steering/06-07-cfg-lm.md`

## Method

At each decoding step $i$, the guided log-probability is:

$$\log \tilde{P}_\theta(w_i \mid w_{<i}, c) = \log P_\theta(w_i \mid w_{<i}) + \gamma\bigl(\log P_\theta(w_i \mid w_{<i}, c) - \log P_\theta(w_i \mid w_{<i})\bigr)$$

- $\gamma = 0$: unconditional generation.
- $\gamma = 1$: standard conditional generation.
- $\gamma > 1$: extrapolation past the conditional — overemphasises prompt.

The unconditional pass drops the prompt prefix; a "negative prompt" $\bar{c}$ can substitute for the unconditional baseline, allowing repulsion from an undesired style or topic. Logit-space operation keeps the method architecture-agnostic and avoids hidden-state surgery.

## Claims

- LAMBADA zero-shot: LLaMA-7B + CFG ($\gamma=1.5$) = 81.3%, beating PaLM-540B (77.9%), Chinchilla-70B, and GPT-3 175B (state-of-the-art as of June 2023).
- CFG $\approx$ doubling parameter count: on 5 of 9 zero-shot tasks the difference between CFG and a 2× larger baseline is statistically insignificant (ANCOVA $p=.01$); CFG outright wins on 2 tasks.
- Consistent gains across GPT-2, Pythia 160M–12B, and LLaMA 7B–65B on BoolQ, HellaSwag, PIQA, SCIQ, TriviaQA, and LAMBADA at $\gamma=1.5$; ARC-Challenge and Winogrande show mixed or negative results (cause unknown).
- Low $\gamma$ ($\leq 1.5$) increases parseable-answer rate on GSM8K / AQuA CoT; high $\gamma$ degrades chain quality.
- Human evaluation: 75% preference for GPT4All-J with CFG ($\gamma=3$) over vanilla sampling on assistant adherence (611 votes, blind evaluation).

## Strengths

- Zero training, zero weight update — pure inference-time intervention.
- Architecture-agnostic: operates on logits, no hidden-state editing required.
- Exploits a natural feature of decoder-only LMs: dropping the prompt prefix trivially yields the unconditional distribution.
- Composes with CoT and Self-Consistency; both stack and yield further gains on hard tasks.
- Negative prompting supported out-of-the-box via generalized equation.
- Interpretability: per-token $\log P(w_t \mid c) - \log P(w_t)$ visualises which tokens the prompt is activating.
- Entropy analysis provides a mechanistic foothold: CFG reaches instruction-tuned output entropy via vocabulary re-ranking, with ~50% top-$p$ overlap.

## Weaknesses

- Doubles inference FLOPs (two full forward passes per step); not free at serving scale.
- ARC-Challenge and Winogrande gains are inconsistent or negative; no account offered.
- High $\gamma$ degrades diversity and hurts pass@k in generation tasks.
- Sensitive to where the prompt/continuation boundary is defined; edge cases (no explicit prompt, chat-history prefixes) require care.
- No theoretical justification for why the conditional–unconditional direction is the right axis; the paper is empirical throughout.

## Relevance to this wiki's project

Direct proof-of-concept for $R_w$: no weight update, no fine-tuning, no external classifier needed to amplify a target behaviour. The "reward signal" is the model's own logit difference between conditional and unconditional passes — an internal re-weighting of the reference distribution in response to a single prompt, exactly the spirit of single-sample steering.

Structural parallel to BOLT: BOLT's KL-regularised target $\pi^* \propto \pi_\text{ref}\exp(r/\beta)$ is a Boltzmann tilt of the base distribution; CFG instantiates the same tilt where the tilt direction is $\gamma(\log P(w \mid c) - \log P(w))$. Both are multiplicative re-weightings of a reference; neither requires retraining. CFG thus shows the tilt structure is sufficient for non-trivial capability gains without any gradient flow.

Relation to ICL-Bayesian: CFG goes further than a soft posterior update — it extrapolates past the conditional, closer to amortised MAP inference than Bayesian posterior integration.

Warm-start / baseline candidate: CFG at $\gamma=1.5$ is a strong zero-training baseline against which any single-sample fine-tuning method (e.g., 1-shot RLVR) should be compared before claiming benefit from weight updates.

## Connections to the wiki

- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] — structural isomorphism: both are multiplicative tilts of a reference distribution; BOLT uses a learned reward, CFG uses the conditioning direction.
- [[../in-context-learning-theory/icl-bayesian-inference]] — CFG hard-extrapolates past the Bayesian posterior rather than softly updating it.
- [[../synthesis/proposed-method]] — $R_w$ existence proof; strongest zero-training comparator.
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — weight-free baseline / warm-start candidate for single-sample RLVR experiments.
- [[../self-play/invisible-leash]] — CFG instantiates the invisible-leash mechanism: the prompt-direction delta acts as a leash without an explicit constraint term.
- [[contrastive-decoding]] — extrapolation cousin; CD subtracts amateur log-probs inside a plausibility gate, CFG subtracts unconditional log-probs without a gate.

## Related

- [[contrastive-decoding]]
- [[dexperts]]
- [[cd-improves-reasoning]]
- [[dola]]
- [[gedi]]
- [[fudge]]
- [[pplm]]
- [[repe]]
- [[iti]]
- [[actadd]]
- [[caa]]
- [[linear-rep-hypothesis]]
