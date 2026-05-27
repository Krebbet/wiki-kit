# Adaptive Computation Time for Recurrent Neural Networks (Graves, arXiv 2016)

Graves introduces ACT, a deterministic and differentiable algorithm that allows an RNN to execute a variable number of internal state transitions per input step before emitting an output. A sigmoidal halting unit accumulates probability mass across intermediate steps; once the cumulative mass reaches $1 - \epsilon$, computation stops and the final step absorbs the remaining probability as a remainder. The network's output and state are mean-field weighted sums over all intermediate steps, making the mechanism fully differentiable without stochastic sampling. A ponder cost penalizes unnecessary computation, trading off accuracy against speed via a scalar hyperparameter $\tau$. The mechanism is architecture-agnostic (demonstrated on vanilla RNN, LSTM, and suggested for NTM) and requires only adding one halting unit and one scalar loss term.

## Method core

**Intermediate steps.** At input step $t$, the network executes $N(t)$ sub-steps. Each sub-step $n$ computes:

$$s_t^n = S(s_t^{n-1},\, x_t^n), \qquad y_t^n = W_y s_t^n + b_y$$

where $x_t^n = x_t + \delta_{n,1}$ (a binary flag distinguishes the first sub-step from repeated ones).

**Halting unit.** An extra sigmoid output:

$$h_t^n = \sigma(W_h s_t^n + b_h)$$

**Halting count and remainder.** Define:

$$N(t) = \min\!\left\{n' : \sum_{n=1}^{n'} h_t^n \geq 1 - \epsilon\right\}$$

$$R(t) = 1 - \sum_{n=1}^{N(t)-1} h_t^n$$

**Halting probabilities.** The final probability distribution over steps is:

$$p_t^n = \begin{cases} R(t) & \text{if } n = N(t) \\ h_t^n & \text{otherwise} \end{cases}$$

This guarantees $\sum_{n=1}^{N(t)} p_t^n = 1$.

**Mean-field accumulation.** Output and state at step $t$:

$$s_t = \sum_{n=1}^{N(t)} p_t^n\, s_t^n, \qquad y_t = \sum_{n=1}^{N(t)} p_t^n\, y_t^n$$

**Ponder cost.** Per-step ponder cost:

$$\rho_t = N(t) + R(t)$$

Total sequence ponder cost (upper bound on actual step count):

$$P(\mathbf{x}) = \sum_{t=1}^{T} \rho_t$$

**Training loss.** Task loss augmented with ponder penalty weighted by $\tau$:

$$\hat{L}(\mathbf{x}, \mathbf{y}) = L(\mathbf{x}, \mathbf{y}) + \tau\, P(\mathbf{x})$$

**Gradient through the halting unit.** The ponder cost is discontinuous at boundaries where $N(t)$ changes; the paper treats $N(t)$ as constant and ignores those points. The resulting gradient is:

$$\frac{\partial \hat{L}}{\partial h_t^n} = \begin{cases} 0 & \text{if } n = N(t) \\ \frac{\partial L}{\partial y_t}(y_t^n - y_t^{N(t)}) + \frac{\partial L}{\partial s_t}(s_t^n - s_t^{N(t)}) - \tau & \text{otherwise} \end{cases}$$

The gradient at the final step is exactly zero, so the halting unit receives no direct loss signal at the boundary — all signal comes from comparing earlier states/outputs to the final ones minus the ponder penalty.

**Maximum ponder cap.** A hard cap $M$ on $N(t)$ prevents runaway pondering early in training (set to 100 for most experiments, 20 for addition).

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (block isolation / swappability) | Low | ACT reuses the same shared weight block repeatedly per step; blocks are not isolated or independently swappable. Weight sharing across sub-steps is explicit design, not a limitation. |
| **G2** (dynamic parameter allocation) | Medium | ACT dynamically varies the number of compute steps, which is a form of adaptive compute allocation. It does not allocate distinct parameter sets per step — the same block is reused. |
| **G3** (token-conditional routing with learned halting) | High | ACT is the direct progenitor of learned halting for token-conditional computation depth. The halting mechanism (remainder trick + mean-field accumulation) is the specific approach that Exp 1 must either adopt or replace with PonderNet. |

## Credibility

arXiv preprint (1603.08983), submitted March 2016, revised to v6 February 2017. Published by Alex Graves at Google DeepMind. No official code repository accompanies the paper. The paper became highly influential as a foundational reference for Universal Transformers and PonderNet. Ablations cover 20 random seeds per $\tau$ value across a logarithmic grid search. Results are on synthetic tasks and a single real-world dataset (Wikipedia character prediction); no held-out test set for synthetic tasks (data generated online). Independent replication exists informally in Universal Transformers (Dehghani et al., 2018) and PonderNet (Banino et al., 2021), both of which cite ACT as the baseline they extend or replace.

## Empirical claims

