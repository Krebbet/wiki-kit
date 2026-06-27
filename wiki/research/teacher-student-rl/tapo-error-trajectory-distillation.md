# TAPO: Error-Trajectory Self-Distillation via Micro-Reflective Trajectories

TAPO (Trajectory-Augmented Policy Optimization) from Alibaba/Qwen/Tsinghua is an on-policy self-distillation method that replaces OPSD's implicit KL-alignment with explicit construction of error-to-correction training trajectories. Where OPSD conditions on a "privileged" correct-trajectory prefix, TAPO constructs micro-reflective trajectories anchored in the model's own erroneous prefixes — preserving distributional proximity while providing a corrective signal at the first failure point. TAPO achieves +9.58 pp over GRPO on AIME 2024 in the cold-start setting.

## Method

TAPO augments GRPO with three interlocking components applied within each training iteration.

**1. Micro-Reflective Trajectory Construction (§3.3)**

Standard GRPO samples $K=8$ responses per query; TAPO partitions them into correct ($P$) and incorrect ($N$) sets.

- **Difficulty-Aware Candidate Selection (DCS):** a query is eligible iff $|P| \ge n_\text{pos}$ and $|N| \ge n_\text{neg}$ (default 2, 4). This targets the Zone of Proximal Development — mastered and beyond-capability queries are excluded, yielding an emergent curriculum as training progresses.
- **Trajectory Synthesis:** for each eligible query, up to $m_\text{max}=4$ incorrect rollouts $y^-$ are paired with a randomly-sampled correct reference $y^+$. A synthesis prompt instructs the actor itself (via vLLM) to (a) identify the first critical error in $y^-$, (b) reproduce the erroneous reasoning verbatim up to that error point, then insert a natural-language correction transition and continue to the correct answer. Output tagged with `<analysis>` and `<reconstruction>` XML.
- The **micro-reflective trajectory** $y^\text{ref}$ preserves the model's own erroneous prefix (maintaining distributional proximity) and diverges only at the first error point.

**Cold-start phase (§3.2):** 45k examples (30k SFT + 15k IFT) from Qwen3-8B-Instruct rollouts on DeepScaleR equip the model with trajectory-construction capability and XML format adherence before RL.

**2. Decoupled Advantage Estimation (DAE, §3.4)**

Constructed trajectories are assigned to a separate group $G^\text{ref}$; original GRPO rollouts remain in $G^\text{orig}$. Advantages computed independently:

$$A^{\text{orig}}_i = (r^{\text{orig}}_i - \mu_{G^\text{orig}}) / (\sigma_{G^\text{orig}} + \epsilon), \quad A^{\text{ref}}_j = (r^{\text{ref}}_j - \mu_{G^\text{ref}}) / (\sigma_{G^\text{ref}} + \epsilon)$$

This prevents **advantage contamination**: appending high-reward constructed trajectories to the original group would inflate the group mean, artificially penalise longer incorrect originals, and drive entropy/length collapse.

Combined loss: $\mathcal{L}_\text{TAPO} = \mathcal{L}_\text{GRPO}(G^\text{orig}) + \lambda \cdot \mathcal{L}_\text{ref}(G^\text{ref})$, $\lambda=1.0$.

**3. OOD Token Suppression (OTS, §3.5)**

Token-level weight $s_t = \log p_\theta(y_t | x, y_{<t}) + H[p_\theta(\cdot | x, y_{<t})]$; $w_t = \text{clamp}(\exp(s_t), 0.01, 10.0)$. Applied only to constructed trajectories — corrective transition tokens (out-of-distribution) are down-weighted; in-distribution tokens receive $w_t \approx 1$.

**Inference:** Standard single-pass generation — no reflection prompt, no thinking mode.

## Results

Qwen3-8B-Instruct with cold-start initialization (~16k ZPD-filtered DeepScaleR queries, K=8):

| Benchmark | GRPO Pass@1 | TAPO Pass@1 | Gain |
|---|---|---|---|
| AIME 2024 | 52.92% | 62.50% | +9.58 pp |
| AIME 2025 | 46.88% | 46.88% | tied |
| HMMT 2025 | 28.75% | 31.46% | +2.71 pp |

