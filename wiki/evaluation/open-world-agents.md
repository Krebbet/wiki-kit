# Open-World Agents (OpenAgent)

OpenAgent (ICML 2026, Nanjing University) formalizes the generalization problem for tool-use agents under distributional shift, introducing a four-dimensional taxonomy of open-world perturbations and a controlled sandbox to expose where SFT and RL training paradigms break down. Rather than a new benchmark in the traditional sense, OpenAgent is a diagnostic framework: it defines structured shift tiers, runs agents through them, and identifies two distinct structural failure modes — one per training paradigm. A mitigation strategy (Perturbation-Augmented Fine-Tuning) partially rescues SFT robustness. *(2026-07-05)*

## Problem setting

OpenAgent characterizes open-world generalization failures along four shift dimensions:

- **ΔQ (query shift)** — distributional drift in user instructions relative to training queries.
- **ΔA (action/tool shift)** — changes to tool sets, tool names, or API schemas.
- **ΔO (observation shift)** — changes to interaction dynamics, return formats, or error message structure.
- **ΔD (domain shift)** — tasks that require knowledge or reasoning patterns outside the training domain.

To isolate these shifts from real-world API noise, the authors build a controlled sandbox that injects perturbations systematically. Within the sandbox, shifts are graded across a four-tier diagnostic hierarchy:

| Tier | Label | What changes |
|---|---|---|
| 1 | Perception | Surface-level signals — tool names, identifiers, schema labels |
| 2 | Interaction | Return format and error signaling patterns |
| 3 | Reasoning | Logic and dependency structure of tool invocations |
| 4 | Internalization | Task domain and task solvability (including unsolvable tasks) |

The hierarchy is cumulative: Tier-4 failures presuppose the agent has already navigated Tiers 1–3 correctly.

## SFT vs. RL failure modes

The framework surfaces two structurally distinct failure patterns, one per training paradigm.

**SFT agents — symbolic anchoring.** SFT-trained agents overfit to surface-level symbolic features of tools encountered during training. When tool names or schema labels are perturbed (Tier-1 Semantic Trap + Identity Erasure), performance collapses sharply. Reported accuracy delta reaches −67.7% and Tool Error Rate rises sharply under these conditions (collect-but-confirm: author-run evaluation on Qwen2.5-7B-Instruct). The agents recognize the task but fail to map it onto the perturbed tool vocabulary — the learned association is between the symbol, not the function.

**RL agents — boundary blindness.** RL-trained agents are more robust to surface perturbations but suffer from a different structural weakness. Because teleological reward signals push agents toward task completion, RL agents lose the ability to recognize and refuse genuinely unsolvable tasks. Reported refusal rate on unsolvable tasks approaches 0%, meaning RL agents force completion even when no valid solution exists. They detect errors but repress the refusal response in service of the completion objective.

**Shared catastrophic failure — Logic Inversion.** When the causal dependency order between tool calls is reversed and documented as such in the new schema, both SFT and RL agents fail catastrophically. Neither paradigm generalizes to structural inversions of tool logic, even when the documentation explicitly describes the new order. This failure is not paradigm-specific; it points to limits in how relational tool knowledge is encoded under either training regime.

## PAFT mitigation

Perturbation-Augmented Fine-Tuning (PAFT) is a disturbance-based intervention for SFT. During fine-tuning, training examples are augmented with perturbations drawn from the same shift taxonomy (ΔQ, ΔA, ΔO, ΔD), exposing the model to open-world variations at training time rather than only at inference time.

Key empirical findings from the paper (collect-but-confirm: author-run on Qwen2.5-7B-Instruct, 6,050 training / 880 evaluation samples):

- At **α=0.3** (perturbation mixing ratio), PAFT recovers early-stage SFT from severe degradation and drives Tier-4 refusal rate on unsolvable tasks from ~0% to **97.8–99.6%** — a near-complete recovery on the boundary-recognition dimension.
- Beyond α=0.3, gains saturate. α=0.4 shows flat or slight regression, suggesting a diminishing-returns ceiling for perturbation density under this setup.
- PAFT addresses SFT's symbolic anchoring failure. It does not directly address RL's boundary blindness, which stems from the reward formulation rather than the training data distribution.

Code is released at [github.com/LAMDA-NeSy/OpenAgent](https://github.com/LAMDA-NeSy/OpenAgent).

## Source

- `raw/research/weekly-2026-07-05/04-05-open-world-agents.md` — captured 2026-07-05 from arXiv 2607.01084 (pymupdf; text complete, images missing)
- arXiv 2607.01084, ICML 2026 (Proceedings of the 43rd International Conference on Machine Learning, Seoul)
- Authors: Song-Lin Lv, Weiming Wu, Rui Zhu, Zi-Jian Cheng, Lan-Zhe Guo — School of Intelligence Science and Technology / LAMDA, Nanjing University

## Related

- [[patterns/sdar]] — SDAR cites open-world shift as motivation; OpenAgent directly quantifies the degradation SDAR aims to avoid.
- [[evaluation/agents-last-exam]] — ALE identifies domain-knowledge failure as the dominant capability gap; OpenAgent probes the ΔD (cross-domain) dimension directly and finds both paradigms fall short.
- [[evaluation/swe-bench-pro]] — both surfaces the same thesis: static-benchmark mastery does not transfer to deployment-time distributional shifts.
- [[conflicts/swe-bench-contamination]] — OpenAgent's controlled sandbox cleanly separates benchmark leakage from genuine robustness, addressing the confound that makes contamination hard to disentangle in live benchmarks.
- [[patterns/skillos]] — SkillOS skill-level abstraction addresses symbolic-anchoring failure from the architecture side; OpenAgent diagnoses it empirically and PAFT addresses it from the training side.
