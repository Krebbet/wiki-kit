# Inferring Concept Prerequisite Relations from Online Educational Resources

Lawrence et al. 2019 (arXiv 1811.12640, AAAI). Introduces PREREQ, a supervised method for learning concept prerequisite relations from course prerequisite data and video playlists in MOOCs. Combines pairwise-link LDA for concept embeddings with a Siamese network classifier to predict binary prerequisite edges.

## Method

PREREQ operates in two stages. First, it learns latent concept representations using **Pairwise-Link LDA** (Nallapati et al. 2008), a generative model that jointly factors document text and prerequisite links between documents. The model outputs two key parameters: $\beta$ (word-topic distributions) and $\eta$ (asymmetric topic-pair prerequisite relations). Concept vectors are derived from the normalized, exponentiated columns of $\beta$, yielding K-dimensional embeddings (K=100 in experiments).

Second, these embeddings feed a **Siamese neural network** with tied weights across two branches. Each branch is a 2-layer fully connected network (with ReLU). The network takes ordered concept pairs $(c_s, c_t)$ and learns a binary classifier via cross-entropy loss. The model is trained on labeled concept prerequisite pairs (60/40 train-test split) augmented with negative samples: reverse pairs and random unrelated pairs oversampled to 1.5× positive examples.

**Datasets:** University Course Dataset (654 courses, 861 course edges, 365 concepts, 1008 manually annotated concept pairs) and NPTEL MOOC Dataset (382 videos from 38 playlists, 1445 video edges, 345 concepts). Concept identification via n-gram matching (1-, 2-, 3-grams) with lemmatization.

## Claims

- **F-score on University Course Dataset:** PREREQ achieves F=59.68 vs. CPR-Recover's F=53.43 and Pairwise-LDA's F=16.66 (Table 2).
- **F-score on MOOC Dataset:** PREREQ F=60.73 vs. CPR-Recover F=56.48 and MOOC-RF F=58.07.
- **Precision@50 and Precision@100:** Significantly outperforms CPR-Recover across sampled course prerequisite edge counts (100–800 edges, Fig. 5).
- **Low-data learning:** Performance degrades only marginally when trained on 40% of labeled data (Fig. 7a), suggesting efficient learning from sparse supervision.
- **Concept representation superiority:** Pairwise-link LDA embeddings outperform standard LDA and Word2Vec on the same task (Fig. 7b), validating the asymmetric directionality signal in $\eta$.
- **Video playlist robustness:** PREREQ infers concept prerequisites from unlabeled MOOC video playlists using temporal ordering as a proxy for document-level prerequisites.

## Relevance to the project

This paper directly addresses the **inferred-prereq paradigm**: learning prerequisite relations from raw educational text without a hand-curated knowledge graph. RCL's $\text{Decompose}(c, \text{trace})$ (D1) must generate concept prerequisites from a concept name and context when the teacher LLM has no explicit KB. PREREQ demonstrates that prerequisite *inference* from document-level constraints (course structure, video order) can substitute for manual curation, a scalable alternative to hard-coded DAGs.

However, PREREQ learns from *document* structure and *text*, whereas RCL's failure-trace paradigm requires integrating **student errors** as training signal. PREREQ ignores the gap: it does not learn from which concepts students struggle on, only from textual association and document order. D1 could profit from hybrid supervision: e.g., if a student fails a task involving concept $c_t$ when $c_s$ is known, the failure trace signals that $c_s \rightarrow c_t$ should hold, a stronger signal than text co-occurrence alone.

**Practical takeaway for D1 prompt engineering:** PREREQ's success with Siamese networks on small supervised concept pairs (1008 pairs) suggests that even 10–20 few-shot examples of valid concept prerequisites could fine-tune an LLM's prerequisite generation via in-context learning or LoRA, more efficiently than full retraining. The asymmetric directionality via $\eta$ also hints that prompting the teacher LLM to decompose concept dependencies step-by-step (e.g., "list concepts learned-before concept X") may elicit more accurate prerequisites than flat enumeration. Temporal or hierarchical structure in the prompt context could substitute for $\eta$'s learned directional signal.

## Source

- arXiv: 1811.12640
- Raw markdown: `../../../raw/research/rcl-gap-fillers/03-concept-prereq-relations.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[lecturebank]] — companion dataset; this paper is the methodology, LectureBank is the curated benchmark
- [[auto-kc-generation]] — LLM-based successor; replaces feature-engineered prereq inference with LLM concept extraction
- [[../synthesis/recursive-concept-learning]] — direct payload for **D1** (Decompose); the asymmetric pairwise-link LDA + Siamese network is the closest non-LLM prior art for the prereq-inference step
- [[../teacher-student-rl/saha-teacher-explanations]] — Theory-of-Mind framing for *when/how* a teacher intervenes; this paper provides the *what* (which concept to surface)
