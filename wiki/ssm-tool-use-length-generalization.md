# SSMs with Interactive Tool-Use Achieve Length Generalization

Apple ML (arXiv:2510.14826, ICLR 2026 Oral). Formal proof, plus matching experiments, that fixed-memory recurrent architectures (Mamba-1/2, LSTM, GRU, Linear Transformer, RetNet, H3, local-attention Transformers — the paper's "GSSM" family) **cannot** solve long-form generation tasks under CoT-only or single-turn tool-use, but **can** achieve perfect length generalization on any computationally tractable such task when given **interactive (multi-turn)** access to a pointer-based memory tool. Constructive: the proof is by encoding a Turing-machine tape as tool calls, and the experiments deliver — Mamba-1.4B trained on ≤5-digit addition extrapolates to **1,000-digit addition at 100%**.

## Method

A "Generalized State Space Model" (GSSM) is any architecture that maintains a fixed-size hidden state across timesteps. The paper covers Mamba-1/2, LSTM, GRU, Linear Transformer, RetNet, H3, and (sliding-window) local-attention Transformers under one definition. This is the paper's most useful framing decision for the wiki: it dissolves the colloquial "SSM vs RNN" split — classical gated RNNs (LSTM/GRU) and selective SSMs (Mamba) sit in the same equivalence class for the purpose of Theorem 2.1, and architecture-level differences ([[mamba-3]]'s continuous-time discretization, complex-state rotation, MIMO update) are orthogonal to the fundamental fixed-memory bound.

A "long-form generation task" is one where the effective output support grows unboundedly with problem complexity (multi-digit arithmetic, Boolean DAG evaluation, Tower of Hanoi, code refactoring across many functions).

**Theorem 2.1 (negative).** For any GSSM, in CoT-only or single-turn-tool-use settings, error ≥ 1 − α for sufficiently large problem size n. Intuition: fixed memory cannot distinguish enough states to track an unboundedly growing computation. Proof in Appendix B.

**Theorem 2.2 (positive, constructive).** There exists a memory-tool oracle (pointer-based read/write + left/right moves — a Turing-machine tape interface) and a training-data construction such that a simple GSSM learning algorithm (standard NTP with teacher forcing, masking observations) achieves length generalization on any computationally tractable task. Proof: encode the Turing-machine transition table as tool-call trajectories; show that for n₀ large enough, all (state, symbol) transition pairs appear in the training set, after which the GSSM has learned the simulator.

Tools used in experiments: pointer memory `find(x)`, bash, scratchpad. Models trained from scratch on synthetic trajectories (arithmetic, logical-graph, Hanoi) or finetuned on SWE-agent-LM-32B distillation traces (coding).

## Results

**Arithmetic (Table 1, Figure 2):**
- **Mamba-1.4B trained on ≤5-digit addition → 100% on 1,000-digit addition** (log-scale extrapolation).
- Mamba on n×1 multiplication: 10 digits → 1,000 digits at 100%. n×2 same.
- LSTM matches Mamba on addition / multiplication, degrades faster on harder tasks.
- Pythia-1.4B (Transformer): 10 → 20 digits (79%) on addition; doesn't generalize.
- Mistral (sliding-window): 10 → 13 digits (25%).

**Algorithmic / reasoning:**
- Logical Graph (Boolean DAG): Mamba 10 → 1,000 nodes (98%); LSTM 100% at 1K; Pythia collapses to 5%.
- Tower of Hanoi: Mamba 8 → 12 disks (49%); all baselines stall at 8 (0% beyond). Output length grows exponentially in disk count, which is the bottleneck even for Mamba.

**Coding (Figure 1):** Mamba-1.4B and Pythia-1.4B finetuned on ~100K SWE-agent trajectories. Interactive setting: Mamba *maintains* accuracy beyond training distribution (larger codebases) where Pythia degrades. Single-turn setting: both fail — confirms Theorem 2.1 empirically. Distillation: Pythia starts higher on small codebases, Mamba overtakes for larger ones.

## Why this matters

The conflict thread on fixed-state SSMs at long context ([[conflicts/fixed-state-ssm-long-context]]) had been operating on assertion: Titans / Hope claim fixed states can't capture rich long-sequence info; Mamba-3 partially conceded retrieval weakness and shifted to hybrids. This paper provides the missing **formal proof** of Position A (Theorem 2.1) — and crucially, it also opens a **third escape hatch** that neither side had on file:

- Position A response (Titans / Hope / Nested Learning): make the state learnable / multi-scale.
- Position B partial (Mamba-3): pair pure SSM with attention layers.
- **New Position B (this paper): leave the SSM alone, give it a Turing-tape tool.**

The empirical claim — Mamba-1.4B doing 1000-digit addition after training on ≤5 digits — is the strongest length-generalization result for any architecture this year. It also reframes [[in-place-ttt]]'s thesis: In-Place TTT extends SSM expressivity via fast-weight TTT; this paper argues interactive tool-use is the more tractable path to unbounded generalization. The paper doesn't claim attention is wrong; it claims that *whatever* fixed-memory substrate you choose, interactive tool-use is the lever that makes length generalization fall out for free.

The lever is also implementable today: no architecture changes, no RL, no fast-weights — pure NTP supervised imitation of tool-use trajectories. This is closer to [[huxley-godel-machine]]'s scaffold-evolution philosophy than to the Mamba-3 / Hope architecture-side line. The two paradigms are now both empirically live for the same problem.

## Reproducibility

- No public code repository.
- Pointer-tool protocol fully specified (Appendix D.1, D.3).
- Trajectories generated from SWE-agent-LM-32B via mini-SWE-agent (https://github.com/SWE-agent/mini-swe-agent).
- 1.4B-scale; supervised NTP only; no RL, no labeled rewards. Reproducible with engineering effort, not GPU budget.

## Source

- `raw/research/weekly-2026-05-04/05-ssm-tool-use-length-generalization.md` — arXiv:2510.14826 (ICLR 2026 Oral, Apple ML).

## Related

- [[mamba-3]] — analyzes SSM expressivity from the architecture side; this paper proves the fundamental bound Mamba-3 tries to push against, and offers tool-use as an alternative lever.
- [[in-place-ttt]] — parallel/contrast: In-Place TTT extends SSM expressivity via fast-weight TTT; this paper argues tool-use is the more tractable escape.
- [[test-time-training]] — adjacent; both fast-weight TTT and tool-augmented SSMs aim to overcome fixed-memory limits.
- [[nested-learning]] — MIRAS taxonomy frames SSMs as associative-memory; this paper frames them as Turing simulators when given a tape.
- [[huxley-godel-machine]] — adjacent: scaffold-side route to capability gains.
- [[conflicts/fixed-state-ssm-long-context]] — extended this run with the formal proof of Position A and a new tool-use Position B variant.
- [[watchlist]] — RetNet, H3, Linear Transformer, mini-SWE-agent, SWE-agent-LM-32B referenced.
