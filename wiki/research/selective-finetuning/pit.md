---
title: "Instruction-tuned LMs are Better Knowledge Learners (PIT)"
aliases: ["PIT", "Pre-Instruction-Tuning", "pit"]
tags: [selective-finetuning, continued-pretraining, instruction-tuning, catastrophic-forgetting, knowledge-injection]
year: 2024
authors: [Jiang, Sun, Shi, Rodriguez, Zhou, Neubig, Lin, Yih, Iyer]
url: "https://arxiv.org/abs/2402.12847"
---

# Instruction-tuned LMs are Better Knowledge Learners (PIT)

The standard recipe for injecting new knowledge into an LLM — continued pre-training (CPT) on new documents, then instruction-tune on QA pairs — leaves most knowledge inaccessible: even after perplexity on the training documents reaches 1, only ~30% of related questions are answered correctly. The problem is a surface-form mismatch. Documents weave facts into prose; QA pairs expose isolated, labelled facts. Pre-Instruction-Tuning (PIT) inverts the standard order — **instruction-tune on QA first, then CPT on documents** — so the model already "knows how knowledge is accessed" before it encodes new facts from complex text. This is the direct answer to the question of adding new data signal without degrading response format: format is established before the new knowledge is absorbed, not patched on afterward.

## Source

Jiang, Sun, Shi, Rodriguez, Zhou, Neubig, Lin, Yih, Iyer. *Instruction-tuned Language Models are Better Knowledge Learners*. 2024. arXiv 2402.12847. FAIR / CMU / UW.

## Method

PIT is a three-stage training schedule applied before the target-document CPT step.

**Stage 0 — baseline for context.** Standard recipe: CPT on new documents → instruction-tune on QA. After exhaustive CPT (perplexity minimized to $\approx 1$), QA accuracy reaches only 27.6% (7B) / 41.7% (70B). Adding instruction-tuning lifts it to 30.3% / 46.4%. The authors call the residual gap the *perplexity curse*: low document perplexity does not imply accessible knowledge.

**Stage 1 — PIT warm-up (QA only).** Train exclusively on related QA pairs (not the target documents). The model learns the schema of knowledge access: what kinds of facts are worth attending to, how answers relate to questions. Even without seeing the new documents, this primes the encoder to treat factual entities as salient rather than incidental. Loss: $\mathcal{L}_a = -\sum_t \log P(a_t \mid q, a_{<t}) / |a|$.

**Stage 2 — joint CPT (QA + documents interleaved).** Train on a mix of the warm-up QA pairs together with the new documents. Having already learned access patterns, the model can use those patterns as a scaffold when encoding the dense document prose. The interleaved order (QA before the associated document within each cycle) outperforms grouped or reversed arrangements. Loss over documents: $\mathcal{L}_d = -\sum_t \log P(d_t \mid d_{<t}) / |d|$.

**Stage 3 — optional QA fine-tune (PIT++).** Add a final pass of QA-only fine-tuning after Stage 2. This is the best-performing variant (48.1% EM on 7B) but the gain over Stage 2 alone (45.4%) is modest — the ordering during Stage 2 already carries most of the benefit.

**Why order matters.** Ablations confirm that QA-after-doc ("instruction-tuning w/o train doc") is no better than the standard recipe (27.1% vs 30.3%). The same data, in the wrong order, yields no improvement. Positioning QA before its associated document during joint training outperforms QA-after in both grouped (+11.0 EM) and interleaved (+2.7 EM) arrangements. Format is not lost because it is anchored before any document exposure.

## Claims

All numbers from Llama-2 7B on Wiki2023-film-test (exact match) unless noted.

- Standard CPT + instruction-tune: 30.3% EM. PIT (Stage 2): 45.4% EM. Improvement: **+17.8 pp** (+58.7% relative) over standard recipe.
- PIT++ (three-stage, interleaved): **48.1% EM** on 7B; **62.7% EM** on 70B (vs 46.4% for standard recipe on 70B).
- Cross-domain transfer: PIT trained on non-film Wikipedia domains, evaluated on film: 36.9% EM (vs 23.6% for standard instruction-tuning) — generalises across domains.
- Perplexity curse confirmed: exhaustive CPT pushes document perplexity to 1 but QA accuracy plateaus at 27.6%. Low perplexity is necessary but not sufficient.
- Anti-alignment-tax control: adding target documents during the instruction-tune phase ("w/o forget" ablation) does not recover standard IT's deficit (30.2% EM) — forgetting is not the cause of the gap; the ordering mechanism is.
- Upweighting salient document tokens (à la answer-span reweighting) is also ineffective: 27.7% EM vs 27.6% baseline — PIT is not simply token salience.
- Generalisation to non-Wikipedia domain (synthetic bioS biographies): CPT 29.6% → PIT 58.1% EM; open-book ceiling is 95.2%.
- Real-user Google questions: standard IT 21.5%, PIT 29.0% EM.

## Strengths / Novelty

