# PoEM: Predicting RL Outcomes from Existing Policies

MIT CSAIL (Hamidieh, Daras, Torralba; arXiv:2609.30226, Sept 2026). PoEM (Product-of-Experts Mixing) predicts what RL post-training on a *new* reward would produce by composing the log-probabilities of policies already RL-trained on other rewards, from a shared reference model — no new RL run required.

## Method

Setup: a reference model `π_ref` and a basis of policies `π_1..π_n`, each post-trained on a distinct reward `r_k` via the standard KL-regularized RL objective. Core theory: if a target reward `r_tar = Σ α_k r_k` is an exact linear combination of basis rewards, the KL-regularized RL optimum for `r_tar` is a product of experts in policy space — a weighted sum of policy log-ratios `φ_k = log π_k − log π_ref`. Applied token-locally for autoregressive LMs: `log π_PoEM(y_t|h_t) = log π_ref(y_t|h_t) + Σ α_k φ_k(h_t,y_t)` — needs only next-token logits from reference and basis policies, no parameter updates, no rollout. For diffusion models, the same log-mixture is derived via Tweedie's formula on the denoiser's output.

Composition weights `α` are recovered by ridge regression: either against basis rewards on a small calibration set, or — when only trained policies are available, not their reward functions — against the basis policies' own log-ratios (motivated by the DPO observation that `βφ_k` is the implicit reward `π_k` is KL-optimal for). A **coverage score** (held-out R² of target reward vs. basis log-ratios) is computed *before* decoding to predict whether PoEM will succeed on a given target reward, without running RL or needing `π_tar`.

Derives directly from DPO's closed-form KL-regularized-RL optimum and decode-time model-combination methods (DExperts, contrastive decoding, proxy-tuning, MOD, DeRa) — the novelty is deriving combination weights from theory rather than hand-specifying them, plus the a-priori coverage diagnostic.

## Results

Five bases spanning text RL (GRPO/DPO on Qwen3-0.6B), reward-model RL (PPO on public RMs), and image diffusion (DDPO on SD v1.4). Metric: `rec(π) = (r(π)−r(π_ref))/(r(π_tar)−r(π_ref))`, 0 = reference, 1 = matches actual RL policy.

- Combined (linear-combo) rewards: PoEM recovers 0.78–1.08 of RL's reward gain on reward-model bases; recovery error (0.19–0.28) is "close to the difference between two independent RL runs with different seeds" (0.12–0.17).
- Geometry: 20 near-orthogonal LoRA adapters (median pairwise cosine 0.02 in weight space, effective rank 19.4/20) collapse to effective rank 6.3/20 in log-ratio (policy) space — near-orthogonal weight updates span far fewer directions in log-likelihood space than in parameter space.
- Held-out (non-linear-combo) rewards: coverage score ranks reward error in advance (Spearman ρ = −0.71 to −0.81). On a 10-reward diverse basis, PoEM beats the single top expert on 9/10 held-out rewards; best-of-16 matches PoEM's reward recovery but needs the actual reward function plus 16 samples/prompt at decode time, which PoEM avoids.
- Image diffusion: composing 12 experts qualitatively reproduces a held-out DDPO expert's effect (saturation, texture, subject centering).

## Applicability

Any team running RL post-training that maintains (or could maintain) a basis of single-reward-trained policies/adapters sharing one reference model and KL coefficient. Needs a small calibration set scorable under the target reward. Most valuable when the target reward is expensive to evaluate (large RM, LLM judge, human rater) or when many reward combinations need cheap previewing before committing to a full RL run. Less useful when best-of-N is already cheap, or when the basis doesn't span the new reward's direction — the coverage diagnostic is the paper's own failure-mode detector for this.

## Reproducibility

No code, PapersWithCode entry, or released weights. Algorithmic descriptions are detailed enough to reimplement; base models (Qwen3-0.6B, public RMs, SD v1.4) are public, but the specific trained expert basis is not confirmed released.

## Source

- raw/research/weekly-2026-09-26/04-poem-predicting-rl-outcomes.md
- arXiv: https://arxiv.org/abs/2609.30226

## Related

- [[llamarl]] — parallel motivation (cost/instability of running RL from scratch), different fix: PoEM predicts instead of accelerating.
- [[magistral]] / [[rl-teachers]] / [[reasonmaxxer]] — general RL-post-training cluster. PoEM's finding that RL mostly re-weights existing policy directions echoes ReasonMaxxer's finding that RL modifies only a sparse slice of token positions — both point at RL's effective degrees of freedom being much smaller than the full parameter space, at different granularities.
- [[gepa-reflective-prompt-evolution]] — sibling "skip the RL run" motivation via a different mechanism (reflective prompt evolution vs. decode-time policy composition).

Tangential to, not contradicting, [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — that cluster asks *why* RLVR gradients help; PoEM asks whether RL's *outcome* can be predicted without running it at all.
