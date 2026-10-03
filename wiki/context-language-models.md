# Context Language Models (CLMs)

arXiv:2609.37725 (Sept 2026; title not captured, "(untitled)" in raw). Context Language Models treat the live context as an editable file that the LM rewrites through general Bash/Python (c_{t+1} = f_θ(c_t) instead of append-only). The claim is that, zero-shot, this beats harness-defined and fixed-action context management (summary, MEM1, ACM-style). It is further improvable by in-context skill evolution, success-gated-efficiency GRPO, and a non-prefix KV-reuse serving patch (Suffix Cache Reuse, SGLang). Headline: Qwen3.6-27B at 32K context reaches 59.4% on BrowseComp-Plus, 11.4% relative above the best baseline, with 21.5% fewer prefix-reuse FLOPs.

## Method

- **Context-as-a-file:** live context is mirrored to a file whose path is in the system prompt. The LM edits it with regex, loops, and helper functions; each edit syncs to the live context for the next turn. No edit means generated tokens are appended. Multi-agent: one context file per agent; subagents are spawned or killed by creating or deleting files.
- **Subsumes fixed-action methods:** the LM defines its own management functions, implicitly or as reusable helpers (e.g. `compact_turns`, called 37 times in one run).
- **Prefix-reuse FLOPs:** cost metric = prefill(unmatched suffix after first prefix mismatch) + decode(generated tokens). Charges mid-context edits for re-prefill.
- **ContextBench:** 4 synthetic tasks (Needle Retention, Sudoku Sketchpad, KV Store, Log Triage), 32K limit, pressure up to 24x.
- **Skill evolution:** skill doc `s` appended to context; GEPA-style loop with train/dev/held-out split, in assisted (stronger proposer) or self-evolution mode.
- **RL:** stepwise GRPO; trajectory outcome advantage broadcast to all segments (same trick as [[memagent]] Multi-Conv DAPO and [[agentflow]] Flow-GRPO). New: success-gated efficiency advantage A_eff = clip((c̄_g − c_i)/c̄_g, −1, 1), successes only, group-mean FLOPs over successes, zero if <2 successes; A = A_out + w_eff·A_eff. Designed to block reward hacking via edit-count or removed-volume rewards.
- **Suffix Cache Reuse (SCR):** after an in-the-middle edit B→B', surviving suffix KV spans are RoPE re-rotated and spliced after B'; only B' is prefilled. Up to K=6 largest spans per edit. Approximate (stale states). For hybrid full/linear-attention models (Qwen3.6-27B, 16 full-attention layers) recurrent state is snapshotted before the edit.

## Results

- **Zero-shot, Qwen3.6-27B, 32K, 100-turn cap:** BrowseComp-Plus 59.4% (21.5% fewer FLOPs than summary, 28.9% fewer than MEM1). TerminalBench 2.1 matches summary accuracy at ~70% FLOPs. TBLite 73.7% vs 67.0% at 91% FLOPs.
- **Math optimization (Claude 4.6 Sonnet, 32K):** beats OpenEvolve and OpenEvolve-Agent on all four problems. Circle packing 2.618 (2.636 with subagents) vs 2.541; Heilbronn 0.03653 vs 0.03127; min-max/min-dist 0.07758 vs 0.07690; Erdős overlap 0.38094 vs 0.38123 (lower is better).
- **EdgeBench-10, 12h:** Qwen3.6-27B CLM 44.6 at 179 PFLOPs vs summary 42.3 at 437 PFLOPs. Claude 4.6 Sonnet CLM 51.0 vs 42.3. Subagents add little.
- **Software World (24h, six-repo swarm, GPT-5.6-Sol, 272K):** 65% greater downstream speedup than summary swarm at equal spend, on 4 unseen packages.
- **Steering:** one prompt sentence shifts compaction timing, boundaries, and backup behavior.
- **Textual evolution:** up to +35.9 points held-out ContextBench accuracy at lower compute (Qwen3.6-27B assisted by Claude Fable 5.1; Opus 5 self-evolution).
- **RL (Qwen3.5-9B, OpenResearcher, held-out BCP):** CLM 28.8 → 42.5%, 1.52 → 1.34 PFLOPs/Q. Summary harness 34.7 → 42.1%, 4.01 → 2.19 PFLOPs/Q. Accuracy edge (0.4 pt) is within noise; FLOPs savings are the real gap (38.8% fewer per intro). Untrained, CLM is ~6 points below summary at 9B.
- **SCR (BCP, Qwen3.6-27B):** matches standard SGLang accuracy at 65.0% of prefix-reuse FLOPs (35% reduction); robust across K in {1..64} on a 64-question sensitivity study.
- **Caveat:** several results use best-of-3 or best-of-run scoring; hard-coded harness baselines were run by the authors.

