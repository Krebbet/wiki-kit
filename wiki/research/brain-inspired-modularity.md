# Brain-Inspired Modularity

Two papers in the thesis foundation use neuroscience and cognitive psychology to motivate modular transformer design: paper 03 (block-operations / SMFR) grounds block discretization in the Symbol Binding Problem, treating modules as cognitive "object slots"; paper 10 (MICRO) goes further, naming experts after four empirically characterised human brain networks and validating alignment with neuroscience localizers. Together they establish that segregating information flow into discrete, specialised sub-circuits is motivated by both cognitive theory and measurable neural organisation — but the strength of the transfer claim differs sharply between them. The contrast is instructive: inspiration-only framings supply design intuition and informal justification, while direct-transfer framings supply falsifiable predictions that can be tested against neuroscience data.

## Two framings

### Symbol Binding Problem (block-operations)

**Tagging: inspiration-only**

Paper 03 motivates uniform tensor blocking via the Symbol Binding Problem (Greff et al., 2020) and the *superposition catastrophe* (Von der Malsburg, 1986): when distinct objects share the same representational substrate, composition is ambiguous — the classic example being two simultaneously perceived objects whose features cannot be unambiguously bound to separate representations. Block-discretisation is offered as an engineering analogue to cognitive "object slots" — each block acts as a placeholder variable that can be routed, swapped, or left unchanged without cross-contamination between conceptually distinct entities. The parallel is explicitly a design metaphor; no neuroscience localizer or behavioural-alignment experiment is run, and no direct-transfer claim is made. The summary flags this as analogical.

Inductive bias claim: enforcing Modular Representation-Preserving Mappings (MRPMs) across uniform blocks creates a bottleneck that should force segregation and compositionality. The SMFR module (Stack of Multiplexers and FNNs with gated Residuals) instantiates this: the Multiplexer outputs a learned M×N soft-routing matrix over input blocks; the FNNR applies per-block gated residual transformations; together they enforce that each output block traces cleanly to a single input block or a new transformation thereof.

Empirically, SMFR achieves 100 % OOD accuracy on double-addition and the ALGO task where FNNs and Transformers fail — lending weight to the inductive bias even if the neuroscience motivation remains loose. On BPMNIST, converged models learned to undo the input permutation in the first layer, recovering permutation-invariant representations — consistent with the slot-binding intuition but not interpretable as a neuroscience prediction. No routing collapse was observed.

### Brain-network-aligned experts (MICRO)

**Tagging: direct-transfer** (with one partial failure noted below)

Paper 10 names and motivates each of its four expert blocks after empirically characterised human brain networks:

| Expert | Brain network | Neuroscience anchor |
|--------|--------------|---------------------|
| Language | Left-lateralised frontal/temporal | Fedorenko et al. |
| Logic | Multiple Demand / fluid intelligence | Fedorenko et al. |
| Social | Theory of Mind / temporo-parietal junction | Saxe & Kanwisher |
| World | Default Mode Network | Gusnard et al. |

The paper applies functional **localizer** experiments — the same fMRI-derived methodology used to isolate these networks in human subjects — to MICRO models. Language and MD localizers successfully recover corresponding experts; the ToM localizer fails at 1B scale and partially succeeds at 3B, attributed to insufficient ToM capacity at small scale (and a small stimulus set: 10 contrastive pairs vs. 240 for language). Human behavioural alignment is additionally measured via COGBENCH (10 metrics, 7 cognitive-psychology experiments); MICRO-LLAMA-1B outperforms MoE and dense baselines on this alignment index.

The r = 0.7 correlation between social-expert selectivity and independently collected mental-state-content ratings (Tuckute et al., 2024b; N = 1,000 sentences) is the strongest quantitative link to neuroscience in either paper — it grounds direct-transfer: a metric from human neuroscience is being applied to the model and yields a meaningful correlation, not just a loose design metaphor. The framing is therefore direct-transfer rather than inspiration-only, with the caveat that causal equivalence (the expert *is* a Theory-of-Mind module in the biological sense) is not established. Functional alignment via a localizer is weaker than mechanistic identity; the paper itself does not claim the latter.

