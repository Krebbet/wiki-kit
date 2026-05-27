# Block-Isolation Training

**Block-isolation training** is the training regime in which a single block (transformer block, CNN block, or arbitrary subnetwork) is updated using a local objective derived only from its own inputs and outputs (or an immediate local proxy), with limited or no end-to-end gradient signal from the global task loss. The block is treated as an independent optimisation unit; the rest of the network is frozen, replaced by a teacher signal, gradient-stopped, or masked. The wiki owner's **G1** experiment — train an isolated transformer block in such a way that swapping it back into a stack preserves generation quality — sits squarely in this regime, and the literature surveyed below provides the partial empirical and theoretical backing.

This page is a synthesis anchor: it groups the methods in this wiki that bear on the question *can a single block be trained in isolation and re-integrated cleanly?*, and it states the open transfer questions that remain when moving from prior settings (CNN representation learning, PTQ calibration, BERT compression, LLM pruning) to autoregressive transformer training-from-scratch.

## The isolation primitive — five flavours

There is no single technique called "block isolation." The literature uses several distinct mechanisms that can be grouped into five flavours, ordered roughly by how "strong" the isolation is:

1. **Output reconstruction against a frozen teacher.** A block is optimised to match the FP / teacher block's output given the same input, typically with an MSE or Fisher-weighted distortion objective. The rest of the network supplies the input distribution at the block's interface but is not differentiated through. Examples: [[brecq]] (block-wise PTQ reconstruction), [[omniquant]] (block-wise differentiable PTQ with learnable clipping / equivalent-transform), [[iterative-layer-distill]] (joint KL+MSE heal-after-removal).
2. **Module replacement with stochastic / continuous mixing.** A substitute module is inserted at the block's location during training; a gate (Bernoulli or deterministic blend) routes activations between the original and substitute, providing gradient flow for the substitute via the surrounding frozen backbone. Examples: [[bert-of-theseus]] ($z_\ell(t) \sim \text{Bernoulli}(p(t))$), [[dcr]] (deterministic blend $\alpha(t)$).
3. **Local auxiliary loss + gradient stop.** Each block has its own auxiliary head with a local objective (classification, contrastive, reconstruction); the gradient is blocked from flowing into upstream blocks. Examples: [[decoupled-greedy-learning]] (CNN, local classifier auxiliary heads, sync/async with replay buffer), [[greedy-infomax]] (CNN/audio, gradient-stopped modules with local InfoNCE), [[legonn]] (gradient-isolating BeamConv interface variant — the cleanest explicit-interface example for transformers).
4. **Independent training + post-hoc composition.** Pieces are trained in *full* isolation (separate processes, separate data, no inter-piece communication during training) and then composed at inference. The most extreme version of isolation: each piece sees no signal from any other during training. Examples: [[btm]] (independent expert LMs, ensembled or weight-averaged), [[btx]] (BTM successor — independent FFN training, then learned MoE router), [[demix]] (domain-conditional FFN experts trained per-domain), [[sparse-upcycling]] (less extreme: copy-and-train, but each MoE expert evolves independently after copy), [[lottery-ticket-bert]] (sparse-mask isolation — a subnet is trained alone with the rest pruned away).
5. **Surgery + recovery training.** A piece is removed or grown, then the rest of the network is fine-tuned to recover quality. The "isolation" is on the *changed* piece; the surrounding network adapts. Examples: [[sheared-llama]] (LLM-scale structured pruning + dynamic batch loading recovery), [[shortgpt]] (one-shot block removal by Block Influence; recovery via continued training), [[bert2bert]] (function-preserving growth + continued training), [[ligo]] (learnt linear growth operator + continued training).

A weaker "**dropout-driven isolation pressure**" variant ([[layerskip]]) does not isolate gradients at all — it trains the network so that any prefix of layers must produce useful output, indirectly forcing each block to be self-sufficient in the residual-stream sense. Insertion-only PEFT ([[lora]], [[adapters-houlsby]]) is also a form of isolation — the inserted piece is trained alone with the backbone frozen — but at adapter granularity, not block granularity.

## What's been empirically demonstrated

