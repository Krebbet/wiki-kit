# Modular Deep Learning (Pfeiffer, Ruder, Vulić, Ponti)

The canonical synthesis of the modular deep learning literature (TMLR 2023). Surveys ~300 papers across NLP, vision, and RL and argues that adapters, LoRA, MoE, progressive networks, neural module networks, and options-in-RL are all special cases of one abstract framework: a set of *modules* selected by a *routing function* and combined by an *aggregation function*, trained under one of three settings. The authors introduce a 4-axis taxonomy and show every variant reduces to the same functional form $f_\theta(x) + f_\phi(x)$, where $\theta$ are shared backbone weights and $\phi$ are module-specific parameters.

## The 4-axis taxonomy

### Computation function

*How is each module implemented?* Three canonical forms, all reducible to $f'_i(x) = f_\theta(x) + f_\phi(x)$ (He et al. 2022 unified view):

- **Parameter composition** — $f'_i(x) = f_{\theta \oplus \phi}(x)$; module is an element-wise weight delta. Examples: sparse subnetworks (LTH), [[research/lora]] ($\phi = BA$), supermasks. Inference-efficient, training-slow.
- **Function composition** — $f'_i(x) = f_{\phi_i}(f_{\theta_i}(x))$; new sub-function wraps the frozen backbone. Examples: [[research/adapters-houlsby]], parallel adapters, $(IA)^3$ rescaling. Highest parameter count; best empirical performance.
- **Input composition** — $f'_i(x) = f_{\theta_i}([\phi_i, x])$; module is prepended to the input. Examples: soft/continuous prompts, prefix tuning, retrieval augmentation. Most parameter-lean; weakest for small models.
- **Hypernetworks** — $\phi = W\alpha$; a small network generates module parameters conditioned on a task embedding $\alpha$. Examples: FiLM, T-Few, Hyper-X. Unified view: acts simultaneously as computation and routing.

Trade-off (survey Table 3): parameter composition is inference-efficient but training-slow; input composition is parameter-lean but hurts inference speed; function composition incurs the most parameters but achieves the best downstream performance.

### Routing function

*How are active modules selected?*

**Fixed routing** (§4.1): routing matrix $A \in \{0,1\}^{|T| \times |M|}$ determined a priori by metadata (task identity, language, domain). Most PEFT methods fall here — each task deterministically receives its own adapter column. Sequential function aggregation (language module → task module, as in MAD-X) is the canonical fixed-routing pattern.

**Learned routing** (§4.2): routing parameters $\rho$ trained jointly with modules. Three sub-types:

- *Hard learned* (§4.2.2) — binary $\alpha \in \{0,1\}^{|M|}$, via RL (REINFORCE/PPO), evolutionary search (PathNet), or Gumbel-Softmax. Inactive modules excluded from the forward/backward pass. Harder to train but efficient. Supports variable-size module sets. Examples adjacent in the wiki: [[research/sheared-llama]] (per-layer binary masks ≈ hard learned with structured sparsity).
- *Soft learned* (§4.2.3) — continuous $\alpha \in [0,1]^{|M|}$ as a probability distribution. MoE (Shazeer 2017, Switch Transformer, GLaM) is the canonical case; top-$k$ MoE sits between hard and soft. **Token-level routing** (§4.2.3) is the dominant MoE mode; see caution below. Key pathologies: training instability (cold-start routing), module collapse, overfitting to noise.
- *Hypernetworks as routing* (§4.2.4) — task embedding $\alpha_t \in \mathbb{R}^{|M|}$ acts as unnormalised routing scores over a generator matrix $\Phi \in \mathbb{R}^{d \times |M|}$.

**Routing level** (§4.3): global (one decision per model), per-layer (independent decision at each layer — search space grows as $|M|^l$), hierarchical. Neural Module Networks use a parser-generated tree as the routing structure.

Empirical note: Mittal et al. 2022 found learned routing consistently underperforms fixed routing in synthetic settings (under-utilises modules). Ponti et al. 2022 showed learned routing can win when tasks are procedurally constructed. Fixed routing dominates in practice.

### Aggregation function

*How are outputs of active modules combined?* Mirrors the computation taxonomy but applies across multiple active modules:

