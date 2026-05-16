---
tags: [selective-finetuning, alignment, data-efficiency, superficial-alignment]
paper: "LIMA: Less Is More for Alignment"
authors: "Zhou et al."
venue: NeurIPS 2023
arxiv: "2305.11206"
---

# LIMA: Less Is More for Alignment

Zhou et al. (Meta AI / CMU / USC, NeurIPS 2023) fine-tune LLaMA 65B on exactly **1,000 hand-curated examples** — no RLHF, no preference modelling, standard cross-entropy SFT — and produce a model that beats RLHF-trained DaVinci003 in head-to-head human preference trials. The paper's organizing thesis, the **Superficial Alignment Hypothesis**, states it plainly: almost all knowledge is acquired during pretraining; instruction-tuning teaches only the surface format for how to expose that knowledge to users. This is the format/substance separation that underlies the present wiki's research programme, here stated as a paper's headline empirical claim.

## Source

- arXiv: 2305.11206
- Raw: `../../../raw/research/selective-finetuning/03-08-lima.md`

## Method

**Superficial Alignment Hypothesis (§2).** A model's knowledge and capabilities are learned almost entirely during pretraining; alignment teaches it which subdistribution of *formats* to use when interacting with users. If format is the only thing being learned, a small, high-quality, stylistically consistent dataset suffices.

**Dataset construction (Table 1).** 1,000 prompt–response pairs, ~750k tokens total:

| Source | $n$ | Character |
|---|---|---|
| Stack Exchange STEM | 200 | quality + diversity filters; auto-mined |
| Stack Exchange Other | 200 | same pipeline |
| wikiHow | 200 | title as prompt; article as response |
| r/WritingPrompts | 150 | manually curated creative responses |
| Super-Natural Instructions | 50 | one example per NLG task |
| Hand-authored (Group A) | 200 | uniform assistant tone; manually written |

Curation rules: minimum 1200 chars, no first-person, no cross-answer references, no links or images; a *uniform response style* is enforced across all outputs. Diversity is in the prompts; consistency is in the responses.

**Training.** Standard SFT on LLaMA 65B. AdamW ($\beta_1=0.9$, $\beta_2=0.95$, weight decay $0.1$), lr $10^{-5}$ decaying linearly to $10^{-6}$, batch 32, 15 epochs, max 2048 tokens. One non-standard detail: residual dropout rising linearly from $p_d=0.0$ at the bottom layer to $p_d=0.3$ at the top (following InstructGPT). Checkpoint selected on 50-example dev set by human preference, not perplexity — perplexity negatively correlates with generation quality (Appendix B).

No RLHF, no DPO, no reward model.

## Claims

- **1,000 examples suffice.** LIMA outperforms Alpaca 65B trained on 52,000 examples in human preference trials (§4.2).
- **Beats RLHF without RLHF.** Human raters prefer LIMA over DaVinci003 (RLHF-trained), 65% vs. 35%. Against Bard: LIMA preferred or tied 58% of cases. Against GPT-4: LIMA preferred or tied 43% of cases (Figure 1).
- **Absolute quality.** Manual analysis of 50 responses: 50% rated Excellent, 38% Pass, 12% Fail (§4.3, Figure 3).
- **Out-of-distribution generalization.** On 13 test prompts with no training analogue: 45% Excellent, 35% Pass, 20% Fail — similar to in-distribution performance (§4.3).
- **Quantity alone does not scale.** Ablation on 7B: doubling training set size (up to 16× in exponential sweeps) from filtered Stack Exchange does not improve ChatGPT-graded quality (Figure 6).
- **Quality beats quantity.** Unfiltered Stack Exchange vs. filtered: ~0.5 Likert-point gap (Figure 5).
- **Diversity beats homogeneity.** Diverse Stack Exchange >> homogeneous wikiHow at equal $n$ and quality (Figure 5).
- **30 examples unlock multi-turn dialogue.** Zero-shot LIMA fails multi-turn in 6/10 conversations within 3 turns; adding 30 dialogue chains raises Excellent turn rate from 45% to 76%, failures from 15/42 turns to 1/46 (§6, Figure 7).
- **6 examples unlock structured output.** Adding 6 formatting-constraint examples enables complex structured responses (marketing plans, bullet summaries) not seen in training (Appendix E, Figure 13).

## Strengths

- Cleanest empirical demonstration of the format/substance separation. The gap between LIMA and Alpaca 65B (52× more data) directly isolates curation quality from quantity.
- The 30-example multi-turn and 6-example format-constraint results are the sharpest data points: capability already exists in the pretrained model; a handful of examples is sufficient signal to invoke it.
- Human evaluation methodology is rigorous: crowd workers plus GPT-4 replication, inter-annotator agreement 78–82%, with tie-discounted scoring.
- Ablation design (diversity vs. quality vs. quantity, independently controlled) is cleaner than most alignment papers.