- **Parity (64-bit binary vectors, simple RNN, 128 hidden units):** Without ACT: ~40% error (vs. 50% random baseline). With ACT ($\tau \leq 0.03$): <5% mean error. Ponder time grows approximately linearly with number of active bits.
- **Logic (recursive binary gates, LSTM 128 cells):** Without ACT: ~20% sequence error. With ACT ($\tau \leq 0.01$): ~0% error. Networks converge ~10K iterations.
- **Addition (multi-digit, LSTM 512 cells):** All $\tau$ values in the grid search achieve 0% error. Ponder scales approximately linearly with digit count; slope ~1 for highest-$\tau$ networks.
- **Sort (2–15 Gaussian numbers, LSTM 512 cells):** Without ACT: ~12% error. Best ACT: ~6% error, at ~9× the computational cost.
- **Wikipedia character prediction (LSTM 1500 cells, 256-class softmax):** Minimal accuracy improvement over fixed-depth LSTM. ACT learns to allocate extra computation at word boundaries, spaces, punctuation — not at unpredictable sequences (e.g., XML IDs).

## Known failure modes

**Gradient discontinuity at halting boundary.** The ponder cost $\rho_t$ is discontinuous at boundaries where $N(t)$ changes (i.e., when cumulative probability crosses $1 - \epsilon$). The paper explicitly acknowledges this and treats $N(t)$ as constant throughout, ignoring the discontinuity. The gradient is therefore a biased estimator of the true gradient. This is the primary source of training instability and was erroneously claimed to be smooth in earlier versions (corrected in v3+).

**Zero gradient at the final halting step.** The halting unit at step $n = N(t)$ receives $\partial \hat{L} / \partial h_t^{N(t)} = 0$, meaning the unit that actually triggers halting gets no direct gradient signal from the ponder cost. All pressure to halt comes indirectly through earlier steps' comparison to the final state.

**Sensitivity to $\tau$.** Behavior is highly sensitive to the time penalty $\tau$. Too high: network halts after one step (degenerates to fixed-depth). Too low: excessive pondering. No principled selection procedure exists; grid search over ~20 values is the approach used. The paper identifies this as a key weakness.

**Potential for gaming the halting distribution.** A footnote documents that training to minimize expected (rather than total) ponder time leads to a learned exploit: the network sets $h_t^1$ just below threshold, keeps $h_t^n = 0$ for intermediate steps, then sets a large $h_t^{N(t)}$, ensuring that $p_t^{N(t)} \ll p_t^1$ in the mean-field update but compensating with large state magnitudes at the final step. The remainder trick (used in the actual paper) avoids this specific exploit.

**Linearity assumption.** Mean-field accumulation $y_t = \sum p_t^n y_t^n$ assumes approximate linearity of the state/output space under interpolation. This assumption is not enforced and may fail for highly nonlinear representations.

**Reuse of identical weights.** All sub-steps share the same $S$, $W_y$, $W_h$. This prevents sub-steps from specializing and may limit the representational capacity of individual iterations compared to depth-varying architectures.

**Implication for Exp 1 (frozen-weight loop router).** PonderNet (Banino et al., 2021) was developed explicitly to address ACT's gradient instability by replacing the remainder trick with a geometric halting prior and a KL-regularized objective. For Experiment 1 — training a router on a frozen-weight Huginn-style loop LLM — ACT's biased gradients at the halting boundary pose a direct training risk. The proposal identifies this as the key reason to prefer PonderNet over ACT.

## Open questions

- No principled method for selecting $\tau$; the paper acknowledges this as future work.
- Experiments are on RNNs with shared weights; generalization to transformer blocks with non-shared weights (e.g., distinct per-layer parameters) is not addressed.
- Only synthetic tasks and one real-world dataset (Wikipedia); no results on modern NLP benchmarks.
- The interaction between ACT halting and attention mechanisms (flagged as promising by Graves) was not explored in the paper itself; this became the Universal Transformers contribution.
- No code release; implementations must reconstruct from the equations, which have a history of subtle errors around the remainder trick.
- Whether the linearity assumption degrades performance in practice for deep or highly nonlinear models is untested.

## Source

- `raw/research/loop-computation/02-act-graves-abs.md`
- `raw/research/loop-computation/10-act-graves-pdf.md`

## Related

- [[universal-transformers]] — applies ACT halting to transformer layers with shared weights; direct extension
- [[pondernet]] — replaces ACT's remainder trick with geometric prior + KL loss, fixing the gradient discontinuity; recommended over ACT for Exp 1
- [[huginn]] — the frozen-weight loop LLM that Exp 1 targets; ACT halting is the mechanism being evaluated or replaced
- [[mod]] — mixture-of-depths routing; token-conditional depth via budget forcing rather than learned halting
- [[calm]] — contextual adaptive layer skipping; shares the token-conditional compute theme in a transformer setting
