# TTPO: Test-Time Policy Optimization

Zhejiang University / Alibaba (arXiv:2608.27448, Aug 2026). Label-free test-time training for LLM reasoning that routes majority-vote-agreeing rollouts to on-policy self-distillation (OPSD) and disagreeing rollouts to a GRPO penalty — exploiting the asymmetry that disagreement with a wrong pseudo-label is still usually a correct training signal, while agreement (even with an unverified pseudo-label) is safe to distill toward.

## Method

Sample K=64 rollouts per problem, cluster by mathematical equivalence, take the largest cluster as majority-vote pseudo-label â. Partition into positive set P (agree with â) and negative set N (disagree).

- **Positive branch (OPSD)**: forward-KL distillation toward an answer-conditioned teacher (same model, conditioned on â as privileged context, thinking-mode-on teacher → thinking-mode-off student, following Zhao et al. 2026's OPSD). Per-token weight down-weights positions where the student has already converged (soft-OR of normalized entropy and teacher–student KL).
- **Negative branch (GRPO)**: binary reward (1 if rollout matches â), group-relative advantage over all K rollouts, penalty confined to negative samples; token mask keeps only high-confidence-error tokens.
- Combined loss: `L = (1/|B|)(Σ_P L_OPSD + λ Σ_N L_GRPO)`, λ=0.1. LoRA (r=64, α=128), 100 steps, gradient on first 1,024 completion tokens only.
- Key empirical motivation: pseudo-label wrong on ~85% of competition-level prompts, but ~79% of *disagreeing* rollouts are wrong regardless of whether the pseudo-label itself is right — so penalizing disagreement is safe even under heavy label noise, while distilling toward a wrong label is not.
- Derives from: TTRL (majority-vote test-time RL), OPSD (Zhao et al. 2026, self-distillation via GT-conditioned teacher), TIP (entropy/divergence token-importance weighting), STAPO (masking low-probability/low-entropy tokens).

## Results

Base models Qwen3-1.7B/4B/8B, LoRA, 4×H20, Avg@12 on AIME25/AIME26/HMMT25/HMMT26/BRUMO25.

- **Pure TTT (label-free, trains on the test set)**: Qwen3-1.7B 38.0%→45.2% avg (+7.2 pts), beating OPSD-TTT (+3.3) and TTRL (+5.4); Qwen3-4B 57.4→61.1 (surpasses Qwen3-8B *base* at 60.7); Qwen3-8B 60.7→65.3.
- **OpenThoughts setting** (labels exist but TTPO ignores them): beats label-supervised OPSD at all three scales (e.g. 40.1 vs 39.7 at 1.7B).
- **Non-thinking transfer**: +25.2/+30.6/+36.4 pts (1.7B/4B/8B) when evaluated with thinking disabled, vs. OPSD's +7.1/+5.8/+3.5 — several-fold larger transfer of thinking-mode reasoning into non-thinking inference.
- **Ablation**: reversing branch assignment (GRPO on positives, distillation on negatives) collapses to 37.2 vs. full TTPO's 48.9 on AIME26 TTT — the asymmetric routing itself, not just the mechanisms, is load-bearing.
- **Counterintuitive**: substituting ground-truth labels for pseudo-labels *underperforms* pseudo-label TTPO — GT answers are too rarely matched on hard problems, starving both branches.

## Applicability

A base model with non-trivial pass rate on the target set, a math-equivalence answer extractor/verifier (competition math only so far), K=64 rollouts/problem for reliable voting (nontrivial test-time compute), but only 100 LoRA-only gradient steps. Best fit: adapting a reasoning model to a specific unlabeled problem set without any ground truth.

## Novelty

A recombination with a genuinely new routing insight, not a new architecture or objective primitive: TTRL's majority-vote test-time RL + OPSD's answer-conditioned self-distillation, split by agreement vs. disagreement. The two token-selection mechanisms (weighting, masking) are direct adaptations of TIP and STAPO respectively. Closest prior work per the paper: prior label-free OPSD variants that distill *all* rollouts (propagating label error to every token) or distill only disagreeing rollouts without the GRPO penalty — TTPO's fix is routing disagreement to a sparse RL penalty instead of dense distillation.

## Reproducibility

Code: github.com/ZJU-REAL/TTPO. Full hyperparameters in the paper's appendix. No mention of released LoRA-adapter weights.

## Adoption

Too new to assess. Positions itself against a dense cluster of concurrent 2026 work (TTRL, Hi-TTRL, SCRL, OPSD, TIP, STAPO) — the label-free test-time-RL-for-reasoning space is actively contested across multiple labs (Alibaba, ByteDance, UCSD/Georgia Tech/UMD, CAS/Xiaohongshu) within weeks of each other.

## Conflicts

No direct contradiction of a wiki claim. One unresolved citation-identity question: TTPO's bibliography cites arXiv:2608.06296 and characterizes it as "distilling only the rollouts that disagree with the pseudo-label." The wiki's [[u-opsd-unsupervised-self-distillation]] page cites the same arXiv ID (2608.06296, UCSD/Georgia Tech/UMD/ByteDance) but describes majority-vote consensus becoming the teacher's privileged conditioning context — closer to a "distill toward consensus" framing than "distill only disagreements." Not resolved in this run (would require re-reading the u-opsd source PDF directly); flagged to `master_notes.md` for manual verification.

## Source

- `raw/research/weekly-2026-08-29/02-ttpo-test-time-policy-opt.md` — arXiv:2608.27448. Captured 2026-08-29.

## Related

- [[u-opsd-unsupervised-self-distillation]] — closest prior work, likely same arXiv ID per the citation-identity flag above; TTPO adds the asymmetric GRPO penalty on disagreeing rollouts that u-opsd's own description doesn't include.
- [[tempo-test-time-rl]] — sibling test-time-RL-for-reasoning design (same problem space, different mechanism: TEMPO uses labeled-data critic recalibration, TTPO is fully label-free via majority-vote + asymmetric routing).
- [[test-time-training]] — that cluster page currently covers only architectural/parametric TTT (Titans, Hope, In-Place TTT); TTPO/TEMPO/u-opsd form a distinct RL/distillation-based test-time-adaptation cluster not yet represented there.
- [[rlsd-self-distilled-rlvr]], [[anti-self-distillation]], [[dopd-dual-on-policy-distillation]], [[flux-opd]] — the wiki's existing OPD/OPSD refinement cluster; TTPO extends it into the fully label-free, test-time regime with an added RL component.
- [[high-entropy-tokens-rlvr]] / [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — TTPO's entropy/divergence token weighting and low-probability/low-entropy token masking are further instances of sparse/selective-token RL and distillation gradients.
