---
name: azr
description: Zhao et al. NeurIPS 2025 — Absolute Zero Reasoner trains a single LLM as both proposer and solver over three code-reasoning modes (deduction, abduction, induction) with zero human data; AZR-Coder-7B achieves +15pp OOD math gain from code-only training, providing the strongest existing evidence that concept-mode curriculum training yields domain-general reasoning.
type: research
---

# AZR: Absolute Zero Reasoner

Andrew Zhao, Yiran Wu, Yang Yue, Tong Wu, Quentin Xu, Matthieu Lin, Shenzhi Wang, Qingyun Wu, Zilong Zheng, Gao Huang. *Absolute Zero: Reinforced Self-play Reasoning with Zero Data.* NeurIPS 2025. arXiv:2505.03335, May 2025.

A single parameterised policy $\pi_\theta$ plays proposer and solver simultaneously, using a code executor as the sole verifiable reward source. No human-curated data at any stage. AZR-Coder-7B starts from a base model and trains entirely on self-proposed code tasks; it surpasses all prior 7B zero-style reasoners on combined coding+math benchmarks and improves OOD math by +15.2 points — compared to +0.65 points for expert-trained code-only RLVR models. The paper studied in [[understanding-self-play]].

## Method

**Three reasoning modes** are defined over the program/input/output triplet $(p, i, o)$ where $o = p(i)$:

- **Deduction** $(p, i) \to o$ — forward execution: given program and input, predict output. Captures step-by-step logical simulation.
- **Abduction** $(p, o) \to i^\pi$ — inverse reasoning: given program and output, infer a plausible input $i^\pi$ such that $p(i^\pi) = p(i^\star)$. Verification uses output equivalence (not exact input match) because $p$ need not be bijective.
- **Induction** $\{(i_j, o_j)\}_j \to p^\pi$ — program synthesis: given $N/2$ input-output pairs and a natural-language description $m$, synthesise program $p^\pi$ generalising to held-out pairs. The held-out split discourages if-else overfitting.

**Unified objective:**

$$J(\theta) := \max_\theta \; \mathbb{E}_{z \sim p(z)} \left[ \lambda \, r_e^\text{propose}(\tau, \pi_\theta) + \mathbb{E}_{y \sim \pi_\theta^\text{solve}(\cdot \mid x)} \left[ r_e^\text{solve}(y, y^\star) \right] \right]$$

where $\tau \sim \pi_\theta^\text{propose}(\cdot \mid z)$ and the seed $z$ is sampled from a buffer of past valid triplets. The proposer is explicitly prompted to generate tasks *different* from the $K = 6$ buffer references, promoting diversity.

**Proposer reward (Goldilocks-frontier):**

$$r^\text{propose} = \begin{cases} 0 & \text{if } \bar{r}^\text{solve} = 0 \\ 1 - \bar{r}^\text{solve} & \text{otherwise} \end{cases}$$

where $\bar{r}^\text{solve} = \frac{1}{G}\sum_{i=1}^{G} r^\text{solve}_{(i)}$ is the Monte Carlo average over $G = 8$ solver rollouts at non-zero temperature. Hard zero for unsolvable tasks (no gradient wasted on pathological proposals); linear decay from 1 rewards tasks where the solver sometimes fails — peak reward at $\bar{r}^\text{solve} \approx 0$, falling to zero at $\bar{r}^\text{solve} = 1$. This is the cleanest single-formula Goldilocks instantiation in the corpus — extend [[../synthesis/proposer-reward-shapes]] (row 7).

**Solver reward:** $r^\text{solve} = \mathbb{1}[y = y^\star]$ evaluated by Python value-equivalence.

**Composite reward:** correctly formatted propose/solve gets $r^\text{role}$; wrong but well-formatted gets $-0.5$; formatting errors get $-1$.

**Algorithm: Task-Relative REINFORCE++ (TRR++).** PPO clipped objective with six independent baselines — one per (task type $\in$ \{ind, ded, abd\}) $\times$ (role $\in$ \{propose, solve\}) cell:

$$A^\text{norm}_{\text{task,role}} = \frac{r - \mu_{\text{task,role}}}{\sigma_{\text{task,role}}}$$

This interpolates between per-question baselines (GRPO) and a global baseline (REINFORCE++), reducing variance in the multitask setup. **No KL loss; no KL reward penalty** (Table 3 hyperparameters: KL Loss = False, KL Reward = False).

**Initialisation.** Buffers seeded from a single zero-triplet (identity function `def f(x): return x`, input `"Hello World"`). 500 training steps, LR $= 10^{-6}$, AdamW, batch $64 \times 6$ (2 roles $\times$ 3 types). A800 cluster, 3–5 days.

## Claims

**1. +15pp OOD math from code-only training.**

| Benchmark | AZR-Coder-7B | Base | $\Delta$ |
|---|---|---|---|
| MATH500 | 72.6 | 54.0 | +22.6 |
| Minerva | 36.4 | 17.3 | +19.1 |
| OlympiadBench | 38.2 | 21.9 | +16.3 |
| AIME'24 | 20.0 | 6.7 | +13.3 |
| **MAvg** | **39.1** | 23.9 | **+15.2** |
| **AVG** | **50.4** | 40.2 | **+10.2** |

