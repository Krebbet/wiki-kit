---
title: "Task-Specific Skill Localization in Fine-tuned Language Models"
authors: "Panigrahi, Saunshi, Zhao, Arora"
venue: "ICML 2023"
arxiv: "2302.06600"
theme: selective-finetuning
tags: [skill-localization, grafting, sparse-finetuning, parameter-efficiency, calibration, continual-learning]
---

# Task-Specific Skill Localization in Fine-tuned Language Models

**The headline result: ~0.01% of parameters carry >95% of a fine-tuned skill.** Panigrahi et al. introduce *skill localization via grafting* — a post-hoc, no-retraining procedure that finds a binary mask $\gamma$ identifying a few thousand parameters in a 125M-parameter RoBERTa model such that transplanting only those fine-tuned values onto the frozen pre-trained model recovers full fine-tuning performance. This is the most direct empirical answer to the question: *Can the parts of a network responsible for one behaviour be isolated from those responsible for another?* The answer is yes — and the isolation is extreme.

Skills are not diffuse. They are parametrically localized to a tiny, identifiable, almost disjoint subset of weights. When a model is fine-tuned on multiple tasks simultaneously, each task's graft region is nearly orthogonal to the others, with overlap magnitude tracking intuitive task similarity. The existence proof is clean: no retraining, no architectural change, just a sparse mask applied post-hoc to the weight delta $\theta_{ft} - \theta_{pre}$.

## Source

Panigrahi, A., Saunshi, N., Zhao, H., & Arora, S. (2023). *Task-Specific Skill Localization in Fine-tuned Language Models*. ICML 2023. arXiv:2302.06600.

