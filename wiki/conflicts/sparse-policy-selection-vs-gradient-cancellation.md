# Sparse Policy Selection vs Token-Gradient Cancellation

**Status:** open. Positions A+B+C captured 2026-05-11; Position D added 2026-06-03; Position E added 2026-06-06.

## Position A — RL touches ~1–4% of tokens; the rest is inert

**Source:** [[reasonmaxxer]] (USC / DEVCOM ARL, arXiv:2605.06241, May 2026).

**Claim:** RL post-training's beneficial token footprint is a *sparse, predictable correction concentrated at high-entropy decision points*. Across four base/RL pairs (Qwen2.5-1.5B/7B, Qwen3-4B; GRPO/PPO/RLOO):

- SHIFTED positions (teacher prefers token outside base top-5): **≈ 0%** in all pairs.
- RERANKED positions (teacher reorders inside base top-5): **1.0–4.1%**.
- Mean rank of teacher's promoted token: **2.14–2.39** (always shallow, never deep).
- The entropy at reranked positions is **5–12× higher** than at unchanged positions.

**Basis (causal):** Oracle intervention — replace only the reranked positions in deterministic base-generation with the teacher's preferred token → **fully reproduces teacher pass@1**. Replace with random top-20 tokens → no improvement. This rules out the alternative explanation that RL distributes corrections across many positions in aggregate.

**Implication:** ReasonMaxxer (entropy-gated contrastive FT on 50 problems, single GPU, minutes) matches or exceeds full RL across 3 model families × 6 scales × 6 math benchmarks at **3 orders of magnitude lower cost** ($4–$25 vs $200–$103,000). The correction is representable in a rank-32 LoRA (0.27–0.49% of parameters).

## Position B — Gradient cancellation across many shared tokens is the bottleneck

**Source:** [[token-gradient-cancellation]] (Alibaba / Tsinghua, DFPO line).

**Claim:** Stable GRPO-style RL requires "gradient exchangeability" — shared / template tokens must cancel across trajectories within a group. GSPO (sequence-coupled multiplicative-weight GRPO) is structurally non-cancelling and degrades at scale. DFPO (Min-Replace or Adv-Orthogonal stop-gradient transforms) restores cancellation.

**Basis:** +5.6 / +6.9 / +5.6 pp avg@32 (AIME25 / LiveCodeBench v6 / HMMT25) over GSPO at Qwen3-32B; gain *grows with group size* — the diagnostic that "many shared tokens carrying meaningful gradient that fails to cancel" is the failure mode.

**Implicit premise (this is what Position A contradicts):** the relevant design space is the full token distribution and the bottleneck is how gradient is distributed across it. ReasonMaxxer's finding that **~97% of token positions carry no causal RL signal** undermines this: if those positions are inert anyway, fixing their cancellation isn't load-bearing — and the gain DFPO shows comes from a different mechanism (perhaps the sparse 1–4% positions getting cleaner updates as a side effect).

## Position C — most tokens aren't inert, they're actively harmful (discriminator view)

**Source:** [[delta-token-credit]] (DelTA, arXiv:2605.21467, 2026-05-25).

**Claim:** view a GRPO/DAPO update as a *discriminator* separating higher- from lower-reward responses. Shared / formatting tokens dominate *both* side-wise centroids and **dilute the rarer directions that actually separate higher-reward responses** (§3.1). The fix is a per-token discriminative-contrast coefficient λ that reweights the surrogate toward reward-separating tokens.

**Basis / new datapoint:** a hard top/bottom λ-split token-selection experiment on Qwen3-8B-Base — **top-50% λ tokens beat full-token DAPO; bottom-50% λ tokens *actively collapse* training** (§5.2, Figs 3–4). Headline +3.26 / +2.62 pp over baselines.

