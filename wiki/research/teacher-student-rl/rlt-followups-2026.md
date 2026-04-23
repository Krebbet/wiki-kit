---
name: rlt-followups-2026
description: Post-RLT landscape (Q4-2025 through Q2-2026) — the dense teacher-side signal paradigm exploding as On-Policy Distillation (OPD), self-distillation with privileged info (OPSD, SDPO, SDFT, G-OPD), explanatory probes (ExGRPO), and systematic log-prob rewards (Kwiatkowski). None directly cites Sakana RLT; all are siblings in the same family. Commercial adoption at Qwen3/MiMo/GLM-5.
type: research
---

# Follow-ups and Adoption Around RLT (2025-06 → 2026-04)

Ten months after [[sakana-rlt]] (Cetin, Zhao, Tang; arXiv:2506.08388, June 2025), the landscape around "teacher-generated signal, student-side likelihood reward" has become crowded — but not via direct citation of RLT. Every major follow-up captured here descends from the sibling line of *On-Policy Distillation* (OPD, Agarwal 2023) rather than from RLT's explanation-as-CoT framing. They converge on the same core insight (dense teacher-side signal > sparse outcome reward) from a different angle.

**Finding.** Among the captured 2026 sources — Kwiatkowski et al. (Meta FAIR/UvA), Tan et al. ExGRPO (ASU/UVA/UNC), Li et al. *Rethinking OPD* (Tsinghua et al.), Zhao et al. OPSD (UCLA/HKU/Meta), Thinking Machines Lab, and Amy Sheng's OPD survey — **none directly cites Sakana's RLT paper**. Grep over the captured PDFs and web pages returns zero hits for "Sakana", "Cetin", or "2506.08388". RLT is thus being developed in parallel with rather than extended by the mainstream dense-distillation line. *(synthesis)*

## Summary table

| Source | Signal to student | Teacher sees answer? | Direct RLT descendant? | Venue |
|---|---|---|---|---|
| [[sakana-rlt]] (Cetin, Zhao, Tang, 2025-06) | Student $\log \pi_s(s\mid q, t_o)$ on teacher think-tokens | **Yes** — (Q, A) → teacher | — | arXiv:2506.08388 |
| Kwiatkowski et al. (2026) | Student $\log \pi_\theta(a^\star\mid p, z)$ on its own CoT | No (self, with reference) | No citation; same reward formula | arXiv:2602.03979 (Meta FAIR + UvA) |
| ExGRPO (Tan et al., 2026) | GRPO on student's answer to *explanatory probes* | — (probes derived from Q, A, R) | No citation; inverted direction | arXiv:2603.19266 (ASU/UVA/UNC) |
| OPSD (Zhao et al., 2026) | Per-token reverse-KL to a privileged "teacher" policy | **Yes** — teacher = same model + solution | No citation; paradigmatically closest | arXiv:2601.18734 (UCLA/HKU/Meta) |
| Rethinking OPD (Li et al., 2026-04) | Teacher $\log \pi_T(\cdot\mid x, \hat y_{<t})$ at student-visited states | No | No citation; mechanism study of OPD | arXiv:2604.13016 (Tsinghua et al.) |
| Thinking Machines Lab (2025-10) | Per-token reverse-KL to a frozen teacher | No | No citation; industry replication of Qwen3 OPD | thinkingmachines.ai blog |
| OPD Survey (Sheng, 2026-02) | — (survey) | — | — | amysheng-ai.github.io blog |

## Per-source notes (source-traceable)

### 1. Kwiatkowski et al. — *Likelihood-Based Reward Designs for General LLM Reasoning* (arXiv:2602.03979, Meta FAIR + Univ. of Amsterdam)

First comprehensive study of probability-based rewards for CoT fine-tuning across verifiable (MATH, DeepScaleR) and non-verifiable (Alpaca, NuminaMath-proof) settings, spanning Qwen-2.5 and Llama-3.2. Compares SFT, RLOO, and four reward variants: probability (VeriFree), average per-token probability (RLPR-style), log-probability, average log-probability, plus a geometric-mean perplexity variant (NOVER) and JEPO's ELBO loss. The log-probability reward is defined as $R(z, a) = \log \pi_\theta(a^\star \mid p, z)$ — one transformer pass over the reference answer, no sampling of $a$ required.

Headline claim: "Among the variants tested, rewards based on log-probabilities perform well in every scenario (short, verifiable answers and long, non-verifiable answers), while all others fail in one or several settings." Log-prob rewards lead to CoT shortening (recovers on verifiable; does not recover on non-verifiable — there it degenerates toward SFT). Probability rewards (VeriFree) collapse on long-form due to vanishing probabilities.

