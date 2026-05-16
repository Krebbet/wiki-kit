---
title: "PackNet: Adding Multiple Tasks to a Single Network by Iterative Pruning"
aliases: ["PackNet", "packnet"]
tags: [selective-finetuning, continual-learning, pruning, gradient-masking, background]
source: "Mallya & Lazebnik, CVPR 2018 — arXiv:1711.05769"
depth: background
---

# PackNet

PackNet is the canonical pre-LLM demonstration that a single network can host multiple tasks without catastrophic forgetting by **hard gradient masking**: prune away redundant weights after each task, freeze the survivors, train the next task on the freed capacity, repeat.

## Source

Mallya, A. & Lazebnik, S. "PackNet: Adding Multiple Tasks to a Single Network by Iterative Pruning." CVPR 2018. [arXiv:1711.05769](https://arxiv.org/pdf/1711.05769)

## Method

**Iterative prune-freeze schedule.** Starting from a network trained on Task 1 (e.g., VGG-16 on ImageNet):

1. **Prune.** Remove the lowest-$|w|$ fraction of weights (e.g., 50 %) from every conv and FC layer. Weights are ranked by absolute magnitude; the bottom fraction is zeroed.
2. **Retrain.** Fine-tune on Task 1 for $\sim$half the original epochs to recover accuracy. The surviving weights form mask $M_1$.
3. **Freeze.** Lock all weights in $M_1$; they are ineligible for further modification or pruning.
4. **Train Task 2.** Allow the zeroed (pruned) weights to revive and train on Task 2. The Task 2 filter is the superposition of the frozen Task 1 weights plus the newly learned weights — shared representations carry over automatically.
5. **Prune Task 2 weights only** (e.g., 75 % of the Task 2 subset), retrain, freeze. This yields mask $M_2$.
6. Repeat for Task 3, 4, … until capacity is exhausted.

**Per-task mask.** At inference, apply the binary mask $M_k$ to reconstruct the weight state for Task $k$. No extra compute is needed — masking is a pointwise multiply during matrix ops. Task identity must be provided externally.

**Mask storage.** Because a parameter first used by Task $K$ is also used by Tasks $K{+}1, \ldots, N$, the mask can be encoded in $\log_2 N$ bits per parameter. For a 537 MB VGG-16 with 4 tasks, the total mask overhead is $\sim$34 MB — a $\sim$1/16 size increase vs. the base model.

Batch-norm statistics (running mean/variance, gain, bias) are frozen after the first prune-retrain round and shared across tasks; no per-task BN overhead is incurred.

## Claims

- **Four tasks in one VGG-16.** ImageNet + CUBS Birds + Stanford Cars + Oxford Flowers packed into a single 595 MB model (vs. 2,173 MB for four separate networks).
- **Near-individual accuracy.** With 75 % initial pruning, top-1 errors on the three fine-grained tasks are within 2.38 %, 1.78 %, and 1.10 % of individually trained networks.
- **Zero interference on prior tasks.** Frozen masks guarantee prior-task accuracy never changes after a new task is added — unlike EWC or LwF, where prior-task error drifts upward with each addition.
- **Beats LwF.** PackNet top-1 error: CUBS 24.95 %, Cars 15.75 %, Flowers 9.75 %; LwF: 30.42 %, 22.97 %, 15.21 % (Table 2).
- **Beats joint training.** ImageNet + Places365 in one model: PackNet ImageNet top-1 29.33 %, joint training 33.49 % (Table 3).
- **Generalizes across architectures.** Results hold on VGG-16 w/ BatchNorm, ResNet-50, DenseNet-121; ResNet-50 loses only 0.45 % ImageNet top-1 after pruning.

## Strengths

- Hard masks give a **provable non-interference guarantee** for prior tasks — a property that soft-penalty methods (EWC, LwF) cannot match.
- No replay data required; no proxy loss; always optimizes directly for the current task.
- Minimal storage overhead ($\log_2 N$ bits/param) compared to progressive network growth or separate model copies.
- Simple pruning criterion (magnitude) works at scale; more sophisticated pruning would only improve results.

## Weaknesses

- **Requires explicit task ID at inference.** The correct mask must be selected; the network cannot self-select the task.
- **Vision-era, classification-only.** All experiments are image classification on CNN backbones; no NLP, generative, or instruction-following settings.
- **Capacity shrinks with each task.** Later tasks receive fewer free parameters; order of training matters (error increases $\sim$3 % on average per position in the queue).
- **Weight-magnitude pruning is heuristic.** It does not directly optimize for future task capacity or for which weights are truly task-specific.
- **Simultaneous multi-task inference is impossible** with weight-level sparsity (filter-level pruning would allow it but cannot prune aggressively enough to fit multiple tasks).

## Relevance to This Wiki's Project

PackNet is **historical anchor, not direct method**. Its contribution to the current project is structural:

- It proved that **gradient masking to a per-task weight subset is sufficient to eliminate catastrophic forgetting** — the principle underlying every modern selective fine-tuning approach.
- The prune-then-freeze pattern is isomorphic to what LoRA adapters and orthogonal subspace methods do at a higher level of abstraction: restrict gradient flow to a task-specific subspace, freeze everything else.
- For the single-sample concept-learning setting, PackNet's hard mask is too coarse — it requires a full training run per task to discover the mask. The project's interest is in inferring the relevant subnetwork from one or a few examples. PackNet shows the destination (sparse, task-specific subnetwork) but not a path to get there from minimal data.

## Connections to the Wiki

**Within theme:**
- [[hat]] — HAT (CVPR-era sibling) learns a soft attention mask per task via sigmoid saturation rather than post-hoc pruning; both enforce gradient isolation but by different mechanisms.
- [[o-lora]] — modern descendant; replaces pruned weight subsets with orthogonal LoRA subspaces, achieving the same non-interference guarantee in the LLM regime without explicit task-indexed masks.
- [[skill-localization]] — extracts a sparse mask *after* fine-tuning (post-hoc attribution); PackNet *learns* the mask *during* training via pruning — complementary perspectives on where task-relevant weights live.
- [[surgical-finetuning]], [[dora]], [[pit]], [[lima]], [[mend]], [[rome]], [[memit]], [[alphaedit]], [[knowledge-neurons]], [[ff-kv-memories]], [[knowledge-editing-survey]] — share the concern of touching only the right weights for a given update; PackNet is the blunt-instrument ancestor.

**Across wiki:**
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — EWC uses Fisher-weighted $L_2$ penalty to soft-protect important weights; PackNet replaces the soft penalty with a hard binary mask. Two solutions to the same objective; PackNet's hard mask gives stronger guarantees but requires task identity at inference.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — Balashov finds that RL training spontaneously activates a sparse functional subnetwork; PackNet enforces an equivalent structure by design. The emergent/designed distinction is load-bearing for the proposed method.
- [[../synthesis/proposed-method]] — PackNet supplies the $R_w$ historical anchor: the idea that restricting gradient updates to a learned weight subset controls interference. The proposed method asks whether that subset can be identified from a single sample rather than a full training run.

## Related

- Han et al., "Learning Both Weights and Connections" (NIPS 2015) — magnitude pruning method PackNet builds on.
- Li & Hoiem, "Learning without Forgetting" (ECCV 2016) — distillation-based baseline that PackNet consistently outperforms.
- Kirkpatrick et al., "EWC" (PNAS 2017) — Fisher-regularization baseline; soft where PackNet is hard.
- Rusu et al., "Progressive Neural Networks" (2016) — growing-capacity alternative; avoids forgetting by never sharing weights across tasks.
