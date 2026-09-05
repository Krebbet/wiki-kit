# Does On-Policy Distillation Really Distill? From Noisy Teacher to Self-Improvement

Yi Ding and Ruqi Zhang, Purdue University, arXiv:2608.31046. The paper first shows that on-policy distillation's (OPD) teacher supervision is noisy — and gets noisier as the teacher gets larger — yet the student is essentially insensitive to that noise, converging to the same performance whether noisy supervision is kept or removed. Digging into why, the authors find OPD's learning signal concentrates almost entirely on tokens where the student already assigns low probability; a single fixed negative advantage on those tokens, with no teacher at all, matches full OPD. The plain-language claim: OPD isn't distilling teacher behavior so much as sharpening the student's own distribution by suppressing its low-confidence tail. They turn this diagnosis into a method, On-Policy Self-Adaptation (OPSA) — a fully supervision-free, entropy-adaptive negative-advantage objective — that outperforms OPD, GRPO, TTRL, and OPSD baselines while using no teacher, no verifier, and no ground-truth answer.

## Method

**Diagnostic setup.** Standard OPD reward/advantage is the reverse-KL sampled-token ($k_1$) estimator: $A_i = \log(\pi_t(y_i)/\pi_s(y_i))$ (Eq. 1–2), where $\pi_t$ is the teacher and $\pi_s$ the student, evaluated on student-sampled trajectories. The logit-level gradient of the OPD loss (Eq. 3) vanishes whenever $|A_i|$ is small or the sampled token's student-probability approaches 1 — this motivates checking where, empirically, the advantage mass actually lives.

Empirically: teacher-supervision noise (advantage sign disagreeing with what a verifier/ground-truth would assign) rises with teacher scale — 30.6% at 4B, 34.7% at 30B-A3B, 50.6% at 235B-A22B, with the largest teacher assigning a *negative* advantage to 97.8% of tokens inside correct final answers. Training on noisy-only, clean-only, or all trajectories converges to comparable AIME24 accuracy (Fig. 2b) — the student doesn't care. Separately, token-level advantage mass is concentrated near zero (29.2% exactly 0, 51.7% below $10^{-4}$) and correlates with high student-log-probability tokens; restricting training to high-logp tokens gives no gain even with randomly assigned advantages (Fig. 3c). Restricting to the lowest-20%-logp tokens with a single fixed advantage $A=-0.5$ reproduces standard OPD's gains (Fig. 4); flipping the sign to $A=+0.2$ causes collapse.

**OPSA objective.** Given this, OPSA drops the teacher entirely. For each response, select the 20% of student-sampled tokens with lowest log-probability ($\mathrm{Slowest20}$). Assign each an entropy-adaptive negative advantage, scaled by where the token's local entropy $H_i$ falls relative to the min/max entropy within that response's low-logp set:

$$r_i = 2\frac{H_i - H_{min}}{H_{max}-H_{min}} - 1 \qquad \text{(Eq. 4)}$$

$$A_i^{dyn} = -\tfrac{1}{2} - \tfrac{\delta}{4}\, r_i \qquad \text{(Eq. 5, } \delta=1\text{)}$$

$$\mathcal{L}_{OPSA} = -\mathbb{E}\Big[\tfrac{1}{|\mathrm{Slowest20}|}\sum_{i\in \mathrm{Slowest20}} A_i^{dyn}\, \log\pi_\theta(y_i \mid x; y_{<i})\Big]$$

Higher-entropy low-logp tokens ("fork" positions) get a stronger (more negative) advantage than low-entropy low-logp tokens. No teacher model, no verifiable reward, no ground-truth/hint — inputs are only the student's own rollouts, log-probabilities, and entropies. Implemented in the `slime` framework on Qwen3/Qwen3.5, 8×H100/H200; ~500 training steps in the main results.

Mechanistically (Sec 4.3, Fig. 6/9), OPSA suppresses tail tokens specifically at high-entropy fork positions while *redistributing* — not collapsing — probability mass among head tokens there, which the authors argue preserves output diversity (Jaccard-distance analysis, Fig. 9) and Pass@k while sharpening confidently-predicted low-entropy positions. This is tied to increased frequency of "reflective" tokens (wait / but / alternatively) and longer, more accurate chain-of-thought (Fig. 7).

## Claims

- **Magnitude of gain (vs base Qwen3-1.7B):** +35.41 pts Avg@32 on AIME24 (263% relative), +25.62 / +17.60 pts on AIME25 / HMMT25 (264% / 307% relative), and more than 2× Pass@32 on all three math benchmarks.
- **Vs standard OPD:** +16.77 pts Avg@32 on AIME24 (48.85 vs 32.08).
- **Vs GRPO / TTRL / OPD / OPSD (Table 3, Qwen3-1.7B):** OPSA wins on every reported metric, averaging +11.04 pts Avg@32 and +8.89 pts Pass@32 over the best baseline — with zero external supervision (Table 1: OPSA is the only method in the comparison satisfying dense-signal + no-verifiable-reward + no-external-teacher + no-hint simultaneously).
- **Model-scale generalization:** holds on Qwen3-4B and Qwen3.5-9B (base 76.35 Avg@32 pushed to 87.81).
- **Domain transfer:** trained only on math (DAPO-17k, labels/answers withheld), OPSA improves out-of-domain on MBPP+ (code) and GPQA-Diamond (QA).
- **Sign matters, not just magnitude:** a *positive* fixed advantage on the same low-logp tokens causes policy collapse — response length collapses toward 0, gradient norm explodes, output degenerates (Fig. 4).
- **Selection ratio is not fully robust:** 20% is close to optimal among {20,30,40}%, but 10% underperforms — over-sharpens the distribution and causes entropy collapse (Fig. 10), contrary to the paper's own framing of "low sensitivity."
- **Fork-token dependence:** masking high-entropy "fork" tokens (identified via a hand-built reflective-word head set) largely eliminates OPSA's gains (Fig. 8) — the benefit is concentrated in this narrow, hand-identified token category.

