# MemHarness: Memory Is Reconstructed, Not Replayed

Shanghai AI Lab / Zhejiang U (arXiv:2607.28272, Jul 2026). An RL-trained unified policy that critiques and rewrites retrieved episodic memories into state-specific guidance before acting, replacing verbatim memory replay in LLM agents, trained end-to-end via GRPO with no supervision on the reconstruction step.

> **Naming note:** distinct from [[memoharness]] (arXiv:2607.14159, Notre Dame/LMU/USC) — a different, unrelated system for structured harness-editing without RL. Same near-identical name, different authors, different mechanism.

## Method

Reframes memory-guided decision-making as a 5-stage process (observe → retrieve → critique → reconstruct → act), inspired by Loftus & Palmer's (1974) reconstructive-memory finding. A single shared policy πθ decides whether to query a vector memory bank (top-k=3), then — the core novelty vs prior work, which drops retrieved text straight into the action context — compares a retrieved experience against its source observation and the current state to emit either adapted guidance or an `<EMPTY>` fallback signal, before conditioning the same policy on that guidance to emit the action. Because the reconstruction step has no ground-truth target, the whole retrieve→reconstruct→act chain is optimized end-to-end with GRPO using only a sparse task-outcome reward plus a small format bonus. The memory bank is populated online during RL from the policy's own trajectory distillations, with EvolveR-style utility pruning and dedup. Backbone: Qwen2.5-7B-Instruct on the verl-agent/veRL framework.

## Results

ALFWorld avg SR / WebShop SR: MemHarness 85.2% / 75.6% — best of all methods tested, including closed-source Gemini-2.5-Pro (62.1% / 35.9%) despite 7B scale. Beats plain GRPO (76.4%/66.1%) and a reproduced EvolveR baseline (70.1%/72.6%). Critically, naive memory+RL baselines *underperform* plain GRPO (Mem0+GRPO 52.0%/37.5%, MemRL 24.0%/9.2%) — verbatim memory injection actively hurts. OOD (unseen ALFWorld layouts): 85.9% vs 76.3% for "RL + Raw Memory." Ablations: removing reconstruction (raw replay) drops ALFWorld to 70.1%, *below* plain RL-only, confirming replay introduces noise; disabling memory at test time while keeping the RL-trained policy still hits 83.0% (vs 76.4% RL-only), showing the reconstruction objective intrinsically improves base reasoning even without memory available; swapping in a generic instruction-tuned LLM (zero-shot) for the reconstruction step drops ALFWorld to 77.7% — end-to-end RL reconstruction, not just any rewriting, is required.

## Applicability

Fits agentic-RL projects with an interactive environment providing a task-success signal (ALFWorld/WebShop-style POMDPs), an existing or buildable episodic memory bank, and RL infrastructure (GRPO/verl-agent or equivalent). Requires a 7B-class base model, a GRPO training loop with group rollouts, a small cold-start SFT stage, and full RL training compute — not a cheap fine-tune. Not applicable to non-interactive/single-turn tasks or settings without a dense-enough reward signal for GRPO.

## Reproducibility

GitHub repo released: `github.com/KnowledgeXLab/MemHarness`, built on public infrastructure (verl-agent/veRL, vLLM, Milvus, BGE-M3) and public benchmarks. No released model weights mentioned.

## Conflicts

No direct contradiction of a resolved wiki claim. Sits in tension with [[delta-mem]]'s "memory-skeptical" framing (frozen backbone + low-rank state edits beats retrieval-augmented memory): MemHarness's own ablations *corroborate* the failure mode motivating memory skepticism (naive memory+GRPO underperforms plain GRPO) but argues the fix is a better reconstruction mechanism rather than abandoning explicit retrieval — nuances rather than contradicts.

## Related

- [[memagent]] — both RL-trained agent-memory systems (GRPO-family) where memory-handling emerges from end-to-end task reward; memagent targets long-context QA via a fixed-size overwritten buffer, MemHarness targets interactive decision-making via an explicit episodic memory bank.
- [[delta-mem]] — see Conflicts above.
- [[seal-self-adapting]] — parallel: both use an RL outer loop to train an adaptation mechanism itself (self-edit generation vs memory critique/reconstruction) rather than treating adaptation as a fixed heuristic.
- [[memoharness]] — naming collision only, see note above.

## Source

- `raw/research/weekly-2026-08-08/05-memharness-memory-reconstruction.md` (arXiv:2607.28272)
