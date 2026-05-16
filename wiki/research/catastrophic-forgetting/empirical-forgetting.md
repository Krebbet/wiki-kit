---
title: "An Empirical Study of Catastrophic Forgetting in LLMs During Continual Fine-tuning"
arxiv: "2308.08747"
authors: "Luo, Yang, Meng, Li, Zhou, Zhang"
year: 2023
tags: [catastrophic-forgetting, continual-learning, instruction-tuning, empirical, background]
theme: catastrophic-forgetting
depth: background
---

# An Empirical Study of Catastrophic Forgetting in LLMs During Continual Fine-tuning

Luo et al. (2023) provide the first systematic empirical characterisation of catastrophic forgetting (CF) in generative LLMs subjected to sequential instruction fine-tuning. The study spans model scales 1b–7b, two architectures (decoder-only BLOOMZ vs. encoder-decoder mT0), and three classes of general knowledge — making it the SFT-forgetting baseline that later mitigation work (EWC-based CPT, RFT, RL-based methods) situates itself against.

## Source

- arXiv: [2308.08747](https://arxiv.org/abs/2308.08747)
- Raw capture: `raw/research/rlvr-forgetting/04-06-empirical-forgetting.md`

## Method

A base model $M_0$ is continually trained on a fixed task sequence of five instruction tasks: Text Simplification → Empathetic Dialogue → Inquisitive QG → Explanation Generation → Headline Generation (Simp → Emdg → InqQG → Exp → HGen). No replay or regularisation is applied — plain SFT at each step.

**Forgetting metric.** For each evaluation element $e$ in set $E_i$, let $R^e_0$ be baseline performance and $R^e_m$ performance after task $m$. The forgetting score is:

$$FG_i = \frac{1}{|E_i|} \sum_{e \in E_i} \frac{1}{N} \sum_{m=1}^{N} \frac{R^e_0 - R^e_m}{R^e_0} \times 100\%$$

**Evaluation axes.** Three suites probe general knowledge retention:
- Domain knowledge (MMLU, 5-shot)
- Reasoning (BoolQ, PIQA, Winogrande, Hellaswag, MathQA, Mutual — zero-shot)
- Reading comprehension (RACE-middle, RACE-high — zero-shot)
- Bias (CrowS-Pairs, as a secondary check)

**Models tested.** BLOOMZ (1.1b, 1.7b, 3b, 7.1b), mT0 (1.2b, 3.7b), LLAMA-7b, ALPACA-7b.

## Claims

1. **CF is universal.** All models exhibit positive $FG$ across all three evaluation axes. Reading comprehension suffers most ($FG$ up to 28.4% for mT0-3.7b), followed by domain knowledge, then reasoning.

2. **Forgetting intensifies with scale (1b–7b).** BLOOMZ $FG$ on domain knowledge: 9.5% (1.1b) → 10.7% (1.7b) → 14.6% (3b) → 18.4% (7.1b). Larger models start higher but converge to similar absolute endpoints, widening the relative gap.

3. **Decoder-only forgets less than encoder-decoder at matched scale.** At 3b scale: BLOOMZ-3b $FG_\text{reasoning} = 11.1$ vs. mT0-3.7b $FG_\text{reasoning} = 16.7$. The autoregressive training objective or capacity distribution is hypothesised as the cause.

4. **Prior general instruction tuning acts as a buffer.** ALPACA-7b (instruction-tuned LLAMA) shows markedly lower $FG$ than raw LLAMA-7b (e.g., reasoning $FG$ 7.6 vs. 31.3). BLOOMZ vs. BLOOM shows a weaker version of the same effect, confounded by large initial-performance gaps.

5. **Mixing general instruction data during continual training mitigates CF.** Adding 10K ALPACA samples to each continual task's training data recovers partial performance (e.g., LLAMA MMLU-human: 26.8% → 30.0% vs. 34.7% baseline).

6. **Bias is incidentally reduced.** Bias $FG$ values are mostly positive — stereotype preferences erode during continual instruction tuning, a side-effect rather than a design goal.

## Strengths / Novelty

- First work to measure CF in *generative* LLMs on *general* knowledge benchmarks (prior work focused on encoder-only models or task-specific forgetting only).
- Clean, reproducible setup: fixed task order, public models, open evaluation harness (lm-evaluation-harness).
- Multi-axis evaluation avoids the single-metric traps that can miss partial forgetting.

## Weaknesses / Limits

- Scale ceiling at 7b; the paper notes that larger models (70b+) may require fewer parameter changes to fit new tasks, potentially changing the scale–forgetting relationship.
- Single task order (Simp → … → HGen). Task-order sensitivity is acknowledged but not studied.
- Models and tasks are multilingual / eclectic; may not generalise to monolingual domain-specialisation scenarios.
- No mechanistic analysis — CF is measured, not explained at the parameter or circuit level.
- 2023 vintage: predates the now-standard practice of training with RLVR; all results are pure SFT.

## Relevance to this wiki's project

**Anchoring question:** "Does stacking skills via fine-tuning just move optimisation around?"

This paper says: yes, empirically. Sequential SFT pushes parameters toward each new task's distribution and the model converges to similarly poor performance on held-out general knowledge regardless of initial scale — consistent with a fixed-capacity hypothesis where new skill acquisition cannibalises existing representations. The $FG$ metric operationalises "moving optimisation around" as a measurable quantity. The ALPACA vs. LLAMA result hints that a richer initial parameter landscape (prior instruction tuning) slows the displacement. This is the SFT-forgetting floor our project's single-sample optimisation regime must beat or at minimum characterise.

## Connections to the wiki

- [[_overview]] — theme anchor; this paper is the empirical baseline node
- [[ewc-gemma2-cpt]] — EWC-based CPT attempts to address the same SFT-forgetting regime documented here
- [[rls-razor]] — RL-based fine-tuning forgets substantially less than SFT; this paper provides the SFT baseline that makes RL's Razor's claims meaningful
- [[rft-mitigates-forgetting]] — RFT-based approaches use this study as the problem specification they target
- [[path-not-taken]] — alternative forgetting trajectories; contrast with the fixed-order result here
- [[mechanistic-forgetting]] — circuit-level analysis of *why* the forgetting pattern above occurs
- [[rft-data-perspective]] — data-mixing finding (§5.4) anticipates the data-curation angle studied there
- [[../selective-finetuning/_overview]] — selective / sparse fine-tuning is a direct structural response to the global parameter displacement shown here
- [[../synthesis/proposed-method]] — the $FG$ metric and scale findings inform what the proposed method must demonstrate it does not replicate

## Related

- Scialom et al. (2022) — "Fine-tuned language models are continual learners"; task-specific CF precursor this paper extends to general knowledge
- Luo et al. (2023b) — same group's probing study on encoder-only models; motivation for expanding to generative LLMs
- Muennighoff et al. (2022) — BLOOMZ / mT0 model family used throughout
- McCloskey & Cohen (1989) — original catastrophic interference characterisation in neural nets (background)
