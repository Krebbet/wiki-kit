# PonderNet: Learning to Ponder (Banino, Balaguer, Blundell; DeepMind 2021)

PonderNet is an adaptive computation algorithm that learns, end-to-end, how many recurrent steps to apply before halting. It reformulates halting as a probabilistic model: the step function emits a per-step scalar $\lambda_n \in (0,1)$ representing the conditional probability of halting at step $n$ given no prior halt. Unrolling produces a geometric-family distribution over halt steps; the training loss couples a step-weighted reconstruction term with a KL regularizer that matches this distribution to a geometric prior parameterized by $\lambda_p$. This replaces ACT's brittle ponder-cost heuristic with a principled, fully differentiable objective that yields unbiased gradients and is substantially more robust to hyperparameter choice.

## Method core

**Architecture.** A step function $s$ maps $(x, h_n) \to (\hat{y}_n, h_{n+1}, \lambda_n)$, where $\lambda_n \in (0,1)$ is the *conditional* halt probability at step $n$ given the chain has not yet halted. This is structurally identical to ACT's step function; the difference lies entirely in how $\lambda_n$ is interpreted and used.

**Halt distribution.** Define a Markov halting process with $P(\Lambda_n = 1 \mid \Lambda_{n-1} = 0) = \lambda_n$. The unconditional probability of halting at step $n$ is:

$$p_n = \lambda_n \prod_{j=1}^{n-1}(1 - \lambda_j)$$

This is a generalized geometric distribution. For $N \to \infty$ the $p_n$ sum to 1; in practice the network is unrolled until the cumulative probability $\sum_{j=1}^n p_j > 1 - \varepsilon$ (default $\varepsilon = 0.05$), and remaining mass is assigned to step $N$.

**Training objective.**

$$\mathcal{L} = \underbrace{\sum_{n=1}^{N} p_n \, \ell(y, \hat{y}_n)}_{\mathcal{L}_{\text{Rec}}} + \beta \, \underbrace{\mathrm{KL}\!\left(p_n \,\|\, p_G(\lambda_p)\right)}_{\mathcal{L}_{\text{Reg}}}$$

where $p_G(\lambda_p)$ is a geometric prior with parameter $\lambda_p$ (expected halt step $= 1/\lambda_p$, truncated at $N$). The reconstruction loss is the *expectation* of $\ell$ across halting steps — not a loss on the expected output. $\beta$ scales the KL regularizer; typical value $\beta = 0.01$.

**KL regularizer vs ACT's ponder cost.** ACT uses a heuristic ponder cost $\tau(N + R)$ (number of steps plus a remainder fraction), where $\tau$ is a scalar penalty with no distributional interpretation and gradients can only flow through the last step. PonderNet's $\mathcal{L}_{\text{Reg}}$ is a proper KL divergence: (a) it is in the same information-theoretic units as cross-entropy losses; (b) it promotes exploration by penalizing zero-probability steps, not just excess steps; (c) it does not use a remainder trick — the expected step count $\sum_n n p_n$ is differentiable exactly.

**Inference.** At evaluation the network steps sequentially; at each step it samples $\Lambda_n \sim \text{Bernoulli}(\lambda_n)$ and halts when $\Lambda_n = 1$, returning $\hat{y}_n$. If the step limit $N$ is reached the last output is used. This is stochastic; training and evaluation are asymmetric (training marginalizes the loss over steps, evaluation samples a single halt).

## Comparison to ACT

