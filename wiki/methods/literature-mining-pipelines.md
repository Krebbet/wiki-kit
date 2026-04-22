# Literature-Mining Pipelines

The recipe for turning the substrates in [[literature-mining-substrates]] into structured triples that can populate the ingredient graph in [[ingredient-data-structures]]. This is the *how* behind [[priority-improvements]] item 3 (the LLM literature-mining layer). The substrate question is answered elsewhere; this page is about the pipeline architecture, what works, what doesn't, and the honest performance numbers from the three existence proofs in the literature.

## The canonical six-stage shape

Every pipeline in the nine-source research pass follows a small number of common stages. Not every pipeline uses every stage, but the ordering is stable:

1. **Retrieval** — pull candidate sentences or documents from a substrate. LitSense API queries against PMC+PubMed, keyword search against Europe PMC, IPC-filtered pulls from PatentsView, or direct scraping of recipe sites.
2. **Filtering / tagging** — coarse relevance filter to cut noise before the expensive extraction model runs. FoodAtlas used a fine-tuned BioBERT classifier with a p > 0.9 threshold to drop sentences that are topically off. FooDis tagged sentences as "Fact / Analysis" vs. "Objective / Hypothesis / Methodology" and dropped the latter to avoid false positives on untested claims.
3. **Extraction** — the named-entity-recognition (NER) plus relation-extraction (RE) step. The model class varies widely (see below) and is where most of the performance-quality trade-off sits.
4. **Linking / normalisation** — ground extracted entities to canonical IDs (NCBI Taxonomy, PubChem, ChEBI, MeSH, FoodOn, UMLS, Disease Ontology). Without this, extracted triples are worth an order of magnitude less — you can't deduplicate, merge, or cross-reference.
5. **Ratification** — human-in-the-loop validation of a subset, both to measure precision and (critically) to supply training signal for the next active-learning round.
6. **Active learning** — choose which candidate sentences to annotate next using the extraction model's own uncertainty or entailment scores, so each new batch of annotator effort disproportionately grows the model's competence.

The third leverage point (the active loop) is what moves a pipeline from a one-shot dump to a compounding asset. FoodAtlas's active-learning strategy identified positive training examples **38.2% faster** than random sampling, ten rounds deep.

## The three existence proofs

### FoodAtlas v1 (Youn et al., Sci. Rep. 2024)

The fullest worked example in the corpus. 155,260 papers → **3,596,755 premise-hypothesis pairs** → **230,848 food–chemical composition relationships** extracted, **46% novel** to every prior database (FooDB, Phenol-Explorer, USDA FDC, Frida, DietRx).

- **Substrate:** PMC+PubMed via NCBI LitSense.
- **Retrieval pattern:** query `{food name} contains` for 1,959 taxonomy-grounded foods.
- **Extraction model:** BioBERT fine-tuned on food-specific entailment. Frames "does food X contain chemical Y?" as a textual-entailment binary classification over premise-hypothesis pairs. **Precision 82.0%, recall 79.2%, F1 77.2%** on held-out test; **calibration R² = 0.94** between predicted probability and empirical positive rate. 88.6% of triples scoring ≥ 0.9 are correct.
- **Schema:** four relations (*contains*, *hasPart*, *isA*, *hasChild*) over three entity types (food, food-part, chemical). Foods grounded to NCBI Taxonomy IDs; chemicals to PubChem; chemical ontology via MeSH tree overlay; food hierarchy via NCBI Taxonomy. Every triple carries a PMID or PMCID — provenance is first-class.
- **HITL:** two independent annotators per sentence, consensus-only retention, 4,120 pairs total across ten active-learning rounds. Separate validation team manually checked 443 link-prediction predictions via Google Scholar, confirming 355 novel relationships.
- **Link prediction over the extracted KG:** RotatE embeddings achieved **F1 73.5%** on a held-out evaluation; **calibration R² = 0.99**. The KG is self-completing — it doesn't just catalogue what was extracted, it surfaces plausible missing edges for the next ratification round. GPT-3.5 (text-davinci-003) zero-shot on the same link-prediction task scored only F1 42.7%; graph-embedding models outperformed transformer-based KG completions.
- **Final KG:** 285,077 triples — 1.5% high-quality (cited + expert-validated), 92.8% medium-quality (cited but not expert-validated), 5.7% low-quality (no citation). The three-tier credibility banding is a pattern worth stealing.

