# What Should I Learn First: Introducing LectureBank for NLP Education and Prerequisite Chain Learning

Li, Fabbri, Tung, Radev (Yale University). NAACL 2018. arXiv 1811.12181. LectureBank is a dataset of 1,352 university lecture files from 60 NLP/ML/AI courses with manually-annotated prerequisite relations among 208 core concepts (921 prerequisite edges), enabling prerequisite-chain learning via embedding and graph-based classifiers.

## Method

LectureBank comprises 1,352 English lecture files (51,939 slides) collected from 60 university courses spanning NLP, ML, AI, deep learning, and information retrieval. Each lecture is automatically classified into a 305-topic taxonomy derived from TutorialBank (Fabbri et al. 2018). Prerequisite relations are manually annotated on a subset of 208 concepts that represent survey-level topics — granular enough to be tractable but coarse enough to capture meaningful dependencies. Two expert annotators (PhD students in NLP) independently label all concept pairs (A, B) as "yes" (A is a prerequisite of B) or "no," achieving Cohen's kappa $\kappa=0.7$ (substantial agreement). The intersection of annotations yields 921 directed edges among 208 vertices, forming a directed acyclic graph with 12 cycles (closely related concept pairs like Domain Adaptation $\leftrightarrow$ Transfer Learning).

The prerequisite chain learning task is framed as binary link prediction. Concept embeddings are extracted via Doc2Vec (300-dim, PVDM) trained on either LectureBank alone, TutorialBank alone, or both combined. For each concept pair, embeddings are concatenated and fed to classifiers: Naïve Bayes, SVM (linear), Logistic Regression, Random Forest, Graph Autoencoder (GAE), and Variational Graph Autoencoder (VGAE). The dataset exhibits severe class imbalance (921 positive vs. 41,829 negative pairs before oversampling); oversampling is critical for baseline classifier performance.

## Claims

- **Dataset size**: 1,352 lecture files, 51,939 slides, 1,221 vocabulary terms extracted from lecture headers; 208 prerequisite-annotated concepts, 921 manually-labeled prerequisite relations.
- **Annotation agreement**: Cohen's kappa $\kappa=0.7$ (two expert annotators); binary annotation improves upon TutorialBank's ternary scheme ($\kappa=0.3$) by explicitly directing annotators to university curricula for ambiguous pairs.
- **Best classifier performance**: SVM with Doc2Vec embeddings trained on TutorialBank achieves the highest F1 score; all three training-set variants (TutorialBank, LectureBank, combined) show comparable F1 within non-significant variance.
- **Precision/recall tradeoff**: Baseline classifiers (NB, SVM, LR, RF) favor precision over recall; graph autoencoders (GAE/VGAE) favor recall but underperform SVM on F1. For downstream applications (e.g., search engines), higher recall is preferred to avoid missing prerequisites.
- **Concept graph structure**: Longest dependency chain contains 14 concepts (Matrix Multiplication $\rightarrow$ ... $\rightarrow$ Scientific Article Summarization); 7 isolated concepts with no prerequisites; highest in-degree: Neural Machine Translation (19 prerequisites); highest out-degree: Data Structures and Algorithms (106 dependent concepts).
- **Oversampling impact**: Oversampling training data is essential; initial imbalanced experiments yield poor results; minimal improvement for GAE/VGAE despite multi-graph modifications.

## Relevance to the project

LectureBank directly operationalises the RCL framework's core decomposition operations. First, the manually-annotated prerequisite relations define a concrete instance of the $\text{Decompose}(c, \text{trace})$ component: given a target concept $c$ (e.g., POS Tagging), the dataset encodes its immediate prerequisites as ground-truth edges in the learned graph. This provides direct payload for RCL's D1 (Decompose) and E3 (Identity) components — operationalizing the binary predicate "A is a prerequisite of B" which is central to identifying concept dependencies. The manual annotation protocol (two expert annotators, $\kappa=0.7$, reference to university curricula) establishes a rigorous definition of conceptual prerequisite that RCL decomposition methods can target.

Second, the annotation cost (208 concepts, 921 edges, two PhD-level annotators) establishes a baseline for the human labor that an LLM teacher would need to replicate. RCL's goal is to learn such prerequisite relations *automatically* from student failure traces (the corpus learns only from text); understanding the manual-annotation burden highlights why learning from error traces is valuable — expert annotation does not scale to arbitrary student populations or concept domains.

Third, LectureBank reveals important limitations of the corpus-driven approach that RCL must address: (a) domain-specificity — the dataset is NLP-only, limiting generalizability to other knowledge domains; (b) fixed concept vocabulary — the 208 concepts are pre-selected and static, whereas RCL's failure-trace-driven decomposition can discover prerequisites dynamically as new student errors emerge; (c) no failure-driven discovery — LectureBank learns prerequisite structure from text occurrence and semantic similarity (via Doc2Vec), not from observed gaps in student understanding, which is where RCL's trace-based decomposition derives its signal. RCL's core innovation is learning decompositions *from patterns in where students fail*, not from curriculum text alone.

## Source

- arXiv: 1811.12181
- Raw markdown: `../../../raw/research/rcl-gap-fillers/02-lecturebank.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[concept-prereq-relations]] — companion methodology paper; LectureBank is the dataset, concept-prereq-relations is the inference algorithm family
- [[auto-kc-generation]] — LLM-based successor to LectureBank's manual annotation; suggests LLM teacher can replicate the prereq-pair labelling
- [[../synthesis/recursive-concept-learning]] — direct payload for **D1** ($\text{Decompose}(c, \text{trace})$) and **E3** (concept identity); LectureBank's prereq-pair structure is the canonical operationalisation
- [[../concept-learning/_overview]] — concept-as-architectural-commitment vs concept-as-prereq-node — adjacent ontologies
