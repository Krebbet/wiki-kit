# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-05-27] research+ingest | recurrent reasoning models

Fourth research+ingest run, directed at recurrent reasoning / latent computation. Sources in `raw/research/recurrent-reasoning/` (6 abstracts + 6 PDFs, all text-only pymupdf captures; 32 broken image refs — acceptable). 5 new wiki pages written in parallel:

- `[[research/ouro]]` — Ouro (Zhu et al., arXiv:2510.25741, Oct 2025; ByteDance Seed). Pre-trained LoopLM family (1.4B/2.6B) trained on 7.7T tokens. Two-stage adaptive halting: Stage I entropy-KL regularization (uniform prior) during pretraining prevents depth-collapse; Stage II freezes LM weights, fine-tunes a linear exit gate on loss-improvement binary cross-entropy. KV-cache analysis: last-step reuse preserves quality (4× memory overhead); first-step reuse catastrophic. Mechanistic finding: Capo experiment shows ≈2 bits/param information capacity regardless of loop count — gains come from manipulation (Mano task, +23%), not storage. Ouro-2.6B matches Qwen3-8B/Gemma3-12B. Stage II gate is the closest published analogue of Exp 1.
- `[[research/rltt]]` — RLTT (Williams & Tureci, Princeton, arXiv:2602.10520, Feb 2026). Distributes GRPO reward across all T_max loops via per-loop weighting ω_t; three strategies (Exit PDF / Progressive / Uniform); +14.4% MATH-500, +16.6% AIME24, +18.7% GPQA zero-shot on Ouro-2.6B-Thinking. Not relevant to Exp 1 Phase 1 (frozen weights); becomes relevant for RL post-training phase.
- `[[research/looprpt]]` — LoopRPT (Tang et al., arXiv Mar 2026; Harbin/Tsinghua/HKUST). First RL pre-training framework for looped LMs. Four components: (1) entropy-based hard-token selection via EMA teacher; (2) step-wise rewards R(k) = Δ_acc(k) − C(k) with difficulty-aware λ_t; (3) noisy rollouts via KV injection; (4) truncated REINFORCE without critic. Trains on OMNI-MATH competition math. Pareto dominance over Ouro baseline and Qwen3-1.7B CoT.
- `[[research/coconut]]` — Coconut (Hao et al., arXiv:2412.06769, Dec 2024; Meta). Latent-mode reasoning: feeds h_{t-1} ∈ ℝ^d as next input embedding during `<bot>`/`<eot>` delimited segments, bypassing decode+re-embed. Multi-stage curriculum training (N+1 stages, optimizer reset between, loss masking). Implicit BFS emerges: step-1 broad candidate generation, step-2 narrowing. Key constraint: requires training from scratch (not post-hoc application to Huginn). Halting: binary `<eot>` classifier or fixed count (fixed count used in practice).
- `[[research/etd]]` — ETD (Koishekenov et al., arXiv Oct 2025). Angular-distance (Kneedle algorithm) identifies E/T/D partition in a pretrained LLM; only T block loops k times; OLMo-2 1B: 7–4k–5 partition. +28.4% GSM8K, +36% MATH with k=3; MATH regresses at k>4 (unexplained). ACT variant learns per-token halting via sigmoid halt head; uses final T-block output (not weighted mixture). Key for Exp 1: ETD shows angular distance as a cheap, post-hoc way to identify "thinker layers" without re-pretraining — could identify where Huginn's core block should be re-entered.

New index section: "Research — Latent / continuous reasoning" (coconut, etd). Ouro and LoopRPT added to "Research — Loop / recurrent-depth architectures". huginn.md updated with R4 anomaly warning and Latent CoT probing section (Lu et al. arXiv:2507.02199) — EXP1_INSERTION_POINT flag for final step.