- **Block-by-block PTQ matches QAT** down to INT2 ([[brecq]]) and W2A16 / W4A4 ([[omniquant]]) on standard architectures. The inner loop is identical to G1's training loop except the teacher signal is FP block outputs rather than a partial-update gradient.
- **Module replacement preserves accuracy** ([[bert-of-theseus]]: ≥98% of teacher GLUE performance with 50% layer count, no auxiliary distillation loss).
- **Local-loss training converges** ([[decoupled-greedy-learning]], [[greedy-infomax]]: CNN-scale ImageNet / STL-10 / LibriSpeech results competitive with end-to-end backprop in their respective settings).
- **Independently-trained pieces can be recombined** ([[btm]] forest of 64 experts at 22.4B params matches monolithic 1.3B; [[btx]] adds a learned router and outperforms BTM; [[sparse-upcycling]] beats both dense continuation and MoE-from-scratch up to 100% of the dense pretraining compute). This is the strongest published evidence that selectively-replaced-and-trained pieces can compose.
- **Sparse subnets train alone to match the dense parent** ([[lottery-ticket-bert]]: BERT winning tickets at 40–90% sparsity match dense fine-tuning across 11 tasks; an MLM-found mask at 70% sparsity transfers universally).
- **LLM-scale prune-and-recover works** ([[sheared-llama]]: LLaMA2-7B → 1.3B / 2.7B at 3% the compute of training from scratch, end-to-end structured pruning + dynamic batch loading recovery). This is the canonical LLM-scale evidence for the surgery-and-recover flavour.
- **Function-preserving growth + train works** ([[bert2bert]]: 45–47% compute savings; [[ligo]]: 22–55% FLOPs savings vs. scratch). The reverse direction of G1 — start from a trained block and grow — is a healthy literature.
- **Heal-after-removal recovers quality** ([[iterative-layer-distill]]: 36→28 layers on Qwen2.5-3B with 9.7% quality loss, joint KL+MSE per-removal fine-tuning).
- **Skippable layers can be trained jointly** ([[layerskip]]: any prefix of layers produces useful output, no auxiliary modules needed for self-speculative decoding).
- **Explicit interface contracts enable cross-task module reuse** ([[legonn]]: a German-English MT decoder transferred to Romanian-English MT and English ASR with no fine-tuning, by grounding the encoder-decoder interface to a marginal distribution over a fixed vocabulary).

## Where the evidence is incomplete (transfer to G1)

- Most direct evidence comes from **adjacent regimes** rather than autoregressive transformer training-from-scratch. PTQ (post-training, frozen weights, calibration data), CNN representation learning (vision/audio, no next-token loss), BERT compression (encoder-only, classification objectives), and LLM pruning (one-shot surgery, then recover) all relax some of G1's constraints.
- **Module replacement** ([[bert-of-theseus]], [[dcr]]) is the most directly transformer-relevant, but in the compression regime — substitute modules are *smaller* and trained to mimic the originals, not interchangeable equals trained from scratch. [[dcr]] specifically calls out heterogeneous-operator swapping (e.g. attention → Linformer) as future work with no current empirical support.
- **Independent training + recombination** ([[btm]], [[btx]], [[demix]]) demonstrates that pieces can compose, but at the *whole-LM* or *FFN-layer* granularity, not the transformer-block granularity. The block-level analogue of BTX (swap independently-trained transformer blocks back into a backbone) is not directly demonstrated by any of the surveyed papers.
- **Heal-after-removal** ([[iterative-layer-distill]], [[sheared-llama]]) recovers quality after a removal, but the surviving blocks are fine-tuned with full backprop through the modified stack, not trained in isolation. Whether the per-block local-loss training that DGL/GIM showed for CNNs scales to transformer blocks is open.
- **Layer dropout** ([[layerskip]]) provides isolation pressure but does not produce truly swappable blocks — layers stay in fixed positions.
- **Interface contracts** ([[legonn]]) demonstrate cross-task module reuse, but the CTC-grounded marginal-distribution interface only works where alignment to a discrete vocabulary makes sense (MT, ASR). It does not transfer cleanly to autoregressive decoder-internal block boundaries.

## Cross-source themes *(synthesis)*