## Sample efficiency

Not single-sample. OPSA is an on-policy RL method trained over the full DAPO-17k question set (~17k math problems, ~500 training steps in the reported figures). The distinctive supervision-reduction is not "fewer labeled examples" but *zero labels or verification signal of any kind* — no ground-truth answer, no verifier, no teacher logits — replaced entirely by intrinsic entropy/log-probability statistics computed from the student's own rollouts. This is a stronger reduction along the supervision axis than most sample-efficiency methods in this wiki, which typically reduce example count while retaining a correctness signal; OPSA instead removes the correctness signal while retaining full-dataset scale.

## Relevance to the project

This paper is best read as a *mechanistic critique* of the pattern-transfer story that [[opd-dual-nature-generalization]] tells about OPD, and it lands in direct tension with it (see conflict below). It also extends the wiki's data-curation-axis findings: OPD-dual-nature already showed teacher-unsolved problems are equally useful to teacher-solved ones (difficulty-insensitivity); this paper pushes that further by showing the *teacher itself* — noisy or absent — barely matters, only the student's own low-confidence tokens do. That reframes "what is OPD's information content" from "teacher-transmitted behavior" to "student self-calibration," a materially different design implication for any single-sample/concept-learning method built on the OPD family: if this diagnosis generalizes, an OPD-style scaffold's value may lie less in the specific exemplar/teacher chosen than in providing any signal that identifies the student's uncertain tokens.

The entropy-adaptive negative-advantage mechanism is structurally parallel to [[../rlvr-mechanics/high-entropy-minority-tokens]]'s entropy-selects-tokens finding, but inverted in role: that page's RLVR result uses entropy to *select which tokens* carry gradient; OPSA uses log-probability to select tokens first (bottom-20%) and entropy only to *scale the magnitude* of an already-fixed-sign advantage among those tokens. Worth tracking as two different roles entropy can play in credit assignment within the same broader token-selective-RL cluster (also touching [[../rlvr-mechanics/rethinking-rl-sparse-selection]]'s "gains concentrate in a small fixed token subset" narrative).

## Limitations

- Fixed-sign requirement is brittle: positive advantage on the same token selection collapses the policy — the method's benefit is a sign convention, not something a naive "penalize uncertainty" framing would robustly discover.
- Token-selection ratio is not actually low-sensitivity across the full range tested (10% underperforms, causing entropy collapse); the paper's claim of robustness among {20,30,40}% understates this.
- Noise/mechanism analysis restricted to tokens inside `\boxed{}` answer spans, since no per-token reference exists for intermediate-reasoning-step correctness — an explicitly flagged measurement limitation, meaning the "OPD doesn't distill" diagnosis is only directly verified for answer-span tokens.
- Tested only on the Qwen3/Qwen3.5 family; the calibration constants ($A_{fix}=-3/4$, 20% ratio) are not shown to transfer to other model families or non-reasoning tasks.
- TTRL and self-consistency-style label-free baselines are shown to collapse Pass@k by sharpening toward a self-consistent (possibly wrong) mode; OPSA is contrasted favorably, but the same self-referential-signal risk is not fully ruled out for OPSA — only not empirically observed here.
- Masking hand-identified "fork" tokens eliminates most of the gain (Fig. 8), meaning generalization of the fork-token concept beyond math CoT (where reflective words like "wait"/"but" are a strong marker) is untested.
- Contemporaneous work the authors cite (Xie et al. 2026; Fu et al. 2026; Hou et al. 2026; Xu et al. 2026; Xing et al. 2026) addresses the same OPD noise/token-selection problem while *retaining* the teacher — this paper does not empirically compare against that retain-the-teacher line, only contrasts philosophically.

## Source

- `raw/research/weekly-2026-09-04/01-opsa-does-opd-really-distill.md`
- arXiv: https://arxiv.org/abs/2608.31046

## Related

- [[opd-dual-nature-generalization]] — direct tension: this paper argues OPD's gains come from suppressing low-logp student tokens, an operation requiring no teacher at all, while opd-dual-nature-generalization argues same-origin vs cross-origin teacher/student pairs generalize differently, which only makes sense if the teacher's specific behavioral content/identity is actually what's transferred. See [[../../conflicts/opsa-vs-opd-pattern-transfer]].
- [[opdvr-verifiable-reward]] — sibling sampled-token-OPD-repair method; complementary diagnosis of the same estimator defect (unreliable off-policy teacher advantage), but OPDVR keeps and calibrates the teacher signal rather than removing it.
- [[gc-opd-group-calibrated]] — both address unreliable teacher advantage signal (noise growing with context/scale); this paper's more radical response is to remove the teacher entirely rather than calibrate it.
- [[rlt-followups-2026]] — landscape-tracking page for the OPD lineage; this is a new 2026 entry extending it.
- [[../rlvr-mechanics/high-entropy-minority-tokens]] — structurally parallel entropy-selective mechanism, but entropy plays a different role (token *selection* there vs advantage *magnitude scaling* here, after logp-based selection).
- [[../../weekly-briefs/2026-09-04]] — brought in by the 2026-09-04 weekly sweep.
