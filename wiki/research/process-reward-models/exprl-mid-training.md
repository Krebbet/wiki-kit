---
name: exprl-mid-training
description: RL-based mid-training that hides reference solutions from the policy, using them only to build LLM-judge grading rubrics for dense outcome/process rewards; better primes subsequent sparse-reward RL than SFT, sparse GRPO, or self-distillation. Setlur co-authorship links to PAV's process-advantage lineage.
type: research
---

# ExpRL: Exploratory RL for LLM Mid-Training

Xiang, Setlur, Blagden, Haber, Kumar, arXiv:2606.17024. ExpRL is a mid-training stage sitting between SFT and standard sparse-reward RLVR: the policy samples on-policy rollouts from the bare problem prompt (reference solution never shown to the actor), and an LLM judge scores each rollout against the *hidden* reference under a fixed rubric, producing a dense reward used for a first on-policy RL phase. The primed policy then goes into ordinary sparse-reward GRPO. The core move is treating reference solutions as **reward scaffolds**, not imitation targets — contrasted directly against SFT-on-references (catastrophic) and self-distillation (a co-trained reference-conditioned teacher, off-policy-target unstable).

## Method

Two stages.

**Stage I (ExpRL mid-training).** Policy samples rollouts from the bare prompt; a judge (a copy of the base model, e.g. Qwen3-4B-Instruct) compares each rollout to the hidden reference under a fixed rubric, outputs a 5-point Likert score $\tilde s \in \{1..5\}$, mapped to $s = (\tilde s - 1)/4 \in [0,1]$. The judge is instructed to *verify, not solve* — no filling gaps, no correcting errors; unsupported rubric items score as absent.