- **Parameter aggregation** — interpolate weights in weight space; enabled by linear mode connectivity (Frankle et al. 2020). Examples: LT-SFT ($\theta' = \theta_0 + \phi_l + \phi_t$), model arithmetic (Ilharco 2022), SMEAR. Adjacent pages: [[research/dcr]], [[research/ligo]], [[research/bert2bert]].
- **Representation aggregation** — weighted average of module output vectors $f'(x) = \sum_j \alpha_j h_j$. Examples: MoE weighted sum, AdapterFusion attention, Polytropon averaging. Adjacent: [[research/btm]], [[research/btx]], [[research/demix]], [[research/sparse-upcycling]].
- **Input aggregation** — concatenate multiple module inputs. Examples: multi-prompt concatenation, retrieval-augmented generation.
- **Function aggregation** — sequential composition $f' = f_{\phi_1} \circ \cdots \circ f_{\phi_{|K|}}$ or hierarchical tree. Examples: MAD-X (language → task adapters in series), Neural Module Networks.

AdapterFusion (Pfeiffer 2021) is attention-based representation aggregation: query = layer input $x$, keys/values = stacked module outputs $H_i$; allows post-hoc discovery of which pre-trained adapters help a new task.

### Training setting

*When are modules trained?*

1. **Joint multitask** (§6.1): modules and routing trained simultaneously from random init. Canonical in MoE (Shazeer 2017, Fedus 2021) and RL routing networks. Pages: [[research/btm]], [[research/btx]], [[research/sparse-upcycling]], [[research/demix]].
2. **Continual learning** (§6.2): modules added sequentially per task; past modules frozen to prevent forgetting. Progressive Networks (Rusu 2016), PathNet, PackNet. Pages: [[research/bert-of-theseus]], [[research/iterative-layer-distill]], [[research/bert2bert]], [[research/ligo]].
3. **Parameter-efficient transfer** (§6.3): base model frozen post-pre-training; modules added and fine-tuned per task. Dominant paradigm for current LLMs. Pages: [[research/lora]], [[research/adapters-houlsby]], [[research/brecq]], [[research/gptq]], [[research/awq]], [[research/omniquant]], [[research/spinquant]].

These are not mutually exclusive: joint multitask pre-training can be followed by post-hoc modular fine-tuning.

---

## Goal-mapping for this wiki

**G1 — Training isolated transformer blocks that remain swappable**

Survey terminology: *function composition* (sequential adapter layers / full transformer blocks as modules) or *parameter composition* (LoRA-style within-layer replacement); *fixed routing* (each block position always receives the same module, gradient does not cross block boundaries); *continual learning* or *parameter-efficient transfer* training setting.

Fitting pages: [[research/bert-of-theseus]] (stochastic block replacement ≈ Bernoulli-gated fixed routing between student and teacher blocks), [[research/dcr]] (continuous weight interpolation between module versions ≈ §5.1 parameter aggregation), [[research/iterative-layer-distill]] (heal-after-removal ≈ continual learning + module pruning), [[research/decoupled-greedy-learning]] (function composition + per-layer auxiliary loss + gradient stop = extreme fixed routing with local training), [[research/greedy-infomax]] (same pattern), [[concepts/block-isolation-training]].

**G2 — Per-block dynamic parameter allocation during training**

Survey terminology: *parameter composition* (LoRA rank varies per block) or *function composition* (variable-size adapter per block); *hard learned routing* with variable-size module activation (§4.2.2 — "variable-size (threshold)" or "variable-size (soft partition)"); *joint multitask* training setting.

Fitting pages: [[research/sheared-llama]] (structured pruning + per-layer allocation ≈ learned hard routing with per-layer binary masks), [[research/omniquant]] (per-block differentiable calibration ≈ block-wise parameter composition), [[research/spinquant]] (per-layer rotation as parameter composition module).

**G3 — Token-conditional routing through a pool of blocks**

Survey terminology: *function composition* (full transformer blocks as experts); *soft or hard learned routing*, specifically token-level MoE (§4.2.3); *representation aggregation* via top-$k$ weighted sum; *joint training from scratch* (§6.1).

Fitting pages: [[research/layerskip]] (per-layer early-exit ≈ hard routing with identity-function option at each depth, AdaShare analogue), [[research/btm]], [[research/btx]], [[research/sparse-upcycling]], [[research/demix]], [[concepts/token-conditional-routing]], [[research/sleb]] (block elimination ≈ extreme fixed routing: route to skip).

**Cross-cutting — Post-hoc block-wise reconstruction (PTQ)**

[[research/brecq]], [[research/gptq]], [[research/awq]], [[research/omniquant]], [[research/spinquant]] fit *parameter composition / post-hoc transfer* (§3.1, §6.3). The local Hessian-based block reconstruction in BRECQ/GPTQ is structurally identical to the block-isolation training primitive in G1 — the survey does not discuss PTQ directly, but the structural parallel is tight.

---

## Key cautions / takeaways

1. **Functional equivalence with different empirical trade-offs**: all three computation forms reduce to $f_\theta(x) + f_\phi(x)$ (He et al. 2022), but function composition outperforms parameter composition, which outperforms input composition in head-to-head comparisons, especially for small models.

2. **Fixed routing dominates in practice**: learned routing suffers from training instability, module collapse, and overfitting; Mittal 2022 found it consistently underperforms fixed routing in controlled experiments. Mitigations: auxiliary load-balancing loss (Switch Transformer), ε-greedy warm-up, metadata conditioning.

3. **§4.2.3 caution — token-level MoE routing impedes task-level specialisation**: load-balancing constraints prevent routing entire examples to a single expert, so token-level MoE modules cannot capture sentence-level semantics or compositional task structure. For G3 goals (block specialisation via token routing), example-level or task-level routing is more appropriate than pure token-level MoE.

4. **Linear mode connectivity enables weight-space aggregation**: models fine-tuned from the same initialisation reside in the same loss basin (Frankle 2020), making weight interpolation viable — underpins model merging, LT-SFT compositional aggregation, and SMEAR.

5. **Module specialisation requires explicit inductive biases**: competition (top-$k$), orthogonality constraints on domain modules, and load-balancing losses are all needed to prevent collapse. Vanilla joint training does not guarantee specialisation.

6. **Post-hoc modularity is the dominant LLM paradigm**: adapters/LoRA achieve near-full-FT performance at <0.5% updated parameters. Community sharing (AdapterHub) demonstrates that modular models enable distributed, asynchronous development.

### 12 open questions (§9.1)

1. Combining computation function types — sparse/low-rank combined with function composition is underexplored.
2. Learned module structure — per-module NAS remains open; current modules share a fixed architecture.
3. Standardising modularity evaluation — no agreed benchmark; current evals repurpose downstream NLP datasets.
4. Nature of modular representations — how do the four axes each influence what is learned?
5. Hierarchical modularity — clean separation between high-level skill modules and low-level feature modules.
6. Learned routing for pre-training — fixed routing requires metadata that may not exist at pre-training time.
7. Modular instruction tuning — linking per-skill modules to instruction-tuning decompositions of capability.
8. Benchmarking routing methods — no metrics for routing quality or module specialisation degree.
9. Structured and sparse aggregation — aggregating within salient subnetworks for OOD generalisation.
10. Learned aggregation — non-linear or domain-specific aggregation functions beyond arithmetic operations.
11. Merging modular models — designing modules specifically to be mergeable; training by merging specialists.
12. Extensible multi-task models — modular pre-training that supports base-model extension without retraining.

---

## Credibility

- **Venue / year:** TMLR 2023 (open-review; post-publication reviews public on OpenReview)
- **Code:** not applicable (survey)
- **Authors / lab:** Pfeiffer (Meta AI / Google DeepMind) — creator of AdapterHub; Ruder (Cohere); Vulić (Cambridge); Ponti (Edinburgh) — all senior figures in modular NLP; survey cites ~300 papers, covers literature to mid-2023
- **Replication status:** not applicable (survey)

---

## Source

- `raw/research/selective-replacement-and-training/30-modular-deep-learning.md` (PDF capture; survey ≈370 KB)
- `raw/research/selective-replacement-and-training/12-modular-deep-learning-abs.md` (arXiv abstract)

---

## Related

This is the crossroads page — every existing wiki page slots into one or more taxonomy cells.

**Computation function**
- Parameter composition: [[research/lora]], [[research/adapters-houlsby]] (also function composition); [[research/brecq]], [[research/gptq]], [[research/awq]], [[research/omniquant]], [[research/spinquant]] (post-hoc block-wise)
- Function composition: [[research/adapters-houlsby]], [[research/bert-of-theseus]], [[research/dcr]], [[research/decoupled-greedy-learning]], [[research/greedy-infomax]]
- Input composition / mixture-of-experts (full-block): [[research/btm]], [[research/btx]], [[research/sparse-upcycling]], [[research/demix]]

**Routing function**
- Token-conditional / depth routing: [[research/layerskip]] (hard, depth); [[concepts/token-conditional-routing]]
- Domain-conditional / fixed: [[research/demix]], [[research/btm]] (ensemble / fixed per domain)
- Continual / progressive replacement: [[research/bert-of-theseus]], [[research/dcr]], [[research/iterative-layer-distill]]
- Structured pruning as learned hard routing: [[research/sheared-llama]], [[research/sleb]], [[research/lottery-ticket-bert]]

**Aggregation function**
- Representation aggregation (MoE weighted sum): [[research/btm]], [[research/btx]], [[research/sparse-upcycling]], [[research/demix]]
- Parameter aggregation (weight-space merge): [[research/dcr]], [[research/ligo]], [[research/bert2bert]]

**Training setting**
- Post-hoc parameter-efficient transfer: [[research/lora]], [[research/adapters-houlsby]], [[research/brecq]], [[research/gptq]], [[research/awq]], [[research/omniquant]], [[research/spinquant]]
- Joint with module replacement: [[research/bert-of-theseus]], [[research/dcr]], [[research/iterative-layer-distill]]
- Continual / growth: [[research/bert2bert]], [[research/ligo]]
- Continual with pruning: [[research/sheared-llama]], [[research/sleb]], [[research/lottery-ticket-bert]]
- Gradient-isolated / decoupled: [[research/decoupled-greedy-learning]], [[research/greedy-infomax]]

**Concept anchors**
- [[concepts/block-isolation-training]], [[concepts/token-conditional-routing]]

> All taxonomy-relevant papers in the surveyed corpus are now ingested (initial gaps for [[calm]], [[mod]], [[legonn]], [[shortgpt]] resolved on 2026-04-30). See [[research-queue]] for next-priority follow-ons (SmoothQuant, AdaRound, AdaLoRA, Switch Transformer, V-MoE, Mixtral, hash routing).
