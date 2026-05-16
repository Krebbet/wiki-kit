---
name: selective-finetuning-overview
description: Theme overview — methods for adding new training signal to a model selectively, without degrading existing behaviour. Fifteen captures across four sub-families: knowledge editing (locate-then-edit), skill localization (sparse parameter masks), continual-learning gradient masking, and PEFT with explicit weight decomposition. Closes the wiki's gap on "selective gradient / behaviour-isolation fine-tuning"; structural sibling to decoding-time-steering (inference-time analogue) and the existing rl-sparse-subnetwork / REASONMAXXER finding (mechanistic substrate).
type: research
---

# Selective fine-tuning — adding capacity without degrading behaviour

Selective fine-tuning methods modify weights *only* in a targeted subset of the network — by location (specific MLP layers, neurons, or attention heads), by structure (orthogonal low-rank subspaces, magnitude vs direction), by mask (per-task binary gradient masks), or by *order* (pre-instruction-tune to shape what continued pretraining encodes). The shared design goal is **isolation**: install new information / capability / behaviour at parameter or subspace $X$ without affecting parameter / subspace $Y$ that carries unrelated capability.

Fifteen captures, four sub-families. The theme is the **weight-level / training-time** complement to [[../decoding-time-steering/_overview]] (inference-time, no weight update) and to [[../rlvr-mechanics/rl-sparse-subnetwork]] (post-hoc observation of sparse-subnetwork emergence under RL). It directly anchors the **R_w extension** to [[../synthesis/proposed-method]] at the weight-modification side, where decoding-time steering anchors it at the inference side.

## Subtrees

### Knowledge editing — locate-then-edit lineage

The dominant approach to surgical weight modification in LLMs. Identify *where* a specific fact / association lives in the network, then *rewrite* only that location.

| Page | Mechanism | Scale |
|---|---|---|
| [[knowledge-neurons]] | Identify *individual neurons* in FFN layers via integrated-gradient attribution; edit/erase by amplifying or suppressing | One neuron per fact (BERT-era) |
| [[ff-kv-memories]] | FF layers = key-value memories: $W_{\text{up}}$ rows are keys, $W_{\text{down}}$ columns are values | Layer-level mechanistic foundation |
| [[rome]] | **Rank-one MLP edit** at the specific mid-layer FF module identified by causal trace | One fact per edit |
| [[memit]] | Scales ROME by distributing edits across critical mid-layers; least-squares solve | **Thousands of edits** on GPT-J 6B / GPT-NeoX 20B |
| [[mend]] | **Hypernetwork** learns to transform the standard fine-tuning gradient via rank-1 decomposition; locate-then-edit at gradient level rather than weight level | 10B+ models, single editor pass |
| [[alphaedit]] | **Null-space projection**: project ROME/MEMIT perturbation onto the null space of preserved knowledge; perturbation cannot affect preserved-fact outputs by construction | +36.7% over baselines; one-line plug-and-play (ICLR 2025 Outstanding) |
| [[knowledge-editing-survey]] | Three-category taxonomy (external-memorisation / global-optimisation / local-modification); six evaluation metrics (success, generalisation, locality, portability, scalability, fluency) | Landscape reference |

### Skill localization & format-vs-substance separation

Empirical evidence that fine-tuned behaviour concentrates in a tiny subset of parameters, and that format/style is separable from content.

| Page | Finding |
|---|---|
| [[skill-localization]] | Grafting finds **~0.01% of params** that carry **>95% of the fine-tuned skill**. Direct empirical answer to "skills isolate to small subsets". |
| [[lima]] | 1000 carefully curated examples beat RLHF-trained DaVinci-003. **Superficial Alignment Hypothesis**: almost all knowledge is in pretraining; alignment is a surface patch teaching format. |
| [[surgical-finetuning]] | Selectively fine-tune subset of *layers* (not params). Different distribution shifts benefit from different layer choices (first layers for input shift; last layers for output shift). Theoretical justification for 2-layer nets. |

### Continual learning — selective gradient masking

Per-task gradient masks or orthogonal subspaces preserve old behaviour while installing new.

| Page | Mechanism |
|---|---|
| [[packnet]] | Iterative pruning + freezing: train on task 1, prune 50%, freeze, train task 2 on freed weights. Canonical pre-LLM existence proof (CVPR 2018). |
| [[hat]] | Per-task **hard attention masks** learned via SGD; previous masks condition new training. Cuts forgetting 45–80%. |
| [[o-lora]] | Each task in a **LoRA subspace orthogonal to all previous tasks**' subspaces. Direct LLM-era realisation; preserves generalisation to unseen tasks. |

