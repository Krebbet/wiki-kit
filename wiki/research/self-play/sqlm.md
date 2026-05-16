---
name: sqlm
description: Self-Questioning Language Models — single LLM acts as both proposer and solver; proposer rewarded by a Goldilocks gate (neither all-correct nor all-wrong across N samples) with no labeled data, producing emergent difficulty curricula from a topic string alone.
type: research
---

# SQLM: Self-Questioning Language Models

Lili Chen, Mihir Prabhudesai, Katerina Fragkiadaki, Hao Liu, Deepak Pathak. Carnegie Mellon University. arXiv:2508.03682 (2025, preprint). A single pre-trained LLM acts as both proposer and solver: given only a topic string, the proposer generates questions and the solver attempts answers, both trained via GRPO with no external data or reference answers. Difficulty is regulated endogenously — the proposer earns reward only when its question is neither universally solved nor universally failed by $N = 4$ solver samples (the Goldilocks gate). Starting from Qwen2.5-3B-Instruct with no curated data, SQLM yields +15.7 pp on three-digit multiplication and +16 pp on linear-equation algebra; Qwen2.5-Coder-3B-Instruct gains +7.1 pp on Codeforces.

## Method

Two policies share the same underlying model weights:

- **Proposer** $\pi_{P_t}(x)$: conditioned on topic $t$, generates question $x$.
- **Solver** $\pi_S(y_\text{pred} \mid x)$: generates answer $y_\text{pred}$ given $x$.

Both are trained via RL:

$$\text{Solver:} \quad \mathbb{E}_{x \sim \pi_{P_t},\, y_\text{pred} \sim \pi_S(\cdot|x)}\bigl[R_S(x, y_\text{pred})\bigr]$$

$$\text{Proposer:} \quad \mathbb{E}_{x \sim \pi_{P_t},\, y_\text{pred} \sim \pi_S(\cdot|x)}\bigl[R_P(x, y_\text{pred})\bigr]$$

### Case 1 — small generator-verifier gap (arithmetic, algebra)

Sample $N = 4$ solver outputs $y_1, \ldots, y_N$; let $y_\text{maj}$ be the majority answer.

$$R_S(x, y_i) = \begin{cases} 1 & \text{if } y_i = y_\text{maj} \\ 0 & \text{otherwise} \end{cases}$$

$$R_P(x) = \begin{cases} 1 & \text{if } 0 < |\{y_i : y_i = y_\text{maj}\}| < N \\ 0 & \text{otherwise} \end{cases}$$

$R_P = 1$ iff solver outputs are neither all-same (too easy) nor all-different (too hard). No ground-truth labels; correctness is proxied by internal majority-vote consensus.

### Case 2 — large generator-verifier gap (coding)

The proposer outputs a problem $x$ together with five unit tests. Let $\text{Pass}(y_\text{pred}, \text{Tests}(x)) \in [0,1]$ be the fraction passed.

$$R_S(x, y_\text{pred}) = \text{Pass}(y_\text{pred}, \text{Tests}(x))$$

$$R_P(x, y_\text{pred}) = \begin{cases} 1 & \text{if } 0 < \text{Pass}(y_\text{pred}, \text{Tests}(x)) < 1 \\ 0 & \text{otherwise} \end{cases}$$

### Training algorithm

1. Sample question $x \sim \pi_{P_t}$.
2. Sample $N = 4$ solver outputs; compute $R_S$ and $R_P$.
3. Update solver every step; update proposer every $K = 5$ steps (best across tasks; $K = \infty$ still improves over baseline but less so).
4. Repeat — proposer distribution drifts toward harder but still-solvable problems as solver improves.

RL algorithm: GRPO via verl. KL coefficient 0.001, clip ratio 0.2, learning rate $1\times10^{-6}$, $N = 4$ samples per example.

**Emergent curriculum:** Arithmetic proposer progresses from simple sums at step 0 ($563 + 247 - 189$) to mixed-operator expressions with exponents at step 20 ($384 \div (52 \times 2) + 7^3 - 111$). Online one-at-a-time generation produces substantially more diverse training problems than pre-generating a static dataset of 6,400 questions (confirmed by PCA of embeddings).

## Claims

| Model | Task | Baseline | SQLM | $\Delta$ |
|---|---|---|---|---|
| Qwen2.5-3B-Instruct | 3-digit multiplication | 0.791 | 0.948 | +15.7 pp |
| Qwen2.5-3B-Instruct | Linear equations | 0.440 | 0.600 | +16.0 pp |
| Qwen2.5-Coder-3B-Instruct | Codeforces | 0.320 | 0.391 | +7.1 pp |
| Llama-3.2-3B-Instruct | Codeforces | — | — | +3.2 pp |
| Llama-3.1-8B-Instruct | Codeforces | — | — | +15.1 pp |

