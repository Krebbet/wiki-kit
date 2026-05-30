# Routing Mechanisms in Modular Networks

This page taxonomizes the routing mechanisms used across five sources in the wiki's foundation corpus, anchored by the modular-deep-learning survey's four-axis framework (computation function, routing function, aggregation function, training setting). For each mechanism, three lint-required axes are applied: (1) soft vs. hard routing, (2) dispatch signal, (3) specialization origin. Patterns of convergence and divergence across sources are drawn out in the cross-cutting section below.

## Taxonomy axes

Per the wiki's lint requirements, every routing mechanism is characterized along three axes:

1. **Soft vs hard** — continuous gating (soft) vs. discrete, mutually exclusive dispatch (hard).
2. **Dispatch signal** — what input determines routing: token content, position, layer index, task label, domain metadata, etc.
3. **Specialization origin** — emergent from training dynamics, or enforced by construction (fixed routing, curriculum, pseudo-labels).

## Concrete mechanisms

| Source | Mechanism | Soft vs hard | Dispatch signal | Specialization origin |
|--------|-----------|-------------|-----------------|----------------------|
| **01 — Expert Choice Routing** | Top-k inverted MoE: experts select tokens (not vice versa) via softmax over a learned projection W_g. Gating matrix G holds continuous weights; expert output is weighted-summed. | **Soft** — continuous gating weights on selected tokens. | Token hidden state (learned linear projection to per-expert scores). | **Emergent** — W_g trained end-to-end, no auxiliary loss. Specialization inferred from downstream perf gap over hash-layer routing; no mechanistic analysis provided. |
| **02 — Mixture of Depths** | Per-layer top-k token selection: each token projects to a scalar router weight; top-k within a sequence engage the block; remainder take the residual (identity) path. Expert-choice framing. | **Hard** — top-k produces two mutually exclusive token sets (block vs. pass-through). | Token embedding (learned linear scalar projection per layer). | **Emergent** — router trained end-to-end. Stochastic control confirms learning is essential; routing analysis shows harder (higher-entropy) predictions correlate with more block engagement. |
| **03 — Block-Operations / SMFR Multiplexer** | Concatenation of all M input blocks fed to an FNN that outputs an M×N softmax weight matrix; content-driven soft routing among uniformly sized activation blocks. Ablation: Straight-Through Gumbel-Softmax (hard). | **Soft** by default (softmax); hard variant (Gumbel-ST) tested, underperforms but beats FNN. | All input blocks concatenated (content-driven, global within the module). | **Emergent** — fully learned. In successful runs, softmax weights correctly zero out irrelevant inputs; permutation-undoing representations emerge without supervision. |
| **09 — Modular DL Survey (fixed routing)** | Dispatch determined by metadata known a priori (task ID, language, domain, modality). Hard, deterministic, hand-designed. | **Hard** — deterministic, no learned component. | Metadata label (task, language, domain) — not derived from input representation. | **Enforced by construction** — specialization is structurally guaranteed; no collapse possible. Empirically outperforms learned routing in most benchmark conditions (Mittal et al. 2022; Muqeeth et al. 2022). |
| **09 — Modular DL Survey (learned routing)** | Linear or MLP projection of input representation x or task embedding t; hard (top-1/top-k, Gumbel-Softmax, RL) or soft (continuous MoE mixture). | **Both** — hard top-k or Gumbel variants; soft continuous-mixture variants. | Input representation or task embedding. | **Emergent** — but documented failure modes: module collapse, training instability at init, OOD drops from token-level routing. Mitigation: load-balancing losses, epsilon-greedy, MI losses, temperature annealing. |
| **10 — MICRO (top-1 router + 3-stage curriculum)** | Per-token top-1 MLP router assigns each token to one of four brain-network-aligned expert blocks (Language, Logic, Social, World) per layer; full block (attention + FFN) is the unit. Stage 2 uses soft top-2 for calibration stability; Stage 3 and inference use hard top-1. | **Hard** (top-1) at inference; **soft** (top-2) during Stage 2 calibration only. | Input token identity and context (learned MLP router), calibrated with GPT-4O-derived domain pseudo-labels in Stage 2. | **Enforced then emergent** — inductive bias injected via ~3,055 MICROSFT pseudo-labeled examples in Stage 2; specialization then persists through 939k-example Stage 3 SFT. Router entropy low post-training; domain-consistent routing patterns confirmed; human behavioral alignment r = 0.7. |

## Cross-cutting observations

*(synthesis)*