**Relation to RLT** *(synthesis)*: the reward formula $\log \pi_\theta(a^\star\mid p, z)$ is structurally identical to RLT's $r^{SS}_i = \text{avg}\{\log \pi_s(s_i\mid t_{o_i}, q_i)\}$ — only that here $\pi_\theta$ is the same model generating both $z$ and scoring $a^\star$, rather than a separate frozen student. No separate teacher; the CoT $z$ is self-generated. RLT is not cited despite using the same core reward shape.

Source: `../../../raw/research/rlt-followups/06-01-kwiatkowski-likelihood-rewards.md`

### 2. Tan et al. — *Probing to Refine: Reinforcement Distillation of LLMs via Explanatory Inversion* / ExGRPO (arXiv:2603.19266, ASU/UVA/UNC)

Addresses the "reversal curse" and superficial pattern memorisation in distilled models. Two components: *Explanatory Inversion* (EI) generates "explanatory probes" — new (Q, R, A) triples produced by a teacher that require articulating the logic behind the original answer; *Explanatory GRPO* (ExGRPO) runs RL with a *Dialogue Structure Utility Bonus* rewarding coherent reasoning across these probes.

Quantitative claim: Gemma-7b student, 12 datasets, average +20.39% over zero-shot and +6.02% over SoTA distillation baselines; surpasses vanilla fine-tuning with 10–25% of the training data.