Expert code-only RLVR models (AceCoder, CodeR1) improve math by only +0.65 points on average; AZR-Coder-7B achieves +15.2.

**2. RLVR-solvable is a strict superset of expert-data models at 7B.**

AZR-Coder-7B surpasses all prior 7B zero-style reasoners by +1.8 absolute points in combined AVG, including models trained on 22k–484k expert-curated examples.

**3. All three task types are non-redundant (Table 2).**

Removing induction: combined AVG 43.8 (full 46.8). Removing all but deduction: 43.3. Training solver only (no proposer training): 45.4 vs. full 46.8. Induction removal hurts math generalisation most.

**4. Scaling is positive.** OOD total-average gains: 3B Coder +5.7, 7B Coder +10.2, 14B Coder +13.2. Larger models benefit more from the same zero-data curriculum.

**5. K-reference conditioning matters.** Removing the $K = 6$ buffer references: combined AVG 43.8 vs. 46.8, with the largest drop on math (−3 points).

## Why this is load-bearing for single-sample concept learning

**The three modes are a concept-mode taxonomy.** Deduction, abduction, and induction decompose concept engagement into forward evaluation, backward inference, and synthesis — three structurally distinct ways to query the same underlying concept. AZR demonstrates empirically that these are non-redundant: the ablation removing induction most severely hurts math generalisation. For the wiki's concept-learning frame, *how* a concept is queried (forward vs. inverse vs. synthesis) is a curriculum dimension in its own right. This is a candidate refinement for component D1 (Decompose) of [[../synthesis/recursive-concept-learning]].

**Proposer reward = cleanest Goldilocks formula in the corpus.** The piecewise formula is a direct operationalisation of Vygotsky's zone of proximal development. Tasks where the solver passes ~50% of rollouts yield maximum proposer reward; the hard zero at $\bar{r}^\text{solve} = 0$ kills unsolvable proposals before they waste compute. Add as row 7 of [[../synthesis/proposer-reward-shapes]].

**Structural information asymmetry.** The solver never sees the proposer's program in abduction (only sees $p$ and $o$); never sees the program at all in induction (only I/O pairs and description $m$). This is the same information-asymmetry pattern as [[spice]], instantiated in the code domain with a verifiable executor rather than a learned reward model.

**Direct test of [[invisible-leash]].** AZR's training is RL, but with a continuously evolving curriculum driven by proposer exploration rather than a fixed data distribution. Does it stay Stage-1-bounded or escape via training duration / entropy preservation? [[understanding-self-play]] shows the solver remains Invisible-Leash-bounded even under AZR training. AZR's +15pp math gain is therefore evidence that the *proposer* curriculum is activating latent base-model capacity at the edge of the leash — not that the leash has been broken. See [[two-stage-dynamic]] for the Stage-2 refinement.

**Cross-domain transfer with no domain-specific data** is the strongest existing evidence that concept-structure training (deduction/abduction/induction across code) yields domain-general reasoning. Code is Turing-complete, so the self-generated task space is open-ended; the massive OOD math gain is consistent with the wiki's thesis that concept-mode training, not domain-specific data, drives generalisation.

## Limitations

- **Code-executor dependence.** Verifiable reward requires a safe sandboxed executor. Extending to open-ended science, language reasoning, or embodied AI requires a different grounding environment; the paper acknowledges web / formal-math / world-simulator extensions as future directions.
- **OOD math transfer is empirical, not mechanistically explained.** The paper documents +15pp but provides no mechanistic account of why code self-play transfers to symbolic math.
- **No KL leash.** KL Loss = False, KL Reward = False throughout training. This keeps the model free to diverge from initialisation; departure from standard RLVR practice means cross-system comparisons must note the missing regulariser.
- **Safety concerns.** Llama-3.1-8B trained with AZR produced concerning chains of thought without adversarial prompting ("uh-oh moment") — autonomous self-improvement may require safety-aware wrappers.
- **Proposer/solver task interference.** Multi-task gradient interference across six (task, role) cells may limit gains; flagged as open research.
- **Only coding and math benchmarks.** Non-math, non-code domains not validated; breadth of domain-general transfer is unknown.

## Source

- `../../../raw/research/self-play-quality-extraction/.ingest/03-azr.md`
- `../../../raw/research/self-play-quality-extraction/05-03-azr.md`
- arXiv: https://arxiv.org/abs/2505.03335

## Related

- [[understanding-self-play]] — mechanistic analysis paper that studies AZR's training dynamics; shows proposer is critical and solver is Invisible-Leash-bounded
- [[invisible-leash]] — formal bound that AZR's empirical results test; solver gains are activating latent capacity, not escaping the leash
- [[two-stage-dynamic]] — Stage-1 vs. Stage-2 refinement; AZR's continuous curriculum is the Stage-1 boundary question
- [[r-zero]] — sister zero-data paper
- [[language-self-play]] — sister self-play method, NL domain
- [[spice]] — sister structural-asymmetry method (same information-asymmetry pattern, NL domain)
- [[sqlm]] — sister proposer/solver approach, no code executor
- [[../synthesis/proposer-reward-shapes]] — AZR proposer reward is row 7 (Goldilocks formula, code domain)
- [[../synthesis/recursive-concept-learning]] — three-mode taxonomy as candidate D1 (Decompose) refinement
- [[../synthesis/proposed-method]]
- [[_overview]]