**How it cuts across A and B:**
- *Agrees with Position A (sparse):* only a subset of tokens carries the load; λ is a mechanistic account of *which* — high discriminative contrast, complementary to (not identical with) ReasonMaxxer's high-entropy criterion.
- *Agrees with Position B (cancellation):* "shared/formatting tokens dominate the centroids" is a discriminator-space restatement of the gradient-cancellation pathology — the same shared-token problem in different math.
- *Beyond both:* Position A treats the ~97% as **inert** and Position B treats shared tokens as merely needing to **cancel to zero**; DelTA's bottom-λ-collapses-training result says a large fraction of tokens is **net-negative**, not neutral. The remedy differs accordingly — surrogate *reweighting* (DelTA) vs gradient *orthogonalization* (DFPO) vs entropy-gated subset *selection* (ReasonMaxxer): three distinct fixes for one underlying "most tokens shouldn't be updated equally" observation.

## Position D — reward signal is partially or wholly spurious; clipping bias drives gains

**Source:** [[spurious-rewards-rlvr]] (arXiv:2506.10947, June 2025).

**Claim:** GRPO training with random or negatively-correlated rewards still yields +21.4 pp MATH-500 on Qwen2.5-Math-7B (vs. +29.1 pp from real rewards). The gain does not come from learning the reward signal. It comes from a clipping bias in GRPO's PPO surrogate that systematically amplifies behaviors already present in the base model's pretrained distribution — the clip term pushes high-prior behaviors further regardless of reward label.

**Basis:** Three reward conditions (ground-truth, random, negatively-correlated) × two model families (Qwen, Llama3/OLMo2). Qwen2.5-Math-7B gains under random rewards; Llama3 and OLMo2 do not. Case study: "code reasoning" frequency (65% → >90%) rises under spurious rewards — it is a high-prior Qwen behavior being amplified, not a learned reward response.

**Implication:** A significant fraction of reported Qwen-family RLVR results may reflect clipping-driven amplification of pretrained behaviors, not genuine policy improvement from reward learning. RLVR benchmarks cannot be attributed to reward-signal learning without a spurious-reward ablation across model families.

**How it cuts across A, B, and C:**
- *Contradicts Position A:* Position A (ReasonMaxxer) frames RL as selecting better policy choices from meaningful signal at 1–4% of tokens. Position D says the signal can be noise and gains still appear — undermining the premise that RL is discovering genuinely better choices.
- *Contradicts Position B:* Position B (DFPO) attributes gains to gradient exchangeability; if reward correctness is irrelevant, fixing cancellation cannot be the primary mechanism either.
- *Consistent with Position C flavor:* DelTA's discriminator view implies shared tokens are net-negative; Position D is consistent if the "amplifiable behaviors" are driven primarily by the few high-discriminator tokens anyway — but Position D doesn't require token-level analysis; clipping operates at the trajectory level.

**Critical caveat:** Model-family-dependent. Effect requires a base model with amplifiable high-prior behaviors (Qwen2.5-Math has them; Llama3/OLMo2 do not). Position D may co-exist with Positions A/B/C in model families where spurious rewards produce no gain.

## Position E — Standard Pass@K is confounded; RLVR genuinely improves CoT quality (metric-validity argument)

**Source:** [[rlvr-incentivizes-reasoning]] (Microsoft Research Asia / PKU / CUHK / UCLA, arXiv:2506.14245, June 2025).

**Claim:** The "sampling efficiency only" result (Yue et al., 2025 and related work) relies on standard Pass@K, which is **confounded on math benchmarks** because base LLMs can guess correct short integer answers with incorrect CoTs. The CoT-Pass@K metric (Pass@K conditioned on LLM-verified chain correctness) reveals a **persistent RLVR advantage at all K up to 1024** on AIME 2025 (post-base-model-cutoff, no contamination).

**Formal basis — Theorem 1:** Under a Logic Prior assumption (correct CoTs yield correct answers with probability α, incorrect CoTs with β, α > β), the expected GRPO advantage satisfies:
- E[Â | correct CoT] = (1−p_c)(α−β)/σ > 0
- E[Â | incorrect CoT] = −p_c(α−β)/σ < 0

