# Token-Conditional Routing

**Token-conditional routing** is the design pattern in which different tokens take different computational paths through a model — selecting which block(s) to execute, when to exit, which expert to dispatch to, or which depth to use — based on a per-token signal computed at inference (and typically learned during training). The wiki owner's **G3** experiment is the strongest form of this: a pool of transformer blocks where a router selects which block(s) process each token, replacing the static n-layer flow.

This page is a synthesis anchor. After two ingest runs (12 + 15 papers), the routing-primitive landscape has multiple distinct flavours, all relevant to G3 in different ways. The **load-bearing cross-cutting caution** from the Modular Deep Learning survey (§4.2.3) frames the design space before the taxonomy: token-level routing introduces a load-balancing constraint that can *prevent* task-level specialisation by pushing the router toward uniform expert utilisation regardless of input.

## Cross-cutting design caution *(synthesis from [[modular-deep-learning]] §4.2.3)*

> Token-level MoE routing introduces a load-balancing auxiliary loss that pushes the router toward roughly uniform expert utilisation. This *impedes task-level specialisation*, because the load-balancing pressure conflicts with the gradient signal that would otherwise concentrate semantically-related tokens on a small number of experts. Coarser routing granularities (per-sequence, per-domain, per-example) avoid the conflict and are typically preferred when the goal is interpretable specialisation; per-token routing wins when the goal is FLOP-efficient compute allocation.

For G3, this implies a fork: if the wiki owner wants the block pool to *specialise* (different blocks doing recognisably different things), per-token routing may be the wrong primitive — domain / example / sequence routing scales better for specialisation. If the goal is purely compute-efficient FLOPs, per-token routing is well-validated by [[mod]] and [[sparse-upcycling]].

## The routing-primitive taxonomy

Five distinct primitives appear in the surveyed corpus, each with different specialisation / efficiency / training tradeoffs:

| Primitive | What's chosen per token | Selection mechanism | Trained? | Canonical citations |
|---|---|---|---|---|
| **Per-token early exit** | Where to stop in depth | Confidence threshold (or learned classifier) | Pre-condition trained ([[layerskip]]); decision typically heuristic ([[calm]]) or future-work-pointing | [[calm]] (confidence-based), [[layerskip]] (training-time prefix-isolation pressure) |
| **Per-token depth routing** | Which layers to execute | Top-k learned router per layer; static tensor sizes | Yes — router trained jointly | [[mod]] (primary citation; per-block top-k across depth) |
| **Per-token FFN expert routing** | Which expert in a layer | Top-k learned softmax router; load-balanced | Yes — router trained jointly with experts | [[sparse-upcycling]] (copy-and-train; ICLR 2023), [[btx]] (post-hoc on independent FFN training) |
| **Domain-conditional / coarser routing** | Which expert in a layer | Domain hash / document metadata (deterministic, not per-token learned) | Experts trained per-domain; routing is metadata-driven | [[demix]] (domain hash), [[btm]] (ensemble / weight-average — implicit routing) |
| **Skip-as-routing** | Whether to execute a layer at all | Layer-level dropout (training pressure); inference selection out-of-band | Yes (dropout schedule); no learned router | [[layerskip]] (skip-pressure during training), [[sleb]] (one-shot removal of low-utility blocks — degenerate router) |

Hash-based / fixed-routing alternatives ([[hash-routing]], queued) and Mixture-of-Modular-Experts variants are not yet ingested.

## What's been empirically demonstrated

- **Per-token depth routing matches dense at fraction of FLOPs.** [[mod]]: 12.5% top-k empirically optimal at 2048-token sequences up to ~1e20 FLOPs; matches baseline at equivalent FLOPs / wall-clock; ~50% faster post-training sampling.
- **Copy-and-train MoE bootstraps from dense beat both dense continuation and MoE-from-scratch.** [[sparse-upcycling]]: T5 Base/Large/XL and ViT B/L upcycled from dense checkpoints outperform their dense counterparts on SuperGLUE / ImageNet at ~50% of dense pretraining compute.
- **Independent expert training + post-hoc learned routing beats independent training + ensemble.** [[btx]]: Llama-2 7B seed → 4 domain experts → MoE finetune outperforms [[btm]]'s ensemble baseline on all tasks at lower inference cost.
- **Per-token confidence-based early exit yields up to ×3 certified speedup.** [[calm]]: T5-XXL summarisation, MT, QA — no quality loss at 1.2–1.5 layers average instead of 24. Oracle ceiling is ×5.2.
- **Domain-conditional FFN experts can be added/removed/mixed at inference.** [[demix]]: an expert can be removed (zero-cost deactivation), a new expert added (DEMIX-DAPT freezes all but the new expert), and experts mixed at inference via parameter-free Bayesian posterior.

## Where the evidence is incomplete (transfer to G3)

