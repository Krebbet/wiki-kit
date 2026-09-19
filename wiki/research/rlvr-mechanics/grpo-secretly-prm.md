# GRPO is Secretly a Process Reward Model

Sullivan & Koller (Saarland, arXiv:2509.21154, ICML 2026) prove that standard GRPO trained with outcome-only (ORM) reward is **exactly equivalent** to an RL objective built on a non-trivial, Monte-Carlo-estimated process reward model — whenever trajectories in a rollout group share overlapping token prefixes, which is nearly always the case in practice. GRPO already computes step-level credit assignment; it just isn't labeled as such. The paper also identifies a structural exploration/exploitation defect this hidden PRM introduces and proposes a near-zero-cost fix, **λ-GRPO**.

## Method

- **Process sets.** For a rollout group $G$ with outcome rewards $r^{(i)}$, define $B(G)$ = the set of all maximal subsets of $G$ ("process sets" $\lambda$) sharing an identical token prefix. $B(G)$ has a natural tree structure: root = $G$, leaves = singleton trajectories, induced by prefix-sharing. Each node $\lambda$ defines a *process step* — the sub-trajectory span shared by all its members — with a Monte-Carlo process reward $r_{mean}(\lambda)$ = mean outcome reward of the trajectories sharing that prefix (Eq. 5).
- **Definition 1 (formal PRM).** A function mapping a trajectory to a sequence of (sub-trajectory, step-reward) pairs. An ORM is the trivial case: one step covering the whole trajectory. Plugging $B(G)$'s step rewards into token-level advantages $A_{i,t} = (R_{i,t} - r_{mean}(G))/r_{std}(G)$ yields a PRM-aware objective $L_{PRM}$ (Eq. 6), structurally parallel to GRPO's token-level (DAPO-style) loss $L_{GRPO}$.
- **Theorem 1 (proof via Lemma 1, Appendix B): for any query, policy, and group, $L_{GRPO}(G) = L_{PRM}(G)$ exactly.** Requires two conditions: µ=1 update/batch (else the PPO clip ratio breaks the derivation), and the DAPO token-level loss formulation (not the original Shao et al. sample-level GRPO loss) — the authors argue DAPO's version is now the de facto standard (e.g. the TRL trainer). Building $B(G)$ costs $O(k^2n)$ for group size $k$, sequence length $n$ — empirically negligible (~1.2×10⁻⁷ sec/token, single CPU core).
- **The defect.** Rewriting $L_{GRPO}$ via the partition of process sets active at each token reveals each set $\lambda$'s loss contribution is scaled by its frequency $|\lambda|$ (Eq. 8) — an *unintended* weighting. High-frequency shared prefixes get their advantage sign amplified, which can (a) suppress exploration of good-but-rare completions when a shared prefix's mean is low, and (b) suppress exploitation of a genuinely best trajectory when its early tokens are shared with worse siblings. Worked example (§4.1): a trajectory with the group's max reward can still see its likelihood *decreased* by GRPO, because its shared prefix carries negative process reward.
- **λ-GRPO fix** (Eq. 9): divide each token's loss term by $|\lambda^{(i,t)}|$, the size of the process set it belongs to — cancels the frequency weighting so every process step contributes equally regardless of how many trajectories share it.

## Claims

- λ-GRPO vs. standard GRPO on DeepSeek-R1-Distill-Qwen-1.5B and Llama-3.2-1B-Instruct (OpenRS math data), evaluated on AIME24/MATH-500/AMC23/Minerva/OlympiadBench: λ-GRPO wins 15/20 cells and beats base on 14/20; reaches >10% average validation-accuracy gain in **less than half the training steps** (~2× speedup) across all four (model × KL-coefficient) configurations tested.
- On a synthetic depth-4 binary-tree exploitation-defect probe (Table 1): at $n=1, r_{neg}=-1.0$, GRPO recovers the max-reward target path in 0.0% of final-step occurrences vs. λ-GRPO's 75.35%.
- On Llama with $\beta=0.04$, λ-GRPO underperforms GRPO on *average* downstream accuracy (though still wins 3/5 individual tasks) — not a uniform win.
- Empirical check: only 0.2% of $k=6$ groups and 0% of $k=36$ groups were "flat" (no prefix sharing at all) on the paper's OpenRS runs — the implicit PRM is non-trivial in practice, though this is dataset/task/model-dependent.

## Relevance to the project

This is a formal-identity result, not an empirical finding — it strengthens the wiki's "RL reranks/reweights, doesn't teach new skills" thread by showing that even GRPO's *credit assignment itself* is a mean-reward-of-prefix-completions estimate, a form of implicit self-consistency over the model's own rollouts rather than an externally injected signal. The paper's own framing explicitly bridges two themes this wiki has tracked mostly separately: [[_overview|RLVR mechanics]] and [[../process-reward-models/_overview|process reward models]] — the Monte-Carlo step-label construction here ($r_{mean}(\lambda)$) is structurally the same thing [[../process-reward-models/math-shepherd|Math-Shepherd]] does explicitly with rollout-success-rate step labels; this paper shows GRPO computes the equivalent quantity implicitly, for free, from group structure alone.

## Limitations

- Equivalence requires µ=1 and the DAPO token-level loss — a real scope caveat against the original Shao et al. sample-level formulation.
- $O(k^2n)$ tree-construction cost is unverified at much larger group sizes or long agentic rollouts (only tested at $k \leq 36$, small models, CPU-only timing).
- The captured raw source cuts off near the Impact Statement section; Appendices (A: limitations, B: proof of Lemma 1, C: training details, D–E) are referenced in-text but not present in the capture. The main text (Theorem 1, λ-GRPO derivation, both experimental sections) is complete.

## Source

- `raw/research/weekly-2026-09-18/02-grpo-secretly-prm.md`
- arXiv:2509.21154

## Related

- [[deepseekmath-grpo]] — this paper re-derives and extends the exact GRPO objective that page documents; DAPO's token-level loss (load-bearing for Theorem 1) is covered via [[../rl-optimizers/dapo]]
- [[_overview]] — theme overview already tracks credit-assignment/token-level results ([[rethinking-rl-sparse-selection]], [[high-entropy-minority-tokens]], [[../rl-optimizers/grpo-std-identity]]); Theorem 1 is arguably the most fundamental result in that cluster — a formal identity, not an empirical one
- [[../process-reward-models/_overview]] / [[../process-reward-models/math-shepherd]] — the paper's own explicitly flagged "bridge": Math-Shepherd's Monte-Carlo step labels are structurally the same construction proven implicit in vanilla GRPO
- [[../process-reward-models/pav-rewarding-progress]] — PAV's process-advantage-as-progress framing is conceptually adjacent; PAV requires a "complementary prover," this paper's PRM falls out for free from group structure
- [[../rl-optimizers/dapo]] — the token-level loss variant Theorem 1's proof depends on
- [[../rl-optimizers/grpo-std-identity]] — both papers do exact algebraic identity-level reformulations of the GRPO objective (std-normalization vs. implicit reward structure) — worth a synthesis note on independent GRPO-internals identity results
- [[../../weekly-briefs/2026-09-18]] — brought in by the 2026-09-18 weekly sweep
