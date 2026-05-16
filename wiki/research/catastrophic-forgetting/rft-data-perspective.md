---
title: "Why RFT Preserves Prior Knowledge Better: A Data Perspective"
arxiv: "2506.23508"
tags: [catastrophic-forgetting, rlvr, data-distribution, learning-dynamics, sft-vs-rft]
status: read
date_added: 2026-05-16
---

# Why Reinforcement Fine-Tuning Enables MLLMs to Preserve Prior Knowledge Better: A Data Perspective

The central empirical finding is sharp: SFT masters novel tasks quickly but incurs severe catastrophic forgetting; RFT learns more slowly but retains prior knowledge. The paper's contribution is explaining *why* through a data-distribution account grounded in learning-dynamics theory — not algorithmic differences alone. The forgetting gap closes almost entirely when SFT trains on RFT-generated rollouts, implicating corpus distribution as the causal driver.

## Source

- arXiv: 2506.23508  
- Raw: `raw/research/rlvr-forgetting/05-04-rft-data-perspective.md`

## Method

**Setup.** Qwen2.5-VL-3B/7B are fine-tuned on 3×3 jigsaw puzzles — a task absent from pretraining corpora (GPT-4o and Qwen-2.5-VL-72B both score 0.0 zero-shot). This gives a clean "genuinely novel task" baseline for measuring forgetting.

**The data ablation.** Four training conditions are compared:

| Condition | Data source | Forgetting |
|---|---|---|
| SFT-Non-Rea | human labels, no CoT | severe |
| SFT-Rea-4o-Rollout | GPT-4o CoT | moderate |
| RFT (GRPO) | self-generated rollouts | mild |
| SFT-Rea-GRPO-Rollout | filtered RFT rollouts used as SFT data | mild (matches RFT) |

The last row is decisive: SFT trained on RFT-generated rollouts achieves similar prior-task retention as RFT with the same SFT training dynamics. The algorithm is not the variable; the corpus is.

**Learning-dynamics framework.** Following Ren & Sutherland (2024), the paper tracks how a gradient step on training example $x_u$ shifts the log-probability of prior-knowledge example $x_v$:

$$\Delta\log\pi^t(x_v)\big|_{x_u} = \eta\, A^t(x_v)\; K^t(x_v, x_u)\; G^t(x_u) + O(\eta^2) \tag{Thm. 5.1}$$

where $K^t(x_v, x_u) = (\nabla_\theta z(x_v))(\nabla_\theta z(x_u))^\top$ is the empirical neural tangent kernel (eNTK) of the logit network. Because $A^t$ and $G^t$ (gradient vectors w.r.t. logits) are bounded, the eNTK norm $\|K^t\|_F$ dominates: larger kernel $\Rightarrow$ more interference $\Rightarrow$ more forgetting.

**Magnitude axis — eNTK lower bound (LBK).** The authors estimate a tractable lower bound:

$$\mathrm{LBK}^t_{uv} \;\propto\; \frac{\|\Delta\log\pi^t(x_v)|_{x_u}\|_F^2}{\|A^t(x_v)\|_F^2 \|G^t(x_u)\|_F^2} \;\lesssim\; \|K^t(x_v, x_u)\|_F^2$$

Measured empirically: Non-Rea data has the largest LBK; Rea-4o-Rollout is smaller; Rea-GRPO-Rollout is smallest. The LBK stabilises within a few dozen steps, validating the assumption that eNTK is approximately constant over training.

**Direction axis — perplexity alignment.** A second theorem gives a symmetry property:

$$\Delta\log\pi^t(x_v)\big|_{x_u} = \Delta\log\pi^t(x_u)\big|_{x_v} + O(\eta^2) \tag{Thm. 5.2}$$

Consequence: training on $x_u$ degrades $\pi(x_v)$ by roughly the same amount as training on $x_v$ would degrade $\pi(x_u)$. So if the base model already assigns moderate probability to $x_u$ (low PPL), it is close in gradient-space to $x_v$ (prior knowledge), and their mutual interference is small.

RFT rollouts concentrate in **low-perplexity** regions of the base model — regions that pretraining already partially shaped. GPT-4o CoT lies in high-PPL regions, disrupting prior knowledge more despite having smaller LBK magnitude than Non-Rea data. RFT surfaces latent "hidden linguistic regions" that are simultaneously compatible with the novel task and with the prior distribution; SFT corpus construction has no natural mechanism to find them.

**SFT–RFT cooperation.** Even one epoch of RFT (jigsaw accuracy < 5%) produces rollouts whose CoT, paired with correct answers, yields an SFT corpus (Rea-Self-Generated) that matches full-RFT forgetting levels. The heavy exploration phase is not required; what is required is that the rollout distribution is model-aligned.

## Claims

