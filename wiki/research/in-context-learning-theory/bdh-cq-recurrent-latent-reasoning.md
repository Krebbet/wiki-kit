---
name: bdh-cq-recurrent-latent-reasoning
description: 150M-param system combining recurrent-memory in-context learning (no weight updates) with iterative latent-space reasoning (no verbalized CoT); new ARC-AGI-1 cost-efficiency SOTA. Fourth mechanistic account of ICL alongside induction-heads / GD / Bayesian.
type: research
---

# BDH-CQ: In-Context Learning with Recurrent Latent Reasoning

Engdahl, Kosowski, Chorowski et al. (Pathway / Bielik / NYU), arXiv:2608.09888. A 150M-parameter reasoning system built on the Dragon Hatchling (BDH) architecture (Kosowski et al. 2025) that separates two mechanisms usually conflated: **in-context learning via an explicit recurrent memory** (demonstrations update a persistent state, fixed weights, no gradient) and **iterative latent-space reasoning** (per-query computation in a structured latent workspace, no verbalized chain-of-thought). Reaches 29.5% pass@2 on public ARC-AGI-1 at $0.00070/task — a new point on the cost–accuracy Pareto frontier, independently reproduced by a black-box audit with no weight access.

## Method

Two architecturally distinct update loops on top of BDH's ReLU-low-rank + linear-attention layers (high-dimensional positive-activation feature space):

**(1) In-context learning via recurrent memory.** Demonstrations $D = \{(x_t, y_t)\}_{t=1}^K$ are processed *sequentially*, not compressed into one task vector:

$$S_t = U_\theta(S_{t-1}, D_t), \quad \theta \text{ fixed} \tag{Eq. 1}$$

— analogous to attention/fast-weight memory; linear attention is the special case $S_t = S_{t-1} + U_\theta(D_t)$.

**(2) Recurrent latent reasoning.** After ingesting $K$ demonstrations, iterate in a structured latent workspace $H_r$:

$$H_0 = E_\theta(x^*, S_K), \qquad H_{r+1} = F_\theta(H_r, S_K), \qquad \hat y = G_\theta(H_R) \tag{Eqs. 2–4}$$

for $r = 0..R{-}1$. $S_t$ (evolves with evidence, supports ICL) and $H_r$ (per-query computation) are kept architecturally distinct. Reasoning "effort" (latent iteration depth $R$) is a trainable/selectable knob (LOW/MEDIUM/HIGH). Trained on ARC-AGI-1 training set + RE-ARC + ConceptARC + ARC-Heavy + ARC-GEN100K + private data with augmentation; eval-task demonstration pairs are never seen in training — no task IDs, no eval-task-specific optimization. Exact update-rule internals and dimensions are proprietary. Training objective is direct supervised(-style): "trains the system to use preceding examples and produce exact target grids" — no RL, no reward signal.

## Claims

29.5% pass@2 on the 400-task public ARC-AGI-1 eval at $0.00070/task (~0.85 H200-GPU-sec/task at $3/hr) — new SOTA on the ARC-AGI cost-efficiency Pareto frontier (Fig. 2): ~57× cheaper than GPT-5.6 Luna (Low, 34.2% at $0.040/task), ~11× cheaper after GPT-5.6's later 80% price cut. An independent black-box audit (Bielik + NYU co-authors, no weight access) reproduced 29.5% pass@2.

ConceptARC (16 concept families, semantic task IDs): 59.38% strict-task pass@2 / 77.92% test-pair pass@2 (Table 1–2; FilledNotFilled/TopBottom2D/ExtendToBoundary strongest at 8–9/10, Copy/Order weakest at 2/10).

**Cost contrast with task-trained recursive solvers (HRM, TRM):** HRM and TRM recursively refine latent+candidate-answer state on ARC but are *transductive* — eval-task demonstration pairs are augmented and used in optimization with learned per-puzzle identity embeddings, i.e. weight/embedding updates at eval time. HRM costs $1.48/task, TRM $1.76/task (ARC Prize-reported) — over 2000× more than BDH-CQ, because BDH-CQ does pure forward-pass ICL with no eval-time backward pass at all.

## Concept-learning evidence

Frames the central object as a "demonstration-conditioned operator schema" — a reusable visual operation bound purely from in-context demonstrations. Controlled generalization ladders (matched interpolation/extrapolation manipulations, significance-tested) give a genuinely mixed picture:

**Supporting compositional-transfer evidence:**
- Dense task-specific color permutations (2–8 simultaneous bindings) solved 24/24 at every tested level — the model recovers and consistently applies a mapping introduced entirely through context.
- Boundary propagation and motif-copying extrapolate cleanly across the full tested range (48/48 at every level), no ceiling reached.
- Atomic operations (relocation, reflection, rotation) each solved 72/72; rotation composes losslessly with relocation (72/72) — genuine compositional transfer, not just atomic pattern-match.

**Countervailing pattern-matching evidence:**
- Color-swap is acquired only in the *original fixed-layout* motif family (26/72) and never composes (0/72); shuffled-color families collapse to 1/24 even in isolation — a seemingly "conceptual" operator that turns out to be representation/layout-dependent.
- Ordering (sequence length 6→8: 29/36→8/24→1/24) and nested containment (saturated to depth 4, falls to 29/36 at depth 5) both show sharp non-monotonic cliffs. These are *not* execution-capacity limits but extrapolation-*coverage* limits: a single matched demonstration at test complexity recovers nesting to 24/24 and ordering from 0/24 to 13/24 (Table 3).
- 52/160 ConceptARC tasks get 1–2/3 test pairs right but fail the full task — partial-correctness evidence that the "induced rule" is often not applied uniformly, cutting against a strict rule-induction account.

