# In-Context Reinforcement Learning with Algorithm Distillation

Laskin, Wang, Oh, Parisotto, Spencer, Steigerwald, Strouse, Hansen, Filos, Brooks, Gazeau, Sahni, Singh, Mnih (DeepMind, 2022). Distils gradient-based RL algorithms into a causal transformer by behaviour-cloning *across-episode learning histories*. The resulting model performs RL **entirely in-context** — no weight updates at deployment — and learns a *more data-efficient* algorithm than the source RL (UCB, A3C, DQN) it was distilled from.

## Method
Treat an RL "algorithm" as a long-history-conditioned policy P: H ∪ O → Δ(A) where h_t = (o_0, a_0, r_0, ..., o_t, a_t, r_t).

1. **Dataset generation**: for N tasks {M_n} sample from a task distribution. Run a source RL algorithm P^source on each until convergence; save the *full learning history* (state-action-reward stream from random init through expert).
2. **Algorithm distillation**: train a causal transformer (GPT-style) by minimising the action-prediction NLL
   L(θ) = − Σ_n Σ_t log P_θ(a_t^(n) | h_{t−1}^(n), o_t^(n))
   on across-episodic subsequences of length c < T sampled from D. **Critical**: c must span multiple episodes so the model sees policy improvement within a single context window. AD models (s, a, r) tokens; **does not** condition on returns (unlike Decision Transformer).
3. **Evaluation**: roll out the transformer in-context — context = queue of last c transitions; weights frozen. Adaptation happens through context accumulation.

## Claims
- **Adversarial Bandit (10-arm, 100 trials)**: AD matches RL² in-distribution and *generalises better* to OOD reward distributions where RL² fails (Fig. 3). Source: UCB.
- **Dark Room / Dark Room Hard / Dark Key-to-Door**: AD in-context RLs across all environments; matches asymptotic RL² (1B env-step upper bound) on Dark variants and reaches within 13% on Watermaze (Fig. 4). Source: A3C (Dark) / DQN (Watermaze).
- **Data efficiency**: AD is *more data-efficient than its source* — single-stream evaluation against multi-stream A3C/DQN (Fig. 4). Even when distilling subsampled (every 10th episode) single-stream A3C, AD still beats the source's per-actor sample efficiency (Fig. 6).
- **Demonstrates exploration, credit assignment, generalisation**: Dark Room Hard has *r=1 exactly once per episode* — AD still infers the goal from prior episodes in context. Dark Key-to-Door has 6,561 tasks, ~2k seen at training; AD hits near-optimal on unseen tasks.
- **Demonstration prompting** (Fig. 5): pre-filling the context with a partial-policy demo *accelerates* AD; ED (expert distillation) merely *maintains* the input policy without improving.
- **Context size required** (Fig. 7): in-context RL emerges only with multi-episodic contexts (≥ 2–4 episodes). One-episode contexts produce no RL behaviour.
- **DMLab Watermaze** (pixel-based 3D POMDP): AD in-context RLs from raw pixels; ED fails entirely.
- **Asymptotic ceiling**: source algorithm slightly outperforms AD asymptotically, but each source produces N task-specific weight sets while AD is a single generalist.

## Sample efficiency
Per-deployment-task sample efficiency is set by how quickly the in-context RL algorithm AD has *internalised* converges — empirically faster than the gradient-based source. But cost is paid up front: pre-training requires complete learning histories from many tasks (2,000 A3C runs to convergence on Dark; 4,000 distributed DQN runs on Watermaze). Single-sample applicability is **negative on its face**: AD cannot acquire a new concept from one example because no weights update. However, with sufficient context AD can extract *behavioural* improvement from a single trajectory of trial-and-error — analogous to one-shot learning *via reasoning* rather than via parameter change. The "single sample" must be a multi-step interactive episode, not a static (x, y) pair.

## Relevance to the project
AD is the canonical demonstration that **a learning algorithm itself can live in-context** — adaptation entirely without weight updates, given a long enough context window. For David's project this is the diametric alternative to fine-tuning: rather than baking a new concept into weights from one example, expose a long enough context that the model *runs its own learning loop* over the example. Practical concerns: (a) AD needs a meta-training corpus of *learning histories* — David would need an analogous corpus of "concept acquisition trajectories" (e.g., self-correction traces, RL-on-one-example replays); (b) AD's improvements are **ephemeral** — close the context and the learned policy is gone. Hybrid: use AD-style in-context RL to discover the concept, then distil the resulting context-conditioned behaviour into weights via [[ttt-few-shot]]-style per-input fine-tuning. The Chen et al. (2022) hyperparameter-optimiser-as-sequence-model is the most direct precedent for "incremental in-context learning" beyond demonstrations.

## Source
- arXiv: 2210.14215 (ICLR 2023)
- Raw markdown: `../../../raw/research/single-sample-llm-learning/24-E-2-algorithm-distillation-icrl.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/E-2-algorithm-distillation-icrl.pdf`

## Related
- [[ttt-few-shot]] — opposite axis: adaptation via *temporary weight updates* per test input.
- [[_overview]] — theme synthesis comparing in-context vs in-weight RL paths to single-sample concept learning.
- [[maml]] — gradient-based meta-RL contrast (in-weights, optimisation-based vs AD's in-context behaviour-cloning).
