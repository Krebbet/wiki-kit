# SGSD: Skill-Conditioned Gated Self-Distillation for LLM Reasoning

On-policy self-distillation (SD) improves LLM reasoning by converting sparse verifier outcomes into dense token-level supervision via a privileged-context teacher drawn from the same model. SGSD extends this by replacing trusted privileged information (reference answers, successful traces) with an **experience-derived skill bank** of general reasoning principles and common mistake patterns. Because retrieved skills may be irrelevant or misleading, SGSD reframes the problem as *teacher hypothesis validation*: a multi-teacher pool (each teacher conditioned on a different retrieved skill–mistake pair) scores the same plain-prompt student rollout, and the verifier outcome determines each teacher's polarity — a teacher that supports a success or suppresses a failure is distilled; one that supports a failure or suppresses a success is reversed. A bounded gated objective ($\ell_\text{gate}$) down-weights near-zero teacher–student log-probability gaps (uninformative agreement) and exponentially damps extreme gaps (likely artifacts), concentrating learning in the informative middle region. On Qwen3-1.7B, SGSD reaches avg@12 = 43.7% across AIME24/AIME25/HMMT25, outperforming GRPO by 6.2 pp and answer-conditioned OPSD by 1.7 pp under a strictly weaker privileged-information assumption; gains are smaller but still positive on 4B and 8B scales.

## Source

- arXiv: https://arxiv.org/abs/2605.28791
- Capture: `raw/research/weekly-2026-05-30/04-sgsd-skill-gated-distillation.md`
- Code: https://github.com/walawalagoose/SGSD

## Method

**Skill bank $\mathcal{B} = \{G, E\}$.** $G$ contains general skills (title, principle, when\_to\_apply); $E$ contains common mistake patterns (description, why\_it\_happens, how\_to\_avoid). Cold-start: sample 256 in-domain problems, generate traces, distill successes into $G$ candidates and failures into $E$ candidates, hierarchically merge to remove duplicates. Online update every $F=25$ steps: extract new candidates from the recent rollout window and merge into the dynamic portion of the bank, skipping if success rate $\hat{p} \ge \gamma = 0.8$.

**Multi-teacher pool.** For problem $x$, retrieve top-$K=8$ skill–mistake pairs via Qwen3-Embedding-0.6B; teacher $k$ receives context $c_k(x) = g_k \oplus e_k \oplus x$. All teachers are stop-gradient copies of the current student policy $\pi_{\bar\theta}$; the student sees only $x$. Teacher weight $\alpha_k(x)$ = softmax of average retrieval similarity score.

**Outcome-validated polarity.** Token-level gap $\Delta_t^{(k)} = \log p_T^{(k)}(y_t | x, y_{<t}) - \log p_S(y_t | x, y_{<t})$. Robust teacher-level support: mask special/formatting tokens, clip gaps at $c_\Delta = 3.0$, average; threshold at $\epsilon_a = 0.05$ to zero for uncertain teachers. Polarity: $\rho_k = \text{sgn}(r) \cdot \text{sgn}(\tilde{a}_k)$ if $|\tilde{a}_k| > \epsilon_a$, else $0$.

**Gated distillation loss:**

$$\ell_\text{gate}(\Delta) = \log 2 - \log\!\left(1 + \exp\!\left(-\frac{\Delta^2}{2\tau_g}\right)\right), \quad \tau_g = 1.0$$

Gradient $g_\tau(\Delta) = \Delta / (\tau_g(1 + \exp(\Delta^2/(2\tau_g))))$ is bounded by $1/(\sqrt{e}\,\tau_g)$, linear near zero (matching local reverse-KL), and exponentially decaying for large $|\Delta|$.

**Full objective:**

$$\mathcal{L}_\text{SGSD}(x) = \sum_{k=1}^{K_x} \alpha_k(x)\,\rho_k\,\bar{\ell}^{(k)}$$

where $\bar{\ell}^{(k)}$ is the masked, token-averaged gated loss for teacher $k$. Update direction is jointly determined by the verifier outcome (via $\rho_k$) and the teacher's stance — not by the teacher alone.

## Results

All experiments use Qwen3-{1.7B, 4B, 8B}, LoRA rank 64, trained 200 steps on DAPO-Math-17K (English), evaluated (avg@12) on AIME24, AIME25, HMMT25.

| Model | Base | GRPO | OPSD | SGSD |
|---|---|---|---|---|
| Qwen3-1.7B | 37.4 | 37.5 | 42.0 | **43.7** |
| Qwen3-4B | 62.3 | 62.7 | 63.5 | **64.3** |
| Qwen3-8B | 62.1 | **65.0** | **66.8** | 65.5 |

