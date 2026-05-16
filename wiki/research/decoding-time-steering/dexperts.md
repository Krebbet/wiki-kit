---
name: DExperts
description: Decoding-time controlled text generation via product-of-experts over frozen base LM, expert LM, and anti-expert LM; logit-additive steering without any base model weight updates.
type: research
---

# DExperts: Decoding-Time Controlled Text Generation with Experts and Anti-Experts

Liu et al. (2021) steer a frozen base LM at inference time by additively combining its logits with those of a small fine-tuned "expert" and "anti-expert". No gradients flow into the base model; all steering lives in the output logit space. The method beats PPLM, DAPT, and GeDi on toxicity and sentiment benchmarks while remaining compatible with black-box APIs.

## Source

Alisa Liu, Maarten Sap, Ximing Lu, Swabha Swayamditta, Chandra Bhagavatula, Noah A. Smith, Yejin Choi. **DExperts: Decoding-Time Controlled Text Generation with Experts and Anti-Experts**. ACL 2021. [arXiv:2105.03023](https://arxiv.org/abs/2105.03023).

## Method

At each decoding step $t$, three frozen LMs — base $M$, expert $M^+$, anti-expert $M^-$ — each produce logit vectors $\mathbf{z}_t$, $\mathbf{z}^+_t$, $\mathbf{z}^-_t$ over the full vocabulary $V$. The DExperts distribution is

$$\tilde{P}(X_t \mid x_{<t}) = \text{softmax}\!\left(\mathbf{z}_t + \alpha\!\left(\mathbf{z}^+_t - \mathbf{z}^-_t\right)\right)$$

where $\alpha > 0$ is a hand-tuned control strength. Equivalently, in probability space:

$$\tilde{P}(X_t \mid x_{<t}) \propto P(X_t \mid x_{<t})\cdot\!\left(\frac{P^+(X_t \mid x_{<t})}{P^-(X_t \mid x_{<t})}\right)^{\!\alpha}$$

This is a product-of-experts (Hinton 2002): a token gains high weight only if $P$ and $P^+$ both approve and $P^-$ disapproves.

**Nucleus truncation.** Before combining, the base logits are truncated to the top-$k$/nucleus vocabulary $V' \subset V$:

$$\mathbf{z}'_t[v] = \begin{cases} \mathbf{z}_t[v] & v \in V' \\ -\infty & \text{otherwise} \end{cases}$$

Sampling is then from $\tilde{P}'(X_t \mid x_{<t}) = \text{softmax}(\mathbf{z}'_t + \alpha(\mathbf{z}^+_t - \mathbf{z}^-_t))$. The expert can rerank within $V'$ but cannot surface tokens the base model already suppressed.

**Anti-expert-only ablation.** Setting $\mathbf{z}^+_t = \mathbf{z}_t$ (reuse base as expert) gives:

$$\tilde{P}(X_t \mid x_{<t}) = \text{softmax}\!\left((1+\alpha)\mathbf{z}_t - \alpha\mathbf{z}^-_t\right)$$

No positive-class training data required.

## Claims

- Toxicity (avg. max.) 0.302, toxicity probability 0.118 on RealToxicityPrompts (GPT-2-Large base, $\alpha=2$) — lowest across all reported systems including PPLM, DAPT, and GeDi.
- Anti-expert-only ablation (0.352 / 0.191) still outperforms every baseline; negative-class data suffices.
- ~650 toxic comments (~40K tokens, ~3 min GPU fine-tuning) are enough to match GeDi, opening the door to easily customizable anti-experts.
- Transfers to black-box GPT-3 via the top-100 logprobs API: toxicity probability drops from 0.525 to 0.293.
- Human preference 62–78% over baselines on adversarial counter-prompt sentiment steering (negative prompts → positive continuations and vice versa).
- Expert/anti-expert sizes can be smaller than the base model with negligible quality loss; a GPT-2 Small expert steers GPT-2 Large effectively.

## Strengths / Novelty

