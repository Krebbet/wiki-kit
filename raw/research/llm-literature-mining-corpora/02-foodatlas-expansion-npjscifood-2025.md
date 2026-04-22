---
url: "https://www.nature.com/articles/s41538-025-00680-9"
title: "A unified knowledge graph linking foodomics to chemical-disease networks and flavor profiles | npj Science of Food"
captured_on: "2026-04-21"
capture_method: "url"
assets_dir: "./assets"
---






[Download PDF](/articles/s41538-025-00680-9.pdf)








* Article
* [Open access](https://www.springernature.com/gp/open-science/about/the-fundamentals-of-open-access-and-open-research)
* Published: 20 January 2026


# A unified knowledge graph linking foodomics to chemical\-disease networks and flavor profiles


* [Fangzhou Li](#auth-Fangzhou-Li-Aff1-Aff2-Aff3)[1](#Aff1),[2](#Aff2),[3](#Aff3),
* [Jason Youn](#auth-Jason-Youn-Aff1-Aff2-Aff3)[1](#Aff1),[2](#Aff2),[3](#Aff3),
* [Kaichi Xie](#auth-Kaichi-Xie-Aff1-Aff3)[1](#Aff1),[3](#Aff3),
* [Trevor Chan](#auth-Trevor-Chan-Aff1-Aff2-Aff3)[1](#Aff1),[2](#Aff2),[3](#Aff3),
* [Pranav Gupta](#auth-Pranav-Gupta-Aff1-Aff2-Aff3)[1](#Aff1),[2](#Aff2),[3](#Aff3),
* [Arielle Yoo](#auth-Arielle-Yoo-Aff2-Aff3)[2](#Aff2),[3](#Aff3),
* [Michael Gunning](#auth-Michael-Gunning-Aff1-Aff2-Aff3)[1](#Aff1),[2](#Aff2),[3](#Aff3),
* [Keer Ni](#auth-Keer-Ni-Aff1-Aff2-Aff3)[1](#Aff1),[2](#Aff2),[3](#Aff3) \&
* …
* [Ilias Tagkopoulos](#auth-Ilias-Tagkopoulos-Aff1-Aff2-Aff3)[1](#Aff1),[2](#Aff2),[3](#Aff3)

Show authors

[*npj Science of Food*](/npjscifood)
**volume 10**, Article number: 33 (2026)
 [Cite this article](#citeas)




* 3896 Accesses
* [Metrics details](/articles/s41538-025-00680-9/metrics)






## Abstract

Modern nutrition science still lacks a comprehensive, machine\-readable map linking diet to molecular composition and biological effects. Here we present FoodAtlas, a large\-scale knowledge graph that links 1430 foods to 3610 chemicals, 2181 diseases, and 958 flavor descriptors through 96,981 provenance\-tracked edges. A transformer\-based text\-mining pipeline extracted 48,474 quantitative food–chemical associations from 125,723 literature sentences (*F*1 \= 0\.67\) and integrated them with 23,211 chemical–disease assertions from the Comparative Toxicogenomics Database, 15,222 chemical\-bioactivity records from ChEMBL, 3645 flavor annotations from FlavorDB and PubChem, and 6429 taxonomic relationships. Graph embeddings revealed six dietary modules whose signature metabolites delineate distinct, multisystem disease\-risk trajectories. Models built on FoodAtlas demonstrate practical utility: a bioactivity predictor achieved strong correlation with antioxidant assays (*R*² \= 0\.52; ρ \= 0\.72\), and a substitution engine reduced simulated total disease risk by 11\.9%.



### Similar content being viewed by others





![](./assets/2e0b4252b1e63e80.png)

### [Tracing the origins of molecular signals in food through integrative metabolomics and chemical databases](https://www.nature.com/articles/s41538-026-00802-x?fromPaywallRec=false)



Article
Open access
18 March 2026






![](./assets/0ad94abb3e786b9a.png)

### [From language models to large\-scale food and biomedical knowledge graphs](https://www.nature.com/articles/s41598-023-34981-4?fromPaywallRec=false)



Article
Open access
15 May 2023






![](./assets/e7389532047b4694.png)

### [A dataset of branched fatty acid esters of hydroxy fatty acids diversity in foods](https://www.nature.com/articles/s41597-023-02712-z?fromPaywallRec=false)



Article
Open access
10 November 2023







 window.dataLayer \= window.dataLayer \|\| \[];
 window.dataLayer.push({
 recommendations: {
 recommender: 'semantic',
 model: 'e5',
 policy\_id: null,
 timestamp: 1776806804,
 embedded\_user: 'null'
 }
 });
 

## Introduction

The interplay between food, chemicals, and health represents a cornerstone of research in nutrition, toxicology, and sensory science. Understanding these complex relationships is critical for addressing pressing global challenges, such as improving public health through personalized nutrition, developing innovative food products, and assessing the safety of dietary components. However, existing resources often lack the granularity, comprehensiveness, or integration necessary to fully explore these domains[1](/articles/s41538-025-00680-9#ref-CR1 "Allot, A. et al. LitSense: making sense of biomedical literature at sentence level. Nucleic Acids Res. 47, W594–W599 (2019)."). FoodAtlas[2](/articles/s41538-025-00680-9#ref-CR2 "Youn, J., Li, F., Simmons, G., Kim, S. & Tagkopoulos, I. FoodAtlas: automated knowledge extraction of food and chemicals from literature. Comput. Biol. Med. 181, 109072 (2024).") was developed to address these limitations by constructing a knowledge graph (KG) that combines data from diverse sources, enabling structured queries and advanced analytics.

Recent advances in the study of the interplay among foods, chemicals, and health have shifted the focus from isolated nutrient databases to integrated, data\-rich platforms that harness multiple omics and artificial intelligence technologies[3](/articles/s41538-025-00680-9#ref-CR3 "Cifuentes, A. Food analysis and foodomics. J. Chromatogr. A 1216, 7109 (2009)."),[4](/articles/s41538-025-00680-9#ref-CR4 "García-Cañas, V., Simó, C., Herrero, M., Ibáñez, E. & Cifuentes, A. Present and future challenges in food analysis: foodomics. Anal. Chem. 84, 10150–10159 (2012)."). Early food composition resources, such as FooDB[5](/articles/s41538-025-00680-9#ref-CR5 "FooDB. 
                  https://foodb.ca/
                  
                . [Accessed at 12/25/2025]") and USDA FoodData Central[6](/articles/s41538-025-00680-9#ref-CR6 "McKillop, K., Harnly, J., Pehrsson, P., Fukagawa, N. & Finley, J. FoodData Central, USDA’s updated approach to food composition data systems. Curr. Dev. Nutr. 5, 596–596 (2021)."), provided detailed chemical and nutritional profiles, but often operated as standalone silos[7](/articles/s41538-025-00680-9#ref-CR7 "USDA FoodData Central. 
                  https://fdc.nal.usda.gov/
                  
                . [Accessed at 12/25/2025]"). The emergence of foodomics, an approach that integrates food chemistry with genomics, proteomics, and metabolomics, has further enriched our understanding of bioactive compounds and their health impacts[8](/articles/s41538-025-00680-9#ref-CR8 "Capozzi, F. & Bordoni, A. Foodomics: a new comprehensive approach to food and nutrition. Genes Nutr. 8, 1–4 (2013)."). Concurrently, the application of knowledge graphs (KGs) in food science has enabled researchers to interlink heterogeneous datasets, thereby facilitating novel applications such as recipe development, diet–disease correlation discovery, and personalized nutrition recommendation[9](/articles/s41538-025-00680-9#ref-CR9 "Min, W., Liu, C., Xu, L. & Jiang, S. Applications of knowledge graphs for food science and industry. Patterns 3, 100484 (2022)."),[2](/articles/s41538-025-00680-9#ref-CR2 "Youn, J., Li, F., Simmons, G., Kim, S. & Tagkopoulos, I. FoodAtlas: automated knowledge extraction of food and chemicals from literature. Comput. Biol. Med. 181, 109072 (2024).").

Despite these promising developments, existing approaches exhibit notable limitations. Most traditional food composition tables (FCTs) and databases like USDA’s FoodData Central or FooDB focus on macronutrients and certain micronutrients, neglecting many bioactive phytochemicals that have potentially significant health effects[7](/articles/s41538-025-00680-9#ref-CR7 "USDA FoodData Central. 
                  https://fdc.nal.usda.gov/
                  
                . [Accessed at 12/25/2025]"),[10](/articles/s41538-025-00680-9#ref-CR10 "Jahangir, M., Kim, H. K., Choi, Y. H. & Verpoorte, R. Health-affecting compounds in Brassicaceae. Compr. Rev. Food Sci. Food Saf. 8, 31–43 (2009)."). Further, ontological resources such as FoodOn[11](/articles/s41538-025-00680-9#ref-CR11 "Dooley, D. M. et al. FoodOn: a harmonized food ontology to increase global food traceability, quality control and data integration. Npj Sci. Food 2, 23 (2018).") provide valuable standardization of food entities, but do not capture granular relationships (e.g., quantitative concentration data or exact part of relationships for foods). As a result, researchers often rely on labor\-intensive data integration approaches that do not scale easily[12](/articles/s41538-025-00680-9#ref-CR12 "Eftimov, T., Ispirova, G., Potočnik, D., Ogrinc, N. & Koroušić Seljak, B. ISO-FOOD ontology: a formal representation of the knowledge within the domain of isotopes for food science. Food Chem. 277, 382–390 (2019)."). Moreover, many existing KGs fail to incorporate advanced natural language processing (NLP) methods, which can unlock vast amounts of untapped data from the literature[13](/articles/s41538-025-00680-9#ref-CR13 "Furukawa H. Deep Learning for End-to-End Automatic Target Recognition from Synthetic Aperture Radar Imagery. IEICE Technical Report; IEICE Tech. Rep. 117, 35–40 (2018)."). Traditional text\-mining methods also face challenges in extracting numerical information (e.g., specific concentrations, complex units), reducing the ability to interpret or apply the data meaningfully.

Recent advances in transformer\-based NLP models have enabled more accurate automated extraction of relationships from textual sources[14](/articles/s41538-025-00680-9#ref-CR14 "Devlin, J., Chang, M-W., Lee, K. & Toutanova, K. BERT: Pre-training of Deep BidirectionalTransformers for Language Understanding. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pages 4171–4186, Minneapolis, Minnesota. Association for Computational Linguistics. (2019)."),[15](/articles/s41538-025-00680-9#ref-CR15 "Vaswani, A. et al. Attention is all you need. Advances in neural information processing systems, 30. 
                  https://doi.org/10.48550/arXiv.1706.03762
                  
                 (2017)."). Models like BioBERT[16](/articles/s41538-025-00680-9#ref-CR16 "Lee, J. et al. BioBERT: a pre-trained biomedical language representation model for biomedical text mining. Bioinformatics 36, 1234–1240 (2020).") have dramatically improved the automated extraction of food–chemical relationships from vast bodies of biomedical literature. For example, FoodChem[17](/articles/s41538-025-00680-9#ref-CR17 "Cenikj, G., Seljak, B. K. & Eftimov, T. FoodChem: A food-chemical relation extraction model. In 2021IEEE Symposium Series on Computational Intelligence (SSCI) (pp. 1-8). IEEE. (2021).") employed these techniques to identify “contains” relations with high accuracy, automating the extraction of thousands of food–chemical interactions. Moreover, large language models can achieve high accuracy in extracting chemical food safety hazards from scientific abstracts, often exceeding 90% without extensive additional training[18](/articles/s41538-025-00680-9#ref-CR18 "Özen, N., Mu, W., van Asselt, ED. & van den Bulk, LM. Extracting chemical food safety hazards from the scientific literature automatically using large language models. Appl. Food Res. 5, 100679, 
                  https://doi.org/10.1016/j.afres.2024.100679
                  
                 (2025)."). These pipelines facilitate integration of data from external sources like the Comparative Toxicogenomics Database (CTD)[19](/articles/s41538-025-00680-9#ref-CR19 "Davis, A. P. et al. Comparative Toxicogenomics Database’s 20th anniversary: update 2025. Nucleic Acids Res. 53, D1328–D1334 (2025).") and flavor repositories[20](/articles/s41538-025-00680-9#ref-CR20 "FlavorDB: a database of flavor molecules | Nucleic Acids Research | Oxford Academic. 
                  https://academic.oup.com/nar/article/46/D1/D1210/4559748
                  
                ."),[21](/articles/s41538-025-00680-9#ref-CR21 "Fonger, G. C. Hazardous substances data bank (HSDB) as a source of environmental fate information on chemicals. Toxicology 103, 137–145 (1995)."), enabling the KG to also encompass health and sensory attributes. However, a gap remains in terms of unifying these diverse data types, such as bioactivity and disease associations, flavor attributes, and chemical concentrations, into a single, consistent knowledge resource that can be readily accessed and queried.

Beyond these general limitations, several food\-focused knowledge resources have emerged, but each covers only parts of the domain. FoodKG[22](/articles/s41538-025-00680-9#ref-CR22 "Haussmann, S. et al. FoodKG: a semantics-driven knowledge graph for food recommendation. In The Semantic Web – ISWC 2019 (eds Ghidini, C. et al.) Vol. 11779 146–162 (Springer International Publishing, Cham, 2019).") integrates recipes, ingredients, and nutrition, FlavorGraph[23](/articles/s41538-025-00680-9#ref-CR23 "Park, D., Kim, K., Kim, S., Spranger, M. & Kang, J. FlavorGraph: a large-scale food-chemical graph for generating food representations and recommending food pairings. Sci. Rep. 11, 931 (2021).") links ingredients with flavor compounds and recipe co\-occurrence, and NutriChem[24](/articles/s41538-025-00680-9#ref-CR24 "Ni, Y., Jensen, K., Kouskoumvekaki, I. & Panagiotou, G. NutriChem 2.0: exploring the effect of plant-based foods on human health and drug efficacy. Database 2017, bax044 (2017).") connects plant\-based foods with phytochemicals and diseases via text\-mining. Supplementary Table [1](/articles/s41538-025-00680-9#MOESM1) summarizes how FoodAtlas compares with these resources in scale and scope. Notably, FoodAtlas is the first to unify food composition, chemical\-bioactivity, and disease associations in a single graph, achieving broader entity coverage and relationship types than any prior resource.

In this work, we present a new framework to support evidence synthesis that we incorporate into *FoodAtlas*[2](/articles/s41538-025-00680-9#ref-CR2 "Youn, J., Li, F., Simmons, G., Kim, S. & Tagkopoulos, I. FoodAtlas: automated knowledge extraction of food and chemicals from literature. Comput. Biol. Med. 181, 109072 (2024)."), which includes large language models to extract food knowledge from scientific literature, capable of extracting diverse metadata, such as concentration values. To support better query and synthesis capabilities, we have doubled the number of resources (9 sources total), incorporated 5 ontologies, and expanded relationships to sensory and disease attributes (Fig. [1](/articles/s41538-025-00680-9#Fig1)). First, we detail the updated information extraction pipeline, which leverages state\-of\-the\-art large language models. Then, we apply unsupervised machine learning to the FoodAtlas data, demonstrating that the learned representations form meaningful clusters related to food and health. Finally, we demonstrate potential real\-world use cases of FoodAtlas by showcasing two relevant health applications. Specifically, a bioactivity predictor model and a simple diet recommendation supported by FoodAtlas data result in predictive results corroborated by published literature.



**Fig. 1: FoodAtlas pipeline for building and analyzing a multi\-layer food–chemical knowledge graph.**

![Fig. 1: FoodAtlas pipeline for building and analyzing a multi-layer food–chemical knowledge graph.](./assets/b6f789dc1ef80dbe.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41538-025-00680-9/figures/1)Food names from FooDB and USDA FoodData Central are used to retrieve full\-text articles in PubMed Central; BioBERT filters co\-mention sentences, which are converted into quantitative Food → Chemical triplets. Chemicals already cataloged in FoodAtlas are then linked to the Comparative Toxicogenomics Database to add Chemical → Disease edges and to FlavorDB for Chemical → Flavor edges, yielding an integrated graph that unifies compositional, biomedical, and sensory information. This enriched FoodAtlas Knowledge Graph underpins downstream tasks—including t\-SNE clustering of foods, supervised bioactivity prediction, and disease\-focused food substitutions—enabling data\-driven nutrition and precision\-diet applications.

## Results

### FoodAtlas incorporates data from a variety of different sources

FoodAtlas markedly broadens both the breadth and resolution of the knowledge graph, interlinking 1430 foods with 3610 chemicals through 48,474 curated food\-to\-chemical edges (Fig. [2](/articles/s41538-025-00680-9#Fig2)). A major feature is the integration of 23,211 chemical\-to\-disease assertions, 13,417 “treats” and 9794 “worsens” relationships, covering 2181 diseases extracted from the CTD. Each chemical node is normalized to its MeSH identifier, and every edge carries CTD provenance metadata, Direct Evidence plus PubMed citations, creating a transparent scaffold for toxicological and biomedical inquiry. FoodAtlas also incorporates the chemical\-to\-bioactivity linking all the chemicals contained in at least one food to 8 key bioactivities derived from ChEMBL, alongside 660 direct food\-to\-bioactivity antioxidant FRAP values. FoodAtlas also introduces a sensory layer: 3645 chemical\-to\-flavor links connecting 958 unique flavor descriptors compiled from FlavorDB and PubChem.



**Fig. 2: Composition of the FoodAtlas Knowledge Graph.**

![Fig. 2: Composition of the FoodAtlas Knowledge Graph.](./assets/50cb8c73cb52422a.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41538-025-00680-9/figures/2)**A** Entity–relation schema with node counts (in parentheses) and edge counts on the arrows: foods (1430\) connect to chemicals (10,266\) through *contains* edges (48,474\); chemicals link hierarchically via *is a* (263,021\); chemicals map to diseases (3177\) through *treats/worsens* relations (138,792\); chemicals map to flavors (1117\) through *has flavor* (6169\); foods are organized taxonomically by additional *is a* edges (11,683\). **B** Chemical superclass breakdown shows that polyatomic molecules dominate (1115; 53\.2%), followed by main group molecules (313; 14\.9%), lipids (158; 7\.5%), ions (140; 6\.7%), glycans (54; 2\.6%), amino acid derivatives (30; 1\.4%), inorganic molecules (16; 0\.8%) and other classes (268; 12\.8%). **C** Integrated circos plot depicting the ecosystem of food–chemical–disease–flavor relationships across all entities in FoodAtlas. The outermost ring shows the category arcs. Inside this, a narrow white ring hosts a scatter\-style evidence lane: red radial bars plot, for every sub\-category, the volume of supporting metadata (bar height scales with evidence count). The innermost colored band comprises the sub\-category arcs. **D** Sunburst plots showing hierarchical distributions of flavor descriptors and disease outcomes. Each sunburst represents the relative frequency of (outer ring) subcategories nested within (inner ring) major categories.

### Large language model\-based information extraction accurately extracts chemical composition

The test set consists of 356 sentences and was used to evaluate the performance of the OpenAI GPT\-4, GPT\-3\.5, and fine\-tuned GPT\-3\.5 models. We applied both a zero\-shot prompt, containing only extraction instructions, and a one\-shot prompt, containing one example along with the instructions to the pre\-trained GPT\-4 and GPT\-3\.5 models (Supplementary Note [1\.1](/articles/s41538-025-00680-9#MOESM1)). Additionally, we fine\-tuned the GPT\-3\.5 model using the zero\-shot prompt, achieving a significantly higher F1\-score of 0\.67 compared to 0\.42 for GPT\-4 with the one\-shot prompt (Supplementary Figs. [2](/articles/s41538-025-00680-9#MOESM1), [3](/articles/s41538-025-00680-9#MOESM1)).

### FoodAtlas knowledge graph encoded meaningful food representation in chemical and health spaces

Projection of the food\-by\-chemical matrix into t\-SNE[25](/articles/s41538-025-00680-9#ref-CR25 "van der Maaten, L. & Hinton, G. Visualizing data using t-SNE. J. Mach. Learn. Res. 9, 2579–2605 (2008).") space of the raw composition matrix confirms that the metabolites driving disease divergence are the dominant axes of compositional variance (Fig. [3A](/articles/s41538-025-00680-9#Fig3)). Following this, a density\-based clustering[26](/articles/s41538-025-00680-9#ref-CR26 "McInnes, L., Healy, J. & Astels, S. hdbscan: hierarchical density based clustering. J. Open Source Softw. 2, 205 (2017).") and a two\-part hurdle test[27](/articles/s41538-025-00680-9#ref-CR27 "Mullahy, J. Specification and testing of some modified count data models. J. Econom. 33, 341–365 (1986)."), chemical enrichment (*q*enrich), and disease intensity (*q*intensity), each with a false discovery rate[28](/articles/s41538-025-00680-9#ref-CR28 "Benjamini, Y. & Hochberg, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J. R. Stat. Soc. Ser. B Methodol. 57, 289–300 (1995).") smaller than 0\.10, resolved six significant disease composition clusters (Fig. [3B](/articles/s41538-025-00680-9#Fig3), Table [1](/articles/s41538-025-00680-9#Tab1), and Supplementary Note [1\.4](/articles/s41538-025-00680-9#MOESM1)). Collectively, these six clusters reveal chemical composition patterns that correlate with divergent disease\-risk trajectories, highlighting potential mechanisms linking dietary components to health outcomes. The *omega\-3 marine oils* cluster contains oily fish and krill products, which are extremely enriched in EPA (*q*enrich \= 1\.3 × 10−20) and DHA (*q*enrich \= 4\.9 × 10−14). This group shows the dataset’s strongest protection, lowering cardiovascular risk (*q*intensity \= 1\.2 × 10−7) and improving metabolic, digestive, and nervous\-system scores (all *q*intensity \< 10−2). The *high omega\-6 seed oils* cluster, which includes sunflower, safflower, and rice\-bran oils, shares significant linoleic\-acid enrichment (*q*enrich \= 4\.0 × 10−7) but exhibits a modest yet significant rise in the composite “pathological\-conditions” score (*q*intensity \= 1\.0 × 10−3), echoing reports that excessive omega\-6 intake can sustain low\-grade inflammation[29](/articles/s41538-025-00680-9#ref-CR29 "Johnson, G. H. & Fritsche, K. Effect of dietary linoleic acid on markers of inflammation in healthy persons: a systematic review of randomized controlled trials. J. Acad. Nutr. Diet. 112, 1041.e1–15 (2012)."). The *anthocyanin\-rich berries*, such as blueberry, bilberry, and black\-currant, are highly enriched for total anthocyanins (*q*enrich \= 2\.3 × 10−5) and deliver broad protection, most prominently against cardiovascular disease (*q*intensity \= 1\.0 × 10−3) with auxiliary benefits in respiratory and metabolic domains (*q*intensity \= 5\.0 × 10−2). The *citrus\-terpene modulators* cluster, consisting of oranges, lemons, and limes, is dominated by limonene (*q*enrich \= 9\.2 × 10−24), is linked to lower neoplasm scores (*q*intensity \= 1\.0 × 10−6) yet higher skin/connective\-tissue scores (*q*intensity \= 1\.0 × 10−10), mirroring limonene’s chemo\-preventive activity alongside its well\-known phototoxicity[30](/articles/s41538-025-00680-9#ref-CR30 "Crowell, P. L. Prevention and therapy of cancer by dietary monoterpenes. J. Nutr. 129, 775S–778S (1999)."). The *fat\-dense animal proteins*, including bacon, sausages, and hard cheeses, concentrate palmitic acid (*q*enrich \= 4\.0 × 10−35) and industrial trans\-fatty acids (*q*enrich \= 2\.3 × 10−14). The cluster is associated with worsening stomatognathic disease (*q*intensity \= 1\.0 × 10−3) and measurable endocrine and cardiovascular penalties (*q*intensity \= 5\.0 × 10−2). Finally, the *high\-fructose fruit concentrates* cluster, which involves grape and apple juices and high\-Brix tomato products, shows extreme fructose (*q*enrich \= 2\.6 × 10−22) and glucose (*q*enrich \= 2\.1 × 10−19) enrichment, translating into increased nervous\-system (qintensity \= 1\.0 × 10−7) and urogenital (*q*intensity \= 1\.0 × 10−7) disease scores and broader metabolic detriments (*q*intensity \= 1\.0 × 10−2).



**Fig. 3: Concordant chemical and disease structure in FoodAtlas foods.**

![Fig. 3: Concordant chemical and disease structure in FoodAtlas foods.](./assets/31149ddd5c8b7a71.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41538-025-00680-9/figures/3)**A** Composition space. A Node2Vec[105](/articles/s41538-025-00680-9#ref-CR105 "Grover, A. & Leskovec, J. \"node2vec: Scalable feature learning for networks.\" Proceedings of the 22nd ACMSIGKDD international conference on Knowledge discovery and data mining. (2016).") embedding built only from food\-to\-chemical edges was projected with t\-SNE (center plot). Density\-based clustering (dashed ellipses) resolves nine chemically coherent groups whose insets (top and side panels) name representative members. The horizontal bar\-stripe beneath the scatter ranks the chemicals that are significantly enriched within each group (signed\-log₁₀ *q* from the two\-part hurdle test; darker blue \= stronger enrichment). **B** Disease\-aware space. Adding signed chemical\-to\-disease edges to the graph and repeating the embedding yields a second t\-SNE in which node color encodes the composite, normalized disease score (blue \= protective, red \= harmful). Six clusters that survive the dual chemical\-plus\-disease hurdle test are emphasized (dashed ellipses, labels). The dot\-matrix to the right compares, for those clusters, (i) over\-represented food categories (top sub\-panel) and (ii) disease classes that differ significantly from the background (bottom; dot size ∝ −log₁₀ *q*, color sign \= protection or risk). The lower bar\-stripe again lists the hallmark enriched chemicals, showing that the same metabolites—EPA/DHA, anthocyanins, limonene, palmitic acid, fructose/glucose, linoleic acid—drive separation in both purely compositional and health\-augmented landscapes.



**Table 1 Chemistry and disease signatures of supported clusters**

[Full size table](/articles/s41538-025-00680-9/tables/1)### By integrating chemical composition, structural fingerprints, and potency data, we accurately predict food\-level antioxidant capacity

The integration of FoodAtlas composition data with ChEMBL potency measurements culminated in a BFL set that maps 15,222 chemicals across 660 foods to quantitative bioactivity readouts via pChEMBL values. A preliminary attempt that relied on pChEMBL values alone was uninformative (Supplementary Note [1\.5](/articles/s41538-025-00680-9#MOESM1)). In contrast, the ensuing BPM, which jointly leverages chemical concentrations, extended\-connectivity fingerprints, and potency scores, captured 52% of the variance in literature FRAP measurements and achieved a Pearson correlation coefficient (PCC) of 0\.72 (*p* \= 3\.9 × 10−14); three quarters of predictions deviated by ≤±0\.81 −log₁₀(FRAP) units (Fig. [4A](/articles/s41538-025-00680-9#Fig4)). Residual analysis confirmed stable model performance, showing a negligible correlation (*r* \= 0\.039\) between predicted values and model residuals. Beyond reproducing reported values, BPM generalizes to previously uncharacterized items: Fig. [4B](/articles/s41538-025-00680-9#Fig4) ranks the 50 common foods per their predicted antioxidant content, illustrating the model’s utility for rapid triage of antioxidant potential in foods lacking experimental FRAP data.



**Fig. 4: Predictive performance of the antioxidant Bioactivity Prediction Model (BPM).**

![Fig. 4: Predictive performance of the antioxidant Bioactivity Prediction Model (BPM).](./assets/3eefa78f49266393.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41538-025-00680-9/figures/4)**A** Goodness of fit and diagnostics. The left panel contrasts BPM\-predicted versus literature\-reported antioxidant activity (negative log\-transformed FRAP values) for foods with available measurements. The model attains an *R*² \= 0\.52 and a Pearson correlation coefficient (PCC) \= 0\.72\. The right panel plots studentized residuals against observed antioxidant values, revealing homoscedastic error dispersion around zero and no systematic bias across the response range. **B** Extrapolative ranking of unmeasured foods. The bar chart lists the top\-50 FoodAtlas foods by predicted antioxidant content (pink bars ± prediction error). Green circles indicate foods for which experimental FRAP data exist, showing close concordance with model estimates and underscoring the BPM’s ability to prioritize candidate foods that currently lack empirical measurements.

### Holistic food substitutions achieve significant disease\-risk reduction and antioxidant gains

We modeled 14,580 disease\-focused substitutions and 7798 antioxidant\-focused substitutions (Fig. [5A](/articles/s41538-025-00680-9#Fig5) and Supplementary Table [5](/articles/s41538-025-00680-9#MOESM1)). Across the full dataset, the mean disease prevention score rose by 11\.9%. Improvements were equally weighted across all meals \- breakfast (9\.9%), lunch (10\.0%), and dinner (11\.1%) meals (Fig. [5B](/articles/s41538-025-00680-9#Fig5)). All reductions remained significant after correction for multiple testing (*q* \< 10−3). Applying the same substitution framework to antioxidant bioactivity more than tripled predicted activity, yielding an average increase of 210\.6%, with peak enhancements at lunch (257\.9%), dinner (185\.8%), and breakfast (176\.4%). We first quantified the aggregate change in disease\-risk score that resulted from category\-matched food swaps (Fig. [5A](/articles/s41538-025-00680-9#Fig5)). Radar plots of individual disease domains confirmed broad\-spectrum improvements rather than benefits confined to a single system (Fig. [5B](/articles/s41538-025-00680-9#Fig5)). To dissect the chemical basis of these effects, we extracted the ten most influential chemicals for each meal type and visualized both their absolute contributions to risk and the direction of change induced by the swap (Fig. [5C](/articles/s41538-025-00680-9#Fig5), left versus right sub\-panels). Protective shifts were consistently driven by polyphenolic flavonoids, including quercetin, kaempferol, and cyanidin, and long\-chain omega\-3 fatty acids (EPA, DHA), which exhibited uniformly negative differential scores (cool hues). Conversely, heterocyclic amines such as PhIP and MeIQx, advanced glycation end\-products (CML, CEL), and saturated tri\-acyl\-glycerols (palmitic\-, stearic\-, and lauric\-TAGs) remained dominant positive contributors (warm hues). The recurrence of these chemical signatures across breakfast, lunch, and dinner indicates that the underlying mechanisms are conserved and time\-of\-day–independent. Three\-layer Sankey diagrams traced the pathways from food categories through chemical classes to disease domains, revealing how dietary risk propagates through the food system (Fig. [5D](/articles/s41538-025-00680-9#Fig5)). By measuring how much the total chemical content of meals changed after substitutions and testing whether these changes were statistically meaningful, we identified the most robust pathways. Equalized node heights decoupled topological structure from magnitude, making “risk bottlenecks” visually salient. Processed\-meat and refined\-grain categories converged through heterocyclic amines and dicarbonyl AGEs onto neoplasm nodes, where food substitutions significantly increased cancer\-related chemical content (*q* \= 1\.8 × 10−56 for breakfast; *q* \= 5\.1 × 10−77 for lunch; *q* \= 1\.1 × 10−68 for dinner), cardiovascular nodes, where substitutions increased heart disease risk (*q* \= 2\.2 × 10−5 for breakfast; *q* \= 8\.5 × 10−19 for lunch; *q* \= 7\.0 × 10−4 for dinner), and endocrine\-metabolic nodes, where substitutions disrupted hormonal systems (*q* \= 8\.7 × 10−4 for breakfast; *q* \= 2\.2 × 10−35 for lunch; *q* \= 2\.9 × 10−30 for dinner). Conversely, berries, leafy greens, and olive products channeled flavonoids and monophenols towards protective endocrine\-metabolic nodes (*q* \= 8\.7 × 10−4 for breakfast; *q* \= 2\.2 × 10−35 for lunch; *q* \= 2\.9 × 10−30 for dinner) and immune nodes (*q* \= 8\.7 × 10−4 for breakfast; *q* \= 5\.1 × 10−37 for lunch; *q* \= 1\.3 × 10−31) where substitutions significantly reduced disease risk (Tables [2](/articles/s41538-025-00680-9#Tab2) and [3](/articles/s41538-025-00680-9#Tab3)).



**Table 2 Representative one\-hop, within\-category substitutions to maximize disease\-risk reduction across meal types**

[Full size table](/articles/s41538-025-00680-9/tables/2)

**Table 3 Representative one\-hop, within\-category substitutions to maximize antioxidant bioactivity enhancement across meal types**

[Full size table](/articles/s41538-025-00680-9/tables/3)

**Fig. 5: FoodAtlas\-guided, category\-matched ingredient swaps attenuate predicted disease risk and expose their chemical drivers across breakfast, lunch, and dinner.**

![Fig. 5: FoodAtlas-guided, category-matched ingredient swaps attenuate predicted disease risk and expose their chemical drivers across breakfast, lunch, and dinner.](./assets/be6aa3d5c9e63f62.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41538-025-00680-9/figures/5)**A** Paired box\-and\-whisker plots of per\-disease scores (22 MeSH classes) for breakfast (blue), lunch (green), and dinner (orange) meals before (lighter tint) and after (darker tint) replacing the single ingredient with the greatest weighted risk by a nutritionally superior food from the same category. Box centers show medians, hinges the inter\-quartile range, whiskers 1\.5 × IQR, and dots outliers; horizontal bars denote Wilcoxon signed\-rank significance (*p* \< 0\.05, \**p* \< 0\.01, \*\**p* \< 0\.001\). All three meal types shift consistently toward lower risk after substitution. **B** Radar plots for one representative meal per time\-of\-day illustrate the multidimensional benefit of a single swap—nectarine → cranberry in a fruit\-and\-cottage\-cheese breakfast (\+21% aggregate improvement), hummus → olive in a pita\-and\-chickpea lunch (\+18%), and oatmeal\-raisin cookie → sweet\-potato purée in a spinach\-and\-feta dinner (\+4%). Solid polygons trace pre\-swap scores, dashed polygons post\-swap scores; adjoining dot\-plots rank the five chemicals contributing most to each improvement. **C** For each meal type, paired heat\-maps display the mean signed contribution of the ten most influential chemicals (columns) to every disease class (rows): the left panel shows the change induced by the swap (baseline – optimized), the right panel the absolute post\-swap impact. Meal\-specific color maps (Blues, Greens, Oranges) reveal a conserved pattern in which polyphenol\-rich flavonoids and omega\-3 fatty acids align with risk reductions (cool hues), whereas heterocyclic amines, advanced glycation products, and saturated tri\-acyl\-glycerols drive risk elevations (warm hues). **D** Three\-layer Sankey diagrams trace risk flow from food categories (left) through chemical classes (center) to disease classes (right). Node heights are equalized with a constant dummy flow to separate topology from magnitude, so dominant “risk bottlenecks” stand out visually. Companion lollipop charts plot the –log₁₀(*p*\-values) for enrichment of each disease class, confirming the statistical significance of the observed pathways. Together, the panels demonstrate that single, FoodAtlas\-recommended swaps reliably lower predicted disease burden and that a small, mechanistically coherent set of chemicals mediates most of the benefit.

## Discussion

In this study, we introduce FoodAtlas, a substantially expanded and fully traceable knowledge graph that integrates compositional, toxicological, flavor, and bioactivity data for advanced dietary analysis. By linking 1430 foods to 3610 chemicals through 48,474 curated food–chemical edges, incorporating 23,211 chemical–disease assertions across 2181 diseases (13,417 ameliorative, 9794 exacerbating), 15,222 chemical\-bioactivity assertions across eight bioactivities, 660 food\-antioxidant bioactivity, and layering in 3645 chemical\-flavor relationships covering 958 descriptors, FoodAtlas represents a major leap in both breadth and resolution over its predecessor. Our ontology\-aware, transformer\-driven ingestion pipeline achieved an F1 of 0\.67 on held\-out extraction tasks, enabling reliable scaling of literature\-derived composition facts. The Bioactivity Prediction Model further demonstrates generalizability, explaining 52% of variance in FRAP assays (*R*² \= 0\.52, PCC \= 0\.72\) and ranking antioxidant potential for previously uncharacterized foods. We used antioxidant activity as a benchmark endpoint because it is one of the most widely studied and quantitatively validated measures in food and nutrition research[31](/articles/s41538-025-00680-9#ref-CR31 "Benzie, I. F. F. & Choi, S.-W. Chapter One - Antioxidants in food: content, measurement, significance, action, cautions, caveats, and research needs. In Advances in Food and Nutrition Research (ed. Henry, J.) Vol. 71 1–53 (Academic Press, 2014)."), or for evaluating bioactive compounds’ health benefits[32](/articles/s41538-025-00680-9#ref-CR32 "Shahidi, F. & Ambigaipalan, P. Phenolics and polyphenolics in foods, beverages and spices: antioxidant activity and health effects – A review. J. Funct. Foods 18, 820–897 (2015)."). The BPM’s reliance on chemical structure, potency, and concentration data illustrates extensibility to other bioactivities, such as those screened via AI for food\-derived peptides with anti\-obesity or anti\-fatigue effects[33](/articles/s41538-025-00680-9#ref-CR33 "Chang, J., Wang, H., Su, W., He, X. & Tan, M. Artificial intelligence in food bioactive peptides screening: recent advances and future prospects. Trends Food Sci. Technol. 156, 104845 (2025)."), while bioactive compounds’ broader impacts on diseases like diabetes and cancer underscore the framework’s biological relevance[34](/articles/s41538-025-00680-9#ref-CR34 "Alvarez-Leite, J. I. The role of bioactive compounds in human health and disease. Nutrients 17, 1170 (2025)."). Finally, our substitution framework, evaluating 14,580 disease\-focused and 7798 antioxidant\-focused one\-hop swaps, yielded a mean 11\.9% disease\-risk reduction and 210\.6% increase in predicted antioxidant activity across breakfast, lunch, and dinner. These results suggested FoodAtlas’s dual role as both a mechanistic knowledge base and a decision\-support engine. The enriched graph structure, complete with MeSH\-normalized nodes and PubMed\-cited provenance metadata, could empower in\-depth toxicological and nutrigenomic investigations.

There are several rooms for improvement for our future work. First, our information\-extraction F1 of 0\.67 indicates errors in entity and relation recognition, particularly in complex or tabular contexts. In the future, we aim to utilize a more advanced large language model, such as GPT\-5[35](/articles/s41538-025-00680-9#ref-CR35 "GPT-5 System Card. 
                  https://openai.com/index/gpt-5-system-card/
                  
                 (2025)."), incorporating techniques like multimodal reasoning[36](/articles/s41538-025-00680-9#ref-CR36 "Zhang, Z. et al. Multimodal chain-of-thought reasoning in language models. 
                  https://openreview.net/forum?id=gDlsMWost9
                  
                 (2023).") and structured output[37](/articles/s41538-025-00680-9#ref-CR37 "Liu, M. X. et al. ‘We Need Structured Output’: towards user-centered constraints on large language model output. In Extended Abstracts of the CHI Conference on Human Factors in Computing Systems 1–9 (Association for Computing Machinery, New York, NY, USA, 2024)."), as well as incorporating unstructured sources (e.g., tables) and hybrid architectures[38](/articles/s41538-025-00680-9#ref-CR38 "Lu, W. et al. Large language model for table processing: a survey. Front. Comput. Sci. 19, 192350 (2025)."), to enhance the extraction performance. Second, CTD\-derived disease associations are binary and do not capture dose\-response dynamics or clinical outcomes. To improve, we consider incorporating quantitative toxicology (dose\-response data, clinical endpoints) for predicting therapeutic success[39](/articles/s41538-025-00680-9#ref-CR39 " Li, F., Youn, J., Millsop, C. & Tagkopoulos, I. Predicting clinical trial success for Clostridium difficile infections based on preclinical data. Front. Artif. Intell. 710.3389/frai.2024.1487335 (2024)."). Third, the BPM’s reliance on existing pChEMBL and concentration data may introduce biases due to uneven assay coverage. In the future, we plan to expand coverage by developing an automated pipeline to extract bioactivity data from the broader scientific literature and implementing active learning approaches to prioritize underrepresented targets and compound classes[40](/articles/s41538-025-00680-9#ref-CR40 "Ren, P. et al. A survey of deep active learning. ACM Comput. Surv. 54, 180:1-180:40 (2021)."). We also plan to expand our predictive bioactivity modeling to other endpoints, e.g., antidiabetic bioactivity, glycemic index values can serve as functional indicators of glucose regulation potential[41](/articles/s41538-025-00680-9#ref-CR41 "Foster-Powell, K., Holt, S. H. & Brand-Miller, J. C. International table of glycemic index and glycemic load values: 2002. Am. J. Clin. Nutr. 76, 5–56 (2002)."), while anti\-inflammatory activity can be approximated using the Dietary Inflammatory Index[42](/articles/s41538-025-00680-9#ref-CR42 "Shivappa, N., Steck, S. E., Hurley, T. G., Hussey, J. R. & Hébert, J. R. Designing and developing a literature-derived, population-based dietary inflammatory index. Public Health Nutr. 17, 1689–1696 (2014)."). Fourth, due to the lack of a standardized flavor ontology, flavors are used as descriptors for chemicals rather than embedded as part of modeling. In the future, we plan to use an LLM\-based human\-in\-the\-loop tool to design a practical ontology for flavors[43](/articles/s41538-025-00680-9#ref-CR43 "Toro, S. et al. Dynamic Retrieval Augmented Generation of Ontologies using Artificial Intelligence (DRAGON-AI). J. Biomed. Semant. 15, 19 (2024)."),[44](/articles/s41538-025-00680-9#ref-CR44 " Youn, J., Naravane, T. & Tagkopoulos, I. Using Word Embeddings to Learn a Better Food Ontology. Front. Artif. Intell. 310.3389/frai.2020.584784. (2020)."), which will help with more versatile downstream tasks. Fifth, our one\-hop substitution approach is simplified and does not reflect the multifaceted complexity of food\-health interaction. Specifically, we do not account for multi\-ingredient and chemical synergies, cultural dietary patterns, or palatability constraints, bioavailability, exposure, and metabolism[45](#ref-CR45 "Jacobs, D. R. Jr & Tapsell, L. C. Food synergy: the key to a healthy diet. Proc. Nutr. Soc. 72, 200–206 (2013)."),[46](#ref-CR46 "Nemec, K. Cultural awareness of eating patterns in the health care setting. Clin. Liver Dis. 16, 204–207 (2020)."),[47](#ref-CR47 "Forde, C. G. & de Graaf, K. Influence of sensory properties in moderating eating behaviors and food intake. Front. Nutr. 9, 841444 (2022)."),[48](#ref-CR48 "Melse-Boonstra, A. Bioavailability of micronutrients from nutrient-dense whole foods: zooming in on dairy, vegetables, and fruits. Front. Nutr. 7, 101 (2020)."),[49](#ref-CR49 "Benford, D. et al. The principles and methods behind EFSA’s guidance on uncertainty analysis in scientific assessment. EFSA J 16, e05122 (2018)."),[50](/articles/s41538-025-00680-9#ref-CR50 "Shannar, A. et al. Pharmacodynamics (PD), pharmacokinetics (PK) and PK-PD modeling of NRF2 activating dietary phytochemicals in cancer prevention and in health. Curr. Pharmacol. Rep. 11, 6 (2024)."), which could limit real\-world adoption. For this work, we focus on highlighting the potential of how the FoodAtlas Knowledge Graph could provide a data source even for simplistic downstream models to capture correlation corroborated with literature validation. As future work, we plan to continuously ingest newly published literature data into the FoodAtlas Knowledge Graph to support different use cases by scientists and collaborate with domain experts to advance the food\-based health intervention research. Lastly, we continuously work to enhance the usability of our data and web interface, which we aim to extend ontologies, such as MONDO[51](/articles/s41538-025-00680-9#ref-CR51 "Vasilevsky, N. A. et al. Mondo: Unifying diseases for the world, by the world. Preprint at 
                  https://doi.org/10.1101/2022.04.13.22273750
                  
                 (2022).") for diseases, for better searchability, different downloadable data formats, such as Parquet, JSON, RDF, and Neo4j, and periodic synchronization with external data sources, such as FoodOn[11](/articles/s41538-025-00680-9#ref-CR11 "Dooley, D. M. et al. FoodOn: a harmonized food ontology to increase global food traceability, quality control and data integration. Npj Sci. Food 2, 23 (2018)."), ChEBI[52](/articles/s41538-025-00680-9#ref-CR52 "Hastings, J. et al. ChEBI in 2016: improved services and an expanding collection of metabolites. Nucleic Acids Res. 44, D1214–D1219 (2016)."), and PubChem[53](/articles/s41538-025-00680-9#ref-CR53 "Kim, S. et al. PubChem 2023 update. Nucleic Acids Res. 51, D1373–D1380 (2023)."), to ensure interoperability.

FoodAtlas provides a promising foundation for precision nutrition and food\-innovation applications, uniting high\-resolution compositional data, mechanistic disease links, predictive bioactivity models, and dietary guidance in a single resource.

## Methods

### Sentence retrieval

We initially gathered 1300 food names, including both common and scientific terms, from FooDB and FoodData Central (FDC)[7](/articles/s41538-025-00680-9#ref-CR7 "USDA FoodData Central. 
                  https://fdc.nal.usda.gov/
                  
                . [Accessed at 12/25/2025]"). We then used these names to search PubMed[54](/articles/s41538-025-00680-9#ref-CR54 "PubMed. PubMed 
                  https://pubmed.ncbi.nlm.nih.gov/
                  
                . [Accessed at 12/25/2025].") and PubMed Central (PMC)[55](/articles/s41538-025-00680-9#ref-CR55 "PubMed Central (PMC). PubMed Central (PMC) 
                  https://pmc.ncbi.nlm.nih.gov/
                  
                . [Accessed at 12/25/2025]."), which host 36 million and 9\.8 million abstracts and full\-text articles in biomedical and life sciences, respectively. The searches were conducted using the NCBI’s Entrez Direct (EDirect)[56](/articles/s41538-025-00680-9#ref-CR56 "Kans, J. Entrez Direct: E-utilities on the Unix Command Line. In Entrez Programming Utilities Help [Internet] (National Center for Biotechnology Information (US), 2025).") to retrieve scientific literature that mentions these food names. We employed a search template “*{food name} AND ((compound) OR (nutrient))*” to ensure that the articles included not only the food name but also at least one of the keywords, ‘compound’ or ‘nutrient.’ This search template was empirically selected to enhance the accuracy of the results. Next, we tokenized the retrieved scientific literature into sentences using the NLTK library[57](/articles/s41538-025-00680-9#ref-CR57 "Bird, S. & Loper, E. NLTK: The Natural Language Toolkit. In Proceedings of the ACL Interactive Poster and Demonstration Sessions, pages 214–217, Barcelona, Spain. Association for Computational Linguistics. (2004).") and excluded sentences that were either too short or too long, following the approach used by LitSense in their study[1](/articles/s41538-025-00680-9#ref-CR1 "Allot, A. et al. LitSense: making sense of biomedical literature at sentence level. Nucleic Acids Res. 47, W594–W599 (2019).").

### Sentence filtering

Since not all sentences in the retrieved articles above were related to food–chemical associations, we followed a two\-step filtering procedure. First, we used a fuzzy matching[58](/articles/s41538-025-00680-9#ref-CR58 "Navarro, G. A guided tour to approximate string matching. ACM Comput. Surv. 33, 31–88 (2001).") technique to keep only sentences containing one of the food terms described in the last section, resulting in about 10 million sentences mentioning food terms. Second, we fine\-tuned a large language model, BioBERT[16](/articles/s41538-025-00680-9#ref-CR16 "Lee, J. et al. BioBERT: a pre-trained biomedical language representation model for biomedical text mining. Bioinformatics 36, 1234–1240 (2020)."), to classify sentences that contain valid food–chemical associations. This process resulted in 773,366 sentences that were highly likely (*p* \> 0\.9\) to contain food–chemical associations. More details can be found in Supplementary Note [1\.1](/articles/s41538-025-00680-9#MOESM1).

### Association extraction

For sentences that indicated food–chemical associations following the filtering step above, we passed those with a probability greater than 90% to the large language model\-based information extraction models. We compared the performance of two different models: OpenAI GPT\-4[59](/articles/s41538-025-00680-9#ref-CR59 "OpenAI et al. GPT-4 technical report. Preprint at 
                  https://doi.org/10.48550/arXiv.2303.08774
                  
                 (2024).") (Model ID: gpt\-4\-0613\) and GPT\-3\.5[60](/articles/s41538-025-00680-9#ref-CR60 "Ye, J. et al. A comprehensive capability analysis of GPT-3 and GPT-3.5 series models. Preprint at 
                  https://doi.org/10.48550/arXiv.2303.10420
                  
                 (2023).") with in\-context learning or fine\-tuning. For both models, we extracted food, food parts, chemicals, and chemical concentrations. For example, the sentence, *“Chinese cabbage leaves contain Ca (1020 g kg\-1 FW), Fe (26 g kg\-1 FW), and total glucosinolates (10\.926 micromol g\-1 DW),”* would result in the following three tuple extraction: *(Chinese cabbage, leaves, Ca, 1020 g kg\-1 FW)*, *(Chinese cabbage, leaves, Fe, 26 g kg\-1 FW)*, and *(Chinese cabbage, leaves, total glucosinolates, 10\.926 micromol g\-1 DW)*. We provided more details in Supplementary Note [1\.1](/articles/s41538-025-00680-9#MOESM1).

### Fine\-tuning of GPT models using annotation rules

To improve the accuracy and specificity of extracted data, we fine\-tuned the GPT\-3\.5 (Model ID: gpt\-3\.5\-turbo\-0125\) model with a dataset curated based on an extensive set of annotation rules. We have two annotators label the same sentences independently and consolidate the disagreement. These rules were designed and validated through the analysis of over 1780 sentences containing food and chemical information. Specifically, we extracted the information in the format: *({food}, {food part}, {chemical compound}, {chemical concentration}*) by following key principles: First, extracting information exactly as presented in sentences to ensure fidelity. Second, annotating the most specific entities, such as individual compounds rather than broader chemical groups or food species, instead of generalized categories. Third, preserving contextual modifiers, such as adjectives and processing descriptors (e.g., “aqueous extract of Mentha aquatica”).

Fine\-tuning focused on enhancing the model’s ability to handle complex entity structures and relationships. For instance, sentences describing chemical concentrations within specific food parts (e.g., “celery leaves contain phenols”) were annotated to reflect both the food entity and its part. Additionally, cases involving synonyms, acronyms, and hierarchical relationships (e.g., “blueberry extract \| Vaccinium angustifolium extract”) were fine\-tuned to prioritize professional terminology and ensure completeness.

The fine\-tuned models were trained to generate outputs in a structured format suitable for integration into the FAKG. Validation metrics, including precision, recall, and F1 scores, demonstrated significant improvements over baseline models, particularly in extracting nuanced relationships and rare descriptors. Supplementary Note [1\.1](/articles/s41538-025-00680-9#MOESM1) shows the details for our fine\-tuned model.

### Knowledge graph construction

Our FoodAtlas knowledge graph (FAKG) was formed by a set of (*{food}*, contains, *{chemical}*)\-triplets. Each entity can be a food or a chemical, indexed by a unique FoodAtlas ID and other identifiers (e.g., FoodOn IDs for food and PubChem CIDs for chemical entities). Each *contains*\-triplet is associated with metadata, providing additional information, including chemical concentration and references to the source where the information was extracted. To scalably expand FAKG, we developed a KG construction pipeline that harmonized and ingested the data extracted by the GPT models into the knowledge graph. First, the pipeline processed the CSV\-formatted outputs from the LLM, discarding a few with incorrect CSV format. Second, chemical concentration information in the raw\-string format was parsed into concentration value\-unit pairs using regular expressions. The units convertible to each other were unified into a standardized unit, such as ‘g,’ ‘mg,’ ‘gram,’ and ‘kg,’ which were all converted into ‘100 g’ with corresponding changes in concentration value. Third, an entity linking system performed synonym resolution and string matching, mapping food and chemical names mentioned in sentences to ontology databases FoodOn[11](/articles/s41538-025-00680-9#ref-CR11 "Dooley, D. M. et al. FoodOn: a harmonized food ontology to increase global food traceability, quality control and data integration. Npj Sci. Food 2, 23 (2018).") and ChEBI[52](/articles/s41538-025-00680-9#ref-CR52 "Hastings, J. et al. ChEBI in 2016: improved services and an expanding collection of metabolites. Nucleic Acids Res. 44, D1214–D1219 (2016)."), respectively. To enrich the interoperability and categorizability, identifiers from several other databases were retrieved (Supplementary Fig. [1](/articles/s41538-025-00680-9#MOESM1) and Supplementary Note [1\.2](/articles/s41538-025-00680-9#MOESM1), [1\.3](/articles/s41538-025-00680-9#MOESM1)).

### Integration of disease data from the Comparative Toxicogenomics Database (CTD)

To enrich the FoodAtlas Knowledge Graph (FAKG) with disease\-related data, we integrated chemical–disease associations from the Comparative Toxicogenomics Database (CTD)[61](/articles/s41538-025-00680-9#ref-CR61 "Davis, A. P., Wiegers, T. C., Rosenstein, M. C. & Mattingly, C. J. MEDIC: a practical disease vocabulary used at the Comparative Toxicogenomics Database. Database J. Biol. Databases Curation 2012, bar065 (2012)."). The CTD provides a robust dataset detailing relationships between chemicals and diseases and contains critical fields such as ChemicalName, ChemicalID (MeSH[62](/articles/s41538-025-00680-9#ref-CR62 "Dhammi, I. K. & Kumar, S. Medical subject headings (MeSH) terms. Indian J. Orthop. 48, 443–444 (2014).") identifier), DiseaseName, DiseaseID (MeSH or OMIM[63](/articles/s41538-025-00680-9#ref-CR63 "Hamosh, A., Scott, A. F., Amberger, J. S., Bocchini, C. A. & McKusick, V. A. Online Mendelian Inheritance in Man (OMIM), a knowledgebase of human genes and genetic disorders. Nucleic Acids Res. 33, D514–D517 (2005).") identifier), DirectEvidence (whether the chemical is a therapeutic or marker/mechanism for the disease, which we map as treats or worsens the disease, respectively), InferenceGeneSymbol, InferenceScore, and PubMedIDs (a \|\-delimited list of references).

We began by mapping the CTD chemicals to FoodAtlas using the ChemicalID field, which corresponds to MeSH identifiers. This alignment allowed us to cross\-reference chemical entities in FoodAtlas with their associated diseases as recorded in CTD. Once the mappings were established, we extracted relationships of the type (chemical, associated with, disease) and populated the knowledge graph with these connections. The integration included metadata for these relationships, such as the original ChemicaIDs and DiseaseIDs found in CTD for the relationship, and whether the chemical exists in foods in FoodAtlas. Additionally, the linked PubMedIDs and their corresponding PMCIDs were incorporated as references to enhance the verifiability and provenance of the data. For the diseases in these relationships, we extracted the DiseaseName, DiseaseID, AltDiseaseIDs (MeSH, OMIM, or DiseaseOntology identifiers), and the list of synonyms from CTD’s disease information to create our FoodAtlas disease entities and their relationships to chemicals (Supplementary Note [1\.3](/articles/s41538-025-00680-9#MOESM1)).

### Integration of flavor data from FlavorDB and PubChem

Chemicals in FlavorDB are indexed using PubChem IDs, allowing for straightforward alignment with existing FoodAtlas entities. We scraped FlavorDB, iterating through PubChem IDs of FoodAtlas chemicals, and retrieving structured JSON data for each chemical. For chemicals missing from FlavorDB, we extended flavor data collection to PubChem’s Hazardous Substances Data Bank (HSDB)[21](/articles/s41538-025-00680-9#ref-CR21 "Fonger, G. C. Hazardous substances data bank (HSDB) as a source of environmental fate information on chemicals. Toxicology 103, 137–145 (1995)."), extracting “Taste” and “Odor” descriptors. While PubChem provided a significant volume of additional data, its descriptors were often noisy and inconsistently formatted. Hence, fuzzy string matching techniques[58](/articles/s41538-025-00680-9#ref-CR58 "Navarro, G. A guided tour to approximate string matching. ACM Comput. Surv. 33, 31–88 (2001).") (Supplementary Note [1\.2](/articles/s41538-025-00680-9#MOESM1)) were employed to harmonize flavor descriptors, creating a unified set of standardized flavor terms. Each unique flavor descriptor was represented in the knowledge graph as an entity with the entity type flavor, and relationships between chemicals and their flavors were established using a newly defined *hasFlavor* relationship (Supplementary Note [1\.3](/articles/s41538-025-00680-9#MOESM1)).

### Integration of food and chemical bioactivity via Bioactivity Prediction Model

To integrate chemical bioactivity with food composition data in the FAKG, we employed a multi\-step procedure for both data assembly and model development using machine learning. First, we mapped chemicals present in FA to corresponding records in the ChEMBL database[64](/articles/s41538-025-00680-9#ref-CR64 "Zdrazil, B. et al. The ChEMBL Database in 2023: a drug discovery platform spanning multiple bioactivity data types and time periods. Nucleic Acids Res. 52, D1180–D1192 (2024)."), using InChIKey identifiers as the primary linkage. This allowed us to retrieve chemical pChEMBL values (i.e., –log10(nM)) for the related assays that capture various types of bioactivity, including antioxidant, antimicrobial, anti\-inflammatory, immunomodulatory, antiviral, neuroprotective, anticancer, and antidiabetic activities (Supplementary Note [1\.5](/articles/s41538-025-00680-9#MOESM1)). After establishing the connections between chemicals in FA and their associated assays in ChEMBL, we linked each food to its constituent chemicals using concentration data available in FA. The resulting dataset enabled the formation of a Bioactivity Food Link (BFL), whereby each food inherited potential bioactivity from the chemicals it contains. This dataset was further enriched by including the Ferric Reducing Antioxidant Power (FRAP) values[65](/articles/s41538-025-00680-9#ref-CR65 "Carlsen, M. H. et al. The total antioxidant content of more than 3100 foods, beverages, spices, herbs and supplements used worldwide. Nutr. J. 9, 3 (2010).") for 159 food samples, providing ground truth for antioxidant capacity. The resulting Bioactivity Prediction Model (BPM) was designed to predict antioxidant capacity, quantified as –log10(FRAP), based on a machine learning architecture, Random Forest. The model relies on three primary input modalities. First, we generated Morgan fingerprints from SMILES strings using RDKit[66](/articles/s41538-025-00680-9#ref-CR66 "Laufkötter, O., Sturm, N., Bajorath, J., Chen, H. & Engkvist, O. Combining structural and bioactivity-based fingerprints improves prediction performance and scaffold hopping capability. J. Cheminformatics 11, 54 (2019)."), encoding chemical structure as a binary vector. Second, we included pChEMBL values[67](/articles/s41538-025-00680-9#ref-CR67 "Lenselink, E. B. et al. Beyond the hype: deep neural networks outperform established methods using a ChEMBL bioactivity benchmark set. J. Cheminformatics 9, 45 (2017)."), which reflect comparable measures of concentrations to reach half\-maximal potency/affinity/response (e.g., IC50, EC50\) on a negative logarithmic scale. Third, we incorporated chemical concentration information from FA to capture the quantity of each chemical present in a given food. These three types of inputs were fed into machine learning models. Outputs from the model predicted –log10(FRAP) for each food. During model training, we employed an 80:20 train\-test split, which we repeated across 25 bootstrap iterations to account for variability due to the limited dataset size. The Random Forest was tuned using a hyperparameter grid search. We tracked metrics such as mean absolute error (MAE), MSE, Pearson’s correlation (PCC), and the coefficient of determination (*R*²) between predicted and observed FRAP values. Residual analysis was used to gauge systematic errors and to verify the stability of predictions across foods with diverse chemical profiles (Supplementary Note [1\.5](/articles/s41538-025-00680-9#MOESM1)).

### One\-hop food substitutions for disease\- and antioxidant bioactivity\-oriented diet improvement

We implemented a one\-hop substitution framework to evaluate and enhance the healthfulness of real\-world meals by jointly optimizing disease\-risk and antioxidant\-bioactivity profiles. First, we ingested the USDA “What We Eat in America” (WWEIA) diet recall data[68](/articles/s41538-025-00680-9#ref-CR68 "What We Eat In America (WWEIA) Database. Food Surveys Research Group 
                  https://doi.org/10.15482/USDA.ADC/1178144
                  
                 (2015)."), extracting each meal’s constituent foods and their portion sizes. For disease modeling, we mapped foods to associated conditions (e.g., cardiovascular, inflammatory) using curated chemical–disease relationships from the CTD. In parallel, we assigned antioxidant bioactivity scores derived from FRAP assays. To enable direct comparison and aggregation across disparate metrics, both disease\-risk and bioactivity scores were min\-max normalized between 0 and 1\. We then computed a weighted aggregate score for each meal by summing individual food contributions in proportion to their serving size. Next, we identified “high\-impact” foods, those whose removal yielded the greatest disease\-risk reduction, and generated candidate alternatives drawn from the same primary food category (e.g., dairy, leafy greens). For each candidate swap, we recomputed the meal’s composite disease and antioxidant scores under the same portion\-weighted scheme. Substitutions that produced the maximal net benefit, minimizing normalized disease risk while maximizing normalized antioxidant activity, were selected as optimal (Supplementary Note [1\.6](/articles/s41538-025-00680-9#MOESM1)).




## Data availability


All data is available at [https://github.com/IBPA/FoodAtlas\-KGv2](https://github.com/IBPA/FoodAtlas-KGv2) and <https://foodatlas.ai>. Food Atlas may be using data that are restricted licenses for different uses, please consult individual license terms from each data source. *CTD compliance*. FoodAtlas integrates curated knowledge from the Comparative Toxicogenomics Database (CTD) by linking to CTD chemical/disease identifiers and PubMed references; we do not redistribute CTD\-curated interaction tables in our public releases. Users can reproduce the CTD integration locally using our scripts, which download CTD data from the source and join via CTD IDs and PMIDs. Non\-commercial use is free; commercial reuse requires a license from CTD’s licensing agent. Please consult CTD’s terms before downloading/using CTD content.


## Code availability


All code and instructions on how to reproduce the results for knowledge graph construction and information extraction can be found at [https://github.com/IBPA/FoodAtlas\-KGv2](https://github.com/IBPA/FoodAtlas-KGv2) and <https://github.com/IBPA/Lit2KG>, respectively.


## References

1. Allot, A. et al. LitSense: making sense of biomedical literature at sentence level. *Nucleic Acids Res.* **47**, W594–W599 (2019\).

[Article](https://doi.org/10.1093%2Fnar%2Fgkz289) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3cXktVyitbs%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31020319) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6602490) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=LitSense%3A%20making%20sense%20of%20biomedical%20literature%20at%20sentence%20level&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgkz289&volume=47&pages=W594-W599&publication_year=2019&author=Allot%2CA)
2. Youn, J., Li, F., Simmons, G., Kim, S. \& Tagkopoulos, I. FoodAtlas: automated knowledge extraction of food and chemicals from literature. *Comput. Biol. Med.* **181**, 109072 (2024\).

[Article](https://doi.org/10.1016%2Fj.compbiomed.2024.109072) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2cXhvVOls7bI) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=39216404) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=FoodAtlas%3A%20automated%20knowledge%20extraction%20of%20food%20and%20chemicals%20from%20literature&journal=Comput.%20Biol.%20Med.&doi=10.1016%2Fj.compbiomed.2024.109072&volume=181&publication_year=2024&author=Youn%2CJ&author=Li%2CF&author=Simmons%2CG&author=Kim%2CS&author=Tagkopoulos%2CI)
3. Cifuentes, A. Food analysis and foodomics. *J. Chromatogr. A* **1216**, 7109 (2009\).

[Article](https://doi.org/10.1016%2Fj.chroma.2009.09.018) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BD1MXht1WntLfI) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=19765718) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Food%20analysis%20and%20foodomics&journal=J.%20Chromatogr.%20A&doi=10.1016%2Fj.chroma.2009.09.018&volume=1216&publication_year=2009&author=Cifuentes%2CA)
4. García\-Cañas, V., Simó, C., Herrero, M., Ibáñez, E. \& Cifuentes, A. Present and future challenges in food analysis: foodomics. *Anal. Chem.* **84**, 10150–10159 (2012\).

[Article](https://doi.org/10.1021%2Fac301680q) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=22958185) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Present%20and%20future%20challenges%20in%20food%20analysis%3A%20foodomics&journal=Anal.%20Chem.&doi=10.1021%2Fac301680q&volume=84&pages=10150-10159&publication_year=2012&author=Garc%C3%ADa-Ca%C3%B1as%2CV&author=Sim%C3%B3%2CC&author=Herrero%2CM&author=Ib%C3%A1%C3%B1ez%2CE&author=Cifuentes%2CA)
5. FooDB. <https://foodb.ca/>. \[Accessed at 12/25/2025]
6. McKillop, K., Harnly, J., Pehrsson, P., Fukagawa, N. \& Finley, J. FoodData Central, USDA’s updated approach to food composition data systems. *Curr. Dev. Nutr.* **5**, 596–596 (2021\).

[Article](https://doi.org/10.1093%2Fcdn%2Fnzab044_027) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8182005) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=FoodData%20Central%2C%20USDA%E2%80%99s%20updated%20approach%20to%20food%20composition%20data%20systems&journal=Curr.%20Dev.%20Nutr.&doi=10.1093%2Fcdn%2Fnzab044_027&volume=5&pages=596-596&publication_year=2021&author=McKillop%2CK&author=Harnly%2CJ&author=Pehrsson%2CP&author=Fukagawa%2CN&author=Finley%2CJ)
7. USDA FoodData Central. <https://fdc.nal.usda.gov/>. \[Accessed at 12/25/2025]
8. Capozzi, F. \& Bordoni, A. Foodomics: a new comprehensive approach to food and nutrition. *Genes Nutr.* **8**, 1–4 (2013\).

[Article](https://link.springer.com/doi/10.1007/s12263-012-0310-x) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3sXkt1ylug%3D%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=22933238) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Foodomics%3A%20a%20new%20comprehensive%20approach%20to%20food%20and%20nutrition&journal=Genes%20Nutr.&doi=10.1007%2Fs12263-012-0310-x&volume=8&pages=1-4&publication_year=2013&author=Capozzi%2CF&author=Bordoni%2CA)
9. Min, W., Liu, C., Xu, L. \& Jiang, S. Applications of knowledge graphs for food science and industry. *Patterns* **3**, 100484 (2022\).

[Article](https://doi.org/10.1016%2Fj.patter.2022.100484) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=35607620) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC9122965) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Applications%20of%20knowledge%20graphs%20for%20food%20science%20and%20industry&journal=Patterns&doi=10.1016%2Fj.patter.2022.100484&volume=3&publication_year=2022&author=Min%2CW&author=Liu%2CC&author=Xu%2CL&author=Jiang%2CS)
10. Jahangir, M., Kim, H. K., Choi, Y. H. \& Verpoorte, R. Health\-affecting compounds in *Brassicaceae*. *Compr. Rev. Food Sci. Food Saf.* **8**, 31–43 (2009\).

[Article](https://doi.org/10.1111%2Fj.1541-4337.2008.00065.x) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3cXnsFOlsL4%3D) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Health-affecting%20compounds%20in%20Brassicaceae&journal=Compr.%20Rev.%20Food%20Sci.%20Food%20Saf.&doi=10.1111%2Fj.1541-4337.2008.00065.x&volume=8&pages=31-43&publication_year=2009&author=Jahangir%2CM&author=Kim%2CHK&author=Choi%2CYH&author=Verpoorte%2CR)
11. Dooley, D. M. et al. FoodOn: a harmonized food ontology to increase global food traceability, quality control and data integration. *Npj Sci. Food* **2**, 23 (2018\).

[Article](https://doi.org/10.1038%2Fs41538-018-0032-6) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31304272) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6550238) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=FoodOn%3A%20a%20harmonized%20food%20ontology%20to%20increase%20global%20food%20traceability%2C%20quality%20control%20and%20data%20integration&journal=Npj%20Sci.%20Food&doi=10.1038%2Fs41538-018-0032-6&volume=2&publication_year=2018&author=Dooley%2CDM)
12. Eftimov, T., Ispirova, G., Potočnik, D., Ogrinc, N. \& Koroušić Seljak, B. ISO\-FOOD ontology: a formal representation of the knowledge within the domain of isotopes for food science. *Food Chem.* **277**, 382–390 (2019\).

[Article](https://doi.org/10.1016%2Fj.foodchem.2018.10.118) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC1cXitVGksbrN) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=30502161) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=ISO-FOOD%20ontology%3A%20a%20formal%20representation%20of%20the%20knowledge%20within%20the%20domain%20of%20isotopes%20for%20food%20science&journal=Food%20Chem.&doi=10.1016%2Fj.foodchem.2018.10.118&volume=277&pages=382-390&publication_year=2019&author=Eftimov%2CT&author=Ispirova%2CG&author=Poto%C4%8Dnik%2CD&author=Ogrinc%2CN&author=Korou%C5%A1i%C4%87%20Seljak%2CB)
13. Furukawa H. Deep Learning for End\-to\-End Automatic Target Recognition from Synthetic Aperture Radar Imagery. IEICE Technical Report; IEICE Tech. Rep. **117**, 35–40 (2018\).
14. Devlin, J., Chang, M\-W., Lee, K. \& Toutanova, K. BERT: Pre\-training of Deep BidirectionalTransformers for Language Understanding. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pages 4171–4186, Minneapolis, Minnesota. Association for Computational Linguistics. (2019\).
15. Vaswani, A. et al. Attention is all you need. Advances in neural information processing systems, 30\. [https://doi.org/10\.48550/arXiv.1706\.03762](https://doi.org/10.48550/arXiv.1706.03762) (2017\).
16. Lee, J. et al. BioBERT: a pre\-trained biomedical language representation model for biomedical text mining. *Bioinformatics* **36**, 1234–1240 (2020\).

[Article](https://doi.org/10.1093%2Fbioinformatics%2Fbtz682) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3cXhslCisLrL) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31501885) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=BioBERT%3A%20a%20pre-trained%20biomedical%20language%20representation%20model%20for%20biomedical%20text%20mining&journal=Bioinformatics&doi=10.1093%2Fbioinformatics%2Fbtz682&volume=36&pages=1234-1240&publication_year=2020&author=Lee%2CJ)
17. Cenikj, G., Seljak, B. K. \& Eftimov, T. FoodChem: A food\-chemical relation extraction model. In 2021IEEE Symposium Series on Computational Intelligence (SSCI) (pp. 1\-8\). IEEE. (2021\).
18. Özen, N., Mu, W., van Asselt, ED. \& van den Bulk, LM. Extracting chemical food safety hazards from the scientific literature automatically using large language models. *Appl. Food Res.* **5**, 100679, [https://doi.org/10\.1016/j.afres.2024\.100679](https://doi.org/10.1016/j.afres.2024.100679) (2025\).

[Article](https://doi.org/10.1016%2Fj.afres.2024.100679) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2MXhtVGkt7g%3D) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Extracting%20chemical%20food%20safety%20hazards%20from%20the%20scientific%20literature%20automatically%20using%20large%20language%20models&journal=Appl.%20Food%20Res.&doi=10.1016%2Fj.afres.2024.100679&volume=5&publication_year=2025&author=%C3%96zen%2CN&author=Mu%2CW&author=van%20Asselt%2CED&author=van%20den%20Bulk%2CLM)
19. Davis, A. P. et al. Comparative Toxicogenomics Database’s 20th anniversary: update 2025\. *Nucleic Acids Res.* **53**, D1328–D1334 (2025\).

[Article](https://doi.org/10.1093%2Fnar%2Fgkae883) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB28Xhs1ehsrY%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=39385618) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Comparative%20Toxicogenomics%20Database%E2%80%99s%2020th%20anniversary%3A%20update%202025&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgkae883&volume=53&pages=D1328-D1334&publication_year=2025&author=Davis%2CAP)
20. FlavorDB: a database of flavor molecules \| Nucleic Acids Research \| Oxford Academic. <https://academic.oup.com/nar/article/46/D1/D1210/4559748>.
21. Fonger, G. C. Hazardous substances data bank (HSDB) as a source of environmental fate information on chemicals. *Toxicology* **103**, 137–145 (1995\).

[Article](https://doi.org/10.1016%2F0300-483X%2895%2903145-6) 
 [CAS](/articles/cas-redirect/1:CAS:528:DyaK2MXovVylsLc%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=8545846) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Hazardous%20substances%20data%20bank%20%28HSDB%29%20as%20a%20source%20of%20environmental%20fate%20information%20on%20chemicals&journal=Toxicology&doi=10.1016%2F0300-483X%2895%2903145-6&volume=103&pages=137-145&publication_year=1995&author=Fonger%2CGC)
22. Haussmann, S. et al. FoodKG: a semantics\-driven knowledge graph for food recommendation. In *The Semantic Web – ISWC 2019* (eds Ghidini, C. et al.) Vol. 11779 146–162 (Springer International Publishing, Cham, 2019\).
23. Park, D., Kim, K., Kim, S., Spranger, M. \& Kang, J. FlavorGraph: a large\-scale food\-chemical graph for generating food representations and recommending food pairings. *Sci. Rep.* **11**, 931 (2021\).

[Article](https://doi.org/10.1038%2Fs41598-020-79422-8) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3MXhsVOit7k%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33441585) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7806805) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=FlavorGraph%3A%20a%20large-scale%20food-chemical%20graph%20for%20generating%20food%20representations%20and%20recommending%20food%20pairings&journal=Sci.%20Rep.&doi=10.1038%2Fs41598-020-79422-8&volume=11&publication_year=2021&author=Park%2CD&author=Kim%2CK&author=Kim%2CS&author=Spranger%2CM&author=Kang%2CJ)
24. Ni, Y., Jensen, K., Kouskoumvekaki, I. \& Panagiotou, G. NutriChem 2\.0: exploring the effect of plant\-based foods on human health and drug efficacy. *Database* **2017**, bax044 (2017\).

[Article](https://doi.org/10.1093%2Fdatabase%2Fbax044) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=29220436) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5502356) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=NutriChem%202.0%3A%20exploring%20the%20effect%20of%20plant-based%20foods%20on%20human%20health%20and%20drug%20efficacy&journal=Database&doi=10.1093%2Fdatabase%2Fbax044&volume=2017&publication_year=2017&author=Ni%2CY&author=Jensen%2CK&author=Kouskoumvekaki%2CI&author=Panagiotou%2CG)
25. van der Maaten, L. \& Hinton, G. Visualizing data using t\-SNE. *J. Mach. Learn. Res.* **9**, 2579–2605 (2008\).

[Google Scholar](http://scholar.google.com/scholar_lookup?&title=Visualizing%20data%20using%20t-SNE&journal=J.%20Mach.%20Learn.%20Res.&volume=9&pages=2579-2605&publication_year=2008&author=Maaten%2CL&author=Hinton%2CG)
26. McInnes, L., Healy, J. \& Astels, S. hdbscan: hierarchical density based clustering. *J. Open Source Softw.* **2**, 205 (2017\).

[Article](https://doi.org/10.21105%2Fjoss.00205) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=hdbscan%3A%20hierarchical%20density%20based%20clustering&journal=J.%20Open%20Source%20Softw.&doi=10.21105%2Fjoss.00205&volume=2&publication_year=2017&author=McInnes%2CL&author=Healy%2CJ&author=Astels%2CS)
27. Mullahy, J. Specification and testing of some modified count data models. *J. Econom.* **33**, 341–365 (1986\).

[Article](https://doi.org/10.1016%2F0304-4076%2886%2990002-3) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Specification%20and%20testing%20of%20some%20modified%20count%20data%20models&journal=J.%20Econom.&doi=10.1016%2F0304-4076%2886%2990002-3&volume=33&pages=341-365&publication_year=1986&author=Mullahy%2CJ)
28. Benjamini, Y. \& Hochberg, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J. R. Stat. Soc. Ser. B Methodol.* **57**, 289–300 (1995\).

[Article](https://doi.org/10.1111%2Fj.2517-6161.1995.tb02031.x) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Controlling%20the%20false%20discovery%20rate%3A%20a%20practical%20and%20powerful%20approach%20to%20multiple%20testing&journal=J.%20R.%20Stat.%20Soc.%20Ser.%20B%20Methodol.&doi=10.1111%2Fj.2517-6161.1995.tb02031.x&volume=57&pages=289-300&publication_year=1995&author=Benjamini%2CY&author=Hochberg%2CY)
29. Johnson, G. H. \& Fritsche, K. Effect of dietary linoleic acid on markers of inflammation in healthy persons: a systematic review of randomized controlled trials. *J. Acad. Nutr. Diet.* **112**, 1041\.e1–15 (2012\).

[Article](https://doi.org/10.1016%2Fj.jand.2012.03.029) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Effect%20of%20dietary%20linoleic%20acid%20on%20markers%20of%20inflammation%20in%20healthy%20persons%3A%20a%20systematic%20review%20of%20randomized%20controlled%20trials&journal=J.%20Acad.%20Nutr.%20Diet.&doi=10.1016%2Fj.jand.2012.03.029&volume=112&pages=1041.e1-15&publication_year=2012&author=Johnson%2CGH&author=Fritsche%2CK)
30. Crowell, P. L. Prevention and therapy of cancer by dietary monoterpenes. *J. Nutr.* **129**, 775S–778S (1999\).

[Article](https://doi.org/10.1093%2Fjn%2F129.3.775S) 
 [CAS](/articles/cas-redirect/1:STN:280:DyaK1M7osFCmsA%3D%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=10082788) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Prevention%20and%20therapy%20of%20cancer%20by%20dietary%20monoterpenes&journal=J.%20Nutr.&doi=10.1093%2Fjn%2F129.3.775S&volume=129&pages=775S-778S&publication_year=1999&author=Crowell%2CPL)
31. Benzie, I. F. F. \& Choi, S.\-W. Chapter One \- Antioxidants in food: content, measurement, significance, action, cautions, caveats, and research needs. In *Advances in Food and Nutrition Research* (ed. Henry, J.) Vol. 71 1–53 (Academic Press, 2014\).
32. Shahidi, F. \& Ambigaipalan, P. Phenolics and polyphenolics in foods, beverages and spices: antioxidant activity and health effects – A review. *J. Funct. Foods* **18**, 820–897 (2015\).

[Article](https://doi.org/10.1016%2Fj.jff.2015.06.018) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC2MXhtFWgt7vN) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Phenolics%20and%20polyphenolics%20in%20foods%2C%20beverages%20and%20spices%3A%20antioxidant%20activity%20and%20health%20effects%20%E2%80%93%20A%20review&journal=J.%20Funct.%20Foods&doi=10.1016%2Fj.jff.2015.06.018&volume=18&pages=820-897&publication_year=2015&author=Shahidi%2CF&author=Ambigaipalan%2CP)
33. Chang, J., Wang, H., Su, W., He, X. \& Tan, M. Artificial intelligence in food bioactive peptides screening: recent advances and future prospects. *Trends Food Sci. Technol.* **156**, 104845 (2025\).

[Article](https://doi.org/10.1016%2Fj.tifs.2024.104845) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2cXivVWntbnE) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Artificial%20intelligence%20in%20food%20bioactive%20peptides%20screening%3A%20recent%20advances%20and%20future%20prospects&journal=Trends%20Food%20Sci.%20Technol.&doi=10.1016%2Fj.tifs.2024.104845&volume=156&publication_year=2025&author=Chang%2CJ&author=Wang%2CH&author=Su%2CW&author=He%2CX&author=Tan%2CM)
34. Alvarez\-Leite, J. I. The role of bioactive compounds in human health and disease. *Nutrients* **17**, 1170 (2025\).

[Article](https://doi.org/10.3390%2Fnu17071170) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=40218927) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC11990537) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20role%20of%20bioactive%20compounds%20in%20human%20health%20and%20disease&journal=Nutrients&doi=10.3390%2Fnu17071170&volume=17&publication_year=2025&author=Alvarez-Leite%2CJI)
35. GPT\-5 System Card. [https://openai.com/index/gpt\-5\-system\-card/](https://openai.com/index/gpt-5-system-card/) (2025\).
36. Zhang, Z. et al. Multimodal chain\-of\-thought reasoning in language models. [https://openreview.net/forum?id\=gDlsMWost9](https://openreview.net/forum?id=gDlsMWost9) (2023\).
37. Liu, M. X. et al. ‘We Need Structured Output’: towards user\-centered constraints on large language model output. In *Extended Abstracts of the CHI Conference on Human Factors in Computing Systems* 1–9 (Association for Computing Machinery, New York, NY, USA, 2024\).
38. Lu, W. et al. Large language model for table processing: a survey. *Front. Comput. Sci.* **19**, 192350 (2025\).

[Article](https://link.springer.com/doi/10.1007/s11704-024-40763-6) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Large%20language%20model%20for%20table%20processing%3A%20a%20survey&journal=Front.%20Comput.%20Sci.&doi=10.1007%2Fs11704-024-40763-6&volume=19&publication_year=2025&author=Lu%2CW)
39. Li, F., Youn, J., Millsop, C. \& Tagkopoulos, I. Predicting clinical trial success for Clostridium difficile infections based on preclinical data. *Front. Artif. Intell.* 710\.3389/frai.2024\.1487335 (2024\).
40. Ren, P. et al. A survey of deep active learning. *ACM Comput. Surv.* **54**, 180:1\-180:40 (2021\).
41. Foster\-Powell, K., Holt, S. H. \& Brand\-Miller, J. C. International table of glycemic index and glycemic load values: 2002\. *Am. J. Clin. Nutr.* **76**, 5–56 (2002\).

[Article](https://doi.org/10.1093%2Fajcn%2F76.1.5) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BD38XltVyhtbY%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=12081815) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=International%20table%20of%20glycemic%20index%20and%20glycemic%20load%20values%3A%202002&journal=Am.%20J.%20Clin.%20Nutr.&doi=10.1093%2Fajcn%2F76.1.5&volume=76&pages=5-56&publication_year=2002&author=Foster-Powell%2CK&author=Holt%2CSH&author=Brand-Miller%2CJC)
42. Shivappa, N., Steck, S. E., Hurley, T. G., Hussey, J. R. \& Hébert, J. R. Designing and developing a literature\-derived, population\-based dietary inflammatory index. *Public Health Nutr.* **17**, 1689–1696 (2014\).

[Article](https://doi.org/10.1017%2FS1368980013002115) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=23941862) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Designing%20and%20developing%20a%20literature-derived%2C%20population-based%20dietary%20inflammatory%20index&journal=Public%20Health%20Nutr.&doi=10.1017%2FS1368980013002115&volume=17&pages=1689-1696&publication_year=2014&author=Shivappa%2CN&author=Steck%2CSE&author=Hurley%2CTG&author=Hussey%2CJR&author=H%C3%A9bert%2CJR)
43. Toro, S. et al. Dynamic Retrieval Augmented Generation of Ontologies using Artificial Intelligence (DRAGON\-AI). *J. Biomed. Semant.* **15**, 19 (2024\).

[Article](https://link.springer.com/doi/10.1186/s13326-024-00320-3) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Dynamic%20Retrieval%20Augmented%20Generation%20of%20Ontologies%20using%20Artificial%20Intelligence%20%28DRAGON-AI%29&journal=J.%20Biomed.%20Semant.&doi=10.1186%2Fs13326-024-00320-3&volume=15&publication_year=2024&author=Toro%2CS)
44. Youn, J., Naravane, T. \& Tagkopoulos, I. Using Word Embeddings to Learn a Better Food Ontology. *Front. Artif. Intell.* 310\.3389/frai.2020\.584784\. (2020\).
45. Jacobs, D. R. Jr \& Tapsell, L. C. Food synergy: the key to a healthy diet. *Proc. Nutr. Soc.* **72**, 200–206 (2013\).

[Article](https://doi.org/10.1017%2FS0029665112003011) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=23312372) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Food%20synergy%3A%20the%20key%20to%20a%20healthy%20diet&journal=Proc.%20Nutr.%20Soc.&doi=10.1017%2FS0029665112003011&volume=72&pages=200-206&publication_year=2013&author=Jacobs%2CDR&author=Tapsell%2CLC)
46. Nemec, K. Cultural awareness of eating patterns in the health care setting. *Clin. Liver Dis.* **16**, 204–207 (2020\).

[Article](https://doi.org/10.1002%2Fcld.1019) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Cultural%20awareness%20of%20eating%20patterns%20in%20the%20health%20care%20setting&journal=Clin.%20Liver%20Dis.&doi=10.1002%2Fcld.1019&volume=16&pages=204-207&publication_year=2020&author=Nemec%2CK)
47. Forde, C. G. \& de Graaf, K. Influence of sensory properties in moderating eating behaviors and food intake. *Front. Nutr.* **9**, 841444 (2022\).

[Article](https://doi.org/10.3389%2Ffnut.2022.841444) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=35265658) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8899294) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Influence%20of%20sensory%20properties%20in%20moderating%20eating%20behaviors%20and%20food%20intake&journal=Front.%20Nutr.&doi=10.3389%2Ffnut.2022.841444&volume=9&publication_year=2022&author=Forde%2CCG&author=de%20Graaf%2CK)
48. Melse\-Boonstra, A. Bioavailability of micronutrients from nutrient\-dense whole foods: zooming in on dairy, vegetables, and fruits. *Front. Nutr.* **7**, 101 (2020\).

[Article](https://doi.org/10.3389%2Ffnut.2020.00101) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32793622) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7393990) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Bioavailability%20of%20micronutrients%20from%20nutrient-dense%20whole%20foods%3A%20zooming%20in%20on%20dairy%2C%20vegetables%2C%20and%20fruits&journal=Front.%20Nutr.&doi=10.3389%2Ffnut.2020.00101&volume=7&publication_year=2020&author=Melse-Boonstra%2CA)
49. Benford, D. et al. The principles and methods behind EFSA’s guidance on uncertainty analysis in scientific assessment. *EFSA J* **16**, e05122 (2018\).

[PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32625670) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7009645) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20principles%20and%20methods%20behind%20EFSA%E2%80%99s%20guidance%20on%20uncertainty%20analysis%20in%20scientific%20assessment&journal=EFSA%20J&volume=16&publication_year=2018&author=Benford%2CD)
50. Shannar, A. et al. Pharmacodynamics (PD), pharmacokinetics (PK) and PK\-PD modeling of NRF2 activating dietary phytochemicals in cancer prevention and in health. *Curr. Pharmacol. Rep.* **11**, 6 (2024\).

[Article](https://link.springer.com/doi/10.1007/s40495-024-00388-6) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=39649473) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC11618211) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Pharmacodynamics%20%28PD%29%2C%20pharmacokinetics%20%28PK%29%20and%20PK-PD%20modeling%20of%20NRF2%20activating%20dietary%20phytochemicals%20in%20cancer%20prevention%20and%20in%20health&journal=Curr.%20Pharmacol.%20Rep.&doi=10.1007%2Fs40495-024-00388-6&volume=11&publication_year=2024&author=Shannar%2CA)
51. Vasilevsky, N. A. et al. Mondo: Unifying diseases for the world, by the world. Preprint at [https://doi.org/10\.1101/2022\.04\.13\.22273750](https://doi.org/10.1101/2022.04.13.22273750) (2022\).
52. Hastings, J. et al. ChEBI in 2016: improved services and an expanding collection of metabolites. *Nucleic Acids Res.* **44**, D1214–D1219 (2016\).

[Article](https://doi.org/10.1093%2Fnar%2Fgkv1031) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC2sXhtV2gu7bM) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=26467479) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=ChEBI%20in%202016%3A%20improved%20services%20and%20an%20expanding%20collection%20of%20metabolites&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgkv1031&volume=44&pages=D1214-D1219&publication_year=2016&author=Hastings%2CJ)
53. Kim, S. et al. PubChem 2023 update. *Nucleic Acids Res.* **51**, D1373–D1380 (2023\).

[Article](https://doi.org/10.1093%2Fnar%2Fgkac956) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=36305812) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=PubChem%202023%20update&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgkac956&volume=51&pages=D1373-D1380&publication_year=2023&author=Kim%2CS)
54. PubMed. *PubMed* <https://pubmed.ncbi.nlm.nih.gov/>. \[Accessed at 12/25/2025].
55. PubMed Central (PMC). *PubMed Central (PMC)* <https://pmc.ncbi.nlm.nih.gov/>. \[Accessed at 12/25/2025].
56. Kans, J. Entrez Direct: E\-utilities on the Unix Command Line. In *Entrez Programming Utilities Help \[Internet]* (National Center for Biotechnology Information (US), 2025\).
57. Bird, S. \& Loper, E. NLTK: The Natural Language Toolkit. In Proceedings of the ACL Interactive Poster and Demonstration Sessions, pages 214–217, Barcelona, Spain. Association for Computational Linguistics. (2004\).
58. Navarro, G. A guided tour to approximate string matching. *ACM Comput. Surv.* **33**, 31–88 (2001\).

[Article](https://doi.org/10.1145%2F375360.375365) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20guided%20tour%20to%20approximate%20string%20matching&journal=ACM%20Comput.%20Surv.&doi=10.1145%2F375360.375365&volume=33&pages=31-88&publication_year=2001&author=Navarro%2CG)
59. OpenAI et al. GPT\-4 technical report. Preprint at [https://doi.org/10\.48550/arXiv.2303\.08774](https://doi.org/10.48550/arXiv.2303.08774) (2024\).
60. Ye, J. et al. A comprehensive capability analysis of GPT\-3 and GPT\-3\.5 series models. Preprint at [https://doi.org/10\.48550/arXiv.2303\.10420](https://doi.org/10.48550/arXiv.2303.10420) (2023\).
61. Davis, A. P., Wiegers, T. C., Rosenstein, M. C. \& Mattingly, C. J. MEDIC: a practical disease vocabulary used at the Comparative Toxicogenomics Database. *Database J. Biol. Databases Curation* **2012**, bar065 (2012\).

[Google Scholar](http://scholar.google.com/scholar_lookup?&title=MEDIC%3A%20a%20practical%20disease%20vocabulary%20used%20at%20the%20Comparative%20Toxicogenomics%20Database&journal=Database%20J.%20Biol.%20Databases%20Curation&volume=2012&publication_year=2012&author=Davis%2CAP&author=Wiegers%2CTC&author=Rosenstein%2CMC&author=Mattingly%2CCJ)
62. Dhammi, I. K. \& Kumar, S. Medical subject headings (MeSH) terms. *Indian J. Orthop.* **48**, 443–444 (2014\).

[Article](https://doi.org/10.4103%2F0019-5413.139827) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=25298548) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4175855) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Medical%20subject%20headings%20%28MeSH%29%20terms&journal=Indian%20J.%20Orthop.&doi=10.4103%2F0019-5413.139827&volume=48&pages=443-444&publication_year=2014&author=Dhammi%2CIK&author=Kumar%2CS)
63. Hamosh, A., Scott, A. F., Amberger, J. S., Bocchini, C. A. \& McKusick, V. A. Online Mendelian Inheritance in Man (OMIM), a knowledgebase of human genes and genetic disorders. *Nucleic Acids Res.* **33**, D514–D517 (2005\).

[Article](https://doi.org/10.1093%2Fnar%2Fgki033) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BD2MXisVektA%3D%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=15608251) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Online%20Mendelian%20Inheritance%20in%20Man%20%28OMIM%29%2C%20a%20knowledgebase%20of%20human%20genes%20and%20genetic%20disorders&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgki033&volume=33&pages=D514-D517&publication_year=2005&author=Hamosh%2CA&author=Scott%2CAF&author=Amberger%2CJS&author=Bocchini%2CCA&author=McKusick%2CVA)
64. Zdrazil, B. et al. The ChEMBL Database in 2023: a drug discovery platform spanning multiple bioactivity data types and time periods. *Nucleic Acids Res.* **52**, D1180–D1192 (2024\).

[Article](https://doi.org/10.1093%2Fnar%2Fgkad1004) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2cXivVamt73L) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37933841) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20ChEMBL%20Database%20in%202023%3A%20a%20drug%20discovery%20platform%20spanning%20multiple%20bioactivity%20data%20types%20and%20time%20periods&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgkad1004&volume=52&pages=D1180-D1192&publication_year=2024&author=Zdrazil%2CB)
65. Carlsen, M. H. et al. The total antioxidant content of more than 3100 foods, beverages, spices, herbs and supplements used worldwide. *Nutr. J.* **9**, 3 (2010\).

[Article](https://link.springer.com/doi/10.1186/1475-2891-9-3) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=20096093) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2841576) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20total%20antioxidant%20content%20of%20more%20than%203100%20foods%2C%20beverages%2C%20spices%2C%20herbs%20and%20supplements%20used%20worldwide&journal=Nutr.%20J.&doi=10.1186%2F1475-2891-9-3&volume=9&publication_year=2010&author=Carlsen%2CMH)
66. Laufkötter, O., Sturm, N., Bajorath, J., Chen, H. \& Engkvist, O. Combining structural and bioactivity\-based fingerprints improves prediction performance and scaffold hopping capability. *J. Cheminformatics* **11**, 54 (2019\).

[Article](https://link.springer.com/doi/10.1186/s13321-019-0376-1) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Combining%20structural%20and%20bioactivity-based%20fingerprints%20improves%20prediction%20performance%20and%20scaffold%20hopping%20capability&journal=J.%20Cheminformatics&doi=10.1186%2Fs13321-019-0376-1&volume=11&publication_year=2019&author=Laufk%C3%B6tter%2CO&author=Sturm%2CN&author=Bajorath%2CJ&author=Chen%2CH&author=Engkvist%2CO)
67. Lenselink, E. B. et al. Beyond the hype: deep neural networks outperform established methods using a ChEMBL bioactivity benchmark set. *J. Cheminformatics* **9**, 45 (2017\).

[Article](https://link.springer.com/doi/10.1186/s13321-017-0232-0) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Beyond%20the%20hype%3A%20deep%20neural%20networks%20outperform%20established%20methods%20using%20a%20ChEMBL%20bioactivity%20benchmark%20set&journal=J.%20Cheminformatics&doi=10.1186%2Fs13321-017-0232-0&volume=9&publication_year=2017&author=Lenselink%2CEB)
68. What We Eat In America (WWEIA) Database. Food Surveys Research Group [https://doi.org/10\.15482/USDA.ADC/1178144](https://doi.org/10.15482/USDA.ADC/1178144) (2015\).
69. Calder, P. C. Omega\-3 fatty acids and inflammatory processes. *Nutrients* **2**, 355–374 (2010\).

[Article](https://doi.org/10.3390%2Fnu2030355) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3cXjvVKisLY%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=22254027) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3257651) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Omega-3%20fatty%20acids%20and%20inflammatory%20processes&journal=Nutrients&doi=10.3390%2Fnu2030355&volume=2&pages=355-374&publication_year=2010&author=Calder%2CPC)
70. Mozaffarian, D. \& Rimm, E. B. Fish intake, contaminants, and human health: evaluating the risks and the benefits. *JAMA* **296**, 1885–1899 (2006\).

[Article](https://doi.org/10.1001%2Fjama.296.15.1885) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BD28XhtFWmt7%2FF) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=17047219) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Fish%20intake%2C%20contaminants%2C%20and%20human%20health%3A%20evaluating%20the%20risks%20and%20the%20benefits&journal=JAMA&doi=10.1001%2Fjama.296.15.1885&volume=296&pages=1885-1899&publication_year=2006&author=Mozaffarian%2CD&author=Rimm%2CEB)
71. Ramsden, C. E. et al. Use of dietary linoleic acid for secondary prevention of coronary heart disease and death: evaluation of recovered data from the Sydney Diet Heart Study and updated meta\-analysis. *BMJ* **346**, e8707 (2013\).

[Article](https://doi.org/10.1136%2Fbmj.e8707) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=23386268) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4688426) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Use%20of%20dietary%20linoleic%20acid%20for%20secondary%20prevention%20of%20coronary%20heart%20disease%20and%20death%3A%20evaluation%20of%20recovered%20data%20from%20the%20Sydney%20Diet%20Heart%20Study%20and%20updated%20meta-analysis&journal=BMJ&doi=10.1136%2Fbmj.e8707&volume=346&publication_year=2013&author=Ramsden%2CCE)
72. Cassidy, A. et al. High anthocyanin intake is associated with a reduced risk of myocardial infarction in young and middle\-aged women. *Circulation* **127**, 188–196 (2013\).

[Article](https://doi.org/10.1161%2FCIRCULATIONAHA.112.122408) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3sXhtVynurs%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=23319811) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3762447) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=High%20anthocyanin%20intake%20is%20associated%20with%20a%20reduced%20risk%20of%20myocardial%20infarction%20in%20young%20and%20middle-aged%20women&journal=Circulation&doi=10.1161%2FCIRCULATIONAHA.112.122408&volume=127&pages=188-196&publication_year=2013&author=Cassidy%2CA)
73. Kalt, W. et al. Recent research on the health benefits of blueberries and their anthocyanins. *Adv. Nutr.* **11**, 224–236 (2020\).

[Article](https://doi.org/10.1093%2Fadvances%2Fnmz065) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31329250) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Recent%20research%20on%20the%20health%20benefits%20of%20blueberries%20and%20their%20anthocyanins&journal=Adv.%20Nutr.&doi=10.1093%2Fadvances%2Fnmz065&volume=11&pages=224-236&publication_year=2020&author=Kalt%2CW)
74. Hankinson, A., Lloyd, B. \& Alweis, R. Lime\-induced phytophotodermatitis. *J. Community Hosp. Intern. Med. Perspect.* **4**, 25090 (2014\).

[Article](https://doi.org/10.3402%2Fjchimp.v4.25090) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Lime-induced%20phytophotodermatitis&journal=J.%20Community%20Hosp.%20Intern.%20Med.%20Perspect.&doi=10.3402%2Fjchimp.v4.25090&volume=4&publication_year=2014&author=Hankinson%2CA&author=Lloyd%2CB&author=Alweis%2CR)
75. Sacks, F. M. et al. Dietary fats and cardiovascular disease: a presidential advisory from the American Heart Association. *Circulation* **136**, e1–e23 (2017\).

[Article](https://doi.org/10.1161%2FCIR.0000000000000510) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28620111) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Dietary%20fats%20and%20cardiovascular%20disease%3A%20a%20presidential%20advisory%20from%20the%20American%20Heart%20Association&journal=Circulation&doi=10.1161%2FCIR.0000000000000510&volume=136&pages=e1-e23&publication_year=2017&author=Sacks%2CFM)
76. de Souza, R. J. et al. Intake of saturated and trans unsaturated fatty acids and risk of all cause mortality, cardiovascular disease, and type 2 diabetes: systematic review and meta\-analysis of observational studies. *BMJ* **351**, h3978 (2015\).

[Article](https://doi.org/10.1136%2Fbmj.h3978) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=26268692) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4532752) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Intake%20of%20saturated%20and%20trans%20unsaturated%20fatty%20acids%20and%20risk%20of%20all%20cause%20mortality%2C%20cardiovascular%20disease%2C%20and%20type%202%20diabetes%3A%20systematic%20review%20and%20meta-analysis%20of%20observational%20studies&journal=BMJ&doi=10.1136%2Fbmj.h3978&volume=351&publication_year=2015&author=Souza%2CRJ)
77. Imamura, F. et al. Consumption of sugar sweetened beverages, artificially sweetened beverages, and fruit juice and incidence of type 2 diabetes: systematic review, meta\-analysis, and estimation of population attributable fraction. *BMJ* **351**, h3576 (2015\).

[Article](https://doi.org/10.1136%2Fbmj.h3576) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=26199070) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4510779) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Consumption%20of%20sugar%20sweetened%20beverages%2C%20artificially%20sweetened%20beverages%2C%20and%20fruit%20juice%20and%20incidence%20of%20type%202%20diabetes%3A%20systematic%20review%2C%20meta-analysis%2C%20and%20estimation%20of%20population%20attributable%20fraction&journal=BMJ&doi=10.1136%2Fbmj.h3576&volume=351&publication_year=2015&author=Imamura%2CF)
78. Yang, Q. et al. Added sugar intake and cardiovascular diseases mortality among US adults. *JAMA Intern. Med.* **174**, 516–524 (2014\).

[Article](https://doi.org/10.1001%2Fjamainternmed.2013.13563) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC2cXhs1Snu7jP) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=24493081) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10910551) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Added%20sugar%20intake%20and%20cardiovascular%20diseases%20mortality%20among%20US%20adults&journal=JAMA%20Intern.%20Med.&doi=10.1001%2Fjamainternmed.2013.13563&volume=174&pages=516-524&publication_year=2014&author=Yang%2CQ)
79. Schwingshackl, L. et al. Food groups and risk of all\-cause mortality: a systematic review and meta\-analysis of prospective studies. *Am. J. Clin. Nutr.* **105**, 1462–1473 (2017\).

[Article](https://doi.org/10.3945%2Fajcn.117.153148) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC1cXotFKmtA%3D%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28446499) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Food%20groups%20and%20risk%20of%20all-cause%20mortality%3A%20a%20systematic%20review%20and%20meta-analysis%20of%20prospective%20studies&journal=Am.%20J.%20Clin.%20Nutr.&doi=10.3945%2Fajcn.117.153148&volume=105&pages=1462-1473&publication_year=2017&author=Schwingshackl%2CL)
80. Rocha, J., Borges, N. \& Pinho, O. Table olives and health: a review. *J. Nutr. Sci.* **9**, e57 (2020\).

[Article](https://doi.org/10.1017%2Fjns.2020.50) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3MXmsV2ks7k%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33354328) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7737178) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Table%20olives%20and%20health%3A%20a%20review&journal=J.%20Nutr.%20Sci.&doi=10.1017%2Fjns.2020.50&volume=9&publication_year=2020&author=Rocha%2CJ&author=Borges%2CN&author=Pinho%2CO)
81. Li, S.\-C. et al. Almond consumption improved glycemic control and lipid profiles in patients with type 2 diabetes mellitus. *Metabolism* **60**, 474–479 (2011\).

[Article](https://doi.org/10.1016%2Fj.metabol.2010.04.009) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3MXjsV2gsL0%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=20580779) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Almond%20consumption%20improved%20glycemic%20control%20and%20lipid%20profiles%20in%20patients%20with%20type%202%20diabetes%20mellitus&journal=Metabolism&doi=10.1016%2Fj.metabol.2010.04.009&volume=60&pages=474-479&publication_year=2011&author=Li%2CS-C)
82. Lee\-Bravatti, M. A. et al. Almond consumption and risk factors for cardiovascular disease: a systematic review and meta\-analysis of randomized controlled trials. *Adv. Nutr.* **10**, 1076–1088 (2019\).

[Article](https://doi.org/10.1093%2Fadvances%2Fnmz043) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31243439) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6855931) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Almond%20consumption%20and%20risk%20factors%20for%20cardiovascular%20disease%3A%20a%20systematic%20review%20and%20meta-analysis%20of%20randomized%20controlled%20trials&journal=Adv.%20Nutr.&doi=10.1093%2Fadvances%2Fnmz043&volume=10&pages=1076-1088&publication_year=2019&author=Lee-Bravatti%2CMA)
83. Martin, N., Germanò, R., Hartley, L., Adler, A. J. \& Rees, K. Nut consumption for the primary prevention of cardiovascular disease. *Cochrane Database Syst. Rev.* **2015**, CD011583 (2015\).

[PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=26411417) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC9798256) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Nut%20consumption%20for%20the%20primary%20prevention%20of%20cardiovascular%20disease&journal=Cochrane%20Database%20Syst.%20Rev.&volume=2015&publication_year=2015&author=Martin%2CN&author=German%C3%B2%2CR&author=Hartley%2CL&author=Adler%2CAJ&author=Rees%2CK)
84. Jiang, R. Nut and peanut butter consumption and risk of type 2 diabetes in women. *JAMA* **288**, 2554 (2002\).

[Article](https://doi.org/10.1001%2Fjama.288.20.2554) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=12444862) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Nut%20and%20peanut%20butter%20consumption%20and%20risk%20of%20type%202%20diabetes%20in%20women&journal=JAMA&doi=10.1001%2Fjama.288.20.2554&volume=288&publication_year=2002&author=Jiang%2CR)
85. Blumberg, J., Vita, J. \& Chen, C. Concord grape juice polyphenols and cardiovascular risk factors: dose\-response relationships. *Nutrients* **7**, 10032–10052 (2015\).

[Article](https://doi.org/10.3390%2Fnu7125519) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC28XhsVagurjO) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=26633488) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4690071) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Concord%20grape%20juice%20polyphenols%20and%20cardiovascular%20risk%20factors%3A%20dose-response%20relationships&journal=Nutrients&doi=10.3390%2Fnu7125519&volume=7&pages=10032-10052&publication_year=2015&author=Blumberg%2CJ&author=Vita%2CJ&author=Chen%2CC)
86. Stein, J. H., Keevil, J. G., Wiebe, D. A., Aeschlimann, S. \& Folts, J. D. Purple grape juice improves endothelial function and reduces the susceptibility of LDL cholesterol to oxidation in patients with coronary artery disease. *Circulation* **100**, 1050–1055 (1999\).

[Article](https://doi.org/10.1161%2F01.CIR.100.10.1050) 
 [CAS](/articles/cas-redirect/1:STN:280:DyaK1Mvgs1Gruw%3D%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=10477529) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Purple%20grape%20juice%20improves%20endothelial%20function%20and%20reduces%20the%20susceptibility%20of%20LDL%20cholesterol%20to%20oxidation%20in%20patients%20with%20coronary%20artery%20disease&journal=Circulation&doi=10.1161%2F01.CIR.100.10.1050&volume=100&pages=1050-1055&publication_year=1999&author=Stein%2CJH&author=Keevil%2CJG&author=Wiebe%2CDA&author=Aeschlimann%2CS&author=Folts%2CJD)
87. Zhao, J., Wang, X., Lin, H. \& Lin, Z. Hazelnut and its by\-products: a comprehensive review of nutrition, phytochemical profile, extraction, bioactivities and applications. *Food Chem.* **413**, 135576 (2023\).

[Article](https://doi.org/10.1016%2Fj.foodchem.2023.135576) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3sXis1ymsLk%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=36745946) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Hazelnut%20and%20its%20by-products%3A%20a%20comprehensive%20review%20of%20nutrition%2C%20phytochemical%20profile%2C%20extraction%2C%20bioactivities%20and%20applications&journal=Food%20Chem.&doi=10.1016%2Fj.foodchem.2023.135576&volume=413&publication_year=2023&author=Zhao%2CJ&author=Wang%2CX&author=Lin%2CH&author=Lin%2CZ)
88. Tey, S. L. et al. Effects of different forms of hazelnuts on blood lipids and α\-tocopherol concentrations in mildly hypercholesterolemic individuals. *Eur. J. Clin. Nutr.* **65**, 117–124 (2011\).

[Article](https://doi.org/10.1038%2Fejcn.2010.200) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3MXht1ShsA%3D%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=20877394) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Effects%20of%20different%20forms%20of%20hazelnuts%20on%20blood%20lipids%20and%20%CE%B1-tocopherol%20concentrations%20in%20mildly%20hypercholesterolemic%20individuals&journal=Eur.%20J.%20Clin.%20Nutr.&doi=10.1038%2Fejcn.2010.200&volume=65&pages=117-124&publication_year=2011&author=Tey%2CSL)
89. Jazinaki, M. S., Rashidmayvan, M. \& Pahlavani, N. The effect of pomegranate juice supplementation on C\-reactive protein levels: GRADE \-assessed systematic review and dose–response updated meta\-analysis of data from randomized controlled trials. *Phytother. Res.* **38**, 2818–2831 (2024\).

[Article](https://doi.org/10.1002%2Fptr.8188) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2cXhtVGks7bN) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=38553998) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20effect%20of%20pomegranate%20juice%20supplementation%20on%20C-reactive%20protein%20levels%3A%20GRADE%20-assessed%20systematic%20review%20and%20dose%E2%80%93response%20updated%20meta-analysis%20of%20data%20from%20randomized%20controlled%20trials&journal=Phytother.%20Res.&doi=10.1002%2Fptr.8188&volume=38&pages=2818-2831&publication_year=2024&author=Jazinaki%2CMS&author=Rashidmayvan%2CM&author=Pahlavani%2CN)
90. Basu, A. \& Penugonda, K. Pomegranate juice: a heart\-healthy fruit juice. *Nutr. Rev.* **67**, 49–56 (2009\).

[Article](https://doi.org/10.1111%2Fj.1753-4887.2008.00133.x) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=19146506) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Pomegranate%20juice%3A%20a%20heart-healthy%20fruit%20juice&journal=Nutr.%20Rev.&doi=10.1111%2Fj.1753-4887.2008.00133.x&volume=67&pages=49-56&publication_year=2009&author=Basu%2CA&author=Penugonda%2CK)
91. Khaw, K.\-T. et al. Randomised trial of coconut oil, olive oil or butter on blood lipids and other cardiovascular risk factors in healthy men and women. *BMJ Open* **8**, e020167 (2018\).

[Article](https://doi.org/10.1136%2Fbmjopen-2017-020167) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=29511019) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5855206) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Randomised%20trial%20of%20coconut%20oil%2C%20olive%20oil%20or%20butter%20on%20blood%20lipids%20and%20other%20cardiovascular%20risk%20factors%20in%20healthy%20men%20and%20women&journal=BMJ%20Open&doi=10.1136%2Fbmjopen-2017-020167&volume=8&publication_year=2018&author=Khaw%2CK-T)
92. Eyres, L., Eyres, M. F., Chisholm, A. \& Brown, R. C. Coconut oil consumption and cardiovascular risk factors in humans. *Nutr. Rev.* **74**, 267–280 (2016\).

[Article](https://doi.org/10.1093%2Fnutrit%2Fnuw002) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=26946252) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4892314) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Coconut%20oil%20consumption%20and%20cardiovascular%20risk%20factors%20in%20humans&journal=Nutr.%20Rev.&doi=10.1093%2Fnutrit%2Fnuw002&volume=74&pages=267-280&publication_year=2016&author=Eyres%2CL&author=Eyres%2CMF&author=Chisholm%2CA&author=Brown%2CRC)
93. Yang, D. K. Cabbage (*Brassica oleracea var. capitata*) protects against H2O2 \-induced oxidative stress by preventing mitochondrial dysfunction in H9c2 cardiomyoblasts. *Evid. Based Complement. Alternat. Med.* **2018**, 2179021 (2018\).

[Article](https://doi.org/10.1155%2F2018%2F2179021) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=30158990) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6109504) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Cabbage%20%28Brassica%20oleracea%20var.%20capitata%29%20protects%20against%20H2O2%20-induced%20oxidative%20stress%20by%20preventing%20mitochondrial%20dysfunction%20in%20H9c2%20cardiomyoblasts&journal=Evid.%20Based%20Complement.%20Alternat.%20Med.&doi=10.1155%2F2018%2F2179021&volume=2018&publication_year=2018&author=Yang%2CDK)
94. Jiang, Y. et al. Cruciferous vegetable intake is inversely correlated with circulating levels of proinflammatory markers in women. *J. Acad. Nutr. Diet.* **114**, 700–708\.e2 (2014\).

[Article](https://doi.org/10.1016%2Fj.jand.2013.12.019) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=24630682) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4063312) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Cruciferous%20vegetable%20intake%20is%20inversely%20correlated%20with%20circulating%20levels%20of%20proinflammatory%20markers%20in%20women&journal=J.%20Acad.%20Nutr.%20Diet.&doi=10.1016%2Fj.jand.2013.12.019&volume=114&pages=700-708.e2&publication_year=2014&author=Jiang%2CY)
95. McKay, D., Eliasziw, M., Chen, C. \& Blumberg, J. A pecan\-rich diet improves cardiometabolic risk factors in overweight and obese adults: a randomized controlled trial. *Nutrients* **10**, 339 (2018\).

[Article](https://doi.org/10.3390%2Fnu10030339) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=29534487) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5872757) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20pecan-rich%20diet%20improves%20cardiometabolic%20risk%20factors%20in%20overweight%20and%20obese%20adults%3A%20a%20randomized%20controlled%20trial&journal=Nutrients&doi=10.3390%2Fnu10030339&volume=10&publication_year=2018&author=McKay%2CD&author=Eliasziw%2CM&author=Chen%2CC&author=Blumberg%2CJ)
96. Robbins, K. S., Gong, Y., Wells, M. L., Greenspan, P. \& Pegg, R. B. Reprint of “Investigation of the antioxidant capacity and phenolic constituents of U.S. pecans. *J. Funct. Foods* **18**, 1002–1013 (2015\).

[Article](https://doi.org/10.1016%2Fj.jff.2015.05.026) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC2MXpsVWrt7o%3D) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Reprint%20of%20%E2%80%9CInvestigation%20of%20the%20antioxidant%20capacity%20and%20phenolic%20constituents%20of%20U.S.%20pecans&journal=J.%20Funct.%20Foods&doi=10.1016%2Fj.jff.2015.05.026&volume=18&pages=1002-1013&publication_year=2015&author=Robbins%2CKS&author=Gong%2CY&author=Wells%2CML&author=Greenspan%2CP&author=Pegg%2CRB)
97. Feeney, E. L., Lamichhane, P. \& Sheehan, J. J. The cheese matrix: understanding the impact of cheese structure on aspects of cardiovascular health – a food science and a human nutrition perspective. *Int. J. Dairy Technol.* **74**, 656–670 (2021\).

[Article](https://doi.org/10.1111%2F1471-0307.12755) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3MXitlWmsbfL) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20cheese%20matrix%3A%20understanding%20the%20impact%20of%20cheese%20structure%20on%20aspects%20of%20cardiovascular%20health%20%E2%80%93%20a%20food%20science%20and%20a%20human%20nutrition%20perspective&journal=Int.%20J.%20Dairy%20Technol.&doi=10.1111%2F1471-0307.12755&volume=74&pages=656-670&publication_year=2021&author=Feeney%2CEL&author=Lamichhane%2CP&author=Sheehan%2CJJ)
98. Rangel, A. H. D. N. et al. An overview of the occurrence of bioactive peptides in different types of cheeses. *Foods* **12**, 4261 (2023\).

[Article](https://doi.org/10.3390%2Ffoods12234261) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3sXis1Gjtb%2FL) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=38231707) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10706718) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=An%20overview%20of%20the%20occurrence%20of%20bioactive%20peptides%20in%20different%20types%20of%20cheeses&journal=Foods&doi=10.3390%2Ffoods12234261&volume=12&publication_year=2023&author=Rangel%2CAHDN)
99. Lemke, S. L. et al. Dietary intake of stearidonic acid–enriched soybean oil increases the omega\-3 index: randomized, double\-blind clinical study of efficacy and safety. *Am. J. Clin. Nutr.* **92**, 766–775 (2010\).

[Article](https://doi.org/10.3945%2Fajcn.2009.29072) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3cXht1GisL3E) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=20739419) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Dietary%20intake%20of%20stearidonic%20acid%E2%80%93enriched%20soybean%20oil%20increases%20the%20omega-3%20index%3A%20randomized%2C%20double-blind%20clinical%20study%20of%20efficacy%20and%20safety&journal=Am.%20J.%20Clin.%20Nutr.&doi=10.3945%2Fajcn.2009.29072&volume=92&pages=766-775&publication_year=2010&author=Lemke%2CSL)
100. Baer, D. J., Henderson, T. \& Gebauer, S. K. Consumption of high\-oleic soybean oil improves lipid and lipoprotein profile in humans compared to a palm oil blend: a randomized controlled trial. *Lipids* **56**, 313–325 (2021\).

[Article](https://doi.org/10.1002%2Flipd.12298) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3MXktF2ltb4%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33596340) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8248317) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Consumption%20of%20high-oleic%20soybean%20oil%20improves%20lipid%20and%20lipoprotein%20profile%20in%20humans%20compared%20to%20a%20palm%20oil%20blend%3A%20a%20randomized%20controlled%20trial&journal=Lipids&doi=10.1002%2Flipd.12298&volume=56&pages=313-325&publication_year=2021&author=Baer%2CDJ&author=Henderson%2CT&author=Gebauer%2CSK)
101. Fang, S., Lin, F., Qu, D., Liang, X. \& Wang, L. Characterization of purified red cabbage anthocyanins: improvement in HPLC separation and protective effect against H2O2\-induced oxidative stress in HepG2 cells. *Molecules* **24**, 124 (2018\).

[Article](https://doi.org/10.3390%2Fmolecules24010124) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=30602654) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6337153) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Characterization%20of%20purified%20red%20cabbage%20anthocyanins%3A%20improvement%20in%20HPLC%20separation%20and%20protective%20effect%20against%20H2O2-induced%20oxidative%20stress%20in%20HepG2%20cells&journal=Molecules&doi=10.3390%2Fmolecules24010124&volume=24&publication_year=2018&author=Fang%2CS&author=Lin%2CF&author=Qu%2CD&author=Liang%2CX&author=Wang%2CL)
102. Wiczkowski, W., Szawara\-Nowak, D. \& Topolska, J. Red cabbage anthocyanins: profile, isolation, identification, and antioxidant activity. *Food Res. Int.* **51**, 303–309 (2013\).

[Article](https://doi.org/10.1016%2Fj.foodres.2012.12.015) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3sXjslWqsbc%3D) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Red%20cabbage%20anthocyanins%3A%20profile%2C%20isolation%2C%20identification%2C%20and%20antioxidant%20activity&journal=Food%20Res.%20Int.&doi=10.1016%2Fj.foodres.2012.12.015&volume=51&pages=303-309&publication_year=2013&author=Wiczkowski%2CW&author=Szawara-Nowak%2CD&author=Topolska%2CJ)
103. Siervo, M. et al. Nitrate\-rich beetroot juice reduces blood pressure in Tanzanian adults with elevated blood pressure: a double\-blind randomized controlled feasibility trial. *J. Nutr.* **150**, 2460–2468 (2020\).

[Article](https://doi.org/10.1093%2Fjn%2Fnxaa170) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32729923) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7467850) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Nitrate-rich%20beetroot%20juice%20reduces%20blood%20pressure%20in%20Tanzanian%20adults%20with%20elevated%20blood%20pressure%3A%20a%20double-blind%20randomized%20controlled%20feasibility%20trial&journal=J.%20Nutr.&doi=10.1093%2Fjn%2Fnxaa170&volume=150&pages=2460-2468&publication_year=2020&author=Siervo%2CM)
104. Clifford, T., Howatson, G., West, D. \& Stevenson, E. The potential benefits of red beetroot supplementation in health and disease. *Nutrients* **7**, 2801–2822 (2015\).

[Article](https://doi.org/10.3390%2Fnu7042801) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC2MXotFKhtLw%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=25875121) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4425174) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20potential%20benefits%20of%20red%20beetroot%20supplementation%20in%20health%20and%20disease&journal=Nutrients&doi=10.3390%2Fnu7042801&volume=7&pages=2801-2822&publication_year=2015&author=Clifford%2CT&author=Howatson%2CG&author=West%2CD&author=Stevenson%2CE)
105. Grover, A. \& Leskovec, J. "node2vec: Scalable feature learning for networks." Proceedings of the 22nd ACMSIGKDD international conference on Knowledge discovery and data mining. (2016\).

[Download references](https://citation-needed.springer.com/v2/references/10.1038/s41538-025-00680-9?format=refman&flavour=references)

## Acknowledgements

This work was supported by the USDA\-NIFA AI Institute for Next Generation Food Systems (AIFS), USDA\-NIFA award number 2020\-67021\-32855\.

## Author information

### Authors and Affiliations

1. Department of Computer Science, the University of California at Davis, Davis, CA, USA

Fangzhou Li, Jason Youn, Kaichi Xie, Trevor Chan, Pranav Gupta, Michael Gunning, Keer Ni \& Ilias Tagkopoulos
2. Genome Center, the University of California at Davis, Davis, CA, USA

Fangzhou Li, Jason Youn, Trevor Chan, Pranav Gupta, Arielle Yoo, Michael Gunning, Keer Ni \& Ilias Tagkopoulos
3. USDA/NSF AI Institute for Next Generation Food Systems (AIFS), Davis, CA, USA

Fangzhou Li, Jason Youn, Kaichi Xie, Trevor Chan, Pranav Gupta, Arielle Yoo, Michael Gunning, Keer Ni \& Ilias Tagkopoulos

Authors1. Fangzhou Li[View author publications](/search?author=Fangzhou%20Li)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Fangzhou%20Li) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Fangzhou%20Li%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
2. Jason Youn[View author publications](/search?author=Jason%20Youn)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Jason%20Youn) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Jason%20Youn%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
3. Kaichi Xie[View author publications](/search?author=Kaichi%20Xie)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Kaichi%20Xie) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Kaichi%20Xie%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
4. Trevor Chan[View author publications](/search?author=Trevor%20Chan)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Trevor%20Chan) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Trevor%20Chan%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
5. Pranav Gupta[View author publications](/search?author=Pranav%20Gupta)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Pranav%20Gupta) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Pranav%20Gupta%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
6. Arielle Yoo[View author publications](/search?author=Arielle%20Yoo)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Arielle%20Yoo) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Arielle%20Yoo%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
7. Michael Gunning[View author publications](/search?author=Michael%20Gunning)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Michael%20Gunning) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Michael%20Gunning%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
8. Keer Ni[View author publications](/search?author=Keer%20Ni)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Keer%20Ni) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Keer%20Ni%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
9. Ilias Tagkopoulos[View author publications](/search?author=Ilias%20Tagkopoulos)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Ilias%20Tagkopoulos) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Ilias%20Tagkopoulos%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
### Contributions

F.L. and J.Y. created the knowledge graph and built the sentence filtration and sentence extraction pipeline. K.X. annotated the information extraction dataset and fine\-tuned GPT\-3\.5 on the data. T.C. performed analysis for results, generated figures, and wrote the paper. P.G. built the bioactivity prediction model. A.Y. integrated disease data into FA. M.G. integrated flavor data into FA. K.N. helped K.X. with annotation. I.T. conceived and supervised all aspects of the project, including project management, framework design, pipeline architecture, predictive model, data analysis, hypothesis generation and testing. All authors contributed to writing the manuscript.

### Corresponding author

Correspondence to
 [Ilias Tagkopoulos](mailto:itagkopoulos@ucdavis.edu).

## Ethics declarations


### Competing interests


The authors declare no competing interests.


## Additional information

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

## Supplementary information

### [Supplementary information (download DOCX )](https://static-content.springer.com/esm/art%3A10.1038%2Fs41538-025-00680-9/MediaObjects/41538_2025_680_MOESM1_ESM.docx)

## Rights and permissions


**Open Access** This article is licensed under a Creative Commons Attribution 4\.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit [http://creativecommons.org/licenses/by/4\.0/](http://creativecommons.org/licenses/by/4.0/).


[Reprints and permissions](https://s100.copyright.com/AppDispatchServlet?title=A%20unified%20knowledge%20graph%20linking%20foodomics%20to%20chemical-disease%20networks%20and%20flavor%20profiles&author=Fangzhou%20Li%20et%20al&contentID=10.1038%2Fs41538-025-00680-9&copyright=The%20Author%28s%29&publication=2396-8370&publicationDate=2026-01-20&publisherName=SpringerNature&orderBeanReset=true&oa=CC%20BY)

## About this article

[![Check for updates. Verify currency and authenticity via CrossMark](data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjgxIiB3aWR0aD0iNTciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj48cGF0aCBkPSJtMTcuMzUgMzUuNDUgMjEuMy0xNC4ydi0xNy4wM2gtMjEuMyIgZmlsbD0iIzk4OTg5OCIvPjxwYXRoIGQ9Im0zOC42NSAzNS40NS0yMS4zLTE0LjJ2LTE3LjAzaDIxLjMiIGZpbGw9IiM3NDc0NzQiLz48cGF0aCBkPSJtMjggLjVjLTEyLjk4IDAtMjMuNSAxMC41Mi0yMy41IDIzLjVzMTAuNTIgMjMuNSAyMy41IDIzLjUgMjMuNS0xMC41MiAyMy41LTIzLjVjMC02LjIzLTIuNDgtMTIuMjEtNi44OC0xNi42Mi00LjQxLTQuNC0xMC4zOS02Ljg4LTE2LjYyLTYuODh6bTAgNDEuMjVjLTkuOCAwLTE3Ljc1LTcuOTUtMTcuNzUtMTcuNzVzNy45NS0xNy43NSAxNy43NS0xNy43NSAxNy43NSA3Ljk1IDE3Ljc1IDE3Ljc1YzAgNC43MS0xLjg3IDkuMjItNS4yIDEyLjU1cy03Ljg0IDUuMi0xMi41NSA1LjJ6IiBmaWxsPSIjNTM1MzUzIi8+PHBhdGggZD0ibTQxIDM2Yy01LjgxIDYuMjMtMTUuMjMgNy40NS0yMi40MyAyLjktNy4yMS00LjU1LTEwLjE2LTEzLjU3LTcuMDMtMjEuNWwtNC45Mi0zLjExYy00Ljk1IDEwLjctMS4xOSAyMy40MiA4Ljc4IDI5LjcxIDkuOTcgNi4zIDIzLjA3IDQuMjIgMzAuNi00Ljg2eiIgZmlsbD0iIzljOWM5YyIvPjxwYXRoIGQ9Im0uMiA1OC40NWMwLS43NS4xMS0xLjQyLjMzLTIuMDFzLjUyLTEuMDkuOTEtMS41Yy4zOC0uNDEuODMtLjczIDEuMzQtLjk0LjUxLS4yMiAxLjA2LS4zMiAxLjY1LS4zMi41NiAwIDEuMDYuMTEgMS41MS4zNS40NC4yMy44MS41IDEuMS44MWwtLjkxIDEuMDFjLS4yNC0uMjQtLjQ5LS40Mi0uNzUtLjU2LS4yNy0uMTMtLjU4LS4yLS45My0uMi0uMzkgMC0uNzMuMDgtMS4wNS4yMy0uMzEuMTYtLjU4LjM3LS44MS42Ni0uMjMuMjgtLjQxLjYzLS41MyAxLjA0LS4xMy40MS0uMTkuODgtLjE5IDEuMzkgMCAxLjA0LjIzIDEuODYuNjggMi40Ni40NS41OSAxLjA2Ljg4IDEuODQuODguNDEgMCAuNzctLjA3IDEuMDctLjIzcy41OS0uMzkuODUtLjY4bC45MSAxYy0uMzguNDMtLjguNzYtMS4yOC45OS0uNDcuMjItMSAuMzQtMS41OC4zNC0uNTkgMC0xLjEzLS4xLTEuNjQtLjMxLS41LS4yLS45NC0uNTEtMS4zMS0uOTEtLjM4LS40LS42Ny0uOS0uODgtMS40OC0uMjItLjU5LS4zMy0xLjI2LS4zMy0yLjAyem04LjQtNS4zM2gxLjYxdjIuNTRsLS4wNSAxLjMzYy4yOS0uMjcuNjEtLjUxLjk2LS43MnMuNzYtLjMxIDEuMjQtLjMxYy43MyAwIDEuMjcuMjMgMS42MS43MS4zMy40Ny41IDEuMTQuNSAyLjAydjQuMzFoLTEuNjF2LTQuMWMwLS41Ny0uMDgtLjk3LS4yNS0xLjIxLS4xNy0uMjMtLjQ1LS4zNS0uODMtLjM1LS4zIDAtLjU2LjA4LS43OS4yMi0uMjMuMTUtLjQ5LjM2LS43OC42NHY0LjhoLTEuNjF6bTcuMzcgNi40NWMwLS41Ni4wOS0xLjA2LjI2LTEuNTEuMTgtLjQ1LjQyLS44My43MS0xLjE0LjI5LS4zLjYzLS41NCAxLjAxLS43MS4zOS0uMTcuNzgtLjI1IDEuMTgtLjI1LjQ3IDAgLjg4LjA4IDEuMjMuMjQuMzYuMTYuNjUuMzguODkuNjdzLjQyLjYzLjU0IDEuMDNjLjEyLjQxLjE4Ljg0LjE4IDEuMzIgMCAuMzItLjAyLjU3LS4wNy43NmgtNC4zNmMuMDcuNjIuMjkgMS4xLjY1IDEuNDQuMzYuMzMuODIuNSAxLjM4LjUuMjkgMCAuNTctLjA0LjgzLS4xM3MuNTEtLjIxLjc2LS4zN2wuNTUgMS4wMWMtLjMzLjIxLS42OS4zOS0xLjA5LjUzLS40MS4xNC0uODMuMjEtMS4yNi4yMS0uNDggMC0uOTItLjA4LTEuMzQtLjI1LS40MS0uMTYtLjc2LS40LTEuMDctLjctLjMxLS4zMS0uNTUtLjY5LS43Mi0xLjEzLS4xOC0uNDQtLjI2LS45NS0uMjYtMS41MnptNC42LS42MmMwLS41NS0uMTEtLjk4LS4zNC0xLjI4LS4yMy0uMzEtLjU4LS40Ny0xLjA2LS40Ny0uNDEgMC0uNzcuMTUtMS4wNy40NS0uMzEuMjktLjUuNzMtLjU4IDEuM3ptMi41LjYyYzAtLjU3LjA5LTEuMDguMjgtMS41My4xOC0uNDQuNDMtLjgyLjc1LTEuMTNzLjY5LS41NCAxLjEtLjcxYy40Mi0uMTYuODUtLjI0IDEuMzEtLjI0LjQ1IDAgLjg0LjA4IDEuMTcuMjNzLjYxLjM0Ljg1LjU3bC0uNzcgMS4wMmMtLjE5LS4xNi0uMzgtLjI4LS41Ni0uMzctLjE5LS4wOS0uMzktLjE0LS42MS0uMTQtLjU2IDAtMS4wMS4yMS0xLjM1LjYzLS4zNS40MS0uNTIuOTctLjUyIDEuNjcgMCAuNjkuMTcgMS4yNC41MSAxLjY2LjM0LjQxLjc4LjYyIDEuMzIuNjIuMjggMCAuNTQtLjA2Ljc4LS4xNy4yNC0uMTIuNDUtLjI2LjY0LS40MmwuNjcgMS4wM2MtLjMzLjI5LS42OS41MS0xLjA4LjY1LS4zOS4xNS0uNzguMjMtMS4xOC4yMy0uNDYgMC0uOS0uMDgtMS4zMS0uMjQtLjQtLjE2LS43NS0uMzktMS4wNS0uN3MtLjUzLS42OS0uNy0xLjEzYy0uMTctLjQ1LS4yNS0uOTYtLjI1LTEuNTN6bTYuOTEtNi40NWgxLjU4djYuMTdoLjA1bDIuNTQtMy4xNmgxLjc3bC0yLjM1IDIuOCAyLjU5IDQuMDdoLTEuNzVsLTEuNzctMi45OC0xLjA4IDEuMjN2MS43NWgtMS41OHptMTMuNjkgMS4yN2MtLjI1LS4xMS0uNS0uMTctLjc1LS4xNy0uNTggMC0uODcuMzktLjg3IDEuMTZ2Ljc1aDEuMzR2MS4yN2gtMS4zNHY1LjZoLTEuNjF2LTUuNmgtLjkydi0xLjJsLjkyLS4wN3YtLjcyYzAtLjM1LjA0LS42OC4xMy0uOTguMDgtLjMxLjIxLS41Ny40LS43OXMuNDItLjM5LjcxLS41MWMuMjgtLjEyLjYzLS4xOCAxLjA0LS4xOC4yNCAwIC40OC4wMi42OS4wNy4yMi4wNS40MS4xLjU3LjE3em0uNDggNS4xOGMwLS41Ny4wOS0xLjA4LjI3LTEuNTMuMTctLjQ0LjQxLS44Mi43Mi0xLjEzLjMtLjMxLjY1LS41NCAxLjA0LS43MS4zOS0uMTYuOC0uMjQgMS4yMy0uMjRzLjg0LjA4IDEuMjQuMjRjLjQuMTcuNzQuNCAxLjA0Ljcxcy41NC42OS43MiAxLjEzYy4xOS40NS4yOC45Ni4yOCAxLjUzcy0uMDkgMS4wOC0uMjggMS41M2MtLjE4LjQ0LS40Mi44Mi0uNzIgMS4xM3MtLjY0LjU0LTEuMDQuNy0uODEuMjQtMS4yNC4yNC0uODQtLjA4LTEuMjMtLjI0LS43NC0uMzktMS4wNC0uN2MtLjMxLS4zMS0uNTUtLjY5LS43Mi0xLjEzLS4xOC0uNDUtLjI3LS45Ni0uMjctMS41M3ptMS42NSAwYzAgLjY5LjE0IDEuMjQuNDMgMS42Ni4yOC40MS42OC42MiAxLjE4LjYyLjUxIDAgLjktLjIxIDEuMTktLjYyLjI5LS40Mi40NC0uOTcuNDQtMS42NiAwLS43LS4xNS0xLjI2LS40NC0xLjY3LS4yOS0uNDItLjY4LS42My0xLjE5LS42My0uNSAwLS45LjIxLTEuMTguNjMtLjI5LjQxLS40My45Ny0uNDMgMS42N3ptNi40OC0zLjQ0aDEuMzNsLjEyIDEuMjFoLjA1Yy4yNC0uNDQuNTQtLjc5Ljg4LTEuMDIuMzUtLjI0LjctLjM2IDEuMDctLjM2LjMyIDAgLjU5LjA1Ljc4LjE0bC0uMjggMS40LS4zMy0uMDljLS4xMS0uMDEtLjIzLS4wMi0uMzgtLjAyLS4yNyAwLS41Ni4xLS44Ni4zMXMtLjU1LjU4LS43NyAxLjF2NC4yaC0xLjYxem0tNDcuODcgMTVoMS42MXY0LjFjMCAuNTcuMDguOTcuMjUgMS4yLjE3LjI0LjQ0LjM1LjgxLjM1LjMgMCAuNTctLjA3LjgtLjIyLjIyLS4xNS40Ny0uMzkuNzMtLjczdi00LjdoMS42MXY2Ljg3aC0xLjMybC0uMTItMS4wMWgtLjA0Yy0uMy4zNi0uNjMuNjQtLjk4Ljg2LS4zNS4yMS0uNzYuMzItMS4yNC4zMi0uNzMgMC0xLjI3LS4yNC0xLjYxLS43MS0uMzMtLjQ3LS41LTEuMTQtLjUtMi4wMnptOS40NiA3LjQzdjIuMTZoLTEuNjF2LTkuNTloMS4zM2wuMTIuNzJoLjA1Yy4yOS0uMjQuNjEtLjQ1Ljk3LS42My4zNS0uMTcuNzItLjI2IDEuMS0uMjYuNDMgMCAuODEuMDggMS4xNS4yNC4zMy4xNy42MS40Ljg0LjcxLjI0LjMxLjQxLjY4LjUzIDEuMTEuMTMuNDIuMTkuOTEuMTkgMS40NCAwIC41OS0uMDkgMS4xMS0uMjUgMS41Ny0uMTYuNDctLjM4Ljg1LS42NSAxLjE2LS4yNy4zMi0uNTguNTYtLjk0LjczLS4zNS4xNi0uNzIuMjUtMS4xLjI1LS4zIDAtLjYtLjA3LS45LS4ycy0uNTktLjMxLS44Ny0uNTZ6bTAtMi4zYy4yNi4yMi41LjM3LjczLjQ1LjI0LjA5LjQ2LjEzLjY2LjEzLjQ2IDAgLjg0LS4yIDEuMTUtLjYuMzEtLjM5LjQ2LS45OC40Ni0xLjc3IDAtLjY5LS4xMi0xLjIyLS4zNS0xLjYxLS4yMy0uMzgtLjYxLS41Ny0xLjEzLS41Ny0uNDkgMC0uOTkuMjYtMS41Mi43N3ptNS44Ny0xLjY5YzAtLjU2LjA4LTEuMDYuMjUtMS41MS4xNi0uNDUuMzctLjgzLjY1LTEuMTQuMjctLjMuNTgtLjU0LjkzLS43MXMuNzEtLjI1IDEuMDgtLjI1Yy4zOSAwIC43My4wNyAxIC4yLjI3LjE0LjU0LjMyLjgxLjU1bC0uMDYtMS4xdi0yLjQ5aDEuNjF2OS44OGgtMS4zM2wtLjExLS43NGgtLjA2Yy0uMjUuMjUtLjU0LjQ2LS44OC42NC0uMzMuMTgtLjY5LjI3LTEuMDYuMjctLjg3IDAtMS41Ni0uMzItMi4wNy0uOTVzLS43Ni0xLjUxLS43Ni0yLjY1em0xLjY3LS4wMWMwIC43NC4xMyAxLjMxLjQgMS43LjI2LjM4LjY1LjU4IDEuMTUuNTguNTEgMCAuOTktLjI2IDEuNDQtLjc3di0zLjIxYy0uMjQtLjIxLS40OC0uMzYtLjctLjQ1LS4yMy0uMDgtLjQ2LS4xMi0uNy0uMTItLjQ1IDAtLjgyLjE5LTEuMTMuNTktLjMxLjM5LS40Ni45NS0uNDYgMS42OHptNi4zNSAxLjU5YzAtLjczLjMyLTEuMy45Ny0xLjcxLjY0LS40IDEuNjctLjY4IDMuMDgtLjg0IDAtLjE3LS4wMi0uMzQtLjA3LS41MS0uMDUtLjE2LS4xMi0uMy0uMjItLjQzcy0uMjItLjIyLS4zOC0uM2MtLjE1LS4wNi0uMzQtLjEtLjU4LS4xLS4zNCAwLS42OC4wNy0xIC4ycy0uNjMuMjktLjkzLjQ3bC0uNTktMS4wOGMuMzktLjI0LjgxLS40NSAxLjI4LS42My40Ny0uMTcuOTktLjI2IDEuNTQtLjI2Ljg2IDAgMS41MS4yNSAxLjkzLjc2cy42MyAxLjI1LjYzIDIuMjF2NC4wN2gtMS4zMmwtLjEyLS43NmgtLjA1Yy0uMy4yNy0uNjMuNDgtLjk4LjY2cy0uNzMuMjctMS4xNC4yN2MtLjYxIDAtMS4xLS4xOS0xLjQ4LS41Ni0uMzgtLjM2LS41Ny0uODUtLjU3LTEuNDZ6bTEuNTctLjEyYzAgLjMuMDkuNTMuMjcuNjcuMTkuMTQuNDIuMjEuNzEuMjEuMjggMCAuNTQtLjA3Ljc3LS4ycy40OC0uMzEuNzMtLjU2di0xLjU0Yy0uNDcuMDYtLjg2LjEzLTEuMTguMjMtLjMxLjA5LS41Ny4xOS0uNzYuMzFzLS4zMy4yNS0uNDEuNGMtLjA5LjE1LS4xMy4zMS0uMTMuNDh6bTYuMjktMy42M2gtLjk4di0xLjJsMS4wNi0uMDcuMi0xLjg4aDEuMzR2MS44OGgxLjc1djEuMjdoLTEuNzV2My4yOGMwIC44LjMyIDEuMi45NyAxLjIuMTIgMCAuMjQtLjAxLjM3LS4wNC4xMi0uMDMuMjQtLjA3LjM0LS4xMWwuMjggMS4xOWMtLjE5LjA2LS40LjEyLS42NC4xNy0uMjMuMDUtLjQ5LjA4LS43Ni4wOC0uNCAwLS43NC0uMDYtMS4wMi0uMTgtLjI3LS4xMy0uNDktLjMtLjY3LS41Mi0uMTctLjIxLS4zLS40OC0uMzctLjc4LS4wOC0uMy0uMTItLjY0LS4xMi0xLjAxem00LjM2IDIuMTdjMC0uNTYuMDktMS4wNi4yNy0xLjUxcy40MS0uODMuNzEtMS4xNGMuMjktLjMuNjMtLjU0IDEuMDEtLjcxLjM5LS4xNy43OC0uMjUgMS4xOC0uMjUuNDcgMCAuODguMDggMS4yMy4yNC4zNi4xNi42NS4zOC44OS42N3MuNDIuNjMuNTQgMS4wM2MuMTIuNDEuMTguODQuMTggMS4zMiAwIC4zMi0uMDIuNTctLjA3Ljc2aC00LjM3Yy4wOC42Mi4yOSAxLjEuNjUgMS40NC4zNi4zMy44Mi41IDEuMzguNS4zIDAgLjU4LS4wNC44NC0uMTMuMjUtLjA5LjUxLS4yMS43Ni0uMzdsLjU0IDEuMDFjLS4zMi4yMS0uNjkuMzktMS4wOS41M3MtLjgyLjIxLTEuMjYuMjFjLS40NyAwLS45Mi0uMDgtMS4zMy0uMjUtLjQxLS4xNi0uNzctLjQtMS4wOC0uNy0uMy0uMzEtLjU0LS42OS0uNzItMS4xMy0uMTctLjQ0LS4yNi0uOTUtLjI2LTEuNTJ6bTQuNjEtLjYyYzAtLjU1LS4xMS0uOTgtLjM0LTEuMjgtLjIzLS4zMS0uNTgtLjQ3LTEuMDYtLjQ3LS40MSAwLS43Ny4xNS0xLjA4LjQ1LS4zMS4yOS0uNS43My0uNTcgMS4zem0zLjAxIDIuMjNjLjMxLjI0LjYxLjQzLjkyLjU3LjMuMTMuNjMuMi45OC4yLjM4IDAgLjY1LS4wOC44My0uMjNzLjI3LS4zNS4yNy0uNmMwLS4xNC0uMDUtLjI2LS4xMy0uMzctLjA4LS4xLS4yLS4yLS4zNC0uMjgtLjE0LS4wOS0uMjktLjE2LS40Ny0uMjNsLS41My0uMjJjLS4yMy0uMDktLjQ2LS4xOC0uNjktLjMtLjIzLS4xMS0uNDQtLjI0LS42Mi0uNHMtLjMzLS4zNS0uNDUtLjU1Yy0uMTItLjIxLS4xOC0uNDYtLjE4LS43NSAwLS42MS4yMy0xLjEuNjgtMS40OS40NC0uMzggMS4wNi0uNTcgMS44My0uNTcuNDggMCAuOTEuMDggMS4yOS4yNXMuNzEuMzYuOTkuNTdsLS43NC45OGMtLjI0LS4xNy0uNDktLjMyLS43My0uNDItLjI1LS4xMS0uNTEtLjE2LS43OC0uMTYtLjM1IDAtLjYuMDctLjc2LjIxLS4xNy4xNS0uMjUuMzMtLjI1LjU0IDAgLjE0LjA0LjI2LjEyLjM2cy4xOC4xOC4zMS4yNmMuMTQuMDcuMjkuMTQuNDYuMjFsLjU0LjE5Yy4yMy4wOS40Ny4xOC43LjI5cy40NC4yNC42NC40Yy4xOS4xNi4zNC4zNS40Ni41OC4xMS4yMy4xNy41LjE3LjgyIDAgLjMtLjA2LjU4LS4xNy44My0uMTIuMjYtLjI5LjQ4LS41MS42OC0uMjMuMTktLjUxLjM0LS44NC40NS0uMzQuMTEtLjcyLjE3LTEuMTUuMTctLjQ4IDAtLjk1LS4wOS0xLjQxLS4yNy0uNDYtLjE5LS44Ni0uNDEtMS4yLS42OHoiIGZpbGw9IiM1MzUzNTMiLz48L2c+PC9zdmc+)](https://crossmark.crossref.org/dialog/?doi=10.1038/s41538-025-00680-9)### Cite this article

Li, F., Youn, J., Xie, K. *et al.* A unified knowledge graph linking foodomics to chemical\-disease networks and flavor profiles.
 *npj Sci Food* **10**, 33 (2026\). https://doi.org/10\.1038/s41538\-025\-00680\-9

[Download citation](https://citation-needed.springer.com/v2/references/10.1038/s41538-025-00680-9?format=refman&flavour=citation)

* Received: 17 July 2025
* Accepted: 17 December 2025
* Published: 20 January 2026
* Version of record: 03 February 2026
* DOI: https://doi.org/10\.1038/s41538\-025\-00680\-9

### Share this article

Anyone you share the following link with will be able to read this content:

Get shareable linkSorry, a shareable link is not currently available for this article.

Copy shareable link to clipboard
 Provided by the Springer Nature SharedIt content\-sharing initiative
 


### Subjects


* [Biochemistry](/subjects/biochemistry)
* [Chemistry](/subjects/chemistry)
* [Computational biology and bioinformatics](/subjects/computational-biology-and-bioinformatics)