**Convergence on expert-choice framing for efficiency.** Both 01 (Expert Choice Routing) and 02 (MoD) independently adopt the expert-choice (inverted) framing — experts or paths select tokens, not vice versa — to avoid load-balancing auxiliary losses and guarantee static-graph computation. This is a practical convergence, not a philosophical one: both papers document that token-choice routing creates load-imbalance pathologies.

**Hard vs. soft split tracks granularity of dispatch.** FFN-level routing (01, 02) tends toward hard dispatch per token-per-layer, optimizing for FLOP reduction. Block-level compositional routing (03) favors soft dispatch because the task requires interpolation between block arrangements, not elimination of one path. Survey (09) documents that soft routing is computationally prohibitive at scale when all modules are activated. *(synthesis)*

**Specialization emergence vs. enforcement: no consensus.** The survey (09) is the most skeptical: learned routing under-utilizes modules, specializes them less as task count grows, and is outperformed by fixed routing in most tested settings. MICRO (10) resolves this by seeding specialization with an explicit curriculum before end-to-end fine-tuning — a hybrid that neither source alone describes. Block-operations (03) shows clean emergent specialization, but only on small-scale synthetic tasks; it does not constitute evidence at language-model scale. *(synthesis)*

**The survey's contrarian finding on learned routing.** The survey explicitly notes (Mittal et al. 2022; Muqeeth et al. 2022) that learned routing generally underperforms fixed routing and that specialization weakens as task count grows. This sits in tension with 01, 02, and 03, all of which report successful learned specialization — but all three operate in single-distribution or low-task-count regimes where the survey's pathologies are least likely to surface. *(synthesis)*

**Dispatch signal scope differs along a local-to-global axis.** MoD (02) routes using a single scalar per token per layer (maximally local). Expert Choice (01) routes using a full hidden-state projection but still per-token-per-layer. SMFR (03) uses the concatenation of all input blocks (global within the module, not per-token). MICRO (10) uses token identity and context. Fixed routing (09) uses metadata entirely external to the input. These differences in signal scope have underexplored implications for compositionality. *(synthesis)*

## Open questions (editorial)

*This section is editorial synthesis; claims are not directly sourced from any single paper.*

- **Does curriculum-seeded specialization generalize beyond four cognitive domains?** MICRO (10) shows the three-stage curriculum works for four brain-network partitions; whether the approach extends to larger expert counts, domain partitions without neuroscience grounding, or purely emergent task-structure discovery is untested.

- **Is the survey's skepticism of learned routing a scale effect or a regime effect?** The survey's negative results on learned routing come primarily from multi-task adapter settings. The single-distribution, efficiency-focused settings of 01 and 02 may simply not stress the collapse and underutilization pathologies the survey documents. A unified evaluation protocol that varies task count, distribution breadth, and expert count is absent from all five sources.

- **Soft vs. hard routing at block granularity.** Expert Choice (01) is nominally soft (continuous gating weights) but structurally hard (only top-k tokens per expert are non-zero). MoD (02) is explicitly hard (binary in/out). SMFR (03) is soft. MICRO (10) transitions from soft to hard over training. The right routing hardness for stable specialization at block (vs. FFN-sub-block) granularity is not established.

- **Causal autoregressive sampling under expert-choice routing.** Both 01 and 02 flag this as an open problem; the mitigations they propose (batch grouping; auxiliary binary predictor) are heuristic. MICRO (10) does not discuss this. A principled solution for top-k routing during autoregressive decoding remains open.

- **Whether routing specialization is mechanistically real or a performance artifact.** Expert Choice (01) infers specialization from benchmark performance versus hash-layer routing — not from mechanistic analysis of what routes where. The survey (09) explicitly flags the absence of a standardized benchmark for measuring specialization degree. MoD (02) and MICRO (10) provide routing-distribution analyses, but these are correlational, not causal.

## Source
- `raw/research/thesis-foundations/01-expert-choice-routing.md` — Expert Choice Routing
- `raw/research/thesis-foundations/02-mixture-of-depths.md` — Mixture of Depths
- `raw/research/thesis-foundations/03-block-operations.md` — Block-Operations
- `raw/research/thesis-foundations/09-modular-deep-learning-survey.md` — Modular Deep Learning survey (anchor)
- `raw/research/thesis-foundations/10-neuro-cognitive-reasoners.md` — MICRO

## Related
- [[expert-choice-routing]]
- [[mixture-of-depths]]
- [[block-operations-and-modular-routing]]
- [[modular-deep-learning-survey]]
- [[mixture-of-cognitive-reasoners-micro]]
- [[learned-routing-specialization]] (open conflict on whether learned routing specializes)
