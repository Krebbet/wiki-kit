# Continual Learning Mechanisms Compose for Long-Horizon Memorization

Zhang, Zhang, Khashabi, Shu (JHU, arXiv:2609.06986) show that no single classic continual-learning mechanism prevents catastrophic forgetting across 100 sequential SFT tasks, but composing complementary "anchors" (data / function / weight) with a LoRA-merging update rule raises average final retention **28-fold** (1.2% → 34.9%) over naive sequential fine-tuning — with the largest gains super-additive rather than additive. This is a pure-SFT, explicit-mechanism study, distinct in angle from the wiki's existing catastrophic-forgetting cluster, which argues RL resists forgetting *implicitly* via KL-minimal/sparse update geometry ([[rft-mitigates-forgetting]], [[mechanistic-forgetting]]).

## Method

Continual supervised fine-tuning over $T=100$ tasks arriving sequentially, domain-incremental (no task ID at inference), no raw-example retention. The objective adds three retention terms to the current-task SFT loss (Eq. 2): $\Theta_t = \arg\min L_\text{SFT}^t(\Theta) + R_D^t(\Theta) + R_F^t(\Theta) + R_W^t(\Theta)$.

- **Data anchor $R_D$** — generative replay: a frozen copy of the previous model generates 300 pseudo-sequences/task from a task-agnostic replay token; paired with each current-task minibatch; the frozen model also supplies soft next-token targets for the replay sequences (distillation-on-replay). Generalizes Deep Generative Replay (Shin et al. 2017) and LAMOL (Sun et al. 2019).
- **Function anchor $R_F$** — self-distillation (Learning without Forgetting, Li & Hoiem 2017): KL divergence between previous-model and current-model predictions on *current-task* inputs only (distinct from the data anchor's soft targets on replay data).
- **Weight anchor $R_W$** — quadratic importance-weighted penalty $\tfrac{1}{2}(\vartheta - \vartheta^*_{t-1})^\top H_{t-1} (\vartheta - \vartheta^*_{t-1})$, instantiated as EWC (diagonal Fisher), Online EWC (running Fisher), or SI (path-integral importance).
- **Low-rank allocation** — shared LoRA (one adapter reused/continually optimized) vs. **merged LoRA** ($W_t = W_{t-1} + \rho B_t A_t$, folds each task's LoRA into dense weights, reinitializes a fresh adapter next task — adapts ReLoRA's merge-and-reinit pattern to continual learning). Both keep retained-state size constant in task count, unlike O-LoRA or OSRM, whose state grows with $T$.
- **Search**: task-level successive halving (90 initial configs across 3 weight-anchor × 3 function-anchor × 5 replay-hyperparameter × 2 LoRA-allocation choices, pruned at task horizons 10→20→50→100), followed by a full $2^4$ factorial (SI × SD × Replay × Merged-LoRA) × 3 datasets × 3 seeds to isolate main/interaction effects.

## Claims

| Configuration | Avg. final retention (3 datasets) |
|---|---|
| Naive sequential SFT | 1.2% |
| Best standalone mechanism | 8.1% (4.2–12.5% by dataset) |
| Best per-dataset composition | 23.2% (Symbol-QA) / 41.8% (LLM-QA) / 54.8% (Real-QA) |
| All three anchors + merged LoRA | **34.9%** (28× naive; only combo ranking top-3 on all 3 datasets) |

- Replay × Merged-LoRA interaction is significantly positive on all 3 datasets — super-additive: standalone main-effect sum is 3.9–13.9 pts, but the combined gain over naive FT is 15.6–46.9 pts.
- Every configuration surviving to the full 100-task horizon in the successive-halving search combines a data anchor with merged LoRA (Fig. 2).
- **SI × merged-LoRA negative interaction** on Symbol-QA (−3.0pp, p<0.05): SI's carried-forward importance values are tied to the *previous* low-rank factors, but merged LoRA reinitializes fresh factors each task, so SI's constraints get misapplied to functionally different coordinates. Absent on the two natural-language datasets — attributed to Symbol-QA's arbitrary, less-reusable associations making misplaced constraints costlier.
- Growing-state allocation (O-LoRA, sequential OSRM) does **not** consistently beat constant-state merged LoRA on retention, but O-LoRA preserves substantially more general capability than merged LoRA on LLM-QA/Real-QA despite smaller retention gains — a retention-vs-capability trade-off the paper surfaces but doesn't resolve.

## Concept-learning evidence — explicitly disclaimed

The authors are explicit this is a memorization, not generalization, study: *"Memorization rather than generalization... Our results therefore do not establish generalization to new query formulations."* Test-time queries are identical to training queries. No RL connection — pure continual SFT.

## Limitations (authors' own)

- Even the best composition's memory half-life (19–44 tasks depending on dataset) keeps declining with age — composition delays forgetting, does not eliminate it.
- All methods, including the best composition, still show catastrophic forgetting of *general* capability (GSM8K, MATH, MGSM, MMLU-Redux) after 100 tasks — improved task-memorization retention does not transfer to preserved general capability.
- Task-level successive halving is a heuristic that "does not guarantee... the best configuration," though 10-task vs. 100-task ranking agreement was strong post hoc.
- Not a sample-efficiency result: each of the 100 tasks has 50–100 training examples, trained near-saturation before moving on — orthogonal to this wiki's single-sample-training thesis; relevant instead to the catastrophic-forgetting and selective-finetuning themes.

## Relevance to the project

Complementary sub-angle to the wiki's existing forgetting cluster rather than a restatement: [[rft-mitigates-forgetting]] and [[mechanistic-forgetting]] argue RL resists forgetting *implicitly*, without any explicit anchor mechanism, via sparse/off-principal-direction updates; this paper stays entirely in SFT and asks what *explicit* mechanisms can be composed to close the gap to that implicit resistance. The two studies use different training regimes (100-task sequential SFT-only here vs. RL-vs-SFT single/few-task comparisons there) and make no overlapping quantitative claim, so this is a scope difference, not a conflict — noted for anyone comparing final-retention numbers across the two sub-threads.

## Source

- `raw/research/weekly-2026-09-18/03-continual-learning-long-horizon.md`
- arXiv:2609.06986

## Related

- [[rft-mitigates-forgetting]] — RL-implicit-resistance sub-thread this page's explicit-anchor-composition sub-thread complements
- [[ewc-gemma2-cpt]] — both use EWC/Fisher weight regularization; this paper's factorial isolates EWC/Online-EWC/SI as the *weakest* individual lever and finds it can actively hurt when combined with merged LoRA — a more skeptical, quantified take
- [[../selective-finetuning/_overview]] — O-LoRA is already catalogued there under continual-learning gradient masking; this paper adds a head-to-head retention-vs-general-capability trade-off data point for O-LoRA vs. merged LoRA
- [[../../weekly-briefs/2026-09-18]] — brought in by the 2026-09-18 weekly sweep
