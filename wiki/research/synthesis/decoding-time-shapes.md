---
name: decoding-time-shapes
description: Cross-method synthesis tabulating 13 decoding-time and activation-steering mechanisms by intervention point, data floor, access required, mechanism formula, and what each implies for the R_w hypothesis. Companion to proposer-reward-shapes for the new decoding-time-steering theme.
type: research
---

# Decoding-time shapes — cross-method synthesis

Companion synthesis page to [[proposer-reward-shapes]]. Where that page tabulates ten proposer-reward shapes from the self-play family, this page tabulates the **thirteen decoding-time / activation-steering mechanisms** captured 2026-05-13 by intervention point, data floor, access required, mechanism formula, and what each implies for [[proposed-method]]'s **R_w extension** ("offline logit-reweighting prior put the model into the right solution space").

The unifying empirical finding across all 13: **the relevant information is already in the base model**; an offline reweighting prior — logit-space or activation-space — suffices to put the model into the right solution space without weight updates. This was unsurfaceable when the watchlist entry was seeded 2026-05-12; the 13-paper sweep makes it concrete.

## Mechanism table

Methods grouped by intervention point. Mechanism formulas reflect the captured paper's notation; see per-page entries for full derivation.

| Method | Intervention | Mechanism (key formula) | Data floor | Access required | R_w implication |
|---|---|---|---|---|---|
| **Logit-level reweighting** | | | | | |
| [[../decoding-time-steering/pplm]] | KV cache | $\Delta H_t \mathrel{+}= \alpha \nabla_{\Delta H_t}\log p(a\|H_t + \Delta H_t)$, $m$ backward passes/token | BoW or 1-layer classifier ($\sim$1K params) | Gradient access to base | Historical ancestor: established "tiny classifier guides large LM at decode time" pattern |
| [[../decoding-time-steering/gedi]] | Next-token logits | $P_w(x_t \| x_{<t}, c) \propto P_\text{LM}(x_t \| x_{<t}) \cdot P_\theta(c \| x_t, x_{<t})^\omega$ | CC-LM on attribute labels | Logit access | Bayes-rule prior; parametric realisation of ICL-Bayesian update |
| [[../decoding-time-steering/fudge]] | Next-token logits | $P(x_i \| x_{1:i-1}, a) \propto P(a \| x_{1:i}) \cdot P(x_i \| x_{1:i-1})$ | Future-discriminator on $10^7$ generations | Logit access | Token-level process-reward analogue; bridges PRM literature to decoding |
| [[../decoding-time-steering/dexperts]] | Next-token logits | $\tilde{P}(X_t) = \text{softmax}(\mathbf{z}_t + \alpha(\mathbf{z}^+_t - \mathbf{z}^-_t))$ | $\sim$650 in-domain examples | Logit / top-100 API | Product-of-experts; anti-expert direction enables *steer-away*; nucleus truncation = decoding-time support-inclusion |
| [[../decoding-time-steering/contrastive-decoding]] | Next-token logits | $\log p_\text{EXP} - \log p_\text{AMA}$ on $V_\text{head}$ plausibility set | Two frozen LMs (same family) | Logit access | Pragmatic-listener interpretation; $V_\text{head}$ = support-inclusion constraint at decode time |
| [[../decoding-time-steering/cd-improves-reasoning]] | Next-token logits | $s^{(\text{CD})}_i = (1+\beta)s^{(e)}_i - \beta s^{(a)}_i$ | Same family + 1.5B amateur | Logit access | Math/reasoning regime; mid-training-checkpoint amateurs operationalise "skill increment" |
| [[../decoding-time-steering/dola]] | Next-token logits | $\hat{p}(x_t) \propto \log\frac{q_N(x_t)}{q_M(x_t)}$ on $V_\text{head}$; $M$ chosen by max JSD | **Zero training** | Layer-wise logit access (single model) | **Single-model** layer-contrast — no auxiliary; cleanest "info is intrinsic" demonstration |
| [[../decoding-time-steering/cfg-lm]] | Next-token logits | $\log\tilde{P}(w \| c) = \log P(w) + \gamma(\log P(w \| c) - \log P(w))$ | **Zero training** | Two forward passes | Structural parallel to BOLT Boltzmann tilt; prompt-direction acts as reward |
| **Activation-level steering** | | | | | |
| [[../decoding-time-steering/actadd]] | Residual stream | $\mathbf{h}^{[l]} \mathrel{+}= c \cdot (\mathbf{h}_+^{[l]} - \mathbf{h}_-^{[l]})$ | **2 prompts** (single pair) | White-box activations | Floor existence proof: single pair = causally effective steering direction |
| [[../decoding-time-steering/caa]] | Residual stream | $v_\text{MD} = \frac{1}{\|D\|}\sum (a_L(p, c_p) - a_L(p, c_n))$; $\mathbf{h}^{[L]} \mathrel{+}= \alpha v_\text{MD}$ | Hundreds of A/B contrast pairs | White-box activations | Base-to-chat transfer: directions exist pre-training, survive RLHF |
| [[../decoding-time-steering/iti]] | Attention head outputs | $x_{l+1} \mathrel{+}= \alpha\sigma_l^h \theta_l^h$ on top-$K$ probe-selected heads | $\sim$40–81 contrast pairs | White-box; head outputs | **40% probe–generation gap** = direct quantitative evidence model "knows but doesn't say" |
| [[../decoding-time-steering/repe]] | Residual stream | LAT PCA on contrast pairs → reading vector $v$; control: $R' = R \pm v$ / piecewise / projection-erasure / LoRRA | 5–128 contrast pairs | White-box activations | Umbrella framework: 4-experiment evaluation protocol; concept-reading beats prompting on 5 QA benchmarks |
| **Theory** | | | | | |
| [[../decoding-time-steering/linear-rep-hypothesis]] | Formal | Theorem 2.5: $\lambda \mathrel{+}= c \bar\lambda_W \Rightarrow P(W=1)\uparrow$, all causally-separable $Z$ unchanged | n/a | n/a | Formal warrant: concept = cone direction defined by counterfactual pairs; Theorem 3.2 unifies probing (reading) and steering (control) via causal inner product |

