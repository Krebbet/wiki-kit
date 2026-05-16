---
name: repe
description: Umbrella transparency framework — Linear Artificial Tomography extracts reading vectors from contrast-pair activations; three inference-time operators (linear combination, piecewise, projection-erasure) steer concept representations without fine-tuning. Establishes the principled vocabulary unifying ITI, ActAdd, and CAA.
type: research
---

# Representation Engineering: A Top-Down Approach to AI Transparency

Zou et al. (2023; arXiv:2310.01405) — CAIS / CMU / UC Berkeley / Stanford. RepE is the **umbrella framework** for the activation-steering sub-family of decoding-time methods. It introduces **Linear Artificial Tomography (LAT)** — a population-level pipeline that extracts a *reading vector* $v$ from contrast-pair hidden states — and proposes three inference-time control operators that apply $v$ to steer model representations toward or away from a target concept. The framework explicitly subsumes prior scattered activation-editing work (ITI, ActAdd, CAA) into a common vocabulary and provides a principled four-experiment evaluation protocol drawn from cognitive neuroscience. Central empirical finding: models internally represent safety-relevant concepts (truthfulness, morality, utility, power) at >90% classification accuracy in activation space while the output layer fails — the bottleneck is *reading-out*, not *knowing*.

## Source

- arXiv: 2310.01405
- Raw: `raw/research/decoding-time-steering/11-08-repe.md`

## Method

RepE has two poles: **Representation Reading** locates the concept; **Representation Control** steers it.

### Linear Artificial Tomography (LAT)

LAT is a three-step scan borrowed structurally from neuroimaging.

**Step 1 — Stimulus design.** Design contrast pairs differing only in the target concept $c$. For concept extraction the template elicits declarative knowledge:

$$T_c: \quad \text{"Consider the amount of }\langle c \rangle\text{ in the following: }\langle s_i \rangle\text{. The amount of }\langle c \rangle\text{ is"}$$

For functional extraction (honesty, power-seeking) the template pairs an experimental instruction-following prompt $T_f^+$ with a reference that does not invoke the function $T_f^-$.

**Step 2 — Collect neural activity.** For a decoder model $M$ and stimulus set $S$, compile last-token hidden states:

$$A_c = \{\,\operatorname{Rep}(M,\, T_c(s_i))[-1] \mid s_i \in S\,\} \tag{1}$$

For functions, collect token-level representations from each position $k$ in the model response for both polarities:

$$A_f^{\pm} = \{\,\operatorname{Rep}(M,\, T_f^{\pm}(q_i, a_i^{[k]}))[-1] \mid (q_i, a_i) \in S,\; 0 < k \le |a_i|\,\} \tag{2}$$

**Step 3 — Fit a linear model.** Apply PCA to the set of pairwise difference vectors:

$$\text{input to PCA:}\quad \{A_c^{(i)} - A_c^{(j)}\}_{\text{pairs}} \qquad \text{(concepts)}$$

$$\text{input to PCA:}\quad \{(-1)^k(A_f^{+(i)} - A_f^{-(i)})\} \qquad \text{(functions)}$$

The **reading vector** $v$ is the first principal component. Predictions use the dot product $\operatorname{Rep}(M, x)^\top v$. Stimulus sets of 5–128 pairs suffice; model-self-generated pairs work. LAT is fully unsupervised — no concept labels used during extraction.

### Representation Control Operators

Given a current representation $R$ and controller $v$, three baseline operators:

**Linear combination** — stimulation or suppression:
$$R' = R \pm \alpha v \tag{3}$$

**Piecewise** — conditional amplification along the concept direction:
$$R' = R + \alpha\,\operatorname{sign}(R^\top v)\, v \tag{4}$$

**Projection-erasure** — remove the concept component entirely:
$$R' = R - \frac{R^\top v}{\|v\|^2}\, v \tag{5}$$

The controller $v$ can be any of three baselines:

- **Reading Vector** — stimulus-independent; obtained from LAT. Shifts all representations in the same direction regardless of input. Cheap but blunt.
- **Contrast Vector** — stimulus-dependent; computed on-the-fly during inference as the difference between forward passes on $T_f^+$ and $T_f^-$ of the *current* input. Stronger but requires >3× inference compute due to two forward passes per step.
- **LoRRA (Low-Rank Representation Adaptation)** — fine-tunes low-rank adapter matrices on attention weights so that representations match contrast-vector targets (Algorithm 1 in the paper). Controllers are baked into the model weights; zero inference overhead. LoRRA loss per layer $l$:
  $$\mathcal{L} = \|m\,(r_l^p - r_l^t)\|^2, \quad r_l^t = \operatorname{Rep}(M, x) + \alpha v_l^c + \beta v_l^r$$
  where $m$ masks pre-response token positions, $v_l^c$ is the contrast vector, and $v_l^r$ is an optional reading vector target.

### Four-Experiment Evaluation Protocol

