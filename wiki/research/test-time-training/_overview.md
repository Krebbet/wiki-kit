# Test-Time Training & In-Context RL — Theme Overview

Two routes to *adaptation at deployment* that bypass conventional pre-training/fine-tuning. **Test-time training (TTT)** updates parameters per-test-input via gradient descent on a synthetic dataset bootstrapped from demonstrations, then discards the update. **In-context RL** (Algorithm Distillation, AD) goes further: a transformer pre-trained on RL learning histories runs its own RL algorithm *in-context*, with no weight updates at deployment. Together they bound the space of "exotic" adaptation methods relevant to single-sample, concept-based learning — TTT is per-input fine-tuning at the limit; AD is gradient-free meta-RL via behaviour cloning of learning curves.

## Papers

- [[ttt-few-shot]] — Akyürek et al. 2024. Per-task LoRA at inference, leave-one-out ICL synthetic data, augmented inference + hierarchical voting. ARC 18.3% → 47.1%; ensembled 61.9% (matches avg human). BBH +7.3pp over ICL.
- [[algorithm-distillation]] — Laskin et al. 2022. Causal transformer distils full RL learning histories; deploys as a *gradient-free* in-context RL algorithm that beats its source's data efficiency. Requires multi-episodic context.

## Cross-cutting synthesis

### TTT durability — can per-input updates become permanent concept updates?
TTT's central design choice is that adapters are *thrown away* per task. The natural follow-up question for David's project: can repeated TTT updates be *merged* (LoRA arithmetic, task vectors) or *distilled* into the base model as a permanent concept library? Akyürek's BBH result — a single shared LoRA across 27 disparate tasks *outperforms* per-task adapters — is a positive signal that concept updates can compose when their gradients are not adversarial. The ARC negative — uniform-format tasks suffer from gradient conflict on a shared adapter — warns that concept families with isomorphic input structure may need orthogonalised subspaces (rank-keyed LoRA, sparse-adapter routing) to coexist.

### In-context RL vs explicit RL
| Axis | TTT (Akyürek) | AD (Laskin) | Conventional RLHF/RLVR |
|---|---|---|---|
| Adaptation locus | Per-task LoRA weights | Pure context (frozen weights) | Permanent weight update |
| Signal type | Supervised LM loss on demos | Action NLL on RL trajectories | Reward / preference / verifier |
| Pre-deployment cost | Optional FT on synthetic data | Full RL run on N tasks → corpus of histories | Reward model + policy training |
| Per-deployment cost | LoRA fine-tune + augmented inference per task | Long-context rollout (quadratic in c) | Inference only |
| Persistence | Discarded after inference | Discarded with context | Permanent |
| Single-sample fit | Direct (K=1 LOO is single-example FT) | Single trajectory, not single (x,y) | Single example → single update (RLOO etc.) |
| Generalisation | Within-task | Across tasks from a meta-distribution | Within RL training distribution |

The two papers occupy opposite corners of the (in-weights, in-context) × (gradient, gradient-free) grid that includes [[../meta-learning-few-shot/maml]] (in-weights, gradient meta-learning) and standard ICL (in-context, gradient-free, no meta-training of the algorithm).

### Method comparison

| Method | Adaptation mechanism | Data needed at deploy | Pre-train requirement | Persistent? | Best result |
|---|---|---|---|---|---|
| Vanilla ICL | Context conditioning | K demos | LM pretraining | No | BBH 50.5% |
| TTT (Direct I/O) | Per-task LoRA on raw pairs | K demos | + optional task-aware FT | No (per task) | ARC ~30% |
| TTT (LOO-ICL + aug + voting) | Per-task LoRA on synthetic ICL tasks | K demos + transformations T | + optional task-aware FT | No (per task) | ARC 47.1% / BBH 57.8% |
| TTT shared adapter | Single LoRA across tasks | K demos × N tasks | LM pretraining | Per session | BBH gain; ARC loss |
| AD | Behaviour cloning over histories, in-context rollout | Trial-and-error episodes (≥2–4 episodes context) | RL histories from N source tasks | No (context only) | Matches RL² asymptote on Dark; > source data-efficiency |
| ED (Expert Distillation, AD baseline) | Behaviour cloning of expert trajectories only | One demo | Expert trajectories from N tasks | No | Maintains input policy, doesn't improve |
| RL² (online meta-RL baseline) | Multi-episode value maximisation | Online interaction | Online meta-training | No (per session) | AD's asymptote |

