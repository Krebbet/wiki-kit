---
title: "Mechanistic Analysis of Catastrophic Forgetting in LLMs During Continual Fine-tuning"
arxiv: "2601.18699"
theme: catastrophic-forgetting
status: read
date_added: 2026-05-16
tags: [catastrophic-forgetting, mechanistic-interpretability, gradient-interference, representational-drift, loss-landscape, continual-learning, attention-mechanisms]
---

# Mechanistic Analysis of Catastrophic Forgetting in LLMs During Continual Fine-tuning

Laitinen Imanov (DTU Compute, 2026) decomposes catastrophic forgetting in sequential fine-tuning into three coupled, architecturally-localized mechanisms: gradient interference in attention weights, representational drift in intermediate layers, and loss landscape flattening around prior-task minima. Rather than treating forgetting as a monolithic behavioral outcome, the paper ties each mechanism to a specific layer range, training-epoch window, and quantitative signature — making targeted intervention feasible.

The anchoring question for this wiki is: **when you stack skills via SFT/RLVR, does it move optimization around, and by what mechanism?** This paper is the closest available mechanistic answer: yes, optimization moves — and it moves non-selectively, disrupting attention heads that are not even relevant to the new task, rotating intermediate representational subspaces away from prior-task geometry, and collapsing the curvature that made prior-task solutions stable.

## Source

