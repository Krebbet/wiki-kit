# Curriculum Learning: A Survey

Comprehensive survey of curriculum learning methods across supervised, self-paced, transfer, and RL settings. Authors: Petru Soviany, Radu Tudor Ionescu, Paolo Rota, Nicu Sebe. International Journal of Computer Vision, 2022. arXiv:2101.10382.

## Method

The survey formalizes curriculum learning as a continuation method on loss function smoothing—applying curriculum to the **data E** (easy-to-hard sample ordering), **model M** (progressive capacity growth), **task T** (task-level difficulty), or **performance measure P** (unsmoothing objectives) all achieve smoother loss landscapes in early training. The authors identify seven major paradigms: (1) **Vanilla CL** uses predefined difficulty criteria (shape complexity, sentence length, object size); (2) **Self-Paced Learning (SPL)** ranks samples dynamically by model loss; (3) **Balanced CL** adds diversity constraints to prevent class/region imbalance; (4) **Self-Paced Curriculum Learning (SPCL)** combines predefined and learned rankings; (5) **Teacher-Student CL** uses auxiliary networks to guide student curriculum; (6) **Implicit CL** embeds curriculum as a side effect (e.g., progressive deblurring); (7) **Progressive CL** applies curriculum to model capacity or task settings rather than data order. Scheduling strategies span batching, weighting, sampling, iterative, and continuous methods. The survey covers 200+ papers across CV, NLP, speech, robotics, and RL domains.

## Claims

- **Convergence & generalization**: Easy-to-hard data ordering improves convergence speed and final accuracy over random shuffling in vision (CNNs, medical imaging), NLP (machine translation, parsing), and robotics without additional computational cost (Bengio et al., Ionescu et al.).
- **RL-specific pattern**: Reinforcement learning curricula are structurally distinct—primarily task-level or teacher-student rather than data-level—because reward signals and policy spaces allow natural difficulty ordering (Narvekar et al., Florensa et al.).
- **Diversity-accuracy tradeoff**: Curriculum can degrade data diversity and lead to worse results if difficulty measures favor narrow sample subsets early; robust difficulty measures incorporating diversity outperform simple ones (Soviany).
- **Data vs. model vs. task equivalence**: Curriculum applied at model level (e.g., progressive neuron activation) avoids the need for explicit difficulty metrics; both achieve loss smoothing but with different engineering tradeoffs (Morerio et al., Sinha et al.).
- **Teacher-student superiority in complex settings**: Teacher-guided curricula outperform fixed rankings in RL and noisy-label domains by adapting to learner progress (Kim & Choi, Hacohen & Weinshall).
- **Self-paced learning volatility**: SPL methods are robust to label noise and imbalanced distributions but risk convergence failures if scheduling is not carefully tuned; weighting strategies often outperform sampling at comparable cost (Kumar et al., Zhang et al.).
- **Domain-specific heuristics work but are brittle**: Simple criteria (length, frequency, size) show consistent gains but often outperformed by learned or complexity-aware measures; vision transformers and LLMs remain largely unexplored for curriculum (survey gap post-2021).

## Relevance to the project

**RCL's position in the taxonomy**: Recursive Concept Learning sits at the intersection of **task-level + failure-driven + RL-trained** curriculum—a sparsely populated quadrant in the survey. The dendrogram (Fig. 2) shows RL curricula cluster distinctly, dominated by teacher-student and task-level approaches; RCL's concept decomposition strategy is neither predefined (vanilla CL) nor purely adaptive (SPL), but learned-and-ranked via recursive refinement. The survey has ~15 RL entries; fewer than 5 address task-level ordering via learned skill hierarchies.

**Open problems addressed by RCL**: The survey identifies three major unsolved problems that RCL directly targets: (1) **Implicit curriculum from learned difficulty**: most RL work relies on reward or learning-progress signals; RCL's concept-failure ranking is an implicit, orthogonal curriculum criterion. (2) **Model-level curriculum underexplored**: While Sinha et al. (deblurring) and Morerio et al. (dropout scheduling) show promise, the survey notes "a shortage of such studies"; RCL's progressive concept activation is a model-level curriculum variant. (3) **Diversity preservation under curriculum**: The survey warns that "curriculum can degrade diversity"; RCL's multi-concept branching mitigates this by maintaining a concept DAG, not a linear difficulty ordering.

**Limitations as pre-LLM survey**: The survey predates widespread LLM fine-tuning and does not address concept-level decomposition curricula—a gap RCL fills. Pre-training curricula (e.g., task complexity in vision transformers, vocabulary expansion in language models) are mentioned as future work; RCL's concept skeleton approach is complementary, applicable to fine-tuning phases where concept-based curricula have not yet been systematized.

## Source

- arXiv: 2101.10382
- Venue: International Journal of Computer Vision, 2022
- Authors: Petru Soviany, Radu Tudor Ionescu, Paolo Rota, Nicu Sebe
- Raw markdown: `../../../raw/research/rcl-gap-fillers/07-curriculum-survey.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[bengio-curriculum]] — the canonical reference this survey extends; read first for theoretical grounding
- [[acl-deep-rl-survey]] — RL-specific companion survey
- [[../synthesis/recursive-concept-learning]] — RCL maps to a specific quadrant of this survey's taxonomy: task-level + failure-driven + RL-trained
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — wiki's existing data-side curriculum coverage (DOTS); this survey complements with the broader taxonomy
