---
name: decoding-time-steering-overview
description: Theme overview — decoding-time and activation-steering methods that shift LLM outputs without weight updates. Thirteen primary mechanisms across logit-space reweighting, residual-stream activation editing, and the formal linear-representation theory that unifies them. Cross-theme empirical/mechanistic backbone for the R_w hypothesis in proposed-method.
type: research
---

# Decoding-time and activation-steering methods

Decoding-time and activation-steering methods modify an LLM's output distribution **without any gradient update to the base model's weights**. Two interventions points dominate: at the logit layer (subtract or extrapolate logits from a contrast model / classifier / layer / prompt), or at the residual-stream activations (add a direction extracted from contrast examples). The thirteen captures in this theme cover a four-year arc — PPLM 2019 through Park-Veitch 2024 — that consistently demonstrates the same mechanistic claim: **the relevant information is already in the base model; an offline reweighting prior suffices to put the model into the right solution space**.

This is the empirical / methodological / theoretical backbone of the **R_w extension** to [[../synthesis/proposed-method]] (added 2026-05-12). Every page in this theme provides direct support; none contradicts.

## Subtrees

### Logit-level reweighting

Operate at the output projection — adjust next-token logits via a contrast model, classifier gradient, layer difference, or conditioning extrapolation. The base model's forward pass is unchanged; an additive logit term is composed in at decode time.

| Page | Mechanism | Data / access |
|---|---|---|
| [[pplm]] | Tiny attribute classifier ($\sim$1K params) gradients pushed into key-value cache; 3–10 backward passes per token | BoW or 1-layer discriminator; gradient access to base |
| [[gedi]] | Small class-conditional LM scores all $\|V\|$ candidates via Bayes-rule $P_w \propto P_\text{LM} \cdot P_\theta(c)^\omega$; two forward passes | CC-LM trained on attribute labels; logit access |
| [[fudge]] | Future-discriminator $B$ predicts whether attribute will be satisfied; per-step Bayesian factor $P(a\|x_{1:i}) \cdot P(x_i\|x_{1:i-1})$ | Discriminator on $10^7$ generations; logit access |
| [[dexperts]] | Product-of-experts: $\mathbf{z}_t + \alpha(\mathbf{z}^+_t - \mathbf{z}^-_t)$; small (anti-)experts steer frozen base | $\sim$650 in-domain examples; logit / top-100 API |
| [[contrastive-decoding]] | Large/small logit difference + $\alpha$-plausibility gate $V_\text{head}$ | Two frozen LMs (same family); training-free |
| [[cd-improves-reasoning]] | CD parameterised as $(1+\beta) s^{(e)} - \beta s^{(a)}$; works for math/reasoning | Same family expert + amateur; +8.1pp GSM8K |
| [[dola]] | **Single-model** layer-contrastive: late-layer logits − dynamically-selected early-layer logits | One model; +12–17pp TruthfulQA |
| [[cfg-lm]] | Conditional/unconditional extrapolation $\log P(w\|c) + \gamma(\log P(w\|c) - \log P(w))$ | Same model two passes; LAMBADA SoTA at 7B |

### Activation-level steering

Operate on the residual stream — extract a direction from paired contrast examples, then add it (with a coefficient) to activations at chosen layers. No forward-pass logit composition; the intervention lives inside the network.

| Page | Mechanism | Data floor |
|---|---|---|
| [[actadd]] | Single contrast pair $\mathbf{h}_+^{[l]} - \mathbf{h}_-^{[l]}$; injected as $\mathbf{h}^{[l]} \leftarrow \mathbf{h}^{[l]} + c \cdot \mathbf{h}_A^{[l]}$ | **2 prompts** — the absolute data-efficiency floor of the family |
| [[caa]] | ActAdd averaged over hundreds of (positive, negative) example pairs | $\sim$hundreds of A/B contrast items |
| [[iti]] | Linear probes per attention head + top-$K$ selection; head-output shift $\alpha \sigma_l^h \theta_l^h$; equivalent bias-bake | $\sim$40–81 contrast pairs; **40% probe–generation gap** |
| [[repe]] | **Umbrella framework**: LAT scan → reading vector → linear / piecewise / projection-erasure control, or LoRRA fine-tune | 5–128 contrast pairs; explicit umbrella for ITI / ActAdd / CAA |

