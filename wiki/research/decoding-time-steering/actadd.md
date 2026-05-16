---
title: "ActAdd: Activation Addition"
aliases: ["ActAdd", "Activation Addition", "Activation Engineering"]
tags: [decoding-time-steering, activation-engineering, single-sample, concept-as-direction, inference-time]
arxiv: "2308.10248"
authors: ["Alexander Matt Turner", "Lisa Thiergart", "Gavin Leech", "David Udell", "Juan J. Vazquez", "Ulisse Mini", "Monte MacDiarmid"]
year: 2023
venue: "ICLR 2024 (workshop / preprint)"
---

# ActAdd: Steering Language Models with Activation Engineering

Turner et al. (2023) introduce **Activation Addition (ActAdd)**: inject a contrast-pair steering vector into a frozen model's residual stream at inference time, with zero optimisation and as few as two prompts. It achieves SOTA toxicity reduction and sentiment control on OPT and LLaMA-3 while preserving off-target capability — establishing the **$n=1$ pair limit** of the activation-steering family as both practically sufficient and theoretically informative.

## Source

Turner, A. M., Thiergart, L., Leech, G., Udell, D., Vazquez, J. J., Mini, U., & MacDiarmid, M. (2023). *Steering Language Models with Activation Engineering*. arXiv:2308.10248. ICLR 2024 workshop / preprint.

## Method

**Step 1 — compute the steering vector** (before inference, two forward passes, no gradients):

Given a contrast pair $(p^+, p^-)$ differing along a single target dimension (e.g. "Love" vs "Hate"), record residual-stream activations at layer $l$ and take their difference:

$$\mathbf{h}_A^{[l]} = \mathbf{h}_+^{[l]} - \mathbf{h}_-^{[l]}$$

**Step 2 — inject at inference** (one more forward pass, no gradients):

At the chosen sequence position $a$ in the user prompt's residual stream, add the scaled vector:

$$\mathbf{h}^{[l]} \leftarrow \mathbf{h}^{[l]} + c \cdot \mathbf{h}_A^{[l]}$$

The forward pass then continues normally from layer $l$ onward. Two free hyperparameters — injection coefficient $c$ and layer $l$ — are selected by sweep; middle layers are typically most effective, consistent with prior work on steering vectors.

## Claims

- **Extreme data efficiency**: requires as few as 2 samples (the contrast pair); ITI (Li et al. 2023) by contrast requires dozens of labelled samples plus trained linear probes.
- **SOTA toxicity reduction**: ActAdd-OPT achieves toxicity 0.112 on RealToxicityPrompts ($n=1000$), 8% below the next-best OPT intervention (PREADD-D at 0.122, $p<0.05$); ActAdd-LLaMA-3 reaches 0.108.
- **SOTA negative→positive sentiment**: ActAdd-LLaMA-3 achieves 0.669 sentiment-flip success on IMDb ($p<0.05$ vs second-best).
- **Off-target capability preservation**: negligible ConceptNet P@K impact across $K=1$–$100$ under the wedding steering vector.
- **Composability**: works despite the model never being trained for activation addition — evidence for linear, compositional structure in the residual stream.

## Strengths

- **Zero labelled data**: the contrast pair is two hand-written prompts; no annotation pipeline required.
- **No optimisation**: no backward passes, no training loop, no per-query gradient search — purely algebraic.
- **Continuous weighted control** via $c$: finer-grained than discrete prompting; the steering magnitude is a dial, not a switch.
- **Modular**: the frozen base weights are untouched and reusable; multiple steering vectors can in principle be composed.
- **Origin-point status**: earliest paper to demonstrate "prompt-pair difference → residual-stream injection" at scale on modern LLMs; CAA, RepE, and in-context vectors all extend from this base.

## Weaknesses

- **White-box access required**: residual stream must be readable and writable; not API-compatible.
- **Hyperparameter sensitivity**: both $c$ and $l$ must be tuned; layer-sweep is non-monotone and varies by model and task (GPT-2-XL wedding vector peaks at layer 6, declines after).
- **Cannot teach new skills**: authors are explicit — ActAdd steers within the model's existing representational space; it cannot add capability absent from pretraining.
- **Reasoning tasks unexamined**: experiments cover toxicity, sentiment, and topic steering; impact on structured reasoning is not evaluated.
- **Fluency cost**: all steering methods incur disfluency; ActAdd's penalty (13.8 for OPT toxicity) is lower than PREADD (56.6) but non-zero.

## Relevance to this wiki's project

ActAdd is the canonical **single-pair-of-points limit of activation steering** — the extreme data-efficiency end of the CAA / RepE family and a direct load-bearing existence proof for two threads of this wiki's central question.

**$R_w$ hypothesis**: ActAdd shows that $\mathbf{h}_+^{[l]} - \mathbf{h}_-^{[l]}$ from *two forward passes* is causally sufficient to produce a measurable behavioural shift. No optimisation, no labelled set, no probe training. If $R_w$ asks whether a single residual-stream direction can encode a concept's write signal, ActAdd is the floor existence proof: yes, one difference vector suffices.

**Invisible Leash by construction**: no gradient update + two in-distribution prompts = zero support shift on the base distribution. The steered model remains within the model's existing geometry. Theorem C.1 (no-distribution-shift condition) holds trivially — there is nothing to shift from.

Within the single-sample family, ActAdd occupies the **activation-level slot**: vs. token-level ICL, and vs. weight-level LoRA / MAML. It is the decoding-time-steering sibling to the weight-update methods in [[../single-sample-rl-finetuning/_overview]].

The proposed method asks whether *one gradient step* can learn a direction equivalent to the hand-crafted contrast-pair difference. ActAdd establishes that the target direction exists and is behaviourally effective — which is the precondition the proposed method must satisfy before asking whether gradient-based recovery is feasible or superior.

## Connections to the wiki

- [[../single-sample-rl-finetuning/_overview]] — ActAdd is the activation-level instance of the single-sample family; slot it against single-step LoRA / MAML as the zero-gradient alternative.
- [[../synthesis/proposed-method]] — ActAdd's contrast-pair vector is the existence proof for $R_w$; the proposed method's question is whether a single gradient step recovers (or improves on) this direction.
- [[../concept-learning/_overview]] — "concept as direction in residual stream" is the shared assumption; ActAdd operationalises it without any probe training.
- [[../self-improvement/invisible-leash]] — ActAdd satisfies the no-support-shift condition by construction; strongest possible instance of the leash holding.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — sparse subnetwork hosts the directions ActAdd recovers; ActAdd is agnostic to subnetwork structure but consistent with it.
- [[caa]] — direct scale-up of ActAdd: CAA averages many contrast pairs; ActAdd is the $n=1$ special case.
- [[iti]] — head-level cousin needing dozens of samples + trained linear probes; ActAdd is the zero-probe, two-sample alternative.
- [[repe]] — umbrella framework; ActAdd is the Contrast Vector instance within RepE's taxonomy.
- [[linear-rep-hypothesis]] — Park et al. Theorem 2.5 provides the formal warrant: adding a concept direction to the residual stream steers the represented concept; ActAdd is the empirical demonstration.

## Related

[[contrastive-decoding]] · [[cd-improves-reasoning]] · [[dexperts]] · [[gedi]] · [[fudge]] · [[pplm]] · [[dola]] · [[cfg-lm]]
