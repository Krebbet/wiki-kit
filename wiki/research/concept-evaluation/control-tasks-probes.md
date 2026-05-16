# Designing and Interpreting Probes with Control Tasks

Hewitt & Liang (Stanford, EMNLP 2019; arXiv 1909.03368) propose **control tasks**—pairing linguistic probing tasks with random-label baseline tasks to measure whether a probe's accuracy reflects representation structure or mere memorization. Control tasks assign random outputs by word type, creating a ceiling on performance a probe can achieve via type-level memorization alone. The key metric is **selectivity**: linguistic task accuracy minus control task accuracy—a high-selectivity probe should beat random labels by a wide margin.

## Method

A control task is constructed for a linguistic task (e.g. part-of-speech tagging or dependency edge prediction) by sampling a random output label independently for each word type in the vocabulary. For POS tagging, each word type receives a fixed random tag (1–45); for dependency edge prediction, each word type receives one of three behaviors: attach to self, attach to root, or attach to last token. The control task then assigns these pre-sampled labels deterministically based on word identity, regardless of context.

Selectivity is defined as linguistic task accuracy minus control task accuracy. By design, a control task can only be solved through memorization at the type level (a probe learning the word-label mapping), while a linguistic task should reflect learned linguistic structure in the representation. A **good probe** exhibits high selectivity: it achieves high linguistic task accuracy and low control task accuracy, demonstrating that its accuracy depends on representation properties, not probe memorization capacity.

The authors systematically study three probe families (linear, bilinear, MLP with 1–2 hidden layers) on ELMo representations using five complexity control methods: hidden state dimensionality (2–1000), dropout (0–0.8), training set size (1–100%), weight decay (0–10.0), and early stopping. They evaluate on Penn Treebank POS tagging and dependency edge prediction.

## Claims

1. **Default MLP probes show poor selectivity.** On POS tagging with standard 1000-dimensional hidden states, MLP-1 achieves 97.3% linguistic accuracy and 92.8% control accuracy, yielding selectivity of only 4.5—suggesting most gains come from memorization. (Table 1, default row)

2. **Linear probes are more selective.** Linear probes on POS tagging reach 97.2% linguistic accuracy (comparable to MLPs) but only 71.2% control accuracy, for selectivity of 26.0—a 5.8× improvement. (Table 1, default row)

3. **Dropout is ineffective for MLP selectivity.** Adding p=0.4 dropout does not consistently improve selectivity; MLP-2 selectivity actually decreases (4.2 → 3.4). Early stopping also fails to reliably boost selectivity. (Table 1, with-dropout row; § 3.5)

4. **Constraining hidden dimensionality improves selectivity.** Reducing MLP-1 hidden states from 1000 to 10 dimensions raises POS selectivity from 4.5 to 16.6 (3.7×) with negligible accuracy loss (97.3 → 97.2). Weight decay and sample-size constraints are also effective. (Table 1, "Probes Designed with Control Tasks")

5. **ELMo2 is more selective than ELMo1 despite lower accuracy.** Linear probes achieve 26.0 selectivity on ELMo1 vs. 31.4 on ELMo2, despite 97.2% vs. 96.6% POS accuracy. This suggests ELMo1 encodes word identity more directly; high ELMo1 accuracy may reflect memorization of word-POS mappings rather than linguistic structure. (Table 2; § 4.2)

6. **Selectivity reveals bilinear probes are more faithful for dependency edge prediction.** Bilinear probes achieve 6.7 selectivity vs. −0.7 for MLP-1 on ELMo1, suggesting that while MLPs reach higher accuracy (92.3%), they may be encoding spurious patterns (e.g. word-form cues) rather than syntactic structure. (Table 2)

7. **Type-level memorization is asymptotic.** The ceiling on control task performance is the fraction of test-set word types that appeared in training. High control accuracy indicates the probe's capacity to memorize independently of the linguistic task structure.

## Relevance to the project

**Selectivity as a precondition for Evaluate(S, c).** In Recursive Concept Learning, when `Evaluate(S, c)` uses internal-representation probes (e.g. a linear classifier on activations) to verify whether a concept was installed, selectivity is critical. A probe that achieves high accuracy on a concept-classification task tells us nothing if it is simply memorizing surface correlates (word identity, task-irrelevant features) from the representation. By requiring the probe to beat a control task (random concept labels, or labels scrambled at the sample level), we can separate "the model encodes this concept" from "the probe learned a spurious pattern." This is especially important in few-shot or single-sample settings where memorization is a major confound.

**High probe accuracy does not imply concept encoding.** This paper's core finding—that 97% accuracy on POS tagging with 92% control accuracy is ambiguous—directly addresses the "did concept-tuning install the concept or memorize a pattern?" question. When fine-tuning on a single example, the model has tremendous capacity to overfit to idiosyncratic features. A concept probe must demonstrate selectivity to rule out the hypothesis that `Evaluate(S, c)` is measuring pattern memorization, not concept installation. The selectivity criterion shifts the burden of proof: the probe must be more accurate on the true concept labels than on random-label controls to claim the concept is encoded.

**Limitations and complementary methods.** Selectivity applies to representation probes (internal classifiers on hidden states). It does not address behavioral probes—does the model actually use the concept when making decisions, or does it encode it silently? CheckList (behavioral test batteries) and Contrast Sets measure behavioral sensitivity, orthogonal to the internal-encoding question. Recursive Concept Learning may need both: selectivity on internal probes (concept installed) and behavioral probes (concept used). Future work should combine these to close the gap between representation and behavior.

## Source

- arXiv: 1909.03368
- Venue: EMNLP 2019
- Authors: John Hewitt, Percy Liang (Stanford)
- Raw markdown: `../../../raw/research/concept-understanding-eval/08-control-tasks-probes.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[causal-abstraction]] — Geiger et al.'s IIA is the intervention-based successor to selectivity; both ask "did the probe learn the concept, or did the model encode it?"
- [[../synthesis/recursive-concept-learning]] — methodological floor for **E1** when the battery uses representation probes (rather than behavioural ones); selectivity is the precondition for any probe claim
- [[../synthesis/proposed-method]] — relevant when a concept-probe in component **V** uses internal activations rather than text output
- [[../in-context-learning-theory/_overview]] — induction-head and ICL-as-gradient-descent claims rest on probes; control-task selectivity is the discipline they require