- **Modularity.** Expert and anti-expert are interchangeable plug-ins; swapping the pair changes the steered attribute with no base model modification.
- **Strict forward-pass cost.** One additional forward pass per (anti-)expert per step — versus PPLM's ~30× slower backward pass through the base model.
- **Asymmetric steering.** Anti-expert lets you steer *away* from an attribute without labeled positive examples, which pure fine-tuning cannot do as cleanly.
- **API compatibility.** Operates on logits/logprobs only; demonstrated on GPT-3 via API top-100 logprobs.
- **Bayesian interpretation.** The logit-additive combination is equivalent to reweighting the base posterior by $(P^+/P^-)^\alpha$, making the probabilistic semantics transparent.

## Weaknesses / Limits

- **Nucleus truncation = Invisible Leash.** The expert cannot recover tokens the base model suppresses ($v \notin V'$). Steering is confined to the base model's already-probable set, analogous to the 0%-shifted-outside-base-top-5 finding (see Connections).
- **$\alpha$ requires hand-tuning.** No adaptive schedule; the fluency–control tradeoff must be empirically swept per task and base model.
- **In-domain expert training.** Experts must be fine-tuned on text from the same domain as the base model's pretraining distribution for effective contrast (noted explicitly for the non-toxic expert).
- **Attribute steering only.** The method shifts probability mass within an attribute dimension but cannot inject new conceptual content not already latent in the base model.
- **Parallel overhead.** Two extra forward passes per step (expert + anti-expert) add wall-clock latency, though far less than PPLM.

## Relevance to this wiki's project

DExperts is the clearest prior-art instantiation of the proposed method's offline-reweight design ($R_w$): a small specialist LM acts as a logit-additive prior over the base model's distribution, with zero weight updates to the base. The nucleus-truncation constraint (Eq. 5) is the decoding-time analogue of the Invisible Leash Theorem (C.1) — the expert cannot surface tokens the base assigns ~0 probability, which is exactly the 0%-shifted-outside-base-top-5 bound. The ~650-comment anti-expert result directly supports the few-sample concept-installation thesis: a handful of targeted examples suffices to mount an effective logit-space prior. Under the Bayesian reading ($\tilde{P} \propto P_\text{base} \cdot (P^+/P^-)^\alpha$), DExperts is posterior reweighting with a ratio likelihood, a structural parallel to the proposed method's reweight operator.

## Connections to the wiki

- [[../synthesis/proposed-method]] — $R_w$ offline-reweight design; DExperts is the closest prior-art instantiation.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — 0%-outside-top-5 analogue; nucleus-truncation is the decoding-time version of the Invisible Leash.
- [[../synthesis/single-sample-concept-skeleton]] — 650-comment few-sample result motivates single-sample anti-expert installation.
- [[../in-context-learning-theory/icl-bayesian-inference]] — PoE form ($\tilde{P} \propto P_\text{base} \cdot (P^+/P^-)^\alpha$) is a Bayesian posterior reweight.
- [[../concept-learning/_overview]] — logit-delta $(\mathbf{z}^+_t - \mathbf{z}^-_t)$ is a logit-space analogue of concept-as-direction steering.

## Related

- [[gedi]] — sibling: Bayes-rule class-conditioned LM; similar product-of-experts spirit, different formulation.
- [[pplm]] — direct ancestor; gradient-based hidden-state perturbation; ~30× slower, same goal.
- [[contrastive-decoding]] — contrasts strong vs. weak LM logits; DExperts generalises to attribute axes.
- [[cd-improves-reasoning]] — contrastive decoding applied to reasoning; related logit-subtraction mechanics.
- [[fudge]] — future-discriminator guidance; complements DExperts' current-step logit steering.
- [[cfg-lm]] — classifier-free guidance adapted to LMs; logit-additive form closely related to DExperts.
- [[repe]] — representation engineering; steers in activation space rather than logit space.
- [[iti]] — inference-time intervention; activation-space complement to logit-space DExperts.
- [[actadd]] — activation addition; additive steering in residual stream vs. output logits.
- [[caa]] — contrastive activation addition; same activation-space lineage.
- [[linear-rep-hypothesis]] — theoretical grounding for why logit/activation directions carry attribute information.
- [[dola]] — dynamic layer-contrast decoding; different contrastive axis (layers), same decoding-time family.