| Aspect | ACT (Graves, 2016) | PonderNet |
|---|---|---|
| $\lambda_n$ semantics | Direct halt probability $p_n$ (absolute, not conditional) | Conditional halt probability $P(\text{halt at } n \mid \text{no prior halt})$ |
| Halt distribution derivation | Implicit via accumulation; remainder trick to normalize | Explicit generalized geometric; exact summation |
| Output at test time | Weighted average $\hat{y} = \sum_n \hat{y}_n \lambda_n$ | Single prediction at sampled halt step |
| Training loss | Accuracy + $\tau(N + R)$ heuristic ponder cost | Weighted reconstruction + $\beta \cdot \text{KL}(p_n \| p_G(\lambda_p))$ |
| Gradient through halting | Biased — only flows through last step (remainder) | Unbiased — full gradient through $p_n$ |
| Hyperparameter interpretability | $\tau$: raw penalty magnitude, no natural scale | $\lambda_p$: inverse of expected steps, $1/\lambda_p$ = prior mean steps |
| Training stability | High sensitivity to $\tau$; most values fail to solve parity | Robust across broad $\lambda_p$ range; fails only at $\lambda_p \approx 0.9$ |
| Chaining multiple modules | Linear cost (can chain ACT blocks) | Exponential cost (loss conditions on each module's halt step) |

**For Exp 1 (frozen Huginn + trained router):** PonderNet is preferred over ACT. The router must learn a halt distribution over block depth, and the KL-vs-geometric-prior objective gives a principled, interpretable regularizer with stable gradients. ACT's remainder trick would produce biased gradient estimates through the halting head, and its $\tau$ sensitivity makes sweep-free training harder.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (block isolation / swappability) | Low | PonderNet is a halting mechanism, not a block-isolation technique. Blocks remain tightly coupled through the shared hidden state. |
| **G2** (dynamic parameter allocation) | Medium | Learns to vary depth (number of block applications) per input, which is a form of dynamic compute allocation. Does not route to different parameter pools. |
| **G3** (token-conditional routing through block pool with learned halting) | High | Directly applicable as the halting head for Exp 1. The geometric prior provides a tunable budget prior; KL loss is well-behaved for end-to-end training over a frozen block pool. |

## Credibility

- Venue: NeurIPS 2021 (workshop paper track; published in JMLR Workshop and Conference Proceedings). DeepMind, London.
- Code: referenced via Universal Transformer codebase (https://bit.ly/3frofUI); no standalone PonderNet repo cited in the paper, but third-party reimplementations exist.
- Ablations: $\lambda_p$ sensitivity study over 10 seeds × 10 values; ACT $\tau$ sensitivity study over 10 seeds × 20 values. Both on the parity task.
- Replication: parity and bAbI results are reproducible; PAI requires the MEMO dataset from DeepMind Research repo.

## Empirical claims

- **Parity (interpolation):** PonderNet outperforms ACT in accuracy and uses fewer total forward passes during training.
- **Parity (extrapolation):** PonderNet achieves near-perfect accuracy on held-out input lengths (49–96 elements, trained on 1–48); ACT stays at chance.
- **bAbI (20 tasks):** Transformer+PonderNet: 0.15 ± 0.9 avg error, 20/20 tasks solved. Universal Transformer+ACT: 0.29 ± 1.4, 20/20 tasks solved. PonderNet uses 1,658 total steps vs. UT's 10,161 steps to solve all 20 tasks.
- **PAI (inference trial A→C):** PonderNet 97.86% (±3.78), MEMO 98.26% (±0.67), Universal Transformer 85.60%. PonderNet matches task-specific MEMO architecture.
- **Hyperparameter robustness:** PonderNet solves parity for all tested $\lambda_p \in (0, 0.9)$; fails only at $\lambda_p = 0.9$ (prior forces ~1 step). ACT solves parity for only a narrow $\tau$ band; most seeds fail.

## Open questions / failure modes

- **Stochastic inference:** evaluation outputs are sampled, not deterministic. For a router replicating a fixed Huginn path, this adds variance per forward pass unless inference is de-randomized (e.g., by always halting at $\arg\max p_n$ or using the expected output).
- **Chaining cost:** composing multiple PonderNet modules grows the loss exponentially in the number of modules. Exp 1 routes through a single halting head, so this is not immediately blocking, but multi-stage routing would require a different formulation.
- **Geometric prior mismatch:** the geometric prior assumes a memoryless process (constant per-step halt probability). Real depth requirements may be multi-modal (e.g., easy inputs need 1 step, hard inputs need 5+). The learned $\lambda_n$ can deviate from geometric, but the KL pressure pulls it back toward the prior shape.
- **No block identity in the halt signal:** PonderNet's halt head sees only the hidden state, not which block was applied. In a heterogeneous block pool, the halt policy cannot directly condition on block identity, which may limit routing specificity.
- **Training/eval asymmetry:** loss uses full marginal over steps; inference uses a single halt sample. Under distribution shift this can cause mismatched step counts.

## Source

- `raw/research/loop-computation/03-pondernet-abs.md`
- `raw/research/loop-computation/11-pondernet-pdf.md`

## Related

- [[act]]
- [[universal-transformers]]
- [[huginn]]
- [[adaponderlm]]
