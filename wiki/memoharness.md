# MemoHarness: Agent Harnesses That Learn from Experience

Notre Dame / LMU Munich / USC preprint (arXiv:2607.14159) introducing MemoHarness, an agent-harness optimization framework that decomposes the harness into six editable control dimensions, searches for a global harness via correctness-first structured editing over a dual-layer experience bank, and then specializes that harness per test case at inference time with no test-time labels, feedback, or extra search — reaching 0.806 on Terminal-Bench (vs 0.722 for the strongest scaffold baseline) while costing less than Codex or Claude Code despite heavier raw token use, thanks to aggressive prompt caching.

## Method

Treats the agent harness — the external control layer wrapping a frozen base LLM — as a product space **W = W(1)×...×W(6)** over six dimensions: context assembly (D1), tool/retrieval interaction (D2), generation/decoding control (D3), orchestration topology (D4), memory management (D5), output processing (D6). This turns harness search into bounded structured editing over separable, interpretable dimensions rather than opaque end-to-end prompt or workflow search.

A **dual-layer experience bank B = (E, G)** anchors the search:
- **E (per-case entries)** — trajectory, reward, cost, and the output of a diagnostic operator: success flag, primary/secondary failure dimension, natural-language failure analysis.
- **G (global patterns)** — distilled every N iterations (or after 3 consecutive failures on the same case) from clustered failure entries in E.

Training-time search starts from a minimal harness **W0** (no demos, no tools, deterministic single-call decoding, no memory, raw output passthrough) and iterates: query the bank → retrieve a bounded evidence slice → controller **Π_train** proposes the next W_t → execute on all labeled search cases → log trajectories and diagnoses → periodically distill G. Final global harness **W\*** is chosen by **lexicographic selection** (Eq. 16): maximize mean task reward first, use mean token cost only as a tiebreaker — explicitly correctness-first, not cost-first, unlike some pipeline optimizers that fold cost into the primary objective.

At test time, with no labels available, a separate controller **Π_test** adapts W* into a case-specific harness **W(x)**: retrieves top-K similar historical entries (cosine similarity over an instruction embedding ψ, spanning both successes and failures) plus feature-conditioned bank slices and global patterns G_T, then emits W(x) in a **single adaptation pass** — no iterative feedback, no re-search, no gradients or RL anywhere in the pipeline. This is the mechanism's centerpiece: a bounded structured-edit-and-validate optimizer at training time, paired with retrieval-only specialization at test time.

Positioned explicitly against: DSPy/MIPRO/TextGrad (pipeline and instruction optimization), AFlow/AutoFlow (workflow search), Promptbreeder/OPRO/ProTeGi (prompt evolution), Reflexion/Self-Refine (in-context reflection), and — as closest prior work — **Meta-Harness** (Lee et al. 2026), which also searches harness code but stops at a single reusable training-time artifact with no test-time per-case adaptation. No empirical comparison to Meta-Harness was possible (no usable public implementation at paper finalization).

## Results

**Terminal-Bench** (18-task held-out split, GPT-5.3-Codex): MemoHarness 0.806 vs strongest baseline (Codex) 0.722 (+0.084); vs Claude Code / OpenCode / Terminus, +0.250 to +0.445.

**Base → final** across three benchmarks: Terminal-Bench 0.722→0.806, LiveCodeBench 0.900→0.967, FinanceAgent 0.600→0.767. FinanceAgent keeps climbing over 10 search rounds (42.5%→65.0% peak at iterations 8–9); LiveCodeBench saturates almost immediately (91.2–95.0% band) — near-saturated single-shot code tasks show little room for harness search to help.

**Cross-dataset transfer** to 6 unseen suites (GPT-5.3-Codex): a Terminal-Bench-sourced harness gives the broadest lift (MMMLU +0.030, StrongReject +0.030, SWE-Bench Pro +0.059); already-saturated suites (HumanEvalFix, Reasoning-Gym-Easy) show no movement — transfer is selective, tracking headroom, not universal.

**Cross-model transfer**: a harness searched only on GPT-5.3-Codex, applied unmodified to 6 other models across 4 families, improves every one — mean +0.098, range +0.038 (GPT-4.1) to +0.233 (GLM-5).

**Cost**: MemoHarness uses more raw input tokens (14.18M) than Codex/Claude Code/Terminus/OpenCode, but 13.32M of that is cached, giving total run cost $6.89 — cheaper than Codex ($10.28) and Claude Code ($9.51) at higher task success (Terminus/OpenCode are cheaper still but far less accurate).

**Operation-level lift** (appendix analysis): newly-added tools like `cat`, `sed`, `which`, `test` correlate with reward increases (+17 to +60pp lift over a ~13.2% baseline); `curl`/`echo`/`file`/`jq` correlate negatively — a concrete signal that harness search is discovering specific, checkable tool-usage patterns rather than just adding capability indiscriminately.

## Novelty vs SkillOpt

MemoHarness generalizes the same core idea [[skillopt]] established for a single artifact: **bounded structured edit, accepted only via a validation gate, no gradients, no RL**. SkillOpt optimizes one skill document under a strict monotone-improvement acceptance rule with zero deployment overhead; MemoHarness optimizes all six harness control surfaces jointly (context, tools, decoding, orchestration, memory, output) and, unlike SkillOpt, adds a typed dual-layer experience bank (diagnostic per-case entries + distilled global patterns, not just scalar validation scores) and a genuinely new capability SkillOpt lacks: **test-time per-case specialization** from the bank with zero test-time feedback, gradients, or re-search. The two form a natural cluster — "bounded structured-edit + validation-gate optimization" as a family distinct from RL/gradient-based harness or skill tuning (contrast [[polar-rl-harness]], which is RL/GRPO through a harness-agnostic proxy) and distinct from evolutionary/reflective prompt search (contrast [[gepa-reflective-prompt-evolution]], which is Pareto-genetic prompt evolution rather than lexicographic correctness-first harness selection).

## Reproducibility

Code released: https://github.com/HowieHwong/MemoHarness. Preprint, under review — no peer-reviewed venue yet, no independent reproduction reported as of this ingest. No released model weights (method is harness-only; operates over existing proprietary/open base LLMs). Authors flag real limits: point estimates only, no confidence intervals or significance tests on the 18-task held-out split; not every baseline is a pure scaffold-only transplant; bank/global-pattern/test-time-adaptation components are not separately ablated in all settings; the controller and diagnostic operators are heuristic, not learned.

## Source

`raw/research/weekly-2026-08-01/03-memharness.md`

## Related

- [[skillopt]] — closest prior-quarter parallel: same bounded structured-edit + validation-gate, non-gradient optimization philosophy, applied to a single skill document rather than the full 6-dimension harness; MemoHarness adds the dual-layer bank and test-time per-case adaptation SkillOpt lacks.
- [[gepa-reflective-prompt-evolution]] — same "no weight updates, search a control artifact via reflection/diagnosis rather than pure scalar reward" family, but genetic-Pareto candidate selection over prompts vs MemoHarness's lexicographic correctness-first harness selection.
- [[polar-rl-harness]] — both are "harness" papers with opposite mechanisms: Polar is an RL (GRPO) rollout framework operating through a harness-agnostic proxy; MemoHarness explicitly avoids RL/gradients entirely.
- [[openclaw]] — parallel dual/multi-layer memory design: MemoHarness's per-case + distilled-global experience bank vs OpenClaw's four-layer memory + retrieval index; both must bound retrieved context as the store grows.
- [[openclaw-claude-code-memory]] — practical instantiation of the same bank-retrieval-for-agent-context problem in a production coding-agent setting.
