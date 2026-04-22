# Literature-Mining Substrates

The corpora you would feed an LLM (or BERT-class) relation-extraction pipeline to populate the ingredient graph in [[ingredient-data-structures]]. The [[priority-improvements]] roadmap made source availability the stopper on item 3 (the LLM literature-mining layer). This page resolves it: the substrate exists, unevenly, and this is what's actually in it.

There are four substrate families: **biomedical literature**, **patents**, **recipe corpora**, and **composition / ontology databases**. Each has its own access model, licensing posture, and coverage gap. The right pipeline uses several of them — the FoodAtlas work is the existence proof (155,260 papers → 230,848 food–chemical relations; see [[literature-mining-pipelines]]).

## Biomedical literature

### PubMed Central (PMC) and PubMed

The backbone. FoodAtlas mined PMC via the NCBI LitSense API, which returns sentence-level matches to queries like `{food name} contains` and surfaces results from both PubMed abstracts and PMC open-access full text. Free, no authentication, public-domain US-government resource.

Size reference: the 2024 FoodAtlas run covered **155,260 papers** and generated **3,596,755 premise-hypothesis pairs**. The 2025 FoodAtlas v2 processed **125,723 filtered sentences** from PMC+PubMed after fuzzy-matching 1300 food names and discarding anything failing a BioBERT relevance classifier.

The hard limit: LitSense's NER and co-occurrence window miss information that lives in **tables, figures, and supplementary files** — where a lot of quantitative food composition data sits. Authors explicitly flag this.

### Europe PMC

The European mirror and enhancement layer over PMC, maintained by EMBL-EBI. **29 million abstracts** (all of PubMed plus ~600K Agricola records for agricultural literature, plus 4.2M patent abstracts from the European Patent Office, plus ~440K metadata-only records) and roughly **3 million full-text articles**, of which **~870K are open-access** (CC-BY, reusable for text-and-data mining). Numbers as of 2015; the OA subset "increases daily".

Access: REST API (JSON/XML, no explicit rate limit but docs recommend it over scraping for >few hundred records), bulk FTP (weekly XML dumps of the OA set, quarterly archives for citation), RSS feeds on saved searches, and a Whatizit-based text-mining engine that pre-extracts chemicals, genes, proteins, and GO/EFO terms — visible in the BioEntities API tab. You can also publish your own mined annotations back via the External Links service, viewable alongside articles within 24 hours of upload.

**Key caveat for food science:** "Paying an article processing charge (APC) and publishing in the Open Access track of a hybrid journal does not always result in the article being deposited in PMCi archives." Many premier food-science journals — *Food Chemistry*, *Food Hydrocolloids*, *Journal of Food Science*, *Trends in Food Science & Technology* — are Elsevier or other commercial-publisher venues with selective deposit. Europe PMC coverage of food-science primary literature is **uneven and publisher-dependent**. Verify each target venue individually.

### Agricola

~600K records, abstracts only, monthly-update cadence, accessed through Europe PMC. Covers agricultural / food / nutrition literature that never reaches PubMed. Valuable for the upstream side of the formulation corpus (raw-ingredient studies, agronomy) where PubMed thins out. Abstracts-only limits how much you can extract.

### Chinese-language biomedical literature

FoodSky (see [[literature-mining-pipelines]]) drew much of its 2.5B-token corpus from CNKI (the Chinese National Knowledge Infrastructure) and public accounts. CNKI is **not** open-access — FoodSky worked within authoritative-source licensing (CC-BY-SA 3.0 for academic sources, CC-BY-NC 3.0 for knowledge graphs) rather than mining the free web. A mirror issue to Elsevier on the English side: the literature exists, the access pipeline is commercial.

## Patents

The chapter-length treatment in [[literature-mining-pipelines]] argues that food-formulation patents contain structured ingredient + process descriptions at a granularity journal articles rarely match. The corpus doesn't yet exist as a curated dataset — you would build it.

### USPTO PatentsView

**7.8+ million granted US patents** with titles, abstracts, claims, and metadata in downloadable CSV tables. Free bulk download, no API rate limit for downloads, data pre-formatted for analysis rather than raw XML. Publication dates include US-only published applications from 2001 onward. Patent identifiers join cleanly with IPC classification tables — the entry point for food is class **A23** (foods and beverages) with subclasses A23L (foods / food preparation), A23C (dairy), A23G (cocoa / chocolate / confectionery), A23P (food shaping), and A23Q (nutrition / dietetics).

### EPO via Google Cloud Public Datasets

Full text of EPO patent documents available through Google Cloud. Paid / mixed tier — storage and compute costs apply even though the data itself is public. The WIPO chapter treats this as the standard route for European full-text coverage.

### Lens Patent API

Free-tier access plus paid plans. Cited in the WIPO chapter as the practical alternative to PatentsView for API-driven workflows.

### WIPO PatentScope

Searchable online but no bulk full-text export at the time of the chapter's writing. Useful for discovery, not for mining.

### Text-mining challenges specific to patents

