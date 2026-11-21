# CurvDelta / CurvLoRA: Low-Curvature Delta Modeling for Surgical Learning and Unlearning (Xiao et al.)

CurvDelta parameterizes the fine-tuning delta inside a fixed low-curvature subspace of a preservation loss, found once at $\theta_0$ via K-FAC with factorwise spectral truncation and two-sided projection. The realized update then provably (locally, quadratically) and empirically barely moves behaviour on a small preservation set. CurvLoRA is the low-rank variant. Claims: a better acquisition-retention trade-off on math/code (Gemma-3-1B, Llama-2-7B) and a better forget-retain balance on TOFU/MUSE. Results are mixed against Replay and CurvLoRA-style baselines on several cells. Not a sample-efficiency paper (100K task examples); relevant to us as a geometry-derived R_w primitive. arXiv:2611.24654; code not released.

## Method

Constrained problem: $\min_\theta L_{task}(\theta)$ s.t. $L_{pres}(\theta)\le\epsilon$, with $L_{pres}=\mathbb E_{D_{pres}}[\mathrm{KL}(p_{\theta_0}\Vert p_\theta)]$. Second-order expansion at $\theta_0$ (Hessian residual vanishes there):

$$L_{pres}\approx \tfrac12\,\Delta\theta^\top G_{pres}\,\Delta\theta,$$

with $G_{pres}$ the GGN/Fisher.

**K-FAC construction.** Per linear layer, $G_{pres}\approx K_{in}\otimes K_{out}$, with $K_{in}=\mathbb E[aa^\top]$ (input activations) and $K_{out}=\mathbb E[gg^\top]$ (output gradients). Both are estimated once at $\theta_0$ on a small $D_{pres}$ (256 FineFineWeb examples).

**Factorwise truncation.** Eigendecompose each factor and keep the leading eigenvectors $U_h$ up to energy fraction $\gamma$ (default 0.9). The projector onto the trailing (low-curvature) eigenspace is $P=I-U_hU_h^\top$. The delta is

$$\Delta W = P_{out}\,\delta\,P_{in}.$$

- **CurvDelta:** $\delta$ is a dense matrix initialized at 0.
- **CurvLoRA:** $\delta=BA$, so $\Delta W=(P_{out}B)(AP_{in})$.
- **Training (Algorithm 1):** estimate K-FAC, cache the leading eigenbases, train $\delta$ by differentiating through the projection, then merge.

Because the constraint is in the parameterization, the realized delta stays in the subspace under any optimizer. Gradient projection (CrispEdit-style) leaves the subspace under Adam, because per-coordinate second-moment rescaling breaks the projection. The paper's Fig 3 shows the parameterization beating projection (CurvDeltaGrad) on FQ and MU.

**Preservation bound (Theorem 1, $\epsilon$-feasibility).** The retained curvature per layer is bounded by $\kappa_l=\lambda_{out}[r_{out}+1]\cdot\lambda_{in}[r_{in}+1]$, the product of the first discarded eigenvalues. Then

$$L_{pres}\lesssim \tfrac12\sum_l \kappa_l\,\lVert\Delta W_l\rVert_F^2 .$$

The subspace geometry is task-independent, so it is cached and reused across tasks, objectives and parameterizations. The loss is arbitrary (SFT, GradDiff, NPO, SimNPO).

## Key claims and numbers

| Setting | CurvDelta / CurvLoRA | Baseline |
|---|---|---|
| Code, Llama-2-7B (CodeFeedback 104K; HumanEval/MBPP) | downstream 40.5 / retention 44.4 / ALL 42.8 | FT 38.5 / 40.4 / 39.6 |
| Math, Llama-2-7B (MetaMathQA 100K) | ALL 39.0 (CurvDelta), 40.1 (CurvLoRA) | Replay 40.2 (best); FT retention 45.6 -> 31.7 |
| Math, Gemma-3-1B | ALL 22.2; retention 22.9; GSM8K 36.9; MATH 5.5 | FT ALL 19.4; retention 18.1; GSM8K 36.9; MATH 5.7 |
| TOFU, Llama-3.1-8B, SimNPO, forget 5% / 10% | FQ -0.1 / -1.1; MU 63.3 / 63.2 | Retrain MU 64.6; LoRA FQ -7.4 / -13.5 |
| MUSE Books | VerbMem 11.6 | Retrain 14.2; retain KnowMem 55.8 vs Retrain 68.6 |
| Runtime (Fig 4c, TOFU, Llama-3.2-3B) | "-59.5% time" vs CrispEdit, lower peak memory | CrispEdit |

