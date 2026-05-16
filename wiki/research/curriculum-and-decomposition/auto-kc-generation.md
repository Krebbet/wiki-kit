# Automated Knowledge Component Generation for Interpretable Knowledge Tracing in Coding Problems

Duan et al. (arXiv:2502.18632, preprint under review) present an LLM-based pipeline for automated knowledge component (KC) generation and knowledge tracing in programming education. The paper demonstrates that GPT-4o-generated KCs outperform human-written KC labels on two real-world coding datasets, enabling more accurate prediction of future student performance in knowledge tracing tasks.

## Method

The KC generation pipeline operates in three stages. First, GPT-4o performs few-shot prompting on each problem using diverse representative student solutions (clustered by CodeBERT embeddings) to generate fine-grained, function-level KC descriptions. Second, the authors apply Hierarchical Agglomerative Clustering on Sentence-BERT embeddings to aggregate semantically similar KCs across all problems and control abstraction level. Third, GPT-4o labels each cluster with a concise, synthesized description, yielding a Q-matrix (problem-KC mappings) at the desired granularity.

For the downstream knowledge tracing (KT) task, the authors develop KCGen-KT, which uses Llama 3 as its backbone to predict both binary correctness and student code submission. The model tracks a k-dimensional student mastery vector (one dimension per KC) via an LSTM, converting mastery levels to soft tokens that blend embeddings of "true" and "false" based on mastery strength. This soft-token mechanism enables gradient flow while injecting interpretable KC knowledge into the LLM input. A compensatory model averaging KC masteries provides the final correctness prediction. Multi-task learning jointly optimizes code generation loss, correctness prediction loss, and a KC-interpretability loss (enforcing monotonicity between KC mastery and correctness).

Evaluation on two datasets—CodeWorkout (Java, 50 problems, 246 students) and FalconCode (Python, 157 problems, 3,267 students)—compares KCGen-KT against TIKTOC and Code-DKT baselines. The comparison protocol isolates the contribution of generated KCs by also testing KCGen-KT with human-written KCs from the datasets.

## Claims

- **LLM-generated KCs consistently outperform human-written KCs on KT performance across both tasks and datasets**, with statistical significance (p < 0.05). CodeWorkout: AUC 0.816 vs. 0.797 (generated vs. human); FalconCode: AUC 0.771 vs. 0.752 (Duan et al., Table 2).
- **KCGen-KT outperforms non-KC-leveraging baselines** (TIKTOC*, Code-DKT) on correctness prediction and code generation, demonstrating that semantic KC information improves LLM-based KT (Table 2).
- **Medium-granularity KCs (50 clusters on CodeWorkout, 60 on FalconCode) achieve optimal performance**, while high abstraction (fewer clusters) degrades performance across all metrics, showing that fine-granular KCs pinpoint necessary skills (Table 3).
- **LLM-generated KCs achieve comparable or better cognitive model fit than human KCs** under the power law of practice, with weighted R² of 0.21 vs. 0.18 (Duan et al., Section 5.2.2).
- **Human evaluation confirms 98.6% interpretability of LLM-generated KCs** (vs. 94.6% for baseline KCs), 93.2% precision, and 96% equal-or-greater coverage in problem-KC mappings compared to human-authored sets (Section 6).
- **Ablation studies identify diverse student solutions and in-context examples as critical**; removing correct solutions or in-context examples significantly reduces performance (Table 4). Using 5–10 student submissions per problem saturates KC quality (Table 5).

## Relevance to the project

This paper provides direct empirical evidence that an LLM can perform diagnostic decomposition—splitting a task into fine-grained, interpretable knowledge components—competitively with or better than human domain experts. This directly validates RCL's D1 viability (Decompose(c, trace) at concept-component granularity). The LLM-generated KCs are not hand-authored; they are mined from problem statements and diverse student solutions, demonstrating an automated pipeline that scales KC generation without manual effort. The consistency of the result across two programming languages and datasets strengthens the claim that LLMs can generalize this decomposition skill to new domains.

The KT-loss-based evaluation mirrors RCL's own downstream metric: the quality of KC decomposition is judged by its utility in predicting student performance. High KC mastery should correlate with correct responses, and the paper shows LLM-generated KCs satisfy this criterion better than human KCs, enabling more accurate mastery tracking. The compensatory model averaging KC masteries and enforcing monotonicity with correctness (Section 3.2.6) directly parallels the need for "concept mastery → task success" alignment in RCL's D2 (differentiated feedback).

However, important limitations qualify the generalization. Programming problems are procedural and structured, with clear correct/incorrect answers and deterministic test cases—closer to Phase-0 modular arithmetic than to open-ended qualitative concepts (e.g., literary analysis, causal reasoning). KCs are extracted from problem text and code rather than from student failure traces; the paper does not show decomposition of an actual student error, trace, or misconception. The power law of practice fit (R² = 0.21) is modest, suggesting KCs, though better than human labels, still do not fully explain learning. Finally, the paper generates KCs independently per problem and acknowledges missing KCs shared across problems, limiting the formation of a unified skill ontology.

## Source

- arXiv: 2502.18632
- Raw markdown: `../../../raw/research/rcl-gap-fillers/09-auto-kc-generation.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[dkt]] — KT backbone this paper extends; the KCGen-KT model uses Llama 3 + soft-token mastery on top of DKT-style response-history modelling
- [[lecturebank]], [[concept-prereq-relations]] — concept-side sibling work; auto-kc-generation is the LLM-based descendant
- [[../synthesis/recursive-concept-learning]] — **strongest single corpus signal that RCL's D1 (Decompose) is feasible.** LLM-generated KCs beat human-written labels on KT (AUC 0.816 vs 0.797) — direct evidence the teacher LLM can do diagnostic decomposition at concept-component granularity
- [[../teacher-student-rl/sakana-rlt]] — RLT's teacher-given-(Q,A) regime; auto-kc-generation extends it to teacher-given-(problem)-extracts-(KCs)
- [[../concept-evaluation/_overview]] — concept-evaluation theme; KCs serve as concept-mastery probe targets in the KT-loss evaluation protocol
