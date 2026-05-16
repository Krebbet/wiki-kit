---
name: alphazero
description: AlphaZero — tabula-rasa self-play RL for chess, shogi, and Go. Single (policy, value) network updated via MCTS-derived visit-count targets and terminal game outcome. Structural template for MCTS-as-policy-improvement-oracle; closed-domain prototype for iterated target generation.
type: research
---

# Mastering Chess and Shogi by Self-Play with a General RL Algorithm (AlphaZero)

Silver, Hubert, Schrittwieser, et al. — DeepMind. arXiv:1712.01815 (2017). AlphaZero learns chess, shogi, and Go from random initialisation using only game rules and self-play, with no handcrafted features or human domain knowledge. Starting from scratch, it surpassed world-champion programs in all three games within 24 hours on TPU hardware.

**TL;DR.** One network $f_\theta(s) = (p, v)$, one reward (terminal game outcome), one policy-improvement operator (MCTS). Achieves superhuman chess/shogi/Go; independently rediscovers all major human chess openings.

## Method

A single deep residual convolutional network maps board state $s$ to a policy vector $p$ (move probabilities) and scalar value $v$ (expected outcome). Both players in each self-play game are controlled by MCTS guided by $f_\theta$.

**MCTS.** 800 simulations per move. At each state the algorithm selects the action balancing low visit count, high prior $p_a$, and high backed-up value. The search returns root visit-count distribution $\pi$ — the improved policy target.

**Training signal.** Terminal outcome $z \in \{-1, 0, +1\}$ (loss / draw / win) is determined by game rules. Loss:

$$(z - v)^2 - \pi^\top \log p + c\|\theta\|^2$$

Value head minimises MSE to outcome; policy head minimises cross-entropy to MCTS visit distribution $\pi$; $c\|\theta\|^2$ is L2 regularisation. No intermediate per-step reward.

**Key property.** The MCTS step is a **policy-improvement oracle**: $\pi$ is strictly better than $p$ under the current value function. Training $p \to \pi$ is iterated policy distillation — each cycle produces a stronger policy that generates better MCTS targets for the next cycle.

**Compute.** ~44M self-play games (chess); 5,000 first-gen TPUs for self-play, 64 second-gen TPUs for gradient updates. Superhuman chess in 4 hours, shogi in 2, Go in 8.

## Claims

- Defeated Stockfish 8 (64-thread, 1 GB hash) 25–0–25 in 100 chess games at 1 min/move.
- Defeated Elmo (CSA world champion) 43–2–5 in 100 shogi games.
- Searches ~80k positions/second in chess vs ~70M for Stockfish; compensates via neural-guided selective search.
- MCTS Elo scales more steeply with per-move time budget than alpha-beta search.
- Independently rediscovers all 12 major human chess openings (each played >100k times historically).
- Zero domain knowledge beyond game rules.

## Why this is load-bearing for single-sample concept learning

The **MCTS step as policy-improvement oracle** is AlphaZero's structural contribution to this wiki. MCTS generates targets $\pi$ strictly better than current policy $p$; training $p \to \pi$ is iterated distillation. The question this wiki asks — can a lookahead process (MCTS in games; some verifier or rollout in language) generate a one-step-better "concept exploration" target that a small LLM distils from a single sample? — is exactly what AlphaZero demonstrates in the closed-domain case.

Implicit curriculum via opponent strength is a side benefit: the opponent is always the current self, so effective training difficulty scales automatically without an explicit curriculum designer.

**Honest read: relevance is structural-template, not direct.** Game domain has crisp rules and a perfect verifier; there is no open-ended concept, no natural language, no analogue to single-sample constraint. AlphaZero provides an existence proof for the loop's viability; it does not instantiate the loop for concepts.

## Limitations

- Closed domain with crisp verifier. No analogue for open-ended domains where "concept" has no formal definition and no automatic win/loss signal.
- Extreme sample cost: 44M self-play games on thousands of TPUs; completely intractable for LLM fine-tuning.
- No generalisation across games: separate AlphaZero instance per game, no shared representation or transfer.
- No language or abstraction: network representations are never interpreted as concepts; no symbolic grounding.
- Opening-discovery analysis is post-hoc and correlational; no mechanistic claim about what the network "knows."

## Source

- `../../../raw/research/self-play-concept-learning/.ingest/01-alphazero.md`
- `../../../raw/research/self-play-concept-learning/01-01-alphazero.md`
- arXiv: https://arxiv.org/abs/1712.01815

## Related

- [[../rl-optimizers/_overview]] — policy-gradient / value-baseline lineage
- [[../self-improvement/rstar-math]] — MCTS + LLM cousin; language-domain successor
- [[../teacher-student-rl/_overview]] — MCTS-as-teacher structural analogue
- [[asymmetric-self-play]] — non-game RL extension of self-play
- [[understanding-self-play]] — proposer-is-everything contrast (AlphaZero's "proposer" is the policy itself via MCTS)
- [[_overview]] — theme synthesis
