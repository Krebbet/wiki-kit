# Scaling Near-Optimal SFT–RL Annotation Budget Allocation from Small to Large LLMs

Wang, Verma, Lin, Liu, Chen, Rus, Low (NUS / SMART / A*STAR / MIT; arXiv:2609.01573) study how to split a fixed post-training annotation budget between supervised fine-tuning (SFT) and a subsequent RL stage. Their core move is to stop chasing a single optimal split ratio $r^*$ and instead characterize the $\varepsilon$-near-optimal *region* $R_\varepsilon$ — the set of allocation ratios within a performance tolerance $\varepsilon$ of peak. They find this region is wide even at small tolerances, widens with model scale, and transfers reliably from small proxy models to large target models, yielding a practical recipe that avoids exhaustive grid search at target scale.

## Method

Given a pretrained model $M_N$ of size $N$ and a fixed annotation budget $B$ (measured in samples, with SFT and RL assumed to have comparable per-sample annotation cost as a baseline), an allocation ratio $r \in [0,1]$ sends $rB$ samples to SFT and $(1-r)B$ to a subsequent RL stage; SFT always precedes RL. Rather than the point optimum $r^*(N,B) = \arg\max_r P(N,r,B)$, the paper defines the $\varepsilon$-near-optimal region:

$$R_\varepsilon(N,B) = \{r \in [0,1] : P(N,r,B) \geq (1-\varepsilon)\max_{r'} P(N,r',B)\}$$

estimated on a discrete 5-point allocation grid $G = \{0, 0.25, 0.5, 0.75, 1\}$ (a 9-point grid gives qualitatively consistent results, App. E.1). Two width estimators are reported: range width $w_\varepsilon^{rng}$ (span of the convex hull on $[0,1]$) and count width $w_\varepsilon^{cnt}$ (fraction of grid points that are near-optimal); these largely agree, and per-ratio hit-rate heatmaps confirm $R_\varepsilon$ is generally contiguous.

To quantify whether a region found cheaply on a small model still holds at scale, they define an asymmetric cross-scale transfer metric:

$$T_\varepsilon(N_s \to N_t; B) = \frac{|\hat R_\varepsilon(N_s,B) \cap \hat R_\varepsilon(N_t,B)|}{|\hat R_\varepsilon(N_s,B)|}$$

measuring how much of a small-proxy region $N_s$ survives at a larger target $N_t$.

This produces a practical **3-step proxy-sweep recipe** (Sec. 3.5): (1) run the 5-point ratio grid on the smallest model in the target family, at the target budget $B$; (2) pick a tolerance $\varepsilon \in [5\%, 10\%]$ (the range found reliable across all tested families/tasks/budgets); (3) take the resulting near-optimal region $[\min \hat R_\varepsilon, \max \hat R_\varepsilon]$ from the proxy sweep and select its **midpoint** as the ratio for the target model (favored over the boundary or the exact proxy point-optimum because it is least sensitive to small shifts between the proxy's and target's regions; snap to the nearest evaluated grid point if needed).

Experiments span Llama 3, Qwen 2.5, and Qwen 3 (up to 14B params) across four tasks (math/GSM8K, instruction-following/IFEval, summarization/Reddit TL;DR–ROUGE-L, helpfulness/HelpSteer2), using both off-policy DPO and on-policy GRPO as the RL stage, and LoRA throughout for tractability.

## Claims

- Under 10% tolerance, most tasks admit near-optimal ratios covering **55–75% of the feasible allocation space** — a wide plateau, not a sharp single optimum.
- The near-optimal region **widens with model scale** (up to the 14B ceiling tested, across Llama 3, Qwen 2.5, Qwen 3).
- Near-optimal regions **transfer far more reliably across scales than the exact point optimum**; point-optimum transfer is "sometimes high but inconsistent," notably for Qwen 2.5.
- The proxy-sweep recipe (small-model sweep → midpoint of the transferred region) hits the target model's tolerance in **94.3% of cases at $\varepsilon=5\%$** and **97.1% at $\varepsilon=10\%$**, validated on existing 1B–8B runs across all 4 tasks and both Llama/Qwen2.5 families.
- Findings hold for both off-policy (DPO) and on-policy (GRPO) RL stages, and persist under heterogeneous SFT/RL annotation costs (cost ratio $\rho = c_{SFT}/c_{DPO} \in \{1,2,5,10\}$) — the region widens further as SFT becomes relatively more expensive, giving practitioners more slack in the split when SFT annotation is the costlier stage.

## Sample efficiency

