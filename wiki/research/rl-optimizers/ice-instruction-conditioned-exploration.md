---
name: ice-instruction-conditioned-exploration
description: ICE — same-parameter instruction-conditioned rollouts broaden DAPO exploration, forward-KL self-distilled into the unconditioned deployed policy; +5.0% pass@1 at Qwen3-1.7B; restores pass@256 coverage lost to vanilla RL. Not a teacher/student or self-play method (identical weights, two prompt contexts).
type: research
---

# Instruction-Conditioned Exploration for Reinforcement Learning with Self-Distillation to an Unconditioned Policy

Dilkes, Yazdanpanah, Stein (Southampton, arXiv:2608.02087) propose ICE: append one of $N{=}5$ fixed behavioural instructions to the prompt during DAPO rollouts to broaden exploration, then pull the deployed *unconditioned* policy toward the correctness-filtered instruction-conditioned rollouts via forward-KL self-distillation. Critically, this is a **same-parameter, two-context** method, not a two-model teacher/student or self-play setup: teacher $\pi^T_\theta := \pi_\theta(\cdot\mid x, I)$ and student $\pi^S_\theta := \pi_\theta(\cdot\mid x)$ are the *identical weights* $\theta$, differing only in whether the prompt carries a behavioural instruction $I$; only the student is ever sampled at test time. At Qwen3-1.7B/4K it beats DAPO by +5.0% relative macro pass@1 across five held-out math benchmarks (5/5 wins, seed-paired 95% CI excludes zero), and — the result most relevant to this wiki — it demonstrates directly that RL raises pass@1 while shrinking pass@256 coverage *below the base model*, and that instruction-conditioned sampling from the same trained checkpoint restores that coverage. The gain does not replicate at Qwen3-4B (−4.5%, CI spans zero), diagnosed as a coverage-headroom failure: the instructions must already expand the *base* model's pass@k at that scale for the mechanism to have anything to transfer.

## Method

The composite instruction-conditioned policy is a mixture over instructions plus the null instruction:

$$\pi^{comp}_\theta(y\mid x) = \sum_I p(I)\,\pi_\theta(y\mid x, I), \qquad \operatorname{supp}(\pi^{comp}_\theta) = \bigcup_I \operatorname{supp}(\pi_\theta(\cdot\mid x, I)) \supseteq \operatorname{supp}(\pi_\theta(\cdot\mid x))$$

$I \in \{I_1,\dots,I_5\}$ are hand/LLM-authored behavioural nudges (e.g. "ask what symmetry does this problem have..."). Each rollout in a GRPO/DAPO group receives one instruction (or none); RL trains on these instruction-conditioned rollouts. This is exploration at the **context** level — sampling temperature/top-p are left at defaults (T=1.0, top_p=1.0); the instructions are what widens $\operatorname{supp}$, not added token-level stochasticity. The authors distinguish this "support composition" (union over conditioning contexts of one policy) from "support expansion" (a claim about parameter change).

Self-distillation extends π-distill (Penaloza et al. 2026). General objective:

$$J(\theta) = \alpha J^R_T(\theta) + (1-\alpha) J^R_S(\theta) - \beta_T D_{KL}(\cdot) - \beta_S D_{KL}(\cdot)$$

The headline **filtered** configuration sets $\alpha{=}1$ (RL reward flows only to the teacher context; no student reward term) and keeps a single forward-KL term pulling the student toward the correctness-filtered, renormalised teacher distribution $\pi^{T+}_\theta$ (only rollouts with $R(y,x)=1$):

$$J_{filt}(\theta) = J^R_T(\theta) - \beta_S\, D_{KL}\!\big(\operatorname{sg}[\pi^{T+}_\theta] \,\|\, \pi^S_\theta\big)$$

No extra rollouts versus vanilla DAPO — one extra forward pass per update for the student KL term. RL backbone is exactly DAPO: token-level loss aggregation, asymmetric clipping ($\epsilon_{low}{=}0.2$, $\epsilon_{high}{=}0.28$), dynamic sampling, overlong reward shaping, binary correctness reward.

## Results

| Setting | vs. DAPO baseline (macro pass@1, 5 held-out math benchmarks) | Bench wins | 95% CI |
|---|---|---|---|
| Qwen3-1.7B / 4K, filtered SD | **+5.0% rel. (+0.012 abs.)** | 5/5 | excludes zero |
| Qwen3-1.7B / 4K, teacher-only RL (no distillation, $\alpha{=}1$, no KL) | +1.9% | — | spans zero |
| Qwen3-1.7B / 8K, filtered SD | +3.5% | 3/5 | — |
| Qwen3-4B / 4K, filtered SD | **−4.5%** | 1/5 | spans zero, does not replicate |

Held-out set: AIME-24/25, MATH-500, HMMT-Feb/Nov-25; $n{=}5$ seeds, seed-paired bootstrap. Correctness filtering is essential: unfiltered forward-KL is catastrophic (−12.9% vs. DAPO). Giving the student its own reward term ($\alpha{<}1$, importance-corrected) destabilises training — truncation rate reaches 61.6% by step 400 with $\alpha{=}0$, response length 1.4× DAPO's.