**Relation to RLT** *(synthesis)*: RLT inverts the information flow one way (teacher gets A, student doesn't); ExGRPO inverts it the other way (probes that give the student A, test whether it can reconstruct the logic). Both target "conceptual understanding vs pattern memorisation" under dense RL. RLT is not cited.

Source: `../../../raw/research/rlt-followups/04-02-probing-to-refine-exgrpo.md`

### 3. Li et al. — *Rethinking On-Policy Distillation: Phenomenology, Mechanism, and Recipe* (arXiv:2604.13016, Tsinghua + ShanghaiTech + UIUC + Renmin, April 2026)

Phenomenology + mechanism + recipe study of OPD. The paper's own opening claim is the strongest *commercial-adoption* data point in the captured corpus: "Recent industry efforts, including Qwen3 [Yang et al., 2025], MiMo [Xiao et al., 2026] and GLM-5 [Zeng et al., 2026], all adopt OPD in their post-training pipelines and report substantial gains."

Key findings:
- **Two governing conditions for successful OPD.** (i) *Thinking-pattern consistency*: student and teacher must share compatible top-$k$ distributions; mismatched patterns produce low initial overlap that training cannot recover. (ii) *Higher scores ≠ new knowledge*: a stronger teacher can still fail if it does not provide information beyond what the student has already seen.
- **Token-level mechanism.** Successful OPD is signatured by progressive alignment on high-probability overlap tokens at student-visited states; the shared top-$k$ tokens concentrate 97–99% of combined probability mass; restricting supervision to overlap tokens alone matches full top-$k$ performance.
- **Recipe.** (i) *Off-policy cold start* — warmup SFT on teacher rollouts to raise initial overlap; (ii) *teacher-aligned prompt selection* — prompts drawn from the teacher's post-training data, mixed with OOD prompts to preserve entropy.
- **Cost of density.** Reward quality degrades with trajectory depth; instability originates at later tokens and propagates backward. "A larger teacher may induce a reward landscape that is locally flat around the student's policy, making token-level gradients ineffective despite an informative global signal." Flags limitation for long-horizon reasoning and agentic settings.

**Relation to RLT** *(synthesis)*: The failure-mode analysis is structurally important for RLT too — RLT's $r^{SS}$ reward is *student-side* log-prob (same flavour as the overlap-token signal here), and the "locally flat reward around student's policy" failure could apply when the teacher think-tokens are too distributionally far from the student's priors. RLT's $r^{KL}$ regulariser is one possible answer to this failure mode (forcing think-tokens to remain plausible from the student's no-solution view). Not cited.

Source: `../../../raw/research/rlt-followups/05-03-rethinking-opd.md`

### 4. Zhao et al. — *Self-Distilled Reasoner: On-Policy Self-Distillation (OPSD)* (arXiv:2601.18734, UCLA + HKU + Meta)

Single LLM acts as both teacher and student with different *contexts*. Teacher policy conditions on privileged information (verified reasoning traces); student policy conditions only on the question; training minimises per-token reverse-KL between the two distributions over the student's own rollouts. No separate teacher model. Ground-truth solutions in the dataset are used as the privileged information — a capability RLT pioneered for separate-teacher-student, now collapsed to self-distillation.

Claims: 4–8× token efficiency over GRPO RLVR on mathematical reasoning; superior to off-policy distillation.

**Relation to RLT** *(synthesis)*: paradigmatically the closest captured follow-up. RLT gives the teacher (a separate model) the (Q, A) pair; OPSD gives the same model, playing the teacher role, the (Q, R*, A) privileged context. Both use privileged information on the teacher side to produce a dense student-side training signal. OPSD trades RLT's separate 7B teacher (expensive) for a same-model teacher (cheaper). RLT's reward is the student's log-prob of the solution given teacher think-tokens; OPSD's is per-token reverse-KL to the privileged policy's distribution. RLT is not cited.

Source: `../../../raw/research/rlt-followups/03-04-opsd-self-distilled-reasoner.md`

### 5. Thinking Machines Lab — *On-Policy Distillation* (Oct 2025, blog)

Production-oriented writeup of OPD. Core method: per-token reverse KL between student and frozen teacher on student-generated trajectories. Industry-relevant claims:
- Replicates Qwen3's OPD recipe via the Tinker API at "a fraction the cost of RL" — the blog's central comparison frame.
- Reverse KL is "unhackable" (low KL implies high probability of teacher-approved behaviour); mode-seeking; reduces exposure bias.
- No separate reward model needed; single forward pass from the teacher for per-token log-probs; student generates with the smaller, cheaper model.
- Demonstrates the approach on math reasoning and assistant-style domain+instruction tasks.

**Relation to RLT** *(synthesis)*: This is the mainline industry adoption of the "dense teacher-side signal" paradigm, but not of RLT's explanation-as-CoT framing. The teacher is a fixed stronger model whose token-level distribution is the reward; the teacher is *not* optimised. In RLT terms, this corresponds to the inner loop only, with a pre-trained teacher substituted for an RL-trained one. RLT is not cited.

Source: `../../../raw/research/rlt-followups/01-05-thinking-machines-opd.md`

### 6. Amy Sheng — *On-Policy Distillation Research Survey 2026* (Feb 2026, blog)

Survey summary of the OPD landscape. Claims relevant to this wiki (source-traceable to the survey):
- Positions Agarwal et al. 2023 (GKD, ICLR 2024, arXiv:2306.13649) as the foundational OPD work.
- **Self-distillation wave (2026):** SDFT (Shenfeld et al., arXiv:2601.19897) for continual learning, SDPO (Hübotter et al., arXiv:2601.20802) for self-distillation from textual feedback, OPSD (Zhao et al., arXiv:2601.18734) for privileged-info self-distillation.
- **G-OPD (Yang et al., arXiv:2602.12125, Renmin University).** Theoretical unification: OPD is a special case of dense KL-constrained RL with teacher's log-prob as dense reward and KL penalty at unit weight. *ExOPD* extrapolates the reward scaling factor (optimal in 1.5–3 range) and claims students can **surpass** teacher performance — breaking the teacher ceiling. Demonstrated on GSM8K and HumanEval.
- Claims Thinking Machines' AIME'24 result: 70% accuracy at 1/10th RL cost.
- Repeated framing: **OPD = dense KL-constrained RL**.

**Note** *(editorial)*: the survey itself is a practitioner blog, not peer-reviewed. Arxiv IDs for cited papers (e.g., 2602.12125 for G-OPD) should be re-verified before citing downstream; this wiki captures them as survey-reported references, not direct reads.

Source: `../../../raw/research/rlt-followups/02-06-opd-survey-2026.md`

## Commercial / industry adoption evidence

*(synthesis — compiled from the captured sources)*

**RLT itself.** Sakana released `SakanaAI/RLT-7B` on Hugging Face (see [[sakana-rlt]] source links); the captured sources provide no evidence of downstream commercial deployment of the model or of RLT's *(Q, A)-to-teacher* training recipe inside a shipped product line. Absence of direct citation suggests the reference-in-prompt framing has not (yet) been widely adopted. *(editorial)*

**OPD (sibling paradigm).** Three production model families are explicitly named by *Rethinking OPD* as having adopted OPD in their post-training pipelines:
- **Qwen3** (Alibaba; Yang et al., 2505.09388)
- **MiMo** (Xiao et al., 2026 — cited by *Rethinking OPD*)
- **GLM-5** (Zhipu; Zeng et al., 2026 — cited by *Rethinking OPD*)

Plus **Thinking Machines Lab's Tinker API** replicating the Qwen3 recipe. These use dense per-token teacher log-probs as reward; none uses RLT's teacher-with-solution-in-prompt framing, based on the captured sources.

## Cross-source themes

*(synthesis)*

1. **The dense teacher-side signal is the common factor.** RLT, OPD, OPSD, ExGRPO, Kwiatkowski's log-prob rewards all collapse to "give the student a dense, log-prob-flavoured reward against a reference, rather than 0/1 outcome". The axes that distinguish them:
   - *Source of the signal*: separate model (RLT, TM Lab OPD, Rethinking OPD) vs same model conditioned on privileged info (OPSD, SDPO, SDFT) vs reference answer in the dataset (Kwiatkowski).
   - *Is the teacher trained?*: yes (RLT) vs no (TM Lab, Qwen3 recipe, most OPD).
   - *What does the teacher see?*: question + answer (RLT, OPSD) vs question only (most OPD).
   - *Granularity*: per-token distribution matching (OPD) vs sequence-level log-prob of reference (RLT, Kwiatkowski).

2. **Self-distillation is the 2026 efficiency story.** The teacher-ceiling and separate-teacher costs that *Rethinking OPD* documents as failure modes are sidestepped by making the teacher the same model under a privileged context (OPSD, SDFT, SDPO, G-OPD). This directly targets a limitation the RLT paper flagged for itself: "RLT requires a separate student model at every gradient step (expensive)."

3. **"Reference-solution as privileged info" is being rediscovered from multiple angles.** RLT puts the solution in the teacher's prompt (2025-06). OPSD conditions the teacher on verified reasoning traces (2026-01). SDFT uses in-context demonstrations as the privileged signal (2026-01). All three are the same structural move: give *something* extra to the "teacher" role that the student doesn't see at inference, then distill on student-visited states.

4. **Teacher-strength paradoxes are reported independently.** *Rethinking OPD* shows a stronger teacher can completely fail a student while a weaker teacher succeeds, under thinking-pattern mismatch; G-OPD's ExOPD argues the student can *surpass* a weaker teacher via reward extrapolation. Both are opposite sides of "teacher-student capability gap matters". RLT's own ablation (reward correlates $r=0.89$ with student gain; the 7B teacher beats 670B teachers) is a third data point that the same family of questions gets answered differently depending on the specific reward.

## Open questions exposed by the follow-up landscape

*(editorial)*

- **Why has RLT's reference-in-prompt framing not been picked up?** Two hypotheses: (a) the extra KL regulariser and separate-student cost are too expensive vs. self-distillation alternatives like OPSD; (b) the OPD line was already the default in Qwen3/MiMo/GLM-5 before RLT landed, so the mainstream had a working recipe. The captured sources do not adjudicate. An honest read is that RLT has not accrued direct citations in ten months despite the paradigm being healthy.
- **Does RLT's $r^{KL}$ plausibility term solve *Rethinking OPD*'s "flat-reward-around-student" failure mode?** Plausibly yes — the KL regulariser forces teacher think-tokens to remain under the student's no-solution distribution, which is exactly the overlap-token condition *Rethinking OPD* identifies as necessary. Untested empirically in any captured source.
- **For the project's "reference-textbook in prompt" setting, is OPSD the natural drop-in?** OPSD collapses the two-model requirement and uses verified traces as privileged info. Closer to the project's target than RLT's two-model setup. Would warrant its own [[../teacher-student-rl/opsd-self-distilled-reasoner]] entry if the project moves in this direction.
- **Does ExOPD-style "surpass the teacher" generalise to RLT-style explanations?** ExOPD reports that scaling the reward weight above 1 lets the student beat the teacher. RLT's reward is sequence-level log-prob, not per-token KL — whether the same scaling trick applies is unknown.

## Source

- `../../../raw/research/rlt-followups/01-05-thinking-machines-opd.md` — Thinking Machines Lab *On-Policy Distillation* blog, Oct 2025
- `../../../raw/research/rlt-followups/02-06-opd-survey-2026.md` — Amy Sheng *OPD Research Survey 2026*, Feb 2026
- `../../../raw/research/rlt-followups/03-04-opsd-self-distilled-reasoner.md` — Zhao et al., *On-Policy Self-Distillation (OPSD)*, arXiv:2601.18734
- `../../../raw/research/rlt-followups/04-02-probing-to-refine-exgrpo.md` — Tan et al., *Probing to Refine / ExGRPO*, arXiv:2603.19266
- `../../../raw/research/rlt-followups/05-03-rethinking-opd.md` — Li et al., *Rethinking On-Policy Distillation*, arXiv:2604.13016 (April 2026)
- `../../../raw/research/rlt-followups/06-01-kwiatkowski-likelihood-rewards.md` — Kwiatkowski et al. *Likelihood-Based Reward Designs*, arXiv:2602.03979 (Meta FAIR + UvA)

## Related

- [[sakana-rlt]] — the method this page tracks follow-ups for
- [[_overview]] — teacher-student RL theme overview
- [[../rlvr-mechanics/deepseekmath-grpo]] — base optimiser shared across OPD/RLT/OPSD
- [[../process-reward-models/_overview]] — dense-vs-sparse reward lineage
- [[../self-improvement/_overview]] — STaR and self-improvement parallels; SDFT/SDPO extend this line
- [[../synthesis/proposed-method]] — project roadmap; OPSD is a candidate cheaper substitute for RLT in the P3 reward slot
