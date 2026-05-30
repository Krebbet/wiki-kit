# Thesis Architecture Sketch — Looped + Routed-to-Specialized-Blocks + Graceful Exit

A first-pass architectural synthesis for the wiki's core thesis: a transformer that runs in a repetitive (looped) structure, routes per-token to specialized transformer blocks each iteration, and exits gracefully per-token when further computation stops improving the prediction. Every component below is attested by one or more foundation-batch sources; the composition is new — no source in the wiki implements all three together. This page is a working sketch, not a validated proposal.

## The three components and their recipes

### 1. Loop — Ouro-style weight-shared recurrence, middle-looped

Base architecture from [[looped-language-models]] (Ouro): a full N-layer decoder stack applied T∈{1,…,T_max} times with fully shared weights; RMSNorm + SwiGLU + RoPE; T_max=4. Ouro reduced T_max from 8 after Stage-1a gradient oscillations at 8 steps — treat 4 as a ceiling, not a starting point.

Structural refinement from [[looped-transformers-and-reasoning]]: **middle-looping**. Independent (non-tied) layers at entry and exit, only the middle block is looped. At 1B scale the middle-looped variant yields better perplexity and more uniform benchmark improvements than plain looping, except on math word problems where plain (12⊗2) wins 34.3% vs. 28.3%.

Prefer this over [[universal-transformer]]'s ACT halting and fixed-T: UT is the conceptual anchor but is only validated at base scale and is superseded empirically by Ouro on every dimension that matters for large-scale pretraining.

### 2. Routing — MICRO-style MOB with curriculum-seeded specialization

At each layer within the looped inner stack, replace the single transformer block with N full expert blocks (attention + FFN) dispatched by a per-token top-1 MLP router — the Mixture-of-Blocks (MOB) architecture from [[mixture-of-cognitive-reasoners-micro]], validated at 1B on LLAMA-3.2-1B base. Block-level (attention+FFN) beats FFN-only-MoE on specialization at tested scales; MICRO's appendix ablation documents this.

**Curriculum is load-bearing.** [[learned-routing-specialization]] (open conflict) documents that pure end-to-end learned routing reliably underspecializes (Mittal, Muqeeth, Lewis via [[modular-deep-learning-survey]]). MICRO's three-stage recipe addresses this: **Stage 1** seed on ~3k domain-pseudo-labeled examples with soft top-2 for stability; **Stage 2** router calibration on pseudo-labels; **Stage 3** hard top-1 SFT generalization on ~939k examples. The specialization that emerges persists through Stage 3 despite the absence of labels there.

**Autoregressive compatibility.** [[expert-choice-routing]] and [[mixture-of-depths]] both use expert-choice top-k, which is non-causal. MoD's aux MLP predictor (stop-gradient, >97% top-k membership accuracy early in training) is the most viable path; EC's batch-grouping proposal is unvalidated. MICRO's top-1 per-token routing is causal by construction and is the preferred primitive here.

**Heterogeneous expert types.** If experts are to be heterogeneous (attention-only, SSM, MLP), the wiki only supports fixed-position routing: [[mamba-2-and-ssm-hybrids]]' recipe at 8B/3.5T tokens is ~8–10% attention / ~43% SSM / ~50% MLP with hand-placed attention positions (paper 08 Algorithm 1, greedy spacing). **No wiki source validates learned routing over heterogeneous block types at any scale** — this is an open research question, not a validated design choice.

### 3. Exit — Ouro's entropy-regularized two-stage gate

Per-token per-step sigmoid over the final-layer hidden state yields exit probability λ_t; a survival-function formulation gives a discrete distribution p(t|x). From [[looped-language-models]]:

- **Stage I** joint training of LM and gate under KL-ELBO entropy regularization vs. a uniform prior (β=0.1→0.05). Without this, vanilla gradient descent collapses to always-T_max — depth bias is self-reinforcing.
- **Stage II** freeze LM weights, fine-tune gate with BCE against marginal-improvement labels.
- **Inference**: **Q-exit** — exit at the first step where the CDF ≥ q. Beats static baselines and hidden-state-difference heuristics by ~2–3 pp on MMLU at equal compute budget.

Use this over [[universal-transformer]]'s ACT, which is superseded empirically by Ouro's two-stage gate.

## Composed architecture

```
[entry layers (independent)] →
  loop_T {
    for each layer in inner stack:
      router_l: token → expert_k
      expert_k block (attention + FFN)
    exit gate (between iterations)
  } →
[exit layers (independent)]
```

