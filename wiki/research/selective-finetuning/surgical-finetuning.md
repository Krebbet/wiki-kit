---
title: "Surgical Fine-Tuning Improves Adaptation to Distribution Shifts"
authors: "Lee, Chen, Tajwar, Kumar, Yao, Liang, Finn"
year: 2023
venue: ICLR
tags: [selective-finetuning, layer-selection, distribution-shift, transfer-learning]
---

# Surgical Fine-Tuning Improves Adaptation to Distribution Shifts

Gradient applied selectively — but at layer granularity, not parameter granularity. Lee et al. show that freezing all but a contiguous subset of layers during fine-tuning (surgical fine-tuning) consistently matches or beats full fine-tuning under distribution shift, and that the optimal subset is determined by the *type* of shift: input corruptions want the first block tuned; output/label shifts want the last layer tuned; feature-level subpopulation shifts want middle blocks. The result is a direct prescription for which layers to touch when adding a capability while protecting others.

## Source

Lee, Y., Chen, A. S., Tajwar, F., Kumar, A., Yao, H., Liang, P., & Finn, C. (2023). Surgical fine-tuning improves adaptation to distribution shifts. *ICLR 2023*. arXiv:2210.11466.

## Method

Given a pre-trained model $f = f_n \circ \cdots \circ f_1(x)$ with per-layer parameters $\theta_i$, surgical fine-tuning solves:

$$\arg\min_{\theta_i,\, \forall i \in S} \hat{L}_\text{tgt}(f(\theta_1, \ldots, \theta_n))$$

where $S \subseteq \{1, \ldots, n\}$ is the chosen subset and all $\theta_i$ for $i \notin S$ are frozen at pre-trained values. The novelty is allowing $S$ to include *early* layers (e.g. $S = \{1\}$) — the opposite of standard last-layer fine-tuning.

**Automatic layer selection — Relative Gradient Norm (Auto-RGN).** Without cross-validation, layers are selected by their gradient-to-parameter ratio:

$$\text{RGN}_i = \frac{\|g_i\|_2}{\|\theta_i\|_2}$$

where $g_i$ is the flattened gradient of layer $i$ on the target loss. At each epoch, per-tensor RGN values are normalized to $[0,1]$ and used as a multiplicative scale on the base learning rate. This requires no extra hyperparameters and a single fine-tuning run. A second criterion, Signal-to-Noise Ratio (Auto-SNR), which measures gradient noise across a minibatch, also outperforms full fine-tuning on most tasks but is less reliable than Auto-RGN.

**Shift-to-layer mapping (empirical).**

| Shift type | Best block |
|---|---|
| Input-level (image corruption: CIFAR-C, ImageNet-C) | First block |
| Feature-level (subpopulation: Living-17, Entity-30) | Middle block |
| Output-level (spurious correlation / label flip: CIFAR-Flip, Waterbirds, CelebA) | Last layer |
| Natural (Camelyon17 — lighting across hospitals) | Embedding layer |
| Natural (FMoW — regional satellite) | Later attention blocks |

## Claims

- **Seven real-world tasks, three shift types:** Surgical fine-tuning (best block chosen by cross-val) outperforms full fine-tuning on all seven datasets spanning input-level, feature-level, and output-level shifts.
- **Auto-RGN without cross-val:** Auto-RGN achieves average rank 1.29 across datasets vs. 2.71 for full fine-tuning and ≥3.28 for all other single-run methods (gradual unfreezing, $L_1$ regularize, Auto-SNR).
- **First-layer beats full-tuning on CIFAR-C by ~3% accuracy** on average across corruptions, even in the few-shot regime down to 1 image per class.
- **Online unsupervised adaptation:** Surgical first-block tuning (online MEMO) reaches 75.5% on CIFAR-10-C vs. 69.7% for full online MEMO; full fine-tuning *deteriorates* as unlabeled test set grows while surgical tuning improves.
- **Theoretical result (Theorem 1, two-layer linear nets):** There exist $d, k, P_\text{src}, P_\text{trg}, n$ such that with high probability, first-layer tuning converges to zero target loss while full fine-tuning maintains non-zero loss throughout training — the head $v$ overfits to new input directions, corrupting previously learned directions outside the finite training set.
- **Proposition 1 (input perturbation):** For $x_\text{tgt} = Ax_\text{src}$ with invertible $A$, there exists a first-layer $B$ achieving zero target loss; no last-layer $v$ alone can do so.
- **Proposition 2 (label perturbation):** For $y_\text{tgt} = t y_\text{src}$, the last layer suffices; first-layer alone may not due to information destroyed by ReLU.
- **Synthetic noise experiment:** Adding noise to one specific block, then tuning only that block, outperforms tuning all blocks and full fine-tuning — tuning irrelevant layers actively hurts.

## Strengths

