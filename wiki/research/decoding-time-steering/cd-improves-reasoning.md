---
name: cd-improves-reasoning
description: Contrastive Decoding Improves Reasoning in Large Language Models. O'Brien & Lewis (2023) adapt the CD framework (Li et al. 2022) to chain-of-thought reasoning, showing that subtracting a small same-family amateur's logits from a large expert's logits — with an α-mask and β-scaled penalty — is training-free, costs ~3.25% extra FLOPs, and pushes LLaMA-65B past GPT-3.5 and PaLM-540B on GSM8K. The mid-training-checkpoint ablation operationalises CD as amplifying late-training skill increments.
type: research
---

# Contrastive Decoding Improves Reasoning in Large Language Models

O'Brien & Lewis (Meta AI / UCSD, arXiv 2309.09117, submitted ICLR 2024) demonstrate that [[contrastive-decoding]] — originally proposed for open-ended generation quality by Li et al. (2022) — transfers directly to chain-of-thought reasoning with large gains and minimal overhead. The key finding is that subtracting a small same-family amateur model's logits from a large expert's logits at each decoding step suppresses surface-copying and abstract reasoning errors while adding only ~3.25% FLOPs (1.5B amateur vs. 65B expert). A re-parameterised $(\alpha, \beta)$ formulation clarifies the method, and a mid-training-checkpoint ablation reveals that CD is mechanistically a first-order optimisation step that accentuates skills the expert has acquired late in training and the amateur has not yet learned.

## Source

- arXiv: 2309.09117
- Raw markdown: `../../../raw/research/decoding-time-steering/01-02-cd-improves-reasoning.md`

## Method

Let $s^{(e)}_i$ and $s^{(a)}_i$ be the unnormalised logits for token $i$ from the expert and amateur respectively. Two steps per decoding position:

**1. Compute the $\alpha$-mask** — restrict the valid vocabulary to tokens the expert considers plausible:

$$V_\text{valid} = \bigl\{j : s^{(e)}_j \geq \log\alpha + \max_k\, s^{(e)}_k\bigr\}$$

**2. Form the CD score** — linearly combine expert and amateur logits, hard-masking the rest:

$$s^{(\text{CD})}_i = \begin{cases}(1+\beta)\,s^{(e)}_i - \beta\,s^{(a)}_i & i \in V_\text{valid} \\ -\infty & i \notin V_\text{valid}\end{cases}$$

The leading $(1+\beta)$ coefficient decouples sampling temperature from the contrastive strength $\beta$, matching the [[dexperts]] objective. The probabilistic form is $p^{(\text{CD})}_i \propto p^{(e)}_i\,(p^{(e)}_i/p^{(a)}_i)^\beta$: as $\beta \to 0$ this reduces to greedy expert decoding; as $\beta \to \infty$ it collapses to $\arg\max_i\, p^{(e)}_i/p^{(a)}_i$.

Default hyperparameters: $\alpha = 0.1$, $\beta = 0.5$; results are fairly insensitive to $\alpha$ for $\beta < 1$. PyTorch implementation is three lines.

## Claims

- LLaMA-65B + CD ($\beta = 0.25$) scores **57.7** on GSM8K, outperforming LLaMA-2 (56.8), GPT-3.5 (57.1, 5-shot), and PaLM-540B (56.5).
- CD lifts LLaMA-30B on GSM8K by **+8.1 pp** (35.3 → 43.4 at $\beta = 0.5$); consistent gains across all model sizes 7B–65B.
- HellaSwag contrastive ranking: LLaMA-65B reaches **88.0**, outperforming LLaMA-2 (85.3), GPT-3.5 (85.5), PaLM-2-L (86.8); only GPT-4 exceeds it.
- Error analysis on 100 GSM8K examples: CD reduces missing-step errors (22% → 20%) and semantic errors (24% → 21%); arithmetic errors slightly increase (4% → 8%), net errors 54% → 52%.
- CD systematically reduces token-level copying from the prompt (measured by n-gram precision/recall on 26k sampled generations); generation lengths are essentially unchanged.
- **MATH is not improved** (65B: 10.6 → 10.3, $-0.3$). CD cannot help when the expert lacks the skill entirely — it is an amplifier, not an installer.
- CD **degrades factual recall**: TriviaQA $-2.1$ pp, OpenBookQA $-2.4$ pp. The contrastive objective is calibrated for reasoning, not verbatim retrieval.
- **Amateur size matters critically**: a 7B amateur *hurts* GSM8K performance; 1.5B helps. Too large an amateur shrinks $V_\text{valid}$ below the solution region.
- **Mid-training checkpoints outperform fully-trained small amateurs**: LLaMA-7B at 10% and 23% through training works as a better amateur than the finished 7B checkpoint. CD interpreted as a first-order optimisation step accentuating late-training skill acquisition.
- FLOP overhead: $1.5/65.2 \approx 2.30\%$ per forward pass, plus a small generation-length overhead → **~3.25% total**. Substantially more FLOP-efficient than self-consistency at matched accuracy.
- CD requires chain-of-thought prompting; without CoT it provides no consistent improvement (task too hard for any contrastive gap to exploit).
- CD generalises beyond LLaMA: FLAN-T5-XXL (11B) expert + FLAN-T5-Small (80M) amateur gives a small GSM8K lift (16.4 → 17.4).

