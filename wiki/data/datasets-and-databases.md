# Datasets and Databases

Catalogue of public (and notable proprietary) datasets the corpus cites for training and evaluating food-formulation models. A good starting place when planning what data the expanded method needs and where to get it.

## Composition and nutrient tables

- **USDA FoodData Central** — the default nutritional reference. Macronutrient-focused; the Future of Food arXiv paper notes it has "limited chemical depth" compared to research databases.
- **FAO/INFOODS** — international food composition database, broader geographic coverage than USDA.
- **Periodic Table of Food Initiative (PTFI)** — an emerging global effort to catalogue foods at molecular resolution; positioned as an eventual successor to composition-only tables. Mentioned as in-progress.

## Chemical and flavour libraries

- **FoodAtlas** (Youn et al., 2024) — **230,848** food–chemical composition relationships automatically extracted from **155,260** scientific papers. Of the 230K compound entries, ~46% had never appeared in any prior database. Biggest single advance in public-domain food chemistry coverage cited in the corpus.
- **Phenol-Explorer** — polyphenol-specific database.
- **LipidBank** — lipid-specific database.
- **FlavorDB** — curated flavour molecules and their sources.
- **Volatile Compounds in Food database** — aroma-active compounds.

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

## Related

- [[ingredient-data-structures]]
- [[predictive-models]]
- [[genai-leverage-points]]
- [[open-gaps]]
- [[industry-examples]]
