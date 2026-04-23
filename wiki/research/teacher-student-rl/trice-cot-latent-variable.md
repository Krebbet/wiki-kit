---
name: trice-cot-latent-variable
description: Phan, Hoffman et al. (Google, NeurIPS 2023) — TRICE. Treats CoT rationales as latent variables; maximises marginal log-likelihood of correct answer over rationales via MCMC-EM with a control variate. Learns from incorrect rationales, unlike STaR. Outperforms STaR, direct tuning, and SFT-on-human-rationales on GSM8K and BIG-Bench Hard.
type: research
---

# Training Chain-of-Thought via Latent-Variable Inference (TRICE)

Phan, Hoffman, Dohan, Douglas, Le, Parisi, Sountsov, Sutton, Vikram, Saurous — Google, NeurIPS 2023, arXiv:2312.02179. Reframes CoT fine-tuning as probabilistic latent-variable inference. The rationale $z$ is an unobserved latent; the LM defines a joint $p_\theta(z, y \mid x)$ over rationale and answer given a question $x$; the objective is the *marginal* log-likelihood of the correct answer, averaging over all possible rationales weighted by their prior probability given $x$. TRICE (Tuning Rationales with Independence-Chain Expectation-maximization) is the algorithm that makes this tractable: MCMC-EM with a persistent rationale memory and a novel control-variate gradient estimator.

## Method

Objective:

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_n \log p_\theta(y_n \mid x_n) = \frac{1}{N}\sum_n \log \sum_z p_\theta(z \mid x_n)\, p(y_n \mid z, x_n)$$

with a *binary* likelihood $p(y \mid z, x) = c(z, y) \in \{0, 1\}$ — i.e. a rationale either implies the correct answer or it does not. The gradient of the marginal log-likelihood is

$$\nabla_\theta \log p_\theta(y \mid x) = \mathbb{E}_{p_\theta(z \mid x, y)}[\nabla_\theta \log p_\theta(z \mid x)]$$

i.e. the expectation over the posterior on rationales conditioned on the correct answer. Sampling from this posterior is intractable, so TRICE runs MCMC over rationales:

1. **Initialise memory.** For each $(x_n, y_n)$, sample an initial rationale $z_n$ from a *hinted* guide distribution $q(z \mid x_n, y_n)$ that may condition on the correct answer (e.g. "give a rationale for this answer"). This resembles STaR's rationalisation step.
2. **Main loop.** Sample minibatch; for each $(x_m, y_m)$ retrieve rationale from memory; propose $\tilde{z} \sim p_\theta(z \mid x_m)$ from the current model; if $c(\tilde{z}, y_m) = 1$ replace the memory rationale with $\tilde{z}$.
3. **Basic gradient.** Average $\nabla_\theta \log p_\theta(z_{i_m} \mid x_{i_m})$ over correct rationales in the updated memory.
4. **Control-variate gradient.** Subtract $\beta_m \nabla_\theta \log p_\theta(\tilde{z}_m \mid x_{i_m})$ where $\beta_m$ is a leave-one-out estimate of the rationale-acceptance probability. This drives the gradient variance to zero as the model's rationale acceptance rate $\to 1$, and crucially it *uses incorrect rationales to push them down* rather than discarding them.
5. **Subsampled control variate.** Systematic resampling of the $L$ highest-weight rationale contributions cuts cost relative to the full control-variate estimator.

## Claims

Applied to GSM8K and BIG-Bench Hard:

- **TRICE outperforms STaR, direct tuning (with or without CoT), prompt-tuning, and even SFT on human-written rationales.**
- **Learns from incorrect rationales.** Via the control-variate term; STaR simply ignores examples where its rationalisation fails. The paper argues this is why TRICE stabilises convergence on harder examples.
- **Variance reduction to zero.** The control variate's expected value is zero (it's a score function), and the remaining noise shrinks as the model improves.
- **Unifies existing methods.** Self-consistency is interpreted as Monte-Carlo marginalisation at inference time; STaR as biased stochastic-EM that underweights hard examples; TRICE averages over rationales both at inference and at training.

## Positioning

TRICE is the theoretically cleanest member of the "rationale-as-latent, answer-likelihood-as-reward" family that [[sakana-rlt]] also belongs to. The algorithmic differences:

| Axis | RLT | TRICE |
|---|---|---|
| Teacher-student separation | Two models ($\pi_\theta$ vs $\pi_s$) | One model ($\pi_\theta$); rationale is latent |
| Solution access | Teacher sees solution; student does not | Initial rationales from a hinted guide that conditions on the answer |
| Reward / objective | $r^{SS} - \lambda r^{KL}$ (dense per-token log-probs) | Marginal log-likelihood of correct answer |
| Handling of wrong rationales | $r^{SS}$ drops them (low likelihood) but continuous | Basic estimator drops; control-variate uses them to push $\tilde{z}$ down |
| Optimisation | GRPO | MCMC-EM + control variate |

TRICE is closer to STaR than RLT in that the rationale-producer and the answer-producer are the same model. Its contribution is the probabilistic reformulation, which gives a principled handle on rationale-quality without requiring an external teacher.

## Source

- `../../../raw/research/teacher-student-reasoning-rl/07-trice-cot-latent-variable.md`
- arXiv: https://arxiv.org/abs/2312.02179
- Reference notebook: https://github.com/google-research/cascades/tree/main/cascades/examples/notebooks/trice.ipynb

## Related

- [[_overview]] — theme synthesis
- [[sakana-rlt]] — two-model RL version of the same objective shape
- [[ho-reasoning-teachers]] — Fine-tune-CoT: non-probabilistic rationale distillation
- [[../self-improvement/star]] — STaR. TRICE interprets STaR as biased stochastic-EM and improves by (a) not dropping hard examples, (b) learning from incorrect rationales via control variate
- [[../in-context-learning-theory/icl-bayesian-inference]] — Bayesian-ICL's "posterior over latent concepts" frame; TRICE is the training-time analogue with rationales instead of concepts
