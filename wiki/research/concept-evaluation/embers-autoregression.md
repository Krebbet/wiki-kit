# Embers of Autoregression: Understanding Large Language Models Through the Problem They are Trained to Solve

McCoy, Yao, Friedman, Hardy, Griffiths propose that LLM behavior is fundamentally shaped by their training objective—next-word prediction over Internet text—rather than the downstream tasks they are deployed for. They demonstrate that model accuracy on deterministic tasks varies based on three probability factors: task probability (how common the task is in training data), output probability (how high-probability the correct answer is), and input probability (how high-probability the input is). Tested on GPT-3.5 and GPT-4 across 11 tasks. PNAS 2024; arXiv:2309.13638.

## Method

The paper adopts a "teleological approach": understanding LLMs by reasoning about the problem they solve. The authors argue that LLMs are statistical next-word prediction systems, and that this training objective creates "embers of autoregression" that influence behavior even on deterministic tasks unrelated to prediction. Three probability factors are proposed: (1) task probability (frequency of task occurrence in training data), (2) output probability (whether the correct output sequence is high or low probability in natural text), (3) input probability (whether the input is high or low probability). On these three factors, they hypothesize models will show higher accuracy for high-probability variants even when the task is deterministic (where probability should not matter).

The paper evaluates two models: GPT-3.5 and GPT-4 (accessed via OpenAI API, temperature 0.0, using gpt-3.5-turbo-0613 and gpt-4-0613). The 11 tasks span character-level and algorithmic operations: shift cipher (encoding and decoding), Pig Latin (encoding and decoding), article swapping, reversal, counting, acronyms, linear functions, multiplication, sorting, keyboard cipher, and birthday factual recall. Sentences are drawn from GlobalVoices and synthetically modified (via RoBERTa substitution and word shuffling) to create high-probability, medium-probability, and low-probability variants. Shift ciphers serve as the running example: rot-13 (common, ~60x more frequent than rot-2 in Internet text) tests task probability; varying output probability within rot-13 decoding tests output probability; varying input probability for encoding tests input probability.

## Claims

- GPT-4 cipher decoding: 51% accuracy when output is high-probability vs. 13% when low-probability (rot-13 decoding, output probability effect)
- GPT-4 Pig Latin: 42% accuracy on the common variant vs. 23% on rare variant (task probability)
- GPT-4 word reversal: 97% accuracy when output is high-probability vs. 53% when low-probability (output probability effect)
- GPT-4 cipher encoding: 21% accuracy on high-probability inputs vs. 11% on low-probability inputs (input probability effect, weaker than output probability)
- Both GPT-3.5 and GPT-4 perform substantially better on rot-13 (common) than rot-2 (rare), despite equal algorithmic complexity (task probability)
- Output probability shows stronger and more consistent effects than input probability across tasks, predicted by the Bayesian decomposition P(output|input) ∝ P(input|output)P(output)
- The paper identifies 11 "embers of autoregression": sensitivity to task frequency, output probability, input probability, lack of embodiment, sensitivity to wording, difficulty on meaning-dependent tasks, inability to modify previously-produced text, societal biases, idiosyncratic memorization, sensitivity to tokenization, and limited compositionality

## Relevance to the project

**Why a single TestSet pass-rate is unreliable:** A naive concept evaluator might measure `Evaluate(S, c)` as the percentage of samples from S where the model applies concept c correctly. The "Embers" paper shows this is insufficient: the model might succeed not because it understands the concept, but because the high-probability outputs happen to coincide with correct applications. A test set of high-probability positive examples (e.g., counting common words, decoding rot-13) will overestimate understanding compared to an equivalent test set of low-probability examples. This confound between conceptual understanding and output probability corrupts the signal from a single test-set pass-rate.

**Implications for `Evaluate(S, c)` design:** The paper suggests a structured pairing strategy: for each concept application, construct both a high-probability and low-probability variant. If the model achieves 90% on high-probability variants and 45% on low-probability variants of the same concept (as the cipher results show), this gap reveals the model is exploiting output probability rather than genuinely applying the concept. A true understanding-eval should show comparable performance across high-probability and low-probability variants. At minimum, evaluators should report separate accuracies for high- and low-probability subsets, enabling post-hoc detection of probability-driven failures.

**Implications for `Decompose(c, trace)` design:** When a teacher reads a failure trace—the model failed to apply concept c on input S—the teacher must distinguish two failure modes: (1) the model genuinely lacks the concept, or (2) the model has the concept but deprioritized a low-probability output. The Embers framework clarifies this: if the failure occurs on a low-probability output variant (rare word, uncommon task, low-frequency input), the teacher should suspect mode (2) and investigate whether the model succeeds on a high-probability variant of the same concept. This shifts the interpretation of failure traces from "model doesn't know c" to "model didn't prioritize c in this low-probability region." Tracing should therefore include metadata on output and input probability to enable this distinction.

## Source

- arXiv: 2309.13638
- Raw markdown: `../../../raw/research/concept-understanding-eval/09-embers-autoregression.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[counterfactual-tasks]] — Wu et al.'s counterfactual variants are *one* way to control for the output-probability confound that Embers identifies
- [[gsm-symbolic]] — GSM-NoOp tests one of Embers' three factors (task probability under irrelevant-clause shift)
- [[../synthesis/recursive-concept-learning]] — **diagnostic prior** for E1's design: any TestSet pass-rate is unreliable as a concept-understanding signal unless paired with high-prob and low-prob output variants
- [[../synthesis/proposed-method]] — implicates `Evaluate(S, c)` design across components; relevant to gap #6 (concept-probe metric calibration)
- [[../in-context-learning-theory/icl-bayesian-inference]] — Embers is the empirical complement to the Bayesian-ICL output-probability story