Notable G3 relevance: Ouro's Stage II (freeze LM + train exit gate on loss-improvement) is the direct precedent for Exp 1's halting mechanism. Ouro-1.4B/2.6B are lighter Exp 1 base candidates vs Huginn-3.5B. ETD's angular-distance partition analysis could identify "natural" thinker layers in any pretrained LLM, useful for deciding which layers to loop.

---

## [2026-05-27] new page | wiki/research/rltt.md

User-directed page write: RLTT (Rewarding Latent Thought Trajectories in Looped Language Models), Williams & Tureci, Princeton preprint arXiv:2602.10520, Feb 2026. Sources: `raw/research/recurrent-reasoning/02-rltt-abs.md` and `07-rltt-pdf.md`. Page covers: core credit-assignment mismatch (GRPO rewards only terminal loop P_θ^(Tmax)); full RLTT gradient formula in LaTeX; three weighting strategies (Exit PDF, Progressive, Uniform) with ablation finding that the RLTT–GRPO gap dominates weighting-strategy differences; memory overhead (halved ppo_max_token_len_per_gpu to 8192, 10% wall-clock savings from emergent length shortening); benchmark results (MATH-500 +14.4%, AIME24 +16.6%, BeyondAIME +10.0%, GSM8K +34.3%, GPQA +18.7% zero-shot); loop-level analysis (largest gains at 1–2 loops); Exp 1 relevance note (not applicable in Phase 1, becomes relevant when Huginn weights unfrozen for RL post-training). G3 High, G1 Low, G2 N/A.

---

## [2026-04-30] research+ingest | selective replacement and training (non-quantization)

User-directed second research run: "methods that focus on selectively replacing parts of a network and training the piece, less concentrated on quantization." 15 candidate papers proposed across 5 buckets (insert-and-train PEFT; replace/grow-and-train function-preserving; train-then-compose; find-and-retrain; concept-anchor-and-queued-G3-targets), all 15 approved. Captured to `raw/research/selective-replacement-and-training/` (15 PDFs via marker engine, CPU-forced; 15 arXiv abstracts as backup). audit_captures clean.

Ingest dispatched 15 sonnet subagents in parallel; all succeeded but 13/15 produced summaries with schema drift (custom frontmatter keys, renamed section headers like "## Core Method" / "## One-paragraph summary"). Orchestrator wrote a one-shot normaliser to canonicalise frontmatter and rename header variants — all 15 then passed `parse_summary` validation. Schema-drift root-cause and proposed kit-level fix (`tools.ingest_plan.normalise_summary`) logged to `master_notes.md` as kit-scope harvest item.

Goal-relevance ranking *(synthesis)*:
- **G1 STRONG**: Sheared LLaMA (canonical LLM-scale prune+recover), BTM/BTX (independent expert training + recombination), Sparse Upcycling (FFN→MoE copy-and-train), DEMix (FFN-granularity isolated training), LegoNN (explicit interface contract), Lottery Ticket BERT (sparse-subnet isolation).
- **G1 direct**: bert2BERT, LiGO (function-preserving growth + train).
- **G1 partial**: LoRA, Adapters-Houlsby (insert-and-train at adapter granularity, not block).
- **G3 PRIMARY**: MoD (per-token depth routing).
- **G3 STRONG**: Sparse Upcycling, BTX (per-token FFN-expert routing), CALM (per-token early exit), BTM (ensemble routing), DEMix (domain-conditional).

Wrote 14 paper pages (modular-deep-learning written earlier in this date as the survey hub) + 1 conflict page (`shortgpt-vs-sleb-redundancy-metric.md`, documented as a missing-head-to-head with no winner ruling) + substantially rewrote both concept pages (block-isolation-training expanded to 5 isolation flavours; token-conditional-routing populated with full 5-primitive taxonomy and Modular-DL-Survey §4.2.3 caution on token-routing-vs-specialisation tension). Updated research-queue: struck shortgpt/mod/calm; added adalora, switch-transformer, v-moe, hash-routing. Index gained new sections for PEFT, MoE/domain-expert pools, Model growth, Structured pruning, Token-conditional routing / dynamic depth.