## Strengths / Novelty

- First systematic application of CD to chain-of-thought reasoning, establishing it as a general-purpose decoding improvement.
- Cleaner $(\alpha, \beta)$ re-parameterisation than Li et al. 2022: decouples sampling temperature from contrastive strength, three-line PyTorch implementation.
- Mid-training-checkpoint ablation gives a mechanistic, operational account of *what CD amplifies*: exactly the skills acquired late in training that the amateur has not yet internalised.
- FLOP efficiency argument is quantified; comparison to self-consistency is direct and favourable.
- $\alpha$-masking ablation ($\beta = 0$, $\alpha = 0.1$) shows that the mask alone does not drive self-consistency gains — the contrastive objective is the active ingredient.

## Weaknesses / Limits

- **Same-family amateur required**: the method relies on shared tokenisation and architecture. Cross-family CD is unexplored and likely requires special handling.
- **LLaMA-1 only** for main results; behaviour on RLHF-tuned or instruction-tuned models unknown and potentially different.
- **MATH ceiling**: CD fails on problems beyond the expert's capability. No amount of contrastive amplification installs absent knowledge.
- **Factual recall degrades**: the same mechanism that suppresses surface-copying also suppresses high-confidence memorised facts. Using the same setup for retrieval tasks requires a different $\beta$ regime.
- **Two forward passes per token**: latency doubles relative to single-model greedy decoding (mitigated but not eliminated by the small amateur).
- Amateur weights at 10–23% through training are not publicly released, limiting reproducibility for the mid-checkpoint result.

## Relevance to this wiki's project

CD is the most direct empirical demonstration of $R_w$ — the reasoning-skill reward signal — in the math/reasoning regime. Three connections are load-bearing:

1. **Amplifier, not installer.** MATH failure mirrors the BOLT coverage-wall finding ($\beta \log(1/\pi^*(S_N|x))$ saturation): decoding-time amplification cannot recover skills outside the expert's support. A single-sample fine-tuning method faces the same ceiling — it must *install* the concept, not merely amplify a weak signal.

2. **$\alpha$-mask as hard support constraint.** The empirical value of $\alpha$-masking aligns with the Rethinking-RL 0%-shifted finding: tokens the expert assigns near-zero probability are masked out unconditionally, providing harder support regularisation than a soft $\beta$ penalty alone. This supports hard-masking below an expert's $\alpha$ threshold as a design choice.

3. **Invisible Leash C.1 — amateur size.** Too-large an amateur (7B) *hurts* performance. The CD penalty must not shrink $V_\text{valid}$ below the solution region. Analogously, in the self-play / teacher-student setting, the "amateur" component (weak model or early checkpoint) must not over-constrain the expert's generation space.

The mid-training-checkpoint finding also operationalises late-training skill increments as recoverable post-hoc by logit subtraction — a conceptual anchor for thinking about what single-sample fine-tuning does at the representation level.

## Connections to the wiki

- [[contrastive-decoding]] — parent method (Li et al. 2022); this paper is a direct reasoning-domain extension; must cross-link.
- [[dola]] — layer-contrastive sibling: contrasts later vs. earlier layers within a single model rather than two separate models.
- [[dexperts]] — same logit-combination objective; O'Brien & Lewis use the expert as both base and steering model.
- [[cfg-lm]], [[gedi]], [[fudge]], [[pplm]], [[repe]], [[iti]], [[actadd]], [[caa]] — decoding-time steering family; CD sits at the logit-arithmetic end of this spectrum.
- [[linear-rep-hypothesis]] — provides mechanistic grounding for why logit arithmetic over model families works.
- [[../synthesis/proposed-method]] — $R_w$ amplification framing; CD is the decoding-time analogue.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — 0%-shifted token finding; $\alpha$-mask is a hard-threshold implementation of the same insight.
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] — BOLT KL ceiling; CD's MATH failure is the decoding-time mirror of BOLT's coverage wall.
- [[../self-play/invisible-leash]] — C.1 ruling: too-large amateur shrinks support below solution region.
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — amplification vs. installation distinction; CD exemplifies amplification.

## Related

- [[contrastive-decoding]] (Li et al. 2022 — parent method)
- [[dola]] (layer-contrastive sibling)
- [[cfg-lm]]
- [[dexperts]]
- [[gedi]]
- [[fudge]]
- [[pplm]]
- [[repe]]
- [[iti]]
- [[actadd]]
- [[caa]]
- [[linear-rep-hypothesis]]
- [[../synthesis/proposed-method]]
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]]
- [[../self-play/invisible-leash]]
- [[../single-sample-rl-finetuning/1-shot-rlvr]]
