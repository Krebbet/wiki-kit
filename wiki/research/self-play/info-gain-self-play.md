---
name: info-gain-self-play
description: Formalises when self-play loops evolve vs. stagnate via epiplexity — the learnable fraction of MDL under bounded observer capacity C and inference budget T. Self-play evolves only when S_{C,T} increases monotonically across iterations. Provides a pre-flight audit (Algorithm 1) and quantifies the AZR induction/abduction/deduction asymmetry (3–4× gap).
type: research
---

# Info-Gain Self-Play: Epiplexity and the Learnable-Information Criterion

Wei Liu, Siya Qi, Yali Du, Yulan He. King's College London / The Alan Turing Institute. *Self-Play Only Evolves When Self-Synthetic Pipeline Ensures Learnable Information Gain.* arXiv:2603.02218, 2026. **TL;DR:** Self-play stagnates not because of reward design failures but because the synthetic pipeline fails to ensure monotonically increasing *learnable information* — structure that a bounded observer can extract and compress. The paper formalises this as epiplexity $S_{C,T}$, provides a computable audit (Algorithm 1), and uses it to explain collapse modes and the induction/abduction/deduction asymmetry observed in Absolute Zero Reasoner.

## Method

### Epiplexity — the learnable fraction of MDL

The bounded MDL optimiser over programs $P$ with parameter capacity $C$ and inference budget $T$ is:

$$P^* = \arg\min_{P \in \mathcal{P}_{C,T}} \left[ |P| + \mathbb{E}\log\frac{1}{P(X)} \right]$$

This decomposes into:

$$\underbrace{S_{C,T}(X)}_{\text{epiplexity}} := |P^*| \qquad \underbrace{H_{C,T}(X)}_{\text{bounded entropy}} := \mathbb{E}\log\frac{1}{P^*(X)}$$

$$\text{MDL}_{C,T}(X) = S_{C,T}(X) + H_{C,T}(X)$$

$S_{C,T}(X)$ is the minimum description cost the bounded observer must pay to compress $X$ — reusable structure that survives gradient descent. $H_{C,T}(X)$ is the residual that the observer cannot compress: observer-bounded noise. The split is observer-relative: the same dataset can be information-rich for a small model and trivially memorisable for a large one.

**Central claim:** Self-play evolves if and only if $S_{C^{(t)},T^{(t)}}(X^{(t)})$ increases monotonically across iteration $t$. Reward improvement and task-metric improvement are necessary but not sufficient: reward hacking and memorisation both improve metrics while leaving $S_{C,T}$ flat.

### Algorithm 1 — prequential MDL audit

Estimate $S_{C,T}$ via prequential (online) MDL coding: train an observer LLM on the synthetic dataset with sequential batch updates; accumulate first-pass online loss (before each update); select the epoch minimising $S/N_\text{train} + (L_\text{val}/\ln 2)/N_\text{val}$. Fully computable from the observer LLM and the candidate dataset — no ground-truth labels. Use as a **pre-training audit** on candidate synthetic batches before committing to an inner-loop training run.

## Claims

- **Stronger PROPOSER → higher epiplexity:** Qwen3 4B $>$ Qwen2.5 14B $>$ Qwen2.5 7B PROPOSER, consistent across all three task directions (Figure 5; absolute values 80k–340k token-bits depending on direction and model size).
- **Induction asymmetry:** Induction epiplexity $\approx$ 250k–340k token-bits; abduction $\approx$ 80k–130k; deduction $\approx$ 80k–130k at matched PROPOSER/SOLVER sizes. **Induction is 3–4× more information-dense than abduction or deduction** — directly quantifying why AZR's math performance drops most when induction is removed.
- **Non-monotone epiplexity vs. SOLVER size:** Peaks at an intermediate size ($\sim$7B–14B for these setups), then declines as the model switches from pattern compression to direct memorisation. Scaling SOLVER size past the sweet spot reduces learnable information.
- **Self-play iterations (Experiment 2, AZR setup):** Epiplexity fluctuates between $\approx$ 40k and $\approx$ 450k without stabilising — multi-reward RL alone is insufficient for monotonic information gain. Confirmed collapse modes: trivial-task drift, cycling, capacity saturation.