Notable caveats baked into the wiki: BTM is arXiv-only (validated post-hoc by BTX); LegoNN's CTC dependency limits transfer to autoregressive decoder-only stacks; Lottery Ticket BERT is BERT-base / unstructured-sparsity only; bert2BERT's FPI gap at LLM scale is unstudied; MoD has a train/inference distribution gap on top-k routing not characterised at long context.

Harvest items logged: subagent schema-drift normalisation (kit scope, in `master_notes.md`).

## [2026-04-30] ingest (survey) | Pfeiffer et al. "Modular Deep Learning" (TMLR 2023)

Created `wiki/research/modular-deep-learning.md` as the taxonomy hub page for the wiki. This is a survey paper so used taxonomy-first format rather than standard method-paper format. Page covers: 4-axis taxonomy (computation function / routing function / aggregation function / training setting), explicit G1/G2/G3 goal-mapping into taxonomy cells, §4.2.3 token-level routing caution (impedes task-level specialisation via load-balancing constraints), all 12 §9.1 open questions, and a full Related section cross-linking every existing wiki page into its taxonomy cell(s). Updated `index.md` with new "Survey / taxonomy" section and 8 previously unindexed research pages (lora, adapters-houlsby, btm, btx, sparse-upcycling, demix, bert2bert, ligo, lottery-ticket-bert, sheared-llama) added to four new index sections. Pages `calm`, `mod`, `legonn`, `shortgpt` referenced in the taxonomy but not yet ingested — noted in the page's Related section.

---

## [2026-04-30] bootstrap | modular transformer architecture research

Initial bootstrap. Schema and commands tailored for modular transformer architecture research — three driving experiments: (G1) training isolated transformer blocks that remain swappable while preserving generation quality, (G2) learning per-block dynamic parameter allocation during training, (G3) token-conditional routing through a pool of blocks rather than a static n-layer stack. Source policy: papers as source of truth, blogs / GitHub / talks as method-discovery scouts only. Each paper page carries a `## Credibility` block (venue, code, weights, ablation rigor, replication status). Tone: terse and expert, LaTeX inline. Ready to receive first source.

## [2026-04-30] research+ingest | efficient single-block training (incl. quantization)

User-directed research run on "efficient methods to train single transformer blocks within a transformer architecture" with explicit emphasis on the quantization lineage. 12 candidate papers proposed across four buckets (quantization block-reconstruction lineage; module replacement; block pruning + heal; local / decoupled CNN-era), all 12 approved. Captured to `raw/research/block-training-quantization/` (12 PDFs via marker engine, CPU-only — flagged as harvest item to make CPU fallback automatic when GPU is busy; 12 arXiv abstract pages as backup). audit_captures clean.

Ingest dispatched 12 sonnet subagents in parallel, one per PDF; all succeeded. Goal-relevance ranking *(synthesis)*:
- **Direct G1**: BRECQ (block-by-block reconstruction), BERT-of-Theseus (Bernoulli-gated module replacement), DCR (deterministic-blend successor), DGL & GIM (CNN-era local-loss / gradient-isolated training), OmniQuant (block-wise differentiable PTQ), Iterative-Layer-Distill (heal-after-removal), LayerSkip (prefix-isolation pressure).
- **G3 baseline**: LayerSkip only (skip = simplest routing decision; per-token learned router is future work).
- **Background-mostly**: GPTQ, AWQ, SLEB, SpinQuant — foundational quantization / pruning context.

Wrote 12 paper pages + 2 concept anchors (`block-isolation-training`, `token-conditional-routing`) + 1 research-queue. Cross-references: within-batch links wired up (quant cluster, Theseus↔DCR, DGL↔GIM, SLEB↔LayerSkip, all G1-relevant pages → concept anchor); dangling links to next-run targets (SmoothQuant, ShortGPT, AdaRound, LLM.int8, MoD, CALM, Mixtral, LaCo, etc.) intentionally left in place per user direction — research-queue.md tracks them.