### FoodAtlas v2 (npj Sci. Food 2025)

Same team, one year later, three changes worth attending to.

- **Extraction model swap:** dropped the BioBERT entailment head in favour of **fine-tuned GPT-3.5-turbo-0125**. Per-sentence F1 dropped from **0.772 → 0.67** — but the new model could extract quantitative structured tuples `(food, food part, chemical, concentration)` rather than just binary contains / doesn't-contain. One-shot GPT-4 on the same task scored only F1 0.42; **fine-tuning beats zero-shot GPT-4** by a wide margin. The design trade: ~18 F1 points per sentence for ~10× edge density and richer schema.
- **Schema expansion:** v2 integrates CTD (chemical–disease), ChEMBL (bioactivity), FlavorDB (flavour descriptors), and PubChem HSDB. Final KG has **96,981 edges** over 1,430 foods × 3,610 chemicals × 2,181 diseases × 958 flavours. A downstream bioactivity-prediction model trained on the KG achieves **R² = 0.52 / Pearson ρ = 0.72** on held-out FRAP antioxidant assay data for 159 foods.
- **What this shows:** the KG is not just an end product — it's a feature store for downstream predictive models. The v2 substitution framework evaluated 14,580 disease-focused meal swaps and predicted **mean 11.9% disease-risk reduction** (all p < 10⁻³). The *design lesson*: plan the downstream-model feature schema backwards from the substitution or formulation objective; don't treat the KG as end-of-pipeline.

### FooDis / FoodChem / ChemDis (Cenikj et al., Sci. Rep. 2023)

Three linked pipelines running on PubMed *abstracts* (not full text). ~43,000 abstracts across two use cases (cardiovascular disease; milk).

- **NER choice:** the authors tried corpus-trained models (BuTTER, FoodNER) for food NER and **abandoned them** due to domain shift — BERT / BiLSTM models trained on *recipe text* did not generalise to *scientific abstracts*. Reverted to **dictionary-based matching against UMLS** (36,836 food entities). This is the single most-cited methodological finding for food NER: **training-text domain matters more than model architecture.**
- **Relation extraction:** SAFFRON ensemble — BioBERT and RoBERTa fine-tuned on CrowdTruth and FoodDisease datasets, plus a voting mechanism: ≥ 3/4 models must agree on "cause" (with ≤ 1/4 voting "treat") to prevent polarity conflicts.
- **Polarity:** binary cause / treat. No quantitative dose-response. This creates a whole category of false positives — ChemDis reported "carbohydrates treat cardiomyopathy" from a sentence actually saying *reduced* carbohydrate intake is therapeutic.
- **Precision:** **~70% mean** across pipelines, 65–79% per relation type. **No recall number is reported** — coverage of true relations in the corpus is untested. This is a common omission worth flagging in any food-mining pipeline: precision on extracted triples is much easier to measure than recall against the underlying corpus.
- **Key finding on evidence-count calibration:** precision approaches 1.0 when a relation is supported by 3+ independent sentences. "Supporting-sentence count" is a cheap, model-free confidence signal — keep it in the schema, don't compress it to a single per-edge probability.

## The extraction-model question

Four model classes have been used for food-literature relation extraction across these sources:

- **Dictionary-based NER + rules.** UMLS food dictionary, FoodIE, drNER, StandFood. Pragmatic but brittle; partial-entity-match errors are the single biggest cost ("sodium" extracted from "sodium-glucose co-transporter"). Food-semantic-web review and FooDis both name partial-extraction as the top error class.
- **Fine-tuned BERT / BioBERT / RoBERTa.** FoodAtlas v1 (entailment), FooDis (RE via SAFFRON voting), BuTTER (BiLSTM+CRF, recipe-trained). Strong when training text matches target text; collapses under domain shift. Fast inference (~10–50 ms per document).
- **Fine-tuned GPT-3.5.** FoodAtlas v2. Enables structured-tuple output (`(food, part, chemical, concentration)`) that BERT-class classifiers don't support. F1 trade is real but the schema change is the reason to do it. Latency 200–500 ms per document on GPU; training data budget ~1,780 manually-labelled sentences with dual annotation.
- **Zero-shot / few-shot GPT-4.** Benchmarked in both FoodAtlas v2 (F1 0.42 vs. 0.67 for fine-tuned GPT-3.5) and the food-semantic-web review. Worse than fine-tuned BERT or fine-tuned GPT-3.5 on food NER and especially on entity *linking* to canonical IDs. Good for cold-start prototyping, not for production extraction.

