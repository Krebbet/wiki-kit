# Reverse-KL Distillation: Statistical Guarantees and Limits (Liu, Wei, Zimmert)

Purely theoretical paper (no experiments) giving minimax sample-complexity bounds for sequence-level reverse-KL policy distillation under student misspecification. Four settings: (online vs offline trajectories) x (full-distribution vs action-probability-only teacher feedback). Main results: full feedback gives a tight $O(B(L^* + \log(|\Pi|/\delta)/T))$ rate; standard exact-refit objectives (DAgger-style, local reverse KL as in on-policy distillation, forward KL, clipped KL) can provably fail from visitation mismatch; online action-only feedback pays an extra $\min\{|A|,|\Pi|,e^{B_\infty}\}$ factor; offline teacher-trajectory distillation attains the optimal $\Theta(B_\infty)$ rate even with action-only feedback.

Source note: summary-based ingest; appendices (proofs, Lemma D.1, Prop 4.3 details) were not read.

## Method

- **Setting:** reward-free finite-horizon MDP, finite student class $\Pi$, teacher $\pi^*$. Target risk $L(\pi)=\mathrm{KL}(P^\pi \,\|\, P^{\pi^*})$ over trajectory distributions. $L^*$ = best-in-class risk (misspecification).
- **Algorithm 1 (online, full feedback):** policy-space learning over $\Pi$ with trajectory loss and importance-ratio clipping; each prefix loss is reweighted by $\min\{1, P^\pi(\xi_h)/P^\pi_t(\xi_h)\}$, so prefixes a candidate rarely visits are downweighted.
- **Algorithm 2 / Eq. (12):** offline learning via Hellinger-to-reverse-KL reduction under the likelihood-ratio bound $P^\pi(\tau)\le e^{B_\infty}P^{\pi^*}(\tau)$.
- **Assumption (online):** relative second moment $\mathbb{E}[(\sum_h \mathrm{KL}_h)^2]\le B\,\mathbb{E}[\sum_h \mathrm{KL}_h]$. Lemma D.1: the likelihood-ratio bound implies it with $B=4(B_\infty+1)$.

## Results / claims

| Setting | Estimation cost | Source |
|---|---|---|
| Online, full feedback | $\Theta(B)$ | Thm 3.2 (upper), 3.3 (tight) |
| Offline, full feedback | $\Theta(B)$ | Thm 3.3 |
| Offline, action-only | $\Theta(B_\infty)$ | Eq. (12), Table 1 |
| Online, action-only | extra factor $\min\{\lvert A\rvert,\lvert\Pi\rvert,e^{B_\infty}\}$, even realizable | Thm 3.5 |

- **Thm 3.2:** $L(\hat\pi)\le O(B(L^*+\log(|\Pi|/\delta)/T))$.
- **Thm 3.3:** $C_{est}=\Theta(B)$; any learner with $C_{est}=O(B)$ needs $C_{app}=\Omega(B)$ (approximation-estimation tradeoff is unavoidable). Holds online and offline.
- **Prop 3.1 (failure of exact refits):** DAgger-style, local reverse-KL (on-policy distillation), forward KL, mixtures, clipped KL, any trajectory subset or weighting. On an $H=2$, $|\Pi|=2$ instance the final policy has risk $\Omega(B)$ after $T=\Theta(B^3)$ episodes with constant probability, despite $L^*\le e^{-\Omega(B)}$. Cause: visitation mismatch, the good policy looks bad on states only the bad policy visits.
- **Online vs offline action-only:** offline can need exponentially fewer episodes in the worst case.

## Relation to thesis

- **Formal grounding for the OPD cluster.** Gives the first sample-complexity framing for full-logit vs sampled-token feedback, which the empirical pages ([[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]], [[research/teacher-student-rl/one-shot-opd]]) treat only empirically. On-policy distillation (GKD, Thinking Machines) uses teacher probability only on student-sampled actions, the statistically weaker action-only regime online.
- **Not single-sample.** No few-sample claim; the value is quantifying how many trajectories are needed and when richer teacher feedback (full logits) substitutes for sampling. Suggests one-shot OPD gains are bounded by what the student's own visitation distribution can expose, a hint for choosing the single example (cover states the student would reach).
- **Mode-seeking asymmetry.** Reverse KL tolerates capacity-limited students, the same asymmetry as the I-projection argument in [[research/rlvr-mechanics/binary-rewards-rl-challenges]].
- **Concept learning:** no evidence either way. It is a distribution-matching result, not concept acquisition vs pattern matching. Contrast [[research/teacher-student-rl/opd-skill-vs-knowledge-transfer]]: that page concerns what transfers, this one how much data is needed.
- **Offline design relevance:** the offline-matches-optimal result bears on semi-offline rollout designs ([[research/teacher-student-rl/semi-opd-offline-student-rollouts]]).
- **Complements gradient-level diagnoses:** this paper locates failure in visitation mismatch of local-loss refits; [[research/teacher-student-rl/mopd-gradient-diagnosis]] and [[research/teacher-student-rl/ier-gradient-reliability-opd]] diagnose the optimisation/signal-reliability side.

## Limitations

- **Stated:** finite policy class, discrete states, tabular-style assumptions; algorithms computationally inefficient (efficient learners left as future work); no empirical test of prefix reweighting/clipping; results concern exact refitting, not the gradient steps used in practice.
- **Unstated:** $B$, $B_\infty$ can be exponential in $H$ for LLM-length sequences, so bounds may be vacuous; absence of an explicit $H$ factor is not horizon-independence. LLM state space is not enumerable. The likelihood-ratio assumption (teacher covers every student trajectory) is unverifiable for LLMs. Reward-free only; no verifier-reward mixing as in RLVR+OPD pipelines. Prop 3.1 is an adversarial 2-policy construction, so it says little about typical failure rates.

## Conflict notes

- **Soft tension:** offline teacher-trajectory distillation can match the optimal rate while online action-only feedback can be exponentially worse. This sits against any on-policy-superiority framing in [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]] and [[research/teacher-student-rl/_overview]] (not verified here what those pages claim). Thm 3.5 is worst-case under strong assumptions with no LLM experiments: a tension to note, not a refutation.
- **Soft qualification:** Prop 3.1 (local reverse-KL refits can provably fail) qualifies the empirical-success framing of OPD pages; no direct contradiction.

## Source

- `raw/research/weekly-2026-10-23/01-reverse-kl-distillation-guarantees.md`
- arXiv:2610.30844 (Liu, Wei, Zimmert)

## Related

- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]] — empirical KL-direction / on- vs off-policy comparison this formalises
- [[research/teacher-student-rl/_overview]] — theory anchor for the OPD cluster
- [[research/teacher-student-rl/semi-opd-offline-student-rollouts]] — offline-vs-online result bears on semi-offline designs
- [[research/teacher-student-rl/mopd-gradient-diagnosis]] — gradient-side failure vs visitation-mismatch failure
- [[research/teacher-student-rl/ier-gradient-reliability-opd]] — OPD signal reliability vs information limits of action-only feedback
- [[research/teacher-student-rl/one-shot-opd]] — one-shot empirics read against these bounds
- [[research/teacher-student-rl/opd-skill-vs-knowledge-transfer]] — what transfers vs how much data is needed
- [[research/rlvr-mechanics/binary-rewards-rl-challenges]] — shared forward/reverse-KL asymmetry
- [[../weekly-briefs/2026-10-23]] — brought in by the 2026-10-23 weekly sweep