## Weaknesses

- Results are for LLaMA 65B; the hypothesis may weaken for smaller models where pretraining coverage is thinner (preliminary 7B experiments needed 2,000 examples for stability, not 1,000 — footnote 5).
- No RLHF means robustness is lower: adversarial prompts or decoding unlucky samples more often produce weak outputs (§7).
- Safety coverage is thin — only 13 adversarial training examples; 20% unsafe response rate on implicit malicious-intent test prompts (§4.3).
- Curation is laborious and hard to scale; manual effort is explicitly called out as a limitation (§7). The paper does not solve the curation bottleneck, it just tightens how little curation is needed.
- The hypothesis is stated as an empirical finding, not proven mechanistically. LIMA does not identify *where* or *how* format is encoded separately from knowledge.

## Relevance to this wiki's project

LIMA is the Superficial Alignment Hypothesis stated as an experimental result: **knowledge lives in pretraining weights; SFT is a surface patch that teaches format**. This is exactly $R_w$'s premise in [[../synthesis/proposed-method]] — that a reward signal can be injected at the formatting layer without perturbing the underlying knowledge representation. LIMA provides the empirical license for that architectural bet.

The format/substance separation also directly answers the anchoring question: *can new data signal be added without degrading response style?* LIMA argues style is *isolable* — a shallow distribution over output tokens, learned from a few consistent examples — and that substance is orthogonal, encoded in parameters shaped by pretraining. Injecting new factual or concept signal at the wrong layer risks coupling the two; targeting the right layer (format-vs-knowledge localization) is the practical challenge.

The multi-turn (30 examples) and format-constraint (6 examples) ablations show that a pretrained model already carries latent capabilities; surface supervision merely *routes* generation into the right subdistribution. That routing is cheap. Making the routing *concept-selective* — so that format tokens remain stable when a single new concept example is added — is the open problem this wiki addresses.

## Connections to the wiki

- [[skill-localization]] — empirical mechanism for LIMA's claim: ~0.01% of parameters carry the skill. If knowledge is localized, style can be updated without touching it.
- [[surgical-finetuning]] — operationalizes the layer choice implied by LIMA: which layers to target for format vs. substance.
- [[pit]] — LIMA's success story runs in the opposite direction from PIT's failure mode: PIT shows that instruction-tuned models forget; LIMA shows that 1,000 examples of *consistent* format do not degrade pretrained knowledge. The asymmetry matters.
- [[rome]], [[memit]], [[alphaedit]], [[mend]], [[knowledge-neurons]], [[ff-kv-memories]] — mechanistic evidence that knowledge is stored in localized, editable structures, consistent with LIMA's "knowledge from pretraining" thesis. These provide the surgical tools; LIMA provides the motivation.
- [[knowledge-editing-survey]] — broader map of the localization literature.
- [[o-lora]], [[dora]], [[packnet]], [[hat]] — parameter-efficient or subnetwork approaches that presuppose format/substance separability; LIMA is the empirical license they implicitly rely on.
- [[../synthesis/proposed-method]] — $R_w$ premise is LIMA's Superficial Alignment Hypothesis applied to single-concept injection.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — REASONMAXXER's 0%-shifted-outside-base-top-5 result is LIMA's hypothesis at the token-probability level: format tokens stay within the pretrained distribution even after RL.
- [[../self-play/invisible-leash]] — Theorem C.1 formalizes LIMA: self-play optimizes within a leash around the pretrained policy, which bounds format drift.
- [[../single-sample-rl-finetuning/_overview]] — LIMA at 1,000 examples is the most-aligned full-corpus single-sample-flavor result; the gap to 1 example is the open research space.
- [[../decoding-time-steering/_overview]] — the entire decoding-time-steering theme is the LIMA claim without any training: if format is a shallow routing, it can be steered at inference time without SFT at all.

## Related

- [[skill-localization]]
- [[surgical-finetuning]]
- [[pit]]
- [[rome]]
- [[memit]]
- [[alphaedit]]
- [[mend]]
- [[knowledge-neurons]]
- [[ff-kv-memories]]
- [[o-lora]]
- [[dora]]
- [[packnet]]
- [[hat]]
- [[knowledge-editing-survey]]
- [[../synthesis/proposed-method]]
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[../self-play/invisible-leash]]
- [[../single-sample-rl-finetuning/_overview]]
- [[../decoding-time-steering/_overview]]