## The pass@256 coverage-shrinkage finding

This is the paper's most load-bearing result for this wiki's RL-as-selection thread. At Qwen3-1.7B, **both DAPO and filtered SD fall below the base model's pass@256** after training (0.483 / 0.475 vs. base 0.512) — RL sharpens pass@1 at the cost of coverage, exactly the pattern formalised in [[../self-play/invisible-leash]] (Theorem C.1 / Corollary C.2: on-policy RL cannot expand support beyond the sampling distribution it started from; pass@k under $\pi_\theta$ is upper-bounded by pass@k under the reference $q$). What's new here: **sampling the same trained checkpoint with the behavioural instructions appended ("+ICE") restores pass@256 to near base-model level (0.508)** — i.e. the coverage lost by the gradient update is still latent in the checkpoint and recoverable via context conditioning, without any further training. This is an independent empirical confirmation of the invisible-leash claim from a new domain (instruction conditioning on math RL, vs. proposer/solver self-play), using the authors' own vocabulary of "support expansion vs. shrinkage" (after Wu et al. 2026) rather than Yue et al.'s framing.

The 4B non-replication is diagnosed through the same lens: at 4B the instructions fail to expand *base-model* pass@256 in the first place (instructed 0.558 vs. base 0.633 — instructions actually *reduce* coverage at this scale), whereas at 1.7B they do (0.544 vs. base 0.512). The authors offer this as a cheap pre-flight test: if instruction-conditioning doesn't already broaden the base model's support at a given scale, filtered self-distillation has nothing useful to transfer into the unconditioned policy.

## Not a teacher/student or self-play method — read this before citing

Despite the title's "asymmetric" framing and the "teacher"/"student" terminology, **ICE has no separate teacher network, no privileged information asymmetry beyond a prompt suffix, and no adversarial or proposer/solver game.** Teacher and student are literally the same parameters $\theta$; the only difference is whether the current forward pass sees an instruction $I$ appended to $x$. "Self-distillation" here means KL-transfer between two *context-conditionings* of one model — in the lineage of context distillation (Askell et al. 2021) — not multi-model or multi-copy self-play. This source does **not** bear on the open conflict between unified and two-model self-play designs; it sits entirely on the single-policy side of that question and should not be read as evidence either way.

## Limitations (authors')

- Gain does not transfer to Qwen3-4B at 4K (see coverage-headroom diagnosis above); only two model scales and two context lengths tested.
- Low seed counts ($n{=}3$–5; several preliminary variants single-seed); headline config selected on the same sweep that reports its promise — authors flag results as "mildly optimistic."
- AIME/HMMT benchmarks are 30 questions each with high pass@1 variance and overlapping skill content; win-counts in isolation overstate significance.
- MATH-500 likely leaked into Qwen3 pretraining.
- Single domain (verifiable math), single model family (Qwen3, thinking disabled).
- Instructions are fixed and untargeted per-problem — no adaptive/dynamic strategy generation (flagged as future work, citing Strategy-Guided Exploration, Szot et al. 2026).
- No comparison against the closest prior template-based exploration method (Prompt Augmentation, Lu et al. 2026); the only baseline is vanilla DAPO.

## Source

- `raw/research/weekly-2026-08-07/05-asymmetric-rl-self-distillation.md`

## Related

- [[sdpg-self-distilled-policy-gradient]] — the closest structural sibling: SDPG also augments GRPO with same-model, context-conditioned self-distillation (unconditional student vs. solution-conditioned teacher), but uses on-policy reverse-KL where ICE uses off-policy, correctness-filtered forward-KL. Both instantiate the "single-model, two-context self-distillation" family; they differ in KL direction and in what the teacher context conditions on (privileged solution vs. behavioural instruction).
- [[../self-play/invisible-leash]] — this paper's pass@256 shrinkage-then-recovery result is an independent empirical confirmation of Theorem C.1 / Corollary C.2 (on-policy RL cannot expand support past the sampling distribution), from a new domain and under different terminology ("support expansion/shrinkage" vs. "invisible leash").
- [[../rlvr-mechanics/_overview]] — reinforces the RL-as-selection-not-learning cluster: RL sharpens pass@1 while narrowing pass@k, consistent with the pattern-selection account already gathered there.
- [[../teacher-student-rl/_overview]] — terminology overlap only. ICE's "teacher"/"student" split is same-parameter and context-only, with no distinct teacher network and no held-out privileged information — distinct from that theme's core setups (an independently-parameterised or independently-trained teacher policy).
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — engages the same "does RLVR expand or merely reweight the reasoning boundary" question from the opposing (boundary-expansion) side; ICE's coverage data is more consistent with the reweighting account but shows the lost coverage is contextually recoverable.
- [[../../weekly-briefs/2026-08-07]] — brought in by the 2026-08-07 weekly sweep