Therefore GRPO monotonically increases p_c (correct-CoT probability). The driver is the gap α−β > 0, which amplifies with training.

**How it cuts across A–D:**
- *Reconciles with Position D (spurious rewards):* Position D's Qwen-family gain under random rewards is now attributable partly to guessing artifacts in Pass@K, not purely to clipping-bias amplification of pretrained behaviors. The metric-invalidity argument provides a complementary explanation.
- *Strengthens Position A direction:* The paper shows RL improvements are real (not just efficiency re-weighting), consistent with Position A's claim that correct tokens at high-entropy positions are being improved. The formal advantage for correct CoTs (+) vs incorrect CoTs (−) gives mathematical grounding to the "sparse selection matters" intuition.
- *Neither confirms nor refutes Position B:* The theorem operates at the CoT level, not the token level. Whether gradient flow through many tokens is required to find which CoTs to reinforce is not addressed.
- *Consistent with Position C:* Token-level discriminative reweighting (DelTA) and CoT-level logic-prior selection are orthogonal mechanisms — both may contribute.

**Failure mode:** Logic Prior violation (base model makes fatal reasoning errors, e.g., language mixing in R1-Zero training on Chinese data) causes the α−β gap to collapse and RLVR behavior to degrade. Residual P(CC|CA)(q) ≈ 0.70 at end of training — 30% incorrect CoTs remain even after full optimization.

**Key empirical finding:** SFT on RLVR-generated CoTs nearly matches RLVR pass@1 (i.e., RLVR is generating qualitatively better CoTs than the base model, not just re-sampling from a fixed distribution).

## What the conflict is really about

Three live readings, both papers consistent with each:

1. **Position A strict:** RL is fundamentally redundant. The 1–4% are all that matter; DFPO's "gradient exchangeability" gain is incidental cleanup. Predicts: applying ReasonMaxxer-style entropy-gated contrastive FT closes most of DFPO's headline gap vs GSPO.
2. **Position B strict:** The 1–4% Reasonmaxxer measures is an artifact of *post-hoc* attribution from already-trained teachers. RL during training discovers / refines that 1–4% precisely because gradient flows cleanly through the other 96%. Predicts: training-from-scratch with ReasonMaxxer's recipe (no RL teacher to imitate) fails to find the same reranked positions.
3. **Both partial:** RL's effect *is* concentrated in 1–4% of positions, but the path to discovering which 1–4% requires meaningful gradient flow across many tokens (Position B's regime). Predicts: ReasonMaxxer requires a teacher (which it does); a pure base-model entropy filter without any RL-derived guidance underperforms.

## Resolution rule

Two concrete tests, in order of cost:

1. **Apply DFPO and ReasonMaxxer to the same Qwen3-32B base.** If ReasonMaxxer-on-base matches DFPO-trained model performance, Position A strict holds. If DFPO meaningfully exceeds ReasonMaxxer-on-base on the same benchmarks, Position B has a residual contribution beyond the sparse 1–4%.
2. **Strip the RL teacher.** Run ReasonMaxxer's entropy-gating with the teacher replaced by a base-model self-distillation signal. If accuracy holds → Position A strict. If accuracy collapses → reading 3 (RL signal still required to identify which 1–4% to correct).

## Related

- [[reasonmaxxer]], [[token-gradient-cancellation]], [[delta-token-credit]] (discriminator-view third frame), [[spurious-rewards-rlvr]] (clipping-bias fourth frame), [[rlvr-incentivizes-reasoning]] (metric-validity fifth frame), [[rlsd-self-distilled-rlvr]] (also questions standard GRPO from a different angle).
- [[gepa-reflective-prompt-evolution]] — parallel "RL was over-engineering" argument from prompt-space.
- [[conflicts/grpo-vs-evolution-strategies]] — adjacent (RL-vs-non-RL debate at the algorithm level rather than the per-token level).