**Pattern across the corpus:** **fine-tuning on domain text beats architecture choice**. A fine-tuned 110M-parameter BERT on in-domain annotated sentences routinely beats zero-shot frontier-scale LLMs on food RE. The lesson is that annotator effort on a few thousand gold sentences compounds faster than model-scale increases.

### The FoodSky question — is a domain-specialist LLM the extraction model?

FoodSky is the only domain-pretrained food LLM in the corpus — fine-tuned Chinese LLaMA-2 and Qwen 2.5 on 811K instructions (FoodEarth corpus, 2.5B tokens). It scores 83.3% on Chinese Chef Exams and 91.2% on Dietetic Exams (zero-shot), beating GPT-4o (78.5%) on food-specific tasks.

It is **not** a per-sentence relation extractor in the FoodAtlas / FooDis sense. The authors don't claim triple extraction; they claim reasoning, regulatory QA, and recipe understanding. The likely position in a pipeline is at **stages 5–6** (ratification and active-learning prompt-selection) rather than stage 3 (extraction):

- **As a ratification assistant** — score whether a FoodAtlas-extracted triple is consistent with the retrieved passage. Higher recall than pure human review, higher precision than unaided BERT.
- **As a topic-aware filter** upstream of extraction — TS3M-style topic indicators could pre-filter for domain relevance before the expensive extraction model runs. This is closer to stage 2 (filtering) than stage 3.
- **As a retrieval-augmented reasoner** — HTRAG-style retrieval over food encyclopedias and regulatory databases at inference time. Useful when the downstream question is "is this extracted edge consistent with FoodOn / FooDB / USDA FDC?" — the kind of cross-source reconciliation that pure classifiers don't do.

The trade-off is cost: FoodSky-Qw-7B needed ~80 GPU-hours and 640 GB memory to train. An extraction-only pipeline can reach FoodAtlas-level performance on one or two orders of magnitude less compute.

A pragmatic pipeline architecture: **BERT (or similar) at stage 3 for recall, FoodSky-class model at stages 2 and 5 for filtering and ratification**.

## Patents as a distinct pipeline track

Every biomedical-literature pipeline above assumes sentence-level extraction from continuous prose. Patents break that assumption and need a different recipe. The WIPO handbook chapter gives it:

1. **Classification-first filtering.** Start from the IPC hierarchy — A23 (foods / beverages) with subclasses A23L / A23C / A23G / A23P / A23Q — to cut the 7.8M-patent USPTO corpus to something like 10K–100K food-relevant patents before any text processing runs. "An important principle when working with data at scale is to identify the process for reducing scale to human manageable levels as soon as is practical."
2. **Dictionary-driven extraction.** Seed a 100–200-term food-specific ingredient / process dictionary; filter patents containing dictionary terms. This is the pragmatic-extraction pattern that FooDis used for food NER over scientific abstracts, transferred to patents.
3. **Hyphen-aware tokenisation.** Default tokenisers split `2,4-dichloro-...` and `modified-food-starch-E1404` on every hyphen, destroying the entities. Use a chemistry-aware tokeniser (LeadMine is the standard) or customise the rule.
4. **Custom stop-words.** Patent prose is inflated with *thereof*, *comprising*, *consisting of*, *said* — extend the SMART / Snowball / ONIX stop lists with a patent-specific layer before TF-IDF or n-gram analysis.
5. **Bigram / trigram feature extraction.** Single tokens aren't enough — "soy protein", "high-shear mixing", "extrusion cooking" live as multi-word units. Apply TF-IDF to n-grams, not just unigrams.
6. **Co-occurrence networks over curated vocabulary.** Pearson correlation or pointwise mutual information between dictionary terms, visualised as igraph / ggraph networks. This is how technology-cluster discovery happens ("clean label" co-occurs with "natural flavours", "plant-based" with "pea protein isolate").
7. **Time-series extraction.** Graph term-frequency trajectories across filing years to detect emerging / declining technologies. Useful as a source of leading-indicator ingredients for the formulation pipeline.

