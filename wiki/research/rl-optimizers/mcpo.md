---
name: mcpo
description: GRPO variant from Ant Group; hinge-KL anchor on mastered prompts + advantage-denominator rescaling to flatten the p(1-p) query-weight bias; consistent pass@1 and pass@8 gains over DAPO on Qwen3-8B/14B-Base
type: research
---

# MCPO: Mastery-Consolidated Policy Optimization for Large Reasoning Models

Liao et al. (Ant Group / Zhejiang University), arXiv:2604.16972. MCPO addresses two neglected failure modes in GRPO-family RLVR that persist even in DAPO: (i) mastered prompts ($p(x)=1$) receive zero gradient, leaving the policy unconstrained — causing ~5% one-step accuracy regression on those prompts within a single global update; (ii) majority-correct prompts ($p(x) > 0.5$) are systematically downweighted because GRPO's implicit query weight is $\propto p(1-p)$, which peaks at $p=0.5$ and shrinks monotonically toward 1 — the opposite of the empirically bimodal rollout-accuracy distribution. MCPO adds a hinge-KL regulariser exclusively on mastered prompts and rescales the advantage denominator for $p(x)>0.5$ to flatten the query weight to a constant $0.5$. The method builds on DAPO's clip-higher and seq-mean-token-mean objective, dropping Dynamic Sampling entirely in favour of retaining and anchoring mastered prompts.

## Method

### Biased query weight in GRPO (Sec 4.2, Eq 6)

DisCO (cited as [15]) decouples the GRPO objective into a query-level weight and a discriminative term. For binary rewards with rollout precision $p(x)$:

$$\mathcal{J}_\text{GRPO}(\theta) = \mathbb{E}_{x\sim\mathcal{D}} \left[ \underbrace{\sqrt{p(x)(1-p(x))}}_{\text{query weight}} \cdot \underbrace{\mathbb{E}_{y^+\sim\pi^+_{\theta_\text{old}},\, y^-\sim\pi^-_{\theta_\text{old}}}\!\left[s^+_\theta(y^+,x) - s^-_\theta(y^-,x)\right]}_{\text{discriminative term}} \right] \tag{6}$$

