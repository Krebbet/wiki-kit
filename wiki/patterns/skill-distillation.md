# Skill distillation: when to collapse multi-agent into single-agent

CUHK + LIGHTSPEED paper (April 2026) that directly attacks an architectural assumption: that multi-agent systems are uniformly worth their coordination cost. The empirical finding is that distilling the *same* multi-agent pipeline into a single-agent skill is sometimes massively beneficial (+28pp accuracy) and sometimes actively harmful (−2pp) — *on the same task*. The variance is not driven by task complexity but by the **evaluation metric**. The paper's central contribution is **Metric Freedom (F)**, a predictor computable from baseline runs *before* any distillation is attempted, that tells you which regime you're in. F has a strong global correlation with skill-distillation lift (r = −0.85, p < 0.0001 across 18 task-metric pairs).

This is a fifth mitigation class for [[topology-taxonomy#long-horizon-context-loss]] alongside materialise-state, adaptive-compression, tiered-memory, and middleware-substrate: **eliminate the handoff entirely when F predicts you can**.

## Metric Freedom (F)

**Definition**: F measures the topological decoupling between an agent's *behavioural variation* and its *score variation*. Given n independent baseline runs per question:

- Pairwise score distance matrix: `D_score_ij = |s_i - s_j|`
- Behavioural distance matrix: `D_out_ij` (task-appropriate structural distance — Jaccard for sets, Hamming for categories) or `D_trace_ij` (`1 - cos_sim` of trace embeddings).
- Apply Mantel test → Spearman rank correlation `r_M` between ranked behavioural and score distance matrices.
- **F = 1 − r_M** ∈ [0, 2]. F > 1 is "extreme high freedom".

**Two instantiations:** `F_out` (final outputs) and `F_trace` (trace embeddings via `text-embedding-3-large`). They correlate strongly (r ≈ 0.78) and yield similar predictions.

**Three regimes:**

| F range | Regime | Skill distillation effect | Example |
|---|---|---|---|
| F ≈ 0–0.3 | Rigid / knife-edge | **Highly beneficial** — narrow corridor of correct behaviour; structured guidance pays off | Causal Estimation MSA (F ≈ 0.1–0.2): only one causal method works |
| F ≈ 0.3–0.6 | Mid-freedom | Moderate, reliable benefit | Text-to-SQL (F = 0.5) |
| F ≈ 0.7–1.3 | Free / flat | **Distillation hurts** — many diverse paths yield equally valid scores; structural constraints harm exploration | Feature Engineering AUC (F ≈ 1–1.3) |

**Theoretical grounding** (Theorem 3.1): `Lift(π) ≤ L₀ (1 − F + Δₙ) · W̃₁(P_π, P₀)`. As F → 1, the gain ceiling vanishes regardless of how much the distilled skill shifts the output distribution.

**Computation cost**: F requires n=6 runs × m=6 questions per dataset (≈ $5.16 operating point), reusing baseline runs already needed for evaluation — *zero additional inference overhead*.

## AdaSkill: the distillation procedure

Two-stage prompt-engineering pipeline (no model fine-tuning):

**Stage 1 — Adaptive MAS Converter** (always runs): decomposes the source MAS into four component classes — callable tools, domain knowledge, pipeline structure, coordination mechanisms — then applies metric-invariant rules:

- Coordination mechanisms are **always discarded** (a single large model internalises coordination natively).
- Callable tools are **always retained**.
- Pipeline structure and domain knowledge are injected proportional to F: near-zero F → mandatory step sequences; intermediate F → conditional hints; high F → bare-minimum reference knowledge only.
- Automated validation: tool imports verified, no pipeline steps leak into high-F skills.

**Stage 2 — Skill Iterator** (only activated for mid- and high-F metrics): a four-agent loop — Explore Agent (analyses benchmark once), Main Agent (orchestrates, tracks history, decides stopping), Runner (executes skill on train/val with verbose traces), Analyzer (spawned **statelessly** per iteration to prevent compounding hallucinations; diagnoses 1–3 most severe failure traces and injects atomic fixes). Terminates on convergence, >95% accuracy, oscillation, or budget exhaustion.

Stage 2 is *deliberately disabled* on low-F metrics because the knife-edge landscape causes oscillation: fixing one failure breaks another.

## Empirical results

4 tasks, 11 datasets, 6 metrics. MAS baselines: APEX-SQL (Text-to-SQL), CAIS (Causal Estimation), MATMCD (Causal Discovery), FELA (Feature Engineering). Backbone: Claude Sonnet 4.6 throughout.

**When distillation matches/exceeds MAS (low-F)**:
- Causal Estimation MSA (F ≈ 0.2): AdaSkill 89.7% MSA on QRData vs CAIS at 83.3% (+6.4pp). Latency 52s vs 123s. The MAS Compiler (faithful pipeline compilation) hits 82.1% at $0.608 — 3× costlier and worse.
- Causal Discovery Sachs (F = 0.24): F1 = 0.952, +8.3pp over raw.
- Text-to-SQL (F = 0.50): +8.8pp EX on BIRD-147; +5.8pp on Spider-120 over Base Agent — without MAS overhead.

**When distillation hurts (high-F)**:
- Causal Estimation MRE (F ≈ 0.8): the same trajectories that gave +28pp under MSA show no advantage or actively degrade under MRE. AdaSkill correctly strips structure and still wins (MRE 23.1 vs CAIS 54.0 on Textbook — lower better).
- Causal Discovery AutoMPG (F = 0.41): adaptive skill slightly trails Base Agent (0.632 vs 0.670), consistent with F's prediction.
- Feature Engineering (F = 1–1.3): AdaSkill discards MAS pipeline entirely. Best mean AUC on Taobao at $3.48 vs Original MAS $11.46; latency 45 min vs ~10 hours.

**Global correlation**: r(F_out, lift_norm) = **−0.85, p < 0.0001, n=18**; r(F_trace, lift_norm) = **−0.77, p < 0.001**.

**Component ablation** — which piece drives the negative correlation: pipeline structure does (r = −0.83 with lift). Tools (r = +0.72) and knowledge (r = +0.52) yield consistent gains across the full F spectrum. So in high-F settings the *structural constraint* is the harm, not the tools or knowledge.

## Cost / latency / context-window argument

The paper quantifies efficiency wins explicitly:

- **Cost**: AdaSkill is **1.4–8× cheaper** than Original MAS across tasks. Feature Engineering: $3.48 vs $11.46.
- **Latency**: **3–15× faster**. Feature Engineering: 45 min vs ~10 hours.
- **Prompt caching amplifier**: single-agent methods get 30–40% cost back from prompt caching; Original MAS baselines get *near-zero* cache benefit because of dynamic inter-agent messaging. This widens the efficiency gap beyond the raw cost ratio.
- **Context fragmentation** is named directly in the abstract as a structural cost of MAS; the paper does not separately quantify token loss at handoffs but attributes the cost wins to fewer model calls and caching eligibility.

## Self-documented limits

- **Per-metric, not per-task**: F must be computed for each metric. Multi-metric settings need composed per-metric modules.
- **Stage 2 oscillation on low-F**: explicitly disabled because iterative refinement is zero-sum on knife-edge landscapes.
- **F-estimation cost**: n=6 × m=6 (~$5). CE-Synthetic-MSA can't even compute F because raw accuracy is 97.8%, leaving no mixed questions after filtering.
- **Evaluation scope**: 4 tasks, all structured/scientific reasoning. Open-ended generation (creative writing) and continuous-action tasks not validated.
- **No weight-level distillation**: AdaSkill is prompt engineering only; whether F predicts utility for fine-tuning-based distillation (AgentArk-style) is untested.
- **Diversity planner dependency**: low-temperature inference collapses runs to identical outputs; a small preprocessing step seeds distinct strategies.

## Positioning vs other long-horizon-context mitigations

The wiki's other mitigation classes for [[topology-taxonomy#long-horizon-context-loss]] all keep the multi-agent design and try to reduce signal loss within it:

| Mitigation | Strategy | When it fits |
|---|---|---|
| [[ai-scientist-v2]] (materialise state) | Tree-search nodes carry full state tuples | Long-horizon research with branching exploration |
| [[context-folding]] (adaptive compression) | Per-step folding directives, variable granularity | Long single-chain trajectories like web agents |
| [[codified-context]] (tiered hot/cold) | Hand-engineered constitution + specialists + KB | Large codebases with institutional knowledge |
| [[cognitive-fabric-nodes]] (substrate) | Memory lifted into the network layer between agents | Multi-agent semantic intermediation |
| **Skill Distillation (this page)** | **Eliminate the handoff entirely** | **When F predicts the metric topology doesn't need a multi-agent decomposition** |

The other four are remediation; this is elimination. They are not in conflict — F is the branch condition that tells you which class to invest in. Low F → invest in handoff preservation (any of the first four). High F → collapse to single-agent and skip the handoff problem entirely.

## Why it matters

- **Frames a precondition no other paper in the wiki names.** Before asking "how do we preserve context across agent handoffs?", ask "should there be handoffs at all?" F operationalises the question.
- **Counterweight to the multi-agent default.** [[topology-taxonomy]] catalogues four MAS topologies and where each breaks; this paper argues that for some tasks *none* of the topologies is the right choice and a sufficiently capable single-agent + tools wins on cost, latency, *and* accuracy.
- **A computable predictor.** F is not a heuristic — it's a metric-distance correlation with theoretical grounding (Theorem 3.1) and a strong empirical fit (r = −0.85). Practitioners can compute it from baseline runs before committing to architecture.
- **Caching is structural, not incidental.** The paper's observation that MAS baselines get near-zero prompt-cache benefit (because of dynamic inter-agent messaging) is a separate, durable cost argument — independent of F — for revisiting MAS choices in cache-aware deployments.

## SDAR: multi-turn RL instance of distillation-into-weights

[[patterns/sdar]] (arXiv 2605.15155) is a concrete multi-turn-RL instantiation of the distillation-into-weights move: skills are retrieved and injected as privileged context for a teacher branch at training time, then internalized into policy weights via a token-level sigmoid gate — no skills are needed at inference. SDAR's "skills internalization" result (84.4% on ALFWorld-3B, outperforming skill-augmented Skill-GRPO* at 80.5% that *does* require skills at test time) is strong empirical evidence for the distillation-into-weights approach in multi-turn agentic settings.

## Source

- `raw/research/long-horizon-context/13-12-skill-distillation-pdf.md` (captured 2026-04-25 from https://arxiv.org/pdf/2604.01608 via marker on CPU; figures preserved in `assets/12-skill-distillation-pdf/`)

## Related

- [[topology-taxonomy#long-horizon-context-loss]] — fifth mitigation class: eliminate the handoff.
- [[building-effective-agents]] — argues multi-agent designs are often over-applied; this paper is the empirical complement.
- [[memory-architectures]] — F's framing (behavioural-vs-score topology) is orthogonal to memory mechanisms; both are tools in the architecture decision.
- [[ai-scientist-v2]], [[context-folding]], [[codified-context]], [[cognitive-fabric-nodes]] — the four within-MAS context-preservation mitigations the F-low regime invests in.
- [[openai-symphony]] — production instance of skill distillation in practice: six skills, daily team-level agent loops over team-wide session logs, automatic re-extraction of durable improvements back into skills/docs.
- [[agent-skills]] — Anthropic's "iterate on one hard task, then extract into a Skill" methodology is the practitioner-facing version of the F-metric collapse move.
- [[notion-token-town]] — manager-agent topology and "automate itself out of a job" framing as adjacent F-question (when does collapsing a multi-agent fleet via a manager-agent layer match the F-predictor's collapse decision?).
- [[externalization-survey]] — situates skill-distillation within the survey's skills-as-externalization chapter (§4); its boundary conditions (semantic alignment, portability, staleness, context-dependent degradation) are conceptual cousins to F.
- [[agentic-harness-engineering]] — both use evidence-driven attribution before mutating an architecture (F predictor vs change-manifest verification).
- [[patterns/sdar]] — multi-turn RL instance of distillation-into-weights: skills used at training, internalized, not needed at inference.