## RL connection

None. Direct supervised(-style) training objective; no reward signal, no exploration strategy. Full training recipe is proprietary.

## Sample efficiency

Not single-sample training — trained on a large curated multi-source ARC-style corpus. But the *inference-time* mechanism is genuinely few-shot in-context: each task specifies its transformation via only $K \approx 2$–4 demonstrations, no gradient updates, no eval-task-specific fine-tuning. Output quality scales with *coverage* in the $K$ demonstrations, not with total training data — a single supporting demonstration at test complexity recovers most of an extrapolation failure (Table 3). Directly relevant to the wiki's "does K-shot generalize" question, but at the mechanism level (fixed $\theta$, memory update only) rather than the RLVR training-sample-count level the wiki otherwise tracks.

## Failure modes / limitations (author-acknowledged)

- Conditional rule selection (which of two demonstrated rules applies, cued by a marker) drops 43.3 pts vs. a same-cue-same-rule control (100%→56.7%, $p=9\times10^{-9}$) — genuine selection-under-ambiguity weakness.
- Parameter values absent from demonstrations (even interpolated, not extrapolated) solve 0/120 vs. 12/40 when demonstrated — needs the *exact* value shown, not just in-range.
- Panel-union/segmentation is sensitive: 2 opposite-corner panels 26/40 but 3 panels 1/40; touching (unseparated) panels 3/40 vs. separated 26/40.
- Support-chain dependency decays monotonically 80%→27.5% as dependency-chain length grows 1→8, controlled against a 3-independent-object baseline (40/40) ruling out mere object-count as the cause.
- Nominal pass@2 may overstate independent-sampling diversity — in the opaque replication, all 75 single-candidate records were already correct at rank 1.
- MIN vs. STANDARD effort: cost drops 3× but score drops only 1.75 pp, and the comparison is not statistically resolved (McNemar $p=0.167$).
- Deterministic at fixed effort — repeated identical requests are byte-identical, no exploration/sampling diversity at inference.
- Authors explicitly caution: output-level failure signatures (dimension-correct, palette-correct, shape-correct-but-wrong-cells) characterize final grids only, not the latent rule followed — "a correct rule applied incompletely is observationally indistinguishable from a narrower rule applied completely."
- Not evaluated on ARC-AGI-2; transfer to language/math reasoning is future work, unstated whether recurrent-memory ICL generalizes beyond the visual-grid domain.
- Architecture internals (dimensions, exact update rules) are proprietary — a genuine reproducibility limitation.

## Cited leads for follow-up

- **Kosowski et al. 2025 (Dragon Hatchling / BDH, arXiv:2509.26507)** — the base architecture this system extends.
- **Hao et al. 2024 (Coconut, arXiv:2412.06769)** — closest continuous-latent-reasoning ancestor; BDH-CQ explicitly contrasts its demonstration-conditioned recurrent memory against Coconut's curriculum-dependent internalization.
- **Wang et al. 2025 (HRM, arXiv:2506.21734)**, **Jolicoeur-Martineau 2025 (TRM, arXiv:2510.04871)** — the directly-compared transductive task-trained recursive solvers (see [[../variable-granularity/hierarchical-reasoning-model]]).
- **Moskvichev et al. 2023 (ConceptARC, TMLR)** — the concept-organized eval ontology used throughout.

## Source

- `raw/research/weekly-2026-08-14/03-bdh-cq-icl-latent-reasoning.md`

## Related

- [[_overview]] — fourth mechanistic account of ICL alongside induction heads, ICL-as-gradient-descent, and Bayesian inference: demonstrations accumulate into an explicit *evolving state* ($S_t$) rather than a static implicit weight update or single posterior update. Directly matches this theme's framing as "closest analogue to single example imprints a concept without weight updates."
- [[icl-implicit-weight-update]] — closest formal parallel: that page's Theorem 2.3 (context ≡ context-free forward pass + rank-1 MLP weight patch) and BDH-CQ's Eq. 1 recurrent-state formulation are two different formalizations of "ICL as an update to an internal state that persists across the context window."
- [[../variable-granularity/hierarchical-reasoning-model]] — direct empirical contrast (source §8, "Task-trained recursive solvers"): HRM/TRM are transductive (eval-time optimization + learned per-puzzle identity embeddings); BDH-CQ is pure forward-pass ICL. Cost delta: $0.0007/task vs. $1.48–1.76/task.
- [[../test-time-training/_overview]] — sharpens this theme's spectrum from "TTT with weight updates" to "ICL with no weight updates" to "recurrent-memory ICL with no weight updates but persistent evolving state."
- [[../concept-evaluation/_overview]] — the paper's controlled ARC-like ladders (conditional rule selection, absent-parameter interpolation/extrapolation, panel-union separation, support-chain depth) are a concept-evaluation methodology directly analogous to this theme's existing methods (GSM-Symbolic, Counterfactual Tasks, Contrast Sets).
- [[../../weekly-briefs/2026-08-14]] — brought in by the 2026-08-14 weekly sweep
