# Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks

Finn, Abbeel, Levine (ICML 2017). MAML learns an initialization θ such that one (or a few) SGD steps on K examples from a new task yield strong performance. It is model-agnostic — applicable to any gradient-trained architecture and to supervised classification, regression, or RL — and introduces no extra learned parameters beyond the model itself.

## Method
- Bi-level optimization. Inner loop adapts per task: θ'_i = θ − α ∇_θ L_{T_i}(f_θ) (one or a few steps with K samples).
- Outer (meta) loop minimizes loss of the *adapted* params on held-out task data: min_θ Σ_{T_i ~ p(T)} L_{T_i}(f_{θ'_i}), updated via θ ← θ − β ∇_θ Σ L_{T_i}(f_{θ'_i}).
- Meta-gradient requires a gradient-through-a-gradient (Hessian-vector products). A first-order approximation (drop the second-derivative term) works almost as well — the authors attribute this to ReLU networks being locally near-linear.
- Algorithms 1–3 instantiate MAML for the general case, supervised few-shot, and policy-gradient RL (with REINFORCE inner / TRPO outer).

## Claims
- Omniglot 5-way 1-shot/5-shot: 98.7% / 99.9% (Table 1) — matches or narrowly beats matching nets, neural statistician, memory-augmented nets, with fewer parameters.
- MiniImageNet 5-way 1-shot/5-shot: 48.70% / 63.11%; first-order MAML 48.07% / 63.15% (Table 1) — beats matching nets and meta-learner LSTM by ~5pp on 1-shot.
- Sinusoid regression: MAML adapts from 5 datapoints and continues improving with more gradient steps; standard pretraining catastrophically overfits (Fig. 2–3).
- RL (2D nav, half-cheetah, ant locomotion): MAML reaches good policies in 1–3 gradient steps where pretrain+finetune sometimes underperforms random init (Figs. 4–5).
- Multi-task baselines (averaging in parameter space, ℓ2-to-mean) all underperform MAML (Table 2), showing MAML is more than "average parameters."

## Sample efficiency
"Few-shot" = K examples per class (K ∈ {1, 5}) for an N-way task drawn from a meta-distribution p(T). The enabling mechanism is *meta-training the initialization* over many tasks so that the loss surface near θ is sensitive in directions aligned with task structure — small gradient steps then produce large per-task gains. Sample efficiency comes from amortizing prior task experience into θ; per-task data is small but cumulative meta-training data is huge.

## Relevance to the project
MAML is the canonical "learn-to-fine-tune" algorithm and the closest pre-LLM analogue of David's single-sample fine-tuning idea. The framing — pre-arranging weights so a single update on a single example moves the model into a useful regime — transfers conceptually to LLMs: a base LLM's pretraining can be viewed as an implicit (un-)meta-learned initialization that already supports in-context few-shot adaptation (Brown et al. 2020). What is missing for the LLM regime: (a) MAML assumes a known task distribution p(T) sampled at train time, whereas LLM users want *concept-level* generalization from one instance with no curated meta-tasks; (b) Hessian-vector meta-gradients are infeasible at 7B+ parameters, so any MAML-for-LLM must use first-order or implicit-gradient surrogates (cf. Reptile, iMAML); (c) MAML adapts via SGD on labels, but the most interesting LLM "single-sample" updates arrive via RL signals or self-generated traces. David's project differs in seeking concept-based, non-task-distributional updates — closer in spirit to MAML's "sensitivity" principle than to its training procedure.

## Source
- Venue: ICML 2017 (PMLR 70). arXiv: 1703.03400
- Raw markdown: `../../../raw/research/single-sample-llm-learning/14-B-1-maml-finn.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/B-1-maml-finn.pdf`

## Related
- [[prototypical-networks]] — metric-based contrast to MAML's gradient-based meta-learning.
- [[learning-from-one-shot]] — single-shot learning *without* any pretraining or meta-training.
- [[../in-context-learning-theory/_overview]] — LLM analogue of fast adaptation without weight updates.
- [[../test-time-training/_overview]] — adapting weights at inference, a modern descendant of MAML's inner loop.
