# Finetuning with Sampling (SFT Learns Better Than You Think)

arXiv:2610.02140 (Karan, Chen, Du; Harvard, Oct 2026). Projection sampling is a Metropolis-Hastings procedure that rewrites off-policy expert traces so they are more likely under the base model while staying correct. Plain SFT on the rewritten data matches or beats on-policy RL and self-distillation (OPSD) on new-task accuracy and on retention of prior capabilities in most settings. The SFT loss is untouched and only the data distribution is reshaped. The one-time cost is on the data side. OPSD still wins on some tasks (medical, Olmo chemistry), and prior-capability retention on medical stays well below base.

## Method

- Objective unchanged; data reshaped. Target is the information projection p_C = argmin_{pi in P_C} KL(pi || p), i.e. the base model p restricted to trajectories "equivalent" to the expert's (Prop. 1, Csiszar 1975). Equivalence means a correct final answer for math/science, and the same factual content per an LLM grader for medical.
- Sampler: MH initialized at the expert trace. The proposal kappa_C is information-preserving (Prop. 2): pick a random index, truncate, and have the base model continue the partial trace with the expert solution in context ("continue in your own words... consistent with expert solution").
- Prop. 3: KL(pi_{k+1} || p) is non-increasing in MCMC steps (data-processing inequality), so sampling compute is a scaling axis.
- Block-wise progressive sampling is adapted from power sampling (Karan & Du 2025, arXiv:2510.14901). Settings: B=32, T=1856, N_MCMC=10. Data-side cost is about |D|*N*T^2/(4B) tokens.
- Practical approximation (App. C.2): accept whenever the candidate has higher likelihood than the current trace. This skips the second forward pass for the transition probability.
- Training is standard SFT (AdamW, cosine schedule; grid over epochs {1,2}, lr {5e-5,1e-5,5e-6}, bs {16,32,64}; medical up to 6 epochs). Expert traces: GPT-5 (chemistry), MATH solutions (math), HuatuoGPT-o1 (medical).

## Results

Qwen2.5-7B-Instruct, chemistry (SciKnowEval L-3, 1800 train / 600 test):
- New-task accuracy: base 0.343, SFT 0.618, Rewrite-SFT 0.613, OPSD 0.618, Sampling-SFT 0.660 (+31.7 pts over base, +4.2 over OPSD).
- Prior-capability average (MMLU/GPQA/AMC/MATH500/GSM8K): base 0.597, SFT 0.520, Rewrite 0.558, OPSD 0.568, Sampling-SFT 0.586 (about -1.1 pts). MMLU fully retained (0.692 vs 0.687).

Qwen2.5-3B, math (MATH L3-5; baselines GRPO, UFT, OPSD, SFT):
- Base MATH(3,4,5) 0.315; vanilla SFT drops across the board.
- Sampling-SFT: +18.0 MATH(3,4,5), +14.4 AMC, +20.3 GSM8K, +33.7 MATH500 (beats best RL baseline by +26.9 on MATH500).
- Sampling-SFT+GRPO is best overall: MATH500 +40.7, GSM8K +25.1, approaching 7B-Instruct.

Caveats where Sampling-SFT does not win:
- **Medical** (Qwen2.5-7B-Instruct, 1000 held-out, GPT-5-mini grader): base 0.353, Sampling-SFT 0.458, **OPSD 0.466** (OPSD wins). Prior-capability average: Sampling-SFT 0.516 vs vanilla SFT 0.353 (recovers a 16.3-pt loss), but **base is 0.597**, so retention is best among the fine-tuned variants and still well below base.
- **Olmo-3-7B-Instruct chemistry**: base 0.328, Sampling-SFT 0.583, **OPSD 0.597** (OPSD wins), SFT 0.567. Prior-capability average 0.617 vs base 0.601, so no net forgetting here.

Analysis:
- Boosted traces have much higher base-model log-likelihood (Fig. 3).
- pass@k on Olmo chemistry stays above both base and OPSD at large k (Fig. 4), which the authors read as learning beyond sharpening. Some eval problems go from 0% to 67.2% / 53.1% pass rate.
- More MCMC steps (0 to 10) give lower KL and higher accuracy (Fig. 5).
- Boosted data keeps 93.9-95.9% correctness (App. C.1).
- Boosted data is model-specific (App. B). Boosting with Olmo and training Qwen on it gives 57.3% chemistry, worse than vanilla SFT (61.8%). A 50/50 mix gives 62.1%.

## Applicability

- Any SFT-from-stronger-teacher pipeline where forgetting or poor generalization is a concern: domain adaptation, distillation traces, and hard problems where GRPO gets no signal.
- Prerequisites: a base model that follows the in-context "continue in your own words" prompt, a correctness check (verifier or LLM grader), and extra inference compute for the rewrite.
- Re-run per base model, since the data is model-specific.
- Tested only at 3B-7B. One-time data cost, cheap relative to RL.
- Authors suggest on-policy distillation teacher shaping and simulated rollouts for hard-sample RL as extensions.

## Novelty/caveats

- Refinement/recombination. It reuses the MH power-sampling machinery with a different target (information projection onto the expert-equivalent set), applied at train time instead of inference time. Adds a formal KL-monotonicity result.
- Closest prior work: PoPE and UFT (expert hints in RL rollouts), OPSD (privileged-context self-distillation) and Anchored SFT (modify the SFT loss). The change here is to leave the loss alone and shape the data.
- Challenges the "SFT memorizes, RL generalizes" / "RL's Razor" framing. There is possible tension with [[reasonmaxxer]] and [[rlvr-incentivizes-reasoning]] (RL as sparse selection vs capability learning), given the "beyond sharpening" claim. No conflict ruling made.
- Not uniformly dominant: OPSD wins on medical and Olmo chemistry, and medical retention is below base. Reliance on the likelihood-swap approximation and a small N_MCMC=10 is disclosed.

## Reproducibility

Code: github.com/aakaran/finetuning-with-sampling (plus a project website). Weights not mentioned. Models are open (Qwen2.5, Olmo-3), but expert traces (GPT-5) and the medical grader (GPT-5-mini) are API-dependent. Compute: H100/H200. Baseline hyperparameters are tuned or defaulted per prior papers. Preprint, under review; no independent reproduction or adoption evidence yet.

## Source

- `raw/research/weekly-2026-10-03/02-sft-with-sampling.md` (arXiv:2610.02140)

## Related

- [[anti-self-distillation]] — OPSD baseline critique; OPSD is this paper's main baseline, beaten on chemistry/math but not medical
- [[negative-self-distillation]] — OPD/OPSD cluster sibling
- [[rlsd-self-distilled-rlvr]] — OPSD cluster sibling
- [[u-opsd-unsupervised-self-distillation]] — OPSD cluster sibling
- [[dopd-dual-on-policy-distillation]] — OPD sibling; the paper proposes using its sampler to shape distillation teachers
- [[flux-opd]] — OPD cluster sibling
- [[one-shot-opd-data-efficiency]] — data-side analysis, parallel concern with data coverage
- [[reasonmaxxer]] — RL as sparse policy selection; contrasts with the "beyond sharpening" claim
- [[rlvr-incentivizes-reasoning]] — pass@k framing parallels Fig. 4
- [[es-solution-coverage]] — pass@k coverage argument
- [[rl-teachers]] — shaping teacher traces for student learnability; closest conceptual sibling
- [[seal-self-adapting]] — model-generated finetuning data
- [[evolution-fine-tuning]] — SFT on expert trajectories to add capability
- [[watchlist]] — likely holds the prior power-sampling paper (arXiv:2510.14901)