The weight $\sqrt{p(x)(1-p(x))}$ peaks at $p=0.5$ and falls to zero at $p\to 0$ or $p\to 1$. Removing the std-normalisation term (Dr. GRPO's fix) does not change this: the $p(1-p)$ factor is structural, arising from the group statistics themselves (Appendix A.3, Eq A.3: $\text{std}=\sqrt{p(1-p)}$ for binary rewards), not from the normalisation. The difficulty bias therefore persists after std removal.

The empirical rollout-accuracy histogram (Fig 3a) is bimodal — most prompts sit near $p\approx 0$ or $p\approx 1$. GRPO assigns maximum weight to the $p\approx 0.5$ minority and near-zero weight to the majority.

### Hinge-KL regulariser on mastered prompts (Sec 5.1, Eq 10–11)

Let $\mathcal{M}$ denote the set of mastered prompts in the current batch ($p(x)=1$, all rollouts correct). For each token $t$ in response $y$ sampled from $\pi_\text{old}$, define the log-ratio drift:

$$d_t(x,y) = \log\pi_\theta(y_t\mid x,y_{<t}) - \log\pi_\text{old}(y_t\mid x,y_{<t}) \tag{7}$$

Approximate reverse-KL per token via the $k_3$ estimator:

$$k_3(d_t) = e^{d_t} - d_t - 1 \tag{8}$$

With drift budget $\delta=0.01$, define threshold offsets $c_+ = k_3(\delta)$, $c_- = k_3(-\delta)$. The hinge penalty is:

$$\phi(d_t) = \begin{cases} 0, & |d_t| \le \delta \\ k_3(d_t) - c_+, & d_t > \delta \\ k_3(d_t) - c_-, & d_t < -\delta \end{cases} \tag{10}$$

The hinge-KL term (applied only on $\mathcal{M}$):

$$\mathbb{D}_\text{HKL}(\pi_\text{old}\|\pi_\theta) = \mathbb{E}_{x\in\mathcal{M}}\,\mathbb{E}_{y\sim\pi_\text{old}(\cdot|x)}\!\left[\frac{1}{|y|}\sum_{t=1}^{|y|}\phi(d_t(x,y))\right] \tag{11}$$

Tolerates small benign drift; penalises excursions beyond $\delta$. Applied between consecutive gradient steps (current $\pi_\theta$ vs. last-step $\pi_\text{old}$), not against a frozen reference.

### Advantage-denominator rescaling (Sec 5.2, Eq 12–14)

For each prompt $x$ with rollout precision $p(x)$, MCPO modifies the advantage denominator:

$$\hat{A}_i^\text{MCPO}(x) = \frac{R_i - \text{mean}(\{R_j\})}{\text{std}(\{R_j\}) \cdot \text{scale}(p(x))} \tag{12}$$

$$\text{scale}(p(x)) = \begin{cases} 1, & p(x) \le 0.5 \\ 2\sqrt{p(x)(1-p(x))}, & p(x) > 0.5 \end{cases} \tag{13}$$

This yields a flat query weight for $p(x)>0.5$ (Appendix proof, Eq A.14–A.15):

$$W(x) = \begin{cases} \sqrt{p(x)(1-p(x))}, & 0 < p(x) \le 0.5 \\ 0.5, & p(x) > 0.5 \end{cases} \tag{14}$$

For $p(x)\le 0.5$ the GRPO weight is unchanged; the fix is applied only where majority-correct prompts are being underweighted. Mastered prompts ($p=1$) contribute no reward gradient but are covered by the hinge-KL term above.

### Full objective (Eq 15)

$$\mathcal{J}_\text{MCPO}(\theta) = \mathbb{E}_{x\sim\mathcal{D}}\!\left[W(x)\cdot\mathbb{E}_{y^+,y^-}\!\left[s^+_\theta - s^-_\theta\right]\right] - \beta\,\mathbb{D}_\text{HKL}(\pi_\text{old}\|\pi_\theta) \tag{15}$$

with $\beta=1$. Dynamic Sampling (DAPO's all-correct/all-wrong filter, Eq 3 constraint) is removed; mastered prompts are retained and anchored instead.

## Claims

Main results, Table 1 (pass@1 averaged over $k=8$ samples at temperature 0.7):

| Model | Method | AIME24 pass@1 | AIME24 pass@8 | AIME25 pass@1 | AIME25 pass@8 | AMC23 pass@1 | AMC23 pass@8 |
|---|---|---|---|---|---|---|---|
| Qwen3-8B-Base | DAPO | 0.400 | 0.648 | 0.308 | 0.482 | 0.844 | 0.971 |
| Qwen3-8B-Base | MCPO | **0.446** | **0.701** | **0.333** | **0.507** | **0.866** | **0.984** |
| Qwen3-14B-Base | DAPO | 0.529 | 0.762 | 0.404 | 0.598 | 0.894 | **0.988** |
| Qwen3-14B-Base | MCPO | **0.558** | **0.775** | **0.429** | **0.644** | **0.909** | 0.981 |

AIME24 pass@1 gain on 8B: +4.58 points. AIME25 pass@1 gain on 8B: +2.5 points. AMC23 (near-saturated baseline) still gains +2.18 pass@1 points on 8B.

Counter-intuitive pass@k result: MCPO improves pass@8 simultaneously with pass@1 — +5.29 on AIME24, +2.49 on AIME25. This is inconsistent with a simple exploitation-exploration trade-off; the paper interprets it as mastery consolidation enabling broader solution diversity (Sec 6.2). MCPO also reduces entropy explosion relative to DAPO (Fig 6) without triggering entropy collapse.

Ablation (Table 2, Qwen3-8B-Base): hinge-KL alone accounts for most pass@1 gain; reweighting alone accounts for most pass@8 gain. Both together dominate on 5/6 metrics. Exception: AIME25 pass@1 is slightly better with hinge-KL only (0.3375 vs 0.3333 for full MCPO).

Training dynamics (Fig 5, Fig 7):
- Mastered-prompt fraction grows to ~25% in DAPO; MCPO yields a **higher** fraction throughout training (Fig 5a).
- All-wrong fraction is **lower** under MCPO throughout (Fig 5b) — consolidation on top appears to improve hard-prompt coverage indirectly.
- One-step accuracy retention on mastered prompts: DAPO ~95%; MCPO higher floor with smaller fluctuations (Fig 7). Neither achieves zero regression.

## Relevance to the project

MCPO's mastered-prompt problem is the exact failure mode flagged in [[../rlvr-mechanics/_overview]] for $N=1$ GRPO. In the single-sample regime, zero-variance (all-correct or all-wrong) groups are the norm, not the exception — nearly every prompt after early learning will be either fully mastered or fully outside the model's capability. GRPO silently contributes zero gradient for all such prompts, and any update from other prompts can corrupt what was already learned.

MCPO's hinge-KL anchor provides a concrete, lightweight mechanism to prevent this: apply a per-step KL budget to mastered prompts so that updates from hard prompts cannot freely overwrite acquired concepts. The $k_3$ estimator makes this computationally cheap (no reference model query; only current-vs-previous-step log-ratio). For $N=1$ training — where the "mastered" state is binary and the fraction of mastered prompts could grow rapidly — the hinge-KL term becomes the primary regularisation signal replacing the gradient signal that standard GRPO loses entirely.

The $p(1-p)$ query-weight analysis also connects directly to the DOTS $p(1-p)$ theorem noted in [[../single-sample-rl-finetuning/data-efficiency-rft]]: both identify the same structural mismatch between GRPO's implicit weighting and the empirical difficulty distribution. MCPO's denominator rescaling is a complementary fix at the objective level (vs. DOTS's data-selection perspective).

## Source

- arXiv: https://arxiv.org/abs/2604.16972
- Raw: `../../../raw/research/weekly-2026-04-23/03-mcpo-mastery-consolidated.md`

## Related

- [[_overview]]
- [[dapo]] — MCPO is a direct extension of DAPO; drops Dynamic Sampling, adds hinge-KL + advantage rescaling on top of DAPO's clip-higher and seq-mean-token-mean objective
- [[dr-grpo]] — Dr. GRPO removes std normalisation to fix difficulty bias; MCPO shows this is incomplete (Sec 4.2, Eq 6) — the $p(1-p)$ factor survives std removal; MCPO's denominator rescaling is required for $p>0.5$
- [[gspo]]
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO ancestor; MCPO's query-weight analysis derives directly from the GRPO advantage formula (Eq 6 via DisCO [15])
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — DOTS's $p(1-p)$ theorem is the data-selection analogue of MCPO's objective-level reweighting; both address the same structural bias
- [[../synthesis/single-sample-concept-skeleton]] — Mastered-prompt consolidation maps directly onto the skeleton's concept-acquisition / catastrophic-forgetting hypothesis
- [[../../weekly-briefs/2026-04-23]] — brought in by the 2026-04-23 weekly sweep

## Conflicts raised

**1. MCPO vs. Dr. GRPO — difficulty-bias fix is incomplete**

Dr. GRPO (Liu et al. [30], [[dr-grpo]]) claims that removing std normalisation from GRPO advantages achieves unbiased, difficulty-invariant updates. MCPO (Sec 4.2, Eq 6, citing DisCO [15]) shows this is false: after std removal, the query weight is still $\propto p(x)(1-p(x))$ — the structural $\sqrt{p(1-p)}$ factor comes from the group standard deviation itself (Appendix Eq A.3), not from the normalisation term that Dr. GRPO removes. The difficulty bias therefore persists. MCPO's advantage-denominator rescaling (Eq 13–14) is required to actually flatten the weight for $p(x)>0.5$.

**2. MCPO vs. DAPO — Dynamic Sampling is actively harmful**

DAPO ([[dapo]]) endorses Dynamic Sampling (filter all-correct and all-wrong groups, Eq 3 constraint) as improving training efficiency with minimal information loss. MCPO (Sec 4.1, Fig 2) shows that discarding mastered prompts removes the anchoring gradient that would otherwise prevent policy drift, causing ~5% mean one-step accuracy regression on previously mastered prompts (measured across all training steps on Qwen3-8B-Base / DAPO-17K). MCPO retains mastered prompts, anchors them with hinge-KL, and achieves a higher mastered-prompt fraction and lower all-wrong fraction throughout training (Fig 5) — the opposite of what Dynamic Sampling is intended to produce.
