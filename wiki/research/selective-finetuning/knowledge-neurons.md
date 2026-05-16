---
title: "Knowledge Neurons in Pretrained Transformers"
authors: "Dai et al."
venue: "ACL 2022"
year: 2022
tags: [selective-finetuning, mechanistic-interpretability, knowledge-editing, ffn, attribution]
status: read
---

# Knowledge Neurons in Pretrained Transformers

Dai et al. (ACL 2022) establish that specific factual associations are stored in identifiable individual neurons inside FFN layers of pretrained transformers. Using an integrated-gradient attribution method applied to fill-in-the-blank cloze tasks, they locate a handful of *knowledge neurons* per fact, then show that zeroing, amplifying, or overwriting the corresponding FFN value slots edits, erases, or updates that knowledge — without any fine-tuning. This is the empirical bedrock for the whole model-editing lineage (ROME, MEMIT, AlphaEdit): if facts are addressable at neuron granularity, weight surgery becomes a principled operation rather than a heuristic.

## Source

Dai, D., Dong, L., Hao, Y., Sui, Z., Chang, B., & Wei, F. (2022). Knowledge Neurons in Pretrained Transformers. *ACL 2022*. [arXiv:2104.08696](https://arxiv.org/abs/2104.08696)

## Method

The model is treated as a key-value memory following Geva et al. (2020): the first FFN linear layer computes intermediate neuron activations (keys), and the second integrates value vectors weighted by those activations. Knowledge attribution asks: how much does neuron $w_i^{(l)}$ — the $i$-th intermediate activation in layer $l$ — contribute to the model's probability of the correct answer?

Formally, define $P_x(\hat{w}_i^{(l)})$ as the model output probability for the correct answer when $w_i^{(l)}$ is clamped to the constant $\hat{w}_i^{(l)}$. The attribution score is the path integral of gradients as the neuron varies from 0 to its pretrained value $w_i^{(l)}$:

$$\mathrm{Attr}(w_i^{(l)}) = w_i^{(l)} \int_{\alpha=0}^{1} \frac{\partial P_x(\alpha w_i^{(l)})}{\partial w_i^{(l)}} \, d\alpha$$

Approximated by Riemann sum with $m = 20$ steps. Neurons whose score exceeds $0.2 \times \max$ attribution are retained (coarse set). A **refining** step then intersects coarse sets across $n$ diverse paraphrase prompts for the same fact, keeping only neurons shared by more than $p\%$ of prompts — this filters syntax/lexical neurons that do not generalise across phrasings.

The full pipeline: (1) generate $n$ diverse cloze prompts for $\langle h, r, t \rangle$; (2) compute attribution scores per prompt; (3) threshold to coarse sets; (4) intersect — neurons surviving in $> p\%$ of prompts are the knowledge neurons.

Experiments use BERT-base-cased on the PARAREL dataset (27,738 relational facts, 34 relations, mean 8.63 paraphrase templates per relation).

## Claims

- **Localisation.** On average 4.13 knowledge neurons are identified per fact; facts sharing the same relation share ~1.23 neurons, facts with different relations share ~0.09. Knowledge neurons are concentrated in the topmost transformer layers.
- **Causal activation–expression link.** Suppressing identified neurons (activation → 0) decreases the correct-answer probability by **29.03%** on average; amplifying (activation ×2) increases it by **31.17%**. Baseline-identified neurons (raw activation as attribution) move the probability by only −1.47% / −1.27% — negligible, confirming the attribution method is load-bearing.
- **Selectivity.** Knowledge neurons are activated significantly more by knowledge-expressing prompts (T1 avg. activation = 0.485) than head-only prompts (T2 = 0.019) or random prompts (T3 = −0.018), validated on a separate web-crawled BINGREL dataset.
- **Fact update.** Directly modifying value slots $\mathrm{FFN}^{(\mathrm{val})}_i \leftarrow \mathrm{FFN}^{(\mathrm{val})}_i - \lambda_1 t + \lambda_2 t'$ (λ₁ = 1, λ₂ = 8; manipulating ~4 neurons) achieves a 34.4% success rate vs. 0.0% for random neurons, with moderate perplexity increase on unrelated facts.
- **Relation erasure.** Setting the 20 most frequent relation-level neurons' value slots to zero raises cloze perplexity for the erased relation by 36–141%, while perplexity on other relations rises only 1–10%.

## Strengths

- First method to attribute knowledge to *individual neurons* rather than layers or heads; provides a causal (intervention-based) validation rather than correlation alone.
- No fine-tuning required for editing; surgery cost is $O(\text{neurons})$ — trivially cheap.
- Refining step elegantly separates fact-specific neurons from syntactic/positional ones by exploiting paraphrase invariance.
- Generalises beyond PARAREL: activation patterns validated on independently crawled open-domain texts (BINGREL).

## Weaknesses

- **Cloze-only, BERT-era.** The knowledge-assessing task is a fill-in-the-blank cloze with a single masked token; generative LLMs expressing knowledge through multi-token generation are not studied.
- **Single-word tail entities.** The setup requires the fact tail to be predictable at one [MASK] position; multi-word answers need a different evaluation scaffold (acknowledged by authors).
- **Shallow editing.** 34.4% success rate and non-zero collateral damage to related facts shows the method is a proof-of-concept, not a production editor. ROME/MEMIT subsequently address this.
- **Generalisation to GPT-style decoders untested in this paper.** The KV-memory structure applies to causal LMs, but attribution is computed at a masked token position — the direct application to autoregressive inference requires adaptation.
- **Prompt sensitivity of attribution.** The refining threshold $p$ is tuned per relation to keep the mean neuron count in [2, 5]; this heuristic may not transfer across model families or knowledge types.

## Relevance to This Wiki's Project

The anchoring question is: *how to inject SFT signal without degrading response style?* Knowledge Neurons answers the prerequisite: facts are not diffused uniformly — they cluster in a sparse, identifiable set of FFN neurons in upper layers. This has two direct implications:

1. **Surgical SFT targets.** If a single-sample SFT update should encode a new concept without touching style, the $R_w$ selective-update component (see [[../synthesis/proposed-method]]) can be scoped to the neurons that attribution identifies as concept-storing. This avoids the overwrite of style-relevant weights elsewhere.
2. **Sparsity budget.** Only ~4 neurons per fact move the probability by ~30%. The RL-sparse-subnetwork finding (5–30% of weights touched; [[../rlvr-mechanics/rl-sparse-subnetwork]]) looks like the same phenomenon at a coarser granularity. Both suggest the model has slack: most parameters are not load-bearing for any given capability, so selective updates need not be globally conservative — only locally precise.

The paper does not solve style preservation (its BERT context predates instruction-tuned LLMs), but it grounds the hypothesis that *content and style occupy different parameter subsets*, which is the structural premise needed to make selective SFT coherent.

## Connections to the Wiki

**Within selective-finetuning theme:**
- [[ff-kv-memories]] — Geva et al. (2021) provide the structural framing (FFN = KV memory) that Dai et al. operationalise at neuron level; read as a pair.
- [[rome]] — direct successor; replaces neuron-activation surgery with rank-one MLP edits for higher success rate and better locality.
- [[memit]] — scales ROME to batch edits across many facts simultaneously.
- [[alphaedit]] — further reduces collateral damage via constrained weight updates.
- [[mend]] — gradient-based meta-learned editor; complementary approach to the surgery framing.
- [[skill-localization]] — finds that skills localise to 0.01% of parameters; same direction as the ~4-neuron-per-fact result here.
- [[lima]] — 1000-sample SFT; style robustness in LIMA is implicitly explained if style neurons and fact neurons are disjoint.
- [[surgical-finetuning]], [[o-lora]], [[dora]], [[pit]] — parameter-efficient methods that exploit similar sparsity assumptions.
- [[packnet]], [[hat]] — structured masking methods that protect subnetworks; complementary to neuron-level attribution.
- [[knowledge-editing-survey]] — situates this paper in the broader taxonomy of editing methods.

**Cross-theme:**
- [[../synthesis/proposed-method]] — $R_w$ neuron-level edits foreshadow the selective-update lineage; Knowledge Neurons is the empirical anchor for that design choice.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — RL touches 5–30% of weights; the neuron-level sparsity here (~4 neurons per fact out of 3,072 FFN internals per layer) is an even sharper instance of the same phenomenon.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — asks which weights RL selects; Knowledge Neurons offers a comparison point from a supervised attribution angle.
- [[../decoding-time-steering/iti]] — Inference-Time Intervention operates at head level; Knowledge Neurons operates at FFN-neuron level — complementary granularities for the same goal of targeted activation steering.
- [[../concept-learning/concept-bottleneck-models]] — CBMs externalise concepts as labelled axes; Knowledge Neurons internalises the same idea as identified neuron sets — both are attempts to make concept storage explicit and manipulable.

## Related

- Geva et al. (2021) — "Transformer Feed-Forward Layers Are Key-Value Memories" (structural framing)
- Meng et al. (2022) — ROME: Locating and Editing Factual Associations in GPT
- Yao et al. (2023) — Editing Large Language Models (survey)
- Sundararajan et al. (2017) — Integrated Gradients (attribution foundation)