SGSD beats OPSD on 1.7B and 4B; falls 1.3 pp behind on 8B, suggesting the skill-PI advantage shrinks as the model's intrinsic self-consistency grows. Skill-augmented baselines (Base+Skill, GRPO+Skill, OPSD+Skill) underperform their plain counterparts, confirming that naive skill injection at rollout/eval time hurts rather than helps — skills must be teacher-side only.

**Ablations (Qwen3-1.7B, AIME24):** removing polarity causes late-stage collapse (step-100 accuracy drops below base); single teacher consistently below full pool; removing all robust-support components (masking + clipping + threshold) falls below base at step 100 (48.1 vs 51.1).

**Design choices:** full-vocabulary distillation outperforms Top-100 approximation by up to 2.8 pp; live synchronized teacher outperforms frozen/periodic/EMA; gated loss peaks higher than reverse-KL, forward-KL, or JSD; adding OPSD-style answer PI to skill teachers causes collapse at step 100 (−9.7 pp AIME24, −10.0 pp AIME25).

## Connections to the wiki

- **[[_overview]]** — SGSD is a new entry in the "teacher sees answer?" axis: teachers see skills, not the answer; direction is co-anchored by verifier and teacher. Repositions the "trusted PI" assumption as a degree of freedom, not a binary.
- **[[opsd-compresses-rlvr]]** — OPSD (Zhao et al., arXiv:2601.18734) is the direct baseline. SGSD uses the same per-token reverse-KL-style credit assignment but with polarity gating and skill-based PI instead of reference-answer PI. Note: "OPSD" here is the Jan-2026 self-distillation paper, not the May-2026 compaction-diagnostic paper on this page — same abbreviation collision flagged in [[opsd-compresses-rlvr]].
- **[[rlt-followups-2026]]** — sits in the same 2026 SD wave; SGSD is distinct from OPSD/SDFT/SDPO in its skill-bank PI and polarity-reversal mechanism.
- **[[co-evolving-policy-distillation]]** — CoPD co-evolves teacher weights; SGSD co-evolves the skill bank while keeping teacher weights synchronized with the student. Different locus of teacher adaptation.
- **[[../self-improvement/_overview]]** — skill bank construction follows the STaR/Reflexion spirit: successful traces → reusable skills; failed traces → mistake patterns. SGSD is the RL-training-loop application.
- **[[../rlvr-mechanics/deepseekmath-grpo]]** — GRPO is the RLVR baseline; SGSD's polarity-gated objective produces a policy-gradient update with a dense per-token coefficient $W_t^{(k)} = \alpha_k \rho_k (m_t/Z) g_\tau(\Delta_t^{(k)})$ that subsumes GRPO's sparse outcome reward.
- **[[../synthesis/concept-curriculum-method]]** — skill bank = distilled concept library; polarity validation = outcome-anchored credit assignment. Directly relevant to the P4 principle-decomposition slot: skills are explicit reasoning principles, validated by on-policy evidence rather than assumed trustworthy.

## Watchlist candidates

- **Skill-SD** (Wang et al., arXiv:2604.10674) — skill-conditioned SD for multi-turn LLM agents; direct sibling paper, different task domain.
- **On-Policy Self-Distillation survey** (Cui et al., arXiv:2605.18141) — landscape overview of the SD family; useful for situating SGSD.
- **UniSD** (Jin et al., arXiv:2605.06597) — unified SD framework; may subsume or conflict with SGSD's formulation.
- **Self-Distillation Zero / SDZ** (He et al., arXiv:2604.12002) — self-revision turns binary rewards into dense supervision; adjacent polarity-aware mechanism.
- **SkillRL** (Xia et al., arXiv:2602.08234) — recursive skill-augmented RL for agents; related skill-library construction.
- **Trace2Skill** (Ni et al., arXiv:2603.25158) — trajectory-to-skill distillation; directly relevant to cold-start bank construction.

## Related

- [[_overview]]
- [[opsd-compresses-rlvr]]
- [[rlt-followups-2026]]
- [[co-evolving-policy-distillation]]
- [[sakana-rlt]]
- [[../self-improvement/_overview]]
- [[../rlvr-mechanics/deepseekmath-grpo]]
- [[../rlvr-mechanics/_overview]]
- [[../synthesis/concept-curriculum-method]]
- [[../single-sample-rl-finetuning/_overview]]
- [[../weekly-briefs/2026-05-30]] — brought in by the 2026-05-30 weekly sweep
