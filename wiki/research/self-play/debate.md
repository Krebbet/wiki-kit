---
name: debate
description: AI Safety via Debate — two agents alternate statements on a question; a judge picks the winner. Complexity-theoretic claim that debate with optimal play extends a polynomial-time judge from NP to PSPACE. MNIST pixel-reveal experiment is the sole empirical result.
type: research
---

# AI Safety via Debate

Irving, Christiano, Amodei — OpenAI. arXiv:1805.00899 (2018). Two AI agents take turns making short statements about a question; a human (or learned) judge declares a winner. Central claim: in equilibrium it is harder to lie than to refute a lie, so agents learn to be honest without direct supervision. Complexity-theoretic analogy: debate with optimal play extends a polynomial-time judge from NP to PSPACE.

**TL;DR.** Zero-sum debate game + weak judge + self-play training $\Rightarrow$ agents converge to truthful strategies. Empirically demonstrated only on MNIST pixel-reveal; natural-language experiments are entirely deferred future work.

## Method

**Protocol.** Given question $q$, both agents state answers $a_0, a_1$, then alternate up to $K$ statements $s_0, \ldots, s_{K-1}$. The judge sees the full transcript $(q, a, s)$ and emits a binary decision. Reward: $+1$ win, $-1$ lose. Zero-sum; no per-step signal.

**Complexity claim.**

> **Theorem 1.** For any $L \in \text{PSPACE}$, there exists a polynomial-time judge such that optimal play in the debate game with polynomially many steps solves $L$.

Replacing the human judge with an arbitrary polynomial-time algorithm $H$, a fixed-depth-$n$ debate corresponds to $\Sigma_n^P$; as $n$ grows polynomially the reachable class becomes PSPACE. A weak judge can supervise agents solving problems exponentially harder than it could solve directly.

**MNIST experiment.** Two agents take turns revealing pixels of a digit image; the judge (trained on random sparse-pixel masks, then held fixed) sees only revealed pixels and classifies. Honest-agent win rate:

| Pixels | Sparse judge accuracy | Debate accuracy |
|--------|-----------------------|-----------------|
| 6 | 59.4% | 88.9% |
| 4 | 48.2% | 85.2% |

Precommit (agent locks in its claimed class before pixel reveals) is critical: without it, the liar adapts mid-game and the improvement shrinks substantially.

## Claims

- In equilibrium, truth-telling is the dominant strategy: refuting a lie is easier than defending one.
- A polynomial-time judge supervising debate agents can oversee problems in PSPACE.
- MNIST pixel-reveal: debate boosts a ~50% chance-level judge to >85% effective accuracy.
- At Nash equilibria: "Both agents try to tell the truth in the most convincing manner possible."
- Successful lies concentrate on visually similar digit pairs (e.g. 5→8, 4→9), consistent with judge confusion patterns.

## Relevance to single-sample concept learning

**Honest read: weak connection; included for family completeness and as a contrast.**

Debate is an **eval-time honesty mechanism**, not a train-time skill-installation mechanism. The agents do not update weights during a debate; the loop runs at inference time or as a training signal over many episodes across many questions. There is no single-sample regime: MNIST games span the full test set and the judge is pre-trained on thousands of examples. The self-play signal is dense (every game emits a win/loss), the structural opposite of single-sample.

The closest concept-learning hook is the pixel-reveal game itself: agents implicitly learn which feature subsets are **diagnostic for a concept** — adversarial feature selection as an implicit curriculum. This is evocative of concept decomposition but the paper does not develop it. The wiki's "train from one example" frame has no direct counterpart here.

Primary value in this wiki: contrast case and family anchor. Debate shows what a multi-agent honesty loop looks like when the training signal is eval-time rather than a single-concept gradient update.

## Limitations

- Theoretical paper; MNIST is the only ML experiment; all other experiments are deferred.
- Relies on a strong, well-calibrated judge; the required competence threshold is not characterised empirically.
- No convergence guarantee for self-play in the debate setting; training-time cycles (learn honesty → forget how to refute → lie) are a known risk.
- PSPACE equivalence breaks for stochastic environments.
- Agents trained for debate may be weaker than unconstrained agents (performance penalty concern; not tested).
- Natural-language debate is explicitly future work: "At this point debate is a proposal only for the natural language case."
- Second-player structural advantage; remedies proposed but not tested.

## Source

- `../../../raw/research/self-play-concept-learning/.ingest/03-debate.md`
- `../../../raw/research/self-play-concept-learning/02-03-debate.md`
- arXiv: https://arxiv.org/abs/1805.00899

## Related

- [[../self-improvement/multi-turn-policy-verifier]] — PAG single-LLM alternation; debate's closest structural cousin
- [[../critique-self-correction/_overview]] — textual critique substitutes for supervision; similar honesty-extraction spirit
- [[../self-improvement/self-rewarding-lm]] — LLM-as-judge; limiting case where the debate judge is the model itself
- [[spag]] — concept-game with adversarial structure; language-domain sibling
- [[_overview]] — theme synthesis
