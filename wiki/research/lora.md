# LoRA: Low-Rank Adaptation of Large Language Models

Freeze the pretrained backbone and inject trainable rank-$r$ matrices $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$ in parallel with each target weight. This achieves parity with full fine-tuning at roughly 0.01% of the parameter count and zero inference latency overhead (post-merge), making it the canonical parameter-efficient fine-tuning (PEFT) primitive. On GPT-3 175B the checkpoint shrinks from 350 GB to 35 MB; VRAM during training drops from 1.2 TB to 350 GB; throughput rises +25%.

## Method core

For a frozen pretrained weight $W_0 \in \mathbb{R}^{d \times k}$, the adapted forward pass is:

$$h = W_0 x + \Delta W x = W_0 x + BAx$$

$A$ is initialized with random Gaussian; $B$ with zeros, so $\Delta W = BA = 0$ at init. The update is scaled by $\frac{\alpha}{r}$ where $\alpha$ is a fixed constant set to the first $r$ tried and not re-tuned — this makes $\alpha$ behave as a learning-rate rescaler so only $r$ needs sweeping.

**Rank:** empirically $r = 1$ or $r = 4$ suffices for most NLP tasks. Grassmann-distance subspace analysis shows top singular directions of $A_{r=8}$ and $A_{r=64}$ strongly overlap, confirming the adaptation is intrinsically low-rank.

**Which layers:** attention weights only ($W_q, W_v$ in most experiments; all four of $W_q, W_k, W_v, W_o$ also explored). MLP layers, LayerNorm, and biases remain frozen. Ablation at fixed 18M-parameter budget (GPT-3 175B, Table 5) shows $\{W_q, W_v\}$ at $r=4$ is the best single choice.

**Merge at inference:** since $W_0$ and $BA$ share shape, sum them before deployment — $W \leftarrow W_0 + BA$ — for zero added latency. Task switching: subtract current $BA$, add new $B'A'$. Unmerged, this reintroduces latency when batching heterogeneous tasks (see failure modes).

**$\Delta W$ vs. $W_0$ geometry (Section 7.3):** $\Delta W$ is *not* aligned with the top singular directions of $W_0$; it amplifies directions not emphasized in pretraining, with amplification $\approx 21.5\times$ at $r=4$ (drops to $\approx 0.6\times$ at $r=64$, suggesting high rank dilutes signal). This supports a reading of LoRA as surfacing latent task-specific features suppressed during pretraining.

## Goal relevance

**G1 (block isolation / swappability):** Partial. LoRA's frozen-backbone + trainable-delta structure is "insert and train only the inserted piece," but granularity is per-weight-matrix, not per-transformer-block — the delta merges back into the same weight rather than standing as a replacement block. The task-switching story (swap $BA$ adapters at inference) is a lightweight analogue to swappable blocks and is a useful comparison point, but LoRA does not demonstrate composability or generation-quality preservation under heterogeneous block swaps in the G1 sense.

**G2 (dynamic per-block parameter budget):** Rank $r$ is a per-layer budget knob, but the paper sets it uniformly. The ablation across weight types ($W_q$ vs. $W_v$, Tables 5–6) provides empirical motivation for per-layer allocation; [[adalora]] (queued) operationalises this via SVD-based importance scoring.

**G3 (token-conditional routing):** Not relevant. LoRA adapts all tokens uniformly.

## Credibility

| Dimension | Assessment |
|---|---|
| Venue / year | ICLR 2022 (published; Version 2) |
| Code | Released — `github.com/microsoft/LoRA`; PyTorch; RoBERTa, DeBERTa, GPT-2 implementations |
| Weights | Released — RoBERTa, DeBERTa, GPT-2 checkpoints alongside code |
| Ablation rigor | Strong — Tables 5–6 sweep weight-type and rank on GPT-3 175B at fixed budget; Figures 3–4 provide geometric subspace analysis; multiple seeds reported |
| Replication status | Extremely high — integrated into HuggingFace PEFT; one of the most widely reproduced PEFT methods |

## Empirical claims

1. **GPT-3 175B (Table 4):** LoRA at 4.7M params matches or exceeds full fine-tuning on WikiSQL (73.4 vs. 73.8), MultiNLI-m (91.7 vs. 89.5), and SAMSum R1/R2/RL (53.8/29.8/45.9 vs. 52.0/28.0/44.5). AdapterH at 40.1M params underperforms LoRA at 4.7M on two of three tasks.
2. **RoBERTa-base GLUE (Table 2):** LoRA (0.3M) avg 87.2 vs. full fine-tune (125M) avg 86.4; beats AdapterD at same 0.3M (avg 84.4).
3. **GPT-2 Medium E2E NLG (Table 3):** LoRA (0.35M) BLEU 70.4 vs. FT (354.9M) BLEU 68.2 and AdapterL (11.09M) BLEU 68.9.
4. **Rank sufficiency (Table 6):** $r=1$ on $\{W_q, W_v\}$ GPT-3 175B achieves WikiSQL 73.4%, within noise of $r=64$. Adapting all four attention heads at $r=2$ matches $\{W_q, W_v\}$ at $r=4$.
5. **Inference latency (Table 1):** Sequential adapters introduce +2–30% latency on GPT-2 medium (worst case batch=1, seq=128: +30.3%); LoRA merged matches fine-tuning baseline exactly.

## Open questions / failure modes

- **Batching heterogeneous tasks:** Cannot batch inputs requiring different $BA$ adapters in a single forward pass if weights are merged — must keep them unmerged and route dynamically, reintroducing latency.
- **Which layers to adapt:** Freezing MLP layers and LayerNorm is a heuristic; optimal selection for other architectures or training-from-scratch scenarios is unstudied.
- **Rank selection is manual:** No principled per-layer $r$ assignment; the paper flags this as future work. [[adalora]] addresses it.
- **Pretraining dependency:** All experiments start from a pretrained checkpoint. Whether low-rank deltas suffice for training from scratch (G1 scenario) is open — the low-intrinsic-rank hypothesis may not hold without pretraining.
- **Amplification degrades at high rank:** $\Delta W$ amplification drops from $21.5\times$ at $r=4$ to $\approx 0.6\times$ at $r=64$; unnecessarily high rank appears to dilute the task-specific signal with noise.

## Source

- `raw/research/selective-replacement-and-training/17-lora.md` (PDF capture)
- `raw/research/selective-replacement-and-training/01-lora-abs.md` (arXiv abstract)

## Related

- [[adapters-houlsby]] — direct predecessor (sequential bottleneck adapters; LoRA is parallel low-rank with zero inference overhead vs. +30% for adapters)
- [[bert-of-theseus]] — insertion-vs-replacement contrast; also freezes original weights while training inserted parameters, but targets block replacement rather than task adaptation
- [[block-isolation-training]] — concept anchor; LoRA's "train only the inserted piece" is a per-weight analogue of block isolation, weaker in granularity
- [[modular-deep-learning]] — survey context (LoRA is canonical PEFT module)
- [[adalora]] — G2-relevant follow-on: dynamic per-layer rank allocation via SVD importance scoring (queued)
