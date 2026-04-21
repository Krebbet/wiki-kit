# Constitutional AI: Harmlessness from AI Feedback

Bai et al. (Anthropic), 2022. Trains a harmless assistant *without harmlessness human labels* by replacing them with a small natural-language constitution (~16 principles) and AI-generated critiques/comparisons. Two stages: (SL-CAI) self-critique-and-revise then SFT on revisions; (RL-CAI / RLAIF) AI-labelled preference model trained on constitutional comparisons, then RL against it. Result: less harmful and less evasive than HH-RLHF at matched helpfulness.

## Method
- **Constitution**: ~16 short natural-language principles (harmfulness-targeted), randomly sampled per revision step. Few-shot exemplars stabilise the critique/revise format.
- **SL stage** — Critique → Revision → SFT.
  - Sample harmful prompt → helpful-only RLHF response (typically harmful).
  - Append "Critique Request" + principle → sample critique.
  - Append "Revision Request" → sample revision. Iterate (multiple revisions per prompt with re-sampled principles).
  - SFT a pretrained LM on the (prompt, final-revision) pairs, mixed with helpful samples to retain helpfulness.
- **RL stage** — RLAIF.
  - Sample response pairs from SL-CAI on red-team prompts.
  - Pose each pair as a multiple-choice "which is better per principle P?" question; use AI's choice (with optional CoT) as preference label.
  - Train a hybrid PM: AI labels for harmlessness, human labels for helpfulness.
  - RL the SL-CAI policy against the PM (RLAIF analogue of RLHF).
- Data scale: 182,831 red-team prompts (42k human + 140k model-generated) × 4 critique-revision pairs each; 135k helpful prompts.

## Claims
- Fig. 2/3: RL-CAI sits Pareto-above HH-RLHF on harmlessness-vs-helpfulness Elo at 52B; CoT variant pushes further. RL-CAI is *less evasive* (engages with sensitive queries explaining objections) yet less harmful.
- Fig. 4: At 52B+, AI multiple-choice judgement on 438 HHH comparisons approaches preference models trained on hundreds of thousands of human labels. CoT (with self-consistency over 5 samples) gives a further boost.
- Fig. 5: PM scores improve monotonically with revision count for harmlessness and HH (helpfulness drops slightly with revisions — the obvious tradeoff).
- Fig. 7: Generating an explicit critique before revision beats direct revision — i.e. the critique step itself adds value, not just the revision.
- Capability scaling: AI identification of harms improves significantly with model size; CoT reasoning amplifies it.

## Sample efficiency
The "seed" is order-of-ten natural-language principles plus a few-shot prompt template. From those, the system manufactures: (i) an entire SFT corpus of harmlessness revisions (~700k revisions) and (ii) a full preference-model dataset (AI-labelled comparisons), entirely without harm-specific human labels. The compression ratio of human bits → training data is extreme: ~16 principles are amplified into hundreds of thousands of training examples. This is the canonical demonstration that a *small set of natural-language rules* can substitute for a large preference-label dataset, provided the base model is capable enough to interpret and apply the rules. The constraint: rules must be expressible in language and the model must be able to detect violations.

## Relevance to the project
Most directly applicable insight here: **a constitution is a concept-component decomposition expressed as language**. Each principle is a sub-axis of "good output"; the model self-critiques along that axis. For concept-based learning from a single example, the analogue is: define the concept as a small set of natural-language "principles" (criteria the example satisfies), then use the model to (a) generate variants, (b) self-critique each variant against each principle, (c) train against the resulting decomposed signal. The CAI evidence that *generating a critique before revising* outperforms direct revision (Fig. 7) suggests the chain-of-thought decomposition itself is the load-bearing structure, not just the final preference. Caveat: CAI works at 52B; principle-following degrades at smaller scales, which is the regime David targets.

## Source
- arXiv: 2212.08073
- Raw markdown: `../../../raw/research/single-sample-llm-learning/28-G-2-constitutional-ai.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/G-2-constitutional-ai.pdf`

## Related
- [[self-refine]]
- [[reflexion]]
- [[../self-improvement/self-rewarding-lm]]
- [[../process-reward-models/_overview]]
