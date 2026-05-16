---
name: asymmetric-self-play
description: Sukhbaatar et al. 2018 — two-agent (Alice/Bob) self-play with an asymmetric time-based reward that automatically drives Alice's task proposals to the edge of Bob's competence, yielding an unsupervised curriculum without any explicit difficulty signal.
type: research
---

# Asymmetric Self-Play: Intrinsic Motivation and Automatic Curricula

Sainbayar Sukhbaatar, Zeming Lin, Ilya Kostrikov, Gabriel Synnaeve, Arthur Szlam, Rob Fergus. ICLR 2018. arXiv:1703.05407. Alice and Bob share the same physical environment: Alice proposes tasks by acting them out (state-action sequences), Bob must undo or repeat them, and a reward structure without any external difficulty signal automatically pushes Alice to stay at the frontier of Bob's competence. Unsupervised self-play significantly reduces sample complexity on downstream target tasks across gridworld (MazeBase), continuous control (MountainCar, SwimmerGather), and RTS (StarCraft build-order).

## Method

Alice and Bob are two separate policy heads with parameters $\theta_A$, $\theta_B$ operating in the same environment. Two regimes:

**Reversible.** Alice starts from $s_0$, acts until STOP at time $t_A$, reaching $s^*$. Bob must return to $s_0$.

**Resettable.** After Alice STOPs, environment resets to $s_0$; Bob must reach $s^*$ (repeat Alice's trajectory).

Alice's policy takes initial and current state:

$$a^A = \pi_A(s_t, s_0;\, \theta_A)$$

Bob's policy takes current and target state:

$$a^B = \pi_B(s_t, s^*;\, \theta_B)$$

Rewards:

$$R^B = -\gamma t_B \tag{1}$$

$$R^A = \gamma \max(0,\, t_B - t_A) \tag{2}$$

where $t_B$ is Bob's steps (set to $t_{\max} - t_A$ on failure), $t_A$ is Alice's steps, and $\gamma$ balances internal vs. external reward scale. At test time Bob is deployed as $\pi_B(s_t, \emptyset;\, \theta_B)$ with no Alice.

**Why the reward is self-regulating.** The $\max(0,\cdot)$ kills reward when Bob is already faster than Alice (no benefit from trivially easy tasks). When Bob always fails ($t_B = t_{\max} - t_A$), Alice's reward is $\gamma(t_{\max} - 2t_A)$, which decreases with $t_A$ — Alice is doubly penalised for spending many steps on impossible tasks. The equilibrium is Alice targeting the edge of Bob's competence: the zone where Bob sometimes succeeds but barely.

**Theoretical guarantee (tabular, deterministic, finite state).** In the tabular, Markovian setting, if $\pi_A$ and $\pi_B$ are in Nash equilibrium, $\pi_B$ is the universal fast policy that transitions between any reachable pair of states in the minimum expected number of steps (Section 2.2 proof).

## Claims

- Self-play with asymmetric reward accelerates learning over target-task-only training in Long Hallway, MazeBase, MountainCar, SwimmerGather, and StarCraft.
- Performance is at least competitive with VIME and SimHash (intrinsic-motivation baselines that are more complex to implement).
- Random Alice performs poorly — bilateral training between Alice and Bob, not random exploration, drives the curriculum.
- In MazeBase, Alice's proposals progress from 0 objects touched → 1 → 2 → 3, tracking Bob's growing competence (Fig. 3 curriculum plot).
- Internal reward scale $\gamma$ must be hand-tuned per environment (Table 1: range 0.01 to 0.1).

## Why this is load-bearing for single-sample concept learning

Asymmetric self-play is the **cleanest pre-LLM template for self-play in non-game, non-symmetric RL**. The Alice/Bob structure is the canonical instantiation of "proposer generates a task, learner attempts it, reward steers proposer to the frontier" — every LLM self-play paper from 2023 onward inherits this skeleton. Understanding where the skeleton works and where it breaks is prerequisite to designing the linguistic analogue.

The $\max(0,\cdot)$ trick in equation (2) is load-bearing for curriculum emergence. It eliminates the need for any external difficulty estimator, task parameterisation, or learning-progress oracle. The same design decision — reward zero for trivial tasks, reward zero for impossible tasks, reward positive only in the middle — recurs in [[../teacher-student-rl/soar-edge-of-learnability]]'s student-improvement signal and in [[understanding-self-play]]'s analysis of proposer reward functions.

The reversibility/resettability assumption is the honest limitation: Alice communicates tasks by *demonstrating* them in a physical environment that can be undone or reset. There is no direct linguistic analogue — an LLM cannot "reset" a context window to a prior state after generating a question. Appendix F.2 explicitly flags this: parameterising tasks, communicating them, and ensuring appropriate difficulty in general settings remains unsolved. The LLM self-play literature (AZR, SPIRAL, SQLM) resolves this by generating task descriptions in natural language and using code execution or game rules as the verifier — a fundamentally different communication channel.

Alice can collapse to a narrow subset of proposals (Fig. 8, SwimmerGather: Alice develops a preferred direction). This mode-collapse problem recurs in LLM self-play as entropy collapse ([[understanding-self-play]]) and is the primary failure mode the proposer-training literature tries to fix.

## Limitations

- All experiments in gridworld, continuous control, or RTS. No symbolic, compositional, or linguistic tasks.
- Reversibility/resettability is a hard assumption with no clean linguistic analogue (Appendix F.2).
- Function approximation breaks the theoretical fast-policy guarantee; only valid in the tabular, Markovian setting.
- Alice can concentrate proposals on a narrow challenge subset (mode collapse with function approximation).
- $\gamma$ is hand-tuned per environment; no principled selection rule.
- Transfer degrades when self-play environment dynamics differ from target task (Appendix C.1).

## Source

- `../../../raw/research/self-play-concept-learning/.ingest/02-asymmetric-self-play.md`
- `../../../raw/research/self-play-concept-learning/10-02-asymmetric-self-play.md`
- arXiv: https://arxiv.org/abs/1703.05407

## Related

- [[../teacher-student-rl/soar-edge-of-learnability]] — LLM-era successor; explicit bilevel meta-RL with student-improvement reward vs. implicit reward here
- [[../curriculum-and-decomposition/poet]] — co-evolving env + agent via explicit selection vs. reward-driven self-regulation within a fixed environment
- [[../curriculum-and-decomposition/acl-deep-rl-survey]] — LP, ALP-GMM; external progress estimation vs. emergent curriculum here
- [[../self-improvement/multi-turn-policy-verifier]] — single-LLM role alternation (PAG); shares role-alternation intuition but uses token-level separation, not separate parameter sets
- [[understanding-self-play]] — mechanistic analysis of which component (proposer vs. solver) drives improvement in LLM self-play
- [[sqlm]] — LLM analogue of Alice/Bob in language
- [[_overview]] — theme synthesis
