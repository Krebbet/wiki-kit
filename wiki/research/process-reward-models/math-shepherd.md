# Math-Shepherd: Verify and Reinforce LLMs Step-by-Step Without Human Annotations

Wang et al. (Peking U / DeepSeek) propose an MCTS-style automatic process annotation that defines step quality as "potential to reach the gold answer," estimated by rolling out N completions per step from a fine-tuned completer. The resulting PRM beats human-annotated PRM800K on MATH despite using zero human step labels, and step-by-step PPO with Math-Shepherd lifts Mistral-7B from 77.9 to 84.1% on GSM8K and 28.6 to 33.0% on MATH (greedy), reaching 89.1% / 43.5% with verification reranking. Demonstrates that the PRM data-collection bottleneck is dissolvable.

## Method
- Step quality definition: q(s_i) = potential of step i to deduce correct final answer (MCTS-rollout intuition).
- Completer: a finetuned LLM (e.g., LLemma-7B) decodes N=8 subsequent reasoning completions from each prefix.
- Hard estimation (HE): label step positive if any rollout reaches a*; soft (SE): fraction reaching a*.
- PRM trained as binary classifier with cross-entropy on these auto-labels (HE used in main experiments because it slots into a standard LM pipeline via two special tokens).
- Two deployment modes:
  1. **Verification (best-of-N):** solution score = min over step scores; optionally combined with self-consistency via SC+RM weighted vote.
  2. **Step-by-step PPO:** PRM provides reward at the end of each reasoning step (vs. ORM's terminal-only reward). KL coef 0.04.
- Data scale: ~170K solutions GSM8K, ~270K MATH, generated from 7B/13B models trained on MetaMath.

## Claims
- DeepSeek-67B + Math-Shepherd verification: 93.3% GSM8K, 48.1% MATH (Table 1) — SOTA among open-source no-tool models at publication.
- Mistral-7B step-by-step PPO: 77.9 → 84.1% GSM8K, 28.6 → 33.0% MATH greedy (Table 2); +verification → 89.1 / 43.5 (Table 3).
- Math-Shepherd PRM > human PRM800K on MATH at the same generator distribution (Fig. 3) — attributed to distribution match (PRM800K labelled GPT-4 traces, Math-Shepherd labels MetaMath traces) plus 4x data volume.
- PRM > ORM gap widens on harder MATH vs. easier GSM8K, consistent with [[lets-verify-step-by-step]] and [[process-outcome-feedback]].
- Annotation quality: HE accuracy 86% at N=4 vs. human labels (Fig. 4a) on GSM8K; SE converges closer to human distribution as N grows (Fig. 4b).
- Hungarian-exam OOD: PRM beats ORM by 9 points (Fig. 6b).
- Sample efficiency: PRM beats ORM by ~4 points at 10K examples and dominates at every scale tested (Fig. 6a).

## Sample efficiency
- Zero human step annotations — only gold final answers (which exist for free in math datasets).
- Per-step compute cost: N completer rollouts per labelled step. With N=8 and ~270K solutions on MATH, this is the dominant compute. The paper flags this as the main limitation but notes vLLM / speculative decoding can amortise.
- Reward-model training set sizes (10K–270K) match what's feasible for a single research lab; PRM advantage manifests by 10K.
- Verification at deployment: 256 candidates per problem in headline numbers (more expensive than ORM-style scalar scoring of one trace).

## Relevance to the project
Most directly actionable paper for the project. Shows that MCTS-style rollouts give per-step credit signals as good as (or better than) human PRM labels — i.e., concept-component reward can be bootstrapped from outcome verifiability without needing a labeller. Design implications:
1. If concept components are intermediate states whose downstream completion can be sampled and graded, soft-estimation rewards yield naturally fractional partial-credit.
2. Step-by-step PPO is the recipe for actually optimising against such rewards (terminal PPO drops most of the signal).
3. Completer quality matters — supervising components requires a model strong enough on the same distribution to produce informative rollouts. For 1–40B small models, this argues for self-distillation loops or starting from a stronger teacher's traces.
Caveat: the rollout cost (N completions per step) is not single-sample; pairs naturally with a low test-time data regime but expensive offline label generation.

## Source
- arXiv: 2312.08935
- Raw markdown: `../../../raw/research/single-sample-llm-learning/17-C-2-math-shepherd.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/C-2-math-shepherd.pdf`

## Related
- [[lets-verify-step-by-step]]
- [[process-outcome-feedback]]
- [[training-verifiers-gsm8k]]
- [[_overview]]
