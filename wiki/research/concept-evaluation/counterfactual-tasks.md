# Reasoning or Reciting? Exploring the Capabilities and Limitations of Language Models Through Counterfactual Tasks

Wu et al. (2023) propose a counterfactual evaluation framework to test whether LLM task performance reflects abstract reasoning or task-specific memorization. Across 11 tasks (arithmetic, code, syntax, logic, spatial, drawing, music, chess, SET), models consistently degrade on counterfactual variants that preserve task structure but alter surface conditions. arXiv:2307.02477.

## Method

The core insight is formalizing tasks as f_w: X → Y under world model w. The default world w[default] encodes assumed task conditions (base-10 arithmetic, 0-indexed arrays, etc.). Counterfactual worlds w[cf] preserve the reasoning procedure but change instantiation—e.g., base-9 addition, 1-indexed Python (ThonPy), reordered syntax, chess with swapped bishop/knight positions.

Evaluation uses 0-shot prompting: specify task f, instance x, and world w, then compare LM output to ground truth. To control for instruction comprehension, each task includes a Counterfactual Comprehension Check (CCC)—a simpler task (e.g., "what number follows 8 in base-9?") using the same counterfactual prompt that only succeeds if the model understands w[cf]. CCCs pass in most cases (especially GPT-4), but counterfactual task performance still drops dramatically.

The 11 tasks span procedural (arithmetic, code), linguistic (syntax, logic), and grounded domains (spatial reasoning, drawing, music, chess, SET). Counterfactuals systematically vary one parameter: arithmetic base (8, 9, 11, 16), indexing (0 vs 1), word order, premise truthfulness, spatial axis orientation, object rotation/flip, instrument tuning/transposition, chess piece placement, and SET rules. Models tested: GPT-4, GPT-3.5, Claude, PaLM-2.

Performance degradation is measured as default-vs-counterfactual accuracy gap. Analysis reveals that commonness (base-8/-16 outperform -9/-11), proximity to default, and difficulty all correlate with smaller gaps. Few-shot demonstrations reduce but don't eliminate gaps.

## Claims

1. "Performance on counterfactual task variants consistently and substantially degrades relative to the performance on the default settings" (Abstract, §4). GPT-4's arithmetic accuracy drops from ~96% (base-10) to ~20% (base-9) with high CCC accuracy (showing instruction comprehension).

2. "While current LMs may possess abstract task-solving skills to an extent, they often also rely on narrow, non-transferable procedures for task-solving" (Abstract). The abstraction-vs-procedure distinction is cleanest in tasks with perfect/near-perfect default performance and high CCCs but low counterfactual accuracy.

3. "Models perform better under more common conditions" (§5.1). Base-8/-16 arithmetic outperforms base-9/-11; drop-D guitar tuning (common among guitarists) yields higher accuracy than arbitrary alterations.

4. "Default task performance can be a good indicator of counterfactual performance" (§5.3). Default-counterfactual accuracy is strongly correlated across task variants, instance difficulty, and models—suggesting some transferable reasoning coexists with memorization.

5. "0-shot chain-of-thought prompting sometimes hurts performance" (§5.4). Encouraging step-by-step reasoning degrades PaLM-2's base-10 addition and all models' chord placement, hypothesized due to "overthinking" simple memorized tasks.

6. "Few-shot demonstrations reduce but don't eliminate the gap" (§5.5). For arithmetic, adding up to 16 demonstrations shrinks the base-9/11/16 gaps but plateaus; the default-counterfactual gap remains "sizeable."

7. "LM reasoning is affected by proximity to the (LM-believed) real world" (§5.2). Logistic regression on first-order logic tasks shows models predict more accurately with true premises and when conclusion truthfulness matches the label—violations of pure symbolic reasoning.

8. "Models understand counterfactual conditions at the surface level but fail to apply them robustly" (§5.6). Drawing task CCC passes (model knows to flip/rotate) but generated objects are often untransformed or degraded; GPT-3.5's parsing fails in 25-38% of counterfactual drawing cases.

## Relevance to the project

**Abstraction vs. procedure distinction.** Counterfactual tasks directly operationalize the question "does the model understand the concept, or only a surface procedure?" For Recursive Concept Learning, this is invaluable: a model may learn to reproduce a procedure for addition in base-10 (procedural), yet fail to generalize the abstract concept to base-9 (conceptual). The CCC protocol elegantly disambiguates instruction-following failure from genuine reasoning failure, enabling clean evaluation of concept transfer.

**Constructing counterfactual variants for procedural concepts.** The paper shows systematic patterns: (a) fundamental world-model changes (base, indexing, rules) reveal reasoning; (b) superficial perturbations (word swaps, rotations) can admit shortcuts. For single-sample learning of procedural concepts (e.g., multiplication, sorting), counterfactuals are natural: change the base, the sort key, the operand order. The construction is mechanistic and reproducible, fitting within a curriculum-learning framework where variant difficulty is tunable.

**Qualitative concept extension.** The paper is strongest on concrete, mechanistic domains (arithmetic, code, games). For abstract conceptual domains (supply & demand, idealism, causality), the counterfactual paradigm requires reframing: abstract concepts don't have "worlds" with swappable parameters. Instead, one might ask: can the model apply a concept under different narrative framing, different symbolic encoding, or different causal scenarios? The CCC idea (verify basic comprehension of the counterfactual condition) transfers well, but task design becomes harder—fewer natural "surface changes" exist.

**Limitations.** Task difficulty must be controlled or acknowledged; some counterfactuals are inherently harder (melody transposition involves 2-step reasoning). Non-perfect CCCs conflate instruction comprehension with reasoning, though large gaps often survive this confounder. Counterfactual conditions may exist in pretraining data (drawings of rotated objects), leading to overestimation of reasoning. The binary reasoning/reciting framing obscures that models operate on a continuum. For single-sample learning, if the model only ever sees one instance, it cannot distinguish memorization from abstraction—counterfactual evaluation becomes essential, but also resource-intensive (requires multiple variants per concept).

## Source

- arXiv: 2307.02477
- Raw markdown: `../../../raw/research/concept-understanding-eval/03-counterfactual-tasks.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[gsm-symbolic]] — symbolic-template variants and counterfactual-content variants are the two canonical recipes for the same memorisation-vs-abstraction question
- [[math-perturb]] — sibling memorisation probe with hard solution-path perturbation
- [[embers-autoregression]] — diagnostic prior; counterfactual variants control for output-probability shift, which Embers identifies as the key confound
- [[../synthesis/recursive-concept-learning]] — **E1** axis (counterfactual pass-rate); also the cleanest "abstraction installed vs procedure memorised" test for `Evaluate(S, c)`
- [[../synthesis/proposed-method]] — gap #6 (LLM concept-probe metric); counterfactual variants are the cross-domain answer
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — single-sample regime where memorisation-vs-abstraction is acute; counterfactual is the natural retest