- arXiv: [2601.18699](https://arxiv.org/abs/2601.18699)
- Raw capture: `raw/research/rlvr-forgetting/06-05-mechanistic-forgetting.md`

**Model-scale note.** The abstract states "109B to 1.5T parameters." This refers to six models: open-weight Llama 4 Scout (109B total / 17B active, 16 experts), Llama 4 Maverick (400B total / 17B active, 128 experts), DeepSeek-V3.1 (671B total, MoE); and proprietary GPT-5.1 (estimated 1.5T), Gemini 2.5 Pro (estimated 1T), Claude Opus 4.5 (undisclosed). The Discussion explicitly notes that the largest *directly inspectable* open-weight model is 400B (Maverick); the 1.5T figure is an estimate for GPT-5.1 accessed via API fine-tuning, not directly probed internally.

## Method

**Experimental design.** Twelve fine-tuning sequences, each 4–6 tasks, across three inter-task similarity tiers (high / medium / low). Each task trained 3–5 epochs. Mechanistic metrics collected before, during, and after each fine-tuning phase: attention weight distributions, hidden-state representations (CKA), gradient statistics, Hessian eigenvalue spectra.

**Mechanism 1 — Gradient interference in attention (epochs 1–2, layers 1–12).**

Gradient cosine similarity between current-task and prior-task gradients is the key quantity. When $\cos(\nabla_\theta \mathcal{L}_\text{new}, \nabla_\theta \mathcal{L}_\text{old}) < -0.3$, forgetting rates increase $2.4\times$ versus conditions with positive alignment ($> 0.1$). Query/key projection matrices are the hotspot: 67% of those parameters show gradient conflict, versus 34% for value projections and 29% for feedforward weights.

Early-warning property: first-epoch gradient alignment predicts final forgetting magnitude at $r = -0.79$ ($p < 0.001$), before any behavioral change is detectable. Disrupted attention heads (15–23% of heads across all layers) exhibit entropy increases of 1.8–2.4 bits and head-specialization index decreases of 0.43 on average. Critically, only 31% of severely disrupted heads have high activation on the *new* task — disruption is largely non-selective.

Ablation evidence: freezing attention layers during fine-tuning reduces forgetting by 64%; freezing feedforward layers reduces it by only 23%; freezing output layers reduces it by 8%.

**Mechanism 2 — Representational drift in intermediate layers (epochs 3–5, layers 8–24).**

Drift measured via Centered Kernel Alignment (CKA) between pre- and post-fine-tuning hidden states on the same inputs. Intermediate layers (8–16 in 24-layer models, 12–24 in 40-layer models) show CKA drops of 0.32–0.47, versus 0.15–0.23 for lower layers and 0.08–0.14 for upper layers.

PCA of activations: the top-10 principal components (capturing 60–75% of variance) rotate by $35°$–$52°$ on average; higher-order components rotate only $8°$–$15°$. Drift does not preferentially target task-irrelevant dimensions — correlation between drift magnitude and task relevance is $r = 0.12$ ($p = 0.24$), i.e. essentially zero. Fine-tuning rotates the representational geometry indiscriminately.

Causal check: post-hoc affine realignment of intermediate representations recovers 38% of lost prior-task performance at cost of 6% new-task degradation. Combined with attention-head restoration, total recovery reaches 71%.

**Mechanism 3 — Loss landscape flattening (epoch 4+, all layers).**

Hessian eigenvalue analysis tracks curvature around prior-task minima. Initial maximum eigenvalue $\lambda_\text{max} = 147.3$ for Task 1; drops to $34.2$ after three subsequent fine-tuning steps. Task-1 landscape linearity index rises from 0.28 to 0.71 (0 = strongly curved, 1 = flat). Current-task curvature remains high ($\lambda_\text{max} = 112.7$), so flattening is task-selective — it degrades old-task geometry, not new.

Temporal offset: curvature begins decreasing 1–2 epochs *before* accuracy degrades, establishing flattening as a leading indicator.

Intervention: adding a curvature-regularization penalty on Hessian eigenvalues along prior-task-relevant directions reduces forgetting by 34% with 12% slower convergence — efficiency ratio 2.83 vs. 0.58 for gradient clipping and 0.45 for L2 regularization.

**Integrated timeline.**

| Epoch window | Dominant mechanism | Layer locus |
|---|---|---|
| 1–2 | Gradient interference → attention disruption | Layers 1–12 |
| 3–5 | Representational drift | Layers 12–24 |
| 4+ | Loss landscape flattening | All layers |

Mechanisms couple: attention disruption changes information flow into intermediate layers (amplifying drift); altered representations shift gradient statistics (intensifying interference); flattening reduces restoring forces that would guide the model back to prior minima.

## Claims

- Freezing attention weights during fine-tuning reduces forgetting by **64%** across all six model scales; feedforward freeze yields only 23%.
- **15–23%** of attention heads undergo severe weight-space disruption ($\|{\Delta W}\| > 2.5\sigma$), disproportionately in lower layers; only 31% of disrupted heads are active on the new task.
- Ablating the top-20% most disrupted heads post fine-tuning recovers **47%** of lost prior-task performance while degrading new-task accuracy by only **8%**.
- CKA in intermediate layers falls **0.32–0.47** (vs. 0.08–0.14 in upper layers).
- Leading representational PCs rotate **35°–52°**; higher-order PCs rotate 8°–15°.
- Gradient alignment in epoch 1 predicts final forgetting at $r = -0.79$ ($p < 0.001$); task-similarity metrics predict forgetting at $r = 0.87$ ($p < 0.001$).
- Behavioral forgetting: Llama 4 Maverick on low-similarity sequences loses **31.7%** absolute accuracy on Task 1 after four sequential tasks; high-similarity sequences lose 24.8% (counterintuitively worse than medium's 18.3%).
- Curvature regularization reduces forgetting **34%** at 12% convergence cost (efficiency 2.83 vs. L2's 0.45).
- The directly-inspectable open-weight scale tops out at 400B (Maverick); 1T–1.5T figures are estimates for API-accessed proprietary models with no internal access.

## Strengths / Novelty

- First systematic decomposition of forgetting into three architecturally-localized mechanisms with distinct epoch-windows and intervention handles.
- Causal validation for each mechanism via freeze/ablation/realignment experiments, not just correlation.
- Early-warning signal ($r = -0.79$ at epoch 1) is immediately operationalizable — you can forecast forgetting before it happens.
- MoE coverage (Llama 4, DeepSeek-V3.1) surfaces a fourth mechanism (expert-routing shift) absent in dense models.
- Curvature regularization outperforms standard baselines by a factor of ~5 on the efficiency ratio.

## Weaknesses / Limits

- Proprietary models (GPT-5.1, Gemini 2.5 Pro, Claude Opus 4.5) studied via API fine-tuning only — internal weight/gradient access unavailable for those architectures, so mechanistic claims rely on behavioral inference plus open-weight extrapolation.
- Task sequences are short (4–6 tasks, 3–5 epochs each); real deployment may face hundreds of sequential adaptations with different temporal dynamics.
- Experiments use supervised fine-tuning; the paper explicitly flags that RLHF/instruction-tuning may involve additional mechanisms.
- Task-sequence similarity is measured with simplified metrics; gradient-level and circuit-level compatibility may require finer measures.
- Scale ceiling for full mechanistic access is 400B (Maverick); whether mechanisms shift qualitatively above 1T is untested.

## Relevance to this wiki's project

The project asks whether stacking skills via RLVR/SFT moves optimization, and by what mechanism. This paper answers: **yes, and non-selectively.** Two implications stand out:

1. **Gradient interference in attention Q/K matrices** is the earliest and most predictive signal. Any curriculum strategy (concept-curriculum-method) that sequences skills must account for gradient conflict between skills — high apparent similarity in task surface is not protective and may be worse.

2. **Representational drift is task-irrelevant**: fine-tuning rotates intermediate representations indiscriminately, not just along new-task dimensions. This means single-sample concept learning on skill $B$ does not just overwrite skill-$B$-irrelevant dimensions of skill $A$ — it overwrites *all* of them roughly equally. The proposed method's goal of learning one concept without erasing another requires either selective gradient routing or explicit curvature protection to avoid this.

The 1–2 epoch early-warning window for gradient alignment gives a concrete monitoring hook: before committing to multi-epoch RLVR fine-tuning on a new skill, one epoch of probing could forecast whether forgetting will be severe.

## Connections to the wiki

**Within catastrophic-forgetting theme:**
- [[ewc-gemma2-cpt]] — EWC identifies *which* parameters matter via Fisher information; this paper identifies *what goes wrong* when those parameters are displaced (attention disruption → representational drift → landscape flattening). Complementary decompositions.
- [[rft-mitigates-forgetting]] — behavioral mitigation; mechanistic grounding here explains *why* RFT-style methods help (they reduce gradient conflict).
- [[rft-data-perspective]] — data-composition angle on forgetting; this paper provides the optimization-dynamics complement.
- [[empirical-forgetting]] — behavioral phenomenology; this paper provides the mechanism behind those patterns.
- [[rls-razor]] — sparsity-based approach to skill retention; gradient interference localized to Q/K matrices is exactly the locus RLS-razor-style methods should target.
- [[path-not-taken]] — off-principal updates; attention disruption in lower layers that is irrelevant to the new task is a concrete instance of off-principal parameter movement.
- [[_overview]] — theme index.

**Across wiki:**
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — sparse subnetwork activation is motivated by avoiding gradient interference; this paper provides the mechanistic evidence for why dense fine-tuning produces that interference.
- [[../selective-finetuning/_overview]] — gradient interference localized to Q/K matrices is precisely the target of selective-gradient methods; the 64% forgetting reduction from attention-freezing is a ceiling benchmark for those methods.
- [[../selective-finetuning/skill-localization]] — skill localization identifies parameter subsets to protect; this paper specifies *which* subsets (attention Q/K in lower layers) are most at risk.
- [[../synthesis/proposed-method]] — any design that stacks skills must budget for 15–23% attention-head disruption per fine-tuning step; curvature regularization (34% reduction) is a candidate regularizer for the concept-curriculum pipeline.

## Related

- Kirkpatrick et al. (EWC, 2017) — Fisher-information parameter protection; mechanistic precursor.
- Lopez-Paz & Ranzato (GEM, 2017) — gradient episodic memory; gradient-alignment framing adopted here.
- Ash & Adams (2020) — warm-starting neural networks; landscape geometry perspective.
- [[../in-context-learning-theory/induction-heads]] — induction heads are the functional circuits this paper identifies as most vulnerable in lower layers.