### Theory anchor

| Page | Contribution |
|---|---|
| [[linear-rep-hypothesis]] | First causal-counterfactual formalisation of "concept = direction"; Theorem 2.2 (probe direction = unembedding rep), Theorem 2.5 (intervention = additive embedding rep), Theorem 3.2 (causal inner product unifies probing and steering via Riesz isomorphism) |

**Park is the theory; Zou (RepE) is the framework; ITI / ActAdd / CAA / DoLa / CD / CFG are concrete instances** — each shows a specific empirical realisation of Park's Theorem 2.5 ("adding the embedding representation to context shifts the concept without disturbing causally-separable concepts").

## Cross-cutting findings

### The unanimous "info is in there" claim

All 13 captures support the same mechanistic claim. There is no disagreement on this axis across the four-year arc:

| Source | What it shows |
|---|---|
| [[iti]] | **~40% probe–generation gap** on LLaMA-7B TruthfulQA — model "knows" far more than it outputs |
| [[repe]] | LAT reading direction outperforms few-shot prompting on 5 QA benchmarks — *reading the model* beats *prompting the model* |
| [[contrastive-decoding]], [[cd-improves-reasoning]] | $V_\text{head}$ gate (plausibility mask within expert's top mass) is load-bearing; tokens are not pulled from the tail |
| [[dola]] | Layer-contrast surfaces factual knowledge **without any external model** — the contrast signal is intrinsic |
| [[cfg-lm]] | Conditional/unconditional logit difference recovers $\sim$2× parameter-count equivalent benefit; no training |
| [[actadd]], [[caa]] | Steering vectors from base-model contrast pairs transfer to RLHF chat models — concept directions exist pre-training |
| [[linear-rep-hypothesis]] | **Formal proof** (Theorem 2.5): adding the embedding direction increases concept probability while leaving causally-separable concepts unchanged |

### Connection to existing wiki anchors

- **[[../synthesis/proposed-method]] R_w extension (2026-05-12).** This theme is the empirical / theoretical backbone for R_w. ITI, RepE, DoLa, CD-for-Reasoning, CFG, and Linear-Rep Hypothesis are the primary anchors.
- **[[../rlvr-mechanics/rethinking-rl-sparse-selection]].** The 0%-shifted-outside-base-top-5 finding is the RLVR token-level analogue of what this theme shows at decode time. REASONMAXXER's rank-8 $W_O$ LoRA (0.04% params) is the logit-space analogue of ITI's head-level intervention. CD's $\alpha$-mask, DEXPERTS' nucleus-truncation, and CFG's extrapolation all enforce the same support-inclusion constraint at decode time rather than at training time.
- **[[../rl-optimizers/bolt-kl-rlvr-boltzmann]].** BOLT's KL-RLVR target $\pi^* \propto \pi_\text{ref}\exp(r/\beta)$ is structurally a multiplicative reweighting of a reference. CFG (conditioning-direction) and CD (amateur-direction) realise the same multiplicative-reweighting structure at decode time without a reward.
- **[[../self-play/invisible-leash]].** Theorem C.1 (support inclusion under on-policy gradient) holds **by construction** for every method in this theme — none use gradient updates, none move outside base support. ActAdd is the cleanest existence proof.
- **[[../concept-learning/_overview]].** CBM (concept-as-axis) and RCE (concept-as-subspace) are the wiki's pre-existing concept-as-direction lineage; Park's Theorem 2.2 + RepE's LAT make this formal at the activation level.
- **[[../in-context-learning-theory/icl-bayesian-inference]].** The Bayesian-posterior framing of ICL has a parametric realisation in GeDi ($P_w \propto P_\text{LM} \cdot P_\theta(c)^\omega$) and FUDGE (per-step factorisation), and a geometric realisation in Park's Theorem 2.2 ($\text{logit}\,P = \alpha \lambda^\top \bar\gamma_W$).
- **[[../single-sample-rl-finetuning/_overview]].** ActAdd at $n=1$ contrast pair is the activation-level single-sample method; complements the weight-level single-sample family (1-shot RLVR, critique-FT-one-problem).

### Where each method sits in the data-efficiency landscape

| Data floor | Method | Notes |
|---|---|---|
| **2 prompts** | ActAdd | Single contrast pair; no labels needed |
| **5–128 pairs** | RepE LAT, CAA | Averaging reduces noise |
| **40–81 pairs** | ITI | Linear probes per head |
| **~650 examples** | DEXPERTS | Anti-expert from in-domain text |
| **0** (training-free) | CD, CD-Reasoning, DoLa, CFG | No labelled data; logit-level only |
| **$10^7$ generations** | FUDGE | Discriminator on synthetic prefixes |
| **Task-specific corpus** | GeDi, PPLM | Class-conditional LM / attribute classifier |

For the wiki's single-sample frame, ActAdd is the strict floor and CD / DoLa / CFG are the zero-training existence proofs.

## Cross-cutting open questions

1. **Does the single-pair vector ([[actadd]]) reliably approximate the averaged-pair vector ([[caa]]) for non-toy concepts?** Critical for single-sample feasibility.
2. **Can layer-contrastive ([[dola]]) decoding be conditioned on a *concept-injection layer* vs *pre-injection layer*, to amplify newly installed content specifically?** Speculative R_w-installation extension.
3. **Do model-contrastive ([[contrastive-decoding]]) and layer-contrastive ([[dola]]) compose, or do they double-count the same residual?** Untested in any captured paper.
4. **Can a single counterfactual pair reliably estimate $\bar{\gamma}_W$ under [[linear-rep-hypothesis]]'s framework, or does the LOO-mean estimator require $n \gg 1$?** Park doesn't address the $n=1$ limit; ActAdd's empirical success suggests yes for some concepts, but not formally established.
5. **Does the base-to-chat transfer of [[caa]] hold for concepts learned only during RLHF?** Untested.
6. **Mid-training-checkpoint amateurs ([[cd-improves-reasoning]]) work better than fully-trained small models — does this generalise beyond the CD setting?** The "skill increments are linearly extractable" claim suggests R_w could be initialised from checkpoint differences rather than learned from scratch.

## See also

- [[../synthesis/decoding-time-shapes]] — Cross-method synthesis tabulating all 13 methods by intervention point × data floor × access × mechanism × R_w-implication
- [[../synthesis/proposed-method]] — R_w extension; this theme is its empirical/theoretical backbone
- [[../selective-finetuning/_overview]] **(added 2026-05-13)** — training-time / weight-modification sibling theme. Decoding-time methods leave weights frozen and compose at inference; selective-finetuning modifies weights surgically. Same underlying claim ("behaviour is isolable") at different mechanism layers.
- [[../synthesis/proposer-reward-shapes]] — sibling synthesis page (proposer-reward family)
- [[../concept-learning/_overview]] — concept-as-direction lineage (CBM, RCE)
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — token-level 0%-shifted finding; the RLVR analogue of this theme's decoding-time finding
- [[../self-play/invisible-leash]] — Theorem C.1 support inclusion; holds by construction for every method here

## Source

Theme synthesised 2026-05-13 from 13 captured papers in `raw/research/decoding-time-steering/`. Per-paper traceability lives in each sibling page's `## Source` section. Cross-cutting claims here are editorial; the unanimity-for-R_w finding is itself a cross-source synthesis, not a direct quotation from any single paper.