Named explicitly in the WIPO chapter:
- **Formulaic stop-word inflation** — "thereof", "comprising", "consisting of", "method of apparatus" — standard stop lists miss these; custom lists needed.
- **Hyphenated chemical nomenclature** — "2,4-dichloro-..." must not be split on hyphens by the tokeniser. Food-relevant cases: additive names, modified-starch labels, enzyme EC numbers.
- **OCR noise** in older scans; the Akhondi chemical-patent corpus annotates OCR artefacts as a distinct entity class ("hydrobroml:c" for "hydrobromic") explicitly so they can be fed back into OCR correction models.
- **Scale** — full text plus claims is RAM-intensive; Apache Spark via Databricks or similar is the recommended scale-out, but titles + abstracts plus IPC filtering typically reduces the food-relevant working corpus to 10K–100K patents, which is tractable on a workstation.

### Licensing

Patents are public-domain for text-mining. PatentsView data are openly downloadable without license restriction. The EPO-via-Google-Cloud route inherits cloud-storage/compute costs but no IP restriction on analysis.

### The chemical-patent corpus as a methodology template

Akhondi et al.'s annotated chemical patent corpus (PLOS One, 2014) is not a food corpus, but it's the closest thing to a methodology template for building one. **200 patents** (121 USPTO, 66 WIPO, 13 EPO), stratified by protein target class; **47 harmonised** by 3+ annotator groups; **400,125 annotations** across 12 entity types including IUPAC, SMILES, InChI, CAS, trademarks, generics, diseases, targets, modes of action, plus an OCR-error class. Hosted at biosemantics.org under CC-BY. Tool stack: LeadMine for pre-annotation, BRAT for the UI, centroid-voting harmonisation.

Relevant F-score numbers for transfer planning: systematic names (IUPAC/SMILES/InChI) achieved **0.81–0.94** inter-annotator agreement; non-systematic names (trademarks, generics, abbreviations) **0.38–0.85**, highly variable; modes of action the worst at **0.17–0.67** due to boundary ambiguity ("mixed agonist" as one span or two). The lesson for a food-formulation analogue: expect high agreement on INCI / CAS / trade names, moderate on functional roles (emulsifier, gelling agent), low on health / application claims. Budget annotation effort accordingly.

## Recipe and pairing corpora

Covered more fully in [[datasets-and-databases]]; summarised here for their role as literature-mining substrates in their own right.

- **Recipe1M+** — 1M+ recipes with paired images. Foundational substrate for recipe-centric mining; the base that FoodKG (below) links against.
- **AllRecipes** — web-scraped, 22,000 recipes used for FoodOntoMap alignment. Scraping-provenance licensing caveat.
- **Yummly**, **Food.com** — used by industrial KGs (Edamam, Uber Eats) but public scraping is on thinner legal ground than the PMC / patents path.
- **Regional coverage bias** — essentially all high-volume recipe corpora skew Western. The food-semantic-web review flags **cultural / geographic bias** and **multilingual support** as the top two unmet needs. FoodSky's Chinese-recipe coverage is the counterexample; there's no equivalent public English-side corpus anchored outside the West.

## Composition and ontology databases

These aren't literature — they're the **grounding targets** a literature-mining pipeline links extracted mentions to. Without them, extracted triples float without canonical IDs.

- **USDA FoodData Central** — replaces the older SR; combines FNDDS (dietary studies), Foundation Foods, Branded Foods. Public. Macronutrient-focused; "limited chemical depth" (Future of Food arXiv paper).
- **FooDB** — **~28,000 chemicals** across **~1,000 raw/unprocessed foods**. Open-access. Key caveat repeatedly flagged across sources: **<1% of associations carry literature citations**. This is exactly what FoodAtlas was built to repair.
- **FoodKG** — Recipe1M+ ingredients linked to USDA, FoodOn, and FooDB. Entity-linking precision improved from ~41% (original) to ~76% (student-verified update) after integration of FooDB. Research-accessible via SPARQL; licensing unclear for commercial use.
- **FoodOntoMap** — cross-ontology alignment layer. 22K recipes, ingredients normalised across FoodOn, OntoFood, SNOMED CT, Hansard Corpus.
- **FoodAtlas v2 KG** — 1430 foods × 3610 chemicals × 2181 diseases × 958 flavors; 96,981 edges; MIT-compatible release at https://github.com/IBPA/FoodAtlas-KGv2. Includes CTD (for chemical–disease), ChEMBL (for bioactivity), FlavorDB, PubChem HSDB.
- **CTD (Comparative Toxicogenomics Database)** — chemical–gene, chemical–disease, gene–disease relations curated from literature. Free for non-commercial; commercial requires license. FoodAtlas v2 uses it directly and asks downstream users to re-download for compliance.
- **ChEMBL** — bioactivity data (pChEMBL values for 15,222 chemical–bioactivity mappings in FoodAtlas v2). Open.
- **FoodOn** — the most-cited food ontology across all nine sources of this research pass. Good fit for raw ingredients and supply-chain relationships; weak on **processed foods and culinary transformations**, which is a real gap for formulation work.
- **AGROVOC** — FAO vocabulary, **39,500 concepts / 924,000 terms in 41 languages**. Agricultural-upstream; FoodOn reuses its terms.
- **SNOMED-CT food subset** — clinical terminology, strong on allergens and intolerances, weak on compositional semantics.
- **LanguaL / FoodEx2** — food-description systems; the food-semantic-web review names them but doesn't treat them deeply. EFSA's FoodEx2 is the common hook for European-regulatory-facing systems.
- **Principal Odor Map** — trained GNN rather than a relational DB, but serves as a grounding target for flavour / aroma extractions. Lee et al. report human-level accuracy on unseen compounds.
- **FlavorDB**, **Phenol-Explorer**, **LipidBank**, **Volatile Compounds in Food** — narrow, deep chemistry layers (see [[datasets-and-databases]]).

