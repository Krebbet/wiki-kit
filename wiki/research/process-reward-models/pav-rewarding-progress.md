# Rewarding Progress: Scaling Automated Process Verifiers for LLM Reasoning

Amrith Setlur, Chirag Nagpal, Adam Fisch, Xinyang Geng, Jacob Eisenstein, Rishabh Agarwal, Alekh Agarwal, Jonathan Berant, Aviral Kumar. Google Research / Google DeepMind / CMU. arXiv:2410.08146. Key insight: process rewards should measure *progress* (step-level advantages under a complementary prover policy) rather than step correctness. Process Advantage Verifiers (PAVs) trained on this principle achieve >8% test-time search accuracy gains and 5–6× sample efficiency in RL over outcome reward models.

## Method

Process advantage verifiers measure per-step progress as the change in a prover policy's likelihood of success before/after a step—formally, step-level advantages $A^\mu(s_h, a_h) = Q^\mu(s_h, a_h) - V^\mu(s_h)$ under prover policy $\mu$ distinct from the base policy. The effective reward combines outcome evaluation and process advantage:

$$\ell_{\text{PAV-RL}}(\pi) := \ell_{\text{ORM-RL}}(\pi) + \alpha \sum_{h=1}^{H} A^\mu(s_h, a_h)$$

Good provers are *complementary* to the base policy: they sufficiently distinguish actions via advantage variance while remaining reasonably aligned with the base. Theorem 3.1 formalizes that improvement scales with $\mathbb{V}_{a \sim \pi_t}[A^\mu(s, a)]$ (distinguishability) and $\mathbb{E}[A^\mu A^{\pi_t}]$ (alignment). Best-of-K policies ($K > 1$) serve as a practical choice of complementary provers. PAVs are trained on coverage/completeness triples $(x, s_{\text{seed}}, \widehat{Q}^\mu)$ where seed rollouts from the prover are extended with Monte-Carlo estimates.

## Claims

- Test-time beam search with PAVs achieves >8% accuracy improvement and 1.5–5× compute efficiency vs. ORM re-ranking across Gemma 2B, 9B, 27B (Figure 4, Table results).
- Online RL with PAV dense rewards is 5–6× more sample-efficient than ORM-only RL and achieves >6% accuracy gain (Figure 7a–c, first large-scale demonstration of dense-reward PRMs in RL).
- Advantages computed under complementary provers (neither too weak nor too strong) substantially improve the base policy; Best-of-4 policies prove empirically optimal across tested base models (Figure 5b, Remark 3.1).
- Weak prover policies can amplify stronger base policies—contrary to intuition, a 9B policy improves a 27B base policy more than a 27B prover (Figure 5c, Proposition F.1).
- PAV-RL discovers solutions to hard problems unsolvable by Best-of-256 sampling from the SFT base policy, demonstrating exploration benefit (Figure 8b).
- Advantages enable superior exploration–exploitation tradeoff: Pass@N grows 5× faster with PAV-RL vs. ORM-RL in synthetic task (Figure 3c).

## Relevance to the project

PAV directly addresses single-sample, concept-based fine-tuning by reframing the reward signal itself. Rather than learning a policy from many samples annotated by external metrics, PAV uses *one concept*—the prover's step-level advantage—to densely guide both test-time search and RL from sparse labels. This is sample-efficient: the paper shows 6× efficiency gains on the same training problems as ORM baselines. The "complementary prover" insight is particularly powerful for single-shot scenarios: a weak, orthogonal prover can provide richer supervision than a strong one, allowing fine-tuning to proceed from minimal data.

Limitation: PAV requires ground-truth outcome labels (correctness) and relies on learned verifiers, which incur fitting error. The method is most applicable to domains with clear terminal outcomes (math reasoning). Extension to open-ended tasks or settings without ground-truth verifiers remains open.

## Source

- arXiv: 2410.08146
- Raw markdown: `../../../raw/research/adjacent-reward-signals/01-pav-rewarding-progress.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/pav-rewarding-progress.pdf`

## Related

- [[lets-verify-step-by-step]] — process reward model foundations; verifier training
- [[math-shepherd]] — step-level reward modeling for reasoning
- [[process-outcome-feedback]] — hybrid dense/sparse reward formulations
- [[training-verifiers-gsm8k]] — verifier scaling and data collection
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — single-sample RL with sparse rewards
- [[../self-improvement/rstar-math]] — self-improve via multi-turn RL
- [[../rlvr-mechanics/_overview]] — advantage estimation and policy gradients
