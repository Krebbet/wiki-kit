# uPRM — Unsupervised Process Reward Models

uPRM (Gadetsky et al., EPFL, arXiv:2605.10158) trains a process reward model with **zero step annotations and no ground-truth final answers**, using only a frozen general-purpose LLM's next-token probabilities over interleaved correctness markers as a self-derived training signal. It matches supervised PRMs on Best-of-8 math (avg 60.1 vs sPRM 60.0, Math-Shepherd-7B 60.4, Skywork-7B 60.8) despite zero annotation cost, beats LLM-as-a-Judge on ProcessBench error localisation by up to 15 F1, and — the load-bearing finding for this wiki — is **substantially more robust to reward hacking** when used as an RL reward than a supervised PRM.

## Source
- [`raw/research/weekly-2026-05-17/02-unsupervised-process-reward-models.md`](../../../raw/research/weekly-2026-05-17/02-unsupervised-process-reward-models.md) — captured 2026-05-17 (arXiv:2605.10158)

## Method

For a trajectory $\tau = (x, y_1, \ldots, y_T)$, a candidate first-error position $j$ is scored by building an interleaved sequence $\mathbf{s}(\tau, j) = [x, y_1, +, \ldots, y_{j-1}, +, y_j, -]$ (Eq. 4) and reading a frozen LLM's (Qwen2.5-14B-Instruct) next-token probabilities for the "+"/"-" markers. Single-trajectory score (Eq. 6):

$$\mathcal{S}(j; \mathbf{s}) := \mathbb{1}[j \le T]\cdot\log p_j^- + \sum_{t<j}\log p_t^+$$

A batch of $N$ trajectories is **concatenated and jointly scored** (Eq. 7–8), exploiting in-context learning so the LLM's per-step judgments mutually calibrate. The PRM $r_\theta$ is LoRA (rank 64) + a 2-layer MLP over special-token hidden states of the same backbone (Eq. 9–11), trained to maximise the entropy-regularised expected joint score (Eq. 12) via a REINFORCE-style actor-critic estimator (Eq. 18). Trajectory packing fixes total reasoning steps per batch (80) rather than trajectory count, stabilising SNR. A corner-collapse correction (Eq. 13, App. A) prevents the joint score degenerating when all $j_n$ land in the same category. Training corpus: PRM800K trajectories **with their labels discarded** — only the reasoning text is used. ~5.5 h on 8×H200 (vs ~4.25 h for the supervised SFT baseline) — overhead negligible against the eliminated annotation cost.

## Results

| Axis | uPRM | Supervised / judge baseline |
|---|---|---|
| ProcessBench F1 (GSM8K/MATH/Olympiad/Omni) | 58.3 / 52.6 / 42.7 / 39.8 | LLM-as-Judge 49.8 / 42.8 / 29.4 / 26.6 |
| Best-of-8 (MATH-500/Minerva/Olympiad avg) | 60.1 | sPRM 60.0; MathShepherd-7B 60.4; Skywork-7B 60.8 |
| TTS Best-of-256, Llama-3.2-1B | 14.6% → **31.7%** | — |
| RL (PURE/RLOO), Qwen2.5-Math-7B MATH-500 | **82.9 ± 0.4** | VR-only 80.1 ± 0.8 |

Reward-hacking robustness: a supervised PRM collapses in <50 RL iterations on Qwen2.5-Math-7B; uPRM completes training on the same model without RH.

## Where it sits in the wiki

- Adds a **fully unsupervised track** to the PRM taxonomy in [[_overview]], distinct from supervised ([[lets-verify-step-by-step]] PRM800K), automated-MC ([[math-shepherd]], needs ground-truth answers), and prover-progress ([[pav-rewarding-progress]]) supervision. uPRM requires *neither* step labels *nor* final answers.
- Mechanistically a decoding-time read: extracting attribute scores from frozen-LLM next-token probabilities mirrors GeDi/FUDGE in [[../decoding-time-steering/_overview]] — another instance of the "information is already in the model" theme.
- A label-free process-reward sibling of [[../rlvr-mechanics/learning-to-think]] (Fisher/SVD information-gain) — same goal, different signal source.
- Structurally a self-training method (signal derived from the model itself) → relevant to [[../self-improvement/_overview]] and an unsupervised verifier candidate for [[../synthesis/test-time-scaling]].
- Candidate dense, zero-annotation reward for the $R_w$ component in [[../synthesis/proposed-method]].

## Is this just LLM-as-a-Judge?