- Clean empirical taxonomy: shift type predicts optimal layer, replicated across architectures (ResNet-26, ResNet-50, CLIP ViT-B/16) and supervised + unsupervised settings.
- Auto-RGN is cost-efficient: one fine-tuning run, no added hyperparameters, beats full fine-tuning on 6/7 datasets.
- Theoretical grounding in two-layer nets is tight: Theorem 1 gives a provable case where surgical first-layer tuning wins, not just empirical correlation.
- Consistent with independent causal mechanisms (ICM) principle — shift locality in the causal graph maps to layer locality in the network.

## Weaknesses

- **Vision-centric throughout.** All empirical results use image classification benchmarks; no NLP or language model experiments. Generalization to transformer decoders with billions of parameters and text-shift scenarios is unvalidated.
- **Layer granularity, not parameter granularity.** The unit of selection is a convolutional block or attention block, not individual parameters or heads. Finer-grained methods (LoRA, PEFT, knowledge editors) can target specific weight matrices or neurons.
- **Cross-val oracle remains better.** Auto-RGN closes most of the gap but does not match exhaustive block search; a principled criterion that reliably identifies the optimal layer set without validation data remains open.
- **Contiguous subsets only.** The framework considers contiguous blocks; non-contiguous selection (e.g., first and last simultaneously) is not evaluated.
- **Small target dataset assumption.** Benefit shrinks as target data grows (Figure 3); surgical advantage is a small-data phenomenon.

## Relevance to This Wiki's Project

The proposed method $R_w$ (selective within-sample fine-tuning) needs a prescription for *which layers to update* given one training example. Lee provides exactly that at layer level: if the single sample encodes an input-domain shift (new style, new corruption), touch only the first block; if it encodes a new label relationship or capability boundary, touch the last layer. The Auto-RGN criterion is immediately applicable — compute gradient norms on the single target example and weight updates accordingly. The theoretical result (Theorem 1) is a direct warning: updating all layers on a single sample will forget source directions outside its span, exactly the catastrophic-forgetting risk $R_w$ must avoid.

## Connections to the Wiki

**Within selective-finetuning theme:**
- [[skill-localization]] — parameter-level localisation (mask or adapter per neuron); Lee operates at the coarser layer level, giving the empirical prior that motivates finer search.
- [[lima]] — LIMA's "format lives in SFT data, knowledge in pretraining" maps cleanly: format ≈ output-level shift → last layer; knowledge ≈ feature/input shift → earlier layers. Lee identifies which layer each one lives in.
- [[ff-kv-memories]] — Geva's finding that lower layers store surface/syntactic patterns and upper layers store semantic facts provides the mechanistic justification for Lee's empirical rule: input corruptions corrupt lower-layer representations → fix lower layers; concept/fact shifts live in upper layers → fix there.
- [[knowledge-neurons]], [[rome]] — ROME localizes factual knowledge to mid-layer FFN weights; Lee's empirical sibling at block granularity, confirming the same depth hierarchy from a transfer-learning direction.
- [[memit]], [[alphaedit]], [[mend]] — knowledge editors that update specific weight matrices; complement Lee by operating at finer granularity within the layers Lee identifies as relevant.
- [[o-lora]], [[dora]], [[pit]] — adapter / subspace methods that restrict *which parameters within a layer* are updated; Lee's block-level prescription tells them which layers to apply to.
- [[packnet]], [[hat]] — continual learning masks that freeze parameters for old tasks; Lee's shift-type→layer mapping gives a principled choice of which layers to freeze for which task.
- [[knowledge-editing-survey]] — survey framing of where edits should land; Lee's empirical taxonomy is a complementary data point.

**Existing wiki cross-refs:**
- [[../synthesis/proposed-method]] — $R_w$ uses Lee's layer prescription: one example, identify shift type, apply gradient only to the corresponding block.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — Balashov finds RL updates touch 5–30% of weights with characteristic layer patterns (earlier for value/representation, later for policy head); directly parallels Lee's supervised distribution-shift findings.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — further evidence of sparse layer activation under RL, complementing Lee's analysis.
- [[../single-sample-rl-finetuning/_overview]] — single-sample setting at layer level: Lee is the supervised analogue of what the RL papers show for reinforcement objectives.
- [[../decoding-time-steering/dola]] — DoLa contrasts early vs. late layer representations at *inference* to improve factuality; Lee chooses which layers to update at *training* — same depth intuition, different phase.

## Related

- Kumar et al. (2022) — LP-FT (linear probing then full fine-tuning); Lee cites this as motivation for why freezing can help.
- Kirichenko et al. (2022) — last-layer retraining suffices for spurious correlation; Lee generalizes to the full shift-type taxonomy.
- Howard & Ruder (2018) — ULMFiT gradual unfreezing; Lee shows that gradual unfreezing does not consistently outperform full fine-tuning, while surgical block selection does.
- Zhang et al. (2021) — MEMO test-time adaptation; Lee's surgical variant improves on it in the online setting.
