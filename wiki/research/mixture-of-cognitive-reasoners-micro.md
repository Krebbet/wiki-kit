# Mixture of Cognitive Reasoners (MICRO)

MICRO (AlKhamissi et al., EPFL/MIT/Harvard) post-trains a pretrained transformer by cloning each transformer block into four brain-network-aligned expert modules — Language, Logic, Social, and World — then applying a three-stage curriculum to seed, calibrate, and preserve functional specialization. The resulting mixture-of-blocks (MOB) architecture uses a per-token top-1 MLP router to dispatch each token to exactly one full expert block (attention + FFN) per layer, and matches or exceeds comparable MoE and dense baselines on reasoning benchmarks while improving human behavioral alignment at the 1B scale.

## Architecture: MOB — 4 brain-network-aligned experts per block

Each transformer layer's single block is replaced by N=4 complete expert blocks; a lightweight MLP router assigns every token to exactly one expert per layer (top-1 hard routing at inference). The four experts and their neuroscientific referents:

| Expert | Brain network | Primary referent |
|--------|--------------|-----------------|
| Language | Left-lateralized frontal/temporal language network | Fedorenko et al. |
| Logic | Multiple Demand (MD) / fluid intelligence | Kanwisher |
| Social | Theory of Mind (ToM) / temporo-parietal junction | Saxe & Kanwisher |
| World | Default Mode Network / long-range integration | Gusnard et al. |

MOB differs from standard MoE — which restricts experts to FFN sub-layers with shared attention — and exhibits clearer functional specialization than MoE at tested scales (135M–3B). MoE ablations appear only in the appendix and do not replicate the same clean specialization pattern.

## Three-stage curriculum: seed → calibrate → generalize

1. **Stage 1 — Seed (MICROSFT)**: ~3,055 domain-labelled examples (2 epochs). GPT-4O annotates reasoning chains with per-token cognitive-domain pseudo-labels (Cohen's κ = 0.533 vs. human majority vote; human–human Fleiss' κ = 0.517). A soft top-2 router mixture is used here for training stability.
2. **Stage 2 — Router calibration**: Router trained on the pseudo-labelled tokens; generalizes to unlabeled data post-calibration. Hard top-1 routing resumes for Stage 3.
3. **Stage 3 — Generalize (TULU-3 SFT)**: 939k examples, 1 epoch. The specialization pattern seeded in Stage 1 is largely preserved through full-scale SFT.

## Specialization evidence

**Routing behavior.** Router entropy is low; domain-consistent routing is observed across model sizes. Arithmetic tokens route preferentially to the Logic expert; social-cognition tokens to the Social expert. Hierarchically, early layers favor the Language expert for linguistic grounding; deeper layers route to domain-specific experts — a structure that emerged without explicit enforcement.

**Neuroscience localizer correlation.** Language and Multiple Demand (MD) functional localizers — methodology from AlKhamissi et al. (2025a), originally designed for fMRI — successfully recover the corresponding MICRO expert modules. The ToM localizer improves with scale (fails at 1B, succeeds at 3B), suggesting ToM capability must exist before it can be localized. Social expert selectivity on 1,000 six-word sentences (Tuckute et al., 2024b dataset) correlates r = 0.7 with independently collected human mental-state-content ratings.

**Behavioral alignment.** MICRO-LLAMA-1B achieves the highest SBRE alignment score on COGBENCH (10 metrics, 7 cognitive psychology experiments) versus MOB and Dense baselines.

## Scale / benchmarks

Primary models: **LLAMA-3.2-1B** and **LLAMA-3.2-3B**. Additional appendix models: SMOLLM2-135M, SMOLLM2-360M, OLMo-2-1B.

Reasoning benchmarks (main paper): GSM8K (0-shot CoT), MINERVA-MATH, MMLU, MMLU-PRO, BBH (few-shot CoT). MICRO matches or outperforms MOB and Dense at 1B; gains are less consistent at 3B.