### PEFT with explicit weight decomposition

| Page | Decomposition |
|---|---|
| [[dora]] | Weight = **magnitude × direction**: $W = m \cdot V / \|V\|_c$. LoRA on direction only; magnitude as separate scalar. Mimics full-FT update geometry (ICML 2024 Oral). |

### Knowledge injection ordering

| Page | Recipe |
|---|---|
| [[pit]] | **Pre-Instruction-Tuning**: instruction-tune on QA examples *before* CPT on new documents. The model learns "how to encode knowledge for QA-style access" before seeing the documents. **Direct knowledge-injection recipe that preserves QA format.** |

## Cross-cutting findings

### "Information lives in identifiable, isolable parameters" — corpus consensus

All 15 papers converge on the same operational claim: **fine-tuned behaviour, factual knowledge, and task-specific skill are not diffusely distributed — they concentrate in small, identifiable subsets** of parameters, subspaces, layers, or neurons. The implication for the wiki's R_w hypothesis is direct: if behaviour is isolable, then *selective* training that targets only one isolable region can install new capability without disturbing others.

Headline numbers across the family:

| Source | Localisation scale |
|---|---|
| [[skill-localization]] | **0.01% of params** carry **>95% of fine-tuned skill** |
| [[knowledge-neurons]] | Single neurons → single fact (Dai 2021) |
| [[rome]] | One MLP layer + rank-one update per fact (Meng 2022) |
| [[memit]] | Thousands of edits distributed across 4–5 critical mid-layers |
| [[surgical-finetuning]] | A handful of layers per shift type |
| [[o-lora]] | One low-rank LoRA subspace per task, orthogonal to others |
| [[dora]] | Magnitude scalar + direction LoRA — two orthogonal update modes |
| [[hat]] | One binary mask over hidden units per task |
| [[packnet]] | One pruned-then-frozen subnetwork per task |
| [[../rlvr-mechanics/rl-sparse-subnetwork]] | RL touches 5–30% of weights spontaneously |
| [[../rlvr-mechanics/rethinking-rl-sparse-selection]] | REASONMAXXER: rank-8 $W_O$ LoRA at **0.04% params** matches RL |

The numbers span vision (PackNet, HAT) through BERT-era cloze (Knowledge Neurons) through GPT-J / GPT-NeoX / LLaMA. The localisation finding survives architectural and scale generalisation.

### The format-vs-substance separation is mechanically grounded

[[lima]]'s Superficial Alignment Hypothesis ("knowledge from pretraining; alignment is a surface patch") has explicit parameter-level corroboration in [[skill-localization]] (skills graft from 0.01% of params), [[surgical-finetuning]] (which layers matter depends on shift type, and they aren't always the same), and the [[knowledge-editing-survey]] *locality* metric (the explicit goal of leaving non-target outputs unchanged). The user's design goal — "add new data signal without degrading response style" — is the wiki's central distinction stated as an engineering objective; this theme provides the parameter-level machinery to act on it.

### Three structural approaches to selectivity

| Approach | Captured methods | Mechanism |
|---|---|---|
| **Locate then edit** | [[rome]], [[memit]], [[knowledge-neurons]] | Find specific location → overwrite |
| **Project the update** | [[alphaedit]], [[o-lora]], [[mend]] (rank-1 hypernet transform) | Apply update only within a privileged subspace / null space |
| **Mask the gradient** | [[packnet]], [[hat]], [[surgical-finetuning]] | Set $\partial \mathcal{L}/\partial \theta_i = 0$ for $i \notin$ target subset |
| **Decompose the weight** | [[dora]] | Split weight into independent modes; update only one |
| **Order the training** | [[pit]], [[lima]] | Recipe-level isolation via stage ordering |

All five compose. A practical R_w pipeline could (a) use [[pit]]-style ordering, (b) limit fine-tuning to the [[skill-localization]] mask of relevant params, (c) project gradients onto an [[o-lora]] orthogonal subspace, (d) post-edit with [[alphaedit]] null-space projection. None of the captured papers tests this composition.

## Connection to existing wiki anchors