TAPO vs. OPSD: +4.79 pp (AIME24), +7.29 pp (HMMT25) in the cold-start setting.

**Capability internalization (Table 2):**
- Direct Solution Rate (DSR, correct without reflection): TAPO +13.5/+15.9/+22.3 pp over GRPO on AIME24/25/HMMT25.
- Effective Reflection Rate (ERR): TAPO +11.4/+4.8/+3.0 pp over GRPO.

**Ablation (Table 3):** SFT on the same micro-reflective data hurts vs. cold-start baseline (~1pp below), confirming RL optimization is critical. Full reconstruction (discard prefix, regenerate) loses 2–4 pp vs. micro-reflective prefix-preserving design.

## Core design insight

OPSD conditions on a privileged correct prefix, which suppresses errors rather than leverages them. TAPO's diagnosis: the bottleneck is the **explicit error diagnosis mechanism**, not the privileged target. By preserving the model's own erroneous prefix up to the first failure point and inserting an explicit correction, TAPO trains the model to identify and repair its own error patterns — which manifests as improved first-pass (DSR) reasoning, not just reflective correction.

## Key limitations

- Cold-start is load-bearing: without it, TAPO underperforms GRPO on AIME25 and HMMT25 (immature policy produces low-quality constructions).
- ZPD filtering discards ~50% of DeepScaleR problems (those below 12.5% or above 87.5% model accuracy).
- AIME 2025 Pass@1: GRPO and TAPO tie at 46.88%; GRPO beats TAPO at Pass@2 (57.08% vs. 56.46%). The "consistent improvements" claim is overstated for this benchmark.
- OPSD (in cold-start setting) is 57.71% on AIME24, stronger than cold-start+GRPO (52.92%) — TAPO's +4.79 over OPSD is the tighter comparison than TAPO vs. vanilla GRPO.
- All benchmarks are competition math; generalization untested.

## Key figures

- **Figure 2:** Micro-reflective correction prompt template with worked arithmetic error example; prefix preservation (red) + reflection phrase (yellow) + corrected reasoning (green)
- **Figure 3:** Training dynamics — OTS weight mean, policy gradient loss, training accuracy, gradient norm, response length, KL divergence (6 panels, 500 steps)
- **Eqs. 4–5:** Decoupled advantage estimation for $G^\text{orig}$ and $G^\text{ref}$
- **Eq. 6:** Combined TAPO loss
- **Eq. 7:** OTS score $s_t$
- **Tables 1–5:** Full results, DSR/ERR internalization, ablations, ZPD sensitivity

## Source

- `raw/research/weekly-2026-06-26/02-tapo-error-trajectory-self-distillation.md` (arXiv:2606.18844)

## Related

- [[research/teacher-student-rl/opsd-compresses-rlvr]] — TAPO's core critique: OPSD's implicit KL-alignment suppresses errors rather than leveraging them; TAPO is the prescriptive counterpart
- [[research/teacher-student-rl/_overview]] — extends the on-policy self-distillation lineage (OPSD, ROSD, OPD) with explicit trajectory construction
- [[research/curriculum-and-decomposition/_overview]] — DCS and ZPD-based filtering are direct instantiations of curriculum learning; parallels scrl-curriculum-credit-assignment
- [[research/self-improvement/_overview]] — self-improvement via self-generated corrective signal; extends STaR / rStar-Math to within-GRPO-iteration correction
- [[research/critique-self-correction/_overview]] — micro-reflective trajectories are a training-time analogue of inference-time Self-Refine / Reflexion, but internalized
- [[research/rl-optimizers/deepseekmath-grpo]] — TAPO is built on GRPO; DAE resolves a specific advantage-contamination failure mode of vanilla GRPO
- [[research/rlvr-mechanics/high-entropy-minority-tokens]] — OTS weight $w_t = \exp(\log p_\theta + H[p_\theta])$ is functionally related to entropy-based token selection; both privilege high-uncertainty positions
- [[research/weekly-briefs/2026-06-26]] — brought in by the 2026-06-26 weekly sweep