## Why this is load-bearing for single-sample concept learning

**Pre-flight check before any self-play implementation.** Run Algorithm 1 on the candidate synthetic dataset before inner-loop training. If $S_{C,T}$ is not rising monotonically, fix the proposer strength, synthetic direction, or SOLVER capacity first — reward optimisation on low-epiplexity data will not drive structural learning.

**Refines the proposer-is-everything framing** ([[understanding-self-play]]): the PROPOSER sets the ceiling on epiplexity, but a PROPOSER that generates tasks beyond the SOLVER's current capacity produces data where $H_{C,T}$ dominates and $S_{C,T} \approx 0$ — indistinguishable from noise at that observer scale. The criterion adds the Goldilocks constraint: proposer quality must be co-calibrated against SOLVER capacity and synthetic direction at each iteration.

**Direct relevance to component G (diversity injection) of [[../synthesis/proposed-method]]:** Diversity that falls outside the learnable range contributes to $H_{C,T}$ (noise), not $S_{C,T}$ (structure). For single-sample concept learning, where every synthetic example is load-bearing, a diversity injection that increases $H$ without increasing $S$ actively degrades the loop. The epiplexity check makes this concrete and measurable.

**Quantitative answer for why induction is load-bearing in AZR.** The 3–4× epiplexity gap explains empirically why removing induction from AZR hurts math most: induction tasks carry structurally richer signal than abduction or deduction at the same SOLVER scale. This translates directly to the concept-learning context: inductive tasks (given examples, infer the concept) are the highest-density training signal and should anchor the synthetic curriculum.

**Connection to Stage 2 dynamics** ([[two-stage-dynamic]]): epiplexity operationalises the "non-trivial fraction" of the Stage 2 expansion budget. Stage 2 can increase Pass@$k$ at large $k$, but only if the additional probability mass is directed at trajectories with high $S_{C,T}$ — otherwise the new diversity is unlearnable noise.

## Limitations

- Asymmetric co-evolution is currently most tractable in easy-to-verify domains (math, code). Hard-to-verify domains (open-ended generation, creative tasks) lack the clean VERIFIER required to close the loop.
- Epiplexity is a macroscopic structural measure: high $S_{C,T}$ does not guarantee task-relevant structure — the measure and task-accuracy metrics must both be monitored.
- Computing Algorithm 1 requires a full fine-tuning pass with online loss accumulation; non-trivial to embed inside a real-time training loop. No lightweight proxy or early-stopping estimate is proposed.
- The three designed mechanisms (asymmetric co-evolution, capacity growth, proactive seeking) are presented as a synergistic system without individual ablations — their independent contributions are not isolated.
- Proactive information seeking requires the model to recognise what it does not know; formulating the right retrieval query from SOLVER failures is itself an open problem.

## Source

- `../../../raw/research/self-play-quality-extraction/.ingest/08-info-gain-self-play.md`
- `../../../raw/research/self-play-quality-extraction/04-08-info-gain-self-play.md`
- arXiv: https://arxiv.org/abs/2603.02218

## Related

- [[understanding-self-play]] — proposer-is-everything framing refined: proposer quality is necessary but not sufficient; epiplexity adds the Goldilocks constraint on SOLVER capacity and synthetic direction
- [[azr]] — AZR three-mode setup; epiplexity quantifies why induction removal hurts math most (3–4× asymmetry)
- [[../synthesis/proposer-reward-shapes]] — info-gain criterion unifies the six reward shapes: each is a different mechanism for keeping $S_{C,T}$ in the learnable regime
- [[../synthesis/proposed-method]] — component G pre-flight: epiplexity audit as go/no-go gate before expanding the diversity-injection loop
- [[../rlvr-mechanics/learning-to-think]] — Fisher information-gain as a related per-step signal; epiplexity is the dataset-level analogue
- [[invisible-leash]] — info-gain criterion identifies the non-trivial fraction of Stage-2 expansion budget; Stage 2 gains are only real if the recovered probability mass has high $S_{C,T}$
- [[two-stage-dynamic]] — Stage 2 exploration creates new probability mass; epiplexity determines whether that mass is learnable or noise
- [[_overview]]
