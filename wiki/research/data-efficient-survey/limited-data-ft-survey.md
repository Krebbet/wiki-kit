# Fine-tuning LLMs with Limited Data: A Survey and Practical Guide

Szep, Rueckert, von Eisenhart-Rothe, Hinterwimmer (TUM, 2024; arXiv:2411.09539). A pragmatic, single-stage-by-stage map of the post-pretraining pipeline under data scarcity: parameter-efficient fine-tuning (PEFT), domain/cross-lingual adaptation, specialization, and preference alignment. Aimed at practitioners adapting encoder *and* decoder PLMs (1B–~400B) when annotation budgets are in the 10²–10⁵ range.

## Scope

In scope (the survey's four pillars):
- **§3 PEFT** — selective, reparametrization (LoRA family), soft prompts / prefix tuning, adapters, hybrids, with selection criteria and inference-overhead tradeoffs.
- **§4 Domain & cross-lingual FT** — continued pre-training (CPT), pattern-exploiting training (PET), meta-learning (encoder branch), intermediate FT, multi-task instruction tuning, MoE, instruction-design choices.
- **§5 FT for specialization** — embedding learning, contrastive/adversarial objectives, semi-/un-/active learning, instruction tuning for narrow tasks, catastrophic-forgetting mitigation, hyperparameter defaults.
- **§6 Preference alignment** — RLHF/RLAIF, direct methods (DPO, IPO, KTO, R-DPO, JPO), reference-free methods (CPO, ORPO, SimPO, SLiC-HF, RRHF), alignment-during-SFT (CoH, SPIN), preference-data quality and scaling.

Out of scope (explicit or by omission): pretraining from scratch, retrieval architecture details, agentic systems, single-example RL fine-tuning, reasoning-trace bootstrapping (STaR/rStar), test-time training, mechanistic interpretability of fine-tuning, and reward design beyond pairwise preference signals.

## Method taxonomy

The survey's organising backbone (with reference to Pfeiffer et al., 2023, for PEFT):

| Family | Section | Composes via | Representative methods | Sweet-spot data size |
|---|---|---|---|---|
| Selective PEFT | §3.1 | sparse subset of existing weights | BitFit, LayerNorm tuning, gradient-selected subnets | small; cheap baseline |
| Reparametrization | §3.1 | low-rank deltas to existing weights | LoRA, QLoRA, AdaLoRA, KronA | 10k–100k+ samples |
| Soft prompts / IA³ | §3.2 | prepended/learned activations | Prefix-Tuning, Prompt-Tuning, P-Tuning, IA³ | a few thousand (large models only) |
| Adapters | §3.3 | inserted feedforward modules | Houlsby, Pfeiffer, Parallel/Ladder side-tuning | moderate to large |
| Hybrid | §3.4 | combinations | Compacter, UniPELT, MAM | extremely low-resource |
| Continued pre-training | §4.1 | self-supervised on in-domain corpus | DAPT, TAPT, vocab extension | from ~100k tokens |
| PET (encoders) | §4.2 | cloze reformulation + verbalizers | PET, ProtoVerb, evolutionary verbalizers | true few-shot |
| Meta-learning (encoders) | §4.2 | bi-level / metric-space | MAML, ProtoNets, contrastive variants | few-shot per class |
| Intermediate FT | §4.2 | staged supervision on related task | STILTs, task-adaptive PT | label-rich intermediate |
| Multi-task instruction tuning | §4.2 | broad instruction mixtures | T0, FLAN, SuperNI | heterogeneous, large |
| MoE routing | §4.2 | conditional expert selection | Switch, AdaMix, Phatgoose | large-scale decoders |
| Embedding learning | §5.1 | retrain/extend token embeddings | entropy-based vocab expansion, alignment maps | low-resource cross-lingual |
| Contrastive / adversarial | §5.2 | representation alignment | SimCSE, language-invariant adapters | paired or unpaired |
| Semi-/unsup. / active learning | §5.3 | leverage unlabeled data | self-training, FixMatch-style, AL by uncertainty | ≥1k labeled |
| RLHF / RLAIF | §6 | reward model + PPO | InstructGPT, d-RLAIF | 100k+ preferences |
| Direct PA | §6 | classification on preference pairs | DPO, IPO, KTO, R-DPO, JPO | 10k+ pairs (KTO works on weaker binary) |
| Reference-free PA | §6 | drop reference model | CPO, ORPO, SimPO, SLiC-HF, RRHF | <10k feasible |
| Alignment-during-SFT | §6 | curated SFT or self-play | LIMA, CoH, SPIN | 1k–10k high-quality |

Tables 1–3 in the paper are the canonical condensed view; Table 4 + Appendix A give an encoder-task PEFT cheat sheet.

## Key claims and findings

**PEFT (§3).**
- Full FT becomes preferable only at million-sample scale; PEFT matches or beats it under ~100k (Zhang 2023a; Lialin 2024). LoRA and adapters are the most robust defaults across model sizes.
- Selective methods underperform but are essentially free at inference; reparametrization can be merged in (no latency); adapters cost up to ~40% slowdown; soft prompts cost 30–40% and converge slowly except at very large scale.
- Scaling PEFT *parameters* yields marginal gains beyond a small budget; scaling the *base model* (with quantization to fit) dominates (§3.6).

**Domain / cross-lingual (§4).**
- CPT on as little as ~100k tokens of in-domain text is beneficial, especially when paired with PEFT to limit forgetting. Relevance > quantity for proxy/mixed-domain CPT.
- For decoders, longer CPT risks catastrophic forgetting (Kalajdzievski 2024); encoders tolerate more.
- Multi-task instruction tuning produces strong zero-shot generalists but suffers negative task transfer without careful mixture design; MoE mitigates this by routing.
- "To mask or not to mask?" — including prompt tokens in the loss with a small weight (0.01–0.1) regularises generalization when instructions are long and data is <15k (Shi 2024; Huerta-Enochian 2024).

**Specialization (§5).**
- Targeted (data-influence-selected) instruction tuning matches full-data performance with 10–15k examples (Xia 2024; Chen 2023a). Core subsets transfer across model scales.
- For multilingual closed-generation, SFT scales as a power law with an elbow around 10k–40k for PEFT; *model size matters more than FT data size or PEFT parameter count*.
- Practical SFT defaults: lr 2e-5 (range 5e-6–5e-5), batch 1–8 with grad accumulation, AdamW + cosine, warmup 3–5%, grad clip 1, 2–3 epochs (up to 20–25 in extreme low-data with early stopping). LoRA r=α=16, dropout 0.05.

**Preference alignment (§6).**
- RLHF (PPO + reward model) demands 100k+ preferences and is unstable; reward modeling itself is robust to ~30% label noise (Shen 2024).
- DPO and variants are the practical default. KTO works from weaker binary (good/bad) signals and is more sample-efficient in the 1B–30B range. IPO regularises against reward hacking. R-DPO penalises verbosity; JPO generalises pairs to arbitrary input pairs.
- Reference-free methods (CPO, ORPO, SimPO) succeed at <10k samples; CPO beats DPO on translation with 22k samples; ORPO is competitive at 141B with 7k samples; SimPO leads benchmarks but lacks theoretical justification.
- **Alignment-during-SFT (LIMA, SPIN, CoH)** can rival explicit PA when SFT data is high-quality. SPIN matches its 50k baseline with 1.8k curated examples.
- Scaling: data scaling dominates reward-model scaling (2× data > 4× reward-model size; Gao 2023). At least ~2k pairs are needed for PPO to escape baseline; smaller models reward-hack earlier; ≥7B exhibits markedly better sample efficiency.
- Downstream cost: PA can hurt knowledge-intensive and math performance, especially CPO/ORPO without an SFT-loss regulariser; DPO begins to hurt downstream after one epoch (Tunstall 2024).

**Discussion (§7).**
- Encoder vs decoder: RoBERTa/DeBERTa (335M) often matches T5-11B on NLU under low-resource conditions thanks to bidirectional attention and dense token supervision. Decoders win when generation or instruction-following is required.
- Cross-lingual: English prompts and "think in English then answer" CoT outperform target-language prompting in few-shot.
- **Model merging** (Model Soup, SLERP) into single weight-space combinations frequently tops Open LLM Leaderboard; effective for low-resource languages; ineffective below ~2B params.

## Coverage gaps

Relative to David's project (single-sample, concept-based fine-tuning of small LLMs), the survey's blind spots:

- **No discussion of single-sample / 1-example fine-tuning.** The lowest data regime considered is "few-shot" in the PET / meta-learning sense (K examples per class) and "1k–10k high-quality" for alignment. Single-prompt RL fine-tuning (e.g., Wang et al. "RL with one training example", or critique-based 1-problem FT) is absent.
- **Concept-level / structured rewards are not covered.** Preference alignment is treated entirely as scalar/pairwise human or LLM judgments. There is no treatment of process rewards, verifier-guided rewards, or concept-decomposition rewards (PRM800K, Math-Shepherd, etc.).
- **Self-improvement / bootstrapping loops are missing.** STaR, rStar-Math, Reflexion, Self-Refine, Constitutional AI's self-critique are not in the taxonomy. SPIN is the closest analogue and gets one paragraph.
- **Test-time training and in-context-learning-as-implicit-update are absent.** Akyürek-style TTT and ICL-as-gradient-descent literature (von Oswald, Garg) are not surveyed despite being directly relevant to "what does a single example update."
- **Mechanistic findings about *what* changes during FT** — sparse subnetworks (e.g., RL-induced sparse subnets), induction heads, representational geometry — are not discussed; the survey is method-by-method, not mechanism-by-mechanism.
- **RLVR / verifiable-reward RL** (DeepSeekMath GRPO, DeepSeek-R1) postdates the survey's preference-alignment framing; closed-form rewards on reasoning traces are not covered.
- **Evaluation of "concept transfer"** — whether a single fine-tune on an instance generalises to a concept class — has no framework here. The survey's metric is task accuracy on a held-out test set.

## Relevance to the project

Use this as the **map**, not the territory. Three concrete uses:

1. **Landmark check** — the survey confirms the empirical floor: best practice in the literature still treats <1k samples as "extreme low-data" requiring hybrid PEFT + careful regularization. David's regime (n=1 with concept-level signal) is genuinely off this map, which is itself useful evidence that a novel framing is required.
2. **Method palette** — the PEFT + alignment matrix (LoRA/IA³ × DPO/KTO/SimPO × SPIN/LIMA-style curation) is the implementation surface to instrument single-sample experiments on; the survey's hyperparameter defaults (lr 2e-5, LoRA r=16, etc.) are reasonable starting points.
3. **Threads to pull** — KTO (binary/asymmetric feedback), SPIN (self-play from one seed set), data-influence selection (Xia 2024), and "prompt-token loss as regularizer" (Shi 2024) are the survey's nearest neighbours to single-sample concept learning; each warrants a dedicated wiki page.
4. **Counter-evidence to track** — claims that "model size dominates over data size for PEFT" and "PA can hurt downstream after one epoch" set quantitative expectations that any single-sample method will be measured against.
5. **Citation skeleton** — the survey's reference list is a curated reading list for the project's broader landscape; treat it as bootstrapping the citation graph, not as ground truth on any individual claim.

## Source

- arXiv: 2411.09539 ("Fine-tuning Large Language Models with Limited Data: A Survey and Practical Guide")
- Raw markdown: `../../../raw/research/single-sample-llm-learning/09-09-ft-limited-data-survey.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/09-ft-limited-data-survey.pdf`

## Related

- [[../single-sample-rl-finetuning/_overview]] — single-example RL fine-tuning (the regime the survey does not reach).
- [[../meta-learning-few-shot/_overview]] — MAML / ProtoNets, the few-shot tradition the survey cites in §4.2.
- [[../self-improvement/_overview]] — STaR, SPIN, Reflexion, Self-Refine; self-bootstrapping methods this survey only partially covers.
