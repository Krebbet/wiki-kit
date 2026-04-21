# CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing

CRITIC is a prompt-based framework enabling frozen LLMs to verify and iteratively self-correct by interacting with external tools (search, interpreter, API). On QA tasks, CRITIC achieves 62.0% F1 on AmbigNQ vs 51.4% for ReAct; on math synthesis, 78.2% accuracy (GSM8K) vs 72.5% for PoT with ChatGPT (2305.11738). Key finding: **external tool feedback is critical**—self-correction without tools degrades performance, revealing LLMs' inability to verify their own correctness.

## Method

**Verify → Correct → Verify loop** (Algorithm 1): Initialize output ŷ₀ via CoT/PoT. Verify step: generate critique c^i via tool interaction on input, output, and task context. Stop if critique confirms correctness; else correction step: regenerate ŷ^(i+1) conditioned on input, prior output, and critique. Iterate up to n rounds or convergence.

**Tool interaction** (§3.2): Construct tools as text-to-text functions (search engine → parsed snippets, code interpreter → execution results, Perspective API → toxicity scores). Interleave in few-shot demonstrations. LLM generates queries; tools return structured feedback concatenated into narrative critique.

**In-context learning** (§3.1): Chain-of-thought reasoning + few-shot demos. No training; frozen LLM.

**Verification**: Unlike prior work (Self-Refine, Reflexion) using oracle environment signals, CRITIC uses tools for verification: "What's the problem with the above answer?" applied to feedback from tool interaction, not internal LLM confidence.

## Claims

**QA (free-form)**: **7.7 F1 gain on ChatGPT** (62.0 vs 54.2 vanilla, AmbigNQ/TriviaQA/HotpotQA avg) (Table 1). **Tool indispensable**: removing tool ("CRITIC w/o Tool") drops 8 F1 points; LLM-only critique contributes <1 F1.

**Math program synthesis**: **5.7% accuracy gain on GSM8K** (78.2% vs 72.5% PoT, ChatGPT) (Table 2). **Intrinsic errors hardest**: unreasonable outputs corrected 57.4% of the time; intrinsic logic errors only 26.7% (Table 7).

**Toxicity reduction**: **79.2% reduction in max toxicity** on REAL ToxicityPrompts vs RL baselines (Quark, Self-Correct) (Table 3). Fluency and diversity preserved.

**Iterative refinement effect**: Marginal gains diminish; 2–3 rounds typically optimal. Improvements over rejection sampling: 4.5–3.3 EM higher via critiques vs best-of-N (§4.4).

**Failure of self-correction**: **Self-evaluation AUROC ~0.73 vs CRITIC ~0.81** on hallucination detection (Table 5); LLMs cannot reliably assess their own correctness without external grounding.

## Relevance to the project

CRITIC introduces tool-augmented critique as a training-free mechanism for LLM self-correction—orthogonal to fine-tuning approaches. For single-sample concept-based fine-tuning, CRITIC offers a runtime primitive: given a single response, tools provide verifiable feedback loops that improve outputs without requiring RL or parametric updates.

**Key primitive**: Decoupling critique generation (from tools) from correction generation (from LLM). This enables weaker models to leverage stronger external signals for grounded self-improvement. Useful for incorporating domain knowledge (e.g., code interpreters) into fine-tuning pipelines.

**Limitations**: Requires task-specific tool design; inference cost scales linearly with iterations; prompt engineering burden non-trivial (Appendix F); does not enhance model capability—only surface-level error correction (doesn't teach new reasoning).

## Source

- arXiv: 2305.11738
- Raw markdown: `../../../raw/research/adjacent-reward-signals/07-critic-tool-interactive.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/critic-tool-interactive.pdf`

## Related

- [[self-refine]] — Both use iterative refinement; Self-Refine relies on LLM's internal feedback, CRITIC on external tools.
- [[reflexion]] — Reflexion uses environment rewards over trajectories; CRITIC uses tool-derived signals per-sample.
- [[constitutional-ai]] — CAI uses learned judge; CRITIC uses freely-available tools (search, interpreter).
- [[../process-reward-models/lets-verify-step-by-step]] — CRITIC verifies code/facts via tools; process reward models train dense step-level classifiers.
- [[../self-improvement/_overview]] — CRITIC is inference-time self-correction; complements training-time self-improvement schemes.