The Akhondi chemical-patent corpus is the annotation-methodology template for going beyond retrieval into structured-triple extraction from patents — see [[literature-mining-substrates]] for schema design inheritance.

## Active learning as the compounding layer

FoodAtlas is the only pipeline in the corpus that reports active-learning numbers directly. The headline:

- **Maximum-likelihood sampling** identified all 1,899 positive training sentences **38.2% faster** than random sampling, over ten rounds.
- **Maximum-entropy sampling** (query-by-committee on model uncertainty): 10.7% faster.
- **Stratified sampling** (balance across entity types / sections): 9.3% faster.

The pragmatic implication: **the selection strategy dominates the annotator-effort return curve**. A small team that writes well-calibrated confidence scores into the pipeline will out-compound a larger team that doesn't. Every ratification round is an opportunity to concentrate effort on the sentences the model is *most uncertain* about, not the ones it's most confident about.

## Validation and benchmarking

Each pipeline in the corpus defines its own benchmark. There is **no standard food-literature-mining benchmark** — this is the cross-cutting observation of the field. What the existing benchmarks actually measure:

- **FoodAtlas v1**: 840-pair held-out test set for entailment (P / R / F1 / AUROC / AUPRC / calibration R²); 443 RotatE predictions manually validated (P / R / F1); novelty comparison against FoodMine, FooDB, Phenol-Explorer, FDC, Frida, DietRx.
- **FoodAtlas v2**: 356-sentence held-out test set for extraction F1; FRAP-assay comparison for the downstream bioactivity model; literature-qualitative validation of substitution recommendations.
- **FooDis / FoodChem / ChemDis**: precision-only, two case studies (9,984 CVD-related + 33,111 milk-related PubMed abstracts); domain-expert annotation by one cardiologist and two food-science specialists; no recall.
- **FoodSky**: CDE-12K (1,278 multiple-choice questions), FoodLongConv (22 essays with BLEU/ROUGE/GLEU), FoodQA (GPT-4-as-judge scoring). Explicitly a reasoning benchmark, not an extraction one.

What a team building the Tier-1 pipeline item should plan to measure, even in absence of a standard:

- **Extraction P / R / F1** on a 500-1000-sentence held-out set, dual-annotated for consensus.
- **Calibration** (R² or ECE between confidence score and empirical positive rate).
- **Entity-linking accuracy** separately from extraction accuracy — the food-semantic-web review finds this is where GPT-3.5 / GPT-4 fall off fastest.
- **Novelty against FooDB / USDA FDC / FoodAtlas v2** — can you demonstrate triples not already in public KGs?
- **Downstream-task lift** — if the KG is meant to support substitution or flavour prediction, measure the improvement in the downstream task against a no-KG baseline. This is how FoodAtlas v2's bioactivity R² works as a validation signal.

## Known failure modes

Consolidated across the corpus:

- **Partial entity extraction** (FooDis): "sodium" extracted from "sodium-glucose co-transporter". Highest-frequency food-NER error.
- **Quantitative / directional sign errors** (FooDis): "carbohydrates treat cardiomyopathy" from a *reduced-carbohydrate* sentence. Binary polarity loses quantitative information and flips signs.
- **Dense-sentence relation conflation** (FooDis): when a single sentence contains multiple entities and relations, RE models conflate co-occurrence with actual relation. More aggressive sentence-boundary and dependency-parsing pre-processing helps.
- **Table / figure / supplementary-file blindness** (FoodAtlas): quantitative composition data sits there, and LitSense / PubMed full-text search doesn't reach it.
- **Processed-foods vocabulary gap** (food-semantic-web review): the ontology layer can't ground what it doesn't name. Extraction failures here are really grounding failures.
- **Cultural / geographic bias** (food-semantic-web review): English-language, Western-food skew. Extraction models trained on such data generalise poorly to dishes and ingredients outside the training distribution.
- **Domain-shift from recipe text to scientific abstracts** (FooDis, FoodAtlas): BERT-class models trained on recipes fail on primary literature, and vice versa. **Train on the target text type.**

