# Same Answer, New Box: Answer-Format Share of RLVR Out-of-Domain Gains

Lyu (Monash; arXiv:2610.20639) re-scores stored greedy outputs of released base/RL checkpoint pairs with one fixed answer extractor and finds that 82% (95% CI 77.4-87.2%) of the out-of-domain multiple-choice gain (MMLU, MMLU-Pro, ARC-C) that harness extractors report for four 7B SimpleRL pairs is answer-format gain: RL moves an already-stated answer into `\boxed{}`, which box-first extractors then credit. It is a pure measurement paper (no training), and it is a measurement-validity warning for every "RLVR transfers OOD" claim scored by text extraction.

## Method

Generate greedy outputs (max 2,048 tokens) from base and RL checkpoints under two prompts (boxed-instruction, plain). Score each output twice: (a) with "harness extractors" copied from public repos (MATH eval code, Open-Reasoner-Zero, Qwen2.5-Math, simple-evals, lm-eval-harness, verl); (b) with one fixed extractor $\omega$ that reads a stated answer from `\boxed{}`, after "the answer is"/"Answer:", on its own line, or after "option/choice". Abstention counts as wrong; items are never dropped.

$$g_{rep}=\mathrm{acc}(RL,h)-\mathrm{acc}(base,h),\quad g_{fix}=\mathrm{acc}(RL,\omega)-\mathrm{acc}(base,\omega),\quad D=g_{rep}-g_{fix}$$

Format share $=\sum D/\sum g_{rep}$, pooled and weighted by reported gain. Only comparisons with clearly positive reported gain (lower 95% bound >= 2 pts) and $\omega$-readable outputs (>=50% extraction on each model, rates within 20 pts) are pooled. Validation: two independent LLM readers plus an adjudicator on 2,720 responses. Seven pairs studied (4 pooled): Qwen2.5-Math-7B (SimpleRL-Zoo, -Zero), Qwen2.5-7B Zoo, Mistral-7B-v0.1 Zoo. Cost is laptop-CPU re-reading of up to 500 items per benchmark.

## Claims

- Over 46 pooled comparisons, harness extractors report a mean +22.5 pt OOD-MC gain; $\omega$ reads +4.0. Format share 82.2%, >=76% per benchmark and per Qwen pair; 75-87% across all analysis variations (non-zero-gain pooling 75%, boxed prompt 79% vs plain 86%, LLM readers 77%).
- Extractor choice alone moves the number: on identical outputs the max-min reported gain differs by a median 15.1 pts (10 without simple-evals). Fig. 1 example, Qwen2.5-7B vs SimpleRL-Zoo on ARC-C: boxed-only extractor +30.6, fixed $\omega$ +9.8, Qwen2.5-Math extractor +1.0, simple-evals -1.8. Per-extractor shares: MATH 85%, ORZ 83%, Qwen2.5-Math 56%.
- In-domain free-form math (MATH-500, GSM8K): base and RL both box ~96-97%, format gain near zero. The artefact is specific to OOD answer forms where the base does not box.
- Survey: of 18 RLVR releases, 17 report OOD-MC results; 13 text-extracted, 1 log-likelihood, 3 unspecified.

## Mechanism

Among outputs $\omega$ can read, 26.6% of base vs 58.3% of RL outputs contain `\boxed{}` (34.7% vs 81.9% on items neither model truncated). Base models mostly state the answer in prose; RL learns early that boxing is rewarded (the training reward is a boxed math answer) and generalises that surface habit to MC prompts. The capability to write the answer already exists in the base (26.6% already boxed), so this is a selection/placement shift, not new competence. Consistent with: format-only reward recovering about half of the MATH-500 gain ([[spurious-rewards-rlvr]]), RL mostly strengthening answer-delimiter SAE features (Du et al. 2026), and first RL steps adapting to the extraction function (MiMo).

## Limitations

- No published gain is decomposed: SimpleRL-Zoo's own eval used temp 1.0, its own prompt and the Qwen2.5-Math reader (letters from text), so 82% is not an estimate for published numbers.
- 82% is conditional on selecting comparisons with large reported gains, which selects toward format-driven cases.
- One release family at 7B; Qwen carries nearly all the gain. Qwen2.5-32B DAPO pair: format share 2.1% (CI -18.5% to 19.9%, 9 comparisons), because the base already boxes when asked.
- Prompt dependent: a letter-in-box system prompt gave 31% for Qwen2.5-Math-7B/MMLU vs 86-88%. Share on other benchmark/answer-form combos moves 50+ pts with the pooling rule.
- $\omega$ is itself fallible: Llama-3.1-8B pilot reads -19 pts; and $\omega$ overstates gain vs the Qwen2.5-Math reader (9.8 vs 1.0), so true share may be higher on some pairs. LLM readers credit RL with more correct answers where $\omega$ abstains, so 77-82% may be a lower bound or noisy. Readers are LLMs only; no human check.
- Does not test compositionality, and does not show the residual +4.0 pts is genuine transfer.

## Thesis relevance

- **Transfer evidence.** A reported OOD gain is evidence of concept/skill transfer only if the scorer is format-invariant. Re-scoring with a second extractor (or log-likelihood / answer matching) is a cheap validity check to add to the concept-evaluation toolkit ([[../concept-evaluation/_overview]]).
- **Single-sample RLVR.** [[../single-sample-rl-finetuning/1-shot-rlvr]] is cited as showing format-only reward recovers most of the one-example gain; any cross-domain or MMLU-style gain attributed to 1-shot RLVR should be re-scored with a fixed extractor before it is read as transfer. The same applies to the single-sample experiments in this wiki: report $g_{rep}$ and $g_{fix}$ both.
- **Selection not installation.** Output-format migration is the shallowest instance of the reuse thesis: [[rethinking-rl-sparse-selection]] (0% mass outside base top-5), [[rlvr-pattern-selection-theory]] (RL shifts which patterns are used), [[context-grounding-mechanism-reuse]]. The Qwen-specific concentration matches [[random-reward-reachability-probe]].
- **Evaluation-methodology dispute** alongside [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] (artefact vs genuine capability extension).
- Leads: Chang et al. 2026 (arXiv:2609.36587, in-domain strict-vs-lenient scorer); Chandak 2025 (answer matching vs MC).

## Source

- raw/research/weekly-2026-10-16/03-rlvr-ood-answer-format.md (arXiv:2610.20639; harness code in arXiv ancillary files)

## Related

- [[_overview]]
- [[spurious-rewards-rlvr]]
- [[rethinking-rl-sparse-selection]]
- [[rlvr-pattern-selection-theory]]
- [[context-grounding-mechanism-reuse]]
- [[random-reward-reachability-probe]]
- [[../single-sample-rl-finetuning/1-shot-rlvr]]
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]]
- [[../single-sample-rl-finetuning/_overview]]
- [[../concept-evaluation/_overview]]
- [[../weekly-briefs/2026-10-16]] — brought in by the 2026-10-16 weekly sweep
