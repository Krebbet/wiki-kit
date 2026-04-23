---
name: rl-optimizers-overview
description: Theme overview — the RL-for-LLM optimiser lineage from PPO → InstructGPT → DPO → GRPO → post-GRPO variants (DAPO, Dr. GRPO, GSPO) + preference-optimisation siblings (KTO) and the REINFORCE-is-enough line (RLOO). Covers what each algorithm changes, why, and where each fits in the sample-efficient regime.
type: research
---

# RL Optimisers for LLM Post-Training

The lineage of policy-optimisation algorithms used to post-train LLMs. This theme collects the canonical papers behind PPO, RLHF-with-PPO, DPO, GRPO (host page in [[../rlvr-mechanics/deepseekmath-grpo]]), and the 2024-2025 wave of GRPO refinements (DAPO, Dr. GRPO, GSPO), plus the REINFORCE-suffices critique (RLOO) and the Kahneman-Tversky/HALO alternative (KTO). Each page documents the algorithm's method, empirical claims, and relevance to single-sample concept learning. This overview stitches the family tree together.

## Pages

- [[ppo]] — Schulman et al. (2017). Clipped surrogate objective, adaptive KL variant, actor-critic + GAE. Foundation of all LLM RLHF.
- [[instructgpt]] — Ouyang et al. (OpenAI, 2022). Canonical three-stage RLHF: SFT → RM → PPO(+ptx). 1.3B InstructGPT preferred over 175B GPT-3.
- [[dpo]] — Rafailov et al. (NeurIPS 2023). Closed-form policy from Bradley-Terry preferences; no RL loop, no reward model, no value function.
- [[rloo]] — Ahmadian et al. (ACL 2024). REINFORCE Leave-One-Out. Many PPO components are unnecessary in RLHF; RLOO beats PPO and DPO on TL;DR and HH.
- [[kto]] — Ethayarajh et al. (ICML 2024). Prospect-theory-derived HALO using binary desirable/undesirable signal instead of preference pairs.
- [[../rlvr-mechanics/deepseekmath-grpo]] — Shao et al. (DeepSeek-AI, 2024). GRPO: drop the critic, group-relative baseline, KL in the loss. Unified gradient view of SFT/RFT/DPO/PPO/GRPO.
- [[dapo]] — Yu et al. (ByteDance Seed + Tsinghua AIR, 2025). Open-source GRPO recipe: Clip-Higher, Dynamic Sampling, Token-Level PG Loss, Overlong Reward Shaping. 50 AIME'24 on Qwen2.5-32B.
- [[dr-grpo]] — Liu et al. (SAIL, COLM 2025). *Understanding R1-Zero-Like Training*. Identifies length- and std-normalisation biases in GRPO; removes them.
- [[gspo]] — Zheng et al. (Alibaba Qwen, 2025). Sequence-level importance ratio and clipping; stabilises MoE RL; powers Qwen3.

## Family tree *(synthesis)*

```
                                PPO (Schulman 2017)
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
          InstructGPT (Ouyang 2022)   DPO (Rafailov 2023)   REINFORCE line
          SFT→RM→PPO+ptx              offline preference     │
                    │                    │                   RLOO (Ahmadian 2024)
                    │                    │                    │
                    │                    KTO (Ethayarajh 2024)│
                    │                    HALO / binary signal │
                    │                                         │
                    └──────── GRPO (Shao 2024) ───────────────┘
                              group-relative, critic-free
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                DAPO (2025)         Dr. GRPO (2025)       GSPO (2025)
                4 tricks            unbiased objective    sequence-level IS
                no KL               COLM best paper       Qwen3 RL
```

*(Diagram is an editorial family tree; inclusion of an arrow does not imply direct citation in every case.)*

## What each algorithm actually changes