- Format-reward ablation (reward for correct output format only) reaches 0.826 / 0.553 on multiplication/algebra — substantially below full SQLM, confirming genuine reasoning gains not formatting.
- Proposer update frequency $K = 5$ works best; frozen proposer ($K = \infty$) still improves over baseline.
- Online generation beats pre-generated static dataset for diversity; diversity collapse is the failure mode of static pre-generation.

## Why this is load-bearing for single-sample concept learning

SQLM is the closest existing paper to the "play with the concept" framing that motivates this wiki. The single human-provided input to the entire system is a topic string — exactly the role a concept plays in the target method. The proposer's job is to generate exercises *in* or *about* that concept; the solver's job is to attempt them. No examples, no labeled data, no reference answers: the concept name alone seeds the curriculum.

This is the **direct user-question match for "play with a concept."** The Goldilocks reward $R_P$ enforces a difficulty corridor purely from internal model state — the proposer is forced to track the solver's evolving capability without any external signal. This makes SQLM the closest LLM analogue to Sukhbaatar's Asymmetric Self-Play and to SOAR's bilevel structure, but with an instantaneous difficulty signal (current pass rate) rather than an improvement-rate signal (delta in solver performance over time).

Compared with [[../teacher-student-rl/soar-edge-of-learnability]]:

| Dimension | SQLM | SOAR |
|---|---|---|
| Difficulty signal | Binary Goldilocks on $N$ majority votes | Bilevel: outer reward = solver improvement rate |
| Grader | Internal consensus / unit tests | External task verifier |
| Shared weights | Yes | Separate teacher and student |
| Concept input | Single topic string | Task distribution or curriculum |
| Collapse guard | Hard gate: $R_P = 0$ when all agree or none agree | Implicit via improvement signal |
| Data required | None | Minimal (seed task distribution) |

SQLM's bilevel structure is shallower than SOAR's: the proposer reward is an immediate function of the current solver generation, not of how much the solver *improves* over time. For a single-sample concept-learning setting, SQLM's approach is easier to instantiate — it needs only one topic string — but it may be slower to escape local Goldilocks zones than SOAR's improvement-rate signal.

The shared-weights design is load-bearing for small-LLM deployment: a single 3B model acts as its own teacher and student, matching the project's constraint of training the deployment model directly rather than relying on a separate, larger teacher.

## Limitations

- Topic must be manually specified; no method for discovering or generating topics. Concept coverage depends on prompt engineering.
- Majority-vote verifier is brittle when systematic errors dominate: if the model consistently converges on the same wrong answer, that wrong answer becomes $y_\text{maj}$ and the solver is reinforced for being wrong. The paper acknowledges no correction mechanism without external guidance.
- Despite no labeled data, prompts required manual iteration per task — especially for coding (unit test format). Flagged as the central limitation.
- Evaluated only on structured, verifiable domains (arithmetic, linear equations, Codeforces). Extension to open-ended concept learning is undemonstrated.
- No mechanism to ensure the proposer explores the full concept space rather than a narrow sub-type in the difficulty corridor.
- No safeguard on question quality, safety, or relevance (flagged as future work).
- Experiments use 3B-parameter models only; behaviour at sub-1B scale unknown.
- No explicit pseudocode in the paper; loop structure must be inferred from prose and hyperparameter table.

## Source

- `../../../raw/research/self-play-concept-learning/06-07-sqlm.md`
- arXiv: https://arxiv.org/abs/2508.03682

## Related

- [[../teacher-student-rl/soar-edge-of-learnability]] — most direct analogue: bilevel improvement-rate reward vs. SQLM's instantaneous Goldilocks gate
- [[../teacher-student-rl/sakana-rlt]] — teacher-generated (Q,A) packets; SQLM replaces the teacher model with a self-play proposer and removes the need for reference answers entirely
- [[../self-improvement/multi-turn-policy-verifier]] — PAG role separation; SQLM collapses proposer and solver into one model, closer to the single-small-LLM constraint
- [[asymmetric-self-play]] — Sukhbaatar's precursor: proposer-solver asymmetry without LLM
- [[understanding-self-play]] — proposer-is-everything analysis
- [[_overview]] — self-play theme overview