Training composition (not attested in any source — design choice): Ouro's two-stage gate schedule must interleave with MICRO's three-stage routing curriculum. Neither source prescribes how.

## Considerations

- **Routing granularity**: block-level (attention+FFN), not FFN-only. MICRO's MoE ablation shows FFN-only loses the clean specialization pattern.
- **Routing hardness over training**: soft → hard. MICRO Stage 2 uses soft top-2 for calibration stability, hard top-1 from Stage 3 onward. [[block-operations-and-modular-routing]] also finds soft > hard on compositional tasks (Gumbel-ST underperforms softmax) but hard still beats FNN baselines.
- **Bits-per-parameter floor**: ~2 bits/param for factual memorization regardless of loop depth ([[looped-language-models]] on bioS/Mano synthetic knowledge tasks). Looping enhances *manipulation*, not *storage* — do not expect loop depth to substitute for parameters when the task is memorization.
- **Dispatch signal scope**: [[routing-mechanisms-in-modular-networks]] catalogues a local-to-global axis — MoD uses a scalar per token (maximally local), MICRO an MLP over token + context, SMFR the concatenation of all blocks (global within module), [[mamba-2-and-ssm-hybrids]] uses layer index (metadata, fixed). Scope effects on compositionality are underexplored.

## Painpoints (all wiki-attested — expect to encounter these)

- **KV cache reuse across loop steps is catastrophic.** [[looped-language-models]] reports GSM8K 78.92 → 18.73 with naïve first-step-cache reuse; >10-pt degradation with prefill-phase sharing. No clean solution in the batch.
- **Gradient oscillation beyond T_max=4.** Ouro hard-ceilinged T_max at 4 for this reason. Extrapolating beyond training T at inference degrades reasoning (though monotonically improves HEx-PHI safety — orthogonal).
- **RL alignment infrastructure broken.** [[looped-language-models]] reports RLVR with DAPO/GRPO produced zero gains over SFT; variable-depth early-exit incompatible with vLLM/SGLang fixed-path rollouts. Fixed-4-step RL also produced no gains — mechanism unexplained.
- **Naive gate training collapses to T_max.** Entropy regularization is non-negotiable.
- **Module collapse without load-balance scaffolds.** [[modular-deep-learning-survey]] catalogues across Mittal, Muqeeth, Lewis.
- **Chicken-and-egg router initialization.** Modules random at init → router cannot make principled decisions → modules never consistently routed → never specialize. MICRO's Stage-1 pseudo-label curriculum resolves this; pure end-to-end training does not. This is the single most load-bearing pain point for the composed design.
- **Perplexity vs. reasoning tradeoff is unresolved.** [[looped-vs-depth-scaling]] open. At iso-FLOP, looped models cover only 34–50% of the perplexity gap to non-looped; reasoning gains may or may not outweigh depending on the axis of comparison. No ≥7B iso-param · iso-FLOP · iso-token study exists.
- **Specialization creates active interference, not neutral silence.** [[mixture-of-cognitive-reasoners-micro]] reports ablating the Social expert on math *improves* GSM8K. Off-domain experts can actively harm, not merely sit idle.
- **Autoregressive top-k is non-causal.** EC and MoD both flag this. MICRO's top-1 per-token routing avoids it; EC-style expert-choice introduces it.
- **Compositional routing at language scale is untested.** [[block-operations-and-modular-routing]] is ≤500k params on synthetic tasks only; BPMNIST convergence lagged FNN baseline at 25k steps and only surpassed at 250k.
- **Hybrid prompt sensitivity.** [[mamba-2-and-ssm-hybrids]] reports hybrid Musique accuracy swings 10.63–16.16 under prompt reformulation vs. 15.25–17.68 for the Transformer baseline. Adding learned routing likely compounds this.

## Unanswered questions that directly block the design

