# Research Queue

Targets for future `/research` runs. Each entry is a dangling `[[wiki-link]]` that already appears on at least one wiki page; ingesting the underlying paper will make the link resolve. Entries are grouped by relevance to the three driving experiments (G1 swappable blocks, G2 dynamic per-block params, G3 token-conditional routing) and ordered by how often they're cited as baselines or predecessors in the existing corpus.

This file is curated by `/research` and `/ingest`. Lint should not warn on the dangling links these targets reference — they are intentional placeholders.

## Experiment 1 blockers — ingest before implementation

These are required reading before Experiment 1 (router-as-static-path) can begin. See `wiki/experiments/exp1-router-replication.md` for context.

- ~~`[[universal-transformers]]`~~ — ingested 2026-05-27. See [[research/universal-transformers]].
- ~~`[[act]]`~~ — ingested 2026-05-27. See [[research/act]].
- ~~`[[pondernet]]`~~ — ingested 2026-05-27. See [[research/pondernet]].
- ~~`[[depth-adaptive-transformer]]`~~ — ingested 2026-05-27. See [[research/depth-adaptive-transformer]].
- `[[looped-transformers]]` — "Looped Transformers as Programmable Computers"; alternative loop LLM framing; may be a better Exp 1 base than classic UT. (Giannou et al., ICML 2023)

## Experiment 1 background — ingest before joint fine-tuning

- `[[block-recurrent-transformers]]` — recurrent hidden state accumulated across loop iterations; relevant if per-token routing needs a step-independent KV cache. (Hutchins et al., 2022)
- `[[deq]]` — Deep Equilibrium Models; fixed-point framing of looped networks; router-halts-at-convergence alternative to step-count halting. (Bai et al., NeurIPS 2019)

## High priority — multi-source baselines

These targets are referenced by ≥2 already-ingested papers and are foundational baselines. Ingest first.

- `[[smoothquant]]` — outlier-migration W8A8 PTQ; baseline for [[awq]], [[omniquant]], [[spinquant]]; OmniQuant's LET is the differentiable evolution. (Xiao et al., ICML 2023)
- `[[adaround]]` (adaptive rounding) — layer-wise rounding optimisation; direct predecessor of [[brecq]]; baseline in PTQ literature. (Nagel et al., ICML 2020)
- `[[llm-int8]]` — outlier-aware W8A8 PTQ via mixed precision; predecessor cited by [[awq]] and [[gptq]]. (Dettmers et al., NeurIPS 2022)
- `[[switch-transformer]]` — foundational sparse-MoE; baseline for [[sparse-upcycling]], [[btx]]; canonical token-choice routing reference. (Fedus et al., JMLR 2022)
- `[[hash-routing]]` — deterministic hash-of-token routing primitive; alternative to learned softmax routers in MoE; cited as a routing-taxonomy cell in [[modular-deep-learning]] and [[concepts/token-conditional-routing]]. (Roller et al., NeurIPS 2021)

## Medium priority — concept anchors and important follow-ons

Single-source targets that fill conceptual gaps in the wiki structure.

- `[[adalora]]` — adaptive-rank LoRA variant; G2-relevant successor of [[lora]] (rank dynamically allocated per layer based on importance). (Zhang et al., ICLR 2023)
- `[[mixtral]]` — production MoE with expert-choice routing; relevant for G3 expert-routing precedent and as a real-world block-pool case. (Jiang et al., 2024)
- `[[v-moe]]` — vision Mixture-of-Experts; baseline for [[sparse-upcycling]] vision experiments; expert-choice routing in ViT. (Riquelme et al., NeurIPS 2021)
- `[[laco]]` — block-pruning sibling of [[sleb]]. (Yang et al., 2024)
- `[[knowledge-distillation]]` — concept page covering the KD background that [[bert-of-theseus]], [[dcr]], [[iterative-layer-distill]] build on.

## Low priority — single-source dangling refs

Cited once, fill in if/when convenient:

- `[[distilbert]]`, `[[bert-pkd]]`, `[[tinybert]]`, `[[mobilebert]]` — KD baselines from [[bert-of-theseus]]
- `[[layerdrop]]` — structured dropout precursor to [[layerskip]]
- `[[pabee]]` — early-exit complement; [[bert-of-theseus]] cites
- `[[fisher-information-matrix]]`, `[[mixed-precision-quantization]]`, `[[adaptive-rounding]]` — concept pages around [[brecq]]'s theory
- `[[layer-wise-quantization]]`, `[[post-training-quantization]]` — concept umbrella pages
- `[[linformer]]`, `[[performer]]` — heterogeneous attention operators that [[dcr]] flags as future-work targets
- `[[draft-and-verify]]` — speculative decoding alternative to [[layerskip]] / [[calm]]
- `[[predsim]]`, `[[cpc]]`, `[[dni]]`, `[[ddg]]` — decoupled-learning siblings of [[decoupled-greedy-learning]] and [[greedy-infomax]]
- `[[quarot]]` — concurrent rotation-based PTQ to [[spinquant]]
- `[[qlora]]` — LoRA + quantization context for [[omniquant]]
- `[[minillm]]` — distillation baseline cited by [[iterative-layer-distill]]

## Recently ingested (no longer queued)

Third `/research+ingest` run (2026-05-27) — loop LLM + adaptive computation:
- ~~[[universal-transformers]]~~ — ingested 2026-05-27.
- ~~[[act]]~~ — ingested 2026-05-27.
- ~~[[pondernet]]~~ — ingested 2026-05-27.
- ~~[[depth-adaptive-transformer]]~~ — ingested 2026-05-27.

Also ingested (not previously queued, found during this research run):
- ~~[[huginn]]~~, ~~[[parcae]]~~, ~~[[mechanistic-looped-lms]]~~, ~~[[loopformer]]~~, ~~[[adaponderlm]]~~, ~~[[tide]]~~, ~~[[sparse-logit-sampling]]~~, ~~[[repeat-rnn]]~~ — all ingested 2026-05-27.

Second `/research+ingest` run (2026-04-30):
- ~~[[shortgpt]]~~ — ingested 2026-04-30. Conflict with [[sleb]] documented at [[conflicts/shortgpt-vs-sleb-redundancy-metric]].
- ~~[[mod]]~~ — ingested 2026-04-30 (Mixture-of-Depths). Now the primary citation on [[concepts/token-conditional-routing]].
- ~~[[calm]]~~ — ingested 2026-04-30. Pairs with [[layerskip]] as the per-token decision layer for prefix-isolation training.

## Resolved conflicts

- **[[sleb]] vs [[shortgpt]]** on redundancy metric — documented at [[conflicts/shortgpt-vs-sleb-redundancy-metric]] (no winner ruling; missing-head-to-head). Status: open for awareness, no action required unless a future paper runs the head-to-head.