The budgets studied are far larger than this wiki's regime: $B$ ranges up to roughly 15–20k annotated samples per task (GSM8K: ~7.5K SFT + ~16.6K synthetic preference pairs; HelpSteer2: ~20K; GRPO-IFeval: ~15K). Critically, **the authors explicitly exclude budgets below $B < 5k$ from their scaling analysis**, describing performance in that regime as "noisy and occasionally non-monotonic," and restrict all reported scaling/transfer statistics to $B \geq 5k$ (consistent with standard practice of excluding pre-convergence points from scaling-law analysis).

**This paper's machinery is validated only for $B \geq 5k$ samples.** Its near-optimal-region width, scale-widening, and cross-scale transfer claims should NOT be assumed to extend down to the wiki's single-sample ($N=1$) or few-shot regime — that regime sits inside the band the paper itself flags as unreliable and out of scope. The paper's contribution to sample efficiency is about reducing *search cost* (a small proxy sweep replaces exhaustive grid search at target scale), not about reducing the *total annotation budget* itself — it is a budget-allocation paper, not a data-efficiency paper in the wiki's sense.

## Relevance to the project

This is directly on-thesis for data-efficient fine-tuning in the broad sense (annotation-budget framing for post-training), but the scope boundary above matters: the wiki's core single-sample thesis operates at the opposite end of the budget axis this paper studies, in exactly the regime ($B < 5k$, and specifically $N=1$) the authors exclude as noisy/non-monotonic.

It is also orthogonal, not conflicting, with [[../synthesis/fine-tuning-best-practices]]'s existing "SFT → RLVR → optional OPSD" *ordering* rule. That page makes a qualitative claim about stage order; this paper adds a quantitative *budget ratio* axis (how much of a fixed budget to give each stage) without touching ordering — SFT always precedes RL in both. The two findings are complementary rather than in tension.

## Limitations

**Acknowledged by the authors:**
- All experiments are in-distribution (train and eval on the same task distribution); OOD transfer (general instruction/preference mix → held-out task) is untested and, per cited work on broken/inverse scaling, likely to scale less reliably.
- Model scale ceiling of 14B (Llama-3-70B, Qwen2.5-32B–72B deferred to future work); budget ceiling ~15–20K samples, near the public-corpus limit for several tasks — extrapolation to frontier scale/budget is unverified.
- Restricted RL algorithm set: only DPO and GRPO; PPO and SimPO untested.
- Cost model is simplistic — ignores training compute, GPU time, and experimental-search cost; budget is annotation-sample-count only (justified by an argument that annotation cost dominates compute by 3–5 orders of magnitude vs. human annotation, a smaller but still favorable margin vs. cheap synthetic annotation).

**Notable self-hedge:** the headline "region widens with scale" finding is explicitly caveated by the authors as possibly a **fixed-tolerance mechanical artifact** — larger models achieve higher absolute peak performance, so under a fixed *relative* tolerance $\varepsilon$ there is mechanically more absolute slack, which could admit more ratios into $R_\varepsilon$ without allocation sensitivity itself having changed. Appendix E.6 reportedly finds edge cases where the widening fails under an alternative tolerance definition. One additional apparent exception: Qwen 2.5 summarization narrows marginally at larger scale under high tolerance, attributed to saturation (the small model already has a wide region) rather than a real reversal.

**Unstated:** no concept-learning or generalization/compositionality evidence is offered anywhere in the paper — the dependent variable throughout is task performance (accuracy, ROUGE-L, reward-model score), not evidence of concept acquisition vs. pattern matching.

## Source

- `raw/research/weekly-2026-09-04/05-sft-rl-annotation-budget-allocation.md`
- arXiv: https://arxiv.org/abs/2609.01573

## Related

- [[limited-data-ft-survey]] — both operate on annotation-budget framing under constrained label counts; this paper's budget range sits inside that survey's regime, a budget-allocation companion to its PEFT/domain-adaptation budget map.
- [[../synthesis/fine-tuning-best-practices]] — adds a complementary quantitative budget-ratio axis to that page's qualitative SFT→RLVR ordering rule; consider proposing this as an extension (do not edit that page directly — just note it here for the user).
- [[../single-sample-rl-finetuning/_overview]] — scope-boundary note: this paper explicitly excludes budgets below 5k samples as "noisy/non-monotonic," which is exactly the wiki's core single-sample regime — its near-optimal-region claims should not be assumed to hold at $N=1$.
- [[../../weekly-briefs/2026-09-04]] — brought in by the 2026-09-04 weekly sweep.
