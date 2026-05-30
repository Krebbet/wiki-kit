# Gated DeltaNet-2

NVIDIA (arXiv:2605.22791, 2026-05-22) proposes Gated DeltaNet-2, which replaces the single tied scalar gate β_t in delta-rule linear attention with two independent channel-wise gates — a key-axis erase gate b_t ∈ [0,1]^{d_k} and a value-axis write gate w_t ∈ [0,1]^{d_v} — and achieves the strongest aggregate results at 1.3B/100B scale over Mamba-2, Gated DeltaNet, KDA, and Mamba-3 (SISO and MIMO) across language modeling, commonsense reasoning, and multi-key needle-in-a-haystack retrieval.

## Method

Builds on the delta-rule fast-weight update family: DeltaNet → Gated DeltaNet (scalar decay α_t) → KDA (channel-wise decay over key dimension) → GDN-2. The shared bottleneck in all predecessors: scalar β_t jointly governs how much old content is erased from the state and how much new value is written, coupling two logically distinct operations.

**Gated Delta Rule-2 state update (Eq. 10):**

    S_t = (I − k_t(b_t ⊙ k_t)^T) D_t S_{t-1} + k_t(w_t ⊙ v_t)^T

- b_t: channel-wise erase gate (key-axis), controls how aggressively each key channel overwrites old associations
- w_t: channel-wise write gate (value-axis), controls commitment of new value content per channel

Special cases: set b_t = w_t = β_t·1 to recover KDA; further restrict to scalar decay to recover Gated DeltaNet.

**Implementation.** Channel-wise decay is absorbed into asymmetric rank-one erase factors via a decay-normalized recurrence, preserving the chunkwise WY algorithm structure from KDA. The gate-aware backward pass (Eqs. 64–65) is new — scalar post-scaling shortcuts valid in KDA break under asymmetric gates. Triton kernels, chunk size C=64, fp32 decay precision. Correctness verified via fp64 autograd in Appendix D.6.

**Hybrid variant.** Gated DeltaNet-2 token mixer + MLP + SWA (2K window) + MLP, interleaved.

## Results

All comparisons at 1.3B parameters, 100B FineWeb-Edu tokens, matched recurrent state size (262,144 floats/layer).

**Language modeling + commonsense (Table 2, aggregate avg):**
- Recurrent: GDN-2 **53.11** vs KDA 52.28, Mamba-3 MIMO 52.39, Gated DeltaNet 52.07; WikiText PPL 15.90 (best)
- Hybrid: GDN-2 **53.97** vs Mamba-3 SISO 52.69, Mamba-3 MIMO 52.72, KDA 52.68

**RULER needle-in-a-haystack (Table 3):**
- Recurrent MK-NIAH-1 @4K: GDN-2 **37.8** vs KDA 28.0, Gated DeltaNet 27.8, Mamba-3 MIMO 18.0
- Recurrent S-NIAH-2 @8K: GDN-2 **39.2** vs KDA 30.6, Gated DeltaNet 32.0
- Hybrid S-NIAH-3 @4K: GDN-2 **55.6** vs Mamba-3 MIMO 54.2, KDA 51.6
- Hybrid MK-NIAH-1 @4K: GDN-2 **48.0** vs Mamba-3 MIMO 46.6, Gated DeltaNet 44.8

**Real-world retrieval (Table 4):** Best average recurrent (29.88) and hybrid (42.28).

**Ablation (Table 5):** Key-axis erase gate b_t carries most of the gain. Scalarizing w_t only: avg 52.79 (−0.32); scalarizing b_t only: avg 52.45 (−0.66). Both are needed for full 53.11.

**Throughput (Fig. 2, H100):** Hybrid 1.3B holds near-flat 38.0 → 36.1 Kt/s over 2K→16K sequence length; Transformer degrades sharply. Small constant overhead vs KDA from the added gate projections.

## Applicability

Drop-in replacement for KDA or Gated DeltaNet blocks — same chunkwise WY structure, low adaptation cost for teams already using NVlabs GDN kernels. H100-class hardware preferred for Triton kernel compatibility. Strongest leverage on multi-key retrieval under fixed-state memory (agentic/RAG pipelines where recurrent decoding throughput matters). Not yet tested beyond 1.3B/100B; no released weights.

## Novelty

Refinement within the delta-rule family, not a new paradigm. Prior work (KDA) already made decay channel-wise on the key axis; GDN-2 extends channel-wise control to the write (value) axis and derives the asymmetric erase-vs-write decomposition with a corrected backward pass. The ablation is the cleanest contribution: it isolates which axis of decoupling drives long-context retrieval gains and attributes the failure of prior recurrent models to update-rule coupling rather than fixed-state capacity.

## Reproducibility

Code: https://github.com/NVlabs/GatedDeltaNet-2. No paperswithcode entry or released weights as of capture (2026-05-25).

## Adoption

Very recent (2026-05-22). Authors include Jan Kautz and Yejin Choi (NVIDIA). Builds on NVlabs GatedDeltaNet codebase; lower adoption friction for that ecosystem. Directly benchmarks against and beats Mamba-3 (ICLR 2026), positioning GDN-2 as current SOTA on the recurrent-delta-rule frontier.

## Source

- `raw/research/weekly-2026-05-25/01-gated-deltanet-2.md` (arXiv:2605.22791)

## Related

- [[mamba-3]] — beaten as recurrent SSM SOTA at matched 1.3B/100B scale on every aggregate metric
- [[delta-mem]] — parallel trajectory in the delta-rule / fast-weight family; δ-mem adds a delta-rule state atop frozen attention, GDN-2 trains delta-rule from scratch
- [[nested-learning]] — associative-memory / delta-rule framing; GDN-2's gains reinforce that the update-rule axis is the load-bearing variable
- [[tidar]] — same lab (NVIDIA); shares hybrid recurrent + local-attention architectural pattern
- [[conflicts/fixed-state-ssm-long-context]] — GDN-2 ablation implicates update-rule specificity (not fixed-state capacity) as the bottleneck for long-context retrieval
- [[conflicts/ssm-vs-associative-memory-taxonomy]] — GDN-2's superiority over Mamba-3 reinforces that the delta-rule update axis is load-bearing in the delta-rule vs SSM design debate