## Three structural patterns

**Subtract-an-amateur (logit, two-model):** [[../decoding-time-steering/pplm]] → [[../decoding-time-steering/gedi]] → [[../decoding-time-steering/dexperts]] → [[../decoding-time-steering/contrastive-decoding]] → [[../decoding-time-steering/cd-improves-reasoning]]. Lineage of replacing the *form* of the auxiliary model — gradient classifier → Bayes-rule CC-LM → anti-expert PoE → small contrast LM — while preserving the *shape* (logit-additive prior from a weaker model). Each step trades expressiveness for efficiency.

**Self-contrast (logit, one-model):** [[../decoding-time-steering/dola]] (layer contrast within one model) + [[../decoding-time-steering/cfg-lm]] (conditional-vs-unconditional contrast within one model). The same model provides both signals; no auxiliary needed. **Strongest "info is intrinsic" evidence** — the contrast lives entirely inside the network's existing forward pass.

**Direction-from-contrast-pairs (activation):** [[../decoding-time-steering/actadd]] ($n=1$) → [[../decoding-time-steering/caa]] (averaged $n$) → [[../decoding-time-steering/iti]] (head-selective + linear probe) → [[../decoding-time-steering/repe]] (umbrella + LoRRA). Same primitive (mean-difference of paired activations); progressively more principled extraction and evaluation. [[../decoding-time-steering/linear-rep-hypothesis]] is the formal explanation of why this primitive works at all.

## Bayesian-vs-Boltzmann correspondence

A useful structural mapping ties this theme to two existing wiki anchors:

| Mathematical form | Decoding-time instance | RLVR / training-time analogue |
|---|---|---|
| Multiplicative posterior $\propto$ prior $\cdot$ likelihood$^{\,\omega}$ | [[../decoding-time-steering/gedi]] $P_w \propto P_\text{LM} \cdot P_\theta(c)^\omega$ | [[../in-context-learning-theory/icl-bayesian-inference]] posterior over latent concepts |
| Logit-additive reweighting | [[../decoding-time-steering/dexperts]] $\mathbf{z} + \alpha(\mathbf{z}^+ - \mathbf{z}^-)$ | [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] $\pi^* \propto \pi_\text{ref}\exp(r/\beta)$ |
| Reference-anchored extrapolation | [[../decoding-time-steering/cfg-lm]] $\log P(w\|c) + \gamma(\log P(w\|c) - \log P(w))$ | BOLT iterative refresh (Theorem 11; $K$ rounds = effective $\beta/K$ sharpening) |
| Contrast within model | [[../decoding-time-steering/dola]] late − early layer; [[../decoding-time-steering/contrastive-decoding]] expert − amateur | [[../rlvr-mechanics/rethinking-rl-sparse-selection]] token-level 1.0–4.1% rerank within base top-5 |
| Direction addition (activation) | [[../decoding-time-steering/actadd]], [[../decoding-time-steering/iti]], [[../decoding-time-steering/caa]], [[../decoding-time-steering/repe]] | [[../concept-learning/concept-bottleneck-models]] test-time intervention; [[../concept-learning/recursive-concept-evolution]] low-rank subspace edits |

In every row, the decoding-time / training-time pair lands on the *same target distribution* up to coverage and refresh schedule. The training-time path moves probability mass via gradient updates; the decoding-time path composes it in at output time. **For concepts already in base support, the two paths are interchangeable.** This is the core mechanistic claim of the R_w extension.

