---
name: moe-adapters-overview
description: Theme overview — converting a dense model into a mixture-of-experts using delta / LoRA adapters as experts (the user's MoERA technique). Seven papers across the lineage: Sparse-Upcycling (dense→MoE ancestor) → BTX (parallel-train then mix) → LoRAMoE (routed LoRA experts for forgetting) → MoV/MoLORA (param-efficient floor) → Self-MoE (self-specialised, no labels) → MoLE (compose pretrained LoRAs) → MoRAM (router-free rank-1). The architectural-avoidance answer to skill-stacking interference; complements catastrophic-forgetting and selective-finetuning.
type: research
---

# MoE via delta / LoRA adapters (the MoERA family)

This theme covers turning a dense model into a **mixture-of-experts where the experts are delta / LoRA adapters** — the literature behind the user's *MoERA* technique (project: MoEModels). The unifying idea: rather than co-training multiple skills into one dense weight matrix (where they interfere — see [[../catastrophic-forgetting/_overview]]), keep a frozen or shared backbone and add **routed, low-rank, additive expert modules**, one per skill/domain, combined by a learned (or self-activating) gate. This is the **architectural-avoidance** answer to the skill-stacking-interference question: skills don't reallocate optimization against each other because they live in separate, separately-trained parameter modules.

## Pages — the lineage

| Page | Position | One-line |
|---|---|---|
| [[sparse-upcycling]] | **Ancestor** (ICLR 2023) | Initialise a sparse MoE from a *dense checkpoint* (seed expert FFNs from the dense MLP). The primitive every later method descends from; T5/ViT beat dense at ~50% of dense sunk cost. |
| [[btx]] | Parallel-train then mix (Meta, 2024) | Branch from seed → train domain experts embarrassingly-parallel → combine FFNs into MoE layers + average rest → MoE-finetune the router. +18.8 math / +13.2 code / +3.6 knowledge over Llama-2-7B. **Zero inter-skill gradient interference by construction.** |
| [[loramoe]] | **Bridge to forgetting** (ACL 2024) | LoRA experts + softmax router as an MoE *plugin*; frozen backbone; **localized balancing constraint** keeps some experts on world-knowledge while others specialise. Explicitly a forgetting-mitigation method. Closest published analogue to MoERA. |
| [[mov-molora]] | Parameter-efficiency floor (Cohere, 2023) | Mixture of Vectors / Mixture of LoRA — extremely-parameter-efficient MoE-adapters; <1% of an 11B model, on par with full FT. The minimal-cost end of the design space. |
| [[self-moe]] | Self-specialised, no labels (2024) | Monolithic LLM → MiXSE: self-specialised LoRA experts built from *synthetic* self-generated data; <0.3% params/expert, ~1% total; +6.5%p avg. The "convert a dense model into MoE without labelled data" recipe. |
| [[mole]] | Compose pretrained LoRAs (ICLR 2024) | Hierarchical weight control to compose multiple *already-trained* LoRAs via learned gating; retrain-free masking mode. The composition end — how to combine independently-built delta experts. |
| [[moram]] | **Router-free** (2026) | Rank-1 adapters as key-value pairs, self-activating via intrinsic-key relevance — no explicit router. Continual-learning framed; minimal interference; bridges back to [[../catastrophic-forgetting/_overview]] and [[../selective-finetuning/ff-kv-memories]]. |

## Design axes

| Axis | Options across the theme |
|---|---|
| Backbone | Frozen ([[loramoe]], [[self-moe]], [[mole]]) vs upcycled/finetuned ([[sparse-upcycling]], [[btx]]) |
| Expert granularity | Full FFN ([[sparse-upcycling]], [[btx]]) vs LoRA ([[loramoe]], [[mole]], [[mov-molora]]) vs vector ([[mov-molora]] MoV) vs rank-1 ([[moram]]) |
| Routing | Learned softmax router ([[loramoe]], [[mov-molora]], [[self-moe]]) vs hierarchical gating ([[mole]]) vs **router-free self-activation** ([[moram]]) vs token-level MoE-finetuned ([[btx]]) |
| Expert training | Jointly with router ([[loramoe]], [[mov-molora]]) vs independently then mixed ([[btx]], [[mole]]) vs self-specialised synthetic ([[self-moe]]) |
| Primary goal | Forgetting mitigation ([[loramoe]], [[moram]]) vs capability/skill addition ([[btx]], [[self-moe]]) vs efficiency ([[mov-molora]], [[sparse-upcycling]]) vs composition ([[mole]]) |

For MoERA specifically: the closest design points are **LoRAMoE** (frozen backbone + routed LoRA experts + balancing constraint — almost exactly MoERA) and **MoRAM** (the router-free variant, if MoERA wants to drop the gate). **MoV/MoLORA** sets the parameter-efficiency floor; **MoLE** answers "how to compose experts you trained separately"; **Self-MoE** answers "how to build the experts without labelled data".

## The skill-stacking answer this theme gives

Where [[../catastrophic-forgetting/_overview]] shows RLVR *implicitly* constrains interference (KL-minimal, off-principal) and [[../selective-finetuning/_overview]] *explicitly* constrains it (masks, null-space), this theme **avoids it architecturally**: separately-trained additive experts cannot reallocate optimization against each other because they do not share a gradient. [[btx]] is the cleanest statement — embarrassingly-parallel expert training means there is *no* inter-skill gradient interference, full stop. [[loramoe]]'s localized balancing constraint is the softer version: jointly trained but with an explicit term reserving expert capacity for prior knowledge. The cost is inference-time routing and (for full-FFN variants) parameter blow-up; the LoRA/vector/rank-1 variants ([[mov-molora]], [[moram]]) are the responses to that cost.

## Connection to existing wiki anchors

- **[[../synthesis/proposed-method]] — R_w / selective behaviour installation.** MoERA-style routed delta-LoRA experts are a *routing-based* realisation of R_w: install a behaviour in one expert without touching the others. Complements the locate-then-edit (ROME/MEMIT) and orthogonal-subspace (O-LoRA) routes in [[../selective-finetuning/_overview]] — same goal (isolated behaviour install), different mechanism (route vs edit vs orthogonalise).
- **[[../catastrophic-forgetting/loramoe]] is shared with that theme** — LoRAMoE is filed here but is *also* the architectural-avoidance entry in the forgetting trichotomy. The two themes are deliberately cross-linked through it.
- **[[../selective-finetuning/o-lora]] / [[../selective-finetuning/dora]].** O-LoRA orthogonalises task subspaces in one model; this theme *routes between* task subspaces. DoRA's magnitude/direction decomposition is the per-expert PEFT primitive MoV/MoLORA mix. Adjacent, not redundant.
- **[[../concept-learning/recursive-concept-evolution]] (RCE).** RCE's growing library of low-rank concept subspaces with a gate is structurally a router-free MoE-of-concept-adapters — [[moram]] is the closest theme-internal analogue (rank-1, self-activating, grown incrementally).
- **[[../selective-finetuning/ff-kv-memories]].** [[moram]]'s rank-1-adapters-as-key-value-pairs framing directly invokes the FF-as-key-value-memory account — the mechanistic bridge between MoE-adapters and the knowledge-editing lineage.

## Open questions

1. **MoERA = LoRAMoE + router-free?** [[loramoe]] (routed, balancing constraint) and [[moram]] (router-free, rank-1) are the two poles closest to MoERA. No captured paper combines LoRAMoE's localized-balancing objective with MoRAM's router-free self-activation — a candidate MoERA design the corpus does not yet test.
2. **Delta-LoRA experts trained by RLVR vs SFT.** Every captured method trains experts by SFT/synthetic data. Whether RLVR-trained experts (which, per [[../catastrophic-forgetting/rls-razor]], are KL-minimal/off-principal) compose *better* under a router than SFT-trained experts is untested and directly relevant to MoERA.
3. **Expert-count scaling and forgetting.** [[loramoe]] reserves capacity via the balancing constraint; [[moram]] adds atomic rank-1 experts incrementally. The $N$-expert degradation curve (does the router itself become the interference bottleneck?) is not characterised across the theme.
4. **Composition of separately-built experts ([[mole]]) vs jointly-trained ([[loramoe]]).** Which yields less interference for MoERA's use case (sequential skill addition)? No head-to-head in the captured corpus.

## See also

- [[../catastrophic-forgetting/_overview]] — the implicit-constraint sibling; shares [[loramoe]] as the hinge
- [[../selective-finetuning/_overview]] — the explicit-constraint sibling (mask/anchor/orthogonalise vs route)
- [[../synthesis/proposed-method]] — R_w; MoERA is a routing-based behaviour-installation route
- [[../concept-learning/recursive-concept-evolution]] — growing low-rank concept library ≈ router-free MoE-of-adapters
- [[../selective-finetuning/ff-kv-memories]] — rank-1-as-KV bridge ([[moram]])

## Source

New theme created 2026-05-16 from 7 papers captured in `raw/research/moe-adapters/`. Per-paper traceability in each page's `## Source`. The lineage ordering, design-axes table, and the implicit/explicit/architectural trichotomy framing are editorial cross-source synthesis.