- **Does learned routing reliably specialize without curriculum seeding?** ([[learned-routing-specialization]] — open conflict.) If no, the composed architecture is structurally dependent on an external labeling source (GPT-4o pseudo-labels or equivalent) and is not truly end-to-end trainable.
- **Does iso-param looping beat depth-scaling at language scale?** ([[looped-vs-depth-scaling]] — open.) Determines whether the looped core of the design is a net win over a non-looped MOB + exit-gate design at equal parameters.
- **Is routing specialization mechanistically real or a performance artifact?** [[routing-mechanisms-in-modular-networks]] flags that [[expert-choice-routing]]'s claim is performance-inferred only; [[mixture-of-cognitive-reasoners-micro]]'s r=0.7 is correlational, not mechanistic. Whether specialization is what we think it is remains unverified.
- **What dispatch-signal scope is needed for block-level specialization to emerge?** Local-to-global axis in [[routing-mechanisms-in-modular-networks]] is unexamined experimentally.
- **How do Ouro's gate curriculum and MICRO's router curriculum compose?** No source in the wiki combines them. Ordering, shared stages, cross-interference all unknown.

## Open research questions to prioritize

Ranked by how load-bearing the answer is for this architecture.

1. **Curriculum-free specialization ablation.** Train MOB without MICRO Stage 1 pseudo-labels; measure specialization via localizer + routing entropy. Directly tests whether seeding is necessary. [[mixture-of-cognitive-reasoners-micro]] has not run this; [[learned-routing-specialization]] identifies it as the single cleanest resolution experiment. Outcome determines whether the architecture is end-to-end trainable.
2. **Loop × router × exit-gate interaction.** Does the router condition on loop step? Does the exit gate see router decisions? Does a token specialized at t=1 get re-dispatched at t=2? None of Ouro / MICRO / MoD compose all three. This is the largest synthesis gap in the wiki.
3. **Variable-loop-count training and extrapolation.** [[looped-transformers-and-reasoning]] flags inference-time scaling via variable loops as a "very promising future direction"; [[looped-language-models]] flags extrapolation beyond T_max as open. The exit gate is meaningless if the model cannot generalize across loop counts.
4. **KV cache architecture for looped-routed models.** [[looped-language-models]] flags no-cross-step-reuse as a hard deployment barrier. A routed-looped model compounds this: router decisions may invalidate cache even within a single step.
5. **Heterogeneous expert types under learned routing.** Does learned routing across {attention, SSM, MLP} experts recover the [[mamba-2-and-ssm-hybrids]] ~8/43/50 ratio? Or collapse? Tests whether the fixed-routing hybrid recipe is a plateau or a lower bound that learned routing can beat.
6. **Mechanistic specialization probes.** Probing classifiers on expert hidden states + causal swap ablations. [[learned-routing-specialization]] §What-would-resolve-this identifies this as a generic gap. Would settle the conflict and validate or falsify specialization claims broadly.
7. **Routing quality metrics.** [[modular-deep-learning-survey]] §9.1 flags the absence of standardized specialization metrics. Defining a measurable specialization metric is a prerequisite for expensive comparison sweeps.

## Source

This page is a cross-source synthesis; it has no primary source. Components are drawn from:

- `raw/research/thesis-foundations/04-universal-transformers.md` — Universal Transformer (loop + ACT precursor)
- `raw/research/thesis-foundations/05-latent-thoughts-looped.md` — Middle-looping structural variant
- `raw/research/thesis-foundations/06-ouro-looped-lm.md` — Ouro weight-shared recurrence + two-stage exit gate
- `raw/research/thesis-foundations/10-neuro-cognitive-reasoners.md` — MICRO MOB + three-stage curriculum
- `raw/research/thesis-foundations/02-mixture-of-depths.md` — Causal top-k predictor
- `raw/research/thesis-foundations/01-expert-choice-routing.md` — Expert-choice framing
- `raw/research/thesis-foundations/03-block-operations.md` — Soft-vs-hard routing and block-granularity routing
- `raw/research/thesis-foundations/07-mamba2-ssd.md` / `08-mamba-empirical-8b.md` — Heterogeneous block-type ratios (fixed routing)
- `raw/research/thesis-foundations/09-modular-deep-learning-survey.md` — Routing taxonomy + learned-routing failure modes

## Related

- [[universal-transformer]]
- [[looped-transformers-and-reasoning]]
- [[looped-language-models]]
- [[mixture-of-cognitive-reasoners-micro]]
- [[expert-choice-routing]]
- [[mixture-of-depths]]
- [[block-operations-and-modular-routing]]
- [[mamba-2-and-ssm-hybrids]]
- [[modular-deep-learning-survey]]
- [[routing-mechanisms-in-modular-networks]]
- [[brain-inspired-modularity]]
- [[learned-routing-specialization]] (open conflict — blocks Component 2 design)
- [[looped-vs-depth-scaling]] (open conflict — blocks Component 1 parameter-efficiency claim)