## Practical pipeline for [[priority-improvements]] item 3

A pragmatic starting shape, based on the corpus:

1. **Choose one ingredient class first.** Alternative fats is a good candidate — a tight ~100-paper PMC+Europe-PMC corpus, FooDB has decent coverage of the relevant lipid chemistry, and the substitution use case in [[ingredient-substitution]] is natural.
2. **Reuse FoodAtlas's substrate.** LitSense API for retrieval. Don't reinvent substrate access before first-pass extraction is working.
3. **Start with a fine-tuned BERT extractor** rather than jumping to GPT-3.5 fine-tuning. Lower cost, tighter iteration, and the F1 advantage is real. Gate on whether the schema can be binary / entity-level; only move to GPT if you need structured-tuple output with quantitative fields.
4. **Budget ~4,000 annotated sentences total** for the extractor, spread across 5–10 active-learning rounds. Dual annotation, consensus-only retention. This is the FoodAtlas shape and it works.
5. **Link to NCBI Taxonomy + PubChem + ChEBI + FoodOn from day one.** Don't defer grounding — unlinked triples are much harder to retrofit later.
6. **Carry per-edge provenance** (PMID/PMCID, supporting-sentence span, supporting-sentence count, model confidence, ratification state) through the whole pipeline. The credibility-tiering (high / medium / low) from FoodAtlas v1 is a cheap, high-leverage design choice.
7. **Run RotatE (or similar graph-embedding) link prediction** once the extracted KG passes ~10K edges. Use it to surface the next round's candidate validation pool — the 443-prediction FoodAtlas example confirmed 355 true novel relationships.
8. **Measure downstream-task lift.** A pilot substitution query on alternative fats, comparing pre-KG and post-KG candidate rankings against historical team decisions, is the right integration test. See [[priority-improvements]]'s evaluation-strategy section.

The LLM literature-mining layer is an execute-able Tier-1 item given this substrate and this pipeline shape. The remaining risk is scope — "LLM literature-mining layer" is a direction, not a bounded project; pick one ingredient class and one downstream query before opening the broader infrastructure work.

## Source

- `raw/research/llm-literature-mining-corpora/01-foodatlas-pipeline-2024.md` — six-stage pipeline, BioBERT entailment, active-learning numbers, RotatE link prediction, three-tier credibility schema.
- `raw/research/llm-literature-mining-corpora/02-foodatlas-expansion-npjscifood-2025.md` — fine-tuned GPT-3.5 extraction, schema expansion, downstream bioactivity model, substitution evaluation.
- `raw/research/llm-literature-mining-corpora/03-lm-to-food-biomed-kg-scirep-2023.md` — SAFFRON voting RE, ~70% precision, polarity-sign failure modes, domain-shift lesson.
- `raw/research/llm-literature-mining-corpora/04-food-semantic-web-review-arxiv-2025.md` — extraction-method evolution (rule-based → BERT → LLM), entity-linking weakness of LLMs, failure modes.
- `raw/research/llm-literature-mining-corpora/05-kg-food-science-review-pmc.md` — construction-recipe taxonomy (ontology → extraction → integration → refinement), industrial-KG pattern.
- `raw/research/llm-literature-mining-corpora/07-foodsky-llm-2025.md` — domain-LLM positioning (ratification / reasoning, not extraction), data-quality-over-volume finding, cost numbers.
- `raw/research/llm-literature-mining-corpora/08-wipo-patent-analytics-ch7-textmining.md` — patent-mining workflow, IPC-first filtering, tidytext stack, hyphen tokenisation.
- `raw/research/llm-literature-mining-corpora/09-annotated-chemical-patent-corpus-plosone.md` — multi-group annotation + centroid voting, entity-type F-score variance, LeadMine / BRAT tool stack.

## Related

- [[literature-mining-substrates]]
- [[ingredient-data-structures]]
- [[genai-leverage-points]]
- [[priority-improvements]]
- [[datasets-and-databases]]
- [[open-gaps]]
- [[human-in-the-loop]]
