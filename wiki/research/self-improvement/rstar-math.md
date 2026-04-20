# rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking

Guan, Zhang et al. (Microsoft Research Asia, 2025). Shows that 1.5B–7B SLMs can match or surpass OpenAI o1 on competition math by combining MCTS-driven deep thinking with a *process preference model (PPM)*, both trained from scratch via four rounds of self-evolution — no distillation from a stronger teacher.

## Method
Three coupled innovations:
1. **Code-augmented CoT MCTS rollouts.** The policy SLM emits each step as a one-line NL CoT *plus* the corresponding Python; only steps whose code executes are kept as MCTS children. Selection uses UCT with `Q(s) = q(s)/N(s)`; PPM provides initial `q` once it exists, and terminal-guided back-prop updates `q(s_i)^k = q(s_i)^{k-1} + q(s_d)^k` with `q(s_d) ∈ {-1, +1}` from ground-truth answer match.
2. **Process Preference Model (PPM).** Sidesteps noisy per-step Q-value regression. For each step, pick the 2 highest-Q candidates that reach a correct final answer as positives and the 2 lowest-Q that lead to wrong answers as negatives, sharing the same prefix; train with Bradley-Terry pairwise ranking loss. Initialised from the policy SLM with a tanh scalar head.
3. **Four-round self-evolution recipe.**
   - R1: bootstrap with DeepSeek-Coder-V2-Instruct (236B) running MCTS @ 8 rollouts; terminal-guided Q only; train SLM-r1, weak PPM-r1.
   - R2: 7B SLM-r1 runs MCTS @ 16 rollouts → reliable PPM-r2.
   - R3: PPM-r2-augmented MCTS produces SLM-r3, PPM-r3.
   - R4: 64–128 rollouts on hard problems → 80.6% Olympiad coverage; final SLM-r4 / PPM-r4.
- Training corpus: 747k math problems (NuminaMath competition split + MetaMath + GPT-4 augmentations filtered by 3-of-10 self-consistency).

## Claims
- MATH benchmark: Qwen2.5-Math-7B 58.8% → **90.0%**, Qwen2.5-Math-1.5B 51.2% → 88.6%, Phi3-mini-3.8B 41.4% → 86.4% (Table 1); beats o1-preview (85.5%), matches o1-mini (90.0%).
- AIME 2024: **53.3%** (8/15 problems) for the 7B variant — top-20% of US high-school olympiad participants; beats o1-preview by +8.7%.
- Olympiad Bench 65.6%, College Math 60.5%, Omni-Math 50.5% with the 7B model.
- Per-round 747k coverage: 60.2% → 66.6% → 77.9% → **90.25%** (Table 2). Olympiad-level coverage 21.0% → 56.0% → 62.2% → 80.6%.
- PPM quality (with policy fixed at SLM-r1): MATH 75.2 → 87.0; AIME 10.0 → 43.3 across r1→r4 (Table 4).
- Authors observe emergent self-reflection in MCTS traces and a PPM preference for theorem-application steps.

## Sample efficiency
rStar-Math doesn't operate from a *single* seed example, but it is the strongest demonstration of single-problem amplification at scale: each of the 747k problems is run through 16–128 MCTS rollouts, generating thousands of step-level candidates per problem; only the 2 highest-mean-Q correct trajectories per problem enter SFT, and step-level positive/negative pairs feed the PPM. So one `(x, y)` produces both a high-quality SFT trajectory *and* dense preference supervision at every step. Auxiliary variability is structural (MCTS branching) rather than purely stochastic, and is filtered through two orthogonal verifiers: code execution (per step) and answer correctness (terminal). Critically, SLMs that initially solve few hard problems progressively expand the *solvable* set across rounds — the bootstrap turns a few seed solutions into a curriculum.

## Relevance to the project
rStar-Math is a template for "single-sample with verifier-gated variability" tailored to small models. For David's concept-based fine-tuning, three transferable ideas: (i) verifier-anchored variability (code execution as a per-step filter) gives much cleaner training data than temperature alone — directly addresses the failure mode STaR warns about; (ii) preference-pair training over Q-ranked siblings is more robust than absolute step scoring when Q is noisy — useful when "concept correctness" can only be ranked, not measured; (iii) the round-by-round expansion of the solvable set shows how a tight self-evolution loop turns a small initial competence into Olympiad-level coverage without an external teacher — exactly the regime David is targeting at 1–40B params.

## Source
- arXiv: 2501.04519
- Raw markdown: `../../../raw/research/single-sample-llm-learning/22-D-3-rstar-math.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/D-3-rstar-math.pdf`

## Related
- [[star]]
- [[self-rewarding-lm]]
- [[_overview]]
