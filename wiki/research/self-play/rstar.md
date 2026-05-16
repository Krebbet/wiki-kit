---
name: rstar
description: rStar augments a small LLM at test time with MCTS over five human-like reasoning actions, then validates trajectories via a peer-sized discriminator SLM using partial-hint completion agreement. No fine-tuning; lifts LLaMA2-7B from 12.51% to 63.91% on GSM8K. Predecessor of rStar-Math. Drop-in template for per-problem diversity generation (proposed-method component G).
type: research
---

# rStar: Mutual Reasoning at Test Time

Zhenting Qi, Mingyuan Ma, Jiahang Xu, Li Lyna Zhang, Fan Yang, Mao Yang. Microsoft Research Asia / Harvard University. *Mutual Reasoning Makes Smaller LLMs Stronger Problem-Solvers.* arXiv:2408.06195, August 2024. **TL;DR:** MCTS over a five-action reasoning space plus a frozen peer-sized discriminator SLM that verifies trajectories by independently completing partial hints — no fine-tuning, no ground-truth labels, no teacher model. At inference alone, small LLMs match fine-tuned baselines.

## Method

### MCTS search

For problem $x$ and target SLM $M$, MCTS builds a tree rooted at $x$; edges are actions, nodes are reasoning steps $s_i$. A leaf path $t = x \oplus s_1 \oplus \cdots \oplus s_d$ is a candidate trajectory. Node selection uses UCT:

$$\text{UCT}(s, a) = \frac{Q(s, a)}{N(s, a)} + c\sqrt{\frac{\ln N_\text{parent}(s)}{N(s, a)}}$$

32 rollouts per problem; depth $d = 5$ (most tasks) or $d = 8$ (MATH); branching factor up to 5 for A1 and A3, default 1 for others. Intermediate node rewards are not self-evaluated (SLM self-rewarding is shown to be near-random); terminal nodes receive majority-voting confidence back-propagated as $Q(s_i, a_i) \mathrel{+}= Q(s_d, a_d)$.

### Five reasoning actions

- **A1** — propose a single next reasoning step (granular; ToT-style).
- **A2** — propose all remaining steps in one shot ("fast thinking" for simpler sub-problems).
- **A3** — propose next sub-question and immediately answer it (least-to-most decomposition; RAP-style).
- **A4** — re-answer a sub-question from A3 with few-shot CoT, correcting A3 errors.
- **A5** — rephrase the problem by listing all conditions explicitly (addresses misread-condition failure mode).

Ordering constraints: A4 only follows A3; A5 only applies at root or sub-question. Ablation (Table 1, LLaMA3-8B, 200 GSM8K samples): full $\{A1\text{–}A5\}$ achieves 75.0% vs. 70.5% for A3 alone; each action contributes incrementally.

### Discriminator SLM — mutual consistency check

A second SLM $\hat{M}$ (Phi3-mini-4k, 3.8B in main experiments; self-discrimination for Phi3 target) receives a partial trajectory and completes it independently. For candidate $t = x \oplus s_1 \oplus \cdots \oplus s_d$, a split point $i \sim \text{Uniform}[0.2d,\, 0.8d]$ is sampled; $\hat{M}$ receives the prefix $x \oplus s_1 \oplus \cdots \oplus s_{i-1}$ and generates the remainder. If $\hat{M}$'s answer matches $t$'s answer, the trajectory is *mutually consistent* and admitted to the validated set. Final answer: the trajectory in the validated set maximising reward × terminal-node confidence.

Discriminator quality (Table 5): Phi3-mini discriminator achieves 91.13% for LLaMA3-8B-Instruct vs. GPT-4 discriminator at 92.57% — a 1.44 pp gap, confirming that a peer-sized frozen SLM is nearly as effective as a frontier model.

## Claims

| Model | Few-shot CoT | rStar |
|---|---|---|
| LLaMA2-7B | 12.51% | **63.91%** |
| Mistral-7B | 36.46% | **81.88%** |
| LLaMA3-8B | 47.23% | **85.52%** |
| LLaMA3-8B-Instruct | 74.53% | **91.13%** |

*(GSM8K, Table 2. Self-consistency @128 reaches only 23.05% for LLaMA2-7B; rStar outperforms SC@maj128 by +40.86 pp.)*

- MATH-500 (LLaMA3-8B-Instruct): 17.80% → 42.94%. (Phi3-mini: 32.20% → 48.60%).
- StrategyQA gains modest: +6–8 pp — structured decomposition matters more for formal reasoning.
- Mistral-7B rStar (81.88%) matches fine-tuned MetaMath (77.70%) without any teacher LLM or gradient update.

## Why this is load-bearing for single-sample concept learning

rStar is the canonical **per-problem multiplier**: one seed $(Q, A)$ → a tree of 32 trajectories covering decompositions, rephrasings, re-answers, and partial CoT chains — all in context, weights frozen.

The five actions map directly onto the manipulations a concept-learner should perform: A3 decomposes the concept into sub-questions, A5 re-encodes it with all conditions stated, A4 re-answers to check consistency, A1/A2 explore the reasoning path at different granularities. The resulting tree is a micro-curriculum derived from a single seed — exactly the diversity component G of [[../synthesis/proposed-method]] requires.

The discriminator-completion-agreement check is a **frozen-weights verifier** requiring no annotations and no reward model. It is structurally identical to what the concept-curriculum method needs: a way to validate whether an intermediate reasoning step genuinely captures the concept, without labelled examples. The check works because partial-hint consistency is an information-theoretic proxy for "does this trajectory stay on a coherent path through concept space."

This makes rStar a **drop-in template for component G**: wrap any forward pass in the MCTS loop, use the peer SLM's partial-completion agreement as the verification signal. No training data, no gradient — pure test-time search over one instance.

## Limitations

- Inference cost: 32 rollouts at depth 5–8 plus parallelised discriminator passes is orders of magnitude heavier than single-pass CoT. Not practical for high-throughput settings.
- A second SLM of comparable capability must be available; for the smallest models, self-discrimination weakens the independence assumption.
- Five actions were designed for math and commonsense reasoning; coverage of relational, procedural, or perceptual concepts is untested.
- Reward signal requires an extractable discrete final answer; open-ended or partial-credit tasks have no obvious analogue.
- StrategyQA gains modest (~6–8 pp vs. ~50 pp on GSM8K): the action space is less suited to loosely-structured commonsense tasks.

## Source

- `../../../raw/research/self-play-quality-extraction/.ingest/07-rstar.md`
- `../../../raw/research/self-play-quality-extraction/03-07-rstar.md`
- arXiv: https://arxiv.org/abs/2408.06195

## Related

- [[../self-improvement/rstar-math]] — rStar-Math (successor): adds process-reward model training on top of rStar's trajectory pipeline; the fine-tuning version of this paper's test-time-only approach
- [[../self-improvement/multi-turn-policy-verifier]] — PAG: train-time actor + verifier alternation; rStar shows the same architecture works frozen at inference
- [[spell]] — SPELL three-role decomposition; rStar collapses Verifier into the discriminator SLM rather than training a third role
- [[../test-time-training/_overview]] — other test-time multipliers; rStar is structured-search rather than gradient-based TTT
- [[../synthesis/proposed-method]] — component G (diversity injection); rStar MCTS + five-action space is a ready-made template
- [[_overview]]