Borrowed from neuroscience; all four types are needed to establish that a reading vector is causally load-bearing:

1. **Correlation** — classification accuracy on held-out stimuli (linear probe).
2. **Manipulation** — counterfactual: add $+v$ or $-v$ and measure output shift.
3. **Termination** — project out $v$ via Eq. (5); measure accuracy drop.
4. **Recovery** — remove $v$, then re-inject; measure performance recovery.

Key negative result: logistic-regression probes pass **Correlation** but fail **Manipulation** and **Termination** — linear decodability does not imply causal load-bearing. PCA / K-Means directions pass all four.

## Claims

- LAT surpasses few-shot prompting on QA benchmarks (LLaMA-2): OBQA 59.2 vs 48.4, CSQA 86.4 vs 84.6, ARC-e 65.7 vs 59.9, ARC-c 60.3 vs 49.5, RACE (approximate).
- Contrast Vector achieves SOTA TruthfulQA MC1: 47.9 (7B) / 54.0 (13B), vs zero-shot 31.0 / 35.9, ActAdd 33.7 / 38.8. 13B LLaMA-2-Chat approaches GPT-4 on this task.
- LoRRA reaches 42.3 (7B) / 47.5 (13B) on TruthfulQA MC1 with negligible inference overhead — comparable to the Reading Vector baseline (34.1 / 42.4) and below Contrast Vector, but no dual-forward-pass cost.
- 5–128 contrast pairs suffice for LAT; model-self-generated pairs work — no labeled data required.
- Concept compositionality: $\operatorname{Risk}(s,a) = \mathbb{E}_{s'}[\max(0,-U(s'))]$ — separately extracted utility and probability vectors compose arithmetically into risk, with linear correlation in early-to-middle layers (Fig. 16).
- Reading vectors for honesty reach >90% accuracy on held-out honest/dishonest examples and generalise OOD to uninstructed deception scenarios.
- LoRRA-controlled LLaMA-2-Chat models show measurable reductions in Immorality and Power scores on the MACHIAVELLI benchmark without degrading task Reward (Table 3).
- Standard zero-shot TruthfulQA failure is attributable to dishonesty rather than capability failure: LAT correctly classifies when the model internally knows the right answer despite generating the wrong one.

## Strengths

- **Subsumes prior work.** Paper explicitly frames ActAdd (Turner et al. 2023) as a Contrast Vector special case — single stimulus pair instead of a population. ITI and CAA are cited as instances of the same family. RepE converts ad-hoc tricks into a principled methodology.
- **Population-level vs individual-stimulus.** LAT operates on a distribution of stimuli; individual-pair difference vectors are noisier. PCA extracts the dominant shared direction rather than a single datapoint's noise.
- **Unsupervised by default.** No concept labels required at extraction time. Self-generated stimuli work. This is critical for extracting superhuman or hard-to-label representations.
- **Falsifiability.** The four-experiment protocol (Correlation / Manipulation / Termination / Recovery) specifies exactly when a reading vector has failed to identify a causally load-bearing direction. The logistic regression negative result is a direct demonstration.
- **LoRRA bridges reading and control.** By fine-tuning low-rank adapters to match contrast-vector targets, LoRRA converts a two-pass inference overhead into a one-time training cost with zero inference penalty.
- **Breadth of concepts demonstrated.** Honesty, hallucination, utility, morality, power-seeking, probability, risk, emotion, harmlessness, fairness, knowledge editing, memorization — all within a single framework.

## Weaknesses

- **Architecture scope.** Validated on LLaMA-2 (7B–70B) and Vicuna; generalisation to non-RLHF base models and other architectures asserted but not systematically tested. Base models show weaker functional representations than chat/RLHF models.
- **Contrast Vector inference cost.** Two forward passes per step = >3× compute at inference. Partial fix via LoRRA but that requires training.
- **Stimulus design sensitivity.** The LAT task template is load-bearing (Fig. 13 shows large accuracy drop without it). The contrast framing (what counts as positive/negative stimulus) requires task-specific design; not turnkey.
- **Reading vector direction invariance.** Stimulus-independent reading vectors shift every generation in the same concept direction regardless of context — no input-adaptive modulation. Contrast Vectors fix this but at compute cost.
- **Layer selection.** Reading performance varies significantly by layer; the paper selects the best layer using a small validation set. Layer generalisation across architectures is unclear.
- **Not an interpretability claim.** RepE locates and steers directions; it does not explain which circuits implement them. The gap between representational and mechanistic explanations is explicit in the paper (Fig. 2), not resolved.

## Relevance to this wiki's project

RepE is the **mechanistic warrant** for the $R_w$ hypothesis and the theoretical frame legitimising the entire decoding-time + activation-steering lineage.

**$R_w$ and the know/output gap.** RepE's central finding — models represent truthfulness at >90% accuracy internally while the output layer fails — directly instantiates $R_w$: the gap is in reading-out, not in knowing. $R_w$ on logits (contrastive decoding, [[contrastive-decoding]], [[dexperts]]) is the output-space analogue of RepE's activation-space steering; RepE is the activation-level mechanistic evidence that the concept signal exists and is linearly accessible.