## Applicability

- Any long-horizon agent: deep research, terminal coding, open-ended discovery (AlphaEvolve/OpenEvolve-style, see [[evolution-fine-tuning]]), multi-agent swarms. Context management becomes a prompt or skill rather than harness code.
- Cheap to try zero-shot: writable context file plus Bash tool. Needs a strong model (untrained 9B underperforms summary). SCR needs a self-hosted stack (SGLang patch); hosted APIs re-prefill after edits.
- The success-gated efficiency advantage is reusable in agentic GRPO pipelines ([[polar-rl-harness]], [[agentflow]]-style) to trade accuracy against inference cost.
- Skill-evolution loop is a direct instance of [[gepa-reflective-prompt-evolution]] / [[skillopt]] applied to context management.
- Safety note from the source: editable context is a persistence channel for prompt injections.

## Novelty/caveats

- Refinement and recombination with a genuinely new framing. Beyond fixed-action methods (Self-Compact, ACM, Sculptor, AutoCompact): unrestricted read-write access to the live context via a general code interface.
- Trending companion, not captured: Recursive Language Models (arXiv 2512.24601). RLM externalizes the input (read-only access); CLM externalizes the live context (read-write).
- New pieces: prefix-reuse FLOPs metric, ContextBench, success-gated efficiency advantage, SCR (extends Memento/PIE-style non-prefix reuse to agent contexts and hybrid linear-attention models).
- Emergent behavior: in-context scoreboards/trackers (163 in-place edits, 6-8K tokens), a new "notes" chat role, reusable compaction functions.
- Soft tension with the harness-as-training-target cluster ([[macaron-v1]], [[memoharness]], [[argus-agentic-runtime]]): CLM moves context control from harness into the model. Future work: distill harnesses into CLMs ("harnesses as procedural memory").
- Brand-new paper; no adoption evidence yet. Evaluation caveats echo [[evolutionary-search-eval-rigor]] (best-of-run, capped budgets in the OpenEvolve comparison).

## Reproducibility

- No repository URL, weights, or released-code statement confirmed in the raw capture. The SCR SGLang patch and ContextBench are described but no release was found.
- Baselines use released harnesses (RLM, ACM) and a Mini-SWE-Agent backbone. Models are largely closed or very new (GPT-5.6-Sol, Claude 4.6 Sonnet, Claude Fable 5.1, Opus 5) plus open Qwen3.6-27B and Qwen3.5-9B. Runs are long (12-24h).
- The tail of the raw capture (Appendix B tail onward) was only grep-scanned during ingest, not read in full.

## Source

- `raw/research/weekly-2026-10-03/03-context-language-models.md` — arXiv:2609.37725.

## Related

- [[memagent]] — RL-trained agent overwriting a fixed 1024-token memory buffer; CLM generalizes to arbitrary context edits.
- [[latentpress]] — soft-token context compression vs CLM text-level self-editing.
- [[neural-garbage-collection]] — RL-trained KV-cache eviction; CLM edits are text-level and need SCR for cache reuse.
- [[triattention]] — KV-cache efficiency sibling (compression vs reuse).
- [[gepa-reflective-prompt-evolution]] — CLM's skill-evolution loop is GEPA on context-management skills.
- [[skillopt]] — text-space skill optimization, here governing context editing.
- [[memoharness]] — external harness optimization vs model-native context control.
- [[memharness]] — RL-learned memory/context reconstruction before acting.
- [[macaron-v1]] — harness co-optimized with weights; prefix-cache-preserving view reconstruction (CLM edits break the prefix, hence SCR).
- [[argus-agentic-runtime]] — role-separated agents with persistent campaign state vs in-context trackers.
- [[polar-rl-harness]] — RL infra; segment-level stepwise GRPO needs similar prefix-merge handling.
- [[agentflow]] — Flow-GRPO also broadcasts outcome reward to every turn.
- [[evolution-fine-tuning]] — OpenEvolve-style math-optimization tasks overlap.
- [[evolutionary-search-eval-rigor]] — critique relevant to the CLM-vs-OpenEvolve comparison.
- [[ssm-tool-use-length-generalization]] — interactive-memory-tool argument; CLM is an editable-context analogue.
- [[delta-mem]] — architectural memory path vs this context-editing path.
- [[terminal-universe]] — shared TerminalBench 2.1 benchmark.
- [[openclaw]] — context window and memory layers; CLM is a model-native alternative.
- [[conflicts/long-context-attention-vs-recurrent-memory]] — adds a context-management third angle.
