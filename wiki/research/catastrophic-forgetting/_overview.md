---
name: catastrophic-forgetting-overview
description: Theme overview — what happens to prior skills/knowledge when you stack new ones onto an LLM via SFT vs RL. Answers the skill-stacking question: RLVR does NOT freely reallocate optimization; on-policy updates are biased toward KL-minimal, off-principal, sparse solutions, so RLVR forgets far less than SFT. Seven pages: EWC seed, RL's Razor, Path-Not-Taken, RFT-mitigates-forgetting (+ data-perspective), mechanistic decomposition, empirical baseline. Bridges to selective-finetuning and moe-adapters as the three structural answers to interference.
type: research
---

# Catastrophic forgetting under skill-stacking

The operative question for this wiki: **when you stack a new skill or body of knowledge onto a model, what happens to the old ones — and does RLVR just move optimization from one skill to another (zero-sum reallocation)?** This theme assembles the empirical, mechanistic, and theoretical evidence. The short answer the corpus gives: **no, RLVR is not freely zero-sum** — on-policy RL updates are structurally constrained (KL-minimal, off-principal, sparse) in a way that SFT updates are not, so RLVR forgets *far less* than SFT at matched new-task accuracy. But it is also **not free**: the constraint is a bias, not a guarantee, and the off-principal "spare capacity" RLVR routes through is a shared pool that can deplete.

## Pages

| Page | Role | One-line |
|---|---|---|
| [[ewc-gemma2-cpt]] | Seed (explicit regularisation) | Fisher-weighted EWC anchor on Gemma2 CPT — preserves English on 7/7 benchmarks while gaining Lithuanian on 5/7. The *explicit-penalty* answer to forgetting. |
| [[rls-razor]] | **The "why" (theory)** | Shenfeld et al. (MIT, 2025) — at matched new-task accuracy RL forgets less than SFT; forgetting is predicted by KL-to-base on the new task; on-policy updates are biased toward **KL-minimal** solutions among the many that solve the task. |
| [[path-not-taken]] | **The "how" (mechanism)** | RLVR provably makes sparse, structured updates **off the principal directions** of the weight matrices — Three-Gate Theory. The mechanistic form of "reallocates without overwriting principals." |
| [[rft-mitigates-forgetting]] | **The skill-stacking experiment** | Continual post-training, 7 sequential tasks: SFT catastrophically forgets prior tasks; RFT learns slower but retains. The direct stacking test. |
| [[rft-data-perspective]] | The "why" (data) | Companion to above — the data-distribution account: RFT's on-policy self-generated rollouts (PPL-symmetric, low eNTK magnitude) preserve prior knowledge; SFT's fixed targets do not. |
| [[mechanistic-forgetting]] | Mechanistic decomposition | Gradient interference in attention, representational drift, loss-landscape flattening. Six models; inspectable open-weight max 400B (1.5T figure is an API-only estimate — see page). |
| [[empirical-forgetting]] | Empirical baseline (2023) | Luo et al. — the foundational SFT-forgetting characterisation (scale, task order, decoder vs encoder) that the RL-side papers improve on. |

## The answer to the skill-stacking question

Three corpus findings, converging:

1. **RL stays KL-close to base ([[rls-razor]]).** Among the many parameter settings that solve the new task, on-policy RL is biased toward the one minimal in KL-divergence from the base policy *on the new-task distribution*. SFT has no such bias and can land arbitrarily far. KL-to-base is a reliable *predictor* of how much prior capability is lost. So RLVR-stacking does not freely reallocate — it preferentially picks the solution that disturbs the base least.
2. **RL updates are off-principal and sparse ([[path-not-taken]]).** The mechanistic realisation of (1): RLVR's weight updates avoid the principal directions of the pretrained weight matrices, routing through low-magnitude off-principal subspace. Principal directions (where prior skills live) are largely untouched — so stacking is *better than zero-sum*, not a simple reallocation. Caveat the page raises: the off-principal pool is shared across stacked skills and can deplete; and SFT's principal-direction overwrites are the asymmetric-risk case.
3. **Empirically, stacking via RFT retains; via SFT it catastrophically forgets ([[rft-mitigates-forgetting]], [[rft-data-perspective]]).** The 7-task continual-post-training experiment confirms (1)+(2) behaviourally. The data-perspective page supplies the orthogonal explanation: on-policy self-generated data is PPL-symmetric and low-eNTK-magnitude, so it perturbs prior-task representations less than fixed SFT targets.

This sharpens, rather than contradicts, the wiki's existing R_w / Invisible-Leash backbone. [[../self-play/invisible-leash]] Theorem C.1 says RL stays within base *support*; RL's Razor says RL stays KL-*close* within that support; Path-Not-Taken says it does so by avoiding *principal directions*. Three nested constraints, same conclusion: **RLVR is a constrained, locality-preserving update, not a free reallocation of optimization across skills.**

