# Recursive Collective Intelligence (equal-budget ladder)

Stanford / Berkeley / NVIDIA / Northwestern (arXiv:2611.32606). Grades LLM agent groups against independent agents given the same completion-token budget (single, majority vote, pass@n). Under shared information, the tested debate/orchestration systems do not beat the matched vote; with split facts, fact-exchange protocols beat pass@n, and label-free SFT on protocol-verified outputs improves groups over successive generations.

## Method
- Budget n_B = group completion tokens / mean tokens of one agent. Levels: beats single (L1), vote (L2), pass@n (L3). pass@n upper-bounds any selector over independent answers. Prompt (reading) tokens are not counted.
- Generations: full-parameter SFT on first turns passing a hand-designed protocol check or on auto-verified outputs; releases gated on a confirmation slice.
- Shapley-share credit over claims for group RL.

## Results
- Shared information: Qwen3.5-9B debate/DeLM/AOrchestra never beat the matched vote. A 27B reviewer over a blackboard does (+0.037 to +0.131, 4 benchmarks).
- HiddenBench, 4x Qwen3.8-27B: blackboard 0.369 (L2) vs shared context + fact forwarding 0.972 (L3). One fully informed agent budget scores 0.942, so pooling gains over full information are small.
- SplitBench held-out, margin over base pass@n, G0 -> G2: 9B -0.253 -> +0.159 (control -0.033); 27B -0.009 -> +0.284 (control +0.016). Over four further seeds, 9B G2 minus control is +0.115 +/- 0.008, below the first seed's +0.192.
- PlanBench group accuracy 0.613 -> 0.950 over G0-G4 (selection set; confounded with less truncation).

## Caveats
- Several recursion curves are reported on selection sets; release-gate gains are conditioned on passing. One gate (Hanabi, d - SE > 0) is lenient. Read against [[resolution-hypothesis]].
- PlanBench, Hanabi and the 5-release HiddenBench run have no training-seed replication; the only HiddenBench run with matched self-training released 3 generations.
- HiddenBench reference answers are base-model consensus, not ground truth.
- Split-information pass@n references see only one member's facts each.
- Source reports "Qwen3.8-27B"; preserved verbatim. Code URL (github.com/lixuan27/RCI-official) not verified.

## Source
- `raw/research/weekly-2026-11-28/05-recursive-collective-intelligence.md`
- https://arxiv.org/abs/2611.32606

## Related
- [[resolution-hypothesis]] - noise-limited selection in agent evolution.
- [[self-evolving-agent-harness]] - held-out reuse and admission gates.
- [[evolutionary-search-eval-rigor]] - budget-matched comparison discipline.
- [[test-time-scaling-taxonomy]] - pass@k and selector limits.
- [[co-cheating-crossfit]] - agreement-based verification can reward shared errors.
- [[u-opsd-unsupervised-self-distillation]] - consensus as label-free signal.
- [[skill-self-play]]
