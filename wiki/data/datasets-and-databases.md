# Datasets and Databases

Catalogue of public (and notable proprietary) datasets the corpus cites for training and evaluating food-formulation models. A good starting place when planning what data the expanded method needs and where to get it.

## Composition and nutrient tables

- **USDA FoodData Central** — the default nutritional reference. Macronutrient-focused; the Future of Food arXiv paper notes it has "limited chemical depth" compared to research databases.
- **FAO/INFOODS** — international food composition database, broader geographic coverage than USDA.
- **Periodic Table of Food Initiative (PTFI)** — an emerging global effort to catalogue foods at molecular resolution; positioned as an eventual successor to composition-only tables. Mentioned as in-progress.

## Chemical and flavour libraries

- **FoodAtlas v1** (Youn et al., Sci. Rep. 2024) — **230,848** food–chemical composition relationships automatically extracted from **155,260** scientific papers via BioBERT entailment over NCBI LitSense retrieval. **46% novel** to every prior public database. Every triple carries a PMID/PMCID; three-tier credibility banding (high / medium / low by evidence weight). See [[literature-mining-pipelines]] for the architecture.
- **FoodAtlas v2** (npj Sci. Food 2025) — successor KG: **1,430 foods × 3,610 chemicals × 2,181 diseases × 958 flavours**, **96,981 edges**. Fine-tuned GPT-3.5 extractor for structured-tuple output `(food, part, chemical, concentration)`. Integrates FooDB, USDA FDC, CTD (chemical–disease), ChEMBL (bioactivity), FlavorDB, PubChem HSDB. Open at github.com/IBPA/FoodAtlas-KGv2.
- **FooDB** — **~28,000 chemicals** across **~1,000 raw/unprocessed foods**. Open-access. Notable caveat flagged repeatedly across the literature-mining corpus: **<1% of associations carry literature citations** — exactly the provenance gap FoodAtlas was built to fill.
- **CTD (Comparative Toxicogenomics Database)** — curated chemical–gene, chemical–disease, gene–disease relations from biomedical literature. Free for non-commercial; commercial use requires licence. Integrated into FoodAtlas v2.
- **ChEMBL** — bioactivity data with pChEMBL potency values; the substrate behind FoodAtlas v2's 15,222 chemical–bioactivity mappings. Open.
- **Phenol-Explorer** — polyphenol-specific database.
- **LipidBank** — lipid-specific database.
- **FlavorDB** — curated flavour molecules and their sources.
- **Volatile Compounds in Food database** — aroma-active compounds.

## Knowledge graphs and ontologies

- **FoodOn** — the most-cited food ontology across the literature-mining corpus. Good fit for raw ingredients and supply-chain relationships (*has-ingredient*, *has-part*, *derives-from*); weak on **processed foods and culinary transformations**.
- **FoodKG** (2019) — Recipe1M+ ingredients linked to USDA, FoodOn, and FooDB. Entity-linking precision improved from ~41% to ~76% after student-verified update + FooDB integration. SPARQL-queryable.
- **FoodOntoMap** — cross-ontology alignment layer over 22,000 AllRecipes recipes, normalising ingredients across FoodOn, OntoFood, SNOMED CT, and Hansard Corpus.
- **AGROVOC** — FAO agricultural vocabulary, **39,500 concepts / 924,000 terms in 41 languages**. Upstream of food; FoodOn reuses its terms.
- **SNOMED-CT food subset** — clinical terminology; strong on allergens and intolerances, weak on compositional semantics.
- **LanguaL / FoodEx2** — food-description systems. EFSA's FoodEx2 is the common hook for European-regulatory-facing systems.
- **Industrial KGs** — Uber Eats, Edamam, Meituan, Yummly maintain proprietary food KGs. Feasibility proof; not accessible. See Min et al. 2022 review for the landscape.

See [[literature-mining-substrates]] for the full audit of which resources are usable as grounding targets in a mining pipeline.

## Recipes, pairings, and sensory

- **Recipe1M+** — >1 million recipes with paired food images; used for cross-modal embedding (recipes ↔ images).
- **FlavorGraph** — food-chemical graph built from 1M recipes and ~1,500 flavour molecules; embeddings predict ingredient pairings. A common input for graph neural network candidate-generation work.
- **Flavor Network** — ingredient-pairing graph constructed from shared volatile compounds.
- **Principal Odor Map** — not a dataset per se but a trained GNN organising odorants by perceptual similarity, with a reported human-level accuracy on unseen compounds (Lee et al., cited in Oz et al. and the arXiv consortium paper).
- **Food.com** recipe-review corpus — used for consumer-language training.

## Industrial / proprietary

- **NotCo** — internal corpus behind Giuseppe (flavour pairings, ingredient embeddings, sensory feedback loops). Not public.
- **Brightseed (Forager)** — internal corpus of ~700,000 phytochemicals analysed for bioactivity; sourced the N-trans-caffeoyltyramine discovery.
- **Foodpairing** — proprietary ingredient-pairing database used by Knorr (Unilever) for flavour-compatibility discovery.

## What's missing

The corpus is consistent that the data gap is not composition data but **multimodal, labelled datasets linking formulation → processing → rheology → sensory → nutrition**. Kuhl writes: "labeled and structured data linking formulation to rheology, texture, and flavor are rare." Oz et al. and the consortium paper both call out that sensory panels cannot scale to deep-learning data volumes; bioavailability and digestibility datasets are underdeveloped; and industrial in-line process logs are proprietary and inconsistent in metadata. See [[open-gaps]] for the wider gap inventory.

**Culturally diverse sensory data** is a specific gap named by multiple sources — most existing sensory corpora are Western.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — flavorDB, odorDB, LCA region-boundness, sensory-data gaps
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — Recipe1M+, FlavorGraph, Principal Odor Map, Phenol-Explorer, LipidBank, public-versus-industrial data split
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — FoodAtlas (230K / 46% coverage stat), Periodic Table of Food Initiative
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — ChefFusion (1M recipes / 900K images), proprietary-data bottleneck
- `raw/research/llm-literature-mining-corpora/01-foodatlas-pipeline-2024.md` — FoodAtlas v1 architecture and credibility tiers
- `raw/research/llm-literature-mining-corpora/02-foodatlas-expansion-npjscifood-2025.md` — FoodAtlas v2 entity and edge counts; CTD/ChEMBL/FlavorDB integration
- `raw/research/llm-literature-mining-corpora/04-food-semantic-web-review-arxiv-2025.md` — FoodKG, FoodOntoMap, FoodOn, SNOMED-CT characterisation
- `raw/research/llm-literature-mining-corpora/05-kg-food-science-review-pmc.md` — industrial-KG landscape, AGROVOC scale

## Related

- [[literature-mining-substrates]]
- [[literature-mining-pipelines]]
- [[ingredient-data-structures]]
- [[predictive-models]]
- [[genai-leverage-points]]
- [[open-gaps]]
- [[industry-examples]]