## Is the substrate enough? — an honest audit

**What's enough for Tier-1 execution** of the literature-mining layer in [[priority-improvements]] item 3:

- PMC full-text OA + Europe PMC OA + Agricola abstracts give you on the order of ~1M food-relevant records to work from — FoodAtlas's 155K-paper, 230K-relation run is the lower-bound demonstration that this suffices for food–chemical composition edges in a single ingredient class.
- FoodOn + FooDB + USDA FDC together give enough grounding targets that extracted mentions can be assigned canonical IDs for most raw ingredients.
- CC-BY licensing on the OA subsets plus public-domain patents means the pipeline can be assembled without commercial licences — a real constraint for a small team.

**What's still not enough:**

- **Elsevier / Wiley / Springer hybrid deposits are patchy.** A lot of the best rheology, texture, and food-processing primary literature lives behind the paywall. The usable English-language open-access food-science corpus is roughly the PMC-deposited subset, which is a fraction of the field.
- **No food-formulation patent corpus exists.** Building one is a nontrivial project (stratify by A23 subclass, seed a 100–200-term ingredient/process dictionary, tokenise carefully around hyphenated chemistry, annotate across 3–4 groups with pharma + regulatory + NLP expertise). Akhondi et al.'s chemical-patent corpus is the template; the food version is work to be done.
- **Culturally diverse recipe corpora beyond Recipe1M+ / AllRecipes don't exist at scale in English.** FoodSky is the existence proof for Chinese; nothing comparable for South Asian, African, or Latin American cuisines as mineable corpora.
- **Processed-foods vocabulary is weak across every ontology surveyed.** FoodOn is strong on biological provenance and weak on "what does 'modified wheat starch E1404' actually mean in a formulation". This affects both extraction (you can't ground what the ontology doesn't name) and downstream use (the ingredient graph inherits the vocabulary gap).
- **Tables, figures, and supplementary files** across all biomedical sources are outside LitSense's reach. This is where a lot of quantitative composition data lives — multimodal extraction is an unsolved layer.

The stopper on [[priority-improvements]] item 3 is **resolved for English-language raw-ingredient composition work**. It is **partially resolved** for substitution and process work (mineable but with coverage gaps). It is **unresolved** for culturally diverse recipes at scale and for processed-foods vocabulary regardless of language.

## Source

- `raw/research/llm-literature-mining-corpora/01-foodatlas-pipeline-2024.md` — LitSense API, PMC+PubMed coverage, FooDB citation gap, scale numbers.
- `raw/research/llm-literature-mining-corpora/02-foodatlas-expansion-npjscifood-2025.md` — KG composition numbers, 9-source integration, CTD/ChEMBL licensing.
- `raw/research/llm-literature-mining-corpora/04-food-semantic-web-review-arxiv-2025.md` — FoodOn / SNOMED / AGROVOC / LanguaL characterisation; cultural-bias and processed-foods gaps.
- `raw/research/llm-literature-mining-corpora/05-kg-food-science-review-pmc.md` — 11-KG survey, 22-ontology table, industrial-KG list.
- `raw/research/llm-literature-mining-corpora/06-europe-pmc-infrastructure-2015.md` — Europe PMC scale, licensing, deposit caveat for hybrid-OA food-science journals.
- `raw/research/llm-literature-mining-corpora/07-foodsky-llm-2025.md` — FoodEarth composition, CNKI / CC-BY-SA / CC-BY-NC licensing posture, Chinese-side substrate.
- `raw/research/llm-literature-mining-corpora/08-wipo-patent-analytics-ch7-textmining.md` — USPTO / EPO / Lens / PatentScope comparison, A23 IPC-class entry point, tokenisation guidance.
- `raw/research/llm-literature-mining-corpora/09-annotated-chemical-patent-corpus-plosone.md` — methodology template (stratified sampling, 12 entity types, LeadMine + BRAT, centroid voting, CC-BY hosting).

## Related

- [[literature-mining-pipelines]]
- [[datasets-and-databases]]
- [[ingredient-data-structures]]
- [[priority-improvements]]
- [[genai-leverage-points]]
- [[open-gaps]]