## Plugging into the wiki's existing components

For each component in [[proposed-method]], a decoding-time analogue:

| Component | Training-time form | Decoding-time analogue |
|---|---|---|
| **R** (RLT reward, dense per-token) | $r^{SS} - \lambda r^{KL}$ | [[../decoding-time-steering/fudge]] future-discriminator scoring partial sequences |
| **C** (reference-in-context) | textbook in teacher's prompt | [[../decoding-time-steering/cfg-lm]] negative-prompt as anti-conditioning |
| **C_w** (parametric SFT on reference) | one-shot weighted SFT | [[../decoding-time-steering/dexperts]] anti-expert from in-domain text (also: [[../decoding-time-steering/gedi]] CC-LM) |
| **R_w** (offline logit-reweight prior) | — (newly proposed) | This entire theme — primary anchors: [[../decoding-time-steering/iti]], [[../decoding-time-steering/repe]], [[../decoding-time-steering/dola]], [[../decoding-time-steering/cd-improves-reasoning]], [[../decoding-time-steering/cfg-lm]] |
| **V** (MDL sibling test) | $\Delta DL(\text{siblings}) < 0$ gate | [[../decoding-time-steering/repe]] termination experiment (random control should *not* recover the intervention) |
| **G** (diversity injection) | group size $G > 1$ in GRPO | [[../decoding-time-steering/cfg-lm]] at low $\gamma$ preserves diversity while raising signal; high $\gamma$ collapses pass@$k$ — same trade-off |
| **L** (format-fluency guard) | KL leash + EWC + mask + Dr-GRPO + DAPO Overlong + MCPO hinge-KL + ptx | [[../decoding-time-steering/contrastive-decoding]] $V_\text{head}$ plausibility constraint = decoding-time analogue of the format leash |

## Open cross-source questions

These came up in multiple per-paper summaries and are not resolved by any single capture:

1. **Single-pair sufficiency for non-toy concepts.** [[../decoding-time-steering/actadd]] works at $n=1$ for sentiment / toxicity / "love-vs-hate". Does the same hold for procedural concepts (e.g. modular multiplication, calculus chain rule)? [[../decoding-time-steering/caa]] uses hundreds of pairs and explicitly warns about single-pair noise; no captured paper bridges the gap.
2. **Composition of subtract-amateur with self-contrast.** Does [[../decoding-time-steering/contrastive-decoding]] compose with [[../decoding-time-steering/dola]] — i.e. simultaneously contrast across models *and* across layers? Both are logit-additive; no captured paper tests the composition.
3. **Mid-training-checkpoint amateurs.** [[../decoding-time-steering/cd-improves-reasoning]] §3.3 finds 10–23%-trained checkpoints work better as amateurs than fully-trained small models. Implies skill increments are linearly extractable. Does this generalise beyond reasoning to concept-level skills? Speculative R_w-initialisation recipe.
4. **Base-to-chat direction transfer.** [[../decoding-time-steering/caa]] §8.3 shows base-model directions transfer to RLHF chat models for the 7 alignment dimensions tested. Does this hold for concepts learned only during RLHF (not pre-existing in base)?
5. **Single counterfactual pair under Park's framework.** [[../decoding-time-steering/linear-rep-hypothesis]] doesn't address the $n=1$ limit. The LOO-mean estimator may not be reliable for one pair; empirically ActAdd succeeds, formally not established.
6. **Cross-paper consistency on the support-inclusion claim.** All 13 papers agree that intervention stays within base support. [[../decoding-time-steering/cd-improves-reasoning]] also shows that too-large amateur (7B vs 1.5B) HURTS performance — penalty must not *shrink* the support below the solution region. Open: what's the right amateur scale / probe selectivity / coefficient $c$ for a given task?

## Related

- [[proposed-method]] — R_w extension; this theme is the empirical/theoretical backbone
- [[proposer-reward-shapes]] — sibling synthesis page (proposer-reward family)
- [[../decoding-time-steering/_overview]] — theme overview
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] — Boltzmann-tilt structural parallel
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — token-level 0%-shifted finding; decoding-time analogue
- [[../self-play/invisible-leash]] — Theorem C.1 support inclusion; holds by construction here
- [[../concept-learning/_overview]] — concept-as-direction lineage
- [[../in-context-learning-theory/icl-bayesian-inference]] — Bayesian posterior framing

## Source

Editorial cross-source synthesis from the 13 captured papers in `raw/research/decoding-time-steering/` and their per-page wiki entries. Each row of every table traces back to its named per-paper page; the unanimity claim, the three-structural-pattern grouping, and the Bayesian-vs-Boltzmann correspondence are this page's editorial framings, not direct extractions from any single source.