Notable caveats baked into the wiki: DCR is workshop+single-seed+no-code+no-heterogeneous-ops (page has prominent Limitations section); Iterative-Layer-Distill is single-lab Russian-language eval; LayerSkip is arXiv-only (not yet peer-reviewed); DGL & GIM are CNN-only (transformer-applicability gap explicit). Forward-flagged conflict: SLEB vs ShortGPT on the redundancy metric, to be resolved when ShortGPT is ingested.

Harvest item logged: `tools/capture_pdf.py` should pre-flight-check GPU availability and auto-fall-back to CPU when contended (kit scope, in `master_notes.md`).

## [2026-05-27] research page | loopformer

Wrote `wiki/research/loopformer.md` from two source files (`03-loopformer-abs.md`, `11-loopformer-pdf.md`). Covers: stagnant-state problem and four diagnostic metrics (CKA, curvature, anisotropy, prompt entropy); sinusoidal Fourier (t, Δt) step conditioning mechanism and AdaLN-style injection; shortcut-consistency training objective; elastic-depth inference; empirical results vs. TMLT-EE and Base-Loop-EE-Cons baselines. Page explicitly documents how step conditioning resolves Technical Challenge 2 (hidden-state observability) in exp1-router-replication: lifting the fixed-point symmetry h^(k) ≈ h^(k+1) makes loop step discriminable from hidden state alone. Added to index under Token-conditional routing / dynamic depth section.

## [2026-05-27] research page | sparse-logit-sampling

Wrote `wiki/research/sparse-logit-sampling.md` from two source files (`06-sparse-logit-sampling-abs.md`, `10-sparse-logit-sampling-pdf.md`). Paper: "Sparse Logit Sampling: Accelerating Knowledge Distillation in LLMs" (Anshumann, Zaidi, Kedia et al., Samsung Research, arXiv 2503.16870, Mar 2025). Covers: formal proof of top-K KD bias (gradient formula shows upscaling factor $\sum_{j\in\mathcal{K}} t_j$ corrupting gradient direction and norm); RSKD importance-sampling estimator ($q = t^\tau$, $\tau=1$, $N=12$ tokens); unbiasedness theorem (Appendix A.7); storage comparison (3.6 TB vs. 90 TB top-K 300 for 100B tokens); empirical results (RSKD matches FullKD quality, top-K 12 has 4.7% ECE vs. 0.2%). Key implication for Exp 1 Challenge 4: top-K $p_\text{static}$ cache is a biased training signal; must switch to RSKD sampling format. This upgrades Challenge 4 severity. Added to index under new "Research — Knowledge distillation (offline / cached logits)" section.

## [2026-05-27] research+ingest | loop LLM + adaptive computation (full run)

Third research+ingest run, directed at Experiment 1 technical challenges. Sources split across two capture batches: `raw/research/loop-computation/` (Universal Transformers, ACT, PonderNet, Depth-Adaptive Transformer, Huginn, Parcae + 2 GitHub READMEs) and `raw/research/loop-challenges/` (Mechanistic Analysis of Looped LMs, LoopFormer, AdaPonderLM, TIDE, Sparse Logit Sampling, Comparing Fixed vs ACT). PDF captures are text-only (marker ran without image extraction; image refs broken but text content intact — acceptable for synthesis). Audit showed 120 broken image refs in loop-computation/ and 18 in loop-challenges/.

12 wiki pages written in parallel:

- `[[research/universal-transformers]]` — weight-tied recurrent transformer with ACT; Turing-complete; foundational base for Huginn. ICLR 2019.
- `[[research/act]]` — original differentiable halting; remainder trick; gradient bias at halting boundary confirmed; prefer PonderNet for Exp 1. arXiv 2016.
- `[[research/pondernet]]` — geometric halt distribution + KL regularization; unbiased gradient; recommended Exp 1 halting mechanism. NeurIPS 2021.
- `[[research/depth-adaptive-transformer]]` — per-token depth in seq2seq; state-copy + layer-specific KV projection solves attention consistency. ICLR 2020.
- `[[research/huginn]]` — Exp 1 base model; EXP1_INSERTION_POINT documented (after core_block(s, e), observing s_i ∈ ℝⁿˣ⁵²⁸⁰ unnormalized; code in recpre/raven_modeling_minimal.py). arXiv 2025.
- `[[research/parcae]]` — Exp 1 fallback base; spectral-norm ZOH stability; 140M–1.3B checkpoints. arXiv 2026.
- `[[research/mechanistic-looped-lms]]` — Prop 4.1: input-injection LMs converge to cyclic fixed points within k≈1-2 iters; h^(k) encodes no step signal after recurrence 2; Prop 4.2: attention patterns freeze. Confirms Challenge 2 is severe; step conditioning required before halt head is viable.
- `[[research/loopformer]]` — (t, Δt) sinusoidal Fourier step conditioning via AdaLN zero-init breaks cyclic fixed-point symmetry; required mitigation for Challenge 2. arXiv 2026.
- `[[research/adaponderlm]]` — monotonic per-token halting masks + where(mask, K_new, K_prev) KV-reuse; concrete, FlashAttention-compatible solution for Challenge 3 (variable-depth attention consistency). arXiv 2025.
- `[[research/tide]]` — post-training per-token early exit via cosine-convergence routers; KV-cache-safe post-hoc design. NeurIPS 2023.
- `[[research/sparse-logit-sampling]]` — top-K logit cache is a biased KD estimator (formal theorem); RSKD importance sampling required; upgrades Challenge 4 severity. arXiv 2025.
- `[[research/repeat-rnn]]` — fixed-ρ Repeat-RNN matches ACT on parity/addition; confirms Challenge 5 (trivial solution trap) is concrete. arXiv 2017.

Experiment proposal updated: Challenge 2 severity upgraded from "empirical unknown" to "confirmed severe — mitigation known"; Prop 4.1 cited; LoopFormer step conditioning identified as required fix. Research queue: universal-transformers, act, pondernet, depth-adaptive-transformer struck; looped-transformers, block-recurrent-transformers, deq remain.

Notable findings for implementation: (1) Huginn's prelude injects e read-only — the router must never modify e; (2) two consecutive KV cache copies needed for AdaPonderLM-style Option B routing (manageable per-layer overhead); (3) RSKD storage for 100B-token corpus ≈ 3.6 TB (borderline for single workstation — plan for streaming or subset caching).

---

## [2026-05-27] page update | huginn.md — Latent CoT probing + R4 anomaly warning

Added two blocks to `wiki/research/huginn.md` from Lu et al. arXiv:2507.02199 (Brown/Harvard, Jul 2025):

1. **"## Latent CoT probing — Lu et al. 2025"** (inserted before ## Source): no interpretable latent CoT in rank-trajectory analysis on arithmetic tasks; R4 dual-role anomaly (logit lens on raw R4 hidden state → incoherent; coda lens on same state → interpretable; R1–R3 are opposite); depth-scaling ceiling ~5% GSM8K w/o CoT across T=4..256 with slight degradation at very high steps. Consistent with mechanistic-looped-lms fixed-point convergence finding.

2. **R4 anomaly warning in EXP1_INSERTION_POINT**: the "observes $s_i$ unnormalized" spec is correct for steps i=1..r-1; the final step (i=r, after R4) has an incoherent representational state under raw logit lens due to R4's dual-role. Recommended mitigations: coda-lens pass-through (pipe $s_r$ through C1–C2 before router head) or step-index conditioning. Cross-references arXiv:2507.02199 pending a dedicated wiki page.

Sources added to huginn.md: `raw/research/recurrent-reasoning/04-latent-cot-huginn-abs.md`, `raw/research/recurrent-reasoning/06-latent-cot-huginn-pdf.md`.
