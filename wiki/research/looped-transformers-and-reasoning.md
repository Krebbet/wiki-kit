# Looped Transformers and Reasoning

Saunshi et al. (Google Research, arXiv Oct. 2024) show that a k-layer transformer block looped L times nearly matches a full kL-layer non-looped model on reasoning tasks while using 1/L the parameters — establishing that many reasoning problems require depth but not parameter count. The paper provides both empirical evidence at 1B scale and theoretical results formalizing the equivalence between looped iterations and chain-of-thought steps. A central finding is that looped models exhibit a strict perplexity deficit vs. iso-FLOP non-looped models, yet consistently outperform them on reasoning-heavy benchmarks — a tradeoff that is not explained by any resolved mechanism.

## Architecture

The looped block is a standard k-layer transformer (self-attention + FFN) applied L times with full weight sharing: f^(L) = f ∘ f ∘ … ∘ f. Notation: **(k ⊗ L)** = k layers looped L times. Two baselines are used throughout:

- **Iso-param**: (k ⊗ 1) — same parameter count, single pass.
- **Iso-FLOP**: (kL ⊗ 1) — same compute, no looping, L× more parameters.

No routing, gating, or conditional compute is applied — all tokens traverse the same block every loop iteration. Loop count L is fixed at training/inference time; adaptive halting is not explored.

**Middle looping** variant: independent (non-looped) layers at the start and end of the network, with only the middle block looped. At 1B scale (k=4, middle variant) this yields better perplexity and more uniform benchmark improvements than plain looping, except on math word problems where plain (12 ⊗ 2) outperforms it (34.3% vs. 28.3%).

## Reasoning vs. Memorization Tradeoff

At 1B–1.5B parameter scale (24-layer base model, Pile dataset, 250B tokens), looped models show a consistent split across task categories:

- **Reasoning primitives and math word problems**: looped outperforms iso-FLOP non-looped for *all* tested parameter budgets k ∈ {4, 6, 8, 12}. Example: (12 ⊗ 2) scores 34.3% on math word problems vs. 29.3% for the 24-layer iso-FLOP baseline, with 50% of the parameters.
- **Validation perplexity**: looped models consistently underperform iso-FLOP baselines, covering only 34–50% of the perplexity gap across all k values.
- **Closed-book QA (memorization)**: looped models show no advantage at matched perplexity — the % gap on closed-book QA closely tracks the perplexity % gap (~37–58%), confirming looping does not help memorization.

The perplexity deficit is attributed to the reduced parameter count (1/L), but the mechanism behind the reasoning *advantage* is unresolved.

## Latent Thoughts / Chain-of-Thought Equivalence

Theorem 5.4 formalizes the connection: a looped transformer with m loops can simulate m steps of chain-of-thought reasoning from an (L+O(1))-layer non-looped transformer, via masking, shift-by-one attention, and MLP-based token decode/encode. This frames each loop iteration as an implicit "latent thought" step — architecturally equivalent to inference-time CoT scaling (O1, DeepSeek-R1 style) without explicit token generation.

## Theoretical Expressiveness

Four key results:

1. A 1-layer looped transformer with T = ⌈log₂ n⌉ loops solves n-element group composition, matching the best-known depth upper bound for non-looped models.
2. Any non-looped transformer with at most R distinct layers can be simulated by a 1-layer looped transformer with modest overhead (embedding size +R+2, hidden dim ×R).
3. p-hop induction is solvable by a 1-layer transformer looped ⌊log₂ p⌋+2 times, matching the non-looped lower bound (Sanford et al., 2024b).
4. CoT simulation equivalence (Theorem 5.4, above).

## Scale and Benchmarks

**Synthetic tasks**: dim=256, 8 heads, FFN=1024; Adafactor, 200k steps, batch=1024. Tasks: n-ary addition (n up to 32), p-hop induction (p=16,32, seq=256), i-GSM (DAG depth 4, modulo 7, ~4M train examples). (1 ⊗ 12) achieves ~99.9% on n-ary addition vs. 100% for (12 ⊗ 1) iso-FLOP; iso-param (1 ⊗ 1) scores 0.1%.

**Language modeling**: 1B–1.5B parameters, 24 layers, dim=2048, FFN=5120, 32 heads, Pile, 250B tokens, 400k steps cosine schedule. 19 downstream tasks across 4 groups: closed-book QA (4), open-book QA (5), math word problems (6), reasoning primitives (4). k-shot eval (5-shot for math and reasoning primitives).

**Depth scaling law**: accuracy ≈ α·log(D) + β where D = effective depth. The coefficient α_loop / α_base > 1 for reasoning tasks (e.g., 1.19× for reasoning primitives) — each doubling of loop count yields more per-task gain than each doubling of non-looped depth.

**Looping regularization** (post-hoc): a cosine similarity regularizer between successive k-layer blocks encourages weight-sharing without architectural modification; applied to the full 24-layer 1B baseline with λ_reg ∈ {1, 10}.

## Open Questions

- **Why does looping create a reasoning inductive bias?** The mechanism is explicitly flagged as unresolved (Section 3.3).
- Does the finding generalize to other reasoning forms (multimodal, commonsense)?
- A formal definition/taxonomy of "reasoning problems" is identified as an open problem.
- Inference-time scaling via variable loop counts (adaptive halting) is flagged as "a very promising future direction" but not explored.
- Which layers to loop and optimal looping strategies (middle vs. full, block size k) are deferred.

## Source
- `raw/research/thesis-foundations/05-latent-thoughts-looped.md` — "Reasoning with Latent Thoughts: On the Power of Looped Transformers," Saunshi et al., Google Research, arXiv Oct. 2024.

## Related
- [[universal-transformer]] — foundational weight-tied looped transformer; Latent-Thoughts formalizes and extends empirically.
- [[looped-language-models]] — Ouro scales the same weight-shared recurrent design to 7.7T tokens, adds adaptive exit, confirms reasoning lift.
- [[mixture-of-depths]] — both address adaptive depth but differ on mechanism (MoD: route tokens around blocks; this: loop same block).
- [[looped-vs-depth-scaling]] (open conflict) — Latent-Thoughts' finding that looped models have worse perplexity but better reasoning than isoFLOP non-looped is the one side of this conflict.
