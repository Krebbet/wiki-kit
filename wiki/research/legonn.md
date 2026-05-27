# LegoNN: Building Modular Encoder-Decoder Models

LegoNN (Dalmia et al., arXiv 2206.03318; CMU / Meta AI FAIR) is a framework for training encoder-decoder models (MT, ASR) whose components are swappable across tasks without fine-tuning. The central mechanism is an explicit interface contract: the encoder output is grounded to a sequence of marginal distributions $\mathbb{P}^{\mathcal{V}_\text{CTC}}_{1:T}$ over a fixed discrete vocabulary via a CTC loss, producing conditionally independent, input-only per-step distributions. Any encoder trained under this constraint can be paired with any decoder trained to consume it. Two decoder-side *ingestor* variants bridge the interface: **WEmb** (differentiable, full-distribution) and **BeamConv** (gradient-isolating, discrete top-$p$). A modality-agnostic Output Length Controller (OLC) handles fractional sequence-length resampling when pairing modules trained on tasks with incompatible input/output length ratios (e.g., speech frames ↔ BPE tokens).

---

## Method core

### Interface contract

Standard encoder-decoder cross-attention couples the decoder to opaque encoder hidden states $\mathbf{h}^E_{1:T}$. LegoNN replaces this with:

$$\mathbb{P}^{\mathcal{V}_\text{CTC}}_{1:T} = \text{softmax}(\text{encoder}(X_{1:T}) \cdot W_o)$$

supervised by a CTC loss. The joint training objective is:

$$\mathcal{F}_\text{obj} = \mathcal{F}_\text{CE}(L^{\mathcal{V}_\text{Attn}}, \mathbb{P}^{\mathcal{V}_\text{Attn}}) + \mathcal{F}_\text{CTC}(L^{\mathcal{V}_\text{CTC}}, \mathbb{P}^{\mathcal{V}_\text{CTC}})$$

**The CTC loss is necessary, not cosmetic.** Removing it while retaining the architecture collapses cross-task swap performance to 0.0 BLEU (Table VIII ablation). CTC marginalization forces each per-step output to be independent of output labels and conditioned only on input — this is what makes the representation portable.

For chains of $M$ modules (e.g., phoneme recogniser → pronunciation model → language decoder), the objective generalises to:

$$\mathcal{F}_\text{obj} = \mathcal{F}_\text{CE}(L^{\mathcal{V}_\text{Attn}^{(M)}}, \mathbb{P}^{\mathcal{V}_\text{Attn}^{(M)}}) + \sum_{i=1}^{M-1} \mathcal{F}_\text{CTC}(L^{\mathcal{V}_\text{CTC}^{(i)}}, \mathbb{P}^{\mathcal{V}_\text{CTC}^{(i)}})$$

### WEmb ingestor (differentiable variant)

Computes the expected embedding of the interface distribution:

$$\mathbf{h}_{1:K} = \mathbb{P}^{\mathcal{V}_\text{CTC}}_{1:K} \cdot W_\text{Emb}; \quad \mathbf{h}_{1:K} = \mathbf{h}_{1:K} + \text{PE}(\mathbf{h}_{1:K})$$

followed by transformer encoder blocks. Receptive field $\text{RF}=1$ by default; $\text{RF}>1$ allows learning local confusion patterns. Gradients flow through $W_\text{Emb}$ back into the encoder. More robust for cross-task / cross-domain reuse because the full marginal is preserved; supports end-to-end fine-tuning.

### BeamConv ingestor (gradient-isolating variant)

Embeds only the token indices of the top-$p$ hypotheses per position:

$$\mathbf{r}_{1:K} = \text{Embedding}(\text{top-p}(\mathbb{P}^{\mathcal{V}_\text{CTC}}_{1:K}))$$

followed by Conv1D, positional embedding, and transformer encoder blocks. The argmax/top-$p$ selection is non-differentiable: **no gradients propagate across the module boundary**. The encoder trains exclusively on its CTC loss; the decoder trains exclusively on its CE loss. This is the cleanest "explicit interface contract for modular composition" precedent in the literature — a hard information bottleneck enforced by discrete token identity rather than floating-point values. More robust within the same task/domain; less robust cross-domain (top-$p$ confusion sets shift). Beam size $p$ is fixed at decoder training time and cannot change at inference, which is a practical constraint.

### Output Length Controller (OLC)

Cross-attention between $K$ learned positional queries $\mathbf{h}^{\text{PE}}_{1:K}$ and encoder representations $X_{1:T}$, producing exactly $K$ output representations via fractional resampling. Required when pairing modules trained for tasks with mismatched input/output length ratios (speech ↔ text); unnecessary for same-domain same-task reuse.

### Vocabulary design

Practical recommendation: $\sim$4k units balances CTC conditional independence against sequence length. Vocabulary must be shared or compatible across all tasks sharing a module — phonemes suffice for speech-only reuse; BPE sub-words are required for cross-modal MT↔ASR reuse.

---

## Goal relevance