Baselines: FT, Replay, CrispEdit, OPLoRA, LoRA, PiSSA, MiLoRA, CorDA, VILA. Retention is measured on TriviaQA, NQ-Open and MMLU.

Ablations (Fig 2):
- Low-curvature subspaces beat dimension-matched high-curvature and random subspaces.
- Curvature estimation is robust from 0.25x to 4x the forget-set size.
- There is a $\gamma$ sweep.

## Limitations

- Local quadratic bound with a block-diagonal K-FAC model that ignores cross-layer terms. Fig 4a shows the quadratic estimate is on a smaller numerical scale than the real retain KL.
- Factorwise truncation discards mixed directions where a small eigenvalue in one factor offsets a large one in the other. The justification is only by appeal to the flat-direction and low-dimensional-optimization literature.
- Feasibility is not guaranteed a priori: $\lVert\Delta W\rVert_F$ depends on the LR schedule and step count, so drift grows with LR (consistent with an LR-confound reading of forgetting).
- Mixed results: Replay, MiLoRA and OPLoRA win some rows. MUSE retain KnowMem is far below Retrain. Gemma MATH is slightly below FT. Llama math ALL is not the best.
- Scale only 1B and 7B for capability learning. No sequential multi-task stacking. Preservation is measured on pretraining-like proxy data and benchmark retention, not on skills. $D_{pres}$ must be representative.

## What it means for our thesis

- **Relevance is as an R_w primitive, not as evidence.** There is no single- or few-shot training, no concept-vs-pattern evaluation, and no RL. The relevance is the mechanism for protecting prior capability during narrow updates.
- **Selective-finetuning stack.** It adds a curvature-subspace sub-family beside PIT, Skill-Localization, O-LoRA, ROME/MEMIT and AlphaEdit. The selection criterion is Fisher curvature on a preservation distribution. O-LoRA / OPLoRA use orthogonality, and AlphaEdit uses a hard null-space of preserved keys. Skill-Localization uses behavioural localization. CurvLoRA is the curvature-selected analogue of O-LoRA and is directly applicable to LoRA-based 1-40B runs.
- **Fit with RL.** The geometry is KL on $D_{pres}$, which is the same KL-minimality notion as in [[rls-razor]], enforced here by construction and off-policy. The loss-agnostic framing suggests wrapping a GRPO/RLVR task loss, but this is untested.
- **Practical cost for single-sample training.** The one-time K-FAC estimate on a 256-example $D_{pres}$ is cheap, and the cached subspace is reusable across concepts. The open risk is the restriction itself: a concept update may need exactly the high-curvature directions the projection removes, and the capacity-vs-preservation trade-off is untested at one-sample scale.
- **Code not released**, so reproduction means reimplementing K-FAC factor estimation plus the projected parameterization.

## Source

- raw/research/weekly-2026-11-20/05-curvdelta-curvlora.md (arXiv:2611.24654)

## Related

- [[research/catastrophic-forgetting/_overview]]
- [[research/catastrophic-forgetting/ewc-gemma2-cpt]]
- [[research/catastrophic-forgetting/rls-razor]]
- [[research/catastrophic-forgetting/composing-cl-anchors-long-horizon]]
- [[research/catastrophic-forgetting/path-not-taken]]
- [[research/selective-finetuning/_overview]]
- [[research/selective-finetuning/o-lora]]
- [[research/selective-finetuning/alphaedit]]
- [[research/selective-finetuning/deletion-tuning]]
- [[research/selective-finetuning/surgical-finetuning]]
- [[research/selective-finetuning/skill-localization]]
- [[research/rlvr-mechanics/rl-sparse-subnetwork]]
- [[research/rlvr-mechanics/relex-rank1-extrapolation]]
- [[research/moe-adapters/_overview]]
- [[../weekly-briefs/2026-11-20]] — brought in by the 2026-11-20 weekly sweep