1. RFT (GRPO) on a genuinely novel task achieves 66–75% accuracy from a 0% baseline, demonstrating RFT can push models beyond their original capability boundary given sufficient exploration steps.
2. SFT achieves comparable novel-task accuracy in ~10–20× fewer steps but causes catastrophic forgetting across grounding, OCR, VQA, and college-level benchmarks; RFT retains near-baseline performance.
3. SFT trained on filtered RFT rollouts (SFT-Rea-GRPO-Rollout) largely matches RFT's forgetting profile, confirming data distribution — not the GRPO weighting mechanism — as the key factor.
4. Non-Rea > Rea-4o > Rea-GRPO is a consistent forgetting hierarchy across jigsaw (MLLM), math reasoning (LLM), and scientific QA settings.
5. eNTK norm (LBK) predicts forgetting severity across data types; reasoning trajectories reduce LBK vs. direct answer supervision.
6. Model-generated rollouts have lower base-model perplexity than GPT-4o CoT; the symmetry theorem (Thm. 5.2) then guarantees less mutual interference with prior-knowledge examples.
7. Short RFT (1 epoch, < 5% jigsaw accuracy) is sufficient to generate alignment-compatible CoT; a subsequent SFT pass on this data achieves strong task performance with low forgetting.

## Strengths / Novelty

- Clean causal isolation: the SFT-Rea-GRPO-Rollout condition rules out GRPO's adaptive reweighting as the mechanism, leaving data distribution as the only active variable.
- Formal grounding in learning-dynamics (eNTK theory), with an empirically measurable proxy (LBK) that stabilises early and tracks forgetting.
- The symmetry theorem (Thm. 5.2) provides a principled link between perplexity alignment and forgetting magnitude.
- Three domains (jigsaw, math, science QA) and two model scales all show the same hierarchy, strengthening generality.
- Practical implication is immediately actionable: run short RFT for distribution alignment, then switch to SFT.

## Weaknesses / Limits

- Jigsaw puzzle evaluation is narrow — a single structured permutation task with a clear verifier. Forgetting on open-ended generation tasks may pattern differently.
- The eNTK analysis assumes kernel stability over training; this holds early but may break during long RFT runs with large learning-rate schedules.
- PPL is a loose proxy for gradient alignment; the actual direction of interference (sign of $K^t(x_v, x_u)$) is not measured, only its magnitude.
- "Low-PPL rollouts preserve prior knowledge" rests on the symmetry theorem, which itself is a first-order ($O(\eta^2)$) approximation. Second-order effects are not characterised.
- No mechanistic account of *which* parameter subsets carry the interference — this is addressed by the mechanistic companion paper [[mechanistic-forgetting]].

## Relevance to this wiki's project

The anchoring question is: **"Does RLVR just move optimization around when stacking skills?"** This paper answers with a precise no: RLVR does not simply relocate the gradient burden — it selects a qualitatively different slice of data space. Self-generated rollouts are low-PPL under the base model, and by the symmetry theorem their gradients are near-parallel to prior-knowledge gradients, so mutual interference is small. When stacking a new skill (jigsaw on top of grounding, math on top of instruction-following), RFT preserves prior performance not by regularizing weights but by operating inside the model's existing probability landscape.

For the proposed single-sample concept curriculum ($R_w$ in [[../synthesis/proposed-method]]), this is directly load-bearing: if concept acquisition is bootstrapped by self-generated rollouts rather than externally curated targets, the curriculum can add new concepts without erasing prior ones. The data-perspective account predicts that rollout quality (low PPL) matters more than rollout quantity or reward magnitude.

## Connections to the wiki

- [[rft-mitigates-forgetting]] — the phenomenon this page explains; pair these two for the full picture.
- [[rls-razor]] — KL-minimality account of why online RL reduces forgetting. That account is algorithmic (implicit KL bias); this paper is data-centric (low-PPL corpus alignment). The two are complementary: KL-minimality keeps the policy close to the reference, and low-PPL rollouts are one mechanism by which that closeness manifests in the data. The authors explicitly acknowledge RL's Razor and frame their contribution as an additional data-centric layer.
- [[path-not-taken]] — related question of which gradient directions are taken vs. avoided.
- [[ewc-gemma2-cpt]] — regularization-based approach to forgetting; the data-perspective account suggests data selection may dominate regularization as a practical lever.
- [[mechanistic-forgetting]] — companion mechanistic paper on which model components carry forgetting.
- [[empirical-forgetting]] — empirical characterization of forgetting patterns; provides the quantitative context for the hierarchy Non-Rea > Rea-4o > Rea-GRPO.
- [[_overview]] — catastrophic forgetting theme index.
- [[../self-improvement/star]] — STaR bootstraps on-policy self-generated data to iteratively improve; the low-PPL alignment argument here directly supports why on-policy data (as in STaR) is more training-stable than fixed human-curated datasets.
- [[../synthesis/proposed-method]] — $R_w$ reward and concept curriculum design; low-PPL rollout selection is a candidate inductive bias for the data-generation loop.
- [[../selective-finetuning/pit]] and [[../selective-finetuning/_overview]] — parameter-isolation approaches to forgetting; data-perspective account suggests data selection is a lighter-weight alternative.

## Related

- Ren & Sutherland (2024) — learning dynamics framework this paper builds on.
- GRPO / DeepSeekMath — the RFT algorithm used: [[../rlvr-mechanics/deepseekmath-grpo]].
- Shenfeld et al. (2025), "RL's Razor" — KL-minimal account, referenced as prior work.