## Three structural answers to interference (cross-theme)

The corpus offers three distinct ways to stack skills without catastrophic interference. This theme is one of them; the other two are sibling themes:

| Answer | Mechanism | Where |
|---|---|---|
| **Implicit constraint** | RL's on-policy KL-minimality / off-principal sparsity makes monolithic stacking gentle | *this theme* ([[rls-razor]], [[path-not-taken]], [[rft-mitigates-forgetting]]) |
| **Explicit constraint** | Mask / anchor / orthogonalise the gradient so it cannot move prior-skill params | [[../selective-finetuning/_overview]] (EWC, PackNet, HAT, O-LoRA, AlphaEdit null-space) |
| **Architectural avoidance** | Don't co-train skills at all — train experts separately, route at inference | [[../moe-adapters/_overview]] (BTX parallel experts, LoRAMoE routed plugins, Self-MoE) |

[[ewc-gemma2-cpt]] (this theme's seed) is actually an *explicit-constraint* method and is the natural hinge to [[../selective-finetuning/_overview]]; [[../moe-adapters/loramoe]] is the natural hinge to [[../moe-adapters/_overview]] (it is a forgetting-mitigation method built from routed LoRA experts). The three themes are complementary, not competing — they target the implicit / explicit / architectural axes respectively.

## Connection to existing wiki anchors

- **[[../synthesis/proposed-method]] — component L (format-fluency guard) + R_w.** RL's Razor + Path-Not-Taken are the mechanistic justification for why an RLVR-based installation loop degrades response style less than an SFT-based one. The 1-shot-RLVR gibberish-at-1.4k-steps failure ([[../single-sample-rl-finetuning/1-shot-rlvr]]) is the boundary case where even RL's KL-minimality is overwhelmed (single mastered prompt, unbounded drift) — RL's Razor explains why that is the *exception*, not the rule.
- **[[../rlvr-mechanics/rl-sparse-subnetwork]] (Balashov) + [[../rlvr-mechanics/rethinking-rl-sparse-selection]] (REASONMAXXER).** Path-Not-Taken's off-principal sparsity is the *forgetting-side* counterpart of Balashov's 5–30%-of-weights and REASONMAXXER's 1–4%-of-tokens findings. Same underlying claim — RL's footprint is small and structured — viewed from the forgetting angle rather than the capability angle.
- **[[../self-play/invisible-leash]].** Support-preservation (Theorem C.1) is the outermost of the three nested RL-locality constraints; RL's Razor (KL-minimality) and Path-Not-Taken (off-principal) are tighter inner constraints.
- **[[../selective-finetuning/pit]].** PIT's instruction-tune-before-CPT ordering is the *recipe-level* forgetting-mitigation; the RFT papers here are the *optimizer-level* answer. Composable.

## Open questions

1. **Does off-principal capacity deplete under repeated RLVR stacking?** [[path-not-taken]] raises this as the live risk: the shared off-principal pool is finite. No captured paper measures the $N$-th-skill degradation curve under sequential RLVR.
2. **RL's Razor at single-sample scale.** RL's Razor's KL-minimality argument assumes a distribution of solving solutions. At $N=1$ (1-shot RLVR) the "many solutions" premise weakens — does the KL-minimal bias still hold, or does the [[../single-sample-rl-finetuning/1-shot-rlvr]] post-saturation gibberish regime indicate it breaks?
3. **Implicit vs explicit vs architectural — when to use which.** No captured source compares RL's-Razor implicit constraint against O-LoRA explicit orthogonalisation against BTX architectural separation on the *same* skill-stacking benchmark. The composition (RFT + O-LoRA mask + MoE routing) is untested.
4. **Mechanistic-forgetting's three mechanisms vs Path-Not-Taken's off-principal account.** Are gradient-interference / representational-drift / loss-landscape-flattening ([[mechanistic-forgetting]]) the *same* phenomenon as principal-direction overwrite ([[path-not-taken]]) viewed differently, or distinct? Not reconciled in either source.

## See also

- [[../selective-finetuning/_overview]] — explicit-constraint sibling (mask / anchor / orthogonalise)
- [[../moe-adapters/_overview]] — architectural-avoidance sibling (route separately-trained experts)
- [[../synthesis/proposed-method]] — R_w extension + component L; this theme is the "why RLVR is gentle" backbone
- [[../rlvr-mechanics/rl-sparse-subnetwork]] / [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — capability-side view of RL's small structured footprint
- [[../self-play/invisible-leash]] — support-preservation (outermost RL-locality constraint)

## Source

Theme synthesised 2026-05-16 from the existing EWC seed plus 6 papers captured in `raw/research/rlvr-forgetting/`. Per-paper traceability in each page's `## Source`. The "three nested constraints" framing and the implicit/explicit/architectural trichotomy are editorial cross-source synthesis, not claims from any single paper.