- The **block** boundary is the most common granularity unit (residual block in CNNs, transformer block in BERT/LLMs), but the corpus spans a wider range: adapter-level ([[lora]], [[adapters-houlsby]]), FFN-layer-level ([[btx]], [[demix]], [[sparse-upcycling]]), MHA/MLP sub-block-level ([[sleb]] / BlockPruner-style decomposition), and full-model-level ([[btm]]). The "right" granularity for G1 is one of the open questions.
- **Cross-block dependencies are the universal failure mode.** [[brecq]]'s theoretical result (block-diagonal Hessian approximation) is the cleanest explicit treatment; everyone else handles it via curriculum (Theseus, DCR), surrounding fine-tuning ([[iterative-layer-distill]], [[sheared-llama]]), strong distributional alignment ([[omniquant]]'s LET), or explicit interface contracts ([[legonn]]).
- **G2 connection.** Several papers express per-block adaptation as a learned parameter — bitwidth ([[brecq]] mixed-precision), clipping/scale ([[omniquant]]), rotation ([[spinquant]] R2), rank ([[lora]] per-layer $r$), bottleneck dimension ([[adapters-houlsby]]), expert count ([[sparse-upcycling]], [[btx]]), pruning ratio ([[sheared-llama]], [[lottery-ticket-bert]]). This is a useful precedent for the wiki owner's **G2** (dynamic per-block parameter allocation), even though most of these are static design choices rather than dynamically learned at training time.
- **Pre-training-then-isolate vs. isolate-during-pretraining.** Almost all surveyed evidence is *post-pretraining* — start from a converged model, then isolate. Only [[decoupled-greedy-learning]] and [[greedy-infomax]] train in isolation from random init (and only at CNN scale). Whether isolated block training can be the *primary* training regime, rather than a fine-tuning regime, is the deepest open question.

## Open questions for G1 transfer

1. **Local objective design.** What is the right local-loss analogue of next-token prediction at a single transformer block? Reconstruction against a teacher block's output (the [[brecq]] / [[omniquant]] route) is well-validated for PTQ but unproven for training from scratch. [[legonn]]'s marginal-distribution interface is the cleanest principled alternative for transformers but assumes a discrete-vocabulary alignment.
2. **Granularity.** Whole transformer block (Attn+MLP residual unit) vs. MHA-only / MLP-only sub-blocks (per [[sleb]] / BlockPruner-style decomposition) vs. FFN-only ([[btx]], [[demix]], [[sparse-upcycling]] all isolate at FFN granularity). No surveyed paper has direct evidence for the right unit when training from scratch.
3. **Interface drift during training.** Theseus/DCR keep neighbouring layers frozen; what happens when *all* blocks train in isolation simultaneously and their interface distributions co-evolve? No prior work directly addresses this.
4. **From-scratch vs. fine-tune-only.** All transformer-scale evidence (Theseus, DCR, BTM/BTX, Sparse Upcycling, Sheared LLaMA, Iterative-Layer-Distill) starts from a strong pretrained checkpoint. CNN-scale evidence ([[decoupled-greedy-learning]], [[greedy-infomax]]) supports from-scratch isolated training but at much smaller scale. Whether isolated block training can replace end-to-end pretraining is unmapped above ~100M params.
5. **Pool of interchangeable blocks.** G1 implies a pool from which any block can occupy any position. None of the surveyed work actually constructs such a pool — Theseus / DCR train one substitute per slot, BTX experts are tied to a layer position, DEMix experts are tied to a domain. The pool design is open territory.
6. **Heal-after-removal vs. heal-after-replacement.** [[iterative-layer-distill]] / [[sheared-llama]] heal after removing a piece. The G1 analogue heals after *replacing* a piece with a freshly-trained one of the same shape but different weights. The dynamics may differ — replacement preserves the residual-stream dimension a removal collapses.

## Reading order — entering this literature for G1

If you are coming to the corpus cold and want to replace-and-train a single transformer block, read in this order. Tiered by directness of evidence and block-granularity match. Later tiers add breadth at diminishing direct relevance.

1. **Tier 1 — direct G1 evidence at transformer scale.** This page (orientation), then [[bert-of-theseus]] (closest direct analogue, Bernoulli-gated replacement at BERT layer scale), then [[sheared-llama]] (LLM-scale prune-and-recover, canonical evidence), then [[iterative-layer-distill]] (heal-after-removal recipe, joint KL+MSE distillation per removal).
2. **Tier 2 — theory + differentiable optimisation, PTQ-derived but principle transfers.** [[brecq]] for the cleanest theoretical treatment (block-by-block reconstruction, block-diagonal Hessian); [[omniquant]] for the differentiable / SGD-trained block-wise optimisation machinery.
3. **Tier 3 — on-target but caveat-laden.** [[dcr]] (Theseus successor; deterministic blend; **read with workshop / single-seed / no-code / no-heterogeneous-op caveats**); [[shortgpt]] (block-importance scoring; **read with the [[conflicts/shortgpt-vs-sleb-redundancy-metric]] tension in mind**).
4. **Tier 4 — interface design + foundational principles.** [[legonn]] (explicit interface contracts via marginal distributions; gradient-isolating variant); [[decoupled-greedy-learning]] + [[greedy-infomax]] (CNN-scale existence proofs that local-loss isolated training converges).
5. **Tier 5 — lateral context, as needed.** [[bert2bert]] / [[ligo]] (opposite direction: growth + train); [[modular-deep-learning]] (taxonomy search index).

