---
title: "MEND — Fast Model Editing at Scale"
aliases: ["MEND", "Model Editor Networks with Gradient Decomposition"]
tags: [selective-finetuning, model-editing, gradient-transform, hypernetwork, knowledge-editing]
source: "Mitchell et al., ICLR 2022 — arXiv:2110.11309"
---

# MEND — Fast Model Editing at Scale

Mitchell et al. (ICLR 2022) present **MEND** (Model Editor Networks with Gradient Decomposition), a collection of small auxiliary networks that transform the standard fine-tuning gradient into a targeted parameter update — correcting a single input-output error in one step, with no damage to unrelated model behaviour, at scales up to 11 B parameters. The key insight is that fully-connected-layer gradients are rank-1 objects: instead of learning a $\mathbb{R}^{d^2} \to \mathbb{R}^{d^2}$ gradient map (intractable for $d \approx 10^4$), MEND decomposes the gradient into its outer-product factors and learns a $\mathbb{R}^{O(d)} \to \mathbb{R}^{O(d)}$ transformation — reducing parameter count by four orders of magnitude.

## Source

- Raw: `../../../raw/research/selective-finetuning/02-05-mend.md`
- Paper: <https://arxiv.org/abs/2110.11309>

## Method

### Problem framing

A model editor $E$ maps an edit pair $(x_e, y_e)$, loss $\ell_e$, base parameters $\theta$, and optional editor parameters $\phi$ to updated parameters $\theta_e$. Three desiderata:

- **Reliability** — $p_{\theta_e}(y_e \mid x_e)$ is maximised.
- **Locality** — $\mathbb{E}_{x_\text{loc}}[\text{KL}(p_\theta(\cdot \mid x_\text{loc}) \| p_{\theta_e}(\cdot \mid x_\text{loc}))]$ is small.
- **Generality** — the edit transfers to semantically equivalent rephrasings $x'_e \in \mathcal{N}(x_e, y_e)$.

Edit success (ES) is the accuracy of $p_{\theta_e}$ on $(x_e, y_e) \cup \mathcal{N}(x_e, y_e)$.

### Rank-1 gradient decomposition

For a fully-connected layer $\ell$ with weight $W_\ell$, the per-example fine-tuning gradient factors as a rank-1 outer product:

$$\nabla_{W_\ell} L = \sum_{i=1}^{B} \delta^i_{\ell+1} \, {u^i_\ell}^\top$$

where $\delta^i_{\ell+1}$ is the loss gradient w.r.t. pre-activations at layer $\ell{+}1$ and $u^i_\ell$ is the input to layer $\ell$ for batch element $i$. For Transformers, the batch index absorbs the sequence index without loss of generality.

A naive gradient-to-update mapping requires $O(d^2)$ inputs — impractical. Conditioning separately on $\delta^i_{\ell+1}$ and $u^i_\ell$ (each $O(d)$) is tractable.

### Editor networks

Each MEND network $g_\ell$ (parameterised by $\phi_\ell$) takes $z_\ell = \text{concat}(u_\ell, \delta_{\ell+1})$ and produces **pseudoactivations** $\tilde{u}_\ell$ and **pseudodeltas** $\tilde{\delta}_{\ell+1}$. The transformed gradient update is:

$$\widetilde{\nabla}_{W_\ell} = \sum_{i=1}^{B} \tilde{\delta}^i_{\ell+1} \, {\tilde{u}^i_\ell}^\top$$

The weight edit is then $\widetilde{W}_\ell = W_\ell - \alpha_\ell \widetilde{\nabla}_{W_\ell}$, where $\alpha_\ell$ is a learned per-layer scalar step size.

Architecture of $g_\ell$: a two-block residual MLP with low-rank weight matrices ($U_j V_j$, keeping total parameters $O(d)$), layer-specific FiLM-style scale $s_\ell$ and offset $o_\ell$, and identity initialisation (residual streams initialise to the identity, ensuring edits start from a sensible prior). Parameters are shared across layers of the same shape; for a standard Transformer MLP, this means only two editor parameter sets (first and second MLP projection).

### Training objective

Editor parameters $\phi$ are trained on an edit dataset $D^\text{tr}_\text{edit}$ by minimising:

$$\mathcal{L}_\text{MEND} = c_e \mathcal{L}_e(\theta_{\widetilde{W}}) + \mathcal{L}_\text{loc}(\theta_W, \theta_{\widetilde{W}})$$

where $\mathcal{L}_e = -\log p_{\theta_{\widetilde{W}}}(y'_e \mid x'_e)$ measures generalisation to equivalence neighbours, and $\mathcal{L}_\text{loc} = \text{KL}(p_{\theta_W}(\cdot \mid x_\text{loc}) \| p_{\theta_{\widetilde{W}}}(\cdot \mid x_\text{loc}))$ enforces locality. No higher-order gradients are computed; $\phi$ is optimised with Adam ($c_e = 0.1$ throughout).

## Claims

- MEND is the only editor that successfully edits GPT-Neo (2.7 B), GPT-J (6 B), T5-XL (2.8 B), and T5-XXL (11 B); all baselines (FT, FT+KL, KE) fail at this scale (Table 3).
- On Wikitext generation: MEND ES = 0.81 / 0.88 on GPT-Neo / GPT-J vs. FT 0.55 / 0.80 and KE ≈ 0.00 / 0.01.
- On zsRE QA: MEND ES = 0.88 / 0.89 on T5-XL / T5-XXL; accuracy drawdown < 0.001 in both cases.
- At small scale (BERT-base, BART-base) MEND matches ENN (the strongest small-scale competitor) while requiring no modification of the pre-edit model.
- Batched editing: MEND applies 25 simultaneous edits with 96 % ES and < 1 % accuracy degradation; ENN degrades to 35 % ES at the same batch size (Table 5).
- MEND trains on a single GPU in under a day even for 10 B+ parameter models; ENN cannot fit in the same memory budget at that scale (Figure 3).
- Identity initialisation and input normalisation are load-bearing: removing either reduces ES sharply and increases training time ~10×  (Table 6 ablations).
- Editing only the smaller of $\tilde{u}_\ell$ or $\tilde{\delta}_{\ell+1}$ — the lightest variant — still produces effective edits, suggesting MEND can scale to 100 B+ parameter models.

## Strengths

- **Tractable at scale.** Rank-1 decomposition reduces the mapping dimensionality from $O(d^2)$ to $O(d)$, enabling single-GPU training even for 11 B models.
- **No forward-pass contamination.** Unlike ENN, MEND does not modify the pre-edit model; the original $p_\theta$ is preserved exactly until an edit is applied.
- **Single-step inference.** At test time, one forward pass + one MEND transform applies an edit — no iterative fine-tuning loop.
- **Batched edits.** Summing per-example transformed gradients handles up to 125 simultaneous edits (degrading gracefully) without architectural changes.
- **Architecture-agnostic.** Applicable to any model with fully-connected layers; demonstrated on T5, GPT, BERT, BART families.

## Weaknesses

- **Locality is soft.** Over-generalisation (editing unrelated inputs that share surface similarity) is a known failure mode; the locality loss alone does not fully prevent it.
- **Requires an edit training set.** The editor $\phi$ must be trained on $D^\text{tr}_\text{edit}$ before deployment — domain mismatch between training and target edits degrades performance.
- **MLP-layer targeting.** Ablations show editing attention matrices is consistently worse than MLP weights for large models; the rank-1 structure is specific to fully-connected projections.
- **Equivalence-neighbourhood proxy.** The paper evaluates generalisation via backtranslation rephrasings; whether edited knowledge propagates to implied downstream questions (e.g., Is Boris Johnson a private citizen?) is untested.
- **Step-size meta-parameter.** $\alpha_\ell$ is learned but scalar per layer — may be insufficient for edits requiring different magnitudes across weight dimensions.

## Relevance to this wiki's project

The anchoring question — "how to add SFT data signal without degrading response style; isolate parts of the network; apply the gradient selectively?" — maps exactly to MEND's design contract.

**Two complementary paradigms for selective editing:**

| Paradigm | Representative | What is targeted |
|---|---|---|
| Locate-then-edit | ROME, MEMIT | Specific weight subsets (MLP mid-layers) identified by causal tracing |
| Gradient-transform | MEND | The gradient itself, learned to be locally applied anywhere |

