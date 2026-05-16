---
title: "RFT Naturally Mitigates Forgetting in Continual Post-Training"
arXiv: "2507.05386"
date_captured: "2026-05-16"
theme: catastrophic-forgetting
tags: [rlvr, continual-learning, catastrophic-forgetting, grpo, sft-vs-rft, skill-stacking]
---

# Reinforcement Fine-Tuning Naturally Mitigates Forgetting in Continual Post-Training

Lai et al. (2025) run the cleanest apples-to-apples comparison yet: sequentially fine-tune the same
model on seven multimodal tasks, once with SFT and once with RFT (GRPO / RLOO / ReMax), and
track per-task retention throughout the sequence. SFT catastrophically forgets; RFT, without any
explicit replay or regularization, matches multi-task learning. The mechanism is not the KL penalty
or chain-of-thought — it is a reward-variance-scaled implicit regularizer that is structurally
inherent to the policy-gradient objective.

## Source

- arXiv: [2507.05386](https://arxiv.org/abs/2507.05386)
- Raw capture: `raw/research/rlvr-forgetting/01-03-rft-mitigates-forgetting.md`

## Method

**Continual post-training (CPT) setup.** Qwen2.5-VL-7B-Instruct is fine-tuned sequentially on
seven vision-language datasets in order: ScienceQA → TextVQA → VizWiz → GQA → Geometry3K →
PathVQA → Super-CLEVR. Full-parameter fine-tuning is used throughout (no LoRA). After completing
the full sequence, the model is evaluated on all seven task test sets and on three general benchmarks
(MMMU, MMLU-Pro, POPE).

**SFT baseline.** Standard next-token NLL loss on $(x, a^*)$ pairs. Learning rate $10^{-5}$,
batch size 24 via LLaMAFactory.

**RFT variants.** Three GRPO-family algorithms are compared:
- *GRPO* — group of $n=8$ rollouts; advantage $A(a_i) = (r_i - \bar{r})/\sigma_r$; KL penalty
  $\beta = 0.01$; reward $r = 0.9\,r_\text{acc} + 0.1\,r_\text{format}$.
- *RLOO* — leave-one-out baseline; $n$ rollouts.
- *ReMax* — greedy decoding as baseline.

All RFT runs share LR $10^{-6}$, rollout batch 512.

**Ablations.** GRPO w/o KL (removes $\beta\,D_\text{KL}$ term) and GRPO w/o CoT (direct QA
format, no chain-of-thought) isolate which components drive retention.

**RIF-RFT (proposed).** A rollout-based instance-filtering algorithm that discards samples
whose reward variance is zero across rollouts (the model always fails or always succeeds), focusing
compute on informative instances and improving training stability.

## Claims

- **SFT catastrophically forgets.** Sequential SFT achieves FM $= -10.4\%$ across the seven
  tasks. ScienceQA accuracy falls from $95.2\%$ to $76.1\%$ after the full sequence; final AvgAcc
  is $54.0\%$ vs. an MTL upper bound of $62.9\%$.

- **RFT inherently resists forgetting.** GRPO achieves FM $= -2.3\%$; RLOO FM $= -2.1\%$;
  ReMax FM $= -3.8\%$. GRPO final AvgAcc $= 60.0\%$, close to the MTL ceiling, **without any
  replay or explicit continual-learning strategy**.

- **RFT protects and enhances general capabilities.** After the full sequence, SFT degrades
  MMMU from $52.1\%$ to $40.1\%$ ($\downarrow 12.0\%$) and MMLU-Pro from $47.5\%$ to $30.6\%$
  ($\downarrow 16.9\%$). GRPO instead *improves* MMMU to $54.2\%$ ($\uparrow 2.1\%$) and POPE
  to $88.5\%$ ($\uparrow 1.9\%$).

- **KL penalty is not the primary mechanism.** Removing the KL term (GRPO w/o KL) yields
  essentially the same AvgAcc ($59.5\%$) and per-task retention. The KL term matters for
  *training stability* (requires restarts in later tasks) but not for anti-forgetting per se.

- **CoT is a performance booster, not a forgetting mitigator.** GRPO w/o CoT still achieves
  AvgAcc $59.4\%$ with strong retention, outperforming full GRPO on VizWiz ($63.8\%$ vs.
  $51.8\%$). Anti-forgetting is paradigm-level, not format-level.

- **Theoretical mechanism — reward-variance scaling.** Using FIM-based forgetting risk $R(g)
  \triangleq g^\top F_{k-1} g$, the paper proves:
  $$\mathbb{E}_{a \sim \pi_{\theta_{k-1}}}[R(g_\text{RFT}(a))] \approx \mathrm{Var}_{a \sim
  \pi_{\theta_{k-1}}}[r(x_k, a)] \cdot R(g_\text{SFT})$$
  Since reward variance is bounded by $1/4$ for normalized rewards, the RFT update's impact on
  prior-task-sensitive directions is always $\leq \tfrac{1}{4}$ that of the SFT gradient —
  automatically, with no added mechanism.

- **RIF-RFT trade-off.** Filtering zero-variance samples reduces data kept to $37$–$82\%$ per
  task but raises FM to $-4.5\%$ (slightly worse than full GRPO at $-2.3\%$) while meaningfully
  cutting compute.

## Strengths / Novelty

- **First direct SFT-vs-RFT CPT comparison** across seven diverse multimodal tasks with the same
  base model, full-parameter fine-tuning, and a rigorous FM metric.
- **Negative ablations are clean.** Both KL and CoT ablations hold across downstream tasks and
  three general benchmarks, ruling out the two most tempting confounds.
- **Theoretical grounding** via the reward-variance proposition gives a principled, checkable
  account of why forgetting is reduced — not just an empirical observation.
- General-benchmark evaluation (MMMU, MMLU-Pro, POPE) catches base-model degradation that
  task-only evaluation misses. The SFT MTL result ($\downarrow 14.3\%$ on MMLU-Pro) shows SFT
  is harmful even without sequentiality.

## Weaknesses / Limits

- Single model family (Qwen2.5-VL-7B); appendix includes other scales but results are not
  detailed in the main paper text reviewed here.
- All seven tasks use rule-based binary rewards (exact match). It is unknown whether the
  variance-scaling mechanism holds for soft or learned reward signals.
- The FM metric measures drop from *peak* performance, which for RFT may be lower than SFT's
  peak (RFT learns more slowly), making the FM gap partly a ceiling-effect artifact.
- RIF-RFT degrades FM ($-2.3 \to -4.5$) and AvgAcc ($60.0 \to 57.5$) relative to full GRPO;
  the efficiency gain may not be worth the capability cost for small datasets.
- No comparison to EWC, replay, or other classic CL baselines within the RFT paradigm.

## Relevance to this wiki's project

**Direct answer to the anchoring question: "When you stack skills/knowledge with RLVR, does it
just move optimization from one skill to another?"**

No — this paper shows it does not, at least empirically. Seven tasks stacked sequentially via
GRPO retain near-MTL performance on *all prior tasks*, not a zero-sum redistribution. The
theoretical mechanism explains why: each gradient is down-weighted in prior-task-sensitive
directions by the reward variance of the current sample. A sample the model already "knows"
(low variance — high reward consistently) produces a large, aggressive update, but that update
is on a direction the model is confident about, not on prior-task directions. A sample the model
is uncertain about produces a small, conservative update on all directions including prior-task
ones.

**Implication for single-sample concept acquisition via RLVR.** The paper's result is that RFT
"learns more slowly but maintains prior knowledge." For our project's skill-stacking scenario
(component L in $R_w$, successive concept curricula), this is structurally good news: each RLVR
step over a new concept will naturally damp disruption to previously stabilized concept weights.
The slow-learning property is a cost — single-sample RLVR may need iterative rollouts to
accumulate signal — but the anti-forgetting property means the ordering of concept introduction
matters less than feared under SFT. The RIF-RFT insight also suggests that concept samples with
zero reward variance (already mastered or totally out-of-reach) should be filtered before
issuing RLVR updates, concentrating compute on the productive frontier.

## Connections to the wiki

**Within catastrophic-forgetting theme:**
- [[rls-razor]] — the *why* at the parameter level: KL-minimality of RLVR updates explains why
  reward-variance-scaled gradients stay small in prior-task subspaces.
- [[path-not-taken]] — the *how* in terms of sparse subnetwork structure: off-principal sparsity
  complements the variance-scaling story.
- [[rft-data-perspective]] — companion paper (Zhang et al. 2025, cited here): shows that
  reasoning trajectories in SFT reduce forgetting, offering a data-format explanation that sits
  alongside this paradigm-level explanation.
- [[ewc-gemma2-cpt]] — EWC as the canonical explicit regularization baseline; this paper shows
  implicit variance-scaling outperforms EWC-style explicit mechanisms in practice.
- [[mechanistic-forgetting]], [[empirical-forgetting]] — situate the SFT forgetting findings
  within the broader mechanistic and empirical literature.
- [[_overview]] — top-level framing of the theme.

**Cross-theme:**
- [[../synthesis/proposed-method]] — component L (skill-stacking via RLVR in $R_w$) is the
  direct application of this paper's finding: RLVR is the preferred paradigm for sequential
  concept acquisition.
- [[../selective-finetuning/pit]] — PIT uses task ordering and parameter isolation to mitigate
  forgetting; RFT is the RL-based alternative that achieves similar retention without explicit
  ordering constraints.
- [[../selective-finetuning/_overview]] — broader context of forgetting mitigation strategies.
- [[../teacher-student-rl/opsd-compresses-rlvr]] — OPSD pipeline (SFT → RLVR → OPSD) relies
  on RLVR as the stable middle step; this paper validates that assumption.

## Related

- Chu et al. (2025), *SFT Memorizes, RL Generalizes* — distinguishes generalization vs.
  memorization; complementary to the forgetting axis here.
- Zhang et al. (2025), *RFT from a Data Perspective* (see [[rft-data-perspective]]) — reasoning
  trajectories in SFT reduce forgetting; cited directly by this paper as a complement.
- DeepSeek-R1 / GRPO (Shao et al. 2024) — the RFT algorithm used; see [[../rlvr-mechanics/deepseekmath-grpo]].
- EWC (Kirkpatrick et al. 2017) — FIM forgetting risk framework imported here for the
  theoretical analysis.