| Algorithm | Canonical paper | Importance sampling | Baseline / critic | KL placement | Distinctive move |
|---|---|---|---|---|---|
| PPO | [[ppo]] | Token-level ratio + clipping | Learned value $V_\phi$ + GAE | Optional adaptive KL *or* clip | Clipped surrogate replaces trust region |
| InstructGPT | [[instructgpt]] | Token-level (PPO) | $V_\phi$ | KL-to-SFT inside reward + pretraining-mix gradient (ptx) | Three-stage RLHF template |
| DPO | [[dpo]] | — (offline) | — | Implicit via $\beta \log \pi/\pi_{\mathrm{ref}}$ | Reparameterise reward; no RL loop |
| RLOO | [[rloo]] | — (on-policy, single sample) | Leave-one-out over $k$ samples | KL inside reward | Sequence-level MDP; drop the critic; drop PPO's clip |
| KTO | [[kto]] | — (offline) | Reference point (KL-weighted $\pi_{\mathrm{ref}}$ baseline) | Implicit via HALO | Binary signal, Kahneman-Tversky value function |
| GRPO | [[../rlvr-mechanics/deepseekmath-grpo]] | Token-level ratio + clipping | **Group statistics** $(r - \mathrm{mean})/\mathrm{std}$ over $G$ rollouts | KL added to loss (not reward) | Drop $V_\phi$, group baseline |
| DAPO | [[dapo]] | Token-level | Group | **Dropped** | Clip-Higher + Dynamic Sampling + Token-Level PG Loss + Overlong Reshape |
| Dr. GRPO | [[dr-grpo]] | Token-level | Group (no std) | Loss | Remove $1/\|o_i\|$ length normalisation and std normalisation |
| GSPO | [[gspo]] | **Sequence-level** ratio $(\pi_\theta/\pi_{\mathrm{old}})^{1/\|y\|}$ | Group | Loss | Sequence-level clip; stabilises MoE |

## Cross-cutting themes *(synthesis)*

**The critic is optional.** PPO's $V_\phi$ is roughly the same size as the policy. Every post-PPO method removes it: RLOO via leave-one-out, DPO via closed-form reparameterisation, KTO via a reference point, GRPO by group-relative advantage, and all post-GRPO variants inherit this. The critic's job — reducing per-step variance so that TD targets are usable — is replaced by either sample-based baselines (RLOO, GRPO) or simply sidestepping the RL loop entirely (DPO, KTO). For small-$G$ / single-sample settings, the critic-free path is non-negotiable: there's no dataset to train $V_\phi$ on.

**Importance sampling is the unsettled axis.** PPO's per-token ratio with clipping is carried forward by [[../rlvr-mechanics/deepseekmath-grpo]] and [[dapo]]; [[gspo]] argues the per-token form is a misapplication of importance sampling when the whole trajectory is treated as one action (as in LLM rollouts) and switches to a sequence-level ratio; [[rloo]] observes the same and argues the entire apparatus of PPO-style importance weighting is unnecessary for RLHF. Sequence-level framing unifies RLOO and GSPO; token-level framing is a PPO-inheritance. The project needs to pick a side.

**KL placement is a five-way split.** PPO puts KL either inside the reward (InstructGPT-style) or as an adaptive outer term. DPO and KTO absorb KL implicitly into their loss via $\beta$. GRPO moves KL into the loss directly with Schulman's positive unbiased estimator. DAPO drops the KL-to-reference term entirely, arguing it is not needed in RLVR on reasoning tasks. Dr. GRPO keeps GRPO's placement but fixes the length/std biases. For single-sample training the KL choice determines how far the policy can drift off a single prompt before the anchor pulls it back — load-bearing for stability.

**Length bias is a convergent finding from multiple directions.** [[dapo]]'s Token-Level PG Loss (uniform per-token weighting), [[dr-grpo]]'s removal of $1/|o_i|$ normalisation, and [[gspo]]'s sequence-level ratio all address the same structural problem: per-response normalisation in GRPO treats long wrong answers as equally bad as short wrong answers, but a per-token policy gradient gives them more weight. Three different fixes for the same root cause, identified independently in early-to-mid 2025.

**Preference optimisation is a self-contained subtree.** DPO → KTO → IPO/ORPO/SLiC are all offline, no-rollout algorithms that reduce RLHF to a supervised loss over static preference (or binary-signal) data. They are dominant for small-compute alignment but largely disjoint from the RLVR-for-reasoning line (GRPO/DAPO/GSPO), which assumes on-policy rollouts and verifiable rewards. [[rloo]] is the bridge: on-policy, verifiable-reward-friendly, but structurally much simpler than PPO or GRPO.

**Open-source adoption has crystallised around GRPO-family RLVR.** Per [[../teacher-student-rl/rlt-followups-2026]], Qwen3 / MiMo / GLM-5 / Thinking Machines all use On-Policy Distillation variants in post-training; the RL loop used for reasoning training inside Qwen3 is [[gspo]]. DAPO is the open reference implementation used by the verl framework. GRPO-with-fixes is now the default recipe for open reasoning models.

## Method comparison — sample-efficiency lens