### Exotic-learning landscape
Relative to the rest of the project corpus:
- **TTT** is closest to [[../meta-learning-few-shot/maml]] (per-task gradient adaptation, modern LoRA-flavoured) and to single-example RL FT ([[../meta-learning-few-shot/learning-from-one-shot]], [[../single-sample-rl-finetuning/1-shot-rlvr]]) but framed at *inference* rather than training.
- **AD** is closest to in-context learning theory ([[../in-context-learning-theory/induction-heads]], [[../in-context-learning-theory/icl-as-gradient-descent]]) — both posit the transformer as an implicit learning algorithm — but explicitly meta-trains on *learning curves* rather than relying on emergent ICL.
- Both bypass the verifier-and-reward stack of [[../rlvr-mechanics/_overview]] entirely. TTT uses supervised LM loss on demos; AD uses NLL on actions from a source algorithm that already solved the credit-assignment problem.
- Neither targets *concept persistence*. The natural composition is: **AD-style in-context discovery → TTT-style per-input distillation → permanent merge**. None of the papers attempt step three.

## Open questions

- **Composability of TTT adapters.** The shared-adapter wins on BBH (text-distinguishable tasks) but loses on ARC (uniform format). What's the boundary, and can it be engineered (orthogonalised subspaces, mixture-of-LoRA routing, task-keyed gating)?
- **Permanent merge.** No experiment tries TTT-then-merge across many tasks. How fast does the base model degrade? Does LoRA-arithmetic (TIES, DARE) preserve the per-task gains when merging dozens of throwaway adapters?
- **Single-sample TTT.** Akyürek operates at K=2–10 demos. With K=1, LOO degenerates and the augmentation pipeline becomes the entire signal — open whether ARC-style invertible transforms generalise to text concepts.
- **AD without an RL source.** AD requires N converged RL runs as a pretraining corpus. For LLM concept learning, what is the analogue of a "learning history" — chains of self-correction, [[../critique-self-correction/reflexion]]-style retry traces, distillation-from-search trajectories? Could D consist of teacher–student CoT improvement curves rather than RL histories?
- **Context length scaling.** AD's emergence requires multi-episodic context. For language tasks where one "episode" might be a whole document, multi-episode context demands hundreds of thousands of tokens — feasibility and cost?
- **Why some tasks resist TTT.** *Boolean Expressions* declines under TTT (85.7% → 80.4%); algorithmic step-by-step tasks gain little. Is this a signal that TTT helps *pattern recognition* concepts more than *procedural* ones — and how does that map onto the project's concept taxonomy?
- **Distribution-shift cost.** ARC public 61.9% vs semi-private 47.5% — TTT's per-task fitting may overfit to subtle benchmark idiosyncrasies. How does this trade off against the obvious overfitting protection of having only K demos?

## Source

See individual paper pages: [[ttt-few-shot]], [[algorithm-distillation]].

## Related themes

- [[../in-context-learning-theory/_overview]] — what computation does the frozen transformer actually run? AD shows it can run an *RL algorithm* given the right pretraining.
- [[../meta-learning-few-shot/_overview]] — TTT is meta-learning's inference-time cousin; AD is offline meta-RL via sequence modelling.
- [[../single-sample-rl-finetuning/_overview]] — adjacent: permanent weight updates from one (x, r) pair vs TTT's throwaway LoRA from K demos.
- [[../self-improvement/_overview]] — Reflexion, Self-Refine, STaR — produce the kind of "learning trajectories" AD's recipe would consume; potential synthesis path.
- [[../rlvr-mechanics/_overview]] — verifier-driven permanent updates; complement to TTT's verifier-free demonstration-only adaptation.
