---
url: "https://www.nature.com/articles/s41598-023-34981-4"
title: "From language models to large-scale food and biomedical knowledge graphs | Scientific Reports"
captured_on: "2026-04-21"
capture_method: "url"
assets_dir: "./assets"
---






[Download PDF](/articles/s41598-023-34981-4.pdf)








* Article
* [Open access](https://www.springernature.com/gp/open-science/about/the-fundamentals-of-open-access-and-open-research)
* Published: 15 May 2023


# From language models to large\-scale food and biomedical knowledge graphs


* [Gjorgjina Cenikj](#auth-Gjorgjina-Cenikj-Aff1-Aff2)[1](#Aff1),[2](#Aff2),
* [Lidija Strojnik](#auth-Lidija-Strojnik-Aff1)[1](#Aff1),
* [Risto Angelski](#auth-Risto-Angelski-Aff3)[3](#Aff3),
* [Nives Ogrinc](#auth-Nives-Ogrinc-Aff1)[1](#Aff1),
* [Barbara Koroušić Seljak](#auth-Barbara-Korou_i__Seljak-Aff1)[1](#Aff1) \&
* …
* [Tome Eftimov](#auth-Tome-Eftimov-Aff1)[1](#Aff1)

Show authors

[*Scientific Reports*](/srep)
**volume 13**, Article number: 7815 (2023)
 [Cite this article](#citeas)




* 7667 Accesses
* 16 Citations
* 5 Altmetric
* [Metrics details](/articles/s41598-023-34981-4/metrics)






## Abstract

Knowledge about the interactions between dietary and biomedical factors is scattered throughout uncountable research articles in an unstructured form (e.g., text, images, etc.) and requires automatic structuring so that it can be provided to medical professionals in a suitable format. Various biomedical knowledge graphs exist, however, they require further extension with relations between food and biomedical entities. In this study, we evaluate the performance of three state\-of\-the\-art relation\-mining pipelines (FooDis, FoodChem and ChemDis) which extract relations between food, chemical and disease entities from textual data. We perform two case studies, where relations were automatically extracted by the pipelines and validated by domain experts. The results show that the pipelines can extract relations with an average precision around 70%, making new discoveries available to domain experts with reduced human effort, since the domain experts should only evaluate the results, instead of finding, and reading all new scientific papers.



### Similar content being viewed by others





![](./assets/1e5366800369dd38.png)

### [A unified knowledge graph linking foodomics to chemical\-disease networks and flavor profiles](https://www.nature.com/articles/s41538-025-00680-9?fromPaywallRec=false)



Article
Open access
20 January 2026






![](./assets/b35c8a650dac757b.png)

### [Re\-examining chemically defined liquid diets through the lens of the microbiome](https://www.nature.com/articles/s41575-021-00519-0?fromPaywallRec=false)



Article
30 September 2021






![](./assets/1592af2b0111717b.png)

### [Knowledge enhancement and full utilization of document information for document\-level biomedical relation extraction](https://www.nature.com/articles/s41598-025-32931-w?fromPaywallRec=false)



Article
Open access
20 December 2025







 window.dataLayer \= window.dataLayer \|\| \[];
 window.dataLayer.push({
 recommendations: {
 recommender: 'semantic',
 model: 'e5',
 policy\_id: null,
 timestamp: 1776745417,
 embedded\_user: 'null'
 }
 });
 

## Introduction

Noncommunicable chronic diseases (NCDs) account for more than 70% of deaths worldwide. Cardiovascular diseases account for most NCD deaths (17\.9 M people annually), followed by cancers (9\.3 M), respiratory diseases (4\.1 M), and diabetes mellitus (1\.5 M)[1](/articles/s41598-023-34981-4#ref-CR1 "Lin, X. et al. Global, regional, and national burden and trend of diabetes in 195 countries and territories: An analysis from 1990 to 2025. Sci. Rep. 10, 1–11. 
                  https://doi.org/10.1038/s41598-020-71908-9
                  
                 (2020)."),[2](/articles/s41598-023-34981-4#ref-CR2 "Nguyen, L. S. et al. Systematic analysis of drug-associated myocarditis reported in the world health organization pharmacovigilance database. Nat. Commun. 13, 1–10 (2022)."). As the leading cause of death globally, most of the deaths that happen from cardiovascular diseases (CVDs) are due to heart attacks and strokes[3](/articles/s41598-023-34981-4#ref-CR3 "Sasson, C. et al. American heart association diabetes and cardiometabolic health summit: Summary and recommendations. J. Am. Heart Assoc. 7, e009271 (2018)."). A lot of scientific evidence indicates that between the most important risk factors for heart disease and stroke are unhealthy diet, alcohol and tobacco consumption, and physical activity. Among all the factors that contribute to the development and progression of CVDs, diet is one of the major ones[4](/articles/s41598-023-34981-4#ref-CR4 "Afshin, A. et al. Health effects of dietary risks in 195 countries, 1990–2017: A systematic analysis for the global burden of disease study 2017. Lancet 393, 1958–1972 (2019)."),[5](/articles/s41598-023-34981-4#ref-CR5 "Jayedi, A., Soltani, S., Abdolshahi, A. & Shab-Bidar, S. Healthy and unhealthy dietary patterns and the risk of chronic disease: An umbrella review of meta-analyses of prospective cohort studies. Br. J. Nutr. 124, 1133–1144 (2020)."). It has been shown that eating more fruit and vegetables and decreasing the salt in diet reduce the risk of CVDs.

Further, although there is a lot of knowledge about dietary effects on CVDs and broadly on NCDs, there are still many unresolved research questions. Such questions are not easy to be answered because food and nutrition in relation to diseases are described by various concepts and entities that interact in various ways[6](/articles/s41598-023-34981-4#ref-CR6 "Althoff, T., Nilforoshan, H., Hua, J. & Leskovec, J. Large-scale diet tracking data reveal disparate associations between food environment and diet. Nat. Commun. 13, 1–12 (2022)."). For instance, there are many foods (described by food entities) made up of components (described by chemical entities)[7](/articles/s41598-023-34981-4#ref-CR7 "Menichetti, G. & Barabasi, A. L. Nutrient concentrations in food display universal behaviour. Nat. Food 20, 20 (2022).") that may fight NCDs (described by disease entities) while others can be harmful[8](/articles/s41598-023-34981-4#ref-CR8 "Gibney, M. J. & Forde, C. G. Nutrition research challenges for processed food and health. Nat. Food 3, 104–109 (2022)."). These impacts are dependent on the combination of foods and their chemicals, the state of the food (e.g., raw/cooked, fresh/molded, etc.), the cooking method (e.g., steamed, grilled, baked, etc.), the health status of the person consuming food (e.g., healthy, ill, allergic) and others[9](/articles/s41598-023-34981-4#ref-CR9 "Micha, R. et al. Association between dietary factors and mortality from heart disease, stroke, and type 2 diabetes in the united states. JAMA 317, 912–924 (2017)."). As there are many combinations of these factors, collecting and structuring the relations between all the concepts and entities describing the impacts of food on NCDs is a very complex work exceeding human capabilities. And taking into account the fact that research in this field is still progressing, the related knowledge evolves on a daily basis, making it challenging to follow. Such knowledge further opens possibilities to use Artificial Intelligence (AI) methods to aid in the early detection (prediction) of NCDs as well as their progression. However, before developing predictive AI methods, unstructured (textual) data available in cohorts, electronic health records (EHRs), registries, and scientific and grey literature needs to be structured and normalized/linked to domain semantic resources and further included in knowledge bases (KBs) which can be utilized for predictive modeling and integrated into health systems which will make the information easily accessible to medical professionals. To this end, user interfaces play a critical role in ensuring that healthcare professionals can effectively utilize AI systems to provide high\-quality care to their patients[10](/articles/s41598-023-34981-4#ref-CR10 "Holzinger, A. & Müller, H. Toward human-ai interfaces to support explainability and causability in medical ai. Computer 54, 78–86. 
                  https://doi.org/10.1109/MC.2021.3092610
                  
                 (2021).").

A Knowledge Graph (KG) is a type of KB, where knowledge is stored in the form of entities characterized by some attributes, and relations connecting the entities. Conventional methods of KG construction can be broadly categorized into manual, and automatic, or semi\-automatic methods. The benefits of manual creation and curation approaches are their high precision and reliability[11](/articles/s41598-023-34981-4#ref-CR11 "Keseler, I. M. et al. Curation accuracy of model organism databases. Database
                  https://doi.org/10.1093/database/bau058
                  
                 (2014)."), however, due to the high amount of effort required by domain experts, they also have lower recall rates, poor scalability and time efficiency[12](/articles/s41598-023-34981-4#ref-CR12 "Yuan, J. et al. Constructing biomedical domain-specific knowledge graph with minimum supervision. Knowl. Inf. Syst. 62, 317–336. 
                  https://doi.org/10.1007/s10115-019-01351-4
                  
                 (2020)."). Automatic and semi\-automatic KG construction is enabled by text\-mining methods, which are able to extract entities and relations which can be structured as a KG.

In the biomedical domain, automatic and semi\-automatic structuring of textual data in the form of KGs is an active research area, which typically involves the use of Information Extraction (IE) pipelines consisting of multiple components. These components include Named Entity Recognition (NER) methods, which extract specific types of entities from raw text, Named Entity Linking (NEL) methods, whose goal is to map entity mentions to entries in a given KB, and Relation Extraction (RE) methods, which aim to automatically detect relations between entities[13](/articles/s41598-023-34981-4#ref-CR13 "Collovini, S., Machado, G. & Vieira, R. A sequence model approach to relation extraction in Portuguese. In Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC’16), 1908–1912 (European Language Resources Association (ELRA), 2016)."). Over the past 20 years, significant progress has been made in creating multiple IE pipelines for the biomedical domain. These pipelines primarily concentrate on identifying genotype and phenotype entities, as well as health\-related entities such as diseases, treatments, drugs, and others. To allow their development, several collaborative workshops, as part of conference events like BioNLP[14](/articles/s41598-023-34981-4#ref-CR14 "Nédellec, C. et al. Overview of bionlp shared task 2013. In Proceedings of the BioNLP shared task 2013 workshop, 1–7 (2013)."), BioCreative[15](/articles/s41598-023-34981-4#ref-CR15 "Leitner, F. et al. An overview of biocreative II 5. IEEE/ACM Trans. Comput. Biol. Bioinform. 7, 385–399 (2010)."), i2b2[16](/articles/s41598-023-34981-4#ref-CR16 "Sun, W., Rumshisky, A. & Uzuner, O. Evaluating temporal relations in clinical text: 2012 i2b2 challenge. J. Am. Med. Inform. Assoc. 20, 806–813 (2013)."), and DDIExtraction[17](/articles/s41598-023-34981-4#ref-CR17 "Segura-Bedmar, I., Martínez Fernández, P. & Sánchez Cisneros, D. The 1st ddiextraction-2011 challenge task: Extraction of drug–drug interactions from biomedical texts. In Proceedings of the 1st Challenge Task on Drug-Drug Interaction Extraction (Isabel Segura-Bedmar, Paloma Martínez, Daniel Sánchez-Cisneros, 2011)."), have been arranged to provide semantic resources (e.g., annotated corpora, ontologies) that will further allow the developing of biomedical IE pipelines. The efforts done in the biomedical domain are focused entirely on biomedical concepts and not investigating relations with food concepts. On the other side, most of the efforts done in IE in the food domain are focused on relations that do not involve health/biomedical concepts, and even more, are developed using static data that is already presented in some other resources (e.g., datasets, controlled vocabularies, ontologies), so they need to be updated when new data is available in these resources. In addition, only a few studies have concentrated on traditional text mining techniques that employ sentiment analysis through manual feature extraction[18](#ref-CR18 "Yang, H., Swaminathan, R., Sharma, A., Ketkar, V. & DSilva, J. Mining biomedical text towards building a quantitative food-disease-gene network. Learn. Struct. Schemas Doc. 20, 205–225 (2011)."),[19](#ref-CR19 "Miao, Q., Zhang, S., Meng, Y. & Yu, H. Polarity analysis for food and disease relationships. In 2012 IEEE/WIC/ACM International Conferences on Web Intelligence and Intelligent Agent Technology, vol. 1, 188–195 (IEEE, 2012)."),[20](/articles/s41598-023-34981-4#ref-CR20 "Ben Abdessalem Karaa, W., Mannai, M., Dey, N., Ashour, A. S. & Olariu, I. Gene-disease-food relation extraction from biomedical database. In Soft Computing Applications: Proceedings of the 7th International Workshop Soft Computing Applications (SOFA 2016), Vol 17, 394–407 (Springer, 2018)."). Despite this, the food and nutrition domain is low\-resourced in semantic data resources compared to the biomedical domain. There is a lack of annotated food\-disease relation corpora that serve as a benchmark and help develop IE pipelines. Even more, food semantic resources such as FoodOn[21](/articles/s41598-023-34981-4#ref-CR21 "Dooley, D. M. et al. Foodon: A harmonized food ontology to increase global food traceability, quality control and data integration. NPJ Sci. Food 2, 1–10 (2018)."), FoodEx2[22](/articles/s41598-023-34981-4#ref-CR22 "(EFSA), E. F. S. A. The food classification and description system foodex 2 (revision 2). Tech. Rep., Wiley Online Library (2015)."), are still under development (i.e., frequently updating them with new data) to support IE activities.

To bridge the gap between the food and biomedical domains, we introduce an approach that uses *language models to extract the relations* that exist between *food, chemical, and disease entities* and further *normalize* them to *allow the creation of a KG*. In our case, we evaluate the approach to trace the new knowledge about CVDs and milk products. The benefit of our approach is that we are not using the information that already exists in some static resources (e.g., databases), but try to catch all relations from textual data related to CVDs and milk products (milk was selected as a case study since it is rich in nutrients, a resource of proteins, vitamins, minerals, and fatty acids, which have an important impact on human metabolism and health) available in scientific abstracts, where new findings are presented. This makes the methodology easy to apply on new corpora of scientific abstracts, where the results of the pipelines can point out areas where the KG should be updated with new entities or relations.

## Related work

A recent survey on knowledge\-based biomedical data science[23](/articles/s41598-023-34981-4#ref-CR23 "Callahan, T. J., Tripodi, I. J., Pielke-Lombardo, H. & Hunter, L. E. Knowledge-based biomedical data science. Annu. Rev. Biomed. Data Sci. 3, 23–41. 
                  https://doi.org/10.1146/annurev-biodatasci-010820-091627
                  
                 (2020).") highlights the application of KGs in the biomedical and clinical domain in improving the retrieval of information from large sources of clinical data or literature[24](#ref-CR24 "Chen, Q. & Li, B. Retrieval method of electronic medical records based on rules and knowledge graph (2018)."),[25](#ref-CR25 "Liu, X. et al. Patienteg dataset: Bringing event graph model with temporal relations to electronic medical records. 
                  arXiv:1812.09905
                  
                 (2018)."),[26](/articles/s41598-023-34981-4#ref-CR26 "Liu, Z., Peng, E., Yan, S., Li, G. & Hao, T. T-know: A knowledge graph-based question answering and information retrieval system for traditional Chinese medicine. In COLING (2018)."), providing evidence to support phenomena observed in data[27](/articles/s41598-023-34981-4#ref-CR27 "Bakal, G., Talari, P., Kakani, E. V. & Kavuluru, R. Exploiting semantic patterns over biomedical knowledge graphs for predicting treatment and causative relations. J. Biomed. Inform. 82, 189–199. 
                  https://doi.org/10.1016/j.jbi.2018.05.003
                  
                 (2018)."),[28](/articles/s41598-023-34981-4#ref-CR28 "Schwertner, M. A., Rigo, S. J., Araújo, D. A., Silva, A. B. & Eskofier, B. Fostering natural language question answering over knowledge bases in oncology EHR. In 2019 IEEE 32nd International Symposium on Computer-Based Medical Systems (CBMS), 501–506. 
                  https://doi.org/10.1109/CBMS.2019.00102
                  
                 (2019)."), using link prediction to complete missing information and hypothesize previously unknown relationships[29](/articles/s41598-023-34981-4#ref-CR29 "Liang, X. et al. Predicting biomedical relationships using the knowledge and graph embedding cascade model. PLoS One 14, 1–23. 
                  https://doi.org/10.1371/journal.pone.0218264
                  
                 (2019)."), and improving patient data representation[30](#ref-CR30 "Aziguli, Zhang, Y., Xie, Y., Xu, Y. & Chen, Y. Structural technology research on symptom data of Chinese medicine. In 2017 IEEE 19th International Conference on e-Health Networking, Applications and Services (Healthcom), 1–4. 
                  https://doi.org/10.1109/HealthCom.2017.8210797
                  
                 (2017)."),[31](#ref-CR31 "Shang, J., Xiao, C., Ma, T., Li, H. & Sun, J. Gamenet: Graph augmented memory networks for recommending medication combination. 
                  arXiv:1809.01852
                  
                 (2019)."),[32](/articles/s41598-023-34981-4#ref-CR32 "Huang, E., Wang, S. & Zhai, C. Visage: Integrating external knowledge into electronic medical record visualization. In Pacific Symposium on Biocomputing. Pacific Symposium on Biocomputing 23, 578–589 (2018)."). In the biomedical domain, IE pipelines have been developed for the extraction of drug\-disease relations[33](/articles/s41598-023-34981-4#ref-CR33 "Xu, R. & Wang, Q. Large-scale extraction of accurate drug-disease treatment pairs from biomedical literature for drug repurposing. BMC Bioinform. 14, 181. 
                  https://doi.org/10.1186/1471-2105-14-181
                  
                 (2013)."),[34](/articles/s41598-023-34981-4#ref-CR34 "Chen, E. S., Hripcsak, G., Xu, H., Markatou, M. & Friedman, C. Automated acquisition of disease drug knowledge from biomedical and clinical documents: An initial study. J. Am. Med. Inform. Assoc. 15, 87–98. 
                  https://doi.org/10.1197/jamia.M2401
                  
                 (2008).") and disease\-symptom relations[35](/articles/s41598-023-34981-4#ref-CR35 "Xia, E. et al. Mining disease-symptom relation from massive biomedical literature and its application in severe disease diagnosis. AMIA Annu. Symp. Proc. 2018, 1118–1126 (2018).") from biomedical literature. A Coronavirus KG has been constructed by merging the Analytical Graph, with a collection of published scientific articles[36](/articles/s41598-023-34981-4#ref-CR36 "Zhang, P. et al. Toward a coronavirus knowledge graph. Genes
                  https://doi.org/10.3390/genes12070998
                  
                 (2021)."). A PubMed KG has been constructed by extracting biomedical entities from PubMed abstracts and enriching it with funding, author, and affiliation data[37](/articles/s41598-023-34981-4#ref-CR37 "Xu, J. et al. Building a PubMed knowledge graph. Sci. Data
                  https://doi.org/10.1038/s41597-020-0543-2
                  
                 (2020)."). A recent work[12](/articles/s41598-023-34981-4#ref-CR12 "Yuan, J. et al. Constructing biomedical domain-specific knowledge graph with minimum supervision. Knowl. Inf. Syst. 62, 317–336. 
                  https://doi.org/10.1007/s10115-019-01351-4
                  
                 (2020).") proposes the construction of domain\-specific KGs with minimal supervision, which is able to derive open\-ended relations from unstructured biomedical articles without the need of extensive labeling. While this study is largely focused on data integration, and only uses NER to extract the biomedical entities from the literature, our study goes a step further in the RE task, to extract the relations between the entities based on the text in the scientific abstracts, so that new relations can be added between entities in existing resources. Apart from using biomedical scientific papers as a source of information, EHRs have also been used for extracting disease\-symptom relations[38](/articles/s41598-023-34981-4#ref-CR38 "Rotmensch, M., Halpern, Y., Tlimat, A., Horng, S. & Sontag, D. Learning a health knowledge graph from electronic medical records. Sci. Rep. 7, 5994. 
                  https://doi.org/10.1038/s41598-017-05778-z
                  
                 (2017).") and constructing a medical KG with nine biomedical entity types[39](/articles/s41598-023-34981-4#ref-CR39 "Li, L. et al. Real-world data medical knowledge graph: Construction and applications. Artif. Intell. Med. 103, 25 (2020).").

In the food domain, FoodKG has been recently developed for representing food recipe data including their ingredients and nutritional content[40](/articles/s41598-023-34981-4#ref-CR40 "Haussmann, S. et al. Foodkg: A semantics-driven knowledge graph for food recommendation. In International Semantic Web Conference, 146–162 (Springer, 2019).") by enriching a large amount of recipe data from Recipe1M dataset with the nutritional information available from USDA’s National Nutrient Database for Standard Reference represented with FoodOn[21](/articles/s41598-023-34981-4#ref-CR21 "Dooley, D. M. et al. Foodon: A harmonized food ontology to increase global food traceability, quality control and data integration. NPJ Sci. Food 2, 1–10 (2018).") semantic meta\-data. Additionally, FoodKG[41](/articles/s41598-023-34981-4#ref-CR41 "Gharibi, M., Zachariah, A. & Rao, P. Foodkg: A tool to enrich knowledge graphs using machine learning techniques. Front. Big Data 3, 12 (2020).") was developed by using the existing text and graph embedding techniques applied to a controlled vocabulary called AGROVOC, to model the relations that exist in a plethora of datasets related to food, energy and water.

## Results

To trace the knowledge about food, chemical, and disease interactions, we have shown the creation of a KG centered around the impact of different foods and chemicals on CVDs, and the other targeting the composition of the selected food item “milk”, as well as its beneficial and detrimental effects on different NCDs. For this purpose, three NLP pipelines, called FooDis, FoodChem, and ChemDis, were combined to extract “food\-disease”, “food\-chemical”, and “chemical\-disease” relations from textual data. Semantically, we distinguish two relations between food\-disease and chemical\-disease entity pairs, which are “treat” and “cause”. In the case of food\-chemical entity pairs, we extracted only one relation which is “contains”. All three pipelines were executed twice, on two different corpora, one that was collected for CVDs and one collected for milk products. In both use cases, the searched keywords were selected by domain experts. In the CVDs case, a more general keyword was selected “heart disease food”, since we would like to retrieve broader aspects between different cardiovascular events and food products. This ends up with 9984 abstracts. In the milk use case, three keywords were selected by the domain experts i.e., “milk composition”, “milk disease”, and “milk health benefits”.

Table [1](/articles/s41598-023-34981-4#Tab1)a presents the number of abstracts that were retrieved and used in the analysis for both use cases, together with the keywords used to retrieve them, while Table [1](/articles/s41598-023-34981-4#Tab1)b presents the number of relations that were extracted for both use cases.



**Table 1 Number of processed paper abstracts and number of extracted relations for each case study.**

[Full size table](/articles/s41598-023-34981-4/tables/1)Figure [1](/articles/s41598-023-34981-4#Fig1)a features the KG constructed by running the three pipelines for the two application use cases. The same nodes are grouped together by normalizing the extracted food, chemical, and disease entities.



**Figure 1**

![Figure 1](./assets/10e546a086296096.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41598-023-34981-4/figures/1)Knowledge graph constructed using the FooDis, FoodChem and ChemDis pipelines. The nodes in green represent the food entities, the nodes in blue represent the chemical entities, and the nodes in red represent the disease entities. The red, green, and blue edges represent the “cause”, “treat” and “contains” relations, respectively. The figures have been generated using the pyvis python library[42](/articles/s41598-023-34981-4#ref-CR42 "Pyvis: Interactive network visualizations. 
                  https://pyvis.readthedocs.io/en/latest/
                  
                . Accessed 03 Mar 2023."), version 0\.1\.8\.2\.

To go into more detail how the KG is constructed, in Fig. [1](/articles/s41598-023-34981-4#Fig1)b we present an example using the relations extracted for the “heart failure” disease entity. The green nodes, “meat products”, “salt” and “dietary fish oil” represent the food entities for which the FooDis pipeline extracted a relation with the “heart failure” disease entity, meaning that they have some effect on its development or treatment. In particular, the red edges connecting the “heart failure” disease entity and the food entities “meat products”, and “salt” indicate that the pipeline identified a “cause” relation, i.e. meat products, and salt can contribute to the occurrence of heart failure. On the other hand, the green edge between the “dietary fish oil” entity and the “heart failure” disease entity indicates a “treat” relation, i.e. the pipeline identified that dietary fish oil has a beneficial effect to heart failure. Similarly, the ChemDis pipeline identified that the chemical entities “DHA”, “ester”, “acid, n\-3 fatty”, “antidiabetics canagliflozin”, “omega\-3 fatty acid” and “calcium” can be used for treating “heart failure”, while the chemical entities “(\-)\-cocaine” and “vitamin E” can contribute to the development of “heart failure”. Table [2](/articles/s41598-023-34981-4#Tab2) presents the supporting sentences from scientific abstracts from which the relations were extracted and further used for constructing the graph presented in Fig. [1](/articles/s41598-023-34981-4#Fig1)b. Next, such graphs are connected based on the same entities to link the information from different abstracts. Further, to validate the extracted information, domain experts were involved to check the extracted relations for both use cases.



**Table 2 Supporting sentences for the relations of entity “heart failure” to different food and chemical entities.**

[Full size table](/articles/s41598-023-34981-4/tables/2)### Use case: cardiovascular diseases

For the CVDs use case, a highly\-skilled domain expert (an MD with more than 40 years of working experience in cardiology) evaluated the extractions from the three pipelines. The relations that were evaluated are extracted after the “Final relation determination” step from the FooDis, FoodChem and ChemDis pipelines. All three pipelines utilized here follow the same workflow. Each extracted relation is determined by all sentences where information about it is presented. We called them “supporting sentences”. The sentences can be from the same or different abstracts, since information about the same relation can be investigated in different papers.

#### Domain expert evaluation

Each pipeline provides the result as a 6\-tuple i.e., (name of the first entity, named of the second entity, synonyms for the first entity, synonyms for the second entity, relation, supporting sentences), which is further evaluated by the domain expert. The domain expert was asked to assign a binary indicator of the truthfulness of the relation. The pipelines were then evaluated by taking the mean of the correctness indicators assigned by the annotator for each relation and pipeline, which we refer to as the precision in the remainder of this section. In particular, if a pipeline extracted three relations, and the expert marked two of these as correct (binary indicators 1,0,1\), the reported precision would be 0\.66\.



**Figure 2**

![Figure 2](./assets/f8746545da3ba828.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41598-023-34981-4/figures/2)Number of extracted and evaluated relations and mean precision of each pipeline for the heart disease study. The plots have been generated using the plotly python library[43](/articles/s41598-023-34981-4#ref-CR43 "Plotly: Low-code data app development. 
                  https://plotly.com/
                  
                . Accessed 03 Mar 2023."), version 5\.7\.0\.

Figure [2](/articles/s41598-023-34981-4#Fig2)a presents the number of relations extracted by each of the pipelines for the CVDs study, and the number of relations that the domain expert evaluated. We need to point out here that all extracted relations were provided to the domain expert, however, the evaluation has been performed only on those relations for which the domain expert has expert knowledge. Because of this, the human evaluation process covers 44% of the “contains” relations extracted by the FoodChem pipeline, 33% of the “treat” relations extracted by the FooDis pipeline, 26% of the “cause” relations extracted by the FooDis pipeline, 26% of the “cause” relations extracted by the ChemDis pipeline, and 23% of the “treat” relations extracted by the ChemDis pipeline.

The mean precision of each of the pipelines (FooDis, ChemDis, and FoodChem) in the CVDs use case is presented in Fig. [2](/articles/s41598-023-34981-4#Fig2)b. From it, the FooDis pipeline achieves the highest precision of 0\.79 for the “cause” and 0\.78 for the “treat” relation. The lowest precision of 0\.68 is achieved by the ChemDis pipeline for the extraction of the “cause” relation.

Since the three pipelines extract a relation based on supporting sentences, in the [Supplementary Materials](/articles/s41598-023-34981-4#MOESM1), we have presented the distribution of the number of relations versus their number of supporting sentences.

All of the pipelines extract more than 74% of the relations based on a single supporting sentence. The ChemDis and FoodChem pipelines can find a larger number of supporting sentences for some relations compared to the FooDis pipeline. In particular, the ChemDis pipeline can find up to five supporting sentences to identify “cause” relations and up to 14 supporting sentences to identify “treat” relations, while the FooDis pipeline uses up to three, and four supporting sentences for the “cause” and “treat” relations, respectively.

Next, to see how the mean precision is affected by the number of supporting sentences, we analyze for each semantic relation separately. The results are presented in [Supplementary Materials](/articles/s41598-023-34981-4#MOESM1). From the conducted analysis, we can conclude that the mean precision is proportional to the number of supporting sentences. Almost for all relations, a precision of 1\.00 is reached when the number of supporting relations is sufficiently high. This indicates that when the number of supporting sentences for a relation increases, there is an agreement between the domain expert validation and the result provided by our pipelines, with some exceptions listed in the [Supplementary Materials](/articles/s41598-023-34981-4#MOESM1).

#### Error analysis

Next, we analyze the types of false discoveries produced by FooDis, FoodChem, and ChemDis pipelines.

Figure [3](/articles/s41598-023-34981-4#Fig3) features the relations with the highest number of supporting sentences for four chemical entities: “carbohydrates”, “fatty acid”, “sodium” and “vitamin d”. Here the results for the selected chemical entity from the two pipelines that deal with chemical entities (i.e., ChemDis and FoodChem) are presented. The green bars refer to the number of sentences in which the relation was correctly identified, while the purple plots refer to the number of false positive sentences for that relation, i.e. sentences where the relation was identified, however, it was marked as incorrect by the experts.

For the “carbohydrates” entity, the ChemDis pipeline produced the false positive relation “carbohydrates\-treat\-cardiomyopathy” when the supporting sentences suggested that a low\-carbohydrate diet is recommended for treating cardiomyopathy. In this case, the pipeline fails to identify that a reduction of the chemical entity is required to treat the disease. In addition, the FoodChem pipeline produces a false discovered relation “bulk\-contains\-carbohydrates”, when the supporting sentence was saying that these two entities are contained in another entity, “dry beans”. For the “fatty acid” chemical entity, the ChemDis pipeline produced the false positive relation “fatty acid\-cause\-dysfunction endothelial”, when the supporting sentence was saying that increased fatty acid levels and endothelial dysfunction were contributing to the development of another disease, “sepsis”. The FoodChem pipeline produced the false entities, “wine\-contains\-fatty acid” and “acid fatty trans\-contains\-fatty acid”. In the first case, the two entities were co\-occurring in the supporting sentence without any relation, while in the second one, the sentence was saying that trans fatty acids are a subcategory of fatty acids. In the case of the “sodium” chemical entity, most of the sentences extracted by the ChemDis pipeline express the correct relation, however, sodium is incorrectly extracted as a partial match of the entity “Sodium\-glucose co\-transporter 2 inhibitors (SGLT2is)”. In the case of “vitamin d”, all of the false positive “cause” relations extracted by the ChemDis pipeline are due to the pipeline not recognizing that the deficiency of the vitamin was causing the diseases.



**Figure 3**

![Figure 3](./assets/439c4c3cd7d4c3d8.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41598-023-34981-4/figures/3)Top 10 “cause”, “treat”, and “contains” relations with maximum number of supporting sentences for four chemical entities: “carbohydrates”, “fatty acid”, “sodium” and “vitamin d”. The entities in the rows of the ChemDis pipeline are diseases caused or treated by the chemical, while the entities in the rows of the FoodChem pipeline are food entities in which the chemical is contained.

Figure [4](/articles/s41598-023-34981-4#Fig4) features the top 10 relations with a maximal number of supporting sentences for three disease entities. Here, we present the results from pipelines that are dealing with disease entities (i.e., FooDis and ChemDis). For the “general cardiovascular disorders” entity, the pipelines extracted the relations “dietary vegetable\-cause\-general cardiovascular disorders”, “acid, saturated fatty\-treat\-general cardiovascular disorders”, “acid fatty polyunsaturated\-cause\-general cardiovascular disorders”, “cholesterol\-treat\-general cardiovascular disorders” due to the fact that the pipelines were not able to recognize that the sentences were referring to the reduction of these food or chemical entities affecting the disease development or treatment of the general cardiovascular disorders. This is also the reason for false positive relations extraction for the other two disease entities featured in the figure.



**Figure 4**

![Figure 4](./assets/ed008103a3d4033e.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41598-023-34981-4/figures/4)Top 10 “cause” and “treat” relations with maximal number of supporting sentences related to three disease entities: “general cardiovascular disorders”, “diabetes”, and “obesity”. The entities listed in the rows of the FooDis pipeline are food entities, while the entities listed in the rows of the ChemDis pipeline are chemical entities, that cause or treat the specified disease.

### Use case: milk

For the use case related to the composition and health effects of milk, two highly\-skilled domain experts evaluated the results from all three pipelines: a chemist and a food and nutritional scientist.

#### Domain expert evaluation

From the 33,111 processed abstracts related to the milk case study, the three pipelines extracted a total of 6792 relations, from which 5139 were evaluated by the two domain experts. We need to point out again that all extracted relations were provided to the domain experts, however, they evaluated only those relations for which they have domain expertise. Figure [5](/articles/s41598-023-34981-4#Fig5)a features the number of relations extracted by each pipeline for the milk case study, and the number of relations the experts evaluated. The highest number of evaluated relations were the “contains” relations extracted by the FoodChem pipeline, and the experts were able to evaluate 96% of them (2849 out of 2754\). The experts also evaluated 73% of the “treat” and 78% of the “cause” relations produced by the FooDis, 34% of the “cause” relations, and 35% of the “treat” relations produced by the ChemDis pipeline.



**Figure 5**

![Figure 5](./assets/5cad585be1405eaf.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41598-023-34981-4/figures/5)Number of extracted and evaluated relations and mean precision of each pipeline for the milk study. The plots have been generated using the plotly python library[43](/articles/s41598-023-34981-4#ref-CR43 "Plotly: Low-code data app development. 
                  https://plotly.com/
                  
                . Accessed 03 Mar 2023."), version 5\.7\.0\.

The mean precision for each of the five semantic relations for both domain experts is presented in Fig. [5](/articles/s41598-023-34981-4#Fig5)b separately. In addition, we have also presented the mean precision for each type of relation by averaging the precision across both domain experts. From the figure, we can see that the first domain expert, who evaluated the relations which were supported by a single sentence, identified more incorrect relations than the second domain expert, who evaluated the relations supported by multiple sentences.

The overall mean precision for each of the five relations averaged across both domain experts are as follows:

* 0\.51 for the “cause” relation extracted by the ChemDis pipeline,
* 0\.79 for the “treat” relation extracted by the ChemDis pipeline,
* 0\.65 for the “cause” relation extracted by the FooDis pipeline,
* 0\.70 for the “treat” relation extracted by the FooDis pipeline,
* 0\.70 for the “contains” relation extracted by the FoodChem pipeline.

The error analysis for the milk case study followed the same procedure as for the heart disease study and resulted in similar findings, presented in the [Supplementary Materials](/articles/s41598-023-34981-4#MOESM1).

## Discussion

Going through the two use cases, it is obvious that the proposed methodology can be used to structure the new knowledge that is coming rapidly with new scientifically published papers. On average, the precision of each extracted relation is around 70%. This indicates that the pipelines allow us to trace the knowledge and make it available to domain experts. This reduces the time required by the domain experts, since they should only evaluate the results, instead of finding and reading all new papers.

Even though the pipelines can contribute to the automation of the KG construction process and reduce the efforts required by the experts in structuring scientific text, there are still opportunities for further improvements. A large portion of the incorrectly extracted relations is due to the partial extraction of entities, especially by the food NER methods, which is a consequence of the simple dictionary\-based approach. We want to point out here that in initial experiments, we also considered other food NER methods that are corpus\-based and involve the training of a ML model on text annotated with food entities. At that time, BuTTER[44](/articles/s41598-023-34981-4#ref-CR44 "Cenikj, G., Popovski, G., Stojanov, R., Koroušić Seljak, B. & Eftimov, T. Butter: Bidirectional lstm for food named-entity recognition. In Proceedings of Big Food and Nutrition Data Management and Analysis at IEEE BigData 2020, 3550–3556. 
                  https://doi.org/10.1109/BigData50022.2020.9378151
                  
                 (2020).") and FoodNER[45](/articles/s41598-023-34981-4#ref-CR45 "Stojanov, R., Popovski, G., Cenikj, G., Koroušić Seljak, B. & Eftimov, T. FoodNER: A fine-tuned BERT for food named-entity recognition. J. Med. Internet Res. (2021) (In press).") were the only corpus\-based food NER models. However, because these models were trained on food recipe text, which is very different from scientific text both in the contents and the writing style, the models failed to generalize to scientific text and did not produce satisfactory results. As far as the chemical and disease NER models are concerned, we chose to use the SABER method, since it performs both the NER and NEL tasks and is reported to have good predictive performance.

Further extension of the pipelines is needed to capture quantities, i.e. whether a surplus or a deficit of the entities in question lead to the development or treatment of the diseases. Some of the relations are false positives due to mistakes made by the RE models, for instance, where a relation was extracted between entities that simply co\-occur in a sentence without any relation, or the relation is expressed in the sentence, but between different entities. The RE models produce such errors, especially in the case where a single sentence contains a lot of entities or expresses multiple relations. This is likely due to the RE models extracting the “cause” and “treat” relations being trained using transfer learning, and the RE models extracting the “contains” relation being trained using small amounts of manually annotated data. The annotations produced as part of this study can be used to re\-train the RE models using larger quantities of high\-quality data.

From the point of view of assessing the importance of milk in our diet, it is crucial to assess the large amount of data available to obtain consistent outcomes and to evaluate the advantages and disadvantages of milk consumption. The presented approach can provide evidence that can be used to develop or renew dietary and health guidelines for relevant decision\-makers.

## Methods

In this study, three relation mining pipelines (FooDis, FoodChem and ChemDis) are used to extract relations between food, chemical, and disease entities, from the raw text of abstracts of biomedical scientific textual data.

The pipelines follow a common template, which is presented in Fig. [6](/articles/s41598-023-34981-4#Fig6). The initial step is querying PubMed and retrieving abstracts of scientific papers. Different Named Entity Recognition (NER) and Named Entity Linking (NEL) methods are applied for the extraction of food, chemical, and disease entities, which are linked to existing resources in the biomedical and food domain.



**Figure 6**

![Figure 6](./assets/5eac5eff9f16408c.png)The alternative text for this image may have been generated using AI.[Full size image](/articles/s41598-023-34981-4/figures/6)Overview of the general pipeline template.

Next, sentences that express facts or analysis of the research and contain at least one pair of different entities are extracted from the abstracts. Abstracts typically include the objective, hypothesis, methodology, and main findings of the research. However, not all of these pieces of information are reliable sources for drawing conclusions, since if the authors’ hypothesis was untrue, and we were to extract information from the sentence that describes that hypothesis, our findings would be incorrect. For this reason, it is necessary to identify sentences which describe the objective, hypothesis, or methodology of the research and only extract relations from the sentences which describe the research findings or previously known facts.

The sentences are annotated for the existence of a “cause”, “treat” or “contains” relation, and the entity pairs are connected with one of these relations on the basis of the gathered evidence.

### Named entity recognition

#### Food named entity recognition

Even though corpus\-based methods have already been developed for the food domain[44](/articles/s41598-023-34981-4#ref-CR44 "Cenikj, G., Popovski, G., Stojanov, R., Koroušić Seljak, B. & Eftimov, T. Butter: Bidirectional lstm for food named-entity recognition. In Proceedings of Big Food and Nutrition Data Management and Analysis at IEEE BigData 2020, 3550–3556. 
                  https://doi.org/10.1109/BigData50022.2020.9378151
                  
                 (2020)."),[45](/articles/s41598-023-34981-4#ref-CR45 "Stojanov, R., Popovski, G., Cenikj, G., Koroušić Seljak, B. & Eftimov, T. FoodNER: A fine-tuned BERT for food named-entity recognition. J. Med. Internet Res. (2021) (In press)."), these methods are trained on the FoodBase corpus[46](/articles/s41598-023-34981-4#ref-CR46 "Popovski, G., Seljak, B. K. & Eftimov, T. FoodBase corpus: A new resource of annotated food entities. Database
                  https://doi.org/10.1093/database/baz121(2019)
                  
                 (2019)."), which contains recipe texts. As was observed in our experiments, when applied on scientific text, the corpus\-based methods have poor generalization, so in order to extract the food entities, we opted for a simpler, dictionary\-based approach which uses a dictionary of food names extracted from the Unified Medical Language System (UMLS) Metathesaurus, which is not dependent on the data used for training the model. For this purpose, we use the MRSTY and MRCONSO tables from the UMLS Rich Release Format files[47](/articles/s41598-023-34981-4#ref-CR47 "Metathesaurus-Rich Release Format (RRF), UMLS® Reference Manual. 
                  https://www.ncbi.nlm.nih.gov/books/NBK9685/
                  
                . Accessed 15 Dec 2021."). The construction of the dictionary involves two steps: extracting the identifiers of all concepts with the semantic type “food” from the MRSTY table, and extracting all of the names used to refer to each of the food concepts from the MRCONSO table. In this dictionary, we have a total of 36,836 instances. By matching the words in the abstracts with the names of food entities defined in the dictionary extracted from the UMLS, we are also able to perform the NEL task, i.e. link the extracted food entities with their identifiers in the UMLS, and further find their identifiers in other KBs to which the UMLS identifiers are linked.

#### Disease named entity recognition

The Sequence Annotator for Biomedical Entities and Relations (SABER)[48](/articles/s41598-023-34981-4#ref-CR48 "Giorgi, J. M. & Bader, G. D. Towards reliable named entity recognition in the biomedical domain. Bioinformatics 36, 280–286. 
                  https://doi.org/10.1093/bioinformatics/btz504
                  
                 (2019).") is a tool providing several pre\-trained models for biomedical NER and NEL, using a neural network architecture consisting of Bidirectional Long Short\-Term Memory and Conditional Random Fields. We use the DISO pre\-trained model to extract disease entities, which can be “Acquired Abnormality”, “Anatomical Abnormality”, “Cell or Molecular Dysfunction”, “Congenital Abnormality”, “Pathologic Function”, “Disease or Syndrome”, “Mental or Behavioral Dysfunction”, “Neoplastic Process”, “Sign or Symptom”. Apart from identifying these entities, SABER can also perform NEL, i.e. link the extracted entities to identifiers in the Disease Ontology[49](/articles/s41598-023-34981-4#ref-CR49 "Schriml, L. M. et al. Human disease ontology 2018 update: Classification, content and workflow expansion. Nucleic Acids Res. 47, D955–D962. 
                  https://doi.org/10.1093/nar/gky1032
                  
                 (2018).").

#### Chemical named entity recognition

We use the pre\-trained model CHED from the SABER[48](/articles/s41598-023-34981-4#ref-CR48 "Giorgi, J. M. & Bader, G. D. Towards reliable named entity recognition in the biomedical domain. Bioinformatics 36, 280–286. 
                  https://doi.org/10.1093/bioinformatics/btz504
                  
                 (2019).") tool to extract chemical entities which can be mentioned in the text using common and trademark names, abbreviations, molecular formulas, chemical database identifiers, and names defined in the nomenclature of the International Union of Pure and Applied Chemistry. SABER is also capable of linking the extracted chemical entities to the PubChem database[50](/articles/s41598-023-34981-4#ref-CR50 "Kim, S. et al. new data content and improved web interfaces. Nucleic Acids Res. 49, D1388–D1395. 
                  https://doi.org/10.1093/nar/gkaa971(2020)
                  
                 (2021).").

### Relation extraction

#### SAFFRON relation extraction model

SAFFRON[51](/articles/s41598-023-34981-4#ref-CR51 "Cenikj, G., Eftimov, T. & Koroušić Seljak, B. SAFFRON: TranSfer leArning for food-disease RelatiOn extractioN. In Proceedings of the 20th Workshop on Biomedical Language Processing, 30–40. 
                  https://doi.org/10.18653/v1/2021.bionlp-1.4
                  
                 (Association for Computational Linguistics, Online, 2021).") is a RE model which employs transfer learning to identify “cause” or “treat” relations. BERT[52](/articles/s41598-023-34981-4#ref-CR52 "Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. Bert: Pre-training of deep bidirectional transformers for language understanding. 
                  arXiv:1810.04805
                  
                 (arXiv preprint) (2018)."), RoBERTa[53](/articles/s41598-023-34981-4#ref-CR53 "Liu, Y. et al. Roberta: A robustly optimized BERT pretraining approach (2019). 
                  arXiv:1907.11692
                  
                 (CoRR).") and BioBERT[54](/articles/s41598-023-34981-4#ref-CR54 "Lee, J. et al. BioBERT: A pre-trained biomedical language representation model for biomedical text mining. Bioinformatics 36, 1234–1240. 
                  https://doi.org/10.1093/bioinformatics/btz682
                  
                 (2019).") models are trained on data that is annotated for the existence of “cause” and “treat” relations between different types of biomedical entities in the CrowdTruth[55](#ref-CR55 "Dumitrache, A., Aroyo, L. & Welty, C. Crowdsourcing ground truth for medical relation extraction. ACM Trans. Interact. Intell. Syst. 8, 25 (2017) 
                  arXiv:1701.02185
                  
                ."),[56](#ref-CR56 "Dumitrache, A., Aroyo, L. & Welty, C. Crowdtruth measures for language ambiguity: The case of medical relation extraction. CEUR Workshop Proc. 1467, 7–19 (2015)."),[57](/articles/s41598-023-34981-4#ref-CR57 "Dumitrache, A., Aroyo, L. & Welty, C. Achieving expert-level annotation quality with crowdtruth: The case of medical relation extraction. In BDM2I@ISWC (2015)."), Adverse Drug Events[58](/articles/s41598-023-34981-4#ref-CR58 "Gurulingappa, H., Mateen-Rajput, A. & Toldo, L. Extraction of potential adverse drug events from medical case reports. J. Biomed. Semant. 3, 15–15. 
                  https://doi.org/10.1186/2041-1480-3-15
                  
                 (2012).") and the FoodDisease datasets[59](/articles/s41598-023-34981-4#ref-CR59 "Cenikj, G., Koroušić Seljak, B. & Eftimov, T. FoodChem: A food-chemical relation extraction model. In 2021 IEEE Symposium Series on Computational Intelligence (SSCI) Proceedings (2021)."). We choose to use the Single Sequence Classifier (SSC) models introduced in[51](/articles/s41598-023-34981-4#ref-CR51 "Cenikj, G., Eftimov, T. & Koroušić Seljak, B. SAFFRON: TranSfer leArning for food-disease RelatiOn extractioN. In Proceedings of the 20th Workshop on Biomedical Language Processing, 30–40. 
                  https://doi.org/10.18653/v1/2021.bionlp-1.4
                  
                 (Association for Computational Linguistics, Online, 2021)."), which are trained by fine\-tuning BioBERT and RoBERTa models to perform the RE task on the CrowdTruth and FoodDisease datasets, since these datasets are annotated for the existence of both the “cause” and the “treat” relation, unlike the models trained on the Adverse Drug Events dataset, which can only identify the “cause” relation. The occurrences of the biomedical entities in each annotated sentence are masked to prevent the models from learning relations between specific entities and teach them to instead recognize relations based on the context words used to express the relation, so they can successfully generalize to the task of recognizing the relations, regardless of the type of entities between which they occur. Each model outputs a binary indicator of the existence of a “cause” or “treat” relation.

The SAFFRON models are applied to each sentence that contains 2 entities of the required type (at least 1 food and 1 disease entity, or at least 1 food and 1 chemical entity), and expresses a “Fact” or “Analysis” of the research article. In particular, the 4 models (BioBERT trained on the FoodDisease dataset, RoBERTa trained on the FoodDisease dataset, BioBERT trained on the CrowdTruth dataset, RoBERTa trained on the CrowdTruth dataset) are applied for the extraction of each relation, “cause” or “treat”. A voting strategy is used to combine the binary predictions of the 8 models. A “cause” relation is assigned if at least 3 out of the 4 models which are trained to extract this relation produce a positive prediction, and at most 1 out of the 4 models which are trained to predict the “treat” relation produce a positive prediction and vice versa. If this condition is not satisfied for any of the “cause” or “treat” relations, the sentence is discarded.

#### FoodChem relation extraction model

The FoodChem RE model[59](/articles/s41598-023-34981-4#ref-CR59 "Cenikj, G., Koroušić Seljak, B. & Eftimov, T. FoodChem: A food-chemical relation extraction model. In 2021 IEEE Symposium Series on Computational Intelligence (SSCI) Proceedings (2021).") is used to extract the “contains” relations between food and chemical entities. For this purpose, 3 transformer\-based models (BERT, BioBERT and RoBERTa) are applied on each sentence that contains at least one food and one chemical entity, and expresses a “Fact” or “Analysis”. A voting scheme is implemented in such a way that a “contains” relation is assigned to a (food, chemical, sentence) triple if at least 2 of the 3 models produce a positive prediction for the existence of the relation. If less than 2 models produce a positive prediction, the triple is discarded.

### Pipelines

The FooDis, FoodChem and ChemDis pipelines follow the same methodological template and only differ in the NER and RE methods used to extract the entities and relations.

#### FooDis pipeline

The FooDis pipeline extracts “cause” and “treat” relations between food and disease entities. A dictionary\-based NER method using the food names in the Unified Medical Language System (UMLS) is applied to extract the food entities from the text of the abstracts. The SABER DISO model is used to extract the disease entities.

#### FoodChem pipeline

The FoodChem pipeline extracts “contains” relations between food and chemical entities. The entities are extracted using the corresponding NER methods, and the FoodChem RE model is applied to each sentence.

#### ChemDis pipeline

The ChemDis pipeline extracts “cause” and “treat” relations between chemical and disease entities. The pipeline components are identical to the FooDis pipeline, with the exception of the use of a different pre\-trained SABER model. In the ChemDis pipeline, the SABER CHED model is used to extract chemical entities, whereas in the FooDis pipeline, the SABER DISO model is used to extract disease entities.

### Knowledge graph construction

The three pipelines FooDis, FoodChem and ChemDis produce triples in the form of (entity1, relation, entity2\). Each entity is further linked to an external KB. Such outputs are naturally suited for the construction of a KG. The constructed KG contains nodes that represent the food, chemical and disease concepts from the external KBs, as determined by their unique identifiers. In the case when several terms can be used to refer to the same entity (i.e. the terms are synonyms), the terms are grouped by their unique identifiers. This means that the relations in which a unique entity is involved are determined based on all of the relations identified for its synonyms. In order to make the results more easily interpretable, instead of only using the identifiers in the constructed KG, we assign to each entity node one of the synonyms as its name. The edges in the constructed KG represent the “cause”, “treat” or “contains” relations.

## Conclusions

In this paper, we conduct an evaluation of three Information Extraction pipelines (FooDis, FoodChem and ChemDis). The pipelines extract relations between food, chemical, and disease entities from abstracts of scientific papers. Three domain experts evaluated the pipelines for two use cases, the first one being centered around cardiovascular diseases, and the second one targeting milk and milk products. This is the first application of the three pipelines where the results were evaluated by domain experts. The FoodChem pipeline, extracting “contains” relations between food and chemical entities, achieves a mean precision of 0\.70 when aggregated across the evaluation of the three experts. The ChemDis pipeline, capturing relations between chemical and disease entities, obtains a mean precision of 0\.56 for the extraction of the “cause” relation and 0\.79 for the “treat” relation. The FooDis pipeline achieves a mean precision of 0\.69 for the extraction of the “cause” relation and 0\.73 for the “treat” relation. The conducted evaluation and the expert consultation revealed potential directions for further improvement of the pipelines. The annotated data is also a valuable resource that can be used to retrain and improve the RE models.




## Data availibility


The relevant data is available at (<https://github.com/gjorgjinac/language_models_to_bio_kgs>).


## References

1. Lin, X. *et al.* Global, regional, and national burden and trend of diabetes in 195 countries and territories: An analysis from 1990 to 2025\. *Sci. Rep.* **10**, 1–11\. [https://doi.org/10\.1038/s41598\-020\-71908\-9](https://doi.org/10.1038/s41598-020-71908-9) (2020\).

[Article](https://doi.org/10.1038%2Fs41598-020-71908-9) 
 [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2020NatSR..10...21L) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3cXhvVSlsr%2FO) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Global%2C%20regional%2C%20and%20national%20burden%20and%20trend%20of%20diabetes%20in%20195%20countries%20and%20territories%3A%20An%20analysis%20from%201990%20to%202025&journal=Sci.%20Rep.&doi=10.1038%2Fs41598-020-71908-9&volume=10&pages=1-11&publication_year=2020&author=Lin%2CX)
2. Nguyen, L. S. *et al.* Systematic analysis of drug\-associated myocarditis reported in the world health organization pharmacovigilance database. *Nat. Commun.* **13**, 1–10 (2022\).

[Article](https://doi.org/10.1038%2Fs41467-021-27631-8) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB38XjtVGisLbK) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Systematic%20analysis%20of%20drug-associated%20myocarditis%20reported%20in%20the%20world%20health%20organization%20pharmacovigilance%20database&journal=Nat.%20Commun.&doi=10.1038%2Fs41467-021-27631-8&volume=13&pages=1-10&publication_year=2022&author=Nguyen%2CLS)
3. Sasson, C. *et al.* American heart association diabetes and cardiometabolic health summit: Summary and recommendations. *J. Am. Heart Assoc.* **7**, e009271 (2018\).

[Article](https://doi.org/10.1161%2FJAHA.118.009271) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=30371251) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6201457) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=American%20heart%20association%20diabetes%20and%20cardiometabolic%20health%20summit%3A%20Summary%20and%20recommendations&journal=J.%20Am.%20Heart%20Assoc.&doi=10.1161%2FJAHA.118.009271&volume=7&publication_year=2018&author=Sasson%2CC)
4. Afshin, A. *et al.* Health effects of dietary risks in 195 countries, 1990–2017: A systematic analysis for the global burden of disease study 2017\. *Lancet* **393**, 1958–1972 (2019\).

[Article](https://doi.org/10.1016%2FS0140-6736%2819%2930041-8) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Health%20effects%20of%20dietary%20risks%20in%20195%20countries%2C%201990%E2%80%932017%3A%20A%20systematic%20analysis%20for%20the%20global%20burden%20of%20disease%20study%202017&journal=Lancet&doi=10.1016%2FS0140-6736%2819%2930041-8&volume=393&pages=1958-1972&publication_year=2019&author=Afshin%2CA)
5. Jayedi, A., Soltani, S., Abdolshahi, A. \& Shab\-Bidar, S. Healthy and unhealthy dietary patterns and the risk of chronic disease: An umbrella review of meta\-analyses of prospective cohort studies. *Br. J. Nutr.* **124**, 1133–1144 (2020\).

[Article](https://doi.org/10.1017%2FS0007114520002330) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3cXit1KqtrjI) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32600500) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Healthy%20and%20unhealthy%20dietary%20patterns%20and%20the%20risk%20of%20chronic%20disease%3A%20An%20umbrella%20review%20of%20meta-analyses%20of%20prospective%20cohort%20studies&journal=Br.%20J.%20Nutr.&doi=10.1017%2FS0007114520002330&volume=124&pages=1133-1144&publication_year=2020&author=Jayedi%2CA&author=Soltani%2CS&author=Abdolshahi%2CA&author=Shab-Bidar%2CS)
6. Althoff, T., Nilforoshan, H., Hua, J. \& Leskovec, J. Large\-scale diet tracking data reveal disparate associations between food environment and diet. *Nat. Commun.* **13**, 1–12 (2022\).

[Article](https://doi.org/10.1038%2Fs41467-021-27522-y) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Large-scale%20diet%20tracking%20data%20reveal%20disparate%20associations%20between%20food%20environment%20and%20diet&journal=Nat.%20Commun.&doi=10.1038%2Fs41467-021-27522-y&volume=13&pages=1-12&publication_year=2022&author=Althoff%2CT&author=Nilforoshan%2CH&author=Hua%2CJ&author=Leskovec%2CJ)
7. Menichetti, G. \& Barabasi, A. L. Nutrient concentrations in food display universal behaviour. *Nat. Food* **20**, 20 (2022\).

[Google Scholar](http://scholar.google.com/scholar_lookup?&title=Nutrient%20concentrations%20in%20food%20display%20universal%20behaviour&journal=Nat.%20Food&volume=20&publication_year=2022&author=Menichetti%2CG&author=Barabasi%2CAL)
8. Gibney, M. J. \& Forde, C. G. Nutrition research challenges for processed food and health. *Nat. Food* **3**, 104–109 (2022\).

[Article](https://doi.org/10.1038%2Fs43016-021-00457-9) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37117956) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Nutrition%20research%20challenges%20for%20processed%20food%20and%20health&journal=Nat.%20Food&doi=10.1038%2Fs43016-021-00457-9&volume=3&pages=104-109&publication_year=2022&author=Gibney%2CMJ&author=Forde%2CCG)
9. Micha, R. *et al.* Association between dietary factors and mortality from heart disease, stroke, and type 2 diabetes in the united states. *JAMA* **317**, 912–924 (2017\).

[Article](https://doi.org/10.1001%2Fjama.2017.0947) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28267855) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5852674) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Association%20between%20dietary%20factors%20and%20mortality%20from%20heart%20disease%2C%20stroke%2C%20and%20type%202%20diabetes%20in%20the%20united%20states&journal=JAMA&doi=10.1001%2Fjama.2017.0947&volume=317&pages=912-924&publication_year=2017&author=Micha%2CR)
10. Holzinger, A. \& Müller, H. Toward human\-ai interfaces to support explainability and causability in medical ai. *Computer* **54**, 78–86\. [https://doi.org/10\.1109/MC.2021\.3092610](https://doi.org/10.1109/MC.2021.3092610) (2021\).

[Article](https://doi.org/10.1109%2FMC.2021.3092610) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Toward%20human-ai%20interfaces%20to%20support%20explainability%20and%20causability%20in%20medical%20ai&journal=Computer&doi=10.1109%2FMC.2021.3092610&volume=54&pages=78-86&publication_year=2021&author=Holzinger%2CA&author=M%C3%BCller%2CH)
11. Keseler, I. M. *et al.* Curation accuracy of model organism databases. *Database*[https://doi.org/10\.1093/database/bau058](https://doi.org/10.1093/database/bau058) (2014\).

[Article](https://doi.org/10.1093%2Fdatabase%2Fbau058) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=24923819) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4207230) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Curation%20accuracy%20of%20model%20organism%20databases&journal=Database&doi=10.1093%2Fdatabase%2Fbau058&publication_year=2014&author=Keseler%2CIM)
12. Yuan, J. *et al.* Constructing biomedical domain\-specific knowledge graph with minimum supervision. *Knowl. Inf. Syst.* **62**, 317–336\. [https://doi.org/10\.1007/s10115\-019\-01351\-4](https://doi.org/10.1007/s10115-019-01351-4) (2020\).

[Article](https://link.springer.com/doi/10.1007/s10115-019-01351-4) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Constructing%20biomedical%20domain-specific%20knowledge%20graph%20with%20minimum%20supervision&journal=Knowl.%20Inf.%20Syst.&doi=10.1007%2Fs10115-019-01351-4&volume=62&pages=317-336&publication_year=2020&author=Yuan%2CJ)
13. Collovini, S., Machado, G. \& Vieira, R. A sequence model approach to relation extraction in Portuguese. In *Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC’16\)*, 1908–1912 (European Language Resources Association (ELRA), 2016\).
14. Nédellec, C. *et al.* Overview of bionlp shared task 2013\. In *Proceedings of the BioNLP shared task 2013 workshop*, 1–7 (2013\).
15. Leitner, F. *et al.* An overview of biocreative II 5\. *IEEE/ACM Trans. Comput. Biol. Bioinform.* **7**, 385–399 (2010\).

[Article](https://doi.org/10.1109%2FTCBB.2010.61) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3cXhtFKqsL%2FI) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=20704011) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=An%20overview%20of%20biocreative%20II%205&journal=IEEE%2FACM%20Trans.%20Comput.%20Biol.%20Bioinform.&doi=10.1109%2FTCBB.2010.61&volume=7&pages=385-399&publication_year=2010&author=Leitner%2CF)
16. Sun, W., Rumshisky, A. \& Uzuner, O. Evaluating temporal relations in clinical text: 2012 i2b2 challenge. *J. Am. Med. Inform. Assoc.* **20**, 806–813 (2013\).

[Article](https://doi.org/10.1136%2Famiajnl-2013-001628) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=23564629) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3756273) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Evaluating%20temporal%20relations%20in%20clinical%20text%3A%202012%20i2b2%20challenge&journal=J.%20Am.%20Med.%20Inform.%20Assoc.&doi=10.1136%2Famiajnl-2013-001628&volume=20&pages=806-813&publication_year=2013&author=Sun%2CW&author=Rumshisky%2CA&author=Uzuner%2CO)
17. Segura\-Bedmar, I., Martínez Fernández, P. \& Sánchez Cisneros, D. The 1st ddiextraction\-2011 challenge task: Extraction of drug–drug interactions from biomedical texts. In *Proceedings of the 1st Challenge Task on Drug\-Drug Interaction Extraction* (Isabel Segura\-Bedmar, Paloma Martínez, Daniel Sánchez\-Cisneros, 2011\).
18. Yang, H., Swaminathan, R., Sharma, A., Ketkar, V. \& DSilva, J. Mining biomedical text towards building a quantitative food\-disease\-gene network. *Learn. Struct. Schemas Doc.* **20**, 205–225 (2011\).

[CAS](/articles/cas-redirect/1:CAS:528:DC%2BC3MXjtFOhsbo%3D) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Mining%20biomedical%20text%20towards%20building%20a%20quantitative%20food-disease-gene%20network&journal=Learn.%20Struct.%20Schemas%20Doc.&volume=20&pages=205-225&publication_year=2011&author=Yang%2CH&author=Swaminathan%2CR&author=Sharma%2CA&author=Ketkar%2CV&author=DSilva%2CJ)
19. Miao, Q., Zhang, S., Meng, Y. \& Yu, H. Polarity analysis for food and disease relationships. In *2012 IEEE/WIC/ACM International Conferences on Web Intelligence and Intelligent Agent Technology*, vol. 1, 188–195 (IEEE, 2012\).
20. Ben Abdessalem Karaa, W., Mannai, M., Dey, N., Ashour, A. S. \& Olariu, I. Gene\-disease\-food relation extraction from biomedical database. In *Soft Computing Applications: Proceedings of the 7th International Workshop Soft Computing Applications (SOFA 2016\), Vol 17*, 394–407 (Springer, 2018\).
21. Dooley, D. M. *et al.* Foodon: A harmonized food ontology to increase global food traceability, quality control and data integration. *NPJ Sci. Food* **2**, 1–10 (2018\).

[Article](https://doi.org/10.1038%2Fs41538-018-0032-6) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Foodon%3A%20A%20harmonized%20food%20ontology%20to%20increase%20global%20food%20traceability%2C%20quality%20control%20and%20data%20integration&journal=NPJ%20Sci.%20Food&doi=10.1038%2Fs41538-018-0032-6&volume=2&pages=1-10&publication_year=2018&author=Dooley%2CDM)
22. (EFSA), E. F. S. A. The food classification and description system foodex 2 (revision 2\). Tech. Rep., Wiley Online Library (2015\).
23. Callahan, T. J., Tripodi, I. J., Pielke\-Lombardo, H. \& Hunter, L. E. Knowledge\-based biomedical data science. *Annu. Rev. Biomed. Data Sci.* **3**, 23–41\. [https://doi.org/10\.1146/annurev\-biodatasci\-010820\-091627](https://doi.org/10.1146/annurev-biodatasci-010820-091627) (2020\).

[Article](https://doi.org/10.1146%2Fannurev-biodatasci-010820-091627) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33954284) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8095730) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Knowledge-based%20biomedical%20data%20science&journal=Annu.%20Rev.%20Biomed.%20Data%20Sci.&doi=10.1146%2Fannurev-biodatasci-010820-091627&volume=3&pages=23-41&publication_year=2020&author=Callahan%2CTJ&author=Tripodi%2CIJ&author=Pielke-Lombardo%2CH&author=Hunter%2CLE)
24. Chen, Q. \& Li, B. Retrieval method of electronic medical records based on rules and knowledge graph (2018\).
25. Liu, X. *et al.* Patienteg dataset: Bringing event graph model with temporal relations to electronic medical records. [arXiv:1812\.09905](http://arxiv.org/abs/1812.09905) (2018\).
26. Liu, Z., Peng, E., Yan, S., Li, G. \& Hao, T. T\-know: A knowledge graph\-based question answering and information retrieval system for traditional Chinese medicine. In *COLING* (2018\).
27. Bakal, G., Talari, P., Kakani, E. V. \& Kavuluru, R. Exploiting semantic patterns over biomedical knowledge graphs for predicting treatment and causative relations. *J. Biomed. Inform.* **82**, 189–199\. [https://doi.org/10\.1016/j.jbi.2018\.05\.003](https://doi.org/10.1016/j.jbi.2018.05.003) (2018\).

[Article](https://doi.org/10.1016%2Fj.jbi.2018.05.003) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=29763706) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6070294) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Exploiting%20semantic%20patterns%20over%20biomedical%20knowledge%20graphs%20for%20predicting%20treatment%20and%20causative%20relations&journal=J.%20Biomed.%20Inform.&doi=10.1016%2Fj.jbi.2018.05.003&volume=82&pages=189-199&publication_year=2018&author=Bakal%2CG&author=Talari%2CP&author=Kakani%2CEV&author=Kavuluru%2CR)
28. Schwertner, M. A., Rigo, S. J., Araújo, D. A., Silva, A. B. \& Eskofier, B. Fostering natural language question answering over knowledge bases in oncology EHR. In *2019 IEEE 32nd International Symposium on Computer\-Based Medical Systems (CBMS)*, 501–506\. [https://doi.org/10\.1109/CBMS.2019\.00102](https://doi.org/10.1109/CBMS.2019.00102) (2019\).
29. Liang, X. *et al.* Predicting biomedical relationships using the knowledge and graph embedding cascade model. *PLoS One* **14**, 1–23\. [https://doi.org/10\.1371/journal.pone.0218264](https://doi.org/10.1371/journal.pone.0218264) (2019\).

[Article](https://doi.org/10.1371%2Fjournal.pone.0218264) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC1MXhslOisb3O) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Predicting%20biomedical%20relationships%20using%20the%20knowledge%20and%20graph%20embedding%20cascade%20model&journal=PLoS%20One&doi=10.1371%2Fjournal.pone.0218264&volume=14&pages=1-23&publication_year=2019&author=Liang%2CX)
30. Aziguli, Zhang, Y., Xie, Y., Xu, Y. \& Chen, Y. Structural technology research on symptom data of Chinese medicine. In *2017 IEEE 19th International Conference on e\-Health Networking, Applications and Services (Healthcom)*, 1–4\. [https://doi.org/10\.1109/HealthCom.2017\.8210797](https://doi.org/10.1109/HealthCom.2017.8210797) (2017\).
31. Shang, J., Xiao, C., Ma, T., Li, H. \& Sun, J. Gamenet: Graph augmented memory networks for recommending medication combination. [arXiv:1809\.01852](http://arxiv.org/abs/1809.01852) (2019\).
32. Huang, E., Wang, S. \& Zhai, C. Visage: Integrating external knowledge into electronic medical record visualization. In *Pacific Symposium on Biocomputing. Pacific Symposium on Biocomputing* **23**, 578–589 (2018\).
33. Xu, R. \& Wang, Q. Large\-scale extraction of accurate drug\-disease treatment pairs from biomedical literature for drug repurposing. *BMC Bioinform.* **14**, 181\. [https://doi.org/10\.1186/1471\-2105\-14\-181](https://doi.org/10.1186/1471-2105-14-181) (2013\).

[Article](https://link.springer.com/doi/10.1186/1471-2105-14-181) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Large-scale%20extraction%20of%20accurate%20drug-disease%20treatment%20pairs%20from%20biomedical%20literature%20for%20drug%20repurposing&journal=BMC%20Bioinform.&doi=10.1186%2F1471-2105-14-181&volume=14&publication_year=2013&author=Xu%2CR&author=Wang%2CQ)
34. Chen, E. S., Hripcsak, G., Xu, H., Markatou, M. \& Friedman, C. Automated acquisition of disease drug knowledge from biomedical and clinical documents: An initial study. *J. Am. Med. Inform. Assoc.* **15**, 87–98\. [https://doi.org/10\.1197/jamia.M2401](https://doi.org/10.1197/jamia.M2401) (2008\).

[Article](https://doi.org/10.1197%2Fjamia.M2401) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=17947625) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2274872) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Automated%20acquisition%20of%20disease%20drug%20knowledge%20from%20biomedical%20and%20clinical%20documents%3A%20An%20initial%20study&journal=J.%20Am.%20Med.%20Inform.%20Assoc.&doi=10.1197%2Fjamia.M2401&volume=15&pages=87-98&publication_year=2008&author=Chen%2CES&author=Hripcsak%2CG&author=Xu%2CH&author=Markatou%2CM&author=Friedman%2CC)
35. Xia, E. *et al.* Mining disease\-symptom relation from massive biomedical literature and its application in severe disease diagnosis. *AMIA Annu. Symp. Proc.* **2018**, 1118–1126 (2018\).

[PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=30815154) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6371303) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Mining%20disease-symptom%20relation%20from%20massive%20biomedical%20literature%20and%20its%20application%20in%20severe%20disease%20diagnosis&journal=AMIA%20Annu.%20Symp.%20Proc.&volume=2018&pages=1118-1126&publication_year=2018&author=Xia%2CE)
36. Zhang, P. *et al.* Toward a coronavirus knowledge graph. *Genes*[https://doi.org/10\.3390/genes12070998](https://doi.org/10.3390/genes12070998) (2021\).

[Article](https://doi.org/10.3390%2Fgenes12070998) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=35052435) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8774900) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Toward%20a%20coronavirus%20knowledge%20graph&journal=Genes&doi=10.3390%2Fgenes12070998&publication_year=2021&author=Zhang%2CP)
37. Xu, J. *et al.* Building a PubMed knowledge graph. *Sci. Data*[https://doi.org/10\.1038/s41597\-020\-0543\-2](https://doi.org/10.1038/s41597-020-0543-2) (2020\).

[Article](https://doi.org/10.1038%2Fs41597-020-0543-2) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33177531) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7658216) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Building%20a%20PubMed%20knowledge%20graph&journal=Sci.%20Data&doi=10.1038%2Fs41597-020-0543-2&publication_year=2020&author=Xu%2CJ)
38. Rotmensch, M., Halpern, Y., Tlimat, A., Horng, S. \& Sontag, D. Learning a health knowledge graph from electronic medical records. *Sci. Rep.* **7**, 5994\. [https://doi.org/10\.1038/s41598\-017\-05778\-z](https://doi.org/10.1038/s41598-017-05778-z) (2017\).

[Article](https://doi.org/10.1038%2Fs41598-017-05778-z) 
 [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2017NatSR...7.5994R) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC1cXhtlemtb%2FF) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28729710) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5519723) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Learning%20a%20health%20knowledge%20graph%20from%20electronic%20medical%20records&journal=Sci.%20Rep.&doi=10.1038%2Fs41598-017-05778-z&volume=7&publication_year=2017&author=Rotmensch%2CM&author=Halpern%2CY&author=Tlimat%2CA&author=Horng%2CS&author=Sontag%2CD)
39. Li, L. *et al.* Real\-world data medical knowledge graph: Construction and applications. *Artif. Intell. Med.* **103**, 25 (2020\).

[Article](https://doi.org/10.1016%2Fj.artmed.2020.101817) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Real-world%20data%20medical%20knowledge%20graph%3A%20Construction%20and%20applications&journal=Artif.%20Intell.%20Med.&doi=10.1016%2Fj.artmed.2020.101817&volume=103&publication_year=2020&author=Li%2CL)
40. Haussmann, S. *et al.* Foodkg: A semantics\-driven knowledge graph for food recommendation. In *International Semantic Web Conference*, 146–162 (Springer, 2019\).
41. Gharibi, M., Zachariah, A. \& Rao, P. Foodkg: A tool to enrich knowledge graphs using machine learning techniques. *Front. Big Data* **3**, 12 (2020\).

[Article](https://doi.org/10.3389%2Ffdata.2020.00012) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33693387) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7931944) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Foodkg%3A%20A%20tool%20to%20enrich%20knowledge%20graphs%20using%20machine%20learning%20techniques&journal=Front.%20Big%20Data&doi=10.3389%2Ffdata.2020.00012&volume=3&publication_year=2020&author=Gharibi%2CM&author=Zachariah%2CA&author=Rao%2CP)
42. Pyvis: Interactive network visualizations. <https://pyvis.readthedocs.io/en/latest/>. Accessed 03 Mar 2023\.
43. Plotly: Low\-code data app development. <https://plotly.com/>. Accessed 03 Mar 2023\.
44. Cenikj, G., Popovski, G., Stojanov, R., Koroušić Seljak, B. \& Eftimov, T. Butter: Bidirectional lstm for food named\-entity recognition. In *Proceedings of Big Food and Nutrition Data Management and Analysis at IEEE BigData 2020*, 3550–3556\. [https://doi.org/10\.1109/BigData50022\.2020\.9378151](https://doi.org/10.1109/BigData50022.2020.9378151) (2020\).
45. Stojanov, R., Popovski, G., Cenikj, G., Koroušić Seljak, B. \& Eftimov, T. FoodNER: A fine\-tuned BERT for food named\-entity recognition. *J. Med. Internet Res.* (2021\) **(In press)**.
46. Popovski, G., Seljak, B. K. \& Eftimov, T. FoodBase corpus: A new resource of annotated food entities. *Database*[https://doi.org/10\.1093/database/baz121(2019\)](https://doi.org/10.1093/database/baz121(2019)) (2019\).

[Article](https://doi.org/10.1093%2Fdatabase%2Fbaz121%282019%29) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31682732) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6827550) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=FoodBase%20corpus%3A%20A%20new%20resource%20of%20annotated%20food%20entities&journal=Database&doi=10.1093%2Fdatabase%2Fbaz121%282019%29&publication_year=2019&author=Popovski%2CG&author=Seljak%2CBK&author=Eftimov%2CT)
47. Metathesaurus\-Rich Release Format (RRF), UMLS® Reference Manual. <https://www.ncbi.nlm.nih.gov/books/NBK9685/>. Accessed 15 Dec 2021\.
48. Giorgi, J. M. \& Bader, G. D. Towards reliable named entity recognition in the biomedical domain. *Bioinformatics* **36**, 280–286\. [https://doi.org/10\.1093/bioinformatics/btz504](https://doi.org/10.1093/bioinformatics/btz504) (2019\).

[Article](https://doi.org/10.1093%2Fbioinformatics%2Fbtz504) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3cXhslCisrrK) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6956779) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Towards%20reliable%20named%20entity%20recognition%20in%20the%20biomedical%20domain&journal=Bioinformatics&doi=10.1093%2Fbioinformatics%2Fbtz504&volume=36&pages=280-286&publication_year=2019&author=Giorgi%2CJM&author=Bader%2CGD)
49. Schriml, L. M. *et al.* Human disease ontology 2018 update: Classification, content and workflow expansion. *Nucleic Acids Res.* **47**, D955–D962\. [https://doi.org/10\.1093/nar/gky1032](https://doi.org/10.1093/nar/gky1032) (2018\).

[Article](https://doi.org/10.1093%2Fnar%2Fgky1032) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC1MXhs1Cgt7rF) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6323977) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Human%20disease%20ontology%202018%20update%3A%20Classification%2C%20content%20and%20workflow%20expansion&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgky1032&volume=47&pages=D955-D962&publication_year=2018&author=Schriml%2CLM)
50. Kim, S. *et al.* new data content and improved web interfaces. *Nucleic Acids Res.* **49**, D1388–D1395\. [https://doi.org/10\.1093/nar/gkaa971(2020\)](https://doi.org/10.1093/nar/gkaa971(2020)) (2021\).

[Article](https://doi.org/10.1093%2Fnar%2Fgkaa971%282020%29) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3MXntFCit7Y%3D) 
 [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33151290) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=new%20data%20content%20and%20improved%20web%20interfaces&journal=Nucleic%20Acids%20Res.&doi=10.1093%2Fnar%2Fgkaa971%282020%29&volume=49&pages=D1388-D1395&publication_year=2021&author=Kim%2CS)
51. Cenikj, G., Eftimov, T. \& Koroušić Seljak, B. SAFFRON: TranSfer leArning for food\-disease RelatiOn extractioN. In *Proceedings of the 20th Workshop on Biomedical Language Processing*, 30–40\. [https://doi.org/10\.18653/v1/2021\.bionlp\-1\.4](https://doi.org/10.18653/v1/2021.bionlp-1.4) (Association for Computational Linguistics, Online, 2021\).
52. Devlin, J., Chang, M.\-W., Lee, K. \& Toutanova, K. Bert: Pre\-training of deep bidirectional transformers for language understanding. [arXiv:1810\.04805](http://arxiv.org/abs/1810.04805) (arXiv preprint) (2018\).
53. Liu, Y. *et al.* Roberta: A robustly optimized BERT pretraining approach (2019\). [arXiv:1907\.11692](http://arxiv.org/abs/1907.11692) (CoRR).
54. Lee, J. *et al.* BioBERT: A pre\-trained biomedical language representation model for biomedical text mining. *Bioinformatics* **36**, 1234–1240\. [https://doi.org/10\.1093/bioinformatics/btz682](https://doi.org/10.1093/bioinformatics/btz682) (2019\).

[Article](https://doi.org/10.1093%2Fbioinformatics%2Fbtz682) 
 [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3cXhslCisLrL) 
 [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7703786) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=BioBERT%3A%20A%20pre-trained%20biomedical%20language%20representation%20model%20for%20biomedical%20text%20mining&journal=Bioinformatics&doi=10.1093%2Fbioinformatics%2Fbtz682&volume=36&pages=1234-1240&publication_year=2019&author=Lee%2CJ)
55. Dumitrache, A., Aroyo, L. \& Welty, C. Crowdsourcing ground truth for medical relation extraction. *ACM Trans. Interact. Intell. Syst.* **8**, 25 (2017\) [arXiv:1701\.02185](http://arxiv.org/abs/1701.02185).

[Google Scholar](http://scholar.google.com/scholar_lookup?&title=Crowdsourcing%20ground%20truth%20for%20medical%20relation%20extraction&journal=ACM%20Trans.%20Interact.%20Intell.%20Syst.&volume=8&publication_year=2017&author=Dumitrache%2CA&author=Aroyo%2CL&author=Welty%2CC)
56. Dumitrache, A., Aroyo, L. \& Welty, C. Crowdtruth measures for language ambiguity: The case of medical relation extraction. *CEUR Workshop Proc.* **1467**, 7–19 (2015\).

[Google Scholar](http://scholar.google.com/scholar_lookup?&title=Crowdtruth%20measures%20for%20language%20ambiguity%3A%20The%20case%20of%20medical%20relation%20extraction&journal=CEUR%20Workshop%20Proc.&volume=1467&pages=7-19&publication_year=2015&author=Dumitrache%2CA&author=Aroyo%2CL&author=Welty%2CC)
57. Dumitrache, A., Aroyo, L. \& Welty, C. Achieving expert\-level annotation quality with crowdtruth: The case of medical relation extraction. In *BDM2I@ISWC* (2015\).
58. Gurulingappa, H., Mateen\-Rajput, A. \& Toldo, L. Extraction of potential adverse drug events from medical case reports. *J. Biomed. Semant.* **3**, 15–15\. [https://doi.org/10\.1186/2041\-1480\-3\-15](https://doi.org/10.1186/2041-1480-3-15) (2012\).

[Article](https://link.springer.com/doi/10.1186/2041-1480-3-15) 
 [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Extraction%20of%20potential%20adverse%20drug%20events%20from%20medical%20case%20reports&journal=J.%20Biomed.%20Semant.&doi=10.1186%2F2041-1480-3-15&volume=3&pages=15-15&publication_year=2012&author=Gurulingappa%2CH&author=Mateen-Rajput%2CA&author=Toldo%2CL)
59. Cenikj, G., Koroušić Seljak, B. \& Eftimov, T. FoodChem: A food\-chemical relation extraction model. In *2021 IEEE Symposium Series on Computational Intelligence (SSCI) Proceedings* (2021\).

[Download references](https://citation-needed.springer.com/v2/references/10.1038/s41598-023-34981-4?format=refman&flavour=references)

## Acknowledgements

This research work is financially supported by the Slovenian Research Agency under programmes P2\-0098 and P1\-0143, and a young researcher Grant PR\-12393 to GC, the European Union’s Horizon 2020 research and innovation programme \[Grant agreement 101005259] (COMFOCUS) and Horizon Europe EU research and innovation framework programme \[Grant agreement 101060712] (FishEuTrust).

## Author information

### Authors and Affiliations

1. Jožef Stefan Institute, Ljubljana, 1000, Slovenia

Gjorgjina Cenikj, Lidija Strojnik, Nives Ogrinc, Barbara Koroušić Seljak \& Tome Eftimov
2. Jožef Stefan International Postgraduate School, Ljubljana, 1000, Slovenia

Gjorgjina Cenikj
3. Clinic Doctor 24\-hours, Ljubljana, 1000, Slovenia

Risto Angelski

Authors1. Gjorgjina Cenikj[View author publications](/search?author=Gjorgjina%20Cenikj)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Gjorgjina%20Cenikj) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Gjorgjina%20Cenikj%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
2. Lidija Strojnik[View author publications](/search?author=Lidija%20Strojnik)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Lidija%20Strojnik) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Lidija%20Strojnik%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
3. Risto Angelski[View author publications](/search?author=Risto%20Angelski)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Risto%20Angelski) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Risto%20Angelski%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
4. Nives Ogrinc[View author publications](/search?author=Nives%20Ogrinc)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Nives%20Ogrinc) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Nives%20Ogrinc%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
5. Barbara Koroušić Seljak[View author publications](/search?author=Barbara%20Korou%C5%A1i%C4%87%20Seljak)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Barbara%20Korou%C5%A1i%C4%87%20Seljak) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Barbara%20Korou%C5%A1i%C4%87%20Seljak%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
6. Tome Eftimov[View author publications](/search?author=Tome%20Eftimov)Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Tome%20Eftimov) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Tome%20Eftimov%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
### Contributions

All authors contributed to the writing of the original manuscript draft, G.C., T.E., and B.K.S. contributed to the conceptualization and methodology, G.C. executed the experiments and analysis, L.S., N.O., and R.A. provided the evaluation of the results, T.E. and B.K.S. provided overall coordination and final editing.

### Corresponding author

Correspondence to
 [Gjorgjina Cenikj](mailto:gjorgjina.cenikj@ijs.si).

## Ethics declarations


### Competing interests


The authors declare no competing interests.


## Additional information

### Publisher's note

Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

## Supplementary Information

### [Supplementary Information. (download PDF )](https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-34981-4/MediaObjects/41598_2023_34981_MOESM1_ESM.pdf)

## Rights and permissions


**Open Access** This article is licensed under a Creative Commons Attribution 4\.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit [http://creativecommons.org/licenses/by/4\.0/](http://creativecommons.org/licenses/by/4.0/).


[Reprints and permissions](https://s100.copyright.com/AppDispatchServlet?title=From%20language%20models%20to%20large-scale%20food%20and%20biomedical%20knowledge%20graphs&author=Gjorgjina%20Cenikj%20et%20al&contentID=10.1038%2Fs41598-023-34981-4&copyright=The%20Author%28s%29&publication=2045-2322&publicationDate=2023-05-15&publisherName=SpringerNature&orderBeanReset=true&oa=CC%20BY)

## About this article

[![Check for updates. Verify currency and authenticity via CrossMark](data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjgxIiB3aWR0aD0iNTciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj48cGF0aCBkPSJtMTcuMzUgMzUuNDUgMjEuMy0xNC4ydi0xNy4wM2gtMjEuMyIgZmlsbD0iIzk4OTg5OCIvPjxwYXRoIGQ9Im0zOC42NSAzNS40NS0yMS4zLTE0LjJ2LTE3LjAzaDIxLjMiIGZpbGw9IiM3NDc0NzQiLz48cGF0aCBkPSJtMjggLjVjLTEyLjk4IDAtMjMuNSAxMC41Mi0yMy41IDIzLjVzMTAuNTIgMjMuNSAyMy41IDIzLjUgMjMuNS0xMC41MiAyMy41LTIzLjVjMC02LjIzLTIuNDgtMTIuMjEtNi44OC0xNi42Mi00LjQxLTQuNC0xMC4zOS02Ljg4LTE2LjYyLTYuODh6bTAgNDEuMjVjLTkuOCAwLTE3Ljc1LTcuOTUtMTcuNzUtMTcuNzVzNy45NS0xNy43NSAxNy43NS0xNy43NSAxNy43NSA3Ljk1IDE3Ljc1IDE3Ljc1YzAgNC43MS0xLjg3IDkuMjItNS4yIDEyLjU1cy03Ljg0IDUuMi0xMi41NSA1LjJ6IiBmaWxsPSIjNTM1MzUzIi8+PHBhdGggZD0ibTQxIDM2Yy01LjgxIDYuMjMtMTUuMjMgNy40NS0yMi40MyAyLjktNy4yMS00LjU1LTEwLjE2LTEzLjU3LTcuMDMtMjEuNWwtNC45Mi0zLjExYy00Ljk1IDEwLjctMS4xOSAyMy40MiA4Ljc4IDI5LjcxIDkuOTcgNi4zIDIzLjA3IDQuMjIgMzAuNi00Ljg2eiIgZmlsbD0iIzljOWM5YyIvPjxwYXRoIGQ9Im0uMiA1OC40NWMwLS43NS4xMS0xLjQyLjMzLTIuMDFzLjUyLTEuMDkuOTEtMS41Yy4zOC0uNDEuODMtLjczIDEuMzQtLjk0LjUxLS4yMiAxLjA2LS4zMiAxLjY1LS4zMi41NiAwIDEuMDYuMTEgMS41MS4zNS40NC4yMy44MS41IDEuMS44MWwtLjkxIDEuMDFjLS4yNC0uMjQtLjQ5LS40Mi0uNzUtLjU2LS4yNy0uMTMtLjU4LS4yLS45My0uMi0uMzkgMC0uNzMuMDgtMS4wNS4yMy0uMzEuMTYtLjU4LjM3LS44MS42Ni0uMjMuMjgtLjQxLjYzLS41MyAxLjA0LS4xMy40MS0uMTkuODgtLjE5IDEuMzkgMCAxLjA0LjIzIDEuODYuNjggMi40Ni40NS41OSAxLjA2Ljg4IDEuODQuODguNDEgMCAuNzctLjA3IDEuMDctLjIzcy41OS0uMzkuODUtLjY4bC45MSAxYy0uMzguNDMtLjguNzYtMS4yOC45OS0uNDcuMjItMSAuMzQtMS41OC4zNC0uNTkgMC0xLjEzLS4xLTEuNjQtLjMxLS41LS4yLS45NC0uNTEtMS4zMS0uOTEtLjM4LS40LS42Ny0uOS0uODgtMS40OC0uMjItLjU5LS4zMy0xLjI2LS4zMy0yLjAyem04LjQtNS4zM2gxLjYxdjIuNTRsLS4wNSAxLjMzYy4yOS0uMjcuNjEtLjUxLjk2LS43MnMuNzYtLjMxIDEuMjQtLjMxYy43MyAwIDEuMjcuMjMgMS42MS43MS4zMy40Ny41IDEuMTQuNSAyLjAydjQuMzFoLTEuNjF2LTQuMWMwLS41Ny0uMDgtLjk3LS4yNS0xLjIxLS4xNy0uMjMtLjQ1LS4zNS0uODMtLjM1LS4zIDAtLjU2LjA4LS43OS4yMi0uMjMuMTUtLjQ5LjM2LS43OC42NHY0LjhoLTEuNjF6bTcuMzcgNi40NWMwLS41Ni4wOS0xLjA2LjI2LTEuNTEuMTgtLjQ1LjQyLS44My43MS0xLjE0LjI5LS4zLjYzLS41NCAxLjAxLS43MS4zOS0uMTcuNzgtLjI1IDEuMTgtLjI1LjQ3IDAgLjg4LjA4IDEuMjMuMjQuMzYuMTYuNjUuMzguODkuNjdzLjQyLjYzLjU0IDEuMDNjLjEyLjQxLjE4Ljg0LjE4IDEuMzIgMCAuMzItLjAyLjU3LS4wNy43NmgtNC4zNmMuMDcuNjIuMjkgMS4xLjY1IDEuNDQuMzYuMzMuODIuNSAxLjM4LjUuMjkgMCAuNTctLjA0LjgzLS4xM3MuNTEtLjIxLjc2LS4zN2wuNTUgMS4wMWMtLjMzLjIxLS42OS4zOS0xLjA5LjUzLS40MS4xNC0uODMuMjEtMS4yNi4yMS0uNDggMC0uOTItLjA4LTEuMzQtLjI1LS40MS0uMTYtLjc2LS40LTEuMDctLjctLjMxLS4zMS0uNTUtLjY5LS43Mi0xLjEzLS4xOC0uNDQtLjI2LS45NS0uMjYtMS41MnptNC42LS42MmMwLS41NS0uMTEtLjk4LS4zNC0xLjI4LS4yMy0uMzEtLjU4LS40Ny0xLjA2LS40Ny0uNDEgMC0uNzcuMTUtMS4wNy40NS0uMzEuMjktLjUuNzMtLjU4IDEuM3ptMi41LjYyYzAtLjU3LjA5LTEuMDguMjgtMS41My4xOC0uNDQuNDMtLjgyLjc1LTEuMTNzLjY5LS41NCAxLjEtLjcxYy40Mi0uMTYuODUtLjI0IDEuMzEtLjI0LjQ1IDAgLjg0LjA4IDEuMTcuMjNzLjYxLjM0Ljg1LjU3bC0uNzcgMS4wMmMtLjE5LS4xNi0uMzgtLjI4LS41Ni0uMzctLjE5LS4wOS0uMzktLjE0LS42MS0uMTQtLjU2IDAtMS4wMS4yMS0xLjM1LjYzLS4zNS40MS0uNTIuOTctLjUyIDEuNjcgMCAuNjkuMTcgMS4yNC41MSAxLjY2LjM0LjQxLjc4LjYyIDEuMzIuNjIuMjggMCAuNTQtLjA2Ljc4LS4xNy4yNC0uMTIuNDUtLjI2LjY0LS40MmwuNjcgMS4wM2MtLjMzLjI5LS42OS41MS0xLjA4LjY1LS4zOS4xNS0uNzguMjMtMS4xOC4yMy0uNDYgMC0uOS0uMDgtMS4zMS0uMjQtLjQtLjE2LS43NS0uMzktMS4wNS0uN3MtLjUzLS42OS0uNy0xLjEzYy0uMTctLjQ1LS4yNS0uOTYtLjI1LTEuNTN6bTYuOTEtNi40NWgxLjU4djYuMTdoLjA1bDIuNTQtMy4xNmgxLjc3bC0yLjM1IDIuOCAyLjU5IDQuMDdoLTEuNzVsLTEuNzctMi45OC0xLjA4IDEuMjN2MS43NWgtMS41OHptMTMuNjkgMS4yN2MtLjI1LS4xMS0uNS0uMTctLjc1LS4xNy0uNTggMC0uODcuMzktLjg3IDEuMTZ2Ljc1aDEuMzR2MS4yN2gtMS4zNHY1LjZoLTEuNjF2LTUuNmgtLjkydi0xLjJsLjkyLS4wN3YtLjcyYzAtLjM1LjA0LS42OC4xMy0uOTguMDgtLjMxLjIxLS41Ny40LS43OXMuNDItLjM5LjcxLS41MWMuMjgtLjEyLjYzLS4xOCAxLjA0LS4xOC4yNCAwIC40OC4wMi42OS4wNy4yMi4wNS40MS4xLjU3LjE3em0uNDggNS4xOGMwLS41Ny4wOS0xLjA4LjI3LTEuNTMuMTctLjQ0LjQxLS44Mi43Mi0xLjEzLjMtLjMxLjY1LS41NCAxLjA0LS43MS4zOS0uMTYuOC0uMjQgMS4yMy0uMjRzLjg0LjA4IDEuMjQuMjRjLjQuMTcuNzQuNCAxLjA0Ljcxcy41NC42OS43MiAxLjEzYy4xOS40NS4yOC45Ni4yOCAxLjUzcy0uMDkgMS4wOC0uMjggMS41M2MtLjE4LjQ0LS40Mi44Mi0uNzIgMS4xM3MtLjY0LjU0LTEuMDQuNy0uODEuMjQtMS4yNC4yNC0uODQtLjA4LTEuMjMtLjI0LS43NC0uMzktMS4wNC0uN2MtLjMxLS4zMS0uNTUtLjY5LS43Mi0xLjEzLS4xOC0uNDUtLjI3LS45Ni0uMjctMS41M3ptMS42NSAwYzAgLjY5LjE0IDEuMjQuNDMgMS42Ni4yOC40MS42OC42MiAxLjE4LjYyLjUxIDAgLjktLjIxIDEuMTktLjYyLjI5LS40Mi40NC0uOTcuNDQtMS42NiAwLS43LS4xNS0xLjI2LS40NC0xLjY3LS4yOS0uNDItLjY4LS42My0xLjE5LS42My0uNSAwLS45LjIxLTEuMTguNjMtLjI5LjQxLS40My45Ny0uNDMgMS42N3ptNi40OC0zLjQ0aDEuMzNsLjEyIDEuMjFoLjA1Yy4yNC0uNDQuNTQtLjc5Ljg4LTEuMDIuMzUtLjI0LjctLjM2IDEuMDctLjM2LjMyIDAgLjU5LjA1Ljc4LjE0bC0uMjggMS40LS4zMy0uMDljLS4xMS0uMDEtLjIzLS4wMi0uMzgtLjAyLS4yNyAwLS41Ni4xLS44Ni4zMXMtLjU1LjU4LS43NyAxLjF2NC4yaC0xLjYxem0tNDcuODcgMTVoMS42MXY0LjFjMCAuNTcuMDguOTcuMjUgMS4yLjE3LjI0LjQ0LjM1LjgxLjM1LjMgMCAuNTctLjA3LjgtLjIyLjIyLS4xNS40Ny0uMzkuNzMtLjczdi00LjdoMS42MXY2Ljg3aC0xLjMybC0uMTItMS4wMWgtLjA0Yy0uMy4zNi0uNjMuNjQtLjk4Ljg2LS4zNS4yMS0uNzYuMzItMS4yNC4zMi0uNzMgMC0xLjI3LS4yNC0xLjYxLS43MS0uMzMtLjQ3LS41LTEuMTQtLjUtMi4wMnptOS40NiA3LjQzdjIuMTZoLTEuNjF2LTkuNTloMS4zM2wuMTIuNzJoLjA1Yy4yOS0uMjQuNjEtLjQ1Ljk3LS42My4zNS0uMTcuNzItLjI2IDEuMS0uMjYuNDMgMCAuODEuMDggMS4xNS4yNC4zMy4xNy42MS40Ljg0LjcxLjI0LjMxLjQxLjY4LjUzIDEuMTEuMTMuNDIuMTkuOTEuMTkgMS40NCAwIC41OS0uMDkgMS4xMS0uMjUgMS41Ny0uMTYuNDctLjM4Ljg1LS42NSAxLjE2LS4yNy4zMi0uNTguNTYtLjk0LjczLS4zNS4xNi0uNzIuMjUtMS4xLjI1LS4zIDAtLjYtLjA3LS45LS4ycy0uNTktLjMxLS44Ny0uNTZ6bTAtMi4zYy4yNi4yMi41LjM3LjczLjQ1LjI0LjA5LjQ2LjEzLjY2LjEzLjQ2IDAgLjg0LS4yIDEuMTUtLjYuMzEtLjM5LjQ2LS45OC40Ni0xLjc3IDAtLjY5LS4xMi0xLjIyLS4zNS0xLjYxLS4yMy0uMzgtLjYxLS41Ny0xLjEzLS41Ny0uNDkgMC0uOTkuMjYtMS41Mi43N3ptNS44Ny0xLjY5YzAtLjU2LjA4LTEuMDYuMjUtMS41MS4xNi0uNDUuMzctLjgzLjY1LTEuMTQuMjctLjMuNTgtLjU0LjkzLS43MXMuNzEtLjI1IDEuMDgtLjI1Yy4zOSAwIC43My4wNyAxIC4yLjI3LjE0LjU0LjMyLjgxLjU1bC0uMDYtMS4xdi0yLjQ5aDEuNjF2OS44OGgtMS4zM2wtLjExLS43NGgtLjA2Yy0uMjUuMjUtLjU0LjQ2LS44OC42NC0uMzMuMTgtLjY5LjI3LTEuMDYuMjctLjg3IDAtMS41Ni0uMzItMi4wNy0uOTVzLS43Ni0xLjUxLS43Ni0yLjY1em0xLjY3LS4wMWMwIC43NC4xMyAxLjMxLjQgMS43LjI2LjM4LjY1LjU4IDEuMTUuNTguNTEgMCAuOTktLjI2IDEuNDQtLjc3di0zLjIxYy0uMjQtLjIxLS40OC0uMzYtLjctLjQ1LS4yMy0uMDgtLjQ2LS4xMi0uNy0uMTItLjQ1IDAtLjgyLjE5LTEuMTMuNTktLjMxLjM5LS40Ni45NS0uNDYgMS42OHptNi4zNSAxLjU5YzAtLjczLjMyLTEuMy45Ny0xLjcxLjY0LS40IDEuNjctLjY4IDMuMDgtLjg0IDAtLjE3LS4wMi0uMzQtLjA3LS41MS0uMDUtLjE2LS4xMi0uMy0uMjItLjQzcy0uMjItLjIyLS4zOC0uM2MtLjE1LS4wNi0uMzQtLjEtLjU4LS4xLS4zNCAwLS42OC4wNy0xIC4ycy0uNjMuMjktLjkzLjQ3bC0uNTktMS4wOGMuMzktLjI0LjgxLS40NSAxLjI4LS42My40Ny0uMTcuOTktLjI2IDEuNTQtLjI2Ljg2IDAgMS41MS4yNSAxLjkzLjc2cy42MyAxLjI1LjYzIDIuMjF2NC4wN2gtMS4zMmwtLjEyLS43NmgtLjA1Yy0uMy4yNy0uNjMuNDgtLjk4LjY2cy0uNzMuMjctMS4xNC4yN2MtLjYxIDAtMS4xLS4xOS0xLjQ4LS41Ni0uMzgtLjM2LS41Ny0uODUtLjU3LTEuNDZ6bTEuNTctLjEyYzAgLjMuMDkuNTMuMjcuNjcuMTkuMTQuNDIuMjEuNzEuMjEuMjggMCAuNTQtLjA3Ljc3LS4ycy40OC0uMzEuNzMtLjU2di0xLjU0Yy0uNDcuMDYtLjg2LjEzLTEuMTguMjMtLjMxLjA5LS41Ny4xOS0uNzYuMzFzLS4zMy4yNS0uNDEuNGMtLjA5LjE1LS4xMy4zMS0uMTMuNDh6bTYuMjktMy42M2gtLjk4di0xLjJsMS4wNi0uMDcuMi0xLjg4aDEuMzR2MS44OGgxLjc1djEuMjdoLTEuNzV2My4yOGMwIC44LjMyIDEuMi45NyAxLjIuMTIgMCAuMjQtLjAxLjM3LS4wNC4xMi0uMDMuMjQtLjA3LjM0LS4xMWwuMjggMS4xOWMtLjE5LjA2LS40LjEyLS42NC4xNy0uMjMuMDUtLjQ5LjA4LS43Ni4wOC0uNCAwLS43NC0uMDYtMS4wMi0uMTgtLjI3LS4xMy0uNDktLjMtLjY3LS41Mi0uMTctLjIxLS4zLS40OC0uMzctLjc4LS4wOC0uMy0uMTItLjY0LS4xMi0xLjAxem00LjM2IDIuMTdjMC0uNTYuMDktMS4wNi4yNy0xLjUxcy40MS0uODMuNzEtMS4xNGMuMjktLjMuNjMtLjU0IDEuMDEtLjcxLjM5LS4xNy43OC0uMjUgMS4xOC0uMjUuNDcgMCAuODguMDggMS4yMy4yNC4zNi4xNi42NS4zOC44OS42N3MuNDIuNjMuNTQgMS4wM2MuMTIuNDEuMTguODQuMTggMS4zMiAwIC4zMi0uMDIuNTctLjA3Ljc2aC00LjM3Yy4wOC42Mi4yOSAxLjEuNjUgMS40NC4zNi4zMy44Mi41IDEuMzguNS4zIDAgLjU4LS4wNC44NC0uMTMuMjUtLjA5LjUxLS4yMS43Ni0uMzdsLjU0IDEuMDFjLS4zMi4yMS0uNjkuMzktMS4wOS41M3MtLjgyLjIxLTEuMjYuMjFjLS40NyAwLS45Mi0uMDgtMS4zMy0uMjUtLjQxLS4xNi0uNzctLjQtMS4wOC0uNy0uMy0uMzEtLjU0LS42OS0uNzItMS4xMy0uMTctLjQ0LS4yNi0uOTUtLjI2LTEuNTJ6bTQuNjEtLjYyYzAtLjU1LS4xMS0uOTgtLjM0LTEuMjgtLjIzLS4zMS0uNTgtLjQ3LTEuMDYtLjQ3LS40MSAwLS43Ny4xNS0xLjA4LjQ1LS4zMS4yOS0uNS43My0uNTcgMS4zem0zLjAxIDIuMjNjLjMxLjI0LjYxLjQzLjkyLjU3LjMuMTMuNjMuMi45OC4yLjM4IDAgLjY1LS4wOC44My0uMjNzLjI3LS4zNS4yNy0uNmMwLS4xNC0uMDUtLjI2LS4xMy0uMzctLjA4LS4xLS4yLS4yLS4zNC0uMjgtLjE0LS4wOS0uMjktLjE2LS40Ny0uMjNsLS41My0uMjJjLS4yMy0uMDktLjQ2LS4xOC0uNjktLjMtLjIzLS4xMS0uNDQtLjI0LS42Mi0uNHMtLjMzLS4zNS0uNDUtLjU1Yy0uMTItLjIxLS4xOC0uNDYtLjE4LS43NSAwLS42MS4yMy0xLjEuNjgtMS40OS40NC0uMzggMS4wNi0uNTcgMS44My0uNTcuNDggMCAuOTEuMDggMS4yOS4yNXMuNzEuMzYuOTkuNTdsLS43NC45OGMtLjI0LS4xNy0uNDktLjMyLS43My0uNDItLjI1LS4xMS0uNTEtLjE2LS43OC0uMTYtLjM1IDAtLjYuMDctLjc2LjIxLS4xNy4xNS0uMjUuMzMtLjI1LjU0IDAgLjE0LjA0LjI2LjEyLjM2cy4xOC4xOC4zMS4yNmMuMTQuMDcuMjkuMTQuNDYuMjFsLjU0LjE5Yy4yMy4wOS40Ny4xOC43LjI5cy40NC4yNC42NC40Yy4xOS4xNi4zNC4zNS40Ni41OC4xMS4yMy4xNy41LjE3LjgyIDAgLjMtLjA2LjU4LS4xNy44My0uMTIuMjYtLjI5LjQ4LS41MS42OC0uMjMuMTktLjUxLjM0LS44NC40NS0uMzQuMTEtLjcyLjE3LTEuMTUuMTctLjQ4IDAtLjk1LS4wOS0xLjQxLS4yNy0uNDYtLjE5LS44Ni0uNDEtMS4yLS42OHoiIGZpbGw9IiM1MzUzNTMiLz48L2c+PC9zdmc+)](https://crossmark.crossref.org/dialog/?doi=10.1038/s41598-023-34981-4)### Cite this article

Cenikj, G., Strojnik, L., Angelski, R. *et al.* From language models to large\-scale food and biomedical knowledge graphs.
 *Sci Rep* **13**, 7815 (2023\). https://doi.org/10\.1038/s41598\-023\-34981\-4

[Download citation](https://citation-needed.springer.com/v2/references/10.1038/s41598-023-34981-4?format=refman&flavour=citation)

* Received: 11 January 2023
* Accepted: 10 May 2023
* Published: 15 May 2023
* Version of record: 15 May 2023
* DOI: https://doi.org/10\.1038/s41598\-023\-34981\-4

### Share this article

Anyone you share the following link with will be able to read this content:

Get shareable linkSorry, a shareable link is not currently available for this article.

Copy shareable link to clipboard
 Provided by the Springer Nature SharedIt content\-sharing initiative
 


### Subjects


* [Cardiovascular diseases](/subjects/cardiovascular-diseases)
* [Nutrition disorders](/subjects/nutrition-disorders)
* [Software](/subjects/software)