Code: [github.com/abhishekpanigrahi1996/Skill-Localization-by-grafting](https://github.com/abhishekpanigrahi1996/Skill-Localization-by-grafting)

## Method

### Model Grafting

Given pre-trained parameters $\theta_{pre}$ and fine-tuned parameters $\theta_{ft}$, a binary mask $\gamma \in \{0,1\}^{|\theta_{ft}|}$ defines a *grafted model*:

$$\theta_{ft}(\gamma) = \gamma \odot \theta_{ft} + (1 - \gamma) \odot \theta_{pre}$$

Equivalently, $\theta_{ft}(\gamma) = \theta_{pre} + \gamma \odot (\theta_{ft} - \theta_{pre})$. The mask both locates the skill and gives a compact representation of what was learned: $\gamma \odot (\theta_{ft} - \theta_{pre})$ is the irreducible update.

Two competing objectives must be balanced:

- *Good localization*: $\|\gamma\|_0$ is tiny (sparsity $\sim 10^{-4}$ to $10^{-5}$)
- *Skill retention*: $\mathcal{L}_T(\theta_{ft}(\gamma)) \approx \mathcal{L}_T(\theta_{ft})$

### Grafting Optimisation

The ideal problem is:

$$\underset{\gamma \in \{0,1\}^{|\theta_{ft}|},\; \|\gamma\|_0 \leq s}{\arg\min}\; \mathcal{L}_T\!\left(\gamma \odot \theta_{ft} + (1-\gamma) \odot \theta_{pre}\right) \tag{2}$$

To handle the discrete constraint, $\gamma$ is reparametrised via a sigmoid over a real-valued vector $S$, layered on top of an initial candidate mask $\gamma_{base}$:

$$\gamma := \gamma_{base} \odot (1 - \sigma(S)) + (1 - \gamma_{base}) \odot \sigma(S) \tag{4}$$

$\gamma_{base}$ is constructed as the top-$s$ parameters by magnitude of movement $|\theta_{ft} - \theta_{pre}|$. The optimisation then refines $\gamma_{base}$ by allowing additions and deletions via a few SGD steps (100 steps, lr $10^7$, batch 1024). The optimiser makes *minimal* changes to $\gamma_{base}$: $S$ is initialised so $\sigma(S) \approx 0$, and only a handful of gradient steps are taken — no $\ell_1$ regularisation is needed for the SGD regime.

**Crucial distinction from lottery tickets:** Lottery-ticket pruning sets non-mask parameters to 0; grafting sets them to $\theta_{pre}$. The difference is decisive — lottery-ticket-style pruning fails to recover any skill at any sparsity without retraining. Grafting needs no retraining.

**Crucial distinction from BitFit:** BitFit fine-tunes only biases (sparsity ~0.1%). Grafting is 10× sparser (0.01%), and bias-only grafting regions fail to localise skills (Fig. 4a in the paper). Mechanism differs: standard FT does not rely on biases.

### AdamW caveat

SGD-trained fine-tuned models exhibit strong localization. AdamW-trained models do not, unless $\ell_1$ regularisation on $\|\theta_{ft} - \theta_{pre}\|_1$ is applied during fine-tuning (strength 0.001 suffices). This suggests that the optimiser's update geometry shapes whether skills compress into sparse subsets.

## Claims

- **0.01% mask, >95% skill recovery.** For RoBERTa-base fine-tuned on 13 GLUE tasks (4096-shot), graft regions containing $\leq 8{,}500$ parameters (sparsity $10^{-4}$) recover $\geq 95\%$ of fine-tuning accuracy across all datasets. Agreement with the full FT model on test labels is 93% (single-sentence tasks) and 86% (two-sentence tasks).
- **GPT-2 analogue: 0.05%.** The same experiment on GPT-2 requires slightly looser sparsity (0.05%) but achieves the same >95% threshold.
- **Calibration: 40–90% ECE reduction.** Grafted models are dramatically better calibrated than vanilla fine-tuning. For SST-2 (4096-shot), ECE drops from 7.4 to 3.1; for QNLI, from 10.2 to 1.0. This holds even after retraining the sparse region, suggesting the sparse subnetwork is intrinsically less overconfident.
- **OOD generalisation improves by ~5%.** Under large distribution shifts (e.g., MPQA→SST-2/Yelp; QNLI→MNLI/SNLI), grafted models outperform vanilla FT by $\geq 5\%$, while BitFit collapses. The graft captures the "core" skill, not dataset-specific artefacts.
- **Multi-task disjointness.** When a model is fine-tuned simultaneously on 8 tasks, task-specific graft regions are nearly disjoint; region overlap correlates with intuitive task similarity (e.g., (SST-2, CR) and (SNLI, MNLI) show higher overlap than unrelated pairs).
- **Skill isolation transfers.** Grafting region $\gamma_i$ for task $i$ improves performance only on task $i$ and closely related tasks, not on unrelated ones — confirmed via relative performance gain $\text{Rel}_{\gamma,t} = (P_{\gamma,t} - P_{0,t})/(P_{1,t} - P_{0,t})$.
- **Compositionality.** Union of regions $\gamma_G = \bigcup_{i \in G} \gamma_i$ retains ~70% of accuracy gains for task subset $G$ without hurting others; 10 steps of fine-tuning on $\gamma_G$ raises this to ~80%.
- **Continual learning.** Freezing the graft region for task 1 and training only non-overlapping parameters for task 2 reduces catastrophic forgetting from a 20% accuracy drop (naive continual FT on QNLI) to 1.5%. Total memory scales as $T \cdot s$ rather than $T \cdot d$.

## Strengths / Novelty

- **Post-hoc, no retraining.** The method works on a standard fine-tuned model as-is, requiring no architectural modification, no PEFT-style re-run. This makes it a diagnostic as much as a technique.
- **Existence proof, not approximation.** Prior sparsity-based FT methods (PEFT, lottery tickets) achieve efficiency by changing the training procedure. Grafting asks: *where did vanilla FT concentrate the skill?* The answer — 0.01% — was not obvious and would not have been predicted by parameter-movement magnitude alone (learned mask beats top-movement baseline by a wide margin at low sparsity).
- **Calibration benefit is free.** Unlike temperature scaling or label smoothing, grafting's calibration gain requires no held-out data and no calibration-specific optimisation. It emerges from the sparsity itself.
- **Compositionality is emergent.** Region unions compose without joint optimisation, which would have been a natural requirement. The fact that they compose at all is a non-trivial structural property.
- **Parametric not activation-level.** Prior "skill neuron" work (Wang et al., 2022) ties skills to activations, which are input-dependent. Graft regions are input-agnostic parameter subsets — a stronger and more portable representation.

## Weaknesses

- **SGD requirement.** The cleanest localization holds only for SGD-trained models. AdamW — the dominant optimizer for LLM fine-tuning — does not produce localised skills without an explicit $\ell_1$ penalty on parameter movement. This limits direct applicability to most modern fine-tuning pipelines without modification.
- **Encoder-only, small scale.** Experiments are on RoBERTa-base (125M) and GPT-2 (117M). Whether 0.01% localization holds for 7B–70B models, or for instruction-tuning / RLHF, is untested. The number of parameters in the mask ($\sim 5{,}000$) is absolute, not relative — at 70B params the fraction would be even smaller, but the mask may need to grow.
- **Classification tasks only.** All GLUE tasks are classification or short-span tasks. Open-ended generation, multi-step reasoning, and chain-of-thought tasks are out of scope.
- **Optimization cost.** Finding $\gamma$ requires 100 SGD steps on the task data, using the fine-tuned and pre-trained model simultaneously. This is cheap but not zero-cost; it also requires access to training data at analysis time.
- **AdamW MT exception.** Interestingly, AdamW *does* show localization in the multi-task setting even without $\ell_1$ regularisation — but not in single-task. The reason is speculative (multi-task pressure naturally encourages compression). This inconsistency between settings is not fully explained.
- **No causal intervention.** Grafting shows that the mask *suffices* for the skill; it doesn't rule out that parameters outside the mask are *also* causally involved. The sufficiency bound is tight but necessity is unproven.

## Relevance to This Wiki's Project

This paper is **the empirical anchor for the $R_w$ hypothesis** at the weight level. The core claim of the proposed method (see [[../synthesis/proposed-method]]) is that a model fine-tuned on one concept stores the concept in a sparse, isolable weight subspace $R_w$, and that targeted gradient application to $R_w$ — and only $R_w$ — can transfer or compose skills without collateral damage to unrelated capabilities.

Panigrahi et al. provide the existence proof:

1. **Skills are sparse in weight space.** 0.01% of parameters suffice. If skills were uniformly diffuse, the project's premise — that you can selectively write, read, or suppress a skill — would be implausible. The extreme sparsity makes selective gradient application tractable.
2. **Skills are nearly disjoint across tasks.** Multi-task grafting shows that skill regions for unrelated tasks barely overlap. This validates the assumption that applying gradients to $R_{w,A}$ does not corrupt skill $B$ stored in $R_{w,B}$.
3. **Overlap tracks similarity.** Region overlap is a proxy for task similarity, which is exactly the structure the project needs for curriculum ordering and transfer: nearby concepts share weight subsets; distant concepts don't interfere.
4. **The weight delta $\gamma \odot (\theta_{ft} - \theta_{pre})$ is the concept representation.** This is the parametric analogue of the single-sample concept skeleton — a compact, transferable delta concentrated in $R_w$.
5. **Compositionality is emergent.** Union grafting composes skill regions with ~70–80% retention, hinting that $R_w$ arithmetic is partially additive — directly relevant to the proposed method's multi-concept composition step.

The SGD caveat is a live constraint: if the project's single-sample fine-tuning uses AdamW, explicit $\ell_1$ regularisation on $\|\theta_{ft} - \theta_{pre}\|_1$ may be needed to produce localisable skills. This is a design choice to record in the experimental setup.

## Connections to the Wiki

**Within selective-finetuning theme:**
- [[rome]] — locate-then-edit for factual associations in MLP key-value pairs; Panigrahi operates at the task-skill level (thousands of params across all layers), ROME at the fact level (single MLP layer). Complementary granularities of "where knowledge lives."
- [[memit]] / [[alphaedit]] — mass fact editing; Panigrahi's multi-task compositionality (union grafting) is the skill-level analogue of editing multiple facts simultaneously.
- [[mend]] — gradient-based fact editing without retraining; grafting is also post-hoc but identifies regions rather than re-routing gradients.
- [[knowledge-neurons]] — neuron-level locality for factual knowledge in feed-forward layers; Panigrahi is at parameter-mask level (any parameter in any layer), broader but coarser than neuron-level pinpointing.
- [[ff-kv-memories]] — feed-forward layers as key-value memories; suggests where graft parameters might concentrate.
- [[lima]] — LIMA argues that instruction-following is surface formatting, not deep capability; Panigrahi shows that even the surface skill (classification head behaviour) is parametrically sparse, compatible with LIMA's view that the underlying capability (knowledge) pre-exists in $\theta_{pre}$.
- [[surgical-finetuning]] — which *layers* to fine-tune; grafting identifies which *parameters* within layers. Orthogonal decompositions of the same question.
- [[o-lora]] — orthogonal subspace fine-tuning to prevent interference; graft regions achieve near-orthogonality empirically, without explicit orthogonality constraints.
- [[dora]] — decomposes weight update into direction and magnitude; graft is purely a location selector — it selects *which* components of $(\theta_{ft} - \theta_{pre})$ to retain, not how to decompose them.
- [[pit]] / [[packnet]] — packing multiple tasks into non-overlapping pruned subnets; the closest pre-LLM ancestor of task-region compositionality. Grafting extends this to the post-hoc, no-retraining regime.
- [[hat]] — hard attention masks for task-specific parameter isolation; structurally similar goal, different mechanism (attention vs. parameter-delta mask).
- [[knowledge-editing-survey]] — broad survey context.

**Cross-theme:**
- [[../synthesis/proposed-method]] — $R_w$ hypothesis; this paper is the empirical anchor.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — Balashov et al. show RL fine-tuning touches 5–30% of weights. Panigrahi shows SFT skills concentrate to 0.01% — RL is far less sparse than SFT grafts, suggesting RL spreads updates more broadly, possibly because reward signals are noisier than supervised labels.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — REASONMAXXER: rank-8 $W_O$ updates at 0.04% of parameters, closest analogue at the token/head level; Panigrahi is the parameter-mask counterpart.
- [[../self-play/invisible-leash]] — the invisible leash (bounded divergence from base model) exists partly because skills are sparse: gradient updates to $R_w$ bleed only weakly into $R_{w}^{\perp}$, so the pre-trained prior persists in the bulk.
- [[../concept-learning/recursive-concept-evolution]] — low-rank concept subspaces in representation space; grafting provides the weight-space dual: sparse parameter subsets that implement those subspaces.
- [[../decoding-time-steering/iti]] — Inference-Time Intervention operates at the head/representation level; Panigrahi at the parameter level. Both find that capability is localised, just at different levels of abstraction.

## Related

- Frankle & Carlin (2018) — Lottery Ticket Hypothesis (requires retraining; graft does not)
- Ben Zaken et al. (2022) — BitFit (biases only; graft is 10× sparser and task-dependent)
- Wang et al. (2022) — Skill neurons in prompt-tuned models (activation-level; graft is parameter-level)
- Meng et al. (2022) — ROME (fact-level localization in MLP; graft is task-level)
- Wortsman et al. (2022) — WiSE-FT (weight interpolation for OOD; graft provides complementary ID-OOD curve)
- Kang et al. (2022) — inference-time task routing (inspires continual learning evaluation)