MEND is the gradient-as-target approach: rather than asking "which weights to touch", it asks "how to reshape the gradient so touching any (selected) weight is safe." This is directly relevant to $R_w$ in the proposed method ([[../synthesis/proposed-method]]) — MEND demonstrates that learning a gradient projection is a tractable substitute for hand-designed locality constraints.

For single-sample concept learning specifically: if a concept correction must be injected from one example without polluting generation style, MEND's framework (train a hypernet on correction-type exemplars, then apply a rank-1 transformed update at inference) is the operative template. The rank-1 structure also resonates with LoRA-family observations that fine-tuning gradients are intrinsically low-rank — the same assumption underpinning the finding in [[../rlvr-mechanics/rl-sparse-subnetwork]] and [[../rlvr-mechanics/rethinking-rl-sparse-selection]] that rank-32 LoRA approximates the RL gradient well. MEND takes this one step further: not just approximating but *transforming* the rank-1 gradient into a better update.

Practical implication: if response-style preservation is the constraint, MEND's locality loss $\mathcal{L}_\text{loc}$ (KL on held-out style examples) is a plug-in objective alongside the concept-accuracy loss. The invisible-leash framing ([[../self-play/invisible-leash]]) — preventing style drift under iterative refinement — maps to exactly this KL penalty.

## Connections to the wiki

- [[rome]] — sibling method: same goal (single-pair edit, no style degradation), different mechanism (causal tracing → closed-form rank-1 weight update vs. learned gradient transform). ROME is faster at inference but not trainable to a new edit distribution; MEND is.
- [[memit]] — extends ROME to batched edits across many layers; analogous to MEND's batched-edit summing but mechanistically different (least-squares weight update vs. hypernet transform).
- [[alphaedit]] — null-space projection approach: projects gradient updates into the null space of a retained-knowledge matrix, enforcing locality by geometry rather than learned regularisation.
- [[knowledge-neurons]] — identifies factual knowledge in FFN neurons by activation patching; informs which layers MEND should target.
- [[ff-kv-memories]] — FFN layers as key-value stores; provides the mechanistic account for why MLP-layer editing (not attention) is most effective in MEND ablations.
- [[skill-localization]] — locates skill-specific parameter subsets; complementary entry point — locate first, then apply MEND-style transform within the subset.
- [[lima]] — 1K carefully chosen SFT examples suffice; MEND operationalises the single-example limit case with locality guarantees.
- [[surgical-finetuning]] — restricts updates to a small parameter subset; MEND's locality loss achieves the same functional constraint via learned regularisation.
- [[o-lora]], [[dora]], [[pit]] — LoRA-family methods that constrain update direction; MEND's rank-1 transform is structurally analogous but learned end-to-end for locality.
- [[packnet]], [[hat]] — mask-based continual learning; complementary to MEND's soft locality: hard masks prevent interference by zeroing gradients, MEND prevents it by reshaping them.
- [[knowledge-editing-survey]] — survey situating MEND within the broader editing taxonomy.
- [[../synthesis/proposed-method]] — $R_w$ component: MEND is a concrete existence proof that a learned gradient transform can replace hand-coded locality constraints.
- [[../rlvr-mechanics/rl-sparse-subnetwork]], [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — rank-32 LoRA approximates the RL gradient; MEND generalises this by learning the optimal rank-1 projection rather than fixing rank.
- [[../self-play/invisible-leash]] — MEND's $\mathcal{L}_\text{loc}$ KL penalty is the fine-tuning-time instantiation of the invisible-leash constraint.

## Related

- [[rome]]
- [[memit]]
- [[alphaedit]]
- [[knowledge-neurons]]
- [[ff-kv-memories]]
- [[skill-localization]]
- [[lima]]
- [[surgical-finetuning]]
- [[o-lora]]
- [[dora]]
- [[pit]]
- [[packnet]]
- [[hat]]
- [[knowledge-editing-survey]]
- [[../synthesis/proposed-method]]
- [[../rlvr-mechanics/rl-sparse-subnetwork]]
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[../self-play/invisible-leash]]
