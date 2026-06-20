# Hierarchical Reasoning Model (HRM)

The Hierarchical Reasoning Model (HRM; Wang et al., 2025) is a recurrent neural architecture that achieves deep sequential reasoning in a single forward pass by coupling two interdependent modules that operate at different timescales — a high-level module for slow, abstract planning and a low-level module for rapid, detailed computation — without any pre-training, chain-of-thought data, or explicit supervision of intermediate steps. With only 27 million parameters trained on 1000 examples, HRM reaches near-perfect accuracy on complex Sudoku puzzles and optimal maze path-finding, and outperforms much larger language models on the Abstraction and Reasoning Corpus (ARC).

## Architecture

HRM is a recurrent architecture, not a transformer. Its two modules run sequentially within each recurrence step:

- **High-level module** — operates on an abstract, compressed representation of the problem state. It updates slowly relative to the low-level module, acting as a planner that sets subgoals or maintains a coarse strategy across recurrence steps.
- **Low-level module** — receives guidance from the high-level state and performs rapid, fine-grained computation: symbol manipulation, constraint propagation, local path search. It updates more frequently and feeds refined state back up to the high-level module.

The two modules are interdependent: the high-level module conditions on low-level outputs (global context from detail) and the low-level module is guided by high-level state (local work constrained by plan). This creates a two-timescale feedback loop within each forward pass.

**Single forward pass:** Unlike CoT-based LLMs, HRM does not produce intermediate reasoning tokens. All reasoning depth is achieved through recurrence — the same architecture iterates its state until convergence, which the authors argue is more computationally efficient and avoids the brittleness of token-level task decomposition.

**Scale:** 27 million parameters total. No pre-training corpus. No chain-of-thought annotations.

## Sample efficiency results

| Task | Training samples | Result |
|---|---|---|
| Complex Sudoku | 1,000 | Near-perfect accuracy |
| Optimal maze path-finding (large mazes) | 1,000 | Near-perfect accuracy |
| ARC (Abstraction and Reasoning Corpus) | — | Outperforms much larger models with significantly longer context windows |

The 1000-sample figure is particularly striking because Sudoku and maze path-finding are combinatorially hard tasks where naively-trained models fail even with millions of examples. HRM generalizes from a small training set because its architecture encodes the right computational primitives (hierarchical decomposition + iteration) rather than relying on statistical pattern matching over large corpora.

This is a direct instance of the wiki's core question: **architectural inductive bias as a substitute for data volume.**

## Relation to concept-granularity architecture hypothesis

The concept-granularity hypothesis (see [[../synthesis/concept-granularity-architecture]]) holds that representations at variable abstraction levels — rather than flat token sequences — are a key enabler of sample-efficient concept learning. HRM is a concrete architectural instantiation of this idea:

- The **high-level module** corresponds to the "slow concept" layer: it maintains abstract, goal-oriented structure that is stable across many low-level steps.
- The **low-level module** corresponds to the "fast feature" layer: it performs symbol-level operations that are subordinate to and guided by the abstract plan.
- The **two-timescale coupling** is structurally analogous to the variable-granularity hypothesis — different parts of the network process information at different levels of abstraction simultaneously, not sequentially in the token stream.

HRM therefore provides empirical evidence that the hierarchy does not need to be explicit in the output (as in CoT) but can be implicit in the computation graph. The architecture does the decomposition; the model does not need to be taught to decompose via annotated intermediate steps.

The connection to [[../synthesis/recursive-concept-learning]] is also direct: HRM's high-level module recursively sets context for the low-level module across recurrence steps, mirroring the hierarchical decomposition structure described there as a prerequisite for sample-efficient generalization.

## Relation to other wiki entries

- **Continuous Latent Contexts (arXiv:2605.09867)** — both approaches move reasoning off the token sequence into a latent computational substrate. Continuous Latent Contexts do this by suppressing token outputs during reasoning steps; HRM does it by recurrence within a single forward pass. The mechanisms differ but the motivation is shared.
- **Latent-GRPO** — trains latent reasoning via RL rather than supervised intermediate steps. HRM also avoids supervised intermediates but uses architectural recurrence rather than RL-shaped latent trajectories.

HRM is the most architecturally principled of the three: it does not require a separate "latent vs. output" switching mechanism, because reasoning is never in the token stream to begin with.

## Conflict flags

- **CoT-based approaches:** HRM explicitly frames CoT as brittle and data-hungry. The wiki contains entries on process reward models and CoT-adjacent methods (e.g., curriculum-and-decomposition). HRM's results are a challenge to those approaches — not a refutation, but evidence that the token-sequence-as-reasoning-trace assumption may be unnecessary for structured tasks. Worth revisiting those entries to note the tension.
- **Scale assumptions:** Most wiki entries on RL-based fine-tuning (RLVR, Latent-GRPO) assume a pre-trained backbone. HRM trains from scratch at 27M params. This is either a very different regime (small structured tasks vs. open-domain language) or evidence that the backbone assumption is also unnecessary. The scope of generalization is an open question.

## Source

- arXiv: [2506.21734](https://arxiv.org/abs/2506.21734)
- Authors: Guan Wang, Jin Li, Yuhao Sun, Xing Chen, Changling Liu, Yue Wu, Meng Lu, Sen Song, Yasin Abbasi Yadkori
- Submitted: 2025-06-26; v3: 2025-08-04

## Related

- [[../weekly-briefs/2026-06-19]] — brought in by the 2026-06-19 weekly sweep
- [[../synthesis/concept-granularity-architecture]] — two-module arch as variable-granularity evidence
- [[../synthesis/recursive-concept-learning]] — hierarchical decomposition instantiation
- [[../decoding-time-steering/continuous-latent-contexts]] — complementary latent-reasoning approach
