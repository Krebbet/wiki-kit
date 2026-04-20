# Training Verifiers to Solve Math Word Problems

Cobbe et al. (OpenAI, 2021) introduce GSM8K (8.5K grade-school word problems) and the foundational **outcome-supervised verifier** (ORM) recipe: sample many solutions, score with a verifier trained on final-answer correctness, return the top-ranked. A 6B verifier matches a 175B finetuned model — roughly a 30x effective parameter boost — and verification scales with data far better than finetuning. Establishes the token-level value-function variant (predict correctness after every token) as superior to single-scalar scoring, and shows residual dropout is essential to avoid verifier overfitting. The paper everything else in this theme cites as the ORM baseline.

## Method
- **GSM8K dataset:** 8.5K human-written problems (7.5K train / 1K test), natural-language solutions, 2–8 calculator-using steps. Calculator annotations `<<expr=val>>` are auto-generated; at test time `python eval()` overrides sampled tokens between `=` and `>>`.
- **Finetuning baseline:** standard CE on full solution sequences; T=0 single sample at test.
- **Verifier (ORM) pipeline:**
  1. Finetune generator for 2 epochs (longer collapses sample diversity).
  2. Sample 100 completions per training problem at T=0.7; label by final-answer correctness.
  3. Train verifier 1 epoch with joint objective: language modelling + scalar correctness head (single bias+gain on a reserved logit).
- **Token-level vs solution-level:** verifier predicts at every token (token-level value function) — outperforms full-solution scoring; less overfitting.
- **Test time:** sample 100, rerank by verifier; optional majority vote among top-K verifier-ranked samples.

## Claims
- 6B + verification ≈ 175B finetuning on GSM8K — ~30x effective parameter boost (Fig. 5).
- Verification scales better with training data than finetuning (Fig. 5); below a threshold it under-performs SFT due to overfitting on small data.
- Token-level verifier > solution-level verifier (Fig. 6a); the per-token signal acts as auxiliary value-function regularisation.
- Joint LM + verifier objective > pure verifier objective (Fig. 6b).
- Generator size matters more than verifier size: larger generator with smaller verifier > vice versa (Fig. 6c) — verification leans on relatively coarse heuristics.
- Test-time scaling: gains continue up to ~400 samples per problem before adversarial-to-verifier solutions cause regression (Fig. 7a). Top-3 to top-30 majority vote among verifier-ranked samples is optimal depending on N (Fig. 7b).
- Dropout (20% residual) is a strong regulariser for both finetuning and verifiers (Fig. 8); without it solution-level verifiers overfit badly.
- Direct-answer finetuning (no chain) collapses 6B from 20.6 → 5.2% — natural-language traces are necessary.

## Sample efficiency
- 7.5K problems × 100 samples = 750K verifier training rows generated automatically from final-answer checking — no human step labels.
- Effective compute trade: 30x model-size equivalence at the cost of 100 samples/problem at inference time. Verifier itself is same size as generator (or smaller).
- The 100-samples-per-problem training data is the labour-free analogue of [[math-shepherd]]'s rollout-based PRM data.

## Relevance to the project
The originator of automated, outcome-grounded reward modelling for reasoning, and the methodological reference for every PRM paper that follows. Three things matter for the project:
1. **Token-level value-function objective is cheap and works** — the same trick can be reused for step-level or component-level scoring; no architectural innovation needed beyond a scalar head on a reserved token.
2. **Verifier > generator scaling exists in the small-model regime** — a 6B verifier rerank already matches a 175B SFT model, suggesting that for 1–40B targets, investing compute in a process verifier is more leveraged than scaling the generator.
3. **Sample diversity collapses by epoch ~2** of generator finetuning; the project's single-sample/concept-based learning regime should treat this as a hard ceiling on how much SFT can be done before the verifier-feeding distribution dies. Concept-component rewards likely need to enter early, before generator overfits.
Also a useful negative result: outcome-only verification leaves trace errors unaddressed (a finding [[process-outcome-feedback]] formalises).

## Source
- arXiv: 2110.14168
- Raw markdown: `../../../raw/research/single-sample-llm-learning/19-C-4-cobbe-training-verifiers-gsm8k.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/C-4-cobbe-training-verifiers-gsm8k.pdf`

## Related
- [[process-outcome-feedback]]
- [[lets-verify-step-by-step]]
- [[math-shepherd]]
- [[_overview]]
