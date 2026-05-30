# Block Operations and Modular Routing

Dietz & Klakow (Saarland, arXiv 2408.00508) propose "block-operations" — splitting activation tensors into uniform blocks and enforcing Modular Representation-Preserving Mappings (MRPMs) — as a drop-in replacement for the FNN sub-block inside transformer-style architectures. Their SMFR module (Stack of Multiplexers and FNNs with gated Residuals) achieves perfect compositional generalization on several synthetic algorithmic tasks where both standard FNNs and Transformers fail outright. The work is motivated by the Symbol Binding Problem and superposition catastrophe, framing blocks as discrete "placeholder variables" analogous to cognitive object slots.

## Mechanism: MRPMs, Multiplexer, and SMFR

**Block-operations** partitions the activation tensor into M uniform blocks; all operations must be Modular Representation-Preserving Mappings — i.e., they route or transform individual blocks without mixing representations across block boundaries in ways that destroy binding.

**MFNNR unit** (the atomic building block): combines two sub-components per block position:
- *Multiplexer* — content-driven soft routing. All M input blocks are concatenated and fed to an internal FNN, producing an M×N softmax weight matrix. Each output block is thus a weighted combination of input blocks, fully learned with no hand-coded wiring.
- *FNNR* — per-block gated residual: can pass the block unchanged, generate a new activation via FNN, or interpolate both, decided dynamically per-block from all inputs.

**SMFR** stacks multiple MFNNR units sequentially (depth swept 0–10). Weights are **not shared across stack positions** — this is depth-scaling, not weight tying. SMFR replaces the feedforward sub-block entirely; it is not interleaved with attention. Extending block-operations to full transformer architectures (including attention sub-blocks) is proposed as future work.

## Routing: Soft vs. Hard

Routing is soft (softmax) by default. An ablation uses Straight-Through Gumbel-Softmax (hard, discrete).

Key finding: **hard routing consistently underperformed soft routing** but still outperformed FNNs on every compositional task. This confirms that routing per se — not commutativity bias alone — drives the generalization gains. Soft routing is strictly preferred; hard routing is unstable to train and loses gradient information.

Specialization was verified empirically: on double-addition, 75% of depth-1 width≥8 trials reached 100% OOD accuracy, with Multiplexer softmax weights correctly zeroing irrelevant inputs. On BPMNIST, well-converged SMFRs learned to undo permutations in the first MFNNR layer, achieving permutation-invariant representations.

## Compositional Generalization Results

| Task | SMFR | FNN | Transformer |
|---|---|---|---|
| Addition/multiplication (modular, synthetic) | Best or near-best | Fails OOD | Fails OOD |
| Double-addition (biased OOD split) | 100% OOD (75% of trials) | Fails | Fails |
| ALGO (5-var conditional, 2-iter train → 1–9 iter OOD) | 100% all iter counts (depth 1–5) | 0.187 OODodd | 0.099 OODodd |
| BPMNIST (block-permuted MNIST) | 0.945 @ 25k steps → surpasses all @ 250k | 0.949 @ 25k | 0.975 @ 25k |

On ALGO, OOD iteration-count generalization (train on 2, test on 1 and 3–9) is achieved through learning the correct atomic rule — not through iterative refinement with shared weights. Transformers perform *worse than FNNs* on OODodd (0.099 vs. 0.187), consistent with pairwise Key/Query attention being poorly suited to tasks requiring joint multi-variable comparisons.

## Negative Results and Failure Modes

- **BPMNIST convergence lag**: SMFR is slower to converge than FNN and Transformer at 25k steps (0.945 vs. 0.975). It only surpasses both at 250k steps. This is a real cost, not just noise.
- **Depth degradation on ALGO**: stacks deeper than 5 degrade performance; hypothesized to push the model toward FNN-style statistical learning by making routing complex.
- **Scaling mismatch**: at high model sizes, pure FNNs marginally exceeded SMFR in some addition/multiplication conditions, attributed to suboptimal depth-stacking vs. widening internal FNNs.
- **Noisy input failure**: learning to rearrange unstructured/noisy inputs into block format succeeded in only 1 of 30 noisy-ALGO trials — not reliable.
- **Gradient stability**: softmax/sigmoid weights can grow to extreme values that zero gradients; requires a custom MSE regularization loss clamped at threshold 20.

## Cognitive and Neuroscientific Motivation

The framing is explicitly grounded in the Symbol Binding Problem (Greff et al. 2020) and the superposition catastrophe (Von der Malsburg 1986). The three binding sub-problems — representation, segregation, composition — map directly onto the block-operations design: blocks are discrete representation containers (segregation), MRPMs preserve block identity across transformations (representation), and the Multiplexer implements learned compositional reassembly. This framing is **inspiration only**; no direct neuroscience transfer claims are made.

## Scale and Evidence Base

**Scale limitation — synthetic only.** All experiments use models from ~13k to 500k parameters. The four tasks are all synthetic: modular arithmetic, double-addition with biased splits, a 5-variable conditional-assignment algorithm (ALGO), and block-permuted MNIST (BPMNIST). No large-scale language modeling, standard NLP benchmarks, or pretrained model adaptation is reported. Compute is unspecified beyond step counts (up to 250k for BPMNIST). Results must be treated as proof-of-concept at small scale; generalization to language-scale training is entirely untested.

## Open Questions

Flagged explicitly by the authors:

1. **Convergence speed**: SMFR needs to reach optimal routing faster; SMFRbias (pre-initializing routing to identity) is a proof-of-concept fix, not a solution.
2. **Unstructured input alignment**: reliable learning to rearrange noisy inputs into block format remains unsolved.
3. **Architecture scaling**: depth+width scaling does not behave like FNN scaling; an analogue to residual connections is needed to stabilize deep SMFRs.
4. **Full transformer integration**: replacing all FNN sub-blocks and adding MRPMs to attention projections — the natural next step — is unrealized.
5. **Internal FNN width**: separating routing overhead from capacity effects requires sweeping internal FNN width independently of stack depth.
6. **Compatibility with object-representation architectures**: Capsule Networks, Slot Attention, and TIMs (Transformer with Independent Mechanisms) are natural integration targets.

## Source

- `raw/research/thesis-foundations/03-block-operations.md` — Dietz & Klakow, "Block-Operations: Using Modular Routing to Improve Compositional Generalization," Saarland University, arXiv:2408.00508 (2024).

## Related

- [[mixture-of-cognitive-reasoners-micro]] — Both motivate via binding problem (Symbol Binding / brain networks) and converge on per-block routing from different theoretical starts.
- [[modular-deep-learning-survey]] — SMFR Multiplexer instances the survey's soft-routing category; paper's soft>hard finding aligns with survey's hard-routing instability analysis.
- [[routing-mechanisms-in-modular-networks]] — feeds the routing aux page.
- [[brain-inspired-modularity]] — Symbol Binding / superposition-catastrophe framing is one of the aux page's two anchors (other is MICRO).
