---
name: gspo
description: Sequence-level importance ratio and clipping; stabilises MoE RL; powers Qwen3.
type: research
---

# Group Sequence Policy Optimization (GSPO)

Zheng, Liu, Li, Chen, Yu et al. — Qwen Team, Alibaba; arXiv:2507.18071 (2025). GRPO's token-level importance ratios are a fundamental misapplication of importance sampling: a single next-token sample cannot correct a distributional mismatch, so each ratio is pure noise. The noise accumulates over long responses and is amplified by the clipping mechanism, producing irreversible model collapse in practice. GSPO replaces the per-token ratio with a sequence-level importance ratio that has clear theoretical meaning, applies clipping at the sequence level, and aligns the unit of optimization with the unit of reward. Used in Qwen3 RL training.

## Method

**Token-level ratio in GRPO/PPO.** Both PPO and GRPO weight each token gradient by its per-step ratio:

$$w_{i,t}(\theta) = \frac{\pi_\theta(y_{i,t} \mid x, y_{i,<t})}{\pi_{\theta_\text{old}}(y_{i,t} \mid x, y_{i,<t})}$$

Since $y_{i,t}$ is a single draw from $\pi_{\theta_\text{old}}(\cdot \mid x, y_{i,<t})$, this ratio does not perform the distribution correction that importance sampling requires (which demands averaging over many samples). Instead it introduces i.i.d. multiplicative noise at every token. For a response of length $|y|$, the objective accumulates $|y|$ such noise terms; the clipping on each term further distorts gradients unpredictably. The paper observes irreversible collapse that cannot be recovered by rolling back checkpoints or retuning hyperparameters (§3).

**GSPO: sequence-level importance ratio.** The sequence-level ratio $s_i(\theta)$ is defined as the geometric mean of per-token likelihood ratios — equivalently, the exponentiated average log-ratio:

$$s_i(\theta) = \left(\frac{\pi_\theta(y_i \mid x)}{\pi_{\theta_\text{old}}(y_i \mid x)}\right)^{1/|y_i|} = \exp\!\left(\frac{1}{|y_i|}\sum_{t=1}^{|y_i|} \log \frac{\pi_\theta(y_{i,t} \mid x, y_{i,<t})}{\pi_{\theta_\text{old}}(y_{i,t} \mid x, y_{i,<t})}\right)$$

Length normalisation is load-bearing: without it, a few token flips can cause dramatic fluctuations in $\pi_\theta(y_i|x)/\pi_{\theta_\text{old}}(y_i|x)$, and sequences of different lengths would require different clipping ranges (§4.1).

**Sequence-level clipping objective.** The GSPO objective clips entire responses, not individual tokens:

$$J_\text{GSPO}(\theta) = \mathbb{E}_{x \sim \mathcal{D},\, \{y_i\}_{i=1}^G \sim \pi_{\theta_\text{old}}(\cdot|x)} \left[ \frac{1}{G} \sum_{i=1}^G \min\!\left( s_i(\theta)\,\hat{A}_i,\; \text{clip}(s_i(\theta),\, 1-\varepsilon,\, 1+\varepsilon)\,\hat{A}_i \right) \right]$$

with group-normalised advantages $\hat{A}_i = \bigl(r(x, y_i) - \text{mean}\{r(x, y_i)\}_{i=1}^G\bigr) / \text{std}\{r(x, y_i)\}_{i=1}^G$.

**Gradient comparison.** The GSPO gradient weights every token in $y_i$ equally by $s_i(\theta) \cdot \hat{A}_i / |y_i|$ (Eq. 10). GRPO weights each token by its own $w_{i,t}(\theta)$, which can fall anywhere in $(0, 1+\varepsilon]$ (for $\hat{A}_i > 0$) or $[1-\varepsilon, +\infty)$ (for $\hat{A}_i < 0$) — unequal, unbounded, and accumulating (§4.2).

**GSPO-token variant.** For multi-turn settings requiring per-token advantage signals, the paper introduces GSPO-token (Eq. 13–17), which uses $s_{i,t}(\theta) = \text{sg}[s_i(\theta)] \cdot \pi_\theta(y_{i,t}|x,y_{i,<t}) / \text{sg}[\pi_{\theta_\text{old}}(y_{i,t}|x,y_{i,<t})]$. When all token advantages are identical, GSPO-token is numerically equivalent to GSPO (§4.3).

## Claims

**Training stability and efficiency (Qwen3-30B-A3B-Base cold-start, §5.1).** GSPO trains stably throughout; GRPO collapses. Under equal training compute and consumed queries, GSPO achieves higher training accuracy and benchmark performance on AIME'24 (Pass@1 ×32), LiveCodeBench (Pass@1 ×8), and CodeForces (Elo).

**Clipping fraction paradox (§5.2).** GSPO clips ~15% of tokens on average; GRPO clips ~0.13% — a difference of two orders of magnitude. Despite discarding far more gradient signal, GSPO trains more efficiently. The authors interpret this as evidence that GRPO's unclipped token-level gradients are noisy and waste sample exploitation capacity.

**MoE stabilisation without Routing Replay (§5.3).** In MoE models (e.g., Qwen3-30B-A3B), expert routing changes between $\pi_{\theta_\text{old}}$ and $\pi_\theta$ after each gradient step — roughly 10% of activated experts differ in the 48-layer model. This makes token-level ratios $w_{i,t}(\theta)$ wildly inconsistent: the numerator and denominator activate different experts. Alibaba's prior workaround was *Routing Replay* (cache the old routing, force $\pi_\theta$ to replay it when computing $w_{i,t}$), which adds memory/communication overhead and limits model capacity. GSPO operates on sequence likelihoods, which are robust to routing volatility since the overall LM capability does not collapse between gradient steps. GSPO trains MoE models stably with no Routing Replay.

**Infrastructure simplification (§5.4).** Token-level log-probs must be recomputed with the training engine (Megatron) to avoid precision discrepancies with inference engines (SGLang, vLLM). Sequence-level likelihoods tolerate these discrepancies, so GSPO can use inference-engine outputs directly — relevant for partial rollout, multi-turn RL, and disaggregated training/inference.

**Qwen3.** GSPO is the RL optimiser for the Qwen3 model family (Qwen, 2025a, arXiv:2505.09388).

## Relevance to the project

GSPO's sequence-level framing is the cleaner design for single-sample or small-N settings where token-level gradient noise dominates. When N is small and reasoning chains are long, the accumulated noise from per-token importance ratios is proportionally worse — there is no statistical averaging over many sequences to wash it out. GSPO's clipping discipline (clip the whole response if it has drifted too far from the old policy) is a principled way to enforce on-policy proximity without the volatility penalty GRPO pays. This connects to [[dr-grpo]], which independently diagnoses the same GRPO instability from a variance-reduction angle and proposes a different correction (dual-clip + reference-free normalisation). [[dapo]] addresses orthogonal pathologies (entropy collapse, reward hacking) via a separate recipe of token-level clipping removal and dynamic sampling; the two analyses are complementary rather than competing.

## Source

- arXiv: https://arxiv.org/abs/2507.18071
- Raw: `../../../raw/research/rl-optimizers/07-08-gspo-alibaba.md`

## Related

- [[_overview]]
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO ancestor and primary foil
- [[dapo]] — orthogonal stabilisation recipe (token-level clip removal, entropy bonus)
- [[dr-grpo]] — independent diagnosis of the same GRPO instability
- [[ppo]] — PPO baseline from which GRPO and GSPO both derive
