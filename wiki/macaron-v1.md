# Macaron-V1: Mixture of LoRA and Model–Harness Co-design for Experiential Intelligence

Mind Lab report (arXiv:2608.09819) introducing Macaron-V1, an open agent-model family built on **Mixture of LoRA (MoL)** — a frozen 744B GLM-5.2 base (Venti variant; Qwen3.6-35B-A3B for the smaller Tall variant) carrying four specialist LoRA adapters (Chat/router, Agent, Coding, GenUI) composed per-turn by the entry adapter's own routing decision, no separate router model — plus **MindForge**, a recursive self-improvement loop that treats the serving harness (tools, prompts, skills, hooks — versioned as HCP, Harness Context Protocol) as a co-optimized training target alongside adapter weights.

## Method

**MoL architecture:** base stays frozen; four adapters at rank 16/alpha 32 (Venti) or rank 64/alpha 128 (Tall) sit on top. A stateless "MoL Proxy" runs a three-stage per-turn lifecycle — Route → Answer → Summary. L0 classifies each incoming turn into one of four canonical labels under a 24-token constrained-decoding budget; L0 *is* the router (no separate classifier, no keyword rules). The answering specialist emits a 192-token summary that other adapters see on future turns instead of the full cross-adapter trace, giving each adapter a deterministic "own-view" reconstruction of the conversation. Own-views are byte-identical on adapter re-entry, which means the engine's native LoRA-aware prefix cache gets automatic reuse with zero engine modification — the paper's central systems trick, and closest in spirit to prior mixture-of-adapter serving work (Punica, S-LoRA) that this paper explicitly frames as productionizing rather than superseding.

**MindForge (harness co-design + RSI):** HCP — a versioned TOML artifact for tools, prompts, skills, hooks, session state — is optimized jointly with adapter weights via a three-stage loop: Discovery (model proposes harder task variants), Expansion (execute under fixed model+HCP, audit failures, search HCP-level config edits in language space), Update (selected trajectories train LoRA adapters via GRPO; accepted HCP versioned as next-gen config). This separates configuration search from parameter updates, structurally similar to [[gepa-reflective-prompt-evolution]]'s no-weight-update reflective search but positioned as one stage inside a larger weight-updating RSI loop. Supporting infrastructure: **UI4A** (agent writes real frontend code under runtime-enforced Action-contract boundaries rather than a fixed schema); a **REPL-based agent harness** (persistent Python namespace avoiding one-round-trip-per-dependency of discrete function calling, gating self-derived helper tools behind private validation before promotion — reusable independent of the LoRA angle); **MinT** (adapter-revision lifecycle manager distinguishing immutable "adapter revision" from mutable "policy record," addressable catalog at 10^6-entry scale); **LongStraw** (captures prompt state without autograd, replays each GRPO group member's response serially under autograd, bounding live memory by the longest single response rather than the full group — a rollout-memory trick for long-context RL); and rollout–train mismatch controls for sparse MoE/DSA bases.

## Results

