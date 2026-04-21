# Full-Parameter Continual Pretraining of Gemma2: Insights into Fluency and Domain Knowledge

Šliogeris et al. (Neurotechnology, May 2025, arXiv:2505.05946) empirically study the tradeoff between linguistic fluency and domain knowledge in continual LLM pretraining. Applying Elastic Weight Consolidation (EWC) with Fisher information estimated on MMLU, they continually pretrain Gemma2-2B on 10% Lithuanian CulturaX, demonstrating that EWC preserves English domain knowledge (7/7 benchmarks) while improving Lithuanian fluency and domain knowledge (5/7 benchmarks).

## Method

**Setup:** Two-task continual learning: task A = initial Gemma2 pretraining; task B = next-token prediction on 10% of CulturaX Lithuanian component. EWC regularizer (Eq. 3): L_B(θ) + (λ/2) Σ_i F_i (θ_i − θ_{A,i})².

**Fisher estimation** (Eq. 4): Empirical Fisher F_i = (1/|D_MMLU|) Σ_{(x,y)∈D_MMLU} (∂ log p_θ(y|x) / ∂θ_i)², computed on MMLU benchmark data (15.9K instances, 57 tasks). Tested regularization strengths λ ∈ {0, 10², 10³, 10⁶, 10⁹, 10¹²}.

**Metrics:** Linguistic fluency = perplexity on TruthfulQA (English, Table 1) and Lithuanian Q/A (Fig. 2). Domain knowledge = accuracy on 7 language understanding benchmarks (Table 1): MMLU, Belebele, GSM8K, HellaSwag, ARC-Easy, TruthfulQA, Winogrande, evaluated in both English and Lithuanian. Training: AdamW, lr=0.0002, batch size 2, warm-up 5%, weight decay 0.01 on 8 H100 GPUs (~4h per λ, 24h total).

## Claims

- EWC mitigates catastrophic forgetting: English perplexity approaches baseline Gemma2 as λ increases (Fig. 1a); English domain knowledge preserved on all 7 benchmarks (Sec. 4, "Results").
- Optimal λ range [10², 10¹¹] improves Lithuanian domain knowledge on 5/7 benchmarks: ARC-Easy, GSM8K, HellaSwag, MMLU, Winogrande; English accuracies improve or maintain (Fig. 3).
- EWC recovers mathematical ability (GSM8K): λ > 10⁶ prevents knowledge forgetting observed in unregularized continual pretraining (Sec. 4, para 3).
- Perplexity-domain knowledge correlation: lower perplexity on TruthfulQA aligns with higher accuracy on domain benchmarks (Fig. 1b, discussion in Sec. 4).
- Over-regularization (λ > 10¹¹) freezes model: Lithuanian perplexity rises (Fig. 2), accuracies stagnate near baseline, indicating insufficient plasticity.
- No external training data required: achieves domain-aware continual pretraining on low-resource Lithuanian using only MMLU-based Fisher for importance weighting.

## Relevance to the project

**Localizing single-sample updates.** EWC exemplifies parameter importance via second-order information (Fisher). For [[../synthesis/single-sample-concept-skeleton]]'s catastrophic-forgetting gap, EWC offers a concrete solution: weight updates by Fisher-estimated parameter sensitivity computed on held-out task-relevant data. In single-sample concept learning, replacing MMLU with a held-out validation set (e.g., 5–10 examples per concept) could guide which weights to update and how aggressively. **Limitation:** EWC assumes access to a representative dataset for Fisher estimation; true single-sample settings may lack this. Moreover, diagonal Fisher approximation (Eq. 4) ignores parameter interactions—richer approximations (cf. [[../rlvr-mechanics/structured-fisher-optimizer]]) could better identify concept-specific subnetworks.

**Connection to sparse subnetwork selection.** EWC indirectly selects salient parameters (high F_i). The paper does not explicitly examine sparse updates, but varying λ implicitly controls how "locked" high-importance parameters become. For [[../rlvr-mechanics/rl-sparse-subnetwork]], this suggests: jointly optimize sparsity mask and EWC strength to isolate concept-specific parameters while preserving base knowledge.

**Domain knowledge as a concept primitive.** The paper treats domain knowledge and linguistic fluency as separable, measurable outcomes. However, adding a new language (Lithuanian) is a long-tail, domain-generalization task, not concept learning in the usual sense. **What the paper does not address:** (1) whether individual *concepts* (e.g., "arithmetic") within a language can be cleanly separated and updated without inter-concept forgetting; (2) how to scale single-sample concept updates (100 tokens per concept) vs. 10% of a 100B-token corpus; (3) whether Gemma2's 2B scale generalizes to larger models where catastrophic forgetting dynamics differ.

## Source

- arXiv: 2505.05946
- Raw markdown: `../../../raw/research/adjacent-reward-signals/05-ewc-gemma2-cpt.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/ewc-gemma2-cpt.pdf`

## Related

- [[../rlvr-mechanics/learning-to-think]] — Fisher for parameter weighting and importance
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — sparse parameter selection; EWC as implicit importance mask
- [[../synthesis/single-sample-concept-skeleton]] — catastrophic forgetting in minimal-data regimes
- [[../meta-learning-few-shot/maml]] — continual learning from few-shot perspective
- [[../data-efficient-survey/limited-data-ft-survey]] — regularization for parameter-efficient adaptation