## Brain-inspired framing: direct-transfer vs. inspiration-only

**Direct-transfer (the paper claims structural identity, not loose analogy):**
- The four experts are explicitly named after and architecturally motivated by four well-characterized human brain networks; domain assignments derive from specific neuroscience literature (not loosely evoked).
- Neuroscience functional localizers — the same methodology used to map brain networks in fMRI data — are applied directly to MICRO models as a validation protocol.
- Layer-wise hierarchical specialization is compared directly against Fedorenko et al. (2024) findings on hierarchical cortical organization.
- MICRO is positioned as part of a NeuroAI research program; the authors describe it as the first modular LM explicitly designed to instantiate brain-like specialization.

**Inspiration-only (no identity claimed):**
- Behavioral alignment via COGBENCH measures similarity to human cognitive experiment outcomes, not neural activity identity.
- The four-network partition is a coarse discretization; the paper does not claim cortical topology is reproduced.
- Expert routing via a learned MLP has no claimed biological mechanism corresponding to inter-network routing in the brain.

## Negative results and failure modes

- **MoE does not match MOB**: FFN-only expert variants do not exhibit the same clear functional specialization at tested scales; results relegated to appendix.
- **ToM localizer fails at 1B**: Only 10 contrastive pairs (vs. 240 for Language, 100 for MD); ToM capability insufficient at 1B scale for reliable localization.
- **3B scaling inconsistency**: Statistically significant gains over baselines hold on only some benchmarks at 3B; the specialization benefit is less reliable than at 1B.
- **Non-orthogonal task-to-domain mapping**: BBH and MMLU subtasks often require multiple cognitive domains; the four-domain partition is not perfectly separable across all task types.
- **Social expert interference on math**: Ablating the Social expert on GSM8K and MATH slightly *improves* performance — the expert is actively detrimental on those tasks, not merely absent.
- **Scale ceiling untested**: No results beyond 3B base model; impact of varying expert count from N=4 is unknown.

## Open questions

- Can specialization extend to non-cognitive partitions (technical domains, natural languages)?
- How does MICRO scale beyond 8B parameters?
- What is the effect of varying expert count from N=4?
- How sensitive is specialization quality to MICROSFT dataset size/composition (~3,000 samples currently)?
- Does MICRO's internal representations align with actual neural activity in fMRI (blocked by lack of item-level fMRI datasets for MD and ToM networks)?
- Would human-annotated Stage 1 labels (vs. GPT-4O pseudo-labels) strengthen the inductive bias?
- Could RLVR as an additional post-training stage (beyond SFT/DPO) further improve specialization or reasoning?
- Future cognitive networks to incorporate: abstract formal reasoning (Kean et al., 2025a) and intuitive physics (Kean et al., 2025b).

## Source
- `raw/research/thesis-foundations/10-neuro-cognitive-reasoners.md` — *Mixture of Cognitive Reasoners: Modular Reasoning with Brain-Like Specialization*, AlKhamissi et al. (EPFL / MIT / Harvard)

## Related
- [[modular-deep-learning-survey]] — MICRO's MOB, top-1 router, and 3-stage curriculum all instance the survey's modular taxonomy.
- [[expert-choice-routing]] — both claim learned routing produces genuine specialization; MICRO extends scope from FFN-only to full blocks.
- [[block-operations-and-modular-routing]] — both motivate via binding problem (MICRO: brain networks; block-ops: Symbol Binding Problem); both converge on per-block routing.
- [[routing-mechanisms-in-modular-networks]] — MICRO's top-1 router feeds the routing aux taxonomy.
- [[brain-inspired-modularity]] — MICRO is one of the two anchors for the brain-inspired aux page (other: block-operations).
- [[learned-routing-specialization]] (open conflict) — MICRO provides the strongest positive evidence (r=0.7 neuroscience localizer correlation); contested by the survey.