One notable failure of the direct-transfer framing: removing the Social expert on math benchmarks *improves* performance — suggesting the Social expert is not merely silent on irrelevant tasks but actively interferes. This is hard to explain within a clean brain-network analogy and is left unaddressed.

## Cross-cutting observations (editorial)

Both papers converge on **per-block routing as the key structural commitment**: granularity should be at the level of full transformer blocks (attention + FFN), not sub-components, and routing should be content-driven. But the cognitive starting points diverge:

- Paper 03 takes a *representation-theoretic* route — the problem is slot confusion, the fix is discretisation. Routing emerges as a mechanism to maintain slot identity across transformations. The cognitive framing is about *what kind of information* occupies a slot.
- Paper 10 takes a *functional-specialisation* route — the problem is that generic transformer layers do not develop domain-specific competencies, the fix is to seed and preserve specialisation via an explicit curriculum. Routing there implements *domain dispatch*, not slot identity.

The two are not contradictory — slot-level segregation (03) and domain-level specialisation (10) are complementary inductive biases — but they motivate architectures that differ in what the routing signal encodes. In SMFR routing selects among *object transformations*; in MICRO routing selects among *domain-competent processors*. Whether these collapse into the same mechanism at scale is unanswered by either paper.

A further tension: paper 03's blocks are uniform and task-agnostic; paper 10's experts are seeded with domain-specific labels. This suggests a spectrum between emergent (unsupervised) and seeded (supervised) specialisation — a design axis neither paper fully explores.

## Relevance to the thesis (editorial)

The thesis question — can a *repetitive* transformer architecture identify correct sub-architectures and route information correctly — maps directly onto the concerns of both papers. "Identifying correct sub-architectures" corresponds to the specialisation question: do routing decisions actually select modules with distinct competencies, and do those competencies stabilise under training? Both papers provide partial evidence (SMFR: routing collapse was not observed; MICRO: low router entropy, domain-consistent routing patterns persist through 939k SFT examples). "Determining what information goes where" corresponds to the routing-signal question: both papers use content-driven, fully learned routers, and both show emergent hierarchical organisation without explicit enforcement (SMFR: early block undoes permutation; MICRO: Language expert dominates early layers, domain experts later). Brain-inspired modularity is thus not decorative framing — it supplies testable predictions about *what* structural biases should produce correct routing.

## Open questions (editorial)

**Does analogical evidence from neuroscience actually transfer?**

For paper 03: no test is offered. The Symbol Binding framing motivates the architecture but does not generate neuroscience-falsifiable predictions. A falsification would require showing that SMFR blocks *do not* behave as object slots (e.g., that content from one block systematically bleeds into another under a structured probe).

For paper 10: the localizer methodology provides a partial test and partially fails (ToM at 1B). A stronger falsification would be: train MICRO on a task set where the four-network partition is *not* the natural decomposition, and show routing collapses or specialisation does not emerge. The paper does not run this. Additionally, the r = 0.7 correlation is correlational — it does not establish that the Social expert computes Theory-of-Mind in any mechanistic sense, only that it is more active on mental-state content. The gap between functional alignment and mechanistic equivalence remains open.

**What would meaningful direct-transfer look like?**

Likely: (a) interventional evidence — ablating the Social expert selectively degrades mental-state reasoning without degrading other domains; (b) representational similarity to actual neural activity (blocked by lack of item-level fMRI data for non-language networks, as the authors note). Neither paper reaches this bar.

## Source
- `raw/research/thesis-foundations/03-block-operations.md` — Block-Operations / SMFR (Symbol Binding Problem anchor)
- `raw/research/thesis-foundations/10-neuro-cognitive-reasoners.md` — MICRO (brain-network anchor)

## Related
- [[block-operations-and-modular-routing]]
- [[mixture-of-cognitive-reasoners-micro]]