| Method | Samples per prompt | Compute relative to PPO | Sample-efficiency niche | Page |
|---|---|---|---|---|
| PPO | 1 rollout + $V_\phi$ | 1× (baseline) | Generic RL; any reward signal | [[ppo]] |
| InstructGPT | PPO + 2× pretraining mix | ~1× (ptx adds cost) | RLHF with human labels | [[instructgpt]] |
| DPO | 0 rollouts (offline) | ~0.2× (no RL loop) | Fixed preference dataset | [[dpo]] |
| RLOO | $k \geq 2$ rollouts (typically 2–4) | "~3× faster, 70% less RAM" vs PPO (Ahmadian blog, based on [[rloo]] table 1) | LLM RLHF with sparse rewards | [[rloo]] |
| KTO | 0 rollouts (offline) | ~0.2× | Imbalanced binary signal | [[kto]] |
| GRPO | $G \geq 16$ rollouts (typically 64) | 0.5× memory vs PPO at 7B; $G\times$ rollout cost | RLVR on math/reasoning | [[../rlvr-mechanics/deepseekmath-grpo]] |
| DAPO | $G$ rollouts + Dynamic Sampling filter | Similar to GRPO per effective prompt | Long-CoT RLVR at scale; 50% fewer training steps than R1-Zero | [[dapo]] |
| Dr. GRPO | $G$ rollouts (as GRPO) | As GRPO | SOTA on AIME 2024 with 27 hours on 8×A100 (Qwen2.5-Math-7B) | [[dr-grpo]] |
| GSPO | $G$ rollouts (as GRPO) | As GRPO, plus smaller clip ranges | MoE RL; Qwen3 scale | [[gspo]] |

## Open questions *(editorial)*

- **Single-sample regime:** with a training set of size 1, GRPO's group baseline reduces to per-prompt variance; DOTS's $p(1-p)$ result (see [[../single-sample-rl-finetuning/data-efficiency-rft]]) implies that a single prompt whose pass-rate drifts out of $[0.2, 0.8]$ produces near-zero gradient. Which post-GRPO fix handles this best — DAPO's Dynamic Sampling (can't help with N=1), Dr. GRPO's unbiased objective (yes, reduces gradient instability near the boundary), or GSPO's sequence-level ratio (orthogonal)? Not tested in the captured literature.
- **DPO vs RLOO contradiction:** [[dpo]] reports PPO failing to beat Pythia-2.8B base on HH while DPO does; [[rloo]] reports RLOO beating both PPO and DPO across TL;DR and HH. The two papers disagree about DPO's performance. A close reading of the experimental protocol differences (base model, reward model, KL budget) would resolve this — the wiki does not currently do this.
- **Does the Dr. GRPO / DAPO Token-Level-Loss convergence generalise to RLT's $r^{SS}$?** [[../teacher-student-rl/sakana-rlt]]'s reward is a sequence-level log-prob over the solution. It is not clear whether the length/std biases Dr. GRPO identifies apply when the reward is already sequence-level. Untested.
- **RLOO vs GRPO with small $G$.** RLOO with $k=2$ is approximately GRPO with $G=2$ without std normalisation. Is there a regime where RLOO strictly dominates GRPO at low $G$? [[rloo]]'s comparison uses PPO and DPO as baselines; GRPO is not in the Ahmadian et al. evaluation.

## Source PDFs

- `../../../raw/research/rl-optimizers/02-01-ppo-schulman.md`
- `../../../raw/research/rl-optimizers/04-02-instructgpt-ouyang.md`
- `../../../raw/research/rl-optimizers/01-03-dpo-rafailov.md`
- `../../../raw/research/rl-optimizers/06-04-rloo-ahmadian.md`
- `../../../raw/research/rl-optimizers/03-05-kto-ethayarajh.md`
- `../../../raw/research/rl-optimizers/05-06-dapo-bytedance.md`
- `../../../raw/research/rl-optimizers/08-07-dr-grpo-liu.md`
- `../../../raw/research/rl-optimizers/07-08-gspo-alibaba.md`
- (GRPO source is under `single-sample-llm-learning/` — see [[../rlvr-mechanics/deepseekmath-grpo]])

## Related themes

- [[../rlvr-mechanics/_overview]] — sparse-subnetwork and info-gain reward are orthogonal to optimiser choice
- [[../single-sample-rl-finetuning/_overview]] — where these optimisers get stressed at N=1
- [[../teacher-student-rl/_overview]] — teacher-optimisation uses GRPO/RLOO-family inner loops
- [[../teacher-student-rl/rlt-followups-2026]] — GSPO, DAPO commercial adoption at Qwen3/MiMo/GLM-5
- [[../synthesis/proposed-method]] — project roadmap uses GRPO as host loop; selection among GRPO/DAPO/Dr. GRPO/GSPO is an open choice