The training signal does originate from a frozen general-purpose LLM judging step correctness, so the *source* is judge-flavoured — and the paper benchmarks against an explicit LLM-as-a-Judge baseline. But uPRM is not LLM-as-a-Judge ([[../critique-self-correction/prometheus-2]] direct/pairwise evaluator; [[../self-improvement/self-rewarding-lm]] judge-on-own-outputs) in the operative sense. Five differences:

1. **Amortised, not per-call.** The deployed reward is a *trained* PRM $r_\theta$ (LoRA + MLP, Eq. 9–11); the frozen LLM is only the training signal. A judge re-queries the LLM at every scoring call.
2. **Probability read, not verdict generation.** The signal is the frozen LLM's next-token probabilities over "+"/"-" markers (Eq. 4, 6) — a decoding-time attribute extraction (GeDi/FUDGE-like, see §Where it sits), not a generated judgment.
3. **Joint in-context calibration.** $N$ trajectories are concatenated and jointly scored (Eq. 7–8) so per-step judgments mutually calibrate — structurally unlike independent per-item judging.
4. **No labels and no final answers.** Distinct PRM-taxonomy track vs supervised ([[lets-verify-step-by-step]]) and automated-MC ([[math-shepherd]], needs ground-truth answers).
5. **RL-reward-hacking robust.** The operative differentiator: a supervised PRM collapses <50 RL iters on Qwen2.5-Math-7B; uPRM does not (§Results). A vanilla judge reward is notoriously hackable. uPRM also *beats* LLM-as-a-Judge on ProcessBench localisation by up to ~15 F1 — outperforming it on the judge's own task.

Crisp framing: LLM-as-a-Judge = *use the model's verdict*; uPRM = *read the model's marker-probability distribution, jointly calibrate it, distil it into a cheap stable trained PRM that survives as an RL reward*. The residual judge-like risk is recorded in §Limitations #5 (single-backbone self-training, no ground-truth correction).

## Conflict / open tension

uPRM §5.3 claims Qwen2.5-Math models train to completion on uPRM-only rewards with no RH — a meaningful **weakening** of the "RH is inevitable with PRM-only rewards" position (Cheng et al., PURE — not yet in wiki). Authors partly reconcile: it is "less frequent and less severe," not eliminated, and the Qwen2.5-7B *base* model still succumbs. Not a clean source-vs-wiki contradiction (PURE isn't on the wiki yet), so recorded here rather than as a conflict file; connects to [[../rlvr-mechanics/binary-rewards-rl-challenges]] — uPRM's softer distributional reward avoids the near-Dirac collapse mode Dymetman formalises. **Follow-up lead:** capture PURE (Cheng et al. — min-form credit assignment) and Razin et al. NeurIPS 2025 ("most accurate RM ≠ best teacher").

## Limitations

1. Joint scoring needs a long-context-capable scoring LLM (decouplable from the PRM backbone).
2. Does not eliminate RH — only delays/softens it; Qwen2.5-7B base still hacks.
3. ProcessBench localisation lags the best supervised PRMs (authors argue downstream utility doesn't need perfect localisation — cites Razin et al.).
4. Math-only; correctness-marker approach untested on open-ended tasks.
5. **Unstated:** self-training from one backbone amplifies its blind spots with no ground-truth correction.

## Related
- [[_overview]] — PRM taxonomy; uPRM is the unsupervised / annotation-free track
- [[math-shepherd]] — automated-label sibling (still needs ground-truth answers; uPRM does not)
- [[lets-verify-step-by-step]] — PRM800K, the labelled corpus uPRM uses unlabelled
- [[pav-rewarding-progress]] — prover-progress label-free sibling (different signal source)
- [[../rlvr-mechanics/learning-to-think]] — label-free process reward via Fisher/SVD; parallel goal
- [[../rlvr-mechanics/binary-rewards-rl-challenges]] — softer reward avoids near-Dirac RH collapse
- [[../self-improvement/_overview]] — uPRM as self-training
- [[../self-improvement/self-rewarding-lm]] — LLM-as-judge-on-own-outputs; contrast in §"Is this just LLM-as-a-Judge?"
- [[../critique-self-correction/prometheus-2]] — canonical evaluator-LM (LLM-as-Judge); contrast in §"Is this just LLM-as-a-Judge?"
- [[../decoding-time-steering/_overview]] — next-token-probability read; "info already in the model"
- [[../synthesis/test-time-scaling]] — unsupervised verifier for Best-of-N / DVTS
- [[../synthesis/proposed-method]] — zero-annotation dense reward candidate for $R_w$
- [[../../weekly-briefs/2026-05-17]] — brought in by the 2026-05-17 weekly sweep