- **Block-pool routing**, the most direct G3 instantiation, is not directly demonstrated by any surveyed paper. [[mod]] routes through *depth* (skip or process) but does not select among multiple alternative blocks; [[sparse-upcycling]] / [[btx]] / [[demix]] all route within an FFN layer's expert pool but layers themselves stay in fixed positions. The cross-product (multiple alternative *full transformer blocks* per position with a learned router) is unmapped.
- **Joint-from-scratch training of pool + router** is also unmapped. [[mod]] trains jointly but only chooses skip-vs-execute. [[sparse-upcycling]] / [[btx]] both bootstrap from dense (the experts are warm-initialised from a converged backbone). Whether a randomly-initialised pool of blocks plus a randomly-initialised router can be trained from scratch is open.
- **Specialisation vs. load-balancing** is an unresolved tension. [[modular-deep-learning]] §4.2.3 is explicit that token-level routing prevents specialisation; [[mod]] and [[sparse-upcycling]] are token-level and report no specialisation analysis. [[demix]] gets specialisation by routing coarser (per-document). Which side of the tradeoff G3 should sit on depends on whether the wiki owner cares more about per-token compute-efficiency or block-level interpretable specialisation.
- **Pool size and initialisation** are unstudied at G3 granularity. MoE literature has K=8 (Mixtral), K=64 ([[btm]]); whether transformer-block pools should be small-and-specialised or large-and-redundant is open.
- **Routing latency.** [[mod]]'s top-k is non-causal at training and uses an auxiliary predictor at inference; [[calm]] adds a confidence computation per token; [[btx]]'s learned router adds a softmax per layer per token. The wall-clock cost of a transformer-block-pool router is bounded but not characterised at scale.

## Cross-source themes *(synthesis)*

- **Static tensor sizes are load-bearing** for hardware efficiency. Both [[mod]] (top-k with k a-priori-defined) and [[sparse-upcycling]] (top-k routing with fixed expert capacity) explicitly preserve static tensor shapes — dynamic-shape routing is theoretically more flexible but production-impractical. G3 should plan for static-tensor routing.
- **Train router separately from pieces is more reliable than joint from scratch.** Across [[btx]] (independent experts then router finetune), [[sparse-upcycling]] (warm-init experts from dense), and [[calm]] (router on a pretrained T5), the surveyed work consistently bootstraps the pool first and the router second. No surveyed work reports successful joint random-init training at scale.
- **Routing decisions degrade more gracefully than architectural choices.** [[layerskip]] / [[mod]] / [[calm]] all show that the *training-time* decision (e.g., LayerSkip's exponential dropout schedule, MoD's k=12.5%, CALM's confidence threshold) tolerates moderate distribution shift at inference. The router's *parameters* drift gracefully; the *router's existence* is more rigid.

## Open questions for G3 transfer

1. **Pool granularity.** Per-token across full transformer blocks (G3 strict reading), per-token across FFN-only sub-blocks (the [[btx]] / [[demix]] / [[sparse-upcycling]] pattern), or per-sequence across full models ([[btm]] ensemble)? No surveyed paper directly compares at the wiki owner's intended granularity.
2. **Specialisation vs. uniformity.** Per [[modular-deep-learning]] §4.2.3, token-level routing prevents specialisation. If G3 wants both token-level routing *and* specialised blocks, a fundamentally different load-balancing objective (or no load-balancing at all) is likely needed.
3. **Router architecture.** Top-k softmax (the [[mod]] / [[btx]] / [[sparse-upcycling]] standard), confidence-threshold ([[calm]]), or hash ([[hash-routing]], queued)? The taxonomy has examples of each but no head-to-head at G3 granularity.
4. **Cold-start.** Can a pool of transformer blocks + router be trained jointly from scratch? Surveyed work universally bootstraps from a dense converged checkpoint. The closest evidence for joint-from-scratch is [[mod]], but its "pool" is degenerate (skip-vs-execute, not multiple blocks).
5. **Auxiliary-predictor inference gap.** [[mod]]'s training-time non-causal top-k requires an auxiliary predictor at inference; the gap is empirically small but not characterised at long context. G3 routers will face the same train-vs-inference distribution gap.

## Source

This is a synthesis page. Primary raw sources:

**First run:**
- `raw/research/block-training-quantization/23-layerskip.md`

**Second run:**
- `raw/research/selective-replacement-and-training/18-mod.md`
- `raw/research/selective-replacement-and-training/19-sparse-upcycling.md`
- `raw/research/selective-replacement-and-training/27-btx.md`
- `raw/research/selective-replacement-and-training/21-calm.md`
- `raw/research/selective-replacement-and-training/25-btm.md`
- `raw/research/selective-replacement-and-training/28-demix.md`
- `raw/research/selective-replacement-and-training/30-modular-deep-learning.md` (§4.2.3 caution)

## Related

- [[mod]] — primary citation; per-token top-k depth routing
- [[sparse-upcycling]] — per-token FFN-expert routing, copy-and-train bootstrap
- [[btx]] — per-token FFN-expert routing, independent-train bootstrap
- [[btm]] — coarser ensemble / weight-average routing
- [[demix]] — domain-conditional routing (deterministic, not per-token)
- [[calm]] — per-token confidence-based early exit
- [[layerskip]] — skip-as-routing training pressure
- [[sleb]] — degenerate routing (one-shot removal)
- [[modular-deep-learning]] — survey hub, source of §4.2.3 caution
- [[block-isolation-training]] — companion concept page (G1); a G3 router presupposes interchangeable / specialised blocks, which is what G1 produces
- [[hash-routing]] — queued; alternative routing primitive