**Strong relevance to G1** (training isolated transformer blocks that remain swappable while preserving generation quality).

LegoNN is the most fully specified "train with an explicit interface contract, then swap across tasks" instantiation in the encoder-decoder literature. Three aspects transfer directly to G1:

1. **Interface contract as a first-class design primitive.** The CTC-grounded marginal-distribution interface is a concrete proposal for what a block interface could mean: each module's output carries a consistent semantic meaning independent of training context. G1 needs the same — some enforced representation contract at block boundaries.

2. **BeamConv as the canonical gradient-isolation precedent.** BeamConv creates a hard gradient barrier between encoder and decoder. This is **the cleanest explicit-interface-contract example for modular composition in the literature**, directly relevant to G1's isolation requirement. The encoder and decoder are fully decoupled at training time; the interface vocabulary is the only shared artifact. See also [[greedy-infomax]] for the isolation lineage and [[block-isolation-training]] for the conceptual anchor.

3. **Key ablation is the strongest empirical argument for interface losses.** Table VIII: without CTC, module swap → 0.0 BLEU. G1 block-isolation designs must account for this — interface enforcement appears necessary, not optional.

**Scope limitation.** LegoNN operates at encoder/decoder granularity (12–16 transformer blocks per module), not at individual transformer layer granularity. Transferring the CTC-based interface to finer-grained block isolation within an autoregressive decoder is non-trivial: CTC requires a monotonic sequence-to-sequence alignment structure that doesn't directly apply to individual decoder layers. An alternative intermediate representation contract is needed for G1's setting.

---

## Credibility

arXiv preprint (2206.03318, 2022), IEEE-style full journal format. No confirmed peer-reviewed publication venue identified in source materials. CMU / Meta AI FAIR authorship is credible; methodology is detailed and ablated. Treat as preprint quality until confirmed published. Results averaged over 3 seeds.

---

## Empirical claims

- **Performance near-parity:** WEmb LegoNN on WMT En-De: 27.5 BLEU vs. 28.3 monolithic baseline (−0.8). Switchboard 300h ASR: matches baseline at 8.4% / 18.2% WER (SWB/CH).
- **Modularity stress test:** Random-seed swap and architecture swap between LegoNN modules yields near-zero degradation for both WEmb and BeamConv. Monolithic encoder-decoder fails completely under all swap conditions.
- **Cross-task zero-shot reuse:** Ro-En encoder + De-En decoder: WEmb 35.0 BLEU vs. 34.0 baseline (+1.0). Europarl ASR encoder + De-En MT decoder: 18.4% WER (ties baseline).
- **Three-module ASR** (Europarl + TED-LIUM + WMT De-En): 19.0% WER zero-shot; 14.8% after fine-tuning (19.5% relative reduction vs. 18.4% baseline).
- **Fine-tuning:** WEmb end-to-end fine-tuning (few thousand steps): 35.5 BLEU Ro-En; 16.1% WER Europarl two-module; 14.8% three-module.
- **Low-resource transfer:** Decoder from full 300h SWB reused with 10%-data encoder: >50% relative WER improvement over a 10%-data baseline.

---

## Open questions / failure modes

- **Venue unconfirmed.** arXiv preprint only — weight results accordingly.
- **Domain mismatch.** Encoder-decoder MT/ASR, not autoregressive decoder-only transformers. Generalisability to LLM-style training from scratch is unconfirmed.
- **CTC dependency.** Interface design assumes CTC-compatible monotonic sequence-to-sequence alignment. Not directly applicable to cross-attention decoders without architectural modification; inapplicable to individual decoder layers without a new interface formulation.
- **BeamConv beam size fixity.** Beam size $p$ is fixed at decoder training time. Any G1 application where the interface specification evolves during training cannot use BeamConv without retraining the decoder.
- **OLC overhead.** Output Length Controller adds parameters and compute; not isolated from other LegoNN overhead in published tables.
- **Vocabulary bottleneck.** ~4k unit vocabulary may discard information useful for fine-grained tasks. Optimal vocabulary size is task/domain-dependent and untested outside MT/ASR.

---

## Source

- `raw/research/selective-replacement-and-training/29-legonn.md` (PDF capture, arXiv 2206.03318, captured 2026-04-30)
- `raw/research/selective-replacement-and-training/10-legonn-abs.md` (arXiv abstract)

---

## Related

- [[bert-of-theseus]] — module-replacement at full transformer scale; Bernoulli gate rather than explicit interface distribution
- [[dcr]] — module-replacement with continuous gate; related swap-training lineage
- [[greedy-infomax]] — gradient-isolated CNN/audio module stack (NeurIPS 2019); conceptual ancestor of BeamConv's isolation property
- [[block-isolation-training]] — concept anchor for G1; LegoNN's BeamConv ingestor is a 4th flavour of isolation primitive alongside layer-wise, contrastive, and distillation-based approaches
- [[modular-deep-learning]] — survey context; LegoNN is a canonical modular composition example
