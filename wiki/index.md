# Wiki Index

Catalog of all pages in this wiki. Updated on every ingest.

Domain: design of a computational food-formulation system — extending a GA + predictive-model pipeline with richer food-science knowledge and GenAI leverage.

---

## Overview

### Landscape (start here)

| Page | Summary |
|---|---|
| [[field-overview]] | Orientation page: where computational food formulation sits in 2025, how the user's GA + predictive-model method fits, and a recommended reading order. |
| [[priority-improvements]] | Consolidated prioritisation of the extensions the method pages propose — ordered by leverage ÷ build-cost, with deferred items and an evaluation strategy. *(synthesis)* |
| [[industry-examples]] | Named companies, platforms, and deployed systems — NotCo, Brightseed, Climax, Perfect Day, Plant Jammer, PIPA, Ajinomatrix, and others. |
| [[open-gaps]] | Where the field agrees it is weak: data, generalisation, bioavailability, explainability, cultural diversity, benchmarks, preference elicitation. |

### Workflow

| Page | Summary |
|---|---|
| [[npd-process]] | Stage-gate NPD and the Wageningen Chain Information Model (CIM) — the organisational baseline the method sits inside. |
| [[human-in-the-loop]] | Where human judgement stays vs. where AI replaces elicitation; interface patterns across the corpus. |

### Methods

| Page | Summary |
|---|---|
| [[candidate-generation]] | Taxonomy of candidate-generation methods (manual, GA, BO, RL, generative, GNN, LLM, ontology), their search spaces and fit conditions. |
| [[ga-in-context]] | Where genetic algorithms sit in the recent literature, when to extend vs. replace, proposed hybrid architecture. |
| [[multi-objective-optimization]] | Why formulation is inherently MOO, Pareto-aware methods, hard-vs-soft constraints, preference elicitation gaps. |
| [[ingredient-substitution]] | The "cheaper peanut-oil replacement" problem class — five-axis match, data requirements, methods, gaps. |
| [[predictive-models]] | Property-prediction models by domain (texture/rheology, flavour/aroma, nutrition, fermentation, sensory), accuracy claims, limits. |
| [[inverse-design]] | Target property → formulation framing, VAE/GAN/diffusion approaches, optimisation-over-surrogate route. |
| [[genai-leverage-points]] | Concrete LLM and generative-AI entry points — literature mining, substitution proposal, feedback translation, copilots, agentic loops. |
| [[literature-mining-pipelines]] | The six-stage extraction recipe (retrieve → filter → extract → link → ratify → active-learn), case studies (FoodAtlas v1/v2, FooDis), validation numbers, tool stack. |

### Food science (reference)

| Page | Summary |
|---|---|
| [[rheology-and-texture]] | Rheology quantities (E, η, Y, G', G", δ), TPA, sensory vs. physical texture, hot/cold break. |
| [[ingredient-functionality]] | Functional roles — gluten, casein, hydrocolloids, emulsifiers, oleosomes, fibres — and processing effects on functionality. |
| [[bioavailability-and-matrix-effects]] | Bioavailability, digestibility, matrix effects, S-Pro² principle, antinutrients, lycopene/glucosinolate mechanisms. |
| [[food-classification-schemes]] | IUFoST formulation-vs-processing scheme and its critique of NOVA; NRF9.3, ΔNRF9.3, FPFIN. |

### Data

| Page | Summary |
|---|---|
| [[datasets-and-databases]] | Public and notable proprietary datasets — USDA, FAO/INFOODS, FoodAtlas v1/v2, FoodKG, FoodOntoMap, FooDB, CTD, ChEMBL, FoodOn, AGROVOC, Recipe1M+, Principal Odor Map, PTFI, and others. |
| [[ingredient-data-structures]] | Heterogeneous graph representations, role taxonomies, similarity measures, ingredient records. |
| [[literature-mining-substrates]] | Audit of the corpora an LLM extraction pipeline can actually use — PMC / Europe PMC / Agricola / patents / recipe corpora / composition DBs — with access, licensing, and coverage-gap assessment. |

---