- **Surgical inversion of a ubiquitous recipe.** No architecture changes, no extra parameters. One scheduling decision — QA before docs — recovers roughly half the gap to open-book performance.
- **Mechanism isolates the cause.** The anti-forgetting control and token-weighting ablations rule out the two obvious alternative explanations. The residual gain really is from ordering.
- **Cross-domain and cross-corpus generalisation.** PIT-trained models improve knowledge absorption on held-out domains and non-Wikipedia sources, suggesting the effect is not about memorising the specific QA pairs used in Stage 1.
- **Dataset contribution.** Wiki2023 provides a clean contamination-controlled benchmark for continual knowledge acquisition; pre-training overlap is empirically bounded by the near-zero baseline accuracy (9.5%).

## Weaknesses

- **QA pairs must be available before documents.** In practice, generating QA pairs requires a capable LLM and adds pipeline cost. For truly novel or proprietary corpora this step may not be cheap.
- **Wikipedia-scoped evaluation.** Wiki2023 is well-structured, factually dense, and in-distribution for instruction-tuned models. Generalisation to web-crawl prose, code, or scientific tables is untested.
- **Closed-book focus only.** The paper does not evaluate whether PIT affects RAG or tool-augmented settings. The format-preservation benefit is demonstrated indirectly (models maintain QA format throughout) but not benchmarked against standard IT on generic instruction-following benchmarks.
- **No RL signal.** PIT is pure supervised fine-tuning. It establishes the format scaffold but does not train the model to verify or self-correct its own knowledge recall.
- **Scale limited to 7B/70B Llama-2.** Scaling laws for the PIT benefit are unknown; the ordering effect may shrink for larger models that already encode strong knowledge access priors.

## Relevance to This Wiki's Project

PIT is the closest existing paper to the $C_w^+$ recipe in [[../synthesis/proposed-method]]: chunked SFT on answer-structured examples before CPT on the raw context. The mechanism is the same — establish access schema before encoding knowledge — and the empirical gain (+17.8 pp EM) is large enough to be practically load-bearing.

For single-sample learning specifically: when the "document" is one long context window and the "QA pairs" are synthesised demonstrations or thinking traces, PIT predicts that running a short SFT pass on those demonstrations *before* the CPT step on the raw context will yield far better knowledge retention than the standard CPT-then-SFT order. This directly guides the training schedule for any approach that mixes RLVR signal with document-level CPT.

The format-preservation property is the other key connection: PIT shows that sequencing (QA first) is sufficient to prevent format collapse, without needing EWC penalties, replay buffers, or orthogonal-subspace projections. For a resource-constrained single-sample setting this is a significant practical advantage.

## Connections to the Wiki

**Within theme:**
- [[lima]] — 1000 high-quality examples preserve instruction-following format; PIT shows that the same format signal can also be used to *enable* new knowledge absorption, not just preserve existing format.
- [[surgical-finetuning]] — identifies which layers to update; PIT is complementary: which *order* to update determines what is preserved.
- [[skill-localization]] — skills are sparse and separable; PIT implicitly exploits this by training format-skill first, then knowledge-skill, without interference.
- [[rome]] / [[memit]] / [[alphaedit]] — locate-then-edit alternatives that modify weights directly at inference time; PIT achieves analogous knowledge injection at training time via ordering rather than surgical edits.
- [[mend]] / [[knowledge-neurons]] / [[ff-kv-memories]] — mechanistic understanding of where factual knowledge lives; PIT's success is consistent with format and knowledge residing in separable circuits.
- [[o-lora]] / [[dora]] / [[packnet]] / [[hat]] — orthogonal subspace / mask-based approaches to prevent task interference; PIT avoids interference via sequential staging rather than subspace constraints.
- [[knowledge-editing-survey]] — situates PIT as a training-time alternative to test-time editing methods.

**Cross-theme:**
- [[../synthesis/proposed-method]] — PIT is the closest precedent for the $C_w^+$ SFT-before-CPT extension of the $R_w / C_w$ framework.
- [[../single-sample-rl-finetuning/cbrl]] — annealed demonstration prepending is an ordering trick analogous to PIT's QA-first warm-up.
- [[../single-sample-rl-finetuning/reft]] — SFT warm-up before PPO; same staging principle as PIT applied to RL.
- [[../single-sample-rl-finetuning/deepseek-r1]] — cold-start long-CoT SFT before RL mirrors PIT's logic: establish a behaviour schema before the harder encoding phase.
- [[../teacher-student-rl/opsd-compresses-rlvr]] — SFT after RL degrades RL policy; PIT shows SFT *order* matters for knowledge too, suggesting the same asymmetry generalises across training objectives.
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — EWC is an alternative forgetting mitigation; PIT argues the standard recipe's failure is not primarily forgetting but surface-form mismatch, making ordering a cleaner fix than regularisation.

## Related

- Zhu & Li (2023) — original mixed biography/QA training finding that motivated PIT.
- Jang et al. (2022); Wang et al. (2021) — earlier small-LM evidence of the perplexity curse.
- Berglund et al. (2023) — *reversal curse*; PIT's perplexity curse is a conceptual sibling.
- Ouyang et al. (2022) — RLHF; alignment tax context for instruction-tuning order effects.