**Skip for the strict G1 reading**: MoE / expert pools ([[btm]], [[btx]], [[sparse-upcycling]], [[demix]] — G3 territory or FFN-only granularity); PEFT ([[lora]], [[adapters-houlsby]] — adapter granularity, not block); routing ([[mod]], [[calm]], [[layerskip]] — G3); training-free pruning ([[sleb]] — no recovery); sparse subnets ([[lottery-ticket-bert]] — different primitive); quantization papers as quant ([[gptq]], [[awq]], [[spinquant]] — orthogonal axis; [[brecq]] / [[omniquant]] are the exceptions because their inner loop matches G1).

## Source

This is a synthesis page. Primary raw sources (across both ingest runs):

**First run — block-training-quantization:**
- `raw/research/block-training-quantization/21-brecq.md`
- `raw/research/block-training-quantization/14-bert-of-theseus.md`
- `raw/research/block-training-quantization/15-dcr.md`
- `raw/research/block-training-quantization/24-dgl.md`
- `raw/research/block-training-quantization/13-gim.md`
- `raw/research/block-training-quantization/18-omniquant.md`
- `raw/research/block-training-quantization/23-layerskip.md`
- `raw/research/block-training-quantization/20-iterative-layer-distill.md`

**Second run — selective-replacement-and-training:**
- `raw/research/selective-replacement-and-training/23-sheared-llama.md`
- `raw/research/selective-replacement-and-training/24-shortgpt.md`
- `raw/research/selective-replacement-and-training/22-lottery-ticket-bert.md`
- `raw/research/selective-replacement-and-training/16-bert2bert.md`
- `raw/research/selective-replacement-and-training/20-ligo.md`
- `raw/research/selective-replacement-and-training/25-btm.md`
- `raw/research/selective-replacement-and-training/27-btx.md`
- `raw/research/selective-replacement-and-training/28-demix.md`
- `raw/research/selective-replacement-and-training/19-sparse-upcycling.md`
- `raw/research/selective-replacement-and-training/29-legonn.md`
- `raw/research/selective-replacement-and-training/17-lora.md`
- `raw/research/selective-replacement-and-training/26-adapters-houlsby.md`
- `raw/research/selective-replacement-and-training/30-modular-deep-learning.md`

## Related

- [[brecq]] — block-by-block reconstruction PTQ
- [[omniquant]] — block-wise differentiable PTQ
- [[bert-of-theseus]] — Bernoulli-gated module replacement
- [[dcr]] — deterministic-blend module replacement (Theseus successor)
- [[decoupled-greedy-learning]] — local-loss + gradient-isolated CNN training
- [[greedy-infomax]] — gradient-isolated representation learning
- [[legonn]] — explicit interface-contract modular composition
- [[btm]] — independent expert LM training + recombination
- [[btx]] — BTM successor with learned MoE router
- [[demix]] — domain-conditional FFN expert pool
- [[sparse-upcycling]] — copy-and-train MoE bootstrap
- [[lottery-ticket-bert]] — sparse-subnet isolation
- [[sheared-llama]] — canonical LLM-scale structured prune + recovery
- [[shortgpt]] — block-importance scoring (one-shot removal)
- [[iterative-layer-distill]] — heal-after-removal training
- [[layerskip]] — layer-dropout-induced prefix-isolation pressure
- [[bert2bert]] — function-preserving growth + train
- [[ligo]] — learnt linear growth operator + train
- [[lora]] — adapter-granularity insertion + train (frozen backbone)
- [[adapters-houlsby]] — sequential bottleneck adapter (LoRA predecessor)
- [[modular-deep-learning]] — survey hub; this page maps onto its training-setting axis
- [[token-conditional-routing]] — companion concept page (G3)
- [[conflicts/shortgpt-vs-sleb-redundancy-metric]] — bears on which blocks are best swap candidates
