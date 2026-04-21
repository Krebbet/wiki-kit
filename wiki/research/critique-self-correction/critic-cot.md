# Critic-CoT: Boosting the Reasoning Abilities of Large Language Model via Chain-of-Thought Critic

Critic-CoT trains LLMs to perform step-wise chain-of-thought critique and refinement via weak supervision, achieving 93.3% on GSM8K and 57.8% on MATH500 with iterative refinement (2408.16326). Unlike prompt-based self-criticism (System-1 intuition), Critic-CoT trains explicit System-2-like reasoning critique. Key insight: strengthening critique ability via SFT on weak-supervision critique-refine pairs **improves base task performance** and enables both filtering and iterative refinement at inference.

## Method

**Weak supervision data construction** (§3.1): Sample multiple solutions from generator G for each question. Use GPT-4-Turbo as critic to generate step-wise labels {+1, −1}. Collect successful critique-refine pairs: (question, attempt, critique, refined_attempt). Automatic filtering: only keep if critique correctly identifies the first error AND refinement yields the right answer. Stage 2 uses learned critic to sample hard negatives.

**Training**: SFT on critic-refine pairs. Critic loss: cross-entropy on step-level correctness labels. Refine loss: generation loss on corrected trajectories starting from error step.

**Inference strategies** (Figure 2b):
- **Critic As Filter**: Generate N solutions via sampling; critic model identifies and filters incorrect ones; select from filtered set (e.g., majority vote over remaining).
- **Iterative Refinement**: Repeatedly apply critic → regenerate from error step until convergence or max iterations.

## Claims

**In-domain (GSM8K)**: **91.7% baseline → 93.3% with iterative refinement** (Table 1a). Majority vote: Maj1@96 → 94.8% baseline → **95.4% with critic filter** (+0.6 points).

**In-domain (MATH500)**: **50.4% baseline → 57.6% after Critic-CoT training alone** (+7.2 points). Iterative refinement: 57.8% (+1.4). Critic+Maj1@512: **66.6%** (Table 1b).

**Out-of-domain**: **AGIEval (MATH-trained model): 56.6% → 63.7% with iterative refinement** (Table 2a). **HumanEval: 76.2% → 84.8%** with Critic-CoT(MATH) (Table 2c).

**Step-wise critique > outcome labels**: Process/outcome-level only models degrade to 89.5%/88.0% critic accuracy vs 92.3% for CoT critique (Table 4, ablation).

**Data quality**: Manual verification shows 85% accuracy on critique of wrong attempts, >90% on refinement and correct attempts (Table 3).

**Not distillation**: Training on GPT-4 solutions only achieves 90.7% GSM8K vs Critic-CoT's 93.3%, showing improvement is from critique training, not oracle solution copying (Table 5).

## Relevance to the project

Critic-CoT directly trains critique capability, filling a gap in the critique-self-correction theme. While Self-Refine and Reflexion leverage off-the-shelf LLM critique (unreliable), and CRITIC uses external tools, Critic-CoT **teaches the model itself to critique step-by-step**. This is directly applicable to single-sample fine-tuning:

1. **Weak supervision**: Enables critique data collection without human annotation; only requires verifiable task (math, code).
2. **Mutual reinforcement**: Training critique improves base task performance (interesting finding: not detrimental). Suggests critique and task-solving share underlying reasoning capability.
3. **Inference primitives**: Offers both filtering and refinement strategies; filtering is sample-efficient (no recomputation), refinement iteratively corrects specific errors.

**Limitations**: Method is task-specific—requires solutions verifiable against ground truth (works for math, code; harder for open-ended tasks). Step-level correctness labels are implicit (derived from solution continuation, not explicit annotation). No evaluation on model trained separately from oracle (only tests final model's own critique capability).

## Source

- arXiv: 2408.16326
- Raw markdown: `../../../raw/research/adjacent-reward-signals/08-critic-cot.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/critic-cot.pdf`

## Related

- [[self-refine]] — Self-Refine prompts for critique without training; Critic-CoT trains explicit step-wise critique via SFT.
- [[reflexion]] — Reflexion uses environment reward; Critic-CoT trains learned step-level critic on weak supervision.
- [[constitutional-ai]] — CAI uses rule-based critique; Critic-CoT learns task-specific critique patterns from data.
- [[../process-reward-models/lets-verify-step-by-step]] — Both target step-level reasoning; Critic-CoT uses weak labels, PRM uses process supervision.
- [[../process-reward-models/math-shepherd]] — Math-Shepherd trains step verifiers; Critic-CoT combines verification + refinement in one model.
- [[../self-improvement/star]] — STaR bootstraps reasoning via RL; Critic-CoT does so via SFT on critique-refine pairs.