- **ExpRL-Outcome** — dense reward $s(x,y,y^\star)$ on the full rollout, GRPO-style group-normalized update.
- **ExpRL-Process** — judge re-scores prefixes $\{y_{\le t}\}$ (split on the model's own `###` step delimiter) to get $s_t = s(x, y_{\le t}, y^\star)$, converted to centered segment advantages:

$$A_t(x,y) = \begin{cases} s_t - s_{t-1}, & t > 1 \\ s_1 - s_T, & t = 1 \end{cases} \tag{Eq. 2}$$

REINFORCE update (Eq. 1, token-level advantage), no group normalization — an ablation (App. A.2) over three centering schemes shows the choice barely matters. Objective (Eq. 3): $\max_\theta \mathbb{E}[R(x,y,y^\star)] - \beta\,\mathrm{KL}(\pi_\theta\|\pi_0)$, $R$ = outcome or process dense reward.

**Stage II (downstream RL).** Initialize from the Stage-I policy, continue with standard *sparse binary outcome* GRPO — reference info fully removed. Only the initialization differs from a vanilla sparse-RL run.

## Claims

On Qwen3-4B-Instruct-2507, after Stage-II sparse RL (Table 1):

| Benchmark | GRPO (no priming) | ExpRL-Outcome | ExpRL-Process |
|---|---|---|---|
| AIME25 | 56.0 | 59.1 | 58.1 |
| AIME26 | 58.75 | 61.7 | **63.4** |
| HMMT-Nov25 | 42.9 | 49.1 | 48.1 |
| IMO-AnswerBench | 35.3 | 37.9 | 35.7 |

Both ExpRL variants beat SFT (26.6–30.3% AIME), sparse GRPO, and self-distillation on every benchmark but IMO-AnswerBench (smallest/most mixed gain of the four). Stage-I *alone*, before any Stage-II RL (Table 2), already lifts pass@1 and pass@16 over base and all baselines except mixed IMO-AnswerBench results. **SFT on the same references catastrophically collapses** pass@1 relative to base — AIME25 46.46% → 6.00%. A mixed-domain 8B-policy + 4B-judge run (Table 4) shows ExpRL-Outcome improving every pass@1 eval (math/science/coding) except LiveCodeBench specifically, where sparse GRPO stays stronger (execution gives a native sparse reward there — see Limitations).

## Concept-learning evidence

Frames the goal as broadening coverage over *composed* solution strategies, not just primitive skills in isolation ("knowing how to check local computations does not mean the model can identify the right case split"). Evidence for genuine behavioral change over narrow reward-hacking: (1) pass@k curves shift up at low-to-moderate $k$; (2) an LLM-judged (Claude Sonnet 4) 21-field behavioral taxonomy (12 solution archetypes + 9 reasoning behaviors, Fig. 9) shows net gains in verification, self-correction, backtracking, and exploration relative to base, while SFT *loses* verification behavior and sparse GRPO changes behavior less; (3) entropy dynamics — sparse GRPO collapses entropy fastest (mode-seeking), ExpRL and self-distillation retain higher token-level entropy, consistent with maintained solution-strategy diversity. Authors explicitly caveat that self-distillation *also* gains several behaviors yet still underperforms ExpRL — behavioral coverage alone isn't sufficient; both behavioral and problem-specific-knowledge coverage matter.

## RL connection

Fully on-policy throughout Stage I (ExpRL-Process specifically needs fully on-policy updates; ExpRL-Outcome tolerates up to one-step off-policy). Reward is dense and LLM-judge-derived, not from the environment/verifier, KL-regularized to $\pi_0$. Contrasted directly with self-distillation (Hübotter et al.): the self-distillation teacher, conditioned on the reference, starts far outside the KL ball of the base policy (Fig. 4), causing the off-policy-target instability that ExpRL avoids by keeping the reference out of the policy's *sampling* path entirely — the reference shapes reward, never sampling.

## Sample efficiency

Not single-sample — a corpus-scale mid-training method (440 InT + 1076 POPE math examples in the main run; +1474 SciKnow +1011 LCB v6 = 4001 total in the mixed-domain run; 10 rollouts/prompt, batch 36/32, 230 Stage-I + 500 Stage-II steps). Relevant to the wiki's thesis mainly as a contrast point: this needs a large reference-solution corpus, and treats references as reward scaffolds rather than few-shot training data per se.

## Failure modes / limitations (authors' own)

- Requires reference solutions to exist at all — not available in every domain.
- **Coding is the clean exception.** Execution gives a strong native sparse reward there; reference-scaffolded judging is a weak substitute (incomplete code doesn't compile; valid implementations diverge stylistically from the reference). A calibration test (Table 6) shows the LiveCodeBench judge is essentially reference-agnostic (misplacement rates ~8–10% regardless of reference correctness) — it's inferring functional correctness directly, not using the scaffold, unlike math where a wrong reference pushes misplacement to ~50% (Table 5).
- Judge must be "minimally capable" — a 0.6B judge is unstable/uninformative regardless of reference condition; 4B+ judges show real discrimination. Judge need not match policy scale (a 4B judge scores an 8B policy fine).
- ExpRL-Process interacts badly with length clipping: under clipping, `###` step-delimiter counts collapse toward 0–1 per rollout — shown (no-clip ablation) to be an artifact of the length-clip penalty, not of process rewards per se. Flagged as an open implementation issue.
- Authors explicitly state Stage-I rewards "need not be perfectly accurate ... as long as they encourage exploration" — reward-hacking/misspecification risk acknowledged but not bounded beyond the one calibration study.

## Cited leads for follow-up

- **POPE (Qu, Setlur, Smith, Salakhutdinov, Kumar, arXiv:2601.18779)** — exposes oracle reference *prefixes* to the policy during downstream RL; contrasted directly with ExpRL, which never exposes references to the actor. Half of ExpRL's math corpus comes from POPE.
- **InT (Yang, Bai, Wu, Yang, Setlur, Kumar, arXiv:2601.14209)** — "self-proposed interventions"; other half of the prompt corpus; source of the "SFT on unfamiliar references disrupts reasoning" citation.
- **RL via self-distillation (Hübotter et al., arXiv:2601.20802)** — the self-distillation baseline.
- **Zhang, Neubig, Yue, "On the interplay of pre-training, mid-training, and RL" (arXiv:2512.07783)** — directly on-topic for the mid-training question generally.

## Source

- `raw/research/weekly-2026-08-14/02-exprl-mid-training.md`

## Related

- [[_overview]]
- [[pav-rewarding-progress]] — **authorship lineage**: Amrith Setlur co-authors both PAV (process-advantage under a complementary *prover policy*) and ExpRL (process-advantage under an LLM-judge rubric scored against a *hidden reference*). Same "process advantage" concept, two different reward-construction mechanisms — a trained prover vs. a reference-conditioned judge.
- [[rredcot]] — parallel: both build dense/process reward from a bank of reference solutions without training a separate reward model; contrasted mechanisms (importance-sampling return-decomposition vs. LLM-judge Likert scoring).
- [[../curriculum-and-decomposition/scrl-curriculum-credit-assignment]] — same "use reference solutions structurally, not as imitation targets" principle, different mechanism (subproblem decomposition vs. rubric scoring).
- [[../curriculum-and-decomposition/adaback-adaptive-rationale]] — opposite end of the reference-exposure spectrum: AdaBack *reveals* partial reference prefixes as hints on failure; ExpRL keeps references fully hidden and uses them only to shape reward.
- [[../self-play/invisible-leash]] — flagged, not asserted, tension: Theorem C.1 bounds $\limsup_k \mathrm{pass@}k_{\pi_\theta} \le \limsup_k \mathrm{pass@}k_q$ under on-policy RL. ExpRL Stage-I is fully on-policy yet reports finite-$k$ pass@16 gains over base purely from denser reward shaping — plausibly consistent (reweighting mass toward rare-but-already-supported paths, not expanding support), but worth checking against Invisible-Leash's precise statement before treating as settled.
- [[../catastrophic-forgetting/rft-mitigates-forgetting]] — corroborating data point at unusually large magnitude: SFT-on-references collapses AIME25 pass@1 from 46.46% to 6.00%, while RL-based methods preserve/improve it.
- [[../teacher-student-rl/_overview]] — same "privileged reference info shapes reward, never exposed as an imitation target" axis as the RLT lineage, except the "teacher" here is a judge scoring against the answer rather than a co-trained policy.
- [[../../weekly-briefs/2026-08-14]] — brought in by the 2026-08-14 weekly sweep