Routing: 99.12% accuracy (Venti), 99.04% (Tall), 100% canonical-label compliance, zero parse errors. Routing+summary overhead ≈32% of per-turn latency (0.54s route + 0.97s summary vs 3.17s answer, Venti). Three-arm check finds no detected quality degradation from KV-cache reuse: routed-with-reuse 0.632±0.019 vs direct single-adapter 0.636±0.026 vs routed-no-reuse 0.650±0.030 — small unpaired samples, not an equivalence proof. Weight residency: MoL holds ~774.8B logical params (744B base + 30.8B adapters) vs 2.976T for four replicated merged-base copies, a 74% reduction — the same "small delta over frozen base" economy seen in [[reasonmaxxer]], via a different mechanism (routed LoRA vs whatever ReasonMaxxer's parametric footprint carries).

Benchmarked against Opus 4.8/GPT-5.5/Gemini 3.1 Pro/GLM-5.2/Qwen 3.7 Max/Minimax M3: Macaron-V1-Venti leads Macaron ChatBench (58.3), Macaron LivingBench (64.0, +0.2 over Opus 4.8), UI4A-Bench (87.8 vs Opus 4.8's 75.9), TerminalBench 2.1 (87.6); trails on VitaBench, ClawGym, SWE-Verified (85.6 vs Opus 4.8's 88.6), DeepSWE, SWE Atlas QnA. Paper explicitly declines an aggregate cross-benchmark ranking claim. Macaron-V1-Tall (50B) beats its own Qwen3.6-35B-A3B base on all 7 matched rows (+1.3 to +25.4 pts).

Harness-search ablation (RSI Expansion stage only, no weight update): on 122 simulation tasks the frozen GLM-5.2 base fails outright; adaptive HCP/skill config search reaches 122/122 cumulative coverage over 69 jobs (450 attempts), vs best single full-set config sweep at 11/122 (9.0%). This measures configuration-search coverage, not RSI training-loop capability improvement — a distinction the paper is careful about.

Infra: MinT adapter-only handoff is 18.3× faster than full-checkpoint merge-and-load for Qwen3-4B (rank-32), 2.85× for Qwen3-30B (rank-16).

## Applicability

Fits production multi-capability agent products wanting to (a) avoid cross-task interference from joint post-training by keeping task families in separate LoRA adapters over one frozen base, (b) close the loop between harness/tool/prompt iteration and adapter fine-tuning. Prerequisites are steep: a resident 100B+ base, GRPO RL infrastructure, an evaluator/judge stack for trajectory selection, and a versioned/searchable production harness. Two pieces are reusable well below that bar: the MoL serving pattern (own-view reconstruction + native prefix-cache reuse, no engine modification) for anyone doing multi-adapter serving on vLLM/SGLang; and the REPL-based agent harness for any agentic coding/tool-use system, independent of the LoRA angle entirely.

## Novelty

Mixed. The MoL architecture (frozen base + routed specialist LoRAs, no merging) is a refinement/productionization of known mixture-of-adapter serving (Punica, S-LoRA), which the paper itself frames as an "operating point" rather than a new mechanism. Genuinely novel: using the entry adapter's own reasoning as the router — no separate router model — combined with deterministic own-view reconstruction making per-adapter KV-cache reuse emergent on unmodified serving engines. The harness-as-training-target framing (HCP + MindForge RSI) sits in a crowded, very recent cluster of concurrent work the paper itself cites (Continual Harness, Recursive harness self-improvement, Meta-Harness) — convergent thinking across labs in mid-2026, not an isolated idea. This paper anchors a growing **harness-as-training-target cluster** alongside [[skillopt]], [[memoharness]], and [[argus-agentic-runtime]] that may warrant its own overview/cluster page once more sources land. Authors are notably candid that several headline numbers (122/122 coverage, KV-reuse quality parity) are diagnostics/systems checks, not causal or generalization claims.

## Reproducibility

Code released: github.com/MindLab-Research/Mixture-of-LoRA-Harness. Weights released: huggingface.co/mindlab-research/Macaron-V1-Venti; Macaron-V1-Tall (Qwen3.6-35B-A3B based) also released for local deployment. Companion systems reports (MinT, LongStraw, R3, DSA alignment) are cited rather than fully reproduced in this paper — several infra numbers are imported from those separate studies. Internal benchmarks (Macaron ChatBench/LivingBench/UI4A-Bench) are proprietary/curated with no public release, limiting independent verification of headline numbers.

## Adoption

No external adoption signal yet — this is the introducing paper, captured at release.

## Source

`raw/research/weekly-2026-08-22/07-macaron-v1-mixture-of-lora.md`

## Related

- [[memoharness]] — parallel harness-optimization approach: MemoHarness does correctness-first structured editing of a fixed harness with no gradients; Macaron's MindForge/HCP couples the same kind of harness search to LoRA weight updates.
- [[skillopt]] — Macaron's Expansion-stage language-space search over prompts/skills/tool policy, validated by re-run, is conceptually the same move as SkillOpt's bounded skill-document edits gated by validation, generalized to the full HCP surface and coupled to adapter training.
- [[argus-agentic-runtime]] — both gate self-evolution/configuration change behind an evidence-based acceptance contract; both are fixed-model/harness-search stories with an RSI angle.
- [[reasonmaxxer]] — both find a large capability delta rides on a small parametric footprint (rank-32/16/64 LoRA carrying all differentiated capability) — different mechanisms, same "small delta over frozen base is enough" theme.
- [[huxley-godel-machine]] — another bounded/auditable self-improvement loop; both frame themselves as approximations of unbounded recursive self-improvement.
- [[gepa-reflective-prompt-evolution]] — GEPA is a no-weight-update reflective prompt/config optimizer; Macaron's Expansion-stage HCP search is the same "language-space search before touching weights" idea, positioned as one stage of a larger RSI loop.
