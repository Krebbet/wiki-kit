# BDH-CQ: In-Context Learning with Recurrent Latent Reasoning

Pathway/Bielik AI/NYU (arXiv:2608.09888) introduce BDH-CQ, a 150M-parameter non-Transformer system that acquires unseen visual transformations purely from in-context demonstrations — no backward pass, no task IDs, no verbalized intermediate reasoning — via a coupled contextual-memory + iterative-latent-workspace recurrence built on the "Dragon Hatchling" (BDH) architecture. Reaches 29.5% pass@2 on ARC-AGI-1 public eval at $0.00070/task, claimed as a new point beyond the reported ARC-AGI-1 cost–accuracy Pareto frontier and ~57× cheaper than GPT-5.6 Luna (Low) at 34.2%/$0.040.

## Method

Built on BDH (Kosowski et al. 2025, arXiv:2509.26507), a post-Transformer sequence model using high-dimensional positive activations, low-rank inter-unit communication, and a recurrent associative state. BDH-CQ adds two coupled recurrences:

1. **Contextual memory**: `S_t = U_θ(S_{t-1}, D_t)` sequentially ingests each demonstration pair `D_t` without compressing to a single task vector. Related to fast-weight/linear-attention memory — linear attention is the degenerate case `S_t = S_{t-1} + U_θ(D_t)`.
2. **Latent workspace**: after all demonstrations and the query are folded into `S_K`, a separate state `H_r` iterates `H_{r+1} = F_θ(H_r, S_K)` for R steps; only the final step decodes to an answer, `ŷ = G_θ(H_R)`. No intermediate tokens are ever produced or supervised — reasoning depth is entirely in the recurrence, same "compute via iteration, not verbalization" stance as [[hrm]].

Exact dimensions, update rules `U_θ`/`F_θ`/`G_θ`, and the training recipe are proprietary — not disclosed even in the paper's method section per the source summary. Training data: ARC-AGI-1 train split, RE-ARC, ConceptARC, ARC-Heavy, ARC-GEN100K, plus undisclosed proprietary augmentations.

Positioned explicitly against transductive recursive solvers: [[hrm]], TRM, and (by extension) [[gram-recursive-reasoning]] require a backward pass and a learned per-puzzle identity embedding fitted to the actual eval task before inference. BDH-CQ performs zero-gradient in-context adaptation — weights are frozen at inference, and the only per-task state is the forward-computed `S_K`/`H_R` recurrence, not a set of updated parameters.

## Results

150M params, ARC-AGI-1 public eval (400 tasks): 24.25% pass@1, 29.5% pass@2 (95% Wilson CI [25.24, 34.15]), ~0.85 H200 GPU-seconds/task → $0.00070/task. An independent black-box audit (co-authors from Bielik AI + NYU, no weight access) reproduced the 29.5% pass@2 figure.

Cost comparison: GPT-5.6 Luna (Low) scores 34.2% at $0.040/task on the ARC Prize leaderboard (Aug 2026) — higher accuracy but ~57× the cost. Against transductive solvers costed at inference time: [[hrm]] $1.48/task (52.0% ARC-AGI-1), TRM $1.76/task — BDH-CQ is ~2,000–2,500× cheaper at lower peak accuracy; not a same-protocol comparison since HRM/TRM/[[gram-recursive-reasoning]] (66.7% ARC-AGI-1) train per-task rather than adapting in-context.

ConceptARC: 45.63–45.00% pass@1, 59.38–60.00% pass@2 task accuracy, 77.92% test-pair pass@2. The 18.5-pt gap between test-pair and whole-task accuracy indicates partial-but-inconsistent rule application on 52/160 tasks — the model gets individual pairs right more often than it gets the whole task right, implying rule extraction is noisy rather than binary pass/fail.

Controlled generalization probes separate capacity limits from extrapolation gaps:
- Boundary-propagation / motif-copying: saturates at 48/48.
- Ordering: collapses from near-ceiling to 1/24 at sequence length 8, recovers to 13/24 given one matched-complexity demonstration.
- Nesting: holds to depth 4, drops to 29/36 at depth 5, recovers to 24/24 with a matching-depth support example.

Reasoning-effort scaling: HIGH 29.5% pass@2 / MEDIUM 27% (11% cheaper) / LOW 21% (22% cheaper) — a smooth accuracy/cost knob via R (latent-workspace iteration count), analogous to test-time compute scaling in looped/recurrent-depth models.

## Applicability

Cost-constrained ARC-style/visual few-shot reasoning where inference cost dominates over peak accuracy. Not adoptable off-the-shelf: no weights, no code, core mechanism (`U_θ`, `F_θ`, `G_θ` definitions and training recipe) undisclosed — reproducing requires building a full BDH-family architecture plus an ARC-scale curated data pipeline from scratch. Authors claim (unpublished, unverified) tensor-sharding scales "particularly easy" from 1B to 600B+ params with early Transformer-like scaling-law behavior preserved — treat as a marketing claim pending any independent scaling evidence.

## Novelty

Recombination rather than a new primitive: continuous/recurrent latent reasoning (Coconut-style continuous-thought feedback; recurrent-depth/looped-Transformer test-time compute, cf. [[hrm]]) fused with in-context/fast-weight memory (linear attention). The gap it closes: prior recursive/latent solvers ([[hrm]], TRM) are transductive — they require gradient-based per-task optimization on the actual eval demonstrations before answering. BDH-CQ claims to be first in this line to acquire a previously-unseen visual transformation solely from in-context demonstrations at inference, with zero backward pass and zero task identifiers.

## Reproducibility

No code, no released weights, no paperswithcode entry. Core architectural update rules and training recipe explicitly proprietary. The only external verification is the black-box audit reproducing the top-line pass@2 score under a documented (but not code-released) protocol, without access to weights.

## Adoption

Too new (Aug 2026) for citation or community pickup signal. Given the proprietary architecture and undisclosed training recipe, third-party reproduction is unlikely near-term.

## Source

`raw/research/weekly-2026-08-22/05-bdh-cq-recurrent-latent-reasoning.md` (arXiv:2608.09888)

## Related

- [[hrm]] — BDH-CQ explicitly contrasts itself against HRM's transductive, per-task-optimized ARC pipeline; HRM costs $1.48/task vs BDH-CQ's $0.00070/task, though under different adaptation regimes (gradient-based per-task fitting vs zero-gradient in-context).
- [[gram-recursive-reasoning]] — same task-trained recursive-solver cluster; GRAM reaches 66.7% ARC-AGI-1 vs BDH-CQ's 29.5% — a different point on the accuracy axis, not directly cost-compared under one protocol.
- [[hrm-text]] — cited as evidence that hierarchical recurrence also supports efficient language modeling at 1B scale, supporting BDH-CQ's framing of recurrence as a general compute-via-iteration mechanism beyond ARC-style tasks.
- [[test-time-training]] — contrast: BDH-CQ updates only a recurrent activation state at inference, with no parameter updates, distinguishing its zero-gradient in-context adaptation from TTT's weight-update mechanisms.