**Concept-as-direction.** RepE's reading vector $v$ is the mechanistic realisation of concept-as-axis. Where [[../concept-learning/concept-bottleneck-models|CBMs]] supervise a concept bottleneck with labeled data, RepE extracts the same axis from contrast pairs without labels. Where [[../concept-learning/recursive-concept-evolution|RCE]] refines a concept subspace iteratively, RepE extracts the dominant direction from a single PCA step. These are all instances of the same geometric claim: target concepts occupy linear subspaces in representation space.

**ICL-Bayesian latent concept.** RepE's compositionality result (utility + probability → risk via arithmetic on directions) and the linear correlation in early layers are consistent with [[../in-context-learning-theory/icl-bayesian-inference|ICL-Bayesian inference]]'s claim that a latent concept posterior has a linear geometric correlate in activation space. This makes single-sample concept installation plausible: if the concept direction can be extracted from $O(10)$ contrast pairs, a single training example that strongly activates the concept direction is a meaningful concept signal.

**Low-rank routing parallel.** LoRRA's low-rank adapter approach (correcting representation trajectories via adapter matrices trained on contrast-vector loss) parallels [[../rlvr-mechanics/rl-sparse-subnetwork|RL-sparse-subnetwork]] observations about low-rank routing corrections being sufficient for concept-level shifts — the representation correction needed is small-rank in both cases.

**Theme-level frame.** RepE is not one method alongside [[iti]], [[actadd]], and [[caa]]; it is the conceptual vocabulary that makes them commensurable and provides shared evaluation criteria. Any activation-steering work in this wiki should be understood as an instance of RepE's framework.

## Connections to the wiki

- **[[../synthesis/proposed-method]]** — $R_w$ on logits is the output-space analogue of RepE's activation-space reading; RepE is the mechanistic warrant for the gap hypothesis.
- **[[../concept-learning/concept-bottleneck-models]]** — CBMs supervise concept axes with labels; RepE extracts them unsupervised from contrast pairs — same geometric claim, different extraction regime.
- **[[../concept-learning/recursive-concept-evolution]]** — RCE refines concept subspaces iteratively; RepE's PCA extracts the dominant direction in one pass; both treat concepts as linear subspaces.
- **[[../concept-learning/_overview]]** — RepE belongs as the activation-level anchor in the concept-learning thread.
- **[[../in-context-learning-theory/icl-bayesian-inference]]** — latent concept posterior has a linear geometric correlate; compositionality result (risk from utility × probability) is consistent.
- **[[../rlvr-mechanics/rl-sparse-subnetwork]]** — low-rank routing correction parallel; LoRRA and sparse-subnetwork both find that concept-level shifts require small-rank weight corrections.
- **[[iti]]** — Inference-Time Intervention (Li et al. 2023) is a RepE Reading + Control instance operating at attention head level; RepE subsumes it.
- **[[actadd]]** — Activation Addition (Turner et al. 2023) is a Contrast Vector special case with a single stimulus pair; RepE generalises to populations and adds evaluation criteria.
- **[[caa]]** — Contrastive Activation Addition (Rimsky et al. 2023) is the averaged-contrast cousin; RepE's LAT is the population-PCA generalisation.
- **[[linear-rep-hypothesis]]** — Park et al. is the formal theory backbone; RepE is the applied framework. Park provides the geometric grounding; Zou provides the pipeline and empirical scope.
- **[[contrastive-decoding]]** — CD operates on logits; RepE operates on hidden states. Both exploit the difference signal between two model forward passes as a concept locator.
- **[[dexperts]]** — output-space logit arithmetic; RepE is the activation-space analogue.
- **[[pplm]]** — gradient-based activation steering predecessor; RepE replaces gradients with PCA directions.
- **[[gedi]]**, **[[fudge]]**, **[[dola]]**, **[[cfg-lm]]**, **[[cd-improves-reasoning]]** — theme siblings; RepE provides the umbrella framework and evaluation vocabulary for all.

## Related

- [[iti]] — head-level instance of RepE Reading + Control
- [[actadd]] — single-pair Contrast Vector; RepE subsumes
- [[caa]] — averaged-contrast variant; RepE's LAT is the population-PCA generalisation
- [[linear-rep-hypothesis]] — formal theory backbone (Park et al.)
- [[contrastive-decoding]] — output-space logit-difference analogue
- [[../concept-learning/concept-bottleneck-models]] — supervised concept-axis extraction
- [[../concept-learning/recursive-concept-evolution]] — iterative subspace refinement
- [[../in-context-learning-theory/icl-bayesian-inference]] — latent concept posterior / linear geometric correlate
- [[../synthesis/proposed-method]] — $R_w$ operationalisation; RepE is the mechanistic warrant
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — low-rank routing correction parallel
