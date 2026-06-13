# RREDCoT: Segment-Level Reward Redistribution for Reasoning Models

RREDCoT (arXiv:2606.06475) addresses GRPO's sparse-reward / high-variance credit-assignment problem by redistributing the terminal reward across CoT segments using RUDDER-style return-decomposition — with no auxiliary reward model. CoT generation is cast as an MDP; optimal per-step credit is the Q-value difference between consecutive segments, estimated via an importance-sampling forward pass over a fixed reference-solution bank. On Qwen3-4B (Numina-CoT, 25k-token generation) this yields AIME24 90.8% vs. 85.0% GRPO vs. 69.2% base — the largest per-step gain over GRPO reported among PRM-adjacent methods as of mid-2026, without any process-label annotation.

## Method

CoT generation is modelled as an MDP: each segment $s_t$ is a state, actions $a_t$ extend the trace, and the only external signal is the terminal reward $\zeta(y)$.

**Optimal redistribution.** Adapting RUDDER (Arjona-Medina et al., 2019), the per-step redistributed reward equals the Q-value difference between consecutive segments:

$$r_t^{\text{red}} = q^w(s_t, a_t) - q^w(s_{t-1}, a_{t-1})$$

This is return-equivalent: $\sum_t r_t^{\text{red}} = \zeta(y)$, so the theoretical fixed point of policy optimization is preserved.

**Value estimation without rollouts.** Rather than MC sampling (which costs $\sim$5 rollouts per segment), $\hat{v}_w(s_t)$ is computed via a single forward pass over a fixed bank of $N$ reference (question, solution, answer) triples:

$$\hat{v}_w(s_t) = \frac{1}{N}\sum_{(u,y)} p(y \mid u, x, w)\, p(u \mid x, w)\, \zeta(y)$$

where $y$ and $u$ are drawn from the reference bank. Importance-sampling weights re-use activations already computed during training, keeping overhead at $\sim$1.5–2$\times$ GRPO.

**Segmentation.** A hybrid strategy splits on newlines then entropy-merges until a target segment count is reached, concentrating mass at high-entropy "exit points" where value estimates are most reliable.

**Gradient.** Per-token GRPO gradients are re-weighted by normalized redistribution coefficients $\sigma(t, q, o, \pi_{\text{rf}})$:

$$\nabla_\theta J_A(\theta) = \mathbb{E}_{(q,o)\sim\mathcal{D}}\!\left[\sum_t \sigma(t,q,o,\pi_{\text{rf}}) \cdot \mathrm{GC}_A(q,o,\pi_{\text{rf}}) \cdot \nabla_\theta \log \pi_\theta(o_t \mid q, o_{<t})\right]$$

## Results

Qwen3-4B trained on Numina-CoT (25k-token generation context):

| Benchmark | Base | GRPO | RREDCoT |
|-----------|------|------|---------|
| AIME24    | 69.2% | 85.0% | **90.8%** |
| AIME26    | 26.7% | 44.2% | **47.5%** |
| Minerva   | 90.6% | 91.5% | **93.5%** |
| MATH500   | 78.1% | 80.4% | **82.3%** |

On a smaller 1.5B model (open-rs, 1024-token context): MATH-500 85.8% vs. 84.8% baseline; AMC23 80.0% vs. 72.5%.

RREDCoT's value estimates correlate with MC sampling better than gradient attribution or Leave-One-Out baselines, particularly in later trajectory stages where credit-assignment error is highest.

## Comparison to PRM-based methods

| Axis | Standard PRM | GRPO-VPS | IOP-GSPO | RREDCoT |
|------|-------------|----------|----------|---------|
| Dense signal source | Human/model process labels | Verifier belief probing | Internalized outcome supervision | Return-decomposition over reference bank |
| Extra model required | Yes (PRM) | Yes (verifier) | No (architecture change) | No |
| Process labels required | Yes | No | No | No |
| Return-equivalent | N/A | No | No | Yes |

RREDCoT and PRM-augmented GRPO are not directly compared in the paper. The methods are plausibly complementary (redistribution could stack with a PRM signal), but no composition experiments exist. RREDCoT's key advantage is that it requires nothing beyond the rollouts GRPO already produces plus a static reference bank — making it a near-zero-overhead upgrade relative to a full PRM pipeline.

## Limitations

1. **Reference bank dependency.** Requires ground-truth (question, solution, answer) triples. Inapplicable to domains without existing solutions.
2. **Importance-sampling bias.** Value estimates are biased when the true high-quality solution distribution is broader than the reference bank; bias grows with problem diversity.
3. **Subgoal-free problems.** Tasks lacking meaningful intermediate subgoal structure may not benefit from step-level redistribution.
4. **Compute overhead.** $\sim$1.5–2$\times$ GRPO wall-clock time for the reference-bank forward pass.
5. **Segmentation heuristic.** Redistribution quality is sensitive to segmentation quality; entropy-based merging is not theoretically grounded.

## Source

- `raw/research/weekly-2026-06-12/05-rredcot.md` — captured PDF (arXiv:2606.06475)

## Related

- [[process-reward-models/_overview]] — parent theme
- [[process-reward-models/grpo-vps]] — parallel: GRPO-VPS uses verifier belief probing for per-step reward; RREDCoT uses return-decomposition
- [[process-reward-models/iop-gspo]] — parallel: IOP internalises outcome supervision into process supervision
- [[rl-optimizers/deepseekmath-grpo]] — base: GRPO is the backbone
- [[weekly-briefs/2026-06-12]] — brought in by the 2026-06-12 weekly sweep