- **[[../synthesis/proposed-method]] R_w extension (2026-05-12).** This theme is the **training-time / weight-level** empirical backbone for R_w, complementing [[../decoding-time-steering/_overview]]'s **inference-time** backbone. Together they give R_w two operational axes — modify weights surgically (this theme) or compose at decode time (decoding-time-steering). Same underlying claim: behaviour is isolable; you can act on one region without disturbing others.
- **[[../rlvr-mechanics/rl-sparse-subnetwork]] (Balashov).** RL spontaneously uses 5–30% of weights. This theme shows the same phenomenon under SFT and gives mechanisms to *enforce* the sparsity.
- **[[../rlvr-mechanics/rethinking-rl-sparse-selection]] (REASONMAXXER).** Rank-8 $W_O$ LoRA at 0.04% params is the closest analogue to [[skill-localization]]'s 0.01% finding at the *token* level. The two papers triangulate the same underlying mechanistic claim from opposite ends (RL token-rerank vs SFT skill-graft).
- **[[../catastrophic-forgetting/ewc-gemma2-cpt]] (EWC).** EWC is the soft-regularisation alternative to this theme's hard-mask / orthogonal-subspace methods. Fisher-weighted penalty vs binary gate / projection — two routes to the same "don't move weights that matter for other tasks" goal. [[../catastrophic-forgetting/_overview]] currently has only EWC as a seed; this theme could be promoted to expand it, or remain its sibling.
- **[[../concept-learning/recursive-concept-evolution]] (RCE).** RCE adds low-rank concept subspaces; [[o-lora]] adds orthogonal LoRA subspaces; [[dora]] decomposes weights into magnitude × direction. Three architectural variants of the same "isolated subspaces for isolated behaviours" idea, at different granularities (concept vs task vs update-mode).
- **[[../decoding-time-steering/repe]] (RepE umbrella).** Activation-space steering — RepE / ITI / ActAdd. This theme's weight-space analogue: ROME / MEMIT / Skill-Localization / Surgical-FT. Same structural argument at different layers of the model stack.
- **[[../single-sample-rl-finetuning/_overview]].** Single-sample at weight level. [[skill-localization]]'s 0.01% finding + [[lima]]'s 1000-example result make this theme's data-floor claim load-bearing for the wiki's single-sample frame.

## Cross-cutting open questions

1. **Does the [[skill-localization]] 0.01% mask survive composition?** If you graft skill $A$ at mask $M_A$ then skill $B$ at $M_B$, do you get both? Or does the second graft erase the first? The paper tests single-skill grafting only.
2. **Composing [[alphaedit]] null-space projection with [[o-lora]] orthogonal subspaces.** Two complementary "perturbation cannot affect $X$" mechanisms — they should compose, but no captured paper tests this.
3. **[[pit]] ordering at scale.** PIT works at 7B / 70B; whether it composes with [[rome]]/[[memit]]-style post-hoc editing for ongoing knowledge updates is untested.
4. **[[skill-localization]] at LLM math scale.** The paper uses BERT-era models; whether 0.01% holds for skills at 7B+ math/reasoning-tuned models is open. [[../rlvr-mechanics/rethinking-rl-sparse-selection]]'s REASONMAXXER finding (0.04% at $W_O$ on Qwen2.5) is suggestive.
5. **Magnitude vs direction across the family.** [[dora]]'s magnitude/direction decomposition is structurally orthogonal to [[o-lora]]'s task-subspace orthogonality. Combining them — "task-orthogonal direction LoRA with separate magnitude" — is unexplored.
6. **Mechanistic substrate of "format" vs "knowledge".** [[lima]] postulates the distinction; [[ff-kv-memories]] gives a layer-level mechanistic story (lower layers = surface patterns, upper layers = semantic / factual). No paper directly tests "fine-tune only upper layers preserves format" vs "fine-tune only lower layers preserves knowledge".

## See also

- [[../synthesis/proposed-method]] — R_w extension; this theme is the training-time backbone
- [[../synthesis/decoding-time-shapes]] — inference-time cousin (logit reweighting + activation steering)
- [[../synthesis/proposer-reward-shapes]] — orthogonal axis (self-play reward shapes)
- [[../decoding-time-steering/_overview]] — inference-time analogue family
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — RL-observed sparsity (mechanism this theme prescribes)
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — REASONMAXXER token-level cousin
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — soft-regularisation sibling

## Source

Theme synthesised 2026-05-13 from 15 captured papers in `raw/research/selective-finetuning/`. Per-paper traceability lives in each sibling page's `## Source` section. The cross-cutting "information is isolable in identifiable parameters" claim is itself a cross-source synthesis, not a direct quotation from any single paper; the parameter-scale numbers in the localisation table trace to their respective sources.
