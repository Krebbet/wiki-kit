---
name: instructgpt
description: Canonical three-stage RLHF-with-PPO pipeline (SFT → RM → PPO-ptx) that aligns GPT-3 to human intent — 1.3B InstructGPT preferred over 175B GPT-3 by human raters.
type: research
---

# InstructGPT: Training Language Models to Follow Instructions with Human Feedback

Ouyang et al. — OpenAI, arXiv:2203.02155 (2022). Introduces the canonical three-stage RLHF pipeline: supervised fine-tuning on human demonstrations, reward model training on human preference comparisons, then PPO optimisation against that reward model. The key result is that a 1.3B InstructGPT model is preferred over the 175B base GPT-3 by human raters despite having 100× fewer parameters, demonstrating that alignment training quality dominates raw scale. PPO-ptx mixes pretraining log-likelihood back into PPO gradients to eliminate the "alignment tax" on public NLP benchmarks.

## Method

### Three-stage pipeline

**Step 1 — Supervised Fine-Tuning (SFT).** Fine-tune GPT-3 on 13K labeler-written demonstrations of desired behavior. Training for 16 epochs with cosine decay and residual dropout 0.2; model selection by RM score on validation set. The SFT model overfit on token-level validation loss after epoch 1 but continued to improve on human preference ratings.

**Step 2 — Reward Model (RM).** Starting from SFT with the final unembedding layer removed, train a 6B scalar-reward model on 33K human comparison labels. Labelers rank K = 4–9 responses per prompt, producing $\binom{K}{2}$ comparison pairs. All pairs from a prompt are batched together to avoid overfitting. RM loss (Eq. 1):

$$\mathcal{L}(\theta) = -\frac{1}{\binom{K}{2}} \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}} \left[\log \sigma\!\left(r_\theta(x,y_w) - r_\theta(x,y_l)\right)\right]$$

where $r_\theta(x,y)$ is the scalar reward for prompt $x$ and completion $y$, $y_w$ the preferred completion, $y_l$ the rejected one. Reward is normalised so labeler demonstrations have mean score 0 before RL.

**Step 3 — RL with PPO (PPO-ptx).** Fine-tune SFT via bandit-episode PPO on 31K prompts. A per-token KL penalty from the SFT reference policy is added to prevent reward over-optimisation. PPO-ptx mixes pretraining log-likelihood gradients to suppress alignment-tax regressions. Combined objective (Eq. 2):

$$\text{objective}(\phi) = \mathbb{E}_{(x,y)\sim\mathcal{D}_{\pi_\phi^{RL}}} \!\left[ r_\theta(x,y) - \beta \log \frac{\pi_\phi^{RL}(y\mid x)}{\pi^{SFT}(y\mid x)} \right] + \gamma\, \mathbb{E}_{x\sim\mathcal{D}_\text{pretrain}} \!\left[\log \pi_\phi^{RL}(x)\right]$$

$\beta$ controls KL strength; $\gamma$ controls the pretraining mix. Pure PPO sets $\gamma = 0$. "InstructGPT" in the paper always refers to the PPO-ptx variant.

### Dataset sizes

| Split | Size | Source |
|---|---|---|
| SFT | 13K prompts | API + labeler-written |
| RM | 33K prompts | API + labeler-written |
| PPO | 31K prompts | API only |

### Model sizes

Three variants trained: 1.3B, 6B, 175B. All use the GPT-3 architecture. RM fixed at 6B (175B RM training unstable; unsuitable as value function).

## Claims

**Preference over GPT-3 (§4.1, Fig. 1).**
- 1.3B InstructGPT (PPO-ptx) preferred over 175B GPT-3. (100× parameter advantage reversed.)
- 175B InstructGPT preferred over 175B GPT-3 **85 ± 3%** of the time.
- 175B InstructGPT preferred over few-shot 175B GPT-3 **71 ± 4%** of the time.
- Preference holds for held-out labelers not in the training set, and on GPT-3-native prompts.

**Truthfulness — TruthfulQA (§4.2, Fig. 6).** PPO-ptx models generate truthful and informative answers ~2× as often as GPT-3. Improvement holds on the subset of questions not adversarially selected against GPT-3.

**Hallucination (§4.2, Fig. 4).** On closed-domain API tasks (summarization, closed-domain QA), InstructGPT hallucinates **21%** of the time vs **41%** for GPT-3 — roughly half the rate.

**Toxicity — RealToxicityPrompts (§4.2, Fig. 7).** InstructGPT generates ~25% fewer toxic outputs than GPT-3 when prompted to be respectful. Bias benchmarks (Winogender, CrowS-Pairs) show no significant improvement.

**Alignment tax (§1, §4.2).** Plain PPO regresses on SQuAD, DROP, HellaSwag, WMT Fr→En. PPO-ptx ($\gamma > 0$) largely eliminates these regressions without degrading labeler preference scores.

**NLP benchmark comparison (§4.1).** InstructGPT preferred over FLAN-tuned GPT-3 **78 ± 4%** of the time and over T0-tuned GPT-3 **79 ± 4%** of the time, despite FLAN/T0 using ~1M training examples vs InstructGPT's ~13K SFT demonstrations.

**Generalisation (§4.1).** Held-out labelers (no training data produced) prefer InstructGPT at the same rate as training labelers. Reward model cross-validation accuracy: 72.4 ± 0.4% (in-distribution) vs 69.6 ± 0.9% (held-out), showing limited overfitting to labeler idiosyncrasies.

## Relevance to the project

InstructGPT is the ancestral implementation for essentially every LLM RL training recipe in the literature. The three-stage structure (SFT cold-start → scalar reward model → policy optimisation with KL regularisation) is the template that DeepSeekMath-GRPO, DPO, RLOO, DAPO, and all subsequent variants modify, replace, or extend. The PPO-ptx objective is the direct antecedent of the per-token KL term that appears throughout modern RLVR work — the $\beta \log(\pi^{RL}/\pi^{SFT})$ term in Eq. 2 is preserved almost verbatim in GRPO, DAPO, and DR-GRPO's reference-policy regularisers. For the single-sample learning project, the SFT → RM → RL stack demonstrates that a small number of high-quality signal examples (13K for SFT, 33K for RM) can produce behaviour qualitatively superior to raw scale — a precedent for the claim that concept-level signal at N ≈ 1–100 scale can be effective.

## Source

- arXiv: https://arxiv.org/abs/2203.02155
- Raw: `../../../raw/research/rl-optimizers/04-02-instructgpt-ouyang.md`

## Related

- [[_overview]]
- [[ppo]] — base optimiser (Schulman et al., 2017)
- [[dpo]] — DPO (Rafailov et al., 2023) proposes eliminating the RM and PPO in favour of a direct preference objective
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO extends InstructGPT's KL-regularised objective to group-relative advantage estimation
